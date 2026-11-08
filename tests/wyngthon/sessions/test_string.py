import base64
import struct

import pytest

from wyngthon.crypto import AuthKey
from wyngthon.sessions import StringSession

KEY = bytes(range(256))


def make_session(address, dc_id=2, port=443, key=KEY):
    session = StringSession()
    session.set_dc(dc_id, address, port)
    if key is not None:
        session.auth_key = AuthKey(key)
    return session


def assert_same(restored, address, dc_id=2, port=443, key=KEY):
    assert restored.dc_id == dc_id
    assert restored.server_address == address
    assert restored.port == port
    assert restored.auth_key.key == key


def test_host_name_round_trip():
    """The default server is a host name, which must survive save/load."""
    saved = make_session('web.wyng.ir').save()
    assert saved[0] == '2'
    assert_same(StringSession(saved), 'web.wyng.ir')


def test_host_name_is_kept_exactly():
    saved = make_session('Some-Host.example.org', dc_id=5, port=8443).save()
    assert_same(StringSession(saved), 'Some-Host.example.org', 5, 8443)


@pytest.mark.parametrize('address', ['149.154.167.51', '2001:67c:4e8:f004::a'])
def test_ip_round_trip_keeps_version_1(address):
    saved = make_session(address).save()
    assert saved[0] == '1'
    assert_same(StringSession(saved), address)


def test_ipv4_string_has_the_original_length():
    assert len(make_session('1.2.3.4').save()) == 353


def test_loads_string_written_by_older_versions():
    raw = struct.pack('>B4sH256s', 2, bytes([1, 2, 3, 4]), 443, KEY)
    old = '1' + base64.urlsafe_b64encode(raw).decode('ascii')
    assert_same(StringSession(old), '1.2.3.4')


def test_save_without_auth_key_is_empty():
    assert make_session('web.wyng.ir', key=None).save() == ''


def test_empty_string_makes_a_new_session():
    assert StringSession('').auth_key is None
    assert StringSession(None).auth_key is None


def test_unknown_version_is_rejected():
    saved = make_session('web.wyng.ir').save()
    with pytest.raises(ValueError):
        StringSession('9' + saved[1:])


@pytest.mark.parametrize('broken', ['2', '2AAAA', '2!!!!', '2' + 'A' * 10])
def test_corrupt_host_string_is_rejected(broken):
    with pytest.raises(ValueError):
        StringSession(broken)


def test_truncated_host_string_is_rejected():
    saved = make_session('web.wyng.ir').save()
    with pytest.raises(ValueError):
        StringSession(saved[:-8])


def test_zero_length_host_is_rejected():
    raw = struct.pack('>BHB', 2, 443, 0) + KEY
    with pytest.raises(ValueError):
        StringSession('2' + base64.urlsafe_b64encode(raw).decode('ascii'))


def test_too_long_host_cannot_be_saved():
    with pytest.raises(ValueError):
        make_session('a' * 256 + '.example').save()


def test_missing_address_cannot_be_saved():
    session = StringSession()
    session.auth_key = AuthKey(KEY)
    with pytest.raises(ValueError):
        session.save()
