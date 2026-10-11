#!/usr/bin/env python3
"""Join reviewed local-pilot labels and report candidate-level model metrics."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path


SCRIPT = Path(__file__).resolve()

def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def wilson(successes: int, total: int, z: float = 1.959963984540054) -> list[float] | None:
    if total == 0:
        return None
    p = successes / total
    denominator = 1 + z * z / total
    center = (p + z * z / (2 * total)) / denominator
    radius = z * math.sqrt(p * (1 - p) / total + z * z / (4 * total * total)) / denominator
    return [center - radius, center + radius]


def rate(successes: int, total: int) -> dict[str, object]:
    return {"numerator": successes, "denominator": total,
            "rate": successes / total if total else None,
            "wilson_95": wilson(successes, total)}


def metrics(rows: list[dict[str, str]], prediction_field: str) -> dict[str, object]:
    labels = Counter(row["review_class"] for row in rows)
    predictions = Counter(row[prediction_field] for row in rows)
    ped_correct = sum(row["review_class"] == "ped" and row[prediction_field] == "ped"
                      for row in rows)
    vehicle_correct = sum(row["review_class"] == "vehicle" and row[prediction_field] == "vehicle"
                          for row in rows)
    semantic = [row for row in rows if row["review_class"] in {"ped", "vehicle"}]
    invalid = [row for row in rows if row["review_class"] == "invalid"]
    correct = ped_correct + vehicle_correct
    return {
        "prediction_field": prediction_field,
        "prediction_counts": dict(sorted(predictions.items())),
        "ped_recall": rate(ped_correct, labels["ped"]),
        "vehicle_recall": rate(vehicle_correct, labels["vehicle"]),
        "ped_precision_including_invalid": rate(
            ped_correct, sum(row[prediction_field] == "ped" for row in rows)),
        "vehicle_precision_including_invalid": rate(
            vehicle_correct, sum(row[prediction_field] == "vehicle" for row in rows)),
        "semantic_only_accuracy": rate(correct, len(semantic)),
        "three_label_accuracy_without_reject": rate(correct, len(rows)),
        "invalid_false_accept_rate_without_reject": rate(len(invalid), len(invalid)),
        "confusion_truth_by_prediction": {
            truth: dict(sorted(Counter(
                row[prediction_field] for row in rows if row["review_class"] == truth
            ).items())) for truth in ("ped", "vehicle", "invalid")
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review-dir", required=True, type=Path)
    args = parser.parse_args()
    directory = args.review_dir.resolve()
    manifest_path = directory / "review_manifest.csv"
    labels_path = directory / "human_labels.csv"
    manifest = read_csv(manifest_path)
    labels = read_csv(labels_path)
    by_id = {row["review_subset_id"]: row for row in labels}
    if len(by_id) != 60 or len(labels) != 60 or len(manifest) != 60:
        raise ValueError("expected exactly 60 unique labels and manifest rows")
    if set(by_id) != {row["review_subset_id"] for row in manifest}:
        raise ValueError("label and manifest identities differ")
    allowed_class = {"ped", "vehicle", "invalid", "ignore"}
    allowed_condition = {"complete", "truncated", "merged", "background_fragment", "other"}
    allowed_crop = {"yes", "no"}
    joined = []
    for source in manifest:
        label = by_id[source["review_subset_id"]]
        if label["review_class"] not in allowed_class:
            raise ValueError("invalid review_class")
        if label["candidate_condition"] not in allowed_condition:
            raise ValueError("invalid candidate_condition")
        if label["crop_usable"] not in allowed_crop:
            raise ValueError("invalid crop_usable")
        row = dict(source)
        for field in ("review_class", "semantic_subtype", "candidate_condition", "crop_usable",
                      "reviewer", "reviewed_at", "review_note"):
            row[field] = label[field]
        joined.append(row)

    reviewed_path = directory / "reviewed_manifest.csv"
    write_csv(reviewed_path, joined)
    label_counts = Counter(row["review_class"] for row in joined)
    condition_counts = Counter(row["candidate_condition"] for row in joined)
    time_bins: dict[str, Counter[str]] = defaultdict(Counter)
    for row in joined:
        time_bins[row["selection_time_bin"]][row["review_class"]] += 1

    model_fields = ("hog64_prediction", "hog324_float_prediction", "hog324_q_prediction")
    model_metrics = {field: metrics(joined, field) for field in model_fields}
    float_q_mismatch = sum(
        row["hog324_float_prediction"] != row["hog324_q_prediction"] for row in joined
    )

    boundary_ids = {"local60_049", "local60_057"}
    conservative = [dict(row) for row in joined]
    for row in conservative:
        if row["review_subset_id"] in boundary_ids:
            row["review_class"] = "invalid"
            row["candidate_condition"] = "truncated"
            row["crop_usable"] = "no"

    report = {
        "schema": "local_intersection_candidate_review_metrics_v1",
        "scope": {
            "development_pilot_only": True,
            "video": "2415171-hd_1920_1080_24fps.mp4",
            "scoring_window_frames_inclusive": [120, 1079],
            "selection_is_model_blind": True,
            "candidate_level_only": True,
            "full_frame_target_annotations_available": False,
            "end_to_end_recall_available": False,
            "training_or_tuning_performed": False,
        },
        "input_hashes": {
            "review_manifest_sha256": digest(manifest_path),
            "human_labels_sha256": digest(labels_path),
        },
        "review": {
            "rows": len(joined),
            "label_counts": dict(sorted(label_counts.items())),
            "semantic_candidate_rate": rate(label_counts["ped"] + label_counts["vehicle"], len(joined)),
            "invalid_candidate_rate": rate(label_counts["invalid"], len(joined)),
            "crop_usable_rate": rate(sum(row["crop_usable"] == "yes" for row in joined), len(joined)),
            "candidate_condition_counts": dict(sorted(condition_counts.items())),
            "by_time_bin": {key: dict(sorted(value.items())) for key, value in sorted(time_bins.items())},
        },
        "models": model_metrics,
        "hog324_float_q_prediction_mismatch": {"count": float_q_mismatch,
                                                 "denominator": len(joined)},
        "boundary_sensitivity": {
            "ids": sorted(boundary_ids),
            "alternative": "reclassify two head-and-leg-missing upper-body candidates as invalid",
            "label_counts": dict(sorted(Counter(row["review_class"] for row in conservative).items())),
            "models": {field: metrics(conservative, field) for field in model_fields},
        },
        "metric_boundary": (
            "These are candidate-ROI sample metrics. They estimate classifier behavior after the "
            "candidate chain emits a box, but cannot measure missed people/vehicles or end-to-end recall."
        ),
    }
    report_path = directory / "review_report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def pct(value: float | None) -> str:
        return "n/a" if value is None else f"{100 * value:.1f}%"

    h64 = model_metrics["hog64_prediction"]
    h324 = model_metrics["hog324_q_prediction"]
    decision = f"""# 本地近距离路口候选级 pilot 结果

