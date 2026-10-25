"""完整CSP外围：只生成规格、封存输入并运行授权的本地ModelSim，不执行TD或训练。"""
import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
PRODUCTION = ROOT.parent
PROJECT = PRODUCTION.parents[2]
PRIOR = PRODUCTION / "reports/csp_tile_integrated_20261015_v2"
SKILL = Path("C:/Users/lenovo/.codex/skills/readable-verilog-generator")
MODEL = Path("D:/modeltech64_2020.4/win64")
VENDOR = Path("E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/sim_release/ph1p")
CORES = ("road_csp_first_probe", "road_mac_probe", "road_dynamic_postprocess",
         "road_dynamic_requant", "road_round_shift", "silu_shared_unit")
PAYLOAD = "b35d4a66a69e441dc29bc60c7e3f507661f48da5f33b810d7340f6ed17a65145"
SIM_DO = "run -all; quit -code 0"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def verify(hashes):
    for filename, expected in hashes.items():
        if digest(Path(filename)) != expected:
            raise ValueError(f"frozen source/input changed: {filename}")


def task_plan(y, x):
    """独立枚举固定图坐标；用于任务/写数量与真实halo的验收，不供应RTL完成。"""
    if not (0 <= y <= 68 and 0 <= x <= 124 and y % 4 == x % 4 == 0):
        raise ValueError("invalid fixed graph tile origin")
    stages = []
    for stage in range(5):
        extent = 6 if stage < 2 else 4
        dw = stage in (0, 2)
        tasks = outputs = groups = 0
        source_positions = set()
        for row in range(extent):
            for col in range(0, extent, 3 if dw else 1):
                sy, sx = y + row - (stage < 2), x + col - (stage < 2)
                for channel in range(12) if dw else range(0, 24 if stage == 4 else 12, 3):
                    coords = [(sy, sx + lane if dw else sx, channel if dw else channel + lane)
                              for lane in range(3) if (not dw or col + lane < extent)]
                    coords = [c for c in coords if 0 <= c[0] < 72 and 0 <= c[1] < 128]
                    if not coords:
                        continue
                    tasks += 1
                    outputs += len(coords)
                    groups += 3 if stage == 4 else 2
                    if dw:
                        for cy, cx, _ in coords:
                            source_positions.update((cy + dy, cx + dx) for dy in (-1, 0, 1)
                                                    for dx in (-1, 0, 1)
                                                    if 0 <= cy + dy < 72 and 0 <= cx + dx < 128)
        stages.append(dict(layer=stage, tasks=tasks, groups=groups, outputs=outputs,
                           real_spatial_sources=len(source_positions)))
    return dict(origin=[y, x], stages=stages,
                tasks=sum(s["tasks"] for s in stages), groups=sum(s["groups"] for s in stages),
                outputs=sum(s["outputs"] for s in stages))


def self_check():
    center = task_plan(32, 60)
    assert (center["tasks"], center["groups"], center["outputs"]) == (576, 1280, 1632)
    assert [s["outputs"] for s in center["stages"]] == [432, 432, 192, 192, 384]
    assert center["stages"][0]["real_spatial_sources"] == 64
    for y, x in ((0, 0), (0, 124), (68, 0), (68, 124)):
        corner = task_plan(y, x)
        assert (corner["tasks"], corner["groups"], corner["outputs"]) == (508, 1144, 1368)
        assert corner["stages"][0]["real_spatial_sources"] == 36
    for origin in ((1, 0), (0, 125), (-4, 0), (72, 0)):
        try:
            task_plan(*origin)
        except ValueError:
            continue
        raise AssertionError("invalid tile accepted")


