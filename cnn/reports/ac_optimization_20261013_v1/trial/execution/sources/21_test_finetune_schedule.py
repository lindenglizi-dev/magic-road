"""CPU checks for the explicit constant-LR fine-tuning protocol."""

from __future__ import annotations

import argparse
import copy
from contextlib import redirect_stderr
import io
import json
import math
from pathlib import Path
import tempfile
from unittest.mock import patch

import numpy as np
import torch
from torch.utils.data import Dataset

from . import train
from .loss import YOLOXLoss, dense_distillation_loss
from .model import RoadYOLOS4


def _fails(operation, error=ValueError) -> None:
    try:
        operation()
    except error:
        return
    raise AssertionError(f"expected {error.__name__}")


def _same(left, right) -> None:
    if torch.is_tensor(left):
        torch.testing.assert_close(left, right, rtol=0, atol=0)
    elif isinstance(left, np.ndarray):
        np.testing.assert_array_equal(left, right)
    elif isinstance(left, dict):
        assert left.keys() == right.keys()
        for key in left:
            _same(left[key], right[key])
    elif isinstance(left, (list, tuple)):
        assert len(left) == len(right)
        for a, b in zip(left, right, strict=True):
            _same(a, b)
    else:
        assert left == right


def _args(*, phase="supervised", schedule="finetune_constant", epochs=5,
          distill_weight=0.25) -> argparse.Namespace:
    return argparse.Namespace(
        phase=phase, epochs=epochs, lr=0.001, lr_schedule=schedule,
        momentum=0.9, weight_decay=5e-4, clip_grad=10.0, batch_size=8,
        accum_steps=8, mosaic=False, seed=42, amp=False,
        distill_weight=distill_weight, checkpoint_kind="training")


def _frozen_legacy_contract() -> None:
    checkpoint_path = (Path(__file__).parent /
                       "releases/RoadYOLO-S4-512_20261005_before_supervised5/cnn/runs/"
                       "person_native_recovery_20261004/epoch_0006.pt")
    checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=False)
    frozen = checkpoint["training_protocol"]
    legacy_args = argparse.Namespace(
        phase=frozen["phase"], epochs=frozen["epochs"], lr=frozen["base_lr"],
        momentum=frozen["momentum"], weight_decay=frozen["weight_decay"],
        clip_grad=frozen["clip_grad"], batch_size=frozen["microbatch"],
        accum_steps=frozen["accum_steps"], mosaic=frozen["mosaic"],
        seed=frozen["seed"], amp=frozen["amp"],
        distill_weight=frozen["distill_weight"],
        checkpoint_kind=frozen["checkpoint_kind"])
    actual = train.protocol_for(
        legacy_args, frozen["optimizer_steps_per_epoch"],
        frozen["teacher_cache_sha256"])
    assert actual == frozen
    assert train.protocol_hash(actual) == checkpoint["training_protocol_sha256"]

    total = frozen["epochs"] * frozen["optimizer_steps_per_epoch"]
    warmup = min(total, frozen["warmup_epochs"] * frozen["optimizer_steps_per_epoch"])
    for step in range(total):
        if step < warmup:
            expected = frozen["base_lr"] * (step + 1) / max(warmup, 1)
        else:
            decay_steps = total - warmup
            progress = 1.0 if decay_steps <= 1 else (step - warmup) / (decay_steps - 1)
            cosine = 0.5 * (1.0 + math.cos(math.pi * progress))
            expected = frozen["base_lr"] * (
                frozen["cosine_min_lr_ratio"] +
                (1.0 - frozen["cosine_min_lr_ratio"]) * cosine)
        assert train.scheduled_lr(step, total, warmup, frozen["base_lr"]) == expected


def _constant_contract_and_guards() -> None:
    supervised = _args()
    distill = _args(phase="distill")
    supervised_protocol = train.protocol_for(supervised, 3, None)
    distill_protocol = train.protocol_for(distill, 3, "a" * 64)
    assert supervised_protocol["name"] == train.FINETUNE_TRAINING_PROTOCOL
    assert supervised_protocol["lr_schedule"] == "finetune_constant"
    assert supervised_protocol["warmup_epochs"] == 0
    assert supervised_protocol["cosine_min_lr_ratio"] == 1.0

    supervised_lrs = [train.scheduled_lr(step, 15, 0, 0.001, supervised.lr_schedule)
                      for step in range(15)]
    distill_lrs = [train.scheduled_lr(step, 15, 0, 0.001, distill.lr_schedule)
                   for step in range(15)]
    assert supervised_lrs == distill_lrs == [0.001] * 15

    same_group = dict(format="road-yolo-checkpoint-v2", checkpoint_kind="training",
                      interrupted=False, training_protocol=supervised_protocol)
    train.ensure_resume_eligible(same_group, supervised_protocol)
    _fails(lambda: train.ensure_resume_eligible(same_group, distill_protocol))
    legacy_protocol = train.protocol_for(_args(schedule="warmup_cosine"), 3, None)
    _fails(lambda: train.ensure_resume_eligible(same_group, legacy_protocol))

    _fails(lambda: train.scheduled_lr(-1, 15, 0, 0.001, "finetune_constant"))
    _fails(lambda: train.scheduled_lr(15, 15, 0, 0.001, "finetune_constant"))
    _fails(lambda: train.scheduled_lr(0, 15, 0, 0.001, "unknown"))
    with redirect_stderr(io.StringIO()):
        _fails(lambda: train.build_parser().parse_args([
            "--dataset", "data.json", "--output", "out",
            "--lr-schedule", "unknown"]), SystemExit)


