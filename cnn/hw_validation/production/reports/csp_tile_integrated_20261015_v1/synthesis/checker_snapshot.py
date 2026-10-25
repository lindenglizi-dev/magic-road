"""联合tile的隔离TD综合检查；不生成位流、不改生产约束或操作板卡。"""
import json
from pathlib import Path
import re
import shutil
import subprocess
import time

import run_csp_first_probe as base

OUT = base.BASE / "csp_tile_integrated_20261015_v1"
TD = Path("E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/bin/td_commands_prompt.exe")
TEMPLATE = base.BASE / "pw48_tile_20261015/physical_attempt2/project_input_reconstructed.al"


def main():
    status = json.loads((OUT / "status.json").read_text(encoding="utf-8"))
    assert status["status"] == "PASS_HARDWARE_DRIVEN_FIRST_RESIDUAL_TILE_NOT_DELIVERY_READY"
    binding = json.loads((OUT / "input_binding.json").read_text(encoding="utf-8"))
    base.check_hashes(binding["original_sha256"])
    base.check_hashes(binding["staged_sha256"])
    work = OUT / "synthesis"
    work.mkdir(exist_ok=False)
    (work / "sources").mkdir()
    sources = []
    for source in [*sorted((OUT / "rtl").glob("*.v")), *sorted((OUT / "reused").glob("*.v"))]:
        target = work / "sources" / source.name
        shutil.copy2(source, target)
        sources.append(target)
    for name in ("weight_program.hex", "parameter_program.hex"):
        shutil.copy2(OUT / "vectors" / name, work / name)
        shutil.copy2(OUT / "vectors" / name, work / "sources" / name)
    project = TEMPLATE.read_text(encoding="utf-8")
    project = project.replace((TEMPLATE.parent).as_posix(), work.as_posix()).replace("road_pw_validation_top", "road_csp_tile_integrated")
    records = "\n".join(f'<File Path="{p.as_posix()}"><FileInfo><Attr Name="UsedInSyn" Val="true"/><Attr Name="UsedInP&R" Val="true"/><Attr Name="BelongTo" Val="design_1"/><Attr Name="CompileOrder" Val="{i}"/></FileInfo></File>' for i,p in enumerate(sources,1))
    project = re.sub(r"<Verilog>.*?</Verilog>","<Verilog>\n"+records+"\n</Verilog>",project,flags=re.S)
    (work / "road_csp_tile_integrated.al").write_text(project,encoding="utf-8")
    # TD可能规范化工程XML，初始投影独立保留。
    (work / "project_input.al").write_text(project,encoding="utf-8")
    (work / "frontend.sdc").write_text("create_clock -name probe_clk -period 10.000 -waveform {0.000 5.000} [get_ports {i_clk}]\n",encoding="ascii")
    script = """import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project road_csp_tile_integrated.al -single_run
elaborate -top road_csp_tile_integrated
optimize_rtl
report_area -verbose -file rtl.area
read_sdc frontend.sdc
optimize_gate
legalize_phy_inst
export_db gate.db
write_verilog gate_netlist.v -top road_csp_tile_integrated
report_area -verbose -io_info -file gate.area
report_qor -step gate -file gate.qor
puts "CSP_TILE_SYNTHESIS_COMPLETE"
close_project
exit
"""
    assert not re.search(r"^\s*(bitgen|place|route|set_false_path|set_multicycle_path)\b",script,re.M)
    (work / "build.tcl").write_text(script,encoding="ascii")
    frozen = {str(p):base.digest(p) for p in [*sources,work / "build.tcl",work / "frontend.sdc",work / "project_input.al",
        work / "weight_program.hex",work / "parameter_program.hex",TD,TEMPLATE,Path(__file__)]}
    base.save(work / "input_manifest.json",frozen)
    argv = [str(TD),"build.tcl"]
    started = time.monotonic()
    base.save(work / "status.json",dict(status="RUNNING_SYNTHESIS_ONLY",bitstream_or_board=False))
    result = subprocess.run(argv,cwd=work,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,
        encoding="utf-8",errors="replace",timeout=240)
    (work / "launcher.log").write_text(result.stdout,encoding="utf-8")
    base.save(work / "command.json",dict(argv=argv,cwd=str(work),exit_code=result.returncode,executable_sha256=base.digest(TD)))
    base.check_hashes(frozen)
    base.check_hashes(binding["original_sha256"])
    base.check_hashes(binding["staged_sha256"])
    complete = result.returncode == 0 and "CSP_TILE_SYNTHESIS_COMPLETE" in result.stdout and (work / "gate.qor").is_file()
    base.save(work / "status.json",dict(status="SYNTHESIS_COMPLETED_NOT_PLACED_OR_ROUTED" if complete else "SYNTHESIS_FAILED_NO_RETRY",
        seconds=time.monotonic()-started,exit_code=result.returncode,input_hashes_unchanged=True,
        bitstream_or_board=False,physical_timing_passed=False,whole_network_resource=False,
        missing_IO_delays="only100MHzclock constraint; no peripheral timing claim",production_delivery_ready=False))
    print("SYNTHESIS_COMPLETED" if complete else "SYNTHESIS_FAILED",flush=True)
    if not complete:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
