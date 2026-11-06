import struct

from .connection import Connection, PacketCodec


class AbridgedPacketCodec(PacketCodec):
    tag = b'\xef'
    obfuscate_tag = b'\xef\xef\xef\xef'

    def encode_packet(self, data):
        length = len(data) >> 2
        if length < 127:
            length = struct.pack('B', length)
        else:
            length = b'\x7f' + int.to_bytes(length, 3, 'little')
        return length + data

    async def read_packet(self, reader):
        first = await reader.readexactly(1)

        length = struct.unpack('<B', first)[0]

        if length >= 127:
            raw_length = await reader.readexactly(3)

            length = struct.unpack(
                '<i',
                raw_length + b'\0'
            )[0]

        body = await reader.readexactly(length << 2)

        return body


class ConnectionTcpAbridged(Connection):
    """
    This is the mode with the lowest overhead, as it will
    only require 1 byte if the packet length is less than
    508 bytes (127 << 2, which is very common).
    """
    packet_codec = AbridgedPacketCodec
