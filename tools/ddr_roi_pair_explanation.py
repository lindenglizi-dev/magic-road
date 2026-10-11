#!/usr/bin/env python3
"""Re-index three saved ROI flip pairs without rerunning crops or models."""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import io
import json
import shutil
from pathlib import Path
from typing import Any

import cv2
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "evaluation/ddr_architecture/roi_failure_ledger_20261001_v2"
CROP = ROOT / "evaluation/local_scene_pilots/intersection_2415171_crop_change_v2"
MARGIN = ROOT / "evaluation/local_scene_pilots/intersection_2415171_margin_change_v1"
MODEL = ROOT / "external_reference_exploration/results/opencv_hog_diagnostic/model_parameters.json"
OUTPUT = ROOT / "evaluation/ddr_architecture/roi_pair_explanation_20261001_v1"
IDENTITIES = ((360, "p01"), (690, "p02"), (1050, "p02"))


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_array(array: np.ndarray) -> str:
    return hashlib.sha256(np.ascontiguousarray(array).tobytes()).hexdigest()


def dump_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def assert_close(actual: float, expected: float, label: str, tolerance: float = 2e-9) -> None:
    if abs(actual - expected) > tolerance:
        raise AssertionError(f"{label}: {actual} != {expected}")


def resize_map(size: int) -> list[int]:
    positions = np.arange(32, dtype=np.int64)
    return np.minimum((size * (4 + 8 * positions)) >> 8, size - 1).astype(int).tolist()


def geometry(box: list[int]) -> dict[str, Any]:
    width = box[2] - box[0] + 1
    height = box[3] - box[1] + 1
    return {
        "inclusive_box": box,
        "width": width,
        "height": height,
        "resize_output": [32, 32],
        "resize_contract": "pixel-centre Q8 nearest-neighbour DDA",
        "x_source_indices_within_crop": resize_map(width),
        "y_source_indices_within_crop": resize_map(height),
    }


def verify_declared_hash(path: Path, expected: str) -> None:
    actual = sha256_file(path)
    if actual != expected:
        raise AssertionError(f"source hash mismatch: {path}: {actual} != {expected}")


