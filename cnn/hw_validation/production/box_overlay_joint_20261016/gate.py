"""Strict diagnostic gates, static native interfaces are never simulation models."""
import json
import sys
from pathlib import Path
import run

run.check()
work = run.fresh('gate')
vendor = Path('E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/sim_release/ph1p/ph1p_logic_dram.v')
interface = run.ROOT / 'vendor_interface.v'
if not interface.exists():
    entry = "import sys,runpy;sys.path.insert(0," + repr(str(run.SKILL)) + ");runpy.run_module('scripts.python.quality.external_interface_stubs',run_name='__main__')"
    run.command([sys.executable, '-B', '-X', 'utf8', '-c', entry, 'render-manifest',
                 '--manifest', str(run.ROOT / 'vendor_interface_manifest.json'), '--output', str(interface)],
                run.ROOT, str(work.relative_to(run.ROOT) / 'reviewed_interface'))
    run.save(run.ROOT / 'vendor_interface_receipt.json', {'source': str(vendor), 'sha256': run.sha(vendor),
        'interface_sha256': run.sha(interface),
        'manifest_sha256': run.sha(run.ROOT / 'vendor_interface_manifest.json'),
        'first_extraction_failure': 'gate/extract.log',
        'boundary': 'reviewed exact static interface only; actual ModelSim uses untouched vendor source'})
entry = "import sys,runpy;sys.path.insert(0," + repr(str(run.SKILL)) + ");runpy.run_module('scripts.python.validation.generated_deliverable_gate',run_name='__main__')"
for path in sorted((run.ROOT / 'rtl').glob('*.v')):
    args = [sys.executable, '-B', '-X', 'utf8', '-c', entry, str(path),
            '--external-interface-source', str(interface)]
    if path.stem == 'road_box_age_overlay':
        args += ['--external-interface-source', str(run.ROOT / 'rtl/road_box_line_overlay.v'),
                 '--external-interface-source', str(run.BASE / 'rtl/road_age_overlay.v')]
    args += ['--json', str(work / (path.stem + '.json')), '--markdown', str(work / (path.stem + '.md'))]
    run.command(args, run.ROOT, str(work.relative_to(run.ROOT) / path.stem), allowed=(0, 1))
    report = json.loads((work / (path.stem + '.json')).read_text(encoding='utf-8'))
    print(path.name, report['errors'], report['strict_warnings'], flush=True)
run.save(work / 'source_hashes.json', {str(p): run.sha(p) for p in (run.ROOT / 'rtl').glob('*.v')})
run.check()
