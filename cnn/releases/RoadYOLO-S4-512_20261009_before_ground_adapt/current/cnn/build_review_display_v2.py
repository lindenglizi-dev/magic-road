"""Create a display-only revision without replacing the frozen review package."""
import json
from pathlib import Path
from .dataset import sha256_file


def main():
    root = Path(__file__).resolve().parent
    package = root / "reports/verified_gt_workflow_20261006"
    source = package / "review_manifest_teacher.json"
    template = root / "review_workbench.html"
    page = package / "index_display_v2.html"
    text = template.read_text(encoding="utf-8")
    assert text.count("__REVIEW_MANIFEST_JSON__") == 1
    manifest = json.loads(source.read_text(encoding="utf-8"))
    frozen_manifest = sha256_file(source)
    with page.open("x", encoding="utf-8") as stream:
        stream.write(text.replace("__REVIEW_MANIFEST_JSON__", json.dumps(manifest, ensure_ascii=False).replace("<", "\\u003c")))
    assert sha256_file(source) == frozen_manifest
    with (package / "display_v2_receipt.json").open("x", encoding="utf-8") as stream:
        json.dump(dict(change="display_only_selected_teacher_and_selected_labels", dataset_id=manifest["dataset_id"],
                       predictions_changed=False, labels_changed=False, training_started=False,
                       original_package_sha256=sha256_file(package / "package_receipt.json"),
                       source_sha256={p.name: sha256_file(p) for p in (source, template, Path(__file__), root / "test_review_workbench_ui.py")},
                       output_sha256=sha256_file(page), browser_smoke="not_run_file_URL_blocked"), stream, ensure_ascii=False, indent=2)
    print("display v2 generated; frozen manifests and original page preserved")


if __name__ == "__main__":
    main()
