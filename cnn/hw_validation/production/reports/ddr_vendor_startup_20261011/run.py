"""原厂 DDR 控制器有限启动观察，全部输出限于当前验证目录。"""
import argparse
import ast
import importlib.util
import json
from pathlib import Path
import re
import shutil
import sys

ROOT=Path(__file__).resolve().parent
PREVIOUS=ROOT.parent/"ddr_tensor_handoff_20261011"
PROJECT=ROOT.parents[4]
definition=importlib.util.spec_from_file_location("helper",ROOT.parent/"down2_full_tensor_20261010/run.py")
helper=importlib.util.module_from_spec(definition)
definition.loader.exec_module(helper)
helper.ROOT=ROOT
save,sha,command,fresh=helper.save,helper.sha,helper.command,helper.fresh


def check():
    frozen=json.loads((ROOT/"frozen.json").read_text(encoding="utf-8"))
    changed=[name for name,digest in frozen.items() if sha(Path(name))!=digest]
    save(ROOT/"frozen_check.json",{"checked":len(frozen),"changed":changed})
    assert not changed,changed


def prepare():
    assert not (ROOT/"frozen.json").exists()
    frozen=json.loads((PREVIOUS/"artifact_manifest.json").read_text(encoding="utf-8"))
    frozen[str(PREVIOUS/"artifact_manifest.json")]=sha(PREVIOUS/"artifact_manifest.json")
    frozen.update(json.loads((PREVIOUS/"frozen.json").read_text(encoding="utf-8")))
    receipt=json.loads((PREVIOUS/"vendor_compile_attempt3/receipt.json").read_text(encoding="utf-8"))
    frozen.update(receipt["source_hashes"])
    source_root=PROJECT/"user_source/hdl_source/ph1p35_ddr/ddr2"
    for path in source_root.rglob("*.vh"):
        frozen[str(path)]=sha(path)
    save(ROOT/"frozen.json",frozen)
    check()
    sys.path.insert(0,str(helper.SKILL))
    from scripts.python.toolchain.dependency_state import check_dependencies
    settings=json.loads((helper.SKILL/"config/defaults.json").read_text(encoding="utf-8"))
    dependencies=check_dependencies(settings,state_path=ROOT/"dependency_state.json")
    save(ROOT/"dependency_preflight.json",dependencies)
    assert dependencies["required_ok"]
    save(ROOT/"reference.json",{"ref_period_ps":10000,"reset_release_ps":2000000,
         "end_ps":1002000000,"expected_ref_edges":100200,"memory_pass_allowed":False})


def gate():
    work=fresh("gate")
    entry=f"import sys;sys.path.insert(0,{str(helper.SKILL)!r});from scripts.python.validation.generated_deliverable_gate import main;raise SystemExit(main())"
    command([sys.executable,"-B","-X","utf8","-c",entry,ROOT/"tests","--include-testbench",
        "--external-interface-source",PROJECT/"user_source/hdl_source/ph1p35_ddr/ddr2/ddr2.v",
        "--json",work/"tests.json","--markdown",work/"tests.md"],work,"strict",allowed=(0,1,2))
    assert (work/"tests.json").exists()
    check()


def simulate():
    check()
    work=fresh("simulation")
    source_root=PROJECT/"user_source/hdl_source/ph1p35_ddr"
    fileset=source_root/"ddr2/sim/fileset/fileset_mis.f"
    args=[line.strip().replace("<mis_path>",source_root.as_posix()) for line in fileset.read_text().splitlines()
          if line.strip() and not line.lstrip().startswith(("#","+define+DDRPHY_ROM_INIT="))]
    cfg=source_root/"ddr2/src/rtl/include/ph1p_mis_define.vh"
    rom=source_root/"ddr2/src/rtl/phy/ddrphy_cfg_rom.txt"
    shutil.copyfile(rom,work/rom.name)
    tb=work/"tb_ddr_vendor_startup.v"
    shutil.copyfile(ROOT/"tests"/tb.name,tb)
    models=json.loads((ROOT.parent/"stem_down2_handoff_20261011/simulation_attempt3/receipt.json").read_text(encoding="utf-8"))["vendor_models"]
    command([helper.MSIM/"vlib.exe","work"],work,"vlib")
    command([helper.MSIM/"vlog.exe","-work","work",*models],work,"primitives")
    command([helper.MSIM/"vlog.exe","-work","work","-sv","-mfcu",cfg,*args,tb],work,"vlog")
    output=command([helper.MSIM/"vsim.exe","-c","-voptargs=+acc","-lib","work","PH1P_PHY_GSR","tb_ddr_vendor_startup",
        "-wlf",work/"startup.wlf","-do","onerror {quit -code 1}; onbreak {quit -code 1}; log /tb_ddr_vendor_startup/*; run -all; quit -code 0"],
        work,"startup",allowed=(0,1,2))
    summary=[line for line in output.splitlines() if "STARTUP_" in line or "PHY_READY_WITHOUT_CHIP" in line or "DRAM_COMMAND" in line]
    execution=json.loads((work/"startup.command.json").read_text(encoding="utf-8"))
    completed="STARTUP_SUMMARY" in output and execution.get("returncode")==0 and "** Fatal:" not in output
    save(work/"receipt.json",{"status":"OBSERVATION_COMPLETE" if completed else "FAILED",
        "memory_pass":False,"chip_model":"absent","lines":summary,"tb_sha256":sha(tb),
        "execution":execution,
        "vendor_hashes":{str(path):sha(Path(path)) for path in models},"fileset_sha256":sha(fileset)})
    print("\n".join(summary),flush=True)
    check()


