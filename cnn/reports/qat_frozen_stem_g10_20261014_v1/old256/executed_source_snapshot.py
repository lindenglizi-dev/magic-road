"""Read-only CPU old256 regression for initial maxabs PTQ and frozen-Stem QAT."""
import json
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import torch

from cnn.evaluate import load_validation_subset
from cnn.integer import postprocess
from cnn.metrics import report
from cnn.train import FullFrameDataset, dataset_content_hash, sha256
from cnn.hw_validation.production.evaluate_qat import PROJECT, SOURCE, SOURCE_PACKAGE, _delta, read
from cnn.hw_validation.production.run_trained_integer import CHECKPOINT_HASH, centered, save
from cnn.hw_validation.production.trained_integer import load_package

NEW = PROJECT / "cnn/reports/qat_frozen_stem_g10_20261014_v1"
DATA = PROJECT / "cnn/data/visdrone_vid_train/raw_manifest/dataset.json"
FP32 = PROJECT / "cnn/reports/ac_optimization_20261013_v1/trial/old256.json"
OUTPUT = NEW / "old256"
DATA_HASH = "ad353c5bce5b0ecef0433c74515324bbfdb031e92aff964cd56c18ae069d9fe4"
CONTENT_HASH = "8858a1ac3ad9d5428a6004e005eba2a1f95513b82512ae8928c2b4c21e631473"
FP32_HASH = "76dde10ebf817fc790b28983255bdf1197939fffbdbe3d25f31ba763de5cf357"


def predictions(heads, image_id, contract):
    rows = postprocess(heads, (contract["score_floor_uint16"],) * 2,
                       contract["top_k_per_class"], contract["max_boxes_per_class"])
    return [{"image_id": image_id, "label": row["label"],
             "box": [value / 256 for value in row["box_q8"]],
             "score": row["score_uint16"] / 65536} for row in rows]


