"""Transaction reference and deterministic vectors for road_nms_serial."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

import numpy as np

from cnn import integer
from cnn.hw_validation.production.postprocess_golden_2fps_20261015 import golden

OUT = Path(__file__).resolve().parent
VECTORS = OUT / "vectors"
BASELINE = OUT.parent / "postprocess_golden_2fps_20261015"
ARTIFACTS = BASELINE / "artifacts"

FROZEN_CASES = (
    "all_low_empty_complete_table",
    "threshold_equal_inclusive_and_below",
    "top128_ties_and_each32_total64",
    "full_heap_replaces_worst_two",
    "cell_order_cross_scale",
    "person_vehicle_same_box_not_suppressed",
    "same_class_duplicate_suppressed",
    "zero_area_after_clipping",
    "zero_area_not_removed_before_topk",
    "source_rounding_degenerate_kept_by_current_reference",
    "real_image",
)

PINNED_SOURCE_SHA256 = {
    "cnn/integer.py": "441b91d86895fb0c0337583325fb9cc39624026a6759d39da51aaab49a5ca040",
    "cnn/hw_validation/production/postprocess_golden_2fps_20261015/golden.py":
        "95a386e97b2b73507315032c57f7386c57a2c1d00c7a874eb5602f9ff9ec4453",
    "cnn/hw_validation/production/postprocess_golden_2fps_20261015/handoff.txt":
        "92450a4ee862d1d7643189b6aea4593c29ed4bdcafba0b5d09c08aaaa2bd48a3",
    "cnn/hw_validation/plans/resource_budget_20261015/后处理共享RAM与接口约定_20261015.txt":
        "07d25e3551d19479d0d0d578a906a71f327d80f76a0cc7e5dc1d6a5fa0ffe87d",
    "cnn/hw_validation/production/postprocess_golden_2fps_20261015/artifacts/receipt.json":
        "39ace33328572b046ab25156f786d8f1196d7638b447cef6607310bf766709e7",
}

DECISION_CODE = {"invalid": 0, "suppressed": 1, "keep": 2}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read_hex(path: Path) -> list[int]:
    return [int(line, 16) for line in path.read_text(encoding="ascii").splitlines()]


def write_hex(path: Path, words: list[int], bits: int) -> None:
    if any(word < 0 or word >= 1 << bits for word in words):
        raise ValueError(f"{path.name}: word outside {bits} bits")
    width = (bits + 3) // 4
    path.write_text("".join(f"{word:0{width}x}\n" for word in words), encoding="ascii")


def unpack_candidate(word: int) -> dict:
    if word < 0 or word >= 1 << 160 or word >> 104:
        raise ValueError("DECODED160 reserved bits or width invalid")
    return {
        "box_q8": [(word >> (18 * index)) & ((1 << 18) - 1) for index in range(4)],
        "cell_id": (word >> 72) & 0x3FFF,
        "score_uint16": (word >> 86) & 0xFFFF,
        "label": (word >> 102) & 1,
        "geometry_valid": bool((word >> 103) & 1),
    }


def pack_comparison(row: dict) -> int:
    for key in ("intersection", "area_a", "area_b"):
        if not 0 <= row[key] < 1 << 40:
            raise ValueError(f"{key} outside 40 bits")
    return (row["label"] << 135 | row["candidate_index"] << 128
            | row["kept_index"] << 121 | row["intersection"] << 81
            | row["area_a"] << 41 | row["area_b"] << 1 | int(row["suppress"]))


def pack_decision(row: dict) -> int:
    return row["label"] << 9 | row["candidate_index"] << 2 | row["code"]


def run_nms(candidates: list[list[dict]]) -> dict:
    outputs, comparisons, decisions = [], [], []
    for label in (0, 1):
        kept: list[tuple[int, dict]] = []
        for candidate_index, row in enumerate(candidates[label]):
            if len(kept) == 32:
                break
            if row["label"] != label or candidate_index >= 128:
                raise ValueError("candidate class/index mismatch")
            box = tuple(row["box_q8"])
            comparison_start = len(comparisons)
            if not row["geometry_valid"]:
                decision = "invalid"
            else:
                if not (box[0] < box[2] and box[1] < box[3]):
                    raise ValueError("geometry_valid record has reversed/zero coordinates")
                if not (0 <= box[0] <= box[2] <= 512 * 256
                        and 0 <= box[1] <= box[3] <= 288 * 256):
                    raise ValueError("geometry_valid record outside network frame")
                area_a = (box[2] - box[0]) * (box[3] - box[1])
                decision = "keep"
                for kept_index, previous in kept:
                    other = tuple(previous["box_q8"])
                    width = max(0, min(box[2], other[2]) - max(box[0], other[0]))
                    height = max(0, min(box[3], other[3]) - max(box[1], other[1]))
                    intersection = width * height
                    area_b = (other[2] - other[0]) * (other[3] - other[1])
                    suppress = integer._overlap_half(box, other)
                    assert suppress == (3 * intersection > area_a + area_b)
                    comparisons.append({
                        "label": label,
                        "candidate_index": candidate_index,
                        "kept_index": kept_index,
                        "intersection": intersection,
                        "area_a": area_a,
                        "area_b": area_b,
                        "suppress": bool(suppress),
                    })
                    if suppress:
                        decision = "suppressed"
                        break
                if decision == "keep":
                    kept.append((candidate_index, row))
                    source = integer.round_div_even(np.asarray(box, dtype=np.int64) * 5, 512).tolist()
                    detection = {
                        "label": label,
                        "score_uint16": row["score_uint16"],
                        "cell_id": row["cell_id"],
                        "box_q8": list(box),
                        "box_source": list(map(int, source)),
                    }
                    detection["packed97_hex"] = f"{golden.result97(detection):025x}"
                    outputs.append(detection)
            decisions.append({
                "label": label,
                "candidate_index": candidate_index,
                "decision": decision,
                "code": DECISION_CODE[decision],
                "comparison_start": comparison_start,
                "comparison_count": len(comparisons) - comparison_start,
            })
    return {"outputs": outputs, "comparisons": comparisons, "decisions": decisions}


def source_snapshot() -> dict[str, str]:
    snapshot = {}
    for relative, expected in PINNED_SOURCE_SHA256.items():
        path = ROOT / relative
        actual = sha256(path)
        if actual != expected:
            raise AssertionError(f"frozen source hash changed: {relative}")
        snapshot[relative] = actual
    receipt = read_json(ARTIFACTS / "receipt.json")
    for name in FROZEN_CASES:
        for filename in ("top128_decoded_160.hex", "nms_events.jsonl",
                         "result_table_97.hex", "final.json"):
            relative = f"{name}/{filename}"
            expected = receipt["artifact_sha256"][relative]
            path = ARTIFACTS / relative
            actual = sha256(path)
            if actual != expected:
                raise AssertionError(f"frozen artifact hash changed: {relative}")
            snapshot[(path.relative_to(ROOT)).as_posix()] = actual
    snapshot[(Path(__file__).relative_to(ROOT)).as_posix()] = sha256(Path(__file__))
    return snapshot


def frozen_case(name: str) -> tuple[list[list[dict]], list[dict]]:
    folder = ARTIFACTS / name
    words = read_hex(folder / "top128_decoded_160.hex")
    candidates = [[], []]
    for word in words:
        row = unpack_candidate(word)
        row["packed160_hex"] = f"{word:040x}"
        candidates[row["label"]].append(row)
    events = [json.loads(line) for line in
              (folder / "nms_events.jsonl").read_text(encoding="utf-8").splitlines()]
    assert [len(candidates[0]), len(candidates[1])] == [
        sum(event["label"] == label for event in events) for label in (0, 1)]
    return candidates, events


def assert_frozen_exact(name: str, candidates: list[list[dict]], result: dict,
                        events: list[dict]) -> None:
    original_words = read_hex(ARTIFACTS / name / "result_table_97.hex")
    actual_words = [int(row["packed97_hex"], 16) for row in result["outputs"]]
    assert actual_words == original_words, f"{name}: FINAL97 mismatch"
    semantic = [{key: value for key, value in row.items() if key != "packed97_hex"}
                for row in result["outputs"]]
    assert semantic == read_json(ARTIFACTS / name / "final.json")["detections"], \
        f"{name}: final detection mismatch"
    decisions = {(row["label"], row["candidate_index"]): row for row in result["decisions"]}
    for event in events:
        key = (event["label"], event["rank"])
        if key not in decisions:
            assert event["decision"] == "not_processed_class_cap" and not event["comparisons"]
            continue
        row = decisions[key]
        expected_decision = {"keep": "keep", "suppress": "suppressed",
                             "drop_zero_area": "invalid"}[event["decision"]]
        assert row["decision"] == expected_decision, f"{name}: decision mismatch {key}"
        observed = result["comparisons"][row["comparison_start"]:
                                         row["comparison_start"] + row["comparison_count"]]
        assert len(observed) == len(event["comparisons"])
        for actual, expected in zip(observed, event["comparisons"], strict=True):
            kept = candidates[event["label"]][actual["kept_index"]]
            assert kept["cell_id"] == expected["kept_cell_id"]
            assert all(actual[key] == expected[key]
                       for key in ("intersection", "area_a", "area_b", "suppress"))


def candidate(label: int, index: int, box: tuple[int, int, int, int],
              geometry_valid: bool = True, score: int = 65534) -> dict:
    row = {"label": label, "cell_id": label * 128 + index,
           "score_uint16": score, "box_q8": list(box),
           "geometry_valid": geometry_valid}
    row["packed160_hex"] = f"{golden.decoded160(row):040x}"
    return row


def analytic_cases() -> list[tuple[str, list[list[dict]]]]:
    equal = [[candidate(0, 0, (0, 0, 6, 2)),
              candidate(0, 1, (2, 0, 8, 2))], []]
    above = [[candidate(0, 0, (0, 0, 6, 2)),
              candidate(0, 1, (1, 0, 7, 2))], []]
    rne = [[candidate(0, 0, (256, 256, 768, 768))], []]
    invalid = [[candidate(0, 0, (10, 10, 10, 20), False)], []]
    worst = [[], []]
    for label in (0, 1):
        disjoint = [candidate(label, index, (2 * index, 0, 2 * index + 1, 1))
                    for index in range(31)]
        worst[label] = disjoint + [candidate(label, index, tuple(disjoint[-1]["box_q8"]))
                                   for index in range(31, 128)]
    return [
        ("analytic_iou_equal_half", equal),
        ("analytic_iou_above_half", above),
        ("analytic_rne_ties", rne),
        ("analytic_invalid_geometry", invalid),
        ("analytic_worst_6944_comparisons", worst),
    ]


def all_cases() -> list[dict]:
    cases = []
    for case_id, name in enumerate(FROZEN_CASES):
        candidates, events = frozen_case(name)
        result = run_nms(candidates)
        assert_frozen_exact(name, candidates, result, events)
        cases.append({"case_id": case_id, "name": name, "origin": "frozen",
                      "candidates": candidates, "result": result})
    for offset, (name, candidates) in enumerate(analytic_cases(), len(FROZEN_CASES)):
        result = run_nms(candidates)
        cases.append({"case_id": offset, "name": name, "origin": "analytic",
                      "candidates": candidates, "result": result})
    equal, above, rne, invalid, worst = cases[-5:]
    assert len(equal["result"]["outputs"]) == 2
    assert not equal["result"]["comparisons"][0]["suppress"]
    assert len(above["result"]["outputs"]) == 1
    assert above["result"]["comparisons"][0]["suppress"]
    assert rne["result"]["outputs"][0]["box_source"] == [2, 2, 8, 8]
    assert invalid["result"]["decisions"][0]["decision"] == "invalid"
    assert len(worst["result"]["comparisons"]) == 6944
    assert len(worst["result"]["outputs"]) == 62
    return cases


def case_metadata(case: dict, file_hashes: dict) -> dict:
    candidates, result = case["candidates"], case["result"]
    return {
        "schema": 1,
        "case_id": case["case_id"],
        "name": case["name"],
        "origin": case["origin"],
        "count_person": len(candidates[0]),
        "count_vehicle": len(candidates[1]),
        "output_count": len(result["outputs"]),
        "comparison_count": len(result["comparisons"]),
        "decision_count": len(result["decisions"]),
        "unread_after_class_cap": [len(candidates[label]) -
            sum(row["label"] == label for row in result["decisions"]) for label in (0, 1)],
        "outputs": result["outputs"],
        "comparisons": result["comparisons"],
        "decisions": result["decisions"],
        "files": file_hashes,
    }


def write_case(case: dict) -> dict:
    folder = VECTORS / f"case_{case['case_id']:02d}"
    folder.mkdir()
    candidates, result = case["candidates"], case["result"]
    candidate_words = []
    for label in (0, 1):
        words = [int(row["packed160_hex"], 16) for row in candidates[label]]
        candidate_words.extend(words + [0] * (128 - len(words)))
    output_words = [int(row["packed97_hex"], 16) for row in result["outputs"]]
    write_hex(folder / "candidate.hex", candidate_words, 160)
    write_hex(folder / "expected.hex", output_words + [0] * (64 - len(output_words)), 97)
    write_hex(folder / "comparisons.hex", [pack_comparison(row) for row in result["comparisons"]], 136)
    write_hex(folder / "decisions.hex", [pack_decision(row) for row in result["decisions"]], 10)
    hashes = {name: {"sha256": sha256(folder / name), "lines": len(read_hex(folder / name)),
                     "bits": bits}
              for name, bits in (("candidate.hex", 160), ("expected.hex", 97),
                                 ("comparisons.hex", 136), ("decisions.hex", 10))}
    write_json(folder / "case.json", case_metadata(case, hashes))
    return read_json(folder / "case.json")


def manifest_row(metadata: dict) -> str:
    return " ".join(map(str, (
        metadata["case_id"], metadata["count_person"], metadata["count_vehicle"],
        metadata["output_count"], metadata["comparison_count"], metadata["decision_count"],
        int(metadata["origin"] == "frozen"), int(metadata["origin"] == "analytic"))))


def vector_hashes() -> dict[str, str]:
    return {path.relative_to(OUT).as_posix(): sha256(path)
            for path in sorted(VECTORS.rglob("*")) if path.is_file()}


def build() -> None:
    if VECTORS.exists() or (OUT / "reference_result.json").exists():
        raise FileExistsError("reference outputs already exist; refusing overwrite")
    before = source_snapshot()
    cases = all_cases()
    VECTORS.mkdir()
    metadata = [write_case(case) for case in cases]
    manifest = [str(len(metadata)), *(manifest_row(row) for row in metadata)]
    (VECTORS / "manifest.txt").write_text("\n".join(manifest) + "\n", encoding="ascii")
    after = source_snapshot()
    assert before == after, "frozen reference changed during generation"
    result = {
        "status": "PASS_NMS_TRANSACTION_REFERENCE_NOT_RTL",
        "schema": 1,
        "case_count": len(cases),
        "frozen_cases_exact": len(FROZEN_CASES),
        "analytic_cases": len(cases) - len(FROZEN_CASES),
        "worst_case_comparisons": len(cases[-1]["result"]["comparisons"]),
        "source_hashes_unchanged": True,
        "source_sha256": after,
        "vector_sha256": vector_hashes(),
        "cases": [{key: row[key] for key in ("case_id", "name", "origin", "count_person",
                   "count_vehicle", "output_count", "comparison_count", "decision_count")}
                  for row in metadata],
        "RTL_run": False,
        "TD_run": False,
    }
    write_json(OUT / "reference_result.json", result)
    print("PASS_NMS_TRANSACTION_REFERENCE cases=16 frozen=11 comparisons_worst=6944")


def verify() -> None:
    receipt = read_json(OUT / "reference_result.json")
    assert receipt["source_sha256"] == source_snapshot()
    assert receipt["vector_sha256"] == vector_hashes()
    cases = all_cases()
    metadata_rows = []
    for case in cases:
        folder = VECTORS / f"case_{case['case_id']:02d}"
        metadata = read_json(folder / "case.json")
        metadata_rows.append(metadata)
        assert metadata == case_metadata(case, metadata["files"])
        candidate_words = []
        for label in (0, 1):
            words = [int(row["packed160_hex"], 16) for row in case["candidates"][label]]
            candidate_words.extend(words + [0] * (128 - len(words)))
        output_words = [int(row["packed97_hex"], 16) for row in case["result"]["outputs"]]
        assert read_hex(folder / "candidate.hex") == candidate_words
        assert read_hex(folder / "expected.hex") == output_words + [0] * (64 - len(output_words))
        assert [pack_comparison(row) for row in case["result"]["comparisons"]] == \
            read_hex(folder / "comparisons.hex")
        assert [pack_decision(row) for row in case["result"]["decisions"]] == \
            read_hex(folder / "decisions.hex")
    manifest = [str(len(metadata_rows)), *(manifest_row(row) for row in metadata_rows)]
    assert (VECTORS / "manifest.txt").read_text(encoding="ascii") == "\n".join(manifest) + "\n"
    print("PASS_NMS_TRANSACTION_REFERENCE_VERIFY source_hashes=unchanged vectors=exact")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build", action="store_true")
    args = parser.parse_args()
    build() if args.build else verify()
