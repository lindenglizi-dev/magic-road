"""Check actual seven-image package, source approval binding and generated JS."""
import json
import re
import subprocess
from copy import deepcopy
from .prepare_spd_draft import PILOT, ROOT, validate_review
from .prepare_ground48 import read_json

package = ROOT / 'cnn/reports/replacement48_spd_draft7_20261008_v1'
review = read_json(package / 'spd_pilot_review_1791443259202.json')
samples = json.loads((PILOT / 'pilot_manifest.json').read_text(encoding='utf-8'))
status = read_json(PILOT / 'execution_status.json')
assert len(validate_review(review, samples, status)) == 7
for invalid in ('hash', 'duplicate', 'gt'):
    bad = deepcopy(review)
    if invalid == 'hash':
        bad['reviews'][0]['image_sha256'] = '0' * 64
    elif invalid == 'duplicate':
        bad['reviews'][1] = deepcopy(bad['reviews'][0])
    else:
        bad['complete_gt'] = True
    try:
        validate_review(bad, samples, status)
    except ValueError:
        pass
    else:
        raise AssertionError(invalid)
page = (package / 'index.html').read_text(encoding='utf-8')
scripts = re.findall(r'<script id="(?:core|draft-core|app)">(.*?)</script>', page, re.S)
assert len(scripts) == 3
result = subprocess.run(['node', '--check', '-'], input='\n'.join(scripts),
                        text=True, capture_output=True)
assert result.returncode == 0, result.stderr
assert read_json(package / 'draft_manifest.json')['complete_gt'] is False
print('PASS: actual seven scene approvals, hash/duplicate/GT rejection, generated JavaScript syntax')
