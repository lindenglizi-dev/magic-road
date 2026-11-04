from PySide6.QtWidgets import (QWidget,QVBoxLayout,QHBoxLayout,QPushButton,QComboBox,QLabel,QProgressBar,QFileDialog)
from services.image_converter import ImageLoadWorker
from services.image_uploader import ImageUploader
from communication.image_protocol import Capability

class UploadPanel(QWidget):
    def __init__(self,controller,view,log):
        super().__init__();self.controller=controller;self.view=view;self.log=log;self.loader=None;self.image=None
        self.uploader=ImageUploader(controller)
        layout=QVBoxLayout(self);row=QHBoxLayout();layout.addLayout(row)
        self.select=QPushButton('选择图片');self.fit=QComboBox();self.fit.addItem('保持比例并补黑边','letterbox');self.fit.addItem('居中裁剪适配','crop')
        self.upload=QPushButton('上传到FPGA');self.cancel=QPushButton('取消上传');self.cancel.setEnabled(False)
        for widget in (self.select,self.fit,self.upload,self.cancel):row.addWidget(widget)
        self.info=QLabel('尚未选择图片');self.info.setWordWrap(True);layout.addWidget(self.info)
        self.bar=QProgressBar();self.bar.setRange(0,1000);layout.addWidget(self.bar)
        self.state=QLabel('FPGA能力未确认，不能上传');layout.addWidget(self.state)
        self.rate=QLabel('进度：0 / 4147200 B；速率：—；剩余：—');layout.addWidget(self.rate)
        note=QLabel('目标1920×1080 RGB565，小端、逐行，无行填充。115200/8N1纯像素理论至少360秒，协议与确认会增加时间。\n'
                    '只有IMAGE_END经FPGA整帧校验并确认后才显示完成。上传期间算法/ROI普通请求暂停。\n'
                    'FPGA当前实际视频源尺寸以状态查询为准；上传1080P不代表HDMI一定输出1080P。')
        note.setWordWrap(True);layout.addWidget(note);layout.addStretch()
        self.select.clicked.connect(self.choose);self.upload.clicked.connect(self.start);self.cancel.clicked.connect(self.uploader.cancel)
        controller.device_changed.connect(lambda status:self.refresh())
        self.uploader.progress.connect(self.progress);self.uploader.state.connect(self.state.setText)
        self.uploader.busy_changed.connect(self.busy_changed);self.uploader.finished.connect(self.completed)
        self.refresh()

    def choose(self):
        if self.loader or self.uploader.busy:return
        path,_=QFileDialog.getOpenFileName(self,'选择本地图片','','图片 (*.png *.jpg *.jpeg *.bmp)')
        if not path:return
        self.select.setEnabled(False);self.loader=ImageLoadWorker(path,self.fit.currentData())
        self.loader.loaded.connect(self.loaded);self.loader.failed.connect(lambda msg:self.log('图片读取失败：'+msg))
        self.loader.finished.connect(self.load_finished);self.loader.start()

    def loaded(self,image):
        self.image=image;self.view.set_frame(image.preview)
        self.info.setText(f'{image.path}\n原始 {image.source_size[0]}×{image.source_size[1]}，文件 {image.file_bytes:,} B；'
                          f'目标1920×1080，RGB565 LE，传输 {len(image.data):,} B；CRC32={image.crc:08X}')

    def load_finished(self):
        worker=self.loader;self.loader=None
        if worker:worker.deleteLater()
        self.select.setEnabled(True);self.refresh()

    def refresh(self):
        device=self.controller.device
        self.upload.setEnabled(bool(self.image and device and device.capabilities&Capability.IMAGE_UPLOAD and not self.uploader.busy))
        if not self.uploader.busy:
            if not device:self.state.setText('FPGA能力未确认，不能上传')
            elif not device.capabilities&Capability.IMAGE_UPLOAD:self.state.setText('当前固件未提供图片上传能力')
            elif self.state.text() in ('FPGA能力未确认，不能上传','当前固件未提供图片上传能力'):
                self.state.setText('FPGA已确认图片上传能力；选择图片后可上传')

    def completed(self,ok,message):
        self.log('上传：'+message)
        if self.controller.serial.connected:
            try:self.controller.query_device()
            except RuntimeError as exc:self.log('上传后状态查询：'+str(exc))

    def start(self):
        try:self.uploader.start(self.image)
        except (RuntimeError,ValueError) as exc:self.log('上传：'+str(exc))

    def busy_changed(self,busy):
        self.select.setEnabled(not busy);self.fit.setEnabled(not busy);self.cancel.setEnabled(busy);self.refresh()

    def progress(self,done,total,rate,remaining):
        self.bar.setValue(done*1000//total)
        self.rate.setText(f'{done:,} / {total:,} B；{rate/1024:.2f} KiB/s；预计剩余 {remaining:.0f} 秒')
