"""Hash prepared review artifacts without signing ground truth or starting training."""
import json
from pathlib import Path
import shutil
from .dataset import sha256_file


def main():
    root = Path(__file__).resolve().parent.parent
    package = root / "cnn/reports/verified_gt_workflow_20261006"
    code = package / "execution_sources"
    code.mkdir(exist_ok=False)
    for name in ("build_verified_review.py", "review_workbench.html", "import_verified_review.py",
                 "test_verified_review.py", "test_review_workbench_ui.py", "test_review_geometry.py",
                 "seal_review_package.py", "teacher.py", "dataset.py"):
        shutil.copyfile(root / "cnn" / name, code / name)
    snapshot = json.loads((package / "snapshot_receipt.json").read_text(encoding="utf-8"))
    current = sha256_file(code / "build_verified_review.py")
    receipt = dict(status="prepared_pending_human_review", verified_gt=False, training_started=False,
                   browser_smoke="blocked_by_file_URL_security_policy_not_run",
                   snapshot_builder_sha256=snapshot["script_sha256"], current_builder_sha256=current,
                   historical_builder_source_available=False,
                   historical_builder_note="Builder changed after snapshot; historical hash retained, old source not archived. Current code is not claimed to reproduce original snapshot byte-for-byte.",
                   artifact_sha256={str(path.relative_to(package)).replace("\\", "/"): sha256_file(path)
                                    for path in sorted(package.rglob("*")) if path.is_file()})
    with (package / "package_receipt.json").open("x", encoding="utf-8") as stream:
        json.dump(receipt, stream, ensure_ascii=False, indent=2)
    assert receipt["artifact_sha256"]["manifest_original.json"] == snapshot["original_manifest_sha256"]
    print("prepared review package sealed; no verified labels or training")


if __name__ == "__main__":
    main()
