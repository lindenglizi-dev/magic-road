"""Train RoadYOLO-S4-512 on complete full-frame detection manifests only."""

from __future__ import annotations

import argparse
from collections import OrderedDict
from dataclasses import dataclass
import hashlib
import json
import math
import os
from pathlib import Path
import random
import re
import sys
import time
from typing import Any, Sequence

import numpy as np
from PIL import Image
import torch
from torch import Tensor
from torch.utils.data import DataLoader, Dataset
import cv2

try:
    from .dataset import _letterbox_720, audit
    from .integer import resize_area
    from .loss import DISTILL_CONTRACT, YOLOXLoss, dense_distillation_loss
    from .model import INPUT_HEIGHT, INPUT_WIDTH, RoadYOLOS4
    from .resume_state import (FORMAT as RESUME_FORMAT, load_latest_resume,
                               save_resume_state, validate_resume_state)
except ImportError:  # python cnn/train.py
    from dataset import _letterbox_720, audit
    from integer import resize_area
    from loss import DISTILL_CONTRACT, YOLOXLoss, dense_distillation_loss
    from model import INPUT_HEIGHT, INPUT_WIDTH, RoadYOLOS4
    from resume_state import (FORMAT as RESUME_FORMAT, load_latest_resume,
                              save_resume_state, validate_resume_state)


CLASS_CONTRACT = {"0": "person", "1": "vehicle"}
TEACHER_CACHE_CONTRACT = "road-yolo-student-dense-v1"
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
TRAINING_PROTOCOL = "formal_sgd_warmup_cosine_mosaic_v1"
FINETUNE_TRAINING_PROTOCOL = "finetune_sgd_constant_v1"
LR_SCHEDULES = ("warmup_cosine", "finetune_constant")
WARMUP_EPOCHS = 5
MOSAIC_CLOSE_EPOCHS = 15
COSINE_MIN_LR_RATIO = 0.05
AMP_INIT_SCALE = 128.0
PREPROCESS_CONTRACT = {
    "prepared": "RGB888_512x288_minus128",
    "raw": "RGB888_letterbox_1280x720_then_area_2_over_5_RNE_minus128",
    "boxes": "network_xyxy_512x288",
}


@dataclass(frozen=True)
class DatasetValidationSnapshot:
    manifest: Path
    manifest_sha256: str
    dataset_content_sha256: str
    rows: list[dict[str, Any]]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def set_seed(seed: int) -> None:
    os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    torch.use_deterministic_algorithms(True)
    torch.backends.cudnn.benchmark = False


def _boxes(value: Any, field: str) -> list[list[float]]:
    if not isinstance(value, list):
        raise ValueError(f"{field} must be a list")
    result = []
    for box in value:
        if not isinstance(box, list) or len(box) != 4:
            raise ValueError(f"{field} entries must be xyxy lists")
        converted = [float(number) for number in box]
        x1, y1, x2, y2 = converted
        if not (0 <= x1 < x2 <= INPUT_WIDTH and 0 <= y1 < y2 <= INPUT_HEIGHT):
            raise ValueError(f"{field} box outside 512x288 network coordinates: {box}")
        result.append(converted)
    return result


def reject_cache_qa(payload: dict[str, Any]) -> None:
    if (payload.get('cache_pilot_provenance') is not None
            or payload.get('manifest_status') == 'development_cache_pilot'
            or str(payload.get('purpose', '')).startswith('CPU_disk_cache_QA')):
        raise ValueError('cache QA manifest is forbidden for training or accuracy evaluation')


def load_dataset_manifest(path: Path, *, allow_cache_qa: bool = False
                          ) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    # Reuse schema/completeness validation, then hash each image exactly once
    # below instead of reading the whole image corpus twice at startup.
    payload = json.loads(path.read_text(encoding='utf-8'))
    if not allow_cache_qa:
        reject_cache_qa(payload)
    if audit(payload)['incomplete_frames']:
        raise ValueError('dataset contains incomplete frames; background supervision is forbidden')
    if payload.get("classes") != list(CLASS_CONTRACT.values()):
        raise ValueError(f"classes must equal {list(CLASS_CONTRACT.values())}")
    if payload.get("training_eligible") is not True:
        raise ValueError("dataset is not marked training_eligible")
    if payload.get("input_size", [INPUT_WIDTH, INPUT_HEIGHT]) != [INPUT_WIDTH, INPUT_HEIGHT]:
        raise ValueError("dataset input_size must be [512, 288]")
    if payload.get("task", "detection") != "detection":
        raise ValueError("task must be detection; ROI datasets are rejected")
    rows = payload.get("images")
    if not isinstance(rows, list) or not rows:
        raise ValueError("dataset images must be a non-empty list")

    required = {"image", "boxes", "labels", "ignore_boxes", "scene_id", "split",
                "source_sha256", "source_frame"}
    normalized = []
    scene_splits: dict[str, str] = {}
    for index, source in enumerate(rows):
        if not isinstance(source, dict) or not required.issubset(source):
            missing = sorted(required - set(source if isinstance(source, dict) else ()))
            raise ValueError(f"images[{index}] missing fields: {missing}")
        row = dict(source)
        row["boxes"] = _boxes(row["boxes"], f"images[{index}].boxes")
        row["ignore_boxes"] = _boxes(row["ignore_boxes"], f"images[{index}].ignore_boxes")
        labels = row["labels"]
        if (not isinstance(labels, list) or len(labels) != len(row["boxes"])
                or any(label not in (0, 1) for label in labels)):
            raise ValueError(f"images[{index}].labels must align with boxes and contain 0/1")
        if row["split"] not in {"train", "val", "newtest"}:
            raise ValueError(f"images[{index}].split must be train, val, or newtest")
        if not isinstance(row["scene_id"], str) or not row["scene_id"]:
            raise ValueError(f"images[{index}].scene_id must be non-empty")
        if not isinstance(row["source_sha256"], str) or not SHA256_RE.fullmatch(row["source_sha256"]):
            raise ValueError(f"images[{index}].source_sha256 must be a SHA-256")
        previous = scene_splits.setdefault(row["scene_id"], row["split"])
        if previous != row["split"]:
            raise ValueError(f"scene {row['scene_id']} leaks across {previous}/{row['split']}")
        image = Path(row["image"])
        row["image_path"] = image if image.is_absolute() else path.parent / image
        row["image_sha256"] = sha256(row["image_path"])
        preprocess = row.get('preprocess', {})
        if (isinstance(preprocess, dict) and preprocess.get('raw_image') is True
                and row['image_sha256'] != row['source_sha256']):
            raise ValueError(f"raw image differs from manifest source hash: {row['image_path']}")
        row["teacher_key"] = str(row.get("teacher_key", row["image"])).replace("\\", "/")
        normalized.append(row)

    splits = {row["split"] for row in normalized}
    if not {"train", "val"}.issubset(splits):
        raise ValueError("complete training manifest requires both train and val rows")
    return payload, normalized


