#!/usr/bin/env python3
"""Build a hash-bound VIRAT full-frame review package without scoring models."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

import cv2


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "evaluation/public_data/virat_ground_v2/catalog.json"
CANONICAL_ANNOTATIONS = ROOT / "evaluation/public_data/virat_ground_v2/annotations.csv"
LICENSE_RECEIPT = ROOT / "public_data/raw/virat_ground_v2/docs/user_acceptance_receipt.json"
EXTENSION_DIR = ROOT / "evaluation/scene_extensions/virat_010107_02_t100"
EXTENSION_OVERLAY = EXTENSION_DIR / "split_overlay.json"
MIN_GROUP_GAP_MS = 2000.0

# Fixed before any prediction is run.  Extra scenes/frames are required because
# 72 frames from three sparse clips cannot reach 100 de-correlated groups/class.
SELECTIONS = [
    ("VIRAT_S_000200_00_000100_000171", 24, "development_validation"),
    ("VIRAT_S_000203_03_000736_000785", 24, "development_validation"),
    ("VIRAT_S_000205_00_000065_000149", 28, "development_holdout_previously_viewed"),
    ("VIRAT_S_000207_02_000498_000530", 24, "development_holdout_previously_viewed"),
    ("VIRAT_S_010107_02_000282_000312", 24, "development_validation_extension"),
]
FORBIDDEN_TRAIN_SCENES = {"000201", "000206"}
PHYSICAL_CAMERAS = {
    # Visual QA shows the same parking-lot landmarks and perspective in these
    # four clips.  Scene IDs are not independent physical-camera evidence.
    "VIRAT_S_000200_00_000100_000171": "virat-parking-lot-camera-a",
    "VIRAT_S_000203_03_000736_000785": "virat-parking-lot-camera-a",
    "VIRAT_S_000205_00_000065_000149": "virat-parking-lot-camera-a",
    "VIRAT_S_000207_02_000498_000530": "virat-parking-lot-camera-a",
    "VIRAT_S_010107_02_000282_000312": "virat-010107-camera-b",
}

FRAME_REVIEW_FIELDS = [
    "sample_id", "clip_id", "scene_id", "camera_id", "development_role",
    "source_catalog_split", "source_family_id", "frame_index", "timestamp_ms",
    "width", "height", "raw_frame_path", "raw_frame_sha256",
    "raw_frame_pixel_sha256", "overlay_path", "overlay_sha256",
    "source_box_count", "source_ped_box_count", "source_vehicle_box_count",
    "source_ignore_box_count", "source_ped_time_group_representatives",
    "source_vehicle_time_group_representatives", "selection_basis",
    "annotation_complete", "training_eligible", "formal_acceptance",
    "review_status", "human_frame_complete", "human_person_complete",
    "human_vehicle_complete", "human_rider_pairs_complete", "human_ignore_complete",
    "human_density_bucket", "human_stress_tags", "reviewer", "reviewed_at",
    "review_notes",
]

BOX_REVIEW_FIELDS = [
    "source_box_id", "sample_id", "clip_id", "scene_id", "frame_index",
    "timestamp_ms", "target_id", "source_object_id", "source_annotation_line",
    "source_annotation_path", "source_annotation_sha256", "xmin", "ymin", "xmax",
    "ymax", "width", "height", "label", "original_label", "original_type", "ignore",
    "source_time_group_id", "source_time_group_representative",
    "source_status", "annotation_complete", "training_eligible", "formal_acceptance",
    "human_box_status", "human_semantic_class", "human_model_label", "human_target_id",
    "human_xmin", "human_ymin", "human_xmax", "human_ymax", "human_occlusion",
    "human_truncation", "human_rider_pair_id", "human_ignore", "human_ignore_reason",
    "reviewer", "reviewed_at", "review_notes",
]

ADDITION_FIELDS = [
    "sample_id", "human_box_id", "semantic_class", "model_label", "target_id",
    "xmin", "ymin", "xmax", "ymax", "occlusion", "truncation", "rider_pair_id",
    "ignore", "ignore_reason", "reviewer", "reviewed_at", "review_notes",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def pixel_sha256(image: Any) -> str:
    return hashlib.sha256(image.tobytes()).hexdigest()


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
                    encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def evenly_spaced(values: list[int], count: int) -> list[int]:
    if len(values) < count:
        raise ValueError(f"only {len(values)} eligible frames for requested {count}")
    if count == 1:
        return [values[len(values) // 2]]
    result = [values[round(index * (len(values) - 1) / (count - 1))]
              for index in range(count)]
    if len(set(result)) != count:
        raise AssertionError("even sampling produced duplicate frames")
    return result


def canonical_clip_rows(path: Path, clip_ids: set[str]) -> dict[str, list[dict[str, Any]]]:
    output: dict[str, list[dict[str, Any]]] = defaultdict(list)
    with path.open(newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            clip_id = row["clip_id"]
            if clip_id not in clip_ids:
                continue
            xmin, ymin, xmax, ymax = (int(row[key]) for key in ("xmin", "ymin", "xmax", "ymax"))
            output[clip_id].append({
                "clip_id": clip_id,
                "scene_id": row["scene_id"],
                "frame_index": int(row["frame_index"]),
                "xmin": xmin, "ymin": ymin, "xmax": xmax, "ymax": ymax,
                "label": row["label"],
                "original_label": row["original_label"],
                "original_type": int(row["original_type"]),
                "target_id": row["object_id"],
                "source_object_id": row["source_object_id"],
                "source_annotation_line": int(row["source_annotation_line"]),
            })
    return output


def extension_rows(path: Path, clip_id: str, scene_id: str) -> list[dict[str, Any]]:
    labels = {0: ("ignore", "unknown"), 1: ("ped", "person"),
              2: ("vehicle", "car"), 3: ("vehicle", "vehicle"),
              4: ("ignore", "object_type_4"), 5: ("ignore", "object_type_5")}
    output = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            values = line.split()
            if len(values) != 8:
                raise ValueError(f"extension annotation line {line_number} does not have 8 fields")
            object_id, _duration, frame, x, y, width, height, raw_type = map(int, values)
            if raw_type not in labels:
                raise ValueError(f"unknown VIRAT type {raw_type} at line {line_number}")
            label, original_label = labels[raw_type]
            output.append({
                "clip_id": clip_id, "scene_id": scene_id, "frame_index": frame,
                "xmin": x, "ymin": y, "xmax": x + width - 1, "ymax": y + height - 1,
                "label": label, "original_label": original_label, "original_type": raw_type,
                "target_id": f"{clip_id}:track-{object_id}",
                "source_object_id": object_id, "source_annotation_line": line_number,
            })
    return output


def validate_boxes(rows: list[dict[str, Any]], frame_count: int, width: int, height: int) -> None:
    for row in rows:
        if not 0 <= row["frame_index"] < frame_count:
            raise ValueError(f"out-of-range annotation frame: {row}")
        if not (0 <= row["xmin"] <= row["xmax"] < width and
                0 <= row["ymin"] <= row["ymax"] < height):
            raise ValueError(f"out-of-range annotation box: {row}")


def assign_time_groups(rows: list[dict[str, Any]], fps_by_clip: dict[str, float]) -> dict[str, int]:
    grouped: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[(row["clip_id"], row["target_id"], row["label"])].append(row)
    counts: Counter[str] = Counter()
    for (clip_id, target_id, label), values in sorted(grouped.items()):
        anchor_ms: float | None = None
        group_number = 0
        for row in sorted(values, key=lambda item: (item["frame_index"], item["source_annotation_line"])):
            timestamp_ms = 1000.0 * row["frame_index"] / fps_by_clip[clip_id]
            representative = anchor_ms is None or timestamp_ms - anchor_ms >= MIN_GROUP_GAP_MS
            if representative:
                group_number += 1
                anchor_ms = timestamp_ms
                counts[label] += 1
            row["source_time_group_id"] = f"{target_id}:tg{group_number:03d}"
            row["source_time_group_representative"] = representative
    return dict(counts)


def render_overlay(frame: Any, rows: list[dict[str, Any]]) -> Any:
    colors = {"ped": (0, 255, 0), "vehicle": (0, 210, 255), "ignore": (160, 160, 160)}
    overlay = frame.copy()
    for row in rows:
        color = colors[row["label"]]
        p1, p2 = (row["xmin"], row["ymin"]), (row["xmax"], row["ymax"])
        cv2.rectangle(overlay, p1, p2, color, 2)
        text = f"{row['label']}:{row['source_object_id']}"
        y = max(12, row["ymin"] - 4)
        cv2.putText(overlay, text, (row["xmin"], y), cv2.FONT_HERSHEY_SIMPLEX,
                    0.38, color, 1, cv2.LINE_AA)
    return overlay


def decode_clip(clip: dict[str, Any], samples: list[dict[str, Any]],
                rows_by_frame: dict[int, list[dict[str, Any]]], output: Path) -> dict[str, Any]:
    video = Path(clip["video_path"])
    capture = cv2.VideoCapture(str(video))
    if not capture.isOpened():
        raise RuntimeError(f"cannot open {video}")
    actual = {
        "frame_count": int(capture.get(cv2.CAP_PROP_FRAME_COUNT)),
        "width": int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
        "height": int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        "fps": float(capture.get(cv2.CAP_PROP_FPS)),
    }
    expected = {key: clip[key] for key in ("frame_count", "width", "height")}
    if any(actual[key] != expected[key] for key in expected):
        raise ValueError(f"video metadata mismatch for {clip['clip_id']}: {actual} != {expected}")
    if abs(actual["fps"] - float(clip["fps"])) > 0.02:
        raise ValueError(f"fps mismatch for {clip['clip_id']}: {actual['fps']} != {clip['fps']}")
    sample_by_frame = {row["frame_index"]: row for row in samples}
    raw_dir, overlay_dir = output / "raw_frames", output / "official_overlays"
    decoded = 0
    for frame_index in range(actual["frame_count"]):
        ok, frame = capture.read()
        if not ok:
            raise RuntimeError(f"decode stopped at frame {frame_index} of {actual['frame_count']}")
        decoded += 1
        sample = sample_by_frame.get(frame_index)
        if sample is None:
            continue
        if frame.shape[:2] != (actual["height"], actual["width"]):
            raise ValueError(f"decoded shape mismatch at {clip['clip_id']} frame {frame_index}")
        source_pixel_hash = pixel_sha256(frame)
        raw_path = raw_dir / f"{sample['sample_id']}.png"
        overlay_path = overlay_dir / f"{sample['sample_id']}.png"
        if not cv2.imwrite(str(raw_path), frame, [cv2.IMWRITE_PNG_COMPRESSION, 3]):
            raise RuntimeError(f"failed to write {raw_path}")
        if not cv2.imwrite(str(overlay_path), render_overlay(frame, rows_by_frame[frame_index]),
                           [cv2.IMWRITE_PNG_COMPRESSION, 3]):
            raise RuntimeError(f"failed to write {overlay_path}")
        restored = cv2.imread(str(raw_path), cv2.IMREAD_COLOR)
        if restored is None or pixel_sha256(restored) != source_pixel_hash:
            raise AssertionError(f"lossless PNG round-trip failed for {raw_path}")
        sample.update({
            "width": actual["width"], "height": actual["height"],
            "raw_frame_path": raw_path.relative_to(output).as_posix(),
            "raw_frame_sha256": sha256(raw_path),
            "raw_frame_pixel_sha256": source_pixel_hash,
            "overlay_path": overlay_path.relative_to(output).as_posix(),
            "overlay_sha256": sha256(overlay_path),
        })
    extra_ok, _extra = capture.read()
    capture.release()
    if decoded != actual["frame_count"] or extra_ok:
        raise AssertionError(f"full sequential decode identity check failed for {clip['clip_id']}")
    return {**actual, "decoded_frames": decoded, "sequential_from_zero": True,
            "no_seek_used": True, "end_of_stream_confirmed": True}


def instructions() -> str:
    return """# VIRAT 地面完整帧审核说明

