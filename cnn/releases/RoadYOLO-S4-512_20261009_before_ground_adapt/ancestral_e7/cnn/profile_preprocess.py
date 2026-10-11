"""CPU-only exact-input cache experiment; never trains or changes checkpoint weights."""
import argparse
import json
from pathlib import Path
import time
from unittest.mock import patch

import numpy as np
import torch

from .train import FullFrameDataset, load_dataset_manifest, sha256


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dataset', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    torch.set_num_threads(2)
    _, rows = load_dataset_manifest(args.dataset, allow_cache_qa=True)
    dataset = FullFrameDataset(rows, 'train', mosaic=True, seed=42)
    if len(dataset) > 128:
        raise ValueError('use the audited pilot only; this experiment caps cache at128 images')
    dataset.set_epoch(6)
    start = time.perf_counter()
    cached = [dataset._load(index) for index in range(len(dataset))]
    construction = time.perf_counter() - start
    indexes = list(range(min(16, len(dataset))))
    timings = {}
    for name in ('raw', 'cached'):
        trials = []
        context = patch.object(dataset, '_load', side_effect=lambda index: cached[index])
        if name == 'cached':
            context.start()
        try:
            for _ in range(3):
                start = time.perf_counter()
                actual = [dataset[index] for index in indexes]
                trials.append(time.perf_counter() - start)
            if name == 'raw':
                baseline = actual
            else:
                for original, candidate in zip(baseline, actual, strict=True):
                    torch.testing.assert_close(original[0], candidate[0], rtol=0, atol=0)
                    for field in ('boxes', 'labels', 'ignore_boxes'):
                        torch.testing.assert_close(original[1][field], candidate[1][field],
                                                   rtol=0, atol=0)
                    assert original[2] == candidate[2]
        finally:
            if name == 'cached':
                context.stop()
        timings[name] = dict(trials_seconds=trials,
                             median_seconds_per_mosaic=float(np.median(trials)) / len(indexes))
    result = dict(status='passed_exact_mosaic_inputs_not_training_speed_evidence',
                  dataset_sha256=sha256(args.dataset), source_sha256=sha256(Path(__file__)),
                  device='cpu', gpu_used=False, training_started=False,
                  cached_source_images=len(cached), tested_mosaics=len(indexes), repeats=3,
                  cached_rgb_bytes=sum(item[0].nbytes for item in cached),
                  cache_construction_seconds=construction,
                  timings=timings,
                  isolated_preprocess_speedup=(timings['raw']['median_seconds_per_mosaic'] /
                                              timings['cached']['median_seconds_per_mosaic']),
                  equivalence='all RGB-128 pixels, boxes, labels, ignore boxes and mosaic keys exact',
                  limitation='in-memory pilot cache; disk cache, full epoch speed and RAM replication '
                             'across Windows workers not measured; no cache added to production trainer')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x', encoding='utf-8') as handle:
        json.dump(result, handle, indent=2)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
