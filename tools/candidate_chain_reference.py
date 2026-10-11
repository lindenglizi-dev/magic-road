#!/usr/bin/env python3
"""Python reference for the current 720p-to-CCL candidate geometry path.

This is an algorithm/coordinate reference, not a cycle-accurate RLE-CCL model.
Its default configuration matches the deployed grayscale and stride-five
sampling, four-frame integer background learning, threshold comparison,
center-preserving 3x3 cleanup and 8-connected component geometry.  A different
sample stride is accepted only for explicitly labelled Python diagnostics.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path

import cv2
import numpy as np

from roi_dataset_tool import fpga_analysis_frame


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


@dataclass(frozen=True)
class Candidate:
    component_label: int
    area: int
    xmin: int
    ymin: int
    xmax: int
    ymax: int

    @property
    def source_sample_box(self) -> tuple[int, int, int, int]:
        """Source locations of the corner samples, not five-pixel cell extents."""
        return (5 * self.xmin, 5 * self.ymin, 5 * self.xmax, 5 * self.ymax)


def toward(old: np.ndarray, new: np.ndarray, shift: int) -> np.ndarray:
    """Match RTL unsigned learn/update_toward with minimum nonzero step one."""
    old16, new16 = old.astype(np.int16), new.astype(np.int16)
    difference = new16 - old16
    step = np.abs(difference) >> shift
    step[(difference != 0) & (step == 0)] = 1
    result = old16 + np.sign(difference) * step
    return result.astype(np.uint8)


def cleanup_3x3(mask: np.ndarray, min_neighbors: int = 3,
                require_center: bool = True) -> np.ndarray:
    binary = (mask != 0).astype(np.uint8)
    neighbors = cv2.filter2D(binary, cv2.CV_16U, np.ones((3, 3), np.uint8),
                             borderType=cv2.BORDER_CONSTANT)
    kept = neighbors >= min_neighbors
    if require_center:
        kept &= binary.astype(bool)
    return kept.astype(np.uint8)


def filter_short_runs(mask: np.ndarray, min_run_length: int = 2) -> np.ndarray:
    """Match run_detector's per-row minimum run length before connectivity."""
    if mask.ndim != 2:
        raise ValueError("run mask must be two-dimensional")
    if min_run_length < 1:
        raise ValueError("min_run_length must be positive")
    binary = (mask != 0).astype(np.uint8)
    if min_run_length == 1:
        return binary
    filtered = np.zeros_like(binary)
    if min_run_length == 2:
        # A pixel belongs to a run of at least two iff a horizontal neighbor is set.
        pairs = binary[:, :-1] & binary[:, 1:]
        filtered[:, :-1] |= pairs
        filtered[:, 1:] |= pairs
        return filtered
    for y, row in enumerate(binary):
        padded = np.pad(row, (1, 1), constant_values=0)
        transitions = np.diff(padded.astype(np.int8))
        starts = np.flatnonzero(transitions == 1)
        ends = np.flatnonzero(transitions == -1) - 1
        for start, end in zip(starts, ends):
            if end - start + 1 >= min_run_length:
                filtered[y, start:end + 1] = 1
    return filtered


def components(mask: np.ndarray, min_area: int = 16, top_k: int = 4) -> list[Candidate]:
    count, _, stats, _ = cv2.connectedComponentsWithStats(
        (mask != 0).astype(np.uint8), connectivity=8)
    candidates = []
    for label in range(1, count):
        x, y, width, height, area = (int(value) for value in stats[label])
        if area >= min_area:
            candidates.append(Candidate(label, area, x, y, x + width - 1, y + height - 1))
    candidates.sort(key=lambda item: (-item.area, item.component_label))
    return candidates[:top_k]


