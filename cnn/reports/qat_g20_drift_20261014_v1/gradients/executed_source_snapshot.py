"""Two-sample CPU gradient comparison for the rejected QAT continuation."""
from __future__ import annotations

import json
import math
import os
from pathlib import Path
import shutil

import numpy as np
import torch

from cnn import disk_cache
from cnn.disk_cache import ValidatedCacheBinding
from cnn.loss import YOLOXLoss
from cnn.model import RoadYOLOS4
from cnn.replay_sampling import ReplayWindow
from cnn.train import DatasetValidationSnapshot, dataset_content_hash, make_frame_dataset, sha256
from cnn.hw_validation.production.inspect_qat_gradients import norm_stats
from cnn.hw_validation.production.qat_exact import QATExactModel
from cnn.hw_validation.production import train_qat as base
from cnn.hw_validation.production import train_qat_frozen_stem_continue as continuation
from cnn.hw_validation.production import train_qat_numpy235 as runtime
from cnn.hw_validation.production.run_trained_integer import save

OUTPUT = base.PROJECT / "cnn/reports/qat_g20_drift_20261014_v1/gradients"
PARENT = continuation.PARENT
CANDIDATE = runtime.RUN / "last.pt"
PARENT_SHA256 = continuation.PARENT_SHA256
CANDIDATE_SHA256 = "36136fa83b37d4d8c4960d22fb5126e3326d984ffce0f4bd3136c24494bdb284"
RECEIPT = runtime.OUT / "cache_receipt.json"
RECEIPT_SHA256 = "6547202873389b09902beec19e674f862dbb3262754ce5ddaf26a4bb91006f76"


def _normalized_rows(payload):
    rows, scenes = [], {}
    for source in payload["images"]:
        row = dict(source)
        if row.get("split") not in ("train", "val") or row.get("preprocess", {}).get("raw_image") is not True:
            raise ValueError("expected only raw train/val development rows")
        previous = scenes.setdefault(row["scene_id"], row["split"])
        if previous != row["split"]:
            raise ValueError("scene leaks across train/val")
        row["boxes"] = [[float(value) for value in box] for box in row["boxes"]]
        row["ignore_boxes"] = [[float(value) for value in box] for box in row["ignore_boxes"]]
        row["image_path"] = Path(row["image"])
        row["image_sha256"] = row["source_sha256"]
        row["teacher_key"] = str(row.get("teacher_key", row["image"])).replace("\\", "/")
        rows.append(row)
    return rows


def training_inputs():
    if sha256(base.TRAIN) != base.TRAIN_HASH or sha256(RECEIPT) != RECEIPT_SHA256:
        raise ValueError("training manifest or reviewed cache receipt changed")
    payload = json.loads(base.TRAIN.read_text(encoding="utf-8"))
    rows = _normalized_rows(payload)
    counts = {split: sum(row["split"] == split for row in rows) for split in ("train", "val")}
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    root = Path(receipt["cache_root"]).resolve()
    encoded = (root / "index.json").read_bytes()
    index_sha = __import__("hashlib").sha256(encoded).hexdigest()
    metadata = json.loads(encoded)
    full_hash = dataset_content_hash(rows)
    entries = metadata.get("entries", [])
    if (counts != {"train": 86, "val": 17} or len(rows) != 103
            or receipt.get("split_counts") != counts or index_sha != receipt["cache_index_sha256"]
            or full_hash != receipt["dataset_content_sha256"]
            or metadata.get("dataset_sha256") != base.TRAIN_HASH
            or metadata.get("dataset_content_sha256") != full_hash
            or metadata.get("rgb_sha256") != receipt["rgb_sha256"]
            or metadata.get("preprocessing", {}).get("libraries", {}).get("numpy") != "2.4.6"
            or len(entries) != 103 or (root / "rgb.bin").stat().st_size != 103 * disk_cache.RECORD_BYTES):
        raise ValueError("reviewed 103-record cache binding changed")
    for row, entry in zip(rows, entries, strict=True):
        if (entry.get("image") != row["image"] or entry.get("source_sha256") != row["image_sha256"]
                or entry.get("row_sha256") != disk_cache.fingerprint(row)):
            raise ValueError("manifest row differs from reviewed cache index")
    snapshot = DatasetValidationSnapshot(base.TRAIN.resolve(), base.TRAIN_HASH, full_hash, rows)
    binding = ValidatedCacheBinding(snapshot, root, metadata, tuple(entries), index_sha)
    dataset = make_frame_dataset(rows, "train", base.TRAIN, mosaic=False,
        cache_root=root, cache_index_sha256=index_sha, cache_binding=binding)
    window = ReplayWindow(dataset, payload["replay_sampling"], 10)
    order = list(window.orders[0])
    selected = order[:2]
    groups = [dataset.rows[index]["sampling_group"] for index in selected]
    if len(dataset) != 86 or sorted(groups) != ["new", "replay"]:
        raise ValueError("order0 first microbatch is not one new plus one replay")
    return dataset, window, dict(manifest_sha256=base.TRAIN_HASH,
        full_103_content_sha256=full_hash,
        train_86_content_sha256=dataset_content_hash(dataset.rows), split_counts=counts,
        cache_receipt_sha256=RECEIPT_SHA256, cache_index_sha256=index_sha,
        cache_rgb_sha256=receipt["rgb_sha256"], selected_indices=selected, selected_groups=groups)


