"""Trainable folded RoadYOLO graph with deployment-exact integer forward values.

The integer path is the existing CPU reference.  Gradients use a local
straight-through float surrogate whose forward value is corrected at every
graph node to the integer reference value.  This is preparatory QAT machinery,
not a GPU training integration or a production candidate.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Mapping

import numpy as np
import torch
from torch import Tensor, nn
from torch.nn import functional as F

from cnn.integer import encode_multiplier
from cnn.hw_validation.production.trained_integer import (
    IntegerModel, load_package, parameter_shapes, write_package)


class _FoldedConv(nn.Module):
    def __init__(self, weight: Tensor, bias: Tensor, weight_scale: np.ndarray) -> None:
        super().__init__()
        self.weight = nn.Parameter(weight.detach().to(dtype=torch.float32, device="cpu").clone())
        self.bias = nn.Parameter(bias.detach().to(dtype=torch.float32, device="cpu").clone())
        # Float64 preserves the package JSON value used to encode multipliers.
        self.register_buffer("weight_scale", torch.as_tensor(weight_scale, dtype=torch.float64))


def _ste_quantize(value: Tensor, scale: Tensor | float, minimum: int, maximum: int) -> Tensor:
    quantized = torch.round(value / scale).clamp(minimum, maximum) * scale
    return value + (quantized - value).detach()


class _ExactSTE(torch.autograd.Function):
    @staticmethod
    def forward(ctx, exact: Tensor, surrogate: Tensor) -> Tensor:
        return exact.clone()

    @staticmethod
    def backward(ctx, gradient: Tensor):
        return None, gradient


class QATExactModel(nn.Module):
    """Fixed graph/scales QAT module with exact deployed forward values.

    ``forward`` accepts centered NCHW pixels (integer-valued floats in
    ``[-128, 127]``) and returns three dequantized NCHW Q7.8 heads.  The module
    owns trainable folded FP32 weight and bias tensors.  Activation and
    per-output-channel weight scales remain frozen.
    """

    def __init__(self, graph: dict, folded: Mapping[str, tuple[Tensor, Tensor]],
                 scales: Mapping[str, float], weight_scales: Mapping[str, object]) -> None:
        super().__init__()
        self.graph = graph
        self.scales = {name: float(value) for name, value in scales.items()}
        convs = [node for node in graph["nodes"] if node["op"] == "conv"]
        names = [node["name"] for node in convs]
        if set(folded) != set(names) or set(weight_scales) != set(names):
            raise ValueError("folded tensors or weight scales differ from graph")
        self.layers = nn.ModuleList()
        for node in convs:
            name = node["name"]
            weight, bias = folded[name]
            expected = parameter_shapes(node)
            ws = np.asarray(weight_scales[name], dtype=np.float64)
            if tuple(weight.shape) != expected["weights"] or tuple(bias.shape) != expected["bias"]:
                raise ValueError(f"{name}: folded tensor shape differs from graph")
            if ws.shape != expected["bias"] or not np.isfinite(ws).all() or np.any(ws <= 0):
                raise ValueError(f"{name}: invalid fixed weight scale")
            self.layers.append(_FoldedConv(weight, bias, ws))
        self._layer_index = {name: index for index, name in enumerate(names)}
        # Reuse IntegerModel's strict scale and package-shape validation.
        IntegerModel(graph, self.integer_parameters(), self.scales)

    @classmethod
    def from_package(cls, package: str | Path,
                     folded: Mapping[str, tuple[Tensor, Tensor]],
                     quantization: str | Path | Mapping[str, dict]) -> "QATExactModel":
        """Load frozen graph/scales/weight scales and verify initial parity."""
        integer, _manifest = load_package(Path(package))
        metadata = (json.loads(Path(quantization).read_text(encoding="utf-8"))
                    if isinstance(quantization, (str, Path)) else dict(quantization))
        weight_scales = {name: row["weight_scale"] for name, row in metadata.items()}
        model = cls(integer.graph, folded, integer.scales, weight_scales)
        actual_parameters = model.integer_parameters()
        for name, expected in integer.parameters.items():
            for field, value in expected.items():
                if not np.array_equal(actual_parameters[name][field], value):
                    raise ValueError(f"{name}.{field}: folded tensors do not reproduce package")
            row = metadata[name]
            node = next(item for item in integer.graph["nodes"] if item.get("name") == name)
            if (not math.isclose(float(row["input_scale"]),
                                 integer.scales[node["inputs"][0]], rel_tol=0, abs_tol=1e-15)
                    or not math.isclose(float(row["output_scale"]), integer.scales[name], rel_tol=0, abs_tol=1e-15)):
                raise ValueError(f"{name}: quantization metadata scale differs from package")
        return model

    def folded_state(self) -> dict[str, tuple[Tensor, Tensor]]:
        return {name: (self.layers[index].weight, self.layers[index].bias)
                for name, index in self._layer_index.items()}

    def integer_parameters(self) -> dict[str, dict[str, np.ndarray]]:
        """Encode current FP32 parameters using the frozen QAT scales."""
        parameters = {}
        by_name = {node["name"]: node for node in self.graph["nodes"] if node["op"] == "conv"}
        for name, index in self._layer_index.items():
            node, layer = by_name[name], self.layers[index]
            weight = layer.weight.detach().cpu().numpy().astype(np.float64)
            bias = layer.bias.detach().cpu().numpy().astype(np.float64)
            weight_scale = layer.weight_scale.detach().cpu().numpy().astype(np.float64)
            if not np.isfinite(weight).all() or not np.isfinite(bias).all():
                raise ValueError(f"{name}: nonfinite weight or bias")
            accumulator_scale = self.scales[node["inputs"][0]] * weight_scale
            quantized_bias = np.rint(bias / accumulator_scale)
            if np.any(quantized_bias < -(1 << 31)) or np.any(quantized_bias >= 1 << 31):
                raise OverflowError(f"{name}: quantized bias outside INT32")
            pre = [encode_multiplier(float(scale * 256)) for scale in accumulator_scale]
            encoded = {
                "weights": np.clip(np.rint(weight / weight_scale[:, None, None, None]),
                                   -128, 127).astype(np.int8),
                "bias": quantized_bias.astype("<i4"),
                "pre_multiplier": np.asarray([value[0] for value in pre], dtype="<i4"),
                "pre_shift": np.asarray([value[1] for value in pre], dtype=np.uint8),
            }
            if node["dtype"] == "int8":
                multiplier, shift = encode_multiplier(1 / (256 * self.scales[name]))
                encoded["post_multiplier"] = np.asarray([multiplier], dtype="<i4")
                encoded["post_shift"] = np.asarray([shift], dtype=np.uint8)
            bound = (np.abs(encoded["bias"].astype(np.int64)) +
                     128 * np.abs(encoded["weights"].astype(np.int64)).sum((1, 2, 3)))
            if np.any(bound >= 1 << 32):
                raise OverflowError(f"{name}: signed33 bound failed")
            parameters[name] = encoded
        return parameters

    @staticmethod
    def _input_int8(image: Tensor) -> np.ndarray:
        if image.ndim != 4 or image.shape[0] < 1 or image.shape[1:] != (3, 288, 512):
            raise ValueError("expected centered NCHW input with shape N,3,288,512")
        if not image.is_floating_point():
            raise ValueError("QAT input must be floating point")
        if not torch.isfinite(image).all() or torch.any(image < -128) or torch.any(image > 127):
            raise ValueError("input outside centered INT8 range")
        rounded = torch.round(image.detach())
        if not torch.equal(rounded, image.detach()):
            raise ValueError("deployment-exact input must be integer-valued centered pixels")
        return rounded.to(torch.int8).permute(0, 2, 3, 1).contiguous().cpu().numpy()

    def integer_forward(self, image: Tensor, *, capture: bool = False):
        """Return raw batched INT16 heads from the CPU integer reference."""
        inputs = self._input_int8(image)
        integer = IntegerModel(self.graph, self.integer_parameters(), self.scales)
        heads, statistics, captures = [], [], [] if capture else None
        for sample in inputs:
            output, stats, values = integer.forward(sample, capture=capture)
            heads.append(output)
            statistics.append(stats)
            if capture:
                captures.append(values)
        batched = [np.stack([sample[index] for sample in heads], axis=0)
                   for index in range(len(self.graph["outputs"]))]
        return batched, statistics, captures

    @staticmethod
    def _exact_tensor(captures: list[dict], name: str, scale: float,
                      like: Tensor) -> Tensor:
        array = np.stack([values[name] for values in captures], axis=0)
        return torch.as_tensor(array, device=like.device).permute(0, 3, 1, 2).to(like.dtype) * scale

    def forward(self, image: Tensor, *, capture: bool = False):
        _heads, _statistics, exact = self.integer_forward(image, capture=True)
        source = _ste_quantize(image, 1.0, -128, 127)
        values = {"input": _ExactSTE.apply(
            self._exact_tensor(exact, "input", 1.0, source), source)}
        trace = {"input": values["input"]}
        for node in self.graph["nodes"]:
            name = node["name"]
            if node["op"] == "conv":
                layer = self.layers[self._layer_index[name]]
                weight_scale = layer.weight_scale.to(layer.weight.dtype)[:, None, None, None]
                weight = _ste_quantize(layer.weight, weight_scale, -128, 127)
                input_scale = self.scales[node["inputs"][0]]
                bias_scale = input_scale * layer.weight_scale.to(layer.bias.dtype)
                bias = _ste_quantize(layer.bias, bias_scale, -(1 << 31), (1 << 31) - 1)
                result = F.conv2d(values[node["inputs"][0]], weight, bias,
                                  stride=node["stride"], padding=node["padding"],
                                  groups=node["groups"])
                result = _ste_quantize(result, 1 / 256, -32768, 32767)
                exact_pre = self._exact_tensor(exact, name + ":pre", 1 / 256, result)
                result = _ExactSTE.apply(exact_pre, result)
                trace[name + ":pre"] = result
                if node["dtype"] == "int8":
                    result = _ste_quantize(F.silu(result), self.scales[name], -128, 127)
                exact_value = self._exact_tensor(exact, name, self.scales[name], result)
                values[name] = _ExactSTE.apply(exact_value, result)
                trace[name] = values[name]
                continue

            inputs = [values[key] for key in node["inputs"]]
            if node["op"] == "split_view":
                for view in node["outputs"]:
                    result = inputs[0][:, view["channel_offset"]:
                                       view["channel_offset"] + view["channels"]]
                    exact_value = self._exact_tensor(exact, view["output"],
                                                     self.scales[view["output"]], result)
                    values[view["output"]] = _ExactSTE.apply(exact_value, result)
                    trace[view["output"]] = values[view["output"]]
            elif node["op"] == "concat_view":
                result = torch.cat(inputs, dim=1)
                exact_value = self._exact_tensor(exact, node["output"], self.scales[node["output"]], result)
                values[node["output"]] = _ExactSTE.apply(exact_value, result)
                trace[node["output"]] = values[node["output"]]
            elif node["op"] == "nearest_view":
                result = F.interpolate(inputs[0], scale_factor=node["scale"], mode="nearest")
                exact_value = self._exact_tensor(exact, node["output"], self.scales[node["output"]], result)
                values[node["output"]] = _ExactSTE.apply(exact_value, result)
                trace[node["output"]] = values[node["output"]]
            elif node["op"] == "residual_view":
                result = _ste_quantize(inputs[0] + inputs[1], self.scales[node["output"]], -128, 127)
                exact_value = self._exact_tensor(exact, node["output"], self.scales[node["output"]], result)
                values[node["output"]] = _ExactSTE.apply(exact_value, result)
                trace[node["output"]] = values[node["output"]]
            elif node["op"] == "maxpool":
                result = F.max_pool2d(inputs[0], 5, 1, 2)
                exact_value = self._exact_tensor(exact, node["output"], self.scales[node["output"]], result)
                values[node["output"]] = _ExactSTE.apply(exact_value, result)
                trace[node["output"]] = values[node["output"]]
            else:
                raise ValueError(f"unsupported frozen operator: {node['op']}")
        outputs = [values[name] for name in self.graph["outputs"]]
        return (outputs, trace) if capture else outputs

    def export_package(self, output: str | Path, provenance: dict) -> dict:
        """Write current parameters without changing the frozen weight scales."""
        return write_package(Path(output), self.graph, self.integer_parameters(), self.scales,
                             dict(provenance, qat_exact_fixed_weight_scales=True,
                                  qat_export_scope="numeric_selftest_not_quality_run"))


__all__ = ["QATExactModel"]
