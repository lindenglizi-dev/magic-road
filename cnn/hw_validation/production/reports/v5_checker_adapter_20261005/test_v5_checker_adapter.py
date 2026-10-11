"""V5 项目级 checker overlay 的最小正负例。"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.python.quality.formatter_ast import build_ast_report_for_text
from scripts.python.quality.vg_comb_targets import (
    build_hierarchy_bindings,
    build_module_implementation_index,
    enumerate_definition_roots,
)
from scripts.python.quality.vg_control_rules import evaluate_control_gate
from scripts.python.quality.vg_expression_rules import evaluate_expression_gate
from scripts.python.quality.vg_semantic_facts import build_vg_facts


class TypedOpaqueInterfaceTests(unittest.TestCase):
    """确认 typed opaque ownership 不会放松真实未知或冲突。"""

    retained_roots: list[Path] = []

    @classmethod
    def setUpClass(cls):
        cls.retained_parent = Path(__file__).resolve().parent / "retained_test_inputs"
        cls.retained_parent.mkdir(exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        for path_root in cls.retained_roots:
            print(f"retained_test_input={path_root}")

    def _facts_and_drivers(self, top: str, interface: str | None):
        root = Path(tempfile.mkdtemp(prefix="ownership_", dir=self.retained_parent))
        self.retained_roots.append(root)
        top_path = root / "design_top.v"
        top_path.write_text(top, encoding="utf-8")
        external_sources = ()
        if interface is not None:
            interface_path = root / "opaque_interface.v"
            interface_path.write_text(interface, encoding="utf-8")
            external_sources = (interface_path,)
        facts = build_vg_facts(top_path, external_interface_sources=external_sources)
        self.assertEqual((), facts.parse_errors)
        index = build_module_implementation_index(facts)
        roots = enumerate_definition_roots(index)
        self.assertEqual(1, len(roots))
        graph = build_hierarchy_bindings(roots[0], index, {})
        drivers = {
            endpoint.target: tuple(producers)
            for endpoint, producers in graph.endpoint_drivers
        }
        return facts, drivers

    def test_input_sink_does_not_pollute_parent(self):
        _, drivers = self._facts_and_drivers(
            """module design_top(
 input wire i_enable,
 output wire o_result
);
wire child_data;
opaque_box u_box(
 .enable(i_enable),
 .data(child_data)
);
assign o_result = child_data;
endmodule
""",
            """module opaque_box(enable,data);
input enable;
output data;
endmodule
""",
        )
        self.assertNotIn("i_enable", drivers)
        self.assertEqual(
            "external output implementation is unknown",
            drivers["child_data"][0].unknown_reason,
        )

    def test_real_feedback_remains_unknown(self):
        _, drivers = self._facts_and_drivers(
            """module design_top(
 output wire o_result
);
wire feedback;
opaque_box u_box(
 .data_in(feedback),
 .data_out(feedback)
);
assign o_result = feedback;
endmodule
""",
            """module opaque_box(data_in,data_out);
input data_in;
output data_out;
endmodule
""",
        )
        self.assertTrue(drivers["feedback"][0].unknown_reason)

    def test_multiple_external_outputs_remain_multiple_drivers(self):
        _, drivers = self._facts_and_drivers(
            """module design_top(
 output wire o_result
);
wire shared_data;
opaque_box u_left(.data(shared_data));
opaque_box u_right(.data(shared_data));
assign o_result = shared_data;
endmodule
""",
            """module opaque_box(data);
output data;
endmodule
""",
        )
        self.assertEqual(2, len(drivers["shared_data"]))

    def test_width_mismatch_still_fails_vg097(self):
        facts, _ = self._facts_and_drivers(
            """module design_top(
 output wire [3:0] o_result
);
opaque_box u_box(.data(o_result));
endmodule
""",
            """module opaque_box(data);
output [7:0] data;
endmodule
""",
        )
        result = evaluate_control_gate("VG097", facts)
        self.assertEqual("failed", result.status)
        self.assertIn("port_width=8 signal_width=4", result.findings[0].evidence)

    def test_inout_remains_unresolved(self):
        _, drivers = self._facts_and_drivers(
            """module design_top(
 inout wire io_bus
);
opaque_box u_box(.bus(io_bus));
endmodule
""",
            """module opaque_box(bus);
inout bus;
endmodule
""",
        )
        self.assertEqual(
            "external inout ownership is unresolved",
            drivers["io_bus"][0].unknown_reason,
        )

    def test_missing_interface_remains_unknown(self):
        _, drivers = self._facts_and_drivers(
            """module design_top(
 output wire o_result
);
wire child_data;
missing_box u_box(.data(child_data));
assign o_result = child_data;
endmodule
""",
            None,
        )
        self.assertEqual(
            "missing module implementation",
            drivers["child_data"][0].unknown_reason,
        )

    def test_output_to_parent_input_exposes_direction_conflict(self):
        _, drivers = self._facts_and_drivers(
            """module design_top(
 input wire i_conflict
);
opaque_box u_box(.data(i_conflict));
endmodule
""",
            """module opaque_box(data);
