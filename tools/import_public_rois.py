"""Import explicitly mapped public boxes from a prepared clip, keeping provenance."""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import cv2
from roi_dataset_tool import DatasetWriter, fpga_analysis_frame


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepared", type=Path, required=True)
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--split", choices=["train", "val", "test"], required=True)
    parser.add_argument("--stride", type=int, default=10)
    args = parser.parse_args()
    if args.stride < 1:
        raise ValueError("stride must be positive")
    receipt_path = args.prepared / "provenance.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    videos = list(args.prepared.glob("*.avi"))
    if len(videos) != 1:
        raise ValueError("expected one prepared AVI")
    video = videos[0]
    if hashlib.sha256(video.read_bytes()).hexdigest() != receipt["output_sha256"]:
        raise ValueError("prepared video changed")
    with (args.prepared / "annotations_720p.csv").open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    writer = DatasetWriter(args.dataset, video, args.split, receipt["scene_id"], "annotated",
                           f"public_annotation:{receipt['dataset']}")
    cap = cv2.VideoCapture(str(video))
    imported = skipped = 0
    decisions = []
    try:
        for row in sorted(rows, key=lambda r: int(r["frame_index"])):
            frame_index = int(row["frame_index"])
            if row["label"] == "ignore" or frame_index % args.stride:
                skipped += 1
                continue
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
            ok, frame = cap.read()
            if not ok:
                raise ValueError(f"could not decode frame {frame_index}")
            # Select only stride-five sample locations lying inside the supplied bbox.
            x0, y0 = math.ceil(int(row["xmin"])/5), math.ceil(int(row["ymin"])/5)
            x1, y1 = int(row["xmax"])//5, int(row["ymax"])//5
            result = writer.save(fpga_analysis_frame(frame), frame_index, receipt.get("fps") or 0.0,
                                 (1280, 720), (x0, y0, x1, y1), row["label"])
            imported += int(result.saved)
            decisions.append({**row, "saved": result.saved, "message": result.message})
    finally:
        cap.release()
    provenance = args.dataset / "provenance"
    provenance.mkdir(exist_ok=True)
    token = hashlib.sha256(receipt_path.read_bytes()).hexdigest()
    (provenance / f"{token}.json").write_text(json.dumps({"receipt": receipt, "split": args.split,
        "prepared_annotations_sha256": hashlib.sha256((args.prepared / 'annotations_720p.csv').read_bytes()).hexdigest(),
        "decisions": decisions, "imported": imported, "skipped": skipped}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Imported {imported}; skipped {skipped}; annotation truth is separate from CCL candidates")


if __name__ == "__main__":
    main()
