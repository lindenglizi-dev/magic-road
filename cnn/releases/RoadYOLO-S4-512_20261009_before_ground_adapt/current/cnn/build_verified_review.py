"""Freeze existing review inputs and prepare AI hints, never verified labels."""
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess
import time

import numpy as np
from PIL import Image, ImageDraw

from .dataset import _refuse_blind, _letterbox_transform, sha256_file
from .teacher import json_hash

ROOT = Path(__file__).resolve().parent.parent
OLD = ROOT / "cnn/reports/strategy_trial_20261006"
OUT = ROOT / "cnn/reports/verified_gt_workflow_20261006"
PLAN = ROOT.parent.parent / "CNN数据审核与继续训练_建议与计划.md"
POLICY = ROOT / "cnn/annotation_policy_v1.md"


def write(path, data):
    with path.open("x", encoding="utf-8") as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2, allow_nan=False)


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def binding(document):
    fields = ("image_id", "source_sha256", "width", "height", "bucket", "split", "original")
    return json_hash(dict(annotation_policy_sha256=document["annotation_policy_sha256"],
                         samples=[{key: row[key] for key in fields} for row in document["samples"]]))


def overlap(first, second):
    a, b = np.asarray(first, dtype=float), np.asarray(second, dtype=float)
    area = np.prod(np.maximum(0, np.minimum(a[2:], b[2:]) - np.maximum(a[:2], b[:2])))
    union = np.prod(np.maximum(0, a[2:]-a[:2])) + np.prod(np.maximum(0, b[2:]-b[:2])) - area
    return float(area / union) if union else 0.0


def geometry(sample):
    warnings = []
    w, h = sample["width"], sample["height"]
    for item in sample["original"]:
        x1, y1, x2, y2 = item["bbox"]
        reason = None
        if not np.isfinite(item["bbox"]).all() or not x1 < x2 or not y1 < y2:
            reason = "invalid_box"
        elif not (0 <= x1 < x2 <= w and 0 <= y1 < y2 <= h):
            reason = "boundary_warning"
        elif min(x2-x1, y2-y1) < 4:
            reason = "small_object_warning"
        elif (x2-x1)*(y2-y1) > .8*w*h:
            reason = "large_region_warning"
        if reason:
            warnings.append(dict(kind=reason, target_id=item["target_id"]))
    for i, first in enumerate(sample["original"]):
        for second in sample["original"][i+1:]:
            if first["class"] != "ignore" and first["class"] == second["class"] and overlap(first["bbox"], second["bbox"]) > .9:
                warnings.append(dict(kind="duplicate_warning", target_id=first["target_id"], other_id=second["target_id"]))
    return warnings


def add_sample(samples, image_id, legacy_id, bucket, split, raw, raw_sha, overlay,
               original, scene_id, camera_id, frame_index, source_metadata):
    _refuse_blind(raw)
    assert sha256_file(raw) == raw_sha, raw
    with Image.open(raw) as image:
        w, h = image.size
    folder = OUT / "images" / image_id
    folder.mkdir(parents=True)
    destination = folder / ("raw" + raw.suffix.lower())
    shutil.copy2(raw, destination)
    assert sha256_file(destination) == raw_sha
    gt = folder / ("source_overlay" + overlay.suffix.lower())
    shutil.copy2(overlay, gt)
    sample = dict(image_id=image_id, legacy_id=legacy_id, bucket=bucket, split=split,
                  width=w, height=h, raw_file=destination.relative_to(OUT).as_posix(),
                  source_sha256=raw_sha, gt_overlay_file=gt.relative_to(OUT).as_posix(),
                  original=original, teacher=[], teacher_status="not_run",
                  source_scene_id=scene_id, camera_id=camera_id, frame_index=frame_index,
                  source_metadata=source_metadata, review_score=0)
    sample["warnings"] = geometry(sample)
    samples.append(sample)


