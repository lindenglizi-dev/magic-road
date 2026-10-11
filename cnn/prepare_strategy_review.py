"""Prepare bounded, model-blind train review; never relabel or start training."""
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import html
import json
import os
from pathlib import Path
import shutil
import subprocess

from PIL import Image, ImageDraw

from .dataset import _letterbox_transform, _letterboxed_box, _refuse_blind, sha256_file
from .public_video import read_visdrone_mot, VISDRONE_NAMES

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "cnn/reports/strategy_trial_20261006"
DATA = ROOT / "cnn/data/visdrone_vid_train/raw_manifest/dataset.json"
PLAN = ROOT / "cnn/reports/error_diagnosis_20261006/RoadYOLO_策略选择与后续执行计划_20261006.txt"
GROUPS = ("bicycle", "motorcycle", "localization_or_semantic_suspect", "ordinary_control")


def dump(path, value):
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)


def candidates(row, group):
    metadata = row["box_metadata"]
    categories = {item["category_id"] for item in metadata}
    if group == "bicycle":
        return 3 in categories
    if group == "motorcycle":
        return 10 in categories
    if group == "localization_or_semantic_suspect":
        return any(item["truncation"] or item["occlusion"] == 2 for item in metadata)
    if group == "ordinary_control":
        return set(row["labels"]) == {0, 1} and not categories.intersection({3, 10})
    raise ValueError(group)


def select(rows, count=32, gap=60):
    chosen, used, frames = [], set(), defaultdict(list)
    for group in GROUPS:
        scenes = defaultdict(list)
        for row in rows:
            if row["split"] == "train" and candidates(row, group):
                scenes[row["scene_id"]].append(row)
        for values in scenes.values():
            values.sort(key=lambda row: row["source_frame"])
        selected = 0
        while selected < count:
            progress = False
            for scene in sorted(scenes):
                row = next((row for row in scenes[scene] if row["image"] not in used
                            and all(abs(row["source_frame"] - old) >= gap for old in frames[scene])), None)
                if row is None:
                    continue
                chosen.append((group, row))
                frames[scene].append(row["source_frame"])
                used.add(row["image"])
                selected += 1
                progress = True
                if selected == count:
                    break
            if not progress:
                break
    return chosen


def preflight():
    release = ROOT / "cnn/releases/RoadYOLO-S4-512_20261005_before_supervised5"
    manifest = json.loads((release / "release.json").read_text(encoding="utf-8"))
    mismatches = [name for name, digest in manifest["files"].items()
                  if sha256_file(release / name) != digest]
    checkpoint = release / "cnn/runs/person_native_recovery_20261004/epoch_0006.pt"
    assert sha256_file(checkpoint) == "17c3cd644bd80a5f66e24eb3f510126fbb5db5bbb302e39250d78d339b6e5d42"
    assert not mismatches, mismatches
    # Scope process evidence to Python commands in this project; no service mutation.
    command = ("Get-CimInstance Win32_Process | Where-Object { $_.Name -match 'python' "
               "-and $_.CommandLine -match 'qiansai' } | Select-Object ProcessId,ParentProcessId,CommandLine | ConvertTo-Json -Depth 3")
    processes = subprocess.run(["powershell", "-NoProfile", "-Command", command],
                               capture_output=True, text=True, check=True, timeout=30)
    values = json.loads(processes.stdout.strip() or "[]")
    values = values if isinstance(values, list) else [values]
    values = [row for row in values if row["ProcessId"] != os.getpid()]
    gpu = subprocess.run(["nvidia-smi", "--query-gpu=uuid,name,temperature.gpu,memory.used,utilization.gpu",
                          "--format=csv,noheader"], capture_output=True, text=True, check=True, timeout=15)
    sources = [PLAN, DATA, ROOT / "cnn/reports/supervised5_oct5/status.json",
               Path(__file__), ROOT / "cnn/dataset.py", ROOT / "cnn/public_video.py"]
    report = dict(status="baseline_integrity_verified_no_training_started",
                  checked_at=datetime.now(timezone.utc).isoformat(),
                  frozen_files=len(manifest["files"]), frozen_mismatches=mismatches,
                  source_checkpoint=str(checkpoint), checkpoint_sha256=sha256_file(checkpoint),
                  disk_free_bytes=shutil.disk_usage(ROOT).free,
                  project_python_process_snapshot=values, gpu_snapshot=gpu.stdout.strip(),
                  snapshot_not_continuous_monitor=True,
                  source_sha256={str(path.relative_to(ROOT)): sha256_file(path) for path in sources},
                  training_started=False, step1_pass=False, step2_pass=False,
                  note="Data review and verified complete ground truth are prerequisites, not waived by preflight.")
    dump(OUT / "preflight.json", report)
    return report


