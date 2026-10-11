"""最小1x1计算链逐级黄金向量；契约冲突未决，不作为已部署模型。"""
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parent
MAC = ROOT / "inputs"
sys.path.insert(0, str(MAC))
from mac_reference import Beat, MacReference, intermediate_banks, _write_vector


def signed(value, bits):
    if not -(1 << (bits - 1)) <= value < (1 << (bits - 1)):
        raise OverflowError(f"signed{bits}: {value}")
    return value


def hex_signed(path):
    values = [int(word, 16) for word in path.read_text().split()]
    assert all(0 <= value <= 65535 for value in values)
    return [value - 65536 if value >= 32768 else value for value in values]


def round_even(value, shift):
    signed(value, 64)
    if value == -(1 << 63) or not 0 <= shift <= 62:
        raise ValueError("非法 round 输入，必须fault，不返回数值")
    return round(Fraction(value, 1 << shift))


def quant(value, multiplier, shift, bits):
    signed(value, 32)
    if not 0 <= multiplier < (1 << 31):
        raise ValueError("非负INT32乘数范围错误")
    product = signed(value * multiplier, 64)
    rounded = round_even(product, shift)
    saturated = max(-(1 << (bits - 1)), min((1 << (bits - 1)) - 1, rounded))
    return product, rounded, saturated


def activate(value, table):
    signed(value, 16)
    address = round_even(value, 2) + 512
    if value <= -2048:
        return address, 0
    if value >= 2048:
        return address, value
    return address, 2047 if address == 1024 else table[address]


def tensor_case(channels, params, table):
    rng = random.Random(params["seed"])
    image = [[rng.randrange(-32, 33) for _ in range(channels)] for _ in range(4)]
    image[0][0:4] = [-128, 127, 0, -1]
    weights = [[rng.randrange(-16, 17) for _ in range(channels)] for _ in range(3)]
    bias = [-517, 129, 103]
    records, groups = [], []
    for position, pixels in enumerate(image):
        acc = list(bias)
        legacy = MacReference()
        for group, start in enumerate(range(0, channels, 8)):
            valid = min(8, channels - start)
            # 无效lane故意填非零极值，防止尾mask遗漏被全零填充掩盖。
            a = tuple(pixels[start:start + valid] + [127] * (8 - valid))
            w = tuple(tuple(row[start:start + valid] + [-128] * (8 - valid)) for row in weights)
            beat = Beat(group == 0, start + 8 >= channels, (1 << valid) - 1, a, w, tuple(bias))
            banks = intermediate_banks(beat)
            acc = [signed(acc[o] + banks.dots[o], 33) for o in range(3)]
            legacy_result = legacy.apply(beat)
            if beat.last:
                assert not legacy_result.fault and list(legacy_result.values) == acc
            else:
                assert legacy_result is None
            groups.append({"position": position, "group": group, "first": beat.first,
                           "last": beat.last, "mask": beat.mask, "activations": a,
                           "weights": w, "bias": bias, "products": banks.products,
                           "pairs": banks.pairs, "quads": banks.quads,
                           "dot": banks.dots, "accumulator": list(acc)})
        for o in range(3):
            expected = bias[o] + sum(pixels[i] * weights[o][i] for i in range(channels))
            assert acc[o] == expected
        fault = any(not -(1 << 31) <= value < (1 << 31) for value in acc)
        assert not fault
        for output, value in enumerate(acc):
            product, rounded, q = quant(value, params["pre_multiplier_per_output"][output],
                                        params["pre_shift_per_output"][output], 16)
            address, silu = activate(q, table)
            post_product, post_round, feature = quant(silu, params["post_multiplier"], params["post_shift"], 8)
            records.append({"position": position, "output_channel": output,
                            "write_address": position * 3 + output, "accumulator": value,
                            "pre_product": product, "pre_rounded": rounded, "silu_input": q,
                            "silu_address": address, "silu_output": silu,
                            "post_product": post_product, "post_rounded": post_round,
                            "feature_int8": feature})
    assert len(records) == 12 and len(groups) == 8
    return {"channels": channels, "effective_mac": 4 * channels * 3,
            "scheduled_multiplier_lanes": len(groups) * 24,
            "inputs": image, "weights": weights, "bias": bias,
            "groups": groups, "outputs": records}


def write_mac_vectors(case):
    reference = MacReference()
    with (ROOT / f"mac_{case['channels']}_channels.txt").open("w", encoding="ascii") as stream:
        for group in case["groups"]:
            beat = Beat(group["first"], group["last"], group["mask"],
                        tuple(group["activations"]), tuple(tuple(w) for w in group["weights"]),
                        tuple(group["bias"]))
            _write_vector(stream, beat, reference.apply(beat))


