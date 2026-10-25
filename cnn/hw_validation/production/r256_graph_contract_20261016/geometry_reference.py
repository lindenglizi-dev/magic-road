"""R256固定几何/TopK/NMS参考：复用冻结整数原语及包内表，不推理或训练。"""
import hashlib
import heapq
import json
import os
from pathlib import Path
import struct
import sys
import time

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[3]
sys.path.insert(0, str(PROJECT))
from cnn import integer as frozen

PLAN = PROJECT / 'cnn/hw_validation/plans/resource_budget_20261015'
CONTRACT = json.loads((PLAN / 'r256_candidate_contract_20261016.json').read_text(encoding='utf-8'))
INDEX = json.loads((HERE.parent / 'model_handoff_20261015/artifacts/layer_parameter_index.json').read_text(encoding='utf-8'))
PACKAGE = PROJECT / 'cnn/reports/qat_frozen_stem_g10_20261014_v1/package'
PAYLOAD = (PACKAGE / 'numeric_test.bin').read_bytes()
assert hashlib.sha256(PAYLOAD).hexdigest() == INDEX['model_key'].removeprefix('sha256:')
TABLES = {}
for item in INDEX['shared_tables']:
    data = PAYLOAD[item['offset']:item['offset'] + item['length']]
    assert hashlib.sha256(data).hexdigest() == item['sha256']
    if item['name'] in ('shared.sigmoid', 'shared.exp'):
        TABLES[item['name']] = struct.unpack('<' + 'H' * item['count'], data)
HEADS = CONTRACT['heads']
CELLS = CONTRACT['prediction']['positions']
THRESHOLDS = (32768, 32768)  # 沿已通过的诊断阈值，不在这批重新选模/调阈值。
DEFAULT = (-32768,) * 7


def rne(value, divisor):
    """标量整数RNE，完整负数/中点校验与冻结向量原语对拍。"""
    if divisor <= 0:
        raise ValueError('除数必须为正')
    quotient, remainder = divmod(abs(value), divisor)
    quotient += remainder > divisor - remainder or (remainder == divisor - remainder and quotient & 1)
    return -quotient if value < 0 else quotient


def sigmoid(raw):
    if not -32768 <= raw <= 32767:
        raise ValueError('logit必须为INT16')
    if raw <= -2048:
        return 0
    if raw >= 2048:
        return 65535
    address = rne(raw, 4) + 512
    return INDEX['sigmoid_upper'] if address == 1024 else TABLES['shared.sigmoid'][address]


def exponent(raw):
    raw = max(-1024, min(896, raw))
    return TABLES['shared.exp'][rne((raw + 1024) * 255, 1920)]


def cell_location(cell):
    if not 0 <= cell < CELLS:
        raise ValueError('cell超出0..3023')
    for scale, head in enumerate(HEADS):
        local = cell - head['first_cell_id']
        if 0 <= local < head['positions']:
            y, x = divmod(local, head['width'])
            return scale, y, x, head['stride']
    raise AssertionError('完整三尺度没有覆盖cell')


