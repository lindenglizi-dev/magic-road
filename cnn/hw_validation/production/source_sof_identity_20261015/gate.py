"""Record strict eight-gate failures without weakening the rules."""
import json
import sys
import run

run.check()
work = run.fresh('gate')
entry = "import sys,runpy;sys.path.insert(0," + repr(str(run.SKILL)) + ");runpy.run_module('scripts.python.validation.generated_deliverable_gate',run_name='__main__')"
for path in sorted((run.ROOT / 'rtl').glob('*.v')):
    run.command([sys.executable, '-B', '-X', 'utf8', '-c', entry, str(path),
                 '--json', str(work / (path.stem + '.json')),
                 '--markdown', str(work / (path.stem + '.md'))], run.ROOT,
                str(work.relative_to(run.ROOT) / path.stem), allowed=(0, 1))
    report = json.loads((work / (path.stem + '.json')).read_text(encoding='utf-8'))
    print(path.name, report['errors'], report['strict_warnings'], flush=True)
run.save(work / 'source_hashes.json', {str(p): run.sha(p) for p in (run.ROOT / 'rtl').glob('*.v')})
run.check()
