"""Update the frozen graph's conditional cadence ledger, not measured FPS."""

import hashlib
import json
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[1]
    production = root.parents[1]
    previous = production / 'reports/v10_postprocess_overlap_20261007/verification/budget/shape_budget.json'
    graph_path = production / 'graph_artifacts/graph.json'
    graph_raw = graph_path.read_bytes()
    graph = json.loads(graph_raw)
    old = json.loads(previous.read_text(encoding='utf-8'))
    assert hashlib.sha256(graph_raw).hexdigest() == old['source']['sha256']
    nodes = {node['name']: node for node in graph['nodes']}
    rows = []
    for layer in old['layers']:
        boundary = layer['conditional_layer_boundary_cycles'] + int(layer['activated_silu'])
        before = after = layer['fitted_job_cadence_cycles_2G_plus_10']
        triplets = 0
        if layer['kind'] == 'depthwise':
            height, width, channels = layer['output_hwc']
            assert width % 4 == 0
            stride = nodes[layer['name']]['stride']
            assert stride in ([1, 1], [2, 2])
            groups = 2 if stride == [1, 1] else 3
            triplets = height * (width // 4) * channels
            # Each four-pixel row segment is one spatial triple and one tail.
            before = after = triplets * (2 * (2 * groups + 10) + 3 + 1)
        elif layer['kind'] == 'pointwise' and layer['input_hwc'][2] == 16:
            # Only the fixed Cin16, G2 PW prefetch has a candidate here.
            after = before - layer['mac_jobs']
        rows.append({'name': layer['name'], 'kind': layer['kind'],
                     'output_hwc': layer['output_hwc'],
                     'v16_conditional_cycles': before + boundary,
                     'v17_conditional_cycles': after + boundary,
                     'conditional_saved_cycles': before - after,
                     'spatial_triplets': triplets,
                     'measured_scope': 'down2 4x4 only; all other layer shapes are unmeasured'})
    assert len(rows) == 67
    # Shape-only H24 comparison; no model, checkpoint or RTL is changed.
    h24_cycles = h24_macs = h24_weights = h24_biases = 0
    for layer in old['layers']:
        name = layer['name']
        height, width, cout = layer['output_hwc']
        cin = layer['input_hwc'][2]
        if name.startswith('head'):
            if '.stem.' not in name:
                cin = 24
            if not name.endswith(('cls_out', 'reg_out')):
                cout = 24
        kh, kw = layer['kernel']
        terms = kh * kw * (1 if layer['kind'] == 'depthwise' else cin)
        h24_macs += height * width * cout * terms
        h24_weights += cout * terms
        h24_biases += cout
        if layer['kind'] == 'depthwise':
            groups = 2 if nodes[name]['stride'] == [1, 1] else 3
            cycles = height * (width // 4) * cout * (2 * (2 * groups + 10) + 4)
        else:
            groups = (terms + 7) // 8
            cycles = height * width * ((cout + 2) // 3) * (
                2 * groups + 10 - int(layer['kind'] == 'pointwise' and cin == 16))
        h24_cycles += cycles + layer['conditional_layer_boundary_cycles'] + int(layer['activated_silu'])
    assert (h24_macs, h24_weights, h24_biases) == (156114432, 96900, 2141)
    report = {'status': 'CONDITIONAL_CADENCE_ONLY_NOT_FULL_FRAME_MEASUREMENT',
              'graph_sha256': hashlib.sha256(graph_raw).hexdigest(),
              'base_ledger_sha256': hashlib.sha256(previous.read_bytes()).hexdigest(),
              'excluded': ['DDR', 'non-convolution ops', 'NMS', 'dynamic quantization',
                           'preload/export', 'per-tile drain and DMA overhead'],
              'assumptions': ['Stride1 packing is not measured by the down2 stride2 probe.',
                              'Per-layer tails reuse old calibrated conditional constants.',
                              'No data reuse, port, physical or full-frame throughput proof.'],
              'v16_conditional_cycles': sum(row['v16_conditional_cycles'] for row in rows),
              'v17_conditional_cycles': sum(row['v17_conditional_cycles'] for row in rows),
              'conditional_saved_cycles': sum(row['conditional_saved_cycles'] for row in rows),
              'target_5fps_cycles': 20000000,
              'h24_shape_only_comparison': {
                  'conditional_cycles': h24_cycles, 'macs': h24_macs,
                  'weights': h24_weights, 'biases': h24_biases,
                  'implemented_trained_or_measured': False,
                  'note': 'Reuse unverified cadence/tail assumptions; no accuracy or throughput proof.'},
              'layers': rows}
    (root / 'verification/layer_cycle_budget.json').write_text(
        json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({key: value for key, value in report.items() if key != 'layers'}))


if __name__ == '__main__':
    main()
