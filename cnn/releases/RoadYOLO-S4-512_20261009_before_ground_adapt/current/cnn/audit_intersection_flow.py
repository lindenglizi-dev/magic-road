"""Audit Intersection-Flow-5K without inventing class or camera semantics."""

from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
import xml.etree.ElementTree as ET
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

from PIL import Image, ImageDraw


PERSON_NAMES = {"pedestrian", "pedestrain"}
CERTAIN_VEHICLE_NAMES = {"vehicle", "bus", "bicycle", "truck"}
UNRESOLVED_NAMES = {"engine", "tricycle"}
EXPECTED_NAMES = PERSON_NAMES | CERTAIN_VEHICLE_NAMES | UNRESOLVED_NAMES | {"obstacle"}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def parse_xml(path: Path) -> tuple[int, int, list[tuple[str, tuple[int, int, int, int]]]]:
    root = ET.parse(path).getroot()
    width, height = int(root.findtext("size/width", "0")), int(root.findtext("size/height", "0"))
    if width <= 0 or height <= 0:
        raise ValueError(f"invalid dimensions: {path}")
    objects = []
    for node in root.findall("object"):
        name = (node.findtext("name") or "").strip().lower()
        box = node.find("bndbox")
        if box is None:
            raise ValueError(f"object without bndbox: {path}")
        values = tuple(int(float(box.findtext(key, "nan"))) for key in ("xmin", "ymin", "xmax", "ymax"))
        x1, y1, x2, y2 = values
        if not (x1 < x2 and y1 < y2):
            raise ValueError(f"non-positive box {values}: {path}")
        objects.append((name, values))
    return width, height, objects


def oracle(counts: list[int], limit: int = 32) -> dict[str, float | int]:
    total = sum(counts)
    kept = sum(min(limit, count) for count in counts)
    return {
        "boxes": total,
        "frames_over_limit": sum(count > limit for count in counts),
        "ideal_recall_ceiling": (kept / total if total else 0.0),
    }


