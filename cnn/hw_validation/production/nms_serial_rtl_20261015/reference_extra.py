"""Large-area numeric vector for road_nms_serial; leaves the frozen 16 cases intact."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import reference

OUT = Path(__file__).resolve().parent
EXTRAS = OUT / "extras"
CASE_DIR = EXTRAS / "full_frame_area"
RESULT = OUT / "reference_extra_result.json"
CASE_ID = 16


def previous_hashes() -> dict[str, str]:
    receipt = reference.read_json(OUT / "reference_result.json")
    assert receipt["source_sha256"] == reference.source_snapshot()
    paths = (OUT / "reference.py", OUT / "reference_result.json",
             OUT / "vectors" / "manifest.txt")
    return {path.relative_to(OUT).as_posix(): reference.sha256(path) for path in paths}


def make_case() -> dict:
    full = (0, 0, 512 * 256, 288 * 256)
    half = (0, 0, 256 * 256, 288 * 256)
    invalid_at_max = (512 * 256, 288 * 256, 512 * 256, 288 * 256)
    candidates = [[], []]
    for label in (0, 1):
        candidates[label] = [
            reference.candidate(label, 0, full),
            reference.candidate(label, 1, full),
            reference.candidate(label, 2, half),
            reference.candidate(label, 3, invalid_at_max, False),
        ]
    result = reference.run_nms(candidates)
    assert len(result["outputs"]) == 4
    assert len(result["comparisons"]) == 4
    assert len(result["decisions"]) == 8
    assert [row["decision"] for row in result["decisions"]] == \
        ["keep", "suppressed", "keep", "invalid"] * 2
    for label in (0, 1):
        comparisons = [row for row in result["comparisons"] if row["label"] == label]
        assert comparisons[0]["intersection"] == comparisons[0]["area_a"] == \
            comparisons[0]["area_b"] == 9_663_676_416
        assert comparisons[0]["suppress"]
        assert comparisons[1]["intersection"] == comparisons[1]["area_a"] == 4_831_838_208
        assert comparisons[1]["area_b"] == 9_663_676_416
        assert 3 * comparisons[1]["intersection"] == \
            comparisons[1]["area_a"] + comparisons[1]["area_b"]
        assert not comparisons[1]["suppress"]
    assert [row["box_source"] for row in result["outputs"]] == \
        [[0, 0, 1280, 720], [0, 0, 640, 720]] * 2
    return {"case_id": CASE_ID, "name": "full_frame_area", "origin": "analytic",
            "candidates": candidates, "result": result}


def expected_words(case: dict) -> tuple[list[int], list[int], list[int], list[int]]:
    candidates, result = case["candidates"], case["result"]
    candidate_words = []
    for label in (0, 1):
        words = [int(row["packed160_hex"], 16) for row in candidates[label]]
        candidate_words.extend(words + [0] * (128 - len(words)))
    outputs = [int(row["packed97_hex"], 16) for row in result["outputs"]]
    comparisons = [reference.pack_comparison(row) for row in result["comparisons"]]
    decisions = [reference.pack_decision(row) for row in result["decisions"]]
    return candidate_words, outputs + [0] * (64 - len(outputs)), comparisons, decisions


def metadata(case: dict, hashes: dict) -> dict:
    value = reference.case_metadata(case, hashes)
    value["numeric_proofs"] = {
        "full_frame_area": 9_663_676_416,
        "half_frame_area": 4_831_838_208,
        "full_frame_area_exceeds_uint32": True,
        "strict_half_equality_not_suppressed": True,
        "source_bounds": [1280, 720],
        "max_coordinate_zero_geometry_skipped": True,
    }
    return value


def build() -> None:
    if EXTRAS.exists() or RESULT.exists():
        raise FileExistsError("extra reference outputs already exist; refusing overwrite")
    before = previous_hashes()
    case = make_case()
    CASE_DIR.mkdir(parents=True)
    names = ("candidate.hex", "expected.hex", "comparisons.hex", "decisions.hex")
    bits = (160, 97, 136, 10)
    for name, words, width in zip(names, expected_words(case), bits, strict=True):
        reference.write_hex(CASE_DIR / name, words, width)
    hashes = {name: {"sha256": reference.sha256(CASE_DIR / name),
                     "lines": len(reference.read_hex(CASE_DIR / name)), "bits": width}
              for name, width in zip(names, bits, strict=True)}
    reference.write_json(CASE_DIR / "case.json", metadata(case, hashes))
    row = reference.manifest_row(reference.read_json(CASE_DIR / "case.json"))
    (EXTRAS / "manifest.txt").write_text(f"1\n{row}\n", encoding="ascii")
    after = previous_hashes()
    assert before == after, "existing 16-case reference changed"
    extra_files = {path.relative_to(OUT).as_posix(): reference.sha256(path)
                   for path in sorted(EXTRAS.rglob("*")) if path.is_file()}
    reference.write_json(RESULT, {
        "status": "PASS_NMS_LARGE_AREA_EXTRA_NOT_RTL",
        "schema": 1,
        "case_id": CASE_ID,
        "case_path": "extras/full_frame_area",
        "count_person": 4,
        "count_vehicle": 4,
        "output_count": 4,
        "comparison_count": 4,
        "decision_count": 8,
        "full_frame_area": 9_663_676_416,
        "previous_hashes_unchanged": True,
        "previous_sha256": after,
        "extra_sha256": extra_files,
        "reference_extra_py_sha256": reference.sha256(Path(__file__)),
        "RTL_run": False,
        "TD_run": False,
    })
    print("PASS_NMS_LARGE_AREA_EXTRA area=9663676416 comparisons=4 outputs=4")


def verify() -> None:
    receipt = reference.read_json(RESULT)
    assert receipt["previous_sha256"] == previous_hashes()
    assert receipt["reference_extra_py_sha256"] == reference.sha256(Path(__file__))
    assert receipt["extra_sha256"] == {
        path.relative_to(OUT).as_posix(): reference.sha256(path)
        for path in sorted(EXTRAS.rglob("*")) if path.is_file()
    }
    case = make_case()
    stored = reference.read_json(CASE_DIR / "case.json")
    assert stored == metadata(case, stored["files"])
    for name, words in zip(("candidate.hex", "expected.hex", "comparisons.hex", "decisions.hex"),
                           expected_words(case), strict=True):
        assert reference.read_hex(CASE_DIR / name) == words
    assert (EXTRAS / "manifest.txt").read_text(encoding="ascii") == \
        "1\n" + reference.manifest_row(stored) + "\n"
    print("PASS_NMS_LARGE_AREA_EXTRA_VERIFY previous=unchanged vectors=exact")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build", action="store_true")
    arguments = parser.parse_args()
    build() if arguments.build else verify()
