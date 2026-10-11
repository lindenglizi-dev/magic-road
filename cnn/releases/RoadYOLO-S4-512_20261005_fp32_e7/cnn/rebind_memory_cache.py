"""Reuse exact pixel QA only for the one-line unused-manifest release."""
import hashlib
import json
import os
from pathlib import Path

from .disk_cache import preprocessing_identity
from .train import sha256

ROOT = Path(__file__).resolve().parent.parent
RELEASE = b'    del _manifest  # Normalized rows own the annotations needed by training.\n'
OLD_TRAIN = 'adb634b9ae29b89c6dde782bc72e870069c267e1090372ad2466c1a599ee17dc'


def check_release(source):
    # Reverse the sole permitted edit; any other code/whitespace change fails.
    if source.count(RELEASE) != 1 or hashlib.sha256(
            source.replace(RELEASE, b'', 1)).hexdigest() != OLD_TRAIN:
        raise ValueError('not the reviewed one-line memory-only change')


def main():
    check_release((ROOT / 'cnn/train.py').read_bytes())
    old = ROOT / 'cnn/data/cache_road_pause_20261003'
    receipt_path = ROOT / 'cnn/reports/cache_road_pause_rebind_20261003.json'
    if sha256(receipt_path) != 'aa024aec8c21f779e8a248f9f3d6179218d34b210785e6bc6cfe2ce7f100eb13':
        raise ValueError('original full parity receipt changed')
    receipt = json.loads(receipt_path.read_text(encoding='utf-8'))
    if sha256(old / 'index.json') != receipt['cache_index_sha256']:
        raise ValueError('original cache index changed')
    metadata = json.loads((old / 'index.json').read_bytes())
    identity = preprocessing_identity()
    previous_identity = json.loads(json.dumps(identity))
    previous_identity['source_sha256']['train.py'] = OLD_TRAIN
    if metadata['preprocessing'] != previous_identity or receipt['preprocessing'] != previous_identity:
        raise ValueError('preprocessing other than memory release changed')
    if (metadata['rgb_sha256'] != receipt['rgb_sha256']
            or (old / 'rgb.bin').stat().st_size != metadata['rgb_bytes']):
        raise ValueError('pixel contract changed')
    destination = ROOT / 'cnn/data/cache_road_memory_20261003'
    report = ROOT / 'cnn/reports/cache_road_memory_rebind_20261003.json'
    if destination.exists() or report.exists():
        raise FileExistsError('memory cache already exists; never overwrite')
    destination.mkdir()
    os.link(old / 'rgb.bin', destination / 'rgb.bin')
    metadata['preprocessing'] = identity
    # No pixel/annotation edits; runtime still hashes the full blob and every read.
    with (destination / 'index.pending.json').open('x', encoding='utf-8') as stream:
        json.dump(metadata, stream, indent=2)
        stream.flush()
        os.fsync(stream.fileno())
    (destination / 'index.pending.json').rename(destination / 'index.json')
    result = dict(receipt, status='passed_memory_only_source_rebind',
                  preprocessing=identity, preprocessing_after=identity,
                  cache_index_sha256=sha256(destination / 'index.json'),
                  inherited_full_parity_receipt_sha256=sha256(receipt_path),
                  verification_scope='Inherited prior complete pixel QA; exact reverse source '
                  'hash proves only unused manifest release. No new full pixel QA performed.',
                  rgb_hardlink_not_backup=True, training_started=False)
    with report.open('x', encoding='utf-8') as stream:
        json.dump(result, stream, indent=2)
    print(json.dumps(dict(status=result['status'], report=str(report))))


if __name__ == '__main__':
    main()
