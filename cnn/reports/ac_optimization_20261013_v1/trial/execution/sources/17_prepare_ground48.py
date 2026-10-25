"""Freeze 48 ground-development frames for manual review; export only after all sign-offs."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from copy import deepcopy
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile
from typing import Any

from .import_verified_review import CHECKS, ReviewError, _validate_patch


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "cnn/reports/verified_gt_workflow_20261006"
OUTPUT = ROOT / "cnn/reports/post_review_s_20261007_v1/ground48"
CAMERA_A = "virat-parking-lot-camera-a"
CAMERA_B = "virat-010107-camera-b"
BINDING_FIELDS = ("image_id", "source_sha256", "width", "height", "bucket", "split", "original")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def json_hash(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def dataset_id(document: dict[str, Any]) -> str:
    return json_hash({
        "annotation_policy_sha256": document["annotation_policy_sha256"],
        "samples": [{key: row[key] for key in BINDING_FIELDS} for row in document["samples"]],
    })


def write_json(path: Path, value: object) -> None:
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write("\n")


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ReviewError(f"expected JSON object: {path}")
    return value


def clip_id(sample: dict[str, Any]) -> str:
    prefix, separator, suffix = sample["image_id"].rpartition("_f")
    if not separator or not suffix.isdigit():
        raise ReviewError(f"cannot recover clip id from {sample['image_id']}")
    return prefix


def even_positions(count: int, wanted: int = 6) -> list[int]:
    if count < wanted or wanted < 2:
        raise ReviewError(f"cannot select {wanted} evenly spaced positions from {count}")
    return [(index * (count - 1) + (wanted - 1) // 2) // (wanted - 1)
            for index in range(wanted)]


def select_samples(original: dict[str, Any], teacher: dict[str, Any]) \
        -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if original.get("dataset_id") != teacher.get("dataset_id"):
        raise ReviewError("source manifests have different dataset_id values")
    if original.get("annotation_policy_sha256") != teacher.get("annotation_policy_sha256"):
        raise ReviewError("source manifests have different annotation policies")
    original_by_id = {row["image_id"]: row for row in original.get("samples", [])}
    teacher_by_id = {row["image_id"]: row for row in teacher.get("samples", [])}
    if original_by_id.keys() != teacher_by_id.keys():
        raise ReviewError("source manifests do not contain the same images")

    road = [row for row in teacher_by_id.values() if row.get("bucket") == "road_development"]
    camera_b = sorted((row for row in road if row.get("camera_id") == CAMERA_B),
                      key=lambda row: row["frame_index"])
    camera_a_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in road:
        if row.get("camera_id") == CAMERA_A:
            camera_a_groups[clip_id(row)].append(row)
    if len(camera_b) != 24 or len(camera_a_groups) != 4:
        raise ReviewError("expected camera-b=24 and exactly four camera-a clips")

    selected_teacher: list[dict[str, Any]] = []
    selected_original: list[dict[str, Any]] = []
    for batch, (camera_a_clip, rows) in enumerate(sorted(camera_a_groups.items()), 1):
        rows.sort(key=lambda row: row["frame_index"])
        camera_a = [rows[index] for index in even_positions(len(rows))]
        batch_rows = [*camera_a, *camera_b[(batch - 1) * 6:batch * 6]]
        if len(batch_rows) != 12:
            raise ReviewError(f"batch {batch} is not 12 images")
        for ordinal, source_row in enumerate(batch_rows, 1):
            image_id = source_row["image_id"]
            frozen = deepcopy(source_row)
            frozen["review_batch"] = batch
            frozen["review_batch_ordinal"] = ordinal
            frozen["selection_clip_id"] = camera_a_clip if source_row["camera_id"] == CAMERA_A else clip_id(source_row)
            source_original = deepcopy(original_by_id[image_id])
            source_original.update({key: frozen[key] for key in
                                    ("review_batch", "review_batch_ordinal", "selection_clip_id")})
            for key in BINDING_FIELDS:
                if source_original[key] != frozen[key]:
                    raise ReviewError(f"source fields changed between manifests: {image_id}.{key}")
            selected_teacher.append(frozen)
            selected_original.append(source_original)
    return selected_original, selected_teacher


def _manifest(source: dict[str, Any], samples: list[dict[str, Any]]) -> dict[str, Any]:
    result = {
        "schema": "cnn_review_workbench_v1",
        "annotation_policy_sha256": source["annotation_policy_sha256"],
        "samples": samples,
        "train_required_count": 0,
        "verified_gt": False,
        "training_started": False,
        "teacher_status": "hints_only_not_ground_truth",
        "human_signed_frames": 0,
        "formal_acceptance": False,
        "bucket_counts": {"road_development": 48},
        "selection_status": "pending_human_full_frame_review",
    }
    result["dataset_id"] = dataset_id(result)
    return result


def blank_patch(manifest: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "cnn_review_patch_v1",
        "dataset_id": manifest["dataset_id"],
        "annotation_policy_sha256": manifest["annotation_policy_sha256"],
        "reviews": [{
            "image_id": sample["image_id"],
            "source_sha256": sample["source_sha256"],
            "reviewer": "",
            "reviewed_at_utc": "",
            "raw_seen": False,
            "complete": False,
            "checks": {key: False for key in sorted(CHECKS)},
            "actions": [],
            "notes": "",
        } for sample in manifest["samples"]],
    }


def render_workbench(template: str, manifest: dict[str, Any]) -> str:
    replacements = {
        "<title>RoadYOLO 人工审核台</title>": "<title>RoadYOLO Ground48 分批人工审核台</title>",
        "<h1>RoadYOLO 原图画框人工审核台</h1>": "<h1>RoadYOLO Ground48 分批人工审核台</h1>",
        '''<label>桶 <select id="bucket">\n    <option value="train_review">训练审核（默认）</option>\n    <option value="road_development">道路开发</option>\n    <option value="person_background_aux">压力集</option>\n    <option value="all">全部</option>\n  </select></label>''': '''<label>批次 <select id="bucket">\n    <option value="1">第 1 批（12 张）</option>\n    <option value="2">第 2 批（12 张）</option>\n    <option value="3">第 3 批（12 张）</option>\n    <option value="4">第 4 批（12 张）</option>\n    <option value="all">全部 48 张</option>\n  </select></label>''',
        'if (manifest.train_required_count !== 128) errors.push("train_required_count 必须为 128");':
            'if (manifest.train_required_count !== 0) errors.push("ground48 train_required_count 必须为 0");',
        'if (manifest.samples.length !== 276) errors.push("samples 必须固定为 276 张");':
            'if (manifest.samples.length !== 48) errors.push("ground48 samples 必须固定为 48 张");',
        'if (counts.train_review !== 128 || counts.road_development !== 124 || counts.person_background_aux !== 24) errors.push("三桶数量必须为 128/124/24");':
            'if (counts.train_review !== 0 || counts.road_development !== 48 || counts.person_background_aux !== 0) errors.push("ground48 桶数量必须为 0/48/0");',
        'const bucket = $("bucket").value;\n    order = manifest.samples.map((item, index) => ({item, index})).filter(row => bucket === "all" || row.item.bucket === bucket);':
            'const bucket = $("bucket").value;\n    order = manifest.samples.map((item, index) => ({item, index})).filter(row => bucket === "all" || String(row.item.review_batch) === bucket);',
        '`${item.image_id} · ${item.bucket}/${item.split} · ${item.width}×${item.height} · 风险 ${item.review_score} · 警告 ${item.warnings.length ? item.warnings.join("；") : "无"}`':
            '`${item.image_id} · 第${item.review_batch}批 ${item.review_batch_ordinal}/12 · ${item.camera_id} · ${item.width}×${item.height} · 风险 ${item.review_score} · 警告 ${item.warnings.length ? item.warnings.join("；") : "无"}`',
        'image_id: sample.image_id, source_sha256: sample.source_sha256, reviewer: "", raw_seen: false, complete: false,':
            'image_id: sample.image_id, source_sha256: sample.source_sha256, reviewer: "1", reviewed_at_utc: "", raw_seen: false, complete: false,',
        'placeholder="人工填写，不能自动生成"': 'placeholder="默认1，可修改"',
        'function markChanged() { review().complete = false; renderComplete(); renderProgress(); }':
            'function markChanged() { review().complete = false; review().reviewed_at_utc = ""; renderComplete(); renderProgress(); }',
        'if (typeof candidate.reviewer !== "string" || typeof candidate.raw_seen !== "boolean" || typeof candidate.complete !== "boolean" || typeof candidate.notes !== "string") throw new Error(`${item.image_id}: 审核记录字段非法`);':
            'if (typeof candidate.reviewer !== "string" || typeof candidate.reviewed_at_utc !== "string" || typeof candidate.raw_seen !== "boolean" || typeof candidate.complete !== "boolean" || typeof candidate.notes !== "string") throw new Error(`${item.image_id}: 审核记录字段非法`);',
        'return {image_id: item.image_id, source_sha256: item.source_sha256, reviewer: candidate.reviewer, raw_seen: candidate.raw_seen, complete: candidate.complete,':
            'return {image_id: item.image_id, source_sha256: item.source_sha256, reviewer: candidate.reviewer.trim() ? candidate.reviewer : "1", reviewed_at_utc: candidate.reviewed_at_utc, raw_seen: candidate.raw_seen, complete: candidate.complete,',
        '$("sign").addEventListener("click", () => { const errors = Core.completionErrors(sample(), review()); if (errors.length) { alert("不能签署 complete：\\n" + errors.join("\\n")); return; } review().complete = true; renderComplete(); renderProgress(); });':
            '''$("sign").addEventListener("click", () => {
    const record = review();
    const signed = {...record, raw_seen: true, checks: Object.fromEntries(Core.checks.map(key => [key, true]))};
    const errors = Core.completionErrors(sample(), signed);
    if (errors.length) { alert("不能签署 complete：\\n" + errors.join("\\n")); return; }
    Object.assign(record, signed, {complete: true, reviewed_at_utc: new Date().toISOString()});
    renderComplete(); renderProgress();
  });''',
        '$("unsign").addEventListener("click", () => { review().complete = false; renderComplete(); renderProgress(); });':
            '$("unsign").addEventListener("click", () => { review().complete = false; review().reviewed_at_utc = ""; renderComplete(); renderProgress(); });',
        '      <button id="rawSeen" class="primary">我已单独看过 RAW 原图</button>\n      <span id="rawState" class="meta"></span>': '',
        '''      <h3>逐项检查</h3>
      <div id="checks" class="checks">
        <label><input type="checkbox" data-check="person"> person</label>
        <label><input type="checkbox" data-check="vehicle"> vehicle</label>
        <label><input type="checkbox" data-check="rider"> rider</label>
        <label><input type="checkbox" data-check="parked_vehicle"> parked vehicle</label>
        <label><input type="checkbox" data-check="small_occluded"> 小目标/遮挡</label>
        <label><input type="checkbox" data-check="ignore"> ignore 区域</label>
      </div>''': '      <p class="meta">点击“签署本图 complete”即确认已查看无框原图，并检查人、车、骑行者、停放车辆、小目标/遮挡和 ignore；不再分别勾选。未核对完请勿签署。</p>',
        '    document.querySelectorAll("[data-check]").forEach(input => input.checked = record.checks[input.dataset.check]);': '',
        '    $("rawSeen").disabled = view !== "raw" || review().raw_seen; draw();': '    draw();',
        '    const record = review(); $("rawState").textContent = record.raw_seen ? "✓ RAW 已人工确认" : "RAW 尚未确认";\n    $("rawSeen").disabled = view !== "raw" || record.raw_seen;': '    const record = review();',
        '  $("rawSeen").addEventListener("click", () => { if (view !== "raw") return; review().raw_seen = true; markChanged(); renderComplete(); });': '',
        '  document.querySelectorAll("[data-check]").forEach(input => input.addEventListener("change", () => { review().checks[input.dataset.check] = input.checked; markChanged(); }));': '',
        '    if (!record.raw_seen || !record.reviewer.trim() || Core.checks.some(key => !record.checks[key])) { alert("先人工查看 RAW、填写审核人并完成六项检查。错误来源框应先逐项 M/I/D。"); return; }':
            '    if (!record.reviewer.trim()) { alert("先填写审核人。错误来源框应先逐项 M/I/D。"); return; }',
    }
    for old, new in replacements.items():
        if old not in template:
            raise ReviewError(f"workbench template anchor missing: {old[:80]}")
        template = template.replace(old, new, 1)
    # Scoped extension: historical review pages and frozen manifests stay intact.
    batch_script = (ROOT / "cnn/ground48_teacher_batch.js").read_text(encoding="utf-8")
    anchor = '  $("teacherStatus").textContent = ""; rebuildOrder(null);'
    if template.count(anchor) != 1:
        raise ReviewError("teacher batch insertion anchor missing or duplicated")
    template = template.replace(anchor, batch_script + "\n" + anchor, 1)
    template = template.replace("Teacher 只能逐项参考，不能批量采用。",
                                "Teacher 可多选采用为 AI 辅助草稿；必须人工核对后签署。", 1)
    template = template.replace("■ 当前手动画框", "■ 人工/已采用草稿框", 1)
    template = template.replace('view !== "raw" && currentBox && Core.validBox',
                                'view !== "raw" && showDraftBoxes && currentBox && Core.validBox', 1)
    template = template.replace(
        'sample().teacher.forEach(item => drawBox(item.bbox, "#ff9800", "", [8, 5]));',
        'sample().teacher.forEach(item => drawBox(item.bbox, "#ff9800", `${item.candidate_id} ${item.class} ${item.score.toFixed(2)}`, [8, 5]));', 1)
    encoded = json.dumps(manifest, ensure_ascii=False, allow_nan=False).replace("<", "\\u003c")
    if template.count("__REVIEW_MANIFEST_JSON__") != 1:
        raise ReviewError("workbench manifest placeholder is missing or duplicated")
    return template.replace("__REVIEW_MANIFEST_JSON__", encoded)


def validate_ground_manifest(path: Path, *, check_files: bool = True) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    text = str(path.resolve()).replace("\\", "/").lower()
    if "blind" in text or "reserve" in text:
        raise ReviewError("blind/reserve manifests are forbidden")
    manifest = read_json(path)
    if manifest.get("schema") != "cnn_review_workbench_v1" or manifest.get("train_required_count") != 0:
        raise ReviewError("not a ground48 review manifest")
    samples = manifest.get("samples")
    if not isinstance(samples, list) or len(samples) != 48:
        raise ReviewError("ground48 manifest must contain exactly 48 samples")
    if dataset_id(manifest) != manifest.get("dataset_id"):
        raise ReviewError("ground48 dataset_id binding mismatch")
    if sha256_file(path.parent / "annotation_policy_v1.md") != manifest.get("annotation_policy_sha256"):
        raise ReviewError("ground48 annotation policy hash mismatch")
    by_id: dict[str, dict[str, Any]] = {}
    for sample in samples:
        image_id = sample.get("image_id")
        if not isinstance(image_id, str) or not image_id or image_id in by_id:
            raise ReviewError("ground48 image_id is missing or duplicated")
        if sample.get("bucket") != "road_development" or sample.get("split") != "dev":
            raise ReviewError(f"ground48 bucket/split mismatch: {image_id}")
        relative = Path(sample.get("raw_file", ""))
        if relative.is_absolute() or ".." in relative.parts or any(word in str(relative).lower() for word in ("blind", "reserve")):
            raise ReviewError(f"unsafe raw path: {image_id}")
        raw = path.parent / relative
        if check_files and (not raw.is_file() or sha256_file(raw) != sample.get("source_sha256")):
            raise ReviewError(f"ground48 image hash mismatch: {image_id}")
        by_id[image_id] = sample
    if Counter(row["camera_id"] for row in samples) != Counter({CAMERA_A: 24, CAMERA_B: 24}):
        raise ReviewError("ground48 camera counts must be 24/24")
    if Counter(row["review_batch"] for row in samples) != Counter({1: 12, 2: 12, 3: 12, 4: 12}):
        raise ReviewError("ground48 batches must be four groups of 12")
    for batch in range(1, 5):
        if Counter(row["camera_id"] for row in samples if row["review_batch"] == batch) != Counter({CAMERA_A: 6, CAMERA_B: 6}):
            raise ReviewError(f"ground48 batch {batch} must contain six images per camera")
    return manifest, by_id


def build_package(source: Path = SOURCE, output: Path = OUTPUT) -> dict[str, Any]:
    source, output = Path(source), Path(output)
    if output.exists():
        raise FileExistsError(f"preserve existing ground48 package; no overwrite: {output}")
    original_path = source / "manifest_original.json"
    teacher_path = source / "review_manifest_teacher.json"
    policy_path = source / "annotation_policy_v1.md"
    template_path = ROOT / "cnn/review_workbench.html"
    index_path = source / "index.html"
    for path in (original_path, teacher_path, policy_path, template_path, index_path):
        lowered = str(path.resolve()).lower()
        if "blind" in lowered or "reserve" in lowered or not path.is_file():
            raise ReviewError(f"unsafe or missing source: {path}")
    original, teacher = read_json(original_path), read_json(teacher_path)
    selected_original, selected_teacher = select_samples(original, teacher)

    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="ground48_", dir=output.parent) as temporary:
        stage = Path(temporary)
        shutil.copy2(policy_path, stage / "annotation_policy_v1.md")
        for original_row, teacher_row in zip(selected_original, selected_teacher, strict=True):
            image_id = teacher_row["image_id"]
            folder = stage / "images" / image_id
            folder.mkdir(parents=True)
            for field in ("raw_file", "gt_overlay_file"):
                source_file = source / teacher_row[field]
                destination = folder / source_file.name
                shutil.copy2(source_file, destination)
                teacher_row[field] = destination.relative_to(stage).as_posix()
                original_row[field] = teacher_row[field]
            if sha256_file(stage / teacher_row["raw_file"]) != teacher_row["source_sha256"]:
                raise ReviewError(f"copied image hash mismatch: {image_id}")

        frozen = _manifest(original, selected_original)
        review = _manifest(teacher, selected_teacher)
        if frozen["dataset_id"] != review["dataset_id"]:
            raise ReviewError("teacher hints changed the frozen dataset binding")
        write_json(stage / "manifest_original.json", frozen)
        write_json(stage / "review_manifest_teacher.json", review)
        write_json(stage / "review_patch_template.json", blank_patch(review))

        batches = []
        for batch in range(1, 5):
            rows = [row for row in review["samples"] if row["review_batch"] == batch]
            batches.append({
                "batch": batch,
                "image_count": len(rows),
                "camera_counts": dict(sorted(Counter(row["camera_id"] for row in rows).items())),
                "image_ids": [row["image_id"] for row in rows],
            })
        selection = {
            "schema": "cnn_ground48_selection_v1",
            "status": "pending_human_review",
            "dataset_id": review["dataset_id"],
            "selection_rule": "camera-b all 24; camera-a four clips x six inclusive evenly spaced sorted ordinals",
            "batch_rule": "each batch has one camera-a clip x6 and chronological camera-b x6",
            "image_count": 48,
            "camera_counts": {CAMERA_A: 24, CAMERA_B: 24},
            "batches": batches,
            "selected": [{key: row[key] for key in
                          ("image_id", "source_sha256", "camera_id", "selection_clip_id",
                           "frame_index", "review_batch", "review_batch_ordinal")}
                         for row in review["samples"]],
            "evidence_boundary": [
                "Development data already inspected; not blind or formal acceptance data.",
                "Teacher boxes are hints only and are not signed ground truth.",
                "No human review state is inherited; all 48 frames remain pending.",
                "ground_val48.json is forbidden until every full frame is manually complete.",
            ],
        }
        write_json(stage / "selection.json", selection)
        (stage / "index.html").write_text(
            render_workbench(template_path.read_text(encoding="utf-8"), review), encoding="utf-8")

        source_hashes = {path.name: sha256_file(path) for path in
                         (original_path, teacher_path, policy_path, template_path, index_path)}
        receipt = {
            "schema": "cnn_ground48_selection_receipt_v1",
            "status": "pending_human_review",
            "dataset_id": review["dataset_id"],
            "source_dataset_id": original["dataset_id"],
            "image_count": 48,
            "human_complete_count": 0,
            "pending_count": 48,
            "all_raw_seen": False,
            "all_checks_complete": False,
            "ground_val48_generated": False,
            "formal_acceptance": False,
            "training_started": False,
            "source_sha256": source_hashes,
            "selected_image_sha256": {row["image_id"]: row["source_sha256"] for row in review["samples"]},
            "outputs": {
                name: sha256_file(stage / name) for name in
                ("manifest_original.json", "review_manifest_teacher.json",
                 "review_patch_template.json", "selection.json", "index.html",
                 "annotation_policy_v1.md")
            },
        }
        write_json(stage / "selection_receipt.json", receipt)
        os.replace(stage, output)
    return receipt


def _parse_signed_time(value: Any, image_id: str) -> str:
    if not isinstance(value, str) or not value:
        raise ReviewError(f"{image_id}: complete review needs reviewed_at_utc")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ReviewError(f"{image_id}: invalid reviewed_at_utc") from exc
    if parsed.tzinfo is None:
        raise ReviewError(f"{image_id}: reviewed_at_utc must include a timezone")
    return value


def export_documents(manifest_path: Path, patch_path: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    manifest, samples = validate_ground_manifest(Path(manifest_path))
    patch_path = Path(patch_path)
    if any(word in str(patch_path.resolve()).replace("\\", "/").lower()
           for word in ("blind", "reserve")):
        raise ReviewError("blind/reserve patch paths are forbidden")
    patch, reviews, patch_raw = _validate_patch(patch_path, manifest, samples)
    if set(reviews) != set(samples) or any(not review["complete"] for review in reviews.values()):
        raise ReviewError("ground48 export requires exactly 48 complete human reviews")
    for image_id, review in reviews.items():
        _parse_signed_time(review.get("reviewed_at_utc"), image_id)

    from .dataset import _letterbox_transform, _letterboxed_box

    verified_images, dataset_rows, label_counts = [], [], Counter()
    time_groups: dict[str, set[tuple[str, str, str]]] = defaultdict(set)
    for sample in manifest["samples"]:
        review = reviews[sample["image_id"]]
        originals = {row["target_id"]: row for row in sample["original"]}
        labels = []
        for action in review["actions"]:
            if action["action"] == "D":
                continue
            label = {key: action[key] for key in
                     ("target_id", "class", "bbox", "action", "reason", "ai_assisted")}
            label["source"] = "manual_review"
            original = originals.get(action["target_id"])
            label["original_target_id"] = action["target_id"] if original else None
            if original:
                label["source_target_id"] = original["source_target_id"]
                label["source_category"] = original["source_category"]
            labels.append(label)
            label_counts[action["class"]] += 1
            if action["class"] != "ignore":
                group = str(original["source_target_id"]) if original else action["target_id"]
                time_groups[action["class"]].add((sample["selection_clip_id"], group,
                                                  "source" if original else sample["image_id"]))
        native = {
            "image_id": sample["image_id"], "camera_id": sample["camera_id"],
            "clip_id": sample["selection_clip_id"], "frame_index": sample["frame_index"],
            "width": sample["width"], "height": sample["height"],
            "raw_file": sample["raw_file"], "source_sha256": sample["source_sha256"],
            "manual_review": {key: review[key] for key in
                              ("reviewer", "reviewed_at_utc", "raw_seen", "complete", "checks", "notes")},
            "labels": labels,
        }
        verified_images.append(native)
        transform = _letterbox_transform(sample["width"], sample["height"])
        boxes, classes, ignores = [], [], []
        for label in labels:
            x1, y1, x2, y2 = label["bbox"]
            box = _letterboxed_box([x1, y1, x2 - x1, y2 - y1], transform)
            if label["class"] == "ignore":
                ignores.append(box)
            else:
                boxes.append(box)
                classes.append({"person": 0, "vehicle": 1}[label["class"]])
        dataset_rows.append({
            "image": sample["raw_file"], "source_sha256": sample["source_sha256"],
            "scene_id": sample["source_scene_id"], "source_frame": sample["frame_index"],
            "split": "val", "incomplete_frame": False,
            "boxes": boxes, "labels": classes, "ignore_boxes": ignores,
            "preprocess": {"raw_image": True, "letterbox_1280x720": transform},
            "teacher_key": sample["image_id"], "manual_review_image_id": sample["image_id"],
            "camera_id": sample["camera_id"], "clip_id": sample["selection_clip_id"],
            "native_frame_index": sample["frame_index"], "native_labels": labels,
        })
    verified = {
        "schema": "cnn_ground48_verified_labels_v1", "dataset_id": manifest["dataset_id"],
        "annotation_policy_sha256": manifest["annotation_policy_sha256"],
        "status": "validated_ready", "formal_acceptance": False, "images": verified_images,
    }
    ground = {
        "schema_version": 1, "task": "detection", "input_size": [512, 288],
        "classes": ["person", "vehicle"], "manifest_status": "development_ground48",
        "purpose": "signed full-frame development validation only; not blind or formal acceptance",
        "training_eligible": True, "evaluation_only": True, "formal_acceptance": False,
        "dataset_id": manifest["dataset_id"], "images": dataset_rows,
    }
    receipt = {
        "schema": "cnn_ground48_export_receipt_v1", "status": "validated_ready",
        "dataset_id": manifest["dataset_id"], "image_count": 48, "complete_count": 48,
        "pending_count": 0, "all_raw_seen": True, "all_checks_complete": True,
        "review_manifest_sha256": sha256_file(Path(manifest_path)),
        "patch_sha256": hashlib.sha256(patch_raw).hexdigest(),
        "annotation_policy_sha256": manifest["annotation_policy_sha256"],
        "selected_image_ids": [row["image_id"] for row in manifest["samples"]],
        "selected_image_sha256": {row["image_id"]: row["source_sha256"] for row in manifest["samples"]},
        "label_counts": dict(sorted(label_counts.items())),
        "time_group_counts": {key: len(value) for key, value in sorted(time_groups.items())},
        "vehicle_subclass_counts": "not_measured",
        "formal_acceptance": False, "training_started": False,
    }
    return verified, ground, receipt


def export_patch(package: Path, patch_path: Path) -> dict[str, Any]:
    package = Path(package)
    verified, ground, receipt = export_documents(package / "review_manifest_teacher.json", patch_path)
    signed_patch = Path(patch_path).read_bytes()
    if hashlib.sha256(signed_patch).hexdigest() != receipt["patch_sha256"]:
        raise ReviewError("signed patch changed during export")
    targets = {
        "ground48_verified_labels.json": verified,
        "ground_val48.json": ground,
    }
    if any((package / name).exists() for name in
           (*targets, "review_patch_signed.json", "ground48_export_receipt.json")):
        raise FileExistsError("preserve existing ground48 export; no overwrite")
    for name, document in targets.items():
        write_json(package / name, document)
        receipt[name.replace(".", "_") + "_sha256"] = sha256_file(package / name)
    with (package / "review_patch_signed.json").open("xb") as stream:
        stream.write(signed_patch)
    receipt["review_patch_signed_json_sha256"] = sha256_file(
        package / "review_patch_signed.json")
    receipt["ground_val48_sha256"] = sha256_file(package / "ground_val48.json")
    write_json(package / "ground48_export_receipt.json", receipt)
    return receipt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--patch", type=Path, help="export only after a complete signed patch")
    args = parser.parse_args(argv)
    result = export_patch(OUTPUT, args.patch) if args.patch else build_package()
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
