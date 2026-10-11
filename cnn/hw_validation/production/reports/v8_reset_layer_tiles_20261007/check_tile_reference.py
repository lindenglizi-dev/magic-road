"""Independent direct convolution and exact rational-rounding vector audit."""
from fractions import Fraction
import hashlib
import json
from pathlib import Path


def read_signed(path, width):
    values = [int(word, 16) for word in path.read_text(encoding="ascii").split()]
    return [value - (1 << width) if value >= (1 << (width - 1)) else value
            for value in values]


def clamp(value, lower, upper):
    return max(lower, min(upper, value))


def stages(acc, channel, table):
    lane = channel % 3
    pre = clamp(round(Fraction(acc * (1, 3, 5)[lane], 1 << (0, 2, 4)[lane])), -32768, 32767)
    addr = round(Fraction(pre, 4)) + 512
    if pre <= -2048:
        activated = 0
    elif pre >= 2048:
        activated = pre
    elif addr == 1024:
        activated = 2047  # Frozen table-boundary value, not a new approximation.
    else:
        activated = table[clamp(addr, 0, 1023)]
    post_int16 = clamp(round(Fraction(activated, 16)), -32768, 32767)
    return pre, activated, post_int16, clamp(post_int16, -128, 127)


def main():
    root = Path(__file__).resolve().parent
    vectors = root / "layers/vectors"
    manifest = json.loads((vectors / "manifest.json").read_text(encoding="utf-8"))
    for name, expected in manifest["files"].items():
        assert hashlib.sha256((vectors / name).read_bytes()).hexdigest() == expected, name
    table = read_signed(root.parent / "v7_onchip_chain_20261006/inputs/silu_table.hex", 16)
    assert table == read_signed(vectors / "silu.hex", 16)
    dw_weight = read_signed(vectors / "dw_weights.hex", 8)
    dw_bias = read_signed(vectors / "dw_biases.hex", 32)
    pw_weight = read_signed(vectors / "pw_weights.hex", 8)
    pw_bias = read_signed(vectors / "pw_biases.hex", 32)
    assert (len(dw_weight), len(dw_bias), len(pw_weight), len(pw_bias)) == (144, 16, 384, 24)
    results = []
    for case in manifest["cases"]:
        name = case["name"]
        records = json.loads((vectors / f"{name}_records.json").read_text(encoding="utf-8"))
        expected_records = []
        if case["mode"] == "full":
            halo = read_signed(vectors / f"{name}_halo.hex", 8)
            assert len(halo) == 9 * 9 * 16
            intermediate = []
            for pixel in range(16):
                row, col = divmod(pixel, 4)
                for channel in range(16):
                    acc = dw_bias[channel] + sum(
                        halo[((2 * row + ky) * 9 + 2 * col + kx) * 16 + channel]
                        * dw_weight[channel * 9 + ky * 3 + kx]
                        for ky in range(3) for kx in range(3))
                    pre, activated, post_int16, output = stages(acc, channel, table)
                    expected_records.append((0, pixel, channel, acc, pre, activated, output, post_int16))
                    intermediate.append(output)
            assert intermediate == read_signed(vectors / f"{name}_dw_output.hex", 8)
        else:
            intermediate = read_signed(vectors / f"{name}_pw_input.hex", 8)
        assert len(intermediate) == 256
        output_values = []
        for pixel in range(16):
            for channel in range(24):
                acc = pw_bias[channel] + sum(intermediate[pixel * 16 + ci]
                    * pw_weight[channel * 16 + ci] for ci in range(16))
                pre, activated, post_int16, output = stages(acc, channel, table)
                expected_records.append((1, pixel, channel, acc, pre, activated, output, post_int16))
                output_values.append(output)
        assert len(records) == len(expected_records)
        for observed, expected in zip(records, expected_records):
            fields = ("layer", "position", "channel", "acc", "pre", "silu", "post")
            assert tuple(observed[field] for field in fields) == expected[:7], (name, observed, expected)
            if "post_int16" in observed:
                assert observed["post_int16"] == expected[7]
        assert output_values == read_signed(vectors / f"{name}_output.hex", 8)
        results.append({"case": name, "stage_records": len(records), "output_items": len(output_values)})
    audit = {"status": "INDEPENDENT_TILE_REFERENCE_PASS", "cases": results,
             "method": "Direct scalar convolution; Fraction nearest-even; immutable old SiLU table; no import from new reference"}
    (root / "independent_tile_reference_audit.json").write_text(
        json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(audit))


if __name__ == "__main__":
    main()