def parameter_group(layer_name, channel):
    if layer_name.endswith(".reg_out"):
        return "prediction_reg4" if channel < 4 else "prediction_obj1"
    if layer_name.endswith(".cls_out"):
        return "prediction_cls2"
    return "head_other" if layer_name.startswith("head") else "nonhead"


def weight_code_stats(weight, scale, gradient):
    step = scale.to(weight.dtype)[:, None, None, None]
    code = weight.detach() / step
    outside = (code < -128) | (code > 127)
    outward = outside & (((code > 127) & (gradient < 0)) | ((code < -128) & (gradient > 0)))
    torch_code = torch.round(code).clamp(-128, 127).to(torch.int8).cpu().numpy()
    numpy_code = np.clip(np.rint(weight.detach().double().cpu().numpy() /
        scale.detach().double().cpu().numpy()[:, None, None, None]), -128, 127).astype(np.int8)
    ratio = (gradient.abs() / step).flatten()
    return dict(elements=weight.numel(), outside_representable_interval=int(outside.sum()),
        rounded_code_out_of_range=int(((torch.round(code) < -128) | (torch.round(code) > 127)).sum()),
        outside_with_gradient_descent_outward=int(outward.sum()),
        torch_float32_vs_numpy_float64_encoded_difference=int(np.count_nonzero(torch_code != numpy_code)),
        gradient_over_quant_step=dict(median=float(ratio.median()),
            p90=float(torch.quantile(ratio, .9)), maximum=float(ratio.max())))


def inspect_case(label, state, folded, dataset, window):
    model = QATExactModel.from_package(base.BASE / "package", folded, base.BASE / "quantization.json").train()
    model.load_state_dict(state["model"], strict=True)
    stem = model.layers[model._layer_index["stem.conv"]]
    stem.weight.requires_grad_(False)
    stem.bias.requires_grad_(False)
    before = {name: value.detach().clone() for name, value in model.state_dict().items()}
    window.set_epoch(0, mosaic=False)
    samples = [window[index] for index in range(2)]
    images = torch.stack([sample[0] for sample in samples])
    targets = [sample[1] for sample in samples]
    losses = YOLOXLoss()(model(images), targets)
    if any(not torch.isfinite(value).all() for value in losses.values()):
        raise FloatingPointError("nonfinite loss")
    foreground = int(losses["num_foreground"].detach())
    numerator = losses["loss"] * max(foreground, 1)
    numerator.backward()
    trainable = [(name, parameter) for name, parameter in model.named_parameters() if parameter.requires_grad]
    if foreground <= 0 or any(p.grad is None or not torch.isfinite(p.grad).all() for _, p in trainable):
        raise FloatingPointError("missing foreground or gradient")
    for _, parameter in trainable:
        parameter.grad.div_(foreground)
    total_sq = sum(float((parameter.grad.double() ** 2).sum()) for _, parameter in trainable)
    global_l2 = math.sqrt(total_sq)
    clip_gain = min(1.0, 10.0 / global_l2)
    groups = {name: 0.0 for name in ("nonhead", "head_other", "prediction_reg4", "prediction_obj1", "prediction_cls2")}
    layers = []
    for name, index in model._layer_index.items():
        layer = model.layers[index]
        if not layer.weight.requires_grad:
            layers.append(dict(name=name, trainable=False,
                weight_codes=weight_code_stats(layer.weight, layer.weight_scale, torch.zeros_like(layer.weight))))
            continue
        weight_l2, weight_max, weight_sq = norm_stats(layer.weight.grad)
        bias_l2, bias_max, bias_sq = norm_stats(layer.bias.grad)
        for channel in range(layer.weight.shape[0]):
            group = parameter_group(name, channel)
            groups[group] += float((layer.weight.grad[channel].double() ** 2).sum())
            groups[group] += float(layer.bias.grad[channel].double() ** 2)
        layers.append(dict(name=name, trainable=True, weight_gradient_l2=weight_l2,
            weight_gradient_max_abs=weight_max, bias_gradient_l2=bias_l2,
            bias_gradient_max_abs=bias_max, squared_norm_share=(weight_sq + bias_sq) / total_sq,
            weight_codes=weight_code_stats(layer.weight, layer.weight_scale, layer.weight.grad)))
    if any(not torch.equal(value, model.state_dict()[name]) for name, value in before.items()):
        raise AssertionError("backward changed model state")
    return dict(label=label, checkpoint_trained_steps=state["trained_steps"],
        sample_keys=[sample[2] for sample in samples], foreground=foreground,
        loss_numerator=float(numerator.detach()), normalized_loss=float(numerator.detach()) / foreground,
        global_gradient_l2=global_l2, clip_gain=clip_gain,
        groups={name: dict(gradient_l2=math.sqrt(value), squared_norm_share=value / total_sq)
                for name, value in groups.items()}, layers=layers, finite_gradients=True,
        model_state_unchanged_after_backward=True)


