"""Render the two local interface contracts with the installed spec writer."""
import re
import sys
import run

run.check()
work = run.fresh('specifications')
entry = f'import sys;sys.path.insert(0,{str(run.base.SKILL)!r});from scripts.python.workflow.cli import main;raise SystemExit(main())'
for path in sorted((run.ROOT / 'rtl').glob('*.v')):
    ports = []
    for direction, high, low, name, description in re.findall(
            r'^\s*(input|output|inout)\s*(?:\[(\d+):(\d+)\])?\s*(\w+),?\s*//\s*(.+)$',
            path.read_text(encoding='utf-8'), re.M):
        ports.append({'name': name, 'direction': direction, 'width': abs(int(high)-int(low))+1 if high else 1,
                      'role': description, 'description': description})
    assert ports
    module = {'name':path.stem, 'feature':'ddr_extended_board', 'rtl_path':path.name,
              'description':'固定1056条命令的独占DDR边界与字节掩码自检；临时SRAM诊断。',
              'interfaces':{'ports':ports},
              'clock':{'domains':'DDR user ~133.33MHz; top ref100MHz/pixel75MHz/serial375MHz'},
              'reset':{'assertion':'Async assertion resets requester and entire controller together',
                       'release':'Top two-flop release; requester additionally waits PHY permission'},
              'behavior':['同步ROM读取：FETCH沿读，LOAD沿锁存，ISSUE核对魔数/索引/对齐/范围，然后才发请求。',
                          '1056个合法命令，528写和528读；194地址，两轮别名检查及140组掩码写读。',
                          'AW/W同拍呈现，各自保持至ready；一个读在途，支持AR同拍返回。',
                          '掩码为一保留原字节；128位逐项比较和RLAST正确才计入成功读。',
                          '首错锁定；初始化与核心窗口分别统计；WRITE的both/AW-only/W-only与AR/R等待互斥。',
                          '显示最高两位为状态，四页携带期望、实际和等待计数；冻结payload直到ack，SOF接收。'],
              'constraints':['native地址单位2字节，范围0x1a00000到0x1fffff8；ROM有效字1056、总深度2048、每字192位。',
                             'C_TIMEOUT=27h7ffffff；不从AW/W接受虚构写完成，不赋予CNN输入槽READY语义。',
                             '保留原显示CDC两级与已批准精确首级/7.5ns最大数据延迟处理；无全局false path。'],
              'corner_cases':['独立AW/W背压、即时读返回、错数据/末拍、超时、PHY丢失、异常返回、指令损坏、部分事务中公共复位。'],
              'verification_cases':['24项受控端点计划、完整命令scoreboard、真实TD实现和独立板测。'],
              'timing_diagrams':[{'id':'command_write','title':'命令读取与独立接受','scenario':'split_write',
                  'description':'阶段图非控制器固定延迟；AW先接受时W继续保持，所有请求在ISSUE检查后。',
                  'wavejson':{'signal':[{'name':'clk','wave':'p........'},
                    {'name':'state','wave':'=========','data':['FETCH','LOAD','ISSUE','WRITE','WRITE','WRITE','ADVANCE','FETCH','LOAD']},
                    {'name':'AWVALID','wave':'0..10....'}, {'name':'AWREADY','wave':'0..10....'},
                    {'name':'WVALID','wave':'0..1..0..'}, {'name':'WREADY','wave':'0....10..'},
                    {'name':'payload','wave':'x.=......','data':['address/data/mask held']} ]}}]}
    contract = work / f'{path.stem}.json'
    run.save(contract, {'modules':[module]})
    run.command([sys.executable,'-B','-X','utf8','-c',entry,'write-spec','--spec',contract,
                 '--source',path,'--out-dir',run.ROOT/'rtl','--no-state'],run.ROOT,str(work.relative_to(run.ROOT)/path.stem))
run.check()
