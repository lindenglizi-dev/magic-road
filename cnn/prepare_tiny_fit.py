"""Prepare 32 COCO train + 16 val sentinels and CPU checks; no training entry."""
import argparse
from collections import Counter
import gc
import json
from pathlib import Path
import time
from unittest.mock import patch

import numpy as np
from PIL import Image, ImageDraw
import torch

from .archive_oct5 import ROOT, WEIGHT_SHA
from .dataset import (COCO_LABEL, _letterboxed_box, _letterbox_transform,
                      _refuse_blind, audit)
from .disk_cache import assert_item_equal, build_cache, open_validated_cache
from .integer import postprocess
from .loss import YOLOXLoss
from .metrics import report
from .model import RoadYOLOS4
from .train import (CLASS_CONTRACT, FullFrameDataset, build_parser, collate,
                    load_dataset_snapshot, make_frame_dataset, protocol_for,
                    protocol_hash, sha256, train)


SOURCE = ROOT / "cnn/data/coco_full/dataset.json"
SOURCE_SHA = "0bee36fd90cc78fd48cfc5a8d80ace60b66ce72ebe8eafaeb116602561566100"
DOWNLOAD = ROOT / "cnn/data/coco/download_receipt_full2017.json"
DOWNLOAD_SHA = "9d9fe8fb2d85361b6c34822ee505a02b996a05e0793778f5752025345b29bd6e"
FROZEN = ROOT / "cnn/releases/RoadYOLO-S4-512_20261009_before_ground_adapt"
CHECKPOINT = FROZEN / "ancestral_e7/cnn/runs/person_native_recovery_20261004/epoch_0006.pt"
OUTPUT = ROOT / "cnn/reports/tiny_fit32_20261009_v2"
RUN = ROOT / "cnn/runs/tiny_fit32_20261009_v2"
# Original-image visibility review, not predictions or GT edits. Preserve v1 evidence.
VISIBILITY_EXCLUSIONS = {
    162712: "printed traffic poster", 479081: "foreground portrait obscures street targets",
    205573: "dark night view", 205300: "strong backlit rider silhouette",
    408449: "dark blurred night targets", 180765: "vehicle and person reflected in mirrors",
    411937: "horse foreground and unclear vehicle extent", 107204: "indoor foreground and obscure vehicle",
    519542: "printed portrait and obscured background person", 539830: "severely truncated vehicle",
    152725: "sign obscures bus occupants", 544002: "dark night view",
    166631: "elephant foreground obscures vehicles", 502179: "water scene with obscure vehicle",
    413291: "interior/window view with obscure vehicle",
    455085: "bus rear and heavily hidden person", 84362: "television/indoor target",
    427338: "ruins with obscure vehicle", 30828: "bench and heavily hidden person/vehicle",
    513580: "aircraft scene with obscure target vehicle", 167486: "dark night view",
    289833: "indoor foreground and unclear vehicle", 422295: "overexposed cow scene with obscure vehicle",
    376958: "television targets", 384101: "kite scene with obscure distant vehicle",
    374904: "horse foreground and heavily truncated vehicle", 458338: "interior/reflection clutter",
    203235: "dark night sports scene", 135281: "dark blurred night vehicles",
    406767: "aircraft scene with obscure target vehicle", 355866: "heavily concealed person",
}
MIN_BOX_WIDTH, MIN_BOX_HEIGHT = 12, 32  # Diagnostic-only easy sample filter, never a GT/ignore rule.


def write_json(path, value):
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)


def guard_row(row):
    # Check all metadata before hashing/decoding any image, not just selected rows.
    text = json.dumps(row, ensure_ascii=False).lower()
    if row.get("split") not in ("train", "val") or any(
            word in text for word in ("blind", "reserve", "newtest", "yizhuang09", "spd:")):
        raise ValueError("forbidden split/path/camera in tiny-fit source")


