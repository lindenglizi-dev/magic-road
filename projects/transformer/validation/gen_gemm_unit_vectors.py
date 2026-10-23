#!/usr/bin/env python3
"""Generate deterministic GEMM unit inputs and an independent integer dot oracle."""
import argparse
import json
from pathlib import Path


DEPTH = 512
CASES = (
    ("single", 1, 1, 1, 0, 0),
    ("tile", 4, 4, 4, 0, 0),
    ("edge", 5, 7, 6, 0, 0),
    ("edge_transposed", 5, 7, 6, 1, 0),
    ("long_k", 5, 7, 256, 0, 0),
    ("long_k_transposed", 5, 7, 256, 1, 0),
    ("missing_a", 5, 7, 6, 0, 1),
    ("recover_a", 4, 4, 4, 1, 0),
    ("missing_b", 5, 7, 6, 1, 2),
    ("recover_b", 1, 1, 1, 0, 0),
)


def write_hex(path, values, width):
    mask = (1 << (4 * width)) - 1
    path.write_text("".join(f"{value & mask:0{width}x}\n" for value in values), encoding="ascii")


def generate(out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = [str(len(CASES))]
    summary = []
    for seed, (name, m, n, k, transposed, fault) in enumerate(CASES):
        case_dir = out_dir / name
        case_dir.mkdir(exist_ok=True)
        a = [[((row * 37 + inner * 53 + seed * 19) % 256) - 128
              for inner in range(k)] for row in range(m)]
        b = [[((inner * 61 + col * 29 + seed * 11) % 256) - 128
              for col in range(n)] for inner in range(k)]
        if k == 256:
            # Large positive/negative dots distinguish INT32 from INT16 accumulation.
            a[0] = [-128] * k
            a[1] = [127] * k
            for inner in range(k):
                b[inner][0] = -128
                b[inner][1] = 127
        if m == n == k == 1:
            a[0][0], b[0][0] = -128, 127
        expected = [sum(a[row][inner] * b[inner][col] for inner in range(k))
                    for row in range(m) for col in range(n)]
        assert all(-(1 << 31) <= value < (1 << 31) for value in expected)
        if k == 256:
            assert max(expected) == 4194304 and min(expected) == -4161536
        a_banks, b_banks = [0] * (4 * DEPTH), [0] * (4 * DEPTH)
        for row in range(m):
            for inner in range(k):
                addr = (row // 4) * k + inner
                assert addr < DEPTH
                a_banks[(row % 4) * DEPTH + addr] = a[row][inner]
        for inner in range(k):
            for col in range(n):
                addr = (col // 4) * k + inner if transposed else inner * ((n + 3) // 4) + col // 4
                assert addr < DEPTH
                b_banks[(col % 4) * DEPTH + addr] = b[inner][col]
        write_hex(case_dir / "a.hex", a_banks, 2)
        write_hex(case_dir / "b.hex", b_banks, 2)
        write_hex(case_dir / "expected.hex", expected, 8)
        manifest.append(f"{name} {m} {n} {k} {transposed} {fault}")
        summary.append({"name": name, "m": m, "n": n, "k": k,
                        "b_transposed": bool(transposed), "drop_operand": fault,
                        "numeric_required": fault == 0, "minimum": min(expected), "maximum": max(expected)})
    (out_dir / "cases.txt").write_text("\n".join(manifest) + "\n", encoding="ascii")
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"PASS GEMM_VECTORS cases={len(CASES)} numeric=8 fault=2 out={out_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, required=True)
    generate(parser.parse_args().out_dir)
