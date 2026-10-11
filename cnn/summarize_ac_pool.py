"""Summarize signed A/C candidates, without publishing training GT or starting training."""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from pathlib import Path

from .archive_virat_review import inspect
from .collect_ac_signed import check as check_previous
from .prepare_ac_correction import isolated
from .prepare_ground48 import ROOT, read_json, sha256_file, write_json

OLD = ROOT/'cnn/reports/ac_signed_progress_20261010_v1/reviewed_partial_labels.json'
VIRAT = ROOT/'cnn/reports/virat_review_received_20261010_v2'
SCOPE = ROOT/'cnn/reports/ac_scope_fixed_20261010_v1/scope_decision.json'
OUT = ROOT/'cnn/reports/ac_pool_inventory_20261011_v1'
PATCH = VIRAT/'review_patch_b6741c9a883e_2026-10-10T14-12-09-125Z.json'


def validate_rows(rows):
    assert len(rows) == len({s['image_id'] for s in rows}), 'Duplicate image identity'
    assert len(rows) == len({s['source_sha256'] for s in rows}), 'Duplicate pixels'
    assert all(s['human_signature_valid'] and not s['training_eligible'] for s in rows)
    isolated(rows)  # Logical family reservations only, not physical-camera proof.


def collect():
    previous = check_previous()
    received = inspect(PATCH)
    assert received == read_json(VIRAT/'review_archive.json')
    clarification = read_json(VIRAT/'user_clarification.json')
    assert clarification['patch_sha256'] == received['patch_sha256']
    assert clarification['dataset_id'] == received['dataset_id']
    assert clarification['deleted_regions']['count'] == received['removed_positive_drafts'] == 13
    rows = deepcopy(previous['images'] + received['images'])
    validate_rows(rows)
    assert len(rows) == 42 and not received['pending']
    by_id = {s['image_id']: s for s in rows}
    counts = {}
    for split in ('train', 'dev', 'stress'):
        subset = [s for s in rows if s['split'] == split]
        counts[split] = dict(images=len(subset), scenes=dict(Counter(s['scene'] for s in subset)),
            labels=dict(Counter(a['class'] for s in subset for a in s['labels'])),
            person_bearing_images=sum(any(a['class'] == 'person' for a in s['labels']) for s in subset),
            families=dict(Counter(s['family_id'] for s in subset)))
    region_holds = []
    for change in received['changes']:
        sample = by_id[change['image_id']]
        for kind, regions in (
            ('user_unidentifiable_removed_person', [a['bbox'] for a in change['removed_positive_drafts']]),
            ('source_unresolved_region', [r[:4] for r in change['source_uncertain_regions']]),
        ):
            for box in regions:
                x1, y1, x2, y2 = box
                assert 0 <= x1 < x2 <= sample['width'] and 0 <= y1 < y2 <= sample['height']
                region_holds.append(dict(image_id=sample['image_id'], bbox=box, kind=kind,
                    disposition='hold; do not infer positive or background supervision',
                    source_reference=f"{VIRAT/'review_archive.json'}#/changes/{change['ordinal']-1}"))
    scope = read_json(SCOPE)['current_round']
    gaps = {split: dict(images=scope[key]-counts[split]['images'], scenes={
        scene: scope[f'{key}_{scene}']-counts[split]['scenes'].get(scene, 0) for scene in ('A', 'C')})
        for split, key in (('train', 'train'), ('dev', 'development'))}
    inputs = [OLD, VIRAT/'review_archive.json', VIRAT/'user_clarification.json', PATCH, SCOPE, Path(__file__)]
    return dict(schema='cnn_ac_candidate_pool_inventory_v1', date_local='2026-10-11',
        status='blocked_pilot_size_completeness_and_camera_evidence', images=rows, counts=counts,
        pending_unsigned=previous['pending'], candidate_count_gaps=gaps,
        region_holds=region_holds, region_hold_coverage='latest VIRAT batch only; not exhaustive pool masks',
        input_sha256={str(p): sha256_file(p) for p in inputs},
        human_review_records_received=42, new_human_assignments=0, original_workload_cap_unchanged=True,
        dataset_frozen=False, complete_GT_published=False, G_ready=False, training_started=False,
        physical_camera_mapping_fully_verified=False, main_dev_E7_baseline_started=False,
        blockers=['128 train / 64 dev target not reached; candidate counts do not certify complete GT',
            'Only 11 person boxes in main training candidates; 6 new parking frames contain no person boxes',
            'MIO camera identities unresolved; new VIRAT physical camera mapping remains provisional',
            'Removed/unresolved regions need deployment of supervision exclusions before dataset publication',
            'Neighbouring video frames do not inherit reviewed complete labels',
            'Courtyard remains auxiliary; no automatic promotion to A/C'],
        next_decision='Retain scope and authorize bounded source expansion, or explicitly revise to a smaller diagnostic-only experiment')


