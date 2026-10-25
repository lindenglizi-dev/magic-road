"""GT/ignore gradient negatives and bounded teacher-cache coverage tests."""
import argparse
import copy
import json
from pathlib import Path
import tempfile
from unittest.mock import patch

import torch

from .loss import DISTILL_CONTRACT, dense_distillation_loss
from .teacher import EXPECTED_HEADS, build_cache, build_sharded_cache
from .train import (CLASS_CONTRACT, PREPROCESS_CONTRACT, TeacherCache,
                    ensure_resume_eligible, protocol_for)


def fails(operation, error=ValueError):
    try:
        operation()
    except error:
        return
    raise AssertionError(f"expected {error.__name__}")


def main():
    torch.set_num_threads(2)
    student = [torch.zeros(1, 7, 1, w, requires_grad=True) for w in (2, 1, 1)]
    teacher = [torch.zeros_like(head) for head in student]
    for head in teacher:
        head[:, :2] = .5
        head[:, 4:6] = 8  # Generic objectness + person.
        head[:, 6] = -8
    targets = [dict(boxes=[[0., 0., 4., 4.], [4., 0., 8., 4.]], labels=[0, 0],
                    ignore_boxes=[[4., 0., 8., 4.]])]
    value = dense_distillation_loss(student, teacher, targets)
    assert value.isfinite() and value > 0
    value.backward()
    assert student[0].grad[0, :, 0, 0].abs().sum() > 0
    assert student[0].grad[0, :, 0, 1].abs().sum() == 0
    assert all(head.grad.abs().sum() == 0 for head in student[1:])
    for kind in ("unsupported_class", "empty_gt", "wrong_gt_class", "unlocalized", "wrong_teacher_argmax"):
        candidate = [head.detach().clone().requires_grad_() for head in student]
        cached = [head.clone() for head in teacher]
        target = copy.deepcopy(targets)
        if kind == "unsupported_class":
            for head in cached:
                head[:, 5:] = -12  # Confident non-target COCO object must not teach.
        elif kind == "empty_gt":
            target[0].update(boxes=[], labels=[])
        elif kind == "wrong_gt_class":
            target[0]["labels"] = [1, 1]
        elif kind == "wrong_teacher_argmax":
            for head in cached:
                head[:, 5] = 1  # Person score above 0.3, but vehicle still wins.
                head[:, 6] = 8
        else:
            for head in cached:
                head[:, :2] = 100
        loss = dense_distillation_loss(candidate, cached, target)
        assert loss.item() == 0, kind
        loss.backward()
        assert all(head.grad.abs().sum() == 0 for head in candidate), kind
    fails(lambda: dense_distillation_loss(student, teacher, []))
    fails(lambda: dense_distillation_loss(student, teacher[:2], targets))

    binding = dict(contract="road-yolo-student-dense-v1", student_architecture_hash="arch",
                   strides=[4, 8, 16], class_contract=CLASS_CONTRACT,
                   dataset_sha256="manifest", dataset_content_sha256="content",
                   preprocess_contract=PREPROCESS_CONTRACT, split="train",
                   teacher_source_sha256="a" * 64, teacher_weight_sha256="b" * 64,
                   teacher_preprocess_sha256="c" * 64, inference_dtype="float32",
                   storage_dtype="float16", format="road-yolo-teacher-cache-v1")
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        rows = [dict(teacher_key=f"frame_{i}") for i in range(5)]
        calls = []

        def fake_input(row, _device):
            calls.append(row["teacher_key"])
            return torch.zeros(1)

        def fake_heads(_model, _input):
            return [torch.zeros(1, 7, h, w) for h, w in EXPECTED_HEADS]

        index_path = root / "index.json"
        with patch("cnn.teacher._prepare_cache", return_value=(rows, binding, object())) as prepare, \
                patch("cnn.teacher.teacher_input", side_effect=fake_input), \
                patch("cnn.teacher.capture_raw_heads", side_effect=fake_heads):
            result = build_sharded_cache(root / "dataset.json", index_path, root, root / "weights.pt",
                                         2, torch.device("cpu"))
            assert prepare.call_count == 1
            build_cache(root / "dataset.json", root / "offset.pt", root,
                        root / "weights.pt", "train", 2, torch.device("cpu"), start_image=2)
            subset = torch.load(root / "offset.pt", weights_only=True)
            assert list(subset["items"]) == ["frame_2", "frame_3"]
        assert result["item_count"] == 5 and calls[:5] == [row["teacher_key"] for row in rows]
        calls = calls[:5]
        cache = TeacherCache(index_path, "arch", "manifest", "content")
        cache.require_keys(calls)
        fails(lambda: cache.require_keys(calls[:-1]))
        fails(lambda: cache.require_keys(calls + calls[:1]))
        for key in ("frame_0", "frame_2", "frame_4", "frame_0"):
            batch = cache.batch([key], torch.device("cpu"))
            assert tuple(batch[0].shape) == (1, 7, 72, 128)
            assert len(cache.loaded) <= 2
        fails(lambda: cache.batch(["missing"], torch.device("cpu")), KeyError)
        index = json.loads(index_path.read_text())
        bad = copy.deepcopy(index)
        bad["shards"][1]["keys"][0] = bad["shards"][0]["keys"][0]
        duplicate = root / "duplicate.json"
        duplicate.write_text(json.dumps(bad))
        fails(lambda: TeacherCache(duplicate, "arch", "manifest", "content"))
        bad = copy.deepcopy(index)
        bad["shards"][0]["sha256"] = "0" * 64
        tampered = root / "tampered.json"
        tampered.write_text(json.dumps(bad))
        fails(lambda: TeacherCache(tampered, "arch", "manifest", "content"))
        bad = copy.deepcopy(index)
        bad["shards"][0]["file"] = "../outside.pt"
        escaped = root / "escaped.json"
        escaped.write_text(json.dumps(bad))
        fails(lambda: TeacherCache(escaped, "arch", "manifest", "content"))
        bad = copy.deepcopy(index)
        bad["shards"][0]["file"] = "missing.pt"
        missing = root / "missing.json"
        missing.write_text(json.dumps(bad))
        fails(lambda: TeacherCache(missing, "arch", "manifest", "content"), FileNotFoundError)
        # Signed index with a false key list must still fail on shard loading.
        bad = copy.deepcopy(index)
        bad["shards"][0]["keys"][0] = "false_key"
        false_key = root / "false_key.json"
        false_key.write_text(json.dumps(bad))
        dishonest = TeacherCache(false_key, "arch", "manifest", "content")
        fails(lambda: dishonest.batch(["false_key"], torch.device("cpu")))

    args = argparse.Namespace(phase="supervised", epochs=20, lr=.002, momentum=.9,
                              weight_decay=5e-4, clip_grad=10., batch_size=8, accum_steps=8,
                              mosaic=False, seed=42, amp=False, distill_weight=1.,
                              checkpoint_kind="training")
    assert "distillation_contract" not in protocol_for(args, 10, None)
    args.phase = "distill"
    new_protocol = protocol_for(args, 10, "cache")
    assert new_protocol["distillation_contract"] == DISTILL_CONTRACT
    old_protocol = dict(new_protocol)
    del old_protocol["distillation_contract"]
    old_state = dict(format="road-yolo-checkpoint-v2", checkpoint_kind="training",
                     training_protocol=old_protocol, interrupted=False)
    fails(lambda: ensure_resume_eligible(old_state, new_protocol))
    print("distillation GT/ignore negatives, exact shard coverage, hash/path guards and bounded LRU passed")


if __name__ == "__main__":
    main()
