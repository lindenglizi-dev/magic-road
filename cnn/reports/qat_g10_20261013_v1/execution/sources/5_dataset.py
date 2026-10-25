"""Build and audit full-frame 512x288 two-class detection datasets.

VIRAT is kept diagnostic-only because local review found missed objects despite
the release README describing the object files as complete.  COCO instances
JSON is the complete-supervision pretraining adapter.  No blind-reserve path is
accepted by this module.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
import zlib
from collections import Counter, defaultdict
from pathlib import Path
from typing import Callable

import cv2
import numpy as np
from PIL import Image

try:
    from .integer import resize_area
except ImportError:  # ``python cnn/dataset.py``
    from integer import resize_area


WIDTH, HEIGHT = 512, 288
CLASSES = ("person", "vehicle")
VIRAT_LABEL = {1: 0, 2: 1, 3: 1, 5: 1}
VIRAT_IGNORE = {0, 4}
VIRAT_SPLIT = {
    "000201": "train", "000206": "train",
    "000200": "val", "000203": "val",
    # These scenes were already viewed for mapping QA; they are not new tests.
    "000205": "development_holdout", "000207": "development_holdout",
    "010107": "development_holdout",
}
COCO_LABEL = {"person": 0, "bicycle": 1, "car": 1,
              "motorcycle": 1, "bus": 1, "truck": 1}
SCENE_RE = re.compile(r"^VIRAT_S_(\d{6})_")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _refuse_blind(path: Path) -> None:
    text = str(path.resolve()).lower()
    if "blind" in text or "reserve" in text:
        raise ValueError(f"blind/reserve paths are forbidden: {path}")


def _scaled_box(x: float, y: float, width: float, height: float,
                source_width: int, source_height: int) -> list[float]:
    """Convert x/y/width/height to clipped continuous half-open coordinates."""
    if not np.isfinite([x, y, width, height]).all():
        raise ValueError("box coordinates must be finite")
    if source_width <= 0 or source_height <= 0:
        raise ValueError("source dimensions must be positive")
    if width <= 0 or height <= 0:
        raise ValueError("box width and height must be positive")
    box = [x * WIDTH / source_width, y * HEIGHT / source_height,
           (x + width) * WIDTH / source_width,
           (y + height) * HEIGHT / source_height]
    box = [max(0.0, min(limit, value))
           for value, limit in zip(box, (WIDTH, HEIGHT, WIDTH, HEIGHT), strict=True)]
    if box[0] >= box[2] or box[1] >= box[3]:
        raise ValueError("box has no frame intersection")
    return [round(value, 6) for value in box]


def _write_png(rgb: np.ndarray, path: Path,
               resizer: Callable[[np.ndarray], np.ndarray] = resize_area) -> None:
    resized = resizer(rgb)
    if resized.shape != (HEIGHT, WIDTH, 3) or resized.dtype != np.uint8:
        raise ValueError("resize_area must return 288x512x3 uint8 RGB")
    path.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(path), cv2.cvtColor(resized, cv2.COLOR_RGB2BGR)):
        raise OSError(f"cannot write PNG: {path}")


def _letterbox_transform(source_width: int, source_height: int) -> dict[str, float | int]:
    if source_width <= 0 or source_height <= 0:
        raise ValueError('image dimensions must be positive')
    ratio = min(1280 / source_width, 720 / source_height)
    resized_width, resized_height = round(source_width * ratio), round(source_height * ratio)
    if min(resized_width, resized_height) < 1:
        raise ValueError('image aspect ratio cannot be represented in 720p')
    offset_x, offset_y = (1280 - resized_width) // 2, (720 - resized_height) // 2
    return {
        "source_width": source_width, "source_height": source_height,
        "resized_width": resized_width, "resized_height": resized_height,
        "scale_x": resized_width / source_width, "scale_y": resized_height / source_height,
        "offset_x": offset_x, "offset_y": offset_y,
    }


def _letterbox_720(rgb: np.ndarray) -> tuple[np.ndarray, dict[str, float | int]]:
    """Center-letterbox arbitrary RGB before the hardware-exact 5-to-2 resize."""
    source_height, source_width = rgb.shape[:2]
    transform = _letterbox_transform(source_width, source_height)
    width, height = int(transform['resized_width']), int(transform['resized_height'])
    ox, oy = int(transform['offset_x']), int(transform['offset_y'])
    ratio = min(1280 / source_width, 720 / source_height)
    resized = cv2.resize(rgb, (width, height),
                         interpolation=cv2.INTER_AREA if ratio < 1 else cv2.INTER_LINEAR)
    canvas = np.zeros((720, 1280, 3), dtype=np.uint8)
    canvas[oy:oy + height, ox:ox + width] = resized
    return canvas, transform


def _letterboxed_box(bbox: list[float], transform: dict[str, float | int]) -> list[float]:
    x, y, width, height = bbox
    sx, sy = float(transform["scale_x"]), float(transform["scale_y"])
    ox, oy = int(transform["offset_x"]), int(transform["offset_y"])
    return _scaled_box(x * sx + ox, y * sy + oy, width * sx, height * sy, 1280, 720)


def _read_virat(path: Path) -> dict[int, list[tuple[int, int, int, int, int]]]:
    rows: dict[int, list[tuple[int, int, int, int, int]]] = defaultdict(list)
    for line_number, text in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        if not text.strip():
            continue
        fields = text.split()
        if len(fields) != 8:
            raise ValueError(f"{path}:{line_number}: expected 8 columns")
        try:
            _, _, frame, x, y, width, height, object_type = map(int, fields)
        except ValueError as exc:
            raise ValueError(f"{path}:{line_number}: non-integer field") from exc
        if frame < 0 or width <= 0 or height <= 0:
            raise ValueError(f"{path}:{line_number}: invalid frame or box")
        if object_type not in VIRAT_LABEL and object_type not in VIRAT_IGNORE:
            raise ValueError(f"{path}:{line_number}: unknown VIRAT type {object_type}")
        rows[frame].append((x, y, width, height, object_type))
    return rows


def _diagnostic_frames(rows: dict[int, list[tuple[int, int, int, int, int]]],
                       limit: int) -> list[int]:
    frames = sorted(rows)
    if limit <= 0 or len(frames) <= limit:
        return frames
    # Preserve class coverage first, then spread the remaining samples in time.
    chosen: list[int] = []
    for label in (0, 1):
        frame = next((frame for frame in frames
                      if any(VIRAT_LABEL.get(row[4]) == label for row in rows[frame])), None)
        if frame is not None and frame not in chosen:
            chosen.append(frame)
    for index in np.linspace(0, len(frames) - 1, limit, dtype=int):
        frame = frames[int(index)]
        if frame not in chosen:
            chosen.append(frame)
        if len(chosen) == limit:
            break
    return sorted(chosen[:limit])


def _virat_pairs(root: Path) -> list[tuple[Path, Path, str]]:
    videos = root / "video_original"
    annotations = root / "annotations"
    pairs = []
    for video in sorted(videos.glob("*.mp4")):
        annotation = annotations / f"{video.stem}.viratdata.objects.txt"
        if not annotation.is_file():
            sidecar = videos / f"{video.stem}.viratdata.objects.txt"
            annotation = sidecar if sidecar.is_file() else annotation
        if not annotation.is_file():
            continue
        match = SCENE_RE.match(video.stem)
        if not match or match.group(1) not in VIRAT_SPLIT:
            raise ValueError(f"unreviewed VIRAT scene: {video.stem}")
        pairs.append((video, annotation, match.group(1)))
    if not pairs:
        raise ValueError("no paired non-blind VIRAT video/object files found")
    return pairs


def build_virat(root: Path, output: Path, max_frames_per_scene: int = 2) -> dict:
    """Build a diagnostic VIRAT subset; every frame remains incomplete."""
    _refuse_blind(root)
    pairs = _virat_pairs(root)
    images = []
    sources = []
    excluded = Counter()
    for video, annotation, scene in pairs:
        rows = _read_virat(annotation)
        video_hash, annotation_hash = sha256_file(video), sha256_file(annotation)
        cap = cv2.VideoCapture(str(video))
        if not cap.isOpened():
            raise ValueError(f"cannot open video: {video}")
        try:
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            source_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            source_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            if (source_width, source_height) != (1280, 720):
                raise ValueError(f"resize_area requires native 1280x720: {video}")
            selected = _diagnostic_frames(
                {frame: value for frame, value in rows.items() if frame < frame_count},
                max_frames_per_scene)
            for frame in selected:
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame)
                ok, bgr = cap.read()
                if not ok or bgr.shape != (720, 1280, 3):
                    raise ValueError(f"cannot decode {video.name} frame {frame}")
                boxes, labels, ignore_boxes = [], [], []
                for x, y, width, height, object_type in rows[frame]:
                    try:
                        box = _scaled_box(x, y, width, height, source_width, source_height)
                    except ValueError:
                        excluded["box_no_frame_intersection"] += 1
                        continue
                    if object_type in VIRAT_LABEL:
                        boxes.append(box)
                        labels.append(VIRAT_LABEL[object_type])
                    else:
                        ignore_boxes.append(box)
                relative = Path("images") / f"{video.stem}_f{frame:06d}.png"
                _write_png(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB), output / relative)
                images.append({
                    "image": relative.as_posix(), "boxes": boxes, "labels": labels,
                    "ignore_boxes": ignore_boxes,
                    "scene_id": f"virat-ground-{scene}",
                    "split": VIRAT_SPLIT[scene], "source_sha256": video_hash,
                    "source_frame": frame, "incomplete_frame": True,
                    "annotation_complete": False,
                    "source_annotation_sha256": annotation_hash,
                })
        finally:
            cap.release()
        sources.append({
            "dataset": "VIRAT Ground Release 2.0", "scene_id": f"virat-ground-{scene}",
            "split": VIRAT_SPLIT[scene], "video": str(video.resolve()),
            "video_sha256": video_hash, "annotation": str(annotation.resolve()),
            "annotation_sha256": annotation_hash,
            "completeness": "incomplete_for_negative_supervision",
        })
    document = {
        "schema_version": 1, "task": "detection", "input_size": [WIDTH, HEIGHT],
        "classes": list(CLASSES),
        "manifest_status": "diagnostic_incomplete",
        "purpose": "diagnostic_incomplete_positive_and_ignore_only",
        "training_eligible": False, "images": images,
    }
    provenance = {
        "adapter": "virat_ground_release_2", "sources": sources,
        "class_mapping": {"1": 0, "2": 1, "3": 1, "5": 1,
                          "0": "ignore", "4": "ignore"},
        "rider_policy": "person is emitted only when an explicit type-1 box exists",
        "completeness_evidence": (
            "official object tracks exist, but project frame review found omitted targets; "
            "unlabelled regions are never supervised as background"),
        "excluded": dict(excluded),
    }
    write_bundle(document, output, output.parent.parent / "reports", "virat_diagnostic", provenance)
    return document


def _coco_source(annotation_json: Path, image_root: Path, output: Path, split: str,
                 source_url: str, license_url: str,
                 max_images: int = 0, *, raw_images: bool = False,
                 allowed_names: set[str] | None = None,
                 expected_hashes: dict[str, str] | None = None,
                 expected_crc: dict[str, tuple[int, int]] | None = None) -> tuple[list[dict], dict]:
    for path in (annotation_json, image_root):
        _refuse_blind(path)
    if not source_url.strip() or not license_url.strip():
        raise ValueError("COCO source and license URLs must be explicit")
    raw = json.loads(annotation_json.read_text(encoding="utf-8"))
    categories = {int(row["id"]): row["name"] for row in raw.get("categories", [])}
    category_label = {identifier: COCO_LABEL[name]
                      for identifier, name in categories.items() if name in COCO_LABEL}
    missing = set(COCO_LABEL) - set(categories.values())
    if missing:
        raise ValueError(f"COCO categories missing: {sorted(missing)}")
    annotations: dict[int, list[dict]] = defaultdict(list)
    for row in raw.get("annotations", []):
        annotations[int(row["image_id"])].append(row)
    all_source_images = sorted(raw.get("images", []), key=lambda row: int(row["id"]))
    local_names = {path.name for path in image_root.iterdir() if path.is_file()}
    if allowed_names is not None:
        if not allowed_names <= local_names:
            raise FileNotFoundError('receipt images missing from local directory')
        local_names &= allowed_names
    source_images = [row for row in all_source_images if row["file_name"] in local_names]
    missing_image_count = len(all_source_images) - len(source_images)
    if max_images > 0:
        source_images = source_images[:max_images]
    images = []
    degenerate_annotations = []
    for source in source_images:
        image_id = int(source["id"])
        path = image_root / source["file_name"]
        if raw_images:
            with Image.open(path) as header:
                if header.size != (int(source['width']), int(source['height'])):
                    raise ValueError(f'annotation/image dimensions differ: {path}')
                transform = _letterbox_transform(*header.size)
            letterboxed = None
        else:
            bgr = cv2.imread(str(path), cv2.IMREAD_COLOR)
            if bgr is None:
                raise ValueError(f"cannot decode image: {path}")
            if bgr.shape[:2] != (int(source['height']), int(source['width'])):
                raise ValueError(f'annotation/image dimensions differ: {path}')
            letterboxed, transform = _letterbox_720(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB))
        boxes, labels, ignore_boxes, ignore_metadata = [], [], [], []
        for row in annotations.get(image_id, []):
            category = int(row["category_id"])
            if category not in category_label:
                continue
            source_box = list(map(float, row["bbox"]))
            if (len(source_box) == 4 and np.isfinite(source_box).all()
                    and source_box[2] >= 0 and source_box[3] >= 0
                    and (source_box[2] == 0 or source_box[3] == 0)
                    and row.get('area') == 0):
                # No valid extent can be inferred. Keep explicit positives, but
                # suppress all background supervision for this affected frame.
                full_frame = [0.0, 0.0, float(WIDTH), float(HEIGHT)]
                if full_frame not in ignore_boxes:
                    ignore_boxes.append(full_frame)
                    ignore_metadata.append({'label': -1, 'crowd': False})
                degenerate_annotations.append({
                    'annotation_id': row.get('id'), 'image_id': image_id,
                    'category_id': category, 'bbox': source_box, 'area': row['area'],
                    'policy': 'zero_area_nonpositive_extent_full_frame_ignore',
                })
                continue
            box = _letterboxed_box(source_box, transform)
            if int(row.get("iscrowd", 0)):
                ignore_boxes.append(box)
                ignore_metadata.append({'label': category_label[category], 'crowd': True})
            else:
                boxes.append(box)
                labels.append(category_label[category])
        safe_split = re.sub(r"[^A-Za-z0-9_-]", "_", split)
        relative = Path("images") / f"coco_{safe_split}_{image_id:012d}.png"
        source_hash = sha256_file(path)
        if expected_hashes is not None and source_hash != expected_hashes.get(path.name):
            raise ValueError(f'image differs from download receipt: {path}')
        if expected_crc is not None:
            crc = 0
            with path.open('rb') as handle:
                for block in iter(lambda: handle.read(1024 * 1024), b''):
                    crc = zlib.crc32(block, crc)
            if (path.stat().st_size, crc) != expected_crc.get(path.name):
                raise ValueError(f'image differs from verified official archive: {path}')
        if not raw_images:
            _write_png(letterboxed, output / relative)
        images.append({
            "image": str(path.resolve()) if raw_images else relative.as_posix(),
            "boxes": boxes, "labels": labels,
            "ignore_boxes": ignore_boxes, "scene_id": f"coco-{image_id}",
            "ignore_metadata": ignore_metadata,
            "split": split, "source_sha256": source_hash,
            "source_frame": image_id, "incomplete_frame": False,
            "annotation_complete": True,
            "preprocess": {"raw_image": raw_images, "letterbox_1280x720": transform,
                           "resize": "integer.resize_area_5_to_2_RNE"},
        })
    if not images:
        raise ValueError(f"no locally available COCO images for {annotation_json}")
    provenance = {
        "adapter": "coco_instances", "annotation_json": str(annotation_json.resolve()),
        "annotation_sha256": sha256_file(annotation_json),
        "image_root": str(image_root.resolve()), "source_url": source_url,
        "license_url": license_url, "split": split,
        "class_mapping": COCO_LABEL,
        "crowd_policy": "selected-class iscrowd boxes are ignore_boxes",
        "annotation_status": "official_ground_truth_declared_by_source_manifest",
        "canonical_image_count": len(all_source_images),
        "local_image_count": len(source_images),
        "missing_local_image_count": missing_image_count,
        "raw_images": raw_images,
        "degenerate_annotations": degenerate_annotations,
    }
    return images, provenance


def build_coco(annotation_json: Path, image_root: Path, output: Path, split: str,
               source_url: str, license_url: str, max_images: int = 0) -> dict:
    """Adapt one official COCO instances JSON to complete pretraining."""
    if (output / 'dataset.json').exists():
        raise FileExistsError('preserve existing dataset; choose a new output directory')
    images, provenance = _coco_source(annotation_json, image_root, output, split,
                                      source_url, license_url, max_images)
    document = {
        "schema_version": 1, "task": "detection", "input_size": [WIDTH, HEIGHT],
        "classes": list(CLASSES),
        "manifest_status": "pretrain_subset",
        "purpose": "complete_two_class_pretraining", "training_eligible": True,
        "images": images,
    }
    write_bundle(document, output, output.parent.parent / "reports", f"coco_{split}", provenance)
    return document


def build_coco_manifest(manifest: Path, output: Path, *, raw_images: bool = False) -> dict:
    """Build all locally present sources listed in ``image_json_paths``."""
    raw = json.loads(manifest.read_text(encoding="utf-8"))
    if (output / 'dataset.json').exists():
        raise FileExistsError('preserve existing dataset; choose a new output directory')
    entries = raw.get("image_json_paths")
    if not isinstance(entries, list) or not entries:
        raise ValueError("manifest must contain a non-empty image_json_paths list")
    images, sources = [], []
    pinned_annotations = {str(Path(row['path']).resolve()): row['sha256']
                          for row in raw.get('annotation_files', [])}
    for entry in entries:
        required = {"annotation_json", "image_root", "split", "source_url", "license_url"}
        if not required <= entry.keys():
            raise ValueError(f"COCO source entry missing {sorted(required - entry.keys())}")
        annotation_path = Path(entry['annotation_json']).resolve()
        if (raw.get('kind', '').startswith('coco_') and
                sha256_file(annotation_path) != pinned_annotations.get(str(annotation_path))):
            raise ValueError('annotations differ from download receipt')
        expected_hashes = None
        expected_crc = None
        if raw.get('image_selection') == 'category_round_robin_sha256_seed42':
            expected_hashes = {Path(row['path']).name: row['sha256']
                               for row in raw['downloads'] if Path(row['path']).parent.resolve()
                               == Path(entry['image_root']).resolve()}
        elif raw.get('image_selection') == 'all_official_2017_images':
            split_name = str(entry['split']) + '2017'
            archive_rows = [row for row in raw['downloads']
                            if Path(row['path']).name == split_name + '.zip']
            if len(archive_rows) != 1:
                raise ValueError('full COCO receipt needs exactly one archive per split')
            archive_row = archive_rows[0]
            archive_path = Path(archive_row['path'])
            if sha256_file(archive_path) != archive_row['sha256']:
                raise ValueError('archive differs from download receipt')
            with zipfile.ZipFile(archive_path) as archive:
                expected_crc = {Path(item.filename).name: (item.file_size, item.CRC)
                                for item in archive.infolist() if not item.is_dir()}
        source_images, provenance = _coco_source(
            Path(entry["annotation_json"]), Path(entry["image_root"]), output,
            str(entry["split"]), str(entry["source_url"]), str(entry["license_url"]),
            int(entry.get("max_images", 0)), raw_images=raw_images,
            allowed_names=set(expected_hashes) if expected_hashes is not None else None,
            expected_hashes=expected_hashes, expected_crc=expected_crc)
        if raw.get('image_selection') == 'all_official_2017_images':
            expected = raw.get('full_image_counts', {}).get(str(entry['split']) + '2017')
            if len(source_images) != expected:
                raise ValueError('full archive count does not match adapted manifest')
        images.extend(source_images)
        sources.append(provenance)
    document = {
        "schema_version": 1, "task": "detection", "input_size": [WIDTH, HEIGHT],
        "classes": list(CLASSES),
        "manifest_status": ('pretrain_full' if raw.get('image_selection') ==
                            'all_official_2017_images' else "pretrain_subset"),
        "purpose": "complete_two_class_pretraining", "training_eligible": True,
        "images": images,
    }
    provenance = {"adapter": "coco_image_json_paths", "manifest": str(manifest.resolve()),
                  "manifest_sha256": sha256_file(manifest), "sources": sources}
    write_bundle(document, output, output.parent.parent / "reports", output.name, provenance)
    return document


def audit(document: dict, base: Path | None = None) -> dict:
    if (document.get("schema_version") != 1 or document.get("task") != "detection" or
            document.get("input_size") != [WIDTH, HEIGHT] or
            document.get("classes") != list(CLASSES)):
        raise ValueError("unsupported dataset schema or classes")
    split_images, split_scenes = Counter(), defaultdict(set)
    class_counts = defaultdict(lambda: [0, 0])
    incomplete = 0
    image_hashes = []
    for index, row in enumerate(document.get("images", [])):
        required = {"image", "boxes", "labels", "ignore_boxes", "scene_id", "split",
                    "source_sha256", "source_frame"}
        if not required <= row.keys() or len(row["boxes"]) != len(row["labels"]):
            raise ValueError(f"image {index}: schema mismatch")
        for box in [*row["boxes"], *row["ignore_boxes"]]:
            if len(box) != 4 or not (0 <= box[0] < box[2] <= WIDTH and
                                     0 <= box[1] < box[3] <= HEIGHT):
                raise ValueError(f"image {index}: invalid half-open box {box}")
        if any(label not in (0, 1) for label in row["labels"]):
            raise ValueError(f"image {index}: invalid label")
        if 'ignore_metadata' in row:
            metadata = row['ignore_metadata']
            if (len(metadata) != len(row['ignore_boxes']) or
                    any(item.get('label') not in (-1, 0, 1) or
                        not isinstance(item.get('crowd'), bool) for item in metadata)):
                raise ValueError(f'image {index}: ignore metadata mismatch')
        split = row["split"]
        split_images[split] += 1
        split_scenes[split].add(row["scene_id"])
        for label in row["labels"]:
            class_counts[split][label] += 1
        incomplete += bool(row.get("incomplete_frame", True))
        if base is not None:
            path = base / row["image"]
            if not path.is_file():
                raise FileNotFoundError(path)
            image_hashes.append({"image": row["image"], "sha256": sha256_file(path)})
    scene_gate = (document.get("manifest_status") == "formal_road" and
                  len(split_scenes["train"]) >= 6 and len(split_scenes["val"]) >= 3 and
                  len(split_scenes["newtest"]) >= 3)
    coverage_gate = all(all(value > 0 for value in class_counts[split])
                        for split in ("train", "val", "newtest"))
    completeness_gate = incomplete == 0
    return {
        "image_count": len(document.get("images", [])),
        "images_by_split": dict(sorted(split_images.items())),
        "scenes_by_split": {key: sorted(value) for key, value in sorted(split_scenes.items())},
        "scene_counts": {key: len(value) for key, value in sorted(split_scenes.items())},
        "class_box_counts": {key: {"person": value[0], "vehicle": value[1]}
                             for key, value in sorted(class_counts.items())},
        "incomplete_frames": incomplete,
        "formal_gates": {
            "at_least_6_train_3_val_3_newtest_scenes": scene_gate,
            "person_and_vehicle_in_train_val_newtest": coverage_gate,
            "all_frames_complete_for_negative_supervision": completeness_gate,
        },
        "formal_training_eligible": scene_gate and coverage_gate and completeness_gate,
        "image_hashes": image_hashes,
    }


def load_dataset(path: Path, *, allow_incomplete: bool = False,
                 require_formal: bool = True) -> dict:
    """Training loader guard: incomplete or non-formal road data fails closed."""
    document = json.loads(path.read_text(encoding="utf-8"))
    report = audit(document, path.parent)
    if not allow_incomplete and report["incomplete_frames"]:
        raise ValueError("dataset contains incomplete frames; background supervision is forbidden")
    if require_formal and not report["formal_training_eligible"]:
        raise ValueError("dataset fails the 6-train/3-val/3-newtest formal gate")
    return document


def write_bundle(document: dict, output: Path, report_dir: Path, name: str,
                 provenance: dict) -> None:
    output.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)
    dataset_path = output / "dataset.json"
    report = audit(document, output)
    with dataset_path.open('x', encoding='utf-8') as stream:
        stream.write(json.dumps(document, ensure_ascii=False, indent=2) + '\n')
    (report_dir / f"dataset_{name}_audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (report_dir / f"dataset_{name}_provenance.json").write_text(
        json.dumps(provenance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    integrity = {"dataset": str(dataset_path.resolve()),
                 "dataset_sha256": sha256_file(dataset_path),
                 "images": report.pop("image_hashes")}
    (report_dir / f"dataset_{name}_integrity.json").write_text(
        json.dumps(integrity, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    virat = subparsers.add_parser("virat")
    virat.add_argument("--root", type=Path, required=True)
    virat.add_argument("--output", type=Path, required=True)
    virat.add_argument("--max-frames-per-scene", type=int, default=2)
    coco = subparsers.add_parser("coco")
    coco.add_argument("--annotations", type=Path, required=True)
    coco.add_argument("--images", type=Path, required=True)
    coco.add_argument("--output", type=Path, required=True)
    coco.add_argument("--split", required=True)
    coco.add_argument("--source-url", required=True)
    coco.add_argument("--license-url", required=True)
    coco.add_argument("--max-images", type=int, default=0)
    coco_manifest = subparsers.add_parser("coco-manifest")
    coco_manifest.add_argument("--manifest", type=Path, required=True)
    coco_manifest.add_argument("--output", type=Path, required=True)
    coco_manifest.add_argument('--raw-images', action='store_true',
                               help='Lazy exact preprocessing from source JPEGs; no duplicate PNG corpus')
    check = subparsers.add_parser("audit")
    check.add_argument("dataset", type=Path)
    check.add_argument("--allow-incomplete", action="store_true")
    check.add_argument("--no-formal-gate", action="store_true")
    args = parser.parse_args()
    if args.command == "virat":
        result = build_virat(args.root, args.output, args.max_frames_per_scene)
    elif args.command == "coco":
        result = build_coco(args.annotations, args.images, args.output, args.split,
                            args.source_url, args.license_url, args.max_images)
    elif args.command == "coco-manifest":
        result = build_coco_manifest(args.manifest, args.output, raw_images=args.raw_images)
    else:
        result = load_dataset(args.dataset, allow_incomplete=args.allow_incomplete,
                              require_formal=not args.no_formal_gate)
    summary = audit(result)
    # Full scene IDs and image hashes remain in the saved audit/integrity reports.
    summary.pop('image_hashes', None)
    summary.pop('scenes_by_split', None)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
