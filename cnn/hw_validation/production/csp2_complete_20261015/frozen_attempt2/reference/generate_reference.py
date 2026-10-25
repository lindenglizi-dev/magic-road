"""Generate the frozen-package full-frame CSP2 diagnostic golden vectors.

CPU/data only: no training, RTL, simulator, implementation, bitstream, or board use.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

os.environ["CUDA_VISIBLE_DEVICES"] = ""

import numpy as np


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[4]
PACKAGE = PROJECT / "cnn/reports/qat_frozen_stem_g10_20261014_v1/package"
VECTORS = ROOT / "vectors"
PARAMETERS = ROOT / "parameters"
WINDOWS = ROOT / "windows"
EXPECTED_PAYLOAD = "b35d4a66a69e441dc29bc60c7e3f507661f48da5f33b810d7340f6ed17a65145"
STATUS = "TRAINED_PTQ_DIAGNOSTIC_NOT_QAT_NOT_BOARD_QUALIFIED"
FRONT = ("stem.conv", "down2.dw.conv", "down2.pw.conv")
STAGES = (
    "csp2.blocks.0.dw.conv",
    "csp2.blocks.0.pw.conv",
    "csp2.blocks.1.dw.conv",
    "csp2.blocks.1.pw.conv",
    "csp2.out.conv",
)
WINDOW_ORIGINS = {
    "top_left": (0, 0),
    "top_right": (0, 124),
    "bottom_left": (68, 0),
    "bottom_right": (68, 124),
    "interior": (32, 60),
}

sys.path.insert(0, str(PROJECT))
from cnn import integer  # noqa: E402
from cnn.hw_validation.production import export_qat_front3 as front  # noqa: E402
from cnn.hw_validation.production.trained_integer import load_package  # noqa: E402


def sha256(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def emit_hex(path: Path, values: np.ndarray, bits: int) -> None:
    """One two's-complement value per line, logical HWC/OIHW flattening."""
    flat = np.asarray(values).ravel(order="C")
    mask = (1 << bits) - 1
    with path.open("w", encoding="ascii", newline="\n") as stream:
        for begin in range(0, flat.size, 8192):
            stream.writelines(
                f"{int(value) & mask:0{bits // 4}x}\n" for value in flat[begin:begin + 8192]
            )


def save_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def diagnostic_rgb() -> np.ndarray:
    """Deterministic complete RGB frame; intentionally not a road-accuracy sample."""
    yy, xx = np.indices((288, 512))
    rgb = np.empty((288, 512, 3), dtype=np.uint8)
    rgb[..., 0] = (xx % 16) * 17
    rgb[..., 1] = (yy % 16) * 17
    rgb[..., 2] = (((xx % 16) * 7) ^ ((yy % 16) * 11)) & 255
    return rgb


def scalar_stage(image: np.ndarray, params: dict[str, np.ndarray], *, stride: int,
                 padding: int, groups: int) -> tuple[np.ndarray, ...]:
    """Existing slow scalar convolution is the independent arithmetic oracle."""
    acc = integer.conv2d(image, params["weights"], params["bias"], stride, padding, groups)
    pre = integer.requantize(acc, params["pre_multiplier"], params["pre_shift"],
                             -32768, 32767).astype(np.int16)
    active = integer.silu(pre)
    post = integer.requantize(active, params["post_multiplier"],
                              params["post_shift"]).astype(np.int8)
    return acc, pre, active, post


def checked_stage(image: np.ndarray, params: dict[str, np.ndarray], lut: np.ndarray,
                  upper: int, *, stride: int, padding: int,
                  groups: int) -> tuple[np.ndarray, ...]:
    vector = front.stage(image, params, lut, upper, stride, padding, groups)
    scalar = scalar_stage(image, params, stride=stride, padding=padding, groups=groups)
    for actual, expected in zip(vector, scalar, strict=True):
        np.testing.assert_array_equal(actual, expected)
    return vector


