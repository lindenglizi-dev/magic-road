import binascii
import copy
import json
import os
from pathlib import Path
import sys
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'deps')]
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
from communication.protocol import Command, Decoder, encode, crc16
from config.loader import load_config
from PySide6.QtWidgets import QApplication, QGroupBox
from services.fpga_controller import FpgaController
from gui.main_window import MainWindow

APP = QApplication.instance() or QApplication([])

def wait_for(predicate, timeout=3):
    end = time.monotonic() + timeout
    while time.monotonic() < end:
        APP.processEvents()
        if predicate(): return
        time.sleep(.005)
    raise AssertionError('Timed out')

class UpperTests(unittest.TestCase):
    def setUp(self):
        self.config = load_config(ROOT / 'config/algorithms.json')

    def test_crc_stream_recovery(self):
        self.assertEqual(crc16(b'123456789'), 0x29b1)
        body = bytes([2, 19, 1, 1, 5])
        packet = b'\xaa\x55' + body + binascii.crc_hqx(body, 0xffff).to_bytes(2, 'little') + b'\r\n'
        self.assertEqual(encode(Command.MODE, b'\x05', 19), packet)
        for split in range(len(packet) + 1):
            decoder = Decoder()
            frames = decoder.feed(packet[:split], 0) + decoder.feed(packet[split:], .001)
            self.assertEqual([f.data for f in frames], [b'\x05'])
        broken = bytearray(packet); broken[7] ^= 1
        decoder = Decoder()
        frames = decoder.feed(b'noise' + broken + packet + packet)
        self.assertEqual(len(frames), 2)
        decoder.feed(packet[:6], 0)
        self.assertEqual(len(decoder.feed(packet, 1)), 1)
        self.assertEqual(Decoder().feed(encode(Command.RESULT, b'\xaa\x55\r\n'))[0].data, b'\xaa\x55\r\n')

    def test_configuration_add_remove_and_validation(self):
        config = copy.deepcopy(self.config)
        config['modes'].pop()
        config['modes'].append({'id':'custom', 'name':'自定义算法', 'command':15})
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'algorithms.json';path.write_text(json.dumps(config), encoding='utf-8')
            loaded = load_config(path)
            controller = FpgaController(loaded);window = MainWindow(controller, loaded)
            self.assertEqual([b.text() for b in window.mode_buttons], [m['name']+('\n'+m['english'] if m.get('english') else '') for m in loaded['modes']])
            group = next(g for g in window.findChildren(QGroupBox) if g.title() == '图像处理模式')
            algorithms = [m for m in loaded['modes'] if m.get('role') != 'source']
            for index, item in enumerate(algorithms):
                actual = group.layout().itemAtPosition(index//3, index%3).widget()
                self.assertTrue(actual.text().startswith(item['name']))
            window.close()
            config['modes'][-1]['command'] = 0
            path.write_text(json.dumps(config), encoding='utf-8')
            with self.assertRaises(ValueError): load_config(path)

    def test_serial_loopback_lifecycle_and_gui(self):
        controller = FpgaController(self.config); manager = controller.serial
        window = MainWindow(controller, self.config)
        window.ports.addItem('COM99 — test', 'COM99')
        window.ports.setCurrentIndex(window.ports.count()-1)
        window.ports.setEditText('loop://')
        self.assertEqual(window.current_port(), 'loop://')
        received=[];sent=[]
        manager.received.connect(received.append);manager.transmitted.connect(sent.append)
        try:
            for _ in range(2):
                manager.open('loop://', 115200)
                wait_for(lambda: manager.connected)
                self.assertTrue(all(b.isEnabled() for b in window.mode_buttons))
                controller.set_mode('sharpen')
                wait_for(lambda: len(received) and b''.join(received)==b''.join(sent))
                self.assertEqual(Decoder().feed(b''.join(received))[-1].data, b'\x05')
                self.assertIn('实际模式请查看 HDMI', window.mode.text())
                manager.close();wait_for(lambda: manager.worker is None)
                self.assertFalse(any(b.isEnabled() for b in window.mode_buttons))
                received.clear();sent.clear()
            with self.assertRaises(RuntimeError): controller.set_mode('original')
            errors=[];manager.error.connect(errors.append)
            manager.open('invalid-protocol://',115200)
            wait_for(lambda: manager.worker is None)
            self.assertTrue(errors)
        finally:
            manager.close()
            wait_for(lambda: manager.worker is None)
            window.close()

if __name__ == '__main__':
    unittest.main(verbosity=2)
