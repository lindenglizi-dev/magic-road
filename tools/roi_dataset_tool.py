#!/usr/bin/env python3
"""Interactive video-to-ROI dataset tool matching the FPGA analysis path."""

from __future__ import annotations

import argparse
import csv
import hashlib
import tempfile
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np

ROI_SIZE = 32
MANIFEST_FIELDS = [
    "sample_id", "split", "label", "class_id", "source_video",
    "frame_index", "timestamp_ms", "source_width", "source_height",
    "analysis_width", "analysis_height", "xmin", "ymin", "xmax", "ymax",
    "crop_path", "roi_path", "roi_sha256",
    "scene_id", "source_sha256", "source_family", "roi_source", "reviewer",
]


def fpga_gray_bgr(frame_bgr: np.ndarray) -> np.ndarray:
    """Match (R>>2)+(G>>1)+(B>>2) in awb96_analysis_adapter."""
    values = frame_bgr.astype(np.uint16)
    return ((values[:, :, 2] >> 2) + (values[:, :, 1] >> 1) +
            (values[:, :, 0] >> 2)).astype(np.uint8)


def fpga_analysis_frame(frame_bgr: np.ndarray) -> np.ndarray:
    """Match the fixed x=0,5,10... and y=0,5,10... analysis sampling."""
    if frame_bgr.shape[:2] != (720, 1280):
        raise ValueError("hardware-aligned input must be 1280x720; prepare and record a 720p derivative first")
    return fpga_gray_bgr(frame_bgr)[::5, ::5]


def fpga_resize_roi(gray_crop: np.ndarray) -> np.ndarray:
    """Match roi_frame_reader pixel-centre Q8 nearest-neighbour DDA."""
    height, width = gray_crop.shape
    if width < 1 or height < 1:
        raise ValueError("empty ROI crop")
    positions = np.arange(ROI_SIZE, dtype=np.int64)
    xs = np.minimum((width * (4 + 8 * positions)) >> 8, width - 1)
    ys = np.minimum((height * (4 + 8 * positions)) >> 8, height - 1)
    return gray_crop[np.ix_(ys, xs)]


def normalize_box(start: tuple[int, int], end: tuple[int, int],
                  width: int, height: int) -> tuple[int, int, int, int]:
    x0, x1 = sorted((start[0], end[0]))
    y0, y1 = sorted((start[1], end[1]))
    return (max(0, min(x0, width - 1)), max(0, min(y0, height - 1)),
            max(0, min(x1, width - 1)), max(0, min(y1, height - 1)))


@dataclass
class SaveResult:
    saved: bool
    message: str


