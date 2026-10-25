"""One bounded replacement proposal; never exports GT or launches training."""
from collections import Counter
from copy import deepcopy
from html import escape
from pathlib import Path
import sys
import zipfile

from PIL import Image, ImageDraw

from cnn.prepare_ac_next8 import SourceRanges, URL
from cnn.prepare_ac_correction import isolated
from cnn.prepare_ground48 import ROOT, read_json, sha256_file, write_json
from cnn.import_verified_review import _box

OUT = Path(__file__).resolve().parent
OLD = ROOT / 'cnn/data/pets_ac_pilot_20261010'
CLOSURE = ROOT / 'cnn/reports/ac_label_closure_20261013_v1/closure_manifest_v2.json'
SOURCE = OUT / 'pets_source_attempt2'
# Fixed before inference: spread over the sequence, not picked by detection scores.
PETS = (40, 100, 170, 240, 310, 380, 450, 520, 590, 660, 730, 790)
VIRAT = (46, 93, 139, 186, 233, 256, 326, 373, 419, 466, 489, 536)


def fetch():
    receipt = read_json(OLD / 'receipt.json')
    for entry in receipt['members']:
        assert sha256_file(Path(entry['path'])) == entry['sha256']
    destination = SOURCE
    destination.mkdir(exist_ok=False)
    remote = SourceRanges()
    remote.etag = receipt['etag']
    members = []
    try:
        with zipfile.ZipFile(remote) as archive:
            for frame in PETS:
                if frame == 100:
                    continue  # Reuse the already verified JPEG, not another download.
                name = f'MOT15/train/PETS09-S2L1/img1/{frame:06d}.jpg'
                entry = archive.getinfo(name)
                assert 0 < entry.file_size <= 2 * 1024**2
                data = archive.read(entry)  # ZIP verifies member CRC.
                path = destination / f'{frame:06d}.jpg'
                with path.open('xb') as stream:
                    stream.write(data)
                members.append(dict(member=name, path=str(path), bytes=len(data),
                                    crc32=entry.CRC, sha256=sha256_file(path)))
                print('Downloaded PETS', frame, flush=True)
    finally:
        write_json(destination / 'receipt.json', dict(url=URL, etag=remote.etag,
            ranges=remote.receipts, payload_bytes=remote.total, members=members,
            complete=len(members) == 11, full_archive_downloaded=False,
            original_receipt_sha256=sha256_file(OLD/'receipt.json'),
            permitted_members='MOT15/train/PETS09-S2L1 only',
            license_note=receipt['license_note'], formal_test=False))


