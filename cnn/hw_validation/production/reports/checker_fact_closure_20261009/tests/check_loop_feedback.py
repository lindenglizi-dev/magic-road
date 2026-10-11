"""用真实 formatter 事实核对 VG136 的 for 归纳变量边界。"""

import argparse
import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SKILL = Path(r"C:\Users\lenovo\.codex\skills\readable-verilog-generator")
REAL_RTL = ROOT.parent / "mac_task_stream_20261009/checker_replay_final/inputs/candidate"


def digest(path: Path) -> str:
    with path.open("rb") as source:
        return hashlib.file_digest(source, "sha256").hexdigest()


def result_record(result) -> dict[str, object]:
    return {
        "status": result.status,
        "findings": [finding.evidence for finding in result.findings],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--overlay", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    overlay = args.overlay.resolve()
    output = args.output.resolve()
    output.relative_to(ROOT)
    sys.dont_write_bytecode = True
    sys.path[:0] = [str(overlay), str(SKILL)]

    from scripts.python.quality.vg_semantic_facts import build_vg_facts
    from scripts.python.quality import vg_structure_rules as fixed

    def module(name: str, ports: tuple[str, ...], body: str) -> str:
        return f"module {name}\n(\n" + ",\n".join(ports) + f"\n);\n{body}\nendmodule\n"

    cases = {
        "induction": module("induction", ("input [3:0] data", "output reg [3:0] value"), """
integer index;
always @(*) begin
    value = 4'd0;
    for (index = 0; index < 4; index = index + 1)
        value[index] = data[index];
end
"""),
        "self_feedback": module("self_feedback", ("input source", "output reg value"), """
always @(*) begin
    value = value | source;
end
"""),
        "multi_node_feedback": module("multi_node_feedback", ("output reg first", "output reg second"), """
always @(*) begin
    first = second;
    second = first;
end
"""),
        "ordinary_named_integer": module("ordinary_named_integer", (), """
integer lane_index;
always @(*) begin
    lane_index = lane_index + 1;
end
"""),
        "loop_body_feedback": module("loop_body_feedback", ("output reg [3:0] value",), """
integer index;
always @(*) begin
    value = 4'd0;
    for (index = 0; index < 4; index = index + 1) begin
        index = index + 2;
        value[index] = 1'b1;
    end
end
"""),
        "loop_body_multi_node": module("loop_body_multi_node", ("output reg [3:0] value",), """
integer index;
integer mirror;
always @(*) begin
    value = 4'd0;
    for (index = 0; index < 4; index = index + 1) begin
        mirror = index;
        index = mirror;
        value[index] = 1'b1;
    end
end
"""),
        "concat_body_write": module("concat_body_write", ("output reg [3:0] value",), """
integer index;
always @(*) begin
    value = 4'd0;
    for (index = 0; index < 4; index = index + 1) begin
        {index, value[index]} = {index + 1, 1'b1};
    end
end
"""),
        "loop_variable_escape": module(
            "loop_variable_escape",
            ("input [3:0] data", "output reg [3:0] value", "output reg escaped"),
            """
integer index;
always @(*) begin
    value = 4'd0;
    for (index = 0; index < 4; index = index + 1)
        value[index] = data[index];
    escaped = index[0];
end
""",
        ),
        "runtime_step": module("runtime_step", ("input [2:0] step", "output reg [3:0] value"), """
integer index;
always @(*) begin
    value = 4'd0;
    for (index = 0; index < 4; index = index + step)
        value[index] = 1'b1;
end
"""),
        "zero_step": module("zero_step", ("output reg [3:0] value",), """
integer index;
always @(*) begin
    value = 4'd0;
    for (index = 0; index < 4; index = index + 0)
        value[index] = 1'b1;
end
"""),
        "identity_update": module("identity_update", ("output reg [3:0] value",), """
integer index;
always @(*) begin
    value = 4'd0;
    for (index = 0; index < 4; index = index)
        value[index] = 1'b1;
end
"""),
        "narrow_reg_induction": module("narrow_reg_induction", ("output reg [15:0] value",), """
reg [3:0] index;
always @(*) begin
    value = 16'd0;
    for (index = 0; index < 16; index = index + 1)
        value[index] = 1'b1;
end
"""),
        "wrong_direction": module("wrong_direction", ("output reg [3:0] value",), """
integer index;
always @(*) begin
    value = 4'd0;
    for (index = 0; index < 4; index = index - 1)
        value[index] = 1'b1;
end
"""),
        "non_induction_update": module("non_induction_update", ("output reg [3:0] value",), """
integer index;
always @(*) begin
    value = 4'd0;
    for (index = 1; index < 4; index = index * 2)
        value[index] = 1'b1;
end
"""),
        "sequential_escape": module(
            "sequential_escape",
            ("input i_clk", "output reg [3:0] value", "output reg escaped"),
            """
integer index;
always @(*) begin
    value = 4'd0;
    for (index = 0; index < 4; index = index + 1)
        value[index] = 1'b1;
end
always @(posedge i_clk) begin
    escaped <= index[0];
end
""",
        ),
        "instance_escape": module("instance_escape", ("output reg [3:0] value",), """
integer index;
always @(*) begin
    value = 4'd0;
    for (index = 0; index < 4; index = index + 1)
        value[index] = 1'b1;
end
escape_sink escape_sink_Inst(
    .value(index)
);
""") + module("escape_sink", ("input [31:0] value",), ""),
    }
    expected = {
        "induction": ("failed", "passed"),
        "self_feedback": ("failed", "failed"),
        "multi_node_feedback": ("failed", "failed"),
        "ordinary_named_integer": ("failed", "failed"),
        "loop_body_feedback": ("failed", "failed"),
        "loop_body_multi_node": ("failed", "failed"),
        "concat_body_write": ("failed", "failed"),
        "loop_variable_escape": ("failed", "failed"),
        "runtime_step": ("failed", "failed"),
        "zero_step": ("failed", "failed"),
        "identity_update": ("failed", "failed"),
        "narrow_reg_induction": ("failed", "failed"),
        "wrong_direction": ("failed", "failed"),
        "non_induction_update": ("failed", "failed"),
        "sequential_escape": ("failed", "failed"),
        "instance_escape": ("failed", "failed"),
    }
    records: dict[str, object] = {}
    directory = output.parent / "loop_feedback_fixtures"
    directory.resolve().relative_to(ROOT)
    directory.mkdir(parents=True, exist_ok=True)
    for name, text in cases.items():
        path = directory / f"{name}.v"
        path.write_text(text, encoding="utf-8")
        facts = build_vg_facts(path, include_testbench=False)
        assert not facts.parse_errors, (name, facts.parse_errors)
        original = fixed._UPSTREAM.evaluate_structure_gate("VG136", facts)
        repaired = fixed.evaluate_structure_gate("VG136", facts)
        actual = (original.status, repaired.status)
        records[name] = {
            "expected": expected[name],
            "actual": actual,
            "passed": actual == expected[name],
            "original": result_record(original),
            "fixed": result_record(repaired),
            "fixture_path": str(path.relative_to(ROOT)),
            "fixture_sha256": digest(path),
        }

    range_path = directory / "array_range.v"
    range_path.write_text(
        module("array_range", ("output reg value",),
               "reg data [0:1];\nalways @(*) begin\n    value = data[2];\nend"),
        encoding="utf-8",
    )
    range_facts = build_vg_facts(range_path, include_testbench=False)
    delegated = fixed.evaluate_structure_gate("VG130", range_facts)
    upstream = fixed._UPSTREAM.evaluate_structure_gate("VG130", range_facts)
    delegation_passed = delegated == upstream

    actual_records = {}
    for name, false_node in (
        ("road_dynamic_postprocess.v", "check_lane"),
        ("down2_dynamic_tile_runner.v", "lane_index"),
    ):
        facts = build_vg_facts(REAL_RTL / name, include_testbench=False)
        assert not facts.parse_errors, (name, facts.parse_errors)
        original = fixed._UPSTREAM.evaluate_structure_gate("VG136", facts)
        repaired = fixed.evaluate_structure_gate("VG136", facts)
        original_evidence = {finding.evidence for finding in original.findings}
        passed_case = original.status == "failed" and false_node in original_evidence and repaired.status == "passed"
        actual_records[name] = {
            "passed": passed_case,
            "false_node": false_node,
            "original": result_record(original),
            "fixed": result_record(repaired),
            "source_sha256": digest(REAL_RTL / name),
        }

    all_passed = (
        all(record["passed"] for record in records.values())
        and all(record["passed"] for record in actual_records.values())
        and delegation_passed
    )
    report = {
        "all_passed": all_passed,
        "overlay": str(overlay),
        "overlay_rule_origin": str(Path(fixed.__file__).resolve()),
        "upstream_rule_origin": str(Path(fixed._UPSTREAM.__file__).resolve()),
        "fixture_cases": records,
        "actual_rtl": actual_records,
        "unaffected_vg130_delegated_exactly": delegation_passed,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"all_passed": all_passed, "output": str(output)}, ensure_ascii=False))
    return 0 if all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
