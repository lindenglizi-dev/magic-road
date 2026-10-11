#!/usr/bin/env python3
"""Convert selected official VIRAT Ground 2.0 object tracks to canonical boxes.

The Release 2 object files use zero-based ``current frame`` values.  A small
number of official rows point one frame beyond the corresponding MP4; those
rows are preserved in ``excluded_annotations.csv`` rather than shifted.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

import cv2


COLLECTION_URL = "https://data.kitware.com/#collection/56f56db28d777f753209ba9f/folder/56f57e748d777f753209bed7"
ANNOTATIONS_FOLDER_ID = "56f57e748d777f753209bed8"
VIDEOS_FOLDER_ID = "56f581ce8d777f753209ca43"
README_ITEM_ID = "56f581c78d777f753209c9c6"
USAGE_AGREEMENT_URL = "https://viratdata.org/resources/VIRAT-Video-Data-Set-Protection-Agreement-1-4-11.pdf"
ITEM_IDS = {
    "000200": ("56f5851c8d777f753209ca59", "56f57e958d777f753209bf1e"),
    "000201": ("56f585ec8d777f753209ca74", "56f57ea18d777f753209bf63"),
    "000203": ("56f586ac8d777f753209ca8c", "56f57ea98d777f753209bfa5"),
    "000205": ("56f586ea8d777f753209caa1", "56f57eab8d777f753209bfd8"),
    "000206": ("56f587318d777f753209cab3", "56f57ead8d777f753209c002"),
    "000207": ("56f587628d777f753209cac2", "56f57eb68d777f753209c02f"),
}
EXPECTED_VIDEOS = {
    "000200": (72268926, "a8888e14bb2a1d38368a10cfd949916fcf9acc9972d3dacc3cbbc502c8d8a568"),
    "000201": (34169120, "b6233ba6fdae9acf5cc516f15e41b6e4c912387ee3713bb9fd9c8c6c30385dfa"),
    "000203": (51811369, "c85ced4e6984bb4a2d97109a7f9e45cf7b398530c0eebc0eba3dcd30c68477ad"),
    "000205": (87292888, "c2e88327b276dec145537d6c7dad7fee44f388f41ad93c69c3255527eaa6da37"),
    "000206": (95474104, "9a78a0fc6c1ffe4579229c6f8b17acd28eed9aaf33d9fd1147f8c07092cacc00"),
    "000207": (32906093, "f17a1165984444b242199a8190d1f0fe6a83c6ea0c07b54c1c3ab633539b4571"),
}
EXPECTED_ANNOTATIONS = {
    "000200": (96114, "05b8969837d64d10d48d1b8018ad3b56dc18b8743afcc71f1170668faeb82f0c"),
    "000201": (142771, "1b809d77d94fa4976ec6d856b84fb2a18deb50917849cf25bbc1962967488243"),
    "000203": (86896, "8b1b43949b0e76552ddf68d578d8452abe6f4393d5c253d9ba5be2a4a699abed"),
    "000205": (119159, "3bcc93823aff5656759fd51ea27e493ebd3a2a2e594d0e681d4df77235bb96c7"),
    "000206": (1551906, "d9baf1ac94d4e96ecdb8ba5c7b375205e32f398a89020e32e821bc07fd548e1a"),
    "000207": (42749, "88ea1f696908e09e6c782b05ee427e1736b848cd286e5dc6d6ddf5b778f70bbc"),
}
EXPECTED_README = (3832, "fc5833e57280512bcb7e19674b9def83c02a8ce324bf783bfbfb778d5d105f40")
SPLITS = {
    "train": ("000201", "000206"),
    "val": ("000200", "000203"),
    "test": ("000205", "000207"),
}
SPLIT_BY_SCENE = {scene: split for split, scenes in SPLITS.items() for scene in scenes}
TYPE_LABEL = {0: "ignore", 1: "ped", 2: "vehicle", 3: "vehicle", 4: "ignore", 5: "ignore"}
TYPE_NAME = {0: "undocumented_type_0", 1: "person", 2: "car", 3: "other_vehicle",
             4: "object", 5: "bike_or_bicycle"}
FIELDS = [
    "clip_id", "scene_id", "split", "frame_index", "xmin", "ymin", "xmax", "ymax",
    "label", "original_label", "original_type", "object_id", "source_object_id",
    "object_duration", "source_x", "source_y", "source_width", "source_height",
    "source_annotation_line",
]
EXCLUDED_FIELDS = FIELDS + ["reason"]
CLIP_RE = re.compile(r"^VIRAT_S_(\d{6})_.*$")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_acceptance_receipt(root: Path) -> dict[str, object] | None:
    path = root / "docs" / "user_acceptance_receipt.json"
    if not path.is_file():
        return None
    receipt = json.loads(path.read_text(encoding="utf-8"))
    if receipt.get("accepted") is not True:
        raise ValueError("VIRAT usage receipt must explicitly record accepted=true")
    if receipt.get("agreement_url") != USAGE_AGREEMENT_URL:
        raise ValueError("VIRAT usage receipt references a different agreement")
    for field in ("confirmation_date", "confirmation_source"):
        if not isinstance(receipt.get(field), str) or not receipt[field].strip():
            raise ValueError(f"VIRAT usage receipt missing {field}")
    return {
        "status": "confirmed_by_user",
        "confirmation_date": receipt["confirmation_date"],
        "confirmation_source": receipt["confirmation_source"],
        "receipt_path": str(path.resolve()),
        "receipt_sha256": digest(path),
    }


def download_url(item_id: str) -> str:
    return f"https://data.kitware.com/api/v1/item/{item_id}/download"


def video_directory(root: Path) -> Path:
    candidates = [root / name for name in ("video_original", "videos_original")
                  if (root / name).is_dir()]
    if len(candidates) != 1:
        raise ValueError("expected exactly one of video_original or videos_original")
    return candidates[0]


def scene_from_clip(clip_id: str) -> str:
    match = CLIP_RE.match(clip_id)
    if not match or match.group(1) not in SPLIT_BY_SCENE:
        raise ValueError(f"unexpected VIRAT clip id: {clip_id}")
    return match.group(1)


def video_metadata(path: Path) -> dict[str, object]:
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise ValueError(f"cannot open video: {path}")
    try:
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = float(cap.get(cv2.CAP_PROP_FPS))
        if frame_count <= 0 or (width, height) != (1280, 720) or not math.isclose(fps, 30.0, abs_tol=0.05):
            raise ValueError(f"unexpected video metadata: {path.name}: {frame_count}, {width}x{height}, {fps}")
        for frame_index in sorted({0, frame_count // 2, frame_count - 1}):
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
            ok, frame = cap.read()
            if not ok or frame.shape[:2] != (height, width):
                raise ValueError(f"cannot decode frame {frame_index}: {path.name}")
        return {"frame_count": frame_count, "width": width, "height": height, "fps": fps}
    finally:
        cap.release()


def parse_object_line(line: str, line_number: int) -> tuple[int, ...]:
    fields = line.split()
    if len(fields) != 8:
        raise ValueError(f"line {line_number}: expected 8 integer columns")
    try:
        values = tuple(int(value) for value in fields)
    except ValueError as exc:
        raise ValueError(f"line {line_number}: non-integer field") from exc
    object_id, duration, frame, x, y, width, height, _ = values
    if object_id < 0 or duration < 1 or frame < 0 or width < 1 or height < 1:
        raise ValueError(f"line {line_number}: invalid identity/frame/geometry")
    return values


def convert(root: Path, output: Path) -> dict[str, object]:
    root = root.resolve()
    videos = video_directory(root)
    annotations = root / "annotations"
    readme = root / "docs" / "README_format_release2.txt"
    if not annotations.is_dir() or not readme.is_file():
        raise ValueError("missing official VIRAT annotations or Release 2 format README")
    acceptance_receipt = load_acceptance_receipt(root)
    readme_hash = digest(readme)
    if readme.stat().st_size != EXPECTED_README[0] or readme_hash != EXPECTED_README[1]:
        raise ValueError("official Release 2 README identity mismatch")

    video_files = {path.stem: path for path in videos.glob("*.mp4")}
    annotation_files = {
        path.name.removesuffix(".viratdata.objects.txt"): path
        for path in annotations.glob("*.viratdata.objects.txt")
    }
    if set(video_files) != set(annotation_files) or len(video_files) != 6:
        raise ValueError("the six video/object-file stems must match exactly")
    if {scene_from_clip(clip) for clip in video_files} != set(SPLIT_BY_SCENE):
        raise ValueError("VIRAT clip set does not match the frozen six-scene split")

    output.mkdir(parents=True, exist_ok=True)
    canonical_rows: list[dict[str, object]] = []
    excluded_rows: list[dict[str, object]] = []
    clips = []
    all_type_counts: Counter[int] = Counter()
    for clip_id in sorted(video_files):
        scene = scene_from_clip(clip_id)
        split = SPLIT_BY_SCENE[scene]
        video = video_files[clip_id]
        annotation = annotation_files[clip_id]
        expected_size, expected_hash = EXPECTED_VIDEOS[scene]
        actual_hash = digest(video)
        if video.stat().st_size != expected_size or actual_hash != expected_hash:
            raise ValueError(
                f"official video identity mismatch: {video.name}: "
                f"size={video.stat().st_size}, sha256={actual_hash}")
        expected_annotation_size, expected_annotation_hash = EXPECTED_ANNOTATIONS[scene]
        actual_annotation_hash = digest(annotation)
        if (annotation.stat().st_size != expected_annotation_size or
                actual_annotation_hash != expected_annotation_hash):
            raise ValueError(
                f"official annotation identity mismatch: {annotation.name}: "
                f"size={annotation.stat().st_size}, sha256={actual_annotation_hash}")
        metadata = video_metadata(video)
        type_counts: Counter[int] = Counter()
        kept_counts: Counter[str] = Counter()
        excluded_counts: Counter[str] = Counter()
        track_types: dict[int, int] = {}
        track_durations: dict[int, int] = {}
        for line_number, text in enumerate(annotation.read_text(encoding="utf-8-sig").splitlines(), 1):
            if not text.strip():
                continue
            object_number, duration, frame, x, y, width, height, object_type = parse_object_line(text, line_number)
            type_counts[object_type] += 1
            all_type_counts[object_type] += 1
            if object_number in track_types and track_types[object_number] != object_type:
                raise ValueError(f"{clip_id}: track {object_number} changes object type")
            if object_number in track_durations and track_durations[object_number] != duration:
                raise ValueError(f"{clip_id}: track {object_number} changes declared duration")
            track_types[object_number] = object_type
            track_durations[object_number] = duration
            label = TYPE_LABEL.get(object_type, "ignore")
            xmax, ymax = x + width - 1, y + height - 1
            row = {
                "clip_id": clip_id,
                "scene_id": f"virat-ground-{scene}",
                "split": split,
                "frame_index": frame,
                "xmin": x, "ymin": y, "xmax": xmax, "ymax": ymax,
                "label": label,
                "original_label": TYPE_NAME.get(object_type, f"unknown_type_{object_type}"),
                "original_type": object_type,
                "object_id": f"{clip_id}:track-{object_number}",
                "source_object_id": object_number,
                "object_duration": duration,
                "source_x": x, "source_y": y, "source_width": width, "source_height": height,
                "source_annotation_line": line_number,
            }
            if frame >= int(metadata["frame_count"]):
                excluded_counts["frame_out_of_range"] += 1
                excluded_rows.append({**row, "reason": "frame_out_of_range"})
                continue
            if xmax < 0 or ymax < 0 or x >= int(metadata["width"]) or y >= int(metadata["height"]):
                excluded_counts["box_no_frame_intersection"] += 1
                excluded_rows.append({**row, "reason": "box_no_frame_intersection"})
                continue
            if x < 0 or y < 0 or xmax >= int(metadata["width"]) or ymax >= int(metadata["height"]):
                excluded_counts["box_requires_clipping"] += 1
                excluded_rows.append({**row, "reason": "box_requires_clipping"})
                continue
            canonical_rows.append(row)
            kept_counts[label] += 1

        video_item, annotation_item = ITEM_IDS[scene]
        clips.append({
            "clip_id": clip_id,
            "scene_id": f"virat-ground-{scene}",
            "split": split,
            **metadata,
            "video_path": str(video),
            "annotation_path": str(annotation),
            "video_sha256": actual_hash,
            "expected_video_bytes": expected_size,
            "official_video_identity_check": "pass_expected_size_and_sha256",
            "annotation_sha256": actual_annotation_hash,
            "expected_annotation_bytes": expected_annotation_size,
            "official_annotation_identity_check": "pass_expected_size_and_sha256",
            "video_item_id": video_item,
            "annotation_item_id": annotation_item,
            "video_download_url": download_url(video_item),
            "annotation_download_url": download_url(annotation_item),
            "source_annotation_rows": sum(type_counts.values()),
            "kept_annotation_rows": sum(kept_counts.values()),
            "excluded_annotation_rows": sum(excluded_counts.values()),
            "type_counts": {str(key): value for key, value in sorted(type_counts.items())},
            "label_counts": dict(sorted(kept_counts.items())),
            "track_counts": {str(key): value for key, value in sorted(Counter(track_types.values()).items())},
            "excluded_counts": dict(sorted(excluded_counts.items())),
        })

    with (output / "annotations.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, FIELDS)
        writer.writeheader()
        writer.writerows(canonical_rows)
    with (output / "excluded_annotations.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, EXCLUDED_FIELDS)
        writer.writeheader()
        writer.writerows(excluded_rows)
    catalog = {
        "dataset": "VIRAT Ground Dataset Release 2.0",
        "status": ("pilot_research_files_present_usage_acceptance_recorded"
                   if acceptance_receipt else
                   "pilot_research_files_present_usage_acceptance_pending"),
        "collection_url": COLLECTION_URL,
        "videos_folder_id": VIDEOS_FOLDER_ID,
        "annotations_folder_id": ANNOTATIONS_FOLDER_ID,
        "readme_item_id": README_ITEM_ID,
        "readme_download_url": download_url(README_ITEM_ID),
        "readme_sha256": readme_hash,
        "expected_readme_bytes": EXPECTED_README[0],
        "official_readme_identity_check": "pass_expected_size_and_sha256",
        "usage_agreement": "VIRAT Video Dataset Usage Agreement, 1-4-11",
        "usage_agreement_url": USAGE_AGREEMENT_URL,
        "user_acceptance_receipt": acceptance_receipt or "pending_user_confirmation",
        "license_boundary": "do not claim redistributable or license-complete; each accessor must accept the official agreement and redistribution to non-accepting third parties is prohibited",
        "frame_index_contract": "official current_frame is zero-based; values >= decoded frame_count are excluded without shifting",
        "box_contract": "official x/y/width/height converted to inclusive xmin/ymin/xmax/ymax; valid rows require full 1280x720 containment",
        "class_mapping": {
            "0": "ignore (present in annotations but undocumented by Release 2 README)",
            "1": "ped", "2": "vehicle", "3": "vehicle", "4": "ignore", "5": "ignore",
        },
        "findings": [
            "type 0 is not defined in README_format_release2.txt; it is preserved and mapped to ignore",
            "out-of-range terminal annotation rows are preserved in excluded_annotations.csv",
            "split=test scenes were viewed for mapping QA and are development holdout only; final blind test requires new unseen scenes",
            ("local user acceptance of the official usage agreement is recorded"
             if acceptance_receipt else
             "local user acceptance of the official usage agreement has not been recorded"),
        ],
        "splits": {key: list(value) for key, value in SPLITS.items()},
        "canonical_annotation_count": len(canonical_rows),
        "excluded_annotation_count": len(excluded_rows),
        "type_counts": {str(key): value for key, value in sorted(all_type_counts.items())},
        "clips": clips,
    }
    (output / "catalog.json").write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return catalog


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True,
                        help="directory containing video(s)_original, annotations and docs")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = convert(args.root, args.output)
    print(json.dumps({
        "canonical_annotation_count": result["canonical_annotation_count"],
        "excluded_annotation_count": result["excluded_annotation_count"],
        "splits": result["splits"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
