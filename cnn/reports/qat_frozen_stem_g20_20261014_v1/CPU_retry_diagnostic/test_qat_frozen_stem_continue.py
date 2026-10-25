"""Contract checks for the fixed G10-to-G20 frozen-Stem continuation."""
import unittest

import torch

from cnn.hw_validation.production import train_qat_frozen_stem_continue as continuation


class FrozenStemContinuationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(2)
        (cls.dataset, cls.window, cls.folded, cls.identity, cls.protocol,
         cls.ancestry, cls.parent) = continuation.prepare()

    def test_parent_and_cycle_two_are_strictly_bound(self):
        self.assertEqual(self.parent['trained_steps'], 10)
        self.assertEqual(len(self.parent['optimizer']['state']), 132)
        self.assertEqual(self.identity['parent_checkpoint_sha256'], continuation.PARENT_SHA256)
        self.assertEqual(self.protocol['schedule_cycle'], 2)
        self.assertEqual(self.protocol['global_qat_updates_after_segment'], 30)
        for global_update in range(10, 20):
            record = continuation.continued_record(self.dataset, self.window, global_update)
            self.assertEqual(record['update'], global_update + 1)
            self.assertEqual(record['schedule_update'], global_update - 9)
            self.assertEqual(record['indices'], list(self.window.orders[global_update - 10]))

    def test_initial_continuation_state_keeps_parent(self):
        model, optimizer = continuation.frozen.make_model(self.folded, torch.device('cpu'))
        continuation.load_state(model, optimizer, self.parent)
        state = continuation.checkpoint(model, optimizer, self.identity, self.protocol,
            self.ancestry, self.parent['sample_history'], candidate=False)
        continuation.validate_state(state, self.identity, self.protocol, self.ancestry,
            self.parent, self.dataset, self.window, candidate=False)
        self.assertEqual(state['trained_steps'], 10)
        self.assertEqual(state['global_qat_updates'], 20)
        self.assertEqual(state['sample_history'], self.parent['sample_history'])


if __name__ == '__main__':
    unittest.main()
