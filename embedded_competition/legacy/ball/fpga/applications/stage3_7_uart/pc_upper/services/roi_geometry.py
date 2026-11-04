"""Pixel-edge coordinates: [x0,x1) × [y0,y1), top-left origin.

Display letterboxes belong to the GUI. A separate capture content rectangle
can describe a known capture-card padding/crop mapping; never guess a crop.
"""
from dataclasses import dataclass
import math

@dataclass(frozen=True)
class Roi:
    x0: int
    y0: int
    x1: int
    y1: int

    def validate(self, width, height):
        if not 0 <= self.x0 < self.x1 <= width or not 0 <= self.y0 < self.y1 <= height:
            raise ValueError(f'ROI需满足0≤X1<X2≤{width}、0≤Y1<Y2≤{height}，终点不包含')
        return self

class RoiGeometry:
    def __init__(self, capture_size, source_size, widget_size, content=None):
        self.cw, self.ch = capture_size; self.sw, self.sh = source_size
        ww, wh = widget_size
        if min(self.cw, self.ch, self.sw, self.sh, ww, wh) <= 0: raise ValueError('无效视频尺寸')
        if ww/self.cw <= wh/self.ch:
            dw, dh = float(ww), ww*self.ch/self.cw
        else:
            dw, dh = wh*self.cw/self.ch, float(wh)
        self.display = ((ww-dw)/2, (wh-dh)/2, dw, dh)
        self.content = content or (0, 0, self.cw, self.ch)
        x, y, width, height = self.content
        if min(width, height) <= 0 or x < 0 or y < 0 or x+width > self.cw or y+height > self.ch:
            raise ValueError('采集内容矩形超出视频帧')
        self.mapping_known = abs((width/height)/(self.sw/self.sh)-1) < .01

    def source_point(self, x, y, clamp=False):
        if not self.mapping_known: raise ValueError('采集内容比例与FPGA源不符，需确认裁剪/补边范围后再框选')
        dx, dy, dw, dh = self.display
        cx, cy, cw, ch = self.content
        px = (x-dx)*self.cw/dw; py = (y-dy)*self.ch/dh
        if not clamp and not (cx <= px <= cx+cw and cy <= py <= cy+ch): return None
        px = min(max(px, cx), cx+cw); py = min(max(py, cy), cy+ch)
        return ((px-cx)*self.sw/cw, (py-cy)*self.sh/ch)

    def select(self, start, end):
        a = self.source_point(*start)
        if a is None: raise ValueError('请从实际画面内容内开始框选')
        b = self.source_point(*end, clamp=True)
        x0, x1 = sorted((a[0], b[0])); y0, y1 = sorted((a[1], b[1]))
        if x1-x0 < 1e-8 or y1-y0 < 1e-8: raise ValueError('ROI宽高必须大于0')
        def snap(value):
            return round(value) if abs(value-round(value)) < 1e-8 else value
        roi = Roi(max(0, math.floor(snap(x0))), max(0, math.floor(snap(y0))),
                  min(self.sw, math.ceil(snap(x1))), min(self.sh, math.ceil(snap(y1))))
        return roi.validate(self.sw, self.sh)

    def display_roi(self, roi):
        dx, dy, dw, dh = self.display; cx, cy, cw, ch = self.content
        return (dx+(cx+roi.x0/self.sw*cw)/self.cw*dw,
                dy+(cy+roi.y0/self.sh*ch)/self.ch*dh,
                (roi.x1-roi.x0)/self.sw*cw/self.cw*dw,
                (roi.y1-roi.y0)/self.sh*ch/self.ch*dh)
