from pathlib import Path
import json
import numpy as np

p=Path(__file__).resolve().parent
a=json.loads((p/'osd_font.json').read_text(encoding='utf-8'))
with (p/'osd_expected.hex').open('w') as f:
    for mode,result_id in [(1,0)]*3+[(1,1)]+[(0,0)]*3+[(0,1)]:
        canvas=np.empty((720,1280,3),dtype=np.uint8)
        canvas[:]=[255,0,0]
        # Existing detector OSD, unchanged: voted result, mode, normal preset, ROI.
        canvas[16:48,16:80]=[255,48,48] if result_id else [96,96,96]
        canvas[16:48,88:112]=[255,128,0] if mode else [0,255,255]
        canvas[16:48,120:144]=[64,64,64]
        canvas[180:182,480:800]=255;canvas[538:540,480:800]=255
        canvas[180:540,480:482]=255;canvas[180:540,798:800]=255
        canvas[64:144,16:144]=np.asarray(a['palette'],dtype=np.uint8)[np.asarray(a['logo'])]
        canvas[16:128,848:1264]=[16,24,32]
        for line,txt in enumerate(a['labels'][mode]+[a['results'][mode][result_id]]):
            for i,ch in enumerate(txt):
                for row,bits in enumerate(a['glyphs'][ch]):
                    for col,bit in enumerate(bits):
                        if bit=='1':canvas[24+line*32+row,856+i*32+col]=[255,224,102]
        data=canvas.tobytes()
        for i in range(0,len(data),16):f.write(data[i:i+16].hex()+'\n')
print('Generated 8 full 1280x720 frame references: unknown/red lamp, switch, unknown/red color')
