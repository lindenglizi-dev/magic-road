"""Isolated capture components; reuse existing bounded local tool helpers."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / 'frontend_rgb_reuse_20261015'
spec = importlib.util.spec_from_file_location('s1_frozen_tools', BASE / 'run.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.module.driver.ROOT = ROOT
PROJECT, SKILL, MSIM = module.PROJECT, module.SKILL, module.MSIM
sha, save, fresh, command, check = module.sha, module.save, module.fresh, module.command, module.check


def dependency():
    import json
    import sys
    sys.path.insert(0, str(SKILL))
    from scripts.python.toolchain.dependency_state import check_dependencies
    result = check_dependencies(json.loads((SKILL / 'config/defaults.json').read_text(encoding='utf-8')),
                                state_path=ROOT / 'dependency_state.json')
    save(ROOT / 'dependency_preflight.json', result)
    assert result['required_ok']


def gate():
    import sys
    check()
    work = fresh('gate')
    vendor = Path('E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/sim_release/ph1p/ph1p_logic_eram.v')
    interface = ROOT / 'vendor_interface.v'
    if not interface.exists():
        extract = "import sys,runpy;sys.path.insert(0," + repr(str(SKILL)) + ");runpy.run_module('scripts.python.quality.external_interface_stubs',run_name='__main__')"
        command([sys.executable, '-B', '-X', 'utf8', '-c', extract, 'extract',
                 '--source', str(vendor), '--module', 'PH1P_LOGIC_ERAM', '--output', str(interface)],
                ROOT, str(work.relative_to(ROOT) / 'extract'))
        save(ROOT / 'vendor_interface_receipt.json', {'source': str(vendor), 'sha256': sha(vendor),
                                                     'interface_sha256': sha(interface),
                                                     'scope': 'static ports only; NEVER simulation or synthesis model'})
    entry = "import sys,runpy;sys.path.insert(0," + repr(str(SKILL)) + ");runpy.run_module('scripts.python.validation.generated_deliverable_gate',run_name='__main__')"
    for path in sorted((ROOT / 'rtl').glob('*.v')):
        command([sys.executable, '-B', '-X', 'utf8', '-c', entry, str(path),
                 '--external-interface-source', str(interface),
                 '--json', str(work / (path.stem + '.json')),
                 '--markdown', str(work / (path.stem + '.md'))], ROOT,
                str(work.relative_to(ROOT) / path.stem), allowed=(0, 1))
    check()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('dependency', 'gate', 'check'))
    globals()[parser.parse_args().action]()
