"""Reproducible integer/float comparisons, ROM roundtrip and RTL-oriented vectors."""
import csv
import json
import math
import sys
import time

import cv2
import numpy as np

from fixed_face import (BASE, C, ROOT, SCHEDULE, XML, detect, export_rom, float_model, floor_sqrt,
                        gray_roi, integral, load_rom, quantize, resize_gray, scalar_window)
sys.path.insert(0, str(BASE))
from face_pipeline import Demo
from scenes import demo_frame, draw_ball
from gate_demo import GateControl
from video_io import FourPixelInput


def check_capture(rgb):
    front = FourPixelInput(1280, 720)
    assert front.step(early=True) is None
    data = rgb.tobytes()
    accum = [0]*64
    gray = np.zeros((64, 64), np.uint8)
    valid = invalid = selected = written = sof_count = eol_count = eof_count = 0
    for offset in range(0, len(data), 12):
        if valid % 7 == 0:
            before = (front.x, front.y)
            assert front.step() is None and before == (front.x, front.y)
            invalid += 1
        word = data[offset:offset+12]
        _, x, y, sof, eol, eof = front.step(word)
        sof_count += sof
        eol_count += eol
        eof_count += eof
        valid += 1
        if 512 <= x < 768 and 232 <= y < 488:
            lane0 = int.from_bytes(word, 'big') >> 72
            assert lane0 == int(rgb[y, x, 0])*65536+int(rgb[y, x, 1])*256+int(rgb[y, x, 2])
            col, row = (x-512)//4, y-232
            weighted = sum(word[0::3])*77+sum(word[1::3])*150+sum(word[2::3])*29
            accum[col] = weighted if row % 4 == 0 else accum[col]+weighted
            if row % 4 == 3:
                gray[row//4, col] = (accum[col]+2048)//4096
                written += 1
            selected += 1
    assert not front.active and valid == 230400 and selected == 16384 and written == 4096
    assert (sof_count, eol_count, eof_count) == (1, 720, 1)
    assert np.array_equal(gray, gray_roi(rgb))
    return {'valid_rgb96_groups': valid, 'invalid_groups': invalid, 'roi_groups': selected,
            'gray_pixels': written, 'lane0_high_bits_verified': True, 'gray_array_equal': True}


def cases():
    original = cv2.imdecode(np.fromfile(BASE/'assets/astronaut.png', np.uint8), cv2.IMREAD_COLOR)
    crop = cv2.cvtColor(original[35:190, 145:295], cv2.COLOR_BGR2RGB)
    output = []
    variants = [('face_base', 180, 0, 0, 1.0, False), ('face_large', 220, 0, 0, 1.0, False),
                ('face_medium', 200, 0, 0, 1.0, False), ('face_left', 180, -20, 0, 1.0, False),
                ('face_right', 180, 20, 0, 1.0, False), ('face_up', 180, 0, -16, 1.0, False),
                ('face_dark', 180, 0, 0, 0.7, False), ('face_bright', 180, 0, 0, 1.3, False),
                ('face_color', 180, 0, 0, 1.0, True)]
    for name, size, dx, dy, brightness, color in variants:
        rgb = demo_frame('count', 0)
        tile = cv2.resize(crop, (size, size))
        if not color:
            tile = cv2.cvtColor(cv2.cvtColor(tile, cv2.COLOR_RGB2GRAY), cv2.COLOR_GRAY2RGB)
        tile = np.clip(tile.astype(float)*brightness, 0, 255).astype(np.uint8)
        x, y = 640-size//2+dx, 360-size//2+dy
        rgb[y:y+size, x:x+size] = tile
        output.append((name, True, rgb))
    output.append(('background', False, demo_frame('count', 0)))
    for color, name in ((1, 'red_ball'), (2, 'yellow_ball'), (3, 'green_ball')):
        rgb = demo_frame('count', 0)
        draw_ball(rgb, 640, 360, color, 60)
        output.append((name, False, rgb))
    rng = np.random.default_rng(20261019)
    for name, patch in (('noise', rng.integers(0, 256, (256, 256), dtype=np.uint8)),
                        ('checkerboard', ((np.indices((256, 256)).sum(0)//16 % 2)*220).astype(np.uint8)),
                        ('uniform', np.full((256, 256), 160, np.uint8))):
        rgb = demo_frame('count', 0)
        rgb[232:488, 512:768] = patch[..., None]
        output.append((name, False, rgb))
    outside = demo_frame('count', 0)
    outside[180:360, 1000:1180] = Demo().tile
    output.append(('face_outside_guide', False, outside))
    return output


def compare_traces(fixed, floating):
    common = mismatch = 0
    for a, b in zip(fixed['levels'], floating['levels']):
        reference = {wi: (ids, branch) for _, wi, ids, branch in b['trace']}
        for _, wi, ids, branch in a['trace']:
            if wi in reference:
                other_ids, other_branch = reference[wi]
                _, ia, ib = np.intersect1d(ids, other_ids, assume_unique=True, return_indices=True)
                common += len(ia)
                mismatch += int(np.count_nonzero(branch[ia] != other_branch[ib]))
    return common, mismatch


def main():
    start = time.perf_counter()
    folder = ROOT/'reports'
    folder.mkdir(exist_ok=True)
    manifest = export_rom()
    model, floating = load_rom(), float_model()
    assert np.array_equal(model['rects'], floating['rects'])
    assert np.array_equal(model['modes'], floating['modes'])
    assert np.array_equal(model['nodes'], quantize(floating['nodes'], 14, 16))
    assert np.array_equal(model['leaves'], quantize(floating['leaves'], 12, 18))
    assert np.array_equal(model['stages'], quantize(floating['stages'], 12, 18))
    assert int(np.max(model['counts']))*int(np.max(np.abs(model['leaves']))) < 1 << 25
    assert np.array_equal(quantize([0.5/4096, -0.5/4096], 12, 18), [1, -1])
    try:
        quantize([32], 12, 18)
    except ValueError:
        pass
    else:
        raise AssertionError('Quantization overflow was silently accepted')
    rng = np.random.default_rng(103520)
    for value in [0, 1, (1 << 34)-1, 484*484*100, *map(int, rng.integers(0, 1 << 34, 1000))]:
        assert floor_sqrt(value) == math.isqrt(value)
    from fixed_face import group_boxes
    assert not group_boxes([(0, 0, 24, 24)]*5)[0]
    assert group_boxes([(0, 0, 24, 24)]*6)[0] == ((0, 0, 24, 24, 6),)
    assert group_boxes([(i*3, 0, 24, 24) for i in range(6)])[0] == ((8, 0, 24, 24, 6),)
    assert group_boxes([(0, 0, 24, 24)]*129)[:2] == ((), True)
    gate = GateControl()
    assert gate.result(1, 0, True) and gate.hits == 1
    assert not gate.result(1, 0, True) and gate.hits == 1
    assert not gate.result(2, 1, True) and gate.hits == 1
    assert gate.result(2, 0, False) and gate.hits == 0
    for sample in (3, 4, 5):
        assert gate.result(sample, 0, True)
    assert not gate.unlocked and gate.pending
    assert gate.frame_start() and gate.unlocked
    gate.reset()
    assert not gate.unlocked and not gate.result(6, 0, True)
    assert gate.result(6, 1, True, fault=True) and gate.hits == 0
    print('PASS ROM, rounding/overflow, sqrt, grouping and gate freshness', flush=True)
    cascade = cv2.CascadeClassifier(str(XML))
    rows, original_case = [], None
    vectors = folder/'vectors'
    vectors.mkdir(exist_ok=True)
    scalar_checks = 0
    for name, expected, rgb in cases():
        q = detect(rgb, model, keep_trace=True)
        f = detect(rgb, floating, floating=True, keep_trace=True)
        common, mismatch = compare_traces(q, f)
        cvgray = cv2.resize(cv2.cvtColor(rgb[232:488, 512:768], cv2.COLOR_RGB2GRAY), (64, 64),
                            interpolation=cv2.INTER_AREA)
        original_cv = cascade.detectMultiScale(cvgray, 1.1, 5, minSize=(24, 24))
        fixed_gray_cv = cascade.detectMultiScale(q['gray'], 1.1, 5, minSize=(24, 24))
        gray_error = int(np.abs(q['gray'].astype(int)-cvgray.astype(int)).max())
        resize_error = max(int(np.abs(resize_gray(q['gray'], size).astype(int)-
                                     cv2.resize(q['gray'], (size, size), interpolation=cv2.INTER_LINEAR).astype(int)).max())
                           for size in C['pyramid_sizes'])
        stage_diff = sum(int(np.count_nonzero(a['rejected'] != b['rejected'])) for a, b in zip(q['levels'], f['levels']))
        raw_diff = len(set(b for level in q['levels'] for b in level['raw']) ^
                       set(b for level in f['levels'] for b in level['raw']))
        row = {'case': name, 'expected_face': expected, 'fixed_boxes': q['boxes'], 'float_boxes': f['boxes'],
               'opencv_original_gray_boxes': original_cv.tolist() if len(original_cv) else [],
               'opencv_fixed_gray_boxes': fixed_gray_cv.tolist() if len(fixed_gray_cv) else [],
               'raw_fixed': q['raw_count'], 'raw_float': f['raw_count'], 'raw_unique_box_symmetric_difference': raw_diff,
               'weak_decisions_compared': common, 'weak_decision_mismatch': mismatch,
               'reject_stage_window_mismatch': stage_diff, 'overflow': q['fault'],
               'gray_max_abs_error_vs_opencv': gray_error, 'resize_max_abs_error_vs_opencv': resize_error,
               'cycles': q['cycles'], 'estimated_ms_at_reference_clock': q['cycles']/103520,
               'cycle_breakdown': q['cycle_breakdown']}
        rows.append(row)
        print(json.dumps({k: row[k] for k in ('case', 'fixed_boxes', 'float_boxes', 'weak_decision_mismatch', 'cycles')}), flush=True)
        if name == 'face_base':
            original_case = rgb
            capture_report = check_capture(rgb)
            (folder/'capture_verification.json').write_text(json.dumps(capture_report, indent=2), encoding='utf-8')
            for by, bx in ((0, 0), (63, 63), (17, 32), (32, 17), (31, 31)):
                weighted = 0
                for sy in range(232+by*4, 236+by*4):
                    for sx in range(512+bx*4, 516+bx*4):
                        red, green, blue = map(int, rgb[sy, sx])
                        weighted += 77*red+150*green+29*blue
                assert int(q['gray'][by, bx]) == (weighted+2048)//4096
            for size in C['pyramid_sizes']:
                resized = resize_gray(q['gray'], size)
                for py, px in ((0, 0), (size-1, size-1), (size//2, size//3)):
                    xc = max(0, min(63*256, ((2*px+1)*64*128)//size-128))
                    yc = max(0, min(63*256, ((2*py+1)*64*128)//size-128))
                    x0, fx = divmod(xc, 256)
                    y0, fy = divmod(yc, 256)
                    upper = int(q['gray'][y0, x0])*(256-fx)+int(q['gray'][y0, min(63, x0+1)])*fx
                    lower = int(q['gray'][min(63, y0+1), x0])*(256-fx)+int(q['gray'][min(63, y0+1), min(63, x0+1)])*fx
                    assert int(resized[py, px]) == (upper*(256-fy)+lower*fy+32768)//65536
            # Check independent scalar arithmetic and branch traces, including a complete positive window.
            level = q['levels'][0]
            ids = [0, len(level['x'])//2, len(level['x'])-1]
            positive = np.flatnonzero(level['rejected'] == 25)
            if len(positive):
                ids.append(int(positive[0]))
            for index in ids:
                reject, cycles, trace = scalar_window(q['gray'], model, int(level['x'][index]), int(level['y'][index]))
                assert reject == int(level['rejected'][index])
                expected_cycles = 484*3+4*2+6+17
                for _, wi, active, branch in level['trace']:
                    loc = np.searchsorted(active, index)
                    if loc < len(active) and active[loc] == index:
                        expected_cycles += 3+(3 if model['modes'][wi] == 2 else 2)*12+6
                reached = 0 if reject == -1 else (25 if reject == 25 else reject+1)
                expected_cycles += reached*4+(2 if reject == 25 else 0)
                assert expected_cycles == cycles
                for si, wi, feature, d, root, threshold, right, leaf, acc, elapsed in trace:
                    candidate = next(t for t in level['trace'] if t[1] == wi)
                    loc = np.searchsorted(candidate[2], index)
                    assert not bool(right) == bool(candidate[3][loc])
                    assert root == floor_sqrt(d)
                with (vectors/f'window_{index}_trace.csv').open('w', newline='', encoding='utf-8') as stream:
                    log = csv.writer(stream)
                    log.writerow(('stage', 'weak', 'feature', 'variance', 'sqrt', 'threshold_q14', 'take_right',
                                  'leaf_q12', 'stage_sum_q12', 'window_cycles'))
                    log.writerows(trace)
                scalar_checks += 1
            sat = integral(q['gray'])
            (vectors/'gray.mem').write_text(''.join(f'{int(v):02x}\n' for v in q['gray'].flat), encoding='ascii')
            (vectors/'integral.mem').write_text(''.join(f'{int(v):05x}\n' for v in sat[1:, 1:].flat), encoding='ascii')
            painted = rgb.copy()
            cv2.rectangle(painted, (512, 232), (767, 487), (0, 235, 255), 1)
            for left, top, right, bottom in q['boxes']:
                cv2.rectangle(painted, (left, top), (right, bottom), (50, 255, 100), 2)
            cv2.imencode('.png', cv2.cvtColor(painted, cv2.COLOR_RGB2BGR))[1].tofile(str(folder/'fixed_detection_preview.png'))
    assert original_case is not None
    total_windows = sum((size-23)**2 for size in C['pyramid_sizes'])
    rectangle_counts = np.where(model['modes'] == 2, 3, 2)
    worst_weak = int(np.sum(3+rectangle_counts*12+6))*total_windows
    worst_base = sum((0 if size == 64 else size*size*14)+size*size*4+
                     (size-23)**2*(484*3+4*2+6+17+25*4+2) for size in C['pyramid_sizes'])
    grouping_upper = (128*127//2)*(8+4*127+1)+128*(2*127+5)+128*(4*20)+128*127*8+64
    report = {'cases': len(rows), 'same_public_photo_augmented_positive_cases': sum(r['expected_face'] for r in rows),
              'fixed_float_presence_disagreement': sum(bool(r['fixed_boxes']) != bool(r['float_boxes']) for r in rows),
              'fixed_positive_misses': [r['case'] for r in rows if r['expected_face'] and not r['fixed_boxes']],
              'fixed_negative_false_positives': [r['case'] for r in rows if not r['expected_face'] and r['fixed_boxes']],
              'weak_decisions_compared': sum(r['weak_decisions_compared'] for r in rows),
              'weak_decision_mismatch': sum(r['weak_decision_mismatch'] for r in rows),
              'scalar_window_replays': scalar_checks, 'parameter_quantization': manifest,
              'maximum_observed_cycles': max(r['cycles'] for r in rows),
              'worst_case_cycle_upper_bound': worst_base+worst_weak+grouping_upper,
              'worst_case_ms_reference_only': (worst_base+worst_weak+grouping_upper)/103520,
              'clock_hz_reference_only': C['clock_hz_reference_only'], 'cycle_schedule_is_assumption': True,
              'scope': 'One public face photo with controlled transformations; synthetic negatives. No general face accuracy, RTL or board claim.',
              'elapsed_seconds': time.perf_counter()-start, 'results': rows}
    (folder/'numeric_verification.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    assert report['fixed_float_presence_disagreement'] == 0, 'Quantization changed face/no-face output; see report'
    assert not report['fixed_positive_misses'] and not report['fixed_negative_false_positives'], 'Controlled-scene detection failure; see report'
    assert all(not r['overflow'] and r['gray_max_abs_error_vs_opencv'] <= 2 and
               r['resize_max_abs_error_vs_opencv'] <= 2 for r in rows)
    print(json.dumps({k: v for k, v in report.items() if k not in ('results', 'parameter_quantization')}), flush=True)


if __name__ == '__main__':
    main()
