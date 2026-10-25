"""CPU-only frozen model handoff; no training/export/RTL/tool invocation."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
PACKAGE = ROOT / 'cnn/reports/qat_frozen_stem_g10_20261014_v1/package'
CHECKPOINT = ROOT / 'cnn/runs/qat_frozen_stem_g10_20261014_v1/last.pt'
PAYLOAD = 'b35d4a66a69e441dc29bc60c7e3f507661f48da5f33b810d7340f6ed17a65145'
CHECKPOINT_SHA = 'f58ce4501104e818c8a6fb10e378d7e7668b937b1332f3530180d4806029d3dd'
MANIFEST_SHA = '93a05a97f78489fabd511909367be0f8b676680c01e5f74a21d571a88f82ff2b'
BASE = ROOT / 'cnn/hw_validation/production'
REPORTS = BASE / 'reports'
FRONT = REPORTS / 'qat_g10_front3_data_20261014_v1'
CSP = REPORTS / 'qat_g10_csp_first_data_20261015_v2'
QUANT = ROOT / 'cnn/reports/replay_g10_integer_20261013_v2/quantization.json'
DATASET = ROOT / 'cnn/reports/ac_g10_20261013_v1/dataset.json'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def save(path, value):
    with Path(path).open('x', encoding='utf-8') as handle:
        json.dump(value, handle, indent=2, ensure_ascii=False)
        handle.write('\n')


def initialize():
    if os.environ.get('CUDA_VISIBLE_DEVICES') != '-1':
        raise ValueError('launch with CUDA_VISIBLE_DEVICES=-1; CPU only')
    sys.path.insert(0, str(ROOT))
    from cnn.hw_validation.production import export_qat_front3 as front
    front.diag.runtime_guard()
    return front, front.diag.runtime.native_runtime_identity()


def window(source, y, x, height, width):
    """True full-tensor padding only; never infer missing interior context as zero."""
    import numpy as np
    if source.ndim != 3 or source.dtype != np.int8 or height <= 0 or width <= 0:
        raise ValueError('full HWC INT8 tensor and positive window required')
    result = np.zeros((height, width, source.shape[2]), dtype=np.int8)
    sy, sx = max(0, y), max(0, x)
    ey, ex = min(source.shape[0], y + height), min(source.shape[1], x + width)
    if sy < ey and sx < ex:
        result[sy-y:ey-y, sx-x:ex-x] = source[sy:ey, sx:ex]
    return result


def tile_bytes(array):
    import numpy as np
    h, w, c = array.shape
    padded = np.pad(array, ((0, (-h) % 4), (0, (-w) % 4), (0, 0)))
    return padded.reshape((h+3)//4, 4, (w+3)//4, 4, c).transpose(0, 2, 1, 3, 4).tobytes()


def pinned_inputs(front):
    expected = {PACKAGE / 'manifest.json': MANIFEST_SHA, PACKAGE / 'numeric_test.bin': PAYLOAD,
                CHECKPOINT: CHECKPOINT_SHA}
    manifest = read(PACKAGE / 'manifest.json')
    expected.update({ROOT / path: value for path, value in manifest['graph_source_sha256'].items()})
    expected[QUANT] = manifest['provenance']['identity']['quantization_sha256']
    expected[DATASET] = '6af48b5ec8da6550a5d0af31db8b8f58d1fc8c9960df0eda9a66ad7c94f5f5e1'
    for path, digest in expected.items():
        if sha(path) != digest:
            raise ValueError(f'bound input changed: {path}')
    model, manifest = front.load_package(PACKAGE)  # Also verifies all 56 physical lane images.
    if (manifest['provenance']['checkpoint_sha256'] != CHECKPOINT_SHA
            or manifest['provenance']['identity']['graph_sha256'] != front.base.protocol_hash(model.graph)):
        raise ValueError('checkpoint/graph binding mismatch')
    for folder in (FRONT, CSP):
        receipt = read(folder / 'verification_receipt.json')
        if folder == FRONT and receipt['payload_sha256'] != PAYLOAD:
            raise ValueError('front3 belongs to a different model')
        if folder == CSP and read(folder / 'identity.json')['payload_sha256'] != PAYLOAD:
            raise ValueError('CSP belongs to a different model')
        for relative, digest in receipt['artifact_sha256'].items():
            path = folder / relative
            if sha(path) != digest:
                raise ValueError(f'reused artifact changed: {path}')
            expected[path] = digest
        expected[folder / 'verification_receipt.json'] = sha(folder / 'verification_receipt.json')
    export = read(PACKAGE.parent / 'export_parity.json')
    if not export['passed'] or export['payload_sha256'] != PAYLOAD or export['checkpoint_sha256'] != CHECKPOINT_SHA:
        raise ValueError('original export parity binding mismatch')
    for relative in ('cnn/train.py', 'cnn/model.py', 'cnn/integer.py', 'cnn/dataset.py',
                     'cnn/hw_validation/production/trained_integer.py',
                     'cnn/hw_validation/production/export_qat_front3.py',
                     'cnn/hw_validation/production/export_qat_csp_first.py'):
        expected[ROOT / relative] = sha(ROOT / relative)
    expected[Path(__file__)] = sha(__file__)
    for path in (BASE / 'graph_artifacts/graph.json', PACKAGE.parent / 'decision.json',
                 PACKAGE.parent / 'export_parity.json',
                 ROOT / 'cnn/reports/early_feature_injection16_20261014_v1/decision.json',
                 ROOT / 'cnn/reports/ac_optimization_20261013_v1/decision.json'):
        expected[path] = sha(path)
    return model, manifest, expected


def layer_index(model, manifest):
    quant = read(QUANT)
    segments = {item['name']: item for item in manifest['segments']}
    layers = []
    for node in model.graph['nodes']:
        if node['op'] != 'conv':
            continue
        name = node['name']
        fields = {}
        for field in model.parameters[name]:
            segment = segments[name + '.' + field]
            fields[field] = {**segment, 'absolute_package': str(PACKAGE),
                'start_word160': segment['offset']//20, 'start_byte_in_word': segment['offset']%20,
                'end_exclusive': segment['offset']+segment['length']}
        layers.append(dict(name=name, graph_index=node['index'], inputs=node['inputs'],
            shape_in=node['input_shape_hwc'], shape_out=node['output_shape_hwc'],
            kernel=node['kernel'], stride=node['stride'], padding=node['padding'], groups=node['groups'],
            storage=node['storage'], output_dtype=node['dtype'], fields=fields,
            input_scale=model.scales[node['inputs'][0]], output_scale=model.scales[name],
            weight_scale_per_output_channel=quant[name]['weight_scale'],
            weight_scale_source=str(QUANT), weight_scale_source_sha256=sha(QUANT),
            accumulator_scale=[model.scales[node['inputs'][0]] * value for value in quant[name]['weight_scale']],
            postprocess_mode='RAW_INT16_NO_SILU_NO_POST' if node['dtype'] == 'int16_q7_8' else 'SILU_INT8'))
    return dict(model_key='sha256:' + PAYLOAD, wire_model_id32=None,
        wire_model_id_status='C7 assigns and binds to full payload SHA; not present in original package',
        canonical_package=str(PACKAGE), original_manifest_status=manifest['status'],
        layers=layers, shared_tables=[s for s in manifest['segments'] if s['name'].startswith('shared.')],
        silu_upper=manifest['silu_upper'], sigmoid_upper=manifest['sigmoid_upper'],
        graph_views=[n for n in model.graph['nodes'] if n['op'] != 'conv'],
        tensor_scales=model.scales, acceptance_eligible=False)


def replay_old_vectors(front, model, manifest):
    import numpy as np
    image = np.array([int(v, 16) for v in (FRONT / 'parameters/rgb.hex').read_text().split()], dtype=np.uint8)
    image = image.reshape(288, 512, 3)
    stages = {}
    from cnn.integer import tables
    lut = tables()['silu']
    stem = front.stage((image[:32, :32].astype(np.int16)-128).astype(np.int8),
                        model.parameters['stem.conv'], lut, manifest['silu_upper'], 2, 1, 1)
    dw = front.stage(np.pad(stem[-1], ((1, 0), (1, 0), (0, 0))),
                      model.parameters['down2.dw.conv'], lut, manifest['silu_upper'], 2, 0, 16)
    pw = front.stage(dw[-1], model.parameters['down2.pw.conv'], lut, manifest['silu_upper'], 1, 0, 1)
    with np.load(FRONT / 'oracle/stages.npz', allow_pickle=False) as old:
        for prefix, arrays in (('stem', stem), ('dw', dw), ('pw', pw)):
            for suffix, array in zip(('acc', 'pre', 'silu', 'post'), arrays, strict=True):
                np.testing.assert_array_equal(array, old[prefix + '_' + suffix])
                stages[prefix+'_'+suffix] = int(array.size)
    np.testing.assert_array_equal(pw[-1], np.load(CSP / 'inputs/input_pw_hwc.npy', allow_pickle=False))
    from cnn.hw_validation.production.export_qat_csp_first import halo_window, add_residual
    cdw = front.stage(halo_window(pw[-1]), model.parameters['csp2.blocks.0.dw.conv'],
                       lut, manifest['silu_upper'], 1, 0, 12)
    cpw = front.stage(cdw[-1], model.parameters['csp2.blocks.0.pw.conv'], lut, manifest['silu_upper'], 1, 0, 1)
    total, residual = add_residual(pw[-1][:4, :4, 12:24], cpw[-1])
    with np.load(CSP / 'golden.npz', allow_pickle=False) as old:
        for prefix, arrays in (('dw', cdw), ('pw', cpw)):
            for suffix, array in zip(('acc', 'pre', 'silu', 'post'), arrays, strict=True):
                np.testing.assert_array_equal(array, old[prefix+'_'+suffix])
        np.testing.assert_array_equal(total, old['residual_sum'])
        np.testing.assert_array_equal(residual, old['residual_post'])
    return dict(front3_stage_values=sum(stages.values()), csp_stage_values=8*192,
                residual_sum_and_post_values=384, exact=True,
                input_kind='synthetic_RGB; every intermediate is computed from actual preceding layer',
                RTL_cycles='NOT_RUN_THIS_BATCH; see explicitly historical index in handoff.txt')


def prefix(front, model, manifest, folder):
    import numpy as np
    from cnn import integer
    from cnn.train import load_dataset_snapshot, FullFrameDataset
    from cnn.hw_validation.production.run_trained_integer import centered
    from cnn.hw_validation.production.trained_integer import nonconv
    _, snapshot = load_dataset_snapshot(DATASET)
    rows = sorted((row for row in snapshot.rows if row['split'] == 'val'), key=lambda row: row['image'])
    image, _, key = FullFrameDataset(rows[:1], 'val', mosaic=False)[0]
    values = {'input': centered(image)}
    np.save(folder / 'input_rgb_hwc.npy', (values['input'].astype(np.int16)+128).astype(np.uint8), allow_pickle=False)
    (folder / 'input_rgb_nhwc.bin').write_bytes((values['input'].astype(np.int16)+128).astype(np.uint8).tobytes())
    records, checks, halos = [], [], []
    lut = integer.tables()['silu']
    for node in model.graph['nodes'][:12]:  # Exact full first3 -> both CSP2 residuals -> output fusion.
        name = node['name']
        if node['op'] != 'conv':
            values.update(nonconv(node, values))
            continue
        source = values[node['inputs'][0]]
        params = model.parameters[name]
        stride, pad, kernel = node['stride'][0], node['padding'][0], node['kernel'][0]
        arrays = front.stage(source, params, lut, manifest['silu_upper'], stride, pad, node['groups'])
        values[name] = arrays[-1]
        h, w, _ = arrays[-1].shape
        origins = ((0, 0), (0, w-4), (h-4, 0), (h-4, w-4), ((h//2)//4*4, (w//2)//4*4))
        for y, x in origins:
            span = 3*stride + kernel
            local = window(source, y*stride-pad, x*stride-pad, span, span)
            acc = integer.conv2d(local, params['weights'], params['bias'], stride, 0, node['groups'])
            pre = integer.requantize(acc, params['pre_multiplier'], params['pre_shift'], -32768, 32767).astype(np.int16)
            activated = integer.silu(pre)
            post = integer.requantize(activated, params['post_multiplier'], params['post_shift']).astype(np.int8)
            for suffix, a, full in zip(('acc', 'pre', 'silu', 'post'), (acc, pre, activated, post), arrays, strict=True):
                np.testing.assert_array_equal(a, full[y:y+4, x:x+4])
                checks.append(dict(layer=name, origin=[y, x], stage=suffix, values=int(a.size), exact=True))
            if name in ('csp2.blocks.0.dw.conv', 'csp2.blocks.1.dw.conv'):
                path = f'{name}_halo_y{y}_x{x}.npy'
                np.save(folder / path, local, allow_pickle=False)
                halos.append(dict(layer=name, origin=[y, x], path=path, shape=list(local.shape),
                                  source=node['inputs'][0], scope='true full predecessor; zero only outside logical image'))
        for suffix, array in zip(('acc', 'pre', 'silu', 'post'), arrays, strict=True):
            path = f'{name}.{suffix}.npy'
            np.save(folder / path, array, allow_pickle=False)
            records.append(dict(node=name, stage=suffix, path=path, shape=list(array.shape), dtype=str(array.dtype)))
        path = f'{name}.tile4x4_hwc.bin'
        (folder / path).write_bytes(tile_bytes(arrays[-1]))
        records.append(dict(node=name, stage='post_ddr_tile_layout', path=path, storage=node['storage']))
    for name in ('split.00.0', 'split.00.1', 'residual.00', 'residual.01', 'concat.00'):
        path = name + '.npy'
        np.save(folder / path, values[name], allow_pickle=False)
        records.append(dict(node=name, stage='view_or_saturated_residual', path=path,
                            shape=list(values[name].shape), dtype=str(values[name].dtype)))
    return dict(input_image=str(rows[0]['image_path']), image_sha256=sha(rows[0]['image_path']), teacher_key=key,
        input_kind='existing development real image; no new ground truth or accuracy evaluation',
        selection='first sorted validation image; independent of predictions',
        preprocess=rows[0].get('preprocess'), dataset_sha256=sha(DATASET),
        nodes=list(range(12)), convolution_layers=8, full_network_forwards=0,
        tensors=records, scalar_and_independent_RNE_checks=checks,
        compared_values=sum(row['values'] for row in checks), csp_halos=halos,
        all_CSP_inputs_from_complete_predecessor=True, actual_DDR_or_RTL=False)


def run(verify=False):
    started = time.perf_counter()
    front, runtime = initialize()
    model, manifest, frozen = pinned_inputs(front)
    if verify:
        receipt = read(OUT / 'artifacts/receipt.json')
        for path, digest in receipt['input_sha256'].items():
            if sha(path) != digest:
                raise ValueError('handoff dependency changed: ' + path)
        for path, digest in receipt['artifact_sha256'].items():
            if sha(OUT / 'artifacts' / path) != digest:
                raise ValueError('handoff artifact changed: ' + path)
        replay_old_vectors(front, model, manifest)
        print('PASS_CPU_MODEL_HANDOFF_VERIFY_NO_GPU_NO_RTL', flush=True)
        return
    folder = OUT / 'artifacts'
    folder.mkdir(exist_ok=False)
    tensors = folder / 'golden_prefix'
    tensors.mkdir()
    save(folder / 'layer_parameter_index.json', layer_index(model, manifest))
    reused = replay_old_vectors(front, model, manifest)
    measured = prefix(front, model, manifest, tensors)
    frozen[Path(measured['input_image'])] = measured['image_sha256']
    save(folder / 'golden_prefix_index.json', measured)
    for path, digest in frozen.items():
        if sha(path) != digest:
            raise ValueError(f'source/input changed during CPU run: {path}')
    save(folder / 'receipt.json', dict(status='CPU_MODEL_HANDOFF_VERIFIED_NOT_DEPLOYMENT',
        canonical_package=str(PACKAGE), payload_sha256=PAYLOAD, checkpoint_sha256=CHECKPOINT_SHA,
        manifest_sha256=MANIFEST_SHA, runtime=runtime, original_status=manifest['status'],
        reused_regression=reused, prefix_compared_values=measured['compared_values'],
        convolution_layers=67, raw_int16_prediction_layers=6,
        input_sha256={str(path): digest for path, digest in frozen.items()},
        artifact_sha256={path.relative_to(folder).as_posix(): sha(path) for path in folder.rglob('*') if path.is_file()},
        seconds=time.perf_counter()-started, training_updates=0, CUDA_initialized=False,
        RTL_run=False, TD_run=False, board_or_bitstream=False, formal_acceptance=False,
        thresholds_frozen=False, whole_network_RTL_compared=False))
    print('PASS_CPU_MODEL_HANDOFF_BUILD_NO_GPU_NO_RTL', flush=True)


def self_test():
    import numpy as np
    from cnn.hw_validation.production.export_qat_front3 import round_even
    a = np.arange(6*7*3, dtype=np.int8).reshape(6, 7, 3)
    halo = window(a, -1, -1, 6, 6)
    np.testing.assert_array_equal(halo[1:, 1:], a[:5, :5])
    assert not halo[0].any() and not halo[:, 0].any()
    packed = np.frombuffer(tile_bytes(a), dtype=np.int8).reshape(2, 2, 4, 4, 3)
    for y, x, c in np.ndindex(a.shape):
        assert packed[y//4, x//4, y%4, x%4, c] == a[y, x, c]
    assert round_even(5, 1) == 2 and round_even(7, 1) == 4 and round_even(-5, 1) == -2
    print('PASS_HALO_TILE_LAYOUT_AND_RNE_SELF_TEST', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    if args.self_test:
        initialize()
        self_test()
    else:
        run(verify=args.verify)
