"""Stage the reviewed train subset and test its CPU input/loss contract, never fit."""
from collections import Counter
import json
from pathlib import Path
import time

import numpy as np
from PIL import Image
import torch

from .dataset import (_refuse_blind, _letterbox_transform, _letterboxed_box,
                      audit, sha256_file)
from .import_verified_review import import_review
from .loss import YOLOXLoss, pairwise_iou
from .model import RoadYOLOS4
from .train import FullFrameDataset, load_dataset_manifest


ROOT = Path(__file__).resolve().parent.parent
PACKAGE = ROOT / "cnn/reports/verified_gt_workflow_20261006"
VERIFIED = PACKAGE / "verified_import_20261006_user_v2"
OUT = ROOT / "cnn/reports/verified_gt_followup_20261007"
CHECKPOINT = ROOT / "cnn/releases/RoadYOLO-S4-512_20261005_before_supervised5/cnn/runs/person_native_recovery_20261004/epoch_0006.pt"


def write(path, value):
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def convert_frame(image):
    if image["bucket"] != "train_review" or image["split"] != "train":
        raise ValueError("only the reviewed training subset may be staged")
    if image["manual_review"]["complete"] is not True:
        raise ValueError("unsigned review")
    transform = _letterbox_transform(image["width"], image["height"])
    row = dict(image=image["raw_file_absolute"], source_sha256=image["source_sha256"],
               scene_id=image["source_scene_id"], source_frame=image["frame_index"] - image["source_metadata"]["frame_base"],
               split="train", incomplete_frame=False, boxes=[], labels=[], ignore_boxes=[],
               preprocess=dict(raw_image=True, letterbox_1280x720=transform),
               teacher_key=image["image_id"], manual_review_image_id=image["image_id"],
               camera_id=image["camera_id"], source_frame_base=0, native_frame_index=image["frame_index"],
               native_labels=image["labels"])
    if row["source_frame"] < 0:
        raise ValueError("source frame is outside its declared numbering base")
    for label in image["labels"]:
        x1, y1, x2, y2 = label["bbox"]
        if (not np.isfinite(label["bbox"]).all() or
                not (0 <= x1 < x2 <= image["width"] and 0 <= y1 < y2 <= image["height"])):
            raise ValueError("invalid native half-open coordinates")
        box = _letterboxed_box([x1, y1, x2-x1, y2-y1], transform)
        if label["class"] == "ignore":
            row["ignore_boxes"].append(box)
        elif label["class"] in {"person", "vehicle"}:
            row["boxes"].append(box)
            row["labels"].append({"person": 0, "vehicle": 1}[label["class"]])
        else:
            raise ValueError("unknown reviewed class")
    return row


def duplicate_hints(image):
    positive = [item for item in image["labels"] if item["class"] != "ignore"]
    if len(positive) < 2:
        return []
    boxes = torch.tensor([item["bbox"] for item in positive], dtype=torch.float32)
    ious = pairwise_iou(boxes, boxes)
    return [dict(image_id=image["image_id"], legacy_id=image["legacy_id"],
                 first=positive[i]["target_id"], second=positive[j]["target_id"],
                 iou=float(ious[i, j]), reason="same_class_overlap_hint_not_automatic_deletion")
            for i in range(len(positive)) for j in range(i+1, len(positive))
            if positive[i]["class"] == positive[j]["class"] and ious[i, j] >= .8]


