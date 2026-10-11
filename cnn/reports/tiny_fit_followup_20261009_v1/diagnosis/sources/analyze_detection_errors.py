"""Explain saved development detections; do not modify labels or train models."""
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path

import numpy as np

from .train import sha256


def ious(predictions, targets, crowd=False):
    a = np.array([row['box'] for row in predictions], dtype=float).reshape(-1, 4)
    b = np.array([row['box'] for row in targets], dtype=float).reshape(-1, 4)
    intersection = np.maximum(0, np.minimum(a[:, None, 2:], b[None, :, 2:])
                              - np.maximum(a[:, None, :2], b[None, :, :2])).prod(2)
    area = (a[:, 2:] - a[:, :2]).prod(1)[:, None]
    denominator = area if crowd else area + (b[:, 2:] - b[:, :2]).prod(1)[None, :] - intersection
    return intersection / np.maximum(denominator, 1e-30)


def match(predictions, matrix, ignored, threshold):
    used, true, false, skipped = set(), set(), set(), set()
    for index, row in enumerate(predictions):
        if row['score'] < threshold:
            continue
        available = [j for j in range(matrix.shape[1]) if j not in used]
        best = max(available, key=lambda j: (matrix[index, j], -j), default=None)
        if best is not None and matrix[index, best] >= .5:
            used.add(best)
            true.add(index)
        elif not np.any(matrix[index] >= .5) and ignored[index]:
            skipped.add(index)
        else:
            false.add(index)
    return used, true, false, skipped


def diagnose(result):
    ground, predictions, regions = defaultdict(list), defaultdict(list), defaultdict(list)
    for row in result['truth']:
        ground[row['image_id']].append(row)
    for index, row in enumerate(result['predictions']):
        predictions[row['image_id']].append((index, row))
    for row in result['ignores']:
        regions[row['image_id']].append(row)
    counts, sizes, scenes, examples = defaultdict(Counter), defaultdict(Counter), defaultdict(Counter), {}
    gt_totals, allowed = Counter(), Counter()
    for image_id in sorted(set(ground) | set(predictions)):
        local = [row for _, row in sorted(predictions[image_id], key=lambda item: (-item[1]['score'], item[0]))]
        for label, name in enumerate(('person', 'vehicle')):
            gt = [row for row in ground[image_id] if row['label'] == label]
            pred = [row for row in local if row['label'] == label]
            other_gt = [row for row in ground[image_id] if row['label'] != label]
            other_pred = [row for row in local if row['label'] != label]
            matrix = ious(pred, gt)
            foreign = ious(pred, other_gt)
            other_support = ious(other_pred, gt)
            ignored = np.zeros(len(pred), dtype=bool)
            for region in regions[image_id]:
                if region['label'] in (-1, label):
                    ignored |= ious(pred, [region], region.get('crowd', False))[:, 0] >= .5
            used, true, false, skipped = match(pred, matrix, ignored, .5)
            used_low, true_low, false_low, _ = match(pred, matrix, ignored, 0.)
            counts[name].update(gt=len(gt), tp=len(true), fp=len(false), fn=len(gt)-len(used),
                                ignored=len(skipped), tp_at_retained_floor=len(true_low),
                                fp_at_retained_floor=len(false_low),
                                pairs_at_32_retained=int(len(pred) == 32),
                                frames_over_gt32=int(len(gt) > 32))
            gt_totals[name] += len(gt)
            allowed[name] += min(32, len(gt))
            for j, target in enumerate(gt):
                if j in used:
                    reason = 'tp'
                elif j in used_low:
                    reason = 'fn_recovered_by_lowering_score_one_to_one'
                elif np.any(matrix[:, j] >= .5):
                    reason = 'fn_same_class_candidate_competes_for_other_GT'
                elif np.any(other_support[:, j] >= .5):
                    reason = 'fn_other_class_box_support'
                elif np.any(matrix[:, j] >= .25):
                    reason = 'fn_same_class_localization_support_IoU_025_to_05'
                else:
                    reason = 'fn_no_retained_support_cause_unresolved'
                height = target['box'][3] - target['box'][1]
                size = 'height_le8' if height <= 8 else 'height_8_to16' if height <= 16 else 'height_gt16'
                sizes[name+'/'+size].update(total=1)
                sizes[name+'/'+size][reason] += 1
                scene = Path(image_id).parent.name
                scenes[name+'/'+scene].update(total=1)
                scenes[name+'/'+scene][reason] += 1
                if reason != 'tp':
                    counts[name][reason] += 1
                    examples.setdefault(name+'/'+reason, dict(target, reason=reason))
            for index in sorted(false):
                if np.any(matrix[index] >= .5):
                    reason = 'fp_duplicate_same_class_overlap'
                elif np.any(foreign[index] >= .5):
                    reason = 'fp_other_class_GT_overlap'
                elif np.any(matrix[index] >= .25):
                    reason = 'fp_same_class_localization_support_IoU_025_to_05'
                else:
                    reason = 'fp_no_GT_support_background_or_missing_annotation_unresolved'
                counts[name][reason] += 1
                examples.setdefault(name+'/'+reason, dict(pred[index], reason=reason))
    for name in ('person', 'vehicle'):
        expected = result['diagnostic_metrics_at_0_5']['classes'][name]
        assert all(counts[name][key] == expected[key] for key in ('tp', 'fp', 'fn', 'ignored')), name
    return dict(classes=dict(counts), size_groups=dict(sizes), scene_groups=dict(scenes),
                raw_count_max32_recall_ceiling={name: allowed[name]/gt_totals[name] for name in gt_totals},
                examples=dict(examples),
                limitation='Exact greedy TP/FP/FN at score0.5; remaining categories are geometric evidence, not causal proof. Retained score floor~0.05; raw pre-TopK/NMS logits not inspected here; unmatched prediction is not automatically background.')


