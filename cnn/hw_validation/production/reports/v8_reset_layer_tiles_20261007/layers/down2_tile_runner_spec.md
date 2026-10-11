# down2_tile_runner specification

## Frozen intent

`down2_tile_runner` validates exactly one 4x4 output tile of the frozen `down2` pair. It is an isolated functional candidate, not a general accelerator and not a production top-level replacement.

- Frozen graph: `down2.dw.conv`, input 144x256x16, 3x3, stride 2, pad 1, groups 16, output 72x128x16.
- Frozen graph: `down2.pw.conv`, input 72x128x16, 1x1, stride 1, output 72x128x24.
- Frozen model order: depthwise convolution -> folded bias -> SiLU -> pointwise convolution -> folded bias -> SiLU.
- Layout: row-major `tile4x4_hwc`, no channel padding.
- Halo: 9x9x16 HWC, global origin `(2*out_row-1, 2*out_col-1)`; out-of-frame elements are zero, never edge-clamped.
- Test-only quantization: pre factors `[1,3,5]`, pre shifts `[0,2,4]`, post factor `1`, post shift `4`; trained QAT parameters are not available.

## Interfaces

- Clock/reset: `i_clk`, asynchronous active-low `i_rstn`.
- SiLU table preload: ready-valid, strict addresses 0..1023. It is accepted only in idle and is blocked during run/export.
- Cache preload: ready-valid `kind/address/data`. Kinds select halo, PW-only input, DW/PW weights, and biases. Every required kind must arrive in increasing address order and complete before RUN can be accepted.
- RUN: `i_start` is accepted only in idle with a healthy complete SiLU table and complete required preload sets. `i_pw_only` selects full DW->PW or standalone PW.
- Export: a successful whole tile sets an internal valid bit. `i_export_start` then exposes 384 HWC bytes through ready-valid. A faulted or reset run cannot be exported.
- Debug: `phase=0/1/2/3` means accumulator/pre-round/SiLU/post-round INT16. Final INT8 is checked independently at export.
- Counters: MAC, pre, SiLU, post, writeback, storage preparation, and scheduler idle are mutually exclusive while busy. Their sum equals `o_core_cycles`; internal verification counters independently record the same categories for DW and PW rather than deriving one layer by subtraction.

## Datapath mapping

- DW: each scalar output uses two MAC groups, first mask `8'hff`, tail mask `8'h01`. Only output lane `channel mod 3` has real weights and bias; the other two output weight/bias lanes are zero because the frozen MAC has one common activation vector. Bias is selected only by `first`; the second group carries `last`.
- PW: each output triple shares the same eight activations. Sixteen input channels use two full-mask groups, producing three channels atomically from one MAC terminal result.
- The frozen MAC, round, and SiLU module interfaces and arithmetic are unchanged.

## Reset, fault, and visibility

- Reset cancels the controller, debug event, table-loaded metadata, output valid, and counters. Array contents are irrelevant until their corresponding preload-complete flags are rebuilt.
- Any MAC/round/table/load fault prevents whole-tile visibility. Partial internal writes are not externally readable.
- Export data/index remain stable under backpressure.

## Verification cases

1. Top-left full tile: output origin `[0,0]`, halo origin `[-1,-1]`, 272 zero-filled halo bytes and 368 zero-valued padding kernel products.
2. Interior full tile: output origin `[20,30]`, halo origin `[39,59]`.
3. Bottom-right full tile: output origin `[68,124]`, halo origin `[135,247]`; the 9x9 halo is entirely in frame.
4. Standalone PW tile with deterministic signed INT8 input.
5. In-flight reset and 20-cycle no-ghost window.
6. Directed MAC overflow proving faulted partial results cannot be exported.
7. Incomplete preload rejection and core-time SiLU-table write rejection.

## Timing diagram

The source WaveJSON is `waveforms/down2_tile_runner_full.json5`. Preload, core, and export endpoints are deliberately separate.

