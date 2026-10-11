#!/usr/bin/env python3
"""Create a deterministic, traceable review batch for final-four candidates."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path

import cv2
import numpy as np

from render_candidate_contexts import digest, render


REVIEW_CLASSES = (
    "ped_full", "ped_truncated", "vehicle", "merged_target",
    "background_fragment", "other_ignore")


def inclusive_iou(left: tuple[int, int, int, int],
                  right: tuple[int, int, int, int]) -> float:
    ix0, iy0 = max(left[0], right[0]), max(left[1], right[1])
    ix1, iy1 = min(left[2], right[2]), min(left[3], right[3])
    intersection = max(0, ix1 - ix0 + 1) * max(0, iy1 - iy0 + 1)
    left_area = (left[2] - left[0] + 1) * (left[3] - left[1] + 1)
    right_area = (right[2] - right[0] + 1) * (right[3] - right[1] + 1)
    union = left_area + right_area - intersection
    return intersection / union if union else 0.0


def load_annotations(path: Path, clip_id: str) -> dict[int, list[dict[str, str]]]:
    if "blind" in str(path).lower():
        raise ValueError("blind-reserve annotations are forbidden")
    result: dict[int, list[dict[str, str]]] = defaultdict(list)
    with path.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["clip_id"] == clip_id and row["label"] in {"ped", "vehicle"}:
                result[int(row["frame_index"])].append(row)
    return result


def annotation_hint(row: dict[str, str], annotations: dict[int, list[dict[str, str]]]
                    ) -> tuple[str, str, float]:
    box = tuple(int(value) for value in json.loads(row["selected_source_box"]))
    matches = []
    for annotation in annotations.get(int(row["frame_index"]), []):
        annotation_box = tuple(int(annotation[key]) for key in
                               ("xmin", "ymin", "xmax", "ymax"))
        matches.append((inclusive_iou(box, annotation_box), annotation))
    best_iou, best = max(matches, key=lambda item: item[0], default=(0.0, None))
    if best is None or best_iou < 0.1:
        return "unmatched_not_background", "", best_iou
    return f"annotation_{best['label']}", best["object_id"], best_iou


def temporal_groups(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    """Greedy tracklets used only to thin review work, never as semantic truth."""
    groups: list[dict[str, object]] = []
    active: dict[str, list[int]] = defaultdict(list)
    ordered = sorted(rows, key=lambda row: (int(row["frame_index"]), row["branch"],
                                            row["candidate_id"]))
    for row in ordered:
        frame = int(row["frame_index"])
        box = tuple(int(value) for value in json.loads(row["selected_source_box"]))
        area = (box[2] - box[0] + 1) * (box[3] - box[1] + 1)
        chosen = None
        for index in reversed(active[row["branch"]]):
            group = groups[index]
            gap = frame - int(group["last_frame"])
            if gap > 2:
                continue
            last_box = group["last_box"]
            last_area = int(group["last_area"])
            ratio = area / last_area if last_area else 0.0
            if 2 / 3 <= ratio <= 1.5 and inclusive_iou(box, last_box) >= 0.8:
                chosen = index
                break
        if chosen is None:
            chosen = len(groups)
            groups.append({"branch": row["branch"], "members": [],
                           "last_frame": frame, "last_box": box, "last_area": area})
            active[row["branch"]].append(chosen)
        group = groups[chosen]
        group["members"].append(row)
        group["last_frame"], group["last_box"], group["last_area"] = frame, box, area
    for index, group in enumerate(groups):
        group["group_id"] = f"g{index:05d}"
    return groups


def representative_rows(groups: list[dict[str, object]]) -> list[dict[str, object]]:
    representatives = []
    for group in groups:
        members = group["members"]
        positions = ([0, len(members) // 2, len(members) - 1]
                     if len(members) >= 10 else [len(members) // 2])
        for position in sorted(set(positions)):
            rule = ("first_middle_last" if len(members) >= 10 else "middle")
            representatives.append({
                "row": members[position], "group_id": group["group_id"],
                "group_size": len(members), "representative_rule": rule,
                "representative_position": position,
            })
    return representatives


def y_band(row: dict[str, str]) -> str:
    box = json.loads(row["selected_analysis_box"])
    center = (int(box[1]) + int(box[3])) / 2
    if center < 90:
        return "y_lt90"
    if center < 110:
        return "y90_109"
    if center < 130:
        return "y110_129"
    return "y_ge130"


def deterministic_sample(items: list[dict[str, object]], target: int, seed: str
                         ) -> list[dict[str, object]]:
    by_stratum: dict[str, list[dict[str, object]]] = defaultdict(list)
    for item in items:
        row = item["row"]
        stratum = f"{row['branch']}|{item['annotation_hint']}|{y_band(row)}"
        item["sampling_stratum"] = stratum
        by_stratum[stratum].append(item)
    for stratum, values in by_stratum.items():
        values.sort(key=lambda item: hashlib.sha256(
            f"{seed}|{stratum}|{item['row']['candidate_id']}".encode()).hexdigest())
    selected = []
    names = sorted(by_stratum)
    while len(selected) < target and any(by_stratum.values()):
        for name in names:
            if by_stratum[name] and len(selected) < target:
                selected.append(by_stratum[name].pop(0))
    totals = defaultdict(int)
    chosen = defaultdict(int)
    for item in items:
        totals[item["sampling_stratum"]] += 1
    for item in selected:
        chosen[item["sampling_stratum"]] += 1
    for item in selected:
        item["inclusion_probability"] = (
            chosen[item["sampling_stratum"]] / totals[item["sampling_stratum"]])
    return selected


def render_sheets(output: Path, manifest: list[dict[str, object]], per_sheet: int = 12
                  ) -> list[dict[str, object]]:
    receipts = []
    columns, tile_width, tile_height = 3, 480, 430
    for page, start in enumerate(range(0, len(manifest), per_sheet), 1):
        page_rows = manifest[start:start + per_sheet]
        row_count = (len(page_rows) + columns - 1) // columns
        sheet = np.full((row_count * tile_height, columns * tile_width, 3), 245, np.uint8)
        for index, row in enumerate(page_rows):
            image = cv2.imread(str(output / row["review_context_path"]))
            if image is None:
                raise ValueError(f"missing review context: {row['candidate_id']}")
            view = cv2.resize(image, (tile_width, tile_height - 54), interpolation=cv2.INTER_AREA)
            top, left = (index // columns) * tile_height, (index % columns) * tile_width
            sheet[top:top + tile_height - 54, left:left + tile_width] = view
            cv2.putText(sheet, row["candidate_id"][-36:], (left + 5, top + tile_height - 33),
                        cv2.FONT_HERSHEY_SIMPLEX, .42, (20, 20, 20), 1, cv2.LINE_AA)
            cv2.putText(sheet, f"{row['branch']} | {row['annotation_hint']}",
                        (left + 5, top + tile_height - 12), cv2.FONT_HERSHEY_SIMPLEX,
                        .42, (20, 20, 20), 1, cv2.LINE_AA)
        path = output / f"contact_sheet_{page:02d}.jpg"
        if not cv2.imwrite(str(path), sheet, [cv2.IMWRITE_JPEG_QUALITY, 94]):
            raise OSError(f"cannot write {path}")
        receipts.append({"path": path.name, "sha256": digest(path),
                         "candidate_count": len(page_rows)})
    return receipts


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--annotations", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--sample-size", type=int, default=120)
    parser.add_argument("--small-fraction", type=float, default=.75)
    parser.add_argument("--seed", default="final4-review-v1")
    args = parser.parse_args()
    if not 1 <= args.sample_size or not 0 <= args.small_fraction <= 1:
        raise ValueError("invalid sample size or small fraction")
    root = args.candidates.resolve()
    if "blind" in str(root).lower():
        raise ValueError("blind-reserve candidates are forbidden")
    report_path, table_path = root / "report.json", root / "candidates.csv"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    if report["hashes"]["candidates_csv_sha256"] != digest(table_path):
        raise ValueError("candidate CSV differs from report")
    if report["parameters"].get("final_output_strategies") != ["internal8_to4"]:
        raise ValueError("review root must contain only internal8_to4")
    with table_path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows or any(row.get("final_strategy") != "internal8_to4" for row in rows):
        raise ValueError("candidate strategy mismatch")
    annotations = load_annotations(args.annotations, report["clip_id"])
    for row in rows:
        hint, object_id, overlap = annotation_hint(row, annotations)
        row["annotation_hint"], row["annotation_hint_object_id"] = hint, object_id
        row["annotation_hint_iou"] = overlap
    groups = temporal_groups(rows)
    reps = representative_rows(groups)
    for item in reps:
        item["annotation_hint"] = item["row"]["annotation_hint"]
    small_target = round(args.sample_size * args.small_fraction)
    main_target = args.sample_size - small_target
    small = deterministic_sample(
        [item for item in reps if item["row"]["branch"] == "small_component_experimental"],
        small_target, args.seed + "|small")
    main = deterministic_sample(
        [item for item in reps if item["row"]["branch"] == "main_area_topk"],
        main_target, args.seed + "|main")
    selected = sorted(small + main, key=lambda item: (
        int(item["row"]["frame_index"]), int(item["row"]["slot"])))
    context_dir = args.output / "contexts"
    context = render(root, context_dir,
                     candidate_ids={item["row"]["candidate_id"] for item in selected})
    context_by_id = {item["candidate_id"]: item for item in context["entries"]}
    manifest = []
    immutable_fields = (
        "candidate_id", "frame_index", "final_strategy", "final_arbitration_rank",
        "slot", "branch", "component_label", "baseline_main4_rank",
        "raw_analysis_box", "selected_analysis_box", "selected_source_box")
    for item in selected:
        row, entry = item["row"], context_by_id[item["row"]["candidate_id"]]
        record = {field: row.get(field, "") for field in immutable_fields}
        record.update({
            "clip_id": report["clip_id"], "scene_split": report["inputs"]["catalog_split"],
            "source_video_sha256": report["hashes"]["source_video_sha256"],
            "candidate_report_sha256": digest(report_path),
            "candidates_csv_sha256": digest(table_path),
            "dedup_group_id": item["group_id"], "group_size": item["group_size"],
            "representative_rule": item["representative_rule"],
            "representative_position": item["representative_position"],
            "sampling_stratum": item["sampling_stratum"],
            "inclusion_probability": item["inclusion_probability"], "sample_seed": args.seed,
            "annotation_hint": row["annotation_hint"],
            "annotation_hint_object_id": row["annotation_hint_object_id"],
            "annotation_hint_iou": row["annotation_hint_iou"],
            "raw_context_path": f"contexts/{entry['raw_context']['path']}",
            "raw_context_sha256": entry["raw_context"]["sha256"],
            "review_context_path": f"contexts/{entry['review_context']['path']}",
            "review_context_sha256": entry["review_context"]["sha256"],
            "review_class": "", "occlusion": "", "truncation_reason": "",
            "dominant_semantic": "", "reviewer": "", "reviewed_at": "",
            "review_basis": "", "review_note": "",
        })
        manifest.append(record)
    args.output.mkdir(parents=True, exist_ok=True)
    manifest_path = args.output / "review_manifest.csv"
    with manifest_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(manifest[0]))
        writer.writeheader()
        writer.writerows(manifest)
    group_path = args.output / "dedup_groups.json"
    group_path.write_text(json.dumps({
        "contract": "gap<=2, source-box IoU>=0.8, area ratio in [2/3,1.5], same branch",
        "groups": [{"group_id": group["group_id"], "branch": group["branch"],
                    "member_ids": [row["candidate_id"] for row in group["members"]]}
                   for group in groups]}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    sheets = render_sheets(args.output, manifest)
    instructions_path = args.output / "REVIEW_INSTRUCTIONS.md"
    instructions_path.write_text(
        "# Candidate review\n\nAllowed `review_class`: " + ", ".join(REVIEW_CLASSES) +
        ". Every sampled row requires an explicit human decision. Annotation hints are "
        "sampling aids only; unmatched never means background. Use `ped_truncated` only when "
        "the candidate box cuts visible body parts; scene occlusion belongs in `occlusion`. "
        "`background_fragment`, `merged_target`, and `other_ignore` require a note. Set "
        "`review_basis=human_visual_review`. No sample is imported into training by this tool.\n",
        encoding="utf-8")
    context_index = context_dir / "index.json"
    receipt = {
        "status": "pending_explicit_human_review_training_imported_false",
        "clip_id": report["clip_id"], "strategy": "internal8_to4",
        "review_classes": list(REVIEW_CLASSES),
        "sample": {"requested": args.sample_size, "selected": len(manifest),
                   "small": len(small), "main": len(main), "seed": args.seed},
        "inputs": {"candidate_report": str(report_path),
                   "candidate_report_sha256": digest(report_path),
                   "candidates_csv": str(table_path), "candidates_csv_sha256": digest(table_path),
                   "annotations": str(args.annotations.resolve()),
                   "annotations_sha256": digest(args.annotations)},
        "outputs": {"review_manifest_sha256": digest(manifest_path),
                    "dedup_groups_sha256": digest(group_path),
                    "context_index_sha256": digest(context_index),
                    "instructions_sha256": digest(instructions_path),
                    "contact_sheets": sheets},
        "boundary": (
            "VIRAT annotations are incomplete. Annotation overlap is only a review hint. "
            "No unmatched candidate is automatically labeled background and no row is imported."),
    }
    (args.output / "receipt.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": receipt["status"], "selected": len(manifest),
                      "output": str(args.output.resolve())}, ensure_ascii=False))


if __name__ == "__main__":
    main()
