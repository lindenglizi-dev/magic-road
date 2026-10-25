"""Focused ancestry and per-class gate checks for the G20 evaluator."""
import copy
import unittest

import torch

from cnn.train import protocol_hash
from cnn.hw_validation.production import train_qat_frozen_stem_continue as runner
from cnn.hw_validation.production.evaluate_qat_continuation import (
    PURPOSE, _continuation_gate, _validate_checkpoint, _validate_package, runtime)


def metrics(person_ap, vehicle_ap, person_recall=.4, vehicle_recall=.4):
    return {"classes": {
        "person": {"precision": .5, "recall": person_recall, "ap50": person_ap, "ap50_95": .1},
        "vehicle": {"precision": .5, "recall": vehicle_recall, "ap50": vehicle_ap, "ap50_95": .1}}}


class ContinuationEvaluationTests(unittest.TestCase):
    def state_and_contract(self):
        parent_identity, parent_protocol = {"parent": 1, "numpy_version": "2.4.6"}, {"total_updates": 10}
        parent_history = [{"update": i + 1} for i in range(10)]
        parent = {"trained_steps": 10, "presentations": 220, "identity": parent_identity,
                  "training_protocol": parent_protocol, "sample_history": parent_history,
                  "model": {"layers.0.weight": torch.tensor([1]),
                            "layers.0.bias": torch.tensor([2])}}
        ancestry = {"parent_checkpoint": str(runner.PARENT.relative_to(runner.base.PROJECT)).replace("\\", "/"),
            "parent_checkpoint_sha256": runner.PARENT_SHA256,
            "parent_trained_steps": 10, "parent_presentations": 220,
            "parent_identity": parent_identity, "parent_identity_sha256": protocol_hash(parent_identity),
            "parent_training_protocol": parent_protocol,
            "parent_training_protocol_sha256": protocol_hash(parent_protocol),
            "parent_sample_history_sha256": protocol_hash(parent_history)}
        transition = {"source_numpy_version": "2.4.6", "current_numpy_version": "2.3.5",
            "intentional": True,
            "control_result_sha256": runtime.CONTROL_RESULT_SHA256,
            "runtime_receipt_sha256": runtime.RUNTIME_RECEIPT_SHA256,
            "cross_runtime_parent_integer_sha256": runtime.CROSS_RUNTIME_SHA256}
        protocol = {"prior_branch_updates": 10, "segment_updates": 10, "total_updates": 20,
            "global_qat_updates_after_segment": 30, "overall_budget_cap": 100,
            "schedule_cycle": 2, "schedule_cycle_sha256": "0" * 64,
            "cpu_resume_check_threads": runtime.CPU_CHECK_THREADS, "gpu_worker_threads": 2,
            "runtime_transition": transition,
            "actual_samples_per_update": 22,
            "frozen_layers": ["stem.conv"], "frozen_fields": ["weight", "bias"]}
        identity = {"source_checkpoint_sha256": runner.base.CHECKPOINT_HASH,
            "numpy_version": "2.3.5", "runtime_transition": transition,
            "protocol_sha256": protocol_hash(protocol), "parent_checkpoint_sha256": runner.PARENT_SHA256,
            "parent_identity": parent_identity, "parent_identity_sha256": protocol_hash(parent_identity),
            "parent_training_protocol": parent_protocol,
            "parent_training_protocol_sha256": protocol_hash(parent_protocol),
            "parent_sample_history_sha256": protocol_hash(parent_history),
            "parent_decision_sha256": runner.PARENT_ARTIFACTS["decision.json"],
            "parent_control_comparison_sha256": runner.PARENT_ARTIFACTS["control_comparison.json"],
            "parent_export_parity_sha256": runner.PARENT_ARTIFACTS["export_parity.json"],
            "source_sha256": {"one.py": "digest"}}
        contract = {"identity": identity, "protocol": protocol, "ancestry": ancestry,
            "source_checkpoint": str(runner.PARENT), "parent_checkpoint_sha256": runner.PARENT_SHA256,
            "segment_start_update": 10, "planned_segment_updates": 10,
            "cumulative_branch_updates": 20, "global_qat_updates_after_segment": 30,
            "overall_qat_budget_cap": 100, "actual_samples_per_update": 22,
            "automatic_retry": False, "automatic_continuation": False,
            "formal_acceptance": False}
        history = copy.deepcopy(parent_history)
        for i in range(10, 20):
            history.append({"update": i + 1, "schedule_update": i - 9, "schedule_cycle": 2,
                "indices": list(range(22)), "keys": [str(x) for x in range(22)],
                "groups": ["new"] * 22, "actual_samples": 22,
                "frozen_stem_unchanged": True, "loss": 1., "gradient_norm_before_clip": 1.})
        state = {"format": runner.FORMAT, "checkpoint_kind": "training", "phase": "qat",
            "candidate": True, "formal_acceptance": False, "trained_steps": 20,
            "next_update": 20, "presentations": 440, "segment_start_update": 10,
            "segment_trained_steps": 10, "segment_presentations": 220,
            "global_qat_updates": 30, "actual_samples_per_update": 22,
            "gradients_pending": False, "identity": identity, "training_protocol": protocol,
            "ancestry": ancestry, "sample_history": history,
            "model": {"layers.0.weight": torch.tensor([1]), "layers.0.bias": torch.tensor([2])},
            "optimizer": {}, "rng_state": {name: 1 for name in ("python", "numpy", "torch", "cuda")}}
        return state, parent, contract

    def test_parent_history_and_global_cursor_cannot_be_forged(self):
        state, parent, contract = self.state_and_contract()
        self.assertEqual(_validate_checkpoint(state, parent, contract), contract["identity"])
        state["sample_history"][0] = {"update": 999}
        with self.assertRaises(ValueError):
            _validate_checkpoint(state, parent, contract)
        state, parent, contract = self.state_and_contract()
        state["global_qat_updates"] = 20
        with self.assertRaises(ValueError):
            _validate_checkpoint(state, parent, contract)
        state, parent, contract = self.state_and_contract()
        parent["identity"]["numpy_version"] = "2.3.5"
        with self.assertRaises(ValueError):
            _validate_checkpoint(state, parent, contract)

    def test_vehicle_recall_drop_fails_even_when_mean_ap_improves(self):
        parent = metrics(.2, .2)
        candidate = metrics(.23, .23, vehicle_recall=.39)
        gate = _continuation_gate(candidate, parent)
        self.assertGreaterEqual(gate["mean_ap50_gain_pp_vs_parent"], 1.)
        self.assertFalse(gate["class_recall_at_0_5_not_below_parent"]["vehicle"])
        self.assertFalse(gate["passed"])

    def test_export_requires_continuation_purpose_and_parent(self):
        identity = {"parent_identity": {"parent": 1}, "source_sha256": {
            "cnn/hw_validation/production/trained_integer.py": "generator"}}
        parent = {"graph": {"nodes": []}, "scales": {"input": 1}}
        manifest = copy.deepcopy(parent)
        manifest.update(generator_sha256="generator", provenance={"purpose": PURPOSE,
            "checkpoint_sha256": "candidate", "source_checkpoint_sha256": runner.base.CHECKPOINT_HASH,
            "trained_steps": 20, "cumulative_qat_updates": 20, "global_qat_updates": 30,
            "segment_qat_updates": 10, "identity": identity,
            "parent_checkpoint_sha256": runner.PARENT_SHA256,
            "parent_identity": identity["parent_identity"], "qat_exact_fixed_weight_scales": True})
        _validate_package(manifest, parent, identity, "candidate")
        manifest["provenance"]["purpose"] = "QAT_G10_DEVELOPMENT_CANDIDATE"
        with self.assertRaises(ValueError):
            _validate_package(manifest, parent, identity, "candidate")


if __name__ == "__main__":
    unittest.main()
