"""Persist bounded CPU checks with source/input hashes; never start real training."""
import argparse
import ast
import json
from pathlib import Path
import subprocess
import shutil
import sys

from .train import sha256


def main():
    root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        default=Path("cnn/reports/ground_distill_20261005/cpu_preflight"))
    args = parser.parse_args()
    folder = (root / args.output).resolve()
    if root not in folder.parents:
        raise ValueError("preflight output must stay inside the project")
    folder.mkdir(parents=True, exist_ok=False)
    modules = ["test_distillation_safety", "test_teacher", "test_training",
               "test_evaluate_teacher", "test_evaluate", "test_metrics", "test_segment_resume"]
    source_names = ["model", "loss", "train", "teacher", "evaluate", "evaluate_teacher",
                    "dataset", "integer", "metrics", "resume_state", "probe_ground_images",
                    "check_ground_preflight"] + modules
    sources = {f"cnn/{name}.py": sha256(root / "cnn" / f"{name}.py") for name in source_names}
    for name in source_names:
        ast.parse((root / "cnn" / f"{name}.py").read_text(encoding="utf-8"), filename=name)
        target = folder / "inputs/cnn" / f"{name}.py"
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(root / "cnn" / f"{name}.py", target)
    checks = []
    for module in modules:
        command = [sys.executable, "-B", "-m", "cnn." + module]
        log = folder / (module + ".log")
        with log.open("x", encoding="utf-8") as stream:
            result = subprocess.run(command, cwd=root, stdout=stream, stderr=subprocess.STDOUT)
        checks.append(dict(command=command, exit_code=result.returncode,
                           log=str(log.relative_to(root)), log_sha256=sha256(log)))
        print(module, result.returncode, flush=True)
    aligned = root / "cnn/reports/ground_distill_20261005"
    student_path = aligned / "coco_val2_student_smoke.json"
    teacher_path = aligned / "coco_val2_teacher_smoke.json"
    student = json.loads(student_path.read_text(encoding="utf-8"))
    teacher = json.loads(teacher_path.read_text(encoding="utf-8"))
    same_inputs = all(student[key] == teacher[key] for key in (
        "dataset_sha256", "evaluated_image_content_sha256", "postprocess_contract", "truth", "ignores"))
    release = root / "cnn/releases/RoadYOLO-S4-512_20261005_fp32_e7"
    manifest = json.loads((release / "release.json").read_text(encoding="utf-8"))
    archive_unchanged = all(sha256(release / name) == value for name, value in manifest["files"].items())
    source_unchanged = all(sha256(root / name) == value for name, value in sources.items())
    passed = all(check["exit_code"] == 0 for check in checks) and same_inputs and archive_unchanged and source_unchanged
    report = dict(status="passed_CPU_preparation_checks" if passed else "failed_CPU_preparation_checks",
                  checks=checks, source_sha256=sources, source_unchanged=source_unchanged,
                  teacher_student_same_subset_GT_ignore_postprocess=same_inputs,
                  same_subset_evidence="2-image COCO integration only, NOT new ground accuracy",
                  archived_files_unchanged=archive_unchanged,
                  release_manifest_sha256=sha256(release / "release.json"),
                  inference_inputs={str(path.relative_to(root)): sha256(path)
                                    for path in (student_path, teacher_path)},
                  actual_ground_probe=str((aligned / "ground_images3_qualitative/report.json").relative_to(root)),
                  actual_ground_probe_sha256=sha256(aligned / "ground_images3_qualitative/report.json"),
                  distillation_training_started=False, formal_acceptance=False,
                  limitation="Synthetic CPU loss/cache/resume checks and real host inference only; no GPU distillation, full new-scene P/R/AP, INT8 parity, or FPGA acceptance.")
    with (folder / "report.json").open("x", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2)
    if not passed:
        raise SystemExit(1)
    print(report["status"], flush=True)


if __name__ == "__main__":
    main()
