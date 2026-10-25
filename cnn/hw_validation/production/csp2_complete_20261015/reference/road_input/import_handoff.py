"""Convert the published real-image C2 prefix into the existing CSP2 TB layout.

This is a NumPy-only layout conversion.  It does not run convolution, training,
RTL, simulation, implementation, bitstream generation, or board operations.
"""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent
REFERENCE = ROOT.parent
PROJECT = ROOT.parents[5]
HANDOFF = PROJECT / "cnn/hw_validation/production/model_handoff_20261015"
PREFIX = HANDOFF / "artifacts/golden_prefix"
INDEX = HANDOFF / "artifacts/golden_prefix_index.json"
RECEIPT = HANDOFF / "artifacts/receipt.json"
VALIDATION = HANDOFF / "validation.json"
PACKAGE = PROJECT / "cnn/reports/qat_frozen_stem_g10_20261014_v1/package"
PARAMETERS = ROOT / "parameters"
VECTORS = ROOT / "vectors"
EXPECTED_IMAGE = "2aa54183d41253020bb1d51ea7a2ba93525d921cfb8948a7a65ac4f86cab7363"
EXPECTED_PAYLOAD = "b35d4a66a69e441dc29bc60c7e3f507661f48da5f33b810d7340f6ed17a65145"
EXPECTED_PARENT_MANIFEST = "6cb626491c7b72862c8ca909ba1ef22e68063b676f7b7ed6683ea808b412fb05"
MARKER = "TRAINED_PTQ_DIAGNOSTIC_NOT_QAT_NOT_BOARD_QUALIFIED"
STAGES = (
    "csp2.blocks.0.dw.conv",
    "csp2.blocks.0.pw.conv",
    "csp2.blocks.1.dw.conv",
    "csp2.blocks.1.pw.conv",
    "csp2.out.conv",
)


