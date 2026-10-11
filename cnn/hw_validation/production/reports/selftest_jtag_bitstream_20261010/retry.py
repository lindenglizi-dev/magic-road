"""保留首次失败；不重复读SDC，使用数据库自带的冻结约束。"""
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
import run


if __name__ == "__main__":
    run.verify("attempt2_before")
    work = run.ROOT / "generation_attempt2"
    assert not work.exists()
    work.mkdir()
    for name in ("pr.db", "board.adc", "board.sdc", "selftest_program.hex"):
        shutil.copyfile(run.BASE / "physical" / name, work / name)
    shutil.copyfile(run.ROOT / "bitgen_db_only.tcl", work / "bitgen.tcl")
    project = ET.fromstring((run.BASE / "physical/road_board_selftest_top.al").read_text(encoding="utf-8").replace("UsedInP&R", "UsedInP&amp;R"))
    project.set("Path", work.as_posix())
    for item in project.findall(".//Source_Files//File"):
        source = run.Path(item.attrib["Path"])
        item.set("Path", (source if source.is_absolute() else (run.BASE / "physical" / source).resolve()).as_posix())
    ET.ElementTree(project).write(work / "road_board_selftest_top.al", encoding="utf-8", xml_declaration=True)
    run.save("attempt2_inputs.json", {str(p): run.digest(p) for p in [*work.iterdir(), run.ROOT / "retry.py", run.TD] if p.is_file()})
    try:
        with (work / "td.log").open("w", encoding="utf-8") as stream:
            result = subprocess.run([str(run.TD), "bitgen.tcl"], cwd=work, stdout=stream, stderr=subprocess.STDOUT, timeout=900, check=False)
        run.save("attempt2_tool_result.json", {"command": [str(run.TD), "bitgen.tcl"], "cwd": str(work), "returncode": result.returncode, "board_access": False, "flash_access": False})
        assert result.returncode == 0
        assert (work / "imported.ts").read_text() == (run.BASE / "physical/route.ts").read_text()
        report = (work / "imported.timing").read_text(encoding="utf-8")
        assert "STA coverage        : 99.98%" in report
        spec = importlib.util.spec_from_file_location("old_paths", run.OLD / "evidence.py")
        parser = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(parser)
        paths = parser.paths(work / "imported.timing")
        old_paths = json.loads((run.BASE / "timing_checks.json").read_text(encoding="utf-8"))["all_endpoints.timing"]
        assert paths == old_paths, "导入数据库的全量时序端点、角点或余量不同"
        area = (work / "imported.area").read_text(encoding="utf-8")
        assert re.search(r"i_rstn\s+INPUT\s+C7\s+LVCMOS33", area)
        for name, value in (("slice", 9691), ("dsp", 30), ("eram", 38)):
            assert int(re.search(r"^#" + name + r"\s+(\d+)", area, re.M)[1]) == value
        assert run.digest(work / "pr.db") == run.digest(run.BASE / "physical/pr.db")
        bit = work / "RoadYOLO_HX1P35A_KEY4_SELFTEST.bit"
        assert bit.is_file() and bit.stat().st_size > 1024
        run.save("bitstream_receipt.json", {"path": str(bit), "bytes": bit.stat().st_size, "sha256": run.digest(bit), "source_pr_db_sha256": run.digest(work / "pr.db"), "device": "PH1P35MDG324", "speed": "3", "board": "HX1P35A V1.0", "reset": "KEY4/C7 active-low", "scope": "three-case autonomous DW/PW selftest, not full CNN", "source_user_marking": "52509006550011 / 2514 / I3, user transcription", "full_imported_timing_matches_frozen": True, "board_tested": False, "flash_written": False, "strict_gates_closed": False})
        run.save("attempt2_timing_checks.json", paths)
        print("BITGEN_VERIFIED_PASS", bit.stat().st_size, run.digest(bit), flush=True)
    finally:
        run.verify("attempt2_after")
