"""Fail-closed importer for manually signed CNN review patches."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from collections import Counter
from pathlib import Path
from typing import Any


MANIFEST_SCHEMA = "cnn_review_workbench_v1"
PATCH_SCHEMA = "cnn_review_patch_v1"
OUTPUT_SCHEMA = "cnn_verified_labels_v1"
CLASSES = {"person", "vehicle", "ignore"}
ACTIONS = {"A", "M", "N", "I", "D"}
CHECKS = {"person", "vehicle", "rider", "parked_vehicle", "small_occluded", "ignore"}
BUCKET_SPLITS = {
    "train_review": "train",
    "road_development": "dev",
    "person_background_aux": "stress",
}
DERIVED_SAMPLE_FIELDS = {"teacher", "teacher_candidates", "teacher_status",
                         "warnings", "review_score"}


class ReviewError(ValueError):
    """The frozen input or manual patch violates the review contract."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def json_hash(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ReviewError(message)


def _string(value: Any, where: str, *, allow_empty: bool = False) -> str:
    _require(isinstance(value, str), f"{where}: expected string")
    if not allow_empty:
        _require(bool(value.strip()), f"{where}: must not be empty")
    return value


def _positive_int(value: Any, where: str) -> int:
    _require(isinstance(value, int) and not isinstance(value, bool) and value > 0,
             f"{where}: expected positive integer")
    return value


def _hex_digest(value: Any, where: str) -> str:
    text = _string(value, where)
    _require(len(text) == 64 and all(char in "0123456789abcdef" for char in text),
             f"{where}: expected lowercase SHA-256")
    return text


def _source_value(value: Any, where: str) -> str | int:
    _require((isinstance(value, str) and bool(value.strip()))
             or (isinstance(value, int) and not isinstance(value, bool)),
             f"{where}: expected non-empty string or integer")
    return value


def _box(value: Any, width: int, height: int, where: str) -> list[int | float]:
    _require(isinstance(value, list) and len(value) == 4, f"{where}: expected XYXY list")
    _require(all(isinstance(item, (int, float)) and not isinstance(item, bool)
                 and math.isfinite(item) for item in value),
             f"{where}: coordinates must be finite numbers")
    x1, y1, x2, y2 = value
    _require(0 <= x1 < x2 <= width and 0 <= y1 < y2 <= height,
             f"{where}: invalid native half-open XYXY box")
    return value


def _json_object(path: Path, kind: str) -> tuple[dict[str, Any], bytes]:
    try:
        raw = path.read_bytes()
        value = json.loads(raw)
    except (OSError, json.JSONDecodeError) as exc:
        raise ReviewError(f"cannot read {kind} JSON: {path}: {exc}") from exc
    _require(isinstance(value, dict), f"{kind}: top level must be an object")
    return value, raw


def _forbid_blind(path: Path, where: str) -> None:
    lowered = str(path).replace("\\", "/").lower()
    _require("blind" not in lowered and "reserve" not in lowered,
             f"{where}: blind/reserve paths are forbidden")


def _raw_path(root: Path, raw_file: Any, image_id: str) -> Path:
    text = _string(raw_file, f"sample {image_id}.raw_file")
    _require("blind" not in text.lower() and "reserve" not in text.lower(),
             f"sample {image_id}: blind/reserve raw path is forbidden")
    relative = Path(text)
    _require(not relative.is_absolute() and not relative.drive and ".." not in relative.parts,
             f"sample {image_id}: raw_file must be a safe relative path")
    _require(len(relative.parts) == 3 and relative.parts[0] == "images"
             and relative.name in {"raw.jpg", "raw.png"},
             f"sample {image_id}: raw_file must be images/<id>/raw.jpg|png")
    resolved_root = root.resolve()
    resolved = (root / relative).resolve()
    _require(resolved.is_relative_to(resolved_root),
             f"sample {image_id}: raw_file escapes the package")
    _require(resolved.is_file(), f"sample {image_id}: missing raw file")
    return resolved


