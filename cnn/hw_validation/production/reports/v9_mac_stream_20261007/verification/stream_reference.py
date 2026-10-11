"""Independent signed-33 streaming MAC golden model and frozen vectors."""

from __future__ import annotations

import hashlib
import json
import random
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent
INT32_MIN = -(1 << 31)
INT32_MAX = (1 << 31) - 1
SIGNED33_MIN = -(1 << 32)
SIGNED33_MAX = (1 << 32) - 1


def signed(value: int, bits: int) -> int:
    lower = -(1 << (bits - 1))
    upper = (1 << (bits - 1)) - 1
    if not lower <= value <= upper:
        raise OverflowError(f"signed{bits} overflow: {value}")
    return value


def pack(values: tuple[int, ...] | list[int], bits: int) -> int:
    word = 0
    mask = (1 << bits) - 1
    for index, value in enumerate(values):
        signed(value, bits)
        word |= (value & mask) << (index * bits)
    return word


def hex_pack(values: tuple[int, ...] | list[int], bits: int) -> str:
    return f"{pack(values, bits):0{(len(values) * bits + 3) // 4}x}"


@dataclass(frozen=True)
class Beat:
    activations: tuple[int, ...]
    weights: tuple[tuple[int, ...], ...]
    bias: tuple[int, int, int] = (0, 0, 0)
    mask: int = 0xFF
    first: bool | None = None
    gap: int = 0

    def __post_init__(self) -> None:
        assert len(self.activations) == 8
        assert len(self.weights) == 3 and all(len(row) == 8 for row in self.weights)
        assert 0 <= self.mask <= 0xFF and self.gap >= 0
        for value in self.activations + tuple(v for row in self.weights for v in row):
            signed(value, 8)
        for value in self.bias:
            signed(value, 32)


@dataclass(frozen=True)
class Case:
    name: str
    beats: tuple[Beat, ...]
    stall: int = 0
    blocked_input_probe: bool = False


def uniform(value: int) -> tuple[int, ...]:
    return (value,) * 8


def beat(activation: int, weights: tuple[int, int, int], **kwargs: object) -> Beat:
    return Beat(uniform(activation), tuple(uniform(value) for value in weights), **kwargs)


def dots(item: Beat) -> tuple[int, int, int]:
    result = []
    for output in range(3):
        products = [
            signed(item.activations[lane] * item.weights[output][lane], 16)
            if (item.mask >> lane) & 1 else 0
            for lane in range(8)
        ]
        pairs = [signed(products[index] + products[index + 1], 17) for index in range(0, 8, 2)]
        quads = [signed(pairs[index] + pairs[index + 1], 18) for index in range(0, 4, 2)]
        result.append(signed(quads[0] + quads[1], 19))
    return tuple(result)


def recovery(name: str, bias_value: int, first_weight: int, second_weight: int) -> Case:
    first = beat(1, (first_weight,) * 3, bias=(bias_value,) * 3)
    second = beat(1, (second_weight,) * 3, bias=(123, -456, 789))
    return Case(name, (first, second))


def lane_fault(name: str, lane: int, positive: bool) -> Case:
    biases = [101, -202, 303]
    weights = [1, -2, 3]
    biases[lane] = INT32_MAX - 4 if positive else INT32_MIN + 4
    weights[lane] = 1 if positive else -1
    return Case(name, (beat(1, tuple(weights), bias=tuple(biases)),), stall=5)


def random_case() -> Case:
    rng = random.Random(0x4D4143494931)
    items = []
    for index in range(12):
        activations = tuple(rng.randint(-128, 127) for _ in range(8))
        weights = tuple(tuple(rng.randint(-128, 127) for _ in range(8)) for _ in range(3))
        items.append(Beat(activations, weights, bias=(37, -41, 43),
                          mask=rng.randint(0, 255), gap=(0, 2, 1, 3)[index % 4]))
    return Case("random_input_bubbles", tuple(items), stall=7)


def cases() -> tuple[Case, ...]:
    result = [
        recovery("positive_temporary_excursion_recovers", INT32_MAX - 4, 1, -1),
        recovery("negative_temporary_excursion_recovers", INT32_MIN + 4, -1, 1),
    ]
    for lane, lane_name in enumerate(("alpha", "beta", "gamma")):
        result.append(lane_fault(f"{lane_name}_positive_final_overflow", lane, True))
        result.append(lane_fault(f"{lane_name}_negative_final_overflow", lane, False))
    result.append(Case("all_lane_atomic_fault", (
        beat(1, (1, 1, 1), bias=(INT32_MAX, INT32_MAX, INT32_MAX)),
    ), stall=30, blocked_input_probe=True))

    maximum_legal = tuple(
        beat(-128, (-128, 127, 0), bias=(INT32_MIN, INT32_MAX, -7) if index == 0 else (1, 2, 3))
        for index in range(24)
    )
    maximum_positive = tuple(
        beat(-128, (-128, 0, 0), bias=(INT32_MAX, 11, -13) if index == 0 else (0, 0, 0))
        for index in range(24)
    )
    maximum_negative = tuple(
        beat(-128, (0, 127, 0), bias=(7, INT32_MIN, 9) if index == 0 else (0, 0, 0))
        for index in range(24)
    )
    result.extend((
        Case("maximum_24_groups_192_products_per_output", maximum_legal, stall=2),
        Case("maximum_positive_terminal_overflow", maximum_positive),
        Case("maximum_negative_terminal_overflow", maximum_negative),
    ))

    tail = Beat(
        (3, 127, -4, -128, 126, 5, -127, 64),
        (
            (2, -128, -3, 127, -127, 4, 126, -128),
            (-1, 127, 2, -128, 126, -3, -127, 64),
            (5, -128, -4, 127, -126, 2, 126, -64),
        ),
        bias=(INT32_MAX, INT32_MIN, INT32_MAX), mask=0x25,
    )
    result.append(Case("extremes_tail_mask_bias_once", (
        beat(2, (1, -2, 3), bias=(100, -200, 300)), tail,
    )))
    result.append(Case("first_zero_continues_history", (
        beat(1, (1, 2, -1), first=False),
    )))
    result.append(Case("first_one_reopens_with_bias", (
        beat(-128, (-128, 127, -128), bias=(-1234, 5678, -9012), first=True),
    )))
    result.append(Case("continuous_no_bubble_ii1", tuple(
        beat((index % 17) - 8, (3, -5, 7), bias=(11, -13, 17)) for index in range(24)
    ), stall=3))
    result.append(random_case())
    return tuple(result)