class CandidateChainReference:
    def __init__(self, learn_frames: int = 4, threshold: int = 20,
                 min_neighbors: int = 3, min_area: int = 16,
                 update_enable: bool = True, freeze_foreground: bool = True,
                 min_run: int = 2, top_k: int = 4, sample_stride: int = 5):
        if learn_frames < 1 or not 0 <= threshold <= 255:
            raise ValueError("invalid learning/threshold configuration")
        self.learn_frames = learn_frames
        self.threshold = threshold
        self.min_neighbors = min_neighbors
        self.min_area = min_area
        if min_area < 1 or min_run < 1 or top_k < 1 or sample_stride < 1:
            raise ValueError("min_area, min_run, top_k and sample_stride must be positive")
        self.min_run = min_run
        self.top_k = top_k
        self.sample_stride = sample_stride
        self.analysis_shape = (
            (720 + sample_stride - 1) // sample_stride,
            (1280 + sample_stride - 1) // sample_stride,
        )
        self.update_enable = update_enable
        self.freeze_foreground = freeze_foreground
        self.background: np.ndarray | None = None
        self.learned_frame_count = 0
        self.last_frame_index: int | None = None

    def process_analysis(self, gray: np.ndarray, frame_index: int) -> dict[str, object]:
        if gray.shape != self.analysis_shape or gray.dtype != np.uint8:
            width, height = self.analysis_shape[1], self.analysis_shape[0]
            raise ValueError(f"analysis frame must be uint8 {width}x{height}")
        if frame_index < 0 or (self.last_frame_index is not None and frame_index <= self.last_frame_index):
            raise ValueError("frame_index must be nonnegative and strictly increasing")
        self.last_frame_index = frame_index
        if self.background is None:
            self.background = gray.copy()
            self.learned_frame_count = 1
            return self._learning_result(frame_index, gray)
        if self.learned_frame_count < self.learn_frames:
            self.background = toward(self.background, gray, 2)
            self.learned_frame_count += 1
            return self._learning_result(frame_index, gray)

        difference = np.abs(gray.astype(np.int16) - self.background.astype(np.int16)).astype(np.uint8)
        raw_mask = (difference >= self.threshold).astype(np.uint8)
        clean_mask = cleanup_3x3(raw_mask, self.min_neighbors, True)
        run_filtered_mask = filter_short_runs(clean_mask, self.min_run)
        found = components(run_filtered_mask, self.min_area, self.top_k)
        background_before_update = self.background.copy()
        if self.update_enable:
            eligible = np.ones_like(raw_mask, dtype=bool)
            if self.freeze_foreground:
                eligible &= raw_mask == 0
            updated = toward(self.background, gray, 4)
            self.background[eligible] = updated[eligible]
        return {
            "frame_index": frame_index,
            "learning": False,
            "background_ready": True,
            "analysis_shape": [self.analysis_shape[1], self.analysis_shape[0]],
            "threshold_comparison": "abs(gray-background) >= threshold",
            "foreground_pixels_raw": int(raw_mask.sum()),
            "foreground_pixels_clean": int(clean_mask.sum()),
            "foreground_pixels_after_min_run": int(run_filtered_mask.sum()),
            "candidates": [
                {**asdict(candidate), "source_sample_box": [
                    self.sample_stride * candidate.xmin,
                    self.sample_stride * candidate.ymin,
                    self.sample_stride * candidate.xmax,
                    self.sample_stride * candidate.ymax,
                ]}
                for candidate in found],
            "gray": gray,
            "background": background_before_update,
            "difference": difference,
            "raw_mask": raw_mask,
            "clean_mask": clean_mask,
            "run_filtered_mask": run_filtered_mask,
        }

    def process_bgr(self, frame: np.ndarray, frame_index: int) -> dict[str, object]:
        if self.sample_stride == 5:
            analysis = fpga_analysis_frame(frame)
        else:
            if frame.shape[:2] != (720, 1280):
                raise ValueError("diagnostic input must be 1280x720")
            from roi_dataset_tool import fpga_gray_bgr
            analysis = fpga_gray_bgr(frame)[::self.sample_stride, ::self.sample_stride]
        return self.process_analysis(analysis, frame_index)

    def _learning_result(self, frame_index: int, gray: np.ndarray) -> dict[str, object]:
        return {
            "frame_index": frame_index,
            "learning": True,
            "background_ready": self.learned_frame_count >= self.learn_frames,
            "learned_frame_count": self.learned_frame_count,
            "analysis_shape": [self.analysis_shape[1], self.analysis_shape[0]],
            "candidates": [],
            "gray": gray,
            "background": self.background.copy(),
            "difference": np.zeros_like(gray),
            "raw_mask": np.zeros_like(gray),
            "clean_mask": np.zeros_like(gray),
            "run_filtered_mask": np.zeros_like(gray),
        }


