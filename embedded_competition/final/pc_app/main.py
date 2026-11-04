
import json
import queue
import secrets
import os
from pathlib import Path
import ipaddress
import socket
import sys
import threading
import time

if '--smoke' in sys.argv:
    os.environ.setdefault('QT_QPA_PLATFORM','offscreen')

import numpy as np
from PySide6.QtCore import Qt, QThread, QTimer, Signal
from PySide6.QtGui import QFontDatabase, QImage, QPixmap
from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow, QMessageBox
from layout import build_layout, ALGORITHMS
from client_session import ClientSession
from network_binding import pin_interface, resolve_binding
from protocol import Decoder, FrameAssembler, encode
from industrial import (CONFIGURE, CLEAR, READ, SET_VIEW, READ_VIEW, RAW_VIEW, BALL_VIEW,
    PanelError, pack_config, write_payload, parse_reply, view_payload, parse_view)
from telemetry import ACQUIRE, READ_PAGE, JsonlRecorder, assemble_pages, page_request, parse_page
from combined_protocol import (CONFIGURE_APPLICATION, CURVE_CHUNK, READ_APPLICATION,
    config_bytes, parse_application, write_payload as application_payload,
    gamma_curve, editor_curve, curve_chunks)


                                                                         


class ResultsCancelled(RuntimeError):
    pass


def decode_rgb565(raw, view):
    words = np.frombuffer(raw, dtype='<u2').reshape(720, 1280)
    r, g, b = words >> 11, (words >> 5) & 63, words & 31
    rgb = np.empty((720, 1280, 3), np.uint8)
    if view == RAW_VIEW:
        rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2] = (r << 3) | (r >> 2), (g << 2) | (g >> 4), (b << 3) | (b >> 2)
    else:
        rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2] = (r*255+15)//31, (g*255+31)//63, (b*255+15)//31
    return rgb


