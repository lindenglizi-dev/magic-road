from datetime import datetime
from pathlib import Path
import uuid
import cv2
from PySide6.QtCore import QThread, Signal

def save_screenshot(frame, directory, extension='png'):
    if frame is None: raise ValueError('尚无有效采集帧')
    extension = extension.lower().lstrip('.')
    if extension not in ('png', 'jpg', 'bmp'): raise ValueError('不支持的截图格式')
    directory = Path(directory); directory.mkdir(parents=True, exist_ok=True)
    path = directory/f'FPGA_{datetime.now():%Y%m%d_%H%M%S_%f}_{uuid.uuid4().hex[:6]}.{extension}'
    ok, encoded = cv2.imencode('.'+extension, frame)
    if not ok: raise OSError('截图编码失败')
    encoded.tofile(str(path))  # Unicode Windows paths; original capture frame only.
    return path

class ScreenshotWorker(QThread):
    saved = Signal(str)
    failed = Signal(str)
    def __init__(self, frame, directory, extension):
        super().__init__()
        self.frame, self.directory, self.extension = frame, directory, extension
    def run(self):
        try: self.saved.emit(str(save_screenshot(self.frame, self.directory, self.extension)))
        except (ValueError, OSError, cv2.error) as exc: self.failed.emit(str(exc))
