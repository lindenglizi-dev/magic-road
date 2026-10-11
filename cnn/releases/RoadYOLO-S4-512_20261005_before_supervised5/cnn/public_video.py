"""Download fixed official VID archives or adapt local VID/MOT data.

The downloader accepts no arbitrary URL.  Conversion never treats unlabelled
pixels as background unless the selected task has official completeness evidence.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import json
from collections import Counter, defaultdict
from pathlib import Path
import shutil
import time
import urllib.error
import urllib.request
import zipfile

import cv2

try:
    from .dataset import (CLASSES, HEIGHT, WIDTH, _letterbox_720, _letterbox_transform,
                          _letterboxed_box, _refuse_blind, _write_png, audit,
                          sha256_file)
except ImportError:  # ``python cnn/public_video.py``
    from dataset import (CLASSES, HEIGHT, WIDTH, _letterbox_720, _letterbox_transform,
                         _letterboxed_box, _refuse_blind, _write_png, audit,
                         sha256_file)


# Official VisDrone MOT IDs.  Tricycles stay ignored: they are not silently
# promoted to the frozen RoadYOLO vehicle class.
VISDRONE_NAMES = {
    0: "ignored_region", 1: "pedestrian", 2: "people", 3: "bicycle",
    4: "car", 5: "van", 6: "truck", 7: "tricycle",
    8: "awning_tricycle", 9: "bus", 10: "motor", 11: "others",
}
VISDRONE_LABEL = {1: 0, 2: 0, 3: 1, 4: 1, 5: 1, 6: 1, 9: 1, 10: 1}
VISDRONE_IGNORE = {0, 7, 8, 11}
VID_VAL_URL = ("https://drive.usercontent.google.com/download?"
               "id=1xuG7Z3IhVfGGKMe3Yj6RnrFHqo_d2a1B&export=download&confirm=t")
VID_VAL_BYTES = 1_602_397_759
VID_TRAIN_URL = ("https://drive.usercontent.google.com/download?"
                 "id=1NSNapZQHar22OYzQYuXCugA3QlMndzvw&export=download&confirm=t")
VID_TRAIN_BYTES = 8_080_572_990
SPACE_RESERVE_BYTES = 20 * 1024**3


def _zip_summary(path: Path) -> dict:
    count, total = 0, 0
    with zipfile.ZipFile(path) as archive:
        for member in archive.infolist():
            parts = Path(member.filename.replace("\\", "/")).parts
            if (not parts or Path(member.filename).is_absolute() or ".." in parts or
                    ":" in parts[0] or member.is_dir() and member.file_size):
                raise ValueError(f"unsafe ZIP member: {member.filename}")
            if ((member.external_attr >> 16) & 0o170000) == 0o120000:
                raise ValueError(f"ZIP symlink is forbidden: {member.filename}")
            count += 1
            total += member.file_size
            if count > 100_000 or total > 16 * 1024**3:
                raise ValueError("unexpected VID archive expansion")
        bad = archive.testzip()
        if bad is not None:
            raise ValueError(f"ZIP CRC failure: {bad}")
    return {"zip_entries": count, "zip_uncompressed_bytes": total}


def _download_vid_archive(destination: Path, subset: str, url: str, expected_bytes: int,
                          *, timeout: int = 60) -> dict:
    """Download one fixed official VID archive, with safe resume and receipt."""
    _refuse_blind(destination)
    receipt = destination.with_suffix(destination.suffix + ".receipt.json")
    if destination.exists() or receipt.exists():
        raise FileExistsError(f"preserve existing archive/receipt: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    partial = destination.with_suffix(destination.suffix + ".part")
    for attempt in range(3):
        offset = partial.stat().st_size if partial.exists() else 0
        if offset > expected_bytes:
            raise ValueError("partial download is larger than the official archive")
        headers = {"User-Agent": "RoadYOLO-research/1"}
        if offset:
            headers["Range"] = f"bytes={offset}-"
        try:
            request = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(request, timeout=timeout) as response:
                if offset:
                    expected_range = f"bytes {offset}-"
                    if (response.status != 206 or not response.headers.get(
                            "Content-Range", "").startswith(expected_range)):
                        raise ValueError("server did not honor the safe resume offset")
                elif response.status != 200:
                    raise ValueError(f"unexpected HTTP status {response.status}")
                content_type = response.headers.get("Content-Type", "").lower()
                if "html" in content_type or "text/" in content_type:
                    raise ValueError(f"download returned {content_type}, not the archive")
                length = int(response.headers.get("Content-Length", -1))
                if length < 0 or length + offset != expected_bytes:
                    raise ValueError(f"official VID-{subset} Content-Length mismatch")
                with partial.open("ab" if partial.exists() else "xb") as output:
                    milestone = output.tell() // (128 * 1024**2)
                    while block := response.read(1024 * 1024):
                        output.write(block)
                        current = output.tell() // (128 * 1024**2)
                        if current > milestone:
                            print(f"VID-{subset}: {output.tell()}/{expected_bytes} bytes",
                                  flush=True)
                            milestone = current
            if partial.stat().st_size != expected_bytes:
                raise IOError("download ended before the declared archive size")
            summary = _zip_summary(partial)
            partial.rename(destination)
            result = {
                "kind": f"visdrone_vid_{subset}_official_download",
                "subset": subset, "url": url, "path": str(destination.resolve()),
                "bytes": expected_bytes, "sha256": sha256_file(destination),
                "completed_utc": datetime.now(timezone.utc).isoformat(), **summary,
                "purpose": ("source-declared-complete development train/validation pool; "
                            "not blind/newtest or formal-road evidence"),
                "status": "downloaded_zip_verified_not_extracted_or_converted",
            }
            receipt.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                               encoding="utf-8")
            return result
        except (OSError, urllib.error.URLError):
            if attempt == 2:
                raise
            time.sleep(attempt + 1)
    raise RuntimeError("download did not complete")


def download_vid_val(destination: Path, *, timeout: int = 60) -> dict:
    """Serialize downloads so retries cannot append to one partial concurrently."""
    return _download_vid_locked(destination, "val", VID_VAL_URL, VID_VAL_BYTES,
                                timeout=timeout)


def download_vid_train(destination: Path, *, timeout: int = 60) -> dict:
    """Download only official VID-train while preserving 20 GiB free space."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    if shutil.disk_usage(destination.parent).free < VID_TRAIN_BYTES + SPACE_RESERVE_BYTES:
        raise OSError("VID-train download would violate the 20 GiB free-space reserve")
    return _download_vid_locked(destination, "train", VID_TRAIN_URL, VID_TRAIN_BYTES,
                                timeout=timeout)


