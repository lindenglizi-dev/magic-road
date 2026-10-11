"""Independently prove the finite reduction bounds from the frozen network graph."""
import json
from pathlib import Path


def main():
    root = Path(__file__).resolve().parent
    graph = json.loads((root.parent.parent / "graph_artifacts/graph.json").read_text(encoding="utf-8"))
    product_min = min(a * w for a in range(-128, 128) for w in range(-128, 128))
    product_max = max(a * w for a in range(-128, 128) for w in range(-128, 128))
    lower = -(1 << 31) + 192 * product_min
    upper = (1 << 31) - 1 + 192 * product_max
    assert (product_min, product_max) == (-16256, 16384)
    assert (lower, upper) == (-2150604800, 2150629375)
    assert -(1 << 32) <= lower <= upper < (1 << 32)
    reductions = []
    for node in graph["nodes"]:
        if node["op"] != "conv":
            continue
        channels = node["input_shape_hwc"][2]
        groups = node["groups"]
        assert channels % groups == 0
        terms = channels // groups * node["kernel"][0] * node["kernel"][1]
        assert terms <= 192, (node["name"], terms)
        reductions.append({"name": node["name"], "effective_products": terms,
                           "groups_of_eight": (terms + 7) // 8})
    assert len(reductions) == 67
    assert max(item["effective_products"] for item in reductions) == 192
    for terms in range(193):
        assert lower <= -(1 << 31) + terms * product_min
        assert (1 << 31) - 1 + terms * product_max <= upper
    result = {"status": "SIGNED33_FINITE_PREFIX_PROOF_PASS",
              "graph_architecture_sha256": graph["architecture_sha256"],
              "int8_product_bounds": [product_min, product_max],
              "partial_accumulator_bounds": [lower, upper],
              "effective_product_limit_per_output": 192, "group_limit": 24,
              "frozen_graph_convolutions": reductions,
              "scope": "Each prefix from one signed32 bias/first initialization, including first0 continuation within that same finite budget; not unlimited accumulation"}
    (root / "numeric_range_proof.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
