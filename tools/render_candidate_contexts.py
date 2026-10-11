#!/usr/bin/env python3
"""Render traceable full-resolution context crops for CCL candidate review."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import tempfile
from pathlib import Path

import cv2
import numpy as np


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def candidate_table(path: Path) -> tuple[Path, Path | None, dict[str, object] | None,
                                         Path | None, dict[str, object] | None]:
    """Resolve either a candidate directory or candidates.csv."""
    path = path.resolve()
    if path.is_dir():
        csv_path = path / "candidates.csv"
        provenance_path = path / "provenance.json"
        report_path = path / "report.json"
    else:
        csv_path = path
        provenance_path = path.parent / "provenance.json"
        report_path = path.parent / "report.json"
    if not csv_path.is_file():
        raise ValueError(f"candidate table not found: {csv_path}")
    provenance = (json.loads(provenance_path.read_text(encoding="utf-8"))
                  if provenance_path.is_file() else None)
    report = (json.loads(report_path.read_text(encoding="utf-8"))
              if report_path.is_file() else None)
    return (csv_path, provenance_path if provenance is not None else None, provenance,
            report_path if report is not None else None, report)


def load_frame_map(path: Path | None) -> tuple[dict[int, int], dict[str, object] | None]:
    if path is None:
        return {}, None
    path = path.resolve()
    if path.is_dir():
        path = path / "manifest.json"
    if not path.is_file():
        raise ValueError(f"frame map not found: {path}")
    if path.suffix.lower() == ".json":
        document = json.loads(path.read_text(encoding="utf-8"))
        rows = document.get("frame_map")
        if not isinstance(rows, list):
            raise ValueError("JSON frame map must contain a frame_map list")
    else:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
    mapping: dict[int, int] = {}
    for row in rows:
        replay, source = int(row["replay_frame"]), int(row["source_frame"])
        if replay in mapping and mapping[replay] != source:
            raise ValueError(f"conflicting source mapping for replay frame {replay}")
        mapping[replay] = source
    return mapping, {"path": str(path), "sha256": digest(path), "count": len(mapping)}


def source_box(row: dict[str, str], source_width: int, source_height: int,
               sample_stride: int) -> tuple[int, int, int, int]:
    if all(row.get(key, "") != "" for key in ("xmin", "ymin", "xmax", "ymax")):
        x0, y0, x1, y1 = (int(row[key]) for key in ("xmin", "ymin", "xmax", "ymax"))
    elif row.get("selected_analysis_box", ""):
        values = json.loads(row["selected_analysis_box"])
        if not isinstance(values, list) or len(values) != 4:
            raise ValueError("selected_analysis_box must be a four-element JSON list")
        x0, y0, x1, y1 = (int(value) for value in values)
    else:
        raise ValueError("candidate row has no supported analysis bbox")
    if not (0 <= x0 <= x1 and 0 <= y0 <= y1):
        raise ValueError(f"invalid analysis bbox for {row.get('candidate_id', '<unknown>')}")
    result = (sample_stride * x0, sample_stride * y0,
              min(source_width - 1, sample_stride * x1 + sample_stride - 1),
              min(source_height - 1, sample_stride * y1 + sample_stride - 1))
    if result[0] >= source_width or result[1] >= source_height:
        raise ValueError(f"analysis bbox outside source frame for {row.get('candidate_id', '<unknown>')}")
    return result


def analysis_box(row: dict[str, str]) -> tuple[int, int, int, int]:
    """Read either the replay-candidate or fixed-budget bbox schema."""
    if all(row.get(key, "") != "" for key in ("xmin", "ymin", "xmax", "ymax")):
        return tuple(int(row[key]) for key in ("xmin", "ymin", "xmax", "ymax"))
    values = json.loads(row.get("selected_analysis_box", ""))
    if not isinstance(values, list) or len(values) != 4:
        raise ValueError("selected_analysis_box must be a four-element JSON list")
    return tuple(int(value) for value in values)


def safe_stem(candidate_id: str) -> str:
    """Map a traceable candidate id to a Windows-safe filename stem."""
    return "".join(character if character.isalnum() or character in "._-" else "_"
                   for character in candidate_id)


def context_box(box: tuple[int, int, int, int], frame_width: int, frame_height: int,
                context_scale: float, min_width: int, min_height: int) -> tuple[int, int, int, int]:
    x0, y0, x1, y1 = box
    box_width, box_height = x1 - x0 + 1, y1 - y0 + 1
    wanted_width = min(frame_width, max(min_width, int(np.ceil(box_width * context_scale))))
    wanted_height = min(frame_height, max(min_height, int(np.ceil(box_height * context_scale))))
    center_x, center_y = (x0 + x1) // 2, (y0 + y1) // 2
    left = max(0, min(center_x - wanted_width // 2, frame_width - wanted_width))
    top = max(0, min(center_y - wanted_height // 2, frame_height - wanted_height))
    return left, top, left + wanted_width - 1, top + wanted_height - 1


def select_rows(rows: list[dict[str, str]], candidate_ids: set[str], slots: set[int]) -> list[dict[str, str]]:
    seen = set()
    selected = []
    for row in rows:
        candidate_id = row.get("candidate_id", "")
        if not candidate_id or candidate_id in seen:
            raise ValueError("candidate_id must be present and unique")
        seen.add(candidate_id)
        if candidate_ids and candidate_id not in candidate_ids:
            continue
        if slots:
            try:
                slot = int(candidate_id.rsplit("slot", 1)[1])
            except (IndexError, ValueError) as exc:
                raise ValueError(f"cannot parse slot from {candidate_id}") from exc
            if slot not in slots:
                continue
        selected.append(row)
    missing = candidate_ids - {row["candidate_id"] for row in selected}
    if missing:
        raise ValueError(f"requested candidate IDs not found: {sorted(missing)}")
    if not selected:
        raise ValueError("candidate selection is empty")
    return selected


def render(candidates: Path, output: Path, source_video: Path | None = None,
           frame_map_path: Path | None = None, candidate_ids: set[str] | None = None,
           slots: set[int] | None = None, sample_stride: int | None = None,
           context_scale: float = 6.0, min_context_width: int = 320,
           min_context_height: int = 240, zoom: int = 2) -> dict[str, object]:
    if context_scale < 1 or min_context_width < 1 or min_context_height < 1 or zoom < 1:
        raise ValueError("scale, context dimensions and zoom must be positive")
    csv_path, provenance_path, provenance, report_path, report = candidate_table(candidates)
    if report is not None:
        expected_csv_hash = report.get("hashes", {}).get("candidates_csv_sha256")
        if expected_csv_hash != digest(csv_path):
            raise ValueError("candidate CSV differs from fixed-budget report")
        report_stride = int(report["parameters"]["sample_stride"])
        if sample_stride is not None and sample_stride != report_stride:
            raise ValueError("sample stride differs from fixed-budget report")
        sample_stride = report_stride
    if sample_stride is None:
        sample_stride = 5
    if sample_stride < 1:
        raise ValueError("sample stride must be positive")
    with csv_path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    selected = select_rows(rows, candidate_ids or set(), slots or set())
    frame_map, frame_map_receipt = load_frame_map(frame_map_path)
    if source_video is None:
        if report and report.get("inputs", {}).get("source_video"):
            source_video = Path(str(report["inputs"]["source_video"]))
        elif provenance and provenance.get("source"):
            source_video = Path(str(provenance["source"]))
        else:
            raise ValueError("--source-video required when provenance.json has no source")
    source_video = source_video.resolve()
    if not source_video.is_file():
        raise ValueError(f"source video not found: {source_video}")
    source_sha256 = digest(source_video)
    if provenance and provenance.get("source_sha256") not in (None, source_sha256):
        raise ValueError("source video SHA256 differs from candidate provenance")
    if report and report.get("hashes", {}).get("source_video_sha256") != source_sha256:
        raise ValueError("source video SHA256 differs from fixed-budget report")

    capture = cv2.VideoCapture(str(source_video))
    if not capture.isOpened():
        raise ValueError(f"cannot open source video: {source_video}")
    frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    if frame_width < 1 or frame_height < 1 or frame_count < 1:
        capture.release()
        raise ValueError("invalid source video metadata")
    output.mkdir(parents=True, exist_ok=True)
    entries = []
    try:
        for row in selected:
            replay_frame = int(row["replay_frame"]) if row.get("replay_frame", "") else None
            csv_source = int(row["source_frame"]) if row.get("source_frame", "") else None
            mapped_source = frame_map.get(replay_frame) if replay_frame is not None else None
            if csv_source is not None and mapped_source is not None and csv_source != mapped_source:
                raise ValueError(f"candidate/frame-map mismatch for {row['candidate_id']}")
            source_frame = csv_source if csv_source is not None else mapped_source
            if source_frame is None and row.get("frame_index", "") != "":
                source_frame = int(row["frame_index"])
            if report and row.get("frame_index", "") != "":
                interval = report.get("scored_frame_interval_inclusive", [])
                if (len(interval) != 2 or
                        not int(interval[0]) <= int(row["frame_index"]) <= int(interval[1])):
                    raise ValueError(f"candidate outside fixed-budget interval: {row['candidate_id']}")
            if source_frame is None:
                raise ValueError(f"no source frame for {row['candidate_id']}")
            if not 0 <= source_frame < frame_count:
                raise ValueError(f"source frame out of range for {row['candidate_id']}")
            capture.set(cv2.CAP_PROP_POS_FRAMES, source_frame)
            ok, frame = capture.read()
            if not ok or frame.shape[:2] != (frame_height, frame_width):
                raise ValueError(f"cannot decode source frame {source_frame}")

            analysis_bbox = analysis_box(row)
            full_bbox = source_box(row, frame_width, frame_height, sample_stride)
            if row.get("selected_source_box", ""):
                recorded = tuple(int(value) for value in json.loads(row["selected_source_box"]))
                if recorded != full_bbox:
                    raise ValueError(f"recorded source bbox mismatch for {row['candidate_id']}")
            crop_bbox = context_box(full_bbox, frame_width, frame_height, context_scale,
                                    min_context_width, min_context_height)
            left, top, right, bottom = crop_bbox
            raw = frame[top:bottom + 1, left:right + 1].copy()
            stem = safe_stem(row["candidate_id"])
            raw_name = f"{stem}_context_raw.png"
            review_name = f"{stem}_context_review.png"
            raw_path, review_path = output / raw_name, output / review_name
            if not cv2.imwrite(str(raw_path), raw):
                raise OSError(f"could not write {raw_path}")

            marked = raw.copy()
            local_box = (full_bbox[0] - left, full_bbox[1] - top,
                         full_bbox[2] - left, full_bbox[3] - top)
            thickness = max(2, min(marked.shape[:2]) // 100)
            cv2.rectangle(marked, local_box[:2], local_box[2:], (0, 0, 255), thickness)
            enlarged = cv2.resize(marked, None, fx=zoom, fy=zoom, interpolation=cv2.INTER_NEAREST)
            header_height = 72
            review = np.full((enlarged.shape[0] + header_height, enlarged.shape[1], 3), 245, np.uint8)
            review[header_height:] = enlarged
            line1 = f"{row['candidate_id']}  source_frame={source_frame}"
            line2 = f"analysis_bbox={analysis_bbox}  source_bbox={full_bbox}"
            cv2.putText(review, line1, (8, 26), cv2.FONT_HERSHEY_SIMPLEX,
                        .65, (20, 20, 20), 2, cv2.LINE_AA)
            cv2.putText(review, line2, (8, 56), cv2.FONT_HERSHEY_SIMPLEX,
                        .52, (20, 20, 20), 1, cv2.LINE_AA)
            if not cv2.imwrite(str(review_path), review):
                raise OSError(f"could not write {review_path}")
            entries.append({
                "candidate_id": row["candidate_id"],
                "replay_frame": replay_frame,
                "source_frame": source_frame,
                "analysis_bbox_inclusive": list(analysis_bbox),
                "source_sample_cell_bbox_inclusive": list(full_bbox),
                "context_bbox_inclusive": list(crop_bbox),
                "raw_context": {"path": raw_name, "sha256": digest(raw_path),
                                "width": int(raw.shape[1]), "height": int(raw.shape[0])},
                "review_context": {"path": review_name, "sha256": digest(review_path),
                                   "width": int(review.shape[1]), "height": int(review.shape[0])},
                "candidate_roi_path": row.get("roi_path"),
                "candidate_roi_sha256": row.get("roi_sha256"),
                "label": row.get("label", ""),
                "reviewer": row.get("reviewer", ""),
            })
    finally:
        capture.release()

    receipt = {
        "status": "unlabeled_context_review_artifact",
        "candidate_table": {"path": str(csv_path), "sha256": digest(csv_path),
                            "row_count": len(rows), "selected_count": len(entries)},
        "candidate_provenance": ({"path": str(provenance_path), "sha256": digest(provenance_path)}
                                 if provenance_path else None),
        "fixed_budget_report": ({"path": str(report_path), "sha256": digest(report_path),
                                  "clip_id": report.get("clip_id")}
                                 if report_path and report else None),
        "source_video": {"path": str(source_video), "sha256": source_sha256,
                         "width": frame_width, "height": frame_height,
                         "frame_count": frame_count},
        "frame_map": frame_map_receipt,
        "parameters": {
            "sample_stride": sample_stride,
            "context_scale": context_scale,
            "min_context_width": min_context_width,
            "min_context_height": min_context_height,
            "zoom": zoom,
            "slots": sorted(slots or set()),
            "candidate_ids": sorted(candidate_ids or set()),
            "bbox_contract": ("analysis bbox is inclusive; source extent covers each sampled "
                              f"{sample_stride}x{sample_stride} cell through "
                              "stride*xmax+stride-1"),
        },
        "entries": entries,
    }
    index_path = output / "index.json"
    index_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return receipt


def self_test() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        video = root / "fixture.avi"
        writer = cv2.VideoWriter(str(video), cv2.VideoWriter_fourcc(*"MJPG"), 5.0, (1280, 720))
        if not writer.isOpened():
            raise RuntimeError("self-test video writer unavailable")
        for index in range(2):
            frame = np.zeros((720, 1280, 3), np.uint8)
            frame[:, :, 1] = 40 + index * 80
            writer.write(frame)
        writer.release()
        table = root / "candidates.csv"
        with table.open("w", encoding="utf-8", newline="") as handle:
            csv_writer = csv.DictWriter(handle, ["candidate_id", "replay_frame", "source_frame",
                "xmin", "ymin", "xmax", "ymax", "roi_path", "roi_sha256", "label", "reviewer"])
            csv_writer.writeheader()
            csv_writer.writerow({"candidate_id": "f00001_slot1", "replay_frame": 1,
                "source_frame": 1, "xmin": 10, "ymin": 12, "xmax": 14, "ymax": 20,
                "roi_path": "roi.png", "roi_sha256": "abc", "label": "", "reviewer": ""})
        result = render(table, root / "out", video, slots={1})
        assert len(result["entries"]) == 1
        entry = result["entries"][0]
        assert entry["source_sample_cell_bbox_inclusive"] == [50, 60, 74, 104]
        assert (root / "out" / entry["raw_context"]["path"]).is_file()
        assert json.loads((root / "out" / "index.json").read_text(encoding="utf-8"))["entries"]
        fixed_root = root / "fixed"
        fixed_root.mkdir()
        fixed_table = fixed_root / "candidates.csv"
        with fixed_table.open("w", encoding="utf-8", newline="") as handle:
            csv_writer = csv.DictWriter(handle, ["candidate_id", "frame_index",
                "selected_analysis_box", "selected_source_box"])
            csv_writer.writeheader()
            csv_writer.writerow({"candidate_id": "peak_difference:f000001:slot4",
                "frame_index": 1, "selected_analysis_box": "[10, 12, 14, 20]",
                "selected_source_box": "[50, 60, 74, 104]"})
        (fixed_root / "report.json").write_text(json.dumps({
            "clip_id": "fixture", "scored_frame_interval_inclusive": [1, 1],
            "parameters": {"sample_stride": 5},
            "inputs": {"source_video": str(video)},
            "hashes": {"candidates_csv_sha256": digest(fixed_table),
                       "source_video_sha256": digest(video)}}, indent=2), encoding="utf-8")
        fixed_result = render(fixed_table, root / "fixed_out", video)
        assert fixed_result["entries"][0]["source_frame"] == 1
        assert fixed_result["entries"][0]["analysis_bbox_inclusive"] == [10, 12, 14, 20]
        assert ":" not in fixed_result["entries"][0]["raw_context"]["path"]
    print("PASS: candidate context selection, source mapping, crop geometry, hashes and index")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path)
    parser.add_argument("--source-video", type=Path)
    parser.add_argument("--frame-map", type=Path,
                        help="manifest.json/directory or CSV with replay_frame,source_frame")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--candidate-id", action="append", default=[])
    parser.add_argument("--slot", action="append", type=int, default=[])
    parser.add_argument("--sample-stride", type=int)
    parser.add_argument("--context-scale", type=float, default=6.0)
    parser.add_argument("--min-context-width", type=int, default=320)
    parser.add_argument("--min-context-height", type=int, default=240)
    parser.add_argument("--zoom", type=int, default=2)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    if args.candidates is None or args.output is None:
        parser.error("--candidates and --output are required unless --self-test is used")
    result = render(args.candidates, args.output, args.source_video, args.frame_map,
                    set(args.candidate_id), set(args.slot), args.sample_stride,
                    args.context_scale, args.min_context_width,
                    args.min_context_height, args.zoom)
    print(json.dumps({"selected_count": len(result["entries"]),
                      "index": str((args.output / 'index.json').resolve())}, ensure_ascii=False))


if __name__ == "__main__":
    main()
