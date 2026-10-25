"""Prepare folded FP32 weights and training-only calibration ranges.

This is intentionally not an INT8 exporter or a deployable model package.
"""

from __future__ import annotations

import copy
import hashlib
import json
import platform
import sys
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path

import torch
from torch import Tensor, nn


OUTPUT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = OUTPUT_DIR.parents[3]
CHECKPOINT = PROJECT_ROOT / "cnn/runs/ac_replay_g10_20261013_v1/last.pt"
DATASET = PROJECT_ROOT / "cnn/reports/ac_optimization_20261013_v1/trial/dataset.json"
EXPECTED_CHECKPOINT_SHA256 = "e7e6a0f514b39417451ff90cec32e7f5adc862136bdf3adeac988c4d454fa262"
EXPECTED_DATASET_SHA256 = "5b25180c25d1f3835ea5248b107f19d2fc39cfac166500c45c87c2dfde08fd59"
EQUIVALENCE_IMAGES = 4
EQUIVALENCE_ATOL = 1e-3
EQUIVALENCE_RTOL = 1e-5
EQUIVALENCE_TOLERANCE_BASIS = (
    "fixed before the final run for 61 sequential FP32 Conv-BN folds; "
    "the first 1e-4 diagnostic was tighter than FP32 reassociation across the full graph"
)
FP64_FORMULA_ATOL = 1e-9
FP64_FORMULA_RTOL = 1e-10

sys.path.insert(0, str(PROJECT_ROOT))
from cnn.model import ConvBNAct, EXPECTED_CONV_COUNT, EXPECTED_SILU_COUNT, RoadYOLOS4
from cnn.train import load_dataset_snapshot, make_frame_dataset


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


class Range:
    """Streaming scalar range; hooks update now so in-place SiLU cannot alter it later."""

    def __init__(self) -> None:
        self.minimum = float("inf")
        self.maximum = float("-inf")
        self.values = 0
        self.tensors = 0
        self.nonfinite = 0

    def update(self, value: Tensor) -> None:
        value = value.detach()
        finite = torch.isfinite(value)
        bad = int((~finite).sum().item())
        self.nonfinite += bad
        self.values += value.numel()
        self.tensors += 1
        if bad:
            value = value[finite]
        if value.numel():
            low, high = torch.aminmax(value)
            self.minimum = min(self.minimum, float(low.item()))
            self.maximum = max(self.maximum, float(high.item()))

    def as_dict(self) -> dict[str, int | float]:
        if not self.values or self.minimum == float("inf"):
            raise RuntimeError("empty range")
        return {
            "min": self.minimum,
            "max": self.maximum,
            "max_abs": max(abs(self.minimum), abs(self.maximum)),
            "values": self.values,
            "tensors": self.tensors,
            "nonfinite": self.nonfinite,
        }


def folded_model(model: RoadYOLOS4, folded: OrderedDict[str, tuple[Tensor, Tensor]]) -> RoadYOLOS4:
    result = copy.deepcopy(model)
    replaced = 0
    for block_name, block in result.named_modules():
        if not isinstance(block, ConvBNAct):
            continue
        weight, bias = folded[f"{block_name}.conv"]
        conv = copy.deepcopy(block.conv)
        conv.weight = nn.Parameter(weight.clone())
        conv.bias = nn.Parameter(bias.clone())
        block.conv = conv
        block.bn = nn.Identity()
        replaced += 1
    if replaced != EXPECTED_SILU_COUNT:
        raise RuntimeError(f"replaced {replaced} ConvBNAct blocks, expected {EXPECTED_SILU_COUNT}")
    return result.eval()