def spec():
    """仅由既有formatter AST读取实际端口，再添加已确认行为与周期图。"""
    sys.path.insert(0, str(SKILL))
    from scripts.python.quality.formatter_ast import build_ast_report_for_text
    modules = []
    for relative in ("rtl/road_csp_complete_client.v", "tests/tb_csp_complete_client.v"):
        path = ROOT / relative
        ast = build_ast_report_for_text(path.read_text(encoding="utf-8"), source_path=path)
        save(ROOT / (path.stem + "_ast.json"), ast)
        # 只使用真实解析出的接口；formatter风格失败保留在AST与严格门，不伪装成通过。
        is_tb = path.stem.startswith("tb_")
        if is_tb:
            # 测试台契约明确只有一个完成端口；官方write-spec再与真实源码核对，未通过AST仍保留。
            module={"name":"tb_csp_complete_client"}
            ports=[dict(name="o_test_complete",direction="output",width=1,role="verification_completion",
                        description="所有当前场景检查完成后置位")]
        else:
            if ast["summary"]["parse_errors"] or len(ast["modules"]) != 1:
                raise ValueError(f"formatter AST unavailable: {relative}")
            module = ast["modules"][0]
            ports = []
            for port in module["ports"]:
                width = port["width"]
                high, low = map(int, width[1:-1].split(":")) if width else (0, 0)
                ports.append(dict(name=port["name"], direction=port["direction"], width=abs(high-low)+1,
                                  role="native", description=port["comment"]))
        clock, reset = ("clk", "rstn") if is_tb else ("i_clk", "i_rstn")
        modules.append(dict(name=module["name"], rtl_path=relative,
            clock=dict(name=clock, edge="posedge", frequency_mhz=100),
            reset=dict(name=reset, active="low", synchronous=False), interfaces=dict(ports=ports),
            behavior=["五阶段固定图调度：DW0、PW0加残差、DW1、PW1加残差、PW融合",
                      "第一残差6x6真实邻域支持第二残差4x4输出；仅全幅图像外padding",
                      "无私有算术实例，valid/ready组与现算术核保持兼容",
                      "末次真实写、注册task_done、层可见性屏障是不同事件",
                      "共同复位取消所有参与服务；取消故障不释放存储，不能用于独立CNN取消"],
            constraints=["逻辑字节服务/参数端口为外围提案，未接真实DDR或ROM reader",
                         "未修改共享算术核接口、II、数值或生产工程；非部署交付"],
            corner_cases=["全幅四边及尾输入/输出lane", "组间参数漂移、错地址/错tag/重复写拒绝",
                          "参数、读、写背压稳定", "共同复位后重新装表", "层屏障错身份拒绝"],
            verification_cases=["同包acc/pre/SiLU/post/sum/output/address逐项比较",
                                "四角四边内部与连续不同tile", "各阶段复位及协议负例", "检查器故意错误期望负例"],
            timing_diagrams=[dict(id="retire", title="末次真实写与阶段可见性", scenario="barrier",
                description="竖线省略其它任务和算术延迟；屏障等待没有固定拍数保证",
                wavejson=dict(signal=[dict(name=clock, wave="p..|......."),
                    dict(name="last_write_accept", wave="010|......."),
                    dict(name="registered_task_done", wave="001|0......"),
                    dict(name="barrier_valid", wave="0..|0111100"),
                    dict(name="barrier_ready_visible", wave="0..|0000100"),
                    dict(name="next_layer_or_done", wave="0..|0000010")]))]))
    save(ROOT / "spec_contract.json", dict(name="csp_complete_client", modules=modules))
    for module in modules:
        save(ROOT / (module["name"]+"_contract.json"),dict(name="csp_complete_client",modules=[module]))


def gate(name):
    """严格公开门独立保存；失败不能由真实仿真或旧物理报告清除。"""
    target=ROOT/name
    output=target/"static_gate"
    output.mkdir(exist_ok=False)
    command=[sys.executable,"-B","-m","scripts.python.validation.generated_deliverable_gate",str(target),
             "--include-testbench","--spec",str(target/"spec_contract.json"),
             "--json",str(output/"gate.json"),"--markdown",str(output/"gate.md")]
    result=subprocess.run(command,cwd=SKILL,capture_output=True,text=True,encoding="utf-8",errors="replace",timeout=180)
    (output/"run.log").write_text(result.stdout+result.stderr,encoding="utf-8")
    save(output/"command.json",dict(argv=command,cwd=str(SKILL),returncode=result.returncode,
                                  log_sha256=digest(output/"run.log")))
    if result.returncode not in (0,1) or not (output/"gate.json").is_file():
        raise RuntimeError("strict gate invocation/publication failed")
    report=read(output/"gate.json")
    print("STRICT_GATE",report["delivery_ready"],"errors",report["errors"],"warnings",report["strict_warnings"],flush=True)


