# Source SOF/time and age reference

`reference.py` is the CPU contract before RTL. It uses only the Python standard library. Run from the project root:

```powershell
python cnn/hw_validation/production/source_sof_identity_20261015/reference/reference.py
python cnn/hw_validation/production/source_sof_identity_20261015/reference/reference.py --emit cnn/hw_validation/production/source_sof_identity_20261015/reference
```

The self-check covers post-reset SOF arming, observed AWB SOF IDs including creditless/busy/time-invalid skipped frames, same-edge old-mirror admission, complete/stalled descriptors, held time payload, ACK only on accepted descriptor, timeout at camera edge 120001, common reset, counter saturation/wrap fault, coordinated new epoch, conservative source and destination mirror lag, every glyph, numeric boundaries, frame-stable text, live draw suppression, and registered RGB/sync outputs over a complete small raster.

`vectors.json` contains 22 glyphs with all 192 pixels of each 12x16 cell, 16 ages with all 2112 pixels of each 132x16 label, frame-edge labels and live draw outputs, and 34 deterministic identity steps. `repeat` means run that edge unchanged exactly that many times and compare the final state; `inject_frame_id` is a verification-only seed to reach the wrap boundary. Results returned by camera edges are preedge admission decisions; state is postedge. `common_reset` cancels both channels. The raw time counter is an external input; no additional absolute clock exists in the model.

`age_pixels.mem` is one bit per line, age-major, then y16..31, then x16..147. `age_values.mem` has matching ages as uint64 hexadecimal. `glyph35.mem` follows the `FONT` insertion order recorded in `vectors.json`, packing row0 in bits34..30 and row6 in bits4..0. Full label pixels include the two blank trailing rows/columns in each fixed cell. `manifest.sha256` binds the reference, contract and vectors.

Model calls begin after each local reset has released. Coincident clock edges must both sample their preedge states; the compact vectors intentionally avoid simultaneous-domain calls. Two logical synchronizer stages and a destination stable-capture wait model the protocol, not metastability or physical bundled-bus timing. Configured camera60MHz is nominal and not board measured. Camera stop stops its watchdog; common reset is required for bounded freshness after clock loss. SOF is AWB reconstructed SOF, not a proven sensor-exposure/CSI-packet count. Frame/slot reservation, pixel DMA, real DDR late returns, physical CDC/MTBF, TD, production integration, bitstream, board and training are outside this reference.

CPU result: all self-check groups passed on 2026-10-15; generated full label pixels:33792. No third-party packages or production files changed.