def verify_equivalence(reference: RoadYOLOS4, folded: RoadYOLOS4, dataset) -> dict[str, object]:
    checks = []
    global_max_abs = 0.0
    global_max_rel = 0.0
    for image_index in range(EQUIVALENCE_IMAGES):
        image, _target, key = dataset[image_index]
        with torch.inference_mode():
            expected = reference(image.unsqueeze(0))
            actual = folded(image.unsqueeze(0))
        heads = []
        for head_index, (left, right) in enumerate(zip(expected, actual)):
            difference = (left - right).abs()
            max_abs = float(difference.max().item())
            max_rel = float((difference / left.abs().clamp_min(EQUIVALENCE_ATOL)).max().item())
            passed = bool(torch.allclose(left, right, atol=EQUIVALENCE_ATOL,
                                         rtol=EQUIVALENCE_RTOL))
            heads.append({"head_index": head_index, "max_abs": max_abs,
                          "max_relative_with_atol_floor": max_rel, "passed": passed})
            global_max_abs = max(global_max_abs, max_abs)
            global_max_rel = max(global_max_rel, max_rel)
            if not passed:
                raise AssertionError(
                    f"fold equivalence failed for train image {image_index}, head {head_index}: "
                    f"max_abs={max_abs}")
        checks.append({"train_index": image_index, "teacher_key": key, "heads": heads})
    return {
        "images": EQUIVALENCE_IMAGES,
        "atol": EQUIVALENCE_ATOL,
        "rtol": EQUIVALENCE_RTOL,
        "tolerance_basis": EQUIVALENCE_TOLERANCE_BASIS,
        "global_max_abs": global_max_abs,
        "global_max_relative_with_atol_floor": global_max_rel,
        "checks": checks,
        "passed": True,
    }


def verify_fp64_formula(reference: RoadYOLOS4, dataset) -> dict[str, object]:
    reference64 = copy.deepcopy(reference).double().eval()
    folded64 = folded_model(reference64, reference64.folded_conv_state())
    checks = []
    global_max_abs = 0.0
    for image_index in range(EQUIVALENCE_IMAGES):
        image, _target, key = dataset[image_index]
        with torch.inference_mode():
            expected = reference64(image.unsqueeze(0).double())
            actual = folded64(image.unsqueeze(0).double())
        heads = []
        for head_index, (left, right) in enumerate(zip(expected, actual)):
            max_abs = float((left - right).abs().max().item())
            passed = bool(torch.allclose(left, right, atol=FP64_FORMULA_ATOL,
                                         rtol=FP64_FORMULA_RTOL))
            heads.append({"head_index": head_index, "max_abs": max_abs, "passed": passed})
            global_max_abs = max(global_max_abs, max_abs)
            if not passed:
                raise AssertionError(
                    f"FP64 fold formula failed for train image {image_index}, head {head_index}: "
                    f"max_abs={max_abs}")
        checks.append({"train_index": image_index, "teacher_key": key, "heads": heads})
    return {
        "meaning": "source parameters converted to FP64, then folded again in FP64",
        "images": EQUIVALENCE_IMAGES,
        "atol": FP64_FORMULA_ATOL,
        "rtol": FP64_FORMULA_RTOL,
        "global_max_abs": global_max_abs,
        "checks": checks,
        "passed": True,
    }


