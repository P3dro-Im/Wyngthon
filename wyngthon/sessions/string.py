import base64
import ipaddress
import struct

from .abstract import Session
from .memory import MemorySession
from ..crypto import AuthKey

# Version 1: the server address is an IP, stored as raw IPv4/IPv6 bytes.
#   dc_id (1 byte) | ip (4 or 16 bytes) | port (2 bytes) | auth key (256 bytes)
_STRUCT_PREFORMAT = '>B{}sH256s'

# Version 2: the server address is a host name, stored as UTF-8 text.
#   dc_id (1 byte) | port (2 bytes) | host length (1 byte) | host | auth key
_HOST_HEADER = '>BHB'
_HOST_HEADER_SIZE = struct.calcsize(_HOST_HEADER)
_KEY_SIZE = 256

IP_VERSION = '1'
HOST_VERSION = '2'
CURRENT_VERSION = HOST_VERSION


class StringSession(MemorySession):
    """
    This session file can be easily saved and loaded as a string. According
    to the initial design, it contains only the data that is necessary for
    successful connection and authentication, so takeout ID is not stored.

    It is thought to be used where you don't want to create any on-disk
    files but would still like to be able to save and load existing sessions
    by other means.

    The first character of the string is its format version. If the server
    address is an IP address, version ``1`` is used (the IP is stored as raw
    bytes). If it is a host name, such as the default server, version ``2``
    is used so the name is kept as is: connecting through a host name is
    required for the TLS certificate of the server to be verified. Strings
    of both versions can be loaded.

    You can use custom `encode` and `decode` functions, if present:

    * `encode` definition must be ``def encode(value: bytes) -> str:``.
    * `decode` definition must be ``def decode(value: str) -> bytes:``.
    """
    def __init__(self, string: str = None):
        super().__init__()
        if string:
            version, string = string[0], string[1:]
            if version == IP_VERSION:
                self._load_ip(string)
            elif version == HOST_VERSION:
                self._load_host(string)
            else:
                raise ValueError('Not a valid string')

    def _load_ip(self, string):
        ip_len = 4 if len(string) == 352 else 16
        self._dc_id, ip, self._port, key = struct.unpack(
            _STRUCT_PREFORMAT.format(ip_len), StringSession.decode(string))

        self._server_address = ipaddress.ip_address(ip).compressed
        if any(key):
            self._auth_key = AuthKey(key)

    def _load_host(self, string):
        try:
            data = StringSession.decode(string)
            dc_id, port, host_len = struct.unpack_from(_HOST_HEADER, data)
            if host_len == 0 or \
                    len(data) != _HOST_HEADER_SIZE + host_len + _KEY_SIZE:
                raise ValueError

            end = _HOST_HEADER_SIZE + host_len
            host = data[_HOST_HEADER_SIZE:end].decode('utf-8')
            key = data[end:]
        except (ValueError, struct.error):
            # binascii.Error and UnicodeDecodeError are ValueErrors too
            raise ValueError('Not a valid string') from None

        self._dc_id = dc_id
        self._port = port
        self._server_address = host
        if any(key):
            self._auth_key = AuthKey(key)

    @staticmethod
    def encode(x: bytes) -> str:
        return base64.urlsafe_b64encode(x).decode('ascii')

    @staticmethod
    def decode(x: str) -> bytes:
        return base64.urlsafe_b64decode(x)

    def save(self: Session):
        if not self.auth_key:
            return ''

        address = self.server_address
        try:
            ip = ipaddress.ip_address(address).packed
        except ValueError:
            # Not an IP address: keep the host name (version 2)
            host = (address or '').encode('utf-8')
            if not 0 < len(host) <= 255:
                raise ValueError(
                    'The server address must have between 1 and 255 bytes '
                    'to be saved in a string session') from None

            return HOST_VERSION + StringSession.encode(
                struct.pack(_HOST_HEADER, self.dc_id, self.port, len(host))
                + host
                + self.auth_key.key
            )

        return IP_VERSION + StringSession.encode(struct.pack(
            _STRUCT_PREFORMAT.format(len(ip)),
            self.dc_id,
            ip,
            self.port,
            self.auth_key.key
        ))
