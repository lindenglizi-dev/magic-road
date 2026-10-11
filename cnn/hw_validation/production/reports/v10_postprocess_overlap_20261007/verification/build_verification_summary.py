"""Build the final v10 functional verification receipt from fresh logs."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
V10 = ROOT.parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require_log(relative: str, marker: str) -> dict[str, object]:
    path = ROOT / relative
    text = path.read_text(encoding="utf-8", errors="replace")
    if marker not in text or "TB_ERROR" in text or "TB_FAIL" in text:
        raise AssertionError(f"final log failed: {path}")
    errors = re.findall(r"Errors:\s*(\d+)", text)
    warnings = re.findall(r"Warnings:\s*(\d+)", text)
    if errors and errors[-1] != "0":
        raise AssertionError(f"tool errors in {path}")
    return {
        "path": str(path),
        "sha256": sha256(path),
        "pass_marker": marker,
        "tool_errors": int(errors[-1]) if errors else 0,
        "tool_warnings": int(warnings[-1]) if warnings else 0,
        "missing_file_indications": sum(
            token in text for token in ("Failed to open", "readmem file", "ENOENT")
        ),
    }


def copy_audit() -> dict[str, object]:
    pairs = []
    for manifest_name in ("copied_inputs_manifest.json", "legacy_inputs_manifest.json"):
        manifest = json.loads((ROOT / manifest_name).read_text(encoding="utf-8"))
        for value in manifest.values():
            if not isinstance(value, list):
                continue
            for record in value:
                if record.get("transformation", "none") != "none":
                    continue
                source = Path(record["source"])
                copy = Path(record["copy"])
                if source.suffix.lower() not in {".hex", ".txt", ".dath"}:
                    continue
                source_hash = sha256(source)
                copy_hash = sha256(copy)
                pairs.append({
                    "source": str(source), "copy": str(copy),
                    "source_sha256": source_hash, "copy_sha256": copy_hash,
                    "match": source_hash == copy_hash,
                })
    mismatches = [pair for pair in pairs if not pair["match"]]
    if mismatches:
        raise AssertionError(f"copied input mismatch: {mismatches}")
    return {"exact_copy_pairs": len(pairs), "mismatches": 0, "pairs": pairs}


def main() -> None:
    final_logs = {
        "candidate_runner_four_cases": require_log(
            "regression_candidate/vsim_attempt4.log", "TB_PASS_DOWN2_TILE cases=4"),
        "candidate_standalone_stress": require_log(
            "regression_candidate/vsim_postprocess_attempt4.log",
            "TB_PASS_POSTPROCESS continuous=5 fixed_bubbles=3 random_groups=48"),
        "v9_mac_123": require_log(
            "regression_v9_mac/vsim.log", "TB_PASS_MAC_STREAM vectors=123"),
        "v8_original_four_layers": require_log(
            "regression_v8_layers/vsim.log", "TB_PASS_DOWN2_TILE cases=4"),
        "v9_serial_same_vectors": require_log(
            "regression_v9_serial_layers/vsim.log", "TB_PASS_DOWN2_TILE cases=4"),
        "v9_low_io_14": require_log(
            "regression_v9_shell/vsim_shell14.log", "TB_PASS_LOW_IO cases=14"),
        "v9_reset_6": require_log(
            "regression_v9_shell/vsim_reset6.log", "TB_PASS_RESET cases=6"),
        "round_7042": require_log(
            "regression_round_7042/simulate.log", "PASS round cases=7042"),
        "silu_65536": require_log(
            "regression_silu_65536/vsim_silu65536.log", "TB_PASS inputs=65536"),
        "python_reference": require_log(
            "reference_self_check_extended.log", "REFERENCE_PASS"),
    }
    if any(item["missing_file_indications"] for item in final_logs.values()):
        raise AssertionError("a final log contains a missing-file indication")

    budget = json.loads((ROOT / "budget" / "shape_budget.json").read_text(encoding="utf-8"))
    copy_result = copy_audit()
    cycle_trace = {
        "source_log": final_logs["candidate_runner_four_cases"],
        "no_stall_down2_full": {
            "jobs": 384,
            "first_four_jobs": [
                {"job": job, "ST_STORAGE": 2, "ST_MAC_SEND": 2,
                 "ST_MAC_WAIT": 10, "input_accepts": 2, "total": 14}
                for job in range(4)
            ],
            "mac_state_cycles": 5376,
            "scheduler_idle_cycles": 54,
            "start_edge": 1,
            "core_endpoint_cycles": 5431,
            "identity": "5376 + 54 + 1 = 5431",
            "dw": {"jobs": 256, "job_cycles": 3584, "boundary": 27,
                   "endpoint": 3611},
            "pw": {"jobs": 128, "job_cycles": 1792, "boundary": 28,
                   "endpoint": 1820},
            "overlapping_busy_observations": {
                "pre": 3712, "silu": 2560, "post": 3712, "writeback": 640,
                "rule": "observations overlap and must not be summed with MAC or each other",
            },
            "storage_wait_cycles": 0,
            "storage_wait_interpretation": (
                "zero means no commit/credit stall; two ST_STORAGE fetch cycles per job "
                "are already inside the 5376-cycle MAC-state window"
            ),
        },
        "random_commit_case": {
            "seed": "0x5eed", "ready_low_cycles": 1300,
            "output_valid_and_not_ready_cycles": 212,
            "core_endpoint_cycles": 5431,
            "all_stage_value_counts": 640,
        },
    }
    (ROOT / "runner_cycle_trace.json").write_text(
        json.dumps(cycle_trace, indent=2) + "\n", encoding="utf-8")

    summary = {
        "status": "FUNCTIONAL_PASS_CONDITIONAL_20M_BUDGET_NOT_MET",
        "candidate": {
            "rtl": {
                name: sha256(V10 / "rtl" / name)
                for name in ("road_postprocess_stream.v", "down2_overlap_tile_runner.v")
            },
            "testbenches": {
                name: sha256(ROOT / "regression_candidate" / name)
                for name in ("tb_road_postprocess_stream.v",
                             "tb_down2_overlap_tile_runner.v")
            },
            "latency_contract": {
                "scalar_pre_accept_to_output_valid": (
                    "23 cycles; valid is visible after the t+23 posedge NBA update"
                ),
                "scalar_pre_accept_to_first_transfer": "24th posedge when ready",
                "round_stages": [9, 9], "silu_stages": 6,
                "stage_busy_counters": "overlap; never additive",
            },
            "standalone_pressure": {
                "empty_fill": {"withdraw_edge": 2140, "last_accept_edge": 2167,
                               "response_edges": 28, "accepted_groups": 10,
                               "accepted_scalars": 30, "deny_until_release": 43,
                               "max_obligations": 30},
                "tail_valid": {"withdraw_edge": 4632, "last_accept_edge": 4650,
                               "response_edges": 19, "accepted_groups": 7,
                               "accepted_scalars": 21, "deny_until_release": 52,
                               "max_obligations": 29},
                "max_occupancy_each_window": {"result_fifo": 2, "pre": 9,
                                              "meta": 6, "post": 9},
                "held_output_stable": True,
            },
            "random_stress": {
                "gap_seed": "0x1d0f", "ready_seed": "0xace1",
                "groups": 48, "scalars": 96, "input_gap_cycles": 175,
                "output_not_ready_cycles": 67,
                "source_stable_before_handshake": True,
                "tag_indexed_no_loss_or_duplicate": True,
            },
            "reset_ages": {"tested": list(range(1, 25)), "pass_count": 24,
                           "reload_and_new_result_after_each": True,
                           "old_ghost_results": 0},
            "table_reload": (
                "a held write forwards on the same edge as global-empty && table_ready; "
                "all previously accepted old-table results drain first"
            ),
            "runner_cycle_trace": cycle_trace,
        },
        "fresh_regressions": final_logs,
        "same_vector_copy_audit": {
            "exact_copy_pairs": copy_result["exact_copy_pairs"], "mismatches": 0,
            "full_manifest": "final_hash_manifest.json",
        },
        "cycle_comparison_same_layer_vectors": {
            "v8_original": {"full": 27393, "dw": 13312, "pw": 14081},
            "v9_serial_mac": {"full": 23937, "dw": 11008, "pw": 12929},
            "v10_overlap_no_stall": {"full": 5431, "dw": 3611, "pw": 1820},
        },
        "budget": {
            "conv_layers": budget["conv_layers"],
            "silu_active_layers": budget["activation_split"]["silu_active_layers"],
            "silu_bypass_layers": budget["activation_split"]["silu_bypass_layers"],
            "silu_active_values": budget["activation_split"]["silu_active_output_values"],
            "silu_bypass_values": budget["activation_split"]["silu_bypass_output_values"],
            "fitted_job_cadence_cycles": budget["fitted_job_cadence_cycles"],
            "conditional_layer_boundaries": budget["conditional_layer_boundary_cycles"],
            "conditional_total_cycles": budget["conditional_extrapolated_total_cycles"],
            "over_20m": budget["conditional_extrapolated_over_20m"],
            "scope": "only down2 G=2 DW/PW measured; other layers extrapolated; DDR/non-conv/decode/NMS/preload/export excluded",
        },
        "known_warnings": (
            "ModelSim vendor PH1P_LOGIC_ERAM emits two pre-existing INIT_FILE "
            "part-select warnings; final logs have no readmem/fopen failure"
        ),
        "superseded_preserved_evidence": [
            {"log": "regression_candidate/vsim_attempt1.log",
             "reason": "real TB observer sampling bug caused post count 605/640"},
            {"log": "regression_candidate/vsim_postprocess_attempt1.log",
             "reason": "TB sampled NBA-visible latency at the wrong phase and required an extra illegal reload wait"},
            {"log": "regression_candidate/vsim_postprocess_attempt2.log",
             "reason": "printed PASS but reset-age loop reused a task-global index; not valid reset coverage"},
            {"log": "regression_candidate/vsim_postprocess_attempt3.log",
             "reason": "real reset coverage passed, but fixed bubbles were not random"},
            {"log": "reference_self_check.log",
             "reason": "pre-fix Python reference mishandled SiLU address 1024"},
        ],
    }
    (ROOT / "verification_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    report = f"""# v10 后处理重叠流水功能验证报告

