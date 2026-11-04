"""四像素输入、RGB96→128打包与双帧缓存的功能模型。"""

import numpy as np


class FourPixelInput:
    """early独立开帧；坐标仅在有效的12字节RGB组到来时推进。"""

    def __init__(self, width, height):
        if width <= 0 or width % 16 or height <= 0:
            raise ValueError('图像宽度必须为16的倍数，高度必须为正')
        self.width, self.height = width, height
        self.x = self.y = 0
        self.active = self.pending = False

    def step(self, data=None, early=False):
        if early:
            if self.active:
                raise ValueError('上一帧未结束就收到early')
            self.x = self.y = 0
            self.active = self.pending = True
        if data is None:
            return None
        if not self.active or len(data) != 12:
            raise ValueError('有效像素组必须属于完整帧且恰为12字节')
        x, y, sof = self.x, self.y, self.pending
        self.pending = False
        eol = x == self.width - 4
        eof = eol and y == self.height - 1
        self.x = 0 if eol else x + 4
        self.y = y + 1 if eol else y
        if eof:
            self.active = False
        return data, x, y, sof, eol, eof


class RGB96Packer:
    """四个有效RGB96组形成三个RGB128字，空拍不推进状态。"""

    def __init__(self):
        self.pending = bytearray()

    def step(self, data=None, sof=False, eol=False, eof=False):
        if sof:
            if self.pending:
                raise ValueError('新帧开始时还有未打包字节')
            self.pending.clear()
        if data is None:
            if eol or eof:
                raise ValueError('行帧尾必须随有效数据')
            return None
        if len(data) != 12:
            raise ValueError('RGB96组必须恰为12字节')
        self.pending.extend(data)
        word = None
        if len(self.pending) >= 16:
            word = bytes(self.pending[:16])
            del self.pending[:16]
        if (eol or eof) and (word is None or self.pending):
            raise ValueError('行帧尾未对齐完整128位字')
        return None if word is None else (word, eol, eof)


def pack_frame(rgb):
    """与逐组模型相同的字节排列；批量执行以便交互预览。"""
    if rgb.dtype != np.uint8 or rgb.ndim != 3 or rgb.shape[2] != 3:
        raise ValueError('帧必须为H×W×3 uint8 RGB')
    if rgb.shape[1] % 16:
        raise ValueError('行宽必须为16的倍数')
    groups = np.ascontiguousarray(rgb).reshape(-1, 12)
    return groups.reshape(-1, 4, 12).reshape(-1, 3, 16).reshape(-1, 16).copy()


class DDRFrameBuffer:
    """每次写入当前帧，HDMI功能输出读取上一帧，启动时输出黑帧。"""

    def __init__(self):
        self.banks = [None, None]
        self.write_bank = 0

    def exchange(self, rgb, metadata):
        words = pack_frame(rgb)
        old = self.banks[1 - self.write_bank]
        self.banks[self.write_bank] = (words, rgb.shape, metadata)
        self.write_bank = 1 - self.write_bank
        if old is None:
            return np.zeros_like(rgb), None, len(words)
        data, shape, old_metadata = old
        return data.reshape(shape).copy(), old_metadata, len(words)
