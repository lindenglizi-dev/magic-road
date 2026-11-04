"""Verify the startup gate with real Haar photo pixels and the original ball model."""
import json
import time

import numpy as np

from face_pipeline import BallFacePipeline, Demo, ROOT, demo_frame, draw_ball


def main():
    start = time.perf_counter()
    tile = Demo().tile
    checks = []
    engine = BallFacePipeline()
    calls = {'ball': 0, 'face': 0}
    analyse, detect = engine.ball.analyse, engine.detector.detect

    def ball_probe(rgb):
        calls['ball'] += 1
        return analyse(rgb)

    def face_probe(rgb, frame_id):
        calls['face'] += 1
        return detect(rgb, frame_id)

    engine.ball.analyse, engine.detector.detect = ball_probe, face_probe

    def feed(face=False, x=None, color=1, repeat=1):
        result = None
        for _ in range(repeat):
            rgb = demo_frame('count', 0)
            if face:
                rgb[180:360, 1000:1180] = tile
            if x is not None:
                draw_ball(rgb, x, 410, color)
            result = engine.process(rgb)
            assert result[4] == 172800
        return result

    for x in (580, 580, 700, 700):
        result = feed(x=x)
        assert result[1] is None and result[2] is None
    assert not engine.unlocked and calls['ball'] == 0
    assert not any(engine.ball.counter.counts.values())
    checks.append('pre_unlock_crossing_has_no_ball_analysis_or_count')
    feed(face=True)  # frame 4: positive 1
    assert engine.face_hits == 1 and not engine.unlocked
    feed(face=True)  # frame 5: cached result must not count twice
    assert engine.face_hits == 1
    feed()  # frame 6: an actual negative resets the consecutive count
    assert engine.face_hits == 0
    feed(face=True)  # frame 7: skipped
    assert engine.face_hits == 0
    checks.append('actual_evaluations_only_and_negative_resets_confirmation')
    for index in range(8, 13):
        result = feed(face=True, x=580)
        assert engine.unlocked == (index == 12)
        assert result[1] is None
    assert engine.unlock_frame == 12 and calls['ball'] == 0
    assert engine.ball.counter.state == 'WAIT_CLEAR'
    face_calls = calls['face']
    checks.append('three_real_haar_confirmations_unlock_on_third_result')
    feed(x=580, repeat=3)
    feed(x=700, repeat=3)
    assert engine.ball.counter.state == 'WAIT_CLEAR'
    assert not any(engine.ball.counter.counts.values())
    feed(repeat=2)
    assert engine.ball.counter.state == 'WAIT_CLEAR'
    feed()
    assert engine.ball.counter.state == 'READY'
    checks.append('ball_already_in_gate_requires_three_empty_frames')
    for color in (1, 1, 3, 2):
        feed(x=580, color=color, repeat=2)
        feed(x=700, color=color, repeat=4)
        feed(repeat=3)
    assert engine.ball.counter.counts == {1: 2, 2: 1, 3: 1}
    assert calls['face'] == face_calls and engine.unlocked
    checks.extend(('face_leaves_and_haar_calls_stop_after_unlock', 'same_color_repeat_and_stationary_ball_count_once'))
    engine.configure(mode='track')
    feed(x=580, repeat=3)
    assert engine.unlocked and engine.ball.snapshot.target is not None
    engine.configure(clear=True)
    assert engine.unlocked and not any(engine.ball.counter.counts.values())
    engine.configure(strict=True)
    assert engine.unlocked
    checks.append('mode_threshold_and_count_clear_preserve_unlock')
    engine.reset()
    assert not engine.unlocked and engine.face_hits == 0 and engine.faces is None
    result = feed(x=700)
    assert result[1] is None and result[3] is None and not np.any(result[0])
    assert not any(engine.ball.counter.counts.values())
    assert calls['face'] > face_calls
    checks.append('reset_relocks_clears_counts_and_flushes_old_ddr_output')
    engine.configure(mode='count')
    assert not engine.unlocked
    for _ in range(8):
        feed(face=True)
        if engine.unlocked:
            break
    assert engine.unlocked
    feed(repeat=3)
    assert engine.ball.counter.state == 'READY'
    checks.append('second_face_confirmation_can_unlock_after_reset')
    result = feed(x=580)
    assert result[3][3] is True and result[3][4] == 3
    assert result[3][0] == engine.frame_id-1
    assert result[3][1].frame_id == engine.frame_id-2
    checks.append('display_gate_state_and_ball_result_follow_ddr_frame_metadata')
    report = {'passed': len(checks), 'failed': 0, 'checks': checks,
              'actual_haar_calls': calls['face'], 'ball_analysis_calls': calls['ball'],
              'first_unlock_frame': 12, 'elapsed_seconds': round(time.perf_counter()-start, 3),
              'scope': 'Python functional gate with actual Haar model; no FPGA resource or board validation'}
    (ROOT/'gate_verification.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report), flush=True)


if __name__ == '__main__':
    main()
