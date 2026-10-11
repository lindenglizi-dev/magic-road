"""Read-only CPU attribution of the fixed tiny-fit mistakes, with stage parity."""
from collections import Counter
import html
import json
from pathlib import Path
import shutil

import numpy as np
from PIL import Image, ImageDraw, ImageOps
import torch

from .analyze_detection_errors import ious, match
from .integer import exponent, postprocess, round_div_even, sigmoid, _overlap_half
from .loss import decode_outputs
from .metrics import evaluate
from .model import RoadYOLOS4
from .prepare_tiny_fit import OUTPUT, ROOT, RUN, guard_row, write_json
from .run_tiny_fit import verify_prepared
from .score_tiny_fit import validate_candidate
from .train import FullFrameDataset, load_dataset_snapshot, sha256

DEST = ROOT / "cnn/reports/tiny_fit_followup_20261009_v1"
WEIGHT_SHA = "0fdf59c746780120ffa36940c4da8202e103dbb9b5f21b7bcec3d5a3318f3aa5"
SCORE_SHA = "6566c010c5e756fe70296d3e9fab207c0f31ec7d55865f4f70b9dce4b3c7eede"
REASONS = {
    "low_confidence": "框已匹配，分数低于0.5",
    "shared_candidate": "候选与其他GT竞争，不能一框算两个目标",
    "NMS_support_lost": "有重叠支持候选被NMS抑制，需结合相邻GT看",
    "TopK_support_lost": "有支持候选未进入Top128",
    "output_cap_support_lost": "支持候选在每类32框上限之后",
    "float_fixed_difference": "浮点支持与定点查表/解码支持不同",
    "below_score_floor": "原始框有支持，但同类分数低于约0.05",
    "other_class_support": "仅另一类别保留框有较高重叠，不能直接证明错类",
    "localization": "有候选，但框位置/范围未达IoU0.5",
    "no_IoU25_support": "当前原始框也无IoU0.25支持，原因仍未定",
    "false_positive": "score0.5的一对一匹配未匹配预测",
}


def assign(predictions, targets, threshold):
    """Return GT->prediction pairs, preserving the shared evaluator's tie rules."""
    matrix = ious(predictions, targets)
    pairs = {}
    for index, row in enumerate(predictions):
        if row["score"] < threshold:
            continue
        available = [j for j in range(len(targets)) if j not in pairs]
        best = max(available, key=lambda j: (matrix[index, j], -j), default=None)
        if best is not None and matrix[index, best] >= .5:
            pairs[best] = index
    used, true, _, _ = match(predictions, matrix, np.zeros(len(predictions), dtype=bool), threshold)
    assert set(pairs) == used and set(pairs.values()) == true
    return pairs


def trace_heads(heads):
    """Mirror stages only for observation; compare final results to production reference."""
    raw, grids, strides = [], [], []
    for head, stride in zip(heads, (4, 8, 16), strict=True):
        y, x = np.indices(head.shape[:2])
        grids.append(np.stack((x, y), -1).reshape(-1, 2))
        strides.append(np.full((y.size, 1), stride, dtype=np.int64))
        raw.append(head.reshape(-1, 7).astype(np.int64))
    raw, grid, stride = np.concatenate(raw), np.concatenate(grids), np.concatenate(strides)
    center = (raw[:, :2] + grid * 256) * stride
    size = round_div_even(exponent(raw[:, 2:4]).astype(np.int64) * stride, 4)
    half = round_div_even(size, 2)
    boxes = np.clip(np.concatenate((center - half, center + half), 1), 0,
                    [512 * 256, 288 * 256] * 2)
    probability = sigmoid(raw[:, 4:]).astype(np.int64)
    scores = round_div_even(probability[:, :1] * probability[:, 1:], 65536)
    valid = np.all(boxes[:, 2:] > boxes[:, :2], axis=1)
    classes, golden = [], postprocess(heads, (3276, 3276))
    for label in (0, 1):
        above = np.flatnonzero(scores[:, label] >= 3276)
        ranked = sorted(above.tolist(), key=lambda cell: (-int(scores[cell, label]), cell))
        top = ranked[:128]
        kept, removed = [], {}
        for cell in top:
            if len(kept) == 32:
                removed[cell] = dict(stage="output_cap32")
            elif not valid[cell]:
                removed[cell] = dict(stage="degenerate_box")
            else:
                suppressor = next((old for old in kept if _overlap_half(
                    tuple(boxes[cell]), tuple(boxes[old]))), None)
                if suppressor is None:
                    kept.append(cell)
                else:
                    removed[cell] = dict(stage="NMS", suppressor_cell=suppressor)
        def records(cells):
            return [dict(label=label, cell_id=int(cell), box=(boxes[cell] / 256).tolist(),
                         score=int(scores[cell, label]) / 65536) for cell in cells if valid[cell]]
        final = records(kept)
        expected = [dict(label=row["label"], cell_id=row["cell_id"],
                         box=[v / 256 for v in row["box_q8"]], score=row["score_uint16"] / 65536)
                    for row in golden if row["label"] == label]
        assert final == expected, "traced final output differs from integer.postprocess"
        classes.append(dict(pre_top=records(ranked), top=records(top), final=final,
                            removed=removed, above_floor_count=len(ranked)))
    return boxes / 256, scores / 65536, classes


