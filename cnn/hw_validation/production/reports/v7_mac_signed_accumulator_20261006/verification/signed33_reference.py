"""Signed-33 MAC reference and deterministic vectors for the approved v7 check."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PROOF = ROOT.parent / "coordinator" / "range_proof.json"
INT32_MIN = -(1 << 31)
INT32_MAX = (1 << 31) - 1
SIGNED33_MIN = -(1 << 32)
SIGNED33_MAX = (1 << 32) - 1


def require_signed(value: int, bits: int) -> int:
    lower = -(1 << (bits - 1))
    upper = (1 << (bits - 1)) - 1
    if not lower <= value <= upper:
        raise OverflowError(f"signed{bits} overflow: {value}")
    return value


def pack_signed(values: list[int] | tuple[int, ...], bits: int) -> int:
    word = 0
    mask = (1 << bits) - 1
    for index, value in enumerate(values):
        require_signed(value, bits)
        word |= (value & mask) << (index * bits)
    return word


def signed_hex(values: list[int] | tuple[int, ...], bits: int) -> str:
    digits = (len(values) * bits + 3) // 4
    return f"{pack_signed(values, bits):0{digits}x}"


@dataclass(frozen=True)
class Beat:
    activations: tuple[int, ...]
    weights: tuple[tuple[int, ...], ...]
    mask: int = 0xFF
    bias: tuple[int, int, int] = (0, 0, 0)

    def __post_init__(self) -> None:
        assert len(self.activations) == 8
        assert len(self.weights) == 3 and all(len(row) == 8 for row in self.weights)
        assert 0 <= self.mask <= 0xFF
        for value in self.activations + tuple(v for row in self.weights for v in row):
            require_signed(value, 8)
        for value in self.bias:
            require_signed(value, 32)


@dataclass(frozen=True)
class Case:
    name: str
    beats: tuple[Beat, ...]
    stall_cycles: int = 3
    expected_fault_lane: int | None = None


def banks(beat: Beat) -> dict[str, list[list[int]] | list[int]]:
    products = []
    pairs = []
    quads = []
    dots = []
    for output in range(3):
        row = []
        for lane in range(8):
            value = beat.activations[lane] * beat.weights[output][lane]
            row.append(require_signed(value if (beat.mask >> lane) & 1 else 0, 16))
        pair = [require_signed(row[index] + row[index + 1], 17) for index in range(0, 8, 2)]
        quad = [require_signed(pair[index] + pair[index + 1], 18) for index in range(0, 4, 2)]
        dot = require_signed(quad[0] + quad[1], 19)
        products.append(row)
        pairs.append(pair)
        quads.append(quad)
        dots.append(dot)
    return {"products": products, "pairs": pairs, "quads": quads, "dots": dots}


def uniform(value: int) -> tuple[int, ...]:
    return (value,) * 8


def recovery_case(name: str, bias_alpha: int, first_weight: int, second_weight: int) -> Case:
    if bias_alpha > 0:
        bias = (bias_alpha, INT32_MAX - 3, INT32_MAX - 2)
    else:
        bias = (bias_alpha, INT32_MIN + 3, INT32_MIN + 2)
    first = Beat(uniform(1), (uniform(first_weight), uniform(first_weight), uniform(first_weight)), bias=bias)
    second = Beat(uniform(1), (uniform(second_weight), uniform(second_weight), uniform(second_weight)),
                  bias=(123, -456, 789))
    return Case(name, (first, second))


def fault_case(name: str, lane: int, positive: bool, stall_cycles: int) -> Case:
    biases = [101, -202, 303]
    weights = [list(uniform(1)), list(uniform(-2)), list(uniform(3))]
    biases[lane] = INT32_MAX - 4 if positive else INT32_MIN + 4
    weights[lane] = list(uniform(1 if positive else -1))
    beat = Beat(uniform(1), tuple(tuple(row) for row in weights), bias=tuple(biases))
    return Case(name, (beat,), stall_cycles=stall_cycles, expected_fault_lane=lane)


def build_cases() -> tuple[Case, ...]:
    cases = [
        recovery_case("positive_excursion_recovers", INT32_MAX - 4, 1, -1),
        recovery_case("negative_excursion_recovers", INT32_MIN + 4, -1, 1),
    ]
    for lane, lane_name in enumerate(("alpha", "beta", "gamma")):
        cases.append(fault_case(f"{lane_name}_positive_final_overflow", lane, True, 3))
        cases.append(fault_case(f"{lane_name}_negative_final_overflow", lane, False, 12 if lane == 1 else 3))

    maximum_beats = []
    for index in range(24):
        bias = (INT32_MIN, INT32_MAX, -7) if index == 0 else (123456, -234567, 345678)
        maximum_beats.append(Beat(uniform(-128), (uniform(-128), uniform(127), uniform(0)), bias=bias))
    cases.append(Case("maximum_192_terms_bias_extremes", tuple(maximum_beats), stall_cycles=12))

    positive_endpoint = []
    negative_endpoint = []
    for index in range(24):
        positive_bias = (INT32_MAX, 11, -13) if index == 0 else (-101, 202, -303)
        negative_bias = (7, INT32_MIN, 9) if index == 0 else (404, -505, 606)
        positive_endpoint.append(
            Beat(uniform(-128), (uniform(-128), uniform(0), uniform(0)), bias=positive_bias)
        )
        negative_endpoint.append(
            Beat(uniform(-128), (uniform(0), uniform(127), uniform(0)), bias=negative_bias)
        )
    cases.append(Case("maximum_positive_prefix_final_fault", tuple(positive_endpoint),
                      expected_fault_lane=0))
    cases.append(Case("maximum_negative_prefix_final_fault", tuple(negative_endpoint),
                      expected_fault_lane=1))

    first = Beat(uniform(2), (uniform(1), uniform(-2), uniform(3)), bias=(100, -200, 300))
    tail_activations = (3, 127, -4, -128, 126, 5, -127, 64)
    tail_weights = (
        (2, -128, -3, 127, -127, 4, 126, -128),
        (-1, 127, 2, -128, 126, -3, -127, 64),
        (5, -128, -4, 127, -126, 2, 126, -64),
    )
    tail = Beat(tail_activations, tail_weights, mask=0x25,
                bias=(INT32_MAX, INT32_MIN, INT32_MAX))
    cases.append(Case("tail_mask_and_bias_once", (first, tail)))
    return tuple(cases)


def build_vectors(cases: tuple[Case, ...]) -> dict[str, object]:
    vectors = []
    committed = [0, 0, 0]
    case_summaries = []
    for case_id, case in enumerate(cases, start=1):
        sequence = None
        for beat_id, beat in enumerate(case.beats):
            first = beat_id == 0
            last = beat_id == len(case.beats) - 1
            bank = banks(beat)
            accumulator_before = list(committed)
            base = list(beat.bias if first else committed)
            if first:
                sequence = list(beat.bias)
            assert sequence is not None
            assert base == sequence
            candidate = [require_signed(base[index] + bank["dots"][index], 33) for index in range(3)]
            sequence = list(candidate)
            final_overflow = last and any(not INT32_MIN <= value <= INT32_MAX for value in candidate)
            if not final_overflow:
                committed = list(candidate)
            expected_data = list(candidate) if last and not final_overflow else [0, 0, 0]
            vector = {
                "case_id": case_id,
                "case_name": case.name,
                "beat_id": beat_id,
                "first": first,
                "last": last,
                "mask": beat.mask,
                "activations": list(beat.activations),
                "weights": [list(row) for row in beat.weights],
                "bias": list(beat.bias),
                "products": bank["products"],
                "pairs": bank["pairs"],
                "quads": bank["quads"],
                "dots": bank["dots"],
                "base_signed33": base,
                "candidate_signed34": candidate,
                "accumulator_before": accumulator_before,
                "accumulator_after": list(committed),
                "emit": last,
                "fault": final_overflow,
                "expected_data": expected_data,
                "stall_cycles": case.stall_cycles if last else 0,
            }
            vectors.append(vector)
        assert sequence is not None
        expected_fault = any(not INT32_MIN <= value <= INT32_MAX for value in sequence)
        assert expected_fault == (case.expected_fault_lane is not None)
        if "recovers" in case.name:
            first_partial = vectors[-2]["candidate_signed34"]
            assert all(value > INT32_MAX for value in first_partial) or all(
                value < INT32_MIN for value in first_partial
            )
            assert not vectors[-2]["fault"] and not vectors[-2]["emit"]
            assert not expected_fault and all(INT32_MIN <= value <= INT32_MAX for value in sequence)
        case_summaries.append({
            "case_id": case_id,
            "name": case.name,
            "beats": len(case.beats),
            "terms": sum(beat.mask.bit_count() for beat in case.beats),
            "final": list(sequence),
            "fault": expected_fault,
            "fault_lane": case.expected_fault_lane,
            "stall_cycles": case.stall_cycles,
        })
    return {"cases": case_summaries, "vectors": vectors}


def flatten(rows: list[list[int]]) -> list[int]:
    return [value for row in rows for value in row]


def write_text_vectors(vectors: list[dict[str, object]]) -> None:
    with (ROOT / "signed33_vectors.txt").open("w", encoding="ascii", newline="\n") as stream:
        for vector in vectors:
            fields = [
                str(vector["case_id"]), str(vector["beat_id"]),
                "1" if vector["first"] else "0", "1" if vector["last"] else "0",
                f"{vector['mask']:02x}", signed_hex(vector["activations"], 8),
                signed_hex(flatten(vector["weights"]), 8), signed_hex(vector["bias"], 32),
                "1" if vector["emit"] else "0", "1" if vector["fault"] else "0",
                signed_hex(vector["expected_data"], 32),
                signed_hex(flatten(vector["products"]), 16),
                signed_hex(flatten(vector["pairs"]), 17),
                signed_hex(flatten(vector["quads"]), 18),
                signed_hex(vector["dots"], 19),
                signed_hex(vector["base_signed33"], 33),
                signed_hex(vector["candidate_signed34"], 34),
                signed_hex(vector["accumulator_after"], 33),
                str(vector["stall_cycles"]),
            ]
            stream.write(" ".join(fields) + "\n")


def self_check(result: dict[str, object], proof: dict[str, object]) -> None:
    assert proof["status"] == "PROVED_FOR_FROZEN_GRAPH_LEGAL_REDUCTIONS"
    assert proof["max_terms"] == 192 and proof["max_beats"] == 24
    assert proof["product_range"] == [-16256, 16384]
    assert proof["whole_range"] == [-2150604800, 2150629375]
    assert proof["signed33_range"] == [SIGNED33_MIN, SIGNED33_MAX]
    assert len(proof["layers"]) == 67
    vectors = result["vectors"]
    assert len(vectors) == 84
    assert sum(1 for vector in vectors if vector["emit"]) == 12
    assert sum(1 for vector in vectors if vector["fault"]) == 8
    maximum = next(case for case in result["cases"] if case["name"] == "maximum_192_terms_bias_extremes")
    assert maximum["beats"] == 24 and maximum["terms"] == 192
    assert maximum["final"] == [-2144337920, 2144362495, -7]
    positive = next(case for case in result["cases"] if case["name"] == "maximum_positive_prefix_final_fault")
    negative = next(case for case in result["cases"] if case["name"] == "maximum_negative_prefix_final_fault")
    assert positive["beats"] == 24 and positive["terms"] == 192
    assert positive["final"][0] == INT32_MAX + 192 * 16384
    assert negative["beats"] == 24 and negative["terms"] == 192
    assert negative["final"][1] == INT32_MIN + 192 * -16256
    tail = next(case for case in result["cases"] if case["name"] == "tail_mask_and_bias_once")
    assert tail["final"] == [154, -258, 389]
    assert all(SIGNED33_MIN <= value <= SIGNED33_MAX
               for vector in vectors for value in vector["candidate_signed34"])


if __name__ == "__main__":
    proof = json.loads(PROOF.read_text(encoding="utf-8"))
    result = build_vectors(build_cases())
    self_check(result, proof)
    result["status"] = "REFERENCE_PASS"
    result["arithmetic_contract"] = {
        "partial_sum_bits": 33,
        "candidate_bits": 34,
        "final_result_bits": 32,
        "overflow_checked_only_on_last": True,
        "maximum_terms": proof["max_terms"],
        "maximum_beats": proof["max_beats"],
        "proof_sha256": hashlib.sha256(PROOF.read_bytes()).hexdigest(),
    }
    (ROOT / "signed33_vectors.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    write_text_vectors(result["vectors"])
    summary = {
        "status": result["status"],
        "cases": len(result["cases"]),
        "vectors": len(result["vectors"]),
        "faults": sum(1 for vector in result["vectors"] if vector["fault"]),
        "maximum_terms": proof["max_terms"],
        "maximum_beats": proof["max_beats"],
    }
    summary_line = json.dumps(summary, sort_keys=True)
    (ROOT / "reference_run.log").write_text(summary_line + "\n", encoding="utf-8")
    print(summary_line)
