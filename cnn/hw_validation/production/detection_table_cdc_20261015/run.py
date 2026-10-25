"""Reuse bounded local tool execution helpers; write only in this candidate."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / 'camera_capture_2fps_20261015'
spec = importlib.util.spec_from_file_location('frozen_capture_tools', BASE / 'run.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
PROJECT, SKILL, MSIM = module.PROJECT, module.SKILL, module.MSIM
sha, save, fresh, command, check = module.sha, module.save, module.fresh, module.command, module.check
save.__globals__['ROOT'] = ROOT


def dependency():
    import json
    import sys
    sys.path.insert(0, str(SKILL))
    from scripts.python.toolchain.dependency_state import check_dependencies
    result = check_dependencies(json.loads((SKILL / 'config/defaults.json').read_text(encoding='utf-8')),
                                state_path=ROOT / 'dependency_state.json')
    save(ROOT / 'dependency_preflight.json', result)
    assert result['required_ok']


if __name__ == '__main__':
    dependency()