def add_residual(bypass: np.ndarray, branch: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    total = bypass.astype(np.int16) + branch.astype(np.int16)
    return total, np.clip(total, -128, 127).astype(np.int8)


def crop_with_zero(source: np.ndarray, y0: int, x0: int, height: int, width: int) -> np.ndarray:
    result = np.zeros((height, width, source.shape[2]), dtype=source.dtype)
    sy0, sx0 = max(y0, 0), max(x0, 0)
    sy1, sx1 = min(y0 + height, source.shape[0]), min(x0 + width, source.shape[1])
    if sy0 < sy1 and sx0 < sx1:
        result[sy0 - y0:sy1 - y0, sx0 - x0:sx1 - x0] = source[sy0:sy1, sx0:sx1]
    return result


def valid_mask(y0: int, x0: int, height: int, width: int,
               full_height: int = 72, full_width: int = 128) -> np.ndarray:
    yy = np.arange(y0, y0 + height)[:, None]
    xx = np.arange(x0, x0 + width)[None, :]
    return (yy >= 0) & (yy < full_height) & (xx >= 0) & (xx < full_width)


def add_stage_views(stages: list[dict[str, np.ndarray]], arrays: tuple[np.ndarray, ...],
                    bypass: np.ndarray | None = None) -> np.ndarray:
    acc, pre, active, post = arrays
    if bypass is None:
        total, output = post.astype(np.int16), post
    else:
        total, output = add_residual(bypass, post)
    stages.append({"acc": acc, "pre": pre, "silu": active, "post": post,
                   "sum": total, "output": output})
    return output


def compare_valid(local: np.ndarray, full: np.ndarray, y0: int, x0: int) -> None:
    for y, x in np.ndindex(local.shape[:2]):
        gy, gx = y0 + y, x0 + x
        if 0 <= gy < full.shape[0] and 0 <= gx < full.shape[1]:
            np.testing.assert_array_equal(local[y, x], full[gy, gx])


def verify_window(label: str, origin: tuple[int, int], source: np.ndarray,
                  params: list[dict[str, np.ndarray]], lut: np.ndarray, upper: int,
                  full: list[dict[str, np.ndarray]]) -> dict[str, object]:
    """Independent real 8x8 -> 6x6 residual0 -> 4x4 residual1/fuse replay."""
    oy, ox = origin
    branch0, branch1 = source[..., :12], source[..., 12:]
    input8 = crop_with_zero(branch1, oy - 2, ox - 2, 8, 8)
    local: list[dict[str, np.ndarray]] = []
    out0 = add_stage_views(local, checked_stage(input8, params[0], lut, upper,
                                                 stride=1, padding=0, groups=12))
    bypass0 = input8[1:7, 1:7]
    out1 = add_stage_views(local, checked_stage(out0, params[1], lut, upper,
                                                 stride=1, padding=0, groups=1), bypass0)
    mask = valid_mask(oy - 1, ox - 1, 6, 6)
    out1 = out1.copy()
    out1[~mask] = 0
    local[1]["output"] = out1
    out2 = add_stage_views(local, checked_stage(out1, params[2], lut, upper,
                                                 stride=1, padding=0, groups=12))
    bypass1 = out1[1:5, 1:5]
    out3 = add_stage_views(local, checked_stage(out2, params[3], lut, upper,
                                                 stride=1, padding=0, groups=1), bypass1)
    passthrough = crop_with_zero(branch0, oy, ox, 4, 4)
    fused_input = np.concatenate((passthrough, out3), axis=2)
    out4 = add_stage_views(local, checked_stage(fused_input, params[4], lut, upper,
                                                 stride=1, padding=0, groups=1))

    for index in (0, 1):
        for field in ("acc", "pre", "silu", "post", "sum"):
            compare_valid(local[index][field], full[index][field], oy - 1, ox - 1)
        compare_valid(local[index]["output"], full[index]["output"], oy - 1, ox - 1)
    for index in (2, 3, 4):
        for field in ("acc", "pre", "silu", "post", "sum", "output"):
            np.testing.assert_array_equal(local[index][field], full[index][field][oy:oy + 4, ox:ox + 4])
    np.testing.assert_array_equal(out4, full[4]["output"][oy:oy + 4, ox:ox + 4])

    emitted: dict[str, dict[str, object]] = {}
    for index, fields in enumerate(local):
        for field, values in fields.items():
            bits = 32 if field == "acc" else 16 if field in ("pre", "silu", "sum") else 8
            name = f"{label}_stage{index}_{field}.hex"
            emit_hex(WINDOWS / name, values, bits)
            emitted[name] = {"shape": list(values.shape), "bits": bits}
    for name, values in ((f"{label}_input8.hex", input8),
                         (f"{label}_residual0_valid_mask.hex", mask.astype(np.uint8)),
                         (f"{label}_fuse_input.hex", fused_input)):
        emit_hex(WINDOWS / name, values, 8)
        emitted[name] = {"shape": list(values.shape), "bits": 8}
    return {"origin_yx": list(origin), "input8_shape_hwc": [8, 8, 12],
            "residual0_shape_hwc": [6, 6, 12], "residual1_shape_hwc": [4, 4, 12],
            "fuse_shape_hwc": [4, 4, 24], "files": emitted,
            "outside_residual0_zero_count": int((~mask).sum() * 12), "exact": True}


def main() -> None:
    for folder in (VECTORS, PARAMETERS, WINDOWS):
        folder.mkdir(parents=True, exist_ok=True)
    model, manifest = load_package(PACKAGE)
    if manifest["payload_sha256"] != EXPECTED_PAYLOAD or manifest["status"] != STATUS:
        raise ValueError("frozen diagnostic package identity changed")
    if front.torch.cuda.is_initialized():
        raise RuntimeError("CUDA was initialized in a CPU-only reference run")
    if [node["name"] for node in model.graph["nodes"][:12]] != [
        *FRONT, "split.00", STAGES[0], STAGES[1], "residual.00",
        STAGES[2], STAGES[3], "residual.01", "concat.00", STAGES[4],
    ]:
        raise ValueError("CSP2 graph boundary changed")

    payload = (PACKAGE / "numeric_test.bin").read_bytes()
    silu_segment = next(segment for segment in manifest["segments"] if segment["name"] == "shared.silu")
    raw_lut = payload[silu_segment["offset"]:silu_segment["offset"] + silu_segment["length"]]
    if hashlib.sha256(raw_lut).hexdigest() != silu_segment["sha256"]:
        raise ValueError("package SiLU segment hash mismatch")
    lut = np.frombuffer(raw_lut, dtype="<i2").copy()
    np.testing.assert_array_equal(lut, integer.tables()["silu"])
    emit_hex(PARAMETERS / "silu.hex", lut, 16)

    rgb = diagnostic_rgb()
    centered = (rgb.astype(np.int16) - 128).astype(np.int8)
    emit_hex(VECTORS / "input_rgb.hex", rgb, 8)
    current = centered
    front_receipt = []
    for name, node in zip(FRONT, model.graph["nodes"][:3], strict=True):
        arrays = checked_stage(current, model.parameters[name], lut, manifest["silu_upper"],
                               stride=node["stride"][0], padding=node["padding"][0],
                               groups=node["groups"])
        current = arrays[-1]
        front_receipt.append({"name": name, "shape_hwc": list(current.shape),
                              "scalar_values_checked": int(current.size), "exact": True})
    source = current
    if source.shape != (72, 128, 24):
        raise ValueError("front-three source shape changed")
    emit_hex(VECTORS / "source.hex", source, 8)

    branch0, branch1 = source[..., :12], source[..., 12:]
    stage_params = [model.parameters[name] for name in STAGES]
    full: list[dict[str, np.ndarray]] = []
    out0 = add_stage_views(full, checked_stage(branch1, stage_params[0], lut,
                                                manifest["silu_upper"], stride=1,
                                                padding=1, groups=12))
    out1 = add_stage_views(full, checked_stage(out0, stage_params[1], lut,
                                                manifest["silu_upper"], stride=1,
                                                padding=0, groups=1), branch1)
    out2 = add_stage_views(full, checked_stage(out1, stage_params[2], lut,
                                                manifest["silu_upper"], stride=1,
                                                padding=1, groups=12))
    out3 = add_stage_views(full, checked_stage(out2, stage_params[3], lut,
                                                manifest["silu_upper"], stride=1,
                                                padding=0, groups=1), out1)
    concat = np.concatenate((branch0, out3), axis=2)
    add_stage_views(full, checked_stage(concat, stage_params[4], lut,
                                        manifest["silu_upper"], stride=1,
                                        padding=0, groups=1))

    field_bits = {"acc": 32, "pre": 16, "silu": 16, "post": 8, "sum": 16, "output": 8}
    vector_files: dict[str, dict[str, object]] = {
        "input_rgb.hex": {"shape": [288, 512, 3], "bits": 8, "dtype": "uint8"},
        "source.hex": {"shape": [72, 128, 24], "bits": 8, "dtype": "int8"},
    }
    for index, fields in enumerate(full):
        for field, values in fields.items():
            name = f"stage{index}_{field}.hex"
            emit_hex(VECTORS / name, values, field_bits[field])
            vector_files[name] = {"shape": list(values.shape), "bits": field_bits[field]}

    parameter_files: dict[str, dict[str, object]] = {
        "silu.hex": {"shape": [1024], "bits": 16, "layout": "index"}
    }
    parameter_bits = {"weights": 8, "bias": 32, "pre_multiplier": 32,
                      "pre_shift": 8, "post_multiplier": 32, "post_shift": 8}
    for index, params in enumerate(stage_params):
        for field, bits in parameter_bits.items():
            name = f"stage{index}_{field}.hex"
            emit_hex(PARAMETERS / name, params[field], bits)
            parameter_files[name] = {"shape": list(params[field].shape), "bits": bits,
                                     "layout": "OIHW" if field == "weights" else "flat"}

    window_receipts = [verify_window(label, origin, source, stage_params, lut,
                                     manifest["silu_upper"], full)
                       for label, origin in WINDOW_ORIGINS.items()]

    graph_nodes = {node["name"]: node for node in model.graph["nodes"]}
    storage = {
        "source": {"tensor": "down2.pw.conv", "base_byte": graph_nodes["down2.pw.conv"]["storage"]["base"]},
        "stage0": {"tensor": STAGES[0], "base_byte": graph_nodes[STAGES[0]]["storage"]["base"]},
        "stage1": {"tensor": "residual.00", "base_byte": graph_nodes[STAGES[1]]["storage"]["base"],
                   "aliases": [STAGES[1]]},
        "stage2": {"tensor": STAGES[2], "base_byte": graph_nodes[STAGES[2]]["storage"]["base"]},
        "stage3": {"tensor": "residual.01", "base_byte": graph_nodes[STAGES[3]]["storage"]["base"],
                   "aliases": [STAGES[3]]},
        "stage4": {"tensor": STAGES[4], "semantic_alias": "csp2.fuse.conv",
                   "base_byte": graph_nodes[STAGES[4]]["storage"]["base"]},
    }
    relevant_scales = {name: model.scales[name] for name in (
        "down2.pw.conv", "split.00.0", "split.00.1", *STAGES,
        "residual.00", "residual.01", "concat.00")}
    source_paths = [Path(__file__), ROOT / "check_reference.py",
                    PROJECT / "cnn/integer.py",
                    PROJECT / "cnn/hw_validation/production/trained_integer.py",
                    PROJECT / "cnn/hw_validation/production/export_qat_front3.py",
                    PROJECT / "cnn/hw_validation/production/graph.py",
                    PROJECT / "cnn/hw_validation/production/graph_artifacts/graph.json"]
    contract = {
        "status": STATUS,
        "scope": "CPU-only deterministic numeric/TB reference; no road accuracy claim",
        "package_payload_sha256": EXPECTED_PAYLOAD,
        "source_sha256": {path.relative_to(PROJECT).as_posix(): sha256(path) for path in source_paths},
        "input_fixture": {"kind": "deterministic synthetic complete RGB diagnostic frame",
                          "shape_hwc": [288, 512, 3], "dtype": "uint8", "period_yx": [16, 16],
                          "R": "(x%16)*17", "G": "(y%16)*17",
                          "B": "(((x%16)*7)^((y%16)*11))&255",
                          "not_road_accuracy_evidence": True},
        "layout": {"activation_hex": "logical full tensor HWC row-major; channel fastest; not tile order",
                   "weights_hex": "OIHW C-order", "signed_hex": "two's complement",
                   "physical_graph_storage": "tile4x4_hwc; bases are logical byte bases only"},
        "front_three": front_receipt,
        "csp_stages": [{"index": index, "name": name,
                        "semantic": ("fuse" if index == 4 else "DW" if index in (0, 2) else "PW+residual"),
                        "shape_hwc": [72, 128, 24 if index == 4 else 12],
                        "sum": "signed16 bypass+post" if index in (1, 3) else "signed16(post)",
                        "output": "sat8(sum)" if index in (1, 3) else "post int8"}
                       for index, name in enumerate(STAGES)],
        "storage": storage,
        "scales": relevant_scales,
        "padding": {"full_frame_DW0_DW1": "one zero pixel outside the true 72x128 tensor",
                    "window_input": "8x8 branch input is zero only outside the true 72x128 tensor",
                    "residual0_for_DW1": "values whose residual0 coordinate is outside 72x128 are forced to zero; biased conv/SiLU values are never padding",
                    "target_tiles": "all 4x4 targets are real in-frame coordinates"},
        "files": {"vectors": vector_files, "parameters": parameter_files,
                  "windows": window_receipts},
        "verification": {"conv_exact_vs_integer_scalar_full_tensor": True,
                         "window_conv_exact_vs_integer_scalar": True,
                         "full_corners_and_interior_windows": True,
                         "training_updates": 0, "CUDA_initialized": False,
                         "RTL_or_simulation_or_TD_or_bitstream_or_board": False},
    }
    save_json(ROOT / "contract.json", contract)
    save_json(ROOT / "status.json", {"status": "PASS_FULL_FRAME_CSP2_REFERENCE",
        "diagnostic_marker": STATUS, "payload_sha256": EXPECTED_PAYLOAD,
        "full_shape_hwc": [72, 128, 24], "windows": list(WINDOW_ORIGINS),
        "CUDA_VISIBLE_DEVICES": os.environ["CUDA_VISIBLE_DEVICES"],
        "CUDA_initialized": front.torch.cuda.is_initialized(),
        "training_or_RTL_or_TD_or_bitstream_or_board": False,
        "asset_manifest": "manifest.json"})

    artifact_paths = sorted(path for folder in (VECTORS, PARAMETERS, WINDOWS)
                            for path in folder.iterdir() if path.is_file()) + [ROOT / "contract.json", ROOT / "status.json"]
    asset_manifest = {
        "status": STATUS,
        "package_payload_sha256": EXPECTED_PAYLOAD,
        "package_files": {path.name: sha256(path) for path in sorted(PACKAGE.iterdir()) if path.is_file()},
        "source_files": {path.relative_to(PROJECT).as_posix(): sha256(path) for path in source_paths},
        "artifacts": {path.relative_to(ROOT).as_posix(): sha256(path) for path in artifact_paths},
        "artifact_count": len(artifact_paths),
    }
    save_json(ROOT / "manifest.json", asset_manifest)
    print("PASS_FULL_FRAME_CSP2_REFERENCE")


if __name__ == "__main__":
    main()
