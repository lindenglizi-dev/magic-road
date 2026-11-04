"""Extend the existing control window; retain its serial widgets and algorithms."""
from pathlib import Path
from PySide6.QtCore import Qt, QTimer, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton,
    QLabel, QSplitter, QTabWidget, QFileDialog, QGroupBox, QScrollArea)
from gui.main_window import MainWindow
from gui.roi_overlay import VideoView
from services.settings_store import SettingsStore
from services.video_capture import DeviceScanner, VideoCaptureWorker
from services.screenshot_manager import ScreenshotWorker
from gui.roi_panel import RoiPanel
from communication.image_protocol import Capability
from gui.upload_panel import UploadPanel

class VisionWindow(MainWindow):
    def __init__(self, controller, config, auto_scan=True, settings=None):
        super().__init__(controller, config)
        self.settings = settings or SettingsStore()
        self.capture_worker = None; self.scanner = None; self.snapshot_worker = None
        self.latest_frame = None; self.closing_window = False
        self.setWindowTitle('FPGA Vision Control System — ' + config['profile'])
        self.resize(1280, 850)
        legacy = self.takeCentralWidget(); legacy_layout = legacy.layout()
        serial_layout = legacy_layout.takeAt(0).layout(); serial_layout.setParent(None)
        legacy_layout.removeWidget(self.status)
        root = QWidget(); self.setCentralWidget(root); layout = QVBoxLayout(root)
        layout.addLayout(serial_layout); layout.addWidget(self.status)
        row = QHBoxLayout(); layout.addLayout(row)
        self.video_devices = QComboBox(); self.video_devices.setEditable(True)
        self.video_devices.setMinimumWidth(210)
        self.scan_video = QPushButton('枚举采集设备'); self.preview_button = QPushButton('开始预览')
        self.capture_resolution = QComboBox()
        for width, height in ((1920,1080), (1280,720), (640,360)):
            self.capture_resolution.addItem(f'{width}×{height}', (width,height))
        saved_resolution=self.settings.get('capture_resolution',[1920,1080])
        if not isinstance(saved_resolution,(list,tuple)):saved_resolution=(1920,1080)
        for i in range(self.capture_resolution.count()):
            if tuple(self.capture_resolution.itemData(i))==tuple(saved_resolution):self.capture_resolution.setCurrentIndex(i)
        self.capture_stats = QLabel('实际采集：未开始；FPS：—')
        for widget in (QLabel('HDMI采集'),self.video_devices,self.scan_video,self.capture_resolution,self.preview_button,self.capture_stats):
            row.addWidget(widget)
        self.video_state = QLabel('采集尺寸由设备协商，以实际帧为准。FPGA源尺寸尚待读取，RTL基线1280×720。')
        layout.addWidget(self.video_state)
        split = QSplitter(Qt.Horizontal)
        live_group = QGroupBox('FPGA HDMI 实时预览 / ROI框选'); live_layout = QVBoxLayout(live_group)
        self.live_view = VideoView(); live_layout.addWidget(self.live_view)
        local_group = QGroupBox('PC 本地图片预览'); local_layout = QVBoxLayout(local_group)
        self.local_view = VideoView(); self.local_view.empty_text='请选择本地图片';local_layout.addWidget(self.local_view)
        split.addWidget(live_group); split.addWidget(local_group); split.setSizes([720,480])
        layout.addWidget(split, 3)
        self.source_row = QHBoxLayout(); layout.addLayout(self.source_row)
        self.source_select = QComboBox(); self.source_select.addItem('Camera',0);self.source_select.addItem('PC Image',1)
        self.source_select.setEnabled(False)
        self.source_status = QLabel('输入源：尚未收到FPGA确认')
        self.source_row.addWidget(QLabel('输入源'));self.source_row.addWidget(self.source_select);self.source_row.addWidget(self.source_status,1)
        self.tabs = QTabWidget(); layout.addWidget(self.tabs, 2)
        legacy_scroll=QScrollArea();legacy_scroll.setWidgetResizable(True);legacy_scroll.setWidget(legacy)
        self.tabs.addTab(legacy_scroll, '算法控制 / UART日志')
        self.roi_tab = RoiPanel(controller,self.live_view,self.append_log,self.settings); self.tabs.addTab(self.roi_tab,'ROI检测')
        self.upload_tab = UploadPanel(controller,self.local_view,self.append_log); self.tabs.addTab(self.upload_tab,'图片上传')
        self.upload_tab.uploader.busy_changed.connect(self.upload_busy)
        self.upload_tab.uploader.finished.connect(lambda *_:self.close() if self.closing_window else None)
        shot = QWidget(); shot_layout = QVBoxLayout(shot);shot_row=QHBoxLayout();shot_layout.addLayout(shot_row)
        self.screenshot_format = QComboBox();self.screenshot_format.addItems(['PNG','JPG','BMP'])
        self.screenshot_directory = Path(self.settings.get('screenshot_directory', str(Path(__file__).resolve().parents[1]/'screenshots')))
        self.directory_label = QLabel(str(self.screenshot_directory));self.directory_label.setWordWrap(True)
        self.shot_button = QPushButton('保存原始采集帧'); directory = QPushButton('设置截图目录');open_directory = QPushButton('打开目录')
        for widget in (self.shot_button,self.screenshot_format,directory,open_directory):shot_row.addWidget(widget)
        shot_layout.addWidget(self.directory_label)
        self.shot_status=QLabel('尚未截图；保存的是采集卡最新有效原始帧。');self.shot_status.setWordWrap(True)
        shot_layout.addWidget(self.shot_status);shot_layout.addStretch()
        self.tabs.addTab(shot,'截图管理')
        self.scan_video.clicked.connect(self.enumerate_video)
        self.preview_button.clicked.connect(self.toggle_preview)
        self.shot_button.clicked.connect(self.save_capture)
        directory.clicked.connect(self.choose_screenshot_directory)
        open_directory.clicked.connect(self.open_screenshot_directory)
        self.live_view.error.connect(lambda message:self.append_log('ROI：'+message))
        self.controller.serial.state_changed.connect(self._serial_state)
        self.query_status=QPushButton('读取FPGA状态');self.source_row.addWidget(self.query_status)
        self.query_status.clicked.connect(self.query_fpga)
        self.source_select.activated.connect(self.set_source)
        self.controller.device_changed.connect(self.device_status)
        if auto_scan: QTimer.singleShot(200,self.enumerate_video)

    def _serial_state(self, state):
        self.source_select.setEnabled(False)
        self.source_status.setText('输入源：尚未收到FPGA确认')
        if self.controller.serial.connected:QTimer.singleShot(80,self.query_fpga)

    def upload_busy(self,busy):
        for button in self.mode_buttons:button.setEnabled(self.controller.serial.connected and not busy)
        self.roi_tab.apply_button.setEnabled(bool(not busy and self.controller.device and self.controller.device.capabilities&Capability.ROI))
        self.roi_tab.read_button.setEnabled(self.roi_tab.apply_button.isEnabled())
        self.query_status.setEnabled(not busy)
        self.source_select.setEnabled(bool(not busy and self.controller.device and self.controller.device.capabilities&Capability.SOURCE_SWITCH))

    def query_fpga(self):
        try:self.controller.query_device()
        except RuntimeError as exc:self.append_log('FPGA查询：'+str(exc))

    def set_source(self,index):
        try:
            self.controller.select_source(self.source_select.itemData(index))
            self.source_status.setText('请求 '+self.source_select.itemText(index)+'；等待FPGA确认')
        except RuntimeError as exc:self.append_log('输入源：'+str(exc))

    def device_status(self,status):
        self.source_select.setEnabled(bool(status and status.capabilities&Capability.SOURCE_SWITCH))
        if status:
            self.live_view.source_size=(status.width,status.height)
            self.source_select.setCurrentIndex(status.source)
            self.source_status.setText(f"FPGA已确认：{'Camera' if status.source==0 else 'PC Image'} · {status.width}×{status.height}")
            item=next((item for item in self.controller.modes.values() if item['command']==status.mode),None)
            if item:self.description.setText(self.mode_description(item))
        else:self.source_status.setText('输入源：尚未收到FPGA确认')

    def enumerate_video(self):
        if self.scanner is not None or self.capture_worker is not None:return
        self.scan_video.setEnabled(False);self.scanner=DeviceScanner()
        self.scanner.devices_found.connect(self._devices)
        self.scanner.finished.connect(self._scan_finished);self.scanner.start()

    def _devices(self, devices):
        self.video_devices.clear()
        for index,name in devices:self.video_devices.addItem(name,index)
        saved=self.video_devices.findData(self.settings.get('video_device',0))
        if saved>=0:self.video_devices.setCurrentIndex(saved)
        if not devices:
            self.video_devices.setEditText(str(self.settings.get('video_device',0)))
            self.append_log('视频：未枚举到设备，可手动输入索引后重试；尚未确认HDMI硬件')

    def _scan_finished(self):
        worker=self.scanner;self.scanner=None
        if worker:worker.deleteLater()
        self.scan_video.setEnabled(self.capture_worker is None)
        if self.closing_window:self.close()

    def toggle_preview(self):
        if self.capture_worker:
            self.capture_worker.stop();self.preview_button.setEnabled(False);return
        text=self.video_devices.currentText().strip()
        try:
            device=self.video_devices.currentData() if text==self.video_devices.itemText(self.video_devices.currentIndex()) else int(text)
            if device is None:device=int(text)
        except ValueError:
            self.append_log('视频：请输入有效设备索引');return
        width,height=self.capture_resolution.currentData()
        self.capture_worker=VideoCaptureWorker(device,width,height)
        self.capture_worker.frame_ready.connect(self._frame)
        self.capture_worker.stats.connect(self._capture_stats)
        self.capture_worker.state.connect(self.video_state.setText)
        self.capture_worker.error.connect(lambda message:self.append_log('视频：'+message))
        self.capture_worker.finished.connect(self._capture_finished)
        self.latest_frame=None
        self.preview_button.setText('停止预览');self.scan_video.setEnabled(False)
        self.video_devices.setEnabled(False);self.capture_resolution.setEnabled(False)
        self.save_setting('video_device',device);self.save_setting('capture_resolution',[width,height]);self.capture_worker.start()

    def _frame(self):
        if self.capture_worker:
            frame=self.capture_worker.take_latest()
            if frame is not None:
                self.latest_frame=frame;self.live_view.set_frame(frame)

    def _capture_stats(self,width,height,fps):
        self.capture_stats.setText(f'实际采集：{width}×{height}；FPS：{fps:.1f}')

    def _capture_finished(self):
        worker=self.capture_worker;self.capture_worker=None
        if worker:worker.deleteLater()
        self.preview_button.setText('开始预览');self.preview_button.setEnabled(True)
        self.video_devices.setEnabled(True);self.capture_resolution.setEnabled(True);self.scan_video.setEnabled(True)
        if self.closing_window:self.close()

    def choose_screenshot_directory(self):
        path=QFileDialog.getExistingDirectory(self,'截图目录',str(self.screenshot_directory))
        if path:
            self.screenshot_directory=Path(path);self.directory_label.setText(path)
            self.save_setting('screenshot_directory',path)

    def save_setting(self,key,value):
        try:self.settings.set(key,value)
        except OSError as exc:self.append_log('配置保存失败：'+str(exc))

    def open_screenshot_directory(self):
        try:
            self.screenshot_directory.mkdir(parents=True,exist_ok=True)
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(self.screenshot_directory)))
        except OSError as exc:self.append_log('截图：'+str(exc))

    def save_capture(self):
        if self.snapshot_worker:return
        frame=self.capture_worker.snapshot() if self.capture_worker else self.latest_frame
        if frame is None:self.screenshot_message('截图失败：尚无有效采集帧');return
        self.snapshot_worker=ScreenshotWorker(frame,self.screenshot_directory,self.screenshot_format.currentText().lower())
        self.snapshot_worker.saved.connect(lambda path:self.screenshot_message('截图已保存：'+path))
        self.snapshot_worker.failed.connect(lambda message:self.screenshot_message('截图失败：'+message))
        self.snapshot_worker.finished.connect(self._screenshot_finished);self.shot_button.setEnabled(False)
        self.snapshot_worker.start()

    def screenshot_message(self,message):
        self.shot_status.setText(message);self.append_log(message)

    def _screenshot_finished(self):
        worker=self.snapshot_worker;self.snapshot_worker=None
        if worker:worker.deleteLater()
        self.shot_button.setEnabled(True)
        if self.closing_window:self.close()

    def closeEvent(self,event):
        self.closing_window=True
        pending=False
        if self.upload_tab.uploader.busy:
            self.upload_tab.uploader.cancel()
            pending=True
        if self.upload_tab.loader:
            if not getattr(self.upload_tab.loader,'window_close_hook',False):
                self.upload_tab.loader.finished.connect(self.close)
                self.upload_tab.loader.window_close_hook=True
            pending=True
        if self.capture_worker:self.capture_worker.stop();pending=True
        if self.scanner:self.scanner.requestInterruption();pending=True
        if self.snapshot_worker:pending=True
        if pending:event.ignore();return
        super().closeEvent(event)
