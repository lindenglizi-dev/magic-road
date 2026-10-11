#!/usr/bin/env python3
"""Import and analyse the reviewed VIRAT 010107 development-scene workbook.

The reviewer returned an OOXML workbook with a misleading ``.csv`` suffix.  This
tool detects the file by magic, opens it from ``BytesIO``, verifies every
non-human field against the sealed source manifest, and emits a canonical,
traceable review package.  It never discovers inputs by directory traversal.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import io
import json
import math
import re
import shutil
import sys
import zipfile
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

try:
    import openpyxl
except ImportError as exc:  # pragma: no cover - environment error is explicit
    raise SystemExit("openpyxl is required; use the bundled workspace Python") from exc


TOOL_VERSION = "1.0"
EXPECTED_ROW_COUNT = 83
SHEET_NAME = "review_manifest"
OOXML_MAGIC = b"PK\x03\x04"

HUMAN_FIELDS = (
    "review_class",
    "candidate_condition",
    "crop_usable",
    "occlusion",
    "truncation_reason",
    "same_frame_new_target",
    "duplicate_of_baseline",
    "duplicate_baseline_number",
    "reviewer",
    "reviewed_at",
    "review_basis",
    "review_note",
)

EXPECTED_RESULTS = {
    "trainable_small_semantic": (8, 30),
    "trainable_scene_semantic": (26, 83),
    "all_real_small_semantic": (9, 30),
    "all_real_scene_semantic": (30, 83),
    "rider_bicycle_count": 4,
    "ped_crop_usable": (26, 26),
    "vehicle_count": 0,
    "hog64_ped_correct": (9, 26),
    "hog324_q_ped_correct": (11, 26),
    "invalid_count": 53,
    "float_q_prediction_mismatch": 0,
}

CONDITION_MAP = {
    "background": "background_fragment",
    "background_fragment": "background_fragment",
    "complete": "complete",
    "truncated": "truncated",
    "merged": "merged",
    "other": "other",
}

REVIEW_BASIS_MAP = {
    "human_visual_review": "human_visual_review",
    "human visual review": "human_visual_review",
    "human-review": "human_visual_review",
}

SEALED_PATH_MARKERS = ("blind_reserve", "holdout")


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def assert_development_path(path: Path) -> None:
    text = str(path).replace("\\", "/").lower()
    if any(marker in text for marker in SEALED_PATH_MARKERS):
        raise ValueError(f"sealed input/output path rejected: {path}")


def workbook_rows_from_bytes(payload: bytes) -> tuple[list[str], list[dict[str, Any]]]:
    if not payload.startswith(OOXML_MAGIC):
        raise ValueError("review source is not OOXML: missing PK magic")
    with zipfile.ZipFile(io.BytesIO(payload), "r") as archive:
        names = set(archive.namelist())
        if "[Content_Types].xml" not in names or "xl/workbook.xml" not in names:
            raise ValueError("PK file is not an OOXML workbook")
    workbook = openpyxl.load_workbook(io.BytesIO(payload), read_only=True, data_only=False)
    try:
        if workbook.sheetnames != [SHEET_NAME]:
            raise ValueError(
                f"workbook must contain exactly [{SHEET_NAME!r}], got {workbook.sheetnames!r}"
            )
        worksheet = workbook[SHEET_NAME]
        values = list(worksheet.iter_rows(values_only=True))
    finally:
        workbook.close()
    if not values:
        raise ValueError("review workbook is empty")
    headers = ["" if value is None else str(value) for value in values[0]]
    if len(headers) != len(set(headers)):
        raise ValueError("review workbook has duplicate headers")
    rows = [dict(zip(headers, row)) for row in values[1:]]
    return headers, rows


def read_reference_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        headers = list(reader.fieldnames or [])
        rows = [dict(row) for row in reader]
    if not headers:
        raise ValueError("reference manifest has no header")
    return headers, rows


_NUMERIC_RE = re.compile(r"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?$")


def display_cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, dt.datetime):
        return value.isoformat(sep=" ")
    if isinstance(value, dt.date):
        return value.isoformat()
    return str(value)


def semantic_equal(left: Any, right: Any) -> bool:
    a = display_cell(left).strip()
    b = display_cell(right).strip()
    if a == b:
        return True
    if not (_NUMERIC_RE.fullmatch(a) and _NUMERIC_RE.fullmatch(b)):
        return False
    try:
        return Decimal(a) == Decimal(b)
    except InvalidOperation:
        return False


def canonical_date(value: Any) -> str:
    if isinstance(value, dt.datetime):
        return value.date().isoformat()
    if isinstance(value, dt.date):
        return value.isoformat()
    text = display_cell(value).strip()
    if not text:
        raise ValueError("reviewed_at is blank")
    for parser in (
        lambda s: dt.datetime.fromisoformat(s).date(),
        lambda s: dt.datetime.strptime(s, "%Y/%m/%d").date(),
        lambda s: dt.datetime.strptime(s, "%m/%d/%Y").date(),
    ):
        try:
            return parser(text).isoformat()
        except ValueError:
            pass
    raise ValueError(f"unsupported reviewed_at value: {text!r}")


def canonical_basis(value: Any) -> str:
    text = display_cell(value).strip().lower()
    try:
        return REVIEW_BASIS_MAP[text]
    except KeyError as exc:
        raise ValueError(f"unsupported review_basis value: {value!r}") from exc


def validate_and_canonicalize(
    workbook_headers: Sequence[str],
    workbook_rows: Sequence[Mapping[str, Any]],
    reference_headers: Sequence[str],
    reference_rows: Sequence[Mapping[str, str]],
) -> tuple[list[str], list[dict[str, str]], dict[str, Any]]:
    if list(workbook_headers) != list(reference_headers):
        raise ValueError("workbook headers differ from the source review manifest")
    if len(workbook_rows) != EXPECTED_ROW_COUNT or len(reference_rows) != EXPECTED_ROW_COUNT:
        raise ValueError(
            f"expected {EXPECTED_ROW_COUNT} workbook and reference rows, got "
            f"{len(workbook_rows)} and {len(reference_rows)}"
        )
    missing_human = [field for field in HUMAN_FIELDS if field not in reference_headers]
    if missing_human:
        raise ValueError(f"reference manifest lacks human fields: {missing_human}")
    immutable_fields = [field for field in reference_headers if field not in HUMAN_FIELDS]
    if "sample_id" not in immutable_fields:
        raise ValueError("sample_id is not an immutable field")

    wb_ids = [display_cell(row.get("sample_id")).strip() for row in workbook_rows]
    ref_ids = [str(row.get("sample_id", "")).strip() for row in reference_rows]
    if len(set(wb_ids)) != EXPECTED_ROW_COUNT or len(set(ref_ids)) != EXPECTED_ROW_COUNT:
        raise ValueError("sample_id values are blank or duplicated")
    if wb_ids != ref_ids:
        missing = sorted(set(ref_ids) - set(wb_ids))
        extra = sorted(set(wb_ids) - set(ref_ids))
        raise ValueError(f"ordered sample_id mismatch; missing={missing}, extra={extra}")

    differences: list[dict[str, str]] = []
    for wb_row, ref_row in zip(workbook_rows, reference_rows):
        sample_id = str(ref_row["sample_id"])
        for field in immutable_fields:
            if not semantic_equal(wb_row.get(field), ref_row.get(field)):
                differences.append(
                    {
                        "sample_id": sample_id,
                        "field": field,
                        "workbook": display_cell(wb_row.get(field)),
                        "reference": str(ref_row.get(field, "")),
                    }
                )
    if differences:
        preview = differences[:5]
        raise ValueError(
            f"{len(differences)} immutable-field differences; first differences={preview!r}"
        )

    output_headers = list(reference_headers)
    review_class_index = output_headers.index("review_class") + 1
    output_headers.insert(review_class_index, "semantic_subtype")
    condition_index = output_headers.index("candidate_condition") + 1
    output_headers.insert(condition_index, "source_candidate_condition")
    canonical_rows: list[dict[str, str]] = []
    normalized_background = 0

    for wb_row, ref_row in zip(workbook_rows, reference_rows):
        row: dict[str, str] = {field: str(ref_row.get(field, "")) for field in immutable_fields}
        for field in HUMAN_FIELDS:
            row[field] = display_cell(wb_row.get(field)).strip()

        review_class = row["review_class"].lower()
        if review_class not in {"ped", "vehicle", "invalid", "ignore"}:
            raise ValueError(f"{row['sample_id']}: unsupported review_class {review_class!r}")
        row["review_class"] = review_class
        row["semantic_subtype"] = "rider_bicycle" if review_class == "ignore" else ""

        source_condition = row["candidate_condition"].lower()
        if source_condition not in CONDITION_MAP:
            raise ValueError(
                f"{row['sample_id']}: unsupported candidate_condition {source_condition!r}"
            )
        canonical_condition = CONDITION_MAP[source_condition]
        row["source_candidate_condition"] = source_condition
        row["candidate_condition"] = canonical_condition
        normalized_background += int(source_condition == "background")

        row["crop_usable"] = row["crop_usable"].lower()
        row["occlusion"] = row["occlusion"].lower()
        row["truncation_reason"] = row["truncation_reason"].lower()
        row["same_frame_new_target"] = row["same_frame_new_target"].lower()
        row["duplicate_of_baseline"] = row["duplicate_of_baseline"].lower()
        if row["crop_usable"] not in {"yes", "no"}:
            raise ValueError(f"{row['sample_id']}: crop_usable must be yes/no")
        if row["occlusion"] not in {"none", "yes", "partial"}:
            raise ValueError(f"{row['sample_id']}: unsupported occlusion")
        if row["truncation_reason"] not in {"none", "crop_tight", "frame_edge", "other"}:
            raise ValueError(f"{row['sample_id']}: unsupported truncation_reason")
        for field in ("same_frame_new_target", "duplicate_of_baseline"):
            if row[field] not in {"yes", "no"}:
                raise ValueError(f"{row['sample_id']}: {field} must be yes/no")
        duplicate_number = row["duplicate_baseline_number"]
        if row["duplicate_of_baseline"] == "yes":
            if not re.fullmatch(r"B[0-3]", duplicate_number):
                raise ValueError(f"{row['sample_id']}: invalid duplicate_baseline_number")
        elif duplicate_number:
            raise ValueError(f"{row['sample_id']}: duplicate number present when duplicate=no")
        if not row["reviewer"]:
            raise ValueError(f"{row['sample_id']}: reviewer is blank")
        row["reviewed_at"] = canonical_date(wb_row.get("reviewed_at"))
        row["review_basis"] = canonical_basis(wb_row.get("review_basis"))
        canonical_rows.append({field: row.get(field, "") for field in output_headers})

    validation = {
        "row_count": len(canonical_rows),
        "sample_ids_unique": True,
        "sample_ids_ordered_exact_match": True,
        "immutable_field_count": len(immutable_fields),
        "immutable_cells_compared": len(immutable_fields) * len(canonical_rows),
        "immutable_differences": 0,
        "background_values_normalized": normalized_background,
    }
    return output_headers, canonical_rows, validation


def count_map(values: Iterable[str]) -> dict[str, int]:
    return dict(sorted(Counter(values).items()))


def cross_tab(rows: Sequence[Mapping[str, str]], left: str, right: str) -> dict[str, dict[str, int]]:
    table: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        table[row[left]][row[right]] += 1
    return {
        key: dict(sorted(counter.items())) for key, counter in sorted(table.items())
    }


def as_float(row: Mapping[str, str], field: str) -> float:
    try:
        result = float(row[field])
    except (KeyError, ValueError) as exc:
        raise ValueError(f"{row.get('sample_id')}: invalid numeric {field}") from exc
    if not math.isfinite(result):
        raise ValueError(f"{row.get('sample_id')}: non-finite {field}")
    return result


def threshold_scan(
    rows: Sequence[Mapping[str, str]],
    score_field: str,
    prediction_field: str,
    integer_score: bool,
) -> dict[str, Any]:
    ped_rows = [row for row in rows if row["review_class"] == "ped"]
    invalid_rows = [row for row in rows if row["review_class"] == "invalid"]
    values = [abs(as_float(row, score_field)) for row in rows]
    unique = sorted(set(values))
    if integer_score:
        thresholds = [0.0] + [float(int(value) + 1) for value in unique]
    else:
        thresholds = [0.0] + [math.nextafter(value, math.inf) for value in unique]
    thresholds = sorted(set(thresholds))
    points: list[dict[str, Any]] = []
    for threshold in thresholds:
        ped_correct = sum(
            row[prediction_field] == "ped" and abs(as_float(row, score_field)) >= threshold
            for row in ped_rows
        )
        invalid_accepted = sum(
            abs(as_float(row, score_field)) >= threshold for row in invalid_rows
        )
        ped_recall = ped_correct / len(ped_rows)
        invalid_far = invalid_accepted / len(invalid_rows)
        points.append(
            {
                "threshold": threshold,
                "ped_correct": ped_correct,
                "ped_total": len(ped_rows),
                "ped_recall": ped_recall,
                "invalid_accepted": invalid_accepted,
                "invalid_total": len(invalid_rows),
                "invalid_far": invalid_far,
                "meets_ped_recall_ge_0_85_and_invalid_far_le_0_10": (
                    ped_recall >= 0.85 and invalid_far <= 0.10
                ),
            }
        )
    feasible = [point for point in points if point["meets_ped_recall_ge_0_85_and_invalid_far_le_0_10"]]
    return {
        "rule": f"accept binary prediction iff abs({score_field}) >= threshold",
        "ped_recall_requirement": 0.85,
        "invalid_far_requirement": 0.10,
        "threshold_count": len(points),
        "feasible_point_count": len(feasible),
        "feasible_points": feasible,
        "points": points,
    }


def analyse(rows: Sequence[Mapping[str, str]]) -> tuple[dict[str, Any], list[dict[str, str]]]:
    classes = Counter(row["review_class"] for row in rows)
    small = [row for row in rows if row["branch"] == "small_component_experimental"]
    trainable_semantic = {"ped", "vehicle"}
    small_semantic = sum(row["review_class"] in trainable_semantic for row in small)
    scene_semantic = sum(row["review_class"] in trainable_semantic for row in rows)
    small_all_real = sum(
        row["review_class"] in trainable_semantic or row["semantic_subtype"] == "rider_bicycle"
        for row in small
    )
    scene_all_real = sum(
        row["review_class"] in trainable_semantic or row["semantic_subtype"] == "rider_bicycle"
        for row in rows
    )
    peds = [row for row in rows if row["review_class"] == "ped"]
    invalid = [row for row in rows if row["review_class"] == "invalid"]
    vehicles = [row for row in rows if row["review_class"] == "vehicle"]

    hog64_ped_correct = sum(row["hog64_prediction"] == "ped" for row in peds)
    hog324_q_ped_correct = sum(row["hog324_q_prediction"] == "ped" for row in peds)
    float_q_mismatch = [
        row for row in rows
        if row["hog324_float_prediction"] != row["hog324_q_prediction"]
    ]

    actual_contract = {
        "trainable_small_semantic": (small_semantic, len(small)),
        "trainable_scene_semantic": (scene_semantic, len(rows)),
        "all_real_small_semantic": (small_all_real, len(small)),
        "all_real_scene_semantic": (scene_all_real, len(rows)),
        "rider_bicycle_count": sum(row["semantic_subtype"] == "rider_bicycle" for row in rows),
        "ped_crop_usable": (sum(row["crop_usable"] == "yes" for row in peds), len(peds)),
        "vehicle_count": len(vehicles),
        "hog64_ped_correct": (hog64_ped_correct, len(peds)),
        "hog324_q_ped_correct": (hog324_q_ped_correct, len(peds)),
        "invalid_count": len(invalid),
        "float_q_prediction_mismatch": len(float_q_mismatch),
    }
    if actual_contract != EXPECTED_RESULTS:
        raise ValueError(
            f"predeclared review contract mismatch: actual={actual_contract!r}, "
            f"expected={EXPECTED_RESULTS!r}"
        )

    hog64_scan = threshold_scan(rows, "hog64_score", "hog64_prediction", False)
    hog324_q_scan = threshold_scan(
        rows, "hog324_q_score_integer", "hog324_q_prediction", True
    )
    if hog64_scan["feasible_point_count"] or hog324_q_scan["feasible_point_count"]:
        raise ValueError("unexpected feasible absolute-score rejection threshold")

    gates = {
        "trainable_small_semantic": {
            "numerator": small_semantic,
            "denominator": len(small),
            "rate": small_semantic / len(small),
            "requirement": 0.60,
            "pass": small_semantic / len(small) >= 0.60,
        },
        "trainable_scene_semantic": {
            "numerator": scene_semantic,
            "denominator": len(rows),
            "rate": scene_semantic / len(rows),
            "requirement": 0.50,
            "pass": scene_semantic / len(rows) >= 0.50,
        },
        "all_real_small_semantic": {
            "numerator": small_all_real,
            "denominator": len(small),
            "rate": small_all_real / len(small),
            "requirement": 0.60,
            "pass": small_all_real / len(small) >= 0.60,
            "includes": ["ped", "vehicle", "rider_bicycle"],
        },
        "all_real_scene_semantic": {
            "numerator": scene_all_real,
            "denominator": len(rows),
            "rate": scene_all_real / len(rows),
            "requirement": 0.50,
            "pass": scene_all_real / len(rows) >= 0.50,
            "includes": ["ped", "vehicle", "rider_bicycle"],
        },
        "ped_crop_usable": {
            "numerator": sum(row["crop_usable"] == "yes" for row in peds),
            "denominator": len(peds),
            "rate": sum(row["crop_usable"] == "yes" for row in peds) / len(peds),
            "requirement": 1.0,
            "pass": all(row["crop_usable"] == "yes" for row in peds),
        },
        "vehicle_evaluation": {
            "sample_count": len(vehicles),
            "status": "not_evaluable_missing_vehicle_reviews",
            "pass": None,
        },
    }

    failures: list[dict[str, str]] = []
    failure_fields = (
        "sample_id", "candidate_id", "frame_index", "branch", "interval_id",
        "review_class", "semantic_subtype", "source_candidate_condition", "candidate_condition",
        "crop_usable", "hog64_score", "hog64_prediction",
        "hog324_float_score", "hog324_float_prediction",
        "hog324_q_score_integer", "hog324_q_prediction", "review_note",
    )
    for row in rows:
        reasons: list[str] = []
        if row["review_class"] == "ped":
            if row["hog64_prediction"] != "ped":
                reasons.append("ped_hog64_miss")
            if row["hog324_q_prediction"] != "ped":
                reasons.append("ped_hog324_q_miss")
        elif row["review_class"] == "invalid":
            reasons.extend(("invalid_hog64_false_accept", "invalid_hog324_q_false_accept"))
        if row["hog324_float_prediction"] != row["hog324_q_prediction"]:
            reasons.append("hog324_float_q_prediction_mismatch")
        if reasons:
            item = {field: row[field] for field in failure_fields}
            item["failure_reasons"] = "|".join(reasons)
            failures.append(item)

    invalid_notes = [row for row in invalid if row["review_note"].strip()]
    analysis = {
        "counts": {
            "rows": len(rows),
            "branch": count_map(row["branch"] for row in rows),
            "interval": count_map(row["interval_id"] for row in rows),
            "review_class": count_map(row["review_class"] for row in rows),
            "semantic_subtype_nonblank": count_map(
                row["semantic_subtype"] for row in rows if row["semantic_subtype"]
            ),
            "candidate_condition": count_map(row["candidate_condition"] for row in rows),
            "source_candidate_condition": count_map(
                row["source_candidate_condition"] for row in rows
            ),
            "crop_usable": count_map(row["crop_usable"] for row in rows),
            "branch_by_class": cross_tab(rows, "branch", "review_class"),
            "interval_by_class": cross_tab(rows, "interval_id", "review_class"),
        },
        "predeclared_gates": gates,
        "model_diagnostics": {
            "hog64_ped_correct": {
                "correct": hog64_ped_correct,
                "total": len(peds),
                "rate": hog64_ped_correct / len(peds),
            },
            "hog324_q_ped_correct": {
                "correct": hog324_q_ped_correct,
                "total": len(peds),
                "rate": hog324_q_ped_correct / len(peds),
            },
            "binary_invalid_far": {
                "hog64": {"accepted": len(invalid), "total": len(invalid), "far": 1.0},
                "hog324_q": {"accepted": len(invalid), "total": len(invalid), "far": 1.0},
                "interpretation": "binary classifiers have no rejection at their native decision",
            },
            "hog324_float_q_prediction_mismatch": {
                "count": len(float_q_mismatch),
                "total": len(rows),
                "sample_ids": [row["sample_id"] for row in float_q_mismatch],
            },
            "absolute_score_threshold_scan": {
                "hog64": hog64_scan,
                "hog324_q": hog324_q_scan,
            },
            "excluded_population": {
                "review_class": "ignore",
                "semantic_subtype": "rider_bicycle",
                "count": sum(row["semantic_subtype"] == "rider_bicycle" for row in rows),
                "reason": "retained as a real semantic candidate but excluded from ped/vehicle training and classification metrics",
            },
        },
        "background_false_positive_observation": {
            "invalid_rows": len(invalid),
            "invalid_rows_with_nonblank_review_note": len(invalid_notes),
            "user_aggregate_observation": "多数背景来自移动影子或停车线",
            "quantification_status": "not_quantified_per_candidate",
            "restriction": (
                "The aggregate observation is retained verbatim but no shadow/parking-line/other "
                "subcategory is assigned because the manifest does not contain per-row subtype labels."
            ),
        },
        "failure_sample_count": len(failures),
    }
    return analysis, failures


def write_csv(path: Path, headers: Sequence[str], rows: Sequence[Mapping[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(headers), extrasaction="raise")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def decision_markdown(analysis: Mapping[str, Any]) -> str:
    gates = analysis["predeclared_gates"]
    models = analysis["model_diagnostics"]
    lines = [
        "# VIRAT 010107 T100 人工审核决策",
        "",
        "## 完整性",
        "",
        "- 已验证 83 个 `sample_id` 与原清单顺序、集合完全一致。",
        "- 已逐单元格比较全部非人工字段，差异为 0。",
        "- 原始 OOXML 文件按字节保存，规范化只发生在派生清单。",
        "",
        "## 预声明门禁",
        "",
        (
            f"- 可训练人车语义，small 分支：{gates['trainable_small_semantic']['numerator']}/"
            f"{gates['trainable_small_semantic']['denominator']} "
            f"（{gates['trainable_small_semantic']['rate']:.2%}），未达到 60%。"
        ),
        (
            f"- 可训练人车语义，全场景：{gates['trainable_scene_semantic']['numerator']}/"
            f"{gates['trainable_scene_semantic']['denominator']} "
            f"（{gates['trainable_scene_semantic']['rate']:.2%}），未达到 50%。"
        ),
        (
            f"- 含骑行者的全部真实语义，small 分支：{gates['all_real_small_semantic']['numerator']}/"
            f"{gates['all_real_small_semantic']['denominator']} "
            f"（{gates['all_real_small_semantic']['rate']:.2%}），未达到 60%。"
        ),
        (
            f"- 含骑行者的全部真实语义，全场景：{gates['all_real_scene_semantic']['numerator']}/"
            f"{gates['all_real_scene_semantic']['denominator']} "
            f"（{gates['all_real_scene_semantic']['rate']:.2%}），未达到 50%。"
        ),
        (
            f"- 行人裁剪可用：{gates['ped_crop_usable']['numerator']}/"
            f"{gates['ped_crop_usable']['denominator']}。"
        ),
        "- 车辆样本为 0，本场景不能评价车辆召回。",
        "",
        "## 模型诊断",
        "",
        (
            f"- HOG64 行人正确：{models['hog64_ped_correct']['correct']}/"
            f"{models['hog64_ped_correct']['total']}。"
        ),
        (
            f"- HOG324-Q 行人正确：{models['hog324_q_ped_correct']['correct']}/"
            f"{models['hog324_q_ped_correct']['total']}。"
        ),
        "- 两个二分类器对 invalid 候选的原生误接受率均为 100%。",
        "- 在 `Person Recall >= 85%` 且 `invalid FAR <= 10%` 的联合条件下，两个绝对分数阈值扫描均无可行点。",
        (
            f"- HOG324 浮点/定点分类不一致："
            f"{models['hog324_float_q_prediction_mismatch']['count']}/83。"
        ),
        "",
        "## 决策边界",
        "",
        (
            "这批人工审核可以用于开发诊断和失败案例分析，但未通过候选语义率门禁，且没有车辆样本，"
            "不能据此宣布分类器或候选策略达标。用户观察“多数背景来自移动影子或停车线”按聚合观察保留；"
            "由于未提供逐候选子类标签，本报告不分配或统计移动影子、停车线及其他背景子类。"
        ),
        (
            "4 个骑自行车的人保留为 `review_class=ignore, semantic_subtype=rider_bicycle`，"
            "不进入人车训练或模型指标。"
        ),
        "",
    ]
    markdown = "\n".join(lines)
    if 'f"' in markdown or any(line.startswith('"') for line in markdown.splitlines()):
        raise RuntimeError("decision markdown contains template residue")
    return markdown


def refresh_decision_and_receipt(output_dir: Path) -> dict[str, Any]:
    """Refresh only DECISION.md and receipt.json after validating sealed artifacts."""
    assert_development_path(output_dir)
    report_path = output_dir / "report.json"
    receipt_path = output_dir / "receipt.json"
    decision_path = output_dir / "DECISION.md"
    if not report_path.is_file() or not receipt_path.is_file():
        raise ValueError("refresh requires existing report.json and receipt.json")
    prior_receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    expected_names = {
        "source_review_file.xlsx",
        "canonical_review_manifest.csv",
        "report.json",
        "failure_samples.csv",
        "DECISION.md",
    }
    if set(prior_receipt.get("artifact_hashes", {})) != expected_names:
        raise ValueError("existing receipt artifact set is incomplete or unexpected")
    for name, expected_hash in prior_receipt["artifact_hashes"].items():
        if sha256_path(output_dir / name) != expected_hash:
            raise ValueError(f"refusing refresh: existing artifact hash mismatch for {name}")

    report = json.loads(report_path.read_text(encoding="utf-8"))
    markdown = decision_markdown(report)
    decision_path.write_text(markdown, encoding="utf-8")

    script_path = Path(__file__).resolve()
    artifact_hashes = {
        name: sha256_path(output_dir / name) for name in sorted(expected_names)
    }
    receipt = {
        "schema": "virat_scene_review_import_receipt_v1",
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "refresh_mode": "decision_and_receipt_only",
        "source_review_sha256": prior_receipt["source_review_sha256"],
        "reference_manifest_sha256": prior_receipt["reference_manifest_sha256"],
        "report_producer_script_sha256": report["inputs"]["script"]["sha256"],
        "script_sha256": sha256_path(script_path),
        "row_count": prior_receipt["row_count"],
        "artifact_hashes": artifact_hashes,
        "receipt_self_hash_included": False,
    }
    write_json(receipt_path, receipt)
    parsed_receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    for name, expected_hash in parsed_receipt["artifact_hashes"].items():
        if sha256_path(output_dir / name) != expected_hash:
            raise RuntimeError(f"artifact readback hash mismatch for {name}")
    return {
        "output_dir": str(output_dir.resolve()),
        "receipt_sha256": sha256_path(receipt_path),
        "decision_sha256": sha256_path(decision_path),
        "script_sha256": sha256_path(script_path),
        "refreshed_files": ["DECISION.md", "receipt.json"],
    }


def build_package(source: Path, reference: Path, output_dir: Path) -> dict[str, Any]:
    for path in (source, reference, output_dir):
        assert_development_path(path)
    source_bytes = source.read_bytes()
    source_sha = sha256_bytes(source_bytes)
    workbook_headers, workbook_rows = workbook_rows_from_bytes(source_bytes)
    reference_headers, reference_rows = read_reference_csv(reference)
    output_headers, canonical_rows, validation = validate_and_canonicalize(
        workbook_headers, workbook_rows, reference_headers, reference_rows
    )
    analysis, failures = analyse(canonical_rows)

    output_dir.mkdir(parents=True, exist_ok=True)
    source_copy = output_dir / "source_review_file.xlsx"
    canonical_path = output_dir / "canonical_review_manifest.csv"
    report_path = output_dir / "report.json"
    failures_path = output_dir / "failure_samples.csv"
    decision_path = output_dir / "DECISION.md"
    receipt_path = output_dir / "receipt.json"

    source_copy.write_bytes(source_bytes)
    if sha256_path(source_copy) != source_sha:
        raise RuntimeError("source workbook copy hash mismatch")
    write_csv(canonical_path, output_headers, canonical_rows)
    failure_headers = [
        "sample_id", "candidate_id", "frame_index", "branch", "interval_id",
        "review_class", "semantic_subtype", "source_candidate_condition", "candidate_condition",
        "crop_usable", "hog64_score", "hog64_prediction", "hog324_float_score",
        "hog324_float_prediction", "hog324_q_score_integer", "hog324_q_prediction",
        "review_note", "failure_reasons",
    ]
    write_csv(failures_path, failure_headers, failures)

    script_path = Path(__file__).resolve()
    report = {
        "schema": "virat_scene_review_import_report_v1",
        "tool_version": TOOL_VERSION,
        "scope": {
            "scene": "VIRAT_S_010107_02_000282_000312",
            "strategy": "fill_only_T100 development review",
            "development_only": True,
            "training_performed": False,
            "threshold_tuning_performed": False,
            "blind_or_holdout_accessed": False,
        },
        "inputs": {
            "source_review_file": {
                "original_path": str(source.resolve()),
                "sha256": source_sha,
                "size_bytes": len(source_bytes),
                "detected_format": "OOXML workbook by PK magic",
                "sheet": SHEET_NAME,
                "exact_copy": "source_review_file.xlsx",
            },
            "reference_manifest": {
                "path": str(reference.resolve()),
                "sha256": sha256_path(reference),
            },
            "script": {"path": str(script_path), "sha256": sha256_path(script_path)},
        },
        "integrity_validation": validation,
        "normalization": {
            "candidate_condition": {
                "source_value_preserved_in": "source_candidate_condition",
                "mapping": {"background": "background_fragment"},
            },
            "reviewed_at": "ISO-8601 date YYYY-MM-DD",
            "review_basis": "human_visual_review",
            "semantic_subtype": {
                "rule": "review_class=ignore -> rider_bicycle for the four user-clarified rows",
                "clarification_source": "user_message_2026-09-28",
                "training_and_model_metrics": "excluded",
            },
        },
        **analysis,
        "limitations": [
            "This is a single development scene and contains no reviewed vehicle examples.",
            "The four rider_bicycle rows remain review_class=ignore and are excluded from ped/vehicle training and model metrics.",
            "Scores were imported from the existing frozen diagnostic run; no retraining occurred.",
            "Absolute-score scans are rejection diagnostics, not probability calibration.",
            "The aggregate background observation has not been labelled per candidate.",
        ],
    }
    write_json(report_path, report)
    decision_path.write_text(decision_markdown(analysis), encoding="utf-8")

    artifact_paths = [source_copy, canonical_path, report_path, failures_path, decision_path]
    artifact_hashes = {path.name: sha256_path(path) for path in artifact_paths}
    receipt = {
        "schema": "virat_scene_review_import_receipt_v1",
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "source_review_sha256": source_sha,
        "reference_manifest_sha256": sha256_path(reference),
        "script_sha256": sha256_path(script_path),
        "row_count": len(canonical_rows),
        "artifact_hashes": artifact_hashes,
        "receipt_self_hash_included": False,
    }
    write_json(receipt_path, receipt)

    # Independent readback: the receipt is deliberately excluded from its own map.
    parsed_receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    for name, expected_hash in parsed_receipt["artifact_hashes"].items():
        actual_hash = sha256_path(output_dir / name)
        if actual_hash != expected_hash:
            raise RuntimeError(f"artifact readback hash mismatch for {name}")
    if parsed_receipt["script_sha256"] != sha256_path(script_path):
        raise RuntimeError("script readback hash mismatch")
    return {
        "output_dir": str(output_dir.resolve()),
        "receipt_sha256": sha256_path(receipt_path),
        "source_sha256": source_sha,
        "rows": len(canonical_rows),
        "failures": len(failures),
        "artifact_hashes": artifact_hashes,
    }


def self_test() -> None:
    assert semantic_equal(1, "1.0")
    assert semantic_equal("-2.500", -2.5)
    assert not semantic_equal("B01", "B1")
    assert canonical_date(dt.datetime(2026, 9, 28, 0, 0)) == "2026-09-28"
    assert canonical_basis("Human Visual Review") == "human_visual_review"
    assert CONDITION_MAP["background"] == "background_fragment"
    try:
        workbook_rows_from_bytes(b"sample_id,x\na,1\n")
    except ValueError as exc:
        assert "PK magic" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("plain CSV must be rejected")

    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = SHEET_NAME
    worksheet.append(["sample_id", "value"])
    worksheet.append(["vr00000", 1])
    memory = io.BytesIO()
    workbook.save(memory)
    workbook.close()
    headers, rows = workbook_rows_from_bytes(memory.getvalue())
    assert headers == ["sample_id", "value"]
    assert rows[0]["sample_id"] == "vr00000"

    try:
        assert_development_path(Path("x/blind_reserve/y"))
    except ValueError:
        pass
    else:  # pragma: no cover
        raise AssertionError("sealed path must be rejected")
    sample_analysis = {
        "predeclared_gates": {
            "trainable_small_semantic": {"numerator": 8, "denominator": 30, "rate": 8 / 30},
            "trainable_scene_semantic": {"numerator": 26, "denominator": 83, "rate": 26 / 83},
            "all_real_small_semantic": {"numerator": 9, "denominator": 30, "rate": 9 / 30},
            "all_real_scene_semantic": {"numerator": 30, "denominator": 83, "rate": 30 / 83},
            "ped_crop_usable": {"numerator": 26, "denominator": 26},
        },
        "model_diagnostics": {
            "hog64_ped_correct": {"correct": 9, "total": 26},
            "hog324_q_ped_correct": {"correct": 11, "total": 26},
            "hog324_float_q_prediction_mismatch": {"count": 0},
        },
    }
    markdown = decision_markdown(sample_analysis)
    assert markdown.startswith("# VIRAT 010107 T100 人工审核决策\n")
    assert 'f"' not in markdown
    assert not any(line.startswith('"') for line in markdown.splitlines())
    print("SELF_TEST PASS")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--refresh-decision-receipt", action="store_true")
    parser.add_argument("--source", type=Path)
    parser.add_argument("--reference-manifest", type=Path)
    parser.add_argument("--output-dir", type=Path)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.self_test:
        self_test()
        return 0
    if args.refresh_decision_receipt:
        if args.output_dir is None:
            raise SystemExit("--refresh-decision-receipt requires --output-dir")
        result = refresh_decision_and_receipt(args.output_dir)
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    missing = [
        name for name, value in (
            ("--source", args.source),
            ("--reference-manifest", args.reference_manifest),
            ("--output-dir", args.output_dir),
        ) if value is None
    ]
    if missing:
        raise SystemExit(f"missing required arguments: {', '.join(missing)}")
    result = build_package(args.source, args.reference_manifest, args.output_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
