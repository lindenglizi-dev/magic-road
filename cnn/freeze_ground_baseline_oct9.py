"""Preserve E7 and current SPD8 evidence; never start training or replace a release."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil

import torch

from .archive_oct5 import ROOT, WEIGHT_SHA, copy_frozen, sha
from .model import RoadYOLOS4
from .teacher import tree_hash


DEST = ROOT / "cnn/releases/RoadYOLO-S4-512_20261009_before_ground_adapt"
ANCESTOR = ROOT / "cnn/releases/RoadYOLO-S4-512_20261005_before_supervised5"
EVIDENCE = ROOT / "cnn/reports/spd_val8_e7_20261009_v3"
PLAN = ROOT.parent.parent / "CNN冻结后恢复训练_建议与执行步骤_20261009.txt"
CHECKPOINT = Path("cnn/runs/person_native_recovery_20261004/epoch_0006.pt")


def verify(destination):
    """A missing completion receipt or any changed payload fails verification."""
    receipt = json.loads((destination / "release.json").read_text(encoding="utf-8"))
    if not receipt["files"]:
        raise ValueError("empty release")
    for name, expected in receipt["files"].items():
        path = destination / name
        if (Path(name).is_absolute() or ".." in Path(name).parts
                or not path.resolve().is_relative_to(destination.resolve())
                or not path.is_file() or sha(path) != expected):
            raise ValueError(f"release payload mismatch: {name}")
    if sha(destination / receipt["checkpoint"]) != WEIGHT_SHA:
        raise ValueError("not the approved E7 checkpoint")
    return dict(status="verified", path=str(destination), files=len(receipt["files"]),
                checkpoint_sha256=WEIGHT_SHA, training_started=False,
                formal_acceptance=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true", help="read-only hash replay")
    args = parser.parse_args()
    if args.verify:
        print(json.dumps(verify(DEST), ensure_ascii=False))
        return
    if DEST.exists():
        raise FileExistsError(DEST)
    if sha(ANCESTOR / CHECKPOINT) != WEIGHT_SHA:
        raise ValueError("E7 source checkpoint changed")
    torch.set_num_threads(2)
    checkpoint = torch.load(ANCESTOR / CHECKPOINT, map_location="cpu", weights_only=False)
    model = RoadYOLOS4()
    model.load_state_dict(checkpoint["model"], strict=True)
    if (checkpoint["epoch"] != 6 or checkpoint["trained_steps"] != 2086
            or checkpoint["architecture_hash"] != model.architecture_hash()):
        raise ValueError("E7 metadata or architecture changed")
    publication = json.loads((EVIDENCE / "publication_receipt.json").read_text(encoding="utf-8"))
    dataset_sha = sha(EVIDENCE / "spd_val8.json")
    if (publication["dataset_sha256"] != dataset_sha
            or publication["checkpoint_sha256"] != WEIGHT_SHA
            or publication["image_count"] != 8
            or publication["labels"] != {"person": 25, "vehicle": 120}):
        raise ValueError("SPD8 publication binding changed")
    for name in ("e7_evaluation.json", "teacher_evaluation.json"):
        report = json.loads((EVIDENCE / name).read_text(encoding="utf-8"))
        if report["dataset_sha256"] != dataset_sha or report["image_count"] != 8:
            raise ValueError(f"evaluation binding changed: {name}")
    teacher_root = ROOT / "cnn/teacher_assets"
    teacher_receipt = json.loads((teacher_root / "receipt.json").read_text(encoding="utf-8"))
    if (sha(teacher_root / "yolox_s.pth") != teacher_receipt["weights"]["sha256"]
            or tree_hash(teacher_root / "source/YOLOX-0.3.0/yolox")
            != teacher_receipt["source_tree_sha256"]):
        raise ValueError("external teacher assets changed")

    # Current sources are separate from the original training-time sources.
    sources = [p for p in (ROOT / "cnn").iterdir() if p.is_file()]
    for folder in (ROOT / "cnn/spec", EVIDENCE,
                   ROOT / "cnn/hw_validation/plans/competition_framework_20261008"):
        sources.extend(p for p in folder.rglob("*") if p.is_file())
    sources.extend(ROOT / name for name in (
        "cnn/reports/supervised5_oct5/status.json",
        "cnn/reports/post_review_s_20261007_v1/stage0_receipt.json",
        "cnn/reports/post_review_s_20261007_v1/merge_receipt.json",
        "cnn/reports/post_review_s_20261007_v1/cache_CPU_receipt.json",
        "cnn/runs/coco_full_pretrain300/train_log.jsonl",
        "cnn/runs/road40_from_coco6_segmented_20261003/train_log.jsonl",
        "cnn/runs/person_ab_20261004_native/train_log.jsonl",
        "cnn/teacher_assets/receipt.json"))
    inventory = {"current/" + p.relative_to(ROOT).as_posix(): p
                 for p in sorted(set(sources))}
    inventory["下一步建议与执行步骤.txt"] = PLAN
    expected = {}
    for name, source in inventory.items():
        if not source.is_file() or not source.resolve().is_relative_to(ROOT.parent.parent):
            raise ValueError(f"missing or escaped input: {source}")
        expected[name] = sha(source)
    external = {}
    for name in ("cnn/data/post_review_s_20261007_v1/dataset_train_val.json",
                 "cnn/data/cache_road_post_review_s_20261007_v1/index.json"):
        path = ROOT / name
        external[name] = dict(path=str(path), sha256=sha(path), bytes=path.stat().st_size)
    external["teacher"] = dict(path=str(teacher_root),
                               weight_sha256=teacher_receipt["weights"]["sha256"],
                               source_tree_sha256=teacher_receipt["source_tree_sha256"])

    DEST.mkdir(parents=True, exist_ok=False)
    copy_frozen(ANCESTOR, DEST / "ancestral_e7")
    for name, source in inventory.items():
        target = DEST / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        if sha(source) != expected[name] or sha(target) != expected[name]:
            raise ValueError(f"input changed or copy failed: {name}")
    files = {p.relative_to(DEST).as_posix(): sha(p)
             for p in sorted(DEST.rglob("*")) if p.is_file()}
    receipt = dict(
        status="frozen_verified_E7_and_SPD8_development_baseline",
        created_at=datetime.now(timezone.utc).isoformat(),
        checkpoint=(Path("ancestral_e7") / CHECKPOINT).as_posix(),
        checkpoint_sha256=WEIGHT_SHA, architecture_hash=model.architecture_hash(),
        native_stage_completed_epochs=7, native_stage_optimizer_steps=2086,
        trainable_parameters=sum(p.numel() for p in model.parameters() if p.requires_grad),
        training_ancestry="COCO complete6 -> VisDrone Mosaic20 -> native7; 19140 inherited complete updates",
        dataset_sha256=dataset_sha, image_count=8, person_gt=25, vehicle_gt=120,
        scene_scope="SPD:yizhuang09:1:0058; one correlated development scene, not Ground48 or newtest",
        excluded_training_camera="SPD:yizhuang09:1 (all sequences)",
        files=files, external_dependencies=external,
        training_started=False, GPU_compute_started=False, formal_acceptance=False,
        int8_export=False, RTL_modified=False,
        boundary="Independent ordinary-file copies, not OS write-locked or off-disk backup. "
                 "Raw training/cache binaries and teacher assets stay external and hash-bound. "
                 "Original absolute paths inside copied evidence are preserved as provenance; "
                 "this is not an automatic portable restore or an FPGA deployment package.")
    with (DEST / "release.json").open("x", encoding="utf-8") as stream:
        json.dump(receipt, stream, ensure_ascii=False, indent=2)
    print(json.dumps(verify(DEST), ensure_ascii=False))


if __name__ == "__main__":
    main()
