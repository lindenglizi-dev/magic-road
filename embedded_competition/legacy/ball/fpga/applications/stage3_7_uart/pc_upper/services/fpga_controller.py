from PySide6.QtCore import QObject, Signal
from communication.serial_manager import SerialManager
from communication.protocol import Command, Decoder, encode
from communication.request_scheduler import RequestScheduler
from communication.image_protocol import DeviceStatus,Capability,RoiStatus
from services.roi_controller import RoiController

class FpgaController(QObject):
    log = Signal(str)
    request_changed = Signal(str)
    device_changed = Signal(object)

    def __init__(self, config):
        super().__init__()
        self.serial = SerialManager()
        self.modes = {item['id']: item for item in config['modes']}
        self.seq = 0
        self.decoder = Decoder()
        self.device = None
        self.scheduler = RequestScheduler(self.serial)
        self.scheduler.log.connect(self.log)
        self.roi = RoiController(self)
        self.roi.log.connect(self.log)
        self.serial.received.connect(self._receive)
        self.serial.transmitted.connect(lambda data: self.log.emit('TX ' + data.hex(' ').upper()))
        self.serial.error.connect(lambda message: self.log.emit('错误：' + message))
        self.serial.state_changed.connect(self._state)

    def _state(self, state):
        self.decoder = Decoder()
        self.device = None
        self.device_changed.emit(None)
        self.roi.reset()
        self.request_changed.emit('尚未发送；FPGA 当前模式未确认')
        self.log.emit(state)

    def set_mode(self, mode_id):
        item = self.modes[mode_id]
        if self.device and self.device.capabilities & Capability.MODE_ACK:
            def completed(ok,data,error):
                confirmed=ok and data==bytes([item['command']])
                self.request_changed.emit(f"FPGA已确认：{item['name']}" if confirmed else '算法模式未确认：'+(error or '返回mode不一致'))
            self.scheduler.submit(Command.MODE,bytes([item['command']]),completed)
            self.request_changed.emit(f"请求：{item['name']}；等待FPGA确认")
            return
        if self.scheduler.exclusive:raise RuntimeError('图片上传占用串口')
        payload = encode(Command.MODE, bytes([item['command']]), self.seq)
        self.serial.send(payload)
        self.seq = (self.seq + 1) & 255
        self.request_changed.emit(f"请求：{item['name']}（mode={item['command']}）；已排队，实际模式请查看 HDMI")

    def _receive(self, data):
        self.log.emit('RX ' + data.hex(' ').upper())
        for frame in self.decoder.feed(data):
            if self.scheduler.receive(frame):continue
            if frame.command==Command.ROI_STATUS:
                try:self.roi.receive(RoiStatus.decode(frame.data))
                except ValueError as exc:self.log.emit('ROI状态错误：'+str(exc))
            else:self.log.emit(f'收到协议帧 seq={frame.seq} cmd=0x{frame.command:02X}')

    def query_device(self):
        def completed(ok,data,error):
            if not ok:self.log.emit('固件能力未确认：'+error);return
            try:
                self.device=DeviceStatus.decode(data)
                self.device_changed.emit(self.device)
                current=next((item['name'] for item in self.modes.values() if item['command']==self.device.mode),str(self.device.mode))
                self.request_changed.emit('FPGA当前模式：'+current)
                self.log.emit(f'FPGA已响应：源{self.device.width}×{self.device.height}，能力0x{self.device.capabilities:X}')
            except ValueError as exc:self.log.emit(str(exc))
        self.scheduler.submit(Command.GET_STATUS,callback=completed,timeout=.8,retries=1)

    def select_source(self,source):
        if not self.device or not self.device.capabilities&Capability.SOURCE_SWITCH:
            raise RuntimeError('固件未确认支持Camera/PC Image切换')
        def completed(ok,data,error):
            if not ok or data!=bytes([source]):self.log.emit('输入源未确认：'+(error or '返回源不一致'))
            if self.serial.connected:self.query_device()
        self.scheduler.submit(Command.SOURCE_SELECT,bytes([source]),completed,timeout=3)
