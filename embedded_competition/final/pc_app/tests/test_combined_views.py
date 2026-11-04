
import os
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
import ast
from collections import deque
import hashlib
import json
from pathlib import Path
import socket
import struct
import sys
from unittest.mock import patch
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import main
from PySide6.QtWidgets import QApplication, QPushButton
from protocol import Decoder, FrameAssembler, Packet, VIDEO_HEADER, encode
from industrial import CONFIG, DEFAULT, CONFIGURE, CLEAR, READ, SET_VIEW, READ_VIEW, pack_config, unpack_config
from combined_protocol import (CONFIGURE_APPLICATION, CURVE_CHUNK, READ_APPLICATION,
    config_bytes, curve_chunks, gamma_curve, editor_curve)

OUT = ROOT.parent / 'build' / 'host_tests'


class Board:
    def __init__(self):
        self.mode = 10
        self.application_revision = self.display_revision = 0
        self.config = config_bytes(10)
        self.view = 1
        self.industrial = CONFIG.pack(*DEFAULT)
        self.panel_revision = 0
        self.good, self.bad = 17, 4
        self.token = 0
        self.calls = []
        self.curves = {0:bytearray(), 1:bytearray()}
        self.raw = bytearray(192)
        self.raw[0:2] = bytes((1, 8))
        self.raw[55] = 0x80
        self.raw[20:32] = struct.pack('<III', 5, 2, 3)
        self.raw[32:40] = struct.pack('<Q', 10)

    def reply(self, packet):
        command, data = packet.command, packet.data
        self.calls.append((command, data))
        if command == READ_APPLICATION:
            return bytes((command,0,2,self.mode))+struct.pack('<HI',self.application_revision,0)+self.config+bytes(8)
        if command in (CONFIGURE_APPLICATION, CURVE_CHUNK):
            request_id, revision = struct.unpack_from('<IH', data)
            assert revision == self.application_revision
            content = data[6:]
            assert len(content) == 24
            self.application_revision = (self.application_revision+1) & 65535
            if command == CURVE_CHUNK:
                kind, offset, count = content[:3]
                assert count == 16 and content[19:] == bytes(5)
                if offset == 0:
                    self.curves[kind].clear()
                assert offset == len(self.curves[kind])
                self.curves[kind].extend(content[3:19])
            else:
                self.mode = content[0]
                if content[1]:
                    assert len(self.curves[int(self.mode==9)]) == 256
                self.config = content[:1]+bytes(1)+content[2:]
                self.display_revision = (self.display_revision+1) & 16383
                if self.mode < 10:
                    self.view = 1
            return bytes((command,0,2,self.mode))+struct.pack('<HI',self.application_revision,request_id)+content+bytes(8)
        if command in (SET_VIEW, READ_VIEW):
            request_id = 0
            if command == SET_VIEW:
                request_id, revision, target = struct.unpack('<IHB', data)
                assert revision == self.display_revision and self.mode == 10
                if target != self.view:
                    self.display_revision = (self.display_revision+1) & 16383
                self.view = target
            return struct.pack('<5BHI', command,0,1,self.view,3,self.display_revision,request_id)
        assert self.mode == 10 and self.view == 1, 'inactive display sent ball request'
        if command in (READ, CONFIGURE, CLEAR):
            request_id = 0
            if command in (CONFIGURE, CLEAR):
                request_id, revision = struct.unpack_from('<IH', data)
                assert revision == self.panel_revision
                if command == CONFIGURE:
                    self.industrial = data[6:]
                else:
                    self.good = self.bad = 0
                self.panel_revision = (self.panel_revision+1) & 65535
            return bytes((command,0,1,7))+struct.pack('<HI',self.panel_revision,request_id)+self.industrial+struct.pack('<II',self.good,self.bad)
        assert command in (0x50,0x51)
        if command == 0x50:
            self.token += 1
            page = 0
        else:
            token, page = struct.unpack('<IB', data)
            assert token == self.token
        return bytes((command,0,1,page,4))+struct.pack('<I',self.token)+self.raw[page*48:(page+1)*48]


