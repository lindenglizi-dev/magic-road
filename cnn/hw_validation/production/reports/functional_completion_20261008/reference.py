"""动态重定标契约与可复现向量；输出仅限本候选目录。"""
import hashlib
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / 'v19_mac_short_closure_20261008/rtl'


def requant(accumulator, multiplier, shift):
    if not -(1 << 31) <= accumulator < 1 << 31 or not 0 <= multiplier < 1 << 31:
        raise ValueError('INT32 accumulator and nonnegative INT32 multiplier required')
    if not 0 <= shift <= 62:
        return 0, 1
    product = accumulator * multiplier
    magnitude = abs(product)
    quotient, remainder = divmod(magnitude, 1 << shift)
    if shift and (remainder > (1 << (shift - 1)) or
                  remainder == (1 << (shift - 1)) and quotient & 1):
        quotient += 1
    rounded = -quotient if product < 0 else quotient
    return max(-32768, min(32767, rounded)), 0


def main():
    assert requant(5, 1, 1) == (2, 0)
    assert requant(7, 1, 1) == (4, 0)
    assert requant(-5, 1, 1) == (-2, 0)
    assert requant(-7, 1, 1) == (-4, 0)
    paths = sorted(BASE.glob('*.v'))
    frozen = {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}
    manifest = ROOT / 'baseline_hashes.json'
    if manifest.exists():
        assert json.loads(manifest.read_text()) == frozen, 'v19 frozen RTL changed'
    else:
        manifest.write_text(json.dumps(frozen, indent=2), encoding='utf-8')
    rng = random.Random(42)
    cases = [(acc, mul, shift) for acc in (-2147483648, -65537, -7, -5, -1, 0, 1, 5, 7, 65535, 2147483647)
             for mul in (0, 1, 3, 65535, 65536, 2147483647) for shift in (0, 1, 15, 31, 62, 63)]
    cases += [(rng.randrange(-(1 << 31), 1 << 31), rng.randrange(1 << 31), rng.randrange(64))
              for _ in range(2000)]
    lines = []
    for tag, (acc, mul, shift) in enumerate(cases):
        value, fault = requant(acc, mul, shift)
        packed = ((acc & 0xffffffff) << 80 | mul << 48 | shift << 40 |
                  tag << 24 | (value & 0xffff) << 8 | fault)
        lines.append(f'{packed:028x}')
    (ROOT / 'vectors.hex').write_text('\n'.join(lines) + '\n', encoding='ascii')
    (ROOT / 'vector_count.vh').write_text(f'`define VECTOR_COUNT {len(cases)}\n', encoding='ascii')
    ports = [('i_clk', 1, 'clock'), ('i_rstn', 1, 'reset'),
             ('i_input_valid', 1, 'input_valid'), ('i_accumulator', 32, 'accumulator'),
             ('i_multiplier', 31, 'multiplier'), ('i_shift', 6, 'shift'), ('i_tag', 16, 'tag'),
             ('o_input_ready', 1, 'input_ready'), ('i_output_ready', 1, 'output_ready'),
             ('o_output_valid', 1, 'output_valid'), ('o_output_data', 16, 'data'),
             ('o_output_tag', 16, 'tag'), ('o_fault', 1, 'fault')]
    contract = {'modules': [{'name': 'road_dynamic_requant', 'feature': 'dynamic_requant',
        'rtl_path': 'road_dynamic_requant.v',
        'description': 'Runtime INT32 times UINT31 followed by frozen RNE/saturating INT16 round pipeline.',
        'interfaces': {'protocol': 'ready_valid', 'ports': [
            dict(name=name, direction='input' if name.startswith('i_') else 'output',
                 width=width, role=role, description=role, clock_domain='i_clk') for name, width, role in ports],
            'handshake_channels': [
                {'id': 'input', 'valid': 'i_input_valid', 'ready': 'o_input_ready',
                 'payload': ['i_accumulator', 'i_multiplier', 'i_shift', 'i_tag']},
                {'id': 'output', 'valid': 'o_output_valid', 'ready': 'i_output_ready',
                 'payload': ['o_output_data', 'o_output_tag', 'o_fault']}]},
        'parameters': [], 'clock': {'name': 'i_clk', 'edge': 'posedge', 'frequency_hz': 100000000},
        'reset': {'name': 'i_rstn', 'active': 'low', 'synchronous': False,
                  'values': 'Cancel product and round valid immediately. Upstream provides synchronized release.'},
        'behavior': ['Input consumption requires valid and ready; all coefficients and tag captured atomically.',
                     'One product register feeds the unchanged nine-stage round kernel.',
                     'Output visible nine rising-edge intervals after input acceptance without stalls; earliest ACK ten intervals.',
                     'II one within this scalar stream; an output stall freezes the complete pipeline.',
                     'Shift63 returns zero and fault; shift0..62 uses RNE and INT16 saturation.'],
        'constraints': ['Nonnegative INT32 multipliers only; no SiLU, INT8 saturation, ROM or DDR in this module.',
                        'Direct multiplication is a functional baseline, not a three-DSP mapping claim.'],
        'corner_cases': ['Negative ties, zero multiplier, extreme INT32 products, shift63 fault, reset under stall.'],
        'verification_cases': ['2396 vectors, continuous input, random bubbles, long output stall, in-flight reset.'],
        'timing_diagrams': [{'id': 'held_result', 'title': 'Whole-pipeline output backpressure',
            'scenario': 'held-result', 'description': 'Contract illustration; output payload remains held before ACK.',
            'wavejson': {'signal': [{'name': 'i_clk', 'wave': 'p...............'},
                {'name': 'i_input_valid', 'wave': '010.............'},
                {'name': 'o_input_ready', 'wave': '1.........0..1..'},
                {'name': 'o_output_valid', 'wave': '0.........1...0.'},
                {'name': 'o_output_data', 'wave': 'x.........3.....', 'data': ['result']},
                {'name': 'i_output_ready', 'wave': '0............1..'}]}}]}]}
    (ROOT / 'road_dynamic_requant.contract.json').write_text(json.dumps(contract, indent=2), encoding='utf-8')
    print(f'REFERENCE_PASS vectors={len(cases)} baseline_files={len(frozen)}')


if __name__ == '__main__':
    main()
