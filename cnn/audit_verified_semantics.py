"""Flag review semantics for human correction; never rewrite signed labels."""
import html
import json
from pathlib import Path

from .dataset import sha256_file
from .prepare_verified_train import OUT, PACKAGE, VERIFIED, read, write


def main():
    manifest = read(PACKAGE / "manifest_original.json")
    verified = read(VERIFIED / "labels_verified.json")
    patch = read(VERIFIED / "review_patch.json")
    originals = {sample["image_id"]: sample for sample in manifest["samples"]}
    issues = []
    corrections = []
    for review in patch["reviews"]:
        sample = originals[review["image_id"]]
        by_id = {item["target_id"]:item for item in sample["original"]}
        for action in review["actions"]:
            if action["action"] != "A":
                corrections.append(dict(image_id=sample["image_id"], legacy_id=sample["legacy_id"],
                                        **action, original=by_id.get(action["target_id"])))
            original = by_id.get(action["target_id"])
            if original and original["class"] == "ignore" and action["class"] == "person" and action["action"] == "M":
                issues.append(dict(image_id=sample["image_id"], legacy_id=sample["legacy_id"],
                                   target_ids=[action["target_id"]], bbox=action["bbox"],
                                   severity="requires_semantic_confirmation_before_training",
                                   reason=action["reason"], issue="ignore_region_promoted_to_single_person",
                                   instruction="如该框包含多人/多车，不可作为一个person；选择此来源框点A恢复原ignore，明确单人用独立N框，未核清区域继续ignore。"))
    duplicates = read(OUT / "duplicate_hints.json")
    for duplicate in duplicates:
        image = next(image for image in verified["images"] if image["image_id"] == duplicate["image_id"])
        labels = {item["target_id"]: item for item in image["labels"]}
        issues.append(dict(image_id=image["image_id"], legacy_id=image["legacy_id"],
                           target_ids=[duplicate["first"], duplicate["second"]],
                           bbox=labels[duplicate["first"]]["bbox"], iou=duplicate["iou"],
                           severity="exact_duplicate_requires_correction" if duplicate["iou"] == 1 else "overlap_hint_needs_visual_check",
                           issue="same_class_duplicate_hint",
                           instruction="新增manual框重复：在本图决策里撤销其中一次N；来源框若同一目标则保留一个、D删除另一个；若是遮挡的两个人则保留。"))
    document = dict(status="stopped_before_training_semantic_review_required", issues=issues,
                    issues_are_not_automatic_label_changes=True, production_training_started=False,
                    CPU_preflight_pass_does_not_validate_label_semantics=True,
                    staged_train_manifest_training_eligible=False, validation_frames_pending=124,
                    stress_frames_pending=24, formal_acceptance=False,
                    verified_labels_sha256=sha256_file(VERIFIED / "labels_verified.json"),
                    frozen_patch_sha256=sha256_file(VERIFIED / "review_patch.json"),
                    source_sha256=sha256_file(Path(__file__)))
    write(OUT / "semantic_review_required.json", document)
    write(OUT / "all_non_A_actions.json", corrections)
    cards = []
    for issue in issues:
        sample = originals[issue["image_id"]]
        image = (PACKAGE / sample["raw_file"]).as_uri()
        x1,y1,x2,y2 = issue["bbox"]
        svg = (f'<svg viewBox="0 0 {sample["width"]} {sample["height"]}" style="width:100%;background:#222">'
               f'<image href="{html.escape(image, quote=True)}" width="{sample["width"]}" height="{sample["height"]}"/>'
               f'<rect x="{x1}" y="{y1}" width="{x2-x1}" height="{y2-y1}" fill="none" stroke="red" stroke-width="5"/></svg>')
        cards.append(f'<section><h2>{html.escape(issue["legacy_id"])} — {html.escape(", ".join(issue["target_ids"]))}</h2>'
                     f'<p>{html.escape(issue["instruction"])}</p><p>{html.escape(issue.get("reason", ""))}</p>{svg}</section>')
    page = ('<!doctype html><html lang="zh"><meta charset="utf-8"><title>只需复核这5张图</title>'
            '<style>body{font:18px sans-serif;max-width:1400px;margin:24px auto}section{margin:32px 0;border-top:2px solid #888}</style>'
            '<h1>定向复核：不是重审128张</h1><p>此页只展示疑点，不修改标签。请在原审核台导入最新草稿，按图号修改并重新签署，然后导出。</p>'
            + ''.join(cards) + '</html>')
    with (OUT / "targeted_review.html").open("x", encoding="utf-8") as stream:
        stream.write(page)
    print(f'semantic review required: {len(issues)} issues, {len({item["image_id"] for item in issues})} images; no label changes')


if __name__ == "__main__":
    main()
