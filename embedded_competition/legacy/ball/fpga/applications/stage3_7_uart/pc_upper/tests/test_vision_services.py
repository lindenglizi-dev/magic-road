"""Software-only fixtures. These results never assert live HDMI/FPGA success."""
import os,sys,tempfile,time,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'deps')]
os.environ.setdefault('QT_QPA_PLATFORM','offscreen')
import numpy as np
import cv2
from PySide6.QtWidgets import QApplication
from services.roi_geometry import RoiGeometry,Roi
from services.screenshot_manager import save_screenshot
from services.video_capture import VideoCaptureWorker
from services.settings_store import SettingsStore
from gui.roi_overlay import VideoView
APP=QApplication.instance() or QApplication([])

class VisionServicesTest(unittest.TestCase):
    def test_roi_scaling_letterbox_reverse_and_resize(self):
        g=RoiGeometry((1920,1080),(1920,1080),(1000,1000))
        self.assertEqual(g.display,(0.,218.75,1000.,562.5))
        self.assertIsNone(g.source_point(50,100))
        self.assertEqual(g.select((250,359.375),(750,640.625)),Roi(480,270,1440,810))
        self.assertEqual(g.select((750,640.625),(250,359.375)),Roi(480,270,1440,810))
        resized=RoiGeometry((1920,1080),(1280,720),(960,540))
        self.assertEqual(resized.select((240,135),(720,405)),Roi(320,180,960,540))
        with self.assertRaises(ValueError):RoiGeometry((640,480),(1920,1080),(640,480)).source_point(10,10)
        padded=RoiGeometry((1920,1200),(1920,1080),(960,600),(0,60,1920,1080))
        self.assertEqual(padded.select((0,30),(960,570)),Roi(0,0,1920,1080))

    def test_screenshot_is_original_frame_and_unicode_path(self):
        frame=np.zeros((72,128,3),dtype=np.uint8);frame[:,:,1]=117
        before=frame.copy();view=VideoView();view.set_frame(frame);view.roi=Roi(5,5,25,25);view.update()
        with tempfile.TemporaryDirectory() as folder:
            path=save_screenshot(frame,Path(folder)/'截图')
            decoded=cv2.imdecode(np.fromfile(path,dtype=np.uint8),cv2.IMREAD_COLOR)
            np.testing.assert_array_equal(decoded,before)
            self.assertEqual(decoded.shape,(72,128,3))
        np.testing.assert_array_equal(frame,before)

    def test_capture_reports_actual_frame_not_requested_dimensions(self):
        class FixtureCapture:
            released=False
            def __init__(self,*args):pass
            def isOpened(self):return True
            def set(self,*args):return True
            def read(self):time.sleep(.005);return True,np.zeros((72,128,3),dtype=np.uint8)
            def release(self):FixtureCapture.released=True
        worker=VideoCaptureWorker(0,1920,1080,factory=FixtureCapture)
        stats=[];worker.stats.connect(lambda w,h,f:stats.append((w,h)))
        worker.start();deadline=time.monotonic()+2
        while not stats and time.monotonic()<deadline:APP.processEvents();time.sleep(.005)
        worker.stop();self.assertTrue(worker.wait(2000));APP.processEvents()
        self.assertEqual(stats[0],(128,72));self.assertTrue(FixtureCapture.released)
        self.assertEqual(worker.snapshot().shape,(72,128,3));self.assertFalse(worker.snapshot().flags.writeable)

    def test_settings_roundtrip(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'settings.json';store=SettingsStore(path);store.set('device',3)
            self.assertEqual(SettingsStore(path).get('device'),3)

if __name__=='__main__':unittest.main(verbosity=2)
