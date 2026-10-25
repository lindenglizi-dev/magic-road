"""对新完整层RTL运行严格门，测试夹具由验证分支独立更新。"""
import sys
import run


def main():
    run.check()
    work = run.fresh('rtl_gate')
    entry = f'import sys;sys.path.insert(0,{str(run.SKILL)!r});from scripts.python.validation.generated_deliverable_gate import main;raise SystemExit(main())'
    sources = {str(p): run.sha(p) for folder in ('rtl', 'reused') for p in (run.ROOT / folder).glob('*.v')}
    run.save(work / 'source_hashes.json', sources)
    external = []
    for path in (run.ROOT / 'shared_core_interface.v', run.ROOT / 'new_interfaces.v',
                 run.PROJECT / 'user_source/hdl_source/ph1p35_ddr/ddr2/ddr2.v',
                 run.ROOT.parent / 'board_selftest_20261010/rtl/road_selftest_display.v'):
        external += ['--external-interface-source', path]
    run.command([sys.executable, '-B', '-X', 'utf8', '-c', entry, run.ROOT / 'rtl', *external,
                 '--json', work / 'rtl.json', '--markdown', work / 'rtl.md'], work, 'gate', allowed=(0, 1, 2))
    assert (work / 'rtl.json').exists()
    assert all(run.sha(p) == h for p, h in sources.items())
    run.check()


if __name__ == '__main__':
    main()