class Connection(QThread):
    frame = Signal(QImage, object)
    snapshot = Signal(dict, object)
    panel = Signal(dict, object)
    application = Signal(dict)
    view = Signal(dict)
    writing = Signal(bool)
    message = Signal(str)
    online = Signal(bool)
    stats = Signal(str)

    def __init__(self, peer, bind):
        super().__init__()
        self.peer = (peer, 6002)
        self.bind = bind
        self.stop_event = threading.Event()
        self.poll_event = threading.Event()
        self.seq = 0
        self.decoder = Decoder()
        self.assembler = FrameAssembler()
        self.replies = []
        self.next_hello = 0
        self.jobs = queue.Queue()
        self.panel_state = None
        self.panel_unsupported = False
        self.next_panel_probe = 0
        self.panel_probe_delay = 2
        self.request_id = secrets.randbits(32)
        self.results_allowed = threading.Event()
        self.view_lock = threading.Lock()
        self.ui_generation = 0
        self.view_job = None
        self.expected_view = None
        self.next_view_probe = 0
        self.last_view_frame_at = time.monotonic()
        self.application_state = None
        self.application_jobs = queue.Queue(maxsize=1)
        self.display_pending = False

    def select_view(self, target, values=(100, 100, 100, 0)):
                                                                                      
        with self.view_lock:
            self.results_allowed.clear()
            self.panel_state = None
            self.ui_generation += 1
            self.view_job = (self.ui_generation, target, values)
            self.expected_view = None
            self.display_pending = True
            self.next_view_probe = 0
            return self.ui_generation

    def select_application(self, mode, values):
        config_bytes(mode, *values)
        with self.view_lock:
            self.results_allowed.clear()
            self.panel_state = None
            self.ui_generation += 1
            self.view_job = None
            self.expected_view = None
            self.display_pending = True
            try:
                self.application_jobs.get_nowait()
            except queue.Empty:
                pass
            self.application_jobs.put_nowait((self.ui_generation, mode, values))
            return self.ui_generation

    def check_generation(self, generation):
        if generation != self.ui_generation:
            raise ResultsCancelled()

    def check_results(self, generation):
        if (not self.results_allowed.is_set() or generation != self.ui_generation or
                self.application_state is None or self.application_state['mode'] != 10):
            raise ResultsCancelled()

    def read_view(self, generation=None):
        generation = self.ui_generation if generation is None else generation
        self.check_generation(generation)
        state = self.request(READ_VIEW, parser=parse_view)
        with self.view_lock:
            self.check_generation(generation)
            if self.application_state is None or (self.application_state['mode'] != 10 and state['view'] != BALL_VIEW):
                raise ValueError('算法模式与显示状态不一致，等待重新确认')
            self.expected_view = (state['view'], state['revision'])
        return state

    def write_view(self, job):
        generation, target, values = job
        self.results_allowed.clear()
        self.read_application(generation)
        if self.application_state['mode'] != 10:
            self.write_application(10, values, generation)
            return
        self.set_board_view(target, generation)
        with self.view_lock:
            if generation == self.ui_generation:
                self.panel_state = None
                self.panel_unsupported = False
                self.next_panel_probe = 0
                self.view_job = None
                self.display_pending = False

    def set_board_view(self, target, generation):
        state = self.read_view(generation)
        self.check_generation(generation)
        self.request_id = (self.request_id + 1) & 0xffffffff
        request_id = self.request_id
        result = self.request(SET_VIEW, view_payload(request_id, state['revision'], target), parser=parse_view)
        if result['request_id'] != request_id or result['view'] != target:
            raise ValueError('显示模式回执与请求不一致')
        with self.view_lock:
            self.check_generation(generation)
            self.expected_view = (target, result['revision'])
        return result


    def stop(self):
        self.stop_event.set()

    def pump(self):
        if self.stop_event.is_set():
            raise InterruptedError()
        now = time.monotonic()
        if now >= self.next_hello:
            self.udp.sendto(b'HXVS\x01', self.peer)
            self.next_hello = now + 1
        try:
            data, source = self.udp.recvfrom(2048)
        except (socket.timeout, ConnectionResetError):
            return
        if source != self.peer:
            return
        if data.startswith(b'HXIM'):
            result = self.assembler.feed(data)
            if result:
                frame_id, raw, tag = result
                with self.view_lock:
                    if (tag is None or tag != self.expected_view or self.display_pending or
                            self.application_state is None):
                        return
                    generation = self.ui_generation
                    self.last_view_frame_at = time.monotonic()
                    actual_view, revision = tag
                    mode = self.application_state['mode']
                    if actual_view == BALL_VIEW and mode == 10:
                        self.results_allowed.set()
                    else:
                        self.results_allowed.clear()
                self.view.emit(dict(view=actual_view, revision=revision, mode=mode, ui_generation=generation))
                rgb = decode_rgb565(raw, RAW_VIEW if mode < 10 else actual_view)
                self.frame.emit(QImage(rgb.data,1280,720,1280*3,QImage.Format.Format_RGB888).copy(),
                    dict(frame_id=frame_id, view=actual_view, revision=revision, mode=mode, ui_generation=generation))
        else:
            self.replies.extend(packet for packet in self.decoder.feed(data)
                if self.results_allowed.is_set() or not packet.data or not ACQUIRE <= packet.data[0] <= READ)
            self.replies[:] = self.replies[-8:]

    def request(self, command, payload=b'', parser=parse_page, attempts=3):
        generation = self.ui_generation
        ball_request = ACQUIRE <= command <= READ
        if ball_request:
            self.check_results(generation)
        self.seq = (self.seq+1) & 255
        sequence = self.seq
        packet = encode(command, sequence, payload)
        self.replies.clear()
        for attempt in range(attempts):
            with self.view_lock:
                if ball_request:
                    self.check_results(generation)
                self.udp.sendto(packet, self.peer)
            deadline = time.monotonic()+0.35
            while time.monotonic() < deadline:
                self.pump()
                if ball_request:
                    self.check_results(generation)
                for response in self.replies:
                    if response.seq == sequence and response.data[:1] == bytes((command,)):
                        with self.view_lock:
                            if ball_request:
                                self.check_results(generation)
                            try:
                                return parser(response, command)
                            except PanelError as error:
                                if ball_request and error.code == 8:
                                    self.results_allowed.clear()
                                    self.expected_view = None
                                raise
        if ball_request:
            self.check_results(generation)
        raise TimeoutError('状态请求无回复；请核对新bit、板卡IP和网线')

    def read_panel(self, attempts=3):
        generation = self.ui_generation
        result = self.request(READ, parser=parse_reply, attempts=attempts)
        self.check_results(generation)
        self.panel_state = result
        self.panel_unsupported = False
        self.panel_probe_delay = 2
        self.next_panel_probe = time.monotonic()+0.5
        self.panel.emit(result, generation)
        return result

    def probe_panel(self, force=False, attempts=1):
        if not self.results_allowed.is_set():
            return
        if not force and (self.panel_unsupported or time.monotonic() < self.next_panel_probe):
            return
        try:
            self.read_panel(attempts)
        except ResultsCancelled:
            raise
        except (TimeoutError, RuntimeError, ValueError) as error:
            if isinstance(error, PanelError) and error.code == 1:
                self.panel_unsupported = True
                self.panel_state = None
                self.message.emit('板端未支持工业参数协议，保持只读；“查询状态”可重新探测。')
            else:
                self.message.emit('工业参数暂未读回，稍后自动重试：'+str(error))
            self.next_panel_probe = time.monotonic()+self.panel_probe_delay
            self.panel_probe_delay = min(self.panel_probe_delay*2, 8)

    def write_panel(self, command, config):
        generation = self.ui_generation
        self.check_results(generation)
        if self.panel_state is None:
            raise RuntimeError('尚未确认板端支持工业参数写入')
        self.request_id = (self.request_id + 1) & 0xffffffff
        payload = write_payload(self.request_id, self.panel_state['revision'], config,
            self.panel_state['capability'], self.panel_state)
        self.writing.emit(True)
        try:
            result = self.request(command, payload, parser=parse_reply)
            if result['request_id'] != self.request_id:
                raise ValueError('板端写入回执ID不匹配')
            self.check_results(generation)
            result['applied'] = True
            self.panel_state = result
            self.panel.emit(result, generation)
            if generation == self.ui_generation:
                self.message.emit(f"板端已应用工业参数版本 {result['revision']}")
        except (TimeoutError, PanelError):
                                                                                    
            self.read_panel()
            raise
        finally:
            self.writing.emit(False)

    def read_application(self, generation=None):
        generation = self.ui_generation if generation is None else generation
        self.check_generation(generation)
        state = self.request(READ_APPLICATION, parser=parse_application)
        with self.view_lock:
            self.check_generation(generation)
            if self.application_state is None or self.application_state['mode'] != state['mode']:
                self.results_allowed.clear()
            self.application_state = state
            state['ui_generation'] = generation
        self.application.emit(state)
        return state

    def write_application(self, mode, values, generation=None):
        generation = self.ui_generation if generation is None else generation
        gamma, contrast, saturation, brightness = values
        config_bytes(mode, gamma, contrast, saturation, brightness)
        self.check_generation(generation)
        self.results_allowed.clear()
        self.read_application(generation)
        self.writing.emit(True)
        try:
            commit = 0
            if mode in (6, 9):
                kind = int(mode == 9)
                curve = editor_curve(gamma, contrast, brightness) if kind else gamma_curve(gamma)
                for content in curve_chunks(kind, curve):
                    self.send_application_write(CURVE_CHUNK, content, generation)
                commit = 1 << kind
            content = config_bytes(mode, gamma, contrast, saturation, brightness, commit)
            self.send_application_write(CONFIGURE_APPLICATION, content, generation)
            self.read_application(generation)
                                                                            
                                                                                 
            if mode == 10:
                self.set_board_view(BALL_VIEW, generation)
            else:
                self.read_view(generation)
            with self.view_lock:
                self.check_generation(generation)
                self.display_pending = False
                self.view_job = None
                self.panel_state = None
                self.panel_unsupported = False
                self.next_panel_probe = 0
        except ResultsCancelled:
            raise
        except (TimeoutError, RuntimeError, ValueError):
                                                                               
                                                                              
            self.application_state = None
            try:
                self.read_application(generation)
                self.read_view(generation)
            except (TimeoutError, RuntimeError, ValueError):
                self.expected_view = None
            raise
        finally:
            self.writing.emit(False)

    def send_application_write(self, command, content, generation=None):
        generation = self.ui_generation if generation is None else generation
        self.check_generation(generation)
        if self.application_state is None:
            raise RuntimeError('尚未确认合并bit，不能写入算法模式')
        self.request_id = (self.request_id + 1) & 0xffffffff
        previous_revision = self.application_state['revision']
        state = self.request(command, application_payload(self.request_id, previous_revision, content), parser=parse_application)
        self.check_generation(generation)
        if (state['request_id'] != self.request_id or state['config'] != content or
                state['revision'] != ((previous_revision + 1) & 0xffff)):
            raise ValueError('合并写入回执ID、版本或内容不匹配')
        self.application_state = state
        return state

    def read_snapshot(self):

        generation = self.ui_generation
        self.check_results(generation)
        pages = [self.request(ACQUIRE)]
        for page in range(1, 4):
            pages.append(self.request(READ_PAGE, page_request(pages[0][0], page)))
        with self.view_lock:
            self.check_results(generation)
            return assemble_pages(pages)

    def run(self):
        session = None
        self.udp = None
        try:
            session = ClientSession(self.peer[0])
            binding = resolve_binding(self.peer[0], self.bind, self.message.emit)
            self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            pin_interface(self.udp, binding)
            try:
                self.udp.bind((binding.address, 6001))
            except OSError:
                self.udp.bind((binding.address, 0))
            self.udp.settimeout(0.015)
            self.udp.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,4*1024*1024)
            self.online.emit(True)
            self.message.emit(f'UDP {self.udp.getsockname()[0]}:{self.udp.getsockname()[1]} → {self.peer[0]}:{self.peer[1]}；无需UART')
            try:
                self.read_application()
                self.read_view()
            except (TimeoutError, RuntimeError, ValueError) as error:
                self.message.emit('等待显示模式确认：'+str(error))
            next_poll = 0
            stats_at = time.monotonic()
            stats_frames = stats_bytes = 0
            while not self.stop_event.is_set():
                self.pump()
                if self.view_job is not None:
                    if time.monotonic() < self.next_view_probe:
                        continue
                    job = self.view_job
                    try:
                        self.write_view(job)
                    except ResultsCancelled:
                        pass
                    except (TimeoutError, RuntimeError, ValueError) as error:
                        self.message.emit('显示切换待确认：'+str(error))
                                                                                                     
                        self.next_view_probe = time.monotonic()+1
                    continue
                try:
                    application_generation, mode, values = self.application_jobs.get_nowait()
                except queue.Empty:
                    pass
                else:
                    try:
                        self.write_application(mode, values, application_generation)
                    except ResultsCancelled:
                        pass
                    except (TimeoutError, RuntimeError, ValueError) as error:
                        self.message.emit('算法切换待重新确认：'+str(error))
                        with self.view_lock:
                            if application_generation == self.ui_generation:
                                self.display_pending = False
                                self.expected_view = None
                                self.next_view_probe = 0
                    continue
                if (self.expected_view is None or time.monotonic()-self.last_view_frame_at > 2) and time.monotonic() >= self.next_view_probe:
                    self.results_allowed.clear()
                    self.view.emit(dict(view=None, ui_generation=self.ui_generation))
                    try:
                        self.read_application()
                        self.read_view()
                    except (TimeoutError, RuntimeError, ValueError) as error:
                        self.message.emit(str(error))
                    self.next_view_probe = time.monotonic()+1
                try:
                    job_generation, command, config = self.jobs.get_nowait()
                except queue.Empty:
                    pass
                else:
                    try:
                        self.check_results(job_generation)
                        self.write_panel(command, config)
                    except ResultsCancelled:
                        pass
                    except (TimeoutError, RuntimeError, ValueError) as error:
                        self.message.emit(str(error))
                if self.results_allowed.is_set() and (time.monotonic() >= next_poll or self.poll_event.is_set()):
                    explicit_query = self.poll_event.is_set()
                    self.poll_event.clear()
                    try:
                        generation = self.ui_generation
                        snapshot = self.read_snapshot()
                        self.check_results(generation)
                        self.snapshot.emit(snapshot, generation)
                    except ResultsCancelled:
                        pass
                    except (TimeoutError, RuntimeError, ValueError) as error:
                        self.message.emit(str(error))
                                                                                        
                    try:
                        self.probe_panel(force=explicit_query)
                    except ResultsCancelled:
                        pass
                    next_poll = time.monotonic()+0.5
                now = time.monotonic()
                if now-stats_at >= 1:
                    seconds = now-stats_at
                    self.stats.emit(f'{(self.assembler.completed-stats_frames)/seconds:.1f} fps  ·  '
                        f'{(self.assembler.bytes-stats_bytes)*8/seconds/1e6:.1f} Mb/s  ·  '
                        f'不完整帧 {self.assembler.dropped}  ·  非法包 {self.assembler.invalid}')
                    stats_at = now
                    stats_frames, stats_bytes = self.assembler.completed, self.assembler.bytes
        except InterruptedError:
            pass
        except Exception as error:
            self.message.emit(str(error))
        finally:
            if self.udp:
                self.udp.close()
            if session:
                session.close()
            self.online.emit(False)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        for font in ('msyh.ttc','msyhbd.ttc'):
            filename=Path(os.environ.get('WINDIR','C:/Windows'))/'Fonts'/font
            if filename.exists():QFontDatabase.addApplicationFont(str(filename))
        self.worker = None
        self.last_image = None
        self.last_video_frame = None
        self.last_snapshot_at = None
        self.last_snapshot = None
        self.last_frame_at = None
        self.is_connected = False
        self.recorder = JsonlRecorder()
        self.panel_state = None
        self.panel_writing = False
        self.last_panel_at = None
        self.current_view = None
        self.current_view_revision = None
        self.ui_generation = 0
        self.application_state = None
        self.tone_timer = QTimer(self); self.tone_timer.setSingleShot(True); self.tone_timer.setInterval(350)
        self.tone_timer.timeout.connect(self.apply_tone)
        build_layout(self, algorithm=False, combined=True)
        self.roi_apply.clicked.connect(self.apply_roi)
        self.clear_counts_button.clicked.connect(self.clear_industrial)
        self.peer, self.binding = self.ip, self.bind
        self.image = self.preview_label
        self.present_view(None)
        self.freshness = QTimer(self); self.freshness.setInterval(1000)
        self.freshness.timeout.connect(self.check_freshness); self.freshness.start()

    def toggle_connection(self):
        if self.worker:
            self.connect_button.setEnabled(False)
            self.worker.stop();return
        try:
            ipaddress.IPv4Address(self.peer.text().strip())
            ipaddress.IPv4Address(self.binding.text().strip())
        except ValueError:
            QMessageBox.warning(self,'地址格式','FPGA IP 和本机绑定必须是 IPv4 地址。')
            return
        self.reset_results('等待本次连接的板端结果')
        self.worker = Connection(self.peer.text().strip(),self.binding.text().strip())
        self.worker.frame.connect(self.show_frame);self.worker.snapshot.connect(self.show_snapshot)
        self.worker.application.connect(self.show_application)
        self.ui_generation += 1
        self.worker.ui_generation = self.ui_generation
        self.current_view = None
        self.current_view_revision = None
        self.present_view(None)
        self.worker.view.connect(self.show_view)
        self.worker.panel.connect(self.show_panel)
        self.worker.writing.connect(self.set_writing)
        self.worker.message.connect(self.on_message)
        self.worker.stats.connect(self.stats_label.setText)
        self.worker.online.connect(self.on_connected)
        self.connect_button.setText('连接中…'); self.connect_button.setEnabled(False)
        self.peer.setEnabled(False); self.binding.setEnabled(False)
        self.worker.finished.connect(self.connection_finished);self.worker.start()

    def on_connected(self, active):
        self.is_connected = active
        self.query.setEnabled(active)
        if not active:
            self.roi_box.setEnabled(False)
        self.present_view(self.current_view)
        if active:
            self.connect_button.setText('断开'); self.connect_button.setEnabled(True)
            self.network_label.setText('UDP 已监听，等待板端视频/状态；不代表 PHY 已确认')

    def connection_finished(self):
        self.worker.deleteLater();self.worker=None
        self.is_connected = False; self.query.setEnabled(False)
        self.connect_button.setText('连接以太网'); self.connect_button.setEnabled(True)
        self.peer.setEnabled(True); self.binding.setEnabled(True)
        self.network_label.setText('UDP：连接已断开')
        self.reset_results('连接已断开；等待重新读取')
        self.current_view = None
        self.current_view_revision = None
        self.present_view(None)

    def reset_results(self, text):
        self.application_state = None
        self.algorithm_box.setEnabled(False)
        self.panel_state = None
        self.panel_writing = False
        self.last_panel_at = None
        self.roi_box.setEnabled(False)
        self.target_color.model().item(self.target_color.findData(0)).setEnabled(False)
        self.discovery_side.setEnabled(False); self.discovery_area.setEnabled(False)
        self.last_snapshot_at = self.last_frame_at = None
        self.last_snapshot = None
        self.last_image = self.last_video_frame = None
        self.image.clear(); self.image.setText(text)
        self.screenshot.setEnabled(False)
        self.summary.setText(text); self.face_label.setText('板端状态：'+text)
        self.profile_notice.setText('等待工业参数能力确认；新协议握手后可在03区通过Ethernet应用参数并回读。旧bit保持只读。')
        self.keys_hint.setText('等待板端能力确认；旧bit按其原操作说明使用按键。')
        self.application_status.setText('实际显示状态：'+text)
        self.details.clear(); self.video_info.setText('视频frameID：—')
        self.stats_label.setText('0.0 fps  ·  0.0 Mb/s  ·  等待图像')
        self.roi_enable.setChecked(False); self.strict.setChecked(False)
        for row in range(4):
            for column in range(1,5):
                self.targets.item(row,column).setText('—')

    def clear_ball_results(self):
        self.recorder.close()
        self.record.setChecked(False)
        self.last_snapshot = self.panel_state = None
        self.last_snapshot_at = self.last_panel_at = None
        self.details.clear()
        self.log_view.clear()
        self.summary.clear()
        self.face_label.clear()
        self.application_status.clear()
        for row in range(4):
            for column in range(1, 5):
                self.targets.item(row, column).setText('—')

    def ball_view_active(self):
        return (self.current_view == BALL_VIEW and self.application_state is not None and
                self.application_state['mode'] == 10)

    def present_view(self, view):
        mode = self.application_state['mode'] if self.application_state else None
        ball = view == BALL_VIEW and mode == 10
        demo = view == BALL_VIEW and mode is not None and mode < 10
        if not ball:
            self.clear_ball_results()
            self.profile_notice.setText('保留全部检测参数；当前不显示、写入或记录小球结果。切换到小球识别并确认完整帧后恢复。')
            self.keys_hint.setText('页面切换使用下方按钮；长按切档已删除，其他按键以配套bit操作说明为准。')
        elif self.panel_state is None:
            self.profile_notice.setText('等待工业参数能力确认；读回后可应用参数和清零。')
        self.roi_box.setEnabled(ball and self.is_connected and self.panel_state is not None and not self.panel_writing)
        self.roi_box.setToolTip('参数在板端帧边界整组生效；以板端回读值和版本为准' if ball else
            '原图模式保留参数与当前数值；切换到小球识别并完成回读后可操作')
        self.targets.setEnabled(ball)
        self.record.setEnabled(ball and self.is_connected)
        confirmed = self.is_connected and mode is not None and view in (RAW_VIEW, BALL_VIEW)
        self.algorithm_box.setEnabled(confirmed and not self.panel_writing)
        self.algorithm_box.setToolTip('0～9算法展示、10小球检测；应用与调色均等待实际显示代次的完整帧确认')
        self.view_switch_button.setEnabled(confirmed and not self.panel_writing)
        self.view_switch_button.setText('切换到原图' if ball else
            ('切换到小球识别' if confirmed or not self.is_connected else '等待显示模式确认…'))
        name = '小球检测' if ball else (ALGORITHMS[mode]+'展示' if demo else
            ('原图（后台继续计数）' if view == RAW_VIEW else '等待显示模式确认'))
        self.setWindowTitle('HX1P35A · '+name+' · Gigabit Vision')
        self.subtitle.setText('千兆以太网图像 · '+name)
        application = ALGORITHMS[mode] if mode is not None and mode < 10 else ('小球检测／计数' if mode == 10 else '待确认')
        self.state_label.setText(f'实际算法：{application} · Camera\n实际显示：{name} · 显示版本 {self.current_view_revision if confirmed else "—"}')
        self.query.setText('查询硬件状态' if ball else '查询显示状态')
        self.preview_check.setToolTip('取消后仅冻结本机画面，网络接收'+('和结果更新' if ball else '')+'继续')
        self.notice.setText('显示 '+name)

    def toggle_view(self):
        self.select_view(RAW_VIEW if self.ball_view_active() else BALL_VIEW)

    def begin_display_change(self, generation):
        self.ui_generation = generation
        self.current_view = None
        self.current_view_revision = None
        self.clear_ball_results()
        self.last_image = None
        self.last_video_frame = None
        self.image.clear()
        self.image.setText('等待板端完整帧确认切换…')
        self.screenshot.setEnabled(False)
        self.present_view(None)

    def select_view(self, target):
        if (not self.worker or not self.is_connected or
                self.current_view not in (RAW_VIEW, BALL_VIEW) or self.application_state is None or
                (self.application_state['mode'] == 10 and target == self.current_view)):
            return
        values = tuple(widget.value() for widget in (self.gamma_slider,self.contrast_slider,self.saturation_slider,self.brightness_slider))
        self.begin_display_change(self.worker.select_view(target, values))

    def show_view(self, state):
        if state['ui_generation'] != self.ui_generation:
            return
        if (self.current_view != state['view'] or self.current_view_revision != state.get('revision')):
            self.current_view = state['view']
            self.current_view_revision = state.get('revision')
            self.clear_ball_results()
            self.last_image = self.last_video_frame = None
            self.image.clear()
            self.image.setText('等待当前页面完整图像…')
            self.screenshot.setEnabled(False)
            self.present_view(self.current_view)

    def accept_results(self, generation):
        return (self.ball_view_active() and generation == self.ui_generation and
                self.worker is not None and self.worker.results_allowed.is_set())

    def on_message(self, text):
        if not self.ball_view_active() and ('工业参数' in text or text.startswith('状态请求')):
            return
        self.notice.setText(text)
        self.log_view.appendPlainText(text)

    def query_state(self):
        if self.worker and self.is_connected:
            if self.ball_view_active():
                self.worker.poll_event.set()
            else:
                self.worker.expected_view = None

    def check_freshness(self):
        now = time.monotonic()
        if self.last_panel_at is not None and now-self.last_panel_at > 2:
            self.roi_box.setEnabled(False)
        if self.ball_view_active() and self.last_snapshot_at is not None and now-self.last_snapshot_at > 2:
            if not self.summary.text().startswith('【状态已过期】'):
                self.summary.setText('【状态已过期】'+self.summary.text())
                self.face_label.setText('【状态已过期】'+self.face_label.text())
                self.application_status.setText('【状态已过期】'+self.application_status.text())
                self.targets.setEnabled(False)
        video = '未收到' if self.last_frame_at is None else ('已超时' if now-self.last_frame_at > 2 else '正常')
        state = '未收到' if self.last_snapshot_at is None else ('已超时' if now-self.last_snapshot_at > 2 else '正常')
        if self.is_connected:
            self.network_label.setText(f'UDP：视频{video}'+(f' / 结果{state}' if self.ball_view_active() else '')+'（PHY 状态未回传）')

    def show_frame(self, image, metadata):
        if (metadata['ui_generation'] != self.ui_generation or metadata['view'] != self.current_view or
                metadata['revision'] != self.current_view_revision or self.application_state is None or
                metadata['mode'] != self.application_state['mode']):
            return
        frame_id = metadata['frame_id']
        self.last_frame_at = time.monotonic()
        self.last_video_frame = frame_id
        self.record_event(dict(type='video',received_unix=time.time(),video_frame_id=frame_id))
        if self.preview_check.isChecked():
            self.last_image=image
            self.video_info.setText(f'视频frameID：{frame_id}（网络输出序号）')
            self.screenshot.setEnabled(True); self.draw_image()

    def draw_image(self):
        if self.last_image is not None:
            self.image.setPixmap(QPixmap.fromImage(self.last_image).scaled(self.image.size(),Qt.KeepAspectRatio,Qt.SmoothTransformation))

    def resizeEvent(self,event):
        super().resizeEvent(event);self.draw_image()

    def show_snapshot(self, state, generation):
        if not self.accept_results(generation):
            return
        self.last_snapshot_at = time.monotonic()
        self.last_snapshot = state
        counts,face=state['counts'],state['face']
        mode = '等待人脸解锁' if not face['unlocked'] else ('暂停计数' if state['paused'] else '运行计数')
        self.summary.setText(f"{mode}  ·  红 {counts['red']} / 绿 {counts['green']} / 黄 {counts['yellow']}\n"
            f"总数 {counts['total']}  ·  E候选拒绝 {counts['E']}（不是错误球数）  ·  当前轨迹 {state['diagnostic']['live']}/4")
        face_status = '故障' if face['fault'] else ('已解锁' if face['unlocked'] else
            ('等待提交解锁' if face['pending'] else ('扫描中' if face['busy'] else '等待确认')))
        face_box = str(tuple(face['box'])) if face['box_valid'] else '无有效框'
        if face.get('enabled') is False:
            self.face_label.clear()
            self.face_label.hide()
            self.setWindowTitle('HX1P35A · 小球计数 · Gigabit Vision')
        else:
            self.face_label.show()
            self.face_label.setText(f"人脸：{face_status}  ·  连续确认 {face['confirmed']}/3  ·  框 {face_box}\n"
                f"ROI {face['roi_id']} / 采样 {face['sample']}  ·  Haar候选窗 {face['raw_count']}（不是人数）")
            self.setWindowTitle('HX1P35A · 人脸与小球 · Gigabit Vision')
        if self.panel_state is None:
            self.roi_enable.setChecked(face['unlocked']); self.strict.setChecked(state['strict'])
        else:
            self.render_panel_summary()
        reason = state['diagnostic']['reason']
        warning = {1:'扫描故障，本任务无效', 2:'候选/轨迹容量不足，可能漏计（共享4轨迹）',
                   5:'处理未完成，当前任务未接收', 7:'视频输入链异常'}.get(reason, f'诊断代码 {reason}' if reason else '诊断正常')
        self.application_status.setText(f"Camera / COUNT4  ·  {'颜色掩膜' if state['mask'] else '原图'} / "
            f"{'STRICT' if state['strict'] else 'NORMAL'}\n{warning}；相机诊断见完整结果 JSON")
        self.targets.setEnabled(True)
        for row, box in enumerate(state['boxes']):
            values = ['—']*4
            if box['valid']:
                values = [{0:'无',1:'红色',2:'黄色',3:'绿色'}[box['color']],
                    ('预测' if box['status']==2 else ('待确认' if box.get('quality_pending') else ('良品' if box.get('good') else '次品'))) if self.panel_state else {0:'无',1:'实际观测',2:'预测'}[box['status']],
                    str(tuple(box['center'])),str(tuple(box['box']))]
            for column,value in enumerate(values,1):
                self.targets.item(row,column).setText(value)
        self.details.setPlainText(json.dumps(state,ensure_ascii=False,indent=2))
        self.record_event(dict(type='snapshot',received_unix=time.time(),
                                 last_received_video_frame_id=self.last_video_frame,state=state))

    def show_application(self, state):
        if state.get('ui_generation') != self.ui_generation:
            return
        if self.application_state is not None and self.application_state['mode'] != state['mode']:
            self.current_view = None
            self.current_view_revision = None
            self.clear_ball_results()
            self.last_image = self.last_video_frame = None
            self.image.clear()
            self.screenshot.setEnabled(False)
        self.application_state = state
        self.algorithms.setCurrentIndex(self.algorithms.findData(state['mode']))
        self.present_view(self.current_view)

    def submit(self, command, value):
        if command == 'source' and value == 0:
            self.on_message('当前使用 Camera；PC Image 回放尚未启用')

    def apply_selected_mode(self):
        self.queue_application(self.algorithms.currentData())

    def queue_application(self, mode):
        if (not self.worker or not self.is_connected or self.application_state is None or
                self.current_view is None or self.panel_writing):
            return
        values = tuple(widget.value() for widget in (self.gamma_slider,self.contrast_slider,self.saturation_slider,self.brightness_slider))
        try:
            generation = self.worker.select_application(mode, values)
        except ValueError as error:
            QMessageBox.warning(self, '图像参数', str(error))
            return
        self.begin_display_change(generation)

    def apply_tone(self):
        self.queue_application(9)

    def reset_editor(self):
        for widget,value in zip((self.gamma_slider,self.contrast_slider,self.saturation_slider,self.brightness_slider),(100,100,100,0)):
            widget.setValue(value)
        self.tone_timer.stop()
        self.apply_tone()

    def show_original(self):
        self.queue_application(0)

    def show_panel(self, state, generation):
        if not self.accept_results(generation):
            return
        self.last_panel_at = time.monotonic()
        refill = self.panel_state is None or state['revision'] != self.panel_state['revision'] or state['capability'] != self.panel_state['capability'] or state.get('applied')
        self.panel_state = state
        self.profile_notice.setText('工业参数能力已确认：03区通过Ethernet应用参数、清零并回读；02区选择算法与调色。PC图片回放尚未启用。')
        self.keys_hint.setText('长按切档已删除；页面使用左侧最下方按钮切换。\n板载短按功能以配套bit操作说明为准。')
        self.roi_box.setTitle('03  工业检测与计数 · Ethernet')
        self.roi_box.setToolTip('参数在板端帧边界整组生效；以板端回读值和版本为准')
        self.roi_box.setEnabled(self.ball_view_active() and self.is_connected and not self.panel_writing)
        extended = state['capability'] == 7
        self.target_color.model().item(self.target_color.findData(0)).setEnabled(extended)
        self.discovery_side.setEnabled(extended); self.discovery_area.setEnabled(extended)
        shape_rule = {0:'不限制形状', 1:'非圆形为次品', 2:'非实心矩形为次品'}[state['config'][2]]
        self.inspection_hint.setText(('可选择单色，或红黄绿全部；三色共享最多4个目标。\n' if extended else '仅统计选定颜色，其他颜色忽略；最多同时跟踪4个目标。\n')+
            f'同一目标越线计一次。{shape_rule}；尺寸/面积不符为次品。\n'
            '框：绿=良品，红=次品，灰=待确认或预测；框色不代表物体颜色。\n'
            '待确认目标不计数。尺寸单位为像素，需固定机位标定。参数变化会开始新一批计数。')
        if refill:
            values = state['config']
            self.roi_enable.setChecked(bool(values[0]))
            self.target_color.setCurrentIndex(self.target_color.findData(values[1]))
            self.target_shape.setCurrentIndex(self.target_shape.findData(values[2]))
            self.strict.setChecked(bool(values[3] & 1))
            self.border.setChecked(bool(values[3] & 2))
            for widget, value in zip(self.coords+self.size_limits, values[4:14]):
                widget.setValue(value)
            self.discovery_side.setValue(values[14]); self.discovery_area.setValue(values[15])
        self.render_panel_summary()
        self.record_event(dict(type='industrial', received_unix=time.time(), state=state))

    def render_panel_summary(self):
        if not self.ball_view_active():
            return
        state = self.panel_state
        if state is not None:
            snapshot = self.last_snapshot
            mode = '检测关闭' if not state['config'][0] else ('暂停计数（识别继续）' if snapshot and snapshot['paused'] else '检测运行')
            text = f"{mode}  ·  良品 {state['good']} / 次品 {state['bad']}（参数通道读数）\n"
            if snapshot:
                counts = snapshot['counts']
                text += (f"红 {counts['red']} / 绿 {counts['green']} / 黄 {counts['yellow']}  ·  总数 {counts['total']}\n"
                         f"E候选拒绝 {counts['E']}（不是次品过线数）  ·  当前轨迹 {snapshot['diagnostic']['live']}/4\n")
            self.summary.setText(text+f"{'红黄绿同时检测' if state['config'][1]==0 else '仅统计选定颜色'}，共享最多4轨迹、同一目标越线一次  ·  板端版本 {state['revision']}")

    def set_writing(self, active):
        self.panel_writing = active
        self.present_view(self.current_view)

    def apply_roi(self):
        if not self.ball_view_active() or not self.worker or self.panel_state is None or self.panel_writing:
            return
        values = (int(self.roi_enable.isChecked()), self.target_color.currentData(), self.target_shape.currentData(),
            int(self.strict.isChecked()) | (int(self.border.isChecked()) << 1),
            *(widget.value() for widget in self.coords+self.size_limits))
        if self.panel_state['capability'] == 7:
            values += (self.discovery_side.value(), self.discovery_area.value())
        try:
            pack_config(values, self.panel_state['capability'])
        except ValueError as error:
            QMessageBox.warning(self, '检测参数', str(error))
            return
        self.set_writing(True)
        self.worker.jobs.put((self.ui_generation, CONFIGURE, values))

    def clear_industrial(self):
        if self.ball_view_active() and self.worker and self.panel_state is not None and not self.panel_writing:
            self.set_writing(True)
            self.worker.jobs.put((self.ui_generation, CLEAR, None))

    def save_frame(self):
        if self.last_image is None:
            return
        path,_ = QFileDialog.getSaveFileName(self,'保存 FPGA 完整帧','fpga_frame.png','PNG (*.png)')
        if path:
            if self.last_image.save(path):
                self.log_view.appendPlainText('已保存完整帧：'+path)
            else:
                QMessageBox.warning(self,'保存失败',path)

    def record_event(self, record):
        if not self.ball_view_active():
            return
        try:
            self.recorder.write(record)
        except OSError as error:
            self.recorder.close();self.record.setChecked(False)
            self.notice.setText('记录已停止：'+str(error))

    def toggle_recording(self, enabled):
        if enabled and not self.ball_view_active():
            self.record.setChecked(False)
            return
        if enabled:
            path,_=QFileDialog.getSaveFileName(self,'保存板端结果记录','ball_face_results.jsonl','JSONL (*.jsonl)')
            if not path:
                self.record.setChecked(False);return
            try:
                self.recorder.open(path)
                self.recorder.write(dict(type='session',schema=1,board_ip=self.peer.text(),
                    note='Video frame ID and OSD commit sequence are separate; no exact DDR/result frame correspondence is claimed.'))
            except OSError as error:
                self.notice.setText(str(error));self.record.setChecked(False)
        else:
            self.recorder.close()

    def closeEvent(self,event):
        if self.worker:
            self.worker.stop()
            if not self.worker.wait(3000):
                self.notice.setText('正在等待网卡操作结束，请稍后关闭。')
                event.ignore();return
        self.recorder.close();super().closeEvent(event)


if __name__=='__main__':
    app=QApplication(sys.argv);window=Window();window.show()
    if '--smoke' in sys.argv:
        def finish():
            target=Path(__file__).resolve().parents[1]/'reports'/'pc_app_smoke.png'
            target.parent.mkdir(parents=True,exist_ok=True)
            if not window.grab().save(str(target)):
                app.exit(2);return
            print(f'PASS GUI smoke: {target}')
            app.quit()
        QTimer.singleShot(400,finish)
    sys.exit(app.exec())
