"""Index and verify saved C2-to-C9 vectors without CNN inference."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).absolute().parent
ROOT = HERE.parents[3]
MANIFEST = HERE / "vector_manifest.json"
C2_ASSETS = ROOT / "cnn/hw_validation/production/head_decode_topk_rtl_20261015/verification/assets"
GOLDEN = ROOT / "cnn/hw_validation/production/postprocess_golden_2fps_20261015"
PACKAGE = ROOT / "cnn/reports/qat_frozen_stem_g10_20261014_v1/package/numeric_test.bin"
EXTRA = HERE / "assets/worst_comparisons_full_output"
C9_STRESS = ROOT / "cnn/hw_validation/production/nms_serial_rtl_20261015/extras/worst_comparisons_full_output/case.json"
PAYLOAD_SHA256 = "b35d4a66a69e441dc29bc60c7e3f507661f48da5f33b810d7340f6ed17a65145"
MODEL_ID32 = "B35D4A66"
PINNED = {
    "c2_cases": "14bd5c85df42824bfd661ddeabd96585d260e478782ea9dde4fc6c515d40ac72",
    "sigmoid_lut": "889fa62b54d26210c37e9260c3e954d1913c0606593381152a2846b2609419ca",
    "exp_lut": "135731b97a0a144eacf953b80a540eb68591bcb6b5bddb588824917218ca8d0c",
    "integer": "441b91d86895fb0c0337583325fb9cc39624026a6759d39da51aaab49a5ca040",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def record(path: Path, **metadata) -> dict:
    return {"path": relative(path), "sha256": sha256(path), "bytes": path.stat().st_size,
            **metadata}


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def hex_words(path: Path, bits: int) -> list[int]:
    words = []
    with path.open("r", encoding="ascii") as stream:
        for line_number, line in enumerate(stream, 1):
            text = line.strip()
            if not text:
                continue
            value = int(text, 16)
            if value >= 1 << bits:
                raise ValueError(f"{relative(path)}:{line_number} exceeds {bits} bits")
            words.append(value)
    return words


def nms_summary(path: Path) -> dict:
    decisions = Counter()
    events = comparisons = 0
    with path.open("r", encoding="utf-8") as stream:
        for line in stream:
            if not line.strip():
                continue
            row = json.loads(line)
            events += 1
            comparisons += len(row["comparisons"])
            decisions[row["decision"]] += 1
    return {"event_count": events, "comparison_count": comparisons,
            "decision_counts": dict(sorted(decisions.items()))}


def case_entry(case_id: int, name: str, heads: Path, decoded: Path,
               expected_person: int, expected_vehicle: int, origin: str) -> dict:
    folder = heads.parent
    final_hex = folder / "result_table_97.hex"
    final_json = folder / "final.json"
    nms_events = folder / "nms_events.jsonl"
    head_words = hex_words(heads, 112)
    decoded_words = hex_words(decoded, 160)
    final_words = hex_words(final_hex, 97)
    if len(head_words) != 12096:
        raise ValueError(f"{name}: expected 12096 head words")
    decoded_counts = [sum(((word >> 102) & 1) == label for word in decoded_words)
                      for label in (0, 1)]
    if decoded_counts != [expected_person, expected_vehicle]:
        raise ValueError(f"{name}: decoded class counts changed")
    if any(word >> 104 for word in decoded_words):
        raise ValueError(f"{name}: DECODED160 reserved bits nonzero")
    saved_final = read_json(final_json)
    if not (len(final_words) == saved_final["box_count"] == len(saved_final["detections"]) <= 64):
        raise ValueError(f"{name}: FINAL97/final.json count mismatch")
    final_counts = [sum(row["label"] == label for row in saved_final["detections"])
                    for label in (0, 1)]
    if final_counts != [sum((word & 1) == label for word in final_words) for label in (0, 1)]:
        raise ValueError(f"{name}: FINAL97 class bits disagree with final.json")
    nms = nms_summary(nms_events)
    if nms["event_count"] != len(decoded_words):
        raise ValueError(f"{name}: NMS event count disagrees with decoded candidates")
    return {
        "case_id": case_id,
        "name": name,
        "origin": origin,
        "expected": {
            "head_words": len(head_words),
            "person_candidates": decoded_counts[0],
            "vehicle_candidates": decoded_counts[1],
            "decoded_candidates": len(decoded_words),
            "final_entries": len(final_words),
            "final_person": final_counts[0],
            "final_vehicle": final_counts[1],
            **nms,
        },
        "heads112": record(heads, words=len(head_words), bits=112),
        "decoded160": record(decoded, words=len(decoded_words), bits=160),
        "final97": record(final_hex, words=len(final_words), bits=97),
        "final_json": record(final_json),
        "nms_events": record(nms_events, events=nms["event_count"],
                             comparisons=nms["comparison_count"]),
    }


def build_extra() -> None:
    """The only golden execution: construct one new saved-head stress case, never a CNN."""
    if EXTRA.exists():
        raise FileExistsError(f"refusing to overwrite {EXTRA}")
    sys.path.insert(0, str(ROOT))
    import numpy as np
    from cnn.hw_validation.production.postprocess_golden_2fps_20261015 import golden

    heads = golden.empty_heads()
    for cell in range(128):
        target_index = cell if cell < 31 else (31 if cell == 127 else 30)
        target_x = 8 + 12 * target_index
        grid_x = cell
        raw = (target_x * 64 - grid_x * 256, 8 * 64, 0, 0)
        if any(not -32768 <= value <= 32767 for value in raw):
            raise ValueError("constructed head raw value outside INT16")
        golden.activate(heads, cell, raw=raw, logits=(2048, 2048, 2048))
    result = golden.trace(heads)
    comparisons = sum(len(row["comparisons"]) for row in result["nms"])
    if len(result["final"]) != 64 or comparisons != 6944:
        raise AssertionError("constructed full-head stress missed 64 outputs / 6944 comparisons")
    EXTRA.mkdir(parents=True)
    head_words = [sum((int(value) & 65535) << (16 * index)
                      for index, value in enumerate(raw))
                  for head in heads for raw in head.reshape(-1, 7)]
    golden.hex_lines(EXTRA / "heads_cell_order_112.hex", head_words, 112)
    golden.hex_lines(EXTRA / "top128_decoded_160.hex",
                     [golden.decoded160(row) for row in result["sorted_top128"]], 160)
    golden.hex_lines(EXTRA / "result_table_97.hex",
                     [golden.result97(row) for row in result["final"]], 97)
    golden.jsonl(EXTRA / "nms_events.jsonl", result["nms"])
    golden.save(EXTRA / "final.json", {
        "result_status": 0,
        "box_count": len(result["final"]),
        "detections": result["final"],
        "logical_operation_counts": result["logical_operation_counts"],
        "source": "saved synthetic S4 head stream; no CNN inference",
    })
    del np


def build_manifest() -> dict:
    c2_path = C2_ASSETS / "cases.json"
    sigmoid_path = C2_ASSETS / "sigmoid_lut_16.hex"
    exp_path = C2_ASSETS / "exp_lut_16.hex"
    integer_path = ROOT / "cnn/integer.py"
    for name, path in (("c2_cases", c2_path), ("sigmoid_lut", sigmoid_path),
                       ("exp_lut", exp_path), ("integer", integer_path)):
        if sha256(path) != PINNED[name]:
            raise AssertionError(f"pinned source changed: {relative(path)}")
    c2 = read_json(c2_path)
    if c2["payload_sha256"] != PAYLOAD_SHA256 or c2["model_id32"] != MODEL_ID32:
        raise AssertionError("C2 model identity changed")
    if sha256(PACKAGE) != PAYLOAD_SHA256 or PAYLOAD_SHA256[:8].upper() != MODEL_ID32:
        raise AssertionError("payload/model identity mismatch")
    delivery_path = GOLDEN / "delivery_manifest.json"
    delivery = read_json(delivery_path)
    boundary_path = GOLDEN / "boundary_vectors.json"
    if delivery["payload_sha256"] != PAYLOAD_SHA256:
        raise AssertionError("golden delivery payload changed")
    if sha256(boundary_path) != c2["boundary_vectors_sha256"]:
        raise AssertionError("boundary vector source changed")
    if len(hex_words(sigmoid_path, 16)) != 1024 or len(hex_words(exp_path, 16)) != 256:
        raise AssertionError("LUT dimensions changed")
    cases = []
    for case_id, saved in enumerate(c2["cases"]):
        heads = ROOT / saved["heads"]
        decoded = ROOT / saved["decoded160"]
        if sha256(heads) != saved["heads_sha256"] or sha256(decoded) != saved["decoded160_sha256"]:
            raise AssertionError(f"{saved['name']}: C2 vector hash changed")
        cases.append(case_entry(case_id, saved["name"], heads, decoded,
                                saved["person_count"], saved["vehicle_count"], "frozen_golden"))
    extra = case_entry(11, "worst_comparisons_full_output",
                       EXTRA / "heads_cell_order_112.hex",
                       EXTRA / "top128_decoded_160.hex", 128, 128,
                       "new_saved_heads_via_frozen_golden")
    c9 = read_json(C9_STRESS)
    if not (c9["comparison_count"] == 6944 and c9["output_count"] == 64):
        raise AssertionError("C9-only stress identity changed")
    by_name = {case["name"]: case for case in cases}
    real = by_name["real_image"]["expected"]
    full = by_name["top128_ties_and_each32_total64"]["expected"]
    if not (real["final_entries"] == 7 and real["comparison_count"] == 16):
        raise AssertionError("real-image expected counts changed")
    if not (full["decoded_candidates"] == 256 and full["final_entries"] == 64
            and full["comparison_count"] == 992):
        raise AssertionError("full Top128 expected counts changed")
    if not (extra["expected"]["final_entries"] == 64
            and extra["expected"]["comparison_count"] == 6944):
        raise AssertionError("joint 6944-comparison extra changed")
    return {
        "schema": 1,
        "scope": "saved 12096-word head streams to frozen FINAL97; no CNN inference",
        "model": {"model_id32": MODEL_ID32, "payload_sha256": PAYLOAD_SHA256,
                  "payload": record(PACKAGE)},
        "limits": {"head_words_per_case": 12096, "candidates_per_class": 128,
                   "final_entries": 64},
        "sources": {
            "checker": record(Path(__file__).absolute()),
            "c2_cases": record(c2_path),
            "golden_delivery_manifest": record(delivery_path),
            "boundary_vectors": record(boundary_path),
            "lut_source": record(integer_path),
            "sigmoid_lut_16": record(sigmoid_path, words=1024, bits=16),
            "exp_lut_16": record(exp_path, words=256, bits=16),
        },
        "cases": cases,
        "joint_extra_cases": [extra],
        "comparison_landmarks": {
            "real_image": {"final_entries": 7, "nms_comparisons": 16},
            "frozen_top128_both_classes": {"decoded_candidates": 256,
                                            "final_entries": 64, "nms_comparisons": 992},
            "joint_saved_head_stress": {"head_words": 12096, "final_entries": 64,
                                          "nms_comparisons": 6944},
            "c9_only_direct_candidate_stress": {
                "included_in_joint_cases": False,
                "final_entries": 64,
                "nms_comparisons": 6944,
                "source": record(C9_STRESS),
            },
        },
        "case_count": len(cases),
        "joint_extra_case_count": 1,
        "CNN_inference_runs": 0,
    }


def render(value: dict) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="read-only exact manifest/source verification")
    args = parser.parse_args()
    if not args.check and not EXTRA.exists():
        build_extra()
    expected = render(build_manifest())
    if args.check:
        if not MANIFEST.is_file() or MANIFEST.read_text(encoding="utf-8") != expected:
            print("JOINT_VECTOR_CHECK_FAIL manifest_or_source_changed")
            return 1
        print("JOINT_VECTOR_CHECK_PASS cases=11 extras=1 heads=12096 real=7 full=64/992 stress=64/6944")
        return 0
    if MANIFEST.exists():
        raise FileExistsError(f"refusing to overwrite {MANIFEST}")
    MANIFEST.write_text(expected, encoding="utf-8", newline="\n")
    if render(build_manifest()) != expected:
        raise AssertionError("source changed while writing manifest")
    print("JOINT_VECTOR_BUILD_PASS cases=11 extras=1 heads=12096 inference=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
