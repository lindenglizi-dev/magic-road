"""逐端口声明的最小适配修正：同向量回归和严格门禁，保存原失败。"""
import json
import shutil
import sys
from execute import HERE, CORE, MODEL, PROJECT, MSIM, run, check, sha, write


def main():
    check()
    layer = HERE / 'layer'
    d = layer / 'declared_validation'
    d.mkdir()
    shutil.copytree(layer / 'stress_bias_contract_host/vectors', d / 'vectors')
    rtl = layer / 'rtl_declared'
    original = (layer / 'rtl/road_down2_dynamic_adapter.v').read_text()
    candidate = (rtl / 'road_down2_dynamic_adapter.v').read_text()
    assert original[original.index('    reg flag_pending;'):] == candidate[candidate.index('    reg flag_pending;'):]
    for name in ('down2_dynamic_tile_runner.v', 'road_mac_probe.v'):
        assert sha(rtl / name) == sha(layer / 'rtl' / name)
    inputs = d / 'gate_inputs'
    inputs.mkdir()
    sources = [*sorted(rtl.glob('*.v')), *[HERE / 'hardware' / name for name in CORE]]
    for source in sources:
        shutil.copy2(source, inputs / source.name)
    run([MSIM / 'vlib.exe', 'work'], d, 'vlib.log')
    tb = layer / 'tb_down2_dynamic_tile_contract.v'
    run([MSIM / 'vlog.exe', '-work', 'work', *sources, HERE / 'model' / MODEL, tb], d, 'vlog.log')
    run([MSIM / 'vsim.exe', '-c', '-lib', 'work', tb.stem, '-do',
         'onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0'], d, 'simulation.log')
    log = (d / 'simulation.log').read_text()
    assert 'TB_PASS_DOWN2_DYNAMIC_TILE' in log and 'Fatal:' not in log and '** Error:' not in log
    assert (d / 'layer_cycles.csv').read_bytes() == (layer / 'stress_bias_contract_host/layer_cycles.csv').read_bytes()
    interface = PROJECT / 'cnn/hw_validation/interfaces/ph1p_eram_interface_complete.v'
    code = run([sys.executable, '-B', '-X', 'utf8', '-m',
        'scripts.python.validation.generated_deliverable_gate', inputs,
        '--external-interface-source', interface, '--json', d / 'gate.json',
        '--markdown', d / 'gate.md'], d, 'gate.log', allowed=(0, 1))
    gate = json.loads((d / 'gate.json').read_text())
    assert gate['checks']['compile']['status'] == 'passed', gate['checks']['compile']
    check()
    write(d / 'receipt.json', {'status': 'DECLARATION_REPAIR_FUNCTION_PASS_STRICT_FAILED',
        'module_body_identical': True, 'same_vectors_cycles': True,
        'sources': {str(p): sha(p) for p in [*sources, HERE / 'model' / MODEL, tb]},
        'errors': gate['errors'], 'strict_warnings': gate['strict_warnings'],
        'gate_exit_code': code, 'checks': {k: v['status'] for k, v in gate['checks'].items()},
        'physical_layout_performed': False})
    print('DECLARED_INTERFACE_PASS', gate['errors'], gate['strict_warnings'], flush=True)


if __name__ == '__main__':
    main()
