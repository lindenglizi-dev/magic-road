"""Canonical companions for changed design modules; no inferred timing claims."""
import json
from pathlib import Path
import shutil
import sys

from run_candidate import ROOT, BASE, SKILL, fresh, command

sys.path.insert(0, str(SKILL))
from scripts.python.quality.formatter_backend import VerilogFormatterEngine


def main():
    work = fresh("s")
    engine = VerilogFormatterEngine({"formatter": {"indent_style": "tab", "indent_size": 4}})
    waveform = {"signal": [{"name": "clk", "wave": "p........."},
                 {"name": "parameters_complete", "wave": "0...1....."},
                 {"name": "start", "wave": "01..010..."},
                 {"name": "busy", "wave": "0.....1..."},
                 {"name": "output_valid", "wave": "0.......1."},
                 {"name": "output_ready", "wave": "1.......01"}]}
    entry = f"import sys;sys.path.insert(0,{str(SKILL)!r});from scripts.python.workflow.cli import main;raise SystemExit(main())"
    targets = [ROOT / "rtl/road_down2_dynamic_adapter.v", ROOT / "rtl/down2_dynamic_tile_runner.v",
               ROOT / "physical/layer_shell/road_dynamic_overlap_low_io_top.v"]
    mirror = work / "sources"
    mirror.mkdir()
    for source in targets:
        staged_source = mirror / source.name
        shutil.copyfile(source, staged_source)
        name, _, ports, _ = engine._parse_module(source.read_text(encoding="utf-8"))
        def width(text):
            if not text:
                return 1
            high, low = text.strip("[]").split(":")
            return abs(int(high) - int(low)) + 1
        declared = [{"name": port.name, "direction": port.direction, "width": width(port.width),
                     "role": port.name, "description": port.comment or port.name, "clock_domain": "i_clk"}
                    for port in ports]
        module = {"name": name, "feature": "r", "rtl_path": source.name,
          "description": "Independent down2 runtime coefficient candidate; TEST scales, not deployed QAT.",
          "interfaces": {"protocol": "discrete", "ports": declared}, "parameters": [],
          "clock": {"name": "i_clk", "edge": "posedge", "frequency_hz": 100000000},
          "reset": {"name": "i_rstn", "active": "low", "synchronous": False,
                    "values": "Cancel all old work; invalidate parameters and reload 1024 SiLU entries. Shell releases after two clock edges."},
          "behavior": ["Reuse frozen MAC, RNE and SiLU. Kernel interfaces, arithmetic and II are unchanged.",
              "Load kind6 addresses0..39: nonnegative INT32 pre multipliers; DW0..15 then PW16..39.",
              "Load kind7 addresses0..39: shifts0..62; 40/41: DW/PW post multiplier; 42/43: DW/PW post shift.",
              "Sequential writes or address-zero restart only. Both complete banks required before runner start.",
              "Parameters writable only while idle; accepted postprocess batches capture coefficients with metadata.",
              "Real 9x9x16 halo feeds DW3x3/s2 then 4x4x16 PW16to24. Export384 INT8 items.",
              "Shell keeps38 external bits; existing16-bit load descriptor accepts kinds6/7 only in this candidate."],
          "constraints": ["No production edits, training, bitgen, board, Flash or additional timing exceptions.",
                          "Diagnostic input/output delays are not a real external-device timing contract."],
          "corner_cases": ["No partial parameter publication; negative multiplier and shift63 are rejected.",
                           "Output ownership under backpressure; reset cancels data and invalidates parameter banks."],
          "verification_cases": ["Fixed-profile byte equivalence and28 layer scenarios using actual PH1P/common models.",
                                 "Runtime nonpower-of-two scales and three tile locations; all intermediate values checked.",
                                 "Real narrow-port exports and gate netlist comparison; static and physical failures remain separate."],
          "timing_diagrams": [{"id": "load_then_start", "title": "Incomplete load cannot start",
                "scenario": "load_then_start", "description": "Protocol schematic only; busy duration is compressed, not literal measured latency.",
                "wavejson": waveform}]}
        contract = work / (name + ".json")
        contract.write_text(json.dumps({"modules": [module]}, indent=2), encoding="utf-8")
        command([sys.executable, "-B", "-X", "utf8", "-c", entry, "write-spec", "--spec", contract,
                 "--out-dir", work / "g", "--source", staged_source, "--no-state"], ROOT,
                str(work.relative_to(ROOT) / name), allowed=(0, 1, 2))
        companion = work / "g/spec/r" / (name + "_spec.md")
        assert companion.exists(), companion
        shutil.copyfile(companion, source.with_name(name + "_spec.md"))
        waveforms = companion.parent / "waveforms"
        shutil.copytree(waveforms, source.parent / "waveforms", dirs_exist_ok=True)
        print("SPEC_PASS", name, "ports", len(ports), "bits", sum(port["width"] for port in declared))
    for name in ("tb_down2_dynamic_overlap", "tb_runtime_layer_shell"):
        # Preserve the known canonical contract limitation; do not invent TB ports.
        tb_module = dict(module, name=name, rtl_path=name + ".v",
                         interfaces={"protocol": "discrete", "ports": []})
        contract = work / (name + ".json")
        contract.write_text(json.dumps({"modules": [tb_module]}, indent=2), encoding="utf-8")
        result = command([sys.executable, "-B", "-X", "utf8", "-c", entry, "write-spec", "--spec", contract,
                 "--out-dir", work / "g", "--source", ROOT / "tests/layer" / (name + ".v"), "--no-state"], ROOT,
                 str(work.relative_to(ROOT) / name), allowed=(0, 1, 2))
        assert "ports must be non-empty" in result, result
        print("TB_CANONICAL_REJECTED_PORTLESS", name)


if __name__ == "__main__":
    main()
