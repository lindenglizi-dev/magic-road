"""CPU-only checks for the post-review protected launcher."""

import io
import json
import os
from pathlib import Path
from types import SimpleNamespace
import tempfile
import time
import unittest
from unittest.mock import patch

from . import run_post_review_s as launcher


class Capture(io.StringIO):
    def close(self):
        pass


def options(root: Path, **changes):
    values = dict(
        dataset=root / "dataset.json", dataset_sha256="1" * 64,
        cache=root / "cache", cache_index_sha256="2" * 64,
        output=root / "run", init_checkpoint=root / "e7.pt",
        init_checkpoint_sha256=launcher.EXPECTED_INIT_SHA256,
        experiment_contract=root / "contract.json", experiment_contract_sha256="3" * 64,
        preflight=root / "preflight.json", preflight_sha256="4" * 64,
        ground_manifest=root / "ground_val48.json", ground_manifest_sha256="5" * 64,
        ground_receipt=root / "ground_receipt.json", ground_receipt_sha256="6" * 64,
        decision_proof=None, decision_proof_sha256=None, continue_to_5=False,
        gpu_uuid="GPU-owned", receipt=root / "receipt.json", execute=False,
        validate_only=False, dry_run=True, preflight_timeout_seconds=3600.0)
    values.update(changes)
    return SimpleNamespace(**values)


