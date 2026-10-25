"""循环命令、原13例和原双时钟周期的窄范围回归。"""
import json
import shutil
import sys
import run


def main():
    run.check()
    work = run.fresh('loader_simulation')
    for name in ('program.hex', 'loop_table.hex', 'loop_parameters.hex', 'loop_pixels.hex'):
        shutil.copyfile(run.ROOT / 'vectors' / name, work / name)
    sources = [run.ROOT / 'rtl/road_frontend_load_sequence.v', run.ROOT / 'tests/tb_frontend_load_sequence.v']
    run.command([run.MSIM / 'vlib.exe', 'work'], work, 'vlib')
    run.command([run.MSIM / 'vlog.exe', '-work', 'work', *sources], work, 'vlog')
    output = run.command([run.MSIM / 'vsim.exe', '-c', '-lib', 'work', 'tb_frontend_load_sequence', '-do',
        'onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0'], work, 'vsim')
    assert 'LOOP_COMMAND_PASS comparisons=17704 ' in output
    run.save(work / 'receipt.json', {'passed': True, 'command_comparisons': 17704, 'full_runs': 2,
        'reset_mid_parameter': True, 'source_hashes': {str(p): run.sha(p) for p in sources}})
    run.command([sys.executable, '-B', '-X', 'utf8', run.ROOT / 'sequence_verification/run_verify.py'], run.ROOT, 'direct_regression')
    current = json.loads((run.ROOT / 'sequence_verification/receipts/manifest.json').read_text(encoding='utf-8'))
    baseline = json.loads((run.BASE / 'sequence_verification/receipts/manifest.json').read_text(encoding='utf-8'))
    assert current['result'] == 'PASS_13_OF_13' and current['case_cycles'] == baseline['case_cycles']
    run.integrated()
    current_integrated = json.loads((run.ROOT / 'integrated_simulation/receipt.json').read_text(encoding='utf-8'))
    old_integrated = json.loads((run.BASE / 'integrated_simulation/receipt.json').read_text(encoding='utf-8'))
    assert current_integrated['results'] == old_integrated['results']
    run.save(run.ROOT / 'functional_comparison.json', {'passed': True, 'all_13_case_cycles_identical': True,
        'case_cycles': current['case_cycles'], 'integrated_cycles_identical': True,
        'loader': str(work / 'receipt.json'), 'source_hashes': current_integrated['source_hashes']})
    run.check()
    print('LOOP_FULL_FUNCTIONAL_PASS same 13 cases and integrated cycles', flush=True)


if __name__ == '__main__':
    main()
