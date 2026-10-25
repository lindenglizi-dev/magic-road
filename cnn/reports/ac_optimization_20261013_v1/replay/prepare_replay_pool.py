"""Build a fixed replay pool from the 127 signed VisDrone train amendments.

This reads the compact review/merge receipts.  It hashes the 410 MB original
manifest but deliberately does not parse it; the merge receipt already binds
each approved replacement to that exact manifest and source row.
"""
from __future__ import annotations

from collections import Counter, defaultdict
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

from cnn.dataset import _letterbox_transform, _letterboxed_box, audit, sha256_file


HERE = Path(__file__).resolve().parent
RAW_MANIFEST = ROOT / "cnn/data/visdrone_vid_train/raw_manifest/dataset.json"
MERGE_RECEIPT = ROOT / "cnn/reports/post_review_s_20261007_v1/merge_receipt.json"
VERIFIED_DIR = ROOT / "cnn/reports/verified_gt_amendment_20261007/verified_labels"
VERIFIED_LABELS = VERIFIED_DIR / "labels_verified.json"
IMPORT_RECEIPT = VERIFIED_DIR / "import_receipt.json"
CURRENT_DATASET = ROOT / "cnn/reports/ac_g10_20261013_v1/dataset.json"
TRAINING_CONTRACT = ROOT / "cnn/reports/ac_bnfreeze_g10_20261013_v1/training_contract.json"
OLD256_BASELINE = ROOT / "cnn/reports/person_native_recovery_20261004/epoch_7_val256.json"
OUTPUT_MANIFEST = HERE / "replay64_manifest.json"
OUTPUT_RECEIPT = HERE / "selection_receipt.json"
OUTPUT_NOTE = HERE / "selection_explanation_zh.txt"
EXPECTED_CHECKS = {"person", "vehicle", "rider", "parked_vehicle", "small_occluded", "ignore"}
DATASET_FAMILY = "VisDrone2019-VID-train"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def json_hash(value) -> str:
    payload = json.dumps(value, ensure_ascii=True, sort_keys=True,
                         separators=(",", ":"), allow_nan=False).encode()
    return hashlib.sha256(payload).hexdigest()


def stable_key(seed: int, *parts: object) -> str:
    return hashlib.sha256(":".join((str(seed), *(str(p) for p in parts))).encode()).hexdigest()


def family_of(row: dict) -> str:
    text = " ".join(str(row.get(key, "")) for key in ("scene_id", "camera_id", "image")).lower()
    for needle, family in (("visdrone", DATASET_FAMILY), ("epfl", "EPFL"),
                           ("virat", "VIRAT"), ("pets", "PETS09")):
        if needle in text:
            return family
    return "unknown:" + hashlib.sha256(text.encode()).hexdigest()[:12]


def visdrone_prefix(value: str) -> str:
    """Conservative family proxy: uav0000123 from uav0000123_04567_v."""
    name = Path(value).name
    return name.split("_", 1)[0] if name.startswith("uav") and "_" in name else name


def failed_checks(checks: dict) -> list[str]:
    return [
        key for key, value in checks.items()
        if ((isinstance(value, bool) and not value)
            or (isinstance(value, int) and not isinstance(value, bool) and value != 0)
            or (isinstance(value, list) and value))
    ]


def select_round_robin(rows: list[dict], target: int, seed: int) -> list[dict]:
    """Maximize scene coverage, then take a deterministic second pass."""
    by_scene: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_scene[row["source_scene_id"]].append(row)
    for scene, items in by_scene.items():
        items.sort(key=lambda row: stable_key(seed, scene, row["source_sha256"], row["image_id"]))
    scenes = sorted(by_scene, key=lambda scene: stable_key(seed, scene))
    selected = []
    while len(selected) < min(target, len(rows)):
        progressed = False
        for scene in scenes:
            if by_scene[scene]:
                item = dict(by_scene[scene].pop(0))
                item["selection_round"] = 1 + sum(
                    old["source_scene_id"] == scene for old in selected)
                selected.append(item)
                progressed = True
                if len(selected) == min(target, len(rows)):
                    break
        if not progressed:
            break
    return selected


def require_signed_review(image: dict) -> None:
    review = image.get("manual_review", {})
    checks = review.get("checks", {})
    if (image.get("bucket") != "train_review" or image.get("split") != "train"
            or review.get("complete") is not True or review.get("raw_seen") is not True
            or not str(review.get("reviewer", "")).strip()
            or set(checks) != EXPECTED_CHECKS or any(value is not True for value in checks.values())
            or image.get("source_metadata", {}).get("frame_base") != 1):
        raise ValueError(f"unsigned or incomplete review: {image.get('image_id')}")


