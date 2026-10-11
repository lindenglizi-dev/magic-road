"""CPU-only policy checks: never retry thermal/errors or changed validation data."""
import unittest
from unittest.mock import patch

from .run_road_overnight import continuation, verify_evaluation


class OvernightTest(unittest.TestCase):
    def test_only_planned_segment_pause_can_resume(self):
        report = dict(status="completed_target_epoch", recovery_checkpoint_verified=True)
        self.assertEqual(continuation(report, 0, None), "next_epoch")
        report["status"] = "paused_resumable_segment"
        self.assertEqual(continuation(report, 0, "segment_soft_limit"), "resume_same_epoch")
        self.assertEqual(continuation(report, 0, "night_deadline"), "stop_deadline")
        for reason in (None, "GPU_telemetry_stale_20s", "controller_exception", "temperature_stop"):
            with self.assertRaises(ValueError):
                continuation(report, 0, reason)
        for status, verified, code in (("hard_stopped", True, 0), ("failed", True, 0),
                                       ("completed_target_epoch", False, 0),
                                       ("completed_target_epoch", True, 1)):
            with self.assertRaises(ValueError):
                continuation(dict(status=status, recovery_checkpoint_verified=verified), code, None)

    def test_identical_eval_and_complete_checkpoint_required(self):
        baseline = {key: "same" for key in ("dataset_sha256", "image_count",
            "evaluated_image_content_sha256", "architecture_hash", "postprocess_contract",
            "truth", "ignores")}
        result = dict(baseline, checkpoint_epoch_number=5, checkpoint_optimizer_steps=1490,
                      checkpoint_sha256="hash", acceptance_eligible=False)
        with patch("cnn.run_road_overnight.sha256", return_value="hash"):
            verify_evaluation(result, baseline, 5, "local_checkpoint")
            with self.assertRaises(ValueError):
                verify_evaluation(dict(result, truth="changed"), baseline, 5, "local_checkpoint")
            with self.assertRaises(ValueError):
                verify_evaluation(dict(result, checkpoint_epoch_number=4), baseline, 5, "local_checkpoint")
            with self.assertRaises(ValueError):
                verify_evaluation(dict(result, acceptance_eligible=True), baseline, 5, "local_checkpoint")


if __name__ == "__main__":
    unittest.main()
