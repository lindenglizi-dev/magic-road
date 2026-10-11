#!/usr/bin/env python3
"""Deterministically sample official VIRAT tracks into FPGA-style 32x32 ROIs."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

import cv2
import numpy as np

from roi_dataset_tool import DatasetWriter, fpga_analysis_frame, fpga_resize_roi


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evenly_spaced(items: list[dict[str, str]], count: int) -> list[dict[str, str]]:
    if len(items) <= count:
        return items
    indices = np.linspace(0, len(items) - 1, count, dtype=int)
    return [items[int(index)] for index in indices]


def sample_rows(rows: list[dict[str, str]], frame_stride: int,
                max_per_track: int, max_per_scene_label: int) -> list[dict[str, str]]:
    tracks: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        if row["label"] in {"ped", "vehicle"}:
            tracks[(row["clip_id"], row["object_id"])].append(row)
    track_samples = []
    for key in sorted(tracks):
        ordered = sorted(tracks[key], key=lambda row: int(row["frame_index"]))
        thinned = []
        last_frame = -frame_stride
        for row in ordered:
            frame = int(row["frame_index"])
            if frame - last_frame >= frame_stride:
                thinned.append(row)
                last_frame = frame
        track_samples.extend(evenly_spaced(thinned, max_per_track))
    scene_labels: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in track_samples:
        scene_labels[(row["scene_id"], row["label"])].append(row)
    selected = []
    for key in sorted(scene_labels):
        ordered = sorted(scene_labels[key], key=lambda row: (
            int(row["frame_index"]), row["object_id"]))
        selected.extend(evenly_spaced(ordered, max_per_scene_label))
    return sorted(selected, key=lambda row: (
        row["split"], row["clip_id"], int(row["frame_index"]), row["object_id"]))


def analysis_box(row: dict[str, str]) -> tuple[int, int, int, int]:
    return (math.ceil(int(row["xmin"]) / 5), math.ceil(int(row["ymin"]) / 5),
            int(row["xmax"]) // 5, int(row["ymax"]) // 5)


def read_frame(cap: cv2.VideoCapture, frame_index: int) -> np.ndarray:
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
    ok, frame = cap.read()
    if not ok or frame.shape[:2] != (720, 1280):
        raise ValueError(f"could not decode 1280x720 frame {frame_index}")
    return frame


def render_contact_sheet(video: Path, rows: list[dict[str, str]], destination: Path,
                         count: int = 8) -> dict[str, object]:
    samples = evenly_spaced(rows, count)
    tile_width, tile_height, columns = 640, 480, 2
    canvas = np.full((math.ceil(len(samples) / columns) * tile_height,
                      columns * tile_width, 3), 245, np.uint8)
    cap = cv2.VideoCapture(str(video))
    review_rows = []
    try:
        for tile_index, row in enumerate(samples):
            frame_index = int(row["frame_index"])
            frame = read_frame(cap, frame_index)
            marked = frame.copy()
            source_box = tuple(int(row[key]) for key in ("xmin", "ymin", "xmax", "ymax"))
            color = (0, 220, 0) if row["label"] == "ped" else (255, 120, 0)
            cv2.rectangle(marked, source_box[:2], source_box[2:], color, 3)
            preview = cv2.resize(marked, (640, 360), interpolation=cv2.INTER_AREA)
            tile = np.full((tile_height, tile_width, 3), 245, np.uint8)
            tile[:360] = preview
            box = analysis_box(row)
            analysis = fpga_analysis_frame(frame)
            roi = fpga_resize_roi(analysis[box[1]:box[3] + 1, box[0]:box[2] + 1])
            enlarged = cv2.cvtColor(cv2.resize(roi, (96, 96), interpolation=cv2.INTER_NEAREST),
                                    cv2.COLOR_GRAY2BGR)
            tile[376:472, 8:104] = enlarged
            description = (f"frame {frame_index} {row['label']} track {row['source_object_id']} "
                           f"analysis={box}")
            cv2.putText(tile, description, (116, 420), cv2.FONT_HERSHEY_SIMPLEX,
                        .45, (20, 20, 20), 1, cv2.LINE_AA)
            cv2.putText(tile, "32x32 FPGA ROI", (116, 444), cv2.FONT_HERSHEY_SIMPLEX,
                        .45, (20, 20, 20), 1, cv2.LINE_AA)
            top, left = (tile_index // columns) * tile_height, (tile_index % columns) * tile_width
            canvas[top:top + tile_height, left:left + tile_width] = tile
            review_rows.append({
                "frame_index": frame_index,
                "object_id": row["object_id"],
                "label": row["label"],
                "source_box": list(source_box),
                "analysis_box": list(box),
                "roi_sha256": hashlib.sha256(roi.tobytes()).hexdigest(),
            })
    finally:
        cap.release()
    destination.mkdir(parents=True, exist_ok=True)
    sheet = destination / "contact_sheet.jpg"
    if not cv2.imwrite(str(sheet), canvas, [cv2.IMWRITE_JPEG_QUALITY, 94]):
        raise OSError(f"failed to write {sheet}")
    report = {
        "video": str(video.resolve()),
        "video_sha256": digest(video),
        "review_status": "pending_human_visual_check",
        "checklist": [
            "official source-frame box alignment",
            "720p to 256x144 stride-five coordinate mapping",
            "32x32 FPGA DDA ROI content and semantic label",
            "small or heavily occluded objects remain distinguishable after downsampling",
        ],
        "samples": review_rows,
        "contact_sheet_sha256": digest(sheet),
    }
    (destination / "review.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


def import_rois(canonical: Path, dataset: Path, output: Path, frame_stride: int = 30,
                max_per_track: int = 12, max_per_scene_label: int = 128,
                review_frames: int = 8) -> dict[str, object]:
    for name, path in (("dataset", dataset), ("output", output)):
        if path.exists() and any(path.iterdir()):
            raise ValueError(
                f"{name} must be a new or empty directory; refusing to overwrite an audit receipt")
    annotations_path = canonical / "annotations.csv"
    catalog_path = canonical / "catalog.json"
    with annotations_path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    acceptance = catalog.get("user_acceptance_receipt")
    acceptance_confirmed = isinstance(acceptance, dict) and acceptance.get("status") == "confirmed_by_user"
    clips = {clip["clip_id"]: clip for clip in catalog["clips"]}
    selected = sample_rows(rows, frame_stride, max_per_track, max_per_scene_label)
    if not selected:
        raise ValueError("sampling selected no ped/vehicle rows")
    by_clip: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in selected:
        by_clip[row["clip_id"]].append(row)

    decisions = []
    imported_counts: Counter[tuple[str, str, str]] = Counter()
    skipped_counts: Counter[str] = Counter()
    review_reports = {}
    for clip_id in sorted(by_clip):
        clip = clips[clip_id]
        video = Path(clip["video_path"])
        if digest(video) != clip["video_sha256"]:
            raise ValueError(f"source video changed: {clip_id}")
        if clip["split"] == "test":
            for row in by_clip[clip_id]:
                decisions.append({**{key: row[key] for key in (
                    "clip_id", "scene_id", "split", "frame_index", "label", "object_id",
                    "source_object_id", "original_label")},
                    "analysis_box": list(analysis_box(row)), "saved": False,
                    "message": "development_holdout_mapping_qa_not_imported"})
            skipped_counts["development_holdout_mapping_qa_not_imported"] += len(by_clip[clip_id])
        else:
            writer = DatasetWriter(dataset, video, clip["split"], clip["scene_id"], "annotated",
                                   "official_annotation:VIRAT_Ground_2.0")
            cap = cv2.VideoCapture(str(video))
            try:
                for row in by_clip[clip_id]:
                    frame_index = int(row["frame_index"])
                    frame = read_frame(cap, frame_index)
                    box = analysis_box(row)
                    before = len(writer.rows)
                    result = writer.save(fpga_analysis_frame(frame), frame_index, float(clip["fps"]),
                                         (1280, 720), box, row["label"])
                    record = {key: row[key] for key in (
                        "clip_id", "scene_id", "split", "frame_index", "label", "object_id",
                        "source_object_id", "original_label")}
                    record.update({"analysis_box": list(box), "saved": result.saved,
                                   "message": result.message})
                    if result.saved:
                        record["sample_id"] = writer.rows[-1]["sample_id"]
                        imported_counts[(clip["split"], clip["scene_id"], row["label"])] += 1
                    else:
                        skipped_counts[result.message] += 1
                    if len(writer.rows) < before:
                        raise AssertionError("dataset writer unexpectedly removed rows")
                    decisions.append(record)
            finally:
                cap.release()
        review_reports[clip_id] = render_contact_sheet(
            video, by_clip[clip_id], output / "reviews" / clip_id, review_frames)

    output.mkdir(parents=True, exist_ok=True)
    selection_fields = [
        "clip_id", "scene_id", "split", "frame_index", "label", "object_id",
        "source_object_id", "original_label", "analysis_box", "saved", "message", "sample_id",
    ]
    with (output / "selected_annotations.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, selection_fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(decisions)
    report = {
        "status": "pilot_import_complete_pending_human_contact_sheet_review",
        "scope": "isolated official VIRAT Ground 2.0 train/val ROI pilot",
        "dataset_root": str(dataset.resolve()),
        "dataset_boundary": "use road_roi_dataset_virat for VIRAT work; road_roi_dataset is a combined legacy pilot and must not be used as a VIRAT-only evaluation set",
        "test_boundary": "split=test is a development holdout already viewed for coordinate/ROI/semantic mapping QA; it is not imported, trained on or scored, but it is not a blind final test and must not be used for formal claims",
        "canonical_catalog_sha256": digest(catalog_path),
        "canonical_annotations_sha256": digest(annotations_path),
        "usage_agreement_receipt": acceptance,
        "sampling": {
            "frame_stride": frame_stride,
            "max_per_track": max_per_track,
            "max_per_scene_label": max_per_scene_label,
            "algorithm": "thin each track by zero-based frame distance, evenly cap per track, then evenly cap per scene/label",
            "reason": "avoid adjacent frames and long/static tracks overwhelming the small pilot",
        },
        "selected_annotation_count": len(selected),
        "imported_count": sum(imported_counts.values()),
        "imported_by_split_scene_label": {
            "/".join(key): value for key, value in sorted(imported_counts.items())},
        "skipped_counts": dict(sorted(skipped_counts.items())),
        "selected_annotations_sha256": digest(output / "selected_annotations.csv"),
        "review_status": {clip: value["review_status"] for clip, value in sorted(review_reports.items())},
        "limitations": [
            "human review of every contact sheet remains required",
            ("VIRAT usage-agreement acceptance is recorded in the canonical catalog"
             if acceptance_confirmed else
             "VIRAT usage-agreement acceptance receipt remains pending user confirmation"),
            "reviewed distant pedestrians can be only 2-6 pixels wide in the 256x144 analysis image, which is a model-capability limit",
            "official boxes test classification input only; CCL candidate quality is a separate experiment",
            "split=test is a viewed development holdout with selection metadata/contact sheets only; a new unseen scene is required for final blind test",
            "binary classifier has no invalid-candidate rejection path",
        ],
    }
    (output / "import_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--frame-stride", type=int, default=30)
    parser.add_argument("--max-per-track", type=int, default=12)
    parser.add_argument("--max-per-scene-label", type=int, default=128)
    parser.add_argument("--review-frames", type=int, default=8)
    args = parser.parse_args()
    for name in ("frame_stride", "max_per_track", "max_per_scene_label", "review_frames"):
        if getattr(args, name) < 1:
            raise ValueError(f"--{name.replace('_', '-')} must be positive")
    report = import_rois(args.canonical.resolve(), args.dataset.resolve(), args.output.resolve(),
                         args.frame_stride, args.max_per_track,
                         args.max_per_scene_label, args.review_frames)
    print(json.dumps({key: report[key] for key in (
        "status", "selected_annotation_count", "imported_count",
        "imported_by_split_scene_label", "skipped_counts")}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
