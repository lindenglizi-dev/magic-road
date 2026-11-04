
import ipaddress
import queue
import secrets
import select
import socket
import struct
import threading
import time
import zlib
from pathlib import Path

import numpy as np
from PIL import Image
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QImage

from protocol import Decoder, FrameAssembler, encode, response_body, parse_status, SUPPORTED_ALGORITHM_IDS, INSPECTION_CAPABILITY, inspection_config, parse_inspection
from protocol import gamma_curve, tone_payload, parse_tone, TONE_CAPABILITY
from protocol import editor_curve, editor_payload, parse_editor
from udp_listener import bind_listener
from client_session import ClientSession
from network_binding import resolve_binding, pin_interface


class Worker(QThread):
    log = Signal(str)
    frame = Signal(QImage)
    state = Signal(dict)
    stats = Signal(str)
    inspection = Signal(dict)
    editing = Signal(dict)
    adjustment = Signal(dict)
    network = Signal(object)                                                       
    progress = Signal(int)
    uploading = Signal(bool)
    connected = Signal(bool)

    def __init__(self, port, fpga_ip, bind_ip="0.0.0.0", parent=None):
        super().__init__(parent)
        ipaddress.IPv4Address(fpga_ip)
        ipaddress.IPv4Address(bind_ip)
        self.port, self.peer, self.bind_ip = port, (fpga_ip, 6002), bind_ip
        self.commands = queue.Queue(maxsize=32)
        self.stop_event, self.cancel_event = threading.Event(), threading.Event()
        self.serial = self.udp = None
        self.client_session = None
        self.seq = secrets.randbelow(256)
        self.decoder, self.assembler = Decoder(), FrameAssembler()
        self.replies = []
        self.next_hello = self.next_stats = 0.0
        self.last_count = self.last_bytes = 0
        self.last_stats = time.monotonic()
        self.capabilities = 0
        self.pending_editor = None
        self.desired_editor = (100,100,100,0)
        self.editor_queued = False
        self.tone_lock = threading.Lock()
        self.pending_tone = None
        self.tone_queued = False
        self.desired_tone = (70, 125, 32)
        self.preview = True
        self.last_frame_at = 0.0

    def submit(self, name, *args):
        if name == "edit":
            with self.tone_lock:
                self.pending_editor = args
                self.desired_editor = args
                if self.editor_queued:
                    return
                self.editor_queued = True
        if name == "tone":
            with self.tone_lock:
                self.pending_tone = args
                self.desired_tone = args
                if self.tone_queued:
                    return
                self.tone_queued = True
        try:
            self.commands.put_nowait((name, args))
        except queue.Full:
            if name == "edit":
                with self.tone_lock:
                    self.editor_queued = False
            if name == "tone":
                with self.tone_lock:
                    self.tone_queued = False
            self.log.emit("控制队列已满，请等待上一条操作完成")

    def stop(self):
        self.stop_event.set()
        self.cancel_event.set()

    def _pump(self, timeout=0.01):
        if self.stop_event.is_set():
            raise InterruptedError("连接已停止")
        now = time.monotonic()
        if now >= self.next_hello:
            self.udp.sendto(b"HXVS" + bytes((int(self.preview),)), self.peer)
            self.next_hello = now + 1.0
        if self.serial:
            data = self.serial.read(self.serial.in_waiting or 1)
            for packet in self.decoder.feed(data) if data else ():
                self.replies.append(("uart", packet))
        readable, _, _ = select.select([self.udp], [], [], timeout)
        if readable:
            deadline = time.monotonic() + 0.012
            while True:
                try:
                    data, source = self.udp.recvfrom(2048)
                except BlockingIOError:
                    break
                except ConnectionResetError:
                    break                                                              
                if source != self.peer:
                    continue
                if data.startswith(b"HXIM"):
                    result = self.assembler.feed(data)
                    if result:
                        _, raw = result
                        self.last_frame_at = time.monotonic()
                                                                                                       
                        rgb = rgb565_to_rgb(raw, 1280, 720)
                        self.frame.emit(QImage(rgb.data, 1280, 720, 1280 * 3, QImage.Format.Format_RGB888).copy())
                else:
                    for packet in Decoder().feed(data):
                        self.replies.append(("udp", packet))
                if time.monotonic() >= deadline:
                    break
                                                                            
        self.replies[:] = self.replies[-64:]
        now = time.monotonic()
        if now >= self.next_stats:
            seconds = max(0.001, now - self.last_stats)
            fps = (self.assembler.completed - self.last_count) / seconds
            mbps = (self.assembler.bytes - self.last_bytes) * 8 / seconds / 1e6
            stale = "  · 等待图像" if now - self.last_frame_at > 2 else ""
            self.stats.emit(f"{fps:.1f} fps  · {mbps:.1f} Mb/s  · 不完整帧 {self.assembler.dropped}  · 非法包 {self.assembler.invalid}{stale}")
            self.last_count, self.last_bytes = self.assembler.completed, self.assembler.bytes
            self.last_stats, self.next_stats = now, now + 1

    def request(self, command, data=b"", channel="uart", timeout=1.5, retries=3):
        if channel == "uart" and not self.serial:
            raise RuntimeError("请连接 UART 后操作")
        self.seq = (self.seq + 1) & 255
        seq = self.seq
        frame = encode(command, seq, data)
        self.replies.clear()
        for attempt in range(retries + 1):
            if channel == "uart":
                self.serial.write(frame)
            else:
                self.udp.sendto(frame, self.peer)
            deadline = time.monotonic() + timeout
            while time.monotonic() < deadline:
                self._pump(0.001 if channel == "udp" else 0.01)
                for index, (origin, packet) in enumerate(self.replies):
                    if (origin == channel and packet.seq == seq and packet.data[:1] == bytes((command,))
                            and packet.command in (0x81, 0x82)):
                        del self.replies[index]
                        return response_body(packet, command)
            if attempt < retries:
                self.log.emit(f"CMD {command:02X} 超时，重试 {attempt + 1}/{retries}")
        raise TimeoutError(f"CMD {command:02X} 无硬件确认；检查网段、PHY状态及摄像头时钟")

    def _read_status(self):
        status = parse_status(self.request(3, timeout=0.8, retries=1))
        self.capabilities = status["caps"]
        self.state.emit(status)
        return status

    def _set_tone(self, gamma, contrast, brightness):
                                                                                        
        payload = tone_payload(gamma, contrast, brightness)
        current = parse_tone(self.request(0x07))
        commit = not current["ready"] or current["gamma"] != gamma
        if commit:
            curve = gamma_curve(gamma)
            self.request(0x06)
            for offset in range(0, 256, 16):
                self.request(0x05, bytes((offset,)) + curve[offset:offset + 16])
        payload = tone_payload(gamma, contrast, brightness, commit)
        actual = parse_tone(self.request(0x04, payload, timeout=3))
        if (actual["contrast_q8"], actual["brightness"], actual["gamma"]) != (round(contrast * 256 / 100), brightness, gamma):
            raise RuntimeError("FPGA 图像参数回复不匹配")
        self.adjustment.emit(actual)
        self.log.emit(f"FPGA 参数已生效：Gamma {gamma / 100:.2f}，对比度 {actual['contrast_q8'] / 256:.2f}，亮度 {brightness:+d}")

    def _set_editor(self, gamma, contrast, saturation, brightness):
        editor_payload(gamma, contrast, saturation, brightness)
        current = parse_editor(self.request(0x0b))
        target = (round(contrast * 256 / 100), brightness, gamma)
        commit = not current["ready"] or (current["contrast_q8"], current["brightness"], current["gamma"]) != target
        if commit:
            curve = editor_curve(gamma, contrast, brightness)
            self.request(0x08)
            for offset in range(0, 256, 16):
                self.request(0x09, bytes((offset,)) + curve[offset:offset + 16])
        actual = parse_editor(self.request(0x0a, editor_payload(gamma, contrast, saturation, brightness, commit), timeout=3))
        if (actual["contrast_q8"], actual["brightness"], actual["gamma"]) != target or actual["saturation_q8"] != round(saturation * 256 / 100) or not actual["ready"]:
            raise RuntimeError("FPGA 编辑参数回复不匹配")
        if self.request(1, bytes((9,))) != bytes((9,)):
            raise RuntimeError("FPGA 编辑模式回复不匹配")
        self.editing.emit(actual)
        self.log.emit("四项叠加编辑已在 FPGA 帧边界生效")
        self._read_status()

    def _upload(self, filename):
        self.uploading.emit(True)
        previous_preview = self.preview
        self.preview = False
        self.next_hello = 0
        session, begun, committed = secrets.randbits(32), False, False
        try:
            self.log.emit("解码图片并转换为 1920×1080 RGB565")
            with Image.open(filename) as image:
                image = image.convert("RGB").resize((1920, 1080), Image.Resampling.LANCZOS)
                rgb = np.asarray(image, dtype=np.uint16)
            pixels = (((rgb[:, :, 0] >> 3) << 11) | ((rgb[:, :, 1] >> 2) << 5) | (rgb[:, :, 2] >> 3)).astype("<u2").tobytes()
            checksum = zlib.crc32(pixels)
            begin = struct.pack("<IHHBII", session, 1920, 1080, 1, len(pixels), checksum)
            body = self.request(0x30, begin, timeout=2)
            if body != struct.pack("<I", session):
                raise RuntimeError("BEGIN 返回的会话不匹配")
            begun = True
            started, last_progress = time.monotonic(), -1
            for offset in range(0, len(pixels), 224):
                if self.cancel_event.is_set():
                    raise InterruptedError("用户取消上传")
                chunk = pixels[offset:offset + 224]
                payload = struct.pack("<II", session, offset) + chunk
                body = self.request(0x31, payload, "udp", timeout=0.3, retries=4)
                if body != struct.pack("<II", session, offset + len(chunk)):
                    raise RuntimeError("DATA ACK 的会话或连续偏移不匹配")
                progress = (offset + len(chunk)) * 99 // len(pixels)
                if progress != last_progress:
                    self.progress.emit(progress)
                    last_progress = progress
            self.log.emit("像素发送完毕，等待 FPGA CRC、DDR 尾字读回及帧间发布确认")
            body = self.request(0x32, struct.pack("<II", session, checksum), timeout=3)
            if body != struct.pack("<II", session, checksum):
                raise RuntimeError("END 校验回复不匹配")
            committed = True
            self.progress.emit(100)
            self.log.emit(f"图片已提交，用时 {time.monotonic() - started:.1f} 秒；可切换至 PC Image")
        finally:
            if begun and not committed and not self.stop_event.is_set():
                try:
                    self.request(0x33, struct.pack("<I", session), timeout=1)
                    self.log.emit("上传会话已终止；上一次完整图片仍保留")
                except Exception as error:
                    self.log.emit(f"终止未确认：{error}；重连后查询实际图片状态")
            self.uploading.emit(False)
            self.preview = previous_preview
            self.next_hello = 0
            if not self.stop_event.is_set():
                self._read_status()

    def run(self):
        try:
            self.client_session = ClientSession(self.peer[0])
            binding = resolve_binding(self.peer[0], self.bind_ip, self.log.emit)
            self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.udp.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 8 * 1024 * 1024)
            pin_interface(self.udp, binding)
            local_address = bind_listener(self.udp, binding.address)
            self.udp.setblocking(False)
            if self.port:
                import serial
                self.serial = serial.Serial(self.port, 115200, timeout=0, write_timeout=1)
                self.serial.reset_input_buffer()
            self.connected.emit(True)
            self.log.emit(f"UDP {local_address[0]}:{local_address[1]} → {self.peer[0]}:6002；收发已绑定 {binding.interface_name}")
            if local_address[1] != 6001:
                self.log.emit("UDP 6001不可用，已自动选择空闲端口；FPGA从订阅包学习回传端口")
            if self.serial:
                try:
                    self._read_status()
                    if self.capabilities & 0xE0 != 0xE0:
                        self.log.emit("当前固件的以太网能力与协议版本不匹配")
                except Exception as error:
                    self.log.emit(str(error))
            next_poll = time.monotonic()
            while not self.stop_event.is_set():
                self._pump()
                try:
                    name, args = self.commands.get_nowait()
                except queue.Empty:
                    name, args = None, ()
                try:
                    if name == "mode":
                        if args[0] not in SUPPORTED_ALGORITHM_IDS:
                            raise ValueError("算法编号须为 0～9")
                        if args[0] == 9:
                                                                                       
                            self._set_editor(*(self.desired_editor))
                        if args[0] == 6:
                            self._set_tone(*self.desired_tone)
                        body = self.request(1, bytes((args[0],)))
                        if body != bytes((args[0],)):
                            raise RuntimeError("模式回复不匹配")
                        self.log.emit(f"硬件已应用算法 {args[0]}")
                        self._read_status()
                    elif name == "edit":
                        with self.tone_lock:
                            latest = self.pending_editor
                            self.pending_editor = None
                            self.editor_queued = False
                        if latest is not None:
                            self._set_editor(*latest)
                    elif name == "tone":
                        with self.tone_lock:
                            latest = self.pending_tone
                            self.pending_tone = None
                            self.tone_queued = False
                        if latest is not None:
                            self._set_tone(*latest)
                    elif name == "source":
                        body = self.request(0x20, bytes((args[0],)), timeout=3)
                        if body != bytes((args[0],)):
                            raise RuntimeError("输入源回复不匹配")
                        self._read_status()
                    elif name == "inspection":
                        data = inspection_config(*args)
                        if self.request(0x12, data) != data:
                            raise RuntimeError("工业检测配置回复不匹配")
                        self.log.emit("检测参数已在 FPGA 帧边界应用；参数变化会清零并开始新一批计数")
                    elif name == "clear_inspection":
                        if self.request(0x13):
                            raise RuntimeError("计数清零回复不匹配")
                        self.log.emit("FPGA 计数和轨迹已清零")
                    elif name == "upload":
                        self._upload(args[0])
                    elif name == "status":
                        self._read_status()
                    elif name == "preview":
                        self.preview = args[0]
                        self.next_hello = 0
                    if self.serial and time.monotonic() >= next_poll:
                        raw = self.request(0x40, retries=0)
                        if len(raw) == 4:
                            self.network.emit(int.from_bytes(raw, "little"))
                        if self.capabilities & INSPECTION_CAPABILITY:
                            self.inspection.emit(parse_inspection(self.request(0x14, retries=0)))
                        next_poll = time.monotonic() + 1.0
                except InterruptedError as error:
                    if self.stop_event.is_set():
                        break
                    self.log.emit(str(error))
                except Exception as error:
                    self.log.emit(str(error))
                    next_poll = time.monotonic() + 3
        except InterruptedError:
            pass
        except Exception as error:
            self.log.emit(f"连接失败：{error}")
        finally:
            if self.udp:
                try:
                    self.udp.sendto(b"HXVS\x00", self.peer)
                except OSError:
                    pass
                self.udp.close()
            if self.serial:
                self.serial.close()
            if self.client_session:
                self.client_session.close()
            self.connected.emit(False)


def rgb565_to_rgb(raw, width, height):
    words = np.frombuffer(raw, dtype="<u2").reshape(height, width)
    r, g, b = (words >> 11) & 31, (words >> 5) & 63, words & 31
    return np.stack(((r << 3) | (r >> 2), (g << 2) | (g >> 4), (b << 3) | (b >> 2)), axis=-1).astype(np.uint8)