class DatasetWriter:
    def __init__(self, output_root: Path, video_path: Path, split: str,
                 scene_id: str = "", roi_source: str = "manual", reviewer: str = "human"):
        self.root = output_root.resolve()
        self.video_path = video_path.resolve()
        self.split = split
        if split not in {"train", "val", "test"}:
            raise ValueError("split must be train, val or test")
        if roi_source not in {"manual", "annotated", "ccl"}:
            raise ValueError("roi_source must be manual, annotated or ccl")
        self.scene_id = scene_id.strip() or video_path.stem.removesuffix("_raw")
        self.source_family = video_path.stem.removesuffix("_raw")
        self.source_hash = hashlib.sha256(self.video_path.read_bytes()).hexdigest()
        self.roi_source = roi_source
        self.reviewer = reviewer
        self.manifest_path = self.root / "manifest.csv"
        self.rows: list[dict[str, str]] = []
        self.exact_keys: set[tuple[str, ...]] = set()
        self.roi_hashes: set[tuple[str, str, str]] = set()
        self.undo_stack: list[str] = []
        self.video_token = hashlib.sha1(
            str(self.video_path).encode("utf-8")
        ).hexdigest()[:8]
        self.root.mkdir(parents=True, exist_ok=True)
        self._load_manifest()

    def _load_manifest(self) -> None:
        if not self.manifest_path.exists():
            return
        with self.manifest_path.open("r", newline="", encoding="utf-8-sig") as handle:
            for row in csv.DictReader(handle):
                if not all(field in row for field in MANIFEST_FIELDS):
                    raise ValueError("legacy manifest: migrate scene/provenance explicitly; do not infer split safety")
                same_group = (row["source_video"] == str(self.video_path) or
                              row["source_sha256"] == self.source_hash or
                              row["source_family"] == self.source_family or
                              row["scene_id"] == self.scene_id)
                if same_group and row["split"] != self.split:
                    raise ValueError(
                        f"this video already belongs to split={row['split']}; "
                        "do not mix one video/family/scene across train/val/test"
                    )
                self.rows.append(row)
                self.exact_keys.add((row["source_video"], row["frame_index"],
                                     row["xmin"], row["ymin"], row["xmax"],
                                     row["ymax"], row["roi_source"]))
                self.roi_hashes.add((row["split"], row["label"], row["roi_sha256"]))

    def _rewrite_manifest(self) -> None:
        temporary = self.manifest_path.with_suffix(".csv.tmp")
        with temporary.open("w", newline="", encoding="utf-8-sig") as handle:
            writer = csv.DictWriter(handle, fieldnames=MANIFEST_FIELDS)
            writer.writeheader()
            writer.writerows(self.rows)
        temporary.replace(self.manifest_path)

    def save(self, analysis_gray: np.ndarray, frame_index: int, fps: float,
             source_size: tuple[int, int], box: tuple[int, int, int, int],
             label: str) -> SaveResult:
        if label not in {"ped", "vehicle", "invalid"}:
            return SaveResult(False, f"unsupported label: {label}")
        xmin, ymin, xmax, ymax = box
        if not (0 <= xmin <= xmax < analysis_gray.shape[1] and
                0 <= ymin <= ymax < analysis_gray.shape[0]):
            return SaveResult(False, "box is outside analysis image")
        if xmax - xmin + 1 < 2 or ymax - ymin + 1 < 2:
            return SaveResult(False, "box must be at least 2x2 analysis pixels")

        relative_video = str(self.video_path)
        exact_key = (relative_video, str(frame_index), str(xmin), str(ymin),
                     str(xmax), str(ymax), self.roi_source)
        if exact_key in self.exact_keys:
            return SaveResult(False, "same frame/box already exists, possibly with another label")

        crop = analysis_gray[ymin:ymax + 1, xmin:xmax + 1]
        roi = fpga_resize_roi(crop)
        roi_hash = hashlib.sha256(roi.tobytes()).hexdigest()
        if any(row["roi_sha256"] == roi_hash and
               (row["split"] != self.split or row["label"] != label or
                row["roi_source"] == self.roi_source) for row in self.rows):
            return SaveResult(False, "duplicate ROI, conflicting label or cross-split pixel leakage")

        sample_id = (f"{self.video_path.stem}_{self.video_token}_"
                     f"f{frame_index:08d}_x{xmin:03d}-{xmax:03d}_"
                     f"y{ymin:03d}-{ymax:03d}_{self.roi_source}_{label}")
        roi_relative = Path(self.split) / label / f"{sample_id}.png"
        crop_relative = Path("raw_crops") / self.split / label / f"{sample_id}.png"
        roi_path = self.root / roi_relative
        crop_path = self.root / crop_relative
        roi_path.parent.mkdir(parents=True, exist_ok=True)
        crop_path.parent.mkdir(parents=True, exist_ok=True)
        if not cv2.imwrite(str(roi_path), roi):
            return SaveResult(False, f"failed to write {roi_path}")
        if not cv2.imwrite(str(crop_path), crop):
            roi_path.unlink(missing_ok=True)
            return SaveResult(False, f"failed to write {crop_path}")

        source_width, source_height = source_size
        row = {
            "sample_id": sample_id,
            "split": self.split,
            "label": label,
            "class_id": {"ped": "0", "vehicle": "1", "invalid": "-1"}[label],
            "scene_id": self.scene_id, "source_sha256": self.source_hash,
            "source_family": self.source_family, "roi_source": self.roi_source,
            "reviewer": self.reviewer,
            "source_video": relative_video,
            "frame_index": str(frame_index),
            "timestamp_ms": f"{(1000.0 * frame_index / fps) if fps > 0 else 0.0:.3f}",
            "source_width": str(source_width),
            "source_height": str(source_height),
            "analysis_width": str(analysis_gray.shape[1]),
            "analysis_height": str(analysis_gray.shape[0]),
            "xmin": str(xmin), "ymin": str(ymin),
            "xmax": str(xmax), "ymax": str(ymax),
            "crop_path": crop_relative.as_posix(),
            "roi_path": roi_relative.as_posix(),
            "roi_sha256": roi_hash,
        }
        self.rows.append(row)
        self.exact_keys.add(exact_key)
        self.roi_hashes.add((self.split, label, roi_hash))
        self.undo_stack.append(sample_id)
        self._rewrite_manifest()
        return SaveResult(True, f"saved {label}: {roi_relative.as_posix()}")

    def undo(self) -> SaveResult:
        if not self.undo_stack:
            return SaveResult(False, "nothing saved in this session to undo")
        sample_id = self.undo_stack.pop()
        index = next((i for i in range(len(self.rows) - 1, -1, -1)
                      if self.rows[i]["sample_id"] == sample_id), None)
        if index is None:
            return SaveResult(False, "undo entry no longer exists")
        row = self.rows.pop(index)
        for field in ("roi_path", "crop_path"):
            target = (self.root / row[field]).resolve()
            if target.is_relative_to(self.root):
                target.unlink(missing_ok=True)
        exact_key = (row["source_video"], row["frame_index"], row["xmin"],
                     row["ymin"], row["xmax"], row["ymax"], row["roi_source"])
        self.exact_keys.discard(exact_key)
        self.roi_hashes.discard((row["split"], row["label"], row["roi_sha256"]))
        self._rewrite_manifest()
        return SaveResult(True, f"removed {sample_id}")