def _zero_weight_distillation_equivalence() -> None:
    torch.manual_seed(7)
    supervised_model = RoadYOLOS4()
    distill_model = copy.deepcopy(supervised_model)
    image = torch.randn(1, 3, 288, 512)
    targets = [{
        "boxes": torch.tensor([[100.0, 50.0, 130.0, 100.0]]),
        "labels": torch.tensor([0]),
        "ignore_boxes": torch.empty((0, 4)),
    }]

    supervised_outputs = supervised_model(image)
    supervised_loss = YOLOXLoss()(supervised_outputs, targets)["loss"]
    supervised_loss.backward()

    distill_outputs = distill_model(image)
    teacher = [torch.zeros_like(head) for head in distill_outputs]
    for head in teacher:
        head[:, 4:] = -8.0
    anchor = teacher[0][0, :, 18, 28]
    anchor[:2] = 0.75
    anchor[2] = math.log(7.5)
    anchor[3] = math.log(12.5)
    anchor[4] = anchor[5] = 8.0
    distillation = dense_distillation_loss(distill_outputs, teacher, targets)
    assert distillation.isfinite() and distillation > 0
    (YOLOXLoss()(distill_outputs, targets)["loss"] + 0.0 * distillation).backward()

    for supervised_parameter, distill_parameter in zip(
            supervised_model.parameters(), distill_model.parameters(), strict=True):
        torch.testing.assert_close(supervised_parameter, distill_parameter, rtol=0, atol=0)
        torch.testing.assert_close(
            supervised_parameter.grad, distill_parameter.grad, rtol=0, atol=0)


class _TinyModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.conv = torch.nn.Conv2d(1, 2, 1, bias=False)
        self.bn = torch.nn.BatchNorm2d(2)
        self.dropout = torch.nn.Dropout(0.25)

    def forward(self, images):
        return self.dropout(self.bn(self.conv(images)))

    def architecture_hash(self):
        return "tiny_finetune_schedule_v1"


class _TinyData(Dataset):
    def __init__(self, split):
        self.size = 4 if split == "train" else 2

    def __len__(self):
        return self.size

    def set_epoch(self, _epoch, mosaic=None):
        assert mosaic is False

    def __getitem__(self, index):
        return torch.full((1, 2, 2), (index + 1) / 10.0), {}, str(index)


class _TinyLoss:
    def __call__(self, outputs, _targets):
        return {"loss": outputs.square().mean()}


def _tiny_args(manifest: Path, output: Path, stop_after_epoch: int) -> argparse.Namespace:
    return train.build_parser().parse_args([
        "--dataset", str(manifest), "--output", str(output), "--device", "cpu",
        "--workers", "0", "--epochs", "5", "--batch-size", "2",
        "--accum-steps", "1", "--lr", "0.001", "--lr-schedule",
        "finetune_constant", "--no-mosaic", "--no-amp", "--stop-after-epoch",
        str(stop_after_epoch), "--checkpoint-every-seconds", "0"])


def _segmented_resume_equivalence() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        manifest = root / "dataset.json"
        manifest.write_text("{}", encoding="utf-8")
        rows = [{"image": "tiny", "image_sha256": "0" * 64}]
        with (patch.object(train, "load_dataset_manifest", return_value=({}, rows)),
              patch.object(train, "make_frame_dataset",
                           side_effect=lambda _rows, split, *_a, **_kw: _TinyData(split)),
              patch.object(train, "RoadYOLOS4", _TinyModel),
              patch.object(train, "YOLOXLoss", _TinyLoss),
              patch.object(torch.cuda, "is_available", return_value=False)):
            continuous_args = _tiny_args(manifest, root / "continuous", 0)
            assert train.train(continuous_args) == 0

            segmented_args = _tiny_args(manifest, root / "segmented", 2)
            assert train.train(segmented_args) == 0
            paused = torch.load(segmented_args.output / "last_resume.pt",
                                map_location="cpu", weights_only=False)
            assert paused["stage"] == "epoch_done" and paused["epoch_index"] == 1
            assert paused["last_lr"] == 0.001
            segmented_args.resume = segmented_args.output / "last_resume.pt"
            segmented_args.stop_after_epoch = 0
            assert train.train(segmented_args) == 0

        continuous = torch.load(continuous_args.output / "last.pt",
                                map_location="cpu", weights_only=False)
        segmented = torch.load(segmented_args.output / "last.pt",
                               map_location="cpu", weights_only=False)
        for field in ("model", "optimizer", "scaler", "rng_state"):
            _same(continuous[field], segmented[field])
        assert continuous["trained_steps"] == segmented["trained_steps"] == 10
        for log in (continuous_args.output / "train_log.jsonl",
                    segmented_args.output / "train_log.jsonl"):
            steps = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()
                     if json.loads(line).get("event") == "step"]
            assert len(steps) == 10
            assert all(item["lr"] == 0.001 for item in steps)


def main() -> None:
    torch.set_num_threads(1)
    _frozen_legacy_contract()
    _constant_contract_and_guards()
    _zero_weight_distillation_equivalence()
    _segmented_resume_equivalence()
    print("constant fine-tune schedule, legacy compatibility and CPU resume checks PASS")


if __name__ == "__main__":
    main()
