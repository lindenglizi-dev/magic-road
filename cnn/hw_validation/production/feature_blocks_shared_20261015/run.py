"""固定块共享客户的独立封存、规格及功能仿真；不改旧候选或运行训练/TD。"""
import argparse
import importlib.util
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[3]
PRIOR = ROOT.parent / "csp_family_layer_scheduled_20261015"
CSP2 = ROOT.parent / "csp2_layer_scheduled_20261015"
_prior_spec = importlib.util.spec_from_file_location("readonly_feature_helpers", PRIOR / "run.py")
_prior = importlib.util.module_from_spec(_prior_spec)
_prior_spec.loader.exec_module(_prior)
digest, read, save, verify = _prior.digest, _prior.read, _prior.save, _prior.verify
MODEL, VENDOR, SKILL, CORES = _prior.MODEL, _prior.VENDOR, _prior.SKILL, _prior.CORES
PAYLOAD = "b35d4a66a69e441dc29bc60c7e3f507661f48da5f33b810d7340f6ed17a65145"


def preflight():
    output = ROOT / "dependency"
    output.mkdir(exist_ok=False)
    temporary = ROOT / "runtime_tmp"
    temporary.mkdir(exist_ok=True)
    environment = dict(os.environ, TEMP=str(temporary), TMP=str(temporary))
    entries = dict(dependencies=["scripts.python.toolchain.manage_skill_dependencies", "check", "--settings", "config/defaults.json"],
                   renderer=["scripts.python.toolchain.wavedrom_runtime", "--settings", "config/defaults.json", "check"],
                   readiness=["scripts.python.toolchain.preflight_verilog_toolchain", "--settings", "config/defaults.json", "--readiness", "execute"])
    for name, arguments in entries.items():
        argv = [sys.executable, "-B", "-m", *arguments]
        result = subprocess.run(argv, cwd=SKILL, env=environment, capture_output=True, text=True,
                                encoding="utf-8", errors="replace", timeout=60)
        log = output / (name + ".log")
        log.write_text(result.stdout + result.stderr, encoding="utf-8")
        save(output / (name + "_command.json"), dict(argv=argv, returncode=result.returncode,
            cwd=str(SKILL), log_sha256=digest(log)))
        print("PREFLIGHT", name, result.returncode, flush=True)


