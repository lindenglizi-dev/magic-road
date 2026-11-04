"""解码实际DDR捕获，并以独立像素场景/字模检查冻结的二维诊断行。"""

import json
from pathlib import Path
import sys

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'python' if (ROOT/'python').is_dir() else ROOT/'python_sim'))
from pipeline import ComponentRAM, Config, segment, GateCounter

FONT = {
 ' ': '00000_00000_00000_00000_00000_00000_00000',
 '0': '01110_10001_10011_10101_11001_10001_01110',
 '1': '00100_01100_00100_00100_00100_00100_01110',
 '2': '01110_10001_00001_00010_00100_01000_11111',
 '3': '11110_00001_00001_01110_00001_00001_11110',
 '4': '00010_00110_01010_10010_11111_00010_00010',
 '5': '11111_10000_10000_11110_00001_00001_11110',
 '6': '01110_10000_10000_11110_10001_10001_01110',
 '7': '11111_00001_00010_00100_01000_01000_01000',
 '8': '01110_10001_10001_01110_10001_10001_01110',
 '9': '01110_10001_10001_01111_00001_00001_01110',
 'A': '01110_10001_10001_11111_10001_10001_10001',
 'B': '11110_10001_10001_11110_10001_10001_11110',
 'C': '01111_10000_10000_10000_10000_10000_01111',
 'D': '11110_10001_10001_10001_10001_10001_11110',
 'E': '11111_10000_10000_11110_10000_10000_11111',
 'F': '11111_10000_10000_11110_10000_10000_10000',
 'G': '01111_10000_10000_10111_10001_10001_01111',
 'H': '10001_10001_10001_11111_10001_10001_10001',
 'L': '10000_10000_10000_10000_10000_10000_11111',
 'N': '10001_11001_10101_10011_10001_10001_10001',
 'O': '01110_10001_10001_10001_10001_10001_01110',
 'P': '11110_10001_10001_11110_10000_10000_10000',
 'R': '11110_10001_10001_11110_10100_10010_10001',
 'S': '01111_10000_10000_01110_00001_00001_11110',
 'T': '11111_00100_00100_00100_00100_00100_00100',
 'U': '10001_10001_10001_10001_10001_10001_01110',
 'W': '10001_10001_10001_10101_10101_10101_01010',
 'X': '10001_10001_01010_00100_01010_10001_10001',
 'Y': '10001_10001_01010_00100_00100_00100_00100',
 '=': '00000_00000_11111_00000_11111_00000_00000',
 '%': '11001_11010_00100_01000_10110_00110_00000',
}


def gamma_table():
    base = np.array([0, 37, 60, 79, 97, 113, 129, 143, 157, 171, 184, 197, 209, 221, 233, 244])
    delta = np.array([37, 23, 19, 18, 16, 16, 14, 14, 14, 13, 13, 12, 12, 12, 11, 11])
    value = np.arange(256)
    result = base[value//16]+(delta[value//16]*(value % 16)+8)//16
    result[255] = 255
    return result.astype(np.uint8)


def scene(center):
    y, x = np.indices((720, 1280))
    image = np.full((720, 1280, 3), (24, 60, 64), np.uint8)
    circle = (x-center)**2+(y-400)**2 <= 10000
    shade = 45+(y-300)//5
    image[circle, 0] = shade[circle]
    image[circle, 1] = shade[circle]
    image[circle, 2] = 18
    highlight = circle & (y >= 370) & (y <= 390) & (x >= center+20) & (x <= center+40)
    image[highlight] = 200
    for row in (180,204,228,252):
        for column in (552,680):image[row:row+4,column:column+4]=(255,32,32)
    return gamma_table()[image]


def main():
    lines = (ROOT/'sim/hdmi_count_recovery_frame.hex').read_text(encoding='ascii').splitlines()
    assert len(lines) == 172800 and all(len(line) == 32 for line in lines), '完整捕获尚未生成'
    image = np.frombuffer(bytes.fromhex(''.join(lines)), np.uint8).reshape(720, 1280, 3)
    cfg = Config()
    store = ComponentRAM(cfg)
    counter = GateCounter(cfg)
    for frame, center in enumerate((-1000,-1000,-1000,580,580,700)):
        mask = segment(scene(center), cfg)
        stats = store.scan(store.capture(mask,frame,0),mask)
        counter.update(stats)
    assert counter.counts == {1:0,2:1,3:0} and counter.state == 'HOLD'
    assert len(stats.candidates) == 1
    box = stats.candidates[0]
    assert box.center == (699, 399), box.center
    count, w, h, area, fill, rejected = stats.diagnostic
    expected_text = f'CCL4 N={count} W={w:04d} H={h:04d} A={area:07d} F={fill:03d}% R={rejected:X}'
    checked = []

    def check_text(text, column, top, ink=(220,232,240)):
        for offset, character in enumerate(text):
            left = 16+(column+offset)*16
            bits = np.array([[int(bit) for bit in row] for row in FONT[character].split('_')], np.uint8)
            expected = np.full((14, 16, 3), (16, 28, 42), np.uint8)
            pixels = np.repeat(np.repeat(bits, 2, axis=0), 2, axis=1).astype(bool)
            expected[:, :10][pixels] = ink
            assert np.array_equal(image[top:top+14, left:left+16], expected), (top, column+offset, character)
            checked.append(dict(character=character, column=column+offset, y=top))

    check_text(expected_text, 0, 128)
    check_text(f'X={box.center[0]:04d}', 0, 72)
    check_text(f'Y={box.center[1]:04d}', 10, 72)
    check_text('FPS=060 EXP=0480', 0, 96)
    check_text('G=16', 18, 96)
    check_text('RB=1', 24, 96)
    check_text('WB=1', 30, 96)
    check_text('    ', 32, 16)
    check_text('COUNT2', 16, 16)
    check_text('0000000001',45,40,ink=(255,223,32))
    probes = []
    for x, y, wanted in [(box.box[0], 400, (255, 223, 32)), (box.box[2], 400, (255, 223, 32)),
                         (*box.center, (255, 223, 32)), (350, 450, tuple(int(v) for v in scene(700)[450, 350])),
                         (100, 200, tuple(int(v) for v in scene(700)[200, 100])),
                         (552,180,tuple(int(v) for v in scene(700)[180,552]))]:
        actual = tuple(int(v) for v in image[y, x])
        assert actual == wanted, (x, y, actual, wanted)
        probes.append(dict(x=x, y=y, rgb=actual))
    destination = ROOT/'reports/rtl_hdmi_count_recovery.png'
    ok, encoded = cv2.imencode('.png', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    assert ok
    encoded.tofile(str(destination))
    report = dict(words=len(lines), shape=list(image.shape), diagnostic=expected_text,
                  displayed_center=box.center, glyphs_checked=len(checked), pixel_probes=probes,
                  counts=counter.counts,scope='Actual RTL synthetic COUNT capture, persistent sparse noise, measured yellow crossing=1. Not board data.')
    (ROOT/'reports/count_pixel_checks.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print('PASS actual DDR capture:', expected_text, 'glyphs=', len(checked), 'probes=', len(probes))


if __name__ == '__main__':
    main()
