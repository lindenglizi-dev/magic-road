"""Bounded source screening only; reference-frame identity and GT remain unverified."""
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
import hashlib
import html
import io
import json
from pathlib import Path
import shlex
import sys
from urllib.request import urlopen

from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parent / 'reports/sdd_source_screen_20261010_v1'
BASE = 'https://raw.githubusercontent.com/flclain/StanfordDroneDataset/master/'
SCENES = ('bookstore', 'coupa', 'deathCircle', 'gates', 'hyang', 'little', 'nexus', 'quad')


def parse_row(line):
    fields = shlex.split(line)
    if len(fields) != 10:
        raise ValueError('unexpected annotation columns')
    values = list(map(int, fields[:9]))
    if values[3] <= values[1] or values[4] <= values[2]:
        raise ValueError('nonpositive box')
    if any(v not in (0, 1) for v in values[6:9]):
        raise ValueError('unexpected flags')
    return values, fields[9]


def download(item):
    scene, name = item
    url = BASE + scene + '/video0/' + name
    record = dict(scene=scene, video='video0', name=name, url=url)
    try:
        with urlopen(url, timeout=20) as response:
            blob = response.read(12_000_001)
        if len(blob) > 12_000_000:
            raise ValueError('bounded download size exceeded; no partial label adopted')
        target = OUT / (scene + '_' + name)
        if name.endswith('.jpg'):
            with Image.open(io.BytesIO(blob)) as image:
                image.load()
                record['size'] = image.size
        else:
            rows = [parse_row(line) for line in blob.decode('utf-8').splitlines() if line.strip()]
            record['rows'] = len(rows)
            record['classes'] = dict(Counter(label for _, label in rows))
            record['frame0_classes'] = dict(Counter(label for v, label in rows if v[5] == 0 and v[6] == 0))
        target.write_bytes(blob)
        record.update(status='downloaded', bytes=len(blob), sha256=hashlib.sha256(blob).hexdigest(), file=target.name)
    except Exception as error:
        record.update(status='failed_not_adopted', error=str(error))
    return record


def check():
    row, label = parse_row('1 0 1 10 20 0 0 1 0 "Pedestrian"')
    assert label == 'Pedestrian' and row[5] == 0
    for bad in ('1 0 1 0 20 0 0 1 0 "Pedestrian"', '1 0 1 10 20 0 2 1 0 "Pedestrian"'):
        try:
            parse_row(bad)
        except ValueError:
            continue
        raise AssertionError('bad row accepted')
    receipt = json.loads((OUT / 'receipt.json').read_text(encoding='utf-8'))
    assert not receipt['training_eligible'] and not receipt['reference_frame_pairing_verified']
    for record in receipt['files']:
        if record['status'] == 'downloaded':
            assert hashlib.sha256((OUT / record['file']).read_bytes()).hexdigest() == record['sha256']
    print('PASS parser negatives, source file hashes, unsigned screening status')


def build():
    if OUT.exists():
        raise FileExistsError('preserve prior screening')
    OUT.mkdir(parents=True)
    jobs = [(scene, name) for scene in SCENES for name in ('reference.jpg', 'annotations.txt')]
    with ThreadPoolExecutor(max_workers=4) as pool:
        records = list(pool.map(download, jobs))
    receipt = dict(source='SDD annotation mirror, not author-hosted bytes', official='https://cvgl.stanford.edu/projects/uav_data/',
        source_reference_images_only=True, reference_frame_pairing_verified=False,
        complete_GT=False, training_eligible=False, human_assignment=0, files=records)
    (OUT / 'receipt.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding='utf-8')
    sheet = Image.new('RGB', (1200, 4 * 360), 'white')
    draw = ImageDraw.Draw(sheet)
    cards = []
    for i, scene in enumerate(SCENES):
        record = next(r for r in records if r['scene'] == scene and r['name'] == 'reference.jpg')
        if record['status'] != 'downloaded':
            continue
        with Image.open(OUT / record['file']) as image:
            preview = image.convert('RGB')
            preview.thumbnail((590, 330))
            sheet.paste(preview, ((i % 2) * 600, (i // 2) * 360 + 25))
        draw.text(((i % 2) * 600 + 5, (i // 2) * 360 + 5), scene + '/video0 reference (frame unverified)', fill='black')
        cards.append(f'<h2>{html.escape(scene)}/video0</h2><a href="{record["file"]}"><img style="max-width:100%" src="{record["file"]}"></a>')
    sheet.save(OUT / 'contact.jpg', quality=94)
    (OUT / 'index.html').write_text('<!doctype html><meta charset="utf-8"><title>SDD来源筛查</title><body style="max-width:1100px;margin:auto">'
        '<h1>校园来源参考图：不是已采用训练数据</h1><p>8个场景，每场景仅video0参考图。镜像标签保留原样；参考图对应帧号尚未核实，不叠加假定GT、不自动签署。无人工作业。</p>'
        '<p><a href="receipt.json">下载与标签检查记录</a></p>' + ''.join(cards), encoding='utf-8')
    print(json.dumps([dict(scene=r['scene'], name=r['name'], status=r['status'], rows=r.get('rows'), error=r.get('error')) for r in records]))
    check()


if __name__ == '__main__':
    check() if len(sys.argv) > 1 and sys.argv[1] == 'check' else build()