def main(verified_dir=VERIFIED, output_dir=OUT):
    started = time.perf_counter()
    torch.set_num_threads(2)
    verified_dir, output_dir = Path(verified_dir), Path(output_dir)
    labels_path = verified_dir / "labels_verified.json"
    receipt = read(verified_dir / "import_receipt.json")
    assert sha256_file(labels_path) == receipt["outputs"]["labels_verified_sha256"]
    assert sha256_file(verified_dir / "review_patch.json") == receipt["frozen_inputs"]["patch_sha256"]
    validation = import_review(PACKAGE / "review_manifest_teacher.json", verified_dir / "review_patch.json",
                               output_dir / "not_exported", validate_only=True)
    assert validation["train_complete_count"] == 128 and validation["pending_train_count"] == 0
    verified = read(labels_path)
    assert verified["schema"] == "cnn_verified_labels_v1" and len(verified["images"]) == 128
    assert verified["dataset_id"] == receipt["dataset_id"]
    output_dir.mkdir(exist_ok=False)
    rows, corrections, duplicates = [], [], []
    for image in verified["images"]:
        path = Path(image["raw_file_absolute"])
        _refuse_blind(path)
        assert sha256_file(path) == image["source_sha256"]
        with Image.open(path) as raw:
            assert raw.size == (image["width"], image["height"])
        row = convert_frame(image)
        transform = row["preprocess"]["letterbox_1280x720"]
        for label in image["labels"]:
            expected = [(label["bbox"][i]*transform["scale_x" if i % 2 == 0 else "scale_y"]
                         + transform["offset_x" if i % 2 == 0 else "offset_y"])*.4 for i in range(4)]
            actual = _letterboxed_box([label["bbox"][0], label["bbox"][1],
                                      label["bbox"][2]-label["bbox"][0], label["bbox"][3]-label["bbox"][1]], transform)
            np.testing.assert_allclose(actual, expected, rtol=0, atol=1e-6)
            if label["action"] != "A":
                corrections.append(dict(image_id=image["image_id"], legacy_id=image["legacy_id"], **label))
        duplicates.extend(duplicate_hints(image))
        row.update(image_path=path)
        rows.append(row)
    document = dict(schema_version=1, task="detection", input_size=[512, 288], classes=["person", "vehicle"],
                    manifest_status="verified_train_subset_staging", training_eligible=False,
                    purpose="CPU_verified_training_subset_preflight_not_training_clearance",
                    source_verified_sha256=sha256_file(labels_path),
                    images=[{key: value for key, value in row.items() if key != "image_path"} for row in rows])
    manifest = output_dir / "dataset_train_staging.json"
    write(manifest, document)
    dataset = FullFrameDataset(rows, "train", mosaic=False)
    input_hashes = []
    for index, row in enumerate(rows):
        tensor, target, key = dataset[index]
        assert tuple(tensor.shape) == (3, 288, 512) and torch.isfinite(tensor).all()
        assert tensor.min() >= -128 and tensor.max() <= 127 and key == row["teacher_key"]
        np.testing.assert_array_equal(target["labels"], row["labels"])
        np.testing.assert_allclose(target["boxes"], np.asarray(row["boxes"]).reshape(-1, 4), rtol=0, atol=2e-5)
        np.testing.assert_allclose(target["ignore_boxes"], np.asarray(row["ignore_boxes"]).reshape(-1, 4), rtol=0, atol=2e-5)
        input_hashes.append(dict(image_id=key, positive_boxes=len(row["boxes"]), ignore_boxes=len(row["ignore_boxes"])))
    try:
        load_dataset_manifest(manifest)
    except ValueError as exc:
        training_rejection = str(exc)
        assert "not marked training_eligible" in training_rejection
    else:
        raise AssertionError("train-only staging must not be launchable")
    release = read(CHECKPOINT.parents[3] / "release.json")
    assert sha256_file(CHECKPOINT) == release["checkpoint_sha256"]
    checkpoint = torch.load(CHECKPOINT, map_location="cpu", weights_only=False)
    model = RoadYOLOS4().eval()
    model.load_state_dict(checkpoint["model"])
    before = {key: value.clone() for key, value in model.state_dict().items()}
    # CPU gradient contract only: no optimizer, no train(), no BN running-stat update.
    tensor, target, key = dataset[0]
    loss = YOLOXLoss()(model(tensor.unsqueeze(0)), [target])
    assert torch.isfinite(loss["loss"]) and loss["num_foreground"] > 0
    loss["loss"].backward()
    assert all(torch.isfinite(parameter.grad).all() for parameter in model.parameters() if parameter.grad is not None)
    assert all(torch.equal(value, before[key]) for key, value in model.state_dict().items())
    assert sha256_file(labels_path) == receipt["outputs"]["labels_verified_sha256"]
    summary = dict(status="CPU_train_subset_preflight_passed_validation_truth_pending", train_images=128,
                   audit=audit(document), input_checks=input_hashes, correction_counts=receipt["stats"],
                   duplicate_hint_count=len(duplicates), manual_review_of_hints_required=True,
                   CPU_forward_backward=dict(image_id=key, loss=float(loss["loss"].detach()),
                       foreground=int(loss["num_foreground"]), parameter_and_BN_changes=0, optimizer_steps=0),
                   training_launch_rejected=training_rejection, source_patch_sha256=receipt["frozen_inputs"]["patch_sha256"],
                   validation_frames_pending=124, stress_frames_pending=24,
                   production_training_started=False, GPU_used=False, formal_acceptance=False,
                   checkpoint_sha256=sha256_file(CHECKPOINT), elapsed_seconds=time.perf_counter()-started,
                   source_sha256={name:sha256_file(ROOT/"cnn"/name) for name in
                                  ("prepare_verified_train.py", "dataset.py", "train.py", "loss.py", "model.py", "integer.py", "import_verified_review.py")})
    write(output_dir / "corrections_review.json", corrections)
    write(output_dir / "duplicate_hints.json", duplicates)
    write(output_dir / "report.json", summary)
    print(json.dumps({key:summary[key] for key in ("status", "train_images", "duplicate_hint_count", "CPU_forward_backward", "production_training_started", "elapsed_seconds")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
