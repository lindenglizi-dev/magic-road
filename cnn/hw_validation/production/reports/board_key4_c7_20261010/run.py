"""HX1P35A KEY4候选：仅迁移复位引脚，隔离重跑TD，不生成位流。"""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
OLD = ROOT.parent / "board_selftest_20261010"
WORK = ROOT / "physical"
TD = Path("E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/bin/td_commands_prompt.exe")
SKILL = Path("C:/Users/lenovo/.codex/skills/readable-verilog-generator")


def digest(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def save(name, value):
    target = ROOT / name
    target.resolve().relative_to(ROOT)
    assert not target.exists(), target
    target.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def check_old(label):
    manifest = json.loads((OLD / "evidence_attempt4/candidate_final_freeze.json").read_text(encoding="utf-8"))
    changed = [p for p, expected in manifest.items() if not Path(p).is_file() or digest(p) != expected]
    save(label + ".json", {"checked": len(manifest), "changed": changed})
    assert not changed, changed


def build():
    assert not WORK.exists(), "保留已有尝试，禁止覆盖"
    check_old("old_before")
    WORK.mkdir()
    for name in ("build.tcl", "board.sdc"):
        shutil.copyfile(OLD / "build" / name, WORK / name)
    shutil.copyfile(OLD / "program/selftest_program.hex", WORK / "selftest_program.hex")
    shutil.copyfile(ROOT / "board.adc", WORK / "board.adc")
    previous = (OLD / "build/board.adc").read_text(encoding="utf-8").splitlines()
    candidate = (WORK / "board.adc").read_text(encoding="utf-8").splitlines()
    # 只忽略注释；所有有效约束除R10→C7外必须逐行一致。
    active = lambda lines: [line.strip() for line in lines if line.strip() and not line.lstrip().startswith("#")]
    assert active(candidate) == [line.replace("LOCATION = R10", "LOCATION = C7") for line in active(previous)]
    text = (OLD / "physical_attempt2/road_board_selftest_top.al").read_text(encoding="utf-8")
    tree = ET.ElementTree(ET.fromstring(text.replace("UsedInP&R", "UsedInP&amp;R")))
    tree.getroot().set("Path", WORK.as_posix())
    sources = []
    for item in tree.findall(".//Source_Files//File"):
        source = Path(item.attrib["Path"])
        if not source.is_absolute():
            source = (OLD / "physical_attempt2" / source).resolve()
        assert source.is_file(), source
        source.relative_to(OLD)
        item.set("Path", source.as_posix())
        sources.append(source)
    assert len(sources) >= 19, len(sources)
    tree.write(WORK / "road_board_selftest_top.al", encoding="utf-8", xml_declaration=True)
    inputs = sources + list((OLD / "official/PLL").rglob("*")) + [TD, ROOT / "run.py", ROOT / "board.adc"]
    inputs += [WORK / name for name in ("board.adc", "board.sdc", "build.tcl", "road_board_selftest_top.al", "selftest_program.hex")]
    save("inputs.json", {str(p): digest(p) for p in inputs if p.is_file()})
    with (ROOT / "dependencies.log").open("w", encoding="utf-8") as stream:
        subprocess.run([sys.executable, "-B", SKILL / "scripts/python/toolchain/manage_skill_dependencies.py", "check", "--settings", SKILL / "config/defaults.json", "--state-path", ROOT / "dependency_state.json"], cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT, check=False)
    dependency_text = (ROOT / "dependencies.log").read_text(encoding="utf-8")
    dependencies = json.loads(dependency_text[dependency_text.index("{"):])
    assert dependencies["required_ok"], dependencies.get("missing_required_tools")
    print("INPUTS_FROZEN sources=", len(sources), "required_dependencies_ok=True", flush=True)
    try:
        with (WORK / "td.log").open("w", encoding="utf-8") as stream:
            result = subprocess.run([str(TD), "build.tcl"], cwd=WORK, stdout=stream, stderr=subprocess.STDOUT, timeout=3600, check=False)
        save("tool_result.json", {"returncode": result.returncode, "cwd": str(WORK), "command": [str(TD), "build.tcl"], "bitgen_requested": False})
        assert result.returncode == 0, result.returncode
    finally:
        check_old("old_after")


def collect():
    inputs = json.loads((ROOT / "inputs.json").read_text(encoding="utf-8"))
    assert all(digest(p) == expected for p, expected in inputs.items())
    # 复用冻结的只读报告解析器；不调用会向旧目录写入的main。
    sys.path.insert(0, str(OLD))
    spec = importlib.util.spec_from_file_location("frozen_evidence", OLD / "evidence.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    names = ("all_endpoints.timing", "internal_reg_to_reg.timing", "compute_reset_sync.timing", "pixel_reset_sync.timing", "compute_reset_distribution.timing", "hdmi_reset_distribution.timing", "dsp_inputs.timing", "dsp_outputs.timing", "eram_inputs.timing", "eram_outputs.timing")
    result = {name: module.paths(WORK / name) for name in names}
    save("timing_checks.json", result)
    check_old("old_final")
    save("outputs.json", {str(p): digest(p) for p in WORK.iterdir() if p.is_file()})
    print(json.dumps(result["all_endpoints.timing"], ensure_ascii=False))


if __name__ == "__main__":
    assert len(sys.argv) == 2 and sys.argv[1] in ("build", "collect")
    {"build": build, "collect": collect}[sys.argv[1]]()