def prepare(name):
    self_check()
    target = ROOT / name
    if not re.fullmatch(r"frozen(?:_attempt[1-9][0-9]*)?", name):
        raise ValueError("fresh named frozen candidate required")
    physical = read(PRIOR / "physical_final_checks.json")
    if not physical["internal_setup_hold_pass"]:
        raise ValueError("prior candidate not the effective physical closure")
    binding = read(PRIOR / "input_binding.json")
    hashes = {}
    for module in CORES:
        path = PRIOR / "reused" / (module + ".v")
        if binding["staged_sha256"][str(path)] != digest(path):
            raise ValueError(f"effective frozen core changed: {module}")
        hashes[str(path)] = digest(path)
    package = PROJECT / "cnn/reports/qat_frozen_stem_g10_20261014_v1/package"
    if digest(package / "numeric_test.bin") != PAYLOAD:
        raise ValueError("selected payload changed")
    reference = read(ROOT / "reference/manifest.json")
    if reference["package_payload_sha256"] != PAYLOAD:
        raise ValueError("reference uses a different model")
    hashes.update({str(ROOT / "reference" / name): expected
                   for name, expected in reference["artifacts"].items()})
    hashes.update({str(PROJECT / name): expected
                   for name, expected in reference["source_files"].items()})
    hashes.update({str(package / name): expected
                   for name, expected in reference["package_files"].items()})
    verify(hashes)
    hashes.update({str(package / name): digest(package / name)
                   for name in ("manifest.json", "numeric_test.bin", "numeric_test_padded.bin")})
    for folder in ("rtl", "tests", "reference", "spec"):
        files = [p for p in (ROOT / folder).rglob("*") if p.is_file() and "__pycache__" not in p.parts]
        if not files:
            raise ValueError(f"missing candidate assets: {folder}")
        hashes.update({str(p): digest(p) for p in files})
    hashes.update({str(ROOT / file): digest(ROOT / file)
                   for file in ("run.py", "requirements.txt", "spec_contract.json", "tb_contract.json")})
    for name in ("ph1p_logic_eram.v", "ph1p_phy_gsr.v"):
        hashes[str(VENDOR / name)] = digest(VENDOR / name)
    for name in ("vlib", "vlog", "vsim"):
        hashes[str(MODEL / (name + ".exe"))] = digest(MODEL / (name + ".exe"))
    verify(hashes)
    target.mkdir(exist_ok=False)
    for folder in ("rtl", "tests", "reference", "spec"):
        shutil.copytree(ROOT / folder, target / folder, ignore=shutil.ignore_patterns("__pycache__"))
    (target / "reused").mkdir()
    for module in CORES:
        shutil.copy2(PRIOR / "reused" / (module + ".v"), target / "reused")
    for filename in ("run.py", "requirements.txt", "spec_contract.json", "tb_contract.json"):
        shutil.copy2(ROOT / filename, target / filename)
    staged = {str(p): digest(p) for p in target.rglob("*") if p.is_file()}
    save(target / "input_binding.json", dict(original_sha256=hashes, staged_sha256=staged,
         payload_sha256=PAYLOAD, arithmetic_unchanged=True,
         arithmetic_instances_in_client=0, single_arithmetic_in_testbench=True,
         actual_DDR=False, board=False, production_delivery_ready=False))
    save(target / "task_plan.json", dict(cases=[task_plan(y,x) for y in (0,32,68) for x in (0,60,124)]))
    save(target / "status.json", dict(status="PREPARED_NOT_EXECUTED", production_delivery_ready=False))
    print("FROZEN", target, flush=True)