def sha256(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def emit_hex(path: Path, values: np.ndarray, bits: int) -> None:
    flat = np.asarray(values).ravel(order="C")
    mask = (1 << bits) - 1
    with path.open("w", encoding="ascii", newline="\n") as stream:
        for begin in range(0, flat.size, 8192):
            stream.writelines(
                f"{int(value) & mask:0{bits // 4}x}\n" for value in flat[begin:begin + 8192]
            )


def main() -> None:
    parent_manifest_path = REFERENCE / "manifest.json"
    if sha256(parent_manifest_path) != EXPECTED_PARENT_MANIFEST:
        raise ValueError("original synthetic reference manifest changed")
    original_files = [path for path in REFERENCE.rglob("*")
                      if path.is_file() and ROOT not in path.parents]
    if len(original_files) != 233:
        raise ValueError("original 233-file reference closure changed")

    index, receipt, validation = map(read_json, (INDEX, RECEIPT, VALIDATION))
    package_manifest = read_json(PACKAGE / "manifest.json")
    if (index["image_sha256"] != EXPECTED_IMAGE or index["nodes"] != list(range(12))
            or index["convolution_layers"] != 8 or index["full_network_forwards"] != 0):
        raise ValueError("published real-image prefix identity changed")
    if (receipt["status"] != "CPU_MODEL_HANDOFF_VERIFIED_NOT_DEPLOYMENT"
            or receipt["payload_sha256"] != EXPECTED_PAYLOAD
            or receipt["original_status"] != MARKER
            or validation["status"] != "PASS_CPU_HANDOFF_REGRESSION"
            or validation["full_prefix_values"] != 7151616
            or package_manifest["payload_sha256"] != EXPECTED_PAYLOAD
            or package_manifest["status"] != MARKER
            or sha256(PACKAGE / "numeric_test.bin") != EXPECTED_PAYLOAD):
        raise ValueError("C2 validation or package identity changed")
    expected_index_hash = receipt["artifact_sha256"]["golden_prefix_index.json"]
    if sha256(INDEX) != expected_index_hash:
        raise ValueError("golden prefix index differs from handoff receipt")

    tensor_index = {row["path"]: row for row in index["tensors"] if row["path"].endswith(".npy")}
    input_hashes: dict[str, str] = {}

    def load(name: str, *, indexed: bool = True) -> np.ndarray:
        path = PREFIX / name
        expected = receipt["artifact_sha256"].get("golden_prefix/" + name)
        actual = sha256(path)
        if expected is None or actual != expected:
            raise ValueError(f"published tensor hash mismatch: {name}")
        row = tensor_index.get(name)
        if indexed and row is None:
            raise ValueError(f"tensor absent from C2 index: {name}")
        array = np.load(path, allow_pickle=False)
        if row is not None and (list(array.shape) != row["shape"] or array.dtype != np.dtype(row["dtype"])):
            raise ValueError(f"tensor shape/dtype mismatch: {name}")
        input_hashes[path.relative_to(PROJECT).as_posix()] = actual
        return array

    # The handoff schema binds RGB through image metadata plus the receipt;
    # unlike node tensors, it is intentionally not repeated in tensors[].
    rgb = load("input_rgb_hwc.npy", indexed=False)
    source = load("down2.pw.conv.post.npy")
    split0, split1 = load("split.00.0.npy"), load("split.00.1.npy")
    residual0, residual1 = load("residual.00.npy"), load("residual.01.npy")
    concat = load("concat.00.npy")
    if rgb.shape != (288, 512, 3) or source.shape != (72, 128, 24):
        raise ValueError("real input/source shape changed")
    np.testing.assert_array_equal(source[..., :12], split0)
    np.testing.assert_array_equal(source[..., 12:], split1)
    np.testing.assert_array_equal(concat[..., :12], split0)
    np.testing.assert_array_equal(concat[..., 12:], residual1)

    full: list[dict[str, np.ndarray]] = []
    for index_value, layer in enumerate(STAGES):
        fields = {field: load(f"{layer}.{field}.npy")
                  for field in ("acc", "pre", "silu", "post")}
        if index_value == 1:
            total = split1.astype(np.int16) + fields["post"].astype(np.int16)
            output = residual0
            np.testing.assert_array_equal(np.clip(total, -128, 127).astype(np.int8), output)
        elif index_value == 3:
            total = residual0.astype(np.int16) + fields["post"].astype(np.int16)
            output = residual1
            np.testing.assert_array_equal(np.clip(total, -128, 127).astype(np.int8), output)
        else:
            total = fields["post"].astype(np.int16)
            output = fields["post"]
        fields.update(sum=total, output=output)
        full.append(fields)

    PARAMETERS.mkdir(parents=True, exist_ok=True)
    VECTORS.mkdir(parents=True, exist_ok=True)
    old_manifest = read_json(parent_manifest_path)
    parameter_hashes: dict[str, str] = {}
    for source_path in sorted((REFERENCE / "parameters").iterdir()):
        if not source_path.is_file():
            continue
        key = source_path.relative_to(REFERENCE).as_posix()
        expected = old_manifest["artifacts"].get(key)
        if expected is None or sha256(source_path) != expected:
            raise ValueError(f"original parameter hash mismatch: {source_path.name}")
        target = PARAMETERS / source_path.name
        shutil.copyfile(source_path, target)
        if sha256(target) != expected:
            raise ValueError(f"copied parameter hash mismatch: {target.name}")
        parameter_hashes[target.relative_to(ROOT).as_posix()] = expected
    if len(parameter_hashes) != 31:
        raise ValueError("expected the existing 31 parameter HEX files")

    vector_contract: dict[str, dict[str, object]] = {}
    for name, array, bits in (("input_rgb.hex", rgb, 8), ("source.hex", source, 8)):
        emit_hex(VECTORS / name, array, bits)
        vector_contract[name] = {"shape": list(array.shape), "bits": bits}
    bits_by_field = {"acc": 32, "pre": 16, "silu": 16,
                     "post": 8, "sum": 16, "output": 8}
    for index_value, fields in enumerate(full):
        for field, array in fields.items():
            name = f"stage{index_value}_{field}.hex"
            emit_hex(VECTORS / name, array, bits_by_field[field])
            vector_contract[name] = {"shape": list(array.shape), "bits": bits_by_field[field]}
    if len(vector_contract) != 32:
        raise ValueError("TB vector filename closure changed")

    source_files = {
        Path(__file__).relative_to(PROJECT).as_posix(): sha256(Path(__file__)),
        INDEX.relative_to(PROJECT).as_posix(): sha256(INDEX),
        RECEIPT.relative_to(PROJECT).as_posix(): sha256(RECEIPT),
        VALIDATION.relative_to(PROJECT).as_posix(): sha256(VALIDATION),
        (PACKAGE / "manifest.json").relative_to(PROJECT).as_posix(): sha256(PACKAGE / "manifest.json"),
        (PACKAGE / "numeric_test.bin").relative_to(PROJECT).as_posix(): EXPECTED_PAYLOAD,
        parent_manifest_path.relative_to(PROJECT).as_posix(): EXPECTED_PARENT_MANIFEST,
        **input_hashes,
    }
    contract = {
        "status": MARKER,
        "scope": "NumPy-only published-C2 tensor layout conversion; no convolution or accuracy claim",
        "image_sha256": EXPECTED_IMAGE,
        "payload_sha256": EXPECTED_PAYLOAD,
        "input_kind": index["input_kind"],
        "selection": index["selection"],
        "shape_hwc": {"rgb": [288, 512, 3], "source": [72, 128, 24],
                      "stage0_to_stage3": [72, 128, 12], "stage4": [72, 128, 24]},
        "layout": {"vectors": "logical HWC row-major, channel fastest, one two's-complement value per line",
                   "parameters": "byte-identical copies of ../parameters; weights remain OIHW"},
        "stages": [{"index": number, "name": name,
                    "sum": "signed16 bypass+post" if number in (1, 3) else "signed16(post)",
                    "output": "published residual tensor" if number in (1, 3) else "published post tensor"}
                   for number, name in enumerate(STAGES)],
        "checks": {"source_split_0_11_and_12_23": True,
                   "residual00_signed16_add_sat8": True,
                   "residual01_signed16_add_sat8": True,
                   "concat_channels_0_11_and_12_23": True,
                   "original_233_files_and_manifest_unchanged": True,
                   "parameter_hex_hashes_exact": True},
        "files": {"parameters": parameter_hashes, "vectors": vector_contract},
        "source_sha256": source_files,
        "not_run": ["convolution", "training", "RTL", "simulation", "TD", "bitstream", "board"],
        "acceptance_eligible": False,
    }
    save_json(ROOT / "contract.json", contract)
    save_json(ROOT / "status.json", {"status": "PASS_REAL_IMAGE_C2_LAYOUT_IMPORT",
        "diagnostic_marker": MARKER, "image_sha256": EXPECTED_IMAGE,
        "payload_sha256": EXPECTED_PAYLOAD, "vectors": len(vector_contract),
        "parameters": len(parameter_hashes), "numpy_only": True,
        "convolution_or_training_or_RTL_or_TD_or_board": False,
        "asset_manifest": "manifest.json"})

    artifacts = sorted([*PARAMETERS.iterdir(), *VECTORS.iterdir(),
                        ROOT / "contract.json", ROOT / "status.json"])
    manifest = {
        "status": MARKER,
        "image_sha256": EXPECTED_IMAGE,
        "payload_sha256": EXPECTED_PAYLOAD,
        "source_sha256": source_files,
        "artifacts": {path.relative_to(ROOT).as_posix(): sha256(path) for path in artifacts},
        "artifact_count": len(artifacts),
        "model_package_copied": False,
    }
    save_json(ROOT / "manifest.json", manifest)
    if sha256(parent_manifest_path) != EXPECTED_PARENT_MANIFEST:
        raise ValueError("original manifest changed during import")
    print("PASS_REAL_IMAGE_C2_LAYOUT_IMPORT")


if __name__ == "__main__":
    main()
