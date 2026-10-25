"""Freeze real stream RTL and CPU plane goldens; run actual local ModelSim.

Every attempt keeps its snapshot, logs and reports. No DUT or golden edits.
"""
from __future__ import annotations
import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
STREAM=ROOT.parent
PACKAGE=STREAM.parents[1]
REFERENCE=PACKAGE/"reference_head"
SKILL=Path("C:/Users/lenovo/.codex/skills/readable-verilog-generator")
MODEL=Path("D:/modeltech64_2020.4/win64")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--label",default="local")
    parser.add_argument("--only",type=int)
    parser.add_argument("--gates",action="store_true")
    args=parser.parse_args()
    if not re.fullmatch(r"[a-zA-Z0-9_]+",args.label):
        raise ValueError("safe attempt label required")
    report=ROOT/"reports"/(datetime.now().strftime("%Y%m%d_%H%M%S_%f")+"_"+args.label)
    snapshot=report/"inputs"
    snapshot.mkdir(parents=True)
    original={}

    def include(source,destination):
        original[str(source)]=sha(source)
        destination.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(source,destination)

    reference_manifest=read(REFERENCE/"artifact_manifest.json")
    assert all(sha(REFERENCE/name)==value for name,value in reference_manifest.items())
    reference_binding=read(REFERENCE/"input_binding.json")
    assert all(sha(Path(name))==value for name,value in reference_binding["source_sha256"].items())
    for name in ("prediction_lines160.hex","cell_field_addresses32.hex","head_cells112.hex","prediction_backing_ranges.json",
                 "input_binding.json","artifact_manifest.json","verification_receipt.json","prediction_receipt.json","FORMAT.txt","PREDICTION_FORMAT.txt"):
        include(REFERENCE/name,snapshot/"reference"/name)
    for name in ("requirements.json","ports.json","spec_input.json","reference.py","reference_receipt.json","codegen_plan.txt"):
        include(STREAM/name,snapshot/name)
    include(STREAM/"rtl/road_head_cell_stream.v",snapshot/"rtl/road_head_cell_stream.v")
    for name in ("tb_head_cell_stream.v","run_stream.py"):
        include(ROOT/name,snapshot/name)
    tb=dict(name="tb_head_cell_stream",rtl_path="tb_head_cell_stream.v",
            clock=dict(name="i_clk",edge="posedge",frequency_mhz=100),reset=dict(name="i_rstn",active="low",synchronous=False),
            interfaces=dict(ports=[dict(name="o_test_complete",direction="output",width=1,role="verification_completion",description="当前独立案例的实际比较通过后才置位")]),
            behavior=["读取冻结六平面物理128位行镜像，不用expected cell驱动源响应",
                      "实际请求逐个对齐独立字段地址，缓存复制每字段也逐个核对原graph地址",
                      "实际12096输出cell完整112位/id/token/model对拍，保留随机长反压",
                      "末源读消费、最末cell消费和done分别记录，取消与错误持busy直到共同reset"],
            constraints=["数组仅属于行为读服务和独立golden，不是DUT预测RAM或实际DDR",
                         "不更改DUT、冻结golden、五核，不做综合或物理映射"],
            corner_cases=["未committed不得准入、首握手后身份扰动、S4/S8/S16边界、H18末两行",
                          "请求pending、取消造成response-held、cell-held共同reset",
                          "错响应地址/error、取消持owner、真实checker一位负例"],
            verification_cases=["full12096_random","uncommitted","identity","cancel_request","reset_request",
                                "reset_response_held","reset_cell_held","wrong_address","read_error","cancel_cell","checker_negative"],
            timing_diagrams=[dict(id="retirement",title="最后读响应与最后cell分别退休",scenario="read-cell-retirement",
                                  description="协议示意不规定内部时延；读响应先消费，cell可以长时间保持；最后cell消费后才done。",
                                  wavejson=dict(signal=[dict(name="i_clk",wave="p..........."),dict(name="read_valid",wave="01..0......."),
                                       dict(name="read_ready",wave="0..10......."),dict(name="rsp_valid",wave="0....10....."),
                                       dict(name="rsp_ready",wave="0....10....."),dict(name="cell_valid",wave="0......1..0."),
                                       dict(name="cell_ready",wave="0........10."),dict(name="done",wave="0.........10")]))])
    save(snapshot/"tb_contract.json",dict(name="head_cell_stream_verification",modules=[tb]))
    combined=read(snapshot/"spec_input.json")
    save(snapshot/"spec_contract.json",dict(name="head_stream_local_validation",modules=combined.get("modules",[combined])+[tb]))
    closure={str(path.relative_to(snapshot)).replace("\\","/"):sha(path) for path in snapshot.rglob("*") if path.is_file()}
    receipt=dict(status="STARTED",original_sha256=original,snapshot_sha256=closure,
                 reference_closure_sha256=reference_binding["closure_sha256"],commands=[],tests=[],
                 tools={name:dict(path=str(MODEL/(name+".exe")),sha256=sha(MODEL/(name+".exe"))) for name in ("vlib","vlog","vsim")},
                 python=dict(path=sys.executable,sha256=sha(Path(sys.executable))),
                 boundary="Actual reader RTL + bounded behavioral logical read service; no actual DDR, preceding hardware producers, full network, physical RAM or FPS claim")
    def persist():
        save(report/"summary.json",receipt)
    def command(name,argv,cwd=snapshot,timeout=240):
        temporary=report/"runtime_tmp"
        temporary.mkdir(exist_ok=True)
        try:
            result=subprocess.run(list(map(str,argv)),cwd=cwd,capture_output=True,text=True,encoding="utf-8",errors="replace",timeout=timeout,
                                  env=dict(os.environ,PYTHONPATH=str(SKILL),TEMP=str(temporary),TMP=str(temporary)))
            code=result.returncode
            content=result.stdout+result.stderr
        except (OSError,subprocess.TimeoutExpired) as error:
            code=-998;content=repr(error)
        log=report/(name+".log")
        log.write_text(content,encoding="utf-8")
        effective=code or int(bool(re.search(r"\*\* (?:Error|Fatal):",content)))
        receipt["commands"].append(dict(name=name,argv=list(map(str,argv)),cwd=str(cwd),returncode=code,effective_returncode=effective,log_sha256=sha(log)))
        persist()
        return effective,content
    persist()
    for name,arguments in dict(dependencies=["scripts.python.toolchain.manage_skill_dependencies","check","--settings","config/defaults.json"],
                               renderer=["scripts.python.toolchain.wavedrom_runtime","--settings","config/defaults.json","check"],
                               readiness=["scripts.python.toolchain.preflight_verilog_toolchain","--settings","config/defaults.json","--readiness","execute"]).items():
        command(name,[sys.executable,"-B","-m",*arguments],SKILL,60)
    if args.gates:
        command("tb_spec",[sys.executable,"-B","-m","scripts.python.workflow.cli","write-spec","--spec",snapshot/"tb_contract.json",
                           "--source",snapshot/"tb_head_cell_stream.v","--out-dir",report/"documents","--language","zh"],SKILL,120)
        command("strict_gate",[sys.executable,"-B","-m","scripts.python.validation.generated_deliverable_gate",snapshot,"--include-testbench",
                               "--spec",snapshot/"spec_contract.json","--json",report/"gate.json","--markdown",report/"gate.md"],SKILL,240)
        if (report/"gate.json").exists():
            receipt["strict_eight_gates"]=read(report/"gate.json")["checks"]
        runtime={str(path):sha(path) for path in (SKILL/"scripts/python").rglob("*.py")}
        runtime.update({str(path):sha(path) for path in (SKILL/"config").rglob("*.json")})
        save(report/"skill_runtime_sha256.json",runtime)
    code,_=command("version",[MODEL/"vsim.exe","-version"],timeout=30)
    code,_=command("vlib",[MODEL/"vlib.exe","work"])
    if code:
        receipt["status"]="VLIB_FAILED_PRESERVED";persist();print(report);return 1
    code,_=command("compile",[MODEL/"vlog.exe","-work","work",snapshot/"rtl/road_head_cell_stream.v",snapshot/"tb_head_cell_stream.v"])
    if code:
        receipt["status"]="COMPILE_FAILED_PRESERVED";persist();print(report);return 1
    runs=[(mode,False) for mode in range(10)]+[(2,True)] if args.only is None else [(args.only,False)]
    for number,(mode,negative) in enumerate(runs):
        trace=report/f"trace_{number}.csv"
        argv=[MODEL/"vsim.exe","-c","-lib","work","tb_head_cell_stream",
              "+VECTOR_ROOT="+(snapshot/"reference").as_posix(),"+TRACE="+trace.as_posix(),f"+MODE={mode}",f"+NEGATIVE={int(negative)}",
              "-do","onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"]
        code,content=command("simulation_"+str(number),argv)
        passed=(bool(code) and "CELL_MISMATCH cell=0" in content and "HEAD_STREAM_PASS" not in content) if negative else code==0 and content.count("HEAD_STREAM_PASS")==1
        receipt["tests"].append(dict(mode=mode,negative=negative,status="PASS_REAL_CHECKER_NEGATIVE" if passed and negative else "PASS" if passed else "FAILED",
                                     metrics=[line for line in content.splitlines() if "HEAD_STREAM_" in line],trace_sha256=sha(trace) if trace.exists() else None))
        persist();print("mode",mode,"negative",negative,receipt["tests"][-1]["status"],flush=True)
        if not passed:
            break
    receipt["snapshot_unchanged"]=all(sha(snapshot/name)==value for name,value in closure.items())
    receipt["original_unchanged"]=all(sha(Path(name))==value for name,value in original.items())
    receipt["status"]="PASS" if receipt["snapshot_unchanged"] and receipt["original_unchanged"] and all(row["status"].startswith("PASS") for row in receipt["tests"]) else "FAILED_PRESERVED"
    persist();print(report)
    return 0 if receipt["status"]=="PASS" else 1


if __name__=="__main__":
    raise SystemExit(main())
