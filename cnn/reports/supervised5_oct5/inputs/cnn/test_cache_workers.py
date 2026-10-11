"""One CPU regression for memory admission and spawned ordered batch parity."""
import unittest

import torch

from .check_cache_workers import RESERVE, check_loader, enforce_reserve, memory_sample
import psutil


class TinyDataset(torch.utils.data.Dataset):
    epoch = 6

    def __len__(self):
        return 24

    def __getitem__(self, index):
        return (torch.full((3, 2, 2), float(index)),
                dict(boxes=torch.tensor([[0., 0., 1., 1.]]),
                     labels=torch.tensor([index % 2]), ignore_boxes=torch.empty((0, 4))), str(index))


class WorkerCheckTest(unittest.TestCase):
    def test_memory_guard_and_workers0(self):
        with self.assertRaises(MemoryError):
            enforce_reserve(dict(available=RESERVE - 1))
        enforce_reserve(dict(available=RESERVE))
        sample = memory_sample(psutil.Process())
        self.assertGreater(sample['tree_rss'], 0)
        base = check_loader(TinyDataset(), 0, 2, True)
        self.assertEqual(base['consumed_samples'], 16)
        with self.assertRaisesRegex(AssertionError, 'differ'):
            check_loader(TinyDataset(), 0, 1, True, ['wrong'])

    def test_exact_spawn_order(self):
        if psutil.virtual_memory().available < RESERVE + (3 << 30):
            self.skipTest('real workers2/4 require6 GiB available; memory guard is not disabled')
        base = check_loader(TinyDataset(), 0, 2, True)
        for workers in (2, 4):
            result = check_loader(TinyDataset(), workers, 2, True, base['batch_sha256'])
            self.assertEqual(result['keys'], base['keys'])
            self.assertTrue(result['workers_stopped'])
        with self.assertRaisesRegex(AssertionError, 'differ'):
            check_loader(TinyDataset(), 2, 1, True, ['wrong'])


if __name__ == '__main__':
    unittest.main()
