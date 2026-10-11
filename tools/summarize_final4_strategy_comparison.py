#!/usr/bin/env python3
"""Aggregate traceable final-four strategy reports without decoding video again."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path


STRATEGIES = ("main3_small1", "main2_small2", "internal8_to4")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_rate(numerator: int, denominator: int) -> float | None:
    return numerator / denominator if denominator else None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if any("blind" in str(path).lower() for path in args.report):
        raise ValueError("blind-reserve reports are forbidden")

    window_rows: list[dict[str, object]] = []
    aggregate: dict[tuple[str, float, str], dict[str, object]] = defaultdict(
        lambda: {"annotation_rows": 0, "baseline_main4_covered_rows": 0,
                 "combined_covered_rows": 0, "added_vs_baseline_rows": 0,
                 "lost_vs_baseline_rows": 0, "window_rates": []})
    selection: dict[str, dict[str, int]] = defaultdict(
        lambda: {"retained_main": 0, "possible_main": 0,
                 "empty_slots": 0, "candidate_count": 0})
    input_receipts = []
    reference_contract = None
    reference_hashes = None

    for report_path in args.report:
        report = json.loads(report_path.read_text(encoding="utf-8"))
        if report.get("status") != "python_fixed_budget_post_cleanup_diagnostic_not_rtl_or_acceptance_evidence":
            raise ValueError(f"unexpected report status: {report_path}")
        results = {row.get("final_strategy"): row for row in report["results"]}
        if set(results) != set(STRATEGIES):
            raise ValueError(f"report does not contain exactly three strategies: {report_path}")
        if report["parameters"].get("small_box_mode") != "perspective":
            raise ValueError(f"comparison must use perspective mode: {report_path}")
        contract_fields = (
            "sample_stride", "learn_frames", "threshold", "min_neighbors", "min_run",
            "main_min_area", "small_min_area", "small_max_area", "minimum_small_box",
            "small_box_mode", "perspective_y_threshold", "perspective_minimum_box",
            "perspective_top_margin", "nms_iou", "final_output_strategies",
            "effective_final_output_budget", "internal_pool_budget",
            "bounded_small_pool_budget")
        contract = {field: report["parameters"].get(field) for field in contract_fields}
        comparable_hashes = {
            field: report["hashes"].get(field) for field in
            ("annotations_csv_sha256", "candidate_chain_reference_sha256",
             "development_catalog_sha256", "script_sha256")}
        if reference_contract is None:
            reference_contract, reference_hashes = contract, comparable_hashes
        elif contract != reference_contract or comparable_hashes != reference_hashes:
            raise ValueError(f"comparison contract or common input hashes differ: {report_path}")
        window_id = (f"{report['clip_id']}:"
                     f"{report['scored_frame_interval_inclusive'][0]}-"
                     f"{report['scored_frame_interval_inclusive'][1]}")
        input_receipts.append({
            "path": str(report_path.resolve()), "sha256": digest(report_path),
            "window_id": window_id,
        })
        for strategy in STRATEGIES:
            result = results[strategy]
            selection[strategy]["retained_main"] += int(
                result["raw_main_top4_retained_count"])
            selection[strategy]["possible_main"] += int(
                result["raw_main_top4_possible_count"])
            selection[strategy]["empty_slots"] += int(result["final_empty_slots"])
            selection[strategy]["candidate_count"] += int(result["candidate_count"])
            for metric in result["annotation_coverage_iou_sweep"]:
                row = {
                    "window_id": window_id, "strategy": strategy,
                    "iou_threshold": float(metric["iou_threshold"]),
                    "label": metric["label"],
                    "annotation_rows": int(metric["annotation_rows"]),
                    "baseline_main4_covered_rows": int(
                        metric["baseline_main4_covered_rows"]),
                    "combined_covered_rows": int(metric["combined_covered_rows"]),
                    "added_vs_baseline_rows": int(metric["added_vs_baseline_rows"]),
                    "lost_vs_baseline_rows": int(metric["lost_vs_baseline_rows"]),
                    "combined_coverage_rate": metric["combined_coverage_rate"],
                }
                window_rows.append(row)
                key = (strategy, row["iou_threshold"], row["label"])
                target = aggregate[key]
                for field in ("annotation_rows", "baseline_main4_covered_rows",
                              "combined_covered_rows", "added_vs_baseline_rows",
                              "lost_vs_baseline_rows"):
                    target[field] += row[field]
                if row["combined_coverage_rate"] is not None:
                    target["window_rates"].append(float(row["combined_coverage_rate"]))

    aggregate_rows = []
    for (strategy, threshold, label), values in sorted(aggregate.items()):
        count = int(values["annotation_rows"])
        combined = int(values["combined_covered_rows"])
        rates = values.pop("window_rates")
        aggregate_rows.append({
            "strategy": strategy, "iou_threshold": threshold, "label": label,
            **values,
            "micro_coverage_rate": safe_rate(combined, count),
            "window_macro_coverage_rate": sum(rates) / len(rates) if rates else None,
        })

    selection_rows = []
    for strategy in STRATEGIES:
        values = selection[strategy]
        selection_rows.append({
            "strategy": strategy, **values,
            "main_top4_retention_rate": safe_rate(
                values["retained_main"], values["possible_main"]),
        })

    args.output.mkdir(parents=True, exist_ok=True)
    output_tables = (("window_metrics.csv", window_rows),
                     ("aggregate_metrics.csv", aggregate_rows),
                     ("selection_metrics.csv", selection_rows))
    for filename, rows in output_tables:
        with (args.output / filename).open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    summary = {
        "status": "development_window_strategy_comparison_not_acceptance_evidence",
        "primary_diagnostic_iou": 0.25,
        "strategies": list(STRATEGIES),
        "inputs": input_receipts,
        "comparison_contract": reference_contract,
        "common_input_hashes": reference_hashes,
        "summarizer_sha256": digest(Path(__file__)),
        "output_csv_sha256": {
            filename: digest(args.output / filename) for filename, _ in output_tables},
        "aggregate_metrics": aggregate_rows,
        "selection_metrics": selection_rows,
        "boundary": (
            "Rows are correlated annotation-frame observations from three already-used "
            "development windows. VIRAT annotations are incomplete. Coverage is a candidate "
            "geometry diagnostic, not object recall, classification recall, or a false-positive rate."),
    }
    (args.output / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": summary["status"],
                      "windows": len(args.report),
                      "output": str(args.output.resolve())}, ensure_ascii=False))


if __name__ == "__main__":
    main()
