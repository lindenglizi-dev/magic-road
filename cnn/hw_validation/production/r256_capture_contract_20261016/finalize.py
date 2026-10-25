"""只封存本候选收据与黄金文件；不重跑旧显示或执行硬件工具。"""
import ast
import json
from pathlib import Path
import sys
import zlib

from self_check import ROOT, digest, save, self_check

manifest = json.loads((ROOT / 'golden_manifest.json').read_text(encoding='utf-8'))
receipt_path = ROOT / manifest['receipt']
receipt = json.loads(receipt_path.read_text(encoding='utf-8'))
assert digest(receipt_path.read_bytes()) == manifest['receipt_sha256']
assert receipt['status'] == 'PASS_CPU_REFERENCE_ONLY' and receipt['frame_cases'] == 9
assert receipt['source_unchanged'] and receipt['inputs_before'] == receipt['inputs_after']
for path, expected in receipt['inputs_before'].items():
    assert digest(Path(path).read_bytes()) == expected, path
assert digest(Path(sys.executable).read_bytes()) == receipt['Python_SHA256']
for path in ROOT.glob('*.py'):
    ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
for case in manifest['cases']:
    directory = ROOT / case['directory']
    assert digest(zlib.decompress((directory / 'source.rgb888.zlib').read_bytes())) == case['source_sha256']
    assert len((directory / 'golden.rgb888').read_bytes()) == 110592
    assert digest((directory / 'golden.rgb888').read_bytes()) == case['RGB_sha256']
    assert digest((directory / 'golden.int8').read_bytes()) == case['INT8_sha256']
cases = {item['name']: ROOT / item['directory'] / 'golden.rgb888' for item in manifest['cases']}
assert cases['numbered'].read_bytes()[:3] == bytes((2, 2, 34))
borders = cases['four_borders'].read_bytes()
assert borders[:3] == borders[-3:] == bytes((51, 51, 10))
colors = cases['colorbars'].read_bytes()
assert colors[:3] == bytes((255, 0, 0)) and colors[32*3:32*3+3] == bytes((0, 255, 0))
try:
    self_check(ROOT.parent)
except ValueError:
    pass
else:
    raise AssertionError('out-of-candidate writes permitted')
save(ROOT / 'source_manifest.json', {
    'candidate': 'RoadYOLO-S4-256-H48',
    'files': {path.name: digest(path.read_bytes()) for path in ROOT.glob('*.py')},
    'interface_contract_sha256': digest((ROOT / 'interface_contract.txt').read_bytes()),
    'input_closure': 'inputs.json', 'input_closure_sha256': digest((ROOT / 'inputs.json').read_bytes()),
    'golden_manifest': 'golden_manifest.json', 'golden_manifest_sha256': digest((ROOT / 'golden_manifest.json').read_bytes()),
    'RTL_files': [], 'new_external_dependencies': [], 'RTL_TD_board_not_run': True})
save(ROOT / 'final_receipt.json', {
    'status': 'PASS_REFERENCE_ARTIFACT_CLOSURE', 'primary_receipt': manifest['receipt'],
    'all_bound_inputs_and_Python_unchanged': True, 'nine_source_RGB_INT8_hashes_verified': True,
    'analytic_numbered_borders_colorbars': 'PASS', 'output_directory_negative_test': 'PASS',
    'Python_AST_parse': 'PASS_NOT_STRICT_SKILL_GATE',
    'previous_display_regression': 'preserved_no_rerun', 'new_RTL_count': 0})
status = json.loads((ROOT / 'status.json').read_text(encoding='utf-8'))
status['sealed'] = True
save(ROOT / 'status.json', status)
save(ROOT / 'artifact_hashes.json', {
    str(path.relative_to(ROOT)): digest(path.read_bytes()) for path in sorted(ROOT.rglob('*'))
    if path.is_file() and path.name != 'artifact_hashes.json'})
print('R256_REFERENCE_SEALED 9frames 995328RGBbytecomparisons; no RTL or hardware claims')
