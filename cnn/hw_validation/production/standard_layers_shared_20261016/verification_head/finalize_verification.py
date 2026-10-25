"""收口修复后唯一owner、31固定层与真实C4的代表tile证据，排除撤回旧owner诊断。"""
import re
from pathlib import Path
from run_standard_tile import ROOT, PACKAGE, CORES, read, save, sha


def main():
    definitions={
        'native_heads105':('013839_322143_native105',105),
        'native_previous4':('013838_735826_nativeold4',4),
        'native_previous6':('013838_806494_nativeold6',6),
        'native_protocol':('013837_329859_nativeproto',13),
        'raw_cancel_after_group':('014056_816020_rawcancel',1),
        'raw_reset_before_output_retirement':('014056_689271_rawoutreset',1),
        'raw_reset_after_group':('014056_509325_rawgrpreset',1),
    }
    reports={}
    metric_groups={}
    current_source_checks={}
    owner_hashes=set()
    raw_totals=dict(outputs=0,wide_outputs=0)
    for name,(folder,count) in definitions.items():
        report=ROOT / 'runs' / folder
        receipt=read(report / 'summary.json')
        assert receipt['status']=='PASS' and len(receipt['tests'])==count,(name,receipt['status'])
        assert receipt['snapshot_unchanged'] and receipt['original_unchanged']
        assert receipt['physical_workstore_selected']
        assert all(sha(report / 'inputs' / p)==digest for p,digest in receipt['snapshot_sha256'].items()),name
        snapshot=report / 'inputs'
        owner_hashes.add(sha(snapshot / 'reused/road_standard_arithmetic_owner.v'))
        owner_binding=read(snapshot / 'owner_binding.json')
        frozen={Path(path).name:digest for path,digest in owner_binding['frozen_sources'].items()}
        for module in CORES:
            assert sha(snapshot / 'reused' / (module+'.v'))==frozen[module+'.v']
        assert sha(snapshot / 'reused/road_feature_workstore.v')=='0d9f78544ce6e726a8ff042d7be0f5a2aee7d717bfbde0495a98a78dea25eb1c'
        gated=read(snapshot / 'owner_gated_regression/status.json')
        assert gated['status']=='PASS_FUNCTION' and gated['case']==21
        compile_command=next(command for command in receipt['commands'] if command['name']=='compile')
        filenames=[Path(arg).name for arg in compile_command['argv'] if arg.endswith('.v')]
        for module in (*CORES,'road_standard_arithmetic_owner','road_standard_tile_client','road_feature_workstore'):
            assert filenames.count(module+'.v')==1
        assert 'road_csp_first_probe.v' not in filenames
        for path,digest in receipt['original_sha256'].items():
            current_source_checks[path]=sha(Path(path))==digest
        if name=='native_protocol':
            assert [test['mode'] for test in receipt['tests']]==list(range(1,13))+[0]
            assert receipt['tests'][-1]['status']=='PASS_REAL_CHECKER_NEGATIVE'
        layers={}
        for test in receipt['tests']:
            nominal=[line for line in test['metrics'] if 'STANDARD_TILE_PASS ' in line]
            if not nominal: continue
            fields={key:int(value) for key,value in re.findall(r'(\w+)=(\d+)',nominal[0])}
            layer=layers.setdefault(str(fields['layer']),dict(tiles=0,cycles=0,groups=0,tasks=0,outputs=0,acc=0,pre=0,silu=0,post=0,byte=0,weight=0,reads=0,parameters=0))
            layer['tiles']+=1
            for key in layer:
                if key!='tiles': layer[key]+=fields[key]
            for marker in test['metrics']:
                if 'STANDARD_TILE_RAW ' in marker and name=='native_heads105':
                    raw={key:int(value) for key,value in re.findall(r'(\w+)=(\d+)',marker)}
                    for key in raw_totals: raw_totals[key]+=raw[key]
        metric_groups[name]=layers
        reports[name]=dict(path=str(report),summary_sha256=sha(report / 'summary.json'),tests=count,snapshot_reverified=True)
    assert len(owner_hashes)==1
    assert all(current_source_checks.values()),[p for p,ok in current_source_checks.items() if not ok]
    heads=metric_groups['native_heads105']
    assert len(heads)==21 and all(layer['tiles']==5 for layer in heads.values())
    old={**metric_groups['native_previous4'],**metric_groups['native_previous6']}
    assert len(old)==10
    head_totals={key:sum(layer[key] for layer in heads.values()) for key in next(iter(heads.values()))}
    assert head_totals['tasks']==22176 and head_totals['groups']==92352
    assert head_totals['pre']==head_totals['outputs']
    assert head_totals['silu']==head_totals['post']==head_totals['outputs']-raw_totals['outputs']
    assert raw_totals['wide_outputs']>0
    quality=ROOT / 'quality/20261016_014043_032197'
    gate=read(quality / 'gate.json')
    result=dict(status='PASS_31_FIXED_SELECTIONS_REPRESENTATIVE_NATIVE_FUNCTIONAL_ONLY',reports=reports,
                native_head_layers=21,native_head_tiles=105,previous_layers_representative=10,total_nominal_tiles=115,
                head_totals=head_totals,raw_int16=raw_totals,per_layer=heads,previous_layer_metrics=old,
                native_protocol_modes=12,real_acc_checker_negative=1,raw_additional_protocol_modes=[13,14,15],
                arithmetic_owner_sha256=next(iter(owner_hashes)),
                arithmetic_owner_qualified_numeric_run='head/owner/runs/20261016_013711_704214_case0',
                arithmetic_owner_qualified_gated_valid_negative_run='head/owner/runs/20261016_013719_886207_case21',
                withdrawn_diagnostic_owner='013418 owner s16first/rawfirst diagnostics excluded because immediate bad-input fault cone was unsafe',
                source_hash_reverified=current_source_checks,
                public_gates={key:value['status'] for key,value in gate['checks'].items()},strict_delivery_ready=gate['delivery_ready'],
                strict_errors=gate['errors'],strict_warnings=gate['strict_warnings'],strict_report=str(quality / 'gate.json'),
                spec=str(ROOT / 'spec/tb_standard_tile_client_spec.md'),runtime_hashes=str(quality / 'tool_runtime_sha256.json'),
                boundaries=['31 fixed layer selections independently sampled:21 heads x5tiles plus10 previous layers x1tile',
                            'All head inputs are controlled synthetic fused-PAN fixtures; no actual PAN/backbone producer or continuous head prefix',
                            'Actual new single owner+five unchanged frozen arithmetic kernels+qualified C4 vendor-native endpoints',
                            'Raw16 equals pre16; no SiLU/post accepted or completed; INT8 compares low8 and independently requires high8 sign extension',
                            'Every source128 request address, backing range, WIF transaction, signed33 group partial,acc/pre/SiLU/post and typed output/address checked',
                            '12096 whole-head cells are CPU reference assets only in this scope; no actual assembler/full prediction producer proven by115 representative tiles',
                            'No physical4ERAM mapping/resource/timing, TD, actual DDR/video, accuracy/FPS, training, production top, bitstream, board, commit or push',
                            'Strict gate failures preserved and not overridden by native functional PASS'])
    save(ROOT / 'final_summary.json',result)
    (ROOT / 'handoff.txt').write_text(
        '角色verify；仅verification_head写入，旧verification/verification_extended及各候选/参考只读。\n'
        '最终采用修复owner013711_case0与同源case21 gated-valid坏输入负例资格；013418两正常诊断撤回最终资格并原样保留。\n'
        '结果：真实C4端点105头tile+31候选旧十层代表10tile全部PASS，native12协议+1真实ACC负例、raw任务cancel/group reset/output未退休reset三项PASS。\n'
        f'头数值：{head_totals["tasks"]}tasks/{head_totals["groups"]}groups/{head_totals["outputs"]}outputs；raw16 {raw_totals["outputs"]}，其中{raw_totals["wide_outputs"]}超出符号扩展INT8范围。\n'
        'INT16原始头全16位逐项比对，pre与输出相等且SiLU/post无交易；INT8低8比对与独立高8符号扩展，不把gold上8为0当DUT错误。\n'
        '覆盖DWstride1 halo36/union15/tail9、mask1/3/7、cls2/reg5尾通道、H18底两行、H72 y68与W128 x124、完整物理source/WIF/输出地址trace。\n'
        '边界：全为独立代表tile，head输入synthetic；不证明实际PAN/backbone/完整头生产者/12096cells组装；不运行TD或声称4ERAM映射/实际时序、DDR、板卡、精度或FPS。\n'
        '规格周期图成功；完整最终native源码闭包strict --include-testbench失败保留quality/20261016_014043_032197/gate.json，真实ModelSim证据另列。\n'
        '详细final_summary.json含全部源/工具/数值hash复核、不可变runs、逐层周期与raw计数；finalize_verification.py可再次复核。\n',encoding='utf-8')
    print('FINAL_HEAD_RECEIPT_PASS',head_totals,raw_totals)
    print(result['public_gates'])


if __name__=='__main__':
    main()
