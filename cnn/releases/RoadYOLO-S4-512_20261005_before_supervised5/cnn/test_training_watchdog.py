"""No GPU: telemetry grace, temperature, hard deadline and idempotent pause."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from .training_watchdog import decision, request_pause, valid_sample


class ProtectionTest(unittest.TestCase):
    def test_decisions(self):
        cool = dict(temperature_c=44, thermal_slowdown=False)
        self.assertEqual(decision(None, 10, 5), (None, None))
        self.assertEqual(decision(cool, 15, 0), (None, None))
        self.assertEqual(decision(None, 20, 20)[0], 'pause')
        self.assertEqual(decision(None, 30, 30)[0], 'kill')
        self.assertEqual(decision(cool, 26 * 60, 0), ('pause', 'segment_soft_limit'))
        self.assertEqual(decision(cool, 30 * 60, 0), ('kill', 'hard_segment_deadline'))
        self.assertEqual(decision(dict(cool, temperature_c=75), 10, 0)[0], 'kill')
        self.assertEqual(decision(dict(cool, thermal_slowdown=True), 10, 0)[0], 'kill')
        # Removing the RAM threshold must not change temperature protection.
        self.assertEqual(decision(dict(cool, system_available_ram_bytes=0), 10, 0), (None, None))
        self.assertEqual(decision(cool, 10, 0, 61), (None, None))
        self.assertEqual(decision(cool, 10, 0, 60), ('pause', 'night_deadline'))
        self.assertEqual(decision(cool, 10, 0, 0), ('kill', 'night_deadline'))
        self.assertEqual(decision(dict(cool, temperature_c=75), 10, 0, 60)[0], 'kill')

    def test_invalid_and_pause_signal(self):
        sample = dict(uuid='gpu', temperature_c=44, power_w=10, memory_mib=100,
                      total_memory_mib=8000, thermal_slowdown=False)
        self.assertEqual(valid_sample(sample, 'gpu'), sample)
        with self.assertRaises(ValueError):
            valid_sample(dict(sample, temperature_c=float('nan')), 'gpu')
        with self.assertRaises(ValueError):
            valid_sample(sample, 'other')
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / 'pause.json'
            request_pause(path, 'segment_soft_limit')
            request_pause(path, 'second_reason')
            self.assertEqual(json.loads(path.read_text())['reason'], 'segment_soft_limit')

    @unittest.skipUnless(os.name == 'nt', 'Windows process handle protection')
    def test_owned_cpu_process_and_owner_exit(self):
        from . import training_watchdog as monitor
        sample = dict(uuid='gpu', temperature_c=44, power_w=10, memory_mib=100,
                      total_memory_mib=8000, thermal_slowdown=False)
        for lost_owner, cutoff, lost_supervisor in ((False, False, False), (True, False, False),
                                                    (False, True, False), (False, False, True)):
            with tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                trainer = subprocess.Popen([sys._base_executable, '-B', '-c',
                                            'import time; time.sleep(30)'],
                                           creationflags=subprocess.CREATE_NO_WINDOW)
                owner = subprocess.Popen([sys._base_executable, '-B', '-c',
                                          'import time; time.sleep(0.5)'],
                                         creationflags=subprocess.CREATE_NO_WINDOW) if lost_owner or lost_supervisor else None
                try:
                    with patch.object(monitor, 'gpu_sample', return_value=sample), \
                            patch.object(monitor, 'HARD_SECONDS', 3 if owner else 0.6), \
                            patch.object(monitor.time, 'time', side_effect=[100, 161] if cutoff else None):
                        monitor.watchdog(trainer.pid, owner.pid if lost_owner else os.getpid(),
                                         'gpu', root / 'failure.json', root / 'telemetry.jsonl',
                                         root / 'pause.json',
                                         160.3 if cutoff else None, owner.pid if lost_supervisor else None)
                    trainer.wait(timeout=3)
                    failure = json.loads((root / 'failure.json').read_text())
                    self.assertEqual(failure['reason'], 'night_controller_exited' if lost_supervisor else
                                     'controller_exited' if owner else
                                     'night_deadline' if cutoff else 'hard_segment_deadline')
                    self.assertNotEqual(trainer.returncode, 0)
                finally:
                    for process in (trainer, owner):
                        if process is not None:
                            if process.poll() is None:
                                process.terminate()
                            process.wait(timeout=3)


if __name__ == '__main__':
    unittest.main()
