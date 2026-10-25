"""只核对本候选复用依赖；首次建收据，以后只比较，不覆盖基线。"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OLD = ROOT.parent / 'postprocess_real_rom_1fps_20261015'
C8 = ROOT.parent / 'detection_table_cdc_20261015'
RECEIPT = ROOT / 'frozen_dependencies.json'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def collect():
    pairs = [(OLD / 'rtl' / name, ROOT / 'rtl' / name) for name in (
        'road_candidate_ram.v', 'road_head_decode_topk.v',
        'road_shared_lut_service.v', 'road_nms_serial.v')]
    pairs += [(C8 / 'rtl' / name, ROOT / 'rtl' / name) for name in (
        'road_detection_table_cdc.v', 'road_time_snapshot.v')]
    pairs += [(path, ROOT / 'vendor_rom' / path.relative_to(OLD / 'vendor_rom'))
              for path in sorted((OLD / 'vendor_rom').rglob('*')) if path.is_file()]
    records = []
    for source, copied in pairs:
        source_hash, copy_hash = digest(source), digest(copied)
        assert source_hash == copy_hash, f'Frozen copy differs: {copied}'
        records.append({'source': str(source), 'copy': str(copied), 'sha256': source_hash})
    return records


if __name__ == '__main__':
    records = collect()
    if RECEIPT.exists():
        assert json.loads(RECEIPT.read_text(encoding='utf-8'))['files'] == records, \
            'Frozen dependency changed since first receipt'
        print(f'PASS unchanged frozen dependencies: {len(records)}')
    else:
        RECEIPT.write_text(json.dumps({'status': 'PASS', 'files': records},
                                     ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f'PASS initial frozen dependencies: {len(records)}')
