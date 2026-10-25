"""Focused identity checks for the QAT development17 evaluator."""
import copy
import unittest

from cnn.train import protocol_hash
from cnn.hw_validation.production.evaluate_qat import (
    BASELINE, CHECKPOINT_HASH, SOURCE_PACKAGE, SOURCE_MANIFEST_HASH, SAMPLES_PER_UPDATE,
    TRAIN_HASH, UPDATES, _validate_candidate, _validate_checkpoint, read)


class EvaluateQATTests(unittest.TestCase):
    def test_checkpoint_and_export_must_share_frozen_identity(self):
        manifest, baseline = read(SOURCE_PACKAGE / "manifest.json"), read(BASELINE)
        protocol = {"total_updates": UPDATES,
                    "actual_samples_per_update": SAMPLES_PER_UPDATE}
        identity = {
            "source_checkpoint_sha256": CHECKPOINT_HASH,
            "architecture_hash": baseline["architecture_hash"],
            "dataset_sha256": TRAIN_HASH,
            "dataset_content_sha256": manifest["provenance"]["calibration_content_sha256"],
            "graph_sha256": protocol_hash(manifest["graph"]),
            "scales_sha256": protocol_hash(manifest["scales"]),
            "source_package_manifest_sha256": SOURCE_MANIFEST_HASH,
            "source_payload_sha256": manifest["payload_sha256"],
            "quantization_sha256": manifest["provenance"]["quantization_sha256"],
            "protocol_sha256": protocol_hash(protocol),
            "source_sha256": {
                "cnn/hw_validation/production/trained_integer.py": manifest["generator_sha256"]},
        }
        history = [{"update": update, "indices": list(range(SAMPLES_PER_UPDATE)),
                    "keys": [str(i) for i in range(SAMPLES_PER_UPDATE)],
                    "groups": ["new"] * SAMPLES_PER_UPDATE,
                    "actual_samples": SAMPLES_PER_UPDATE, "loss": 1.,
                    "gradient_norm_before_clip": 1.}
                   for update in range(1, UPDATES + 1)]
        state = {"format": "road-qat-resume-v1", "checkpoint_kind": "training",
                 "phase": "qat", "candidate": True, "formal_acceptance": False,
                 "trained_steps": UPDATES, "next_update": UPDATES,
                 "presentations": UPDATES * SAMPLES_PER_UPDATE,
                 "actual_samples_per_update": SAMPLES_PER_UPDATE,
                 "gradients_pending": False, "sample_history": history,
                 "model": {"one": 1}, "optimizer": {}, "rng_state": {},
                 "identity": identity, "training_protocol": protocol}
        validated = _validate_checkpoint(state, manifest, baseline)
        candidate = copy.deepcopy(manifest)
        candidate["provenance"] = {"purpose": "QAT_G10_DEVELOPMENT_CANDIDATE",
            "checkpoint_sha256": "candidate-checkpoint",
            "source_checkpoint_sha256": CHECKPOINT_HASH, "trained_steps": UPDATES,
            "identity": identity, "qat_exact_fixed_weight_scales": True}
        _validate_candidate(candidate, manifest, validated, "candidate-checkpoint")
        candidate["provenance"]["checkpoint_sha256"] = "wrong"
        with self.assertRaises(ValueError):
            _validate_candidate(candidate, manifest, validated, "candidate-checkpoint")


if __name__ == "__main__":
    unittest.main()
