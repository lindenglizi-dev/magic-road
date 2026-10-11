"""DW 同通道三空间点排布参考；只证明整数等价，不模拟 RTL 周期。"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import random
import runpy


ROOT = Path(__file__).resolve().parent
REPORTS = ROOT.parent
MAC_SOURCE = REPORTS / "v9_mac_stream_20261007/verification/stream_reference.py"
POST_SOURCE = REPORTS / "v11_internal_timing_20261007/verification/reference.py"
TILE_SOURCE = REPORTS / "v8_reset_layer_tiles_20261007/layers/reference.py"
MAC = runpy.run_path(str(MAC_SOURCE))
POST = runpy.run_path(str(POST_SOURCE))
TILE = runpy.run_path(str(TILE_SOURCE))


def pack_windows(read_pixel, kernel, bias, stride, y, x, channel, count, pad=0):
    """输出行内的1至3点；并集固定15/21槽，公共输入mask与输出mask分开。"""
    if stride not in (1, 2) or count not in (1, 2, 3) or pad not in (0, 1):
        raise ValueError("only 3x3/s1,s2, padding0,1 and row-local count1..3")
    if len(kernel) != 9 or min(y, x, channel) < 0:
        raise ValueError("invalid kernel or output identity")
    for value in kernel:
        MAC["signed"](value, 8)
    MAC["signed"](bias, 32)
    width = 3 + 2 * stride
    locations = [(row, col) for row in range(3) for col in range(width)]
    acts = [read_pixel(y * stride - pad + row, x * stride - pad + col, channel)
            for row, col in locations]
    for value in acts:
        MAC["signed"](value, 8)
    sparse = [[kernel[row * 3 + col - lane * stride]
               if lane < count and 0 <= col - lane * stride < 3 else 0
               for row, col in locations] for lane in range(3)]
    beats = []
    for offset in range(0, len(acts), 8):
        valid = min(8, len(acts) - offset)
        beats.append({
            "activation": acts[offset:offset + 8] + [0] * (8 - valid),
            "weight": [weights[offset:offset + 8] + [0] * (8 - valid)
                       for weights in sparse],
            "bias": [bias if lane < count else 0 for lane in range(3)],
            "input_mask": (1 << valid) - 1,
            "first": offset == 0, "last": offset + 8 >= len(acts),
        })
    return {"beats": beats, "output_mask": (1 << count) - 1,
            "destinations": [[y, x + lane, channel] if lane < count else None
                             for lane in range(3)], "union_size": len(acts)}


def evaluate(task):
    """复用冻结乘积树；偏置只first一次，signed33部分和、末组INT32原子故障。"""
    acc = [0, 0, 0]
    partials = []
    beats = task["beats"]
    assert 1 <= len(beats) <= 24
    assert beats[0]["first"] and beats[-1]["last"]
    for index, beat in enumerate(beats):
        assert beat["first"] == (index == 0)
        assert beat["last"] == (index == len(beats) - 1)
        item = MAC["Beat"](tuple(beat["activation"]),
                           tuple(tuple(row) for row in beat["weight"]),
                           tuple(beat["bias"]), beat["input_mask"])
        dot = MAC["dots"](item)
        acc = [MAC["signed"]((beat["bias"][lane] if beat["first"] else acc[lane])
                             + dot[lane], 33) for lane in range(3)]
        partials.append(list(acc))
    fault = any(not -(1 << 31) <= value < (1 << 31) for value in acc)
    return {"acc": acc, "partials": partials, "fault": fault,
            "result": [0, 0, 0] if fault else acc,
            "writes": [] if fault else [destination for destination in task["destinations"]
                                         if destination is not None]}


def compare(task, read_pixel, kernel, bias, stride, pad=0):
    """独立九项卷积作对照；量化参数按逻辑通道，不按打包后的物理lane。"""
    direct = []
    for destination in task["destinations"]:
        if destination is None:
            direct.append(0)
            continue
        y, x, channel = destination
        direct.append(bias + sum(read_pixel(y * stride - pad + row,
                                           x * stride - pad + col, channel)
                                 * kernel[row * 3 + col]
                                 for row in range(3) for col in range(3)))
    result = evaluate(task)
    assert result["acc"] == direct
    assert result["fault"] == any(not -(1 << 31) <= value < (1 << 31)
                                  for value in direct)
    stages = []
    if not result["fault"]:
        for lane, destination in enumerate(task["destinations"]):
            if destination is not None:
                stage = POST["quantize"](result["acc"][lane], destination[2] % 3)
                assert stage == POST["quantize"](direct[lane], destination[2] % 3)
                stages.append({"destination": destination, "acc": direct[lane],
                               "pre": stage[0], "silu": stage[1],
                               "post": stage[2], "output": stage[3]})
    return result, stages


def self_check():
    rng = random.Random(42)
    checks = 0
    samples = []
    for stride in (1, 2):
        for height, width in ((1, 1), (3, 4), (9, 9), (11, 13)):
            pixels = [[[rng.randint(-128, 127) for _ in range(3)]
                       for _ in range(width)] for _ in range(height)]
            def read_pixel(y, x, channel):
                return pixels[y][x][channel] if 0 <= y < height and 0 <= x < width else 0
            for y in range((height - 1) // stride + 1):
                for x in range((width - 1) // stride + 1):
                    row_remaining = (width - 1) // stride + 1 - x
                    for count in range(1, min(3, row_remaining) + 1):
                        for channel in range(3):
                            kernel = [rng.randint(-128, 127) for _ in range(9)]
                            bias = rng.randint(-10000, 10000)
                            task = pack_windows(read_pixel, kernel, bias, stride,
                                                y, x, channel, count, pad=1)
                            result, stages = compare(task, read_pixel, kernel, bias, stride, pad=1)
                            assert task["union_size"] == (15 if stride == 1 else 21)
                            assert task["beats"][-1]["input_mask"] == (127 if stride == 1 else 31)
                            assert len(result["writes"]) == count
                            assert len(set(map(tuple, result["writes"]))) == count
                            # 后续组的bias故意扰动，证明只有first加入bias。
                            task["beats"][-1]["bias"] = [123, -456, 789]
                            assert evaluate(task) == result
                            checks += 1
                            if len(samples) < 6:
                                samples.append({"task": task, "expected": result, "stages": stages})

    # 原冻结4x4/s2、16通道的三组halo：对拍全部DW和配对PW中间值。
    frozen_tiles = []
    for origin in ((0, 0), (20, 30), (68, 124)):
        halo, _ = TILE["halo"](*origin)
        expected_dw, expected_records = TILE["depthwise"](halo)
        expected_pw, expected_pw_records = TILE["pointwise"](expected_dw)
        def read_halo(y, x, channel):
            return halo[(y * 9 + x) * 16 + channel] if 0 <= y < 9 and 0 <= x < 9 else 0
        produced = [None] * 256
        tasks = []
        for y in range(4):
            for x, count in ((0, 3), (3, 1)):
                for channel in range(16):
                    kernel = TILE["dw_weights"]()[channel * 9:channel * 9 + 9]
                    bias = TILE["dw_biases"]()[channel]
                    task = pack_windows(read_halo, kernel, bias, 2, y, x, channel, count)
                    result, stages = compare(task, read_halo, kernel, bias, 2)
                    for record in stages:
                        row, col, chan = record["destination"]
                        address = (row * 4 + col) * 16 + chan
                        expected = expected_records[address]
                        assert produced[address] is None
                        assert all(record[key] == expected[key]
                                   for key in ("acc", "pre", "silu", "post", "output"))
                        produced[address] = record["output"]
                    tasks.append({"task": task, "expected": result, "stages": stages})
        assert produced == expected_dw
        actual_pw, actual_pw_records = TILE["pointwise"](produced)
        assert actual_pw == expected_pw and actual_pw_records == expected_pw_records
        frozen_tiles.append({"origin": origin, "tasks": tasks,
                             "dw_values": len(produced), "pw_values": len(actual_pw),
                             "accepted_mac_beats": sum(len(row["task"]["beats"]) for row in tasks)})

    # INT32末组溢出必须取消全组三个写入；合法极值没有中途截断。
    for pixel, weight, bias, fault in ((-128, -128, (1 << 31) - 1, True),
                                      (127, -128, -(1 << 31), True),
                                      (-128, -128, -(1 << 31), False),
                                      (127, -128, (1 << 31) - 1, False)):
        for count in (1, 2, 3):
            reader = lambda y, x, channel: pixel
            task = pack_windows(reader, [weight] * 9, bias, 2, 0, 0, 0, count)
            result, _ = compare(task, reader, [weight] * 9, bias, 2)
            assert result["fault"] == fault
            assert len(result["writes"]) == (0 if fault else count)
            checks += 1
    # stride2各窗中心互不重叠：只有任意一条输出路溢出时，也不得写另两条。
    for target in range(3):
        for polarity in (-1, 1):
            bias = (1 << 31) - 2 if polarity == 1 else -(1 << 31) + 1
            reader = lambda y, x, channel: polarity * 2 if (y, x) == (1, 2 * target + 1) else 0
            kernel = [0, 0, 0, 0, 1, 0, 0, 0, 0]
            task = pack_windows(reader, kernel, bias, 2, 0, 0, 0, 3)
            result, _ = compare(task, reader, kernel, bias, 2)
            overflowing = [lane for lane, value in enumerate(result["acc"])
                           if not -(1 << 31) <= value < (1 << 31)]
            assert overflowing == [target] and result["fault"] and not result["writes"]
            checks += 1
    return {"status": "CPU_NUMERIC_PASS", "random_and_boundary_tasks": checks,
            "frozen_tiles": frozen_tiles, "sample_tasks": samples,
            "old_dw_tasks_per_tile": 256, "packed_dw_tasks_per_tile": 128,
            "old_dw_mac_beats_per_tile": 512, "packed_dw_mac_beats_per_tile": 384,
            "scope": "test parameters; CPU packing/numeric/address reference only; no RTL cycle/FPS claim"}


if __name__ == "__main__":
    report = self_check()
    report["source_sha256"] = {str(path): hashlib.sha256(path.read_bytes()).hexdigest()
                               for path in (Path(__file__), MAC_SOURCE, POST_SOURCE, TILE_SOURCE,
                                            POST["FROZEN_SILU"])}
    (ROOT / "reference_receipt.json").write_text(json.dumps(report, ensure_ascii=False, indent=2),
                                               encoding="utf-8")
    print(json.dumps({key: value for key, value in report.items()
                      if key not in ("frozen_tiles", "sample_tasks")}, ensure_ascii=False))