def serializable_result(result: dict[str, object]) -> dict[str, object]:
    return {key: value for key, value in result.items() if not isinstance(value, np.ndarray)}


def run_video(video: Path, output: Path, frame_count: int = 60,
              threshold: int = 20, mode: str = "deployed",
              start_frame: int = 0) -> dict[str, object]:
    if mode not in {"deployed", "static-background-diagnostic"}:
        raise ValueError("unknown candidate reference mode")
    chain = CandidateChainReference(
        threshold=threshold, update_enable=(mode == "deployed"), freeze_foreground=True)
    cap = cv2.VideoCapture(str(video))
    if not cap.isOpened():
        raise ValueError(f"cannot open {video}")
    records = []
    try:
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        for offset in range(frame_count):
            ok, frame = cap.read()
            if not ok:
                break
            frame_index = start_frame + offset
            records.append(serializable_result(chain.process_bgr(frame, frame_index)))
    finally:
        cap.release()
    output.mkdir(parents=True, exist_ok=True)
    contract = {
        "status": "algorithm_and_coordinate_reference_not_cycle_accurate_rle_ccl",
        "mode": mode,
        "input": "1280x720 BGR decoded frame with zero-based frame_index",
        "gray": "(R>>2)+(G>>1)+(B>>2), uint8",
        "sampling": "analysis[y,x]=gray[5*y,5*x], yielding deployed 256x144; this deliberately does not use background_model.v's generic default FRAME_HEIGHT=150",
        "learning": "first frame initializes; next three frames use toward(old,new,shift=2,min_step=1); no candidates during four learning frames",
        "difference": f"foreground when abs(gray-background) >= {threshold}",
        "threshold": threshold,
        "post_learning_update": ("deployed: background_update_enable=1, freeze_foreground=1, "
                                 "toward shift=4 with minimum step one" if mode == "deployed" else
                                 "static-background-diagnostic: updates disabled by explicit mode"),
        "cleanup": "zero-padded 3x3 sum >=3 and center pixel must be one",
        "run_filter": "after cleanup, discard each horizontal run shorter than MIN_RUN_LENGTH=2",
        "components": "8-connected; area is foreground pixel count; inclusive bbox; top four by descending area then scan label",
        "coordinate_mapping": "candidate boxes use inclusive analysis coordinates; source_sample_box multiplies each coordinate by five and denotes sampled source locations",
        "frame_identity": "output frame_index equals the input video frame consumed for that mask; no display/HDMI identity is inferred",
        "unmodeled_rtl_limits": "MAX_RUN=64, MAX_LABEL=32, overflow/discard behavior, and cycle-level label-union timing are not modeled",
    }
    summary = {
        "contract": contract,
        "video": str(video.resolve()),
        "video_sha256": digest(video),
        "script_sha256": digest(Path(__file__)),
        "parameters": {
            "requested_frame_count": frame_count,
            "start_frame": start_frame,
            "threshold": threshold,
            "mode": mode,
        },
        "processed_frames": len(records),
        "learning_frames": sum(record["learning"] for record in records),
        "candidate_frames": sum(bool(record["candidates"]) for record in records),
        "candidate_count": sum(len(record["candidates"]) for record in records),
        "frames": records,
    }
    (output / "contract.json").write_text(
        json.dumps(contract, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "run_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--frames", type=int, default=60)
    parser.add_argument("--start-frame", type=int, default=0)
    parser.add_argument("--threshold", type=int, default=20)
    parser.add_argument("--mode", choices=("deployed", "static-background-diagnostic"),
                        default="deployed")
    args = parser.parse_args()
    if args.frames < 1 or args.start_frame < 0:
        raise ValueError("--frames must be positive and --start-frame nonnegative")
    result = run_video(args.video, args.output, args.frames, args.threshold, args.mode,
                       args.start_frame)
    print(json.dumps({key: result[key] for key in (
        "processed_frames", "learning_frames", "candidate_frames", "candidate_count")},
        ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
