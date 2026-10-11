"""Export a matching SVG and PNG architecture diagram using Pillow."""
from pathlib import Path
from html import escape
import math
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent
W, H = 2200, 1640
im = Image.new('RGB', (W, H), '#f5f7fb')
d = ImageDraw.Draw(im)
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">', '<rect width="100%" height="100%" fill="#f5f7fb"/>']
COLORS = {'rtl': ('#e8f1ff', '#3872b8'), 'py': ('#e7f5ed', '#39845a'), 'pending': ('#fff4d9', '#bc8b27'), 'risk': ('#ffe8e6', '#bc5148')}

def text(x, y, value, size=26, fill='#173451', center=False):
    font = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', size)
    d.text((x, y), value, font=font, fill=fill, anchor='mt' if center else 'lt')
    anchor = 'middle' if center else 'start'
    svg.append(f'<text x="{x}" y="{y+size}" text-anchor="{anchor}" font-family="Microsoft YaHei, Noto Sans CJK SC, sans-serif" font-size="{size}" fill="{fill}">{escape(value)}</text>')

def rect(x, y, w, h, fill, stroke='#d5deea', radius=16):
    d.rounded_rectangle((x, y, x+w, y+h), radius, fill, stroke, 2)
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')

def box(x, y, w, h, lines, kind='rtl'):
    rect(x, y, w, h, *COLORS[kind])
    top = y + (h-len(lines)*36)//2
    for i, line in enumerate(lines):
        text(x+w/2, top+i*36, line, 25, center=True)

def arrow(points, dashed=False, color='#597187'):
    for a, b in zip(points, points[1:]):
        length = math.dist(a, b)
        if dashed:
            for k in range(0, int(length), 16):
                p = tuple(a[j]+(b[j]-a[j])*k/length for j in (0, 1))
                q = tuple(a[j]+(b[j]-a[j])*min(k+9, length)/length for j in (0, 1))
                d.line((p, q), fill=color, width=3)
        else:
            d.line((a, b), fill=color, width=3)
    a, b = points[-2:]
    angle = math.atan2(b[1]-a[1], b[0]-a[0])
    tip = [b, (b[0]-14*math.cos(angle-.45), b[1]-14*math.sin(angle-.45)), (b[0]-14*math.cos(angle+.45), b[1]-14*math.sin(angle+.45))]
    d.polygon(tip, fill=color)
    dash = ' stroke-dasharray="9 7"' if dashed else ''
    svg.append(f'<polyline points="{" ".join(f"{x},{y}" for x,y in points)}" fill="none" stroke="{color}" stroke-width="3"{dash}/>')
    svg.append(f'<polygon points="{" ".join(f"{x},{y}" for x,y in tip)}" fill="{color}"/>')

def panel(y, h, title):
    rect(50, y, 2100, h, '#ffffff')
    text(80, y+18, title, 31)

text(70, 35, '道路视觉项目 · 当前模型与处理架构', 52)
text(73, 108, '2026-09-30  |  实现状态示意；不代表完整时序、CDC 或板级性能已验证', 25, '#637488')
for x, kind, label in [(75, 'rtl', 'RTL 已实现'), (525, 'py', 'Python 诊断'), (975, 'pending', '待接入 / 待验证'), (1535, 'risk', '当前排查重点')]:
    rect(x, 157, 24, 24, *COLORS[kind], radius=5)
    text(x+38, 153, label, 23)

panel(205, 205, '01  FPGA 显示主链')
for x, lines in [(100, ['SC500 摄像头', 'MIPI RAW10']), (510, ['ISP / AWB', '1280×720 RGB']), (920, ['视频打包', 'DDR 帧缓存']), (1330, ['HDMI 叠加', '接收框表快照']), (1740, ['HDMI 输出', '720p 视频＋框'])]:
    box(x, 275, 350, 105, lines)
for x in [450, 860, 1270, 1680]:
    arrow([(x, 327), (x+60, 327)])

