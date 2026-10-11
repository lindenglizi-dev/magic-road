// Ground48 only. Selection is per image; adopting never signs a review.
globalThis.TeacherBatchCore = (() => {
  function plan(sample, review, selected) {
    if (!review.reviewer.trim()) throw new Error("先填写本图审核人。");
    const wanted = new Set(selected);
    if ([...wanted].some(id => !sample.teacher.some(item => item.candidate_id === id))) throw new Error("选择包含未知候选。");
    const effective = sample.original.map(item => review.actions.find(action => action.target_id === item.target_id) || item)
      .filter(item => item.action !== "D");
    effective.push(...review.actions.filter(item => !sample.original.some(original => original.target_id === item.target_id)));
    const additions = [], skipped = [], overlaps = [];
    const same = (a, b) => a.class === b.class && a.bbox.every((value, i) => value === b.bbox[i]);
    function iou(a, b) {
      const w = Math.max(0, Math.min(a[2], b[2]) - Math.max(a[0], b[0]));
      const h = Math.max(0, Math.min(a[3], b[3]) - Math.max(a[1], b[1]));
      const intersection = w * h;
      return intersection / ((a[2]-a[0])*(a[3]-a[1]) + (b[2]-b[0])*(b[3]-b[1]) - intersection);
    }
    for (const candidate of sample.teacher.filter(item => wanted.has(item.candidate_id))) {
      const target_id = "teacher_" + candidate.candidate_id;
      if (sample.original.some(item => item.target_id === target_id)) throw new Error("候选 ID 与来源框冲突。");
      if (review.actions.some(item => item.target_id === target_id) || effective.some(item => same(item, candidate))) {
        skipped.push(candidate.candidate_id); continue;
      }
      const entry = {target_id, action:"N", class:candidate.class, bbox:candidate.bbox.slice(),
        reason:`人工批量核对采用教师候选 ${candidate.candidate_id}`, ai_assisted:true};
      const errors = globalThis.WorkbenchCore.actionErrors(sample, entry);
      if (errors.length) throw new Error(errors.join("；"));
      if (effective.some(item => item.class === entry.class && iou(item.bbox, entry.bbox) >= 0.5)) overlaps.push(candidate.candidate_id);
      additions.push(entry); effective.push(entry);
    }
    return {additions, skipped, overlaps};
  }
  return {plan};
})();

// UI: inserted inside the existing workbench closure to reuse its draft/actions.
const teacherSelections = new Map();
let teacherEditId = null;
let showDraftBoxes = true;
const batchPanel = document.createElement("section");
batchPanel.innerHTML = `<p class="meta">本图教师候选：全选后可逐个取消。只采用你已核对的框；采用后仍须检查漏检和重复框。</p>
  <div class="actions"><button id="teacherSelectAll">全选本图教师框</button><button id="teacherClear">取消全选</button><button id="teacherAdopt" class="primary">采用所选教师框</button></div>
  <button id="toggleDraftBoxes" aria-pressed="false">隐藏已添加框</button>
  <p id="teacherSelectionCount" class="meta"></p>
  <div id="teacherBatchList" style="max-height:230px;overflow:auto;border:1px solid #ccd5dd;padding:6px"></div>
  <button id="teacherSaveEdit" hidden>保存已采用框的修改（使用坐标/类别/原因栏）</button>`;
