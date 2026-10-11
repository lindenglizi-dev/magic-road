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
  if (!result.validation.valid) { alert(result.validation.errors.join('
')); return; }
  const blob=new Blob([JSON.stringify(result,null,2)+'
'],{type:'application/json'});
  const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='review.json'; a.click();
  setTimeout(()=>URL.revokeObjectURL(a.href),1000); updateStatus();
});
