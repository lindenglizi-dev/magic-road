"""功能闭合后占用一次诊断综合；任何失败保留且不重试。"""
import argparse
from pathlib import Path
import re
import shutil
import subprocess
import time

import run

ROOT = Path(__file__).resolve().parent
TD = Path("E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/bin/td_commands_prompt.exe")
TEMPLATE = ROOT.parent / "reports/pw48_tile_20261015/physical_attempt2/project_input_reconstructed.al"
TOP = "road_narrow_feature_top"


def execute(candidate):
    target = run.check(candidate)
    ready = run.read(ROOT / "functional_ready.json")
    assert ready["candidate"] == candidate and ready["all_required_cases_passed"]
    assert ready["unexplained_high_confidence_semantic_risks"] == []
    assert ready["IO_bits"] <= 64
    run.verify(ready["evidence_sha256"])
    folder = ROOT / "synthesis"
    folder.mkdir(exist_ok=False)
    (folder / "sources").mkdir()
    sources = [path for group in ("rtl", "core", "reused") for path in (target / group).glob("*.v")]
    assert len(sources) == 10 and len({path.name for path in sources}) == len(sources)
    copied = []
    for path in sources:
        destination = folder / "sources" / path.name
        shutil.copy2(path, destination)
        copied.append(destination)
    project = TEMPLATE.read_text(encoding="utf-8").replace(TEMPLATE.parent.as_posix(), folder.as_posix())
    project = project.replace("road_pw_validation_top", TOP)
    files = "\n".join(f'<File Path="{path.as_posix()}"><FileInfo><Attr Name="UsedInSyn" Val="true"/><Attr Name="UsedInP&R" Val="true"/><Attr Name="BelongTo" Val="design_1"/><Attr Name="CompileOrder" Val="{index}"/></FileInfo></File>'
                      for index, path in enumerate(copied, 1))
    project, replacements = re.subn(r"<Verilog>.*?</Verilog>", "<Verilog>\n" + files + "\n</Verilog>", project, flags=re.S)
    assert replacements == 1
    (folder / (TOP + ".al")).write_text(project, encoding="utf-8")
    (folder / "project_input.al").write_text(project, encoding="utf-8")
    shutil.copy2(ROOT / "build.tcl", folder / "build.tcl")
    shutil.copy2(ROOT / "diagnostic_clock.sdc", folder / "frontend.sdc")
    script = (folder / "build.tcl").read_text(encoding="utf-8")
    assert not re.search(r"^\s*(?:bitgen|place|route|set_false_path|set_multicycle_path)\b", script, re.M)
    inputs = {str(path): run.digest(path) for path in [*copied, folder / "project_input.al", folder / "build.tcl",
              folder / "frontend.sdc", ROOT / "functional_ready.json", Path(__file__), TD, TEMPLATE]}
    run.save(folder / "input_manifest.json", inputs)
    run.save(folder / "status.json", dict(status="RUNNING_SINGLE_DIAGNOSTIC_SYNTHESIS", place_route=False,
             bitstream=False, actual_model_ROM=False, production_delivery_ready=False))
    started = time.monotonic()
    try:
        result = subprocess.run([str(TD), "build.tcl"], cwd=folder, capture_output=True, text=True,
                                encoding="utf-8", errors="replace", timeout=600)
        output = result.stdout + result.stderr
        (folder / "launcher.log").write_text(output, encoding="utf-8")
        run.save(folder / "command.json", dict(argv=[str(TD), "build.tcl"], cwd=str(folder),
            native_returncode=result.returncode, log_sha256=run.digest(folder / "launcher.log"), executable_sha256=run.digest(TD)))
        run.verify(inputs)
        run.check(candidate)
        complete = result.returncode == 0 and "NARROW_FEATURE_DIAGNOSTIC_SYNTHESIS_COMPLETE" in output
        complete = complete and all((folder / filename).is_file() for filename in ("gate.area", "gate.qor", "gate_netlist.v"))
        run.save(folder / "status.json", dict(status="SYNTHESIS_COMPLETE_NOT_PNR" if complete else "SYNTHESIS_FAILED_NO_RETRY",
            seconds=time.monotonic() - started, native_returncode=result.returncode, input_hashes_unchanged=True,
            actual_model_ROM=False, physical_timing=False, place_route=False, bitstream=False, board=False,
            whole_network_resource=False, production_delivery_ready=False))
        assert complete, "slot failed; do not retry"
        print("NARROW_DIAGNOSTIC_SYNTHESIS_COMPLETE", flush=True)
    except BaseException as error:
        run.save(folder / "failure.json", dict(error=repr(error), seconds=time.monotonic() - started, automatic_retry=False))
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", default="frozen")
    execute(parser.parse_args().candidate)
