#!/usr/bin/env python3
"""Prepare an unlabeled, offline human-review package for local scene 3785878.

This tool performs no training, classification, threshold tuning, or scoring.
It decodes the registered source continuously, normalizes every frame to the
explicit 1280x720 input contract, advances the default candidate reference,
and exports fixed full-frame and candidate review entry points.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
import shutil
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import cv2
import numpy as np


SCRIPT = Path(__file__).resolve()
PROJECT = SCRIPT.parents[1]
TOOLS = PROJECT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from analyze_virat_failure_sources import GeometryTracker  # noqa: E402
from candidate_chain_reference import CandidateChainReference  # noqa: E402
from roi_dataset_tool import fpga_resize_roi  # noqa: E402


VIDEO = PROJECT / "public_data/raw/3785878-hd_1920_1080_30fps.mp4"
V1_OUTPUT = PROJECT / "evaluation/local_scene_pilots/intersection_3785878_train_review_v1"
OUTPUT = PROJECT / "evaluation/local_scene_pilots/intersection_3785878_train_review_v2"
INVENTORY = PROJECT / "evaluation/local_scene_pilots/selection_2026-09-28/inventory.json"
KNOWN_PACKAGE = PROJECT / "evaluation/local_scene_pilots/intersection_2415171_target32_v2/package.json"
KNOWN_CANDIDATES = PROJECT / "evaluation/local_scene_pilots/intersection_2415171_f120_1079_v1/candidates.csv"
KNOWN_RECEIPT = PROJECT / "evaluation/local_scene_pilots/intersection_2415171_f120_1079_v1/receipt.json"
TEMPLATE = TOOLS / "local_paired_annotation.html"

EXPECTED_SHA256 = "cdf796ed98837f8f2497cd87941c5ec51cb42ddd05f25a2c0acfdee78a21d422"
KNOWN_SHA256 = "5bd44aededccb88ac75febb170ae0f916b909277a0b4e8450adc4e33d440ea6b"
EXPECTED_WIDTH, EXPECTED_HEIGHT = 1920, 1080
EXPECTED_FPS = 30000.0 / 1001.0
EXPECTED_FRAMES = 1214
NORMALIZED_WIDTH, NORMALIZED_HEIGHT = 1280, 720
FULL_FRAME_IDS = list(range(150, 1141, 90))
CONTRACT_ID = "local3785878_train_review_source_normalized720_inclusive_v2"
PREPROCESSING_CONTRACT = "source1920x1080_inter_area_1280x720_fpga_gray_stride5_v1"
SCENE_STATUS = "proposed_train_pending_provenance"
SOURCE_LICENSE = "unknown_pending_user_confirmation"
MAX_CANDIDATES = 24
TRACK_REPRESENTATIVE_GAP = 30
FORBIDDEN = re.compile(r"(^|[/\\_.-])(blind|holdout|reserve|test)($|[/\\_.-])", re.I)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def pixel_sha256(image: np.ndarray) -> str:
    return hashlib.sha256(np.ascontiguousarray(image, dtype=np.uint8).tobytes()).hexdigest()


def dump(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                    encoding="utf-8")


def guard_allowed(path: Path) -> None:
    if FORBIDDEN.search(path.resolve().as_posix()):
        raise ValueError(f"sealed path rejected: {path}")


def video_metadata(path: Path) -> dict[str, Any]:
    capture = cv2.VideoCapture(str(path))
    if not capture.isOpened():
        raise ValueError(f"cannot open video: {path}")
    metadata = {
        "width": int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
        "height": int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        "fps": float(capture.get(cv2.CAP_PROP_FPS)),
        "frame_count": int(capture.get(cv2.CAP_PROP_FRAME_COUNT)),
        "fourcc": int(capture.get(cv2.CAP_PROP_FOURCC)),
    }
    capture.release()
    metadata["codec_fourcc"] = "".join(
        chr((metadata["fourcc"] >> (8 * index)) & 255) for index in range(4)
    ).rstrip("\x00")
    return metadata


def validate_inputs(video: Path, output: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    for path in (video, output, INVENTORY, KNOWN_PACKAGE, KNOWN_CANDIDATES,
                 KNOWN_RECEIPT, TEMPLATE):
        guard_allowed(path)
    if output.exists() and any(output.iterdir()):
        raise ValueError(f"output must be absent or empty: {output}")
    actual_sha = sha256(video)
    if actual_sha != EXPECTED_SHA256:
        raise ValueError(f"source SHA256 mismatch: {actual_sha}")
    metadata = video_metadata(video)
    if (metadata["width"] != EXPECTED_WIDTH or metadata["height"] != EXPECTED_HEIGHT or
            metadata["frame_count"] != EXPECTED_FRAMES or
            not math.isclose(metadata["fps"], EXPECTED_FPS, rel_tol=0.0, abs_tol=1e-9)):
        raise ValueError(f"source metadata mismatch: {metadata}")

    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    selected = next((row for row in inventory.get("videos", []) if row.get("name") == video.name), None)
    if selected is None or selected.get("sha256") != EXPECTED_SHA256:
        raise ValueError("previously viewed inventory does not bind the selected source")
    if any(selected.get(key) != expected for key, expected in
           (("width", EXPECTED_WIDTH), ("height", EXPECTED_HEIGHT),
            ("frame_count", EXPECTED_FRAMES))):
        raise ValueError("inventory metadata differs from the frozen contract")

    known_package = json.loads(KNOWN_PACKAGE.read_text(encoding="utf-8"))
    known_receipt = json.loads(KNOWN_RECEIPT.read_text(encoding="utf-8"))
    if known_package.get("source_sha256") != KNOWN_SHA256:
        raise ValueError("known 2415171 package source identity changed")
    candidate_hash = sha256(KNOWN_CANDIDATES)
    if known_receipt.get("artifact_hashes", {}).get("candidates.csv") != candidate_hash:
        raise ValueError("known 2415171 candidate/ROI manifest hash changed")
    with KNOWN_CANDIDATES.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    known_roi_hashes = {row["roi_pixel_sha256"] for row in rows}
    if not rows or "" in known_roi_hashes:
        raise ValueError("known 2415171 ROI manifest is incomplete")
    if EXPECTED_SHA256 == KNOWN_SHA256:
        raise ValueError("new training source unexpectedly equals the existing 2415171 scene")
    known_check = {
        "source_sha256": KNOWN_SHA256,
        "candidate_manifest_path": KNOWN_CANDIDATES.relative_to(PROJECT).as_posix(),
        "candidate_manifest_sha256": candidate_hash,
        "candidate_rows": len(rows),
        "unique_roi_pixel_hashes": len(known_roi_hashes),
        "source_distinct_from_3785878": True,
        "access_boundary": "known development manifest only; no sealed split was read",
    }
    return {**metadata, "sha256": actual_sha}, known_check


def analysis_to_normalized(box: Sequence[int]) -> list[int]:
    x0, y0, x1, y1 = (int(value) for value in box)
    return [x0 * 5, y0 * 5, min(NORMALIZED_WIDTH - 1, x1 * 5 + 4),
            min(NORMALIZED_HEIGHT - 1, y1 * 5 + 4)]


def normalized_to_original(box: Sequence[int]) -> list[int]:
    """Outward inclusive mapping from normalized pixels into original pixels."""
    x0, y0, x1, y1 = (int(value) for value in box)
    return [x0 * 3 // 2, y0 * 3 // 2,
            min(EXPECTED_WIDTH - 1, ((x1 + 1) * 3 + 1) // 2 - 1),
            min(EXPECTED_HEIGHT - 1, ((y1 + 1) * 3 + 1) // 2 - 1)]


def inclusive_iou(left: Sequence[int], right: Sequence[int]) -> float:
    ix0, iy0 = max(left[0], right[0]), max(left[1], right[1])
    ix1, iy1 = min(left[2], right[2]), min(left[3], right[3])
    intersection = max(0, ix1 - ix0 + 1) * max(0, iy1 - iy0 + 1)
    la = (left[2] - left[0] + 1) * (left[3] - left[1] + 1)
    ra = (right[2] - right[0] + 1) * (right[3] - right[1] + 1)
    return intersection / (la + ra - intersection) if la + ra > intersection else 0.0


def temporal_bin(frame_index: int) -> int:
    return min(2, frame_index * 3 // EXPECTED_FRAMES)


def deterministic_order(rows: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    def key(row: dict[str, Any]) -> tuple[str, int, int]:
        token = (f"{row['temporal_bin']}|{row['geometry_track_id']}|"
                 f"{row['frame_index']}|{row['slot']}|{row['roi_pixel_sha256']}")
        return hashlib.sha256(token.encode("ascii")).hexdigest(), row["frame_index"], row["slot"]
    return sorted(rows, key=key)


def select_review_candidates(rows: Sequence[dict[str, Any]], limit: int = MAX_CANDIDATES
                             ) -> list[dict[str, Any]]:
    """Balance three bins, prefer one representative per geometry track, dedupe pixels."""
    if limit < 1:
        return []
    quotas = [limit // 3 + (1 if index < limit % 3 else 0) for index in range(3)]
    pools = [deterministic_order(row for row in rows if row["temporal_bin"] == index)
             for index in range(3)]
    selected: list[dict[str, Any]] = []
    used_hashes: set[str] = set()
    selected_by_track: dict[str, list[int]] = defaultdict(list)
    counts = [0, 0, 0]

    def eligible(row: dict[str, Any], unique_track_only: bool) -> bool:
        track = row["geometry_track_id"]
        if row["roi_pixel_sha256"] in used_hashes:
            return False
        previous = selected_by_track[track]
        if unique_track_only and previous:
            return False
        return all(abs(row["frame_index"] - frame) >= TRACK_REPRESENTATIVE_GAP for frame in previous)

    for unique_track_only in (True, False):
        for bin_index in range(3):
            for row in pools[bin_index]:
                if counts[bin_index] >= quotas[bin_index]:
                    break
                if not eligible(row, unique_track_only):
                    continue
                selected.append(row)
                counts[bin_index] += 1
                used_hashes.add(row["roi_pixel_sha256"])
                selected_by_track[row["geometry_track_id"]].append(row["frame_index"])
        if len(selected) >= limit:
            break
    return sorted(selected, key=lambda row: (row["frame_index"], row["slot"]))


def write_image(path: Path, image: np.ndarray) -> None:
    if not cv2.imwrite(str(path), image, [cv2.IMWRITE_PNG_COMPRESSION, 4]):
        raise OSError(f"cannot write image: {path}")


def context_box(box: Sequence[int], width: int, height: int) -> list[int]:
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0 + 1, y1 - y0 + 1
    cw, ch = max(480, bw * 5), max(320, bh * 5)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    left, top = max(0, cx - cw // 2), max(0, cy - ch // 2)
    right, bottom = min(width - 1, left + cw - 1), min(height - 1, top + ch - 1)
    left, top = max(0, right - cw + 1), max(0, bottom - ch + 1)
    return [left, top, right, bottom]


def full_annotation_html(package: Mapping[str, Any]) -> str:
    text = TEMPLATE.read_text(encoding="utf-8")
    replacements = {
        "路口完整目标审核 · 32帧": "3785878训练候选场景完整目标审核 · 12帧",
        "共32帧。": ("共12帧。帧号保持原视频身份；画布是原片经 cv2.INTER_AREA 明确归一化后的 "
                  "1280x720 图。每帧另有原始1920x1080无损图链接用于核对。"),
        "index+1}/32": "index+1}/${pkg.frames.length}",
        "data.frames.filter(f=>f.completed).length}/32 帧":
            "data.frames.filter(f=>f.completed).length}/${pkg.frames.length} 帧",
        "f.frame_index/(24000/1001)": "f.frame_index/pkg.fps",
        "if(index<31)": "if(index<pkg.frames.length-1)",
        "32帧全部检查": "12帧全部检查",
        "intersection_2415171_targets_review.json": "intersection_3785878_train_fullgt_review.json",
    }
    for old, new in replacements.items():
        if old not in text:
            raise ValueError(f"annotation template contract text missing: {old}")
        text = text.replace(old, new)
    marker = '<label><input type="checkbox" id="done">本帧已全部检查</label></div>'
    text = text.replace(marker, marker[:-6] +
                        '<a id="originalLink" target="_blank">打开原始1920x1080帧</a></div>')
    refresh = "$('done').checked=f.completed;"
    text = text.replace(refresh, refresh +
                        "$('originalLink').href=pkg.frames[index].original_path;")
    text = text.replace("__PACKAGE_JSON__", json.dumps(package, ensure_ascii=False))
    return text


def candidate_review_html(package: Mapping[str, Any]) -> str:
    payload = json.dumps(package, ensure_ascii=False)
    return f'''<!doctype html><html lang="zh-CN"><meta charset="utf-8">
<title>3785878候选人工审核 · {len(package['candidates'])}项</title>
<style>
body{{font:15px system-ui;background:#101823;color:#e9eef7;margin:18px auto;max-width:1500px;padding:0 16px}}
h1{{font-size:24px}} p{{line-height:1.55;color:#c2cfe0}} .card{{display:grid;grid-template-columns:minmax(420px,2fr) 220px minmax(360px,1fr);gap:14px;align-items:start;background:#172536;margin:14px 0;padding:12px;border:1px solid #53657d;border-radius:8px}}
img{{max-width:100%;height:auto;background:#222}} .roi{{image-rendering:pixelated;width:192px;height:192px}} label{{display:block;margin:5px 0}} select,input,button{{font:inherit;padding:6px;background:#203249;color:#fff;border:1px solid #607089;border-radius:5px}} .meta{{font-family:ui-monospace,monospace;font-size:12px;color:#b9c7d8;overflow-wrap:anywhere}} #status{{color:#7be3ce}} .warn{{color:#ffd57e}}
</style><h1>3785878 候选人工审核</h1>
<p>候选来自连续 frame 0..1213 的默认 top4 候选链，只按三个时间区间、几何轨迹间隔和ROI像素去重抽样。抽样包含候选链启动早期样本（例如 frame 23）；它们仅用于训练样本人工审核，不作为预热后运行期指标。页面不含模型分数，也不会自动训练。蓝框图是原始1920x1080像素上下文；右侧是归一化720图经 FPGA灰度/stride5 后得到的32x32 ROI。</p>
<p class="warn">请逐项选择类别。骑行者应选 ignore 并填写 subtype（如 rider_bicycle）。未审核项保持空值，不能当作背景。</p>
<div id="cards"></div><p id="status"></p>
<div><label>审核者 <input id="reviewer"></label><label>审核日期 <input type="date" id="date"></label><label><input type="checkbox" id="confirm"> 我已亲自核对全部候选与属性</label></div>
<button id="save">导出审核 JSON</button><button id="importBtn">导入之前的 JSON</button><input id="importFile" type="file" accept=".json" hidden>
<script>
const pkg={payload},$=id=>document.getElementById(id),cacheKey=pkg.contract_id+':candidate:'+pkg.source_sha256;
let data={{contract_id:pkg.contract_id,source_sha256:pkg.source_sha256,review_basis:'human_candidate_review',reviewer:'',reviewed_at:'',human_confirmed:false,candidates:pkg.candidates.map(c=>({{candidate_id:c.candidate_id,label:'',subtype:'',condition:'',crop_usable:'',motion:'',track_id:'',reviewed:false,note:''}}))}};
function validate(d){{if(d.contract_id!==pkg.contract_id||d.source_sha256!==pkg.source_sha256||d.review_basis!=='human_candidate_review'||d.candidates.length!==pkg.candidates.length)throw Error('来源、合同或候选数量不匹配');
d.candidates.forEach((r,i)=>{{if(r.candidate_id!==pkg.candidates[i].candidate_id)throw Error('候选身份不匹配');if(!['','ped','vehicle','invalid','ignore','uncertain'].includes(r.label))throw Error('非法类别');if(!['','full','truncated','merged','fragment'].includes(r.condition))throw Error('非法完整性');if(!['','yes','no','uncertain'].includes(r.crop_usable))throw Error('非法crop_usable');if(!['','moving','stationary','uncertain'].includes(r.motion))throw Error('非法运动状态');if(r.label==='ignore'&&!r.subtype.trim())throw Error('ignore需要subtype');}});return d;}}
try{{const cached=localStorage.getItem(cacheKey);if(cached)data=validate(JSON.parse(cached));}}catch(e){{}}
function store(){{data.reviewer=$('reviewer').value.trim();data.reviewed_at=$('date').value;data.human_confirmed=$('confirm').checked;try{{localStorage.setItem(cacheKey,JSON.stringify(data));}}catch(e){{}}refreshStatus();}}
function invalidate(card,r){{r.reviewed=false;card.querySelector('input[data-key="reviewed"]').checked=false;data.human_confirmed=false;$('confirm').checked=false;}}
function field(select,id,values,labels){{select.innerHTML='<option value="">未填写</option>'+values.map((v,i)=>`<option value="${{v}}">${{labels[i]}}</option>`).join('');select.value=data.candidates[id][select.dataset.key];select.onchange=()=>{{data.candidates[id][select.dataset.key]=select.value;invalidate(select.closest('.card'),data.candidates[id]);store();}};}}
function render(){{const root=$('cards');root.replaceChildren();pkg.candidates.forEach((c,i)=>{{const r=data.candidates[i],card=document.createElement('section');card.className='card';card.innerHTML=`<div><img src="${{c.context_blue_path}}"><div class="meta">${{c.candidate_id}} · frame=${{c.frame_index}} · bin=${{c.temporal_bin}} · geometry_track=${{c.geometry_track_id}}<br>analysis=${{c.analysis_box_inclusive}}<br>normalized720=${{c.normalized_box_inclusive}}<br>original1920=${{c.original_box_inclusive}}</div></div><div><img class="roi" src="${{c.roi_path}}"><div class="meta">ROI pixel SHA256<br>${{c.roi_pixel_sha256}}</div></div><div class="form"><label>类别 <select data-key="label"></select></label><label>subtype <input data-key="subtype" placeholder="ignore必填，如 rider_bicycle"></label><label>完整性 <select data-key="condition"></select></label><label>crop_usable <select data-key="crop_usable"></select></label><label>运动 <select data-key="motion"></select></label><label>人工轨迹ID <input data-key="track_id"></label><label>备注 <input data-key="note"></label><label><input type="checkbox" data-key="reviewed"> 本项已核对</label></div>`;
const sels=card.querySelectorAll('select');field(sels[0],i,['ped','vehicle','invalid','ignore','uncertain'],['行人 ped','机动车 vehicle','无效 invalid','忽略 ignore','不确定 uncertain']);field(sels[1],i,['full','truncated','merged','fragment'],['完整','截断','粘连','碎片']);field(sels[2],i,['yes','no','uncertain'],['yes','no','uncertain']);field(sels[3],i,['moving','stationary','uncertain'],['moving','stationary','uncertain']);
card.querySelectorAll('input[data-key]:not([type=checkbox])').forEach(input=>{{input.value=r[input.dataset.key];input.oninput=()=>{{r[input.dataset.key]=input.value;invalidate(input.closest('.card'),r);store();}};}});const check=card.querySelector('input[data-key="reviewed"]');check.checked=r.reviewed;check.onchange=()=>{{r.reviewed=check.checked;data.human_confirmed=false;$('confirm').checked=false;store();}};root.append(card);}});}}
function refreshStatus(){{$('status').textContent=`已核对 ${{data.candidates.filter(r=>r.reviewed).length}}/${{data.candidates.length}}；未填写标签 ${{data.candidates.filter(r=>!r.label).length}}。`;}}
$('reviewer').value=data.reviewer;$('date').value=data.reviewed_at;$('confirm').checked=data.human_confirmed;$('reviewer').oninput=store;$('date').onchange=store;$('confirm').onchange=store;
$('save').onclick=()=>{{store();try{{validate(data);}}catch(e){{alert(e.message);return;}}if(data.human_confirmed&&(!data.reviewer||!data.reviewed_at||data.candidates.some(r=>!r.reviewed||!r.label||!r.condition||!r.crop_usable||!r.motion))){{alert('确认完成需要审核者、日期以及所有候选的类别、完整性、crop_usable、运动与逐项核对。也可取消确认后导出草稿。');return;}}const a=document.createElement('a'),url=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{{type:'application/json'}}));a.href=url;a.download='intersection_3785878_candidate_review.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}};
$('importBtn').onclick=()=>$('importFile').click();$('importFile').onchange=async e=>{{try{{if(!e.target.files.length)return;const d=validate(JSON.parse(await e.target.files[0].text()));if(!confirm('导入会替换当前审核内容，确定继续吗？'))return;data=d;$('reviewer').value=d.reviewer||'';$('date').value=d.reviewed_at||'';$('confirm').checked=d.human_confirmed===true;store();render();}}catch(err){{alert(err.message);}}finally{{e.target.value='';}}}};
render();refreshStatus();
</script></html>'''


def contact_sheet(images: Sequence[tuple[np.ndarray, str]], columns: int,
                  tile: tuple[int, int]) -> np.ndarray:
    tile_w, tile_h = tile
    rows = math.ceil(len(images) / columns)
    canvas = np.full((rows * (tile_h + 30), columns * tile_w, 3), 238, np.uint8)
    for index, (image, label) in enumerate(images):
        y, x = divmod(index, columns)
        view = cv2.resize(image, (tile_w, tile_h), interpolation=cv2.INTER_AREA)
        canvas[y*(tile_h+30):y*(tile_h+30)+tile_h, x*tile_w:(x+1)*tile_w] = view
        cv2.putText(canvas, label, (x*tile_w+7, y*(tile_h+30)+tile_h+21),
                    cv2.FONT_HERSHEY_SIMPLEX, .5, (20, 20, 20), 1, cv2.LINE_AA)
    return canvas


def build(video: Path, output: Path) -> dict[str, Any]:
    metadata, known_check = validate_inputs(video, output)
    output.mkdir(parents=True, exist_ok=True)
    frame720_dir = output / "full_frames_720"
    original_dir = output / "full_frames_original"
    raw_context_dir = output / "candidate_context_original_raw"
    blue_context_dir = output / "candidate_context_original_blue"
    roi_dir = output / "candidate_rois_32x32"
    for directory in (frame720_dir, original_dir, raw_context_dir, blue_context_dir, roi_dir):
        directory.mkdir()

    chain = CandidateChainReference()
    tracker = GeometryTracker()
    capture = cv2.VideoCapture(str(video))
    all_candidates: list[dict[str, Any]] = []
    fixed_frames: list[dict[str, Any]] = []
    fixed_contact: list[tuple[np.ndarray, str]] = []
    fixed_set = set(FULL_FRAME_IDS)
    try:
        for frame_index in range(EXPECTED_FRAMES):
            ok, original = capture.read()
            if not ok or original.shape[:2] != (EXPECTED_HEIGHT, EXPECTED_WIDTH):
                raise ValueError(f"continuous decode failed at source frame {frame_index}")
            normalized = cv2.resize(original, (NORMALIZED_WIDTH, NORMALIZED_HEIGHT),
                                    interpolation=cv2.INTER_AREA)
            result = chain.process_bgr(normalized, frame_index)
            boxes = [[int(candidate[key]) for key in ("xmin", "ymin", "xmax", "ymax")]
                     for candidate in result["candidates"]]
            tracks = tracker.update(frame_index, [tuple(box) for box in boxes])
            frame_candidate_boxes: list[list[int]] = []
            for slot, (candidate, box, track) in enumerate(zip(result["candidates"], boxes, tracks)):
                normalized_box = analysis_to_normalized(box)
                original_box = normalized_to_original(normalized_box)
                roi = fpga_resize_roi(result["gray"][box[1]:box[3]+1, box[0]:box[2]+1])
                roi_hash = pixel_sha256(roi)
                frame_candidate_boxes.append(normalized_box)
                all_candidates.append({
                    "candidate_id": f"default_top4:f{frame_index:06d}:slot{slot}:cc{candidate['component_label']}",
                    "frame_index": frame_index,
                    "timestamp_seconds": frame_index / EXPECTED_FPS,
                    "slot": slot,
                    "component_label": int(candidate["component_label"]),
                    "component_area": int(candidate["area"]),
                    "analysis_box_inclusive": box,
                    "normalized_box_inclusive": normalized_box,
                    "original_box_inclusive": original_box,
                    "geometry_track_id": track["causal_track_id"],
                    "geometry_previous_gap_frames": track["causal_previous_gap_frames"],
                    "geometry_track_age_frames": track["causal_track_age_frames"],
                    "temporal_bin": temporal_bin(frame_index),
                    "roi_pixel_sha256": roi_hash,
                    "_roi": roi,
                })
            if frame_index in fixed_set:
                p720 = frame720_dir / f"f{frame_index:06d}.png"
                poriginal = original_dir / f"f{frame_index:06d}.png"
                write_image(p720, normalized)
                write_image(poriginal, original)
                fixed_frames.append({
                    "frame_index": frame_index,
                    "timestamp_seconds": frame_index / EXPECTED_FPS,
                    "path": p720.relative_to(output).as_posix(),
                    "sha256": sha256(p720),
                    "original_path": poriginal.relative_to(output).as_posix(),
                    "original_sha256": sha256(poriginal),
                    "mapping": "same source frame; 720 image is cv2.INTER_AREA normalized from 1920x1080",
                    "candidate_boxes": frame_candidate_boxes,
                    "completed": False,
                    "targets": [],
                })
                fixed_contact.append((normalized.copy(), f"source frame {frame_index}"))
    finally:
        capture.release()
    if chain.last_frame_index != EXPECTED_FRAMES - 1:
        raise AssertionError("candidate reference did not advance through source frame 1213")
    if [row["frame_index"] for row in fixed_frames] != FULL_FRAME_IDS:
        raise AssertionError("fixed full-frame selection incomplete")

    selected = select_review_candidates(all_candidates)
    if len(selected) != min(MAX_CANDIDATES, len({row["roi_pixel_sha256"] for row in all_candidates})):
        raise AssertionError(f"unexpected candidate selection count: {len(selected)}")
    selected_by_track: dict[str, list[int]] = defaultdict(list)
    for row in selected:
        selected_by_track[row["geometry_track_id"]].append(row["frame_index"])
    for frames in selected_by_track.values():
        if any(right - left < TRACK_REPRESENTATIVE_GAP for left, right in zip(frames, frames[1:])):
            raise AssertionError("same-track review representatives violate the 30-frame gap")

    capture = cv2.VideoCapture(str(video))
    candidate_contact: list[tuple[np.ndarray, str]] = []
    exported_candidates = []
    try:
        for ordinal, row in enumerate(selected):
            capture.set(cv2.CAP_PROP_POS_FRAMES, row["frame_index"])
            ok, original = capture.read()
            if not ok or original.shape[:2] != (EXPECTED_HEIGHT, EXPECTED_WIDTH):
                raise ValueError(f"candidate context decode failed at {row['frame_index']}")
            box = row["original_box_inclusive"]
            crop_box = context_box(box, EXPECTED_WIDTH, EXPECTED_HEIGHT)
            left, top, right, bottom = crop_box
            raw = original[top:bottom+1, left:right+1].copy()
            blue = raw.copy()
            local = [box[0]-left, box[1]-top, box[2]-left, box[3]-top]
            cv2.rectangle(blue, local[:2], local[2:], (255, 90, 20),
                          max(3, min(blue.shape[:2]) // 120))
            stem = f"c{ordinal:02d}_f{row['frame_index']:06d}_s{row['slot']}"
            raw_path = raw_context_dir / f"{stem}.png"
            blue_path = blue_context_dir / f"{stem}.png"
            roi_path = roi_dir / f"{stem}.png"
            write_image(raw_path, raw)
            write_image(blue_path, blue)
            write_image(roi_path, row["_roi"])
            exported = {key: value for key, value in row.items() if not key.startswith("_")}
            exported.update({
                "context_box_original_inclusive": crop_box,
                "context_raw_path": raw_path.relative_to(output).as_posix(),
                "context_raw_sha256": sha256(raw_path),
                "context_blue_path": blue_path.relative_to(output).as_posix(),
                "context_blue_sha256": sha256(blue_path),
                "roi_path": roi_path.relative_to(output).as_posix(),
                "roi_file_sha256": sha256(roi_path),
                "initial_human_review": {"label": "", "subtype": "", "condition": "",
                                         "crop_usable": "", "motion": "", "track_id": "",
                                         "reviewed": False, "note": ""},
            })
            exported_candidates.append(exported)
            candidate_contact.append((blue, f"{stem} bin{row['temporal_bin']} {row['geometry_track_id']}"))
    finally:
        capture.release()

    package = {
        "schema": "local_training_scene_human_review_package_v1",
        "contract_id": CONTRACT_ID,
        "scene_id": "intersection_3785878",
        "scene_status": SCENE_STATUS,
        "scene_observation": ("snowy built environment; visibly different from the 2415171 tropical "
                              "intersection, while source/family independence remains user-pending"),
        "source_sha256": EXPECTED_SHA256,
        "source_license": SOURCE_LICENSE,
        "source_path": video.relative_to(PROJECT).as_posix(),
        "source_metadata": metadata,
        "fps": EXPECTED_FPS,
        "review_basis": "empty_human_review_forms",
        "truth_status": "pending_human_annotation",
        "training_performed": False,
        "scoring_performed": False,
        "preprocessing_contract": {
            "version": PREPROCESSING_CONTRACT,
            "input": [EXPECTED_WIDTH, EXPECTED_HEIGHT],
            "normalization": "cv2.resize to 1280x720 with cv2.INTER_AREA before all FPGA analysis",
            "normalized_input": [NORMALIZED_WIDTH, NORMALIZED_HEIGHT],
            "analysis": "FPGA integer grayscale, then [::5,::5] source samples",
            "analysis_size": [256, 144],
            "coordinate_contract": ("all boxes inclusive; analysis cells map outward to normalized "
                                    "5x5 extents, then normalized extents map outward to original pixels"),
        },
        "full_frame_sampling": {
            "rule": "fixed source frames 150..1140 inclusive every 90; independent of candidates/models",
            "frame_indices": FULL_FRAME_IDS,
            "count": len(FULL_FRAME_IDS),
        },
        "candidate_sampling": {
            "input": "default CandidateChainReference top4 across continuous source frames 0..1213",
            "all_candidate_count": len(all_candidates),
            "selected_count": len(exported_candidates),
            "rule": ("three equal source-time bins with quotas [8,8,8]; deterministic hash order; "
                     "prefer one candidate per geometry track globally; later same-track representatives "
                     "allowed only at source-frame gap >=30; exact 32x32 ROI pixel SHA256 dedup globally"),
            "temporal_bin_ranges_inclusive": [[0, 404], [405, 809], [810, 1213]],
            "selected_per_bin": dict(Counter(str(row["temporal_bin"]) for row in exported_candidates)),
            "unique_selected_tracks": len(selected_by_track),
            "same_track_repeat_boundary": "absolute source-frame gap >=30",
            "roi_duplicate_boundary": "exact uint8 32x32 pixel bytes across this candidate review batch",
        },
        "known_2415171_separation_check": known_check,
        "inventory_provenance": {
            "path": INVENTORY.relative_to(PROJECT).as_posix(),
            "sha256": sha256(INVENTORY),
            "selection_status": "selected_from_previously_viewed_inventory; not blind",
        },
        "frames": fixed_frames,
        "candidates": exported_candidates,
    }
    dump(output / "package.json", package)
    (output / "full_gt_review.html").write_text(full_annotation_html(package), encoding="utf-8")
    (output / "candidate_review.html").write_text(candidate_review_html(package), encoding="utf-8")
    write_image(output / "qa_full12_contact.png", contact_sheet(fixed_contact, 4, (320, 180)))
    write_image(output / "qa_candidate24_contact.png", contact_sheet(candidate_contact, 4, (360, 240)))

    dependencies = [SCRIPT, TOOLS / "candidate_chain_reference.py",
                    TOOLS / "roi_dataset_tool.py", TOOLS / "analyze_virat_failure_sources.py",
                    TEMPLATE]
    artifact_hashes = {
        path.relative_to(output).as_posix(): sha256(path)
        for path in sorted(output.rglob("*")) if path.is_file() and path.name != "receipt.json"
    }
    receipt = {
        "schema": "local_training_review_receipt_v1",
        "source": {"path": video.relative_to(PROJECT).as_posix(), "sha256": EXPECTED_SHA256,
                   "license": SOURCE_LICENSE, **metadata},
        "scene_status": SCENE_STATUS,
        "preprocessing_contract_version": PREPROCESSING_CONTRACT,
        "decoded_source_interval_inclusive": [0, EXPECTED_FRAMES - 1],
        "full_frame_count": len(fixed_frames),
        "candidate_count": len(exported_candidates),
        "candidate_sampling": package["candidate_sampling"],
        "dependency_hashes": {path.relative_to(PROJECT).as_posix(): sha256(path)
                              for path in dependencies},
        "artifact_hashes": artifact_hashes,
        "assertions": {
            "all_human_labels_initially_blank": True,
            "all_human_confirmations_initially_false": True,
            "continuous_default_candidate_chain": True,
            "classification_model_loaded": False,
            "training_performed": False,
            "scoring_performed": False,
            "fixed_full_frame_sampling_model_independent": True,
            "source_frame_identity_preserved": True,
            "blind_or_sealed_source_read": False,
            "historical_catalog_modified": False,
        },
        "receipt_self_hash_included": False,
    }
    dump(output / "receipt.json", receipt)
    return {"output": str(output.resolve()), "full_frames": len(fixed_frames),
            "candidates": len(exported_candidates), "source_sha256": EXPECTED_SHA256}


def self_test() -> dict[str, Any]:
    assert FULL_FRAME_IDS == [150, 240, 330, 420, 510, 600, 690, 780, 870, 960, 1050, 1140]
    assert analysis_to_normalized([0, 0, 255, 143]) == [0, 0, 1279, 719]
    assert normalized_to_original([0, 0, 1279, 719]) == [0, 0, 1919, 1079]
    assert normalized_to_original([1, 1, 4, 4]) == [1, 1, 7, 7]
    assert inclusive_iou([0, 0, 9, 9], [0, 0, 9, 9]) == 1.0
    fixture = []
    for bin_index, base in enumerate((0, 405, 810)):
        for index in range(12):
            fixture.append({"temporal_bin": bin_index, "geometry_track_id": f"t{bin_index}_{index}",
                            "frame_index": base + index, "slot": 0,
                            "roi_pixel_sha256": hashlib.sha256(f"{bin_index}:{index}".encode()).hexdigest()})
    selected = select_review_candidates(fixture)
    assert len(selected) == 24
    assert Counter(row["temporal_bin"] for row in selected) == {0: 8, 1: 8, 2: 8}
    assert len({row["geometry_track_id"] for row in selected}) == 24
    return {"self_test": "PASS", "fixed_frames": len(FULL_FRAME_IDS),
            "candidate_limit": MAX_CANDIDATES}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video", type=Path, default=VIDEO)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--reuse-v1", action="store_true",
                        help="Refresh the verified v1 review pages without decoding the video again")
    args = parser.parse_args()
    if args.self_test:
        result = self_test()
    elif args.reuse_v1:
        guard_allowed(args.output)
        if args.output.resolve() == V1_OUTPUT.resolve() or args.output.exists():
            raise ValueError("refresh requires a new output directory; preserve v1")
        receipt_path = V1_OUTPUT / "receipt.json"
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        for name, expected in receipt["artifact_hashes"].items():
            path = (V1_OUTPUT / name).resolve()
            if not path.is_relative_to(V1_OUTPUT.resolve()) or sha256(path) != expected:
                raise ValueError(f"v1 artifact changed: {name}")
        for name, expected in receipt["dependency_hashes"].items():
            path = (PROJECT / name).resolve()
            if not path.is_relative_to(PROJECT) or (path != SCRIPT and sha256(path) != expected):
                raise ValueError(f"v1 dependency changed: {name}")
        if args.video.resolve() != VIDEO.resolve() or sha256(VIDEO) != EXPECTED_SHA256:
            raise ValueError("refresh source differs from the registered video")
        package = json.loads((V1_OUTPUT / "package.json").read_text(encoding="utf-8"))
        if package["source_sha256"] != EXPECTED_SHA256:
            raise ValueError("v1 package source mismatch")
        if any(f["completed"] or f["targets"] for f in package["frames"]):
            raise ValueError("do not replace completed human annotations")
        if any(any(value not in ("", False) for value in c["initial_human_review"].values())
               for c in package["candidates"]):
            raise ValueError("do not replace candidate human labels")
        shutil.copytree(V1_OUTPUT, args.output)
        package["contract_id"] = CONTRACT_ID
        package["candidate_sampling"]["startup_samples"] = (
            "includes source frames before five seconds; training review only, not post-warmup metrics")
        dump(args.output / "package.json", package)
        (args.output / "full_gt_review.html").write_text(full_annotation_html(package), encoding="utf-8")
        (args.output / "candidate_review.html").write_text(candidate_review_html(package), encoding="utf-8")
        receipt["reused_from"] = {"path": V1_OUTPUT.relative_to(PROJECT).as_posix(),
                                "receipt_sha256": sha256(receipt_path), "video_decoded_again": False}
        receipt["dependency_hashes"][SCRIPT.relative_to(PROJECT).as_posix()] = sha256(SCRIPT)
        receipt["candidate_sampling"] = package["candidate_sampling"]
        receipt["artifact_hashes"] = {
            p.relative_to(args.output).as_posix(): sha256(p)
            for p in sorted(args.output.rglob("*")) if p.is_file() and p.name != "receipt.json"}
        dump(args.output / "receipt.json", receipt)
        result = {"output": str(args.output), "full_frames": len(package["frames"]),
                  "candidates": len(package["candidates"]), "video_decoded_again": False}
    else:
        result = build(args.video, args.output)
    print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))


if __name__ == "__main__":
    main()
