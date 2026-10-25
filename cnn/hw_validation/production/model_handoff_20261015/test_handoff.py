"""Read-only CPU regression of the published model handoff, including negative checks."""
from pathlib import Path
import json
import time
from unittest.mock import patch

import handoff as h


def main():
    started = time.perf_counter()
    front, runtime = h.initialize()
    import numpy as np
    from cnn.hw_validation.production import trained_integer as ti
    from cnn.hw_validation.production.export_qat_csp_first import halo_window
    from cnn.integer import tables
    model, manifest, _ = h.pinned_inputs(front)
    index = h.read(h.OUT / 'artifacts/layer_parameter_index.json')
    prefix = h.read(h.OUT / 'artifacts/golden_prefix_index.json')
    assert len(index['layers']) == 67 and index['canonical_package'] == str(h.PACKAGE)
    physical = (h.PACKAGE / 'numeric_test_padded.bin').read_bytes()
    assert front.word_bytes(physical, 19, 3) == physical[19:22]
    assert front.word_bytes(physical, 10239, 3) == physical[10239:10242]
    end = 0
    for segment in manifest['segments']:
        assert segment['offset'] == end
        data = front.word_bytes(physical, end, segment['length'])
        assert h.hashlib.sha256(data).hexdigest() == segment['sha256']
        end += len(data)
    assert end == 140522
    heads = [row for row in index['layers'] if row['output_dtype'] == 'int16_q7_8']
    assert len(heads) == 6
    assert all(row['output_scale'] == 1/256 and not any(field.startswith('post_') for field in row['fields'])
               and row['postprocess_mode'] == 'RAW_INT16_NO_SILU_NO_POST' for row in heads)
    bounds = {}
    for name, p in model.parameters.items():
        bound = np.abs(p['bias'].astype(np.int64)) + 128*np.abs(p['weights'].astype(np.int64)).sum((1, 2, 3))
        bounds[name] = int(bound.max())
        assert np.all(bound < 1 << 31)
    folder = h.OUT / 'artifacts/golden_prefix'
    rgb = np.load(folder / 'input_rgb_hwc.npy', allow_pickle=False)
    assert rgb.dtype == np.uint8 and rgb.shape == (288, 512, 3)
    assert (folder / 'input_rgb_nhwc.bin').read_bytes() == rgb.tobytes()
    values = {'input': (rgb.astype(np.int16)-128).astype(np.int8)}
    checks = []
    for node in model.graph['nodes'][:12]:
        name = node['name']
        if node['op'] != 'conv':
            values.update(ti.nonconv(node, values))
            continue
        stages = front.stage(values[node['inputs'][0]], model.parameters[name], tables()['silu'],
                             manifest['silu_upper'], node['stride'][0], node['padding'][0], node['groups'])
        for suffix, array in zip(('acc', 'pre', 'silu', 'post'), stages, strict=True):
            expected = np.load(folder / f'{name}.{suffix}.npy', allow_pickle=False)
            np.testing.assert_array_equal(array, expected)
            checks.append(dict(node=name, stage=suffix, values=int(array.size), exact=True))
        values[name] = stages[-1]
        packed = (folder / f'{name}.tile4x4_hwc.bin').read_bytes()
        assert len(packed) == node['storage']['raw_bytes']
        hgt, width, channels = stages[-1].shape
        for y, x, c in ((0, 0, 0), (hgt-1, width-1, channels-1), (4, 4, channels//2)):
            offset = (((y//4)*((width+3)//4)+x//4)*16+(y%4)*4+x%4)*channels+c
            assert packed[offset] == int(stages[-1][y, x, c]) & 255
    for row in prefix['tensors']:
        if row['stage'] == 'view_or_saturated_residual':
            actual = np.load(folder / row['path'], allow_pickle=False)
            np.testing.assert_array_equal(actual, values[row['node']])
            checks.append(dict(node=row['node'], stage=row['stage'], values=int(actual.size), exact=True))
    rejected = []
    for name, action in (
        ('negative_ROM_offset', lambda: front.word_bytes(physical, -1, 1)),
        ('out_of_range_ROM_offset', lambda: front.word_bytes(physical, len(physical), 1)),
        ('shift_63', lambda: front.round_even(5, 63)),
        ('missing_interior_halo', lambda: halo_window(np.zeros((8, 8, 24), dtype=np.int8), origin=(8, 8))),
    ):
        try:
            action()
        except ValueError:
            rejected.append(name)
        else:
            raise AssertionError('negative case accepted: ' + name)
    with patch.object(h, 'sha', return_value='0'*64):
        try:
            h.pinned_inputs(front)
        except ValueError:
            rejected.append('wrong_model_digest')
        else:
            raise AssertionError('model digest mismatch was accepted')
    h.self_test()
    for path, digest in h.read(h.OUT / 'artifacts/receipt.json')['input_sha256'].items():
        assert h.sha(path) == digest, path
    result = dict(status='PASS_CPU_HANDOFF_REGRESSION', seconds=time.perf_counter()-started,
        full_prefix_values=sum(row['values'] for row in checks), stage_checks=checks,
        negatives_rejected=rejected, package_segments=len(manifest['segments']),
        max_conservative_accumulator_bound=max(bounds.values()), all_67_INT32_bounds_safe=True,
        halos_available=len(prefix['csp_halos']), runtime_numpy=runtime['numpy_version'],
        source_sha256=h.sha(__file__), CUDA_initialized=False, RTL_cycles=None,
        training_updates=0, new_accuracy_measurement=False, formal_acceptance=False)
    h.save(h.OUT / 'validation.json', result)
    print(json.dumps({k: v for k, v in result.items() if k != 'stage_checks'}), flush=True)


if __name__ == '__main__':
    main()
