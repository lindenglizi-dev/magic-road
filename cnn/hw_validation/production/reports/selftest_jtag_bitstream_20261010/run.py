"""从冻结C7布局数据库生成临时JTAG自检文件，不操作下载器。"""
import ast
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / "board_key4_c7_20261010"
OLD = ROOT.parent / "board_selftest_20261010"
TD = Path("E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/bin/td_commands_prompt.exe")
SKILL = Path("C:/Users/lenovo/.codex/skills/readable-verilog-generator")
WORK = ROOT / "generation"


def digest(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def save(name, value):
    target = ROOT / name
    target.resolve().relative_to(ROOT)
    assert not target.exists(), target
    target.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def verify(label):
    frozen = {}
    for manifest in (OLD / "frozen.json", OLD / "evidence_attempt4/candidate_final_freeze.json", BASE / "final_freeze.json", BASE / "outputs.json"):
        entries = json.loads(manifest.read_text(encoding="utf-8"))
        for path, expected in entries.items():
            assert path not in frozen or frozen[path] == expected, path
            frozen[path] = expected
    changed = [p for p, sha in frozen.items() if not Path(p).is_file() or digest(p) != sha]
    save(label + ".json", {"checked": len(frozen), "changed": changed})
    assert not changed, changed


def main():
    assert not WORK.exists(), "禁止覆盖已有生成尝试"
    ast.parse((ROOT / "run.py").read_text(encoding="utf-8"))
    verify("frozen_before")
    with (ROOT / "dependencies.log").open("w", encoding="utf-8") as stream:
        subprocess.run([sys.executable, "-B", SKILL / "scripts/python/toolchain/manage_skill_dependencies.py", "check", "--settings", SKILL / "config/defaults.json", "--state-path", ROOT / "dependency_state.json"], cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT, timeout=90, check=False)
    log = (ROOT / "dependencies.log").read_text(encoding="utf-8")
    assert json.loads(log[log.index("{"):])["required_ok"]
    WORK.mkdir()
    for name in ("pr.db", "board.sdc", "board.adc", "selftest_program.hex"):
        shutil.copyfile(BASE / "physical" / name, WORK / name)
        assert digest(WORK / name) == digest(BASE / "physical" / name)
    shutil.copyfile(ROOT / "bitgen.tcl", WORK / "bitgen.tcl")
    project = ET.fromstring((BASE / "physical/road_board_selftest_top.al").read_text(encoding="utf-8").replace("UsedInP&R", "UsedInP&amp;R"))
    project.set("Path", WORK.as_posix())
    for item in project.findall(".//Source_Files//File"):
        source = Path(item.attrib["Path"])
        if not source.is_absolute():
            source = (BASE / "physical" / source).resolve()
        assert source.is_file(), source
        item.set("Path", source.as_posix())
    ET.ElementTree(project).write(WORK / "road_board_selftest_top.al", encoding="utf-8", xml_declaration=True)
    save("generation_inputs.json", {str(p): digest(p) for p in [*WORK.iterdir(), ROOT / "run.py", TD] if p.is_file()})
    print("FROZEN_INPUTS_PASS; bitgen only, no place/route/program", flush=True)
    try:
        with (WORK / "td.log").open("w", encoding="utf-8") as stream:
            result = subprocess.run([str(TD), "bitgen.tcl"], cwd=WORK, stdout=stream, stderr=subprocess.STDOUT, timeout=900, check=False)
        save("tool_result.json", {"command": [str(TD), "bitgen.tcl"], "cwd": str(WORK), "returncode": result.returncode, "board_access": False, "flash_access": False})
        assert result.returncode == 0, result.returncode
        area = (WORK / "imported.area").read_text(encoding="utf-8")
        assert re.search(r"i_rstn\s+INPUT\s+C7\s+LVCMOS33", area)
        for name, value in (("slice", 9691), ("dsp", 30), ("eram", 38)):
            assert int(re.search(r"^#" + name + r"\s+(\d+)", area, re.M)[1]) == value, name
        assert (WORK / "imported.ts").read_text() == (BASE / "physical/route.ts").read_text()
        bit = WORK / "RoadYOLO_HX1P35A_KEY4_SELFTEST.bit"
        assert bit.is_file() and bit.stat().st_size > 1024
        assert digest(WORK / "pr.db") == digest(BASE / "physical/pr.db")
        save("bitstream_receipt.json", {"path": str(bit), "bytes": bit.stat().st_size, "sha256": digest(bit), "source_pr_db_sha256": digest(WORK / "pr.db"), "device": "PH1P35MDG324", "speed": "3", "board": "HX1P35A V1.0", "reset": "KEY4/C7 active-low", "scope": "autonomous three-case DW/PW numerical selftest, not full CNN", "rtl_or_route_modified": False, "board_tested": False, "flash_written": False, "strict_gates_closed": False})
        print("BITGEN_PASS", bit.name, bit.stat().st_size, digest(bit), flush=True)
    finally:
        verify("frozen_after")


if __name__ == "__main__":
    main()
