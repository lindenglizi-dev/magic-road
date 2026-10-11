"""CPU-only checks for owned segmented launcher and lossless event draining."""
import io
import json
from pathlib import Path
import queue
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from . import run_road_epoch as runner


class LaunchTest(unittest.TestCase):
    def test_isolated_person_arms(self):
        names = ('COCO', 'COCO_SHA', 'OUTPUT', 'REPORTS', 'PROTOCOL_SHA')
        saved = {name: getattr(runner, name) for name in names}
        try:
            for arm in ('native', 'mosaic'):
                runner.configure_person_ab(arm)
                self.assertEqual(runner.COCO, runner.ROAD_OUTPUT / 'epoch_0019.pt')
                self.assertEqual(runner.COCO_SHA, runner.ROAD20_SHA)
                self.assertNotEqual(runner.OUTPUT, runner.ROAD_OUTPUT)
                self.assertEqual(runner.OUTPUT.name, 'person_ab_20261004_' + arm)
                self.assertEqual(runner.REPORTS.parent.name, 'person_ab_20261004')
                if arm == 'mosaic':
                    self.assertEqual(runner.PROTOCOL_SHA, runner.ROAD_PROTOCOL_SHA)
                else:
                    self.assertNotEqual(runner.PROTOCOL_SHA, runner.ROAD_PROTOCOL_SHA)
            with self.assertRaises(ValueError):
                runner.configure_person_ab('../original')
            with patch.object(runner.sys, 'argv', ['runner', '--person-ab-arm', 'native',
                                                   '--stop-after-epoch', '3']):
                with self.assertRaises(SystemExit):
                    runner.main()
        finally:
            for name, value in saved.items():
                setattr(runner, name, value)

    def test_ready_handshake(self):
        process = SimpleNamespace(stdout=io.StringIO(
            '{"event":"watchdog_ready","started_monotonic":123.5}\n'))
        self.assertEqual(runner.read_ready(process)["started_monotonic"], 123.5)
        self.assertEqual(runner.HARD_SECONDS, 30 * 60)
        self.assertEqual(runner.SOFT_SECONDS, 26 * 60)
        with self.assertRaisesRegex(RuntimeError, "permission denied"):
            runner.read_ready(SimpleNamespace(stdout=io.StringIO('{"event":"failed"}\n')))
        with self.assertRaises(ValueError):
            runner.read_ready(SimpleNamespace(stdout=io.StringIO('')))

    def test_event_drain_and_owned_paths(self):
        self.assertEqual(runner.OUTPUT.name, "road40_from_coco6_segmented_20261003")
        self.assertEqual(runner.CACHE.name, "cache_road_recovery_20261003")
        events = queue.Queue()
        process = SimpleNamespace(stdout=io.StringIO(
            'multiline startup\n{"event":"step","trained_steps":10}\n'
            '{"event":"paused_segment","trained_steps":10}\n'))
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "stdout.log"
            runner.stream_events(process, path, events)
            self.assertEqual(events.get()["event"], "step")
            self.assertEqual(events.get()["event"], "paused_segment")
            self.assertEqual(events.get()["event"], "worker_stdout_closed")
            self.assertTrue(events.empty())
            self.assertIn("paused_segment", path.read_text())
            runner.stream_events(process, path, events)
            self.assertEqual(events.get()["event"], "stdout_reader_failed")
            self.assertEqual(events.get()["event"], "worker_stdout_closed")

    def test_frozen_network_sources(self):
        for name, expected in runner.EXPECTED_MODEL_SHA.items():
            self.assertEqual(runner.sha256(runner.ROOT / "cnn" / name), expected)

    def test_checkpoint_required_for_success(self):
        event = dict(event="paused_segment", checkpoint=str(runner.OUTPUT / "last_resume.pt"),
                     trained_steps=10, stage="train", epoch_index=0, next_microbatch=80,
                     next_sample_cursor=640, val_next_batch=0)
        result = dict(status="paused_resumable_segment", watchdog_pid=123,
                      last_event=event, checkpoints={})
        with self.assertRaisesRegex(ValueError, "matching valid checkpoint"):
            runner.validate_segment_result(result)
        receipt = {key: value for key, value in event.items() if key not in ("event", "checkpoint")}
        result["checkpoints"]["last_resume.pt"] = dict(receipt, valid=True)
        runner.validate_segment_result(result)
        self.assertTrue(result["recovery_checkpoint_verified"])
        receipt["next_microbatch"] = 72
        result["checkpoints"]["last_resume.pt"] = dict(receipt, valid=True)
        with self.assertRaisesRegex(ValueError, "cursor differs"):
            runner.validate_segment_result(result)

    def test_target_epoch_requires_matching_full_checkpoint(self):
        result = dict(status="completed_target_epoch", stop_after_epoch=2, watchdog_pid=123,
                      last_event=dict(event="paused_complete_epoch", epoch_number=2,
                                      trained_steps=596, checkpoint=str(runner.OUTPUT / "last.pt")),
                      checkpoints={"last.pt": dict(valid=True, epoch=1, trained_steps=596)})
        runner.validate_segment_result(result)
        self.assertTrue(result["recovery_checkpoint_verified"])
        result["checkpoints"]["last.pt"]["epoch"] = 0
        with self.assertRaisesRegex(ValueError, "target full road epoch"):
            runner.validate_segment_result(result)
        result["checkpoints"]["last.pt"]["epoch"] = 1
        result["last_event"]["epoch_number"] = 1
        with self.assertRaisesRegex(ValueError, "target full road epoch"):
            runner.validate_segment_result(result)
        result["last_event"]["epoch_number"] = 2
        result["stop_after_epoch"] = 1
        with self.assertRaisesRegex(ValueError, "target full road epoch"):
            runner.validate_segment_result(result)

    def test_report_survives_worker_and_initial_watchdog_failure(self):
        for initial_monitor_failure in (False, True):
            with tempfile.TemporaryDirectory() as temporary:
                segment = Path(temporary)
                worker = SimpleNamespace(pid=123, returncode=1, stdin=io.StringIO(),
                                         stdout=io.StringIO('{"event":"preflight_ready","trainer_pid":123}\n'
                                             if initial_monitor_failure else ''),
                                         poll=lambda: 1, wait=lambda **kw: 1)
                monitor = SimpleNamespace(pid=124, stdout=io.StringIO('{"event":"watchdog_failed"}\n'),
                                          poll=lambda: 1, wait=lambda **kw: 1)

                def launch(*args, **kwargs):
                    if "--watchdog" in args[0]:
                        (segment / "watchdog_failure.json").write_text(
                            '{"status":"hard_stopped","reason":"injected_initial_failure"}')
                        return monitor
                    return worker

                def digest(path):
                    if path == runner.COCO:
                        return runner.COCO_SHA
                    if path == runner.DATASET:
                        return runner.DATASET_SHA
                    if path == runner.CACHE_RECEIPT:
                        return runner.CACHE_RECEIPT_SHA
                    if path == runner.CACHE / "index.json":
                        return "74ef3e7bac0a6a5b134931898e57f115428b3a7751a5581f870048101dc0fa83"
                    if path.name in ("train.py", "resume_state.py", "test_segment_resume.py"):
                        return json.loads(max(runner.REPORTS.glob("segment_*/parity.json")).read_text())[
                            "test_source_sha256"][path.name]
                    return runner.EXPECTED_MODEL_SHA.get(path.name, "stable")

                with (patch.object(runner.sys, "argv", ["runner"]),
                      patch.object(runner, "next_segment", return_value=segment),
                      patch.object(runner, "sha256", side_effect=digest),
                      patch.object(runner.subprocess, "Popen", side_effect=launch),
                      patch.object(runner, "summarize_checkpoints", return_value={})): 
                    self.assertEqual(runner.main(), 1)
                report = json.loads((segment / "report.json").read_text())
                self.assertEqual(report["status"], "hard_stopped" if initial_monitor_failure else "failed")
                if initial_monitor_failure:
                    self.assertEqual(report["failure"]["reason"], "injected_initial_failure")


if __name__ == "__main__":
    unittest.main()
