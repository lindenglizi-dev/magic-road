"""CPU first-batch input/loss/gradient equivalence; never updates saved weights.

QA manifests are explicitly allowed here ONLY for pipeline checks. The actual
trainer and accuracy evaluator reject them. No optimizer, AMP, or GPU is used.
"""
import argparse
import json
from pathlib import Path

import torch
from torch.utils.data import DataLoader

from .disk_cache import assert_item_equal, build_cache
from .loss import YOLOXLoss
from .model import RoadYOLOS4
from .train import (CLASS_CONTRACT, build_parser, collate, ensure_resume_eligible,
                    load_dataset_manifest, make_frame_dataset, protocol_for,
                    protocol_hash, sha256)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dataset', type=Path, required=True)
    parser.add_argument('--checkpoint', type=Path, required=True)
    parser.add_argument('--cache-dir', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    declared = json.loads(args.dataset.read_text(encoding='utf-8'))
    if len(declared['images']) > 128 or any(
            row['split'] not in ('train', 'val') for row in declared['images']):
        raise ValueError('only a bounded development pipeline check is allowed')
    torch.set_num_threads(2)
    torch.use_deterministic_algorithms(True)
    checkpoint_hash = sha256(args.checkpoint)
    checkpoint = torch.load(args.checkpoint, map_location='cpu', weights_only=False)
    model = RoadYOLOS4().cpu()
    if (checkpoint['architecture_hash'] != model.architecture_hash()
            or checkpoint['class_contract'] != CLASS_CONTRACT):
        raise ValueError('checkpoint architecture/class mismatch')
    # This checks the existing 300-epoch contract without changing its schedule.
    original_args = build_parser().parse_args(['--dataset', str(args.dataset),
                                             '--output', 'unused_no_training'])
    original_protocol = protocol_for(original_args,
                                    checkpoint['training_protocol']['optimizer_steps_per_epoch'], None)
    ensure_resume_eligible(checkpoint, original_protocol)
    _, rows = load_dataset_manifest(args.dataset, allow_cache_qa=True)
    cache = build_cache(args.dataset, rows, args.cache_dir)
    receipt = sha256(args.cache_dir / 'index.json')
    results = []
    for mosaic in (False, True):
        datasets = [make_frame_dataset(rows, 'train', args.dataset, mosaic=mosaic),
                    make_frame_dataset(rows, 'train', args.dataset, mosaic=mosaic,
                                       cache_root=args.cache_dir, cache_index_sha256=receipt)]
        batches = []
        for data in datasets:
            data.set_epoch(6, mosaic)
            loader = DataLoader(data, batch_size=2, shuffle=True, num_workers=0,
                                generator=torch.Generator().manual_seed(48), collate_fn=collate)
            batches.append(next(iter(loader)))
        for index in range(2):
            assert_item_equal((batches[0][0][index], batches[0][1][index], batches[0][2][index]),
                              (batches[1][0][index], batches[1][1][index], batches[1][2][index]))
        snapshots = []
        for images, targets, _keys in batches:
            model.load_state_dict(checkpoint['model'], strict=True)
            model.train()  # BN updates only this disposable in-memory copy.
            model.zero_grad(set_to_none=True)
            heads = model(images)
            values = YOLOXLoss()(heads, targets)
            if not all(torch.isfinite(value).all() for value in values.values()):
                raise FloatingPointError('non-finite CPU diagnostic loss')
            values['loss'].backward()
            gradients = {name: parameter.grad.detach().clone()
                         for name, parameter in model.named_parameters() if parameter.grad is not None}
            if not gradients or not all(torch.isfinite(value).all() for value in gradients.values()):
                raise FloatingPointError('non-finite CPU diagnostic gradients')
            snapshots.append(dict(losses={key: value.detach().clone() for key, value in values.items()},
                                  heads=[head.detach().clone() for head in heads], gradients=gradients,
                                  state={key: value.detach().clone()
                                         for key, value in model.state_dict().items()}))
        left, right = snapshots
        if left['gradients'].keys() != right['gradients'].keys():
            raise AssertionError('gradient parameter sets differ')
        for field in ('losses', 'gradients', 'state'):
            for key in left[field]:
                torch.testing.assert_close(left[field][key], right[field][key], rtol=0, atol=0)
        for left_head, right_head in zip(left['heads'], right['heads'], strict=True):
            torch.testing.assert_close(left_head, right_head, rtol=0, atol=0)
        results.append(dict(mosaic=mosaic, microbatch=2, shuffled_keys=batches[0][2],
                            losses={key: float(value) for key, value in left['losses'].items()},
                            compared_gradient_tensors=len(left['gradients']),
                            max_input_head_loss_gradient_and_BN_difference=0))
    if sha256(args.checkpoint) != checkpoint_hash:
        raise ValueError('saved checkpoint changed during diagnostic')
    result = dict(status='passed_CPU_first_batch_loss_gradient_equivalence_not_accuracy',
                  device='cpu', cpu_threads=2, amp=False, gpu_used=False, optimizer_steps=0,
                  saved_weights_modified=False, training_resumed=False,
                  checkpoint_sha256=checkpoint_hash, checkpoint_epoch=checkpoint['epoch'] + 1,
                  dataset_sha256=sha256(args.dataset), cache_index_sha256=receipt,
                  cache_bytes=cache['rgb_bytes'], original_protocol_sha256=protocol_hash(original_protocol),
                  original_protocol_resume_eligible=True, results=results,
                  source_sha256={name: sha256(Path(__file__).parent / name)
                                 for name in ('check_cache_training.py', 'train.py', 'disk_cache.py', 'evaluate.py')},
                  limitation='Two FP32 CPU microbatches of2, Mosaic off/on, forward/backward only. '
                             'No optimizer update, GPU AMP, full-batch accumulation, training speed, '
                             'accuracy result, or full road cache. QA data cannot enter the actual trainer.')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x', encoding='utf-8') as stream:
        json.dump(result, stream, indent=2)
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    main()
