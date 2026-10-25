"""Trace the frozen RoadYOLO graph into scheduler-ready DDR descriptors."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import sys
from typing import Any

import torch
from torch import Tensor, nn
from torch.utils._python_dispatch import TorchDispatchMode


CNN_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = CNN_ROOT.parent
if str(CNN_ROOT) not in sys.path:
    sys.path.insert(0, str(CNN_ROOT))

from model import ConvBNAct, RoadYOLOS4  # noqa: E402


KIB = 1024
MIB = 1024 * KIB
ALIGNMENT = 4 * KIB
INPUT_SLOT_BYTES = 512 * KIB
INPUT_BASES = (52 * MIB, 52 * MIB + INPUT_SLOT_BYTES)
FEATURE_BEGIN = 53 * MIB
ARENA_END = 64 * MIB
EXPECTED_FEATURE_BYTES = 7_204_864
EXPECTED_HEAD_BYTES = 169_344


def align_up(value: int, alignment: int = ALIGNMENT) -> int:
    if value < 0 or alignment <= 0 or alignment & (alignment - 1):
        raise ValueError("alignment must be a positive power of two and value nonnegative")
    return (value + alignment - 1) & -alignment


def allocate(cursor: int, raw_bytes: int, arena_end: int = ARENA_END) -> dict[str, int]:
    if raw_bytes <= 0:
        raise ValueError("allocation must contain data")
    base = align_up(cursor)
    size = align_up(raw_bytes)
    if base + size > arena_end:
        raise MemoryError("feature arena exhausted")
    return {"base": base, "raw_bytes": raw_bytes, "allocated_bytes": size,
            "end": base + size}


def shape_hwc(tensor: Tensor) -> list[int]:
    if tensor.ndim != 4 or tensor.shape[0] != 1:
        raise ValueError(f"expected NCHW batch-one tensor, got {tuple(tensor.shape)}")
    return [int(tensor.shape[2]), int(tensor.shape[3]), int(tensor.shape[1])]


class GraphTrace(TorchDispatchMode):
    def __init__(self) -> None:
        super().__init__()
        self.nodes: list[dict[str, Any]] = []
        self.cursor = FEATURE_BEGIN
        self._names: dict[int, str] = {}
        self._dtypes: dict[int, str] = {}
        self._keepalive: list[Tensor] = []
        self._counts = {key: 0 for key in ("split", "concat", "residual", "pool", "upsample")}
        self._by_output: dict[str, dict[str, Any]] = {}

    def bind(self, tensor: Tensor, name: str, dtype: str) -> None:
        self._names[id(tensor)] = name
        self._dtypes[id(tensor)] = dtype
        self._keepalive.append(tensor)

    def resolve(self, tensor: Tensor) -> str:
        try:
            return self._names[id(tensor)]
        except KeyError as exc:
            raise RuntimeError(f"untracked tensor {tuple(tensor.shape)}") from exc

    def dtype(self, tensor: Tensor) -> str:
        return self._dtypes[id(tensor)]

    def next_name(self, kind: str) -> str:
        index = self._counts[kind]
        self._counts[kind] += 1
        return f"{kind}.{index:02d}"

    def append(self, node: dict[str, Any]) -> None:
        node["index"] = len(self.nodes)
        self.nodes.append(node)
        output = node.get("output")
        if output:
            self._by_output[output] = node

    def storage(self, tensor: Tensor, bytes_per_element: int) -> dict[str, int | str]:
        height, width, channels = shape_hwc(tensor)
        raw = math.ceil(height / 4) * math.ceil(width / 4) * 16 * channels * bytes_per_element
        result = allocate(self.cursor, raw)
        self.cursor = result["end"]
        return {**result, "layout": "tile4x4_hwc", "channels_stored": channels,
                "bytes_per_element": bytes_per_element}

    def add_conv(self, name: str, conv: nn.Conv2d, source: Tensor, output: Tensor) -> None:
        input_name = self.resolve(source)
        is_head = name.endswith("cls_out") or name.endswith("reg_out")
        dtype = "int16_q7_8" if is_head else "int8"
        bytes_per_element = 2 if is_head else 1
        height, width, channels = shape_hwc(output)
        kh, kw = conv.kernel_size
        node = {
            "name": name,
            "op": "conv",
            "inputs": [input_name],
            "output": name,
            "input_shape_hwc": shape_hwc(source),
            "output_shape_hwc": [height, width, channels],
            "kernel": [kh, kw],
            "stride": list(conv.stride),
            "padding": list(conv.padding),
            "operator_padding_value": 0,
            "groups": conv.groups,
            "weights": conv.weight.numel(),
            "macs": height * width * channels * (conv.in_channels // conv.groups) * kh * kw,
            "dtype": dtype,
            "storage": self.storage(output, bytes_per_element),
        }
        node["storage"]["partial_tile_invalid_fill"] = 0
        self.append(node)
        self.bind(output, name, dtype)

    def __torch_dispatch__(self, func: Any, types: Any, args: tuple[Any, ...] = (),
                           kwargs: dict[str, Any] | None = None) -> Any:
        kwargs = kwargs or {}
        result = func(*args, **kwargs)

        if func == torch.ops.aten.split.Tensor:
            source, outputs = args[0], result
            name = self.next_name("split")
            offset = 0
            views = []
            for index, output in enumerate(outputs):
                output_name = f"{name}.{index}"
                channels = shape_hwc(output)[2]
                views.append({"output": output_name, "channel_offset": offset,
                              "channels": channels})
                self.bind(output, output_name, self.dtype(source))
                offset += channels
            self.append({"name": name, "op": "split_view", "inputs": [self.resolve(source)],
                         "outputs": views, "axis": "C", "allocation": None})

        elif func == torch.ops.aten.cat.default:
            tensors = list(args[0])
            if int(args[1] if len(args) > 1 else kwargs.get("dim", 0)) != 1:
                raise ValueError("only channel concatenation is supported")
            name = self.next_name("concat")
            dtypes = {self.dtype(tensor) for tensor in tensors}
            if len(dtypes) != 1:
                raise ValueError("concat inputs must share a dtype")
            self.append({"name": name, "op": "concat_view",
                         "inputs": [self.resolve(tensor) for tensor in tensors],
                         "output": name, "shape_hwc": shape_hwc(result),
                         "dtype": dtypes.pop(), "allocation": None})
            self.bind(result, name, self.nodes[-1]["dtype"])

        elif func == torch.ops.aten.upsample_nearest2d.default:
            source = args[0]
            name = self.next_name("upsample")
            src_shape, dst_shape = shape_hwc(source), shape_hwc(result)
            self.append({"name": name, "op": "nearest_view", "inputs": [self.resolve(source)],
                         "output": name, "shape_hwc": dst_shape,
                         "source_index": {"y": "y//2", "x": "x//2"},
                         "scale": [dst_shape[0] // src_shape[0], dst_shape[1] // src_shape[1]],
                         "dtype": self.dtype(source), "allocation": None})
            self.bind(result, name, self.dtype(source))

        elif func == torch.ops.aten.add.Tensor:
            bypass, branch = args[:2]
            if shape_hwc(bypass) != shape_hwc(branch):
                raise ValueError("residual inputs must have equal shapes")
            branch_name = self.resolve(branch)
            producer = self._by_output.get(branch_name)
            if not producer or producer["op"] != "conv" or producer["dtype"] != "int8":
                raise ValueError("residual branch must be an INT8 convolution output")
            name = self.next_name("residual")
            producer["write_transform"] = {
                "op": "post_silu_output_requant_add_sat8",
                "bypass": self.resolve(bypass),
                "requires_aligned_int8_scale": True,
            }
            self.append({"name": name, "op": "residual_view",
                         "inputs": [self.resolve(bypass), branch_name], "output": name,
                         "shape_hwc": shape_hwc(result), "dtype": "int8",
                         "storage_alias": branch_name, "allocation": None})
            self.bind(result, name, "int8")

        elif func == torch.ops.aten.max_pool2d_with_indices.default:
            source, output = args[0], result[0]
            name = self.next_name("pool")
            node = {"name": name, "op": "maxpool", "inputs": [self.resolve(source)],
                    "output": name, "input_shape_hwc": shape_hwc(source),
                    "output_shape_hwc": shape_hwc(output), "kernel": [5, 5],
                    "stride": [1, 1], "padding": [2, 2],
                    "operator_padding_value": -128, "dtype": "int8",
                    "storage": self.storage(output, 1)}
            node["storage"]["partial_tile_invalid_fill"] = 0
            self.append(node)
            self.bind(output, name, "int8")

        return result


def source_hashes() -> dict[str, str]:
    paths = [CNN_ROOT / "model.py", CNN_ROOT / "contract.json", CNN_ROOT / "integer.py",
             Path(__file__).resolve().parent / "deployment_contract.json",
             Path(__file__).resolve()]
    return {path.relative_to(PROJECT_ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in paths}


def resolve_byte_address(graph: dict[str, Any], tensor: str, y: int, x: int, c: int,
                         slot: int = 0) -> int:
    """Return the first byte of one logical element; virtual views recurse to storage."""
    slots = graph["memory"]["input_slots"]
    if slot < 0 or slot >= len(slots):
        raise ValueError("input slot out of range")
    nodes = graph["nodes"]
    by_output = {node["output"]: node for node in nodes if "output" in node}
    split_outputs = {view["output"]: (node, view) for node in nodes
                     if node["op"] == "split_view" for view in node["outputs"]}

    def tensor_shape(name: str) -> list[int]:
        if name == "input":
            return graph["input"]["shape_hwc"]
        if name in split_outputs:
            node, view = split_outputs[name]
            height, width, _channels = tensor_shape(node["inputs"][0])
            return [height, width, view["channels"]]
        try:
            node = by_output[name]
        except KeyError as exc:
            raise ValueError(f"unknown tensor {name!r}") from exc
        return node.get("output_shape_hwc", node.get("shape_hwc"))

    def resolve(name: str, row: int, column: int, channel: int) -> int:
        height, width, channels = tensor_shape(name)
        if not (0 <= row < height and 0 <= column < width and 0 <= channel < channels):
            raise ValueError(f"index outside {name} shape {(height, width, channels)}")
        if name == "input":
            return slots[slot]["base"] + (row * width + column) * channels + channel
        if name in split_outputs:
            node, view = split_outputs[name]
            return resolve(node["inputs"][0], row, column, view["channel_offset"] + channel)

        node = by_output[name]
        if "storage" in node:
            storage = node["storage"]
            tile_columns = math.ceil(width / 4)
            tile = (row // 4) * tile_columns + column // 4
            local_pixel = (row % 4) * 4 + column % 4
            element = tile * 16 * channels + local_pixel * channels + channel
            return storage["base"] + element * storage["bytes_per_element"]
        if node["op"] == "residual_view":
            return resolve(node["storage_alias"], row, column, channel)
        if node["op"] == "nearest_view":
            scale_y, scale_x = node["scale"]
            return resolve(node["inputs"][0], row // scale_y, column // scale_x, channel)
        if node["op"] == "concat_view":
            for source in node["inputs"]:
                source_channels = tensor_shape(source)[2]
                if channel < source_channels:
                    return resolve(source, row, column, channel)
                channel -= source_channels
        raise ValueError(f"tensor {name!r} has no resolvable storage")

    return resolve(tensor, y, x, c)


def build_graph() -> dict[str, Any]:
    model = RoadYOLOS4().to("meta").eval()
    trace = GraphTrace()
    hooks = []
    wrapped = {id(module.conv) for module in model.modules() if isinstance(module, ConvBNAct)}

    for module_name, module in model.named_modules():
        if isinstance(module, ConvBNAct):
            name = f"{module_name}.conv"
            hooks.append(module.register_forward_hook(
                lambda block, inputs, output, name=name: trace.add_conv(
                    name, block.conv, inputs[0], output)))
        elif isinstance(module, nn.Conv2d) and id(module) not in wrapped:
            hooks.append(module.register_forward_hook(
                lambda conv, inputs, output, name=module_name: trace.add_conv(
                    name, conv, inputs[0], output)))

    source = torch.empty(1, 3, 288, 512, device="meta")
    trace.bind(source, "input", "uint8_centered_to_int8")
    try:
        with trace, torch.no_grad():
            outputs = model(source)
    finally:
        for hook in hooks:
            hook.remove()

    convs = [node for node in trace.nodes if node["op"] == "conv"]
    pools = [node for node in trace.nodes if node["op"] == "maxpool"]
    expected_names = [name for name, _conv in model.named_convs()]
    if [node["name"] for node in convs] != expected_names:
        raise RuntimeError("execution trace does not match named_convs order")
    counts = {kind: sum(node["op"] == op for node in trace.nodes) for kind, op in {
        "conv": "conv", "pool": "maxpool", "residual": "residual_view",
        "split": "split_view", "concat": "concat_view", "upsample": "nearest_view"}.items()}
    if counts != {"conv": 67, "pool": 3, "residual": 12,
                  "split": 7, "concat": 15, "upsample": 2}:
        raise RuntimeError(f"frozen graph count mismatch: {counts}")
    feature_bytes = trace.cursor - FEATURE_BEGIN
    head_bytes = sum(math.prod(node["output_shape_hwc"]) * 2 for node in convs
                     if node["dtype"] == "int16_q7_8")
    max_pw_cin = max(node["input_shape_hwc"][2] for node in convs
                     if node["kernel"] == [1, 1] and node["groups"] == 1)
    if (feature_bytes, head_bytes, max_pw_cin) != (
            EXPECTED_FEATURE_BYTES, EXPECTED_HEAD_BYTES, 192):
        raise RuntimeError("frozen storage contract mismatch")

    return {
        "schema": "road_yolo_production_graph_v1",
        "status": "static_schedule_only_fail_closed",
        "source_sha256": source_hashes(),
        "architecture_sha256": model.architecture_hash(),
        "input": {"shape_hwc": [288, 512, 3], "dtype": "uint8", "layout": "NHWC"},
        "memory": {
            "address_unit": "byte_unverified_do_not_enable_dma",
            "input_slots": [{"base": base, "allocated_bytes": INPUT_SLOT_BYTES,
                             "valid_bytes": 288 * 512 * 3, "layout": "NHWC", "dtype": "uint8"}
                            for base in INPUT_BASES],
            "feature_begin": FEATURE_BEGIN,
            "feature_end": trace.cursor,
            "arena_end": ARENA_END,
            "allocation_alignment": ALIGNMENT,
            "liveness_reuse": False,
        },
        "layout": {"name": "tile4x4_hwc", "tile_order": "row_major",
                    "pixel_order": "row_major_hwc", "channel_padding": False,
                    "tile_bytes": "16*C*bytes_per_element", "multi_byte_order": "little"},
        "nodes": trace.nodes,
        "outputs": [trace.resolve(output) for output in outputs],
        "summary": {**counts, "allocations": len(convs) + len(pools),
                    "feature_allocated_bytes": feature_bytes,
                    "raw_head_bytes": head_bytes,
                    "max_pointwise_input_channels": max_pw_cin,
                    "macs": sum(node["macs"] for node in convs)},
        "release_blocks": ["DDR address unit", "write visibility fence", "read return ownership",
                           "residual and concat scale alignment"],
    }


def write_graph(path: Path) -> dict[str, Any]:
    graph = build_graph()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(graph, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return graph


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).resolve().parent / "graph_artifacts" / "graph.json")
    args = parser.parse_args()
    graph = write_graph(args.output)
    print(json.dumps({"output": str(args.output), **graph["summary"]}, sort_keys=True))


if __name__ == "__main__":
    main()