def support(records, target):
    if not records:
        return dict(best_IoU=0., candidate=None, supporting_cells=[])
    values = ious(records, [target])[:, 0]
    index = max(range(len(records)), key=lambda j: (values[j], records[j]["score"], -j))
    return dict(best_IoU=float(values[index]), candidate=records[index],
                supporting_cells=[row["cell_id"] for j, row in enumerate(records) if values[j] >= .5])


def reason_for(stages, removed):
    if stages["final"]["supporting_cells"]:
        return "shared_candidate"
    for cell in stages["top"]["supporting_cells"]:
        if removed.get(cell, {}).get("stage") == "NMS":
            return "NMS_support_lost"
        if removed.get(cell, {}).get("stage") == "output_cap32":
            return "output_cap_support_lost"
    if stages["pre_top"]["supporting_cells"]:
        return "TopK_support_lost"
    if stages["float_floor"]["supporting_cells"]:
        return "float_fixed_difference"
    if stages["float_all"]["supporting_cells"]:
        return "below_score_floor"
    if stages["other_class_final"]["supporting_cells"]:
        return "other_class_support"
    if max(stages[key]["best_IoU"] for key in ("float_all", "fixed_all")) >= .25:
        return "localization"
    return "no_IoU25_support"


def render_case(case, pixels, row, targets, predictions, folder):
    raw = Image.fromarray(pixels)
    annotated = raw.copy()
    draw = ImageDraw.Draw(annotated)
    for target in targets:
        draw.rectangle(target["box"], outline="#777777", width=1)
    for prediction in predictions:
        if prediction["score"] >= .5:
            draw.rectangle(prediction["box"], outline="#00cfff", width=1)
    draw.rectangle(case["target"]["box"], outline="#00ff00", width=2)
    candidate = case["selected_candidate"]
    if candidate:
        draw.rectangle(candidate["box"], outline="#ff9900", width=2)
    box = case["target"]["box"]
    if candidate:
        box = [min(box[0], candidate["box"][0]), min(box[1], candidate["box"][1]),
               max(box[2], candidate["box"][2]), max(box[3], candidate["box"][3])]
    crop_box = (max(0, int(box[0]) - 12), max(0, int(box[1]) - 12),
                min(512, int(np.ceil(box[2])) + 12), min(288, int(np.ceil(box[3])) + 12))
    zoom = ImageOps.pad(annotated.crop(crop_box), (512, 288), color="#222222")
    sheet = Image.new("RGB", (1536, 322), "#181818")
    for index, (panel, title) in enumerate(((raw, "Input: no boxes"),
            (annotated, "GT green | score>=0.5 cyan | selected candidate orange"), (zoom, "Selected region"))):
        sheet.paste(panel, (index * 512, 34))
        ImageDraw.Draw(sheet).text((index * 512 + 4, 8), title, fill="white")
    name = f"{case['case_id']}.jpg"
    sheet.save(folder / name, quality=93)
    candidate_text = f'候选分数 {candidate["score"]:.4f}，' if candidate else '没有候选。'
    return (f'<section id="{case["case_id"]}"><h2>{case["case_id"]}：{html.escape(REASONS[case["reason"]])}</h2>'
            f'<p>图像 {row["source_frame"]}，类别 {case["class_name"]}，GT序号 {case["target_index"]}。'
            f'{candidate_text}'
            f'最佳保留IoU {case["stages"]["final"]["best_IoU"]:.4f}。'
            f'<a href="{html.escape(Path(row["image"]).as_uri(), quote=True)}">无框完整原图</a></p>'
            f'<img src="cases/{name}" loading="lazy"><details><summary>逐级证据</summary>'
            f'<pre>{html.escape(json.dumps(case, ensure_ascii=False, indent=2))}</pre></details></section>')