def select_rows(document):
    if document.get("training_eligible") is not True or audit(document)["incomplete_frames"]:
        raise ValueError("requires a complete, eligible COCO training manifest")
    pools = {"train": [], "val": []}
    for row in document["images"]:
        guard_row(row)
        image_id = row["source_frame"]
        if (row["scene_id"] != f"coco-{image_id}"
                or Path(row["image"]).stem != f"{image_id:012d}"
                or not row.get("preprocess", {}).get("raw_image")
                or row.get("annotation_complete") is not True):
            raise ValueError("source is not the declared raw official COCO image")
        counts = Counter(row["labels"])
        if (image_id not in VISIBILITY_EXCLUSIONS
                and set(counts) == {0, 1} and max(counts.values()) <= 32
                and not row["ignore_boxes"]
                and all(box[2] - box[0] >= MIN_BOX_WIDTH and box[3] - box[1] >= MIN_BOX_HEIGHT
                        for box in row["boxes"])):
            pools[row["split"]].append(row)
    selected = []
    for split, count in (("train", 32), ("val", 16)):
        pool = sorted(pools[split], key=lambda row: (row["source_sha256"], row["image"]))
        if len(pool) < count:
            raise ValueError(f"not enough eligible {split} images: {len(pool)} < {count}")
        selected.extend(pool[:count])
    for field in ("image", "scene_id", "source_sha256", "source_frame"):
        if len({row[field] for row in selected}) != 48:
            raise ValueError(f"duplicate/overlapping selected {field}")
    return selected, {split: len(pool) for split, pool in pools.items()}


def verify_annotations(rows, entry, expected_sha):
    """Reconstruct all selected targets from pinned official annotations, not predictions."""
    path = ROOT / entry["annotation_json"]
    _refuse_blind(path)
    if sha256(path) != expected_sha:
        raise ValueError("official COCO annotation hash changed")
    print(f"checking official {entry['split']} annotations", flush=True)
    # ponytail: stdlib parse one split at a time; no custom streaming JSON parser.
    with path.open(encoding="utf-8") as stream:
        raw = json.load(stream)
    wanted = {row["source_frame"]: row for row in rows if row["split"] == entry["split"]}
    categories = {row["id"]: COCO_LABEL[row["name"]] for row in raw["categories"]
                  if row["name"] in COCO_LABEL}
    sources = {row["id"]: row for row in raw["images"] if row["id"] in wanted}
    annotations = [row for row in raw["annotations"] if row["image_id"] in wanted]
    all_categories = raw["categories"]
    del raw
    gc.collect()
    if sources.keys() != wanted.keys():
        raise ValueError("selected source image absent from official annotations")
    mapping = []
    for image_id, row in wanted.items():
        source = sources[image_id]
        image = Path(row["image"])
        expected_path = (ROOT / entry["image_root"] / source["file_name"]).resolve()
        _refuse_blind(image)
        if image.resolve() != expected_path or sha256(image) != row["source_sha256"]:
            raise ValueError("selected pixels do not match official image identity")
        with Image.open(image) as header:
            if header.size != (source["width"], source["height"]):
                raise ValueError("official annotation/image dimensions differ")
        transform = _letterbox_transform(source["width"], source["height"])
        boxes, labels, ids, original_categories = [], [], [], []
        for annotation in annotations:
            if annotation["image_id"] != image_id or annotation["category_id"] not in categories:
                continue
            if annotation.get("iscrowd") or min(annotation["bbox"][2:]) <= 0:
                raise ValueError("selected frame unexpectedly needs crowd/degenerate ignore")
            boxes.append(_letterboxed_box(list(map(float, annotation["bbox"])), transform))
            labels.append(categories[annotation["category_id"]])
            ids.append(annotation["id"])
            original_categories.append(annotation["category_id"])
        if (boxes != row["boxes"] or labels != row["labels"]
                or transform != row["preprocess"]["letterbox_1280x720"]):
            raise ValueError("selected target/geometry differs from complete official annotations")
        mapping.append(dict(image_id=image_id, split=row["split"], annotation_ids=ids,
                            original_category_ids=original_categories,
                            preserved_all_target_annotations=True))
    if sha256(path) != expected_sha:
        raise ValueError("annotation source changed during inspection")
    return dict(source=str(path), source_sha256=expected_sha,
                images=list(sources.values()), annotations=annotations,
                categories=all_categories, target_mapping=mapping)


