"""Small deterministic checks for the formal training protocol."""

from __future__ import annotations

import argparse
from pathlib import Path
import tempfile

import numpy as np
from PIL import Image
import torch

from .dataset import _letterbox_720
from .integer import resize_area
from .train import (CLASS_CONTRACT, COSINE_MIN_LR_RATIO, PREPROCESS_CONTRACT,
                    FullFrameDataset, TRAINING_PROTOCOL, TeacherCache,
                    ensure_resume_eligible, protocol_for, protocol_hash, scheduled_lr,
                    validate_output_directory)


def _row(path: Path, value: int, *, raw: bool = False) -> dict:
    preprocess = {}
    if raw:
        source = np.full((480, 640, 3), value, dtype=np.uint8)
        Image.fromarray(source).save(path)
        _, transform = _letterbox_720(source)
        preprocess = {"raw_image": True, "letterbox_1280x720": transform}
    else:
        Image.fromarray(np.full((288, 512, 3), value, dtype=np.uint8)).save(path)
    return {
        "image_path": path, "boxes": [[10, 20, 110, 220]], "labels": [value & 1],
        "ignore_boxes": [[200, 100, 300, 200]], "teacher_key": path.name,
        "split": "train", "preprocess": preprocess,
    }


def main() -> None:
    assert scheduled_lr(0, 100, 10, 0.01) == 0.001
    assert scheduled_lr(9, 100, 10, 0.01) == 0.01
    assert scheduled_lr(99, 100, 10, 0.01) == 0.01 * COSINE_MIN_LR_RATIO

    args = argparse.Namespace(
        phase="supervised", epochs=300, lr=0.01, momentum=0.9, weight_decay=5e-4,
        clip_grad=10.0, batch_size=8, accum_steps=8, mosaic=True, seed=42, amp=True,
        distill_weight=1.0, checkpoint_kind="training")
    protocol = protocol_for(args, 231, None)
    assert protocol["name"] == TRAINING_PROTOCOL and len(protocol_hash(protocol)) == 64
    for checkpoint in (
            {"format": "road-yolo-checkpoint-v1", "checkpoint_kind": "diagnostic"},
            {"format": "road-yolo-checkpoint-v2", "checkpoint_kind": "diagnostic"}):
        try:
            ensure_resume_eligible(checkpoint, protocol)
        except ValueError as error:
            assert "weights-only" in str(error)
        else:
            raise AssertionError("legacy/diagnostic checkpoint resumed")

    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        output = root / "output"
        output.mkdir()
        (output / "unexpected.txt").write_text("different run", encoding="utf-8")
        resume = root / "resume.pt"
        resume.write_bytes(b"checkpoint")
        try:
            validate_output_directory(output, resume)
        except FileExistsError as error:
            assert "unknown run" in str(error)
        else:
            raise AssertionError("mixed output directory accepted")

        teacher_path = root / "teacher.pt"
        teacher = {
            "contract": "road-yolo-student-dense-v1", "student_architecture_hash": "arch",
            "strides": [4, 8, 16], "class_contract": CLASS_CONTRACT,
            "dataset_sha256": "manifest", "dataset_content_sha256": "content",
            "preprocess_contract": PREPROCESS_CONTRACT, "items": {},
        }
        torch.save(teacher, teacher_path)
        TeacherCache(teacher_path, "arch", "manifest", "content")
        try:
            TeacherCache(teacher_path, "arch", "wrong", "content")
        except ValueError as error:
            assert "manifest mismatch" in str(error)
        else:
            raise AssertionError("teacher cache accepted another dataset")

        rows = [_row(root / f"prepared_{index}.png", index * 40) for index in range(4)]
        dataset = FullFrameDataset(rows, "train", mosaic=True, seed=42)
        dataset.set_epoch(7)
        image_a, target_a, key_a = dataset[0]
        image_b, target_b, key_b = dataset[0]
        torch.testing.assert_close(image_a, image_b)
        assert key_a == key_b and key_a.startswith("mosaic:")
        assert target_a["boxes"].shape == (4, 4)
        assert target_a["ignore_boxes"].shape == (4, 4)
        torch.testing.assert_close(target_a["boxes"], target_b["boxes"])
        assert (target_a["boxes"][:, (0, 2)] <= 512).all()
        assert (target_a["boxes"][:, (1, 3)] <= 288).all()

        raw_row = _row(root / "raw.png", 91, raw=True)
        raw_data = FullFrameDataset([raw_row], "train")
        actual, _, _ = raw_data[0]
        source = np.asarray(Image.open(raw_row["image_path"]).convert("RGB"))
        expected = resize_area(_letterbox_720(source)[0]).astype(np.float32)
        expected = torch.from_numpy(expected).permute(2, 0, 1) - 128.0
        torch.testing.assert_close(actual, expected)

    print("training protocol checks passed")


if __name__ == "__main__":
    main()
