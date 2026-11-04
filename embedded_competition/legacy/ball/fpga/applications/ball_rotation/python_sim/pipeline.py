"""小球工程逐帧功能模型：实际RGB输入，不接收场景中的球坐标或身份。"""

from collections import deque
from dataclasses import dataclass, replace

import cv2
import numpy as np

from video_io import DDRFrameBuffer

NAMES = {0: 'UNKNOWN', 1: 'RED', 2: 'YELLOW', 3: 'GREEN'}
COLORS = {0: (145, 151, 160), 1: (255, 86, 98), 2: (255, 217, 68), 3: (64, 229, 153)}


@dataclass(frozen=True)
class Config:
    width: int = 1280
    height: int = 720
    roi: tuple = (64, 160, 1216, 640)
    gate: tuple = (544, 160, 736, 640)
    line: int = 640
    hysteresis: int = 16
    strict: bool = False
    min_area: int = 128
    min_size: int = 12
    max_size: int = 384
    max_candidates: int = 8
    max_move: int = 64
    clear_frames: int = 3
    confirm_frames: int = 2
    min_gate_pixels: int = 8
    component_queue_depth: int = 4096

    def __post_init__(self):
        x0, y0, x1, y1 = self.roi
        gx0, gy0, gx1, gy1 = self.gate
        if not 0 < self.width <= 4095 or self.width % 16 or not 0 < self.height <= 4095:
            raise ValueError('宽度必须为16的倍数，高度必须为正')
        if not (0 <= x0 < x1 <= self.width and 0 <= y0 < y1 <= self.height):
            raise ValueError('ROI越界')
        if not (x0 <= gx0 < self.line-self.hysteresis < self.line+self.hysteresis < gx1 <= x1
                and y0 <= gy0 < gy1 <= y1):
            raise ValueError('计数门及迟滞区必须完整位于ROI内')
        positive = (self.min_area, self.min_size, self.max_size,
                    self.max_candidates, self.max_move, self.clear_frames,
                    self.confirm_frames, self.min_gate_pixels, self.component_queue_depth)
        if min(positive) < 1 or self.min_size > self.max_size:
            raise ValueError('检测参数无效')


@dataclass(frozen=True)
class Detection:
    box: tuple
    color: int
    area: int

    @property
    def center(self):
        x0, y0, x1, y1 = self.box
        return (x0+x1)//2, (y0+y1)//2


@dataclass(frozen=True)
class FrameStats:
    frame_id: int
    epoch: int
    candidates: tuple
    raw_gate_pixels: int
    overflow: bool
    mask: np.ndarray
    diagnostic: tuple = (0, 0, 0, 0, 0, 0)
    gate_region_occupied: bool = False


