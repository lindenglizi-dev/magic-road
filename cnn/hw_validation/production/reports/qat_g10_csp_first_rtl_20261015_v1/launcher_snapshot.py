"""Independent CSP data-path simulation; no training, production or board work."""
import argparse
from datetime import datetime
import json
from pathlib import Path
import re
import shutil
import subprocess
import time

from run_qat_front3_rtl import BASE, OLD, check_hashes, digest

SOURCE = Path(__file__).resolve().parent / "csp_first_probe"
DATA = BASE / "qat_g10_csp_first_data_20261015_v2"
OUT = BASE / "qat_g10_csp_first_rtl_20261015_v1"
MODEL = Path("D:/modeltech64_2020.4/win64")
VENDOR = Path("E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/sim_release/ph1p")
CORES = ("road_mac_probe", "road_dynamic_postprocess", "road_dynamic_requant", "road_round_shift", "silu_shared_unit")


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def pack(values, bits):
    return sum((int(value) & ((1 << bits)-1)) << (i*bits) for i, value in enumerate(values))


def emit(root, name, values, bits):
    (root / f"{name}.hex").write_text("".join(f"{int(v) & ((1 << bits)-1):0{(bits+3)//4}x}\n" for v in values), encoding="ascii")


def readhex(path):
    return [int(value, 16) for value in path.read_text().split()]


def specs():
    ports = [
        ("i_clk", 1, "100MHz同域时钟"), ("i_rstn", 1, "全部核心共同低有效异步复位，重新装表后计算"),
        ("i_table_valid", 1, "空闲表项valid"), ("i_table_addr", 10, "顺序1024项SiLU地址"),
        ("i_table_data", 16, "原包signed16表项"), ("o_table_ready", 1, "真实表项接受许可"),
        ("o_table_loaded", 1, "完整表重载完成"), ("i_input_valid", 1, "组valid，等待ready时载荷保持"),
        ("i_first", 1, "首组锁存任务元数据"), ("i_last", 1, "末组关闭归约"),
        ("i_lane_mask", 8, "八输入槽mask"), ("i_activation_data", 64, "八signed8低字节优先激活"),
        ("i_weight_data", 192, "三路各八signed8权重"), ("i_bias_data", 96, "三signed32偏置，仅first加入"),
        ("o_input_ready", 1, "单任务组准入"), ("i_output_mask", 3, "首组锁存的三输出mask"),
        ("i_tags", 48, "三外部标识，各16位"), ("i_addresses", 96, "三逻辑字节地址，各32位"),
        ("i_pre_multipliers", 96, "三非负signed32前乘数"), ("i_pre_shifts", 18, "三六位前移位，范围0到62"),
        ("i_post_multiplier", 32, "共享非负signed32后乘数"), ("i_post_shift", 6, "共享后移位0到62"),
        ("i_residual", 1, "融合旁路模式"), ("i_bypass_data", 24, "三signed8旁路值"),
        ("i_input_fault", 1, "任务故障输入"), ("i_output_ready", 1, "最终写端接受"),
        ("o_output_valid", 1, "完整写回载荷有效并保持"), ("o_output_data", 8, "sat8结果"),
        ("o_output_tag", 16, "写回标识"), ("o_output_address", 32, "写回逻辑字节地址"),
        ("o_output_sum", 9, "饱和前signed9观察值"), ("o_fault", 1, "故障粘滞，共同复位清除")]
    waveform = dict(signal=[dict(name="i_clk", wave="p..|....."), dict(name="i_rstn", wave="1..|....."),
        dict(name="i_input_valid", wave="011|0...."), dict(name="o_input_ready", wave="011|0...."),
        dict(name="i_first", wave="010|0...."), dict(name="i_last", wave="001|0...."),
        dict(name="o_output_valid", wave="0..|.1110"), dict(name="i_output_ready", wave="1..|.0011"),
        dict(name="o_output_data/tag/address", wave="x..|.=.==", data=["A", "B", "C"])])
    common = dict(clock=dict(name="i_clk", edge="posedge", frequency_mhz=100),
        reset=dict(name="i_rstn", active="low", synchronous=False),
        constraints=["只验证独立数据通路，不宣称整网、真实DDR或物理实现通过", "不得修改冻结算术核、II或外设协议"],
        corner_cases=["未装表禁止计算", "元数据保持到最后有效写端接受", "复位取消旧token并重新装表", "故障不自动恢复"],
        verification_cases=["真实QAT阶段逐项对拍与DW实际输出驱动PW", "输入气泡、输出长背压及三处复位重跑", "任务错误、INT32末组溢出、非法移位", "合成正负饱和贯穿完整写beat"])
    module = dict(name="road_csp_first_probe", rtl_path="rtl/road_csp_first_probe.v", **common,
        interfaces=dict(ports=[dict(name=n, direction="input" if n.startswith("i_") else "output", width=w,
            role="clock" if n == "i_clk" else "reset" if n == "i_rstn" else "native", description=d, clock_domain="i_clk") for n, w, d in ports]),
        behavior=["单归约上下文，first接受锁存元数据，last后等待原MAC结果", "动态重定标、SiLU及后重定标复用冻结核心",
                  "量化输出真实接受时计算signed9旁路和并sat8，同步锁存地址与tag", "写槽背压保持，最终有效写接受后才开放新任务"],
        timing_diagrams=[dict(id="hold", title="单事务及写回保持", scenario="backpressure", description="契约示意；竖线省略实际核心延迟，不是实测周期", wavejson=waveform)])
    tb = dict(name="tb_csp_first_probe", rtl_path="tests/tb_csp_first_probe.v",
        clock=dict(name="clk", edge="posedge", frequency_mhz=100), reset=dict(name="rstn", active="low", synchronous=False),
        interfaces=dict(ports=[dict(name="o_test_complete", direction="output", width=1, role="verification_completion", description="仅全部相应检查通过后置1")]),
        behavior=["内部产生时钟、装表和有限任务，逐项scoreboard", "存储和任务由测试台驱动，不冒充可综合调度器"],
        constraints=["仅验证模块，不进入生产综合源清单"], corner_cases=common["corner_cases"], verification_cases=common["verification_cases"],
        timing_diagrams=[dict(id="complete", title="检查完成", scenario="completion", description="终止前置完成位，非实测耗时", wavejson=dict(signal=[dict(name="clk", wave="p..|..."), dict(name="rstn", wave="01.|..."), dict(name="o_test_complete", wave="0..|.1.")]))])
    save(SOURCE / "spec_contract.json", dict(name="csp_first_probe", modules=[module, tb]))
    print("SPEC_CONTRACT_WRITTEN")


