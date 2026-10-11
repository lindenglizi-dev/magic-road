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
            before = triplets * (2 * (2 * groups + 10) + 5 + 1)
            after = triplets * (2 * (2 * groups + 10) + 3 + 1)
        rows.append({'name': layer['name'], 'kind': layer['kind'],
                     'output_hwc': layer['output_hwc'],
                     'v15_conditional_cycles': before + boundary,
                     'v16_conditional_cycles': after + boundary,
                     'conditional_saved_cycles': before - after,
                     'spatial_triplets': triplets,
                     'measured_scope': 'down2 4x4 only; all other layer shapes are unmeasured'})
    assert len(rows) == 67
    report = {'status': 'CONDITIONAL_CADENCE_ONLY_NOT_FULL_FRAME_MEASUREMENT',
              'graph_sha256': hashlib.sha256(graph_raw).hexdigest(),
              'base_ledger_sha256': hashlib.sha256(previous.read_bytes()).hexdigest(),
              'excluded': ['DDR', 'non-convolution ops', 'NMS', 'dynamic quantization',
                           'preload/export', 'per-tile drain and DMA overhead'],
              'assumptions': ['Stride1 packing is not measured by the down2 stride2 probe.',
                              'Per-layer tails reuse old calibrated conditional constants.',
                              'No data reuse, port, physical or full-frame throughput proof.'],
              'v15_conditional_cycles': sum(row['v15_conditional_cycles'] for row in rows),
              'v16_conditional_cycles': sum(row['v16_conditional_cycles'] for row in rows),
              'conditional_saved_cycles': sum(row['conditional_saved_cycles'] for row in rows),
              'target_5fps_cycles': 20000000, 'layers': rows}
    (root / 'verification/layer_cycle_budget.json').write_text(
        json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({key: value for key, value in report.items() if key != 'layers'}))


if __name__ == '__main__':
    main()
