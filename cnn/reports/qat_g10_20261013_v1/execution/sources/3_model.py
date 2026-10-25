"""Frozen floating-point RoadYOLO-S4-512 reference model.

The layer graph is intentionally explicit.  Export and RTL tooling rely on the
stable convolution names, output order, and architecture hash defined here.
"""

from __future__ import annotations

from collections import OrderedDict
import hashlib
import json
import math
from typing import Callable, Iterable

import torch
from torch import Tensor, nn
import torch.nn.functional as F


INPUT_HEIGHT = 288
INPUT_WIDTH = 512
NUM_CLASSES = 2
OUTPUT_CHANNELS = 5 + NUM_CLASSES
STRIDES = (4, 8, 16)

EXPECTED_CONV_COUNT = 67
EXPECTED_CONV_WEIGHTS = 113_100
EXPECTED_FOLDED_BIASES = 2_501
EXPECTED_MACS = 214_465_536
EXPECTED_SILU_COUNT = 61


class ConvBNAct(nn.Module):
    """Convolution followed by batch normalization and SiLU."""

    def __init__(self, in_channels: int, out_channels: int, kernel_size: int = 1,
                 stride: int = 1, groups: int = 1) -> None:
        super().__init__()
        padding = kernel_size // 2
        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size, stride,
                              padding, groups=groups, bias=False)
        self.bn = nn.BatchNorm2d(out_channels, eps=1e-3, momentum=0.03)
        self.act = nn.SiLU(inplace=True)

    def forward(self, x: Tensor) -> Tensor:
        return self.act(self.bn(self.conv(x)))


class RoadSiLUQAT(nn.Module):
    """Hardware-LUT SiLU forward with the analytic SiLU gradient (STE)."""

    def __init__(self) -> None:
        super().__init__()
        grid = -8.0 + torch.arange(1024, dtype=torch.float32) / 64.0
        self.register_buffer("table", torch.round(F.silu(grid) * 256.0) / 256.0)
        self.register_buffer("upper", torch.tensor(round(8 / (1 + math.exp(-8)) * 256) / 256))

    def forward(self, x: Tensor) -> Tensor:
        quantized = torch.round(x * 256.0).clamp(-32768, 32767)
        address = torch.round(quantized / 4.0).to(torch.long) + 512
        approximate = self.table[address.clamp(0, 1023)]
        approximate = torch.where(address == 1024, self.upper, approximate)
        approximate = torch.where(quantized <= -2048, torch.zeros_like(approximate), approximate)
        approximate = torch.where(quantized >= 2048, quantized / 256.0, approximate)
        exact = F.silu(x)
        return exact + (approximate.to(exact.dtype) - exact).detach()


class DSDown(nn.Module):
    """Depthwise stride-two convolution followed by a pointwise projection."""

    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.dw = ConvBNAct(in_channels, in_channels, 3, 2, in_channels)
        self.pw = ConvBNAct(in_channels, out_channels)

    def forward(self, x: Tensor) -> Tensor:
        return self.pw(self.dw(x))


class LiteResidual(nn.Module):
    def __init__(self, channels: int) -> None:
        super().__init__()
        self.dw = ConvBNAct(channels, channels, 3, groups=channels)
        self.pw = ConvBNAct(channels, channels)

    def forward(self, x: Tensor) -> Tensor:
        return x + self.pw(self.dw(x))


class CSPLite(nn.Module):
    """Channel-view split, residual half branch, concatenate, then project."""

    def __init__(self, channels: int, repeats: int) -> None:
        super().__init__()
        if channels % 2:
            raise ValueError("CSPLite channels must be even")
        half = channels // 2
        self.blocks = nn.Sequential(*(LiteResidual(half) for _ in range(repeats)))
        self.out = ConvBNAct(channels, channels)

    def forward(self, x: Tensor) -> Tensor:
        bypass, branch = x.chunk(2, dim=1)
        return self.out(torch.cat((bypass, self.blocks(branch)), dim=1))


