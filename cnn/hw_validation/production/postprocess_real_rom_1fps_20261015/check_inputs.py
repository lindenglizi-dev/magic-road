"""Verify copied RTL and the exact G10 ROM image without running inference."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).absolute().parent
PRODUCTION = HERE.parent
ROOT = HERE.parents[3]
BASELINE = PRODUCTION / "postprocess_joint_1fps_20261015"
PACKAGE = ROOT / "cnn/reports/qat_frozen_stem_g10_20261014_v1/package"
SHARED = PRODUCTION / "shared_lut_service_1fps_20261015"
PINNED = {
    "road_candidate_ram.v": "c5d80e1ed84c89c1615ec254dabd80437ad3c0edb4abe62f087d2d17f7789eab",
    "road_head_decode_topk.v": "c1560e608dfb571b5c268908734d7b3f694fff25be7db13ca802226ed1c5df02",
    "road_nms_serial.v": "e73ff1879f34cbac59de850d4b9e4bfd72ea6d6e63046fed8c95e3b2aad1b9f1",
    "road_shared_lut_service.v": "434110b3ee9116d759704e6a998060c988910060dde011542c4c9d3fe73a51ad",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    closure = {}
    for name, expected in PINNED.items():
        original = ((SHARED if name == "road_shared_lut_service.v" else BASELINE)
                    / "rtl" / name)
        for path in (original, HERE / "rtl" / name):
            actual = sha256(path.read_bytes())
            assert actual == expected, f"frozen source changed: {path}"
            closure[str(path.relative_to(ROOT))] = actual
    payload = (PACKAGE / "numeric_test.bin").read_bytes()
    physical = (PACKAGE / "numeric_test_padded.bin").read_bytes()
    assert sha256(payload) == "b35d4a66a69e441dc29bc60c7e3f507661f48da5f33b810d7340f6ed17a65145"
    assert sha256(physical) == "bab36c254dfeb21ad21f4c600018be962f9352ddde79dcb08e64e7bd117ec417"
    assert len(payload) == 140522 and len(physical) == 143360
    assert physical[:len(payload)] == payload
    image_path = SHARED / "verification/assets/physical_words_160.hex"
    image = image_path.read_bytes()
    assert sha256(image) == "78220008aefaf3921c20517771c39e310bb7ec8d1b58d1503bd5db97c863522f"
    words = [int(line, 16) for line in image.decode("ascii").splitlines() if line.strip()]
    assert len(words) == 7168 and all(0 <= word < (1 << 160) for word in words)
    assert b"".join(word.to_bytes(20, "little") for word in words) == physical
    closure[str(image_path.relative_to(ROOT))] = sha256(image)
    for offset, count, name in ((137962, 1024, "sigmoid"), (140010, 256, "exp")):
        lut_path = (PRODUCTION / "head_decode_topk_rtl_20261015/verification/assets"
                    / f"{name}_lut_16.hex")
        expected = [int(line, 16) for line in lut_path.read_text(encoding="ascii").splitlines()]
        actual = [int.from_bytes(physical[index:index + 2], "little")
                  for index in range(offset, offset + count * 2, 2)]
        assert len(expected) == count and actual == expected, f"table mismatch: {name}"
    receipt = json.loads((BASELINE / "runs/20261015_213439_689_6337bb56/summary.json").read_text(encoding="utf-8"))
    assert receipt["status"] == "PASS_MODELSIM_POSTPROCESS_JOINT"
    assert receipt["simulations_passed"] == 22 and receipt["source_unchanged_during_run"]
    assert sha256((BASELINE / "tb_road_postprocess_joint.v").read_bytes()) == receipt["hashes"]["tb_road_postprocess_joint.v"]
    vendor_root = HERE / "vendor_rom"
    if vendor_root.exists():
        vendor_receipt = json.loads((vendor_root / "source_receipt.json").read_text(encoding="utf-8"))
        assert vendor_receipt["status"] == "PASS" and vendor_receipt["snapshot_unchanged"]
        assert vendor_receipt["payload_sha256"] == sha256(payload)
        assert vendor_receipt["physical_sha256"] == sha256(physical)
        lanes = 0
        for relative, expected in vendor_receipt["closure_sha256"].items():
            imported = vendor_root / relative
            if not imported.is_file():
                continue
            actual = sha256(imported.read_bytes())
            assert actual == expected, f"imported vendor closure changed: {relative}"
            closure[str(imported.relative_to(ROOT))] = actual
            if relative.startswith("artifacts/group_") and relative.endswith(".dath"):
                lanes += 1
        assert lanes == 56, "actual ROM needs all 56 frozen initialization lanes"
        for relative in ("rtl/road_numeric_rom_reader.v", "rtl/road_yolo_numeric_rom_group.v",
                         "vendor/ph1p_logic_eram.v", "vendor/ph1p_phy_gsr.v", "artifacts/manifest.json"):
            assert (vendor_root / relative).is_file(), f"missing actual ROM dependency: {relative}"
        print("REAL_ROM_VENDOR_BINDING_PASS lanes=56 upstream_words=7168 upstream_lut_entries=1280")
    print("REAL_ROM_INPUT_CHECK_PASS words=7168 bytes=143360 sigmoid=1024 exp=256 baseline_runs=22")
    print(json.dumps(closure, indent=2))


if __name__ == "__main__":
    main()
