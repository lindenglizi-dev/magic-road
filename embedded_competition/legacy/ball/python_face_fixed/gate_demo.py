"""Run the unchanged ball model behind a cycle-budgeted fixed-point face gate."""
import argparse
import csv
from dataclasses import dataclass
import json
import sys
import time

import cv2
import numpy as np

from fixed_face import BASE, C, ROOT, detect, load_rom
sys.path.insert(0, str(BASE))
from face_pipeline import Demo
from pipeline import Pipeline, render, text
from scenes import demo_frame, draw_ball
from video_io import DDRFrameBuffer


@dataclass
class GateControl:
    epoch: int = 0
    hits: int = 0
    last_sample: int = -1
    pending: bool = False
    unlocked: bool = False

    def result(self, sample_id, epoch, present, fault=False):
        if epoch != self.epoch or sample_id <= self.last_sample or self.unlocked or self.pending:
            return False
        self.last_sample = sample_id
        self.hits = self.hits+1 if present and not fault else 0
        self.pending = self.hits == 3
        return True

    def frame_start(self):
        if self.pending:
            self.pending, self.unlocked = False, True
            return True
        return False

    def reset(self):
        self.epoch = (self.epoch+1) & 65535
        self.hits, self.last_sample = 0, -1
        self.pending = self.unlocked = False