class LauncherTest(unittest.TestCase):
    def test_fixed_command_and_init_resume_selection(self):
        with tempfile.TemporaryDirectory(dir=launcher.ROOT) as temporary:
            root = Path(temporary)
            args = options(root)
            command, mode, stop = launcher.build_train_command(args)
            self.assertEqual((mode, stop), ("init_E7_weights_only", 2))
            self.assertIn("--init-checkpoint", command)
            self.assertNotIn("--resume", command)
            for pair in (("--epochs", "5"), ("--stop-after-epoch", "2"),
                         ("--lr", "0.001"), ("--lr-schedule", "finetune_constant"),
                         ("--batch-size", "8"), ("--accum-steps", "8"),
                         ("--workers", "0"), ("--checkpoint-every-seconds", "120")):
                self.assertEqual(command[command.index(pair[0]) + 1], pair[1])
            self.assertIn("--amp", command)
            self.assertIn("--no-mosaic", command)

            args.output.mkdir()
            (args.output / "last_resume.pt").write_bytes(b"cursor")
            command, mode, stop = launcher.build_train_command(args)
            self.assertEqual((mode, stop), ("resume_paused_same_run", 2))
            self.assertEqual(Path(command[command.index("--resume") + 1]).name,
                             "last_resume.pt")
            (args.output / "last.pt").write_bytes(b"S2")
            args.continue_to_5 = True
            command, mode, stop = launcher.build_train_command(args)
            self.assertEqual((mode, stop), ("resume_S2_same_run", 5))
            self.assertEqual(Path(command[command.index("--resume") + 1]).name, "last.pt")

    def test_pending_ground_blocks_execute_not_CPU_validation(self):
        with tempfile.TemporaryDirectory(dir=launcher.ROOT) as temporary:
            root = Path(temporary)
            args = options(root)
            for path in (args.dataset, args.cache / "index.json", args.init_checkpoint,
                         args.experiment_contract, args.preflight, args.ground_receipt):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("{}", encoding="utf-8")
            documents = {
                args.dataset: {},
                args.experiment_contract: {
                    "status": "prepared_pending_ground48", "protocol": launcher.PROTOCOL,
                    "training_authorized": True, "epochs": 5, "initial_stop_after_epoch": 2,
                    "dataset_sha256": args.dataset_sha256,
                    "cache_index_sha256": args.cache_index_sha256,
                    "init_checkpoint_sha256": args.init_checkpoint_sha256,
                    "output": str(args.output.resolve()),
                    "train_images": launcher.EXPECTED_TRAIN,
                    "val_images": launcher.EXPECTED_VAL},
                args.preflight: {
                    "status": "cpu_prepared_ground_pending", "gpu_execution_ready": False,
                    "dataset_sha256": args.dataset_sha256,
                    "cache_index_sha256": args.cache_index_sha256,
                    "init_checkpoint_sha256": args.init_checkpoint_sha256,
                    "train_images": launcher.EXPECTED_TRAIN,
                    "val_images": launcher.EXPECTED_VAL},
                args.ground_receipt: {"status": "pending_human_review", "image_count": 48,
                                      "human_complete_count": 0, "pending_count": 48,
                                      "ground_val48_generated": False},
            }
            digests = {args.dataset: args.dataset_sha256,
                       args.cache / "index.json": args.cache_index_sha256,
                       args.init_checkpoint: args.init_checkpoint_sha256,
                       args.experiment_contract: args.experiment_contract_sha256,
                       args.preflight: args.preflight_sha256,
                       args.ground_receipt: args.ground_receipt_sha256}
            with (patch.object(launcher, "sha256", side_effect=lambda path: digests[path]),
                  patch.object(launcher, "load_json", side_effect=lambda path: documents[path])):
                gates, _ = launcher.inspect(args)
            self.assertFalse([gate for gate in gates if "validate_only" in gate["blocks"]])
            names = {gate["gate"] for gate in gates}
            self.assertIn("preflight_not_GPU_ready", names)
            self.assertIn("ground_manifest_missing", names)
            self.assertIn("ground_human_review_incomplete", names)

    def test_S5_requires_bound_positive_decision(self):
        with tempfile.TemporaryDirectory(dir=launcher.ROOT) as temporary:
            args = options(Path(temporary), continue_to_5=True)
            with patch.object(launcher, "pinned_json", return_value=None):
                gates, _ = launcher.inspect(args)
            self.assertIn("S2_to_S5_decision_missing", {gate["gate"] for gate in gates})

    def test_forged_ready_with_one_unsigned_row_is_execute_blocked(self):
        from . import prepare_ground48 as ground_tool
        with tempfile.TemporaryDirectory(dir=launcher.ROOT) as temporary:
            root = Path(temporary)
            args = options(root, ground_manifest=root / "ground_val48.json")
            review_path = root / "review_manifest_teacher.json"
            verified_path = root / "ground48_verified_labels.json"
            signed_path = root / "review_patch_signed.json"
            review_path.write_text("{}", encoding="utf-8")
            signed_path.write_text('{"signed":true}', encoding="utf-8")
            canonical_verified = {"images": [{"manual_review": {"raw_seen": True}}]}
            canonical_ground = {"images": [{"boxes": [[1, 2, 3, 4]], "ignore_boxes": []}]}
            rebuilt_receipt = {"schema": "cnn_ground48_export_receipt_v1",
                               "status": "validated_ready", "dataset_id": "bound-dataset",
                               "image_count": 48, "complete_count": 48, "pending_count": 0,
                               "all_raw_seen": True, "all_checks_complete": True,
                               "patch_sha256": launcher.sha256(signed_path)}
            variants = (
                ({"images": [{"manual_review": {"raw_seen": False}}]}, canonical_ground,
                 "unsigned row"),
                (canonical_verified,
                 {"images": [{"boxes": [[1, 2, 4, 4]], "ignore_boxes": []}]},
                 "changed box"),
            )
            for actual_verified, actual_ground, label in variants:
                with self.subTest(label=label):
                    args.ground_manifest.write_text(json.dumps(actual_ground), encoding="utf-8")
                    verified_path.write_text(json.dumps(actual_verified), encoding="utf-8")
                    receipt = {**rebuilt_receipt,
                               "ground_val48_sha256": launcher.sha256(args.ground_manifest),
                               "ground48_verified_labels_json_sha256": launcher.sha256(verified_path),
                               "review_patch_signed_json_sha256": launcher.sha256(signed_path)}
                    gates, identities = [], {}
                    with patch.object(ground_tool, "export_documents", return_value=(
                            canonical_verified, canonical_ground, rebuilt_receipt)):
                        launcher.validate_ground_evidence(args, receipt, gates, identities)
                    self.assertEqual([gate["gate"] for gate in gates],
                                     ["ground_evidence_closure"])
                    self.assertEqual(gates[0]["blocks"], ["execute"])

    def test_ground_export_retains_exact_signed_patch(self):
        from . import prepare_ground48 as ground_tool
        with tempfile.TemporaryDirectory(dir=launcher.ROOT) as temporary:
            root = Path(temporary)
            (root / "review_manifest_teacher.json").write_text("{}", encoding="utf-8")
            patch_path = root / "outside_signed_patch.json"
            patch_bytes = b'{\n  "signed": true\n}\n'
            patch_path.write_bytes(patch_bytes)
            receipt = {"patch_sha256": launcher.sha256(patch_path)}
            with patch.object(ground_tool, "export_documents",
                              return_value=({"verified": True}, {"ground": True}, receipt)):
                result = ground_tool.export_patch(root, patch_path)
            self.assertEqual((root / "review_patch_signed.json").read_bytes(), patch_bytes)
            self.assertEqual(result["review_patch_signed_json_sha256"],
                             launcher.sha256(root / "review_patch_signed.json"))
            with (patch.object(ground_tool, "export_documents",
                               return_value=({"verified": True}, {"ground": True}, receipt)),
                  self.assertRaises(FileExistsError)):
                ground_tool.export_patch(root, patch_path)

    def test_watchdog_attachment_failure_stops_only_owned_child(self):
        class Process:
            def __init__(self, pid, stdout, returncode=0):
                self.pid, self.stdout, self.stdin = pid, io.StringIO(stdout), Capture()
                self.returncode, self.killed, self.terminated = returncode, False, False
            def poll(self):
                return None
            def wait(self, **_kwargs):
                return self.returncode
            def kill(self):
                self.killed = True
            def terminate(self):
                self.terminated = True

        with tempfile.TemporaryDirectory(dir=launcher.ROOT) as temporary:
            args = options(Path(temporary))
            worker = Process(123, '{"event":"preflight_ready","trainer_pid":123}\n')
            monitor = Process(124, '{"event":"watchdog_failed"}\n', 1)
            calls = []
            def launch(command, **_kwargs):
                calls.append(command)
                return worker if len(calls) == 1 else monitor
            with patch.object(launcher.subprocess, "Popen", side_effect=launch):
                result = launcher.run_protected(["python", "-m", "cnn.train"], args)
            self.assertEqual(result["status"], "failed_no_retry")
            self.assertEqual(calls[1][calls[1].index("--watchdog") + 1], "123")
            self.assertNotIn("GO\n", worker.stdin.getvalue())
            self.assertFalse(monitor.terminated)

    def test_GO_only_after_owned_watchdog_ready(self):
        class Process:
            def __init__(self, pid, stdout):
                self.pid, self.stdout, self.stdin = pid, io.StringIO(stdout), Capture()
                self.returncode = 0
            def poll(self):
                return 0
            def wait(self, **_kwargs):
                return 0
            def terminate(self):
                raise AssertionError("completed monitor must not be terminated")

        with tempfile.TemporaryDirectory(dir=launcher.ROOT) as temporary:
            args = options(Path(temporary))
            args.output.mkdir()
            checkpoint = args.output / "last_resume.pt"
            checkpoint.write_bytes(b"committed")
            worker = Process(321, ('{"event":"preflight_ready","trainer_pid":321}\n'
                                   + json.dumps({"event": "paused_segment",
                                       "checkpoint": str(checkpoint), "stage": "train",
                                       "next_microbatch": 8, "next_sample_cursor": 64,
                                       "val_next_batch": 0}) + "\n"))
            monitor = Process(322, json.dumps({
                "event": "watchdog_ready", "trainer_pid": 321,
                "owner_pid": os.getpid(), "initial": {"uuid": "GPU-owned"}}) + "\n")
            with patch.object(launcher.subprocess, "Popen", side_effect=[worker, monitor]):
                result = launcher.run_protected(
                    ["python", "-m", "cnn.train", "--stop-after-epoch", "2"], args)
            self.assertEqual(worker.stdin.getvalue(), "GO\n")
            self.assertEqual(result["status"], "paused_or_completed_verified_by_event")

    def test_duplicate_preflight_does_not_send_second_GO(self):
        class Process:
            def __init__(self, pid, stdout):
                self.pid, self.stdout, self.stdin = pid, io.StringIO(stdout), Capture()
                self.returncode = 0
            def poll(self):
                return None
            def wait(self, **_kwargs):
                return 0
            def terminate(self):
                pass

        with tempfile.TemporaryDirectory(dir=launcher.ROOT) as temporary:
            args = options(Path(temporary))
            worker = Process(401, ('{"event":"preflight_ready","trainer_pid":401}\n'
                                   '{"event":"preflight_ready","trainer_pid":401}\n'))
            monitor = Process(402, json.dumps({
                "event": "watchdog_ready", "trainer_pid": 401,
                "owner_pid": os.getpid(), "initial": {"uuid": "GPU-owned"}}) + "\n")
            calls = []
            def launch(command, **_kwargs):
                calls.append(command)
                return worker if len(calls) == 1 else monitor
            with patch.object(launcher.subprocess, "Popen", side_effect=launch):
                result = launcher.run_protected(
                    ["python", "-m", "cnn.train", "--stop-after-epoch", "2"], args)
            self.assertEqual(result["status"], "failed_no_retry")
            self.assertEqual(worker.stdin.getvalue(), "GO\n")
            self.assertEqual(len(calls), 2)

    def test_preflight_wait_is_bounded(self):
        class SlowEmpty:
            def __iter__(self):
                return self
            def __next__(self):
                time.sleep(0.1)
                raise StopIteration
            def close(self):
                pass
        class Process:
            pid, returncode = 501, 0
            stdin, stdout = Capture(), SlowEmpty()
            def poll(self):
                return None
            def wait(self, **_kwargs):
                return 0
            def kill(self):
                pass

        with tempfile.TemporaryDirectory(dir=launcher.ROOT) as temporary:
            args = options(Path(temporary), preflight_timeout_seconds=0.01)
            with patch.object(launcher.subprocess, "Popen", return_value=Process()):
                started = time.monotonic()
                result = launcher.run_protected(["python", "-m", "cnn.train"], args)
            self.assertLess(time.monotonic() - started, 1)
            self.assertEqual(result["status"], "failed_no_retry")
            self.assertIn("did not produce a ready event", result["error"])

    def test_committed_cursor_must_match_update_boundary(self):
        with tempfile.TemporaryDirectory(dir=launcher.ROOT) as temporary:
            output = Path(temporary) / "run"
            event = {"event": "paused_segment", "checkpoint": str(output / "last_resume.pt"),
                     "stage": "train", "next_microbatch": 8,
                     "next_sample_cursor": 64, "val_next_batch": 0}
            launcher.validate_committed_event(event, output, 2)
            event["next_sample_cursor"] = 63
            with self.assertRaisesRegex(ValueError, "cursors disagree"):
                launcher.validate_committed_event(event, output, 2)


if __name__ == "__main__":
    unittest.main()
