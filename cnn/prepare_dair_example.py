"""Inspect the downloaded DAIR-I example; keep AI additions unsigned and quarantined."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import html
import io
import json
import math
from pathlib import Path
import stat
import time
import zipfile

from PIL import Image, ImageDraw

from .prepare_ground48 import ROOT, read_json, sha256_file, write_json
from .prepare_spd_pilot import safe_member

ARCHIVE = Path('E:/EDownloads/example-single-infrastructure-side.zip')
EXPECTED_SHA = '02135f0265706ef56e459d298fb1e2b93e08eb468f6a773878486488ee208d39'
BASE = 'single-infrastructure-side/'
OUT = ROOT / 'cnn/reports/dair_example_ai_20261010_v1'
DIRECT = {'Pedestrian': 'person', 'Car': 'vehicle', 'Van': 'vehicle',
          'Truck': 'vehicle', 'Bus': 'vehicle'}


def box_values(obj, width, height):
    box = [float(obj['2d_box'][k]) for k in ('xmin', 'ymin', 'xmax', 'ymax')]
    if not (all(math.isfinite(v) for v in box) and
            0 <= box[0] < box[2] <= width and 0 <= box[1] < box[3] <= height):
        raise ValueError(f'invalid source box: {box}')
    return box


def member(relative, folder):
    safe_member(relative)
    if not relative.startswith(folder + '/'):
        raise ValueError(f'wrong member kind: {relative}')
    return BASE + relative


def draw_view(sample, objects, destination, color):
    with Image.open(OUT / sample['raw_file']) as raw:
        image = raw.convert('RGB')
    draw = ImageDraw.Draw(image)
    for obj in objects:
        ink = obj.get('color', color)
        draw.rectangle(obj['bbox'], outline=ink, width=2)
        label = obj['id'] + ' ' + obj.get('class', obj.get('source_type', ''))
        draw.text((obj['bbox'][0], max(0, obj['bbox'][1] - 12)), label,
                  fill=ink, stroke_width=1, stroke_fill='black')
    image.save(destination, quality=95)


def build():
    if OUT.exists():
        raise FileExistsError('preserve existing inspection, do not overwrite')
    assert sha256_file(ARCHIVE) == EXPECTED_SHA, 'unexpected archive version'
    protected_paths = [ROOT / p for p in (
        'cnn/model.py', 'cnn/train.py', 'cnn/contract.json',
        'cnn/reports/ac_signed_progress_20261010_v1/reviewed_partial_labels.json')]
    protected = {str(p): sha256_file(p) for p in protected_paths}
    records, counts, locations = [], Counter(), Counter()
    with zipfile.ZipFile(ARCHIVE) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ValueError('duplicate ZIP members')
        assert sum(i.file_size for i in archive.infolist()) < 100_000_000
        for info in archive.infolist():
            safe_member(info.filename)
            if stat.S_ISLNK(info.external_attr >> 16) or info.file_size > 20_000_000:
                raise ValueError('symlink or excessive member size')
        assert archive.testzip() is None, 'ZIP CRC failure'
        rows = json.loads(archive.read(BASE + 'data_info.json'))
        for row in sorted(rows, key=lambda r: r['image_path']):
            image_member = member(row['image_path'], 'image')
            label_member = member(row['label_camera_std_path'], 'label/camera')
            assert Path(image_member).stem == Path(label_member).stem
            raw = archive.read(image_member)
            with Image.open(io.BytesIO(raw)) as image:
                image.verify()
            with Image.open(io.BytesIO(raw)) as image:
                width, height = image.size
            labels = json.loads(archive.read(label_member))
            objects = [dict(id=f'o{i+1}', source_type=o['type'],
                       proposed_class=DIRECT.get(o['type']), bbox=box_values(o, width, height),
                       source_record=o) for i, o in enumerate(labels)]
            calib = [json.loads(archive.read(member(row[k], 'calib'))) for k in
                     ('calib_camera_intrinsic_path', 'calib_virtuallidar_to_camera_path')]
            calibration_sha = hashlib.sha256(json.dumps(calib, sort_keys=True).encode()).hexdigest()
            counts.update(o['type'] for o in labels)
            locations[row['intersection_loc']] += 1
            records.append(dict(image_id=Path(image_member).stem, image_member=image_member,
                label_member=label_member, image_sha256=hashlib.sha256(raw).hexdigest(),
                label_sha256=hashlib.sha256(archive.read(label_member)).hexdigest(),
                width=width, height=height, location=row['intersection_loc'],
                calibration_sha256=calibration_sha, original=objects, source_record=row))
        assert len({r['image_id'] for r in records}) == len(records) == 71
        assert len([n for n in names if n.startswith(BASE+'image/') and n.endswith('.jpg')]) == 71
        assert len([n for n in names if n.startswith(BASE+'label/camera/') and n.endswith('.json')]) == 71
        OUT.mkdir(parents=True)
        # ponytail: eight source-position representatives, not exhaustive visual review of 71 frames.
        groups = sorted(set(r['calibration_sha256'] for r in records))
        selected = []
        for group in groups:
            family = [r for r in records if r['calibration_sha256'] == group]
            selected.extend(family[round(i*(len(family)-1)/3)] for i in range(4))
        assert len(selected) == 8
        for record in selected:
            folder = OUT / record['image_id']
            folder.mkdir()
            raw = archive.read(record['image_member'])
            with (folder/'raw.jpg').open('xb') as stream:
                stream.write(raw)
            record.update(raw_file=f'{record["image_id"]}/raw.jpg',
                          split='quarantine_no_train_or_dev_assignment', teacher=[])
            draw_view(record, record['original'], folder/'official.jpg', '#00ff66')
            with Image.open(io.BytesIO(raw)) as image:
                from .dataset import _letterbox_720
                from .integer import resize_area
                import numpy as np
                rgb720,_ = _letterbox_720(np.array(image.convert('RGB')))
                Image.fromarray(resize_area(rgb720)).save(folder/'input_preview.png')
        for start in range(0, len(records), 20):
            sheet = Image.new('RGB', (1600, 1000), 'white')
            draw = ImageDraw.Draw(sheet)
            for i, record in enumerate(records[start:start+20]):
                with Image.open(io.BytesIO(archive.read(record['image_member']))) as image:
                    image = image.convert('RGB'); image.thumbnail((400, 225))
                x, y = i % 4 * 400, i // 4 * 200
                image.thumbnail((400, 175))
                sheet.paste(image, (x, y+25))
                draw.text((x+4, y+5), record['image_id']+' '+record['location'], fill='black')
            sheet.save(OUT/f'contact_{start:03d}.jpg', quality=92)
    receipt = dict(schema='dair_example_quarantined_ai_v1', archive=str(ARCHIVE),
        archive_sha256=EXPECTED_SHA, archive_bytes=ARCHIVE.stat().st_size,
        CRC_passed=True, paired_images=71, decoded_images=71, locations=dict(locations),
        source_class_rows=dict(counts), all_source_boxes_in_bounds=True,
        calibration_groups=len(groups), selected_images=8,
        selection='four evenly spaced source positions per calibration group, before inference',
        official_source='https://github.com/AIR-THU/DAIR-V2X',
        coordinate_endpoint_convention_verified=False,
        physical_camera_isolation_from_SPD_verified=False,
        complete_project_GT_verified=False, dataset_license_certified=False,
        new_human_assignments=0, human_workload_cap=32, training_started=False,
        G_ready=False, dataset_frozen=False, GPU_used=False,
        records=records, samples=selected, protected=protected)
    write_json(OUT/'inspection.json', receipt)
    print('PASS ZIP CRC,71 paired decoded images,all boxes in bounds;8 quarantined representatives', flush=True)


def hints():
    import torch
    from .build_verified_review import decode_heads
    from .dataset import _letterbox_transform
    from .teacher import capture_raw_heads, load_official_model, teacher_input, tree_hash
    if (OUT/'teacher_hints.json').exists():
        raise FileExistsError('preserve prior inference')
    receipt = read_json(OUT/'inspection.json')
    assert [s['image_id'] for s in receipt['samples']]==['000000','000011','000021','000034','000036','000049','000066','000097']
    assets = ROOT/'cnn/teacher_assets'; binding = read_json(assets/'receipt.json')
    weights = assets/'yolox_s.pth'; source = assets/'source/YOLOX-0.3.0'
    assert sha256_file(weights) == binding['weights']['sha256']
    assert tree_hash(source/'yolox') == binding['source_tree_sha256']
    torch.set_num_threads(2); torch.set_num_interop_threads(1)
    device = torch.device('cpu'); model = load_official_model(source, weights, device)
    start = time.perf_counter()
    for sample in receipt['samples']:
        path = OUT/sample['raw_file']
        assert sha256_file(path) == sample['image_sha256']
        transform = _letterbox_transform(sample['width'], sample['height'])
        row = dict(image_path=path, preprocess=dict(raw_image=True, letterbox_1280x720=transform))
        predictions = decode_heads(capture_raw_heads(model, teacher_input(row, device)), transform)
        for i, prediction in enumerate(predictions):
            prediction.update(id=f't{i}', kind='TEACHER_HINT_NOT_GT')
        sample['teacher'] = predictions
        draw_view(sample, predictions, OUT/sample['image_id']/'teacher.jpg', '#ff9900')
        print(sample['image_id'], len(predictions), 'CPU hints', flush=True)
    write_json(OUT/'teacher_hints.json', dict(samples=receipt['samples'], device='cpu',
        GPU_used=False, training_started=False, seconds=time.perf_counter()-start,
        weight_sha256=sha256_file(weights), source_tree_sha256=binding['source_tree_sha256'],
        input='1024x576 FP32 BGR', confidence=.1, nms_iou=.6, script_sha256=sha256_file(Path(__file__))))


def details():
    regions = {'000000': [(1500,250,1920,450),(540,260,670,390)],
               '000011': [(1550,250,1920,700),(520,260,790,370)],
               '000021': [(1550,240,1920,450)],
               '000034': [(1650,240,1920,540),(1280,620,1410,840)],
               '000036': [(1280,150,1850,370)],
               '000049': [(1280,150,1550,370)],
               '000066': [(1280,150,1700,330)],
               '000097': [(840,270,990,400),(1550,250,1850,400)]}
    for identity, boxes in regions.items():
        with Image.open(OUT/identity/'raw.jpg') as image:
            for i, box in enumerate(boxes):
                path=OUT/identity/f'detail_{i}.png'
                if path.exists():
                    raise FileExistsError(path)
                crop=image.crop(box)
                crop.resize((crop.width*2,crop.height*2)).save(path)
    print('Saved fixed raw crops,2x display only; coordinates remain original-image XYXY')


def validate_addition(value, sample):
    if not isinstance(value, list) or len(value) != 4:
        raise ValueError('addition must be class,XYXY,source-id,reason')
    label, box, reference, reason = value
    if label not in ('person','vehicle') or not isinstance(box,list) or len(box)!=4:
        raise ValueError('invalid class or box')
    box_values({'2d_box':dict(zip(('xmin','ymin','xmax','ymax'),box))},sample['width'],sample['height'])
    if reference and reference not in {o['id'] for o in sample['original']}:
        raise ValueError('unknown original target reference')
    if not isinstance(reason,str) or not reason.strip():
        raise ValueError('missing visual reason')


def previews():
    """Refresh only our unpublished derived previews with the existing exact preprocessor."""
    import numpy as np
    from .dataset import _letterbox_720
    from .integer import resize_area
    path=OUT/'preview_receipt.json'
    if path.exists():
        raise FileExistsError(path)
    records=[]
    for sample in read_json(OUT/'inspection.json')['samples']:
        with Image.open(OUT/sample['raw_file']) as image:
            rgb720,transform=_letterbox_720(np.array(image.convert('RGB')))
        output=OUT/sample['image_id']/'input_preview.png'
        Image.fromarray(resize_area(rgb720)).save(output)
        records.append(dict(image_id=sample['image_id'],transform=transform,
                            preview_sha256=sha256_file(output)))
    write_json(path,dict(contract='existing letterbox_720 then integer.resize_area exact2/5 RNE',
                        records=records,FPGA_verified=False))


def draft():
    if (OUT/'ai_additions.json').exists() or (OUT/'index.html').exists():
        raise FileExistsError('preserve prior AI draft')
    hints_receipt=read_json(OUT/'teacher_hints.json')
    edits=read_json(OUT/'assistant_edits.json')
    samples=hints_receipt['samples']
    assert set(edits['images'])=={s['image_id'] for s in samples}
    results=[]; counts=Counter(); cards=[]
    for sample in samples:
        identity=sample['image_id']; edit=edits['images'][identity]; additions=[]
        for i,value in enumerate(edit['add'],1):
            validate_addition(value,sample)
            label,box,reference,reason=value
            additions.append(dict(id=f'ai{i:03d}',**{'class':label},bbox=box,
                source_target_id=reference or None,reason=reason,
                kind='AI_VISUAL_DRAFT_NOT_GT',human_verified=False,color='#00cfff'))
        counts.update(o['class'] for o in additions)
        kept=[dict(id=o['id'],**{'class':o['proposed_class']},bbox=o['bbox'],
                   kind='OFFICIAL_REFERENCE_NOT_VERIFIED',color='#00ff66')
              for o in sample['original'] if o['proposed_class']]
        unresolved=[o['id'] for o in sample['original'] if not o['proposed_class']
                    and o['source_type']!='Trafficcone']
        folder=OUT/identity
        draw_view(sample,additions,folder/'ai_only.jpg','#00cfff')
        draw_view(sample,kept+additions,folder/'combined_draft.jpg','#00ff66')
        results.append(dict(image_id=identity,source_image_sha256=sample['image_sha256'],
            source_label_sha256=sample['label_sha256'],additions=additions,
            direct_source_reference=kept,unresolved_original_ids=unresolved,
            note=edit['note'],uncertain=edit['uncertain'],complete=False,
            human_verified=False,training_eligible=False,split='quarantine',scene='D'))
        views=[('raw.jpg','无框原图'),('ai_only.jpg','只看AI补画（青色）'),
               ('combined_draft.jpg','来源参考＋AI草稿（绿色＋青色）'),
               ('official.jpg','官方原始类别框'),('teacher.jpg','教师提示（橙色，含误检，不是GT）'),
               ('input_preview.png','512×288面积缩放预览（不是FPGA对拍）')]
        details_html=''.join(f'<details {"open" if filename=="ai_only.jpg" else ""}><summary>{title}</summary><a href="{identity}/{filename}"><img loading="lazy" src="{identity}/{filename}" alt="{identity} {title}"></a></details>' for filename,title in views)
        issues=''.join('<li>'+html.escape(note)+'</li>' for note in edit['uncertain'])
        cards.append(f'<section><h2>{identity}：AI新增{len(additions)}框</h2><p>{html.escape(edit["note"])}</p>{details_html}<h3>尚未闭合，不能签完整GT</h3><ul>{issues}</ul></section>')
    result=dict(schema='dair_assistant_unsigned_additions_v1',archive_sha256=EXPECTED_SHA,
        ai_edits_sha256=sha256_file(OUT/'assistant_edits.json'),
        teacher_hints_sha256=sha256_file(OUT/'teacher_hints.json'),
        coordinate_contract=edits['coordinate_contract'],images=results,
        AI_added_box_counts=dict(counts),AI_inspected_representatives=8,
        full_archive_visually_completed=False,human_verified=False,
        complete_GT=False,dataset_frozen=False,G_ready=False,training_started=False,
        new_human_assignments=0,human_workload_cap=32,GPU_used=False,
        source_gate='not_A_C_main_domain; D junction with darker/daylight images; quarantined',
        physical_family='keep all71 together; two calibration variants are not independent cameras')
    write_json(OUT/'ai_additions.json',result)
    page='''<!doctype html><html lang="zh"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DAIR样例检查与AI补画草稿</title>
<style>body{max-width:1500px;margin:24px auto;padding:16px;font:17px/1.6 sans-serif;background:#f4f6f8}header,section{background:white;border:1px solid #ccd3dc;padding:18px;margin-bottom:20px}img{display:block;max-width:100%;height:auto}summary{cursor:pointer;padding:10px;background:#edf2f7;margin-top:8px}a{color:#075cad}.warn{color:#a12121}</style>
<header><h1>下载检查通过；场景不满足A/C主训练要求</h1><p>71张原图与相机标签配对、解码、CRC和坐标边界检查通过。画面均为同一复杂大路口、含白天和较暗画面；只能保留D压力候选，不能补齐A/C主域。</p><p class="warn">本页仅8张AI补画代表图，不是71张全部标完。青色ai编号是AI草稿；绿色o编号是来源参考；橙色t编号是教师提示，包含明显误检。不确定项保留待定，未自动设ignore。没有人工签署、没有新审核任务、没有启动训练。</p><p>默认只显示AI新增框，展开无框原图/来源/教师可对照；点击图片打开原始尺寸。合并草稿不画原有骑行合框，以免与新拆框叠加；原始标签并未删除。不存在置信度、P/R或完整GT通过声明。</p><p>新增统计：COUNTS。<a href="ai_additions.json">AI补画坐标JSON</a> · <a href="inspection.json">下载和配对检查记录</a> · <a href="检查结论与后续.txt">检查结论</a></p></header>'''
    with (OUT/'index.html').open('x',encoding='utf-8') as stream:
        stream.write(page.replace('COUNTS',html.escape(str(dict(counts))))+''.join(cards)+'</html>')
    print('AI unsigned additions:',dict(counts),'8 images;D only,not training-ready',flush=True)


def check():
    assert box_values({'2d_box': dict(xmin='0', ymin='1', xmax='2', ymax='3')}, 4, 4)==[0,1,2,3]
    for values in ((0,0,0,1), (0,0,5,1), (0,0,float('nan'),1)):
        try:
            box_values({'2d_box': dict(zip(('xmin','ymin','xmax','ymax'),values))},4,4)
        except ValueError:
            pass
        else:
            raise AssertionError('invalid box accepted')
    try:
        member('../bad.jpg','image')
    except ValueError:
        pass
    else:
        raise AssertionError('unsafe ZIP member accepted')
    receipt = read_json(OUT/'inspection.json')
    assert sha256_file(ARCHIVE)==receipt['archive_sha256']
    for name, digest in receipt['protected'].items():
        assert sha256_file(Path(name))==digest, name
    assert receipt['human_workload_cap']==32 and receipt['new_human_assignments']==0
    assert not any(receipt[k] for k in ('training_started','G_ready','dataset_frozen','GPU_used'))
    for s in receipt['samples']:
        assert sha256_file(OUT/s['raw_file'])==s['image_sha256']
    if (OUT/'preview_receipt.json').exists():
        import numpy as np
        from .dataset import _letterbox_720
        from .integer import resize_area
        for s,p in zip(receipt['samples'],read_json(OUT/'preview_receipt.json')['records'],strict=True):
            with Image.open(OUT/s['raw_file']) as image:
                rgb720,_=_letterbox_720(np.array(image.convert('RGB')))
            with Image.open(OUT/s['image_id']/'input_preview.png') as image:
                assert np.array_equal(np.array(image),resize_area(rgb720))
            assert sha256_file(OUT/s['image_id']/'input_preview.png')==p['preview_sha256']
    if (OUT/'ai_additions.json').exists():
        result=read_json(OUT/'ai_additions.json')
        edits=read_json(OUT/'assistant_edits.json')
        assert sha256_file(OUT/'assistant_edits.json')==result['ai_edits_sha256']
        assert sha256_file(OUT/'teacher_hints.json')==result['teacher_hints_sha256']
        actual=Counter()
        for sample,row in zip(receipt['samples'],result['images'],strict=True):
            assert sample['image_id']==row['image_id']
            assert row['scene']=='D' and row['split']=='quarantine'
            for value in edits['images'][row['image_id']]['add']:
                validate_addition(value,sample)
            actual.update(a['class'] for a in row['additions'])
            assert not any(row[k] for k in ('complete','human_verified','training_eligible'))
        assert dict(actual)==result['AI_added_box_counts']
        assert dict(actual)=={'person':20,'vehicle':24}
        assert result['source_gate'].startswith('not_A_C_main_domain')
        assert result['human_workload_cap']==32 and result['new_human_assignments']==0
        assert not any(result[k] for k in ('complete_GT','dataset_frozen','G_ready','training_started','human_verified'))
        from html.parser import HTMLParser
        class Links(HTMLParser):
            def handle_starttag(self,tag,attrs):
                for key,value in attrs:
                    if key in ('href','src'):
                        assert (OUT/value).is_file(),value
        Links().feed((OUT/'index.html').read_text(encoding='utf-8'))
        bad=['person',[0,0,1,1],'nonexistent','test']
        try:
            validate_addition(bad,receipt['samples'][0])
        except ValueError:
            pass
        else:
            raise AssertionError('unknown target ID accepted')
    print('PASS source bindings,negative box/path checks,protected labels,scope and unsigned status',flush=True)


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('build','hints','details','previews','draft','check'))
    {'build':build,'hints':hints,'details':details,'previews':previews,'draft':draft,'check':check}[parser.parse_args().action]()
