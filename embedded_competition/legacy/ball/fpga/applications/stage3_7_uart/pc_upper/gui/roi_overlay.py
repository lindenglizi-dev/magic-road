from PySide6.QtCore import Qt, Signal, QRectF, QPointF
from PySide6.QtGui import QImage, QPainter, QColor, QPen
from PySide6.QtWidgets import QWidget
from services.roi_geometry import RoiGeometry

class VideoView(QWidget):
    roi_selected = Signal(object)
    error = Signal(str)
    def __init__(self):
        super().__init__()
        self.setMinimumSize(320, 180)
        self.image = None; self.source_size = (1280, 720); self.content = None
        self.roi = None; self.selecting = False; self.start = None; self.end = None
        self.overlay_enabled = True; self.confirmed = False; self.result_text = '未确认'
        self.empty_text='等待 HDMI 采集视频'

    def set_frame(self, bgr):
        height, width = bgr.shape[:2]
        self.image = QImage(bgr.data, width, height, bgr.strides[0], QImage.Format.Format_BGR888).copy()
        self.update()

    def geometry_map(self):
        if self.image is None: raise ValueError('请先开始视频预览')
        return RoiGeometry((self.image.width(), self.image.height()), self.source_size,
                           (self.width(), self.height()), self.content)

    def paintEvent(self, event):
        p = QPainter(self); p.fillRect(self.rect(), QColor('#101820'))
        if self.image is None:
            p.setPen(QColor('#c0ccd8')); p.drawText(self.rect(), Qt.AlignCenter, self.empty_text)
            return
        mapping = self.geometry_map()
        p.drawImage(QRectF(*mapping.display), self.image)
        if self.overlay_enabled and self.roi and mapping.mapping_known:
            p.setPen(QPen(QColor('#00df8d' if self.confirmed else '#ffbf40'), 2))
            rect = QRectF(*mapping.display_roi(self.roi)); p.drawRect(rect)
            p.drawText(rect.topLeft()+QPointF(3, -5),
                       f'{self.roi.x0},{self.roi.y0} → {self.roi.x1},{self.roi.y1}  {self.result_text}')
        if self.start is not None and self.end is not None:
            p.setPen(QPen(QColor('#ffbf40'), 2, Qt.DashLine)); p.drawRect(QRectF(self.start, self.end).normalized())

    def mousePressEvent(self, event):
        if self.selecting and event.button() == Qt.LeftButton:
            try:
                mapping = self.geometry_map()
                if mapping.source_point(event.position().x(), event.position().y()) is not None:
                    self.start = event.position(); self.end = self.start
            except ValueError as exc: self.error.emit(str(exc))

    def mouseMoveEvent(self, event):
        if self.start is not None: self.end = event.position(); self.update()

    def mouseReleaseEvent(self, event):
        if self.start is None: return
        try:
            mapping = self.geometry_map()
            self.roi = mapping.select((self.start.x(), self.start.y()), (event.position().x(), event.position().y()))
            self.confirmed = False; self.result_text = '草稿，未发送'
            self.roi_selected.emit(self.roi)
        except ValueError as exc: self.error.emit(str(exc))
        finally:
            self.start = self.end = None; self.selecting = False; self.update()