def training_arguments(manifest, cache, index_sha):
    return ["--dataset", str(manifest), "--output", str(RUN),
            "--init-checkpoint", str(CHECKPOINT), "--phase", "supervised",
            "--epochs", "75", "--batch-size", "8", "--accum-steps", "1",
            "--lr", "0.001", "--lr-schedule", "finetune_constant",
            "--momentum", "0.9", "--weight-decay", "0.0005", "--clip-grad", "10",
            "--seed", "42", "--workers", "0", "--device", "cuda", "--no-amp",
            "--no-mosaic", "--checkpoint-kind", "diagnostic", "--max-steps", "300",
            "--checkpoint-every-seconds", "0", "--input-cache", str(cache),
            "--input-cache-index-sha256", index_sha]


def score_fit(model, rows, manifest, checkpoint_metadata, checkpoint_sha):
    """Training-split memorization baseline, explicitly NOT validation accuracy."""
    dataset = FullFrameDataset(rows, "train", mosaic=False)
    predictions, truth = [], []
    model.eval()
    with torch.inference_mode():
        for index, row in enumerate(dataset.rows):
            image, _, _ = dataset[index]
            outputs = model(image.unsqueeze(0))
            heads = [np.clip(np.rint(out[0].permute(1, 2, 0).numpy() * 256),
                             -32768, 32767).astype(np.int16) for out in outputs]
            predictions.extend(dict(image_id=row["image"], label=det["label"],
                                    box=[value / 256 for value in det["box_q8"]],
                                    score=det["score_uint16"] / 65536)
                               for det in postprocess(heads, (3276, 3276)))
            truth.extend(dict(image_id=row["image"], label=label, box=box)
                         for box, label in zip(row["boxes"], row["labels"], strict=True))
            if (index + 1) % 8 == 0:
                print(f"CPU training-fit baseline {index + 1}/32", flush=True)
    return dict(status="training_fit_baseline_same_as_train_NOT_validation",
                split="train", same_as_train=True, checkpoint_sha256=checkpoint_sha,
                checkpoint_epoch_number=checkpoint_metadata["epoch"] + 1,
                checkpoint_optimizer_steps=checkpoint_metadata["trained_steps"],
                architecture_hash=checkpoint_metadata["architecture_hash"],
                checkpoint_training_dataset_sha256=checkpoint_metadata["dataset_sha256"],
                checkpoint_training_dataset_content_sha256=checkpoint_metadata["dataset_content_sha256"],
                scoring_scope="E7_initializer_baseline_on_tiny_training_rows; NOT a trained tiny-fit checkpoint",
                dataset_sha256=sha256(manifest), image_count=len(dataset),
                inference="FP32_CNN_plus_fixed_point_postprocess_NOT_INT8",
                postprocess=dict(top_k_per_class=128, max_boxes_per_class=32,
                                 nms_iou=0.5, score_floor_uint16=3276),
                diagnostic_metrics_at_0_5=report(predictions, truth, [], thresholds=(.5, .5)),
                predictions=predictions, truth=truth, ignores=[], formal_acceptance=False)


