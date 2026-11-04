"""无额外测试框架：检查整数数据通路、真实RGB检测与帧事件保护。"""

from dataclasses import replace
import json
import math
from pathlib import Path
import time

import cv2
import numpy as np

from pipeline import Config, Detection
from rotation import render_ball
from rotation_rtl_model import (Bank, CLOCK_HZ, FixedMeter, Measurement,
                                RotationHardwareModel, TURN, cordic_phase,
                                divide_round, extract_marker)


CFG = Config(width=320, height=288, roi=(0, 0, 320, 288),
             gate=(128, 0, 192, 288), line=160, hysteresis=8)


def sequence(rpm=30, frames=181, color=1, moving=False, hidden=(), light=1.0, noise=2):
    model = RotationHardwareModel(CFG)
    results, truths = [], {}
    for index in range(frames):
        stamp = index/60
        phase = rpm*6*stamp
        center = (160+25*math.sin(index*.08), 150+8*math.sin(index*.11)) if moving else (160, 150)
        rgb = render_ball(320, 288, center, 60, phase, color=color,
                          marker=index not in hidden, noise=noise, seed=index)
        if light != 1:
            rgb = np.clip(rgb.astype(float)*light, 0, 255).astype(np.uint8)
        model.step(rgb, stamp)
        results.extend(model.new_results)
        truths[index] = phase
    results.extend(model.flush())
    return model, results, truths


def test_integer_divider_and_cordic():
    for n in (-2**63+1, -123456789, -5, -1, 0, 1, 5, 123456789, 2**63-1):
        for d in (1, 2, 3, 17, 2**32-1):
            q, r = divmod(abs(n), d)
            expected = (q+int(2*r >= d))*(-1 if n < 0 else 1)
            assert divide_round(n, d) == expected
    errors = []
    for angle in range(360):
        rad = math.radians(angle)
        x, y = round(1200*math.cos(rad)), round(1200*math.sin(rad))
        actual = cordic_phase(x, y)*360/TURN
        errors.append(abs((actual-angle+180) % 360-180))
    assert max(errors) < .06, max(errors)
    for x, y, expected in ((1200, 0, 0), (0, 1200, 16384), (-1200, 0, 32768), (0, -1200, 49152)):
        assert abs(((cordic_phase(x, y)-expected+32768) & 65535)-32768) <= 2
    try:
        cordic_phase(0, 0)
        raise AssertionError('零向量未被拒绝')
    except ValueError:
        pass
    return {'max_cordic_error_deg': max(errors), 'divider_cases': 55}


