"""Bind the teacher/E7/replay-G10 comparison to the same 17 GT images."""
import hashlib
import json
from pathlib import Path

from cnn.metrics import report

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).with_name("comparison17.json")
INPUTS = {
    "teacher": Path(__file__).with_name("teacher_development17.json"),
    "replay_g10": ROOT / "cnn/reports/ac_optimization_20261013_v1/trial/development17.json",
    "e7": ROOT / "cnn/reports/ac_bnfreeze_g10_20261013_v1/e7_control17.json",
}
DATASET = ROOT / "cnn/reports/ac_g10_20261013_v1/dataset.json"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    models = {name: json.loads(path.read_text(encoding="utf-8"))
              for name, path in INPUTS.items()}
    reference = models["teacher"]
    for name, value in models.items():
        assert value["image_count"] == 17, name
        assert value["dataset_sha256"] == reference["dataset_sha256"], name
        assert value["evaluated_image_content_sha256"] == reference["evaluated_image_content_sha256"], name
        assert value["truth"] == reference["truth"], name
        assert value["ignores"] == reference["ignores"], name
    dataset = json.loads(DATASET.read_text(encoding="utf-8"))
    rows = [row for row in dataset["images"] if row["split"] == "val"]
    cameras = {}
    for row in rows:
        cameras.setdefault(row["camera_id"], []).append(row["image"])
    grouped = {}
    for camera, image_ids in sorted(cameras.items()):
        keep = set(image_ids)
        grouped[camera] = {"image_count": len(keep), "gt": {
            name: sum(row["label"] == label and row["image_id"] in keep
                      for row in reference["truth"])
            for label, name in enumerate(("person", "vehicle"))}, "models": {}}
        for name, value in models.items():
            pick = lambda key: [row for row in value[key] if row["image_id"] in keep]
            grouped[camera]["models"][name] = report(
                pick("predictions"), pick("truth"), pick("ignores"), thresholds=(.5, .5))
    overall = {name: value["diagnostic_metrics_at_0_5"] for name, value in models.items()}
    deltas = {}
    for student in ("replay_g10", "e7"):
        deltas[student] = {cls: {metric: overall["teacher"]["classes"][cls][metric]
                                       - overall[student]["classes"][cls][metric]
                                for metric in ("precision", "recall", "ap50", "ap50_95")}
                           for cls in ("person", "vehicle")}
    closure = [ROOT / path for path in ("cnn/evaluate_teacher.py", "cnn/teacher.py",
               "cnn/metrics.py", "cnn/integer.py", "cnn/dataset.py", "cnn/evaluate.py", "cnn/train.py")]
    result = {
        "status": "same_original_images_same_gt_verified",
        "strict_input_equality": False,
        "input_difference": "teacher BGR FP32 1024x576; students RGB minus128 FP32 512x288",
        "dataset_sha256": sha(DATASET),
        "evaluated_image_content_sha256": reference["evaluated_image_content_sha256"],
        "input_reports": {name: {"path": str(path), "sha256": sha(path)} for name, path in INPUTS.items()},
        "source_closure": {str(path.relative_to(ROOT)).replace("\\", "/"): sha(path) for path in closure},
        "overall_at_score_0_5": overall,
        "teacher_minus_student": deltas,
        "camera_groups": grouped,
        "ground_truth_policy": "manifest human GT is authoritative; teacher predictions are not labels",
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
