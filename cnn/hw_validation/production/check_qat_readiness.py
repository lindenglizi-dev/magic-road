"""CPU detection-loss/backward/resume/export smoke; never an accuracy candidate."""
import argparse
import json
import time
from pathlib import Path

import numpy as np
import torch

from cnn.loss import YOLOXLoss
from cnn.model import RoadYOLOS4
from cnn.train import load_dataset_snapshot, make_frame_dataset, sha256
from cnn.hw_validation.production.qat_exact import QATExactModel
from cnn.hw_validation.production.run_trained_integer import (
    PROJECT, CHECKPOINT, CHECKPOINT_HASH, TRAIN, TRAIN_HASH, centered, save)
from cnn.hw_validation.production.trained_integer import load_package

BASE = PROJECT / 'cnn/reports/replay_g10_integer_20261013_v2'
MANIFEST_HASH = '64ad4e3284c4fdf90fa9f9ddc468db00159c46b152a13d440753030a979624f9'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    torch.set_num_threads(2)
    torch.manual_seed(42)
    for path, wanted in [(CHECKPOINT, CHECKPOINT_HASH), (TRAIN, TRAIN_HASH), (BASE / 'package/manifest.json', MANIFEST_HASH)]:
        if sha256(path) != wanted:
            raise ValueError('frozen input differs')
    source = RoadYOLOS4().eval()
    state = torch.load(CHECKPOINT, map_location='cpu', weights_only=False)
    source.load_state_dict(state['model'])
    folded = source.folded_conv_state()
    integer, manifest = load_package(BASE / 'package')
    _, snapshot = load_dataset_snapshot(TRAIN)
    if snapshot.dataset_content_sha256 != state['dataset_content_sha256']:
        raise ValueError('training content differs')
    dataset = make_frame_dataset(snapshot.rows, 'train', TRAIN, mosaic=False)
    image, target, key = dataset[0]
    qat = QATExactModel.from_package(BASE / 'package', folded, BASE / 'quantization.json')
    sample = image.unsqueeze(0)
    started = time.perf_counter()
    outputs, trace = qat(sample, capture=True)
    forward_seconds = time.perf_counter() - started
    heads, _, captures = integer.forward(centered(image), capture=True)
    checked_values = 0
    for name, actual in trace.items():
        scale = 1 / 256 if name.endswith(':pre') else integer.scales[name]
        recovered = torch.round(actual.detach() / scale).permute(0, 2, 3, 1).numpy()[0]
        np.testing.assert_array_equal(recovered, captures[name])
        checked_values += recovered.size
    for actual, expected in zip(outputs, heads, strict=True):
        np.testing.assert_array_equal((actual.detach()[0].permute(1, 2, 0) * 256).numpy(), expected)
    criterion = YOLOXLoss()
    started = time.perf_counter()
    losses = criterion(outputs, [target])
    if not all(torch.isfinite(value).all() for value in losses.values()):
        raise FloatingPointError('nonfinite real detection loss')
    losses['loss'].backward()
    gradients = [parameter.grad for parameter in qat.parameters() if parameter.requires_grad]
    if any(gradient is None or not torch.isfinite(gradient).all() for gradient in gradients):
        raise FloatingPointError('missing or nonfinite gradient')
    gradient_nonzero = sum(int(torch.count_nonzero(value)) for value in gradients)
    if not gradient_nonzero:
        raise AssertionError('STE did not propagate detection gradients')
    norm = torch.nn.utils.clip_grad_norm_(qat.parameters(), 10., error_if_nonfinite=True)
    optimizer = torch.optim.SGD(qat.parameters(), lr=1e-4, momentum=.9, weight_decay=5e-4)
    before = {name: value.detach().clone() for name, value in qat.named_parameters()}
    optimizer.step()
    backward_update_seconds = time.perf_counter() - started
    changed = sum(int(torch.count_nonzero(value.detach() != before[name])) for name, value in qat.named_parameters())
    if not changed or any(not torch.isfinite(value).all() for value in qat.parameters()):
        raise AssertionError('disposable update failed')
    # Diagnostic-only state: never use this one-image smoke as a candidate.
    state_path = args.output / 'disposable_smoke_state.pt'
    torch.save({'status': 'ONE_IMAGE_ONE_UPDATE_NUMERIC_SMOKE_NOT_TRAINING_CANDIDATE',
                'source_checkpoint_sha256': CHECKPOINT_HASH, 'source_manifest_sha256': MANIFEST_HASH,
                'model': qat.state_dict(), 'optimizer': optimizer.state_dict()}, state_path)
    restored = QATExactModel.from_package(BASE / 'package', folded, BASE / 'quantization.json')
    saved = torch.load(state_path, map_location='cpu', weights_only=True)
    restored.load_state_dict(saved['model'], strict=True)
    restored_optimizer = torch.optim.SGD(restored.parameters(), lr=1e-4, momentum=.9, weight_decay=5e-4)
    restored_optimizer.load_state_dict(saved['optimizer'])
    sources = [Path(__file__), Path(__file__).with_name('qat_exact.py'), Path(__file__).with_name('trained_integer.py'),
               PROJECT / 'cnn/loss.py', PROJECT / 'cnn/integer.py', PROJECT / 'cnn/train.py']
    exported = restored.export_package(args.output / 'disposable_package', {
        'purpose': 'ONE_IMAGE_ONE_UPDATE_NUMERIC_SMOKE_NOT_TRAINING_CANDIDATE',
        'checkpoint_sha256': CHECKPOINT_HASH, 'source_manifest_sha256': MANIFEST_HASH,
        'source_sha256': {str(path.relative_to(PROJECT)).replace('\\', '/'): sha256(path) for path in sources}})
    reread, _ = load_package(args.output / 'disposable_package')
    with torch.no_grad():
        new_outputs = qat(sample)
        restored_outputs = restored(sample)
    exported_heads, _, _ = reread.forward(centered(image))
    for actual, restored_value, expected in zip(new_outputs, restored_outputs, exported_heads, strict=True):
        torch.testing.assert_close(actual, restored_value, atol=0, rtol=0)
        np.testing.assert_array_equal((actual[0].permute(1, 2, 0) * 256).numpy(), expected)
    # Restore must also preserve momentum, not only weights.
    for left, right in zip(optimizer.state.values(), restored_optimizer.state.values(), strict=True):
        torch.testing.assert_close(left['momentum_buffer'], right['momentum_buffer'], atol=0, rtol=0)
    if sha256(CHECKPOINT) != CHECKPOINT_HASH:
        raise ValueError('original checkpoint changed')
    result = {'status': 'CPU_QAT_FORWARD_BACKWARD_RESTORE_EXPORT_SMOKE_PASS',
              'image': key, 'image_sha256': dataset.rows[0]['image_sha256'], 'split': 'train',
              'source_checkpoint_unchanged_sha256': CHECKPOINT_HASH, 'source_manifest_sha256': MANIFEST_HASH,
              'source_sha256': {str(path.relative_to(PROJECT)).replace('\\', '/'): sha256(path) for path in sources},
              'trace_tensors_checked': len(trace), 'trace_values_checked': checked_values,
              'loss': {name: float(value.detach()) for name, value in losses.items()},
              'gradient_tensors': len(gradients), 'gradient_nonzero_elements': gradient_nonzero,
              'gradient_norm_before_clip': float(norm), 'changed_parameter_elements': changed,
              'forward_seconds_single_image': forward_seconds, 'loss_backward_update_seconds': backward_update_seconds,
              'disposable_optimizer_updates': 1, 'candidate_training_started': False,
              'cuda_initialized': torch.cuda.is_initialized(), 'restore_and_export_heads_bit_exact': True,
              'optimizer_momentum_restore_exact': True, 'state_sha256': sha256(state_path),
              'export_payload_sha256': exported['payload_sha256'],
              'export_manifest_sha256': sha256(args.output / 'disposable_package/manifest.json'),
              'training_launcher_integrated': False, 'GPU_throughput_tested': False,
              'formal_acceptance': False, 'production_release': False,
              'limitations': 'CPU reference-corrected forward, not efficient GPU backend; no 100-update training run; no accuracy improvement claim; no crash-resume/temperature protection integration yet'}
    save(args.output / 'report.json', result)
    print(json.dumps(result, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
