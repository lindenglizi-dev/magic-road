"""Eight original MOT17 training frames; source screening only, never GT publication."""
from __future__ import annotations

import argparse
from collections import Counter
import configparser
from html import escape
import math
from pathlib import Path
import sys
import zipfile

from PIL import Image, ImageDraw

# Reuse the bounded ZIP reader; an older imported helper uses a top-level dataset import.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from . import prepare_ac_next8 as remotezip
from .prepare_ground48 import ROOT, read_json, sha256_file, write_json

DATA = ROOT / 'cnn/data/mot17_person_pilot_20261010'
OUT = ROOT / 'cnn/reports/mot17_person_source_20261010_v1'
URL = 'https://motchallenge.net/data/MOT17.zip'
SIZE = 5860214001
PREFIX = 'MOT17/train/MOT17-02-SDP/'
FRAMES = (1, 76, 151, 226, 301, 376, 451, 526)
CLASSES = ('unused', 'pedestrian', 'person_on_vehicle', 'car', 'bicycle',
           'motorbike', 'non_mot_vehicle', 'static_person', 'distractor',
           'occluder', 'occluder_ground', 'occluder_full', 'reflection', 'crowd')


def parse_gt(text):
    rows, identities = [], set()
    for line_number, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        v = list(map(float, line.split(',')))
        if (len(v) != 9 or not all(math.isfinite(x) for x in v)
                or any(v[i] != int(v[i]) for i in (0, 1, 6, 7))
                or not (1 <= v[0] <= 600 and v[1] > 0 and v[4] > 0 and v[5] > 0)
                or v[6] not in (0, 1) or not 1 <= v[7] <= 13 or not 0 <= v[8] <= 1):
            raise ValueError(f'Unexpected official GT row {line_number}')
        key = (int(v[0]), int(v[1]))
        if key in identities:
            raise ValueError(f'Duplicate frame/track: {key}')
        identities.add(key)
        x, y, w, h = v[2:6]
        rows.append(dict(frame=key[0], track_id=key[1], source_line=line_number,
                         source_xywh=v[2:6], source_flag=int(v[6]),
                         source_class=int(v[7]), visibility=v[8],
                         # Source coordinates are 1-based; no width/height subtraction.
                         xyxy_zero_based=[x-1, y-1, x-1+w, y-1+h]))
    return rows


def fetch():
    if DATA.exists():
        raise FileExistsError('Preserve prior/partial download; no automatic retry')
    DATA.mkdir(parents=True)
    remotezip.URL, remotezip.SIZE = URL, SIZE  # Process-local, not old source edits.
    remote = remotezip.SourceRanges()
    receipt = dict(url=URL, archive_bytes=SIZE, complete=False, members=[],
                   archive_fully_downloaded=False, archive_sha256=None,
                   accessed_pixels_and_labels='MOT17/train/MOT17-02-SDP only',
                   central_directory_contains_train_and_test_filenames=True,
                   training_started=False, model_inference_started=False)
    try:
        with zipfile.ZipFile(remote) as archive:
            for suffix in ['gt/gt.txt', 'seqinfo.ini', *[f'img1/{f:06d}.jpg' for f in FRAMES]]:
                name = PREFIX + suffix
                info = archive.getinfo(name)
                if info.file_size > 2*1024**2:
                    raise ValueError('Unexpectedly large member')
                raw = archive.read(info)  # ZIP CRC verified by stdlib.
                destination = DATA / Path(suffix).name
                with destination.open('xb') as stream:
                    stream.write(raw)
                receipt['members'].append(dict(member=name, path=str(destination),
                    bytes=len(raw), crc32=info.CRC, sha256=sha256_file(destination)))
                print('Fetched', suffix, len(raw), flush=True)
        receipt['complete'] = True
    except Exception as exc:
        receipt['error'] = f'{type(exc).__name__}: {exc}'
        raise
    finally:
        receipt.update(etag=remote.etag, downloaded_payload_bytes=remote.total,
                       ranges=remote.receipts, downloader_sha256=sha256_file(Path(__file__)))
        write_json(DATA / 'receipt.json', receipt)


def verify_download():
    receipt = read_json(DATA / 'receipt.json')
    assert receipt['complete'] and len(receipt['members']) == 10
    assert receipt['downloaded_payload_bytes'] <= 8*1024**2 and len(receipt['ranges']) <= 40
    for member in receipt['members']:
        assert member['member'].startswith(PREFIX)
        assert sha256_file(Path(member['path'])) == member['sha256']
    config = configparser.ConfigParser()
    config.read(DATA / 'seqinfo.ini', encoding='utf-8-sig')
    seq = config['Sequence']
    assert tuple(int(seq[k]) for k in ('imWidth', 'imHeight', 'seqLength', 'frameRate')) == (1920, 1080, 600, 30)
    return receipt, parse_gt((DATA / 'gt.txt').read_text(encoding='utf-8-sig'))