def _validate_manifest(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]],
                                             dict[str, dict[str, Any]], Path, bytes, bytes]:
    _forbid_blind(path, "manifest")
    manifest, raw = _json_object(path, "manifest")
    _require(manifest.get("schema") == MANIFEST_SCHEMA, "manifest: unsupported schema")
    policy_hash = _hex_digest(manifest.get("annotation_policy_sha256"),
                              "manifest.annotation_policy_sha256")
    samples = manifest.get("samples")
    _require(isinstance(samples, list), "manifest.samples: expected list")
    _require(_positive_int(manifest.get("train_required_count"),
                          "manifest.train_required_count") == 128,
             "manifest.train_required_count must be 128")

    by_id: dict[str, dict[str, Any]] = {}
    train_count = 0
    for index, sample in enumerate(samples):
        where = f"manifest.samples[{index}]"
        _require(isinstance(sample, dict), f"{where}: expected object")
        image_id = _string(sample.get("image_id"), f"{where}.image_id")
        _require(image_id not in by_id, f"manifest: duplicate image_id {image_id}")
        _string(sample.get("legacy_id"), f"{where}.legacy_id")
        bucket = _string(sample.get("bucket"), f"{where}.bucket")
        split = _string(sample.get("split"), f"{where}.split")
        _require(bucket in BUCKET_SPLITS, f"sample {image_id}: unknown bucket {bucket}")
        _require(BUCKET_SPLITS[bucket] == split,
                 f"sample {image_id}: bucket/split crossing is forbidden")
        width = _positive_int(sample.get("width"), f"{where}.width")
        height = _positive_int(sample.get("height"), f"{where}.height")
        source_hash = _hex_digest(sample.get("source_sha256"), f"{where}.source_sha256")
        raw_path = _raw_path(path.parent, sample.get("raw_file"), image_id)
        _require(sha256_file(raw_path) == source_hash,
                 f"sample {image_id}: raw file SHA-256 mismatch")

        originals = sample.get("original")
        _require(isinstance(originals, list), f"{where}.original: expected list")
        target_ids: set[str] = set()
        for target_index, target in enumerate(originals):
            target_where = f"{where}.original[{target_index}]"
            _require(isinstance(target, dict), f"{target_where}: expected object")
            target_id = _string(target.get("target_id"), f"{target_where}.target_id")
            _require(target_id not in target_ids,
                     f"sample {image_id}: duplicate original target_id {target_id}")
            target_ids.add(target_id)
            label = _string(target.get("class"), f"{target_where}.class")
            _require(label in CLASSES, f"{target_where}: unknown class {label}")
            _box(target.get("bbox"), width, height, f"{target_where}.bbox")
            _source_value(target.get("source_category"), f"{target_where}.source_category")
            _source_value(target.get("source_target_id"), f"{target_where}.source_target_id")
        sample["_raw_path"] = raw_path
        by_id[image_id] = sample
        train_count += bucket == "train_review"

    _require(train_count == 128, f"manifest: expected 128 train_review samples, got {train_count}")
    binding = {
        "annotation_policy_sha256": policy_hash,
        "samples": [{key: sample[key] for key in
                     ("image_id", "source_sha256", "width", "height", "bucket", "split", "original")}
                    for sample in samples],
    }
    _require(_hex_digest(manifest.get("dataset_id"), "manifest.dataset_id") == json_hash(binding),
             "manifest.dataset_id does not bind the ordered source snapshot")

    policy_path = path.parent / "annotation_policy_v1.md"
    _forbid_blind(policy_path, "annotation policy")
    _require(policy_path.is_file(), "manifest: annotation_policy_v1.md is missing")
    policy_raw = policy_path.read_bytes()
    _require(hashlib.sha256(policy_raw).hexdigest() == policy_hash,
             "manifest: annotation policy SHA-256 mismatch")
    return manifest, samples, by_id, policy_path, raw, policy_raw