def audit(root: Path) -> dict:
    annotations = sorted(root.glob("annotations/*/*.xml"))
    if not annotations:
        annotations = sorted(root.rglob("annotations/*/*.xml"))
    if not annotations:
        raise ValueError(f"no VOC annotations found under {root}")
    raw_counts: Counter[str] = Counter()
    split_images: Counter[str] = Counter()
    split_counts: dict[str, Counter[str]] = defaultdict(Counter)
    person_heights = []
    cap_counts: dict[str, list[int]] = {"person": [], "vehicle_certain": []}
    cap_by_split: dict[str, dict[str, list[int]]] = defaultdict(
        lambda: {"person": [], "vehicle_certain": []})
    label_hashes = hashlib.sha256()
    dimensions = Counter()
    outside_by_class: Counter[str] = Counter()
    outside_frames: set[str] = set()
    max_overflow = {"left": 0, "top": 0, "right": 0, "bottom": 0}
    timestamp_rows = []
    for path in annotations:
        split = path.parent.name
        width, height, objects = parse_xml(path)
        dimensions[f"{width}x{height}"] += 1
        split_images[split] += 1
        names = Counter(name for name, _ in objects)
        for name, box in objects:
            if box[0] < 0 or box[1] < 0 or box[2] > width or box[3] > height:
                outside_by_class[name] += 1
                outside_frames.add(path.relative_to(root).as_posix())
                max_overflow["left"] = max(max_overflow["left"], -box[0])
                max_overflow["top"] = max(max_overflow["top"], -box[1])
                max_overflow["right"] = max(max_overflow["right"], box[2] - width)
                max_overflow["bottom"] = max(max_overflow["bottom"], box[3] - height)
        raw_counts.update(names)
        split_counts[split].update(names)
        person_count = sum(names[name] for name in PERSON_NAMES)
        vehicle_count = sum(names[name] for name in CERTAIN_VEHICLE_NAMES)
        cap_counts["person"].append(person_count)
        cap_counts["vehicle_certain"].append(vehicle_count)
        cap_by_split[split]["person"].append(person_count)
        cap_by_split[split]["vehicle_certain"].append(vehicle_count)
        if "." in path.stem:
            try:
                timestamp_rows.append((float(path.stem), split, path.stem))
            except ValueError:
                pass
        person_heights.extend((box[3] - box[1]) * 288.0 / height
                              for name, box in objects if name in PERSON_NAMES)
        label_hashes.update(path.relative_to(root).as_posix().encode())
        label_hashes.update(bytes.fromhex(digest(path)))
    heights = sorted(person_heights)
    percentile = lambda fraction: heights[min(len(heights) - 1, int(fraction * len(heights)))] if heights else None
    unknown = sorted(set(raw_counts) - EXPECTED_NAMES)
    timestamp_rows.sort()
    cross_split = [
        (right[0] - left[0], left[1], left[2], right[1], right[2])
        for left, right in zip(timestamp_rows, timestamp_rows[1:])
        if left[1] != right[1]
    ]
    nearest = min(cross_split) if cross_split else None
    return {
        "status": "audit_only_not_training_eligible",
        "annotation_files": len(annotations),
        "xml_declared_dimensions": dict(dimensions),
        "dimension_scope": "XML declarations only; all JPEG dimensions were not decoded by this audit",
        "boxes_outside_xml_dimensions": {
            "boxes": sum(outside_by_class.values()), "affected_xml_files": len(outside_frames),
            "by_raw_class": dict(sorted(outside_by_class.items())),
            "max_overflow_pixels": max_overflow,
            "status": "blocking coordinate-contract audit; clipping is not silently authorized",
        },
        "images_by_source_split": dict(split_images),
        "raw_class_counts": dict(sorted(raw_counts.items())),
        "raw_class_counts_by_split": {key: dict(sorted(value.items())) for key, value in sorted(split_counts.items())},
        "source_label_spelling": {
            "classes_txt_declares": "pedestrian",
            "voc_alias_observed": "pedestrain" if raw_counts["pedestrain"] else None,
            "mapping_status": "alias accepted for audit only; training mapping remains unfrozen",
        },
        "class_contract": {
            "person_audit_aliases": sorted(PERSON_NAMES),
            "vehicle_certain_for_capacity_only": sorted(CERTAIN_VEHICLE_NAMES),
            "unresolved": sorted(UNRESOLVED_NAMES),
            "obstacle": "ignore candidate; completeness/negative policy not established",
            "unknown_observed": unknown,
        },
        "person_height_at_512x288": {
            "count": len(heights), "min": heights[0] if heights else None,
            "p10": percentile(0.10), "median": percentile(0.50),
            "p90": percentile(0.90), "max": heights[-1] if heights else None,
            "at_most_8_px": sum(value <= 8 for value in heights),
            "at_most_16_px": sum(value <= 16 for value in heights),
        },
        "top32_oracle_from_raw_annotation_counts": {
            "all": {key: oracle(value) for key, value in cap_counts.items()},
            "by_source_split": {
                split: {key: oracle(value) for key, value in values.items()}
                for split, values in sorted(cap_by_split.items())
            },
            "scope": "capacity-only; excludes unresolved engine/tricycle and does not measure model recall",
        },
        "source_split_isolation_evidence": {
            "float_timestamp_images": len(timestamp_rows),
            "adjacent_cross_split_pairs_within_1_second": sum(row[0] <= 1.0 for row in cross_split),
            "adjacent_cross_split_pairs_within_2_seconds": sum(row[0] <= 2.0 for row in cross_split),
            "nearest_cross_split_pair": ({
                "delta_seconds": nearest[0], "left_split": nearest[1], "left_stem": nearest[2],
                "right_split": nearest[3], "right_stem": nearest[4],
            } if nearest else None),
            "conclusion": "published train/val/test contains adjacent timestamp frames across splits and is not scene-isolated",
        },
        "annotation_closure_sha256": label_hashes.hexdigest(),
        "blocking_gates": [
            "No authoritative image-to-camera/original-family mapping was found; source train/val/test cannot prove camera isolation.",
            "Published source splits contain adjacent timestamp frames across train/val/test.",
            "engine and tricycle meanings do not match the frozen vehicle contract without an authoritative mapping decision.",
            "Fixed overlay review found bicycle boxes enclosing rider plus bicycle without a separate person box.",
            "The source provides no motion-state field or complete stationary-target annotation policy evidence.",
            "Thousands of VOC boxes exceed the declared image dimensions; the coordinate repair policy is unresolved.",
            "Obstacle treatment and full-frame negative-supervision completeness are not established.",
        ],
        "training_eligible": False,
        "formal_road_eligible": False,
    }


