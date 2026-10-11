"""完整 Stem 张量经过冻结 PAXI 桥的条件模型回归；不放行真实控制器。"""
import argparse
import ast
import importlib.util
import json
from pathlib import Path
import re
import shutil
import sys

import numpy as np

ROOT = Path(__file__).resolve().parent
PREVIOUS = ROOT.parent / "stem_down2_handoff_20261011"
PROJECT = ROOT.parents[4]
DDR = PROJECT / "cnn/hw_validation/ddr"
definition = importlib.util.spec_from_file_location("helpers", ROOT.parent/"down2_full_tensor_20261010/run.py")
helpers = importlib.util.module_from_spec(definition)
definition.loader.exec_module(helpers)
helpers.ROOT = ROOT
save, sha, fresh, command = helpers.save, helpers.sha, helpers.fresh, helpers.command


def check():
    frozen = json.loads((ROOT/"frozen.json").read_text(encoding="utf-8"))
    changed = [name for name, digest in frozen.items() if sha(Path(name)) != digest]
    save(ROOT/"frozen_check.json", {"checked":len(frozen), "changed":changed})
    assert not changed, changed


def prepare():
    assert not (ROOT/"frozen.json").exists()
    frozen = json.loads((PREVIOUS/"artifact_manifest.json").read_text(encoding="utf-8"))
    frozen[str(PREVIOUS/"artifact_manifest.json")] = sha(PREVIOUS/"artifact_manifest.json")
    frozen.update(json.loads((PREVIOUS/"dependency_check.json").read_text(encoding="utf-8"))["hashes"])
    protected = [DDR/"paxi_single_outstanding_bridge.v",DDR/"tb_paxi_single_outstanding_bridge.v",
        DDR/"paxi_single_outstanding_model.py",DDR/"requirements.md",
        PROJECT/"user_source/hdl_source/ph1p35_ddr/ph1p35_324_ddr_wrapper.v",
        PROJECT/"user_source/hdl_source/mc_to_user_interface.v",helpers.GRAPH]
    frozen.update({str(path):sha(path) for path in protected})
    save(ROOT/"frozen.json", frozen)
    check()
    graph=json.loads(helpers.GRAPH.read_text(encoding="utf-8"))
    stem=next(node for node in graph["nodes"] if node["name"]=="stem.conv")
    memory=stem["storage"]
    assert memory["base"]==55574528 and memory["raw_bytes"]==589824, memory
    addresses=np.arange(36864,dtype=np.uint32)*16+memory["base"]
    assert np.unique(addresses).size==36864
    assert int(addresses[0])==0x03500000 and int(addresses[-1])+16==0x03590000
    # 此处只证明候选映射可逆，不把模型右移一位当硅片地址证明。
    assert np.array_equal((addresses>>1)<<1,addresses)
    values=np.arange(256,dtype=np.uint8)
    assert all(int.from_bytes(values[i:i+16].tobytes(),"little").to_bytes(16,"little")==values[i:i+16].tobytes()
               for i in range(0,256,16))
    save(ROOT/"reference.json",{"status":"PASS", "scope":"address and little-endian transfer contract only",
        "base":memory["base"],"bytes":589824,"beats":36864,"beat_bytes":16,
        "controller_address":"candidate byte_addr >> 1, vendor proof remains required",
        "commit":"test endpoint explicitly publishes visibility; never wired to production",
        "integration_release":False,"previous_reference_sha256":sha(PREVIOUS/"reference.json")})
    print("TRANSFER_REFERENCE_PASS beats=36864 bytes=589824",flush=True)


def gate():
    work=fresh("gate")
    entry=f"import sys;sys.path.insert(0,{str(helpers.SKILL)!r});from scripts.python.validation.generated_deliverable_gate import main;raise SystemExit(main())"
    command([sys.executable,"-B","-X","utf8","-c",entry,ROOT/"tests","--include-testbench",
             "--external-interface-source",DDR/"paxi_single_outstanding_bridge.v","--external-interface-source",helpers.CORE,
             "--external-interface-source",PREVIOUS/"rtl","--json",work/"tests.json","--markdown",work/"tests.md"],
             work,"strict",allowed=(0,1,2))
    assert (work/"tests.json").exists(), "Gate failed to publish report; inspect strict.log"
    check()