def check():
    result = collect()
    assert [result['counts'][s]['images'] for s in ('train', 'dev', 'stress')] == [31, 5, 6]
    assert result['counts']['train']['labels'] == {'person': 11, 'vehicle': 153}
    assert result['counts']['dev']['labels'] == {'person': 14, 'vehicle': 63, 'ignore': 2}
    assert result['counts']['stress']['labels'] == {'person': 17, 'vehicle': 3}
    assert result['candidate_count_gaps'] == {'train': {'images': 97, 'scenes': {'A': 79, 'C': 18}},
                                             'dev': {'images': 59, 'scenes': {'A': 47, 'C': 12}}}
    assert Counter(r['kind'] for r in result['region_holds']) == {
        'user_unidentifiable_removed_person': 13, 'source_unresolved_region': 12}
    try:
        validate_rows(result['images'] + [result['images'][0]])
    except AssertionError:
        pass
    else:
        raise AssertionError('Duplicate row accepted')
    if (OUT/'candidate_pool.json').exists():
        assert read_json(OUT/'candidate_pool.json') == result
    print('PASS: signed hashes/coordinates, unique identities, split reservations, counts/gaps, not-ready state')
    return result


def build():
    assert not OUT.exists(), 'Preserve existing inventory; run check instead'
    result = check()
    OUT.mkdir()
    write_json(OUT/'candidate_pool.json', result)
    report = '''A/C 已审核候选数据汇总（2026-10-11）

当前位置：步骤2，整理训练/开发候选；尚未冻结可训练数据。
主训练候选31张：A17、C14；person 11框、vehicle 153框，9张含人。
主开发候选5张：A1、C4；person 14框、vehicle 63框、ignore 2框。
庭院辅助6张：person 17框、vehicle 3框，不默认加入A/C主训练。
合计42张已完成人工确认；另2张旧草稿未签署，不导入，不追加审核任务。

原约定目标：训练128张（A96/C32）、开发64张（A48/C16）。
候选数量仍缺：训练97张（A79/C18）、开发59张（A47/C12）。
这只是数量差额；已审核候选也不等于完整GT及机位隔离已通过。

本次12张VIRAT已经收到，无需重审。删除的13个人框保留删除，
按用户“无法辨认为人”的说明保留监督排除要求，不加回、不认作确定背景。
新停车场6张另有12条来源不确定区域记录；仅登记待排除/处理区域，
本次没有生成训练掩码，也没有将它们自动签署为ignore真值。
相邻帧不继承完整标注。MIO机位未明确；VIRAT新机位归属仍为暂定。

下一步决策：
建议保留原规模，先授权一次有上限的数据扩充任务，给出总量和来源，
先AI补框，不逐批追加人工工作；若仍不能闭合完整标注，则报告不足。
若要使用更小数据做诊断，需要明确修改实验范围；31/5不能冒充泛化验证，
也不能跳过不确定区域处理。当前不启动G100、不做E7新主开发基线。
本次只发布候选汇总清单；模型、训练缓存、原审核文件、验收口径和RTL不变。
'''
    with (OUT/'数据汇总与下一步.txt').open('x', encoding='utf-8') as stream:
        stream.write(report)
    check()
    print(OUT)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('build', 'check'))
    globals()[parser.parse_args().action]()
