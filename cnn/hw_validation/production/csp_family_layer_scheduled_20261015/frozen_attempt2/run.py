"""固定CSP3/CSP4候选封存及本地功能仿真；旧CSP2目录始终只读。"""
import argparse
import importlib.util
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[3]
PRIOR = ROOT.parent / "csp2_layer_scheduled_20261015"
REFERENCE = ROOT / "reference_attempt2"  # 首次参考残差旁路错误保留，改用独立修正副本
SKILL = Path("C:/Users/lenovo/.codex/skills/readable-verilog-generator")
MODEL = Path("D:/modeltech64_2020.4/win64")
VENDOR = Path("E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/sim_release/ph1p")
_prior_spec = importlib.util.spec_from_file_location("csp_layer_readonly_helpers", PRIOR / "run.py")
_prior = importlib.util.module_from_spec(_prior_spec)
_prior_spec.loader.exec_module(_prior)
digest, read, save, verify, CORES = _prior.digest, _prior.read, _prior.save, _prior.verify, _prior.CORES


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
        (output / (name + ".log")).write_text(result.stdout + result.stderr, encoding="utf-8")
        save(output / (name + "_command.json"), dict(argv=argv, returncode=result.returncode,
            cwd=str(SKILL), log_sha256=digest(output / (name + ".log"))))
        print("PREFLIGHT", name, result.returncode, flush=True)


def spec():
    sys.path.insert(0, str(SKILL))
    from scripts.python.quality.formatter_ast import build_ast_report_for_text
    modules = []
    for relative in ("rtl/road_csp_family_client.v", "tests/tb_csp_family_client.v"):
        path = ROOT / relative
        ast = build_ast_report_for_text(path.read_text(encoding="utf-8"), source_path=path)
        save(ROOT / (path.stem + "_ast.json"), ast)
        is_tb = path.stem.startswith("tb_")
        if is_tb:
            ports = [dict(name="o_test_complete", direction="output", width=1,
                          role="verification_completion", description="当前完整场景全部检查成功后置位")]
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
            parameters=[dict(name="C_FAMILY", default=3, description="合法常量3=CSP3，4=CSP4")],
            clock=dict(name=clock, edge="posedge", frequency_mhz=100),
            reset=dict(name=reset, active="low", synchronous=False), interfaces=dict(ports=ports),
            behavior=["C_FAMILY仅取3或4，对应冻结CSP3或CSP4，不是运行时任意图",
                      "七阶段按层完整遍历：三个DW/PW残差单元及最终PW融合",
                      "只有真实图像外补零；CSP4最后tile仅两行有效输出，禁止写物理padding行",
                      "16B单在途行缓存、完整tile输入复用、当前三输出通道权重驻留",
                      "原核组接口/II/数值保留；末次真实写、注册退休、整层可见性分别观察",
                      "共同复位取消全部端点，重新装SiLU；未证明独立取消排空"],
            constraints=["合法常量C_FAMILY为3或4；参数channel7/group4只是外围扩宽",
                         "同一套冻结算术、无私有MAC/SiLU/完整ROM",
                         "4ERAM为共同工作仓目标，容量不证明实际映射或端口时序",
                         "100M是整机1FPS预算，局部对拍不能证明整网FPS；过期500ms不改"],
            corner_cases=["CSP3完整36行、CSP4完整18行与末两行tile",
                          "DW三点/尾一点，PW24/48/96输入组，残差alias保持",
                          "随机反压稳定，错误参数/读地址/返回地址/屏障拒绝",
                          "共同复位强制装表、检查器真实acc错误负例"],
            verification_cases=["CSP3每次442368、CSP4每次221184阶段输出/中间值逐项一致",
                                "正常、随机、复位重跑和协议负例", "padding不写、源读/参数次数及周期账独立核验"],
            timing_diagrams=[dict(id="visible", title="完整层退休与下一层预取", scenario="barrier",
                description="省略其它任务；ready由外部写可见服务提供，不是固定等待拍数",
                wavejson=dict(signal=[dict(name=clock, wave="p..|......."),
                    dict(name="last_write_accept", wave="010|......."),
                    dict(name="registered_task_done", wave="001|0......"),
                    dict(name="layer_barrier_valid", wave="0..|0111100"),
                    dict(name="layer_visible_ready", wave="0..|0000100"),
                    dict(name="next_layer_prefetch", wave="0..|0000010")]))])
        modules.append(module)
        save(ROOT / (path.stem + "_contract.json"), dict(name="csp_family", modules=[module]))
    save(ROOT / "spec_contract.json", dict(name="csp_family", modules=modules,
        design_requirements=dict(parameter_constraints=[dict(id="fixed_family", expression="C_FAMILY == 3 or C_FAMILY == 4",
            message="只接受本次两种冻结图形状")])) )


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
    save(output / "command.json", dict(argv=argv, cwd=str(SKILL), returncode=result.returncode,
                                       log_sha256=digest(log)))
    if result.returncode not in (0,1) or not (output / "gate.json").is_file():
        raise RuntimeError("strict gate invocation/publication failed")
    report = read(output / "gate.json")
    print("STRICT_GATE", report["delivery_ready"], report["errors"], report["strict_warnings"], flush=True)