def _download_vid_locked(destination: Path, subset: str, url: str, expected_bytes: int,
                         *, timeout: int) -> dict:
    destination.parent.mkdir(parents=True, exist_ok=True)
    lock = destination.with_suffix(destination.suffix + ".lock")
    try:
        lock.touch(exist_ok=False)
    except FileExistsError as exc:
        raise FileExistsError(f"another VID-{subset} download owns {lock}") from exc
    try:
        return _download_vid_archive(destination, subset, url, expected_bytes, timeout=timeout)
    finally:
        lock.unlink(missing_ok=True)


def _extract_vid_archive(archive_path: Path, output: Path, subset: str,
                         expected_bytes: int) -> dict:
    """Extract a verified-size VID ZIP through a new staging directory."""
    for path in (archive_path, output):
        _refuse_blind(path)
    if archive_path.stat().st_size != expected_bytes:
        raise ValueError(f"VID-{subset} archive byte count mismatch")
    if output.exists():
        raise FileExistsError(f"preserve existing extraction target: {output}")
    staging = output.with_name(output.name + ".extracting")
    if staging.exists():
        raise FileExistsError(f"preserve prior extraction staging directory: {staging}")
    summary = _zip_summary(archive_path)
    if (subset == "train" and
            shutil.disk_usage(output.parent).free <
            summary["zip_uncompressed_bytes"] + SPACE_RESERVE_BYTES):
        raise OSError("VID-train extraction would violate the 20 GiB free-space reserve")
    staging.mkdir(parents=True)
    with zipfile.ZipFile(archive_path) as source:
        for member in source.infolist():
            target = staging / member.filename
            if member.is_dir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            with source.open(member) as input_stream, target.open("xb") as output_stream:
                shutil.copyfileobj(input_stream, output_stream, 1024 * 1024)
    staging.rename(output)
    result = {
        "kind": f"visdrone_vid_{subset}_extraction", "subset": subset,
        "archive": str(archive_path.resolve()),
        "archive_sha256": sha256_file(archive_path), "output": str(output.resolve()),
        "completed_utc": datetime.now(timezone.utc).isoformat(), **summary,
        "status": "extracted_not_converted",
    }
    (output / "extraction_receipt.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def extract_vid_val(archive_path: Path, output: Path) -> dict:
    return _extract_vid_archive(archive_path, output, "val", VID_VAL_BYTES)


def extract_vid_train(archive_path: Path, output: Path) -> dict:
    return _extract_vid_archive(archive_path, output, "train", VID_TRAIN_BYTES)


def read_visdrone_mot(path: Path) -> dict[int, list[dict]]:
    """Read official 1-based, ten-column VisDrone MOT ground truth."""
    rows: dict[int, list[dict]] = defaultdict(list)
    with path.open(encoding="utf-8-sig", newline="") as handle:
        for line_number, fields in enumerate(csv.reader(handle), 1):
            if not fields or not any(field.strip() for field in fields):
                continue
            if len(fields) != 10:
                raise ValueError(f"{path}:{line_number}: expected 10 columns")
            try:
                frame, target = int(fields[0]), int(fields[1])
                left, top, width, height, score = map(float, fields[2:7])
                category, truncation, occlusion = map(int, fields[7:10])
            except ValueError as exc:
                raise ValueError(f"{path}:{line_number}: invalid numeric field") from exc
            if frame < 1 or width <= 0 or height <= 0 or score not in (0, 1):
                raise ValueError(f"{path}:{line_number}: invalid frame, box, or GT score")
            if category not in VISDRONE_NAMES:
                raise ValueError(f"{path}:{line_number}: unknown category {category}")
            if truncation not in (0, 1) or occlusion not in (0, 1, 2):
                raise ValueError(f"{path}:{line_number}: invalid truncation/occlusion")
            rows[frame].append({
                "target_id": target, "bbox": [left, top, width, height],
                "score": int(score), "category": category,
                "truncation": truncation, "occlusion": occlusion,
            })
    return rows


def _sequence_images(path: Path) -> dict[int, Path]:
    images = {}
    for image in sorted(path.iterdir()):
        if not image.is_file() or image.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
            continue
        if not image.stem.isdigit():
            raise ValueError(f"non-numeric VisDrone frame name: {image}")
        frame = int(image.stem)
        if frame in images:
            raise ValueError(f"duplicate VisDrone frame index {frame}: {image}")
        images[frame] = image
    if not images:
        raise ValueError(f"no VisDrone images found: {path}")
    return images


def inspect_visdrone(root: Path) -> dict:
    """Audit extracted annotation taxonomy and structural integrity without conversion."""
    _refuse_blind(root)
    sequences, annotations = root / "sequences", root / "annotations"
    if not sequences.is_dir() or not annotations.is_dir():
        raise ValueError("expected VisDrone root with sequences/ and annotations/")
    totals, sequence_reports = Counter(), []
    total_density = {name: [] for name in CLASSES}
    for sequence in sorted(path for path in sequences.iterdir() if path.is_dir()):
        annotation = annotations / f"{sequence.name}.txt"
        if not annotation.is_file():
            raise FileNotFoundError(annotation)
        frames, rows = _sequence_images(sequence), read_visdrone_mot(annotation)
        missing = sorted(set(rows) - set(frames))
        if missing:
            raise ValueError(f"{sequence.name}: annotation references missing frames")
        ordered_frames = sorted(frames)
        probes = sorted({ordered_frames[0], ordered_frames[len(ordered_frames) // 2],
                         ordered_frames[-1]})
        dimensions = []
        for frame in probes:
            image = cv2.imread(str(frames[frame]), cv2.IMREAD_GRAYSCALE)
            if image is None:
                raise ValueError(f"cannot decode image: {frames[frame]}")
            dimensions.append([image.shape[1], image.shape[0]])
        if len({tuple(value) for value in dimensions}) != 1:
            raise ValueError(f"{sequence.name}: sampled frame dimensions differ")
        width, height = dimensions[0]
        category_score, track_categories = Counter(), defaultdict(set)
        exact_rows, invalid_bounds, rider_rows, rider_with_person_overlap = set(), 0, 0, 0
        duplicate_rows = 0
        for frame, frame_rows in rows.items():
            people = [row["bbox"] for row in frame_rows if row["category"] in {1, 2}]
            for row in frame_rows:
                key = (frame, row["target_id"], *row["bbox"], row["score"],
                       row["category"], row["truncation"], row["occlusion"])
                duplicate_rows += key in exact_rows
                exact_rows.add(key)
                category_score[(row["category"], row["score"])] += 1
                track_categories[row["target_id"]].add(row["category"])
                left, top, box_width, box_height = row["bbox"]
                invalid_bounds += not (0 <= left < left + box_width <= width and
                                       0 <= top < top + box_height <= height)
                if row["score"] and row["category"] in {3, 10}:
                    rider_rows += 1
                    box = [left, top, left + box_width, top + box_height]
                    for person in people:
                        px, py, pw, ph = person
                        intersection = max(0, min(box[2], px + pw) - max(box[0], px)) * max(
                            0, min(box[3], py + ph) - max(box[1], py))
                        if intersection > 0:
                            rider_with_person_overlap += 1
                            break
        counts = {f"{VISDRONE_NAMES[category]}:score{score}": count
                  for (category, score), count in sorted(category_score.items())}
        totals.update(counts)
        density = {name: [] for name in CLASSES}
        for frame in sorted(frames):
            frame_counts = Counter(
                VISDRONE_LABEL[row["category"]] for row in rows.get(frame, [])
                if row["score"] and row["category"] in VISDRONE_LABEL)
            for label, name in enumerate(CLASSES):
                density[name].append(frame_counts[label])
                total_density[name].append(frame_counts[label])
        density_report = {
            name: {
                "box_count": sum(values), "max_boxes_per_frame": max(values),
                "frames_over_cap32": sum(value > 32 for value in values),
                "cap32_oracle_recall": (
                    sum(min(value, 32) for value in values) / sum(values)
                    if sum(values) else None),
            }
            for name, values in density.items()
        }
        report = {
            "sequence_id": sequence.name, "image_count": len(frames),
            "frame_min": min(frames), "frame_max": max(frames),
            "annotation_rows": sum(category_score.values()),
            "annotation_sha256": sha256_file(annotation), "sampled_dimensions": dimensions,
            "category_score_counts": counts,
            "class_density_and_cap32": density_report,
            "frames_without_annotation_rows": len(set(frames) - set(rows)),
            "duplicate_rows": duplicate_rows, "boxes_outside_sampled_dimensions": invalid_bounds,
            "target_ids_with_multiple_categories": sum(
                len(categories) > 1 for categories in track_categories.values()),
            "active_bicycle_or_motor_rows": rider_rows,
            "active_bicycle_or_motor_rows_overlapping_person_box": rider_with_person_overlap,
        }
        sequence_reports.append(report)
    return {
        "kind": "visdrone_extracted_source_audit", "root": str(root.resolve()),
        "sequence_count": len(sequence_reports),
        "image_count": sum(row["image_count"] for row in sequence_reports),
        "annotation_rows": sum(row["annotation_rows"] for row in sequence_reports),
        "category_score_counts": dict(sorted(totals.items())),
        "class_density_and_cap32": {
            name: {
                "box_count": sum(values), "max_boxes_per_frame": max(values),
                "frames_over_cap32": sum(value > 32 for value in values),
                "cap32_oracle_recall": (
                    sum(min(value, 32) for value in values) / sum(values)
                    if sum(values) else None),
            }
            for name, values in total_density.items()
        },
        "rider_overlap_is_semantic_proof": False,
        "sequences": sequence_reports,
    }


def _write_reports(document: dict, output: Path, report_dir: Path,
                   name: str, provenance: dict) -> None:
    report_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "audit": report_dir / f"public_video_{name}_audit.json",
        "provenance": report_dir / f"public_video_{name}_provenance.json",
        "integrity": report_dir / f"public_video_{name}_integrity.json",
    }
    if any(path.exists() for path in paths.values()):
        raise FileExistsError(f"public-video report already exists for {name}")
    dataset_path = output / "dataset.json"
    report = audit(document, output)
    image_hashes = report.pop("image_hashes")
    paths["audit"].write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                               encoding="utf-8")
    paths["provenance"].write_text(
        json.dumps(provenance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    integrity = {"dataset": str(dataset_path.resolve()),
                 "dataset_sha256": sha256_file(dataset_path), "images": image_hashes}
    paths["integrity"].write_text(
        json.dumps(integrity, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_visdrone(root: Path, output: Path, split: str | None, report_dir: Path, *, task: str,
                   split_map: dict[str, str] | None = None,
                   stride: int = 1, max_frames_per_sequence: int = 0,
                   raw_images: bool = False) -> dict:
    """Convert an extracted official VisDrone VID/MOT split to cnn.dataset schema."""
    _refuse_blind(root)
    if task not in {"vid", "mot"}:
        raise ValueError("task must be vid or mot")
    if (split is None) == (split_map is None):
        raise ValueError("provide exactly one of split or split_map")
    if stride < 1 or max_frames_per_sequence < 0 or (split is not None and not split.strip()):
        raise ValueError("stride must be positive; max frames nonnegative; split non-empty")
    sequences, annotations = root / "sequences", root / "annotations"
    if not sequences.is_dir() or not annotations.is_dir():
        raise ValueError("expected VisDrone root with sequences/ and annotations/")
    if output.exists() and any(output.iterdir()):
        raise FileExistsError(f"output is not empty: {output}")

    images, sources = [], []
    sequence_dirs = sorted(path for path in sequences.iterdir() if path.is_dir())
    if not sequence_dirs:
        raise ValueError("no VisDrone sequence directories found")
    sequence_names = {path.name for path in sequence_dirs}
    if split_map is not None and set(split_map) != sequence_names:
        raise ValueError("split_map must name every extracted sequence exactly once")
    output.mkdir(parents=True, exist_ok=True)
    for sequence in sequence_dirs:
        sequence_split = split if split is not None else split_map[sequence.name]
        if sequence_split not in {"train", "val", "newtest"}:
            raise ValueError(f"invalid split for {sequence.name}: {sequence_split}")
        annotation = annotations / f"{sequence.name}.txt"
        if not annotation.is_file():
            raise FileNotFoundError(annotation)
        rows = read_visdrone_mot(annotation)
        frame_paths = _sequence_images(sequence)
        missing = sorted(set(rows) - set(frame_paths))
        if missing:
            raise ValueError(f"{sequence.name}: annotations reference missing frames {missing[:5]}")
        selected = sorted(frame_paths)[::stride]
        if max_frames_per_sequence:
            selected = selected[:max_frames_per_sequence]
        annotation_hash = sha256_file(annotation)
        for frame in selected:
            source = frame_paths[frame]
            bgr = cv2.imread(str(source), cv2.IMREAD_COLOR)
            if bgr is None:
                raise ValueError(f"cannot decode image: {source}")
            if raw_images:
                letterboxed = None
                transform = _letterbox_transform(bgr.shape[1], bgr.shape[0])
            else:
                letterboxed, transform = _letterbox_720(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB))
            boxes, labels, ignore_boxes = [], [], []
            box_metadata, ignore_metadata = [], []
            for row in rows.get(frame, []):
                box = _letterboxed_box(row["bbox"], transform)
                category = row["category"]
                metadata = {
                    "target_id": row["target_id"], "category_id": category,
                    "original_label": VISDRONE_NAMES[category], "score": row["score"],
                    "truncation": row["truncation"], "occlusion": row["occlusion"],
                }
                if not row["score"] or category in VISDRONE_IGNORE:
                    ignore_boxes.append(box)
                    ignore_metadata.append({
                        **metadata, "label": VISDRONE_LABEL.get(category, -1),
                        "crowd": False,
                    })
                else:
                    boxes.append(box)
                    labels.append(VISDRONE_LABEL[category])
                    box_metadata.append(metadata)
            relative = Path("images") / f"visdrone_{sequence.name}_{frame:07d}.png"
            if not raw_images:
                _write_png(letterboxed, output / relative)
            images.append({
                "image": str(source.resolve()) if raw_images else relative.as_posix(),
                "boxes": boxes, "labels": labels,
                "ignore_boxes": ignore_boxes,
                "box_metadata": box_metadata, "ignore_metadata": ignore_metadata,
                "scene_id": f"visdrone-{task}-{sequence.name}", "split": sequence_split,
                "source_sha256": sha256_file(source), "source_frame": frame,
                "source_annotation_sha256": annotation_hash,
                "incomplete_frame": task != "vid", "annotation_complete": task == "vid",
                "completeness_basis": (
                    "official_VID_ten_class_per_frame_annotation_statement"
                    if task == "vid" else "MOT_only_five_categories_evaluated"),
                "rider_box_policy_review_required": any(
                    row["category"] in {3, 10} for row in rows.get(frame, [])),
                "preprocess": {"raw_image": raw_images, "letterbox_1280x720": transform,
                               "resize": "integer.resize_area_5_to_2_RNE"},
            })
        sources.append({
            "sequence_id": sequence.name, "scene_id": f"visdrone-{task}-{sequence.name}",
            "split": sequence_split, "annotation": str(annotation.resolve()),
            "annotation_sha256": annotation_hash, "source_frame_count": len(frame_paths),
            "selected_frame_count": len(selected),
        })

    document = {
        "schema_version": 1, "task": "detection", "input_size": [WIDTH, HEIGHT],
        "classes": list(CLASSES),
        "manifest_status": ("source_declared_complete_development" if task == "vid"
                            else "diagnostic_incomplete"),
        "purpose": ("source_declared_complete_public_video_development" if task == "vid"
                    else "public_video_positive_and_ignore_development_only"),
        "training_eligible": task == "vid", "raw_images": raw_images, "images": images,
    }
    dataset_path = output / "dataset.json"
    dataset_path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n",
                            encoding="utf-8")
    provenance = {
        "adapter": f"visdrone_{task}_2019", "sources": sources,
        "official_source_url": "https://github.com/VisDrone/VisDrone-Dataset",
        "official_format_url": (
            "https://github.com/VisDrone/VisDrone2018-VID-toolkit" if task == "vid"
            else "https://github.com/VisDrone/VisDrone2018-MOT-toolkit"),
        "dataset_license_status": "not_explicitly_licensed_in_official_dataset_repository",
        "class_mapping": {str(key): (VISDRONE_LABEL[key] if key in VISDRONE_LABEL else "ignore")
                          for key in VISDRONE_NAMES},
        "rider_policy": (
            "category 2 people maps to person; bicycle/motor boxes map independently to vehicle; "
            "the adapter does not infer or synthesize a second box"),
        "completeness_evidence": (
            "official VID documentation declares ten target categories and says different objects "
            "and ignored regions are manually annotated in every frame; accepted for development "
            "training pending local mapping review" if task == "vid" else
            "official MOT documentation says objects and ignored regions are annotated per frame, "
            "but evaluates only five categories; all MOT frames remain incomplete"),
        "negative_supervision_allowed": task == "vid",
        "raw_images": raw_images,
        "formal_road_eligible": False,
        "rider_box_policy_status": "unverified_requires_local_overlay_review",
        "split_isolation": "sequence_id is the indivisible scene group",
        "split_map": ({source["sequence_id"]: source["split"] for source in sources}
                      if split_map is not None else None),
    }
    report_name = f"visdrone_{task}_{split if split is not None else 'mixed'}"
    _write_reports(document, output, report_dir,
                   report_name + ("_raw" if raw_images else ""), provenance)
    return document


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--root", type=Path, help="extracted VID/MOT root to convert")
    mode.add_argument("--inspect-visdrone", type=Path, metavar="ROOT",
                      help="audit an extracted VisDrone source without conversion")
    mode.add_argument("--download-vid-val", type=Path, metavar="ZIP")
    mode.add_argument("--extract-vid-val", type=Path, metavar="ZIP")
    mode.add_argument("--download-vid-train", type=Path, metavar="ZIP")
    mode.add_argument("--extract-vid-train", type=Path, metavar="ZIP")
    parser.add_argument("--output", type=Path)
    split_group = parser.add_mutually_exclusive_group()
    split_group.add_argument("--split", choices=("train", "val", "newtest"))
    split_group.add_argument("--split-map", type=Path,
                             help="JSON object mapping every sequence directory to a split")
    parser.add_argument("--task", choices=("vid", "mot"))
    parser.add_argument("--report-dir", type=Path, default=Path(__file__).parent / "reports")
    parser.add_argument("--stride", type=int, default=1)
    parser.add_argument("--max-frames-per-sequence", type=int, default=0)
    parser.add_argument("--raw-images", action="store_true",
                        help="reference original JPEGs instead of writing prepared PNGs")
    args = parser.parse_args()
    if args.inspect_visdrone:
        if not args.output or args.task or args.split or args.split_map or args.raw_images:
            parser.error("inspect mode requires only --inspect-visdrone ROOT --output REPORT")
        result = inspect_visdrone(args.inspect_visdrone)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as stream:
            json.dump(result, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    if args.download_vid_val:
        if args.output or args.task or args.split or args.split_map or args.raw_images:
            parser.error("download mode accepts only --download-vid-val")
        print(json.dumps(download_vid_val(args.download_vid_val), ensure_ascii=False, indent=2))
        return
    if args.download_vid_train:
        if args.output or args.task or args.split or args.split_map or args.raw_images:
            parser.error("download mode accepts only --download-vid-train")
        print(json.dumps(download_vid_train(args.download_vid_train),
                         ensure_ascii=False, indent=2))
        return
    if args.extract_vid_val:
        if not args.output or args.task or args.split or args.split_map or args.raw_images:
            parser.error("extract mode requires only --extract-vid-val ZIP --output DIR")
        print(json.dumps(extract_vid_val(args.extract_vid_val, args.output),
                         ensure_ascii=False, indent=2))
        return
    if args.extract_vid_train:
        if not args.output or args.task or args.split or args.split_map or args.raw_images:
            parser.error("extract mode requires only --extract-vid-train ZIP --output DIR")
        print(json.dumps(extract_vid_train(args.extract_vid_train, args.output),
                         ensure_ascii=False, indent=2))
        return
    if not args.output or not args.task or (args.split is None) == (args.split_map is None):
        parser.error("convert mode requires --output, --task, and exactly one split option")
    split_map = (json.loads(args.split_map.read_text(encoding="utf-8"))
                 if args.split_map else None)
    if split_map is not None and not isinstance(split_map, dict):
        raise ValueError("split-map JSON must be an object")
    result = build_visdrone(args.root, args.output, args.split, args.report_dir,
                            task=args.task, split_map=split_map, stride=args.stride,
                            max_frames_per_sequence=args.max_frames_per_sequence,
                            raw_images=args.raw_images)
    print(json.dumps(audit(result, args.output), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
