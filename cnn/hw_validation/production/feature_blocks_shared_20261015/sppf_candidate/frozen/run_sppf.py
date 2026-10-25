"""SPPF增量候选：同一客户CSP4真实写回后进入SPPF；旧CSP候选只读。"""
import argparse
import copy
import importlib.util
from pathlib import Path
import os
import re
import shutil
import subprocess
import sys
import time

PARENT = Path(__file__).resolve().parent
ROOT = PARENT / "sppf_candidate"
_spec = importlib.util.spec_from_file_location("fixed_csp_readonly_run", PARENT / "run.py")
base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(base)
digest, read, save, verify = base.digest, base.read, base.save, base.verify
PROJECT, MODEL, VENDOR, SKILL, CORES, PAYLOAD = base.PROJECT, base.MODEL, base.VENDOR, base.SKILL, base.CORES, base.PAYLOAD


def specs():
    contract = copy.deepcopy(read(PARENT / "spec_contract.json"))
    contract["name"] = "feature_sppf"
    client, test = contract["modules"]
    client["behavior"] = ["固定块2/3/4保留，新增5=SPPF；start握手锁存身份，busy不切换",
        "一个FSM、3072B工作缓存、24项权重bank、唯一外部算术owner",
        "SPPF squeeze PW -> 三次signed INT8 pool5x5 pad=-128 -> 四路concat -> out PW",
        "pool单缓存口逐样本比较并持有写载荷至ready，不使用MAC/SiLU，不写y18/y19",
        "concat为四物理张量读视图，不复制实体concat缓存；每层写可见性后推进",
        "参数/屏障块归属及原核数值/II/复位保持，真实DDR尚未接入"]
    client["corner_cases"] += ["池化负数/极值及逻辑pad=-128区别于物理尾padding0", "池化长写背压及共同复位"]
    client["verification_cases"] = ["同实例真实CSP4写回结果供SPPF读取，全部conv和pool逐项对拍",
        "正常、随机、pool中共同复位后完整重跑、长写反压、实际pool检查器负例", "新增客户端对原2->3->4全幅回归"]
    test["name"] = "tb_feature_sppf_client"
    test["rtl_path"] = "tests/tb_feature_sppf_client.v"
    test["behavior"] = ["一个客户及唯一旧算术owner，顺序执行CSP4再SPPF，跨块保留真实写回内存",
        "只注入CSP4初始CPU源，SPPF从真实CSP4输出读取，不预填SPPF中间值",
        "卷积acc/pre/SiLU/post和池化signed max逐项核对，四路concat逐字节核验",
        "实际参数/读/核/写/屏障反压、pool中共同复位重跑及检查器负例分列"]
    test["corner_cases"] = client["corner_cases"]
    test["verification_cases"] = client["verification_cases"][:2]
    temporary = ROOT / "runtime_tmp"
    temporary.mkdir(exist_ok=True)
    for module in contract["modules"]:
        path = ROOT / (module["name"] + "_contract.json")
        save(path, dict(name="feature_sppf", modules=[module]))
        argv = [sys.executable,"-B","-m","scripts.python.workflow.cli","write-spec","--spec",str(path),
                "--out-dir",str(ROOT),"--language","zh"]
        if module is client:
            argv += ["--source",str(ROOT / module["rtl_path"])]
        result = subprocess.run(argv,cwd=PROJECT,env=dict(os.environ,PYTHONPATH=str(SKILL),TEMP=str(temporary),TMP=str(temporary)),
            capture_output=True,text=True,encoding="utf-8",errors="replace",timeout=60)
        log = ROOT / (module["name"] + "_render.log")
        log.write_text(result.stdout+result.stderr,encoding="utf-8")
        save(ROOT / (module["name"]+"_render_command.json"),dict(argv=argv,cwd=str(PROJECT),returncode=result.returncode,log_sha256=digest(log)))
        if result.returncode:
            raise RuntimeError("SPPF spec render failed; preserve before retry")
    save(ROOT / "spec_contract.json",contract)


