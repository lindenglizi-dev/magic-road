"""Fixed RoadYOLO graph: calibrated PTQ package and exact integer reference.

Not QAT, not a qualified bitstream. Floating point is used only for calibration
and parameter encoding; IntegerModel.forward uses integer arithmetic throughout.
"""
from __future__ import annotations

import hashlib
import json
import math
import zlib
from pathlib import Path

import numpy as np
import torch
from torch.nn import functional as F

from cnn.integer import encode_multiplier, requantize, silu, tables
from cnn.hw_validation.production.graph import build_graph


def digest(data):
    return hashlib.sha256(data).hexdigest()


def conv_exact(image, weights, bias, stride=1, padding=0, groups=1):
    """Vectorized HWC integer convolution; scalar cnn.integer.conv2d is oracle."""
    if image.dtype != np.int8 or weights.dtype != np.int8:
        raise ValueError('INT8 image and weights required')
    if image.ndim != 3 or weights.ndim != 4 or stride < 1 or padding < 0:
        raise ValueError('invalid convolution shape')
    cout, cin, kh, kw = weights.shape
    if groups < 1 or image.shape[2] != cin * groups or cout % groups:
        raise ValueError('invalid groups')
    if bias.shape != (cout,) or bias.dtype.kind not in 'iu':
        raise ValueError('invalid bias')
    if np.any(bias < -(1 << 31)) or np.any(bias >= 1 << 31):
        raise OverflowError('bias outside INT32')
    kernel = weights.astype(np.int64)
    # An absolute bound also proves every partial reduction fits signed 33 bits.
    bound = np.abs(bias.astype(np.int64)) + 128 * np.abs(kernel).sum((1, 2, 3))
    if np.any(bound >= 1 << 32):
        raise OverflowError('cannot prove signed33 partial reduction safety')
    padded = np.pad(image, ((padding, padding), (padding, padding), (0, 0)))
    height, width = [(padded.shape[i] - k) // stride + 1 for i, k in enumerate((kh, kw))]
    if min(height, width) <= 0:
        raise ValueError('empty output')
    result = np.broadcast_to(bias.astype(np.int64), (height, width, cout)).copy()
    for y in range(kh):
        for x in range(kw):
            patch = padded[y:y + height * stride:stride, x:x + width * stride:stride].astype(np.int64)
            if groups == cout == image.shape[2] and cin == 1:
                result += patch * kernel[:, 0, y, x]
            else:
                for group in range(groups):
                    inputs = slice(group * cin, (group + 1) * cin)
                    outputs = slice(group * (cout // groups), (group + 1) * (cout // groups))
                    result[..., outputs] += patch[..., inputs] @ kernel[outputs, :, y, x].T
    if np.any(result < -(1 << 31)) or np.any(result >= 1 << 31):
        raise OverflowError('final accumulator outside INT32; frame invalid')
    return result.astype(np.int32)


def nonconv(node, values):
    inputs = [values[name] for name in node['inputs']]
    op = node['op']
    if op == 'split_view':
        return {view['output']: inputs[0][..., view['channel_offset']:
                    view['channel_offset'] + view['channels']] for view in node['outputs']}
    if op == 'concat_view':
        result = np.concatenate(inputs, axis=2)
    elif op == 'nearest_view':
        result = inputs[0].repeat(node['scale'][0], 0).repeat(node['scale'][1], 1)
    elif op == 'residual_view':
        if inputs[0].dtype == np.int8:
            result = np.clip(inputs[0].astype(np.int16) + inputs[1].astype(np.int16), -128, 127).astype(np.int8)
        else:
            result = inputs[0] + inputs[1]
    elif op == 'maxpool':
        source = inputs[0]
        padded = np.pad(source, ((2, 2), (2, 2), (0, 0)), constant_values=
                        -128 if source.dtype == np.int8 else -np.inf)
        result = np.maximum.reduce([padded[y:y + source.shape[0], x:x + source.shape[1]]
                                    for y in range(5) for x in range(5)])
    else:
        raise ValueError(f'unsupported frozen operator: {op}')
    return {node['output']: result}


def float_forward(graph, folded, image):
    values = {'input': image}
    for node in graph['nodes']:
        if node['op'] != 'conv':
            values.update(nonconv(node, values))
            continue
        weight, bias = folded[node['name']]
        source = torch.from_numpy(np.ascontiguousarray(values[node['inputs'][0]].transpose(2, 0, 1))).unsqueeze(0)
        output = F.conv2d(source, weight, bias, stride=node['stride'],
                          padding=node['padding'], groups=node['groups'])
        if node['dtype'] == 'int8':
            output = F.silu(output)
        values[node['output']] = output[0].permute(1, 2, 0).numpy().copy()
    return values


def aligned_scales(graph, ranges):
    """Union only scale-preserving edges; convolutions have independent scales."""
    parent = {name: name for name in ranges}
    def root(name):
        while parent[name] != name:
            name = parent[name]
        return name
    for node in graph['nodes']:
        if node['op'] == 'conv':
            continue
        outputs = ([v['output'] for v in node['outputs']] if node['op'] == 'split_view'
                   else [node['output']])
        names = node['inputs'] + outputs
        for name in names[1:]:
            parent[root(name)] = root(names[0])
    components = {}
    for name in parent:
        components.setdefault(root(name), []).append(name)
    raw = {node['output'] for node in graph['nodes'] if node.get('dtype') == 'int16_q7_8'}
    scales, groups = {}, []
    for members in components.values():
        if any(name in raw for name in members):
            if not all(name in raw for name in members):
                raise ValueError('mixed feature/head scale group')
            scale = 1 / 256
        elif 'input' in members:
            scale = 1.0
        else:
            maximum = max(ranges[name]['max_abs'] for name in members)
            scale = maximum / 127 if maximum else 1.0
        for name in members:
            scales[name] = scale
        groups.append({'members': members, 'scale': scale})
    return scales, groups


def encode_parameters(graph, folded, scales):
    parameters, quantization = {}, {}
    for node in graph['nodes']:
        if node['op'] != 'conv':
            continue
        name = node['name']
        weight, bias = (tensor.detach().numpy().astype(np.float64) for tensor in folded[name])
        if not np.isfinite(weight).all() or not np.isfinite(bias).all():
            raise ValueError('nonfinite weight/bias')
        maximum = np.max(np.abs(weight), axis=(1, 2, 3))
        weight_scale = np.where(maximum > 0, maximum / 127, 1.0)
        input_scale = scales[node['inputs'][0]]
        accumulator_scale = input_scale * weight_scale
        qb = np.rint(bias / accumulator_scale)
        if np.any(qb < -(1 << 31)) or np.any(qb >= 1 << 31):
            raise OverflowError('quantized bias outside INT32')
        pre = [encode_multiplier(float(scale * 256)) for scale in accumulator_scale]
        params = {
            'weights': np.clip(np.rint(weight / weight_scale[:, None, None, None]), -128, 127).astype(np.int8),
            'bias': qb.astype('<i4'),
            'pre_multiplier': np.array([p[0] for p in pre], dtype='<i4'),
            'pre_shift': np.array([p[1] for p in pre], dtype=np.uint8),
        }
        if node['dtype'] == 'int8':
            multiplier, shift = encode_multiplier(1 / (256 * scales[name]))
            params['post_multiplier'] = np.array([multiplier], dtype='<i4')
            params['post_shift'] = np.array([shift], dtype=np.uint8)
        bound = np.abs(params['bias'].astype(np.int64)) + 128 * np.abs(params['weights'].astype(np.int64)).sum((1, 2, 3))
        if np.any(bound >= 1 << 32):
            raise OverflowError(f'{name}: signed33 bound failed')
        quantization[name] = {'weight_scale': weight_scale.tolist(), 'input_scale': input_scale,
                              'output_scale': scales[name], 'absolute_accumulator_bound': int(bound.max())}
        parameters[name] = params
    return parameters, quantization


class IntegerModel:
    def __init__(self, graph, parameters, scales):
        self.graph, self.parameters, self.scales = graph, parameters, scales
        expected_names = {'input'}
        convs = {node['name']: node for node in graph['nodes'] if node['op'] == 'conv'}
        for node in graph['nodes']:
            expected_names.update([view['output'] for view in node['outputs']]
                                  if node['op'] == 'split_view' else [node['output']])
        if set(scales) != expected_names or any(not isinstance(value, (int, float)) or
                isinstance(value, bool) or not math.isfinite(value) or value <= 0 for value in scales.values()):
            raise ValueError('invalid tensor scales')
        if scales['input'] != 1.0 or any(scales[node['output']] != 1 / 256 for node in graph['nodes']
                                         if node.get('dtype') == 'int16_q7_8'):
            raise ValueError('fixed input or prediction scale changed')
        if set(parameters) != set(convs):
            raise ValueError('parameter layer set differs from graph')
        for name, node in convs.items():
            shapes = parameter_shapes(node)
            if set(parameters[name]) != set(shapes):
                raise ValueError(f'{name}: missing or extra parameter')
            for field, dtype in FIELDS:
                if field not in shapes:
                    continue
                array = parameters[name][field]
                if array.shape != shapes[field] or array.dtype != np.dtype(dtype):
                    raise ValueError(f'{name}.{field}: shape/dtype differs from graph')
                if 'multiplier' in field and np.any(array < 0):
                    raise ValueError('negative multiplier')
                if 'shift' in field and np.any(array > 62):
                    raise ValueError('invalid shift')
            if node['dtype'] == 'int8':
                expected = encode_multiplier(1 / (256 * scales[name]))
                if (int(parameters[name]['post_multiplier'][0]), int(parameters[name]['post_shift'][0])) != expected:
                    raise ValueError('output scale inconsistent with encoded post requantization')
        for node in graph['nodes']:
            if node['op'] == 'conv':
                continue
            names = node['inputs'] + ([v['output'] for v in node['outputs']]
                    if node['op'] == 'split_view' else [node['output']])
            if any(scales[name] != scales[names[0]] for name in names):
                raise ValueError(f"unaligned scales at {node['name']}")

    def forward(self, image, *, capture=False):
        if image.shape != (288, 512, 3) or image.dtype != np.int8:
            raise ValueError('expected centered HWC INT8 512x288 input')
        values, statistics = {'input': image}, {}
        for node in self.graph['nodes']:
            name = node['name']
            if node['op'] != 'conv':
                outputs = nonconv(node, values)
                if node['op'] == 'residual_view':
                    total = sum(values[key].astype(np.int16) for key in node['inputs'])
                    statistics[name] = {'saturated': int(((total < -128) | (total > 127)).sum()), 'values': total.size}
                values.update(outputs)
                continue
            p = self.parameters[name]
            acc = conv_exact(values[node['inputs'][0]], p['weights'], p['bias'],
                             node['stride'][0], node['padding'][0], node['groups'])
            pre = requantize(acc, p['pre_multiplier'], p['pre_shift'], -32768, 32767).astype(np.int16)
            output = (requantize(silu(pre), p['post_multiplier'], p['post_shift']).astype(np.int8)
                      if node['dtype'] == 'int8' else pre)
            # Endpoint occupancy is not an exact clipping count: report it as such.
            statistics[name] = {'pre_endpoint_count': int(((pre == -32768) | (pre == 32767)).sum()),
                                'output_endpoint_count': int(((output == np.iinfo(output.dtype).min) |
                                                             (output == np.iinfo(output.dtype).max)).sum()),
                                'values': output.size, 'acc_min': int(acc.min()), 'acc_max': int(acc.max())}
            values[name] = output
            if capture:
                values[name + ':acc'] = acc
                values[name + ':pre'] = pre
        return [values[name] for name in self.graph['outputs']], statistics, values if capture else None


FIELDS = [('weights', 'i1'), ('bias', '<i4'), ('pre_multiplier', '<i4'),
          ('pre_shift', 'u1'), ('post_multiplier', '<i4'), ('post_shift', 'u1')]
DTYPE_LABEL = {'i1': 'int8', '<i4': 'int32_le', 'u1': 'uint8', '<i2': '<i2', '<u2': '<u2'}
FIELD_ROLE = {'weights': 'weights_int8', 'bias': 'folded_bias_int32',
              'pre_multiplier': 'accumulator_to_q7_8_per_channel', 'pre_shift': 'accumulator_to_q7_8_per_channel',
              'post_multiplier': 'silu_to_int8_per_tensor', 'post_shift': 'silu_to_int8_per_tensor'}
LAYOUT = {'word_bytes': 20, 'words_per_group': 512, 'groups': 14, 'lanes': 4, 'lane_bytes': 5}
STATUS = 'TRAINED_PTQ_DIAGNOSTIC_NOT_QAT_NOT_BOARD_QUALIFIED'


def parameter_shapes(node):
    cout = node['output_shape_hwc'][2]
    shapes = {'weights': (cout, node['input_shape_hwc'][2] // node['groups'], *node['kernel']),
              'bias': (cout,), 'pre_multiplier': (cout,), 'pre_shift': (cout,)}
    if node['dtype'] == 'int8':
        shapes.update(post_multiplier=(1,), post_shift=(1,))
    return shapes


def write_package(output, graph, parameters, scales, provenance):
    """Same OIHW field order and 160-bit layout as numeric_package TEST fixture."""
    IntegerModel(graph, parameters, scales)
    output.mkdir(parents=True, exist_ok=False)
    payload, layers, segments = bytearray(), [], []
    for node in graph['nodes']:
        if node['op'] != 'conv':
            continue
        name = node['name']
        layer = {'name': name, 'graph_index': node['index'], 'output_dtype': node['dtype'], 'fields': {}}
        for field, dtype in FIELDS:
            if field not in parameters[name]:
                if field.startswith('post_') and node['dtype'] == 'int16_q7_8':
                    continue
                raise ValueError('missing parameter field')
            array = np.asarray(parameters[name][field], dtype=dtype)
            data = array.tobytes()
            offset = len(payload)
            layer['fields'][field] = offset
            segments.append({'name': name + '.' + field, 'offset': offset, 'length': len(data),
                             'dtype': DTYPE_LABEL[dtype], 'shape': list(array.shape), 'count': array.size,
                             'role': FIELD_ROLE[field], 'sha256': digest(data)})
            payload.extend(data)
        layers.append(layer)
    for name, dtype in [('silu', '<i2'), ('sigmoid', '<u2'), ('exp', '<u2')]:
        array = np.asarray(tables()[name], dtype=dtype)
        data = array.tobytes()
        segments.append({'name': 'shared.' + name, 'offset': len(payload), 'length': len(data),
                         'dtype': dtype, 'shape': list(array.shape), 'count': array.size,
                         'role': 'shared_lut', 'sha256': digest(data)})
        payload.extend(data)
    if len(payload) != 140522 or len(layers) != 67:
        raise ValueError('frozen package size mismatch')
    physical = bytes(payload) + bytes(143360 - len(payload))
    # Existing schema2 consumers require these historical filenames. Status and
    # provenance distinguish this trained PTQ candidate from random test packages.
    (output / 'numeric_test.bin').write_bytes(payload)
    (output / 'numeric_test_padded.bin').write_bytes(physical)
    (output / 'words.dath').write_text(''.join(physical[i:i + 20][::-1].hex() + '\n'
                                             for i in range(0, len(physical), 20)), encoding='ascii')
    lane_files = []
    for group in range(14):
        for lane in range(4):
            name = f'group_{group:02d}_lane_{lane}.dath'
            content = ''.join(physical[(group * 512 + word) * 20 + lane * 5:
                                      (group * 512 + word) * 20 + lane * 5 + 5][::-1].hex() + '\n'
                              for word in range(512))
            (output / name).write_text(content, encoding='ascii', newline='\n')
            lane_files.append({'name': name, 'sha256': digest(content.encode('ascii'))})
    manifest = {'schema_version': 2, 'status': STATUS,
                'payload_bytes': len(payload), 'physical_bytes': len(physical), 'padding_bytes': 2838,
                'payload_sha256': digest(payload), 'physical_sha256': digest(physical),
                'physical_crc32': f'{zlib.crc32(physical) & 0xffffffff:08x}', 'layout': LAYOUT,
                'graph_source_sha256': graph['source_sha256'], 'generator_sha256': digest(Path(__file__).read_bytes()),
                'contract_sha256': digest((Path(__file__).parent / 'deployment_contract.json').read_bytes()),
                'layers': layers, 'segments': segments, 'graph': graph, 'scales': scales, 'lane_files': lane_files,
                'silu_upper': int(tables()['silu_upper']), 'sigmoid_upper': int(tables()['sigmoid_upper']),
                'provenance': provenance, 'acceptance_eligible': False}
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    return manifest


def load_package(output):
    manifest = json.loads((output / 'manifest.json').read_text(encoding='utf-8'))
    payload = (output / 'numeric_test.bin').read_bytes()
    physical = (output / 'numeric_test_padded.bin').read_bytes()
    fixed = {'schema_version': 2, 'status': STATUS, 'payload_bytes': 140522,
             'physical_bytes': 143360, 'padding_bytes': 2838, 'layout': LAYOUT, 'acceptance_eligible': False}
    if any(manifest.get(key) != value for key, value in fixed.items()):
        raise ValueError('fixed package metadata changed')
    if (len(payload) != 140522 or digest(payload) != manifest['payload_sha256'] or
            physical != payload + bytes(143360 - len(payload)) or digest(physical) != manifest['physical_sha256']):
        raise ValueError('package hash/size/padding mismatch')
    expected_graph = build_graph()
    if manifest['graph'] != expected_graph:
        raise ValueError('graph/source differs from current frozen implementation')
    if (manifest['graph_source_sha256'] != expected_graph['source_sha256'] or
            manifest['contract_sha256'] != digest((Path(__file__).parent / 'deployment_contract.json').read_bytes()) or
            manifest['physical_crc32'] != f'{zlib.crc32(physical) & 0xffffffff:08x}'):
        raise ValueError('package source/contract/CRC mismatch')
    parameters = {n['name']: {} for n in expected_graph['nodes'] if n['op'] == 'conv'}
    expected_segments, expected_layers, offset = [], [], 0
    for node in expected_graph['nodes']:
        if node['op'] != 'conv':
            continue
        layer = {'name': node['name'], 'graph_index': node['index'], 'output_dtype': node['dtype'], 'fields': {}}
        for field, dtype in FIELDS:
            if field not in parameter_shapes(node):
                continue
            shape = parameter_shapes(node)[field]
            length = math.prod(shape) * np.dtype(dtype).itemsize
            expected_segments.append((node['name'] + '.' + field, DTYPE_LABEL[dtype], list(shape), offset, length,
                                      math.prod(shape), FIELD_ROLE[field]))
            layer['fields'][field] = offset
            offset += length
        expected_layers.append(layer)
    for name, dtype in [('silu', '<i2'), ('sigmoid', '<u2'), ('exp', '<u2')]:
        array = tables()[name]
        length = array.size * np.dtype(dtype).itemsize
        expected_segments.append(('shared.' + name, dtype, list(array.shape), offset, length, array.size, 'shared_lut'))
        offset += length
    if manifest['layers'] != expected_layers or len(manifest['segments']) != len(expected_segments):
        raise ValueError('package field layout differs from graph')
    end = 0
    for segment, expected in zip(manifest['segments'], expected_segments, strict=True):
        if tuple(segment[key] for key in ('name', 'dtype', 'shape', 'offset', 'length', 'count', 'role')) != expected:
            raise ValueError('package segment schema differs from frozen graph')
        if segment['offset'] != end:
            raise ValueError('noncontiguous segments')
        end += segment['length']
        data = payload[segment['offset']:end]
        if digest(data) != segment['sha256']:
            raise ValueError('segment hash mismatch')
        dtype = {label: dtype for dtype, label in DTYPE_LABEL.items()}[segment['dtype']]
        array = np.frombuffer(data, dtype=dtype).reshape(segment['shape']).copy()
        name, field = segment['name'].rsplit('.', 1)
        if name == 'shared':
            if not np.array_equal(array, tables()[field]):
                raise ValueError('LUT differs from integer reference')
        else:
            parameters[name][field] = array
    if end != len(payload):
        raise ValueError('incomplete package')
    if manifest['silu_upper'] != int(tables()['silu_upper']) or manifest['sigmoid_upper'] != int(tables()['sigmoid_upper']):
        raise ValueError('rounded LUT endpoints changed')
    words = (output / 'words.dath').read_text(encoding='ascii').splitlines()
    if len(words) != 7168 or b''.join(bytes.fromhex(word)[::-1] for word in words) != physical:
        raise ValueError('160-bit word image differs from payload')
    expected_lane_files = []
    for group in range(14):
        for lane in range(4):
            content = (output / f'group_{group:02d}_lane_{lane}.dath').read_bytes()
            expected = ''.join(physical[(group * 512 + word) * 20 + lane * 5:
                                       (group * 512 + word) * 20 + lane * 5 + 5][::-1].hex() + '\n'
                               for word in range(512)).encode('ascii')
            if content != expected:
                raise ValueError('physical ROM lane differs from payload')
            expected_lane_files.append({'name': f'group_{group:02d}_lane_{lane}.dath', 'sha256': digest(expected)})
    if manifest['lane_files'] != expected_lane_files:
        raise ValueError('lane manifest differs from physical ROM')
    return IntegerModel(expected_graph, parameters, manifest['scales']), manifest
