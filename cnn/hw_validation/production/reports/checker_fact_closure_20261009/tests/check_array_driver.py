"""验证 VG153 对 unpacked array 元素写入的声明根事实。"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SKILL = Path.home() / ".codex" / "skills" / "readable-verilog-generator"
REAL_SOURCE = ROOT.parent / "v19_mac_short_closure_20261008" / "rtl" / "down2_overlap_tile_runner.v"


FIXTURES = {
    "dynamic_unpacked_root.v": """module dynamic_unpacked_root(
    input wire i_clk,
    input wire [1:0] i_write_index,
    input wire [1:0] i_read_index,
    input wire [7:0] i_data,
    output wire [7:0] o_data
);
reg [7:0] memory [0:3];
always @(posedge i_clk) begin
    memory[i_write_index] <= i_data;
end
assign o_data = memory[i_read_index];
endmodule
""",
    "complete_constant_unpacked.v": """module complete_constant_unpacked(
    input wire i_clk,
    input wire [1:0] i_read_index,
    input wire [7:0] i_data,
    output wire [7:0] o_data
);
reg [7:0] memory [0:3];
always @(posedge i_clk) begin
    memory[0] <= i_data;
    memory[1] <= i_data;
    memory[2] <= i_data;
    memory[3] <= i_data;
end
assign o_data = memory[i_read_index];
endmodule
""",
    "unwritten_unpacked.v": """module unwritten_unpacked(
    input wire [1:0] i_read_index,
    output wire [7:0] o_data
);
reg [7:0] memory [0:3];
assign o_data = memory[i_read_index];
endmodule
""",
    "constant_element_mismatch.v": """module constant_element_mismatch(
    input wire i_clk,
    input wire [7:0] i_data,
    output wire [7:0] o_data
);
reg [7:0] memory [0:3];
always @(posedge i_clk) begin
    memory[0] <= i_data;
end
assign o_data = memory[1];
endmodule
""",
    "packed_partial.v": """module packed_partial(
    input wire i_clk,
    input wire [3:0] i_data,
    output wire [7:0] o_data
);
reg [7:0] packed_data;
always @(posedge i_clk) begin
    packed_data[3:0] <= i_data;
end
assign o_data = packed_data;
endmodule
""",
    "indexed_read.v": """module indexed_read(
    input wire i_clk,
    input wire [1:0] i_write_index,
    input wire [7:0] i_data,
    output wire [7:0] o_data
);
reg [1:0] read_index;
reg [7:0] memory [0:3];
always @(posedge i_clk) begin
    memory[i_write_index] <= i_data;
end
assign o_data = memory[read_index];
endmodule
""",
    "unknown_module_output.v": """module unknown_module_output(
    output wire [7:0] o_data
);
wire [7:0] unknown_data;
unknown_child u_unknown(.o_data(unknown_data));
assign o_data = unknown_data;
endmodule
""",
    "multiple_instance_outputs.v": """module known_child(
    input wire [7:0] i_data,
    output wire [7:0] o_data
);
assign o_data = i_data;
endmodule

module multiple_instance_outputs(
    input wire [7:0] i_first,
    input wire [7:0] i_second,
    output wire [7:0] o_data
);
wire [7:0] shared_data;
known_child u_first(.i_data(i_first), .o_data(shared_data));
known_child u_second(.i_data(i_second), .o_data(shared_data));
assign o_data = shared_data;
endmodule
""",
    "module_scope_isolation.v": """module array_writer(
    input wire i_clk,
    input wire [1:0] i_index,
    input wire [7:0] i_data,
    output wire [7:0] o_data
);
reg [7:0] memory [0:3];
always @(posedge i_clk) begin
    memory[i_index] <= i_data;
end
assign o_data = memory[i_index];
endmodule

