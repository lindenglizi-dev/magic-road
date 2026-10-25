"""CPU-only SRIF1 / FINAL97 / coherent-time reference.

This is a digital contract model.  It deliberately does not claim physical CDC,
RAM inference, timing closure, board operation, or oscillator accuracy.
"""
from __future__ import annotations

import hashlib
import json
import random
import sys
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
CANDIDATE = HERE.parent
REPO = HERE.parents[4]
sys.path.insert(0, str(CANDIDATE))
from reference_table import Tables  # noqa: E402  (frozen predecessor, read-only)


MODEL_ID = 0xB35D4A66
MODEL_PAYLOAD_SHA256 = "b35d4a66a69e441dc29bc60c7e3f507661f48da5f33b810d7340f6ed17a65145"
SOURCE_HZ = 100_000_000
DEST_HZ = 75_000_000
SOURCE_TICK_CYCLES = 100_000
WATCHDOG_CYCLES = 150_000
DEFAULT_AGE_LIMIT_MS = 500
BOUNDARY_AGE_LIMIT_MS = 2000
AGE_MARGIN_MS = 4

META_FIELDS = (
    ("epoch", 0, 32),
    ("task_id", 32, 32),
    ("source_frame_id", 64, 32),
    ("model_id", 96, 32),
    ("box_count", 128, 7),
    ("result_status", 135, 2),
    ("capture_timestamp_ms", 137, 64),
    ("completion_timestamp_ms", 201, 64),
)

FINAL97_FIELDS = (
    ("class_id", 0, 1),
    ("score", 1, 16),
    ("source_x0", 17, 20),
    ("source_y0", 37, 20),
    ("source_x1", 57, 20),
    ("source_y1", 77, 20),
)


def _pack(fields, values, total_bits):
    word = 0
    for name, lsb, width in fields:
        value = int(values[name])
        if not 0 <= value < (1 << width):
            raise ValueError(f"{name}={value} does not fit {width} bits")
        word |= value << lsb
    assert 0 <= word < (1 << total_bits)
    return word


def _unpack(fields, word, total_bits):
    word = int(word)
    if not 0 <= word < (1 << total_bits):
        raise ValueError(f"word does not fit {total_bits} bits")
    return {name: (word >> lsb) & ((1 << width) - 1) for name, lsb, width in fields}


def pack_metadata(metadata):
    """Pack one SRIF1 task metadata record; task_id is not a frame token."""
    if not 0 <= int(metadata["box_count"]) <= 64:
        raise ValueError("box_count must be in [0, 64]")
    return _pack(META_FIELDS, metadata, 265)


def unpack_metadata(word):
    return _unpack(META_FIELDS, word, 265)


def pack_final97(entry):
    return _pack(FINAL97_FIELDS, entry, 97)


def unpack_final97(word):
    return _unpack(FINAL97_FIELDS, word, 97)


def pack_time_snapshot(epoch, now_ms):
    if not 0 <= int(epoch) < (1 << 32) or not 0 <= int(now_ms) < (1 << 64):
        raise ValueError("time snapshot field out of range")
    return int(epoch) | (int(now_ms) << 32)


def unpack_time_snapshot(word):
    if not 0 <= int(word) < (1 << 96):
        raise ValueError("time snapshot does not fit 96 bits")
    return {"epoch": int(word) & 0xFFFFFFFF, "now_ms": int(word) >> 32}


