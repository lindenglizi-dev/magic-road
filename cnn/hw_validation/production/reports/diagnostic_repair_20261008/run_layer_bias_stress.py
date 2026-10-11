"""补强最终输出覆盖：同一RTL和测试量化，运行时装载更宽范围的合法偏置。"""
import importlib.util
import json
import sys
from execute import HERE, REPORTS, CORE, MODEL, MSIM, check, run, sha, write


def main():
    check()
    parent = HERE / 'layer'
    contract_check = '--contract' in sys.argv
    destination = parent / ('stress_bias_contract_host' if contract_check else
                            'stress_bias_host' if '--host' in sys.argv else 'stress_bias')
    destination.mkdir()
    vectors = destination / 'vectors'
    vectors.mkdir()
    reference = REPORTS / 'v8_reset_layer_tiles_20261007/layers/reference.py'
    spec = importlib.util.spec_from_file_location('tile_reference', reference)
    ref = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ref)

    def values(name, bits):
        raw = [int(line, 16) for line in (parent / 'vectors' / name).read_text().splitlines()]
        return [value - (1 << bits) if value & (1 << (bits - 1)) else value for value in raw]

    dw_weights = values('dw_weights.hex', 8)
    pw_weights = values('pw_weights.hex', 8)
    dw_bias = [(channel - 4) * 32768 for channel in range(16)]
    pw_bias = [(channel - 6) * 65536 for channel in range(24)]
    ref.dw_weights = lambda: dw_weights
    ref.pw_weights = lambda: pw_weights
    ref.dw_biases = lambda: dw_bias
    ref.pw_biases = lambda: pw_bias

    def quantize(acc, slot):
        pre = ref.round_shift(acc * 65536, 24)
        activated = ref.silu(pre)
        post = ref.round_shift(activated * 16777216, 31)
        return pre, activated, post, ref.sat8(post)

    ref.quantize = quantize

    def hexfile(name, entries, bits):
        with (vectors / name).open('x', encoding='ascii') as stream:
            mask = (1 << bits) - 1
            stream.write(''.join(f'{v & mask:0{bits // 4}x}\n' for v in entries))

    for name, entries, bits in [('silu.hex', ref.SILU, 16),
                               ('dw_weights.hex', dw_weights, 8), ('pw_weights.hex', pw_weights, 8),
                               ('dw_biases.hex', dw_bias, 32), ('pw_biases.hex', pw_bias, 32)]:
        hexfile(name, entries, bits)
    cases = []
    for name in ('edge', 'interior', 'bottom_right'):
        halo = values(name + '_halo.hex', 8)
        dw, dw_records = ref.depthwise(halo)
        pw, pw_records = ref.pointwise(dw)
        records = sorted(dw_records + pw_records, key=lambda r: (r['layer'], r['position'], r['channel']))
        assert len(records) == 640 and len(set(dw)) >= 8 and len(set(pw)) >= 8
        assert any(v != 0 for v in pw) and all(-2**31 <= r['acc'] < 2**31 for r in records)
        hexfile(name + '_halo.hex', halo, 8)
        hexfile(name + '_output.hex', pw, 8)
        hexfile(name + '_acc.hex', [r['acc'] for r in records], 32)
        hexfile(name + '_commit.hex', [r['output'] for r in records], 32)
        hexfile(name + '_stages.hex', [v for r in records for v in (r['pre'], r['silu'], r['post'])], 32)
        cases.append({'name': name, 'dw_distinct': len(set(dw)), 'pw_distinct': len(set(pw)),
                      'pw_nonzero': sum(v != 0 for v in pw), 'pw_range': [min(pw), max(pw)]})
    write(vectors / 'manifest.json', {
        'scope': 'Additional synthetic bias regression; package weights and quantization retained',
        'biases_are_original_package': False, 'cases': cases,
        'files': {p.name: sha(p) for p in sorted(vectors.iterdir()) if p.is_file()}})
    tb = parent / ('tb_down2_dynamic_tile_contract.v' if contract_check else 'tb_down2_dynamic_tile_phases.v')
    sources = [parent / 'rtl/down2_dynamic_tile_runner.v', parent / 'rtl/road_down2_dynamic_adapter.v',
               parent / 'rtl/road_mac_probe.v', *[HERE / 'hardware' / name for name in CORE],
               HERE / 'model' / MODEL, tb]
    before = {str(p): sha(p) for p in sources}
    run([MSIM / 'vlib.exe', 'work'], destination, 'vlib.log')
    run([MSIM / 'vlog.exe', '-work', 'work', *sources], destination, 'vlog.log')
    run([MSIM / 'vsim.exe', '-c', '-lib', 'work', tb.stem, '-do',
         'onerror {quit -code 1}; onbreak {quit -code 1}; run -all; quit -code 0'], destination, 'simulation.log')
    log = (destination / 'simulation.log').read_text()
    assert 'TB_PASS_DOWN2_DYNAMIC_TILE' in log and 'Fatal:' not in log and '** Error:' not in log
    assert before == {str(p): sha(p) for p in sources}
    check()
    write(destination / 'receipt.json', {'status': 'NONZERO_TILE_STRESS_PASS', 'cases': cases,
          'sources': before, 'reference_sha256': sha(reference), 'rtl_unchanged': True,
          'parameters': 'Same fixed TEST multipliers/shifts; biases supplied via existing loader',
          'coverage': 'Seven runs: 640 accumulators, 1920 intermediate values, 640 unique commits, 384 exports per run',
          'physical_or_accuracy_signoff': False})
    print('NONZERO_TILE_STRESS_PASS', cases, flush=True)


if __name__ == '__main__':
    main()
