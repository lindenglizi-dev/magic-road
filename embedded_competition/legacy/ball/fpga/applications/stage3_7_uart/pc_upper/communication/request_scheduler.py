"""One outstanding request over the existing SerialManager, GUI-thread timers.

Retries reuse the same packet/SEQ. The FPGA must deduplicate writes by transfer
ID/offset; the one-byte SEQ alone is not an image packet identity.
"""
from collections import deque
from dataclasses import dataclass
import time
from PySide6.QtCore import QObject,QTimer,Signal
from communication.protocol import Command,encode

@dataclass
class Request:
    command:int
    data:bytes
    callback:object
    owner:str='control'
    retries:int=3
    seq:int=0
    packet:bytes=b''
    sent_at:float=0.
    timeout:float=1.5

class RequestScheduler(QObject):
    log=Signal(str)
    def __init__(self,serial):
        super().__init__();self.serial=serial;self.queue=deque();self.active=None;self.seq=0;self.exclusive=None
        self.timer=QTimer(self);self.timer.setInterval(30);self.timer.timeout.connect(self._tick);self.timer.start()
        serial.state_changed.connect(self._connection)

    def lock(self,owner):
        if self.exclusive or self.active or self.queue:raise RuntimeError('串口正在处理其他请求，请稍后上传')
        self.exclusive=owner

    def unlock(self,owner):
        if self.exclusive==owner:self.exclusive=None

    def submit(self,command,data=b'',callback=None,owner='control',timeout=1.5,retries=3,priority=False):
        if not self.serial.connected:raise RuntimeError('串口未连接')
        if self.exclusive and owner!=self.exclusive:raise RuntimeError('图片传输占用串口；请完成或取消后再控制')
        if len(self.queue)>32:raise RuntimeError('控制任务队列已满')
        request=Request(int(command),bytes(data),callback,owner,retries,timeout=timeout)
        if priority:self.queue.appendleft(request)
        else:self.queue.append(request)
        self._next()

    def _next(self):
        if self.active or not self.queue or not self.serial.connected:return
        request=self.queue.popleft();request.seq=self.seq;self.seq=(self.seq+1)&255
        request.packet=encode(request.command,request.data,request.seq);self.active=request
        self._send()

    def _send(self):
        try:
            self.serial.send(self.active.packet);self.active.sent_at=time.monotonic()
        except (RuntimeError,ValueError) as exc:self._finish(False,b'',str(exc))

    def receive(self,frame):
        request=self.active
        if not request or frame.seq!=request.seq or frame.command not in (Command.ACK,Command.NACK):return False
        if len(frame.data)<2 or frame.data[0]!=request.command:return False
        code=frame.data[1]
        self._finish(frame.command==Command.ACK and code==0,frame.data[2:],'' if code==0 else f'FPGA错误码{code}')
        return True

    def _finish(self,ok,data,error):
        request=self.active;self.active=None
        if request and request.callback:request.callback(ok,data,error)
        self._next()

    def _tick(self):
        if self.active and time.monotonic()-self.active.sent_at>self.active.timeout:
            if self.active.retries:
                self.active.retries-=1;self.log.emit(f'超时重传 CMD=0x{self.active.command:02X} SEQ={self.active.seq}');self._send()
            else:self._finish(False,b'','FPGA响应超时；未确认执行')

    def clear_owner(self,owner):
        self.queue=deque(r for r in self.queue if r.owner!=owner)

    def _connection(self,state):
        if not self.serial.connected:
            active=self.active;queued=list(self.queue)
            self.active=None;self.queue.clear();self.exclusive=None
            for request in ([active] if active else [])+queued:
                if request.callback:request.callback(False,b'','串口已断开')
