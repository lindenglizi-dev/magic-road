"""核对RTL候选、暗球几何真值，并从真实DDR输出恢复画面。"""

import argparse
import csv
import json
from pathlib import Path
import sys

import numpy as np
from PIL import Image


def main():
    app = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument('--python-dir', type=Path, default=app/'python_sim')
    args = parser.parse_args()
    sys.path.insert(0, str(args.python_dir))
    from pipeline import Config, Pipeline, segment

    cfg = Config(width=160, height=96, roi=(0, 0, 160, 96), gate=(56, 0, 104, 96),
                 line=80, hysteresis=4, min_area=16, min_size=3, max_size=64, max_move=12)
    engine = Pipeline(cfg)
    palette = np.array(((24, 24, 24), (255, 32, 32), (255, 255, 0), (0, 255, 64)), np.uint8)
    actual_candidates = list(csv.reader((app/'sim/core_candidates.csv').open()))
    actual_frames = list(csv.reader((app/'sim/core_frames.csv').open()))
    expected_candidates, expected_frames = [], []
    for row in csv.reader((app/'sim/core_input.csv').open()):
        frame_id, first_x, first_c, second_x, second_c, many = map(int, row)
        rgb = np.full((96, 160, 3), 24, np.uint8)
        for center, color in ((first_x, first_c), (second_x, second_c)):
            if color:
                rgb[40:57, max(0, center-8):min(160, center+9)] = palette[color]
        if many:
            rgb[40:57, (np.arange(160) % 16 >= 4) & (np.arange(160) % 16 <= 12)] = palette[1]
        stats = engine.analyse(rgb)
        for detection in stats.candidates:
            x0, y0, x1, y1 = detection.box
            expected_candidates.append(list(map(str, (frame_id, detection.color, detection.area, x0, y0, x1, y1))))
        expected_frames.append(list(map(str, (frame_id, stats.raw_gate_pixels, int(stats.overflow)))))
    assert actual_candidates == expected_candidates, 'RTL/Python候选不一致'
    assert actual_frames == expected_frames, 'RTL/Python门区占用或溢出不一致'

    # 几何真值独立于分类算法；输入为暗球、青色纹理及无色高光。
    y, x = np.indices((224, 240))
    dx, dy = x-120, y-112
    sphere = dx*dx+dy*dy <= 85*85
    highlight = (dx+20)**2+(dy+20)**2 <= 64
    shade = np.clip(dx+85, 0, 170)
    knots = np.array((0, 37, 60, 79, 97, 113, 129, 143, 157, 171, 184, 197, 209, 221, 233, 244, 255))
    raw_values = np.arange(256)
    tone = knots[raw_values//16] + ((knots[raw_values//16+1]-knots[raw_values//16])*(raw_values % 16)+8)//16
    tone[255] = 255
    gamma_error = float(np.max(np.abs(tone - 255*(raw_values/255)**0.7)))
    # 首个16级区间作线性插值，曲线最大误差出现在输入4，约4.91级。
    assert gamma_error < 5
    large_cfg = Config(width=240, height=224, roi=(0, 0, 240, 224), gate=(80, 0, 160, 224), line=120, hysteresis=8)
    for color in (1, 2, 3):
        raw = np.stack((np.full_like(x, 60), 120+(x+y) % 7, 130+(3*x+y) % 7), axis=-1)
        dominant, secondary, blue = 45+40*shade//170, 22+23*shade//170, 18+12*shade//170
        channels = (dominant, secondary, blue) if color == 1 else (secondary, dominant, blue)
        if color == 2:
            channels = dominant, 43+38*shade//170, 8+12*shade//170
        for channel, values in enumerate(channels):
            raw[:, :, channel][sphere] = values[sphere]
        raw[sphere & highlight] = 245
        expected_mask = np.where(sphere & ~highlight, color, 0)
        assert np.array_equal(segment(tone[raw].astype(np.uint8), large_cfg), expected_mask)

    lines = (app/'sim/hdmi_lowlight_frame.hex').read_text().splitlines()
    assert len(lines) == 172800 and all(len(line) == 32 for line in lines)
    capture = np.frombuffer(bytes.fromhex(''.join(lines)), np.uint8).reshape(720, 1280, 3)
    # 圆的最左列只有一个像素，被每列至少两点的规则排除，故框左边为217。
    probes = {'tracked_center': (400, 316, (255, 64, 80)), 'tracked_box': (300, 217, (255, 64, 80)),
              'current_ball': (400, 332, (98, 46, 40)), 'gamma_background': (200, 100, (49, 93, 97)),
              'gamma_label': (16, 402, (220, 232, 240))}
    for name, (py, px, expected) in probes.items():
        assert tuple(capture[py, px]) == expected, (name, capture[py, px], expected)
    Image.fromarray(capture).save(app/'reports/rtl_hdmi_lowlight.png')
    report = {'status': 'PASS', 'core_frames': len(expected_frames), 'candidate_comparisons': len(expected_candidates),
              'shaded_color_masks': 3, 'gamma_max_curve_error': gamma_error,
              'actual_rtl_capture_words': len(lines), 'pixel_probes': list(probes),
              'scope': 'Software and RTL simulation; not a physical camera measurement'}
    (app/'reports/lowlight_numeric_checks.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report), flush=True)


if __name__ == '__main__':
    main()
