"""收口独立数值/协议/负例证据；静态失败与物理边界保持原样。"""
from pathlib import Path
import re

from run_standard_tile import ROOT, PACKAGE, REUSED, sha, read, save


def main():
    numerical=ROOT / 'reports/20261016_010708_294186_all20_random'
    protocol=ROOT / 'reports/20261016_011057_773026_protocol_suite'
    quality=ROOT / 'quality/20261016_011110_498512'
    numeric_receipt=read(numerical / 'summary.json')
    protocol_receipt=read(protocol / 'summary.json')
    assert numeric_receipt['status']=='PASS' and len(numeric_receipt['tests'])==20
    assert protocol_receipt['status']=='PASS' and len(protocol_receipt['tests'])==13
    assert [test['mode'] for test in protocol_receipt['tests']]==list(range(1,13))+[0]
    assert protocol_receipt['tests'][-1]['status']=='PASS_REAL_CHECKER_NEGATIVE'
    snapshot_checks={}
    unchanged_functional={}
    for report,receipt in ((numerical,numeric_receipt),(protocol,protocol_receipt)):
        assert receipt['snapshot_unchanged'] and receipt['original_unchanged']
        snapshot_checks[report.name]=all(sha(report / 'inputs' / p)==value for p,value in receipt['snapshot_sha256'].items())
        assert snapshot_checks[report.name]
        for path,value in receipt['original_sha256'].items():
            p=Path(path)
            if '/verification/' not in p.as_posix():
                assert sha(p)==value,p
                unchanged_functional[path]=value
    metrics=[]
    per_layer={}
    for test in numeric_receipt['tests']:
        marker=next(line for line in test['metrics'] if 'STANDARD_TILE_PASS ' in line)
        fields={key:int(value) for key,value in re.findall(r'(\w+)=(\d+)',marker)}
        metrics.append(fields)
        layer=per_layer.setdefault(str(fields['layer']),dict(tiles=0,cycles=0,groups=0,tasks=0,outputs=0,acc=0,pre=0,silu=0,post=0,byte=0,weight=0,reads=0,parameters=0))
        layer['tiles']+=1
        for key in layer:
            if key!='tiles': layer[key]+=fields[key]
    gate=read(quality / 'gate.json')
    files={str(path.relative_to(ROOT)):sha(path) for path in ROOT.iterdir() if path.is_file() and path.suffix in ('.py','.v','.json') and path.name!='final_summary.json'}
    result=dict(status='PASS_REPRESENTATIVE_BEHAVIORAL_WIF1_FUNCTIONAL_ONLY',numerical_report=str(numerical),protocol_report=str(protocol),
                numerical_tiles=20,protocol_modes=12,real_acc_checker_negative=1,per_layer=per_layer,metrics=metrics,
                snapshot_reverified=snapshot_checks,functional_source_reverified=unchanged_functional,
                public_gates={key:value['status'] for key,value in gate['checks'].items()},
                strict_delivery_ready=gate['delivery_ready'],strict_errors=gate['errors'],strict_warnings=gate['strict_warnings'],
                strict_gate_report=str(quality / 'gate.json'),tool_runtime_sha256=str(quality / 'tool_runtime_sha256.json'),
                tb_spec_generated=True,tb_spec_source_crosscheck=False,
                tb_spec_source_crosscheck_limitation='Formatter source scan misclassifies task inputs as module ports; exact-source failed report preserved; explicit confirmed module spec rendered with supported no-source mode',
                simulation_warnings='12 inherited warnings each elaboration: original owner leaves9 observation outputs unconnected (10messages incl summary); vendor INIT_FILE out-of-bounds part-select2. None suppressed or rewritten.',
                current_verification_files_sha256=files,
                physical_backend_adapter='physical_backend.py self-check PASS; --workstore-source hook prepared but no actual C4 source selected or simulated',
                boundaries=['Behavioral WIF1 has testbench arrays and is not physical4ERAM evidence',
                            '20tiles/4layers; CPU source tensors do not establish actual preceding hardware producer',
                            'No full-layer/sequential-prefix/67layer/DDRx/video/accuracy/FPS acceptance',
                            'No training, TD, production top, bitstream, board, commit or push',
                            'Static strict failures retained; numerical PASS does not make delivery_ready'])
    save(ROOT / 'final_summary.json',result)
    (ROOT / 'handoff.txt').write_text(
        '角色：verify；分支work/roadyolo；仅写本verification目录。\n'
        '状态：四标准层20真实代表tile，12窄协议场景及1真实ACC负例均PASS。\n'
        '数值：逐个WIF请求/响应轨迹、完整源行HWC映射、每MAC组activation/weight/mask/first/last、signed33部分和，最终acc/pre/SiLU/post及输出地址。\n'
        '边界：当前仍为行为WIF1，不证明物理4ERAM、完整层/前缀、DDR、整网、板卡、精度或FPS。\n'
        '复现：python -B verification/run_standard_tile.py --label fresh_name（20tile）；追加--protocol-suite（12协议+1负例）。本地ModelSim在沙箱可能WinError623，已授权本机运行的独立尝试可用。\n'
        '静态：周期图write-spec成功；strict --include-testbench失败原样保留于quality/20261016_011110_498512/gate.json。不要用功能PASS覆盖严格门。\n'
        '工具：preflight依赖/renderer/readiness真实日志、Python/ModelSim/vendor/数值及源码hash在summary；quality绑定skill runtime hash。\n'
        '物理入口：physical_backend.py自检PASS；run_standard_tile.py --workstore-source <合格C4源>可替换同一TB端点，尚未运行。\n'
        '稳定收据：final_summary.json；reports/20261016_010708_294186_all20_random；reports/20261016_011057_773026_protocol_suite。\n',encoding='utf-8')
    print('FINAL_RECEIPT_PASS',sum(x['tasks'] for x in per_layer.values()),sum(x['groups'] for x in per_layer.values()),sum(x['outputs'] for x in per_layer.values()))
    print(result['public_gates'])


if __name__=='__main__':
    main()
