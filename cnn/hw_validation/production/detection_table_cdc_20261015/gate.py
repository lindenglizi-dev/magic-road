"""Strict diagnostic record; never rewrite RTL to hide a failed rule."""
import json
import sys
import run

run.check()
work = run.fresh('gate')
entry = "import sys,runpy;sys.path.insert(0," + repr(str(run.SKILL)) + ");runpy.run_module('scripts.python.validation.generated_deliverable_gate',run_name='__main__')"
for path in sorted((run.ROOT / 'rtl').glob('*.v')):
    args = [sys.executable, '-B', '-X', 'utf8', '-c', entry, str(path),
            '--json', str(work / (path.stem + '.json')), '--markdown', str(work / (path.stem + '.md'))]
    run.command(args, run.ROOT, str(work.relative_to(run.ROOT) / path.stem), allowed=(0, 1))
    item = json.loads((work / (path.stem + '.json')).read_text(encoding='utf-8'))
    print(path.name, item['errors'], item['strict_warnings'], flush=True)
run.save(work / 'source_hashes.json', {str(path): run.sha(path) for path in (run.ROOT / 'rtl').glob('*.v')})
run.check()
