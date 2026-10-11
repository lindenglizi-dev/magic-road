"""只发布真实模块接口说明、周期图及当前层源闭包的严格诊断。"""
import json
import shutil
import sys
from execute import HERE, CORE, PROJECT, TOP, check, run, sha, write


def ports(direction, definitions):
    return [dict(name=name, width=int(width), direction=direction, role=name,
                 description=name, clock_domain='i_clk')
            for name, width in (item.split(':') for item in definitions.split())]


def module(name, input_fields, output_fields, behavior, channels):
    return dict(name=name, feature='down2_dynamic_tile', rtl_path=name+'.v',
        description='down2 DW16 stride2 与 PW16→24 固定4×4探针的接口',
        interfaces=dict(protocol='ready_valid', ports=ports('input', input_fields)+ports('output', output_fields),
                        handshake_channels=channels, streams=[]), parameters=[],
        clock=dict(name='i_clk', edge='posedge', frequency_hz=100000000),
        reset=dict(name='i_rstn', active='low', synchronous=False,
                   values='异步取消全部在途任务及装载计数；调用方提供同步释放，重新装满1024项表。'),
        behavior=behavior,
        constraints=['TEST包系数为65536/24与16777216/31；未接真实QAT或运行时参数加载器。',
                     'single in-flight batch；所有消费采用valid与ready握手。'],
        corner_cases=['halo边界取零、完整装载前禁止启动、长反压、结果保持时复位、重新装表后无旧结果。'],
        verification_cases=['640 acc、1920 pre/SiLU/post、640唯一提交、384最终导出；DW256批、PW128批。'],
        timing_diagrams=[dict(id='stall',title='结果反压与接收',scenario='result_stall',
            description='事件示意；运算期间经过多拍，图中省略中间计算拍，不声明固定延迟。',
            wavejson={'signal':[{'name':'i_clk','wave':'p.......'},
                {'name':'input accepted','wave':'010.....'},
                {'name':'compute','wave':'0.1..0..'},
                {'name':'result valid','wave':'0....1.0'},
                {'name':'result ready','wave':'1....01.'},
                {'name':'result payload','wave':'x....=..','data':['held result']}]} )])