def build():
    if (OUT / "manifest_original.json").exists() or (OUT / "images").exists():
        raise FileExistsError("preserve previous snapshot; no overwrite")
    OUT.mkdir(exist_ok=True)
    snapshot = OUT / "dataset_snapshot_20261006"
    snapshot.mkdir()
    shutil.copy2(POLICY, OUT / "annotation_policy_v1.md")
    inputs = [PLAN, POLICY, OLD / "train_review/review_manifest.json",
              OLD / "ground_review/authoritative_v2/ground_dev_manifest.json",
              OLD / "third_camera_person_review/review_manifest.json"]
    sources = {}
    for index, path in enumerate(inputs):
        _refuse_blind(path)
        target = snapshot / (str(index) + "_" + path.name)
        shutil.copy2(path, target)
        sources[str(path)] = dict(sha256=sha256_file(path), snapshot_file=target.relative_to(OUT).as_posix())
    samples = []
    annotation_sources = {}
    training = read(inputs[2])
    for item in training["samples"]:
        raw = OLD / "train_review" / item["raw_file"]
        annotation = Path(item["source_annotation"])
        _refuse_blind(annotation)
        if str(annotation) not in annotation_sources:
            assert sha256_file(annotation) == item["annotation_sha256"]
            target = snapshot / ("train_source_" + annotation.name)
            shutil.copy2(annotation, target)
            annotation_sources[str(annotation)] = dict(sha256=item["annotation_sha256"], snapshot_file=target.relative_to(OUT).as_posix())
        original = []
        for row in item["source_annotations"]:
            x, y, width, height = row["bbox"]
            category = row["category"]
            label = ("person" if category in (1, 2) else
                     "vehicle" if category in (3, 4, 5, 6, 9, 10) else "ignore")
            if row["score"] <= 0:
                label = "ignore"
            original.append(dict(target_id="o" + str(row["target_id"]), source_target_id=row["target_id"],
                                 source_category=category, **{"class": label}, bbox=[x, y, x+width, y+height]))
        sequence = Path(item["source_image"]).parent.name
        image_id = sequence + "_f" + str(item["source_frame_1based"]).zfill(7)
        add_sample(samples, image_id, item["sample_id"], "train_review", "train", raw,
                   item["source_sha256"], OLD / "train_review" / item["overlay_file"],
                   original, item["scene_id"], "unverified_visdrone_camera_family", item["source_frame_1based"],
                   dict(original_image=item["source_image"], original_annotation=str(annotation),
                        original_annotation_sha256=item["annotation_sha256"], frame_base=1))
    ground = read(inputs[3])
    import csv
    boxes_by_sample = defaultdict(list)
    with (OLD / "ground_review/authoritative_v2/source_box_review.csv").open(encoding="utf-8-sig", newline="") as stream:
        for row in csv.DictReader(stream):
            boxes_by_sample[row["sample_id"]].append(dict(target_id="o"+row["source_object_id"],
                source_target_id=row["source_object_id"], source_category=int(row["original_type"]),
                **{"class": "person" if row["label"] == "ped" else row["label"]},
                bbox=[int(row["xmin"]), int(row["ymin"]), int(row["xmax"])+1, int(row["ymax"])+1]))
    base = OLD / "ground_review/authoritative_v2"
    for item in ground["frames"]:
        add_sample(samples, item["clip_id"] + "_f" + str(item["frame_index"]).zfill(7),
                   item["sample_id"], "road_development", "dev", base/item["raw_frame_path"],
                   item["raw_frame_sha256"], base/item["overlay_path"], boxes_by_sample[item["sample_id"]],
                   item["scene_id"], item["camera_id"], item["frame_index"], dict(frame_base=0, source_manifest=str(inputs[3])))
    courtyard = read(inputs[4])
    clip = courtyard["clip"]
    boxes_by_frame = defaultdict(list)
    for row in courtyard["source_boxes"]:
        boxes_by_frame[row["frame_index"]].append(dict(target_id="o"+str(row["source_object_id"]),
            source_target_id=row["source_object_id"], source_category=row["original_type"],
            **{"class": "person" if row["label"] == "ped" else row["label"]},
            bbox=[row["xmin"], row["ymin"], row["xmax"]+1, row["ymax"]+1]))
    base = OLD / "third_camera_person_review"
    for item in courtyard["frames"]:
        add_sample(samples, clip["clip_id"]+"_f"+str(item["frame_index"]).zfill(7), item["sample_id"],
                   "person_background_aux", "stress", base/item["raw_frame_path"], item["raw_frame_sha256"],
                   base/item["overlay_path"], boxes_by_frame[item["frame_index"]], clip["scene_id"],
                   "virat-010001-courtyard-camera-c", item["frame_index"], dict(frame_base=0, source_manifest=str(inputs[4])))
    assert len(samples) == 276 and len({s["image_id"] for s in samples}) == 276
    for sample in samples:
        ids = [row["target_id"] for row in sample["original"]]
        assert len(ids) == len(set(ids)), sample["image_id"]
    manifest = dict(schema="cnn_review_workbench_v1", annotation_policy_sha256=sha256_file(POLICY),
                    samples=samples, train_required_count=128, verified_gt=False,
                    training_started=False, teacher_status="not_run", human_signed_frames=0,
                    formal_acceptance=False, bucket_counts=dict(Counter(s["bucket"] for s in samples)))
    manifest["dataset_id"] = binding(manifest)
    write(OUT / "manifest_original.json", manifest)
    write(OUT / "review_manifest.json", manifest)
    write(snapshot / "sources.json", dict(inputs=sources, train_annotation_sources=annotation_sources,
          blind_reference_only=dict(scene_ids=["010106", "010108"], contents_accessed=False,
          historical_receipt_reference="evaluation/public_data/virat_ground_v2/blind_reserve_integrity.json")))
    write(OUT / "snapshot_receipt.json", dict(dataset_id=manifest["dataset_id"],
          created_at=datetime.now(timezone.utc).isoformat(), images=len(samples),
          bucket_counts=manifest["bucket_counts"], source_metadata_sha256=sha256_file(snapshot/"sources.json"),
          original_manifest_sha256=sha256_file(OUT/"manifest_original.json"),
          script_sha256=sha256_file(Path(__file__)), blind_contents_accessed=False,
          original_labels_modified=False, training_started=False))
    print(json.dumps(dict(status="snapshot_prepared_not_verified_GT", samples=len(samples), buckets=manifest["bucket_counts"])))