def manifest_row(image: dict, merged: dict, rank: int) -> dict:
    transform = _letterbox_transform(image["width"], image["height"])
    boxes, labels, ignore_boxes = [], [], []
    for label in image["labels"]:
        x1, y1, x2, y2 = label["bbox"]
        box = _letterboxed_box([x1, y1, x2 - x1, y2 - y1], transform)
        if label["class"] == "ignore":
            ignore_boxes.append(box)
        elif label["class"] in {"person", "vehicle"}:
            boxes.append(box)
            labels.append({"person": 0, "vehicle": 1}[label["class"]])
        else:
            raise ValueError(f"unknown class in {image['image_id']}: {label['class']}")
    return {
        "image": str(Path(merged["image"]).resolve()),
        "source_sha256": image["source_sha256"],
        "scene_id": image["source_scene_id"],
        "camera_id": image["camera_id"],
        "dataset_family": DATASET_FAMILY,
        "video_family_id": image["source_scene_id"],
        "source_frame": image["frame_index"],
        "source_frame_base": 1,
        "native_frame_index": image["frame_index"],
        "split": "train",
        "incomplete_frame": False,
        "annotation_complete": True,
        "boxes": boxes,
        "labels": labels,
        "ignore_boxes": ignore_boxes,
        "preprocess": {"raw_image": True, "letterbox_1280x720": transform,
                       "resize": "integer.resize_area_5_to_2_RNE"},
        "teacher_key": image["image_id"],
        "manual_review_image_id": image["image_id"],
        "legacy_id": image["legacy_id"],
        "annotation_review_status": "reviewed_then_user_authorized_amendment",
        "completeness_basis": "signed_manual_review_plus_authorized_amendment",
        "review_evidence": {
            "reviewer": image["manual_review"]["reviewer"],
            "raw_seen": True,
            "all_six_checks_passed": True,
            "reviewed_labels_sha256": json_hash(image["labels"]),
            "merged_amended_row_sha256": merged["amended_row_sha256"],
            "visual_quality_status": "reviewer_signed_not_independently_reinspected_for_replay",
        },
        "replay_selection_rank": rank,
        "replay_selection_round": image["selection_round"],
    }


def atomic_write(path: Path, value: str) -> None:
    pending = path.with_suffix(path.suffix + ".pending")
    pending.write_text(value, encoding="utf-8")
    os.replace(pending, path)


def self_test() -> None:
    rows = [
        {"source_scene_id": scene, "source_sha256": str(index) * 64, "image_id": f"i{index}"}
        for index, scene in enumerate(("a", "a", "b", "b", "c"), 1)
    ]
    first = select_round_robin(rows, 4, 42)
    second = select_round_robin(rows, 4, 42)
    assert first == second and len(first) == 4
    assert len({row["source_scene_id"] for row in first[:3]}) == 3
    assert [row["selection_round"] for row in first[:3]] == [1, 1, 1]
    assert first[3]["selection_round"] == 2
    assert failed_checks({"all_ok": True, "overlap": 0, "names": []}) == []
    assert failed_checks({"all_ok": False}) == ["all_ok"]  # False must not pass as integer zero.
    print("self-test PASS")


