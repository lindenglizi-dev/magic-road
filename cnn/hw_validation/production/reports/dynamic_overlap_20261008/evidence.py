"""隔离候选的路径约束、旧证据冻结和文件哈希。"""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / 'diagnostic_repair_20261008'


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def confined(path):
    path = Path(path).resolve()
    assert path.is_relative_to(ROOT), path
    return path


def freeze():
    record = json.loads((BASE / 'frozen.json').read_text(encoding='utf-8'))
    receipt = json.loads((BASE / 'delivery_receipt.json').read_text(encoding='utf-8'))
    record.update({str(BASE / name): digest for name, digest in receipt['artifact_hashes'].items()})
    record[str(BASE / 'delivery_receipt.json')] = sha(BASE / 'delivery_receipt.json')
    with confined(ROOT / 'frozen.json').open('x', encoding='utf-8') as stream:
        json.dump(record, stream, ensure_ascii=False, indent=2)
    check()


def check():
    record = json.loads((ROOT / 'frozen.json').read_text(encoding='utf-8'))
    failed = [name for name, digest in record.items() if sha(name) != digest]
    assert not failed, failed
    for name in ('road_dynamic_requant.v', 'road_round_shift.v', 'silu_shared_unit.v'):
        assert sha(ROOT / 'rtl' / name) == sha(BASE / 'candidate/rtl' / name), name
    assert sha(ROOT / 'rtl/road_mac_probe.v') == sha(BASE / 'layer/rtl_declared/road_mac_probe.v')
    print('FROZEN_BASE_AND_ARITHMETIC_PASS', len(record), flush=True)


if __name__ == '__main__':
    if sys.argv[1:] == ['freeze']:
        freeze()
    else:
        check()