def spec():
    sys.path.insert(0, str(SKILL))
    from scripts.python.quality.formatter_ast import build_ast_report_for_text
    modules = []
    for relative in ("rtl/road_feature_blocks_client.v", "tests/tb_feature_blocks_client.v"):
        path = ROOT / relative
        ast = build_ast_report_for_text(path.read_text(encoding="utf-8"), source_path=path)
        save(ROOT / (path.stem + "_ast.json"), ast)
        is_tb = path.stem.startswith("tb_")
        if is_tb:
            ports = [dict(name="o_test_complete", direction="output", width=1,
                          role="verification_completion", description="所有当前场景检查完成")]
        else:
            if ast["summary"]["parse_errors"] or len(ast["modules"]) != 1:
                raise ValueError("client AST unavailable; no inferred interface")
            ports = []
            for port in ast["modules"][0]["ports"]:
                width = port["width"]
                high, low = map(int, width[1:-1].split(":")) if width else (0, 0)
                ports.append(dict(name=port["name"], direction=port["direction"], width=abs(high-low)+1,
                                  role="native", description=port["comment"]))
        clock, reset = ("clk", "rstn") if is_tb else ("i_clk", "i_rstn")
        module = dict(name=path.stem, rtl_path=relative,
            clock=dict(name=clock, edge="posedge", frequency_mhz=100),
            reset=dict(name=reset, active="low", synchronous=False), interfaces=dict(ports=ports),
            behavior=["start握手锁存固定块2/3/4，busy期间不得切换，非法选择故障拒绝",
                      "一个FSM、3072B工作缓存、24项权重bank，复用唯一外部算术owner",
                      "CSP2五阶段、CSP3/4七阶段，全幅整层可见性后推进",
                      "参数响应和屏障必须匹配锁存block_id，读返回匹配单在途地址",
                      "开始块清行缓存valid，工作缓存不reset但每个使用项先完整覆盖",
                      "共同复位清控制且重新装SiLU；不证明独立取消排空"],
            constraints=["固定图非任意引擎，核心端口/II/数值/复位不改",
                         "CSP2 Cin12尾mask0f，CSP4物理尾tile仅两行有效，禁止y18/y19写",
                         "同实例顺序运行不等于down3/down4已接入或连续CNN",
                         "4ERAM为容量组织目标，未实际映射/综合/物理时序",
                         "100M是整机1FPS目标，不是本组件已证明整机帧率"],
            corner_cases=["忙时block/start扰动，跨块缓存完全覆盖，随机背压保持payload",
                          "非法块、错误参数block、错误屏障block与真实acc负例",
                          "共同复位、SiLU重装、CSP4尾行与CSP2尾通道"],
            verification_cases=["同实例2->3->4全幅数值及地址逐项一致",
                                "正常/随机/复位完整序列和归属拒绝",
                                "阶段/状态/端点周期互斥核验，CPU来源与RTL计算分开"],
            timing_diagrams=[dict(id="select", title="固定块只在启动握手锁存", scenario="selection",
                description="中间省略全幅计算；done仍busy，返回idle后才接受下一块",
                wavejson=dict(signal=[dict(name=clock, wave="p..|......"),
                    dict(name="start_accept", wave="010|000010"),
                    dict(name="input_block", wave="==.|=...=.", data=["2", "3", "15", "3"]),
                    dict(name="locked_block", wave=".=.|....=.", data=["2", "3"]),
                    dict(name="busy", wave="0.1|110.1."),
                    dict(name="done", wave="0..|010..."),
                    dict(name="start_ready", wave="1.0|001.0.")]))])
        modules.append(module)
        contract = ROOT / (path.stem + "_contract.json")
        save(contract, dict(name="feature_blocks", modules=[module]))
        temporary = ROOT / "runtime_tmp"
        temporary.mkdir(exist_ok=True)
        argv = [sys.executable, "-B", "-m", "scripts.python.workflow.cli", "write-spec",
                "--spec", str(contract), "--out-dir", str(ROOT), "--language", "zh"]
        if not is_tb:
            argv += ["--source", str(path)]
        result = subprocess.run(argv, cwd=PROJECT, env=dict(os.environ,TEMP=str(temporary),TMP=str(temporary),PYTHONPATH=str(SKILL)),
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
        log = ROOT / (path.stem + "_spec_render.log")
        log.write_text(result.stdout + result.stderr, encoding="utf-8")
        save(ROOT / (path.stem + "_spec_command.json"), dict(argv=argv, cwd=str(PROJECT),
             returncode=result.returncode, log_sha256=digest(log)))
        if result.returncode:
            raise RuntimeError("spec render failed; preserved")
    save(ROOT / "spec_contract.json", dict(name="feature_blocks", modules=modules))


def prepare(name):
    if not re.fullmatch(r"frozen(?:_attempt[1-9][0-9]*)?", name):
        raise ValueError("fresh candidate name required")
    target = ROOT / name
    if target.exists():
        raise ValueError("preserve existing candidate")
    old_bindings = [read(CSP2 / "frozen/input_binding.json"), read(PRIOR / "frozen_attempt3/input_binding.json")]
    for previous in old_bindings:
        verify(previous["original_sha256"])
        verify(previous["staged_sha256"])
    manifest = read(ROOT / "reference/csp_manifest.json")
    if manifest["payload_sha256"] != PAYLOAD:
        raise ValueError("reference uses another model")
    image = read(ROOT / "reference/csp2/contract.json")["image_sha256"]
    if read(ROOT / "reference/source_receipts/family_manifest.json")["image_sha256"] != image:
        raise ValueError("CSP fixtures use different source images")
    original = {str(ROOT / "reference" / p): value for p, value in manifest["artifacts"].items()}
    for p, value in manifest["source_sha256"].items():
        path = Path(p)
        original[str(path if path.is_absolute() else PROJECT / path)] = value
    original[str(ROOT / "reference/csp_manifest.json")] = digest(ROOT / "reference/csp_manifest.json")
    for folder in ("rtl", "tests", "spec"):
        files = [p for p in (ROOT / folder).rglob("*") if p.is_file() and "__pycache__" not in p.parts]
        if not files:
            raise ValueError(f"missing {folder}")
        original.update({str(p): digest(p) for p in files})
    for filename in ("run.py", "requirements.txt", "tb_contract.json", "spec_contract.json"):
        original[str(ROOT / filename)] = digest(ROOT / filename)
    for path in (PRIOR / "run.py", CSP2 / "run.py"):
        original[str(path)] = digest(path)
    for module in CORES:
        path = PRIOR / "frozen_attempt3/reused" / (module + ".v")
        original[str(path)] = old_bindings[1]["staged_sha256"][str(path)]
    for tool in ("vlib", "vlog", "vsim"):
        path = MODEL / (tool + ".exe")
        original[str(path)] = digest(path)
    for filename in ("ph1p_logic_eram.v", "ph1p_phy_gsr.v"):
        path = VENDOR / filename
        original[str(path)] = digest(path)
    verify(original)
    target.mkdir()
    for folder in ("rtl", "tests", "spec"):
        shutil.copytree(ROOT / folder, target / folder, ignore=shutil.ignore_patterns("__pycache__"))
    for relative in (*manifest["artifacts"], "csp_manifest.json"):
        destination = target / "reference" / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / "reference" / relative, destination)
    (target / "reused").mkdir()
    for module in CORES:
        shutil.copy2(PRIOR / "frozen_attempt3/reused" / (module + ".v"), target / "reused")
    for filename in ("run.py", "requirements.txt", "tb_contract.json", "spec_contract.json"):
        shutil.copy2(ROOT / filename, target / filename)
    staged = {str(p): digest(p) for p in target.rglob("*") if p.is_file()}
    save(target / "input_binding.json", dict(original_sha256=original, staged_sha256=staged,
        old_bindings=old_bindings, payload_sha256=PAYLOAD, image_sha256=image,
        arithmetic_changed=False, actual_DDR=False, one_runtime_client=True,
        physical_shared_cache_mapped=False, production_delivery_ready=False))
    print("FROZEN", target, flush=True)