def contact_sheets(rows, manifest, output):
    for split in ("train", "val"):
        dataset = FullFrameDataset(rows, split)
        for start in range(0, len(dataset), 16):
            sheet = Image.new("RGB", (1024, 672), "white")
            for index in range(start, min(start + 16, len(dataset))):
                pixels, target, _ = dataset._load(index)
                image = Image.fromarray(pixels)
                draw = ImageDraw.Draw(image)
                for box, label in zip(target["boxes"].tolist(), target["labels"].tolist(), strict=True):
                    draw.rectangle(box, outline=(0, 255, 0) if label == 0 else (255, 180, 0), width=2)
                image = image.resize((256, 144))
                x, y = ((index - start) % 4) * 256, ((index - start) // 4) * 168
                sheet.paste(image, (x, y + 24))
                ImageDraw.Draw(sheet).text((x + 3, y + 3),
                    f"{split} {index + 1}: COCO {dataset.rows[index]['source_frame']}", fill="black")
            sheet.save(output / f"{split}_gt_{start // 16 + 1:02d}.jpg")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--preview-only", action="store_true",
                        help="raw GT sheets only; no CNN, gradients, cache or preflight claim")
    args = parser.parse_args()
    output = args.output.resolve()
    if not output.is_relative_to(ROOT / "cnn/reports") or output.exists():
        raise ValueError("requires a new directory inside cnn/reports")
    for path in (SOURCE, DOWNLOAD, CHECKPOINT, output):
        _refuse_blind(path)
    if (sha256(SOURCE) != SOURCE_SHA or sha256(DOWNLOAD) != DOWNLOAD_SHA
            or sha256(CHECKPOINT) != WEIGHT_SHA):
        raise ValueError("source/checkpoint receipt identity changed")
    started = time.perf_counter()
    torch.set_num_threads(2)
    torch.use_deterministic_algorithms(True)
    with SOURCE.open(encoding="utf-8") as stream:
        selected, pool_counts = select_rows(json.load(stream))
    gc.collect()
    output.mkdir(parents=True, exist_ok=False)
    document = dict(schema_version=1, task="detection", input_size=[512, 288],
                    classes=["person", "vehicle"], training_eligible=True,
                    manifest_status="diagnostic_training_fit_32_plus_val16",
                    purpose="training_fit_diagnostic_not_road_validation", images=selected,
                    diagnostic_only=True, formal_road_eligible=False)
    manifest = output / "tiny_fit32_manifest.json"
    write_json(manifest, document)
    if args.preview_only:
        _, snapshot = load_dataset_snapshot(manifest)
        contact_sheets(snapshot.rows, manifest, output)
        write_json(output / "preview_receipt.json", dict(
            status="source_GT_preview_only_NOT_preflight", dataset_sha256=sha256(manifest),
            original_image_visibility_exclusions=VISIBILITY_EXCLUSIONS,
            selected_by_predictions=False, training_started=False, GPU_compute_started=False))
        print(str(output), flush=True)
        return
    download = json.loads(DOWNLOAD.read_text(encoding="utf-8"))
    pinned = {str((ROOT / item["path"]).resolve()): item["sha256"]
              for item in download["annotation_files"]}
    sources = []
    for entry in download["image_json_paths"]:
        source = verify_annotations(selected, entry,
                                    pinned[str((ROOT / entry["annotation_json"]).resolve())])
        write_json(output / f"official_{entry['split']}_selected.json", source)
        sources.append(dict(path=source["source"], sha256=source["source_sha256"],
                            selected_images=len(source["images"])))
        del source
        gc.collect()
    _, snapshot = load_dataset_snapshot(manifest)
    cache = output / "cache"
    cache_receipt = build_cache(manifest, snapshot.rows, cache)
    index_sha = sha256(cache / "index.json")
    binding = open_validated_cache(snapshot, cache, index_sha)
    raw = {split: FullFrameDataset(snapshot.rows, split) for split in ("train", "val")}
    cached = {split: make_frame_dataset(snapshot.rows, split, manifest, cache_root=cache,
               cache_index_sha256=index_sha, cache_binding=binding) for split in ("train", "val")}
    for split in raw:
        for index in range(len(raw[split])):
            assert_item_equal(raw[split][index], cached[split][index])
    command = training_arguments(manifest, cache, index_sha)
    training_args = build_parser().parse_args(command + ["--validate-only"])
    # Validate the real CUDA-target argument path but fail if it queries/initializes CUDA.
    with patch("torch.cuda.is_available", side_effect=AssertionError("CUDA access forbidden")), \
            patch("torch.cuda.init", side_effect=AssertionError("CUDA access forbidden")):
        if train(training_args) != 0:
            raise ValueError("real trainer validate-only failed")
        checkpoint = torch.load(CHECKPOINT, map_location="cpu", weights_only=False)
        model = RoadYOLOS4().cpu()
        model.load_state_dict(checkpoint["model"], strict=True)
        if checkpoint["architecture_hash"] != model.architecture_hash():
            raise ValueError("architecture mismatch")
        baseline = score_fit(model, snapshot.rows, manifest, checkpoint, sha256(CHECKPOINT))
        write_json(output / "e7_training_fit_baseline.json", baseline)
        images, targets, _ = collate([cached["train"][index] for index in range(8)])
        model.train()  # Disposable BN state only, no optimizer and no saved-weight update.
        losses = YOLOXLoss()(model(images), targets)
        if not all(torch.isfinite(value).all() for value in losses.values()):
            raise FloatingPointError("non-finite CPU loss")
        losses["loss"].backward()
        gradients = [p.grad for p in model.parameters() if p.requires_grad]
        if (not gradients or any(g is None or not torch.isfinite(g).all() for g in gradients)
                or not any(torch.count_nonzero(g) for g in gradients)):
            raise FloatingPointError("missing, non-finite or all-zero gradients")
    contact_sheets(snapshot.rows, manifest, output)
    if sha256(SOURCE) != SOURCE_SHA or sha256(CHECKPOINT) != WEIGHT_SHA:
        raise ValueError("source or saved network changed during checks")
    protocol = protocol_for(training_args, 4, None)
    write_json(output / "training_contract_proposed.json", dict(
        status="CPU_prepared_GPU_execution_NOT_authorized_by_this_receipt",
        checkpoint_sha256=WEIGHT_SHA, dataset_sha256=sha256(manifest),
        dataset_content_sha256=snapshot.dataset_content_sha256, cache_index_sha256=index_sha,
        protocol=protocol, protocol_sha256=protocol_hash(protocol),
        trainer_arguments=command, optimizer_update_cap=300, wall_seconds_cap=1800,
        protection_required=True, automatic_resume=False, training_authorized=False,
        diagnostic_checkpoint_warning="no mid-epoch resumable save; timeout uses last complete epoch"))
    artifacts = {p.relative_to(output).as_posix(): sha256(p)
                 for p in output.rglob("*") if p.is_file()}
    receipt = dict(status="prepared_and_CPU_preflight_passed_NOT_trained",
        dataset_sha256=sha256(manifest), checkpoint_sha256=WEIGHT_SHA,
        source_manifest_sha256=SOURCE_SHA, official_annotation_sources=sources,
        selection="source_sha256_sorted_after_label_size_density_filters_and_finite_original_image_visibility_exclusions",
        minimum_network_box_size=[MIN_BOX_WIDTH, MIN_BOX_HEIGHT],
        original_image_visibility_exclusions=VISIBILITY_EXCLUSIONS,
        visibility_review_scope="limited image-level diagnostic selection, not new GT certification",
        selected_by_predictions=False, eligible_pool_counts=pool_counts,
        audit=audit(document), all_selected_targets_reconstructed_from_official_annotations=True,
        exact_image_hash_scene_and_image_id_overlap=0, excluded_camera="SPD:yizhuang09:1/all",
        source_completeness="official annotations, not new manual full-frame completeness certification",
        sentinel_scope="official COCO val, disjoint from tiny train but historically used; not unseen road test",
        cache_items_compared=48, cache_max_difference=0, cache_rgb_bytes=cache_receipt["rgb_bytes"],
        real_trainer_validate_only_passed=True, CUDA_calls_blocked_during_preflight=True,
        CPU_forward_backward_microbatch=8, optimizer_updates=0, training_started=False,
        GPU_compute_started=False, saved_weights_modified=False, formal_acceptance=False,
        CPU_loss={name: float(value) for name, value in losses.items()},
        gradient_tensors_checked=len(gradients), elapsed_seconds=time.perf_counter() - started,
        artifacts=artifacts, source_sha256={name: sha256(ROOT / "cnn" / name) for name in (
            "prepare_tiny_fit.py", "dataset.py", "train.py", "disk_cache.py", "model.py",
            "loss.py", "integer.py", "metrics.py")})
    write_json(output / "preflight_receipt.json", receipt)
    print(json.dumps({key: receipt[key] for key in (
        "status", "cache_items_compared", "CPU_forward_backward_microbatch", "optimizer_updates",
        "CPU_loss", "elapsed_seconds")}, ensure_ascii=False), flush=True)
    print(str(output / "preflight_receipt.json"), flush=True)


if __name__ == "__main__":
    main()
