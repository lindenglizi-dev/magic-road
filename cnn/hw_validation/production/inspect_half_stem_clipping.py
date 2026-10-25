"""Locate saved half-scale probe's Stem clipping relative to existing letterbox edges."""
from pathlib import Path

import numpy as np
import torch

from cnn.integer import requantize, silu
from cnn.hw_validation.production import probe_half_scales as probe
from cnn.hw_validation.production import diagnose_quantization16 as diag
from cnn.hw_validation.production import train_qat as base
from cnn.hw_validation.production.trained_integer import conv_exact
from cnn.train import sha256


def edge_regions(transform, shape=(144, 256)):
    """Stem centers in network pixels; 2-pixel edge band includes resize/3x3 halo."""
    height, width = shape
    y, x = np.meshgrid(2 * np.arange(height) + .5, 2 * np.arange(width) + .5, indexing="ij")
    empty = np.zeros(shape, dtype=bool)
    if not transform:
        return {"edge_band": empty, "padding_away_from_edge": empty, "interior_or_no_known_padding": ~empty}
    left, top = .4 * transform["offset_x"], .4 * transform["offset_y"]
    right = left + .4 * transform["resized_width"]
    bottom = top + .4 * transform["resized_height"]
    edge = empty.copy()
    for coordinates, bound, enabled in ((x, left, left > 0), (x, right, right < 512),
                                        (y, top, top > 0), (y, bottom, bottom < 288)):
        if enabled:
            edge |= np.abs(coordinates - bound) <= 2
    padding = ((x < left) | (x >= right) | (y < top) | (y >= bottom)) & ~edge
    return {"edge_band": edge, "padding_away_from_edge": padding,
            "interior_or_no_known_padding": ~(edge | padding)}


def self_check():
    transform = dict(offset_x=190, offset_y=0, resized_width=900, resized_height=720)
    regions = edge_regions(transform)
    assert np.all(sum(region.astype(np.int8) for region in regions.values()) == 1)
    assert regions["padding_away_from_edge"][70, 0]
    assert regions["edge_band"][70, 38]
    assert regions["interior_or_no_known_padding"][70, 128]
    assert not edge_regions(dict(offset_x=0, offset_y=0, resized_width=1280, resized_height=720))["edge_band"].any()


def main():
    self_check()
    diag.runtime_guard()
    dataset, control, half, _, _, identity = probe.bind_inputs()
    if identity != base.read(probe.OUT / "identity.json"):
        raise ValueError("probe identity changed")
    if base.read(probe.OUT / "status.json")["status"] != "REJECTED_AT_TRAIN16_STOP_NO_FACTOR_SEARCH":
        raise ValueError("this localization is only for the saved rejected probe")
    node = control.graph["nodes"][0]
    if node["name"] != "stem.conv" or node["stride"] != [2, 2]:
        raise ValueError("Stem graph changed")
    results = []
    with torch.inference_mode():
        for sample in base.read(diag.OUT / "selection.json")["samples"]:
            index = sample["train_index"]
            image, _, key = dataset[index]
            p = half.parameters[node["name"]]
            for field in ("weights", "bias", "pre_multiplier", "pre_shift"):
                np.testing.assert_array_equal(p[field], control.parameters[node["name"]][field])
            acc = conv_exact(base.centered(image), p["weights"], p["bias"], 2, 1, 1)
            pre = requantize(acc, p["pre_multiplier"], p["pre_shift"], -32768, 32767).astype(np.int16)
            raw = diag.unclipped(silu(pre), p["post_multiplier"], p["post_shift"])
            clipped = np.clip(raw, -128, 127)
            mask = (raw < -128) | (raw > 127)
            energy = ((raw - clipped).astype(np.float64) * half.scales["stem.conv"]) ** 2
            original = base.read(probe.OUT / "cases" / f"train_{index:02d}.json")
            if int(mask.sum()) != original["half"]["features"]["stem.conv"]["clipping"]["post_clipped"]:
                raise ValueError("Stem recomputation differs from saved full graph")
            transform = dataset.rows[index].get("preprocess", {}).get("letterbox_1280x720")
            regions = edge_regions(transform)
            results.append({"key": key, "group": sample["group"], "transform": transform,
                "known_padding_metadata": transform is not None,
                "regions": {name: {"clipped_values": int(mask[region].sum()),
                                   "clipping_square_loss": float(energy[region].sum())}
                            for name, region in regions.items()}})
    totals = {name: {field: sum(case["regions"][name][field] for case in results)
                     for field in ("clipped_values", "clipping_square_loss")}
              for name in results[0]["regions"]}
    probe.check_identity(identity)
    base.save(probe.OUT / "stem_clipping_locations.json", {"status": "completed_Stem_only_failure_localization",
        "samples": results, "totals": totals, "identity_sha256": base.protocol_hash(identity),
        "source_sha256": sha256(Path(__file__)), "self_check_passed": True, "full_graph_new_inference": False,
        "Stem_only_inference": True, "new_scale_factor_tested": False, "training_updates": 0, "gpu_used": False,
        "limit": "Two-network-pixel band around documented letterbox edges; spatial association, not proof of detection causality. Unknown padding metadata remains unclassified."})


if __name__ == "__main__":
    main()
