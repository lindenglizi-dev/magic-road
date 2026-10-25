"""CPU-only gradient evidence for the frozen-Stem QAT control."""
from __future__ import annotations

import json
import math
import os
from pathlib import Path
import sys

import torch

PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT))

from cnn.hw_validation.production.qat_exact import QATExactModel
from cnn.hw_validation.production.run_trained_integer import PROJECT, save
from cnn.hw_validation.production.train_qat import BASE, MICROBATCH, prepare
from cnn.loss import YOLOXLoss
from cnn.train import protocol_hash, set_seed, sha256


OUTPUT = PROJECT / "cnn/reports/qat_frozen_stem_g10_20261014_v1/gradient_inspection.json"


def norm_stats(gradient):
    value = gradient.detach().double()
    return float(torch.linalg.vector_norm(value)), float(value.abs().max()), float((value * value).sum())


def main():
    if os.environ.get("CUDA_VISIBLE_DEVICES") != "":
        raise ValueError("CUDA_VISIBLE_DEVICES must be empty")
    if OUTPUT.exists():
        raise FileExistsError(OUTPUT)
    torch.set_num_threads(2)
    torch.set_num_interop_threads(2)
    torch.use_deterministic_algorithms(True)
    set_seed(42)
    dataset, window, folded, identity, protocol = prepare()
    model = QATExactModel.from_package(BASE / "package", folded, BASE / "quantization.json").train()
    criterion = YOLOXLoss()
    window.set_epoch(0, mosaic=False)
    order = list(window.orders[0])
    if len(order) != 22 or MICROBATCH != 2:
        raise ValueError("frozen replay update-0 shape changed")

    records, actual_keys, loss_numerator, foreground = [], [], 0.0, 0
    model.zero_grad(set_to_none=True)
    for offset in range(0, 22, MICROBATCH):
        samples = [window[index] for index in range(offset, offset + MICROBATCH)]
        images = torch.stack([sample[0] for sample in samples])
        targets = [sample[1] for sample in samples]
        losses = criterion(model(images), targets)
        if any(not torch.isfinite(value).all() for value in losses.values()):
            raise FloatingPointError("nonfinite loss")
        count = int(losses["num_foreground"].detach())
        numerator = losses["loss"] * max(count, 1)
        numerator.backward()
        loss_numerator += float(numerator.detach())
        foreground += count
        for local, (_, target, key) in enumerate(samples):
            actual_keys.append(key)
            records.append({"dataset_index": order[offset + local], "key": key,
                            "labels": target["labels"].tolist()})
        print(json.dumps({"microbatch": offset // MICROBATCH + 1, "samples": offset + 2}), flush=True)
    expected_keys = [dataset.rows[index]["teacher_key"] for index in order]
    if actual_keys != expected_keys or foreground <= 0:
        raise ValueError("replay order/key or foreground count changed")
    for parameter in model.parameters():
        if parameter.grad is None or not torch.isfinite(parameter.grad).all():
            raise FloatingPointError("missing or nonfinite gradient")
        parameter.grad.div_(foreground)

    raw = []
    for name, index in model._layer_index.items():
        layer = model.layers[index]
        weight_l2, weight_max, weight_sq = norm_stats(layer.weight.grad)
        bias_l2, bias_max, bias_sq = norm_stats(layer.bias.grad)
        raw.append((name, layer, weight_l2, weight_max, weight_sq, bias_l2, bias_max, bias_sq))
    total_sq = sum(row[4] + row[7] for row in raw)
    global_norm = math.sqrt(total_sq)
    stem_sq = raw[0][4] + raw[0][7]
    without_stem_norm = math.sqrt(max(total_sq - stem_sq, 0.0))
    total_ratio = 10.0 / global_norm
    frozen_ratio = 10.0 / without_stem_norm
    total_gain, frozen_gain = min(1.0, total_ratio), min(1.0, frozen_ratio)

    layers = []
    for name, layer, weight_l2, weight_max, weight_sq, bias_l2, bias_max, bias_sq in raw:
        step = layer.weight_scale.float()[:, None, None, None]
        ratio = (layer.weight.grad.abs() / step).flatten()
        before = torch.round(layer.weight.detach() / step).clamp(-128, 127)
        current = torch.round((layer.weight.detach() - protocol["lr"] * total_gain * layer.weight.grad) /
                              step).clamp(-128, 127)
        frozen = before if name == raw[0][0] else torch.round(
            (layer.weight.detach() - protocol["lr"] * frozen_gain * layer.weight.grad) / step).clamp(-128, 127)
        layers.append({"name": name, "weight_gradient_l2": weight_l2,
            "weight_gradient_max_abs": weight_max, "bias_gradient_l2": bias_l2,
            "bias_gradient_max_abs": bias_max, "squared_norm": weight_sq + bias_sq,
            "squared_norm_share": (weight_sq + bias_sq) / total_sq,
            "gradient_over_weight_quant_step": {"median": float(ratio.median()),
                "p90": float(torch.quantile(ratio, .9)), "max": float(ratio.max())},
            "gradient_only_code_change_count_current_clip": int(torch.count_nonzero(current != before)),
            "gradient_only_code_change_count_frozen_stem_clip": int(torch.count_nonzero(frozen != before)),
            "weight_elements": layer.weight.numel()})

    report = {"schema_version": 1, "status": "passed_gradient_inspection_no_update",
        "purpose": "independent frozen-Stem G10 control preparation",
        "identity": identity, "protocol": protocol,
        "source_closure": {**identity["source_sha256"],
            "cnn/hw_validation/production/inspect_qat_gradients.py": sha256(Path(__file__))},
        "sample_order": order, "samples": records,
        "order_sha256": protocol_hash(order), "sample_keys_sha256": protocol_hash(actual_keys),
        "labels_sha256": protocol_hash([row["labels"] for row in records]),
        "loss": {"numerator": loss_numerator, "foreground": foreground,
                 "normalized": loss_numerator / foreground},
        "gradient": {"global_l2": global_norm, "stem_layer": raw[0][0],
            "stem_squared_norm_share": stem_sq / total_sq,
            "without_stem_l2": without_stem_norm,
            "clip_gain_ratio_10_over_total_norm": total_ratio,
            "clip_gain_ratio_10_over_without_stem_norm": frozen_ratio,
            "effective_total_clip_gain": total_gain, "effective_frozen_stem_clip_gain": frozen_gain},
        "layers": layers, "device": "cpu", "cpu_threads": 2, "gpu_used": False,
        "optimizer_created": False, "optimizer_updates": 0, "training_started": False,
        "backward_performed": True, "finite_gradients": True,
        "model_exported": False, "accuracy_measured": False,
        "code_change_limitation": "Gradient-only one-step susceptibility at protocol LR; omits momentum and weight decay and is not observed training.",
        "scope_limitation": "One fixed 22-sample train replay window; no validation, accuracy, model selection, or FPGA evidence."}
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    save(OUTPUT, report)
    print(json.dumps({"output": str(OUTPUT), "global_l2": global_norm,
                      "stem_share": stem_sq / total_sq}), flush=True)


if __name__ == "__main__":
    main()
