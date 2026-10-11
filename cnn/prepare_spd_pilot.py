"""Inspect official SPD zip and produce at most eight unsigned review examples."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import html
import json
import math
from pathlib import Path, PurePosixPath
import stat
import zipfile

import cv2
import numpy as np

from .dataset import _letterbox_720
from .integer import resize_area
from .prepare_ground48 import ROOT, OUTPUT, read_json, sha256_file, write_json

BASE = 'V2X-Seq-SPD-Example/infrastructure-side/'
DIRECT = {'Pedestrian': 'person', 'Car': 'vehicle', 'Bus': 'vehicle', 'Truck': 'vehicle'}
RIDERS = {'Cyclist', 'Motorcyclist', 'Tricyclist'}


def safe_member(name):
    path = PurePosixPath(name)
    if not name or path.is_absolute() or '..' in path.parts or '\\' in name or ':' in name:
        raise ValueError(f'unsafe archive member: {name}')
    return name


def paired_member(relative, kind):
    safe_member(relative)
    if not relative.startswith(kind + '/'):
        raise ValueError(f'incorrect camera/image pairing: {relative}')
    return BASE + relative


def inspect_objects(objects, width, height):
    result, issues = [], []
    for index, item in enumerate(objects):
        source_id = f'o{index + 1}'
        raw = item.get('2d_box', {})
        box = [raw.get(key) for key in ('xmin', 'ymin', 'xmax', 'ymax')]
        valid = (all(isinstance(v, (int, float)) and not isinstance(v, bool)
                     and math.isfinite(v) for v in box)
                 and box[0] < box[2] and box[1] < box[3])
        bounds = valid and 0 <= box[0] < box[2] <= width and 0 <= box[1] < box[3] <= height
        if not valid:
            issues.append(f'{source_id}: invalid/nonfinite/zero-area 2d_box')
        elif not bounds:
            issues.append(f'{source_id}: out-of-image coordinates; original retained, not silently clipped')
        label = DIRECT.get(item.get('type'))
        if item.get('type') == 'Van':
            issues.append(f'{source_id}: Van proposed vehicle mapping requires human approval')
        elif item.get('type') in RIDERS:
            issues.append(f'{source_id}: rider composite box needs independent person/body annotation')
        elif label is None:
            issues.append(f'{source_id}: unresolved class {item.get("type")}')
        result.append(dict(source_id=source_id, source_type=item.get('type'),
            token=item.get('token'), track_id=item.get('track_id'), bbox_xyxy=box,
            geometry_valid=bool(valid), in_bounds=bool(bounds),
            proposed_class=label, requires_review=not bounds or label is None,
            truncated_state=item.get('truncated_state'), occluded_state=item.get('occluded_state')))
    return result, issues


def select_pilot(records, maximum=8):
    eligible = [row for row in records if row['estimated_split_count'] < 20
                and all(obj['geometry_valid'] for obj in row['objects'])]
    # Same-source frames stay one group; spread by sequence position, not model score.
    if len(eligible) <= maximum:
        return eligible
    return [eligible[round(i * (len(eligible) - 1) / (maximum - 1))] for i in range(maximum)]


def overlay(rgb, objects, mapped=False):
    canvas = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    for item in objects:
        if not item['geometry_valid']:
            continue
        if mapped and item['proposed_class'] is not None:
            label, color = item['proposed_class'], (40, 210, 40)
        else:
            label = item['source_type'] + (' REVIEW' if mapped else '')
            color = (0, 150, 255) if mapped else (255, 200, 0)
        box = [round(v) for v in item['bbox_xyxy']]
        cv2.rectangle(canvas, tuple(box[:2]), tuple(box[2:]), color, 2)
        cv2.putText(canvas, f'{item["source_id"]} {label}',
                    (max(0, box[0]), max(18, min(canvas.shape[0]-5, box[1]))),
                    cv2.FONT_HERSHEY_SIMPLEX, .55, color, 2)
    return canvas


def write_image(path, image):
    if not cv2.imwrite(str(path), image):
        raise OSError(path)


def build(archive: Path, output: Path):
    if output.exists():
        raise FileExistsError(f'preserve existing package: {output}')
    old_manifest = read_json(OUTPUT / 'review_manifest_teacher.json')
    protected = [OUTPUT / name for name in ('index.html', 'manifest_original.json',
                   'review_manifest_teacher.json', 'annotation_policy_v1.md')]
    protected += [OUTPUT / row['raw_file'] for row in old_manifest['samples']]
    protected += [ROOT / name for name in ('cnn/model.py', 'cnn/contract.json',
                    'cnn/template/design_top_wrapper.v')]
    before = {str(path): sha256_file(path) for path in protected}
    old_hashes = {row['source_sha256'] for row in old_manifest['samples']}
    records = []
    with zipfile.ZipFile(archive) as source:
        names = source.namelist()
        if len(set(names)) != len(names):
            raise ValueError('duplicate archive member names')
        if sum(info.file_size for info in source.infolist()) > 2_000_000_000:
            raise ValueError('example archive exceeds inspection size budget')
        for info in source.infolist():
            safe_member(info.filename)
            if stat.S_ISLNK(info.external_attr >> 16) or info.file_size > 50_000_000:
                raise ValueError('symlink or oversized archive member')
        bad = source.testzip()
        if bad:
            raise ValueError(f'CRC failure: {bad}')
        metadata_bytes = source.read(BASE + 'data_info.json')
        metadata = json.loads(metadata_bytes)
        if len({row['frame_id'] for row in metadata}) != len(metadata):
            raise ValueError('duplicate metadata frame id')
        for row in metadata:
            image_member = paired_member(row['image_path'], 'image')
            label_member = paired_member(row['label_camera_std_path'], 'label/camera')
            if Path(image_member).stem != row['frame_id'] or Path(label_member).stem != row['frame_id']:
                raise ValueError('frame id and camera label/image filename mismatch')
            image_bytes, label_bytes = source.read(image_member), source.read(label_member)
            image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
            if image is None:
                raise ValueError(f'cannot decode {image_member}')
            height, width = image.shape[:2]
            objects, issues = inspect_objects(json.loads(label_bytes), width, height)
            counts = Counter(item['source_type'] for item in objects)
            estimated = sum(counts.values()) + sum(counts[key] for key in RIDERS)
            records.append(dict(sample_id='spd_inf_' + row['frame_id'],
                frame_id=row['frame_id'], width=width, height=height,
                camera_id=row['camera_id'], intersection_loc=row['intersection_loc'],
                sequence_id=row['sequence_id'], source_group=f'SPD:{row["intersection_loc"]}:{row["camera_id"]}:{row["sequence_id"]}',
                image_timestamp_raw=row['image_timestamp'], timestamp_unit='UNCONFIRMED',
                timestamp_sec=None, record_kind='sequence_frame',
                image_member=image_member, label_member=label_member,
                image_sha256=hashlib.sha256(image_bytes).hexdigest(),
                label_sha256=hashlib.sha256(label_bytes).hexdigest(),
                pixel_sha256_rgb=hashlib.sha256(cv2.cvtColor(image, cv2.COLOR_BGR2RGB).tobytes()).hexdigest(),
                source_counts=dict(counts), source_count=sum(counts.values()),
                estimated_split_count=estimated, objects=objects, issues=issues,
                proposed_role='road_development', human_review_status='PENDING',
                formal_gt_eligible=False, original_source_info=row))
        selected = select_pilot(records)
        output.mkdir(parents=True, exist_ok=False)
        (output / 'raw').mkdir()
        (output / 'views').mkdir()
        (output / 'raw/data_info.json').write_bytes(metadata_bytes)
        (output / 'raw/README.md').write_bytes(source.read('V2X-Seq-SPD-Example/README.md'))
        for row in selected:
            identity = row['sample_id']
            image_bytes = source.read(row['image_member'])
            (output / f'raw/{identity}.jpg').write_bytes(image_bytes)
            (output / f'raw/{identity}.json').write_bytes(source.read(row['label_member']))
            rgb = cv2.cvtColor(cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
            write_image(output / f'views/{identity}_official.jpg', overlay(rgb, row['objects']))
            write_image(output / f'views/{identity}_mapped.jpg', overlay(rgb, row['objects'], True))
            rgb720, transform = _letterbox_720(rgb)
            write_image(output / f'views/{identity}_input.png', cv2.cvtColor(resize_area(rgb720), cv2.COLOR_RGB2BGR))
            row['preprocess'] = dict(letterbox_720=transform, input_size=[512, 288],
                                     resize='existing integer.resize_area exact2/5 RNE', pixel_center=128)
    write_json(output / 'candidate_records.json', records)
    write_json(output / 'pilot_manifest.json', selected)
    unchanged = {path: sha256_file(Path(path)) == digest for path, digest in before.items()}
    write_json(output / 'protected_files_check.json', dict(baseline_sha256=before,
                                                         unchanged=unchanged, all_unchanged=all(unchanged.values())))
    classes = Counter()
    for row in records:
        classes.update(row['source_counts'])
    status = dict(stage='WAIT_HUMAN_REVIEW', archive=str(archive), archive_bytes=archive.stat().st_size,
        archive_sha256=sha256_file(archive), archive_crc='PASS', source='user-downloaded official SPD-Example link',
        official_url='https://drive.google.com/file/d/1gjOmGEBMcipvDzu2zOrO9ex_OscUZMYY/view',
        local_checksum_not_publisher_authentication=True, paired_frames=len(records),
        actual_source_groups=dict(Counter(row['source_group'] for row in records)), source_classes=dict(classes),
        low_density_prescreen_count=sum(row['estimated_split_count'] < 20 for row in records),
        pilot_count=len(selected), human_verified_count=0, ready_to_replace_count=0,
        geometry_issue_frame_count=sum(any(not obj['in_bounds'] for obj in row['objects']) for row in records),
        rider_issue_frame_count=sum(any(obj['source_type'] in RIDERS for obj in row['objects']) for row in records),
        old48_byte_duplicate_count=sum(row['image_sha256'] in old_hashes for row in records),
        full_training_leakage_check='NOT_RUN: no promotion; source group must be excluded from all future training',
        license='No license/usage agreement in example archive; permission scope must be verified before promotion/redistribution.',
        timestamp='Raw timestamps retained; unit not inferred from digit count.',
        all_protected_files_unchanged=all(unchanged.values()), training='NOT_RUN', rtl_changes=False,
        limitations=['Official 2d_box is source evidence, not verified complete project GT.',
            'Rider whole boxes not relabeled as person or vehicle; Van mapping remains pending.',
            'Density is an estimated source count with rider doubling, not a confirmed visible target total.',
            'All examples are a correlated one-camera sequence, not independent scene validation.'])
    write_json(output / 'execution_status.json', status)
    write_review(output, selected, status)
    return status


def write_review(output, selected, status):
    cards = []
    for i, row in enumerate(selected):
        identity = html.escape(row['sample_id'])
        issues = ''.join('<li>' + html.escape(issue) + '</li>' for issue in row['issues'])
        images = ''.join(f'<details {"open" if suffix == "raw" else ""}><summary>{title}</summary><img src="{path}" alt="{title}"></details>'
                        for suffix, title, path in [('raw','无框原图',f'raw/{identity}.jpg'),
                            ('official','官方原始类别框（非项目完整GT）',f'views/{identity}_official.jpg'),
                            ('mapped','项目映射候选：绿色直接映射，橙色待审',f'views/{identity}_mapped.jpg'),
                            ('input','实际512×288输入预览（无框）',f'views/{identity}_input.png')])
        cards.append(f'<section><h2>{i+1}. {identity}</h2><p>源对象 {row["source_count"]}；骑行者拆分后估计 {row["estimated_split_count"]}；{html.escape(str(row["source_counts"]))}</p>{images}<details><summary>类别／坐标问题</summary><ul>{issues}</ul></details><label>场景适合程度 <select data-status><option value="uncertain">未判断</option><option value="suitable_needs_labels">适合，但标签待修订</option><option value="replace">不适合，换来源</option></select></label><label>备注 <textarea placeholder="漏标、骑行者、太远太小、框范围等"></textarea></label><p><a href="raw/{identity}.json">原始标签</a></p></section>')
    binding = json.dumps([dict(sample_id=row['sample_id'], image_sha256=row['image_sha256'],
                              label_sha256=row['label_sha256']) for row in selected]).replace('<', '\\u003c')
    page = '''<!doctype html><html lang="zh"><meta charset="utf-8"><title>SPD替换先导审核</title>
<style>body{max-width:1200px;margin:24px auto;font-family:sans-serif;padding:12px}section{border:1px solid #aaa;padding:16px;margin:20px 0}img{max-width:100%;height:auto}summary,button{cursor:pointer;padding:10px}textarea{display:block;width:95%;height:60px}select{padding:8px}header{position:sticky;top:0;background:white;padding:12px;border:1px solid #ccc;z-index:1}</style>
<header><h1>SPD路侧8图先导：只审场景，不签完整GT</h1><p>这8图都来自同机位序列。官方框不保证完整；骑行者需人体/车体分开、Van待确认。橙色不是教师框。无需逐个重画，先判断这批是否值得继续。目标数仍需检查漏标。</p><label>审核人 <input id="reviewer" value="1"></label> <button id="export">导出8图意见</button><p>刷新前导出；本页不自动保存。不训练、不替换旧48图。</p></header>''' + ''.join(cards) + '''<script>
const bindings=BINDINGS;
document.getElementById('export').onclick=()=>{
const reviewer=document.getElementById('reviewer').value.trim();if(!reviewer){alert('请填写审核人');return;}
const reviews=[...document.querySelectorAll('section')].map((section,i)=>({...bindings[i],status:section.querySelector('select').value,notes:section.querySelector('textarea').value}));
const value={schema:'spd_pilot_suitability_v1',archive_sha256:'ARCHIVE',reviewer,reviewed_at_utc:new Date().toISOString(),complete_gt:false,reviews};
const url=URL.createObjectURL(new Blob([JSON.stringify(value,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download='spd_pilot_review_'+Date.now()+'.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
};</script></html>'''
    page = page.replace('BINDINGS', binding).replace('ARCHIVE', status['archive_sha256'])
    with (output / 'index.html').open('x', encoding='utf-8') as handle:
        handle.write(page)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.archive, args.output), ensure_ascii=False, indent=2))
