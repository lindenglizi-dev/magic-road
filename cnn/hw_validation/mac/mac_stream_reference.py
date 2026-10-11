"""Reference packing for the 32-bit dynamic MAC resource-probe wrapper."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Tuple

from mac_reference import Beat


OP_ACTIVATION = 0
OP_WEIGHT = 1
OP_BIAS = 2
OP_CONTROL = 3


@dataclass(frozen=True)
class Command:
    """One accepted wrapper command word."""

    opcode: int
    index: int
    data: int


def _pack_signed(values: Iterable[int], bits: int) -> int:
    packed = 0
    mask = (1 << bits) - 1
    for index, value in enumerate(values):
        packed |= (value & mask) << (index * bits)
    return packed


def commands_for_beat(beat: Beat) -> Tuple[Command, ...]:
    """Return the fixed twelve-command transaction for one MAC beat."""
    activation = _pack_signed(beat.activations, 8)
    weights = _pack_signed((value for row in beat.weights for value in row), 8)
    biases = _pack_signed(beat.biases, 32)
    control = beat.mask | (int(beat.first) << 8) | (int(beat.last) << 9)
    commands = [Command(OP_ACTIVATION, index, (activation >> (32 * index)) & 0xFFFFFFFF) for index in range(2)]
    commands.extend(Command(OP_WEIGHT, index, (weights >> (32 * index)) & 0xFFFFFFFF) for index in range(6))
    commands.extend(Command(OP_BIAS, index, (biases >> (32 * index)) & 0xFFFFFFFF) for index in range(3))
    commands.append(Command(OP_CONTROL, 0, control))
    return tuple(commands)


def dynamic_resource_probe_beat() -> Beat:
    """Provide non-constant runtime values across every activation and weight byte."""
    return Beat(
        first=True,
        last=True,
        mask=0xFF,
        activations=(-128, -91, -37, -1, 1, 29, 83, 127),
        weights=(
            (-127, -103, -79, -53, -31, -7, 19, 43),
            (-119, -89, -61, -29, 3, 37, 71, 101),
            (-113, -73, -41, -11, 23, 59, 97, 125),
        ),
        biases=(-1234567, 7654321, -314159),
    )

