"""Crash-safe resumable training state slots."""

from __future__ import annotations

import os
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Callable

import torch


FORMAT = "road-yolo-resume-v3"
STAGES = {"train", "val", "epoch_done"}


def validate_resume_state(state: dict[str, Any],
                          expected_protocol: dict[str, Any] | None = None) -> None:
    if state.get("format") != FORMAT:
        raise ValueError("not a road-yolo v3 resume state")
    if state.get("checkpoint_kind") != "training" or state.get("interrupted"):
        raise ValueError("diagnostic/interrupted state is not resumable")
    if state.get("stage") not in STAGES:
        raise ValueError("resume stage must be train, val, or epoch_done")
    if expected_protocol is not None and state.get("training_protocol") != expected_protocol:
        raise ValueError("resume training protocol mismatch")
    protocol = state.get("training_protocol")
    if not isinstance(protocol, dict):
        raise ValueError("resume state has no training protocol")
    digest = hashlib.sha256(json.dumps(
        protocol, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    if state.get("training_protocol_sha256") != digest:
        raise ValueError("resume training protocol digest mismatch")
    for field in ("model", "optimizer", "rng_state"):
        if not isinstance(state.get(field), dict):
            raise ValueError(f"resume state has no {field}")
    for field in ("epoch_index", "trained_steps", "next_microbatch",
                  "next_sample_cursor", "epoch_samples", "val_next_batch",
                  "val_samples"):
        if not isinstance(state.get(field), int) or state[field] < 0:
            raise ValueError(f"invalid resume {field}")
    order = state.get("epoch_order")
    if not isinstance(order, list) or any(not isinstance(index, int) for index in order):
        raise ValueError("invalid resume epoch_order")
    cursor = state["next_sample_cursor"]
    if cursor > len(order):
        raise ValueError("resume sample cursor exceeds epoch order")
    if state["stage"] == "train" and (state["val_next_batch"] or state["val_samples"]
                                        or float(state.get("val_loss_sum", 0.0))):
        raise ValueError("training resume cannot have a validation cursor")
    for field in ("epoch_loss_sum", "val_loss_sum", "last_lr"):
        value = state.get(field)
        if not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
            raise ValueError(f"invalid resume {field}")


def _load(path: Path, expected_protocol: dict[str, Any] | None) -> dict[str, Any]:
    state = torch.load(path, map_location="cpu", weights_only=False)
    if not isinstance(state, dict):
        raise ValueError("resume payload is not a dictionary")
    validate_resume_state(state, expected_protocol)
    return state


def load_latest_resume(output: Path, expected_protocol: dict[str, Any] | None = None
                       ) -> tuple[dict[str, Any], Path]:
    """Load newest valid slot, falling back to the previous completed write."""
    errors = []
    for name in ("last_resume.pt", "last_resume.prev.pt"):
        path = Path(output) / name
        if not path.is_file():
            continue
        try:
            return _load(path, expected_protocol), path
        except Exception as error:
            errors.append(f"{name}: {error}")
    detail = "; ".join(errors) if errors else "no resume slots exist"
    raise ValueError(f"no valid resumable checkpoint in {output}: {detail}")


def save_resume_state(output: Path, state: dict[str, Any], *,
                      replace: Callable[[str | Path, str | Path], None] = os.replace) -> Path:
    """Durably write last_resume.pt while retaining the prior valid slot."""
    validate_resume_state(state, state["training_protocol"])
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    latest = output / "last_resume.pt"
    previous = output / "last_resume.prev.pt"
    temporary = output / "last_resume.pt.tmp"
    with temporary.open("wb") as handle:
        torch.save(state, handle)
        handle.flush()
        os.fsync(handle.fileno())
    if latest.exists():
        try:
            _load(latest, state["training_protocol"])
        except Exception:
            pass  # Preserve the previous valid slot; the bad latest is replaceable.
        else:
            replace(latest, previous)
    replace(temporary, latest)
    return latest
