import asyncio
import collections
import logging
import os
import socket

try:
    import aiohttp
except ImportError:
    aiohttp = None

_log = logging.getLogger(__name__)

from .tcpabridged import AbridgedPacketCodec
from .connection import ObfuscatedConnection

from ...crypto import AESModeCTR


class WebSocketReader:
    """
    Adapter that wraps an aiohttp WebSocket connection and exposes
    the readexactly(n) interface expected by PacketCodec.
    """

    __slots__ = (
        '_ws',
        '_chunks',
        '_chunk_offset',
        '_total_len',
    )

    def __init__(self, ws):
        self._ws = ws
        self._chunks = collections.deque()
        self._chunk_offset = 0
        self._total_len = 0

    async def readexactly(self, n):
        while self._total_len < n:
            try:
                msg = await self._ws.receive()
            except Exception as e:
                _log.debug(
                    'WebSocket receive error: %s',
                    e,
                )
                break

            if msg.type in (
                aiohttp.WSMsgType.CLOSE,
                aiohttp.WSMsgType.CLOSING,
                aiohttp.WSMsgType.CLOSED,
            ):
                break

            if msg.type == aiohttp.WSMsgType.ERROR:
                break

            # Ignore non-data WebSocket messages.
            if msg.type not in (
                aiohttp.WSMsgType.BINARY,
                aiohttp.WSMsgType.TEXT,
            ):
                continue

            data = msg.data

            if isinstance(data, str):
                data = data.encode()

            if not data:
                continue

            self._chunks.append(data)
            self._total_len += len(data)

        if self._total_len < n:
            raise IOError(
                'WebSocket closed while reading'
            )

        # Fast path:
        # requested data exists entirely inside first chunk.
        first = self._chunks[0]

        first_avail = (
            len(first) - self._chunk_offset
        )

        if first_avail >= n:
            result = first[
                self._chunk_offset:
                self._chunk_offset + n
            ]

            self._chunk_offset += n
            self._total_len -= n

            if self._chunk_offset >= len(first):
                self._chunks.popleft()
                self._chunk_offset = 0

            return result

        # Slow path:
        # requested data spans multiple WebSocket frames.
        parts = bytearray(n)
        offset = 0
        remaining = n

        if self._chunk_offset > 0:
            chunk = self._chunks[0]

            avail = (
                len(chunk) - self._chunk_offset
            )

            parts[
                offset:
                offset + avail
            ] = memoryview(chunk)[
                self._chunk_offset:
            ]

            offset += avail
            remaining -= avail

            self._chunks.popleft()
            self._chunk_offset = 0

        while remaining > 0:
            chunk = self._chunks.popleft()
            chunk_len = len(chunk)

            if chunk_len <= remaining:
                parts[
                    offset:
                    offset + chunk_len
                ] = chunk

                offset += chunk_len
                remaining -= chunk_len

            else:
                parts[
                    offset:
                    offset + remaining
                ] = memoryview(chunk)[
                    :remaining
                ]

                self._chunks.appendleft(chunk)
                self._chunk_offset = remaining
                remaining = 0

        self._total_len -= n

        if not self._chunks:
            self._chunk_offset = 0

        result = bytes(parts)
        return result


class WebSocketWriter:
    """
    Adapter that wraps an aiohttp WebSocket connection and exposes
    write(), drain(), close() and wait_closed().
    """

    __slots__ = (
        '_ws',
        '_pending',
    )

    def __init__(self, ws):
        self._ws = ws
        self._pending = bytearray()

    def write(self, data):
        self._pending.extend(data)

    async def drain(self):
        if not self._pending:
            return

        data = bytes(self._pending)
        
        self._pending.clear()

        await self._ws.send_bytes(data)

    def close(self):
        # Actual WebSocket closing is done asynchronously by
        # wait_closed().
        pass

    async def wait_closed(self):
        if self._ws is None:
            return

        try:
            await self._ws.close()
        except Exception as e:
            _log.debug(
                'WebSocket close error: %s',
                e,
            )


