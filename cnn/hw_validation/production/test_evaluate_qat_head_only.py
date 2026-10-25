"""Focused gate and package checks for head-only H5 evaluation."""
import copy
import json
import unittest

import numpy as np
import torch

from cnn.hw_validation.production import train_qat_head_only as runner
from cnn.hw_validation.production.evaluate_qat_head_only import (
    PURPOSE, _gate, _report_ancestry, _validate_package)


def metrics(person_ap, vehicle_ap, person_recall=.4, vehicle_recall=.4):
    return {"classes": {
        "person": {"precision": .5, "recall": person_recall, "ap50": person_ap, "ap50_95": .1},
        "vehicle": {"precision": .5, "recall": vehicle_recall, "ap50": vehicle_ap, "ap50_95": .1}}}


class HeadOnlyEvaluationTests(unittest.TestCase):
    def test_recall_drop_fails_even_when_mean_ap_improves(self):
        result = _gate(metrics(.23, .23, vehicle_recall=.39), metrics(.2, .2))
        self.assertGreaterEqual(result["mean_ap50_gain_pp_vs_parent"], 1.)
        self.assertFalse(result["class_recall_at_0_5_not_below_parent"]["vehicle"])
        self.assertFalse(result["passed"])

    def test_package_requires_head_only_scope_and_counts(self):
        identity = {"source_sha256": {
            "cnn/hw_validation/production/trained_integer.py": "generator"}}
        parent = {"graph": {"nodes": []}, "scales": {"input": 1}}
        manifest = copy.deepcopy(parent)
        manifest.update(generator_sha256="generator", provenance={"purpose": PURPOSE,
            "checkpoint_sha256": "candidate", "source_checkpoint_sha256": runner.base.CHECKPOINT_HASH,
            "parent_checkpoint_sha256": runner.PARENT_SHA256, "trained_steps": runner.UPDATES,
            "local_head_only_updates": runner.UPDATES,
            "global_qat_updates": runner.GLOBAL_UPDATES, "identity": identity,
            "trainable_parameter_tensors": 42, "frozen_parameter_tensors": 92,
            "qat_exact_fixed_weight_scales": True})
        _validate_package(manifest, parent, identity, "candidate")
        manifest["provenance"]["frozen_parameter_tensors"] = 91
        with self.assertRaises(ValueError):
            _validate_package(manifest, parent, identity, "candidate")

    def test_tensor_and_ndarray_parent_rng_are_reported_as_binding(self):
        ancestry = {"parent_checkpoint_sha256": runner.PARENT_SHA256,
            "parent_identity": {"kept": True}, "parent_rng_state": {
                "python": (1, 2), "numpy": np.array([3]),
                "torch": torch.tensor([4]), "cuda": [torch.tensor([5])]}}
        reported = _report_ancestry(ancestry)
        json.dumps(reported)
        self.assertEqual(reported["parent_identity"], {"kept": True})
        self.assertEqual(reported["parent_rng_state"]["parent_checkpoint_sha256"], runner.PARENT_SHA256)
        self.assertEqual(reported["parent_rng_state"]["stream_names"],
                         ["python", "numpy", "torch", "cuda"])


if __name__ == "__main__":
    unittest.main()