output data;
endmodule
""",
        )
        self.assertEqual(
            "external output implementation is unknown",
            drivers["i_conflict"][0].unknown_reason,
        )


class FormatterAndWidthTests(unittest.TestCase):
    """覆盖 V5-03 前端形状和真实宽度正负例。"""

    retained_roots: list[Path] = []

    @classmethod
    def setUpClass(cls):
        cls.retained_parent = Path(__file__).resolve().parent / "retained_test_inputs"
        cls.retained_parent.mkdir(exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        for path_root in cls.retained_roots:
            print(f"retained_test_input={path_root}")

    def _facts(self, source: str, *, external: str | None = None):
        root = Path(tempfile.mkdtemp(prefix="frontend_", dir=self.retained_parent))
        self.retained_roots.append(root)
        source_path = root / "design.v"
        source_path.write_text(source, encoding="utf-8")
        external_sources = ()
        if external is not None:
            external_path = root / "child_interface.v"
            external_path.write_text(external, encoding="utf-8")
            external_sources = (external_path,)
        return build_vg_facts(source_path, external_interface_sources=external_sources)

    def test_bare_zero_port_module_uses_original_formatter(self):
        report = build_ast_report_for_text("module tb_schema;\nreg signal;\nendmodule\n")
        self.assertEqual([], report["diagnostics"])
        self.assertEqual([], report["modules"][0]["ports"])

    def test_periodic_always_parses_but_production_delay_fails(self):
        facts = self._facts(
            "module production_delay();\nreg i_clk;\nalways #5 i_clk = ~i_clk;\nendmodule\n"
        )
        self.assertEqual((), facts.parse_errors)
        self.assertEqual("always #5", facts.sources[0].report["modules"][0]["always"][0]["header"])
        self.assertEqual("failed", evaluate_control_gate("VG131", facts).status)

    def test_malformed_periodic_always_still_fails_closed(self):
        report = build_ast_report_for_text(
            "module malformed_delay();\nreg i_clk;\nalways #() i_clk = ~i_clk;\nendmodule\n"
        )
        self.assertTrue(any(item["severity"] == "error" for item in report["diagnostics"]))

    def test_numeric_and_signed_ten_bit_slices_pass(self):
        facts = self._facts(
            """module signed_slice(
 input wire signed [9:0] i_data,
 output wire o_equal
);
reg signed [10:0] wider;
assign o_equal = (i_data == wider[9:0]);
endmodule
"""
        )
        result = evaluate_expression_gate("VG085", facts)
        self.assertEqual("passed", result.status)
        self.assertTrue(result.applicable)

    def test_whole_vector_equal_unequal_and_explicit_sign_extension(self):
        facts = self._facts(
            """module signed_vector(
 input wire signed [7:0] i_data,
 input wire signed [9:0] i_peer,
 output wire o_equal,
 output wire o_unequal
);
wire signed [9:0] extended;
assign extended = {i_data[7], i_data[7], i_data};
assign o_equal = (extended == i_peer);
assign o_unequal = (extended != i_peer);
endmodule
"""
        )
        self.assertEqual((), facts.parse_errors)
        module = facts.sources[0].report["modules"][0]
        extension = next(item for item in module["comb_expressions"] if item["target"] == "extended")
        self.assertEqual("", extension["parse_error"])
        result = evaluate_expression_gate("VG085", facts)
        self.assertEqual("passed", result.status)
        self.assertTrue(result.applicable)

    def test_true_slice_width_mismatch_fails(self):
        facts = self._facts(
            """module mismatched_slice(
 input wire [9:0] i_data,
 output wire o_equal
);
reg [10:0] wider;
assign o_equal = (i_data == wider[10:0]);
endmodule
"""
        )
        result = evaluate_expression_gate("VG085", facts)
        self.assertEqual("failed", result.status)
        self.assertIn("wider[10:0]", result.findings[0].evidence)

    def test_parameter_slice_resolves_with_formatter_facts(self):
        facts = self._facts(
            """module parameter_slice #(
 parameter WIDTH = 10
)(
 input wire [WIDTH-1:0] i_data,
 output wire o_equal
);
reg signed [WIDTH:0] wider;
assign o_equal = (i_data == wider[WIDTH-1:0]);
endmodule
"""
        )
        result = evaluate_expression_gate("VG085", facts)
        self.assertEqual("passed", result.status)
        self.assertTrue(result.applicable)

    def test_unknown_parameter_slice_is_inconclusive(self):
        facts = self._facts(
            """module unknown_slice(
 input wire [9:0] i_data,
 output wire o_equal
);
reg [10:0] wider;
assign o_equal = (i_data == wider[UNKNOWN-1:0]);
endmodule
"""
        )
        self.assertEqual("inconclusive", evaluate_expression_gate("VG085", facts).status)

    def test_parameter_binding_and_real_mismatch(self):
        interface = """module child_box #(
 parameter WIDTH = 8
)(
 output wire [WIDTH-1:0] data
);
endmodule
"""
        matching = self._facts(
            """module binding_ok(
 output wire [9:0] o_data
);
child_box #(.WIDTH(10)) u_child(.data(o_data));
endmodule
""",
            external=interface,
        )
        mismatched = self._facts(
            """module binding_bad(
 output wire [8:0] o_data
);
child_box #(.WIDTH(10)) u_child(.data(o_data));
endmodule
""",
            external=interface,
        )
        self.assertEqual("passed", evaluate_control_gate("VG097", matching).status)
        self.assertEqual("failed", evaluate_control_gate("VG097", mismatched).status)


if __name__ == "__main__":
    unittest.main(verbosity=2)