本包只准备开发集人工审核，不含模型预测、训练或评分。`raw_frames/` 是 1280×720
无损原帧；`official_overlays/` 仅叠加 VIRAT source-provided boxes。官方框不是完整背景
真值，不能据此把未框区域当负样本。

## 填写顺序

1. 先锁定 `frame_review_manifest.csv` 的行和图像哈希，不增删或替换抽样帧。
2. 对每帧核完所有可见 person，以及 car/bus/truck/motorcycle/bicycle 五类 vehicle。
3. 骑行者必须分别给 person 框和对应两轮车 vehicle 框，允许重叠，并填写相同
   `rider_pair_id`。无法判定的区域设为 ignore，不猜类别。
4. 对既有官方框在 `source_box_review.csv` 填 `human_box_status`：
   `valid|adjust|relabel|ignore|uncertain`。坐标或类别修订只填 human_* 字段，不改 source 字段。
5. 漏框追加到 `human_additions.csv`；`semantic_class` 取
   `person|car|bus|truck|motorcycle|bicycle|other`，`model_label` 只取
   `ped|vehicle|ignore`。坐标是零起始、闭区间，必须落在 1280×720 内。
6. 确认框、漏标、ignore 和骑行者均核完后，才把帧级五个 `human_*_complete`
   填 `yes`，补 reviewer/reviewed_at。任一不确定则保持空白或填 `no`。

