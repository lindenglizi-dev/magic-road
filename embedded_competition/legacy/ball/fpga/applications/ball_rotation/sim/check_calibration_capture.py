"""从实际RTL DDR输出恢复画面，并读取第四行标定信息。"""
import json
from pathlib import Path

import numpy as np
from PIL import Image


def main():
    app = Path(__file__).resolve().parents[1]
    lines = (app/'sim/hdmi_lowlight_frame.hex').read_text(encoding='ascii').splitlines()
    assert len(lines) == 172800 and all(len(line) == 32 for line in lines)
    rgb = np.frombuffer(bytes.fromhex(''.join(lines)), dtype=np.uint8).reshape(720, 1280, 3)
    font = {
        'F':'11111_10000_10000_11110_10000_10000_10000',
        'P':'11110_10001_10001_11110_10000_10000_10000',
        'S':'01111_10000_10000_01110_00001_00001_11110',
        '=':'00000_00000_11111_00000_11111_00000_00000',
        '0':'01110_10001_10011_10101_11001_10001_01110',
        '1':'00100_01100_00100_00100_00100_00100_01110',
        '4':'00010_00110_01010_10010_11111_00010_00010',
        '6':'01110_10000_10000_11110_10001_10001_01110',
        '8':'01110_10001_10001_01110_10001_10001_01110',
        'E':'11111_10000_10000_11110_10000_10000_11111',
        'X':'10001_10001_01010_00100_01010_10001_10001',
        'G':'01111_10000_10000_10111_10001_10001_01111',
        'R':'11110_10001_10001_11110_10100_10010_10001',
        'B':'11110_10001_10001_11110_10001_10001_11110',
        'W':'10001_10001_10001_10101_10101_10101_01010',
        'C':'01111_10000_10000_10000_10000_10000_01111',
        'A':'01110_10001_10001_11111_10001_10001_10001',
        'L':'10000_10000_10000_10000_10000_10000_11111',
    }
    # 字符位置由接口约定决定；不从RTL字符选择逻辑复制布局。
    expected = {**dict(enumerate('FPS=060')), **{8+i:c for i,c in enumerate('EXP=0480')},
                **{18+i:c for i,c in enumerate('G=16')}, **{24+i:c for i,c in enumerate('RB=1')},
                **{30+i:c for i,c in enumerate('WB=1')}, **{36+i:c for i,c in enumerate('CAL')}}
    for column, character in expected.items():
        observed = rgb[96:110:2, 16+column*16:26+column*16:2]
        bits = np.all(observed == (220, 232, 240), axis=2).astype(np.uint8)
        target = np.array([list(s) for s in font[character].split('_')], dtype=np.uint8)
        assert np.array_equal(bits, target), (column, character, bits.tolist())
    assert tuple(rgb[400, 316]) == (255, 64, 80), 'tracking center lost'
    assert tuple(rgb[400, 332]) == (98, 46, 40), 'gamma or pixel order changed'
    Image.fromarray(rgb).save(app/'reports/rtl_hdmi_calibration.png')
    report = dict(status='PASS', actual_ddr_words=len(lines), monitor_row='FPS=060 EXP=0480 G=16 RB=1 WB=1 CAL',
                  glyphs_checked=len(expected), tracking_center=(316,400),
                  boundary='RTL output after AWB; camera monitor/I2C/WB tested separately; no physical measurement')
    (app/'reports/calibration_pixel_checks.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
