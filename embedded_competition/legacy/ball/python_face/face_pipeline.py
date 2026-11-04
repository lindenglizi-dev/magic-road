"""Keep the existing ball pipeline and add an independent Haar face branch."""
from dataclasses import dataclass
from pathlib import Path
import math
import sys
import time

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parent
BALL_SIM = ROOT.parent / 'python_sim'
if not BALL_SIM.is_dir():  # Staging verification uses the unchanged installed ball model.
    BALL_SIM = Path('E:/project/ball/python_sim')
sys.path.insert(0, str(BALL_SIM))
from pipeline import Pipeline, render, text
from scenes import demo_frame, draw_ball
from video_io import DDRFrameBuffer


@dataclass(frozen=True)
class FaceSnapshot:
    frame_id: int
    boxes: tuple
    milliseconds: float


class FaceDetector:
    def __init__(self, width=320, min_size=24):
        if width < 64 or min_size < 24:
            raise ValueError('Face width must be >=64; minimum window must be >=24')
        self.width, self.min_size = width, min_size
        self.cascade = cv2.CascadeClassifier(str(ROOT / 'assets/haarcascade_frontalface_default.xml'))
        if self.cascade.empty():
            raise RuntimeError('Cannot load the Haar cascade model')

    def detect(self, rgb, frame_id):
        if rgb.dtype != np.uint8 or rgb.ndim != 3 or rgb.shape[2] != 3:
            raise ValueError('Expected H x W x 3 uint8 RGB')
        start = time.perf_counter()
        height, width = rgb.shape[:2]
        reduced_width = min(width, self.width)
        reduced_height = max(1, round(height * reduced_width / width))
        gray = cv2.cvtColor(cv2.resize(rgb, (reduced_width, reduced_height),
                                      interpolation=cv2.INTER_AREA), cv2.COLOR_RGB2GRAY)
        found = self.cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5,
                                             minSize=(self.min_size, self.min_size))
        sx, sy = width / reduced_width, height / reduced_height
        boxes = tuple(sorted((max(0, math.floor(x*sx)), max(0, math.floor(y*sy)),
                              min(width-1, math.ceil((x+w)*sx)-1),
                              min(height-1, math.ceil((y+h)*sy)-1))
                             for x, y, w, h in found))
        return FaceSnapshot(frame_id, boxes, (time.perf_counter()-start)*1000)


