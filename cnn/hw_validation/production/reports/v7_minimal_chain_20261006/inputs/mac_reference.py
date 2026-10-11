"""Integer reference and deterministic vectors for the 8-by-3 MAC probe."""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional, Sequence, TextIO, Tuple


INT32_MIN = -(1 << 31)
INT32_MAX = (1 << 31) - 1
INT64_MIN = -(1 << 63)
INT64_MAX = (1 << 63) - 1


@dataclass(frozen=True)
class Beat:
    """One accepted 8-input by 3-output MAC beat."""

    first: bool
    last: bool
    mask: int
    activations: Tuple[int, ...]
    weights: Tuple[Tuple[int, ...], ...]
    biases: Tuple[int, ...]


@dataclass(frozen=True)
class Outcome:
    """A terminal normal result or overflow fault."""

    fault: bool
    values: Tuple[int, int, int]


@dataclass(frozen=True)
class IntermediateBanks:
    """Exact signed values expected at the four registered reduction banks."""

    products: Tuple[int, ...]
    pairs: Tuple[int, ...]
    quads: Tuple[int, ...]
    dots: Tuple[int, ...]


def _check_signed(value: int, bits: int, name: str) -> int:
    minimum = -(1 << (bits - 1))
    maximum = (1 << (bits - 1)) - 1
    if not minimum <= value <= maximum:
        raise ValueError(f"{name}={value} is outside signed {bits}-bit range")
    return value


def _check_i64(value: int) -> int:
    if not INT64_MIN <= value <= INT64_MAX:
        raise OverflowError("reference intermediate exceeded signed 64-bit range")
    return value


def _validate_beat(beat: Beat) -> None:
    if not 0 <= beat.mask <= 0xFF:
        raise ValueError("mask must be an unsigned 8-bit value")
    if len(beat.activations) != 8:
        raise ValueError("exactly eight activations are required")
    if len(beat.weights) != 3 or any(len(row) != 8 for row in beat.weights):
        raise ValueError("weights must be three rows of eight values")
    if len(beat.biases) != 3:
        raise ValueError("exactly three biases are required")
    for value in beat.activations:
        _check_signed(value, 8, "activation")
    for row in beat.weights:
        for value in row:
            _check_signed(value, 8, "weight")
    for value in beat.biases:
        _check_signed(value, 32, "bias")


def intermediate_banks(beat: Beat) -> IntermediateBanks:
    """Return output-major product, pair, quad, and dot banks for one beat."""
    _validate_beat(beat)
    products = tuple(
        beat.activations[lane_index] * beat.weights[output_index][lane_index]
        if (beat.mask >> lane_index) & 1
        else 0
        for output_index in range(3)
        for lane_index in range(8)
    )
    pairs = tuple(
        products[output_index * 8 + pair_index * 2]
        + products[output_index * 8 + pair_index * 2 + 1]
        for output_index in range(3)
        for pair_index in range(4)
    )
    quads = tuple(
        pairs[output_index * 4 + quad_index * 2]
        + pairs[output_index * 4 + quad_index * 2 + 1]
        for output_index in range(3)
        for quad_index in range(2)
    )
    dots = tuple(
        quads[output_index * 2] + quads[output_index * 2 + 1]
        for output_index in range(3)
    )
    return IntermediateBanks(products, pairs, quads, dots)


class MacReference:
    """Stateful signed accumulator with explicit accepted/stalled cycles."""

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.accumulators = (0, 0, 0)

    def apply(self, beat: Beat, accepted: bool = True) -> Optional[Outcome]:
        _validate_beat(beat)
        if not accepted:
            return None

        base = beat.biases if beat.first else self.accumulators
        banks = intermediate_banks(beat)
        candidates = [
            _check_i64(base[output_index] + _check_i64(banks.dots[output_index]))
            for output_index in range(3)
        ]

        if any(value < INT32_MIN or value > INT32_MAX for value in candidates):
            return Outcome(fault=True, values=(0, 0, 0))

        self.accumulators = tuple(candidates)
        if beat.last:
            return Outcome(fault=False, values=self.accumulators)
        return None


