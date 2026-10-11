"""Convert a grouped UA-DETRAC-derived YOLO mirror sample to canonical CSV.

This adapter is deliberately marked pilot-only: the selected mirror resized
native 960x540 frames to 640x640 and may contain augmentation.  It must not be
reported as evaluation on the original UA-DETRAC images.  All files from one
source sequence remain in one local split regardless of the mirror's split.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
import shutil
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

import cv2


DATASET_URL = "https://huggingface.co/datasets/thundarstrom/traffic-vehicle-detection"
LICENSE_URL = DATASET_URL + "/blob/main/README.md"
ALLOWED_ORIGINAL_LABELS = {"car", "bus", "truck", "van", "others"}
FIELDS = [
    "frame_index", "xmin", "ymin", "xmax", "ymax", "label",
    "original_label", "object_id", "source_sequence_id", "source_frame_id",
    "mirror_image_name", "augmentation_id", "source_yolo_line",
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def identity(path: Path) -> tuple[str, int, str]:
    match = re.fullmatch(r"(MVI_\d+)_img(\d+)_jpg\.rf\.([0-9a-f]+)", path.stem)
    if not match:
        raise ValueError(f"unsupported mirror filename: {path.name}")
    return match.group(1), int(match.group(2)), match.group(3)


def yolo_box(line: str, width: int, height: int, line_number: int,
             class_map: dict[int, str]) -> tuple[str, tuple[int, int, int, int]]:
    fields = line.split()
    if len(fields) != 5:
        raise ValueError(f"YOLO line {line_number}: expected 5 fields")
    try:
        class_id = int(fields[0])
        center_x, center_y, box_width, box_height = map(float, fields[1:])
    except ValueError as error:
        raise ValueError(f"YOLO line {line_number}: invalid value") from error
    if class_id not in class_map:
        raise ValueError(f"YOLO line {line_number}: unsupported class {class_id}")
    if not all(math.isfinite(value) for value in (center_x, center_y, box_width, box_height)):
        raise ValueError(f"YOLO line {line_number}: non-finite box")
    if not (0 <= center_x <= 1 and 0 <= center_y <= 1 and 0 < box_width <= 1 and 0 < box_height <= 1):
        raise ValueError(f"YOLO line {line_number}: normalized box outside contract")
    xmin = max(0, math.floor((center_x - box_width / 2) * width))
    ymin = max(0, math.floor((center_y - box_height / 2) * height))
    xmax = min(width - 1, math.ceil((center_x + box_width / 2) * width) - 1)
    ymax = min(height - 1, math.ceil((center_y + box_height / 2) * height) - 1)
    if xmin > xmax or ymin > ymax:
        raise ValueError(f"YOLO line {line_number}: empty box")
    return class_map[class_id], (xmin, ymin, xmax, ymax)


def official_frame_counts(path: Path) -> dict[int, Counter[str]]:
    root = ET.parse(path).getroot()
    result = {}
    for frame in root.findall("frame"):
        result[int(frame.attrib["num"])] = Counter(
            target.find("attribute").attrib["vehicle_type"]
            for target in frame.findall("./target_list/target"))
    return result


def convert(source: Path, output: Path, sequence_id: str, class_map: dict[int, str],
            split: str = "train", official_xml: Path | None = None) -> dict[str, object]:
    if split not in {"train", "val", "test"}:
        raise ValueError("split must be train, val or test")
    if output.exists():
        raise ValueError("use a new output directory")
    if set(class_map) != {0, 1, 2, 3} or not set(class_map.values()) <= ALLOWED_ORIGINAL_LABELS:
        raise ValueError("class map must explicitly map IDs 0..3 to known original labels")
    image_dir, label_dir = source / "images", source / "labels"
    images = sorted(image_dir.glob("*.jpg"), key=lambda path: identity(path)[1:])
    if not images:
        raise ValueError("no mirror JPG files")
    records = []
    seen_frames = set()
    for image in images:
        sequence, frame_id, augmentation = identity(image)
        if sequence != sequence_id:
            raise ValueError(f"mixed source sequence: {sequence} != {sequence_id}")
        if frame_id in seen_frames:
            raise ValueError(f"multiple augmented variants for source frame {frame_id}")
        seen_frames.add(frame_id)
        label = label_dir / (image.stem + ".txt")
        if not label.is_file():
            raise ValueError(f"missing label for {image.name}")
        records.append((frame_id, augmentation, image, label))
    extra_labels = {path.stem for path in label_dir.glob("*.txt")} - {item[2].stem for item in records}
    if extra_labels:
        raise ValueError(f"labels without images: {sorted(extra_labels)[:3]}")

    frames_output = output / "frames"
    frames_output.mkdir(parents=True)
    rows = []
    image_receipts = []
    class_counts = {name: 0 for name in sorted(set(class_map.values()))}
    mirror_counts_by_source_frame = {}
    for frame_index, (source_frame, augmentation, image, label_file) in enumerate(records):
        pixels = cv2.imread(str(image))
        if pixels is None or pixels.shape[:2] != (640, 640):
            raise ValueError(f"expected 640x640 mirror image: {image}")
        destination = frames_output / f"frame_{frame_index:04d}.jpg"
        shutil.copy2(image, destination)
        image_receipts.append({"frame_index": frame_index, "source_frame_id": source_frame,
                               "source_name": image.name, "source_sha256": digest(image),
                               "prepared_name": destination.name, "prepared_sha256": digest(destination)})
        for occurrence, line in enumerate(label_file.read_text(encoding="utf-8-sig").splitlines()):
            if not line.strip():
                continue
            original_label, box = yolo_box(line, 640, 640, occurrence + 1, class_map)
            class_counts[original_label] += 1
            mirror_counts_by_source_frame.setdefault(source_frame, Counter())[original_label] += 1
            rows.append({
                "frame_index": frame_index,
                "xmin": box[0], "ymin": box[1], "xmax": box[2], "ymax": box[3],
                "label": "ignore" if original_label == "others" else "vehicle",
                "original_label": original_label,
                "object_id": f"mirror-{sequence_id}-{source_frame:05d}-{occurrence:03d}",
                "source_sequence_id": sequence_id, "source_frame_id": source_frame,
                "mirror_image_name": image.name, "augmentation_id": augmentation,
                "source_yolo_line": line,
            })
    if not rows:
        raise ValueError("no annotations")
    crosscheck = "not_run"
    official_hash = None
    if official_xml:
        official = official_frame_counts(official_xml)
        mismatches = []
        for source_frame, mirror_counts in sorted(mirror_counts_by_source_frame.items()):
            if mirror_counts != official.get(source_frame, Counter()):
                mismatches.append({"source_frame_id": source_frame,
                                   "mirror": dict(mirror_counts),
                                   "official": dict(official.get(source_frame, Counter()))})
        if mismatches:
            raise ValueError(f"mirror/official class-count mismatch: {mismatches[:3]}")
        crosscheck = f"pass_all_{len(mirror_counts_by_source_frame)}_frames"
        official_hash = digest(official_xml)
    csv_path = output / "annotations.csv"
    with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    result = {
        "dataset": "UA-DETRAC-derived traffic-vehicle-detection mirror",
        "status": "pilot_only_not_original_ua_detrac_evaluation",
        "source_url": DATASET_URL,
        "license_url": LICENSE_URL,
        "sequence_id": sequence_id,
        "scene_id": f"ua-detrac-mirror-{sequence_id}",
        "split": split,
        "source_transform": "mirror reports 640x640 stretch from 960x540 and possible flip/rotation/brightness/noise augmentation",
        "leakage_rule": "all variants and frames from this sequence must remain in this split",
        "class_id_mapping": {str(key): value for key, value in sorted(class_map.items())},
        "class_mapping": {name: "ignore" if name == "others" else "vehicle"
                          for name in sorted(set(class_map.values()))},
        "official_xml_class_count_crosscheck": crosscheck,
        "official_xml_sha256": official_hash,
        "frame_count": len(records), "annotation_count": len(rows),
        "class_counts": class_counts, "images": image_receipts,
        "annotations_sha256": digest(csv_path),
    }
    (output / "catalog.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True, help="new directory")
    parser.add_argument("--sequence-id", required=True)
    parser.add_argument("--class-map", type=Path, required=True,
                        help="reviewed JSON containing a mapping object for raw class IDs 0..3")
    parser.add_argument("--official-xml", type=Path, required=True,
                        help="official UA-DETRAC XML used to verify per-frame class counts")
    parser.add_argument("--split", choices=["train", "val", "test"], default="train")
    args = parser.parse_args()
    mapping_document = json.loads(args.class_map.read_text(encoding="utf-8"))
    class_map = {int(key): value for key, value in mapping_document["mapping"].items()}
    result = convert(args.source, args.output, args.sequence_id, class_map, args.split, args.official_xml)
    print(json.dumps({key: result[key] for key in ("status", "frame_count", "annotation_count", "class_counts")},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
