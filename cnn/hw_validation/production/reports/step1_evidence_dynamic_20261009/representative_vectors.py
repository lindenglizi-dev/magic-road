"""Generate actual layer-shape arithmetic fixtures; no training or deployment scales."""

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[4]
sys.path.insert(0, str(PROJECT))
from cnn import integer
from run_stage import sha, publish


def pack(items, bits):
    return sum((int(value) & ((1 << bits) - 1)) << (bits * index)
               for index, value in enumerate(items))


def main():
    graph_path = HERE.parents[1] / "graph_artifacts/graph.json"
    graph = json.loads(graph_path.read_text(encoding="utf-8"))
    assert graph["summary"]["max_pointwise_input_channels"] == 192
    definitions = [("stem", 3, 16, 3, 2, 1), ("down2_dw", 16, 16, 3, 2, 16),
                   ("down2_pw", 16, 24, 1, 1, 1), ("concat_pw", 192, 96, 1, 1, 1),
                   ("head_class", 48, 2, 1, 1, 1), ("head_reg_obj", 48, 5, 1, 1, 1)]
    rng = np.random.default_rng(42)
    rows = []
    coverage = []
    tag = 0
    for case, cin, cout, kernel, stride, groups in definitions:
        size = 8 if kernel == 3 else 4
        padding = 1 if kernel == 3 else 0
        image = rng.integers(-32, 32, (size, size, cin), dtype=np.int8)
        weights = rng.integers(-16, 16, (cout, cin // groups, kernel, kernel), dtype=np.int8)
        biases = rng.integers(-1000, 1001, cout, dtype=np.int32)
        accumulators = integer.conv2d(image, weights, biases, stride, padding, groups)
        assert accumulators.shape == (4, 4, cout)
        # Non-power-of-two runtime coefficients prevent the fixed-test shortcut.
        multipliers = np.array([1048583 + 7919 * channel for channel in range(cout)], dtype=np.int64)
        shifts = np.array([21 + channel % 2 for channel in range(cout)], dtype=np.int64)
        activated = not case.startswith("head_")
        post_mul, post_shift = 16777191, 32
        pre = integer.requantize(accumulators, multipliers, shifts, -32768, 32767)
        expected = (integer.requantize(integer.silu(pre).astype(np.int32), post_mul, post_shift)
                    if activated else pre)
        padded = np.pad(image, ((padding, padding), (padding, padding), (0, 0)))
        tasks = 0
        group_count = 0
        for y in range(4):
            for x in range(4):
                # DW remains a single-output reference task; spatial packing is already
                # covered by the frozen 14-case layer regression, not redesigned here.
                for base in range(0, cout, 1 if groups > 1 else 3):
                    channels = list(range(base, min(base + (1 if groups > 1 else 3), cout)))
                    start = base if groups > 1 else 0
                    patch = padded[y * stride:y * stride + kernel,
                                   x * stride:x * stride + kernel, start:start + cin // groups].ravel()
                    kernels = [weights[channel].transpose(1, 2, 0).ravel() for channel in channels]
                    groups_needed = (len(patch) + 7) // 8
                    assert 1 <= groups_needed <= 24
                    mac_expected = [int(accumulators[y, x, channel]) for channel in channels]
                    output_expected = [int(expected[y, x, channel]) for channel in channels]
                    pre_mul = [int(multipliers[channel]) for channel in channels]
                    pre_shift = [int(shifts[channel]) for channel in channels]
                    tags = list(range(tag, tag + len(channels)))
                    tag += len(channels)
                    pad3 = lambda values: values + [0] * (3 - len(values))
                    rows.append(" ".join(f"{value:x}" for value in
                        (groups_needed, pack(pad3(mac_expected), 32), pack(pad3(output_expected), 16),
                         pack(pad3(pre_mul), 32), pack(pad3(pre_shift), 6), post_mul, post_shift,
                         int(activated), (1 << len(channels)) - 1, pack(pad3(tags), 16))))
                    reconstructed = [int(biases[channel]) for channel in channels]
                    for group in range(groups_needed):
                        offset = group * 8
                        acts = list(map(int, patch[offset:offset + 8]))
                        lane_weights = [list(map(int, lane[offset:offset + 8])) for lane in kernels]
                        for lane in range(len(channels)):
                            reconstructed[lane] += sum(a * b for a, b in zip(acts, lane_weights[lane]))
                        acts += [0] * (8 - len(acts))
                        ws = [pack(lane + [0] * (8 - len(lane)), 8) for lane in lane_weights]
                        rows.append(" ".join(f"{value:x}" for value in
                            (pack(acts, 8), pack(pad3(ws), 64),
                             (1 << min(8, len(patch) - offset)) - 1,
                             pack(pad3([int(biases[channel]) for channel in channels]), 32))))
                    assert reconstructed == mac_expected
                    tasks += 1
                    group_count += groups_needed
        coverage.append({"case": case, "cin": cin, "cout": cout, "kernel": kernel,
                         "stride": stride, "groups": groups, "padding": padding,
                         "tasks": tasks, "input_groups": group_count, "outputs": 16 * cout,
                         "activate": activated, "boundary": "serial operator-chain test, not tile/DMA throughput"})
    (HERE / "representative.txt").write_text("\n".join(rows) + "\n", encoding="ascii")
    manifest = {"seed": 42, "tasks": sum(item["tasks"] for item in coverage), "outputs": tag,
                "cases": coverage, "vector_sha256": sha(HERE / "representative.txt"),
                "graph_sha256": sha(graph_path), "parameter_origin": "deterministic tests, NOT QAT",
                "numeric_source_sha256": sha(PROJECT / "cnn/integer.py")}
    publish("representative_manifest.json", manifest)
    print("REPRESENTATIVE_REFERENCE_PASS", manifest["tasks"], tag)


if __name__ == "__main__":
    main()
