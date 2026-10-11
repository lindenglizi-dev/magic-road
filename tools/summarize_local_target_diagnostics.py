#!/usr/bin/env python3
"""Verify the bounded diagnostics and measure one min-run bypass counterfactual."""
from pathlib import Path
import html
import json
import cv2
from local_paired_diagnostic import PROJECT, PACKAGE, digest, dump, read_json, match
from roi_dataset_tool import fpga_analysis_frame, fpga_resize_roi
from run_local_scene_pilot import MODEL_DIR, load_models, make_hog324, quantization_contract, score_roi

BASE = PROJECT/'evaluation/local_scene_pilots'
STAGE = BASE/'intersection_2415171_stage_diagnostic_v1'
GRID = BASE/'intersection_2415171_fourgrid_v2'
OUT = BASE/'intersection_2415171_diagnostic_summary_v2'


def verified(directory):
    receipt = read_json(directory/'receipt.json')
    hashes = receipt.get('artifact_hashes')
    if hashes is None:
        raise ValueError('Missing artifact hashes')
    for name, expected in hashes.items():
        path = (directory/name).resolve()
        if not path.is_relative_to(directory.resolve()) or digest(path) != expected:
            raise ValueError(f'Artifact mismatch: {name}')
    return receipt


def main():
    if OUT.exists():
        raise ValueError('Use a new output version')
    verified(STAGE)
    verified(GRID)
    verified(PACKAGE)
    stage = read_json(STAGE/'report.json')
    grid = read_json(GRID/'report.json')
    frames = read_json(STAGE/'frame_stages.json')
    roi_rows = read_json(GRID/'fourgrid_rows.json')
    parameters, _, model_receipt = load_models(MODEL_DIR)
    hog = make_hog324()
    quant = quantization_contract(parameters['opencv_hog324'])
    package_frames = {f['frame_index']: f for f in read_json(PACKAGE/'package.json')['frames']}
    results = []
    metrics = {k: {'targets': 0, 'covered': 0, 'correct_hog324q': 0,
                   'coverage_gained': [], 'coverage_lost': []} for k in ('ped', 'vehicle')}
    candidates_total = 0
    for f in frames:
        # min_run=1 is identity on the saved clean mask. Background update is
        # driven by raw pixels, so bypassing the later run filter has no feedback.
        pool = [c for c in f['stages']['clean_all']['components'] if c['area'] >= 16][:4]
        links = match(f['targets'], [c['source_box'] for c in pool])
        prior = {p['track_id'] for p in f['stages']['top4']['matching']['0.5']['pairs']}
        gray = fpga_analysis_frame(cv2.imread(str(PACKAGE/package_frames[f['frame_index']]['path'])))
        scored = []
        for c in pool:
            x0, y0, x1, y1 = c['analysis_box']
            score = score_roi(fpga_resize_roi(gray[y0:y1+1, x0:x1+1]), parameters, hog, quant)
            scored.append({**c, 'score': score})
        candidates_total += len(pool)
        for i, target in enumerate(f['targets']):
            entry = metrics[target['label']]
            entry['targets'] += 1
            now, before = i in links, target['track_id'] in prior
            entry['covered'] += now
            entry['correct_hog324q'] += bool(now and scored[links[i]]['score']['hog324_q_prediction'] == target['label'])
            if now != before:
                entry['coverage_gained' if now else 'coverage_lost'].append([f['frame_index'], target['track_id']])
        results.append({'frame_index': f['frame_index'], 'candidates': scored,
                        'matching': [{'track_id': f['targets'][i]['track_id'], 'candidate_index': j} for i,j in links.items()]})
    visibility = {}
    for label in ('ped', 'vehicle'):
        visibility[label] = {}
        for condition in ('full', 'occluded', 'frame_truncated'):
            subset = [r for r in roi_rows if r['label'] == label and r['visibility'] == condition]
            visibility[label][condition] = {'targets': len(subset),
                'covered': sum(r['matched'] for r in subset),
                'hog324q_correct': {k: sum(r[k] is not None and r[k]['hog324_q_prediction'] == label for r in subset)
                                    for k in 'ABCD'}}
    summary = {'scope': 'user-confirmed moving ped/vehicle only; single scene, 32 frames, four tracks',
               'stage_primary_iou05': stage['primary_iou05'],
               'fourgrid_by_class': grid['metrics']['by_class'], 'visibility_strata': visibility,
               'min_run1_counterfactual': {'parameters_changed': {'min_run': {'baseline': 2, 'counterfactual': 1}},
                    'implementation': 'reuse hash-verified clean-mask components from continuous baseline replay; same min_area16, descending-area/OpenCV-label tie-break, top4, frozen models',
                    'background_feedback': 'none: background updates depend on raw mask, not cleanup/run/CCL',
                    'metrics': metrics, 'candidates_total': candidates_total,
                    'invalid_far': None, 'precision': None,
                    'boundary': 'diagnostic only; no invalid labels; cannot accept for deployment from target recall alone'},
               'decision': 'Reject direct min_run1 deployment: localization coverage improves but correctly localized-and-classified pedestrians decrease from 7 to 4. Check crop/model coupling with independent training data; no topK expansion, DDR ROI or RTL justified yet.',
               'limitations': ['Ground-truth boxes include occlusion and frame-edge truncation; do not call all GT crops complete bodies.',
                   'Four-grid holds the existing models fixed; high-resolution benefit under matched training remains unknown.',
                   'No background truth: unmatched candidates may contain partial targets, static objects or riders.',
                   'No test set, no training, no thresholds selected, no RTL measurements.',
                   'OpenCV versus DFS validates Python components only; physical RLE capacity/overflow remains unmeasured.',
                   'Capacity proxies (max row runs 16, max components 86) cover only the 32 scored frames, not every frame of the continuous replay.']}
    OUT.mkdir()
    dump(OUT/'summary.json', summary)
    dump(OUT/'min_run1_frames.json', results)
    stage_rows = ''.join(f'<tr><td>{html.escape(name)}</td><td>{value["by_class"]["ped"]["matched"]}/46</td><td>{value["by_class"]["vehicle"]["matched"]}/11</td></tr>'
                         for name,value in stage['primary_iou05'].items())
    minrun_rows = ''.join(f'<tr><td>{name}</td><td>{v["covered"]}/{v["targets"]}</td><td>{v["correct_hog324q"]}/{v["targets"]}</td><td>{len(v["coverage_gained"])}</td><td>{len(v["coverage_lost"])}</td></tr>' for name,v in metrics.items())
    gt_rows = ''.join(f'<tr><td>{name}</td><td>{v["models"]["hog324_q_prediction"]["all_targets_AB_correct"]["A"]}/{v["targets"]}</td><td>{v["models"]["hog324_q_prediction"]["all_targets_AB_correct"]["B"]}/{v["targets"]}</td><td>{v["models"]["hog324_q_prediction"]["matched_subset_ABCD_correct"]["C"]}/{v["targets"]}</td></tr>' for name,v in grid['metrics']['by_class'].items())
    contacts = ''.join(f'<a href="../intersection_2415171_fourgrid_v2/fourgrid_contact_{i:02d}.png">联系表 {i}</a> ' for i in range(1,7))
    page = f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>路口视频：人工确认后的诊断</title>
