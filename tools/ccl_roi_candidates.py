"""Export actual RTL CCL crops for human review; never use geometry class as truth."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from pathlib import Path
import cv2
import numpy as np
from roi_dataset_tool import fpga_resize_roi, DatasetWriter


def render_contact_sheets(output: Path, records: list[dict], per_sheet: int = 40) -> list[dict]:
    """Render nearest-neighbor ROI sheets for human semantic review."""
    receipts = []
    columns, tile_width, tile_height = 5, 150, 130
    for page, start in enumerate(range(0, len(records), per_sheet), 1):
        page_records = records[start:start + per_sheet]
        rows = (len(page_records) + columns - 1) // columns
        sheet = np.full((rows * tile_height, columns * tile_width, 3), 245, np.uint8)
        for index, record in enumerate(page_records):
            roi = cv2.imread(str(output / record["roi_path"]), cv2.IMREAD_GRAYSCALE)
            if roi is None or roi.shape != (32, 32):
                raise ValueError(f"invalid exported ROI: {record['roi_path']}")
            preview = cv2.cvtColor(
                cv2.resize(roi, (96, 96), interpolation=cv2.INTER_NEAREST), cv2.COLOR_GRAY2BGR)
            top = (index // columns) * tile_height
            left = (index % columns) * tile_width
            sheet[top:top + 96, left:left + 96] = preview
            cv2.putText(sheet, record["candidate_id"], (left, top + 110),
                        cv2.FONT_HERSHEY_SIMPLEX, .32, (20, 20, 20), 1, cv2.LINE_AA)
            cv2.putText(sheet, f"source={record['source_frame']}", (left, top + 124),
                        cv2.FONT_HERSHEY_SIMPLEX, .32, (20, 20, 20), 1, cv2.LINE_AA)
        path = output / f"contact_sheet_{page:02d}.jpg"
        if not cv2.imwrite(str(path), sheet, [cv2.IMWRITE_JPEG_QUALITY, 95]):
            raise OSError(f"could not write {path}")
        receipts.append({"path": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                         "first_candidate_index": start,
                         "candidate_count": len(page_records)})
    return receipts


def render_frame_overlays(output: Path, records: list[dict], images: dict[int, np.ndarray],
                          per_sheet: int = 12) -> list[dict]:
    """Render analysis frames with every RTL candidate box and slot identity."""
    by_frame: dict[int, list[dict]] = {}
    for record in records:
        by_frame.setdefault(int(record["replay_frame"]), []).append(record)
    frames = sorted(by_frame)
    receipts = []
    columns, tile_width, tile_height = 3, 512, 320
    colors = [(0, 220, 0), (255, 120, 0), (0, 120, 255), (220, 0, 220)]
    for page, start in enumerate(range(0, len(frames), per_sheet), 1):
        page_frames = frames[start:start + per_sheet]
        rows = (len(page_frames) + columns - 1) // columns
        sheet = np.full((rows * tile_height, columns * tile_width, 3), 245, np.uint8)
        for index, frame in enumerate(page_frames):
            view = cv2.cvtColor(cv2.resize(images[frame], (512, 288),
                                           interpolation=cv2.INTER_NEAREST), cv2.COLOR_GRAY2BGR)
            for record in by_frame[frame]:
                slot = int(record["candidate_id"].rsplit("slot", 1)[1])
                x0, y0, x1, y1 = (int(record[key]) for key in ("xmin", "ymin", "xmax", "ymax"))
                color = colors[slot % len(colors)]
                cv2.rectangle(view, (2 * x0, 2 * y0), (2 * x1 + 1, 2 * y1 + 1), color, 2)
                cv2.putText(view, f"s{slot}", (2 * x0, max(10, 2 * y0 - 3)),
                            cv2.FONT_HERSHEY_SIMPLEX, .4, color, 1, cv2.LINE_AA)
            top = (index // columns) * tile_height
            left = (index % columns) * tile_width
            sheet[top:top + 288, left:left + 512] = view
            source_frame = by_frame[frame][0]["source_frame"]
            cv2.putText(sheet, f"replay={frame} source={source_frame}", (left + 4, top + 309),
                        cv2.FONT_HERSHEY_SIMPLEX, .5, (20, 20, 20), 1, cv2.LINE_AA)
        path = output / f"frame_overlay_{page:02d}.jpg"
        if not cv2.imwrite(str(path), sheet, [cv2.IMWRITE_JPEG_QUALITY, 95]):
            raise OSError(f"could not write {path}")
        receipts.append({"path": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                         "first_replay_frame": page_frames[0], "frame_count": len(page_frames)})
    return receipts


def render_source_overlays(output: Path, records: list[dict], source: Path,
                           per_sheet: int = 12) -> list[dict]:
    """Render decoded 1280x720 source frames with sampled-cell candidate extents."""
    by_frame: dict[int, list[dict]] = {}
    for record in records:
        by_frame.setdefault(int(record["source_frame"]), []).append(record)
    frames = sorted(by_frame)
    capture = cv2.VideoCapture(str(source))
    if not capture.isOpened():
        raise ValueError(f"cannot open source video for overlays: {source}")
    receipts = []
    colors = [(0, 220, 0), (255, 120, 0), (0, 120, 255), (220, 0, 220)]
    columns, tile_width, tile_height = 3, 640, 390
    try:
        for page, start in enumerate(range(0, len(frames), per_sheet), 1):
            page_frames = frames[start:start + per_sheet]
            rows = (len(page_frames) + columns - 1) // columns
            sheet = np.full((rows * tile_height, columns * tile_width, 3), 245, np.uint8)
            for index, frame_index in enumerate(page_frames):
                capture.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
                ok, frame = capture.read()
                if not ok or frame.shape[:2] != (720, 1280):
                    raise ValueError(f"cannot decode source frame {frame_index}")
                for record in by_frame[frame_index]:
                    slot = int(record["candidate_id"].rsplit("slot", 1)[1])
                    x0, y0, x1, y1 = (int(record[key]) for key in
                                      ("xmin", "ymin", "xmax", "ymax"))
                    color = colors[slot % len(colors)]
                    cv2.rectangle(frame, (5 * x0, 5 * y0),
                                  (min(1279, 5 * x1 + 4), min(719, 5 * y1 + 4)), color, 4)
                    cv2.putText(frame, f"s{slot}", (5 * x0, max(18, 5 * y0 - 6)),
                                cv2.FONT_HERSHEY_SIMPLEX, .7, color, 2, cv2.LINE_AA)
                view = cv2.resize(frame, (640, 360), interpolation=cv2.INTER_AREA)
                top = (index // columns) * tile_height
                left = (index % columns) * tile_width
                sheet[top:top + 360, left:left + 640] = view
                cv2.putText(sheet, f"source={frame_index}", (left + 4, top + 382),
                            cv2.FONT_HERSHEY_SIMPLEX, .5, (20, 20, 20), 1, cv2.LINE_AA)
            path = output / f"source_overlay_{page:02d}.jpg"
            if not cv2.imwrite(str(path), sheet, [cv2.IMWRITE_JPEG_QUALITY, 95]):
                raise OSError(f"could not write {path}")
            receipts.append({"path": path.name,
                             "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                             "first_source_frame": page_frames[0], "frame_count": len(page_frames)})
    finally:
        capture.release()
    return receipts


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frames", type=Path, required=True)
    parser.add_argument("--objects", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--scene-id", required=True)
    parser.add_argument("--split", choices=["train", "val", "test"], required=True)
    parser.add_argument("--reviewed", type=Path, help="CSV copied from candidates.csv, with label/reviewer completed")
    parser.add_argument("--dataset", type=Path)
    parser.add_argument("--source-overlays", action="store_true",
                        help="also decode source video frames for full-resolution review sheets")
    args = parser.parse_args()
    manifest = json.loads((args.frames / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("preprocessing") != "rtl_shift_gray_stride5_v1":
        raise ValueError("replay used a different preprocessing path; regenerate frames")
    source = Path(manifest["source"])
    if hashlib.sha256(source.read_bytes()).hexdigest() != manifest["source_sha256"]:
        raise ValueError("source video changed")
    frame_map = {r["replay_frame"]: r["source_frame"] for r in manifest["frame_map"]}
    with args.objects.open(encoding="utf-8-sig", newline="") as handle:
        objects = list(csv.DictReader(handle))
    records = []
    images = {}
    for row in objects:
        if row["valid"] != "1":
            continue
        frame = int(row["frame"])
        if frame not in images:
            images[frame] = np.loadtxt(args.frames / f"frame_{frame:04d}.hex",
                                      dtype=np.uint8, converters=lambda v: int(v, 16)).reshape(144, 256)
        box = tuple(int(row[k]) for k in ("xmin", "ymin", "xmax", "ymax"))
        x0, y0, x1, y1 = box
        if not (0 <= x0 <= x1 < 256 and 0 <= y0 <= y1 < 144):
            raise ValueError("RTL produced out-of-bounds box")
        roi = fpga_resize_roi(images[frame][y0:y1+1, x0:x1+1])
        token = f"f{frame:05d}_slot{row['slot']}"
        records.append(dict(candidate_id=token, replay_frame=frame, source_frame=frame_map[frame],
                            xmin=x0, ymin=y0, xmax=x1, ymax=y1, geometry_class=row["class"],
                            label="", reviewer="", roi_path=f"{token}.png",
                            roi_sha256=hashlib.sha256(roi.tobytes()).hexdigest()))
        if not args.reviewed:
            args.output.mkdir(parents=True, exist_ok=True)
            if not cv2.imwrite(str(args.output / f"{token}.png"), roi):
                raise OSError("could not write candidate ROI")
    if args.reviewed:
        if not args.dataset:
            parser.error("--dataset required with --reviewed")
        originals = {r["candidate_id"]: r for r in records}
        imported = 0
        with args.reviewed.open(encoding="utf-8-sig", newline="") as handle:
            reviewed = list(csv.DictReader(handle))
        # Validate all decisions before saving any of them.
        for row in reviewed:
            original = originals[row["candidate_id"]]
            for key in original:
                if key not in {"label", "reviewer"} and str(original[key]) != row[key]:
                    raise ValueError(f"candidate metadata changed: {key}")
            if row["label"] and (row["label"] not in {"ped", "vehicle", "invalid"} or not row["reviewer"].strip()):
                raise ValueError("each reviewed sample needs an explicit valid label and reviewer")
        writer = DatasetWriter(args.dataset, source, args.split, args.scene_id, "ccl")
        for row in reviewed:
            if not row["label"]:
                continue
            writer.reviewer = row["reviewer"]
            result = writer.save(images[int(row["replay_frame"])], int(row["source_frame"]),
                                 manifest["source_fps"], (1280, 720),
                                 tuple(int(row[k]) for k in ("xmin", "ymin", "xmax", "ymax")), row["label"])
            imported += int(result.saved)
        print(f"Imported {imported} reviewed CCL samples")
    else:
        args.output.mkdir(parents=True, exist_ok=True)
        fields = ["candidate_id", "replay_frame", "source_frame", "xmin", "ymin", "xmax", "ymax",
                  "geometry_class", "label", "reviewer", "roi_path", "roi_sha256"]
        with (args.output / "candidates.csv").open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fields)
            writer.writeheader()
            writer.writerows(records)
        contact_sheets = render_contact_sheets(args.output, records)
        frame_overlays = render_frame_overlays(args.output, records, images)
        source_overlays = render_source_overlays(args.output, records, source) if args.source_overlays else []
        (args.output / "provenance.json").write_text(json.dumps({
            "source": str(source), "source_sha256": manifest["source_sha256"],
            "scene_id": args.scene_id, "split": args.split,
            "objects_sha256": hashlib.sha256(args.objects.read_bytes()).hexdigest(),
            "status": "unlabeled; geometry_class is not ground truth", "count": len(records),
            "contact_sheets": contact_sheets,
            "frame_overlays": frame_overlays,
            "source_overlays": source_overlays,
        }, indent=2), encoding="utf-8")
        print(f"Exported {len(records)} unlabelled CCL candidates")


if __name__ == "__main__":
    main()
