"""三通道功能诊断：复用部署整数参考，不导入训练或修改旧候选。"""
import hashlib
import importlib.util
import json
from pathlib import Path
import random

import numpy as np

ROOT = Path(__file__).resolve().parent
PRODUCTION = ROOT.parents[1]
CNN = PRODUCTION.parents[1]


def main():
    spec = importlib.util.spec_from_file_location('road_integer', CNN / 'integer.py')
    integer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(integer)
    frozen_paths = [PRODUCTION / 'reports/functional_completion_20261008/road_dynamic_requant.v',
                    PRODUCTION / 'reports/v19_mac_short_closure_20261008/rtl/road_round_shift.v',
                    PRODUCTION / 'reports/v19_mac_short_closure_20261008/rtl/silu_shared_unit.v',
                    PRODUCTION / 'reports/v19_mac_short_closure_20261008/rtl/road_mac_probe.v',
                    CNN / 'integer.py']
    hashes = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in frozen_paths}
    receipt = ROOT / 'frozen_dependencies.json'
    if receipt.exists():
        assert json.loads(receipt.read_text(encoding='utf-8')) == hashes
    else:
        receipt.write_text(json.dumps(hashes, indent=2), encoding='utf-8')
    table = integer.tables()['silu']
    (ROOT / 'table.hex').write_text(''.join(f'{int(v) & 65535:04x}\n' for v in table), encoding='ascii')
    rng = random.Random(42)
    cases = []
    # 第一批逐项验证尾部、负数中点和 SiLU 上端点。
    for mode in (0, 1):
        for value in (-32768, -2049, -2048, -7, -5, -1, 0, 1, 5, 7, 2045, 2046, 2047, 2048, 32767):
            cases.append((mode, 7, [value, value + 1, value - 1], [1, 3, 5], [0, 1, 2], 1, 0))
    for _ in range(300):
        cases.append((rng.randrange(2), rng.randrange(1, 8),
                      [rng.randrange(-(1 << 31), 1 << 31) for _ in range(3)],
                      [rng.randrange(1 << 31) for _ in range(3)],
                      [rng.randrange(63) for _ in range(3)], rng.randrange(1 << 31), rng.randrange(63)))
    lines = []
    expected = []
    for batch, (mode, mask, accumulators, multipliers, shifts, post_mul, post_shift) in enumerate(cases):
        tags = [3 * batch + lane for lane in range(3)]
        results = []
        for lane in range(3):
            pre = integer.requantize(np.array(accumulators[lane]), multipliers[lane], shifts[lane], -32768, 32767)
            if mode:
                activated = integer.silu(pre)
                result = integer.requantize(activated, post_mul, post_shift)
            else:
                result = pre
            results.append(int(result))
            if mask & (1 << lane):
                expected.append((tags[lane], int(result), 1 - mode))
        pack = lambda values, bits: sum((v & ((1 << bits) - 1)) << (bits * i) for i, v in enumerate(values))
        lines.append(' '.join(f'{v:x}' for v in (pack(accumulators, 32), pack(multipliers, 32),
                    pack(shifts, 6), post_mul, post_shift, mode, mask, pack(tags, 16), pack(results, 16))))
    (ROOT / 'batches.txt').write_text('\n'.join(lines) + '\n', encoding='ascii')
    (ROOT / 'expected.json').write_text(json.dumps(expected), encoding='utf-8')
    (ROOT / 'counts.vh').write_text(f'`define BATCH_COUNT {len(cases)}\n', encoding='ascii')
    ports = [('i_clk', 1), ('i_rstn', 1), ('i_table_valid', 1), ('i_table_addr', 10),
             ('i_table_data', 16), ('o_table_ready', 1), ('o_table_loaded', 1),
             ('i_input_valid', 1), ('i_accumulators', 96), ('i_pre_multipliers', 96),
             ('i_pre_shifts', 18), ('i_post_multiplier', 32), ('i_post_shift', 6),
             ('i_activate', 1), ('i_lane_mask', 3), ('i_tags', 48), ('i_input_fault', 1),
             ('o_input_ready', 1), ('i_output_ready', 1), ('o_output_valid', 1),
             ('o_output_data', 16), ('o_output_tag', 16), ('o_output_int16', 1), ('o_fault', 1)]
    contract = {'modules': [{'name': 'road_dynamic_postprocess', 'feature': 'dynamic_postprocess',
        'rtl_path': 'road_dynamic_postprocess.v', 'description': 'Diagnostic single-batch three-lane dynamic quantization and optional SiLU with atomic cached publication.',
        'interfaces': {'protocol': 'ready_valid', 'ports': [dict(name=name, width=width,
            direction='input' if name.startswith('i_') else 'output', role=name,
            description=name, clock_domain='i_clk') for name, width in ports],
            'handshake_channels': [
                {'id': 'table', 'valid': 'i_table_valid', 'ready': 'o_table_ready', 'payload': ['i_table_addr', 'i_table_data']},
                {'id': 'batch', 'valid': 'i_input_valid', 'ready': 'o_input_ready', 'payload':
                 ['i_accumulators', 'i_pre_multipliers', 'i_pre_shifts', 'i_post_multiplier', 'i_post_shift', 'i_activate', 'i_lane_mask', 'i_tags', 'i_input_fault']},
                {'id': 'result', 'valid': 'o_output_valid', 'ready': 'i_output_ready',
                 'payload': ['o_output_data', 'o_output_tag', 'o_output_int16']}]},
        'parameters': [], 'clock': {'name': 'i_clk', 'edge': 'posedge', 'frequency_hz': 100000000},
        'reset': {'name': 'i_rstn', 'active': 'low', 'synchronous': False,
            'values': 'Cancel batch and all child valid immediately; clear fatal and require all 1024 table entries again. Caller synchronizes release.'},
        'behavior': ['A batch transfers only on valid and ready; capture all three coefficients, shifts, accumulators and opaque tags together.',
            'Input ready remains zero until sequential table addresses 0..1023 have transferred.',
            'Process active lanes in ascending order with one shared quantizer: pre quantization, optional SiLU, optional post quantization.',
            'Activated output is signed INT8 represented by sign extension into INT16; prediction output retains signed INT16 and bypasses SiLU and post quantization.',
            'Cache all active results before publishing the first; sticky fault suppresses the complete batch until reset.',
            'Output payload and valid hold under backpressure. Variable batch latency; no frame-throughput claim.'],
        'constraints': ['Diagnostic functional baseline, not a throughput replacement for frozen v19.',
            'Only active lanes require legal pre multipliers and shift0..62; post parameter legality applies only to activated batches.',
            'No ROM parameter loader, DDR, model weights, bitstream or real board validation in this module.'],
        'corner_cases': ['Zero mask faults; any input MAC fault prevents publication; bad last-lane parameter faults before any scalar starts.',
            'Reset in all eight active states; partial table reset; table sequence fault; output stall and poison live input ports after acceptance.'],
        'verification_cases': ['330 batches and 604 outputs compared against existing cnn/integer.py.',
            'Eight active-state resets, partial table load, six atomic batch faults, clean recovery output and wrong table address.'],
        'timing_diagrams': [{'id': 'atomic_batch', 'title': 'Batch capture and held scalar publication',
            'scenario': 'atomic-batch', 'description': 'Illustrative compressed timeline, compute interval is not one clock and no fixed batch latency is implied.',
            'wavejson': {'signal': [{'name': 'i_clk', 'wave': 'p...........'},
                {'name': 'i_input_valid', 'wave': '010.........'},
                {'name': 'o_input_ready', 'wave': '110........1'},
                {'name': 'phase', 'wave': '23...4...5.2', 'data': ['idle', 'compute all lanes', 'held alpha', 'emit beta/gamma', 'idle']},
                {'name': 'o_output_valid', 'wave': '0....1....0.'},
                {'name': 'i_output_ready', 'wave': '0.......1...'},
                {'name': 'o_output_tag', 'wave': 'x....3...45x', 'data': ['alpha', 'beta', 'gamma']}]}}]}]}
    (ROOT / 'road_dynamic_postprocess.contract.json').write_text(json.dumps(contract, indent=2), encoding='utf-8')
    print(f'REFERENCE_PASS batches={len(cases)} outputs={len(expected)} frozen={len(hashes)}')
    result_file = ROOT / 'results.csv'
    if result_file.exists():
        actual = [tuple(map(int, line.split(','))) for line in result_file.read_text().splitlines()]
        assert actual == expected, 'Exported RTL results differ from the existing integer reference'
        print(f'EXPORT_COMPARE_PASS outputs={len(actual)}')
    for name in ('road_dynamic_requant.v', 'road_round_shift.v', 'silu_shared_unit.v'):
        copy = ROOT / 'dependencies' / name
        if copy.exists():
            original = next(path for path in frozen_paths if path.name == name)
            assert copy.read_bytes() == original.read_bytes(), name
    return integer


if __name__ == '__main__':
    main()
