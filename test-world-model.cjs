const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const html = fs.readFileSync(require('node:path').join(__dirname,'world-model.html'),'utf8');
const sandbox = {};
vm.runInNewContext(html.match(/<script id="world-core">([\s\S]*?)<\/script>/)[1],sandbox);
const W = sandbox.WorldLab;
const lab = W.createLab();
assert.equal(lab.model.search(lab.state),null,'Empty model cannot plan using the real map');
assert.equal(lab.model.predict(lab.state,0),undefined);
assert(W.equal(W.transition(lab.world,{x:4,y:3,key:false},0),{x:4,y:3,key:false}),'Door blocks without key');
assert(W.equal(W.transition(lab.world,{x:4,y:3,key:true},0),{x:5,y:3,key:true}),'Door permits key holder');
assert(W.transition(lab.world,{x:1,y:4,key:false},1).key,'Key is collected');
assert(W.equal(W.transition(lab.world,W.start(),3),W.start()),'Walls block movement');
assert.throws(()=>W.transition(lab.world,W.start(),99));
for (let i=0;i<400;i++) if (!W.explore(lab)) break;
lab.state = W.start();
let plan = lab.model.search(lab.state);
assert(plan?.length,'Exploration learns a route from start');
const learnedLength = plan.length;
for (const action of plan) assert.equal(W.step(lab,action).correct,true);
assert(W.goal(lab.state),'Learned route reaches goal with key');
lab.state = W.start();
lab.world.changed = true;
let mismatches = 0;
for (let i=0;i<100 && !W.goal(lab.state);i++) {
  plan = lab.model.search(lab.state);
  assert(plan?.length,'Model can replan using learned alternate route');
  if (W.step(lab,plan[0]).correct === false) mismatches++;
}
assert.equal(mismatches,1,'Changed wall causes a prediction error before model adapts');
assert(W.goal(lab.state),'Replanning reaches goal after change');
const isolated = new W.Model();
const origin = W.start(), next = {x:2,y:1,key:false};
isolated.observe(origin,0,next); next.x=9;
assert.equal(isolated.predict(origin,0).x,2,'Observations are copied');
const prediction = isolated.predict(origin,0); prediction.x=8;
assert.equal(isolated.predict(origin,0).x,2,'Imagining does not mutate model');
console.log(`PASS: learned ${lab.model.transitions.size} transitions; route ${learnedLength} steps; changed-wall error detected and replanned.`);

// Minimal DOM stand-in exercises the real click handlers; it does not check browser layout.
const element = () => ({textContent:'',disabled:false,dataset:{},children:[],classList:{add(){}},
  append(child){this.children.push(child);},replaceChildren(){this.children=[];},setAttribute(){}});
const actions = Object.fromEntries(['explore','plan','execute','change','home'].map(name=>[name,element()]));
for (const [name,button] of Object.entries(actions)) button.dataset.action=name;
const values = Object.fromEntries(['samples','known','accuracy','detail'].map(name=>[name,element()]));
const boards = {real:element(),model:element()};
let clickHandler, tick;
const root = {
  querySelector(selector){
    const [,type,name] = selector.match(/\[data-(value|action|board)="([^"]+)"\]/);
    return ({value:values,action:actions,board:boards})[type][name];
  },
  querySelectorAll(){return ['plan','change','home'].map(name=>actions[name]);},
  addEventListener(name,handler){clickHandler=handler;}
};
sandbox.document={getElementById:()=>root,createElement:element};
sandbox.window={addEventListener(){}};
sandbox.setInterval=handler=>{tick=handler;return 1;};
sandbox.clearInterval=()=>{tick=null;};
const scripts=[...html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)];
vm.runInNewContext(scripts[1][1],sandbox);
const click = name => clickHandler({target:{closest:()=>actions[name]}});
assert.equal(boards.real.children.length,77);
click('plan'); assert(values.detail.textContent.includes('没有通向目标'));
click('explore'); assert.equal(actions.plan.disabled,true);
for (let i=0;tick && i<200;i++) tick();
assert.equal(tick,null,'Exploration terminates');
click('plan'); assert(values.detail.textContent.includes('16 步'));
assert.equal(actions.execute.disabled,false);
click('change');
let uiMismatch=false;
for(let i=0;i<60 && !actions.execute.disabled;i++){
  click('execute');
  uiMismatch ||= values.detail.textContent.includes('预测失误');
}
assert(uiMismatch,'UI reports changed-world prediction error');
assert(values.detail.textContent.includes('到达终点'));
assert.equal(actions.execute.disabled,true);
click('home'); click('plan'); assert.equal(actions.execute.disabled,false);
console.log('PASS: click handlers explore, plan, detect change, replan, finish and restart without clearing experience.');
