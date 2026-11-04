"""UVC/HDMI acquisition only. No FPGA algorithms or image enlargement."""
from threading import Event, Lock
import time
import cv2
from PySide6.QtCore import QThread, Signal

class DeviceScanner(QThread):
    devices_found = Signal(object)
    def __init__(self, limit=8):
        super().__init__()
        self.limit = limit

    def run(self):
        found = []
        for index in range(self.limit):
            if self.isInterruptionRequested(): break
            capture = cv2.VideoCapture(index, cv2.CAP_DSHOW)
            try:
                if capture.isOpened():
                    found.append((index, f'视频设备 {index}（DirectShow）'))
            finally:
                capture.release()
        self.devices_found.emit(found)

class VideoCaptureWorker(QThread):
    frame_ready = Signal()
    stats = Signal(int, int, float)
    state = Signal(str)
    error = Signal(str)

    def __init__(self, device, requested_width=1920, requested_height=1080, fps=30, factory=None):
        super().__init__()
        self.device, self.width, self.height, self.fps = device, requested_width, requested_height, fps
        self.factory = factory or cv2.VideoCapture
        self.stop_event = Event()
        self.lock = Lock()
        self.latest = None
        self.notified = False

    def take_latest(self):
        with self.lock:
            self.notified = False
            return self.latest

    def snapshot(self):
        with self.lock:
            return self.latest

    def stop(self):
        self.stop_event.set()

    def run(self):
        cap = None
        try:
            self.state.emit('正在打开采集设备')
            cap = self.factory(self.device, cv2.CAP_DSHOW)
            if not cap.isOpened(): raise RuntimeError('无法打开采集设备；请检查设备索引及其他程序占用')
            cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            cap.set(cv2.CAP_PROP_FPS, self.fps)
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            self.state.emit('采集中；分辨率以实际视频帧为准')
            since = time.monotonic(); count = 0; failures = 0; shape = None
            while not self.stop_event.is_set():
                ok, frame = cap.read()
                if not ok or frame is None:
                    failures += 1
                    if failures >= 15: raise RuntimeError('视频信号中断或设备已断开；停止后可重新连接')
                    self.stop_event.wait(.03)
                    continue
                failures = 0
                frame = frame.copy()
                frame.setflags(write=False)
                height, width = frame.shape[:2]
                count += 1; now = time.monotonic()
                if shape != (width, height) or now-since >= 1:
                    measured = count/(now-since) if now-since >= .25 else 0.
                    self.stats.emit(width, height, measured)
                    if now-since >= 1: since = now; count = 0
                    shape = (width, height)
                with self.lock:
                    self.latest = frame
                    notify = not self.notified
                    self.notified = True
                if notify: self.frame_ready.emit()
        except (RuntimeError, cv2.error, OSError) as exc:
            self.error.emit(str(exc))
        finally:
            if cap is not None: cap.release()
            self.state.emit('预览已停止')