def prepare(name):
    if not re.fullmatch(r"frozen(?:_attempt[1-9][0-9]*)?",name):
        raise ValueError("fresh candidate name required")
    target = ROOT / name
    if target.exists():
        raise ValueError("preserve existing candidate")
    previous = read(PARENT / "frozen_attempt2/input_binding.json")
    for binding in [previous,*previous["old_bindings"]]:
        verify(binding["original_sha256"])
        verify(binding["staged_sha256"])
    original, artifacts = {}, {}
    for filename in ("csp_manifest.json","sppf_manifest.json"):
        path = PARENT / "reference" / filename
        manifest = read(path)
        if manifest["payload_sha256"] != PAYLOAD:
            raise ValueError("SPPF reference model mismatch")
        original[str(path)] = digest(path)
        for relative, value in manifest["source_sha256"].items():
            original[str(PROJECT / relative)] = value
        for relative, value in manifest["artifacts"].items():
            source = PARENT / "reference" / relative
            if relative in artifacts and artifacts[relative] != value:
                raise ValueError("conflicting reference artifacts")
            artifacts[relative] = value
            original[str(source)] = value
    for folder in ("rtl","tests","spec"):
        files = [path for path in (ROOT / folder).rglob("*") if path.is_file() and "__pycache__" not in path.parts]
        if not files:
            raise ValueError(f"SPPF missing {folder}")
        original.update({str(path):digest(path) for path in files})
    for path in (Path(__file__),PARENT/"run.py",ROOT/"tb_contract.json",ROOT/"spec_contract.json",
                 ROOT/"reference_schedule.py",ROOT/"schedule_report.json"):
        original[str(path)] = digest(path)
    for module in CORES:
        path = PARENT / "frozen_attempt2/reused" / (module+".v")
        original[str(path)] = previous["staged_sha256"][str(path)]
    for tool in ("vlib","vlog","vsim"):
        path = MODEL / (tool+".exe")
        original[str(path)] = digest(path)
    for filename in ("ph1p_logic_eram.v","ph1p_phy_gsr.v"):
        path = VENDOR / filename
        original[str(path)] = digest(path)
    verify(original)
    target.mkdir()
    for folder in ("rtl","tests","spec"):
        shutil.copytree(ROOT/folder,target/folder,ignore=shutil.ignore_patterns("__pycache__"))
    for relative in artifacts:
        destination = target / "reference" / relative
        destination.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(PARENT/"reference"/relative,destination)
    for filename in ("csp_manifest.json","sppf_manifest.json"):
        shutil.copy2(PARENT/"reference"/filename,target/"reference"/filename)
    (target/"reused").mkdir()
    for module in CORES:
        shutil.copy2(PARENT/"frozen_attempt2/reused"/(module+".v"),target/"reused")
    shutil.copy2(PARENT/"frozen_attempt2/tests/tb_feature_blocks_client.v",target/"tests")
    shutil.copy2(PARENT/"frozen_attempt2/tests/tb_feature_blocks_client_spec.md",target/"tests")
    shutil.copy2(PARENT/"frozen_attempt2/tb_contract.json",target/"regression_contract.json")
    for filename in ("tb_contract.json","spec_contract.json","reference_schedule.py","schedule_report.json"):
        shutil.copy2(ROOT/filename,target/filename)
    shutil.copy2(Path(__file__),target/"run_sppf.py")
    staged = {str(path):digest(path) for path in target.rglob("*") if path.is_file()}
    save(target/"input_binding.json",dict(original_sha256=original,staged_sha256=staged,prior_binding=previous,
        payload_sha256=PAYLOAD,image_sha256=previous["image_sha256"],one_runtime_client=True,
        upstream_down3_down4_CPU_only=True,actual_DDR=False,physical_cache_mapping=False,production_delivery_ready=False))
    print("FROZEN_SPPF",target,flush=True)


def gate(name):
    target = ROOT/name
    output = target/"static_gate"
    output.mkdir(exist_ok=False)
    argv = [sys.executable,"-B","-m","scripts.python.validation.generated_deliverable_gate",str(target),
            "--include-testbench","--spec",str(target/"spec_contract.json"),"--json",str(output/"gate.json"),"--markdown",str(output/"gate.md")]
    result = subprocess.run(argv,cwd=SKILL,capture_output=True,text=True,encoding="utf-8",errors="replace",timeout=240)
    log = output/"run.log"
    log.write_text(result.stdout+result.stderr,encoding="utf-8")
    save(output/"command.json",dict(argv=argv,cwd=str(SKILL),returncode=result.returncode,log_sha256=digest(log)))
    if result.returncode not in (0,1) or not (output/"gate.json").is_file():
        raise RuntimeError("SPPF strict gate invocation failed")
    report = read(output/"gate.json")
    print("STRICT_GATE_SPPF",report["delivery_ready"],report["errors"],report["strict_warnings"],flush=True)


