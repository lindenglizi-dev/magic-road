from pathlib import Path
from PIL import Image
p=Path(__file__).resolve().parent
for source,target in [('osd_actual_top.hex','osd_actual_preview.png'),
                      ('osd_actual_color_top.hex','osd_color_preview.png')]:
    data=bytes.fromhex((p/source).read_text())
    assert len(data)==1280*160*3
    Image.frombytes('RGB',(1280,160),data).save(p.parent/'reports'/target)
print('Rendered traffic/red lamp and color/red previews from actual RTL output')