def main():
    contract, _ = verify_prepared()
    checkpoint_path = RUN / "last.pt"
    scored_path = OUTPUT / "execution_v1/training_fit.json"
    if sha256(checkpoint_path) != WEIGHT_SHA or sha256(scored_path) != SCORE_SHA:
        raise ValueError("tiny-fit checkpoint or scored predictions changed")
    checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=False)
    validate_candidate(checkpoint, contract)
    manifest_path = OUTPUT / "tiny_fit32_manifest.json"
    for row in json.loads(manifest_path.read_text(encoding="utf-8"))["images"]:
        guard_row(row)
    _, snapshot = load_dataset_snapshot(manifest_path)
    dataset = FullFrameDataset(snapshot.rows, "train", mosaic=False)
    saved = json.loads(scored_path.read_text(encoding="utf-8"))
    model = RoadYOLOS4().cpu().eval()
    model.load_state_dict(checkpoint["model"], strict=True)
    torch.set_num_threads(2)
    torch.use_deterministic_algorithms(True)
    folder = DEST / "diagnosis"
    folder.mkdir(parents=True, exist_ok=False)
    (folder / "cases").mkdir()
    cases, cards, stage_counts, frame_stats, fp_cases = [], [], Counter(), [], []
    for index, row in enumerate(dataset.rows):
        pixels, _, _ = dataset._load(index)
        image, _, _ = dataset[index]
        with torch.inference_mode():
            outputs = model(image.unsqueeze(0))
            float_boxes, obj, cls, _, _ = decode_outputs(outputs)
            float_scores = (obj.sigmoid().unsqueeze(-1) * cls.sigmoid())[0].numpy()
            float_boxes = np.clip(float_boxes[0].numpy(), 0, [512, 288, 512, 288])
        heads = [np.clip(np.rint(out[0].permute(1, 2, 0).numpy() * 256), -32768, 32767).astype(np.int16)
                 for out in outputs]
        fixed_boxes, fixed_scores, traces = trace_heads(heads)
        local_saved = [p for p in saved["predictions"] if p["image_id"] == row["image"]]
        recomputed = [dict(image_id=row["image"], label=p["label"], box=p["box"], score=p["score"])
                      for trace in traces for p in trace["final"]]
        assert recomputed == local_saved, "CPU recomputation does not reproduce saved score report"
        frame_stats.append(dict(image_id=row["image"], source_sha256=row["source_sha256"],
            above_floor_counts=[trace["above_floor_count"] for trace in traces],
            final_counts=[len(trace["final"]) for trace in traces],
            INT16_saturation_values=sum(int(np.count_nonzero(np.abs(out.numpy()) * 256 > 32767)) for out in outputs)))
        for label, name in enumerate(("person", "vehicle")):
            gt = [dict(image_id=row["image"], label=label, box=box)
                  for box, category in zip(row["boxes"], row["labels"]) if category == label]
            trace = traces[label]
            high, low = assign(trace["final"], gt, .5), assign(trace["final"], gt, .05)
            expected = evaluate(local_saved, gt, label=label, threshold=.5)
            assert len(high) == expected["tp"]
            for key in ("pre_top", "top", "final"):
                stage_counts[f"{name}/{key}_TP_at005"] += len(assign(trace[key], gt, .05))
            valid_float = np.all(float_boxes[:, 2:] > float_boxes[:, :2], axis=1)
            def all_records(boxes, scores, mask):
                return [dict(label=label, cell_id=int(cell), box=boxes[cell].tolist(),
                             score=float(scores[cell, label])) for cell in np.flatnonzero(mask)]
            raw_float = all_records(float_boxes, float_scores, valid_float)
            float_floor = sorted([p for p in raw_float if p["score"] >= .05],
                                 key=lambda p: (-p["score"], p["cell_id"]))
            stage_counts[f"{name}/float_floor_TP_at005"] += len(assign(float_floor, gt, .05))
            raw_fixed = all_records(fixed_boxes, fixed_scores,
                                   np.all(fixed_boxes[:, 2:] > fixed_boxes[:, :2], axis=1))
            for j, target in enumerate(gt):
                if j in high:
                    continue
                stages = {key: support(trace[key], target) for key in ("pre_top", "top", "final")}
                stages.update(float_all=support(raw_float, target), fixed_all=support(raw_fixed, target),
                              float_floor=support(float_floor, target),
                              other_class_final=support(traces[1 - label]["final"], target))
                reason = "low_confidence" if j in low else reason_for(stages, trace["removed"])
                candidate = trace["final"][low[j]] if j in low else stages["pre_top"]["candidate"]
                case = dict(case_id=f"case_{len(cases)+1:02d}", image_id=row["image"], class_name=name,
                            target_index=j, target=target, reason=reason, stages=stages,
                            selected_candidate=candidate,
                            removed_support={str(cell): trace["removed"].get(cell)
                                             for cell in stages["top"]["supporting_cells"]})
                cases.append(case)
                cards.append(render_case(case, pixels, row, gt, trace["final"], folder / "cases"))
            for j, prediction in enumerate(trace["final"]):
                if prediction["score"] >= .5 and j not in high.values():
                    evidence = support([dict(target, cell_id=k, score=1.) for k, target in enumerate(gt)], prediction)
                    fp_id = f"fp_{len(fp_cases)+1:02d}"
                    picture = Image.fromarray(pixels).resize((1024, 576))
                    draw = ImageDraw.Draw(picture)
                    for box in row["boxes"]:
                        draw.rectangle([v * 2 for v in box], outline="lime", width=2)
                    draw.rectangle([v * 2 for v in prediction["box"]], outline="orange", width=3)
                    draw.text((5, 5), f'{fp_id} {name} {prediction["score"]:.4f} | GT green, unmatched orange',
                              fill="orange", stroke_width=1, stroke_fill="black")
                    picture.save(folder / "cases" / f"{fp_id}.jpg", quality=93)
                    fp_cases.append(dict(image_id=row["image"], class_name=name, prediction=prediction,
                                         best_GT_IoU=evidence["best_IoU"], reason="false_positive",
                                         picture=f"cases/{fp_id}.jpg"))
                    cards.append(f'<section><h2>{fp_id}：score0.5未匹配预测</h2>'
                                 f'<p>绿色GT，橙色未匹配预测。分数 {prediction["score"]:.4f}，'
                                 f'同类GT最佳IoU {evidence["best_IoU"]:.4f}；未匹配不自动等于背景。</p>'
                                 f'<img src="cases/{fp_id}.jpg" loading="lazy"></section>')
        print(f"CPU stage trace {index+1}/32", flush=True)
    counts = Counter(f"{case['class_name']}/{case['reason']}" for case in cases)
    assert len(cases) == 38 and sum(c["reason"] == "low_confidence" for c in cases) == 24
    for label, name in enumerate(("person", "vehicle")):
        expected = saved["diagnostic_metrics_at_0_5"]["classes"][name]
        assert sum(c["class_name"] == name for c in cases) == expected["fn"]
        assert sum(c["class_name"] == name for c in fp_cases) == expected["fp"]
    source_names = ("diagnose_tiny_fit.py", "analyze_detection_errors.py", "integer.py", "loss.py",
                    "metrics.py", "model.py", "train.py", "dataset.py", "score_tiny_fit.py")
    sources = {name: sha256(ROOT / "cnn" / name) for name in source_names}
    receipt = dict(status="fixed_training_fit_miss_attribution_NOT_validation", checkpoint_sha256=WEIGHT_SHA,
        dataset_sha256=snapshot.manifest_sha256, dataset_content_sha256=snapshot.dataset_content_sha256,
        scored_report_sha256=SCORE_SHA, counts=dict(counts), stage_one_to_one_counts=dict(stage_counts),
        cases=cases, false_positives=fp_cases, frames=frame_stats, exact_recomputed_frames=32,
        exact_trace_vs_reference_frames=32, source_sha256=sources,
        training_started=False, labels_changed=False, formal_acceptance=False,
        limitation="Geometric stage evidence, not human GT certification or proof of training optimality. Float/fixed preTop comparisons are not alternate deployment metrics.")
    write_json(folder / "diagnosis.json", receipt)
    (folder / "index.html").write_text('<!doctype html><meta charset="utf-8"><title>32图固定漏检排查</title>'
        '<style>body{font:16px sans-serif;margin:24px;background:#f5f5f5}img{width:100%;max-width:1536px}'
        'section{background:white;padding:15px;margin:24px 0}pre{white-space:pre-wrap;overflow-wrap:anywhere}</style>'
        '<h1>32图固定漏检排查：只读，不需要重新标框</h1>'
        '<p>这是训练图诊断，不是独立验证。无框网络输入／全图对照／局部放大。绿色选中GT，蓝色score≥0.5预测，橙色追查候选。'
        '候选可能低分或已被抑制，橙框不代表最终输出。每条均链接未经覆盖的无框完整原图。</p>'
        f'<p>全部38个score0.5漏检，其中24个低分恢复；计数：{html.escape(str(dict(counts)))}</p>'
        '<details><summary>score0.5误报（全部）</summary><pre>'+html.escape(json.dumps(fp_cases, ensure_ascii=False, indent=2))+
        '</pre></details>'+''.join(cards), encoding='utf-8')
    (folder / "sources").mkdir()
    for name in source_names:
        shutil.copy2(ROOT / "cnn" / name, folder / "sources" / name)
        assert sha256(folder / "sources" / name) == sources[name]
    assert sha256(checkpoint_path) == WEIGHT_SHA and sha256(scored_path) == SCORE_SHA
    print(json.dumps(dict(counts=dict(counts), stage_counts=dict(stage_counts), output=str(folder)), ensure_ascii=False))


if __name__ == "__main__":
    main()
