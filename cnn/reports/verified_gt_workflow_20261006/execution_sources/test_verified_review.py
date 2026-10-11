"""CPU-only contract tests for import_verified_review.py."""

from __future__ import annotations

import copy
import hashlib
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

try:
    from .import_verified_review import ReviewError, import_review, json_hash, main, sha256_file
except ImportError:
    from import_verified_review import ReviewError, import_review, json_hash, main, sha256_file


CHECKS = {
    "person": True,
    "vehicle": True,
    "rider": True,
    "parked_vehicle": True,
    "small_occluded": True,
    "ignore": True,
}


class VerifiedReviewTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.policy = self.root / "annotation_policy_v1.md"
        self.policy.write_text("fixed manual annotation policy\n", encoding="utf-8")
        policy_hash = sha256_file(self.policy)
        samples = []
        reviews = []
        for index in range(128):
            image_id = f"train_{index:03d}"
            raw = self.root / "images" / image_id / "raw.jpg"
            raw.parent.mkdir(parents=True)
            raw.write_bytes(f"raw-image-{index}".encode())
            original = [{
                "target_id": f"o{index}",
                "class": "person",
                "bbox": [1, 2, 10, 20],
                "source_category": 1,
                "source_target_id": index,
            }]
            samples.append({
                "image_id": image_id,
                "legacy_id": f"legacy-{index}",
                "bucket": "train_review",
                "split": "train",
                "width": 32,
                "height": 24,
                "raw_file": f"images/{image_id}/raw.jpg",
                "source_sha256": sha256_file(raw),
                "original": original,
                "teacher_candidates": [{"target_id": "teacher_fake", "class": "vehicle",
                                          "bbox": [2, 2, 12, 12]}],
                "warnings": [],
                "review_score": 0,
                "source_scene_id": f"scene-{index // 8}",
                "camera_id": "camera-fixture",
                "frame_index": index,
                "source_metadata": {"fixture": True, "source_index": index},
            })
            reviews.append({
                "image_id": image_id,
                "source_sha256": sha256_file(raw),
                "reviewer": "human-reviewer",
                "raw_seen": True,
                "complete": True,
                "checks": dict(CHECKS),
                "actions": [{
                    "target_id": f"o{index}",
                    "action": "A",
                    "class": "person",
                    "bbox": [1, 2, 10, 20],
                    "reason": "",
                    "ai_assisted": False,
                }],
                "notes": "",
            })
        self.manifest = {
            "schema": "cnn_review_workbench_v1",
            "dataset_id": "",
            "annotation_policy_sha256": policy_hash,
            "train_required_count": 128,
            "samples": samples,
        }
        self._rehash_dataset()
        self.patch = {
            "schema": "cnn_review_patch_v1",
            "dataset_id": self.manifest["dataset_id"],
            "annotation_policy_sha256": policy_hash,
            "reviews": reviews,
        }
        self.manifest_path = self.root / "review_manifest.json"
        self.patch_path = self.root / "annotation_patch.json"
        self.output = self.root / "verified"
        self._write_inputs()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _rehash_dataset(self) -> None:
        self.manifest["dataset_id"] = json_hash({
            "annotation_policy_sha256": self.manifest["annotation_policy_sha256"],
            "samples": [{key: sample[key] for key in
                         ("image_id", "source_sha256", "width", "height",
                          "bucket", "split", "original")}
                        for sample in self.manifest["samples"]],
        })

    def _write_inputs(self) -> None:
        self.manifest_path.write_text(json.dumps(self.manifest, indent=2), encoding="utf-8")
        self.patch_path.write_text(json.dumps(self.patch, indent=2), encoding="utf-8")

    def _write_snapshot(self) -> None:
        original = self.root / "manifest_original.json"
        original.write_bytes(self.manifest_path.read_bytes())
        (self.root / "snapshot_receipt.json").write_text(json.dumps({
            "dataset_id": self.manifest["dataset_id"],
            "original_manifest_sha256": sha256_file(original),
        }), encoding="utf-8")

    def _rejects(self, pattern: str, *, validate_only: bool = True) -> None:
        self._write_inputs()
        with self.assertRaisesRegex(ReviewError, pattern):
            import_review(self.manifest_path, self.patch_path, self.output,
                          validate_only=validate_only)
        self.assertFalse(self.output.exists())

    def test_positive_human_signed_export_is_frozen_and_scoped(self) -> None:
        self.patch["reviews"][1]["actions"][0].update(
            action="M", bbox=[2, 3, 11, 21], reason="manual box correction")
        self.patch["reviews"][2]["actions"][0].update(
            action="D", reason="manual duplicate removal")
        self.patch["reviews"][3]["actions"].append({
            "target_id": "new-person",
            "action": "N",
            "class": "person",
            "bbox": [20, 5, 30, 22],
            "reason": "teacher prompted, human confirmed on RAW",
            "ai_assisted": True,
        })
        self.patch["reviews"][4]["actions"][0].update(
            action="I", **{"class": "ignore"}, reason="too occluded", ai_assisted=True)
        self._write_inputs()
        self._write_snapshot()
        manifest_before = self.manifest_path.read_bytes()
        receipt = import_review(self.manifest_path, self.patch_path, self.output)

        self.assertEqual(self.manifest_path.read_bytes(), manifest_before)
        self.assertFalse(receipt["training_started"])
        self.assertFalse(receipt["formal_acceptance"])
        self.assertEqual(receipt["stats"]["original"], 128)
        self.assertEqual(receipt["stats"]["added"], 1)
        self.assertEqual(receipt["stats"]["modified"], 1)
        self.assertEqual(receipt["stats"]["deleted"], 1)
        self.assertEqual(receipt["stats"]["ignored"], 1)
        self.assertEqual(receipt["stats"]["ai_suggestions_checked"], 2)
        self.assertEqual(receipt["stats"]["ai_suggestions_accepted"], 1)
        labels_path = self.output / "labels_verified.json"
        labels = json.loads(labels_path.read_text(encoding="utf-8"))
        self.assertEqual(labels["scope"], {"bucket": "train_review", "split": "train",
                                            "image_count": 128})
        self.assertEqual(len(labels["images"]), 128)
        self.assertTrue(Path(labels["images"][0]["raw_file_absolute"]).is_absolute())
        self.assertEqual(labels["images"][0]["source_scene_id"], "scene-0")
        self.assertEqual(labels["images"][0]["source_metadata"]["source_index"], 0)
        self.assertEqual(labels["images"][3]["labels"][1]["source"], "manual_review")
        self.assertTrue(labels["images"][3]["labels"][1]["ai_assisted"])
        self.assertEqual((self.output / "manifest_original.json").read_bytes(), manifest_before)
        self.assertEqual((self.output / "review_patch.json").read_bytes(),
                         self.patch_path.read_bytes())
        self.assertEqual(receipt["outputs"]["labels_verified_sha256"], sha256_file(labels_path))

    def test_formal_export_requires_frozen_snapshot_receipt(self) -> None:
        with self.assertRaisesRegex(ReviewError, "requires snapshot_receipt"):
            import_review(self.manifest_path, self.patch_path, self.output)

    def test_snapshot_receipt_binds_source_trace_fields(self) -> None:
        self._write_snapshot()
        self.manifest["samples"][0]["source_metadata"]["source_index"] = 999
        self._write_inputs()
        with self.assertRaisesRegex(ReviewError, "source fields changed"):
            import_review(self.manifest_path, self.patch_path, self.output, validate_only=True)

    def test_snapshot_receipt_rejects_original_manifest_hash_change(self) -> None:
        self._write_snapshot()
        (self.root / "manifest_original.json").write_text("{}", encoding="utf-8")
        with self.assertRaisesRegex(ReviewError, "original manifest SHA-256 mismatch"):
            import_review(self.manifest_path, self.patch_path, self.output, validate_only=True)

    def test_validate_only_allows_unreviewed_and_writes_nothing(self) -> None:
        self.patch["reviews"].pop()
        self._write_inputs()
        status = import_review(self.manifest_path, self.patch_path, self.output,
                               validate_only=True)
        self.assertEqual(status["status"], "validated_pending")
        self.assertEqual(status["pending_train_count"], 1)
        self.assertFalse(status["verified_generated"])
        self.assertFalse(self.output.exists())
        self._write_snapshot()
        with self.assertRaisesRegex(ReviewError, "train reviews are pending"):
            import_review(self.manifest_path, self.patch_path, self.output)

    def test_partial_review_is_pending_not_verified(self) -> None:
        review = self.patch["reviews"][0]
        review.update(complete=False, raw_seen=False, reviewer="")
        review["checks"]["rider"] = False
        review["actions"] = []
        self._write_inputs()
        status = import_review(self.manifest_path, self.patch_path, self.output,
                               validate_only=True)
        self.assertEqual(status["pending_train_count"], 1)
        self._write_snapshot()
        with self.assertRaisesRegex(ReviewError, "train reviews are pending"):
            import_review(self.manifest_path, self.patch_path, self.output)

    def test_complete_review_rejects_raw_false(self) -> None:
        self.patch["reviews"][0]["raw_seen"] = False
        self._rejects("raw_seen=true")

    def test_complete_review_rejects_missing_original_decision(self) -> None:
        self.patch["reviews"][0]["actions"] = []
        self._rejects("every original target")

    def test_accept_cannot_change_source(self) -> None:
        self.patch["reviews"][0]["actions"][0]["bbox"] = [2, 2, 10, 20]
        self._rejects("A must preserve")

    def test_teacher_candidate_cannot_be_accepted_as_original(self) -> None:
        self.patch["reviews"][0]["actions"].append({
            "target_id": "teacher_fake", "action": "A", "class": "vehicle",
            "bbox": [2, 2, 12, 12], "reason": "", "ai_assisted": True,
        })
        self._rejects("A requires an original")

    def test_unknown_target_cannot_modify_source(self) -> None:
        self.patch["reviews"][0]["actions"][0].update(
            target_id="not-source", action="M", reason="attempt")
        self._rejects("M requires an original")

    def test_modify_and_new_cannot_create_ignore(self) -> None:
        for kind in ("M", "N"):
            with self.subTest(action=kind):
                action = self.patch["reviews"][0]["actions"][0]
                saved = copy.deepcopy(action)
                action.update(action=kind, **{"class": "ignore"}, reason="wrong UI action")
                if kind == "N":
                    action["target_id"] = "new-ignore"
                self._rejects("cannot create ignore")
                self.patch["reviews"][0]["actions"][0] = saved

    def test_rejects_bad_and_nan_coordinates(self) -> None:
        for bbox, pattern in (([0, 0, 33, 2], "invalid native"),
                              ([0, 0, float("nan"), 2], "finite")):
            with self.subTest(bbox=bbox):
                action = self.patch["reviews"][0]["actions"][0]
                saved = copy.deepcopy(action)
                action.update(action="M", bbox=bbox, reason="manual correction")
                self._rejects(pattern)
                self.patch["reviews"][0]["actions"][0] = saved

    def test_rejects_source_hash_mismatch(self) -> None:
        raw = self.root / self.manifest["samples"][0]["raw_file"]
        raw.write_bytes(b"changed after freeze")
        self._rejects("raw file SHA-256 mismatch")

    def test_rejects_duplicate_image_ids(self) -> None:
        duplicate = copy.deepcopy(self.manifest["samples"][0])
        self.manifest["samples"].append(duplicate)
        self._rehash_dataset()
        self.patch["dataset_id"] = self.manifest["dataset_id"]
        self._rejects("duplicate image_id")

    def test_rejects_duplicate_action_target_ids(self) -> None:
        self.patch["reviews"][0]["actions"].append(
            copy.deepcopy(self.patch["reviews"][0]["actions"][0]))
        self._rejects("duplicate action target_id")

    def test_rejects_path_escape_without_opening_it(self) -> None:
        self.manifest["samples"][0]["raw_file"] = "../blind/raw.jpg"
        self._rejects("blind/reserve raw path")

    def test_rejects_policy_hash_mismatch(self) -> None:
        self.policy.write_text("changed policy\n", encoding="utf-8")
        self._rejects("policy SHA-256 mismatch")

    def test_rejects_cross_split_even_with_recomputed_dataset_id(self) -> None:
        self.manifest["samples"][0]["split"] = "dev"
        self._rehash_dataset()
        self.patch["dataset_id"] = self.manifest["dataset_id"]
        self._rejects("bucket/split crossing")

    def test_dataset_id_binds_original_and_order(self) -> None:
        self.manifest["samples"][0]["original"][0]["class"] = "vehicle"
        self._rejects("dataset_id does not bind")

    def test_rejects_unknown_class_action_and_sample(self) -> None:
        cases = (("class", "animal", "unknown class"),
                 ("action", "X", "unknown action"))
        for key, value, pattern in cases:
            with self.subTest(field=key):
                saved = self.patch["reviews"][0]["actions"][0][key]
                self.patch["reviews"][0]["actions"][0][key] = value
                self._rejects(pattern)
                self.patch["reviews"][0]["actions"][0][key] = saved
        self.patch["reviews"][0]["image_id"] = "unknown-sample"
        self._rejects("unknown sample")

    def test_rejects_patch_policy_and_dataset_mismatch(self) -> None:
        self.patch["annotation_policy_sha256"] = "0" * 64
        self._rejects("annotation_policy_sha256")
        self.patch["annotation_policy_sha256"] = self.manifest["annotation_policy_sha256"]
        self.patch["dataset_id"] = "0" * 64
        self._rejects("dataset_id")

    def test_rejects_overwrite(self) -> None:
        self.output.mkdir()
        with self.assertRaisesRegex(ReviewError, "output already exists"):
            import_review(self.manifest_path, self.patch_path, self.output, validate_only=True)

    def test_cli_validate_only_contract(self) -> None:
        self.patch["reviews"].pop()
        self._write_inputs()
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            result = main(["--manifest", str(self.manifest_path),
                           "--patch", str(self.patch_path),
                           "--output", str(self.output), "--validate-only"])
        self.assertEqual(result, 0)
        self.assertEqual(json.loads(stdout.getvalue())["status"], "validated_pending")

    def test_real_frozen_manifest_accepts_empty_draft_without_output(self) -> None:
        manifest_path = (Path(__file__).parent / "reports" /
                         "verified_gt_workflow_20261006" / "review_manifest.json")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        patch_path = self.root / "real_manifest_empty_patch.json"
        patch_path.write_text(json.dumps({
            "schema": "cnn_review_patch_v1",
            "dataset_id": manifest["dataset_id"],
            "annotation_policy_sha256": manifest["annotation_policy_sha256"],
            "reviews": [],
        }), encoding="utf-8")
        output = self.root / "real_manifest_should_not_exist"
        status = import_review(manifest_path, patch_path, output, validate_only=True)
        self.assertEqual(status["train_required_count"], 128)
        self.assertEqual(status["pending_train_count"], 128)
        self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
