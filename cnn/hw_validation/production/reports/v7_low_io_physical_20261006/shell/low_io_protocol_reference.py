"""Reference encoder and guard model for the RoadYOLO 16-bit physical shell."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


TABLE_BEGIN = 0x1000
PACKET_PREFIX = 0x2000
RUN_PREFIX = 0x3000
EXPORT = 0x4000
STATUS = 0x5000
DIAGNOSTIC_READ_PREFIX = 0x6000
MAX_PACKETS = 96
MAX_POSITIONS = 4
MAX_GROUPS = 24
MAX_TERMS = 192


def words_le(value: int, width: int) -> list[int]:
    """Return one fixed-width integer as least-significant 16-bit words."""
    if width % 16:
        raise ValueError("width must be a multiple of 16")
    if value < 0 or value >= 1 << width:
        raise ValueError(f"value does not fit {width} bits")
    return [(value >> shift) & 0xFFFF for shift in range(0, width, 16)]


@dataclass(frozen=True)
class Packet:
    first: bool
    last: bool
    mask: int
    activation: int
    weight: int
    bias: int

    def encode(self) -> list[int]:
        """Encode one complete 362-bit compute packet as one header and 22 words."""
        if not 0 <= self.mask <= 0xFF:
            raise ValueError("mask does not fit eight bits")
        header = PACKET_PREFIX | (int(self.first) << 11) | (int(self.last) << 10) | (self.mask << 2)
        return [header, *words_le(self.activation, 64), *words_le(self.weight, 192), *words_le(self.bias, 96)]


def validate_packets(packets: Iterable[Packet]) -> tuple[int, int]:
    """Validate finite legal reductions and return packet and position counts."""
    packet_list = list(packets)
    if not 1 <= len(packet_list) <= MAX_PACKETS:
        raise ValueError("packet count must be in 1..96")
    position_count = 0
    group_count = 0
    term_count = 0
    position_open = False
    for packet in packet_list:
        if packet.first == position_open:
            raise ValueError("first marker does not match position boundary")
        position_open = True
        group_count += 1
        term_count += packet.mask.bit_count()
        if group_count > MAX_GROUPS or term_count > MAX_TERMS:
            raise ValueError("position exceeds 24 groups or 192 valid terms")
        if packet.last:
            position_open = False
            position_count += 1
            if position_count > MAX_POSITIONS:
                raise ValueError("more than four positions")
            group_count = 0
            term_count = 0
    if position_open:
        raise ValueError("last position is incomplete")
    return len(packet_list), position_count


def encode_run(packets: Iterable[Packet]) -> list[int]:
    """Encode validated packets followed by an exact-count run command."""
    packet_list = list(packets)
    packet_count, _ = validate_packets(packet_list)
    return [word for packet in packet_list for word in packet.encode()] + [RUN_PREFIX | packet_count]


def self_test() -> None:
    """Exercise framing, byte order, and all finite reduction guards."""
    packet = Packet(True, True, 0xA5, 0x1122334455667788, (1 << 191) | 0xBEEF, 0x123456789ABCDEF012345678)
    encoded = packet.encode()
    assert len(encoded) == 23
    assert encoded[:5] == [0x2E94, 0x7788, 0x5566, 0x3344, 0x1122]
    assert encoded[-6:] == [0x5678, 0x1234, 0xDEF0, 0x9ABC, 0x5678, 0x1234]
    assert validate_packets([packet]) == (1, 1)
    maximum = [Packet(index == 0, index == 23, 0xFF, 0, 0, 0) for index in range(24)]
    assert validate_packets(maximum) == (24, 1)
    try:
        validate_packets([Packet(index == 0, index == 24, 0xFF, 0, 0, 0) for index in range(25)])
    except ValueError:
        pass
    else:
        raise AssertionError("25-group reduction was accepted")
    maximum_buffer = [Packet(group == 0, group == 23, 0xFF, 0, 0, 0) for _position in range(4) for group in range(24)]
    assert validate_packets(maximum_buffer) == (96, 4)
    try:
        validate_packets(maximum_buffer + [Packet(True, True, 0x01, 0, 0, 0)])
    except ValueError:
        pass
    else:
        raise AssertionError("fifth position was accepted")
    try:
        validate_packets([Packet(True, False, 0x01, 0, 0, 0)])
    except ValueError:
        pass
    else:
        raise AssertionError("incomplete position was accepted")
    assert encode_run([packet])[-1] == 0x3001
    print("REFERENCE_PASS packets=24 positions=1 max_terms=192")


if __name__ == "__main__":
    self_test()