class FakeUDP:
    def __init__(self, board, peer):
        self.board, self.peer = board, peer
        self.incoming = deque()
        self.sent = []

    def sendto(self, data, peer):
        self.sent.append(data)
        for packet in Decoder().feed(data):
            self.incoming.append(encode(0x81,packet.seq,self.board.reply(packet)))

    def recvfrom(self, size):
        if not self.incoming:
            raise socket.timeout()
        return self.incoming.popleft(), self.peer


def packet(fid, index, tag, payload, width=1280, height=720, version=2):
    return VIDEO_HEADER.pack(b'HXIM',version,1,24,fid,width,height,index,width*height*2//len(payload),len(payload),tag)+payload


def check():
    app = QApplication.instance() or QApplication([])
    OUT.mkdir(parents=True, exist_ok=True)
                                                                              
    original = Path(__file__).parent / 'fixtures' / 'reference_transport.py'
    function = next(node for node in ast.parse(original.read_text(encoding='utf-8-sig')).body
                    if isinstance(node,ast.FunctionDef) and node.name=='rgb565_to_rgb')
    namespace = {'np':np}
    exec(compile(ast.Module(body=[function],type_ignores=[]),str(original),'exec'),namespace)
    words = np.arange(720*1280,dtype=np.uint32).astype('<u2').reshape(720,1280)
    assert np.array_equal(main.decode_rgb565(words.tobytes(),0),namespace['rgb565_to_rgb'](words.tobytes(),1280,720))
    fixture = Path(__file__).parent / 'fixtures' / 'camera_frame.rgb96.hex'
    rgb = np.frombuffer(bytes.fromhex(fixture.read_text()),dtype=np.uint8).reshape(720,1280,3)
    packed = (((rgb[:,:,0].astype(np.uint16)>>3)<<11) | ((rgb[:,:,1].astype(np.uint16)>>2)<<5) | (rgb[:,:,2]>>3)).astype('<u2').tobytes()
    chunks = [packed[index:index+1280] for index in range(0,len(packed),1280)]
    small = FrameAssembler(8,2,8)
    assert small.feed(packet(0,0,2,b'12345678',8,2)) is None
    assert small.feed(packet(0,1,3,b'12345678',8,2)) is None and small.invalid == 1
    assert small.feed(packet(0,0,0,b'12345678',8,2)) is None
    for fid, tag in ((0xffffffff,65534),(0,3)):
        small.frames.clear()
        for index in range(4):
            result = small.feed(packet(fid,index,tag,b'12345678',8,2))
        assert result[0] == fid and result[2] == (tag&1,tag>>2)

    board = Board()
    worker = main.Connection('127.0.0.1','127.0.0.1')
    worker.udp = FakeUDP(board,worker.peer)
    worker.next_hello = float('inf')
    window = main.Window()
    window.worker = worker
    window.is_connected = True
    worker.application.connect(window.show_application)
    worker.view.connect(window.show_view)
    worker.frame.connect(window.show_frame)
    worker.panel.connect(window.show_panel)
    worker.snapshot.connect(window.show_snapshot)
    worker.writing.connect(window.set_writing)
    records = []
    window.recorder.write = records.append
    fid = 0

    def frame(tag=None):
        nonlocal fid
        fid += 1
        tag = (board.display_revision<<2)|2|board.view if tag is None else tag
        for index in reversed(range(len(chunks))):
            worker.udp.incoming.append(packet(fid,index,tag,chunks[index]))
            worker.pump()

    def apply_application(mode, values=(70,125,80,32)):
        for widget,value in zip((window.gamma_slider,window.contrast_slider,window.saturation_slider,window.brightness_slider),values):
            widget.blockSignals(True);widget.setValue(value);widget.blockSignals(False)
        window.algorithms.setCurrentIndex(window.algorithms.findData(mode))
        next(button for button in window.findChildren(QPushButton) if button.text()=='应用算法').click()
        generation, selected, selected_values = worker.application_jobs.get_nowait()
        assert selected == mode and selected_values == values
        old_tag = (board.display_revision<<2)|2|board.view
        start = len(board.calls)
        worker.write_application(mode,values,generation)
        calls = [command for command,_ in board.calls[start:]]
        committed = calls.index(CONFIGURE_APPLICATION)
        assert calls[committed+1:committed+3] == [READ_APPLICATION,READ_VIEW]
        uploads = [data[6:] for command,data in board.calls[start:] if command==CURVE_CHUNK]
        assert len(uploads) == (16 if mode in (6,9) else 0)
        if uploads:
            expected = editor_curve(values[0],values[1],values[3]) if mode==9 else gamma_curve(values[0])
            assert b''.join(content[3:19] for content in uploads) == expected
        assert window.current_view is None and not worker.results_allowed.is_set()
        frame(old_tag)
        assert window.current_view is None and window.last_image is None
        frame()
        assert window.current_view == 1 and window.application_state['mode'] == mode
        return generation

    try:
        assert window.algorithms.count() == 11 and not window.algorithm_box.isEnabled()
        controls = window.view_switch_button.parentWidget().layout()
        assert controls.indexOf(window.view_switch_button) == controls.indexOf(window.application_box)+1
        worker.read_application();worker.read_view()
        assert window.current_view is None and not window.view_switch_button.isEnabled()
        frame()
        assert window.ball_view_active() and window.view_switch_button.text() == '切换到原图'
        worker.read_panel()
        state = worker.read_snapshot();worker.snapshot.emit(state,worker.ui_generation)
        assert window.roi_box.isEnabled() and window.last_snapshot == state and records
                                                                                 
        for color, shape, strict in ((1,1,False),(2,2,True),(3,0,False),(0,1,True)):
            window.target_color.setCurrentIndex(window.target_color.findData(color))
            window.target_shape.setCurrentIndex(window.target_shape.findData(shape))
            window.strict.setChecked(strict)
            for widget,value in zip(window.coords,(100,180,1100,600)):
                widget.setValue(value)
            for widget,value in zip(window.size_limits,(8,200,12,220,600,32)):
                widget.setValue(value)
            window.discovery_side.setValue(8);window.discovery_area.setValue(48)
            window.roi_apply.click()
            job_generation, command, config = worker.jobs.get_nowait()
            assert job_generation == worker.ui_generation
            assert command == CONFIGURE and config[1:3] == (color,shape)
            assert config[3]&1 == strict and config[4:14] == (100,180,1100,600,8,200,12,220,600,32)
            assert config[14:] == (8,48)
            worker.write_panel(command,config);worker.read_panel();app.processEvents()
            assert unpack_config(board.industrial) == config and window.roi_box.isEnabled()
        window.clear_counts_button.click()
        job_generation, command, config = worker.jobs.get_nowait()
        assert job_generation == worker.ui_generation
        assert command == CLEAR and config is None
        worker.write_panel(command,config);app.processEvents()
        assert board.good == board.bad == 0 and worker.panel_state['good'] == 0
        preserved = tuple(widget.value() for widget in window.coords+window.size_limits)+(window.target_color.currentData(),window.target_shape.currentData())
        old_generation = window.ui_generation
        window.view_switch_button.click()
        assert window.current_view is None and not worker.results_allowed.is_set()
        window.show_snapshot({'invalid':'stale generation must be rejected'},old_generation)
        worker.write_view(worker.view_job)
        frame()
        assert window.current_view == 0 and not window.roi_box.isEnabled() and not window.record.isEnabled()
        assert all(window.targets.item(row,1).text()=='—' for row in range(4))
        assert not window.summary.text() and not window.details.toPlainText()
        assert preserved == tuple(widget.value() for widget in window.coords+window.size_limits)+(window.target_color.currentData(),window.target_shape.currentData())
        records.clear();window.record_event({'type':'snapshot'});assert not records
        for command in range(0x50,0x55):
            sent = len(worker.udp.sent)
            try:worker.request(command)
            except main.ResultsCancelled:pass
            else:raise AssertionError('raw sent a ball request')
            assert len(worker.udp.sent) == sent
        window.show_panel({'invalid':'raw must reject before decoding'},window.ui_generation)
        for mode in range(11):
            apply_application(mode)
            if mode < 10:
                assert not worker.results_allowed.is_set() and not window.ball_view_active()
                assert not window.roi_box.isEnabled() and not window.record.isEnabled()
                window.show_snapshot({'invalid':'demo view1 is not ball'},window.ui_generation)
                assert not window.summary.text() and window.view_switch_button.text() == '切换到小球识别'
            else:
                assert worker.results_allowed.is_set() and window.ball_view_active()
                                                                            
        apply_application(4)
        start = len(board.calls)
        window.view_switch_button.click();worker.write_view(worker.view_job)
        assert CONFIGURE_APPLICATION in [c for c,_ in board.calls[start:]] and board.calls[-1][0] == SET_VIEW
        frame();assert window.ball_view_active()
        worker.read_panel();worker.snapshot.emit(worker.read_snapshot(),worker.ui_generation)
        window.preview_check.setChecked(False)
        image_key = window.last_image.cacheKey()
        frame()
        assert window.last_image.cacheKey() == image_key and window.last_video_frame == fid
        worker.snapshot.emit(worker.read_snapshot(),worker.ui_generation)
        assert window.last_snapshot is not None
        window.preview_check.setChecked(True)
                                                                             
        receive = worker.pump
        def cancel_receive():
            worker.select_application(0,(100,100,100,0))
            worker.replies.append(Packet(worker.seq,0x81,b'\x50\x00'))
        worker.pump = cancel_receive
        try:
            worker.request(0x50,parser=lambda *args:(_ for _ in ()).throw(AssertionError('parsed cancelled reply')))
        except main.ResultsCancelled:pass
        else:raise AssertionError('accepted old request after generation changed')
        worker.pump = receive
                                                                             
        previous_generation = window.ui_generation
        replacement = main.Connection('127.0.0.1','127.0.0.1')
        replacement.udp = FakeUDP(board,replacement.peer);replacement.next_hello = float('inf')
        window.worker = None;window.is_connected = False
        with patch.object(main,'Connection',return_value=replacement),patch.object(replacement,'start'):
            window.toggle_connection()
        replacement.online.emit(True)
        assert window.ui_generation > previous_generation and window.current_view is None
        window.show_frame(None,dict(ui_generation=previous_generation))
        window.show_snapshot({'invalid':'old connection'},previous_generation)
        assert window.last_image is None and window.last_snapshot is None and not window.view_switch_button.isEnabled()
        replacement.read_application();replacement.read_view()
        assert window.current_view is None and not replacement.results_allowed.is_set()
        window.worker = None
        window.show();app.processEvents()
        assert window.grab().save(str(OUT/'combined_host_offline.png'))
        print('PASS_COMBINED_VIEWS all11 modes; original tone uploads; application_then_view_read; full tagged actual-image frames; demo/raw no results; stale data cancellation; bottom button; reconnect; frozen preview; original raw RGB565')
        receipt = dict(passed=True,scope='Offline encoded protocol and actual Qt widgets; no FPGA/NIC actions',
                       source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
                           for name in ['main.py','layout.py','industrial.py','protocol.py','combined_protocol.py','tests/test_combined_views.py']})
        (OUT/'receipt.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
    finally:
        window.worker = None
        for timer in window.findChildren(main.QTimer):timer.stop()
        window.close()
        worker.deleteLater();window.deleteLater();app.processEvents()


if __name__ == '__main__':
    check()