def test_integer_phase_window_and_missing_samples():
    meter = FixedMeter()
    stamp = 0
    for dt in (0, .13, .11, .14, .12, .10, .13, .15):
        stamp += dt
        meter.update(round(stamp*30*6/360*TURN) & 65535, round(stamp*CLOCK_HZ))
    assert abs(meter.rpm_x10-300) <= 1 and not meter.partial
    meter.update(None, round((stamp+.03)*CLOCK_HZ))
    assert meter.rpm_x10 is None
    previous = meter.net_phase
    meter.update(None, round((stamp+.4)*CLOCK_HZ))
    assert meter.partial and meter.net_phase == previous
    meter.update(0, round((stamp+.42)*CLOCK_HZ))
    assert meter.net_phase == previous and meter.rpm_x10 is None
    try:
        meter.update(0, round((stamp+.42)*CLOCK_HZ))
        raise AssertionError('重复时间未被拒绝')
    except ValueError:
        pass
    fast = FixedMeter()
    fast.update(0, 0)
    fast.update(TURN//2, round(CLOCK_HZ/60))
    assert fast.partial and fast.net_phase == 0
    return {'irregular_rpm_x10': 300, 'long_gap_freezes': True, 'half_turn_rejected': True}


def test_three_colors_and_rotation_directions():
    report = []
    for color, rpm in ((1, 30), (2, -45), (3, 40)):
        model, results, truths = sequence(rpm=rpm, color=color)
        valid = [r for r in results if r.angle is not None]
        errors = [abs(r.rpm_x10/10-rpm) for r in results[35:] if r.rpm_x10 is not None]
        angles = [abs((r.angle*360/TURN-truths[r.frame_id]+180) % 360-180) for r in valid]
        assert len(valid) >= len(results)-4
        assert len(errors) > 135 and np.percentile(errors, 95) < 2, (color, np.percentile(errors, 95))
        expected = (truths[valid[-1].frame_id]-truths[valid[0].frame_id])/360
        assert abs(model.meter.net_phase/TURN-expected) < .015
        assert not model.meter.partial
        assert [r.frame_id for r in results] == list(range(len(results)))
        assert all(r.done_tick >= r.tick for r in results)
        report.append({'color': color, 'rpm': rpm, 'valid': len(valid),
                       'rpm_p95_error': float(np.percentile(errors, 95)),
                       'angle_p95_error_deg': float(np.percentile(angles, 95))})
    return report


def test_translation_not_spin():
    model, results, _ = sequence(rpm=0, moving=True)
    speeds = [abs(r.rpm_x10/10) for r in results[35:] if r.rpm_x10 is not None]
    assert len(speeds) > 130 and np.percentile(speeds, 95) < 2, np.percentile(speeds, 95)
    assert abs(model.meter.net_phase/TURN) < .02 and model.meter.cw == model.meter.ccw == 0
    return {'rpm_abs_p95': float(np.percentile(speeds, 95)), 'net_rev': model.meter.net_phase/TURN}


def test_short_long_gap_and_unmarked_ball():
    short, rows, _ = sequence(hidden=range(70, 73))
    by_id = {r.frame_id: r for r in rows}
    assert all(by_id[i].angle is None and by_id[i].rpm_x10 is None for i in range(70, 73))
    assert not short.meter.partial
    long, rows, _ = sequence(hidden=range(70, 95))
    assert long.meter.partial
    assert all(r.rpm_x10 is None for r in rows if 70 <= r.frame_id < 95)
    blank, rows, _ = sequence(frames=35, hidden=range(35))
    assert all(r.angle is None and r.rpm_x10 is None for r in rows)
    assert blank.meter.net_phase == 0
    return {'short_gap_continuous': True, 'long_gap_partial': True, 'unmarked_not_zero_rpm': True}


def test_same_frame_threshold_and_multiple_markers():
    model = RotationHardwareModel(CFG)
    rows = []
    for index in range(100):
        rgb = render_ball(320, 288, (160, 150), 60, index*3, noise=2, seed=index)
        rgb = np.clip(rgb.astype(float)*(.6 if index < 50 else 1.0), 0, 255).astype(np.uint8)
        model.step(rgb, index/60)
        rows.extend(model.new_results)
    rows.extend(model.flush())
    assert all(r.angle is not None for r in rows[3:]), [(r.frame_id, r.reason) for r in rows if r.angle is None]
    low = np.median([r.median for r in rows[10:40]])
    high = np.median([r.median for r in rows[60:90]])
    assert high > 1.4*low
    ambiguous = RotationHardwareModel(CFG)
    records = []
    for index in range(12):
        rgb = render_ball(320, 288, (160, 150), 60, 0)
        cv2.circle(rgb, (124, 150), 6, (11, 12, 13), -1)
        ambiguous.step(rgb, index/60)
        records.extend(ambiguous.new_results)
    records.extend(ambiguous.flush())
    assert all(r.reason == 'MULTIPLE MARKERS' for r in records[2:])
    return {'dim_median': float(low), 'bright_median': float(high), 'ambiguous_rejected': True}


def test_bank_ownership_overrun_and_clear():
    model = RotationHardwareModel(CFG, marker_cycles=5_500_000)
    rows = []
    for index in range(35):
        model.step(render_ball(320, 288, (160, 150), 60, index*3), index/60)
        rows.extend(model.new_results)
    rows.extend(model.flush())
    assert model.counters['BANK OVERRUN'] > 0
    assert [r.frame_id for r in rows] == list(range(35))
    assert all(not b.busy for b in model.banks)
    assert any(r.angle is not None for r in rows)
    normal = RotationHardwareModel(CFG)
    for index in range(8):
        normal.step(render_ball(320, 288, (160, 150), 60, index*3), index/60)
    old_epoch = normal.epoch
    normal.clear()
    assert not normal.events and all(not b.busy for b in normal.banks)
    fresh = []
    for index in range(8, 20):
        normal.step(render_ball(320, 288, (160, 150), 60, index*3), index/60)
        fresh.extend(normal.new_results)
    fresh.extend(normal.flush())
    assert fresh and all(r.epoch == old_epoch+1 for r in fresh)
    return {'overrun_rejections': model.counters['BANK OVERRUN'], 'ordered_publication': True, 'clear_discards_old_epoch': True}


def test_window_miss_tags_and_queue_limit():
    cfg = replace(CFG, width=640, roi=(0, 0, 640, 288))
    model, rows = RotationHardwareModel(cfg), []
    for index in range(11):
        x = 160 if index < 6 else 160+64*(index-5)
        model.step(render_ball(640, 288, (x, 150), 60, index*3), index/60)
        rows.extend(model.new_results)
    rows.extend(model.flush())
    assert any(r.reason == 'WINDOW MISS' for r in rows), [(r.frame_id, r.reason) for r in rows]
    bank = Bank(busy=True, frame_id=3, epoch=1, tick=100, origin=(32, 22))
    ball = Detection((100, 90, 219, 209), 1, 10000)
    mismatch = extract_marker(bank, ball, Measurement(4, 1, 100), CFG)
    assert mismatch.angle is None and mismatch.reason == 'FRAME TAG MISMATCH'
    bank.gray[:] = 120
    bank.gray[55:70, 75:90] = 10
    result = extract_marker(bank, ball, Measurement(3, 1, 100), CFG, queue_capacity=2)
    assert result.reason == 'MARKER QUEUE OVERFLOW' and result.angle is None, result.reason
    return {'window_miss_rejected': True, 'frame_mismatch_rejected': True, 'bounded_queue_rejected': True}


def test_stop_reversal_and_full_turns_numeric():
    meter = FixedMeter()
    from rotation import demo_phase
    states = {}
    for index in range(721):
        stamp = index/60
        phase, _ = demo_phase(stamp)
        meter.update(round(phase/360*TURN) & 65535, round(stamp*CLOCK_HZ))
        if index in (210, 390, 660):
            states[index] = meter.state
    assert states == {210: 'STOP', 390: 'CCW', 660: 'CW'}
    assert abs(meter.net_phase*360/TURN-demo_phase(12)[0]) < .01
    assert (meter.cw, meter.ccw) == (5, 2)
    return {'states': states, 'full_cw': meter.cw, 'full_ccw': meter.ccw, 'net_rev': meter.net_phase/TURN}


def test_register_saturation_gray_storage_and_input_boundary():
    meter = FixedMeter()
    meter.cw = 0xffffffff
    for index in range(121):
        meter.update(round(index/120*TURN) & 65535, round(index/60*CLOCK_HZ))
    assert meter.cw == 0xffffffff and meter.counter_saturated and meter.partial
    model = RotationHardwareModel(CFG)
    assert sum(bank.gray.nbytes for bank in model.banks) == 32768
    model.window = (32, 22, 0)
    rgb = render_ball(320, 288, (160, 150), 60, 15)
    model.step(rgb, 0)
    patch = rgb[22:278, 32:288].astype(np.uint16)
    gray = (patch[..., 0]+2*patch[..., 1]+patch[..., 2]) >> 2
    expected = ((gray[0::2, 0::2]+gray[0::2, 1::2]+gray[1::2, 0::2]+gray[1::2, 1::2]+2) >> 2).astype(np.uint8)
    assert np.array_equal(model.banks[0].gray, expected)
    for bad_stamp in (0, -1, math.nan):
        try:
            model.step(rgb, bad_stamp)
            raise AssertionError('非法时间未被拒绝')
        except ValueError:
            pass
    try:
        model.step(rgb.astype(np.float32), 1)
        raise AssertionError('非法RGB类型未被拒绝')
    except ValueError:
        pass
    return {'gray_bank_bytes': 32768, 'parallel_gray_average_exact': True, 'counter_saturates': True}


def main():
    started = time.perf_counter()
    report = {}
    for name, fn in sorted(globals().copy().items()):
        if name.startswith('test_') and callable(fn):
            report[name] = fn()
            print('PASS', name, json.dumps(report[name], ensure_ascii=False), flush=True)
    result = {'passed': len(report), 'failed': 0, 'checks': report,
              'elapsed_seconds': round(time.perf_counter()-started, 3),
              'scope': 'integer and frame-event Python model; not RTL simulation or board evidence'}
    folder = Path(__file__).parent/'output/rotation_rtl_tests'
    folder.mkdir(parents=True, exist_ok=True)
    (folder/'test_report.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
