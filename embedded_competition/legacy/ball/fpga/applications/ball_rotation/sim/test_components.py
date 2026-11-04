"""独立区域基准、实际标签向量和溢出边界，不使用场景目标身份。"""

from dataclasses import replace
import json
from pathlib import Path
import sys

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'python' if (ROOT / 'python').exists()
                       else ROOT/'python_sim'))
from pipeline import ComponentRAM, Config

CFG = Config(width=160, height=128, roi=(8, 8, 152, 120),
             gate=(56, 8, 104, 120), line=80, hysteresis=4,
             min_area=32, min_size=8, max_size=96)


def oracle(mask, cfg):
    """逐单元直方图和OpenCV独立连通标记核对模型。"""
    x0, y0, x1, y1 = cfg.roi
    cells = np.zeros(((y1+3)//4-y0//4, (x1+3)//4-x0//4), np.uint8)
    weights = np.zeros_like(cells)
    for gy in range(cells.shape[0]):
        for gx in range(cells.shape[1]):
            a, b = x0//4*4+gx*4, y0//4*4+gy*4
            patch = mask[b:b+4, a:a+4]
            hist = [int(np.count_nonzero(patch == color)) for color in (1, 2, 3)]
            winner = hist.index(max(hist))
            if hist[winner] >= 4 and hist[winner]*4 >= sum(hist)*3:
                cells[gy, gx], weights[gy, gx] = winner+1, hist[winner]
    regions = []
    for color in (1, 2, 3):
        count, labels, _, _ = cv2.connectedComponentsWithStats((cells == color).astype(np.uint8), connectivity=4)
        for label in range(1, count):
            yy, xx = np.nonzero(labels == label)
            area = int(weights[yy, xx].sum())
            left, top = max(x0, x0//4*4+int(xx.min())*4), max(y0, y0//4*4+int(yy.min())*4)
            right, bottom = min(x1-1, x0//4*4+int(xx.max())*4+3), min(y1-1, y0//4*4+int(yy.max())*4+3)
            w, h = right-left+1, bottom-top+1
            rejection = (int(area < cfg.min_area)
                         | (int(not cfg.min_size <= w <= cfg.max_size or not cfg.min_size <= h <= cfg.max_size) << 1)
                         | (int(w > 2*h or h > 2*w) << 2) | (int(area*4 < w*h) << 3))
            regions.append((int((yy*cells.shape[1]+xx).min()), color, area,
                            (left, top, right, bottom), w, h, area*100//(w*h), rejection))
    regions.sort()
    return regions


def cases():
    yy, xx = np.indices((CFG.height, CFG.width))
    result = [('empty', np.zeros_like(xx, np.uint8))]
    for color in (1, 2, 3):
        mask = np.zeros_like(xx, np.uint8)
        ball = (xx-80)**2+(yy-80)**2 <= 22**2
        mask[ball] = color
        result.append((f'clean_{color}', mask.copy()))
        # 异色/同色区域位于球的相同X列，但与球不相连。
        mask[16:20, 72:88] = color % 3+1
        mask[28:32, 76:84] = color
        result.append((f'same_x_noise_{color}', mask.copy()))
        mask[ball & ((xx+2*yy) % 5 == 0)] = 0
        rng = np.random.default_rng(720+color)
        background = (rng.random(mask.shape) < .008) & ~ball
        background[:8] = background[120:] = False
        background[:, :8] = background[:, 152:] = False
        mask[background] = rng.integers(1, 4, np.count_nonzero(background))
        result.append((f'holed_and_sparse_{color}', mask.copy()))
    for colors in ((1, 1), (1, 3)):
        mask = np.zeros_like(xx, np.uint8)
        mask[(xx-80)**2+(yy-32)**2 <= 12**2] = colors[0]
        mask[(xx-80)**2+(yy-88)**2 <= 12**2] = colors[1]
        result.append((f'same_x_two_{colors}', mask))
    mask = np.zeros_like(xx, np.uint8)
    mask[8:20, 8:20] = 1
    mask[108:120, 140:152] = 3
    result.append(('roi_first_last', mask))
    mask = np.zeros_like(xx, np.uint8)
    distance = (xx-80)**2+(yy-64)**2
    mask[(distance <= 26**2) & (distance >= 24**2)] = 2
    result.append(('reject_thin_ring', mask))
    mask = np.zeros_like(xx, np.uint8)
    mask[44:48, 40:120] = 1
    result.append(('reject_aspect_and_size', mask))
    mask = np.zeros_like(xx, np.uint8)
    for y in (16, 48, 80):
        for x in (16, 64, 112):
            mask[y:y+12, x:x+12] = 1
    result.append(('candidate_overflow', mask))
    return result


def main():
    selected = cases()
    headers, vectors, expected, details = [], [], [], []
    engine = ComponentRAM(CFG)
    for frame_id, (name, mask) in enumerate(selected):
        bank = engine.capture(mask, frame_id, 17+frame_id)
        stats = engine.scan(bank, mask)
        independent = oracle(mask, CFG)
        accepted = [r for r in independent if not r[-1]]
        assert stats.overflow == (len(accepted) > CFG.max_candidates), name
        for actual, wanted in zip(stats.candidates, accepted):
            assert (actual.color, actual.area, actual.box) == (wanted[1], wanted[2], wanted[3]), name
        if not stats.overflow:
            assert len(stats.candidates) == len(accepted), name
            largest = max(independent, key=lambda r: r[2], default=None)
            diag = (0, 0, 0, 0, 0) if largest is None else (*largest[4:7], largest[7])
            # 诊断顺序为宽、高、面积、填充率、拒绝位。
            if largest is not None:
                diag = (largest[4], largest[5], largest[2], largest[6], largest[7])
            assert stats.diagnostic == (len(accepted), *diag), (name, stats.diagnostic, diag)
        n, width, height, area, fill, reject = stats.diagnostic
        header = n | (int(stats.overflow) << 4) | (width << 5) | (height << 17) | (area << 29) | (fill << 49) | (reject << 56)
        headers.append(f'{header:016x}')
        for candidate_index in range(8):
            word = 0
            if candidate_index < len(stats.candidates):
                d = stats.candidates[candidate_index]
                word = d.color | (d.area << 2) | (d.box[0] << 22) | (d.box[2] << 34) | (d.box[1] << 46) | (d.box[3] << 58)
            expected.append(f'{word:018x}')
        for group in mask.reshape(-1, 4):
            vectors.append(f'{sum(int(label) << (lane*2) for lane, label in enumerate(group)):02x}')
        details.append(dict(frame=frame_id, name=name, candidates=[dict(color=d.color, area=d.area, box=d.box) for d in stats.candidates],
                            diagnostic=stats.diagnostic, overflow=stats.overflow))
    # 队列容量是真实边界；超限时不可提供一个看似正常的部分区域。
    small = replace(CFG, component_queue_depth=2)
    limited = ComponentRAM(small)
    solid = np.zeros((small.height, small.width), np.uint8)
    solid[32:96, 32:128] = 1
    assert limited.scan(limited.capture(solid, 0, 0), solid).overflow
    # 非对齐ROI与最后不完整单元。
    partial = replace(CFG, height=126, roi=(3, 2, 157, 126), gate=(56, 2, 104, 126), max_size=384)
    edge = np.zeros((126, 160), np.uint8);edge[2:14, 3:15] = 3;edge[114:126, 145:157] = 1
    part = ComponentRAM(partial)
    stats = part.scan(part.capture(edge, 0, 0), edge)
    assert len(stats.candidates) == 2 and stats.candidates[-1].box[2:] == (156, 125)
    partial_cases = [edge]
    solid = np.zeros_like(edge);solid[2:126, 3:157] = 1
    partial_cases += [solid, np.zeros_like(edge)]
    four = np.zeros_like(edge);four[40, 40:44] = 2
    three = np.zeros_like(edge);three[40, 40:43] = 2
    partial_cases += [four, three]
    partial_headers, partial_candidates, partial_words = [], [], []
    for frame_id, mask in enumerate(partial_cases):
        for depth in (4096, 2):
            instance = ComponentRAM(replace(partial, component_queue_depth=depth))
            result = instance.scan(instance.capture(mask, frame_id, frame_id+32), mask)
            n, w, h, a, fill, rejection = result.diagnostic
            partial_headers.append(f'{n | (int(result.overflow)<<4) | (w<<5) | (h<<17) | (a<<29) | (fill<<49) | (rejection<<56):016x}')
            for index in range(8):
                word = 0
                if index < len(result.candidates):
                    d = result.candidates[index]
                    word = d.color | (d.area<<2) | (d.box[0]<<22) | (d.box[2]<<34) | (d.box[1]<<46) | (d.box[3]<<58)
                partial_candidates.append(f'{word:018x}')
        for group in mask.reshape(-1, 4):
            partial_words.append(f'{sum(int(value) << (lane*2) for lane,value in enumerate(group)):02x}')
    for suffix, lines in [('headers', partial_headers), ('candidates', partial_candidates), ('frames', partial_words)]:
        (ROOT / 'sim' / f'component_partial_{suffix}.hex').write_text('\n'.join(lines)+'\n', encoding='ascii')
    for suffix, lines in [('headers', headers), ('frames', vectors), ('candidates', expected)]:
        (ROOT / 'sim' / f'component_{suffix}.hex').write_text('\n'.join(lines)+'\n', encoding='ascii')
    (ROOT / 'reports' / 'component_model_cases.json').write_text(json.dumps(details, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'PASS component model: {len(selected)} scenes, independent OpenCV regions, queue overflow and partial ROI; {len(vectors)} RTL input words')


if __name__ == '__main__':
    main()
