"""Exact segmented trainer resume checks; GPU parity is opt-in."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import tempfile
from unittest.mock import patch

import numpy as np
import torch
from torch.utils.data import DataLoader, Dataset

from . import train
from .resume_state import load_latest_resume, save_resume_state


class TinyModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.conv = torch.nn.Conv2d(1, 2, 1, bias=False)
        self.bn = torch.nn.BatchNorm2d(2)
        self.dropout = torch.nn.Dropout(0.25)

    def forward(self, images):
        return self.dropout(self.bn(self.conv(images)))

    def architecture_hash(self):
        return "tiny_segment_resume_v3"


class TinyData(Dataset):
    accesses: list[tuple[str, int]] = []

    def __init__(self, split):
        self.split = split
        self.size = 65 if split == "train" else 5

    def __len__(self):
        return self.size

    def set_epoch(self, epoch, mosaic=None):
        assert mosaic is True

    def __getitem__(self, index):
        self.accesses.append((self.split, index))
        return torch.full((1, 2, 2), (index + 1) / 100.0), {}, str(index)


class TinyLoss:
    pause_path: Path | None = None
    pause_call = 0
    fail_call = 0

    def __init__(self):
        self.calls = 0

    def __call__(self, outputs, targets):
        self.calls += 1
        if self.pause_path is not None and self.calls == self.pause_call:
            self.pause_path.write_text("pause", encoding="ascii")
        if self.fail_call and self.calls == self.fail_call:
            raise RuntimeError("injected group failure")
        return {"loss": outputs.square().mean()}


class IndexData(Dataset):
    def __init__(self, size):
        self.size = size

    def __len__(self):
        return self.size

    def __getitem__(self, index):
        return index


def _args(manifest: Path, output: Path, device: str) -> argparse.Namespace:
    return train.build_parser().parse_args([
        "--dataset", str(manifest), "--output", str(output),
        "--device", device, "--workers", "0", "--epochs", "40",
        "--stop-after-epoch", "1", "--checkpoint-every-steps", "1",
        "--checkpoint-every-seconds", "0"])


def _same(left, right):
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


def _run_equivalence(root: Path, manifest: Path, device: str) -> None:
    baseline_args = _args(manifest, root / f"baseline_{device}", device)
    assert train.train(baseline_args) == 0
    baseline = torch.load(baseline_args.output / "last.pt", map_location="cpu",
                          weights_only=False)

    segmented_args = _args(manifest, root / f"segmented_{device}", device)
    pause = root / f"pause_{device}.request"
    segmented_args.pause_request = pause
    TinyLoss.pause_path, TinyLoss.pause_call = pause, 1
    assert train.train(segmented_args) == 0
    first, _ = load_latest_resume(segmented_args.output)
    assert first["stage"] == "train" and first["next_sample_cursor"] == 64
    assert first["last_optimizer_effective_batch"] == 64

    pause.unlink()
    segmented_args.resume = segmented_args.output / "last_resume.pt"
    TinyLoss.pause_call = 2  # Tail training batch, then the validation batch.
    assert train.train(segmented_args) == 0
    during_val, _ = load_latest_resume(segmented_args.output)
    assert during_val["stage"] == "val"
    assert during_val["val_next_batch"] == 1 and during_val["val_samples"] == 5
    # Emulate a hard kill after epoch_0000.pt, before last.pt/epoch_done.
    saved_model = TinyModel()
    saved_model.load_state_dict(during_val["model"])
    saved_optimizer = torch.optim.SGD(saved_model.parameters(), lr=segmented_args.lr,
                                      momentum=segmented_args.momentum,
                                      weight_decay=segmented_args.weight_decay)
    saved_optimizer.load_state_dict(during_val["optimizer"])
    saved_scaler = torch.amp.GradScaler("cuda", enabled=bool(
        during_val["training_protocol"]["amp"]))
    saved_scaler.load_state_dict(during_val["scaler"])
    _same(saved_scaler.state_dict(), during_val["scaler"])
    metric = {
        "name": "validation_loss_stub",
        "value": during_val["val_loss_sum"] / during_val["val_samples"],
        "status": "unaccepted_no_AP_precision_or_recall",
        "train_loss": during_val["epoch_loss_sum"] / during_val["epoch_samples"],
    }
    train.save_checkpoint(
        segmented_args.output / "epoch_0000.pt", model=saved_model,
        optimizer=saved_optimizer, scaler=saved_scaler, epoch=0,
        trained_steps=during_val["trained_steps"], phase=segmented_args.phase,
        checkpoint_kind=segmented_args.checkpoint_kind,
        dataset_hash=during_val["dataset_sha256"],
        dataset_content_sha256=during_val["dataset_content_sha256"],
        effective_batch=during_val["effective_batch"],
        last_optimizer_effective_batch=during_val["last_optimizer_effective_batch"],
        metric=metric, training_protocol=during_val["training_protocol"])

    pause.unlink()
    TinyLoss.pause_path = None
    TinyData.accesses.clear()
    assert train.train(segmented_args) == 0
    assert not TinyData.accesses  # Completed validation cursor reads nothing twice.
    segmented = torch.load(segmented_args.output / "last.pt", map_location="cpu",
                           weights_only=False)
    for field in ("model", "optimizer", "scaler", "rng_state"):
        _same(baseline[field], segmented[field])
    assert segmented["last_optimizer_effective_batch"] == 1


def _group_failure_keeps_latest(root: Path, manifest: Path) -> None:
    args = _args(manifest, root / "fault_run", "cpu")
    pause = root / "fault_pause.request"
    args.pause_request = pause
    TinyLoss.pause_path, TinyLoss.pause_call, TinyLoss.fail_call = pause, 1, 0
    assert train.train(args) == 0
    before = train.sha256(args.output / "last_resume.pt")
    pause.unlink()
    args.resume = args.output / "last_resume.pt"
    TinyLoss.pause_path, TinyLoss.fail_call = None, 1
    try:
        train.train(args)
    except RuntimeError as error:
        assert "injected group failure" in str(error)
    else:
        raise AssertionError("injected mid-group failure did not propagate")
    assert train.sha256(args.output / "last_resume.pt") == before
    TinyLoss.fail_call = 0


def _slot_fault_injection(root: Path, source_output: Path) -> None:
    state, _ = load_latest_resume(source_output)
    inside_group = dict(state, stage="train", next_microbatch=1,
                        next_sample_cursor=8, epoch_samples=8, trained_steps=1,
                        val_next_batch=0, val_samples=0, val_loss_sum=0.0)
    try:
        train._validate_v3_cursors(
            inside_group, train_size=65, val_size=5, batch_size=8,
            accum_steps=8, optimizer_steps_per_epoch=2, seed=42)
    except ValueError as error:
        assert "accumulation group" in str(error)
    else:
        raise AssertionError("mid-accumulation resume cursor was accepted")
    for rejected in (dict(state, checkpoint_kind="diagnostic"),
                     dict(state, interrupted=True)):
        try:
            train.ensure_resume_eligible(rejected)
        except ValueError:
            pass
        else:
            raise AssertionError("diagnostic/interrupted v3 state was accepted")
    output = root / "slots"
    save_resume_state(output, state)
    changed = dict(state, last_lr=state["last_lr"] + 1.0)
    save_resume_state(output, changed)
    (output / "last_resume.pt").write_bytes(b"corrupt latest")

    def fail_latest(source, destination):
        if Path(destination).name == "last_resume.pt":
            raise OSError("injected replace failure")
        os.replace(source, destination)

    try:
        save_resume_state(output, dict(state, last_lr=2.0), replace=fail_latest)
    except OSError as error:
        assert "injected" in str(error)
    else:
        raise AssertionError("replace fault was not injected")
    recovered, recovered_path = load_latest_resume(output)
    assert recovered_path.name == "last_resume.prev.pt"
    _same(recovered, state)


def _legacy_order() -> None:
    for size in (65, 19050):
        generator = torch.Generator().manual_seed(42)
        actual = [int(index) for batch in DataLoader(
            IndexData(size), batch_size=8, shuffle=True, generator=generator,
            num_workers=0) for index in batch]
        assert actual == train.epoch_order(size, 42, 0)
    assert train.accumulation_group_samples(2376, 2382, 8, 8, 19050) == 42
    assert train.accumulation_group_samples(8, 9, 8, 8, 65) == 1


def _publish_report(path: Path) -> None:
    if path.exists():
        raise FileExistsError(f"parity report already exists: {path}")
    payload = {
        "status": "passed_GPU_AMP_segment_resume_equivalence",
        "device": "cuda", "amp": True,
        "maximum_compared_difference": 0,
        "model_and_BN_max_abs_diff": 0,
        "SGD_state_max_abs_diff": 0,
        "AMP_scaler_state_diff": 0,
        "RNG_state_diff": 0,
        "test_source_sha256": {
            "train.py": train.sha256(Path(train.__file__)),
            "resume_state.py": train.sha256(Path(__file__).with_name("resume_state.py")),
            "test_segment_resume.py": train.sha256(Path(__file__)),
        },
        "limitation": ("tiny model with 65-train/5-val synthetic data; not a full "
                       "RoadYOLO model comparison and no accuracy evidence"),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("x", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gpu-parity", action="store_true")
    parser.add_argument("--supervised-start", action="store_true")
    parser.add_argument("--output", type=Path)
    options = parser.parse_args()
    if options.output is not None and not options.gpu_parity:
        raise ValueError("--output is only valid with --gpu-parity")
    if options.gpu_parity and options.output is None:
        raise ValueError("--gpu-parity requires --output")
    torch.set_num_threads(1)
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        manifest = root / "dataset.json"
        manifest.write_text("{}", encoding="utf-8")
        rows = [{"image": "tiny", "image_sha256": "0" * 64}]
        with (patch.object(train, "load_dataset_manifest", return_value=({}, rows)),
              patch.object(train, "make_frame_dataset",
                           side_effect=lambda rows, split, *a, **kw: TinyData(split)),
              patch.object(train, "RoadYOLOS4", TinyModel),
              patch.object(train, "YOLOXLoss", TinyLoss),
              patch.object(torch.cuda, "is_available", return_value=False)):
            _run_equivalence(root, manifest, "cpu")
            _group_failure_keeps_latest(root, manifest)
            _slot_fault_injection(root, root / "segmented_cpu")
        _legacy_order()
        if options.gpu_parity:
            if options.supervised_start:
                print(json.dumps({"event": "preflight_ready", "trainer_pid": os.getpid()}),
                      flush=True)
                if input().strip() != "GO":
                    raise RuntimeError("supervised parity requires GO on stdin")
            if not torch.cuda.is_available():
                raise RuntimeError("--gpu-parity requires CUDA")
            with (patch.object(train, "load_dataset_manifest", return_value=({}, rows)),
                  patch.object(train, "make_frame_dataset",
                               side_effect=lambda rows, split, *a, **kw: TinyData(split)),
                  patch.object(train, "RoadYOLOS4", TinyModel),
                  patch.object(train, "YOLOXLoss", TinyLoss)):
                _run_equivalence(root, manifest, "cuda")
            _publish_report(options.output.resolve())
            print(json.dumps({"event": "parity_passed",
                              "report": str(options.output.resolve())}), flush=True)
    print("v3 train/val segmented resume, BN/RNG, tails, atomic fallback PASS")


if __name__ == "__main__":
    main()
