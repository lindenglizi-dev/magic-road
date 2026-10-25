"""Compare the frozen E7/G10 development reports without tuning thresholds."""
from pathlib import Path
import json

from cnn.metrics import report
from cnn.prepare_ground48 import read_json, write_json, sha256_file

OUT=Path(__file__).resolve().parent


def main():
    baseline=read_json(OUT/'e7_baseline.json')
    candidate=read_json(OUT/'g10_development_matched_order.json')
    execution=read_json(OUT/'execution_attempt2/report.json')
    dataset=read_json(OUT/'dataset.json')
    assert execution['status']=='completed_G10' and execution['completed_updates']==10
    assert baseline['dataset_sha256']==candidate['dataset_sha256']==sha256_file(OUT/'dataset.json')
    assert baseline['truth']==candidate['truth'] and baseline['ignores']==candidate['ignores']
    assert baseline['postprocess_contract']==candidate['postprocess_contract']
    assert candidate['checkpoint_sha256']==execution['checkpoint_sha256']
    comparisons={}
    fields=('precision','recall','ap50','ap50_95')
    for label in ('person','vehicle'):
        b=baseline['diagnostic_metrics_at_0_5']['classes'][label]
        c=candidate['diagnostic_metrics_at_0_5']['classes'][label]
        comparisons[label]=dict(E7={k:b[k] for k in fields},G10={k:c[k] for k in fields},
            delta_percentage_points={k:100*(c[k]-b[k]) for k in fields})
    groups={}
    for camera in sorted({r['camera_id'] for r in dataset['images'] if r['split']=='val'}):
        images={r['image'] for r in dataset['images'] if r['split']=='val' and r['camera_id']==camera}
        groups[camera]={}
        for name,evaluation in (('E7',baseline),('G10',candidate)):
            parts=[[r for r in evaluation[k] if r['image_id'] in images]
                   for k in ('predictions','truth','ignores')]
            groups[camera][name]=report(*parts,thresholds=(.5,.5))
    telemetry=[json.loads(line) for line in (OUT/'execution_attempt2/segment.telemetry.jsonl').read_text().splitlines()]
    samples=[r for r in telemetry if 'temperature_c' in r]
    events=[json.loads(line) for line in (Path(execution['checkpoint']).parent/'train_log.jsonl').read_text().splitlines()]
    steps=[r for r in events if r.get('event')=='step']
    assert len(steps)==10 and max(r['optimizer_steps_completed'] for r in steps)==10
    result=dict(status='G10_completed_and_development_scored',train_images=22,development_images=17,
        optimizer_updates=10,comparisons=comparisons,per_camera=groups,
        peak_GPU_temperature_c=max(r['temperature_c'] for r in samples),
        peak_GPU_memory_mib=max(r['memory_mib'] for r in samples),
        monitored_seconds=max(r['elapsed_seconds'] for r in samples),
        frozen_E7_unchanged=execution['frozen_E7_unchanged'],formal_acceptance=False,
        automatic_continuation=False,old256_regression='not_run_this_turn',
        caveats=['FP32 student plus fixed-point postprocess; not INT8/FPGA evidence.',
                 '17 correlated development frames; not independent formal acceptance.',
                 'Precision/recall at confidence0.5 and matching IoU0.5; AP uses retained score floor0.05.'])
    write_json(OUT/'comparison.json',result)
    print(json.dumps(result,ensure_ascii=False),flush=True)


if __name__=='__main__':
    main()
