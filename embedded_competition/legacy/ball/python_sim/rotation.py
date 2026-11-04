"""球面标记旋转测量：RGB像素→现有判色/组件→黑点→相位展开→RPM/圈数。"""

import argparse
from collections import deque
from dataclasses import dataclass
import csv
import json
import math
from pathlib import Path
import time

import cv2
import numpy as np

from pipeline import COLORS, NAMES, ComponentRAM, Config, TargetTracker, segment, text
from scenes import BALL_RGB, draw_ball


@dataclass
class Observation:
    center: tuple | None = None
    radius: float = 0.0
    marker: tuple | None = None
    angle: float | None = None
    color: int = 0
    candidate_count: int = 0
    marker_count: int = 0
    reason: str = 'NO BALL'


class RotationMeter:
    """固定轴近似正对相机。坐标y向下，因此正角速度为相机视角顺时针。"""

    def __init__(self, max_rpm=120.0, max_gap=0.25):
        if not math.isfinite(max_rpm) or max_rpm <= 0 or not 0 < max_gap <= 1:
            raise ValueError('max_rpm必须为有限正数，max_gap须在(0,1]秒')
        self.max_rpm, self.max_gap = max_rpm, max_gap
        self.reset()

    def reset(self):
        self.previous = None
        self.last_time = None
        self.net = 0.0
        self.rpm = None
        self.partial = False
        self.state = 'WAIT MARKER'
        self.history = deque()
        self.cw = self.ccw = 0
        self.direction = self.segment_turns = 0
        self.anchor = self.extreme = 0.0

    def update(self, angle, stamp):
        if not math.isfinite(stamp) or (self.last_time is not None and stamp <= self.last_time):
            raise ValueError('时间戳必须有限且严格递增')
        if angle is not None and not math.isfinite(angle):
            raise ValueError('角度必须有限')
        self.last_time = stamp
        if angle is None:
            self.state, self.rpm = 'MARKER LOST', None
            if self.previous and stamp-self.previous[0] > min(self.max_gap, 150/(6*self.max_rpm)):
                self.partial = True
            return
        restarted = self.previous is None
        if self.previous is not None:
            old_time, old_angle = self.previous
            dt = stamp-old_time
            delta = (angle-old_angle+180) % 360-180
            # ponytail: 无法从两幅图恢复跨过半圈的相位；缺口只重建参考，不补造圈数。
            if dt > self.max_gap+1e-9 or dt*6*self.max_rpm >= 150 or abs(delta) > dt*6*self.max_rpm+4:
                self.partial, restarted = True, True
                self.history.clear()
                self.direction = self.segment_turns = 0
                self.anchor = self.extreme = self.net
            else:
                self.net += delta
                self.count_turns()
        self.previous = (stamp, angle)
        self.history.append((stamp, self.net))
        # 低采样率时至少保留四个有效观测，速度仍按实际时间而非假定60fps计算。
        while len(self.history) > 4 and stamp-self.history[0][0] > 0.30:
            self.history.popleft()
        self.rpm = None
        if len(self.history) >= 4 and stamp-self.history[0][0] >= 0.10:
            times = np.array([p[0]-stamp for p in self.history])
            phases = np.array([p[1] for p in self.history])
            times -= times.mean()
            self.rpm = float(np.dot(times, phases-phases.mean())/np.dot(times, times)/6)
            self.state = 'STOP' if abs(self.rpm) < 2 else ('CW' if self.rpm > 0 else 'CCW')
        else:
            self.state = 'ACQUIRE' if restarted else 'WARMUP'

    def count_turns(self):
        if self.direction == 0:
            if abs(self.net-self.anchor) < 8:
                return
            self.direction = 1 if self.net > self.anchor else -1
        self.extreme = max(self.extreme, self.net) if self.direction > 0 else min(self.extreme, self.net)
        turns = int((abs(self.extreme-self.anchor)+1e-7)//360)
        if self.direction > 0:
            self.cw += turns-self.segment_turns
        else:
            self.ccw += turns-self.segment_turns
        self.segment_turns = turns
        if self.direction*(self.extreme-self.net) > 8:
            self.anchor, self.extreme = self.extreme, self.net
            self.direction *= -1
            self.segment_turns = 0


class RotationPipeline:
    def __init__(self, cfg=None, max_rpm=120.0, dark_ratio=0.45):
        self.cfg = cfg or Config()
        if not 0.1 <= dark_ratio <= 0.8:
            raise ValueError('dark_ratio须在[0.1,0.8]')
        self.dark_ratio = dark_ratio
        self.store, self.tracker = ComponentRAM(self.cfg), TargetTracker(self.cfg)
        self.meter = RotationMeter(max_rpm)
        self.frame = self.ball_id = 0
        self.last_stamp = None
        self.color_mask = self.marker_mask = None

    def clear(self):
        self.tracker.reset()
        self.meter.reset()

    def step(self, rgb, stamp):
        if not math.isfinite(stamp) or (self.last_stamp is not None and stamp <= self.last_stamp):
            raise ValueError('输入时间戳必须有限且严格递增')
        self.color_mask = segment(rgb, self.cfg)
        self.last_stamp = stamp
        self.marker_mask = np.zeros(self.color_mask.shape, np.uint8)
        stats = self.store.scan(self.store.capture(self.color_mask, self.frame, 0), self.color_mask)
        self.frame += 1
        acquiring = self.tracker.target is None
        if stats.overflow:
            self.tracker.reset()
            observation = Observation(reason='COMPONENT OVERFLOW')
        else:
            self.tracker.update(stats.candidates)
            observation = Observation(candidate_count=len(stats.candidates))
            if self.tracker.state in ('CONFIRM', 'TRACK'):
                if acquiring:
                    self.ball_id += 1
                    self.meter.reset()
                observation = self.find_marker(rgb, self.tracker.observed, len(stats.candidates))
        self.meter.update(observation.angle, stamp)
        return observation

    def find_marker(self, rgb, ball, candidate_count):
        x0, y0, x1, y1 = ball.box
        roi = self.cfg.roi
        result = Observation(color=ball.color, candidate_count=candidate_count)
        if x0 <= roi[0]+2 or y0 <= roi[1]+2 or x1 >= roi[2]-3 or y1 >= roi[3]-3:
            result.reason = 'BALL CLIPPED'
            return result
        # 测量使用当前实测组件，不能把PRED显示坐标用于球面相位。
        mask = (self.color_mask[y0:y1+1, x0:x1+1] == ball.color).astype(np.uint8)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return result
        outer = max(contours, key=cv2.contourArea)
        (cx, cy), radius = cv2.minEnclosingCircle(outer)
        cx, cy = cx+x0, cy+y0
        result.center, result.radius = (cx, cy), radius
        if radius < 12 or cv2.contourArea(cv2.convexHull(outer)) < 0.75*math.pi*radius**2:
            result.reason = 'BALL SHAPE UNCERTAIN'
            return result
        left, top = max(0, int(cx-radius)), max(0, int(cy-radius))
        right, bottom = min(self.cfg.width, math.ceil(cx+radius+1)), min(self.cfg.height, math.ceil(cy+radius+1))
        gray = cv2.cvtColor(rgb[top:bottom, left:right], cv2.COLOR_RGB2GRAY)
        yy, xx = np.ogrid[top:bottom, left:right]
        distance = (xx-cx)**2+(yy-cy)**2
        interior = distance < (radius*0.85)**2
        level = float(np.median(gray[interior]))*self.dark_ratio
        dark = ((gray < level) & interior).astype(np.uint8)
        self.marker_mask[top:bottom, left:right] = dark
        count, _, areas, centers = cv2.connectedComponentsWithStats(dark, connectivity=8)
        markers = []
        for index in range(1, count):
            area = areas[index, cv2.CC_STAT_AREA]
            width, height = areas[index, cv2.CC_STAT_WIDTH], areas[index, cv2.CC_STAT_HEIGHT]
            mx, my = centers[index]+(left, top)
            offset = math.hypot(mx-cx, my-cy)/radius
            if max(6, radius**2*0.0008) <= area <= math.pi*radius**2*0.04 and 0.2 <= offset <= 0.78:
                if max(width, height) <= 2*min(width, height) and area >= width*height*0.35:
                    markers.append((mx, my))
        result.marker_count = len(markers)
        if len(markers) != 1:
            result.reason = 'NO MARKER' if not markers else 'MULTIPLE MARKERS'
            return result
        result.marker = markers[0]
        result.angle = math.degrees(math.atan2(result.marker[1]-cy, result.marker[0]-cx)) % 360
        result.reason = 'VALID'
        return result


def render_ball(width, height, center, radius, angle, color=1, marker=True, noise=0, seed=0):
    """输入场景：黑色球冠随绕视轴自转；球坐标/角度不会传入检测器。"""
    rgb = np.full((height, width, 3), (30, 42, 51), np.uint8)
    rgb[height//3:] = (56, 65, 72)
    cx, cy = center
    cv2.ellipse(rgb, (round(cx), round(cy+radius*0.94)), (round(radius*1.15), round(radius*0.15)),
                0, 0, 360, (33, 39, 44), -1)
    draw_ball(rgb, round(cx), round(cy), color, round(radius))
    left, top = max(0, math.floor(cx-radius)), max(0, math.floor(cy-radius))
    right, bottom = min(width, math.ceil(cx+radius+1)), min(height, math.ceil(cy+radius+1))
    yy, xx = np.mgrid[top:bottom, left:right]
    nx, ny = (xx-cx)/radius, (yy-cy)/radius
    inside = nx*nx+ny*ny <= 1
    nz = np.sqrt(np.maximum(0, 1-nx*nx-ny*ny))
    theta = math.radians(angle)
    surface_dot = nx*0.60*math.cos(theta)+ny*0.60*math.sin(theta)+nz*0.80
    if marker:
        rgb[top:bottom, left:right][inside & (surface_dot >= math.cos(0.11))] = (11, 12, 13)
    if noise:
        patch = rgb[top:bottom, left:right].astype(np.int16)
        patch += np.random.default_rng(seed).integers(-noise, noise+1, patch.shape, dtype=np.int16)
        rgb[top:bottom, left:right] = np.clip(patch, 0, 255).astype(np.uint8)
    return rgb


def demo_phase(stamp):
    segments = ((3.0, 30.0), (1.5, 0.0), (3.5, -45.0), (4.0, 60.0))
    cycles, local = divmod(stamp, 12.0)
    angle = cycles*sum(duration*rpm*6 for duration, rpm in segments)
    for duration, rpm in segments:
        elapsed = min(duration, local)
        angle += elapsed*rpm*6
        if local < duration:
            return angle, rpm
        local -= duration
    return angle, 60.0


def annotate(rgb, engine, observation):
    image = rgb.copy()
    cfg, meter = engine.cfg, engine.meter
    cv2.rectangle(image, cfg.roi[:2], (cfg.roi[2]-1, cfg.roi[3]-1), (130, 147, 162), 1)
    if observation.center:
        center = tuple(round(v) for v in observation.center)
        cv2.circle(image, center, round(observation.radius), COLORS[observation.color], 2)
        cv2.drawMarker(image, center, (245, 245, 245), cv2.MARKER_CROSS, 14, 1)
        if observation.marker:
            point = tuple(round(v) for v in observation.marker)
            cv2.line(image, center, point, (90, 230, 255), 2)
            cv2.circle(image, point, 9, (90, 230, 255), 2)
    image[:144] = (13, 24, 37)
    rpm = '--' if meter.rpm is None else f'{abs(meter.rpm):05.1f}'
    angle = '--' if observation.angle is None else f'{observation.angle:06.1f}'
    lines = [f'BALL ROTATION    {NAMES[observation.color]}    ID={engine.ball_id}    {meter.state}',
             f'RPM={rpm}    ANGLE={angle}deg    NET={meter.net/360:+.3f}rev',
             f'FULL CW={meter.cw}    FULL CCW={meter.ccw}    COVERAGE={"UNAVAILABLE" if meter.previous is None else ("PARTIAL" if meter.partial else "CONTINUOUS")}',
             f'{observation.reason}   [C] CLEAR  [SPACE] PAUSE  [M] MASK  [Q] EXIT']
    for index, line in enumerate(lines):
        text(image, line, (18, 28+index*32), scale=0.65, color=(224, 235, 243))
    return image


def save_png(path, rgb):
    ok, data = cv2.imencode('.png', cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))
    if not ok:
        raise RuntimeError('图像编码失败')
    data.tofile(str(path))


def fit_frame(bgr, width=1280, height=720):
    scale = min(width/bgr.shape[1], height/bgr.shape[0])
    resized = cv2.resize(bgr, (round(bgr.shape[1]*scale), round(bgr.shape[0]*scale)))
    rgb = np.full((height, width, 3), (30, 35, 40), np.uint8)
    top, left = (height-resized.shape[0])//2, (width-resized.shape[1])//2
    rgb[top:top+resized.shape[0], left:left+resized.shape[1]] = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
    return rgb


def run(args):
    folder = Path(args.output)
    folder.mkdir(parents=True, exist_ok=True)
    engine = RotationPipeline(max_rpm=args.max_rpm, dark_ratio=args.dark_ratio)
    source = None
    live = args.source.isdecimal()
    fps = args.fps
    if args.source != 'demo':
        source = cv2.VideoCapture(int(args.source) if live else args.source)
        if not source.isOpened():
            source.release()
            raise RuntimeError(f'无法打开输入：{args.source}')
        if not live:
            reported = source.get(cv2.CAP_PROP_FPS)
            if math.isfinite(reported) and reported > 0:
                fps = reported
    writers = []
    processed = 0
    paused = show_mask = False
    maximum = args.frames or (720 if args.headless and (source is None or live) else 0)
    errors, measured_rpms = [], []
    valid_angles = 0
    clock_start = time.perf_counter()
    output = None
    last_stamp = -1.0
    window = 'Ball rotation - RGB measurement'
    try:
        if args.headless or args.record:
            for name in ('rotation_input.mp4', 'rotation_result.mp4'):
                writer = cv2.VideoWriter(str(folder/name), cv2.VideoWriter_fourcc(*'mp4v'), fps, (1280, 720))
                writers.append(writer)
                if not writer.isOpened():
                    raise RuntimeError('视频编码器无法打开')
        if not args.headless:
            cv2.namedWindow(window, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(window, 1280, 720)
        with (folder/'rotation_trace.csv').open('w', newline='', encoding='utf-8-sig') as handle:
            log = csv.writer(handle)
            log.writerow(('frame','time_s','ball_id','color','ball_x','ball_y','marker_x','marker_y',
                          'angle_deg','signed_rpm','net_rev','full_cw','full_ccw','state','reason','partial',
                          'reference_rpm_demo_only'))
            while maximum == 0 or processed < maximum:
                tick = time.perf_counter()
                if not paused:
                    reference = None
                    if source is None:
                        stamp = processed/fps
                        phase, reference = demo_phase(stamp)
                        center = (640+160*math.sin(stamp*0.6), 420+24*math.sin(stamp*0.8))
                        hidden = 5.40 <= stamp % 12 < 5.45
                        rgb = render_ball(1280, 720, center, 112, phase, marker=not hidden, noise=2, seed=processed)
                    else:
                        ok, bgr = source.read()
                        if not ok:
                            break
                        rgb = fit_frame(bgr)
                        stamp = time.perf_counter()-clock_start if live else source.get(cv2.CAP_PROP_POS_MSEC)/1000
                        if not math.isfinite(stamp) or stamp <= last_stamp:
                            stamp = max(processed/fps, last_stamp+1/fps) if not live else max(time.perf_counter()-clock_start, last_stamp+1e-6)
                    observation = engine.step(rgb, stamp)
                    valid_angles += int(observation.angle is not None)
                    last_stamp = stamp
                    output = annotate(rgb, engine, observation)
                    meter = engine.meter
                    if meter.rpm is not None:
                        measured_rpms.append(meter.rpm)
                        # 真值仅作离线误差统计，排除变速后的0.5s稳定时间。
                        local = stamp % 12
                        if reference is not None and min(abs(local-boundary) for boundary in (0,3,4.5,8,12)) > 0.5:
                            errors.append(abs(meter.rpm-reference))
                    center_values = observation.center or ('','')
                    marker_values = observation.marker or ('','')
                    log.writerow((processed,stamp,engine.ball_id,NAMES[observation.color],*center_values,*marker_values,
                                  observation.angle,meter.rpm,meter.net/360,meter.cw,meter.ccw,meter.state,
                                  observation.reason,meter.partial,reference))
                    for writer, frame in zip(writers,(rgb,output)):
                        writer.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
                    if processed == round(fps*2):
                        save_stages(folder, rgb, engine, output)
                    processed += 1
                    if args.headless and processed % 120 == 0:
                        print(f'frame={processed} state={meter.state} rpm={meter.rpm} net={meter.net/360:.3f}',flush=True)
                if not args.headless:
                    shown = output
                    if show_mask and output is not None:
                        shown = np.zeros_like(output)
                        shown[engine.marker_mask != 0] = (255, 255, 255)
                    if shown is not None:
                        cv2.imshow(window, cv2.cvtColor(shown, cv2.COLOR_RGB2BGR))
                    key = cv2.waitKey(max(1, round(1000/fps-(time.perf_counter()-tick)*1000))) & 255
                    if key in (27, ord('q')) or cv2.getWindowProperty(window,cv2.WND_PROP_VISIBLE) < 1:
                        break
                    if key == ord(' '):
                        paused = not paused
                    elif key == ord('c'):
                        engine.clear()
                    elif key == ord('m'):
                        show_mask = not show_mask
    finally:
        for writer in writers:
            writer.release()
        if source is not None:
            source.release()
        if not args.headless:
            cv2.destroyAllWindows()
    if processed == 0:
        raise RuntimeError('没有有效输入帧')
    save_png(folder/'last_frame.png', output)
    result = {'frames':processed,'input_timebase_fps':fps,'elapsed_processing_seconds':round(time.perf_counter()-clock_start,3),
              'source':args.source,'model':'RGB image algorithm; not RTL cycle simulation',
              'axis_assumption':'fixed rotation axis approximately toward camera; unique dark marker offset from axis',
              'max_rpm_bound':args.max_rpm,'net_rev':engine.meter.net/360,'full_cw':engine.meter.cw,
              'full_ccw':engine.meter.ccw,'coverage_partial':engine.meter.partial,
              'stable_demo_rpm_mae':float(np.mean(errors)) if errors else None,
              'stable_demo_samples':len(errors),'min_measured_rpm':min(measured_rpms,default=None),
              'max_measured_rpm':max(measured_rpms,default=None),'valid_angle_frames':valid_angles,
              'coverage':'UNAVAILABLE' if engine.meter.previous is None else ('PARTIAL' if engine.meter.partial else 'CONTINUOUS'),
              'physical_camera_validated':False}
    (folder/'summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False),flush=True)
    return result


def save_stages(folder, rgb, engine, output):
    palette = np.array([(12,18,25),COLORS[1],COLORS[2],COLORS[3]],np.uint8)
    masks = (engine.color_mask, engine.marker_mask)
    colored, marker = palette[masks[0]], np.repeat((masks[1]*255)[...,None],3,axis=2)
    panels = []
    for name, title, image in (('01_rotation_input.png','INPUT RGB / RENDERER',rgb),
                               ('02_rotation_color.png','EXISTING COLOR SEGMENTATION',colored),
                               ('03_rotation_marker.png','DARK MARKER IN MEASURED BALL ROI',marker),
                               ('04_rotation_output.png','ANGLE -> UNWRAP -> RPM / TURNS',output)):
        save_png(folder/name,image)
        panel = np.full((390,640,3),(12,20,30),np.uint8)
        panel[30:] = cv2.resize(image,(640,360))
        text(panel,title,(12,22),scale=0.48)
        panels.append(panel)
    save_png(folder/'rotation_pipeline.png',np.vstack((np.hstack(panels[:2]),np.hstack(panels[2:]))))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',default='demo',help='demo、摄像头编号或视频路径')
    parser.add_argument('--headless',action='store_true')
    parser.add_argument('--record',action='store_true')
    parser.add_argument('--frames',type=int,default=0,help='0为交互不限帧；headless demo默认720帧')
    parser.add_argument('--fps',type=float,default=60,help='demo时间轴/文件无FPS时的回退值')
    parser.add_argument('--max-rpm',type=float,default=120,help='真实转速的已知上界；无法从采样图像自动识别混叠')
    parser.add_argument('--dark-ratio',type=float,default=0.45,help='黑点灰度阈值相对球面中位亮度比例')
    parser.add_argument('--output',default=str(Path(__file__).parent/'output/rotation'))
    args = parser.parse_args()
    if args.frames < 0 or not math.isfinite(args.fps) or not 1 <= args.fps <= 240:
        parser.error('frames须非负，fps须在[1,240]')
    run(args)


if __name__ == '__main__':
    main()
