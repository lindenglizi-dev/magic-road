"""Narrow dependency-free checks for the self-contained review workbench."""
from pathlib import Path
import re
import subprocess


HTML = Path(__file__).with_name("review_workbench.html")


def main() -> None:
    text = HTML.read_text(encoding="utf-8")
    assert text.count("__REVIEW_MANIFEST_JSON__") == 1
    scripts = dict(re.findall(r'<script id="([^"]+)"(?: type="[^"]+")?>(.*?)</script>', text, re.S))
    assert {"review-manifest", "core", "app-script"} <= scripts.keys()
    assert 'id="acceptRemaining"' in text and "不会采用任何 Teacher 候选" in text

    syntax = subprocess.run(
        ["node", "--check", "-"], input=scripts["core"] + "\n" + scripts["app-script"],
        text=True, encoding="utf-8", capture_output=True, check=False,
    )
    assert syntax.returncode == 0, syntax.stderr

    checks = r'''
const assert = require("node:assert/strict");
const C = globalThis.WorkbenchCore;
assert.deepEqual(C.clientToNative(60, 45, {left:10, top:20, width:100, height:50}, 1000, 500), [500, 250]);
const sample = {width:100, height:80, original:[{target_id:"o1", class:"person", bbox:[1,2,10,20]}]};
const review = {reviewer:"human", raw_seen:true, checks:Object.fromEntries(C.checks.map(k => [k,true])), actions:[], notes:"", complete:false};
assert.match(C.completionErrors(sample, review).join("|"), /o1/);
review.raw_seen = false;
assert.match(C.completionErrors(sample, review).join("|"), /RAW/);
review.raw_seen = true; review.reviewer = "";
assert.match(C.completionErrors(sample, review).join("|"), /审核人/);
review.reviewer = "human"; review.checks.person = false;
assert.match(C.completionErrors(sample, review).join("|"), /六项/);
review.checks.person = true;
review.actions.push({target_id:"o1", action:"A", class:"person", bbox:[1,2,10,20], reason:"", ai_assisted:false});
assert.deepEqual(C.completionErrors(sample, review), []);
assert.ok(C.actionErrors(sample, {target_id:"o1", action:"A", class:"vehicle", bbox:[1,2,10,20], reason:"", ai_assisted:false}).length);
assert.ok(C.actionErrors(sample, {target_id:"manual_001", action:"N", class:"person", bbox:[0,0,101,20], reason:"missed", ai_assisted:true}).length);
const counts = [["train_review","train",128],["road_development","dev",124],["person_background_aux","stress",24]];
let n = 0, samples = [];
for (const [bucket, split, count] of counts) for (let i = 0; i < count; i++, n++) samples.push({
  image_id:`frame_${n}`, legacy_id:`legacy_${n}`, bucket, split, width:100, height:80,
  source_sha256:"c".repeat(64), raw_file:`images/${n}.jpg`, gt_overlay_file:`overlays/${n}.jpg`,
  original:[], teacher:[], warnings:[], review_score:0
});
assert.deepEqual(C.validateManifest({schema:"cnn_review_workbench_v1", dataset_id:"a".repeat(64), annotation_policy_sha256:"b".repeat(64), teacher_status:"not_run", train_required_count:128, samples}), []);
console.log("review workbench checks: PASS");
'''
    actual = HTML.parent / "reports/verified_gt_workflow_20261006/review_manifest_teacher.json"
    if actual.exists():
        checks += "\nconst actual = " + actual.read_text(encoding="utf-8") + ";\nassert.deepEqual(C.validateManifest(actual), []);\nconsole.log('actual 276-image teacher manifest: PASS');\n"
    behavior = subprocess.run(
        ["node", "-"], input=scripts["core"] + "\n" + checks, text=True, encoding="utf-8", capture_output=True, check=False,
    )
    assert behavior.returncode == 0, behavior.stderr
    print(behavior.stdout.strip())


if __name__ == "__main__":
    main()
