# ROI review bundle builder safety revision

Date: 2026-10-02

This note is separate from the frozen `roi_review_bundle_20261002_v1` directory and ZIP. The existing bundle, receipt, manifest, verification record, checksum, and ZIP were not rebuilt or overwritten.

## Change

- `build()` now refuses to run when `evaluation/ddr_architecture/roi_review_bundle_20261002_v1` already exists and directs the caller to `--verify`.
- The previous conditional `unlink()` paths for the ZIP, checksum, and verification file were removed. No file was deleted during this revision.
- `--verify` remains the read-only path for the frozen bundle.

## Hash distinction

- Script SHA-256 recorded by the frozen build receipt: `95151b032c9f433f9c28010b1045ba80c6e3133126d558334bb06ca35c35ec67`
- Revised builder script SHA-256: `d2352d82b20dc47103ad19026876bd555ee14142932e229fd9d9c746d36ad0ee`
- Frozen ZIP SHA-256: `e0f2d2c37b0cac52c4f1fd0c49c15a8f7efeeb091cc00932d1c2e3e1eac40caa`

The differing script hashes are intentional: the first identifies the code that created the frozen package; the second identifies the later overwrite-safety revision.
