"""Strict original/candidate diagnostics, writing only under the S1 directory."""
import argparse
import json
import sys
import run


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('target', choices=('original', 'candidate'))
    args = parser.parse_args()
    run.check()
    sys.path.insert(0, str(run.SKILL))
    from scripts.python.toolchain.dependency_state import check_dependencies
    deps = check_dependencies(json.loads((run.SKILL / 'config/defaults.json').read_text(encoding='utf-8')),
                              state_path=run.ROOT / 'dependency_state.json')
    run.save(run.ROOT / 'dependency_preflight_current.json', deps)
    assert deps['required_ok']
    work = run.fresh('gate_' + args.target)
    target = (run.BASE if args.target == 'original' else run.ROOT) / 'rtl'
    entry = f'import sys;sys.path.insert(0,{str(run.SKILL)!r});from scripts.python.validation.generated_deliverable_gate import main;raise SystemExit(main())'
    external = []
    for path in (run.ROOT / 'shared_core_interface.v', run.ROOT / 'new_interfaces.v',
                 run.PROJECT / 'user_source/hdl_source/ph1p35_ddr/ddr2/ddr2.v',
                 run.PROJECT / 'cnn/hw_validation/production/reports/board_selftest_20261010/rtl/road_selftest_display.v'):
        external += ['--external-interface-source', path]
    run.command([sys.executable, '-B', '-X', 'utf8', '-c', entry, target, *external,
                 '--json', work / 'rtl.json', '--markdown', work / 'rtl.md'], work, 'gate', allowed=(0, 1, 2))
    result = json.loads((work / 'rtl.json').read_text(encoding='utf-8'))
    run.save(work / 'source_hashes.json', {str(p): run.sha(p) for p in target.glob('*.v')})
    print({k: result[k] for k in ('errors', 'strict_warnings', 'delivery_ready')}, flush=True)
    run.check()


if __name__ == '__main__':
    main()
