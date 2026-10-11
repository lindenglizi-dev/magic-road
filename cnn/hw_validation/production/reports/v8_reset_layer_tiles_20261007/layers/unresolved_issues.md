# Unresolved issues

- Trained QAT per-layer multipliers, shifts, weights, and biases are unavailable. This run uses labeled deterministic test parameters.
- No synthesis, resource report, placement, routing, timing, board execution, bitstream, or Flash operation was performed. Resource placement is therefore unknown and is not estimated.
- The official PH1P model retains two `INIT_FILE=NONE` out-of-range part-select warnings. Functional inference is gated by a complete runtime table load.
- Local arrays model the tile and parameter caches. `storage_wait` is not a DDR measurement.
- The readable-Verilog strict gate result is recorded separately and remains a delivery blocker if any public gate is not ready.
