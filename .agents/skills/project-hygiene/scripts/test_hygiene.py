"""Behavior checks in a disposable fixture; no live cache or repository changes."""
import datetime as dt
import json
import os
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch

import hygiene


class HygieneTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Keep the fixture for inspection; no recursive cleanup or deletion loops.
        cls.root = Path(tempfile.mkdtemp(prefix='hygiene-test-'))

    def repository(self, name):
        repo = self.root/name
        repo.mkdir()
        hygiene.git(repo, 'init', '-q')
        return repo

    def test_index_gate_uses_staged_blob_and_allows_rom(self):
        repo = self.repository('index')
        (repo/'required.hex').write_text('12\n', encoding='utf-8')
        hygiene.git(repo, 'add', '--', 'required.hex')
        self.assertTrue(hygiene.staged(repo)['passed'])
        (repo/'large.bin').write_bytes(b'x'*1025)
        hygiene.git(repo, 'add', '--', 'large.bin')
        (repo/'large.bin').write_bytes(b'')
        gate = hygiene.staged(repo, max_bytes=1024)
        self.assertEqual(gate['findings'][0]['bytes'], 1025)

    def test_generated_and_credential_paths_blocked(self):
        repo = self.repository('paths')
        (repo/'artifacts').mkdir()
        (repo/'artifacts/result.txt').write_text('result', encoding='utf-8')
        (repo/'.env').write_text('EXAMPLE_ONLY=yes', encoding='utf-8')
        hygiene.git(repo, 'add', '--', '.env', 'artifacts/result.txt')
        self.assertEqual(len(hygiene.staged(repo)['findings']), 2)

    def test_retention_preserves_pinned_running_unknown_and_recent(self):
        artifacts = self.root/'retention'
        artifacts.mkdir()
        now = time.time()
        for name, status, days, pinned in [('s1','success',8,False), ('s2','success',9,False),
                ('s3','success',10,False), ('f1','failed',8,False), ('f2','failed',9,False),
                ('baseline','success',40,True), ('active','running',40,False),
                ('recent1','failed',1,False), ('recent2','failed',2,False)]:
            folder = artifacts/name
            folder.mkdir()
            marker = {'project_hygiene': 1, 'status': status, 'pinned': pinned,
                      'finished_at': dt.datetime.fromtimestamp(now-days*86400, dt.timezone.utc).isoformat()}
            (folder/'run.json').write_text(json.dumps(marker), encoding='utf-8')
        (artifacts/'manual_data').mkdir()
        (artifacts/'invalid').mkdir()
        (artifacts/'invalid/run.json').write_text('{}', encoding='utf-8')
        candidates = {Path(r['path']).name for r in hygiene.run_candidates(artifacts, now) if r['candidate']}
        self.assertEqual(candidates, {'s3','f1','f2'})
        self.assertTrue((artifacts/'s3/run.json').exists())

    def test_scan_does_not_follow_directory_link(self):
        folder = self.root/'links'
        folder.mkdir()
        outside = self.root/'outside'
        outside.mkdir()
        (outside/'keep.txt').write_text('must remain', encoding='utf-8')
        try:
            (folder/'external').symlink_to(outside, target_is_directory=True)
        except OSError:
            # Verify the Windows reparse-point branch when symlink privilege is absent.
            with patch.object(hygiene, 'linked', return_value=True):
                result = hygiene.measure(folder)
        else:
            result = hygiene.measure(folder)
        self.assertEqual(result['bytes'], 0)
        self.assertTrue(result['links'])
        self.assertEqual((outside/'keep.txt').read_text(encoding='utf-8'), 'must remain')

    def test_scan_records_real_delta_and_keeps_single_report(self):
        repo = self.repository('scan')
        home = self.root/'home'
        cache = home/'.codex'
        cache.mkdir(parents=True)
        (cache/'sample').write_bytes(b'123')
        report_dir = self.root/'report'
        with patch.object(hygiene.Path, 'home', return_value=home), \
             patch.dict(os.environ, {'LOCALAPPDATA': str(home/'local')}):
            hygiene.scan(repo, report_dir)
            (cache/'sample').write_bytes(b'1234567')
            hygiene.scan(repo, report_dir)
        report = json.loads((report_dir/'latest.json').read_text(encoding='utf-8'))
        entry = next(r for r in report['directories'] if r['path']==str(cache))
        self.assertEqual(entry['delta_bytes'], 4)
        self.assertEqual(list(report_dir.iterdir()), [report_dir/'latest.json'])
        self.assertEqual(report['files_deleted'], 0)


if __name__ == '__main__':
    unittest.main()
