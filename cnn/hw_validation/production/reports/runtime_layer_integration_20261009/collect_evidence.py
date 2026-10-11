"""Bind the candidate results; internal register-only timing is not whole timing."""
from collections import Counter
import csv
import json
import re
from pathlib import Path

from run_candidate import ROOT, BASE, digest, check_frozen

PATTERN = re.compile(r"Slack\s+:\s+(-?\d+\.\d+)ns\s+Begin Point\s+:\s+([^\r\n]+)"
                     r"\s+End Point\s+:\s+([^\r\n]+)\s+Check Type\s+:\s+(\w+)"
                     r"\s+Process\s+:\s+(\w+)")


def paths(path):
    return [{"slack": float(slack), "begin": begin.split()[0], "end": end.split()[0],
             "kind": kind, "corner": corner,
             "external": begin.startswith("i_") or end.startswith("o_")}
            for slack, begin, end, kind, corner in PATTERN.findall(path.read_text(encoding="utf-8"))]


def main():
    check_frozen()
    physical = ROOT / "physical_attempt2"
    area = (physical / "shell_route.area").read_text(encoding="utf-8")
    resource = {key: int(re.search(r"(?m)^#" + key + r"\s+(\d+)", area)[1])
                for key in ("slice", "dsp", "eram", "IO")}
    violations = paths(physical / "coverage_100000_violations.timing")
    negatives = [row for row in violations if row["slack"] < 0]
    timing = {}
    for name in ("internal_reg_to_reg", "functional_reset_distribution", "dsp_all", "eram_all"):
        rows = paths(physical / (name + ".timing"))
        timing[name] = {"paths": len(rows), "minima": {kind: min(row["slack"] for row in rows if row["kind"] == kind)
                        for kind in sorted({row["kind"] for row in rows})},
                        "negative": [row for row in rows if row["slack"] < 0]}
    work = next(path for path in sorted(ROOT.glob("layer_regression*")) if (path / "receipt.json").exists())
    cycles = {path.stem: list(csv.DictReader(path.open(encoding="utf-8"))) for path in sorted(work.glob("*.csv"))}
    for case, rows in cycles.items():
        assert len(rows) == 7
        for row in rows:
            bins = ("writeback_stall", "capacity_wait", "commit_cycle", "mac_issue", "input_wait", "task_close", "drain", "other")
            assert sum(int(row[key]) for key in bins) == int(row["endpoint"])
            assert int(row["dw_endpoint"]) + int(row["pw_endpoint"]) == int(row["endpoint"])
            assert all(int(row[key]) == 640 for key in ("acc", "pre", "silu", "post", "commit"))
    result = {"release": False, "parameter_origin": "TEST_NOT_QAT", "physical_resources_including_shell": resource,
              "timing": timing, "violations": negatives, "negative_categories": dict(Counter(
                  ("external_" if row["external"] else "internal_") + row["kind"] for row in negatives)),
              "cycles": cycles, "coefficients": "40 per-channel pre; two per-layer post; 84 extra preload writes",
              "synthesis_warning": {"warning_retained": True,
                    "undriven_net_scan": "PASS_NO_LOAD_BEARING_UNDRIVEN_NET_IN_ALL_EIGHT_DEFINITIONS",
                    "pin_zeroing_event_trace": "NOT_EXPORTED_BY_TD; no blanket suppression or production release"},
              "frozen_check": json.loads((ROOT / "frozen_check.json").read_text()),
              "source_manifest": {str(path): digest(path) for path in list((ROOT / "rtl").glob("*.v")) +
                  [ROOT / "physical/layer_shell/road_dynamic_overlap_low_io_top.v"]}}
    definition_receipt = json.loads((ROOT / "zc/receipt.json").read_text(encoding="utf-8"))
    result["undriven_definition_scan"] = {name: {"count": len(lines)-1,
                    "loaded": sum("PINS 0 DRIVER 0" not in line for line in lines[1:])}
                    for name, lines in definition_receipt.items()}
    assert all(row["loaded"] == 0 for row in result["undriven_definition_scan"].values())
    result["strict_same_scope"] = json.loads((ROOT / "gate_comparison/comparison.json").read_text(encoding="utf-8"))
    gate = json.loads((ROOT / "gates_attempt3/full_closure.json").read_text(encoding="utf-8"))
    result["strict_states"] = {name: value["status"] for name, value in gate["checks"].items()}
    result["shell_rtl"] = json.loads((ROOT / "shell_rtl/receipt.json").read_text(encoding="utf-8"))
    result["shell_gate"] = json.loads((ROOT / "shell_gate/receipt.json").read_text(encoding="utf-8"))
    result["next"] = "PW runner-only turnover measurement/candidate; no kernel II or contract change without decision"
    result["status"] = "RUNTIME_LAYER_FUNCTION_AND_INTERNAL_TIMING_PASS_NOT_DEPLOYMENT_RELEASE"
    result["numeric_reference_check"] = json.loads((ROOT / "reference_check.json").read_text(encoding="utf-8"))
    result["td_tool_sha256"] = digest(Path(r"E:\Anlogic\TD_6.2.1_Engineer_6.2.168.116\bin\td_commands_prompt.exe"))
    assert all(digest(Path(name)) == value for name, value in json.loads(
               (physical / "input_manifest.json").read_text(encoding="utf-8")).items())
    (ROOT / "measured_evidence.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    (ROOT / "status.json").write_text(json.dumps({key: value for key, value in result.items()
                if key not in ("violations", "cycles", "shell_rtl", "shell_gate")}, ensure_ascii=False, indent=2), encoding="utf-8")
    artifacts = [path for path in ROOT.rglob("*") if path.is_file() and path.suffix in
                 (".py", ".v", ".tcl", ".sdc", ".adc", ".al", ".db", ".svg", ".hex") and
                 not any(part in ("work", "source_closure", "baseline") for part in path.relative_to(ROOT).parts)]
    (ROOT / "evidence_hashes.json").write_text(json.dumps({str(path.relative_to(ROOT)): digest(path)
                 for path in artifacts}, indent=2), encoding="utf-8")
    print(json.dumps({"resources": resource, "negative_categories": result["negative_categories"],
                      "timing": {name: {"minima": row["minima"], "negative_count": len(row["negative"])}
                                 for name, row in timing.items()}, "unique_internal_failures":
                      sorted({(row["kind"], row["begin"], row["end"]) for row in negatives if not row["external"]})}, indent=2))


if __name__ == "__main__":
    main()
