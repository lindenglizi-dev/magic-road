"""Software fixtures, not a live FPGA or a captured HDMI result."""
import os,sys,struct,tempfile,time,unittest,zlib
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'deps')]
os.environ.setdefault('QT_QPA_PLATFORM','offscreen')
import cv2,numpy as np
from PySide6.QtCore import QObject,Signal
from PySide6.QtWidgets import QApplication
from communication.protocol import Command,Frame,Decoder,encode
from communication.image_protocol import DeviceStatus,Capability,RoiConfig,RoiStatus,IMAGE_BYTES
from communication.request_scheduler import RequestScheduler
from services.image_converter import rgb565_bytes,convert_image
from services.image_uploader import ImageUploader
from services.roi_geometry import Roi
from services.roi_controller import RoiController
APP=QApplication.instance() or QApplication([])

class SerialFixture(QObject):
    state_changed=Signal(str)
    connected=True
    def __init__(self):super().__init__();self.sent=[]
    def send(self,packet):self.sent.append(packet)

class ImageControlTest(unittest.TestCase):
    def setUp(self):
        self.serial=SerialFixture();self.scheduler=RequestScheduler(self.serial)
        self.device=DeviceStatus(1280,720,31,0,0,False,0,0)
        self.controller=SimpleNamespace(device=self.device,scheduler=self.scheduler)
    def tearDown(self):self.scheduler.timer.stop()
    def acknowledge(self,data=b'',code=0):
        r=self.scheduler.active;self.assertIsNotNone(r)
        self.scheduler.receive(Frame(r.seq,Command.ACK if not code else Command.NACK,bytes([r.command,code])+data))
    def test_565_native_size_order_crc_and_fit(self):
        colors=np.array([[[0,0,255],[0,255,0],[255,0,0],[255,255,255]]],dtype=np.uint8)
        self.assertEqual(rgb565_bytes(colors),bytes.fromhex('00f8e0071f00ffff'))
        with tempfile.TemporaryDirectory() as folder:
            file=Path(folder)/'图片.png';cv2.imencode('.png',np.full((100,100,3),(0,0,255),np.uint8))[1].tofile(str(file))
            image=convert_image(file)
            self.assertEqual(len(image.data),4147200);self.assertEqual(image.target_size,(1920,1080))
            self.assertEqual(image.crc,zlib.crc32(image.data));self.assertEqual(image.data[:2],b'\0\0')
            self.assertEqual(image.preview[540,960,2],255)
            cropped=convert_image(file,'crop');self.assertEqual(cropped.data[:2],b'\x00\xf8')
    def test_scheduler_retry_identity_matching_and_disconnect(self):
        result=[];self.scheduler.submit(Command.ROI_QUERY,callback=lambda *r:result.append(r),retries=1)
        r=self.scheduler.active;self.scheduler.receive(Frame(r.seq,Command.ACK,b'\x01\x00'))
        self.assertIs(self.scheduler.active,r)
        r.sent_at=0;self.scheduler._tick();self.assertEqual(self.serial.sent[0],self.serial.sent[1])
        r.sent_at=0;self.scheduler._tick();self.assertFalse(result[0][0]);self.assertIsNone(self.scheduler.active)
        self.scheduler.submit(Command.GET_STATUS,callback=lambda *r:result.append(r))
        self.serial.connected=False;self.serial.state_changed.emit('断开');self.assertFalse(result[-1][0])
    def test_upload_full_1080_ack_order_end_and_exclusive_control(self):
        image=SimpleNamespace(data=b'\x00\xf8'*(1920*1080),crc=0)
        image.crc=zlib.crc32(image.data);up=ImageUploader(self.controller);results=[];up.finished.connect(lambda *r:results.append(r))
        up.start(image);self.assertEqual(self.scheduler.active.command,Command.IMAGE_BEGIN)
        with self.assertRaises(RuntimeError):self.scheduler.submit(Command.MODE,b'\x04')
        self.acknowledge(struct.pack('<I',up.transfer_id))
        packets=0
        while self.scheduler.active.command==Command.IMAGE_DATA:
            data=self.scheduler.active.data;tid,offset=struct.unpack('<II',data[:8])
            self.assertEqual(offset,up.offset);self.assertEqual(tid,up.transfer_id)
            self.assertEqual(data[8:],image.data[offset:offset+224]);self.assertEqual(len(Decoder().feed(self.serial.sent[-1])),1)
            packets+=1;self.acknowledge(struct.pack('<II',tid,offset+len(data)-8))
        self.assertEqual(packets,18515);self.assertEqual(up.offset,IMAGE_BYTES)
        self.assertTrue(up.busy);self.assertFalse(results)
        self.acknowledge(struct.pack('<II',up.transfer_id,image.crc))
        self.assertEqual(results[0][0],True);self.assertIsNone(self.scheduler.exclusive)
    def test_upload_cancel_and_bad_ack_do_not_report_success(self):
        image=SimpleNamespace(data=bytes(IMAGE_BYTES),crc=0)
        up=ImageUploader(self.controller);result=[];up.finished.connect(lambda *r:result.append(r))
        up.start(image);self.acknowledge(struct.pack('<I',up.transfer_id));up.cancel()
        self.acknowledge(struct.pack('<II',up.transfer_id,224))
        self.assertEqual(self.scheduler.active.command,Command.IMAGE_ABORT);self.acknowledge(struct.pack('<I',up.transfer_id))
        self.assertFalse(result[-1][0]);self.assertFalse(up.busy)
        up.start(image);self.acknowledge(struct.pack('<I',up.transfer_id));self.acknowledge(bytes(8))
        self.assertFalse(up.busy);self.assertFalse(result[-1][0])
    def test_roi_draft_applied_only_after_hardware_status(self):
        controller=RoiController(self.controller);config=RoiConfig(Roi(1,2,320,180))
        controller.apply(config);self.assertIsNone(controller.applied)
        self.acknowledge(config.encode(1280,720));self.assertIsNone(controller.applied)
        body=b'\x01'+config.encode(1280,720)+struct.pack('<HIBBIIII',2,50,1,1,400,0,0,0)
        self.acknowledge(body);self.assertEqual(controller.applied.config,config);self.assertEqual(controller.applied.result,1)
        self.assertIsNone(controller.pending)
    def test_extended_protocol_crc_and_status_validation(self):
        packet=encode(Command.IMAGE_DATA,bytes(range(232)),255)
        self.assertEqual(Decoder().feed(packet)[0].data,bytes(range(232)))
        corrupt=bytearray(packet);corrupt[42]^=1;self.assertEqual(Decoder().feed(corrupt),[])
        payload=struct.pack('<BHHIBBBIH',1,1280,720,31,4,0,0,0,2)
        self.assertEqual(DeviceStatus.decode(payload).width,1280)
        with self.assertRaises(ValueError):DeviceStatus.decode(payload[:-1])

if __name__=='__main__':unittest.main(verbosity=2)