def decode_heads(heads, transform):
    candidates = []
    for label in range(2):
        entries = []
        for head, stride in zip(heads, (4, 8, 16), strict=True):
            raw = head[0].permute(1, 2, 0).cpu().numpy()
            score = 1/(1+np.exp(-np.clip(raw[..., 4], -80, 80))) * 1/(1+np.exp(-np.clip(raw[..., 5+label], -80, 80)))
            ys, xs = np.where(score >= .10)
            for y, x in zip(ys, xs, strict=True):
                center = (raw[y, x, :2]+[x,y])*stride
                size = np.exp(np.clip(raw[y,x,2:4], -4, 3.5))*stride
                box = np.concatenate((center-size/2, center+size/2))
                box = np.clip(box, 0, [512,288,512,288])
                box = [(box[i]*2.5-transform["offset_x" if i%2 == 0 else "offset_y"])/transform["scale_x" if i%2 == 0 else "scale_y"] for i in range(4)]
                box = np.clip(box, 0, [transform["source_width"],transform["source_height"]]*2).tolist()
                if box[2] > box[0] and box[3] > box[1]:
                    entries.append(dict(**{"class": ("person","vehicle")[label]}, bbox=box, score=float(score[y,x])))
        entries.sort(key=lambda item: (-item["score"], item["bbox"]))
        kept = []
        for entry in entries:
            if not any(overlap(entry["bbox"], other["bbox"]) > .6 for other in kept):
                kept.append(entry)
        candidates.extend(kept)
    return candidates


