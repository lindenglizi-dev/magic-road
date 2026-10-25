"""Saved-head regression and compact boundary delivery; never invokes a CNN forward."""
import json
from pathlib import Path
import time

import golden as g


def main():
    started = time.perf_counter()
    g.verify()
    import numpy as np
    from cnn.integer import sigmoid, round_div_even
    folder = g.OUT/'artifacts'
    receipt = g.read(folder/'receipt.json')
    checked_records = 0
    for case in [folder/'real_image', *[folder/r['name'] for r in g.read(folder/'boundaries.json')['pipeline_cases']]]:
        final = g.read(case/'final.json')
        words = [int(line, 16) for line in (case/'result_table_97.hex').read_text().splitlines()]
        assert len(words) == final['box_count'] <= 64 and final['result_status'] == 0
        for word, row in zip(words, final['detections'], strict=True):
            assert word < 1 << 97 and (word & 1) == row['label']
            assert (word >> 1) & 65535 == row['score_uint16']
            assert [(word >> (17+20*i)) & ((1 << 20)-1) for i in range(4)] == [v << 8 for v in row['box_source']]
            checked_records += 1
        raw = [json.loads(line) for line in (case/'top128_sorted.jsonl').read_text().splitlines()]
        words = [int(line, 16) for line in (case/'top128_raw_160.hex').read_text().splitlines()]
        decoded = [int(line, 16) for line in (case/'top128_decoded_160.hex').read_text().splitlines()]
        for row, word, boxword in zip(raw, words, decoded, strict=True):
            assert word == g.candidate160(row) and word >> 111 == 0
            assert (word >> 64) & 16383 == row['cell_id']
            assert (word >> 78) & 65535 == row['score_uint16']
            assert [(word >> (16*i)) & 65535 for i in range(4)] == [v & 65535 for v in row['raw']]
            assert [(boxword >> (18*i)) & ((1 << 18)-1) for i in range(4)] == row['box_q8']
            assert boxword >> 104 == 0
            checked_records += 1
        for label in (0, 1):
            local = [row for row in raw if row['label'] == label]
            assert len(local) <= 128
            assert [(r['score_uint16'], -r['cell_id']) for r in local] == sorted(
                [(r['score_uint16'], -r['cell_id']) for r in local], reverse=True)
    assert int(round_div_even(np.int64(65535)*65535, 65536)) == 65534
    assert int(round_div_even(np.int64(32768)*65535, 65536)) == 32768
    assert list(map(int, sigmoid(np.array([-2048, 0, 2048], dtype=np.int16)))) == [0, 32768, 65535]
    rejected = []
    for name, action in (
        ('source_coordinate_overflow', lambda: g.result97(dict(label=0, score_uint16=1, box_source=[0, 0, 1281, 720]))),
        ('class_overflow', lambda: g.result97(dict(label=2, score_uint16=1, box_source=[0, 0, 1, 1]))),
        ('score_overflow', lambda: g.result97(dict(label=0, score_uint16=65536, box_source=[0, 0, 1, 1]))),
        ('cell_id_overflow', lambda: g.activate(g.empty_heads(), 12096)),
    ):
        try:
            action()
        except ValueError:
            rejected.append(name)
        else:
            raise AssertionError('invalid packing/input accepted: ' + name)
    boundaries = g.read(folder/'boundaries.json')
    compact = dict(full_head_shapes=g.SHAPES, default_int16_value=-32768,
        input_format='sparse raw7 overrides in global cell order; no full zero/low-score tensor copies needed',
        thresholds_uint16=g.THRESHOLDS, analytic_cases=boundaries['analytic_cases'], pipeline_cases=[])
    for case in boundaries['pipeline_cases']:
        stages = case['stages']
        cells = {row['cell_id'] for row in case['sparse_heads']}
        compact['pipeline_cases'].append(dict(name=case['name'], sparse_heads=case['sparse_heads'],
            scores_at_overridden_cells=[r for r in stages['cell_scores'] if r['cell_id'] in cells],
            expected_top128=stages['sorted_top128'], expected_heap_events=stages['heap_events'],
            expected_nms_events=stages['nms'], expected_final=stages['final'],
            expected_result97_hex=[f'{g.result97(r):025x}' for r in stages['final']],
            logical_operation_counts=stages['logical_operation_counts']))
    g.save(g.OUT/'boundary_vectors.json', compact)
    result = dict(status='PASS_POSTPROCESS_PACKING_AND_STAGE_REGRESSION',
        packed_records_checked=checked_records, negative_cases_rejected=rejected,
        pipeline_cases=receipt['deterministic_pipeline_cases'], analytic_cases=receipt['deterministic_analytic_cases'],
        compact_boundary_bytes=(g.OUT/'boundary_vectors.json').stat().st_size,
        compact_boundary_sha256=g.sha(g.OUT/'boundary_vectors.json'),
        source_sha256=g.sha(__file__), additional_CNN_forwards=0, seconds=time.perf_counter()-started)
    g.save(g.OUT/'validation.json', result)
    print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
