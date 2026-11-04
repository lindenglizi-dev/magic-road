"""Independent NumPy reference for twelve modes and bilingual OSD.
WB selection uses a distinct injected stream; vendor AWB is tested separately.
"""
from pathlib import Path
import sys,json
import numpy as np
w,h=map(int,sys.argv[1:3]) if len(sys.argv)>1 else (640,112)
p=Path(__file__).parent
y,x=np.indices((h,w));r=(x*17+y*11)%256;g=(x*3+y*29)%256;b=(x*31+y*7)%256
region=(x>w//4)&(x<w//2)&(y>h//2)&(y<h-8)
hole=(abs(x-3*w//8)<2)&(abs(y-3*h//4)<2)
for channel,value in [(r,230),(g,220),(b,210)]:
 channel[region]=value;channel[hole]=0
 channel[(x+7*y)%113==0]=255;channel[(x+11*y)%127==0]=0
raw=np.stack([r,g,b],axis=-1)
gray=(77*r+150*g+29*b)>>8
wb=np.stack([np.minimum(r*3//2,255),g,b*3//4],axis=-1)
def filt(a,kind):
 q=[a[dy:dy+h-2,dx:dx+w-2] for dy in range(3) for dx in range(3)]
 if kind=='sobel':
  gx=-q[0]+q[2]-2*q[3]+2*q[5]-q[6]+q[8]
  gy=q[0]+2*q[1]+q[2]-q[6]-2*q[7]-q[8]
  v=((abs(gx)+abs(gy))>=128)*255
 elif kind=='sharp':v=np.clip(5*q[4]-q[1]-q[3]-q[5]-q[7],0,255)
 elif kind=='median':v=np.median(np.stack(q),axis=0).astype(int)
 elif kind=='erode':v=np.minimum.reduce(q)
 elif kind=='dilate':v=np.maximum.reduce(q)
 else:raise ValueError(kind)
 out=np.zeros_like(a);out[1:-1,1:-1]=v;return out
def rgb(a):return np.repeat(a[:,:,None],3,axis=2)
binary=(gray>=128)*255
results=[raw,wb,rgb(binary),rgb(filt(gray,'median')),rgb(filt(gray,'sobel')),rgb(filt(gray,'sharp')),
 np.floor(255*(raw/255)**.7+.5),np.clip((5*raw-128)//4,0,255),np.clip(raw+32,0,255),
 np.clip((3*raw-gray[:,:,None])//2,0,255),rgb(filt(filt(binary,'erode'),'dilate')),
 rgb(filt(filt(binary,'dilate'),'erode'))]
assets=json.loads((p/'osd_font.json').read_text(encoding='utf-8'))
results=[a.astype(np.uint8) for a in results]
if w>=608 and h>=96:
 for mode,canvas in enumerate(results):
  canvas[16:96,16:144]=np.asarray(assets['palette'],dtype=np.uint8)[np.asarray(assets['logo'])]
  canvas[16:96,w-432:w-16]=[16,24,32]
  for line,txt in enumerate(assets['labels'][mode]):
   assert len(txt)<=12,txt
   for i,ch in enumerate(txt):
    for row,bits in enumerate(assets['glyphs'][ch]):
     for col,bit in enumerate(bits):
      if bit=='1':canvas[24+line*32+row,w-424+i*32+col]=[255,224,102]
for filename,canvas in [('input.hex',raw),('input_wb.hex',wb)]:
 with (p/filename).open('w') as f:
  data=canvas.astype(np.uint8).tobytes()
  for i in range(0,len(data),12):f.write(data[i:i+12].hex()+'\n')
with (p/'expected.hex').open('w') as f:
 for result in results:
  data=result.tobytes()
  for i in range(0,len(data),16):f.write(data[i:i+16].hex()+'\n')
print(f'Independent golden vectors: {w}x{h}, original plus 11 numbered algorithms with OSD')