def vectors(root):
    root.mkdir()
    for path in (DATA / "vectors").glob("*.hex"):
        shutil.copy2(path, root / path.name)
    shutil.copy2(DATA / "parameters/silu.hex", root / "silu.hex")
    tasks = json.loads((DATA / "mac_tasks.json").read_text())["tasks"]
    metadata = {key: [] for key in ("tags", "addresses", "pre_multiplier", "pre_shift", "post_multiplier", "post_shift", "mask", "residual", "bypass_indices")}
    group_data = {key: [] for key in ("activation", "weight", "bias", "mask", "first", "last", "halo_indices")}
    for task in tasks:
        layer = task["layer"]
        params = {name: readhex(DATA / "parameters" / f"{layer}_{name}.hex") for name in ("pre_multiplier", "pre_shift", "post_multiplier", "post_shift")}
        tags, addresses, multipliers, shifts, bypass = [], [], [], [], []
        for coord in task["coordinates"]:
            if coord is None:
                tags.append(65535); addresses.append(0); multipliers.append(0); shifts.append(0); bypass.append(65535)
                continue
            y, x, c = coord
            index = (y*4+x)*12+c
            tags.append(index + (192 if layer == "pw" else 0))
            addresses.append((56643584 if layer == "pw" else 56532992)+index)
            multipliers.append(params["pre_multiplier"][c]); shifts.append(params["pre_shift"][c])
            bypass.append(index if layer == "pw" else 65535)
        for key, value in (("tags", pack(tags, 16)), ("addresses", pack(addresses, 32)),
                ("pre_multiplier", pack(multipliers, 32)), ("pre_shift", pack(shifts, 6)),
                ("post_multiplier", params["post_multiplier"][0]), ("post_shift", params["post_shift"][0]),
                ("mask", task["output_mask"]), ("residual", layer == "pw"), ("bypass_indices", pack(bypass, 16))):
            metadata[key].append(value)
        for group_index, group in enumerate(task["groups"]):
            for key in ("activation", "weight", "bias"):
                group_data[key].append(int(group[f"{key}_hex"], 16))
            group_data["mask"].append(group["input_mask"])
            for key in ("first", "last"):
                group_data[key].append(group[key])
            indices = [65535]*8
            if layer == "dw":
                y, x, c = task["coordinates"][0]
                width = sum(coord is not None for coord in task["coordinates"])+2
                for lane in range(8):
                    offset = group_index*8+lane
                    if offset < width*3:
                        ky, kx = divmod(offset, width)
                        indices[lane] = ((y+ky)*6+x+kx)*12+c
            else:
                y, x, _ = task["coordinates"][0]
                for lane in range(8):
                    channel = group_index*8+lane
                    if channel < 12:
                        indices[lane] = (y*4+x)*12+channel
            group_data["halo_indices"].append(pack(indices, 16))
    task_widths = dict(tags=48, addresses=96, pre_multiplier=96, pre_shift=24, post_multiplier=32,
                       post_shift=8, mask=8, residual=8, bypass_indices=48)
    group_widths = dict(activation=64, weight=192, bias=96, mask=8, first=8, last=8, halo_indices=128)
    for key, values in metadata.items():
        emit(root, f"task_{key}", values, task_widths[key])
    for key, values in group_data.items():
        emit(root, f"group_{key}", values, group_widths[key])
    addresses = json.loads((DATA / "addresses.json").read_text())
    emit(root, "halo_native_addresses", [r["native_beat_address"] if not r["padding"] else 0xffffffff for r in addresses["halo"]], 32)
    emit(root, "halo_byte_lanes", [r["byte_lane"] if not r["padding"] else 0 for r in addresses["halo"]], 8)
    emit(root, "bypass_native_addresses", [(r["bypass_byte_address"] & ~15)//2 for r in addresses["outputs"]], 32)
    emit(root, "bypass_byte_lanes", [r["bypass_byte_address"] & 15 for r in addresses["outputs"]], 8)
    source = readhex(BASE / "qat_g10_front3_paxi_20261015_v1/vectors/pw_golden.hex")[:1536]
    words = [pack(source[i:i+16], 8) for i in range(0, len(source), 16)]
    native = [(56311808+tile*384+word*16)//2 for tile in (0, 1, 32, 33) for word in range(24)]
    emit(root, "input_words", words, 128); emit(root, "input_native_addresses", native, 32)
    memory = dict(zip(native, words, strict=True))
    halo = [0 if record["padding"] else (memory[record["native_beat_address"]] >> (8*record["byte_lane"])) & 255 for record in addresses["halo"]]
    if halo != readhex(root / "halo.hex"):
        raise ValueError("native beat/lane halo replay differs from verified golden")
    for activations, encoded in zip(group_data["activation"][:192], group_data["halo_indices"][:192], strict=True):
        indices = [(encoded >> (lane*16)) & 65535 for lane in range(8)]
        if pack([0 if index == 65535 else halo[index] for index in indices], 8) != activations:
            raise ValueError("DW packed groups did not come from native-beat halo")
    dw = readhex(root / "dw_post.hex")
    for activations, encoded in zip(group_data["activation"][192:], group_data["halo_indices"][192:], strict=True):
        indices = [(encoded >> (lane*16)) & 65535 for lane in range(8)]
        if pack([0 if index == 65535 else dw[index] for index in indices], 8) != activations:
            raise ValueError("PW index mapping differs from verified DW-to-PW contract")
    # Separate synthetic KAT: one whole residual beat with both saturation signs.
    lut = readhex(root / "silu.hex")
    biases = [(256, -256, 0)[i % 3] for i in range(16)]
    silu = [lut[512+bias//4] for bias in biases]
    silu = [v-65536 if v >= 32768 else v for v in silu]
    post = [max(-128, min(127, v*4)) for v in silu]
    bypass = [(127, -128, -128)[i % 3] for i in range(16)]
    sums = [a+b for a, b in zip(post, bypass, strict=True)]
    output = [max(-128, min(127, v)) for v in sums]
    if sums[:3] != [254, -256, -128]:
        raise ValueError("synthetic saturation KAT contract changed")
    for name, values, bits in (("acc", biases, 32), ("pre", biases, 16), ("silu", silu, 16),
                              ("post", post, 8), ("sum", sums, 16), ("output", output, 8), ("word", [pack(output, 8)], 128)):
        emit(root, f"sat_{name}", values, bits)
    sat_task = {key: [] for key in (*task_widths, "bypass") if key != "bypass_indices"}
    sat_group = {key: [] for key in group_widths if key != "halo_indices"}
    for start in range(0, 16, 3):
        valid = min(3, 16-start)
        indices = list(range(start, start+valid))
        tags = [384+i for i in indices]+[65535]*(3-valid)
        for key, value in (("tags", pack(tags, 16)), ("addresses", pack([56643584+i for i in indices]+[0]*(3-valid), 32)),
                ("pre_multiplier", pack([1]*valid+[0]*(3-valid), 32)), ("pre_shift", 0),
                ("post_multiplier", 4), ("post_shift", 0), ("mask", (1 << valid)-1), ("residual", 1),
                ("bypass", pack([bypass[i] for i in indices]+[0]*(3-valid), 8))):
            sat_task[key].append(value)
        for group in range(2):
            for key, value in (("activation", 0), ("weight", 0), ("bias", pack([biases[i] for i in indices]+[0]*(3-valid), 32)),
                               ("mask", 255 if group == 0 else 15), ("first", group == 0), ("last", group == 1)):
                sat_group[key].append(value)
    for key, values in sat_task.items():
        emit(root, f"sat_task_{key}", values, 24 if key == "bypass" else task_widths[key])
    for key, values in sat_group.items():
        emit(root, f"sat_group_{key}", values, group_widths[key])


def prepare():
    status = json.loads((DATA / "status.json").read_text())
    receipt = json.loads((DATA / "verification_receipt.json").read_text())
    check_hashes({str(DATA / "verification_receipt.json"): status["verification_receipt_sha256"]})
    check_hashes({str(DATA / name): sha for name, sha in receipt["artifact_sha256"].items()})
    if status["status"] != "REAL_QAT_CSP_FIRST_DATA_READY_FOR_RTL_DESIGN":
        raise ValueError("CSP data prerequisite missing")
    identity = json.loads((DATA / "identity.json").read_text())
    frozen = dict(identity["input_sha256"])
    frozen.update({str(DATA / name): sha for name, sha in receipt["artifact_sha256"].items()})
    frozen[str(DATA / "verification_receipt.json")] = digest(DATA / "verification_receipt.json")
    documentation = [SOURCE / "spec_contract.json", *[p for p in (SOURCE / "spec").rglob("*") if p.is_file()]]
    if len(documentation) < 7:
        raise ValueError("required same-name module specs and WaveDrom outputs missing")
    sources = [SOURCE / "rtl/road_csp_first_probe.v", SOURCE / "tests/tb_csp_first_probe.v", Path(__file__), *documentation]
    reused = [OLD / "reused" / f"{name}.v" for name in CORES]
    vendor = [VENDOR / "ph1p_logic_eram.v", VENDOR / "ph1p_phy_gsr.v"]
    tools = [MODEL / f"{name}.exe" for name in ("vlib", "vlog", "vsim")]
    frozen.update({str(p): digest(p) for p in [*sources, *reused, *vendor, *tools]})
    check_hashes(frozen)
    OUT.mkdir(exist_ok=False)
    for path in sources:
        target = OUT / (path.relative_to(SOURCE) if path.is_relative_to(SOURCE) else "launcher_snapshot.py")
        target.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(path, target)
    (OUT / "reused").mkdir()
    for path in reused:
        shutil.copy2(path, OUT / "reused" / path.name)
    vectors(OUT / "vectors")
    (OUT / "run").mkdir()
    shutil.copy2(DATA / "contract.json", OUT / "data_contract.json")
    shutil.copy2(DATA / "identity.json", OUT / "data_identity.json")
    staged = {str(p): digest(p) for p in OUT.rglob("*") if p.is_file()}
    save(OUT / "input_binding.json", dict(original_sha256=frozen, staged_sha256=staged,
        payload_sha256=identity["payload_sha256"], checkpoint_sha256=identity["checkpoint_sha256"],
        scope="single-context arithmetic wrapper; TB generates tasks and native memory reads; actual DW output feeds PW"))
    save(OUT / "status.json", dict(status="PREPARED_NOT_SIMULATED", formal_acceptance=False))
    print("PREPARED", OUT, flush=True)


def execute():
    binding = json.loads((OUT / "input_binding.json").read_text())
    check_hashes(binding["original_sha256"]); check_hashes(binding["staged_sha256"])
    with (OUT / "execution_started.json").open("x", encoding="utf-8") as f:
        json.dump(dict(start=datetime.now().astimezone().isoformat()), f)
    started, commands, cases = time.monotonic(), [], []

    def run(argv, name):
        commands.append(dict(argv=argv, cwd=str(OUT / "run"), executable_sha256=digest(Path(argv[0]))))
        save(OUT / "commands.json", dict(commands=commands))
        print("RUN", name, flush=True)
        result = subprocess.run(argv, cwd=OUT / "run", text=True, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, encoding="utf-8", errors="replace", timeout=180)
        (OUT / "run" / name).write_text(result.stdout, encoding="utf-8")
        commands[-1]["exit_code"] = result.returncode
        save(OUT / "commands.json", dict(commands=commands))
        if result.returncode:
            raise RuntimeError(f"external failure {result.returncode}: {name}")
        return result.stdout
    try:
        run([str(MODEL / "vlib.exe"), "work"], "vlib.log")
        source = [VENDOR / "ph1p_logic_eram.v", VENDOR / "ph1p_phy_gsr.v",
                  *[OUT / "reused" / f"{name}.v" for name in CORES], OUT / "rtl/road_csp_first_probe.v", OUT / "tests/tb_csp_first_probe.v"]
        compile_log = run([str(MODEL / "vlog.exe"), "-work", "work", *map(str, source)], "compile.log")
        summary = re.findall(r"Errors:\s*(\d+),\s*Warnings:\s*(\d+)", compile_log)
        if not summary or tuple(map(int, summary[-1])) != (0, 0):
            raise ValueError("compile not0errors/0warnings")
        for case in range(10):
            output = run([str(MODEL / "vsim.exe"), "-c", "-lib", "work", "PH1P_PHY_GSR", "tb_csp_first_probe",
                f"+CASE={case}", f"+VECTORS={(OUT / 'vectors').as_posix()}", "-do",
                "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"], f"case_{case}.log")
            receipt = validate_receipt(case, output)
            if re.search(r"\*\* (?:Error|Fatal):", output):
                raise ValueError(f"case{case} missing expected receipt")
            cases.append(dict(case=case, receipt=receipt, log=f"run/case_{case}.log"))
            save(OUT / "case_receipts.json", dict(cases=cases))
        check_hashes(binding["original_sha256"]); check_hashes(binding["staged_sha256"])
        save(OUT / "status.json", dict(status="PASS_CSP_FIRST_LOCAL_PROBE_10_OF_10", as_of=datetime.now().astimezone().isoformat(),
            seconds=time.monotonic()-started, cases=cases, compile_errors=0, compile_warnings=0,
            original_and_staged_hashes_unchanged=True, RTL_kernels_changed=False, new_wrapper=True,
            scope=binding["scope"], training_updates=0, actual_DDR_or_full_graph=False,
            synthesis_bitstream_or_board=False, formal_acceptance=False))
        print("PASS_CSP_FIRST_LOCAL_PROBE_10_OF_10", flush=True)
    except BaseException as error:
        save(OUT / "status.json", dict(status="FAILED_NO_RETRY", error=repr(error), cases=cases,
            seconds=time.monotonic()-started, formal_acceptance=False))
        raise


def validate_receipt(case, output):
    """Reject a pass from a wrong case, incomplete run or fault/pass mixup."""
    markers = re.findall(r"CSP_FIRST_(?:PASS|EXPECTED_FAULT) [^\r\n]*", output)
    if len(markers) != 1:
        raise ValueError(f"case{case}: expected exactly one terminal receipt")
    marker = markers[0]
    fields = {key: int(value) for key, value in re.findall(r"(\w+)=(\d+)", marker)}
    if case in (6, 7, 8):
        expected = dict(case=case, outputs=0)
        prefix = "CSP_FIRST_EXPECTED_FAULT "
    else:
        count = 16 if case == 9 else 384
        expected = dict(case=case, generation=2 if case in (3, 4, 5) else 1,
            groups=12 if case == 9 else 320, tasks=6 if case == 9 else 160,
            outputs=count, acc=count, pre=count, silu=count, post=count, sums=16 if case == 9 else 192)
        prefix = "CSP_FIRST_PASS "
    if not marker.startswith(prefix) or any(fields.get(key) != value for key, value in expected.items()):
        raise ValueError(f"case{case}: incomplete or incorrect receipt: {marker}")
    if case not in (6, 7, 8) and fields.get("cycles", 0) <= 0:
        raise ValueError("missing measured cycle count")
    return marker


def selftest():
    good = "CSP_FIRST_PASS case=0 generation=1 groups=320 tasks=160 outputs=384 acc=384 pre=384 silu=384 post=384 sums=192 cycles=1"
    assert validate_receipt(0, good) == good
    assert validate_receipt(6, "CSP_FIRST_EXPECTED_FAULT case=6 outputs=0")
    for case, bad in ((0, good.replace("outputs=384", "outputs=383")), (1, good),
                      (6, good.replace("case=0", "case=6")), (0, good+"\n"+good),
                      (0, good.replace("cycles=1", "cycles=0"))):
        try:
            validate_receipt(case, bad)
        except ValueError:
            continue
        raise AssertionError("invalid receipt accepted")
    print("RECEIPT_CHECK_PASS positive2 negative5")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("spec", "prepare", "execute", "selftest"))
    {"spec": specs, "prepare": prepare, "execute": execute, "selftest": selftest}[parser.parse_args().action]()