def compare(sample):
    original = [row for row in sample["original"] if row["class"] != "ignore"]
    ignores = [row for row in sample["original"] if row["class"] == "ignore"]
    for index, prediction in enumerate(sample["teacher"]):
        prediction["candidate_id"] = "t"+str(index)
        same = [overlap(prediction["bbox"], row["bbox"]) for row in original if row["class"] == prediction["class"]]
        cross = [overlap(prediction["bbox"], row["bbox"]) for row in original if row["class"] != prediction["class"]]
        prediction["kind"] = ("MATCHED" if max(same, default=0) > .5 else
                              "CHECK_CLASS" if max(cross, default=0) > .5 else
                              "CHECK_BOX" if max(same, default=0) > .2 else "UNMATCHED_PRED")
        prediction["overlaps_ignore"] = any(overlap(prediction["bbox"], row["bbox"]) > .2 for row in ignores)
    for target in original:
        if not any(row["class"] == target["class"] and overlap(row["bbox"], target["bbox"]) > .2 for row in sample["teacher"]):
            sample["warnings"].append(dict(kind="CHECK_GT", target_id=target["target_id"]))
    c = Counter(row["kind"] for row in sample["teacher"])
    g = Counter(row["kind"] for row in sample["warnings"])
    sample["review_score"] = 3*c["UNMATCHED_PRED"]+2*g["boundary_warning"]+2*c["CHECK_CLASS"]+g["small_object_warning"]


def teacher(device):
    import torch
    from .teacher import load_official_model, capture_raw_heads, teacher_input, tree_hash
    manifest = read(OUT/"review_manifest.json")
    assert binding(manifest) == manifest["dataset_id"]
    assets = ROOT / "cnn/teacher_assets"
    receipt = read(assets/"receipt.json")
    source, weights = assets/"source/YOLOX-0.3.0", assets/"yolox_s.pth"
    assert sha256_file(weights) == receipt["weights"]["sha256"]
    assert tree_hash(source/"yolox") == receipt["source_tree_sha256"]
    destination = OUT/"teacher_predictions"
    destination.mkdir(exist_ok=True)
    config = dict(weight_sha256=sha256_file(weights), source_sha256=tree_hash(source/"yolox"),
                  mode="review_hints_not_truth_or_deployment", input="1024x576_FP32_official_BGR_letterbox",
                  confidence=.10, nms_iou=.6, numerical_decoder="floating_adapted_raw_heads_tw_th_clamp_-4_3.5",
                  candidate_cap=None, native_box_coordinates="half_open_XYXY", device=device,
                  dataset_id=manifest["dataset_id"], annotation_policy_sha256=manifest["annotation_policy_sha256"],
                  source_closure_sha256={str(path.relative_to(ROOT)):sha256_file(path) for path in
                    (Path(__file__), ROOT/"cnn/teacher.py", ROOT/"cnn/dataset.py")})
    torch.set_num_threads(2)
    model = load_official_model(source, weights, torch.device(device))
    started = time.perf_counter()
    for index, sample in enumerate(manifest["samples"]):
        path = OUT/sample["raw_file"]
        assert sha256_file(path) == sample["source_sha256"]
        target = destination/(sample["image_id"]+".json")
        if target.exists():
            saved = read(target)
            assert saved["config_sha256"] == json_hash(config) and saved["source_sha256"] == sample["source_sha256"]
            predictions = saved["predictions"]
        else:
            transform = _letterbox_transform(sample["width"], sample["height"])
            row = dict(image_path=path, preprocess=dict(raw_image=True, letterbox_1280x720=transform))
            outputs = capture_raw_heads(model, teacher_input(row, torch.device(device)))
            predictions = decode_heads(outputs, transform)
            write(target, dict(image_id=sample["image_id"], source_sha256=sample["source_sha256"],
                  config_sha256=json_hash(config), predictions=predictions))
        sample["teacher"] = predictions
        sample["teacher_status"] = "hints_only_not_ground_truth"
        compare(sample)
        if (index+1)%16 == 0 or index == 0:
            print("teacher review",index+1,"/",len(manifest["samples"]),"seconds",round(time.perf_counter()-started,1),flush=True)
            if device.startswith("cuda"):
                temperature = subprocess.run(["nvidia-smi", "--query-gpu=temperature.gpu", "--format=csv,noheader,nounits"], capture_output=True,text=True,check=True,timeout=10)
                if max(map(int,temperature.stdout.split())) >= 82:
                    raise RuntimeError("teacher review thermal protection; partial per-image hints preserved")
    manifest["teacher_status"] = "all_hints_prepared_not_verified_GT"
    manifest["teacher_config"] = config
    write(OUT/"review_manifest_teacher.json", manifest)
    write(OUT/"teacher_receipt.json", dict(images=len(manifest["samples"]), config=config,
          total_seconds=time.perf_counter()-started, hint_count=sum(len(row["teacher"]) for row in manifest["samples"]),
          config_sha256=json_hash(config), production_training_started=False, labels_modified=False,
          human_signed_frames=0, artifact_sha256={path.name:sha256_file(path) for path in sorted(destination.glob("*.json"))}))
    print("teacher review complete",flush=True)


