"""CPU-only checks for deterministic ground48 selection and fail-closed export."""

from __future__ import annotations

from collections import Counter, defaultdict
from copy import deepcopy
import json
from pathlib import Path
import re
import subprocess
import tempfile

from .import_verified_review import CHECKS, ReviewError
from .prepare_ground48 import (CAMERA_A, CAMERA_B, OUTPUT, SOURCE, blank_patch,
                               dataset_id, even_positions, export_documents,
                               read_json, render_workbench, select_samples, validate_ground_manifest)


def main() -> None:
    assert even_positions(24) == [0, 5, 9, 14, 18, 23]
    assert even_positions(28) == [0, 5, 11, 16, 22, 27]
    original = read_json(SOURCE / "manifest_original.json")
    teacher = read_json(SOURCE / "review_manifest_teacher.json")
    selected_original, selected_teacher = select_samples(original, teacher)
    assert [row["image_id"] for row in selected_teacher] == [row["image_id"] for row in select_samples(original, teacher)[1]]
    assert len(selected_teacher) == 48
    assert Counter(row["camera_id"] for row in selected_teacher) == Counter({CAMERA_A: 24, CAMERA_B: 24})
    camera_a_clips: dict[str, list[int]] = defaultdict(list)
    for row in selected_teacher:
        if row["camera_id"] == CAMERA_A:
            camera_a_clips[row["selection_clip_id"]].append(row["frame_index"])
    assert len(camera_a_clips) == 4 and all(len(rows) == 6 for rows in camera_a_clips.values())
    for batch in range(1, 5):
        rows = [row for row in selected_teacher if row["review_batch"] == batch]
        assert len(rows) == 12
        assert Counter(row["camera_id"] for row in rows) == Counter({CAMERA_A: 6, CAMERA_B: 6})
    assert all(not row.get("manual_review") for row in selected_original)

    manifest, samples = validate_ground_manifest(OUTPUT / "review_manifest_teacher.json")
    assert len(samples) == 48 and manifest["dataset_id"] == dataset_id(manifest)
    html = (OUTPUT / "index.html").read_text(encoding="utf-8")
    template = Path(__file__).with_name("review_workbench.html").read_text(encoding="utf-8")
    assert html == render_workbench(template, manifest), "live page differs from generator"
    assert 'id="rawSeen"' not in html and 'id="checks"' not in html
    assert '[data-check]' not in html and '$("rawSeen")' not in html
    scripts = dict(re.findall(r'<script id="([^"]+)"(?: type="[^"]+")?>(.*?)</script>', html, re.S))
    assert {"review-manifest", "core", "app-script"} <= scripts.keys()
    syntax = subprocess.run(
        ["node", "--check", "-"], input=scripts["core"] + "\n" + scripts["app-script"],
        text=True, encoding="utf-8", capture_output=True, check=False,
    )
    assert syntax.returncode == 0, syntax.stderr
    node_checks = r'''
const assert = require("node:assert/strict");
const C = globalThis.WorkbenchCore;
assert.deepEqual(C.validateManifest(actual), []);
assert.equal(actual.samples.length, 48);
for (let batch = 1; batch <= 4; batch++) {
  const rows = actual.samples.filter(row => row.review_batch === batch);
  assert.equal(rows.length, 12);
  assert.equal(rows.filter(row => row.camera_id === "virat-parking-lot-camera-a").length, 6);
  assert.equal(rows.filter(row => row.camera_id === "virat-010107-camera-b").length, 6);
}
const sample = actual.samples.find(row => row.original.length);
const unsigned = {reviewer:"", reviewed_at_utc:"", raw_seen:false, complete:false,
  checks:Object.fromEntries(C.checks.map(key => [key,false])), actions:[], notes:""};
const errors = C.completionErrors(sample, unsigned).join("|");
assert.match(errors, /RAW/);
assert.match(errors, /审核人/);
assert.match(errors, /六项/);
assert.match(errors, /来源框未决策/);
console.log("ground48 generated workbench: manifest valid, unsigned rejected, 4 batches x 12 with 6A/6B");
'''
    # Exercise the actual signing handler: only an explicit valid signature
    # fills legacy attestation fields; failure must not alter the draft.
    sign_handler = re.search(r'\$\("sign"\)\.addEventListener\("click", \(\) => \{(.*?)\n  \}\);',
                             scripts["app-script"], re.S)
    assert sign_handler
    node_checks += r'''
let record = {...unsigned, checks:{...unsigned.checks}, actions:[]};
const Core = C;
const review = () => record;
const alerts = [];
const alert = message => alerts.push(message);
const renderComplete = () => {};
const renderProgress = () => {};
const signSample = () => sample;
const sign = () => {
''' + sign_handler.group(1).replace("sample()", "signSample()") + r'''
};
const before = JSON.stringify(record);
sign();
assert.equal(JSON.stringify(record), before);
assert.equal(alerts.length, 1);
record.reviewer = "fixture-human";
record.actions = sample.original.map(item => ({target_id:item.target_id, action:"A",
  class:item.class, bbox:item.bbox.slice(), reason:"", ai_assisted:false}));
assert.equal(record.raw_seen, false);
assert.equal(record.complete, false);
sign();
assert.equal(record.complete, true);
assert.equal(record.raw_seen, true);
assert.ok(C.checks.every(key => record.checks[key] === true));
assert.ok(Number.isFinite(Date.parse(record.reviewed_at_utc)));
assert.deepEqual(C.completionErrors(sample, record), []);
console.log("single explicit signature: valid attestation, rejected draft unchanged");
'''
    blank_review = re.search(r'const blankReview = sample => \(\{.*?\n  \}\);',
                             scripts["app-script"], re.S)
    assert blank_review
    node_checks += blank_review.group(0) + r'''
const fresh = blankReview(sample);
assert.equal(fresh.reviewer, "1");
assert.equal(fresh.complete, false);
assert.equal(fresh.raw_seen, false);
'''
    importer = re.search(r'  function validateImportedReview\(candidate, item\) \{.*?\n  \}',
                         scripts["app-script"], re.S)
    assert importer
    node_checks += importer.group(0) + r'''
const aiDraft = {...record, image_id:sample.image_id, source_sha256:sample.source_sha256,
  complete:false, reviewed_at_utc:"", actions:[...record.actions,
    {target_id:"teacher_ui_test", action:"N", class:"person", bbox:[0,0,5,5],
      reason:"人工批量核对采用教师候选 ui_test", ai_assisted:true}]};
const reloaded = validateImportedReview(JSON.parse(JSON.stringify(aiDraft)), sample);
assert.deepEqual(reloaded, aiDraft);
assert.equal(reloaded.complete, false);
assert.equal(reloaded.actions.at(-1).ai_assisted, true);
assert.equal(validateImportedReview({...aiDraft, reviewer:""}, sample).reviewer, "1");
assert.equal(validateImportedReview({...aiDraft, reviewer:"custom-human"}, sample).reviewer, "custom-human");
assert.throws(() => validateImportedReview({...aiDraft, complete:true, reviewer:""}, sample), /审核人/);
const corrupt = JSON.parse(JSON.stringify(aiDraft)); corrupt.actions.at(-1).bbox[2] = sample.width + 1;
assert.throws(() => validateImportedReview(corrupt, sample), /XYXY/);
console.log("actual draft importer: batch AI actions round-trip unchanged; invalid box rejected");
'''
    behavior = subprocess.run(
        ["node", "-"], input=(scripts["core"] + "\nconst actual = "
                                     + scripts["review-manifest"].strip() + ";\n" + node_checks),
        text=True, encoding="utf-8", capture_output=True, check=False,
    )
    assert behavior.returncode == 0, behavior.stderr
    patch = read_json(OUTPUT / "review_patch_template.json")
    assert len(patch["reviews"]) == 48
    assert all(not row["complete"] and not row["raw_seen"] and not row["reviewer"]
               for row in patch["reviews"])
    assert not (OUTPUT / "ground_val48.json").exists()

    changed = deepcopy(manifest)
    changed["samples"][0]["source_sha256"] = "0" * 64
    assert dataset_id(changed) != manifest["dataset_id"]
    try:
        export_documents(OUTPUT / "review_manifest_teacher.json", OUTPUT / "reserve_patch.json")
    except ReviewError:
        pass
    else:
        raise AssertionError("reserve path was not rejected before reading")

    # In-memory fixture: full decisions are exportable, but a missing source-box
    # decision cannot silently turn a frame into negative truth.
    complete = blank_patch(manifest)
    for review in complete["reviews"]:
        sample = samples[review["image_id"]]
        review.update(complete=True, raw_seen=True, reviewer="fixture-human",
                      reviewed_at_utc="2026-10-07T00:00:00+00:00",
                      checks={key: True for key in CHECKS},
                      actions=[{"target_id": item["target_id"], "action": "A",
                                "class": item["class"], "bbox": item["bbox"],
                                "reason": "", "ai_assisted": False}
                               for item in sample["original"]])
    bad = deepcopy(complete)
    row_with_box = next(row for row in bad["reviews"] if samples[row["image_id"]]["original"])
    row_with_box["actions"] = []
    with tempfile.TemporaryDirectory(prefix="ground48_test_", dir=OUTPUT.parent) as temporary_dir:
        temporary = Path(temporary_dir) / "synthetic_bad_patch.json"
        temporary.write_text(json.dumps(bad), encoding="utf-8")
        try:
            export_documents(OUTPUT / "review_manifest_teacher.json", temporary)
        except ReviewError:
            pass
        else:
            raise AssertionError("partial or missing-box patch was accepted")
        temporary = Path(temporary_dir) / "synthetic_complete_patch.json"
        temporary.write_text(json.dumps(complete), encoding="utf-8")
        verified, ground, receipt = export_documents(
            OUTPUT / "review_manifest_teacher.json", temporary)
        assert len(verified["images"]) == len(ground["images"]) == 48
        assert Counter(row["camera_id"] for row in ground["images"]) == Counter({CAMERA_A: 24, CAMERA_B: 24})
        assert all(row["split"] == "val" and row["incomplete_frame"] is False for row in ground["images"])
        assert receipt["complete_count"] == 48 and receipt["pending_count"] == 0
    print(behavior.stdout.strip())
    print("PASS: 48 frames, cameras 24/24, batches 4x12 (6A/6B), zero inherited signatures, hash binding, fail-closed negative export")


if __name__ == "__main__":
    main()