def decode(raw, x, y, stride):
    """只改变冻结decode的256x144裁边，不改变exp/size/half两级RNE。"""
    if len(raw) != 4 or any(not -32768 <= value <= 32767 for value in raw):
        raise ValueError('框回归须四项INT16')
    if stride not in (4, 8, 16) or not (0 <= x < 256 // stride and 0 <= y < 144 // stride):
        raise ValueError('grid/stride不属于R256')
    centers = ((raw[0] + x * 256) * stride, (raw[1] + y * 256) * stride)
    half = tuple(rne(rne(exponent(value) * stride, 4), 2) for value in raw[2:])
    box = (centers[0] - half[0], centers[1] - half[1],
           centers[0] + half[0], centers[1] + half[1])
    return tuple(max(0, min(limit, value)) for value, limit in zip(box, (65536, 36864) * 2))


def restore_source(box):
    if len(box) != 4 or any(not 0 <= value <= limit for value, limit in zip(box, (65536, 36864) * 2)):
        raise ValueError('源坐标还原只接裁边后的网络Q8')
    # 不先做旧5/2还原，不再二次舍入。结果端口仍是整数源像素<<8。
    return [max(0, min(limit, rne(value * 5, 256)))
            for value, limit in zip(box, (1280, 720) * 2)]


def result97(row):
    word = row['label'] | row['score_uint16'] << 1
    for index, pixel in enumerate(row['box_source']):
        if not 0 <= pixel <= (1280 if index % 2 == 0 else 720):
            raise ValueError('源坐标越界')
        word |= (pixel << 8) << (17 + 20 * index)
    assert 0 <= word < 1 << 97
    return f'{word:025x}'


def trace(overrides):
    """完整3024位置扫描；只稀疏保存输入，TopK在解码/零面积过滤之前。"""
    for cell, raw in overrides.items():
        cell_location(cell)
        if len(raw) != 7 or any(not isinstance(v, int) or not -32768 <= v <= 32767 for v in raw):
            raise ValueError('预测字段必须为七项INT16')
    heaps, events = [[], []], []
    for cell in range(CELLS):
        raw = overrides.get(cell, DEFAULT)
        probabilities = [sigmoid(value) for value in raw[4:]]
        _scale, y, x, stride = cell_location(cell)
        for label in (0, 1):
            score = rne(probabilities[0] * probabilities[label + 1], 65536)
            if score < THRESHOLDS[label]:
                continue
            heap = heaps[label]
            record = (score, -cell, stride, y, x, tuple(raw[:4]))
            if len(heap) < 128:
                heapq.heappush(heap, record)
                action = 'push'
            elif record[:2] > heap[0][:2]:
                heapq.heapreplace(heap, record)
                action = 'replace_root'
            else:
                action = 'reject_not_better'
            events.append({'label': label, 'cell_id': cell, 'score_uint16': score,
                           'action': action, 'heap_size': len(heap), 'root_key': list(heap[0][:2])})
    topk, nms, final = [], [], []
    for label, heap in enumerate(heaps):
        kept = []
        for rank, (score, negative_cell, stride, y, x, raw) in enumerate(sorted(heap, reverse=True)):
            box = decode(raw, x, y, stride)
            cell = -negative_cell
            valid = box[0] < box[2] and box[1] < box[3]
            topk.append({'label': label, 'cell_id': cell, 'score_uint16': score,
                         'rank': rank, 'raw4': list(raw), 'box_q8': list(box), 'geometry_valid': valid})
            comparisons = []
            if len(kept) == 32:
                decision = 'not_processed_class_cap'
            elif not valid:
                decision = 'drop_zero_area'
            else:
                suppress = False
                for previous in kept:
                    a = previous['box_q8']
                    inter = max(0, min(box[2], a[2]) - max(box[0], a[0])) * max(0, min(box[3], a[3]) - max(box[1], a[1]))
                    area_sum = (box[2] - box[0]) * (box[3] - box[1]) + (a[2] - a[0]) * (a[3] - a[1])
                    suppress = frozen._overlap_half(box, tuple(a))
                    assert suppress == (3 * inter > area_sum)
                    comparisons.append({'kept_cell_id': previous['cell_id'], 'intersection': inter,
                                        'area_sum': area_sum, 'suppress': suppress})
                    if suppress:
                        break
                decision = 'suppress' if suppress else 'keep'
                if not suppress:
                    row = {'label': label, 'score_uint16': score, 'cell_id': cell,
                           'box_q8': list(box), 'box_source': restore_source(box)}
                    kept.append(row)
                    final.append(row)
            nms.append({'label': label, 'cell_id': cell, 'decision': decision, 'comparisons': comparisons})
    return {'heap_events': events, 'sorted_top128': topk, 'nms': nms, 'final': final,
            'result_table_97_hex': [result97(row) for row in final],
            'box_count': len(final), 'result_status': 0,
            'logical_operations_not_cycles': {'cells': CELLS, 'sigmoid': CELLS * 3,
                                              'score_products': CELLS * 2, 'threshold_tests': CELLS * 2}}


def active(raw=(0, 0, 0, 0), logits=(2048, 2048, -32768)):
    return list(raw + logits)


def cases():
    """固定候选边界夹具，人工构造，不冒充CNN预测或识别精度。"""
    vectors = []
    def add(name, inputs, check):
        result = trace(inputs)
        check(result)
        vectors.append({'name': name, 'default_raw7': list(DEFAULT), 'cell_count': CELLS,
                        'overrides': [{'cell_id': cell, 'raw7': raw} for cell, raw in sorted(inputs.items())],
                        'expected': result})
    add('empty_complete_table', {}, lambda r: equal(r['box_count'], 0))
    add('threshold_inclusive', {0: active(logits=(0, 2048, -32768)),
                               1: active(logits=(0, 0, -32768))},
        lambda r: equal([(d['cell_id'], d['score_uint16']) for d in r['final']], [(0, 32768)]))
    boundary_cells = (0, 2303, 2304, 2879, 2880, 3023)
    add('first_last_and_scale_boundaries', {cell: active() for cell in boundary_cells},
        lambda r: equal([d['cell_id'] for d in r['sorted_top128']], list(boundary_cells)))
    add('two_classes_same_box', {0: active(logits=(2048, 2048, 2048))},
        lambda r: equal([d['label'] for d in r['final']], [0, 1]))
    add('same_class_duplicate', {0: active(raw=(512, 512, 0, 0)),
                                 1: active(raw=(256, 512, 0, 0))},
        lambda r: equal([d['cell_id'] for d in r['final']], [0]))
    add('top128_ties_each32_total64', {cell: active(logits=(2048, 2048, 2048)) for cell in range(130)},
        lambda r: (equal([d['cell_id'] for d in r['sorted_top128'] if d['label'] == 0], list(range(128))),
                   equal([sum(d['label'] == label for d in r['final']) for label in (0, 1)], [32, 32])))
    replacement = {cell: active(logits=(0, 2048, -32768)) for cell in range(128)}
    replacement.update({128: active(), 129: active()})
    add('full_heap_replaces_worst_two', replacement,
        lambda r: (equal(sum(d['action'] == 'replace_root' for d in r['heap_events']), 2),
                   equal({d['cell_id'] for d in r['sorted_top128']}, set(range(126)) | {128, 129})))
    add('clipped_zero_area', {0: active(raw=(32767, 32767, -1024, -1024))},
        lambda r: equal(r['box_count'], 0))
    invalid = {cell: active(raw=(32767, 32767, -1024, -1024)) for cell in range(128)}
    invalid[128] = active()
    add('zero_area_still_occupies_topk', invalid,
        lambda r: (equal(len(r['sorted_top128']), 128), equal(r['box_count'], 0)))
    add('source_rounding_collapsed_still_published', {3: active(raw=(0, 0, -1024, -1024))},
        lambda r: (equal(r['box_count'], 1), equal(r['final'][0]['box_source'][0], r['final'][0]['box_source'][2])))
    edges = (
        ('left_edge', 0, (0, 512, 896, 0), 0, 0),
        ('top_edge', 0, (512, 0, 0, 896), 1, 0),
        ('right_edge', 2303, (256, 0, 896, 0), 2, 65536),
        ('bottom_edge', 2303, (0, 256, 0, 896), 3, 36864),
    )
    for name, cell, raw, coordinate, expected in edges:
        add(name, {cell: active(raw=raw)},
            lambda r, coordinate=coordinate, expected=expected: equal(r['final'][0]['box_q8'][coordinate], expected))
    add('all_four_edges', {2880: active(raw=(2048, 1152, 896, 896))},
        lambda r: equal(r['final'][0]['box_source'], [0, 0, 1280, 720]))
    return vectors


def equal(actual, expected):
    if actual != expected:
        raise AssertionError((actual, expected))


def self_check():
    import numpy as np
    # 复用原始整数参考作独立比对；只运行算子，不调用CNN或重校准。
    raw_values = np.arange(-32768, 32768, dtype=np.int64)
    assert [sigmoid(int(v)) for v in raw_values] == frozen.sigmoid(raw_values).tolist()
    assert [exponent(int(v)) for v in raw_values] == frozen.exponent(raw_values).tolist()
    rne_count = 0
    for divisor in (1, 2, 4, 25, 256, 512, 1920, 65536):
        values = list(range(-1025, 1026)) + [divisor * q + divisor // 2 for q in range(-5, 6)]
        assert [rne(v, divisor) for v in values] == frozen.round_div_even(np.array(values), divisor).tolist()
        rne_count += len(values)
    decode_count = 0
    raws = ((0, 0, 0, 0), (-32768, -32768, -32768, -32768),
            (32767, 32767, 32767, 32767), (512, -256, -1024, 896), (2048, 1152, 896, 896))
    for cell in range(CELLS):
        _scale, y, x, stride = cell_location(cell)
        for raw in raws:
            old = frozen._decode(np.array(raw, dtype=np.int16), x, y, stride)
            expected = tuple(min(v, limit) for v, limit in zip(old, (65536, 36864) * 2))
            equal(decode(raw, x, y, stride), expected)
            decode_count += 1
    equal(restore_source([0, 0, 65536, 36864]), [0, 0, 1280, 720])
    equal(restore_source([128, 128, 384, 384]), [2, 2, 8, 8])
    equal(rne(52 * 5, 256), 1)
    equal(rne(52 * 5, 512) * 2, 2)  # 旧路径后乘2的明确反例。
    equal(frozen._overlap_half((0, 0, 6, 2), (2, 0, 8, 2)), False)
    equal(frozen._overlap_half((0, 0, 6, 2), (1, 0, 7, 2)), True)
    failures_checked = 0
    for callback in (lambda: cell_location(-1), lambda: cell_location(3024),
                     lambda: decode((0, 0, 0), 0, 0, 4),
                     lambda: decode((0, 0, 0, 0), 16, 0, 16),
                     lambda: trace({0: [0] * 6}), lambda: trace({3024: [0] * 7}),
                     lambda: restore_source([0, 0, 65537, 36864]),
                     lambda: sigmoid(32768), lambda: rne(1, 0)):
        try:
            callback()
        except ValueError:
            failures_checked += 1
        else:
            raise AssertionError('非法输入未拒绝')
    vectors = cases()
    return vectors, {'status': 'PASS_R256_GEOMETRY_NOT_CNN_VALUES', 'pipeline_cases': len(vectors),
                     'sigmoid_inputs_compared': 65536, 'exp_inputs_compared': 65536,
                     'rne_values_compared': rne_count, 'decode_cases_compared': decode_count,
                     'invalid_inputs_rejected': failures_checked}


def run():
    started = time.perf_counter()
    vectors, receipt = self_check()
    folder = HERE / 'geometry'
    folder.mkdir(exist_ok=True)
    contents = {'scope': 'synthetic full-cell head fixtures, not CNN predictions or accuracy',
                'candidate': CONTRACT['candidate_tag'], 'thresholds_uint16': list(THRESHOLDS),
                'topk_per_class': 128, 'max_per_class': 32, 'max_total': 64,
                'heads': HEADS, 'prediction_bytes': 42336, 'pipeline_cases': vectors,
                'analytic': {'source_q8_bounds': [65536, 36864], 'source_edges': [0, 0, 1280, 720],
                             'source_half_ties': {'network_q8': [128, 128, 384, 384], 'pixels': [2, 2, 8, 8]},
                             'double_round_counterexample': {'network_q8': 52, 'one_RNE': 1, 'old_RNE_then_times_two': 2},
                             'IoU_half_suppresses': False, 'IoU_above_half_suppresses': True}}
    output = folder / 'vectors.json'
    output.write_text(json.dumps(contents, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    receipt.update({'cpu_seconds': time.perf_counter() - started,
                    'payload_sha256': hashlib.sha256(PAYLOAD).hexdigest(),
                    'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                    'vectors_sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
                    'GPU_tasks': False, 'CNN_forwards': 0, 'training_updates': 0,
                    'calibration_updates': 0, 'RTL_run': False, 'TD_run': False,
                    'new_accuracy_measurement': False, 'formal_acceptance': False})
    (folder / 'self_check_receipt.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(receipt, ensure_ascii=False))


if __name__ == '__main__':
    run()
