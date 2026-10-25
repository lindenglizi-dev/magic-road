"""与 RTL 对拍的整数契约；不使用浮点运算替代部署路径。

浮点仅用于一次性生成查表常量。完整帧输入与所有输出坐标都可追溯。
"""

from __future__ import annotations

import heapq
import math
from functools import lru_cache

import numpy as np


def round_div_even(values: np.ndarray | int, divisor: int) -> np.ndarray:
    """有符号除法，最近偶数；调用者须保证输入不等于 INT64_MIN。"""
    if divisor <= 0:
        raise ValueError("divisor 必须为正整数")
    source = np.asarray(values, dtype=np.int64)
    if np.any(source == np.iinfo(np.int64).min):
        raise OverflowError("INT64_MIN 不能先取绝对值")
    absolute = np.abs(source)
    quotient, remainder = np.divmod(absolute, divisor)
    # 不将 remainder 乘二，避免一般除数附近溢出。
    above = remainder > divisor - remainder
    tie = remainder == divisor - remainder
    quotient = quotient + (above | (tie & ((quotient & 1) != 0)))
    return np.where(source < 0, -quotient, quotient)


def requantize(values: np.ndarray, multiplier: np.ndarray | int,
               shift: np.ndarray | int, minimum: int = -128,
               maximum: int = 127) -> np.ndarray:
    """INT32×正INT32，INT64乘积，右移RNE并饱和。"""
    source = np.asarray(values)
    mul = np.asarray(multiplier)
    amount = np.asarray(shift)
    if any(item.dtype.kind not in 'iu' for item in (source, mul, amount)):
        raise ValueError("重定标输入、乘数和移位必须为整数")
    if np.any(source < -(1 << 31)) or np.any(source >= (1 << 31)):
        raise OverflowError("累加值超出 INT32")
    if np.any(mul < 0) or np.any(mul >= (1 << 31)):
        raise ValueError("multiplier 必须是非负 INT32")
    if np.any(amount < 0) or np.any(amount > 62):
        raise ValueError("shift 必须位于0..62")
    source, mul, amount = (item.astype(np.int64) for item in (source, mul, amount))
    product, amounts = np.broadcast_arrays(source * mul, amount)
    result = np.empty(product.shape, dtype=np.int64)
    for unique_shift in np.unique(amounts):
        selected = amounts == unique_shift
        result[selected] = round_div_even(product[selected], 1 << int(unique_shift))
    return np.clip(result, minimum, maximum)


def encode_multiplier(scale: float) -> tuple[int, int]:
    """将正比例编码为 multiplier/2**shift，拒绝不可表达比例。"""
    if not math.isfinite(scale) or scale <= 0:
        raise ValueError("量化比例须为有限正数")
    mantissa, exponent = math.frexp(scale)
    multiplier = round(mantissa * (1 << 31))
    if multiplier == 1 << 31:
        multiplier //= 2
        exponent += 1
    shift = 31 - exponent
    if not 0 <= shift <= 62:
        raise ValueError("量化比例超出部署重定标范围")
    return multiplier, shift


