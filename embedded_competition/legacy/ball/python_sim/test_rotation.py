"""无额外测试框架：像素真值仅进入渲染器，独立检查旋转测量结果。"""

from dataclasses import replace
import json
import math
from pathlib import Path
import time

import cv2
import numpy as np

from pipeline import Config
from rotation import RotationMeter, RotationPipeline, demo_phase, render_ball


CFG = Config(width=320,height=240,roi=(0,0,320,240),gate=(128,0,192,240),
             line=160,hysteresis=8,max_size=180)


def measure(rpm=30, frames=301, color=1, hidden=(), moving=False, angle=None, noise=0, light=1.0):
    engine = RotationPipeline(CFG)
    samples = []
    for index in range(frames):
        stamp = index/60
        phase = rpm*6*stamp if angle is None else angle
        center = (160+35*math.sin(index*0.07),130+14*math.sin(index*0.11)) if moving else (160,130)
        rgb = render_ball(320,240,center,52,phase,color,marker=index not in hidden,noise=noise,seed=index)
        if light != 1:
            rgb = np.clip(rgb.astype(float)*light,0,255).astype(np.uint8)
        observation = engine.step(rgb,stamp)
        samples.append((index,observation.angle,engine.meter.rpm,engine.meter.net,
                        engine.meter.partial,observation.reason,engine.meter.cw,engine.meter.ccw))
    return engine, samples


def test_three_colors_and_both_directions():
    results = []
    for color,rpm,frames,expected_cw,expected_ccw in ((1,30,301,2,0),(2,-45,181,0,2),(3,40,151,1,0)):
        engine,samples = measure(rpm,frames,color,noise=2)
        errors = [abs(s[2]-rpm) for s in samples[30:] if s[2] is not None]
        assert len(errors) >= frames-35, (color,len(errors))
        assert np.percentile(errors,95) < 2, (color,np.percentile(errors,95))
        expected = rpm*6*((frames-1)/60)
        assert abs(engine.meter.net-expected) < 3, (color,engine.meter.net,expected)
        assert (engine.meter.cw,engine.meter.ccw) == (expected_cw,expected_ccw)
        assert not engine.meter.partial
        results.append({'color':color,'rpm':rpm,'rpm_error_95':float(np.percentile(errors,95)),
                        'angle_error_deg':engine.meter.net-expected,'cw':engine.meter.cw,'ccw':engine.meter.ccw})
    return results


def test_translation_is_not_rotation():
    engine,samples = measure(0,181,moving=True,angle=41,noise=3)
    speeds = [abs(s[2]) for s in samples[30:] if s[2] is not None]
    assert len(speeds)>140 and np.percentile(speeds,95)<2, np.percentile(speeds,95)
    assert abs(engine.meter.net)<3 and engine.meter.cw == engine.meter.ccw == 0
    assert engine.ball_id == 1 and engine.meter.state == 'STOP'
    return {'rpm_abs_95':float(np.percentile(speeds,95)),'net_deg':engine.meter.net}


def test_short_and_long_occlusions():
    brief = range(100,103)
    engine,samples = measure(frames=265,hidden=brief)
    assert not engine.meter.partial and abs(engine.meter.net-792)<3
    for index in brief:
        assert samples[index][1] is None and samples[index][2] is None
        assert samples[index][3] == samples[99][3]
    hidden = range(100,125)
    engine,samples = measure(frames=301,hidden=hidden)
    assert engine.meter.partial and engine.ball_id == 1
    assert all(samples[index][3] == samples[99][3] for index in hidden)
    assert engine.meter.net < 900-40, engine.meter.net
    return {'short_gap_net_error_deg':samples[99][3]-297,
            'long_gap_partial':engine.meter.partial,'long_gap_observed_deg':engine.meter.net}


def test_unmarked_and_ambiguous():
    engine,samples = measure(frames=50,hidden=range(50))
    assert all(s[1] is None and s[2] is None for s in samples)
    assert engine.meter.net == 0 and engine.meter.cw == engine.meter.ccw == 0
    engine = RotationPipeline(CFG)
    for index in range(20):
        rgb = render_ball(320,240,(160,130),52,0)
        cv2.circle(rgb,(129,130),5,(11,12,13),-1)
        obs = engine.step(rgb,index/60)
        assert obs.marker_count == 2 and obs.angle is None, obs
    assert engine.meter.net == 0
    return {'unmarked_reports_no_rotation_measurement':True,'multiple_markers_rejected':True}


