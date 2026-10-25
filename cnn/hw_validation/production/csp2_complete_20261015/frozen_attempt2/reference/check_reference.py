"""Small assert-only check for HWC order and image-edge residual padding."""

import numpy as np

import generate_reference as ref


def main() -> None:
    source = np.arange(4 * 5 * 2, dtype=np.int16).astype(np.int8).reshape(4, 5, 2)
    crop = ref.crop_with_zero(source, -1, 3, 4, 4)
    assert crop.shape == (4, 4, 2)
    assert not crop[0].any() and not crop[:, 2:].any()
    np.testing.assert_array_equal(crop[1:, :2], source[:3, 3:5])
    mask = ref.valid_mask(-1, 3, 4, 4, 4, 5)
    residual = np.full((4, 4, 2), 91, dtype=np.int8)
    residual[~mask] = 0
    assert not residual[~mask].any() and np.all(residual[mask] == 91)
    path = ref.ROOT / "check_hwc.tmp"
    ref.emit_hex(path, source, 8)
    assert [int(word, 16) for word in path.read_text().split()] == [int(v) & 255 for v in source.ravel()]
    path.unlink()
    print("PASS_REFERENCE_CHECK")


if __name__ == "__main__":
    main()
