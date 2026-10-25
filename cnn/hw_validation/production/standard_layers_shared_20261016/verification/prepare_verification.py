"""为独立tile自检生成伴随周期图并实跑包含testbench的八门。"""
from datetime import datetime
import json
import os
from pathlib import Path
import subprocess
import sys

from run_standard_tile import ROOT, PACKAGE, SKILL, sha, read, save


def main():
    target=ROOT / 'quality' / datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    target.mkdir(parents=True)
    temporary=target / 'runtime_tmp'
    temporary.mkdir()
    tb=dict(name='tb_standard_tile_client',rtl_path='tb_standard_tile_client.v',
            clock=dict(name='i_clk',edge='posedge',frequency_mhz=100),
            reset=dict(name='i_rstn',active='low',synchronous=False),
            interfaces=dict(ports=[dict(name='o_test_complete',direction='output',width=1,
                                       role='verification_completion',description='全部真实自检通过后置位')]),
            behavior=['实例化唯一冻结24MAC和动态pre/SiLU/post owner，外部WIF1为明确行为端点',
                      '每通道最多一个未退休事务，随机请求ready与响应延迟，实际握手才推进',
                      '逐个WIF请求轨迹、signed33部分和、最终acc/pre/SiLU/post以及输出字节地址核验'],
            constraints=['数组只在testbench用于行为存储，不代表物理4ERAM',
                         'CPU来源仅证明本层代表tile，未证明实际完整前缀、DDR或整网',
                         '冻结五核接口、II、复位及数值不修改'],
            corner_cases=['四角/内部、H18底部两有效行、mask1尾输出',
                          '非法layer/tile、错误参数身份、取消占有、共同reset未退休请求/响应'],
            verification_cases=['20真实G10参数tile全数值比对','随机反压载荷保持',
                                '实际acc检查器注入1bit负例必须失败','窄协议故障只由共同reset解除'],
            timing_diagrams=[dict(id='retire',title='WIF1请求接受与响应消费分开',scenario='wif_retirement',
                description='请求和响应各自保持至握手，组发射前响应已消费；示意不规定native延迟',
                wavejson=dict(signal=[dict(name='i_clk',wave='p........'),
                                      dict(name='req_valid',wave='01.0.....'),
                                      dict(name='req_ready',wave='0.10.....'),
                                      dict(name='rsp_valid',wave='0...1.0..'),
                                      dict(name='rsp_ready',wave='0....10..'),
                                      dict(name='core_accept',wave='0......10')]))])
    contract=dict(name='standard_tile_verification',modules=[tb])
    save(ROOT / 'tb_contract.json',contract)
    combined=read(PACKAGE / 'spec_input.json')
    combined=dict(name='standard_tile_client_verification',modules=combined.get('modules',[combined])+[tb])
    save(ROOT / 'spec_contract.json',combined)
    commands=[]
    def run(name,argv):
        working_directory=ROOT if name=='spec' else SKILL
        result=subprocess.run(argv,cwd=working_directory,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=360,
                              env=dict(os.environ,PYTHONPATH=str(SKILL),TEMP=str(temporary),TMP=str(temporary)))
        log=target / (name+'.log')
        log.write_text(result.stdout+result.stderr,encoding='utf-8')
        commands.append(dict(argv=argv,cwd=str(working_directory),returncode=result.returncode,log_sha256=sha(log)))
        save(target / 'commands.json',commands)
        print(name,result.returncode,flush=True)
    run('spec',[sys.executable,'-B','-m','scripts.python.workflow.cli','write-spec','--spec',str(ROOT / 'tb_contract.json'),
                '--out-dir',str(ROOT),'--language','zh'])
    run('gate',[sys.executable,'-B','-m','scripts.python.validation.generated_deliverable_gate',str(ROOT / 'tb_standard_tile_client.v'),
                '--include-testbench','--spec',str(ROOT / 'tb_contract.json'),'--json',str(target / 'gate.json'),'--markdown',str(target / 'gate.md')])
    runtime={str(p):sha(p) for p in (SKILL / 'scripts/python').rglob('*.py')}
    for p in (SKILL / 'config').rglob('*.json'):
        runtime[str(p)]=sha(p)
    save(target / 'tool_runtime_sha256.json',runtime)
    print(target)


if __name__=='__main__':
    main()
