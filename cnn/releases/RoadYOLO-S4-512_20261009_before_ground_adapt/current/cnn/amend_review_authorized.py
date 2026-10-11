"""Apply only the five review corrections explicitly approved by the user."""
import argparse
import copy
from pathlib import Path

from .dataset import sha256_file
from .import_verified_review import import_review
from .prepare_verified_train import PACKAGE, VERIFIED, ROOT, main as preflight, read, write


OUT = ROOT / "cnn/reports/verified_gt_amendment_20261007"
PARENT_HASH = "a8f25b4beea6394572ac0bfeea594a5ea8150383789508b92c4aebf8c513791c"
RESTORE_IGNORE = (("train_011", "o104"), ("train_011", "o105"),
                  ("train_046", "o104"), ("train_077", "o79"))


def amend(parent, original):
    result = copy.deepcopy(parent)
    samples = {sample["legacy_id"]:sample for sample in original["samples"]}
    reviews = {review["image_id"]:review for review in result["reviews"]}
    changes = []
    for legacy_id, target_id in RESTORE_IGNORE:
        sample = samples[legacy_id]
        source = next(item for item in sample["original"] if item["target_id"] == target_id)
        review = reviews[sample["image_id"]]
        action = next(item for item in review["actions"] if item["target_id"] == target_id)
        if not (source["class"] == "ignore" and action["action"] == "M" and action["class"] == "person"):
            raise ValueError("approved correction no longer matches its parent")
        replacement = dict(target_id=target_id, action="A", **{"class":"ignore"},
                           bbox=source["bbox"].copy(), reason="用户授权恢复原始ignore，群体不是单个person",
                           ai_assisted=False)
        changes.append(dict(legacy_id=legacy_id, image_id=sample["image_id"],
                            before=copy.deepcopy(action), after=replacement))
        review["actions"][review["actions"].index(action)] = replacement
    sample = samples["train_005"]
    review = reviews[sample["image_id"]]
    keep = next(item for item in review["actions"] if item["target_id"] == "manual_004")
    remove = next(item for item in review["actions"] if item["target_id"] == "manual_007")
    if not (keep["action"] == remove["action"] == "N" and keep["class"] == remove["class"] == "person"
            and keep["bbox"] == remove["bbox"]):
        raise ValueError("approved exact duplicate no longer matches its parent")
    review["actions"].remove(remove)
    changes.append(dict(legacy_id="train_005", image_id=sample["image_id"],
                        before=remove, after=None, kept_target_id="manual_004"))
    result["authorized_amendment"] = dict(
        kind="assistant_applied_user_approved_corrections_not_new_manual_review",
        approval_date_local="2026-10-07", approval_reply="好",
        approval_scope="restore four original ignore boxes; remove one exact duplicate; leave train_075 unchanged",
        parent_patch_sha256=PARENT_HASH, changes=changes,
        complete_flags_and_reviewer_inherited_from_parent=True)
    return result, changes


def check(parent, corrected, original):
    samples = {sample["legacy_id"]:sample for sample in original["samples"]}
    parents = {review["image_id"]:review for review in parent["reviews"]}
    reviews = {review["image_id"]:review for review in corrected["reviews"]}
    expected = {samples[key]["image_id"] for key in ("train_005", "train_011", "train_046", "train_077")}
    assert {key for key in reviews if reviews[key] != parents[key]} == expected
    assert reviews[samples["train_075"]["image_id"]] == parents[samples["train_075"]["image_id"]]
    for legacy_id, target_id in RESTORE_IGNORE:
        source = next(item for item in samples[legacy_id]["original"] if item["target_id"] == target_id)
        action = next(item for item in reviews[samples[legacy_id]["image_id"]]["actions"] if item["target_id"] == target_id)
        assert action["action"] == "A" and action["class"] == "ignore" and action["bbox"] == source["bbox"]
    for key in reviews:
        before, after = parents[key], reviews[key]
        assert all(before[field] == after[field] for field in before if field != "actions")
        before_actions = {item["target_id"]:item for item in before["actions"]}
        after_actions = {item["target_id"]:item for item in after["actions"]}
        authorized_ids = {target for legacy, target in RESTORE_IGNORE if samples[legacy]["image_id"] == key}
        if key == samples["train_005"]["image_id"]:
            authorized_ids.add("manual_007")
        assert {target for target in before_actions if before_actions[target] != after_actions.get(target)} == authorized_ids
        assert not (after_actions.keys() - before_actions.keys())


def main(self_test=False):
    parent_path = VERIFIED / "review_patch.json"
    assert sha256_file(parent_path) == PARENT_HASH
    parent = read(parent_path)
    original = read(PACKAGE / "manifest_original.json")
    corrected, changes = amend(parent, original)
    check(parent, corrected, original)
    invalid = copy.deepcopy(parent)
    duplicate_image = next(sample["image_id"] for sample in original["samples"] if sample["legacy_id"] == "train_005")
    record = next(row for row in invalid["reviews"] if row["image_id"] == duplicate_image)
    next(item for item in record["actions"] if item["target_id"] == "manual_007")["bbox"][0] += 1
    try:
        amend(invalid, original)
    except ValueError:
        pass
    else:
        raise AssertionError("non-exact duplicate must not be auto-removed")
    if self_test:
        print("PASS: exactly five authorized corrections, other actions and review signatures preserved; near duplicate untouched; changed duplicate rejected")
        return
    OUT.mkdir(exist_ok=False)
    patch_path = OUT / "review_patch_user_authorized.json"
    write(patch_path, corrected)
    import_result = import_review(PACKAGE / "review_manifest_teacher.json", patch_path, OUT / "verified_labels")
    preflight(OUT / "verified_labels", OUT / "CPU_preflight")
    hints = read(OUT / "CPU_preflight/duplicate_hints.json")
    assert len(hints) == 1 and hints[0]["legacy_id"] == "train_075" and hints[0]["iou"] < 1
    assert sha256_file(parent_path) == PARENT_HASH
    write(OUT / "amendment_receipt.json", dict(status="authorized_corrections_applied_CPU_preflight_passed", changes=changes,
          original_manual_file_preserved=True, parent_patch_sha256=PARENT_HASH,
          user_authorization=corrected["authorized_amendment"],
          remaining_overlap_hint=hints, validation_frames_pending=124, stress_frames_pending=24,
          production_training_started=False, formal_acceptance=False,
          source_sha256={name:sha256_file(ROOT/"cnn"/name) for name in ("amend_review_authorized.py", "prepare_verified_train.py")},
          outputs_sha256={str(path.relative_to(OUT)):sha256_file(path) for path in OUT.rglob("*") if path.is_file()},
          import_stats=import_result["stats"]))
    print("authorized corrections frozen separately; CPU checks passed; no training started")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    main(parser.parse_args().self_test)
