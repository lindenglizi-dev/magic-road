"""Read-only skill dependency check with all outputs inside the candidate."""
import json
import sys
from pathlib import Path
from guard import ROOT, check, run

SKILL = Path(r'C:\Users\lenovo\.codex\skills\readable-verilog-generator')

if __name__ == '__main__':
    code = run([sys.executable, '-B', '-X', 'utf8', '-c',
                'import sys,runpy;sys.path.insert(0,sys.argv.pop(1));'
                'runpy.run_module("scripts.python.toolchain.manage_skill_dependencies",run_name="__main__")',
                str(SKILL), 'check', '--settings', str(SKILL / 'config/defaults.json'),
                '--state-path', str(ROOT / 'dependency_state.json')],
               ROOT, ROOT / 'dependency_preflight.log')
    print(json.dumps({'exit': code, 'guard': check()}))
