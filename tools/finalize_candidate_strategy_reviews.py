#!/usr/bin/env python3
"""Finalize two sealed human-review manifests without touching their sources.

This tool applies the explicitly adjudicated rows from the 2026-09-27 review,
normalizes reviewer metadata, verifies source/image hashes, and emits immutable
derived CSV/JSON artifacts.  It never imports samples into training and rejects
test/blind/holdout inputs.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


FINAL_DATE = "2026-09-27"
FINAL_BASIS = "human_visual_review"
FINAL_REVIEWER = "1"
ALLOWED_SPLITS = {"train", "val"}
SEALED_TOKENS = {"test", "blind", "holdout"}

FILL_REL = Path(
    "evaluation/candidate_reviews/guarded_fill_only_T100_paired_review/"
    "review_manifest_v2.csv"
)
FILL_RECEIPT_REL = FILL_REL.with_name("receipt_v2.json")
INTERNAL_REL = Path(
    "evaluation/candidate_reviews/final4_internal8_000206_f600_1499_y100/"
    "review_manifest.csv"
)
INTERNAL_RECEIPT_REL = INTERNAL_REL.with_name("receipt.json")
DEFAULT_OUT_REL = Path("evaluation/candidate_reviews/finalized_20260927")

APPENDED_FIELDS = [
    "source_row_number",
    "source_manifest_sha256",
    "review_basis_canonical",
    "review_basis_source",
    "normalized_at",
    "original_review_class",
    "original_same_frame_new_target",
    "original_duplicate_of_baseline",
    "original_duplicate_baseline_number",
    "original_crop_usable",
    "original_reviewer",
    "original_reviewed_at",
    "original_review_basis",
    "adjudication_status",
    "adjudication_reason",
    "metric_eligible",
    "audit_gap_codes",
]

INTERNAL_APPENDED_FIELDS = [
    "source_row_number",
    "source_manifest_sha256",
    "review_basis_canonical",
    "review_basis_source",
    "normalized_at",
    "original_review_class",
    "original_dominant_semantic",
    "original_reviewer",
    "original_reviewed_at",
    "original_review_basis",
    "adjudication_status",
    "adjudication_reason",
    "metric_eligible",
    "audit_gap_codes",
]


def _fill(**values: str) -> dict[str, str]:
    return values


# This is an explicit decision table, not an inferred relabeling rule.
FILL_ADJUDICATIONS: dict[str, dict[str, str]] = {
    "gf0005": _fill(
        review_class="background_fragment", same_frame_new_target="no",
        crop_usable="no", occlusion="none", truncation_reason="none",
        geometry_preference="none",
        review_note="parking-line/curb fragment; nearby pedestrian lies outside T100 ROI",
    ),
    "gf0011": _fill(
        review_class="background_fragment", same_frame_new_target="no",
        crop_usable="no", occlusion="none", truncation_reason="none",
        geometry_preference="none",
        review_note="parking-line/curb fragment; nearby pedestrian lies outside T100 ROI",
    ),
    "gf0042": _fill(
        review_class="background_fragment", same_frame_new_target="no",
        crop_usable="no", occlusion="none", truncation_reason="none",
        geometry_preference="none",
        review_note="foliage-edge/background fragment; no coherent semantic target in T100 ROI",
    ),
    "gf0045": _fill(
        review_class="background_fragment", same_frame_new_target="no",
        crop_usable="no", occlusion="none", truncation_reason="none",
        geometry_preference="none",
        review_note="foliage-edge/background fragment; no coherent semantic target in T100 ROI",
    ),
    "gf0004": _fill(
        review_class="ped_truncated", same_frame_new_target="yes", crop_usable="yes",
        occlusion="partial", truncation_reason="crop_tight", geometry_preference="equivalent",
        review_note="T100 cuts visible head/upper body; remaining torso/legs retain pedestrian structure",
    ),
    "gf0006": _fill(
        review_class="ped_truncated", same_frame_new_target="yes", crop_usable="yes",
        occlusion="partial", truncation_reason="crop_tight", geometry_preference="equivalent",
        review_note="T100 cuts visible head/upper body; remaining torso/legs retain pedestrian structure",
    ),
    "gf0010": _fill(
        review_class="ped_truncated", same_frame_new_target="yes", crop_usable="yes",
        occlusion="partial", truncation_reason="crop_tight", geometry_preference="equivalent",
        review_note="T100 cuts visible head/upper body; remaining torso/legs retain pedestrian structure",
    ),
    "gf0012": _fill(
        review_class="ped_truncated", same_frame_new_target="yes", crop_usable="yes",
        occlusion="none", truncation_reason="crop_tight", geometry_preference="equivalent",
        review_note="T100 cuts visible head/upper body; remaining torso/legs retain pedestrian structure",
    ),
    "gf0023": _fill(
        review_class="ped_full", same_frame_new_target="yes", crop_usable="yes",
        occlusion="none", truncation_reason="none", geometry_preference="equivalent",
    ),
    "gf0025": _fill(
        review_class="ped_full", same_frame_new_target="yes", crop_usable="yes",
        occlusion="none", truncation_reason="none", geometry_preference="equivalent",
    ),
    "gf0037": _fill(
        review_class="ped_full", same_frame_new_target="yes", crop_usable="yes",
        occlusion="partial", truncation_reason="none", geometry_preference="T100",
        review_note="visible upper body is contained; lower body is scene-occluded by vehicle",
    ),
    "gf0044": _fill(
        review_class="ped_full", same_frame_new_target="yes", crop_usable="yes",
        occlusion="partial", truncation_reason="none", geometry_preference="equivalent",
        review_note="visible upper body is contained; lower body is scene-occluded by vehicle",
    ),
    "gf0048": _fill(
        review_class="ped_truncated", same_frame_new_target="yes", crop_usable="no",
        occlusion="none", truncation_reason="crop_tight", geometry_preference="T90",
    ),
    "gf0049": _fill(
        review_class="ped_full", same_frame_new_target="yes", crop_usable="yes",
        occlusion="none", truncation_reason="none", geometry_preference="T100",
    ),
    "gf0050": _fill(
        review_class="ped_full", same_frame_new_target="yes", crop_usable="yes",
        occlusion="none", truncation_reason="none", geometry_preference="T100",
    ),
    "gf0051": _fill(
        review_class="ped_truncated", same_frame_new_target="yes", crop_usable="no",
        occlusion="partial", truncation_reason="crop_tight", geometry_preference="T90",
    ),
    "gf0052": _fill(
        review_class="ped_full", same_frame_new_target="yes", crop_usable="yes",
        occlusion="none", truncation_reason="none", geometry_preference="T100",
    ),
    "gf0053": _fill(
        review_class="ped_truncated", same_frame_new_target="yes", crop_usable="no",
        occlusion="none", truncation_reason="crop_tight", geometry_preference="T90",
    ),
}

INTERNAL_MERGED_ID = "internal8_to4:peak_difference:f000609:slot0"
INTERNAL_UNCERTAIN_IDS = {
    "internal8_to4:peak_difference:f000612:slot1",
    "internal8_to4:peak_difference:f000716:slot2",
    "internal8_to4:peak_difference:f000720:slot3",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def canonical_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"missing CSV header: {path}")
        return list(reader.fieldnames), list(reader)


def write_csv(path: Path, fields: list[str], rows: Iterable[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n", extrasaction="raise")
        writer.writeheader()
        writer.writerows(rows)


def normalize_reviewed_at(value: str) -> str:
    """Normalize actual dates while preserving missing/placeholder dates as null CSV cells."""
    cleaned = (value or "").strip()
    if not cleaned or cleaned.upper() == "YYYY-MM-DD":
        return ""
    match = re.fullmatch(r"(\d{4})[/-](\d{1,2})[/-](\d{1,2})", cleaned)
    if not match:
        raise ValueError(f"unsupported reviewed_at value: {value!r}")
    year, month, day = (int(part) for part in match.groups())
    normalized = f"{year:04d}-{month:02d}-{day:02d}"
    if normalized != FINAL_DATE:
        raise ValueError(f"unexpected review date: {normalized}")
    return normalized


def has_sealed_token(value: str | Path) -> bool:
    tokens = {part for part in re.split(r"[^a-z0-9]+", str(value).lower()) if part}
    return bool(tokens & SEALED_TOKENS)


def ensure_under(path: Path, root: Path, label: str) -> Path:
    resolved = path.resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError(f"{label} escapes project root: {resolved}") from exc
    if has_sealed_token(resolved.relative_to(root.resolve())):
        raise ValueError(f"{label} contains sealed test/blind/holdout token: {resolved}")
    return resolved


def verify_hash(path: Path, expected: str, label: str, checks: list[dict[str, str]]) -> str:
    if not path.is_file():
        raise FileNotFoundError(f"missing {label}: {path}")
    actual = sha256(path)
    if actual.lower() != expected.lower():
        raise ValueError(f"{label} hash mismatch: expected {expected}, got {actual}: {path}")
    checks.append({"label": label, "path": str(path), "sha256": actual})
    return actual


def verify_image(path: Path, expected: str, label: str, checks: list[dict[str, str]]) -> None:
    verify_hash(path, expected, label, checks)
    try:
        from PIL import Image
    except ImportError as exc:
        raise RuntimeError("Pillow is required to verify review images") from exc
    with Image.open(path) as image:
        image.verify()


def path_from_receipt(project: Path, raw: str, label: str) -> Path:
    candidate = Path(raw)
    if not candidate.is_absolute():
        candidate = project / candidate
    return ensure_under(candidate, project, label)


def validate_split(rows: list[dict[str, str]], label: str) -> None:
    splits = {row.get("scene_split", "").strip().lower() for row in rows}
    if not splits or not splits <= ALLOWED_SPLITS:
        raise ValueError(f"{label} includes forbidden/unknown scene_split: {sorted(splits)}")
    for row in rows:
        for field in ("window_id", "clip_id", "scene_split"):
            if has_sealed_token(row.get(field, "")):
                raise ValueError(f"{label} row contains sealed token in {field}: {row.get(field)}")


def verify_fill_sources(
    project: Path,
    manifest: Path,
    receipt_path: Path,
    rows: list[dict[str, str]],
) -> tuple[dict[str, Any], list[dict[str, str]]]:
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    checks: list[dict[str, str]] = []
    inputs = receipt["input_receipts"]
    for name in ("guarded_report", "selected_candidates", "decision_events", "window_metrics", "catalog", "guarded_tool", "review_tool"):
        item = inputs[name]
        verify_hash(path_from_receipt(project, item["path"], f"fill {name}"), item["sha256"], f"fill {name}", checks)
    video_hashes: dict[str, str] = {}
    for clip_id, item in inputs["videos"].items():
        video_hashes[clip_id] = verify_hash(
            path_from_receipt(project, item["path"], f"fill video {clip_id}"),
            item["sha256"], f"fill video {clip_id}", checks,
        )
    group_receipts = {item["group_id"]: item for item in receipt["outputs"]["group_images"]}
    if set(group_receipts) != {row["group_id"] for row in rows}:
        raise ValueError("fill group-image receipt IDs do not exactly match manifest")
    review_root = manifest.parent
    for row in rows:
        item = group_receipts[row["group_id"]]
        if row["review_image_path"] != item["path"] or row["review_image_sha256"] != item["sha256"]:
            raise ValueError(f"fill row/receipt image mismatch: {row['group_id']}")
        image_path = ensure_under(review_root / row["review_image_path"], review_root, "fill review image")
        verify_image(image_path, row["review_image_sha256"], f"fill image {row['group_id']}", checks)
        if row["source_video_sha256"] != video_hashes[row["clip_id"]]:
            raise ValueError(f"fill row video hash mismatch: {row['group_id']}")
    for index, item in enumerate(receipt["outputs"].get("contact_sheets", []), 1):
        image_path = ensure_under(review_root / item["path"], review_root, "fill contact sheet")
        verify_image(image_path, item["sha256"], f"fill contact sheet {index}", checks)
    # The receipt binds the blank template. Human review intentionally changes the manifest.
    prior = receipt["outputs"]["review_manifest"]["sha256"]
    current = sha256(manifest)
    if prior == current:
        raise ValueError("fill manifest still equals the blank-template receipt; no human edits detected")
    return receipt, checks


def verify_internal_sources(
    project: Path,
    manifest: Path,
    receipt_path: Path,
    rows: list[dict[str, str]],
    known_videos: dict[str, dict[str, Any]],
) -> tuple[dict[str, Any], list[dict[str, str]]]:
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    checks: list[dict[str, str]] = []
    for name in ("candidate_report", "candidates_csv", "annotations"):
        expected_key = f"{name}_sha256"
        verify_hash(
            path_from_receipt(project, receipt["inputs"][name], f"internal {name}"),
            receipt["inputs"][expected_key], f"internal {name}", checks,
        )
    review_root = manifest.parent
    verify_hash(review_root / "dedup_groups.json", receipt["outputs"]["dedup_groups_sha256"],
                "internal dedup groups", checks)
    verify_hash(review_root / "contexts/index.json", receipt["outputs"]["context_index_sha256"],
                "internal context index", checks)
    verify_hash(review_root / "REVIEW_INSTRUCTIONS.md", receipt["outputs"]["instructions_sha256"],
                "internal review instructions", checks)
    for index, item in enumerate(receipt["outputs"].get("contact_sheets", []), 1):
        image_path = ensure_under(review_root / item["path"], review_root, "internal contact sheet")
        verify_image(image_path, item["sha256"], f"internal contact sheet {index}", checks)
    for row in rows:
        for kind in ("raw", "review"):
            rel = row[f"{kind}_context_path"]
            image_path = ensure_under(review_root / rel, review_root, f"internal {kind} context")
            verify_image(image_path, row[f"{kind}_context_sha256"], f"internal {kind} {row['candidate_id']}", checks)
        if row["candidate_report_sha256"] != receipt["inputs"]["candidate_report_sha256"]:
            raise ValueError(f"internal candidate-report hash mismatch in {row['candidate_id']}")
        if row["candidates_csv_sha256"] != receipt["inputs"]["candidates_csv_sha256"]:
            raise ValueError(f"internal candidate CSV hash mismatch in {row['candidate_id']}")
        clip = row["clip_id"]
        if clip not in known_videos:
            raise ValueError(f"internal clip missing from sealed fill receipt video catalog: {clip}")
        if row["source_video_sha256"] != known_videos[clip]["sha256"]:
            raise ValueError(f"internal source-video hash mismatch in {row['candidate_id']}")
    prior = receipt["outputs"]["review_manifest_sha256"]
    current = sha256(manifest)
    if prior == current:
        raise ValueError("internal manifest still equals blank-template receipt; no human edits detected")
    return receipt, checks


def changes(old: dict[str, str], new: dict[str, str], fields: Iterable[str]) -> dict[str, dict[str, str]]:
    return {field: {"from": old.get(field, ""), "to": new.get(field, "")}
            for field in fields if old.get(field, "") != new.get(field, "")}


def finalize_fill(
    fields: list[str], rows: list[dict[str, str]], manifest_hash: str,
) -> tuple[list[dict[str, str]], list[dict[str, Any]], list[dict[str, str]]]:
    if len(rows) != 54 or {r["group_id"] for r in rows} != {f"gf{i:04d}" for i in range(54)}:
        raise ValueError("fill manifest must contain exactly gf0000..gf0053")
    output: list[dict[str, str]] = []
    decisions: list[dict[str, Any]] = []
    conflicts: list[dict[str, str]] = []
    for row_number, source in enumerate(rows, 2):
        old = dict(source)
        row = dict(source)
        key = row["group_id"]
        explicit = FILL_ADJUDICATIONS.get(key, {})
        row.update(explicit)
        row["reviewer"] = FINAL_REVIEWER
        row["reviewed_at"] = normalize_reviewed_at(old["reviewed_at"])
        # Duplicate means the same semantic target already has a baseline main box.
        # Background is neither a new target nor a duplicate target.
        if row["review_class"] == "background_fragment":
            row["same_frame_new_target"] = "no"
            row["duplicate_of_baseline"] = "no"
            row["duplicate_baseline_number"] = ""
        elif row["same_frame_new_target"] == "yes":
            row["duplicate_of_baseline"] = "no"
            row["duplicate_baseline_number"] = ""
        elif row["duplicate_of_baseline"] != "yes" or not re.fullmatch(r"M[0-3]", row["duplicate_baseline_number"]):
            raise ValueError(f"semantic target lacks a valid same-frame new/duplicate decision: {key}")
        if row["crop_usable"] not in {"yes", "no"}:
            raise ValueError(f"invalid crop_usable in {key}")
        if row["review_class"] not in {"ped_full", "ped_truncated", "background_fragment"}:
            raise ValueError(f"unexpected fill review_class in {key}: {row['review_class']}")
        row_changes = changes(old, row, fields)
        reason = "explicit_2026-09-27_adjudication" if explicit else "metadata_normalization_only"
        gap_codes: list[str] = []
        row.update({
            "source_row_number": str(row_number),
            "source_manifest_sha256": manifest_hash,
            "review_basis_canonical": FINAL_BASIS,
            "review_basis_source": old["review_basis"],
            "normalized_at": FINAL_DATE,
            "original_review_class": old["review_class"],
            "original_same_frame_new_target": old["same_frame_new_target"],
            "original_duplicate_of_baseline": old["duplicate_of_baseline"],
            "original_duplicate_baseline_number": old["duplicate_baseline_number"],
            "original_crop_usable": old["crop_usable"],
            "original_reviewer": old["reviewer"],
            "original_reviewed_at": old["reviewed_at"],
            "original_review_basis": old["review_basis"],
            "adjudication_status": "changed" if row_changes else "unchanged",
            "adjudication_reason": reason,
            "metric_eligible": "yes",
            "audit_gap_codes": "|".join(gap_codes),
        })
        if row_changes:
            decisions.append({"dataset": "fill_only_T100", "row_key": key,
                              "source_row_number": row_number, "reason": reason, "changes": row_changes})
            for field, delta in row_changes.items():
                if field in {"review_class", "same_frame_new_target", "crop_usable", "review_note"}:
                    conflicts.append({
                        "dataset": "fill_only_T100", "row_key": key,
                        "source_row_number": str(row_number), "severity": "resolved",
                        "code": "explicit_adjudication", "field": field,
                        "observed": delta["from"], "resolution": delta["to"],
                        "metric_effect": "included_after_adjudication", "note": reason,
                    })
        output.append(row)
    class_counts = Counter(row["review_class"] for row in output)
    crop_counts = Counter(row["crop_usable"] for row in output)
    if class_counts != Counter({"background_fragment": 21, "ped_full": 19, "ped_truncated": 14}):
        raise AssertionError(f"fill class totals violate approved decision: {class_counts}")
    if crop_counts != Counter({"no": 30, "yes": 24}):
        raise AssertionError(f"fill crop totals violate approved decision: {crop_counts}")
    return output, decisions, conflicts


def finalize_internal(
    fields: list[str], rows_including_blank: list[dict[str, str]], manifest_hash: str,
) -> tuple[list[dict[str, str]], list[dict[str, Any]], list[dict[str, str]], int]:
    blank_count = sum(not any((value or "").strip() for value in row.values()) for row in rows_including_blank)
    rows = [row for row in rows_including_blank if any((value or "").strip() for value in row.values())]
    if len(rows) != 120 or blank_count != 1:
        raise ValueError(f"internal manifest expected 120 substantive + 1 blank row, got {len(rows)} + {blank_count}")
    if len({row["candidate_id"] for row in rows}) != 120:
        raise ValueError("internal candidate_id values are not unique")
    output: list[dict[str, str]] = []
    decisions: list[dict[str, Any]] = []
    conflicts: list[dict[str, str]] = []
    for row_number, source in enumerate(rows_including_blank, 2):
        if not any((value or "").strip() for value in source.values()):
            conflicts.append({
                "dataset": "internal8_to4", "row_key": "", "source_row_number": str(row_number),
                "severity": "ignored", "code": "blank_csv_row", "field": "*", "observed": "blank row",
                "resolution": "excluded from canonical output", "metric_effect": "excluded", "note": "",
            })
            continue
        old = dict(source)
        row = dict(source)
        key = row["candidate_id"]
        reason = "metadata_normalization_only"
        eligible = "yes"
        gaps: list[str] = []
        row["reviewer"] = FINAL_REVIEWER
        row["reviewed_at"] = normalize_reviewed_at(old["reviewed_at"])
        if key == INTERNAL_MERGED_ID:
            row["review_class"] = "merged_target"
            row["dominant_semantic"] = "merged"
            row["review_note"] = "two people merged into one candidate ROI"
            reason = "explicit_2026-09-27_merged_target_adjudication"
        elif key in INTERNAL_UNCERTAIN_IDS:
            row["review_class"] = "uncertain"
            row["dominant_semantic"] = "uncertain"
            if not row["review_note"].strip():
                row["review_note"] = "human review could not resolve candidate semantics"
            eligible = "no"
            reason = "explicit_2026-09-27_uncertain_excluded_from_metrics"
            gaps.append("uncertain_semantics")
        if row["review_class"] == "background_fragment" and not row["review_note"].strip():
            gaps.append("background_note_missing")
            conflicts.append({
                "dataset": "internal8_to4", "row_key": key, "source_row_number": str(row_number),
                "severity": "open", "code": "background_note_missing", "field": "review_note",
                "observed": "", "resolution": "preserved blank; audit gap retained",
                "metric_effect": "included_as_human_background_with_open_note_gap", "note": "",
            })
        row_changes = changes(old, row, fields)
        row.update({
            "source_row_number": str(row_number),
            "source_manifest_sha256": manifest_hash,
            "review_basis_canonical": FINAL_BASIS,
            "review_basis_source": old["review_basis"],
            "normalized_at": FINAL_DATE,
            "original_review_class": old["review_class"],
            "original_dominant_semantic": old["dominant_semantic"],
            "original_reviewer": old["reviewer"],
            "original_reviewed_at": old["reviewed_at"],
            "original_review_basis": old["review_basis"],
            "adjudication_status": "changed" if row_changes else "unchanged",
            "adjudication_reason": reason,
            "metric_eligible": eligible,
            "audit_gap_codes": "|".join(gaps),
        })
        if row_changes:
            decisions.append({"dataset": "internal8_to4", "row_key": key,
                              "source_row_number": row_number, "reason": reason, "changes": row_changes})
        if key == INTERNAL_MERGED_ID or key in INTERNAL_UNCERTAIN_IDS:
            conflicts.append({
                "dataset": "internal8_to4", "row_key": key, "source_row_number": str(row_number),
                "severity": "resolved", "code": "explicit_adjudication", "field": "review_class",
                "observed": old["review_class"], "resolution": row["review_class"],
                "metric_effect": "included" if eligible == "yes" else "excluded",
                "note": reason,
            })
        output.append(row)
    if {row["candidate_id"] for row in output if row["metric_eligible"] == "no"} != INTERNAL_UNCERTAIN_IDS:
        raise AssertionError("only the three approved uncertain rows may be metric-ineligible")
    return output, decisions, conflicts, blank_count


def counts(rows: list[dict[str, str]], field: str) -> dict[str, int]:
    return dict(sorted(Counter(row[field] for row in rows).items()))


def run(project: Path, output_dir: Path) -> dict[str, Any]:
    project = project.resolve()
    fill_path = ensure_under(project / FILL_REL, project, "fill manifest")
    fill_receipt_path = ensure_under(project / FILL_RECEIPT_REL, project, "fill receipt")
    internal_path = ensure_under(project / INTERNAL_REL, project, "internal manifest")
    internal_receipt_path = ensure_under(project / INTERNAL_RECEIPT_REL, project, "internal receipt")
    output_dir = ensure_under(output_dir, project, "output directory")
    if output_dir != (project / DEFAULT_OUT_REL).resolve():
        raise ValueError(f"output must be the sealed finalized directory: {project / DEFAULT_OUT_REL}")
    output_dir.mkdir(parents=True, exist_ok=True)

    fill_fields, fill_source = read_csv(fill_path)
    internal_fields, internal_source = read_csv(internal_path)
    validate_split(fill_source, "fill")
    validate_split([r for r in internal_source if any((v or "").strip() for v in r.values())], "internal")
    fill_receipt, fill_checks = verify_fill_sources(project, fill_path, fill_receipt_path, fill_source)
    known_videos = fill_receipt["input_receipts"]["videos"]
    internal_receipt, internal_checks = verify_internal_sources(
        project, internal_path, internal_receipt_path,
        [r for r in internal_source if any((v or "").strip() for v in r.values())], known_videos,
    )

    fill_hash = sha256(fill_path)
    internal_hash = sha256(internal_path)
    fill_rows, fill_decisions, fill_conflicts = finalize_fill(fill_fields, fill_source, fill_hash)
    internal_rows, internal_decisions, internal_conflicts, blank_count = finalize_internal(
        internal_fields, internal_source, internal_hash
    )

    fill_out = output_dir / "fill_only_adjudicated.csv"
    internal_out = output_dir / "internal8_adjudicated.csv"
    adjudications_out = output_dir / "adjudications.json"
    conflicts_out = output_dir / "conflicts.csv"
    summary_out = output_dir / "summary.json"
    hashes_out = output_dir / "artifact_hashes.json"
    receipt_out = output_dir / "receipt.json"

    write_csv(fill_out, fill_fields + APPENDED_FIELDS, fill_rows)
    write_csv(internal_out, internal_fields + INTERNAL_APPENDED_FIELDS, internal_rows)
    conflict_fields = ["dataset", "row_key", "source_row_number", "severity", "code", "field",
                       "observed", "resolution", "metric_effect", "note"]
    all_conflicts = fill_conflicts + internal_conflicts
    write_csv(conflicts_out, conflict_fields, all_conflicts)
    canonical_json(adjudications_out, {
        "contract": "explicit human adjudications plus metadata normalization; source manifests unchanged",
        "normalized_at": FINAL_DATE,
        "fill_only": fill_decisions,
        "internal8": internal_decisions,
    })
    background_gap_count = sum("background_note_missing" in r["audit_gap_codes"] for r in internal_rows)
    summary = {
        "status": "human_review_finalized_development_evidence_not_training_import",
        "normalized_at": FINAL_DATE,
        "fill_only_T100": {
            "rows": len(fill_rows),
            "review_class": counts(fill_rows, "review_class"),
            "crop_usable": counts(fill_rows, "crop_usable"),
            "same_frame_new_target": counts(fill_rows, "same_frame_new_target"),
            "duplicate_of_baseline": counts(fill_rows, "duplicate_of_baseline"),
            "metric_eligible": counts(fill_rows, "metric_eligible"),
            "approved_total_assertions": {
                "ped_full": 19, "ped_truncated": 14, "background_fragment": 21,
                "crop_usable_yes": 24, "crop_usable_no": 30,
            },
        },
        "internal8_to4": {
            "substantive_rows": len(internal_rows),
            "ignored_blank_rows": blank_count,
            "review_class": counts(internal_rows, "review_class"),
            "metric_eligible": counts(internal_rows, "metric_eligible"),
            "merged_candidate_id": INTERNAL_MERGED_ID,
            "uncertain_excluded_candidate_ids": sorted(INTERNAL_UNCERTAIN_IDS),
            "background_note_missing_open_gaps": background_gap_count,
        },
        "conflicts": {
            "rows": len(all_conflicts),
            "by_severity": dict(sorted(Counter(r["severity"] for r in all_conflicts).items())),
            "open_audit_gaps": sum(r["severity"] == "open" for r in all_conflicts),
        },
        "boundary": (
            "Development train/validation review only. Uncertain internal8 rows are excluded from metrics. "
            "No test/blind/holdout data were accepted and no reviewed row was imported into training."
        ),
    }
    canonical_json(summary_out, summary)

    script_hash = sha256(Path(__file__).resolve())
    core_outputs = [fill_out, internal_out, adjudications_out, conflicts_out, summary_out]
    artifact_hashes = {
        "schema_version": 2,
        "script": {"path": str(Path(__file__).resolve()), "sha256": script_hash},
        "inputs": {
            "fill_manifest": {"path": str(fill_path), "sha256": fill_hash},
            "fill_receipt": {"path": str(fill_receipt_path), "sha256": sha256(fill_receipt_path)},
            "internal_manifest": {"path": str(internal_path), "sha256": internal_hash},
            "internal_receipt": {"path": str(internal_receipt_path), "sha256": sha256(internal_receipt_path)},
        },
        "outputs": {path.name: sha256(path) for path in core_outputs},
    }
    canonical_json(hashes_out, artifact_hashes)
    receipt = {
        "status": "complete_hash_verified_human_review_finalization",
        "schema_version": 2,
        "normalized_at": FINAL_DATE,
        "script": artifact_hashes["script"],
        "inputs": artifact_hashes["inputs"],
        "input_hash_verification": {
            "fill_checks": fill_checks,
            "internal_checks": internal_checks,
            "fill_blank_template_manifest_sha256": fill_receipt["outputs"]["review_manifest"]["sha256"],
            "fill_reviewed_manifest_differs_from_blank_template": True,
            "internal_blank_template_manifest_sha256": internal_receipt["outputs"]["review_manifest_sha256"],
            "internal_reviewed_manifest_differs_from_blank_template": True,
        },
        "outputs": {
            **artifact_hashes["outputs"],
            hashes_out.name: sha256(hashes_out),
        },
        "assertions": {
            "fill_expected_counts_pass": True,
            "internal_blank_row_ignored": blank_count == 1,
            "uncertain_rows_excluded_exactly": sorted(INTERNAL_UNCERTAIN_IDS),
            "all_source_and_review_image_hashes_verified": True,
            "sealed_split_guard_pass": True,
        },
        "boundary": summary["boundary"],
    }
    canonical_json(receipt_out, receipt)
    return {**summary, "output_dir": str(output_dir), "receipt_sha256": sha256(receipt_out)}


def self_test() -> None:
    assert has_sealed_token("foo/blind/bar")
    assert has_sealed_token("candidate_test.csv")
    assert not has_sealed_token("latest_candidate.csv")
    assert not has_sealed_token("contest_data")
    assert normalize_reviewed_at("2026/9/27") == "2026-09-27"
    assert normalize_reviewed_at("2026-09-27") == "2026-09-27"
    assert normalize_reviewed_at("YYYY-MM-DD") == ""
    assert normalize_reviewed_at("") == ""
    assert set(FILL_ADJUDICATIONS) == {
        "gf0004", "gf0005", "gf0006", "gf0010", "gf0011", "gf0012", "gf0023", "gf0025",
        "gf0037", "gf0042", "gf0044", "gf0045", "gf0048", "gf0049", "gf0050", "gf0051",
        "gf0052", "gf0053",
    }
    assert len(INTERNAL_UNCERTAIN_IDS) == 3
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        inside = root / "train" / "x.csv"
        inside.parent.mkdir()
        inside.write_text("x", encoding="utf-8")
        assert ensure_under(inside, root, "self-test") == inside.resolve()
        try:
            ensure_under(root / "blind" / "x.csv", root, "self-test")
        except ValueError:
            pass
        else:
            raise AssertionError("sealed path guard did not reject blind")
    print("SELF_TEST_PASS")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    default_project = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=default_project)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.self_test:
        self_test()
        return 0
    project = args.project_root.resolve()
    output = args.output.resolve() if args.output else (project / DEFAULT_OUT_REL).resolve()
    result = run(project, output)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