def contract_counterexample():
    bias = ((1 << 31) - 5, 0, 0)
    a = (1,) * 8
    positive = Beat(True, False, 255, a, ((1,) * 8, (0,) * 8, (0,) * 8), bias)
    negative = Beat(False, True, 255, a, ((-1,) * 8, (0,) * 8, (0,) * 8), bias)
    legacy = MacReference()
    first = legacy.apply(positive)
    assert first.fault and first.values == (0, 0, 0)
    with (ROOT / "counterexample_legacy.txt").open("w", encoding="ascii") as stream:
        _write_vector(stream, positive, first)
    first_dot = intermediate_banks(positive).dots[0]
    second_dot = intermediate_banks(negative).dots[0]
    partial = bias[0] + first_dot
    final = partial + second_dot
    signed(partial, 33)
    signed(final, 32)
    return {"bias": bias, "first_dot": [first_dot, 0, 0], "second_dot": [second_dot, 0, 0],
            "first_partial": [partial, 0, 0], "final": [final, 0, 0],
            "legacy_first_group_fault": True, "legacy_fault_payload": first.values,
            "deployment_final_fault": False, "status": "REPRODUCED_CONTRACT_CONFLICT"}


def self_check(table, golden):
    assert len(table) == 1024 and len(golden) == 65536
    assert [activate(value, table)[1] for value in range(-32768, 32768)] == golden
    assert [round_even(v, 1) for v in [-5, -3, -1, 1, 3, 5]] == [-2, -2, 0, 0, 2, 2]
    assert quant(100000, 1, 0, 16)[2] == 32767
    assert quant(-100000, 1, 0, 16)[2] == -32768
    assert quant(100000, 1, 0, 8)[2] == 127
    assert quant(-100000, 1, 0, 8)[2] == -128
    for v, m, shift in [(0, -1, 0), (0, 1 << 31, 0), (1 << 31, 1, 0), (0, 1, 63)]:
        try:
            quant(v, m, shift, 16)
        except (ValueError, OverflowError):
            continue
        raise AssertionError("非法参数被接受")
    for value in [-2048, -2047, 0, 2046, 2047, 2048, -32768, 32767]:
        activate(value, table)
    assert activate(2046, table) == (1024, 2047)
    return {"full_domain_frozen_table_checks": 65536, "round_ties": 6,
            "saturation_boundary_checks": 4, "invalid_parameter_rejections": 4,
            "scope": "Python reference only, no RTL or protocol timing proof"}


if __name__ == "__main__":
    params = json.loads((ROOT / "test_parameters.json").read_text())
    if any(params["zero_points"].values()):
        raise ValueError("仅支持对称量化zero-point=0，不能忽略非零修正")
    for weight_scale, multiplier, shift in zip(params["weight_scale_per_output"],
                                              params["pre_multiplier_per_output"],
                                              params["pre_shift_per_output"]):
        assert Fraction(multiplier, 1 << shift) == Fraction(params["input_scale"]) * Fraction(weight_scale) / Fraction(params["silu_scale"])
    assert Fraction(params["post_multiplier"], 1 << params["post_shift"]) == Fraction(params["silu_scale"]) / Fraction(params["output_scale"])
    table_path = ROOT / "inputs" / "silu_table.hex"
    golden_path = ROOT / "inputs" / "silu_expected.hex"
    assert hashlib.sha256(table_path.read_bytes()).hexdigest() == "05d6d7062a6b6d0c9178562168d7f8e1554182bb99878b85a0cb6faeb71a25a6"
    assert hashlib.sha256(golden_path.read_bytes()).hexdigest() == "4f6552528d4035f14203e9aafbf8142ad3de8cd5867a0cfdfdcacb5131b908e2"
    table, golden = hex_signed(table_path), hex_signed(golden_path)
    checks = self_check(table, golden)
    counterexample = contract_counterexample()
    result = {"purpose": params["purpose"], "checks": checks,
              "cases": [tensor_case(16, params, table), tensor_case(13, params, table)],
              "contract_counterexample": counterexample,
              "rtl_chain_status": "BLOCKED_CONTRACT_CONFLICT"}
    (ROOT / "stage_vectors.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    for case in result["cases"]:
        write_mac_vectors(case)
    frozen = sorted(path for path in (ROOT / "inputs").iterdir() if path.is_file())
    frozen.extend([ROOT / "test_parameters.json", Path(__file__).resolve()])
    tool_paths = [Path("E:/project/qiansai/.tools/road_yolo_venv/Scripts/python.exe"),
                  Path("E:/project/qiansai/.tools/iverilog/bin/iverilog.exe"),
                  Path("E:/project/qiansai/.tools/iverilog/bin/vvp.exe")]
    manifest = {"date": "2026-10-06 Asia/Shanghai", "status": "diagnostic only, conflict pending",
                "inputs": [{"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
                           for path in frozen],
                "tools": [{"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
                          for path in tool_paths]}
    (ROOT / "baseline_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"checks": checks, "base_mac": 192, "tail_mac": 156,
                      "outputs_per_case": 12, "counterexample": counterexample}))
