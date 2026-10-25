"""Merge candidate inventories only. This is not a training-data export."""
from collections import Counter
from copy import deepcopy
from pathlib import Path

from cnn.prepare_ac_correction import isolated
from cnn.prepare_ground48 import ROOT, read_json, sha256_file, write_json
from cnn.prepare_virat_ac_expansion import validate_samples

OUT=Path(__file__).resolve().parent
OLD=ROOT/'cnn/reports/ac_pool_inventory_20261011_v1/candidate_pool.json'
BATCHES=[ROOT/'cnn/reports/virat_ac_expand_20261011_v1',OUT]


def main():
    old=read_json(OLD)
    rows=deepcopy([s for s in old['images'] if s['split'] in ('train','dev')])
    inputs=[OLD,Path(__file__)]
    holds=deepcopy(old['region_holds'])
    for directory in BATCHES:
        manifest=read_json(directory/'review_manifest_teacher.json')
        patch=read_json(directory/'ai_visual_patch.json')
        edits=read_json(directory/'assistant_visual_edits.json')
        inputs.extend(directory/n for n in ('review_manifest_teacher.json','ai_visual_patch.json','assistant_visual_edits.json','visual_status.json'))
        for s,r in zip(manifest['samples'],patch['reviews'],strict=True):
            assert s['image_id']==r['image_id'] and not r['complete']
            rows.append(dict(image_id=s['image_id'],split=s['split'],scene=s['scene'],
                family_id=s['family_id'],camera_id=s['camera_id'],source_sha256=s['source_sha256'],
                raw_file_absolute=str(directory/s['raw_file']),width=s['width'],height=s['height'],
                labels=[a for a in r['actions'] if a['action']!='D'],human_signature_valid=False,
                training_eligible=False,source_record=s['source_record'],
                label_draft=str(directory/'ai_visual_patch.json'),
                uncertain_regions=edits['images'][s['legacy_id']].get('uncertain',[])))
    validate_samples(rows,[])
    isolated(rows)
    counts={split:dict(images=sum(s['split']==split for s in rows),
        scenes=dict(Counter(s['scene'] for s in rows if s['split']==split)),
        proposed_boxes=dict(Counter(a['class'] for s in rows if s['split']==split for a in s['labels'])),
        person_bearing_images=sum(s['split']==split and any(a['class']=='person' for a in s['labels']) for s in rows)) for split in ('train','dev')}
    assert counts['train']['images']==128 and counts['dev']['images']==64
    assert counts['train']['scenes']=={'A':96,'C':32} and counts['dev']['scenes']=={'A':48,'C':16}
    for s in rows: assert sha256_file(Path(s['raw_file_absolute']))==s['source_sha256'],s['image_id']
    report=dict(schema='cnn_ac_candidate_pool_v2',status='candidate_count_target_met_GT_still_open',images=rows,counts=counts,
        input_sha256={str(p):sha256_file(p) for p in inputs},prior_region_holds=holds,
        excluded_stress_images=6,excluded_prior_unsigned_images=len(old['pending_unsigned']),
        new_human_assignments=0,human_signed_main_frames=sum(s['human_signature_valid'] for s in rows),
        dataset_frozen=False,complete_GT_published=False,G_ready=False,training_started=False,
        blockers=['Draft completeness/uncertain regions unresolved; teacher/AI drafts are not human GT',
                  'Physical family IDs remain provisional; no claim of full historical training-camera exclusion',
                  'A development includes one straight-road construction camera, not48 independent sites',
                  'No supervision/evaluation mask policy is silently applied to deferred regions'])
    destination=OUT/'candidate_pool_128_64.json'
    if destination.exists(): assert read_json(destination)==report
    else: write_json(destination,report)
    print('PASS192 unique candidate frames,128/64, A96/C32 and A48/C16, split reservations and image hashes')
    print(counts)


if __name__=='__main__': main()
