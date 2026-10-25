"""五级写回候选：冻结源、Python逐拍契约、真实ModelSim回归；不训练或操作板卡。"""
import argparse
from datetime import datetime
from itertools import permutations
import json
from pathlib import Path
import random
import re
import shutil
import subprocess

import csp_writeback_schedule as semantic
import run_csp_first_followup as followup
import run_csp_first_probe as base

SOURCE = Path(__file__).resolve().parent / "csp_writeback_pipeline"
PRIOR = base.BASE / "qat_g10_csp_first_closure_20261015_v2"


def trace_vectors(path):
    model = semantic.Writeback()
    metadata = (1, (1, 2, 3), (100, 200, 300), (0, 0, 0), True)
    counts = dict(cycles=0, exhaustive_pairs=0, frozen_tasks=0, masks=0,
                  permutations=0, cancellation=0, faults=0, reuse=0)
    with path.open("x", encoding="ascii") as output:
        def cycle(item=None, ready=True, reset=False, external=False, begin=None):
            nonlocal metadata
            if reset:
                model.__init__()  # RTL异步复位在边沿前已经清除状态。
            if begin is not None:
                metadata = begin
            mask, tags, addresses, bypass, residual = metadata
            value = model.output()
            visible = value is not None and not reset and not external
            flags = (int(not reset) | (int(model.loaded) << 1) | (int(external) << 2)
                     | (int(begin is not None) << 3) | (int(item is not None) << 4)
                     | (int(bool(item and item[2])) << 5) | (int(ready) << 6)
                     | (int(residual) << 7))
            drive = base.pack([flags], 8) | (mask << 8) | (base.pack(tags, 16) << 11)
            drive |= base.pack(addresses, 32) << 59 | base.pack(bypass, 8) << 155
            if item is not None:
                drive |= (item[1] & 65535) << 179 | item[0] << 195
            control = (int(model.pp_ready() and not reset and not external)
                       | (int(visible) << 1) | (int(model.owned) << 2)
                       | (int(model.fault or external) << 3))
            expected = control
            if visible:
                _, data, total, tag, address = value
                expected |= (data & 255) << 8 | (total & 511) << 16 | tag << 25 | address << 41
            pipe_valid = sum(int(token is not None) << i for i, token in enumerate(model.pipe))
            expected |= model.seen << 73 | model.remaining << 76 | pipe_valid << 79
            if model.pipe[2] is not None:
                expected |= (model.pipe[2][1] & 511) << 83
            if model.pipe[3] is not None:
                expected |= (model.pipe[3][1] & 511) << 92
            output.write(f"{(expected << 211) | drive:078x}\n")
            accepted, emitted = model.step(item, ready, reset=reset, external_fault=external)
            if begin is not None:
                model.begin(*begin)
            counts["cycles"] += 1
            return accepted, emitted

        def restart():
            cycle(reset=True)
            model.load_complete()

        def task(spec, values, order=None, stalled=False):
            if not model.loaded:
                model.load_complete()
            cycle(begin=spec)
            mask, tags, _, _, _ = spec
            lanes = list(order) if order is not None else [i for i in range(3) if mask & (1 << i)]
            rng = random.Random(42 + counts["frozen_tasks"])
            sent = 0
            for age in range(1000):
                ready = not stalled or age >= 37 and rng.randrange(4) != 0
                item = None
                if sent < len(lanes) and (not stalled or rng.randrange(5)):
                    lane = lanes[sent]
                    item = (tags[lane], values[lane], False)
                accepted, _ = cycle(item, ready)
                sent += int(accepted)
                if not model.owned:
                    assert sent == len(lanes) and not model.fault
                    cycle()
                    return
            raise AssertionError("task did not retire")

        restart()
        for a in range(-128, 128):
            for b in range(-128, 128):
                task((1, (1, 2, 3), (100, 200, 300), (b, 0, 0), True), (a, 0, 0))
                counts["exhaustive_pairs"] += 1
        for mask, tags, addresses, bypass, residual, values in semantic.vectors():
            spec = (mask, tags, addresses, bypass, residual)
            task(spec, values)
            task(spec, values, stalled=True)
            counts["frozen_tasks"] += 1
        for mask in range(1, 8):
            task((mask, (3, 7, 9), (10, 20, 30), (-128, 127, 1), True), (127, 127, -128), stalled=True)
            counts["masks"] += 1
            for order in permutations(i for i in range(3) if mask & (1 << i)):
                task((mask, (3, 7, 9), (10, 20, 30), (-128, 127, 1), True), (127, 127, -128), order, True)
                counts["permutations"] += 1
        for external in (False, True):
            for age in range(1, 6):
                restart()
                cycle(begin=(7, (1, 2, 3), (10, 20, 30), (0, 0, 0), True))
                cycle((1, 99, False), ready=False)
                for _ in range(age - 1):
                    cycle(ready=False)
                cycle(reset=not external, external=external)
                for _ in range(7):
                    cycle()
                counts["cancellation"] += 1
        for bad in ((99, 1, False), (1, 1, True), (1, 128, False), (1, 1, False)):
            restart()
            cycle(begin=(7, (1, 2, 3), (10, 20, 30), (0, 0, 0), True))
            if bad == (1, 1, False):
                cycle(bad)
            cycle(bad)
            for _ in range(7):
                cycle((2, 1, False))
            counts["faults"] += 1
        for bad_spec in ((0, (1, 2, 3)), (3, (1, 1, 3))):
            restart()
            cycle(begin=(bad_spec[0], bad_spec[1], (10, 20, 30), (0, 0, 0), True))
            for _ in range(7):
                cycle()
            counts["faults"] += 1
        for delay in (0, 4):
            restart()
            cycle(begin=(1, (1, 2, 3), (10, 20, 30), (0, 0, 0), True))
            cycle((1, 5, False))
            for _ in range(delay):
                cycle(ready=False)
            accepted, _ = cycle((1, 6, False))
            assert not accepted and model.fault
            for _ in range(7):
                cycle()
            counts["faults"] += 1
        # 坏token同步检错时，边沿前已合法有效的写仍可提交。
        restart()
        cycle(begin=(7, (1, 2, 3), (10, 20, 30), (0, 0, 0), True))
        cycle((1, 5, False))
        for _ in range(4):
            cycle(ready=False)
        accepted, emitted = cycle((99, 0, False))
        assert accepted and emitted[1] == 5 and model.fault
        cycle()
        counts["faults"] += 1
        restart()
        for _ in range(2):
            task((7, (1, 2, 3), (10, 20, 30), (127, -128, 1), True), (127, -128, 1), stalled=True)
            counts["reuse"] += 1
        restart()
        cycle()
    return counts