def execute(name,case,regression):
    target = ROOT/name
    binding = read(target/"input_binding.json")
    for item in [binding,binding["prior_binding"],*binding["prior_binding"]["old_bindings"]]:
        verify(item["original_sha256"])
        verify(item["staged_sha256"])
    run = target/("regression_case"+str(case) if regression else "case"+str(case))
    run.mkdir(exist_ok=False)
    records, started = [], time.monotonic()

    def command(argv,filename):
        result = subprocess.run(list(map(str,argv)),cwd=run,capture_output=True,text=True,encoding="utf-8",errors="replace",timeout=2400)
        content = result.stdout+result.stderr
        log = run/filename
        log.write_text(content,encoding="utf-8")
        code = result.returncode or int(bool(re.search(r"\*\* (?:Error|Fatal):",content)))
        records.append(dict(argv=list(map(str,argv)),cwd=str(run),native_returncode=result.returncode,validated_returncode=code,log_sha256=digest(log)))
        save(run/"commands.json",records)
        return content,code

    try:
        _,code = command([MODEL/"vlib.exe","work"],"vlib.log")
        if code:
            raise RuntimeError("SPPF vlib failed")
        sources = [VENDOR/"ph1p_logic_eram.v",VENDOR/"ph1p_phy_gsr.v"]
        sources += [target/"reused"/(module+".v") for module in CORES]
        sources += [target/"rtl/road_feature_blocks_client.v",target/"tests/tb_feature_sppf_client.v",target/"tests/tb_feature_blocks_client.v"]
        output,code = command([MODEL/"vlog.exe","-work","work",*sources],"compile.log")
        summaries = re.findall(r"Errors:\s*(\d+),\s*Warnings:\s*(\d+)",output)
        if code or not summaries or summaries[-1] != ("0","0"):
            raise RuntimeError("SPPF compile not clean")
        contract = read(target/("regression_contract.json" if regression else "tb_contract.json"))
        entry, = [row for row in contract["runner_cases"] if row["case"]==case]
        negative = case==99
        top = "tb_feature_blocks_client" if regression else "tb_feature_sppf_client"
        token = "NEGATIVE_ACC" if regression else "NEGATIVE_POOL"
        argv = [MODEL/"vsim.exe","-c","-lib","work","PH1P_PHY_GSR",top,
            f"+CASE={0 if negative else case}",f"+VECTORS_ROOT={(target/'reference').as_posix()}",
            *([f"+{token}=1"] if negative else entry.get("plusargs",[])),"-do","run -all; quit -code 0"]
        print("RUN_SPPF",case,"regression",regression,flush=True)
        output,code = command(argv,"simulation.log")
        prefix = "FEATURE_BLOCKS" if regression else "FEATURE_SPPF"
        if negative:
            required = "NEGATIVE_ACC injected acc mismatch" if regression else "NEGATIVE_POOL injected pool mismatch"
            if not code or required not in output or prefix+"_PASS" in output:
                raise AssertionError("SPPF actual checker negative escaped")
        else:
            if code:
                raise RuntimeError("SPPF simulation failed; preserved")
            markers = re.findall(prefix+r"_(?:PASS|EXPECTED_FAULT) [^\r\n]*",output)
            if len(markers)!=1 or not markers[0].startswith(entry["marker"]):
                raise AssertionError("SPPF unique marker absent")
            values = {key:int(value) for key,value in re.findall(r"(\w+)=(\d+)",markers[0])}
            if values.get("case")!=case or any(values.get(k)!=v for k,v in entry.get("expected_fields",{}).items()):
                raise AssertionError("SPPF receipt contract mismatch")
            ledger_prefix = "FEAT_BLOCK" if regression else "FEAT_SPPF"
            save(run/"receipt.json",dict(marker=markers[0],fields=values,
                stage_ledger=re.findall(ledger_prefix+r"_STAGE [^\r\n]*",output),
                state_ledger=re.findall(ledger_prefix+r"_STATE [^\r\n]*",output),
                measured_runs=re.findall(ledger_prefix+r"_RUN [^\r\n]*",output)))
        for item in [binding,binding["prior_binding"],*binding["prior_binding"]["old_bindings"]]:
            verify(item["original_sha256"])
            verify(item["staged_sha256"])
        save(run/"status.json",dict(status="PASS_REAL_CHECKER_NEGATIVE" if negative else "PASS_FUNCTION_CASE",case=case,
             regression=regression,seconds=time.monotonic()-started,actual_DDR=False,synthesis=False,full_graph=False,production_delivery_ready=False))
        print("PASS_SPPF",case,regression,round(time.monotonic()-started,2),flush=True)
    except BaseException as error:
        save(run/"status.json",dict(status="FAILED_PRESERVED",case=case,regression=regression,error=repr(error)))
        raise


if __name__=="__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action",choices=("spec","prepare","gate","execute"))
    parser.add_argument("--name",default="frozen")
    parser.add_argument("--case",type=int,default=0)
    parser.add_argument("--regression",action="store_true")
    args=parser.parse_args()
    if args.action=="spec":
        specs()
    elif args.action=="execute":
        execute(args.name,args.case,args.regression)
    else:
        globals()[args.action](args.name)