def calibrate(model: RoadYOLOS4, dataset) -> dict[str, object]:
    conv_inputs = OrderedDict((name, Range()) for name, _conv in model.named_convs())
    activations = OrderedDict(
        (name, Range()) for name, module in model.named_modules() if isinstance(module, nn.SiLU))
    raw_heads = OrderedDict(
        (name, Range()) for name, module in model.named_modules()
        if isinstance(module, nn.Conv2d) and name.endswith(("cls_out", "reg_out")))
    if len(conv_inputs) != EXPECTED_CONV_COUNT or len(activations) != EXPECTED_SILU_COUNT:
        raise RuntimeError("unexpected model topology during calibration")
    if len(raw_heads) != 6:
        raise RuntimeError(f"found {len(raw_heads)} raw heads, expected 6")

    hooks = []
    for name, conv in model.named_convs():
        hooks.append(conv.register_forward_pre_hook(
            lambda _module, inputs, layer=name: conv_inputs[layer].update(inputs[0])))
        if name in raw_heads:
            hooks.append(conv.register_forward_hook(
                lambda _module, _inputs, output, layer=name: raw_heads[layer].update(output)))
    for name, module in model.named_modules():
        if name in activations:
            hooks.append(module.register_forward_hook(
                lambda _module, _inputs, output, layer=name: activations[layer].update(output)))
    try:
        with torch.inference_mode():
            for index in range(len(dataset)):
                image, _target, _key = dataset[index]
                model(image.unsqueeze(0))
    finally:
        for hook in hooks:
            hook.remove()

    payload = {
        "schema": 1,
        "meaning": "observed FP32 ranges on the folded model; not aligned INT8 scales",
        "forwarded_split": "train",
        "image_count": len(dataset),
        "conv_inputs": {name: value.as_dict() for name, value in conv_inputs.items()},
        "activation_outputs": {name: value.as_dict() for name, value in activations.items()},
        "raw_head_outputs": {name: value.as_dict() for name, value in raw_heads.items()},
    }
    nonfinite = sum(
        item["nonfinite"]
        for group in (payload["conv_inputs"], payload["activation_outputs"],
                      payload["raw_head_outputs"])
        for item in group.values())
    payload["all_finite"] = nonfinite == 0
    payload["nonfinite_observations"] = nonfinite
    if nonfinite:
        raise FloatingPointError(f"calibration observed {nonfinite} non-finite values")
    return payload


