"""CPU-only numerical and bounded-scheduling reference for road_area_resize."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import deque
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent
COMPONENT = ROOT.parent
VECTORS = COMPONENT / "vectors"
SOURCE_H, SOURCE_W = 720, 1280
OUTPUT_H, OUTPUT_W = 288, 512
ACTIVE_BEATS = SOURCE_W // 4
NORMAL_LINE_CYCLES = 800
SERIAL_QUEUE_DEPTH = 192
RANDOM_SEED = 20261015


def sha256(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def bytes_sha256(values: np.ndarray) -> str:
    return hashlib.sha256(np.ascontiguousarray(values).tobytes()).hexdigest()


def numbered_bars() -> np.ndarray:
    y, x = np.indices((SOURCE_H, SOURCE_W))
    bar = x // 80
    frame = np.empty((SOURCE_H, SOURCE_W, 3), dtype=np.uint8)
    frame[..., 0] = bar * 17
    frame[..., 1] = (y % 16) * 17
    frame[..., 2] = (bar << 4) | (x & 15)
    return frame


def area_resize(rgb: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if rgb.shape != (SOURCE_H, SOURCE_W, 3) or rgb.dtype != np.uint8:
        raise ValueError("input must be uint8 RGB [720,1280,3]")
    blocks_x = rgb.astype(np.uint16).reshape(SOURCE_H, SOURCE_W // 5, 5, 3)
    horizontal = np.stack((2 * blocks_x[:, :, 0] + 2 * blocks_x[:, :, 1] + blocks_x[:, :, 2],
                           blocks_x[:, :, 2] + 2 * blocks_x[:, :, 3] + 2 * blocks_x[:, :, 4]), axis=2)
    horizontal = horizontal.reshape(SOURCE_H, OUTPUT_W, 3)
    blocks_y = horizontal.reshape(OUTPUT_H // 2, 5, OUTPUT_W, 3)
    vertical = np.stack((2 * blocks_y[:, 0] + 2 * blocks_y[:, 1] + blocks_y[:, 2],
                         blocks_y[:, 2] + 2 * blocks_y[:, 3] + 2 * blocks_y[:, 4]), axis=1)
    vertical = vertical.reshape(OUTPUT_H, OUTPUT_W, 3)
    # The positive integer numerator cannot tie at x.5 for odd divisor 25.
    output = ((vertical.astype(np.uint16) + 12) // 25).astype(np.uint8)
    return horizontal, vertical, output


def naive_pixel(rgb: np.ndarray, output_y: int, output_x: int) -> np.ndarray:
    weights_y = (2, 2, 1, 0, 0) if output_y % 2 == 0 else (0, 0, 1, 2, 2)
    weights_x = (2, 2, 1, 0, 0) if output_x % 2 == 0 else (0, 0, 1, 2, 2)
    source_y = output_y // 2 * 5
    source_x = output_x // 2 * 5
    total = np.zeros(3, dtype=np.uint32)
    for dy, wy in enumerate(weights_y):
        for dx, wx in enumerate(weights_x):
            total += int(wy * wx) * rgb[source_y + dy, source_x + dx].astype(np.uint32)
    return ((total + 12) // 25).astype(np.uint8)


def emit_awb96(path: Path, frame: np.ndarray) -> None:
    pixels = frame.reshape(SOURCE_H, ACTIVE_BEATS, 4, 3)
    with path.open("w", encoding="ascii", newline="\n") as stream:
        for y in range(SOURCE_H):
            for begin in range(0, ACTIVE_BEATS, 64):
                chunk = pixels[y, begin:begin + 64]
                stream.writelines(
                    "".join(f"{int(r):02x}{int(g):02x}{int(b):02x}" for r, g, b in beat) + "\n"
                    for beat in chunk
                )


def emit_output48(path: Path, output: np.ndarray) -> None:
    packed = (output[..., 0].astype(np.uint32)
              | (output[..., 1].astype(np.uint32) << 8)
              | (output[..., 2].astype(np.uint32) << 16)).ravel()
    with path.open("w", encoding="ascii", newline="\n") as stream:
        for begin in range(0, packed.size, 8192):
            # Serial vertical reference: upper pixel lane is zero, lower bytes are R,G,B.
            stream.writelines(f"{int(value):012x}\n" for value in packed[begin:begin + 8192])


def decode_awb96(word: str) -> np.ndarray:
    if len(word) != 24:
        raise ValueError("AWB96 word must contain 24 hex digits")
    # Leftmost/high lane 95:72 is the earliest pixel.
    return np.array([[int(word[offset:offset + 2], 16),
                      int(word[offset + 2:offset + 4], 16),
                      int(word[offset + 4:offset + 6], 16)]
                     for offset in range(0, 24, 6)], dtype=np.uint8)


def horizontal_schedule() -> list[dict[str, int]]:
    records = []
    next_output = 0
    ready_edge = [5 * (x // 2) + (2 if x % 2 == 0 else 4) for x in range(OUTPUT_W)]
    for beat in range(ACTIVE_BEATS):
        end_x = beat * 4 + 3
        first_output = next_output
        while next_output < OUTPUT_W and ready_edge[next_output] <= end_x:
            next_output += 1
        count = next_output - first_output
        records.append({"beat": beat, "phase": (beat * 4) % 5, "count": count,
                        "mask": 1 if count == 1 else 3, "first_output_x": first_output})
    assert next_output == OUTPUT_W
    assert [records[index]["phase"] for index in range(5)] == [0, 4, 3, 2, 1]
    assert [records[index]["count"] for index in range(5)] == [1, 2, 1, 2, 2]
    assert max(record["count"] for record in records) == 2
    return records


def queue_run(line_interval: int, rows: int = SOURCE_H,
              depth: int | None = SERIAL_QUEUE_DEPTH) -> dict[str, int | None]:
    schedule = horizontal_schedule()
    queue_level = 0
    maximum = 0
    first_overflow_cycle = None
    first_overflow_row = None
    first_overflow_beat = None
    last_arrival_cycle = (rows - 1) * line_interval + ACTIVE_BEATS - 1
    for cycle in range(last_arrival_cycle + 1):
        row = cycle // line_interval
        beat = cycle % line_interval
        arrivals = schedule[beat]["count"] if row < rows and beat < ACTIVE_BEATS else 0
        # One current result can flow directly into the serial consumer; only residue is queued.
        queue_level = max(0, queue_level + arrivals - 1)
        maximum = max(maximum, queue_level)
        if depth is not None and queue_level > depth and first_overflow_cycle is None:
            first_overflow_cycle = cycle
            first_overflow_row = row
            first_overflow_beat = beat
    drain_cycles = queue_level
    return {"max_queue": maximum, "level_after_last_active": queue_level,
            "drain_cycles": drain_cycles, "first_overflow_cycle": first_overflow_cycle,
            "first_overflow_row": first_overflow_row, "first_overflow_beat": first_overflow_beat}


def serial_vertical_reference(horizontal: np.ndarray, expected: np.ndarray,
                              schedule: list[dict[str, int]]) -> dict[str, int]:
    queue: deque[tuple[int, int]] = deque()
    processed = np.zeros((SOURCE_H, OUTPUT_W), dtype=bool)
    produced = np.zeros((OUTPUT_H, OUTPUT_W), dtype=bool)
    actual = np.zeros_like(expected)
    first_output_cycle = -1
    last_output_cycle = -1
    maximum = 0
    last_cycle = (SOURCE_H - 1) * NORMAL_LINE_CYCLES + ACTIVE_BEATS - 1
    cycle = 0
    while cycle <= last_cycle or queue:
        row = cycle // NORMAL_LINE_CYCLES
        beat = cycle % NORMAL_LINE_CYCLES
        if row < SOURCE_H and beat < ACTIVE_BEATS:
            record = schedule[beat]
            queue.extend((row, x) for x in range(record["first_output_x"],
                                                 record["first_output_x"] + record["count"]))
        if queue:
            source_y, x = queue.popleft()
            processed[source_y, x] = True
            phase = source_y % 5
            if phase in (2, 4):
                group = source_y // 5
                if phase == 2:
                    rows = (group * 5, group * 5 + 1, group * 5 + 2)
                    weights = (2, 2, 1)
                    output_y = group * 2
                else:
                    rows = (group * 5 + 2, group * 5 + 3, group * 5 + 4)
                    weights = (1, 2, 2)
                    output_y = group * 2 + 1
                assert all(processed[y, x] for y in rows)
                total = sum(weight * horizontal[y, x].astype(np.uint32)
                            for y, weight in zip(rows, weights, strict=True))
                actual[output_y, x] = ((total + 12) // 25).astype(np.uint8)
                produced[output_y, x] = True
                if first_output_cycle < 0:
                    first_output_cycle = cycle
                last_output_cycle = cycle
        maximum = max(maximum, len(queue))
        cycle += 1
    assert processed.all() and produced.all()
    assert np.array_equal(actual, expected)
    return {"max_queue": maximum, "first_output_cycle": first_output_cycle,
            "last_output_cycle": last_output_cycle, "completion_cycles": cycle}


def write_schedules(schedule: list[dict[str, int]]) -> None:
    with (VECTORS / "horizontal_schedule.csv").open("w", encoding="ascii", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=("beat", "phase", "count", "mask", "first_output_x"))
        writer.writeheader()
        writer.writerows(schedule)
    with (VECTORS / "vertical_row_schedule.csv").open("w", encoding="ascii", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(("source_y", "input_start_cycle", "serial_end_cycle", "output_y",
                         "output_start_cycle", "output_end_cycle"))
        for source_y in range(SOURCE_H):
            start = source_y * NORMAL_LINE_CYCLES
            phase = source_y % 5
            output_y = source_y // 5 * 2 + (1 if phase == 4 else 0) if phase in (2, 4) else -1
            writer.writerow((source_y, start, start + 511, output_y,
                             start if output_y >= 0 else -1, start + 511 if output_y >= 0 else -1))


def main() -> None:
    VECTORS.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(RANDOM_SEED)
    frames = [
        ("frame0_numbered_bars", numbered_bars()),
        ("frame1_random_seed20261015", rng.integers(0, 256, (SOURCE_H, SOURCE_W, 3), dtype=np.uint8)),
        ("frame2_all255", np.full((SOURCE_H, SOURCE_W, 3), 255, dtype=np.uint8)),
    ]
    schedule = horizontal_schedule()
    write_schedules(schedule)
    frame_records = []
    first_horizontal = None
    first_output = None
    selected = ((0, 0), (0, 1), (1, 0), (143, 255), (287, 511), (100, 300))
    for name, frame in frames:
        horizontal, vertical, output = area_resize(frame)
        assert int(horizontal.max()) <= 1275
        assert int(vertical.max()) <= 6375
        for y, x in selected:
            assert np.array_equal(output[y, x], naive_pixel(frame, y, x))
        awb_path = VECTORS / f"{name}_awb96.hex"
        output_path = VECTORS / f"{name}_rgb48_serial.hex"
        emit_awb96(awb_path, frame)
        emit_output48(output_path, output)
        awb_words = awb_path.read_text(encoding="ascii").splitlines()
        output_words = output_path.read_text(encoding="ascii").splitlines()
        assert len(awb_words) == SOURCE_H * ACTIVE_BEATS
        assert len(output_words) == OUTPUT_H * OUTPUT_W
        for index in (0, 1, ACTIVE_BEATS - 1, ACTIVE_BEATS, len(awb_words) // 2, len(awb_words) - 1):
            y, beat = divmod(index, ACTIVE_BEATS)
            assert np.array_equal(decode_awb96(awb_words[index]), frame[y, beat * 4:beat * 4 + 4])
        for index in (0, 1, OUTPUT_W - 1, OUTPUT_W, len(output_words) // 2, len(output_words) - 1):
            y, x = divmod(index, OUTPUT_W)
            expected_word = int(output[y, x, 0]) | (int(output[y, x, 1]) << 8) | (int(output[y, x, 2]) << 16)
            assert int(output_words[index], 16) == expected_word
        first_word = awb_words[0]
        output_first_word = output_words[0]
        frame_records.append({
            "name": name, "input_shape_hwc": list(frame.shape), "output_shape_hwc": list(output.shape),
            "input_rgb_bytes_sha256": bytes_sha256(frame), "output_rgb_bytes_sha256": bytes_sha256(output),
            "awb96_file": awb_path.name, "awb96_words": SOURCE_H * ACTIVE_BEATS,
            "awb96_sha256": sha256(awb_path), "first_awb96_word": first_word,
            "output_file": output_path.name, "output_words": OUTPUT_H * OUTPUT_W,
            "output_sha256": sha256(output_path), "first_output48_word": output_first_word,
            "horizontal_max": int(horizontal.max()), "vertical_max": int(vertical.max()),
        })
        if first_horizontal is None:
            first_horizontal, first_output = horizontal, output
    assert np.all(frames[2][1] == 255)
    assert np.all(area_resize(frames[2][1])[2] == 255)
    serial = serial_vertical_reference(first_horizontal, first_output, schedule)
    assert serial["max_queue"] == SERIAL_QUEUE_DEPTH

    normal = queue_run(NORMAL_LINE_CYCLES)
    minimum_interval = next(interval for interval in range(ACTIVE_BEATS, NORMAL_LINE_CYCLES + 1)
                            if queue_run(interval)["first_overflow_cycle"] is None)
    no_gap = queue_run(ACTIVE_BEATS)
    assert normal["max_queue"] == SERIAL_QUEUE_DEPTH and normal["first_overflow_cycle"] is None
    assert minimum_interval == 512
    assert no_gap["first_overflow_row"] == 1 and no_gap["first_overflow_beat"] == 1

    vector_hashes = {path.name: sha256(path) for path in sorted(VECTORS.iterdir()) if path.is_file()}
    contract = {
        "status": "PASS_CPU_REFERENCE_NOT_RTL_OR_BOARD",
        "scope": "Exact 2/5 RGB arithmetic, lane mapping and bounded scheduling only; no training, GPU, RTL, TD, ERAM mapping, DDR, camera, board or bitstream",
        "source": {"shape_hwc": [720, 1280, 3], "awb96_words_per_line": 320,
                   "lane_order_earliest_to_latest": ["95:72", "71:48", "47:24", "23:0"],
                   "lane_fields": {"R": "23:16", "G": "15:8", "B": "7:0"}},
        "output": {"shape_hwc": [288, 512, 3], "serial_reference_mask": "01",
                   "o_pixels": "bits7:0 R, 15:8 G, 23:16 B, bits47:24 zero",
                   "note": "interface permits two lanes, but bounded serial vertical reference emits one"},
        "arithmetic": {"horizontal_weights": [[2, 2, 1, 0, 0], [0, 0, 1, 2, 2]],
                       "horizontal_width_bits": 11, "horizontal_max_allowed": 1275,
                       "vertical_weights": [[2, 2, 1, 0, 0], [0, 0, 1, 2, 2]],
                       "vertical_width_bits": 13, "vertical_max_allowed": 6375,
                       "rounding": "one final round-nearest-even divide by 25; integer numerator cannot tie; implemented as (sum+12)//25",
                       "forbidden": "no intermediate divide by 5"},
        "horizontal_schedule": {"input_pixels_per_cycle": 4, "phase_sequence": [0, 4, 3, 2, 1],
                                "outputs_per_cycle": [1, 2, 1, 2, 2], "maximum_lanes": 2,
                                "repeats_per_line": 64, "outputs_per_line": 512,
                                "masks": {"one": "01", "two": "11"}},
        "serial_queue": {"model": "enqueue 1/2 horizontal results, same cycle consume at most one including current arrivals, FIFO residue bounded",
                         "depth": SERIAL_QUEUE_DEPTH, "normal": {"active_cycles": 320, "blank_cycles": 480,
                         "line_interval": NORMAL_LINE_CYCLES, **normal},
                         "minimum_schedulable": {"line_interval": minimum_interval, "blank_cycles": minimum_interval - ACTIVE_BEATS},
                         "no_line_idle": {"line_interval": ACTIVE_BEATS, **no_gap,
                                          "expected": "OVERLOAD; first overflow on source row 1 beat 1"}},
        "vertical_serial": {"source_row_phases_producing_output": {"2": "first output row", "4": "second output row"},
                            "pixels_per_output_cycle": 1, **serial},
        "frames": frame_records,
        "hashes": {"vectors": vector_hashes,
                   "requirements.txt": sha256(COMPONENT / "requirements.txt"),
                   "interfaces.json": sha256(COMPONENT / "interfaces.json"),
                   "generate.py": sha256(Path(__file__))},
        "evidence_boundary": "Functional CPU reference only; does not prove two-ERAM mapping, LUTRAM/Slice budget, camera timing, vendor RAM behavior, physical timing, real DDR visibility or 2 FPS board operation",
    }
    (ROOT / "contract.json").write_text(json.dumps(contract, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = f"""# 精确彩色 2/5 缩放 CPU 参考

