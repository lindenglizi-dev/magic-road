"""6944-comparison, 64-output extra vector for road_nms_serial."""
from __future__ import annotations

import argparse
from pathlib import Path

import reference

OUT = Path(__file__).resolve().parent
CASE_DIR = OUT / "extras" / "worst_comparisons_full_output"
RESULT = OUT / "reference_extra_worst_result.json"
CASE_ID = 17


def previous_hashes() -> dict[str, str]:
    original = reference.read_json(OUT / "reference_result.json")
    assert original["source_sha256"] == reference.source_snapshot()
    large = reference.read_json(OUT / "reference_extra_result.json")
    for relative, expected in large["previous_sha256"].items():
        assert reference.sha256(OUT / relative) == expected
    for relative, expected in large["extra_sha256"].items():
        assert reference.sha256(OUT / relative) == expected
    assert reference.sha256(OUT / "reference_extra.py") == large["reference_extra_py_sha256"]
    paths = [OUT / "reference.py", OUT / "reference_result.json",
             OUT / "vectors" / "manifest.txt", OUT / "reference_extra.py",
             OUT / "reference_extra_result.json", OUT / "extras" / "manifest.txt"]
    paths += [OUT / relative for relative in large["extra_sha256"]
              if relative != "extras/manifest.txt"]
    return {path.relative_to(OUT).as_posix(): reference.sha256(path) for path in paths}


def make_case() -> dict:
    candidates = [[], []]
    for label in (0, 1):
        disjoint = [reference.candidate(label, index, (2 * index, 0, 2 * index + 1, 1))
                    for index in range(31)]
        repeats = [reference.candidate(label, index, tuple(disjoint[-1]["box_q8"]))
                   for index in range(31, 127)]
        final = reference.candidate(label, 127, (64, 0, 65, 1))
        candidates[label] = disjoint + repeats + [final]
    result = reference.run_nms(candidates)
    assert len(result["outputs"]) == 64
    assert len(result["comparisons"]) == 6944
    assert len(result["decisions"]) == 256
    for label in (0, 1):
        class_outputs = [row for row in result["outputs"] if row["label"] == label]
        class_decisions = [row for row in result["decisions"] if row["label"] == label]
        class_comparisons = [row for row in result["comparisons"] if row["label"] == label]
        assert len(class_outputs) == 32 and class_outputs[-1]["cell_id"] == label * 128 + 127
        assert [row["decision"] for row in class_decisions[:31]] == ["keep"] * 31
        assert [row["decision"] for row in class_decisions[31:127]] == ["suppressed"] * 96
        assert class_decisions[127]["decision"] == "keep"
        assert len(class_comparisons) == 3472
    return {"case_id": CASE_ID, "name": "worst_comparisons_full_output",
            "origin": "analytic", "candidates": candidates, "result": result}


def words(case: dict) -> tuple[list[int], list[int], list[int], list[int]]:
    candidate_words = []
    for label in (0, 1):
        candidate_words.extend(int(row["packed160_hex"], 16) for row in case["candidates"][label])
    result = case["result"]
    return (candidate_words,
            [int(row["packed97_hex"], 16) for row in result["outputs"]],
            [reference.pack_comparison(row) for row in result["comparisons"]],
            [reference.pack_decision(row) for row in result["decisions"]])


def metadata(case: dict, hashes: dict) -> dict:
    value = reference.case_metadata(case, hashes)
    value["numeric_proofs"] = {
        "comparisons_per_class": 3472,
        "comparisons_total": 6944,
        "outputs_per_class": 32,
        "outputs_total": 64,
        "sequence_per_class": "31 disjoint keep, 96 repeat-last suppress, final disjoint keep",
    }
    return value


def build() -> None:
    if CASE_DIR.exists() or RESULT.exists():
        raise FileExistsError("worst extra outputs already exist; refusing overwrite")
    before = previous_hashes()
    case = make_case()
    CASE_DIR.mkdir()
    names = ("candidate.hex", "expected.hex", "comparisons.hex", "decisions.hex")
    bits = (160, 97, 136, 10)
    for name, values, width in zip(names, words(case), bits, strict=True):
        reference.write_hex(CASE_DIR / name, values, width)
    hashes = {name: {"sha256": reference.sha256(CASE_DIR / name),
                     "lines": len(reference.read_hex(CASE_DIR / name)), "bits": width}
              for name, width in zip(names, bits, strict=True)}
    reference.write_json(CASE_DIR / "case.json", metadata(case, hashes))
    after = previous_hashes()
    assert before == after, "existing references changed"
    extra_hashes = {path.relative_to(OUT).as_posix(): reference.sha256(path)
                    for path in sorted(CASE_DIR.iterdir()) if path.is_file()}
    reference.write_json(RESULT, {
        "status": "PASS_NMS_6944_COMPARISON_64_OUTPUT_EXTRA_NOT_RTL",
        "schema": 1,
        "case_id": CASE_ID,
        "case_path": "extras/worst_comparisons_full_output",
        "count_person": 128,
        "count_vehicle": 128,
        "output_count": 64,
        "comparison_count": 6944,
        "decision_count": 256,
        "previous_hashes_unchanged": True,
        "previous_sha256": after,
        "extra_sha256": extra_hashes,
        "reference_extra_worst_py_sha256": reference.sha256(Path(__file__)),
        "RTL_run": False,
        "TD_run": False,
    })
    print("PASS_NMS_6944_COMPARISON_64_OUTPUT_EXTRA comparisons=6944 outputs=64")


def verify() -> None:
    receipt = reference.read_json(RESULT)
    assert receipt["previous_sha256"] == previous_hashes()
    assert receipt["reference_extra_worst_py_sha256"] == reference.sha256(Path(__file__))
    assert receipt["extra_sha256"] == {
        path.relative_to(OUT).as_posix(): reference.sha256(path)
        for path in sorted(CASE_DIR.iterdir()) if path.is_file()
    }
    case = make_case()
    stored = reference.read_json(CASE_DIR / "case.json")
    assert stored == metadata(case, stored["files"])
    for name, values in zip(("candidate.hex", "expected.hex", "comparisons.hex", "decisions.hex"),
                            words(case), strict=True):
        assert reference.read_hex(CASE_DIR / name) == values
    print("PASS_NMS_6944_COMPARISON_64_OUTPUT_EXTRA_VERIFY previous=unchanged vectors=exact")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build", action="store_true")
    arguments = parser.parse_args()
    build() if arguments.build else verify()