def specs():
    spec = json.loads((base.SOURCE.parent / "csp_first_closure/spec_contract.json").read_text(encoding="utf-8"))
    module = spec["modules"][0]
    module["behavior"] = ["first实际接受锁存任务，M/S/A/C/W五级写回，每路预留一个槽",
        "M接受后第5拍最早外部提交，连续输入可连续写出，所有权保持至最终有效写握手",
        "seen收齐即关闭PP ready，额外valid零接受并粘滞fault；同步检错不追回同拍旧合法写",
        "未知tag、重复tag、非INT8符号扩展及rawmode取消未提交结果，共同复位后完整重装表"]
    module["timing_diagrams"] = [dict(id="pipeline", title="五级写回与三槽保持", scenario="pipeline",
        description="PP在边沿0/1/2接受，持续写ready时在5/6/7提交；阶段与槽数据有效独立",
        wavejson=dict(signal=[dict(name="i_clk", wave="p........"),
            dict(name="pp_accept", wave="1110....."), dict(name="M", wave="01110...."),
            dict(name="S", wave="0.1110..."), dict(name="A", wave="0..1110.."),
            dict(name="C", wave="0...1110."), dict(name="W", wave="0....1110"),
            dict(name="write_accept", wave="0....1110")]))]
    module["verification_cases"] += ["65536组INT8残差输入对逐拍检查", "三路乱序接收及长背压",
        "M/S/A/C/W各级取消", "额外valid零准入与同步检错合法旧写边界"]
    trace = dict(spec["modules"][1])
    trace.update(name="tb_csp_writeback_trace", rtl_path="tests/tb_csp_writeback_trace.v",
                 behavior=["仅强制MAC/PP边界，逐拍比较Python写回契约；不作为实际核心功能证据"],
                 verification_cases=module["verification_cases"])
    spec["modules"].append(trace)
    base.save(SOURCE / "spec_contract.json", spec)


