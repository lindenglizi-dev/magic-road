"""Build a read-only saved-prediction error report; never trains or edits GT."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import html
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

from cnn.analyze_detection_errors import diagnose, ious, match  # noqa: E402
from cnn.diagnose_tiny_fit import assign  # noqa: E402
from cnn.metrics import report as metric_report  # noqa: E402
from cnn.train import sha256  # noqa: E402

HERE = Path(__file__).resolve().parent
CLASS_NAMES = ("person", "vehicle")
REPORTS = {
    "development17": {
        "E7": ROOT / "cnn/reports/ac_bnfreeze_g10_20261013_v1/e7_control17.json",
        "step5": ROOT / "cnn/reports/ac_bnfreeze_g10_20261013_v1/early_checkpoints/update_5_development17.json",
        "step10": ROOT / "cnn/reports/ac_bnfreeze_g10_20261013_v1/development17.json",
    },
    "old256": {
        "E7": ROOT / "cnn/reports/person_native_recovery_20261004/epoch_7_val256.json",
        "step5": ROOT / "cnn/reports/ac_bnfreeze_g10_20261013_v1/early_checkpoints/update_5_old256.json",
        "step10": ROOT / "cnn/reports/ac_bnfreeze_g10_20261013_v1/old256_regression.json",
    },
}
MANIFESTS = {
    "development17": ROOT / "cnn/reports/ac_g10_20261013_v1/dataset.json",
    "old256": ROOT / "cnn/data/visdrone_vid_train/raw_manifest/dataset.json",
}
SOURCE_FILES = (
    ROOT / "cnn/analyze_detection_errors.py",
    ROOT / "cnn/diagnose_tiny_fit.py",
    ROOT / "cnn/metrics.py",
    ROOT / "cnn/train.py",
)
SAFE_REASON = {
    "fn_no_retained_support_cause_unresolved":
        "fn_no_support_at_retained_floor_raw_candidate_unobserved",
    "fp_no_GT_support_background_or_missing_annotation_unresolved":
        "fp_no_retained_GT_support_semantics_unresolved",
}
REASON_ZH = {
    "tp": "0.5 阈值真阳性",
    "fn_recovered_by_lowering_score_one_to_one": "约 0.05 保留地板内有一对一支撑，但低于 0.5",
    "fn_same_class_candidate_competes_for_other_GT": "同类保留框与其他 GT 竞争",
    "fn_other_class_box_support": "仅另一类别保留框提供 IoU≥0.5 的几何支撑",
    "fn_same_class_localization_support_IoU_025_to_05": "同类保留框仅有 0.25≤IoU<0.5 定位支撑",
    "fn_no_support_at_retained_floor_raw_candidate_unobserved": "约 0.05 保留地板以上无支撑；原始候选未保存，不能判定不存在",
    "fp_duplicate_same_class_overlap": "同类重复框的几何重叠",
    "fp_other_class_GT_overlap": "与另一类 GT 的几何重叠",
    "fp_same_class_localization_support_IoU_025_to_05": "同类 GT 仅有 0.25≤IoU<0.5",
    "fp_no_retained_GT_support_semantics_unresolved": "与保留 GT 无支撑；不能自动判为背景或漏标",
}


def safe_reason(reason):
    return SAFE_REASON.get(reason, reason)


def normalized(value):
    if isinstance(value, dict):
        return {safe_reason(key): normalized(item) for key, item in value.items()}
    return value


def size_bin(box):
    height = box[3] - box[1]
    return "height_le8" if height <= 8 else "height_8_to16" if height <= 16 else "height_gt16"


def best_candidate(predictions, target):
    if not predictions:
        return None, 0.0
    values = ious(predictions, [target])[:, 0]
    index = max(range(len(predictions)), key=lambda j: (values[j], predictions[j]["score"], -j))
    return predictions[index], float(values[index])


def detail(result, metadata):
    ground, predictions, ignores = defaultdict(list), defaultdict(list), defaultdict(list)
    for row in result["truth"]:
        ground[row["image_id"]].append(row)
    for index, row in enumerate(result["predictions"]):
        predictions[row["image_id"]].append((index, row))
    for row in result["ignores"]:
        ignores[row["image_id"]].append(row)
    targets, false_positives, ignored_predictions = [], [], []
    totals = defaultdict(Counter)
    for image_id in sorted(set(ground) | set(predictions)):
        meta = metadata[image_id]
        local = [row for _, row in sorted(predictions[image_id], key=lambda item: (-item[1]["score"], item[0]))]
        for label, name in enumerate(CLASS_NAMES):
            gt = [row for row in ground[image_id] if row["label"] == label]
            pred = [row for row in local if row["label"] == label]
            other_gt = [row for row in ground[image_id] if row["label"] != label]
            other_pred = [row for row in local if row["label"] != label]
            matrix, foreign, other_support = ious(pred, gt), ious(pred, other_gt), ious(other_pred, gt)
            ignored = np.zeros(len(pred), dtype=bool)
            for region in ignores[image_id]:
                if region["label"] in (-1, label):
                    ignored |= ious(pred, [region], region.get("crowd", False))[:, 0] >= .5
            used, true, false, skipped = match(pred, matrix, ignored, .5)
            used_low, _, _, _ = match(pred, matrix, ignored, 0.)
            high_pairs, low_pairs = assign(pred, gt, .5), assign(pred, gt, 0.)
            assert set(high_pairs) == used and set(high_pairs.values()) == true
            assert set(low_pairs) == used_low
            totals[name].update(gt=len(gt), tp=len(used), fp=len(false), fn=len(gt) - len(used),
                                ignored=len(skipped))
            for target_index, target in enumerate(gt):
                if target_index in high_pairs:
                    reason, outcome, candidate = "tp", "tp", pred[high_pairs[target_index]]
                elif target_index in low_pairs:
                    reason, outcome = "fn_recovered_by_lowering_score_one_to_one", "fn"
                    candidate = pred[low_pairs[target_index]]
                elif np.any(matrix[:, target_index] >= .5):
                    reason, outcome = "fn_same_class_candidate_competes_for_other_GT", "fn"
                    candidate, _ = best_candidate(pred, target)
                elif np.any(other_support[:, target_index] >= .5):
                    reason, outcome = "fn_other_class_box_support", "fn"
                    candidate, _ = best_candidate(other_pred, target)
                elif np.any(matrix[:, target_index] >= .25):
                    reason, outcome = "fn_same_class_localization_support_IoU_025_to_05", "fn"
                    candidate, _ = best_candidate(pred, target)
                else:
                    reason, outcome = "fn_no_support_at_retained_floor_raw_candidate_unobserved", "fn"
                    candidate, _ = best_candidate(pred, target)
                _, candidate_iou = best_candidate([candidate] if candidate else [], target)
                targets.append({
                    "key": f"{image_id}|{label}|{target_index}", "image_id": image_id,
                    "camera_id": meta.get("camera_id"), "scene_id": meta["scene_id"],
                    "class_name": name, "target_index": target_index, "target": target,
                    "size_bin": size_bin(target["box"]), "outcome": outcome,
                    "reason": reason, "candidate": candidate, "candidate_IoU": candidate_iou,
                })
            for index in sorted(false):
                if np.any(matrix[index] >= .5):
                    reason = "fp_duplicate_same_class_overlap"
                elif np.any(foreign[index] >= .5):
                    reason = "fp_other_class_GT_overlap"
                elif np.any(matrix[index] >= .25):
                    reason = "fp_same_class_localization_support_IoU_025_to_05"
                else:
                    reason = "fp_no_retained_GT_support_semantics_unresolved"
                false_positives.append({
                    "image_id": image_id, "camera_id": meta.get("camera_id"),
                    "scene_id": meta["scene_id"], "class_name": name,
                    "prediction": pred[index], "reason": reason,
                })
            for index in sorted(skipped):
                ignored_predictions.append({"image_id": image_id, "camera_id": meta.get("camera_id"),
                    "scene_id": meta["scene_id"], "class_name": name, "prediction": pred[index]})
    expected = result["diagnostic_metrics_at_0_5"]["classes"]
    for name in CLASS_NAMES:
        assert all(totals[name][key] == expected[name][key] for key in ("tp", "fp", "fn", "ignored"))
    return {"targets": targets, "false_positives": false_positives,
            "ignored_predictions": ignored_predictions, "totals": totals}


def grouped_counts(details, field):
    groups = defaultdict(lambda: defaultdict(Counter))
    for row in details["targets"]:
        group = row[field]
        if group is not None:
            counts = groups[group][row["class_name"]]
            counts["gt"] += 1
            counts[row["outcome"]] += 1
            if row["reason"] != row["outcome"]:
                counts[row["reason"]] += 1
    for row in details["false_positives"]:
        group = row[field]
        if group is not None:
            groups[group][row["class_name"]].update(fp=1, **{row["reason"]: 1})
    for row in details["ignored_predictions"]:
        group = row[field]
        if group is not None:
            groups[group][row["class_name"]].update(ignored=1)
    return {group: {name: dict(counts) for name, counts in classes.items()}
            for group, classes in sorted(groups.items())}


def load_group(group):
    manifest_data = json.loads(MANIFESTS[group].read_text(encoding="utf-8"))
    assert manifest_data["input_size"] == [512, 288]
    metadata = {row["image"]: row for row in manifest_data["images"]}
    loaded = {stage: json.loads(path.read_text(encoding="utf-8")) for stage, path in REPORTS[group].items()}
    first = loaded["E7"]
    for stage, result in loaded.items():
        assert result["truth"] == first["truth"], (group, stage, "truth")
        assert result["ignores"] == first["ignores"], (group, stage, "ignores")
        assert result["postprocess_contract"] == first["postprocess_contract"], (group, stage, "postprocess")
        image_ids = {row["image_id"] for key in ("truth", "predictions", "ignores") for row in result[key]}
        assert image_ids <= metadata.keys(), (group, stage, "metadata")
    return metadata, loaded


def aggregate(group, stage, result, metadata, details):
    canonical = diagnose(result)
    for name in CLASS_NAMES:
        assert all(canonical["classes"][name][key] == details["totals"][name][key]
                   for key in ("tp", "fp", "fn", "ignored"))
    explicit_cameras = sum(row.get("camera_id") is not None for row in metadata.values()
                           if row["image"] in {target["image_id"] for target in details["targets"]})
    return {
        "source": REPORTS[group][stage].relative_to(ROOT).as_posix(),
        "source_sha256": sha256(REPORTS[group][stage]),
        "checkpoint_sha256": result["checkpoint_sha256"],
        "postprocess_contract": result["postprocess_contract"],
        "classes": normalized(canonical["classes"]),
        "size_groups_input_512x288": normalized(canonical["size_groups"]),
        "camera_groups": grouped_counts(details, "camera_id"),
        "scene_groups": grouped_counts(details, "scene_id"),
        "camera_metadata": ("explicit_camera_id" if explicit_cameras else
                            "unavailable_in_source_manifest; scene_id_reported_separately"),
        "raw_stage_evidence": {
            "available": False,
            "no_raw_candidate_count": None,
            "nms_causal_count": None,
            "statement": "Only retained postprocess predictions at score floor 3276/65536 are saved.",
        },
    }


def inverse_box(box, meta):
    letterbox = meta["preprocess"]["letterbox_1280x720"]
    sx, sy = letterbox["scale_x"], letterbox["scale_y"]
    ox, oy = letterbox["offset_x"], letterbox["offset_y"]
    return [(box[0] * 2.5 - ox) / sx, (box[1] * 2.5 - oy) / sy,
            (box[2] * 2.5 - ox) / sx, (box[3] * 2.5 - oy) / sy]


def compact_event(event, meta):
    answer = {key: event[key] for key in ("outcome", "reason", "size_bin", "candidate_IoU")}
    answer["target_box_input_512x288"] = event["target"]["box"]
    answer["target_box_source"] = inverse_box(event["target"]["box"], meta)
    if event["candidate"]:
        answer["candidate"] = {
            "score": event["candidate"]["score"],
            "box_input_512x288": event["candidate"]["box"],
            "box_source": inverse_box(event["candidate"]["box"], meta),
        }
    else:
        answer["candidate"] = None
    return answer


def select_cases(group, metadata, details):
    stages = {stage: {row["key"]: row for row in value["targets"]}
              for stage, value in details.items()}
    final = stages["step10"]
    ranked = []
    for key, row in final.items():
        outcomes = [stages[stage][key]["outcome"] for stage in ("E7", "step5", "step10")]
        reason = row["reason"]
        category = ("E7真阳性到第10步漏检" if outcomes[0] == "tp" and outcomes[2] == "fn" else
                    "E7漏检到第10步恢复" if outcomes[0] == "fn" and outcomes[2] == "tp" else
                    "持续漏检且保留地板无支撑" if all(x == "fn" for x in outcomes) and
                    reason == "fn_no_support_at_retained_floor_raw_candidate_unobserved" else
                    "第10步定位支撑不足" if "localization" in reason else
                    "第10步低分支撑" if reason == "fn_recovered_by_lowering_score_one_to_one" else
                    "其他漏检")
        priority = {"E7真阳性到第10步漏检": 0, "E7漏检到第10步恢复": 1,
                    "持续漏检且保留地板无支撑": 2, "第10步定位支撑不足": 3,
                    "第10步低分支撑": 4, "其他漏检": 5}[category]
        ranked.append((priority, row["target"]["box"][3] - row["target"]["box"][1], key, category))
    chosen, images, class_counts = [], set(), Counter()
    for _, _, key, category in sorted(ranked):
        row = final[key]
        if row["image_id"] in images or class_counts[row["class_name"]] >= 3:
            continue
        meta = metadata[row["image_id"]]
        chosen.append({
            "case_id": f"{group}_{len(chosen)+1:02d}", "type": "target_comparison",
            "category": category, "image_id": row["image_id"], "camera_id": row["camera_id"],
            "scene_id": row["scene_id"], "class_name": row["class_name"],
            "target_index": row["target_index"], "source_frame": meta["source_frame"],
            "source_image_sha256": meta["source_sha256"],
            "inverse_letterbox": meta["preprocess"]["letterbox_1280x720"],
            "stages": {stage: compact_event(stages[stage][key], meta)
                       for stage in ("E7", "step5", "step10")},
        })
        images.add(row["image_id"])
        class_counts[row["class_name"]] += 1
        if len(chosen) == 5:
            break
    for fp in sorted(details["step10"]["false_positives"],
                     key=lambda row: (-row["prediction"]["score"], row["image_id"])):
        if fp["image_id"] in images:
            continue
        meta = metadata[fp["image_id"]]
        chosen.append({
            "case_id": f"{group}_{len(chosen)+1:02d}", "type": "false_positive",
            "category": "第10步未匹配预测", "image_id": fp["image_id"],
            "camera_id": fp["camera_id"], "scene_id": fp["scene_id"],
            "class_name": fp["class_name"], "source_frame": meta["source_frame"],
            "source_image_sha256": meta["source_sha256"], "reason": fp["reason"],
            "prediction_score": fp["prediction"]["score"],
            "prediction_box_input_512x288": fp["prediction"]["box"],
            "prediction_box_source": inverse_box(fp["prediction"]["box"], meta),
            "truth_boxes_source": [inverse_box(row["target"]["box"], meta)
                                   for row in details["step10"]["targets"]
                                   if row["image_id"] == fp["image_id"]],
            "inverse_letterbox": meta["preprocess"]["letterbox_1280x720"],
        })
        break
    return chosen


def rect(box, css, title):
    x1, y1, x2, y2 = box
    return (f'<rect class="{css}" x="{x1:.3f}" y="{y1:.3f}" width="{x2-x1:.3f}" '
            f'height="{y2-y1:.3f}"><title>{html.escape(title)}</title></rect>')


def svg(meta, overlays, caption):
    letterbox = meta["preprocess"]["letterbox_1280x720"]
    width, height = letterbox["source_width"], letterbox["source_height"]
    uri = Path(meta["image"]).as_uri()
    return (f'<figure><svg viewBox="0 0 {width} {height}" role="img" '
            f'aria-label="{html.escape(caption)}"><image href="{html.escape(uri, quote=True)}" '
            f'width="{width}" height="{height}"/>{"".join(overlays)}</svg>'
            f'<figcaption>{html.escape(caption)}</figcaption></figure>')


def case_html(case, metadata):
    meta = metadata[case["image_id"]]
    raw = html.escape(Path(case["image_id"]).as_uri(), quote=True)
    if case["type"] == "target_comparison":
        panels = []
        for stage in ("E7", "step5", "step10"):
            event = case["stages"][stage]
            overlays = [rect(event["target_box_source"], "gt", "已有 GT")]
            if event["candidate"]:
                overlays.append(rect(event["candidate"]["box_source"], "candidate", "最相关保留预测"))
            panels.append(svg(meta, overlays,
                f'{stage}：{event["outcome"]}；{REASON_ZH.get(event["reason"], event["reason"])}'))
        body = ''.join(panels)
    else:
        overlays = [rect(box, "gt", "已有 GT") for box in case["truth_boxes_source"]]
        overlays.append(rect(case["prediction_box_source"], "candidate", "第10步未匹配预测"))
        body = svg(meta, overlays,
            f'第10步 FP：{REASON_ZH.get(case["reason"], case["reason"])}；score={case["prediction_score"]:.4f}')
    identity = case["camera_id"] or f'无显式 camera_id；scene_id={case["scene_id"]}'
    return (f'<article><h3>{html.escape(case["case_id"])} · {html.escape(case["category"])}</h3>'
            f'<p>{html.escape(case["class_name"])}；{html.escape(identity)}；帧 {case["source_frame"]}。'
            f'<a href="{raw}">打开原始无标注图</a></p><div class="panels">{body}</div></article>')


def table(headers, rows):
    return ('<table><thead><tr>' + ''.join(f'<th>{html.escape(str(v))}</th>' for v in headers) +
            '</tr></thead><tbody>' + ''.join('<tr>' + ''.join(
                f'<td>{html.escape(str(v))}</td>' for v in row) + '</tr>' for row in rows) +
            '</tbody></table>')


def build_html(output, metadata_by_group):
    summary_rows, camera_rows, size_rows = [], [], []
    for group, stages in output["reports"].items():
        for stage, report in stages.items():
            for name in CLASS_NAMES:
                counts = report["classes"][name]
                summary_rows.append((group, stage, name, counts["tp"], counts["fp"], counts["fn"],
                                     counts["ignored"], counts["tp_at_retained_floor"]))
            for camera, classes in report["camera_groups"].items():
                for name, counts in classes.items():
                    camera_rows.append((group, stage, camera, name, counts.get("gt", 0),
                                        counts.get("tp", 0), counts.get("fp", 0), counts.get("fn", 0)))
            for key, counts in report["size_groups_input_512x288"].items():
                name, bucket = key.split("/", 1)
                size_rows.append((group, stage, name, bucket, counts.get("total", 0),
                                  counts.get("tp", 0), counts.get("fn", 0)))
    cards = ''.join(case_html(case, metadata_by_group[case["case_id"].split("_")[0]])
                    for case in output["selected_examples"])
    return f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>AC 当前学生误差分布</title><style>
body{{font:15px/1.55 system-ui,sans-serif;margin:24px;background:#f3f5f7;color:#18202a}}main{{max-width:1500px;margin:auto}}
h1,h2,h3{{line-height:1.25}}.note,article{{background:white;padding:16px;margin:16px 0;border-radius:8px}}
table{{border-collapse:collapse;width:100%;background:white;margin:10px 0 24px}}th,td{{border:1px solid #ccd3da;padding:6px;text-align:right}}th:first-child,td:first-child{{text-align:left}}
.panels{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:10px}}figure{{margin:0}}svg{{display:block;width:100%;background:#111}}
rect{{fill:none;vector-effect:non-scaling-stroke}}.gt{{stroke:#20e070;stroke-width:3}}.candidate{{stroke:#ff9d24;stroke-width:3}}figcaption{{font-size:13px}}
</style><main><h1>AC 当前学生：已保存预测误差分布</h1>
<p class="note">只读诊断，不是正式验收。绿色是已有 GT，橙色是已保存预测；框通过清单中的 letterbox 参数反算回原图坐标。预测仅覆盖分数地板 3276/65536（约 0.05）之后的后处理输出：无保留支撑不等于无原始候选，也不能据此证明 NMS 原因。两类标签只有 person/vehicle，未自动推断车型或动静状态。旧 256 清单没有显式 camera_id，因此不伪造相机分组，只在 JSON 中另报显式 scene_id。</p>
<p><a href="diagnosis.json">完整 JSON</a> · <a href="receipt.json">哈希收据</a></p>
<h2>精确 TP/FP/FN（score=0.5）</h2>{table(("数据","阶段","类别","TP","FP","FN","忽略","约0.05地板TP"), summary_rows)}
<h2>17 图真实 camera_id 分组</h2>{table(("数据","阶段","camera_id","类别","GT","TP","FP","FN"), camera_rows)}
<h2>512×288 输入框高度分桶</h2>{table(("数据","阶段","类别","高度桶","GT","TP","FN"), size_rows)}
<h2>关键样例（{len(output["selected_examples"])}，上限 12）</h2>{cards}</main></html>'''


def self_check():
    gt = [{"image_id": "a", "label": 0, "box": [0, 0, 4, 4]},
          {"image_id": "a", "label": 0, "box": [10, 10, 14, 14]}]
    pred = [dict(gt[0], score=.9), dict(gt[0], score=.8),
            {"image_id": "a", "label": 0, "box": [10, 10, 14, 14], "score": .2}]
    result = {"truth": gt, "predictions": pred, "ignores": [],
              "diagnostic_metrics_at_0_5": metric_report(pred, gt, thresholds=(.5, .5))}
    meta = {"a": {"image": "a", "camera_id": "camera-real", "scene_id": "scene-real",
                   "preprocess": {"letterbox_1280x720": {"source_width": 512, "source_height": 288,
                       "scale_x": 2.5, "scale_y": 2.5, "offset_x": 0, "offset_y": 0}}}}
    answer = detail(result, meta)
    assert answer["totals"]["person"] == Counter(gt=2, tp=1, fp=1, fn=1, ignored=0)
    assert next(row for row in answer["targets"] if row["target_index"] == 1)["reason"] == \
        "fn_recovered_by_lowering_score_one_to_one"
    assert grouped_counts(answer, "camera_id")["camera-real"]["person"]["gt"] == 2
    assert inverse_box([1, 2, 3, 4], meta["a"]) == [1, 2, 3, 4]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    self_check()
    if args.self_test:
        print("PASS saved prediction aggregation, camera metadata, and inverse letterbox")
        return
    output = {
        "status": "saved_prediction_diagnosis_not_formal_acceptance",
        "training_started": False, "labels_changed": False, "gpu_used": False,
        "input_space": [512, 288], "score_threshold": .5,
        "reports": {}, "selected_examples": [],
        "limitations": [
            "Saved predictions begin at score floor 3276/65536; raw pre-TopK/NMS candidates were not inspected.",
            "No NMS cause is claimed without pre-NMS evidence.",
            "Two-class labels cannot establish vehicle subtype or motion/static state.",
        ],
    }
    metadata_by_group, details_by_group = {}, {}
    for group in REPORTS:
        metadata, loaded = load_group(group)
        metadata_by_group[group], details_by_group[group] = metadata, {}
        output["reports"][group] = {}
        for stage, result in loaded.items():
            details = detail(result, metadata)
            details_by_group[group][stage] = details
            output["reports"][group][stage] = aggregate(group, stage, result, metadata, details)
        output["selected_examples"].extend(select_cases(group, metadata, details_by_group[group]))
    assert len(output["selected_examples"]) <= 12
    diagnosis_path, html_path = HERE / "diagnosis.json", HERE / "index.html"
    diagnosis_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    html_path.write_text(build_html(output, metadata_by_group), encoding="utf-8")
    receipt = {
        "status": "complete_read_only_saved_prediction_diagnosis",
        "inputs_sha256": {path.relative_to(ROOT).as_posix(): sha256(path)
                          for path in [*MANIFESTS.values(),
                              *(path for reports in REPORTS.values() for path in reports.values())]},
        "sources_sha256": {path.relative_to(ROOT).as_posix(): sha256(path)
                           for path in (*SOURCE_FILES, Path(__file__))},
        "outputs_sha256": {"diagnosis.json": sha256(diagnosis_path), "index.html": sha256(html_path)},
        "assertions": {"six_reports_match_saved_tp_fp_fn_ignored": True,
                       "selected_examples_at_most_12": True,
                       "camera_groups_use_explicit_camera_id_only": True,
                       "inverse_letterbox_from_manifest": True},
        "command": "CUDA_VISIBLE_DEVICES='' E:/project/qiansai/.tools/road_yolo_venv/Scripts/python.exe -B run.py",
        "training_started": False, "labels_changed": False, "gpu_used": False,
    }
    (HERE / "receipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"reports": {group: {stage: {name: {key: report["classes"][name][key]
        for key in ("tp", "fp", "fn", "ignored")} for name in CLASS_NAMES}
        for stage, report in stages.items()} for group, stages in output["reports"].items()},
        "selected_examples": len(output["selected_examples"]), "output": str(HERE)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
