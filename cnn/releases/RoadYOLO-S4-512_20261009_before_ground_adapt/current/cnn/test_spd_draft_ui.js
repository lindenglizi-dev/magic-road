// Actual generated UI handlers with a tiny DOM; no browser/GPU/network.
const fs=require('node:fs'), path=require('node:path'), assert=require('node:assert/strict');
const page=fs.readFileSync(path.join(__dirname,process.argv[2]||'reports/replacement48_spd_draft7_20261008_v1/index.html'),'utf8');
const script=id=>page.match(new RegExp(`<script id="${id}"[^>]*>([\\s\\S]*?)</script>`))[1];
const data=JSON.parse(script('manifest'));
eval(script('core')); eval(script('draft-core'));
const empty={schema:'spd_label_draft_v1',archive_sha256:data.archive_sha256,
  suitability_review_sha256:data.suitability_review_sha256,reviewer:'1',complete_gt:false,
  reviews:data.samples.map(s=>({sample_id:s.sample_id,image_sha256:s.image_sha256,label_sha256:s.label_sha256,notes:'',boxes:[]}))};
assert.ok([7,8].includes(data.samples.length));
assert.equal(data.samples.some(s=>s.sample_id==='spd_inf_010907'),data.samples.length===8);
assert.deepEqual(SpDraftCore.validateDraft(empty,data),empty);
assert.throws(()=>SpDraftCore.validateDraft({...empty,complete_gt:true},data));
const corrupt=JSON.parse(JSON.stringify(empty));corrupt.reviews[0].image_sha256='0'.repeat(64);
assert.throws(()=>SpDraftCore.validateDraft(corrupt,data));
const nodes=new Map();
class Node {constructor(){this.value='';this.children=[];this.textContent='';this.style={};}
 append(o){this.children.push(o);} replaceChildren(){this.children=[];this.value='';}
 getContext(){return {clearRect(){},drawImage(){},strokeRect(){},setLineDash(){},fillRect(){},fillText(){},measureText(){return {width:20};}};}
 getBoundingClientRect(){return {left:0,top:0,width:960,height:540};} setPointerCapture(){} }
const node=id=>{if(!nodes.has(id))nodes.set(id,new Node());return nodes.get(id);};
node('manifest').textContent=JSON.stringify(data);node('zoom').value='0.5';node('reviewer').value='1';node('class').value='person';
const document={getElementById:node,createElement:()=>new Node()};
class Image {set src(value){if(this.onload)this.onload();}}
let approved=true;const alerts=[];const confirm=()=>approved,alert=t=>alerts.push(t);
eval(script('app'));
// Capture real UI records through export validator (without a browser download).
let exported;const validate=SpDraftCore.validateDraft;
SpDraftCore.validateDraft=(value,manifest)=>{exported=validate(value,manifest);return exported;};
const URL={createObjectURL:()=>'',revokeObjectURL(){}};
Node.prototype.click=function(){};
node('adoptDirect').onclick();node('export').onclick();
assert.equal(exported.reviews[0].boxes.length,data.samples[0].objects.filter(o=>o.proposed_class).length);
assert.ok(exported.reviews[0].boxes.every(b=>!['Cyclist','Motorcyclist'].includes(data.samples[0].objects.find(o=>o.source_id===b.source_id).source_type)));
if(data.class_mapping_decisions?.Van==='vehicle'){
 assert.ok(data.samples.every(s=>s.objects.filter(o=>o.source_type==='Van').every(o=>o.proposed_class==='vehicle')));
 assert.ok(exported.reviews[0].boxes.some(b=>data.samples[0].objects.find(o=>o.source_id===b.source_id).source_type==='Van'&&b.class==='vehicle'));
}
const count=exported.reviews[0].boxes.length;
const rider=data.samples[0].objects.find(o=>o.source_type==='Cyclist');
node('source').value=rider.source_id;node('source').onchange();node('adopt').onclick();node('export').onclick();
assert.equal(exported.reviews[0].boxes.length,count);assert.ok(alerts.some(s=>s.includes('骑行者')));
// Draw a human box using source-image coordinates; save stays draft-only.
node('reason').value='人工拆分骑行者人体';
node('canvas').onpointerdown({clientX:100,clientY:100,pointerId:1});
node('canvas').onpointerup({clientX:120,clientY:140,pointerId:1});node('save').onclick();node('export').onclick();
assert.deepEqual(exported.reviews[0].boxes.at(-1).bbox,[200,200,240,280]);
assert.equal(exported.reviews[0].boxes.at(-1).source_id,rider.source_id);
const before=JSON.stringify(exported.reviews);node('drafts').onclick();node('export').onclick();
assert.equal(JSON.stringify(exported.reviews),before);assert.equal(exported.complete_gt,false);
node('frame').value='1';node('frame').onchange();node('export').onclick();
assert.equal(exported.reviews[1].boxes.length,0);
console.log('PASS: seven IDs/hash binding, no GT promotion, direct-only adoption, rider blocked, native drag, hide preserves records, per-frame isolation');
if(data.samples.length===8){
  const old=JSON.parse(JSON.stringify(exported));old.reviews=old.reviews.filter(r=>r.sample_id!=='spd_inf_010907');
  assert.equal(SpDraftCore.validateDraft(old,data).reviews.length,7);
  const bad=JSON.parse(JSON.stringify(old));bad.reviews.pop();assert.throws(()=>SpDraftCore.validateDraft(bad,data));
  node('import').files=[{text:async()=>JSON.stringify(old)}];
  node('import').onchange().then(()=>{
    node('export').onclick();assert.equal(exported.reviews.length,8);
    assert.deepEqual(exported.reviews.slice(0,7),old.reviews);
    assert.deepEqual(exported.reviews[7].boxes,[]);
    console.log('PASS: actual seven-image import preserves edits and appends only the new eighth blank draft');
  }).catch(e=>{console.error(e);process.exitCode=1;});
}
