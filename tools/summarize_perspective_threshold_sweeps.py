#!/usr/bin/env python3
"""Aggregate compatible perspective-threshold sweep receipts across windows."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", action="append", type=Path, required=True)
    parser.add_argument("--threshold", action="append", type=int, default=[])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    thresholds = sorted(set(args.threshold or (90, 100, 110)))
    if any("blind" in str(path).lower() for path in args.report):
        raise ValueError("blind-reserve report is forbidden")
    windows, receipts = [], []
    contract = None
    common_hashes = None
    for report_path in args.report:
        report = json.loads(report_path.read_text(encoding="utf-8"))
        if report.get("status") != "single_decode_perspective_threshold_final4_diagnostic_not_rtl_or_acceptance_evidence":
            raise ValueError(f"unexpected status: {report_path}")
        table_path = report_path.parent / "threshold_metrics.csv"
        if digest(table_path) != report["output_hashes"]["threshold_metrics_csv_sha256"]:
            raise ValueError(f"metrics hash mismatch: {report_path}")
        current_contract = report["parameters"]
        current_hashes = {
            "annotations_sha256": report["input_hashes"]["annotations_sha256"],
            "catalog_sha256": report["input_hashes"]["catalog_sha256"],
            "sweep_script_sha256": report["script_hashes"]["sweep_script_sha256"],
            "fixed_budget_dependency_sha256": report["script_hashes"][
                "fixed_budget_dependency_sha256"],
            "candidate_chain_dependency_sha256": report["script_hashes"][
                "candidate_chain_dependency_sha256"],
        }
        if contract is None:
            contract, common_hashes = current_contract, current_hashes
        elif current_contract != contract or current_hashes != common_hashes:
            raise ValueError(f"sweep contracts or common hashes differ: {report_path}")
        with table_path.open(encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                threshold = int(row["perspective_y_threshold"])
                if row["truth_center_y_band"] != "all" or threshold not in thresholds:
                    continue
                windows.append({
                    "window_id": (f"{report['clip_id']}:"
                                  f"{report['scored_frame_interval_inclusive'][0]}-"
                                  f"{report['scored_frame_interval_inclusive'][1]}"),
                    "threshold": threshold, "label": row["label"],
                    "annotation_rows": int(row["annotation_rows"]),
                    "covered_iou_0p1": int(row["final_covered_iou_0p1"]),
                    "covered_iou_0p25": int(row["final_covered_iou_0p25"]),
                    "covered_iou_0p5": int(row["final_covered_iou_0p5"]),
                    "main_possible": int(row["internal_main_count"]),
                    "main_retained": int(row["retained_main_count"]),
                    "empty_slots": int(row["final_empty_slots"]),
                    "nms_rejected": int(row["nms_rejected_candidates"]),
                })
        receipts.append({"path": str(report_path.resolve()), "sha256": digest(report_path)})
    aggregate = []
    for threshold in thresholds:
        for label in ("ped", "vehicle"):
            subset = [row for row in windows
                      if row["threshold"] == threshold and row["label"] == label]
            if len(subset) != len(args.report):
                raise ValueError(f"threshold {threshold}/{label} missing from a report")
            total = sum(row["annotation_rows"] for row in subset)
            record = {"threshold": threshold, "label": label,
                      "window_count": len(subset), "annotation_rows": total}
            for field in ("covered_iou_0p1", "covered_iou_0p25", "covered_iou_0p5"):
                covered = sum(row[field] for row in subset)
                suffix = field.removeprefix("covered_")
                record[field] = covered
                record[f"micro_rate_{suffix}"] = covered / total if total else None
                record[f"window_macro_rate_{suffix}"] = sum(
                    row[field] / row["annotation_rows"] if row["annotation_rows"] else 0
                    for row in subset) / len(subset)
            possible = sum(row["main_possible"] for row in subset)
            retained = sum(row["main_retained"] for row in subset)
            record.update({"main_possible": possible, "main_retained": retained,
                           "main_retention_rate": retained / possible if possible else None,
                           "empty_slots": sum(row["empty_slots"] for row in subset),
                           "nms_rejected": sum(row["nms_rejected"] for row in subset)})
            aggregate.append(record)
    args.output.mkdir(parents=True, exist_ok=True)
    output_tables = (("window_metrics.csv", windows), ("aggregate_metrics.csv", aggregate))
    for filename, rows in output_tables:
        with (args.output / filename).open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    summary = {
        "status": "cross_scene_perspective_threshold_diagnostic_not_acceptance_evidence",
        "thresholds": thresholds, "inputs": receipts,
        "contract": contract, "common_hashes": common_hashes,
        "summarizer_sha256": digest(Path(__file__)),
        "outputs": {name: digest(args.output / name) for name, _ in output_tables},
        "aggregate": aggregate,
        "boundary": (
            "Annotation-frame rows are temporally correlated and uneven across scenes. "
            "Use window macro rates beside micro rates. Geometry coverage is not object "
            "recall, classification recall, or a false-positive rate."),
    }
    (args.output / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": summary["status"], "windows": len(args.report),
                      "output": str(args.output.resolve())}, ensure_ascii=False))


if __name__ == "__main__":
    main()
