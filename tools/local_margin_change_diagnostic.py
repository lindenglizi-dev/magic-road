#!/usr/bin/env python3
"""Explain fixed linear score changes with real ROI/product/accumulator vectors.

OpenCV HOG internals remain floating point. Integer descriptor/linear arithmetic
here is a diagnostic, not an integer HOG or RTL equivalence claim.
"""
import json
from pathlib import Path
import cv2
import numpy as np
from local_paired_diagnostic import PROJECT, PACKAGE, read_json, digest, dump
from local_fourgrid_diagnostic import DEFAULT_ANNOTATIONS, validate_confirmation_chain
from roi_dataset_tool import fpga_analysis_frame, fpga_resize_roi
from run_local_scene_pilot import MODEL_DIR, load_models, make_hog324, quantization_contract, score_roi, extract_variant
from summarize_local_target_diagnostics import verified

BASE = PROJECT/'evaluation/local_scene_pilots'
GRID = BASE/'intersection_2415171_fourgrid_v2'
SUMMARY = BASE/'intersection_2415171_diagnostic_summary_v2'
OUT = BASE/'intersection_2415171_margin_change_v1'


def main():
    if OUT.exists():
        raise ValueError('New output directory required')
    validate_confirmation_chain(DEFAULT_ANNOTATIONS, read_json(DEFAULT_ANNOTATIONS))
    for directory in (PACKAGE, GRID, SUMMARY):
        verified(directory)
    model, _, model_receipt = load_models(MODEL_DIR)
    hog = make_hog324()
    quant = quantization_contract(model['opencv_hog324'])
    weights = quant['weight_q']
    rows = read_json(GRID/'fourgrid_rows.json')
    alternate = {f['frame_index']: f for f in read_json(SUMMARY/'min_run1_frames.json')}
    package_frames = {f['frame_index']: f for f in read_json(PACKAGE/'package.json')['frames']}
    records, vectors, all_acc = [], {'weight_q': weights, 'bias_q': np.array([quant['bias_q']], dtype=np.int64)}, []
    float_weights = np.array(model['opencv_hog324']['folded_weights_on_raw_features'])
    for row in rows:
        frame = alternate[row['frame_index']]
        link = next((m for m in frame['matching'] if m['track_id'] == row['track_id']), None)
        if not row['matched'] or link is None:
            continue
        new = frame['candidates'][link['candidate_index']]
        gray = fpga_analysis_frame(cv2.imread(str(PACKAGE/package_frames[row['frame_index']]['path'])))
        identity = f'f{row["frame_index"]:06d}_{row["track_id"]}'
        pairs = []
        for name, box, expected in [('before', row['candidate_analysis_box'], row['C']),
                                    ('after', new['analysis_box'], new['score'])]:
            x0, y0, x1, y1 = box
            roi = fpga_resize_roi(gray[y0:y1+1, x0:x1+1])
            score = score_roi(roi, model, hog, quant)
            for key in ('hog324_q_score_integer', 'hog324_float_score', 'hog324_q_prediction', 'hog324_feature_sha256'):
                if score[key] != expected[key]:
                    raise AssertionError(f'Frozen score mismatch {identity} {name} {key}')
            if name == 'before' and __import__('hashlib').sha256(roi.tobytes()).hexdigest() != expected['roi_pixel_sha256']:
                raise AssertionError('Baseline ROI pixel identity mismatch')
            features = extract_variant(roi, 'opencv_hog324', hog)
            fq = np.rint(features * quant['feature_scale']).astype(np.int64)
            products = fq * weights
            accumulator = np.cumsum(np.r_[np.int64(quant['bias_q']), products], dtype=np.int64)
            if int(accumulator[-1]) != int(score['hog324_q_score_integer']):
                raise AssertionError('Score / sequential integer sum mismatch')
            all_acc.extend([int(accumulator.min()), int(accumulator.max())])
            for suffix, array in [('roi', roi), ('features_float', features), ('features_q', fq),
                                  ('products_q', products), ('acc_bias_first_q', accumulator)]:
                vectors[f'{identity}_{name}_{suffix}'] = array
            pairs.append((features, products, score))
        before, after = pairs
        delta = after[1] - before[1]
        score_delta = int(after[2]['hog324_q_score_integer']) - int(before[2]['hog324_q_score_integer'])
        if sum(map(int, delta)) != score_delta:
            raise AssertionError('Per-feature delta does not reconstruct score delta')
        float_delta = float((after[0]-before[0]) @ float_weights)
        observed = float(after[2]['hog324_float_score'])-float(before[2]['hog324_float_score'])
        if abs(float_delta - observed) > 1e-9:
            raise AssertionError('Float delta decomposition mismatch')
        top = sorted(range(324), key=lambda i: (-abs(int(delta[i])), i))[:12]
        records.append({'frame_index': row['frame_index'], 'track_id': row['track_id'], 'label': row['label'],
                        'before_box': row['candidate_analysis_box'], 'after_box': new['analysis_box'],
                        'before_score': before[2], 'after_score': after[2],
                        'classification_flipped': before[2]['hog324_q_prediction'] != after[2]['hog324_q_prediction'],
                        'integer_score_delta': score_delta, 'reconstructed_delta': sum(map(int,delta)),
                        'float_delta': float_delta,
                        'largest_feature_delta_terms': [{'feature_index': i, 'product_delta': int(delta[i])} for i in top],
                        'vector_prefix': identity})
    flips = [r for r in records if r['classification_flipped']]
    observed_peak = max(map(abs, all_acc), default=0)
    worst_bound = abs(quant['bias_q']) + 8191 * sum(abs(int(w)) for w in weights)
    OUT.mkdir()
    np.savez_compressed(OUT/'vectors.npz', **vectors)
    dump(OUT/'score_changes.json', records)
    report = {'scope': 'both baseline and min_run1 matched at IoU>=0.5; no best-overlap substitution',
              'paired_observations': len(records), 'classification_flips': len(flips),
              'flip_identities': [[r['frame_index'], r['track_id']] for r in flips],
              'score_and_delta_mismatches': 0,
              'float_q_label_mismatches': sum(r[name]['hog324_float_prediction'] != r[name]['hog324_q_prediction']
                                             for r in records for name in ('before_score','after_score')),
              'accumulator_order': 'bias first, then feature indices 0..323; signed int64 reference',
              'observed_peak_abs_accumulator': observed_peak,
              'observed_fits_signed32': observed_peak <= 2147483647,
              'conservative_13bit_feature_bound': worst_bound,
              'bound_fits_signed32': worst_bound <= 2147483647,
              'decision': 'On these paired crops the class changes exist in float and quantized paths; do not attribute them to quantization or change thresholds to patch individual frames.',
              'limits': ['Changes in weighted features explain arithmetic, not which visual object owns an edge.',
                         'Feature indices are OpenCV descriptor order; no unverified spatial bin interpretation.',
                         'Only matched-to-both subset; localization losses are reported by the crop-change diagnostic.',
                         'OpenCV float HOG plus integer linear layer; no RTL result, no integer gradient/bin validation.',
                         'Observed signed32 fit is not proof of a globally safe accumulator width.']}
    dump(OUT/'report.json', report)
    dump(OUT/'receipt.json', {'models':model_receipt,
         'source_receipts': {str(d.relative_to(PROJECT)):digest(d/'receipt.json') for d in (PACKAGE,GRID,SUMMARY)},
         'confirmation_receipt_sha256': digest(DEFAULT_ANNOTATIONS.parent/'confirmation_receipt.json'),
         'dependencies': {str(p.relative_to(PROJECT)):digest(p) for p in [Path(__file__), PROJECT/'tools/local_fourgrid_diagnostic.py', PROJECT/'tools/run_local_scene_pilot.py', PROJECT/'tools/roi_dataset_tool.py', PROJECT/'external_reference_exploration/opencv_hog_candidate_diagnostic.py']},
         'artifact_hashes': {p.name:digest(p) for p in sorted(OUT.iterdir()) if p.is_file()}})
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
