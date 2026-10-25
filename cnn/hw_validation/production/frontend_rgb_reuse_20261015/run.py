"""S1 candidate: bind the existing full-frontend tools to this directory only."""
import argparse
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / 'reports/frontend_ddr_full_20261015'
spec = importlib.util.spec_from_file_location('frozen_full_driver', BASE / 'run.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.driver.ROOT = ROOT
PROJECT, PREVIOUS, SKILL, MSIM = module.PROJECT, module.PREVIOUS, module.SKILL, module.MSIM
sha, save, fresh, command, check = module.sha, module.save, module.fresh, module.command, module.check


def timing(path):
    spec = importlib.util.spec_from_file_location('frozen_timing_parser', BASE.parent / 'ddr_display_cdc_20261013/run_cdc.py')
    parser = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(parser)
    return parser.timing(path)


def physical():
    import json
    check()
    work = ROOT / 'implementation'
    assert (work / 'source_hashes.json').exists(), 'Run prepare_physical.py first'
    assert not (work / 'td.log').exists(), 'Do not repeat a physical attempt'
    closure = json.loads((work / 'source_hashes.json').read_text(encoding='utf-8'))
    assert all(sha(p) == h for p, h in closure.items())
    output = command(['E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/bin/td_commands_prompt.exe', 'build.tcl'],
                     work, 'td', allowed=(0, 1, 2))
    assert 'ONCE_PHYSICAL_COMPLETE' in output
    assert all(sha(p) == h for p, h in closure.items())
    check()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('check', 'physical'))
    args = parser.parse_args()
    if args.action == 'check':
        check()
    else:
        physical()
