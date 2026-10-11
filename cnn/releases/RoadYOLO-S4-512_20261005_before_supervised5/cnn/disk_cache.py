"""Opt-in pre-Mosaic disk cache with a bounded standalone CPU QA command.

RGB records are immutable uint8 HWC. An index is published only after all records
are flushed. Missing, stale, incomplete, or corrupt caches fail closed.
"""
from __future__ import annotations

import argparse
import ast
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import shutil
import time
from typing import TYPE_CHECKING

import cv2
import numpy as np
import PIL
import torch
from torch.utils.data import DataLoader

if TYPE_CHECKING:
    from .train import DatasetValidationSnapshot

try:
    from .train import (FullFrameDataset, PREPROCESS_CONTRACT, collate,
                        dataset_content_hash, load_dataset_manifest, reject_cache_qa, sha256)
except ImportError:  # Preserve python cnn/train.py with its opt-in cache.
    from train import (FullFrameDataset, PREPROCESS_CONTRACT, collate,
                       dataset_content_hash, load_dataset_manifest, reject_cache_qa, sha256)


SHAPE = (288, 512, 3)
RECORD_BYTES = int(np.prod(SHAPE))
CONTRACT = 'road-yolo-pre-mosaic-rgb888-disk-v1'
MAX_PILOT_IMAGES = 128


def fingerprint(value):
    encoded = json.dumps(value, sort_keys=True, separators=(',', ':'),
                         default=str).encode('utf-8')
    return hashlib.sha256(encoded).hexdigest()


def _ast_sha256(path, *, name, method=None):
    tree = ast.parse(path.read_text(encoding='utf-8'))
    nodes = tree.body
    for node in nodes:
        node_name = next((target.id for target in getattr(node, 'targets', ())
                          if isinstance(target, ast.Name)), getattr(node, 'name', None))
        if node_name == name:
            if method is not None:
                node = next((child for child in node.body
                             if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef))
                             and child.name == method), None)
            if node is not None:
                return hashlib.sha256(ast.dump(node, include_attributes=False).encode()).hexdigest()
    raise ValueError(f'missing preprocessing source node: {path.name}:{name}.{method or ""}')


def preprocessing_identity():
    root = Path(__file__).parent
    return dict(contract=PREPROCESS_CONTRACT, pixel_order='HWC_RGB', dtype='uint8',
                shape=list(SHAPE), record_bytes=RECORD_BYTES,
                source_sha256={
                    'disk_cache.py': _ast_sha256(root / 'disk_cache.py',
                                                 name='DiskCachedDataset', method='_load'),
                    'train.py': _ast_sha256(root / 'train.py', name='FullFrameDataset'),
                    'dataset.py': sha256(root / 'dataset.py'),
                    'integer.py': sha256(root / 'integer.py'),
                },
                preprocess_contract_ast_sha256=_ast_sha256(
                    root / 'train.py', name='PREPROCESS_CONTRACT'),
                annotation_normalization_ast_sha256=_ast_sha256(
                    root / 'train.py', name='_boxes'),
                source_identity_scope={
                    'disk_cache.py': 'AST DiskCachedDataset._load',
                    'train.py': 'AST FullFrameDataset',
                    'dataset.py': 'whole file (_letterbox_720 dependency)',
                    'integer.py': 'whole file (resize_area dependency)',
                },
                libraries=dict(opencv=cv2.__version__, numpy=np.__version__,
                               pillow=PIL.__version__, torch=torch.__version__))


@dataclass(frozen=True)
class ValidatedCacheBinding:
    """One fail-closed cache validation shared by train and val readers."""
    snapshot: object
    root: Path
    metadata: dict
    entries: tuple[dict, ...]
    index_sha256: str


