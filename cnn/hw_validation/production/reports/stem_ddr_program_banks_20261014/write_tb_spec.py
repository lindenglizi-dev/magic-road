"""Document the portless ROM-only test without inventing external ports."""
import sys
import run

work=run.fresh('testbench_specification')
module={'name':'tb_program_banks','feature':'program_banks','rtl_path':'tb_program_banks.v',
    'description':'只验证实际调度器的双bank ROM，不把force状态的输出当CNN通过。',
    'interfaces':{'ports':[]},'clock':{'signal':'clk internal','period_ns':10},
    'reset':{'signal':'rstn internal','assertion':'Immediate cancellation of transport',
             'release':'Normal integrated regression separately checks full table reload'},
    'behavior':['对全部8192词检查FETCH沿后的命令和选择位。','每词保持两拍，PC翻bank而非FETCH时命令保持。'],
    'constraints':['Simulation only; hierarchical force is never part of synthesizable RTL.'],
    'corner_cases':['4095/4096 boundary, address8191, non-FETCH hold, reset cancellation'],
    'verification_cases':['8192 words, 16384 hold checks, swapped-bank negative case'],
    'timing_diagrams':[{'id':'rom_test','title':'取指测试','scenario':'one_word_hold','description':'每个地址读取后停顿两拍。',
        'wavejson':{'signal':[{'name':'clk','wave':'p...'}, {'name':'FETCH','wave':'10..'},
                              {'name':'command','wave':'=...','data':['expected[address]']} ]}}]}
path=work/'tb_program_banks.json'
run.save(path,{'modules':[module]})
entry=f'import sys;sys.path.insert(0,{str(run.SKILL)!r});from scripts.python.workflow.cli import main;raise SystemExit(main())'
run.command([sys.executable,'-B','-X','utf8','-c',entry,'write-spec','--spec',path,
    '--source',run.ROOT/'tests/tb_program_banks.v','--out-dir',run.ROOT/'tests','--no-state'],run.ROOT,str(work.relative_to(run.ROOT)/'testbench'))
print('BANK_TESTBENCH_SPEC_PASS')
