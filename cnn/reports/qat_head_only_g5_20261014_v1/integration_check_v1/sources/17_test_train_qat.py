"""Accumulation must preserve YOLOX's whole-update foreground normalization."""
import copy
from types import SimpleNamespace
import unittest

import torch

from cnn.loss import YOLOXLoss
from cnn.hw_validation.production.train_qat import update_once


class TinyHeads(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.heads = torch.nn.ParameterList([
            torch.nn.Parameter(torch.randn(1, 7, size, size) * .1) for size in (4, 2, 1)])

    def forward(self, image):
        return [head.expand(len(image), -1, -1, -1) for head in self.heads]

    def integer_parameters(self):
        return {}


class TrainingTests(unittest.TestCase):
    def test_microbatches_match_complete_22_sample_loss_and_update(self):
        torch.manual_seed(42)
        model = TinyHeads()
        full = copy.deepcopy(model)
        targets = []
        for index in range(22):
            boxes = ([] if index % 3 == 0 else [[1., 1., 8., 14.]]
                     if index % 3 == 1 else [[1., 1., 6., 12.], [9., 1., 15., 14.]])
            targets.append(dict(boxes=torch.tensor(boxes).reshape(-1, 4),
                labels=torch.zeros(len(boxes), dtype=torch.long), ignore_boxes=torch.empty(0, 4)))
        images = torch.zeros(22, 3, 1, 1)
        rows = [dict(teacher_key=str(i), sampling_group='new' if i < 11 else 'replay') for i in range(22)]
        dataset = SimpleNamespace(rows=rows)

        class Window:
            orders = [list(range(22))]

            def set_epoch(self, epoch, mosaic=False):
                pass

            def __getitem__(self, index):
                return images[index], targets[index], str(index)

        optimizer = torch.optim.SGD(model.parameters(), lr=1e-4, momentum=.9, weight_decay=5e-4)
        other = torch.optim.SGD(full.parameters(), lr=1e-4, momentum=.9, weight_decay=5e-4)
        actual = update_once(model, optimizer, dataset, Window(), 0, torch.device('cpu'))
        expected = YOLOXLoss()(full(images), targets)
        expected['loss'].backward()
        norm = torch.nn.utils.clip_grad_norm_(full.parameters(), 10.)
        other.step()
        self.assertAlmostEqual(actual['loss'], float(expected['loss'].detach()), places=5)
        self.assertAlmostEqual(actual['gradient_norm_before_clip'], float(norm), places=5)
        for left, right in zip(model.parameters(), full.parameters(), strict=True):
            torch.testing.assert_close(left, right, atol=1e-7, rtol=1e-6)


if __name__ == '__main__':
    unittest.main()
