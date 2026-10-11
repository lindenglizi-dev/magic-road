from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import tempfile
import unittest

import graph


class ProductionGraphTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = graph.build_graph()
        cls.nodes = cls.manifest["nodes"]

    def test_frozen_trace_and_storage(self) -> None:
        summary = self.manifest["summary"]
        self.assertEqual(summary, {
            "conv": 67, "pool": 3, "residual": 12, "split": 7,
            "concat": 15, "upsample": 2, "allocations": 70,
            "feature_allocated_bytes": 7_204_864, "raw_head_bytes": 169_344,
            "max_pointwise_input_channels": 192, "macs": 214_465_536,
        })
        self.assertEqual(self.manifest["outputs"], ["concat.12", "concat.13", "concat.14"])

        allocated = [node for node in self.nodes if node["op"] in ("conv", "maxpool")]
        cursor = graph.FEATURE_BEGIN
        for node in allocated:
            storage = node["storage"]
            self.assertEqual(storage["base"], cursor)
            self.assertEqual(storage["base"] % 4096, 0)
            self.assertEqual(storage["allocated_bytes"] % 4096, 0)
            self.assertEqual(storage["channels_stored"],
                             node["output_shape_hwc"][2])
            h, w, c = node["output_shape_hwc"]
            expected_raw = math.ceil(h / 4) * math.ceil(w / 4) * 16 * c * storage["bytes_per_element"]
            self.assertEqual(storage["raw_bytes"], expected_raw)
            self.assertEqual(storage["partial_tile_invalid_fill"], 0)
            last = graph.resolve_byte_address(
                self.manifest, node["output"], h - 1, w - 1, c - 1)
            self.assertGreaterEqual(last, storage["base"])
            self.assertLessEqual(last + storage["bytes_per_element"],
                                 storage["base"] + storage["raw_bytes"])
            cursor = storage["end"]
        self.assertEqual(cursor, graph.FEATURE_BEGIN + 7_204_864)
        self.assertLessEqual(cursor, graph.ARENA_END)

    def test_views_are_resolved_and_residual_order_is_explicit(self) -> None:
        known = {"input"}
        residuals = []
        for node in self.nodes:
            self.assertTrue(set(node["inputs"]) <= known, node["name"])
            if node["op"] == "split_view":
                known.update(view["output"] for view in node["outputs"])
            else:
                known.add(node["output"])
            if node["op"] == "residual_view":
                residuals.append(node)
                producer = next(item for item in self.nodes
                                if item.get("output") == node["storage_alias"])
                self.assertEqual(producer["write_transform"], {
                    "op": "post_silu_output_requant_add_sat8",
                    "bypass": node["inputs"][0],
                    "requires_aligned_int8_scale": True,
                })
        self.assertEqual(len(residuals), 12)

    def test_heads_slots_hashes_and_fail_closed_boundaries(self) -> None:
        heads = [node for node in self.nodes
                 if node["op"] == "conv" and node["dtype"] == "int16_q7_8"]
        self.assertEqual(len(heads), 6)
        self.assertEqual(sum(math.prod(node["output_shape_hwc"]) * 2 for node in heads), 169_344)
        self.assertEqual([slot["base"] for slot in self.manifest["memory"]["input_slots"]],
                         [52 * graph.MIB, 52 * graph.MIB + 512 * graph.KIB])
        self.assertTrue(all(slot["allocated_bytes"] == 512 * graph.KIB
                            for slot in self.manifest["memory"]["input_slots"]))
        self.assertFalse(self.manifest["memory"]["liveness_reuse"])
        self.assertIn("unverified", self.manifest["memory"]["address_unit"])
        self.assertIn("cnn/hw_validation/production/deployment_contract.json",
                      self.manifest["source_sha256"])
        for relative, digest in self.manifest["source_sha256"].items():
            self.assertEqual(hashlib.sha256((graph.PROJECT_ROOT / relative).read_bytes()).hexdigest(),
                             digest)

    def test_allocator_boundaries(self) -> None:
        exact = graph.allocate(graph.ARENA_END - graph.ALIGNMENT, graph.ALIGNMENT)
        self.assertEqual(exact["end"], graph.ARENA_END)
        with self.assertRaises(MemoryError):
            graph.allocate(graph.ARENA_END, 1)
        with self.assertRaises(MemoryError):
            graph.allocate(graph.ARENA_END - graph.ALIGNMENT, graph.ALIGNMENT + 1)
        with self.assertRaises(ValueError):
            graph.allocate(graph.FEATURE_BEGIN, 0)
        for value, alignment in ((-1, graph.ALIGNMENT), (0, 0), (0, 3)):
            with self.subTest(value=value, alignment=alignment), self.assertRaises(ValueError):
                graph.align_up(value, alignment)

    def test_padding_values_are_not_partial_tile_values(self) -> None:
        convs = [node for node in self.nodes if node["op"] == "conv"]
        pools = [node for node in self.nodes if node["op"] == "maxpool"]
        self.assertTrue(all(node["operator_padding_value"] == 0 for node in convs))
        self.assertTrue(all(node["operator_padding_value"] == -128 for node in pools))
        self.assertTrue(all(node["storage"]["partial_tile_invalid_fill"] == 0
                            for node in convs + pools))

    def test_byte_address_numeric_goldens(self) -> None:
        resolve = lambda tensor, y, x, c, slot=0: graph.resolve_byte_address(
            self.manifest, tensor, y, x, c, slot)
        goldens = {
            ("input", 0, 0, 0, 0): 54_525_952,
            ("input", 0, 0, 0, 1): 55_050_240,
            ("input", 287, 511, 2, 0): 54_968_319,
            ("stem.conv", 0, 3, 15, 0): 55_574_591,
            ("stem.conv", 0, 4, 0, 0): 55_574_784,
            ("csp4.out.conv", 17, 31, 95, 0): 58_170_623,
            ("head4.reg_out", 17, 31, 4, 0): 62_777_518,
            ("split.00.1", 0, 0, 0, 0): 56_311_820,
            ("residual.00", 4, 4, 11, 0): 56_649_931,
            ("concat.00", 0, 0, 0, 0): 56_311_808,
            ("concat.00", 0, 0, 12, 0): 56_864_768,
            ("upsample.00", 4, 8, 0, 0): 58_299_520,
            ("concat.10", 0, 0, 191, 0): 58_237_023,
            ("concat.12", 0, 0, 0, 0): 61_919_232,
            ("concat.12", 0, 0, 2, 0): 61_919_236,
            ("concat.12", 0, 0, 6, 0): 60_997_634,
        }
        addresses = []
        for (tensor, y, x, c, slot), expected in goldens.items():
            with self.subTest(tensor=tensor, y=y, x=x, c=c, slot=slot):
                address = resolve(tensor, y, x, c, slot)
                self.assertEqual(address, expected)
                addresses.append(address)
        self.assertEqual(len(addresses), len(set(addresses)))

    def test_byte_address_rejects_every_index_boundary(self) -> None:
        invalid = [
            ("input", -1, 0, 0, 0), ("input", 288, 0, 0, 0),
            ("input", 0, 512, 0, 0), ("input", 0, 0, 3, 0),
            ("input", 0, 0, 0, -1), ("input", 0, 0, 0, 2),
            ("csp4.out.conv", 18, 0, 0, 0),
            ("csp4.out.conv", 0, 32, 0, 0),
            ("csp4.out.conv", 0, 0, 96, 0),
            ("split.00.1", 0, 0, 12, 0),
            ("concat.10", 0, 0, 192, 0),
            ("missing", 0, 0, 0, 0),
        ]
        for tensor, y, x, c, slot in invalid:
            with self.subTest(tensor=tensor, y=y, x=x, c=c, slot=slot), \
                    self.assertRaises(ValueError):
                graph.resolve_byte_address(self.manifest, tensor, y, x, c, slot)

    def test_reproduction_writes_deterministic_json(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "graph.json"
            first = graph.write_graph(path)
            first_bytes = path.read_bytes()
            second = graph.write_graph(path)
            self.assertEqual(first, second)
            self.assertEqual(first_bytes, path.read_bytes())
            self.assertEqual(json.loads(first_bytes), first)


if __name__ == "__main__":
    unittest.main()
