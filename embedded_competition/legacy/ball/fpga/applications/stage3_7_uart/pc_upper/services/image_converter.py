"""Image transport preparation only; FPGA algorithms are never executed here."""
from dataclasses import dataclass
from pathlib import Path
import zlib
import cv2
import numpy as np
from PySide6.QtCore import QThread,Signal
from communication.image_protocol import IMAGE_WIDTH,IMAGE_HEIGHT

@dataclass(frozen=True)
class ConvertedImage:
    path:str
    source_size:tuple
    file_bytes:int
    target_size:tuple
    preview:object
    data:bytes
    crc:int

def rgb565_bytes(bgr):
    values=bgr.astype(np.uint16)
    words=((values[:,:,2]>>3)<<11)|((values[:,:,1]>>2)<<5)|(values[:,:,0]>>3)
    return words.astype('<u2').tobytes(order='C')

def convert_image(filename,fit='letterbox',target=(IMAGE_WIDTH,IMAGE_HEIGHT)):
    path=Path(filename)
    if path.suffix.lower() not in ('.png','.jpg','.jpeg','.bmp'):raise ValueError('请选择PNG/JPEG/BMP图片')
    image=cv2.imdecode(np.fromfile(path,dtype=np.uint8),cv2.IMREAD_COLOR)
    if image is None:raise ValueError('无法解码图片')
    sh,sw=image.shape[:2];tw,th=target
    if min(sw,sh,tw,th)<=0:raise ValueError('图片尺寸无效')
    scale=(min if fit=='letterbox' else max)(tw/sw,th/sh)
    if fit not in ('letterbox','crop'):raise ValueError('不支持的适配方式')
    width=max(1,round(sw*scale));height=max(1,round(sh*scale))
    resized=cv2.resize(image,(width,height),interpolation=cv2.INTER_AREA if scale<1 else cv2.INTER_LINEAR)
    if fit=='letterbox':
        preview=np.zeros((th,tw,3),dtype=np.uint8)
        x=(tw-width)//2;y=(th-height)//2;preview[y:y+height,x:x+width]=resized
    else:
        x=(width-tw)//2;y=(height-th)//2;preview=np.ascontiguousarray(resized[y:y+th,x:x+tw])
    data=rgb565_bytes(preview);preview.setflags(write=False)
    return ConvertedImage(str(path), (sw,sh),path.stat().st_size,(tw,th),preview,data,zlib.crc32(data)&0xffffffff)

class ImageLoadWorker(QThread):
    loaded=Signal(object)
    failed=Signal(str)
    def __init__(self,path,fit):super().__init__();self.path=path;self.fit=fit
    def run(self):
        try:self.loaded.emit(convert_image(self.path,self.fit))
        except (ValueError,OSError,cv2.error) as exc:self.failed.emit(str(exc))
