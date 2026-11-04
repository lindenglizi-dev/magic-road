"""ACK-driven upload state machine on the shared nonblocking serial scheduler."""
import secrets,struct,time
from PySide6.QtCore import QObject,Signal
from communication.protocol import Command
from communication.image_protocol import Capability,IMAGE_BYTES,IMAGE_CHUNK,image_begin

class ImageUploader(QObject):
    progress=Signal(int,int,float,float)
    state=Signal(str)
    finished=Signal(bool,str)
    busy_changed=Signal(bool)
    def __init__(self,controller):
        super().__init__();self.controller=controller;self.busy=False;self.cancelled=False
        self.image=None;self.offset=0;self.transfer_id=0;self.started=0.;self.phase='idle'

    def start(self,image):
        device=self.controller.device
        if not device or not device.capabilities&Capability.IMAGE_UPLOAD:
            raise RuntimeError('FPGA未确认具有图片上传/DDR缓存能力')
        if self.busy:raise RuntimeError('已经在上传图片')
        if len(image.data)!=IMAGE_BYTES:raise ValueError('必须上传1920×1080 RGB565，共4147200字节')
        self.controller.scheduler.lock('image')
        self.image=image;self.offset=0;self.transfer_id=secrets.randbits(32) or 1
        self.busy=True;self.cancelled=False;self.end_sent=False;self.started=time.monotonic();self.phase='begin'
        self.busy_changed.emit(True);self.state.emit('等待FPGA接受图片描述')
        self._submit(Command.IMAGE_BEGIN,image_begin(self.transfer_id,image.crc),self._begin_ack)

    def _submit(self,command,data,callback):
        try:self.controller.scheduler.submit(command,data,callback,owner='image',timeout=2,retries=3)
        except (RuntimeError,ValueError) as exc:self._finish(False,str(exc))

    def _begin_ack(self,ok,data,error):
        if not self.busy:return
        if not ok:self._finish(False,'IMAGE_BEGIN未确认：'+error);return
        if data!=struct.pack('<I',self.transfer_id):
            self._finish(False,'IMAGE_BEGIN会话确认不一致');return
        if self.cancelled:self._abort();return
        self.phase='data';self._next()

    def _next(self):
        if self.cancelled:self._abort();return
        if self.offset==len(self.image.data):
            self.phase='end';self.end_sent=True;self.state.emit('全部分包已确认，等待FPGA整帧CRC和缓存提交')
            self._submit(Command.IMAGE_END,struct.pack('<II',self.transfer_id,self.image.crc),self._end_ack);return
        chunk=self.image.data[self.offset:self.offset+IMAGE_CHUNK]
        self.expected_offset=self.offset+len(chunk)
        self._submit(Command.IMAGE_DATA,struct.pack('<II',self.transfer_id,self.offset)+chunk,self._data_ack)

    def _data_ack(self,ok,data,error):
        if not self.busy:return
        if self.cancelled:self._abort();return
        if not ok:self._finish(False,'数据包未确认：'+error);return
        if len(data)!=8 or struct.unpack('<II',data)!=(self.transfer_id,self.expected_offset):
            self._finish(False,'FPGA数据包确认的会话/偏移不一致');return
        self.offset=self.expected_offset;elapsed=max(time.monotonic()-self.started,.001)
        rate=self.offset/elapsed;remaining=(len(self.image.data)-self.offset)/max(rate,1)
        self.progress.emit(self.offset,len(self.image.data),rate,remaining)
        self._next()

    def _end_ack(self,ok,data,error):
        if not self.busy:return
        if self.cancelled:self._abort();return
        if not ok:self._finish(False,'整帧未确认：'+error);return
        if len(data)!=8 or struct.unpack('<II',data)!=(self.transfer_id,self.image.crc):
            self._finish(False,'整帧CRC确认不一致');return
        self._finish(True,'FPGA已校验并提交完整图片，可切换PC Image')

    def cancel(self):
        if not self.busy:return
        self.cancelled=True;self.state.emit('正在取消，等待当前包边界/FPGA确认')
        active=self.controller.scheduler.active
        if active and active.owner=='image':active.retries=0;active.timeout=min(active.timeout,.4)
        else:self._abort()

    def _abort(self):
        if self.phase=='abort':return
        self.phase='abort'
        def completed(ok,data,error):
            confirmed=ok and data==struct.pack('<I',self.transfer_id)
            message='上传已停止（FPGA已确认）' if confirmed else '本地已停止；FPGA取消未确认：'+(error or '会话确认不一致')
            if self.end_sent:message+='；结束指令已发送，可能已提交图片，请读取FPGA状态'
            self._finish(False,message)
        self._submit(Command.IMAGE_ABORT,struct.pack('<I',self.transfer_id),completed)

    def _finish(self,ok,message):
        if not self.busy:return
        self.busy=False;self.phase='idle'
        self.controller.scheduler.clear_owner('image');self.controller.scheduler.unlock('image')
        self.busy_changed.emit(False);self.state.emit(message);self.finished.emit(ok,message)
