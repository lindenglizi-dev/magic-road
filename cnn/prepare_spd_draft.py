"""Bind human suitability review to an editable seven-image draft, not verified GT."""
import argparse
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
import shutil

from .prepare_ground48 import ROOT, read_json, sha256_file, write_json

PILOT = ROOT / 'cnn/reports/replacement48_spd_pilot_20261008_v1'


def validate_review(review, pilot, status):
    if (review.get('schema') != 'spd_pilot_suitability_v1'
            or review.get('archive_sha256') != status['archive_sha256']
            or review.get('complete_gt') is not False
            or not isinstance(review.get('reviewer'), str) or not review['reviewer'].strip()):
        raise ValueError('suitability review schema/archive/reviewer mismatch')
    rows = review.get('reviews', [])
    expected = {row['sample_id']: row for row in pilot}
    if len(rows) != len(expected) or {row['sample_id'] for row in rows} != set(expected):
        raise ValueError('review IDs missing, repeated or unknown')
    for row in rows:
        source = expected[row['sample_id']]
        if row.get('status') not in {'suitable_needs_labels', 'uncertain', 'replace'}:
            raise ValueError('unknown suitability status')
        if any(row.get(key) != source[key] for key in ('image_sha256', 'label_sha256')):
            raise ValueError('review source hash mismatch')
        if not isinstance(row.get('notes'), str):
            raise ValueError('invalid notes')
    return {row['sample_id'] for row in rows if row['status'] == 'suitable_needs_labels'}


def build(review_path, output, include_confirmed=None, van_as_vehicle=False):
    if output.exists():
        raise FileExistsError(output)
    pilot = read_json(PILOT / 'execution_status.json')
    sources = json.loads((PILOT / 'pilot_manifest.json').read_text(encoding='utf-8'))
    accepted = validate_review(read_json(review_path), sources, pilot)
    if include_confirmed is not None:
        if include_confirmed not in {row['sample_id'] for row in sources}:
            raise ValueError('additional scene ID not in verified pilot')
        accepted.add(include_confirmed)
    protected = [PILOT / 'index.html', PILOT / 'pilot_manifest.json', review_path]
    protected += [PILOT / 'raw' / (row['sample_id'] + suffix)
                  for row in sources for suffix in ('.jpg', '.json')]
    before = {str(path): sha256_file(path) for path in protected}
    output.mkdir(parents=True, exist_ok=False)
    (output / 'raw').mkdir()
    shutil.copy2(review_path, output / review_path.name)
    selected = []
    for row in sources:
        if row['sample_id'] not in accepted:
            continue
        for suffix, key in (('.jpg','image_sha256'),('.json','label_sha256')):
            source = PILOT / 'raw' / (row['sample_id'] + suffix)
            if sha256_file(source) != row[key]:
                raise ValueError('pilot raw image/label hash changed')
            shutil.copy2(source, output / 'raw' / source.name)
        row = deepcopy(row)
        if van_as_vehicle:
            for obj in row['objects']:
                if obj['source_type'] == 'Van':
                    obj['proposed_class'] = 'vehicle'
                    obj['requires_review'] = not obj['in_bounds']
            row['issues'] = [issue for issue in row['issues'] if 'Van proposed vehicle mapping' not in issue]
        selected.append(row)
    package = dict(schema='spd_editable_draft_package_v1', archive_sha256=pilot['archive_sha256'],
                   suitability_review_sha256=sha256_file(review_path), samples=selected,
                   complete_gt=False, role='road_development_candidate', trained=False,
                   additional_scene_confirmation=include_confirmed,
                   class_mapping_decisions={'Van':'vehicle'} if van_as_vehicle else {})
    write_json(output / 'draft_manifest.json', package)
    template = (ROOT / 'cnn/spd_draft_ui.html').read_text(encoding='utf-8')
    template = template.replace('7图', f'{len(selected)}图')
    if van_as_vehicle:
        template = template.replace('Van可逐框确认作为vehicle。', 'Van已按用户要求映射为vehicle。')
        template = template.replace('不包含Van和骑行者', '包含Van→vehicle，不包含骑行者')
        template = template.replace('不包含Van、骑行者', '包含Van→vehicle，但不包含骑行者')
        template = template.replace('对Van确认类别；', 'Van已映射vehicle；')
        template = template.replace('${o.source_type}', "${o.source_type==='Van'&&o.proposed_class==='vehicle'?'vehicle':o.source_type}")
    original_ui = (ROOT / 'cnn/review_workbench.html').read_text(encoding='utf-8')
    core = original_ui.split('<script id="core">',1)[1].split('</script>',1)[0]
    page = template.replace('__CORE__', core).replace('__MANIFEST__',
            json.dumps(package, ensure_ascii=False, allow_nan=False).replace('<','\\u003c'))
    with (output / 'index.html').open('x', encoding='utf-8') as handle:
        handle.write(page)
    unchanged = {path: sha256_file(Path(path)) == digest for path, digest in before.items()}
    result = dict(stage='WAIT_HUMAN_LABEL_CORRECTION', accepted_for_scene_review=len(selected),
        uncertain_excluded=[row['sample_id'] for row in sources if row['sample_id'] not in accepted],
        source_objects=sum(len(row['objects']) for row in selected),
        rider_objects=sum(obj['source_type'] in {'Cyclist','Motorcyclist','Tricyclist'}
                          for row in selected for obj in row['objects']),
        van_objects=sum(obj['source_type']=='Van' for row in selected for obj in row['objects']),
        suitability_counts=dict(Counter(row['status'] for row in read_json(review_path)['reviews'])),
        human_verified_gt_count=0, source_files_unchanged=all(unchanged.values()),
        notes='Scene approval only. No inferred split coordinates, no blanket ignore, no training or replacement.',
        converter_sha256=sha256_file(Path(__file__)), ui_template_sha256=sha256_file(ROOT/'cnn/spd_draft_ui.html'))
    write_json(output / 'execution_status.json', result)
    write_json(output / 'protected_files_check.json', dict(baseline_sha256=before, unchanged=unchanged))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--review', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--include-confirmed', help='Additional pilot scene explicitly approved by the user')
    parser.add_argument('--van-as-vehicle', action='store_true', help='User-confirmed Van mapping, without source label changes')
    args = parser.parse_args()
    print(build(args.review, args.output, args.include_confirmed, args.van_as_vehicle))
