"""CPU-only read-only checkpoint replay; relaxed limits are NOT deployment metrics."""
import argparse
from collections import defaultdict
import json
from pathlib import Path

import numpy as np
import torch

from .integer import postprocess
from .loss import decode_outputs
from .metrics import evaluate
from .model import RoadYOLOS4
from .train import FullFrameDataset, sha256


def float_candidates(outputs, image_id, top_k, limit):
    boxes, objects, classes, _, _ = decode_outputs(outputs)
    boxes = boxes[0].numpy().clip([0, 0, 0, 0], [512, 288, 512, 288])
    scores = (objects.sigmoid().unsqueeze(-1) * classes.sigmoid())[0].numpy()
    records = []
    for label in (0, 1):
        order = np.lexsort((np.arange(len(boxes)), -scores[:, label]))
        order = order[scores[order, label] >= 3276 / 65536][:top_k]
        valid = (boxes[order, 2] > boxes[order, 0]) & (boxes[order, 3] > boxes[order, 1])
        order = order[valid]
        kept = []
        while len(order) and len(kept) < limit:
            index = order[0]
            kept.append(index)
            order = order[1:]
            left = np.maximum(boxes[order, :2], boxes[index, :2])
            right = np.minimum(boxes[order, 2:], boxes[index, 2:])
            intersection = np.maximum(0, right - left).prod(axis=1)
            union = ((boxes[order, 2:] - boxes[order, :2]).prod(axis=1)
                     + (boxes[index, 2:] - boxes[index, :2]).prod() - intersection)
            order = order[intersection / np.maximum(union, 1e-9) <= .5]
        records.extend(dict(image_id=image_id, label=label, box=boxes[index].tolist(),
                            score=float(scores[index, label])) for index in kept)
    return records


def self_check():
    heads = [torch.full((1, 7, 288 // s, 512 // s), -20.) for s in (4, 8, 16)]
    heads[0][0, :4, 10, 10] = torch.tensor([.5, .5, 0., 0.])
    heads[0][0, 4:, 10, 10] = 20.
    rows = float_candidates(heads, 'check', 128, 32)
    assert [row['label'] for row in rows] == [0, 1]
    assert rows[0]['box'] == [40., 40., 44., 44.]
    heads[0][0, :4, 10, 11] = torch.tensor([-.5, .5, 0., 0.])
    heads[0][0, 4:, 10, 11] = 20.
    assert len(float_candidates(heads, 'check', 128, 32)) == 2  # duplicate NMS
    heads[0][0, :4, 10, 20] = torch.tensor([.5, .5, 0., 0.])
    heads[0][0, 4:, 10, 20] = 20.
    assert len(float_candidates(heads, 'check', 128, 32)) == 4
    assert len(float_candidates(heads, 'check', 128, 1)) == 2


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checkpoint', type=Path, required=True)
    parser.add_argument('--evaluation', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    torch.set_num_threads(2)
    self_check()
    baseline = json.loads(args.evaluation.read_text(encoding='utf-8'))
    assert sha256(args.checkpoint) == baseline['checkpoint_sha256']
    checkpoint = torch.load(args.checkpoint, map_location='cpu', weights_only=False)
    model = RoadYOLOS4().eval()
    model.load_state_dict(checkpoint['model'])
    truths = defaultdict(list)
    for row in baseline['truth']:
        truths[row['image_id']].append(row)
    image_ids = sorted(set(row['image_id'] for row in baseline['predictions']) | set(truths))
    assert len(image_ids) == baseline['image_count']
    variants = {name: [] for name in ('integer_replay', 'float_128_32', 'float_1024_256')}
    image_hashes = []
    with torch.inference_mode():
        for index, image_id in enumerate(image_ids):
            path = Path(image_id)
            image_hashes.append(dict(image=image_id, sha256=sha256(path)))
            row = dict(image_path=path, preprocess={'raw_image': True}, boxes=[],
                       labels=[], ignore_boxes=[], teacher_key=image_id, split='val')
            image, _, _ = FullFrameDataset([row], 'val')[0]
            outputs = model(image.unsqueeze(0))
            heads = [np.clip(np.rint(head[0].permute(1, 2, 0).numpy() * 256),
                             -32768, 32767).astype(np.int16) for head in outputs]
            variants['integer_replay'].extend(dict(image_id=image_id, label=det['label'],
                box=[v / 256 for v in det['box_q8']], score=det['score_uint16'] / 65536)
                for det in postprocess(heads, (3276, 3276)))
            for name, top_k, limit in (('float_128_32', 128, 32), ('float_1024_256', 1024, 256)):
                variants[name].extend(float_candidates(outputs, image_id, top_k, limit))
            if index == 0 or (index + 1) % 32 == 0:
                print(f'CPU diagnosis {index + 1}/{len(image_ids)}', flush=True)
    def key(row):
        return row['image_id'], row['label'], row['score'], tuple(row['box'])
    assert sorted(map(key, variants['integer_replay'])) == sorted(map(key, baseline['predictions']))
    metrics = {name: {str((label, threshold)): evaluate(rows, baseline['truth'],
        baseline['ignores'], label=label, threshold=threshold)
        for label in (0, 1) for threshold in (0., .5)} for name, rows in variants.items()}
    result = dict(status='diagnostic_only_not_acceptance', checkpoint_sha256=sha256(args.checkpoint),
                  evaluation_sha256=sha256(args.evaluation), image_count=len(image_ids),
                  integer_replay_exact=True, metrics=metrics, image_hashes=image_hashes,
                  limit='CPU FP32 only; expanded candidates not FPGA contract; no training or changes')
    with args.output.open('x', encoding='utf-8') as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
    print(json.dumps({k: v for k, v in result.items() if k != 'image_hashes'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
