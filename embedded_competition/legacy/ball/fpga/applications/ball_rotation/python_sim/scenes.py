"""输入端场景发生器。只生成RGB图像，坐标及球身份不传给检测模块。"""

import math

import cv2
import numpy as np

BALL_RGB = {1: (232, 42, 52), 2: (238, 208, 38), 3: (40, 216, 102)}


def draw_ball(rgb, x, y, color, radius=34):
    """在输入画面上画有明暗与高光的实体；算法必须从像素重新定位。"""
    height, width = rgb.shape[:2]
    left, right = max(0, x-radius), min(width, x+radius+1)
    top, bottom = max(0, y-radius), min(height, y+radius+1)
    if left >= right or top >= bottom:
        return
    yy, xx = np.mgrid[top:bottom, left:right]
    nx, ny = (xx-x)/radius, (yy-y)/radius
    circle = nx*nx+ny*ny <= 1
    shade = np.clip(0.72-0.17*nx-0.19*ny, 0.42, 1.0)
    surface = np.array(BALL_RGB[color])*shade[..., None]
    highlight = np.exp(-((nx+0.30)**2+(ny+0.36)**2)/0.018)*0.70
    surface = surface*(1-highlight[..., None])+248*highlight[..., None]
    rgb[top:bottom, left:right][circle] = np.clip(surface[circle], 0, 255).astype(np.uint8)


def background(frame, width=1280, height=720):
    rgb = np.full((height, width, 3), (25, 33, 43), np.uint8)
    rgb[200:600] = (39, 46, 55)
    for x in range(-120, width+120, 120):
        offset = (frame*5) % 120
        cv2.line(rgb, (x+offset, 202), (x+offset, 598), (47, 55, 64), 2)
    cv2.line(rgb, (0, 198), (width-1, 198), (98, 109, 120), 4)
    cv2.line(rgb, (0, 602), (width-1, 602), (98, 109, 120), 4)
    for x in range(80, width, 180):
        cv2.arrowedLine(rgb, (x, 625), (x+65, 625), (91, 110, 125), 2, tipLength=0.22)
    return rgb


def demo_frame(mode, frame):
    rgb = background(frame)
    if mode == 'track':
        color = (1, 3, 2)[(frame//80) % 3]
        local = frame % 80
        if local < 75 and frame not in (55, 56):
            x = round(640+360*math.sin(frame*0.037))
            y = round(410+115*math.sin(frame*0.061))
            draw_ball(rgb, x, y, color)
    else:
        # 第一颗球在门内停72帧，期间隐藏2帧模拟短暂完全漏检。
        motion = frame-min(max(frame-60, 0), 72)
        for index, color in enumerate((1, 1, 3, 2, 3, 2)):
            age = motion-(12+index*32)
            if age < 0 or (index == 0 and frame in (79, 80)):
                continue
            x = -48+age*16
            draw_ball(rgb, x, 410, color)
    # 灰白与蓝色干扰物位于ROI内；它们不应成为三色目标。
    cv2.circle(rgb, (1120, 550), 21, (165, 165, 165), -1)
    cv2.circle(rgb, (1190, 550), 21, (40, 70, 230), -1)
    return rgb