def build() -> dict[str, object]:
    committed = [0, 0, 0]
    vectors = []
    summaries = []
    for case_id, case in enumerate(cases(), 1):
        case_start = len(vectors)
        for beat_id, item in enumerate(case.beats):
            first = item.first if item.first is not None else beat_id == 0
            last = beat_id == len(case.beats) - 1
            dot_values = list(dots(item))
            base = list(item.bias) if first else list(committed)
            candidate = [signed(base[lane] + dot_values[lane], 33) for lane in range(3)]
            fault = last and any(not INT32_MIN <= value <= INT32_MAX for value in candidate)
            if not fault:
                committed = list(candidate)
            expected_data = [0, 0, 0] if fault else list(candidate)
            vectors.append({
                "case_id": case_id, "case_name": case.name, "beat_id": beat_id,
                "first": first, "last": last, "gap": item.gap, "stall": case.stall if last else 0,
                "blocked_input_probe": case.blocked_input_probe and last,
                "mask": item.mask, "activations": list(item.activations),
                "weights": [list(row) for row in item.weights], "bias": list(item.bias),
                "dots": dot_values, "candidate_signed34": candidate,
                "accumulator_after": list(committed), "fault": fault,
                "expected_data": expected_data if last else [0, 0, 0],
            })
        summaries.append({
            "case_id": case_id, "name": case.name, "first_vector": case_start,
            "vectors": len(case.beats), "active_products_per_output": sum(item.mask.bit_count() for item in case.beats),
            "stall": case.stall, "fault": vectors[-1]["fault"], "final": vectors[-1]["candidate_signed34"],
        })
    return {"status": "REFERENCE_PASS", "cases": summaries, "vectors": vectors}


def write_vectors(result: dict[str, object]) -> None:
    with (ROOT / "stream_vectors.txt").open("w", encoding="ascii", newline="\n") as stream:
        for vector in result["vectors"]:
            weights = [value for row in vector["weights"] for value in row]
            fields = [
                vector["case_id"], vector["beat_id"], int(vector["first"]), int(vector["last"]),
                vector["gap"], vector["stall"], int(vector["blocked_input_probe"]),
                f"{vector['mask']:02x}", hex_pack(vector["activations"], 8), hex_pack(weights, 8),
                hex_pack(vector["bias"], 32), hex_pack(vector["dots"], 19),
                hex_pack(vector["candidate_signed34"], 34), hex_pack(vector["accumulator_after"], 33),
                int(vector["fault"]), hex_pack(vector["expected_data"], 32),
            ]
            stream.write(" ".join(map(str, fields)) + "\n")


def self_check(result: dict[str, object]) -> None:
    vectors = result["vectors"]
    by_name = {case["name"]: case for case in result["cases"]}
    assert len(result["cases"]) == 17 and len(vectors) == 123
    assert by_name["maximum_24_groups_192_products_per_output"]["vectors"] == 24
    assert by_name["maximum_24_groups_192_products_per_output"]["active_products_per_output"] == 192
    assert not by_name["maximum_24_groups_192_products_per_output"]["fault"]
    assert by_name["maximum_positive_terminal_overflow"]["fault"]
    assert by_name["maximum_negative_terminal_overflow"]["fault"]
    for name in ("positive_temporary_excursion_recovers", "negative_temporary_excursion_recovers"):
        case = by_name[name]
        first = vectors[case["first_vector"]]["candidate_signed34"]
        final = vectors[case["first_vector"] + 1]["candidate_signed34"]
        assert any(not INT32_MIN <= value <= INT32_MAX for value in first)
        assert all(INT32_MIN <= value <= INT32_MAX for value in final)
    assert all(SIGNED33_MIN <= value <= SIGNED33_MAX for vector in vectors for value in vector["candidate_signed34"])
    assert sum(vector["fault"] for vector in vectors) == 9


if __name__ == "__main__":
    result = build()
    self_check(result)
    write_vectors(result)
    encoded = json.dumps(result, indent=2) + "\n"
    (ROOT / "stream_vectors.json").write_text(encoded, encoding="utf-8")
    summary = {
        "status": result["status"], "cases": len(result["cases"]), "vectors": len(result["vectors"]),
        "fault_terminals": sum(vector["fault"] for vector in result["vectors"]),
        "vectors_sha256": hashlib.sha256((ROOT / "stream_vectors.txt").read_bytes()).hexdigest(),
    }
    print(json.dumps(summary, sort_keys=True))
