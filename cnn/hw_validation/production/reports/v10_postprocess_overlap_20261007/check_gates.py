"""Strict, read-only RTL gates; preserve full findings and source identities."""
import argparse
import json
import shutil
import sys
from pathlib import Path
from guard import ROOT, PROJECT, bounded, check, digest, run

SKILL = Path(r"C:\Users\lenovo\.codex\skills\readable-verilog-generator")


def worker(target, output):
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(SKILL))
    from scripts.python.workflow.workspace import use_workspace_root
    from scripts.python.quality.deliverable_gate import (
        run_verilog_deliverable_gate, write_verilog_deliverable_gate_report)
    from scripts.python.quality.quality_gate import EXTERNAL_INTERFACE_SOURCES_SPEC_KEY
    interface = PROJECT / "cnn/hw_validation/interfaces/ph1p_eram_interface_complete.v"
    spec = {EXTERNAL_INTERFACE_SOURCES_SPEC_KEY: (interface,)}
    with use_workspace_root(PROJECT):
        gate = run_verilog_deliverable_gate(target, spec=spec, strict=True,
                                           include_testbench=False)
        write_verilog_deliverable_gate_report(gate, json_path=output.with_suffix(".json"),
                                             markdown_path=output.with_suffix(".md"))
    payload = {"strict": gate["strict"], "errors": gate["errors"],
               "strict_warnings": gate["strict_warnings"],
               "delivery_ready": gate["delivery_ready"],
               "checks": {key: value["status"] for key, value in gate["checks"].items()},
               "rules": gate["delivery_issues_by_rule"]}
    print(json.dumps(payload))
    return 0 if gate["delivery_ready"] else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--target", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.worker:
        return worker(bounded(args.target), bounded(args.output))
    check()
    closure = ROOT / "gates/source_closure"
    closure.mkdir(parents=True, exist_ok=False)
    prior = ROOT.parent
    inputs = [prior / "v9_mac_stream_20261007/core/road_mac_probe.v",
              prior / "v7_onchip_chain_20261006/inputs/road_round_shift.v",
              prior / "v7_onchip_chain_20261006/inputs/silu_shared_unit.v",
              ROOT / "rtl/road_postprocess_stream.v",
              ROOT / "rtl/down2_overlap_tile_runner.v"]
    inputs += [path for path in sorted((ROOT / "physical").glob("*.v"))
               if not path.name.startswith("tb_")]
    assert len(inputs) >= 6, "Actual physical top must exist before closure gate"
    identity = {}
    for path in inputs:
        target = closure / path.name
        assert not target.exists(), path
        shutil.copyfile(path, target)
        identity[str(path)] = {"sha256": digest(path), "snapshot": str(target)}
    (ROOT / "gates/source_manifest.json").write_text(json.dumps(identity, indent=2) + "\n",
                                                   encoding="utf-8")
    results = {}
    for target in [ROOT / "rtl/road_postprocess_stream.v",
                   ROOT / "rtl/down2_overlap_tile_runner.v", closure]:
        label = target.stem
        prefix = ROOT / "gates" / label
        command = [sys.executable, "-B", "-X", "utf8", str(Path(__file__).resolve()),
                   "--worker", "--target", str(target), "--output", str(prefix)]
        code = run(command, ROOT, prefix.with_suffix(".log"), timeout=1200)
        if code not in (0, 1) or not prefix.with_suffix(".json").exists():
            raise RuntimeError(f"Gate invocation failed: {label}, exit={code}")
        gate = json.loads(prefix.with_suffix(".json").read_text(encoding="utf-8"))
        rules = gate["delivery_issues_by_rule"]
        priority = {"VG097", "VG104", "VG122", "VG125", "VG130", "VG137",
                    "VG141", "VG153", "VG155"}
        results[label] = {"exit": code, "errors": gate["errors"],
                          "strict_warnings": gate["strict_warnings"],
                          "delivery_ready": gate["delivery_ready"],
                          "checks": {key: value["status"] for key, value in gate["checks"].items()},
                          "priority_semantics": {key: val for key, val in rules.items() if key in priority},
                          "other_unclosed": {key: val for key, val in rules.items() if key not in priority},
                          "raw_report_sha256": digest(prefix.with_suffix(".json"))}
    (ROOT / "gates/summary.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(results))
    print(json.dumps(check()))


if __name__ == "__main__":
    raise SystemExit(main())
