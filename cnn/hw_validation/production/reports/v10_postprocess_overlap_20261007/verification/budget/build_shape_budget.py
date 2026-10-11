"""Build structural cycle inputs from the frozen 67-convolution graph."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
GRAPH = ROOT.parents[3] / "graph_artifacts" / "graph.json"
OUTPUT = ROOT / "shape_budget.json"
RUNNER_LOG = ROOT.parent / "regression_candidate" / "vsim_attempt4.log"


def ceil_div(value: int, divisor: int) -> int:
    return (value + divisor - 1) // divisor


def main() -> None:
    raw = GRAPH.read_bytes()
    graph = json.loads(raw)
    layers = []
    for node in graph["nodes"]:
        if node["op"] != "conv":
            continue
        in_h, in_w, in_channels = node["input_shape_hwc"]
        out_h, out_w, out_channels = node["output_shape_hwc"]
        kernel_h, kernel_w = node["kernel"]
        groups = node["groups"]
        if node["name"] == "stem.conv":
            kind = "stem_regular"
        elif groups == in_channels == out_channels:
            kind = "depthwise"
        elif node["kernel"] == [1, 1] and groups == 1:
            kind = "pointwise"
        else:
            kind = "regular"
        terms = kernel_h * kernel_w * (in_channels // groups)
        input_groups_per_job = ceil_div(terms, 8)
        outputs = out_h * out_w * out_channels
        jobs = outputs if kind == "depthwise" else out_h * out_w * ceil_div(out_channels, 3)
        activated = node["dtype"] == "int8"
        layers.append({
            "index": node["index"],
            "name": node["name"],
            "kind": kind,
            "activated_silu": activated,
            "input_hwc": [in_h, in_w, in_channels],
            "output_hwc": [out_h, out_w, out_channels],
            "groups": groups,
            "kernel": [kernel_h, kernel_w],
            "terms_per_output": terms,
            "mac_input_groups_per_job": input_groups_per_job,
            "output_values": outputs,
            "mac_jobs": jobs,
            "physical_result_lanes": jobs * 3,
            "unused_result_lanes": jobs * 3 - outputs,
            "illustrative_cycles_2_per_group_plus_12_turnover":
                jobs * (2 * input_groups_per_job + 12),
            "fitted_job_cadence_cycles_2G_plus_10":
                jobs * (2 * input_groups_per_job + 10),
            "conditional_layer_boundary_cycles": 27 if kind == "depthwise" else 28,
        })

    by_kind = {}
    for kind in ("stem_regular", "regular", "depthwise", "pointwise"):
        selected = [layer for layer in layers if layer["kind"] == kind]
        by_kind[kind] = {
            "layers": len(selected),
            "output_values": sum(layer["output_values"] for layer in selected),
            "mac_jobs": sum(layer["mac_jobs"] for layer in selected),
            "mac_input_groups": sum(layer["mac_jobs"] * layer["mac_input_groups_per_job"]
                                    for layer in selected),
            "unused_result_lanes": sum(layer["unused_result_lanes"] for layer in selected),
            "illustrative_cycles_2_per_group_plus_12_turnover":
                sum(layer["illustrative_cycles_2_per_group_plus_12_turnover"]
                    for layer in selected),
            "fitted_job_cadence_cycles_2G_plus_10":
                sum(layer["fitted_job_cadence_cycles_2G_plus_10"]
                    for layer in selected),
            "conditional_layer_boundary_cycles":
                sum(layer["conditional_layer_boundary_cycles"] for layer in selected),
        }

    activation_counts = Counter(layer["activated_silu"] for layer in layers)
    estimate = sum(layer["illustrative_cycles_2_per_group_plus_12_turnover"]
                   for layer in layers)
    fitted_jobs = sum(layer["fitted_job_cadence_cycles_2G_plus_10"] for layer in layers)
    fitted_boundaries = sum(layer["conditional_layer_boundary_cycles"] for layer in layers)
    fitted_total = fitted_jobs + fitted_boundaries
    runner_raw = RUNNER_LOG.read_bytes()
    report = {
        "status": "DOWN2_MEASURED_FIT_PLUS_CONDITIONAL_GRAPH_EXTRAPOLATION",
        "source": {
            "path": str(GRAPH),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "architecture_sha256": graph["architecture_sha256"],
            "graph_status": graph["status"],
        },
        "assumptions": [
            "One MAC job produces three outputs except current depthwise scheduling, which uses one selected lane and wastes two physical result lanes.",
            "Each job accepts ceil(kernel_h*kernel_w*(input_channels/groups)/8) MAC groups.",
            "The illustrative estimate applies 2 cycles per accepted MAC group plus 12 cycles per single-context job turnover.",
            "The illustrative estimate is neither a measurement nor a proven lower bound; replace its coefficients with actual runner endpoint measurements.",
            "The final cadence fit uses the measured no-stall G=2 jobs: 2 ST_STORAGE + 2 ST_MAC_SEND + 10 ST_MAC_WAIT = 14 cycles/job, hence 2*G+10.",
            "Only the down2 depthwise and pointwise G=2 runner were measured. G>2 layers use a conditional linear extrapolation, not a measured result or hard lower bound.",
            "Conditional per-layer boundaries reuse measured down2 values: 27 cycles for depthwise and 28 for pointwise/stem. Bypass heads can differ and remain unmeasured.",
            "SiLU-active is identified by graph int8 output; the six int16_q7_8 head outputs bypass activation.",
            "DDR, non-convolution operators, decode, NMS, preload, export, and physical timing are excluded."
        ],
        "measured_runner_fit": {
            "log": str(RUNNER_LOG),
            "log_sha256": hashlib.sha256(runner_raw).hexdigest(),
            "scope": "down2 4x4 tile, 256 DW jobs plus 128 PW jobs, all G=2",
            "job_state_cycles": {"ST_STORAGE": 2, "ST_MAC_SEND": 2,
                                 "ST_MAC_WAIT": 10, "total": 14},
            "jobs": 384,
            "mac_window_cycles": 5376,
            "dw_endpoint_cycles": 3611,
            "dw_job_cycles": 3584,
            "dw_boundary_cycles": 27,
            "pw_endpoint_cycles": 1820,
            "pw_job_cycles": 1792,
            "pw_boundary_cycles": 28,
            "full_core_cycles": 5431,
            "mutually_exclusive_identity": "5376 MAC-state cycles + 54 drain-state cycles + 1 start edge = 5431",
            "overlapping_busy_counters_not_additive": {
                "pre": 3712, "silu": 2560, "post": 3712, "writeback": 640
            },
        },
        "frame_limit": {"clock_hz": 100000000, "fps": 5, "cycles": 20000000},
        "conv_layers": len(layers),
        "activation_split": {
            "silu_active_layers": activation_counts[True],
            "silu_bypass_layers": activation_counts[False],
            "silu_active_output_values": sum(layer["output_values"] for layer in layers
                                             if layer["activated_silu"]),
            "silu_bypass_output_values": sum(layer["output_values"] for layer in layers
                                             if not layer["activated_silu"]),
        },
        "by_kind": by_kind,
        "illustrative_total_cycles": estimate,
        "illustrative_over_20m": estimate - 20000000,
        "fitted_job_cadence_cycles": fitted_jobs,
        "conditional_layer_boundary_cycles": fitted_boundaries,
        "conditional_extrapolated_total_cycles": fitted_total,
        "conditional_extrapolated_over_20m": fitted_total - 20000000,
        "optimization_examples": [
            {
                "name": "wrapper product-shift-tag elastic register",
                "single_variable": "insert one elastic register at the wrapper product/shift/tag boundary without changing arithmetic values or frozen arithmetic ports",
                "conditional_savings_cycles": 0,
                "recommendation": "recommended next isolated experiment for physical closure",
                "constraint": "Adds one latency cycle; the maximum obligation bound must be re-measured and proved (it may rise from 30 to 31), together with tags, backpressure and all reset ages. It is not implemented or proved here and is not a frame-cycle optimization."
            },
            {
                "name": "runner consecutive group issue",
                "single_variable": "overlap/prefetch ST_STORAGE so groups after the first issue on consecutive cycles",
                "conditional_savings_cycles": sum(
                    layer["mac_jobs"] * (layer["mac_input_groups_per_job"] - 1)
                    for layer in layers),
                "recommendation": "defer until physical closure",
                "constraint": "Changes runner scheduling/interface timing and requires separate approval and full re-verification."
            },
            {
                "name": "single-context terminal turnover",
                "single_variable": "remove one ST_MAC_WAIT-equivalent cycle per job",
                "conditional_savings_cycles_per_removed_cycle": sum(
                    layer["mac_jobs"] for layer in layers),
                "recommendation": "not selected; arithmetic-core scope",
                "constraint": "The frozen MAC is already input-II=1; this changes terminal/next-job behavior."
            },
            {
                "name": "three-channel depthwise packing",
                "single_variable": "use all three result lanes for adjacent DW channels",
                "recommendation": "not assumed and not free",
                "constraint": "Would require the shared 8-input path to cover 27 channel-specific activation terms across multiple groups, plus diagonal-weight, scheduling and storage adaptation; it is not free three-lane parallelism."
            }
        ],
        "layers": layers,
    }
    if len(layers) != 67 or activation_counts != Counter({True: 61, False: 6}):
        raise AssertionError("frozen graph count changed")
    OUTPUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": report["status"],
        "conv_layers": len(layers),
        "activation_split": report["activation_split"],
        "by_kind": by_kind,
        "illustrative_total_cycles": estimate,
        "conditional_extrapolated_total_cycles": fitted_total,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
