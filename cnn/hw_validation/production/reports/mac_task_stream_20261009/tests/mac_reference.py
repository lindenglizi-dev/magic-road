"""Generate bounded signed33 MAC task-stream vectors before the RTL testbench.

Only generated vectors are written; frozen arithmetic and source RTL are untouched.
"""

import argparse
import json
import random
from pathlib import Path


def pack(values, width):
    return sum((value & ((1 << width) - 1)) << (index * width)
               for index, value in enumerate(values))


def make_tasks():
    rng = random.Random(20261009)
    tasks = []
    for index in range(112):
        length = (24, 1, 2, 3)[index % 4]
        bias = [rng.randrange(-2000000, 2000001) for _ in range(3)]
        groups = []
        for _ in range(length):
            activation = [rng.randrange(-128, 128) for _ in range(8)]
            weight = [[rng.randrange(-128, 128) for _ in range(8)]
                      for _ in range(3)]
            groups.append((rng.randrange(256), activation, weight))
        tasks.append((f"random_{index}", bias, groups))
    # A temporary signed32 excursion is legal; only final sums set atomic fault.
    unit = [1] + [0] * 7
    plus = [[1] + [0] * 7 for _ in range(3)]
    minus = [[-1] + [0] * 7 for _ in range(3)]
    tasks.extend([
        ("positive_recovery", [2147483647] * 3,
         [(1, unit, plus), (1, unit, minus)]),
        ("negative_recovery", [-2147483648] * 3,
         [(1, unit, minus), (1, unit, plus)]),
        ("positive_atomic_fault", [2147483647, 0, -7], [(1, unit, plus)]),
        ("after_positive_fault", [21, -22, 23], [(1, unit, minus)]),
        ("negative_atomic_fault", [0, -2147483648, 7], [(1, unit, minus)]),
        ("after_negative_fault", [-31, 32, -33], [(1, unit, plus)]),
        ("masked_zero", [-2147483648, 2147483647, 0],
         [(0, [-128] * 8, [[-128] * 8 for _ in range(3)])]),
    ])
    return tasks


def reference(tasks):
    inputs, outputs, details = [], [], []
    for name, bias, groups in tasks:
        assert 1 <= len(groups) <= 24
        accumulator = list(bias)
        trace = []
        for index, (mask, activation, weight) in enumerate(groups):
            first, last = index == 0, index == len(groups) - 1
            for lane in range(3):
                accumulator[lane] += sum(activation[j] * weight[lane][j]
                                         for j in range(8) if mask & (1 << j))
                assert -(1 << 32) <= accumulator[lane] < (1 << 32)
            trace.append(list(accumulator))
            # Non-first bias is intentionally unrelated: it must be ignored.
            bus_bias = bias if first else [index * 1234567, -index * 7654321, 99]
            word = (int(first) << 361) | (int(last) << 360) | (mask << 352)
            word |= pack(bus_bias, 32) << 256
            word |= pack([value for lane in weight for value in lane], 8) << 64
            word |= pack(activation, 8)
            inputs.append(word)
        fault = any(not -(1 << 31) <= value < (1 << 31) for value in accumulator)
        outputs.append((int(fault) << 96) | (0 if fault else pack(accumulator, 32)))
        details.append({"name": name, "groups": len(groups), "trace": trace,
                        "fault": fault, "result": [0] * 3 if fault else accumulator})
    positive = next(item for item in details if item["name"] == "positive_recovery")
    negative = next(item for item in details if item["name"] == "negative_recovery")
    assert positive["trace"][0][0] == 2147483648 and not positive["fault"]
    assert negative["trace"][0][0] == -2147483649 and not negative["fault"]
    assert sum(item["fault"] for item in details) == 2
    assert {1, 2, 3, 24} <= {item["groups"] for item in details}
    return inputs, outputs, details


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path,
                        default=Path(__file__).resolve().parent / "vectors")
    args = parser.parse_args()
    inputs, outputs, details = reference(make_tasks())
    args.out_dir.mkdir(parents=True, exist_ok=True)
    input_path = args.out_dir / "mac_inputs.hex"
    output_path = args.out_dir / "mac_expected.hex"
    input_path.write_text("".join(f"{word:091x}\n" for word in inputs), encoding="ascii")
    output_path.write_text("".join(f"{word:025x}\n" for word in outputs), encoding="ascii")
    (args.out_dir / "mac_reference.json").write_text(
        json.dumps({"groups": len(inputs), "tasks": len(outputs), "cases": details},
                   indent=2) + "\n", encoding="utf-8")
    print(f"PASS Python signed33 reference: {len(outputs)} tasks, {len(inputs)} groups")
    print(f"+N_GROUPS={len(inputs)} +N_TASKS={len(outputs)} "
          f"+INPUTS={input_path.as_posix()} +EXPECTED={output_path.as_posix()}")


if __name__ == "__main__":
    main()
