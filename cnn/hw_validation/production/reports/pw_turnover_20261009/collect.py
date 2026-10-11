"""汇总同源对拍及实际物理证据，保留外部时序和严格门禁未签核。"""
from collections import Counter
import csv
import difflib
import json
import re
from pathlib import Path

from run import ROOT, PREV, RUNNER, TB, tools, frozen

PATH = re.compile(r"Slack\s+:\s+(-?\d+\.\d+)ns\s+Begin Point\s+:\s+([^\r\n]+)"
                  r"\s+End Point\s+:\s+([^\r\n]+)\s+Check Type\s+:\s+(\w+)\s+Process\s+:\s+(\w+)")


def paths(path):
    return [{"slack": float(slack), "begin": begin.split()[0], "end": end.split()[0],
             "kind": kind, "corner": corner, "external": begin.startswith("i_") or end.startswith("o_")}
            for slack, begin, end, kind, corner in PATH.findall(path.read_text(encoding="utf-8"))]


def main():
    frozen()
    physical = ROOT / "physical"
    area = (physical / "shell_route.area").read_text(encoding="utf-8")
    resources = {name: int(re.search(r"(?m)^#"+name+r"\s+(\d+)", area)[1])
                 for name in ("slice", "dsp", "eram", "IO", "reg")}
    timing = {}
    for name in ("internal_reg_to_reg", "functional_reset_distribution", "reset_sync_interstage",
                 "external_reset_entry", "dsp_all", "eram_all"):
        rows = paths(physical / (name + ".timing"))
        timing[name] = {"paths": len(rows), "minima": {kind: min(row["slack"] for row in rows if row["kind"]==kind)
            for kind in sorted({row["kind"] for row in rows})}, "negative": [row for row in rows if row["slack"]<0]}
    negative = [row for row in paths(physical / "coverage_100000_violations.timing") if row["slack"]<0]
    gates = max((path for path in ROOT.glob("gates*") if (path / "comparison.json").exists()),
                key=lambda path: (path / "comparison.json").stat().st_mtime_ns)
    cycles = {}
    for label in ("baseline", "candidate"):
        work = max((path for path in ROOT.glob(label+"*") if (path / "receipt.json").exists()),
                   key=lambda path: (path / "receipt.json").stat().st_mtime_ns)
        cycles[label] = {}
        for path in sorted(work.glob("*.csv")):
            rows = [{key: int(value) for key, value in row.items()} for row in csv.DictReader(path.open(encoding="utf-8"))]
            assert len(rows)==10
            for row in rows:
                assert sum(row[key] for key in ("writeback_stall", "capacity_wait", "commit_cycle", "mac_issue",
                    "input_wait", "task_close", "drain", "other"))==row["endpoint"]
                assert row["dw_endpoint"]+row["pw_endpoint"]==row["endpoint"]
                assert all(row[key]==640 for key in ("acc", "pre", "silu", "post", "commit"))
                assert row["export"]==384 and row["pw_firsts"]==128
                assert sum(row[key] for key in ("pw_idle", "pw_storage", "pw_send", "pw_wait", "pw_dw_drain",
                    "pw_drain", "pw_done", "pw_fault", "pw_export", "pw_dw_post"))==row["pw_endpoint"]
            cycles[label][path.stem] = rows
    old = (PREV / "rtl/down2_dynamic_tile_runner.v").read_text(encoding="utf-8").splitlines(True)
    new = RUNNER.read_text(encoding="utf-8").splitlines(True)
    (ROOT / "runner.patch").write_text("".join(difflib.unified_diff(old, new,
        fromfile="frozen_runtime_runner", tofile="pw_prefetch_runner")), encoding="utf-8")
    result = {"status": "PW_PREFETCH_FUNCTION_AND_INTERNAL_TIMING_PASS_NOT_DEPLOYMENT_RELEASE",
        "release": False, "parameter_origin": "TEST_NOT_QAT", "resources_including_shell": resources,
        "timing": timing, "negative_categories": dict(Counter(("external_" if row["external"] else "internal_")+
            row["kind"] for row in negative)), "violations": negative, "cycles": cycles,
        "strict_comparison": json.loads((gates / "comparison.json").read_text(encoding="utf-8")),
        "strict_states": {key: value["status"] for key, value in json.loads(
            (gates / "candidate.json").read_text(encoding="utf-8"))["checks"].items()},
        "testbench_strict": {key: value for key, value in json.loads(
            (gates / "testbench.json").read_text(encoding="utf-8")).items() if key in (
                "errors", "strict_warnings", "checks", "delivery_ready")},
        "new_runner_undriven": json.loads((ROOT / "z/receipt.json").read_text(encoding="utf-8")),
        "shell_rtl": json.loads((ROOT / "shell_rtl_attempt2/receipt.json").read_text(encoding="utf-8")),
        "shell_gate": json.loads((ROOT / "shell_gate/receipt.json").read_text(encoding="utf-8")),
        "frozen": json.loads((ROOT / "frozen_check.json").read_text(encoding="utf-8")),
        "physical_source_manifest": json.loads((physical / "input_manifest.json").read_text(encoding="utf-8")),
        "td_sha256": tools.digest(tools.TD)}
    assert not [row for row in negative if not row["external"]]
    assert all(tools.digest(Path(name))==sha for name, sha in result["physical_source_manifest"].items())
    (ROOT / "measured_evidence.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    (ROOT / "status.json").write_text(json.dumps({key: value for key, value in result.items()
        if key not in ("violations", "cycles", "shell_rtl", "shell_gate", "new_runner_undriven")},
        ensure_ascii=False, indent=2), encoding="utf-8")
    artifacts = [path for path in ROOT.rglob("*") if path.is_file() and
        path.name != "evidence_hashes.json" and path.suffix in (".v", ".py", ".tcl", ".sdc", ".adc", ".al", ".db",
            ".csv", ".svg", ".md", ".json", ".log", ".timing", ".rpt", ".area") and
        not any(part in ("work", "baseline", "candidate", "__pycache__") for part in path.relative_to(ROOT).parts[:-1])]
    (ROOT / "evidence_hashes.json").write_text(json.dumps({str(path.relative_to(ROOT)): tools.digest(path)
        for path in artifacts}, indent=2), encoding="utf-8")
    print(json.dumps({"resources": resources, "negative_categories": result["negative_categories"],
        "timing": {key: value["minima"] for key, value in timing.items()}}, indent=2))


if __name__ == "__main__":
    main()