def render_samples(sample_root: Path, output: Path) -> list[dict]:
    if output.exists():
        raise FileExistsError(f"preserve existing sample review: {output}")
    output.mkdir(parents=True)
    results = []
    colors = {"pedestrian": "#ff00ff", "pedestrain": "#ff00ff", "bicycle": "#00ffff",
              "engine": "#ffff00", "tricycle": "#ff8800", "obstacle": "#888888"}
    for xml_path in sorted(sample_root.glob("*.xml")):
        image_path = xml_path.with_suffix(".jpg")
        if not image_path.is_file():
            raise FileNotFoundError(image_path)
        width, height, objects = parse_xml(xml_path)
        image = Image.open(image_path).convert("RGB")
        if image.size != (width, height):
            raise ValueError(f"image/XML dimensions differ: {image_path}")
        draw = ImageDraw.Draw(image)
        for name, box in objects:
            color = colors.get(name, "#00ff00")
            draw.rectangle(box, outline=color, width=3)
            draw.text((box[0], max(0, box[1] - 12)), name, fill=color, stroke_width=1, stroke_fill="black")
        target = output / f"{xml_path.stem}_overlay.jpg"
        image.save(target, quality=92)
        results.append({"stem": xml_path.stem, "image_sha256": digest(image_path),
                        "xml_sha256": digest(xml_path), "overlay": target.name,
                        "objects": dict(Counter(name for name, _ in objects))})
    return results


def archive_receipt(path: Path) -> dict:
    md5 = hashlib.md5()  # nosec: source-integrity value published by GCS, not security use
    sha256 = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            md5.update(block)
            sha256.update(block)
    with zipfile.ZipFile(path) as archive:
        bad = archive.testzip()
        entries = archive.infolist()
    return {
        "path": str(path.resolve()), "bytes": path.stat().st_size,
        "expected_bytes_from_http_range": 6175277050,
        "md5": md5.hexdigest(), "expected_md5_from_gcs_etag": "bfa3150b821855f9ff92b08609b33c8c",
        "sha256": sha256.hexdigest(), "zip_entries": len(entries),
        "uncompressed_bytes": sum(entry.file_size for entry in entries),
        "zip_crc_test": "passed" if bad is None else f"failed:{bad}",
        "source": "https://www.kaggle.com/datasets/starsw/intersection-flow-5k",
        "api_source": "https://www.kaggle.com/api/v1/datasets/download/starsw/intersection-flow-5k?datasetVersionNumber=4",
        "license": "CC BY-NC-SA 4.0",
        "license_url": "https://creativecommons.org/licenses/by-nc-sa/4.0/",
    }


def self_test() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory) / "Intersection-Flow-5K"
        labels = root / "annotations" / "train"
        labels.mkdir(parents=True)
        (labels / "a.xml").write_text("""<annotation><size><width>1920</width><height>1080</height></size>
<object><name>pedestrain</name><bndbox><xmin>10</xmin><ymin>10</ymin><xmax>30</xmax><ymax>40</ymax></bndbox></object>
<object><name>vehicle</name><bndbox><xmin>50</xmin><ymin>50</ymin><xmax>90</xmax><ymax>100</ymax></bndbox></object></annotation>""", encoding="utf-8")
        result = audit(root)
        assert result["raw_class_counts"] == {"pedestrain": 1, "vehicle": 1}
        assert result["top32_oracle_from_raw_annotation_counts"]["all"]["person"]["ideal_recall_ceiling"] == 1.0
        assert result["training_eligible"] is False


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--sample-root", type=Path)
    parser.add_argument("--render-output", type=Path)
    parser.add_argument("--archive", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        print("self-test: passed")
        return
    if not args.root or not args.output:
        parser.error("--root and --output are required")
    result = audit(args.root)
    if args.sample_root:
        if not args.render_output:
            parser.error("--render-output is required with --sample-root")
        result["fixed_sample_review"] = render_samples(args.sample_root, args.render_output)
        result["fixed_sample_visual_findings"] = {
            "10110010": "All four bicycle boxes enclose a visible rider and bicycle together; no person box is present.",
            "1662003896.981607437": "The engine box encloses a yellow engineering/construction vehicle, not a motorcycle; bicycle boxes enclose riders with their cycles.",
            "1662026780.586349010": "Same fixed camera view as the preceding timestamp sample; bicycle boxes enclose riders with their cycles while person boxes annotate other pedestrians.",
            "scope": "manual visual review of three fixed lexicographic/timestamp-family samples only",
        }
    if args.archive:
        result["archive_receipt"] = archive_receipt(args.archive)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
