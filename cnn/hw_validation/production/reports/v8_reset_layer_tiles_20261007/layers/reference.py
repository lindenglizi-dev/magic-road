"""Frozen integer reference and vectors for the down2 4x4 tile validation."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent
VECTORS = ROOT / "vectors"
PRE_FACTOR = (1, 3, 5)
PRE_SHIFT = (0, 2, 4)
POST_FACTOR = 1
POST_SHIFT = 4


def round_shift(value: int, shift: int) -> int:
    """Divide by 2**shift with nearest-even rounding and INT16 saturation."""
    magnitude = abs(value)
    quotient, remainder = divmod(magnitude, 1 << shift)
    half = 0 if shift == 0 else 1 << (shift - 1)
    if shift and (remainder > half or (remainder == half and quotient & 1)):
        quotient += 1
    result = -quotient if value < 0 else quotient
    return max(-32768, min(32767, result))


def silu_table() -> list[int]:
    return [round(((-8.0 + index / 64.0) /
                   (1.0 + math.exp(-(-8.0 + index / 64.0)))) * 256.0)
            for index in range(1024)]


SILU = silu_table()
SILU_UPPER = round(8.0 / (1.0 + math.exp(-8.0)) * 256.0)


def silu(value: int) -> int:
    address = round_shift(value, 2) + 512
    if value <= -2048:
        return 0
    if value >= 2048:
        return value
    if address == 1024:
        return SILU_UPPER
    return SILU[max(0, min(1023, address))]


def sat8(value: int) -> int:
    return max(-128, min(127, value))


def activation(input_row: int, input_col: int, channel: int) -> int:
    return ((input_row * 7 + input_col * 5 + channel * 3) % 17) - 8


def halo(output_row: int, output_col: int) -> tuple[list[int], int]:
    values = []
    padding_zeros = 0
    halo_row = 2 * output_row - 1
    halo_col = 2 * output_col - 1
    for local_row in range(9):
        for local_col in range(9):
            input_row = halo_row + local_row
            input_col = halo_col + local_col
            for channel in range(16):
                if 0 <= input_row < 144 and 0 <= input_col < 256:
                    values.append(activation(input_row, input_col, channel))
                else:
                    values.append(0)
                    padding_zeros += 1
    return values, padding_zeros


def dw_weights() -> list[int]:
    return [((channel * 5 + kernel * 3) % 7) - 3
            for channel in range(16) for kernel in range(9)]


def dw_biases() -> list[int]:
    return [(channel - 8) * 9 for channel in range(16)]


def pw_weights() -> list[int]:
    return [((output * 7 + channel * 3) % 9) - 4
            for output in range(24) for channel in range(16)]


def pw_biases() -> list[int]:
    return [(output - 12) * 11 for output in range(24)]


def pw_fixture() -> list[int]:
    return [((position * 5 + channel * 7) % 31) - 15
            for position in range(16) for channel in range(16)]


def quantize(accumulator: int, slot: int) -> tuple[int, int, int, int]:
    pre = round_shift(accumulator * PRE_FACTOR[slot], PRE_SHIFT[slot])
    activated = silu(pre)
    post = round_shift(activated * POST_FACTOR, POST_SHIFT)
    return pre, activated, post, sat8(post)


def depthwise(case_halo: list[int]) -> tuple[list[int], list[dict[str, int]]]:
    weights = dw_weights()
    biases = dw_biases()
    output = [0] * (16 * 16)
    records = []
    for position in range(16):
        out_row, out_col = divmod(position, 4)
        for channel in range(16):
            accumulator = biases[channel]
            for kernel in range(9):
                kernel_row, kernel_col = divmod(kernel, 3)
                halo_index = (((out_row * 2 + kernel_row) * 9 +
                               (out_col * 2 + kernel_col)) * 16 + channel)
                accumulator += case_halo[halo_index] * weights[channel * 9 + kernel]
            slot = channel % 3
            pre, activated, post, result = quantize(accumulator, slot)
            output[position * 16 + channel] = result
            records.append({"layer": 0, "position": position, "channel": channel,
                            "slot": slot, "acc": accumulator, "pre": pre,
                            "silu": activated, "post": post, "output": result})
    return output, records


def pointwise(input_values: list[int]) -> tuple[list[int], list[dict[str, int]]]:
    weights = pw_weights()
    biases = pw_biases()
    output = [0] * (16 * 24)
    records = []
    for position in range(16):
        for channel_out in range(24):
            accumulator = biases[channel_out]
            for channel_in in range(16):
                accumulator += (input_values[position * 16 + channel_in] *
                                weights[channel_out * 16 + channel_in])
            slot = channel_out % 3
            pre, activated, post, result = quantize(accumulator, slot)
            output[position * 24 + channel_out] = result
            records.append({"layer": 1, "position": position,
                            "channel": channel_out, "slot": slot,
                            "acc": accumulator, "pre": pre,
                            "silu": activated, "post": post, "output": result})
    return output, records


def write_hex(path: Path, values: list[int], width: int) -> None:
    mask = (1 << width) - 1
    digits = (width + 3) // 4
    path.write_text("".join(f"{value & mask:0{digits}x}\n" for value in values),
                    encoding="ascii")


def write_case(name: str, input_values: list[int], mode: str,
               padding_zeros: int = 0,
               tile_output_origin: tuple[int, int] | None = None) -> dict[str, object]:
    if mode == "full":
        dw_output, dw_records = depthwise(input_values)
        output, pw_records = pointwise(dw_output)
        records = dw_records + pw_records
        write_hex(VECTORS / f"{name}_halo.hex", input_values, 8)
        write_hex(VECTORS / f"{name}_dw_output.hex", dw_output, 8)
    else:
        dw_output = input_values
        output, records = pointwise(input_values)
        write_hex(VECTORS / f"{name}_pw_input.hex", input_values, 8)
    expected = []
    for record in records:
        expected.extend((record["acc"], record["pre"], record["silu"],
                         record["post"]))
    write_hex(VECTORS / f"{name}_stages.hex", expected, 32)
    write_hex(VECTORS / f"{name}_output.hex", output, 8)
    (VECTORS / f"{name}_records.json").write_text(
        json.dumps(records, indent=2) + "\n", encoding="utf-8")
    result = {"name": name, "mode": mode, "padding_zero_bytes": padding_zeros,
            "input_count": len(input_values), "dw_count": len(dw_output),
            "output_count": len(output), "record_count": len(records),
            "stage_value_count": len(expected),
            "non_saturated_outputs": sum(-128 < value < 127 for value in output),
            "distinct_outputs": len(set(output))}
    if tile_output_origin is not None:
        result["tile_output_origin"] = list(tile_output_origin)
        result["halo_origin"] = [2 * tile_output_origin[0] - 1,
                                 2 * tile_output_origin[1] - 1]
    return result


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    VECTORS.mkdir(exist_ok=True)
    write_hex(VECTORS / "silu.hex", SILU, 16)
    write_hex(VECTORS / "dw_weights.hex", dw_weights(), 8)
    write_hex(VECTORS / "dw_biases.hex", dw_biases(), 32)
    write_hex(VECTORS / "pw_weights.hex", pw_weights(), 8)
    write_hex(VECTORS / "pw_biases.hex", pw_biases(), 32)
    edge, edge_padding = halo(0, 0)
    interior, interior_padding = halo(20, 30)
    bottom_right, bottom_right_padding = halo(68, 124)
    cases = [
        write_case("edge_full", edge, "full", edge_padding, (0, 0)),
        write_case("interior_full", interior, "full", interior_padding, (20, 30)),
        write_case("bottom_right_full", bottom_right, "full", bottom_right_padding, (68, 124)),
        write_case("pw_standalone", pw_fixture(), "pw"),
    ]
    assert edge_padding == 272
    assert interior_padding == 0
    assert bottom_right_padding == 0
    assert all(case["non_saturated_outputs"] > 0 for case in cases)
    assert all(case["distinct_outputs"] >= 8 for case in cases)
    manifest = {
        "status": "test_parameters_not_trained_qat",
        "topology": "down2.dw.conv -> SiLU -> down2.pw.conv -> SiLU",
        "layout": "tile4x4_hwc_no_channel_padding",
        "halo": "9x9x16, origin=(2*out_row-1,2*out_col-1), OOB=0",
        "quantization": {"pre_factor": PRE_FACTOR, "pre_shift": PRE_SHIFT,
                         "post_factor": POST_FACTOR, "post_shift": POST_SHIFT,
                         "rounding": "nearest_even", "saturation": "int16_then_int8"},
        "cases": cases,
        "dw_utilization": {
            "accepted_groups": 512, "physical_mac_slots": 12288,
            "valid_kernel_products": 2304, "common_mask_open_slots": 6912,
            "zero_weight_non_target_products": 4608,
            "tail_masked_slots": 5376,
            "edge_padding_kernel_products": 368,
            "activation_lane_utilization": 0.5625,
            "physical_mac_slot_utilization": 0.1875,
        },
        "files": {},
    }
    for path in sorted(VECTORS.iterdir()):
        if path.is_file() and path.name != "manifest.json":
            manifest["files"][path.name] = sha256(path)
    (VECTORS / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"cases": cases, "manifest": str(VECTORS / "manifest.json")},
                     indent=2))


if __name__ == "__main__":
    main()
