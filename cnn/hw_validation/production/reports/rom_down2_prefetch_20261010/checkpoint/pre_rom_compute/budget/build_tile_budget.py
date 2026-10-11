"""Build the frozen 67-convolution tile/task ledger; never estimate full-frame FPS."""

from __future__ import annotations

from hashlib import sha256
import json
from math import ceil
from pathlib import Path


HERE = Path(__file__).resolve().parent
PRODUCTION = HERE.parents[2]
REPORTS = PRODUCTION / "reports"
HW_VALIDATION = PRODUCTION.parent
GRAPH = PRODUCTION / "graph_artifacts" / "graph.json"
OLD_TASK_BUDGET = REPORTS / "mac_task_stream_20261009" / "layer_budget.json"
CURRENT_SCHEDULE = REPORTS / "scheduler_predecode_20261010" / "layer_budget.json"
DIRECT_REFERENCE = REPORTS / "control_operand_hold_20261009" / "layer_budget.json"
PLAN = HW_VALIDATION / "plans" / "global_closure_20261010" / "RoadYOLO_首批执行步骤与后续里程碑.md"
OUTPUT_JSON = HERE / "current_tile_budget.json"
OUTPUT_REPORT = HERE / "REPORT.md"
UNKNOWN = "UNKNOWN"
UNMEASURED = "UNMEASURED"
PREVIOUS_OUTPUT_SHA256 = {
    "current_tile_budget.json": "41d5709205091e32491f94f62bc7fc91d83144d69439e362efb79f839797ea70",
    "REPORT.md": "c36f9db85c3d686b51833ab6b735afa4f9a1e4fa772233caed2eedad36d9cb89",
}


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return path.relative_to(HW_VALIDATION.parent.parent).as_posix()


def tile_axis(length: int) -> list[int]:
    return [min(4, length - start) for start in range(0, length, 4)]


def dw_tasks(height: int, width: int, channels: int) -> int:
    return sum(valid_h * ceil(valid_w / 3) * channels
               for valid_h in tile_axis(height) for valid_w in tile_axis(width))


def task_models(kind: str, height: int, width: int, cout: int) -> tuple[int, int]:
    tile_count = ceil(height / 4) * ceil(width / 4)
    if kind == "dw":
        return dw_tasks(height, width, cout), tile_count * 4 * ceil(4 / 3) * cout
    output_groups = ceil(cout / 3)
    return height * width * output_groups, tile_count * 16 * output_groups


def kind_of(node: dict) -> str:
    kernel = node["kernel"][0]
    cin = node["input_shape_hwc"][2]
    if kernel == 3 and node["groups"] == cin:
        return "dw"
    return "pw" if kernel == 1 else "stem"


def node_digest(node: dict) -> str:
    raw = json.dumps(node, sort_keys=True, separators=(",", ":")).encode()
    return sha256(raw).hexdigest()


