"""Bounded equivalence checks and timing of frozen-before/current Python code."""
import hashlib
import importlib.util
import json
import platform
import statistics
import sys
import time
from pathlib import Path

import cv2
import numpy as np

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
sys.path[:0] = [str(ROOT/'tools'), str(ROOT/'external_reference_exploration')]
import hog_reference
import candidate_chain_reference
from opencv_hog_diagnostic import read_manifest, assert_safe_path, load_roi
from opencv_hog_candidate_diagnostic import load_models, model_score


def load_before(name):
    spec = importlib.util.spec_from_file_location('before_'+name, OUT/'before'/f'{name}.py')
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def timings(old, new, items):
    # Alternate order over five rounds; compare medians, not a single run.
    elapsed = [[], []]
    for turn in range(5):
        for which in ((0, 1) if turn % 2 == 0 else (1, 0)):
            func = (old, new)[which]
            start = time.perf_counter()
            for item in items:
                func(item)
            elapsed[which].append((time.perf_counter()-start)/len(items))
    before, after = map(statistics.median, elapsed)
    return {'old_ms_per_item':1000*before, 'new_ms_per_item':1000*after,
            'speedup':before/after, 'repeats':5, 'items_per_repeat':len(items)}


old_hog = load_before('hog_reference')
old_chain = load_before('candidate_chain_reference')
dataset = ROOT/'road_roi_dataset_virat'
rows = read_manifest(dataset)
models, _, model_receipt = load_models(ROOT/'external_reference_exploration/results/opencv_hog_diagnostic')
rois, sources = [], {}
for row in rows:
    path = dataset / row['roi_path']
    assert_safe_path(path, 'ROI')
    assert path.resolve().is_relative_to(dataset.resolve())
    roi = load_roi(dataset, row, verify_hash=True).astype(int).tolist()
    before = old_hog.extract_features(roi)
    after = hog_reference.extract_features(roi)
    assert before == after, row['sample_id']
    assert model_score(np.asarray(before[0]), models['current_rtl64']) == model_score(np.asarray(after[0]), models['current_rtl64'])
    rois.append(roi)
    sources[path.relative_to(ROOT).as_posix()] = {'pixel_sha256':row['roi_sha256'], 'file_sha256':digest(path)}

mask_dir = ROOT/'evaluation/local_scene_pilots/intersection_2415171_stage_diagnostic_v1/masks'
stage_rows = json.loads((mask_dir.parent/'frame_stages.json').read_text(encoding='utf-8'))
frozen_top4 = {row['frame_index']:row['stages']['top4']['components'] for row in stage_rows}
masks = []
for path in sorted(mask_dir.glob('*_clean_all.png')):
    mask = (cv2.imread(str(path), cv2.IMREAD_GRAYSCALE) != 0).astype(np.uint8)
    for minimum in (1, 2, 3):
        a = old_chain.filter_short_runs(mask, minimum)
        b = candidate_chain_reference.filter_short_runs(mask, minimum)
        assert np.array_equal(a, b), (path.name, minimum)
        assert old_chain.components(a) == old_chain.components(b)
    frozen = (cv2.imread(str(path.with_name(path.name.replace('_clean_all','_run_all'))), cv2.IMREAD_GRAYSCALE) != 0).astype(np.uint8)
    assert np.array_equal(candidate_chain_reference.filter_short_runs(mask, 2), frozen)
    found = candidate_chain_reference.components(frozen)
    expected = frozen_top4[int(path.name[1:7])]
    assert [(c.area,c.xmin,c.ymin,c.xmax,c.ymax) for c in found] == [(r['area'],*r['analysis_box']) for r in expected]
    masks.append(mask)
    sources[path.relative_to(ROOT).as_posix()] = digest(path)
assert len(rois) == 429 and len(masks) == 32

changed = ['tools/hog_reference.py','tools/candidate_chain_reference.py',
           'tools/local_background_counterfactual.py','tests/test_python_references.py',
           'tests/test_hog_reference.py']
report = {
    'as_of':'2026-10-11', 'python':sys.version, 'platform':platform.platform(),
    'numpy':np.__version__, 'opencv':cv2.__version__,
    'verified_real_rois':len(rois), 'feature_bin_score_mismatches':0,
    'verified_real_masks':len(masks), 'run_lengths_compared':[1,2,3],
    'mask_and_candidate_mismatches':0, 'frozen_run_mask_mismatches':0,
    'frozen_top4_box_area_mismatches':0,
    'hog64':timings(old_hog.extract_features, hog_reference.extract_features, rois),
    'run_filter_default2':timings(old_chain.filter_short_runs, candidate_chain_reference.filter_short_runs, masks),
    'model_receipt':model_receipt, 'data_hashes':sources,
    'source_hashes':{f:digest(ROOT/f) for f in changed},
    'before_hashes':