"""封存CSP2逐层候选并运行有明确边界的本地功能仿真；不运行训练或TD。"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[3]
OLD = ROOT.parent / "csp2_complete_20261015"
SKILL = Path("C:/Users/lenovo/.codex/skills/readable-verilog-generator")
MODEL = Path("D:/modeltech64_2020.4/win64")
VENDOR = Path("E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/sim_release/ph1p")
CORES = ("road_csp_first_probe", "road_mac_probe", "road_dynamic_postprocess",
         "road_dynamic_requant", "road_round_shift", "silu_shared_unit")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def verify(hashes):
    for filename, expected in hashes.items():
        if digest(Path(filename)) != expected:
            raise ValueError(f"immutable input changed: {filename}")


def spec():
    """规格端口只读既有formatter AST，测试台单完成端口显式声明，不伪造解析成功。"""
    sys.path.insert(0, str(SKILL))
    from scripts.python.quality.formatter_ast import build_ast_report_for_text
    modules = []
    for relative in ("rtl/road_csp_layer_client.v", "tests/tb_csp_layer_client.v"):
        path = ROOT / relative
        ast = build_ast_report_for_text(path.read_text(encoding="utf-8"), source_path=path)
        save(ROOT / (path.stem + "_ast.json"), ast)
        is_tb = path.stem.startswith("tb_")
        if is_tb:
            ports = [dict(name="o_test_complete", direction="output", width=1,
                          role="verification_completion", description="完整当前场景检查成功后置位")]
        else:
            if ast["summary"]["parse_errors"] or len(ast["modules"]) != 1:
                raise ValueError("client formatter AST unavailable; do not infer ports")
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
            behavior=["一帧五阶段顺序全幅遍历，每个逻辑输出计算和写入一次",
                      "4x4输出tile，DW真实6x6输入；只有真实图像外补零",
                      "16B对齐逻辑读取与完整tile输入复用；当前输出组权重驻留",
                      "原核首末组、三路输出及signed9残差饱和完全保留",
                      "最后真实写、任务退休、整层写可见性屏障和done分别观察",
                      "共同复位取消所有端点并重新装表；不声称独立取消排空"],
            constraints=["无私有MAC；不更改真实PAXI；仅受控逻辑端点",
                         "缓存4ERAM只是容量目标，未综合/布局布线",
                         "8M首轮预算不是已达标结论；局部周期不证明整网1FPS或2FPS",
                         "graph字节地址只在唯一外部DDR边界转换一次"],
            corner_cases=["四边padding、DW尾一路、PW12输入尾四lane",
                          "随机请求/返回/核授予/写反压及载荷稳定",
                          "未可见中间值禁止读取；最后阶段屏障确认前不完成",
                          "错误读/参数身份拒绝，故意黄金acc错误必须失败"],
            verification_cases=["同真实图acc/pre/SiLU/post/sum/地址逐项检查663552值",
                                "正常全幅、随机反压全幅、共同复位再跑全幅", "协议拒绝与检查器负例"],
            timing_diagrams=[dict(id="layer", title="完整层可见性和下一层读取", scenario="barrier",
                description="中间省略所有tile；ready表示受控服务写可见，不是固定等待",
                wavejson=dict(signal=[dict(name=clock, wave="p..|......."),
                    dict(name="last_write_accept", wave="010|......."),
                    dict(name="task_retired", wave="001|0......"),
                    dict(name="layer_barrier_valid", wave="0..|0111100"),
                    dict(name="layer_visible_ready", wave="0..|0000100"),
                    dict(name="next_layer_prefetch", wave="0..|0000010")])),
                dict(id="read", title="16B单一未完成读取", scenario="read",
                description="请求/返回独立反压；地址为逻辑字节且16B对齐",
                wavejson=dict(signal=[dict(name=clock, wave="p........"),
                    dict(name="read_valid", wave="0110....."), dict(name="read_ready", wave="0010....."),
                    dict(name="response_valid", wave="0...110.."), dict(name="response_ready", wave="0....10.."),
                    dict(name="cached_byte_use", wave="0.....110")]))])
        modules.append(module)
        save(ROOT / (path.stem + "_contract.json"), dict(name="csp_layer", modules=[module]))
    save(ROOT / "spec_contract.json", dict(name="csp_layer", modules=modules))


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
    if result.returncode not in (0, 1) or not (output / "gate.json").is_file():
        raise RuntimeError("strict gate invocation failed")
    report = read(output / "gate.json")
    print("STRICT_GATE", report["delivery_ready"], "errors", report["errors"],
          "warnings", report["strict_warnings"], flush=True)


def prepare(name):
    if not re.fullmatch(r"frozen(?:_attempt[1-9][0-9]*)?", name):
        raise ValueError("fresh frozen candidate name required")
    target = ROOT / name
    if target.exists():
        raise ValueError("candidate already exists; preserve it")
    original = {}
    road = OLD / "reference/road_input"
    manifest = read(road / "manifest.json")
    for filename, expected in manifest["artifacts"].items():
        original[str(road / filename)] = expected
    original.update({str(PROJECT / k): v for k, v in manifest["source_sha256"].items()})
    original[str(road / "manifest.json")] = digest(road / "manifest.json")
    previous = OLD / "frozen_attempt2/reused"
    old_binding = read(OLD / "frozen_attempt2/input_binding.json")
    for module in CORES:
        path = previous / (module + ".v")
        expected = old_binding["staged_sha256"][str(path)]
        original[str(path)] = expected
    for name_of_tool in ("vlib", "vlog", "vsim"):
        path = MODEL / (name_of_tool + ".exe")
        original[str(path)] = digest(path)
    for filename in ("ph1p_logic_eram.v", "ph1p_phy_gsr.v"):
        path = VENDOR / filename
        original[str(path)] = digest(path)
    graph = ROOT.parent / "graph_artifacts/graph.json"
    original[str(graph)] = digest(graph)
    for folder in ("rtl", "tests", "spec"):
        files = [p for p in (ROOT / folder).rglob("*") if p.is_file()]
        if not files:
            raise ValueError(f"missing {folder}")
        original.update({str(p): digest(p) for p in files})
    for filename in ("run.py", "requirements.txt", "tb_contract.json", "spec_contract.json"):
        original[str(ROOT / filename)] = digest(ROOT / filename)
    verify(original)
    target.mkdir()
    for folder in ("rtl", "tests", "spec"):
        shutil.copytree(ROOT / folder, target / folder)
    shutil.copytree(road, target / "vectors", ignore=shutil.ignore_patterns("__pycache__"))
    (target / "reused").mkdir()
    for module in CORES:
        shutil.copy2(previous / (module + ".v"), target / "reused")
    for filename in ("run.py", "requirements.txt", "tb_contract.json", "spec_contract.json"):
        shutil.copy2(ROOT / filename, target / filename)
    shutil.copy2(graph, target / "graph.json")
    staged = {str(p): digest(p) for p in target.rglob("*") if p.is_file()}
    save(target / "input_binding.json", dict(original_sha256=original, staged_sha256=staged,
        payload_sha256=manifest["payload_sha256"], image_sha256=manifest["image_sha256"],
        private_MAC_instances=0, arithmetic_changed=False, actual_DDR=False,
        native_address_conversion=False, production_delivery_ready=False))
    print("FROZEN", target, flush=True)


def execute(name, case, fault_kind):
    target = ROOT / name
    binding = read(target / "input_binding.json")
    verify(binding["original_sha256"])
    verify(binding["staged_sha256"])
    run = target / (f"verification_case{case}" + (f"_kind{fault_kind}" if case == 5 else ""))
    run.mkdir(exist_ok=False)
    records = []
    started = time.monotonic()

    def command(argv, log_name):
        result = subprocess.run(list(map(str, argv)), cwd=run, capture_output=True, text=True,
                                encoding="utf-8", errors="replace", timeout=2400)
        content = result.stdout + result.stderr
        path = run / log_name
        path.write_text(content, encoding="utf-8")
        effective = result.returncode or int(bool(re.search(r"\*\* (?:Error|Fatal):", content)))
        records.append(dict(argv=list(map(str, argv)), cwd=str(run), native_returncode=result.returncode,
                            validated_returncode=effective, log_sha256=digest(path)))
        save(run / "commands.json", records)
        return content, effective

    try:
        content, code = command([MODEL / "vlib.exe", "work"], "vlib.log")
        if code:
            raise RuntimeError("vlib failed")
        sources = [VENDOR / "ph1p_logic_eram.v", VENDOR / "ph1p_phy_gsr.v"]
        sources += [target / "reused" / (module + ".v") for module in CORES]
        sources += [target / "rtl/road_csp_layer_client.v", target / "tests/tb_csp_layer_client.v"]
        content, code = command([MODEL / "vlog.exe", "-work", "work", *sources], "compile.log")
        if code or re.findall(r"Errors:\s*(\d+),\s*Warnings:\s*(\d+)", content)[-1] != ("0", "0"):
            raise RuntimeError("compile not clean; preserve diagnostics")
        negative = case == 99
        contract = read(target / "tb_contract.json")
        entries = [entry for entry in contract["runner_cases"] if entry["case"] == case and
                   (case != 5 or f"+FAULT_KIND={fault_kind}" in entry.get("plusargs", []))]
        if not negative and len(entries) != 1:
            raise ValueError("case is not uniquely bound by testbench contract")
        entry = None if negative else entries[0]
        argv = [MODEL / "vsim.exe", "-c", "-lib", "work", "PH1P_PHY_GSR", "tb_csp_layer_client",
                f"+CASE={0 if negative else case}", f"+VECTORS={(target / 'vectors').as_posix()}",
                *(["+NEGATIVE_ACC=1"] if negative else entry.get("plusargs", [])),
                "-do", "run -all; quit -code 0"]
        print("RUN_FULL_FRAME_OR_PROTOCOL_CASE", case, flush=True)
        content, code = command(argv, "simulation.log")
        if negative:
            if not code or "NEGATIVE_ACC injected acc mismatch" not in content or "CSP_LAYER_PASS" in content:
                raise AssertionError("real checker negative not rejected")
        else:
            if code:
                raise RuntimeError("simulation failed; preserve log")
            markers = re.findall(r"CSP_LAYER_(?:PASS|EXPECTED_FAULT) [^\r\n]*", content)
            if len(markers) != 1:
                raise AssertionError("unique completion receipt absent")
            fields = {k: int(v) for k, v in re.findall(r"(\w+)=(\d+)", markers[0])}
            if fields.get("case") != case:
                raise AssertionError("wrong case receipt")
            if not markers[0].startswith(entry["marker"]) or any(
                    fields.get(key) != value for key, value in entry.get("expected_fields", {}).items()):
                raise AssertionError("receipt does not match frozen testbench contract")
            if markers[0].startswith("CSP_LAYER_PASS"):
                if fields.get("outputs") != 663552 or any(fields.get(k) != 663552 for k in ("acc", "pre", "silu", "post")):
                    raise AssertionError("full-frame comparisons incomplete")
            save(run / "receipt.json", dict(marker=markers[0], fields=fields,
                stage_ledger=re.findall(r"CSP_LAYER_STAGE [^\r\n]*", content),
                state_ledger=re.findall(r"CSP_LAYER_STATE [^\r\n]*", content),
                measured_runs=re.findall(r"CSP_LAYER_RUN [^\r\n]*", content)))
        verify(binding["original_sha256"])
        verify(binding["staged_sha256"])
        save(run / "status.json", dict(status="PASS_REAL_CHECKER_NEGATIVE" if negative else "PASS_FUNCTION_CASE",
            case=case, seconds=time.monotonic()-started, arithmetic_changed=False,
            actual_DDR=False, TD=False, training_updates=0, production_delivery_ready=False))
        print("PASS", case, "seconds", round(time.monotonic()-started, 2), flush=True)
    except BaseException as error:
        save(run / "status.json", dict(status="FAILED_PRESERVED", error=repr(error), case=case))
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("spec", "prepare", "execute", "gate"))
    parser.add_argument("--name", default="frozen")
    parser.add_argument("--case", type=int, default=0)
    parser.add_argument("--fault-kind", type=int, choices=(0, 1), default=0)
    args = parser.parse_args()
    if args.action == "spec":
        spec()
    elif args.action == "gate":
        gate(args.name)
    elif args.action == "prepare":
        prepare(args.name)
    else:
        execute(args.name, args.case, args.fault_kind)