def render():
    path = OUT / "review_manifest_teacher.json"
    if not path.exists():
        path = OUT/"review_manifest.json"
    manifest = read(path)
    assert binding(manifest) == manifest["dataset_id"]
    template = (ROOT/"cnn/review_workbench.html").read_text(encoding="utf-8")
    assert template.count("__REVIEW_MANIFEST_JSON__") == 1
    encoded = json.dumps(manifest, ensure_ascii=False, allow_nan=False).replace("<", "\\u003c")
    with (OUT/"index.html").open("x",encoding="utf-8") as stream:
        stream.write(template.replace("__REVIEW_MANIFEST_JSON__", encoded))
    write(OUT/"geometry_warning.json", {sample["image_id"]:sample["warnings"] for sample in manifest["samples"]})
    write(OUT/"review_queue.json", [dict(image_id=sample["image_id"],review_score=sample["review_score"])
          for sample in sorted(manifest["samples"], key=lambda row:(-row["review_score"], row["image_id"]))])
    write(OUT/"review_summary.json", dict(status="pending_human_review", bucket_counts=manifest["bucket_counts"],
          images_reviewed=0, verified_gt=False, training_started=False, teacher_status=manifest["teacher_status"],
          source_label_counts=dict(Counter(row["class"] for sample in manifest["samples"] for row in sample["original"])),
          warning_counts=dict(Counter(row["kind"] for sample in manifest["samples"] for row in sample["warnings"])),
          suggestion_counts=dict(Counter(row["kind"] for sample in manifest["samples"] for row in sample["teacher"]))))
    print("review page rendered",flush=True)


def self_test():
    assert overlap([0,0,10,10],[0,0,10,10]) == 1
    assert overlap([0,0,10,10],[10,0,20,10]) == 0
    sample = dict(width=20,height=20,original=[dict(target_id="o0",**{"class":"person"},bbox=[-1,0,4,8])])
    assert geometry(sample)[0]["kind"] == "boundary_warning"
    sample.update(teacher=[dict(**{"class":"vehicle"},bbox=[-1,0,4,8],score=.2)], warnings=[])
    compare(sample)
    assert sample["teacher"][0]["kind"] == "CHECK_CLASS"
    assert sample["warnings"][0]["kind"] == "CHECK_GT"
    doc = dict(annotation_policy_sha256="policy",samples=[dict(image_id="x",source_sha256="a",width=20,height=20,bucket="train_review",split="train",original=[])])
    before = binding(doc)
    doc["samples"][0]["teacher"] = [{"bbox":[0,0,1,1]}]
    assert binding(doc) == before
    doc["samples"][0]["split"] = "dev"
    assert binding(doc) != before
    print("review geometry, matching and original-source binding PASS")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action",choices=["build","teacher","render","self-test"])
    parser.add_argument("--device",default="cpu")
    args = parser.parse_args()
    {"build":build,"teacher":lambda:teacher(args.device),"render":render,"self-test":self_test}[args.action]()