def build(target: int = 64, seed: int = 42) -> dict:
    merge = read_json(MERGE_RECEIPT)
    verified = read_json(VERIFIED_LABELS)
    imported = read_json(IMPORT_RECEIPT)
    current = read_json(CURRENT_DATASET)
    contract = read_json(TRAINING_CONTRACT)
    old256 = read_json(OLD256_BASELINE)

    if sha256_file(RAW_MANIFEST) != merge["source_manifest_sha256"]:
        raise ValueError("original 410 MB source manifest differs from merge receipt")
    if sha256_file(VERIFIED_LABELS) != merge["authorized_labels_sha256"]:
        raise ValueError("verified labels differ from merge receipt")
    if imported["outputs"]["labels_verified_sha256"] != merge["authorized_labels_sha256"]:
        raise ValueError("review import receipt is not the merge input")
    if merge["matched_reviewed"] != 128 or len(merge["replaced"]) != 127 or len(merge["excluded"]) != 1:
        raise ValueError("expected 127 replacements and one explicit exclusion")
    if merge["excluded"][0]["legacy_id"] != "train_075":
        raise ValueError("unexpected excluded review")
    if verified.get("schema") != "cnn_verified_labels_v1" or len(verified.get("images", [])) != 128:
        raise ValueError("unexpected verified-label package")
    if (old256.get("split") != "val" or old256.get("image_count") != 256
            or old256.get("dataset_sha256") != merge["source_manifest_sha256"]):
        raise ValueError("old256 is not the fixed original validation subset")

    replaced = {item["image_id"]: item for item in merge["replaced"]}
    verified_by_id = {item["image_id"]: item for item in verified["images"]}
    if len(replaced) != 127 or len(verified_by_id) != 128 or set(replaced) - set(verified_by_id):
        raise ValueError("review/merge identities do not join one-to-one")

    current_hashes = defaultdict(set)
    current_paths = defaultdict(set)
    current_families = defaultdict(set)
    for row in current["images"]:
        path = Path(row["image"]).resolve()
        if sha256_file(path) != row["source_sha256"]:
            raise ValueError(f"current ac_g10 image hash changed: {path}")
        current_hashes[row["split"]].add(row["source_sha256"])
        current_paths[row["split"]].add(str(path).casefold())
        current_families[row["split"]].add(family_of(row))

    old256_paths = {
        str(Path(item["image_id"]).resolve()).casefold()
        for key in ("truth", "ignores", "predictions") for item in old256[key]
    }
    if len(old256_paths) != 256:
        raise ValueError("old256 report does not identify exactly 256 images")
    old256_hashes = set()
    old256_sequences = set()
    for text in old256_paths:
        path = Path(text)
        if not path.is_file():
            raise FileNotFoundError(path)
        old256_hashes.add(sha256_file(path))
        old256_sequences.add(path.parent.name)
    if len(old256_hashes) != 256:
        raise ValueError("old256 images are not content-unique")
    old256_prefixes = {visdrone_prefix(scene) for scene in old256_sequences}
    all_old_val_scenes = {
        scene.removeprefix("visdrone-vid-") for scene in merge["audit"]["scenes_by_split"]["val"]
    }
    all_old_val_prefixes = {visdrone_prefix(scene) for scene in all_old_val_scenes}

    eligible = []
    for image_id, merged in replaced.items():
        image = verified_by_id[image_id]
        require_signed_review(image)
        if (image["source_scene_id"] != merged["scene_id"]
                or image["frame_index"] != merged["native_frame_index"]
                or image["source_sha256"] != merged["source_sha256"]):
            raise ValueError(f"review/merge source identity mismatch: {image_id}")
        source_path = Path(merged["image"]).resolve()
        if source_path.stem != f"{image['frame_index']:07d}":
            raise ValueError(f"ambiguous native frame filename: {source_path}")
        if sha256_file(source_path) != image["source_sha256"]:
            raise ValueError(f"reviewed source bytes changed: {source_path}")
        if any(image["source_sha256"] in hashes for hashes in current_hashes.values()):
            continue
        if any(str(source_path).casefold() in paths for paths in current_paths.values()):
            continue
        if (image["source_sha256"] in old256_hashes
                or str(source_path).casefold() in old256_paths
                or visdrone_prefix(image["source_scene_id"].removeprefix("visdrone-vid-"))
                in all_old_val_prefixes):
            continue
        eligible.append(image)

    if len({item["source_sha256"] for item in eligible}) != len(eligible):
        raise ValueError("eligible reviewed images are not content-unique")
    chosen = select_round_robin(eligible, target, seed)
    rows = [manifest_row(image, replaced[image["image_id"]], rank)
            for rank, image in enumerate(chosen, 1)]
    selected_hashes = {row["source_sha256"] for row in rows}
    selected_paths = {str(Path(row["image"]).resolve()).casefold() for row in rows}
    selected_scenes = {row["scene_id"] for row in rows}
    selected_sequences = {scene.removeprefix("visdrone-vid-") for scene in selected_scenes}
    selected_prefixes = {visdrone_prefix(scene) for scene in selected_sequences}
    selected_families = {row["dataset_family"] for row in rows}
    if selected_families & set().union(*current_families.values()):
        raise ValueError("dataset-family overlap with ac_g10")

    manifest = {
        "schema_version": 1,
        "task": "detection",
        "input_size": [512, 288],
        "classes": ["person", "vehicle"],
        "dataset_id": "ac_optimization_replay64_reviewed_visdrone_seed42_v1",
        "manifest_status": "fixed_candidate_replay_pool_not_launchable_alone",
        "purpose": "old_train_replay_candidate_pool_only",
        "training_eligible": False,
        "formal_acceptance": False,
        "selection_seed": seed,
        "selection_method": "scene_round_robin_then_sha256_rank",
        "source_bindings": {
            "original_train_manifest": str(RAW_MANIFEST),
            "original_train_manifest_sha256": merge["source_manifest_sha256"],
            "reviewed_labels": str(VERIFIED_LABELS),
            "reviewed_labels_sha256": merge["authorized_labels_sha256"],
            "merge_receipt": str(MERGE_RECEIPT),
            "merge_receipt_sha256": sha256_file(MERGE_RECEIPT),
            "current_ac_g10_dataset": str(CURRENT_DATASET),
            "current_ac_g10_dataset_sha256": sha256_file(CURRENT_DATASET),
            "old256_baseline": str(OLD256_BASELINE),
            "old256_baseline_sha256": sha256_file(OLD256_BASELINE),
        },
        "annotation_evidence": {
            "status": "reviewer_signed_and_user_authorized",
            "visual_quality_status": "not_independently_reinspected_for_replay_selection",
            "unreviewed_source_rows_allowed": False,
            "excluded_legacy_ids": [item["legacy_id"] for item in merge["excluded"]],
        },
        "images": rows,
    }
    measurement = audit(manifest)
    if measurement["incomplete_frames"] or measurement["images_by_split"] != {"train": len(rows)}:
        raise ValueError("replay manifest audit failed")

    command = contract["command"]
    checkpoint = Path(command[command.index("--init-checkpoint") + 1])
    if sha256_file(checkpoint) != contract["initializer_sha256"]:
        raise ValueError("frozen E7 initializer differs from training contract")

    atomic_write(OUTPUT_MANIFEST, json.dumps(manifest, ensure_ascii=False, indent=2, allow_nan=False) + "\n")
    receipt = {
        "schema": "cnn_replay_pool_selection_receipt_v1",
        "status": "fixed_replay_pool_ready" if len(rows) == target else "reliable_pool_shortfall",
        "target_size": target,
        "selected_size": len(rows),
        "shortfall": max(0, target - len(rows)),
        "seed": seed,
        "selection_method": manifest["selection_method"],
        "eligible_signed_replacements": len(eligible),
        "selected_scene_count": len(selected_scenes),
        "selected_scenes": sorted(selected_scenes),
        "selected_class_box_counts": measurement["class_box_counts"]["train"],
        "review_boundary": {
            "reviewer_signed_replacements": 127,
            "explicitly_excluded": 1,
            "unreviewed_original_train_not_considered": merge["unreviewed_train_images"],
            "visual_quality": "prior reviewer signed raw_seen; no independent replay-specific visual reinspection",
        },
        "source_identity": {
            "dataset_family": DATASET_FAMILY,
            "video_family_key": "scene_id",
            "source_manifest_path": str(RAW_MANIFEST),
            "source_manifest_sha256": merge["source_manifest_sha256"],
            "reviewed_labels_sha256": merge["authorized_labels_sha256"],
            "merge_receipt_sha256": sha256_file(MERGE_RECEIPT),
        },
        "current_dataset": {
            "path": str(CURRENT_DATASET),
            "sha256": sha256_file(CURRENT_DATASET),
            "split_counts": dict(sorted(Counter(row["split"] for row in current["images"]).items())),
            "families_by_split": {split: sorted(values)
                                  for split, values in sorted(current_families.items())},
        },
        "old256_validation": {
            "report": str(OLD256_BASELINE),
            "report_sha256": sha256_file(OLD256_BASELINE),
            "image_count": len(old256_paths),
            "video_sequences": sorted(old256_sequences),
            "uav_prefix_family_proxy": sorted(old256_prefixes),
            "all_original_val_scenes": sorted(all_old_val_scenes),
            "all_original_val_uav_prefix_family_proxy": sorted(all_old_val_prefixes),
            "dataset_family": DATASET_FAMILY,
            "limitation": "uavNNNN prefix is a conservative name-derived proxy; physical camera identity is not verified",
        },
        "checks": {
            "all_selected_source_split_train": all(row["split"] == "train" for row in rows),
            "all_selected_reviewer_signed": len(rows) == len(chosen),
            "all_selected_pixel_hashes_verified": True,
            "selected_hashes_unique": len(selected_hashes) == len(rows),
            "selected_paths_unique": len(selected_paths) == len(rows),
            "selected_dataset_family_overlap_current": sorted(
                selected_families & set().union(*current_families.values())),
            "selected_scene_overlap_current": sorted(
                selected_scenes & {row["scene_id"] for row in current["images"]}),
            "selected_content_overlap_current_train": len(selected_hashes & current_hashes["train"]),
            "selected_content_overlap_current_val": len(selected_hashes & current_hashes["val"]),
            "selected_content_overlap_current_newtest": len(selected_hashes & current_hashes["newtest"]),
            "selected_path_overlap_current_train": len(selected_paths & current_paths["train"]),
            "selected_path_overlap_current_val": len(selected_paths & current_paths["val"]),
            "selected_path_overlap_current_newtest": len(selected_paths & current_paths["newtest"]),
            "selected_content_overlap_old256": len(selected_hashes & old256_hashes),
            "selected_path_overlap_old256": len(selected_paths & old256_paths),
            "selected_video_sequence_overlap_old256": sorted(selected_sequences & old256_sequences),
            "selected_uav_prefix_overlap_old256": sorted(selected_prefixes & old256_prefixes),
            "selected_video_sequence_overlap_all_old_val": sorted(selected_sequences & all_old_val_scenes),
            "selected_uav_prefix_overlap_all_old_val": sorted(selected_prefixes & all_old_val_prefixes),
        },
        "audit": measurement,
        "frozen_E7": {
            "checkpoint": str(checkpoint),
            "sha256": contract["initializer_sha256"],
            "training_contract": str(TRAINING_CONTRACT),
            "training_contract_sha256": sha256_file(TRAINING_CONTRACT),
        },
        "outputs": {
            "manifest": str(OUTPUT_MANIFEST),
            "manifest_sha256": sha256_file(OUTPUT_MANIFEST),
        },
        "execution_boundary": {
            "model_loaded": False,
            "training_started": False,
            "GPU_used": False,
            "labels_edited": False,
            "sampler_or_trainer_modified": False,
            "original_410MB_manifest_parsed": False,
        },
        "source_script_sha256": sha256_file(Path(__file__)),
    }
    failures = failed_checks(receipt["checks"])
    if failures:
        raise ValueError(f"isolation checks failed: {failures}")
    atomic_write(OUTPUT_RECEIPT, json.dumps(receipt, ensure_ascii=False, indent=2, allow_nan=False) + "\n")
    note = (
        f"固定旧样本重放池：目标 {target} 张，实际 {len(rows)} 张，短缺 {receipt['shortfall']} 张。\n"
        f"来源：原始 VisDrone2019-VID-train 的 train split；只采用合并收据中 127 张人工签署、"
        "已查看 RAW、六项检查通过且用户授权替换的图，明确排除 train_075，未使用 18,922 张未复核源标签。\n"
        f"选择：seed={seed}，先按 scene 轮转覆盖，再按稳定 SHA256 顺序补足；共覆盖 {len(selected_scenes)} 个视频 scene。\n"
        "隔离：与当前 ac_g10 的 22 张 train、17 张 val（无 newtest）在像素 SHA256、绝对路径、scene、"
        "数据族上均无交集；当前数据族为 EPFL/PETS09/VIRAT，旧池为 VisDrone2019-VID-train。\n"
        "旧验证隔离：与固定 old256 的像素、路径、视频 sequence、uavNNNN 前缀均无交集；"
        "对全部原始 val 只核验了视频 sequence 与 uavNNNN 前缀无交集，未逐图比较其余像素或路径。"
        "其中 uavNNNN 只是从名称推导的保守家族代理，不能证明真实物理摄像机身份。\n"
        "证据边界：这些帧已有历史人工签署，但本轮没有重新逐图目视检查，因此只能称 reviewer-signed，"
        "不能声称 replay 专项视觉质量已再次验证。未加载模型、未训练、未用 GPU、未改标签、未改采样器或训练器。\n"
    )
    atomic_write(OUTPUT_NOTE, note)
    print(json.dumps({key: receipt[key] for key in
                     ("status", "target_size", "selected_size", "shortfall",
                      "eligible_signed_replacements", "selected_scene_count")}, ensure_ascii=False))
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=int, default=64)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        build(args.target, args.seed)


if __name__ == "__main__":
    main()
