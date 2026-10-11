"""独立短收尾候选：绑定冻结输入、检查回归日志，不改写RTL。"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / 'v17_pw_prefetch_20261008'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def snapshot():
    return {str(p.relative_to(BASE)).replace('\\', '/'): sha(p)
            for p in sorted(BASE.rglob('*')) if p.is_file()}

def main():
    mode = sys.argv[1]
    receipt = ROOT / 'baseline_freeze.json'
    if mode == 'freeze':
        assert not receipt.exists(), 'Do not overwrite frozen baseline'
        saved = {'baseline': str(BASE), 'files': snapshot()}
        original = json.loads((BASE / 'source_manifest.json').read_text(encoding='utf-8'))
        assert all(saved['files'][name] == value for name, value in original['files'].items())
        receipt.write_text(json.dumps(saved, indent=2) + '\n', encoding='utf-8')
        print('FREEZE_PASS files=', len(saved['files']))
    elif mode == 'check':
        before = json.loads(receipt.read_text(encoding='utf-8'))['files']
        after = snapshot()
        assert before == after, 'Frozen v17 has changed'
        for path in (ROOT / 'verification/vectors').glob('*.hex'):
            assert sha(path) == sha(BASE / 'verification/regression_candidate/vectors' / path.name), path.name
        original_mac = BASE.parent / 'v9_mac_stream_20261007'
        assert sha(ROOT / 'verification/stream_vectors.txt') == sha(original_mac / 'verification/stream_vectors.txt')
        assert sha(ROOT / 'frozen/road_mac_probe.v') == sha(original_mac / 'core/road_mac_probe.v'), 'Historical original MAC changed'
        for name in ('down2_overlap_tile_runner.v', 'road_postprocess_stream.v',
                     'road_round_shift.v', 'silu_shared_unit.v'):
            assert sha(ROOT / 'rtl' / name) == sha(ROOT / 'frozen' / name), name
        for name in ('shell.sdc', 'shell.adc', 'road_postprocess_low_io_top.v', 'build.tcl'):
            assert sha(ROOT / 'physical' / name) == sha(ROOT / 'frozen' / name), name
        frozen_mac = (ROOT / 'frozen/road_mac_probe.v').read_text(encoding='utf-8')
        candidate_mac = (ROOT / 'rtl/road_mac_probe.v').read_text(encoding='utf-8')
        # A0..A5行为区字节等价；只允许终态延迟与输出源变更。
        start = '//-------------主要任务处理区域-------------//'
        assert frozen_mac.split(start)[1].split('//A6延迟')[0].strip() == candidate_mac.split(start)[1].split('endmodule')[0].strip(), 'Arithmetic body changed'
        checked = {}
        for name, marker in (('mac_final.log', 'TB_PASS_MAC_STREAM'),
                             ('tile_final.log', 'TB_PASS_DOWN2_TILE')):
            log = (ROOT / 'verification' / name).read_text(encoding='utf-8')
            assert marker in log and 'TB_ERROR' not in log and 'TB_FAIL' not in log, name
            checked[name] = sha(ROOT / 'verification' / name)
        report = {'status': 'FUNCTION_PASS_PHYSICAL_SEPARATE', 'baseline_files_unchanged': len(before),
                  'unchanged_arithmetic_A0_A5': True, 'logs': checked,
                  'vector_binding': {str(p.relative_to(ROOT)).replace('\\', '/'): sha(p)
                                     for p in sorted((ROOT / 'verification/vectors').glob('*.hex'))},
                  'stream_vectors_sha256': sha(ROOT / 'verification/stream_vectors.txt'),
                  'rtl': {p.name: sha(p) for p in sorted((ROOT / 'rtl').glob('*.v'))}}
        (ROOT / 'verification/function_receipt.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
        print('FREEZE_AND_FUNCTION_PASS', json.dumps(report))
    else:
        raise ValueError(mode)

if __name__ == '__main__':
    main()
