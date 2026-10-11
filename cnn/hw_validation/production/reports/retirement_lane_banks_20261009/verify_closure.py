"""Check immutable inputs and bind both candidate simulations to current RTL."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / "dynamic_overlap_20261008"
TAIL = ROOT.parent / "dw_tail_compact_20261009"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def verify_hashes(mapping, directory=None):
    for name, digest in mapping.items():
        path = Path(name) if directory is None else directory / name
        assert sha(path) == digest.lower(), str(path)
    return len(mapping)


def candidate(path):
    core = read(path / "tests/receipt.json")
    assert core["source_sha256_before"] == core["source_sha256_after"]
    verify_hashes(core["source_sha256_after"], path / "rtl")
    assert "batches=330 outputs=604" in core["pass_marker"]
    if path == ROOT:
        assert "valid_xz=0" in core["pass_marker"]
    layer = read(path / "tests/layer/receipt.json")
    assert layer["sources_before"] == layer["sources_after"]
    verify_hashes(layer["sources_after"])
    counts = {}
    for fixture, rows in layer["results"].items():
        assert len(rows) == 7
        for row in rows:
            bins = ("writeback_stall", "capacity_wait", "commit_cycle", "mac_issue",
                    "input_wait", "task_close", "drain", "other")
            assert sum(row[key] for key in bins) == row["endpoint"]
            assert row["dw_endpoint"] + row["pw_endpoint"] == row["endpoint"]
            assert all(row[key] == 640 for key in ("acc", "pre", "silu", "post", "commit"))
            assert row["export"] == 384
        counts[fixture] = rows[0]
    gate = read(path / "gates/rtl_gate.json")
    assert gate["checks"]["compile"]["status"] == "passed"
    assert gate["checks"]["ast"]["parse_errors"] == 0
    assert not gate["delivery_ready"]
    return {
        "core": core["pass_marker"], "layer_cases": 14,
        "no_stall": counts, "current_rtl_sha256": core["source_sha256_after"],
        "strict": {"errors": gate["errors"], "warnings": gate["strict_warnings"],
                   "states": {key: value["status"] for key, value in gate["checks"].items()},
                   "rules": dict(Counter(row["rule"] for row in gate["findings"]))},
    }


def negative_paths(path):
    pattern = (r"Slack\s+:\s+(-?\d+\.\d+)ns\s+Begin Point\s+:\s+([^\r\n]+)"
               r"\s+End Point\s+:\s+([^\r\n]+)\s+Check Type\s+:\s+(\w+)")
    result = []
    for slack, begin, end, kind in re.findall(pattern, path.read_text(encoding="utf-8")):
        if float(slack) < 0:
            begin, end = begin.split()[0], end.split()[0]
            result.append({"slack_ns": float(slack), "begin": begin, "end": end,
                           "kind": kind, "external": begin.startswith("i_") or end.startswith("o_")})
    return result


def physical(path, scope):
    directory = path / "physical" / scope
    original = BASE / "physical" / scope
    for suffix in ("sdc", "adc"):
        assert sha(directory / ("shell." + suffix)) == sha(original / ("shell." + suffix))
    shell = "road_dynamic_chain_low_io_top.v" if scope == "runtime_chain" else "road_dynamic_overlap_low_io_top.v"
    assert sha(directory / shell) == sha(original / shell)
    assert (directory / "pr.db").is_file()
    assert not re.search(r"(?m)^\s*bitgen\b", (directory / "build.tcl").read_text(encoding="utf-8"))
    area = (directory / "shell_route.area").read_text(encoding="utf-8")
    resources = {key: int(re.search(r"(?m)^#" + key + r"\s+(\d+)", area)[1])
                 for key in ("slice", "dsp", "eram", "IO")}
    assert resources["IO"] == 38
    negatives = negative_paths(directory / "coverage_100000_violations.timing")
    reset = negative_paths(directory / "functional_reset_distribution.timing")
    with (directory / "coverage_100000_all_paths.timing").open(encoding="utf-8") as stream:
        header = "".join(next(stream) for _ in range(25))
    assert "100.00%" in header and "Routed" in header and "Both (Slow and Fast)" in header
    return {"resources_including_shell": resources, "negative_paths_main_report": negatives,
            "negative_paths_reset_special_report": reset, "coverage": "100.00% routed, Slow/Fast",
            "main_internal_failures": sum(not row["external"] for row in negatives),
            "source_sha256": {file.name: sha(file) for file in (path / "rtl").glob("*.v")},
            "shell_sha256": sha(directory / shell), "constraints_sha256": {
                suffix: sha(directory / ("shell." + suffix)) for suffix in ("sdc", "adc")},
            "gate_db_sha256": sha(directory / "gate.db"), "pr_db_sha256": sha(directory / "pr.db")}


def main():
    assert sha(BASE / "delivery_receipt.json") == sha(ROOT / "baseline_receipt.json")
    historical_count = verify_hashes(read(BASE / "frozen.json"))
    original_count = verify_hashes(read(BASE / "delivery_receipt.json")["artifact_sha256"], BASE)
    for path in (ROOT, TAIL):
        for name in ("road_mac_probe.v", "road_dynamic_requant.v", "road_round_shift.v",
                     "silu_shared_unit.v", "road_down2_dynamic_adapter.v"):
            assert sha(path / "rtl" / name) == sha(BASE / "rtl" / name), (path, name)
    assert sha(ROOT / "rtl/down2_dynamic_tile_runner.v") == sha(BASE / "rtl/down2_dynamic_tile_runner.v")
    assert sha(ROOT / "rtl/road_dynamic_postprocess.v") == sha(TAIL / "rtl/road_dynamic_postprocess.v")
    for original in (BASE / "rtl").glob("*.v"):
        assert sha(original) == sha(ROOT / "gates/baseline_rtl" / original.name)
    result = {"status": "FUNCTIONAL_CLOSURE_PASS_NOT_PHYSICAL_OR_DELIVERY",
              "historical_frozen_files": historical_count,
              "original_artifacts": original_count,
              "A": candidate(ROOT), "B": candidate(TAIL)}
    assert result["A"]["no_stall"]["original"]["endpoint"] == 3331
    assert result["B"]["no_stall"]["original"]["endpoint"] == 3203
    result["baseline_strict_errors_same_seven_rtl"] = read(ROOT / "gates/baseline_same_scope.json")["errors"]
    if (TAIL / "physical/layer_shell/functional_reset_distribution.timing").is_file():
        implementations = {"A_runtime": physical(ROOT, "runtime_chain"),
                           "A_layer": physical(ROOT, "layer_shell"),
                           "B_layer": physical(TAIL, "layer_shell")}
        assert implementations["A_runtime"]["main_internal_failures"] == 0
        assert implementations["A_layer"]["main_internal_failures"] == 0
        assert implementations["B_layer"]["main_internal_failures"] == 5
        assert min(row["slack_ns"] for row in implementations["B_layer"]["negative_paths_reset_special_report"]) == -0.082
        result["physical"] = implementations
        result["decision"] = "A_INTERNAL_TIMING_PASS_DIAGNOSTIC_ONLY_B_INTERNAL_SETUP_FAILED"
        result["full_frame_fps"] = None
    with (ROOT / "closure_verification.json").open("w", encoding="utf-8") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
    print("CLOSURE_PASS", historical_count, original_count, "A=3331 B=3203")


if __name__ == "__main__":
    main()