def vendor_compile():
    """只编译原厂生成的完整文件集，确认当前模拟器能否读取匹配的加密模型。"""
    check()
    work=fresh("vendor_compile")
    source_root=PROJECT/"user_source/hdl_source/ph1p35_ddr"
    fileset=source_root/"ddr2/sim/fileset/fileset_mis.f"
    arguments=[line.strip().replace("<mis_path>",source_root.as_posix())
               for line in fileset.read_text(encoding="utf-8").splitlines()
               if line.strip() and not line.lstrip().startswith(("#", "+define+DDRPHY_ROM_INIT="))]
    files=[Path(arg) for arg in arguments if not arg.startswith("+")]
    assert all(path.exists() for path in files)
    configuration=source_root/"ddr2/src/rtl/include/ph1p_mis_define.vh"
    rom=source_root/"ddr2/src/rtl/phy/ddrphy_cfg_rom.txt"
    shutil.copyfile(rom,work/rom.name)
    previous=json.loads((PREVIOUS/"simulation_attempt3/receipt.json").read_text(encoding="utf-8"))
    command([helpers.MSIM/"vlib.exe","work"],work,"vlib")
    command([helpers.MSIM/"vlog.exe","-work","work",*previous["vendor_models"]],work,"primitives")
    # 原文件集依赖共享宏；不改厂商源码，只显式预载配置并使用单编译单元。
    output=command([helpers.MSIM/"vlog.exe","-work","work","-sv","-mfcu",
                    configuration,*arguments],work,"vlog",allowed=(0,1,2))
    record=json.loads((work/"vlog.command.json").read_text(encoding="utf-8"))
    save(work/"receipt.json",{"status":"PASS" if record["returncode"]==0 else "FAILED",
         "scope":"compile generated controller and vendor PHY only; no functional DDR execution",
         "source_hashes":{str(path):sha(path) for path in [*files,configuration,rom]},"fileset_sha256":sha(fileset),
         "log":"vlog.log"})
    print("VENDOR_COMPILE",record["returncode"],output.splitlines()[-3:],flush=True)


def vendor_elaborate():
    check()
    work=ROOT/"vendor_compile_attempt3"
    assert json.loads((work/"receipt.json").read_text(encoding="utf-8"))["status"]=="PASS"
    command([helpers.MSIM/"vsim.exe","-c","-lib","work","PH1P_PHY_GSR","ddr2",
             "-do","onerror {quit -code 1}; onbreak {quit -code 1}; run 0; quit -code 0"],
            work,"elaborate",allowed=(0,1,2))
    record=json.loads((work/"elaborate.command.json").read_text(encoding="utf-8"))
    save(work/"elaboration.json",{"status":"PASS" if record["returncode"]==0 else "FAILED",
         "scope":"hierarchy load only, no stimulus or physical DDR2 model, no initialization check",
         "log":"elaborate.log"})
    check()


def specifications():
    sys.path.insert(0,str(helpers.SKILL))
    from scripts.python.toolchain.dependency_state import check_dependencies
    settings=json.loads((helpers.SKILL/"config/defaults.json").read_text(encoding="utf-8"))
    dependencies=check_dependencies(settings,state_path=ROOT/"dependency_state.json")
    save(ROOT/"dependency_preflight.json",dependencies)
    assert dependencies["required_ok"], "Required skill/tool dependency missing"
    work=fresh("specifications")
    entry=f"import sys;sys.path.insert(0,{str(helpers.SKILL)!r});from scripts.python.workflow.cli import main;raise SystemExit(main())"
    output=command([sys.executable,"-B","-X","utf8","-c",entry,"write-spec",
        "--spec",ROOT/"tests/contract.json","--source",ROOT/"tests/tb_paxi_tensor_handoff.v",
        "--out-dir",work,"--no-state"],ROOT,str(work.relative_to(ROOT)/"tb"),allowed=(0,1,2))
    assert "ports must be non-empty" in output, "Recheck canonical portless TB support"
    save(work/"limitation.json",{"status":"BLOCKED_PORTLESS_TB","fake_ports_added":False,
         "manual_companion":"tests/tb_paxi_tensor_handoff_spec.md",
         "waveforms":"Unchanged H1-B bridge canonical WaveDrom SVGs reused"})
    check()