def specifications():
    work=fresh("specifications")
    wave={"signal":[{"name":"ref_clk","wave":"p........."},
        {"name":"sys_rst_n","wave":"0..1......"},
        {"name":"PAXI_valid","wave":"0........."},
        {"name":"derived_clock_or_ready","wave":"x........."}],
        "head":{"text":"Schematic only: clock/ready outputs are observed, not forced"}}
    module={"name":"tb_ddr_vendor_startup","feature":"ddr_vendor_startup","rtl_path":"tb_ddr_vendor_startup.v",
        "description":"Portless original-IP startup observation, no device model or memory PASS",
        "interfaces":{"protocol":"discrete","ports":[]},"parameters":[],
        "clock":{"name":"ref_clk","edge":"posedge","frequency_hz":100000000},
        "reset":{"name":"sys_rst_n","active":"low","synchronous":False,"values":"Low for 2us, then observed for 1ms"},
        "behavior":["Idle APB and PAXI; observe original clocks, resets and DDR commands"],
        "constraints":["No force, clock replacement, model substitution or timing acceleration"],
        "corner_cases":["Missing clock, readiness timeout, unsolicited return"],
        "verification_cases":["100200 reference rising edges in 1002us; no read/write claim without chip model"],
        "timing_diagrams":[{"id":"startup","title":"Startup observation","scenario":"startup",
            "description":"Compressed stimulus schematic, no asserted PLL lock latency", "wavejson":wave}]}
    save(work/"contract.json",{"modules":[module]})
    entry=f"import sys;sys.path.insert(0,{str(helper.SKILL)!r});from scripts.python.workflow.cli import main;raise SystemExit(main())"
    output=command([sys.executable,"-B","-X","utf8","-c",entry,"write-spec","--spec",work/"contract.json",
        "--source",ROOT/"tests/tb_ddr_vendor_startup.v","--out-dir",work,"--no-state"],ROOT,
        str(work.relative_to(ROOT)/"canonical"),allowed=(0,1,2))
    assert "ports must be non-empty" in output
    save(work/"limitation.json",{"status":"BLOCKED_PORTLESS_TB","fake_ports_added":False})
    save(work/"startup.wave.json",wave)
    entry=f"import sys;sys.path.insert(0,{str(helper.SKILL)!r});from scripts.python.toolchain.wavedrom_runtime import main;raise SystemExit(main())"
    command([sys.executable,"-B","-X","utf8","-c",entry,"render","--input",work/"startup.wave.json",
        "--output",work/"startup.svg"],ROOT,str(work.relative_to(ROOT)/"render"))
    check()


def finish():
    check()
    work=ROOT/"simulation"
    receipt=json.loads((work/"receipt.json").read_text(encoding="utf-8"))
    assert receipt["status"]=="OBSERVATION_COMPLETE",receipt["status"]
    execution=json.loads((work/"startup.command.json").read_text(encoding="utf-8"))
    assert execution["returncode"]==0
    log=(work/"startup.log").read_text(encoding="utf-8")
    assert "Errors: 0," in log and "** Fatal:" not in log
    assert sha(ROOT/"tests/tb_ddr_vendor_startup.v")==receipt["tb_sha256"]
    line=next(line for line in receipt["lines"] if "STARTUP_SUMMARY" in line)
    values={key:int(value) for key,value in re.findall(r"(\w+)=(\d+)",line)}
    assert values["ref"]==100200 and values["unsolicited"]==0,values
    # 原日志的%t按厂商模型最小1fs精度打印，虽然标签写ps；发布数据显式纠正。
    assert values["ready_time_ps"]%1000==0
    values["ready_time_ps"]=values["ready_time_ps"]//1000
    samples=[]
    for line in receipt["lines"]:
        if "STARTUP_SAMPLE" in line:
            sample={key:int(value) for key,value in re.findall(r"(\w+)=(\d+)",line)}
            sample["time_ps"]//=1000
            samples.append(sample)
    assert len(samples)==10 and samples[-1]["time_ps"]==1002000000
    rates={name: (samples[-1][name+"_edges"]-samples[-2][name+"_edges"])/100.0
           for name in ("cfg","dhi","ddr")}
    gates=json.loads((ROOT/"gate/tests.json").read_text(encoding="utf-8"))
    save(ROOT/"status.json",{"status":"REAL_IP_STARTUP_OBSERVED_MEMORY_MODEL_MISSING",
        "memory_pass":False,"observed":values,"strict_gate":{"errors":gates["errors"],"checks":gates["checks"]},
        "samples":samples,"last_100us_frequency_mhz":rates,"simulation_seconds":execution["seconds"],
        "log_time_correction":"time_ps fields formatted via %t are in fs; normalized here to ps using vendor simulation precision 1fs",
        "ready_is_not_memory_evidence":True,"frozen":json.loads((ROOT/"frozen_check.json").read_text()),
        "next":"Obtain supported PH1P35MDG324 integrated DDR2 model/testbench and write-visibility contract"})
    save(ROOT/"artifact_manifest.json",{str(path):sha(path) for path in sorted(ROOT.rglob("*")) if path.is_file()
        and path.name!="artifact_manifest.json" and "work" not in path.relative_to(ROOT).parts and path.suffix not in (".wlf",".pyc")})
    print(json.dumps(values),flush=True)


if __name__=="__main__":
    ast.parse(Path(__file__).read_text(encoding="utf-8"))
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action",choices=("prepare","gate","simulate","specifications","finish","check"))
    globals()[parser.parse_args().action]()
