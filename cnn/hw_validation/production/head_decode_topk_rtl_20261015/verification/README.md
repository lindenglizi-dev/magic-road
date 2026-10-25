# Head decode / TopK RTL verification

This directory is verification-only. It consumes the saved postprocess golden vectors and never reruns CNN inference or training.

## Prepare and check vectors

From the project root:

```powershell
python cnn/hw_validation/production/head_decode_topk_rtl_20261015/verification/prepare_vectors.py
python cnn/hw_validation/production/head_decode_topk_rtl_20261015/verification/prepare_vectors.py --check
```

The first command creates only `verification/assets/`: a case index and LUT values taken from the shared integer reference. The check confirms 11 cases, 12,096 cells per case, DECODED160 counts, payload identity, and deterministic LUT files.

## Compile and run

After both DUT files exist under `../rtl/`:

```powershell
python cnn/hw_validation/production/head_decode_topk_rtl_20261015/verification/run_rtl.py --suite all
```

Useful narrower runs:

```powershell
python cnn/hw_validation/production/head_decode_topk_rtl_20261015/verification/run_rtl.py --suite regression --case real_image
python cnn/hw_validation/production/head_decode_topk_rtl_20261015/verification/run_rtl.py --suite protocol
python cnn/hw_validation/production/head_decode_topk_rtl_20261015/verification/run_rtl.py --suite reset
```

The runner uses a real local `iverilog`/`vvp`, compiles once, requires an explicit `TB_PASS` from every run, and writes logs plus `reports/summary.json`. No simulator fallback is reported as a pass.

## Governance note

The requested readable-verilog-generator workflow is applied. The companion readable-python-generator and readable-script-generator skills are not installed in this session, so no installation was attempted. The two Python files use only a mechanical vector index/export path and a standard-library process runner; this limitation is kept separate from RTL simulator evidence.