def main() -> None:
    torch.set_num_threads(2)
    torch.set_num_interop_threads(2)
    if torch.cuda.is_initialized():
        raise RuntimeError("CUDA was unexpectedly initialized")
    checkpoint_hash = sha256(CHECKPOINT)
    dataset_hash = sha256(DATASET)
    if checkpoint_hash != EXPECTED_CHECKPOINT_SHA256 or dataset_hash != EXPECTED_DATASET_SHA256:
        raise RuntimeError("input hash mismatch")

    manifest, snapshot = load_dataset_snapshot(DATASET)
    train_dataset = make_frame_dataset(snapshot.rows, "train", DATASET, mosaic=False)
    split_counts = {
        split: sum(row["split"] == split for row in snapshot.rows)
        for split in sorted({row["split"] for row in snapshot.rows})
    }
    if split_counts != {"train": 86, "val": 17} or len(train_dataset) != 86:
        raise RuntimeError(f"unexpected dataset split counts: {split_counts}")

    checkpoint = torch.load(CHECKPOINT, map_location="cpu", weights_only=False)
    reference = RoadYOLOS4().eval()
    if checkpoint["architecture_hash"] != reference.architecture_hash():
        raise RuntimeError("checkpoint architecture mismatch")
    reference.load_state_dict(checkpoint["model"], strict=True)
    folded = reference.folded_conv_state()
    if len(folded) != EXPECTED_CONV_COUNT:
        raise RuntimeError("folded state layer count mismatch")
    prepared = folded_model(reference, folded)

    equivalence = verify_equivalence(reference, prepared, train_dataset)
    fp64_formula = verify_fp64_formula(reference, train_dataset)
    ranges = calibrate(prepared, train_dataset)

    folded_path = OUTPUT_DIR / "folded_fp32_weights.pt"
    ranges_path = OUTPUT_DIR / "calibration_ranges.json"
    report_path = OUTPUT_DIR / "report.json"
    torch.save({
        "schema": 1,
        "kind": "RoadYOLO-S4-512 folded FP32 preparation weights; not model ROM",
        "architecture_hash": reference.architecture_hash(),
        "layers": OrderedDict(
            (name, {"weight": weight.cpu(), "bias": bias.cpu()})
            for name, (weight, bias) in folded.items()),
    }, folded_path)
    ranges_path.write_text(json.dumps(ranges, indent=2, ensure_ascii=False) + "\n",
                           encoding="utf-8")

    source_files = {
        "cnn/model.py": PROJECT_ROOT / "cnn/model.py",
        "cnn/train.py": PROJECT_ROOT / "cnn/train.py",
        "prepare_integer_assets.py": Path(__file__).resolve(),
    }
    train_inputs = [{
        "teacher_key": row["teacher_key"],
        "manifest_image": str(row["image"]).replace("\\", "/"),
        "image_sha256": row["image_sha256"],
    } for row in snapshot.rows if row["split"] == "train"]
    report = {
        "schema": 1,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "status": "passed_float_fold_and_training_only_range_calibration",
        "scope": "candidate integer preparation only; no QAT, INT8 deployment, ROM, or hardware run",
        "cpu_only": True,
        "torch_threads": torch.get_num_threads(),
        "torch_interop_threads": torch.get_num_interop_threads(),
        "cuda_initialized": torch.cuda.is_initialized(),
        "versions": {"python": platform.python_version(), "torch": torch.__version__},
        "inputs": {
            "checkpoint": str(CHECKPOINT.relative_to(PROJECT_ROOT)).replace("\\", "/"),
            "checkpoint_sha256": checkpoint_hash,
            "checkpoint_epoch_number": int(checkpoint["epoch"]) + 1,
            "checkpoint_trained_steps": int(checkpoint["trained_steps"]),
            "checkpoint_dataset_sha256": checkpoint["dataset_sha256"],
            "checkpoint_dataset_content_sha256": checkpoint["dataset_content_sha256"],
            "dataset_manifest": str(DATASET.relative_to(PROJECT_ROOT)).replace("\\", "/"),
            "dataset_manifest_sha256": dataset_hash,
            "dataset_content_sha256": snapshot.dataset_content_sha256,
            "split_counts": split_counts,
            "train_images": train_inputs,
        },
        "source_sha256": {name: sha256(path) for name, path in source_files.items()},
        "architecture_hash": reference.architecture_hash(),
        "folded_layer_count": len(folded),
        "folded_bias_values": sum(bias.numel() for _weight, bias in folded.values()),
        "equivalence": equivalence,
        "initial_fp32_diagnostic": {
            "atol": 1e-4,
            "rtol": 1e-5,
            "passed": False,
            "train_index": 0,
            "head_index": 0,
            "max_abs": 0.0002574920654296875,
            "boundary": "fail-fast stopped at the first failing head; this was not a four-image run",
        },
        "fp64_formula_equivalence": fp64_formula,
        "calibration": {
            "forwarded_split": ranges["forwarded_split"],
            "image_count": ranges["image_count"],
            "conv_input_ranges": len(ranges["conv_inputs"]),
            "activation_output_ranges": len(ranges["activation_outputs"]),
            "raw_head_output_ranges": len(ranges["raw_head_outputs"]),
            "all_finite": ranges["all_finite"],
            "inplace_silu_safety": "range extrema are reduced inside each hook; tensors are not retained",
        },
        "outputs": {
            "folded_weights": folded_path.name,
            "folded_weights_sha256": sha256(folded_path),
            "ranges": ranges_path.name,
            "ranges_sha256": sha256(ranges_path),
        },
        "not_completed": [
            "INT32 bias encoding and overflow proof",
            "concat and residual aligned-scale choice and validation",
            "pre- and post-requantization integer contract",
            "deployment-equivalent QAT and INT8 accuracy evaluation",
            "deployable model ROM or FPGA programming asset",
            "teacher evaluation, validation split inference, blind-test inference, and hardware run",
        ],
    }
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n",
                           encoding="utf-8")
    print(json.dumps({
        "status": report["status"],
        "equivalence_max_abs": equivalence["global_max_abs"],
        "calibration_images": ranges["image_count"],
        "all_finite": ranges["all_finite"],
        "report": str(report_path),
    }, indent=2))


if __name__ == "__main__":
    main()