def _validate_snapshot(manifest_path: Path, manifest: dict[str, Any], *, required: bool) \
        -> bytes | None:
    receipt_path = manifest_path.parent / "snapshot_receipt.json"
    original_path = manifest_path.parent / "manifest_original.json"
    if not receipt_path.exists():
        _require(not required, "formal export requires snapshot_receipt.json")
        return None
    receipt, _ = _json_object(receipt_path, "snapshot receipt")
    _require(original_path.is_file(), "snapshot receipt: manifest_original.json is missing")
    original, original_raw = _json_object(original_path, "original manifest")
    _require(_hex_digest(receipt.get("original_manifest_sha256"),
                         "snapshot_receipt.original_manifest_sha256") ==
             hashlib.sha256(original_raw).hexdigest(),
             "snapshot receipt: original manifest SHA-256 mismatch")
    _require(receipt.get("dataset_id") == manifest["dataset_id"] == original.get("dataset_id"),
             "snapshot receipt: dataset_id mismatch")
    original_samples = original.get("samples")
    current_samples = manifest.get("samples")
    _require(isinstance(original_samples, list) and len(original_samples) == len(current_samples),
             "snapshot receipt: sample count changed")
    for index, (frozen, current) in enumerate(zip(original_samples, current_samples, strict=True)):
        _require(isinstance(frozen, dict), f"manifest_original.samples[{index}]: expected object")
        frozen_source = {key: value for key, value in frozen.items()
                         if key not in DERIVED_SAMPLE_FIELDS and not key.startswith("review_")}
        current_source = {key: value for key, value in current.items()
                          if key not in DERIVED_SAMPLE_FIELDS and not key.startswith("review_")
                          and key != "_raw_path"}
        _require(frozen_source == current_source,
                 f"snapshot receipt: source fields changed for sample {current.get('image_id', index)}")
    return original_raw


def _validate_action(action: Any, sample: dict[str, Any], originals: dict[str, dict[str, Any]],
                     seen: set[str], where: str) -> None:
    _require(isinstance(action, dict), f"{where}: expected object")
    target_id = _string(action.get("target_id"), f"{where}.target_id")
    _require(target_id not in seen, f"{where}: duplicate action target_id {target_id}")
    seen.add(target_id)
    kind = _string(action.get("action"), f"{where}.action")
    _require(kind in ACTIONS, f"{where}: unknown action {kind}")
    label = _string(action.get("class"), f"{where}.class")
    _require(label in CLASSES, f"{where}: unknown class {label}")
    bbox = _box(action.get("bbox"), sample["width"], sample["height"], f"{where}.bbox")
    reason = _string(action.get("reason"), f"{where}.reason", allow_empty=True)
    _require(type(action.get("ai_assisted")) is bool,
             f"{where}.ai_assisted: expected boolean")

    source = originals.get(target_id)
    if kind in {"A", "M", "D"}:
        _require(source is not None, f"{where}: {kind} requires an original target_id")
    if kind == "N":
        _require(source is None, f"{where}: N target_id already exists in original")
    if kind in {"M", "N"}:
        _require(label != "ignore", f"{where}: {kind} cannot create ignore; use I")
    if kind == "I":
        _require(label == "ignore", f"{where}: I requires class=ignore")
    if kind == "A":
        _require(label == source["class"] and bbox == source["bbox"],
                 f"{where}: A must preserve original class and bbox")
    if kind == "D":
        _require(label == source["class"] and bbox == source["bbox"],
                 f"{where}: D must identify the unchanged original target")
    if kind in {"M", "N", "I", "D"}:
        _require(bool(reason.strip()), f"{where}: {kind} requires a reason")