def evaluate_metadata(metadata, entry_count, now_ms, time_epoch, time_valid,
                      expected_model_id=MODEL_ID, age_limit_ms=DEFAULT_AGE_LIMIT_MS):
    """Return the exact draw decision and conservative age upper bound."""
    m = dict(metadata)
    decision = {"draw": False, "reason": None, "age_upper_ms": None}
    if not time_valid:
        decision["reason"] = "time_invalid"
    elif m["epoch"] != time_epoch:
        decision["reason"] = "epoch_mismatch"
    elif m["model_id"] != expected_model_id:
        decision["reason"] = "model_mismatch"
    elif not 0 <= m["box_count"] <= 64:
        decision["reason"] = "bad_count"
    elif m["box_count"] != entry_count:
        decision["reason"] = "count_mismatch"
    elif m["result_status"] != 0:
        decision["reason"] = "status_not_valid"
    elif m["capture_timestamp_ms"] > now_ms:
        decision["reason"] = "future_capture"
    elif m["completion_timestamp_ms"] > now_ms:
        decision["reason"] = "future_completion"
    elif m["capture_timestamp_ms"] > m["completion_timestamp_ms"]:
        decision["reason"] = "timestamp_order"
    else:
        decision["age_upper_ms"] = now_ms - m["capture_timestamp_ms"] + AGE_MARGIN_MS
        if decision["age_upper_ms"] <= age_limit_ms:
            decision.update(draw=True, reason="valid")
        else:
            decision["reason"] = "too_old"
    return decision


class SrifTables(Tables):
    """SRIF1 checks layered on the frozen three-table event model."""

    def publish_srif(self, metadata, entries):
        metadata = dict(metadata)
        entries = tuple(entries)
        pack_metadata(metadata)
        if metadata["box_count"] != len(entries):
            raise ValueError("sealed box_count must equal accepted entry count")
        if metadata["result_status"] != 0 and entries:
            raise ValueError("cancel/fault/reserved task must seal with zero boxes")
        self.publish(metadata, entries)

    def visible_srif(self, now_ms, time_epoch, time_valid,
                     expected_model_id=MODEL_ID, age_limit_ms=DEFAULT_AGE_LIMIT_MS):
        if self.active is None:
            return (), {"draw": False, "reason": "no_active", "age_upper_ms": None}
        metadata, entries = self.active
        decision = evaluate_metadata(metadata, len(entries), now_ms, time_epoch, time_valid,
                                     expected_model_id, age_limit_ms)
        return (entries if decision["draw"] else ()), decision


def source_now_ms(elapsed_source_cycles):
    """The tick cycle freezes the incremented value: cycle 100000 -> now_ms 1."""
    if elapsed_source_cycles < 0:
        raise ValueError("negative cycle count")
    return elapsed_source_cycles // SOURCE_TICK_CYCLES


def watchdog_valid(elapsed_destination_cycles):
    """The target withdraws valid when the pre-increment count is >=150000."""
    return elapsed_destination_cycles <= WATCHDOG_CYCLES


def cdc_numeric_bounds():
    """Conditional active-clock digital bounds, in exact nanosecond fractions."""
    ts = Fraction(1_000_000_000, SOURCE_HZ)
    td = Fraction(1_000_000_000, DEST_HZ)
    req_to_capture = 4 * td       # exclusive: 2-flop req sync + stable wait/capture
    capture_to_ack = 3 * ts       # exclusive: ack return through source synchronizers
    watchdog_withdraw = (WATCHDOG_CYCLES + 1) * td
    freeze_to_withdraw = req_to_capture + watchdog_withdraw
    return {
        "source_period_ns": ts,
        "destination_period_ns": td,
        "req_to_capture_upper_exclusive_ns": req_to_capture,
        "capture_to_ack_upper_exclusive_ns": capture_to_ack,
        "round_trip_upper_exclusive_ns": req_to_capture + capture_to_ack,
        "watchdog_withdraw_max_ns": watchdog_withdraw,
        "freeze_to_watchdog_withdraw_upper_exclusive_ns": freeze_to_withdraw,
    }


def _fraction_json(value):
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "decimal": float(value),
    }


def make_entry(index):
    return {
        "class_id": index & 1,
        "score": (0x1000 + 977 * index) & 0xFFFF,
        "source_x0": (17 * index + 1) & 0xFFFFF,
        "source_y0": (29 * index + 2) & 0xFFFFF,
        "source_x1": (17 * index + 0x101) & 0xFFFFF,
        "source_y1": (29 * index + 0x202) & 0xFFFFF,
    }


