"""Update only measured layer projections; other layers keep explicit lower bounds."""
import csv
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DESCRIPTORS = ROOT.parent / 'fixed_graph_function_20261008/fixed_layer_descriptors.json'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    graph = json.loads(DESCRIPTORS.read_text(encoding='utf-8'))
    receipt = json.loads((ROOT / 'tests/layer/receipt.json').read_text(encoding='utf-8'))
    with (ROOT / 'tests/layer/original_cycles.csv').open(encoding='utf-8') as stream:
        measured = next(csv.DictReader(stream))
    assert int(measured['endpoint']) == 3203
    assert int(measured['dw_endpoint']) + int(measured['pw_endpoint']) == 3203
    measured_names = {'down2.dw.conv': 'dw_endpoint', 'down2.pw.conv': 'pw_endpoint'}
    layers = []
    for layer in graph['layers']:
        samples = math.prod(layer['output_hwc'])
        macs = samples * layer['terms_per_output']
        mac_lower_bound = (macs + 23) // 24
        # Independent PRE/POST engines and a scalar SiLU each have II=1.
        # This is work capacity, not endpoint latency or an actual schedule.
        scalar_work_lower_bound = samples
        tile_projection = None
        if layer['name'] in measured_names:
            assert layer['output_hwc'][2] == (16 if layer['op'] == 'DW' else 24)
            tile_projection = layer['tile_rows'] * layer['tile_columns'] * int(
                measured[measured_names[layer['name']]])
        layers.append({
            'name': layer['name'], 'op': layer['op'], 'output_hwc': layer['output_hwc'],
            'activate': layer['activate'], 'macs': macs,
            'ideal_24mac_work_lower_bound_cycles': mac_lower_bound,
            'ideal_scalar_postprocess_work_lower_bound_cycles': scalar_work_lower_bound,
            'sequential_layer_ideal_lower_bound_cycles': max(mac_lower_bound, scalar_work_lower_bound),
            'measured_4x4_tile_endpoint_cycles': int(measured[measured_names[layer['name']]])
                if tile_projection is not None else None,
            'conditional_frame_tile_projection_cycles': tile_projection,
            'projection_excludes': ['DDR/DMA', 'preload/export', 'real QAT', 'cross-tile handoff']
                if tile_projection is not None else ['not measured on this shape'],
        })
    assert len(layers) == 67 and sum(row['macs'] for row in layers) == 214465536
    report = {
        'status': 'TWO_SHAPES_MEASURED_OTHER_65_UNMEASURED_NOT_5FPS_PROOF',
        'graph_sha256': graph['graph_sha256'], 'descriptors_sha256': sha(DESCRIPTORS),
        'layer_receipt_sha256': sha(ROOT / 'tests/layer/receipt.json'),
        'source_hashes': receipt['sources_after'], 'clock_hz': 100000000,
        'target_frame_cycles': 20000000,
        'activated_samples': sum(math.prod(layer['output_hwc']) for layer in graph['layers'] if layer['activate']),
        'raw_samples': sum(math.prod(layer['output_hwc']) for layer in graph['layers'] if not layer['activate']),
        'sum_sequential_layer_ideal_lower_bounds_cycles': sum(row['sequential_layer_ideal_lower_bound_cycles'] for row in layers),
        'measured_small_block': {'old_serial_cycles': 20633, 'frozen_overlap_cycles': 3331,
                                 'new_cycles': 3203, 'dw': 1887, 'pw': 1316},
        'sum_two_measured_shapes_conditional_projection_cycles': sum(
            row['conditional_frame_tile_projection_cycles'] or 0 for row in layers),
        'full_frame_prediction_cycles': None,
        'reason_no_full_prediction': 'Two layer shapes cannot calibrate 65 unmeasured shapes. Pipeline busy durations overlap; neither their sum nor the measured tile speedup is a frame estimate.',
        'layers': layers,
    }
    target = ROOT / 'layer_cycle_budget.json'
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('BUDGET_PASS layers=67 measured_shapes=2 remaining_shapes=65',
          'two_shape_projection=', report['sum_two_measured_shapes_conditional_projection_cycles'],
          'ideal_lower_bound=', report['sum_sequential_layer_ideal_lower_bounds_cycles'])


if __name__ == '__main__':
    main()
