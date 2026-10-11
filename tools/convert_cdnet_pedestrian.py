"""Convert the official CDnet pedestrian-box subset to canonical CSV files.

CDnet rows are ``frameID 0 x y width height``.  ``frameID`` is one-based and
the box values may be half-pixels.  The canonical files use zero-based frame
indices and inclusive integer boxes which conservatively enclose the source
rectangle.  CDnet does not provide track identities, so ``object_id`` is only
a stable per-frame annotation identifier and must not be used as a track ID.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from collections import Counter
from pathlib import Path

import cv2


SOURCE_URL = (
    "https://changedetection.net/static/pedestrian%20detection/"
    "pedestrian%20detection%20dataset.zip"
)
ANNOTATION_URL = (
    "https://changedetection.net/static/pedestrian%20detection/"
    "pedestrian%20detection%20groundtruth.zip"
)
LICENSE_URL = "https://changedetection.net/dataset2014/"

# Chosen before looking at classifier results.  Each sequence is one scene.
DEFAULT_SPLITS = {
    "train": ["backdoor", "busStation", "copyMachine", "cubicle", "office", "pedestrians"],
    "val": ["peopleInShade", "skating"],
    "test": ["PETS2006", "sofa"],
}

FIELDS = [
    "frame_index", "xmin", "ymin", "xmax", "ymax", "label",
    "original_label", "object_id", "source_frame_id", "source_x",
    "source_y", "source_width", "source_height", "mapping_note",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_row(line: str, line_number: int) -> dict[str, object]:
    values = line.split()
    if len(values) != 6:
        raise ValueError(f"line {line_number}: expected 6 fields, got {len(values)}")
    frame_text, reserved_text, x_text, y_text, width_text, height_text = values
    try:
        frame_id = int(frame_text)
        reserved = int(reserved_text)
        x, y, width, height = map(float, (x_text, y_text, width_text, height_text))
    except ValueError as error:
        raise ValueError(f"line {line_number}: invalid number") from error
    if frame_id < 1:
        raise ValueError(f"line {line_number}: CDnet frameID must be one-based")
    if reserved != 0:
        raise ValueError(f"line {line_number}: reserved field must be zero")
    if not all(math.isfinite(value) for value in (x, y, width, height)):
        raise ValueError(f"line {line_number}: non-finite box")
    if x < 0 or y < 0 or width <= 0 or height <= 0:
        raise ValueError(f"line {line_number}: invalid box")
    xmin, ymin = math.floor(x), math.floor(y)
    xmax, ymax = math.ceil(x + width) - 1, math.ceil(y + height) - 1
    if xmax < xmin or ymax < ymin:
        raise ValueError(f"line {line_number}: empty mapped box")
    return {
        "frame_index": frame_id - 1,
        "xmin": xmin,
        "ymin": ymin,
        "xmax": xmax,
        "ymax": ymax,
        "label": "ped",
        "original_label": "pedestrian",
        "source_frame_id": frame_id,
        "source_x": x_text,
        "source_y": y_text,
        "source_width": width_text,
        "source_height": height_text,
        "mapping_note": "floor(x,y); ceil(x+width,y+height)-1; source frameID-1",
    }


def load_splits(path: Path | None) -> dict[str, list[str]]:
    splits = DEFAULT_SPLITS if path is None else json.loads(path.read_text(encoding="utf-8"))
    if set(splits) != {"train", "val", "test"}:
        raise ValueError("split file must contain exactly train, val and test")
    flattened = [sequence for split in ("train", "val", "test") for sequence in splits[split]]
    if len(flattened) != len(set(flattened)):
        raise ValueError("a sequence appears in more than one split")
    return {split: list(splits[split]) for split in ("train", "val", "test")}


def find_gt_files(root: Path) -> dict[str, Path]:
    files = {}
    for path in root.rglob("gt.txt"):
        sequence = path.parent.name
        if sequence in files:
            raise ValueError(f"duplicate gt.txt for sequence {sequence}")
        files[sequence] = path
    if not files:
        raise ValueError("no CDnet gt.txt files found")
    return files


def find_sequence(root: Path, sequence: str) -> Path:
    candidates = [path for path in root.rglob(sequence) if path.is_dir()]
    candidates = [path for path in candidates if (path / "input").is_dir()]
    if len(candidates) != 1:
        raise ValueError(f"expected exactly one image sequence {sequence}, found {len(candidates)}")
    return candidates[0] / "input"


def frame_numbers(image_dir: Path) -> dict[int, Path]:
    numbers = {}
    for path in image_dir.iterdir():
        if path.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
            continue
        digits = "".join(character for character in path.stem if character.isdigit())
        if not digits:
            raise ValueError(f"cannot read frame number from {path.name}")
        number = int(digits)
        if number in numbers:
            raise ValueError(f"duplicate frame number {number} in {image_dir}")
        numbers[number] = path
    if not numbers:
        raise ValueError(f"no images in {image_dir}")
    return numbers


def convert(annotations_root: Path, images_root: Path, output: Path,
            split_path: Path | None = None) -> dict[str, object]:
    if output.exists():
        raise ValueError("use a new output directory")
    splits = load_splits(split_path)
    split_by_sequence = {sequence: split for split, sequences in splits.items() for sequence in sequences}
    gt_files = find_gt_files(annotations_root)
    if set(gt_files) != set(split_by_sequence):
        missing = sorted(set(split_by_sequence) - set(gt_files))
        extra = sorted(set(gt_files) - set(split_by_sequence))
        raise ValueError(f"annotation/split sequence mismatch; missing={missing}, extra={extra}")
    output.mkdir(parents=True)
    catalog = {
        "dataset": "CDnet 2014 pedestrian detection subset",
        "source_url": SOURCE_URL,
        "annotation_url": ANNOTATION_URL,
        "license_and_citation_url": LICENSE_URL,
        "frame_index_contract": "source frameID is 1-based; canonical frame_index is frameID-1",
        "box_contract": "source x/y/width/height may be fractional; canonical inclusive box encloses it",
        "identity_contract": "object_id is per-frame annotation identity, not a track identity",
        "class_mapping": {"pedestrian": "ped"},
        "negative_policy": "unannotated regions are not invalid samples",
        "splits": splits,
        "sequences": [],
    }
    for sequence in sorted(gt_files):
        image_dir = find_sequence(images_root, sequence)
        available_frames = frame_numbers(image_dir)
        first_image = cv2.imread(str(available_frames[min(available_frames)]), cv2.IMREAD_GRAYSCALE)
        if first_image is None:
            raise ValueError(f"cannot read first image in {image_dir}")
        image_height, image_width = first_image.shape
        rows = []
        excluded = []
        clipped_to_image = 0
        sanitized_trailing_del = 0
        frame_occurrences: Counter[int] = Counter()
        for line_number, line in enumerate(gt_files[sequence].read_text(encoding="utf-8-sig").splitlines(), 1):
            if not line.strip():
                continue
            cleaned = line.rstrip("\x7f")
            sanitized_trailing_del += int(cleaned != line)
            if any(ord(character) < 32 or ord(character) == 127 for character in cleaned):
                raise ValueError(f"{sequence} line {line_number}: unsupported control character")
            row = parse_row(cleaned, line_number)
            source_frame = int(row["source_frame_id"])
            if source_frame not in available_frames:
                raise ValueError(f"{sequence} line {line_number}: image frame {source_frame} is missing")
            original_box = tuple(int(row[key]) for key in ("xmin", "ymin", "xmax", "ymax"))
            clipped_box = (max(0, original_box[0]), max(0, original_box[1]),
                           min(image_width - 1, original_box[2]), min(image_height - 1, original_box[3]))
            if clipped_box[0] > clipped_box[2] or clipped_box[1] > clipped_box[3]:
                excluded.append({**row, "exclusion_reason": "source_box_has_no_image_intersection"})
                continue
            if clipped_box != original_box:
                clipped_to_image += 1
                for key, value in zip(("xmin", "ymin", "xmax", "ymax"), clipped_box):
                    row[key] = value
                row["mapping_note"] += "; clipped_to_image"
            occurrence = frame_occurrences[source_frame]
            frame_occurrences[source_frame] += 1
            row["object_id"] = f"cdnet-{sequence}-{source_frame:06d}-{occurrence:03d}"
            rows.append(row)
        if not rows:
            raise ValueError(f"no annotations in {gt_files[sequence]}")
        sequence_output = output / sequence
        sequence_output.mkdir()
        csv_path = sequence_output / "annotations.csv"
        with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, FIELDS)
            writer.writeheader()
            writer.writerows(rows)
        if excluded:
            excluded_fields = FIELDS + ["exclusion_reason"]
            with (sequence_output / "excluded_annotations.csv").open(
                    "w", encoding="utf-8-sig", newline="") as handle:
                writer = csv.DictWriter(handle, excluded_fields)
                writer.writeheader()
                writer.writerows(excluded)
        catalog["sequences"].append({
            "sequence_id": sequence,
            "scene_id": f"cdnet2014-ped-{sequence}",
            "split": split_by_sequence[sequence],
            "image_directory": str(image_dir.resolve()),
            "image_count": len(available_frames),
            "image_width": image_width,
            "image_height": image_height,
            "annotation_count": len(rows),
            "source_annotation_count": len(rows) + len(excluded),
            "annotated_frame_count": len(frame_occurrences),
            "first_source_frame": min(frame_occurrences),
            "last_source_frame": max(frame_occurrences),
            "sanitized_trailing_ascii_del": sanitized_trailing_del,
            "clipped_to_image_count": clipped_to_image,
            "excluded_no_intersection_count": len(excluded),
            "gt_sha256": sha256(gt_files[sequence]),
            "canonical_sha256": sha256(csv_path),
        })
    catalog["totals"] = {
        "sequences": len(catalog["sequences"]),
        "images": sum(item["image_count"] for item in catalog["sequences"]),
        "annotations": sum(item["annotation_count"] for item in catalog["sequences"]),
        "source_annotations": sum(item["source_annotation_count"] for item in catalog["sequences"]),
        "clipped_to_image": sum(item["clipped_to_image_count"] for item in catalog["sequences"]),
        "excluded_no_intersection": sum(item["excluded_no_intersection_count"] for item in catalog["sequences"]),
        "annotated_frames": sum(item["annotated_frame_count"] for item in catalog["sequences"]),
    }
    (output / "catalog.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")
    return catalog


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--annotations-root", type=Path, required=True)
    parser.add_argument("--images-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True, help="new directory")
    parser.add_argument("--splits", type=Path, help="optional JSON train/val/test sequence map")
    args = parser.parse_args()
    result = convert(args.annotations_root, args.images_root, args.output, args.splits)
    print(json.dumps(result["totals"], ensure_ascii=False))


if __name__ == "__main__":
    main()
