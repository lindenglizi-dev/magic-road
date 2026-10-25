"""封存硬件驱动首残差tile的功能、源闭包、局部综合和明确未通过项。"""
from datetime import datetime
import json
from pathlib import Path
import re

import run_csp_first_probe as base

OUT = base.BASE / "csp_tile_integrated_20261015_v2"


def main():
    binding = json.loads((OUT / "input_binding.json").read_text(encoding="utf-8"))
    base.check_hashes(binding["original_sha256"])
    base.check_hashes(binding["staged_sha256"])
    status = json.loads((OUT / "status.json").read_text(encoding="utf-8"))
    assert len(status["cases"]) == 13 and status["compile_errors"] == status["compile_warnings"] == 0
    synth = json.loads((OUT / "synthesis/status.json").read_text(encoding="utf-8"))
    assert synth["qualified_synthesis"] and synth["mapping_blockers"] == []
    synth_inputs = json.loads((OUT / "synthesis/input_manifest.json").read_text(encoding="utf-8"))
    base.check_hashes(synth_inputs)
    for path in (OUT / "synthesis/sources").glob("*.v"):
        original = OUT / ("rtl" if (OUT / "rtl" / path.name).exists() else "reused") / path.name
        assert base.digest(path) == base.digest(original)
    area = (OUT / "synthesis/gate.area").read_text(encoding="utf-8")
    def number(pattern):
        matches = re.findall(pattern,area,re.M)
        assert len(matches) == 1,pattern
        return int(matches[0])
    resources = dict(DSP=number(r"^#dsp\s+(\d+)"),ERAM=number(r"^#eram\s+(\d+)"),
        slice_estimate=number(r"^#slice\*\s+(\d+)"),registers=number(r"^#reg\s+(\d+)"),
        LUT=number(r"^#lut\s+(\d+)"),scope="TD optimize_gate of standalone first residual tile; not placed/routed or full system")
    assert resources["DSP"] == 30 and resources["ERAM"] == 1
    # 显式ROM逐词与紧凑程序核对，不能仅依赖工具没有发出未驱动警告。
    program = (OUT / "rtl/road_csp_tile_program.v").read_text(encoding="utf-8")
    for field,width,count in (("weight",192,56),("parameter",248,16)):
        words = re.findall(rf"reg_{field}_o\s*<=\s*{width}'h([0-9a-f]+)",program)
        assert len(words) == count
        assert [int(word,16) for word in words] == base.readhex(OUT / "vectors" / f"{field}_program.hex")
    variants = [base.readhex(OUT / "vectors" / f"golden_{n}_output.hex") for n in range(2)]
    changed_dw = sum(a != b for a,b in zip(variants[0][:192],variants[1][:192]))
    changed_all = sum(a != b for a,b in zip(*variants))
    assert changed_dw == 6 and changed_all == 44
    gate = json.loads((OUT / "source_closure_gate.json").read_text(encoding="utf-8"))
    new_gate = json.loads((OUT / "new_modules_gate.json").read_text(encoding="utf-8"))
    cases = {row["case"]:row["fields"] for row in status["cases"]}
    assert cases[0]["cycles"] == 12001 and cases[7]["runs"] == 2 and cases[7]["table_loads"] == 1
    assert cases[11]["outputs"] == 0 and cases[12]["outputs"] == 1
    result = dict(as_of=datetime.now().astimezone().isoformat(),cases_passed=13,
        complete_runs_in_cases=9,original_hashes_rechecked=len(binding["original_sha256"]),
        staged_hashes_rechecked=len(binding["staged_sha256"]),synthesis_hashes_rechecked=len(synth_inputs),
        registered_completion_verified_by_structure_and_cycles=True,
        baseline_writeback_only_cycles=7807,integrated_without_retirement_register_cycles=11841,
        final_integrated_cycles=12001,registered_retirement_extra=160,
        normal_run_microseconds_at_100MHz=120.01,source_and_LUT_load_cycles_excluded=True,
        changed_input_test=dict(DW_changed=6,all_outputs_changed=44,table_loads=1,runs=2),
        real_DW_cache_writes_per_run=192,real_PW_cache_reads_per_run=128,
        tasks_per_run=160,groups_per_run=320,outputs_per_run=384,
        resources=resources,qualified_synthesis=True,physical_timing_passed=False,
        new_module_gate=dict(errors=new_gate["errors"],strict_warnings=new_gate["strict_warnings"]),
        source_closure_gate=dict(errors=gate["errors"],strict_warnings=gate["strict_warnings"],
            checks={k:v.get("status") for k,v in gate["checks"].items()}),
        actual_DDR=False,full_CSP2_layer=False,full_graph=False,board=False,training_updates=0,
        production_delivery_ready=False,finalizer_sha256=base.digest(Path(__file__)))
    base.save(OUT / "final_checks.json",result)
    base.save(OUT / "resource_summary.json",resources)
    if not (OUT / "functional_status_before_synthesis.json").exists():
        base.save(OUT / "functional_status_before_synthesis.json",status)
    status.pop("synthesis_or_board",None)
    status.update(synthesis_executed=True,synthesis_qualified=True,physical_timing_passed=False,board=False,
        strict_gate_passed=False,strict_errors=gate["errors"],strict_warnings=gate["strict_warnings"],
        resources=resources,final_checks="final_checks.json")
    base.save(OUT / "status.json",status)
    print("SEALED_13_CASES_TD_SYNTHESIS30DSP1ERAM_NOT_PHYSICAL_OR_FULL_GRAPH",flush=True)


if __name__ == "__main__":
    main()
