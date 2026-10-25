"""Two-class detection metrics; validation thresholds are never fitted on test.

Rows contain image_id, label (0/1), box (continuous xyxy); predictions also
contain score in [0,1]. Ignore rows may have label=-1 and crowd=True (IoA).
This is an explicit road-protocol evaluator, not a replacement for COCOeval.
"""
from __future__ import annotations

import math
from collections import defaultdict
import numpy as np


def overlap(a, b, *, crowd=False):
    intersection = max(0., min(a[2], b[2]) - max(a[0], b[0])) * max(
        0., min(a[3], b[3]) - max(a[1], b[1]))
    area_a = (a[2] - a[0]) * (a[3] - a[1])
    area_b = (b[2] - b[0]) * (b[3] - b[1])
    denominator = area_a if crowd else area_a + area_b - intersection
    return intersection / denominator if denominator > 0 else 0.


def _validate(rows, predictions=False, ignores=False):
    for row in rows:
        if row['label'] not in ((-1, 0, 1) if ignores else (0, 1)):
            raise ValueError('invalid label')
        box = row['box']
        if len(box) != 4 or not all(math.isfinite(v) for v in box):
            raise ValueError('box must contain four finite coordinates')
        if box[2] <= box[0] or box[3] <= box[1]:
            raise ValueError('box must have positive area')
        if predictions and (not math.isfinite(row['score']) or not 0 <= row['score'] <= 1):
            raise ValueError('invalid probability')
        hash(row['image_id'])


def _match(predictions, truth, ignores, label, iou):
    """Match once by image; score-threshold sweeps are prefixes of this ranking."""
    if label not in (0, 1) or not 0 < iou <= 1:
        raise ValueError('invalid evaluation setting')
    _validate(predictions, predictions=True)
    _validate(truth)
    _validate(ignores, ignores=True)
    ground = [row for row in truth if row['label'] == label]
    by_image, ignore_by_image = defaultdict(list), defaultdict(list)
    for index, target in enumerate(ground):
        by_image[target['image_id']].append((index, target))
    for region in ignores:
        if region['label'] in (-1, label):
            ignore_by_image[region['image_id']].append(region)
    ranked = sorted(((index, row) for index, row in enumerate(predictions)
                     if row['label'] == label), key=lambda item: (-item[1]['score'], item[0]))
    matched, scores, tp, fp, ignored = set(), [], [], [], []
    for _, prediction in ranked:
        local = by_image[prediction['image_id']]
        candidates = [(overlap(prediction['box'], target['box']), index)
                      for index, target in local if index not in matched]
        best = max(candidates, default=(0., -1), key=lambda pair: (pair[0], -pair[1]))
        scores.append(prediction['score'])
        if best[0] >= iou:
            matched.add(best[1])
            tp.append(1)
            fp.append(0)
            ignored.append(0)
        elif not any(overlap(prediction['box'], target['box']) >= iou
                     for _, target in local) and any(
                 overlap(prediction['box'], region['box'], crowd=region.get('crowd', False)) >= iou
                 for region in ignore_by_image[prediction['image_id']]):
            tp.append(0)
            fp.append(0)
            ignored.append(1)
        else:
            tp.append(0)
            fp.append(1)
            ignored.append(0)
    return np.array(scores), np.array(tp), np.array(fp), np.array(ignored), len(ground)


def _summarize(curve, threshold):
    if not 0 <= threshold <= 1:
        raise ValueError('invalid score threshold')
    scores, tp, fp, ignored, ground_count = curve
    active = (scores >= threshold) & (ignored == 0)
    tp, fp = tp[active], fp[active]
    cumulative_tp = np.cumsum(tp)
    cumulative_fp = np.cumsum(fp)
    precision = cumulative_tp / np.maximum(cumulative_tp + cumulative_fp, 1)
    recall = cumulative_tp / max(ground_count, 1)
    envelope = np.maximum.accumulate(precision[::-1])[::-1]
    ap = (float(np.mean([max(envelope[recall >= level], default=0.)
                         for level in np.linspace(0, 1, 101)])) if ground_count else None)
    total_tp, total_fp = int(tp.sum()), int(fp.sum())
    return dict(tp=total_tp, fp=total_fp, fn=ground_count - total_tp,
                ignored=int(ignored[scores >= threshold].sum()),
                precision=total_tp / max(total_tp + total_fp, 1),
                recall=total_tp / ground_count if ground_count else None, ap=ap)


def evaluate(predictions, truth, ignores=(), *, label, threshold=0., iou=.5):
    """Score-order, one-to-one greedy matching; a valid GT takes priority over ignore."""
    return _summarize(_match(predictions, truth, ignores, label, iou), threshold)


def select_thresholds(predictions, truth, ignores=()):
    """Run only on validation: maximize recall at P95, then choose higher threshold."""
    thresholds = []
    for label in (0, 1):
        candidates = []
        curve = _match(predictions, truth, ignores, label, .5)
        scores, tp, fp, ignored, ground_count = curve
        for integer in range(5, 96):
            threshold = integer / 100
            active = scores >= threshold
            count_tp, count_fp = int(tp[active].sum()), int(fp[active].sum())
            if ground_count and count_tp / max(count_tp + count_fp, 1) >= .95:
                candidates.append((count_tp / ground_count, threshold))
        thresholds.append(max(candidates)[1] if candidates else None)
    return thresholds


def report(predictions, truth, ignores=(), *, thresholds, duration_minutes=None):
    if len(thresholds) != 2 or any(value is None for value in thresholds):
        raise ValueError('both validation-frozen thresholds are required')
    if duration_minutes is not None and duration_minutes <= 0:
        raise ValueError('duration must be positive')
    classes = {}
    for label, name in enumerate(('person', 'vehicle')):
        result = evaluate(predictions, truth, ignores, label=label, threshold=thresholds[label])
        aps = [evaluate(predictions, truth, ignores, label=label, iou=integer / 100)['ap']
               for integer in range(50, 96, 5)]
        result['ap50'] = aps[0]
        result['ap50_95'] = float(np.mean(aps)) if aps[0] is not None else None
        result['false_positives_per_minute'] = (result['fp'] / duration_minutes
                                               if duration_minutes is not None else None)
        result['p95_r85_pass'] = (result['precision'] >= .95 and
                                  result['recall'] is not None and result['recall'] >= .85)
        classes[name] = result
    return dict(protocol='road_greedy_101point_ap_v1', classes=classes,
                numerical_target_pass=all(row['p95_r85_pass'] for row in classes.values()),
                formal_acceptance=False)
