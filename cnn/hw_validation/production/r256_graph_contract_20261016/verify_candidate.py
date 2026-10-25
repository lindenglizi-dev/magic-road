"""交叉核对图地址CSV与几何cell编号，验证冻结输入，禁止外推CNN数值/FPS。"""
import csv
import hashlib
import json
from pathlib import Path
import time

import freeze_inputs
import geometry_reference as geometry

HERE = Path(__file__).resolve().parent


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run():
    started = time.perf_counter()
    freeze_inputs.run()
    graph = read(HERE / 'graph/graph.json')
    old = read(HERE.parent / 'graph_artifacts/graph.json')
    graph_receipt = read(HERE / 'graph/self_check_receipt.json')
    geometry_receipt = read(HERE / 'geometry/self_check_receipt.json')
    assert graph_receipt['status'] == 'PASS_SHAPES_ADDRESSES_ONLY'
    assert geometry_receipt['status'] == 'PASS_R256_GEOMETRY_NOT_CNN_VALUES'
    assert geometry_receipt['script_sha256'] == sha(HERE / 'geometry_reference.py')
    assert geometry_receipt['vectors_sha256'] == sha(HERE / 'geometry/vectors.json')
    for name, identity in graph_receipt['artifacts'].items():
        assert sha(HERE / 'graph' / name) == identity['sha256'], name
    for name, digest in graph_receipt['source_sha256'].items():
        assert sha(Path(name)) == digest, name
    nodes = {n['name']: n for n in graph['nodes']}
    for before in old['nodes']:
        current = nodes[before['name']]
        if 'output_shape_hwc' in before:
            h, w, c = before['output_shape_hwc']
            assert current['output_shape_hwc'] == [h // 2, w // 2, c]
    with (HERE / 'graph/tiles.csv').open(encoding='utf-8', newline='') as stream:
        tiles = {(row['tensor'], int(row['tile_y']), int(row['tile_x'])): row for row in csv.DictReader(stream)}
    physical_bytes = set()
    with (HERE / 'graph/head_addresses.csv').open(encoding='utf-8', newline='') as stream:
        rows = list(csv.DictReader(stream))
    assert len(rows) == 21168
    for ordinal, row in enumerate(rows):
        cell, field = divmod(ordinal, 7)
        scale, y, x, stride = geometry.cell_location(cell)
        assert tuple(int(row[key]) for key in ('cell_id', 'field_index', 'y', 'x', 'stride')) == (cell, field, y, x, stride)
        assert int(row['packed_byte_offset']) == ordinal * 2
        producer = f'head{scale + 2}.reg_out' if field < 5 else f'head{scale + 2}.cls_out'
        channel = field if field < 5 else field - 5
        count = 5 if field < 5 else 2
        tile = tiles[(producer, y // 4, x // 4)]
        assert int(tile['valid_pixel_mask']) & (1 << ((y % 4) * 4 + x % 4))
        address = int(tile['base']) + (((y % 4) * 4 + x % 4) * count + channel) * 2
        assert int(row['physical_byte_address']) == address
        assert address + 2 <= int(tile['end_exclusive'])
        physical_bytes.update((address, address + 1))
    assert len(physical_bytes) == 42336
    assert int(rows[-1]['cell_id']) == 3023 and int(rows[-1]['packed_byte_end_exclusive']) == 42336
    vectors = read(HERE / 'geometry/vectors.json')
    for case in vectors['pipeline_cases']:
        overrides = {row['cell_id']: row['raw7'] for row in case['overrides']}
        assert geometry.trace(overrides) == case['expected'], case['name']
    audit = read(HERE / 'audit/audit_receipt.json')
    assert audit['status'] == 'PASS_READ_ONLY_ACTUAL_SOURCE_CLOSURE_AUDIT'
    assert audit['compiled_source_rows'] == 33 and audit['bindings'] == 6
    source_hashes = read(HERE / 'audit/read_source_hashes.json')
    assert source_hashes['unchanged'] and not source_hashes['changed']
    for name, digest in source_hashes['before'].items():
        assert sha(Path(name)) == digest, name
    output_files = [p for subdir in ('graph', 'geometry', 'audit')
                    for p in sorted((HERE / subdir).rglob('*')) if p.is_file()]
    output_files.extend(HERE / name for name in ('freeze_inputs.py', 'geometry_reference.py',
                                                'graph_reference.py', 'verify_candidate.py', 'input_closure.json'))
    result = {'status': 'PASS_R256_SHAPE_ADDRESS_GEOMETRY_CROSSCHECK_ONLY',
              'candidate': geometry.CONTRACT['candidate_tag'],
              'candidate_contract_sha256': sha(geometry.PLAN / 'r256_candidate_contract_20261016.json'),
              'candidate_graph_sha256': sha(HERE / 'graph/graph.json'),
              'payload_sha256': hashlib.sha256(geometry.PAYLOAD).hexdigest(),
              'wire_model_id': None, 'wire_resize_id': None,
              'head_fields_checked': len(rows), 'distinct_physical_head_bytes': len(physical_bytes),
              'synthetic_postprocess_cases_replayed': len(vectors['pipeline_cases']),
              'actual_compiled_source_rows_audited': audit['compiled_source_rows'],
              'actual_instance_bindings_audited': audit['bindings'],
              'CPU_seconds': time.perf_counter() - started,
              'artifacts': {p.relative_to(HERE).as_posix(): sha(p) for p in output_files},
              'CNN_values': 'NOT_TESTED_C2_OWNS', 'RTL_changes': False,
              'RTL_simulation_synthesis_timing': 'NOT_RUN', 'FPGA_resources_FPS_accuracy': 'NOT_MEASURED',
              'deployment_candidate_selected': False}
    (HERE / 'verification_receipt.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k != 'artifacts'}, ensure_ascii=False))


if __name__ == '__main__':
    run()
