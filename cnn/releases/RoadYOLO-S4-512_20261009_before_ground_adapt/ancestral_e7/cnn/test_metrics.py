"""Runnable matching, crowd-ignore, and threshold-freeze regression."""
import unittest
from unittest.mock import patch
from . import metrics
from .metrics import evaluate, report, select_thresholds


class MetricsTest(unittest.TestCase):
    def test_threshold_sweep_matches_once_per_class(self):
        truth = [dict(image_id=index, label=index % 2, box=[0, 0, 10, 10])
                 for index in range(1000)]
        predictions = [{**row, 'score': 1.} for row in truth]
        with patch.object(metrics, '_match', wraps=metrics._match) as matcher:
            self.assertEqual(select_thresholds(predictions, truth), [.95, .95])
            self.assertEqual(matcher.call_count, 2)
        with patch.object(metrics, 'overlap', wraps=metrics.overlap) as comparison:
            result = evaluate(predictions, truth, label=0)
            self.assertEqual(result['tp'], 500)
            self.assertEqual(comparison.call_count, 500)

    def test_duplicate_and_cross_class(self):
        target = dict(image_id='frame', label=0, box=[0, 0, 10, 10])
        truth = [target, {**target, 'label': 1}]
        predictions = [{**target, 'score': .9}, {**target, 'score': .8},
                       {**target, 'label': 1, 'score': .9}]
        result = evaluate(predictions, truth, label=0)
        self.assertEqual((result['tp'], result['fp'], result['fn']), (1, 1, 0))
        self.assertAlmostEqual(result['ap'], 1.)
        thresholds = select_thresholds(predictions, truth)
        self.assertEqual(thresholds, [.9, .9])
        self.assertTrue(report(predictions, truth, thresholds=thresholds)['numerical_target_pass'])

    def test_crowd_and_ground_priority(self):
        target = dict(image_id=1, label=0, box=[0, 0, 2, 2])
        predictions = [{**target, 'score': 1.}]
        ignore = [{**target, 'label': -1, 'box': [0, 0, 100, 100], 'crowd': True}]
        self.assertEqual(evaluate(predictions, [], ignore, label=0)['ignored'], 1)
        self.assertEqual(evaluate(predictions, [target], ignore, label=0)['tp'], 1)
        duplicate = evaluate(predictions * 2, [target], ignore, label=0)
        self.assertEqual((duplicate['tp'], duplicate['fp'], duplicate['ignored']), (1, 1, 0))
        self.assertEqual(select_thresholds([], [target]), [None, None])
        with self.assertRaises(ValueError):
            report([], [target], thresholds=[None, .5])


if __name__ == '__main__':
    unittest.main()