def csv_bytes(rows: list[dict[str, Any]]) -> bytes:
    fields = list(rows[0])
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def build() -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, str]]:
    ledger_receipt = read_json(LEDGER / "receipt.json")
    crop_receipt = read_json(CROP / "receipt.json")
    margin_receipt = read_json(MARGIN / "receipt.json")
    sources = {
        "evaluation/ddr_architecture/roi_failure_ledger_20261001_v2/roi_failure_ledger.json": LEDGER / "roi_failure_ledger.json",
        "evaluation/local_scene_pilots/intersection_2415171_crop_change_v2/all_targets.json": CROP / "all_targets.json",
        "evaluation/local_scene_pilots/intersection_2415171_margin_change_v1/score_changes.json": MARGIN / "score_changes.json",
        "evaluation/local_scene_pilots/intersection_2415171_margin_change_v1/vectors.npz": MARGIN / "vectors.npz",
        "external_reference_exploration/results/opencv_hog_diagnostic/model_parameters.json": MODEL,
    }
    declared = {
        str(LEDGER / "roi_failure_ledger.json"): ledger_receipt["artifact_hashes"]["roi_failure_ledger.json"],
        str(CROP / "all_targets.json"): crop_receipt["artifact_hashes"]["all_targets.json"],
        str(MARGIN / "score_changes.json"): margin_receipt["artifact_hashes"]["score_changes.json"],
        str(MARGIN / "vectors.npz"): margin_receipt["artifact_hashes"]["vectors.npz"],
        str(MODEL): margin_receipt["models"]["model_parameters_sha256"],
    }
    for path_text, expected in declared.items():
        verify_declared_hash(Path(path_text), expected)

    ledger_by_id = {(row["frame_id"], row["track_id"]): row for row in read_json(LEDGER / "roi_failure_ledger.json")["records"]}
    crop_by_id = {(row["frame_index"], row["track_id"]): row for row in read_json(CROP / "all_targets.json")}
    margin_by_id = {(row["frame_index"], row["track_id"]): row for row in read_json(MARGIN / "score_changes.json")}
    model = read_json(MODEL)["opencv_hog324"]
    if model["decision_score_positive_class"] != "vehicle" or model["class_order"] != ["ped", "vehicle"]:
        raise AssertionError("unexpected model class contract")
    weights_float = np.asarray(model["folded_weights_on_raw_features"], dtype=np.float64)
    bias_float = float(model["folded_bias_on_raw_features"])
    weight_scale = 32767.0 / float(np.max(np.abs(weights_float)))

    pairs: list[dict[str, Any]] = []
    contributions: list[dict[str, Any]] = []
    image_sources: dict[str, str] = {}
    with np.load(MARGIN / "vectors.npz") as vectors:
        weights_q = vectors["weight_q"].astype(np.int64)
        bias_q = int(vectors["bias_q"][0])
        if not np.array_equal(weights_q, np.rint(weights_float * weight_scale).astype(np.int64)):
            raise AssertionError("saved quantized weights do not match the hash-bound model contract")
        if bias_q != round(bias_float * 4096 * weight_scale):
            raise AssertionError("saved quantized bias does not match the hash-bound model contract")

        for frame, track in IDENTITIES:
            identity = f"f{frame:06d}_{track}"
            ledger_row = ledger_by_id[(frame, track)]
            crop_row = crop_by_id[(frame, track)]
            margin_row = margin_by_id[(frame, track)]
            if ledger_row["failure_kind"] != "geometry_match_retained_but_hog324_prediction_flipped":
                raise AssertionError(f"unexpected ledger kind: {identity}")
            if not margin_row["classification_flipped"] or crop_row["prediction_transition"] != "correct_to_wrong":
                raise AssertionError(f"flip identity mismatch: {identity}")

            sides: dict[str, Any] = {}
            arrays: dict[str, dict[str, np.ndarray]] = {}
            for side, crop_key, ledger_key, score_key in (
                ("baseline", "baseline_match", "current", "before_score"),
                ("min_run1", "minrun_match", "keep_all", "after_score"),
            ):
                prefix = f"{identity}_{'before' if side == 'baseline' else 'after'}"
                candidate = crop_row[crop_key]
                ledger_candidate = ledger_row[ledger_key]
                score = margin_row[score_key]
                if candidate["analysis_box"] != ledger_candidate["analysis_bbox_inclusive"]:
                    raise AssertionError(f"analysis box mismatch: {identity} {side}")
                if candidate["source_box"] != ledger_candidate["source_bbox_inclusive"]:
                    raise AssertionError(f"source box mismatch: {identity} {side}")
                if candidate["score"] != score:
                    raise AssertionError(f"score dictionary mismatch: {identity} {side}")

                roi = vectors[prefix + "_roi"]
                feature_float = vectors[prefix + "_features_float"]
                feature_q = vectors[prefix + "_features_q"]
                products_q = vectors[prefix + "_products_q"]
                accumulator = vectors[prefix + "_acc_bias_first_q"]
                roi_rel = crop_row["baseline_roi_path" if side == "baseline" else "minrun_roi_path"]
                roi_path = CROP / roi_rel
                expected_png_hash = crop_receipt["artifact_hashes"][roi_rel]
                verify_declared_hash(roi_path, expected_png_hash)
                decoded = cv2.imread(str(roi_path), cv2.IMREAD_GRAYSCALE)
                if decoded is None or not np.array_equal(decoded, roi):
                    raise AssertionError(f"saved PNG and NPZ ROI mismatch: {identity} {side}")
                if sha256_array(roi) != candidate["roi_pixel_sha256"]:
                    raise AssertionError(f"ROI pixel hash mismatch: {identity} {side}")
                if sha256_array(feature_float.astype("<f8")) != score["hog324_feature_sha256"]:
                    raise AssertionError(f"HOG324 feature hash mismatch: {identity} {side}")
                if not np.array_equal(products_q, feature_q * weights_q):
                    raise AssertionError(f"saved products mismatch: {identity} {side}")
                rebuilt_acc = np.cumsum(np.r_[np.int64(bias_q), products_q], dtype=np.int64)
                if not np.array_equal(accumulator, rebuilt_acc):
                    raise AssertionError(f"saved accumulator mismatch: {identity} {side}")
                q_score = int(accumulator[-1])
                if q_score != int(score["hog324_q_score_integer"]):
                    raise AssertionError(f"integer score mismatch: {identity} {side}")
                float_score = float(feature_float @ weights_float + bias_float)
                assert_close(float_score, float(score["hog324_float_score"]), f"float score {identity} {side}")
                normalized = q_score / (4096 * weight_scale)
                assert_close(normalized, float(score["hog324_q_score_normalized"]), f"normalized score {identity} {side}")

                output_image = f"images/{identity}_{side}_roi32.png"
                image_sources[output_image] = str(roi_path.relative_to(ROOT)).replace("\\", "/")
                sides[side] = {
                    "candidate_id": candidate["candidate_id"],
                    "component_label": candidate["component_label"],
                    "component_area": candidate["component_area"],
                    "candidate_rank": candidate["rank"],
                    "analysis_crop": geometry(candidate["analysis_box"]),
                    "source_sample_footprint_inclusive": candidate["source_box"],
                    "iou_with_ground_truth": candidate["iou_with_gt"],
                    "saved_roi": {
                        "copied_path": output_image,
                        "source_path": image_sources[output_image],
                        "png_sha256": expected_png_hash,
                        "pixel_sha256": candidate["roi_pixel_sha256"],
                    },
                    "saved_scores": score,
                    "saved_hog324_vectors": {
                        "npz_prefix": prefix,
                        "dimension": 324,
                        "float_feature_sha256": score["hog324_feature_sha256"],
                        "quantized_feature_sha256": sha256_array(feature_q.astype("<i8")),
                        "quantized_products_sha256": sha256_array(products_q.astype("<i8")),
                        "bias_first_accumulator_sha256": sha256_array(accumulator.astype("<i8")),
                    },
                }
                arrays[side] = {
                    "feature_float": feature_float,
                    "feature_q": feature_q,
                    "products_q": products_q,
                    "accumulator": accumulator,
                }

            before = arrays["baseline"]
            after = arrays["min_run1"]
            product_delta = after["products_q"] - before["products_q"]
            integer_delta = int(after["accumulator"][-1] - before["accumulator"][-1])
            if int(product_delta.sum()) != integer_delta or integer_delta != margin_row["integer_score_delta"]:
                raise AssertionError(f"integer delta reconstruction mismatch: {identity}")
            float_terms = weights_float * (after["feature_float"] - before["feature_float"])
            float_delta = float(float_terms.sum())
            assert_close(float_delta, margin_row["float_delta"], f"float delta {identity}")
            order = sorted(range(324), key=lambda i: (-abs(int(product_delta[i])), i))[:12]
            stored_top = [(row["feature_index"], row["product_delta"]) for row in margin_row["largest_feature_delta_terms"]]
            rebuilt_top = [(i, int(product_delta[i])) for i in order]
            if rebuilt_top != stored_top:
                raise AssertionError(f"stored top contribution mismatch: {identity}")
            for index in range(324):
                contributions.append({
                    "identity": identity,
                    "feature_index": index,
                    "baseline_feature_float": format(float(before["feature_float"][index]), ".17g"),
                    "min_run1_feature_float": format(float(after["feature_float"][index]), ".17g"),
                    "float_score_delta_contribution": format(float(float_terms[index]), ".17g"),
                    "baseline_feature_q": int(before["feature_q"][index]),
                    "min_run1_feature_q": int(after["feature_q"][index]),
                    "weight_q": int(weights_q[index]),
                    "baseline_product_q": int(before["products_q"][index]),
                    "min_run1_product_q": int(after["products_q"][index]),
                    "integer_score_delta_contribution": int(product_delta[index]),
                })
            abs_total = sum(abs(int(value)) for value in product_delta)
            abs_top = sum(abs(value) for _, value in rebuilt_top)
            pairs.append({
                "identity": identity,
                "ground_truth": {
                    "class": crop_row["label"],
                    "visibility": crop_row["visibility"],
                    "source_bbox_inclusive": crop_row["gt_box"],
                },
                "observed": {
                    "component_relation": ledger_row["component_relation"],
                    "overlapping_baseline_component_labels": ledger_row["overlapping_current_component_labels"],
                    "shape_relation": crop_row["shape_relation"],
                    "baseline": sides["baseline"],
                    "min_run1": sides["min_run1"],
                    "hog324_float_score_delta": margin_row["float_delta"],
                    "hog324_integer_score_delta": integer_delta,
                    "hog324_integer_delta_reconstructed_from_324_saved_products": int(product_delta.sum()),
                    "changed_quantized_feature_count": int(np.count_nonzero(after["feature_q"] != before["feature_q"])),
                    "largest_saved_integer_product_delta_terms": margin_row["largest_feature_delta_terms"],
                    "top12_absolute_product_delta_share": abs_top / abs_total if abs_total else 0.0,
                },
                "inference": (
                    "The changed inclusive crop and saved ROI pixels changed the stored HOG324 features; "
                    "their linear contributions exactly reconstruct the ped-to-vehicle score crossing."
                ),
                "inference_limit": (
                    "Feature indices are raw OpenCV descriptor order. They are not assigned a visual or spatial "
                    "meaning here, and the evidence does not identify which object owns an edge."
                ),
            })

    result = {
        "schema": "ddr_roi_pair_explanation_v1",
        "scope": "Historical saved-artifact re-index only; no video decode, crop, feature extraction, model run, training, or threshold scan.",
        "model_contract": {
            "artifact_status": model["status"],
            "positive_class": "vehicle",
            "decision_rule": "score >= 0 is vehicle; score < 0 is ped",
            "float_score": "sum(weight_float[i] * saved_feature_float[i]) + bias_float",
            "integer_score": "bias_q followed by feature_q[i] * weight_q[i], i=0..323, signed int64 reference",
            "feature_quantization": "round-to-nearest Q1.12 (scale 4096)",
            "weight_quantization": "round(weight * (32767 / max_abs_weight)) to signed 16-bit",
            "deployment_boundary": "The hash-bound HOG324 artifact declares diagnostic_float_model_not_frozen_not_rtl.",
        },
        "crop_contract": {
            "input": "inclusive crop on the saved 256x144 stride-5 analysis grayscale plane",
            "source_mapping": "[x0*5,y0*5,min(1279,x1*5+4),min(719,y1*5+4)] inclusive sample footprint",
            "resize": "32x32 uint8 via fpga_resize_roi pixel-centre Q8 nearest-neighbour DDA",
            "axis_index_formula": "min((input_size * (4 + 8 * output_index)) >> 8, input_size - 1)",
        },
        "pairs": pairs,
        "missing_saved_evidence": [
            "Full HOG64 feature vectors and per-feature contributions were not saved; only their feature hashes, scores, and predictions exist.",
            "No verified semantic mapping from OpenCV HOG324 feature index to a named spatial/orientation bin was saved.",
            "No integer-gradient/bin HOG324 or RTL feature/score trace exists for these pairs.",
            "No saved evidence identifies the visual owner or semantic cause of each changed edge.",
        ],
        "conclusion": {
            "observed": "All three saved baseline crops score ped and all three saved min_run1 crops score vehicle in both HOG324 float and quantized linear paths; each exact score delta is reconstructed from saved features/products.",
            "inferred": "Crop-content change is sufficient to explain the arithmetic flips in these three instances.",
            "not_supported": "The evidence does not justify a universal expand/shrink rule, retaining an old class, retraining, threshold changes, or RTL deployment of HOG324.",
        },
    }
    return result, contributions, {name: sha256_file(path) for name, path in sources.items()}