def prepare(out):
    out.mkdir(exist_ok=False)
    (out / "run").mkdir()
    originals = [SOURCE / "rtl/road_csp_first_probe.v", SOURCE / "tests/tb_csp_first_probe.v",
                 SOURCE / "tests/tb_csp_writeback_trace.v", SOURCE / "spec_contract.json",
                 Path(__file__), Path(semantic.__file__), Path(base.__file__), Path(followup.__file__)]
    for folder in ("rtl", "tests", "spec", "reused", "vectors"):
        shutil.copytree(SOURCE / folder if folder in ("rtl", "tests", "spec") else PRIOR / folder, out / folder)
    for source in originals[3:]:
        shutil.copy2(source, out / source.name)
    originals += [p for p in (PRIOR / "reused").glob("*.v")]
    originals += [p for p in (PRIOR / "vectors").glob("*.hex")]
    originals += [p for p in (SOURCE / "spec").rglob("*") if p.is_file()]
    originals += [base.VENDOR / "ph1p_logic_eram.v", base.VENDOR / "ph1p_phy_gsr.v"]
    originals += [base.MODEL / f"{name}.exe" for name in ("vlib", "vlog", "vsim")]
    counts = trace_vectors(out / "writeback_trace.hex")
    base.save(out / "trace_coverage.json", counts)
    original = {str(p): base.digest(p) for p in originals}
    staged = {str(p): base.digest(p) for p in out.rglob("*") if p.is_file()}
    base.save(out / "input_binding.json", dict(original_sha256=original, staged_sha256=staged,
        scope="five-stage writeback boundary trace plus unchanged frozen arithmetic cores in17 real regressions"))
    base.save(out / "status.json", dict(status="PREPARED_NOT_SIMULATED", formal_acceptance=False))
    print("PREPARED", out, counts, flush=True)


def execute(out):
    # 复用原17项真实核心回归的收据判定及外部执行封装。
    base.OUT = out
    base.execute(range(17), followup.validate_receipt)
    binding = json.loads((out / "input_binding.json").read_text())
    base.check_hashes(binding["original_sha256"])
    base.check_hashes(binding["staged_sha256"])
    commands = json.loads((out / "commands.json").read_text())["commands"]
    def run(argv, name):
        entry = dict(argv=list(map(str, argv)), cwd=str(out / "run"), executable_sha256=base.digest(Path(argv[0])))
        commands.append(entry)
        result = subprocess.run(entry["argv"], cwd=out / "run", stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, encoding="utf-8", errors="replace", timeout=180)
        (out / "run" / name).write_text(result.stdout, encoding="utf-8")
        entry["exit_code"] = result.returncode
        base.save(out / "commands.json", dict(commands=commands))
        if result.returncode or re.search(r"\*\* (?:Error|Fatal):", result.stdout):
            raise RuntimeError(f"trace external failure: {name}")
        return result.stdout
    try:
        output = run([base.MODEL / "vlog.exe", "-work", "work", out / "tests/tb_csp_writeback_trace.v"], "trace_compile.log")
        if not re.search(r"Errors:\s*0,\s*Warnings:\s*0", output):
            raise ValueError("trace compile requires0errors/0warnings")
        output = run([base.MODEL / "vsim.exe", "-c", "-lib", "work", "PH1P_PHY_GSR", "tb_csp_writeback_trace",
            f"+TRACE={(out / 'writeback_trace.hex').as_posix()}", "-do",
            "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"], "trace.log")
        count = json.loads((out / "trace_coverage.json").read_text())["cycles"]
        if re.findall(r"CSP_WRITEBACK_TRACE_PASS cycles=(\d+)", output) != [str(count)]:
            raise ValueError("trace terminal receipt incomplete")
        base.check_hashes(binding["original_sha256"])
        base.check_hashes(binding["staged_sha256"])
        status = json.loads((out / "status.json").read_text())
        status.update(status="PASS_WRITEBACK_TRACE_AND_17_REAL_CORE_CASES_NOT_DELIVERY_READY",
                      as_of=datetime.now().astimezone().isoformat(), trace_cycles=count,
                      forced_boundary_scope="trace only;17 actual-core cases have no new boundary force",
                      full_graph=False, production_delivery_ready=False)
        base.save(out / "status.json", status)
        print(status["status"], flush=True)
    except BaseException as error:
        base.save(out / "trace_failure.json", dict(error=repr(error)))
        status = json.loads((out / "status.json").read_text())
        status.update(status="TRACE_FAILED_KEEP_17_CASE_EVIDENCE", error=repr(error))
        base.save(out / "status.json", status)
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("spec", "prepare", "execute"))
    parser.add_argument("--out", type=Path, default=base.BASE / "csp_writeback_pipeline_20261015_v1")
    args = parser.parse_args()
    if args.action == "spec":
        specs()
    elif args.action == "prepare":
        prepare(args.out.resolve())
    else:
        execute(args.out.resolve())
