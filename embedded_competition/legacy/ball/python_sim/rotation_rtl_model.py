"""旋转RTL结构的整数/存储/帧事件模型；不等同于RTL逐时钟仿真。"""

import argparse
from collections import Counter, deque
from dataclasses import dataclass, field, replace
import csv
import heapq
import json
import math
from pathlib import Path
import time

import cv2
import numpy as np

from pipeline import ComponentRAM, Config, TargetTracker, segment, text
from rotation import demo_phase, fit_frame, render_ball, save_png


CLOCK_HZ = 103_520_000
TURN = 65_536
ATAN_TABLE = (8192, 4836, 2555, 1297, 651, 326, 163, 81, 41, 20, 10, 5, 3, 1, 1, 0)


def checked(value, bits, signed=False):
    """对计划中的寄存器位宽执行检查，Python大整数不能悄悄掩盖溢出。"""
    lower = -(1 << (bits-1)) if signed else 0
    upper = (1 << (bits-int(signed)))-1
    if not lower <= value <= upper:
        raise OverflowError(f'{value} does not fit {"s" if signed else "u"}{bits}')
    return value


def divide_round(numerator, denominator, bits=96):
    """有符号恢复除法，最近整数舍入；每轮处理一位。"""
    if denominator <= 0:
        raise ValueError('除数必须为正')
    sign = -1 if numerator < 0 else 1
    magnitude = checked(abs(numerator), bits)
    checked(denominator, bits)
    remainder = quotient = 0
    for shift in range(bits-1, -1, -1):
        remainder = (remainder << 1) | ((magnitude >> shift) & 1)
        if remainder >= denominator:
            remainder -= denominator
            quotient |= 1 << shift
    return sign*(quotient+int(2*remainder >= denominator))


def cordic_phase(dx, dy):
    """输入为s16的Q4坐标差；输出u16圈相位，Y向下时正向为顺时针。"""
    checked(dx, 16, True)
    checked(dy, 16, True)
    if dx == dy == 0:
        raise ValueError('零向量没有角度')
    x, y, angle = dx << 8, dy << 8, 0
    if x < 0:
        x, y, angle = -x, -y, TURN//2
    for shift, increment in enumerate(ATAN_TABLE):
        old_x, old_y = x, y
        if old_y > 0:
            x, y, angle = old_x+(old_y >> shift), old_y-(old_x >> shift), angle+increment
        elif old_y < 0:
            x, y, angle = old_x-(old_y >> shift), old_y+(old_x >> shift), angle-increment
        checked(x, 26, True)
        checked(y, 26, True)
    return angle & 0xffff