def _validate_patch(path: Path, manifest: dict[str, Any], samples: dict[str, dict[str, Any]]) \
        -> tuple[dict[str, Any], dict[str, dict[str, Any]], bytes]:
    _forbid_blind(path, "patch")
    patch, raw = _json_object(path, "patch")
    _require(patch.get("schema") == PATCH_SCHEMA, "patch: unsupported schema")
    _require(patch.get("dataset_id") == manifest["dataset_id"],
             "patch.dataset_id does not match manifest")
    _require(patch.get("annotation_policy_sha256") == manifest["annotation_policy_sha256"],
             "patch.annotation_policy_sha256 does not match manifest")
    reviews = patch.get("reviews")
    _require(isinstance(reviews, list), "patch.reviews: expected list")

    by_id: dict[str, dict[str, Any]] = {}
    for index, review in enumerate(reviews):
        where = f"patch.reviews[{index}]"
        _require(isinstance(review, dict), f"{where}: expected object")
        image_id = _string(review.get("image_id"), f"{where}.image_id")
        _require(image_id in samples, f"{where}: unknown sample {image_id}")
        _require(image_id not in by_id, f"patch: duplicate review for {image_id}")
        sample = samples[image_id]
        _require(review.get("source_sha256") == sample["source_sha256"],
                 f"{where}: source_sha256 mismatch")
        reviewer = _string(review.get("reviewer"), f"{where}.reviewer", allow_empty=True)
        _require(type(review.get("raw_seen")) is bool, f"{where}.raw_seen: expected boolean")
        _require(type(review.get("complete")) is bool, f"{where}.complete: expected boolean")
        checks = review.get("checks")
        _require(isinstance(checks, dict) and set(checks) == CHECKS,
                 f"{where}.checks: expected exactly six named checks")
        _require(all(type(value) is bool for value in checks.values()),
                 f"{where}.checks: every value must be boolean")
        _string(review.get("notes"), f"{where}.notes", allow_empty=True)
        actions = review.get("actions")
        _require(isinstance(actions, list), f"{where}.actions: expected list")
        originals = {target["target_id"]: target for target in sample["original"]}
        seen: set[str] = set()
        for action_index, action in enumerate(actions):
            _validate_action(action, sample, originals, seen,
                             f"{where}.actions[{action_index}]")

        if review["complete"]:
            _require(bool(reviewer.strip()), f"{where}: complete review needs a human reviewer")
            _require(review["raw_seen"] is True, f"{where}: complete review requires raw_seen=true")
            _require(all(value is True for value in checks.values()),
                     f"{where}: complete review requires all checks=true")
            decisions = {action["target_id"] for action in actions
                         if action["target_id"] in originals
                         and action["action"] in {"A", "M", "I", "D"}}
            _require(decisions == set(originals),
                     f"{where}: every original target needs exactly one A/M/I/D decision")
        by_id[image_id] = review
    return patch, by_id, raw


def _status(samples: list[dict[str, Any]], reviews: dict[str, dict[str, Any]]) -> dict[str, Any]:
    train_ids = [sample["image_id"] for sample in samples if sample["bucket"] == "train_review"]
    complete_train = [image_id for image_id in train_ids
                      if image_id in reviews and reviews[image_id]["complete"]]
    pending_train = [image_id for image_id in train_ids if image_id not in complete_train]
    return {
        "status": "validated_ready" if not pending_train else "validated_pending",
        "verified_generated": False,
        "training_started": False,
        "train_required_count": len(train_ids),
        "train_complete_count": len(complete_train),
        "pending_train_count": len(pending_train),
        "pending_train_image_ids": pending_train,
        "review_states": dict(Counter(
            "complete" if review["complete"] else "pending" for review in reviews.values())),
    }


def _build_verified(manifest: dict[str, Any], samples: list[dict[str, Any]],
                    reviews: dict[str, dict[str, Any]], manifest_path: Path,
                    patch_path: Path, policy_path: Path, original_manifest_hash: str,
                    review_manifest_hash: str, patch_hash: str) \
        -> tuple[dict[str, Any], dict[str, Any]]:
    images = []
    stats = Counter()
    risk_text: list[str] = []
    for sample in samples:
        if sample["bucket"] != "train_review":
            continue
        review = reviews[sample["image_id"]]
        originals = {target["target_id"]: target for target in sample["original"]}
        labels = []
        stats["original"] += len(originals)
        risk_text.append(review["notes"].lower())
        for action in review["actions"]:
            kind = action["action"]
            stats[{"A": "accepted_original", "M": "modified", "N": "added",
                   "I": "ignored", "D": "deleted"}[kind]] += 1
            if action["ai_assisted"]:
                stats["ai_suggestions_checked"] += 1
                if kind in {"A", "M", "N"} and action["class"] != "ignore":
                    stats["ai_suggestions_accepted"] += 1
            risk_text.append(action["reason"].lower())
            if kind == "D":
                continue
            labels.append({
                "target_id": action["target_id"],
                "class": action["class"],
                "bbox": action["bbox"],
                "source": "manual_review",
                "action": kind,
                "ai_assisted": action["ai_assisted"],
                "original_target_id": action["target_id"] if action["target_id"] in originals else None,
            })
        images.append({
            "image_id": sample["image_id"],
            "legacy_id": sample["legacy_id"],
            "bucket": sample["bucket"],
            "split": sample["split"],
            "width": sample["width"],
            "height": sample["height"],
            "raw_file_absolute": str(sample["_raw_path"]),
            "source_sha256": sample["source_sha256"],
            "manual_review": {key: review[key] for key in
                              ("reviewer", "raw_seen", "complete", "checks", "notes")},
            "labels": labels,
            **{key: sample[key] for key in
               ("source_scene_id", "camera_id", "frame_index", "source_metadata")
               if key in sample},
        })
    risk_joined = "\n".join(risk_text)
    risk = {
        "rider_log_matches": sum(risk_joined.count(word) for word in ("rider", "骑行")),
        "parked_vehicle_log_matches": sum(risk_joined.count(word) for word in
                                          ("parked", "停放", "静止车辆")),
    }
    risk["expanded_review_required"] = any(risk.values())
    verified = {
        "schema": OUTPUT_SCHEMA,
        "dataset_id": manifest["dataset_id"],
        "annotation_policy_sha256": manifest["annotation_policy_sha256"],
        "scope": {"bucket": "train_review", "split": "train", "image_count": len(images)},
        "source_chain": {
            "original_manifest": {
                "path": str((manifest_path.parent / "manifest_original.json").resolve()),
                "sha256": original_manifest_hash,
            },
            "review_manifest": {"path": str(manifest_path.resolve()),
                                "sha256": review_manifest_hash},
            "manual_patch": {"path": str(patch_path.resolve()), "sha256": patch_hash},
            "annotation_policy": {"path": str(policy_path.resolve()),
                                  "sha256": manifest["annotation_policy_sha256"]},
        },
        "images": images,
    }
    return verified, {"scope": "train_review", **stats, "systematic_review_signal": risk}