状态：开发诊断；没有完整帧目标真值，因此不能报告端到端召回率，也不冻结模型或 RTL。

## 人工审核样本

- 从 251 个几何代表中，按三个固定时间段和候选 ID 哈希模型盲选 60 项。
- 人工标签：ped {label_counts['ped']}、vehicle {label_counts['vehicle']}、invalid {label_counts['invalid']}。
- 语义候选比例：{label_counts['ped'] + label_counts['vehicle']}/60 = {pct((label_counts['ped'] + label_counts['vehicle']) / 60)}。
- invalid 比例：{label_counts['invalid']}/60 = {pct(label_counts['invalid'] / 60)}。
- 47 个 invalid 主要由人体碎片、路面亮斑和树叶背景构成。

## 候选 ROI 分类

| 模型 | Ped Recall | Vehicle Recall | 语义样本准确率 | 无拒识 invalid FAR |
|---|---:|---:|---:|---:|
| HOG64 | {h64['ped_recall']['numerator']}/{h64['ped_recall']['denominator']} = {pct(h64['ped_recall']['rate'])} | {h64['vehicle_recall']['numerator']}/{h64['vehicle_recall']['denominator']} = {pct(h64['vehicle_recall']['rate'])} | {h64['semantic_only_accuracy']['numerator']}/{h64['semantic_only_accuracy']['denominator']} = {pct(h64['semantic_only_accuracy']['rate'])} | 100% |
| HOG324-Q | {h324['ped_recall']['numerator']}/{h324['ped_recall']['denominator']} = {pct(h324['ped_recall']['rate'])} | {h324['vehicle_recall']['numerator']}/{h324['vehicle_recall']['denominator']} = {pct(h324['vehicle_recall']['rate'])} | {h324['semantic_only_accuracy']['numerator']}/{h324['semantic_only_accuracy']['denominator']} = {pct(h324['semantic_only_accuracy']['rate'])} | 100% |

