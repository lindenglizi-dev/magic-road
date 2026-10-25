"""CPU regression checks for opt-in frozen BatchNorm fine-tuning."""

from __future__ import annotations

import argparse
from contextlib import redirect_stdout
import io
from pathlib import Path
import tempfile
from unittest.mock import patch

import torch

from . import train
from .model import RoadYOLOS4
from .test_finetune_schedule import _TinyData, _TinyLoss, _TinyModel, _same


class _TrackingTinyModel(_TinyModel):
    modes: list[tuple[bool, bool]] = []

    def forward(self, images):
        self.modes.append((self.training, self.bn.training))
        return super().forward(images)


def _args(manifest: Path, output: Path, *, freeze_bn: bool = True,
          stop_after_epoch: int = 0) -> argparse.Namespace:
    options = [
        "--dataset", str(manifest), "--output", str(output), "--device", "cpu",
        "--workers", "0", "--epochs", "2", "--batch-size", "2",
        "--accum-steps", "1", "--lr", "0.001", "--lr-schedule",
        "finetune_constant", "--no-mosaic", "--no-amp", "--stop-after-epoch",
        str(stop_after_epoch), "--checkpoint-every-seconds", "0",
    ]
    if freeze_bn:
        options.append("--freeze-bn")
    return train.build_parser().parse_args(options)


def _real_model_policy() -> None:
    torch.manual_seed(7)
    model = RoadYOLOS4()
    batch_norms = [module for module in model.modules()
                   if isinstance(module, torch.nn.BatchNorm2d)]
    assert len(batch_norms) == 61

    train.set_training_mode(model)
    assert all(module.training for module in batch_norms)
    assert all(parameter.requires_grad for module in batch_norms
               for parameter in module.parameters())

    train.set_training_mode(model, freeze_bn=True)
    assert model.training
    assert all(not module.training for module in batch_norms)
    assert all(not parameter.requires_grad for module in batch_norms
               for parameter in module.parameters())
    frozen = {name: value.detach().clone() for name, value in model.state_dict().items()
              if ".bn." in name}
    assert len(frozen) == 61 * 5
    before = model.stem.conv.weight.detach().clone()
    optimizer = torch.optim.SGD((parameter for parameter in model.parameters()
                                 if parameter.requires_grad), lr=0.01)
    loss = model.stem(torch.randn(1, 3, 8, 8)).square().mean()
    loss.backward()
    assert model.stem.conv.weight.grad is not None
    assert torch.isfinite(model.stem.conv.weight.grad).all()
    optimizer.step()
    assert not torch.equal(before, model.stem.conv.weight)
    for name, expected in frozen.items():
        torch.testing.assert_close(model.state_dict()[name], expected, rtol=0, atol=0)


def _protocol_contract(manifest: Path, root: Path) -> None:
    legacy = _args(manifest, root / "legacy", freeze_bn=False)
    without_attribute = argparse.Namespace(**vars(legacy))
    del without_attribute.freeze_bn
    old = train.protocol_for(without_attribute, 2, None)
    default = train.protocol_for(legacy, 2, None)
    frozen = train.protocol_for(_args(manifest, root / "frozen"), 2, None)
    assert old == default
    assert train.protocol_hash(old) == train.protocol_hash(default)
    assert "batch_norm_policy" not in default
    assert frozen == dict(default,
                          batch_norm_policy="frozen_running_stats_and_affine_v1")


def _bn_state(checkpoint: dict) -> dict:
    return {key: value for key, value in checkpoint["model"].items()
            if key.startswith("bn.") or ".bn." in key}


def _transitions() -> list[tuple[bool, bool]]:
    return [mode for index, mode in enumerate(_TrackingTinyModel.modes)
            if index == 0 or mode != _TrackingTinyModel.modes[index - 1]]


def _trainer_resume(manifest: Path, root: Path) -> None:
    rows = [{"image": "tiny", "image_sha256": "0" * 64}]
    with (patch.object(train, "load_dataset_manifest", return_value=({}, rows)),
          patch.object(train, "make_frame_dataset",
                       side_effect=lambda _rows, split, *_a, **_kw: _TinyData(split)),
          patch.object(train, "RoadYOLOS4", _TrackingTinyModel),
          patch.object(train, "YOLOXLoss", _TinyLoss),
          patch.object(torch.cuda, "is_available", return_value=False),
          redirect_stdout(io.StringIO())):
        train.set_seed(42)
        initial = _TrackingTinyModel().state_dict()

        continuous_args = _args(manifest, root / "continuous")
        _TrackingTinyModel.modes.clear()
        assert train.train(continuous_args) == 0
        assert _transitions() == [
            (True, False), (False, False), (True, False), (False, False)]

        segmented_args = _args(manifest, root / "segmented", stop_after_epoch=1)
        _TrackingTinyModel.modes.clear()
        assert train.train(segmented_args) == 0
        paused = torch.load(segmented_args.output / "last_resume.pt",
                            map_location="cpu", weights_only=False)
        assert _transitions() == [
            (True, False), (False, False)]

        mismatched = _args(manifest, segmented_args.output, freeze_bn=False)
        mismatched.resume = segmented_args.output / "last_resume.pt"
        _TrackingTinyModel.modes.clear()
        try:
            train.train(mismatched)
        except ValueError as error:
            assert "protocol" in str(error)
        else:
            raise AssertionError("resume accepted a changed --freeze-bn policy")
        assert not _TrackingTinyModel.modes

        segmented_args.resume = segmented_args.output / "last_resume.pt"
        segmented_args.stop_after_epoch = 0
        _TrackingTinyModel.modes.clear()
        assert train.train(segmented_args) == 0
        assert _transitions() == [
            (True, False), (False, False)]

    continuous = torch.load(continuous_args.output / "last.pt",
                            map_location="cpu", weights_only=False)
    segmented = torch.load(segmented_args.output / "last.pt",
                           map_location="cpu", weights_only=False)
    for field in ("model", "optimizer", "scaler", "rng_state"):
        _same(continuous[field], segmented[field])
    for checkpoint in (paused, continuous, segmented):
        for key, value in _bn_state(checkpoint).items():
            torch.testing.assert_close(value, initial[key], rtol=0, atol=0)
        assert sum(len(group["params"]) for group in
                   checkpoint["optimizer"]["param_groups"]) == 1
    assert continuous["trained_steps"] == segmented["trained_steps"] == 4


def main() -> None:
    torch.set_num_threads(1)
    _real_model_policy()
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        manifest = root / "dataset.json"
        manifest.write_text("{}", encoding="utf-8")
        _protocol_contract(manifest, root)
        _trainer_resume(manifest, root)
    print("frozen BN policy, optimizer filtering and CPU resume checks PASS")


if __name__ == "__main__":
    main()
