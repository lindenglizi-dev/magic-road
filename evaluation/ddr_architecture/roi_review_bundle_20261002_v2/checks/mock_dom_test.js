'use strict';
const assert = require('node:assert/strict');
const mockMeta = {"source_schema": "virat_background_subtype_review_v1", "review_schema_version": 1, "bundle_version": "roi_review_bundle_20261002_v2", "item_count": 27, "background_subtype_target_count": 22, "protection_control_count": 5, "source_manifest_path": "evaluation/scene_extensions/virat_010107_background_subtype_review_v1/review_manifest.csv", "source_manifest_sha256": "882fa4f531fbd170792dfb53a16c0dcbbfd6de586ed7e73dbdf620c2e4097d90", "source_receipt_sha256": "7063429571ca519dd4806879971cbb357c63b2b2f05e0ae5688705e073f54d14"};
const mockDatasets = [{"id": "bs0000", "role": "background_subtype_target", "sampleId": "vr00001", "candidateId": "fill_only_T100:f000120:slot1:cc5", "panelPath": "panels/panel_vr00001.png", "panelSha256": "d97ff32f763ead44722938816cedc375b10a181d27943efd93c3bad9aee0e9a8"}, {"id": "bs0001", "role": "background_subtype_target", "sampleId": "vr00008", "candidateId": "fill_only_T100:f000138:slot2:cc1", "panelPath": "panels/panel_vr00008.png", "panelSha256": "4e5f40b69d804723728d434ea07c9239cb64dea774cc972412adf5187e64b8cf"}, {"id": "bs0002", "role": "background_subtype_target", "sampleId": "vr00009", "candidateId": "fill_only_T100:f000139:slot3:cc9", "panelPath": "panels/panel_vr00009.png", "panelSha256": "c86abc70ce0cc18c1514fe454a47cdd142de9afce7f96c8f86cbc4935e910e05"}, {"id": "bs0003", "role": "background_subtype_target", "sampleId": "vr00016", "candidateId": "fill_only_T100:f000158:slot1:cc8", "panelPath": "panels/panel_vr00016.png", "panelSha256": "9a7f6dde1f9979fbdd6d91a20271509e1e920a586dbf703b2fdf2fccaf05d045"}, {"id": "bs0004", "role": "background_subtype_target", "sampleId": "vr00019", "candidateId": "fill_only_T100:f000179:slot0:cc9", "panelPath": "panels/panel_vr00019.png", "panelSha256": "bd37376c17959e752d167303e61c4bd2cbca93f65ecab02919fc3046532f8d65"}, {"id": "bs0005", "role": "background_subtype_target", "sampleId": "vr00024", "candidateId": "fill_only_T100:f000192:slot2:cc11", "panelPath": "panels/panel_vr00024.png", "panelSha256": "8c39c936f9531a6a3cfe25e42b86519d24ab35362288946c401c62f4c4a386a1"}, {"id": "bs0006", "role": "background_subtype_target", "sampleId": "vr00025", "candidateId": "fill_only_T100:f000195:slot1:cc8", "panelPath": "panels/panel_vr00025.png", "panelSha256": "e0f73558ac6cf8cea14438e378ff06178b0ccc1ba93dc613b4b40fe8d8cff234"}, {"id": "bs0007", "role": "background_subtype_target", "sampleId": "vr00048", "candidateId": "fill_only_T100:f000290:slot3:cc7", "panelPath": "panels/panel_vr00048.png", "panelSha256": "f40b287d559e9ac3f13dac274197c7e0d18854fbcd737a6e0282063d1b2b1cce"}, {"id": "bs0008", "role": "background_subtype_target", "sampleId": "vr00049", "candidateId": "fill_only_T100:f000297:slot2:cc7", "panelPath": "panels/panel_vr00049.png", "panelSha256": "f81d11bc07e7f6e0e37c65f9668972fa75b3bc4cfbd04336211a825c9a284ecd"}, {"id": "bs0009", "role": "background_subtype_target", "sampleId": "vr00052", "candidateId": "fill_only_T100:f000301:slot3:cc10", "panelPath": "panels/panel_vr00052.png", "panelSha256": "14ae63ec68810ee676f82aaab3ced85bcb70cff8637878a93a01598606c41a14"}, {"id": "bs0010", "role": "background_subtype_target", "sampleId": "vr00003", "candidateId": "fill_only_T100:f000123:slot3:cc7", "panelPath": "panels/panel_vr00003.png", "panelSha256": "dfcc5d7b999c8a944ee275d26c106908c1b95fd7a7a9c5abb109fd1cba64d7e0"}, {"id": "bs0011", "role": "background_subtype_target", "sampleId": "vr00067", "candidateId": "fill_only_T100:f000388:slot3:cc9", "panelPath": "panels/panel_vr00067.png", "panelSha256": "ce23e5ae01c30266b9ff28b3628d8b7e365366bf2fa18f6981afe358c875f631"}, {"id": "bs0012", "role": "background_subtype_target", "sampleId": "vr00038", "candidateId": "fill_only_T100:f000259:slot3:cc3", "panelPath": "panels/panel_vr00038.png", "panelSha256": "c927d3de76cc50dbf96dba13b2bcf38a8fbdbe17fa772073f41e7bf8c5ea0883"}, {"id": "bs0013", "role": "background_subtype_target", "sampleId": "vr00006", "candidateId": "fill_only_T100:f000127:slot3:cc6", "panelPath": "panels/panel_vr00006.png", "panelSha256": "b6541f96bfc74c73de752218f70af85c24ceb5979653bbcfeb7853fc8c374bcc"}, {"id": "bs0014", "role": "background_subtype_target", "sampleId": "vr00074", "candidateId": "fill_only_T100:f000421:slot3:cc7", "panelPath": "panels/panel_vr00074.png", "panelSha256": "047433add867d859331dafc5bc09bbc9dd2eaa2dc82d61d56a5564f45e7b39eb"}, {"id": "bs0015", "role": "background_subtype_target", "sampleId": "vr00043", "candidateId": "fill_only_T100:f000270:slot3:cc3", "panelPath": "panels/panel_vr00043.png", "panelSha256": "ae6e2ca0eaf87d287fccd9b86f38c1571bc805d165ec00c1c1bcc49c238b3fa0"}, {"id": "bs0016", "role": "background_subtype_target", "sampleId": "vr00007", "candidateId": "fill_only_T100:f000130:slot2:cc6", "panelPath": "panels/panel_vr00007.png", "panelSha256": "d6e6facdf62a42eea58a05f037a9cf921b3443a1ea1b05b587bdbfd304dabb89"}, {"id": "bs0017", "role": "background_subtype_target", "sampleId": "vr00055", "candidateId": "fill_only_T100:f000329:slot3:cc4", "panelPath": "panels/panel_vr00055.png", "panelSha256": "75d9564c06b36cb88d3508756439aab41780d6cbb67c7e9f5663c19a78ad4689"}, {"id": "bs0018", "role": "background_subtype_target", "sampleId": "vr00011", "candidateId": "fill_only_T100:f000145:slot3:cc6", "panelPath": "panels/panel_vr00011.png", "panelSha256": "4ae3bd75a5972d5998cf09fce9e239f12ac59860799f93e374dd18675d6b30ad"}, {"id": "bs0019", "role": "background_subtype_target", "sampleId": "vr00058", "candidateId": "fill_only_T100:f000343:slot3:cc4", "panelPath": "panels/panel_vr00058.png", "panelSha256": "c3e155b52fc942922f6364ccdaece9b28b6b84f9305ced3bed4087d5c7c5801d"}, {"id": "bs0020", "role": "background_subtype_target", "sampleId": "vr00018", "candidateId": "fill_only_T100:f000170:slot3:cc8", "panelPath": "panels/panel_vr00018.png", "panelSha256": "29b4d39f00a342f7e63c647fb30757af2b7745970fd9bd0a05243f86e47922ad"}, {"id": "bs0021", "role": "background_subtype_target", "sampleId": "vr00061", "candidateId": "fill_only_T100:f000354:slot3:cc4", "panelPath": "panels/panel_vr00061.png", "panelSha256": "0ba3cec017065166de8720ebfa1e95f414a86240f2bc36aa66833829a7f6b753"}, {"id": "bs0022", "role": "protection_control", "sampleId": "vr00002", "candidateId": "fill_only_T100:f000120:slot2:cc7", "panelPath": "panels/panel_vr00002.png", "panelSha256": "950fcbe5e3578f7725c1655418133f434bae2f3f7129d83aac6ded809642504c"}, {"id": "bs0023", "role": "protection_control", "sampleId": "vr00015", "candidateId": "fill_only_T100:f000157:slot3:cc5", "panelPath": "panels/panel_vr00015.png", "panelSha256": "a7847c7baed111c79369265b86299e7e7d3c78c0ee658292af84b4fbe3b63646"}, {"id": "bs0024", "role": "protection_control", "sampleId": "vr00035", "candidateId": "fill_only_T100:f000240:slot3:cc7", "panelPath": "panels/panel_vr00035.png", "panelSha256": "ba2951c4db680edf90ed3ad3c96a66d06905195dcb22be44a8664cf9530e422b"}, {"id": "bs0025", "role": "protection_control", "sampleId": "vr00063", "candidateId": "fill_only_T100:f000361:slot3:cc7", "panelPath": "panels/panel_vr00063.png", "panelSha256": "ecdf8778101b872909f9ffd98555197a5ba9b46eb2d936d3ff6f3d376a1188b4"}, {"id": "bs0026", "role": "protection_control", "sampleId": "vr00082", "candidateId": "fill_only_T100:f000474:slot3:cc1", "panelPath": "panels/panel_vr00082.png", "panelSha256": "5b8ce8339aa85c870ccb526a7cb7faff50410d97a44f18b4a028eaca4c179e7f"}];
function field(value='') { return {value, addEventListener() {}}; }
const mockCards = mockDatasets.map(dataset => {
  const fields = {
    '.subtype': field(''), '.control-status': field(dataset.role === 'protection_control' ? 'pending' : ''),
    '.reviewer': field(''), '.reviewed-at': field(''), '.note': field('')
  };
  return {dataset, fields, querySelector(selector) { return fields[selector]; }};
});
const statusElement = {textContent:''};
let exportHandler = null, downloaded = null, lastBlob = null, alerts = [];
const exportButton = {addEventListener(event, handler) { assert.equal(event, 'click'); exportHandler = handler; }};
globalThis.document = {
  getElementById(id) {
    if (id === 'source-meta') return {textContent:JSON.stringify(mockMeta)};
    if (id === 'status') return statusElement;
    if (id === 'export') return exportButton;
    throw new Error(`unexpected id: ${id}`);
  },
  querySelectorAll(selector) {
    if (selector === '.review-card') return mockCards;
    if (selector === 'select,input,textarea') return [];
    throw new Error(`unexpected selector: ${selector}`);
  },
  createElement(tag) {
    assert.equal(tag, 'a');
    return {href:'', download:'', click() {
      downloaded = {download:this.download, text:lastBlob.parts.join('')};
    }};
  }
};
globalThis.Blob = class { constructor(parts, options) { this.parts=parts; this.options=options; } };
globalThis.URL = {createObjectURL(blob) { lastBlob=blob; return 'blob:mock'; }, revokeObjectURL() {}};
globalThis.setTimeout = () => 0;
globalThis.alert = message => alerts.push(String(message));