HOG324 浮点与量化分类不一致为 {float_q_mismatch}/60。两个边界上半身样本改判 invalid 的敏感性结果保存在 `review_report.json`。

## 决策

较大目标改善了部分可用 ROI 的分类条件，但当前部署候选链仍被背景与目标碎片主导：全窗口 960 帧中 840 帧占满四槽，本次盲选样本 invalid 达 {pct(label_counts['invalid'] / 60)}。因此不能仅凭换成近距离场景进入 RTL；下一步应先在 Python 修复候选框合并与背景碎片抑制，再使用同一冻结窗口重跑。

本报告不把模型预测分布当作正确率，也不把候选级 recall 当作完整视频的目标召回率。

## 领导者复核后的下一步

目前不能把 HOG324-Q 的 5/10 与 010107 的 11/26 直接比较为“近距离提高”；两个场景、抽样和样本量不同，vehicle 也只有 3 项。下一步优先修候选链，暂不扩大模型训练。

在同一冻结窗口只允许逐项运行两个 Python 诊断，第一轮不组合，也不做阈值网格搜索：

1. 先按重复背景响应、阴影和目标残片复核 invalid 来源，再试一个有机制依据的背景抑制规则。
2. 仅在上下文证明多个碎片来自同一目标时，试一个固定空间/时间约束的 top4 前组件合并规则；停车车辆、多人相邻和影子作为反例。

运行前须补一份按预注册时间抽样的完整帧目标参考，记录未进入 top4 的人车。每个实验冻结视频哈希、frame0 因果背景、f120–1079、基线和模型版本，保持最终不超过四框；分别报告有效目标保留/丢失、invalid 减少、裁剪完整性和四槽占用。任何新框或改变几何的框都重新人工审核。

本窗口一旦用于制定规则就属于开发数据。胜出规则必须在另一个未参与制定的固定机位窗口或视频验证，经过独立验证和资源/时序评估后才讨论 RTL。
"""
    decision_path = directory / "DECISION.md"
    decision_path.write_text(decision, encoding="utf-8")
    receipt = {
        "schema": "local_intersection_review_receipt_v1",
        "script_sha256": digest(SCRIPT),
        "inputs": {
            "review_manifest.csv": digest(manifest_path),
            "human_labels.csv": digest(labels_path),
        },
        "outputs": {
            "reviewed_manifest.csv": digest(reviewed_path),
            "review_report.json": digest(report_path),
            "DECISION.md": digest(decision_path),
        },
        "assertions": {
            "review_rows_exactly_60": True,
            "labels_join_one_to_one": True,
            "selection_was_model_blind": True,
            "candidate_level_only": True,
            "end_to_end_recall_not_reported": True,
            "training_or_threshold_tuning_performed": False,
        },
    }
    receipt_path = directory / "receipt.json"
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
                            encoding="utf-8")
    readback = json.loads(receipt_path.read_text(encoding="utf-8"))
    for name, expected in readback["outputs"].items():
        if digest(directory / name) != expected:
            raise RuntimeError(f"receipt readback mismatch: {name}")
    print(json.dumps({"reviewed_manifest": str(reviewed_path),
                      "report": str(report_path), "decision": str(decision_path),
                      "receipt": str(receipt_path)},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
