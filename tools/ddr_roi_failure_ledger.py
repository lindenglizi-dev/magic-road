#!/usr/bin/env python3
"""Re-index frozen 256-line ROI failure evidence without replay or retraining."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "evaluation/ddr_architecture/roi_failure_ledger_20261001_v2"
TARGET_DIR = ROOT / "evaluation/ddr_architecture/target_change_20261001_v2"
CROP_DIR = ROOT / "evaluation/local_scene_pilots/intersection_2415171_crop_change_v2"
MARGIN_DIR = ROOT / "evaluation/local_scene_pilots/intersection_2415171_margin_change_v1"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def verify_receipt_artifact(directory: Path, name: str) -> str:
    receipt = load_json(directory / "receipt.json")
    expected = receipt["artifact_hashes"][name]
    actual = sha256(directory / name)
    assert actual == expected, f"receipt mismatch: {directory.name}/{name}"
    return actual


def find_one(rows, **wanted):
    matches = [row for row in rows if all(str(row[key]) == str(value) for key, value in wanted.items())]
    assert len(matches) == 1, (wanted, len(matches))
    return matches[0]


def model_side(match: dict | None) -> dict | None:
    if match is None:
        return None
    score = match["score"]
    return {
        "candidate_id": match["candidate_id"],
        "component_label": match["component_label"],
        "candidate_rank": match["rank"],
        "component_area": match["component_area"],
        "analysis_bbox_inclusive": match["analysis_box"],
        "source_bbox_inclusive": match["source_box"],
        "iou_with_target": match["iou_with_gt"],
        "roi_pixel_sha256": match["roi_pixel_sha256"],
        "hog324_q_prediction": score["hog324_q_prediction"],
        "hog324_q_margin_integer": int(score["hog324_q_score_integer"]),
        "hog324_float_prediction": score["hog324_float_prediction"],
        "hog324_float_margin": float(score["hog324_float_score"]),
    }


def build_ledger() -> tuple[list[dict], dict]:
    target_changes = list(csv.DictReader((TARGET_DIR / "target_change_ledger.csv").open(encoding="utf-8-sig", newline="")))
    target_stages = list(csv.DictReader((TARGET_DIR / "target_stage_ledger.csv").open(encoding="utf-8-sig", newline="")))
    crop_rows = load_json(CROP_DIR / "all_targets.json")
    margin_rows = load_json(MARGIN_DIR / "score_changes.json")

    records: list[dict] = []

    # The only frozen baseline256 case where the same qualifying component is
    # retained by min_run1 but moves out of Top4.
    change = find_one(
        target_changes,
        source_frame_id=450,
        target_id="p01",
        config="baseline256",
        stage="top4",
    )
    before = find_one(
        target_stages,
        source_frame_id=450,
        target_id="p01",
        config="baseline256",
        branch="current",
        stage="area_all",
    )
    after = find_one(
        target_stages,
        source_frame_id=450,
        target_id="p01",
        config="baseline256",
        branch="keep_all",
        stage="area_all",
    )
    crop = find_one(crop_rows, frame_index=450, track_id="p01")
    assert change["change_current_to_keep_all"] == "lost"
    assert change["pixel_structural_relation"] == "unchanged"
    assert change["ranking_membership_changed"] == "True"
    assert before["matched_component_label"] == after["matched_component_label"] == "62"
    assert (int(before["matched_component_area_rank"]), int(after["matched_component_area_rank"])) == (4, 6)
    assert json.loads(before["matched_component_source_bbox"]) == json.loads(after["matched_component_source_bbox"])
    assert crop["minrun_match"] is None and crop["lost_attribution"]["reason"] == "area_top4_selection_loss"
    saved = model_side(crop["baseline_match"])
    records.append(
        {
            "failure_kind": "retained_component_displaced_from_top4",
            "frame_id": 450,
            "track_id": "p01",
            "target_class": "ped",
            "visibility": crop["visibility"],
            "target_source_bbox_inclusive": crop["gt_box"],
            "current": saved,
            "keep_all_component_before_top4": {
                "component_label": int(after["matched_component_label"]),
                "candidate_rank": int(after["matched_component_area_rank"]),
                "component_area": int(after["matched_component_pixel_area"]),
                "source_bbox_inclusive": json.loads(after["matched_component_source_bbox"]),
                "iou_with_target": float(after["matched_component_iou"]),
                "selected_by_top4": False,
                "saved_model_evidence": {
                    "status": "same_component_and_bbox_as_current; score was stored only on the current selected candidate",
                    "hog324_q_prediction": saved["hog324_q_prediction"],
                    "hog324_q_margin_integer": saved["hog324_q_margin_integer"],
                    "independent_keep_all_score_record": False,
                },
            },
            "component_relation": "unchanged",
            "attribution": "ranking_loss_before_classifier",
            "source_reports": [
                "evaluation/ddr_architecture/target_change_20261001_v2/target_stage_ledger.csv",
                "evaluation/local_scene_pilots/intersection_2415171_crop_change_v2/all_targets.json",
            ],
        }
    )

    flips = [(360, "p01"), (690, "p02"), (1050, "p02")]
    for frame_id, track_id in flips:
        change = find_one(
            target_changes,
            source_frame_id=frame_id,
            target_id=track_id,
            config="baseline256",
            stage="top4",
        )
        crop = find_one(crop_rows, frame_index=frame_id, track_id=track_id)
        margin = find_one(margin_rows, frame_index=frame_id, track_id=track_id)
        current = model_side(crop["baseline_match"])
        keep_all = model_side(crop["minrun_match"])
        assert crop["coverage_outcome"] == "both"
        assert crop["prediction_transition"] == "correct_to_wrong"
        assert margin["classification_flipped"] is True
        assert current and keep_all
        assert current["iou_with_target"] >= 0.5 and keep_all["iou_with_target"] >= 0.5
        assert current["hog324_q_prediction"] == margin["before_score"]["hog324_q_prediction"] == "ped"
        assert keep_all["hog324_q_prediction"] == margin["after_score"]["hog324_q_prediction"] == "vehicle"
        assert current["hog324_q_margin_integer"] == int(margin["before_score"]["hog324_q_score_integer"])
        assert keep_all["hog324_q_margin_integer"] == int(margin["after_score"]["hog324_q_score_integer"])
        assert change["change_current_to_keep_all"] == "stable_match"
        records.append(
            {
                "failure_kind": "geometry_match_retained_but_hog324_prediction_flipped",
                "frame_id": frame_id,
                "track_id": track_id,
                "target_class": crop["label"],
                "visibility": crop["visibility"],
                "target_source_bbox_inclusive": crop["gt_box"],
                "current": current,
                "keep_all": keep_all,
                "component_relation": change["pixel_structural_relation"],
                "overlapping_current_component_labels": json.loads(change["overlapping_current_component_labels"]),
                "integer_margin_delta": margin["integer_score_delta"],
                "float_margin_delta": margin["float_delta"],
                "attribution": "stored_crop_and_score_change; not a quantization-only flip",
                "source_reports": [
                    "evaluation/ddr_architecture/target_change_20261001_v2/target_change_ledger.csv",
                    "evaluation/local_scene_pilots/intersection_2415171_crop_change_v2/all_targets.json",
                    "evaluation/local_scene_pilots/intersection_2415171_margin_change_v1/score_changes.json",
                ],
            }
        )

    checks = {
        "status": "PASS",
        "record_count": len(records),
        "ranking_loss_count": sum(row["failure_kind"].startswith("retained_component") for row in records),
        "model_flip_count": sum(row["failure_kind"].startswith("geometry_match") for row in records),
        "flip_identities": [[row["frame_id"], row["track_id"]] for row in records[1:]],
    }
    assert checks == {
        "status": "PASS",
        "record_count": 4,
        "ranking_loss_count": 1,
        "model_flip_count": 3,
        "flip_identities": [[360, "p01"], [690, "p02"], [1050, "p02"]],
    }
    return records, checks


def write_csv(path: Path, records: list[dict]) -> None:
    fields = [
        "failure_kind", "frame_id", "track_id", "target_class", "visibility",
        "current_component_label", "current_rank", "current_source_bbox", "current_iou",
        "current_prediction", "current_margin", "new_component_label", "new_rank",
        "new_source_bbox", "new_iou", "new_prediction", "new_margin", "component_relation",
        "new_score_provenance", "new_independent_score_record",
    ]
    with path.open("w", encoding="utf-8", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=fields)
        writer.writeheader()
        for record in records:
            current = record["current"]
            new = record["keep_all"] if "keep_all" in record else record["keep_all_component_before_top4"]
            saved = new.get("saved_model_evidence", {})
            writer.writerow({
                "failure_kind": record["failure_kind"],
                "frame_id": record["frame_id"],
                "track_id": record["track_id"],
                "target_class": record["target_class"],
                "visibility": record["visibility"],
                "current_component_label": current["component_label"],
                "current_rank": current["candidate_rank"],
                "current_source_bbox": json.dumps(current["source_bbox_inclusive"], separators=(",", ":")),
                "current_iou": current["iou_with_target"],
                "current_prediction": current["hog324_q_prediction"],
                "current_margin": current["hog324_q_margin_integer"],
                "new_component_label": new["component_label"],
                "new_rank": new["candidate_rank"],
                "new_source_bbox": json.dumps(new["source_bbox_inclusive"], separators=(",", ":")),
                "new_iou": new["iou_with_target"],
                "new_prediction": new.get("hog324_q_prediction", saved.get("hog324_q_prediction")),
                "new_margin": new.get("hog324_q_margin_integer", saved.get("hog324_q_margin_integer")),
                "component_relation": record["component_relation"],
                "new_score_provenance": ("stored_keep_all_score" if "keep_all" in record
                                         else "current_selected_same_bbox"),
                "new_independent_score_record": "keep_all" in record,
            })


def report_text(records: list[dict], input_hashes: dict[str, str]) -> str:
    ranking = records[0]
    lines = [
        "# 256 检测线 ROI 失败定位账本",
        "",
        "本报告只重整已冻结的逐目标、ROI 和模型分数记录；未解码视频、未重算候选、未训练模型、未改变阈值。",
        "",
        "## 定位结果",
        "",
        "| 类型 | frame/track | current | keep_all | 结论 |",
        "|---|---|---|---|---|",
    ]
    new = ranking["keep_all_component_before_top4"]
    lines.append(
        f"| Top4 排名损失 | {ranking['frame_id']}/{ranking['track_id']} | "
        f"cc{ranking['current']['component_label']} rank{ranking['current']['candidate_rank']}, "
        f"IoU={ranking['current']['iou_with_target']:.4f}, ped, margin={ranking['current']['hog324_q_margin_integer']} | "
        f"同一 cc{new['component_label']} rank{new['candidate_rank']}, IoU={new['iou_with_target']:.4f}, 未进入 Top4 | "
        "组件和框未变，分类前已被更大的组件挤出。 |"
    )
    for row in records[1:]:
        current, after = row["current"], row["keep_all"]
        lines.append(
            f"| 几何合格但类别翻转 | {row['frame_id']}/{row['track_id']} | "
            f"cc{current['component_label']} rank{current['candidate_rank']}, IoU={current['iou_with_target']:.4f}, "
            f"{current['hog324_q_prediction']}, margin={current['hog324_q_margin_integer']} | "
            f"cc{after['component_label']} rank{after['candidate_rank']}, IoU={after['iou_with_target']:.4f}, "
            f"{after['hog324_q_prediction']}, margin={after['hog324_q_margin_integer']} | "
            f"{row['component_relation']} 后裁剪与分数改变；float 与量化路径同向翻转。 |"
        )
    lines += [
        "",
        "## 工程含义",
        "",
        "- `f450/p01` 不能靠分类器修复：目标组件仍满足 IoU≥0.5，但从面积 rank4 降至 rank6，在 ROI 启动前已经丢失。",
        "- `f360/p01`、`f690/p02`、`f1050/p02` 两侧都满足 IoU≥0.5；三例均是多个旧组件连接后的裁剪变化，已有 HOG324 浮点和量化记录都由 ped 变为 vehicle。",
        "- 这些记录不证明哪个视觉结构造成合并，也不支持调阈值、训练新模型或将 keep_all 设为默认。",
        "- 未匹配目标和候选仍是 unknown/missed geometry；没有任何条目被自动标为 invalid。",
        "",
        "## 证据边界",
        "",
        "这是历史结果重整，不是新增识别准确率证据。`f450/p01` 的 keep_all 分支没有独立保存分类输出；由于账本证明组件、框和像素关系不变，本报告仅引用原 selected crop 的已存分数，并明确标记为非独立记录。",
        "",
        "输入文件 SHA-256：",
        "",
    ]
    lines.extend(f"- `{name}`: `{digest}`" for name, digest in input_hashes.items())
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()

    input_files = {
        "evaluation/ddr_architecture/target_change_20261001_v2/target_change_ledger.csv": TARGET_DIR / "target_change_ledger.csv",
        "evaluation/ddr_architecture/target_change_20261001_v2/target_stage_ledger.csv": TARGET_DIR / "target_stage_ledger.csv",
        "evaluation/local_scene_pilots/intersection_2415171_crop_change_v2/all_targets.json": CROP_DIR / "all_targets.json",
        "evaluation/local_scene_pilots/intersection_2415171_margin_change_v1/score_changes.json": MARGIN_DIR / "score_changes.json",
    }
    verify_receipt_artifact(TARGET_DIR, "target_change_ledger.csv")
    verify_receipt_artifact(TARGET_DIR, "target_stage_ledger.csv")
    verify_receipt_artifact(CROP_DIR, "all_targets.json")
    verify_receipt_artifact(MARGIN_DIR, "score_changes.json")
    input_hashes = {name: sha256(path) for name, path in input_files.items()}
    records, checks = build_ledger()
    if args.self_check:
        print(json.dumps(checks, ensure_ascii=False, indent=2))
        return

    output = args.output.resolve()
    assert ROOT in output.parents, "output must remain inside the project"
    expected_names = {"roi_failure_ledger.json", "roi_failure_ledger.csv", "report.md", "receipt.json"}
    if output.exists():
        existing_names = {path.name for path in output.iterdir()}
        assert "receipt.json" not in existing_names, "refusing to overwrite a completed audit"
        assert existing_names <= expected_names, "unexpected file in partial audit directory"
    else:
        output.mkdir(parents=True)
    ledger_path = output / "roi_failure_ledger.json"
    csv_path = output / "roi_failure_ledger.csv"
    report_path = output / "report.md"
    ledger_path.write_text(json.dumps({"records": records, "self_check": checks}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_csv(csv_path, records)
    report_path.write_text(report_text(records, input_hashes), encoding="utf-8")
    receipt = {
        "status": "PASS_historical_evidence_reindex_only",
        "command": ["python", "tools/ddr_roi_failure_ledger.py"],
        "script_sha256": sha256(Path(__file__)),
        "input_hashes": input_hashes,
        "input_receipt_hashes": {
            "target_change_20261001_v2/receipt.json": sha256(TARGET_DIR / "receipt.json"),
            "intersection_2415171_crop_change_v2/receipt.json": sha256(CROP_DIR / "receipt.json"),
            "intersection_2415171_margin_change_v1/receipt.json": sha256(MARGIN_DIR / "receipt.json"),
        },
        "artifact_hashes": {
            ledger_path.name: sha256(ledger_path),
            csv_path.name: sha256(csv_path),
            report_path.name: sha256(report_path),
        },
        "self_check": checks,
        "boundaries": [
            "No video decode, background replay, ROI resampling, model execution, training, threshold change, or blind-reserve access.",
            "Frozen historical results were re-indexed; this is not new accuracy evidence.",
            "Unknown or unmatched evidence is never converted to invalid labels.",
            "Component relation is mechanical pixel connectivity, not a semantic cause label.",
        ],
    }
    (output / "receipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(checks, ensure_ascii=False))


if __name__ == "__main__":
    main()
