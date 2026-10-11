"""Down2 runtime-scale contract, reusing frozen data and the integer model."""
import json
from pathlib import Path
import shutil
import sys

import numpy as np

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parents[4]))
from cnn import integer
from run_candidate import digest

VERIFY_ONLY = False


def load(path, bits):
    words = np.array([int(word, 16) for word in path.read_text().split()], dtype=np.int64)
    return np.where(words >= 1 << (bits - 1), words - (1 << bits), words)


def emit(path, values, bits):
    assert path.resolve().is_relative_to(ROOT)
    content = "".join(f"{int(value) & ((1 << bits)-1):0{bits//4}x}\n" for value in np.asarray(values).ravel())
    if VERIFY_ONLY:
        assert path.read_text(encoding="ascii") == content, path
    else:
        path.write_text(content, encoding="ascii")


def prepare(check=False):
    global VERIFY_ONLY
    VERIFY_ONLY = check
    fixture = ROOT.parent / "diagnostic_repair_20261008/layer"
    receipts = []
    for profile in ("fixed", "dynamic"):
        for family, source in (("original", fixture / "vectors"),
                               ("stress", fixture / "stress_bias_contract_host/vectors")):
            target = ROOT / "vectors" / f"{profile}_{family}"
            if not check:
                assert not target.exists(), target
                target.mkdir(parents=True)
            for name in ("silu.hex", "dw_weights.hex", "pw_weights.hex", "dw_biases.hex", "pw_biases.hex"):
                if check:
                    assert (source / name).read_bytes() == (target / name).read_bytes(), name
                else:
                    shutil.copyfile(source / name, target / name)
            if profile == "fixed":
                multipliers = np.full(40, 65536, dtype=np.int64)
                shifts = np.full(40, 24, dtype=np.int64)
                post_mul, post_shift = [16777216, 16777216], [31, 31]
            else:
                multipliers = np.array([1048583 + 7919 * channel for channel in range(40)], dtype=np.int64)
                shifts = np.array([27 + channel % 2 for channel in range(40)], dtype=np.int64)
                post_mul, post_shift = [16777191, 33554393], [31, 32]
            controls = np.concatenate((shifts, post_mul, post_shift))
            emit(target / "multipliers.hex", multipliers, 32)
            emit(target / "controls.hex", controls, 32)
            dw_weights = load(source / "dw_weights.hex", 8).astype(np.int8).reshape(16, 1, 3, 3)
            pw_weights = load(source / "pw_weights.hex", 8).astype(np.int8).reshape(24, 16, 1, 1)
            biases = (load(source / "dw_biases.hex", 32), load(source / "pw_biases.hex", 32))
            changes = []
            for case in ("edge", "interior", "bottom_right"):
                halo = load(source / f"{case}_halo.hex", 8).astype(np.int8).reshape(9, 9, 16)
                emit(target / f"{case}_halo.hex", halo, 8)
                all_acc, all_stages, all_commit = [], [], []
                image = halo
                for layer, (weights, bias, channels, stride) in enumerate(
                        ((dw_weights, biases[0], slice(0, 16), 2), (pw_weights, biases[1], slice(16, 40), 1))):
                    acc = integer.conv2d(image, weights, bias, stride=stride, groups=16 if layer == 0 else 1)
                    pre = integer.requantize(acc, multipliers[channels], shifts[channels], -32768, 32767)
                    active = integer.silu(pre)
                    commit = integer.requantize(active.astype(np.int32), post_mul[layer], post_shift[layer])
                    assert commit.shape == (4, 4, 16 if layer == 0 else 24)
                    all_acc.extend(acc.ravel())
                    all_stages.extend(np.stack((pre, active, commit), axis=-1).ravel())
                    all_commit.extend(commit.ravel())
                    image = commit.astype(np.int8)
                for suffix, values, bits in (("acc", all_acc, 32), ("stages", all_stages, 32),
                                             ("commit", all_commit, 32), ("output", image, 8)):
                    emit(target / f"{case}_{suffix}.hex", values, bits)
                    if profile == "fixed":
                        assert (target / f"{case}_{suffix}.hex").read_bytes() == (source / f"{case}_{suffix}.hex").read_bytes()
                changes.append(int(np.count_nonzero(image.ravel() != load(source / f"{case}_output.hex", 8))))
            receipts.append({"profile": profile, "family": family, "changed_output_items": changes,
                             "coefficients": "TEST_ONLY", "input": str(source)})
    if check:
        (ROOT / "reference_check.json").write_text(json.dumps({"status": "PASS", "integer_sha256": digest(Path(integer.__file__)),
                    "numpy_version": np.__version__, "receipt": receipts}, indent=2), encoding="utf-8")
    else:
        (ROOT / "reference_receipt.json").write_text(json.dumps(receipts, indent=2), encoding="utf-8")
    print("REFERENCE_PASS profiles=2 families=2 tiles=3 fixed_byte_identical=1 dynamic_changed=", receipts[2:])


if __name__ == "__main__":
    prepare(check="--check" in sys.argv)