def gate(name):
    target = ROOT / name
    output = target / "static_gate"
    output.mkdir(exist_ok=False)
    argv = [sys.executable, "-B", "-m", "scripts.python.validation.generated_deliverable_gate",
            str(target), "--include-testbench", "--spec", str(target / "spec_contract.json"),
            "--json", str(output / "gate.json"), "--markdown", str(output / "gate.md")]
    result = subprocess.run(argv, cwd=SKILL, capture_output=True, text=True,
                            encoding="utf-8", errors="replace", timeout=240)
    log = output / "run.log"
    log.write_text(result.stdout + result.stderr, encoding="utf-8")
    save(output / "command.json", dict(argv=argv, cwd=str(SKILL), returncode=result.returncode, log_sha256=digest(log)))
    if result.returncode not in (0, 1) or not (output / "gate.json").is_file():
        raise RuntimeError("strict gate invocation failed")
    report = read(output / "gate.json")
    print("STRICT_GATE", report["delivery_ready"], report["errors"], report["strict_warnings"], flush=True)


def execute(name, case):
    target = ROOT / name
    binding = read(target / "input_binding.json")
    for entry in [binding, *binding["old_bindings"]]:
        verify(entry["original_sha256"])
        verify(entry["staged_sha256"])
    run = target / f"case{case}"
    run.mkdir(exist_ok=False)
    records = []
    started = time.monotonic()

    def command(argv, filename):
        result = subprocess.run(list(map(str, argv)), cwd=run, capture_output=True, text=True,
                                encoding="utf-8", errors="replace", timeout=2400)
        content = result.stdout + result.stderr
        log = run / filename
        log.write_text(content, encoding="utf-8")
        effective = result.returncode or int(bool(re.search(r"\*\* (?:Error|Fatal):", content)))
        records.append(dict(argv=list(map(str, argv)), cwd=str(run), native_returncode=result.returncode,
                            validated_returncode=effective, log_sha256=digest(log)))
        save(run / "commands.json", records)
        return content, effective

    try:
        output, code = command([MODEL / "vlib.exe", "work"], "vlib.log")
        if code:
            raise RuntimeError("vlib failed")
        sources = [VENDOR / "ph1p_logic_eram.v", VENDOR / "ph1p_phy_gsr.v"]
        sources += [target / "reused" / (module + ".v") for module in CORES]
        sources += [target / "rtl/road_feature_blocks_client.v", target / "tests/tb_feature_blocks_client.v"]
        output, code = command([MODEL / "vlog.exe", "-work", "work", *sources], "compile.log")
        summaries = re.findall(r"Errors:\s*(\d+),\s*Warnings:\s*(\d+)", output)
        if code or not summaries or summaries[-1] != ("0", "0"):
            raise RuntimeError("compile not clean")
        entries = [entry for entry in read(target / "tb_contract.json")["runner_cases"] if entry["case"] == case]
        if len(entries) != 1:
            raise ValueError("case contract not unique")
        entry = entries[0]
        negative = case == 99
        argv = [MODEL / "vsim.exe", "-c", "-lib", "work", "PH1P_PHY_GSR", "tb_feature_blocks_client",
                f"+CASE={0 if negative else case}", f"+VECTORS_ROOT={(target / 'reference').as_posix()}",
                *( ["+NEGATIVE_ACC=1"] if negative else entry.get("plusargs", [])),
                "-do", "run -all; quit -code 0"]
        print("RUN", case, flush=True)
        output, code = command(argv, "simulation.log")
        if negative:
            if not code or "NEGATIVE_ACC injected acc mismatch" not in output or "FEATURE_BLOCKS_PASS" in output:
                raise AssertionError("real checker negative not rejected")
        else:
            if code:
                raise RuntimeError("simulation failed; preserved")
            markers = re.findall(r"FEATURE_BLOCKS_(?:PASS|EXPECTED_FAULT) [^\r\n]*", output)
            if len(markers) != 1 or not markers[0].startswith(entry["marker"]):
                raise AssertionError("unique completion marker absent")
            values = {key: int(value) for key, value in re.findall(r"(\w+)=(\d+)", markers[0])}
            if values.get("case") != case or any(values.get(k) != v for k,v in entry.get("expected_fields", {}).items()):
                raise AssertionError("receipt differs from frozen contract")
            save(run / "receipt.json", dict(marker=markers[0], fields=values,
                stage_ledger=re.findall(r"FEAT_BLOCK_STAGE [^\r\n]*", output),
                state_ledger=re.findall(r"FEAT_BLOCK_STATE [^\r\n]*", output),
                measured_runs=re.findall(r"FEAT_BLOCK_RUN [^\r\n]*", output)))
        for record in [binding, *binding["old_bindings"]]:
            verify(record["original_sha256"])
            verify(record["staged_sha256"])
        save(run / "status.json", dict(status="PASS_REAL_CHECKER_NEGATIVE" if negative else "PASS_FUNCTION_CASE",
            case=case, seconds=time.monotonic()-started, one_runtime_client=True,
            physical_shared_cache_mapped=False, actual_DDR=False, full_graph=False,
            training_updates=0, synthesis=False, production_delivery_ready=False))
        print("PASS", case, round(time.monotonic()-started,2), flush=True)
    except BaseException as error:
        save(run / "status.json", dict(status="FAILED_PRESERVED", case=case, error=repr(error)))
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("preflight", "spec", "prepare", "gate", "execute"))
    parser.add_argument("--name", default="frozen")
    parser.add_argument("--case", type=int, default=0)
    args = parser.parse_args()
    if args.action in ("preflight", "spec"):
        globals()[args.action]()
    elif args.action == "execute":
        execute(args.name, args.case)
    else:
        globals()[args.action](args.name)
