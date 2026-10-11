"""CPU-only checks for the isolated epoch-7 -> epoch-12 launcher."""
import io
import json
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import patch

from . import run_road_epoch as segment
from . import run_supervised5_oct5 as run


class SupervisedFiveTest(unittest.TestCase):
    def test_real_frozen_source_and_val256_identity(self):
        import torch
        self.assertEqual(segment.sha256(run.SOURCE), run.SOURCE_SHA)
        checkpoint = torch.load(run.SOURCE, map_location="cpu", weights_only=False)
        run.validate_source(checkpoint)
        self.assertEqual(segment.sha256(run.OLD256), run.OLD256_SHA)
        baseline = json.loads(run.OLD256.read_text(encoding="utf-8"))
        run.validate_baseline(baseline, 256)

    def test_gate_is_explicit_ap50_development_heuristic(self):
        def report(person, vehicle):
            def row(value):
                return {"precision": value, "recall": value, "ap": value,
                        "ap50": value, "ap50_95": value}
            return {"diagnostic_metrics_at_0_5": {"classes": {
                "person": row(person), "vehicle": row(vehicle)}}}

        passed = run.comparison(report(.211, .19), report(.20, .20))
        self.assertTrue(passed["development_heuristic_pass"])
        self.assertEqual(passed["gate_metric"], "ap50_percentage_point_delta")
        self.assertFalse(passed["formal_statistical_significance"])
        failed = run.comparison(report(.209, .19), report(.20, .20))
        self.assertFalse(failed["development_heuristic_pass"])

    def test_wait_requires_complete_summary_line(self):
        with tempfile.TemporaryDirectory() as directory:
            log = Path(directory) / "baseline.log"
            self.assertIsNone(run.completed_baseline_summary(log))
            log.write_text('{"thresholds": [0.5], "metrics":')
            self.assertIsNone(run.completed_baseline_summary(log))
            log.write_text('progress\n' + json.dumps({
                "thresholds": [0.5], "metrics": {}, "timing_seconds": {}}) + '\n')
            self.assertIsNotNone(run.completed_baseline_summary(log))

    def test_baseline_identity_tamper_is_rejected(self):
        baseline = json.loads(run.OLD256.read_text(encoding="utf-8"))
        baseline["checkpoint_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "baseline identity"):
            run.validate_baseline(baseline, 256)

    def test_duplicate_run_lock_fails_before_reading_inputs(self):
        with tempfile.TemporaryDirectory() as directory:
            existing = Path(directory) / "existing-output"
            existing.mkdir()
            with (patch.object(run, "OUTPUT", existing),
                  patch.object(run, "RUN", Path(directory) / "unused-report"),
                  patch.object(run.sys, "argv", ["runner"])):
                with self.assertRaisesRegex(FileExistsError, "already reserved"):
                    run.main()

    def test_no_mosaic_command_resumes_full_state_without_gpu_start(self):
        saved = {name: getattr(segment, name) for name in
                 ("OUTPUT", "REPORTS", "COCO", "COCO_SHA", "PROTOCOL_SHA")}
        try:
            with tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                output, reports, report_dir = root / "output", root / "reports", root / "report"
                output.mkdir()
                (output / "last.pt").write_bytes(b"full state")
                reports.mkdir()
                proof_dir = reports / "segment_0000"
                proof_dir.mkdir()
                (proof_dir / "parity.json").write_text(json.dumps({
                    "status": "passed_GPU_AMP_segment_resume_equivalence",
                    "maximum_compared_difference": 0, "test_source_sha256": {}}))
                report_dir.mkdir()
                segment.OUTPUT, segment.REPORTS = output, reports
                launched = []

                process = SimpleNamespace(pid=123, stdin=io.StringIO(), stdout=io.StringIO(),
                                          poll=lambda: 1, wait=lambda **_: 1)

                def launch(command, **kwargs):
                    launched.append(command)
                    return process

                receipt = json.loads(segment.CACHE_RECEIPT.read_text(encoding="utf-8"))

                def digest(path):
                    if path == segment.COCO:
                        return segment.COCO_SHA
                    if path == segment.DATASET:
                        return segment.DATASET_SHA
                    if path == segment.CACHE_RECEIPT:
                        return segment.CACHE_RECEIPT_SHA
                    if path == segment.CACHE / "index.json":
                        return receipt["cache_index_sha256"]
                    return segment.EXPECTED_MODEL_SHA.get(path.name, "stable")

                with (patch.object(segment.sys, "argv", ["runner", "--no-mosaic",
                                                          "--stop-after-epoch", "12"]),
                      patch.object(segment, "next_segment", return_value=report_dir),
                      patch.object(segment, "sha256", side_effect=digest),
                      patch.object(segment.subprocess, "Popen", side_effect=launch),
                      patch.object(segment, "summarize_checkpoints", return_value={})):
                    self.assertEqual(segment.main(), 1)
                command = launched[0]
                self.assertIn("--no-mosaic", command)
                self.assertEqual(command[command.index("--resume") + 1], str(output / "last.pt"))
                self.assertNotIn("--init-checkpoint", command)

                missing_output = root / "missing-output"
                missing_output.mkdir()
                segment.OUTPUT = missing_output
                second_report = root / "missing-state-report"
                second_report.mkdir()
                launched.clear()
                with (patch.object(segment.sys, "argv", ["runner", "--no-mosaic",
                                                          "--stop-after-epoch", "12"]),
                      patch.object(segment, "next_segment", return_value=second_report),
                      patch.object(segment, "sha256", side_effect=digest),
                      patch.object(segment.subprocess, "Popen", side_effect=launch),
                      patch.object(segment, "summarize_checkpoints", return_value={})):
                    self.assertEqual(segment.main(), 1)
                self.assertEqual(launched, [])
                failure = json.loads((second_report / "report.json").read_text())
                self.assertIn("full-state last.pt", failure["error"])
        finally:
            for name, value in saved.items():
                setattr(segment, name, value)


if __name__ == "__main__":
    unittest.main()