def self_check():
    from .metrics import report
    gt = [dict(image_id='a', label=0, box=[0, 0, 4, 4]), dict(image_id='a', label=0, box=[10, 10, 14, 14]),
          dict(image_id='a', label=1, box=[20, 20, 24, 24])]
    pred = [dict(gt[0], score=.9), dict(gt[0], score=.8), dict(gt[1], score=.2), dict(gt[2], score=.9)]
    result = dict(truth=gt, predictions=pred, ignores=[],
                  diagnostic_metrics_at_0_5=report(pred, gt, thresholds=(.5, .5)))
    answer = diagnose(result)['classes']['person']
    assert answer['tp'] == 1 and answer['fp_duplicate_same_class_overlap'] == 1
    assert answer['fn_recovered_by_lowering_score_one_to_one'] == 1
    print('PASS saved-prediction matching and low-score/duplicate diagnosis')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--evaluation', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    self_check()
    if args.self_test:
        return
    if args.evaluation or args.output:
        if not args.evaluation or not args.output:
            parser.error('--evaluation and --output must be supplied together')
        result = diagnose(json.loads(args.evaluation.read_text(encoding='utf-8')))
        with args.output.open('x', encoding='utf-8') as stream:
            json.dump(dict(status='diagnostic_not_formal_acceptance',
                input_sha256=sha256(args.evaluation), reports=result,
                training_started=False), stream, ensure_ascii=False, indent=2)
        print(json.dumps(dict(classes=result['classes'], sizes=result['size_groups'],
                              max32_ceiling=result['raw_count_max32_recall_ceiling'])))
        return
    root = Path(__file__).resolve().parent.parent
    paths = {'epoch7': root/'cnn/reports/supervised5_baseline_20261005/epoch7_full_val.json',
             'epoch12': root/'cnn/reports/supervised5_oct5/epoch12_full_val.json'}
    reports = {name: json.loads(path.read_text(encoding='utf-8')) for name, path in paths.items()}
    for key in ('truth', 'ignores', 'dataset_sha256', 'evaluated_image_content_sha256', 'postprocess_contract'):
        assert reports['epoch7'][key] == reports['epoch12'][key], key
    output = dict(status='saved_full_validation_error_diagnosis_not_formal_acceptance',
                  reports={name: diagnose(value) for name, value in reports.items()},
                  input_sha256={name: sha256(path) for name, path in paths.items()},
                  source_sha256=sha256(Path(__file__)), training_started=False)
    path = root/'cnn/reports/error_diagnosis_20261006/saved_prediction_errors.json'
    with path.open('x', encoding='utf-8') as stream:
        json.dump(output, stream, ensure_ascii=False, indent=2)
    for name, value in output['reports'].items():
        print(name, json.dumps(dict(classes=value['classes'], size_groups=value['size_groups'],
                                   max32_ceiling=value['raw_count_max32_recall_ceiling'])))


if __name__ == '__main__':
    main()
