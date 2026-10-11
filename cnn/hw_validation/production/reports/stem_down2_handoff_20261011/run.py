"""Stem 实际 RTL 输出交接给 down2；所有输出限定本目录，旧基线不写。"""
import argparse
import ast
import csv
import importlib.util
import json
from pathlib import Path
import re
import shutil
import sys

import numpy as np

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / "down2_full_tensor_20261010"
spec = importlib.util.spec_from_file_location("full_layer_helpers", BASE / "run.py")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
# 仅复用函数；其输出根目录改为本候选，不调用旧 prepare/gate/simulate/finish。
base.ROOT = ROOT
save, sha, fresh, command, tiled, integer = base.save, base.sha, base.fresh, base.command, base.tiled, base.integer


def check():
    frozen = json.loads((ROOT / "frozen.json").read_text(encoding="utf-8"))
    changed = [path for path, digest in frozen.items() if sha(Path(path)) != digest]
    save(ROOT / "frozen_check.json", {"checked": len(frozen), "changed": changed})
    assert not changed, changed


def prepare():
    assert not (ROOT / "reference.json").exists(), "Completed vectors are frozen"
    if not (ROOT / "frozen.json").exists():
        frozen = json.loads((BASE / "artifact_manifest.json").read_text(encoding="utf-8"))
        frozen[str(BASE / "artifact_manifest.json")] = sha(BASE / "artifact_manifest.json")
        save(ROOT / "frozen.json", frozen)
    check()
    out = ROOT / "vectors"
    out.mkdir(exist_ok=True)
    rng = np.random.default_rng(43)
    rgb = rng.integers(0, 256, (288, 512, 3), dtype=np.uint8)
    rgb[0] = 0; rgb[-1] = 255
    rgb[:, 0] = [0, 128, 255]; rgb[:, -1] = [255, 0, 128]
    weights = rng.integers(-128, 128, (16, 3, 3, 3), dtype=np.int16).astype(np.int8)
    biases = np.arange(16, dtype=np.int64)*4096-32768
    mul = base.words("multipliers.hex", 32)[:16]
    shifts = base.words("controls.hex", 32)[:16]
    post_mul, post_shift = 16777191, 28
    source = (rgb.astype(np.int16)-128).astype(np.int8)
    acc = integer.conv2d(source, weights, biases, stride=2, padding=1)
    pre = integer.requantize(acc, mul, shifts, -32768, 32767)
    active = integer.silu(pre)
    stem = integer.requantize(active.astype(np.int32), post_mul, post_shift).astype(np.int8)
    assert stem.shape == (144, 256, 16)
    dw_weights = base.words("dw_weights.hex", 8).astype(np.int8).reshape(16, 1, 3, 3)
    pw_weights = base.words("pw_weights.hex", 8).astype(np.int8).reshape(24, 16, 1, 1)
    multipliers, controls = base.words("multipliers.hex", 32), base.words("controls.hex", 32)
    def stages(values, channels, layer):
        before = integer.requantize(values, multipliers[channels], controls[channels], -32768, 32767)
        activated = integer.silu(before)
        after = integer.requantize(activated.astype(np.int32), controls[40+layer], controls[42+layer])
        return np.stack((before, activated, after), axis=-1)
    dw_acc = integer.conv2d(stem, dw_weights, base.words("dw_biases.hex", 32), stride=2, padding=1, groups=16)
    dw_stage = stages(dw_acc, slice(0, 16), 0)
    pw_acc = integer.conv2d(dw_stage[..., 2].astype(np.int8), pw_weights, base.words("pw_biases.hex", 32))
    pw_stage = stages(pw_acc, slice(16, 40), 1)
    padded_rgb = np.pad(source, ((1, 1), (1, 1), (0, 0)))
    # 同一 OIHW 权重依照硬件 27 项顺序划为 4 组，证明全部 tile 映射。
    errors = 0
    for ty in range(36):
        for tx in range(64):
            halo = padded_rgb[ty*8:ty*8+9, tx*8:tx*8+9]
            patch = np.lib.stride_tricks.sliding_window_view(halo.astype(np.int64), (3, 3), axis=(0, 1))[::2, ::2]
            operands = patch.reshape(16, 27)
            accum = operands @ weights.reshape(16, 27).astype(np.int64).T + biases
            errors += int(np.count_nonzero(accum.reshape(4, 4, 16) != acc[ty*4:ty*4+4, tx*4:tx*4+4]))
    assert errors == 0
    padded_stem = np.pad(stem, ((1, 1), (1, 1), (0, 0)))
    halos = [padded_stem[ty*8:ty*8+9, tx*8:tx*8+9] for ty in range(18) for tx in range(32)]
    def emit(name, values, bits):
        # 分批格式化，避免百万行文本和逐行 Python 字符串同时驻留。
        flat = np.asarray(values).ravel()
        mask = (1 << bits)-1
        with (out / name).open("w", encoding="ascii") as stream:
            for begin in range(0, flat.size, 8192):
                stream.writelines(f"{int(value) & mask:0{bits//4}x}\n" for value in flat[begin:begin+8192])
    emit("rgb.hex", rgb, 8)
    emit("stem_weights.hex", weights, 8); emit("stem_biases.hex", biases, 32)
    emit("stem_multipliers.hex", mul, 32); emit("stem_shifts.hex", shifts, 32)
    emit("stem_post.hex", [post_mul, post_shift], 32)
    emit("stem_acc.hex", tiled(acc), 32)
    emit("stem_stages.hex", tiled(np.stack((pre, active, stem), axis=-1).reshape(144, 256, 48)), 32)
    emit("input_tiled.hex", tiled(stem), 8)
    emit("halos.hex", halos, 8)
    emit("acc.hex", np.concatenate((tiled(dw_acc).reshape(576, 256), tiled(pw_acc).reshape(576, 384)), axis=1), 32)
    emit("stages.hex", np.concatenate((tiled(dw_stage.reshape(72, 128, 48)).reshape(576, 256, 3),
                                      tiled(pw_stage.reshape(72, 128, 72)).reshape(576, 384, 3)), axis=1), 32)
    emit("output_tiled.hex", tiled(pw_stage[..., 2]), 8)
    for name in ("silu.hex", "dw_weights.hex", "pw_weights.hex", "dw_biases.hex", "pw_biases.hex", "multipliers.hex", "controls.hex"):
        shutil.copyfile(base.FIXTURE / name, out / name)
    np.save(out / "expected_stem_hwc.npy", stem)
    np.save(out / "expected_pw_hwc.npy", pw_stage[..., 2].astype(np.int8))
    save(ROOT / "reference.json", {"status": "PASS", "parameters": "TEST_ONLY, not deployment QAT",
         "stem_tiles": 2304, "down2_tiles": 576, "local_vs_whole_mismatches": errors,
         "stem_output_bytes": int(stem.size), "down2_output_bytes": int(pw_acc.size),
         "stem_unique_values": int(np.unique(stem).size), "stem_groups": 4, "valid_products_per_lane": 27,
         "last_input_mask": 7, "last_output_mask": 1,
         "centering": "RTL halo kind0 applies pixel XOR 128; kind1 writes operator zero; down2 unchanged INT8",
         "layout": "tile4x4_hwc, no channel padding; actual Stem export populates downstream memory",
         "stem_post_multiplier": post_mul, "stem_post_shift": post_shift,
         "hashes": {path.name: sha(path) for path in out.iterdir()}})
    check()
    print("REFERENCE_PASS stem_tiles=2304 down2_tiles=576 mapping_mismatches=0", flush=True)


