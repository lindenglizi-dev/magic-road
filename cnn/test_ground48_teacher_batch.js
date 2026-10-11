// CPU-only behavior test; tiny DOM fixture, no browser/package dependency.
const assert = require("node:assert/strict");
const fs = require("node:fs"), path = require("node:path");
const html = fs.readFileSync(path.join(__dirname, "review_workbench.html"), "utf8");
eval(html.match(/<script id="core">([\s\S]*?)<\/script>/)[1]);
const Core = globalThis.WorkbenchCore;
const nodes = new Map();
class Node {
  constructor() { this.children = []; this.events = {}; this.value = ""; this.checked = false; }
  append(...items) { this.children.push(...items); }
  replaceChildren() { this.children = []; }
  after() {}
  setAttribute() {}
  addEventListener(name, handler) { (this.events[name] ||= []).push(handler); }
  fire(name) { (this.events[name] || []).forEach(handler => handler()); }
  set innerHTML(text) { for (const match of text.matchAll(/id="([^"]+)"/g)) nodes.set(match[1], new Node()); }
}
const $ = id => { if (!nodes.has(id)) nodes.set(id, new Node()); return nodes.get(id); };
$("teacher").parentElement = new Node();
const document = {createElement:() => new Node(), createTextNode:text => text};
const frame = {image_id:"f1", width:100, height:80,
  original:[{target_id:"o1", class:"person", bbox:[1,2,10,20]}],
  teacher:[{candidate_id:"t1", class:"person", score:0.9, bbox:[20,10,30,40]},
    {candidate_id:"t2", class:"vehicle", score:0.8, bbox:[40,20,90,60]},
    {candidate_id:"t3", class:"person", score:0.7, bbox:[1,2,10,20]},
    {candidate_id:"t4", class:"person", score:0.6, bbox:[20,11,30,41]}]};
let current = frame, record = {reviewer:"human", actions:[], complete:true, reviewed_at_utc:"old"};
let view = "raw", box = null, approvals = true;
const alerts = [], confirmations = [];
const sample = () => current, review = () => record;
const alert = message => alerts.push(message);
const confirm = message => { confirmations.push(message); return approvals; };
function draw() {}
function render() { renderDecisions(); }
function renderDecisions() {}
function markChanged() { record.complete = false; record.reviewed_at_utc = ""; }
function setView(value) { view = value; draw(); }
function setBox(value) { box = value.slice(); }
function readBox() { return box.slice(); }
const drawn = [];
function drawBox(bbox, color, label) { drawn.push({bbox, color, label}); }
eval(fs.readFileSync(path.join(__dirname, "ground48_teacher_batch.js"), "utf8"));
const Batch = globalThis.TeacherBatchCore;
const untouched = JSON.stringify(record);
assert.throws(() => Batch.plan(frame, {...record, reviewer:""}, ["t1"]), /审核人/);
assert.throws(() => Batch.plan(frame, record, ["unknown"]), /未知/);
const subset = Batch.plan(frame, record, ["t1", "t3"]);
assert.equal(subset.additions.length, 1); assert.deepEqual(subset.skipped, ["t3"]);
assert.equal(subset.additions[0].ai_assisted, true);
assert.equal(JSON.stringify(record), untouched);
assert.throws(() => Batch.plan({...frame, teacher:[{candidate_id:"bad", class:"person", bbox:[0,0,101,20]}]}, record, ["bad"]), /XYXY/);

render(); $("teacherSelectAll").fire("click");
assert.ok(frame.teacher.every(candidate => drawn.some(item => item.label === `${candidate.candidate_id} ${candidate.class} ${candidate.score.toFixed(2)}`)));
assert.match($("teacherSelectionCount").textContent, /4\/4/);
const secondCheckbox = $("teacherBatchList").children[1].children[0].children[0];
secondCheckbox.checked = false; secondCheckbox.fire("change");
assert.match($("teacherSelectionCount").textContent, /3\/4/);
approvals = false; $("teacherAdopt").fire("click");
assert.equal(JSON.stringify(record), untouched);
approvals = true; $("teacherAdopt").fire("click");
assert.deepEqual(record.actions.map(item => item.target_id), ["teacher_t1", "teacher_t4"]);
assert.ok(record.actions.every(item => item.ai_assisted && item.action === "N"));
assert.equal(record.complete, false); assert.equal(record.reviewed_at_utc, "");
assert.ok(drawn.some(item => item.label === "t1 person 已采用"));
assert.match(confirmations.at(-1), /t4/); // overlapping selected pair is reported, not suppressed.
const adopted = JSON.stringify(record.actions);
const beforeToggle = JSON.stringify(record);
drawn.length = 0; $("toggleDraftBoxes").fire("click");
assert.equal($("toggleDraftBoxes").textContent, "显示已添加框");
assert.ok(!drawn.some(item => item.color === "#00c8ff"));
assert.ok(drawn.some(item => item.color === "#ff9800"));
assert.equal(JSON.stringify(record), beforeToggle);
drawn.length = 0; $("toggleDraftBoxes").fire("click");
assert.ok(drawn.some(item => item.label === "t1 person 已采用"));
assert.equal(JSON.stringify(record), beforeToggle);
$("teacherAdopt").fire("click"); assert.equal(JSON.stringify(record.actions), adopted);

// Actual edit button/handler, then re-adopt: preserve manual correction.
$("teacherBatchList").children[0].children[1].fire("click");
box = [21,12,32,42]; $("className").value = "person"; $("reason").value = "人工修正位置";
$("teacherSaveEdit").fire("click");
assert.deepEqual(record.actions[0].bbox, box);
$("teacherAdopt").fire("click"); assert.deepEqual(record.actions[0].bbox, box);
record = JSON.parse(JSON.stringify(record)); // exported action fields survive draft reload.
assert.equal(Batch.plan(frame, record, ["t1"]).additions.length, 0);
assert.ok(record.actions.every(item => Core.actionErrors(frame, item).length === 0));

// Selections never spill to another image; clear does not delete adopted drafts.
current = {...frame, image_id:"f2"}; render();
assert.match($("teacherSelectionCount").textContent, /0\/4/);
current = frame; render(); assert.match($("teacherSelectionCount").textContent, /3\/4/);
$("teacherClear").fire("click"); assert.match($("teacherSelectionCount").textContent, /0\/4/);
assert.equal(record.actions.length, 2);
record.actions.splice(0, 1); renderDecisions(); // same removal path as existing undo.
assert.equal(Batch.plan(frame, record, ["t1"]).additions.length, 1);
console.log("PASS: teacher subset/all/deselect, cancel, validation, exact duplicates, overlap warning, edit/reload/undo, per-image scope, no auto-sign");
