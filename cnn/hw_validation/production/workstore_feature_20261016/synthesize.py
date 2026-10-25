"""获排期的一次诊断综合；必须先完成同向量功能和语义风险核查。"""
import argparse
from pathlib import Path
import re
import shutil
import subprocess
import time

import run

ROOT = Path(__file__).resolve().parent
TD = Path("E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/bin/td_commands_prompt.exe")
TEMPLATE = ROOT.parent/"reports/pw48_tile_20261015/physical_attempt2/project_input_reconstructed.al"


def main(candidate):
    target = ROOT/candidate
    run.check_binding(target)
    closure = run.read(ROOT/"functional_ready.json")
    assert closure["candidate"] == candidate and closure["all_required_cases_passed"]
    assert closure["unexplained_high_confidence_semantic_risks"] == []
    run.verify(closure["evidence"])
    assert run.digest(ROOT/"delivery_manifest.json") == closure["delivery_manifest_sha256"]
    run.verify(run.read(ROOT/"delivery_manifest.json")["artifacts_sha256"])
    folder = ROOT/"synthesis"
    folder.mkdir(exist_ok=False)  # 一次slot，不覆盖失败，不自动再跑。
    (folder/"sources").mkdir()
    sources = [*sorted((target/"rtl").glob("*.v")), *sorted((target/"reused").glob("*.v"))]
    assert {path.name for path in sources} == {
        "road_feature_workstore.v", "road_feature_blocks_client.v", "road_feature_workstore_top.v",
        *[module+".v" for module in run.CORES]}
    copied = []
    for path in sources:
        destination = folder/"sources"/path.name
        shutil.copy2(path, destination)
        copied.append(destination)
    project = TEMPLATE.read_text(encoding="utf-8")
    project = project.replace(TEMPLATE.parent.as_posix(), folder.as_posix()).replace("road_pw_validation_top", "road_feature_workstore_top")
    files = "\n".join(f'<File Path="{p.as_posix()}"><FileInfo><Attr Name="UsedInSyn" Val="true"/><Attr Name="UsedInP&R" Val="true"/><Attr Name="BelongTo" Val="design_1"/><Attr Name="CompileOrder" Val="{n}"/></FileInfo></File>'
                       for n, p in enumerate(copied, 1))
    project, replaced = re.subn(r"<Verilog>.*?</Verilog>", "<Verilog>\n"+files+"\n</Verilog>", project, flags=re.S)
    assert replaced == 1
    (folder/"road_feature_workstore_top.al").write_text(project, encoding="utf-8")
    (folder/"project_input.al").write_text(project, encoding="utf-8")
    shutil.copy2(ROOT/"synthesis_plan.tcl", folder/"build.tcl")
    shutil.copy2(ROOT/"diagnostic_clock.sdc", folder/"frontend.sdc")
    script = (folder/"build.tcl").read_text(encoding="utf-8")
    assert not re.search(r"^\s*(?:bitgen|place|route|set_false_path|set_multicycle_path)\b", script, re.M)
    frozen = {str(path): run.digest(path) for path in [*copied, folder/"build.tcl", folder/"frontend.sdc",
        folder/"project_input.al", ROOT/"functional_ready.json", Path(__file__), TD, TEMPLATE]}
    run.save(folder/"input_manifest.json", frozen)
    run.save(folder/"status.json", dict(status="RUNNING_ONE_DIAGNOSTIC_SYNTHESIS", candidate=candidate,
        place_route=False, bitstream=False, board=False, whole_network_resource=False))
    argv, started = [str(TD), "build.tcl"], time.monotonic()
    try:
        result = subprocess.run(argv, cwd=folder, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=600)
        output = result.stdout+result.stderr
        (folder/"launcher.log").write_text(output, encoding="utf-8")
        run.save(folder/"command.json", dict(argv=argv, cwd=str(folder), native_returncode=result.returncode,
            executable_sha256=run.digest(TD), log_sha256=run.digest(folder/"launcher.log")))
        run.verify(frozen)
        run.check_binding(target)
        complete = result.returncode == 0 and "FEATURE_WORKSTORE_DIAGNOSTIC_SYNTHESIS_COMPLETE" in output
        complete = complete and all((folder/name).is_file() for name in ("gate.qor", "gate.area", "gate_netlist.v"))
        run.save(folder/"status.json", dict(status="DIAGNOSTIC_SYNTHESIS_COMPLETED_NOT_PNR" if complete else "SYNTHESIS_FAILED_NO_RETRY",
            seconds=time.monotonic()-started, native_returncode=result.returncode, hashes_unchanged=True,
            actual_ERAM_count="must inspect gate.area/netlist", physical_timing=False, place_route=False,
            bitstream=False, board=False, whole_network_resource=False, production_delivery_ready=False))
        print("DIAGNOSTIC_SYNTHESIS_COMPLETE" if complete else "SYNTHESIS_FAILED_NO_RETRY", flush=True)
        assert complete, "diagnostic slot failed; preserve and do not retry"
    except BaseException as error:
        run.save(folder/"failure.json", dict(error=repr(error), seconds=time.monotonic()-started, automatic_retry=False))
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", default="frozen")
    args = parser.parse_args()
    main(args.candidate)
