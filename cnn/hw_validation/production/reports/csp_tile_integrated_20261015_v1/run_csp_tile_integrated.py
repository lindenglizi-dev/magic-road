"""固定首残差tile：硬件调度、真实DW缓存、单端口取数与写完成的联合验证。"""
import argparse
from datetime import datetime
import json
from pathlib import Path
import re
import shutil
import subprocess
import time

import run_csp_first_probe as base

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "csp_tile_integrated"
PRIOR = base.BASE / "csp_writeback_pipeline_20261015_v2"


def signed(value, bits):
    return value - (1 << bits) if value & (1 << (bits - 1)) else value


def rne(value, shift):
    if not shift:
        return value
    quotient, remainder = divmod(value, 1 << shift)
    half = 1 << (shift - 1)
    return quotient + int(remainder > half or remainder == half and quotient & 1)


def sat(value, bits):
    return max(-(1 << (bits - 1)), min((1 << (bits - 1)) - 1, value))


def activation(value, table):
    if value <= -2048:
        return 0
    if value >= 2048:
        return value
    index = rne(value, 2) + 512
    return 2048 if index == 1024 else signed(table[index], 16)


def reference(out):
    """先证明紧凑ROM、地址和单次更新源的整数golden，后由RTL实现同一行为。"""
    vectors = {p.stem: base.readhex(p) for p in (PRIOR / "vectors").glob("*.hex")}
    weights = [None] * 56
    parameters = [None] * 16
    for task in range(160):
        pw = task >= 96
        if pw:
            pixel, output_group = divmod(task - 96, 4)
            y, x = divmod(pixel, 4)
            channel = output_group * 3
        else:
            y, rem = divmod(task, 24)
            channel, tail = divmod(rem, 2)
            x = tail * 3
        mask = 7 if pw or x == 0 else 1
        index = (y * 4 + x) * 12 + channel
        tags = [(192 + index + lane if pw else index + lane * 12)
                if mask & (1 << lane) else 65535 for lane in range(3)]
        addresses = [(0x03605000 + index + lane if pw else 0x035EA000 + index + lane * 12)
                     if mask & (1 << lane) else 0 for lane in range(3)]
        assert base.pack(tags, 16) == vectors["task_tags"][task]
        assert base.pack(addresses, 32) == vectors["task_addresses"][task]
        assert mask == vectors["task_mask"][task]
        assert int(pw) == vectors["task_residual"][task]
        if pw:
            assert base.pack([index + lane for lane in range(3)], 16) == vectors["task_bypass_indices"][task]
        parameter_index = 12 + output_group if pw else channel
        for group in range(2):
            position = task * 2 + group
            weight_index = 48 + output_group * 2 + group if pw else channel * 4 + (x == 3) * 2 + group
            word = vectors["group_weight"][position]
            if weights[weight_index] is not None:
                assert weights[weight_index] == word
            weights[weight_index] = word
            if not pw:
                indices = []
                for lane in range(8):
                    slot = group * 8 + lane
                    union_width = 3 if x else 5
                    indices.append(((y + slot // union_width) * 6 + x + slot % union_width) * 12 + channel
                                   if slot < (9 if x else 15) else 65535)
                assert base.pack(indices, 16) == vectors["group_halo_indices"][position]
            pword = (vectors["group_bias"][position] | vectors["task_pre_multiplier"][task] << 96
                     | vectors["task_pre_shift"][task] << 192 | vectors["task_post_multiplier"][task] << 210
                     | vectors["task_post_shift"][task] << 242)
            if mask == 7:
                if parameters[parameter_index] is not None:
                    assert parameters[parameter_index] == pword
                parameters[parameter_index] = pword
            else:
                expected = parameters[parameter_index]
                # 无效输出路在核心入口清零，保持冻结三路原子溢出语义。
                assert (expected & ((1 << 32)-1)) == vectors["group_bias"][position]
                assert ((expected >> 96) & ((1 << 32)-1)) == vectors["task_pre_multiplier"][task]
                assert ((expected >> 192) & 63) == vectors["task_pre_shift"][task]
    assert all(word is not None for word in weights + parameters)
    base.emit(out, "weight_program", weights, 192)
    base.emit(out, "parameter_program", parameters, 248)
    for variant in range(2):
        halo = [signed(v, 8) for v in vectors["halo"]]
        bypass = [signed(v, 8) for v in vectors["bypass"]]
        if variant:
            halo[100] = 127 if halo[100] < 0 else -128
            bypass[19] = sat(bypass[19] + (3 if bypass[19] < 125 else -3), 8)
        base.emit(out, f"source_{variant}", halo + bypass, 8)
        dw = [None] * 192
        golden = {name: [None] * 384 for name in ("acc", "pre", "silu", "post", "sum", "output", "address")}
        for task in range(160):
            pw = task >= 96
            for lane in range(3):
                if not vectors["task_mask"][task] & (1 << lane):
                    continue
                tag = vectors["task_tags"][task] >> (lane * 16) & 65535
                value = signed(vectors["group_bias"][task * 2] >> (lane * 32) & 0xffffffff, 32)
                for group in range(2):
                    position = task * 2 + group
                    for input_lane in range(8):
                        source_index = vectors["group_halo_indices"][position] >> (input_lane * 16) & 65535
                        sample = 0 if source_index == 65535 else dw[source_index] if pw else halo[source_index]
                        assert sample is not None
                        weight = signed(vectors["group_weight"][position] >> ((lane * 8 + input_lane) * 8) & 255, 8)
                        value += sample * weight
                assert -(1 << 31) <= value < (1 << 31)
                multiplier = vectors["task_pre_multiplier"][task] >> (lane * 32) & 0xffffffff
                shift = vectors["task_pre_shift"][task] >> (lane * 6) & 63
                pre = sat(rne(value * multiplier, shift), 16)
                nonlinear = activation(pre, vectors["silu"])
                post = sat(rne(nonlinear * vectors["task_post_multiplier"][task], vectors["task_post_shift"][task]), 8)
                total = post + (bypass[tag - 192] if pw else 0)
                for name, number in (("acc", value), ("pre", pre), ("silu", nonlinear), ("post", post),
                                     ("sum", total), ("output", sat(total, 8)),
                                     ("address", vectors["task_addresses"][task] >> (lane * 32) & 0xffffffff)):
                    golden[name][tag] = number
                if not pw:
                    dw[tag] = post
        if variant == 0:
            for name in ("acc", "pre", "silu", "post"):
                bits = 32 if name == "acc" else 16 if name in ("pre", "silu") else 8
                existing = vectors[f"dw_{name}"] + vectors[f"pw_{name}"]
                assert golden[name] == [signed(v, bits) for v in existing], name
            assert golden["output"][192:] == [signed(v, 8) for v in vectors["residual_post"]]
        for name, values in golden.items():
            assert None not in values
            bits = 32 if name in ("acc", "address") else 16 if name in ("pre", "silu", "sum") else 8
            base.emit(out, f"golden_{variant}_{name}", values, bits)
    base.save(out / "reference_receipt.json", dict(status="PASS", groups=320, tasks=160,
        baseline_goldens_identical=True, weights_words=56, parameter_words=16,
        compact_program_bytes=56*24 + 16*31, source_bytes=624, variants=2,
        scope="single first residual tile integer/compact program; not RTL/DDR/full graph"))


def specs():
    # 端口和行为来自本轮已确认固定接口，渲染阶段再与真实RTL交叉核对。
    top_ports = [("i_clk",1,"100MHz同域时钟"),("i_rstn",1,"共同异步低有效复位"),
        ("i_table_valid",1,"空闲时表valid"),("i_table_addr",10,"顺序表地址"),("i_table_data",16,"Q7.8表项"),
        ("o_table_ready",1,"真实表握手许可"),("o_table_loaded",1,"完整表激活状态"),
        ("i_source_begin",1,"清理源有效状态"),("o_source_begin_ready",1,"完整退休后才允许替换源"),
        ("i_source_valid",1,"源字节valid"),("i_source_address",10,"624字节逻辑源索引"),
        ("i_source_data",8,"源INT8字节"),("o_source_ready",1,"源字节接受许可"),
        ("o_source_loaded",1,"624个不同源字节齐全"),("i_start",1,"单tile启动请求"),
        ("o_start_ready",1,"源与表完整且空闲"),("i_cancel",1,"边沿前取消且粘滞"),
        ("i_output_ready",1,"真实外部写许可"),("o_output_valid",1,"完整外部写载荷valid"),
        ("o_output_data",8,"真实INT8输出"),("o_output_tag",16,"DW或PW输出身份"),
        ("o_output_address",32,"冻结图逻辑字节地址"),("o_output_sum",9,"signed9残差和"),
        ("o_busy",1,"任务或适配占有"),("o_done",1,"末次实际写后的单拍完成"),("o_fault",1,"粘滞故障")]
    cache_ports = [("i_clk",1,"同域时钟"),("i_rstn",1,"共同异步复位"),("i_clear",1,"启动新tile时同步清有效位"),
        ("i_write_valid",1,"真实DW写请求"),("i_write_index",8,"0至191逻辑索引"),("i_write_data",8,"真实DW字节"),
        ("i_read_valid",1,"PW八输入组请求"),("i_read_pixel",4,"4x4像素位置"),("i_read_group",1,"八加四输入分组"),
        ("i_output_ready",1,"响应消费许可"),("o_write_ready",1,"采集阶段写许可"),("o_loaded",1,"192个不同结果已齐全"),
        ("o_write_count",8,"唯一实际写数量"),("o_fault",1,"非法写粘滞错误"),("o_read_ready",1,"完整屏障及响应空间许可"),
        ("o_output_valid",1,"注册缓存响应valid"),("o_output_data",64,"八字节实际缓存值"),
        ("o_output_mask",8,"末组只低四lane有效"),("o_output_pixel",4,"响应像素身份"),("o_output_group",1,"响应分组身份")]
    def module(name, path, ports, behavior, waveform, clock="i_clk", reset="i_rstn"):
        return dict(name=name,rtl_path=path,clock=dict(name=clock,edge="posedge",frequency_mhz=100),
            reset=dict(name=reset,active="low",synchronous=False),
            interfaces=dict(ports=[dict(name=n,direction="input" if n.startswith("i_") else "output",width=w,
                role="clock" if n==clock else "reset" if n==reset else "native",description=d,clock_domain=clock) for n,w,d in ports]),
            behavior=behavior, constraints=["仅首残差tile，不代表完整CSP2、整网、真实DDR或物理实现", "保留冻结算术端口、II和数值"],
            corner_cases=["完整源与表之前禁止启动","源重复和越界写粘滞错误","复位取消全部在途有效位","输出反压保持"],
            verification_cases=["320组、160任务、384输出和各中间值逐项一致", "192实际DW写驱动128次PW缓存读",
                "随机与长反压","三阶段复位","两次不同输入tile不复位核心或重装表","外部取消阻止同拍写"],
            timing_diagrams=[dict(id="sequence",title="固定tile边界与完成",scenario="sequence",
                description="省略实际算术延迟；done严格来自最后实际写",wavejson=dict(signal=waveform))])
    top = module("road_csp_tile_integrated","rtl/road_csp_tile_integrated.v",top_ports,
        ["624唯一源字节及1024表项完整后单start启动，硬件产生全部描述符和操作数",
         "DW单端口源RAM拼装；PW只消费192个实际DW写齐后的缓存响应",
         "最后有效外部写握手才推进任务；DW写入缓存与外部观察同步接受",
         "source_begin只清源有效性，start只清缓存有效性，跨tile保留SiLU表"],
        [dict(name="i_clk",wave="p..|....."),dict(name="i_start",wave="010|....."),
         dict(name="o_busy",wave="011|11110"),dict(name="write_accept",wave="0..|...10"),dict(name="o_done",wave="0..|....1")])
    cache = module("road_csp_dw_cache","rtl/road_csp_dw_cache.v",cache_ports,
        ["i_clear同步撤销位图、计数及响应valid，不复位RAM，不清除粘滞故障",
         "192不同有效写之后允许PW请求，响应一槽并保持至真实接受"],
        [dict(name="i_clk",wave="p..|....."),dict(name="i_clear",wave="010|....."),
         dict(name="o_loaded",wave="100|..111"),dict(name="i_read_valid",wave="0..|...10"),dict(name="o_output_valid",wave="0..|....1")])
    tb = module("tb_csp_tile_integrated","tests/tb_csp_tile_integrated.v",[("o_test_complete",1,"所有当前场景检查通过")],
        ["只供应源、表和外部背压，不驱动内部任务、操作数或完成",
         "真实核心各阶段与同包整数golden对拍，重复tile改变源以捕获旧缓存"],
        [dict(name="clk",wave="p..|..."),dict(name="o_test_complete",wave="0..|..1")],clock="clk",reset="rstn")
    base.save(SOURCE / "spec_contract.json",dict(name="csp_tile_integrated",modules=[top,cache,tb]))
    print("SPEC_WRITTEN",flush=True)


def prepare(out):
    manifest = json.loads((PRIOR / "integration_sources.json").read_text(encoding="utf-8"))
    base.check_hashes({str(PRIOR / v["path"]): v["sha256"] for v in manifest["sources"]})
    original = [Path(__file__), SOURCE / "rtl/road_csp_tile_integrated.v", SOURCE / "rtl/road_csp_dw_cache.v",
                SOURCE / "tests/tb_csp_tile_integrated.v", SOURCE / "spec_contract.json"]
    original += [p for p in (SOURCE / "spec").rglob("*") if p.is_file()]
    original += [PRIOR / "rtl/road_csp_first_probe.v", PRIOR / "integration_inputs/road_csp_tile_schedule.v"]
    original += [p for p in (PRIOR / "reused").glob("*.v")]
    original += [p for p in (PRIOR / "vectors").glob("*.hex")]
    original += [base.VENDOR / "ph1p_logic_eram.v", base.VENDOR / "ph1p_phy_gsr.v"]
    original += [base.MODEL / f"{name}.exe" for name in ("vlib", "vlog", "vsim")]
    frozen = {str(p): base.digest(p) for p in original}
    out.mkdir(exist_ok=False)
    for directory in ("rtl", "tests", "spec"):
        shutil.copytree(SOURCE / directory, out / directory)
    shutil.copytree(PRIOR / "reused", out / "reused")
    shutil.copy2(PRIOR / "rtl/road_csp_first_probe.v", out / "reused/road_csp_first_probe.v")
    shutil.copy2(PRIOR / "integration_inputs/road_csp_tile_schedule.v", out / "reused/road_csp_tile_schedule.v")
    shutil.copytree(PRIOR / "vectors", out / "vectors")
    reference(out / "vectors")
    shutil.copy2(Path(__file__), out / Path(__file__).name)
    shutil.copy2(SOURCE / "spec_contract.json", out / "spec_contract.json")
    (out / "run").mkdir()
    staged = {str(p): base.digest(p) for p in out.rglob("*") if p.is_file()}
    base.save(out / "input_binding.json", dict(original_sha256=frozen, staged_sha256=staged,
        scope="single start executes first residual tile with hardware-controlled source fetch and actual DW cache",
        source_origin="prior QAT first3 integer fixture from original synthetic RGB, not camera measurements"))
    base.save(out / "status.json", dict(status="PREPARED_NOT_SIMULATED", production_delivery_ready=False))
    print("PREPARED", out, flush=True)


def execute(out, cases=range(11)):
    binding = json.loads((out / "input_binding.json").read_text(encoding="utf-8"))
    base.check_hashes(binding["original_sha256"])
    base.check_hashes(binding["staged_sha256"])
    (out / "execution_started.json").write_text(json.dumps(dict(start=datetime.now().astimezone().isoformat())), encoding="utf-8")
    commands, receipts = [], []
    started = time.monotonic()
    def run(argv, name):
        entry = dict(argv=list(map(str, argv)), cwd=str(out / "run"), executable_sha256=base.digest(Path(argv[0])))
        commands.append(entry)
        result = subprocess.run(entry["argv"], cwd=out / "run", stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, encoding="utf-8", errors="replace", timeout=180)
        (out / "run" / name).write_text(result.stdout, encoding="utf-8")
        entry["exit_code"] = result.returncode
        base.save(out / "commands.json", dict(commands=commands))
        if result.returncode or re.search(r"\*\* (?:Error|Fatal):", result.stdout):
            raise RuntimeError(f"external failure: {name}")
        return result.stdout
    try:
        run([base.MODEL / "vlib.exe", "work"], "vlib.log")
        sources = [base.VENDOR / "ph1p_logic_eram.v", base.VENDOR / "ph1p_phy_gsr.v"]
        sources += sorted((out / "reused").glob("*.v")) + sorted((out / "rtl").glob("*.v"))
        sources += [out / "tests/tb_csp_tile_integrated.v"]
        compile_log = run([base.MODEL / "vlog.exe", "-work", "work", *sources], "compile.log")
        assert re.findall(r"Errors:\s*(\d+),\s*Warnings:\s*(\d+)", compile_log)[-1] == ("0", "0")
        for case in cases:
            print("RUN", case, flush=True)
            output = run([base.MODEL / "vsim.exe", "-c", "-lib", "work", "PH1P_PHY_GSR", "tb_csp_tile_integrated",
                f"+CASE={case}", f"+VECTORS={(out / 'vectors').as_posix()}", "-do",
                "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"], f"case_{case}.log")
            markers = re.findall(r"CSP_TILE_(?:PASS|EXPECTED_FAULT) [^\r\n]*", output)
            assert len(markers) == 1
            fields = {k: int(v) for k, v in re.findall(r"(\w+)=(\d+)", markers[0])}
            assert fields.get("case") == case
            if case in (8, 9, 10):
                assert markers[0].startswith("CSP_TILE_EXPECTED_FAULT")
            else:
                assert markers[0].startswith("CSP_TILE_PASS")
                assert all(fields.get(k) == v for k, v in dict(groups=320, tasks=160, outputs=384,
                    acc=384, pre=384, silu=384, post=384, dw_writes=192, pw_reads=128).items())
                assert fields["cycles"] > 0
                if case == 7:
                    assert fields["runs"] == 2 and fields["table_loads"] == 1
            receipts.append(dict(case=case, receipt=markers[0], fields=fields))
            base.save(out / "case_receipts.json", dict(cases=receipts))
        base.check_hashes(binding["original_sha256"])
        base.check_hashes(binding["staged_sha256"])
        base.save(out / "status.json", dict(status="PASS_HARDWARE_DRIVEN_FIRST_RESIDUAL_TILE_NOT_DELIVERY_READY",
            cases=receipts, seconds=time.monotonic()-started, compile_errors=0, compile_warnings=0,
            arithmetic_executed=True, scheduler_cache_integrated=True,
            source_operand_fetch_by_RTL=True, completion_from_actual_last_write=True,
            testbench_task_driver=False, actual_DDR=False, full_CSP2_layer=False, full_graph=False,
            synthesis_or_board=False, training_updates=0, production_delivery_ready=False,
            original_and_staged_hashes_unchanged=True))
        print("PASS_HARDWARE_DRIVEN_FIRST_RESIDUAL_TILE", flush=True)
    except BaseException as error:
        base.save(out / "status.json", dict(status="FAILED_NO_RETRY", error=repr(error), cases=receipts,
            production_delivery_ready=False))
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("reference", "prepare", "execute", "spec"))
    parser.add_argument("--out", type=Path, default=base.BASE / "csp_tile_integrated_20261015_v1")
    args = parser.parse_args()
    if args.action == "reference":
        args.out.mkdir(exist_ok=False)
        reference(args.out)
    elif args.action == "prepare":
        prepare(args.out.resolve())
    elif args.action == "execute":
        execute(args.out.resolve())
    else:
        specs()