class FixedMeter:
    """定宽相位展开、整数最小二乘RPM、方向迟滞和计圈。"""

    def __init__(self, max_rpm=120):
        if not isinstance(max_rpm, int) or not 1 <= max_rpm <= 120:
            raise ValueError('本版先验上界必须为1～120的整数RPM')
        self.max_rpm = max_rpm
        self.reset()

    def reset(self):
        self.previous = self.last_tick = None
        self.net_phase = self.anchor = self.extreme = 0
        self.direction = self.segment_turns = self.cw = self.ccw = 0
        self.history = deque()
        self.rpm_x10 = None
        self.partial = False
        self.counter_saturated = False
        self.state = 'WAIT MARKER'

    def update(self, angle, tick):
        checked(tick, 64)
        if self.last_tick is not None and tick <= self.last_tick:
            raise ValueError('采集时间戳必须严格递增')
        self.last_tick = tick
        self.rpm_x10 = None
        if angle is None:
            self.state = 'MARKER LOST'
            if self.previous:
                gap = tick-self.previous[0]
                self.partial |= gap*4 > CLOCK_HZ or gap*self.max_rpm >= 25*CLOCK_HZ
            return
        checked(angle, 16)
        restarted = self.previous is None
        if self.previous is not None:
            old_tick, old_angle = self.previous
            dt = tick-old_tick
            delta = ((angle-old_angle+TURN//2) & 0xffff)-TURN//2
            # 约4度容差取向上整数量化；所有判断使用交叉乘法。
            impossible = (abs(delta)-729)*60*CLOCK_HZ > self.max_rpm*dt*TURN
            if dt*4 > CLOCK_HZ or dt*self.max_rpm >= 25*CLOCK_HZ or impossible:
                self.partial, restarted = True, True
                self.history.clear()
                self.direction = self.segment_turns = 0
                self.anchor = self.extreme = self.net_phase
            else:
                self.net_phase = checked(self.net_phase+delta, 48, True)
                self._count_turns()
        self.previous = tick, angle
        self.history.append((tick, self.net_phase))
        while len(self.history) > 4 and (tick-self.history[0][0])*10 > 3*CLOCK_HZ:
            self.history.popleft()
        while len(self.history) > 32:
            self.history.popleft()
        if len(self.history) < 4 or (tick-self.history[0][0])*10 < CLOCK_HZ:
            self.state = 'ACQUIRE' if restarted else 'WARMUP'
            return
        base_tick, base_phase = self.history[0]
        # 时间单位1024个时钟，约9.89us；只量化相对时间，不改采集时间轴。
        points = [(checked((t-base_tick) >> 10, 18), checked(p-base_phase, 20, True))
                  for t, p in self.history]
        count = len(points)
        sum_t = sum(t for t, _ in points)
        sum_p = sum(p for _, p in points)
        sum_tt = sum(t*t for t, _ in points)
        sum_tp = sum(t*p for t, p in points)
        numerator = checked(count*sum_tp-sum_t*sum_p, 64, True)
        denominator = checked(count*sum_tt-sum_t*sum_t, 64)
        self.rpm_x10 = checked(divide_round(numerator*600*CLOCK_HZ,
                                          denominator*TURN*1024), 24, True)
        self.state = 'STOP' if abs(self.rpm_x10) < 20 else ('CW' if self.rpm_x10 > 0 else 'CCW')

    def _count_turns(self):
        hysteresis = 1456  # 约8度。
        if self.direction == 0:
            if abs(self.net_phase-self.anchor) < hysteresis:
                return
            self.direction = 1 if self.net_phase > self.anchor else -1
        self.extreme = (max if self.direction > 0 else min)(self.extreme, self.net_phase)
        turns = abs(self.extreme-self.anchor) >> 16
        increment = turns-self.segment_turns
        if self.direction > 0:
            self.counter_saturated |= self.cw+increment > 0xffffffff
            self.cw = min(0xffffffff, self.cw+increment)
        else:
            self.counter_saturated |= self.ccw+increment > 0xffffffff
            self.ccw = min(0xffffffff, self.ccw+increment)
        self.partial |= self.counter_saturated
        self.segment_turns = turns
        if self.direction*(self.extreme-self.net_phase) > hysteresis:
            self.anchor, self.extreme = self.extreme, self.net_phase
            self.direction *= -1
            self.segment_turns = 0


@dataclass
class Bank:
    gray: np.ndarray = field(default_factory=lambda: np.zeros((128, 128), np.uint8))
    busy: bool = False
    frame_id: int = -1
    epoch: int = 0
    tick: int = 0
    origin: tuple = (0, 0)
    window_source: int = -1
    ready_tick: int = 0


@dataclass
class Measurement:
    frame_id: int
    epoch: int
    tick: int
    ball_id: int = 0
    reason: str = 'WAIT WINDOW'
    color: int = 0
    box: tuple | None = None
    center_q4: tuple | None = None
    marker_q4: tuple | None = None
    angle: int | None = None
    origin: tuple | None = None
    window_source: int = -1
    median: int = 0
    threshold: int = 0
    marker_count: int = 0
    cycles: int = 0
    done_tick: int = 0
    bank_index: int = -1
    dark: np.ndarray | None = None
    gray: np.ndarray | None = None
    rpm_x10: int | None = None
    net_phase: int = 0
    cw: int = 0
    ccw: int = 0
    partial: bool = False
    state: str = 'WAIT MARKER'
    counter_saturated: bool = False


def extract_marker(bank, ball, result, cfg, queue_capacity=512):
    """只读取已采集灰度bank和同帧实测球框，四连通、有界队列。"""
    if (bank.frame_id, bank.epoch, bank.tick) != (result.frame_id, result.epoch, result.tick):
        result.reason = 'FRAME TAG MISMATCH'
        return result
    result.origin, result.window_source = bank.origin, bank.window_source
    result.color, result.box = ball.color, ball.box
    x0, y0, x1, y1 = ball.box
    width, height = x1-x0+1, y1-y0+1
    result.center_q4 = ((x0+x1)*8, (y0+y1)*8)
    cx, cy = result.center_q4
    rx0, ry0, rx1, ry1 = cfg.roi
    if x0 <= rx0+2 or y0 <= ry0+2 or x1 >= rx1-3 or y1 >= ry1-3:
        result.reason = 'BALL CLIPPED'
        return result
    if not 80 <= min(width, height) <= max(width, height) <= 192:
        result.reason = 'BALL SIZE OUT OF RANGE'
        return result
    if max(width, height)*4 > min(width, height)*5:
        result.reason = 'BALL SHAPE UNCERTAIN'
        return result
    ox, oy = bank.origin
    if x0 < ox or y0 < oy or x1 >= ox+256 or y1 >= oy+256:
        result.reason = 'WINDOW MISS'
        return result
    radius = min(width, height)*8  # Q4半径。
    inner = radius*217 >> 8
    xx = ox*16+np.arange(128, dtype=np.int32)*32+8
    yy = oy*16+np.arange(128, dtype=np.int32)*32+8
    interior = (xx[None, :]-cx)**2+(yy[:, None]-cy)**2 < inner*inner
    histogram = np.bincount(bank.gray[interior], minlength=256)
    total = checked(int(histogram.sum()), 15)
    target, accumulated = (total+1)//2, 0
    for median, number in enumerate(histogram):
        accumulated += int(number)
        if accumulated >= target:
            break
    result.median, result.threshold = median, median*115 >> 8
    dark = (bank.gray < result.threshold) & interior
    result.dark, result.gray = dark.copy(), bank.gray.copy()  # 仅用于软件阶段图输出。
    visited = np.zeros((128, 128), bool)
    result.cycles = 256+2*16384+256
    markers = []
    for flat in np.flatnonzero(dark):
        row, column = divmod(int(flat), 128)
        if visited[row, column]:
            continue
        pending = deque([(row, column)])
        visited[row, column] = True
        count = sx = sy = 0
        left = right = column
        top = bottom = row
        while pending:
            row, column = pending.popleft()
            count = checked(count+1, 15)
            sx = checked(sx+column*32+8, 32)
            sy = checked(sy+row*32+8, 32)
            left, right = min(left, column), max(right, column)
            top, bottom = min(top, row), max(bottom, row)
            result.cycles += 24  # 暂定同步RAM/FSM服务预算，并非已实现RTL周期。
            for nr, nc in ((row-1, column), (row+1, column), (row, column-1), (row, column+1)):
                if 0 <= nr < 128 and 0 <= nc < 128 and dark[nr, nc] and not visited[nr, nc]:
                    if len(pending) >= queue_capacity:
                        result.reason = 'MARKER QUEUE OVERFLOW'
                        return result
                    visited[nr, nc] = True
                    pending.append((nr, nc))
        mx, my = ox*16+divide_round(sx, count, 32), oy*16+divide_round(sy, count, 32)
        area, bw, bh = count*4, (right-left+1)*2, (bottom-top+1)*2
        offset = (mx-cx)**2+(my-cy)**2
        minimum = max(6, radius*radius//(256*1250))
        maximum = radius*radius*804//(256*256*25)
        if (minimum <= area <= maximum and (radius*51 >> 8)**2 <= offset <= (radius*200 >> 8)**2
                and max(bw, bh) <= 2*min(bw, bh) and area*100 >= bw*bh*35):
            markers.append((mx, my))
        result.cycles += 64
    result.marker_count = len(markers)
    if len(markers) != 1:
        result.reason = 'NO MARKER' if not markers else 'MULTIPLE MARKERS'
        return result
    result.marker_q4 = markers[0]
    result.angle = cordic_phase(markers[0][0]-cx, markers[0][1]-cy)
    result.reason = 'VALID'
    result.cycles += 16+8192  # CORDIC及窗口串行算术预留预算。
    return result


class RotationHardwareModel:
    """RGB帧输入；双bank真实所有权和事件延迟，像素级逐拍时序尚未建模。"""

    def __init__(self, cfg=None, fps=60, color_cycles=1_035_271, marker_cycles=None, max_rpm=120):
        self.cfg = cfg or Config()
        if self.cfg.width < 256 or self.cfg.height < 256:
            raise ValueError('采集图像必须能容纳256×256窗口')
        if not math.isfinite(fps) or not 1 <= fps <= 240 or color_cycles < 0:
            raise ValueError('帧率或统计延迟无效')
        if marker_cycles is not None and marker_cycles < 0:
            raise ValueError('黑点服务周期必须非负')
        self.period = round(CLOCK_HZ/fps)
        self.color_cycles, self.marker_cycles = color_cycles, marker_cycles
        self.store, self.tracker = ComponentRAM(self.cfg), TargetTracker(self.cfg)
        self.meter = FixedMeter(max_rpm)
        self.banks = [Bank(), Bank()]
        self.events, self.completed = [], {}
        self.frame_id = self.next_publish = self.epoch = self.ball_id = 0
        self.sequence = 0
        self.last_input_tick = None
        self.window = self.latest = None
        self.engine_free = 0
        self.meter_ball_id = 0
        self.new_results = []
        self.counters = Counter()

    def clear(self):
        self.epoch += 1
        self.events.clear()
        self.completed.clear()
        self.next_publish = self.frame_id
        for bank in self.banks:
            bank.busy = False
        self.tracker.reset()
        self.meter.reset()
        self.window = self.latest = None
        self.engine_free = 0
        self.new_results = []

    def _event(self, tick, kind, payload):
        self.sequence += 1
        heapq.heappush(self.events, (tick, self.sequence, kind, payload))

    def advance(self, tick):
        while self.events and self.events[0][0] <= tick:
            when, _, kind, payload = heapq.heappop(self.events)
            if kind == 'color':
                self._color_done(when, *payload)
            else:
                result = payload
                if result.epoch != self.epoch:
                    continue
                bank = self.banks[result.bank_index]
                if not bank.busy or bank.frame_id != result.frame_id:
                    raise AssertionError('bank在完成前被覆盖')
                bank.busy = False
                self.completed[result.frame_id] = result
            self._publish_ready()

    def _publish_ready(self):
        while self.next_publish in self.completed:
            result = self.completed.pop(self.next_publish)
            self.next_publish += 1
            if result.ball_id and result.ball_id != self.meter_ball_id:
                self.meter.reset()
                self.meter_ball_id = result.ball_id
            self.meter.update(result.angle, result.tick)
            result.rpm_x10, result.net_phase = self.meter.rpm_x10, self.meter.net_phase
            result.cw, result.ccw, result.partial = self.meter.cw, self.meter.ccw, self.meter.partial
            result.state = self.meter.state
            result.counter_saturated = self.meter.counter_saturated
            self.latest = result
            self.new_results.append(result)
            self.counters[result.reason] += 1

    def step(self, rgb, stamp):
        if not math.isfinite(stamp) or stamp < 0:
            raise ValueError('采集时间必须为非负有限数')
        tick = checked(round(stamp*CLOCK_HZ), 64)
        if self.last_input_tick is not None and tick <= self.last_input_tick:
            raise ValueError('输入时间必须严格前进')
        if rgb.shape != (self.cfg.height, self.cfg.width, 3) or rgb.dtype != np.uint8:
            raise ValueError('输入必须为配置大小的uint8 RGB图像')
        self.new_results = []
        self.advance(tick)
        self.last_input_tick = tick
        frame_id, index = self.frame_id, self.frame_id & 1
        self.frame_id += 1
        bank = self.banks[index]
        reason, captured = 'WAIT WINDOW', False
        if bank.busy:
            reason = 'BANK OVERRUN'
        elif self.window is not None:
            ox, oy, source_id = self.window
            patch = rgb[oy:oy+256, ox:ox+256].astype(np.uint16)
            gray = (patch[..., 0]+2*patch[..., 1]+patch[..., 2]) >> 2
            sums = gray[0::2, 0::2]+gray[0::2, 1::2]+gray[1::2, 0::2]+gray[1::2, 1::2]
            bank.gray[:] = ((sums+2) >> 2).astype(np.uint8)
            bank.busy, bank.frame_id, bank.epoch, bank.tick = True, frame_id, self.epoch, tick
            bank.origin, bank.window_source = (ox, oy), source_id
            bank.ready_tick = tick+self.period*(oy+256)//self.cfg.height
            captured = True
        mask = segment(rgb, self.cfg)
        stats = self.store.scan(self.store.capture(mask, frame_id, self.epoch), mask)
        stats = replace(stats, mask=None)  # 事件只保留组件元数据，不缓存整帧RGB/掩膜。
        due = tick+self.period*self.cfg.roi[3]//self.cfg.height+self.color_cycles
        self._event(due, 'color', (stats, tick, index if captured else -1, reason))
        return self.latest

    def _color_done(self, when, stats, tick, bank_index, fallback_reason):
        if stats.epoch != self.epoch:
            return
        acquiring = self.tracker.target is None
        if stats.overflow:
            self.tracker.reset()
        else:
            self.tracker.update(stats.candidates)
        observed = self.tracker.observed if self.tracker.state in ('CONFIRM', 'TRACK') else None
        if observed is not None:
            if acquiring:
                self.ball_id += 1
            # PRED只决定未来采集窗，当前测角使用observed。
            x, y = self.tracker.target.center
            ox = max(0, min((self.cfg.width-256)//4*4, (x-128)//4*4))
            oy = max(0, min((self.cfg.height-256)//2*2, (y-128)//2*2))
            self.window = ox, oy, stats.frame_id
        elif self.tracker.target is None:
            self.window = None
        result = Measurement(stats.frame_id, stats.epoch, tick, self.ball_id,
                             reason=fallback_reason, done_tick=when, bank_index=bank_index)
        if observed is None:
            result.reason = 'COLOR COMPONENT OVERFLOW' if stats.overflow else 'NO MEASURED BALL'
        if bank_index >= 0:
            bank = self.banks[bank_index]
            if observed is not None:
                result = extract_marker(bank, observed, result, self.cfg)
            duration = self.marker_cycles if self.marker_cycles is not None else max(1, result.cycles)
            start = max(when, bank.ready_tick, self.engine_free)
            result.done_tick = start+duration
            self.engine_free = result.done_tick
            self._event(result.done_tick, 'marker', result)
        else:
            self.completed[result.frame_id] = result

    def flush(self):
        self.new_results = []
        while self.events:
            self.advance(self.events[0][0])
        return self.new_results


def annotate_model(rgb, model, result):
    image = rgb.copy()
    if result is not None and result.origin:
        ox, oy = result.origin
        cv2.rectangle(image, (ox, oy), (ox+255, oy+255), (70, 190, 235), 1)
    if result is not None and result.box:
        x0, y0, x1, y1 = result.box
        cv2.rectangle(image, (x0, y0), (x1, y1), (240, 100, 100), 2)
        center = tuple(round(v/16) for v in result.center_q4)
        cv2.drawMarker(image, center, (255, 255, 255), cv2.MARKER_CROSS, 12)
        if result.marker_q4:
            marker = tuple(round(v/16) for v in result.marker_q4)
            cv2.line(image, center, marker, (255, 230, 80), 2)
            cv2.circle(image, marker, 8, (255, 230, 80), 2)
    image[:144] = (13, 24, 37)
    if result is None:
        lines = ('RTL STRUCTURE MODEL / WARMUP', 'WAIT SOURCE-FRAME MATCH',
                 '256x256 WINDOW -> 128x128 GRAY x 2 BANKS', 'FUNCTIONAL + INTEGER + EVENT MODEL / NOT RTL SIMULATION')
    else:
        rpm = '--' if result.rpm_x10 is None else f'{abs(result.rpm_x10)/10:05.1f}'
        angle = '--' if result.angle is None else f'{result.angle*360/TURN:06.1f}'
        lines = (f'RTL STRUCTURE MODEL  ID={result.ball_id}  {result.state}  RPM={rpm}  ANGLE={angle}',
                 f'NET={result.net_phase/TURN:+.3f}rev  CW={result.cw}  CCW={result.ccw}  {"PARTIAL" if result.partial else "OBSERVED"}',
                 f'SRC={result.frame_id} WIN_SRC={result.window_source} BANK={result.bank_index} MED={result.median} TH={result.threshold} {result.reason}',
                 'MEASURED BOX / FIXED-POINT CORDIC / EVENT LATENCY ASSUMPTIONS / [C] CLEAR [Q] EXIT')
    for index, line in enumerate(lines):
        text(image, line, (16, 27+index*32), scale=0.57, color=(228, 237, 245))
    if result is not None and result.gray is not None:
        gray = np.repeat(result.gray[..., None], 3, axis=2)
        mask = np.repeat((result.dark.astype(np.uint8)*255)[..., None], 3, axis=2)
        image[160:288, 16:144] = gray
        image[320:448, 16:144] = mask
        text(image, 'GRAY / MASK', (16, 155), scale=0.4)
    return image


def trace_row(result):
    return {'frame': result.frame_id, 'epoch': result.epoch, 'capture_ticks': result.tick,
            'done_ticks': result.done_tick, 'latency_ms': (result.done_tick-result.tick)*1000/CLOCK_HZ,
            'bank': result.bank_index, 'window_source_frame': result.window_source,
            'ball_id': result.ball_id, 'center_q4': result.center_q4, 'marker_q4': result.marker_q4,
            'phase_u16': result.angle, 'angle_deg': None if result.angle is None else result.angle*360/TURN,
            'signed_rpm': None if result.rpm_x10 is None else result.rpm_x10/10,
            'net_rev': result.net_phase/TURN, 'cw': result.cw, 'ccw': result.ccw,
            'state': result.state, 'reason': result.reason, 'partial': result.partial,
            'counter_saturated': result.counter_saturated,
            'median': result.median, 'threshold': result.threshold, 'service_budget_cycles': result.cycles}


def run(args):
    folder = Path(args.output)
    folder.mkdir(parents=True, exist_ok=True)
    capture = None
    fps, live = args.fps, args.source.isdecimal()
    if args.source != 'demo':
        capture = cv2.VideoCapture(int(args.source) if live else args.source)
        if not capture.isOpened():
            capture.release()
            raise RuntimeError('无法打开视频输入')
        if not live:
            reported = capture.get(cv2.CAP_PROP_FPS)
            if math.isfinite(reported) and reported > 0:
                fps = reported
    model = RotationHardwareModel(fps=fps)
    reference = {}
    rows, errors, angle_errors, float_errors = [], [], [], []
    floating_measurements = {}
    float_engine = None
    if args.compare:
        from rotation import RotationPipeline
        float_engine = RotationPipeline()
    writers = []
    clock_start, index, paused = time.perf_counter(), 0, False
    limit = args.frames or (720 if args.headless and (capture is None or live) else 0)
    title = 'Ball rotation RTL structure model'
    shown = None

    def collect(results):
        for result in results:
            row = trace_row(result)
            truth = reference.get(result.frame_id)
            row['reference_rpm_demo_only'] = None if truth is None else truth[1]
            rows.append(row)
            if truth is not None:
                phase, expected_rpm, stamp = truth
                if result.angle is not None:
                    error = (result.angle*360/TURN-phase+180) % 360-180
                    angle_errors.append(abs(error))
                if result.rpm_x10 is not None and min(abs(stamp % 12-b) for b in (0, 3, 4.5, 8, 12)) > 0.5:
                    errors.append(abs(result.rpm_x10/10-expected_rpm))
            if result.frame_id == round(2*fps) and result.gray is not None:
                save_png(folder/'02_cached_gray.png', np.repeat(result.gray[..., None], 3, axis=2))
                save_png(folder/'03_marker_mask.png', np.repeat((result.dark.astype(np.uint8)*255)[..., None], 3, axis=2))

    try:
        if args.headless or args.record:
            for name in ('rtl_rotation_input.mp4', 'rtl_rotation_result.mp4'):
                writer = cv2.VideoWriter(str(folder/name), cv2.VideoWriter_fourcc(*'mp4v'), fps, (1280, 720))
                writers.append(writer)
                if not writer.isOpened():
                    raise RuntimeError('无法创建视频编码器')
        if not args.headless:
            cv2.namedWindow(title, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(title, 1280, 720)
        while not limit or index < limit:
            began = time.perf_counter()
            if not paused:
                if capture is None:
                    stamp = index/fps
                    phase, rpm = demo_phase(stamp)
                    center = (640+150*math.sin(stamp*0.6), 420+22*math.sin(stamp*0.8))
                    rgb = render_ball(1280, 720, center, 76, phase, marker=not (5.40 <= stamp % 12 < 5.45), noise=2, seed=index)
                    reference[index] = phase, rpm, stamp
                else:
                    ok, bgr = capture.read()
                    if not ok:
                        break
                    rgb = fit_frame(bgr)
                    stamp = time.perf_counter()-clock_start if live else capture.get(cv2.CAP_PROP_POS_MSEC)/1000
                    last = model.last_input_tick
                    if not math.isfinite(stamp) or (last is not None and round(stamp*CLOCK_HZ) <= last):
                        stamp = max(index/fps, 0 if last is None else last/CLOCK_HZ+1/fps)
                model.step(rgb, stamp)
                collect(model.new_results)
                if float_engine is not None:
                    floating_observation = float_engine.step(rgb, stamp)
                    floating_measurements[index] = floating_observation.angle, float_engine.meter.rpm
                    # 对照算法也只接收RGB和时间；真值仅用于报告误差。
                    if capture is None and float_engine.meter.rpm is not None and min(abs(stamp % 12-b) for b in (0, 3, 4.5, 8, 12)) > 0.5:
                        float_errors.append(abs(float_engine.meter.rpm-reference[index][1]))
                shown = annotate_model(rgb, model, model.latest)
                if index == round(2*fps):
                    save_png(folder/'01_input.png', rgb)
                    save_png(folder/'04_output.png', shown)
                # 显示当前视频叠加最近已完成的旧帧测量；不得称为当前帧空间完全对齐。
                for writer, frame in zip(writers, (rgb, shown)):
                    writer.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
                index += 1
                if args.headless and index % 120 == 0:
                    print(f'frames={index} published={len(rows)} state={model.meter.state} rpm_x10={model.meter.rpm_x10}', flush=True)
            if not args.headless:
                if shown is not None:
                    cv2.imshow(title, cv2.cvtColor(shown, cv2.COLOR_RGB2BGR))
                key = cv2.waitKey(max(1, round(1000/fps-(time.perf_counter()-began)*1000))) & 255
                if key in (27, ord('q')) or cv2.getWindowProperty(title, cv2.WND_PROP_VISIBLE) < 1:
                    break
                if key == ord(' '):
                    paused = not paused
                elif key == ord('c'):
                    model.clear()
                    if float_engine is not None:
                        float_engine.clear()
        collect(model.flush())
    finally:
        for writer in writers:
            writer.release()
        if capture is not None:
            capture.release()
        if not args.headless:
            cv2.destroyAllWindows()
    if not index:
        raise RuntimeError('输入没有有效帧')
    for row in rows:
        float_angle, float_rpm = floating_measurements.get(row['frame'], (None, None))
        row['float_angle_deg'] = float_angle
        row['float_signed_rpm'] = float_rpm
        row['angle_delta_to_float_deg'] = (None if row['angle_deg'] is None or float_angle is None
                                           else (row['angle_deg']-float_angle+180) % 360-180)
    with (folder/'rtl_rotation_trace.csv').open('w', newline='', encoding='utf-8-sig') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]) if rows else ['frame'])
        writer.writeheader()
        writer.writerows(rows)
    save_png(folder/'last_display_frame.png', shown)
    summary = {'frames': index, 'published': len(rows), 'valid_angles': sum(row['phase_u16'] is not None for row in rows),
               'stable_rpm_samples': len(errors), 'stable_rpm_mae': float(np.mean(errors)) if errors else None,
               'stable_rpm_p95': float(np.percentile(errors, 95)) if errors else None,
               'angle_error_p95_deg': float(np.percentile(angle_errors, 95)) if angle_errors else None,
               'float_algorithm_stable_rpm_mae': float(np.mean(float_errors)) if float_errors else None,
               'final_net_rev': model.meter.net_phase/TURN, 'full_cw': model.meter.cw, 'full_ccw': model.meter.ccw,
               'partial': model.meter.partial, 'reasons': dict(model.counters),
               'max_latency_ms': max((row['latency_ms'] for row in rows), default=0),
               'elapsed_processing_seconds': round(time.perf_counter()-clock_start, 3), 'source': args.source,
               'input_timebase_fps': fps, 'gray_bank_bits': 128*128*8*2,
               'model': 'integer datapath + explicit dual-bank ownership + frame event scheduler; NOT RTL cycle simulation',
               'timing_assumptions': 'uniform rows per input period; color service=1035271 cycles; marker service=operation budget, not measured RTL',
               'physical_camera_validated': False, 'rtl_compiled_or_synthesized': False}
    (folder/'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False), flush=True)
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', default='demo')
    parser.add_argument('--headless', action='store_true')
    parser.add_argument('--record', action='store_true')
    parser.add_argument('--compare', action='store_true', help='同时运行原浮点算法作离线精度对照')
    parser.add_argument('--frames', type=int, default=0)
    parser.add_argument('--fps', type=float, default=60)
    parser.add_argument('--output', default=str(Path(__file__).parent/'output/rotation_rtl'))
    args = parser.parse_args()
    if args.frames < 0 or not math.isfinite(args.fps) or not 1 <= args.fps <= 240:
        parser.error('frames须非负；fps须在1～240之间')
    run(args)


if __name__ == '__main__':
    main()
