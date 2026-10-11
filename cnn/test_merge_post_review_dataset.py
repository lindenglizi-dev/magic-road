"""Small CPU regression: identity join, signed GT, ignore, and isolation."""
from copy import deepcopy
import unittest

from .dataset import _letterbox_transform
from .import_verified_review import CHECKS
from .merge_post_review_dataset import merge_document


def fixture():
    transform = _letterbox_transform(1280, 720)
    rows = [dict(image=f"C:/fixture/{index}/0000001.png", boxes=[[4, 8, 12, 16]],
                 labels=[0], ignore_boxes=[[20, 20, 40, 40]],
                 ignore_metadata=[dict(label=-1, crowd=False)], scene_id=f"scene{index}",
                 split="val" if index == 3 else "train", source_sha256=str(index)*64,
                 source_frame=1, incomplete_frame=False, annotation_complete=True,
                 preprocess=dict(raw_image=True, letterbox_1280x720=transform))
            for index in range(4)]
    source = dict(schema_version=1, task="detection", input_size=[512, 288],
                  classes=["person", "vehicle"], training_eligible=True, images=rows)
    reviewed = []
    for index in range(2):
        reviewed.append(dict(image_id=f"r{index}", legacy_id="train_075" if index else "train_001",
                             bucket="train_review", split="train", width=1280, height=720,
                             camera_id="unverified_fixture_camera",
                             source_scene_id=f"scene{index}", frame_index=1,
                             source_metadata=dict(frame_base=1), source_sha256=str(index)*64,
                             raw_file_absolute=rows[index]["image"],
                             manual_review=dict(complete=True, raw_seen=True, reviewer="human",
                                                checks={name: True for name in CHECKS}, notes=""),
                             labels=[dict(class_="unused", **{"class": "vehicle"},
                                          bbox=[10, 20, 30, 40], action="M"),
                                     {"class": "ignore", "bbox": [50, 50, 100, 100], "action": "A"}]))
    return source, dict(schema="cnn_verified_labels_v1", images=reviewed)


class MergeTest(unittest.TestCase):
    def test_preserve_source_and_validation_and_reject_bad_identity(self):
        source, verified = fixture()
        before = deepcopy(source)
        result, receipt = merge_document(source, verified, expected_reviewed=2)
        self.assertEqual(source, before)
        self.assertEqual(len(result["images"]), 3)
        self.assertEqual(receipt["matched_reviewed"], 2)
        self.assertEqual(receipt["unreviewed_train_images"], 1)
        self.assertEqual(result["images"][0]["labels"], [1])
        self.assertEqual(result["images"][0]["boxes"], [[4.0, 8.0, 12.0, 16.0]])
        self.assertEqual(result["images"][0]["ignore_metadata"], source["images"][0]["ignore_metadata"])
        self.assertEqual(result["images"][1:], source["images"][2:])
        self.assertFalse(result["formal_acceptance"])
        for name, alter in (
                ("unsigned", lambda s, v: v["images"][0]["manual_review"].update(complete=False)),
                ("uncertain", lambda s, v: v["images"][0]["manual_review"]["checks"].update(ignore=False)),
                ("validation", lambda s, v: s["images"][0].update(split="val")),
                ("zero_based_join", lambda s, v: v["images"][0].update(frame_index=0)),
                ("pixel_hash", lambda s, v: v["images"][0].update(source_sha256="f"*64)),
                ("preprocess", lambda s, v: s["images"][0]["preprocess"].update(letterbox_1280x720={})),
                ("stress", lambda s, v: v["images"][0].update(bucket="person_background_aux")),
                ("newtest", lambda s, v: s["images"][3].update(split="newtest")),
                ("bad_native_filename", lambda s, v: s["images"][0].update(image="C:/fixture/0/0000002.png"))):
            with self.subTest(name=name):
                changed_source, changed_verified = deepcopy(source), deepcopy(verified)
                alter(changed_source, changed_verified)
                with self.assertRaises(ValueError):
                    merge_document(changed_source, changed_verified, expected_reviewed=2)
        broken = deepcopy(verified)
        broken["images"][1].update(source_scene_id="scene0")
        with self.assertRaisesRegex(ValueError, "duplicate reviewed"):
            merge_document(source, broken, expected_reviewed=2)


if __name__ == "__main__":
    unittest.main()