def main():
    check()
    layer=HERE/'layer'
    runner=module('down2_dynamic_tile_runner',
        'i_clk:1 i_rstn:1 i_table_valid:1 i_table_addr:10 i_table_data:16 '
        'i_load_valid:1 i_load_kind:3 i_load_addr:11 i_load_data:32 i_start:1 '
        'i_pw_only:1 i_commit_ready:1 i_export_start:1 i_output_ready:1',
        'o_table_ready:1 o_table_loaded:1 o_table_fault:1 o_load_ready:1 o_busy:1 '
        'o_done:1 o_fault:1 o_output_valid:1 o_output_data:8 o_output_index:9 o_export_done:1 '
        'o_debug_valid:1 o_debug_phase:2 o_debug_layer:1 o_debug_position:4 o_debug_channel:5 '
        'o_debug_value:32 o_preload_writes:32 o_core_cycles:32 o_mac_cycles:32 o_pre_cycles:32 '
        'o_silu_cycles:32 o_post_cycles:32 o_writeback_cycles:32 o_storage_wait_cycles:32 '
        'o_scheduler_idle_cycles:32 o_export_cycles:32 o_result_queue_count:2 '
        'o_result_reserved:1 o_meta_count:4 o_mac_result_count:32 o_pre_accept_count:32 '
        'o_silu_accept_count:32 o_post_accept_count:32 o_writeback_count:32',
        ['kind0 halo1296字节；kind2 DW144权重；kind3 DW16偏置；kind4 PW384权重；kind5 PW24偏置。',
         'DW 3空间点MAC结果逐标量送动态核；256次DW提交写内部缓存，PW从该缓存计算。',
         'core_cycles覆盖start接受后busy至全部384个PW写回并done；装表/预载/导出单计。',
         '旧pre/silu/post活动计数来自兼容端口并为零，应使用TB真实状态互斥分类。'],
        [dict(id='load',valid='i_load_valid',ready='o_load_ready',payload=['i_load_kind','i_load_addr','i_load_data']),
         dict(id='export',valid='o_output_valid',ready='i_output_ready',payload=['o_output_data','o_output_index'])])
    adapter=module('road_down2_dynamic_adapter',
        'i_clk:1 i_rstn:1 i_table_valid:1 i_table_addr:10 i_table_data:16 i_input_valid:1 '
        'i_result_data:96 i_result_fault:1 i_layer:1 i_position:4 i_channel_base:5 '
        'i_lane_mask:3 i_output_ready:1',
        'o_table_ready:1 o_table_loaded:1 o_table_fault:1 o_input_ready:1 o_output_valid:1 '
        'o_output_data:8 o_output_tag:16 o_fault:1 o_result_queue_count:2 o_meta_count:4 '
        'o_pre_busy:1 o_silu_busy:1 o_post_busy:1 o_pre_accept:1 o_silu_accept:1 o_post_accept:1',
        ['DW接受单有效lane，PW接受三有效lane；tag={layer,position4,channel5,zeros6}。',
         '一个在途批次；最后有效lane提交后释放pending，输出反压时数据和tag保持。',
         'o_table_fault沿原有聚合故障，不是独立装表故障遥测。',
         '兼容busy/accept六端口固定0，不作为真实活动率；量化核心与原串行接口保持一致。'],
        [dict(id='batch',valid='i_input_valid',ready='o_input_ready',
              payload=['i_result_data','i_result_fault','i_layer','i_position','i_channel_base','i_lane_mask']),
         dict(id='result',valid='o_output_valid',ready='i_output_ready',payload=['o_output_data','o_output_tag'])])
    contract={'modules':[runner,adapter]}
    if (layer/'modules.contract.json').exists():
        assert json.loads((layer/'modules.contract.json').read_text())==contract
    else:
        write(layer/'modules.contract.json',contract)
    suffix='_files' if '--files' in sys.argv else '_host' if '--host' in sys.argv else ''
    spec_out=layer/('spec_verified'+suffix);spec_out.mkdir()
    for item in (runner,adapter):
        spec_path=layer/(item['name']+'.contract.json')
        write(spec_path,{'modules':[item]})
        run([sys.executable,'-B','-X','utf8','-m','scripts.python.workflow.cli','write-spec',
             '--spec',spec_path,'--out-dir',spec_out,'--source',layer/'rtl'/item['rtl_path'],
             '--language','zh'],HERE,item['name']+'_spec'+suffix+'.log')
    shell=json.loads((HERE/'candidate/shell.contract.json').read_text())
    m=shell['modules'][0]
    channels=[dict(id='rx',valid='i_rx_valid',ready='o_rx_ready',payload=['i_rx_data']),
              dict(id='tx',valid='o_tx_valid',ready='i_tx_ready',payload=['o_tx_data'])]
    m['interfaces']['handshake_channels']=channels
    m['interfaces']['streams']=[]
    write(HERE/'candidate/shell_verified.contract.json',shell)
    shell_out=HERE/'candidate/spec_verified';shell_out.mkdir()
    run([sys.executable,'-B','-X','utf8','-m','scripts.python.workflow.cli','write-spec',
         '--spec',HERE/'candidate/shell_verified.contract.json','--out-dir',shell_out,
         '--source',HERE/'candidate/rtl'/TOP,'--language','zh'],HERE,'shell_spec_verified.log')
    gate_inputs=layer/'gate_inputs';gate_inputs.mkdir()
    for source in [*sorted((layer/'rtl').glob('*.v')),*[HERE/'hardware'/n for n in CORE]]:
        shutil.copy2(source,gate_inputs/source.name)
    gate_out=layer/'gate';gate_out.mkdir()
    interface=PROJECT/'cnn/hw_validation/interfaces/ph1p_eram_interface_complete.v'
    code=run([sys.executable,'-B','-X','utf8','-m','scripts.python.validation.generated_deliverable_gate',
        gate_inputs,'--external-interface-source',interface,'--json',gate_out/'gate.json',
        '--markdown',gate_out/'gate.md'],gate_out,'gate.log',allowed=(0,1))
    gate=json.loads((gate_out/'gate.json').read_text())
    write(gate_out/'receipt.json',{'exit_code':code,'errors':gate['errors'],
        'strict_warnings':gate['strict_warnings'],'checks':{k:v['status'] for k,v in gate['checks'].items()},
        'inputs':{str(p):sha(p) for p in gate_inputs.glob('*.v')},'interface_sha256':sha(interface)})
    check()
    print('SPECS_RENDERED_LAYER_GATE',gate['errors'],gate['strict_warnings'],flush=True)


if __name__=='__main__':
    main()