def _validated_cache(rows, manifest_hash, content_hash, root, expected_index_sha256,
                     *, verify_sources):
    root = Path(root).resolve()
    encoded_index = (root / 'index.json').read_bytes()
    index_hash = hashlib.sha256(encoded_index).hexdigest()
    if expected_index_sha256 is not None and index_hash != expected_index_sha256.lower():
        raise ValueError('cache index receipt mismatch')
    metadata = json.loads(encoded_index)
    if (metadata.get('contract') != CONTRACT or metadata.get('status') != 'complete'
            or metadata.get('dataset_sha256') != manifest_hash
            or metadata.get('dataset_content_sha256') != content_hash
            or metadata.get('preprocessing') != preprocessing_identity()):
        raise ValueError('stale cache identity, manifest, or preprocessing')
    entries = metadata.get('entries', [])
    if len(entries) != len(rows) or metadata.get('rgb_bytes') != len(rows) * RECORD_BYTES:
        raise ValueError('incomplete cache index')
    for index, (row, entry) in enumerate(zip(rows, entries, strict=True)):
        if (entry.get('image') != row['image'] or entry.get('offset') != index * RECORD_BYTES
                or entry.get('row_sha256') != fingerprint(row)
                or entry.get('source_sha256') != row['image_sha256']
                or (verify_sources and sha256(row['image_path']) != row['image_sha256'])):
            raise ValueError('stale source, row, or cache offset')
    blob = root / 'rgb.bin'
    if blob.stat().st_size != metadata['rgb_bytes']:
        raise ValueError('incomplete cache data')
    if sha256(blob) != metadata['rgb_sha256']:
        raise ValueError('corrupt cache data')
    return root, metadata, tuple(entries), index_hash


def open_validated_cache(snapshot: 'DatasetValidationSnapshot', root,
                         expected_index_sha256):
    """Validate one cache once after manifest validation and before CUDA startup."""
    try:
        from .train import DatasetValidationSnapshot
    except ImportError:  # python cnn/train.py
        from train import DatasetValidationSnapshot
    if not isinstance(snapshot, DatasetValidationSnapshot):
        raise TypeError('cache requires a DatasetValidationSnapshot from load_dataset_snapshot')
    if (not isinstance(expected_index_sha256, str) or len(expected_index_sha256) != 64
            or any(character not in '0123456789abcdefABCDEF'
                   for character in expected_index_sha256)):
        raise ValueError('cache binding requires an exact index SHA-256 receipt')
    root, metadata, entries, index_hash = _validated_cache(
        snapshot.rows, snapshot.manifest_sha256, snapshot.dataset_content_sha256,
        root, expected_index_sha256, verify_sources=False)
    return ValidatedCacheBinding(snapshot, root, metadata, entries, index_hash)


def build_cache(manifest, rows, root, *, full_development=False):
    """Exclusive new directory; a failed build remains unpublished, never reused."""
    if not rows or (not full_development and len(rows) > MAX_PILOT_IMAGES) or any(
            row['split'] not in ('train', 'val') for row in rows):
        raise ValueError('prototype requires at most128 development images; no newtest')
    if full_development:
        declared = json.loads(manifest.read_text(encoding='utf-8'))
        reject_cache_qa(declared)
        if (len(declared['images']) != len(rows) or any(
                row['split'] not in ('train', 'val') for row in declared['images'])):
            raise ValueError('full cache requires every development row; no newtest')
    required = len(rows) * RECORD_BYTES
    root.parent.mkdir(parents=True, exist_ok=True)
    if shutil.disk_usage(root.parent).free < required + 20 * (1 << 30):
        raise ValueError('cache would violate the20 GiB free-space reserve')
    manifest_hash = sha256(manifest)
    identity = preprocessing_identity()
    root.mkdir()  # Never overwrite an existing or interrupted experiment.
    started = time.perf_counter()
    entries = []
    digest = hashlib.sha256()
    datasets = {split: FullFrameDataset(rows, split) for split in ('train', 'val')}
    local_index = dict(train=0, val=0)
    with (root / 'rgb.bin').open('xb') as stream:
        for row in rows:
            if sha256(row['image_path']) != row['image_sha256']:
                raise ValueError('source changed after manifest validation')
            index = local_index[row['split']]
            pixels, _, _ = datasets[row['split']]._load(index)
            local_index[row['split']] += 1
            if pixels.shape != SHAPE or pixels.dtype != np.uint8:
                raise ValueError('cache requires512x288 RGB888 before centering')
            encoded = pixels.tobytes(order='C')
            entries.append(dict(image=row['image'], row_sha256=fingerprint(row),
                                source_sha256=row['image_sha256'],
                                offset=stream.tell(), rgb_sha256=hashlib.sha256(encoded).hexdigest()))
            stream.write(encoded)
            digest.update(encoded)
            if full_development and (len(entries) % 1000 == 0 or len(entries) == len(rows)):
                print(f'build {len(entries)}/{len(rows)} '
                      f'{time.perf_counter() - started:.1f}s', flush=True)
        stream.flush()
        os.fsync(stream.fileno())
    if sha256(manifest) != manifest_hash:
        raise ValueError('manifest changed during cache construction')
    if preprocessing_identity() != identity:
        raise ValueError('preprocessing changed during cache construction')
    metadata = dict(contract=CONTRACT, status='complete',
                    dataset_sha256=manifest_hash,
                    dataset_content_sha256=dataset_content_hash(rows),
                    preprocessing=identity, entries=entries,
                    rgb_bytes=required, rgb_sha256=digest.hexdigest(),
                    construction_seconds=time.perf_counter() - started)
    # Readers require index.json. A partial temporary index is never published.
    with (root / 'index.pending.json').open('x', encoding='utf-8') as stream:
        json.dump(metadata, stream, indent=2)
        stream.flush()
        os.fsync(stream.fileno())
    (root / 'index.pending.json').rename(root / 'index.json')
    return metadata


