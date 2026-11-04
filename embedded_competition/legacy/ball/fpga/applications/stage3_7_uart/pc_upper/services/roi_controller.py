from datetime import datetime
from PySide6.QtCore import QObject,Signal
from communication.protocol import Command
from communication.image_protocol import Capability,RoiConfig,RoiStatus

class RoiController(QObject):
    changed=Signal(object)
    state=Signal(str)
    log=Signal(str)
    def __init__(self,controller):
        super().__init__();self.controller=controller;self.applied=None;self.pending=None

    def apply(self,config):
        status=self.controller.device
        if not status or not status.capabilities&Capability.ROI:raise RuntimeError('FPGA尚未确认支持动态ROI')
        payload=config.encode(status.width,status.height);self.pending=config
        self.state.emit('ROI命令等待FPGA帧边界确认')
        def completed(ok,data,error):
            if not ok:self.pending=None;self.state.emit('ROI未确认：'+error);return
            if data!=payload:self.pending=None;self.state.emit('ROI确认参数不一致');return
            try:self.query()
            except RuntimeError as exc:self.state.emit('ROI确认后查询失败：'+str(exc))
        self.controller.scheduler.submit(Command.ROI_CONFIG,payload,completed)

    def query(self):
        def completed(ok,data,error):
            if not ok:self.state.emit('ROI查询失败：'+error);return
            try:self.receive(RoiStatus.decode(data))
            except ValueError as exc:self.state.emit(str(exc))
        self.controller.scheduler.submit(Command.ROI_QUERY,callback=completed)

    def receive(self,status):
        device=self.controller.device
        if not device:return
        status.config.roi.validate(device.width,device.height)
        self.applied=status
        if self.pending and status.config==self.pending:self.pending=None
        self.changed.emit(status)
        self.state.emit(f'FPGA已确认 ROI rev={status.revision} · {datetime.now():%H:%M:%S}')

    def reset(self):
        self.applied=None;self.pending=None;self.state.emit('ROI状态：未确认')
