"""Fixed-threshold CPU evaluation; never continues training or tunes the recipe."""
import json
import os
from pathlib import Path
import subprocess
import sys

from cnn.metrics import report
from cnn.prepare_ground48 import ROOT, read_json, write_json, sha256_file
from .run import OUT, BASE, RUN, E7, E7_SHA

OLD_BASELINE = ROOT/'cnn/reports/person_native_recovery_20261004/epoch_7_val256.json'
OLD_DATASET = ROOT/'cnn/data/visdrone_vid_train/raw_manifest/dataset.json'
FIELDS = ('precision', 'recall', 'ap50', 'ap50_95')


def compare(baseline, candidate):
    for key in ('truth', 'ignores', 'postprocess_contract', 'dataset_sha256',
                'evaluated_image_content_sha256', 'image_count', 'total_validation_images'):
        assert baseline[key] == candidate[key], key
    result = {}
    for label in ('person', 'vehicle'):
        b = baseline['diagnostic_metrics_at_0_5']['classes'][label]
        c = candidate['diagnostic_metrics_at_0_5']['classes'][label]
        result[label] = dict(E7={k:b[k] for k in FIELDS}, frozen_BN_G10={k:c[k] for k in FIELDS},
                            delta_pp={k:100*(c[k]-b[k]) for k in FIELDS})
    return result


