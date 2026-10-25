"""从已验证综合数据库进行隔离布局布线，复用既有TD时序解析；不生成位流。"""
import argparse
from datetime import datetime
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

import run_csp_first_probe as base

TD = Path("E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/bin/td_commands_prompt.exe")
PARSER = base.BASE / "table_command_isolation_20261013/physical_report.py"
REPORT_TEMPLATE = base.BASE / "pw48_tile_20261015/physical_attempt2/build.tcl"


def main(out, name):
    binding = json.loads((out / "input_binding.json").read_text(encoding="utf-8"))
    base.check_hashes(binding["original_sha256"])
    base.check_hashes(binding["staged_sha256"])
    synth = out / "synthesis"
    assert json.loads((synth / "status.json").read_text(encoding="utf-8"))["qualified_synthesis"]
    synth_inputs = json.loads((synth / "input_manifest.json").read_text(encoding="utf-8"))
    base.check_hashes(synth_inputs)
    work = out / name
    work.mkdir(exist_ok=False)
    shutil.copy2(synth / "gate.db",work / "source_gate.db")
    shutil.copy2(synth / "frontend.sdc",work / "frontend.sdc")
    project = (synth / "project_input.al").read_text(encoding="utf-8").replace(synth.as_posix(),work.as_posix())
    (work / "sources").mkdir()
    for source in (synth / "sources").iterdir():
        if source.is_file():
            shutil.copy2(source,work / "sources" / source.name)
    (work / "road_csp_tile_integrated.al").write_text(project,encoding="utf-8")
    (work / "project_input.al").write_text(project,encoding="utf-8")
    # 复用已执行过的布局设置和完整报告命令，只替换独立顶层名称。
    template = REPORT_TEMPLATE.read_text(encoding="utf-8")
    placement = template[template.index("set_param place effort high"):template.index("puts \"REPORT_COMPLETION_DONE\"")]
    placement = placement.replace("road_pw_validation_top","road_csp_tile_integrated")
    script = """import_device ph1_35p.db -package PH1P35MDG324 -speed 3
open_project road_csp_tile_integrated.al -single_run
import_db source_gate.db
read_sdc frontend.sdc
if {[llength [get_clocks probe_clk]] != 1} {error "Expected one100MHzprobe clock"}
update_timing
""" + placement + """
puts "CSP_TILE_PHYSICAL_REPORTS_COMPLETE"
close_project
exit
"""
    assert not re.search(r"^\s*(bitgen|set_false_path|set_multicycle_path|set_max_delay|set_min_delay)\b",script,re.M)
    assert (work / "frontend.sdc").read_bytes() == (synth / "frontend.sdc").read_bytes()
    (work / "build.tcl").write_text(script,encoding="ascii")
    frozen = {str(p):base.digest(p) for p in [work / "source_gate.db",work / "frontend.sdc",work / "project_input.al",
        work / "build.tcl",TD,PARSER,REPORT_TEMPLATE,Path(__file__),*sorted((work / "sources").iterdir())]}
    base.save(work / "input_manifest.json",frozen)
    base.save(work / "status.json",dict(status="RUNNING_PLACE_AND_ROUTE",started=datetime.now().astimezone().isoformat(),
        bitstream_or_board=False,production_delivery_ready=False))
    argv = [str(TD),"build.tcl"]
    started = time.monotonic()
    try:
        result = subprocess.run(argv,cwd=work,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,
            encoding="utf-8",errors="replace",timeout=360)
        (work / "launcher.log").write_text(result.stdout,encoding="utf-8")
        base.save(work / "command.json",dict(argv=argv,cwd=str(work),exit_code=result.returncode,executable_sha256=base.digest(TD)))
        base.check_hashes(frozen)
        base.check_hashes(binding["original_sha256"])
        base.check_hashes(binding["staged_sha256"])
        complete = result.returncode == 0 and "CSP_TILE_PHYSICAL_REPORTS_COMPLETE" in result.stdout
        assert complete and (work / "pr.db").is_file(),"TD did not complete route/reports"
        parser_spec = importlib.util.spec_from_file_location("csp_existing_physical_parser",PARSER)
        parser = importlib.util.module_from_spec(parser_spec)
        sys.modules[parser_spec.name] = parser
        parser_spec.loader.exec_module(parser)
        reports, failures = {}, []
        for report in ("all_endpoints","all_endpoints_include_ignored","internal_all_checks","external_reset_entry",
                       "dsp_outputs_all_checks","dsp_inputs_all_checks","eram_outputs_all_checks","eram_inputs_all_checks"):
            stats, failed = parser.read_timing(work / f"{report}.timing",keep_negative=True)
            reports[report] = stats
            if report == "all_endpoints_include_ignored":
                failures = failed
        area = parser.parse_area((work / "frontend_route.area").read_text(encoding="utf-8"))
        assert area["dsp"]["used"] == 30 and area["eram"]["used"] == 1,"arithmetic/ROM mapping changed"
        assert area["io"]["used"] == 127,"top I/O changed"
        assert all(reports["internal_all_checks"]["checks"].get(check,{}).get("reported_paths",0) > 0
                   for check in ("setup","hold")),"missing actual internal timing checks"
        internal_failures = [row for row in failures if row["scope"] == "internal"]
        core_pass = not internal_failures
        blockers = re.findall(r"(?:HDL-5314 WARNING[^\r\n]*|TMR-2509 CRITICAL-WARNING[^\r\n]*|TMR-2507 CRITICAL-WARNING[^\r\n]*)",result.stdout)
        summary = dict(device="PH1P35MDG324-3",clock_mhz=100,resources=area,reports=reports,
            failed_endpoints=failures,internal_failed_endpoints=internal_failures,internal_timing_pass=core_pass,
            mapping_blockers=blockers,source_gate_sha256=base.digest(work / "source_gate.db"),
            routed_database_sha256=base.digest(work / "pr.db"),
            limits="standalone first residual tile; external I/O delays and board pinout unqualified; no DDR/video/full graph",
            production_delivery_ready=False)
        base.save(work / "physical_summary.json",summary)
        base.save(work / "failed_endpoint_inventory.json",failures)
        base.save(work / "status.json",dict(status="ROUTED_INTERNAL_PASS_EXTERNAL_OPEN" if core_pass else "ROUTED_INTERNAL_TIMING_FAILED",
            seconds=time.monotonic()-started,resources=area,internal_failed_endpoints=len(internal_failures),
            original_and_staged_hashes_unchanged=True,clock_constraints_unchanged=True,
            external_timing_qualified=False,mapping_blockers=blockers,bitstream_or_board=False,production_delivery_ready=False))
        print("ROUTED_INTERNAL_PASS" if core_pass else "ROUTED_INTERNAL_TIMING_FAILED",area,len(internal_failures),flush=True)
    except BaseException as error:
        base.save(work / "status.json",dict(status="PHYSICAL_FAILED_NO_RETRY",error=repr(error),
            seconds=time.monotonic()-started,bitstream_or_board=False,production_delivery_ready=False))
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out",type=Path,default=base.BASE / "csp_tile_integrated_20261015_v2")
    parser.add_argument("--name",default="physical")
    args = parser.parse_args()
    if not re.fullmatch(r"physical(?:_attempt[1-9][0-9]*)?",args.name):
        raise SystemExit("name must select one fresh isolated physical directory")
    main(args.out.resolve(),args.name)