class FixedGatePipeline:
    def __init__(self, mode='count'):
        self.model = load_rom()
        self.ball = Pipeline(mode=mode)
        self.gate = GateControl()
        self.frame_id = -1
        self.job = self.last_result = None
        self.result_events = []
        self.unlock_frame = None
        self.last_trace = None

    def reset(self):
        self.gate.reset()
        self.job = self.last_result = None
        self.unlock_frame = None
        self.ball.configure(clear=True)
        self.ball.ddr = DDRFrameBuffer()

    def process(self, rgb):
        if rgb.shape != (720, 1280, 3) or rgb.dtype != np.uint8:
            raise ValueError('Expected full-resolution RGB uint8')
        self.frame_id += 1
        fid = self.frame_id
        now = fid*C['clock_hz_reference_only']//C['video_fps_assumption']
        completed = -1
        if self.job is not None and self.job['finish_cycle'] < now:
            job, self.job = self.job, None
            result = job['result']
            if self.gate.result(job['sample_id'], job['epoch'], bool(result['boxes']), result['fault']):
                self.last_result = result
                completed = job['sample_id']
                self.result_events.append({'sample_frame': completed, 'arrival_frame': fid,
                                           'finish_cycle': job['finish_cycle'], 'cycles': result['cycles'],
                                           'face': bool(result['boxes']), 'fault': result['fault'],
                                           'confirm': self.gate.hits})
        if self.gate.frame_start():
            self.unlock_frame = fid
            self.ball.configure(clear=True)
            self.last_result = None
        display = self.ball.snapshot
        stats = None
        if self.gate.unlocked:
            self.ball.frame_id = fid-1
            stats = self.ball.analyse(rgb)
            self.ball.accept(stats)
        elif self.job is None:
            result = detect(rgb, self.model)
            self.job = {'sample_id': fid, 'epoch': self.gate.epoch, 'result': result,
                        'finish_cycle': (fid+1)*C['clock_hz_reference_only']//C['video_fps_assumption']+result['cycles']}
        mask = np.zeros((720, 1280), np.uint8) if stats is None else stats.mask
        painted = render(rgb, mask, display, self.ball.cfg, self.ball.mode)
        cv2.rectangle(painted, (0, 42), (1279, 77), (14, 22, 34), -1)
        message = 'BALL ENABLED / FIXED HAAR OFF' if self.gate.unlocked else 'ALIGN FACE WITH CENTER GUIDE / BALL DISABLED'
        text(painted, message, (28, 65), (0, 235, 255), 0.6)
        if not self.gate.unlocked:
            cv2.rectangle(painted, (512, 232), (767, 487), (0, 235, 255), 2)
            text(painted, 'FACE ROI 256 -> 64', (512, 220), (0, 235, 255), 0.5)
            if self.last_result is not None:
                for left, top, right, bottom in self.last_result['boxes']:
                    cv2.rectangle(painted, (left, top), (right, bottom), (0, 235, 255), 2)
        cv2.rectangle(painted, (885, 77), (1279, 116), (14, 22, 34), -1)
        text(painted, f'CONFIRM {self.gate.hits}/3  BUSY {int(self.job is not None)}', (895, 102),
             (0, 235, 255), 0.52)
        cv2.rectangle(painted, (0, 671), (1279, 719), (14, 22, 34), -1)
        text(painted, 'ROM -> integer Haar -> 3 fresh samples -> frame-boundary enable -> original ball pipeline',
             (24, 690), scale=0.48)
        text(painted, 'Timing is a proposed FSM budget at 103.520 MHz, NOT measured RTL timing. Q: quit',
             (24, 712), (120, 143, 164), 0.43)
        hdmi, shown, words = self.ball.ddr.exchange(painted, (fid, self.gate.unlocked, self.gate.hits,
                                                            -1 if display is None else display.frame_id))
        counts = self.ball.counter.counts
        self.last_trace = (fid, now, int(self.gate.unlocked), self.gate.hits, int(stats is not None),
                           int(self.job is not None), completed, counts[1], counts[3], counts[2],
                           0 if stats is None else self.ball.snapshot.event,
                           -1 if shown is None else shown[0], -1 if shown is None else int(shown[1]), words)
        return hdmi


def source_frame(index, tile, mode='count'):
    rgb = demo_frame(mode, max(0, index-120))
    if index < 30:
        draw_ball(rgb, 450+index*16, 410, 1)
    if 40 <= index < 110:
        rgb[270:450, 550:730] = tile
    return rgb


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--frames', type=int, default=480)
    parser.add_argument('--mode', choices=('count', 'track'), default='count')
    parser.add_argument('--headless', action='store_true')
    args = parser.parse_args()
    if args.frames < 1:
        parser.error('--frames must be positive')
    folder = ROOT/'reports'/('gate_'+args.mode)
    folder.mkdir(parents=True, exist_ok=True)
    engine, tile = FixedGatePipeline(args.mode), Demo().tile
    writer = cv2.VideoWriter(str(folder/'simulation.mp4'), cv2.VideoWriter_fourcc(*'mp4v'), 24, (1280, 720))
    if not writer.isOpened():
        raise RuntimeError('Cannot open MP4 writer')
    started = time.perf_counter()
    try:
        with (folder/'frame_trace.csv').open('w', encoding='utf-8-sig', newline='') as stream:
            log = csv.writer(stream)
            log.writerow(('input_frame', 'sof_cycle', 'unlocked', 'confirm', 'ball_processed', 'face_busy',
                          'completed_sample', 'red', 'green', 'yellow', 'event', 'display_frame', 'display_unlocked', 'ddr_words'))
            for index in range(args.frames):
                hdmi = engine.process(source_frame(index, tile, args.mode))
                log.writerow(engine.last_trace)
                writer.write(cv2.cvtColor(hdmi, cv2.COLOR_RGB2BGR))
                if index in (20, 56, 100, 180, 479):
                    cv2.imencode('.png', cv2.cvtColor(hdmi, cv2.COLOR_RGB2BGR))[1].tofile(str(folder/f'frame_{index:03d}.png'))
                if index % 120 == 119:
                    print(f'frames={index+1} unlock={engine.unlock_frame} counts={engine.ball.counter.counts}', flush=True)
                if not args.headless:
                    cv2.imshow('Fixed-point face startup gate / Python model', cv2.cvtColor(hdmi, cv2.COLOR_RGB2BGR))
                    if cv2.waitKey(1) & 255 in (ord('q'), 27):
                        break
        counts = engine.ball.counter.counts
        report = {'frames': engine.frame_id+1, 'mode': args.mode, 'unlock_frame': engine.unlock_frame,
                  'counts': {'red': counts[1], 'green': counts[3], 'yellow': counts[2]},
                  'face_results': engine.result_events, 'host_elapsed_seconds': time.perf_counter()-started,
                  'scope': 'Integer functional model plus proposed-cycle scheduler; not cycle-accurate RTL or board evidence'}
        (folder/'summary.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
        print(json.dumps(report), flush=True)
    finally:
        writer.release()
        if not args.headless:
            cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
