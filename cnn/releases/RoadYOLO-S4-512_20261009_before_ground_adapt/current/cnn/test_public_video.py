"""Offline regression tests for the public-video adapter."""

from __future__ import annotations

import json
import io
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import zipfile

import cv2
import numpy as np

from .dataset import _letterbox_720
from .integer import resize_area
from .public_video import (build_visdrone, download_vid_train, download_vid_val,
                           inspect_visdrone, read_visdrone_mot)

try:
    import torch
    from .teacher import teacher_input
    from .train import FullFrameDataset
except ModuleNotFoundError:  # The lightweight data-tool Python need not contain Torch.
    torch = teacher_input = FullFrameDataset = None


class PublicVideoTest(unittest.TestCase):
    def test_fixed_vid_download_writes_verified_receipt(self) -> None:
        payload = io.BytesIO()
        with zipfile.ZipFile(payload, "w") as archive:
            archive.writestr("VisDrone2019-VID-val/annotations/example.txt", b"1,2,3")
        data = payload.getvalue()

        class Response:
            status = 200
            headers = {"Content-Length": str(len(data)),
                       "Content-Type": "application/octet-stream"}

            def __enter__(self):
                self.offset = 0
                return self

            def __exit__(self, *args):
                pass

            def read(self, size):
                block = data[self.offset:self.offset + size]
                self.offset += len(block)
                return block

        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "raw.zip"
            with (patch("cnn.public_video.VID_VAL_BYTES", len(data)),
                  patch("urllib.request.urlopen", return_value=Response())):
                receipt = download_vid_val(destination)
            self.assertEqual(receipt["zip_entries"], 1)
            self.assertTrue(destination.is_file())
            self.assertTrue(destination.with_suffix(".zip.receipt.json").is_file())
            with self.assertRaises(FileExistsError):
                download_vid_val(destination)

            train_destination = Path(temporary) / "train.zip"
            with (patch("cnn.public_video.VID_TRAIN_BYTES", len(data)),
                  patch("cnn.public_video.SPACE_RESERVE_BYTES", 1),
                  patch("cnn.public_video.shutil.disk_usage",
                        return_value=SimpleNamespace(free=len(data) + 1)),
                  patch("urllib.request.urlopen", return_value=Response())):
                train_receipt = download_vid_train(train_destination)
            self.assertEqual(train_receipt["subset"], "train")
            self.assertIn("not blind/newtest", train_receipt["purpose"])

    def test_visdrone_vid_mapping_is_development_complete_not_formal(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            root = base / "VisDrone2019-MOT-val"
            sequence = root / "sequences" / "uav0000001_00000_v"
            annotation = root / "annotations" / f"{sequence.name}.txt"
            sequence.mkdir(parents=True)
            annotation.parent.mkdir()
            frame = np.full((50, 100, 3), 127, dtype=np.uint8)
            self.assertTrue(cv2.imwrite(str(sequence / "0000001.jpg"), frame))
            self.assertTrue(cv2.imwrite(str(sequence / "0000002.jpg"), frame))
            categories = [1, 2, 3, 4, 5, 6, 9, 10, 7, 8, 0, 11]
            lines = [f"1,{index},1,1,10,10,1,{category},0,0"
                     for index, category in enumerate(categories, 1)]
            lines.append("1,99,1,1,10,10,0,4,0,0")
            annotation.write_text("\n".join(lines) + "\n", encoding="utf-8")

            source_audit = inspect_visdrone(root)
            self.assertEqual(source_audit["sequence_count"], 1)
            self.assertEqual(source_audit["image_count"], 2)
            self.assertEqual(source_audit["category_score_counts"]["car:score1"], 1)
            self.assertEqual(source_audit["sequences"][0]["frames_without_annotation_rows"], 1)
            self.assertEqual(source_audit["class_density_and_cap32"]["person"]["box_count"], 2)

            output, reports = base / "output", base / "reports"
            document = build_visdrone(
                root, output, None, reports, task="vid",
                split_map={sequence.name: "train"})
            self.assertTrue(document["training_eligible"])
            self.assertEqual(document["manifest_status"],
                             "source_declared_complete_development")
            self.assertEqual(len(document["images"]), 2)
            first = document["images"][0]
            self.assertEqual(first["labels"], [0, 0, 1, 1, 1, 1, 1, 1])
            self.assertEqual(len(first["ignore_boxes"]), 5)
            self.assertEqual(first["box_metadata"][2]["original_label"], "bicycle")
            self.assertEqual(first["ignore_metadata"][-1]["score"], 0)
            self.assertTrue(all(not row["incomplete_frame"] for row in document["images"]))
            self.assertTrue(first["rider_box_policy_review_required"])
            provenance = json.loads(next(reports.glob("*provenance.json")).read_text())
            self.assertTrue(provenance["negative_supervision_allowed"])
            self.assertFalse(provenance["formal_road_eligible"])

            raw_output, raw_reports = base / "raw_output", base / "raw_reports"
            raw_document = build_visdrone(
                root, raw_output, None, raw_reports, task="vid",
                split_map={sequence.name: "train"}, raw_images=True)
            raw_row, prepared_row = raw_document["images"][0], document["images"][0]
            self.assertTrue(raw_row["preprocess"]["raw_image"])
            self.assertEqual(Path(raw_row["image"]), (sequence / "0000001.jpg").resolve())
            self.assertFalse((raw_output / "images").exists())
            for field in ("boxes", "labels", "ignore_boxes", "box_metadata",
                          "ignore_metadata"):
                self.assertEqual(raw_row[field], prepared_row[field])

            prepared_bgr = cv2.imread(str(output / prepared_row["image"]), cv2.IMREAD_COLOR)
            source_bgr = cv2.imread(raw_row["image"], cv2.IMREAD_COLOR)
            letterboxed, _ = _letterbox_720(cv2.cvtColor(source_bgr,
                                                         cv2.COLOR_BGR2RGB))
            self.assertTrue(np.array_equal(
                cv2.cvtColor(prepared_bgr, cv2.COLOR_BGR2RGB), resize_area(letterboxed)))

            if torch is not None:
                training_row = {**raw_row, "image_path": Path(raw_row["image"]),
                                "teacher_key": raw_row["image"]}
                student, student_target, _ = FullFrameDataset([training_row], "train")[0]
                expected_student = torch.from_numpy(
                    resize_area(letterboxed).astype(np.float32)).permute(2, 0, 1) - 128.0
                torch.testing.assert_close(student, expected_student)
                self.assertEqual(student_target["boxes"].shape[0], len(raw_row["boxes"]))
                self.assertEqual(tuple(
                    teacher_input(training_row, torch.device("cpu")).shape),
                    (1, 3, 576, 1024))

    def test_rejects_unknown_category_and_blind_path(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            bad = base / "bad.txt"
            bad.write_text("1,1,0,0,1,1,1,12,0,0\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "unknown category"):
                read_visdrone_mot(bad)
            with self.assertRaisesRegex(ValueError, "blind/reserve"):
                build_visdrone(base / "blind_reserve", base / "out", "newtest",
                               base / "reports", task="vid")


if __name__ == "__main__":
    unittest.main()
