"""Evaluate the official FP32 teacher on the same raw val subset as the student.

Raw 1024x576 teacher heads map to 512x288 coordinates before the unchanged
Q7.8 decoder, Top-128 and max-32. This is development evidence, not FPGA FPS.
"""
import argparse
import json
from pathlib import Path
import time

import numpy as np
import torch

from .dataset import _refuse_blind
from .evaluate import load_validation_subset
from .integer import postprocess
from .metrics import evaluate, report, select_thresholds
from .teacher import (TEACHER_PREPROCESS, capture_raw_heads, json_hash,
                      load_official_model, teacher_input, tree_hash)
from .train import dataset_content_hash, sha256


def quantize_heads(outputs):
    """Match student evaluator's nearest-even Q7.8 head rounding and saturation."""
    return [np.clip(np.rint(output[0].permute(1, 2, 0).cpu().numpy() * 256),
                    -32768, 32767).astype(np.int16) for output in outputs]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-images", type=int, required=True)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--threads", type=int, default=4)
    parser.add_argument("--assets", type=Path, default=Path("cnn/teacher_assets"))
    args = parser.parse_args()
    if args.max_images <= 0 or args.threads <= 0:
        raise ValueError("positive development subset count and thread count required")
    if args.output.exists():
        raise FileExistsError(args.output)
    _refuse_blind(args.dataset)
    torch.set_num_threads(args.threads)
    started = time.perf_counter()
    rows, total = load_validation_subset(args.dataset, None, args.max_images)
    for row in rows:
        _refuse_blind(row["image_path"])
    source = args.assets / "source/YOLOX-0.3.0"
    weights = args.assets / "yolox_s.pth"
    receipt = json.loads((args.assets / "receipt.json").read_text(encoding="utf-8"))
    weight_sha, source_sha = sha256(weights), tree_hash(source / "yolox")
    if (weight_sha != receipt["weights"]["sha256"]
            or source_sha != receipt["source_tree_sha256"]):
        raise ValueError("official teacher asset receipt mismatch")
    device = torch.device(args.device)
    model = load_official_model(source, weights, device)
    predictions, truth, ignores = [], [], []
    for index, row in enumerate(rows):
        outputs = capture_raw_heads(model, teacher_input(row, device))
        for detection in postprocess(quantize_heads(outputs), (3276, 3276)):
            predictions.append(dict(image_id=row["image"], label=detection["label"],
                                    box=[v / 256 for v in detection["box_q8"]],
                                    score=detection["score_uint16"] / 65536))
        truth.extend(dict(image_id=row["image"], label=label, box=box)
                     for label, box in zip(row["labels"], row["boxes"], strict=True))
        metadata = row.get("ignore_metadata",
                           [{"label": -1, "crowd": False}] * len(row["ignore_boxes"]))
        ignores.extend(dict(image_id=row["image"], label=item["label"], box=box,
                            crowd=item["crowd"])
                       for box, item in zip(row["ignore_boxes"], metadata, strict=True))
        if index == 0 or (index + 1) % 32 == 0 or index + 1 == len(rows):
            print(f"teacher validation {index + 1}/{len(rows)}", flush=True)
    thresholds = select_thresholds(predictions, truth, ignores)
    diagnostic = report(predictions, truth, ignores, thresholds=(.5, .5))
    result = dict(
        status="teacher_development_diagnostic_not_formal_acceptance",
        inference="official_FP32_YOLOX_S_1024x576_heads_mapped_to_student_512x288",
        teacher_weight_sha256=weight_sha, teacher_source_sha256=source_sha,
        teacher_preprocess=TEACHER_PREPROCESS,
        teacher_preprocess_sha256=json_hash(TEACHER_PREPROCESS),
        dataset_sha256=sha256(args.dataset),
        evaluated_image_content_sha256=dataset_content_hash(rows),
        image_count=len(rows), total_validation_images=total, split="val",
        subset_selection="same_evenly_spaced_sorted_image_names_as_student",
        postprocess_contract=dict(top_k_per_class=128, max_boxes_per_class=32,
                                  nms_iou=.5, score_floor_uint16=3276),
        validation_thresholds=thresholds, diagnostic_metrics_at_0_5=diagnostic,
        baseline_at_0_5={name: evaluate(predictions, truth, ignores, label=label,
                                      threshold=.5)
                         for label, name in enumerate(("person", "vehicle"))},
        p95_operating_points={name: (evaluate(predictions, truth, ignores,
                                             label=label, threshold=thresholds[label])
                                    if thresholds[label] is not None else None)
                              for label, name in enumerate(("person", "vehicle"))},
        predictions=predictions, truth=truth, ignores=ignores,
        total_seconds=time.perf_counter() - started, device=str(device),
        acceptance_eligible=False,
        limitation="Teacher has higher input resolution and model capacity; not a resolution-matched ablation, INT8 CNN, COCOeval, clustered CI, or FPGA throughput measurement.")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
    print(json.dumps(dict(status=result["status"], image_count=len(rows),
                          metrics=diagnostic, seconds=result["total_seconds"])))


if __name__ == "__main__":
    main()
