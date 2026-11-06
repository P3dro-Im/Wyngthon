"""
This module holds several utilities regarding RSA and server fingerprints.
"""

import os
import struct
from hashlib import sha1, sha256

try:
    import rsa
    import rsa.core
except ImportError:
    rsa = None
    raise ImportError('Missing module "rsa", please install via pip.')

from ..tl import TLObject
from . import AES


# {fingerprint: (RSA key, old)} dictionary
_server_keys = {}


def get_byte_array(integer):
    """Return the variable length bytes corresponding to the given int."""
    return int.to_bytes(
        integer,
        (integer.bit_length() + 8 - 1) // 8,
        byteorder='big',
        signed=False,
    )


def _compute_fingerprint(key):
    """
    Given an RSA key, computes its fingerprint like Telegram does.

    :param key: the RSA key.
    :return: its 8-bytes-long fingerprint.
    """
    n = TLObject.serialize_bytes(get_byte_array(key.n))
    e = TLObject.serialize_bytes(get_byte_array(key.e))

    return struct.unpack(
        '<q',
        sha1(n + e).digest()[-8:],
    )[0]


def add_key(pub, *, old):
    """Adds a new public key to be used when encrypting data."""
    global _server_keys

    key = rsa.PublicKey.load_pkcs1(pub)

    _server_keys[_compute_fingerprint(key)] = (
        key,
        old,
    )


def _rsa_raw_encrypt(payload, key):
    """
    Perform raw RSA modular exponentiation.

    The payload must represent an integer smaller than RSA modulus n.
    """
    payload_int = int.from_bytes(
        payload,
        byteorder='big',
        signed=False,
    )

    # rsa.core.encrypt_int() also checks this, but checking here gives
    # us a clean failure and prevents accidental invalid RSA input.
    if payload_int >= key.n:
        raise OverflowError(
            'RSA payload is greater than or equal to modulus n'
        )

    encrypted = rsa.core.encrypt_int(
        payload_int,
        key.e,
        key.n,
    )

    return encrypted.to_bytes(
        256,
        byteorder='big',
    )


def _secure_encrypt(data, key):
    """
    Generate the secure encrypted data used by Telegram Web for
    req_DH_params.

    This follows the algorithm extracted from the Web Worker:

        g = data + random padding to 192 bytes
        reverse(g)

        random 32-byte AES key

        SHA256(aes_key + g)

        plaintext =
            reverse(g) + SHA256(aes_key + g)

        AES-256-IGE(plaintext, aes_key, zero_iv)

        masked_key =
            aes_key XOR SHA256(ciphertext)

        secure_payload =
            masked_key + ciphertext

        RSA:
            secure_payload^e mod n

    The Worker retries up to 20 times if the generated RSA payload
    is greater than or equal to the RSA modulus n.
    """

    # Worker checks this before creating the 192-byte buffer.
    if len(data) > 144:
        raise ValueError(
            'PQ inner data is too large: {} bytes'.format(
                len(data)
            )
        )

    # ---------------------------------------------------------
    # Step 1
    # g = data + random padding
    # ---------------------------------------------------------
    padded = data + os.urandom(
        192 - len(data)
    )

    # ---------------------------------------------------------
    # Step 2
    # _ = reverse(g)
    # ---------------------------------------------------------
    reversed_data = padded[::-1]

    # ---------------------------------------------------------
    # Step 3-10
    # Generate a random AES key and construct the payload.
    #
    # The Worker retries this entire part up to 20 times.
    # ---------------------------------------------------------
    for attempt in range(20):
        # Random 256-bit AES key.
        aes_key = os.urandom(32)

        # SHA256(aes_key + g)
        aes_hash = sha256(
            aes_key + padded
        ).digest()

        # reverse(g) + SHA256(aes_key + g)
        plaintext = (
            reversed_data
            + aes_hash
        )

        # AES-256-IGE with a 32-byte zero IV.
        encrypted = AES.encrypt_ige(
            plaintext,
            aes_key,
            bytes(32),
        )

        # SHA256(ciphertext)
        ciphertext_hash = sha256(
            encrypted
        ).digest()

        # aes_key XOR SHA256(ciphertext)
        masked_key = bytes(
            a ^ b
            for a, b in zip(
                aes_key,
                ciphertext_hash,
            )
        )

        # masked_key + ciphertext
        secure_payload = (
            masked_key
            + encrypted
        )

        # Must always be exactly 256 bytes.
        if len(secure_payload) != 256:
            raise ValueError(
                'Secure RSA payload must be 256 bytes, got {}'.format(
                    len(secure_payload)
                )
            )

        # -----------------------------------------------------
        # Critical Worker check:
        #
        # if (payload >= RSA_n)
        #     continue
        # -----------------------------------------------------
        payload_int = int.from_bytes(
            secure_payload,
            byteorder='big',
            signed=False,
        )

        if payload_int >= key.n:
            continue

        # Payload is valid for raw RSA.
        encrypted_int = rsa.core.encrypt_int(
            payload_int,
            key.e,
            key.n,
        )

        return encrypted_int.to_bytes(
            256,
            byteorder='big',
        )

    raise RuntimeError(
        'Failed to generate RSA payload smaller than modulus '
        'after 20 attempts'
    )