def test_dim_ball_and_noisy_mark():
    engine,samples = measure(30,151,noise=4,light=0.55)
    errors = [abs(s[2]-30) for s in samples[30:] if s[2] is not None]
    assert len(errors)>115 and np.percentile(errors,95)<2
    assert abs(engine.meter.net-450)<3 and not engine.meter.partial
    return {'rpm_error_95':float(np.percentile(errors,95))}


def test_phase_sampling_and_input_validation():
    meter = RotationMeter(max_rpm=120)
    meter.update(359,0)
    meter.update(1,1/60)
    assert abs(meter.net-2)<1e-9
    for index in range(2,30):
        meter.update((1+index*3)%360,index/60)
    frozen = meter.net
    meter.update(None,1.0)
    assert meter.net == frozen and meter.rpm is None and meter.partial
    meter.update(230,1.1)
    assert meter.net == frozen and meter.state == 'ACQUIRE'
    try:
        meter.update(1,1.1)
        raise AssertionError('重复时间戳未拒绝')
    except ValueError:
        pass
    engine = RotationPipeline(CFG)
    try:
        engine.step(np.zeros((20,20,3),np.uint8),0)
        raise AssertionError('错误图像未拒绝')
    except ValueError:
        pass
    for name,value in (('max_rpm',float('nan')),('max_rpm',0)):
        try:
            RotationMeter(**{name:value})
            raise AssertionError('非法参数未拒绝')
        except ValueError:
            pass
    return {'wrap_359_to_1_deg':2,'large_gap_rebases_without_count':True,'invalid_inputs_rejected':True}


def test_stop_and_reverse():
    engine = RotationPipeline(CFG)
    errors = []
    states = {}
    for index in range(721):
        stamp = index/60
        phase,rpm = demo_phase(stamp)
        rgb = render_ball(320,240,(160,130),52,phase,noise=2,seed=index)
        engine.step(rgb,stamp)
        if index in (210,390,660):
            states[index] = engine.meter.state
        if engine.meter.rpm is not None and min(abs(stamp-boundary) for boundary in (0,3,4.5,8,12))>0.5:
            errors.append(abs(engine.meter.rpm-rpm))
    assert states == {210:'STOP',390:'CCW',660:'CW'}, states
    assert abs(engine.meter.net-demo_phase(12)[0])<3 and not engine.meter.partial
    assert np.percentile(errors,95)<2, np.percentile(errors,95)
    assert engine.meter.cw >= 4 and engine.meter.ccw == 2
    return {'states':states,'rpm_error_95':float(np.percentile(errors,95)),
            'net_deg':engine.meter.net,'full_cw':engine.meter.cw,'full_ccw':engine.meter.ccw}


def test_irregular_timestamps_and_clear():
    meter = RotationMeter(max_rpm=120)
    stamp = 0.0
    meter.update(0,stamp)
    for dt in (0.13,0.11,0.14,0.12,0.10,0.13,0.15):
        stamp += dt
        meter.update((stamp*180)%360,stamp)
    assert meter.rpm is not None and abs(meter.rpm-30)<1e-9
    assert not meter.partial
    meter.reset()
    assert meter.net == 0 and meter.rpm is None and meter.cw == meter.ccw == 0 and not meter.partial
    return {'variable_interval_rpm':30,'clear_resets_reference_and_counts':True}


def main():
    start = time.perf_counter()
    checks = {}
    for name,fn in sorted(globals().copy().items()):
        if name.startswith('test_') and callable(fn):
            checks[name] = fn()
            print('PASS',name,checks[name],flush=True)
    result = {'passed':len(checks),'failed':0,'checks':checks,'elapsed_seconds':round(time.perf_counter()-start,3),
              'scope':'Known rendered RGB inputs through actual segmentation, component and marker algorithms; no RTL/board claims'}
    folder = Path(__file__).parent/'output/rotation_tests'
    folder.mkdir(parents=True,exist_ok=True)
    (folder/'test_report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False),flush=True)


if __name__ == '__main__':
    main()