def render_markdown(data: dict[str, Any]) -> str:
    lines = [
        "# 三个 ROI 翻转实例的成对解释",
        "",
        "本报告只重整已保存的 ROI、裁剪参数、评分和特征向量；未解码视频、未重裁剪、未提取新特征、未运行模型、未训练或扫描阈值。",
        "",
        "## 成对结果",
        "",
        "| 实例 | analysis crop（baseline → min_run1） | HOG324 float（baseline → min_run1） | HOG324 Q（baseline → min_run1） | 量化增量重构 |",
        "|---|---|---|---|---|",
    ]
    for pair in data["pairs"]:
        old = pair["observed"]["baseline"]
        new = pair["observed"]["min_run1"]
        old_score = old["saved_scores"]
        new_score = new["saved_scores"]
        old_box = old["analysis_crop"]["inclusive_box"]
        new_box = new["analysis_crop"]["inclusive_box"]
        delta = pair["observed"]["hog324_integer_score_delta"]
        lines.append(
            f"| {pair['identity']} | `{old_box}` → `{new_box}` | "
            f"{old_score['hog324_float_score']} ped → {new_score['hog324_float_score']} vehicle | "
            f"{old_score['hog324_q_score_integer']} ped → {new_score['hog324_q_score_integer']} vehicle | "
            f"{delta} = Σ324 product delta |"
        )
    lines += [
        "",
        "每个实例的 baseline/min_run1 图像是原 PNG 的逐字节复制。`pair_explanations.json` 给出闭区间 analysis/source 框、输入宽高、32 个 x/y 最近邻采样索引、ROI 像素哈希、HOG64/HOG324 原始已存评分和向量键。`feature_contributions.csv` 展开三组 324 维已存特征、乘积与 delta。",
        "",
        "## 观测与推断",
        "",
        "**观测：** 三例的新框都包含旧框，ROI 像素哈希均改变；HOG324 浮点与量化路径均由 ped 翻为 vehicle。量化分数增量分别由 324 个已存乘积差精确重构，浮点分数也由已存特征和哈希绑定的线性权重复核。",
        "",
        "**推断：** 在这三例中，裁剪内容变化足以解释线性评分越过零点。贡献最大的特征索引只解释算术，不证明哪个视觉对象或方向结构造成翻转。",
        "",
        "## 明确缺失",
        "",
    ]
    lines.extend(f"- {item}" for item in data["missing_saved_evidence"])
    lines += [
        "",
        "HOG324 工件自身状态是 `diagnostic_float_model_not_frozen_not_rtl`；这里的“冻结”仅指输入文件由哈希和收据锁定，不表示部署模型已冻结。三个例子不支持统一扩框/缩框、沿用旧类别、改阈值、重新训练或 RTL 接入。",
        "",
    ]
    return "\n".join(lines)


