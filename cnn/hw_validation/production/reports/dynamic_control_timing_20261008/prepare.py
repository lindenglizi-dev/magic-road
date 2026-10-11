"""Freeze earlier evidence; all generated files stay beside this script."""
from pathlib import Path
import hashlib
import json
import shutil
import sys

HERE = Path(__file__).resolve().parent
REPORTS = HERE.parent
OLD = REPORTS / 'fixed_graph_function_20261008'
V19 = REPORTS / 'v19_mac_short_closure_20261008'

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def check():
    frozen = json.loads((HERE / 'frozen.json').read_text(encoding='utf-8'))
    changed = [name for name, digest in frozen.items() if sha(REPORTS / name) != digest]
    assert not changed, changed
    print('FREEZE_CHECK_PASS', len(frozen))

def prepare():
    assert not (HERE / 'frozen.json').exists(), 'Do not replace a freeze'
    paths = []
    for directory in (OLD, V19, REPORTS / 'functional_completion_20261008',
                      REPORTS / 'dynamic_postprocess_function_20261008'):
        paths.extend(p for p in directory.rglob('*') if p.is_file())
    frozen = {p.relative_to(REPORTS).as_posix(): sha(p) for p in paths}
    (HERE / 'frozen.json').write_text(json.dumps(frozen, indent=2), encoding='utf-8')
    for folder in ('baseline/rtl', 'candidate/rtl', 'baseline/physical', 'candidate/physical'):
        (HERE / folder).mkdir(parents=True, exist_ok=True)
    for target in ('baseline', 'candidate'):
        for p in (OLD / 'rtl').glob('*.v'):
            shutil.copy2(p, HERE / target / 'rtl' / p.name)
        for name in ('batches.txt', 'counts.vh', 'table.hex', 'results.csv'):
            shutil.copy2(OLD / name, HERE / target / name)
        shutil.copy2(REPORTS / 'dynamic_postprocess_function_20261008' / 'tb_road_dynamic_postprocess.v', HERE / target / 'tb_road_dynamic_postprocess.v')
        for name in ('shell.sdc', 'shell.adc'):
            shutil.copy2(V19 / 'physical' / name, HERE / target / 'physical' / name)
    gate = json.loads((OLD / 'gate.json').read_text(encoding='utf-8'))
    selected = [f for f in gate['findings'] if f.get('rule_id', f.get('rule', '')) in
                {'VG093', 'VG138', 'VG145', 'VG146', 'VG151', 'VG152', 'VG153', 'VG154'}]
    (HERE / 'semantic_findings.json').write_text(json.dumps(selected, ensure_ascii=False, indent=2), encoding='utf-8')
    print('FREEZE_CREATED', len(frozen), 'semantic findings', len(selected))
    check()

if __name__ == '__main__':
    check() if '--check' in sys.argv else prepare()