module array_reader(
    input wire [1:0] i_index,
    output wire [7:0] o_data
);
reg [7:0] memory [0:3];
assign o_data = memory[i_index];
endmodule
""",
    "based_constant_partial.v": """module based_constant_partial(
    input wire i_clk,
    input wire [7:0] i_data,
    output wire [7:0] o_data
);
reg [7:0] memory [0:3];
always @(posedge i_clk) begin
    memory[2'd0] <= i_data;
end
assign o_data = memory[1];
endmodule
""",
    "param_constant_partial.v": """module param_constant_partial(
    input wire i_clk,
    input wire [7:0] i_data,
    output wire [7:0] o_data
);
localparam PARAM_ZERO = 0;
reg [7:0] memory [0:3];
always @(posedge i_clk) begin
    memory[PARAM_ZERO] <= i_data;
end
assign o_data = memory[1];
endmodule
""",
    "dynamic_element_packed_partial.v": """module dynamic_element_packed_partial(
    input wire i_clk,
    input wire [1:0] i_write_index,
    input wire [1:0] i_read_index,
    input wire [3:0] i_data,
    output wire [7:0] o_data
);
reg [7:0] memory [0:3];
always @(posedge i_clk) begin
    memory[i_write_index][3:0] <= i_data;
end
assign o_data = memory[i_read_index];
endmodule
""",
    "multidimensional_partial.v": """module multidimensional_partial(
    input wire i_clk,
    input wire [1:0] i_first_index,
    input wire i_second_index,
    input wire [7:0] i_data,
    output wire [7:0] o_data
);
reg [7:0] memory [0:3][0:1];
always @(posedge i_clk) begin
    memory[i_first_index][i_second_index] <= i_data;
end
assign o_data = memory[i_first_index][i_second_index];
endmodule
""",
}


def _digest(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def _result(path: Path) -> dict[str, object]:
    from scripts.python.quality.vg_contract_liveness import evaluate_liveness_gate
    from scripts.python.quality.vg_semantic_facts import build_vg_facts

    evaluation = evaluate_liveness_gate(build_vg_facts(path), "VG153")
    findings = [finding.to_dict() for finding in evaluation.findings]
    return {
        "status": evaluation.status,
        "applicable": evaluation.applicable,
        "message": evaluation.message,
        "symbols": sorted({str(item.get("symbol") or "") for item in findings if item.get("symbol")}),
        "driver_states": sorted({str(item.get("driver_state") or "") for item in findings if item.get("driver_state")}),
        "findings": findings,
    }


def _expect(result: dict[str, object], *, absent: tuple[str, ...] = (), present: tuple[str, ...] = (), state: str | None = None) -> bool:
    symbols = set(result["symbols"])
    return (
        all(name not in symbols for name in absent)
        and all(name in symbols for name in present)
        and (state is None or result["status"] == state)
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--overlay", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    overlay = args.overlay.resolve()
    output = args.output.resolve()
    output.relative_to(ROOT)
    if output.suffix.lower() != ".json":
        output = output / "array_driver_results.json"
    fixture_dir = output.parent / f"{output.stem}_fixtures"
    fixture_dir.mkdir(parents=True, exist_ok=True)
    output.parent.mkdir(parents=True, exist_ok=True)

    sys.path[:0] = [str(overlay), str(SKILL)]
    fixture_paths = {}
    for name, source in FIXTURES.items():
        path = fixture_dir / name
        path.write_text(source, encoding="utf-8")
        fixture_paths[name] = path

    results = {name: _result(path) for name, path in fixture_paths.items()}
    results["real_runner"] = _result(REAL_SOURCE)
    expectations = {
        "dynamic_unpacked_root": _expect(results["dynamic_unpacked_root.v"], absent=("memory",), state="passed"),
        "complete_constant_unpacked": _expect(results["complete_constant_unpacked.v"], absent=("memory",), state="passed"),
        "unwritten_unpacked": _expect(results["unwritten_unpacked.v"], present=("memory",), state="failed"),
        "constant_element_mismatch": _expect(results["constant_element_mismatch.v"], present=("memory",), state="failed"),
        "packed_partial": _expect(results["packed_partial.v"], present=("packed_data",), state="failed"),
        "indexed_read": _expect(results["indexed_read.v"], absent=("memory",), present=("read_index",), state="failed"),
        "unknown_module_output": _expect(results["unknown_module_output.v"], present=("unknown_data",), state="failed"),
        "multiple_instance_outputs": _expect(results["multiple_instance_outputs.v"], present=("shared_data",), state="failed") and "unresolved_instance_output" in results["multiple_instance_outputs.v"]["driver_states"],
        "module_scope_isolation": _expect(results["module_scope_isolation.v"], present=("memory",), state="failed"),
        "based_constant_partial": _expect(results["based_constant_partial.v"], present=("memory",), state="failed"),
        "param_constant_partial": _expect(results["param_constant_partial.v"], present=("memory",), state="failed"),
        "dynamic_element_packed_partial": _expect(results["dynamic_element_packed_partial.v"], present=("memory",), state="failed"),
        "multidimensional_partial": _expect(results["multidimensional_partial.v"], present=("memory",), state="failed"),
        "real_runner_roots": _expect(results["real_runner"], absent=("reg_halo", "reg_dw_cache", "reg_output_cache")),
    }

    import scripts.python.quality.formatter_ast as formatter_ast
    import scripts.python.quality.formatter_backend.expression_facts as expression_facts
    import scripts.python.quality.vg_contract_liveness as liveness
    import scripts.python.quality.vg_rule_models as rule_models
    import scripts.python.quality.vg_semantic_facts as semantic_facts
    import scripts.python.quality.vg_value_facts as value_facts

    imports = {
        name: {"path": str(path), "sha256": _digest(path)}
        for name, path in {
            "formatter_ast": Path(formatter_ast.__file__).resolve(),
            "expression_facts": Path(expression_facts.__file__).resolve(),
            "vg_contract_liveness": Path(liveness.__file__).resolve(),
            "vg_rule_models": Path(rule_models.__file__).resolve(),
            "vg_semantic_facts": Path(semantic_facts.__file__).resolve(),
            "vg_value_facts": Path(value_facts.__file__).resolve(),
        }.items()
    }
    expected_liveness = overlay / "scripts/python/quality/vg_contract_liveness.py"
    if (overlay / "scripts/__init__.py").exists() and expected_liveness.exists():
        assert Path(imports["vg_contract_liveness"]["path"]) == expected_liveness

    report = {
        "all_passed": all(expectations.values()),
        "scope": "VG153 target semantics only; unrelated strict findings are not treated as an all-gates pass.",
        "array_driver_limit": "Dynamic unpacked writes prove a declaration-root driver, not per-element initialization coverage.",
        "cases": {
            name: {
                "passed": expectations[name],
                "result": results["real_runner" if name == "real_runner_roots" else name + ".v"],
            }
            for name in expectations
        },
        "fixture_sha256": {name: _digest(path) for name, path in fixture_paths.items()},
        "source_sha256": {str(REAL_SOURCE): _digest(REAL_SOURCE), str(Path(__file__).resolve()): _digest(Path(__file__).resolve())},
        "import_sha256": imports,
    }
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"all_passed": report["all_passed"], "output": str(output)}, ensure_ascii=False))
    return 0 if report["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
