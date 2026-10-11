"""Synthetic checks for raw YOLOX-S teacher-head adaptation."""

from __future__ import annotations

import math

import torch

from .teacher import (COCO_VEHICLE, EXPECTED_HEADS, TEACHER_PREPROCESS,
                      adapt_raw_head, json_hash, merge_class_logits,
                      validate_cache_metadata)


def _decoded(raw: torch.Tensor, grid_x: int, grid_y: int, stride: float) -> torch.Tensor:
    tx, ty, tw, th = raw
    return torch.tensor(((tx + grid_x) * stride, (ty + grid_y) * stride,
                         math.exp(float(tw)) * stride, math.exp(float(th)) * stride))


def main() -> None:
    classification = torch.full((1, 80, 1, 1), -8.0)
    classification[:, 0] = 0.75
    vehicle_logits = torch.tensor([-2.0, 0.25, 1.5, -0.5, 0.9])
    classification[:, COCO_VEHICLE, 0, 0] = vehicle_logits
    merged = merge_class_logits(classification)
    torch.testing.assert_close(merged[0, 0, 0, 0], torch.tensor(0.75))
    expected_probability = vehicle_logits.sigmoid().max()
    torch.testing.assert_close(merged[0, 1, 0, 0].sigmoid(), expected_probability)

    for height, width in EXPECTED_HEADS:
        regression = torch.zeros(1, 4, height, width)
        regression[:, 2] = -10.0
        regression[:, 3] = 10.0
        objectness = torch.randn(1, 1, height, width)
        classes = torch.randn(1, 80, height, width)
        adapted = adapt_raw_head(regression, objectness, classes)
        assert adapted.shape == (1, 7, height, width)
        assert adapted[:, 2].min() == -4.0 and adapted[:, 3].max() == 3.5
        torch.testing.assert_close(adapted[:, 4:5], objectness)

    raw = torch.tensor([0.25, -0.125, 0.5, -0.75])
    for teacher_stride in (8.0, 16.0, 32.0):
        teacher_box = _decoded(raw, 17, 9, teacher_stride) * 0.5
        student_box = _decoded(raw, 17, 9, teacher_stride * 0.5)
        torch.testing.assert_close(teacher_box, student_box)

    expected = {
        "dataset_sha256": "dataset", "dataset_content_sha256": "content",
        "preprocess_contract": {"student": "bound"},
        "student_architecture_hash": "architecture",
        "teacher_source_sha256": "source", "teacher_weight_sha256": "weight",
        "teacher_preprocess_sha256": json_hash(TEACHER_PREPROCESS),
    }
    payload = {**expected, "inference_dtype": "float32", "storage_dtype": "float16"}
    validate_cache_metadata(payload, expected)
    payload["teacher_weight_sha256"] = "different"
    try:
        validate_cache_metadata(payload, expected)
    except ValueError as error:
        assert "teacher_weight_sha256 mismatch" in str(error)
    else:
        raise AssertionError("cache accepted another teacher weight")
    print("teacher adapter checks passed")


if __name__ == "__main__":
    main()
