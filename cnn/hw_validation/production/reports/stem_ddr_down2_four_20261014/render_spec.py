"""Canonical port-checked specifications and WaveDrom for the new modules."""
import json
import re
import sys
import run

run.check()
work=run.fresh('specifications')
entry=f'import sys;sys.path.insert(0,{str(run.SKILL)!r});from scripts.python.workflow.cli import main;raise SystemExit(main())'
for path in sorted((run.ROOT/'rtl').glob('*.v')):
    if path.stem=='road_paxi_mailbox':
        contract=json.loads((run.ROOT/'mailbox_verification/road_paxi_mailbox_spec.json').read_text(encoding='utf-8'))
    else:
        ports=[]
        for direction,high,low,name,description in re.findall(
                r'^\s*(input|output|inout)\s*(?:signed\s*)?(?:\[(\d+):(\d+)\])?\s*(\w+),?\s*//\s*(.+)$',
                path.read_text(encoding='utf-8'),re.M):
            ports.append({'name':name,'direction':direction,'width':abs(int(high)-int(low))+1 if high else 1,
                          'role':description,'description':description})
        assert ports
        module={'name':path.stem,'feature':'stem_ddr_down2_four','rtl_path':path.name,
                'description':'十六个实际Stem tile经DDR实读后装载down2，末端1536字节逐项核对的一次性诊断。',
                'interfaces':{'ports':ports},'clock':{'domains':'CNN100MHz; DDR133.33MHz; HDMI75/375MHz'},
                'reset':{'assertion':'Entire DDR and arithmetic jointly asserted asynchronously',
                         'release':'Two-flop release in each domain, reload all 1024 SiLU entries before start'},
                'behavior':['固定程序，16个Stem tile、256个唯一写字、289个真实读字、35次补零像素、1536输出字节。',
                            'Stem从原缓存读口导出并先比黄金，实际载荷写DDR；实读先比较，再逐字节装入1296字节halo。',
                            '写响应只表示AW/W接受；一次运行不复用地址或生产槽，不发布READY或通用提交。',
                            '端点周期分十项互斥统计；忙活动可并行，不能相加。',
                            '任何故障终止本轮，首错保持直到整个DDR共同复位。'],
                'constraints':['Read-only ROM initialization is checked separately from board readback.',
                               'No new timing exceptions for mailbox; existing bounded display CDC retained.',
                               'TEST_ONLY coefficients, no deployed-model precision or full CNN FPS claim.'],
                'corner_cases':['Request/response stalls, wrong data, missing response, failure after PASS, reset in every phase.'],
                'verification_cases':['Independent controlled endpoint, actual frozen arithmetic, distinct PAXI mailbox regression, real integrated TD.'],
                'timing_diagrams':[{'id':'once_handoff','title':'一次性交接顺序','scenario':'exclusive_once',
                    'description':'阶段顺序示意；不表示固定DDR返回延迟或写提交。',
                    'wavejson':{'signal':[{'name':'clk','wave':'p........'},
                        {'name':'phase','wave':'=========','data':['TABLE','STEM_LOAD','STEM_RUN','STEM_EXPORT','WRITE_ACCEPT','READ','HALO_LOAD','DW_PW','PASS']},
                        {'name':'req_valid','wave':'0...1.0..'},
                        {'name':'rsp_valid','wave':'0....1.0.'},
                        {'name':'DDR_payload','wave':'x...=....','data':['actual Stem/read data held']} ]}}]}
        contract={'modules':[module]}
    spec=work/f'{path.stem}.json'
    run.save(spec,contract)
    run.command([sys.executable,'-B','-X','utf8','-c',entry,'write-spec','--spec',spec,'--source',path,
                 '--out-dir',run.ROOT/'rtl','--no-state'],run.ROOT,str(work.relative_to(run.ROOT)/path.stem))
run.check()
print('SPECIFICATIONS_PASS')
