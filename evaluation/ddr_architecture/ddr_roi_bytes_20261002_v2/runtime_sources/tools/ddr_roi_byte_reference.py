#!/usr/bin/env python3
"""Integer byte-address reference for a 32x32 ROI read from tight RGB888."""
from __future__ import annotations

import json


FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
ROI_SIZE = 32
BEAT_BYTES = 16


def rgb_at(x: int, y: int) -> tuple[int, int, int]:
    return ((3*x + 5*y + 17) & 255,
            (7*x + 11*y + 29) & 255,
            (13*x + 19*y + 43) & 255)


def byte_at(address: int, frame_base: int = 0) -> int:
    offset = address - frame_base
    if not 0 <= offset < FRAME_WIDTH * FRAME_HEIGHT * 3:
        raise ValueError('address outside frame')
    pixel, channel = divmod(offset, 3)
    y, x = divmod(pixel, FRAME_WIDTH)
    return rgb_at(x, y)[channel]


def beat_at(byte_address: int, frame_base: int = 0) -> int:
    if byte_address % BEAT_BYTES:
        raise ValueError('beat address must be 16-byte aligned')
    data = bytes(byte_at(byte_address + lane, frame_base) for lane in range(BEAT_BYTES))
    return int.from_bytes(data, 'big')


def sample_coordinate(lo: int, hi: int, roi_index: int) -> int:
    if not 0 <= lo < hi:
        raise ValueError('ROI interval must be non-empty and half-open')
    return lo + ((hi - lo) * (2*roi_index + 1) >> 6)


def pixel_request(frame_base: int, x: int, y: int) -> dict:
    byte_address = frame_base + (y*FRAME_WIDTH + x)*3
    first = byte_address & -BEAT_BYTES
    last = (byte_address + 2) & -BEAT_BYTES
    beats = [first] if first == last else [first, last]
    rgb = tuple(byte_at(byte_address + channel, frame_base) for channel in range(3))
    return {'pixel_byte_address': byte_address, 'beat_addresses': beats,
            'rgb': list(rgb), 'gray': (rgb[0] >> 2) + (rgb[1] >> 1) + (rgb[2] >> 2)}


def roi_reference(frame_base: int, box: tuple[int, int, int, int]) -> list[dict]:
    x0, y0, x1, y1 = box
    if not (0 <= x0 < x1 <= FRAME_WIDTH and 0 <= y0 < y1 <= FRAME_HEIGHT):
        raise ValueError('box must be inside the frame and use half-open endpoints')
    result = []
    for v in range(ROI_SIZE):
        y = sample_coordinate(y0, y1, v)
        for u in range(ROI_SIZE):
            x = sample_coordinate(x0, x1, u)
            result.append({'u': u, 'v': v, 'source_x': x, 'source_y': y,
                           **pixel_request(frame_base, x, y)})
    return result


def self_check() -> dict:
    base = 0x1000
    full = roi_reference(base, (0, 0, 1280, 720))
    assert len(full) == 1024
    assert (full[0]['source_x'], full[0]['source_y']) == (20, 11)
    assert (full[-1]['source_x'], full[-1]['source_y']) == (1260, 708)
    repeated = roi_reference(base, (5, 0, 6, 1))
    assert len({(row['source_x'], row['source_y']) for row in repeated}) == 1
    assert all(len(row['beat_addresses']) == 2 for row in repeated)
    last = roi_reference(base, (1279, 719, 1280, 720))
    assert all((row['source_x'], row['source_y']) == (1279, 719) for row in last)
    cross = pixel_request(base, 10, 719)
    assert cross['pixel_byte_address'] % 16 == 14 and len(cross['beat_addresses']) == 2
    beat = beat_at(base, base)
    assert beat.to_bytes(16, 'big')[:3] == bytes(rgb_at(0, 0))
    return {'status': 'PASS', 'roi_pixels_checked': len(full) + len(repeated) + len(last),
            'crossbeat_offsets_checked': [14, 15],
            'lane_contract': 'lowest byte address is beat[127:120]'}


if __name__ == '__main__':
    print(json.dumps(self_check(), ensure_ascii=False, indent=2))