panel(435, 225, '02  FPGA 检测旁路：运动定位 → 最多四个目标')
nodes = [['5倍点采样＋灰度', '256×144'], ['背景差分', '阈值20 / 前景冻结'], ['3×3 清理', 'Run 最短长度2'], ['RLE-CCL / 8连通', '最多32标签 / 帧'], ['面积 ≥16', '按面积选 Top4'], ['几何规则分类', '存储 / 跟踪 / 事件']]
for i, lines in enumerate(nodes):
    box(100+i*340, 510, 290, 105, lines)
    if i < 5:
        arrow([(390+i*340, 562), (440+i*340, 562)])
arrow([(685, 380), (685, 422), (65, 422), (65, 495), (245, 495), (245, 510)])
text(720, 395, 'AWB 分支', 21)
arrow([(1945, 510), (1945, 423), (1505, 423), (1505, 380)])
text(1650, 397, '跟踪快照 / CDC', 21)

panel(695, 250, '03  RTL 特征支路：模块已具备，训练分类结果尚未闭环')
box(100, 775, 350, 110, ['双 bank 灰度 RAM', '256×144 / 帧'])
box(620, 775, 350, 110, ['ROI 读取与缩放', '32×32 最近邻'])
box(1140, 775, 350, 110, ['RTL HOG64', 'Sobel / 4×4 cells×4 bins'])
box(1660, 765, 420, 130, ['64维定点线性 SVM', '内积核已独立仿真', '训练权重 / 结果回写待接入'], 'pending')
arrow([(245, 615), (245, 680), (65, 680), (65, 753), (275, 753), (275, 775)])
arrow([(1605, 615), (1605, 678), (1030, 678), (1030, 753), (795, 753), (795, 775)])
text(960, 647, '候选框任务 / 源帧号 / CDC', 21)
arrow([(450, 830), (620, 830)])
arrow([(970, 830), (1140, 830)])
arrow([(1490, 830), (1660, 830)], dashed=True)
text(105, 909, '待验证：帧号配对、bank 所有权、ack 时机与 HDMI 显示延迟', 22, '#89631e')

panel(975, 285, '04  Python 真实数据诊断：HOG324 仍在此阶段')
for x, lines in [(100, ['MP4＋人工标注', '归一化为720p']), (510, ['灰度 / 抽样 / 前景', '清理 / Run / OpenCV CCL']), (920, ['Top4 候选框', '32×32 ROI']), (1330, ['HOG64 / HOG324', '分别训练线性 SVM']), (1740, ['诊断报告', '定位 / 分类 / 量化差异'])]:
    box(x, 1055, 350, 115, lines, 'py')
for x in [450, 860, 1270, 1680]:
    arrow([(x, 1112), (x+60, 1112)], color='#39845a')
arrow([(275, 1170), (275, 1202), (1505, 1202), (1505, 1170)], color='#39845a')
text(490, 1215, '真值框直接裁剪 → 独立评估分类器，区分定位损失与分类损失', 22, '#39845a')

rect(50, 1290, 1030, 225, *COLORS['risk'])
text(80, 1312, '当前优先检查前端', 32, '#732e28')
text(80, 1365, '背景碎片 / 目标框完整性 → Run 信息损失 → 标签容量', 25)
text(80, 1410, '样例有 48–81 个组件，RTL 容量为 32 标签 / 帧。', 25)
text(80, 1455, '容量风险已识别；实际溢出与目标损失待 RTL 回放核对。', 23)
rect(1110, 1290, 1040, 225, *COLORS['pending'])
text(1140, 1312, '读图边界', 32, '#654910')
text(1140, 1365, 'HDMI 类别来自几何规则；HOG324 尚未接入 FPGA。', 25)
text(1140, 1410, 'Python CCL 不受 RTL 标签容量约束，也不是周期仿真。', 25)
text(1140, 1455, '当前二分类强制人 / 车；分数不是概率，拒识尚未冻结。', 23)
text(70, 1560, '优先级：短段 Mask RTL 对拍 → 固定背景分割对照 → 必要时验证受限候选窗口 → 分类适配', 26)
svg.append('</svg>')
im.save(OUT / 'current_architecture.png')
(OUT / 'current_architecture.svg').write_text('\n'.join(svg), encoding='utf-8')
assert im.size == (W, H)
print(OUT / 'current_architecture.png')
print(OUT / 'current_architecture.svg')