class DiskCachedDataset(FullFrameDataset):
    """Reuse the original Mosaic/centering path; hold no full pixel cache in RAM.

    ponytail: reopen/seek/hash one record per read; persistent worker handles only
    if a later full-epoch profile proves open costs matter.
    """
    def __init__(self, rows, split, manifest, root, *, mosaic=False, seed=42,
                 expected_index_sha256=None, binding=None):
        super().__init__(rows, split, mosaic=mosaic, seed=seed)
        if binding is None:
            self.root, metadata, entries, _ = _validated_cache(
                rows, sha256(manifest), dataset_content_hash(rows), root,
                expected_index_sha256, verify_sources=True)
        else:
            if not isinstance(binding, ValidatedCacheBinding):
                raise TypeError('binding must come from open_validated_cache')
            if (rows is not binding.snapshot.rows
                    or Path(manifest).resolve() != binding.snapshot.manifest.resolve()
                    or Path(root).resolve() != binding.root
                    or (expected_index_sha256 is not None
                        and expected_index_sha256.lower() != binding.index_sha256)):
                raise ValueError('cache binding does not match rows, manifest, root, or receipt')
            self.root, metadata, entries = binding.root, binding.metadata, binding.entries
        self.entries = [entry for row, entry in zip(rows, entries, strict=True)
                        if row['split'] == split]

    def _load(self, index):
        entry, row = self.entries[index], self.rows[index]
        with (self.root / 'rgb.bin').open('rb') as stream:
            stream.seek(entry['offset'])
            encoded = stream.read(RECORD_BYTES)
        if (len(encoded) != RECORD_BYTES
                or hashlib.sha256(encoded).hexdigest() != entry['rgb_sha256']):
            raise ValueError('missing or corrupt RGB cache record')
        pixels = np.frombuffer(encoded, np.uint8).reshape(SHAPE).copy()
        target = {
            'boxes': torch.tensor(row['boxes'], dtype=torch.float32).reshape(-1, 4),
            'labels': torch.tensor(row['labels'], dtype=torch.long),
            'ignore_boxes': torch.tensor(row['ignore_boxes'], dtype=torch.float32).reshape(-1, 4),
        }
        return pixels, target, row['teacher_key']


def assert_item_equal(left, right):
    torch.testing.assert_close(left[0], right[0], rtol=0, atol=0)
    for field in ('boxes', 'labels', 'ignore_boxes'):
        torch.testing.assert_close(left[1][field], right[1][field], rtol=0, atol=0)
    assert left[2] == right[2], 'teacher/Mosaic keys or sample order differ'


