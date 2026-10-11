#!/usr/bin/env python3
"""Combine annotation-overlap hints with explicit human decisions, failing closed."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def finalize(matches_path: Path, decisions_path: Path, threshold: float = .3) -> tuple[list[dict], dict]:
    with matches_path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    decisions_document = json.loads(decisions_path.read_text(encoding="utf-8"))
    decisions = decisions_document["decisions"]
    known_ids = {row["candidate_id"] for row in rows}
    if set(decisions) - known_ids:
        raise ValueError("manual decision references an unknown candidate")
    reviewed = []
    basis_counts: Counter[str] = Counter()
    label_counts: Counter[str] = Counter()
    used_manual = set()
    for row in rows:
        candidate_id = row["candidate_id"]
        overlap_label = row["best_annotation_label"]
        overlap_iou = float(row["best_annotation_iou"])
        if overlap_iou >= threshold and overlap_label in {"ped", "vehicle"}:
            label = overlap_label
            reviewer = f"official_annotation_overlap_iou_ge_{threshold:g}"
            basis = "annotation_overlap_assisted"
            note = f"best annotation IoU={overlap_iou:.6f}"
        else:
            if candidate_id not in decisions:
                raise ValueError(f"missing explicit manual decision: {candidate_id}")
            decision = decisions[candidate_id]
            if decision.get("label") not in {"ped", "vehicle", "invalid", "ignore"}:
                raise ValueError(f"invalid manual label: {candidate_id}")
            for field in ("reviewer", "note"):
                if not isinstance(decision.get(field), str) or not decision[field].strip():
                    raise ValueError(f"manual decision missing {field}: {candidate_id}")
            label, reviewer, note = decision["label"], decision["reviewer"], decision["note"]
            basis = "human_visual_review"
            used_manual.add(candidate_id)
        reviewed.append({**row, "label": label, "reviewer": reviewer,
                         "review_basis": basis, "review_note": note})
        basis_counts[basis] += 1
        label_counts[label] += 1
    if used_manual != set(decisions):
        raise ValueError("manual decisions overlap auto-resolved candidates or were not consumed")
    review_context = decisions_document.get("review_context", {})
    if review_context and not isinstance(review_context, dict):
        raise ValueError("review_context must be an object")
    report = {
        "status": "review_complete_not_imported",
        "candidate_count": len(reviewed),
        "label_counts": dict(sorted(label_counts.items())),
        "review_basis_counts": dict(sorted(basis_counts.items())),
        "annotation_overlap_threshold": threshold,
        "matches_sha256": digest(matches_path),
        "manual_decisions_sha256": digest(decisions_path),
        "training_imported": False,
        "ignored_candidate_count": label_counts.get("ignore", 0),
        "metric_candidate_count": len(reviewed) - label_counts.get("ignore", 0),
        "review_context": review_context,
        "boundary": review_context.get(
            "boundary",
            "Consecutive source frames are correlated and are not appended wholesale to training."),
    }
    return reviewed, report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--matches", type=Path, required=True)
    parser.add_argument("--manual-decisions", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--iou-threshold", type=float, default=.3)
    args = parser.parse_args()
    if not 0 <= args.iou_threshold <= 1:
        raise ValueError("--iou-threshold must be in [0,1]")
    rows, report = finalize(args.matches, args.manual_decisions, args.iou_threshold)
    args.output.mkdir(parents=True, exist_ok=True)
    reviewed_path = args.output / "reviewed_candidates.csv"
    with reviewed_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    report["reviewed_candidates_sha256"] = digest(reviewed_path)
    (args.output / "review_summary.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