class AnnotationApp:
    def __init__(self, video: Path, output: Path, split: str,
                 stride: int, start_frame: int, display_scale: int, scene_id: str = ""):
        self.video = video.resolve()
        self.capture = cv2.VideoCapture(str(self.video))
        if not self.capture.isOpened():
            raise ValueError(f"cannot open video: {self.video}")
        self.frame_count = int(self.capture.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = float(self.capture.get(cv2.CAP_PROP_FPS))
        self.frame_index = max(0, start_frame)
        self.stride = max(1, stride)
        self.scale = max(2, display_scale)
        self.writer = DatasetWriter(output, video, split, scene_id)
        self.window = "FPGA ROI Dataset Tool"
        self.frame_bgr: np.ndarray | None = None
        self.analysis_gray: np.ndarray | None = None
        self.drag_start: tuple[int, int] | None = None
        self.drag_current: tuple[int, int] | None = None
        self.selected_box: tuple[int, int, int, int] | None = None
        self.message = "drag on left analysis view; P=ped, V=vehicle"
        self.message_color = (80, 220, 80)

    def _analysis_point(self, x: int, y: int) -> tuple[int, int] | None:
        if self.analysis_gray is None:
            return None
        display_width = self.analysis_gray.shape[1] * self.scale
        display_height = self.analysis_gray.shape[0] * self.scale
        if not (0 <= x < display_width and 0 <= y < display_height):
            return None
        return min(x // self.scale, self.analysis_gray.shape[1] - 1), \
            min(y // self.scale, self.analysis_gray.shape[0] - 1)

    def _mouse(self, event: int, x: int, y: int, _flags: int, _param: object) -> None:
        point = self._analysis_point(x, y)
        if event == cv2.EVENT_RBUTTONDOWN:
            self.drag_start = None
            self.drag_current = None
            self.selected_box = None
            self.message = "selection cleared"
        elif event == cv2.EVENT_LBUTTONDOWN and point is not None:
            self.drag_start = point
            self.drag_current = point
            self.selected_box = None
        elif event == cv2.EVENT_MOUSEMOVE and self.drag_start is not None and point is not None:
            self.drag_current = point
        elif event == cv2.EVENT_LBUTTONUP and self.drag_start is not None:
            if point is not None and self.analysis_gray is not None:
                self.selected_box = normalize_box(
                    self.drag_start, point,
                    self.analysis_gray.shape[1], self.analysis_gray.shape[0]
                )
                self.message = f"selected {self.selected_box}; press P or V"
            self.drag_start = None
            self.drag_current = None

    def _load_frame(self) -> bool:
        if self.frame_index < 0 or (self.frame_count > 0 and
                                    self.frame_index >= self.frame_count):
            return False
        self.capture.set(cv2.CAP_PROP_POS_FRAMES, self.frame_index)
        ok, frame = self.capture.read()
        if not ok:
            return False
        self.frame_bgr = frame
        self.analysis_gray = fpga_analysis_frame(frame)
        self.selected_box = None
        self.drag_start = None
        self.drag_current = None
        if frame.shape[1] != 1280 or frame.shape[0] != 720:
            self.message = (f"warning: source is {frame.shape[1]}x{frame.shape[0]}, "
                            f"analysis is {self.analysis_gray.shape[1]}x{self.analysis_gray.shape[0]}")
            self.message_color = (0, 180, 255)
        return True

    def _draw_box(self, image: np.ndarray, box: tuple[int, int, int, int],
                  offset_x: int, color: tuple[int, int, int]) -> None:
        xmin, ymin, xmax, ymax = box
        p0 = (offset_x + xmin * self.scale, ymin * self.scale)
        p1 = (offset_x + (xmax + 1) * self.scale - 1,
              (ymax + 1) * self.scale - 1)
        cv2.rectangle(image, p0, p1, color, 2)

    def _render(self) -> np.ndarray:
        assert self.frame_bgr is not None and self.analysis_gray is not None
        view_width = self.analysis_gray.shape[1] * self.scale
        view_height = self.analysis_gray.shape[0] * self.scale
        analysis_view = cv2.cvtColor(
            cv2.resize(self.analysis_gray, (view_width, view_height),
                       interpolation=cv2.INTER_NEAREST), cv2.COLOR_GRAY2BGR
        )
        source_view = cv2.resize(self.frame_bgr, (view_width, view_height),
                                 interpolation=cv2.INTER_AREA)
        canvas = np.zeros((view_height + 92, view_width * 2, 3), dtype=np.uint8)
        canvas[:view_height, :view_width] = analysis_view
        canvas[:view_height, view_width:] = source_view
        cv2.putText(canvas, "FPGA analysis 256x144", (10, 24),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 255), 2)
        cv2.putText(canvas, "source video", (view_width + 10, 24),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 255), 2)

        active_box = self.selected_box
        if self.drag_start is not None and self.drag_current is not None:
            active_box = normalize_box(self.drag_start, self.drag_current,
                                       self.analysis_gray.shape[1],
                                       self.analysis_gray.shape[0])
        if active_box is not None:
            self._draw_box(canvas, active_box, 0, (0, 255, 0))
            self._draw_box(canvas, active_box, view_width, (0, 255, 0))

        status = (f"frame {self.frame_index}/{max(0, self.frame_count - 1)}  "
                  f"split={self.writer.split}  stride={self.stride}  "
                  f"saved_total={len(self.writer.rows)}")
        controls = "P pedestrian | V vehicle | I invalid | N/Space next | B previous | +/- stride | U undo | Q quit"
        cv2.putText(canvas, status, (10, view_height + 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.62, (230, 230, 230), 1)
        cv2.putText(canvas, controls, (10, view_height + 52),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.52, (190, 190, 190), 1)
        cv2.putText(canvas, self.message[:150], (10, view_height + 78),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.52, self.message_color, 1)
        return canvas

    def _save_selected(self, label: str) -> None:
        if self.selected_box is None or self.analysis_gray is None or self.frame_bgr is None:
            self.message = "draw a box first"
            self.message_color = (0, 0, 255)
            return
        result = self.writer.save(
            self.analysis_gray, self.frame_index, self.fps,
            (self.frame_bgr.shape[1], self.frame_bgr.shape[0]),
            self.selected_box, label,
        )
        self.message = result.message
        self.message_color = (80, 220, 80) if result.saved else (0, 180, 255)
        if result.saved:
            self.selected_box = None

    def run(self) -> int:
        cv2.namedWindow(self.window, cv2.WINDOW_NORMAL)
        cv2.setMouseCallback(self.window, self._mouse)
        if not self._load_frame():
            raise ValueError("cannot read the requested start frame")
        try:
            while True:
                cv2.imshow(self.window, self._render())
                key = cv2.waitKeyEx(20)
                if key < 0:
                    continue
                low = key & 0xFF
                if low in (ord("q"), 27):
                    break
                if low == ord("p"):
                    self._save_selected("ped")
                elif low == ord("v"):
                    self._save_selected("vehicle")
                elif low == ord("i"):
                    self._save_selected("invalid")
                elif low == ord("u"):
                    result = self.writer.undo()
                    self.message = result.message
                    self.message_color = (80, 220, 80) if result.saved else (0, 180, 255)
                elif low in (ord("n"), ord(" ")) or key == 2555904:
                    self.frame_index += self.stride
                    if not self._load_frame():
                        self.frame_index -= self.stride
                        self.message = "end of video"
                elif low == ord("b") or key == 2424832:
                    self.frame_index = max(0, self.frame_index - self.stride)
                    self._load_frame()
                elif low in (ord("+"), ord("=")):
                    self.stride = min(1000, self.stride + 1)
                    self.message = f"stride={self.stride}"
                elif low in (ord("-"), ord("_")):
                    self.stride = max(1, self.stride - 1)
                    self.message = f"stride={self.stride}"
                elif low == ord("c"):
                    self.selected_box = None
                    self.message = "selection cleared"
        finally:
            self.capture.release()
            cv2.destroyAllWindows()
        return 0


def self_test() -> int:
    frame = np.zeros((720, 1280, 3), dtype=np.uint8)
    for y in range(10):
        for x in range(20):
            frame[y, x] = (x + 2, y + 4, x + y + 8)
    analysis = fpga_analysis_frame(frame)
    assert analysis.shape == (144, 256)
    expected = fpga_gray_bgr(frame)
    assert np.array_equal(analysis, expected[::5, ::5])

    crop = np.asarray([[10, 20], [30, 40]], dtype=np.uint8)
    roi = fpga_resize_roi(crop)
    assert roi.shape == (32, 32)
    assert roi[0, 0] == 10 and roi[-1, -1] == 40

    with tempfile.TemporaryDirectory(prefix="roi_dataset_tool_") as directory:
        root = Path(directory)
        fake_video = root / "source.mp4"
        fake_video.touch()
        writer = DatasetWriter(root / "dataset", fake_video, "train")
        result = writer.save(np.tile(np.arange(40, dtype=np.uint8), (20, 1)),
                             12, 30.0, (200, 100), (3, 4, 14, 16), "ped")
        assert result.saved and len(writer.rows) == 1
        duplicate = writer.save(np.tile(np.arange(40, dtype=np.uint8), (20, 1)),
                                12, 30.0, (200, 100), (3, 4, 14, 16), "ped")
        assert not duplicate.saved
        conflicting = writer.save(np.tile(np.arange(40, dtype=np.uint8), (20, 1)),
                                  12, 30.0, (200, 100), (3, 4, 14, 16), "vehicle")
        assert not conflicting.saved
        split_guarded = False
        try:
            DatasetWriter(root / "dataset", fake_video, "test")
        except ValueError:
            split_guarded = True
        assert split_guarded
        undone = writer.undo()
        assert undone.saved and len(writer.rows) == 0
    print("PASS: FPGA downsample, DDA resize, save, duplicate/split guards and undo")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--split", choices=("train", "val", "test"))
    parser.add_argument("--scene-id", help="shared capture group, including all clips and derivatives")
    parser.add_argument("--stride", type=int, default=10,
                        help="frames advanced by N/Space; default 10")
    parser.add_argument("--start-frame", type=int, default=0)
    parser.add_argument("--display-scale", type=int, default=3)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        return self_test()
    if args.video is None or args.output is None or args.split is None:
        parser.error("--video, --output and --split are required unless --self-test is used")
    if not args.scene_id:
        parser.error("--scene-id is required: clips from the same capture must stay together")
    return AnnotationApp(args.video, args.output, args.split, args.stride,
                         args.start_frame, args.display_scale, args.scene_id).run()


if __name__ == "__main__":
    raise SystemExit(main())