class FusionCSP(nn.Module):
    """Reduce a 2C concatenation to C and refine half with one residual block."""

    def __init__(self, channels: int) -> None:
        super().__init__()
        self.reduce = ConvBNAct(2 * channels, channels)
        self.block = LiteResidual(channels // 2)

    def forward(self, x: Tensor) -> Tensor:
        bypass, branch = self.reduce(x).chunk(2, dim=1)
        return torch.cat((bypass, self.block(branch)), dim=1)


class SPPFSqueeze(nn.Module):
    """SPPF with a frozen 96->24 squeeze and 96-channel projection."""

    def __init__(self) -> None:
        super().__init__()
        self.squeeze = ConvBNAct(96, 24)
        self.pool = nn.MaxPool2d(5, 1, 2)
        self.out = ConvBNAct(96, 96)

    def forward(self, x: Tensor) -> Tensor:
        y0 = self.squeeze(x)
        y1 = self.pool(y0)
        y2 = self.pool(y1)
        y3 = self.pool(y2)
        return self.out(torch.cat((y0, y1, y2, y3), dim=1))


class DetectionHead(nn.Module):
    """Seven-convolution head: shared stem, separate cls and reg/object paths."""

    def __init__(self, in_channels: int) -> None:
        super().__init__()
        self.stem = ConvBNAct(in_channels, 48)
        self.cls_dw = ConvBNAct(48, 48, 3, groups=48)
        self.cls_pw = ConvBNAct(48, 48)
        self.cls_out = nn.Conv2d(48, NUM_CLASSES, 1, bias=True)
        self.reg_dw = ConvBNAct(48, 48, 3, groups=48)
        self.reg_pw = ConvBNAct(48, 48)
        self.reg_out = nn.Conv2d(48, 5, 1, bias=True)

    def forward(self, x: Tensor) -> Tensor:
        x = self.stem(x)
        cls = self.cls_out(self.cls_pw(self.cls_dw(x)))
        reg_obj = self.reg_out(self.reg_pw(self.reg_dw(x)))
        return torch.cat((reg_obj, cls), dim=1)


class RoadYOLOS4(nn.Module):
    """RoadYOLO-S4-512 with outputs ordered at strides 4, 8, and 16."""

    def __init__(self) -> None:
        super().__init__()
        self.stem = ConvBNAct(3, 16, 3, 2)
        self.down2 = DSDown(16, 24)
        self.csp2 = CSPLite(24, 2)
        self.down3 = DSDown(24, 48)
        self.csp3 = CSPLite(48, 3)
        self.down4 = DSDown(48, 96)
        self.csp4 = CSPLite(96, 3)
        self.sppf = SPPFSqueeze()

        self.lateral4 = ConvBNAct(96, 48)
        self.fuse3_td = FusionCSP(48)
        self.lateral3 = ConvBNAct(48, 24)
        self.fuse2_td = FusionCSP(24)

        self.down3_bu = DSDown(24, 48)
        self.fuse3_bu = FusionCSP(48)
        self.down4_bu = DSDown(48, 96)
        self.fuse4_bu = FusionCSP(96)

        self.head2 = DetectionHead(24)
        self.head3 = DetectionHead(48)
        self.head4 = DetectionHead(96)
        self._initialize_parameters()

    def _initialize_parameters(self) -> None:
        for module in self.modules():
            if isinstance(module, nn.Conv2d):
                nn.init.kaiming_normal_(module.weight, mode="fan_out", nonlinearity="relu")
                if module.bias is not None:
                    nn.init.zeros_(module.bias)
        prior = -math.log((1.0 - 0.01) / 0.01)
        for head in (self.head2, self.head3, self.head4):
            with torch.no_grad():
                head.reg_out.bias[4] = prior
                head.cls_out.bias.fill_(prior)

    def forward(self, x: Tensor) -> list[Tensor]:
        if x.ndim != 4 or tuple(x.shape[-2:]) != (INPUT_HEIGHT, INPUT_WIDTH):
            raise ValueError(f"expected NCHW input with spatial size {INPUT_WIDTH}x{INPUT_HEIGHT}")

        x = self.stem(x)
        p2 = self.csp2(self.down2(x))
        p3 = self.csp3(self.down3(p2))
        p4 = self.sppf(self.csp4(self.down4(p3)))

        td3 = self.fuse3_td(torch.cat((
            F.interpolate(self.lateral4(p4), scale_factor=2, mode="nearest"), p3), dim=1))
        td2 = self.fuse2_td(torch.cat((
            F.interpolate(self.lateral3(td3), scale_factor=2, mode="nearest"), p2), dim=1))

        bu3 = self.fuse3_bu(torch.cat((self.down3_bu(td2), td3), dim=1))
        bu4 = self.fuse4_bu(torch.cat((self.down4_bu(bu3), p4), dim=1))
        return [self.head2(td2), self.head3(bu3), self.head4(bu4)]

    def named_convs(self) -> Iterable[tuple[str, nn.Conv2d]]:
        """Yield all 67 convolutions in stable module traversal order."""
        for name, module in self.named_modules():
            if isinstance(module, nn.Conv2d):
                yield name, module

    def capture_conv_outputs(self, x: Tensor, detach: bool = True
                             ) -> OrderedDict[str, Tensor]:
        """Run one forward pass and capture raw outputs of every named Conv2d."""
        captured: OrderedDict[str, Tensor] = OrderedDict()
        hooks = []
        for name, conv in self.named_convs():
            def save(_module: nn.Module, _inputs: tuple[Tensor, ...], output: Tensor,
                     layer_name: str = name) -> None:
                captured[layer_name] = output.detach().clone() if detach else output
            hooks.append(conv.register_forward_hook(save))
        try:
            self(x)
        finally:
            for hook in hooks:
                hook.remove()
        return captured

    def folded_conv_state(self) -> OrderedDict[str, tuple[Tensor, Tensor]]:
        """Return eval-time Conv+BN folded weights/biases without mutating the model."""
        folded: OrderedDict[str, tuple[Tensor, Tensor]] = OrderedDict()
        handled: set[int] = set()
        for block_name, block in self.named_modules():
            if not isinstance(block, ConvBNAct):
                continue
            conv, bn = block.conv, block.bn
            scale = bn.weight / torch.sqrt(bn.running_var + bn.eps)
            weight = conv.weight * scale.reshape(-1, 1, 1, 1)
            conv_bias = torch.zeros_like(bn.running_mean)
            bias = bn.bias + (conv_bias - bn.running_mean) * scale
            folded[f"{block_name}.conv"] = (weight.detach().clone(), bias.detach().clone())
            handled.add(id(conv))
        for name, conv in self.named_convs():
            if id(conv) in handled:
                continue
            bias = conv.bias
            if bias is None:
                bias = torch.zeros(conv.out_channels, device=conv.weight.device,
                                   dtype=conv.weight.dtype)
            folded[name] = (conv.weight.detach().clone(), bias.detach().clone())
        if len(folded) != EXPECTED_CONV_COUNT:
            raise RuntimeError(f"folded {len(folded)} convolutions, expected {EXPECTED_CONV_COUNT}")
        return folded

    def replace_silu(self, factory: Callable[[], nn.Module]) -> int:
        """Replace all 61 SiLUs with a supplied numerical/QAT implementation."""
        count = 0
        for module in self.modules():
            for name, child in tuple(module.named_children()):
                if isinstance(child, nn.SiLU):
                    replacement = factory()
                    if not isinstance(replacement, nn.Module):
                        raise TypeError("SiLU replacement factory must return nn.Module")
                    setattr(module, name, replacement)
                    count += 1
        if count != EXPECTED_SILU_COUNT:
            raise RuntimeError(f"replaced {count} SiLUs, expected {EXPECTED_SILU_COUNT}")
        return count

    def architecture_manifest(self) -> dict[str, object]:
        layers = []
        for name, conv in self.named_convs():
            layers.append({
                "name": name,
                "in_channels": conv.in_channels,
                "out_channels": conv.out_channels,
                "kernel": list(conv.kernel_size),
                "stride": list(conv.stride),
                "padding": list(conv.padding),
                "groups": conv.groups,
            })
        return {
            "name": "RoadYOLO-S4-512",
            "input_nchw": [None, 3, INPUT_HEIGHT, INPUT_WIDTH],
            "classes": ["person", "vehicle"],
            "output_order": ["tx", "ty", "tw", "th", "objectness", "person", "vehicle"],
            "strides": list(STRIDES),
            "layers": layers,
        }

    def architecture_hash(self) -> str:
        payload = json.dumps(self.architecture_manifest(), sort_keys=True,
                             separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()


def model_statistics(model: RoadYOLOS4, device: str | torch.device = "cpu"
                     ) -> dict[str, object]:
    """Measure the frozen contract with one shape-only forward pass."""
    model = model.to(device)
    macs = 0
    hooks = []

    def count_macs(conv: nn.Conv2d, _inputs: tuple[Tensor, ...], output: Tensor) -> None:
        nonlocal macs
        per_output = (conv.in_channels // conv.groups) * conv.kernel_size[0] * conv.kernel_size[1]
        macs += output.numel() * per_output

    for _name, conv in model.named_convs():
        hooks.append(conv.register_forward_hook(count_macs))
    was_training = model.training
    model.eval()
    try:
        with torch.no_grad():
            outputs = model(torch.zeros(1, 3, INPUT_HEIGHT, INPUT_WIDTH, device=device))
    finally:
        for hook in hooks:
            hook.remove()
        model.train(was_training)

    convs = list(model.named_convs())
    return {
        "architecture_hash": model.architecture_hash(),
        "conv_count": len(convs),
        "conv_weights": sum(conv.weight.numel() for _, conv in convs),
        "folded_biases": sum(conv.out_channels for _, conv in convs),
        "macs": macs,
        "silu_count": sum(isinstance(module, nn.SiLU) for module in model.modules()),
        "output_shapes": [list(output.shape) for output in outputs],
    }


def assert_frozen_contract(stats: dict[str, object]) -> None:
    expected = {
        "conv_count": EXPECTED_CONV_COUNT,
        "conv_weights": EXPECTED_CONV_WEIGHTS,
        "folded_biases": EXPECTED_FOLDED_BIASES,
        "macs": EXPECTED_MACS,
        "silu_count": EXPECTED_SILU_COUNT,
        "output_shapes": [[1, 7, 72, 128], [1, 7, 36, 64], [1, 7, 18, 32]],
    }
    mismatches = {key: (stats.get(key), value) for key, value in expected.items()
                  if stats.get(key) != value}
    if mismatches:
        raise AssertionError(f"RoadYOLO frozen contract mismatch: {mismatches}")


def prepare_experimental_qat(model: RoadYOLOS4) -> RoadYOLOS4:
    """Experimental partial QAT hook; not deployment-equivalent or acceptance-ready.

    It folds BN, installs exact-LUT SiLU STEs, and inserts symmetric INT8 fake
    quantization.  It deliberately does not claim residual/concatenation scale
    alignment, INT32 bias encoding, or the two integer requantization stages.
    ``train.py`` therefore fails closed for the QAT phase.
    """
    if getattr(model, "_road_qat_prepared", False):
        return model
    model.eval()
    for module in model.modules():
        if isinstance(module, ConvBNAct):
            torch.ao.quantization.fuse_modules(module, [["conv", "bn"]], inplace=True)
    model.replace_silu(RoadSiLUQAT)
    activation = torch.ao.quantization.FakeQuantize.with_args(
        observer=torch.ao.quantization.MovingAverageMinMaxObserver,
        quant_min=-128, quant_max=127, dtype=torch.qint8,
        qscheme=torch.per_tensor_symmetric, reduce_range=False)
    weight = torch.ao.quantization.FakeQuantize.with_args(
        observer=torch.ao.quantization.MovingAveragePerChannelMinMaxObserver,
        quant_min=-128, quant_max=127, dtype=torch.qint8,
        qscheme=torch.per_channel_symmetric, ch_axis=0, reduce_range=False)
    model.qconfig = torch.ao.quantization.QConfig(activation=activation, weight=weight)
    model.train()
    torch.ao.quantization.prepare_qat(model, inplace=True)
    model._road_qat_prepared = True
    return model


__all__ = [
    "INPUT_HEIGHT", "INPUT_WIDTH", "NUM_CLASSES", "OUTPUT_CHANNELS", "STRIDES",
    "RoadSiLUQAT", "RoadYOLOS4", "assert_frozen_contract", "model_statistics",
    "prepare_experimental_qat",
]