$("teacher").parentElement.after(batchPanel);
function batchSelection() {
  if (!teacherSelections.has(sample().image_id)) teacherSelections.set(sample().image_id, new Set());
  return teacherSelections.get(sample().image_id);
}
function renderTeacherBatch() {
  const list = $("teacherBatchList"); list.replaceChildren();
  const selected = batchSelection();
  sample().teacher.forEach(candidate => {
    const row = document.createElement("div"), label = document.createElement("label");
    const checkbox = document.createElement("input"); checkbox.type = "checkbox";
    checkbox.checked = selected.has(candidate.candidate_id);
    checkbox.setAttribute("aria-label", `选择教师框 ${candidate.candidate_id}`);
    checkbox.addEventListener("change", () => {
      teacherEditId = null; $("teacherSaveEdit").hidden = true;
      if (checkbox.checked) selected.add(candidate.candidate_id); else selected.delete(candidate.candidate_id);
      $("teacher").value = candidate.candidate_id; $("teacherDisplay").value = "selected";
      setView("ai"); renderTeacherBatch();
    });
    const adopted = review().actions.find(item => item.target_id === "teacher_" + candidate.candidate_id);
    label.append(checkbox, document.createTextNode(`${candidate.candidate_id} · ${candidate.class} · ${candidate.score.toFixed(3)}${adopted ? " · 已采用" : ""}`));
    row.append(label);
    const locate = document.createElement("button"); locate.textContent = adopted ? "定位/编辑" : "定位";
    locate.addEventListener("click", () => {
      $("original").value = ""; $("teacher").value = candidate.candidate_id;
      $("teacherDisplay").value = "selected"; setView("ai");
      const box = adopted || candidate;
      $("className").value = box.class; $("reason").value = adopted ? adopted.reason : "";
      $("aiAssisted").checked = true; setBox(box.bbox);
      teacherEditId = adopted ? adopted.target_id : null; $("teacherSaveEdit").hidden = !adopted;
    });
    row.append(locate); list.append(row);
  });
  $("teacherSelectionCount").textContent = `本图选中 ${selected.size}/${sample().teacher.length}；选择不等于采用。`;
  $("teacherAdopt").disabled = !selected.size;
}
const drawBeforeBatch = draw;
draw = function () {
  drawBeforeBatch();
  if (view === "raw") return;
  if (showDraftBoxes) review().actions.filter(item => ["N", "I", "M"].includes(item.action)).forEach(item => {
    const teacher = sample().teacher.find(candidate => "teacher_" + candidate.candidate_id === item.target_id);
    drawBox(item.bbox, "#00c8ff", teacher ? `${teacher.candidate_id} ${item.class} 已采用` : "");
  });
  if (view === "ai") sample().teacher.filter(item => batchSelection().has(item.candidate_id))
    .forEach(item => drawBox(item.bbox, "#ff9800", `${item.candidate_id} ${item.class} ${item.score.toFixed(2)}`, [8, 5]));
};
$("toggleDraftBoxes").addEventListener("click", () => {
  showDraftBoxes = !showDraftBoxes;
  $("toggleDraftBoxes").textContent = showDraftBoxes ? "隐藏已添加框" : "显示已添加框";
  $("toggleDraftBoxes").setAttribute("aria-pressed", String(!showDraftBoxes));
  draw();
});
const renderBeforeBatch = render;
render = function () { teacherEditId = null; $("teacherSaveEdit").hidden = true; renderBeforeBatch(); renderTeacherBatch(); };
const decisionsBeforeBatch = renderDecisions;
renderDecisions = function () { decisionsBeforeBatch(); renderTeacherBatch(); draw(); };
["original", "teacher"].forEach(id => $(id).addEventListener("change", () => {
  teacherEditId = null; $("teacherSaveEdit").hidden = true;
}));
$("teacherSelectAll").addEventListener("click", () => {
  sample().teacher.forEach(item => batchSelection().add(item.candidate_id));
  $("teacherDisplay").value = "selected"; setView("ai"); renderTeacherBatch();
});
$("teacherClear").addEventListener("click", () => { batchSelection().clear(); renderTeacherBatch(); draw(); });
$("teacherAdopt").addEventListener("click", () => {
  try {
    const planned = globalThis.TeacherBatchCore.plan(sample(), review(), [...batchSelection()]);
    if (!planned.additions.length) { alert("没有可新增的框：所选候选已采用，或与已有框完全相同。"); return; }
    const warning = planned.overlaps.length ? `\n重叠提示：${planned.overlaps.join(", ")} 与已有同类框 IoU≥0.5，采用后请核对是否重复。` : "";
    if (!confirm(`你已核对所选框的位置和类别，确认采用 ${planned.additions.length} 个教师框？\n跳过 ${planned.skipped.length} 个已采用/完全相同框；不会覆盖已有修改，也不会签署 complete。${warning}`)) return;
    review().actions.push(...planned.additions); markChanged(); renderDecisions(); draw();
  } catch (error) { alert(error.message); }
});
$("teacherSaveEdit").addEventListener("click", () => {
  try {
    const index = review().actions.findIndex(item => item.target_id === teacherEditId);
    if (index < 0) throw new Error("此框已撤销，请重新定位。");
    const label = $("className").value;
    const entry = {...review().actions[index], action:label === "ignore" ? "I" : "N", class:label,
      bbox:readBox(), reason:$("reason").value.trim(), ai_assisted:true};
    const errors = Core.actionErrors(sample(), entry); if (errors.length) throw new Error(errors.join("；"));
    review().actions[index] = entry; markChanged(); renderDecisions();
  } catch (error) { alert(error.message); }
});
