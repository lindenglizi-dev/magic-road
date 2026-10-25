"""Generate full-frame TEST_ONLY front-three-layer DDR/TB reference vectors."""

from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent
REPORT_ROOT = ROOT.parent
VECTORS = REPORT_ROOT / "vectors"
PROJECT = ROOT.parents[5]
OLD = ROOT.parents[1] / "stem_down2_handoff_20261011"
OLD_VECTORS = OLD / "vectors"
sys.path.insert(0, str(PROJECT))
from cnn import integer  # noqa: E402


INPUT_BASE = 0x03400000
STEM_BASE = 0x03500000
PW_BASE = 0x03600000
BEAT_BYTES = 16


def sha256(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def read_hex(path: Path, bits: int, signed: bool = True) -> np.ndarray:
    raw = np.array([int(word, 16) for word in path.read_text().split()], dtype=np.int64)
    if signed:
        raw = np.where(raw >= 1 << (bits - 1), raw - (1 << bits), raw)
    return raw


def tiled(tensor: np.ndarray) -> np.ndarray:
    height, width, channels = tensor.shape
    assert height % 4 == width % 4 == 0
    return tensor.reshape(height // 4, 4, width // 4, 4, channels).transpose(0, 2, 1, 3, 4).copy()


def emit_hex(path: Path, values: np.ndarray, bits: int) -> None:
    mask = (1 << bits) - 1
    flat = np.asarray(values).ravel()
    with path.open("w", encoding="ascii", newline="\n") as stream:
        for begin in range(0, flat.size, 8192):
            stream.writelines(f"{int(value) & mask:0{bits // 4}x}\n" for value in flat[begin:begin + 8192])


def emit_beats(path: Path, payload: bytes) -> None:
    assert len(payload) % BEAT_BYTES == 0
    with path.open("w", encoding="ascii", newline="\n") as stream:
        for begin in range(0, len(payload), BEAT_BYTES):
            # Text is a 128-bit value: the first memory byte occupies data[7:0].
            stream.write(f"{int.from_bytes(payload[begin:begin + BEAT_BYTES], 'little'):032x}\n")


def parse_beats(path: Path) -> bytes:
    return b"".join(int(word, 16).to_bytes(BEAT_BYTES, "little") for word in path.read_text().split())


def stages(acc: np.ndarray, multipliers: np.ndarray, shifts: np.ndarray,
           post_multiplier: int, post_shift: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    pre = integer.requantize(acc, multipliers, shifts, -32768, 32767).astype(np.int16)
    active = integer.silu(pre)
    post = integer.requantize(active.astype(np.int32), post_multiplier, post_shift).astype(np.int8)
    return pre, active, post


def cache_trace(addresses: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """One 16-byte cache line, invalidated at each tile; row-major local HWC access."""
    offsets = [0]
    counts = []
    trace = []
    for tile_addresses in addresses:
        cache_line = None
        prior_fetch = None
        runs = 0
        tile_fetches = 0
        for address in tile_addresses:
            if address < 0:
                continue
            line = int(address) & ~(BEAT_BYTES - 1)
            if line == cache_line:
                continue
            if prior_fetch is None or line != prior_fetch + BEAT_BYTES:
                runs += 1
            trace.append(line)
            tile_fetches += 1
            cache_line = line
            prior_fetch = line
        counts.append((tile_fetches, runs))
        offsets.append(len(trace))
    return (np.asarray(offsets, dtype="<u4"), np.asarray(trace, dtype="<u4"),
            np.asarray(counts, dtype="<u2"))


def stem_halos(source: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    values = np.zeros((36 * 64, 9 * 9 * 3), dtype=np.int8)
    addresses = np.full(values.shape, -1, dtype="<i4")
    for ty in range(36):
        for tx in range(64):
            tile = ty * 64 + tx
            for hy in range(9):
                y = ty * 8 + hy - 1
                for hx in range(9):
                    x = tx * 8 + hx - 1
                    for channel in range(3):
                        local = (hy * 9 + hx) * 3 + channel
                        if 0 <= y < 288 and 0 <= x < 512:
                            address = INPUT_BASE + (y * 512 + x) * 3 + channel
                            assert INPUT_BASE <= address < INPUT_BASE + source.size
                            addresses[tile, local] = address
                            values[tile, local] = source[y, x, channel]
    return values, addresses


def stem_tiled_offset(y: int, x: int, channel: int) -> int:
    return (((y // 4) * 64 + x // 4) * 4 + y % 4) * 4 * 16 + (x % 4) * 16 + channel


def dw_halos(stem: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    values = np.zeros((18 * 32, 9 * 9 * 16), dtype=np.int8)
    addresses = np.full(values.shape, -1, dtype="<i4")
    flat_tiled = tiled(stem).ravel()
    for ty in range(18):
        for tx in range(32):
            tile = ty * 32 + tx
            for hy in range(9):
                y = ty * 8 + hy - 1
                for hx in range(9):
                    x = tx * 8 + hx - 1
                    for channel in range(16):
                        local = (hy * 9 + hx) * 16 + channel
                        if 0 <= y < 144 and 0 <= x < 256:
                            offset = stem_tiled_offset(y, x, channel)
                            address = STEM_BASE + offset
                            assert STEM_BASE <= address < STEM_BASE + stem.size
                            assert flat_tiled[offset] == stem[y, x, channel]
                            addresses[tile, local] = address
                            values[tile, local] = stem[y, x, channel]
    return values, addresses


def axis_class(index: int) -> int:
    return 0 if index == 0 else 1 + (index & 1)


def write_raw(path: Path, values: np.ndarray, dtype: str) -> None:
    np.asarray(values, dtype=dtype).tofile(path)


def main() -> None:
    VECTORS.mkdir(parents=True, exist_ok=True)
    assert integer.__file__ is not None

    yy, xx = np.indices((288, 512))
    rgb = np.empty((288, 512, 3), dtype=np.uint8)
    rgb[..., 0] = (xx % 16) * 17
    rgb[..., 1] = (yy % 16) * 17
    rgb[..., 2] = (((xx % 16) * 7) ^ ((yy % 16) * 11)) & 255
    source = (rgb.astype(np.int16) - 128).astype(np.int8)

    stem_weights = read_hex(OLD_VECTORS / "stem_weights.hex", 8).astype(np.int8).reshape(16, 3, 3, 3)
    stem_biases = read_hex(OLD_VECTORS / "stem_biases.hex", 32)
    stem_multipliers = read_hex(OLD_VECTORS / "stem_multipliers.hex", 32)
    stem_shifts = read_hex(OLD_VECTORS / "stem_shifts.hex", 32, signed=False)
    stem_post = read_hex(OLD_VECTORS / "stem_post.hex", 32, signed=False)
    dw_weights = read_hex(OLD_VECTORS / "dw_weights.hex", 8).astype(np.int8).reshape(16, 1, 3, 3)
    dw_biases = read_hex(OLD_VECTORS / "dw_biases.hex", 32)
    pw_weights = read_hex(OLD_VECTORS / "pw_weights.hex", 8).astype(np.int8).reshape(24, 16, 1, 1)
    pw_biases = read_hex(OLD_VECTORS / "pw_biases.hex", 32)
    multipliers = read_hex(OLD_VECTORS / "multipliers.hex", 32)
    controls = read_hex(OLD_VECTORS / "controls.hex", 32, signed=False)
    old_silu = read_hex(OLD_VECTORS / "silu.hex", 16).astype(np.int16)
    assert np.array_equal(old_silu, integer.tables()["silu"])

    stem_acc = integer.conv2d(source, stem_weights, stem_biases, stride=2, padding=1)
    stem_pre, stem_silu, stem_out = stages(stem_acc, stem_multipliers, stem_shifts,
                                           int(stem_post[0]), int(stem_post[1]))
    dw_acc = integer.conv2d(stem_out, dw_weights, dw_biases, stride=2, padding=1, groups=16)
    dw_pre, dw_silu, dw_out = stages(dw_acc, multipliers[:16], controls[:16],
                                     int(controls[40]), int(controls[42]))
    pw_acc = integer.conv2d(dw_out, pw_weights, pw_biases)
    pw_pre, pw_silu, pw_out = stages(pw_acc, multipliers[16:40], controls[16:40],
                                     int(controls[41]), int(controls[43]))
    assert stem_out.shape == (144, 256, 16)
    assert dw_out.shape == (72, 128, 16)
    assert pw_out.shape == (72, 128, 24)

    layer_values = {
        "stem_acc_s32.hex": (stem_acc, 32), "stem_pre_s16.hex": (stem_pre, 16),
        "stem_silu_s16.hex": (stem_silu, 16), "stem_post_s8.hex": (stem_out, 8),
        "dw_acc_s32.hex": (dw_acc, 32), "dw_pre_s16.hex": (dw_pre, 16),
        "dw_silu_s16.hex": (dw_silu, 16), "dw_post_s8.hex": (dw_out, 8),
        "pw_acc_s32.hex": (pw_acc, 32), "pw_pre_s16.hex": (pw_pre, 16),
        "pw_silu_s16.hex": (pw_silu, 16), "pw_post_s8.hex": (pw_out, 8),
    }
    for name, (values, bits) in layer_values.items():
        emit_hex(VECTORS / name, tiled(values), bits)

    motif = rgb[:16, :16].tobytes()
    emit_beats(VECTORS / "rgb_pattern_rom_128.hex", motif)
    emit_beats(VECTORS / "rgb_pattern_words.hex", motif)
    assert len((VECTORS / "rgb_pattern_words.hex").read_text().split()) == 48
    rebuilt = bytearray()
    rom = parse_beats(VECTORS / "rgb_pattern_rom_128.hex")
    for y in range(288):
        row = rom[(y % 16) * 48:(y % 16 + 1) * 48]
        rebuilt.extend(row * 32)
    assert bytes(rebuilt) == rgb.tobytes()

    emit_beats(VECTORS / "input_ddr_128.hex", bytes(rebuilt))
    emit_beats(VECTORS / "stem_ddr_128.hex", tiled(stem_out).tobytes())
    emit_beats(VECTORS / "pw_ddr_128.hex", tiled(pw_out).tobytes())
    assert parse_beats(VECTORS / "input_ddr_128.hex") == rgb.tobytes()
    assert parse_beats(VECTORS / "stem_ddr_128.hex") == tiled(stem_out).tobytes()
    assert parse_beats(VECTORS / "pw_ddr_128.hex") == tiled(pw_out).tobytes()
    np.save(VECTORS / "input_rgb_hwc.npy", rgb)
    np.save(VECTORS / "expected_stem_hwc.npy", stem_out)
    np.save(VECTORS / "expected_dw_hwc.npy", dw_out)
    np.save(VECTORS / "expected_pw_hwc.npy", pw_out)

    stem_tiles = tiled(stem_out).reshape(2304, 256)
    stem_classes = np.empty(2304, dtype=np.uint8)
    stem_representatives: dict[int, np.ndarray] = {}
    for ty in range(36):
        for tx in range(64):
            tile = ty * 64 + tx
            y_class, x_class = axis_class(ty), axis_class(tx)
            class_id = y_class * 3 + x_class
            stem_classes[tile] = class_id
            stem_representatives.setdefault(class_id, stem_tiles[tile].copy())
            assert np.array_equal(stem_tiles[tile], stem_representatives[class_id])
    assert sorted(stem_representatives) == list(range(9))
    for class_id, values in stem_representatives.items():
        emit_hex(VECTORS / f"stem_board_class_y{class_id // 3}_x{class_id % 3}_s8.hex", values, 8)
    write_raw(VECTORS / "stem_tile_class_u8.bin", stem_classes, "u1")

    pw_tiles = tiled(pw_out).reshape(576, 384)
    pw_classes = np.empty(576, dtype=np.uint8)
    pw_representatives: dict[int, np.ndarray] = {}
    for ty in range(18):
        for tx in range(32):
            tile = ty * 32 + tx
            class_id = (1 if ty else 0) * 2 + (1 if tx else 0)
            pw_classes[tile] = class_id
            pw_representatives.setdefault(class_id, pw_tiles[tile].copy())
            assert np.array_equal(pw_tiles[tile], pw_representatives[class_id])
    assert sorted(pw_representatives) == list(range(4))
    for class_id, values in pw_representatives.items():
        emit_hex(VECTORS / f"pw_board_class_y{class_id // 2}_x{class_id % 2}_s8.hex", values, 8)
    write_raw(VECTORS / "pw_tile_class_u8.bin", pw_classes, "u1")
    combined = b"".join(stem_representatives[class_id].tobytes() for class_id in range(9))
    combined += b"".join(pw_representatives[class_id].tobytes() for class_id in range(4))
    assert len(combined) == 240 * BEAT_BYTES
    emit_beats(VECTORS / "combined_golden.hex", combined + bytes(16 * BEAT_BYTES))
    assert len((VECTORS / "combined_golden.hex").read_text().split()) == 256

    stem_halo_values, stem_halo_addresses = stem_halos(source)
    dw_halo_values, dw_halo_addresses = dw_halos(stem_out)
    for prefix, values, addresses in (("stem", stem_halo_values, stem_halo_addresses),
                                      ("dw", dw_halo_values, dw_halo_addresses)):
        write_raw(VECTORS / f"{prefix}_halo_values_s8.bin", values, "i1")
        write_raw(VECTORS / f"{prefix}_halo_byte_addr_s32.bin", addresses, "<i4")
        offsets, trace, counts = cache_trace(addresses)
        write_raw(VECTORS / f"{prefix}_read_trace_offsets_u32.bin", offsets, "<u4")
        write_raw(VECTORS / f"{prefix}_read_trace_byte_addr_u32.bin", trace, "<u4")
        write_raw(VECTORS / f"{prefix}_read_counts_u16.bin", counts, "<u2")

    for name in ("stem_weights.hex", "stem_biases.hex", "stem_multipliers.hex", "stem_shifts.hex",
                 "stem_post.hex", "dw_weights.hex", "dw_biases.hex", "pw_weights.hex",
                 "pw_biases.hex", "multipliers.hex", "controls.hex", "silu.hex"):
        shutil.copyfile(OLD_VECTORS / name, VECTORS / f"param_{name}")

    stem_offsets, stem_trace, stem_counts = cache_trace(stem_halo_addresses)
    dw_offsets, dw_trace, dw_counts = cache_trace(dw_halo_addresses)
    assert stem_offsets[-1] == len(stem_trace) == int(stem_counts[:, 0].sum())
    assert dw_offsets[-1] == len(dw_trace) == int(dw_counts[:, 0].sum())
    assert all(INPUT_BASE <= int(address) < INPUT_BASE + rgb.size for address in stem_trace)
    assert all(STEM_BASE <= int(address) < STEM_BASE + stem_out.size for address in dw_trace)

    vector_hashes = {path.name: sha256(path) for path in sorted(VECTORS.iterdir()) if path.is_file()}
    dependency_paths = [Path(integer.__file__), OLD / "run.py"] + [OLD_VECTORS / name for name in (
        "stem_weights.hex", "stem_biases.hex", "stem_multipliers.hex", "stem_shifts.hex", "stem_post.hex",
        "dw_weights.hex", "dw_biases.hex", "pw_weights.hex", "pw_biases.hex", "multipliers.hex",
        "controls.hex", "silu.hex")]
    contract = {
        "status": "PASS_TEST_ONLY_NOT_DEPLOYMENT_MODEL",
        "scope": "Python numeric/address/TB reference only; no training, GPU, RTL, synthesis, board, flash or bitstream",
        "input_pattern": {
            "shape_hwc": [288, 512, 3], "dtype": "uint8", "period": [16, 16],
            "R": "(x%16)*17", "G": "(y%16)*17",
            "B": "(((x%16)*7)^((y%16)*11))&255", "edge_overwrite": False,
        },
        "layout": {
            "layers": "tile4x4_hwc, tile row-major then local row, local column, channel",
            "input": "NHWC RGB", "weight": "OIHW", "hex_signed": "two's complement",
            "beat_hex": "128-bit hex; earliest byte is data[7:0] (little-endian byte lanes)",
        },
        "layers": {
            "stem": {"shape_hwc": [144, 256, 16], "acc": "int32", "pre": "int16", "silu": "int16", "post": "int8"},
            "dw3s2": {"shape_hwc": [72, 128, 16], "acc": "int32", "pre": "int16", "silu": "int16", "post": "int8"},
            "pw": {"shape_hwc": [72, 128, 24], "acc": "int32", "pre": "int16", "silu": "int16", "post": "int8"},
        },
        "ddr": {
            "address_rule": "native_address = byte_address >> 1; 128-bit beat = 16 bytes; native beat step = 8",
            "input": {"base_byte": INPUT_BASE, "end_exclusive_byte": INPUT_BASE + rgb.size, "beats": rgb.size // 16},
            "stem": {"base_byte": STEM_BASE, "end_exclusive_byte": STEM_BASE + stem_out.size, "beats": stem_out.size // 16},
            "pw": {"base_byte": PW_BASE, "end_exclusive_byte": PW_BASE + pw_out.size, "beats": pw_out.size // 16},
        },
        "pattern_rom": {"shape_words": [16, 3], "words": 48, "fill": "repeat three words 32 times per row; repeat 16 rows 18 times", "exact_rgb_match": True},
        "board_golden": {
            "stem": {"tiles_checked": 2304, "classes": 9, "bytes_per_class": 256,
                     "axis_class": "0 if tile index is 0; otherwise 1+(index&1), so even->1 and odd->2",
                     "representative_tile_indices": [int(np.flatnonzero(stem_classes == class_id)[0]) for class_id in range(9)],
                     "tile_counts": np.bincount(stem_classes, minlength=9).tolist(), "mismatches": 0},
            "pw": {"tiles_checked": 576, "classes": 4, "bytes_per_class": 384,
                   "class": "(ty!=0)*2+(tx!=0)",
                   "representative_tile_indices": [int(np.flatnonzero(pw_classes == class_id)[0]) for class_id in range(4)],
                   "tile_counts": np.bincount(pw_classes, minlength=4).tolist(), "mismatches": 0},
            "combined_golden": {"valid_words": 240, "physical_words": 256, "padding_words": 16,
                                "order": "Stem classes 0..8 (16 words each), PW classes 0..3 (24 words each), zero pad"},
        },
        "halo": {
            "stem": {"shape": [2304, 243], "local_index": "((hy*9+hx)*3+c)",
                     "global": "y=ty*8+hy-1,x=tx*8+hx-1", "value": "valid RGB-128 int8; invalid operator zero",
                     "byte_address": "input_base+(y*512+x)*3+c; invalid=-1",
                     "files": {"values": "int8[2304,243]", "addresses": "little-endian int32[2304,243]",
                               "read_offsets": "little-endian uint32[2305]", "read_trace": f"little-endian uint32[{len(stem_trace)}] byte line addresses",
                               "read_counts": "little-endian uint16[2304,2], columns beat_reads/contiguous_runs"}},
            "dw": {"shape": [576, 1296], "local_index": "((hy*9+hx)*16+c)",
                   "global": "y=ty*8+hy-1,x=tx*8+hx-1", "value": "valid Stem post int8; invalid zero",
                   "byte_address": "stem_base+tile4x4_hwc_offset; invalid=-1",
                   "files": {"values": "int8[576,1296]", "addresses": "little-endian int32[576,1296]",
                             "read_offsets": "little-endian uint32[577]", "read_trace": f"little-endian uint32[{len(dw_trace)}] byte line addresses",
                             "read_counts": "little-endian uint16[576,2], columns beat_reads/contiguous_runs"}},
            "boundary": "Only top/left pad. Bottom/right final stride-2 windows are fully valid for even input shapes.",
        },
        "read_model": {
            "cache": "one 16-byte line keyed by native_aligned=(byte_address>>1)&~7; invalidated at each tile; local HWC traversal; invalid entries issue no read",
            "stem": {"beat_reads": int(stem_counts[:, 0].sum()), "contiguous_runs": int(stem_counts[:, 1].sum()),
                     "per_tile_min": int(stem_counts[:, 0].min()), "per_tile_max": int(stem_counts[:, 0].max())},
            "dw": {"beat_reads": int(dw_counts[:, 0].sum()), "contiguous_runs": int(dw_counts[:, 1].sum()),
                   "per_tile_min": int(dw_counts[:, 0].min()), "per_tile_max": int(dw_counts[:, 0].max())},
        },
        "hashes": {
            "vectors": vector_hashes,
            "dependencies": {str(path.relative_to(PROJECT)).replace("\\", "/"): sha256(path) for path in dependency_paths},
        },
    }
    (ROOT / "contract.json").write_text(json.dumps(contract, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    report = f"""# 完整前三层 DDR Python 参考报告

状态：PASS（仅 TEST_ONLY 诊断参数，不是部署 QAT 模型）。

- 输入：512×288×3 RGB，严格使用 16×16 周期公式，无边缘覆写。
- 全帧数值：Stem 144×256×16、DW3s2 72×128×16、PW 72×128×24；每层 acc/pre/silu/post 均按 tile4x4_hwc 导出并哈希。
- DDR：input/stem/pw 字节基址分别为 0x{INPUT_BASE:08x}/0x{STEM_BASE:08x}/0x{PW_BASE:08x}；128-bit beat 数分别为 {rgb.size // 16}/{stem_out.size // 16}/{pw_out.size // 16}。native=byte>>1，每 beat 步长 8。
- RGB pattern ROM：16 行×3 个 128-bit 字，共 48 字；逐字重建 96 beats/行、288 行，与完整 RGB {rgb.size} 字节逐项一致。
- Stem 板上 golden：9 类×256B；轴分类 0=top/left，非边界 class=1+(index&1)，即 even=1、odd=2。2304 tile 逐项一致，0 mismatch。
- PW 板上 golden：4 类×384B；按 ty==0 与 tx==0 分类。576 tile 逐项一致，0 mismatch。
- combined_golden.hex：Stem 9×16 词后接 PW 4×24 词，共 240 个有效 128-bit 词，尾补 16 个零词至 256。
- Halo：Stem [2304,243] 读 NHWC RGB；DW [576,1296] 读 Stem tile4x4_hwc。无效地址=-1、值=0；底/右最后窗口全部有效。
- 16B 单行缓存（每 tile 失效）：Stem {int(stem_counts[:, 0].sum())} beat reads、{int(stem_counts[:, 1].sum())} 连续段，单 tile {int(stem_counts[:, 0].min())}..{int(stem_counts[:, 0].max())} reads；DW {int(dw_counts[:, 0].sum())} beat reads、{int(dw_counts[:, 1].sum())} 连续段，单 tile {int(dw_counts[:, 0].min())}..{int(dw_counts[:, 0].max())} reads。
- 数值来源：旧冻结 stem_down2_handoff_20261011 测试权重、偏置、量化参数和 SiLU 表；依赖与全部向量哈希见 contract.json。

未执行：训练、GPU、RTL 修改、仿真、综合、板卡、Flash、位流。
"""
    (ROOT / "报告.txt").write_text(report, encoding="utf-8")

    deliverables = sorted(
        [path for path in ROOT.rglob("*") if path.is_file() and path.name != "manifest.sha256"]
        + [path for path in VECTORS.rglob("*") if path.is_file()]
    )
    manifest = "".join(f"{sha256(path)}  {path.relative_to(REPORT_ROOT).as_posix()}\n" for path in deliverables)
    (ROOT / "manifest.sha256").write_text(manifest, encoding="utf-8", newline="\n")
    print(f"PASS stem_reads={stem_counts[:, 0].sum()} dw_reads={dw_counts[:, 0].sum()} vectors={len(vector_hashes)}")


if __name__ == "__main__":
    main()
