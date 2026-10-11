"""Render a deterministic contact sheet for prepared boxes and FPGA-style ROIs."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path

import cv2
import numpy as np

from roi_dataset_tool import fpga_analysis_frame, fpga_resize_roi


def evenly_spaced(values: list[int], count: int) -> list[int]:
    if len(values) <= count:
        return values
    indices = np.linspace(0, len(values) - 1, count, dtype=int)
    return [values[index] for index in indices]


def analysis_box(row: dict[str, str]) -> tuple[int, int, int, int]:
    return (math.ceil(int(row["xmin"]) / 5), math.ceil(int(row["ymin"]) / 5),
            int(row["xmax"]) // 5, int(row["ymax"]) // 5)


def render(prepared: Path, output: Path, frame_count: int = 8) -> dict[str, object]:
    if output.exists():
        raise ValueError("use a new output directory")
    receipt_path = prepared / "provenance.json"
    annotations_path = prepared / "annotations_720p.csv"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    with annotations_path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    rows_by_frame: dict[int, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        if row["label"] != "ignore":
            rows_by_frame[int(row["frame_index"])].append(row)
    selected = evenly_spaced(sorted(rows_by_frame), frame_count)
    if not selected:
        raise ValueError("no reviewable annotations")
    videos = list(prepared.glob("*.avi"))
    if len(videos) != 1:
        raise ValueError("expected one prepared AVI")
    if hashlib.sha256(videos[0].read_bytes()).hexdigest() != receipt["output_sha256"]:
        raise ValueError("prepared video changed")

    tile_width, tile_height = 640, 500
    columns = 2
    canvas = np.full((math.ceil(len(selected) / columns) * tile_height,
                      columns * tile_width, 3), 245, np.uint8)
    cap = cv2.VideoCapture(str(videos[0]))
    review_rows = []
    try:
        for tile_index, source_frame in enumerate(selected):
            cap.set(cv2.CAP_PROP_POS_FRAMES, source_frame)
            ok, frame = cap.read()
            if not ok:
                raise ValueError(f"could not decode frame {source_frame}")
            marked = frame.copy()
            colors = {"ped": (0, 220, 0), "vehicle": (255, 120, 0), "invalid": (0, 0, 255)}
            for row in rows_by_frame[source_frame]:
                box = tuple(int(row[key]) for key in ("xmin", "ymin", "xmax", "ymax"))
                cv2.rectangle(marked, box[:2], box[2:], colors[row["label"]], 3)
                cv2.putText(marked, row["label"], (box[0], max(20, box[1] - 5)),
                            cv2.FONT_HERSHEY_SIMPLEX, .65, colors[row["label"]], 2, cv2.LINE_AA)
            preview = cv2.resize(marked, (640, 360), interpolation=cv2.INTER_AREA)
            tile = np.full((tile_height, tile_width, 3), 245, np.uint8)
            tile[:360] = preview
            cv2.putText(tile, f"frame {source_frame} | boxes {len(rows_by_frame[source_frame])}",
                        (8, 386), cv2.FONT_HERSHEY_SIMPLEX, .65, (20, 20, 20), 2, cv2.LINE_AA)
            analysis = fpga_analysis_frame(frame)
            for roi_index, row in enumerate(rows_by_frame[source_frame][:4]):
                x0, y0, x1, y1 = analysis_box(row)
                if not (0 <= x0 <= x1 < 256 and 0 <= y0 <= y1 < 144):
                    raise ValueError(f"box becomes empty/outside analysis frame at frame {source_frame}")
                roi = fpga_resize_roi(analysis[y0:y1 + 1, x0:x1 + 1])
                enlarged = cv2.resize(roi, (96, 96), interpolation=cv2.INTER_NEAREST)
                enlarged = cv2.cvtColor(enlarged, cv2.COLOR_GRAY2BGR)
                x_position = 8 + roi_index * 154
                tile[398:494, x_position:x_position + 96] = enlarged
                cv2.putText(tile, row["label"], (x_position + 99, 445),
                            cv2.FONT_HERSHEY_SIMPLEX, .4, (20, 20, 20), 1, cv2.LINE_AA)
                review_rows.append({"frame_index": source_frame, "object_id": row["object_id"],
                                    "label": row["label"], "analysis_box": [x0, y0, x1, y1],
                                    "roi_sha256": hashlib.sha256(roi.tobytes()).hexdigest()})
            top = (tile_index // columns) * tile_height
            left = (tile_index % columns) * tile_width
            canvas[top:top + tile_height, left:left + tile_width] = tile
    finally:
        cap.release()
    output.mkdir(parents=True)
    sheet_path = output / "contact_sheet.jpg"
    if not cv2.imwrite(str(sheet_path), canvas, [cv2.IMWRITE_JPEG_QUALITY, 94]):
        raise RuntimeError("failed to write contact sheet")
    report = {
        "dataset": receipt["dataset"], "sequence_id": receipt["sequence_id"],
        "scene_id": receipt["scene_id"], "selected_frames": selected,
        "reviewed_boxes": review_rows,
        "prepared_video_sha256": receipt["output_sha256"],
        "annotations_sha256": hashlib.sha256(annotations_path.read_bytes()).hexdigest(),
        "contact_sheet_sha256": hashlib.sha256(sheet_path.read_bytes()).hexdigest(),
        "review_status": "pending_human_visual_check",
        "checklist": ["frame content and box alignment", "letterbox geometry",
                      "32x32 FPGA-style ROI content and class label"],
    }
    (output / "review.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepared", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True, help="new directory")
    parser.add_argument("--frames", type=int, default=8)
    args = parser.parse_args()
    if args.frames < 1:
        raise ValueError("--frames must be positive")
    result = render(args.prepared, args.output, args.frames)
    print(json.dumps({"selected_frames": result["selected_frames"],
                      "review_status": result["review_status"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
