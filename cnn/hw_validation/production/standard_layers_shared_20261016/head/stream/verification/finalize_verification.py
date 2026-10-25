"""Keep simulator and strict-gate evidence separate, render confirmed TB timing."""
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode=True
from run_stream import ROOT,REFERENCE,SKILL,read,save,sha


def main():
    report=ROOT/"reports/20261016_014307_806497_final_suite"
    result=read(report/"summary.json")
    assert result["status"]=="PASS" and len(result["tests"])==11
    assert all(row["status"].startswith("PASS") for row in result["tests"])
    assert all(sha(Path(name))==value for name,value in result["original_sha256"].items())
    assert all(sha(report/"inputs"/name)==value for name,value in result["snapshot_sha256"].items())
    target=ROOT/"finalization"/datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    target.mkdir(parents=True)
    temporary=target/"runtime_tmp"
    temporary.mkdir()
    render_root=ROOT/"s"  # Keep the renderer's temporary paths below Windows path limits.
    # Confirmed-spec route: the runtime source checker misclassifies function
    # formal 'address' as a top-level TB port. Do not invent that extra port.
    argv=[sys.executable,"-B","-m","scripts.python.workflow.cli","write-spec","--spec",str(report/"inputs/tb_contract.json"),
          "--out-dir",str(render_root),"--language","zh"]
    completed=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,encoding="utf-8",errors="replace",timeout=120,
                             env=dict(os.environ,PYTHONPATH=str(SKILL),TEMP=str(temporary),TMP=str(temporary)))
    log=target/"confirmed_tb_spec.log"
    log.write_text(completed.stdout+completed.stderr,encoding="utf-8")
    assert completed.returncode==0,log
    diagrams=list(render_root.rglob("*.svg"))
    specs=list(render_root.rglob("*_spec.md"))
    assert len(diagrams)==len(specs)==1
    gate=read(report/"gate.json")
    gates={name:dict(data) for name,data in gate["checks"].items()}
    gates["toolchain"]={"status":"passed","source":"Actual local ModelSim2020.4 vlog+vsim","positive_cases":10,"real_checker_negative":1,
                         "strict_gate_original_status":gate["checks"]["toolchain"]["status"]}
    samples=[int(line,16) for line in (REFERENCE/"head_cells112.hex").read_text(encoding="ascii").splitlines()]
    outside=0
    for cell in samples:
        for lane in range(7):
            value=(cell>>(lane*16))&65535
            signed=value if value<32768 else value-65536
            outside+=int(signed < -128 or signed > 127)
    assert outside>0
    source={str(report/"summary.json"):sha(report/"summary.json"),str(report/"gate.json"):sha(report/"gate.json"),
            str(report/"skill_runtime_sha256.json"):sha(report/"skill_runtime_sha256.json"),str(Path(__file__)):sha(Path(__file__)),
            str(ROOT/"quality_initial/dut_gate.json"):sha(ROOT/"quality_initial/dut_gate.json")}
    source.update({str(path):sha(path) for path in render_root.rglob("*") if path.is_file()})
    source[str(log)]=sha(log)
    closure=hashlib.sha256(json.dumps(source,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    summary={"status":"FUNCTIONAL_PASS_STRICT_NOT_READY","actual_modelsim":"PASS","tests":result["tests"],"eight_gates":gates,
             "strict_original_checks":gate["checks"],"normal_metrics":result["tests"][0]["metrics"],"raw16_values_outside_int8":outside,
             "confirmed_tb_spec":str(specs[0]),"timing_diagram":str(diagrams[0]),"render_command":argv,
             "confirmed_spec_only":True,"source_port_checker_failure":"Function input address incorrectly treated as top-level TB port; original failure retained",
             "functional_snapshot":str(report/"inputs"),"functional_receipt":str(report/"summary.json"),"finalization_closure_sha256":closure,
             "source_sha256":source,"tool_hashes":result["tools"],"snapshot_unchanged":True,"original_unchanged":True,
             "boundary":"Actual stream RTL with controlled bounded behavioral128 read service; not physicalDDR, actual head producers, continuous prefix, whole network, timing/resource or FPS acceptance"}
    save(target/"delivery.json",summary)
    save(ROOT/"delivery.json",summary)
    text=("角色：verify；独占head/stream/verification/。DUT与全部reference保持只读。\n"
          "真实ModelSim：10正向协议案例与1真实比较器负例通过。完整12096cell、84672field、30240实际read/response一致。\n"
          "完整正常流313338拍；最后源读消费313293、末cell消费313336、完成随后出现。随机请求背压14723拍、cell背压6192拍。\n"
          "未committed拒绝、首握手后identity扰动、两尺度边界/H18尾、request/response-held/cell-held reset、cancel与错地址/error故障占有至reset均覆盖。\n"
          "response-held由取消撤ready后真实未决响应保持构造；共同reset同时取消行为源和DUT，不解释成正常响应端反压能力。\n"
          "原DUT八门与包含TB的严格八门原样保留。TB formatter控制解析失败；ModelSim编译/执行成功不替代严格静态失败。\n"
          "TB周期图已通过confirmed-spec无source路线生成；原source checker把function formal误认模块端口的失败保留，不添加假端口。\n"
          "所有原始sandbox/DLL/规格渲染失败和负例日志保留。未TD/训练/生产/板卡/commit，不是实际DDR/head生产者/整网。\n"
          f"最终回执：{target/'delivery.json'}\n最终闭包：{closure}\n")
    (ROOT/"handoff.txt").write_text(text,encoding="utf-8")
    print(json.dumps({"status":summary["status"],"raw16_values_outside_int8":outside,"closure_sha256":closure,"delivery":str(target/"delivery.json")}))


if __name__=="__main__":
    main()