def build_report(result: dict) -> str:
    counts = result["asserted_counts"]
    d = result["down2_fixed_assertions"]
    lines = [
        "# 4x4 tile 任务预算修正报告",
        "",
        "本报告只修正冻结 graph 的任务/存储口径，不是整网周期仿真，也不形成 FPS 结论。",
        "",
        "## 结论",
        "",
        f"- 67 个卷积已逐层列账：Stem {counts['stem']}、DW {counts['dw']}、PW {counts['pw']}；原始预测 INT16 层 {counts['raw_prediction_int16']}。",
        "- DW 三空间点严格限制在同一 4x4 tile、同一有效输出行；stride2 的 3 组/stride1 的 2 组只是任务模型，不代表现 RTL 已支持。",
        "- `planned_issued_tasks` 全部为 `UNKNOWN`，指整层发射及未来适配策略未证；down2 固定满 tile 已实测 DW/PW 每 tile 各 128 任务。部分 tile 同时列逻辑有效行模型和满物理槽模型，填 0 不被解释为已实现跳行。",
        f"- down2 DW/PW 的 1 tile RTL 实测仅为 {d['dw_measured_tile_cycles']}/{d['pw_measured_tile_cycles']} 拍；完整层 {d['dw_projected_layer_cycles']}/{d['pw_projected_layer_cycles']} 拍仅是 tile 数乘法外推。其余 65 层为 `UNMEASURED`。",
        f"- down2 DW 完整 4x4 tile：{d['dw_valid_multiplications_per_tile']:,} 次有效乘法/{d['dw_physical_multiplier_slots_per_tile']:,} 个物理槽，平均利用率 {d['dw_average_slot_utilization_percent']}%。",
        "- graph `storage.raw_bytes` 按 tile padding 复核；逻辑有效字节独立按 H×W×C×元素字节计算。",
        "",
        "## 23 个 DW 旧/新任务差异",
        "",
        "旧口径为 `H×ceil(W/3)×C`，会让三点包跨过 4 列 tile 边界；新口径逐 tile、逐有效行计算。",
        "",
        "| layer | stride | old | new logical | full-slot model | delta |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in result["dw_old_new_task_differences"]:
        lines.append(
            f"| {row['layer']} | {row['stride']} | {row['old_cross_tile_tasks']:,} | "
            f"{row['new_tile_local_logical_tasks']:,} | {row['full_tile_slot_task_model']:,} | "
            f"{row['delta_new_minus_old']:+,} |"
        )
    lines += [
        "",
        "## 部分 tile 策略",
        "",
        "| layer | H×W×C | logical tasks | full-slot model | actual issued | logical/tile/allocated bytes |",
        "|---|---|---:|---:|---|---|",
    ]
    for row in result["partial_tile_layers"]:
        layout = row["layout"]
        tasks = row["tasks"]
        lines.append(
            f"| {row['layer']} | {row['shape']} | {tasks['logical_required_tasks']:,} | "
            f"{tasks['full_physical_tile_slot_task_model']:,} | UNKNOWN | "
            f"{layout['logical_valid_bytes']:,}/{layout['tile_storage_bytes']:,}/{layout['aligned_allocated_bytes']:,} |"
        )
    lines += [
        "",
        "`down4.pw.conv` 的固定例：18×32×96，逻辑任务 18,432，满槽模型 20,480；逻辑字节 55,296，tile 存储 61,440。实际发射策略仍 UNKNOWN。",
        "",
        "## 20M 周期参考仍缺的实际项",
        "",
    ]
    lines.extend(f"- {item['item']}: {item['status']} — {item['reason']}"
                 for item in result["budget_reference"]["unknown_full_frame_costs"])
    lines += [
        "",
        "因此不计算未知项为 0，不从 20,000,000 拍中扣除已知项，不声明 5 FPS、余量或达标比例。",
        "",
        "## 修订记录",
        "",
        f"- 上一版 JSON SHA256：`{PREVIOUS_OUTPUT_SHA256['current_tile_budget.json']}`。",
        f"- 上一版报告 SHA256：`{PREVIOUS_OUTPUT_SHA256['REPORT.md']}`。",
        "- 本版仅澄清：down2 动态 pre/post 与通道 TEST 参数已接入；UNKNOWN 是 schema2 ROM 真实取参、整图层参数装载/重叠及整层发射策略未测。",
        "",
        "## 输入与旧文件不变",
        "",
    ]
    for item in result["input_immutability"]:
        lines.append(f"- `{item['path']}`: `{item['sha256_before']}`（前后相同）")
    lines += [
        "",
        "生成检查：67/23/43/1/6 数量、down2 固定断言、down4 部分 tile 例、所有 raw_bytes tile padding、旧 DW 公式与旧表一致、输入哈希前后一致，全部通过。",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    inputs = [GRAPH, OLD_TASK_BUDGET, CURRENT_SCHEDULE, DIRECT_REFERENCE, PLAN, Path(__file__).resolve()]
    before = {path: digest(path) for path in inputs}
    graph = load(GRAPH)
    old_task_budget = load(OLD_TASK_BUDGET)
    current_schedule = load(CURRENT_SCHEDULE)
    direct_reference = load(DIRECT_REFERENCE)
    old_dw = {row["layer"]: row for row in old_task_budget["rows"] if row["kind"] == "dw"}
    current_rows = {row["layer"]: row for row in current_schedule["rows"]}
    direct_rows = {row["layer"]: row for row in direct_reference["rows"]}

    rows = []
    dw_differences = []
    for node in graph["nodes"]:
        if node["op"] != "conv":
            continue
        kind = kind_of(node)
        height, width, cout = node["output_shape_hwc"]
        cin = node["input_shape_hwc"][2]
        kernel = node["kernel"][0]
        stride = node["stride"][0]
        storage = node["storage"]
        bytes_per_element = storage["bytes_per_element"]
        tile_rows, tile_cols = ceil(height / 4), ceil(width / 4)
        tile_count = tile_rows * tile_cols
        logical_tasks, full_slot_tasks = task_models(kind, height, width, cout)
        union_slots = (21 if stride == 2 else 15) if kind == "dw" else cin * kernel * kernel
        input_groups = ceil(union_slots / 8)
        input_tail_lanes = union_slots % 8 or 8
        logical_elements = height * width * cout
        logical_bytes = logical_elements * bytes_per_element
        tile_bytes = tile_count * 16 * storage["channels_stored"] * bytes_per_element
        assert tile_bytes == storage["raw_bytes"], node["name"]
        assert logical_bytes <= tile_bytes <= storage["allocated_bytes"], node["name"]

        partial = height % 4 != 0 or width % 4 != 0
        if kind == "dw":
            output_lanes = {
                "meaning": "spatial_points_per_tile_local_pack",
                "full_pack": 3,
                "full_tile_row_pack_sequence": [3, 1],
                "last_tile_row_pack_sequence": [min(3, width % 4 or 4), max((width % 4 or 4) - 3, 0)],
            }
        else:
            output_lanes = {
                "meaning": "output_channels_per_task",
                "full_group": 3,
                "last_group": cout % 3 or 3,
            }

        measured = UNMEASURED
        measured_tasks = UNMEASURED
        projection = UNMEASURED
        if node["name"] in {"down2.dw.conv", "down2.pw.conv"}:
            measured = current_rows[node["name"]]["measured_tile_cycles"]
            measured_tasks = logical_tasks // tile_count
            assert measured_tasks == 128
            assert measured == direct_rows[node["name"]]["measured_tile_cycles"]
            projection = measured * tile_count
        row = {
            "graph_node": {
                "index": node["index"],
                "name": node["name"],
                "canonical_sha256": node_digest(node),
                "graph_sha256": before[GRAPH],
            },
            "structure": {
                "operator": "conv",
                "kind": kind,
                "input_hwc": node["input_shape_hwc"],
                "output_hwc": node["output_shape_hwc"],
                "cin": cin,
                "cout": cout,
                "kernel": node["kernel"],
                "stride": node["stride"],
                "padding": node["padding"],
                "groups": node["groups"],
                "output_type": node["dtype"],
            },
            "layout": {
                "layout": storage["layout"],
                "tile_rows": tile_rows,
                "tile_cols": tile_cols,
                "tile_count": tile_count,
                "last_tile_valid_height": height % 4 or 4,
                "last_tile_valid_width": width % 4 or 4,
                "bytes_per_element": bytes_per_element,
                "logical_valid_bytes": logical_bytes,
                "tile_storage_bytes": tile_bytes,
                "graph_storage_raw_bytes": storage["raw_bytes"],
                "aligned_allocated_bytes": storage["allocated_bytes"],
                "partial_tile_invalid_fill": storage["partial_tile_invalid_fill"],
            },
            "tasks": {
                "basis": "TILE_LOCAL_THREE_POINT_PACK_NO_CROSS_TILE" if kind == "dw" else "OUTPUT_PIXEL_BY_OUTPUT_CHANNEL_GROUP",
                "logical_required_tasks": logical_tasks,
                "full_physical_tile_slot_task_model": full_slot_tasks,
                "planned_issued_tasks": UNKNOWN,
                "input_groups_per_task": input_groups,
                "input_tail_valid_lanes": input_tail_lanes,
                "output_valid_lanes": output_lanes,
            },
            "boundary_policy": {
                "has_partial_tile": partial,
                "partial_tile_policy": "UNKNOWN_SKIP_VALID_ROWS_OR_EXECUTE_FULL_SLOTS" if partial else "NO_PARTIAL_TILE",
                "zero_fill_is_not_issue_policy_evidence": True,
            },
            "cycle_evidence": {
                "mathematical_lower_bound": {
                    "status": "MODEL_ONLY_NOT_MEASURED",
                    "input_group_accept_floor_cycles": logical_tasks * input_groups,
                    "serialized_output_element_floor_cycles": logical_elements,
                    "combined_floor_cycles": max(logical_tasks * input_groups, logical_elements),
                },
                "scheduler_model": {
                    "status": "COUNT_MODEL_ONLY_NOT_RTL_SUPPORT",
                    "dw_stride2_groups_3_stride1_groups_2_are_model_only": kind == "dw",
                },
                "rtl_measured_4x4_tile_issued_tasks": measured_tasks,
                "rtl_measured_4x4_tile_cycles": measured,
                "full_layer_projection_from_tile_measurement": projection,
                "projection_status": "EXTRAPOLATED_NOT_FULL_LAYER_MEASUREMENT" if projection != UNMEASURED else UNMEASURED,
                "full_layer_rtl_measured_cycles": UNMEASURED,
                "full_layer_ddr_measured_cycles": UNMEASURED,
            },
            "extra_costs": {
                "graph_weight_int8_bytes": node["weights"],
                "rom_transaction_bytes": UNKNOWN,
                "rom_wait_cycles": UNKNOWN,
                "ddr_read_transaction_bytes": UNKNOWN,
                "ddr_write_transaction_bytes": UNKNOWN,
                "ddr_wait_cycles": UNKNOWN,
                "parameter_load_cycles": UNKNOWN,
                "writeback_visibility_barrier_cycles": UNKNOWN,
                "non_convolution_and_layer_switch_cycles": UNKNOWN,
            },
        }
        rows.append(row)
        if kind == "dw":
            old_formula = height * ceil(width / 3) * cout
            assert old_dw[node["name"]]["tasks"] == old_formula
            dw_differences.append({
                "layer": node["name"],
                "stride": stride,
                "old_cross_tile_tasks": old_formula,
                "old_budget_tasks": old_dw[node["name"]]["tasks"],
                "new_tile_local_logical_tasks": logical_tasks,
                "full_tile_slot_task_model": full_slot_tasks,
                "delta_new_minus_old": logical_tasks - old_formula,
                "planned_issued_tasks": UNKNOWN,
            })

    counts = {
        "conv": len(rows),
        "dw": sum(row["structure"]["kind"] == "dw" for row in rows),
        "pw": sum(row["structure"]["kind"] == "pw" for row in rows),
        "stem": sum(row["structure"]["kind"] == "stem" for row in rows),
        "raw_prediction_int16": sum(row["structure"]["output_type"] == "int16_q7_8" for row in rows),
    }
    assert counts == {"conv": 67, "dw": 23, "pw": 43, "stem": 1, "raw_prediction_int16": 6}
    by_name = {row["graph_node"]["name"]: row for row in rows}
    down2_dw, down2_pw = by_name["down2.dw.conv"], by_name["down2.pw.conv"]
    assert down2_dw["layout"]["tile_count"] == 576
    assert down2_dw["tasks"]["logical_required_tasks"] == 73728
    assert down2_dw["tasks"]["input_groups_per_task"] == 3
    assert down2_dw["tasks"]["logical_required_tasks"] // 576 == 128
    assert down2_dw["tasks"]["logical_required_tasks"] * 3 == 221184
    assert down2_pw["tasks"]["logical_required_tasks"] == 73728
    assert down2_pw["tasks"]["input_groups_per_task"] == 2
    assert down2_pw["tasks"]["logical_required_tasks"] // 576 == 128
    assert down2_pw["tasks"]["logical_required_tasks"] * 2 == 147456
    assert down2_dw["cycle_evidence"]["rtl_measured_4x4_tile_cycles"] == 1095
    assert down2_pw["cycle_evidence"]["rtl_measured_4x4_tile_cycles"] == 592
    assert down2_dw["cycle_evidence"]["full_layer_projection_from_tile_measurement"] == 630720
    assert down2_pw["cycle_evidence"]["full_layer_projection_from_tile_measurement"] == 340992
    down4_pw = by_name["down4.pw.conv"]
    assert down4_pw["tasks"]["logical_required_tasks"] == 18432
    assert down4_pw["tasks"]["full_physical_tile_slot_task_model"] == 20480
    assert down4_pw["layout"]["logical_valid_bytes"] == 55296
    assert down4_pw["layout"]["tile_storage_bytes"] == 61440
    down4_dw = by_name["down4.dw.conv"]
    assert down4_dw["tasks"]["logical_required_tasks"] == 13824
    assert down4_dw["tasks"]["full_physical_tile_slot_task_model"] == 15360
    assert sum(row["cycle_evidence"]["rtl_measured_4x4_tile_cycles"] != UNMEASURED for row in rows) == 2
    assert sum(row["cycle_evidence"]["rtl_measured_4x4_tile_cycles"] == UNMEASURED for row in rows) == 65

    unknown_costs = [
        {"item": "actual_issued_tasks_and_partial_tile_policy", "status": UNKNOWN, "reason": "薄适配器尚未证明跳有效行或执行满槽"},
        {"item": "per_layer_scheduler_launch_retire_and_drain", "status": UNKNOWN, "reason": "67层调度器尚未实现和测量"},
        {"item": "rom_transaction_bytes_and_wait", "status": UNKNOWN, "reason": "schema2真实消费者与缓存复用尚未测量"},
        {"item": "ddr_read_write_beats_and_arbitration_wait", "status": UNKNOWN, "reason": "真实PAXI闭环未建立"},
        {"item": "parameter_load_and_overlap", "status": UNKNOWN, "reason": "down2动态pre/post与通道TEST参数已接入；schema2 ROM真实取参和整图层参数装载/重叠未测"},
        {"item": "writeback_visibility_barrier", "status": UNKNOWN, "reason": "写接受不等于写可见，实际完成事件未绑定"},
        {"item": "non_convolution_nodes", "status": UNKNOWN, "reason": "pool、residual、concat、nearest尚无完整周期"},
        {"item": "layer_transition_and_tensor_view_control", "status": UNKNOWN, "reason": "106节点全图sequencer尚未闭合"},
        {"item": "decode_topk_nms_and_result_table", "status": UNKNOWN, "reason": "纯FPGA后处理尚未实现和测量"},
        {"item": "capture_queue_cdc_display_and_real_backpressure", "status": UNKNOWN, "reason": "完整视频/DDR/显示路径尚未集成"},
    ]
    after = {path: digest(path) for path in inputs}
    assert before == after
    input_immutability = [{
        "path": rel(path),
        "bytes": path.stat().st_size,
        "sha256_before": before[path],
        "sha256_after": after[path],
        "unchanged": True,
    } for path in inputs]
    partial_rows = [{
        "layer": row["graph_node"]["name"],
        "shape": "x".join(map(str, row["structure"]["output_hwc"])),
        "layout": row["layout"],
        "tasks": row["tasks"],
        "partial_tile_policy": row["boundary_policy"]["partial_tile_policy"],
    } for row in rows if row["boundary_policy"]["has_partial_tile"]]
    known_counts = {}
    for kind in ("stem", "dw", "pw"):
        subset = [row for row in rows if row["structure"]["kind"] == kind]
        known_counts[kind] = {
            "logical_required_tasks": sum(row["tasks"]["logical_required_tasks"] for row in subset),
            "full_physical_tile_slot_task_model": sum(row["tasks"]["full_physical_tile_slot_task_model"] for row in subset),
            "logical_input_group_accepts": sum(row["tasks"]["logical_required_tasks"] * row["tasks"]["input_groups_per_task"] for row in subset),
            "logical_output_bytes": sum(row["layout"]["logical_valid_bytes"] for row in subset),
            "tile_storage_bytes": sum(row["layout"]["tile_storage_bytes"] for row in subset),
            "aligned_allocated_bytes": sum(row["layout"]["aligned_allocated_bytes"] for row in subset),
        }

    result = {
        "schema": "road_yolo_current_tile_budget_v1",
        "status": "COUNT_LEDGER_ONLY_NOT_FULL_NETWORK_CYCLE_MEASUREMENT",
        "scope": "Frozen graph; 4x4 tile-local tasks; no RTL, TD, training, deployment, or FPS claim.",
        "revision": {
            "reason": "Clarify measured down2 tile issue count and parameter-load unknown boundary.",
            "previous_output_sha256": PREVIOUS_OUTPUT_SHA256,
        },
        "inputs": {"graph_architecture_sha256": graph["architecture_sha256"], "graph_source_sha256": graph["source_sha256"]},
        "input_immutability": input_immutability,
        "asserted_counts": counts,
        "task_contract": {
            "tile_h_w": [4, 4],
            "dw_pack": "three adjacent spatial points, same channel, same output row, never across tile boundary",
            "dw_stride2_union_slots_and_input_groups": [21, 3],
            "dw_stride1_union_slots_and_input_groups": [15, 2],
            "dw_group_counts_status": "MODEL_ONLY_NOT_CURRENT_RTL_SUPPORT",
            "planned_issued_tasks_status": UNKNOWN,
        },
        "rows": rows,
        "dw_old_new_task_differences": dw_differences,
        "partial_tile_layers": partial_rows,
        "known_count_components_not_a_cycle_total": known_counts,
        "down2_fixed_assertions": {
            "tile_count": 576,
            "dw_tasks_per_tile": 128,
            "dw_fixed_full_tile_issued_tasks_measured": 128,
            "dw_input_groups_per_tile": 384,
            "dw_layer_tasks": 73728,
            "dw_layer_input_groups": 221184,
            "pw_tasks_per_tile": 128,
            "pw_fixed_full_tile_issued_tasks_measured": 128,
            "pw_input_groups_per_tile": 256,
            "pw_layer_tasks": 73728,
            "pw_layer_input_groups": 147456,
            "dw_measured_tile_cycles": 1095,
            "pw_measured_tile_cycles": 592,
            "dw_projected_layer_cycles": 630720,
            "pw_projected_layer_cycles": 340992,
            "projection_status": "EXTRAPOLATED_NOT_FULL_LAYER_MEASUREMENT",
            "dw_valid_multiplications_per_tile": 2304,
            "dw_physical_multiplier_slots_per_tile": 9216,
            "dw_average_slot_utilization_percent": 25.0,
        },
        "budget_reference": {
            "cycles_per_frame_reference_only": 20000000,
            "assessment": UNKNOWN,
            "fps_claim": "NOT_MADE",
            "remaining_cycles": UNKNOWN,
            "unknown_items_are_not_zero": True,
            "unknown_full_frame_costs": unknown_costs,
        },
        "self_checks": {
            "all_required_assertions_passed": True,
            "old_dw_rows_match_old_cross_tile_formula": True,
            "all_graph_raw_bytes_match_tile_padded_storage": True,
            "old_inputs_unchanged": True,
            "measured_rows": 2,
            "unmeasured_rows": 65,
        },
    }
    assert len(dw_differences) == 23
    assert OUTPUT_JSON.parent == HERE and OUTPUT_REPORT.parent == HERE
    OUTPUT_JSON.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    OUTPUT_REPORT.write_text(build_report(result), encoding="utf-8")
    assert all(digest(path) == before[path] for path in inputs)
    print(json.dumps({
        "rows": len(rows),
        "dw_differences": len(dw_differences),
        "partial_tile_layers": len(partial_rows),
        "measured_rows": 2,
        "unmeasured_rows": 65,
        "fps_claim": False,
        "output": str(OUTPUT_JSON),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