<style>body{{font:16px/1.65 system-ui;margin:32px auto;max-width:1040px;padding:0 24px;color:#202c3c}}table{{border-collapse:collapse;width:100%;margin:16px 0}}th,td{{padding:8px 14px;border:1px solid #ccd4dd;text-align:left}}th{{background:#edf3f8}}.note{{background:#fff2d5;padding:16px}}a{{color:#1765a0}}</style>
<h1>路口视频：人工确认后的诊断</h1><p>2026-09-30 · 只评移动人车 · 32 帧 / 46 次行人、11 次车辆观测 / 4 条轨迹</p>
<p class="note">这是单场景开发诊断，不是模型验收。原始标注未改；聊天确认另存收据。所有遮挡和出画面目标仍保留在分母中。未匹配框没有自动标为背景。</p>
<h2>候选定位：IoU ≥ 0.5，一对一匹配</h2><table><tr><th>阶段</th><th>行人覆盖</th><th>车辆覆盖</th></tr>{stage_rows}</table>
<p>这些是候选集合的离线覆盖，尚未加入分类正确性。Top8/16 只增加一次行人覆盖；更早的 run 过滤值得先检查。96 张实际 Mask 的独立 DFS 与 OpenCV 像素集合、面积、框一致，32 帧冻结 Top4 重放一致。未验证 RTL 活跃 label 容量、溢出、周期或 CDC。</p>
<h2>冻结 HOG324：图像来源与候选定位</h2><table><tr><th>类别</th><th>A 原图人工框正确</th><th>B 分析图人工框正确</th><th>C 定位达标且分类正确</th></tr>{gt_rows}</table>
<p>A/B 使用同一物理 cell 范围，并保留原始人工框计算 IoU。43 个未匹配目标的 C/D 为空。人工框包含截断/遮挡，不等于完整人体。当前模型没有从原图输入获得收益，但这不排除匹配训练后的收益。浮点/量化线性层分类一致不等于整数 HOG 或 RTL 对拍通过。</p><p>{contacts}</p>
<h2>单项对照：只把最短 run 从 2 改为 1</h2><table><tr><th>类别</th><th>覆盖</th><th>定位和 HOG324 都正确</th><th>覆盖新增</th><th>覆盖丢失</th></tr>{minrun_rows}</table>
<p>复用连续运行的 clean mask，保持面积16、最多四框和冻结模型。背景更新不依赖该后处理，因此无需重复解码。此分支仅为 Python 反事实诊断：没有 invalid 真值，不能评价误接受率。容量代理统计仅覆盖32个评分帧，不能外推连续区间无溢出。</p>
<h2>后续决策</h2><p><strong>不采用直接旁路短 run 过滤：</strong>行人覆盖11→15，但定位和分类同时正确7→4；车辆覆盖3→5，同时正确2→4。覆盖收益没有转化为行人识别收益。</p><p>下一步检查框形与模型的耦合，并用独立训练场景准备真实候选训练数据。增加候选预算及高分辨率 DDR 读取均无当前证据支持。新增框需查看上下文并评估误报；本轮评价目标不能回灌训练。生产 RTL 保持不变。</p>
<p><a href="summary.json">汇总数据</a> · <a href="min_run1_frames.json">单项对照逐帧数据</a> · <a href="receipt.json">输入与产物收据</a></p></html>'''
    (OUT/'report.html').write_text(page, encoding='utf-8')
    dump(OUT/'receipt.json', {'schema': 'local_target_diagnostic_summary_v1',
         'source_receipts': {str(p.relative_to(PROJECT)): digest(p) for p in (STAGE/'receipt.json',GRID/'receipt.json',PACKAGE/'receipt.json')},
         'models': model_receipt, 'script_sha256': digest(__file__),
         'artifact_hashes': {p.name:digest(p) for p in sorted(OUT.iterdir()) if p.is_file()}})
    print(json.dumps({'output': str(OUT), 'min_run1': metrics, 'candidate_count': candidates_total}, indent=2))


if __name__ == '__main__':
    main()
