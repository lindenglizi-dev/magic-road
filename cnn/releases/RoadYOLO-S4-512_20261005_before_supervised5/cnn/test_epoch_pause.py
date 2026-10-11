"""CPU-only real trainer save/pause/resume regression with a tiny test model."""
import json
from pathlib import Path
import tempfile
from unittest.mock import patch

import torch
from torch.utils.data import Dataset

from . import train


class TinyModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.layer = torch.nn.Linear(1, 1)

    def forward(self, images):
        return self.layer(images)

    def architecture_hash(self):
        return "tiny_pause_regression_only"


class TinyData(Dataset):
    def __init__(self, split):
        self.size = 65 if split == "train" else 2

    def __len__(self):
        return self.size

    def set_epoch(self, epoch, mosaic=None):
        assert mosaic is True  # Forty-epoch schedule keeps Mosaic in both tested epochs.

    def __getitem__(self, index):
        return torch.tensor([index / 100]), {}, str(index)


class TinyLoss:
    def __call__(self, outputs, targets):
        return {"loss": outputs.square().mean()}


def main():
    torch.set_num_threads(1)
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        manifest = root / "dataset.json"
        manifest.write_text("{}", encoding="utf-8")
        rows = [{"image": "tiny", "image_sha256": "0" * 64}]
        args = train.build_parser().parse_args([
            "--dataset", str(manifest), "--output", str(root / "run"),
            "--device", "cpu", "--workers", "0", "--epochs", "40",
            "--stop-after-epoch", "1"])
        with (patch.object(train, "load_dataset_manifest", return_value=({}, rows)),
              patch.object(train, "make_frame_dataset",
                           side_effect=lambda rows, split, *a, **kw: TinyData(split)),
              patch.object(train, "RoadYOLOS4", TinyModel),
              patch.object(train, "YOLOXLoss", TinyLoss),
              patch.object(torch.cuda, "is_available", return_value=False)):
            assert train.train(args) == 0
            first = torch.load(args.output / "last.pt", weights_only=False)
            train.ensure_resume_eligible(first, first["training_protocol"])
            assert first["epoch"] == 0 and first["trained_steps"] == 2
            assert first["resume_eligible"] and not first["interrupted"]
            assert first["last_optimizer_effective_batch"] == 1
            assert first["training_protocol"]["epochs"] == 40
            assert first["optimizer"]["param_groups"][0]["lr"] == .002
            assert not (args.output / "epoch_0001.pt").exists()
            events = [json.loads(line) for line in
                      (args.output / "train_log.jsonl").read_text().splitlines()]
            assert events[-1]["event"] == "paused_complete_epoch"
            original_hash = train.sha256(args.output / "epoch_0000.pt")
            args.resume = args.output / "last.pt"
            args.stop_after_epoch = 2
            assert train.train(args) == 0
            second = torch.load(args.resume, weights_only=False)
            train.ensure_resume_eligible(second, first["training_protocol"])
            assert second["epoch"] == 1 and second["trained_steps"] == 4
            assert second["training_protocol_sha256"] == first["training_protocol_sha256"]
            assert train.sha256(args.output / "epoch_0000.pt") == original_hash
            assert not (args.output / "epoch_0002.pt").exists()
            assert train.train(args) == 0  # completed_before_GPU is an idempotent success.
    print("complete epoch pause, tail batch, unchanged schedule and resume PASS")


if __name__ == "__main__":
    main()
