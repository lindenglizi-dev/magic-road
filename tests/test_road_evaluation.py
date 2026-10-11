"""Data contract regression; synthetic fixtures are never real model evidence."""
import argparse
import contextlib
import csv
import io
import json
import sys
import tempfile
import unittest
import subprocess
from pathlib import Path
import numpy as np

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "tools"))
from roi_dataset_tool import DatasetWriter, fpga_analysis_frame
from road_evaluation import audit_dataset, run
from measure_existing_sim import summarize_vcd
from convert_cdnet_pedestrian import convert as convert_cdnet, parse_row as parse_cdnet_row
from audit_roi_dataset import summarize as summarize_dataset
from convert_detrac_yolo_pilot import convert as convert_detrac_pilot


class RoadEvaluationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def dataset(self):
        rng = np.random.default_rng(31)
        for split in ("train", "val", "test"):
            video = self.root / f"{split}.mp4"
            video.write_bytes(split.encode())
            writer = DatasetWriter(self.root / "data", video, split, f"scene-{split}")
            for label in ("ped", "vehicle", "invalid"):
                for index in range(4):
                    image = rng.integers(0, 15, (144, 256), dtype=np.uint8)
                    if label == "ped":
                        image[2:29, 12:19] = 200
                    elif label == "vehicle":
                        image[12:19, 2:29] = 200
                    self.assertTrue(writer.save(image, index + 10 * {"ped": 0, "vehicle": 1, "invalid": 2}[label],
                                                30, (1280, 720), (0, 0, 31, 31), label).saved)
        return self.root / "data"

    def test_source_and_scene_leakage_rejected(self):
        root = self.dataset()
        with self.assertRaises(ValueError):
            DatasetWriter(root, self.root / "test.mp4", "train", "scene-test")
        copied = self.root / "renamed.mp4"
        copied.write_bytes((self.root / "test.mp4").read_bytes())
        with self.assertRaises(ValueError):
            DatasetWriter(root, copied, "train", "different-name")
        unrelated = self.root / "unrelated.mp4"
        unrelated.write_bytes(b"new content")
        with self.assertRaises(ValueError):
            DatasetWriter(root, unrelated, "train", "scene-val")

    def test_dataset_audit_reports_coverage_without_claiming_readiness(self):
        report = summarize_dataset(self.dataset())
        self.assertEqual(report["status"], "pass")
        self.assertEqual(report["sample_count"], 36)
        self.assertTrue(report["readiness"]["fit_ready"])
        self.assertTrue(report["readiness"]["invalid_evaluation_ready"])

    def test_mutated_roi_rejected(self):
        root = self.dataset()
        rows = audit_dataset(root)
        import cv2
        cv2.imwrite(str(root / rows[0]["roi_path"]), np.zeros((32, 32), dtype=np.uint8))
        with self.assertRaisesRegex(ValueError, "pixels changed"):
            audit_dataset(root)

    def test_holdout_is_separate_and_invalid_reported(self):
        root = self.dataset()
        criteria = self.root / "criteria.json"
        criteria.write_text(json.dumps({"ped_recall_min": .85, "vehicle_recall_min": .9,
                                       "invalid_false_accept_max": .1, "frozen": True,
                                       "rtl_python_class_disagreements_max": 0,
                                       "acceptance_roi_source": "manual"}))
        args = argparse.Namespace(dataset=root, output=self.root / "experiment", phase="fit",
            criteria=criteria, train_source="manual", c_grid=[.1, 1.0], seed=3,
            weight_bits=12, accumulator_bits=40)
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(run(args), 0)
        self.assertFalse((args.output / "test_metrics.json").exists())
        args.phase = "test"
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(run(args), 0)
        metrics = json.loads((args.output / "test_metrics.json").read_text())
        self.assertEqual(metrics["by_roi_source"]["manual"]["quantized"]["invalid_false_accept_rate"], 1.0)
        self.assertEqual(metrics["by_roi_source"]["ccl"]["status"], "not_measured")
        self.assertFalse(metrics["acceptance"]["integration_ready"])
        self.assertIn("invalid_false_accept_rate", metrics["acceptance"]["blockers"])
        with self.assertRaisesRegex(ValueError, "already evaluated"):
            run(args)

    def test_pending_criteria_cannot_create_formal_freeze(self):
        root = self.dataset()
        criteria = self.root / "criteria.pending.json"
        criteria.write_text(json.dumps({"ped_recall_min": .85, "vehicle_recall_min": .9,
                                       "invalid_false_accept_max": .1, "frozen": False,
                                       "rtl_python_class_disagreements_max": 0,
                                       "acceptance_roi_source": "manual"}))
        args = argparse.Namespace(dataset=root, output=self.root / "pending-experiment", phase="fit",
            criteria=criteria, train_source="manual", c_grid=[1.0], seed=3,
            weight_bits=12, accumulator_bits=40)
        with self.assertRaisesRegex(ValueError, "criteria.frozen=true"):
            run(args)
        self.assertFalse((args.output / "freeze.json").exists())

    def test_frozen_null_criterion_fails_closed(self):
        root = self.dataset()
        criteria = self.root / "criteria.null.json"
        criteria.write_text(json.dumps({"ped_recall_min": None, "vehicle_recall_min": .9,
                                       "invalid_false_accept_max": .1, "frozen": True,
                                       "rtl_python_class_disagreements_max": 0,
                                       "acceptance_roi_source": "manual"}))
        args = argparse.Namespace(dataset=root, output=self.root / "null-experiment", phase="fit",
            criteria=criteria, train_source="manual", c_grid=[1.0], seed=3,
            weight_bits=12, accumulator_bits=40)
        with self.assertRaisesRegex(ValueError, "ped_recall_min"):
            run(args)
        self.assertFalse((args.output / "freeze.json").exists())

    def test_dimensions_fail_closed(self):
        with self.assertRaises(ValueError):
            fpga_analysis_frame(np.zeros((1080, 1920, 3), dtype=np.uint8))
        self.assertEqual(fpga_analysis_frame(np.zeros((720, 1280, 3), dtype=np.uint8)).shape, (144, 256))

    def test_vcd_timestamp_and_alias_sampling(self):
        path = self.root / "test.vcd"
        path.write_text('$scope module tb $end\n$var wire 1 ! clk $end\n'
                        '$var wire 1 " rst_n $end\n$var wire 1 # pulse $end\n'
                        '$upscope $end\n#0\n0!\n1"\n0#\n#5\n1!\n1#\n'
                        '#10\n0!\n#15\n1!\n0#\n')
        result = summarize_vcd(path, "clk", "rst_n", ["pulse"])
        self.assertEqual(result["signals"]["pulse"]["runs"], [[1, 1]])

    def test_public_sequence_prepare_and_import(self):
        import cv2
        source = self.root / "source"
        source.mkdir()
        for index in range(3):
            image = np.zeros((90, 160, 3), dtype=np.uint8)
            image[20:70, 50:110] = (20 + 40 * index, 120, 230)
            self.assertTrue(cv2.imwrite(str(source / f"frame_{index:03d}.png"), image))
        annotations = self.root / "annotations.csv"
        with annotations.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, ["frame_index", "xmin", "ymin", "xmax", "ymax",
                                                   "label", "original_label", "object_id"])
            writer.writeheader()
            for index, label in enumerate(("ped", "vehicle", "invalid")):
                writer.writerow({"frame_index": index, "xmin": 50, "ymin": 20, "xmax": 109,
                                 "ymax": 69, "label": label, "original_label": label, "object_id": index})
        prepared = self.root / "prepared"
        subprocess.run([sys.executable, str(PROJECT / "tools/prepare_public_video.py"),
            "--input", str(source), "--output", str(prepared), "--dataset-name", "fixture",
            "--sequence-id", "sequence", "--scene-id", "scene-public",
            "--source-url", "https://example.invalid/dataset", "--license-url",
            "https://example.invalid/license", "--fps", "25", "--annotations", str(annotations)], check=True)
        review = self.root / "review"
        subprocess.run([sys.executable, str(PROJECT / "tools/review_prepared_annotations.py"),
            "--prepared", str(prepared), "--output", str(review), "--frames", "2"], check=True)
        review_report = json.loads((review / "review.json").read_text(encoding="utf-8"))
        self.assertEqual(review_report["review_status"], "pending_human_visual_check")
        self.assertTrue((review / "contact_sheet.jpg").is_file())
        dataset = self.root / "public-data"
        subprocess.run([sys.executable, str(PROJECT / "tools/import_public_rois.py"),
            "--prepared", str(prepared), "--dataset", str(dataset), "--split", "train", "--stride", "1"], check=True)
        rows = audit_dataset(dataset)
        self.assertEqual({row["label"] for row in rows}, {"ped", "vehicle", "invalid"})
        self.assertEqual({row["roi_source"] for row in rows}, {"annotated"})
        self.assertTrue((dataset / "provenance").is_dir())

    def test_ccl_candidate_export_uses_replay_pixels(self):
        frames = self.root / "frames"
        frames.mkdir()
        values = np.arange(144 * 256, dtype=np.uint32) & 0xFF
        (frames / "frame_0000.hex").write_text("\n".join(f"{v:02x}" for v in values) + "\n")
        source = self.root / "source.mp4"
        source.write_bytes(b"fixture")
        (frames / "manifest.json").write_text(json.dumps({
            "source": str(source), "source_sha256": __import__("hashlib").sha256(source.read_bytes()).hexdigest(),
            "preprocessing": "rtl_shift_gray_stride5_v1", "frame_map": [{"replay_frame": 0, "source_frame": 12}],
            "source_fps": 30
        }))
        objects = self.root / "objects.csv"
        with objects.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, ["frame", "slot", "valid", "class", "xmin", "ymin", "xmax", "ymax"])
            writer.writeheader()
            writer.writerow({"frame": 0, "slot": 0, "valid": 1, "class": 2,
                             "xmin": 10, "ymin": 20, "xmax": 25, "ymax": 27})
        candidates = self.root / "candidates"
        subprocess.run([sys.executable, str(PROJECT / "tools/ccl_roi_candidates.py"),
            "--frames", str(frames), "--objects", str(objects), "--output", str(candidates),
            "--scene-id", "scene-ccl", "--split", "val"], check=True)
        with (candidates / "candidates.csv").open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["source_frame"], "12")
        self.assertEqual(rows[0]["label"], "")
        self.assertTrue((candidates / "contact_sheet_01.jpg").is_file())
        self.assertTrue((candidates / "frame_overlay_01.jpg").is_file())

    def test_cdnet_fractional_boxes_and_one_based_frames(self):
        mapped = parse_cdnet_row("1 0 0.5 44.5 60 196", 1)
        self.assertEqual(mapped["frame_index"], 0)
        self.assertEqual((mapped["xmin"], mapped["ymin"], mapped["xmax"], mapped["ymax"]),
                         (0, 44, 60, 240))

        annotations = self.root / "cdnet-gt"
        images = self.root / "cdnet-images"
        sequence = "fixtureSequence"
        (annotations / sequence).mkdir(parents=True)
        (annotations / sequence / "gt.txt").write_text(
            "1 0 0.5 1.5 2 3\x7f\n1 0 4 5 6 7\n"
            "1 0 15.5 2 2 3\n1 0 20 2 2 3\n", encoding="utf-8")
        (images / sequence / "input").mkdir(parents=True)
        import cv2
        self.assertTrue(cv2.imwrite(str(images / sequence / "input" / "in000001.jpg"),
                                   np.zeros((16, 16, 3), dtype=np.uint8)))
        splits = self.root / "splits.json"
        splits.write_text(json.dumps({"train": [sequence], "val": [], "test": []}), encoding="utf-8")
        output = self.root / "canonical"
        catalog = convert_cdnet(annotations, images, output, splits)
        self.assertEqual(catalog["totals"]["source_annotations"], 4)
        self.assertEqual(catalog["totals"]["annotations"], 3)
        self.assertEqual(catalog["totals"]["clipped_to_image"], 1)
        self.assertEqual(catalog["totals"]["excluded_no_intersection"], 1)
        self.assertEqual(catalog["sequences"][0]["sanitized_trailing_ascii_del"], 1)
        with (output / sequence / "annotations.csv").open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(rows[0]["frame_index"], "0")
        self.assertNotEqual(rows[0]["object_id"], rows[1]["object_id"])
        self.assertEqual(rows[0]["label"], "ped")
        self.assertEqual(rows[2]["xmax"], "15")
        self.assertTrue((output / sequence / "excluded_annotations.csv").is_file())
        self.assertIn("source frameID", catalog["frame_index_contract"])

    def test_index_only_sequence_never_invents_timestamps(self):
        import cv2
        source = self.root / "index-only-source"
        source.mkdir()
        for index in range(2):
            self.assertTrue(cv2.imwrite(str(source / f"in{index + 1:06d}.jpg"),
                                       np.zeros((24, 32, 3), dtype=np.uint8)))
        prepared = self.root / "index-only-prepared"
        subprocess.run([sys.executable, str(PROJECT / "tools/prepare_public_video.py"),
            "--input", str(source), "--output", str(prepared), "--dataset-name", "fixture",
            "--sequence-id", "unknown-fps", "--scene-id", "scene-index-only",
            "--source-url", "https://example.invalid/dataset", "--license-url",
            "https://example.invalid/license", "--index-only"], check=True)
        receipt = json.loads((prepared / "provenance.json").read_text(encoding="utf-8"))
        self.assertIsNone(receipt["fps"])
        self.assertEqual(receipt["container_fps"], 1.0)
        self.assertEqual(receipt["timebase"], "index_only_unknown_source_cadence")
        self.assertTrue(all(item["timestamp_ms"] is None for item in receipt["frame_map"]))

    def test_detrac_pilot_converter_groups_one_source_sequence(self):
        import cv2
        source = self.root / "detrac-pilot"
        (source / "images").mkdir(parents=True)
        (source / "labels").mkdir()
        stem = "MVI_41063_img00009_jpg.rf." + "a" * 32
        self.assertTrue(cv2.imwrite(str(source / "images" / f"{stem}.jpg"),
                                   np.zeros((640, 640, 3), dtype=np.uint8)))
        (source / "labels" / f"{stem}.txt").write_text(
            "0 0.5 0.5 0.25 0.5\n2 0.1 0.1 0.2 0.2\n", encoding="utf-8")
        output = self.root / "detrac-canonical"
        report = convert_detrac_pilot(source, output, "MVI_41063",
                                      {0: "car", 1: "bus", 2: "truck", 3: "van"})
        self.assertEqual(report["frame_count"], 1)
        self.assertEqual(report["annotation_count"], 2)
        self.assertEqual(report["class_counts"]["car"], 1)
        self.assertEqual(report["class_counts"]["truck"], 1)
        with (output / "annotations.csv").open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual({row["label"] for row in rows}, {"vehicle"})
        self.assertEqual(rows[0]["source_frame_id"], "9")


if __name__ == "__main__":
    unittest.main()
