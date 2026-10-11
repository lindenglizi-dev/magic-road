"""Narrow executable checks for the floating RoadYOLO training reference.

These checks prove architecture and numerical plumbing only.  Synthetic loss
or CUDA execution is not accuracy, quantization, or hardware evidence.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from unittest.mock import patch

import numpy as np
import torch

try:
    from .integer import silu as integer_silu
    from .loss import TW_TH_MAX, TW_TH_MIN, YOLOXLoss, decode_outputs
    from .model import RoadSiLUQAT, RoadYOLOS4, assert_frozen_contract, model_statistics
    from .train import (FullFrameDataset, accumulation_group_samples, build_parser,
                        dataset_content_hash, ensure_resume_eligible,
                        load_dataset_manifest, sha256 as train_sha256, train)
except ImportError:  # python cnn/test_model.py
    from integer import silu as integer_silu
    from loss import TW_TH_MAX, TW_TH_MIN, YOLOXLoss, decode_outputs
    from model import RoadSiLUQAT, RoadYOLOS4, assert_frozen_contract, model_statistics
    from train import (FullFrameDataset, accumulation_group_samples, build_parser,
                       dataset_content_hash, ensure_resume_eligible,
                       load_dataset_manifest, sha256 as train_sha256, train)


ROOT = Path(__file__).resolve().parent
DEFAULT_DATASET = ROOT / "data" / "coco_pretrain" / "dataset.json"


def target(index: int = 0) -> dict[str, torch.Tensor]:
    shift = float(index % 8)
    return {
        "boxes": torch.tensor([[80.0 + shift, 48.0, 152.0 + shift, 224.0],
                               [280.0, 112.0, 416.0, 248.0]]),
        "labels": torch.tensor([0, 1]),
        "ignore_boxes": torch.tensor([[0.0, 0.0, 32.0, 32.0]]),
    }


def check_contract(device: torch.device) -> tuple[RoadYOLOS4, dict[str, object]]:
    model = RoadYOLOS4().to(device)
    stats = model_statistics(model, device)
    assert_frozen_contract(stats)
    folded = model.folded_conv_state()
    assert len(folded) == 67
    assert sum(weight.numel() for weight, _bias in folded.values()) == 113_100
    assert sum(bias.numel() for _weight, bias in folded.values()) == 2_501
    return model, stats


def check_numeric_contract() -> None:
    q8 = np.array([-32768, -2048, -2047, -2, 0, 2, 2047, 2048, 32767],
                  dtype=np.int16)
    actual = torch.round(RoadSiLUQAT()(torch.from_numpy(q8.astype(np.float32)) / 256.0)
                         * 256.0).to(torch.int16).numpy()
    np.testing.assert_array_equal(actual, integer_silu(q8))

    heads = [torch.zeros(1, 7, 72, 128), torch.zeros(1, 7, 36, 64),
             torch.zeros(1, 7, 18, 32)]
    heads[0][0, 2, 0, 0] = -100.0
    heads[0][0, 3, 0, 0] = 100.0
    boxes, *_ = decode_outputs(heads)
    width_height = boxes[0, 0, 2:] - boxes[0, 0, :2]
    expected = torch.exp(torch.tensor([TW_TH_MIN, TW_TH_MAX])) * 4.0
    torch.testing.assert_close(width_height, expected)

    # A degenerate annotation makes the full frame unknown background, not a
    # negative image. Explicit valid GT must still receive positive supervision.
    criterion = YOLOXLoss()
    with torch.no_grad():
        unknown = {"boxes": torch.empty(0, 4), "labels": torch.empty(0, dtype=torch.long),
                   "ignore_boxes": torch.tensor([[0.0, 0.0, 512.0, 288.0]])}
        ignored = criterion(heads, [unknown])
        assert ignored['object_loss'].item() == 0
        regular = target()
        baseline = criterion(heads, [regular])
        regular['ignore_boxes'] = unknown['ignore_boxes']
        protected = criterion(heads, [regular])
        assert protected['num_foreground'].item() > 0
        for field in ('num_foreground', 'iou_loss', 'class_loss'):
            torch.testing.assert_close(protected[field], baseline[field])
        assert protected['object_loss'].item() < baseline['object_loss'].item()


def check_manifest(path: Path) -> dict[str, int]:
    hash_target = f'{load_dataset_manifest.__module__}.sha256'
    with patch(hash_target, wraps=train_sha256) as hash_calls:
        payload, rows = load_dataset_manifest(path)
        assert hash_calls.call_count == len(rows)
    if any(row.get('preprocess', {}).get('raw_image') is True for row in rows):
        with patch(hash_target, return_value='0' * 64):
            try:
                load_dataset_manifest(path)
            except ValueError as error:
                assert 'source hash' in str(error)
            else:
                raise AssertionError('raw image content mismatch was accepted')
    train_data = FullFrameDataset(rows, "train")
    val_data = FullFrameDataset(rows, "val")
    image, item_target, _key = train_data[0]
    assert image.shape == (3, 288, 512) and image.dtype == torch.float32
    assert item_target["boxes"].shape[1:] == (4,)
    assert payload["classes"] == ["person", "vehicle"]
    content_hash = dataset_content_hash(rows)
    assert len(content_hash) == 64 and dataset_content_hash(list(reversed(rows))) == content_hash
    changed = [dict(row) for row in rows]
    changed[0]["image_sha256"] = "0" * 64
    assert dataset_content_hash(changed) != content_hash
    return {"train_images": len(train_data), "val_images": len(val_data)}


def check_backward(model: RoadYOLOS4, device: torch.device) -> float:
    model.train()
    model.zero_grad(set_to_none=True)
    images = torch.randn(1, 3, 288, 512, device=device)
    result = YOLOXLoss()(model(images), [target()])
    result["loss"].backward()
    gradients = [parameter.grad for parameter in model.parameters()
                 if parameter.grad is not None]
    assert gradients and all(torch.isfinite(gradient).all() for gradient in gradients)
    assert any(torch.count_nonzero(gradient).item() for gradient in gradients)
    return float(result["loss"].detach())


def check_qat_fails_closed() -> None:
    try:
        train(argparse.Namespace(phase="qat"))
    except ValueError as error:
        assert "QAT blocked" in str(error)
    else:
        raise AssertionError("QAT phase must fail closed")


def cuda_accumulation_smoke() -> dict[str, float | int | str]:
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA accumulation smoke requested but CUDA is unavailable")
    device = torch.device("cuda")
    torch.cuda.empty_cache()
    torch.cuda.reset_peak_memory_stats(device)
    model = RoadYOLOS4().to(device).train()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.9,
                                weight_decay=5e-4)
    scaler = torch.amp.GradScaler("cuda", enabled=True)
    criterion = YOLOXLoss()
    images = torch.zeros(8, 3, 288, 512, device=device)
    targets = [target(index) for index in range(8)]
    optimizer.zero_grad(set_to_none=True)
    last_loss = 0.0
    for _microstep in range(8):
        with torch.amp.autocast(device_type="cuda", enabled=True):
            result = criterion(model(images), targets)
            loss = result["loss"] / 8
        scaler.scale(loss).backward()
        last_loss = float(result["loss"].detach())
    scaler.unscale_(optimizer)
    torch.nn.utils.clip_grad_norm_(model.parameters(), 10.0)
    scaler.step(optimizer)
    scaler.update()
    torch.cuda.synchronize(device)
    return {
        "device": torch.cuda.get_device_name(device),
        "microbatch": 8,
        "accum_steps": 8,
        "effective_batch": 64,
        "last_synthetic_loss": last_loss,
        "peak_allocated_mib": round(torch.cuda.max_memory_allocated(device) / 2**20, 2),
        "peak_reserved_mib": round(torch.cuda.max_memory_reserved(device) / 2**20, 2),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--skip-cuda-accum-smoke", action="store_true")
    args = parser.parse_args()

    defaults = build_parser().parse_args(["--dataset", "dataset.json", "--output", "out"])
    assert (defaults.batch_size, defaults.accum_steps, defaults.seed, defaults.mosaic) == (
        8, 8, 42, True)
    assert [accumulation_group_samples(step, 12, 8, 8, 96)
            for step in range(12)] == [64] * 8 + [32] * 4
    tail_samples = [8, 8, 8, 8, 1]
    assert accumulation_group_samples(12, 13, 8, 8, 97) == 33
    assert abs(sum(samples / 33 for samples in tail_samples) - 1.0) < 1e-12
    try:
        ensure_resume_eligible({"interrupted": True})
    except ValueError as error:
        assert "cannot be resumed exactly" in str(error)
    else:
        raise AssertionError("mid-epoch resume must fail closed")
    check_qat_fails_closed()
    check_numeric_contract()
    dataset_counts = check_manifest(args.dataset.resolve())
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model, stats = check_contract(device)
    backward_loss = check_backward(model, device)
    cuda = None if args.skip_cuda_accum_smoke else cuda_accumulation_smoke()
    print(json.dumps({
        "status": "passed_synthetic_only_no_accuracy_evidence",
        "architecture": stats,
        "dataset": dataset_counts,
        "single_sample_backward_loss": backward_loss,
        "cuda_accumulation": cuda,
        "qat": "experimental_qat_not_deployment_equivalent_and_cli_blocked",
        "training_protocol": "formal_sgd_warmup_cosine_mosaic_v1",
    }, indent=2))


if __name__ == "__main__":
    main()
