"""Frozen Stem remains in checkpoints but is excluded from clipping and SGD."""
import unittest
import torch

from cnn.model import RoadYOLOS4
from cnn.hw_validation.production import train_qat as base
from cnn.hw_validation.production.train_qat_frozen_stem import make_model


class FrozenStemTests(unittest.TestCase):
    def test_frozen_parameters_and_optimizer_exclusion(self):
        torch.set_num_threads(2)
        source = RoadYOLOS4().eval()
        source.load_state_dict(torch.load(base.CHECKPOINT, map_location='cpu', weights_only=False)['model'])
        model, optimizer = make_model(source.folded_conv_state(), torch.device('cpu'))
        stem = model.layers[model._layer_index['stem.conv']]
        self.assertFalse(stem.weight.requires_grad)
        self.assertFalse(stem.bias.requires_grad)
        self.assertEqual(len(list(model.parameters())), 132)
        self.assertEqual(len(list(model.named_parameters())), 134)
        before = {key: model.state_dict()[key].clone() for key in ('layers.0.weight', 'layers.0.bias')}
        for parameter in model.parameters():
            parameter.grad = torch.ones_like(parameter)
        torch.nn.utils.clip_grad_norm_(model.parameters(), 10.)
        optimizer.step()
        for key, expected in before.items():
            torch.testing.assert_close(model.state_dict()[key], expected, atol=0, rtol=0)
        self.assertIsNone(stem.weight.grad)
        self.assertIsNone(stem.bias.grad)
        self.assertNotIn(stem.weight, optimizer.state)
        self.assertNotIn(stem.bias, optimizer.state)


if __name__ == '__main__':
    unittest.main()
