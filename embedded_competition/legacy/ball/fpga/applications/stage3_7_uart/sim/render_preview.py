"""Render actual RTL output captured by the 640x112 testbench, not golden pixels."""
from pathlib import Path
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent
raw=bytes.fromhex((p/'captured.hex').read_text())
size=640*112*3
assert len(raw)==13*size
sheet=Image.new('RGB',(2*656,6*144),(233,236,240));draw=ImageDraw.Draw(sheet)
names=['ORIGINAL / LOCKED','0 GRAY','1 SOBEL','2 EROSION','3 DILATION','4 GAUSSIAN','5 SHARPEN','6 OPEN','7 CLOSE','8 DENOISE','9 FILL HOLES']
for n,name in enumerate(names):
 x=(n%2)*656+8;y=(n//2)*144+4
 draw.text((x,y),name,fill=(20,30,40))
 frame=Image.frombytes('RGB',(640,112),raw[n*size:(n+1)*size])
 sheet.paste(frame,(x,y+20))
sheet.save(p.parent/'reports/rtl_osd_preview.png')
print('Rendered all eleven actual RTL frames')
Image.frombytes('RGB',(640,112),raw[:size]).save(p.parent/'reports/rtl_original_osd.png')
