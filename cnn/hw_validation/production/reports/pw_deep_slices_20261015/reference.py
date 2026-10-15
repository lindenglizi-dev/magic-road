"""Bit-exact 4x4 golden vectors for the two frozen deep pointwise shapes."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[5]
PACKAGE = (ROOT / "cnn/hw_validation/production/reports"
           / "qat_g10_front3_data_20261014_v1/inputs")
MANIFEST_PATH = PACKAGE / "manifest.json"
PAYLOAD_PATH = PACKAGE / "numeric_test.bin"
GRAPH_PATH = ROOT / "cnn/hw_validation/production/graph_artifacts/graph.json"
BASELINE = HERE.parent / "pw48_tile_20261015/reference_receipt.json"

EXPECTED_MANIFEST_SHA256 = "93a05a97f78489fabd511909367be0f8b676680c01e5f74a21d571a88f82ff2b"
EXPECTED_PAYLOAD_SHA256 = "b35d4a66a69e441dc29bc60c7e3f507661f48da5f33b810d7340f6ed17a65145"
PACKAGE_STATUS = "TRAINED_PTQ_DIAGNOSTIC_NOT_QAT_NOT_BOARD_QUALIFIED"
LAYERS = {
    "sppf.squeeze.conv": (96, 24),
    "fuse4_bu.reduce.conv": (192, 96),
}

sys.path.insert(0, str(ROOT))
from cnn.integer import conv2d, requantize, silu, tables  # noqa: E402


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def array_sha256(values: np.ndarray) -> str:
    return hashlib.sha256(np.ascontiguousarray(values).tobytes()).hexdigest()


def write_hex(path: Path, values: np.ndarray, bits: int, signed: bool) -> dict[str, object]:
    data = np.asarray(values).reshape(-1).astype(np.int64)
    low = -(1 << (bits - 1)) if signed else 0
    high = (1 << (bits - 1)) if signed else (1 << bits)
    if np.any(data < low) or np.any(data >= high):
        raise ValueError(f"{path.name}: value outside {bits}-bit {'signed' if signed else 'unsigned'} range")
    mask = (1 << bits) - 1
    digits = (bits + 3) // 4
    path.write_text("".join(f"{int(value) & mask:0{digits}x}\n" for value in data), encoding="ascii")
    return {"name": path.name, "count": int(data.size), "bits": bits,
            "signed": signed, "sha256": sha256(path)}


def load_segment(manifest: dict, payload: bytes, name: str) -> tuple[np.ndarray, dict]:
    segment = next((item for item in manifest["segments"] if item["name"] == name), None)
    if segment is None:
        raise AssertionError(f"missing package segment: {name}")
    raw = payload[segment["offset"]:segment["offset"] + segment["length"]]
    if len(raw) != segment["length"] or hashlib.sha256(raw).hexdigest() != segment["sha256"]:
        raise AssertionError(f"package segment hash mismatch: {name}")
    dtype = {"int8": "i1", "uint8": "u1", "int32_le": "<i4", "<i2": "<i2"}[segment["dtype"]]
    values = np.frombuffer(raw, dtype=dtype).copy()
    if values.size != segment["count"]:
        raise AssertionError(f"package segment count mismatch: {name}")
    return values, {key: segment[key] for key in
                    ("name", "offset", "length", "dtype", "shape", "count", "sha256")}


def load_layer(manifest: dict, payload: bytes, name: str, cin: int, cout: int) -> tuple[dict, list[dict]]:
    values: dict[str, np.ndarray | int] = {}
    records = []
    for field in ("weights", "bias", "pre_multiplier", "pre_shift", "post_multiplier", "post_shift"):
        data, record = load_segment(manifest, payload, f"{name}.{field}")
        values[field] = int(data[0]) if field.startswith("post_") else data
        records.append(record)
    values["weights"] = np.asarray(values["weights"], dtype=np.int8).reshape(cout, cin)
    for field in ("bias", "pre_multiplier", "pre_shift"):
        if np.asarray(values[field]).shape != (cout,):
            raise AssertionError(f"{name}.{field}: shape mismatch")
    return values, records


def deterministic_input(cin: int, seed: int) -> np.ndarray:
    """Frozen random INT8 HWC tile; this is not an image or accuracy sample."""
    return np.random.default_rng(seed).integers(-128, 128, (4, 4, cin), dtype=np.int16).astype(np.int8)


def verify_bank_mapping(inputs: np.ndarray, weights: np.ndarray) -> dict[str, int | bool]:
    flat_input = inputs.reshape(16, inputs.shape[2])
    cout, cin = weights.shape
    input_depth = 16 * cin // 8
    input_banks = np.empty((8, input_depth), dtype=np.int8)
    input_seen = np.zeros(input_banks.shape, dtype=bool)
    for position, ic in np.ndindex(16, cin):
        bank, row = ic % 8, position * (cin // 8) + ic // 8
        if input_seen[bank, row]:
            raise AssertionError("input bank mapping is not injective")
        input_seen[bank, row] = True
        input_banks[bank, row] = flat_input[position, ic]

    weight_banks = np.empty((24, 96), dtype=np.int8)
    weight_seen = np.zeros(weight_banks.shape, dtype=bool)
    for local_oc, ic in np.ndindex(cout, cin):
        bank = (local_oc % 3) * 8 + ic % 8
        row = (local_oc // 3) * (cin // 8) + ic // 8
        if weight_seen[bank, row]:
            raise AssertionError("weight bank mapping is not injective")
        weight_seen[bank, row] = True
        weight_banks[bank, row] = weights[local_oc, ic]
    if not input_seen.all() or not weight_seen.all():
        raise AssertionError("bank mapping is not bijective")

    groups = np.empty((16, cout // 3, cin // 8, 3), dtype=np.int64)
    for position, oc_group, ic_group, lane in np.ndindex(groups.shape):
        groups[position, oc_group, ic_group, lane] = sum(
            int(input_banks[ic % 8, position * (cin // 8) + ic // 8])
            * int(weight_banks[lane * 8 + ic % 8,
                               oc_group * (cin // 8) + ic // 8])
            for ic in range(ic_group * 8, ic_group * 8 + 8))
    direct_groups = (flat_input.astype(np.int64)[:, None, :]
                     * weights.astype(np.int64)[None, :, :])
    expected = direct_groups.reshape(16, cout // 3, 3, cin // 8, 8).sum(axis=4).transpose(0, 1, 3, 2)
    if not np.array_equal(groups, expected):
        raise AssertionError("bank groups differ from direct OIHW products")
    return {"input_bank_depth": input_depth, "input_bank_entries": int(input_seen.size),
            "weight_bank_depth": 96, "weight_bank_entries": int(weight_seen.size),
            "group_values_matched": int(groups.size), "bijections": True}


def golden(inputs: np.ndarray, parameters: dict, layer: str,
           verify_banks: bool = True) -> tuple[dict[str, np.ndarray], dict]:
    weights = np.asarray(parameters["weights"], dtype=np.int8)
    bias = np.asarray(parameters["bias"], dtype=np.int32)
    premul = np.asarray(parameters["pre_multiplier"], dtype=np.int64)
    preshift = np.asarray(parameters["pre_shift"], dtype=np.uint8)
    postmul, postshift = int(parameters["post_multiplier"]), int(parameters["post_shift"])
    if np.any(premul < 0) or np.any(premul >= (1 << 31)) or np.any(preshift > 62):
        raise AssertionError(f"{layer}: invalid pre-requantization parameters")
    if not 0 <= postmul < (1 << 31) or not 0 <= postshift <= 62:
        raise AssertionError(f"{layer}: invalid post-requantization parameters")

    bank_checks = verify_bank_mapping(inputs, weights) if verify_banks else {
        "bank_mapping": "not_applicable_full_96_output_layer_before_12_channel_slicing"}
    products = inputs.reshape(16, -1).astype(np.int64)[:, None, :] * weights.astype(np.int64)[None, :, :]
    prefixes = np.cumsum(products, axis=2) + bias.astype(np.int64)[None, :, None]
    if np.any(prefixes < -(1 << 32)) or np.any(prefixes >= (1 << 32)):
        raise AssertionError(f"{layer}: partial sum outside signed33")
    group_prefixes = (np.cumsum(products.reshape(16, weights.shape[0], -1, 8).sum(axis=3), axis=2)
                      + bias.astype(np.int64)[None, :, None])
    if np.any(group_prefixes < -(1 << 32)) or np.any(group_prefixes >= (1 << 32)):
        raise AssertionError(f"{layer}: 8-product group prefix outside signed33")
    acc = conv2d(inputs, weights.reshape(weights.shape[0], weights.shape[1], 1, 1), bias)
    direct = products.sum(axis=2) + bias.astype(np.int64)[None, :]
    if not np.array_equal(acc.reshape(16, -1), direct):
        raise AssertionError(f"{layer}: cnn.integer.conv2d mismatch")
    if np.any(acc < -(1 << 31)) or np.any(acc >= (1 << 31)):
        raise AssertionError(f"{layer}: final accumulator outside INT32")
    pre = requantize(acc, premul, preshift, -32768, 32767).astype(np.int16)
    activated = silu(pre)
    post = requantize(activated, postmul, postshift, -128, 127).astype(np.int8)
    arrays = {"input": inputs.astype(np.int32), "weights": weights, "bias": bias,
              "pre_multiplier": premul, "pre_shift": preshift,
              "post_params": np.array([postmul, postshift], dtype=np.int64),
              "acc": acc, "pre": pre, "silu": activated, "post": post}
    checks = {**bank_checks, "signed33_prefix_values": int(prefixes.size),
              "signed33_prefix_min": int(prefixes.min()), "signed33_prefix_max": int(prefixes.max()),
              "signed33_group_prefix_values": int(group_prefixes.size),
              "signed33_group_prefix_min": int(group_prefixes.min()),
              "signed33_group_prefix_max": int(group_prefixes.max()),
              "final_int32_values": int(acc.size), "direct_conv_match": True,
              "numeric_implementation": "cnn.integer.conv2d/requantize/silu"}
    return arrays, checks


def emit_case(name: str, profile: int, cin: int, cout: int, slab_offset: int,
              layer: str, arrays: dict[str, np.ndarray], checks: dict,
              segments: list[dict], input_seed: int) -> dict:
    widths = {"input": (32, True), "weights": (8, True), "bias": (32, True),
              "pre_multiplier": (32, False), "pre_shift": (8, False),
              "post_params": (32, False), "acc": (32, True), "pre": (16, True),
              "silu": (16, True), "post": (8, True)}
    files = {field: write_hex(HERE / f"{name}_{field}.hex", values, *widths[field])
             for field, values in arrays.items()}
    return {"name": name, "profile": profile, "cin": cin, "cout": cout,
            "slab_offset": slab_offset, "file_prefix": name, "source_layer": layer,
            "input_seed": input_seed, "input_layout": "4x4 HWC, INT8 values sign-extended to INT32 hex",
            "weight_layout": f"OIHW {cout}x{cin}x1x1",
            "output_layout": f"4x4 HWC local channels; global OC offset {slab_offset}",
            "source_segments": segments, "files": files,
            "phase_golden": {field: {"count": int(arrays[field].size),
                                             "sha256": array_sha256(arrays[field])}
                               for field in ("acc", "pre", "silu", "post")},
            "ranges": {field: {"min": int(np.min(values)), "max": int(np.max(values))}
                       for field, values in arrays.items()}, "checks": checks}


def main() -> None:
    if sha256(MANIFEST_PATH) != EXPECTED_MANIFEST_SHA256 or sha256(PAYLOAD_PATH) != EXPECTED_PAYLOAD_SHA256:
        raise AssertionError("frozen QAT-G10 package snapshot drifted")
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    payload = PAYLOAD_PATH.read_bytes()
    if manifest["status"] != PACKAGE_STATUS or manifest["payload_sha256"] != EXPECTED_PAYLOAD_SHA256:
        raise AssertionError("package status or payload identity mismatch")
    live_graph_sources = {name: sha256(ROOT / name) for name in manifest["graph_source_sha256"]}
    if live_graph_sources != manifest["graph_source_sha256"]:
        raise AssertionError("package graph/core source closure drifted")
    if sha256(ROOT / "cnn/hw_validation/production/trained_integer.py") != manifest["generator_sha256"]:
        raise AssertionError("trained_integer package generator drifted")
    if sha256(ROOT / "cnn/hw_validation/production/deployment_contract.json") != manifest["contract_sha256"]:
        raise AssertionError("deployment contract drifted")

    graph = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
    graph_shapes = {node["name"]: (node["input_shape_hwc"], node["output_shape_hwc"])
                    for node in graph["nodes"] if node.get("name") in LAYERS}
    expected_shapes = {name: ([18, 32, cin], [18, 32, cout])
                       for name, (cin, cout) in LAYERS.items()}
    if graph_shapes != expected_shapes:
        raise AssertionError("frozen graph shape mismatch")
    concat10 = next(node for node in graph["nodes"] if node.get("name") == "concat.10")
    if concat10["inputs"] != ["down4_bu.pw.conv", "sppf.out.conv"] or concat10["shape_hwc"] != [18, 32, 192]:
        raise AssertionError("concat.10 source-channel order drifted")
    lut, lut_segment = load_segment(manifest, payload, "shared.silu")
    if not np.array_equal(lut, tables()["silu"]):
        raise AssertionError("package SiLU differs from cnn.integer")
    silu_file = write_hex(HERE / "silu_table.hex", lut, 16, True)
    silu_file.update({"ordering": "address_0_to_1023",
                      "source_segment_sha256": lut_segment["sha256"]})

    squeeze, squeeze_segments = load_layer(manifest, payload, "sppf.squeeze.conv", 96, 24)
    reduce, reduce_segments = load_layer(manifest, payload, "fuse4_bu.reduce.conv", 192, 96)
    input96 = deterministic_input(96, 0x9618)
    input192 = deterministic_input(192, 0x1928)
    arrays96, checks96 = golden(input96, squeeze, "sppf.squeeze.conv")
    full192, full192_checks = golden(input192, reduce, "fuse4_bu.reduce.conv", verify_banks=False)
    cases = [emit_case("p96_squeeze", 1, 96, 24, 0, "sppf.squeeze.conv",
                       arrays96, checks96, squeeze_segments, 0x9618)]

    slice_outputs: dict[str, list[np.ndarray]] = {field: [] for field in ("acc", "pre", "silu", "post")}
    for slab in range(8):
        offset = slab * 12
        sliced_parameters = {**reduce, "weights": reduce["weights"][offset:offset + 12],
                             "bias": reduce["bias"][offset:offset + 12],
                             "pre_multiplier": reduce["pre_multiplier"][offset:offset + 12],
                             "pre_shift": reduce["pre_shift"][offset:offset + 12]}
        slab_arrays, slab_checks = golden(input192, sliced_parameters,
                                          f"fuse4_bu.reduce.conv[{offset}:{offset + 12}]")
        for field in slice_outputs:
            expected = full192[field][..., offset:offset + 12]
            if not np.array_equal(slab_arrays[field], expected):
                raise AssertionError(f"slab {slab} {field} differs from full-layer golden")
            slice_outputs[field].append(slab_arrays[field])
        slab_segments = [record for record in reduce_segments if record["name"].endswith((
            ".post_multiplier", ".post_shift"))]
        cases.append(emit_case(f"p192_slice{slab:02d}", 2, 192, 12, offset,
                               "fuse4_bu.reduce.conv", slab_arrays, slab_checks,
                               slab_segments + [{"parent_segment": record["name"],
                                                 "parent_sha256": record["sha256"],
                                                 "slice": [offset, offset + 12]}
                                                for record in reduce_segments
                                                if not record["name"].endswith((".post_multiplier", ".post_shift"))],
                               0x1928))

    reassembly = {}
    for field, slabs in slice_outputs.items():
        joined = np.concatenate(slabs, axis=-1)
        if not np.array_equal(joined, full192[field]):
            raise AssertionError(f"192-layer {field} slab reassembly mismatch")
        reassembly[field] = {"values": int(joined.size), "exact": True,
                             "full_sha256": array_sha256(full192[field]),
                             "reassembled_sha256": array_sha256(joined)}

    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    if [item["name"] for item in baseline["cases"]] != [
            "cls_package", "reg_package", "extrema_channel_scale", "zero_bias_limits"]:
        raise AssertionError("PW48 compatibility case set drifted")
    contract = {
        "schema_version": 1,
        "profiles": {
            "0": {"shape": "48->48", "source": "../pw48_tile_20261015", "duplicated": False},
            "1": {"shape": "96->24", "case": "p96_squeeze"},
            "2": {"shape": "192->12", "cases": [f"p192_slice{i:02d}" for i in range(8)]},
        },
        "task_order": "position then local_output_group; 3 outputs per task",
        "reduction": "Cin/8 sequential input groups, 8 products per output per group",
        "input_bank": "bank=ic%8,row=position*(Cin/8)+ic//8; depth 192 for Cin96, 384 for Cin192",
        "weight_bank": "bank=(local_oc%3)*8+ic%8,row=(local_oc//3)*(Cin/8)+ic//8; always 24 banks x 96",
        "parameter_bank": "3 banks,row=local_oc//3; 8 rows for Cout24, 4 rows for Cout12",
        "concat_10_input": "HWC channels are contiguous in frozen graph order: down4_bu.pw.conv then sppf.out.conv; no channel reorder",
        "numeric": "signed33 every prefix; final INT32; cnn.integer exact RNE, Q7.8 SiLU, post INT8",
        "limits": "fixed profiles only; 12-bit load addresses unchanged; no graph/global output writer",
    }
    contract_path = HERE / "reference_contract.json"
    contract_path.write_text(json.dumps(contract, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    receipt = {
        "schema_version": 1, "status": "PASS",
        "qualification": "RETAINED_QAT_G10_PARAMETERS_DETERMINISTIC_RANDOM_INPUT_NOT_ACCURACY_EVIDENCE",
        "baseline": {"branch": "work/roadyolo", "commit": "9661d2ae827a4197cedacd621dd05fbc1006d762"},
        "sources": {
            "reference.py": sha256(Path(__file__)), "reference_contract.json": sha256(contract_path),
            "package_manifest": {"path": str(MANIFEST_PATH.relative_to(ROOT)).replace("\\", "/"),
                                 "sha256": EXPECTED_MANIFEST_SHA256, "status": manifest["status"]},
            "package_payload": {"path": str(PAYLOAD_PATH.relative_to(ROOT)).replace("\\", "/"),
                                "sha256": EXPECTED_PAYLOAD_SHA256},
            "checkpoint_sha256": manifest["provenance"]["checkpoint_sha256"],
            "generator_sha256": manifest["generator_sha256"],
            "deployment_contract_sha256": manifest["contract_sha256"],
            "graph_artifact_sha256": sha256(GRAPH_PATH),
            "graph_core_source_sha256": live_graph_sources,
            "export_qat_front3_sha256": sha256(ROOT / "cnn/hw_validation/production/export_qat_front3.py"),
            "pw48_reference_receipt_sha256": sha256(BASELINE),
            "shared_silu_segment": lut_segment,
        },
        "contract": contract, "cases": cases,
        "common_files": {"silu_table": silu_file},
        "compatibility_profile0": {"reused_not_duplicated": True,
            "directory": "../pw48_tile_20261015", "cases": [item["name"] for item in baseline["cases"]],
            "all_four_direct_conv_match": all(item["checks"]["direct_conv_match"] for item in baseline["cases"])},
        "full_layer_checks": {"fuse4_bu.reduce.conv": {
            "shape": [4, 4, 96], "computed_once_before_slicing": True,
            "all_eight_slabs_reassemble_exactly": True, "phases": reassembly,
            "signed33_prefix_values": full192_checks["signed33_prefix_values"],
            "signed33_group_prefix_values": full192_checks["signed33_group_prefix_values"],
            "final_int32_values": full192_checks["final_int32_values"]}},
        "verification": {"new_cases": len(cases), "compatibility_cases": 4,
            "all_slice_phase_golden": True, "all_bank_bijections": True,
            "all_signed33_prefixes_checked": True, "all_final_accumulators_int32": True,
            "universal_signed33_bound": {
                "max_abs_bias": 1 << 31, "max_products": 192,
                "max_abs_product": 128 * 128, "max_abs_sum": (1 << 31) + 192 * 128 * 128,
                "signed33_abs_limit": 1 << 32, "safe": (1 << 31) + 192 * 128 * 128 < (1 << 32),
                "note": "covers all legal INT8 inputs/weights and INT32 bias; final INT32 remains vector-checked"},
            "no_cuda": True, "training_updates": 0, "full_network_forwards": 0,
            "no_accuracy_claim": True, "rtl_compared": False},
    }
    (HERE / "reference_receipt.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "cases": [item["name"] for item in cases],
                      "receipt": "reference_receipt.json"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
