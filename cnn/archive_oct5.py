"""Preserve the completed native epoch-7 release without replacing old evidence."""
import hashlib
import json
import argparse
from pathlib import Path
import shutil
import sys

import torch

from .model import RoadYOLOS4
from .resume_state import validate_resume_state


ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "cnn/releases/RoadYOLO-S4-512_20261005_fp32_e7"
WEIGHT_SHA = "17c3cd644bd80a5f66e24eb3f510126fbb5db5bbb302e39250d78d339b6e5d42"
REFREEZE = ROOT / "cnn/releases/RoadYOLO-S4-512_20261005_before_supervised5"


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def copy_frozen(source, destination):
    """Copy verified frozen inputs, never rebuild from changed live sources."""
    source, destination = Path(source).resolve(), Path(destination).resolve()
    if destination.is_relative_to(source) or source.is_relative_to(destination):
        raise ValueError("freeze source and destination must be disjoint")
    manifest = source / "release.json"
    manifest_sha = sha(manifest)
    release = json.loads(manifest.read_text(encoding="utf-8"))
    files = release["files"]
    if not files:
        raise ValueError("empty frozen input inventory")
    for name, expected in files.items():
        if Path(name).is_absolute() or ".." in Path(name).parts or name == "release.json":
            raise ValueError(f"unsafe frozen inventory path: {name}")
        path = source / name
        if not path.resolve().is_relative_to(source) or not path.is_file() or sha(path) != expected:
            raise ValueError(f"frozen input is missing, escaped, or changed: {name}")
    if sha(manifest) != manifest_sha:
        raise ValueError("release inventory changed during verification")
    destination.mkdir(parents=True, exist_ok=False)
    for name, expected in {**files, "release.json": manifest_sha}.items():
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source / name, target)
        if sha(target) != expected:
            raise ValueError(f"refreeze copy mismatch: {name}")
    receipt = dict(status="copied_original_frozen_release_and_verified",
                   source=str(source), destination=str(destination),
                   source_release_sha256=manifest_sha, files_verified=len(files),
                   checkpoint_sha256=release.get("checkpoint_sha256"),
                   purpose="pre-supervised-five-epoch immutable baseline",
                   scope="original CNN release only; production RTL and external raw/cache binaries are not copied",
                   formal_acceptance=False, training_started=False)
    with (destination / "refreeze_receipt.json").open("x", encoding="utf-8") as stream:
        json.dump(receipt, stream, ensure_ascii=False, indent=2)
    return receipt


def main():
    status_path = ROOT / "cnn/reports/person_native_recovery_20261004/status.json"
    status = json.loads(status_path.read_text(encoding="utf-8"))
    if status["status"] != "completed_epoch7_evaluated":
        raise ValueError("release requires the completed, evaluated epoch-7 run")
    checkpoint_path = ROOT / "cnn/runs/person_native_recovery_20261004/epoch_0006.pt"
    if sha(checkpoint_path) != WEIGHT_SHA:
        raise ValueError("frozen epoch-7 checkpoint changed")
    checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=False)
    model = RoadYOLOS4()
    model.load_state_dict(checkpoint["model"], strict=True)
    assert checkpoint["epoch"] == 6 and checkpoint["trained_steps"] == 2086
    assert checkpoint["architecture_hash"] == model.architecture_hash()
    live = torch.load(checkpoint_path.parent / "last_resume.pt",
                      map_location="cpu", weights_only=False)
    validate_resume_state(live, checkpoint["training_protocol"])
    for name, expected in status["source_sha256"].items():
        if sha(ROOT / "cnn" / name) != expected:
            raise ValueError(f"training source changed before preservation: {name}")
    dataset = ROOT / "cnn/data/visdrone_vid_train/raw_manifest/dataset.json"
    assert sha(dataset) == checkpoint["dataset_sha256"]
    files = [ROOT / "cnn" / name for name in status["source_sha256"]]
    for folder in (checkpoint_path.parent, status_path.parent, ROOT / "cnn/spec"):
        files.extend(path for path in folder.rglob("*") if path.is_file())
    files.extend((dataset, ROOT / "cnn/data/cache_road_recovery_20261003/index.json",
                  ROOT / "cnn/reports/cache_road_recovery_migration_20261003.json",
                  Path(status["source_checkpoint"]), Path(status["baseline_report"])))
    files = sorted(set(files))
    if any(not path.is_file() for path in files):
        raise FileNotFoundError("release input is missing")
    DEST.mkdir(parents=True, exist_ok=False)
    hashes = {}
    for source in files:
        relative = source.relative_to(ROOT)
        target = DEST / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        expected = sha(source)
        if sha(target) != expected:
            raise ValueError(f"archive copy mismatch: {relative}")
        hashes[relative.as_posix()] = expected
    release = dict(status="saved_and_verified_fp32_development_release",
                   release_date="2026-10-05", training_completed_at=status["updated_at"],
                   checkpoint_sha256=WEIGHT_SHA, architecture_hash=model.architecture_hash(),
                   epoch=7, optimizer_steps=2086, files=hashes,
                   runtime=dict(python=sys.version, torch=torch.__version__),
                   formal_acceptance=False, int8_export=False,
                   external_inputs="Raw images and 10.7 GB rgb.bin remain external; copied manifests/index bind their identities.",
                   backup_boundary="Separate local directory, not an off-disk disaster backup.")
    with (DEST / "release.json").open("x", encoding="utf-8") as stream:
        json.dump(release, stream, ensure_ascii=False, indent=2)
    assert all(sha(DEST / name) == value for name, value in hashes.items())
    print(json.dumps(dict(status=release["status"], path=str(DEST), files=len(hashes),
                          checkpoint_sha256=WEIGHT_SHA)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--copy-frozen", action="store_true")
    args = parser.parse_args()
    if args.copy_frozen:
        print(json.dumps(copy_frozen(DEST, REFREEZE)))
    else:
        main()
