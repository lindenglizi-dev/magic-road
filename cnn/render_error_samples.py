"""Render fixed diagnostic examples; colors are evidence, not relabeling."""
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from .dataset import _refuse_blind
from .train import FullFrameDataset, sha256


def main():
    root = Path(__file__).resolve().parent.parent
    folder = root/'cnn/reports/error_diagnosis_20261006'
    analysis_path = folder/'saved_prediction_errors.json'
    evaluation_path = root/'cnn/reports/supervised5_oct5/epoch12_full_val.json'
    manifest_path = root/'cnn/data/visdrone_vid_train/raw_manifest/dataset.json'
    analysis = json.loads(analysis_path.read_text(encoding='utf-8'))
    evaluation = json.loads(evaluation_path.read_text(encoding='utf-8'))
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    assert sha256(evaluation_path) == analysis['input_sha256']['epoch12']
    assert sha256(manifest_path) == evaluation['dataset_sha256']
    rows = {row['image']: row for row in manifest['images'] if row['split'] == 'val'}
    output = folder/'error_samples'
    output.mkdir(exist_ok=False)
    receipt = []
    for key, example in analysis['reports']['epoch12']['examples'].items():
        if not any(reason in key for reason in ('no_retained_support', 'other_class_GT', 'localization_support', 'no_GT_support')):
            continue
        source = rows[example['image_id']]
        path = Path(source['image'])
        _refuse_blind(path)
        assert sha256(path) == source['source_sha256']
        row = {**source, 'image_path': path, 'teacher_key': source['image']}
        tensor, _, _ = FullFrameDataset([row], 'val')[0]
        array = (tensor.permute(1, 2, 0).numpy()+128).astype(np.uint8)
        image = Image.fromarray(array).resize((1024, 576), Image.Resampling.NEAREST)
        draw = ImageDraw.Draw(image)
        for target in evaluation['truth']:
            if target['image_id'] == example['image_id']:
                draw.rectangle([v*2 for v in target['box']], outline='lime', width=1)
        for prediction in evaluation['predictions']:
            if prediction['image_id'] == example['image_id'] and prediction['score'] >= .5:
                draw.rectangle([v*2 for v in prediction['box']], outline='red', width=1)
        draw.rectangle([v*2 for v in example['box']], outline='yellow', width=3)
        draw.text((4, 4), key, fill='yellow', stroke_width=1, stroke_fill='black')
        name = key.replace('/', '_')+'.png'
        image.save(output/name)
        receipt.append(dict(key=key, example=example, image_sha256=source['source_sha256'],
                            output=name, output_sha256=sha256(output/name)))
    with (output/'receipt.json').open('x', encoding='utf-8') as stream:
        json.dump(dict(samples=receipt, analysis_sha256=sha256(analysis_path),
                       renderer_sha256=sha256(Path(__file__)),
                       colors='GT green, predictions score>=0.5 red, selected example yellow',
                       labels_changed=False, limitation='fixed first example per category; not a representative annotation audit'), stream, indent=2)
    print('rendered', len(receipt), 'fixed error examples')


if __name__ == '__main__':
    main()
