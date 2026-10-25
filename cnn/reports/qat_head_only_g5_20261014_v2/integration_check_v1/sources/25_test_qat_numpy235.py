"""Static contracts for the NumPy 2.3.5 continuation adapter."""
import unittest

from cnn.hw_validation.production import train_qat_frozen_stem_continue as continuation
from cnn.hw_validation.production import train_qat_numpy235 as adapter


class NumPy235AdapterTests(unittest.TestCase):
    def test_passed_control_and_runtime_are_exactly_bound(self):
        result, receipt, cross = adapter.control_evidence()
        runtime = adapter.native_runtime_identity()
        self.assertTrue(result['passed'])
        self.assertEqual(runtime['numpy_version'], '2.3.5')
        self.assertEqual(runtime['runtime_receipt_sha256'], adapter.RUNTIME_RECEIPT_SHA256)
        self.assertEqual(receipt['runtime']['native_sha256'], runtime['native_sha256'])
        self.assertTrue(cross['passed'])
        self.assertEqual(runtime['cross_runtime_parent_integer_sha256'], adapter.CROSS_RUNTIME_SHA256)
        transition = adapter.expected_cache_receipt()['runtime_transition']
        self.assertEqual((transition['source_numpy'], transition['current_numpy']), ('2.4.6', '2.3.5'))

    def test_install_is_idempotent_and_keeps_parent(self):
        parent = continuation.PARENT
        adapter.install()
        adapter.install()
        self.assertEqual(continuation.PARENT, parent)
        self.assertEqual(continuation.OUT, adapter.OUT)
        self.assertEqual(continuation.RUN, adapter.RUN)
        self.assertEqual(continuation.CHECK_DIR, adapter.CHECK_DIR)
        self.assertEqual(continuation.WORKER_MODULE, adapter.WORKER_MODULE)
        self.assertEqual(continuation.CPU_CHECK_THREADS, 2)
        self.assertIs(continuation.prepare, adapter.prepare)


if __name__ == '__main__':
    unittest.main()