def render_html(data: dict[str, Any]) -> str:
    cards = []
    for pair in data["pairs"]:
        observed = pair["observed"]
        old, new = observed["baseline"], observed["min_run1"]
        top = "".join(
            f"<tr><td>{row['feature_index']}</td><td>{row['product_delta']}</td></tr>"
            for row in observed["largest_saved_integer_product_delta_terms"][:6]
        )
        cards.append(f"""
<section><h2>{html.escape(pair['identity'])}</h2><div class="rois">
<figure><img src="{old['saved_roi']['copied_path']}"><figcaption>baseline<br>{old['analysis_crop']['inclusive_box']}<br>float {old['saved_scores']['hog324_float_score']} / Q {old['saved_scores']['hog324_q_score_integer']} → ped</figcaption></figure>
<figure><img src="{new['saved_roi']['copied_path']}"><figcaption>min_run1<br>{new['analysis_crop']['inclusive_box']}<br>float {new['saved_scores']['hog324_float_score']} / Q {new['saved_scores']['hog324_q_score_integer']} → vehicle</figcaption></figure>
</div><p>Δfloat={observed['hog324_float_score_delta']:.12g}; ΔQ={observed['hog324_integer_score_delta']}; changed Q features={observed['changed_quantized_feature_count']}/324.</p>
<details><summary>largest saved integer product deltas</summary><table><tr><th>feature</th><th>Δproduct</th></tr>{top}</table></details></section>""")
    return f"""<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>ROI pair explanations</title>
<style>body{{font:16px system-ui;max-width:1000px;margin:30px auto;color:#222}}section{{border-top:1px solid #bbb;padding:18px 0}}.rois{{display:flex;gap:48px}}figure{{margin:0}}img{{width:256px;height:256px;image-rendering:pixelated;border:1px solid #555}}figcaption{{line-height:1.5}}table{{border-collapse:collapse}}td,th{{border:1px solid #bbb;padding:4px 9px}}code{{background:#eee}}</style>
<h1>三个 ROI 翻转实例的成对解释</h1><p>仅展示已保存工件。图像是已有 32×32 PNG 的逐字节复制；没有重跑视频、裁剪、特征或模型。</p>{''.join(cards)}
<h2>边界</h2><p>特征索引仅解释线性算术，不作空间/方向语义映射。HOG324 工件状态为 <code>diagnostic_float_model_not_frozen_not_rtl</code>。</p></html>"""


