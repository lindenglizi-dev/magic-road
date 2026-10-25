"""仅本owner目录的参考、canonical规格、不可变快照与真实ModelSim验证。"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import random
import re
import shutil
import subprocess
import sys
from datetime import datetime

from reference import ROOT, FROZEN, TABLE, evaluate, self_check

SKILL = Path("C:/Users/lenovo/.codex/skills/readable-verilog-generator")
MODEL = Path("D:/modeltech64_2020.4/win64")
VENDOR = Path("E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/sim_release/ph1p")
CORES = ["road_mac_probe", "road_dynamic_postprocess", "road_dynamic_requant", "road_round_shift", "silu_shared_unit"]
PORTS = [
    ("i_clk",1,"同域100MHz时钟"),("i_rstn",1,"所有原核共同低有效异步复位"),
    ("i_table_valid",1,"空闲表项保持有效"),("i_table_addr",10,"原表严格递增装载地址"),("i_table_data",16,"原模型有符号Q7.8表项"),
    ("i_input_valid",1,"八输入组保持到真实握手"),("i_first",1,"仅首组开启归约并锁存元数据"),("i_last",1,"当前组关闭归约"),
    ("i_lane_mask",8,"八输入槽使能"),("i_activation_data",64,"低字节优先八个INT8"),("i_weight_data",192,"三路各八个INT8权重"),("i_bias_data",96,"原MAC只在first使用三路INT32偏置"),
    ("i_output_mask",3,"首组锁存三路输出有效位"),("i_tags",48,"首组锁存不透明输出身份"),("i_addresses",96,"首组锁存三路写地址"),
    ("i_pre_multipliers",96,"首组锁存三路前乘数"),("i_pre_shifts",18,"首组锁存三路前移位"),("i_post_multiplier",32,"首组锁存共享后乘数"),("i_post_shift",6,"首组锁存共享后移位"),
    ("i_activate",1,"首组选择SiLU INT8或raw INT16"),("i_input_fault",1,"任务错误转为保持故障"),("i_output_ready",1,"唯一写端实际退休许可"),
    ("o_table_ready",1,"空闲且原DPP接受表项"),("o_table_loaded",1,"原核完整表装载状态"),("o_input_ready",1,"归约输入组接纳许可"),
    ("o_output_valid",1,"匹配身份和类型的完整输出有效"),("o_output_data",16,"激活符号扩展INT8或raw INT16"),("o_output_int16",1,"等于首组activate反值"),("o_output_tag",16,"与数据同生存期身份"),("o_output_address",32,"身份所选锁存写地址"),
    ("o_fault",1,"元数据或核故障粘滞"),("o_busy",1,"首组到末输出退休或故障保持")]


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, value):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def command(argv, cwd, output):
    temporary = ROOT / "runtime_tmp"
    temporary.mkdir(exist_ok=True)
    result = subprocess.run(list(map(str, argv)), cwd=cwd, env=dict(os.environ, TEMP=str(temporary), TMP=str(temporary), PYTHONPATH=str(SKILL)),
                            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=240)
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    Path(output).write_text(result.stdout + result.stderr, encoding="utf-8")
    effective = result.returncode or int(bool(re.search(r"\*\* (?:Error|Fatal):", result.stdout + result.stderr)))
    save(str(output) + ".command.json", dict(argv=list(map(str, argv)), cwd=str(cwd), native_returncode=result.returncode, validated_returncode=effective, log_sha256=digest(output)))
    return result.stdout + result.stderr, effective


def contract():
    module = dict(name="road_standard_arithmetic_owner", rtl_path="rtl/road_standard_arithmetic_owner.v",
        clock=dict(name="i_clk", edge="posedge", frequency_mhz=100), reset=dict(name="i_rstn", active="low", synchronous=False),
        interfaces=dict(ports=[dict(name=n, direction="input" if n.startswith("i_") else "output", width=w, role="native", description=d) for n,w,d in PORTS]),
        behavior=["单任务IDLE/GROUP/ACC/OUTPUT/FAULT三段状态机", "首组锁存mask/tags/address/pre/post/activate，后续元数据变化忽略",
                  "ACC只向原DPP提交一次完整MAC结果", "最后有效lane真实输出握手后才能解除busy；故障必须共同复位", "输出直接采用原DPP保持槽，owner没有结果array或residual"],
        constraints=["原五核端口、II、复位、算术均不改", "所有核同域共同reset；两拍owner准入释放，最早第三沿接收", "每路最多192乘积/24组由现固定客户端保证", "接口无帧号；外部调度负责完整任务身份与DDR可见性"],
        corner_cases=["mask1/3/7、opaque唯一tags、错误/重复身份与错误类型", "激活输出必须INT8符号扩展；raw保留完整INT16", "末输出背压不释放，table只在idle接受", "reset取消原核和元数据，SiLU必须重新装满"],
        verification_cases=["整数参考逐MAC/pre/SiLU/post/final值", "真实ModelSim原核和原SiLU1024表", "多组bias一次、尾mask、首组锁存扰动", "GROUP/ACC/OUTPUT共同复位和故障保持"],
        timing_diagrams=[dict(id="retirement", title="仅最后真实输出退休释放", scenario="retirement", description="省略原核计算拍，输出反压保持身份，MAC交接不释放owner", wavejson=dict(signal=[
            dict(name="i_clk",wave="p..|......"),dict(name="first_accept",wave="010|000000"),dict(name="mac_to_dpp",wave="000|100000"),
            dict(name="output_valid",wave="000|011110"),dict(name="output_ready",wave="000|001010"),dict(name="remaining",wave=".=.|..=.=.",data=["3","2","0"]),dict(name="busy",wave="0.1|111100")]))])
    save(ROOT / "spec_contract.json", dict(name="owner", modules=[module]))
    arguments=[sys.executable,"-B","-m","scripts.python.workflow.cli","write-spec","--spec",ROOT/"spec_contract.json","--out-dir",ROOT,"--language","zh"]
    if (ROOT/"rtl/road_standard_arithmetic_owner.v").is_file():
        arguments += ["--source",ROOT/"rtl/road_standard_arithmetic_owner.v"]
    log, code = command(arguments,ROOT,ROOT/"spec_render.log")
    if code:
        raise RuntimeError(log)
    if (ROOT/"rtl").is_dir():
        shutil.copy2(ROOT/"spec/road_standard_arithmetic_owner_spec.md",ROOT/"rtl")
    if (ROOT/"tests/tb_standard_arithmetic_owner.v").is_file():
        tb=json.loads(json.dumps(module))
        tb.update(name="tb_standard_arithmetic_owner",rtl_path="tests/tb_standard_arithmetic_owner.v",clock=dict(name="clk",edge="posedge",frequency_mhz=100),reset=dict(name="rstn",active="low",synchronous=False),interfaces=dict(ports=[dict(name="o_test_complete",direction="output",width=1,role="verification_completion",description="全部断言完成后结束")]))
        tb["behavior"]=["加载冻结Python数值向量与原SiLU1024表", "CASE0运行12任务并逐ACC/PRE/SiLU/POST/final对拍", "CASE1/2/3在GROUP/ACC/OUTPUT共同reset后重装表恢复", "CASE10..19/21检查身份类型、首组协议与核错误的sticky故障", "CASE99真实修改ACC期望值一位，原数值checker必须报错而非PASS"]
        tb["constraints"]=["仅仿真夹具，非可综合设计；force仅用于输出损坏负例", "不测ROM7168、TD、DDR、整网或板卡"]
        tb["timing_diagrams"][0]["wavejson"]["signal"][0]["name"]="clk"
        save(ROOT/"tb_contract.json",dict(name="owner_tests",modules=[tb]))
        log,code=command([sys.executable,"-B","-m","scripts.python.workflow.cli","write-spec","--spec",ROOT/"tb_contract.json","--out-dir",ROOT,"--language","zh"],ROOT,ROOT/"tb_spec_render.log")
        if code: raise RuntimeError(log)
        shutil.copy2(ROOT/"spec/tests/tb_standard_arithmetic_owner_spec.md",ROOT/"tests")


def vectors():
    table = self_check()
    rng = random.Random(20261016)
    data = {k: [] for k in ("mask","activate","groups","bias","mul","shift","postmul","postshift","activation","weight","lanemask","acc","pre","silu","post","output")}
    def pack(values, width):
        return sum((v & ((1 << width)-1)) << (i * width) for i,v in enumerate(values))
    details = []
    for task in range(12):
        activate = task % 2
        mask = (1,3,7)[task % 3]
        count = 1 + task % 4
        bias = [-80000+task, 80000-task, -513+task] if task < 6 else [rng.randrange(-3000,3001) for _ in range(3)]
        mul, shift = ([1,3,5], [0,1,2]) if not activate else ([1,3,5],[5,6,7])
        postmul, postshift = 3, 5
        groups = []
        for group in range(4):
            a = [rng.randrange(-128,128) for _ in range(8)]
            w = [[rng.randrange(-128,128) for _ in range(8)] for _ in range(3)]
            lm = 0x1f if group == count-1 and count > 1 else 0xff
            data["activation"].append(pack(a,8)); data["weight"].append(pack(sum(w,[]),8)); data["lanemask"].append(lm)
            if group < count:
                groups.append((a,w,lm))
        result = evaluate(groups,bias,mul,shift,postmul,postshift,activate,table)
        for key,value in (("mask",mask),("activate",activate),("groups",count),("bias",pack(bias,32)),("mul",pack(mul,32)),("shift",pack(shift,6)),("postmul",postmul),("postshift",postshift)):
            data[key].append(value)
        for key in ("acc","pre","silu","post","output"):
            data[key].extend(result[key] if result[key] else [0,0,0])
        details.append(dict(task=task,activate=activate,mask=mask,groups=count,intermediate=result))
    target = ROOT / "vectors"
    target.mkdir(exist_ok=True)
    widths=dict(mask=1,activate=1,groups=1,bias=24,mul=24,shift=5,postmul=8,postshift=2,activation=16,weight=48,lanemask=2,acc=8,pre=4,silu=4,post=4,output=4)
    for key, values in data.items():
        bits = widths[key]*4
        filename = "activation_expected" if key == "silu" else key
        (target / (filename+".hex")).write_text("".join(f"{v & ((1 << bits)-1):0{widths[key]}x}\n" for v in values),encoding="ascii")
    shutil.copy2(TABLE,target/"silu.hex")
    save(target/"cases.json", details)
    save(target/"source_receipt.json",dict(table=str(TABLE),table_sha256=digest(TABLE),frozen_contract=str(FROZEN/"reference/csp2/contract.json"),contract_sha256=digest(FROZEN/"reference/csp2/contract.json"),seed=20261016,full_rom_sweep=False))


def simulate(case):
    target = ROOT / "runs" / (datetime.now().strftime("%Y%m%d_%H%M%S_%f")+f"_case{case}")
    target.mkdir(parents=True)
    for folder in ("rtl","tests","vectors","spec"):
        shutil.copytree(ROOT/folder,target/folder)
    for name in ("run.py","reference.py","requirements.json","codegen_plan.txt","spec_contract.json"):
        shutil.copy2(ROOT/name,target/name)
    (target/"reused").mkdir()
    for name in CORES:
        shutil.copy2(FROZEN/"reused"/(name+".v"),target/"reused")
    (target/"vendor").mkdir()
    for name in ("ph1p_logic_eram.v","ph1p_phy_gsr.v"):
        shutil.copy2(VENDOR/name,target/"vendor")
    inputs={str(p.relative_to(target)):digest(p) for p in target.rglob("*") if p.is_file()}
    tools={str(MODEL/(name+".exe")):digest(MODEL/(name+".exe")) for name in ("vlib","vlog","vsim")}
    save(target/"binding.json",dict(source_vector_sha256=inputs,tool_sha256=tools,frozen_sources={str(FROZEN/"reused"/(n+".v")):digest(FROZEN/"reused"/(n+".v")) for n in CORES},table_sha256=digest(TABLE)))
    try:
        log,code=command([MODEL/"vlib.exe","work"],target,target/"vlib.log")
        if code: raise RuntimeError("vlib failed")
        sources=[target/"vendor/ph1p_logic_eram.v",target/"vendor/ph1p_phy_gsr.v"]+[target/"reused"/(n+".v") for n in CORES]+[target/"rtl/road_standard_arithmetic_owner.v",target/"tests/tb_standard_arithmetic_owner.v"]
        log,code=command([MODEL/"vlog.exe","-work","work",*sources],target,target/"compile.log")
        if code or not re.search(r"Errors: 0, Warnings: 0",log): raise RuntimeError("compile failed or warnings")
        log,code=command([MODEL/"vsim.exe","-c","-lib","work","PH1P_PHY_GSR","tb_standard_arithmetic_owner",f"+CASE={case}",f"+VECTORS={(target/'vectors').as_posix()}","-do","run -all; quit -code 0"],target,target/"simulation.log")
        if case == 99:
            assert code and "OWNER_FAIL injected numerical mismatch" in log and "OWNER_PASS" not in log
        else:
            assert not code and len(re.findall(r"OWNER_PASS [^\r\n]+",log)) == 1, log[-2000:]
        assert all(digest(target/p)==value for p,value in inputs.items())
        assert all(digest(path)==value for path,value in tools.items())
        save(target/"status.json",dict(status="PASS_CHECKER_NEGATIVE" if case==99 else "PASS_FUNCTION",case=case,markers=re.findall(r"OWNER_PASS [^\r\n]+",log),actual_ModelSim=True,TD=False,board=False,full_graph=False,full_ROM_sweep=False))
    except BaseException as error:
        save(target/"status.json",dict(status="FAILED_PRESERVED",case=case,error=repr(error)))
        raise
    print(target,flush=True)


def gate():
    target=ROOT/"gates"/datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    log,code=command([sys.executable,"-B","-m","scripts.python.validation.generated_deliverable_gate",ROOT/"rtl/road_standard_arithmetic_owner.v","--spec",ROOT/"spec_contract.json","--external-interface-source",FROZEN/"reused","--json",target/"gate.json","--markdown",target/"gate.md"],SKILL,target/"run.log")
    print(target, "exit",code,flush=True)


def report():
    owner_hash=digest(ROOT/"rtl/road_standard_arithmetic_owner.v")
    cases={}
    for path in sorted((ROOT/"runs").glob("*/status.json")):
        status=json.loads(path.read_text(encoding="utf-8"))
        binding=json.loads((path.parent/"binding.json").read_text(encoding="utf-8"))
        source_hashes={key.replace("\\","/"):value for key,value in binding["source_vector_sha256"].items()}
        if status["status"].startswith("PASS") and source_hashes["rtl/road_standard_arithmetic_owner.v"]==owner_hash:
            cases[status["case"]]=dict(run=str(path.parent),status=status["status"],status_sha256=digest(path),binding_sha256=digest(path.parent/"binding.json"),markers=status["markers"])
    gate_path=sorted((ROOT/"gates").glob("*/gate.json"))[-1]
    gate=json.loads(gate_path.read_text(encoding="utf-8"))
    selected=ROOT/"runs/20261016_013711_704214_case0"
    assert digest(selected/"rtl/road_standard_arithmetic_owner.v")==owner_hash
    frozen_contract=json.loads((FROZEN/"reference/csp2/contract.json").read_text(encoding="utf-8"))
    assert digest(TABLE)==frozen_contract["files"]["parameters"]["parameters/silu.hex"]
    assert digest(selected/"vectors/silu.hex")==digest(TABLE)
    assert set(cases)=={0,1,2,3,10,11,12,13,14,15,16,17,18,19,21,99}
    assert all(digest(path)==value for path,value in json.loads((selected/"binding.json").read_text(encoding="utf-8"))["frozen_sources"].items())
    save(ROOT/"handoff.json",dict(qualified_owner=str(selected/"rtl/road_standard_arithmetic_owner.v"),owner_sha256=owner_hash,live_source_same_hash=True,source_bound_spec=str(ROOT/"rtl/road_standard_arithmetic_owner_spec.md"),cases=cases,
        strict_gate=dict(path=str(gate_path),sha256=digest(gate_path),delivery_ready=gate["delivery_ready"],errors=gate["errors"],strict_warnings=gate["strict_warnings"],checks=gate["checks"]),
        tools=dict(python=str(Path(sys.executable)),python_sha256=digest(sys.executable)),silu_table_matches_frozen_contract=True,
        formatter_diagnostic_only=True,frozen_kernels_modified=False,physical_TD=False,DDR=False,full_graph=False,production=False))
    print("OWNER_HANDOFF",owner_hash,"cases",len(cases),"strict_ready",gate["delivery_ready"])


def format():
    from scripts.python.quality.formatter_ast import normalize_text_with_formatter_ast, create_formatter_backend
    source=ROOT/"rtl/road_standard_arithmetic_owner.v"
    (ROOT/"formatted").mkdir(exist_ok=True)
    try:
        text,report=normalize_text_with_formatter_ast(source.read_text(encoding="utf-8"),source_path=source)
    except Exception as error:
        backend=create_formatter_backend(profile="formatter-normalize")
        first=backend.format_text(source.read_text(encoding="utf-8"),source)
        second=backend.format_text(first,source)
        (ROOT/"formatted/diagnostic_first.v").write_text(first,encoding="utf-8")
        (ROOT/"formatted/diagnostic_second.v").write_text(second,encoding="utf-8")
        save(ROOT/"formatted/status.json",dict(status="FAILED_PRESERVED",error=repr(error),live_source_unchanged=True))
        raise
    (ROOT/"formatted/road_standard_arithmetic_owner.v").write_text(text,encoding="utf-8")
    save(ROOT/"formatted/ast.json",report)


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action",choices=("contract","vectors","simulate","gate","format","report"))
    parser.add_argument("--case",type=int,default=0)
    args=parser.parse_args()
    if args.action == "simulate": simulate(args.case)
    else: globals()[args.action]()
