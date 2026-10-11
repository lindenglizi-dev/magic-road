"""CPU checks only, including a deadline stopping one owned dummy process."""
import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import torch

from .benchmark_cache_gpu import (assert_tree_equal, batch_digest, gpu_sample,
                                  stop_reason, tree_cpu, watchdog)


class BenchmarkTest(unittest.TestCase):
    def test_telemetry_and_exact_state_guards(self):
        good = dict(uuid='GPU-test', temperature_c=40, power_w=5,
                    memory_mib=100, total_memory_mib=8192, thermal_slowdown=False)
        self.assertIsNone(stop_reason(good, 10))
        self.assertEqual(stop_reason(good, 295), 'hard_GPU_window_deadline')
        self.assertEqual(stop_reason(dict(good, temperature_c=75), 0),
                         'conservative_temperature_stop')
        self.assertEqual(stop_reason(dict(good, thermal_slowdown=True), 0),
                         'device_thermal_slowdown')
        self.assertEqual(stop_reason(dict(good, system_available_ram_bytes=3 * (1 << 30) - 1), 0),
                         'system_available_RAM_below3_GiB')
        with patch('cnn.benchmark_cache_gpu.subprocess.run') as command:
            command.return_value.stdout = 'GPU-test,40,5,100,8192,Not Active,Not Active\n'
            self.assertEqual(gpu_sample('GPU-test'), good)
            command.return_value.stdout = 'GPU-other,40,5,100,8192,Not Active,Not Active\n'
            with self.assertRaisesRegex(ValueError, 'identity mismatch'):
                gpu_sample('GPU-test')
            command.return_value.stdout = 'GPU-test,40,5,100,8192,N/A,Not Active\n'
            with self.assertRaisesRegex(ValueError, 'unavailable'):
                gpu_sample('GPU-test')
        state = dict(model=torch.tensor([-1., 2.]), optimizer=[dict(momentum=3)], scale=4096)
        snapshot = tree_cpu(state)
        assert_tree_equal(state, snapshot)
        state['model'][0] = 4
        with self.assertRaises(AssertionError):
            assert_tree_equal(state, snapshot)
        trajectory = [tree_cpu(snapshot), tree_cpu(snapshot), tree_cpu(snapshot)]
        changed = tree_cpu(trajectory)
        changed[1]['optimizer'][0]['momentum'] = 4
        with self.assertRaises(AssertionError):
            assert_tree_equal(trajectory, changed)  # A mismatch after step0 must not be ignored.
        images = torch.zeros(1, 3, 2, 2)
        target = dict(boxes=torch.zeros(0, 4), labels=torch.zeros(0, dtype=torch.long),
                      ignore_boxes=torch.zeros(0, 4))
        self.assertNotEqual(batch_digest(images, [target], ['a']),
                            batch_digest(images, [target], ['b']))

    @unittest.skipUnless(os.name == 'nt', 'Windows pinned-process watchdog')
    def test_deadline_only_stops_owned_CPU_dummy(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            dummy = subprocess.Popen([sys._base_executable, '-c', 'import time; time.sleep(30)'],
                                     creationflags=subprocess.CREATE_NO_WINDOW)
            try:
                good = dict(uuid='GPU-test', temperature_c=40, power_w=5,
                            memory_mib=100, total_memory_mib=8192, thermal_slowdown=False)
                with patch('cnn.benchmark_cache_gpu.gpu_sample', return_value=good), \
                        patch('cnn.benchmark_cache_gpu.system_available_ram', return_value=6 * (1 << 30)), \
                        patch('cnn.benchmark_cache_gpu.HARD_SECONDS', 0.1), \
                        contextlib.redirect_stdout(io.StringIO()):
                    watchdog(dummy.pid, 'GPU-test', root / 'failure.json', root / 'telemetry.jsonl')
                self.assertEqual(dummy.wait(timeout=3), 124)
                result = json.loads((root / 'failure.json').read_text())
                self.assertEqual(result['status'], 'stopped_by_watchdog')
                self.assertEqual(result['reason'], 'hard_GPU_window_deadline')
            finally:
                if dummy.poll() is None:
                    dummy.terminate()
                    dummy.wait(timeout=3)

    @unittest.skipUnless(os.name == 'nt', 'Windows pinned-process watchdog')
    def test_watchdog_exception_stops_owned_CPU_dummy(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            dummy = subprocess.Popen([sys._base_executable, '-c', 'import time; time.sleep(30)'],
                                     creationflags=subprocess.CREATE_NO_WINDOW)
            good = dict(uuid='GPU-test', temperature_c=40, power_w=5,
                        memory_mib=100, total_memory_mib=8192, thermal_slowdown=False)
            try:
                with patch('cnn.benchmark_cache_gpu.gpu_sample', return_value=good), \
                        patch('cnn.benchmark_cache_gpu.system_available_ram', return_value=6 * (1 << 30)), \
                        patch('cnn.benchmark_cache_gpu.time.sleep', side_effect=OSError('injected failure')), \
                        contextlib.redirect_stdout(io.StringIO()):
                    with self.assertRaisesRegex(OSError, 'injected failure'):
                        watchdog(dummy.pid, 'GPU-test', root / 'failure.json', root / 'telemetry.jsonl')
                self.assertEqual(dummy.wait(timeout=3), 124)
                self.assertTrue(json.loads((root / 'failure.json').read_text())['reason'].startswith(
                    'watchdog_exception:'))
            finally:
                if dummy.poll() is None:
                    dummy.terminate()
                    dummy.wait(timeout=3)


if __name__ == '__main__':
    unittest.main()