def encrypt(
    fingerprint,
    data,
    *,
    use_old=False,
    secure=False,
):
    """
    Encrypt data using the Telegram RSA public key.

    With secure=False:
        Standard MTProto RSA encryption:

            SHA1(data) + data + random padding

    With secure=True:
        Telegram Web secure encryption used for req_DH_params.
    """
    global _server_keys

    key, old = _server_keys.get(
        fingerprint,
        [None, None],
    )

    if (not key) or (old and not use_old):
        return None

    # ---------------------------------------------------------
    # Telegram Web secure RSA
    # ---------------------------------------------------------
    if secure:
        return _secure_encrypt(
            data,
            key,
        )

    # ---------------------------------------------------------
    # Standard MTProto RSA
    # ---------------------------------------------------------
    to_encrypt = (
        sha1(data).digest()
        + data
        + os.urandom(
            235 - len(data)
        )
    )

    return _rsa_raw_encrypt(
        to_encrypt,
        key,
    )


# =============================================================
# Default Telegram RSA public keys
# =============================================================

for pub in (
    '''-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEAxF//0M0+/5PzgdNagTX+J+dJgr75ZCTuiG8i4x7YwmJF+jiOGCjm
7X7BLCaMc1+hOZYDL3+Gvle/AKykW1qouaCJMVx/H+2l8LFXLelZ2PLawTb8A7Bl
TqWzL3db5BugMNWziL9TuhR8In1bwKY07QVpR9in5zjAsAGLBk+mGt0DnVyMf1Xo
p2lLCFNmm0F4ykcAeaLCCIPbGWddliLY8xEEhI4GO2l1U3kZMwIOdOnAGJFtgUAo
Te+FHR6F1s9adCVZB1teL/hf9R+WmekJwygVz0MYEH7y6U49T45+/W7OF6X6g0W0
j1uSSrsY4qN7twxbTad9zdGZ7ys+9v+PuQIDAQAB
-----END RSA PUBLIC KEY-----''',

    '''-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEAyr+18Rex2ohtVy8sroGPBwXD3DOoKCSpjDqYoXgCqB7ioln4eDCF
fOBUlfXUEvM/fnKCpF46VkAftlb4VuPDeQSS/ZxZYEGqHaywlroVnXHIjgqoxiAd
192xRGreuXIaUKmkwlM9JID9WS2jUsTpzQ91L8MEPLJ/4zrBwZua8W5fECwCCh2c
9G5IzzBm+otMS/YKwmR1olzRCyEkyAEjXWqBI9Ftv5eG8m0VkBzOG655WIYdyV0H
fDK/NWcvGqa0w/nriMD6mDjKOryamw0OP9QuYgMN0C9xMW9y8SmP4h92OAWodTYg
Y1hZCxdv6cs5UnW9+PWvS+WIbkh+GaWYxwIDAQAB
-----END RSA PUBLIC KEY-----''',
):
    add_key(
        pub,
        old=False,
    )