class BallFacePipeline:
    def __init__(self, mode='count', face_every=2, face_width=320, min_face_size=24, face_gate=True):
        if face_every < 1:
            raise ValueError('face_every must be positive')
        self.ball = Pipeline(mode=mode)
        self.detector = FaceDetector(face_width, min_face_size)
        self.face_every = face_every
        self.faces = None
        self.last_face_ms = 0.0
        self.last_detection = None
        self.face_gate = face_gate
        self.unlocked = not face_gate
        self.face_hits = 0
        self.frame_id = -1
        self.unlock_frame = None

    def configure(self, **options):
        epoch = self.ball.epoch
        self.ball.configure(**options)
        if self.ball.epoch != epoch:
            self.faces = None
            self.face_hits = 0 if not self.unlocked else self.face_hits

    def reset(self):
        self.ball.configure(clear=True)
        self.ball.ddr = DDRFrameBuffer()  # Discard pre-reset frames and their OSD metadata.
        self.unlocked = not self.face_gate
        self.faces = None
        self.face_hits = 0
        self.unlock_frame = None
        self.last_face_ms = 0.0
        self.last_detection = None

    def process(self, rgb, mask_view=False):
        if rgb.shape != (self.ball.cfg.height, self.ball.cfg.width, 3) or rgb.dtype != np.uint8:
            raise ValueError('Input must match the ball pipeline resolution and uint8 RGB type')
        self.frame_id += 1
        ball_enabled = self.unlocked
        display_unlocked, display_hits = self.unlocked, self.face_hits
        display_ball, display_faces = self.ball.snapshot, self.faces
        stats = None
        self.last_face_ms = 0.0
        self.last_detection = None
        if not self.face_gate or not self.unlocked:
            if self.faces is None or self.frame_id % self.face_every == 0:
                self.faces = self.detector.detect(rgb, self.frame_id)
                self.last_detection = self.faces
                self.last_face_ms = self.faces.milliseconds
                if self.face_gate:
                    self.face_hits = self.face_hits+1 if self.faces.boxes else 0
                    if self.face_hits >= 3:
                        self.unlocked = True
                        self.unlock_frame = self.frame_id
                        self.ball.configure(clear=True)  # Counter starts in WAIT_CLEAR.
                        self.faces = None
        if ball_enabled:
            self.ball.frame_id = self.frame_id-1
            stats = self.ball.analyse(rgb)
            self.ball.accept(stats)
        mask = np.zeros(rgb.shape[:2], np.uint8) if stats is None else stats.mask
        painted = render(rgb, mask, display_ball, self.ball.cfg, self.ball.mode, mask_view and ball_enabled)
        if display_faces is not None:
            for left, top, right, bottom in display_faces.boxes:
                cv2.rectangle(painted, (left, top), (right, bottom), (0, 235, 255), 2)
                text(painted, 'FACE', (left, max(153, top-7)), (0, 235, 255), 0.55)
        # ponytail: skipped frames reuse boxes, no motion prediction; raise face rate if needed.
        count = 0 if display_faces is None else len(display_faces.boxes)
        age = '-' if display_faces is None else str(self.frame_id-display_faces.frame_id)
        cv2.rectangle(painted, (885, 77), (1279, 116), (14, 22, 34), -1)
        info = f'FACES {count} AGE {age} HAAR /{self.face_every}'
        if self.face_gate:
            info = 'FACE CHECK OFF' if display_unlocked else f'FACE CONFIRM {display_hits}/3'
            cv2.rectangle(painted, (0, 42), (880, 77), (14, 22, 34), -1)
            message = 'BALL ENABLED / R TO RELOCK' if display_unlocked else 'WAIT FACE / BALL DETECTION DISABLED'
            text(painted, message, (28, 65), (0, 235, 255), 0.6)
        text(painted, info, (895, 102),
             (0, 235, 255), 0.54)
        cv2.rectangle(painted, (0, 671), (1279, 700), (14, 22, 34), -1)
        text(painted, 'FACE CONFIRM x3 -> BALL ENABLE -> shared OSD -> RGB128 DDR -> HDMI' if self.face_gate else
             'RGB -> BALL + GRAY/HAAR -> shared OSD -> RGB128 DDR -> HDMI',
             (24, 689), scale=0.53)
        if self.face_gate:
            cv2.rectangle(painted, (0, 701), (1279, 719), (14, 22, 34), -1)
            text(painted, '1 Track  2 Count  M Mask  T Threshold  C Clear  R Relock  SPACE Pause  Q Quit',
                 (24, 713), (120, 143, 164), 0.43)
        hdmi, shown, words = self.ball.ddr.exchange(
            painted, (self.frame_id, display_ball, display_faces, display_unlocked, display_hits))
        return hdmi, stats, self.ball.snapshot, shown, words


class Demo:
    """Real photo pixels and simulated balls; no boxes are passed to the detector."""
    def __init__(self, color=False, face_gate=False):
        raw = np.fromfile(ROOT / 'assets/astronaut.png', dtype=np.uint8)
        image = cv2.imdecode(raw, cv2.IMREAD_COLOR)
        if image is None:
            raise RuntimeError('Cannot load the public-domain face test image')
        # Grayscale tile isolates branch integration from skin/ball color ambiguity.
        crop = cv2.resize(image[35:190, 145:295], (180, 180))
        self.tile = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB) if color else cv2.cvtColor(
            cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2RGB)
        self.face_gate = face_gate

    def frame(self, mode, index):
        rgb = demo_frame(mode, max(0, index-70) if self.face_gate else index)
        visible = 40 <= index < 64 if self.face_gate else index % 120 < 96
        if self.face_gate and index < 30:
            draw_ball(rgb, 450+index*16, 410, 1)  # A pre-unlock crossing must not count.
        if visible:
            x = 1000 if self.face_gate else 1000 + round(55 * math.sin(index * 0.055))
            rgb[180:360, x:x+180] = self.tile
        return rgb
