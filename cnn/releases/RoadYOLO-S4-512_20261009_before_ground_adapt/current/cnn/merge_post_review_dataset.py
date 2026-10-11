"""Merge authorized train annotations into a NEW bounded-development dataset.

Never exports road/stress images, fits a model, or edits the original manifests.
Unreviewed source rows and ALL original validation rows remain unchanged.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import time

from .dataset import _refuse_blind, audit, sha256_file
from .import_verified_review import CHECKS, import_review
from .prepare_verified_train import convert_frame


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "cnn/data/visdrone_vid_train/raw_manifest/dataset.json"
VERIFIED = ROOT / "cnn/reports/verified_gt_amendment_20261007/verified_labels"
SOURCE_SHA = "ad353c5bce5b0ecef0433c74515324bbfdb031e92aff964cd56c18ae069d9fe4"
LABELS_SHA = "03eea1385a6f33a3431dde4304733277a09578f6e89dde54014a793befdf2065"


def json_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=True,
                                    separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def write_new(path, value):
    """Publish complete JSON only; interrupted files stay visibly pending."""
    if path.exists():
        raise FileExistsError(path)
    pending = path.with_name(path.name + ".pending")
    with pending.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    pending.rename(path)


def source_key(row):
    # This source is the frozen VisDrone VID manifest, whose native frames are one-based.
    frame = row.get("source_frame")
    if (not isinstance(row.get("scene_id"), str) or type(frame) is not int or frame < 1
            or not Path(row["image"]).stem.isdigit()
            or int(Path(row["image"]).stem) != frame):
        raise ValueError("source native frame identity is ambiguous")
    return row["scene_id"], frame


def same_box(first, second):
    return len(first) == len(second) == 4 and all(abs(a-b) <= 1e-5
                                                for a, b in zip(first, second))


def reviewed_payload(original, image):
    review = image.get("manual_review", {})
    if (image.get("bucket") != "train_review" or image.get("split") != "train"
            or review.get("complete") is not True or review.get("raw_seen") is not True
            or not str(review.get("reviewer", "")).strip()
            or set(review.get("checks", {})) != CHECKS
            or any(value is not True for value in review["checks"].values())):
        raise ValueError("review is not explicitly complete and train-only")
    if image.get("source_metadata", {}).get("frame_base") != 1:
        raise ValueError("reviewed native frame base must be explicit and one-based")
    if original["source_sha256"] != image["source_sha256"]:
        raise ValueError("reviewed pixels differ from the matched original source")
    converted = convert_frame(image)
    if (converted["preprocess"]["letterbox_1280x720"]
            != original["preprocess"]["letterbox_1280x720"]):
        raise ValueError("reviewed and original preprocessing differ")
    metadata = original.get("ignore_metadata", [])
    if len(metadata) != len(original["ignore_boxes"]):
        raise ValueError("original ignore metadata does not align")
    ignore_metadata = []
    for box in converted["ignore_boxes"]:
        inherited = [item for old_box, item in zip(original["ignore_boxes"], metadata)
                     if same_box(box, old_box)]
        if len(inherited) > 1 and any(item != inherited[0] for item in inherited):
            raise ValueError("ambiguous original ignore metadata")
        ignore_metadata.append(dict(inherited[0]) if inherited else
                               dict(label=-1, crowd=False, source="manual_ignore"))
    result = dict(original)
    result.update(boxes=converted["boxes"], labels=converted["labels"],
                  ignore_boxes=converted["ignore_boxes"], ignore_metadata=ignore_metadata,
                  annotation_review_status="reviewed_then_user_authorized_amendment",
                  manual_review_image_id=image["image_id"], manual_review=review,
                  reviewed_labels_sha256=json_hash(image["labels"]),
                  native_frame_index=image["frame_index"], source_frame_base=1,
                  completeness_basis="signed_manual_review_plus_authorized_amendment",
                  rider_box_policy_review_required=False)
    # Keep original image/key/preprocess/frame fields so cached RGB can be shared safely.
    return result


def merge_document(source, verified, *, expected_reviewed=128, exclude="train_075"):
    if (source.get("training_eligible") is not True
            or source.get("classes") != ["person", "vehicle"]
            or source.get("input_size") != [512, 288]
            or any(row.get("split") not in {"train", "val"}
                   for row in source.get("images", []))):
        raise ValueError("only the complete source-declared development corpus is allowed")
    reviewed = verified.get("images", [])
    if verified.get("schema") != "cnn_verified_labels_v1" or len(reviewed) != expected_reviewed:
        raise ValueError("unexpected verified training subset")
    by_key = {}
    for image in reviewed:
        key = image["source_scene_id"], image["frame_index"]
        if key in by_key:
            raise ValueError("duplicate reviewed native frame")
        # Check excluded review too; exclusion must not hide a malformed or unsigned patch.
        if image.get("bucket") != "train_review" or image.get("split") != "train":
            raise ValueError("road/stress images are forbidden in training merge")
        by_key[key] = image
    rows, seen, replaced, excluded = [], set(), [], []
    unreviewed = 0
    for original in source["images"]:
        _refuse_blind(Path(original["image"]))
        key = source_key(original)
        if key in seen:
            raise ValueError("duplicate source native frame")
        seen.add(key)
        image = by_key.get(key)
        if image is None:
            rows.append(original)
            unreviewed += original["split"] == "train"
            continue
        if original["split"] != "train":
            raise ValueError("reviewed frame would modify validation")
        amended = reviewed_payload(original, image)
        item = dict(image=original["image"], image_id=image["image_id"],
                    legacy_id=image["legacy_id"], scene_id=key[0], native_frame_index=key[1],
                    source_sha256=original["source_sha256"],
                    original_row_sha256=json_hash(original))
        if image["legacy_id"] == exclude:
            excluded.append(dict(item, reason="unresolved_o58_o59_overlap_whole_frame_exclusion"))
        else:
            rows.append(amended)
            replaced.append(dict(item, amended_row_sha256=json_hash(amended)))
    if set(by_key) - seen or len(excluded) != 1 or len(replaced) != expected_reviewed-1:
        raise ValueError("every review must match uniquely; exactly one whole-frame exclusion required")
    old_val = [row for row in source["images"] if row["split"] == "val"]
    new_val = [row for row in rows if row["split"] == "val"]
    if new_val != old_val:
        raise ValueError("validation rows changed")
    document = dict(source, images=rows,
                    manifest_status="mixed_source_and_reviewed_bounded_development",
                    purpose="post_review_S_bounded_development_not_formal_acceptance",
                    formal_acceptance=False,
                    annotation_review_scope=dict(
                        default_train_status="source_declared_unreviewed",
                        amended_train_images=len(replaced), unreviewed_train_images=unreviewed,
                        excluded_image_ids=[item["image_id"] for item in excluded],
                        validation_status="original_source_declared_regression_unchanged"))
    measurement = audit(document)
    if measurement["incomplete_frames"]:
        raise ValueError("incomplete frame cannot become negative supervision")
    return document, dict(matched_reviewed=len(replaced)+len(excluded), replaced=replaced,
                         excluded=excluded, unreviewed_train_images=unreviewed,
                         original_val_rows_sha256=json_hash(old_val),
                         output_val_rows_sha256=json_hash(new_val), audit=measurement)


def prepare(source_path, verified_dir, output_dir, report_path):
    started = time.perf_counter()
    for path in (source_path, verified_dir, output_dir, report_path):
        _refuse_blind(path)
    if output_dir.exists() or report_path.exists():
        raise FileExistsError("new output directory and receipt required")
    labels_path = verified_dir / "labels_verified.json"
    import_path = verified_dir / "import_receipt.json"
    if sha256_file(source_path) != SOURCE_SHA or sha256_file(labels_path) != LABELS_SHA:
        raise ValueError("not the approved original corpus and authorized revised labels")
    source = json.loads(source_path.read_text(encoding="utf-8"))
    verified = json.loads(labels_path.read_text(encoding="utf-8"))
    receipt = json.loads(import_path.read_text(encoding="utf-8"))
    if receipt["outputs"]["labels_verified_sha256"] != LABELS_SHA:
        raise ValueError("verified-label receipt mismatch")
    chain = verified["source_chain"]
    for item in chain.values():
        path = Path(item["path"])
        _refuse_blind(path)
        if sha256_file(path) != item["sha256"]:
            raise ValueError("verified source-chain hash mismatch")
    validation = import_review(Path(chain["review_manifest"]["path"]),
                               Path(chain["manual_patch"]["path"]),
                               output_dir / "not_exported", validate_only=True)
    if validation["pending_train_count"] or validation["train_complete_count"] != 128:
        raise ValueError("manual training review not complete")
    for image in verified["images"]:
        path = Path(image["raw_file_absolute"])
        _refuse_blind(path)
        if sha256_file(path) != image["source_sha256"]:
            raise ValueError("reviewed original-image bytes changed")
    document, result = merge_document(source, verified)
    counts = Counter(row["split"] for row in document["images"])
    if counts != Counter(train=19049, val=5151) or result["unreviewed_train_images"] != 18922:
        raise ValueError("approved merge counts differ")
    for row in source["images"]:
        if not Path(row["image"]).is_absolute():
            raise ValueError("source paths must remain absolute when changing manifest location")
    if sha256_file(source_path) != SOURCE_SHA or sha256_file(labels_path) != LABELS_SHA:
        raise ValueError("input changed during merge")
    output_dir.mkdir(parents=True, exist_ok=False)
    manifest_path = output_dir / "dataset_train_val.json"
    document["source_bindings"] = dict(source_manifest_sha256=SOURCE_SHA,
                                        authorized_labels_sha256=LABELS_SHA,
                                        import_receipt_sha256=sha256_file(import_path))
    write_new(manifest_path, document)
    result.update(status="merged_development_only_ground48_truth_pending",
                  dataset_path=str(manifest_path.resolve()), dataset_sha256=sha256_file(manifest_path),
                  source_manifest_sha256=SOURCE_SHA, authorized_labels_sha256=LABELS_SHA,
                  import_receipt_sha256=sha256_file(import_path),
                  source_sha256=sha256_file(Path(__file__)),
                  train_images=19049, val_images=5151, GPU_used=False, optimizer_updates=0,
                  training_started=False, formal_acceptance=False,
                  exclusion_authorization="2026-10-07 user approved execution of v2 plan",
                  elapsed_seconds=time.perf_counter()-started,
                  boundary="127 reviewed amendments; 18922 source-only; old val unchanged; no fitting")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    write_new(report_path, result)
    print(json.dumps({key: result[key] for key in
                     ("status", "train_images", "val_images", "matched_reviewed",
                      "unreviewed_train_images", "dataset_sha256", "elapsed_seconds")}))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--verified", type=Path, default=VERIFIED)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    prepare(args.source, args.verified, args.output, args.report)


if __name__ == "__main__":
    main()
