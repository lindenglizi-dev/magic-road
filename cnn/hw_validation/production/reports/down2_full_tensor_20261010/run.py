"""完整 down2 验证；只写本目录，冻结核不修改，不训练、不生成位流。"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

import numpy as np

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[4]
CORE = ROOT.parent / "board_selftest_20261010/core"
FIXTURE = ROOT.parent / "board_selftest_20261010/vectors"
GRAPH = PROJECT / "cnn/hw_validation/production/graph_artifacts/graph.json"
SKILL = Path("C:/Users/lenovo/.codex/skills/readable-verilog-generator")
MSIM = Path("D:/modeltech64_2020.4/win64")
sys.path.insert(0, str(PROJECT))
from cnn import integer


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def save(path, value):
    path.resolve().relative_to(ROOT)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def fresh(name):
    target = ROOT / name
    counter = 1
    while target.exists():
        counter += 1
        target = ROOT / f"{name}_attempt{counter}"
    target.mkdir(parents=True)
    return target


def command(args, work, name, allowed=(0,)):
    work.resolve().relative_to(ROOT)
    log = work / (name + ".log")
    assert not log.exists(), log
    started = time.monotonic()
    record = {"command": list(map(str, args)), "cwd": str(work)}
    try:
        with log.open("w", encoding="utf-8") as output:
            result = subprocess.run(record["command"], cwd=work, stdout=output,
                                    stderr=subprocess.STDOUT, timeout=1800, check=False)
        record["returncode"] = result.returncode
    except (OSError, subprocess.TimeoutExpired) as error:
        record["error"] = str(error)
        raise
    finally:
        record["seconds"] = time.monotonic() - started
        save(work / (name + ".command.json"), record)
    assert result.returncode in allowed, (log, record)
    return log.read_text(encoding="utf-8", errors="replace")


def check():
    frozen = json.loads((ROOT / "frozen.json").read_text(encoding="utf-8"))
    changed = [name for name, digest in frozen.items() if sha(Path(name)) != digest]
    save(ROOT / "frozen_check.json", {"checked": len(frozen), "changed": changed})
    assert not changed, changed


def freeze():
    assert not (ROOT / "frozen.json").exists(), "不覆盖已冻结基线"
    paths = [*CORE.glob("*.v"), *FIXTURE.glob("*.hex"), GRAPH, Path(integer.__file__),
             PROJECT / "cnn/hw_validation/production/deployment_contract.json",
             PROJECT / "user_source/hdl_source/top.v"]
    paths = [path for path in paths if path.exists()]
    save(ROOT / "frozen.json", {str(path): sha(path) for path in paths})
    save(ROOT / "scope.json", {"coefficients": "TEST_ONLY_dynamic_stress",
         "kernel_modified": False, "production_modified": False,
         "board_or_bitstream_or_training": False,
         "full_layer_orchestration": "testbench, not synthesizable DDR sequencer",
         "physical_resources": "not remeasured: no design RTL changed"})
    check()


def words(name, bits):
    raw = np.array([int(value, 16) for value in (FIXTURE / name).read_text().split()], dtype=np.int64)
    return np.where(raw >= 1 << (bits - 1), raw - (1 << bits), raw)


def emit(directory, name, values, bits):
    mask = (1 << bits) - 1
    (directory / name).write_text("".join(f"{int(value) & mask:0{bits//4}x}\n"
                                        for value in np.asarray(values).ravel()), encoding="ascii")


def tiled(tensor):
    height, width, channels = tensor.shape
    assert height % 4 == 0 and width % 4 == 0
    return tensor.reshape(height//4, 4, width//4, 4, channels).transpose(0, 2, 1, 3, 4).copy()


def prepare():
    """整张参考与局部 halo 独立比较，再发布仿真输入。"""
    check()
    out = ROOT / "vectors"
    assert not out.exists(), "向量只发布一次"
    out.mkdir()
    graph = json.loads(GRAPH.read_text(encoding="utf-8"))
    stem, dw, pw = graph["nodes"][:3]
    assert [node["name"] for node in (stem, dw, pw)] == ["stem.conv", "down2.dw.conv", "down2.pw.conv"]
    assert stem["output_shape_hwc"] == dw["input_shape_hwc"] == [144, 256, 16]
    assert dw["stride"] == [2, 2] and dw["padding"] == [1, 1]
    assert pw["output_shape_hwc"] == [72, 128, 24] and pw["padding"] == [0, 0]
    rng = np.random.default_rng(42)
    image = rng.integers(-128, 128, (144, 256, 16), dtype=np.int16).astype(np.int8)
    # 明确覆盖极值和跨 tile 边界；输入不是来自训练模型的 Stem。
    image[0, :, :] = -128
    image[-1, :, :] = 127
    image[:, 0, :] = np.arange(16, dtype=np.int8) - 8
    image[:, -1, :] = np.arange(16, dtype=np.int8) * 7 - 56
    weight_dw = words("dw_weights.hex", 8).astype(np.int8).reshape(16, 1, 3, 3)
    weight_pw = words("pw_weights.hex", 8).astype(np.int8).reshape(24, 16, 1, 1)
    biases = (words("dw_biases.hex", 32), words("pw_biases.hex", 32))
    multipliers, controls = words("multipliers.hex", 32), words("controls.hex", 32)
    acc_dw = integer.conv2d(image, weight_dw, biases[0], stride=2, padding=1, groups=16)
    def stages(acc, channel_slice, layer):
        pre = integer.requantize(acc, multipliers[channel_slice], controls[channel_slice], -32768, 32767)
        active = integer.silu(pre)
        post = integer.requantize(active.astype(np.int32), controls[40+layer], controls[42+layer])
        return np.stack((pre, active, post), axis=-1)
    stage_dw = stages(acc_dw, slice(0, 16), 0)
    acc_pw = integer.conv2d(stage_dw[..., 2].astype(np.int8), weight_pw, biases[1])
    stage_pw = stages(acc_pw, slice(16, 40), 1)
    padded = np.pad(image, ((1, 1), (1, 1), (0, 0)))
    halos, padding_counts = [], []
    for ty in range(18):
        for tx in range(32):
            halo = padded[ty*8:ty*8+9, tx*8:tx*8+9]
            assert halo.shape == (9, 9, 16)
            # 独立局部矢量化求和，不复用整张 conv2d 的循环和地址公式。
            patch = np.lib.stride_tricks.sliding_window_view(halo.astype(np.int64), (3, 3), axis=(0, 1))[::2, ::2]
            local_acc = (patch * weight_dw[:, 0]).sum(axis=(-1, -2)) + biases[0]
            ys, xs = slice(ty*4, ty*4+4), slice(tx*4, tx*4+4)
            assert np.array_equal(local_acc, acc_dw[ys, xs]), (ty, tx, "DW")
            local_dw = stages(local_acc, slice(0, 16), 0)[..., 2]
            local_pw = local_dw @ weight_pw[:, :, 0, 0].astype(np.int64).T + biases[1]
            assert np.array_equal(local_pw, acc_pw[ys, xs]), (ty, tx, "PW")
            halos.append(halo)
            padding_counts.append(sum(16 for y in range(9) for x in range(9)
                                      if not (0 <= ty*8+y-1 < 144 and 0 <= tx*8+x-1 < 256)))
    all_acc = np.concatenate((tiled(acc_dw).reshape(576, 256), tiled(acc_pw).reshape(576, 384)), axis=1)
    all_stages = np.concatenate((tiled(stage_dw.reshape(72, 128, 48)).reshape(576, 256, 3),
                                tiled(stage_pw.reshape(72, 128, 72)).reshape(576, 384, 3)), axis=1)
    emit(out, "input_tiled.hex", tiled(image), 8)
    emit(out, "halos.hex", halos, 8)
    emit(out, "acc.hex", all_acc, 32)
    emit(out, "stages.hex", all_stages, 32)
    emit(out, "output_tiled.hex", tiled(stage_pw[..., 2]), 8)
    np.save(out / "input_hwc.npy", image)
    np.save(out / "expected_dw_hwc.npy", stage_dw[..., 2].astype(np.int8))
    np.save(out / "expected_pw_hwc.npy", stage_pw[..., 2].astype(np.int8))
    for name in ("silu.hex", "dw_weights.hex", "pw_weights.hex", "dw_biases.hex",
                 "pw_biases.hex", "multipliers.hex", "controls.hex"):
        shutil.copyfile(FIXTURE / name, out / name)
    save(ROOT / "reference.json", {"status": "PASS", "tiles": 576,
         "input_shape": list(image.shape), "dw_shape": list(acc_dw.shape), "pw_shape": list(acc_pw.shape),
         "reference_acc_items": int(all_acc.size), "reference_stage_items": int(all_stages.size),
         "output_bytes": int(acc_pw.size), "output_unique_values": int(np.unique(stage_pw[..., 2]).size),
         "local_vs_full_mismatches": 0, "padding_bytes": sum(padding_counts),
         "top_left_padding_bytes": padding_counts[0], "top_right_padding_bytes": padding_counts[31],
         "bottom_left_padding_bytes": padding_counts[544], "bottom_right_padding_bytes": padding_counts[575],
         "storage": {node["name"]: node["storage"] for node in (stem, dw, pw)},
         "coefficients": "TEST_ONLY, not real QAT", "seed": 42,
         "hashes": {path.name: sha(path) for path in out.iterdir() if path.is_file()}})
    check()
    print("REFERENCE_PASS full_tiles=576 local_vs_full=0", flush=True)


def gate():
    work = fresh("gate")
    entry = f"import sys;sys.path.insert(0,{str(SKILL)!r});from scripts.python.validation.generated_deliverable_gate import main;raise SystemExit(main())"
    command([sys.executable, "-B", "-X", "utf8", "-c", entry, ROOT / "tests", "--include-testbench",
             "--external-interface-source", CORE,
             "--json", work / "tests.json", "--markdown", work / "tests.md"], work, "tests", allowed=(0, 1, 2))
    check()


def specifications():
    work = fresh("specifications")
    entry = f"import sys;sys.path.insert(0,{str(SKILL)!r});from scripts.python.workflow.cli import main;raise SystemExit(main())"
    text = command([sys.executable, "-B", "-X", "utf8", "-c", entry, "write-spec",
                    "--spec", ROOT / "tests/contract.json", "--source", ROOT / "tests/tb_down2_full_tensor.v",
                    "--out-dir", work, "--no-state"], ROOT, str(work.relative_to(ROOT) / "canonical"), allowed=(0, 1, 2))
    assert "ports must be non-empty" in text, text
    save(work / "limitation.json", {"status": "BLOCKED_PORTLESS_TB", "fake_ports_added": False,
         "manual_companion": "tests/tb_down2_full_tensor_spec.md",
         "waveform": "tests/waveforms/full_layer.svg"})


def simulate():
    check()
    work = fresh("simulation")
    old = ROOT.parent / "mac_ce_fanout_local_20261010/shell_rtl/vlog.command.json"
    vendor = [path for path in json.loads(old.read_text())["command"] if "sim_release" in str(path)]
    snapshot = work / "sources"
    snapshot.mkdir()
    source_tb = snapshot / "tb_down2_full_tensor.v"
    shutil.copyfile(ROOT / "tests/tb_down2_full_tensor.v", source_tb)
    source_hashes = {str(path): sha(path) for path in [*CORE.glob("*.v"), source_tb]}
    command([MSIM / "vlib.exe", "work"], work, "vlib")
    command([MSIM / "vlog.exe", "-work", "work", *vendor, *sorted(CORE.glob("*.v")),
             source_tb], work, "vlog")
    results = []
    for mode in ("normal", "stalls"):
        print("SIMULATING", mode, flush=True)
        output = command([MSIM / "vsim.exe", "-c", "-lib", "work", "PH1P_PHY_GSR", "tb_down2_full_tensor",
             "+VECTORS=" + (ROOT / "vectors").as_posix(), "+MODE=" + mode,
             "+REPORT=" + (work / (mode + ".csv")).as_posix(),
             "+DUMP=" + (work / (mode + "_output.hex")).as_posix(), "-do",
             "onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0"], work, mode)
        assert "TB_PASS_DOWN2_FULL_TENSOR" in output, output[-4000:]
        actual = np.array([int(line, 16) for line in (work / (mode + "_output.hex")).read_text().split()], dtype=np.uint8)
        actual = actual.view(np.int8).reshape(18, 32, 4, 4, 24).transpose(0, 2, 1, 3, 4).reshape(72, 128, 24)
        expected = np.load(ROOT / "vectors/expected_pw_hwc.npy")
        assert np.array_equal(actual, expected), mode
        rows = list(csv.DictReader((work / (mode + ".csv")).open(encoding="utf-8")))
        assert len(rows) == 576 and [int(row["tile"]) for row in rows] == list(range(576))
        for row in rows:
            assert sum(int(row[f"bin{i}"]) for i in range(8)) == int(row["core"])
            assert int(row["dw_commits"]) == 256 and int(row["pw_commits"]) == int(row["exports"]) == 384
        totals = {key: sum(int(row[key]) for row in rows) for key in rows[0] if key != "tile"}
        np.save(work / (mode + "_actual_hwc.npy"), actual)
        results.append({"mode": mode, "tiles": 576, "mismatches": 0,
                        "core_min": min(int(row["core"]) for row in rows),
                        "core_max": max(int(row["core"]) for row in rows), "totals": totals,
                        "pass_line": [line for line in output.splitlines() if "TB_PASS_DOWN2_FULL_TENSOR" in line]})
        save(work / "receipt.json", {"status": "PARTIAL" if len(results) == 1 else "PASS", "results": results,
             "source_hashes": source_hashes,
             "vectors_manifest_sha256": sha(ROOT / "reference.json"), "vendor_models": vendor})
        print("SIM_PASS", mode, "cycles", totals["core"], flush=True)
    check()


def finish():
    """绑定最终源码、工具与完整输出，发布阶段状态而不是整机通过声明。"""
    check()
    candidates = sorted(ROOT.glob("simulation*/receipt.json"), key=lambda path: path.stat().st_mtime_ns)
    receipt_path = candidates[-1]
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    assert receipt["status"] == "PASS"
    assert sha(receipt_path.parent / "sources/tb_down2_full_tensor.v") == sha(ROOT / "tests/tb_down2_full_tensor.v")
    gate_paths = sorted(ROOT.glob("gate*/tests.json"), key=lambda path: path.stat().st_mtime_ns)
    gate_path = gate_paths[-1]
    gate_result = json.loads(gate_path.read_text(encoding="utf-8"))
    tracked = [ROOT / "run.py", ROOT / "reference.json", ROOT / "frozen.json", ROOT / "scope.json",
               ROOT / "tests/tb_down2_full_tensor.v", ROOT / "tests/tb_down2_full_tensor_spec.md",
               ROOT / "tests/contract.json", ROOT / "tests/waveforms/full_layer.json5",
               ROOT / "tests/waveforms/full_layer.svg", ROOT / "完整层验证报告与后续步骤.md",
               receipt_path, gate_path, gate_path.with_suffix(".md")]
    tracked += list((ROOT / "vectors").iterdir())
    tracked += [Path(path) for path in receipt["vendor_models"]]
    tracked += [MSIM / (name + ".exe") for name in ("vlib", "vlog", "vsim")]
    tracked += [path for path in receipt_path.parent.iterdir() if path.is_file() and path.suffix in (".json", ".csv", ".log", ".hex", ".npy")]
    tracked += [Path(path) for path in json.loads((ROOT / "frozen.json").read_text(encoding="utf-8"))]
    save(ROOT / "status.json", {"stage": "down2_full_tensor_testbench_PASS",
         "tiles": 576, "mismatches": 0, "duplicate_writes": 0, "missing_writes": 0,
         "receipt": str(receipt_path.relative_to(ROOT)), "gate": str(gate_path.relative_to(ROOT)),
         "strict_delivery_ready": gate_result["delivery_ready"], "strict_errors": gate_result["errors"],
         "next": "Stem to down2: add fixed Stem scheduler and validate actual inter-layer handoff",
         "not_yet_validated": ["synthesizable full-layer DMA sequencer", "Stem RTL integration",
                               "actual DDR", "complete CNN", "real QAT parameters", "video FPS"],
         "physical_run": False, "board_run": False, "new_bitstream": False})
    tracked.append(ROOT / "status.json")
    save(ROOT / "artifact_manifest.json", {str(path): sha(path) for path in tracked if path.is_file()})
    print("FROZEN_FULL_LAYER_PASS", receipt_path.parent.name, "files", len(set(tracked)), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("freeze", "prepare", "gate", "specifications", "simulate", "check", "finish"))
    globals()[parser.parse_args().action]()
