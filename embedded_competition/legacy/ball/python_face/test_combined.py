"""Actual Haar detection, ball regression, and shared display-frame checks."""
import json
import math
import time

import cv2
import numpy as np

from face_pipeline import BallFacePipeline, Demo, FaceDetector, Pipeline, ROOT
import test_simulation as original_tests


def iou(a, b):
    overlap = max(0, min(a[2], b[2])-max(a[0], b[0])+1) * max(0, min(a[3], b[3])-max(a[1], b[1])+1)
    area = lambda r: (r[2]-r[0]+1)*(r[3]-r[1]+1)
    return overlap / (area(a)+area(b)-overlap)


def main():
    start = time.perf_counter()
    checks = []
    for name, check in sorted(vars(original_tests).items()):
        if name.startswith('test_') and callable(check):
            check()
            checks.append('original.'+name)
    print(f'PASS original ball checks: {len(checks)}', flush=True)
    demo, detector = Demo(), FaceDetector()
    for index in (0, 20, 40, 60, 80, 120, 160, 200):
        boxes = detector.detect(demo.frame('count', index), index).boxes
        x = 1000+round(55*math.sin(index*0.055))
        truth = (x+38, 216, x+151, 325)
        assert boxes and max(iou(box, truth) for box in boxes) > 0.65, (index, boxes)
    assert not detector.detect(demo.frame('count', 100), 100).boxes
    assert not detector.detect(np.zeros((720, 1280, 3), np.uint8), 0).boxes
    checks.append('real_haar_positive_negative_translation_and_coordinate_mapping')
    print('PASS actual Haar face sample and negative frames', flush=True)
    engine, baseline = BallFacePipeline(face_gate=False), Pipeline()
    previous_ball = previous_faces = None
    prior_source = -1
    shown_faces = 0
    for index in range(360):
        rgb = demo.frame('count', index)
        reference = baseline.analyse(rgb)
        baseline.accept(reference)
        hdmi, stats, snapshot, shown, words = engine.process(rgb)
        assert snapshot == baseline.snapshot, index
        assert stats.candidates == reference.candidates and np.array_equal(stats.mask, reference.mask)
        assert words == 172800
        if index == 0:
            assert shown is None and not np.any(hdmi)
        else:
            assert shown[0] == index-1
            assert shown[1] == previous_ball and shown[2] == previous_faces
            assert shown[0] > prior_source
            prior_source = shown[0]
            if shown[2] is not None:
                assert 1 <= shown[0]-shown[2].frame_id <= 2
                if shown[2].boxes:
                    shown_faces += 1
                    x, y, _, _ = shown[2].boxes[0]
                    assert tuple(hdmi[y, x]) == (0, 235, 255), (index, x, y)
        if index % 120 >= 96:
            assert not engine.faces.boxes, index
        previous_ball = None if index == 0 else saved_ball
        previous_faces = None if index == 0 else saved_faces
        saved_ball, saved_faces = snapshot, engine.faces
        if index == 159:
            cv2.imencode('.png', cv2.cvtColor(hdmi, cv2.COLOR_RGB2BGR))[1].tofile(str(ROOT/'verification_preview.png'))
        if index % 120 == 119:
            print(f'PASS combined frames {index+1}/360, counts={snapshot.counts}', flush=True)
    assert engine.ball.snapshot.counts == (2, 2, 2)
    assert shown_faces > 200, shown_faces
    checks.extend(('combined_360_frames_ball_exact_regression', 'six_balls_counted_once_with_stop_and_dropout',
                   'face_boxes_share_osd_and_ddr_metadata', 'negative_face_clears_and_cache_age_bounded'))
    tracked = BallFacePipeline(mode='track', face_gate=False)
    tracked_base = Pipeline(mode='track')
    for index in range(90):
        rgb = demo.frame('track', index)
        stats = tracked_base.analyse(rgb)
        tracked_base.accept(stats)
        result = tracked.process(rgb)
        assert result[2] == tracked_base.snapshot
    checks.append('track_mode_90_frames_exact_regression')
    tracked.configure(mode='count', clear=True)
    assert tracked.faces is None and tracked.ball.snapshot is None
    result = tracked.process(demo.frame('count', 0))
    # DDR can still output the prior epoch; metadata must retain that old epoch.
    assert result[3][1].epoch == 0 and result[2].epoch == 1
    checks.append('mode_switch_clear_and_epoch_metadata')
    color_input = Demo(color=True).frame('count', 40)
    color_stats = Pipeline().analyse(color_input)
    skin_candidates = [list(c.box) for c in color_stats.candidates if c.box[0] > 1000]
    assert detector.detect(color_input, 0).boxes
    checks.append('real_color_photo_face_detected')
    report = {'passed': len(checks), 'failed': 0, 'checks': checks,
              'combined_count_frames': 360, 'track_frames': 90,
              'final_red_green_yellow': engine.ball.snapshot.counts,
              'face_visible_hdmi_frames': shown_faces,
              'known_skin_color_ball_candidates': skin_candidates,
              'elapsed_seconds': round(time.perf_counter()-start, 3),
              'scope': 'Python functional prototype only. No RTL resource or board evidence.'}
    (ROOT/'verification.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report), flush=True)


if __name__ == '__main__':
    main()