def segment(rgb, cfg):
    if rgb.shape != (cfg.height, cfg.width, 3) or rgb.dtype != np.uint8:
        raise ValueError('输入尺寸或类型错误，应为配置尺寸的uint8 RGB帧')
    x0, y0, x1, y1 = cfg.roi
    r, g, b = np.moveaxis(rgb[y0:y1, x0:x1].astype(np.int16), -1, 0)
    if cfg.strict:
        yellow = ((r >= 150) & (g >= 150) & (r > b+50) & (g > b+50)
                  & (r+60 >= g) & (g+60 >= r))
        red = (r >= 150) & (r > g+50) & (r > b+50) & ~yellow
        green = (g >= 150) & (g > r+50) & (g > b+50) & ~yellow & ~red
    else:
        # 与RTL普通档一致；这里的RGB为Gamma之后的检测输入。
        yellow = ((r >= 64) & (g >= 64) & (r > b+12) & (g > b+12)
                  & (4*r > 5*b) & (4*g > 5*b) & (4*r <= 5*g) & (4*g <= 5*r))
        red = (r >= 64) & (r > g+12) & (r > b+12) & (4*r > 5*g) & (4*r > 5*b) & ~yellow
        green = ((g >= 64) & (g > r+12) & (g > b+12) & (4*g > 5*r)
                 & (4*g > 5*b) & ~yellow & ~red)
        # 暗部候选降低绝对门限；同组至少三像素同色才接受。
        weak_yellow = ((r >= 32) & (g >= 32) & (r > b+6) & (g > b+6)
                       & (8*r > 9*b) & (8*g > 9*b) & (4*r <= 5*g) & (4*g <= 5*r))
        weak_red = ((r >= 32) & (r > g+6) & (r > b+6)
                    & (8*r > 9*g) & (8*r > 9*b) & ~weak_yellow)
        weak_green = ((g >= 32) & (g > r+6) & (g > b+6)
                      & (8*g > 9*r) & (8*g > 9*b) & ~weak_yellow & ~weak_red)
    mask = np.zeros((cfg.height, cfg.width), np.uint8)
    mask[y0:y1, x0:x1] = red.astype(np.uint8) + yellow*2 + green*3
    if not cfg.strict:
        weak = np.zeros_like(mask)
        weak[y0:y1, x0:x1] = weak_red.astype(np.uint8) + weak_yellow*2 + weak_green*3
        strong_groups = mask.reshape(cfg.height, cfg.width//4, 4)
        weak_groups = weak.reshape(cfg.height, cfg.width//4, 4)
        supported_strong = np.zeros_like(strong_groups)
        supported_weak = np.zeros_like(weak_groups)
        for color in (1, 2, 3):
            strong_hit = strong_groups == color
            weak_hit = weak_groups == color
            supported_strong[strong_hit & (strong_hit.sum(axis=2, keepdims=True) >= 2)] = color
            supported_weak[weak_hit & (weak_hit.sum(axis=2, keepdims=True) >= 3)] = color
        # ponytail: 水平四像素支持只抑制稀疏噪点，密集背景需后续二维分离。
        mask = np.where(supported_strong != 0, supported_strong, supported_weak).reshape(mask.shape)
    return mask


class ComponentRAM:
    """双帧4x4单元和有界四邻域队列；不模拟RAM时钟。"""

    def __init__(self, cfg):
        self.cfg = cfg
        x0, y0, x1, y1 = cfg.roi
        self.origin = (x0//4*4, y0//4*4)
        self.banks = np.zeros((2, (y1+3)//4-y0//4, (x1+3)//4-x0//4), np.uint8)
        self.tags = [None, None]
        self.write_bank = 0

    def capture(self, mask, frame_id, epoch):
        cfg = self.cfg
        bank = self.write_bank
        gh, gw = self.banks.shape[1:]
        ox, oy = self.origin
        padded = np.zeros((gh*4, gw*4), np.uint8)
        h, w = min(cfg.height-oy, gh*4), min(cfg.width-ox, gw*4)
        padded[:h, :w] = mask[oy:oy+h, ox:ox+w]
        counts = np.stack([(padded == color).reshape(gh, 4, gw, 4).sum(axis=(1, 3))
                           for color in (1, 2, 3)], axis=-1)
        winners = counts.argmax(axis=2)
        areas = counts.max(axis=2)
        keep = (areas >= 4) & (areas*4 >= counts.sum(axis=2)*3)
        self.banks[bank] = np.where(keep, ((winners+1) << 5) | areas, 0).astype(np.uint8)
        self.tags[bank] = (frame_id, epoch)
        self.write_bank = 1-bank
        return bank

    def scan(self, bank, mask):
        cfg = self.cfg
        cells = self.banks[bank].copy()
        gh, gw = cells.shape
        ox, oy = self.origin
        candidates = []
        diagnostic = (0, 0, 0, 0, 0)
        overflow = False
        gate_region_occupied = False
        for address in range(gh*gw):
            sy, sx = divmod(address, gw)
            word = int(cells[sy, sx])
            if not word:
                continue
            color = word >> 5
            queue = deque([(sx, sy, word & 31)])
            cells[sy, sx] = 0
            left = right = sx
            top = bottom = sy
            area = 0
            while queue and not overflow:
                x, y, count = queue.popleft()
                area += count
                left, right = min(left, x), max(right, x)
                top, bottom = min(top, y), max(bottom, y)
                for nx, ny in ((x-1, y), (x+1, y), (x, y-1), (x, y+1)):
                    if not (0 <= nx < gw and 0 <= ny < gh):
                        continue
                    neighbor = int(cells[ny, nx])
                    if neighbor >> 5 != color:
                        continue
                    if len(queue) >= cfg.component_queue_depth:
                        overflow = True
                        break
                    cells[ny, nx] = 0
                    queue.append((nx, ny, neighbor & 31))
            if overflow:
                break
            x0, y0 = max(cfg.roi[0], ox+left*4), max(cfg.roi[1], oy+top*4)
            x1, y1 = min(cfg.roi[2]-1, ox+right*4+3), min(cfg.roi[3]-1, oy+bottom*4+3)
            width, height = x1-x0+1, y1-y0+1
            gx0, gy0, gx1, gy1 = cfg.gate
            # 形状筛选失败的较大连通区域仍可能是球，不能因此宣布空门。
            if area >= cfg.min_area and x0 < gx1 and x1 >= gx0 and y0 < gy1 and y1 >= gy0:
                gate_region_occupied = True
            rejected = (int(area < cfg.min_area)
                        | (int(not cfg.min_size <= width <= cfg.max_size
                               or not cfg.min_size <= height <= cfg.max_size) << 1)
                        | (int(width > 2*height or height > 2*width) << 2)
                        | (int(area*4 < width*height) << 3))
            if area > diagnostic[2]:
                diagnostic = (width, height, area, area*100//(width*height), rejected)
            if not rejected:
                if len(candidates) == cfg.max_candidates:
                    overflow = True
                    break
                candidates.append(Detection((x0, y0, x1, y1), color, area))
        gx0, gy0, gx1, gy1 = cfg.gate
        frame_id, epoch = self.tags[bank]
        return FrameStats(frame_id, epoch, tuple(candidates[:cfg.max_candidates]),
                          int(np.count_nonzero(mask[gy0:gy1, gx0:gx1])),
                          overflow, mask, (len(candidates), *diagnostic), gate_region_occupied)


class TargetTracker:
    def __init__(self, cfg):
        self.cfg = cfg
        self.reset()

    def reset(self):
        self.target = None
        self.observed = None
        self.velocity = (0, 0)
        self.state = 'SEARCH'
        self.misses = self.hits = 0
        self.color = self.color_hits = 0

    def update(self, candidates):
        target = None
        if self.target is None and candidates:
            target = max(candidates, key=lambda candidate: candidate.area)
        elif self.observed is not None:
            old = self.observed
            x, y = (c+v*(self.misses+1) for c, v in zip(old.center, self.velocity))
            limit = self.cfg.max_move * (2 if self.state == 'CONFIRM' else self.misses+1)
            width, height = old.box[2]-old.box[0]+1, old.box[3]-old.box[1]+1
            nearby = [d for d in candidates if d.color == old.color
                      and width <= 2*(d.box[2]-d.box[0]+1) <= 4*width
                      and height <= 2*(d.box[3]-d.box[1]+1) <= 4*height
                      and (max(abs(d.center[0]-x), abs(d.center[1]-y)) <= limit
                           or max(abs(a-b) for a, b in zip(d.center, old.center)) <= limit)]
            if nearby:
                target = min(nearby, key=lambda d: (max(abs(d.center[0]-x), abs(d.center[1]-y)) > limit,
                                                  abs(d.center[0]-x)+abs(d.center[1]-y)))
        if target is None:
            self.misses += 1
            if self.target is not None and self.misses < self.cfg.clear_frames:
                self.state = 'LOST'
            else:
                self.reset()
            return
        self.color_hits = self.color_hits+1 if target.color == self.color else 1
        self.color = target.color
        self.hits += 1
        if self.observed is None:
            self.velocity = (0, 0)
        elif self.misses == 0:
            ceiling = 2*self.cfg.max_move
            self.velocity = tuple(0 if abs(a-b) <= 4 else max(-ceiling, min(ceiling, a-b))
                                  for a, b in zip(target.center, self.observed.center))
        self.misses = 0
        self.observed = target
        x0, y0, x1, y1 = target.box
        rx0, ry0, rx1, ry1 = self.cfg.roi
        dx = max(rx0-x0, min(rx1-1-x1, self.velocity[0]))
        dy = max(ry0-y0, min(ry1-1-y1, self.velocity[1]))
        # ponytail: 一帧匀速补偿，急停可能超前一帧；漏检期间冻结，运动模糊需相机解决。
        self.target = Detection((x0+dx, y0+dy, x1+dx, y1+dy), target.color, target.area)
        self.state = 'TRACK' if self.color_hits >= self.cfg.confirm_frames else 'CONFIRM'


class GateCounter:
    MAX_COUNT = (1 << 32)-1

    def __init__(self, cfg):
        self.cfg = cfg
        self.counts = {1: 0, 2: 0, 3: 0}
        self.reset()

    def reset(self, clear_counts=False):
        if clear_counts:
            self.counts = {1: 0, 2: 0, 3: 0}
        self.state = 'WAIT_CLEAR'
        self.empty = self.hits = self.back_hits = 0
        self.locked_color = self.pending_color = 0
        self.event = 0
        self.reason = ''

    def block(self, reason):
        self.state, self.reason = 'BLOCKED', reason
        self.empty = self.hits = self.back_hits = self.event = 0

    def update(self, stats):
        cfg = self.cfg
        self.event = 0
        if stats.overflow:
            self.block('CANDIDATE OVERFLOW')
            return
        gx0, gy0, gx1, gy1 = cfg.gate
        inside = [d for d in stats.candidates if d.box[0] < gx1 and d.box[2] >= gx0
                  and d.box[1] < gy1 and d.box[3] >= gy0]
        occupied = (stats.gate_region_occupied and stats.raw_gate_pixels >= cfg.min_gate_pixels) or bool(inside)
        if not occupied:
            self.hits = self.back_hits = 0
            self.empty = min(self.empty+1, cfg.clear_frames)
            if self.empty >= cfg.clear_frames:
                self.state, self.reason = 'READY', ''
                self.locked_color = self.pending_color = 0
            return
        self.empty = 0
        if len(inside) > 1:
            self.block('MULTIPLE BALLS IN GATE')
            return
        if self.state in ('WAIT_CLEAR', 'BLOCKED') or not inside:
            self.hits = 0
            return
        target = inside[0]
        x, y = target.center
        if not gx0 <= x < gx1 or not gy0 <= y < gy1:
            self.hits = self.back_hits = 0
            return
        upstream, downstream = x <= cfg.line-cfg.hysteresis, x >= cfg.line+cfg.hysteresis
        if self.state in ('ARMED', 'HOLD') and target.color != self.locked_color:
            self.block('COLOR MISMATCH OR REVERSE MOTION')
            return
        if self.state == 'READY':
            if not upstream:
                self.block('NO UPSTREAM CONFIRMATION')
                return
            self.hits = self.hits+1 if target.color == self.pending_color else 1
            self.pending_color = target.color
            if self.hits >= cfg.confirm_frames:
                self.locked_color, self.state = target.color, 'ARMED'
        elif self.state == 'ARMED' and downstream:
            if self.counts[self.locked_color] < self.MAX_COUNT:
                self.counts[self.locked_color] += 1
                self.event = self.locked_color
            else:
                self.reason = 'COUNTER SATURATED'
            self.state = 'HOLD'
        elif self.state == 'HOLD':
            self.back_hits = self.back_hits+1 if upstream else 0
            if self.back_hits >= cfg.confirm_frames:
                self.block('GAP TOO SHORT OR REVERSE MOTION')


@dataclass(frozen=True)
class Snapshot:
    frame_id: int
    epoch: int
    candidates: tuple
    target: object
    tracker_state: str
    counts: tuple
    gate_state: str
    empty: int
    event: int
    reason: str
    diagnostic: tuple


def text(image, value, xy, color=(225, 232, 241), scale=0.6):
    cv2.putText(image, value, xy, cv2.FONT_HERSHEY_SIMPLEX, scale, color, 1, cv2.LINE_AA)


def render(rgb, mask, snapshot, cfg, mode, mask_view=False):
    image = rgb.copy()
    if mask_view:
        palette = np.array([COLORS[i] if i else (12, 18, 25) for i in range(4)], np.uint8)
        image = palette[mask]
    x0, y0, x1, y1 = cfg.roi
    cv2.rectangle(image, (x0, y0), (x1-1, y1-1), (109, 137, 161), 1)
    if mode == 'count':
        gx0, gy0, gx1, gy1 = cfg.gate
        tint = image[gy0:gy1, gx0:gx1]
        tint[:] = (tint.astype(np.uint16)*4+np.array((25, 44, 60), np.uint16))//5
        for x in (gx0, cfg.line-cfg.hysteresis, cfg.line+cfg.hysteresis, gx1-1):
            cv2.line(image, (x, gy0), (x, gy1-1), (83, 149, 186), 1)
        cv2.line(image, (cfg.line, gy0), (cfg.line, gy1-1), (217, 235, 247), 2)
        text(image, 'A', (gx0+8, gy0+22), scale=0.65)
        text(image, 'D', (gx1-25, gy0+22), scale=0.65)
    if snapshot is not None:
        targets = snapshot.candidates if mode == 'count' else (() if snapshot.target is None else (snapshot.target,))
        for target in targets:
            a, b, c, d = target.box
            color = COLORS[0 if mode == 'track' and snapshot.tracker_state == 'LOST' else target.color]
            cv2.rectangle(image, (max(0, a-5), max(0, b-5)),
                          (min(cfg.width-1, c+5), min(cfg.height-1, d+5)), color, 2)
            cx, cy = target.center
            cv2.drawMarker(image, (cx, cy), color, cv2.MARKER_CROSS, 15, 1)
            text(image, f'{NAMES[target.color]}  X={cx} Y={cy}', (max(4, a-4), max(150, b-14)), color, 0.48)
    cv2.rectangle(image, (0, 0), (cfg.width-1, 137), (14, 22, 34), -1)
    text(image, 'BALL VISION  /  PYTHON ENGINEERING SIMULATION', (28, 34), scale=0.78)
    text(image, 'SINGLE TARGET TRACKING' if mode == 'track' else 'LEFT-TO-RIGHT CONVEYOR COUNTING', (28, 65), (107, 179, 224), 0.6)
    if snapshot is not None:
        counts = dict(zip((1, 2, 3), snapshot.counts))
        if mode == 'count':
            for x, color in ((28, 1), (220, 3), (435, 2)):
                text(image, f'{NAMES[color]} {counts[color]:03d}', (x, 103), COLORS[color], 0.75)
            text(image, f'TOTAL {sum(snapshot.counts):03d}', (665, 103), (239, 243, 248), 0.8)
            text(image, f'GATE: {snapshot.gate_state}  EMPTY: {snapshot.empty}/3', (895, 65), scale=0.48)
        else:
            position = '--' if snapshot.target is None else f'X={snapshot.target.center[0]} Y={snapshot.target.center[1]}'
            text(image, f'{snapshot.tracker_state}    {position}', (28, 105), scale=0.8)
        if snapshot.reason:
            text(image, snapshot.reason, (885, 105), (255, 156, 99), 0.4)
        if snapshot.event:
            text(image, f'+1 {NAMES[snapshot.event]}', (900, 35), COLORS[snapshot.event], 0.75)
        number, width, height, area, fill, rejected = snapshot.diagnostic
        text(image, f'CCL4 N={number} W={width:04d} H={height:04d} A={area:07d} F={fill:03d}% R={rejected:X}',
             (28, 128), scale=0.45)
    cv2.rectangle(image, (0, cfg.height-49), (cfg.width-1, cfg.height-1), (14, 22, 34), -1)
    measured = '--' if snapshot is None else str(snapshot.frame_id)
    text(image, f'RGB pixels -> ROI -> color -> 2D regions -> tracking/count -> OSD -> DDR -> HDMI RGB | result frame {measured}',
         (24, cfg.height-26), scale=0.47)
    text(image, '1 Track   2 Count   M Mask   T Threshold   C Clear   SPACE Pause   Q Quit',
         (24, cfg.height-7), (120, 143, 164), 0.43)
    return image


class Pipeline:
    def __init__(self, cfg=Config(), mode='count'):
        if mode not in ('track', 'count'):
            raise ValueError('模式只能为track或count')
        self.cfg, self.mode = cfg, mode
        self.epoch = 0
        self.frame_id = self.last_accepted = -1
        self.components = ComponentRAM(cfg)
        self.tracker, self.counter = TargetTracker(cfg), GateCounter(cfg)
        self.ddr = DDRFrameBuffer()
        self.snapshot = None

    def configure(self, mode=None, strict=None, clear=False):
        new_mode = self.mode if mode is None else mode
        if new_mode not in ('track', 'count'):
            raise ValueError('无效模式')
        new_cfg = self.cfg if strict is None else replace(self.cfg, strict=strict)
        if new_mode == self.mode and new_cfg == self.cfg and not clear:
            return
        self.epoch += 1
        self.cfg, self.mode = new_cfg, new_mode
        self.components.cfg = self.tracker.cfg = self.counter.cfg = new_cfg
        self.counter.reset(clear_counts=clear)
        self.tracker.reset()
        self.snapshot = None

    def analyse(self, rgb):
        mask = segment(rgb, self.cfg)
        self.frame_id += 1
        bank = self.components.capture(mask, self.frame_id, self.epoch)
        return self.components.scan(bank, mask)

    def accept(self, stats):
        if stats.epoch != self.epoch or stats.frame_id <= self.last_accepted:
            return False
        self.last_accepted = stats.frame_id
        if self.mode == 'track':
            if stats.overflow:
                self.tracker.reset()
            else:
                self.tracker.update(stats.candidates)
        else:
            self.counter.update(stats)
        self.snapshot = Snapshot(stats.frame_id, stats.epoch, stats.candidates,
                                 self.tracker.target, self.tracker.state,
                                 tuple(self.counter.counts[c] for c in (1, 2, 3)),
                                 self.counter.state, self.counter.empty, self.counter.event,
                                 'DETECTOR OVERFLOW' if stats.overflow else self.counter.reason, stats.diagnostic)
        return True

    def process(self, rgb, mask_view=False):
        stats = self.analyse(rgb)
        display = self.snapshot  # 模型固定用上一完整检测帧叠加，避免同帧偷看结果。
        self.accept(stats)
        painted = render(rgb, stats.mask, display, self.cfg, self.mode, mask_view)
        hdmi, shown, words = self.ddr.exchange(painted, (stats.frame_id, display))
        return hdmi, stats, self.snapshot, shown, words