## 结论

候选 RTL 的功能回归通过；20M cycle/frame 条件预算未满足。最终可信日志是 runner `vsim_attempt4.log` 和 standalone `vsim_postprocess_attempt4.log`。旧失败与覆盖不足日志均保留，不计入通过证据。

## 候选功能覆盖

- standalone：连续 5 组、固定气泡 3 组、固定种子随机 48 组/96 scalar、长固定反压、满信用、表重载、末组故障、通道系数切换、24 个真实 pipeline age 复位全部通过。
- 随机流：gap seed `0x1d0f`，ready seed `0xace1`，实际输入空拍 175、输出 not-ready 67；源在握手前稳定，tag-indexed scoreboard 无丢失、重复或逐值错误。
- 反压空流水窗口：ready 撤销 edge 2140，最后新增组接受 edge 2167，响应 28 edges；新增 10 组/30 scalar，随后连续拒绝 43 拍直到 release。
- 已有 tail-valid 窗口：edge 4632 到最后新增组 edge 4650，响应 19 edges；新增 7 组/21 scalar，连续拒绝 52 拍。
- 两窗口最大占用均为 result FIFO 2、pre 9、meta 6、post 9；最大 scalar obligations 分别 30/29；held output 保持稳定。
- 标量时序：pre accept 在 t，`o_output_valid` 在 t+23 posedge 的 NBA 更新后可见；ready 时首次合法 transfer 是 t+24 edge。两段 round 各 9 stage，SiLU 6 stage，忙周期相互重叠不能相加。
- 原 SiLU 65536 测试的 `latency=5` 是其 after-NBA 采样口径，对应 6 个注册推进 edge，与本设计 6-stage 定义不冲突。
- 表重载请求可以在 `global empty && table_ready` 成立的同一 edge forward，无需额外多等一拍；已接受的旧表结果先完全排空，无混表。

