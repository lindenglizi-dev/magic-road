"""冻结图的67层描述符和160-bit ROM参数读取参考，绝不使能DDR。"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PRODUCTION = ROOT.parents[1]


def main():
    graph_path = PRODUCTION / 'graph_artifacts/graph.json'
    artifact = PRODUCTION / 'numeric_artifacts'
    manifest_path = artifact / 'manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    graph = json.loads(graph_path.read_text(encoding='utf-8'))
    assert graph['source_sha256'] == manifest['graph_source_sha256']
    for name, expected_hash in graph['source_sha256'].items():
        assert hashlib.sha256((PRODUCTION.parents[2] / name).read_bytes()).hexdigest() == expected_hash, name
    payload = (artifact / 'numeric_test.bin').read_bytes()
    physical = (artifact / 'numeric_test_padded.bin').read_bytes()
    assert hashlib.sha256(payload).hexdigest() == manifest['payload_sha256']
    assert hashlib.sha256(physical).hexdigest() == manifest['physical_sha256']
    word_lines = (artifact / 'words.dath').read_text(encoding='ascii').splitlines()
    words = [bytes.fromhex(line)[::-1] for line in word_lines]
    assert len(words) == 14 * 512 and all(len(word) == 20 for word in words)
    assert b''.join(words) == physical and physical[:len(payload)] == payload
    segments = {segment['name']: segment for segment in manifest['segments']}
    cursor = 0
    for segment in manifest['segments']:
        assert segment['offset'] == cursor
        cursor += segment['length']
        assert hashlib.sha256(payload[segment['offset']:cursor]).hexdigest() == segment['sha256']
    assert cursor == len(payload)
    layer_package = {layer['name']: layer for layer in manifest['layers']}
    touched = set()
    crossing = set()

    def read(offset, width, signed=False):
        if offset < 0 or offset + width > len(payload):
            raise ValueError('field outside valid package')
        value = bytearray()
        for address in range(offset, offset + width):
            word, byte = divmod(address, 20)
            group, local = divmod(word, 512)
            assert 0 <= group < 14 and 0 <= local < 512
            touched.add(word)
            value.append(words[group * 512 + local][byte])
        if offset // 20 != (offset + width - 1) // 20:
            crossing.add((offset, width))
        assert bytes(value) == payload[offset:offset + width]
        return int.from_bytes(value, 'little', signed=signed)

    rows = []
    groups = []
    weights_checked = 0
    for node in graph['nodes']:
        if node['op'] != 'conv':
            continue
        record = layer_package[node['name']]
        assert record['graph_index'] == node['index'] and record['output_dtype'] == node['dtype']
        height, width, cout = node['output_shape_hwc']
        cin = node['input_shape_hwc'][2]
        kh, kw = node['kernel']
        depthwise = node['groups'] == cin == cout and kh == kw == 3
        terms = kh * kw * (cin // node['groups'])
        assert 1 <= terms <= 192
        activate = node['dtype'] == 'int8'
        offsets = record['fields']
        assert activate == ('post_multiplier' in offsets) == ('post_shift' in offsets)
        for name, offset in offsets.items():
            assert segments[node['name'] + '.' + name]['offset'] == offset
        post_multiplier = read(offsets['post_multiplier'], 4, True) if activate else 0
        post_shift = read(offsets['post_shift'], 1) if activate else 0
        assert 0 <= post_multiplier < 1 << 31 and 0 <= post_shift <= 62
        # 逐权重字节核对物理读口的字节顺序，不创建新的权重布局。
        for index in range(node['weights']):
            read(offsets['weights'] + index, 1, True)
            weights_checked += 1
        for channel_base in range(0, cout, 3):
            lanes = min(3, cout - channel_base)
            bias, pre_multiplier, pre_shift = [0] * 3, [0] * 3, [0] * 3
            for lane in range(lanes):
                channel = channel_base + lane
                bias[lane] = read(offsets['bias'] + 4 * channel, 4, True)
                pre_multiplier[lane] = read(offsets['pre_multiplier'] + 4 * channel, 4, True)
                pre_shift[lane] = read(offsets['pre_shift'] + channel, 1)
                assert 0 <= pre_multiplier[lane] < 1 << 31 and 0 <= pre_shift[lane] <= 62
            groups.append(dict(layer_id=len(rows), node_id=node['index'], channel_base=channel_base,
                               lane_mask=(1 << lanes) - 1, bias=bias, pre_multiplier=pre_multiplier,
                               pre_shift=pre_shift, post_multiplier=post_multiplier, post_shift=post_shift,
                               activate=activate))
        rows.append(dict(layer_id=len(rows), node_id=node['index'], name=node['name'],
                         op='DW' if depthwise else 'PW' if kh == kw == 1 else 'STEM',
                         source_views=node['inputs'], destination=node['output'],
                         input_hwc=node['input_shape_hwc'], output_hwc=node['output_shape_hwc'],
                         groups=node['groups'], kernel=node['kernel'], stride=node['stride'],
                         padding=node['padding'], padding_value=node['operator_padding_value'],
                         terms_per_output=terms, mac_groups=(terms + 7) // 8,
                         storage=node['storage'], field_offsets=offsets, activate=activate,
                         tile_columns=(width + 3) // 4, tile_rows=(height + 3) // 4,
                         output_element_bytes=1 if activate else 2))
    assert len(rows) == 67 and sum(row['activate'] for row in rows) == 61
    assert weights_checked == 113100
    assert sum(group['lane_mask'].bit_count() for group in groups) == 2501
    # 专门验证物理组交界，以及拒绝负地址和末尾越界。
    for offset in (19, 10239, 20479, len(payload) - 4):
        read(offset, 4)
    for offset, width in ((-1, 1), (len(payload), 1), (len(payload) - 3, 4)):
        try:
            read(offset, width)
        except ValueError:
            continue
        raise AssertionError('invalid package offset accepted')
    result = dict(status='FIXED_GRAPH_PARAMETER_REFERENCE_PASS_NOT_RTL_EXECUTOR',
                  graph_sha256=hashlib.sha256(graph_path.read_bytes()).hexdigest(),
                  manifest_sha256=hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
                  payload_sha256=manifest['payload_sha256'], layers=rows,
                  parameter_groups=groups, layer_count=len(rows), parameter_group_count=len(groups),
                  output_channels=2501, weights_checked=weights_checked,
                  cross_word_fields=len(crossing), physical_words_touched=len(touched),
                  limits=['TEST package, not trained quantized weights', 'DDR address unit still unverified',
                          'source_views require existing view resolver; not flat source DDR bases',
                          'mac_groups describes scalar arithmetic reduction, not spatial-triplet packing',
                          'not full 106-node execution schedule or measured cycles'])
    (ROOT / 'fixed_layer_descriptors.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps({key: value for key, value in result.items() if key not in ('layers', 'parameter_groups')}))


if __name__ == '__main__':
    main()
