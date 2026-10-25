import copy
import unittest

import torch

from cnn.hw_validation.production import train_qat as base
from cnn.hw_validation.production import train_qat_frozen_stem_continue as continuation
from cnn.hw_validation.production import train_qat_head_only as head_only
from cnn.hw_validation.production.trained_integer import load_package
from cnn.train import sha256


class HeadOnlyContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parent = torch.load(continuation.PARENT, map_location="cpu", weights_only=False)
        cls.graph = load_package(base.BASE / "package")[0].graph

    def test_actual_head_mapping_is_42_of_134_parameter_tensors(self):
        trainable, frozen, mapping = head_only.parameter_contract(self.parent, self.graph)
        self.assertEqual((len(trainable), len(frozen), len(mapping)), (42, 92, 42))
        self.assertEqual(len({row["parent_optimizer_slot"] for row in mapping}), 42)
        self.assertEqual([row["head_optimizer_slot"] for row in mapping], list(range(42)))
        self.assertTrue(all(self.parent["model"][row["name"]].shape ==
                            self.parent["optimizer"]["state"][row["parent_optimizer_slot"]]
                            ["momentum_buffer"].shape for row in mapping))

    def test_authorization_and_fixed_parent(self):
        self.assertEqual(sha256(head_only.AUTHORIZATION), head_only.AUTHORIZATION_SHA256)
        self.assertEqual(sha256(head_only.PARENT), head_only.PARENT_SHA256)
        self.assertEqual(head_only.GLOBAL_UPDATES, 35)
        self.assertEqual(head_only.FORMAT, "road-qat-head-only-g5-v1")

    def test_optimizer_shape_and_hyperparameters_fail_closed(self):
        _trainable, _frozen, mapping = head_only.parameter_contract(self.parent, self.graph)
        group = copy.deepcopy(self.parent["optimizer"]["param_groups"][0])
        group["params"] = list(range(42))
        state = {index: {"momentum_buffer": self.parent["optimizer"]["state"]
                         [row["parent_optimizer_slot"]]["momentum_buffer"].clone()}
                 for index, row in enumerate(mapping)}
        payload = {"param_groups": [group], "state": state}
        self.assertTrue(head_only._optimizer_ok(payload, mapping))
        wrong_lr = copy.deepcopy(payload)
        wrong_lr["param_groups"][0]["lr"] = 2e-4
        self.assertFalse(head_only._optimizer_ok(wrong_lr, mapping))
        wrong_shape = copy.deepcopy(payload)
        wrong_shape["state"][0]["momentum_buffer"] = wrong_shape["state"][0]["momentum_buffer"].reshape(-1)
        self.assertFalse(head_only._optimizer_ok(wrong_shape, mapping))


if __name__ == "__main__":
    unittest.main()
