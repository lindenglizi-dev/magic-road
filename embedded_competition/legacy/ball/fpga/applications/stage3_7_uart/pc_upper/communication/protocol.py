"""Pure Python streaming protocol; no serial or Qt dependency."""
from dataclasses import dataclass
from enum import IntEnum
import time

class Command(IntEnum):
    MODE = 0x01
    SET_PARAM = 0x02
    GET_STATUS = 0x03
    RESULT = 0x80
    ACK = 0x81
    NACK = 0x82
    ROI_CONFIG = 0x10
    ROI_QUERY = 0x11
    SOURCE_SELECT = 0x20
    IMAGE_BEGIN = 0x30
    IMAGE_DATA = 0x31
    IMAGE_END = 0x32
    IMAGE_ABORT = 0x33
    ROI_STATUS = 0x90

def crc16(data):
    crc = 0xffff
    for value in data:
        crc ^= value << 8
        for _ in range(8):
            crc = ((crc << 1) ^ (0x1021 if crc & 0x8000 else 0)) & 0xffff
    return crc

@dataclass(frozen=True)
class Frame:
    seq: int
    command: int
    data: bytes

def encode(command, data=b'', seq=0):
    if len(data) > 240:
        raise ValueError('负载超过 240 字节')
    body = bytes([2, seq, command, len(data)]) + bytes(data)
    return b'\xaa\x55' + body + crc16(body).to_bytes(2, 'little') + b'\x0d\x0a'

class Decoder:
    def __init__(self, timeout=0.1):
        self.buffer = bytearray()
        self.last = None
        self.timeout = timeout

    def feed(self, data, now=None):
        now = time.monotonic() if now is None else now
        if self.last is not None and now - self.last > self.timeout:
            self.buffer.clear()
        self.last = now
        self.buffer.extend(data)
        frames = []
        while True:
            start = self.buffer.find(b'\xaa\x55')
            if start < 0:
                self.buffer[:] = b'\xaa' if self.buffer.endswith(b'\xaa') else b''
                break
            del self.buffer[:start]
            if len(self.buffer) < 6:
                break
            length = self.buffer[5]
            if self.buffer[2] != 2 or length > 240:
                del self.buffer[0]; continue
            total = 10 + length
            if len(self.buffer) < total:
                break
            raw = self.buffer[:total]
            if raw[-2:] != b'\r\n' or crc16(raw[2:-4]) != int.from_bytes(raw[-4:-2], 'little'):
                del self.buffer[0]; continue
            frames.append(Frame(raw[3], raw[4], bytes(raw[6:-4])))
            del self.buffer[:total]
        return frames