def execute(name, only_case=None):
    target = ROOT / name
    binding = read(target / "input_binding.json")
    verify(binding["original_sha256"])
    verify(binding["staged_sha256"])
    run = target / ("verification" if only_case is None else f"verification_case{only_case}")
    run.mkdir(exist_ok=False)
    commands, receipts = [], []
    started = time.monotonic()
    def command(args, filename, negative=False):
        record = dict(argv=list(map(str,args)), cwd=str(run), executable_sha256=digest(Path(args[0])))
        commands.append(record)
        result = subprocess.run(record["argv"], cwd=run, capture_output=True, text=True,
                                encoding="utf-8", errors="replace", timeout=300)
        content = result.stdout + result.stderr
        (run / filename).write_text(content, encoding="utf-8")
        # ModelSim可能在$fatal后执行quit -code 0；真实Fatal/Error必须统一转换为验证失败。
        effective_exit=result.returncode or int(bool(re.search(r"\*\* (?:Error|Fatal):",content)))
        record.update(returncode=result.returncode,validated_returncode=effective_exit,log_sha256=digest(run / filename))
        save(run / "commands.json", commands)
        if negative:
            if effective_exit == 0 or "** Fatal: NEGATIVE_ACC injected acc mismatch" not in content or "CSP_COMPLETE_PASS" in content:
                raise AssertionError("checker negative not rejected by intended accumulator check")
        elif result.returncode or re.search(r"\*\* (?:Error|Fatal):", content):
            raise RuntimeError(f"ModelSim failure; preserved {run / filename}")
        return content
    try:
        command([MODEL / "vlib.exe", "work"], "vlib.log")
        sources = [VENDOR / "ph1p_logic_eram.v", VENDOR / "ph1p_phy_gsr.v"]
        sources += [target / "reused" / (module+".v") for module in CORES]
        sources += [target / "rtl/road_csp_complete_client.v", target / "tests/tb_csp_complete_client.v"]
        output = command([MODEL / "vlog.exe", "-work", "work", *sources], "compile.log")
        if re.findall(r"Errors:\s*(\d+),\s*Warnings:\s*(\d+)", output)[-1] != ("0", "0"):
            raise AssertionError("ModelSim compilation not warning-free")
        contract = read(target / "tb_contract.json")
        cases = contract["runner_cases"]
        if only_case is not None:
            cases = [c for c in cases if c["case"] == only_case]
            if not cases:
                raise ValueError("requested case absent")
        for index, entry in enumerate(cases):
            args = [MODEL / "vsim.exe", "-c", "-lib", "work", "PH1P_PHY_GSR", "tb_csp_complete_client",
                    f"+CASE={entry['case']}", f"+VECTORS={(target/'reference').as_posix()}", *entry.get("plusargs", []),
                    "-do", SIM_DO]
            print("RUN", index, entry, flush=True)
            output = command(args, f"case_{index}.log")
            markers = re.findall(r"CSP_COMPLETE_(?:PASS|EXPECTED_FAULT) [^\r\n]*", output)
            if len(markers) != 1:
                raise AssertionError("missing unique completion receipt")
            fields = {key:int(value) for key,value in re.findall(r"(\w+)=(\d+)", markers[0])}
            expected_marker = entry.get("marker", "CSP_COMPLETE_EXPECTED_FAULT" if entry["case"] in (13,14,15,16,18) else "CSP_COMPLETE_PASS")
            if not markers[0].startswith(expected_marker) or fields.get("case") != entry["case"]:
                raise AssertionError("wrong case/status marker")
            for key, value in entry.get("expected_fields", {}).items():
                if fields.get(key) != value:
                    raise AssertionError(f"receipt mismatch {key}: {fields.get(key)} != {value}")
            if expected_marker.endswith("PASS") and not (fields.get("outputs",0)>0 and
                all(fields.get(key)==fields["outputs"] for key in ("acc","pre","silu","post"))):
                raise AssertionError("empty or incomplete numerical checks")
            receipts.append(dict(case=entry, receipt=markers[0], fields=fields,
                                 measured_runs=re.findall(r"CSP_COMPLETE_RUN [^\r\n]*", output)))
            save(run / "case_receipts.json", receipts)
        if only_case is None:
            args=[MODEL/"vsim.exe", "-c", "-lib", "work", "PH1P_PHY_GSR", "tb_csp_complete_client",
                  "+CASE=4", "+NEGATIVE_ACC=1", f"+VECTORS={(target/'reference').as_posix()}",
                  "-do", SIM_DO]
            command(args, "checker_negative.log", negative=True)
        verify(binding["original_sha256"])
        verify(binding["staged_sha256"])
        save(run / "status.json", dict(status="PASS_COMPLETE_CSP_TILE_FUNCTION_NOT_INTEGRATED",
            cases=len(receipts), seconds=time.monotonic()-started, compile_errors=0, compile_warnings=0,
            arithmetic_unchanged=True, private_arithmetic_in_client=False, five_convolutions=True,
            two_residuals=True, concat_and_final_fusion=True, true_halo=True,
            checker_negative_executed=only_case is None, actual_DDR=False, full_CSP2_frame_traversal=False,
            synthesis=False, timing=False, strict_delivery=False, training_updates=0,
            production_delivery_ready=False, source_hashes_unchanged=True))
        print("PASS_COMPLETE_CSP_TILE_FUNCTION_NOT_INTEGRATED", flush=True)
    except BaseException as error:
        save(run / "status.json", dict(status="FAILED_PRESERVED", error=repr(error), cases=receipts,
                                      production_delivery_ready=False))
        raise


