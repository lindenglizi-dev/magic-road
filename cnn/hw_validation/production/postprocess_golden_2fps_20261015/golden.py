"""Frozen decoder/Top128/NMS stage vectors; CPU only, no shared-source edits."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import heapq
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
OUT = Path(__file__).resolve().parent
PRIOR = ROOT / 'cnn/hw_validation/production/model_handoff_20261015'
PACKAGE = ROOT / 'cnn/reports/qat_frozen_stem_g10_20261014_v1/package'
PAYLOAD = 'b35d4a66a69e441dc29bc60c7e3f507661f48da5f33b810d7340f6ed17a65145'
INTEGER_SHA = '441b91d86895fb0c0337583325fb9cc39624026a6759d39da51aaab49a5ca040'
CONTRACT_SHA = '5cff8d5a406dc235a0d5d35cbf72903c0d6b48477e99a0cabf58251331f3a681'
THRESHOLDS = (32768, 32768)
STRIDES = (4, 8, 16)
SHAPES = ((72, 128, 7), (36, 64, 7), (18, 32, 7))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def save(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False)
        stream.write('\n')


def jsonl(path, rows):
    with Path(path).open('x', encoding='utf-8') as stream:
        for row in rows:
            stream.write(json.dumps(row, separators=(',', ':')) + '\n')


def hex_lines(path, words, bits):
    with Path(path).open('x', encoding='ascii') as stream:
        for word in words:
            if not 0 <= word < 1 << bits:
                raise ValueError('packed word outside declared width')
            stream.write(f'{word:0{(bits+3)//4}x}\n')


def unsigned(value, bits):
    value = int(value)
    if not 0 <= value < 1 << bits:
        raise ValueError('unsigned field overflow')
    return value


def candidate160(row):
    word = 0
    for i, value in enumerate(row['raw']):
        if not -32768 <= value <= 32767:
            raise ValueError('raw head outside INT16')
        word |= (value & 65535) << (16*i)
    for key, bit, width in (('cell_id', 64, 14), ('score_uint16', 78, 16),
                            ('label', 94, 1), ('scale_index', 95, 2), ('x', 97, 7), ('y', 104, 7)):
        word |= unsigned(row[key], width) << bit
    return word


def decoded160(row):
    word = sum(unsigned(value, 18) << (18*i) for i, value in enumerate(row['box_q8']))
    return (word | unsigned(row['cell_id'], 14) << 72 | unsigned(row['score_uint16'], 16) << 86
            | unsigned(row['label'], 1) << 102 | int(row['geometry_valid']) << 103)


def result97(detection):
    word = unsigned(detection['label'], 1) | unsigned(detection['score_uint16'], 16) << 1
    for i, pixel in enumerate(detection['box_source']):
        if not 0 <= pixel <= (1280 if i % 2 == 0 else 720):
            raise ValueError('source coordinate outside source frame')
        word |= unsigned(pixel << 8, 20) << (17+20*i)
    return word


def trace(heads):
    """Observe the existing algorithm, then assert its final list exactly matches postprocess."""
    import numpy as np
    from cnn import integer as ref
    expected = ref.postprocess(heads, THRESHOLDS)
    heaps = [[], []]
    candidates, heap_events, cell_scores, topk, nms, final = [], [], [], [], [], []
    counts = Counter(cells=12096, sigmoid_lookups=36288, score_products=24192, threshold_tests=24192)
    cell = 0
    for scale, (head, stride) in enumerate(zip(heads, STRIDES, strict=True)):
        probabilities = ref.sigmoid(head[..., 4:]).astype(np.int64)
        scores = ref.round_div_even(probabilities[..., :1] * probabilities[..., 1:], 65536)
        for y, x in np.ndindex(head.shape[:2]):
            cell_scores.append(dict(cell_id=cell, scale_index=scale, y=y, x=x,
                probabilities=list(map(int, probabilities[y, x])), scores=list(map(int, scores[y, x]))))
            for label in (0, 1):
                score = int(scores[y, x, label])
                if score < THRESHOLDS[label]:
                    continue
                raw = tuple(map(int, head[y, x, :4]))
                row = dict(label=label, cell_id=cell, score_uint16=score,
                           scale_index=scale, stride=stride, y=y, x=x, raw=list(raw))
                record = (score, -cell, stride, y, x, raw)
                heap = heaps[label]
                root_before = list(heap[0][:2]) if heap else None
                if len(heap) < 128:
                    heapq.heappush(heap, record)
                    action = 'push'
                elif record[:2] > heap[0][:2]:
                    heapq.heapreplace(heap, record)
                    action = 'replace_root'
                else:
                    action = 'reject_not_better'
                counts[action] += 1
                # This offline annotation is not an extra required RTL decode-before-TopK stage.
                row['box_q8_annotation_only'] = list(ref._decode(np.array(raw, dtype=np.int16), x, y, stride))
                candidates.append(row)
                heap_events.append(dict(label=label, cell_id=cell, action=action, root_before=root_before,
                    root_after=list(heap[0][:2]), heap_size=len(heap)))
            cell += 1
    assert cell == 12096
    for label, heap in enumerate(heaps):
        kept = []
        for rank, (score, negative_cell, stride, y, x, raw) in enumerate(sorted(heap, reverse=True)):
            box = ref._decode(np.array(raw, dtype=np.int16), x, y, stride)
            row = dict(label=label, cell_id=-negative_cell, score_uint16=score,
                scale_index=STRIDES.index(stride), stride=stride, y=y, x=x, raw=list(raw),
                box_q8=list(box), geometry_valid=box[0] < box[2] and box[1] < box[3], rank=rank)
            topk.append(row)
        class_rows = [row for row in topk if row['label'] == label]
        counts['decode_topk'] += len(class_rows)
        for row in class_rows:
            box = tuple(row['box_q8'])
            event = dict(label=label, cell_id=row['cell_id'], rank=row['rank'], comparisons=[])
            if len(kept) == 32:
                event['decision'] = 'not_processed_class_cap'
            elif not row['geometry_valid']:
                event['decision'] = 'drop_zero_area'
                counts['zero_area'] += 1
            else:
                suppress = False
                for previous_id, previous in kept:
                    width = max(0, min(box[2], previous[2])-max(box[0], previous[0]))
                    height = max(0, min(box[3], previous[3])-max(box[1], previous[1]))
                    inter = width*height
                    area_a = (box[2]-box[0])*(box[3]-box[1])
                    area_b = (previous[2]-previous[0])*(previous[3]-previous[1])
                    suppress = ref._overlap_half(box, previous)
                    assert suppress == (3*inter > area_a+area_b)
                    counts['nms_pair_comparisons'] += 1
                    event['comparisons'].append(dict(kept_cell_id=previous_id,
                        intersection=inter, area_a=area_a, area_b=area_b, suppress=suppress))
                    if suppress:
                        break
                event['decision'] = 'suppress' if suppress else 'keep'
                if not suppress:
                    kept.append((row['cell_id'], box))
                    source = ref.round_div_even(np.array(box, dtype=np.int64)*5, 512).tolist()
                    final.append(dict(label=label, score_uint16=row['score_uint16'],
                        cell_id=row['cell_id'], box_q8=list(box), box_source=source))
            nms.append(event)
    assert final == expected, 'stage instrumentation differs from shared postprocess'
    return dict(candidates=candidates, cell_scores=cell_scores, heap_events=heap_events,
                sorted_top128=topk, nms=nms, final=final, logical_operation_counts=dict(counts))


def empty_heads():
    import numpy as np
    return [np.full(shape, -32768, dtype=np.int16) for shape in SHAPES]


def activate(heads, cell, raw=(0, 0, 0, 0), logits=(2048, 2048, -32768)):
    sizes = (9216, 2304, 576)
    if not 0 <= cell < sum(sizes):
        raise ValueError('cell outside full graph')
    scale = 0
    while cell >= sizes[scale]:
        cell -= sizes[scale]
        scale += 1
    y, x = divmod(cell, SHAPES[scale][1])
    heads[scale][y, x] = (*raw, *logits)


def boundary_cases():
    """Sparse full-shape heads plus direct analytic operator fixtures, never model predictions."""
    import numpy as np
    from cnn import integer as ref
    cases = []
    def add(name, heads, check):
        result = trace(heads)
        check(result)
        records = [dict(cell_id=sum(h.shape[0]*h.shape[1] for h in heads[:s])+y*h.shape[1]+x,
                        raw7=list(map(int, h[y, x])))
                   for s, h in enumerate(heads) for y, x in np.ndindex(h.shape[:2])
                   if not np.all(h[y, x] == -32768)]
        cases.append(dict(name=name, input_encoding='full SHAPES default INT16_MIN plus sparse overrides',
            sparse_heads=records, stages=result))
    heads = empty_heads()
    add('all_low_empty_complete_table', heads, lambda r: assert_equal(len(r['final']), 0))
    heads = empty_heads()
    activate(heads, 0, logits=(0, 2048, -32768))
    activate(heads, 1, logits=(0, 0, -32768))
    add('threshold_equal_inclusive_and_below', heads,
        lambda r: assert_equal([(d['cell_id'], d['score_uint16']) for d in r['final']], [(0, 32768)]))
    heads = empty_heads()
    for cell in range(130):
        activate(heads, cell, logits=(2048, 2048, 2048))
    add('top128_ties_and_each32_total64', heads, lambda r: (
        assert_equal([d['cell_id'] for d in r['sorted_top128'] if d['label'] == 0], list(range(128))),
        assert_equal([sum(d['label'] == c for d in r['final']) for c in (0, 1)], [32, 32])))
    heads = empty_heads()
    for cell in range(128):
        activate(heads, cell, logits=(0, 2048, -32768))
    activate(heads, 128)
    activate(heads, 129)
    add('full_heap_replaces_worst_two', heads, lambda r: (
        assert_equal(r['logical_operation_counts']['replace_root'], 2),
        assert_equal({d['cell_id'] for d in r['sorted_top128']}, set(range(126)) | {128, 129})))
    heads = empty_heads()
    for cell in (9215, 9216, 11520):
        activate(heads, cell)
    add('cell_order_cross_scale', heads,
        lambda r: assert_equal([d['cell_id'] for d in r['sorted_top128']], [9215, 9216, 11520]))
    heads = empty_heads()
    activate(heads, 0, logits=(2048, 2048, 2048))
    add('person_vehicle_same_box_not_suppressed', heads,
        lambda r: assert_equal([d['label'] for d in r['final']], [0, 1]))
    heads = empty_heads()
    activate(heads, 0, raw=(512, 512, 0, 0))
    activate(heads, 1, raw=(256, 512, 0, 0))
    add('same_class_duplicate_suppressed', heads, lambda r: (
        assert_equal([d['cell_id'] for d in r['final']], [0]),
        assert_equal(r['nms'][1]['decision'], 'suppress')))
    heads = empty_heads()
    activate(heads, 0, raw=(32767, 32767, -1024, -1024))
    add('zero_area_after_clipping', heads, lambda r: (
        assert_equal(len(r['final']), 0), assert_equal(r['nms'][0]['decision'], 'drop_zero_area')))
    heads = empty_heads()
    for cell in range(128):
        activate(heads, cell, raw=(32767, 32767, -1024, -1024))
    activate(heads, 128)
    add('zero_area_not_removed_before_topk', heads, lambda r: (
        assert_equal(len(r['sorted_top128']), 128), assert_equal(len(r['final']), 0)))
    heads = empty_heads()
    activate(heads, 3, raw=(0, 0, -1024, -1024))
    add('source_rounding_degenerate_kept_by_current_reference', heads, lambda r: (
        assert_equal(len(r['final']), 1),
        assert_equal(r['final'][0]['box_source'][0], r['final'][0]['box_source'][2])))
    analytic = []
    for name, a, b, expected in (
        ('iou_equal_half_not_suppressed', (0, 0, 6, 2), (2, 0, 8, 2), False),
        ('iou_above_half_suppressed', (0, 0, 6, 2), (1, 0, 7, 2), True),
        ('zero_area_overlap_false', (2, 0, 2, 2), (0, 0, 6, 2), False),
    ):
        actual = ref._overlap_half(a, b)
        assert actual is expected
        analytic.append(dict(name=name, operator='_overlap_half', boxes=[a, b], suppress=actual))
    for name, raw, equivalent in (
        ('tw_th_below_clip', (0, 0, -32768, -32768), (0, 0, -1024, -1024)),
        ('tw_th_above_clip', (0, 0, 32767, 32767), (0, 0, 896, 896)),
    ):
        a = ref._decode(np.array(raw, dtype=np.int16), 10, 10, 4)
        b = ref._decode(np.array(equivalent, dtype=np.int16), 10, 10, 4)
        assert a == b
        analytic.append(dict(name=name, operator='_decode', raw=raw, equivalent_raw=equivalent,
                             x=10, y=10, stride=4, box_q8=a))
    for name, box, expected in (
        ('source_four_frame_edges', (0, 0, 131072, 73728), (0, 0, 1280, 720)),
        ('source_RNE_half_ties', (256, 256, 768, 768), (2, 2, 8, 8)),
    ):
        source = tuple(map(int, ref.round_div_even(np.array(box)*5, 512)))
        assert source == expected
        detection = dict(label=1, score_uint16=32768, box_source=list(source))
        analytic.append(dict(name=name, operator='source_RNE_and_result97', box_q8=box,
                             box_source=source, packed97_hex=f'{result97(detection):025x}'))
    return dict(scope='deterministic tests, not camera/model accuracy', pipeline_cases=cases,
                analytic_cases=analytic, all_passed=True)


def assert_equal(a, b):
    if a != b:
        raise AssertionError((a, b))


def emit_trace(folder, heads, result):
    folder.mkdir()
    words = (sum((int(v)&65535) << (16*i) for i, v in enumerate(raw))
             for head in heads for raw in head.reshape(-1, 7))
    hex_lines(folder / 'heads_cell_order_112.hex', words, 112)
    jsonl(folder / 'score_stream.jsonl', result['cell_scores'])
    jsonl(folder / 'candidates.jsonl', result['candidates'])
    jsonl(folder / 'heap_events.jsonl', result['heap_events'])
    jsonl(folder / 'top128_sorted.jsonl', result['sorted_top128'])
    jsonl(folder / 'nms_events.jsonl', result['nms'])
    hex_lines(folder / 'candidate_raw_160.hex', map(candidate160, result['candidates']), 160)
    hex_lines(folder / 'top128_raw_160.hex', map(candidate160, result['sorted_top128']), 160)
    hex_lines(folder / 'top128_decoded_160.hex', map(decoded160, result['sorted_top128']), 160)
    hex_lines(folder / 'result_table_97.hex', map(result97, result['final']), 97)
    save(folder / 'final.json', dict(result_status=0, box_count=len(result['final']),
        detections=result['final'], logical_operation_counts=result['logical_operation_counts'],
        frame_metadata='source-held framing is external; no synthetic actual capture timestamp',
        complete_empty_valid=not result['final']))


def build():
    import numpy as np
    from cnn.hw_validation.production.model_handoff_20261015 import handoff
    from cnn.hw_validation.production.trained_integer import load_package
    started = time.perf_counter()
    _, runtime = handoff.initialize()
    frozen = {}
    for path, expected in ((ROOT/'cnn/integer.py', INTEGER_SHA),
            (ROOT/'cnn/hw_validation/production/deployment_contract.json', CONTRACT_SHA),
            (PACKAGE/'numeric_test.bin', PAYLOAD)):
        if sha(path) != expected:
            raise ValueError('shared numerical identity changed: ' + str(path))
        frozen[str(path)] = expected
    old_receipt = read(PRIOR/'artifacts/receipt.json')
    rgb_path = PRIOR/'artifacts/golden_prefix/input_rgb_hwc.npy'
    if sha(rgb_path) != old_receipt['artifact_sha256']['golden_prefix/input_rgb_hwc.npy']:
        raise ValueError('real preprocessed image differs from previous handoff')
    for path in (rgb_path, PRIOR/'artifacts/golden_prefix_index.json',
                 ROOT/'cnn/hw_validation/production/trained_integer.py',
                 ROOT/'cnn/hw_validation/production/graph.py', PACKAGE/'manifest.json', Path(__file__)):
        frozen[str(path)] = sha(path)
    model, manifest = load_package(PACKAGE)
    assert manifest['payload_sha256'] == PAYLOAD
    folder = OUT/'artifacts'
    folder.mkdir(exist_ok=False)
    rgb = np.load(rgb_path, allow_pickle=False)
    if rgb.dtype != np.uint8 or rgb.shape != (288, 512, 3):
        raise ValueError('preprocessed input format changed')
    # Only full CNN forward in this batch; no earlier cache or prefix is re-exported.
    inference_started = time.perf_counter()
    heads, _statistics, _values = model.forward((rgb.astype(np.int16)-128).astype(np.int8))
    inference_seconds = time.perf_counter()-inference_started
    for stride, head in zip(STRIDES, heads, strict=True):
        np.save(folder/f'heads_s{stride}.npy', head, allow_pickle=False)
        (folder/f'heads_s{stride}.bin').write_bytes(head.astype('<i2').tobytes())
    result = trace(heads)
    emit_trace(folder/'real_image', heads, result)
    evaluation_path = PACKAGE.parent/'evaluation/development17.json'
    prior = read(evaluation_path)
    image_path = read(PRIOR/'artifacts/golden_prefix_index.json')['input_image']
    expected = [dict(label=row['label'], score_uint16=round(row['score']*65536),
                     box_q8=[round(v*256) for v in row['box']]) for row in prior['predictions']
                if row['image_id'] == image_path and row['score'] >= .5]
    observed = [{key: row[key] for key in ('label', 'score_uint16', 'box_q8')} for row in result['final']]
    key = lambda row: (row['label'], -row['score_uint16'], row['box_q8'])
    assert sorted(expected, key=key) == sorted(observed, key=key), 'existing same-image diagnostic results differ'
    frozen[str(evaluation_path)] = sha(evaluation_path)
    boundary = boundary_cases()
    save(folder/'boundaries.json', boundary)
    for case in boundary['pipeline_cases']:
        test_heads = empty_heads()
        for row in case['sparse_heads']:
            activate(test_heads, row['cell_id'], raw=row['raw7'][:4], logits=row['raw7'][4:])
        emit_trace(folder/case['name'], test_heads, case['stages'])
    for path, expected_hash in frozen.items():
        if sha(path) != expected_hash:
            raise ValueError('input/shared source changed during run: ' + path)
    save(folder/'receipt.json', dict(status='PASS_CPU_POSTPROCESS_GOLDEN_NOT_RTL',
        payload_sha256=PAYLOAD, package_manifest_status=manifest['status'],
        checkpoint_sha256=manifest['provenance']['checkpoint_sha256'],
        input_image=image_path, thresholds_uint16=THRESHOLDS,
        real_image_box_count=len(result['final']), old_same_image_outputs_exact=True,
        deterministic_pipeline_cases=len(boundary['pipeline_cases']),
        deterministic_analytic_cases=len(boundary['analytic_cases']),
        full_integer_CNN_forwards=1, CPU_forward_seconds=inference_seconds,
        CPU_total_seconds=time.perf_counter()-started, runtime=runtime,
        real_image_logical_operation_counts=result['logical_operation_counts'],
        worst_case_logical_bounds=dict(cells=12096, sigmoid_lookups=36288, score_products=24192,
            threshold_tests=24192, heap_key_comparisons=362880,
            heap_extract_comparisons=3584, decode_topk=256, nms_pair_comparisons=6944,
            final_boxes=64, note='bounded operations, NOT measured FPGA cycles'),
        input_sha256=frozen,
        artifact_sha256={p.relative_to(folder).as_posix(): sha(p) for p in folder.rglob('*') if p.is_file()},
        CUDA_initialized=False, training_updates=0, new_accuracy_measurement=False,
        RTL_cycles=None, RTL_run=False, TD_run=False, bitstream_or_board=False,
        model_id32='C7 binding not assigned here', formal_acceptance=False))
    print(json.dumps(dict(status='PASS_CPU_POSTPROCESS_GOLDEN_NOT_RTL',
        boxes=len(result['final']), pipeline_cases=len(boundary['pipeline_cases']),
        analytic_cases=len(boundary['analytic_cases']), CPU_forward_seconds=inference_seconds)), flush=True)


def verify():
    from cnn.hw_validation.production.model_handoff_20261015 import handoff
    handoff.initialize()
    import numpy as np
    folder = OUT/'artifacts'
    receipt = read(folder/'receipt.json')
    for path, expected in receipt['input_sha256'].items():
        assert sha(path) == expected, path
    for path, expected in receipt['artifact_sha256'].items():
        assert sha(folder/path) == expected, path
    heads = [np.load(folder/f'heads_s{s}.npy', allow_pickle=False) for s in STRIDES]
    result = trace(heads)  # Reuses saved heads; never runs another CNN forward.
    assert result['final'] == read(folder/'real_image/final.json')['detections']
    assert json.loads(json.dumps(boundary_cases())) == read(folder/'boundaries.json')
    print('PASS_POSTPROCESS_VERIFY_SAVED_HEADS_NO_CNN_FORWARD_NO_GPU', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build', action='store_true')
    args = parser.parse_args()
    build() if args.build else verify()
