"""Port-checked specification for the single changed module and ROM test."""
import json
import sys

import run

run.check()
work=run.fresh('specifications')
entry=f'import sys;sys.path.insert(0,{str(run.SKILL)!r});from scripts.python.workflow.cli import main;raise SystemExit(main())'
contract=json.loads((run.BASE/'specifications/road_stem_ddr_sequence.json').read_text(encoding='utf-8'))
module=contract['modules'][0]
module['feature']='program_banks'
module['behavior'].append('FETCH沿同时寄存两个4096词bank的返回和cnt_program[12]；之后组合选出原命令字，直到下一FETCH保持，不增加周期。')
module['constraints'].append('Only command storage changes; original arithmetic, mailbox, clock/SDC, FSM and program words remain frozen.')
module['timing_diagrams']=[{'id':'bank_fetch','title':'跨bank取指与保持','scenario':'bank_boundary',
    'description':'FETCH上升沿后返回有效；DECODE消费同一命令，非FETCH时改PC也不得改命令。',
    'wavejson':{'signal':[{'name':'clk','wave':'p.....'},
        {'name':'state','wave':'======','data':['FETCH','DECODE','HOLD','FETCH','DECODE','HOLD']},
        {'name':'PC','wave':'=..=..','data':['4095','4096']},
        {'name':'bank_q','wave':'0..1..'},
        {'name':'command','wave':'=..=..','data':['word4095','word4096']} ]}}]
path=work/'road_stem_ddr_sequence.json'
run.save(path,contract)
run.command([sys.executable,'-B','-X','utf8','-c',entry,'write-spec','--spec',path,
    '--source',run.ROOT/'rtl/road_stem_ddr_sequence.v','--out-dir',run.ROOT/'rtl','--no-state'],run.ROOT,str(work.relative_to(run.ROOT)/'sequence'))
run.save(run.ROOT/'codegen_plan.json',{'task_classes':['modify','validate'],
    'requirements':'requirements.txt','baseline':str(run.BASE),
    'python_model':'prepare.py: two exact 4096-word projections of frozen program.hex',
    'rtl':'rtl/road_stem_ddr_sequence.v','interface_change':False,'latency_change':0,
    'changed_entities':['command ROM arrays','two synchronous returns','registered bank selector','original command bridge'],
    'verification':['8192 words','16384 hold checks','13 unchanged cases','two-clock integration','strict gates','one complete TD run'],
    'gates':['compile','ast','readability','comment','naming','profile','testbench','toolchain'],
    'source_diff':'source_diff.patch','production_delivery':False})
run.check()
print('SEQUENCE_SPEC_PASS')
