"""从已封存 CSP4 生成 SPPF CPU golden 与上行 PAN 精确依赖规格。"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[4]
sys.path.insert(0, str(PROJECT))

import numpy as np
import torch

from cnn.hw_validation.production.trained_integer import load_package, nonconv

OLD = PROJECT / "cnn/hw_validation/production/csp_family_layer_scheduled_20261015/reference_attempt2/generate_reference.py"
MODULE = importlib.util.spec_from_file_location("frozen_cpu_helpers", OLD)
HELPERS = importlib.util.module_from_spec(MODULE)
MODULE.loader.exec_module(HELPERS)
OUT = ROOT / "sppf"
torch.set_num_threads(1)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(name: str, data: object) -> None:
    (OUT / name).parent.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def scalar_pool(source: np.ndarray, padding: int = -128, unsigned: bool = False) -> np.ndarray:
    """独立逐元素25点 oracle；不调用向量池化或其 padding helper。"""
    height, width, channels = source.shape
    result = np.empty_like(source)
    for y in range(height):
        for x in range(width):
            for channel in range(channels):
                best = -128 if not unsigned else 0
                for dy in range(-2, 3):
                    for dx in range(-2, 3):
                        yy, xx = y + dy, x + dx
                        value = int(source[yy, xx, channel]) if 0 <= yy < height and 0 <= xx < width else padding
                        if unsigned:
                            value &= 255
                        best = max(best, value)
                result[y, x, channel] = best if best < 128 else best - 256
    return result


def physical_tile(source: np.ndarray) -> tuple[np.ndarray, dict]:
    height, width, channels = source.shape
    physical = np.zeros(((height + 3) // 4, (width + 3) // 4, 4, 4, channels), dtype=np.int8)
    valid = np.zeros(physical.shape, dtype=bool)
    for y in range(height):
        for x in range(width):
            physical[y // 4, x // 4, y % 4, x % 4] = source[y, x]
            valid[y // 4, x // 4, y % 4, x % 4] = True
    assert np.all(physical[~valid] == 0)
    return physical.ravel(), {"physical_bytes": physical.size, "valid_bytes": source.size,
                              "invalid_tail_bytes_zero": int((~valid).sum()),
                              "algorithm_padding": -128, "physical_invalid_fill": 0}


def dependencies(graph: dict, package: dict) -> dict:
    nodes = {node["name"]: node for node in graph["nodes"]}
    producers = {}
    for node in graph["nodes"]:
        for output in node.get("outputs", [{"output": node.get("output")} ]):
            producers[output["output"]] = node

    def shape(tensor: str) -> list[int]:
        producer = producers[tensor]
        if producer["op"] == "split_view":
            parent = shape(producer["inputs"][0])
            return parent[:2] + [next(v["channels"] for v in producer["outputs"] if v["output"] == tensor)]
        return producer.get("output_shape_hwc", producer.get("shape_hwc"))

    def view(tensor: str) -> dict:
        node = producers[tensor]
        op = node["op"]
        if op in ("conv", "maxpool"):
            return {"tensor": tensor, "op": "storage", "shape_hwc": shape(tensor), "storage": node["storage"]}
        if op == "residual_view":
            return {"tensor": tensor, "op": "storage_alias", "target": node["storage_alias"],
                    "backing": view(node["storage_alias"]), "residual_inputs": node["inputs"],
                    "write": "signed9 graph bypass + PW post, sat8; alias contains the sum"}
        if op == "split_view":
            row = next(v for v in node["outputs"] if v["output"] == tensor)
            return {"tensor": tensor, "op": op, "channel_offset": row["channel_offset"],
                    "channels": row["channels"], "source": view(node["inputs"][0])}
        if op == "nearest_view":
            return {"tensor": tensor, "op": op, "source_index": node["source_index"],
                    "scale": node["scale"], "source": view(node["inputs"][0])}
        if op == "concat_view":
            offset, branches = 0, []
            for name in node["inputs"]:
                channels = shape(name)[2]
                branches.append({"channel_begin": offset, "channel_end_exclusive": offset + channels,
                                 "source": view(name)})
                offset += channels
            assert offset == shape(tensor)[2]
            return {"tensor": tensor, "op": op, "branches": branches}
        raise ValueError(op)

    selected = [node for node in graph["nodes"] if 46 <= node["index"] <= 63]
    convs = [node for node in selected if node["op"] == "conv"]
    assert len(convs) == 8 and not any("out.conv" in node["name"] for node in convs)
    rows = []
    for node in convs:
        rows.append({"graph_node": node, "input_view": view(node["inputs"][0]),
                     "parameters": [segment for segment in package["segments"]
                                    if segment["name"].startswith(node["name"] + ".")],
                     "write_bypass_view": view(node["write_transform"]["bypass"]) if "write_transform" in node else None})

    def storage_names(tensor: str) -> set[str]:
        if tensor == "input":
            return set()
        node = producers[tensor]
        if node["op"] in ("conv", "maxpool"):
            return {node["name"]}
        if node["op"] == "residual_view":
            return {node["storage_alias"]}
        return set().union(*(storage_names(name) for name in node["inputs"]))

    lifetimes = {}
    for node in graph["nodes"]:
        if node["op"] not in ("conv", "maxpool"):
            continue
        for tensor in node["inputs"]:
            for name in storage_names(tensor):
                lifetimes.setdefault(name, []).append(node["name"])
        if "write_transform" in node:
            for name in storage_names(node["write_transform"]["bypass"]):
                lifetimes.setdefault(name, []).append(node["name"] + ":residual_write")
    retained = {name: {"consumers": consumers, "release": "after last actual read response consumed by " + consumers[-1]}
                for name, consumers in lifetimes.items()
                if name in {"csp2.out.conv", "csp3.out.conv", "sppf.out.conv", "lateral4.conv",
                            "fuse3_td.reduce.conv", "fuse3_td.block.pw.conv", "fuse2_td.reduce.conv"}}
    return {"status": "SPEC_ONLY_NO_PAN_GOLDEN_NO_RTL", "nodes": selected, "convolutions": rows,
            "outputs": {"fuse3_td": view("concat.05"), "fuse2_td": view("concat.07")},
            "storage_lifetimes": retained,
            "address_formula": "base + (((y//4)*ceil(W/4)+x//4)*16+(y%4)*4+x%4)*storedC+c",
            "numeric": "signed33 MAC, INT32 final; RNE/sat16 pre, shared SiLU, RNE/sat8 post; aligned signed9 residual sat8",
            "missing_real_producers": ["down3_bu.dw.conv", "down3_bu.pw.conv", "down4_bu.dw.conv", "down4_bu.pw.conv"],
            "shared_storage_budget": {"work_bytes": 3072, "weight_banks": 24, "parameter_group_bits": 5},
            "boundary": "Views describe addresses without materializing nearest/concat; actual final-read retirement still requires RTL evidence."}


def main() -> None:
    assert not (ROOT / "sppf_manifest.json").exists(), "SPPF already frozen"
    csp_manifest = json.loads((ROOT / "csp_manifest.json").read_text(encoding="utf-8"))
    source_paths = {PROJECT / key for key in csp_manifest["source_sha256"]}
    source_paths.update(ROOT / key for key in csp_manifest["artifacts"])
    source_paths.update([ROOT / "csp_manifest.json", Path(__file__), OLD,
                         PROJECT / "cnn/hw_validation/production/trained_integer.py"])
    before = {path.relative_to(PROJECT).as_posix(): sha(path) for path in sorted(source_paths)}
    for key, expected in csp_manifest["artifacts"].items():
        assert sha(ROOT / key) == expected, key
    model, package = load_package(HELPERS.PACKAGE)
    assert package["payload_sha256"] == HELPERS.PAYLOAD_SHA256
    assert not torch.cuda.is_initialized()
    graph = package["graph"]
    nodes = {node["name"]: node for node in graph["nodes"]}
    source = np.load(ROOT / "csp4/npy/stage6_output.npy", allow_pickle=False)
    assert source.shape == (18, 32, 96) and source.dtype == np.int8
    values = {"csp4.out.conv": source}
    fields_by_name, pool_checks, physical_checks = {}, [], {}
    OUT.mkdir(exist_ok=True)
    for name in ("sppf.squeeze.conv", "pool.00", "pool.01", "pool.02", "concat.03", "sppf.out.conv"):
        node = nodes[name]
        if node["op"] == "conv":
            fields = HELPERS.execute_conv(node, values[node["inputs"][0]], model.parameters, scalar_check=True)
            fields_by_name[name] = fields
            values[name] = fields["post"]
            for field, array in fields.items():
                np.save(OUT / f"{name}.{field}.npy", array, allow_pickle=False)
                HELPERS.emit_hex(OUT / f"{name}.{field}.hex", array, HELPERS.BITS[field])
            for field, array in model.parameters[name].items():
                HELPERS.emit_hex(OUT / "parameters" / f"{name}.{field}.hex", array, HELPERS.PARAM_BITS[field])
        else:
            values.update(nonconv(node, values))
            np.save(OUT / f"{name}.npy", values[name], allow_pickle=False)
            HELPERS.emit_hex(OUT / f"{name}.hex", values[name], 8)
            if node["op"] == "maxpool":
                oracle = scalar_pool(values[node["inputs"][0]])
                np.testing.assert_array_equal(values[name], oracle)
                wrong = scalar_pool(values[node["inputs"][0]], padding=0)
                mismatch = np.flatnonzero(oracle.ravel() != wrong.ravel())
                pool_checks.append({"node": name, "full_scalar_values": oracle.size,
                                    "negative_output_values": int((oracle < 0).sum()),
                                    "real_road_wrong_pad0_mismatch_values": int(mismatch.size)})
        if "storage" in node:
            tile, check = physical_tile(values[name])
            HELPERS.emit_hex(OUT / f"{name}.tile.hex", tile, 8)
            physical_checks[name] = check
    # Actual numerical counterexamples: all-negative borders distinguish -128 from 0;
    # mixed signed extremes distinguish signed max from an unsigned byte compare.
    negative = np.arange(-35, 0, dtype=np.int8).reshape(5, 7, 1)
    mixed = np.array([-128, -5, 1, 127, -1, 2], dtype=np.int8).reshape(2, 3, 1)
    probes = []
    for name, array, wrong_pad, unsigned in (("negative_border_wrong_pad0", negative, 0, False),
                                            ("mixed_wrong_unsigned", mixed, -128, True)):
        correct = scalar_pool(array)
        vector = nonconv(nodes["pool.00"], {nodes["pool.00"]["inputs"][0]: array})["pool.00"]
        np.testing.assert_array_equal(vector, correct)
        wrong = scalar_pool(array, padding=wrong_pad, unsigned=unsigned)
        mismatch = np.flatnonzero(correct.ravel() != wrong.ravel())
        assert mismatch.size > 0
        index = int(mismatch[0])
        probes.append({"name": name, "source": array.tolist(), "mismatches": int(mismatch.size),
                       "first_flat_index": index, "correct": int(correct.ravel()[index]),
                       "wrong": int(wrong.ravel()[index]), "wrong_rejected": True})
    HELPERS.emit_hex(OUT / "parameters/silu.hex", HELPERS.tables()["silu"], 16)
    save("contract.json", {"status": HELPERS.MARKER, "payload_sha256": HELPERS.PAYLOAD_SHA256,
                           "source": "csp4/npy/stage6_output.npy", "nodes": [nodes[name] for name in values if name != "csp4.out.conv"],
                           "concat_order": nodes["concat.03"]["inputs"], "pool_padding": -128,
                           "physical_tile_invalid_fill": 0, "full_scalar_conv_checked": 2,
                           "pool_full_scalar_checked": 3, "boundary": "CPU-only SPPF from corrected frozen CSP4; no continuous RTL prefix"})
    save("pan_dependency_spec.json", dependencies(graph, package))
    after = {path.relative_to(PROJECT).as_posix(): sha(path) for path in sorted(source_paths)}
    assert before == after
    assert not torch.cuda.is_initialized()
    report = {"status": "PASS_CPU_SPPF_REFERENCE", "pool_checks": pool_checks,
              "physical_tile_checks": physical_checks, "true_numerical_negative_checks": probes,
              "conv_full_scalar_checked": 2, "source_before_after_equal": True,
              "source_files_checked": len(before), "cuda_initialized": torch.cuda.is_initialized(),
              "cpu_only": True, "training": False, "pan_status": "DEPENDENCY_SPEC_ONLY",
              "not_measured": ["RTL", "DDR_visibility", "continuous_backbone", "resource_mapping", "timing", "board"],
              "command": "D:/anaconda3/python.exe -B reference/generate_sppf_reference.py"}
    save("report.json", report)
    artifacts = {path.relative_to(ROOT).as_posix(): sha(path) for path in sorted(OUT.rglob("*")) if path.is_file()}
    artifacts[Path(__file__).name] = sha(Path(__file__))
    manifest = {"status": HELPERS.MARKER, "payload_sha256": HELPERS.PAYLOAD_SHA256,
                "source_sha256": after, "artifacts": artifacts, "artifact_count": len(artifacts),
                "immutable_after_generation": True, "csp_manifest_unchanged": sha(ROOT / "csp_manifest.json")}
    (ROOT / "sppf_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"PASS: 2 scalar convolutions, 3 full scalar pools, 2 rejected numerical negatives; {len(artifacts)} artifacts")


if __name__ == "__main__":
    main()