def verify_exit(name):
    """只复测启动器的正反例；保留已经完成的28项数值收据和失败状态，不重复整套。"""
    target=ROOT/name
    binding=read(target/"input_binding.json")
    old_launcher=str(ROOT/"run.py")
    verify({key:value for key,value in binding["original_sha256"].items() if key!=old_launcher})
    verify(binding["staged_sha256"])
    if digest(target/"run.py")!=binding["original_sha256"][old_launcher]:
        raise ValueError("old launcher's immutable baseline changed")
    receipts=read(target/"verification/case_receipts.json")
    if len(receipts)!=len(read(target/"tb_contract.json")["runner_cases"]):
        raise ValueError("numerical suite incomplete; cannot repair only exit translation")
    output=target/"verification_exit_attempt3"
    output.mkdir(exist_ok=False)
    records=[]
    for negative in (False,True):
        argv=[MODEL/"vsim.exe","-c","-lib","work","PH1P_PHY_GSR","tb_csp_complete_client",
              "+CASE=4",f"+VECTORS={(target/'reference').as_posix()}",
              *(["+NEGATIVE_ACC=1"] if negative else []),"-do",SIM_DO]
        result=subprocess.run(list(map(str,argv)),cwd=target/"verification",capture_output=True,text=True,encoding="utf-8",errors="replace",timeout=300)
        content=result.stdout+result.stderr
        path=output/("negative.log" if negative else "positive.log")
        path.write_text(content,encoding="utf-8")
        effective_exit=result.returncode or int(bool(re.search(r"\*\* (?:Error|Fatal):",content)))
        records.append(dict(negative=negative,argv=list(map(str,argv)),cwd=str(target/"verification"),returncode=result.returncode,
                            validated_returncode=effective_exit,
                            log_sha256=digest(path),executable_sha256=digest(MODEL/"vsim.exe")))
        save(output/"commands.json",records)
        if negative:
            assert effective_exit!=0 and "** Fatal: NEGATIVE_ACC injected acc mismatch" in content
            assert "CSP_COMPLETE_PASS" not in content
        else:
            assert effective_exit==0 and "CSP_COMPLETE_PASS case=4" in content
            assert not re.search(r"\*\* (?:Error|Fatal):",content)
    verify({key:value for key,value in binding["original_sha256"].items() if key!=old_launcher})
    verify(binding["staged_sha256"])
    save(output/"receipt.json",dict(status="PASS_EXIT_TRANSLATION_POSITIVE_AND_REAL_NEGATIVE",
         actual_positive_cases_already_completed=len(receipts),old_launcher_sha256=digest(target/"run.py"),
         corrected_launcher_sha256=digest(Path(__file__)),original_except_launcher_unchanged=True,
         staged_inputs_unchanged=True,RTL_or_numeric_changed=False,commands=records,
         prior_failed_negative_preserved="../verification/checker_negative.log",
         production_delivery_ready=False))
    print("PASS_EXIT_TRANSLATION_POSITIVE_AND_REAL_NEGATIVE",flush=True)


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("self-check", "spec", "prepare", "execute", "gate", "verify-exit"))
    parser.add_argument("--name", default="frozen")
    parser.add_argument("--case", type=int)
    args=parser.parse_args()
    if args.action=="self-check":
        self_check()
        print("SCHEDULING_REFERENCE_SELF_CHECK_PASS")
    elif args.action=="spec":
        spec()
    elif args.action=="prepare":
        prepare(args.name)
    elif args.action=="gate":
        gate(args.name)
    elif args.action=="verify-exit":
        verify_exit(args.name)
    else:
        execute(args.name, args.case)
