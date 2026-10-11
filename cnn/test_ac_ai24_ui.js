// Bounded DOM behavior check for the actual generated page; no browser/dependency.
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const directory=path.join(__dirname,'reports/ac_ai_drawn24_20261010_v1');
const html=fs.readFileSync(path.join(directory,'index.html'),'utf8');
const scripts=Object.fromEntries([...html.matchAll(/<script id="([^"]+)"(?: type="[^"]+")?>([\s\S]*?)<\/script>/g)].map(m=>[m[1],m[2]]));
const nodes=new Map(),drawn=[],alerts=[];
class Element {
  constructor() { this.children=[];this.events={};this.value='';this.checked=false;this.style={};this.dataset={};this.classList={toggle(){}};this.parentElement={after(){}}; }
  append(...items) { this.children.push(...items); }
  replaceChildren() { this.children=[]; }
  addEventListener(name,handler) { (this.events[name] ||= []).push(handler); }
  fire(name) { for(const handler of this.events[name]||[]) handler(); }
  setAttribute() {}
  set innerHTML(text) { for(const m of text.matchAll(/id="([^"]+)"/g)) nodes.set(m[1],new Element()); }
}
for(const m of html.matchAll(/id="([^"]+)"/g)) nodes.set(m[1],new Element());
for(const id of ['review-manifest','ai-draft']) nodes.get(id).textContent=scripts[id];
nodes.get('bucket').value='all';nodes.get('zoom').value='1';nodes.get('teacherDisplay').value='selected';
const context={clearRect(){},drawImage(){},save(){},restore(){},setLineDash(){},fillRect(){},fillText(){},measureText:t=>({width:t.length*6}),
  strokeRect:(...box)=>drawn.push(box)};
nodes.get('canvas').getContext=()=>context;
const views=['raw','gt','ai'].map(value=>{const e=new Element();e.dataset.view=value;return e;});
const actions=['A','M','N','I','D'].map(value=>{const e=new Element();e.dataset.action=value;return e;});
global.document={getElementById:id=>nodes.get(id),createElement:()=>new Element(),createTextNode:t=>t,
  addEventListener(){},
  querySelectorAll:selector=>selector==='[data-view]'?views:selector==='[data-action]'?actions:[]};
global.Image=class { constructor(){this.complete=true;this.naturalWidth=720;} set src(value){this._src=value;if(this.onload)this.onload();} };
global.alert=t=>alerts.push(t);global.confirm=()=>true;
vm.runInThisContext(scripts.core);
const anchor='  $("teacherStatus").textContent = ""; rebuildOrder(null);';
assert.equal(scripts['app-script'].split(anchor).length,2);
vm.runInThisContext(scripts['app-script'].replace(anchor,
  'globalThis.state24={reviews,manifest,sample,review,draw,render,view:()=>view};\n'+anchor));
const state=global.state24,first=state.reviews[0];
assert.equal(nodes.get('fatal').hidden,true);assert.equal(state.view(),'gt');
assert.equal(state.reviews.length,24);assert.equal(first.actions.length,2);
assert.equal(first.complete,false);assert.equal(first.reviewer,'1');
assert.equal(nodes.get('completeCount').textContent,'全清单 complete 0/24');
assert.equal(drawn.length>0,true);drawn.length=0;
nodes.get('toggleDraftBoxes').fire('click');assert.equal(drawn.length,0);
nodes.get('toggleDraftBoxes').fire('click');assert.ok(drawn.length>0);
// Actual assistant-added draft: locate, edit using the existing save handler.
const row=nodes.get('decisions').children[0];row.children[0].fire('click');
assert.equal(nodes.get('teacherSaveEdit').hidden,false);
nodes.get('x1').value='306';nodes.get('reason').value='human corrected left edge';
nodes.get('teacherSaveEdit').fire('click');assert.equal(first.actions[0].bbox[0],306);
assert.equal(first.complete,false);assert.equal(first.reviewed_at_utc,'');
views[0].fire('click');drawn.length=0;state.draw();assert.equal(drawn.length,0);
nodes.get('next').fire('click');assert.equal(state.sample().image_id,'mio_00055961');
nodes.get('prev').fire('click');assert.equal(first.actions[0].bbox[0],306);
assert.equal(alerts.length,0);assert.ok(state.reviews.every(r=>!r.complete));
console.log('PASS actual page: draft autoload; default reviewer; RAW; hide/show; edit/save; navigation; no auto-sign');
