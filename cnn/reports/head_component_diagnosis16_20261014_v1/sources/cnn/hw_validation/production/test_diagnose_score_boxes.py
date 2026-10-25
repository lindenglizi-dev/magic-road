"""Narrow postprocess and GT-attribution regression checks."""
import unittest
import numpy as np
from cnn import integer, metrics
from cnn.hw_validation.production import diagnose_score_boxes as diag


class DiagnosisTests(unittest.TestCase):
    def test_vector_decode(self):
        rng = np.random.default_rng(42)
        heads = [rng.integers(-32768, 32768, (288 // s, 512 // s, 7), dtype=np.int16) for s in (4, 8, 16)]
        boxes, _ = diag.raw_grid(heads)
        offset = 0
        for head, stride in zip(heads, (4, 8, 16), strict=True):
            for y, x in ((0, 0), (head.shape[0] - 1, head.shape[1] - 1), (2, 3)):
                self.assertEqual(boxes[offset + y * head.shape[1] + x].tolist(),
                                 list(integer._decode(head[y, x], x, y, stride)))
            offset += head.shape[0] * head.shape[1]

    def test_top_ties_invalid_and_cap(self):
        heads = [np.full((288 // s, 512 // s, 7), -32768, dtype=np.int16) for s in (4, 8, 16)]
        heads[0][..., :4] = 0
        # Equal-score invalid cells must consume the entire Top128, not be replaced.
        heads[0][0, :, :2] = -32768
        heads[0][0, :, 4:] = 1000
        _, _, _, traces, detections = diag.stages(heads)
        self.assertEqual(traces[0]["top128"], list(range(128)))
        self.assertEqual(len(traces[0]["invalid_visited"]), 128)
        self.assertEqual(detections, [])
        heads[0][0, :, :4] = [0, 0, -1024, -1024]
        heads[0][0, :, 1] = 256
        _, _, _, traces, detections = diag.stages(heads)
        self.assertEqual(len(traces[0]["kept"]), 32)
        self.assertEqual(len(traces[0]["unvisited_after_cap"]), 96)
        self.assertEqual(len(detections), 64)
        self.assertFalse(integer._overlap_half([0, 0, 3, 1], [1, 0, 4, 1]))
        self.assertTrue(integer._overlap_half([0, 0, 4, 1], [1, 0, 5, 1]))

    def test_matching_ties_duplicate_ignore_floor(self):
        truth = [dict(image_id="a", label=0, box=[0, 0, 2, 2], gt_id=f"a#{i}") for i in (0, 1)]
        predictions = [dict(image_id="a", label=0, box=[0, 0, 2, 2], score=diag.FLOOR) for _ in range(3)]
        predictions.append(dict(image_id="b", label=0, box=[0, 0, 2, 2], score=diag.FLOOR))
        ignores = [dict(image_id=key, label=-1, box=[0, 0, 2, 2], crowd=True) for key in ("a", "b")]
        records, curve = diag.match_trace(predictions, truth, ignores, 0)
        self.assertEqual([r["gt_id"] for r in records], ["a#0", "a#1", None, None])
        self.assertEqual([r["fp"] for r in records], [0, 0, 1, 0])
        self.assertEqual([r["ignored"] for r in records], [0, 0, 0, 1])
        self.assertEqual(len(curve), 3)
        self.assertEqual(metrics.evaluate(predictions, truth, ignores, label=0, threshold=diag.FLOOR)["tp"], 2)
        self.assertEqual(metrics.evaluate(predictions, truth, ignores, label=0, threshold=.05)["tp"], 0)
        empty, curve = diag.match_trace([], [], [], 1)
        self.assertEqual((empty, curve), ([], []))


if __name__ == "__main__":
    unittest.main()