def generate() -> None:
    if OUTPUT.exists() and any(OUTPUT.iterdir()):
        raise ValueError(f"new or empty output directory required: {OUTPUT}")
    data, contribution_rows, input_hashes = build()
    (OUTPUT / "images").mkdir(parents=True)
    for pair in data["pairs"]:
        for side in ("baseline", "min_run1"):
            saved = pair["observed"][side]["saved_roi"]
            shutil.copyfile(ROOT / saved["source_path"], OUTPUT / saved["copied_path"])
    dump_json(OUTPUT / "pair_explanations.json", data)
    (OUTPUT / "feature_contributions.csv").write_bytes(csv_bytes(contribution_rows))
    (OUTPUT / "report.md").write_text(render_markdown(data), encoding="utf-8")
    (OUTPUT / "report.html").write_text(render_html(data), encoding="utf-8")
    artifacts = {
        str(path.relative_to(OUTPUT)).replace("\\", "/"): sha256_file(path)
        for path in sorted(OUTPUT.rglob("*")) if path.is_file()
    }
    receipt = {
        "schema": "ddr_roi_pair_explanation_receipt_v1",
        "status": "PASS_historical_saved_artifact_reindex_only",
        "command": ["python", "tools/ddr_roi_pair_explanation.py"],
        "script_sha256": sha256_file(Path(__file__)),
        "input_hashes": input_hashes,
        "input_receipt_hashes": {
            str(path.relative_to(ROOT)).replace("\\", "/"): sha256_file(path)
            for path in (LEDGER / "receipt.json", CROP / "receipt.json", MARGIN / "receipt.json")
        },
        "artifact_hashes": artifacts,
        "self_check": {
            "status": "PASS",
            "pair_count": 3,
            "roi_png_npz_pixel_matches": 6,
            "float_score_reconstruction_mismatches": 0,
            "integer_score_reconstruction_mismatches": 0,
            "product_delta_reconstruction_mismatches": 0,
            "identities": [pair["identity"] for pair in data["pairs"]],
        },
        "boundaries": [
            "No video decode, source-frame read, crop, resize, feature extraction, model inference, training, or threshold scan.",
            "Saved ROI PNG pixels were decoded only to prove identity with the saved NPZ ROI arrays.",
            "Scores were reconstructed only from saved features/products and hash-bound linear parameters.",
            "Observed feature contributions are arithmetic facts, not semantic or visual-cause labels.",
        ],
    }
    dump_json(OUTPUT / "receipt.json", receipt)
    print(json.dumps(receipt["self_check"], ensure_ascii=False, indent=2))


def check_existing() -> None:
    receipt = read_json(OUTPUT / "receipt.json")
    if receipt["script_sha256"] != sha256_file(Path(__file__)):
        raise AssertionError("script hash mismatch")
    for relative, expected in receipt["input_hashes"].items():
        verify_declared_hash(ROOT / relative, expected)
    for relative, expected in receipt["input_receipt_hashes"].items():
        verify_declared_hash(ROOT / relative, expected)
    for relative, expected in receipt["artifact_hashes"].items():
        verify_declared_hash(OUTPUT / relative, expected)
    data, rows, _ = build()
    if data != read_json(OUTPUT / "pair_explanations.json"):
        raise AssertionError("pair explanation content mismatch")
    if hashlib.sha256(csv_bytes(rows)).hexdigest() != receipt["artifact_hashes"]["feature_contributions.csv"]:
        raise AssertionError("feature contribution content mismatch")
    print(json.dumps(receipt["self_check"], ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    check_existing() if args.check_only else generate()


if __name__ == "__main__":
    main()
