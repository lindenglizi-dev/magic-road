"""Bounded CPU diagnostic of native versus actual Mosaic SimOTA assignment."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime
import hashlib
import json
from pathlib import Path
import platform
import random
import time

import numpy as np
import torch
from torch import Tensor, nn

from .loss import _candidate_mask, decode_outputs, pairwise_iou, simota_assign
from .model import INPUT_HEIGHT, INPUT_WIDTH, NUM_CLASSES, RoadYOLOS4
from .train import CLASS_CONTRACT, FullFrameDataset, sha256


ROOT = Path(__file__).resolve().parent.parent
CHECKPOINT = ROOT / "cnn/runs/road40_from_coco6_segmented_20261003/epoch_0019.pt"
MANIFEST = ROOT / "cnn/data/visdrone_vid_train/raw_manifest/dataset.json"
OUTPUT = ROOT / "cnn/reports/person_assignment_probe_20261004.json"
CHECKPOINT_SHA256 = "61edd64aa14409e5d8df9aeed7e519440e41ead353e551134b774bcc038bf94c"
MANIFEST_SHA256 = "ad353c5bce5b0ecef0433c74515324bbfdb031e92aff964cd56c18ae069d9fe4"
SEED = 42
EPOCH = 19
MAX_GROUPS = 16
TIME_LIMIT_SECONDS = 300.0


def _mosaic_indices(index: int, size: int) -> list[int]:
    generator = random.Random((SEED << 40) ^ (EPOCH << 20) ^ index)
    return [index] + [generator.randrange(size) for _ in range(3)]


def _tensor_summary(values: list[float]) -> dict[str, float | int | None]:
    if not values:
        return {"count": 0, "mean": None, "median": None, "min": None, "max": None}
    array = np.asarray(values, dtype=np.float64)
    return {
        "count": len(values), "mean": float(array.mean()),
        "median": float(np.median(array)), "min": float(array.min()),
        "max": float(array.max()),
    }


def _box_size_summary(boxes: list[list[float]]) -> dict[str, dict[str, float | int | None]]:
    if not boxes:
        return {name: _tensor_summary([]) for name in ("width", "height", "area")}
    array = np.asarray(boxes, dtype=np.float64)
    width, height = array[:, 2] - array[:, 0], array[:, 3] - array[:, 1]
    return {
        "width": _tensor_summary(width.tolist()),
        "height": _tensor_summary(height.tolist()),
        "area": _tensor_summary((width * height).tolist()),
    }


def _bn_digest(model: nn.Module) -> str:
    digest = hashlib.sha256()
    for name, module in model.named_modules():
        if isinstance(module, nn.BatchNorm2d):
            digest.update(name.encode("utf-8"))
            for tensor in (module.running_mean, module.running_var, module.num_batches_tracked):
                digest.update(tensor.detach().cpu().contiguous().numpy().tobytes())
    return digest.hexdigest()


def _toy_conflict_check() -> dict[str, int]:
    boxes = torch.tensor([[0.0, 0.0, 10.0, 10.0]])
    objects = torch.zeros(1)
    classes = torch.zeros(1, NUM_CLASSES)
    centers = torch.tensor([[5.0, 5.0]])
    strides = torch.tensor([4.0])
    gt_boxes = boxes.repeat(2, 1)
    gt_labels = torch.zeros(2, dtype=torch.long)
    foreground, matched_gt, matched_iou = simota_assign(
        boxes, objects, classes, centers, strides, gt_boxes, gt_labels)
    assert int(foreground.sum()) == 1
    assert matched_gt.tolist() == [0]
    torch.testing.assert_close(matched_iou, torch.ones(1))
    return {"gt": 2, "pre_conflict_claims": 2, "post_conflict_foreground": 1,
            "post_conflict_matched_gt": 1}


def _normalized_train_rows(payload: dict, manifest: Path) -> list[dict]:
    assert payload.get("classes") == list(CLASS_CONTRACT.values())
    assert payload.get("training_eligible") is True
    assert payload.get("input_size") == [INPUT_WIDTH, INPUT_HEIGHT]
    rows = []
    for source in payload["images"]:
        if source["split"] != "train":
            continue
        row = dict(source)
        image = Path(row["image"])
        row["image_path"] = image if image.is_absolute() else manifest.parent / image
        row["teacher_key"] = str(row.get("teacher_key", row["image"])).replace("\\", "/")
        rows.append(row)
    assert rows
    return rows


def _assert_mosaic_geometry(native_targets: list[dict[str, Tensor]],
                            mosaic_target: dict[str, Tensor]) -> None:
    offsets = ((0, 0), (INPUT_WIDTH // 2, 0),
               (0, INPUT_HEIGHT // 2), (INPUT_WIDTH // 2, INPUT_HEIGHT // 2))
    boxes = torch.cat([FullFrameDataset._move_boxes(target["boxes"], left, top)
                       for target, (left, top) in zip(native_targets, offsets, strict=True)])
    ignores = torch.cat([FullFrameDataset._move_boxes(target["ignore_boxes"], left, top)
                         for target, (left, top) in zip(native_targets, offsets, strict=True)])
    labels = torch.cat([target["labels"] for target in native_targets])
    torch.testing.assert_close(mosaic_target["boxes"], boxes)
    torch.testing.assert_close(mosaic_target["ignore_boxes"], ignores)
    torch.testing.assert_close(mosaic_target["labels"], labels)
    if boxes.numel():
        assert bool((boxes[:, (0, 2)] >= 0).all() and (boxes[:, (0, 2)] <= INPUT_WIDTH).all())
        assert bool((boxes[:, (1, 3)] >= 0).all() and (boxes[:, (1, 3)] <= INPUT_HEIGHT).all())
    if ignores.numel():
        assert bool((ignores[:, (0, 2)] >= 0).all() and
                    (ignores[:, (0, 2)] <= INPUT_WIDTH).all())
        assert bool((ignores[:, (1, 3)] >= 0).all() and
                    (ignores[:, (1, 3)] <= INPUT_HEIGHT).all())


def _blank_metrics() -> dict:
    return {
        "gt": Counter(), "matched": Counter(), "no_in_box": Counter(),
        "foreground": Counter(), "best_iou": defaultdict(list),
        "assigned_iou": defaultdict(list), "assigned_iou_zero_filled": defaultdict(list),
        "boxes": defaultdict(list), "candidate_counts": [],
    }


def _measure_one(decoded: tuple[Tensor, Tensor, Tensor, Tensor, Tensor], batch_index: int,
                 target: dict[str, Tensor], totals: dict) -> dict:
    boxes, objects, classes, centers, strides = decoded
    gt_boxes = target["boxes"].float()
    gt_labels = target["labels"].long()
    per_class = {str(label): {"gt": 0, "matched_gt_after_conflict": 0,
                              "no_in_box_cell": 0, "foreground_anchors": 0}
                 for label in range(NUM_CLASSES)}
    if not len(gt_boxes):
        return {"gt": 0, "ignore": len(target["ignore_boxes"]), "candidate_union": 0,
                "per_class": per_class}

    candidates, _ = _candidate_mask(gt_boxes, centers[batch_index], strides[batch_index], 2.5)
    candidate_boxes = boxes[batch_index, candidates]
    pair_ious = pairwise_iou(gt_boxes, candidate_boxes)
    best = pair_ious.max(dim=1).values
    candidate_centers = centers[batch_index, candidates]
    left_top = candidate_centers[None] - gt_boxes[:, None, :2]
    right_bottom = gt_boxes[:, None, 2:] - candidate_centers[None]
    has_in_box = torch.cat((left_top, right_bottom), dim=2).amin(dim=2).gt(0).any(dim=1)
    foreground, matched_gt, matched_iou = simota_assign(
        boxes[batch_index], objects[batch_index], classes[batch_index],
        centers[batch_index], strides[batch_index], gt_boxes, gt_labels)
    matched_set = set(matched_gt.tolist())
    for gt_index, label in enumerate(gt_labels.tolist()):
        label_key = str(label)
        assigned = matched_iou[matched_gt == gt_index]
        assigned_best = float(assigned.max()) if len(assigned) else None
        per_class[label_key]["gt"] += 1
        per_class[label_key]["matched_gt_after_conflict"] += int(gt_index in matched_set)
        per_class[label_key]["no_in_box_cell"] += int(not bool(has_in_box[gt_index]))
        totals["gt"][label] += 1
        totals["matched"][label] += int(gt_index in matched_set)
        totals["no_in_box"][label] += int(not bool(has_in_box[gt_index]))
        totals["best_iou"][label].append(float(best[gt_index]))
        if assigned_best is not None:
            totals["assigned_iou"][label].append(assigned_best)
        totals["assigned_iou_zero_filled"][label].append(assigned_best or 0.0)
        totals["boxes"][label].append(gt_boxes[gt_index].tolist())
    for gt_index in matched_gt.tolist():
        label = int(gt_labels[gt_index])
        per_class[str(label)]["foreground_anchors"] += 1
        totals["foreground"][label] += 1
    totals["candidate_counts"].append(int(candidates.sum()))
    return {"gt": len(gt_boxes), "ignore": len(target["ignore_boxes"]),
            "candidate_union": int(candidates.sum()), "per_class": per_class}


def _final_metrics(totals: dict) -> dict:
    result = {"images": len(totals["candidate_counts"]),
              "candidate_union_count": _tensor_summary(totals["candidate_counts"]),
              "per_class": {}}
    for label in range(NUM_CLASSES):
        gt = totals["gt"][label]
        matched = totals["matched"][label]
        no_in_box = totals["no_in_box"][label]
        result["per_class"][str(label)] = {
            "name": CLASS_CONTRACT[str(label)], "gt": gt,
            "matched_gt_after_conflict": matched,
            "matched_gt_after_conflict_fraction": matched / gt if gt else None,
            "foreground_anchors": totals["foreground"][label],
            "gt_no_in_box_cell": no_in_box,
            "gt_no_in_box_cell_fraction": no_in_box / gt if gt else None,
            "best_prior_candidate_iou": _tensor_summary(totals["best_iou"][label]),
            "best_assigned_iou_matched_only": _tensor_summary(totals["assigned_iou"][label]),
            "best_assigned_iou_all_gt_zero_if_unmatched":
                _tensor_summary(totals["assigned_iou_zero_filled"][label]),
            "gt_box_size": _box_size_summary(totals["boxes"][label]),
        }
    return result


def _selected_indices(size: int, groups: int) -> list[int]:
    indices = np.linspace(0, size - 1, groups, dtype=np.int64).tolist()
    assert len(indices) == groups and len(set(indices)) == groups
    return indices


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--groups", type=int, default=MAX_GROUPS)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    if not 1 <= args.groups <= MAX_GROUPS:
        raise ValueError(f"groups must be 1..{MAX_GROUPS}")
    if args.output.exists():
        raise FileExistsError(args.output)

    torch.set_num_threads(2)
    torch.set_num_interop_threads(1)
    torch.use_deterministic_algorithms(True)
    started = time.perf_counter()
    checkpoint_stat = CHECKPOINT.stat()
    manifest_stat = MANIFEST.stat()
    assert sha256(CHECKPOINT) == CHECKPOINT_SHA256
    assert sha256(MANIFEST) == MANIFEST_SHA256
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    rows = _normalized_train_rows(payload, MANIFEST)
    dataset = FullFrameDataset(rows, "train", mosaic=False, seed=SEED)
    mosaic_dataset = FullFrameDataset(rows, "train", mosaic=True, seed=SEED)
    dataset.set_epoch(EPOCH)
    mosaic_dataset.set_epoch(EPOCH)
    anchors = _selected_indices(len(dataset), args.groups)
    all_indices = sorted(set(index for anchor in anchors
                             for index in _mosaic_indices(anchor, len(dataset))))
    selected_raw = []
    for index in all_indices:
        row = dataset.rows[index]
        digest = sha256(row["image_path"])
        if row.get("preprocess", {}).get("raw_image") is True:
            assert digest == row["source_sha256"]
        selected_raw.append({"train_index": index, "image": str(row["image_path"]),
                             "sha256": digest, "bytes": row["image_path"].stat().st_size})

    checkpoint = torch.load(CHECKPOINT, map_location="cpu", weights_only=False)
    model = RoadYOLOS4()
    assert checkpoint["architecture_hash"] == model.architecture_hash()
    assert checkpoint["dataset_sha256"] == MANIFEST_SHA256
    model.load_state_dict(checkpoint["model"], strict=True)
    model.eval()
    assert not model.training
    assert all(not module.training for module in model.modules()
               if isinstance(module, nn.BatchNorm2d))
    bn_before = _bn_digest(model)
    toy = _toy_conflict_check()
    totals = {"native": _blank_metrics(), "mosaic": _blank_metrics()}
    group_rows = []

    with torch.inference_mode():
        for group_number, anchor in enumerate(anchors, 1):
            if time.perf_counter() - started >= TIME_LIMIT_SECONDS:
                raise TimeoutError("five-minute probe limit reached; rerun with fewer --groups")
            indices = _mosaic_indices(anchor, len(dataset))
            native = [dataset[index] for index in indices]
            mosaic = mosaic_dataset[anchor]
            native_images, native_targets, native_keys = zip(*native)
            mosaic_image, mosaic_target, mosaic_key = mosaic
            _assert_mosaic_geometry(list(native_targets), mosaic_target)
            assert mosaic_key == "mosaic:" + "|".join(native_keys)
            assert Counter(mosaic_target["labels"].tolist()) == Counter(
                label for target in native_targets for label in target["labels"].tolist())
            images = torch.stack((*native_images, mosaic_image))
            decoded = decode_outputs(model(images))
            native_rows = [_measure_one(decoded, index, target, totals["native"])
                           for index, target in enumerate(native_targets)]
            mosaic_row = _measure_one(decoded, 4, mosaic_target, totals["mosaic"])
            group_rows.append({
                "group": group_number, "anchor_train_index": anchor,
                "constituent_train_indices": indices,
                "native": {
                    "images": 4, "gt": sum(row["gt"] for row in native_rows),
                    "ignore": sum(row["ignore"] for row in native_rows),
                    "per_image": native_rows,
                },
                "mosaic": {"images": 1, **mosaic_row},
            })
            assert group_rows[-1]["native"]["gt"] == mosaic_row["gt"]
            assert group_rows[-1]["native"]["ignore"] == mosaic_row["ignore"]
            if group_number == 1:
                print(json.dumps({"event": "early_metrics", "group": 1,
                                  "native": _final_metrics(totals["native"]),
                                  "mosaic": _final_metrics(totals["mosaic"])},
                                 separators=(",", ":")), flush=True)

    elapsed = time.perf_counter() - started
    if elapsed > TIME_LIMIT_SECONDS:
        raise TimeoutError("probe exceeded five-minute limit; no receipt written")
    bn_after = _bn_digest(model)
    assert bn_after == bn_before
    assert CHECKPOINT.stat().st_size == checkpoint_stat.st_size
    assert CHECKPOINT.stat().st_mtime_ns == checkpoint_stat.st_mtime_ns
    assert MANIFEST.stat().st_size == manifest_stat.st_size
    assert MANIFEST.stat().st_mtime_ns == manifest_stat.st_mtime_ns
    assert sha256(CHECKPOINT) == CHECKPOINT_SHA256
    assert sha256(MANIFEST) == MANIFEST_SHA256

    result = {
        "status": "completed_bounded_diagnostic",
        "scope": "eval_mode_CPU_FP32_SimOTA_assignment_diagnostic_not_train_mode_or_performance_acceptance",
        "created_at": datetime.now().astimezone().isoformat(),
        "elapsed_seconds": elapsed, "time_limit_seconds": TIME_LIMIT_SECONDS,
        "device": "cpu", "torch_threads": torch.get_num_threads(),
        "torch_interop_threads": torch.get_num_interop_threads(),
        "torch_version": torch.__version__, "python": platform.python_version(),
        "seed": SEED, "epoch": EPOCH, "groups_requested": args.groups,
        "groups_completed": len(group_rows), "native_images": 4 * len(group_rows),
        "mosaic_images": len(group_rows), "selection": "numpy.linspace_train_indices_inclusive",
        "checkpoint": {"path": str(CHECKPOINT), "sha256": CHECKPOINT_SHA256,
                       "epoch_field": checkpoint.get("epoch"),
                       "architecture_hash": checkpoint["architecture_hash"],
                       "dataset_sha256": checkpoint["dataset_sha256"]},
        "manifest": {"path": str(MANIFEST), "sha256": MANIFEST_SHA256,
                     "train_rows": len(rows)},
        "source_sha256": {
            "probe_person_assignment.py": sha256(Path(__file__)),
            "model.py": sha256(ROOT / "cnn/model.py"),
            "loss.py": sha256(ROOT / "cnn/loss.py"),
            "train.py": sha256(ROOT / "cnn/train.py"),
        },
        "selected_raw_bytes": selected_raw,
        "self_checks": {
            "deterministic_toy_conflict": toy,
            "actual_mosaic_key_and_positive_ignore_geometry_all_groups": True,
            "class_counts_native_equal_mosaic_all_groups": True,
            "batch_norm_snapshot_unchanged": True, "batch_norm_sha256": bn_after,
            "checkpoint_and_manifest_size_mtime_hash_unchanged": True,
        },
        "metric_definitions": {
            "best_prior_candidate_iou": "per GT maximum IoU over _candidate_mask union",
            "best_assigned_iou": "per GT maximum assigned IoU after SimOTA conflict resolution",
            "gt_no_in_box_cell": "GT has no strictly inside anchor center in prior candidate union",
            "matched_gt_after_conflict": "GT index appears in simota_assign matched_gt",
        },
        "metrics": {name: _final_metrics(value) for name, value in totals.items()},
        "groups": group_rows,
        "limitations": [
            "eval-mode assignment diagnostic; training-mode BatchNorm behavior is not measured",
            "assignment statistics are not detection performance or acceptance evidence",
            "only selected raw bytes are rehashed; the frozen manifest binds the full corpus",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
    print(json.dumps({"event": "final_receipt", "status": result["status"],
                      "groups": len(group_rows), "elapsed_seconds": elapsed,
                      "metrics": result["metrics"], "report": str(args.output),
                      "report_sha256": sha256(args.output)}, separators=(",", ":")), flush=True)


if __name__ == "__main__":
    main()