class WebSocketObfuscatedIO:
    """
    Wyngthon-compatible obfuscated transport running over
    WebSocket binary frames.
    """

    header = None

    def __init__(self, connection):
        self._reader = connection._reader
        self._writer = connection._writer

        (
            self.header,
            self._encrypt,
            self._decrypt,
        ) = self._init_header(
            connection.packet_codec
        )

    @staticmethod
    def _init_header(packet_codec):
        keywords = (
            b'PVrG',
            b'GET ',
            b'POST',
            b'\xee\xee\xee\xee',
        )

        while True:
            random = os.urandom(64)

            if (
                random[0] != 0xef
                and random[:4] not in keywords
                and random[4:8] != b'\0\0\0\0'
            ):
                break

        random = bytearray(random)

        random_reversed = random[
            55:7:-1
        ]

        encrypt_key = bytes(
            random[8:40]
        )

        encrypt_iv = bytes(
            random[40:56]
        )

        decrypt_key = bytes(
            random_reversed[:32]
        )

        decrypt_iv = bytes(
            random_reversed[32:48]
        )

        encryptor = AESModeCTR(
            encrypt_key,
            encrypt_iv,
        )

        decryptor = AESModeCTR(
            decrypt_key,
            decrypt_iv,
        )

        random[56:60] = (
            packet_codec.obfuscate_tag
        )

        random[56:64] = (
            encryptor.encrypt(
                bytes(random)
            )[56:64]
        )

        return (
            random,
            encryptor,
            decryptor,
        )

    async def readexactly(self, n):
        raw = await self._reader.readexactly(n)
        decrypted = self._decrypt.encrypt(raw)
        return decrypted

    def write(self, data):
        encrypted = self._encrypt.encrypt(data)

        self._writer.write(encrypted)


class ConnectionWebSocket(ObfuscatedConnection):
    """
    WebSocket connection using Wyngthon's obfuscated transport
    and abridged packet codec.

    The IP, port and DC ID are supplied by TelegramBaseClient.
    """

    obfuscated_io = WebSocketObfuscatedIO
    packet_codec = AbridgedPacketCodec

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._ws = None
        self._session = None

    async def _connect(self, timeout=None, ssl=None):
        if aiohttp is None:
            raise ImportError(
                'ConnectionWebSocket requires aiohttp. '
                'Install it with: pip install aiohttp'
            )

        # These values are supplied by Connection.__init__()
        # and originate from TelegramBaseClient.
        host = self._ip
        port = self._port

        # TelegramBaseClient decides the actual DC/host/port.
        # Port 443 uses secure WebSocket.
        protocol = (
            'wss'
            if port == 443
            else 'ws'
        )

        url = (
            f'{protocol}://'
            f'{host}:{port}/apiws'
        )

        headers = {
            'Origin': 'https://web.wyng.ir',
        }

        timeout_obj = None

        if timeout is not None:
            timeout_obj = aiohttp.ClientTimeout(
                total=timeout
            )

        self._session = aiohttp.ClientSession(
            timeout=timeout_obj
        )

        try:
            self._ws = await self._session.ws_connect(
                url,
                headers=headers,
                protocols=('binary',),
                max_msg_size=2 ** 24,
            )

        except Exception:
            try:
                await self._session.close()
            except Exception:
                pass

            self._session = None
            self._ws = None

            raise

        self._reader = WebSocketReader(
            self._ws
        )

        self._writer = WebSocketWriter(
            self._ws
        )

        # Try to configure the underlying TCP socket.
        # This is optional because aiohttp does not guarantee
        # that its internal transport is publicly exposed.
        try:
            ws_writer = getattr(
                self._ws,
                '_writer',
                None,
            )

            if ws_writer is not None:
                transport = getattr(
                    ws_writer,
                    '_transport',
                    None,
                )

                if transport is not None:
                    sock = transport.get_extra_info(
                        'socket'
                    )

                    if sock is not None:
                        try:
                            sock.setsockopt(
                                socket.IPPROTO_TCP,
                                socket.TCP_NODELAY,
                                1,
                            )
                        except OSError as e:
                            self._log.debug(
                                'Could not set TCP_NODELAY: %s',
                                e,
                            )

        except Exception as e:
            self._log.debug(
                'Could not configure WebSocket socket: %s',
                e,
            )

        # Keep Wyngthon's normal initialization.
        self._codec = self.packet_codec(self)

        self._init_conn()

        await self._writer.drain()

    async def disconnect(self):
        """
        Close the WebSocket and aiohttp session.
        """

        # Let Wyngthon cancel its send/receive tasks and perform
        # its normal connection cleanup first.
        try:
            await super().disconnect()
        except Exception:
            # Continue closing the actual WebSocket/session even
            # if the parent cleanup raises.
            self._log.debug(
                'Error during parent disconnect',
                exc_info=True,
            )

        if self._ws is not None:
            try:
                await self._ws.close()
            except Exception as e:
                self._log.debug(
                    'WebSocket close error: %s',
                    e,
                )

            self._ws = None

        if self._session is not None:
            try:
                await self._session.close()
            except Exception as e:
                self._log.debug(
                    'aiohttp session close error: %s',
                    e,
                )

            self._session = None