def gate():
    work = fresh("gate")
    entry = f"import sys;sys.path.insert(0,{str(base.SKILL)!r});from scripts.python.validation.generated_deliverable_gate import main;raise SystemExit(main())"
    for directory in ("rtl", "tests"):
        command([sys.executable, "-B", "-X", "utf8", "-c", entry, ROOT / directory,
                 "--include-testbench", "--external-interface-source", base.CORE,
                 "--json", work / (directory + ".json"), "--markdown", work / (directory + ".md")],
                 work, directory, allowed=(0, 1, 2))
    check()


def specifications():
    work = fresh("specifications")
    source = ROOT / "rtl/road_stem_tile_scheduler.v"
    ports = []
    for direction, high, name in re.findall(r"\b(input|output)\s+(?:signed\s+)?(?:\[(\d+):0\])?\s*(\w+)\s*[,\n]", source.read_text(encoding="utf-8")):
        if "load" in name:
            description = "仅 IDLE 接受的顺序装载；kind0 原始 RGB 中心化一次，kind1 为 padding 零，kind2至6为参数。"
        elif "mac" in name:
            description = "连接冻结 8输入乘3输出 MAC；每 batch 四组，末输入掩码07，尾输出通道仅一路有效。"
        elif "pp" in name:
            description = "连接冻结后处理；tag低8位为像素乘16加通道；保持有效负载直至握手。"
        elif "output" in name or "export" in name:
            description = "完整 tile 才可在 IDLE 请求导出；256个缓存元素按索引输出，反压期间保持。"
        elif name == "i_rstn":
            description = "异步低有效取消全部有效性；算术模块必须同复位，释放后重新装载1024项表和参数。"
        elif name == "i_clk":
            description = "单同步时钟域；100MHz仅为功能仿真时钟，不是物理签核。"
        else:
            description = "仅表及六类装载完整且无故障才能启动；busy核心窗口，done单拍，fault粘滞。"
        ports.append({"name": name, "direction": direction, "width": int(high)+1 if high else 1,
                      "clock_domain": "i_clk", "role": name, "description": description})
    assert len(ports) == 47, len(ports)
    waveform = {"signal": [{"name":"clk","wave":"p......."},
        {"name":"halo_complete","wave":"0...1..."}, {"name":"start","wave":"010.10.."},
        {"name":"busy","wave":"0....1.0"}]}
    module = {"name": "road_stem_tile_scheduler", "feature": "stem_handoff", "rtl_path": source.name,
        "description": "固定3×3 stride2 Stem tile调度，算子外置；功能优先，单batch顺序执行。",
        "interfaces": {"protocol":"discrete", "ports":ports}, "parameters":[],
        "clock":{"name":"i_clk","edge":"posedge","frequency_hz":100000000},
        "reset":{"name":"i_rstn","active":"low","synchronous":False,
                 "values":"立即取消状态、所有loaded标志、输出有效性；缓存不清零；完整重装表和参数后再启动。"},
        "behavior":["加载243项halo，432权重、16偏置、16乘数、16移位、2项post；依序加载各类，重新从地址0加载即撤销完整标志。",
            "4×4×16输出；每像素六个输出batch，前三路并行，最后仅一路；每路27项四组归约。",
            "PREPARE注册操作数，SEND保持到MAC接受，末组转MAC_WAIT；结果握手进入POST_WAIT；真实提交完成后ADVANCE。",
            "输入与输出保持到ready；done不能视为export接受；必须IDLE发起导出。",
            "核心周期按busy计数，不含load、done和export；无跨batch重叠。"],
        "constraints":["外部MAC、后处理及本调度器同复位；单batch最多27有效乘积，未扩大192上限。",
            "TEST_ONLY系数；不代表QAT模型精度，无物理时序或DDR保证。"],
        "corner_cases":["部分halo、尾输出mask001、末输入mask07、边界operator-zero、反压和复位取消。"],
        "verification_cases":["2304个Stem tile全阶段及完整589824字节输出，再输入真实576个down2 tile。"],
        "timing_diagrams":[{"id":"partial","title":"完整性准入","scenario":"partial",
            "description":"压缩示意，不表示真实核心延迟；第一次start被拒绝，完整后接受。", "wavejson":waveform}]}
    save(ROOT / "rtl/contract.json", {"modules":[module]})
    entry = f"import sys;sys.path.insert(0,{str(base.SKILL)!r});from scripts.python.workflow.cli import main;raise SystemExit(main())"
    command([sys.executable,"-B","-X","utf8","-c",entry,"write-spec","--spec",ROOT/"rtl/contract.json",
        "--source",source,"--out-dir",work,"--no-state"],ROOT,str(work.relative_to(ROOT)/"rtl"),allowed=(0,1,2))
    generated = work / "spec/stem_handoff/road_stem_tile_scheduler_spec.md"
    assert generated.exists(), "Canonical spec failed; inspect rtl.log"
    shutil.copyfile(generated, source.with_name(source.stem+"_spec.md"))
    shutil.copytree(generated.parent/"waveforms",ROOT/"rtl/waveforms",dirs_exist_ok=True)
    tb = dict(module, name="tb_stem_down2", rtl_path="tb_stem_down2.v",
              description="Portless testbench with actual intermediate tensor handoff, not DDR",
              interfaces={"protocol":"discrete","ports":[]})
    save(ROOT/"tests/contract.json",{"modules":[tb]})
    output = command([sys.executable,"-B","-X","utf8","-c",entry,"write-spec","--spec",ROOT/"tests/contract.json",
        "--source",ROOT/"tests/tb_stem_down2.v","--out-dir",work,"--no-state"],ROOT,str(work.relative_to(ROOT)/"tb"),allowed=(0,1,2))
    assert "ports must be non-empty" in output
    save(work/"limitation.json",{"status":"BLOCKED_PORTLESS_TB", "fake_ports_added":False,
         "manual_companion":"tests/tb_stem_down2_spec.md", "waveform":"../rtl/waveforms/road_stem_tile_scheduler_partial.svg"})