## 接续门禁

人工签署前固定为 `annotation_complete=false`、`training_eligible=false`、
`formal_acceptance=false`。审核完成后应由独立导入器验证 sample_id、图像哈希、坐标、
target_id 唯一性和骑行者成对关系，生成新版本目录；不得覆盖本包，也不得把官方框自动
升级为完整真值。source time group 按同 clip + target_id + label 贪心选择至少 2000 ms
间隔的代表帧；它不是 box-frame row 数，也尚不是人工核实组数。

## 恢复

脚本拒绝覆盖已有目录。中断或校验失败时保留原目录作为失败证据，换一个新的输出目录重跑；
成功包可用 `--verify-existing <目录>` 只读复核全部产物 SHA-256。
"""


def verify_existing(output: Path) -> dict[str, Any]:
    receipt_path = output / "ground_review_receipt.json"
    index_path = output / "artifact_hashes.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    if sha256(index_path) != receipt["artifact_hashes_sha256"]:
        raise AssertionError("artifact_hashes.json hash mismatch")
    artifacts = json.loads(index_path.read_text(encoding="utf-8"))
    for relative, expected in artifacts.items():
        path = output / relative
        if not path.is_file() or sha256(path) != expected:
            raise AssertionError(f"artifact mismatch: {relative}")
    return {"status": "verified", "artifact_count": len(artifacts),
            "receipt_sha256": sha256(receipt_path)}


def build(output: Path) -> dict[str, Any]:
    if output.exists():
        raise FileExistsError(f"refusing to overwrite existing output: {output}")
    output.mkdir(parents=True)
    (output / "raw_frames").mkdir()
    (output / "official_overlays").mkdir()

    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    license_receipt = json.loads(LICENSE_RECEIPT.read_text(encoding="utf-8"))
    overlay = json.loads(EXTENSION_OVERLAY.read_text(encoding="utf-8"))
    if not license_receipt.get("accepted"):
        raise ValueError("VIRAT usage agreement receipt is not accepted")
    if sha256(LICENSE_RECEIPT) != catalog["user_acceptance_receipt"]["receipt_sha256"]:
        raise ValueError("license receipt hash does not match catalog")
    catalog_clips = {row["clip_id"]: dict(row) for row in catalog["clips"]}
    canonical_ids = {clip_id for clip_id, _count, _role in SELECTIONS
                     if clip_id != overlay["clip_id"]}
    rows_by_clip = canonical_clip_rows(CANONICAL_ANNOTATIONS, canonical_ids)
    extension_annotation = Path(overlay["annotations"])
    rows_by_clip[overlay["clip_id"]] = extension_rows(
        extension_annotation, overlay["clip_id"], overlay["scene_id"])

    clips: dict[str, dict[str, Any]] = {}
    for clip_id, requested, role in SELECTIONS:
        if clip_id in catalog_clips:
            clip = catalog_clips[clip_id]
            source_split = clip["split"]
            if source_split == "train" or any(scene in clip["scene_id"] for scene in FORBIDDEN_TRAIN_SCENES):
                raise ValueError(f"train scene is forbidden in ground review: {clip_id}")
            clip.update({"development_role": role, "source_catalog_split": source_split,
                         "sample_count": requested})
        else:
            clip = {
                "clip_id": clip_id, "scene_id": overlay["scene_id"],
                "frame_count": 479, "width": 1280, "height": 720, "fps": 23.97,
                "video_path": overlay["video"], "annotation_path": overlay["annotations"],
                "video_sha256": overlay["video_sha256"],
                "annotation_sha256": overlay["annotations_sha256"],
                "development_role": role, "source_catalog_split": overlay["split"],
                "sample_count": requested,
            }
        clips[clip_id] = clip
        clip["physical_camera_id"] = PHYSICAL_CAMERAS[clip_id]

    for clip_id, clip in clips.items():
        if sha256(Path(clip["video_path"])) != clip["video_sha256"]:
            raise ValueError(f"source video SHA-256 mismatch: {clip_id}")
        if sha256(Path(clip["annotation_path"])) != clip["annotation_sha256"]:
            raise ValueError(f"source annotation SHA-256 mismatch: {clip_id}")
        validate_boxes(rows_by_clip[clip_id], clip["frame_count"], clip["width"], clip["height"])

    selected_frames: dict[str, list[int]] = {}
    all_samples: list[dict[str, Any]] = []
    selected_box_rows: list[dict[str, Any]] = []
    sample_number = 0
    for clip_id, _requested, _role in SELECTIONS:
        clip = clips[clip_id]
        by_frame: dict[int, list[dict[str, Any]]] = defaultdict(list)
        for row in rows_by_clip[clip_id]:
            by_frame[row["frame_index"]].append(row)
        eligible = sorted(frame for frame, rows in by_frame.items()
                          if {row["label"] for row in rows} >= {"ped", "vehicle"})
        chosen = evenly_spaced(eligible, clip["sample_count"])
        selected_frames[clip_id] = chosen
        for frame_index in chosen:
            sample_id = f"gr{sample_number:04d}"
            sample_number += 1
            frame_rows = by_frame[frame_index]
            sample = {
                "sample_id": sample_id, "clip_id": clip_id,
                "scene_id": clip["scene_id"], "camera_id": clip["physical_camera_id"],
                "development_role": clip["development_role"],
                "source_catalog_split": clip["source_catalog_split"],
                "source_family_id": clip["physical_camera_id"], "frame_index": frame_index,
                "timestamp_ms": f"{1000.0 * frame_index / clip['fps']:.6f}",
                "selection_basis": "fixed_even_spacing_over_frames_with_source_ped_and_vehicle_boxes",
                "annotation_complete": "false", "training_eligible": "false",
                "formal_acceptance": "false", "review_status": "pending_human_full_frame_review",
                "human_frame_complete": "", "human_person_complete": "",
                "human_vehicle_complete": "", "human_rider_pairs_complete": "",
                "human_ignore_complete": "", "human_density_bucket": "",
                "human_stress_tags": "", "reviewer": "", "reviewed_at": "",
                "review_notes": "",
            }
            all_samples.append(sample)
            for row in frame_rows:
                selected_box_rows.append({**row, "sample_id": sample_id,
                                          "timestamp_ms": sample["timestamp_ms"],
                                          "source_annotation_path": clip["annotation_path"],
                                          "source_annotation_sha256": clip["annotation_sha256"]})

    fps_by_clip = {clip_id: float(clip["fps"]) for clip_id, clip in clips.items()}
    time_group_counts = assign_time_groups(selected_box_rows, fps_by_clip)
    selected_rows_by_clip_frame: dict[tuple[str, int], list[dict[str, Any]]] = defaultdict(list)
    for row in selected_box_rows:
        selected_rows_by_clip_frame[(row["clip_id"], row["frame_index"])].append(row)

    decode_receipts = {}
    for clip_id, _requested, _role in SELECTIONS:
        clip_samples = [row for row in all_samples if row["clip_id"] == clip_id]
        rows_by_frame = {frame: selected_rows_by_clip_frame[(clip_id, frame)]
                         for frame in selected_frames[clip_id]}
        decode_receipts[clip_id] = decode_clip(clips[clip_id], clip_samples, rows_by_frame, output)

    samples_by_id = {row["sample_id"]: row for row in all_samples}
    for sample_id, sample in samples_by_id.items():
        rows = [row for row in selected_box_rows if row["sample_id"] == sample_id]
        counts = Counter(row["label"] for row in rows)
        representatives = Counter(row["label"] for row in rows
                                  if row["source_time_group_representative"])
        sample.update({
            "source_box_count": len(rows), "source_ped_box_count": counts["ped"],
            "source_vehicle_box_count": counts["vehicle"],
            "source_ignore_box_count": counts["ignore"],
            "source_ped_time_group_representatives": representatives["ped"],
            "source_vehicle_time_group_representatives": representatives["vehicle"],
        })

    box_review_rows = []
    for index, row in enumerate(sorted(selected_box_rows,
                                       key=lambda item: (item["sample_id"], item["label"], item["target_id"]))):
        box_review_rows.append({
            **row, "source_box_id": f"sb{index:05d}",
            "width": row["xmax"] - row["xmin"] + 1,
            "height": row["ymax"] - row["ymin"] + 1,
            "ignore": "true" if row["label"] == "ignore" else "false",
            "source_time_group_representative": str(row["source_time_group_representative"]).lower(),
            "source_status": "source_provided_box_not_complete_background_truth",
            "annotation_complete": "false", "training_eligible": "false",
            "formal_acceptance": "false", "human_box_status": "",
            "human_semantic_class": "", "human_model_label": "", "human_target_id": "",
            "human_xmin": "", "human_ymin": "", "human_xmax": "", "human_ymax": "",
            "human_occlusion": "", "human_truncation": "", "human_rider_pair_id": "",
            "human_ignore": "", "human_ignore_reason": "", "reviewer": "",
            "reviewed_at": "", "review_notes": "",
        })

    write_csv(output / "frame_review_manifest.csv", all_samples, FRAME_REVIEW_FIELDS)
    write_csv(output / "source_box_review.csv", box_review_rows, BOX_REVIEW_FIELDS)
    write_csv(output / "human_additions.csv", [], ADDITION_FIELDS)
    (output / "REVIEW_INSTRUCTIONS.md").write_text(instructions(), encoding="utf-8")

    scene_counts = Counter(row["camera_id"] for row in all_samples)
    frame_camera_gate = len(all_samples) >= 72 and sum(count >= 24 for count in scene_counts.values()) >= 3
    source_group_gate = all(time_group_counts.get(label, 0) >= 100 for label in ("ped", "vehicle"))
    source_inventory = {
        "license": {"receipt_path": str(LICENSE_RECEIPT),
                    "receipt_sha256": sha256(LICENSE_RECEIPT), **license_receipt},
        "canonical": {"catalog_path": str(CATALOG), "catalog_sha256": sha256(CATALOG),
                      "annotations_path": str(CANONICAL_ANNOTATIONS),
                      "annotations_sha256": sha256(CANONICAL_ANNOTATIONS)},
        "clips": [{key: clip[key] for key in (
            "clip_id", "scene_id", "development_role", "source_catalog_split", "frame_count",
            "width", "height", "fps", "video_path", "video_sha256", "annotation_path",
            "annotation_sha256", "sample_count", "physical_camera_id")}
                  for clip in clips.values()],
        "excluded_train_scenes": sorted(FORBIDDEN_TRAIN_SCENES),
        "blind_reserve_accessed": False,
        "blind_reserve_boundary": "no blind-reserve path is enumerated, opened, searched, or decoded",
    }
    write_json(output / "source_inventory.json", source_inventory)
    manifest = {
        "schema": "cnn_ground_full_frame_review_v1",
        "created_at": datetime.now().astimezone().isoformat(),
        "status": "pending_explicit_human_full_frame_annotation",
        "purpose": "development review only; no model prediction, training, or scoring",
        "selection_contract": {
            "fixed_before_predictions": True, "requires_source_ped_and_vehicle_box": True,
            "physical_camera_grouping": {
                "virat-parking-lot-camera-a": ["000200", "000203", "000205", "000207"],
                "virat-010107-camera-b": ["010107"],
                "basis": "manual visual QA of stable landmarks and identical perspective; scene_id is not treated as camera identity",
            },
            "per_clip": [{"clip_id": clip_id, "selected_frames": selected_frames[clip_id]}
                         for clip_id, _requested, _role in SELECTIONS],
            "time_group_definition": "same clip+target_id+label, greedy representatives >=2000 ms apart",
        },
        "counts": {"frames": len(all_samples), "cameras": len(scene_counts),
                   "frames_by_camera": dict(scene_counts),
                   "source_box_rows": len(selected_box_rows),
                   "source_time_groups": time_group_counts},
        "gates": {
            "at_least_72_frames_and_3_cameras_with_24_each": frame_camera_gate,
            "source_provided_100_time_groups_per_class": source_group_gate,
            "human_verified_100_time_groups_per_class": False,
            "annotation_complete": False, "training_eligible": False,
            "formal_acceptance": False,
        },
        "decode_receipts": decode_receipts,
        "frames": all_samples,
    }
    write_json(output / "ground_dev_manifest.json", manifest)

    artifact_paths = sorted(path for path in output.rglob("*") if path.is_file())
    artifact_hashes = {path.relative_to(output).as_posix(): sha256(path) for path in artifact_paths}
    write_json(output / "artifact_hashes.json", artifact_hashes)
    receipt = {
        "status": "complete_review_package_human_annotation_pending",
        "script": {"path": str(Path(__file__).resolve()), "sha256": sha256(Path(__file__))},
        "opencv_version": cv2.__version__, "artifact_count": len(artifact_hashes),
        "artifact_hashes_sha256": sha256(output / "artifact_hashes.json"),
        "frame_manifest_sha256": sha256(output / "frame_review_manifest.csv"),
        "source_box_review_sha256": sha256(output / "source_box_review.csv"),
        "ground_dev_manifest_sha256": sha256(output / "ground_dev_manifest.json"),
        "source_hashes_verified": True, "coordinates_in_range": True,
        "distinct_source_files": len({clip["video_sha256"] for clip in clips.values()}),
        "distinct_physical_cameras": len({clip["physical_camera_id"] for clip in clips.values()}),
        "train_scene_overlap": False, "blind_reserve_accessed": False,
        "full_sequential_decode_pass": True, "lossless_png_roundtrip_pass": True,
        "counts": manifest["counts"], "gates": manifest["gates"],
        "boundary": "source boxes are review hints; human completion, training eligibility, and formal acceptance remain false",
        "recovery": "never overwrite; verify with --verify-existing or rerun into a new output directory",
    }
    write_json(output / "ground_review_receipt.json", receipt)
    return {"status": receipt["status"], "frames": len(all_samples),
            "cameras": len(scene_counts), "source_time_groups": time_group_counts,
            "frame_camera_gate": frame_camera_gate, "source_group_gate": source_group_gate,
            "receipt_sha256": sha256(output / "ground_review_receipt.json")}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--output", type=Path)
    group.add_argument("--verify-existing", type=Path)
    args = parser.parse_args()
    result = build(args.output.resolve()) if args.output else verify_existing(args.verify_existing.resolve())
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
