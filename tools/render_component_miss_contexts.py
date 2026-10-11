#!/usr/bin/env python3
"""Render source and analysis-mask context for selected missed target frames."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path

import cv2
import numpy as np

from candidate_chain_reference import CandidateChainReference
from candidate_resolution_sweep import source_extent_box
from select_candidate_windows import inclusive_iou


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def context_box(box: tuple[int, int, int, int], frame_width: int, frame_height: int,
                minimum_width: int = 320, minimum_height: int = 240) -> tuple[int, int, int, int]:
    x0, y0, x1, y1 = box
    center_x, center_y = (x0 + x1) // 2, (y0 + y1) // 2
    left = max(0, min(center_x - minimum_width // 2, frame_width - minimum_width))
    top = max(0, min(center_y - minimum_height // 2, frame_height - minimum_height))
    return left, top, min(frame_width - 1, left + minimum_width - 1), \
        min(frame_height - 1, top + minimum_height - 1)


def draw_shifted(image: np.ndarray, box: tuple[int, int, int, int],
                 crop: tuple[int, int, int, int], color: tuple[int, int, int],
                 thickness: int = 2) -> None:
    left, top, _, _ = crop
    x0, y0, x1, y1 = box
    cv2.rectangle(image, (x0 - left, y0 - top), (x1 - left, y1 - top), color, thickness)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video", type=Path, required=True)
    parser.add_argument("--annotations", type=Path, required=True)
    parser.add_argument("--clip-id", required=True)
    parser.add_argument("--target-label", choices=("ped", "vehicle"), required=True)
    parser.add_argument("--frames", type=int, nargs="+", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    target_frames = sorted(set(args.frames))
    if not target_frames or target_frames[0] < 0:
        raise ValueError("frames must be nonnegative")

    annotations: dict[int, list[dict[str, str]]] = defaultdict(list)
    with args.annotations.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            if (row["clip_id"] == args.clip_id and row["label"] == args.target_label and
                    int(row["frame_index"]) in target_frames):
                annotations[int(row["frame_index"])].append(row)
    missing = [frame for frame in target_frames if not annotations.get(frame)]
    if missing:
        raise ValueError(f"no target annotation at selected frames: {missing}")

    capture = cv2.VideoCapture(str(args.video))
    if not capture.isOpened():
        raise ValueError(f"cannot open {args.video}")
    frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    chain = CandidateChainReference()
    args.output.mkdir(parents=True, exist_ok=True)
    entries = []
    try:
        for frame_index in range(target_frames[-1] + 1):
            ok, frame = capture.read()
            if not ok:
                raise ValueError(f"video ended before frame {frame_index}")
            result = chain.process_bgr(frame, frame_index)
            if frame_index not in annotations:
                continue
            mask = (result["run_filtered_mask"] != 0).astype(np.uint8)
            count, labels, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
            components = []
            for label in range(1, count):
                x, y, width, height, area = (int(value) for value in stats[label])
                components.append({"label": label, "area": area, "xmin": x, "ymin": y,
                                   "xmax": x + width - 1, "ymax": y + height - 1})
            components.sort(key=lambda item: (-item["area"], item["label"]))
            source_boxes = [source_extent_box(item, 5) for item in components]
            for target_index, annotation in enumerate(annotations[frame_index]):
                target_box = tuple(int(annotation[field]) for field in
                                   ("xmin", "ymin", "xmax", "ymax"))
                ious = [inclusive_iou(box, target_box) for box in source_boxes]
                best_index = int(np.argmax(ious)) if ious else None
                crop_box = context_box(target_box, frame_width, frame_height)
                left, top, right, bottom = crop_box
                source = frame[top:bottom + 1, left:right + 1].copy()
                draw_shifted(source, target_box, crop_box, (0, 0, 255), 3)
                for index, box in enumerate(source_boxes[:4]):
                    draw_shifted(source, box, crop_box, (0, 255, 0), 2)
                    cv2.putText(source, f"top{index + 1}",
                                (box[0] - left, max(12, box[1] - top - 3)),
                                cv2.FONT_HERSHEY_SIMPLEX, .4, (0, 255, 0), 1, cv2.LINE_AA)
                if best_index is not None:
                    draw_shifted(source, source_boxes[best_index], crop_box, (255, 255, 0), 2)
                cv2.putText(source, f"frame={frame_index} red=GT green=top4 cyan=best",
                            (5, 18), cv2.FONT_HERSHEY_SIMPLEX, .45, (255, 255, 255),
                            2, cv2.LINE_AA)

                analysis = cv2.cvtColor(result["gray"], cv2.COLOR_GRAY2BGR)
                analysis[mask != 0] = (0, 0, 255)
                for index, item in enumerate(components):
                    color = (0, 255, 0) if index < 4 else (120, 120, 120)
                    cv2.rectangle(analysis, (item["xmin"], item["ymin"]),
                                  (item["xmax"], item["ymax"]), color, 1)
                if best_index is not None:
                    best = components[best_index]
                    cv2.rectangle(analysis, (best["xmin"], best["ymin"]),
                                  (best["xmax"], best["ymax"]), (255, 255, 0), 2)
                ax0, ay0, ax1, ay1 = (value // 5 for value in target_box)
                cv2.rectangle(analysis, (ax0, ay0), (ax1, ay1), (0, 255, 255), 1)
                analysis = cv2.resize(analysis, (640, 360), interpolation=cv2.INTER_NEAREST)
                source = cv2.resize(source, (640, 480), interpolation=cv2.INTER_CUBIC)
                canvas = np.full((880, 640, 3), 245, np.uint8)
                canvas[:480] = source
                canvas[500:860] = analysis
                best = components[best_index] if best_index is not None else None
                summary = ("best: none" if best is None else
                           f"best rank={best_index + 1} area={best['area']} "
                           f"iou={ious[best_index]:.4f} box="
                           f"({best['xmin']},{best['ymin']},{best['xmax']},{best['ymax']})")
                cv2.putText(canvas, summary, (8, 876), cv2.FONT_HERSHEY_SIMPLEX,
                            .45, (0, 0, 0), 1, cv2.LINE_AA)
                name = f"f{frame_index:05d}_target{target_index}.png"
                path = args.output / name
                if not cv2.imwrite(str(path), canvas):
                    raise OSError(f"could not write {path}")
                entries.append({
                    "frame_index": frame_index,
                    "object_id": annotation["object_id"],
                    "target_box_source_inclusive": list(target_box),
                    "component_count": len(components),
                    "best_component_rank": best_index + 1 if best_index is not None else None,
                    "best_component_area": best["area"] if best else None,
                    "best_component_iou": ious[best_index] if best_index is not None else None,
                    "best_component_analysis_box": ([best[key] for key in
                        ("xmin", "ymin", "xmax", "ymax")] if best else None),
                    "image": name,
                    "image_sha256": digest(path),
                })
    finally:
        capture.release()

    receipt = {
        "status": "component_miss_visual_diagnostic_not_training_or_acceptance_evidence",
        "clip_id": args.clip_id,
        "target_label": args.target_label,
        "selected_frames": target_frames,
        "video_sha256": digest(args.video),
        "annotations_sha256": digest(args.annotations),
        "script_sha256": digest(Path(__file__)),
        "entries": entries,
        "legend": "source red=annotation, green=area top4, cyan=best IoU; analysis red pixels=run mask, yellow=annotation",
    }
    (args.output / "index.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": receipt["status"], "entry_count": len(entries)},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
