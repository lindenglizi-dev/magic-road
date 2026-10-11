"""Bounded A/C source screening only; never trains or publishes incomplete GT."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import html
import io
import json
from pathlib import Path, PurePosixPath
import shutil
import urllib.request
import zipfile

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from dataset import _letterbox_720
from fetch_coco import digest
from integer import resize_area
from prepare_scene_view_candidates import build_contact_sheet, build_thumbnail


ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'cnn/data/epfl_multiclass_pilot_20261009'
OUT = ROOT / 'cnn/reports/ac_source_screen_20261009_v1'
EPFL_PAGE = 'https://www.epfl.ch/labs/cvlab/data/data-multiclass/'
EPFL_BASE = 'https://documents.epfl.ch/groups/d/di/disal-sem/public/'
FILES = {
    'source.html': (EPFL_PAGE, 1024 * 1024),
    'multiclass_ground_truth.zip': (EPFL_BASE + 'multiclass_ground_truth.zip', 2 * 1024**2),
    'multiclass_ground_truth_images.zip': (EPFL_BASE + 'multiclass_ground_truth_images.zip', 40 * 1024**2),
}
FAMILY = 'epfl_multiclass_synchronized_campus_recording'


def fetch_epfl(name: str) -> dict:
    url, limit = FILES[name]
    destination = DATA / name
    if destination.exists():
        if not 0 < destination.stat().st_size <= limit:
            raise ValueError(f'Invalid existing source: {destination}')
        return {'path': str(destination), 'url': url, 'bytes': destination.stat().st_size,
                'sha256': digest(destination), 'reused': True}
    DATA.mkdir(parents=True, exist_ok=True)
    if shutil.disk_usage(DATA).free < limit + 256 * 1024**2:
        raise OSError('Insufficient free space for bounded source download')
    partial = destination.with_suffix(destination.suffix + '.part')
    # Preserve an interrupted download instead of silently overwriting its evidence.
    if partial.exists():
        raise FileExistsError(partial)
    request = urllib.request.Request(url, headers={'User-Agent': 'RoadYOLO-research/1'})
    with urllib.request.urlopen(request, timeout=30) as response:
        expected = int(response.headers.get('Content-Length', '0'))
        if expected > limit:
            raise ValueError('Official source exceeds the bounded download budget')
        if name.endswith('.zip') and 'zip' not in response.headers.get('Content-Type', ''):
            raise ValueError('Expected ZIP, received another content type')
        with partial.open('xb') as stream:
            while block := response.read(1024 * 1024):
                if stream.tell() + len(block) > limit:
                    raise ValueError('Download exceeds byte budget')
                stream.write(block)
        if not partial.stat().st_size or (expected and partial.stat().st_size != expected):
            raise ValueError('Incomplete download')
        final_url = response.geturl()
    if name.endswith('.zip'):
        with zipfile.ZipFile(partial) as archive:
            if archive.testzip() is not None:
                raise ValueError('ZIP CRC failed')
    partial.rename(destination)
    return {'path': str(destination), 'url': url, 'final_url': final_url,
            'bytes': destination.stat().st_size, 'sha256': digest(destination), 'reused': False}


def safe_members(archive: zipfile.ZipFile) -> list[zipfile.ZipInfo]:
    members = [entry for entry in archive.infolist() if not entry.is_dir()]
    names = set()
    for entry in members:
        name = PurePosixPath(entry.filename)
        if (name.is_absolute() or '..' in name.parts or ':' in entry.filename
                or '\\' in entry.filename or entry.filename in names
                or entry.file_size > 32 * 1024**2):
            raise ValueError(f'Unsafe ZIP entry: {entry.filename}')
        names.add(entry.filename)
    if len(members) > 10000 or sum(entry.file_size for entry in members) > 512 * 1024**2:
        raise ValueError('Archive exceeds extraction budget')
    return members


def fetch() -> None:
    receipt = OUT / 'epfl_download_receipt.json'
    if receipt.exists():
        raise FileExistsError(receipt)
    downloads = [fetch_epfl(name) for name in FILES]
    inventories = {}
    for name in FILES:
        if not name.endswith('.zip'):
            continue
        with zipfile.ZipFile(DATA / name) as archive:
            entries = safe_members(archive)
            inventories[name] = [{'name': entry.filename, 'bytes': entry.file_size,
                                  'crc32': entry.CRC} for entry in entries]
    OUT.mkdir(parents=True, exist_ok=True)
    payload = {'schema': 'epfl_ac_download_v1', 'purpose': 'source screening, not data freeze',
               'source_url': EPFL_PAGE, 'license_url': EPFL_PAGE,
               'license_note': 'Official page permits research; public demo/redistribution scope not yet confirmed.',
               'family_id': FAMILY,
               'split_note': 'All six synchronized views belong to one original family; no random train/dev split.',
               'training_started': False, 'labels_changed': False, 'frozen': False,
               'downloads': downloads, 'archives': inventories}
    receipt.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for name, entries in inventories.items():
        print(name, len(entries), 'members', entries[:8], flush=True)
    print(receipt, flush=True)


def epfl_boxes(archive: zipfile.ZipFile, camera: int, ordinal: int) -> tuple[list[dict], list[str]]:
    boxes, absent = [], []
    names = set(archive.namelist())
    for label in ('person', 'car', 'bus'):
        name = (f'bounding_boxes_EPFL_cross/gt_files242_{label}/visible_frame/'
                f'det_frame{ordinal}_cam{camera}.txt')
        if name not in names:
            absent.append(label)
            continue
        raw = archive.read(name)
        for row_number, line in enumerate(raw.decode('ascii').splitlines(), 1):
            if not line.strip():
                continue
            box = list(map(float, line.split()))
            if (len(box) != 4 or not np.isfinite(box).all()
                    or box[0] >= box[2] or box[1] >= box[3]):
                raise ValueError(f'Invalid source box: {name}:{row_number}')
            boxes.append({'source_class': label, 'xyxy_raw': box, 'member': name,
                          'row': row_number, 'member_sha256': hashlib.sha256(raw).hexdigest()})
    return boxes, absent


def prepare_image(image: Image.Image, row: dict, overlay: Image.Image) -> dict:
    asset = OUT / 'images' / row['candidate_id']
    asset.mkdir(parents=True, exist_ok=False)
    image = image.convert('RGB')
    image.save(asset / 'raw.png')
    overlay.save(asset / 'source_boxes.png')
    canvas, transform = _letterbox_720(np.asarray(image))
    Image.fromarray(resize_area(canvas)).save(asset / 'network.png')
    row['size'] = list(image.size)
    row['preprocess_transform'] = transform
    row['preprocess_note'] = 'Existing center-letterbox to 720p then exact 2/5 area resize; no inference.'
    row['assets'] = {name: {'path': str((asset / f'{name}.png').resolve()),
                            'sha256': digest(asset / f'{name}.png')}
                     for name in ('raw', 'source_boxes', 'network')}
    thumb = asset / 'thumb.jpg'
    build_thumbnail(asset / 'raw.png', thumb)
    row['thumbnail_path'] = str(thumb.resolve())
    row['training_eligible'] = False
    row['review_status'] = 'candidate_pending_full_frame_coverage_and_coordinate_contract'
    return row


def build() -> None:
    if (OUT / 'screening_manifest.json').exists() or (OUT / 'images').exists():
        raise FileExistsError('Preserve prior screening output; do not overwrite')
    receipt = json.loads((OUT / 'epfl_download_receipt.json').read_text(encoding='utf-8'))
    for entry in receipt['downloads']:
        if digest(Path(entry['path'])) != entry['sha256']:
            raise ValueError('Downloaded source changed')
    rows, source_counts = [], Counter()
    font = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 11)
    with zipfile.ZipFile(DATA / 'multiclass_ground_truth.zip') as labels, \
            zipfile.ZipFile(DATA / 'multiclass_ground_truth_images.zip') as images:
        for entry in safe_members(labels):
            if entry.filename.endswith('.txt'):
                category = entry.filename.split('gt_files242_')[1].split('/')[0]
                source_counts[category] += sum(bool(line.strip()) for line in labels.read(entry).splitlines())
        # Two fixed annotation ordinals, five views. Not ten independent scenes or original-video frame IDs.
        for camera in (0, 4, 5, 2, 3):
            scene = 'A' if camera in (0, 4, 5) else 'C'
            for ordinal in (40, 160):
                member = f'c{camera}/{ordinal:08d}.jpg'
                raw = images.read(member)
                image = Image.open(io.BytesIO(raw)).convert('RGB')
                boxes, absent = epfl_boxes(labels, camera, ordinal)
                overlay = image.copy()
                draw = ImageDraw.Draw(overlay)
                for index, box in enumerate(boxes, 1):
                    color = '#10c14a' if box['source_class'] == 'person' else '#168aff'
                    draw.rectangle(box['xyxy_raw'], outline=color, width=2)
                    draw.text((box['xyxy_raw'][0], max(0, box['xyxy_raw'][1] - 13)),
                              f"{box['source_class']}{index}", fill=color, font=font)
                row = {'candidate_id': f'epfl_c{camera}_o{ordinal:03d}', 'scene': scene,
                       'visual_class': '固定斜俯视', 'scene_type': '校园通道' if scene == 'A' else '校园停车位/邻接通道',
                       'source': 'EPFL Multi-view Multi-class', 'source_url': EPFL_PAGE,
                       'camera_id': f'EPFL:c{camera}', 'family_id': FAMILY,
                       'source_archive': str(DATA / 'multiclass_ground_truth_images.zip'),
                       'source_member': member, 'source_sha256': hashlib.sha256(raw).hexdigest(),
                       'annotation_ordinal': ordinal, 'original_video_frame': None,
                       'boxes': boxes, 'missing_class_files': absent,
                       'concerns': ['仅提供person/car/bus，当前vehicle还包含自行车/摩托车；需核实可见两轮车是否漏标。',
                                    '缺少某类txt不能在未证实格式约定前自动当作该类零目标。',
                                    'XYXY按原值仅作预览；0/1基、可见/完整范围及原视频帧号映射尚未冻结。',
                                    '六视角为同一次同步拍摄，不可跨训练/开发原片家族；图像原生360×288。']}
                rows.append(prepare_image(image, row, overlay))
    selection_path = ROOT / 'cnn/reports/post_review_s_20261007_v1/ground48/selection.json'
    selection = json.loads(selection_path.read_text(encoding='utf-8'))
    wanted = ('VIRAT_S_000200_00_000100_000171_f0001376',
              'VIRAT_S_010107_02_000282_000312_f0000249')
    for image_id in wanted:
        item = next(item for item in selection['selected'] if item['image_id'] == image_id)
        directory = selection_path.parent / 'images' / image_id
        raw_path = directory / 'raw.png'
        if digest(raw_path) != item['source_sha256']:
            raise ValueError('VIRAT source does not match frozen selection')
        row = {'candidate_id': image_id, 'scene': 'C', 'visual_class': '固定斜俯视',
               'scene_type': '停车场/邻接道路', 'source': 'VIRAT Ground Release 2',
               'source_url': 'https://viratdata.org/', 'camera_id': item['camera_id'],
               'family_id': item['camera_id'], 'sequence_id': item['selection_clip_id'],
               'original_video_frame': item['frame_index'], 'original_path': str(raw_path),
               'source_sha256': digest(raw_path), 'selection_sha256': digest(selection_path),
               'source_overlay_path': str(directory / 'source_overlay.png'),
               'source_overlay_sha256': digest(directory / 'source_overlay.png'),
               'concerns': ['仅复用先前已查看的开发图，不读盲测预留。',
                            '既有来源框核查未证明全帧完整；画面可见但未标的车辆不能当背景。',
                            '不是要求用户重新补完Ground48，本批只作场景/标注覆盖对照。']}
        with Image.open(raw_path) as image, Image.open(directory / 'source_overlay.png') as overlay:
            rows.append(prepare_image(image, row, overlay.convert('RGB')))
    payload = {'schema': 'road_ac_source_screen_v1', 'purpose': '12 representative frames, not training GT',
               'screening_locked': True, 'dataset_frozen': False, 'G_ready': False,
               'verified_train_images': 0, 'verified_dev_images': 0,
               'target': {'train': 256, 'fallback_train': 128, 'main_dev': 64},
               'training_started': False, 'model_inference_run': False, 'labels_changed': False,
               'acceptance_changed': False, 'D_allowed_in_main_training': False,
               'scene_counts': dict(Counter(row['scene'] for row in rows)),
               'epfl_source_row_counts': dict(source_counts),
               'epfl_web_claim_counts': {'person': 1297, 'car': 3553, 'bus': 56},
               'epfl_count_note': 'Downloaded archive totals differ slightly from web summary; preserved, not deduplicated or repaired.',
               'source_receipt_sha256': digest(OUT / 'epfl_download_receipt.json'),
               'preprocess_source_sha256': {str(path.relative_to(ROOT)): digest(path)
                                            for path in (ROOT / 'cnn/dataset.py', ROOT / 'cnn/integer.py')},
               'read_boundary': ['New EPFL publicly released unsplit candidate images and labels only.',
                                 'Two previously viewed Ground48 source images and existing source overlays.',
                                 'No test/blind/reserve pixels or labels; no teacher/student inference.'],
               'blockers': ['No two verified complete A/C sources with camera/original-family-isolated train/dev.',
                            'EPFL category coverage and coordinate/absence semantics require closure.',
                            'VIRAT existing coverage gap remains; Intersection reviewed scenes remain D stress only.'],
               'frames': rows}
    (OUT / 'screening_manifest.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    build_contact_sheet(rows, OUT / 'contact_sheet.jpg', cols=3)
    build_page(payload)
    check()


def build_page(payload: dict) -> None:
    escape = html.escape
    audit_path = OUT / 'visual_audit.json'
    findings = {}
    if audit_path.exists():
        audit = json.loads(audit_path.read_text(encoding='utf-8'))
        findings = {item['candidate_id']: item['note'] for item in audit['findings']}
    parts = ['<!doctype html><html lang="zh-CN"><meta charset="utf-8">',
             '<meta name="viewport" content="width=device-width, initial-scale=1">',
             '<title>A/C首批12帧来源核查</title><style>',
             'body{font:16px/1.7 "Microsoft YaHei",sans-serif;margin:24px auto;padding:0 16px;max-width:1150px;color:#182635;background:#f4f6f8}',
             'article,header{background:white;padding:18px;margin:20px 0;border:1px solid #b9c7d6;border-radius:8px}',
             'img{max-width:100%;height:auto}details{margin:12px 0}summary{cursor:pointer;padding:8px}a{color:#12528b}',
             '.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px}.warn{color:#8b2a0b}code{overflow-wrap:anywhere}',
             '</style><header><h1>A/C首批12张代表帧</h1>',
             '<p>A通道6张、C停车场/园区6张。默认无框原图；展开可看官方来源框和512×288预览。没有模型预测或教师框。</p>',
             '<p class="warn"><strong>场景候选已锁定，训练/开发数据尚未冻结。</strong>不完整标注不能直接用于训练；当前合格train=0、dev=0。</p>',
             '<p>EPFL十张图是五个视角、两个同步采样编号，不是十个独立场景；六相机属于同一原片家族。',
             '其原生图360×288，512预览中的黑边来自现有等比例预处理；放大不会新增细节。</p>',
             '<p><a href="筛选结果与冻结状态.txt">筛选结果与下一步</a> · <a href="screening_manifest.json">逐帧来源与哈希</a></p></header>']
    for index, row in enumerate(payload['frames'], 1):
        assets = {key: Path(value['path']).relative_to(OUT).as_posix() for key, value in row['assets'].items()}
        parts += [f'<article id="f{index}"><h2>{index:02d} · {row["scene"]} · {escape(row["scene_type"])}</h2>',
                  f'<p><code>{escape(row["candidate_id"])}</code><br>来源：<a href="{escape(row["source_url"], quote=True)}">{escape(row["source"])}</a>',
                  f'；机位：{escape(row["camera_id"])}；资格：待核实，不进入训练。</p>',
                  f'<p>原片家族：<code>{escape(row["family_id"])}</code></p>',
                  (f'<p class="warn"><strong>本轮发现：</strong>{escape(findings[row["candidate_id"]])}</p>'
                   if row['candidate_id'] in findings else ''),
                  f'<div class="grid"><div><h3>完整无框原图</h3><a href="{assets["raw"]}"><img src="{assets["raw"]}" alt="完整无框原图 {index}"></a></div>',
                  f'<div><h3>512×288输入预览（非预测）</h3><img src="{assets["network"]}" alt="现有预处理预览 {index}"></div></div>',
                  '<details><summary>展开官方来源框：绿person、蓝car/bus；VIRAT沿用既有来源预览配色。不是模型识别结果。</summary>',
                  f'<a href="{assets["source_boxes"]}"><img src="{assets["source_boxes"]}" alt="来源标注框 {index}"></a></details>',
                  '<h3>核查要点</h3><ul>']
        parts += [f'<li>{escape(note)}</li>' for note in row['concerns']]
        parts += ['</ul></article>']
    parts += ['<footer><p>只读样例册，无导入/训练按钮。不修改旧标签、旧审核页或场景选择记录。</p></footer></html>']
    (OUT / 'index.html').write_text('\n'.join(parts), encoding='utf-8')


def check() -> None:
    payload = json.loads((OUT / 'screening_manifest.json').read_text(encoding='utf-8'))
    assert len(payload['frames']) == 12 and payload['scene_counts'] == {'A': 6, 'C': 6}
    assert payload['dataset_frozen'] is False and payload['G_ready'] is False
    assert payload['training_started'] is False and payload['labels_changed'] is False
    assert payload['D_allowed_in_main_training'] is False
    assert len({row['source_sha256'] for row in payload['frames']}) == 12
    expected_epfl = {f'epfl_c{camera}_o{ordinal:03d}': (camera, ordinal)
                     for camera in (0, 4, 5, 2, 3) for ordinal in (40, 160)}
    expected_virat = {'VIRAT_S_000200_00_000100_000171_f0001376',
                      'VIRAT_S_010107_02_000282_000312_f0000249'}
    assert {row['candidate_id'] for row in payload['frames']} == set(expected_epfl) | expected_virat
    receipt = json.loads((OUT / 'epfl_download_receipt.json').read_text(encoding='utf-8'))
    assert digest(OUT / 'epfl_download_receipt.json') == payload['source_receipt_sha256']
    for entry in receipt['downloads']:
        assert digest(Path(entry['path'])) == entry['sha256']
    for row in payload['frames']:
        assert row['scene'] in ('A', 'C') and row['training_eligible'] is False
        for key, asset in row['assets'].items():
            path = Path(asset['path'])
            assert path.is_relative_to(OUT) and digest(path) == asset['sha256']
            with Image.open(path) as image:
                image.load()
                if key == 'network':
                    assert image.size == (512, 288)
        with Image.open(row['assets']['raw']['path']) as image:
            pixels = np.asarray(image.convert('RGB'))
        if 'source_archive' in row:
            camera, ordinal = expected_epfl[row['candidate_id']]
            assert row['family_id'] == FAMILY and row['camera_id'] == f'EPFL:c{camera}'
            assert row['annotation_ordinal'] == ordinal
            assert Path(row['source_archive']) == DATA / 'multiclass_ground_truth_images.zip'
            assert row['source_member'] == f'c{camera}/{ordinal:08d}.jpg'
            with zipfile.ZipFile(row['source_archive']) as archive:
                raw = archive.read(row['source_member'])
            assert hashlib.sha256(raw).hexdigest() == row['source_sha256']
            with Image.open(io.BytesIO(raw)) as source:
                assert np.array_equal(pixels, np.asarray(source.convert('RGB')))
            with zipfile.ZipFile(DATA / 'multiclass_ground_truth.zip') as archive:
                boxes, absent = epfl_boxes(archive, camera, ordinal)
                assert row['boxes'] == boxes and row['missing_class_files'] == absent
        else:
            expected_directory = (ROOT / 'cnn/reports/post_review_s_20261007_v1/ground48/images'
                                  / row['candidate_id'])
            assert Path(row['original_path']) == expected_directory / 'raw.png'
            assert Path(row['source_overlay_path']) == expected_directory / 'source_overlay.png'
            assert digest(Path(row['original_path'])) == row['source_sha256']
            assert digest(Path(row['source_overlay_path'])) == row['source_overlay_sha256']
            with Image.open(row['original_path']) as source:
                assert np.array_equal(pixels, np.asarray(source.convert('RGB')))
        canvas, transform = _letterbox_720(pixels)
        assert transform == row['preprocess_transform']
        with Image.open(row['assets']['network']['path']) as image:
            assert np.array_equal(np.asarray(image), resize_area(canvas))
    for relative, expected in payload['preprocess_source_sha256'].items():
        assert digest(ROOT / relative) == expected
    print(f'PASS: 12 source-bound A/C frames, unique source hashes, preview sizes, no false freeze: {OUT}')


def self_test() -> None:
    import io
    for filename, valid in [('camera0/frame.png', True), ('../escape.png', False),
                            ('/escape.png', False), ('C:/escape.png', False),
                            ('camera0\\..\\escape.png', False)]:
        memory = io.BytesIO()
        with zipfile.ZipFile(memory, 'w') as archive:
            archive.writestr(filename, b'123')
        memory.seek(0)
        with zipfile.ZipFile(memory) as archive:
            try:
                result = safe_members(archive)
                assert valid and len(result) == 1
            except ValueError:
                assert not valid
    for count, expected in [(128, 2), (256, 4)]:
        assert (count + 63) // 64 == expected
    for values, valid in [('1 2 3 4', True), ('1 2 nan 4', False), ('3 2 1 4', False)]:
        memory = io.BytesIO()
        with zipfile.ZipFile(memory, 'w') as archive:
            archive.writestr('bounding_boxes_EPFL_cross/gt_files242_person/visible_frame/det_frame40_cam0.txt', values)
        with zipfile.ZipFile(memory) as archive:
            try:
                boxes, absent = epfl_boxes(archive, 0, 40)
                assert valid and len(boxes) == 1 and absent == ['car', 'bus']
            except ValueError:
                assert not valid
    print('PASS: safe archive boundaries, invalid coordinates, explicit missing-class state and pilot update arithmetic')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fetch-epfl', action='store_true')
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--build', action='store_true')
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--render-page', action='store_true', help='Refresh only this screening HTML from locked assets and audit notes')
    args = parser.parse_args()
    if args.self_test:
        self_test()
    elif args.fetch_epfl:
        fetch()
    elif args.build:
        build()
    elif args.check:
        check()
    elif args.render_page:
        check()
        build_page(json.loads((OUT / 'screening_manifest.json').read_text(encoding='utf-8')))
    else:
        parser.error('choose --self-test, --fetch-epfl, --build, --check or --render-page')