def dataset_content_hash(rows: Sequence[dict[str, Any]]) -> str:
    """Hash stable image path/content pairs; annotations remain bound by JSON hash."""
    entries = sorted((str(row["image"]).replace("\\", "/"), row["image_sha256"])
                     for row in rows)
    encoded = json.dumps(entries, ensure_ascii=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def load_dataset_snapshot(path: Path, *, allow_cache_qa: bool = False
                          ) -> tuple[dict[str, Any], DatasetValidationSnapshot]:
    """Validate/hash source images once and retain their shared row identity."""
    payload, rows = load_dataset_manifest(path, allow_cache_qa=allow_cache_qa)
    return payload, DatasetValidationSnapshot(
        path.resolve(), sha256(path), dataset_content_hash(rows), rows)


class FullFrameDataset(Dataset):
    def __init__(self, rows: Sequence[dict[str, Any]], split: str, *,
                 mosaic: bool = False, seed: int = 42) -> None:
        self.rows = [row for row in rows if row["split"] == split]
        if not self.rows:
            raise ValueError(f"dataset has no {split} rows")
        self.mosaic = mosaic
        self.seed = seed
        self.epoch = 0

    def set_epoch(self, epoch: int, mosaic: bool | None = None) -> None:
        self.epoch = epoch
        if mosaic is not None:
            self.mosaic = mosaic

    def __len__(self) -> int:
        return len(self.rows)

    def _load(self, index: int) -> tuple[np.ndarray, dict[str, Tensor], str]:
        row = self.rows[index]
        preprocess = row.get("preprocess", {})
        raw_image = isinstance(preprocess, dict) and preprocess.get("raw_image") is True
        if raw_image:
            bgr = cv2.imread(str(row["image_path"]), cv2.IMREAD_COLOR)
            if bgr is None:
                raise ValueError(f"cannot decode raw image: {row['image_path']}")
            letterboxed, transform = _letterbox_720(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB))
            expected = preprocess.get("letterbox_1280x720")
            if expected is not None and transform != expected:
                raise ValueError(f"raw image transform mismatch: {row['image_path']}")
            pixels = resize_area(letterboxed)
        else:
            with Image.open(row["image_path"]) as image:
                image = image.convert("RGB")
                if image.size != (INPUT_WIDTH, INPUT_HEIGHT):
                    raise ValueError(
                        f"{row['image_path']} is {image.size}; raw sources require "
                        "preprocess.raw_image=true")
                pixels = np.asarray(image, dtype=np.uint8).copy()
        target = {
            "boxes": torch.tensor(row["boxes"], dtype=torch.float32).reshape(-1, 4),
            "labels": torch.tensor(row["labels"], dtype=torch.long),
            "ignore_boxes": torch.tensor(row["ignore_boxes"], dtype=torch.float32).reshape(-1, 4),
        }
        return pixels, target, row["teacher_key"]

    @staticmethod
    def _move_boxes(boxes: Tensor, left: int, top: int) -> Tensor:
        moved = boxes.clone() * 0.5
        if moved.numel():
            moved[:, (0, 2)] += left
            moved[:, (1, 3)] += top
        return moved

    def _mosaic(self, index: int) -> tuple[np.ndarray, dict[str, Tensor], str]:
        # No crop is used: every source pixel and every positive/ignore box is
        # retained, so the augmentation cannot invent negative image regions.
        generator = random.Random((self.seed << 40) ^ (self.epoch << 20) ^ index)
        indices = [index] + [generator.randrange(len(self.rows)) for _ in range(3)]
        canvas = np.empty((INPUT_HEIGHT, INPUT_WIDTH, 3), dtype=np.uint8)
        boxes, labels, ignores, keys = [], [], [], []
        for source_index, (left, top) in zip(
                indices, ((0, 0), (INPUT_WIDTH // 2, 0),
                          (0, INPUT_HEIGHT // 2),
                          (INPUT_WIDTH // 2, INPUT_HEIGHT // 2))):
            pixels, target, key = self._load(source_index)
            resized = Image.fromarray(pixels).resize(
                (INPUT_WIDTH // 2, INPUT_HEIGHT // 2), Image.Resampling.BILINEAR)
            canvas[top:top + INPUT_HEIGHT // 2, left:left + INPUT_WIDTH // 2] = resized
            boxes.append(self._move_boxes(target["boxes"], left, top))
            labels.append(target["labels"])
            ignores.append(self._move_boxes(target["ignore_boxes"], left, top))
            keys.append(key)
        target = {
            "boxes": torch.cat(boxes),
            "labels": torch.cat(labels),
            "ignore_boxes": torch.cat(ignores),
        }
        return canvas, target, "mosaic:" + "|".join(keys)

    def __getitem__(self, index: int) -> tuple[Tensor, dict[str, Tensor], str]:
        pixels, target, key = self._mosaic(index) if self.mosaic else self._load(index)
        # Deployment input is uint8 RGB with zero point 128, not 0..1 normalization.
        tensor = torch.from_numpy(pixels.astype(np.float32)).permute(2, 0, 1) - 128.0
        return tensor, target, key


def collate(batch: Sequence[tuple[Tensor, dict[str, Tensor], str]]
            ) -> tuple[Tensor, list[dict[str, Tensor]], list[str]]:
    images, targets, keys = zip(*batch)
    return torch.stack(images), list(targets), list(keys)


def make_frame_dataset(rows, split, manifest, *, cache_root=None,
                       cache_index_sha256=None, cache_binding=None,
                       seed=42, mosaic=False):
    """Cache is opt-in and must pin the exact reviewed index bytes."""
    if (cache_root is None) != (cache_index_sha256 is None):
        raise ValueError('cache root and index SHA-256 must be supplied together')
    if cache_root is None:
        return FullFrameDataset(rows, split, seed=seed, mosaic=mosaic)
    if not SHA256_RE.fullmatch(cache_index_sha256):
        raise ValueError('invalid cache index SHA-256')
    if __package__:
        from .disk_cache import DiskCachedDataset
    else:
        from disk_cache import DiskCachedDataset
    return DiskCachedDataset(rows, split, manifest, cache_root, seed=seed,
                             mosaic=mosaic, expected_index_sha256=cache_index_sha256.lower(),
                             binding=cache_binding)


def accumulation_group_samples(microstep: int, microsteps: int, accum_steps: int,
                               batch_size: int, dataset_size: int) -> int:
    """Actual samples in this optimizer step, including a partial last batch."""
    group_start = (microstep // accum_steps) * accum_steps
    group_end = min(group_start + accum_steps, microsteps)
    return min(dataset_size, group_end * batch_size) - group_start * batch_size


def scheduled_lr(step: int, total_steps: int, warmup_steps: int, base_lr: float,
                 lr_schedule: str = "warmup_cosine") -> float:
    """Return the selected learning rate once per optimizer step."""
    if not 0 <= step < total_steps:
        raise ValueError("optimizer step is outside the planned schedule")
    if lr_schedule == "finetune_constant":
        return base_lr
    if lr_schedule != "warmup_cosine":
        raise ValueError(f"unknown learning-rate schedule: {lr_schedule}")
    if step < warmup_steps:
        return base_lr * (step + 1) / max(warmup_steps, 1)
    decay_steps = total_steps - warmup_steps
    progress = 1.0 if decay_steps <= 1 else (step - warmup_steps) / (decay_steps - 1)
    cosine = 0.5 * (1.0 + math.cos(math.pi * progress))
    return base_lr * (COSINE_MIN_LR_RATIO + (1.0 - COSINE_MIN_LR_RATIO) * cosine)


def protocol_for(args: argparse.Namespace, optimizer_steps_per_epoch: int,
                 teacher_sha256: str | None) -> dict[str, Any]:
    lr_schedule = getattr(args, "lr_schedule", "warmup_cosine")
    protocol = {
        "name": TRAINING_PROTOCOL,
        "phase": args.phase,
        "checkpoint_kind": args.checkpoint_kind,
        "epochs": args.epochs,
        "optimizer": "SGD",
        "base_lr": args.lr,
        "momentum": args.momentum,
        "weight_decay": args.weight_decay,
        "clip_grad": args.clip_grad,
        "microbatch": args.batch_size,
        "accum_steps": args.accum_steps,
        "optimizer_steps_per_epoch": optimizer_steps_per_epoch,
        "warmup_epochs": WARMUP_EPOCHS,
        "cosine_min_lr_ratio": COSINE_MIN_LR_RATIO,
        "mosaic": bool(args.mosaic),
        "mosaic_close_epochs": MOSAIC_CLOSE_EPOCHS,
        "seed": args.seed,
        "deterministic_algorithms": "strict",
        "amp": bool(args.amp),
        "amp_init_scale": AMP_INIT_SCALE,
        "distill_weight": args.distill_weight,
        "teacher_cache_sha256": teacher_sha256,
        "preprocess_contract": PREPROCESS_CONTRACT,
    }
    if args.phase == "distill":
        protocol["distillation_contract"] = DISTILL_CONTRACT
    if lr_schedule == "finetune_constant":
        protocol.update({
            "name": FINETUNE_TRAINING_PROTOCOL,
            "lr_schedule": lr_schedule,
            "warmup_epochs": 0,
            "cosine_min_lr_ratio": 1.0,
        })
    elif lr_schedule != "warmup_cosine":
        raise ValueError(f"unknown learning-rate schedule: {lr_schedule}")
    if getattr(args, "freeze_bn", False):
        # Omit the default to preserve existing resume protocol hashes.
        protocol["batch_norm_policy"] = "frozen_running_stats_and_affine_v1"
    return protocol


def protocol_hash(protocol: dict[str, Any]) -> str:
    encoded = json.dumps(protocol, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def ensure_resume_eligible(checkpoint: dict[str, Any],
                           expected_protocol: dict[str, Any] | None = None) -> None:
    if checkpoint.get("interrupted"):
        raise ValueError(
            "mid-epoch interrupted checkpoints cannot be resumed exactly; "
            "use --init-checkpoint for an explicit weights-only restart")
    if checkpoint.get("format") == RESUME_FORMAT:
        validate_resume_state(checkpoint, expected_protocol)
        return
    if checkpoint.get("format") != "road-yolo-checkpoint-v2":
        raise ValueError("legacy checkpoints are weights-only; use --init-checkpoint")
    if checkpoint.get("checkpoint_kind") != "training":
        raise ValueError("diagnostic checkpoints are weights-only; use --init-checkpoint")
    if expected_protocol is not None and checkpoint.get("training_protocol") != expected_protocol:
        raise ValueError("resume training protocol mismatch; use --init-checkpoint to restart")


class TeacherCache:
    """Already-adapted S4/S8/S16 dense targets; never merged into GT boxes."""

    def __init__(self, path: Path, architecture_hash: str, dataset_sha256: str,
                 dataset_content_sha256: str) -> None:
        self.path = path.resolve()
        self.loaded = OrderedDict()
        self.key_shards = {}
        self.shards = []
        payload = (json.loads(path.read_text(encoding="utf-8")) if path.suffix == ".json"
                   else torch.load(path, map_location="cpu", weights_only=True))
        if payload.get("contract") != TEACHER_CACHE_CONTRACT:
            raise ValueError(f"teacher cache contract must be {TEACHER_CACHE_CONTRACT}")
        if payload.get("student_architecture_hash") != architecture_hash:
            raise ValueError("teacher cache targets a different student architecture")
        if payload.get("strides") != [4, 8, 16]:
            raise ValueError("teacher cache must include adapted stride-4/8/16 dense heads")
        if payload.get("class_contract") != CLASS_CONTRACT:
            raise ValueError("teacher cache class contract mismatch")
        if payload.get("dataset_sha256") != dataset_sha256:
            raise ValueError("teacher cache dataset manifest mismatch")
        if payload.get("dataset_content_sha256") != dataset_content_sha256:
            raise ValueError("teacher cache image content mismatch")
        if payload.get("preprocess_contract") != PREPROCESS_CONTRACT:
            raise ValueError("teacher cache preprocessing contract mismatch")
        self.binding = {key: payload[key] for key in (
            "contract", "student_architecture_hash", "strides", "class_contract",
            "dataset_sha256", "dataset_content_sha256", "preprocess_contract")}
        if payload.get("format") == "road-yolo-teacher-index-v1":
            self.items = None
            for name in ("teacher_source_sha256", "teacher_weight_sha256", "teacher_preprocess_sha256"):
                if not SHA256_RE.fullmatch(payload.get(name, "")):
                    raise ValueError("teacher index source/weight/preprocessing binding missing")
                self.binding[name] = payload[name]
            if payload.get("inference_dtype") != "float32" or payload.get("storage_dtype") != "float16":
                raise ValueError("teacher index dtype contract mismatch")
            self.binding.update(inference_dtype="float32", storage_dtype="float16")
            if payload.get("split") != "train" or not isinstance(payload.get("shards"), list):
                raise ValueError("teacher index requires train shards")
            for number, shard in enumerate(payload["shards"]):
                shard_path = (self.path.parent / shard["file"]).resolve()
                if self.path.parent not in shard_path.parents:
                    raise ValueError("teacher shard escapes index directory")
                if not SHA256_RE.fullmatch(shard["sha256"]) or sha256(shard_path) != shard["sha256"]:
                    raise ValueError("teacher shard hash mismatch")
                if not isinstance(shard.get("keys"), list) or not shard["keys"]:
                    raise ValueError("teacher shard keys missing")
                for key in shard["keys"]:
                    if not isinstance(key, str) or key in self.key_shards:
                        raise ValueError("duplicate or invalid teacher shard key")
                    self.key_shards[key] = number
                self.shards.append({**shard, "path": shard_path})
            if len(self.key_shards) != payload.get("item_count"):
                raise ValueError("teacher index item count mismatch")
        else:
            self.items = payload.get("items")
            if not isinstance(self.items, dict):
                raise ValueError("teacher cache items must be a dictionary")

    def require_keys(self, keys: Sequence[str]) -> None:
        actual = set(self.items) if self.items is not None else set(self.key_shards)
        if len(set(keys)) != len(keys) or actual != set(keys):
            raise ValueError("teacher cache must cover each training key exactly once")

    def item(self, key: str):
        if self.items is not None:
            return self.items[key]
        number = self.key_shards[key]
        if number not in self.loaded:
            shard = self.shards[number]
            if sha256(shard["path"]) != shard["sha256"]:
                raise ValueError("teacher shard changed after preflight")
            payload = torch.load(shard["path"], map_location="cpu", weights_only=True, mmap=True)
            if any(payload.get(name) != value for name, value in self.binding.items()):
                raise ValueError("teacher shard binding mismatch")
            items = payload.get("items")
            if not isinstance(items, dict) or set(items) != set(shard["keys"]):
                raise ValueError("teacher shard key coverage mismatch")
            if len(self.loaded) == 2:
                self.loaded.popitem(last=False)
            self.loaded[number] = items
        self.loaded.move_to_end(number)
        return self.loaded[number][key]

    def batch(self, keys: Sequence[str], device: torch.device) -> list[Tensor]:
        samples = []
        for key in keys:
            try:
                item = self.item(key)
            except KeyError as error:
                raise KeyError(f"teacher cache missing {key}") from error
            heads = item.get("heads", item)
            if not isinstance(heads, (list, tuple)) or len(heads) != 3:
                raise ValueError(f"teacher item {key} must contain three adapted heads")
            samples.append([torch.as_tensor(head, dtype=torch.float32) for head in heads])
        result = []
        expected = ((7, 72, 128), (7, 36, 64), (7, 18, 32))
        for scale, shape in enumerate(expected):
            head = torch.stack([sample[scale] for sample in samples])
            if tuple(head.shape[1:]) != shape:
                raise ValueError(f"adapted teacher scale {scale} has {head.shape[1:]}, expected {shape}")
            if not torch.isfinite(head).all():
                raise ValueError("non-finite teacher head")
            result.append(head.to(device, non_blocking=True))
        return result


def rng_state() -> dict[str, Any]:
    return {
        "python": random.getstate(),
        "numpy": np.random.get_state(),
        "torch": torch.get_rng_state(),
        "cuda": torch.cuda.get_rng_state_all() if torch.cuda.is_available() else [],
    }


def restore_rng(state: dict[str, Any]) -> None:
    random.setstate(state["python"])
    np.random.set_state(state["numpy"])
    torch.set_rng_state(state["torch"])
    if torch.cuda.is_available() and state.get("cuda"):
        torch.cuda.set_rng_state_all(state["cuda"])


def save_checkpoint(path: Path, *, model: RoadYOLOS4, optimizer: torch.optim.Optimizer,
                    scaler: torch.amp.GradScaler, epoch: int, trained_steps: int,
                    phase: str, checkpoint_kind: str, dataset_hash: str,
                    dataset_content_sha256: str,
                    effective_batch: int, last_optimizer_effective_batch: int,
                    metric: dict[str, Any], training_protocol: dict[str, Any],
                    interrupted: bool = False) -> None:
    state = {
        "format": "road-yolo-checkpoint-v2",
        "phase": phase,
        "checkpoint_kind": checkpoint_kind,
        "epoch": epoch,
        "trained_steps": trained_steps,
        "architecture_hash": model.architecture_hash(),
        "dataset_sha256": dataset_hash,
        "dataset_content_sha256": dataset_content_sha256,
        "class_contract": CLASS_CONTRACT,
        "effective_batch": effective_batch,
        "effective_batch_semantics": "target; epoch tail may be smaller",
        "last_optimizer_effective_batch": last_optimizer_effective_batch,
        "acceptance_eligible": False,
        "metric_status": "unaccepted_loss_only_no_detection_metrics",
        "training_protocol": training_protocol,
        "training_protocol_sha256": protocol_hash(training_protocol),
        "metric": metric,
        "interrupted": interrupted,
        "resume_eligible": not interrupted and checkpoint_kind == "training",
        "model": model.state_dict(),  # includes BN running statistics
        "optimizer": optimizer.state_dict(),
        "scaler": scaler.state_dict(),
        "rng_state": rng_state(),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("wb") as handle:
        torch.save(state, handle)
        handle.flush()
        os.fsync(handle.fileno())
    temporary.replace(path)


def epoch_order(dataset_size: int, seed: int, epoch: int) -> list[int]:
    """Match this host's legacy DataLoader shuffle without loading any samples."""
    generator = torch.Generator().manual_seed(seed + epoch)
    torch.empty((), dtype=torch.int64).random_(generator=generator)
    return torch.randperm(dataset_size, generator=generator).tolist()


def _resume_payload(*, model, optimizer, scaler, args, training_protocol,
                    dataset_hash, dataset_content_sha256, effective_batch,
                    last_optimizer_effective_batch, stage, epoch_index, order,
                    trained_steps, next_microbatch, next_sample_cursor,
                    epoch_loss_sum, epoch_samples, val_next_batch=0,
                    val_loss_sum=0.0, val_samples=0, last_lr=0.0) -> dict[str, Any]:
    return {
        "format": RESUME_FORMAT, "checkpoint_kind": args.checkpoint_kind,
        "interrupted": False, "stage": stage, "phase": args.phase,
        "epoch_index": epoch_index, "epoch_order": order,
        "trained_steps": trained_steps, "next_microbatch": next_microbatch,
        "next_sample_cursor": next_sample_cursor,
        "epoch_loss_sum": epoch_loss_sum, "epoch_samples": epoch_samples,
        "val_next_batch": val_next_batch, "val_loss_sum": val_loss_sum,
        "val_samples": val_samples, "last_lr": last_lr,
        "architecture_hash": model.architecture_hash(),
        "dataset_sha256": dataset_hash,
        "dataset_content_sha256": dataset_content_sha256,
        "class_contract": CLASS_CONTRACT, "effective_batch": effective_batch,
        "last_optimizer_effective_batch": last_optimizer_effective_batch,
        "training_protocol": training_protocol,
        "training_protocol_sha256": protocol_hash(training_protocol),
        "model": model.state_dict(), "optimizer": optimizer.state_dict(),
        "scaler": scaler.state_dict(), "rng_state": rng_state(),
    }


def append_log(path: Path, event: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, sort_keys=True) + "\n")


def _state_equal(left: Any, right: Any) -> bool:
    if torch.is_tensor(left):
        return torch.is_tensor(right) and torch.equal(left.cpu(), right.cpu())
    if isinstance(left, np.ndarray):
        return isinstance(right, np.ndarray) and np.array_equal(left, right)
    if isinstance(left, dict):
        return (isinstance(right, dict) and left.keys() == right.keys()
                and all(_state_equal(left[key], right[key]) for key in left))
    if isinstance(left, (list, tuple)):
        return (isinstance(right, type(left)) and len(left) == len(right)
                and all(_state_equal(a, b) for a, b in zip(left, right, strict=True)))
    return left == right


def _matches_completed_checkpoint(path: Path, live: dict[str, Any], metric: dict[str, Any] | None
                                  ) -> bool:
    try:
        saved = torch.load(path, map_location="cpu", weights_only=False)
    except Exception:
        return False
    fields = ("architecture_hash", "dataset_sha256", "dataset_content_sha256",
              "class_contract", "phase", "effective_batch", "trained_steps",
              "training_protocol", "model", "optimizer", "scaler")
    return (saved.get("format") == "road-yolo-checkpoint-v2"
            and saved.get("epoch") == live.get("epoch_index")
            and saved.get("interrupted") is False
            and (metric is None or saved.get("metric") == metric)
            and all(_state_equal(saved.get(field), live.get(field)) for field in fields))


def _validate_v3_cursors(checkpoint: dict[str, Any], *, train_size: int, val_size: int,
                         batch_size: int, accum_steps: int, optimizer_steps_per_epoch: int,
                         seed: int) -> None:
    if checkpoint.get("format") != RESUME_FORMAT:
        return
    epoch = int(checkpoint["epoch_index"])
    planned_epochs = int(checkpoint["training_protocol"]["epochs"])
    if not 0 <= epoch < planned_epochs:
        raise ValueError("resume epoch is outside the training protocol")
    order = checkpoint["epoch_order"]
    if order != epoch_order(train_size, seed, epoch):
        raise ValueError("resume epoch order mismatch")
    cursor = int(checkpoint["next_sample_cursor"])
    microbatch = int(checkpoint["next_microbatch"])
    stage = checkpoint["stage"]
    train_microbatches = math.ceil(train_size / batch_size)
    if (microbatch > train_microbatches
            or cursor != min(microbatch * batch_size, train_size)
            or cursor != int(checkpoint["epoch_samples"])):
        raise ValueError("resume training cursors disagree")
    if stage == "train" and microbatch % accum_steps and microbatch != train_microbatches:
        raise ValueError("resume training cursor is inside an accumulation group")
    completed = (optimizer_steps_per_epoch if stage in {"val", "epoch_done"}
                 else math.ceil(microbatch / accum_steps))
    if int(checkpoint["trained_steps"]) != epoch * optimizer_steps_per_epoch + completed:
        raise ValueError("resume optimizer-step cursor disagrees")
    if stage in {"val", "epoch_done"} and (cursor != train_size
                                            or microbatch != train_microbatches):
        raise ValueError("post-training resume does not end at the training boundary")
    val_samples = int(checkpoint["val_samples"])
    val_batches = int(checkpoint["val_next_batch"])
    if (val_batches > math.ceil(val_size / batch_size)
            or val_samples != min(val_batches * batch_size, val_size)):
        raise ValueError("resume validation cursors disagree")
    if stage == "epoch_done" and val_samples != val_size:
        raise ValueError("completed epoch does not end at the validation boundary")


def validate_output_directory(output: Path, resume: Path | None) -> None:
    if not output.exists() or not any(output.iterdir()):
        return
    if resume is None:
        raise FileExistsError(f"output is not empty: {output}")
    allowed = {"last.pt", "interrupted.pt", "train_log.jsonl",
               "last_resume.pt", "last_resume.prev.pt", "last_resume.pt.tmp"}
    unknown = [entry.name for entry in output.iterdir()
               if entry.name not in allowed and not re.fullmatch(r"epoch_\d{4}\.pt", entry.name)]
    if unknown:
        raise FileExistsError(f"output contains files from an unknown run: {unknown}")
    if resume.name in {"last_resume.pt", "last_resume.prev.pt"}:
        if resume.parent.resolve() != output.resolve():
            raise ValueError("resume slot must belong to the output directory")
        return
    last = output / "last.pt"
    if not last.is_file():
        raise FileExistsError("non-empty v2 resume output has no last.pt identity")
    if last.resolve() != resume.resolve() and sha256(last) != sha256(resume):
        raise ValueError("resume checkpoint does not match output/last.pt")


def set_training_mode(model: RoadYOLOS4, freeze_bn: bool = False) -> None:
    """Reapply the opt-in BN policy after every train/eval transition."""
    model.train()
    if freeze_bn:
        for module in model.modules():
            if isinstance(module, torch.nn.BatchNorm2d):
                module.eval()
                module.requires_grad_(False)


def evaluate_loss(model: RoadYOLOS4, loader: DataLoader, criterion: YOLOXLoss,
                  device: torch.device, amp: bool, *, freeze_bn: bool = False) -> float:
    model.eval()
    total, samples = 0.0, 0
    with torch.no_grad():
        for images, targets, _keys in loader:
            images = images.to(device, non_blocking=True)
            with torch.amp.autocast(device_type=device.type, enabled=amp):
                result = criterion(model(images), targets)
            loss = float(result["loss"].item())
            if not math.isfinite(loss):
                raise FloatingPointError("non-finite validation loss")
            total += loss * images.shape[0]
            samples += images.shape[0]
    set_training_mode(model, freeze_bn)
    return total / max(samples, 1)


def train(args: argparse.Namespace) -> int:
    lr_schedule = getattr(args, "lr_schedule", "warmup_cosine")
    freeze_bn = getattr(args, "freeze_bn", False)
    stop_after_epoch = getattr(args, "stop_after_epoch", 0)
    if not 0 <= stop_after_epoch <= args.epochs:
        raise ValueError("--stop-after-epoch must be 0 or a planned one-based epoch")
    if args.phase == "qat":
        raise ValueError(
            "QAT blocked: the frozen contract lacks complete bias/output/skip-tensor scales. "
            "SiLU or Conv fake-quant hooks alone are not hardware-equivalent QAT.")
    if args.init_checkpoint is not None and args.resume is not None:
        raise ValueError("use only one of --init-checkpoint or --resume")

    # All corpus/cache verification is deliberately before set_seed or any CUDA query.
    dataset_path = args.dataset.resolve()
    manifest, snapshot = load_dataset_snapshot(dataset_path)
    rows = snapshot.rows
    dataset_hash = snapshot.manifest_sha256
    dataset_content_sha256 = snapshot.dataset_content_sha256
    cache_root = getattr(args, "input_cache", None)
    cache_receipt = getattr(args, "input_cache_index_sha256", None)
    if (cache_root is None) != (cache_receipt is None):
        raise ValueError("cache root and index SHA-256 must be supplied together")
    cache_binding = None
    if cache_root is not None:
        if __package__:
            from .disk_cache import open_validated_cache
        else:
            from disk_cache import open_validated_cache
        cache_binding = open_validated_cache(snapshot, cache_root, cache_receipt)
    cache_options = dict(cache_root=cache_root, cache_index_sha256=cache_receipt,
                         cache_binding=cache_binding)
    train_data = make_frame_dataset(rows, "train", dataset_path, seed=args.seed, **cache_options)
    val_data = make_frame_dataset(rows, "val", dataset_path, **cache_options)
    del manifest

    probe = RoadYOLOS4()
    architecture_hash = probe.architecture_hash()
    del probe
    teacher = None
    teacher_sha256 = None
    if args.phase == "distill":
        if args.teacher_cache is None:
            raise ValueError("distill phase requires --teacher-cache; it will not run without a teacher")
        if args.mosaic:
            raise ValueError("distill teacher keys are per image; pass --no-mosaic")
        teacher = TeacherCache(args.teacher_cache, architecture_hash, dataset_hash,
                               dataset_content_sha256)
        teacher.require_keys([row["teacher_key"] for row in train_data.rows])
        teacher_sha256 = sha256(args.teacher_cache)
    elif args.teacher_cache is not None:
        raise ValueError("--teacher-cache is only valid in distill phase")

    device = torch.device(args.device)
    args.amp = bool(args.amp and device.type == "cuda")
    effective_batch = args.batch_size * args.accum_steps
    tail_effective_batch = len(train_data) % effective_batch or effective_batch
    microsteps_per_epoch = math.ceil(len(train_data) / args.batch_size)
    optimizer_steps_per_epoch = math.ceil(microsteps_per_epoch / args.accum_steps)
    total_optimizer_steps = optimizer_steps_per_epoch * args.epochs
    warmup_steps = (0 if lr_schedule == "finetune_constant" else
                    min(total_optimizer_steps, optimizer_steps_per_epoch * WARMUP_EPOCHS))
    training_protocol = protocol_for(args, optimizer_steps_per_epoch, teacher_sha256)
    output = args.output.resolve()
    validate_output_directory(output, args.resume)

    checkpoint = None
    resume_path = args.resume
    if resume_path is not None:
        if resume_path.name in {"last_resume.pt", "last_resume.prev.pt"}:
            checkpoint, resume_path = load_latest_resume(output, training_protocol)
        else:
            checkpoint = torch.load(resume_path, map_location="cpu", weights_only=False)
        ensure_resume_eligible(checkpoint, training_protocol)
        for key, expected in {
                "architecture_hash": architecture_hash, "dataset_sha256": dataset_hash,
                "dataset_content_sha256": dataset_content_sha256,
                "class_contract": CLASS_CONTRACT, "phase": args.phase,
                "effective_batch": effective_batch}.items():
            if checkpoint.get(key) != expected:
                raise ValueError(f"resume {key} mismatch: {checkpoint.get(key)!r} != {expected!r}")
        _validate_v3_cursors(
            checkpoint, train_size=len(train_data), val_size=len(val_data),
            batch_size=args.batch_size, accum_steps=args.accum_steps,
            optimizer_steps_per_epoch=optimizer_steps_per_epoch, seed=args.seed)
    init_checkpoint = None
    if args.init_checkpoint is not None:
        init_checkpoint = torch.load(args.init_checkpoint, map_location="cpu", weights_only=False)
        if init_checkpoint.get("architecture_hash") != architecture_hash:
            raise ValueError("initial checkpoint architecture mismatch")
        if init_checkpoint.get("class_contract") != CLASS_CONTRACT:
            raise ValueError("initial checkpoint class/head contract mismatch")
        if not isinstance(init_checkpoint.get("model"), dict):
            raise ValueError("initial checkpoint has no model state")

    completed_epochs = 0
    if checkpoint is not None:
        completed_epochs = (int(checkpoint["epoch"]) + 1
                            if checkpoint["format"] == "road-yolo-checkpoint-v2"
                            else int(checkpoint["epoch_index"]) +
                            (checkpoint["stage"] == "epoch_done"))
    if stop_after_epoch and completed_epochs >= stop_after_epoch:
        completed_path = output / "last.pt"
        if (checkpoint.get("format") == RESUME_FORMAT
                and not _matches_completed_checkpoint(completed_path, checkpoint, None)):
            raise ValueError("epoch_done resume has no matching complete last.pt")
        event = {"event": "completed_before_GPU", "epoch_number": completed_epochs,
                 "trained_steps": int(checkpoint["trained_steps"]),
                 "checkpoint": str(completed_path),
                 "resume_checkpoint": str(resume_path)}
        print(json.dumps(event), flush=True)
        return 0
    if getattr(args, "supervised_start", False):
        if args.workers != 0:
            raise ValueError("--supervised-start requires --workers 0")
        ready = {"event": "preflight_ready", "trainer_pid": os.getpid(),
                 "dataset_sha256": dataset_hash,
                 "dataset_content_sha256": dataset_content_sha256,
                 "resume": str(resume_path) if resume_path else None}
        print(json.dumps(ready), flush=True)
        if input().strip() != "GO":
            raise RuntimeError("supervised start requires GO on stdin")
    if args.validate_only:
        return 0

    set_seed(args.seed)
    if device.type == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA requested but unavailable; pass --device cpu explicitly for diagnostics")
    model = RoadYOLOS4().to(device)
    set_training_mode(model, freeze_bn)
    optimizer = torch.optim.SGD((p for p in model.parameters() if p.requires_grad),
                                lr=args.lr, momentum=args.momentum,
                                weight_decay=args.weight_decay)
    amp = args.amp
    scaler = torch.amp.GradScaler("cuda", enabled=amp, init_scale=AMP_INIT_SCALE)
    if init_checkpoint is not None:
        model.load_state_dict(init_checkpoint["model"], strict=True)
    if checkpoint is not None:
        model.load_state_dict(checkpoint["model"])
        optimizer.load_state_dict(checkpoint["optimizer"])
        scaler.load_state_dict(checkpoint.get("scaler", {}))

    if checkpoint is None:
        epoch, stage, trained_steps = 0, "train", 0
        order = epoch_order(len(train_data), args.seed, epoch)
        next_microbatch = next_sample_cursor = 0
        epoch_loss_sum = 0.0
        epoch_samples = val_next_batch = val_samples = 0
        val_loss_sum = 0.0
        last_lr = optimizer.param_groups[0]["lr"]
        last_optimizer_effective_batch = 0
    elif checkpoint["format"] == "road-yolo-checkpoint-v2":
        epoch, stage = int(checkpoint["epoch"]) + 1, "train"
        trained_steps = int(checkpoint["trained_steps"])
        if trained_steps != epoch * optimizer_steps_per_epoch:
            raise ValueError("v2 resume checkpoint is not at a complete epoch boundary")
        order = epoch_order(len(train_data), args.seed, epoch) if epoch < args.epochs else []
        next_microbatch = next_sample_cursor = 0
        epoch_loss_sum = 0.0
        epoch_samples = val_next_batch = val_samples = 0
        val_loss_sum = 0.0
        last_lr = optimizer.param_groups[0]["lr"]
        last_optimizer_effective_batch = int(checkpoint["last_optimizer_effective_batch"])
    else:
        epoch, stage = int(checkpoint["epoch_index"]), checkpoint["stage"]
        trained_steps = int(checkpoint["trained_steps"])
        order = checkpoint["epoch_order"]
        if order != epoch_order(len(train_data), args.seed, epoch):
            raise ValueError("resume epoch order mismatch")
        next_microbatch = int(checkpoint["next_microbatch"])
        next_sample_cursor = int(checkpoint["next_sample_cursor"])
        epoch_loss_sum = float(checkpoint["epoch_loss_sum"])
        epoch_samples = int(checkpoint["epoch_samples"])
        val_next_batch = int(checkpoint["val_next_batch"])
        val_loss_sum = float(checkpoint["val_loss_sum"])
        val_samples = int(checkpoint["val_samples"])
        last_lr = float(checkpoint["last_lr"])
        last_optimizer_effective_batch = int(checkpoint["last_optimizer_effective_batch"])
    if args.max_steps and trained_steps >= args.max_steps:
        raise ValueError("--max-steps must exceed the checkpoint trained_steps")
    if next_sample_cursor != epoch_samples or next_microbatch != math.ceil(
            next_sample_cursor / args.batch_size):
        raise ValueError("resume training cursors disagree")
    completed_in_epoch = (optimizer_steps_per_epoch if stage in {"val", "epoch_done"}
                          else math.ceil(next_microbatch / args.accum_steps))
    if trained_steps != epoch * optimizer_steps_per_epoch + completed_in_epoch:
        raise ValueError("resume optimizer-step cursor disagrees")
    if val_samples > len(val_data) or val_next_batch != math.ceil(
            val_samples / args.batch_size):
        raise ValueError("resume validation cursors disagree")

    criterion = YOLOXLoss()
    if checkpoint is not None:
        restore_rng(checkpoint["rng_state"])
    output.mkdir(parents=True, exist_ok=True)
    log_path = output / "train_log.jsonl"
    common = {"batch_size": args.batch_size, "num_workers": args.workers,
              "pin_memory": device.type == "cuda", "collate_fn": collate}
    startup = {
        "device": str(device), "phase": args.phase, "microbatch": args.batch_size,
        "accum_steps": args.accum_steps, "effective_batch": effective_batch,
        "architecture_hash": architecture_hash, "dataset_sha256": dataset_hash,
        "dataset_content_sha256": dataset_content_sha256,
        "training_protocol": training_protocol,
        "training_protocol_sha256": protocol_hash(training_protocol),
        "optimizer_steps_per_epoch": optimizer_steps_per_epoch,
        "total_optimizer_steps": total_optimizer_steps, "warmup_steps": warmup_steps,
        "tail_effective_batch": tail_effective_batch, "acceptance_eligible": False,
        "input_cache": str(cache_root) if cache_root else None,
        "input_cache_index_sha256": cache_receipt, "stop_after_epoch": stop_after_epoch,
    }
    append_log(log_path, {"event": "start", **startup, "epoch_index": epoch,
                          "stage": stage, "trained_steps": trained_steps})
    print(json.dumps(startup), flush=True)
    optimizer.zero_grad(set_to_none=True)
    checkpoint_steps = getattr(args, "checkpoint_every_steps", 0)
    checkpoint_seconds = getattr(args, "checkpoint_every_seconds", 120.0)
    pause_request = getattr(args, "pause_request", None)
    resumable = args.checkpoint_kind == "training"
    last_save_time = time.perf_counter()

    def live_payload() -> dict[str, Any]:
        return _resume_payload(
            model=model, optimizer=optimizer, scaler=scaler, args=args,
            training_protocol=training_protocol, dataset_hash=dataset_hash,
            dataset_content_sha256=dataset_content_sha256, effective_batch=effective_batch,
            last_optimizer_effective_batch=last_optimizer_effective_batch, stage=stage,
            epoch_index=epoch, order=order, trained_steps=trained_steps,
            next_microbatch=next_microbatch, next_sample_cursor=next_sample_cursor,
            epoch_loss_sum=epoch_loss_sum, epoch_samples=epoch_samples,
            val_next_batch=val_next_batch, val_loss_sum=val_loss_sum,
            val_samples=val_samples, last_lr=last_lr)

    def save_live() -> Path | None:
        nonlocal last_save_time
        if not resumable:
            return None
        path = save_resume_state(output, live_payload())
        last_save_time = time.perf_counter()
        return path

    def requested_pause() -> bool:
        return pause_request is not None and pause_request.exists()

    def paused() -> int:
        path = save_live()
        event = {"event": "paused_segment", "trained_steps": trained_steps,
                 "stage": stage, "epoch_index": epoch,
                 "next_microbatch": next_microbatch,
                 "next_sample_cursor": next_sample_cursor,
                 "val_next_batch": val_next_batch,
                 "checkpoint": str(path) if path else None}
        append_log(log_path, event)
        print(json.dumps(event), flush=True)
        return 0

    if checkpoint is None or checkpoint["format"] == "road-yolo-checkpoint-v2":
        save_live()  # Step zero, or the next epoch boundary imported from v2.
    if requested_pause():
        return paused()

    try:
        while epoch < args.epochs:
            mosaic_active = bool(args.mosaic and epoch < max(0, args.epochs - MOSAIC_CLOSE_EPOCHS))
            train_data.set_epoch(epoch, mosaic=mosaic_active)
            if stage == "epoch_done":
                if stop_after_epoch == epoch + 1:
                    event = {"event": "paused_complete_epoch", "epoch_number": epoch + 1,
                             "trained_steps": trained_steps, "epochs_total": args.epochs,
                             "checkpoint": str(output / "last.pt")}
                    append_log(log_path, event)
                    print(json.dumps(event), flush=True)
                    return 0
                epoch += 1
                if epoch >= args.epochs:
                    break
                stage, order = "train", epoch_order(len(train_data), args.seed, epoch)
                next_microbatch = next_sample_cursor = 0
                epoch_loss_sum = 0.0
                epoch_samples = val_next_batch = val_samples = 0
                val_loss_sum = 0.0
                save_live()
                continue

            if stage == "train":
                set_training_mode(model, freeze_bn)
                sampler = order[next_sample_cursor:]
                loader = DataLoader(train_data, sampler=sampler, shuffle=False,
                                    generator=torch.Generator().manual_seed(args.seed + epoch),
                                    **common)
                iterator = iter(loader)
                optimizer_step_samples = 0
                group_data_seconds = group_compute_seconds = 0.0
                group_gpu_events = []
                while True:
                    data_started = time.perf_counter()
                    try:
                        images, targets, keys = next(iterator)
                    except StopIteration:
                        break
                    group_data_seconds += time.perf_counter() - data_started
                    microstep = next_microbatch
                    batch_samples = int(images.shape[0])
                    optimizer_step_samples += batch_samples
                    compute_started = time.perf_counter()
                    gpu_pair = None
                    if device.type == "cuda":
                        gpu_pair = (torch.cuda.Event(enable_timing=True),
                                    torch.cuda.Event(enable_timing=True))
                        gpu_pair[0].record()
                    images = images.to(device, non_blocking=True)
                    with torch.amp.autocast(device_type=device.type, enabled=amp):
                        outputs = model(images)
                        result = criterion(outputs, targets)
                        total_loss = result["loss"]
                        if teacher is not None:
                            total_loss = total_loss + args.distill_weight * dense_distillation_loss(
                                outputs, teacher.batch(keys, device), targets)
                        group_samples = accumulation_group_samples(
                            microstep, microsteps_per_epoch, args.accum_steps,
                            args.batch_size, len(train_data))
                        scaled_loss = total_loss * batch_samples / group_samples
                    if not torch.isfinite(total_loss).item():
                        raise FloatingPointError(
                            f"non-finite training loss at epoch {epoch}, microstep {microstep}")
                    scaler.scale(scaled_loss).backward()
                    if gpu_pair is not None:
                        gpu_pair[1].record()
                        group_gpu_events.append(gpu_pair)
                    group_compute_seconds += time.perf_counter() - compute_started
                    epoch_loss_sum += float(total_loss.detach().item()) * batch_samples
                    epoch_samples += batch_samples
                    next_sample_cursor += batch_samples
                    next_microbatch += 1
                    due = (next_microbatch % args.accum_steps == 0
                           or next_microbatch == microsteps_per_epoch)
                    if not due:
                        continue
                    scaler.unscale_(optimizer)
                    gradient_norm = torch.nn.utils.clip_grad_norm_(
                        model.parameters(), args.clip_grad, error_if_nonfinite=True)
                    if not torch.isfinite(gradient_norm).item():
                        raise FloatingPointError(
                            f"non-finite gradient at epoch {epoch}, microstep {microstep}")
                    last_lr = scheduled_lr(trained_steps, total_optimizer_steps,
                                           warmup_steps, args.lr, lr_schedule)
                    for group in optimizer.param_groups:
                        group["lr"] = last_lr
                    scaler.step(optimizer)
                    scaler.update()
                    optimizer.zero_grad(set_to_none=True)
                    trained_steps += 1
                    last_optimizer_effective_batch = optimizer_step_samples
                    optimizer_step_samples = 0
                    gpu_compute_ms = None
                    if group_gpu_events:
                        group_gpu_events[-1][1].synchronize()
                        gpu_compute_ms = sum(start.elapsed_time(end)
                                             for start, end in group_gpu_events)
                    progress = {
                        "event": "step", "epoch_number": epoch + 1,
                        "optimizer_steps_completed": trained_steps,
                        "optimizer_steps_total": total_optimizer_steps,
                        "epoch_samples": epoch_samples,
                        "train_loss": epoch_loss_sum / epoch_samples, "lr": last_lr,
                        "mosaic": mosaic_active, "data_seconds": group_data_seconds,
                        "compute_seconds": group_compute_seconds,
                        "gpu_compute_ms": gpu_compute_ms,
                    }
                    append_log(log_path, progress)
                    print(json.dumps(progress), flush=True)
                    group_data_seconds = group_compute_seconds = 0.0
                    group_gpu_events = []
                    due_checkpoint = ((checkpoint_steps > 0
                                       and trained_steps % checkpoint_steps == 0)
                                      or (checkpoint_seconds > 0 and
                                          time.perf_counter() - last_save_time
                                          >= checkpoint_seconds))
                    if due_checkpoint:
                        save_live()
                    if requested_pause():
                        return paused()
                    if args.max_steps and trained_steps >= args.max_steps:
                        if next_microbatch != microsteps_per_epoch:
                            metric = {"name": "not_run_partial_epoch", "value": None,
                                      "status": "diagnostic_partial_epoch_not_resumable",
                                      "train_loss": epoch_loss_sum / max(epoch_samples, 1)}
                            save_checkpoint(
                                output / "interrupted.pt", model=model, optimizer=optimizer,
                                scaler=scaler, epoch=epoch, trained_steps=trained_steps,
                                phase=args.phase, checkpoint_kind=args.checkpoint_kind,
                                dataset_hash=dataset_hash,
                                dataset_content_sha256=dataset_content_sha256,
                                effective_batch=effective_batch,
                                last_optimizer_effective_batch=last_optimizer_effective_batch,
                                metric=metric, training_protocol=training_protocol,
                                interrupted=True)
                            return 0
                        break
                if next_microbatch != microsteps_per_epoch:
                    raise RuntimeError("training loader ended before the epoch cursor")
                stage = "val"
                val_next_batch = val_samples = 0
                val_loss_sum = 0.0
                save_live()  # Train complete; validation has not consumed a batch.
                if requested_pause():
                    return paused()

            if stage == "val":
                model.eval()
                remaining = range(val_samples, len(val_data))
                val_loader = DataLoader(val_data, sampler=remaining, shuffle=False,
                                        generator=torch.Generator().manual_seed(args.seed),
                                        **common)
                with torch.no_grad():
                    for images, targets, _keys in val_loader:
                        images = images.to(device, non_blocking=True)
                        with torch.amp.autocast(device_type=device.type, enabled=amp):
                            result = criterion(model(images), targets)
                        loss = float(result["loss"].item())
                        if not math.isfinite(loss):
                            raise FloatingPointError("non-finite validation loss")
                        val_loss_sum += loss * images.shape[0]
                        val_samples += int(images.shape[0])
                        val_next_batch += 1
                        save_started = time.perf_counter()
                        save_live()
                        validation_progress = {
                            "event": "val_batch", "epoch_number": epoch + 1,
                            "val_next_batch": val_next_batch, "val_samples": val_samples,
                            "checkpoint_seconds": time.perf_counter() - save_started,
                        }
                        append_log(log_path, validation_progress)
                        print(json.dumps(validation_progress), flush=True)
                        if requested_pause():
                            return paused()
                set_training_mode(model, freeze_bn)
                if val_samples != len(val_data):
                    raise RuntimeError("validation loader ended before the validation cursor")
                metric = {
                    "name": "validation_loss_stub",
                    "value": val_loss_sum / max(val_samples, 1),
                    "status": "unaccepted_no_AP_precision_or_recall",
                    "train_loss": epoch_loss_sum / max(epoch_samples, 1),
                }
                checkpoint_path = output / f"epoch_{epoch:04d}.pt"
                if checkpoint_path.exists():
                    if not _matches_completed_checkpoint(
                            checkpoint_path, live_payload(), metric):
                        raise FileExistsError(
                            f"different checkpoint would be overwritten: {checkpoint_path}")
                else:
                    save_checkpoint(
                        checkpoint_path, model=model, optimizer=optimizer, scaler=scaler,
                        epoch=epoch, trained_steps=trained_steps, phase=args.phase,
                        checkpoint_kind=args.checkpoint_kind, dataset_hash=dataset_hash,
                        dataset_content_sha256=dataset_content_sha256,
                        effective_batch=effective_batch,
                        last_optimizer_effective_batch=last_optimizer_effective_batch,
                        metric=metric, training_protocol=training_protocol)
                save_checkpoint(
                    output / "last.pt", model=model, optimizer=optimizer, scaler=scaler,
                    epoch=epoch, trained_steps=trained_steps, phase=args.phase,
                    checkpoint_kind=args.checkpoint_kind, dataset_hash=dataset_hash,
                    dataset_content_sha256=dataset_content_sha256,
                    effective_batch=effective_batch,
                    last_optimizer_effective_batch=last_optimizer_effective_batch,
                    metric=metric, training_protocol=training_protocol)
                stage = "epoch_done"
                save_live()
                event = {"event": "epoch", "epoch_index": epoch,
                         "epoch_number": epoch + 1, "epochs_total": args.epochs,
                         "optimizer_steps_completed": trained_steps,
                         "optimizer_steps_total": total_optimizer_steps,
                         "lr": last_lr, "mosaic": mosaic_active,
                         "epoch_complete": True, **metric}
                append_log(log_path, event)
                print(json.dumps(event), flush=True)
    except KeyboardInterrupt:
        print("interrupted; latest completed resume boundary retained", flush=True)
        return 130
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--phase", choices=("supervised", "distill", "qat"),
                        default="supervised")
    parser.add_argument("--teacher-cache", type=Path)
    parser.add_argument("--distill-weight", type=float, default=1.0)
    parser.add_argument("--epochs", type=int, default=300)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--accum-steps", type=int, default=8)
    parser.add_argument("--lr", type=float, default=0.01)
    parser.add_argument("--lr-schedule", choices=LR_SCHEDULES, default="warmup_cosine")
    parser.add_argument("--momentum", type=float, default=0.9)
    parser.add_argument("--weight-decay", type=float, default=5e-4)
    parser.add_argument("--clip-grad", type=float, default=10.0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--amp", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--mosaic", action=argparse.BooleanOptionalAction, default=True,
                        help="four full-frame tiles; automatically off for final 15 epochs")
    parser.add_argument("--freeze-bn", action="store_true",
                        help="freeze BatchNorm running statistics and affine parameters")
    parser.add_argument("--resume", type=Path)
    parser.add_argument("--init-checkpoint", type=Path)
    parser.add_argument("--checkpoint-kind", choices=("diagnostic", "training"),
                        default="training")
    parser.add_argument("--max-steps", type=int, default=0,
                        help="diagnostic stop after optimizer steps; never an accuracy run")
    parser.add_argument("--stop-after-epoch", type=int, default=0,
                        help="pause after this complete one-based epoch; preserve the full schedule")
    parser.add_argument("--checkpoint-every-steps", type=int, default=0,
                        help="save resumable state after this many optimizer updates")
    parser.add_argument("--checkpoint-every-seconds", type=float, default=120.0,
                        help="maximum seconds between resumable update-boundary saves")
    parser.add_argument("--pause-request", type=Path,
                        help="pause at the next saved complete update/batch boundary")
    parser.add_argument("--supervised-start", action="store_true",
                        help="emit preflight_ready and wait for GO before CUDA startup")
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--input-cache", type=Path, help="opt-in pre-Mosaic disk cache")
    parser.add_argument("--input-cache-index-sha256", help="required pinned index receipt")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    for name in ("epochs", "batch_size", "accum_steps", "workers"):
        if getattr(args, name) < (0 if name == "workers" else 1):
            raise ValueError(f"--{name.replace('_', '-')} is out of range")
    if (args.max_steps < 0 or args.checkpoint_every_steps < 0
            or args.checkpoint_every_seconds < 0 or args.lr <= 0 or args.distill_weight < 0
            or args.momentum < 0 or args.weight_decay < 0 or args.clip_grad <= 0):
        raise ValueError("training numeric option is out of range")
    if args.max_steps and args.checkpoint_kind != "diagnostic":
        raise ValueError("--max-steps requires --checkpoint-kind diagnostic")
    return train(args)


if __name__ == "__main__":
    # Cache imports must share the snapshot class with -m and script entrypoints.
    sys.modules[f"{__package__}.train" if __package__ else "train"] = sys.modules[__name__]
    raise SystemExit(main())