def build():
    receipt, rows = verify_download()
    if OUT.exists():
        raise FileExistsError('Preserve existing report')
    OUT.mkdir(parents=True)
    cards, samples = [], []
    sheet = Image.new('RGB', (960, 4*294), '#111111')
    for i, frame in enumerate(FRAMES):
        raw_path = DATA / f'{frame:06d}.jpg'
        with Image.open(raw_path) as source:
            image = source.convert('RGB')
        assert image.size == (1920, 1080)
        selected = [r for r in rows if r['frame'] == frame]
        counts = dict(Counter(CLASSES[r['source_class']] for r in selected))
        overlay = image.copy()
        draw = ImageDraw.Draw(overlay)
        for r in selected:
            kind = r['source_class']
            color = '#00df6d' if kind == 1 else '#00dfff' if kind == 2 else '#208cff' if kind in (3, 4, 5) else '#ffc14d' if kind == 7 else '#aaaaaa'
            x1, y1, x2, y2 = r['xyxy_zero_based']
            box = [max(0, x1), max(0, y1), min(1920, x2), min(1080, y2)]
            if box[2] > box[0] and box[3] > box[1]:
                draw.rectangle(box, outline=color, width=2)
                draw.text((box[0], box[1]), f'{r["track_id"]}:c{kind}', fill=color,
                          stroke_width=1, stroke_fill='black')
        overlay_path = OUT / f'{frame:06d}_source.jpg'
        overlay.save(overlay_path, quality=92)
        heights = [r['source_xywh'][3]*288/1080 for r in selected if r['source_class'] == 1]
        samples.append(dict(frame=frame, time_seconds=(frame-1)/30,
            raw_path=str(raw_path), raw_sha256=sha256_file(raw_path), source_counts=counts,
            source_boxes=selected, source_person_heights_at_512x288=heights,
            source_overlay_path=str(overlay_path), source_overlay_sha256=sha256_file(overlay_path),
            training_eligible=False, human_complete=False, project_complete_GT=False))
        thumb = image.resize((480, 270))
        left, top = (i % 2)*480, (i // 2)*294
        sheet.paste(thumb, (left, top+24))
        ImageDraw.Draw(sheet).text((left+5, top+5), f'frame {frame:06d} | pedestrian {counts.get("pedestrian", 0)} | raw', fill='white')
        cards.append(f'<article><h2>Frame {frame:06d} / {(frame-1)/30:.1f}s</h2>'
            f'<p>{escape(str(counts))}</p><a href="{raw_path.as_uri()}"><img src="{raw_path.as_uri()}" alt="Unmarked original frame {frame}"></a>'
            f'<details><summary>展开官方来源框（不是教师预测，不是已审核训练GT）</summary><img src="{overlay_path.name}" alt="Official source boxes"></details></article>')
    sheet.save(OUT / 'raw_contact.jpg', quality=94)
    summary = dict(dataset='MOT17-02-SDP', purpose='person-source screening only',
        official_page='https://motchallenge.net/data/MOT17/', receipt=receipt,
        family='MOT17-02 / MOT16-02 / MOT15 Venice-2; detector suffixes duplicate frames',
        split='unassigned; entire camera/original family must stay in one future split',
        same_camera_reserve='MOT17-01 / MOT16-01 / MOT15 Venice-1; no test pixels read',
        selection='8 fixed timeline positions, no teacher/student score selection',
        full_sequence_source_counts=dict(Counter(CLASSES[r['source_class']] for r in rows)),
        samples=samples, training_started=False, model_inference_started=False,
        human_review_cap=32, new_human_review_images_assigned=0,
        limitations=['Source vehicles not exhaustively annotated; cannot use missing vehicles as negatives.',
                    'Source flags/classes and amodal boxes are not automatically project labels.',
                    'Repeated tracks over 20 seconds are not independent people/cameras.',
                    'Official cached home states CC BY-NC-SA 3.0; current home HTTP410, competition/redistribution not certified.'])
    write_json(OUT / 'screening.json', summary)
    with (OUT / 'index.html').open('x', encoding='utf-8') as stream:
        stream.write('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>MOT17行人来源核查8图</title>'
            '<style>body{max-width:1200px;margin:24px auto;background:#17191d;color:#eee;font:16px sans-serif}img{width:100%;height:auto}article{margin:28px 0}summary{cursor:pointer}p{line-height:1.6}a{color:#8cd5ff}</style>'
            '<h1>MOT17-02 行人来源核查：8张原图</h1><p>仅来源筛选，不需要你现在逐图签署。未进入训练；人工审核总上限32张不变。默认原图，来源框折叠。</p>'
            '<p>绿=c1行人；青=c2骑行者；蓝=c3–5车体；橙=c7静态人；灰=其他来源类别。车辆可能缺标；灰色并非项目已确认ignore。标签为track:c类别。</p>'
            '<p>原始全身框可越界；仅显示时裁边。02是白天固定中等视角广场，非低密度道路主集；09论文列室内，本轮未取09图。</p>'
            + ''.join(cards) + '</html>')
    print('Built screening only:', OUT, flush=True)


def check():
    row = parse_gt('1,2,1,1,4,5,1,1,0.5')[0]
    assert row['xyxy_zero_based'] == [0, 0, 4, 5]
    assert parse_gt('1,2,-3,1,4,5,0,12,0')[0]['source_flag'] == 0
    for invalid in ('0,2,1,1,4,5,1,1,0.5', '1,2,1,1,0,5,1,1,0.5',
                    '1,2,1,1,4,5,1,14,0.5', '1,2,1,1,4,5,1,1,nan'):
        try:
            parse_gt(invalid)
        except ValueError:
            pass
        else:
            raise AssertionError('Invalid GT accepted')
    if (OUT / 'screening.json').exists():
        verify_download()
        report = read_json(OUT / 'screening.json')
        assert [r['frame'] for r in report['samples']] == list(FRAMES)
        for sample in report['samples']:
            assert not sample['training_eligible'] and not sample['project_complete_GT']
            assert sha256_file(Path(sample['source_overlay_path'])) == sample['source_overlay_sha256']
    print('Parser/coordinates and available artifacts: PASS', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('fetch', 'build', 'check'))
    action = parser.parse_args().action
    {'fetch': fetch, 'build': build, 'check': check}[action]()
