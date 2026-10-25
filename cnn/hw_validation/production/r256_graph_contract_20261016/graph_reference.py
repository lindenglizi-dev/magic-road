"""Fixed R256 shape/address reference; no CNN values, DDR transactions or RTL."""
from __future__ import annotations

import copy
import csv
import hashlib
import json
import math
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
PRODUCTION = HERE.parent
BASELINE = PRODUCTION / 'graph_artifacts/graph.json'
PARAMETERS = PRODUCTION / 'model_handoff_20261015/artifacts/layer_parameter_index.json'
CONTRACT = PRODUCTION.parent / 'plans/resource_budget_20261015/r256_candidate_contract_20261016.json'
OUT = HERE / 'graph'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def align_up(value, alignment=4096):
    assert value > 0 and alignment > 0 and alignment & (alignment - 1) == 0
    return (value + alignment - 1) & -alignment


def _resolver(graph):
    outputs = {n['output']: n for n in graph['nodes'] if 'output' in n}
    splits = {v['output']: (n, v) for n in graph['nodes'] if n['op'] == 'split_view'
              for v in n['outputs']}

    def shape(name):
        if name == 'input':
            return graph['input']['shape_hwc']
        if name in splits:
            n, v = splits[name]
            return [*shape(n['inputs'][0])[:2], v['channels']]
        n = outputs[name]
        return n.get('output_shape_hwc', n.get('shape_hwc'))

    def resolve(name, y, x, c, slot=0):
        h, w, channels = shape(name)
        if not (0 <= slot < len(graph['memory']['input_slots']) and
                0 <= y < h and 0 <= x < w and 0 <= c < channels):
            raise ValueError(f'outside {name} HWC/slot: {(y, x, c, slot)}')
        if name == 'input':
            return graph['memory']['input_slots'][slot]['base'] + (y * w + x) * channels + c
        if name in splits:
            n, v = splits[name]
            return resolve(n['inputs'][0], y, x, c + v['channel_offset'], slot)
        n = outputs[name]
        if 'storage' in n:
            s = n['storage']
            tile = (y // 4) * ((w + 3) // 4) + x // 4
            element = (tile * 16 + (y % 4) * 4 + x % 4) * channels + c
            address = s['base'] + element * s['bytes_per_element']
            assert s['base'] <= address < address + s['bytes_per_element'] <= s['base'] + s['raw_bytes']
            return address
        if n['op'] == 'residual_view':
            return resolve(n['storage_alias'], y, x, c, slot)
        if n['op'] == 'nearest_view':
            sy, sx = n['scale']
            return resolve(n['inputs'][0], y // sy, x // sx, c, slot)
        if n['op'] == 'concat_view':
            for source in n['inputs']:
                count = shape(source)[2]
                if c < count:
                    return resolve(source, y, x, c, slot)
                c -= count
        raise ValueError(f'unresolved tensor {name}')

    return shape, resolve


def tensor_shape(graph, name):
    """Return logical [H,W,C], including split outputs and virtual views."""
    return list(_resolver(graph)[0](name))


def resolve_byte_address(graph, tensor, y, x, c, slot=0):
    """First byte of a valid logical element; INT16 is little endian."""
    return _resolver(graph)[1](tensor, y, x, c, slot)


def operator_sample(graph, node, y, x, c, slot=0):
    """Conv/pool source read or logical padding; never read a padded tile lane."""
    if isinstance(node, str):
        node = next(n for n in graph['nodes'] if n['name'] == node)
    if node['op'] not in ('conv', 'maxpool'):
        raise ValueError('only conv/maxpool have operator padding')
    shape, resolve = _resolver(graph)
    source = node['inputs'][0]
    h, w, channels = shape(source)
    if not 0 <= c < channels:
        raise ValueError('source channel outside tensor')
    if 0 <= y < h and 0 <= x < w:
        return {'address': resolve(source, y, x, c, slot), 'fill': None,
                'semantics': 'logical_source'}
    return {'address': None, 'fill': node['operator_padding_value'],
            'semantics': 'conv_zero' if node['op'] == 'conv' else 'pool_minus128'}


def build_graph():
    """Reuse the frozen topology/parameter fields; propagate fixed R256 shapes."""
    old, index, contract = read(BASELINE), read(PARAMETERS), read(CONTRACT)
    graph = copy.deepcopy(old)
    graph['schema'] = 'road_yolo_r256_offline_graph_v1'
    graph['status'] = 'SHAPE_ADDRESS_ONLY_NOT_CNN_VALUES_OR_DEPLOYMENT'
    graph['candidate_tag'] = contract['candidate_tag']
    graph['source_sha256'] = {str(p): sha(p) for p in (BASELINE, PARAMETERS, CONTRACT, Path(__file__))}
    graph['parameter_model_key'] = index['model_key']
    inp = contract['input_tensor']
    graph['input']['shape_hwc'] = [inp['height'], inp['width'], inp['channels']]
    shapes = {'input': graph['input']['shape_hwc']}
    parameters = {layer['name']: layer for layer in index['layers']}
    cursor = graph['memory']['feature_begin']
    layer_number = 0
    for n in graph['nodes']:
        inputs = [shapes[name] for name in n['inputs']]
        h, w, cin = inputs[0]
        op = n['op']
        if op == 'split_view':
            assert sum(v['channels'] for v in n['outputs']) == cin
            for v in n['outputs']:
                shapes[v['output']] = [h, w, v['channels']]
                v['shape_hwc'] = shapes[v['output']]
            n['address_mapping'] = 'recurse(source,y,x,channel_offset+c)'
            continue
        if op in ('conv', 'maxpool'):
            kh, kw = n['kernel']
            sy, sx = n['stride']
            py, px = n['padding']
            cout = n['output_shape_hwc'][2]
            out_shape = [(h + 2 * py - kh) // sy + 1, (w + 2 * px - kw) // sx + 1, cout]
            n['input_shape_hwc'], n['output_shape_hwc'] = inputs[0], out_shape
            if op == 'conv':
                p = parameters[n['name']]
                assert p['shape_in'][2] == cin and p['shape_out'][2] == cout
                assert p['groups'] == n['groups'] and p['fields']['weights']['count'] == n['weights']
                n['parameter_fields'] = copy.deepcopy(p['fields'])
                n['layer_number'] = layer_number
                layer_number += 1
                n['macs'] = out_shape[0] * out_shape[1] * cout * (cin // n['groups']) * kh * kw
            oh, ow, oc = out_shape
            bpe = n['storage']['bytes_per_element']
            raw = ((oh + 3) // 4) * ((ow + 3) // 4) * 16 * oc * bpe
            allocated = align_up(raw)
            n['storage'].update(base=cursor, raw_bytes=raw, allocated_bytes=allocated,
                                end=cursor + allocated)
            cursor += allocated
        elif op == 'nearest_view':
            sy, sx = n['scale']
            out_shape = [h * sy, w * sx, cin]
            n['shape_hwc'] = out_shape
            n['address_mapping'] = 'recurse(source,y//scale_y,x//scale_x,c)'
        elif op == 'concat_view':
            assert all(s[:2] == [h, w] for s in inputs)
            out_shape = [h, w, sum(s[2] for s in inputs)]
            n['shape_hwc'] = out_shape
            n['address_mapping'] = 'select channel segment; recurse(segment_source,y,x,c-segment_offset)'
        elif op == 'residual_view':
            assert inputs[0] == inputs[1]
            out_shape = inputs[0]
            n['shape_hwc'] = out_shape
            n['address_mapping'] = 'recurse(branch_storage_alias,y,x,c); branch write_transform reads bypass before sat8'
        else:
            raise ValueError(f'unexpected frozen operator {op}')
        shapes[n['output']] = out_shape
    for slot in graph['memory']['input_slots']:
        slot['valid_bytes'] = inp['bytes']
    graph['memory']['feature_end'] = cursor
    assert cursor <= graph['memory']['arena_end']
    convs = [n for n in graph['nodes'] if n['op'] == 'conv']
    graph['summary'].update(feature_allocated_bytes=cursor - graph['memory']['feature_begin'],
                            raw_head_bytes=sum(math.prod(n['output_shape_hwc']) * 2 for n in convs
                                               if n['dtype'] == 'int16_q7_8'),
                            macs=sum(n['macs'] for n in convs),
                            max_logical_feature_bytes=max(math.prod(n['output_shape_hwc'])
                                                          for n in convs if n['dtype'] == 'int8'))
    graph['prediction'] = copy.deepcopy(contract['prediction'])
    graph['prediction']['packed_stream_is_not_an_additional_allocation'] = True
    graph['heads'] = [dict(head, tensor=tensor) for head, tensor in zip(contract['heads'], graph['outputs'])]
    graph['padding_contract'] = {'conv_logical': 0, 'maxpool_logical': -128,
                                 'physical_invalid_tile_lane': 0,
                                 'alignment_slack': 'not_a_logical_tensor_element_do_not_read'}
    return graph


def head_address_rows(graph):
    """All HWC7 stream offsets and actual reg/cls view storage addresses."""
    _, resolve = _resolver(graph)
    fields = graph['prediction']['order']
    for scale, head in enumerate(graph['heads']):
        for y in range(head['height']):
            for x in range(head['width']):
                cell = head['first_cell_id'] + y * head['width'] + x
                for c, field in enumerate(fields):
                    tensor = f'head{scale + 2}.reg_out' if c < 5 else f'head{scale + 2}.cls_out'
                    physical_c = c if c < 5 else c - 5
                    yield {'cell_id': cell, 'stride': head['stride'], 'y': y, 'x': x,
                           'field_index': c, 'field': field, 'packed_byte_offset': (cell * 7 + c) * 2,
                           'packed_byte_end_exclusive': (cell * 7 + c + 1) * 2,
                           'view': head['tensor'], 'physical_tensor': tensor,
                           'physical_channel': physical_c,
                           'physical_byte_address': resolve(head['tensor'], y, x, c),
                           'physical_byte_end_exclusive': resolve(tensor, y, x, physical_c) + 2}


def tile_rows(graph):
    for n in graph['nodes']:
        if 'storage' not in n:
            continue
        h, w, c = n['output_shape_hwc']
        s = n['storage']
        cols = (w + 3) // 4
        for ty in range((h + 3) // 4):
            for tx in range(cols):
                valid_h, valid_w = min(4, h - 4 * ty), min(4, w - 4 * tx)
                mask = sum(1 << (ly * 4 + lx) for ly in range(valid_h) for lx in range(valid_w))
                base = s['base'] + (ty * cols + tx) * 16 * c * s['bytes_per_element']
                yield {'tensor': n['output'], 'tile_id': ty * cols + tx, 'tile_y': ty, 'tile_x': tx,
                       'base': base, 'end_exclusive': base + 16 * c * s['bytes_per_element'],
                       'valid_rows': valid_h, 'valid_columns': valid_w, 'valid_pixel_mask': mask,
                       'channels': c, 'bytes_per_element': s['bytes_per_element'],
                       'invalid_lane_fill': 0}


def resource_delta(graph, baseline):
    rows = []
    for n, old in zip(graph['nodes'], baseline['nodes']):
        if 'storage' not in n:
            continue
        h, w, c = n['output_shape_hwc']
        s, previous = n['storage'], old['storage']
        rows.append({'tensor': n['output'], 'shape_hwc': [h, w, c],
                     'old_base': previous['base'], 'new_base': s['base'],
                     'old_logical_bytes': math.prod(old['output_shape_hwc']) * s['bytes_per_element'],
                     'new_logical_bytes': h * w * c * s['bytes_per_element'],
                     'old_physical_tile_bytes': previous['raw_bytes'], 'new_physical_tile_bytes': s['raw_bytes'],
                     'old_allocated_bytes': previous['allocated_bytes'], 'new_allocated_bytes': s['allocated_bytes'],
                     'physical_ratio': f"{s['raw_bytes']}/{previous['raw_bytes']}",
                     'padding_bytes': s['raw_bytes'] - h * w * c * s['bytes_per_element'],
                     'alignment_slack_bytes': s['allocated_bytes'] - s['raw_bytes']})
    return {'status': 'STATIC_BYTE_MAC_BUDGET_NOT_RESOURCE_OR_CYCLE_MEASUREMENT',
            'old_feature_allocated_bytes': baseline['summary']['feature_allocated_bytes'],
            'new_feature_allocated_bytes': graph['summary']['feature_allocated_bytes'],
            'old_MAC': baseline['summary']['macs'], 'new_MAC': graph['summary']['macs'],
            'logical_head_bytes': graph['summary']['raw_head_bytes'],
            'physical_head_tile_bytes': sum(n['storage']['raw_bytes'] for n in graph['nodes']
                                            if n.get('dtype') == 'int16_q7_8' and 'storage' in n),
            'allocated_head_bytes': sum(n['storage']['allocated_bytes'] for n in graph['nodes']
                                       if n.get('dtype') == 'int16_q7_8' and 'storage' in n),
            'input_slots_preserved': True, 'MAC_lanes_unchanged': 24, 'conv_weights_unchanged': 113100,
            'fixed_DSP_ROM_workstore_resources_do_not_scale_with_resolution': True,
            'DSP_ERAM_Slice': 'NOT_MEASURED', 'whole_frame_cycles_FPS': 'NOT_MEASURED',
            'layers': rows}


def self_check(graph, baseline=None, index=None):
    baseline, index = baseline or read(BASELINE), index or read(PARAMETERS)
    shape, resolve = _resolver(graph)
    nodes = graph['nodes']
    convs = [n for n in nodes if n['op'] == 'conv']
    counts = {op: sum(n['op'] == op for n in nodes) for op in
              ('conv', 'maxpool', 'residual_view', 'split_view', 'concat_view', 'nearest_view')}
    assert len(nodes) == 106 and counts == {'conv': 67, 'maxpool': 3, 'residual_view': 12,
                                          'split_view': 7, 'concat_view': 15, 'nearest_view': 2}
    assert [(n['name'], n['op'], n['inputs']) for n in nodes] == [
        (n['name'], n['op'], n['inputs']) for n in baseline['nodes']]
    assert sum(n['weights'] for n in convs) == 113100
    assert sum(n['macs'] for n in convs) == 53616384
    assert graph['summary']['max_logical_feature_bytes'] == 147456
    for name, expected in {'stem.conv': [72, 128, 16], 'csp2.out.conv': [36, 64, 24],
                           'csp3.out.conv': [18, 32, 48], 'csp4.out.conv': [9, 16, 96]}.items():
        assert shape(name) == expected
    assert len(index['layers']) == len(convs) == 67
    for layer, n in zip(index['layers'], convs):
        assert n['name'] == layer['name'] and n['parameter_fields'] == layer['fields']
        h, w, cout = n['output_shape_hwc']
        assert n['macs'] == h * w * cout * (n['input_shape_hwc'][2] // n['groups']) * math.prod(n['kernel'])
    cursor = graph['memory']['feature_begin']
    for n in nodes:
        if 'storage' in n:
            s = n['storage']
            h, w, c = shape(n['output'])
            assert s['base'] == cursor and s['base'] % 4096 == 0
            assert s['raw_bytes'] == ((h + 3) // 4) * ((w + 3) // 4) * 16 * c * s['bytes_per_element']
            assert s['allocated_bytes'] == align_up(s['raw_bytes']) and s['end'] <= graph['memory']['arena_end']
            cursor = s['end']
    assert cursor == graph['memory']['feature_end']
    for i, slot in enumerate(graph['memory']['input_slots']):
        old = baseline['memory']['input_slots'][i]
        assert slot['base'] == old['base'] and slot['allocated_bytes'] == old['allocated_bytes'] == 524288
        assert slot['valid_bytes'] == 110592
        assert resolve('input', 143, 255, 2, i) == slot['base'] + 110591
        assert slot['base'] + slot['allocated_bytes'] <= graph['memory']['feature_begin']
        for offset in range(110592):
            pixel, channel = divmod(offset, 3)
            y, x = divmod(pixel, 256)
            assert resolve('input', y, x, channel, i) == slot['base'] + offset
    assert graph['memory']['input_slots'][0]['base'] + 524288 <= graph['memory']['input_slots'][1]['base']
    for slot in (-1, 2):
        try:
            resolve('input', 0, 0, 0, slot)
        except ValueError:
            pass
        else:
            raise AssertionError('out-of-range input slot accepted')

    checked = view_checked = 0
    # Every logical element, including every nested virtual view, is range checked.
    for n in nodes:
        names = [v['output'] for v in n['outputs']] if n['op'] == 'split_view' else [n['output']]
        for name in names:
            h, w, c = shape(name)
            for y in range(h):
                for x in range(w):
                    for channel in range(c):
                        address = resolve(name, y, x, channel)
                        assert graph['memory']['feature_begin'] <= address < graph['memory']['feature_end']
                        if n['op'] == 'nearest_view':
                            assert address == resolve(n['inputs'][0], y // 2, x // 2, channel)
                        elif n['op'] == 'residual_view':
                            assert address == resolve(n['inputs'][1], y, x, channel)
                        elif n['op'] == 'split_view':
                            v = next(v for v in n['outputs'] if v['output'] == name)
                            assert address == resolve(n['inputs'][0], y, x, channel + v['channel_offset'])
                        elif n['op'] == 'concat_view':
                            offset = 0
                            for source in n['inputs']:
                                if channel < offset + shape(source)[2]:
                                    assert address == resolve(source, y, x, channel - offset)
                                    break
                                offset += shape(source)[2]
                        checked += 1
                        view_checked += int('storage' not in n)
            for bad in ((-1, 0, 0), (h, 0, 0), (0, w, 0), (0, 0, c)):
                try:
                    resolve(name, *bad)
                except ValueError:
                    pass
                else:
                    raise AssertionError('out-of-range coordinate accepted')
    padding_pixels = tail_tiles = 0
    by_output = {n['output']: n for n in nodes if 'output' in n}
    for tile in tile_rows(graph):
        n = by_output[tile['tensor']]
        s = n['storage']
        assert tile['end_exclusive'] <= s['base'] + s['raw_bytes']
        h, w, c = shape(n['output'])
        for local in range(16):
            ly, lx = divmod(local, 4)
            y, x = tile['tile_y'] * 4 + ly, tile['tile_x'] * 4 + lx
            valid = y < h and x < w
            assert bool(tile['valid_pixel_mask'] & (1 << local)) == valid
            if valid:
                for channel in range(c):
                    assert resolve(n['output'], y, x, channel) == tile['base'] + (local * c + channel) * s['bytes_per_element']
            else:
                assert tile['invalid_lane_fill'] == 0
                padding_pixels += 1
        if h == 9 and tile['tile_y'] == 2:
            assert tile['valid_rows'] == 1 and tile['valid_pixel_mask'] == 15
            tail_tiles += 1
    assert tail_tiles > 0 and padding_pixels > 0
    padding_cases = 0
    for n in nodes:
        if n['op'] in ('conv', 'maxpool'):
            h, w, c = n['input_shape_hwc']
            for y, x in ((-1, 0), (0, -1), (h, w - 1), (h - 1, w)):
                result = operator_sample(graph, n, y, x, c - 1)
                assert result['address'] is None and result['fill'] == (0 if n['op'] == 'conv' else -128)
                padding_cases += 1
            assert operator_sample(graph, n, h - 1, w - 1, c - 1)['address'] == resolve(n['inputs'][0], h - 1, w - 1, c - 1)
        if n['op'] == 'residual_view':
            producer = by_output[n['inputs'][1]]
            assert producer['write_transform']['bypass'] == n['inputs'][0]
            assert producer['write_transform']['op'] == 'post_silu_output_requant_add_sat8'
    rows = list(head_address_rows(graph))
    assert len(rows) == 21168 and len({r['cell_id'] for r in rows}) == 3024
    assert [r['packed_byte_offset'] for r in rows] == list(range(0, 42336, 2))
    assert len({r['physical_byte_address'] for r in rows}) == 21168
    assert rows[-1]['cell_id'] == 3023 and rows[-1]['packed_byte_end_exclusive'] == 42336
    for r in rows:
        assert r['physical_byte_address'] == resolve(r['physical_tensor'], r['y'], r['x'], r['physical_channel'])
        assert r['physical_byte_address'] % 2 == 0
    boundaries = [rows[cell * 7] for cell in (0, 2303, 2304, 2879, 2880, 3023)]
    assert [(r['cell_id'], r['stride']) for r in boundaries] == [(0, 4), (2303, 4), (2304, 8), (2879, 8), (2880, 16), (3023, 16)]
    return {'status': 'PASS_SHAPES_ADDRESSES_ONLY', 'node_count': 106, 'conv_count': 67,
            'MAC': 53616384, 'logical_elements_range_checked': checked,
            'input_slot_byte_addresses_checked': 221184,
            'view_elements_mapping_checked': view_checked, 'physical_invalid_pixels_zero_fill': padding_pixels,
            'P4_tail_tiles_one_valid_row_checked': tail_tiles, 'operator_padding_cases': padding_cases,
            'parameter_fields_exactly_preserved': 67, 'head_cells': 3024, 'head_fields': 21168,
            'packed_head_bytes': 42336, 'scale_boundaries': boundaries,
            'CNN_values': 'NOT_TESTED', 'DDR_visibility_ownership': 'NOT_TESTED',
            'RTL_toolchain_resource_timing_FPS': 'NOT_RUN',
            'source_sha256': graph['source_sha256'], 'python_executable': sys.executable,
            'python_executable_sha256': sha(Path(sys.executable)),
            'command': f'"{sys.executable}" "{Path(__file__).resolve()}"'}


def _write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def _write_csv(path, rows):
    rows = iter(rows)
    first = next(rows)
    with path.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(first))
        writer.writeheader()
        writer.writerow(first)
        writer.writerows(rows)


def run():
    graph = build_graph()
    receipt = self_check(graph)
    rejected = []
    for case in ('P4_old_allocation_divided_by_four', 'weight_offset_changed', 'MAC_changed', 'input_slot_relocated'):
        bad = copy.deepcopy(graph)
        if case == 'P4_old_allocation_divided_by_four':
            node = next(n for n in bad['nodes'] if n['name'] == 'csp4.out.conv')
            node['storage']['raw_bytes'] = 61440 // 4
        elif case == 'weight_offset_changed':
            bad['nodes'][0]['parameter_fields']['weights']['offset'] += 1
        elif case == 'MAC_changed':
            bad['nodes'][0]['macs'] += 1
        else:
            bad['memory']['input_slots'][0]['base'] += 4096
        try:
            self_check(bad)
        except AssertionError:
            rejected.append(case)
        else:
            raise AssertionError(f'negative regression was accepted: {case}')
    receipt['negative_regressions_rejected'] = rejected
    OUT.mkdir(exist_ok=True)
    _write_json(OUT / 'graph.json', graph)
    _write_json(OUT / 'views.json', [n for n in graph['nodes'] if 'storage' not in n])
    _write_json(OUT / 'resource_delta.json', resource_delta(graph, read(BASELINE)))
    _write_csv(OUT / 'layers.csv', ({'layer_number': n['layer_number'], 'graph_index': n['index'],
               'name': n['name'], 'input_hwc': json.dumps(n['input_shape_hwc']),
               'output_hwc': json.dumps(n['output_shape_hwc']), 'MAC': n['macs'],
               'weight_offset': n['parameter_fields']['weights']['offset'], 'weights': n['weights'],
               'base': n['storage']['base'], 'physical_tile_bytes': n['storage']['raw_bytes'],
               'allocated_bytes': n['storage']['allocated_bytes'], 'end': n['storage']['end']}
               for n in graph['nodes'] if n['op'] == 'conv'))
    _write_csv(OUT / 'tiles.csv', tile_rows(graph))
    _write_csv(OUT / 'head_addresses.csv', head_address_rows(graph))
    receipt['artifacts'] = {p.name: {'sha256': sha(p), 'bytes': p.stat().st_size}
                            for p in sorted(OUT.iterdir()) if p.is_file() and p.name != 'self_check_receipt.json'}
    _write_json(OUT / 'self_check_receipt.json', receipt)
    print(json.dumps({k: v for k, v in receipt.items() if k not in
                      ('source_sha256', 'artifacts', 'scale_boundaries')}, ensure_ascii=False))
    return receipt


if __name__ == '__main__':
    run()
