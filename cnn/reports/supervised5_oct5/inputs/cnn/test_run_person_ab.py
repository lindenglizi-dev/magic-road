"""CPU-only success/failure checks; no optimizer, GPU, or real training."""
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from . import run_person_ab as runner


class PersonABTest(unittest.TestCase):
    def test_bounded_serial_arms_and_fail_closed(self):
        for case in ('success', 'worker_error', 'source_change'):
            fail = case == 'worker_error'
            with tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                run = root / 'experiment'
                baseline = root / 'baseline.json'
                baseline.write_text(json.dumps(dict(checkpoint_sha256=runner.ROAD20_SHA)))
                launched = []

                def launch(command, **kwargs):
                    arm = command[command.index('--person-ab-arm') + 1]
                    self.assertEqual(command[command.index('--stop-after-epoch') + 1], '2')
                    self.assertIn('--supervisor-pid', command)
                    launched.append(arm)
                    segment = run / arm / 'segment_0001'
                    segment.mkdir(parents=True)
                    report = segment / 'report.json'
                    report.write_text(json.dumps(dict(status='completed_target_epoch',
                                                       recovery_checkpoint_verified=not fail)))
                    kwargs['stdout'].write(json.dumps(dict(report=str(report))) + '\n')
                    kwargs['stdout'].flush()
                    return SimpleNamespace(pid=123, wait=lambda **_: int(fail), poll=lambda: int(fail))

                def evaluate(command, **kwargs):
                    self.assertEqual(command[command.index('--device') + 1], 'cpu')
                    self.assertEqual(command[command.index('--max-images') + 1], '256')
                    output = Path(command[command.index('--output') + 1])
                    output.write_text(json.dumps(dict(diagnostic_metrics_at_0_5={}, p95_operating_points={})))
                    if case == 'source_change':
                        (root / 'cnn').mkdir(exist_ok=True)
                        (root / 'cnn/changed.py').write_text('pass')

                with (patch.object(runner, 'RUN', run), patch.object(runner, 'ROOT', root),
                      patch.object(runner, 'BASELINE', baseline),
                      patch.object(runner, 'sha256', return_value=runner.ROAD20_SHA),
                      patch.object(runner.subprocess, 'Popen', side_effect=launch),
                      patch.object(runner.subprocess, 'run', side_effect=evaluate),
                      patch.object(runner, 'verify_evaluation') as verified):
                    self.assertEqual(runner.main(), int(case != 'success'))
                    state = json.loads((run / 'status.json').read_text())
                    if case != 'success':
                        self.assertEqual(state['status'], 'stopped_error_no_retry')
                        self.assertEqual(launched, ['native'])
                        self.assertEqual(verified.call_count, 0 if fail else 1)
                    else:
                        self.assertEqual(state['status'], 'completed_both_arms')
                        self.assertEqual(launched, ['native', 'mosaic'])
                        self.assertEqual(verified.call_count, 4)
                        self.assertEqual([len(arm['evaluations']) for arm in state['arms'].values()], [2, 2])
                    with self.assertRaises(FileExistsError):
                        runner.main()


if __name__ == '__main__':
    unittest.main()