## 同向量 runner 结果

| 版本 | full | DW | PW |
|---|---:|---:|---:|
| v8 原串行 | 27393 | 13312 | 14081 |
| v9 MAC + 原串行 runner | 23937 | 11008 | 12929 |
| v10 overlap，无停顿 | 5431 | 3611 | 1820 |

v10 的 384 个 G=2 job 在 MAC 状态窗口内是 5376 cycles。前四个 job 逐拍都为 `2 ST_STORAGE + 2 ST_MAC_SEND + 10 ST_MAC_WAIT = 14`，每个接受两组。互斥端点恒等式是 `5376 MAC + 54 drain + 1 start = 5431`。`storage_wait=0` 只表示没有 commit/credit 等待；每 job 的两个 ST_STORAGE 已包含在 5376 中。pre=3712、SiLU=2560、post=3712、writeback=640 是并行忙观察，绝不能与 MAC 相加。

case 2 使用 seed `0x5eed` 的随机 commit-ready：ready-low 1300 cycles，其中 212 cycles 与有效输出相撞；所有 640 个阶段值和最终值仍通过。无停顿计时只取 case 0/1，不与随机 case 混合。

## 原回归复跑

- v9 MAC：123 vectors、17 results、9 faults、II1 97、9 bubbles、9 resets，PASS，0 errors/0 warnings。
- v9 低 IO：原 14 项 PASS；reset 6 项 PASS。
- round：7042 cases、14084 intermediate、1278 stalls、5 faults、checksum `00014ec4`，PASS。
- SiLU：65536 inputs、latency 5、II1、3072 legal writes、0 stale output errors，PASS。
- v8 四层与 v9-serial 同向量四层均 PASS。所有复制输入逐文件 SHA-256 一致；ModelSim 仅有两条既有 PH1P INIT_FILE part-select warning，无 readmem/fopen 缺失。

