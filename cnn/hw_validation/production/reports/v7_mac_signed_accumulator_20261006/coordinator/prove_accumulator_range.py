"""从冻结67层图证明合法归约的signed33范围，不执行训练或重建模型。"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PRODUCTION = ROOT.parents[2]
PROJECT = PRODUCTION.parents[2]


def prove(graph):
    layers = []
    for node in graph["nodes"]:
        if node["op"] != "conv":
            continue
        channels = node["input_shape_hwc"][2]
        groups = node["groups"]
        kh, kw = node["kernel"]
        assert groups > 0 and channels % groups == 0
        assert all(isinstance(value, int) and value > 0 for value in [channels, groups, kh, kw])
        terms = kh * kw * (channels // groups)
        beats = kh * kw * ((channels // groups + 7) // 8)
        assert node["weights"] == terms * node["output_shape_hwc"][2]
        assert node["macs"] == terms * node["output_shape_hwc"][0] * node["output_shape_hwc"][1] * node["output_shape_hwc"][2]
        layers.append({"name": node["name"], "terms": terms, "beats": beats,
                       "kernel": [kh, kw], "channels_per_group": channels // groups})
    assert len(layers) == 67
    assert graph["summary"]["macs"] == 214465536
    assert sum(node["macs"] for node in graph["nodes"] if node["op"] == "conv") == 214465536
    terms = max(layer["terms"] for layer in layers)
    beats = max(layer["beats"] for layer in layers)
    assert terms == 192 and beats == 24
    minimum_product = -128 * 127
    maximum_product = -128 * -128
    bounds = [{"prefix_terms": n, "lower": -(1 << 31) + n * minimum_product,
               "upper": (1 << 31) - 1 + n * maximum_product} for n in range(terms + 1)]
    for bound in bounds:
        assert -(1 << 32) <= bound["lower"] <= bound["upper"] <= (1 << 32) - 1
    return {"status": "PROVED_FOR_FROZEN_GRAPH_LEGAL_REDUCTIONS", "layers": layers,
            "max_terms": terms, "max_beats": beats,
            "max_term_layers": [layer["name"] for layer in layers if layer["terms"] == terms],
            "product_range": [minimum_product, maximum_product],
            "all_prefix_bounds": bounds,
            "whole_range": [min(b["lower"] for b in bounds), max(b["upper"] for b in bounds)],
            "signed33_range": [-(1 << 32), (1 << 32) - 1],
            "scope": "one output location and channel, INT32 bias once, at most 192 active INT8 products; 24 accepted 8-lane beats at most",
            "caller_obligation": "first begins a reduction, last ends it; scheduler never exceeds 24 beats/192 valid terms. No new counter or external port added.",
            "not_proved": "unbounded malformed first/last streams; whole-network scheduler correctness, physical implementation or formal equivalence"}


if __name__ == "__main__":
    graph_path = PRODUCTION / "graph_artifacts" / "graph.json"
    graph = json.loads(graph_path.read_text(encoding="utf-8"))
    closure = []
    for relative, expected in graph["source_sha256"].items():
        source = PROJECT / relative
        actual = hashlib.sha256(source.read_bytes()).hexdigest()
        assert actual == expected, f"Frozen graph source drift: {relative}"
        closure.append({"path": str(source), "sha256": actual})
    result = prove(graph)
    result["graph_sha256"] = hashlib.sha256(graph_path.read_bytes()).hexdigest()
    result["source_closure"] = closure
    result["proof_source_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (ROOT / "range_proof.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: result[key] for key in ["status", "max_terms", "max_beats", "max_term_layers", "whole_range", "signed33_range"]}))