def base_metadata(count, task_id=0x13579BDF):
    return {
        "epoch": 0x10203040,
        "task_id": task_id,
        "source_frame_id": 0x2468ACE0,
        "model_id": MODEL_ID,
        "box_count": count,
        "result_status": 0,
        "capture_timestamp_ms": 1000,
        "completion_timestamp_ms": 1003,
    }


def _table_case(count):
    tables = SrifTables()
    entries = tuple(pack_final97(make_entry(i)) for i in range(count))
    metadata = base_metadata(count, 0x90000000 + count)
    assert metadata["task_id"] != metadata["source_frame_id"]
    tables.publish_srif(metadata, entries)
    frozen = tables.source
    for _ in range(max(count - 1, 0)):
        tables.destination_tick(True, False)
        assert tables.source is not None and tables.pending is None
    for _ in range(7):
        tables.destination_tick(False, False)
        assert tables.source == frozen
    tables.destination_tick(True, True)  # last copy and SOF: no same-cycle bypass
    assert tables.acks == 1 and tables.active is None and tables.pending[1] == entries
    tables.destination_tick(False, True)
    visible, decision = tables.visible_srif(1496, metadata["epoch"], True)
    assert visible == entries and decision == {"draw": True, "reason": "valid", "age_upper_ms": 500}
    return {
        "count": count,
        "metadata_hex_265": f"{pack_metadata(metadata):067x}",
        "metadata": metadata,
        "entry_hex_97": [f"{entry:025x}" for entry in entries],
        "stall_cycles_before_last": 7,
        "ack_count": tables.acks,
        "same_cycle_last_copy_sof_bypass": False,
        "draw_at_now_1496": decision,
    }


def _pending_full_case():
    tables = SrifTables()
    first = (pack_final97(make_entry(1)),)
    second = (pack_final97(make_entry(2)),)
    tables.publish_srif(base_metadata(1, 1), first)
    tables.destination_tick(True, False)
    assert tables.pending is not None
    tables.publish_srif(base_metadata(1, 2), second)
    held = tables.source
    for _ in range(11):
        tables.destination_tick(True, False)
        assert tables.source == held and tables.pending[1] == first
    tables.destination_tick(True, True)
    assert tables.active[1] == first and tables.source == held and tables.pending is None
    tables.destination_tick(True, False)
    assert tables.pending[1] == second and tables.acks == 2
    return {"held_cycles": 11, "first_active_before_second_pending": True, "ack_count": 2}


def _filter_cases():
    cases = []

    def add(name, expected_draw, mutation=None, now=1496, epoch=0x10203040,
            time_valid=True, entry_count=1, limit=DEFAULT_AGE_LIMIT_MS, reason=None):
        metadata = base_metadata(1)
        if mutation:
            metadata.update(mutation)
        decision = evaluate_metadata(metadata, entry_count, now, epoch, time_valid, MODEL_ID, limit)
        assert decision["draw"] is expected_draw
        if reason is not None:
            assert decision["reason"] == reason
        cases.append({
            "name": name,
            "now_ms": now,
            "time_epoch": epoch,
            "time_valid": time_valid,
            "age_limit_ms": limit,
            "entry_count": entry_count,
            "metadata": metadata,
            "expected": decision,
        })

    add("default_500_accept_raw_496", True)
    add("default_500_reject_raw_497", False, now=1497, reason="too_old")
    add("independent_2000_accept_raw_1996", True, now=2996, limit=2000)
    add("independent_2000_reject_raw_1997", False, now=2997, limit=2000, reason="too_old")
    add("time_invalid", False, time_valid=False, reason="time_invalid")
    add("epoch_mismatch", False, epoch=0x10203041, reason="epoch_mismatch")
    add("model_mismatch", False, {"model_id": MODEL_ID ^ 1}, reason="model_mismatch")
    for status in (1, 2, 3):
        add(f"status_{status}", False, {"result_status": status}, reason="status_not_valid")
    add("count_mismatch", False, entry_count=0, reason="count_mismatch")
    add("future_capture", False,
        {"capture_timestamp_ms": 1497, "completion_timestamp_ms": 1498}, reason="future_capture")
    add("future_completion", False,
        {"capture_timestamp_ms": 1495, "completion_timestamp_ms": 1497}, reason="future_completion")
    add("capture_after_completion", False,
        {"capture_timestamp_ms": 1200, "completion_timestamp_ms": 1199}, reason="timestamp_order")
    return cases


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source_evidence():
    paths = [
        CANDIDATE / "requirements.txt",
        CANDIDATE / "interfaces.json",
        CANDIDATE / "codegen_plan.json",
        CANDIDATE / "reference_table.py",
        REPO / "cnn/hw_validation/plans/resource_budget_20261015/连续视频1FPS目标与第四批任务_20261015.txt",
        REPO / "cnn/hw_validation/plans/resource_budget_20261015/后处理共享RAM与接口约定_20261015.txt",
        REPO / "user_source/ip_source/PLL/PLL.v",
        REPO / "user_source/ip_source/PLL/.params_PLL.txt",
        REPO / "user_source/ip_source/PLL/Design.xml",
        REPO / "cnn/template/design_top_wrapper.v",
        REPO / "cnn/hw_validation/production/csp2_complete_20261015/status.json",
    ]
    for path in paths:
        assert path.is_file(), path
    return {path.relative_to(REPO).as_posix(): sha256(path) for path in paths}


