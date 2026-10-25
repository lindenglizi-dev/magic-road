"""新任务调度候选的复用源码冻结检查，不覆盖旧收据。"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OLD = ROOT.parent / 'result_publish_joint_20261015'
RECEIPT = ROOT / 'frozen_dependencies.json'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def collect():
    pairs = [(path, ROOT / 'rtl' / path.name)
             for path in sorted((OLD / 'rtl').glob('*.v'))]
    pairs += [(path, ROOT / 'vendor_rom' / path.relative_to(OLD / 'vendor_rom'))
              for path in sorted((OLD / 'vendor_rom').rglob('*')) if path.is_file()]
    for folder, name in (
        ('camera_capture_2fps_20261015', 'road_capture_slots.v'),
        ('source_sof_identity_20261015', 'road_source_sof_identity.v')):
        pairs.append((ROOT.parent / folder / 'rtl' / name, ROOT / 'rtl' / name))
    records = []
    for source, copied in pairs:
        source_hash = digest(source)
        assert source_hash == digest(copied), f'Frozen copy differs: {copied}'
        records.append({'source': str(source), 'copy': str(copied), 'sha256': source_hash})
    return records


if __name__ == '__main__':
    records = collect()
    if RECEIPT.exists():
        assert json.loads(RECEIPT.read_text(encoding='utf-8'))['files'] == records
        print(f'PASS unchanged frozen dependencies: {len(records)}')
    else:
        RECEIPT.write_text(json.dumps({'status': 'PASS', 'files': records},
                                     ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f'PASS initial frozen dependencies: {len(records)}')
