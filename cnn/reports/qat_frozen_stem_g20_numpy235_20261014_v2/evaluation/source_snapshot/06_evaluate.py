"""Evaluate a local trusted checkpoint on validation only; never opens newtest.

Float CNN + frozen fixed-point decoder is a diagnostic baseline, NOT INT8 CNN.
Output is exclusive-created to preserve prior evidence.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import time

import numpy as np
import torch

from .integer import postprocess
from .dataset import audit
from .metrics import evaluate, report, select_thresholds
from .model import RoadYOLOS4
from .train import (SHA256_RE, FullFrameDataset, dataset_content_hash,
                    load_dataset_manifest, reject_cache_qa, sha256)


def load_validation_subset(path, expected_content_hash, count):
    """Caller binds the original manifest SHA; rehash only selected raw val images.

    Declared raw hashes must reproduce the checkpoint's training content identity.
    Unselected image bytes are NOT reverified, and this is never full validation.
    """
    payload = json.loads(path.read_text(encoding='utf-8'))
    reject_cache_qa(payload)
    if count <= 0 or payload.get('training_eligible') is not True:
        raise ValueError('positive diagnostic count and eligible dataset required')
    if audit(payload)['incomplete_frames']:
        raise ValueError('incomplete diagnostic frame')
    declared, scenes = [], {}
    for row in payload['images']:
        if (row['split'] not in ('train', 'val') or not row['scene_id']
                or not row.get('preprocess', {}).get('raw_image')
                or not SHA256_RE.fullmatch(row['source_sha256'])):
            raise ValueError('subset mode requires development-only raw images with hashes')
        previous = scenes.setdefault(row['scene_id'], row['split'])
        if previous != row['split']:
            raise ValueError('scene leaks across train/val')
        declared.append(dict(image=row['image'], image_sha256=row['source_sha256']))
    if expected_content_hash is not None and dataset_content_hash(declared) != expected_content_hash:
        raise ValueError('declared raw content identity differs from checkpoint')
    candidates = sorted((row for row in payload['images'] if row['split'] == 'val'),
                        key=lambda row: row['image'])
    if not candidates:
        raise ValueError('no validation images')
    # Fixed even spacing over image names; no selection by labels or predictions.
    size = min(count, len(candidates))
    selected = []
    for index in range(size):
        row = dict(candidates[index * len(candidates) // size])
        image = Path(row['image'])
        row['image_path'] = image if image.is_absolute() else path.parent / image
        row['image_sha256'] = sha256(row['image_path'])
        if row['image_sha256'] != row['source_sha256']:
            raise ValueError('selected raw image differs from source hash')
        row['teacher_key'] = str(row.get('teacher_key', row['image'])).replace('\\', '/')
        selected.append(row)
    return selected, len(candidates)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checkpoint', type=Path, required=True)
    parser.add_argument('--dataset', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--device', default='cuda')
    parser.add_argument('--max-images', type=int, default=0,
                        help='raw-only fixed validation subset; diagnostic, not full validation')
    parser.add_argument('--threads', type=int, default=4, help='CPU inference threads')
    parser.add_argument('--development-domain', action='store_true',
                        help='explicit raw development-domain diagnostic; not a training-data match')
    args = parser.parse_args()
    if args.max_images < 0 or args.threads < 1:
        raise ValueError('invalid diagnostic image/thread count')
    if args.development_domain and not args.max_images:
        raise ValueError('development-domain diagnostic requires explicit raw image count')
    torch.set_num_threads(args.threads)
    started = time.perf_counter()
    if args.output.exists():
        raise FileExistsError(args.output)
    # Checkpoints contain RNG state; pickle loading is only for our local artifacts.
    checkpoint = torch.load(args.checkpoint, map_location='cpu', weights_only=False)
    model = RoadYOLOS4()
    if checkpoint['architecture_hash'] != model.architecture_hash():
        raise ValueError('checkpoint architecture mismatch')
    evaluation_dataset_hash = sha256(args.dataset)
    if not args.development_domain and checkpoint['dataset_sha256'] != evaluation_dataset_hash:
        raise ValueError('checkpoint dataset hash mismatch')
    model.load_state_dict(checkpoint['model'])
    model.to(args.device).eval()
    if args.max_images:
        rows, total_val_images = load_validation_subset(
            args.dataset, None if args.development_domain else
            checkpoint['dataset_content_sha256'], args.max_images)
        content_hash = None if args.development_domain else checkpoint['dataset_content_sha256']
        verification_scope = 'selected_raw_val_bytes_only; other_hashes_manifest_declared'
    else:
        _, rows = load_dataset_manifest(args.dataset)
        content_hash = dataset_content_hash(rows)
        if checkpoint.get('dataset_content_sha256') != content_hash:
            raise ValueError('checkpoint image-content hash absent or mismatched; retrain diagnostic')
        total_val_images = sum(row['split'] == 'val' for row in rows)
        verification_scope = 'all_manifest_image_bytes'
    dataset = FullFrameDataset(rows, 'val')
    timings = {name: [] for name in ('preprocess', 'forward', 'postprocess')}
    startup_seconds = time.perf_counter() - started
    predictions, truth, ignores = [], [], []
    with torch.inference_mode():
        for index, row in enumerate(dataset.rows):
            stage = time.perf_counter()
            image, _, _ = dataset[index]
            device_image = image.unsqueeze(0).to(args.device)
            if args.device.startswith('cuda'):
                torch.cuda.synchronize()
            timings['preprocess'].append(time.perf_counter() - stage)
            stage = time.perf_counter()
            outputs = model(device_image)
            if args.device.startswith('cuda'):
                torch.cuda.synchronize()
            timings['forward'].append(time.perf_counter() - stage)
            stage = time.perf_counter()
            heads = [np.clip(np.rint(output[0].permute(1, 2, 0).cpu().numpy() * 256),
                             -32768, 32767).astype(np.int16) for output in outputs]
            # Retain every score admitted by validation scan (>=0.05).
            detections = postprocess(heads, (3276, 3276))
            timings['postprocess'].append(time.perf_counter() - stage)
            predictions.extend(dict(image_id=row['image'], label=det['label'],
                                    box=[value / 256 for value in det['box_q8']],
                                    score=det['score_uint16'] / 65536)
                               for det in detections)
            truth.extend(dict(image_id=row['image'], label=label, box=box)
                         for label, box in zip(row['labels'], row['boxes'], strict=True))
            metadata = row.get('ignore_metadata',
                               [{'label': -1, 'crowd': False}] * len(row['ignore_boxes']))
            ignores.extend(dict(image_id=row['image'], label=region['label'], box=box,
                                crowd=region['crowd'])
                           for box, region in zip(row['ignore_boxes'], metadata, strict=True))
            if index == 0 or (index + 1) % 32 == 0 or index + 1 == len(dataset):
                print(f'validation {index + 1}/{len(dataset)}', flush=True)
    metric_started = time.perf_counter()
    thresholds = select_thresholds(predictions, truth, ignores)
    result = (report(predictions, truth, ignores, thresholds=thresholds)
              if all(value is not None for value in thresholds) else None)
    diagnostic = report(predictions, truth, ignores, thresholds=(.5, .5))
    p95_points = {name: (evaluate(predictions, truth, ignores, label=label,
                                 threshold=thresholds[label])
                         if thresholds[label] is not None else None)
                  for label, name in enumerate(('person', 'vehicle'))}
    output = dict(status='diagnostic_not_formal_acceptance',
                  inference='FP32_CNN_plus_Q7_8_fixed_point_postprocess_not_INT8_CNN',
                  checkpoint_sha256=sha256(args.checkpoint), dataset_sha256=evaluation_dataset_hash,
                  dataset_content_sha256=content_hash,
                  training_dataset_sha256=checkpoint['dataset_sha256'],
                  training_dataset_content_sha256=checkpoint['dataset_content_sha256'],
                  development_domain_diagnostic=args.development_domain,
                  architecture_hash=model.architecture_hash(), split='val',
                  image_count=len(dataset), total_validation_images=total_val_images,
                  validation_subset=len(dataset) < total_val_images,
                  subset_selection=('evenly_spaced_sorted_image_names'
                                    if len(dataset) < total_val_images else None),
                  image_verification_scope=verification_scope,
                  evaluated_image_content_sha256=dataset_content_hash(dataset.rows),
                  checkpoint_epoch_number=checkpoint['epoch'] + 1,
                  checkpoint_optimizer_steps=checkpoint['trained_steps'],
                  device=args.device, cpu_threads=args.threads,
                  postprocess_contract=dict(top_k_per_class=128, max_boxes_per_class=32,
                                            nms_iou=.5, score_floor_uint16=3276),
                  validation_thresholds=thresholds, p95_operating_points=p95_points,
                  diagnostic_metrics_at_0_5=diagnostic,
                  metrics=result, predictions=predictions, truth=truth, ignores=ignores,
                  baseline_at_0_5={name: evaluate(predictions, truth, ignores, label=label,
                                                 threshold=.5)
                                     for label, name in enumerate(('person', 'vehicle'))},
                  limitation=('AP score floor approximately0.05; per-class Top128/max32; '
                              'legacy ignore defaults wildcard IoU; no cluster CI or newtest run; '
                              'not COCOeval' +
                              ('; subset is nonrandom sorted-name systematic sampling '
                               'floor(i*N/K), not endpoint-symmetric or a formal representative sample'
                               if len(dataset) < total_val_images else '')),
                  acceptance_eligible=False)
    output['timing_seconds'] = {
        'startup': startup_seconds, 'metrics': time.perf_counter() - metric_started,
        'total': time.perf_counter() - started,
        'per_image': {name: dict(mean=float(np.mean(values)),
                                p95=float(np.percentile(values, 95)), total=sum(values))
                      for name, values in timings.items()},
        'scope': 'host diagnostic inference; not training throughput or FPGA FPS',
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x', encoding='utf-8') as stream:
        json.dump(output, stream, ensure_ascii=False, indent=2)
    print(json.dumps(dict(thresholds=thresholds, metrics=diagnostic,
                          timing_seconds=output['timing_seconds']), ensure_ascii=False))


if __name__ == '__main__':
    main()
