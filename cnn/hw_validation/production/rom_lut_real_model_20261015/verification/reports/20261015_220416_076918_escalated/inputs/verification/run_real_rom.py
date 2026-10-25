"""Snapshot the real G10 ROM closure and run two independent ModelSim tops."""

from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys


PAYLOAD_SHA = "b35d4a66a69e441dc29bc60c7e3f507661f48da5f33b810d7340f6ed17a65145"
PHYSICAL_SHA = "bab36c254dfeb21ad21f4c600018be962f9352ddde79dcb08e64e7bd117ec417"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--attempt-label", default="sandbox")
    args = parser.parse_args()
    verification = Path(__file__).resolve().parent
    package = verification.parent
    project = package.parents[3]
    frozen = project / "cnn/reports/qat_frozen_stem_g10_20261014_v1/package"
    vendor = Path("E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/sim_release/ph1p")
    tools = {name: Path(shutil.which(name + ".exe") or "missing") for name in ("vlib", "vlog", "vsim")}
    if not all(path.is_file() for path in tools.values()):
        raise SystemExit("ModelSim tools unavailable")
    payload = frozen / "numeric_test.bin"
    physical = frozen / "numeric_test_padded.bin"
    assert sha(payload) == PAYLOAD_SHA and sha(physical) == PHYSICAL_SHA
    assert physical.read_bytes() == payload.read_bytes() + bytes(2838)
    assert len(payload.read_bytes()) == 140522 and len(physical.read_bytes()) == 143360
    for path in frozen.iterdir():
        if path.is_file():
            assert sha(package / "artifacts" / path.name) == sha(path), path.name
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    report = verification / "reports" / (stamp + "_" + args.attempt_label)
    report.mkdir(parents=True)
    snapshot = report / "inputs"
    snapshot.mkdir()
    for directory in ("rtl", "artifacts"):
        shutil.copytree(package / directory, snapshot / directory)
    tb_dir = snapshot / "verification"
    tb_dir.mkdir()
    for path in verification.iterdir():
        if path.is_file():
            shutil.copy2(path, tb_dir / path.name)
    models = snapshot / "vendor"
    models.mkdir()
    vendor_paths = [vendor / "ph1p_logic_eram.v", vendor / "ph1p_phy_gsr.v"]
    for path in vendor_paths:
        shutil.copy2(path, models / path.name)
    vector_dir = snapshot / "vectors"
    vector_dir.mkdir()
    physical_bytes = physical.read_bytes()
    (vector_dir / "physical_words.hex").write_text("".join(physical_bytes[n:n+20][::-1].hex()+"\n" for n in range(0,143360,20)), encoding="ascii")
    for name, offset, count in (("sigmoid",137962,1024),("exp",140010,256)):
        (vector_dir / (name+".hex")).write_text("".join(f"{int.from_bytes(physical_bytes[offset+2*n:offset+2*n+2],'little'):04x}\n" for n in range(count)), encoding="ascii")
    # Independent byte reconstruction checks the testbench word endian convention.
    decoded = b"".join(int(line,16).to_bytes(20,"little") for line in (vector_dir / "physical_words.hex").read_text().splitlines())
    assert decoded == physical_bytes
    closure = {str(path.relative_to(snapshot)).replace("\\","/"): sha(path) for path in snapshot.rglob("*") if path.is_file()}
    receipt = {
        "status":"STARTED", "attempt_label":args.attempt_label,
        "payload_sha256":PAYLOAD_SHA,"physical_sha256":PHYSICAL_SHA,
        "payload_bytes":140522,"padding_bytes":2838,"physical_bytes":143360,
        "closure_sha256":closure,"tools":{name:{"path":str(path),"sha256":sha(path)} for name,path in tools.items()},
        "commands":[],"tests":{},"boundaries":["Functional vendor-model simulation only","No physical mapping/timing, DDR, board, full-network or 1FPS conclusion","No forced or injected real-ROM failures"],
    }
    summary = report / "summary.json"

    def save() -> None:
        summary.write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")

    def execute(name: str, command: list[str]) -> tuple[int,str]:
        entry = {"name":name,"argv":command,"cwd":str(snapshot)}
        receipt["commands"].append(entry)
        save()
        try:
            result = subprocess.run(command,cwd=snapshot,capture_output=True,text=True,timeout=args.timeout)
            code, output = result.returncode,result.stdout+result.stderr
        except subprocess.TimeoutExpired as failure:
            code,output = -999,str(failure)
        except OSError as failure:
            code,output = -998,repr(failure)
        (report / (name+".log")).write_text(output,encoding="utf-8")
        entry.update({"returncode":code,"warnings":[line for line in output.splitlines() if "Warning:" in line]})
        save()
        return code,output

    library = report / "work"
    code,_ = execute("vlib",[str(tools["vlib"]),str(library)])
    if code:
        receipt["status"]="LIBRARY_FAILED";save();print(summary);return 1
    sources = [*sorted(models.glob("*.v")),*sorted((snapshot / "rtl").glob("*.v")),*sorted(tb_dir.glob("tb_*.v"))]
    code,_ = execute("vlog",[str(tools["vlog"]),"-work",str(library),*map(str,sources)])
    if code:
        receipt["status"]="COMPILE_FAILED";save();print(summary);return 1
    for top,marker,plusargs in (
        ("tb_real_model_rom_reader","TB_PASS_REAL_MODEL_ROM_READER",[f"+WORDS={vector_dir / 'physical_words.hex'}"]),
        ("tb_real_model_lut","TB_PASS_REAL_MODEL_LUT",[f"+SIGMOID={vector_dir / 'sigmoid.hex'}",f"+EXP={vector_dir / 'exp.hex'}"]),
    ):
        trace = report / (top+".csv")
        command = [str(tools["vsim"]),"-c","-lib",str(library),"PH1P_PHY_GSR",top,*plusargs,f"+TRACE={trace}","-do","onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"]
        code,output = execute(top,command)
        passed = code==0 and marker in output and "TB_FAIL" not in output and "** Error:" not in output
        receipt["tests"][top] = {"status":"PASS" if passed else "FAILED","returncode":code,"trace":str(trace),"metrics":[line for line in output.splitlines() if "METRIC " in line]}
        save()
        print(top,receipt["tests"][top]["status"])
    receipt["snapshot_unchanged"] = all(sha(snapshot / name)==digest for name,digest in closure.items())
    receipt["status"] = "PASS" if receipt["snapshot_unchanged"] and all(test["status"]=="PASS" for test in receipt["tests"].values()) else "FAILED"
    save();print(summary)
    return 0 if receipt["status"]=="PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