def resize_area(rgb: np.ndarray) -> np.ndarray:
    """原生720p RGB的5→2面积缩放，二维累加完成后一次RNE。"""
    if rgb.shape != (720, 1280, 3) or rgb.dtype != np.uint8:
        raise ValueError("输入必须为720×1280×3 uint8 RGB")
    blocks = rgb.astype(np.uint16).reshape(144, 5, 256, 5, 3)
    horizontal = np.stack((2 * blocks[:, :, :, 0] + 2 * blocks[:, :, :, 1]
                           + blocks[:, :, :, 2],
                           blocks[:, :, :, 2] + 2 * blocks[:, :, :, 3]
                           + 2 * blocks[:, :, :, 4]), axis=3)
    total = np.stack((2 * horizontal[:, 0] + 2 * horizontal[:, 1] + horizontal[:, 2],
                      horizontal[:, 2] + 2 * horizontal[:, 3] + 2 * horizontal[:, 4]),
                     axis=1).reshape(288, 512, 3)
    # Maxima: horizontal=1275, total=6375, safely within UINT16.
    # Odd divisor 25 has no half-integer ties: this is exactly one final RNE.
    return ((total + 12) // 25).astype(np.uint8)


@lru_cache(maxsize=1)
def tables() -> dict[str, np.ndarray | int]:
    """1024项不含+8端点，舍入到该端点时使用硬连线常量。"""
    x = -8 + np.arange(1024, dtype=np.float64) / 64
    sigmoid = 1 / (1 + np.exp(-x))
    silu = np.rint(x * sigmoid * 256).astype(np.int16)
    probabilities = np.clip(np.rint(sigmoid * 65536), 0, 65535).astype(np.uint16)
    exponent = np.rint(np.exp(np.linspace(-4, 3.5, 256)) * 1024).astype(np.uint16)
    return {"silu": silu, "sigmoid": probabilities, "exp": exponent,
            "silu_upper": round(8 / (1 + math.exp(-8)) * 256),
            "sigmoid_upper": round(65536 / (1 + math.exp(-8)))}


def silu(values: np.ndarray) -> np.ndarray:
    source = np.asarray(values, dtype=np.int64)
    if np.any(source < -32768) or np.any(source > 32767):
        raise ValueError("SiLU 输入超出 INT16")
    address = round_div_even(source, 4) + 512
    constants = tables()
    result = constants["silu"][np.clip(address, 0, 1023)].astype(np.int64)
    result = np.where(address == 1024, constants["silu_upper"], result)
    result = np.where(source <= -2048, 0, result)
    result = np.where(source >= 2048, source, result)
    return result.astype(np.int16)


def sigmoid(values: np.ndarray) -> np.ndarray:
    source = np.asarray(values, dtype=np.int64)
    if np.any(source < -32768) or np.any(source > 32767):
        raise ValueError("sigmoid 输入超出 INT16")
    address = round_div_even(source, 4) + 512
    constants = tables()
    result = constants["sigmoid"][np.clip(address, 0, 1023)].astype(np.int64)
    result = np.where(address == 1024, constants["sigmoid_upper"], result)
    result = np.where(source <= -2048, 0, result)
    result = np.where(source >= 2048, 65535, result)
    return result.astype(np.uint16)


def exponent(values: np.ndarray) -> np.ndarray:
    source = np.clip(np.asarray(values, dtype=np.int64), -1024, 896)
    address = round_div_even((source + 1024) * 255, 1920)
    return tables()["exp"][address]


def conv2d(image: np.ndarray, weights: np.ndarray, bias: np.ndarray,
           stride: int = 1, padding: int = 0, groups: int = 1) -> np.ndarray:
    """NHWC INT8 × OIHW INT8 → NHWC INT32，小向量黄金模型。

    累加在INT64中完成，再检查INT32范围，绝不静默回绕。
    """
    if image.dtype != np.int8 or weights.dtype != np.int8:
        raise ValueError("卷积输入及权重必须为INT8")
    if image.ndim != 3 or weights.ndim != 4 or stride < 1 or padding < 0:
        raise ValueError("卷积形状、stride或padding非法")
    out_channels, per_group, kh, kw = weights.shape
    if groups < 1 or image.shape[2] != per_group * groups or out_channels % groups:
        raise ValueError("卷积分组不一致")
    biases = np.asarray(bias)
    if biases.dtype.kind not in 'iu':
        raise ValueError("bias必须为整数")
    if biases.shape != (out_channels,):
        raise ValueError("bias长度不一致")
    if np.any(biases < -(1 << 31)) or np.any(biases >= (1 << 31)):
        raise OverflowError("bias超出 INT32")
    biases = biases.astype(np.int64)
    padded = np.pad(image, ((padding, padding), (padding, padding), (0, 0)))
    height = (padded.shape[0] - kh) // stride + 1
    width = (padded.shape[1] - kw) // stride + 1
    if height <= 0 or width <= 0:
        raise ValueError("卷积输出为空")
    output = np.empty((height, width, out_channels), dtype=np.int64)
    channels_per_output_group = out_channels // groups
    for channel in range(out_channels):
        start = (channel // channels_per_output_group) * per_group
        kernel = weights[channel].transpose(1, 2, 0).astype(np.int64)
        for y in range(height):
            for x in range(width):
                patch = padded[y * stride:y * stride + kh,
                               x * stride:x * stride + kw,
                               start:start + per_group].astype(np.int64)
                output[y, x, channel] = np.sum(patch * kernel) + biases[channel]
    if np.any(output < -(1 << 31)) or np.any(output >= (1 << 31)):
        raise OverflowError("卷积累加溢出 INT32")
    return output.astype(np.int32)


def _decode(raw: np.ndarray, x: int, y: int, stride: int) -> tuple[int, ...]:
    center = (raw[:2].astype(np.int64) + np.array([x, y]) * 256) * stride
    size = round_div_even(exponent(raw[2:4]).astype(np.int64) * stride, 4)
    half = round_div_even(size, 2)
    low, high = center - half, center + half
    box = np.concatenate((low, high))
    return tuple(np.clip(box, 0, [512 * 256, 288 * 256] * 2).tolist())


def _overlap_half(first: tuple[int, ...], second: tuple[int, ...]) -> bool:
    width = max(0, min(first[2], second[2]) - max(first[0], second[0]))
    height = max(0, min(first[3], second[3]) - max(first[1], second[1]))
    intersection = width * height
    area_first = (first[2] - first[0]) * (first[3] - first[1])
    area_second = (second[2] - second[0]) * (second[3] - second[1])
    return 2 * intersection > area_first + area_second - intersection


def postprocess(heads: list[np.ndarray], thresholds: tuple[int, int],
                top_k: int = 128, max_boxes: int = 32) -> list[dict]:
    """三尺度HWC7 Q7.8输出；每类Top-K、整数IoU0.5 NMS。"""
    if len(heads) != 3 or not 1 <= top_k <= 128 or not 1 <= max_boxes <= 32:
        raise ValueError("后处理规格不一致")
    if len(thresholds) != 2 or any(not 0 <= t <= 65535 for t in thresholds):
        raise ValueError("thresholds须为两个UINT16")
    heaps: list[list] = [[], []]
    cell = 0
    for head, stride in zip(heads, (4, 8, 16), strict=True):
        if head.shape != (288 // stride, 512 // stride, 7) or head.dtype != np.int16:
            raise ValueError("head须符合HWC7 INT16，stride4/8/16")
        probabilities = sigmoid(head[..., 4:]).astype(np.int64)
        scores = round_div_even(probabilities[..., :1] * probabilities[..., 1:], 65536)
        for y, x in np.ndindex(head.shape[:2]):
            for label in (0, 1):
                score = int(scores[y, x, label])
                if score < thresholds[label]:
                    continue
                record = (score, -cell, stride, y, x, tuple(int(v) for v in head[y, x, :4]))
                heap = heaps[label]
                if len(heap) < top_k:
                    heapq.heappush(heap, record)
                elif record[:2] > heap[0][:2]:
                    heapq.heapreplace(heap, record)
            cell += 1
    detections = []
    for label, heap in enumerate(heaps):
        kept = []
        for score, negative_cell, stride, y, x, raw in sorted(heap, reverse=True):
            box = _decode(np.array(raw, dtype=np.int16), x, y, stride)
            if box[0] >= box[2] or box[1] >= box[3]:
                continue
            if any(_overlap_half(box, previous) for previous in kept):
                continue
            kept.append(box)
            source = round_div_even(np.array(box) * 5, 512).tolist()
            detections.append({"label": label, "score_uint16": score,
                               "cell_id": -negative_cell,
                               "box_q8": list(box), "box_source": source})
            if len(kept) == max_boxes:
                break
    return detections
