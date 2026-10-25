"""Export CSP3/CSP4 real-road CPU golden vectors from the frozen PTQ package.

Only the existing integer reference is used.  This does not train, run RTL,
invoke a GPU, synthesize, implement, build a bitstream, or touch a board.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
from pathlib import Path

os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import numpy as np
import torch


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[4]
sys.path.insert(0, str(PROJECT))

from cnn.integer import conv2d, requantize, silu, tables  # noqa: E402
from cnn.hw_validation.production.trained_integer import (  # noqa: E402
    conv_exact,
    load_package,
    nonconv,
)

torch.set_num_threads(1)


GRAPH_PATH = PROJECT / "cnn/hw_validation/production/graph_artifacts/graph.json"
PACKAGE = PROJECT / "cnn/reports/qat_frozen_stem_g10_20261014_v1/package"
PREFIX = PROJECT / "cnn/hw_validation/production/model_handoff_20261015/artifacts/golden_prefix"
PREFIX_INDEX = PROJECT / "cnn/hw_validation/production/model_handoff_20261015/artifacts/golden_prefix_index.json"
HANDOFF_RECEIPT = PROJECT / "cnn/hw_validation/production/model_handoff_20261015/artifacts/receipt.json"
CSP2_ROAD_MANIFEST = PROJECT / "cnn/hw_validation/production/csp2_complete_20261015/reference/road_input/manifest.json"
PAYLOAD_SHA256 = "b35d4a66a69e441dc29bc60c7e3f507661f48da5f33b810d7340f6ed17a65145"
RGB_NPY_SHA256 = "cb8a0f3cbdecdf52b480d3dc42d800b5fbcc9758fc1ef1ed8cab7bb7e57104e3"
IMAGE_SHA256 = "2aa54183d41253020bb1d51ea7a2ba93525d921cfb8948a7a65ac4f86cab7363"
MARKER = "TRAINED_PTQ_DIAGNOSTIC_NOT_QAT_NOT_BOARD_QUALIFIED"

FAMILY_STAGES = {
    "csp3": [
        "csp3.blocks.0.dw.conv",
        "csp3.blocks.0.pw.conv",
        "csp3.blocks.1.dw.conv",
        "csp3.blocks.1.pw.conv",
        "csp3.blocks.2.dw.conv",
        "csp3.blocks.2.pw.conv",
        "csp3.out.conv",
    ],
    "csp4": [
        "csp4.blocks.0.dw.conv",
        "csp4.blocks.0.pw.conv",
        "csp4.blocks.1.dw.conv",
        "csp4.blocks.1.pw.conv",
        "csp4.blocks.2.dw.conv",
        "csp4.blocks.2.pw.conv",
        "csp4.out.conv",
    ],
}

FAMILY_META = {
    "csp3": {
        "tag": 0,
        "height": 36,
        "width": 64,
        "half_channels": 24,
        "full_channels": 48,
        "source_producers": ["down3.dw.conv", "down3.pw.conv"],
        "source_tensor": "down3.pw.conv",
        "split": "split.01",
        "residuals": ["residual.02", "residual.03", "residual.04"],
        "concat": "concat.01",
    },
    "csp4": {
        "tag": 1,
        "height": 18,
        "width": 32,
        "half_channels": 48,
        "full_channels": 96,
        "source_producers": ["down4.dw.conv", "down4.pw.conv"],
        "source_tensor": "down4.pw.conv",
        "split": "split.02",
        "residuals": ["residual.05", "residual.06", "residual.07"],
        "concat": "concat.02",
    },
}

BITS = {"acc": 32, "pre": 16, "silu": 16, "post": 8, "sum": 16, "output": 8}
PARAM_BITS = {
    "weights": 8,
    "bias": 32,
    "pre_multiplier": 32,
    "pre_shift": 8,
    "post_multiplier": 32,
    "post_shift": 8,
}


def sha256(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def emit_hex(path: Path, values: np.ndarray, bits: int) -> None:
    flat = np.asarray(values).ravel(order="C")
    mask = (1 << bits) - 1
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="ascii", newline="\n") as stream:
        for begin in range(0, flat.size, 8192):
            stream.writelines(
                f"{int(value) & mask:0{bits // 4}x}\n" for value in flat[begin:begin + 8192]
            )


def graph_index(graph: dict) -> tuple[dict[str, dict], dict[str, dict]]:
    nodes = {node["name"]: node for node in graph["nodes"]}
    producers: dict[str, dict] = {}
    for node in graph["nodes"]:
        if node["op"] == "split_view":
            for view in node["outputs"]:
                producers[view["output"]] = node
        else:
            producers[node["output"]] = node
    return nodes, producers


def storage_of(tensor: str, nodes: dict[str, dict], producers: dict[str, dict]) -> tuple[dict, int]:
    producer = producers[tensor]
    if producer["op"] == "conv":
        return producer["storage"], 0
    if producer["op"] == "residual_view":
        return nodes[producer["storage_alias"]]["storage"], 0
    if producer["op"] == "split_view":
        view = next(row for row in producer["outputs"] if row["output"] == tensor)
        parent_storage, parent_offset = storage_of(producer["inputs"][0], nodes, producers)
        return parent_storage, parent_offset + view["channel_offset"]
    raise ValueError(f"{tensor}: no single storage backing")


def source_views(tensor: str, channels: int, nodes: dict[str, dict], producers: dict[str, dict]) -> list[dict]:
    producer = producers[tensor]
    if producer["op"] == "concat_view":
        rows, logical = [], 0
        for name in producer["inputs"]:
            input_producer = producers[name]
            if input_producer["op"] == "split_view":
                width = next(row["channels"] for row in input_producer["outputs"] if row["output"] == name)
            elif input_producer["op"] == "residual_view":
                width = input_producer["shape_hwc"][2]
            else:
                width = input_producer.get("output_shape_hwc", input_producer.get("shape_hwc"))[2]
            storage, offset = storage_of(name, nodes, producers)
            rows.append({
                "tensor": name,
                "logical_channel_offset": logical,
                "channels": width,
                "base": storage["base"],
                "stored_channels": storage["channels_stored"],
                "physical_channel_offset": offset,
            })
            logical += width
        if logical != channels:
            raise ValueError(f"{tensor}: concat channel count changed")
        return rows
    storage, offset = storage_of(tensor, nodes, producers)
    return [{
        "tensor": tensor,
        "logical_channel_offset": 0,
        "channels": channels,
        "base": storage["base"],
        "stored_channels": storage["channels_stored"],
        "physical_channel_offset": offset,
    }]


def physical_address(view: dict, height: int, width: int, y: int, x: int, logical_channel: int) -> int:
    local_channel = logical_channel - view["logical_channel_offset"]
    if not 0 <= local_channel < view["channels"]:
        raise ValueError("logical channel outside source view")
    tile_cols = math.ceil(width / 4)
    pixel = ((y // 4) * tile_cols + x // 4) * 16 + (y % 4) * 4 + x % 4
    return view["base"] + pixel * view["stored_channels"] + view["physical_channel_offset"] + local_channel


def view_for_channel(views: list[dict], channel: int) -> dict:
    return next(view for view in views
                if view["logical_channel_offset"] <= channel
                < view["logical_channel_offset"] + view["channels"])


def expected_reads(node: dict, views: list[dict], bypass_views: list[dict] | None = None) -> tuple[int, int, int]:
    height, width, input_channels = node["input_shape_hwc"]
    output_height, output_width, _ = node["output_shape_hwc"]
    tile_rows, tile_cols = math.ceil(output_height / 4), math.ceil(output_width / 4)
    lines: list[int] = []
    current_line = None
    count = 0

    def consume(address: int) -> None:
        nonlocal current_line, count
        line = address & ~15
        lines.append(line)
        if line != current_line:
            count += 1
            current_line = line

    if node["groups"] == input_channels:
        for tile_y in range(tile_rows):
            for tile_x in range(tile_cols):
                for local_y in range(6):
                    for local_x in range(6):
                        in_y = tile_y * 4 * node["stride"][0] + local_y - node["padding"][0]
                        in_x = tile_x * 4 * node["stride"][1] + local_x - node["padding"][1]
                        if 0 <= in_y < height and 0 <= in_x < width:
                            for channel in range(input_channels):
                                consume(physical_address(
                                    view_for_channel(views, channel), height, width, in_y, in_x, channel
                                ))
    else:
        for tile_y in range(tile_rows):
            for tile_x in range(tile_cols):
                positions = [(y, x) for y in range(tile_y * 4, min(output_height, tile_y * 4 + 4))
                             for x in range(tile_x * 4, min(output_width, tile_x * 4 + 4))]
                for y, x in positions:
                    for channel in range(input_channels):
                        consume(physical_address(
                            view_for_channel(views, channel), height, width, y, x, channel
                        ))
                if bypass_views:
                    for y, x in positions:
                        for channel in range(node["output_shape_hwc"][2]):
                            consume(physical_address(
                                view_for_channel(bypass_views, channel), output_height, output_width, y, x, channel
                            ))
    return count, min(lines), max(lines)


def stage_contract(local_stage: int, node: dict, nodes: dict, producers: dict) -> dict:
    height, width, input_channels = node["input_shape_hwc"]
    output_height, output_width, output_channels = node["output_shape_hwc"]
    views = source_views(node["inputs"][0], input_channels, nodes, producers)
    tile_rows, tile_cols = math.ceil(output_height / 4), math.ceil(output_width / 4)
    output_groups = math.ceil(output_channels / 3)
    input_groups = math.ceil(input_channels / 8)
    is_dw = node["groups"] == input_channels
    tasks = (output_height * tile_cols * 2 * output_channels if is_dw
             else output_height * output_width * output_groups)
    groups_per_task = math.ceil(math.prod(node["kernel"]) / 8) if is_dw else input_groups
    dw_records_per_tile_channel = math.ceil(15 / 8) + math.ceil(9 / 8)
    parameter_requests = (tile_rows * tile_cols * output_channels * dw_records_per_tile_channel if is_dw
                          else tile_rows * tile_cols * output_groups * input_groups)
    destination = node["storage"]
    residual = node.get("write_transform", {}).get("op") == "post_silu_output_requant_add_sat8"
    bypass = node.get("write_transform", {}).get("bypass") if residual else None
    bypass_views = source_views(bypass, output_channels, nodes, producers) if bypass else []
    reads, read_min, read_max = expected_reads(node, views, bypass_views)
    last_y, last_x = output_height - 1, output_width - 1
    destination_view = {
        "logical_channel_offset": 0,
        "channels": output_channels,
        "base": destination["base"],
        "stored_channels": destination["channels_stored"],
        "physical_channel_offset": 0,
    }
    return {
        "stage": local_stage,
        "graph_node_index": node["index"],
        "name": node["name"],
        "kind": "dw" if is_dw else ("fuse" if local_stage == 6 else "pw"),
        "kernel": node["kernel"],
        "stride": node["stride"],
        "padding": node["padding"],
        "groups": node["groups"],
        "input_shape_hwc": node["input_shape_hwc"],
        "output_shape_hwc": node["output_shape_hwc"],
        "source_views": views,
        "destination": destination,
        "destination_valid_address_min": destination["base"],
        "destination_valid_address_max": physical_address(
            destination_view, output_height, output_width, last_y, last_x, output_channels - 1
        ),
        "residual": residual,
        "bypass_tensor": bypass,
        "bypass_views": bypass_views,
        "output_group_count": output_groups,
        "input_group_count": groups_per_task,
        "logical_channel_group_count": input_groups,
        "input_group_count_semantics": (
            "accepted packed core groups per task; DW is two spatial kernel groups, "
            "not logical input channels divided by eight"
        ),
        "task_count": tasks,
        "accepted_core_groups": tasks * groups_per_task,
        "accepted_core_groups_per_task": groups_per_task,
        "expected_parameter_requests": parameter_requests,
        "expected_parameter_responses": parameter_requests,
        "dw_parameter_records_per_tile_channel": dw_records_per_tile_channel if is_dw else None,
        "expected_read_requests": reads,
        "read_line_address_min": read_min,
        "read_line_address_max": read_max,
        "logical_output_elements": output_height * output_width * output_channels,
        "tile_rows": tile_rows,
        "tile_cols": tile_cols,
        "last_tile_valid_rows": output_height - (tile_rows - 1) * 4,
        "last_tile_valid_cols": output_width - (tile_cols - 1) * 4,
        "dw_spatial_tasks_per_4wide_row": "3-lane x+0..2 then lane0-only x+3" if is_dw else None,
        "vector_files": {field: f"vectors/stage{local_stage}_{field}.hex" for field in BITS},
        "parameter_files": {field: f"parameters/stage{local_stage}_{field}.hex" for field in PARAM_BITS},
    }


def verify_csp2_read_model(nodes: dict, producers: dict) -> None:
    expected = {
        "csp2.blocks.0.dw.conv": 30210,
        "csp2.blocks.0.pw.conv": 20736,
        "csp2.blocks.1.dw.conv": 16748,
        "csp2.blocks.1.pw.conv": 13824,
        "csp2.out.conv": 27648,
    }
    for name, count in expected.items():
        node = nodes[name]
        views = source_views(node["inputs"][0], node["input_shape_hwc"][2], nodes, producers)
        bypass = node.get("write_transform", {}).get("bypass")
        bypass_views = source_views(bypass, node["output_shape_hwc"][2], nodes, producers) if bypass else []
        actual, _, _ = expected_reads(node, views, bypass_views)
        if actual != count:
            raise AssertionError(f"{name}: read model {actual} != frozen CSP2 ledger {count}")


def build_contract(graph: dict) -> dict:
    nodes, producers = graph_index(graph)
    verify_csp2_read_model(nodes, producers)
    families = {}
    for family, meta in FAMILY_META.items():
        graph_semantics = verify_family_graph_semantics(family, nodes)
        stages = [stage_contract(index, nodes[name], nodes, producers)
                  for index, name in enumerate(FAMILY_STAGES[family])]
        height, width = meta["height"], meta["width"]
        families[family] = {
            "family": family,
            "tag": meta["tag"],
            "height": height,
            "width": width,
            "half_channels": meta["half_channels"],
            "full_channels": meta["full_channels"],
            "tile_rows": math.ceil(height / 4),
            "tile_cols": math.ceil(width / 4),
            "last_tile_valid_rows": height % 4 or 4,
            "last_tile_valid_cols": width % 4 or 4,
            "source_tensor": meta["source_tensor"],
            "source_shape_hwc": [height, width, meta["full_channels"]],
            "source_producers": [nodes[name] for name in meta["source_producers"]],
            "split_node": nodes[meta["split"]],
            "residual_nodes": [nodes[name] for name in meta["residuals"]],
            "concat_node": nodes[meta["concat"]],
            "graph_semantics": graph_semantics,
            "stages": stages,
            "totals": {
                "stages": 7,
                "logical_output_elements": sum(row["logical_output_elements"] for row in stages),
                "all_acc_pre_silu_post_sum_output_values": 6 * sum(
                    row["logical_output_elements"] for row in stages
                ),
                "task_count": sum(row["task_count"] for row in stages),
                "accepted_core_groups": sum(row["accepted_core_groups"] for row in stages),
                "expected_parameter_requests": sum(row["expected_parameter_requests"] for row in stages),
                "expected_read_requests": sum(row["expected_read_requests"] for row in stages),
            },
            "tail_rule": "only y < height is written; physical 4x4 tail padding rows are not expected writes",
        }
    pan_names = [
        "fuse3_bu.reduce.conv", "split.05", "fuse3_bu.block.dw.conv",
        "fuse3_bu.block.pw.conv", "residual.10", "concat.09",
    ]
    return {
        "schema": "csp_family_layer_reference_v2_residual_bypass_corrected",
        "status": MARKER,
        "scope": "CPU-only corrected CSP3/CSP4 integer reference from existing C2 output; not an RTL-prefix claim",
        "payload_sha256": PAYLOAD_SHA256,
        "rgb_npy_sha256": RGB_NPY_SHA256,
        "graph_sha256": sha256(GRAPH_PATH),
        "layout": {
            "logical_vectors": "HWC row-major, channel fastest",
            "weights": "OIHW row-major",
            "tile4x4_hwc_address": "base + ((((y//4)*tile_cols + x//4)*16 + (y%4)*4 + x%4)*stored_channels + channel_offset + c)",
            "read_address": "tile4x4_hwc byte address rounded down to a 16-byte line",
            "hex": "one lowercase zero-padded two's-complement value per line",
            "bits": BITS,
            "parameter_bits": PARAM_BITS,
        },
        "scheduler": {
            "tile": [4, 4],
            "mac_input_lanes": 8,
            "mac_output_lanes": 3,
            "dw_4wide_schedule": ["x+0,x+1,x+2", "x+3 on lane0 only"],
            "pw_output_channel_tail": False,
        },
        "resource_capacity_model_not_synthesis": {
            "eram_count": 4,
            "raw_capacity_bytes": 10240,
            "dw_operand_cache_max_bytes": 1728,
            "pw_operand_cache_max_bytes": 1536,
            "resident_weight_bytes": 288,
            "dynamic_parameter_bytes": 31,
            "memory_line_bytes": 16,
            "maximum_live_bytes": 2063,
            "fits_raw_capacity": True,
            "synthesis_or_timing_claim": False,
        },
        "families": families,
        "pan_dependency_handoff_read_only": {
            "exact_producers": [nodes[name] for name in pan_names],
            "final_tensor": "concat.09",
            "extra_out_conv": False,
            "note": "FusionCSP is reduce PW, split, DW, PW residual, concat; do not invent an out.conv",
        },
        "not_run": ["training", "GPU", "RTL", "simulation", "TD", "synthesis", "bitstream", "board"],
        "acceptance_eligible": False,
    }


def execute_conv(node: dict, source: np.ndarray, parameters: dict, *, scalar_check: bool) -> dict[str, np.ndarray]:
    p = parameters[node["name"]]
    acc = conv_exact(source, p["weights"], p["bias"], node["stride"][0], node["padding"][0], node["groups"])
    if scalar_check:
        oracle = conv2d(source, p["weights"], p["bias"], node["stride"][0], node["padding"][0], node["groups"])
        np.testing.assert_array_equal(acc, oracle)
    pre = requantize(acc, p["pre_multiplier"], p["pre_shift"], -32768, 32767).astype(np.int16)
    activated = silu(pre)
    post = requantize(activated, p["post_multiplier"], p["post_shift"]).astype(np.int8)
    return {"acc": acc, "pre": pre, "silu": activated, "post": post}


def verify_family_graph_semantics(family: str, nodes: dict) -> dict:
    meta = FAMILY_META[family]
    split = nodes[meta["split"]]
    concat = nodes[meta["concat"]]
    if split["op"] != "split_view" or split["inputs"] != [meta["source_tensor"]]:
        raise AssertionError(f"{family}: split does not consume the frozen family source")
    if [view["channels"] for view in split["outputs"]] != [meta["half_channels"]] * 2:
        raise AssertionError(f"{family}: split widths differ from the frozen half channels")
    residual_checks = []
    for stage, residual_name in zip((1, 3, 5), meta["residuals"], strict=True):
        conv = nodes[FAMILY_STAGES[family][stage]]
        residual = nodes[residual_name]
        transform = conv.get("write_transform", {})
        if transform.get("op") != "post_silu_output_requant_add_sat8":
            raise AssertionError(f"{conv['name']}: frozen residual write transform missing")
        if not transform.get("requires_aligned_int8_scale"):
            raise AssertionError(f"{conv['name']}: residual scale alignment not required")
        if residual["op"] != "residual_view" or residual["inputs"] != [transform["bypass"], conv["output"]]:
            raise AssertionError(f"{conv['name']}: write_transform and residual_view disagree")
        if residual["storage_alias"] != conv["output"]:
            raise AssertionError(f"{residual_name}: storage alias is not the PW destination")
        residual_checks.append({
            "stage": stage,
            "conv": conv["name"],
            "bypass": transform["bypass"],
            "residual_view": residual_name,
            "residual_inputs": residual["inputs"],
            "storage_alias": residual["storage_alias"],
            "requires_aligned_int8_scale": True,
        })
    if concat["op"] != "concat_view" or concat["inputs"] != [split["outputs"][0]["output"], meta["residuals"][-1]]:
        raise AssertionError(f"{family}: final concat aliases differ from the frozen graph")
    return {"split": split["name"], "concat": concat["name"], "residuals": residual_checks}


def execute_family(family: str, source: np.ndarray, nodes: dict, parameters: dict) -> tuple[list[dict], np.ndarray, list[dict]]:
    meta = FAMILY_META[family]
    graph_check = verify_family_graph_semantics(family, nodes)
    values = {meta["source_tensor"]: source}
    values.update(nonconv(nodes[meta["split"]], values))
    residual_by_branch = {nodes[name]["inputs"][1]: nodes[name] for name in meta["residuals"]}
    captured = []
    negative_checks = []
    for local_stage, name in enumerate(FAMILY_STAGES[family]):
        node = nodes[name]
        source_name = node["inputs"][0]
        if source_name not in values:
            producer = nodes[meta["concat"]]
            if producer["output"] != source_name:
                raise AssertionError(f"{name}: named input {source_name} is unavailable")
            values.update(nonconv(producer, values))
        conv_source = values[source_name]
        fields = execute_conv(node, conv_source, parameters, scalar_check=True)
        values[node["output"]] = fields["post"]
        transform = node.get("write_transform")
        if transform:
            residual = residual_by_branch[node["output"]]
            values.update(nonconv(residual, values))
            output = values[residual["output"]]
            bypass = values[transform["bypass"]]
            total = bypass.astype(np.int16) + fields["post"].astype(np.int16)
            np.testing.assert_array_equal(output, np.clip(total, -128, 127).astype(np.int8))

            old_wrong_total = conv_source.astype(np.int16) + fields["post"].astype(np.int16)
            old_wrong_output = np.clip(old_wrong_total, -128, 127).astype(np.int8)
            mismatch = np.flatnonzero(output.ravel() != old_wrong_output.ravel())
            if mismatch.size == 0:
                raise AssertionError(f"{name}: real-road negative cannot distinguish the old DW-post bypass")
            first = int(mismatch[0])
            negative_checks.append({
                "stage": local_stage,
                "conv": name,
                "graph_bypass": transform["bypass"],
                "old_wrong_bypass": source_name,
                "mismatch_values": int(mismatch.size),
                "first_mismatch_flat_index": first,
                "correct_output": int(output.ravel()[first]),
                "old_wrong_output": int(old_wrong_output.ravel()[first]),
                "old_wrong_rejected": True,
            })
        else:
            total = fields["post"].astype(np.int16)
            output = fields["post"]
        fields.update(sum=total, output=output)
        captured.append(fields)
    graph_check["real_road_old_wrong_bypass_negative"] = negative_checks
    return captured, values[nodes[FAMILY_STAGES[family][-1]]["output"]], graph_check


def verify_schedule_coverage(contract: dict) -> dict:
    checks = {}
    for family, family_contract in contract["families"].items():
        family_checks = []
        for stage in family_contract["stages"]:
            height, width, channels = stage["output_shape_hwc"]
            coverage = np.zeros((height, width, channels), dtype=np.uint8)
            if stage["kind"] == "dw":
                for y in range(height):
                    for tile_x in range(stage["tile_cols"]):
                        x = tile_x * 4
                        for channel in range(channels):
                            coverage[y, x:x + 3, channel] += 1
                            coverage[y, x + 3, channel] += 1
            else:
                for y in range(height):
                    for x in range(width):
                        for begin in range(0, channels, 3):
                            coverage[y, x, begin:min(begin + 3, channels)] += 1
            if not np.all(coverage == 1):
                raise AssertionError(f"{family} stage{stage['stage']}: schedule coverage is not exactly once")
            family_checks.append({
                "stage": stage["stage"],
                "covered_once": int(np.count_nonzero(coverage == 1)),
                "minimum": int(coverage.min()),
                "maximum": int(coverage.max()),
            })
        if family == "csp4" and family_contract["last_tile_valid_rows"] != 2:
            raise AssertionError("CSP4 last tile must contain exactly two valid rows")
        checks[family] = family_checks
    return checks


def export_family(family: str, source: np.ndarray, stages: list[dict], parameters: dict,
                  family_contract: dict) -> dict:
    family_root = ROOT / family
    vector_root = family_root / "vectors"
    numpy_root = family_root / "npy"
    parameter_root = family_root / "parameters"
    for directory in (vector_root, numpy_root, parameter_root):
        directory.mkdir(parents=True, exist_ok=True)
    emit_hex(vector_root / "source.hex", source, 8)
    np.save(numpy_root / "source.npy", source, allow_pickle=False)
    vector_rows = {"source.hex": {"shape": list(source.shape), "dtype": str(source.dtype), "bits": 8}}
    numpy_rows = {"source.npy": {"shape": list(source.shape), "dtype": str(source.dtype)}}
    parameter_rows = {}
    emit_hex(parameter_root / "silu.hex", np.asarray(tables()["silu"], dtype=np.int16), 16)
    parameter_rows["silu.hex"] = {"shape": [1024], "dtype": "int16", "bits": 16, "layout": "LUT"}
    for index, (name, fields) in enumerate(zip(FAMILY_STAGES[family], stages, strict=True)):
        for field, bits in BITS.items():
            hex_name = f"stage{index}_{field}.hex"
            npy_name = f"stage{index}_{field}.npy"
            emit_hex(vector_root / hex_name, fields[field], bits)
            np.save(numpy_root / npy_name, fields[field], allow_pickle=False)
            vector_rows[hex_name] = {"shape": list(fields[field].shape), "dtype": str(fields[field].dtype), "bits": bits}
            numpy_rows[npy_name] = {"shape": list(fields[field].shape), "dtype": str(fields[field].dtype)}
        for field, bits in PARAM_BITS.items():
            values = parameters[name][field]
            filename = f"stage{index}_{field}.hex"
            emit_hex(parameter_root / filename, values, bits)
            parameter_rows[filename] = {
                "shape": list(values.shape),
                "dtype": str(values.dtype),
                "bits": bits,
                "layout": "OIHW" if field == "weights" else "C" if values.size > 1 else "scalar",
            }
    contract = {
        "status": MARKER,
        "scope": f"CPU-only {family.upper()} seven-stage reference; source is existing downsample PW output",
        "payload_sha256": PAYLOAD_SHA256,
        "rgb_npy_sha256": RGB_NPY_SHA256,
        "family": family_contract,
        "files": {"vectors": vector_rows, "npy": numpy_rows, "parameters": parameter_rows},
        "full_scalar_conv2d_oracle_checked": True,
        "rtl_or_simulation_or_training_run": False,
    }
    save_json(family_root / "contract.json", contract)
    return contract


def source_closure() -> dict[str, str]:
    paths = [
        Path(__file__), GRAPH_PATH,
        PREFIX_INDEX, HANDOFF_RECEIPT, PREFIX / "input_rgb_hwc.npy",
        PREFIX / "csp2.out.conv.post.npy", CSP2_ROAD_MANIFEST,
        PROJECT / "cnn/hw_validation/production/trained_integer.py",
        PROJECT / "cnn/hw_validation/production/graph.py",
        PROJECT / "cnn/hw_validation/production/deployment_contract.json",
        PROJECT / "cnn/integer.py",
        PROJECT / "cnn/model.py",
        PROJECT / "cnn/contract.json",
        *sorted(path for path in PACKAGE.iterdir() if path.is_file()),
    ]
    return {path.relative_to(PROJECT).as_posix(): sha256(path) for path in paths}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract-only", action="store_true")
    args = parser.parse_args()
    graph = read_json(GRAPH_PATH)
    package_manifest = read_json(PACKAGE / "manifest.json")
    prefix_index = read_json(PREFIX_INDEX)
    handoff = read_json(HANDOFF_RECEIPT)
    if package_manifest["payload_sha256"] != PAYLOAD_SHA256 or sha256(PACKAGE / "numeric_test.bin") != PAYLOAD_SHA256:
        raise ValueError("frozen package payload changed")
    if package_manifest["status"] != MARKER or package_manifest["graph"] != graph:
        raise ValueError("package status or frozen graph differs from graph artifact")
    if sha256(PREFIX / "input_rgb_hwc.npy") != RGB_NPY_SHA256:
        raise ValueError("real-road RGB tensor changed")
    if handoff["payload_sha256"] != PAYLOAD_SHA256 or prefix_index["image_sha256"] != IMAGE_SHA256:
        raise ValueError("model handoff identity changed")
    contract = build_contract(graph)
    save_json(ROOT / "family_contract.json", contract)
    if args.contract_only:
        print("PASS_FAMILY_CONTRACT")
        return

    before = source_closure()
    os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")
    model, loaded_manifest = load_package(PACKAGE)
    if loaded_manifest["payload_sha256"] != PAYLOAD_SHA256:
        raise ValueError("validated package payload changed")
    nodes, _ = graph_index(graph)
    csp2 = np.load(PREFIX / "csp2.out.conv.post.npy", allow_pickle=False)
    if csp2.shape != (72, 128, 24) or csp2.dtype != np.int8:
        raise ValueError("existing C2 output shape/dtype changed")

    down3_dw = execute_conv(nodes["down3.dw.conv"], csp2, model.parameters, scalar_check=True)["post"]
    csp3_source = execute_conv(nodes["down3.pw.conv"], down3_dw, model.parameters, scalar_check=True)["post"]
    csp3_stages, csp3_output, csp3_graph_checks = execute_family(
        "csp3", csp3_source, nodes, model.parameters
    )
    down4_dw = execute_conv(nodes["down4.dw.conv"], csp3_output, model.parameters, scalar_check=True)["post"]
    csp4_source = execute_conv(nodes["down4.pw.conv"], down4_dw, model.parameters, scalar_check=True)["post"]
    csp4_stages, csp4_output, csp4_graph_checks = execute_family(
        "csp4", csp4_source, nodes, model.parameters
    )

    contracts = {
        "csp3": export_family("csp3", csp3_source, csp3_stages, model.parameters, contract["families"]["csp3"]),
        "csp4": export_family("csp4", csp4_source, csp4_stages, model.parameters, contract["families"]["csp4"]),
    }
    coverage = verify_schedule_coverage(contract)
    after = source_closure()
    if before != after:
        raise AssertionError("read-only source closure changed during generation")
    status = {
        "status": "PASS_CPU_CSP3_CSP4_REFERENCE",
        "diagnostic_marker": MARKER,
        "scope": "C2 output -> CPU down3/CSP3/down4/CSP4 only; not RTL or complete-prefix evidence",
        "payload_sha256": PAYLOAD_SHA256,
        "image_sha256": prefix_index["image_sha256"],
        "rgb_npy_sha256": RGB_NPY_SHA256,
        "families": {
            "csp3": {"source_shape": list(csp3_source.shape), "output_shape": list(csp3_output.shape),
                     "stages": 7, "golden_values_all_fields": contracts["csp3"]["family"]["totals"]["all_acc_pre_silu_post_sum_output_values"]},
            "csp4": {"source_shape": list(csp4_source.shape), "output_shape": list(csp4_output.shape),
                     "stages": 7, "golden_values_all_fields": contracts["csp4"]["family"]["totals"]["all_acc_pre_silu_post_sum_output_values"]},
        },
        "full_scalar_conv2d_oracle_checked_stages": 18,
        "graph_nonconv_named_input_checks": {
            "csp3": csp3_graph_checks,
            "csp4": csp4_graph_checks,
        },
        "load_package_nonconv_scale_alignment_verified": True,
        "old_wrong_dw_post_bypass_rejected_for_all_six_real_residuals": all(
            row["old_wrong_rejected"]
            for family_checks in (csp3_graph_checks, csp4_graph_checks)
            for row in family_checks["real_road_old_wrong_bypass_negative"]
        ),
        "cuda_visible_devices": os.environ["CUDA_VISIBLE_DEVICES"],
        "torch_cuda_initialized": torch.cuda.is_initialized(),
        "schedule_coverage": coverage,
        "source_closure_before": before,
        "source_closure_after": after,
        "source_closure_unchanged": True,
        "not_run": contract["not_run"],
        "acceptance_eligible": False,
    }
    save_json(ROOT / "status.json", status)
    save_json(ROOT / "commands.json", {
        "python": "D:/anaconda3/python.exe",
        "environment": {"CUDA_VISIBLE_DEVICES": "", "OMP_NUM_THREADS": "1", "MKL_NUM_THREADS": "1"},
        "commands": [
            "D:/anaconda3/python.exe generate_reference.py --contract-only",
            "D:/anaconda3/python.exe generate_reference.py",
        ],
        "training_or_gpu_or_rtl_or_simulation_or_td_or_board": False,
    })

    artifacts = sorted(path for path in ROOT.rglob("*") if path.is_file()
                       and path.name not in {"manifest.json", "generate_reference.py"})
    manifest = {
        "status": MARKER,
        "payload_sha256": PAYLOAD_SHA256,
        "image_sha256": prefix_index["image_sha256"],
        "rgb_npy_sha256": RGB_NPY_SHA256,
        "source_sha256": after,
        "package_sha256": {
            "manifest.json": sha256(PACKAGE / "manifest.json"),
            "numeric_test.bin": PAYLOAD_SHA256,
        },
        "artifacts": {path.relative_to(ROOT).as_posix(): sha256(path) for path in artifacts},
        "artifact_count": len(artifacts),
        "model_package_copied": False,
        "immutable_after_generation": True,
    }
    save_json(ROOT / "manifest.json", manifest)
    print("PASS_CPU_CSP3_CSP4_REFERENCE")


if __name__ == "__main__":
    main()