状态：PASS，仅功能数值与有界调度参考。

- 三帧均完成 1280×720 AWB96 高 lane 优先解包与 512×288 RGB 输出；文件形状和 SHA-256 见 contract.json。
- 水平相位 0/4/3/2/1 每拍产生 1/2/1/2/2 个结果，最大2 lane，每行合计512。
- 算术仅在二维加权和后执行一次 RNE /25；水平最大 {max(item['horizontal_max'] for item in frame_records)}，纵向最大 {max(item['vertical_max'] for item in frame_records)}。
- 串行纵向模型当拍最多消费1项，深度192；320拍连续输入后残余192项。普通480空拍可完全排空，最短可排空间隔192拍、行周期512拍。
- 无行间空闲时预期过载：深度192在第2行 beat1 首次溢出；整帧连续有效期间无界积压达到 {no_gap['max_queue']} 项。
- 普通800拍行周期下，首输出周期 {serial['first_output_cycle']}，末输出周期 {serial['last_output_cycle']}，数值与直接二维参考逐项一致。

未证明：2 ERAM物理映射、LUTRAM/Slice预算、真实摄像头/DDR、TD时序、实板2 FPS。
"""
    (ROOT / "报告.txt").write_text(report, encoding="utf-8")
    files = sorted([path for path in ROOT.iterdir() if path.is_file() and path.name != "manifest.sha256"]
                   + [path for path in VECTORS.iterdir() if path.is_file()])
    manifest = "".join(f"{sha256(path)}  {path.relative_to(COMPONENT).as_posix()}\n" for path in files)
    (ROOT / "manifest.sha256").write_text(manifest, encoding="utf-8", newline="\n")
    print(f"PASS frames=3 queue={serial['max_queue']} minimum_line_interval={minimum_interval} no_gap_overflow={no_gap['first_overflow_cycle']}")


if __name__ == "__main__":
    main()
