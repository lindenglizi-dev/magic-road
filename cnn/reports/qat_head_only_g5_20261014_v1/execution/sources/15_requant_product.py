"""精确 INT32×UINT31 三乘法参考；CPU 通过不代表已经映射为三个 DSP。"""
import hashlib
import json
from pathlib import Path
import random
import re


def product(accumulator, multiplier):
    """固定分块位宽，返回待 RTL 逐级比较的全部中间量。"""
    if not -(1 << 31) <= accumulator < (1 << 31) or not 0 <= multiplier < (1 << 31):
        raise ValueError("accumulator must be INT32 and multiplier must be UINT31")
    low = accumulator & 65535
    high = accumulator >> 16
    scale_low = multiplier & 65535
    scale_high = multiplier >> 16
    sum_input = low + high
    sum_scale = scale_low + scale_high
    lower_product = low * scale_low
    upper_product = high * scale_high
    sum_product = sum_input * sum_scale
    difference = sum_product - lower_product
    cross = difference - upper_product
    partial = lower_product + (cross << 16)
    result = partial + (upper_product << 32)
    values = {"sum_input": sum_input, "sum_scale": sum_scale,
              "lower_product": lower_product, "upper_product": upper_product,
              "sum_product": sum_product, "difference": difference,
              "cross": cross, "partial": partial, "result": result}
    widths = {"sum_input": 18, "sum_scale": 18, "lower_product": 34,
              "upper_product": 32, "sum_product": 36, "difference": 36,
              "cross": 36, "partial": 64, "result": 64}
    for name, value in values.items():
        assert -(1 << (widths[name] - 1)) <= value < (1 << (widths[name] - 1)), name
    assert result == accumulator * multiplier
    return values


def main():
    accumulators = (-(1 << 31), -65536, -32768, -1, 0, 1, 32767,
                    65535, 65536, (1 << 31) - 1)
    multipliers = (0, 1, 32767, 32768, 65535, 65536, (1 << 31) - 1)
    cases = 0
    for accumulator in accumulators:
        for multiplier in multipliers:
            product(accumulator, multiplier)
            cases += 1
    rng = random.Random(42)
    for _ in range(100000):
        product(rng.randrange(-(1 << 31), 1 << 31), rng.randrange(1 << 31))
        cases += 1
    for accumulator, multiplier in ((-(1 << 31) - 1, 0), (1 << 31, 0),
                                    (0, -1), (0, 1 << 31)):
        try:
            product(accumulator, multiplier)
        except ValueError:
            continue
        raise AssertionError("invalid port value was accepted")
    report = {"cases": cases, "seed": 42, "status": "cpu_exact_product_passed",
              "multiplier_shapes": [[17, 17, 34], [16, 16, 32], [18, 18, 36]],
              "input": "INT32 accumulator, nonnegative UINT31 multiplier",
              "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "scope": "arithmetic decomposition only; no RTL, DSP mapping or timing claim",
              "rtl_requirements": ["sign or zero extend to 64 bits before left shift",
                                   "slice-only staged additions, common enable, II=1",
                                   "three DSP mapping must be measured by TD"]}
    vendor_root = Path("E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/sim_release/ph1p")
    physical = vendor_root / "ph1p_phy_dspmult_v2.v"
    header = physical.read_text(encoding="utf-8").split("`pragma protect", 1)[0]
    for direction, upper, port in (("input", 26, "x"), ("input", 17, "y"), ("output", 44, "p")):
        if not re.search(rf"{direction}\s+\[{upper}:0\]\s+{port}\b", header):
            raise ValueError("Official PH1P multiplier interface changed")
    report["vendor_model_sha256"] = {
        str(path): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in (physical, vendor_root / "ph1p_logic_mult.v")}
    root = Path(__file__).resolve().parent
    (root / "reports/requant_product_cpu.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report))


if __name__ == "__main__":
    main()