def build():
    assert not (OUT/'proposal.json').exists(), 'Preserve earlier proposal'
    closure = read_json(CLOSURE)
    receipt = read_json(SOURCE/'receipt.json')
    assert receipt['complete'] and len(receipt['members']) == 11
    bindings = {str(p): sha256_file(p) for p in
                (CLOSURE, OLD/'gt.txt', OLD/'receipt.json', SOURCE/'receipt.json')}
    for entry in receipt['members']:
        assert sha256_file(Path(entry['path'])) == entry['sha256']
        bindings[entry['path']] = entry['sha256']
    rows = []
    for frame in VIRAT:
        name = f'VIRAT_S_010204_05_000856_000890_f{frame:07d}'
        sample = deepcopy(next(s for s in closure['images'] if s['image_id'] == name))
        assert not sample['holds'] and not sample['human_signature_valid']
        sample['proposal_note'] = '现存AI草稿；无登记待定不等于标全。远端人物、重复框和遮挡仍须整图检查。'
        sample['provenance_kind'] = 'existing_unsigned_source_plus_AI_draft'
        rows.append(sample)
    source_rows = [list(map(float, line.split(','))) for line in
                   (OLD/'gt.txt').read_text(encoding='utf-8').splitlines()]
    for frame in PETS:
        path = (OLD if frame == 100 else SOURCE) / f'{frame:06d}.jpg'
        labels = []
        for number, values in enumerate(source_rows, 1):
            if int(values[0]) != frame:
                continue
            assert len(values) == 10 and values[6] in (0, 1)
            x, y, w, h = values[2:6]
            labels.append(dict(target_id=f'p{int(values[1])}', **{'class': 'person'},
                bbox=[x-1, y-1, x-1+w, y-1+h],
                source_row=number, source_values=values, source_track_id=int(values[1]),
                source_confidence=int(values[6]), needs_review=values[6] == 0))
        rows.append(dict(image_id=f'pets09_s2l1_f{frame:06d}', split='dev', scene='A',
            family_id='PETS09-S2L1-all-views', camera_id='PETS09-S2L1-view1',
            raw_file_absolute=str(path), source_sha256=sha256_file(path),
            width=768, height=576, labels=labels, human_signature_valid=False,
            frame_1based=frame, source_url='https://motchallenge.net/data/MOT15/',
            proposal_note='绿色为官方person参考；黄色为原confidence=0待定框，不能直接作正例或擅设ignore。车辆未包含，需AI逐图补查；不是完整GT。',
            provenance_kind='official_person_reference_not_two_class_GT'))
    retained = [s for s in closure['images'] if s['disposition'] == 'review_preserved_candidate_not_G_ready']
    summary = dict(schema='bounded_AC_replacement_proposal_v1', images=rows,
        retained_reviewed_ids=[s['image_id'] for s in retained],
        retained_counts=dict(Counter(s['split'] for s in retained)),
        proposed_additional_human_review_cap=24, additional_assignment_activated=False,
        maximum_combined_candidate_images=39, proposed_train=22, proposed_dev=17,
        proposed_diagnostic_updates=10, scope_change_requires_confirmation=True,
        source_bindings=bindings, original_scope_128_64_replaced=False,
        purpose='Concrete scope proposal; tiny supervised diagnostic only if approved and GT passes',
        dataset_frozen=False, G_ready=False, training_started=False,
        caveats=['Only one short VIRAT clip and one PETS camera supply new person images.',
                 'PETS has 19 unique tracks in the complete sequence; frames are correlated.',
                 'This is not the original 128/64 or formal P95/R85 experiment.',
                 'Historical E7 exposure/camera isolation must be checked before comparison.',
                 'Rejected candidates consume the cap; no automatic replacement or extra review.'])
    (OUT/'previews').mkdir(exist_ok=False)
    cards = []
    for i, sample in enumerate(rows, 1):
        image = Image.open(sample['raw_file_absolute']).convert('RGB')
        d = ImageDraw.Draw(image)
        for label in sample['labels']:
            _box(label['bbox'], sample['width'], sample['height'], sample['image_id'])
            d.rectangle(label['bbox'], outline='#ffba00' if label.get('needs_review') else '#00dd66', width=2)
            d.text(label['bbox'][:2], label['target_id'], fill='white', stroke_width=1, stroke_fill='black')
        image.thumbnail((960, 720))
        image.save(OUT/'previews'/f'{i:02d}.jpg', quality=90)
        raw_url = Path(sample['raw_file_absolute']).as_uri()
        cards.append(f'<article><h2>{i:02d} · {sample["split"]} · {escape(sample["image_id"])}</h2>'
            f'<p>{escape(sample["proposal_note"])}</p><p>{len(sample["labels"])}个参考框，不是新GT。</p>'
            f'<img loading="lazy" src="previews/{i:02d}.jpg" alt="来源或AI参考框">'
            f'<details><summary>查看无框完整原图</summary><img loading="lazy" src="{raw_url}" alt="完整原图"></details></article>')
    write_json(OUT/'proposal.json', summary)
    with (OUT/'index.html').open('x', encoding='utf-8') as stream:
        stream.write('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>A/C一次性替换范围</title>'
            '<style>body{font-family:system-ui;max-width:1060px;margin:24px auto;padding:0 18px;line-height:1.6}img{max-width:100%}article{border-top:1px solid #999;padding:12px 0}summary{cursor:pointer}</style>'
            '<h1>A/C一次性替换范围：待确认方案</h1><p>不要求现在逐图签署。这是统一候选与数量说明，不是已完成补标的审核台。</p>'
            '<p>保留已有10张训练、5张开发审核记录；拟新增12张VIRAT训练、12张PETS开发，最多24张新增审核（剔除也计入，不自动替换）。合计最多22训练／17开发。</p>'
            '<p>这是极小规模诊断建议，不冒充原128／64实验。新行人素材各只有一个机位，邻帧和重复轨迹不是独立目标。原计划未改、尚未启动训练。</p>'
            '<p>同意具体数量及用途后：AI先逐图补查 → 一次交付最多24张审核台 → 通过后冻结实际数量 → 测E7 → 再按小样本用途决定G100。不通过不追加审核。</p>'
            '<p>官方来源：<a href="https://motchallenge.net/data/MOT15/">MOT15 / PETS09-S2L1</a>；PETS全家族仅开发、VIRAT0102xx全家族仅训练。</p>'
            + ''.join(cards) + '</html>')
    check()


def check():
    m = read_json(OUT/'proposal.json')
    rows = m['images']
    assert len(rows) == len({s['image_id'] for s in rows}) == len({s['source_sha256'] for s in rows}) == 24
    assert Counter(s['split'] for s in rows) == {'train':12, 'dev':12}
    assert m['retained_counts'] == {'train':10, 'dev':5}
    assert not set(m['retained_reviewed_ids']) & {s['image_id'] for s in rows}
    isolated(rows)
    bad = deepcopy(rows)
    bad[0]['split'] = 'dev'
    try:
        isolated(bad)
    except ValueError:
        pass
    else:
        raise AssertionError('Same-family train/dev leakage accepted')
    for path, digest in m['source_bindings'].items():
        assert sha256_file(Path(path)) == digest, path
    for i, sample in enumerate(rows, 1):
        path = Path(sample['raw_file_absolute'])
        assert sha256_file(path) == sample['source_sha256']
        with Image.open(path) as image:
            assert image.size == (sample['width'], sample['height'])
        for label in sample['labels']:
            _box(label['bbox'], sample['width'], sample['height'], sample['image_id'])
        assert (OUT/'previews'/f'{i:02d}.jpg').is_file()
        assert not sample['human_signature_valid']
    assert not any(m[k] for k in ('dataset_frozen','G_ready','training_started','additional_assignment_activated'))
    assert m['proposed_diagnostic_updates'] == 10 and m['scope_change_requires_confirmation']
    assert sum(bool(a.get('needs_review')) for s in rows for a in s['labels']) == 3
    print('PASS24 proposal identities/hashes/boxes/family separation; retained15 untouched; no GT/training')


if __name__ == '__main__':
    assert sys.argv[1:] in (['fetch'], ['build'], ['check'])
    globals()[sys.argv[1]]()
