"""Typed V2 extensions. Every field is little endian; MODE=01 is unchanged."""
from dataclasses import dataclass
from enum import IntFlag, IntEnum
import struct
from services.roi_geometry import Roi

class Capability(IntFlag):
    MODE_ACK=1
    ROI=2
    IMAGE_UPLOAD=4
    SOURCE_SWITCH=8
    NATIVE_1080_IMAGE=16

class ErrorCode(IntEnum):
    OK=0
    UNSUPPORTED=1
    BAD_LENGTH=2
    RANGE=3
    BUSY=4
    NO_IMAGE=5
    BAD_OFFSET=6
    BAD_CRC=7
    NOT_READY=8
    TIMEOUT=9

COLOR_NAMES={0:'UNKNOWN',1:'RED',2:'YELLOW',3:'GREEN',4:'BLUE'}
IMAGE_WIDTH=1920
IMAGE_HEIGHT=1080
IMAGE_BYTES=IMAGE_WIDTH*IMAGE_HEIGHT*2
IMAGE_CHUNK=224

@dataclass(frozen=True)
class DeviceStatus:
    width:int
    height:int
    capabilities:int
    mode:int
    source:int
    image_valid:bool
    uploaded:int
    roi_revision:int

    @classmethod
    def decode(cls, data):
        if len(data)!=18:raise ValueError('FPGA状态长度错误')
        schema,w,h,caps,mode,source,valid,uploaded,revision=struct.unpack('<BHHIBBBIH',data)
        if schema!=1 or w<4 or h<2 or w%4 or source>1:raise ValueError('FPGA状态字段错误')
        return cls(w,h,caps,mode,source,bool(valid),uploaded,revision)

@dataclass(frozen=True)
class RoiConfig:
    roi:Roi
    enabled:bool=True
    traffic:bool=True
    strict:bool=False
    border:bool=False

    def encode(self,width,height):
        self.roi.validate(width,height)
        return struct.pack('<BBBBHHHH',self.enabled,self.traffic,self.strict,self.border,
                           self.roi.x0,self.roi.y0,self.roi.x1,self.roi.y1)

    @classmethod
    def decode(cls,data):
        if len(data)!=12:raise ValueError('ROI配置长度错误')
        e,t,s,m,x0,y0,x1,y1=struct.unpack('<BBBBHHHH',data)
        if max(e,t,s,m)>1:raise ValueError('ROI标志错误')
        return cls(Roi(x0,y0,x1,y1),bool(e),bool(t),bool(s),bool(m))

@dataclass(frozen=True)
class RoiStatus:
    config:RoiConfig
    revision:int
    frame:int
    result:int
    warmed_up:bool
    counts:tuple

    @classmethod
    def decode(cls,data):
        if len(data)!=37 or data[0]!=1:raise ValueError('ROI状态格式错误')
        config=RoiConfig.decode(data[1:13])
        revision,frame,result,warm,r,y,g,b=struct.unpack('<HIBBIIII',data[13:])
        if result not in COLOR_NAMES:raise ValueError('未知FPGA颜色编码')
        return cls(config,revision,frame,result,bool(warm),(r,y,g,b))

def image_begin(transfer_id,crc):
    return struct.pack('<IHHBII',transfer_id,IMAGE_WIDTH,IMAGE_HEIGHT,1,IMAGE_BYTES,crc)
