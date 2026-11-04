
from dataclasses import dataclass
import binascii
import struct
import time

@dataclass(frozen=True)
class Packet:
    seq: int
    command: int
    data: bytes


def encode(command, seq, data=b""):
    if len(data) > 240:
        raise ValueError("V2 payload exceeds 240 bytes")
    body = bytes((2, seq & 255, command, len(data))) + data
    return b"\xaa\x55" + body + struct.pack("<H", binascii.crc_hqx(body, 0xFFFF)) + b"\r\n"


class Decoder:
    def __init__(self):
        self.buffer = bytearray()
        self.last = 0.0

    def feed(self, data):
        now = time.monotonic()
        if now - self.last > 0.1:
            self.buffer.clear()
        self.last = now
        self.buffer.extend(data)
        packets = []
        while True:
            at = self.buffer.find(b"\xaa\x55")
            if at < 0:
                self.buffer[:] = self.buffer[-1:] if self.buffer[-1:] == b"\xaa" else b""
                break
            del self.buffer[:at]
            if len(self.buffer) < 6:
                break
            length = self.buffer[5]
            if self.buffer[2] != 2 or length > 240:
                del self.buffer[0]
                continue
            total = length + 10
            if len(self.buffer) < total:
                break
            frame = bytes(self.buffer[:total])
            if (frame[-2:] != b"\r\n" or
                    binascii.crc_hqx(frame[2:-4], 0xFFFF) != int.from_bytes(frame[-4:-2], "little")):
                del self.buffer[0]
                continue
            packets.append(Packet(frame[3], frame[4], frame[6:-4]))
            del self.buffer[:total]
        return packets


VIDEO_HEADER = struct.Struct("<4sBBHIHHHHHH")


class FrameAssembler:

    def __init__(self, width=1280, height=720, chunk_bytes=1280):
        self.width, self.height, self.chunk_bytes = width, height, chunk_bytes
        self.total = width * height * 2
        self.count = self.total // chunk_bytes
        self.frames = {}
        self.completed = self.dropped = self.invalid = self.duplicates = self.bytes = 0
        self.last_complete = None
        self.last_complete_at = 0.0

    def _expire(self, now):
        for frame_id, item in list(self.frames.items()):
            if now - item[2] > 0.35:
                del self.frames[frame_id]
                self.dropped += 1

    def feed(self, data, now=None):
        now = time.monotonic() if now is None else now
        self._expire(now)
                                                                                    
        if self.last_complete is not None and now - self.last_complete_at > 2.0:
            self.last_complete = None
        if len(data) < VIDEO_HEADER.size:
            self.invalid += 1
            return None
        magic, version, fmt, header, frame_id, w, h, index, count, length, reserved = VIDEO_HEADER.unpack_from(data)
        if (magic != b"HXIM" or version not in (1, 2) or fmt != 1 or header != 24 or
                (version == 1 and reserved != 0) or
                (w, h) != (self.width, self.height) or count != self.count or
                index >= count or length != self.chunk_bytes or len(data) != 24 + length):
            self.invalid += 1
            return None
        if version == 2 and not reserved & 2:
                                                                                    
            return None
        if self.last_complete is not None:
            delta = (frame_id - self.last_complete) & 0xFFFFFFFF
            if delta == 0 or delta > 0x80000000:
                return None
        self.bytes += len(data)
        if frame_id not in self.frames:
            if len(self.frames) >= 3:
                oldest = min(self.frames, key=lambda key: self.frames[key][2])
                del self.frames[oldest]
                self.dropped += 1
            self.frames[frame_id] = (bytearray(self.total), set(), now, (version, reserved))
        buffer, seen, _, tag = self.frames[frame_id]
        if tag != (version, reserved):
            del self.frames[frame_id]
            self.invalid += 1
            return None
        if index in seen:
            self.duplicates += 1
            return None
        buffer[index * length:(index + 1) * length] = data[24:]
        seen.add(index)
        if len(seen) == count:
            del self.frames[frame_id]
            self.completed += 1
            self.last_complete = frame_id
            self.last_complete_at = now
                                                                
            for key in list(self.frames):
                if ((key - frame_id) & 0xFFFFFFFF) > 0x80000000:
                    del self.frames[key]
                    self.dropped += 1
            return frame_id, bytes(buffer), (None if version == 1 else (reserved & 1, reserved >> 2))
        return None

