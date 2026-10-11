"""Publish bounded receipts and canonical spec attempts in this directory only."""

import json
import sys
from pathlib import Path

from run_stage import ROOT, BASE, SKILL, publish, run, sha, check


def main():
    specs = ROOT / "specs"
    attempt = 1
    while specs.exists():
        attempt += 1
        specs = ROOT / f"specs_attempt{attempt}"
    specs.mkdir()
    waveform = {"signal": [{"name": "clk", "wave": "p........."},
                           {"name": "valid", "wave": "0.1...0..."},
                           {"name": "ready", "wave": "1.0..1...."},
                           {"name": "payload", "wave": "x.=...x...", "data": ["held until handshake"]}]}
    publish(str(specs.relative_to(ROOT)) + "/handshake.json", waveform)
    for name in ("tb_dynamic_shell_vectors", "tb_representative_chain", "road_driven_probe"):
        ports = []
        if name == "road_driven_probe":
            ports = [{"name": port, "direction": "output" if port == "o_data" else "input",
                      "width": 1, "role": port, "description": port, "clock_domain": "i_clk"}
                     for port in ("i_clk", "i_rstn", "i_data", "o_data")]
        module = {"name": name, "feature": "step1", "rtl_path": name + ".v",
                  "description": "Independent evidence probe; no production change.",
                  "interfaces": {"protocol": "discrete", "ports": ports}, "parameters": [],
                  "clock": {"name": "i_clk" if ports else "internal test clock", "edge": "posedge", "frequency_hz": 100000000},
                  "reset": {"name": "i_rstn" if ports else "internal test reset", "active": "low", "synchronous": False,
                            "values": "Cancel old transactions; reload table before calculation."},
                  "behavior": ["Verify runtime operands against frozen integer results; do not change the DUT."],
                  "constraints": ["Diagnostic only; no bitgen, new timing exceptions or board claim."],
                  "corner_cases": ["Output must remain stable during backpressure; reset cancels pending work."],
                  "verification_cases": ["Use actual installed vendor models and retained logs."],
                  "timing_diagrams": [{"id": "hold", "title": "Payload ownership", "scenario": "ready_valid",
                                       "description": "Handshake protocol schematic, not measured pipeline latency.", "wavejson": waveform}]}
        publish(str(specs.relative_to(ROOT)) + f"/{name}.contract.json", {"modules": [module]})
        code = f"import sys;sys.path.insert(0,{str(SKILL)!r});from scripts.python.workflow.cli import main;raise SystemExit(main())"
        source = ROOT / (name + ".v") if not ports else ROOT / "syn5025_probe" / (name + ".v")
        log = run([sys.executable, "-B", "-X", "utf8", "-c", code, "write-spec", "--spec",
                   specs / (name + ".contract.json"), "--out-dir", specs / "generated", "--source", source,
                   "--no-state"], ROOT, specs.name + "/" + name, allowed=(0, 1, 2))
        if not ports:
            assert "ports must be non-empty" in log, log
    render_code = f"import sys;sys.path.insert(0,{str(SKILL)!r});from scripts.python.toolchain.wavedrom_runtime import main;raise SystemExit(main())"
    run([sys.executable, "-B", "-X", "utf8", "-c", render_code, "render", "--input",
         specs / "handshake.json", "--output", specs / "handshake.svg"], ROOT, specs.name + "/waveform")
    manifest = json.loads((ROOT / "representative_manifest.json").read_text(encoding="utf-8"))
    text = (ROOT / "representative_replay/representative.log").read_text(encoding="utf-8")
    measured = []
    for line in text.splitlines():
        if "REP_TASK " in line:
            task, groups, mac, endpoint = map(int, line.split("REP_TASK ")[1].split())
            measured.append((task, groups, mac, endpoint))
    assert len(measured) == manifest["tasks"]
    offset = 0
    for case in manifest["cases"]:
        rows = measured[offset:offset + case["tasks"]]
        assert sum(row[1] for row in rows) == case["input_groups"]
        case["serial_driver_cycles"] = sum(row[3] for row in rows)
        case["mac_accept_window_min_max"] = [min(row[2] for row in rows), max(row[2] for row in rows)]
        case["task_endpoint_min_max"] = [min(row[3] for row in rows), max(row[3] for row in rows)]
        offset += case["tasks"]
    publish("representative_cycles.json", manifest)
    gate = json.loads((ROOT / "gates/shell_tb.json").read_text(encoding="utf-8"))
    publish("status.json", {
        "stage": "STEP1_FUNCTIONAL_EVIDENCE_PASS_INTEGRATION_PENDING", "release": False,
        "rtl_vs_gate": {"packets": 330, "results": 604, "cycles": 32014, "mismatches": 0, "sdf": False},
        "original_core": "PASS with actual PH1P library; eight reset positions, sparse masks, full queues and faults",
        "original_layers": {"cases": 14, "no_stall_cycles": 3331, "dw": 2015, "pw": 1316},
        "representative_chain": {"tasks": 1040, "outputs": 2544, "mismatches": 0, "parameter_origin": "TEST_NOT_QAT"},
        "strict_shell_tb": {"delivery_ready": gate["delivery_ready"], "issues": gate["delivery_issues_by_rule"]},
        "syn5025": "NOT_CLOSED: absent in fully driven minimal probe; CNN objects remain unlocalized",
        "specs": "Canonical probe generated; portless testbench write-spec rejected, manual companions explicitly noncanonical",
        "remaining": ["actual runtime-coefficient layer adapter and physical top", "SYN-5025 endpoint localization",
                      "PW turnover", "vendor DDR write visibility", "full network/resource/timing/5FPS", "QAT and independent accuracy"],
        "changed": "new validation runner, testbenches, vectors, probe and reports only",
        "kernel_sources_modified": False, "training": "NOT_RUN", "bitgen": "NOT_RUN", "board": "NOT_RUN"})
    check()
    publish("evidence_hashes.json", {str(path.relative_to(ROOT)): sha(path) for path in
            [ROOT / "run_stage.py", ROOT / "representative_vectors.py", ROOT / "write_evidence.py",
             ROOT / "tb_dynamic_shell_vectors.v", ROOT / "tb_representative_chain.v",
             ROOT / "representative.txt", ROOT / "representative_manifest.json"]})
    print("EVIDENCE_PUBLISHED")


if __name__ == "__main__":
    main()