def _pack_signed(values: Sequence[int], bits: int) -> int:
    packed = 0
    mask = (1 << bits) - 1
    for index, value in enumerate(values):
        _check_signed(value, bits, "packed value")
        packed |= (value & mask) << (index * bits)
    return packed


def _flatten_weights(weights: Sequence[Sequence[int]]) -> Tuple[int, ...]:
    return tuple(value for row in weights for value in row)


def _write_vector(stream: TextIO, beat: Beat, outcome: Optional[Outcome]) -> None:
    activation_hex = _pack_signed(beat.activations, 8)
    weight_hex = _pack_signed(_flatten_weights(beat.weights), 8)
    bias_hex = _pack_signed(beat.biases, 32)
    emit = int(outcome is not None)
    fault = int(outcome.fault) if outcome is not None else 0
    result_hex = _pack_signed(outcome.values, 32) if outcome is not None else 0
    banks = intermediate_banks(beat)
    product_hex = _pack_signed(banks.products, 16)
    pair_hex = _pack_signed(banks.pairs, 17)
    quad_hex = _pack_signed(banks.quads, 18)
    dot_hex = _pack_signed(banks.dots, 19)
    stream.write(
        f"{int(beat.first)} {int(beat.last)} {beat.mask:02x} "
        f"{activation_hex:016x} {weight_hex:048x} {bias_hex:024x} "
        f"{emit} {fault} {result_hex:024x} {product_hex:096x} "
        f"{pair_hex:051x} {quad_hex:027x} {dot_hex:015x}\n"
    )


def _random_beat(rng: random.Random) -> Beat:
    activations = tuple(rng.randint(-128, 127) for _ in range(8))
    weights = tuple(tuple(rng.randint(-128, 127) for _ in range(8)) for _ in range(3))
    biases = tuple(rng.randint(-1_000_000, 1_000_000) for _ in range(3))
    return Beat(True, True, rng.randint(0, 255), activations, weights, biases)


def directed_beats() -> Iterable[Beat]:
    zeros = (0,) * 8
    yield Beat(True, True, 0xFF, (-128,) * 8, ((-128,) * 8,) * 3, (0, 1, -1))
    yield Beat(True, True, 0x81, (127, -128, 3, -4, 5, -6, 7, -8), ((1,) * 8, (-1,) * 8, zeros), (3, -3, 17))
    yield Beat(True, False, 0xFF, (1,) * 8, ((1,) * 8, (2,) * 8, (-3,) * 8), (10, 20, 30))
    yield Beat(False, False, 0x0F, (4,) * 8, ((2,) * 8, (-2,) * 8, (1,) * 8), (999, 999, 999))
    yield Beat(False, True, 0xF0, (-5,) * 8, ((3,) * 8, (1,) * 8, (-2,) * 8), (-999, -999, -999))
    yield Beat(True, True, 0x01, (1,) + zeros[1:], ((1,) * 8,) * 3, (INT32_MAX, 0, 0))
    yield Beat(True, True, 0x01, (-128,) + zeros[1:], ((127,) * 8,) * 3, (INT32_MIN, 0, 0))


def write_vectors(path: Path, random_cases: int = 1024, seed: int = 42) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    reference = MacReference()
    count = 0
    with path.open("w", encoding="ascii", newline="\n") as stream:
        for beat in directed_beats():
            outcome = reference.apply(beat)
            _write_vector(stream, beat, outcome)
            count += 1
        rng = random.Random(seed)
        for _ in range(random_cases):
            beat = _random_beat(rng)
            outcome = reference.apply(beat)
            _write_vector(stream, beat, outcome)
            count += 1
    return count


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vectors", type=Path, required=True)
    parser.add_argument("--random-cases", type=int, default=1024)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    if args.random_cases < 1024:
        raise SystemExit("random case count must be at least 1024")
    count = write_vectors(args.vectors, args.random_cases, args.seed)
    print(f"PYTHON-GOLDEN PASS vectors={count} random={args.random_cases} seed={args.seed}")


if __name__ == "__main__":
    main()