def main():
    execution = read_json(OUT/'execution/report.json')
    assert execution['status'] == 'completed_frozen_BN_G10'
    assert execution['frozen_E7_unchanged'] and execution['original_G10_unchanged'] and execution['source_unchanged']
    assert execution['checkpoint_sha256'] == sha256_file(RUN/'last.pt')
    assert sha256_file(E7) == E7_SHA
    assert sha256_file(OLD_BASELINE) == '501282373e41cdc3a26a3b66f61097c95562878bab8012a0fa588eee18ec1ec8'
    cases = [('e7_control17', E7, BASE/'dataset.json', 17, 4),
             ('development17', RUN/'last.pt', BASE/'dataset.json', 17, 4),
             ('old256_regression', RUN/'last.pt', OLD_DATASET, 256, 2)]
    assert not any((OUT/(name+'.json')).exists() for name, *_ in cases)
    assert not (OUT/'comparison.json').exists() and not (OUT/'结果与下一步.txt').exists()
    env = dict(os.environ, CUDA_VISIBLE_DEVICES='')
    evaluations = {}
    for name, checkpoint, dataset, count, threads in cases:
        command = [sys.executable, '-u', '-B', '-m', 'cnn.evaluate', '--checkpoint', str(checkpoint),
                   '--dataset', str(dataset), '--output', str(OUT/(name+'.json')), '--device', 'cpu',
                   '--threads', str(threads), '--max-images', str(count), '--development-domain']
        print('CPU evaluation: '+name, flush=True)
        subprocess.run(command, cwd=ROOT, env=env, check=True, timeout=600)
        result = evaluations[name] = read_json(OUT/(name+'.json'))
        assert result['image_count'] == count and result['device'] == 'cpu'
        assert result['checkpoint_sha256'] == sha256_file(checkpoint)
    old17 = read_json(BASE/'e7_baseline.json')
    for key in ('predictions', 'truth', 'ignores', 'diagnostic_metrics_at_0_5', 'postprocess_contract'):
        assert evaluations['e7_control17'][key] == old17[key], ('E7 control failed', key)
    main_comparison = compare(evaluations['e7_control17'], evaluations['development17'])
    old_comparison = compare(read_json(OLD_BASELINE), evaluations['old256_regression'])
    gates = dict(person_AP50_gain_at_least_1pp=main_comparison['person']['delta_pp']['ap50'] >= 1,
        person_recall_nondecreasing=main_comparison['person']['delta_pp']['recall'] >= 0,
        vehicle_AP50_drop_at_most_1pp=main_comparison['vehicle']['delta_pp']['ap50'] >= -1,
        old256_AP50_drop_at_most_1pp_each=all(old_comparison[c]['delta_pp']['ap50'] >= -1
                                             for c in ('person', 'vehicle')))
    cameras = {}
    dataset = read_json(BASE/'dataset.json')
    for camera in sorted({r['camera_id'] for r in dataset['images'] if r['split']=='val'}):
        images = {r['image'] for r in dataset['images'] if r['split']=='val' and r['camera_id']==camera}
        cameras[camera] = {}
        for name in ('e7_control17', 'development17'):
            r = evaluations[name]
            parts = [[row for row in r[k] if row['image_id'] in images] for k in ('predictions','truth','ignores')]
            cameras[camera][name] = report(*parts, thresholds=(.5,.5))
    samples = [json.loads(line) for line in (OUT/'execution/segment.telemetry.jsonl').read_text().splitlines()]
    samples = [r for r in samples if 'temperature_c' in r]
    thermal = [execution['initial_gpu'], *samples]
    result = dict(status='completed_and_evaluated', optimizer_updates=10,
        development17=main_comparison, old256=old_comparison, gates=gates, per_camera=cameras,
        numeric_development_gates_pass=all(gates.values()), camera_review_required=True,
        frozen_BN_verification=execution['frozen_BN_verification'], E7_control_reproduced=True,
        GPU_peak_sampled_temperature_c=max(r['temperature_c'] for r in thermal),
        GPU_peak_sampled_memory_mib=max(r['memory_mib'] for r in thermal),
        monitored_seconds=max((r['elapsed_seconds'] for r in samples), default=0),
        automatic_continuation=False, formal_acceptance=False,
        evidence_sha256={name:sha256_file(OUT/(name+'.json')) for name in evaluations},
        old_baseline_sha256=sha256_file(OLD_BASELINE), evaluator_script_sha256=sha256_file(Path(__file__)))
    write_json(OUT/'comparison.json', result)
    lines = ['RoadYOLO 冻结BN小预算实验结果，2026-10-13', '',
        '从冻结E7新建优化器，BN运行统计及仿射参数冻结，LR0.0001；10次更新已完成。',
        '训练22图，8+8+6构成每次更新，实际有效batch22；未追加G100，未蒸馏，未修改RTL。',
        '12个保存点的61层BN共305个张量均与E7逐项相等；优化器仅含73个非BN参数张量。',
        'P/R固定置信度0.5、匹配IoU0.5；AP保留原分数下限约0.05及Top128/每类32框。', '']
    for title, comparisons in (('主开发17图', main_comparison), ('旧256图回归', old_comparison)):
        lines.append(title+'：P / R / AP50 / AP50:95（%）')
        for label, values in comparisons.items():
            b = ' / '.join(f'{100*values["E7"][k]:.2f}' for k in FIELDS)
            c = ' / '.join(f'{100*values["frozen_BN_G10"][k]:.2f}' for k in FIELDS)
            lines.append(f'{label}: E7 {b} → 本次 {c}')
        lines.append('')
    lines += ['门槛：'+json.dumps(gates, ensure_ascii=False),
        '采样GPU最高温度：'+str(result['GPU_peak_sampled_temperature_c'])+'℃；采样显存峰值：'+str(result['GPU_peak_sampled_memory_mib'])+'MiB。',
        '结论：'+('数值开发门槛通过，仍需检查分机位趋势后再决定后续小预算训练。' if all(gates.values()) else
                 '开发继续门槛未通过，保留E7，不用本候选替换，不自动追加训练。'),
        '本次是冻结BN与降低学习率的组合试验，不能独立归因每个改动的贡献。',
        '只属FP32加定点后处理开发结果；17图包含相关帧，旧256是固定子集，均非正式P95/R85验收。',
        '没有执行完整5151图、独立测试、QAT、INT8或板测。原E7和旧G10保持不变。']
    with (OUT/'结果与下一步.txt').open('x', encoding='utf-8') as stream:
        stream.write('\n'.join(lines)+'\n')
    print(json.dumps(result, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