const ALLOWED = ["shadow", "parking_line_related", "background_change", "other", "uncertain"];
const sourceMeta = JSON.parse(document.getElementById('source-meta').textContent);
const cards = [...document.querySelectorAll('.review-card')];
function collect() {
  const errors = [], ids = new Set(), items = [];
  for (const card of cards) {
    const id = card.dataset.id, role = card.dataset.role;
    const subtype = card.querySelector('.subtype').value;
    const control = card.querySelector('.control-status').value;
    if (ids.has(id)) errors.push(`duplicate id: ${id}`); ids.add(id);
    if (role === 'background_subtype_target' && subtype && !ALLOWED.includes(subtype)) errors.push(`invalid subtype: ${id}`);
    if (role === 'protection_control' && subtype) errors.push(`protection control has subtype: ${id}`);
    const status = role === 'background_subtype_target' ? (subtype ? 'reviewed' : 'pending') : control;
    items.push({
      review_item_id:id, sample_id:card.dataset.sampleId, candidate_id:card.dataset.candidateId,
      review_role:role, source_panel_path:card.dataset.panelPath, source_panel_sha256:card.dataset.panelSha256,
      review_status:status || 'pending', background_subtype:subtype,
      reviewer:card.querySelector('.reviewer').value.trim(), reviewed_at:card.querySelector('.reviewed-at').value,
      review_note:card.querySelector('.note').value.trim()
    });
  }
  const pending = items.filter(x => x.review_status === 'pending').length;
  return {
    schema:'ddr_roi_human_review_v1', schema_version:1,
    source:sourceMeta, exported_at:new Date().toISOString(),
    validation:{valid:errors.length===0, errors, expected_items:sourceMeta.item_count, actual_items:items.length, unique_ids:ids.size},
    summary:{pending, reviewed:items.length-pending}, items
  };
}
function updateStatus() { const r=collect(); document.getElementById('status').textContent=`${r.summary.pending} pending / ${r.summary.reviewed} 已填写`; }
document.querySelectorAll('select,input,textarea').forEach(x=>x.addEventListener('input',updateStatus));
document.getElementById('export').addEventListener('click',()=>{
  const result=collect();
  if (!result.validation.valid) { alert(result.validation.errors.join('\n')); return; }
  const blob=new Blob([JSON.stringify(result,null,2)+'\n'],{type:'application/json'});
  const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='review.json'; a.click();
  setTimeout(()=>URL.revokeObjectURL(a.href),1000); updateStatus();
});


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
assert.ok(downloaded.text.endsWith('\n'));
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
