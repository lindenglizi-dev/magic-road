"""CPU-only fixed batch, full-state fork, and fail-closed checks."""
import json
from pathlib import Path
import shutil
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from . import run_person_recovery as recovery
from . import run_road_epoch as segment


class RecoveryTest(unittest.TestCase):
    def test_epoch_boundary_full_state_fork_matches_continuous(self):
        import torch
        from . import train
        from .test_segment_resume import TinyData, TinyLoss, TinyModel, _args, _same
        torch.set_num_threads(1)
        TinyLoss.pause_path, TinyLoss.fail_call = None, 0
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = root / 'dataset.json'
            manifest.write_text('{}')
            rows = [dict(image='tiny', image_sha256='0' * 64)]
            with (patch.object(train, 'load_dataset_manifest', return_value=({}, rows)),
                  patch.object(train, 'make_frame_dataset', side_effect=lambda rows, split, *a, **kw: TinyData(split)),
                  patch.object(train, 'RoadYOLOS4', TinyModel), patch.object(train, 'YOLOXLoss', TinyLoss),
                  patch.object(torch.cuda, 'is_available', return_value=False)):
                continuous = _args(manifest, root / 'continuous', 'cpu')
                continuous.stop_after_epoch = 2
                self.assertEqual(train.train(continuous), 0)
                first = _args(manifest, root / 'first', 'cpu')
                self.assertEqual(train.train(first), 0)
                fork = _args(manifest, root / 'fork', 'cpu')
                fork.output.mkdir()
                fork.resume = fork.output / 'last.pt'
                shutil.copyfile(first.output / 'last.pt', fork.resume)
                fork.stop_after_epoch = 2
                self.assertEqual(train.train(fork), 0)
            a = torch.load(continuous.output / 'last.pt', map_location='cpu', weights_only=False)
            b = torch.load(fork.output / 'last.pt', map_location='cpu', weights_only=False)
            for key in ('model', 'optimizer', 'rng_state', 'scaler', 'trained_steps', 'training_protocol'):
                _same(a[key], b[key])
            self.assertEqual(a['trained_steps'], 4)

    def test_recovery_configuration_and_target_guard(self):
        saved = {name: getattr(segment, name) for name in
                 ('COCO', 'COCO_SHA', 'OUTPUT', 'REPORTS', 'PROTOCOL_SHA')}
        try:
            with patch.object(segment, 'sha256', side_effect=lambda path:
                    segment.NATIVE2_SHA if path == segment.NATIVE2 else segment.ROAD20_SHA):
                with self.assertRaisesRegex(ValueError, 'full state'):
                    segment.configure_person_recovery()
            for args in (['--person-recovery-five'],
                         ['--person-recovery-five', '--stop-after-epoch', '8'],
                         ['--person-ab-arm', 'native', '--stop-after-epoch', '3']):
                with patch.object(segment.sys, 'argv', ['runner'] + args):
                    with self.assertRaises(SystemExit):
                        segment.main()
        finally:
            for name, value in saved.items():
                setattr(segment, name, value)

    def test_only_normal_pause_resumes_and_no_duplicate_batch(self):
        for case in ('success', 'pause', 'error', 'deadline', 'source_change'):
            with tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                run, output = root / 'reports', root / 'output'
                source, baseline = root / 'source.pt', root / 'baseline.json'
                source.write_bytes(b'complete training state')
                baseline.write_text('{}')
                launched = []

                def launch(command, **kwargs):
                    launched.append(command)
                    self.assertIn('--person-recovery-five', command)
                    self.assertEqual(command[command.index('--stop-after-epoch') + 1], '7')
                    self.assertEqual((output / 'last.pt').read_bytes(), source.read_bytes())
                    path = run / 'segments' / f'segment_{len(launched):04d}'
                    path.mkdir(parents=True)
                    pause = case in ('pause', 'deadline') and len(launched) == 1
                    status = 'paused_resumable_segment' if pause else 'completed_target_epoch'
                    report = dict(status=status, recovery_checkpoint_verified=case != 'error',
                        checkpoints={'last.pt': dict(valid=True, epoch=1 if pause else 6)})
                    (path / 'report.json').write_text(json.dumps(report))
                    if pause:
                        (path / 'pause.json').write_text(json.dumps(dict(
                            reason='night_deadline' if case == 'deadline' else 'segment_soft_limit')))
                    kwargs['stdout'].write(json.dumps(dict(report=str(path / 'report.json'))) + '\n')
                    kwargs['stdout'].flush()
                    return SimpleNamespace(pid=123, wait=lambda **_: int(case == 'error'), poll=lambda: 0)

                def evaluate(command, **kwargs):
                    self.assertEqual(command[command.index('--device') + 1], 'cpu')
                    self.assertEqual(command[command.index('--max-images') + 1], '256')
                    Path(command[command.index('--output') + 1]).write_text('{}')
                    if case == 'source_change':
                        (root / 'cnn').mkdir()
                        (root / 'cnn/changed.py').write_text('pass')

                with (patch.object(recovery, 'RUN', run), patch.object(recovery, 'OUTPUT', output),
                      patch.object(recovery, 'ROOT', root), patch.object(recovery, 'SOURCE', source),
                      patch.object(recovery, 'BASELINE', baseline),
                      patch.object(segment, 'sha256', side_effect=lambda path:
                          recovery.BASELINE_SHA if path == baseline else recovery.SOURCE_SHA),
                      patch('torch.load', return_value={}), patch.object(recovery, 'validate_source'),
                      patch.object(recovery.subprocess, 'Popen', side_effect=launch),
                      patch.object(recovery.subprocess, 'run', side_effect=evaluate),
                      patch.object(recovery, 'verify_evaluation'),
                      patch.object(recovery, 'comparison', return_value={})): 
                    self.assertEqual(recovery.main(), int(case in ('error', 'source_change')))
                    state = json.loads((run / 'status.json').read_text())
                    expected = ('stopped_error_no_retry' if case in ('error', 'source_change') else
                                'paused_deadline' if case == 'deadline' else 'completed_epoch7_evaluated')
                    self.assertEqual(state['status'], expected)
                    self.assertEqual(len(launched), 2 if case == 'pause' else 1)
                    with self.assertRaises(FileExistsError):
                        recovery.main()

    def test_candidate_diagnostic_is_not_recall(self):
        truth = dict(image_id='scene/a.jpg', label=0, box=[0, 0, 4, 8])
        result = dict(truth=[truth], predictions=[dict(truth, score=.2)])
        diagnostic = recovery.candidate_diagnostics(result)
        self.assertEqual(diagnostic['groups']['person']['covered_only_below_score_0_5'], 1)
        self.assertEqual(diagnostic['groups']['person/h_le_8']['total'], 1)
        self.assertIn('not detection recall', diagnostic['limitation'])


if __name__ == '__main__':
    unittest.main()