def import_review(manifest_path: Path, patch_path: Path, output: Path,
                  *, validate_only: bool = False) -> dict[str, Any]:
    manifest_path, patch_path, output = map(Path, (manifest_path, patch_path, output))
    _forbid_blind(output, "output")
    _require(not output.exists(), f"output already exists: {output}")
    manifest, sample_list, samples, policy_path, manifest_raw, policy_raw = \
        _validate_manifest(manifest_path)
    original_manifest_raw = _validate_snapshot(manifest_path, manifest,
                                               required=not validate_only)
    patch, reviews, patch_raw = _validate_patch(patch_path, manifest, samples)
    status = _status(sample_list, reviews)
    if validate_only:
        return status
    _require(not status["pending_train_count"],
             f"cannot export: {status['pending_train_count']} train reviews are pending")

    manifest_hash = hashlib.sha256(manifest_raw).hexdigest()
    original_manifest_hash = hashlib.sha256(original_manifest_raw).hexdigest()
    patch_hash = hashlib.sha256(patch_raw).hexdigest()
    verified, stats = _build_verified(manifest, sample_list, reviews, manifest_path,
                                      patch_path, policy_path, original_manifest_hash,
                                      manifest_hash, patch_hash)
    output.mkdir(parents=True, exist_ok=False)
    (output / "manifest_original.json").write_bytes(original_manifest_raw)
    (output / "review_manifest.json").write_bytes(manifest_raw)
    (output / "review_patch.json").write_bytes(patch_raw)
    (output / "annotation_policy_v1.md").write_bytes(policy_raw)
    labels_path = output / "labels_verified.json"
    labels_path.write_text(json.dumps(verified, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    receipt = {
        "schema": "cnn_verified_import_receipt_v1",
        "status": "verified_gt_generated",
        "dataset_id": manifest["dataset_id"],
        "verified_training_subset": True,
        "training_started": False,
        "formal_acceptance": False,
        "stats": stats,
        "frozen_inputs": {
            "original_manifest_sha256": original_manifest_hash,
            "review_manifest_sha256": manifest_hash,
            "patch_sha256": patch_hash,
            "annotation_policy_sha256": manifest["annotation_policy_sha256"],
        },
        "outputs": {"labels_verified_sha256": sha256_file(labels_path)},
        "evidence_boundary": [
            "Only the 128 train_review images are exported for training.",
            "This does not verify the full 19050-image corpus.",
            "road_development may remain pending and is never exported for training.",
            "person_background_aux stress samples are never exported for training.",
            "Scene-isolated validation truth remains a gate before training or formal acceptance.",
        ],
    }
    (output / "import_receipt.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return receipt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--patch", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = import_review(args.manifest, args.patch, args.output,
                               validate_only=args.validate_only)
    except ReviewError as exc:
        print(json.dumps({"status": "rejected", "error": str(exc)}, ensure_ascii=False),
              file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