def main():
    if os.environ.get("CUDA_VISIBLE_DEVICES") != "-1" or np.__version__ != "2.3.5":
        raise RuntimeError("set CUDA_VISIBLE_DEVICES=-1 and use the isolated NumPy 2.3.5 runtime")
    if os.environ.get("PYTORCH_NVML_BASED_CUDA_CHECK") != "1":
        raise RuntimeError("CPU diagnosis must avoid CUDA Runtime availability probing")
    if torch.cuda.is_available() or torch.cuda.is_initialized():
        raise RuntimeError("CUDA must remain hidden")
    torch.set_num_threads(2)
    torch.set_num_interop_threads(2)
    torch.use_deterministic_algorithms(True)
    OUTPUT.mkdir(parents=True, exist_ok=False)
    source = Path(__file__).resolve()
    test = source.with_name("test_inspect_qat_continuation_gradients.py")
    shutil.copyfile(source, OUTPUT / "executed_source_snapshot.py")
    source_hash = sha256(source)
    save(OUTPUT / "preflight.json", dict(source_sha256=source_hash,
        source_snapshot_sha256=sha256(OUTPUT / "executed_source_snapshot.py"),
        test_sha256=sha256(test), parent_checkpoint_sha256=sha256(PARENT),
        candidate_checkpoint_sha256=sha256(CANDIDATE), inference_started=False,
        optimizer_created=False, optimizer_step_called=False, gpu_used=False))
    if sha256(PARENT) != PARENT_SHA256 or sha256(CANDIDATE) != CANDIDATE_SHA256:
        raise ValueError("checkpoint changed")
    dataset, window, data = training_inputs()
    parent = torch.load(PARENT, map_location="cpu", weights_only=False)
    candidate = torch.load(CANDIDATE, map_location="cpu", weights_only=False)
    if (parent.get("trained_steps") != 10 or candidate.get("trained_steps") != 20
            or candidate.get("global_qat_updates") != 30
            or candidate.get("ancestry", {}).get("parent_checkpoint_sha256") != PARENT_SHA256
            or candidate.get("sample_history", [])[10].get("indices") != list(window.orders[0])
            or parent.get("sample_history", [])[0].get("indices") != list(window.orders[0])
            or candidate["model"]["layers.0.weight"].equal(parent["model"]["layers.0.weight"]) is not True
            or candidate["model"]["layers.0.bias"].equal(parent["model"]["layers.0.bias"]) is not True):
        raise ValueError("checkpoint cursor, ancestry, schedule, or frozen Stem differs")
    original = torch.load(base.CHECKPOINT, map_location="cpu", weights_only=False)
    fp32 = RoadYOLOS4().eval()
    fp32.load_state_dict(original["model"], strict=True)
    folded = fp32.folded_conv_state()
    cases = [inspect_case("parent_frozen_stem_G10", parent, folded, dataset, window),
             inspect_case("rejected_continuation_G20", candidate, folded, dataset, window)]
    if cases[0]["sample_keys"] != cases[1]["sample_keys"]:
        raise ValueError("cases consumed different samples")
    report = dict(schema="road-qat-g20-two-sample-gradient-diagnostic-v1",
        status="completed_limited_gradient_diagnostic_no_update", source_sha256=source_hash,
        checkpoints=dict(parent_sha256=PARENT_SHA256, candidate_sha256=CANDIDATE_SHA256),
        dataset=data, sample_keys=cases[0]["sample_keys"], cases=cases,
        comparison={name: dict(parent=cases[0]["groups"][name], candidate=cases[1]["groups"][name],
            squared_norm_share_delta=cases[1]["groups"][name]["squared_norm_share"] - cases[0]["groups"][name]["squared_norm_share"])
            for name in cases[0]["groups"]},
        device="cpu", cpu_threads=2, pytorch_nvml_based_cuda_check="1", gpu_used=False, optimizer_created=False,
        optimizer_step_called=False, checkpoint_files_unchanged=(sha256(PARENT) == PARENT_SHA256 and sha256(CANDIDATE) == CANDIDATE_SHA256),
        validation_pixels_read=0, validation_targets_used=False,
        validation_manifest_metadata_parsed_for_split_and_binding=True,
        limitation="One fixed two-image microbatch (one new, one replay), not the full 22-sample update gradient and not root-cause proof. Outward-gradient counts describe the unmasked STE surrogate only.")
    save(OUTPUT / "report.json", report)
    print(json.dumps(dict(output=str(OUTPUT), parent_l2=cases[0]["global_gradient_l2"],
        candidate_l2=cases[1]["global_gradient_l2"])), flush=True)


if __name__ == "__main__":
    main()