def finish():
    check()
    simulation = ROOT / "simulation_attempt3"
    receipt = json.loads((simulation/"receipt.json").read_text(encoding="utf-8"))
    assert receipt["status"] == "PASS" and len(receipt["results"]) == 2
    for name, digest in receipt["source_hashes"].items():
        snapshot = Path(name)
        live = ROOT/("rtl" if snapshot.name.startswith("road_") else "tests")/snapshot.name
        assert sha(snapshot) == digest == sha(live), live
    reference = json.loads((ROOT/"reference.json").read_text(encoding="utf-8"))
    for name, digest in reference["hashes"].items():
        assert sha(ROOT/"vectors"/name) == digest, name
    ast.parse((ROOT/"run.py").read_text(encoding="utf-8"))
    dependency = json.loads((BASE/"frozen.json").read_text(encoding="utf-8"))
    assert all(sha(Path(path)) == digest for path, digest in dependency.items()), "Old core closure changed"
    save(ROOT/"dependency_check.json", {"checked":len(dependency),"changed":[],"hashes":dependency,
         "tools_and_vendor":{str(path):sha(path) for path in
            [Path(v) for v in receipt["vendor_models"]]+[base.MSIM/"vlog.exe",base.MSIM/"vsim.exe"]}})
    cycles = {}
    for mode in ("normal","stalls"):
        cycles[mode] = {}
        for layer, filename, count in (("stem",mode+".csv.stem.csv",2304),("down2",mode+".csv",576)):
            with (simulation/filename).open(encoding="utf-8") as stream:
                rows=list(csv.DictReader(stream))
            assert len(rows) == count
            totals={key:sum(int(row[key]) for row in rows) for key in rows[0] if key!="tile"}
            assert sum(totals[f"bin{i}"] for i in range(8)) == totals["core"]
            cycles[mode][layer] = dict(totals, core_min=min(int(row["core"]) for row in rows),
                                      core_max=max(int(row["core"]) for row in rows))
    gate_dir=ROOT/"gate_attempt2"
    gates={name:json.loads((gate_dir/(name+".json")).read_text(encoding="utf-8")) for name in ("rtl","tests")}
    save(ROOT/"cycle_summary.json",cycles)
    save(ROOT/"status.json",{"status":"FUNCTIONAL_HANDOFF_PASS_NOT_DEPLOYMENT_READY",
        "reference":"reference.json","simulation":"simulation_attempt3/receipt.json",
        "actual_handoff":True,"stem_tiles":2304,"down2_tiles":576,"tensor_mismatches":0,
        "strict_gate":{name:{"errors":g["errors"],"strict_warnings":g["strict_warnings"],
                             "checks":g["checks"],"report":str((gate_dir/(name+".json")).relative_to(ROOT))}
                        for name,g in gates.items()},
        "old_artifacts_unchanged":167,"frozen_dependency_count":len(dependency),
        "not_done":["Stem cancellation and fault injection regression","shared-operator hardware top",
                    "actual DDR interface loop","TD synthesis and timing for new scheduler","deployment QAT model","full CNN and board FPS"],
        "next":"Actual DDR transfer contract inspection, then bounded simulation loop; no guessed write visibility"})
    save(ROOT/"artifact_manifest.json", {str(path):sha(path) for path in sorted(ROOT.rglob("*"))
         if path.is_file() and path.name!="artifact_manifest.json" and path.suffix not in (".wlf",".pyc")})
    print("FROZEN_FUNCTIONAL_HANDOFF_PASS",flush=True)


