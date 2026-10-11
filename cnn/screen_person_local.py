"""Bounded local person-source screening; no GT publication or model execution."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from html import escape
import io
from pathlib import Path
import sys
import zipfile

import cv2
from PIL import Image, ImageDraw

# Existing EPFL helper retains a top-level dataset import.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from .prepare_ac_pilot import DATA as EPFL, FAMILY, epfl_boxes
from .prepare_ground48 import ROOT, read_json, sha256_file, write_json

OUT = ROOT / 'cnn/reports/person_local_screen_20261010_v2'
CATALOG = ROOT / 'evaluation/public_data/virat_ground_v2/catalog.json'
EPFL_PAIRS = ((0, 147), (0, 218), (4, 56), (4, 177), (5, 147), (5, 190))
TRAIN_CLIPS = ('VIRAT_S_000201_02_000590_000623',
               'VIRAT_S_000206_07_001501_001600')
PATCH = Path('C:/Users/lenovo/Downloads/review_patch_5d9172720dfa_2026-10-10T05-58-08-506Z.json')


def spaced_frames(counts, limit, gap):
    chosen = []
    for frame in sorted(counts, key=lambda f: (-counts[f]['person'], f)):
        if counts[frame]['person'] and all(abs(frame - old) >= gap for old in chosen):
            chosen.append(frame)
        if len(chosen) == limit:
            break
    return sorted(chosen)


def virat_rows(clip):
    """Read only the two explicitly allowed training annotation files."""
    assert clip['clip_id'] in TRAIN_CLIPS and clip['split'] == 'train'
    path = Path(clip['annotation_path'])
    assert sha256_file(path) == clip['annotation_sha256']
    rows = defaultdict(list)
    for line_no, line in enumerate(path.read_text(encoding='utf-8-sig').splitlines(), 1):
        if not line.strip():
            continue
        values = list(map(int, line.split()))
        if len(values) != 8:
            raise ValueError(f'{path}:{line_no}: unexpected VIRAT layout')
        track, duration, frame, x, y, width, height, kind = values
        if frame >= clip['frame_count']:
            continue  # Official terminal rows already excluded by the canonical importer.
        if not (0 <= frame and 0 <= x < x + width <= clip['width']
                and 0 <= y < y + height <= clip['height']):
            raise ValueError(f'{path}:{line_no}: out-of-bounds source box')
        label = 'person' if kind == 1 else 'vehicle' if kind in (2, 3) else 'ignore'
        rows[frame].append(dict(label=label, bbox=[x, y, x + width, y + height],
                                track_id=track, original_type=kind, source_line=line_no))
    return rows


def save_preview(image, row):
    directory = OUT / 'images' / row['image_id']
    directory.mkdir(parents=True)
    image.save(directory / 'raw.png')
    overlay = image.copy()
    draw = ImageDraw.Draw(overlay)
    for number, box in enumerate(row['source_boxes'], 1):
        color = {'person': '#00dc60', 'vehicle': '#008cff', 'ignore': '#888888'}[box['label']]
        draw.rectangle(box['bbox'], outline=color, width=2)
        draw.text(box['bbox'][:2], f'{number} {box["label"]}', fill=color,
                  stroke_width=1, stroke_fill='black')
    overlay.save(directory / 'source.png')
    row.update(width=image.width, height=image.height, training_eligible=False,
               human_complete=False, source_labels_are_complete_GT=False,
               raw_path=str(directory / 'raw.png'),
               raw_sha256=sha256_file(directory / 'raw.png'),
               source_overlay_sha256=sha256_file(directory / 'source.png'))
    row['source_counts'] = dict(Counter(b['label'] for b in row['source_boxes']))
    scale = min(1280 / image.width, 720 / image.height) * .4
    heights = [(b['bbox'][3] - b['bbox'][1]) * scale
               for b in row['source_boxes'] if b['label'] == 'person']
    row['source_person_heights_at_512x288'] = heights


def build():
    if OUT.exists() and any(OUT.iterdir()):
        raise FileExistsError('Preserve prior screening; use --check instead')
    protected_paths = [PATCH, CATALOG, ROOT / 'cnn/model.py', ROOT / 'cnn/annotation_policy_v1.md',
                       ROOT / 'cnn/reports/ac_scope_fixed_20261010_v1/scope_decision.json',
                       ROOT / 'cnn/reports/ac_ai_drawn24_20261010_v1/review_manifest_ai_draft.json',
                       ROOT / 'cnn/reports/ac_patch_check_20261010_v3/patch_validation.json']
    protected = {str(p): sha256_file(p) for p in protected_paths}
    OUT.mkdir(exist_ok=True)
    frames, epfl_inventory = [], []
    with zipfile.ZipFile(EPFL / 'multiclass_ground_truth.zip') as labels, \
            zipfile.ZipFile(EPFL / 'multiclass_ground_truth_images.zip') as images:
        for camera in range(6):
            counts = Counter()
            errors = []
            for ordinal in range(1, 243):
                try:
                    boxes, _ = epfl_boxes(labels, camera, ordinal)
                except ValueError as exc:
                    errors.append(str(exc))
                    continue
                number = sum(b['source_class'] == 'person' for b in boxes)
                counts['source_person_boxes'] += number
                counts['person_bearing_frames'] += number > 0
                counts['max_person_per_frame'] = max(counts['max_person_per_frame'], number)
            epfl_inventory.append(dict(camera_id=f'EPFL:c{camera}', **counts,
                                       invalid_source_frames=errors,
                                       count_scope='valid-source-box frames only; errors excluded, not repaired'))
        for camera, ordinal in EPFL_PAIRS:
            boxes, missing = epfl_boxes(labels, camera, ordinal)
            member = f'c{camera}/{ordinal:08d}.jpg'
            row = dict(image_id=f'epfl_c{camera}_o{ordinal:03d}', source='EPFL',
                       reserved_split='train', camera_id=f'EPFL:c{camera}', family_id=FAMILY,
                       ordinal=ordinal, original_frame_index=None, source_member=member,
                       source_boxes=[dict(label='person' if b['source_class'] == 'person' else 'vehicle',
                                          bbox=b['xyxy_raw'], source_record=b) for b in boxes],
                       gaps=['person/car/bus source only; bicycle/static-vehicle coverage not certified',
                             'ordinal is not native frame/time; all synchronized views one family',
                             'native 360x288; not new 720p camera evidence'], missing_class_files=missing)
            save_preview(Image.open(io.BytesIO(images.read(member))).convert('RGB'), row)
            frames.append(row)
    catalog = read_json(CATALOG)
    virat_inventory = []
    cv2.setNumThreads(2)
    for clip_id in TRAIN_CLIPS:
        clip = next(c for c in catalog['clips'] if c['clip_id'] == clip_id)
        rows = virat_rows(clip)
        counts = {f: Counter(b['label'] for b in boxes) for f, boxes in rows.items()}
        tracks = {b['track_id'] for boxes in rows.values() for b in boxes if b['label'] == 'person'}
        chosen = spaced_frames(counts, 2 if clip_id == TRAIN_CLIPS[0] else 4, 450)
        path = Path(clip['video_path'])
        assert sha256_file(path) == clip['video_sha256']
        virat_inventory.append(dict(clip_id=clip_id, existing_split=clip['split'],
                                    distinct_source_person_tracks=len(tracks),
                                    max_source_person_per_frame=max(c['person'] for c in counts.values()),
                                    chosen_frames=chosen, video_sha256=clip['video_sha256'],
                                    annotation_sha256=clip['annotation_sha256'],
                                    camera_isolation_verified=False,
                                    camera_conflict_with_existing_development=True))
        cap = cv2.VideoCapture(str(path))
        try:
            for frame in range(max(chosen) + 1):
                ok, pixels = cap.read()
                if not ok:
                    raise ValueError(f'{clip_id}: sequential decode failed at {frame}')
                if frame not in chosen:
                    continue
                row = dict(image_id=f'{clip_id}_f{frame:07d}', source='VIRAT',
                           reserved_split='legacy_train_camera_conflict_quarantined',
                           camera_id='VIRAT-0002xx-visual-match', source_scene_id=clip['scene_id'],
                           family_id='VIRAT-0002xx-shared-camera-provisional',
                           source_frame=frame, source_timestamp_seconds=frame / clip['fps'],
                           source_video=str(path), source_boxes=rows[frame],
                           gaps=['same physical camera as existing 0002xx development; NOT eligible training',
                                 'source track annotations are not exhaustive static-vehicle GT',
                                 'type0 preserved as unknown-source ignore, not certified semantic ignore'])
                save_preview(Image.fromarray(cv2.cvtColor(pixels, cv2.COLOR_BGR2RGB)), row)
                frames.append(row)
        finally:
            cap.release()
    assert len(frames) == 12
    summary = Counter()
    for row in frames:
        summary.update(row['source_counts'])
    report = dict(schema='local_person_screen_v1', purpose='source screening, not a new review assignment',
                  requires_person_vehicle_same_frame=False, training_started=False, GPU_used=False,
                  inference_run=False, network_weights_changed=False, dataset_frozen=False,
                  additional_manual_assignments=0, manual_workload_cap_changed=False,
                  source_boxes_are_GT=False, selected_source_box_counts=dict(summary),
                  previous_incomplete_screen_preserved=str(OUT.with_name('person_local_screen_20261010_v1')),
                  initial_failure='strict EPFL parser rejected zero-area person box in cam5 ordinal218; '
                                  'invalid source frame retained as a finding, selected valid ordinal190 instead',
                  person_bearing_previews=sum(r['source_counts'].get('person', 0) > 0 for r in frames),
                  independent_person_count=None, epfl_inventory=epfl_inventory,
                  virat_inventory=virat_inventory, frames=frames, protected_files=protected,
                  source_archive_hashes={p.name: sha256_file(p) for p in
                                         (EPFL / 'multiclass_ground_truth.zip', EPFL / 'multiclass_ground_truth_images.zip')},
                  script_sha256=sha256_file(Path(__file__)),
                  boundary='Repeated people across times/views; source counts are not unique people or complete GT. '
                           'PETS/VIRAT dev, D junctions and blind/reserve excluded from new candidate selection.')
    write_json(OUT / 'screening.json', report)
    for start in (0, 6):
        sheet = Image.new('RGB', (1440, 690), '#eeeeee')
        draw = ImageDraw.Draw(sheet)
        for number, row in enumerate(frames[start:start + 6], start + 1):
            image = Image.open(row['raw_path']).convert('RGB')
            image.thumbnail((480, 290))
            x, y = ((number - 1) % 3) * 480, ((number - 1 - start) // 3) * 345
            sheet.paste(image, (x, y + 44))
            draw.text((x + 8, y + 5), f'{number:02d} {row["source"]} {row["image_id"][-20:]}', fill='black')
            draw.text((x + 8, y + 23), f'SOURCE P={row["source_counts"].get("person", 0)} '
                      f'V={row["source_counts"].get("vehicle", 0)}; NOT GT', fill='black')
        sheet.save(OUT / f'raw_{start + 1:02d}_{start + 6:02d}.jpg', quality=93)
    cards = []
    for number, row in enumerate(frames, 1):
        base = 'images/' + row['image_id']
        cards.append(f'<section><h2>{number:02d} {escape(row["image_id"])}</h2>'
                     f'<p>来源框计数：{escape(str(row["source_counts"]))}；不是完整GT，不是模型结果。</p>'
                     f'<a href="{base}/raw.png"><img src="{base}/raw.png" alt="无框原图"></a>'
                     f'<details><summary>查看来源参考框（非教师预测）</summary>'
                     f'<img src="{base}/source.png" alt="来源参考框"></details></section>')
    (OUT / 'index.html').write_text('<!doctype html><html lang="zh-CN"><meta charset="utf-8">'
                                  '<title>行人训练来源筛选</title><style>body{max-width:1200px;margin:24px auto;'
                                  'font:18px sans-serif;background:#f5f5f5}section{background:white;padding:16px;'
                                  'margin:16px 0}img{max-width:100%;height:auto}summary{cursor:pointer}</style>'
                                  '<h1>行人来源筛选：12张预览，不是新增审核任务</h1>'
                                  '<p>允许行人较多、没有车的图片。本页没有签署或导出按钮；不要求你补标。'
                                  '绿色person、蓝色vehicle、灰色未知来源ignore均只是来源参考，未自动变成GT。</p>'
                                  '<p>EPFL所有同步视角属于一个原片家族；VIRAT旧train片段与现有开发图机位重合，隔离待决，不能直接训练。'
                                  '相邻时刻或多视角可出现同一个人，框数不能当独立人数。未训练、未推理。</p>'
                                  + ''.join(cards) + '</html>', encoding='utf-8')
    check()
    print('SCREENED', dict(summary), '12 previews; no training/inference/manual assignment')


def check():
    report = read_json(OUT / 'screening.json')
    assert len(report['frames']) == 12 and not report['training_started'] and not report['inference_run']
    assert report['additional_manual_assignments'] == 0 and not report['dataset_frozen']
    assert len({r['image_id'] for r in report['frames']}) == 12
    assert report['script_sha256'] == sha256_file(Path(__file__))
    for path, digest in report['protected_files'].items():
        assert sha256_file(Path(path)) == digest, path
    for row in report['frames']:
        assert not row['training_eligible'] and not row['source_labels_are_complete_GT']
        assert sha256_file(Path(row['raw_path'])) == row['raw_sha256']
        assert sha256_file(Path(row['raw_path']).with_name('source.png')) == row['source_overlay_sha256']
        assert Counter(b['label'] for b in row['source_boxes']) == row['source_counts']
    assert spaced_frames({0: Counter(person=2), 1: Counter(person=9), 500: Counter(person=3)}, 2, 450) == [1, 500]
    assert spaced_frames({0: Counter(vehicle=5)}, 2, 450) == []
    print('PASS source images/counts, spacing, preserved old files, no-GT/no-training boundaries')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    check() if args.check else build()
