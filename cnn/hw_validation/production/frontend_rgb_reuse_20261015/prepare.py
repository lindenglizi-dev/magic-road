"""Copy only the frozen full-frontend closure; never write the baseline."""
import json
import shutil
import run


def main():
    root, base = run.ROOT, run.BASE
    assert not (root / 'frozen.json').exists()
    paths = [p for folder in ('rtl', 'reused', 'vectors', 'build', 'reference', 'tests')
             for p in (base / folder).rglob('*') if p.is_file()]
    paths += [base / name for name in ('run.py', 'verification/run_verify.py', 'comparison.json',
              'verification/suite_manifest.json', 'physical/pr.db', 'physical/source_hashes.json',
              'physical/board.sdc', 'physical/resolved_display.sdc', 'physical/ddr2/src/sdc/ddr2.sdc',
              'shared_core_interface.v', 'new_interfaces.v', 'dependency_preflight.json')]
    frozen = {str(p): run.sha(p) for p in paths}
    frozen.update(json.loads((base / 'physical/source_hashes.json').read_text(encoding='utf-8')))
    assert all(run.sha(p) == h for p, h in frozen.items())
    run.save(root / 'frozen.json', frozen)
    for folder in ('rtl', 'reused', 'vectors', 'build', 'reference', 'tests'):
        shutil.copytree(base / folder, root / folder)
    (root / 'verification').mkdir()
    shutil.copyfile(base / 'verification/run_verify.py', root / 'verification/run_verify.py')
    for name in ('shared_core_interface.v', 'new_interfaces.v', 'dependency_preflight.json'):
        shutil.copyfile(base / name, root / name)
    run.save(root / 'reused_sources.json', {str(p): run.sha(p) for p in (root / 'reused').glob('*.v')})
    run.save(root / 'status.json', {'stage': 'BASELINE_FROZEN_S1_PENDING', 'physical_started': False,
        'bitstream_generated': False, 'board_run': False, 'production_modified': False})
    run.check()
    print('S1_FROZEN_BASE_PREPARED', flush=True)


if __name__ == '__main__':
    main()