def finish():
    check()
    receipt=json.loads((ROOT/"simulation/receipt.json").read_text(encoding="utf-8"))
    assert receipt["status"]=="PASS"
    for name,digest in receipt["source_hashes"].items():
        assert sha(Path(name))==digest, name
    for path in (ROOT/"tests").iterdir():
        if path.suffix in (".v",".vh"):
            assert sha(path)==sha(ROOT/"simulation/sources"/path.name), path
    gates=json.loads((ROOT/"gate_attempt2/tests.json").read_text(encoding="utf-8"))
    cycles={}
    for result in receipt["results"]:
        if result["mode"]=="bridge_regression":
            continue
        line=next(line for line in result["lines"] if "PAXI_TENSOR_PASS" in line)
        values={key:int(value) for key,value in re.findall(r"(\w+)=(\d+)",line)}
        assert values["bytes"]==589824 and values["writes"]==values["reads"]==36864
        assert values["success"]==73728 and values["cancelled"]==2
        values["transfer_total_cycles"]=values["write_cycles"]+values["read_cycles"]
        cycles[result["mode"]]=values
    save(ROOT/"cycle_summary.json",{"scope":"conditional endpoint; not board or complete-network FPS","modes":cycles})
    frozen=json.loads((ROOT/"frozen_check.json").read_text(encoding="utf-8"))
    save(ROOT/"status.json",{"status":"CONDITIONAL_TRANSFER_PASS_REAL_DDR_BLOCKED",
        "date":"2026-10-11","integration_release":False,"tensor_mismatches":0,
        "previous_files_checked":frozen["checked"],"previous_files_changed":frozen["changed"],
        "strict_tests":{"errors":gates["errors"],"strict_warnings":gates["strict_warnings"],"checks":gates["checks"]},
        "vendor_compile":json.loads((ROOT/"vendor_compile_attempt3/receipt.json").read_text(encoding="utf-8")),
        "vendor_elaboration":json.loads((ROOT/"vendor_compile_attempt3/elaboration.json").read_text(encoding="utf-8")),
        "address_unit":"2 byte confirmed by installed IPUG034 table 2-17 and generated 128b/25b/26b configuration",
        "not_done":["Matched DDR2 chip model and controller functional testbench","Vendor RAW/commit guarantee",
                    "Synthesizable whole-tensor DMA sequencer","Production wrapper handshake repair",
                    "New top synthesis/timing","Deployment parameters/full CNN/board FPS"],
        "next":"Matched DDR2 chip model, actual IP testbench, RAW and independent AW/W acceptance; no fake commit"})
    save(ROOT/"artifact_manifest.json",{str(path):sha(path) for path in sorted(ROOT.rglob("*"))
        if path.is_file() and path.name!="artifact_manifest.json" and "work" not in path.relative_to(ROOT).parts
        and path.suffix not in (".wlf",".pyc")})
    print("FINAL_CONDITIONAL_TRANSFER_PASS old_files_unchanged="+str(frozen["checked"]),flush=True)


def simulate():
    check()
    work=fresh("simulation")
    sources=work/"sources";sources.mkdir()
    for source in [*sorted((ROOT/"tests").glob("*.v")),*sorted((ROOT/"tests").glob("*.vh")),
                   PREVIOUS/"tests/stem_driver.vh",PREVIOUS/"rtl/road_stem_tile_scheduler.v",
                   DDR/"paxi_single_outstanding_bridge.v",DDR/"tb_paxi_single_outstanding_bridge.v"]:
        shutil.copyfile(source,sources/source.name)
    previous=json.loads((PREVIOUS/"simulation_attempt3/receipt.json").read_text(encoding="utf-8"))
    command([helpers.MSIM/"vlib.exe","work"],work,"vlib")
    command([helpers.MSIM/"vlog.exe","-work","work","+incdir+"+sources.as_posix(),
             *previous["vendor_models"],*sorted(helpers.CORE.glob("*.v")),*sorted(sources.glob("*.v"))],work,"vlog")
    results=[]
    for mode in ("bridge_regression","normal","stalls"):
        print("SIMULATING",mode,flush=True)
        top="tb_paxi_single_outstanding_bridge" if mode=="bridge_regression" else "tb_paxi_tensor_handoff"
        output=command([helpers.MSIM/"vsim.exe","-c","-lib","work","PH1P_PHY_GSR",top,
            "+VECTORS="+(PREVIOUS/"vectors").as_posix(),"+MODE="+mode,"+ALLOW_CONDITIONAL_MODEL=1",
            "+REPORT="+(work/(mode+".csv")).as_posix(),"+DUMP="+(work/(mode+"_output.hex")).as_posix(),
            "-do","onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"],work,mode)
        marker="H1-B isolated PAXI bridge PASS" if mode=="bridge_regression" else "TB_PASS_PAXI_TENSOR_HANDOFF"
        assert marker in output,work/(mode+".log")
        if mode!="bridge_regression":
            actual=np.array([int(v,16) for v in (work/(mode+"_output.hex")).read_text().split()],dtype=np.uint8)
            actual=actual.view(np.int8).reshape(18,32,4,4,24).transpose(0,2,1,3,4).reshape(72,128,24)
            assert np.array_equal(actual,np.load(PREVIOUS/"vectors/expected_pw_hwc.npy"))
        results.append({"mode":mode,"status":"PASS","lines":[line for line in output.splitlines()
            if "PAXI_TENSOR" in line or "STEM_TOTAL" in line or marker in line]})
        save(work/"receipt.json",{"status":"PASS" if len(results)==3 else "PARTIAL",
            "scope":"conditional PAXI model; actual generated controller and DDR chip are not instantiated",
            "integration_release":False,"results":results,
            "source_hashes":{str(path):sha(path) for path in sources.iterdir()},
            "input_reference_sha256":sha(PREVIOUS/"reference.json")})
        print("SIM_PASS",mode,flush=True)
    check()


if __name__=="__main__":
    ast.parse(Path(__file__).read_text(encoding="utf-8"))
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action",choices=("prepare","gate","simulate","vendor_compile","vendor_elaborate","specifications","finish","check"))
    globals()[parser.parse_args().action]()