def main():
    if OUTPUT.exists():
        raise FileExistsError(OUTPUT)
    torch.set_num_threads(2)
    torch.set_num_interop_threads(2)
    paths = {
        "dataset": DATA, "FP32_old256": FP32,
        "initial_PTQ_report": SOURCE / "development17.json",
        "initial_PTQ_manifest": SOURCE_PACKAGE / "manifest.json",
        "frozen_manifest": NEW / "package/manifest.json",
        "frozen_development17": NEW / "evaluation/development17.json",
        "frozen_restoration_gate": NEW / "evaluation/evaluation_gate.json",
        "frozen_execution": NEW / "execution/report.json",
        "control_comparison": NEW / "control_comparison.json",
    }
    if sha256(DATA) != DATA_HASH or sha256(FP32) != FP32_HASH:
        raise ValueError("old256 dataset or FP32 baseline changed")
    frozen17, gate = read(paths["frozen_development17"]), read(paths["frozen_restoration_gate"])
    execution, comparison = read(paths["frozen_execution"]), read(paths["control_comparison"])
    if (gate.get("restoration_passed") is not True
            or gate.get("old256_continuation_eligible") is not True
            or gate.get("formal_acceptance") is not False
            or not all(gate.get("required_gates", {}).values())
            or execution.get("status") != "completed_frozen_stem_qat_G10"
            or execution.get("sources_unchanged") is not True
            or execution.get("original_checkpoint_unchanged") is not True
            or execution.get("formal_acceptance") is not False
            or frozen17.get("formal_acceptance") is not False
            or frozen17.get("acceptance_eligible") is not False
            or execution.get("checkpoint_sha256") != frozen17["input_hashes"]["checkpoint_sha256"]):
        raise ValueError("frozen-Stem same17 restoration/source/checkpoint gate is not valid")
    for key, path in (("new_evaluation", paths["frozen_development17"]),
                      ("new_evaluation_gate", paths["frozen_restoration_gate"]),
                      ("new_execution", paths["frozen_execution"])):
        if comparison["input_sha256"].get(key) != sha256(path):
            raise ValueError(f"control comparison no longer binds {key}")
    for closure in (frozen17["training_identity"]["source_sha256"], frozen17["source_sha256"]):
        if any(sha256(PROJECT / name) != digest for name, digest in closure.items()):
            raise ValueError("frozen training or evaluation source changed")

    initial, initial_manifest = load_package(SOURCE_PACKAGE)
    frozen, frozen_manifest = load_package(NEW / "package")
    initial17 = read(paths["initial_PTQ_report"])
    if (initial17["package_identity"]["manifest_sha256"] != sha256(paths["initial_PTQ_manifest"])
            or initial17["package_identity"]["payload_sha256"] != initial_manifest["payload_sha256"]
            or initial17["package_identity"]["physical_sha256"] != initial_manifest["physical_sha256"]
            or frozen17["input_hashes"]["candidate_manifest_sha256"] != sha256(paths["frozen_manifest"])
            or frozen17["input_hashes"]["candidate_payload_sha256"] != frozen_manifest["payload_sha256"]
            or frozen17["input_hashes"]["candidate_physical_sha256"] != frozen_manifest["physical_sha256"]
            or frozen_manifest["provenance"]["checkpoint_sha256"] != execution["checkpoint_sha256"]):
        raise ValueError("initial or frozen package binding differs")

    baseline = read(FP32)
    contract = baseline["postprocess_contract"]
    if (baseline.get("checkpoint_sha256") != CHECKPOINT_HASH
            or baseline.get("dataset_sha256") != DATA_HASH
            or baseline.get("evaluated_image_content_sha256") != CONTENT_HASH
            or baseline.get("image_count") != 256 or baseline.get("total_validation_images") != 5151):
        raise ValueError("FP32 old256 identity differs")
    rows, total = load_validation_subset(DATA, None, 256)
    dataset = FullFrameDataset(rows, "val")
    if total != 5151 or dataset_content_hash(dataset.rows) != CONTENT_HASH:
        raise ValueError("selected old256 image content differs")

    OUTPUT.mkdir(parents=True, exist_ok=False)
    started = time.perf_counter()
    predicted = {"initial_maxabs_PTQ": [], "frozen_stem_QAT": []}
    truth, ignores, timings = [], [], []
    with ThreadPoolExecutor(max_workers=2) as pool:
        for index, row in enumerate(dataset.rows):
            image, _, _ = dataset[index]
            pixels = centered(image)
            stage = time.perf_counter()
            jobs = {name: pool.submit(model.forward, pixels) for name, model in
                    (("initial_maxabs_PTQ", initial), ("frozen_stem_QAT", frozen))}
            for name, job in jobs.items():
                heads, _, _ = job.result()
                predicted[name].extend(predictions(heads, row["image"], contract))
            timings.append(time.perf_counter() - stage)
            truth.extend({"image_id": row["image"], "label": label, "box": box}
                         for label, box in zip(row["labels"], row["boxes"], strict=True))
            metadata = row.get("ignore_metadata",
                               [{"label": -1, "crowd": False}] * len(row["ignore_boxes"]))
            ignores.extend({"image_id": row["image"], "label": region["label"], "box": box,
                            "crowd": region["crowd"]}
                           for box, region in zip(row["ignore_boxes"], metadata, strict=True))
            if (index + 1) % 16 == 0:
                print(f"paired integer old256 {index + 1}/256", flush=True)
    if truth != baseline["truth"] or ignores != baseline["ignores"]:
        raise ValueError("old256 GT or ignore protocol changed")
    metrics = {name: report(rows, truth, ignores, thresholds=(.5, .5))
               for name, rows in predicted.items()}
    fp32 = baseline["diagnostic_metrics_at_0_5"]
    delta_initial = _delta(metrics["initial_maxabs_PTQ"], fp32)
    delta_frozen = _delta(metrics["frozen_stem_QAT"], fp32)
    delta_control = _delta(metrics["frozen_stem_QAT"], metrics["initial_maxabs_PTQ"])
    class_pass = {name: delta_control[name]["ap50"] >= -1. for name in ("person", "vehicle")}
    hashes = {name: sha256(path) for name, path in paths.items()}
    save(OUTPUT / "development256.json", {
        "status": "QAT_FROZEN_STEM_OLD256_REGRESSION_DIAGNOSTIC",
        "image_count": 256, "total_validation_images": total,
        "dataset_sha256": DATA_HASH, "evaluated_image_content_sha256": CONTENT_HASH,
        "postprocess_contract": contract, "metrics_at_score_0_5": dict(metrics, FP32=fp32),
        "delta_pp_vs_FP32": {"initial_maxabs_PTQ": delta_initial, "frozen_stem_QAT": delta_frozen},
        "delta_pp_frozen_stem_vs_initial_maxabs_PTQ": delta_control,
        "predictions": predicted, "truth": truth, "ignores": ignores,
        "paired_cpu_forward_seconds": timings, "input_sha256": hashes,
        "source_sha256": sha256(Path(__file__)), "acceptance_eligible": False,
        "formal_acceptance": False,
        "limitation": "fixed old256 development regression; not independent or formal acceptance",
    })
    save(OUTPUT / "evaluation_gate.json", {
        "status": "PASS_OLD256_REGRESSION" if all(class_pass.values()) else "FAIL_OLD256_REGRESSION",
        "criterion": "each_class_AP50_delta_vs_initial_maxabs_PTQ_at_least_minus_1pp",
        "class_pass": class_pass, "observed_delta_pp": delta_control,
        "FP32_quantization_gap_pp": {"initial_maxabs_PTQ": delta_initial,
                                      "frozen_stem_QAT": delta_frozen},
        "passed": all(class_pass.values()), "FP32_reference_is_not_acceptance": True,
        "formal_acceptance": False,
    })
    save(OUTPUT / "status.json", {
        "status": "completed_paired_old256_CPU_evaluation", "cpu_only": True,
        "cuda_initialized": torch.cuda.is_initialized(), "training_started": False,
        "image_count": 256, "paired_models": 2, "seconds": time.perf_counter() - started,
        "old256_regression_passed": all(class_pass.values()), "formal_acceptance": False,
    })
    print(json.dumps({"metrics": metrics, "delta_pp_frozen_vs_initial": delta_control,
                      "old256_regression_passed": all(class_pass.values())}), flush=True)


if __name__ == "__main__":
    main()
