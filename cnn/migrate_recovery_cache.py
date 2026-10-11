"""Publish the reviewed road cache under the scoped preprocessing identity."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import torch

from .disk_cache import preprocessing_identity
from .train import sha256


ROOT = Path(__file__).resolve().parent.parent
OLD_INDEX_SHA256 = "850854a0d4a89de0466bfd80d3dbdd25eee10ab77f22f03ccf97f707f2fd3cec"
OLD_RECEIPT_SHA256 = "e33fd1a17eb501406d0dd87755221353546f7f8f4226337bbb4424188ef0c1b4"
FULL_PARITY_RECEIPT_SHA256 = "aa024aec8c21f779e8a248f9f3d6179218d34b210785e6bc6cfe2ce7f100eb13"
BASELINE_SHA256 = "914a5c29aa17a26b932eb3e79a24ddb33b600512f993535da2384bb1ea6c4f39"
RGB_SHA256 = "cb01e0c54596ab66e2418b926eabda2ce5236db41e082786355933f18bef1758"


def migrate_cache(manifest: Path, old_root: Path, old_receipt_path: Path,
                  full_parity_receipt_path: Path, baseline_path: Path,
                  new_root: Path, output: Path) -> dict:
    paths = [manifest, old_root, old_receipt_path, full_parity_receipt_path,
             baseline_path, new_root, output]
    (manifest, old_root, old_receipt_path, full_parity_receipt_path,
     baseline_path, new_root, output) = (Path(path).resolve() for path in paths)
    if torch.cuda.is_initialized():
        raise RuntimeError('cache migration must run before CUDA initialization')
    if new_root.exists() or output.exists():
        raise FileExistsError('recovery cache and receipt are publish-once')
    output_pending = output.with_suffix(output.suffix + '.pending')
    if output_pending.exists():
        raise FileExistsError(output_pending)
    if (sha256(old_root / 'index.json') != OLD_INDEX_SHA256
            or sha256(old_receipt_path) != OLD_RECEIPT_SHA256
            or sha256(full_parity_receipt_path) != FULL_PARITY_RECEIPT_SHA256
            or sha256(baseline_path) != BASELINE_SHA256):
        raise ValueError('reviewed cache, receipt, or source baseline changed')

    metadata = json.loads((old_root / 'index.json').read_bytes())
    receipt = json.loads(old_receipt_path.read_text(encoding='utf-8'))
    baseline = json.loads(baseline_path.read_text(encoding='utf-8'))
    migration_source_sha256 = sha256(Path(__file__))
    identity = preprocessing_identity()
    ast_hashes = baseline['pixel_ast_sha256']
    source_hashes = baseline['source_sha256']
    if (identity['source_sha256']['train.py'] != ast_hashes['train.py']['FullFrameDataset']
            or identity['source_sha256']['disk_cache.py'] != ast_hashes['disk_cache.py']['_load']
            or identity['preprocess_contract_ast_sha256']
            != ast_hashes['train.py']['PREPROCESS_CONTRACT']
            or identity['annotation_normalization_ast_sha256']
            != ast_hashes['train.py']['_boxes']
            or identity['source_sha256']['dataset.py'] != source_hashes['dataset.py']
            or identity['source_sha256']['integer.py'] != source_hashes['integer.py']):
        raise ValueError('pixel preprocessing source changed from the pre-edit baseline')
    old_identity = metadata.get('preprocessing', {})
    stable_fields = ('contract', 'pixel_order', 'dtype', 'shape', 'record_bytes', 'libraries')
    if any(identity.get(field) != old_identity.get(field) for field in stable_fields):
        raise ValueError('preprocessing contract or library versions changed')
    blob = old_root / 'rgb.bin'
    if (metadata.get('status') != 'complete'
            or metadata.get('rgb_sha256') != RGB_SHA256
            or blob.stat().st_size != metadata.get('rgb_bytes')
            or receipt.get('cache_index_sha256') != OLD_INDEX_SHA256
            or receipt.get('rgb_sha256') != RGB_SHA256
            or receipt.get('inherited_full_parity_receipt_sha256')
            != FULL_PARITY_RECEIPT_SHA256
            or metadata.get('dataset_sha256') != sha256(manifest)):
        raise ValueError('reviewed metadata or inherited full parity provenance changed')

    new_root.parent.mkdir(parents=True, exist_ok=True)
    output.parent.mkdir(parents=True, exist_ok=True)
    new_root.mkdir()
    os.link(blob, new_root / 'rgb.bin')
    if not os.path.samefile(blob, new_root / 'rgb.bin'):
        raise ValueError('recovery RGB blob is not a hard link to the reviewed cache')
    new_metadata = dict(metadata)
    new_metadata['preprocessing'] = identity
    new_metadata['migration'] = {
        'kind': 'scoped_preprocessing_identity_no_pixel_reread',
        'old_cache_index_sha256': OLD_INDEX_SHA256,
        'old_receipt_sha256': OLD_RECEIPT_SHA256,
        'inherited_full_parity_receipt_sha256': FULL_PARITY_RECEIPT_SHA256,
        'source_baseline_sha256': BASELINE_SHA256,
        'migration_source_sha256': migration_source_sha256,
    }
    pending_index = new_root / 'index.pending.json'
    with pending_index.open('x', encoding='utf-8') as stream:
        json.dump(new_metadata, stream, indent=2)
        stream.flush()
        os.fsync(stream.fileno())
    pending_index.rename(new_root / 'index.json')
    result = {
        'status': 'passed_scoped_preprocessing_identity_migration_no_pixel_reread',
        'manifest_path': str(manifest),
        'old_cache_path': str(old_root),
        'new_cache_path': str(new_root),
        'old_receipt_path': str(old_receipt_path),
        'full_parity_receipt_path': str(full_parity_receipt_path),
        'source_baseline_path': str(baseline_path),
        'dataset_sha256': metadata['dataset_sha256'],
        'dataset_content_sha256': metadata['dataset_content_sha256'],
        'cached_images': len(metadata['entries']),
        'cache_bytes': metadata['rgb_bytes'],
        'rgb_sha256': RGB_SHA256,
        'cache_index_sha256': sha256(new_root / 'index.json'),
        'old_cache_index_sha256': OLD_INDEX_SHA256,
        'old_receipt_sha256': OLD_RECEIPT_SHA256,
        'inherited_full_parity_receipt_sha256': FULL_PARITY_RECEIPT_SHA256,
        'source_baseline_sha256': BASELINE_SHA256,
        'migration_source_sha256': migration_source_sha256,
        'preprocessing': identity,
        'previous_libraries': old_identity.get('libraries'),
        'rgb_hardlink_same_file': True,
        'old_cache_preserved': True,
        'full_pixel_reread_performed': False,
        'training_started': False,
        'gpu_used': False,
    }
    with output_pending.open('x', encoding='utf-8') as stream:
        json.dump(result, stream, indent=2)
        stream.flush()
        os.fsync(stream.fileno())
    output_pending.rename(output)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, default=ROOT / 'cnn/data/visdrone_vid_train/raw_manifest/dataset.json')
    parser.add_argument('--old-cache', type=Path, default=ROOT / 'cnn/data/cache_road_memory_20261003')
    parser.add_argument('--old-receipt', type=Path, default=ROOT / 'cnn/reports/cache_road_memory_rebind_20261003.json')
    parser.add_argument('--full-parity-receipt', type=Path, default=ROOT / 'cnn/reports/cache_road_pause_rebind_20261003.json')
    parser.add_argument('--baseline', type=Path, default=ROOT / 'cnn/artifacts/recovery_source_baseline_20261003.json')
    parser.add_argument('--new-cache', type=Path, default=ROOT / 'cnn/data/cache_road_recovery_20261003')
    parser.add_argument('--output', type=Path, default=ROOT / 'cnn/reports/cache_road_recovery_migration_20261003.json')
    args = parser.parse_args()
    result = migrate_cache(args.manifest, args.old_cache, args.old_receipt,
                           args.full_parity_receipt, args.baseline,
                           args.new_cache, args.output)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
