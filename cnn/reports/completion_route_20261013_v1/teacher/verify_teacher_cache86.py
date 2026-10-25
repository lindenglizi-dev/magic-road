"""Verify 86-item cache structure and source binding without re-inference."""
import hashlib
import json
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parents[4]
CACHE = Path(__file__).with_name("teacher_train86.pt")
DATASET = ROOT / "cnn/reports/ac_optimization_20261013_v1/trial/dataset.json"
OUT = Path(__file__).with_name("teacher_train86_receipt.json")


def sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


payload = torch.load(CACHE, map_location="cpu", weights_only=True)
manifest = json.loads(DATASET.read_text(encoding="utf-8"))
expected = {str(row.get("teacher_key", row["image"])).replace("\\", "/")
            for row in manifest["images"] if row["split"] == "train"}
items = payload["items"]
shapes = ((7, 72, 128), (7, 36, 64), (7, 18, 32))
assert len(expected) == len(items) == payload["item_count"] == 86
assert set(items) == expected
assert payload["dataset_sha256"] == sha(DATASET)
for item in items.values():
    assert set(item) == {"heads"}
    assert tuple(tuple(head.shape) for head in item["heads"]) == shapes
    assert all(head.dtype == torch.float16 and torch.isfinite(head).all() for head in item["heads"])
receipt = {
    "status": "passed_structure_coverage_and_source_binding",
    "cache_sha256": sha(CACHE), "cache_bytes": CACHE.stat().st_size,
    "split": "train", "item_count": 86, "expected_item_count": 86,
    "key_coverage": "86/86 exact manifest train teacher_key set",
    "head_shapes_chw": shapes, "storage_dtype": "float16", "all_values_finite": True,
    "dataset_sha256": payload["dataset_sha256"],
    "dataset_content_sha256": payload["dataset_content_sha256"],
    "student_architecture_hash": payload["student_architecture_hash"],
    "teacher_weight_sha256": payload["teacher_weight_sha256"],
    "teacher_source_sha256": payload["teacher_source_sha256"],
    "teacher_preprocess_sha256": payload["teacher_preprocess_sha256"],
    "ground_truth_policy": payload["ground_truth_policy"],
    "verification_boundary": "loaded every cached tensor and checked keys/shapes/dtype/finiteness/binding metadata; did not rerun teacher or numerically compare cached heads",
}
OUT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
print(json.dumps(receipt))