def prepare(name):
    if not re.fullmatch(r"frozen(?:_attempt[1-9][0-9]*)?", name):
        raise ValueError("fresh frozen candidate name required")
    target = ROOT / name
    if target.exists():
        raise ValueError("preserve existing candidate")
    previous = read(PRIOR / "frozen/input_binding.json")
    verify(previous["original_sha256"])
    verify(previous["staged_sha256"])
    reference = REFERENCE
    manifest = read(reference / "manifest.json")
    if manifest["payload_sha256"] != "b35d4a66a69e441dc29bc60c7e3f507661f48da5f33b810d7340f6ed17a65145":
        raise ValueError("reference uses another model")
    original = {str(reference / name): value for name, value in manifest["artifacts"].items()}
    for name, value in manifest["source_sha256"].items():
        path = Path(name)
        original[str(path if path.is_absolute() else PROJECT / path)] = value
    original[str(reference / "manifest.json")] = digest(reference / "manifest.json")
    original[str(PRIOR / "run.py")] = digest(PRIOR / "run.py")
    for module in CORES:
        path = PRIOR / "frozen/reused" / (module + ".v")
        original[str(path)] = previous["staged_sha256"][str(path)]
    for tool in ("vlib", "vlog", "vsim"):
        path = MODEL / (tool + ".exe")
        original[str(path)] = digest(path)
    for filename in ("ph1p_logic_eram.v", "ph1p_phy_gsr.v"):
        path = VENDOR / filename
        original[str(path)] = digest(path)
    for folder in ("rtl", "tests", "spec"):
        files = [p for p in (ROOT / folder).rglob("*") if p.is_file() and "__pycache__" not in p.parts]
        if not files:
            raise ValueError(f"missing {folder}")
        original.update({str(p): digest(p) for p in files})
    for filename in ("run.py", "requirements.txt", "tb_contract.json", "spec_contract.json"):
        original[str(ROOT / filename)] = digest(ROOT / filename)
    verify(original)
    target.mkdir()
    for folder in ("rtl", "tests", "spec"):
        shutil.copytree(ROOT / folder, target / folder, ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copytree(reference, target / "reference", ignore=shutil.ignore_patterns("__pycache__"))
    (target / "reused").mkdir()
    for module in CORES:
        shutil.copy2(PRIOR / "frozen/reused" / (module + ".v"), target / "reused")
    for filename in ("run.py", "requirements.txt", "tb_contract.json", "spec_contract.json"):
        shutil.copy2(ROOT / filename, target / filename)
    staged = {str(p): digest(p) for p in target.rglob("*") if p.is_file()}
    save(target / "input_binding.json", dict(original_sha256=original, staged_sha256=staged,
        prior_CSP2_original_sha256=previous["original_sha256"], prior_CSP2_staged_sha256=previous["staged_sha256"],
        payload_sha256=manifest["payload_sha256"], image_sha256=manifest["image_sha256"],
        arithmetic_changed=False, client_MAC_instances=0, actual_DDR=False,
        reference_revision=str(reference), first_reference_failure_preserved=True,
        upstream_prefix_CPU_only=True, production_delivery_ready=False))
    print("FROZEN", target, flush=True)


def execute(name, family, case, fault_kind):
    target = ROOT / name
    binding = read(target / "input_binding.json")
    for key in ("original_sha256", "staged_sha256", "prior_CSP2_original_sha256", "prior_CSP2_staged_sha256"):
        verify(binding[key])
    run = target / (f"family{family}_case{case}" + (f"_kind{fault_kind}" if case == 5 else ""))
    run.mkdir(exist_ok=False)
    records = []
    started = time.monotonic()

    def command(argv, filename):
        result = subprocess.run(list(map(str, argv)), cwd=run, capture_output=True, text=True,
                                encoding="utf-8", errors="replace", timeout=2400)
        content = result.stdout + result.stderr
        path = run / filename
        path.write_text(content, encoding="utf-8")
        effective = result.returncode or int(bool(re.search(r"\*\* (?:Error|Fatal):", content)))
        records.append(dict(argv=list(map(str, argv)), cwd=str(run), native_returncode=result.returncode,
                            validated_returncode=effective, log_sha256=digest(path)))
        save(run / "commands.json", records)
        return content, effective

    try:
        output, code = command([MODEL / "vlib.exe", "work"], "vlib.log")
        if code:
            raise RuntimeError("vlib failed")
        sources = [VENDOR / "ph1p_logic_eram.v", VENDOR / "ph1p_phy_gsr.v"]
        sources += [target / "reused" / (module + ".v") for module in CORES]
        sources += [target / "rtl/road_csp_family_client.v", target / "tests/tb_csp_family_client.v"]
        output, code = command([MODEL / "vlog.exe", "-work", "work", *sources], "compile.log")
        if code or re.findall(r"Errors:\s*(\d+),\s*Warnings:\s*(\d+)", output)[-1] != ("0", "0"):
            raise RuntimeError("compile not clean")
        negative = case == 99
        contract = read(target / "tb_contract.json")
        entries = [entry for entry in contract["runner_cases"] if entry["case"] == case and
                   (case != 5 or f"+FAULT_KIND={fault_kind}" in entry.get("plusargs", []))]
        if not negative and len(entries) != 1:
            raise ValueError("case contract not unique")
        entry = None if negative else entries[0]
        argv = [MODEL / "vsim.exe", "-c", "-lib", "work", "PH1P_PHY_GSR", "tb_csp_family_client",
                f"-gC_FAMILY={family}", f"+CASE={0 if negative else case}",
                f"+VECTORS={(target / 'reference' / f'csp{family}').as_posix()}",
                *(["+NEGATIVE_ACC=1"] if negative else entry.get("plusargs", [])),
                "-do", "run -all; quit -code 0"]
        print("RUN", family, case, fault_kind, flush=True)
        output, code = command(argv, "simulation.log")
        if negative:
            if not code or "NEGATIVE_ACC injected acc mismatch" not in output or "CSP_FAMILY_PASS" in output:
                raise AssertionError("real checker negative not rejected")
        else:
            if code:
                raise RuntimeError("simulation failed; preserved")
            markers = re.findall(r"CSP_FAMILY_(?:PASS|EXPECTED_FAULT) [^\r\n]*", output)
            if len(markers) != 1 or not markers[0].startswith(entry["marker"]):
                raise AssertionError("unique expected completion marker absent")
            values = {key: int(value) for key, value in re.findall(r"(\w+)=(\d+)", markers[0])}
            if values.get("family") != family or values.get("case") != case:
                raise AssertionError("wrong family/case receipt")
            expected = entry.get("expected_fields_by_family", {}).get(str(family), entry.get("expected_fields", {}))
            if any(values.get(key) != value for key, value in expected.items()):
                raise AssertionError("receipt differs from frozen case contract")
            if markers[0].startswith("CSP_FAMILY_PASS"):
                total = 442368 if family == 3 else 221184
                if any(values.get(key) != total for key in ("outputs", "acc", "pre", "silu", "post")):
                    raise AssertionError("full numerical coverage incomplete")
            save(run / "receipt.json", dict(marker=markers[0], fields=values,
                stage_ledger=re.findall(r"CSP_FAMILY_STAGE [^\r\n]*", output),
                state_ledger=re.findall(r"CSP_FAMILY_STATE [^\r\n]*", output),
                measured_runs=re.findall(r"CSP_FAMILY_RUN [^\r\n]*", output)))
        for key in ("original_sha256", "staged_sha256", "prior_CSP2_original_sha256", "prior_CSP2_staged_sha256"):
            verify(binding[key])
        save(run / "status.json", dict(status="PASS_REAL_CHECKER_NEGATIVE" if negative else "PASS_FUNCTION_CASE",
            family=family, case=case, seconds=time.monotonic()-started, upstream_prefix_CPU_only=True,
            arithmetic_changed=False, actual_DDR=False, synthesis=False, training_updates=0,
            production_delivery_ready=False))
        print("PASS", family, case, round(time.monotonic()-started, 2), flush=True)
    except BaseException as error:
        save(run / "status.json", dict(status="FAILED_PRESERVED", family=family, case=case, error=repr(error)))
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("preflight", "spec", "gate", "prepare", "execute"))
    parser.add_argument("--name", default="frozen")
    parser.add_argument("--family", type=int, choices=(3,4), default=3)
    parser.add_argument("--case", type=int, default=0)
    parser.add_argument("--fault-kind", type=int, choices=(0,1), default=0)
    args = parser.parse_args()
    if args.action == "preflight":
        preflight()
    elif args.action == "spec":
        spec()
    elif args.action == "gate":
        gate(args.name)
    elif args.action == "prepare":
        prepare(args.name)
    else:
        execute(args.name, args.family, args.case, args.fault_kind)
