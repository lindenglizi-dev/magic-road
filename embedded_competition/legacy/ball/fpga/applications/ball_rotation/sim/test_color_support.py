"""正式模型的暗部/稀疏噪点语义，用于生成RTL逐组对照向量。"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT/'python' if (ROOT/'python').is_dir() else ROOT/'python_sim'
sys.path.insert(0, str(MODEL_DIR))
from pipeline import Config, ComponentRAM, segment


def main():
    cfg = Config(width=160, height=192, roi=(0, 0, 160, 192),
                 gate=(56, 0, 104, 192), line=80, hysteresis=4)
    yy, xx = np.indices((192, 160))
    circle = (xx-80)**2+(yy-130)**2 <= 24**2
    for color, pixel in ((1, (60, 28, 24)), (2, (60, 58, 20)), (3, (24, 60, 28))):
        rgb = np.full((192, 160, 3), 20, np.uint8)
        rgb[circle] = pixel
        rgb[10, 80] = (220, 20, 20) if color != 1 else (20, 220, 20)
        mask = segment(rgb, cfg)
        assert np.count_nonzero(mask == color) > 1500 and mask[10, 80] == 0
        store = ComponentRAM(cfg)
        result = store.scan(store.capture(mask, 0, 0), mask)
        assert len(result.candidates) == 1 and result.candidates[0].color == color
        assert 104 <= result.candidates[0].box[1] <= 108
    # 无彩色的暗灰/白/青色以及单像素红噪点都不能变成球。
    rgb = np.full((192, 160, 3), (30, 30, 30), np.uint8)
    rgb[0:20] = (255, 255, 255)
    rgb[20:40] = (24, 60, 64)
    rgb[50, 80] = (220, 20, 20)
    assert not np.any(segment(rgb, cfg))
    # 门限两侧的确定样本：31/32、色差6/7、相对优势等于/大于9:8。
    boundary_cases = [
        ([(31, 0, 0)]*4, [0]*4), ([(32, 0, 0)]*4, [1]*4),
        ([(32, 26, 26)]*4, [0]*4), ([(33, 26, 26)]*4, [1]*4),
        ([(72, 64, 64)]*4, [0]*4), ([(73, 64, 64)]*4, [1]*4),
        ([(32, 32, 0)]*4, [2]*4), ([(0, 32, 0)]*4, [3]*4),
        ([(60, 28, 24)]*2+[(20, 20, 20)]*2, [0]*4),
        ([(60, 28, 24)]*3+[(20, 20, 20)], [1, 1, 1, 0]),
        ([(160, 0, 0)]*2+[(20, 20, 20)]*2, [1, 1, 0, 0]),
    ]
    for pixels, expected in boundary_cases:
        image = np.zeros((192, 160, 3), np.uint8)
        image[0, :4] = pixels
        assert segment(image, cfg)[0, :4].tolist() == expected, (pixels, expected)
    rng = np.random.default_rng(20261018)
    rows = []
    for strict in (False, True):
        from dataclasses import replace
        local = replace(cfg, strict=strict)
        for index in range(1024):
            group = rng.integers(0, 256, (4, 3), dtype=np.uint8)
            if index < 512:
                group[1:4] = group[0]
            if index < len(boundary_cases):
                group = np.asarray(boundary_cases[index][0], dtype=np.uint8)
            image = np.zeros((192, 160, 3), np.uint8)
            image[0, :4] = group
            labels = segment(image, local)[0, :4]
            packed = sum(int(label) << (lane*2) for lane, label in enumerate(labels))
            rows.append(f'{int(strict)} {group.tobytes().hex()} {packed:02x}\n')
    (ROOT/'sim/color_support_vectors.txt').write_text(''.join(rows), encoding='ascii')
    (ROOT/'reports/color_support_model.json').write_text(json.dumps({
        'status':'PASS', 'rgb_group_vectors':len(rows),
        'dark_colors':3, 'boundary_cases':len(boundary_cases), 'isolated_foreground_pixel_rejected':True,
        'limitation':'Four-pixel horizontal support does not separate dense disconnected background.',
        'sensor_rgb_measured':False}, indent=2)+'\n', encoding='utf-8')
    print('PASS model:3dim balls recovered; isolated noise/gray/white/cyan rejected;2048group vectors')


if __name__ == '__main__':
    main()