def build_outputs():
    rng = random.Random(20261015)
    sample_meta = base_metadata(33)
    sample_meta["task_id"] = rng.getrandbits(32)
    sample_meta["source_frame_id"] = rng.getrandbits(32)
    assert sample_meta["task_id"] != sample_meta["source_frame_id"]
    packed_meta = pack_metadata(sample_meta)
    assert unpack_metadata(packed_meta) == sample_meta

    for i in (0, 1, 31, 63):
        entry = make_entry(i)
        assert unpack_final97(pack_final97(entry)) == entry
    max_entry = {name: (1 << width) - 1 for name, _, width in FINAL97_FIELDS}
    assert unpack_final97(pack_final97(max_entry)) == max_entry
    assert unpack_time_snapshot(pack_time_snapshot(0x89ABCDEF, 0x0123456789ABCDEF)) == {
        "epoch": 0x89ABCDEF, "now_ms": 0x0123456789ABCDEF}

    table_cases = [_table_case(count) for count in (0, 1, 32, 33, 64)]
    pending_full = _pending_full_case()
    filters = _filter_cases()

    mismatch = SrifTables()
    try:
        mismatch.publish_srif(base_metadata(2), (pack_final97(make_entry(0)),))
        raise AssertionError("count mismatch was accepted")
    except ValueError as exc:
        assert "box_count" in str(exc)

    diagnostic = SrifTables()
    diag_meta = base_metadata(0)
    diag_meta["result_status"] = 2
    diagnostic.publish_srif(diag_meta, ())
    diagnostic.destination_tick(True, False)
    diagnostic.destination_tick(False, True)
    assert diagnostic.visible_srif(1004, diag_meta["epoch"], True)[1]["reason"] == "status_not_valid"

    assert [source_now_ms(x) for x in (0, 99_999, 100_000, 199_999, 200_000)] == [0, 0, 1, 1, 2]
    assert watchdog_valid(150_000) and not watchdog_valid(150_001)
    bounds = cdc_numeric_bounds()
    assert bounds["req_to_capture_upper_exclusive_ns"] == Fraction(160, 3)
    assert bounds["round_trip_upper_exclusive_ns"] == Fraction(250, 3)
    assert bounds["round_trip_upper_exclusive_ns"] < 1_000_000
    assert bounds["watchdog_withdraw_max_ns"] == Fraction(6_000_040, 3)
    assert bounds["freeze_to_watchdog_withdraw_upper_exclusive_ns"] == Fraction(6_000_200, 3)
    assert bounds["freeze_to_watchdog_withdraw_upper_exclusive_ns"] < 3_000_000

    sources = _source_evidence()
    vectors = {
        "schema": "SRIF1_FINAL97_TIME96_CPU_V1",
        "seed": 20261015,
        "model_id_hex": f"0x{MODEL_ID:08X}",
        "metadata_roundtrip": {
            "metadata": sample_meta,
            "packed_hex_265": f"{packed_meta:067x}",
            "hex_digits": 67,
        },
        "final97_layout": [
            {"name": name, "lsb": lsb, "width": width} for name, lsb, width in FINAL97_FIELDS],
        "table_cases": table_cases,
        "pending_full_case": pending_full,
        "filter_cases": filters,
        "seal_count_mismatch": {"accepted": False, "exception": "ValueError"},
        "diagnostic_zero_count": {"status": 2, "accepted_for_transfer": True, "draw": False},
        "source_tick_examples": [
            {"elapsed_source_cycles": x, "now_ms": source_now_ms(x)}
            for x in (0, 99_999, 100_000, 199_999, 200_000)],
        "watchdog_boundary": [
            {"elapsed_destination_cycles": x, "time_valid": watchdog_valid(x)}
            for x in (149_999, 150_000, 150_001)],
        "cdc_bounds_ns": {name: _fraction_json(value) for name, value in bounds.items()},
    }

    contract = {
        "status": "PASS",
        "scope": "CPU digital reference only; TEST_ONLY",
        "format": {
            "payload": "FINAL97/PIF1",
            "metadata": "SRIF1 265-bit task metadata",
            "time_snapshot": "96-bit {now_ms[63:0],epoch[31:0]}",
            "metadata_fields": [
                {"name": name, "lsb": lsb, "width": width} for name, lsb, width in META_FIELDS],
            "task_id_semantics": "task token; independent from source_frame_id and not a frame token",
        },
        "model_binding": {
            "model_id_hex": f"0x{MODEL_ID:08X}",
            "model_id_decimal": MODEL_ID,
            "full_payload_sha256": MODEL_PAYLOAD_SHA256,
        },
        "tables": {
            "count": 3,
            "entries_per_table": 64,
            "entry_bits": 97,
            "metadata_bits_per_table": 265,
            "logical_payload_bits": 97 * 64 * 3,
            "logical_metadata_bits": 265 * 3,
            "logical_total_bits": (97 * 64 + 265) * 3,
            "pending_full_blocks_copy": True,
            "source_held_until_final_copy_ack": True,
            "last_copy_plus_sof_has_no_bypass": True,
            "count_zero_still_transfers_metadata_and_acks": True,
        },
        "filter": {
            "required": ["time_valid", "epoch_match", "model_match", "status_zero",
                         "count_matches_entries", "capture<=completion<=now"],
            "age_upper_formula_ms": "now_ms - capture_timestamp_ms + 4",
            "accept_formula": "age_upper_ms <= age_limit_ms",
            "default_age_limit_ms": DEFAULT_AGE_LIMIT_MS,
            "independent_boundary_age_limit_ms": BOUNDARY_AGE_LIMIT_MS,
        },
        "time_cdc": {
            "source_hz": SOURCE_HZ,
            "source_tick_cycles": SOURCE_TICK_CYCLES,
            "tick_semantics": "freeze incremented now_ms on each 100000th source cycle",
            "destination_hz": DEST_HZ,
            "destination_clock_evidence": "template PLL clk4_out configuration is 75 MHz",
            "request_path": "2 destination synchronizer stages then one stable wait/capture",
            "ack_path": "ack only after capture; source observes through synchronizers",
            "watchdog_cycles": WATCHDOG_CYCLES,
            "watchdog_semantics": "valid through elapsed=150000; invalid at elapsed=150001",
            "bounds_ns": {name: _fraction_json(value) for name, value in bounds.items()},
            "steady_publish_interval_ms": 1,
            "snapshot_lag_contract_ms": 3,
            "timestamp_quantization_margin_ms": 1,
            "age_margin_ms": AGE_MARGIN_MS,
            "condition": "both clocks active and digital sampling assumptions hold",
        },
        "reset": {
            "common_async_assert": True,
            "two_cycle_synchronous_release_each_domain": True,
            "unilateral_hot_reset_supported": False,
            "ram_clear_required": False,
            "valid_and_count_isolate_uncleared_ram": True,
        },
        "not_validated": [
            "metastability MTBF or physical bundled-data CDC",
            "active-clock availability or oscillator tolerance",
            "RAM primitive/inference mapping",
            "synthesis, place-and-route, timing closure, board, bitstream, TD",
        ],
        "source_sha256": sources,
        "vectors_file": "vectors.json",
        "self_check": "python reference_srif.py",
    }

    report = f"""detection_table_cdc_20261015 CPU参考报告
状态：PASS（仅数字CPU契约，TEST_ONLY）

1. 格式与三表
- SRIF1元数据265bit，task_id是任务号，不是frame token；source_frame_id独立。
- FINAL97保持PIF1：[0]class、[16:1]score、其余四个20bit Q12.8坐标。
- source/pending/active三表逻辑位数：18624 + 795 = 19419bit。
- count=0/1/32/33/64、随机停顿、pending满、最后copy与SOF同拍不旁路均由assert覆盖。
- seal的box_count必须等于已接收entry数；非零status只允许零框并禁止绘制。

2. 绘制过滤与年龄
- 必须time_valid、epoch/model匹配、status=0、count一致、capture<=completion<=now。
- age_upper_ms = now_ms - capture_timestamp_ms + 4；默认500ms，独立2000ms边界。
- 500ms：raw age 496接收、497拒绝；2000ms：1996接收、1997拒绝。
- model_id=0x{MODEL_ID:08X}，完整payload SHA256={MODEL_PAYLOAD_SHA256}。

3. 时间与CDC数字上界（条件：两时钟持续活动）
- source=100MHz，每100000拍+1ms，并在tick拍冻结递增后的now_ms。
- destination使用模板PLL clk4_out=75MHz的配置证据；非实测频率。
- req经两级同步并稳定等待后capture：<4*Td={float(bounds['req_to_capture_upper_exclusive_ns']):.9f}ns。
- ack返回source：<3*Ts={float(bounds['capture_to_ack_upper_exclusive_ns']):.9f}ns；数字往返<{float(bounds['round_trip_upper_exclusive_ns']):.9f}ns，远小于1ms发布间隔。
- watchdog在150000拍边界仍valid，150001拍撤销；最长{float(bounds['watchdog_withdraw_max_ns']) / 1_000_000:.9f}ms。
- 冻结到撤销总上界<{float(bounds['freeze_to_watchdog_withdraw_upper_exclusive_ns']) / 1_000_000:.9f}ms <3ms；不重复叠加source发布1ms。
- capture timestamp另计<1ms量化，故约定保守age margin仍为+4ms。

4. 明确未验证
- 未验证实际亚稳态延迟、物理bundled-data CDC、时钟存活/晶振误差、RAM物理映射。
- 未运行综合、布局布线、时序、TD、板卡、位流；未改RTL及旧reference_table.py。

复现：python reference_srif.py
输出：contract.json、vectors.json、manifest.sha256、报告.txt
"""
    return contract, vectors, report


def main():
    contract, vectors, report = build_outputs()
    (HERE / "contract.json").write_text(json.dumps(contract, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (HERE / "vectors.json").write_text(json.dumps(vectors, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (HERE / "报告.txt").write_text(report, encoding="utf-8")
    manifest_names = ("reference_srif.py", "contract.json", "vectors.json", "报告.txt")
    manifest = "".join(f"{sha256(HERE / name)}  {name}\n" for name in manifest_names)
    (HERE / "manifest.sha256").write_text(manifest, encoding="utf-8")
    print("SRIF1_REFERENCE_PASS tables=0,1,32,33,64 age=500,2000 cdc_roundtrip_ns<83.334")


if __name__ == "__main__":
    main()
