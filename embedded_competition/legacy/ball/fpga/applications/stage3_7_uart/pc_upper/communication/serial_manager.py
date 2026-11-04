"""The only module that imports pyserial. All I/O happens on a worker."""
from queue import Queue, Empty, Full
from threading import Event
from PySide6.QtCore import QObject, QThread, Signal
import serial
from serial.tools import list_ports

class SerialWorker(QThread):
    opened = Signal()
    received = Signal(bytes)
    transmitted = Signal(bytes)
    failed = Signal(str)

    def __init__(self, port, baud):
        super().__init__()
        self.port, self.baud = port, baud
        self.outbox = Queue(maxsize=64)
        self.stop_event = Event()

    def run(self):
        try:
            with serial.serial_for_url(self.port, baudrate=self.baud, timeout=0.02,
                                       write_timeout=0.25, rtscts=False, dsrdtr=False) as handle:
                self.opened.emit()
                while not self.stop_event.is_set():
                    try:
                        payload = self.outbox.get_nowait()
                    except Empty:
                        payload = None
                    if payload is not None:
                        if handle.write(payload) != len(payload):
                            raise serial.SerialTimeoutException('串口写入不完整')
                        self.transmitted.emit(payload)
                    incoming = handle.read(min(max(handle.in_waiting, 1), 4096))
                    if incoming:
                        self.received.emit(incoming)
        except (serial.SerialException, OSError, ValueError) as exc:
            self.failed.emit(str(exc))

class SerialManager(QObject):
    state_changed = Signal(str)
    received = Signal(bytes)
    transmitted = Signal(bytes)
    error = Signal(str)

    def __init__(self):
        super().__init__()
        self.worker = None
        self.connected = False
        self.closing = False

    @staticmethod
    def scan():
        return [(p.device, p.description) for p in list_ports.comports()]

    def open(self, port, baud):
        if self.worker is not None:
            raise RuntimeError('请先断开串口')
        if not port:
            raise ValueError('请选择串口')
        self.closing = False
        self.worker = SerialWorker(port, baud)
        self.worker.opened.connect(self._opened)
        self.worker.received.connect(self.received)
        self.worker.transmitted.connect(self.transmitted)
        self.worker.failed.connect(self.error)
        self.worker.finished.connect(self._finished)
        self.state_changed.emit('连接中')
        self.worker.start()

    def _opened(self):
        if not self.closing:
            self.connected = True
            self.state_changed.emit('串口已打开；FPGA 未确认')

    def _finished(self):
        worker = self.worker
        self.worker = None
        self.connected = False
        self.closing = False
        if worker is not None:
            worker.deleteLater()
        self.state_changed.emit('已断开')

    def close(self):
        self.connected = False
        self.closing = True
        if self.worker:
            self.worker.stop_event.set()
            self.state_changed.emit('正在断开')

    def send(self, data):
        if not self.connected or self.worker is None:
            raise RuntimeError('串口未连接')
        try:
            self.worker.outbox.put_nowait(bytes(data))
        except Full:
            raise RuntimeError('发送队列已满，请稍后重试') from None
