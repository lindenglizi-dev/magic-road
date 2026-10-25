"""数据-only：真实QAT的CSP2首个残差单元，禁止训练或隐含RTL执行。"""
from datetime import datetime
import hashlib
from pathlib import Path
import shutil
import time

import numpy as np
import torch

from cnn import integer
from cnn.hw_validation.production import export_qat_front3 as front
from cnn.hw_validation.production.graph import resolve_byte_address
from cnn.hw_validation.production.trained_integer import nonconv

base = front.base
OUT = front.OUT.parent / "qat_g10_csp_first_data_20261015_v1"
PRIOR = front.OUT.parent / "qat_g10_front3_paxi_20261015_v1"
LAYERS = ("csp2.blocks.0.dw.conv", "csp2.blocks.0.pw.conv")


def halo_window(source, origin=(0, 0), full_shape=(72, 128)):
    """只对真实图像越界补零；已知窗口之外的图像内数据必须报错。"""
    if source.dtype != np.int8 or source.shape != (8, 8, 24):
        raise ValueError("expected verified top-left8x8x24 INT8 window")
    if any(not isinstance(v, int) or v < 0 or v % 4 for v in origin):
        raise ValueError("output origin must be nonnegative tile-aligned")
    if any(origin[i] + 4 > full_shape[i] for i in (0, 1)):
        raise ValueError("output tile outside true tensor")
    result = np.zeros((6, 6, 12), dtype=np.int8)
    for row, col in np.ndindex(6, 6):
        y, x = origin[0] + row - 1, origin[1] + col - 1
        if not (0 <= y < full_shape[0] and 0 <= x < full_shape[1]):
            continue
        if not (0 <= y < source.shape[0] and 0 <= x < source.shape[1]):
            raise ValueError("missing real halo context; not an image-padding boundary")
        result[row, col] = source[y, x, 12:24]
    return result


def add_residual(bypass, branch):
    if bypass.dtype != np.int8 or branch.dtype != np.int8 or bypass.shape != branch.shape:
        raise ValueError("residual requires equally-shaped INT8 operands")
    total = bypass.astype(np.int16) + branch.astype(np.int16)
    return total, np.clip(total, -128, 127).astype(np.int8)


