"""Package saved ROI evidence and pending human-review panels without recomputation."""

from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import html
import json
import re
import shutil
import subprocess
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath


PROJECT = Path(__file__).resolve().parents[1]
PAIR_SOURCE = PROJECT / "evaluation/ddr_architecture/roi_pair_explanation_20261001_v1"
REVIEW_SOURCE = PROJECT / "evaluation/scene_extensions/virat_010107_background_subtype_review_v1"
OUTPUT = PROJECT / "evaluation/ddr_architecture/roi_review_bundle_20261002_v2"
ZIP_PATH = OUTPUT / "roi_review_bundle_20261002_v2.zip"
ZIP_HASH_PATH = OUTPUT / "roi_review_bundle_20261002_v2.zip.sha256"
ZIP_VERIFICATION_PATH = OUTPUT / "zip_verification.json"
V1_OUTPUT = PROJECT / "evaluation/ddr_architecture/roi_review_bundle_20261002_v1"
NODE = Path("D:/nodejs/node.exe")

PAIR_FILES = [
    "report.html",
    "report.md",
    "feature_contributions.csv",
    "pair_explanations.json",
    "receipt.json",
]
REVIEW_FILES = ["README.md", "report.json", "review_manifest.csv", "receipt.json"]
ALLOWED_SUBTYPES = [
    "shadow",
    "parking_line_related",
    "background_change",
    "other",
    "uncertain",
]


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def json_dump(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def copy_file(source: Path, destination: Path) -> None:
    if not source.is_file():
        raise FileNotFoundError(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)


def image_uri(path: Path) -> str:
    return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def fmt_box(value: object) -> str:
    return html.escape(json.dumps(value, ensure_ascii=False))


def sampling_fact(crop: dict) -> str:
    width = crop["width"]
    height = crop["height"]
    if width < 32:
        x_fact = f"x轴 {width}→32，源列重复采样"
    elif width > 32:
        x_fact = f"x轴 {width}→32，源列间隔采样"
    else:
        x_fact = "x轴 32→32"
    if height < 32:
        y_fact = f"y轴 {height}→32，源行重复采样"
    elif height > 32:
        y_fact = f"y轴 {height}→32，源行间隔采样"
    else:
        y_fact = "y轴 32→32"
    return f"{x_fact}；{y_fact}"


def review_cards(rows: list[dict]) -> str:
    cards = []
    subtype_options = '<option value="">pending</option>' + "".join(
        f'<option value="{html.escape(value)}">{html.escape(value)}</option>'
        for value in ALLOWED_SUBTYPES
    )
    control_options = (
        '<option value="pending">pending</option>'
        '<option value="confirmed_protection">confirmed_protection</option>'
        '<option value="needs_followup">needs_followup</option>'
    )
    for row in rows:
        item_id = html.escape(row["review_item_id"])
        role = row["review_role"]
        panel = "human_review/" + row["panel_path"].replace("\\", "/")
        if role == "background_subtype_target":
            selector = (
                '<label>背景子类<select class="subtype">'
                + subtype_options
                + "</select></label>"
                '<input class="control-status" type="hidden" value="">'
            )
            instruction = "请选择背景子类；无法判断时选 uncertain，未审保持 pending。"
        else:
            selector = (
                '<label>保护核对<select class="control-status">'
                + control_options
                + "</select></label>"
                '<input class="subtype" type="hidden" value="">'
            )
            instruction = "保护对照不得填写背景子类；可确认保护或标记需继续核对。"
        cards.append(
            f'''<article class="review-card" data-id="{item_id}" data-role="{html.escape(role)}"
 data-sample-id="{html.escape(row['sample_id'])}" data-candidate-id="{html.escape(row['candidate_id'])}"
 data-panel-path="{html.escape(row['panel_path'])}" data-panel-sha256="{html.escape(row['panel_sha256'])}">
<h3>{item_id} · {html.escape(row['sample_id'])}</h3>
<p class="muted">{html.escape(role)} · frame {html.escape(row['frame_index'])} · {html.escape(row['branch'])}</p>
<img class="panel" src="{html.escape(panel)}" alt="{item_id} review panel">
<p>{html.escape(instruction)}</p>
<div class="fields">{selector}
<label>审阅者<input class="reviewer" type="text" autocomplete="name"></label>
<label>审阅时间<input class="reviewed-at" type="datetime-local"></label>
<label class="wide">说明<textarea class="note" rows="2"></textarea></label></div>
</article>'''
        )
    return "\n".join(cards)


def build_html(pair_data: dict, review_rows: list[dict], source_meta: dict) -> str:
    pair_sections = []
    for pair in pair_data["pairs"]:
        identity = pair["identity"]
        observed = pair["observed"]
        before = observed["baseline"]
        after = observed["min_run1"]
        before_crop = before["analysis_crop"]
        after_crop = after["analysis_crop"]
        before_area = before_crop["width"] * before_crop["height"]
        after_area = after_crop["width"] * after_crop["height"]
        ratio = after_area / before_area
        before_png = PAIR_SOURCE / before["saved_roi"]["copied_path"]
        after_png = PAIR_SOURCE / after["saved_roi"]["copied_path"]
        before_score = before["saved_scores"]
        after_score = after["saved_scores"]
        pair_sections.append(
            f'''<section class="pair"><h2>{html.escape(identity)}</h2>
<div class="roi-grid">
<figure><img class="roi" src="{image_uri(before_png)}" alt="{html.escape(identity)} baseline ROI"><figcaption>
baseline · crop {fmt_box(before_crop['inclusive_box'])}<br>
{before_crop['width']}×{before_crop['height']}，面积 {before_area}<br>
float {html.escape(before_score['hog324_float_score'])} → {html.escape(before_score['hog324_float_prediction'])}<br>
Q {html.escape(before_score['hog324_q_score_integer'])} → {html.escape(before_score['hog324_q_prediction'])}</figcaption></figure>
<figure><img class="roi" src="{image_uri(after_png)}" alt="{html.escape(identity)} min_run1 ROI"><figcaption>
min_run1 · crop {fmt_box(after_crop['inclusive_box'])}<br>
{after_crop['width']}×{after_crop['height']}，面积 {after_area}<br>
float {html.escape(after_score['hog324_float_score'])} → {html.escape(after_score['hog324_float_prediction'])}<br>
Q {html.escape(after_score['hog324_q_score_integer'])} → {html.escape(after_score['hog324_q_prediction'])}</figcaption></figure>
</div>
<p><strong>已存裁剪面积比：</strong>{after_area}/{before_area} = {ratio:.2f}。</p>
<p><strong>采样尺度事实：</strong>baseline：{sampling_fact(before_crop)}；min_run1：{sampling_fact(after_crop)}。两者都使用已记录的 pixel-centre Q8 最近邻 DDA 索引。</p>
<p><strong>已存算术：</strong>Δfloat={observed['hog324_float_score_delta']:.12g}；ΔQ={observed['hog324_integer_score_delta']}，且等于 324 项已存乘积差之和。</p>
</section>'''
        )

    meta_json = json.dumps(source_meta, ensure_ascii=False).replace("</", "<\\/")
    allowed_json = json.dumps(ALLOWED_SUBTYPES, ensure_ascii=False)
    cards = review_cards(review_rows)
    missing = "".join(f"<li>{html.escape(item)}</li>" for item in pair_data["missing_saved_evidence"])
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ROI 证据与人工审阅包</title>
<style>
:root{{--ink:#20242a;--muted:#667085;--line:#d0d5dd;--accent:#155eef;--bg:#f7f8fa}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 system-ui,"Microsoft YaHei",sans-serif}}
main{{max-width:1220px;margin:auto;padding:28px}}section,article{{background:white;border:1px solid var(--line);border-radius:12px;padding:18px;margin:16px 0}}
h1,h2,h3{{line-height:1.25}}code{{background:#eef2f6;padding:.12rem .3rem;border-radius:4px}}.muted{{color:var(--muted)}}
.roi-grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}}figure{{margin:0}}.roi{{width:256px;height:256px;max-width:100%;image-rendering:pixelated;border:1px solid #555}}
.review-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(360px,1fr));gap:16px}}.review-card{{margin:0}}.panel{{width:100%;height:auto;border:1px solid var(--line)}}
.fields{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}}label{{display:flex;flex-direction:column;gap:4px}}.wide{{grid-column:1/-1}}
input,select,textarea,button{{font:inherit;padding:8px;border:1px solid #98a2b3;border-radius:6px}}button{{background:var(--accent);color:white;border:0;cursor:pointer;padding:10px 16px}}
.sticky{{position:sticky;bottom:8px;display:flex;align-items:center;gap:14px;background:#fff;border:1px solid var(--line);padding:12px;border-radius:10px;box-shadow:0 4px 16px #0002}}
@media(max-width:700px){{main{{padding:12px}}.roi-grid,.fields{{grid-template-columns:1fr}}}}
</style></head><body><main>
<h1>ROI 证据与人工审阅包</h1>
<p>本页只重整已保存工件。未解码视频、未重裁剪、未重提特征、未重评分、未训练或扫描阈值。</p>
<section><h2>三对 ROI 的已存观测</h2>
<p>三例面积比分别为 <strong>1.57、1.56、2.37</strong>。六张 ROI 已作为 base64 数据嵌入本页，离线打开仍可见。</p></section>
{''.join(pair_sections)}
<section><h2>观测、推断与缺失</h2>
<p><strong>观测：</strong>{html.escape(pair_data['conclusion']['observed'])}</p>
<p><strong>推断：</strong>{html.escape(pair_data['conclusion']['inferred'])}</p>
<p><strong>不支持：</strong>{html.escape(pair_data['conclusion']['not_supported'])}</p>
<h3>明确缺失</h3><ul>{missing}</ul></section>
<section><h2>人工待审入口：22 个 invalid 子类 + 5 个保护对照</h2>
<p>所有人审字段初始为空，页面默认状态为 pending。背景目标只能选择既有五类；保护对照不得填写背景子类。填写后点击导出，浏览器会生成带版本、项目 ID、面板原哈希和来源清单哈希的 <code>review.json</code>。</p>
<p><a href="human_review/README.md">原审阅说明</a> · <a href="human_review/review_manifest.csv">原空白清单</a> · <a href="human_review/contact_sheets/contact_sheet_01.jpg">联系表入口</a></p></section>
<div class="review-grid">{cards}</div>
<div class="sticky"><button id="export">导出 review.json</button><span id="status" class="muted">27 项均为 pending</span></div>
<script id="source-meta" type="application/json">{meta_json}</script>
<script>
const ALLOWED = {allowed_json};
const sourceMeta = JSON.parse(document.getElementById('source-meta').textContent);
const cards = [...document.querySelectorAll('.review-card')];
function collect() {{
  const errors = [], ids = new Set(), items = [];
  for (const card of cards) {{
    const id = card.dataset.id, role = card.dataset.role;
    const subtype = card.querySelector('.subtype').value;
    const control = card.querySelector('.control-status').value;
    if (ids.has(id)) errors.push(`duplicate id: ${{id}}`); ids.add(id);
    if (role === 'background_subtype_target' && subtype && !ALLOWED.includes(subtype)) errors.push(`invalid subtype: ${{id}}`);
    if (role === 'protection_control' && subtype) errors.push(`protection control has subtype: ${{id}}`);
    const status = role === 'background_subtype_target' ? (subtype ? 'reviewed' : 'pending') : control;
    items.push({{
      review_item_id:id, sample_id:card.dataset.sampleId, candidate_id:card.dataset.candidateId,
      review_role:role, source_panel_path:card.dataset.panelPath, source_panel_sha256:card.dataset.panelSha256,
      review_status:status || 'pending', background_subtype:subtype,
      reviewer:card.querySelector('.reviewer').value.trim(), reviewed_at:card.querySelector('.reviewed-at').value,
      review_note:card.querySelector('.note').value.trim()
    }});
  }}
  const pending = items.filter(x => x.review_status === 'pending').length;
  return {{
    schema:'ddr_roi_human_review_v1', schema_version:1,
    source:sourceMeta, exported_at:new Date().toISOString(),
    validation:{{valid:errors.length===0, errors, expected_items:sourceMeta.item_count, actual_items:items.length, unique_ids:ids.size}},
    summary:{{pending, reviewed:items.length-pending}}, items
  }};
}}
function updateStatus() {{ const r=collect(); document.getElementById('status').textContent=`${{r.summary.pending}} pending / ${{r.summary.reviewed}} 已填写`; }}
document.querySelectorAll('select,input,textarea').forEach(x=>x.addEventListener('input',updateStatus));
document.getElementById('export').addEventListener('click',()=>{{
  const result=collect();
  if (!result.validation.valid) {{ alert(result.validation.errors.join('\\n')); return; }}
  const blob=new Blob([JSON.stringify(result,null,2)+'\\n'],{{type:'application/json'}});
  const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='review.json'; a.click();
  setTimeout(()=>URL.revokeObjectURL(a.href),1000); updateStatus();
}});
</script></main></body></html>'''


def source_path_hashes(paths: list[Path]) -> dict[str, str]:
    return {path.relative_to(PROJECT).as_posix(): digest(path) for path in sorted(paths)}


def load_review_rows() -> list[dict]:
    with (REVIEW_SOURCE / "review_manifest.csv").open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 27:
        raise AssertionError(f"expected 27 review rows, got {len(rows)}")
    roles = Counter(row["review_role"] for row in rows)
    if roles != Counter({"background_subtype_target": 22, "protection_control": 5}):
        raise AssertionError(f"unexpected role counts: {roles}")
    human_fields = ["background_subtype", "reviewer", "reviewed_at", "review_note"]
    if any(row[field].strip() for row in rows for field in human_fields):
        raise AssertionError("source human-review fields are not blank")
    if len({row["review_item_id"] for row in rows}) != len(rows):
        raise AssertionError("duplicate review_item_id")
    return rows


def safe_member(name: str) -> bool:
    path = PurePosixPath(name)
    return (
        not path.is_absolute()
        and ".." not in path.parts
        and "" not in path.parts
        and "\\" not in name
        and not (path.parts and ":" in path.parts[0])
    )


def assert_receipt_artifacts(base: Path, receipt: dict) -> int:
    checked = 0
    for relative, expected in receipt["artifact_hashes"].items():
        path = base / relative
        if not path.is_file() or digest(path) != expected:
            raise AssertionError(f"receipt artifact mismatch: {path}")
        checked += 1
    return checked


def extract_page_script(page: str) -> str:
    scripts = re.findall(r"<script>(.*?)</script>", page, flags=re.DOTALL)
    if len(scripts) != 1:
        raise AssertionError(f"expected one executable page script, got {len(scripts)}")
    return scripts[0].strip() + "\n"


def run_node_check(script: Path, log: Path, expect_success: bool) -> subprocess.CompletedProcess[str]:
    if not NODE.is_file():
        raise FileNotFoundError(NODE)
    completed = subprocess.run(
        [str(NODE), "--check", str(script)],
        cwd=PROJECT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    log.write_text(
        f"command: {NODE} --check {script}\n"
        f"exit_code: {completed.returncode}\n"
        f"stdout:\n{completed.stdout}\n"
        f"stderr:\n{completed.stderr}\n",
        encoding="utf-8",
    )
    if (completed.returncode == 0) != expect_success:
        raise AssertionError(
            f"unexpected node --check result for {script}: {completed.returncode}"
        )
    return completed


def mock_dom_script(page_script: str, rows: list[dict], source_meta: dict) -> str:
    datasets = [
        {
            "id": row["review_item_id"],
            "role": row["review_role"],
            "sampleId": row["sample_id"],
            "candidateId": row["candidate_id"],
            "panelPath": row["panel_path"],
            "panelSha256": row["panel_sha256"],
        }
        for row in rows
    ]
    prelude = f"""'use strict';
const assert = require('node:assert/strict');
const mockMeta = {json.dumps(source_meta, ensure_ascii=False)};
const mockDatasets = {json.dumps(datasets, ensure_ascii=False)};
function field(value='') {{ return {{value, addEventListener() {{}}}}; }}
const mockCards = mockDatasets.map(dataset => {{
  const fields = {{
    '.subtype': field(''), '.control-status': field(dataset.role === 'protection_control' ? 'pending' : ''),
    '.reviewer': field(''), '.reviewed-at': field(''), '.note': field('')
  }};
  return {{dataset, fields, querySelector(selector) {{ return fields[selector]; }}}};
}});
const statusElement = {{textContent:''}};
let exportHandler = null, downloaded = null, lastBlob = null, alerts = [];
const exportButton = {{addEventListener(event, handler) {{ assert.equal(event, 'click'); exportHandler = handler; }}}};
globalThis.document = {{
  getElementById(id) {{
    if (id === 'source-meta') return {{textContent:JSON.stringify(mockMeta)}};
    if (id === 'status') return statusElement;
    if (id === 'export') return exportButton;
    throw new Error(`unexpected id: ${{id}}`);
  }},
  querySelectorAll(selector) {{
    if (selector === '.review-card') return mockCards;
    if (selector === 'select,input,textarea') return [];
    throw new Error(`unexpected selector: ${{selector}}`);
  }},
  createElement(tag) {{
    assert.equal(tag, 'a');
    return {{href:'', download:'', click() {{
      downloaded = {{download:this.download, text:lastBlob.parts.join('')}};
    }}}};
  }}
}};
globalThis.Blob = class {{ constructor(parts, options) {{ this.parts=parts; this.options=options; }} }};
globalThis.URL = {{createObjectURL(blob) {{ lastBlob=blob; return 'blob:mock'; }}, revokeObjectURL() {{}}}};
globalThis.setTimeout = () => 0;
globalThis.alert = message => alerts.push(String(message));
"""
    tests = """
let result = collect();
assert.equal(result.validation.valid, true);
assert.equal(result.validation.actual_items, 27);
assert.equal(result.validation.unique_ids, 27);
assert.equal(result.summary.pending, 27);
assert.equal(result.summary.reviewed, 0);
for (let i=0; i<cards.length; i++) {
  assert.equal(result.items[i].review_item_id, cards[i].dataset.id);
  assert.equal(result.items[i].source_panel_sha256, cards[i].dataset.panelSha256);
}
const background = cards.find(card => card.dataset.role === 'background_subtype_target');
background.fields['.subtype'].value = 'shadow';
background.fields['.reviewer'].value = 'reviewer-a';
background.fields['.reviewed-at'].value = '2026-10-02T12:34';
background.fields['.note'].value = 'checked background';
const protection = cards.find(card => card.dataset.role === 'protection_control');
protection.fields['.control-status'].value = 'confirmed_protection';
protection.fields['.reviewer'].value = 'reviewer-b';
protection.fields['.note'].value = 'keep protected';
result = collect();
assert.equal(result.validation.valid, true);
assert.equal(result.summary.pending, 25);
assert.equal(result.summary.reviewed, 2);
const backgroundItem = result.items.find(item => item.review_item_id === background.dataset.id);
const protectionItem = result.items.find(item => item.review_item_id === protection.dataset.id);
assert.equal(backgroundItem.background_subtype, 'shadow');
assert.equal(backgroundItem.source_panel_sha256, background.dataset.panelSha256);
assert.equal(protectionItem.review_status, 'confirmed_protection');
assert.equal(protectionItem.background_subtype, '');
assert.equal(result.source.source_manifest_sha256, mockMeta.source_manifest_sha256);
assert.equal(typeof exportHandler, 'function');
exportHandler();
assert.ok(downloaded);
assert.equal(downloaded.download, 'review.json');
assert.ok(downloaded.text.endsWith('\\n'));
const exported = JSON.parse(downloaded.text);
assert.equal(exported.schema, 'ddr_roi_human_review_v1');
assert.equal(exported.source.bundle_version, 'roi_review_bundle_20261002_v2');
assert.equal(exported.items.length, 27);
assert.equal(exported.items.find(item => item.review_item_id === background.dataset.id).source_panel_sha256, background.dataset.panelSha256);
protection.fields['.subtype'].value = 'shadow';
downloaded = null; alerts = [];
exportHandler();
assert.equal(downloaded, null);
assert.equal(alerts.length, 1);
assert.ok(alerts[0].includes('protection control has subtype'));
console.log(JSON.stringify({status:'PASS', initial_pending:27, simulated_reviewed:2,
  export_items:exported.items.length, invalid_protection_subtype_rejected:true,
  identity_and_hash_preserved:true}));
"""
    return prelude + "\n" + page_script + "\n" + tests


def verify_zip() -> dict:
    if not ZIP_PATH.is_file():
        raise FileNotFoundError(ZIP_PATH)
    with zipfile.ZipFile(ZIP_PATH) as archive:
        names = archive.namelist()
        if any(not safe_member(name) for name in names):
            raise AssertionError("zip contains unsafe path")
        if len(names) != len(set(names)):
            raise AssertionError("zip contains duplicate member")
        manifest = json.loads(archive.read("bundle_manifest.json"))
        expected = set(manifest["files"]) | {"bundle_manifest.json"}
        if set(names) != expected:
            raise AssertionError("zip member set does not match bundle_manifest.json")
        mismatches = []
        for name, fact in manifest["files"].items():
            payload = archive.read(name)
            if digest_bytes(payload) != fact["sha256"] or len(payload) != fact["bytes"]:
                mismatches.append(name)
        if mismatches:
            raise AssertionError(f"zip content hash mismatch: {mismatches}")
    return {
        "status": "PASS",
        "zip_path": ZIP_PATH.relative_to(PROJECT).as_posix(),
        "zip_sha256": digest(ZIP_PATH),
        "member_count": len(names),
        "manifested_file_count": len(manifest["files"]),
        "unsafe_paths": 0,
        "hash_mismatches": 0,
    }


def build() -> dict:
    if OUTPUT.exists():
        raise FileExistsError(
            f"refusing to overwrite existing evidence bundle: {OUTPUT}; use --verify"
        )
    OUTPUT.mkdir(parents=True, exist_ok=False)
    pair_data = json.loads((PAIR_SOURCE / "pair_explanations.json").read_text(encoding="utf-8"))
    rows = load_review_rows()
    pair_receipt = json.loads((PAIR_SOURCE / "receipt.json").read_text(encoding="utf-8"))
    review_receipt = json.loads((REVIEW_SOURCE / "receipt.json").read_text(encoding="utf-8"))
    receipt_artifacts_checked = (
        assert_receipt_artifacts(PAIR_SOURCE, pair_receipt)
        + assert_receipt_artifacts(REVIEW_SOURCE, review_receipt)
    )

    source_files: list[Path] = []
    for relative in PAIR_FILES:
        source = PAIR_SOURCE / relative
        copy_file(source, OUTPUT / "roi_pair" / relative)
        source_files.append(source)
    pair_images = sorted((PAIR_SOURCE / "images").glob("*.png"))
    if len(pair_images) != 6:
        raise AssertionError(f"expected 6 ROI PNGs, got {len(pair_images)}")
    for source in pair_images:
        copy_file(source, OUTPUT / "roi_pair/images" / source.name)
        source_files.append(source)

    for relative in REVIEW_FILES:
        source = REVIEW_SOURCE / relative
        copy_file(source, OUTPUT / "human_review" / relative)
        source_files.append(source)
    review_panels = sorted((REVIEW_SOURCE / "panels").glob("*.png"))
    contact_sheets = sorted((REVIEW_SOURCE / "contact_sheets").glob("*.jpg"))
    if len(review_panels) != 27 or len(contact_sheets) != 7:
        raise AssertionError("review panel/contact-sheet count mismatch")
    for source in review_panels:
        copy_file(source, OUTPUT / "human_review/panels" / source.name)
        source_files.append(source)
    for source in contact_sheets:
        copy_file(source, OUTPUT / "human_review/contact_sheets" / source.name)
        source_files.append(source)

    source_hashes = source_path_hashes(source_files)
    json_dump(OUTPUT / "source_hashes.json", {"schema": "ddr_roi_review_source_hashes_v2", "files": source_hashes})

    review_receipt_hash = digest(REVIEW_SOURCE / "receipt.json")
    review_manifest_hash = digest(REVIEW_SOURCE / "review_manifest.csv")
    source_meta = {
        "source_schema": "virat_background_subtype_review_v1",
        "review_schema_version": 1,
        "bundle_version": "roi_review_bundle_20261002_v2",
        "item_count": 27,
        "background_subtype_target_count": 22,
        "protection_control_count": 5,
        "source_manifest_path": "evaluation/scene_extensions/virat_010107_background_subtype_review_v1/review_manifest.csv",
        "source_manifest_sha256": review_manifest_hash,
        "source_receipt_sha256": review_receipt_hash,
    }
    template_items = []
    for row in rows:
        template_items.append({
            "review_item_id": row["review_item_id"],
            "sample_id": row["sample_id"],
            "candidate_id": row["candidate_id"],
            "review_role": row["review_role"],
            "source_panel_path": row["panel_path"],
            "source_panel_sha256": row["panel_sha256"],
            "review_status": "pending",
            "background_subtype": "",
            "reviewer": "",
            "reviewed_at": "",
            "review_note": "",
        })
    json_dump(OUTPUT / "review_template.json", {
        "schema": "ddr_roi_human_review_v1",
        "schema_version": 1,
        "source": source_meta,
        "summary": {"pending": 27, "reviewed": 0},
        "items": template_items,
    })

    html_text = build_html(pair_data, rows, source_meta)
    (OUTPUT / "index.html").write_text(html_text, encoding="utf-8")
    contribution_rows = sum(1 for _ in (PAIR_SOURCE / "feature_contributions.csv").open(encoding="utf-8")) - 1
    if contribution_rows != 3 * 324:
        raise AssertionError(f"expected 972 contribution rows, got {contribution_rows}")
    embedded_payloads = re.findall(r'src="data:image/png;base64,([A-Za-z0-9+/=]+)"', html_text)
    if len(embedded_payloads) != 6:
        raise AssertionError("index.html does not embed exactly six ROI images")
    embedded_hashes = [digest_bytes(base64.b64decode(payload, validate=True)) for payload in embedded_payloads]
    expected_roi_hashes = [digest(path) for path in pair_images]
    if embedded_hashes != expected_roi_hashes:
        raise AssertionError("embedded ROI image hash mismatch")
    if any(f'human_review/{row["panel_path"]}' not in html_text for row in rows):
        raise AssertionError("index.html does not link every review panel")
    for row in rows:
        copied_panel = OUTPUT / "human_review" / row["panel_path"]
        if not copied_panel.is_file() or digest(copied_panel) != row["panel_sha256"]:
            raise AssertionError(f"review panel link/hash mismatch: {row['review_item_id']}")

    checks = OUTPUT / "checks"
    checks.mkdir()
    page_script = extract_page_script(html_text)
    page_script_path = checks / "index.js"
    page_script_path.write_text(page_script, encoding="utf-8")
    run_node_check(page_script_path, checks / "node_check.txt", expect_success=True)

    v1_html_path = V1_OUTPUT / "index.html"
    v1_zip_path = V1_OUTPUT / "roi_review_bundle_20261002_v1.zip"
    if not v1_html_path.is_file() or not v1_zip_path.is_file():
        raise FileNotFoundError("frozen v1 failure evidence is missing")
    v1_script_path = checks / "v1_broken_index.js"
    v1_script_path.write_text(extract_page_script(v1_html_path.read_text(encoding="utf-8")), encoding="utf-8")
    run_node_check(v1_script_path, checks / "v1_node_check.txt", expect_success=False)

    mock_path = checks / "mock_dom_test.js"
    mock_path.write_text(mock_dom_script(page_script, rows, source_meta), encoding="utf-8")
    mock_completed = subprocess.run(
        [str(NODE), str(mock_path)], cwd=PROJECT, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    (checks / "mock_dom_test.txt").write_text(
        f"command: {NODE} {mock_path}\n"
        f"exit_code: {mock_completed.returncode}\n"
        f"stdout:\n{mock_completed.stdout}\n"
        f"stderr:\n{mock_completed.stderr}\n",
        encoding="utf-8",
    )
    if mock_completed.returncode != 0 or '"status":"PASS"' not in mock_completed.stdout:
        raise AssertionError("mock DOM/export test failed")

    readme = """# ROI 证据与人工审阅包\n\n打开 `index.html` 查看三对已存 ROI 与 27 项人工待审面板。六张 32×32 ROI 已嵌入 HTML；待审面板作为包内文件引用。\n\n页面导出的 `review.json` 会保留 schema/version、27 个 review ID、每张面板的原始 SHA-256，以及来源清单和 receipt 哈希。未选择项保持 `pending`。保护对照不得填写背景子类。\n\n本包没有解码视频、重裁剪、重提特征、重评分、训练或阈值扫描。人工确认尚未完成。\n"""
    (OUTPUT / "README.md").write_text(readme, encoding="utf-8")

    receipt = {
        "schema": "ddr_roi_review_bundle_receipt_v2",
        "status": "PASS_saved_artifact_review_bundle_only",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "command": ["python", "tools/ddr_roi_review_bundle.py"],
        "script_sha256": digest(Path(__file__)),
        "inputs": source_hashes,
        "counts": {
            "roi_pairs": 3,
            "embedded_roi_png": 6,
            "feature_contribution_rows": contribution_rows,
            "background_subtype_targets": 22,
            "protection_controls": 5,
            "review_panels": 27,
            "contact_sheets": 7,
        },
        "review_contract": {
            "allowed_background_subtypes": ALLOWED_SUBTYPES,
            "initial_human_status": "pending",
            "source_human_fields_blank": True,
            "protection_background_subtype_must_remain_blank": True,
            "export_schema": "ddr_roi_human_review_v1",
            "export_schema_version": 1,
        },
        "boundaries": [
            "Only existing saved artifacts were copied or embedded.",
            "No video decode, crop, resize, feature extraction, scoring, training, or threshold scan was performed.",
            "No human label was inferred or marked complete.",
            "Unknown review decisions remain pending.",
        ],
        "self_check": {
            "embedded_roi_data_uris": 6,
            "embedded_roi_hash_matches": 6,
            "linked_review_panels": 27,
            "linked_review_panel_hash_matches": 27,
            "source_receipt_artifacts_checked": receipt_artifacts_checked,
            "source_hash_mismatches": 0,
            "node_page_syntax": "PASS",
            "mock_dom_collect_export": "PASS",
            "v1_broken_page_syntax_preserved": True,
            "zip_integrity": "verified separately in zip_verification.json",
        },
        "v1_failure_evidence": {
            "index_html_sha256": digest(v1_html_path),
            "zip_sha256": digest(v1_zip_path),
            "node_check_exit_nonzero": True,
            "copied_check_log": "checks/v1_node_check.txt",
            "v1_files_modified": False,
        },
    }
    json_dump(OUTPUT / "receipt.json", receipt)

    payload_files = sorted(
        path for path in OUTPUT.rglob("*")
        if path.is_file() and path not in {ZIP_PATH, ZIP_HASH_PATH, ZIP_VERIFICATION_PATH, OUTPUT / "bundle_manifest.json"}
    )
    manifest_files = {
        path.relative_to(OUTPUT).as_posix(): {"sha256": digest(path), "bytes": path.stat().st_size}
        for path in payload_files
    }
    json_dump(OUTPUT / "bundle_manifest.json", {
        "schema": "ddr_roi_review_bundle_manifest_v2",
        "root": "roi_review_bundle_20261002_v2",
        "files": manifest_files,
    })

    archive_files = payload_files + [OUTPUT / "bundle_manifest.json"]
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in archive_files:
            archive.write(path, path.relative_to(OUTPUT).as_posix())

    verification = verify_zip()
    json_dump(ZIP_VERIFICATION_PATH, verification)
    ZIP_HASH_PATH.write_text(f"{verification['zip_sha256']}  {ZIP_PATH.name}\n", encoding="ascii")
    return verification | receipt["counts"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true", help="verify the existing ZIP only")
    args = parser.parse_args()
    result = verify_zip() if args.verify else build()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
