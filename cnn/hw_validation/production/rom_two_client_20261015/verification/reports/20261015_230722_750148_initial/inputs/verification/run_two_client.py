"""Freeze one two-client closure and run independent bounded ModelSim tops."""

from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
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
    parser.add_argument("--attempt-label", default="local")
    args = parser.parse_args()
    verification = Path(__file__).resolve().parent
    package = verification.parent
    project = package.parents[3]
    frozen = project / "cnn/reports/qat_frozen_stem_g10_20261014_v1/package"
    vendor = Path("E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/sim_release/ph1p")
    tools = {name: Path(shutil.which(name + ".exe") or "missing") for name in ("vlib", "vlog", "vsim")}
    if not all(path.is_file() for path in tools.values()):
        raise SystemExit("ModelSim tools unavailable")
    assert sha(package / "artifacts/numeric_test.bin") == PAYLOAD_SHA
    assert sha(package / "artifacts/numeric_test_padded.bin") == PHYSICAL_SHA
    for path in frozen.iterdir():
        if path.is_file():
            assert sha(package / "artifacts" / path.name) == sha(path), path.name
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    report = verification / "reports" / (stamp + "_" + args.attempt_label)
    report.mkdir(parents=True)
    snapshot = report / "inputs"
    snapshot.mkdir()
    for directory in ("rtl", "artifacts", "reference"):
        shutil.copytree(package / directory, snapshot / directory)
    for name in ("requirements.json", "codegen_plan.txt", "top_ports.json"):
        shutil.copy2(package / name, snapshot / name)
    tb_dir = snapshot / "verification"
    tb_dir.mkdir()
    for path in verification.iterdir():
        if path.is_file() and (path.suffix in (".v", ".py") or path.name.endswith("_spec.md")):
            shutil.copy2(path, tb_dir / path.name)
    models = snapshot / "vendor"
    models.mkdir()
    for name in ("ph1p_logic_eram.v", "ph1p_phy_gsr.v"):
        shutil.copy2(vendor / name, models / name)
    vector_dir = snapshot / "vectors"
    vector_dir.mkdir()
    physical = (snapshot / "artifacts/numeric_test_padded.bin").read_bytes()
    assert len(physical) == 143360
    (vector_dir / "physical_words.hex").write_text("".join(physical[n:n+20][::-1].hex()+"\n" for n in range(0,len(physical),20)),encoding="ascii")
    decoded = b"".join(int(line,16).to_bytes(20,"little") for line in (vector_dir / "physical_words.hex").read_text().splitlines())
    assert decoded == physical
    expected = json.loads((snapshot / "reference/prefetch_expected.json").read_text(encoding="utf-8"))
    assert len(expected)==1676 and sum(not item["is_table"] for item in expected)==652
    packed = [((int(item["is_table"])<<46)|(item["kind"]<<43)|(item["address"]<<32)|item["data_u32"]) for item in expected]
    assert packed == [int(line,16) for line in (snapshot / "reference/prefetch_expected_47.hex").read_text().splitlines()]
    for name,offset,count in (("sigmoid",137962,1024),("exp",140010,256)):
        values=[int(line,16) for line in (snapshot / f"reference/{name}_expected_16.hex").read_text().splitlines()]
        assert values==[int.from_bytes(physical[offset+n*2:offset+n*2+2],"little") for n in range(count)]
    closure = {path.relative_to(snapshot).as_posix():sha(path) for path in snapshot.rglob("*") if path.is_file()}
    receipt = {
        "status":"STARTED","attempt_label":args.attempt_label,"snapshot":str(snapshot),
        "payload_sha256":PAYLOAD_SHA,"physical_sha256":PHYSICAL_SHA,
        "closure_sha256":closure,"tools":{name:{"path":str(path),"sha256":sha(path)} for name,path in tools.items()},
        "commands":[],"tests":{},
        "boundaries":["Functional simulation with actual PH1P ERAM and GSR models","No full7168 audit, TD, physical resource/timing, DDR, board or full-network claim","Boundary top has controlled request-ready interposer; unchanged real-reader latency","Fair order assumes eventual reader request readiness, return, and owner response readiness","Original prefetch has no ROM-fault input; global fault requires common reset","Strict deliverable gate for DUT is separately owned by coordinator; default gate skips TB files"],
    }
    summary = report / "summary.json"

    def save() -> None:
        summary.write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")

    def execute(name: str,command: list[str]) -> tuple[int,str]:
        entry={"name":name,"argv":command,"cwd":str(snapshot)}
        receipt["commands"].append(entry);save()
        try:
            result=subprocess.run(command,cwd=snapshot,capture_output=True,text=True,timeout=args.timeout)
            code,output=result.returncode,result.stdout+result.stderr
        except subprocess.TimeoutExpired as failure:
            code,output=-999,str(failure)
        except OSError as failure:
            code,output=-998,repr(failure)
        (report / (name+".log")).write_text(output,encoding="utf-8")
        entry.update({"returncode":code,"warnings":[line for line in output.splitlines() if "Warning:" in line]});save()
        return code,output

    library=snapshot / "work"
    code,_=execute("vlib",[str(tools["vlib"]),str(library)])
    if code:
        receipt["status"]="LIBRARY_FAILED";save();print(summary);return 1
    sources=[*sorted(models.glob("*.v")),*sorted((snapshot / "rtl").glob("*.v")),*sorted(tb_dir.glob("tb_*.v"))]
    code,_=execute("vlog",[str(tools["vlog"]),"-work",str(library),*map(str,sources)])
    if code:
        receipt["status"]="COMPILE_FAILED";save();print(summary);return 1
    for top,marker,plusargs in (
        ("tb_rom_arbiter_boundary","TB_PASS_ROM_ARBITER_BOUNDARY",[f"+WORDS={(vector_dir / 'physical_words.hex').as_posix()}"]),
        ("tb_rom_two_client_real","TB_PASS_ROM_TWO_CLIENT_REAL",[f"+PREFETCH={(snapshot / 'reference/prefetch_expected_47.hex').as_posix()}",f"+SIGMOID={(snapshot / 'reference/sigmoid_expected_16.hex').as_posix()}",f"+EXP={(snapshot / 'reference/exp_expected_16.hex').as_posix()}"]),
    ):
        trace=report / (top+".csv")
        code,output=execute(top,[str(tools["vsim"]),"-c","-lib","work","PH1P_PHY_GSR",top,*plusargs,f"+TRACE={trace.as_posix()}","-do","onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"])
        passed=code==0 and marker in output and "TB_FAIL" not in output and "** Error:" not in output
        receipt["tests"][top]={"status":"PASS" if passed else "FAILED","returncode":code,"trace":str(trace),"metrics":[line for line in output.splitlines() if "METRIC " in line]}
        save();print(top,receipt["tests"][top]["status"])
    receipt["snapshot_unchanged"]=all(sha(snapshot / name)==digest for name,digest in closure.items())
    receipt["source_still_matches_snapshot"]=all(sha(package / name)==digest for name,digest in closure.items() if name.startswith(("rtl/","artifacts/","reference/")))
    receipt["status"]="PASS" if receipt["snapshot_unchanged"] and receipt["source_still_matches_snapshot"] and all(test["status"]=="PASS" for test in receipt["tests"].values()) else "FAILED"
    save();print(summary)
    return 0 if receipt["status"]=="PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