def build():
    if (OUT / "preflight.json").exists() or (OUT / "train_review").exists():
        raise FileExistsError("Preserve partial/completed outputs; inspect before selecting a new version.")
    OUT.mkdir(parents=True, exist_ok=True)
    preflight()
    folder = OUT / "train_review"
    folder.mkdir()
    document = json.loads(DATA.read_text(encoding="utf-8"))
    selected = select(document["images"])
    assert len({row["image"] for _, row in selected}) == len(selected)
    dump(folder / "selection.json", dict(dataset_sha256=sha256_file(DATA),
         model_predictions_used=False, min_same_sequence_frame_gap=60,
         fps_unknown_no_two_second_claim=True, frame_base=1,
         selection="sorted sequence round-robin, then earliest remaining frame; fixed before inference",
         suspect_basis="source truncation or severe occlusion, NOT measured FP from validation",
         requested_per_group=32, actual_per_group=dict(Counter(group for group, _ in selected)),
         samples=[dict(group=group, image=row["image"], scene_id=row["scene_id"],
                       source_frame=row["source_frame"]) for group, row in selected]))
    originals, reviews, artifacts = {}, [], {}
    cards = []
    for index, (group, row) in enumerate(selected, 1):
        path = Path(row["image"])
        _refuse_blind(path)
        assert sha256_file(path) == row["source_sha256"], path
        sequence = path.parent.name
        annotation = path.parent.parent.parent / "annotations" / (sequence + ".txt")
        _refuse_blind(annotation)
        if sequence not in originals:
            assert sha256_file(annotation) == row["source_annotation_sha256"]
            originals[sequence] = read_visdrone_mot(annotation)
        source_rows = originals[sequence][row["source_frame"]]
        source_by_id = {item["target_id"]: item for item in source_rows}
        assert len(source_by_id) == len(source_rows), "duplicate source target ID"
        with Image.open(path) as decoded:
            native = decoded.convert("RGB")
        transform = _letterbox_transform(*native.size)
        assert transform == row["preprocess"]["letterbox_1280x720"]
        for box, metadata in zip(row["boxes"], row["box_metadata"], strict=True):
            original = source_by_id[metadata["target_id"]]
            assert original["category"] == metadata["category_id"]
            assert _letterboxed_box(original["bbox"], transform) == box
        name = f"train_{index:03d}"
        raw = folder / (name + path.suffix.lower())
        shutil.copy2(path, raw)
        assert sha256_file(raw) == row["source_sha256"]
        overlay = native.copy()
        draw = ImageDraw.Draw(overlay)
        for original in source_rows:
            category = original["category"]
            x, y, width, height = original["bbox"]
            color = "lime" if category in (1, 2) else "orange" if category in (3, 10) else "cyan"
            if not original["score"] or category in (0, 7, 8, 11):
                color = "gray"
            draw.rectangle((x, y, x+width, y+height), outline=color, width=2)
            draw.text((x, max(0, y-12)), f"{original['target_id']}:{VISDRONE_NAMES[category]}", fill=color,
                      stroke_width=1, stroke_fill="black")
        overlay.thumbnail((1280, 960))
        panel = folder / (name + "_overlay.jpg")
        overlay.save(panel, quality=94)
        for target in (raw, panel):
            artifacts[target.name] = sha256_file(target)
        reviews.append(dict(sample_id=name, group=group, source_image=str(path),
             source_sha256=row["source_sha256"], source_annotation=str(annotation),
             annotation_sha256=row["source_annotation_sha256"], scene_id=row["scene_id"],
             source_frame_1based=row["source_frame"], native_size=list(native.size),
             source_annotations=source_rows, existing_network_boxes=row["boxes"],
             existing_labels=row["labels"], existing_ignore_boxes=row["ignore_boxes"],
             raw_file=raw.name, overlay_file=panel.name,
             review=dict(reviewer="", all_people_separately_labeled="", vehicle_extent_correct="",
                         missing_targets="", occlusion_truncation_correct="", ignore_correct="",
                         rider_person_boxes_xyxy_source_pixels=[], vehicle_corrections_xyxy_source_pixels=[],
                         uncertain_regions_xyxy_source_pixels=[], notes="", signed_complete=False)))
        cards.append(f'<article><h2>{name} / {html.escape(group)} / {sequence} / f{row["source_frame"]}</h2>'
                     f'<a href="{raw.name}">查看无框完整原图</a><br><a href="{panel.name}">'
                     f'<img loading="lazy" src="{panel.name}" alt="{name}"></a></article>')
        print(json.dumps(dict(prepared=index, total=len(selected), sample=name)), flush=True)
    dump(folder / "review_manifest.json", dict(status="pending_explicit_review_no_labels_changed",
         samples=reviews, training_eligible=False, formal_acceptance=False,
         instruction="Fill review only. Boxes use native source half-open XYXY. Never infer empty regions are background."))
    (folder / "index.html").write_text('<!doctype html><meta charset="utf-8"><title>128帧训练标签审核</title>'
         '<style>body{font-family:sans-serif;background:#151515;color:#eee;margin:24px}img{max-width:100%}'
         'a{color:#7acbff}article{margin:28px 0;border-top:1px solid #555}</style>'
         '<h1>训练标签审核：未改标签、未启动训练</h1>'
         '<p>绿：源行人；橙：自行车/摩托车；青：其他车辆；灰：ignore。颜色是来源分类，不是审核结论。</p>'
         '<p>先看无框完整原图，再检查骑行者是否有独立person框、车体范围、漏标和ignore。'
         '在review_manifest.json的review字段填写结论与原图XYXY框；不确定留uncertain，不签署complete。</p>'
         '<p>疑例依据为原始截断/严重遮挡标志，不冒充模型在训练集上的真实误报。原manifest及验证标签不变。</p>'
         + ''.join(cards), encoding="utf-8")
    for name in ("selection.json", "review_manifest.json", "index.html"):
        artifacts[name] = sha256_file(folder / name)
    counts = dict(Counter(group for group, _ in selected))
    dump(folder / "receipt.json", dict(status="prepared_pending_review", sample_count=len(reviews),
         actual_per_group=counts, requested_128_frames_met=len(reviews) == 128,
         sequence_count=len(originals), renderer_sha256=sha256_file(Path(__file__)),
         helpers_sha256={name: sha256_file(ROOT / "cnn" / name) for name in ("dataset.py", "public_video.py")},
         dataset_sha256=sha256_file(DATA), artifacts=artifacts,
         original_dataset_unchanged=True, model_inference_run=False, labels_changed=False,
         negative_supervision_verified=False, training_started=False, step1_pass=False,
         limits=["No actual human review yet", "60-frame gap is not a verified time duration",
                 "Geometric/source flags are not class-error proof", "Official source metadata does not prove separate rider labels",
                 "VisDrone usage rights remain recorded separately; no redistribution permission inferred"]))
    print(json.dumps(dict(status="prepared_pending_review", count=len(reviews), groups=counts)))


def self_test():
    rows = []
    for scene in ("A", "B", "C"):
        for frame in range(1, 601, 60):
            rows.append(dict(image=f"{scene}/{frame}", scene_id=scene, source_frame=frame,
                 split="train", labels=[0, 1], box_metadata=[dict(category_id=3, truncation=1, occlusion=0),
                                                           dict(category_id=10, truncation=0, occlusion=0)]))
    rows.append({**rows[0], "image": "VAL", "split": "val"})
    chosen = select(rows, count=2)
    assert Counter(group for group, _ in chosen) == {"bicycle": 2, "motorcycle": 2,
                                                  "localization_or_semantic_suspect": 2}
    assert len({row["image"] for _, row in chosen}) == len(chosen)
    assert all(row["split"] == "train" for _, row in chosen)
    for scene in ("A", "B", "C"):
        frames = sorted(row["source_frame"] for _, row in chosen if row["scene_id"] == scene)
        assert all(b-a >= 60 for a, b in zip(frames, frames[1:]))
    assert select(rows, count=2) == chosen
    print("selection self-test passed: no duplicate/val, gap, shortage, deterministic")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    self_test() if args.self_test else build()
