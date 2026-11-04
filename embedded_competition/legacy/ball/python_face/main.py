"""Run both ball and face detection on the same demo, camera, or video frames."""
import argparse
import csv
import json
from pathlib import Path
import time

import cv2
import numpy as np

from face_pipeline import BallFacePipeline, Demo, ROOT


def run(args):
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    engine = BallFacePipeline(args.mode, args.face_every, args.face_width, args.min_face_size,
                              face_gate=not args.simultaneous)
    demo = Demo(color=args.demo_color_face, face_gate=not args.simultaneous) if args.source == 'demo' else None
    capture = None
    writer = None
    trace = None
    frames, face_times, events = 0, [], []
    face_positive = face_evaluations = 0
    ball_frames = 0
    mask_view = paused = False
    last = None
    start = time.perf_counter()
    try:
        if demo is None:
            source = int(args.source) if args.source.isdecimal() else args.source
            capture = cv2.VideoCapture(source)
            if not capture.isOpened():
                raise RuntimeError(f'Cannot open source: {args.source}')
        if args.record or args.headless:
            writer = cv2.VideoWriter(str(output / 'simulation.mp4'), cv2.VideoWriter_fourcc(*'mp4v'),
                                     24, (1280, 720))
            if not writer.isOpened():
                raise RuntimeError('Cannot open the MP4 encoder')
        trace = (output / 'frame_trace.csv').open('w', newline='', encoding='utf-8-sig')
        log = csv.writer(trace)
        log.writerow(('input_frame', 'epoch', 'mode', 'red', 'green', 'yellow', 'event',
                      'face_result_frame', 'face_boxes', 'face_ms', 'hdmi_source_frame',
                      'hdmi_ball_result_frame', 'hdmi_face_result_frame', 'ddr_words',
                      'unlocked', 'face_hits', 'ball_processed', 'hdmi_unlocked', 'hdmi_face_hits'))
        limit = args.frames or ((360 if args.simultaneous else 430) if demo is not None else 0)
        while not limit or frames < limit:
            if not paused:
                if demo is not None:
                    rgb = demo.frame(engine.ball.mode, frames)
                else:
                    valid, bgr = capture.read()
                    if not valid:
                        break
                    rgb = cv2.cvtColor(cv2.resize(bgr, (1280, 720)), cv2.COLOR_BGR2RGB)
                last, stats, snapshot, shown, words = engine.process(rgb, mask_view)
                faces = engine.last_detection or engine.faces
                if engine.last_face_ms:
                    face_times.append(engine.last_face_ms)
                    face_evaluations += 1
                    face_positive += bool(engine.last_detection.boxes)
                ball_frames += stats is not None
                event = 0 if snapshot is None else snapshot.event
                if event:
                    events.append({'frame': engine.frame_id, 'color': event})
                counts = tuple(engine.ball.counter.counts[c] for c in (1, 3, 2))
                log.writerow((engine.frame_id, engine.ball.epoch, engine.ball.mode, *counts,
                              event, -1 if faces is None else faces.frame_id,
                              json.dumps(() if faces is None else faces.boxes),
                              round(engine.last_face_ms, 3), -1 if shown is None else shown[0],
                              -1 if shown is None or shown[1] is None else shown[1].frame_id,
                              -1 if shown is None or shown[2] is None else shown[2].frame_id, words,
                              int(engine.unlocked), engine.face_hits, int(stats is not None),
                              -1 if shown is None else int(shown[3]), -1 if shown is None else shown[4]))
                if writer is not None:
                    writer.write(cv2.cvtColor(last, cv2.COLOR_RGB2BGR))
                frames += 1
                if frames == 160:
                    cv2.imencode('.png', cv2.cvtColor(last, cv2.COLOR_RGB2BGR))[1].tofile(
                        str(output / 'preview.png'))
                if frames in (20, 50):
                    name = 'waiting_face.png' if frames == 20 else 'ball_enabled.png'
                    cv2.imencode('.png', cv2.cvtColor(last, cv2.COLOR_RGB2BGR))[1].tofile(str(output / name))
            if not args.headless:
                cv2.imshow('Ball + Face / Python prototype', cv2.cvtColor(last, cv2.COLOR_RGB2BGR))
                key = cv2.waitKey(1) & 255
                if key in (ord('q'), 27):
                    break
                if key == ord(' '):
                    paused = not paused
                elif key in (ord('1'), ord('2')):
                    engine.configure(mode='track' if key == ord('1') else 'count')
                elif key == ord('m'):
                    mask_view = not mask_view
                elif key == ord('t'):
                    engine.configure(strict=not engine.ball.cfg.strict)
                elif key == ord('c'):
                    engine.configure(clear=True)
                elif key == ord('r'):
                    engine.reset()
        if last is None:
            raise RuntimeError('The input contained no frames')
        cv2.imencode('.png', cv2.cvtColor(last, cv2.COLOR_RGB2BGR))[1].tofile(str(output / 'last_frame.png'))
        result = {'frames': frames, 'mode': engine.ball.mode, 'source': args.source,
                  'counts_rgb_order': tuple(engine.ball.counter.counts[c] for c in (1, 2, 3)),
                  'counts_by_color': {'red': engine.ball.counter.counts[1],
                                      'green': engine.ball.counter.counts[3],
                                      'yellow': engine.ball.counter.counts[2]},
                  'total': sum(engine.ball.counter.counts.values()), 'events': events,
                  'face_evaluations': face_evaluations, 'face_positive_evaluations': face_positive,
                  'face_width': args.face_width, 'face_every': args.face_every,
                  'demo_color_face': args.demo_color_face,
                  'face_gate': engine.face_gate, 'unlocked': engine.unlocked,
                  'unlock_frame': engine.unlock_frame, 'ball_processed_frames': ball_frames,
                  'face_ms_mean': float(np.mean(face_times)) if face_times else None,
                  'face_ms_p95': float(np.percentile(face_times, 95)) if face_times else None,
                  'host_processing_fps': frames/(time.perf_counter()-start),
                  'recording_fps': 24, 'fpga_performance_verified': False}
        (output / 'summary.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps(result, ensure_ascii=False), flush=True)
    finally:
        if capture is not None:
            capture.release()
        if writer is not None:
            writer.release()
        if trace is not None:
            trace.close()
        if not args.headless:
            cv2.destroyAllWindows()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', default='demo', help='demo, camera index, or video path')
    parser.add_argument('--mode', choices=('track', 'count'), default='count')
    parser.add_argument('--headless', action='store_true')
    parser.add_argument('--record', action='store_true')
    parser.add_argument('--simultaneous', action='store_true', help='Legacy ball + face mode without startup gate')
    parser.add_argument('--demo-color-face', action='store_true', help='Use color photo; exposes skin/ball color ambiguity')
    parser.add_argument('--frames', type=int, default=0)
    parser.add_argument('--face-every', type=int, default=2)
    parser.add_argument('--face-width', type=int, default=320)
    parser.add_argument('--min-face-size', type=int, default=24, help='Minimum face window at reduced resolution')
    parser.add_argument('--output', default=str(ROOT / 'output/gate'))
    options = parser.parse_args()
    if options.frames < 0:
        parser.error('--frames cannot be negative')
    run(options)