def simulate():
    check()
    work = fresh("simulation")
    sources = work / "sources"
    sources.mkdir()
    for directory in ("rtl", "tests"):
        for path in (ROOT / directory).iterdir():
            if path.suffix in (".v", ".vh"):
                shutil.copyfile(path, sources / path.name)
    previous = ROOT.parent / "mac_ce_fanout_local_20261010/shell_rtl/vlog.command.json"
    vendor = [path for path in json.loads(previous.read_text())["command"] if "sim_release" in str(path)]
    command([base.MSIM / "vlib.exe", "work"], work, "vlib")
    command([base.MSIM / "vlog.exe", "-work", "work", "+incdir+" + sources.as_posix(),
             *vendor, *sorted(base.CORE.glob("*.v")), *sorted(sources.glob("*.v"))], work, "vlog")
    results = []
    for mode in ("normal", "stalls"):
        print("SIMULATING", mode, flush=True)
        output = command([base.MSIM / "vsim.exe", "-c", "-lib", "work", "PH1P_PHY_GSR", "tb_stem_down2",
             "+VECTORS=" + (ROOT / "vectors").as_posix(), "+MODE=" + mode,
             "+REPORT=" + (work / (mode + ".csv")).as_posix(),
             "+DUMP=" + (work / (mode + "_output.hex")).as_posix(), "-do",
             "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"], work, mode)
        assert "TB_PASS_STEM_DOWN2" in output
        actual = np.array([int(v, 16) for v in (work / (mode + "_output.hex")).read_text().split()], dtype=np.uint8)
        actual = actual.view(np.int8).reshape(18, 32, 4, 4, 24).transpose(0, 2, 1, 3, 4).reshape(72, 128, 24)
        assert np.array_equal(actual, np.load(ROOT / "vectors/expected_pw_hwc.npy"))
        results.append({"mode": mode, "status": "PASS", "mismatches": 0,
                        "lines": [line for line in output.splitlines() if "STEM_TOTAL" in line or "TB_PASS_STEM_DOWN2" in line]})
        save(work / "receipt.json", {"status": "PASS" if len(results) == 2 else "PARTIAL", "results": results,
             "source_hashes": {str(path): sha(path) for path in sources.iterdir()},
             "reference_sha256": sha(ROOT / "reference.json"), "vendor_models": vendor})
        print("SIM_PASS", mode, flush=True)
    check()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "check", "gate", "specifications", "simulate", "finish"))
    globals()[parser.parse_args().action]()