def address(base_address, width, channels, y, x, c):
    """与图视图解析独立的tile4x4_hwc单字节地址公式。"""
    return base_address + (((y // 4) * ((width + 3) // 4) + x // 4) * 16 +
                           (y % 4) * 4 + x % 4) * channels + c


def pack(values, bits):
    return sum((int(value) & ((1 << bits) - 1)) << (i * bits) for i, value in enumerate(values))


def mac_task(activations, weights, biases, coordinates):
    """编码现有64/192/96位接口，尾输入lane补零，不修改MAC协议。"""
    count = len(activations)
    if not 1 <= count <= 192 or weights.shape != (3, count) or biases.shape != (3,):
        raise ValueError("invalid three-lane MAC task")
    groups = []
    for start in range(0, count, 8):
        valid = min(8, count - start)
        act = np.zeros(8, dtype=np.int8)
        weight = np.zeros((3, 8), dtype=np.int8)
        act[:valid], weight[:, :valid] = activations[start:start+valid], weights[:, start:start+valid]
        groups.append(dict(activation_hex=f"{pack(act, 8):016x}", weight_hex=f"{pack(weight.ravel(), 8):048x}",
                           bias_hex=f"{pack(biases, 32):024x}", input_mask=(1 << valid)-1,
                           first=start == 0, last=start+valid == count))
    return dict(coordinates=coordinates, output_mask=sum(1 << i for i, c in enumerate(coordinates) if c is not None),
                groups=groups)


def mac_tasks(halo, dw_post, dw, pw):
    tasks = []
    for y, channel, start_x in np.ndindex(4, 12, 2):
        x = start_x * 3
        lanes = min(3, 4-x)
        union_width = lanes + 2
        act = halo[y:y+3, x:x+union_width, channel].ravel()
        weight = np.zeros((3, len(act)), dtype=np.int8)
        bias = np.zeros(3, dtype=np.int32)
        coords = [None]*3
        for lane in range(lanes):
            for ky, kx in np.ndindex(3, 3):
                weight[lane, ky*union_width+lane+kx] = dw["weights"][channel, 0, ky, kx]
            bias[lane], coords[lane] = dw["bias"][channel], [y, x+lane, channel]
        tasks.append(dict(layer="dw", **mac_task(act, weight, bias, coords)))
    for y, x, output_group in np.ndindex(4, 4, 4):
        channels = np.arange(output_group*3, output_group*3+3)
        tasks.append(dict(layer="pw", **mac_task(dw_post[y, x], pw["weights"][channels, :, 0, 0],
                                                 pw["bias"][channels], [[y, x, int(c)] for c in channels])))
    return tasks


def verify_mac_tasks(tasks, goldens):
    """独立按HEX端口解码归约，每个有效输出必须恰好一次命中golden。"""
    seen = set()
    for task in tasks:
        result = [0, 0, 0]
        for index, group in enumerate(task["groups"]):
            if group["first"] != (index == 0) or group["last"] != (index == len(task["groups"])-1):
                raise ValueError("MAC first/last mismatch")
            act, weight, bias = (int(group[name], 16) for name in ("activation_hex", "weight_hex", "bias_hex"))
            signed = lambda value, bits: value - (1 << bits) if value & (1 << (bits-1)) else value
            for lane in range(3):
                if group["first"]:
                    result[lane] = signed((bias >> (32*lane)) & 0xffffffff, 32)
                for slot in range(8):
                    a = signed((act >> (slot*8)) & 255, 8)
                    w = signed((weight >> ((lane*8+slot)*8)) & 255, 8)
                    if group["input_mask"] & (1 << slot):
                        result[lane] += a*w
                    elif a or w:
                        raise ValueError("nonzero masked input lane")
                if not -(1 << 32) <= result[lane] < (1 << 32):
                    raise OverflowError("signed33 partial overflow")
        for lane, coord in enumerate(task["coordinates"]):
            if bool(task["output_mask"] & (1 << lane)) != (coord is not None):
                raise ValueError("MAC output mask mismatch")
            if coord is None:
                if result[lane] != 0:
                    raise ValueError("inactive output not zero")
                continue
            key = (task["layer"], *coord)
            if key in seen or result[lane] != int(goldens[task["layer"]][tuple(coord)]):
                raise ValueError("MAC duplicate or accumulator mismatch")
            seen.add(key)
    if len(seen) != sum(array.size for array in goldens.values()):
        raise ValueError("MAC output coverage hole")
    return len(seen)


def run():
    started = time.perf_counter()
    front.check_hashes(front.PINNED)
    binding = base.read(PRIOR / "input_binding.json")
    frozen = {**binding["original_sha256"], **binding["staged_sha256"]}
    prior_receipt = base.read(PRIOR / "verification_receipt.json")
    frozen.update({str(PRIOR / name): sha for name, sha in prior_receipt["sha256"].items()})
    if base.read(PRIOR / "status.json")["status"] != "PASS_REAL_QAT_FRONT3_PAXI_2_OF_2":
        raise ValueError("previous two-clock prerequisite failed")
    input_path = front.OUT / "parameters/expected_pw_hwc.npy"
    source_paths = [Path(__file__), Path(__file__).with_name("test_export_qat_csp_first.py"),
                    Path(front.__file__), Path(integer.__file__),
                    Path(__file__).with_name("graph.py"), Path(__file__).with_name("trained_integer.py")]
    frozen.update({str(path): front.sha256(path) for path in [*source_paths, input_path,
                    PRIOR / "verification_receipt.json", PRIOR / "status.json"]})
    front.check_hashes(frozen)
    model, manifest = front.load_package(front.PACKAGE)
    nodes = model.graph["nodes"][3:7]
    if [n["name"] for n in nodes] != ["split.00", *LAYERS, "residual.00"]:
        raise ValueError("unexpected frozen CSP graph boundary")
    if any(model.scales[name] != model.scales["down2.pw.conv"] for name in
           ("split.00.0", "split.00.1", LAYERS[1], "residual.00")):
        raise ValueError("split/residual scales not aligned")
    OUT.mkdir(exist_ok=False)
    for folder in ("parameters", "vectors", "sources", "inputs"):
        (OUT / folder).mkdir()
    for path in source_paths:
        shutil.copy2(path, OUT / "sources" / path.name)
    for name in ("manifest.json", "numeric_test.bin", "numeric_test_padded.bin"):
        shutil.copy2(front.PACKAGE / name, OUT / "inputs" / name)
    base.save(OUT / "graph_segment.json", dict(nodes=nodes, graph_sha256=front.sha256(
        base.PROJECT / "cnn/hw_validation/production/graph_artifacts/graph.json")))
    physical = (front.PACKAGE / "numeric_test_padded.bin").read_bytes()
    parameters, fields, bounds = {}, [], {}
    for segment in manifest["segments"]:
        name = segment["name"]
        if not (any(name.startswith(layer + ".") for layer in LAYERS) or name == "shared.silu"):
            continue
        raw = front.word_bytes(physical, segment["offset"], segment["length"])
        if hashlib.sha256(raw).hexdigest() != segment["sha256"]:
            raise ValueError("parameter ROM segment mismatch")
        dtype = {"int8": "i1", "int32_le": "<i4", "uint8": "u1", "<i2": "<i2"}[segment["dtype"]]
        values = np.frombuffer(raw, dtype=dtype).copy().reshape(segment["shape"])
        fields.append(dict(name=name, offset=segment["offset"], bytes=len(raw), sha256=segment["sha256"]))
        if name == "shared.silu":
            lut = values
            front.emit(OUT / "parameters/silu.hex", values, 16)
        else:
            layer, field = name.rsplit(".", 1)
            np.testing.assert_array_equal(values, model.parameters[layer][field])
            parameters.setdefault(layer, {})[field] = values
            prefix = "dw" if layer == LAYERS[0] else "pw"
            front.emit(OUT / "parameters" / f"{prefix}_{field}.hex", values,
                       8 if field in ("weights", "pre_shift", "post_shift") else 32)
    if len(fields) != 13 or sum(row["bytes"] for row in fields) != 2526:
        raise ValueError("expected12 parameter fields plus shared SiLU")
    for layer, params in parameters.items():
        bound = np.abs(params["bias"].astype(np.int64)) + 128*np.abs(params["weights"].astype(np.int64)).sum((1, 2, 3))
        if np.any(bound >= 1 << 31):
            raise OverflowError("INT32 final/signed33 partial bound failed")
        bounds[layer] = int(bound.max())
    source = np.load(input_path, allow_pickle=False)
    tiled = np.concatenate([source[y:y+4, x:x+4].ravel() for y, x in ((0, 0), (0, 4), (4, 0), (4, 4))])
    previous_pw = np.array([int(v, 16) for v in (PRIOR / "vectors/pw_golden.hex").read_text().split()][:1536])
    np.testing.assert_array_equal(tiled.astype(np.int16) & 255, previous_pw)
    np.save(OUT / "inputs/input_pw_hwc.npy", source, allow_pickle=False)
    split = nonconv(nodes[0], {"down2.pw.conv": source})
    halo = halo_window(source)
    dw, pw = (parameters[layer] for layer in LAYERS)
    dw_stages = front.stage(halo, dw, lut, manifest["silu_upper"], 1, 0, 12)
    pw_stages = front.stage(dw_stages[-1], pw, lut, manifest["silu_upper"], 1, 0, 1)
    bypass = split["split.00.1"][:4, :4].copy()
    total, residual = add_residual(bypass, pw_stages[-1])
    values = dict(split_passthrough=split["split.00.0"][:4, :4], bypass=bypass,
                  residual_sum=total, residual_post=residual)
    comparisons = []
    for prefix, params, image, expected, groups in (("dw", dw, halo, dw_stages, 12),
            ("pw", pw, dw_stages[-1], pw_stages, 1)):
        acc = integer.conv2d(image, params["weights"], params["bias"], 1, 0, groups)
        pre = integer.requantize(acc, params["pre_multiplier"], params["pre_shift"], -32768, 32767).astype(np.int16)
        activated = integer.silu(pre)
        post = integer.requantize(activated, params["post_multiplier"], params["post_shift"]).astype(np.int8)
        for name, oracle, scalar in zip(("acc", "pre", "silu", "post"), expected,
                                      (acc, pre, activated, post), strict=True):
            np.testing.assert_array_equal(oracle, scalar)
            values[f"{prefix}_{name}"] = oracle
            comparisons.append(dict(stage=f"{prefix}_{name}", values=int(oracle.size), exact=True))
    # Larger known window computes independently with true top/left padding;
    # only its top-left4x4 output is used, never its artificial bottom/right edge.
    larger_dw = front.stage(split["split.00.1"], dw, lut, manifest["silu_upper"], 1, 1, 12)
    larger_pw = front.stage(larger_dw[-1], pw, lut, manifest["silu_upper"], 1, 0, 1)
    for actual, expected in zip((*dw_stages, *pw_stages), (*larger_dw, *larger_pw), strict=True):
        np.testing.assert_array_equal(actual, expected[:4, :4])
    scalar_residual = nonconv(nodes[3], {"split.00.1": bypass, LAYERS[1]: pw_stages[-1]})["residual.00"]
    np.testing.assert_array_equal(residual, scalar_residual)
    tasks = mac_tasks(halo, dw_stages[-1], dw, pw)
    mac_count = verify_mac_tasks(tasks, {"dw": dw_stages[0], "pw": pw_stages[0]})
    base.save(OUT / "mac_tasks.json", dict(tasks=tasks, valid_accumulators=mac_count))
    np.savez_compressed(OUT / "golden.npz", **values, halo=halo)
    for name, array in values.items():
        front.emit(OUT / "vectors" / f"{name}.hex", array, 32 if name.endswith("acc") else
                   16 if name.endswith(("pre", "silu", "sum")) else 8)
    front.emit(OUT / "vectors/halo.hex", halo, 8)
    # A byte-address shadow verifies split lane selection without fabricating DDR completion.
    source_base = model.graph["nodes"][2]["storage"]["base"]
    memory = {address(source_base, 128, 24, y, x, c): int(source[y, x, c])
              for y, x, c in np.ndindex(source.shape)}
    initial = memory.copy()
    halo_records, output_records = [], []
    for y, x, c in np.ndindex(6, 6, 12):
        sy, sx = y-1, x-1
        location = None if sy < 0 or sx < 0 else resolve_byte_address(model.graph, "split.00.1", sy, sx, c)
        if location is not None and location != address(source_base, 128, 24, sy, sx, c+12):
            raise ValueError("split view address mismatch")
        if int(halo[y, x, c]) != (0 if location is None else memory[location]):
            raise ValueError("halo byte/address mismatch")
        halo_records.append(dict(index=(y*6+x)*12+c, y=sy, x=sx, c=c, padding=location is None,
            byte_address=location, native_beat_address=None if location is None else (location & ~15)//2,
            byte_lane=None if location is None else location & 15))
    for y, x, c in np.ndindex(4, 4, 12):
        bypass_addr = resolve_byte_address(model.graph, "split.00.1", y, x, c)
        dw_addr = resolve_byte_address(model.graph, LAYERS[0], y, x, c)
        output_addr = resolve_byte_address(model.graph, "residual.00", y, x, c)
        if dw_addr != address(nodes[1]["storage"]["base"], 128, 12, y, x, c) or output_addr != address(nodes[2]["storage"]["base"], 128, 12, y, x, c):
            raise ValueError("write address mismatch")
        if output_addr != resolve_byte_address(model.graph, LAYERS[1], y, x, c):
            raise ValueError("residual must alias fused branch storage")
        if memory[bypass_addr] != int(bypass[y, x, c]):
            raise ValueError("residual bypass read mismatch")
        memory[dw_addr], memory[output_addr] = int(dw_stages[-1][y, x, c]), int(residual[y, x, c])
        output_records.append(dict(y=y, x=x, c=c, bypass_byte_address=bypass_addr,
            dw_write_byte_address=dw_addr, fused_residual_write_byte_address=output_addr))
    if any(memory[key] != value for key, value in initial.items()):
        raise ValueError("input or first12 passthrough overwritten")
    beats = []
    for name, array, storage in (("dw", dw_stages[-1], nodes[1]["storage"]),
                                ("residual", residual, nodes[2]["storage"])):
        words = [pack(array.ravel()[i:i+16], 8) for i in range(0, array.size, 16)]
        for index, word in enumerate(words):
            location = storage["base"] + index*16
            if any(((word >> (lane*8)) & 255) != memory[location+lane] & 255 for lane in range(16)):
                raise ValueError("128-bit write packing mismatch")
            beats.append(dict(tensor=name, byte_address=location, native_address=location//2,
                              data_hex=f"{word:032x}", PAXI_mask=0))
        front.emit(OUT / "vectors" / f"{name}_words.hex", np.array(words, dtype=object), 128)
    base.save(OUT / "addresses.json", dict(unit="logical_byte; native beat=aligned_byte/2, byte_lane retained; no DMA enabled",
        halo=halo_records, outputs=output_records, writes=beats, raw_PW_post_not_written_before_residual=True))
    front.check_hashes(frozen)
    artifacts = {p.relative_to(OUT).as_posix(): front.sha256(p) for p in OUT.rglob("*") if p.is_file()}
    base.save(OUT / "identity.json", dict(input_sha256=frozen, payload_sha256=manifest["payload_sha256"],
        checkpoint_sha256=binding["checkpoint_sha256"], runtime=front.diag.runtime.native_runtime_identity()))
    base.save(OUT / "verification_receipt.json", dict(status="CSP_FIRST_DATA_VERIFIED_NOT_RTL", fields=fields,
        selected_bytes=2526, bounds=bounds, comparisons=comparisons, golden_values=sum(a.size for a in values.values()),
        halo_values=432, real_halo_values=300, padding_values=132, output_bytes=192,
        independent_scalar_and_larger_context_exact=True, mac_tasks=len(tasks), mac_groups=sum(len(t["groups"]) for t in tasks),
        mac_accumulators_checked=mac_count, shadow_writes=384, write_beats=len(beats),
        residual_saturation_count=int(((total < -128) | (total > 127)).sum()),
        source_passthrough_preserved=True, artifact_sha256=artifacts, formal_acceptance=False))
    base.save(OUT / "status.json", dict(status="REAL_QAT_CSP_FIRST_DATA_READY_FOR_RTL_DESIGN",
        as_of=datetime.now().astimezone().isoformat(), seconds=time.perf_counter()-started,
        training_updates=0, numeric_full_network_forwards=0, CUDA_initialized=torch.cuda.is_initialized(),
        RTL_changed=False, RTL_compared=False, simulation_synthesis_bitstream_or_board=False,
        formal_acceptance=False, verification_receipt_sha256=front.sha256(OUT / "verification_receipt.json")))
    print("PASS_CSP_FIRST_DATA", flush=True)


if __name__ == "__main__":
    front.diag.runtime_guard()
    run()