## 67 层条件预算

冻结图共 67 个 conv：61 个 SiLU-active、6 个 bypass；激活值 6,833,664，旁路值 84,672。以实测 G=2 job 拟合 `2G+10` 后，job cadence 外推为 {budget['fitted_job_cadence_cycles']:,} cycles；按 DW 27、PW/stem 28 的实测边界条件外推增加 {budget['conditional_layer_boundary_cycles']:,}，合计 {budget['conditional_extrapolated_total_cycles']:,}，超过 20M 预算 {budget['conditional_extrapolated_over_20m']:,}。

这不是整帧实测或硬下界：只有 down2 DW/PW、G=2 实测；G>2、6 个 activation bypass 层的边界均是条件外推，且不含 DDR、非卷积、decode、NMS、preload、export。

下一项推荐的单变量实验是 wrapper product/shift/tag 边界增加一级弹性寄存，以先处理物理实现的 setup 风险；它不降低上述 frame-cycle 外推，会增加 1 拍 latency，最大 scalar obligation 必须重新测定并证明（可能由 30 升到 31），同时重证 tag、反压和全部复位年龄。本轮没有实现或证明该方案。runner 连续 group issue 的条件收益约 {budget['optimization_examples'][1]['conditional_savings_cycles']:,} cycles/frame，但会改变调度/接口时序，暂后置。MAC 末组单 context 周转涉及算术核；三通道 DW 打包则需让共享 8 输入跨多组覆盖 27 个通道专属激活项，并适配对角权重、调度和存储，不能当免费三 lane 并行，也不在本轮改动内。

## 保留的非通过证据

- runner attempt1：TB 负沿观察与 ready 更新竞争，post 仅计 605/640；修复仅在 TB。
- standalone attempt1：NBA 可见时刻和合法同拍 table forward 的断言口径错误。
- standalone attempt2：共享全局 index 使 24-age 循环覆盖失真，已降级；attempt3 修复真实复位，但尚无随机气泡；attempt4 才是最终证据。
- Python reference 初版错误钳位 SiLU address 1024；最终版直接读取冻结表并对该点返回 2047。
"""
    (ROOT / "verification_report.md").write_text(report, encoding="utf-8")

    selected = [
        V10 / "rtl" / "road_postprocess_stream.v",
        V10 / "rtl" / "down2_overlap_tile_runner.v",
        ROOT / "regression_candidate" / "tb_road_postprocess_stream.v",
        ROOT / "regression_candidate" / "tb_down2_overlap_tile_runner.v",
        ROOT / "reference.py", ROOT / "deep_review.json",
        ROOT / "verification_summary.json", ROOT / "verification_report.md",
        ROOT / "runner_cycle_trace.json", ROOT / "budget" / "shape_budget.json",
    ]
    manifest = {
        "status": "FINAL_FILES_HASHED_AND_COPIED_INPUTS_MATCH",
        "files": [{"path": str(path), "bytes": path.stat().st_size,
                   "sha256": sha256(path)} for path in selected],
        "copy_audit": copy_result,
    }
    (ROOT / "final_hash_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": summary["status"],
        "final_logs": len(final_logs),
        "copy_pairs": copy_result["exact_copy_pairs"],
        "copy_mismatches": 0,
        "conditional_cycles": budget["conditional_extrapolated_total_cycles"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
