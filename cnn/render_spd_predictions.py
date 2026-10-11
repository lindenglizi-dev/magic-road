"""Show all saved SPD8 detections, without relabeling, retraining or cherry-picking."""
import argparse
import html
import json
from pathlib import Path

from PIL import Image, ImageDraw

from .metrics import evaluate
from .train import sha256


def overlay(raw, records, title, predictions=False, threshold=0.):
    image = raw.resize((1024, 576))
    draw = ImageDraw.Draw(image)
    for row in records:
        if predictions and row['score'] < threshold:
            continue
        color = ('#ff4b4b' if row['label'] == 0 else '#00cfff') if predictions else '#60ff60'
        coords = [v*2 for v in row['box']]
        draw.rectangle(coords, outline=color, width=2)
        text = ('P' if row['label'] == 0 else 'V') + (f' {row["score"]:.2f}' if predictions else ' GT')
        x, y = max(0, min(940, coords[0])), max(24, coords[1]-12)
        draw.text((x, y), text, fill=color, stroke_width=1, stroke_fill='black')
    draw.rectangle([0, 0, 1024, 24], fill='black')
    draw.text((6, 6), title, fill='white')
    return image


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--teacher', action='store_true')
    args = parser.parse_args()
    name = 'Teacher' if args.teacher else 'E7'
    root = Path(__file__).resolve().parent.parent
    folder = root/'cnn/reports/spd_val8_e7_20261009_v3'
    evaluation_path = folder/('teacher_evaluation.json' if args.teacher else 'e7_evaluation.json')
    manifest_path = folder/'spd_val8.json'
    evaluation = json.loads(evaluation_path.read_text(encoding='utf-8'))
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    assert sha256(manifest_path) == evaluation['dataset_sha256']
    if args.teacher:
        student = json.loads((folder/'e7_evaluation.json').read_text(encoding='utf-8'))
        assert all(student[key] == evaluation[key] for key in (
            'truth', 'ignores', 'dataset_sha256', 'evaluated_image_content_sha256', 'postprocess_contract'))
    protected = {p: sha256(p) for p in (evaluation_path, manifest_path)}
    for label, class_name in enumerate(('person', 'vehicle')):
        result = evaluate(evaluation['predictions'], evaluation['truth'], label=label, threshold=.5)
        assert all(result[key] == evaluation['baseline_at_0_5'][class_name][key] for key in ('tp', 'fp', 'fn'))
    output = folder/('teacher_prediction_views_v2' if args.teacher else 'prediction_views')
    output.mkdir(exist_ok=False)
    cards, samples = [], []
    for source in manifest['images']:
        image_id = source['image']
        path = folder/image_id
        assert sha256(path) == source['source_sha256']
        protected[path] = sha256(path)
        with Image.open(path) as handle:
            raw = handle.convert('RGB')
        assert raw.size == (1920, 1080)  # no padding; raw->network is exactly 512/1920
        gt = [r for r in evaluation['truth'] if r['image_id'] == image_id]
        predictions = [r for r in evaluation['predictions'] if r['image_id'] == image_id]
        sid = Path(image_id).stem
        panels = [overlay(raw, gt, sid+' | Human GT: green'),
                  overlay(raw, predictions, sid+f' | {name} score>=0.50: P red, V cyan', True, .5)]
        paired = Image.new('RGB', (2048, 576))
        for index, panel in enumerate(panels):
            paired.paste(panel, (index*1024, 0))
        paired.save(output/(sid+'_compare.jpg'), quality=95)
        low = overlay(raw, predictions, sid+f' | {name} score>=0.10: diagnostic only', True, .1)
        low.save(output/(sid+'_score010.jpg'), quality=95)
        # A fixed central rider region in the first frame, not a best-scoring example.
        if sid == 'spd_inf_010721':
            crop = Image.new('RGB', (1200, 400))
            for index, panel in enumerate([*panels, low]):
                crop.paste(panel.crop((530, 220, 640, 320)).resize((400, 364)), (index*400, 36))
            draw = ImageDraw.Draw(crop)
            for index, title in enumerate(('Human GT', f'{name} score>=0.50', f'{name} score>=0.10')):
                draw.text((index*400+8, 12), title, fill='white')
            crop.save(output/'010721_central_rider.jpg', quality=95)
        local_metrics = {name: evaluate(predictions, gt, label=label, threshold=.5)
                         for label, name in enumerate(('person', 'vehicle'))}
        samples.append(dict(image_id=image_id, metrics=local_metrics))
        cards.append(f'<section><h2>{sid}</h2><p>{html.escape(str(local_metrics))}</p>'
            f'<img src="{sid}_compare.jpg"><details><summary>仅诊断：降低到0.10，显示全部保留预测</summary>'
            f'<img src="{sid}_score010.jpg"></details><a href="../{image_id}">无框原图</a></section>')
    (output/'index.html').write_text(f'<!doctype html><meta charset="utf-8"><title>{name}真实预测对照</title>'
        '<style>body{font-family:sans-serif;margin:24px}img{width:100%;max-width:2048px}section{margin:30px 0}p{overflow-wrap:anywhere}</style>'
        f'<h1>SPD8：人工GT与{name}真实预测</h1><p>每图左侧：绿色人工GT。右侧：score≥0.5预测，红色P为person，蓝色V为vehicle；颜色不代表正确或错误。'
        'P/V分别是人/车，数字为置信分数。全部8图均展示，不挑最佳图。低阈值只作诊断，不替换基线。</p>'
        '<p>本页只读，不需要再次审核或标框。o12按用户要求未加入GT，预测未获特殊忽略。</p>'+''.join(cards), encoding='utf-8')
    assert all(sha256(path) == digest for path, digest in protected.items())
    (output/'receipt.json').write_text(json.dumps(dict(image_count=len(samples), samples=samples,
        evaluation_sha256=protected[evaluation_path], dataset_sha256=protected[manifest_path],
        source_sha256=sha256(Path(__file__)), all_inputs_unchanged=True,
        labels_changed=False, training_started=False, selection='all eight images in dataset order',
        source=f'saved {name} predictions only; no generated detections'), indent=2), encoding='utf-8')
    print('PASS: saved metrics agree; rendered all 8 frames; input hashes unchanged')


if __name__ == '__main__':
    main()