def build_full_development(args):
    """All development frames, streamed on CPU; never inspect a newtest image."""
    if not args.dataset_sha256 or sha256(args.dataset) != args.dataset_sha256.lower():
        raise ValueError('full development requires the matching dataset SHA-256 receipt')
    declared = json.loads(args.dataset.read_text(encoding='utf-8'))
    reject_cache_qa(declared)
    if any(row['split'] not in ('train', 'val') for row in declared['images']):
        raise ValueError('full cache is development-only; no newtest')
    required = len(declared['images']) * RECORD_BYTES
    args.cache_dir.parent.mkdir(parents=True, exist_ok=True)
    free_before = shutil.disk_usage(args.cache_dir.parent).free
    if free_before < required + 20 * (1 << 30):
        raise ValueError('cache would violate the20 GiB free-space reserve')
    torch.set_num_threads(2)
    print(f'validate manifest: {len(declared["images"])} frames, {required} bytes', flush=True)
    _, rows = load_dataset_manifest(args.dataset)
    if sha256(args.dataset) != args.dataset_sha256.lower():
        raise ValueError('manifest changed during validation')
    metadata = build_cache(args.dataset, rows, args.cache_dir, full_development=True)
    receipt = sha256(args.cache_dir / 'index.json')
    checks = []
    started = time.perf_counter()
    for split in ('train', 'val'):
        raw = FullFrameDataset(rows, split)
        cached = DiskCachedDataset(rows, split, args.dataset, args.cache_dir,
                                   expected_index_sha256=receipt)
        for index in range(len(raw)):
            # Centering is one-to-one for RGB888: exact centered input also proves RGB bytes.
            assert_item_equal(raw[index], cached[index])
            if (index + 1) % 1000 == 0 or index + 1 == len(raw):
                print(f'verify {split} {index + 1}/{len(raw)} '
                      f'{time.perf_counter() - started:.1f}s', flush=True)
        checks.append(dict(split=split, kind='all_centered_RGB_targets_and_keys', count=len(raw)))
        if split == 'train':
            # ponytail: bounded Mosaic regression; full GPU/epoch parity remains a separate gate.
            indices = np.linspace(0, len(raw) - 1, min(32, len(raw)), dtype=int)
            for epoch in (6, 7):
                raw.set_epoch(epoch, True)
                cached.set_epoch(epoch, True)
                for index in indices:
                    assert_item_equal(raw[int(index)], cached[int(index)])
                checks.append(dict(split=split, kind='evenly_spaced_Mosaic',
                                   epoch=epoch, count=len(indices)))
    free_after = shutil.disk_usage(args.cache_dir.parent).free
    if (free_after < 20 * (1 << 30) or sha256(args.dataset) != args.dataset_sha256.lower()
            or preprocessing_identity() != metadata['preprocessing']
            or sha256(args.cache_dir / 'index.json') != receipt):
        raise ValueError('post-verification reserve or identity check failed')
    result = dict(status='passed_full_development_cache_CPU_equivalence_not_training_speed',
                  dataset_sha256=metadata['dataset_sha256'],
                  dataset_content_sha256=metadata['dataset_content_sha256'],
                  cache_index_sha256=receipt, rgb_sha256=metadata['rgb_sha256'],
                  preprocessing=metadata['preprocessing'],
                  cached_images=len(rows), cache_bytes=required, checks=checks,
                  positive_boxes=sum(len(row['boxes']) for row in rows),
                  ignore_regions=sum(len(row['ignore_boxes']) for row in rows),
                  construction_seconds=metadata['construction_seconds'],
                  verification_seconds=time.perf_counter() - started,
                  free_bytes_before=free_before, free_bytes_after=free_after,
                  device='cpu', cpu_threads=2, gpu_used=False, optimizer_updates=0,
                  training_started=False, maximum_compared_difference=0,
                  full_training_speed_measured=False, accuracy_measured=False,
                  limitation='All development single-frame inputs checked; Mosaic is bounded. '
                             'No GPU AMP, accumulated batch64, optimizer, accuracy or FPGA evidence.')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x', encoding='utf-8') as stream:
        json.dump(result, stream, indent=2)
    print(json.dumps(result, indent=2), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dataset', type=Path, required=True)
    parser.add_argument('--cache-dir', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--full-development', action='store_true')
    parser.add_argument('--dataset-sha256')
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    if args.full_development:
        build_full_development(args)
        return
    if args.dataset_sha256 is not None:
        raise ValueError('--dataset-sha256 requires --full-development')
    declared = json.loads(args.dataset.read_text(encoding='utf-8'))
    if len(declared['images']) > MAX_PILOT_IMAGES or any(
            row['split'] not in ('train', 'val') for row in declared['images']):
        raise ValueError('use an audited development pilot of at most128 images')
    torch.set_num_threads(2)
    _, rows = load_dataset_manifest(args.dataset, allow_cache_qa=True)
    metadata = build_cache(args.dataset, rows, args.cache_dir)
    checks = []
    for split in ('train', 'val'):
        raw = FullFrameDataset(rows, split)
        cached = DiskCachedDataset(rows, split, args.dataset, args.cache_dir)
        for index in range(len(raw)):
            # Compare both raw uint8 RGB and centered float32 CNN input.
            left, right = raw._load(index), cached._load(index)
            np.testing.assert_array_equal(left[0], right[0])
            assert_item_equal(raw[index], cached[index])
        checks.append(dict(split=split, kind='all_RGB_and_centered_inputs', count=len(raw)))
        if split == 'train':
            for epoch, mosaic in ((6, True), (7, True), (285, False)):
                raw.set_epoch(epoch, mosaic)
                cached.set_epoch(epoch, mosaic)
                for index in range(len(raw)):
                    assert_item_equal(raw[index], cached[index])
                checks.append(dict(split=split, epoch=epoch, mosaic=mosaic, count=len(raw)))
            for workers in (0, 2):
                raw.set_epoch(7, True)
                cached.set_epoch(7, True)
                options = dict(batch_size=8, num_workers=workers, shuffle=True, collate_fn=collate)
                loaders = [DataLoader(data, generator=torch.Generator().manual_seed(49), **options)
                           for data in (raw, cached)]
                count = 0
                for left, right in zip(*loaders, strict=True):
                    torch.testing.assert_close(left[0], right[0], rtol=0, atol=0)
                    assert left[2] == right[2], 'shuffle order differs'
                    for a, b in zip(left[1], right[1], strict=True):
                        for field in ('boxes', 'labels', 'ignore_boxes'):
                            torch.testing.assert_close(a[field], b[field], rtol=0, atol=0)
                    count += len(left[2])
                assert count == len(raw)
                checks.append(dict(kind='shuffled_DataLoader', workers=workers, count=count))
    raw = FullFrameDataset(rows, 'train', mosaic=True, seed=42)
    cached = DiskCachedDataset(rows, 'train', args.dataset, args.cache_dir, mosaic=True, seed=42)
    raw.set_epoch(6)
    cached.set_epoch(6)
    timings = {}
    for name, dataset in (('raw', raw), ('disk', cached)):
        trials = []
        for _ in range(3):
            started = time.perf_counter()
            for index in range(len(dataset)):
                dataset[index]
            trials.append(time.perf_counter() - started)
        timings[name] = dict(trials_seconds=trials,
                             median_seconds_per_mosaic=float(np.median(trials)) / len(dataset))
    result = dict(status='passed_exact_disk_cache_prototype_not_training_speed',
                  dataset_sha256=sha256(args.dataset), cache_index_sha256=sha256(args.cache_dir / 'index.json'),
                  source_sha256=sha256(Path(__file__)), device='cpu', cpu_threads=2,
                  gpu_used=False, training_started=False, production_trainer_modified=False,
                  cached_images=len(rows), cache_bytes=metadata['rgb_bytes'],
                  construction_seconds=metadata['construction_seconds'], checks=checks,
                  timings=timings,
                  isolated_preprocess_speedup=(timings['raw']['median_seconds_per_mosaic'] /
                                              timings['disk']['median_seconds_per_mosaic']),
                  limitation='Warm OS filesystem cache; not physical cold-disk latency, forward/backward '
                             'or full training throughput. Pilot only; no full COCO/road cache built.')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x', encoding='utf-8') as stream:
        json.dump(result, stream, indent=2)
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    main()
