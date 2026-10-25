"""独立收口十层候选与真实C4端点回归，明确输入来源及未完成边界。"""
import re
from pathlib import Path
from run_standard_tile import ROOT, PACKAGE, read, save, sha


def main():
    groups={
        'behavior_old20':('012036_488483_old20',20),
        'behavior_new30':('012035_400029_new30',30),
        'native_new30':('012138_973556_native30',30),
        'native_old4':('012139_263840_nativeold4',4),
        'native_protocol':('012323_645238_nativeproto',13),
    }
    reports={}
    metrics={}
    source_checks={}
    for name,(folder,count) in groups.items():
        report=ROOT / 'runs' / folder
        receipt=read(report / 'summary.json')
        assert receipt['status']=='PASS' and len(receipt['tests'])==count,(name,receipt['status'])
        assert receipt['snapshot_unchanged'] and receipt['original_unchanged']
        assert all(sha(report / 'inputs' / path)==digest for path,digest in receipt['snapshot_sha256'].items()),name
        for path,digest in receipt['original_sha256'].items():
            source_checks[path]=sha(Path(path))==digest
        if name=='native_protocol':
            assert [test['mode'] for test in receipt['tests']]==list(range(1,13))+[0]
            assert receipt['tests'][-1]['status']=='PASS_REAL_CHECKER_NEGATIVE'
        per_layer={}
        all_metrics=[]
        for test in receipt['tests']:
            markers=[line for line in test['metrics'] if 'STANDARD_TILE_PASS ' in line]
            if not markers: continue
            fields={key:int(value) for key,value in re.findall(r'(\w+)=(\d+)',markers[0])}
            all_metrics.append(fields)
            layer=per_layer.setdefault(str(fields['layer']),dict(tiles=0,cycles=0,groups=0,tasks=0,outputs=0,acc=0,pre=0,silu=0,post=0,byte=0,weight=0,reads=0,parameters=0))
            layer['tiles']+=1
            for key in layer:
                if key!='tiles': layer[key]+=fields[key]
        metrics[name]=dict(per_layer=per_layer,tiles=all_metrics)
        reports[name]=dict(path=str(report),summary_sha256=sha(report / 'summary.json'),tests=count,
                           snapshot_reverified=True,physical_selected=receipt['physical_workstore_selected'])
    assert all(source_checks.values()),[path for path,ok in source_checks.items() if not ok]
    quality=ROOT / 'quality/20261016_012247_170594'
    gate=read(quality / 'gate.json')
    qualification=read(ROOT / 'c4_qualification.json')
    assert qualification['status']=='PASS_READ_ONLY_C4_FUNCTIONAL_QUALIFICATION'
    provenance={layer['layer_id']:layer.get('input_source',{}) for layer in read(PACKAGE / 'reference_extended/tasks.json')['layers']}
    base_old=metrics['behavior_old20']['per_layer']
    base_new=metrics['behavior_new30']['per_layer']
    totals={key:sum(row[key] for row in [*base_old.values(),*base_new.values()]) for key in ('tiles','cycles','groups','tasks','outputs','acc','pre','silu','post','byte','weight','reads','parameters')}
    result=dict(status='PASS_TEN_FIXED_LAYERS_REPRESENTATIVE_FUNCTIONAL_ONLY',reports=reports,metrics=metrics,
                unique_behavioral_totals=totals,native_tiles=34,native_protocol_modes=12,real_acc_checker_negative=1,
                current_source_hash_reverified=source_checks,c4_qualification=str(ROOT / 'c4_qualification.json'),
                c4_source_sha256=qualification['rtl_sha256'],native_latency_observation=dict(byte_cycles=2,weight_cycles=4,complete_case_pass=False),
                extended_input_provenance=provenance,
                public_gates={key:value['status'] for key,value in gate['checks'].items()},strict_delivery_ready=gate['delivery_ready'],
                strict_errors=gate['errors'],strict_warnings=gate['strict_warnings'],strict_report=str(quality / 'gate.json'),
                gate_source_closure='Actual native-first snapshot: client+sole owner+five frozen kernels+real C4+vendor RAM/GSR+TB',
                spec_period_diagram_generated=True,spec=str(ROOT / 'spec/tb_standard_tile_client_spec.md'),
                runtime_hashes=str(quality / 'tool_runtime_sha256.json'),
                python_script_skills='readable-python-generator/readable-script-generator not available; no installation or strict-pass claim',
                warnings='Behavioral12/native20 inherited elaboration warnings retained: owner observation outputs unconnected and vendor INIT_FILE part-select bounds; no suppression',
                boundaries=['50 unique representative tiles across ten fixed layers, not full layers or a continuous prefix',
                            'New layer46 uses existing CPU real-road tensor;55/64/73 synthetic controlled INT8,65/74 synthetic-derived; all use real frozen G10 parameters',
                            'C4 native functional endpoints consumed in same TB; arrays only independent expected-value scoreboard',
                            'No physical4ERAM resource mapping, TD, whole network, actual DDR/video, accuracy/FPS, headINT16, board or production claim',
                            'Old verification/base candidate/reference read-only throughout; all new attempts retained',
                            'Strict failures are blockers to strict delivery and are not overridden by functional PASS'])
    save(ROOT / 'final_summary.json',result)
    (ROOT / 'handoff.txt').write_text(
        '角色：verify；只写verification_extended，旧verification/base RTL/reference只读。\n'
        '结果：十层替换候选行为旧20+新30全部PASS；真实C4厂商模型WIF1新增30+原四层代表4全部PASS；native12协议+1真实ACC负例PASS。\n'
        f'去重行为计数：{totals["tasks"]}tasks/{totals["groups"]}groups/{totals["outputs"]}outputs，signed33 partial+acc/pre/SiLU/post逐项核验。\n'
        '源服务：真实物理128bit行镜像、合法backing范围与逐请求source address trace；三个concat view不当成连续base。\n'
        'WIF1：逐个请求/响应方向、地址、data轨迹，完整覆盖后读；各通道未退休事务、stalled payload、组/任务/写回/屏障退休一致。\n'
        '数值来源：layer46 CPU真实road SPPF；55/64/73 synthetic、65/74 synthetic-derived；全部real frozen G10 params，无实际连续生产者证明。\n'
        'C4资格：c4_qualification.json核对原始16+封存12hash和case0/1/99；native2/4cycle观察仅部分endpoint观察，不冒充complete_case。\n'
        '物理边界：native功能通过不证明4ERAM资源/布局布线/时序、DDR、整网/精度/FPS；没有运行TD/训练/生产/板卡。\n'
        '规格write-spec周期图成功；完整native源闭包strict --include-testbench失败保留quality/20261016_012247_170594/gate.json，功能PASS不覆盖严格门。\n'
        '复现：run_standard_tile.py --reference-set original/extended --label fresh；native加--workstore-source ../workstore_feature_20261016/storage_frozen/rtl/road_feature_workstore.v；窄协议加--protocol-suite。\n'
        '详细immutable snapshots、commands、tool/vendor/source/numeric hashes、cycles见final_summary.json指向的runs/*/summary.json。\n',encoding='utf-8')
    print('FINAL_EXTENDED_RECEIPT_PASS',totals)
    print(result['public_gates'])


if __name__=='__main__':
    main()
