# Storage/resource review summary

Date: 2026-10-10. Role: `review`. Scope: first-batch section 9 only. No old file, RTL, main `run.py`, package, simulation, TD project, training state, bitstream, board, or Flash was changed.

## Verified

- The two saved routed shells are separate source closures, not one interchangeable baseline: `down2_dynamic_tile_runner.v` and `road_mac_probe.v` hashes differ; the other six RTL files match.
- The complete distributed-memory allocation reconciles exactly to the reports: 2,016 DRAM LUTs for `control_operand_hold_20261009`, 2,040 for `scheduler_predecode_20261010`. The +24 difference is entirely at the DW-weight read site (328 to 352 DRAM LUTs); this statement is limited to mapped memory, not all logic-resource causes.
- Both shells use one ERAM20K for the 1024x20 SiLU table. Halo, weights/biases, DW intermediate output, final output, runtime quant parameters, and metadata/result queues are separately itemized in `memory_resource_breakdown.json`, including source capacity, mapped LUT/ERAM, port shape, read-latency boundary, and collision rule.
- The low-I/O diagnostic/control shell is separated by hierarchy subtraction. The published total Slice counts still include it: 7,994 and 7,983. Hierarchy columns cannot be converted into an exact shell Slice count.
- The routed video template remains 12,358 Slice / 8 DSP / 40 ERAM. Simple addition leaves 864 Slice with the control-hold shell or 875 Slice with the scheduler-predecode shell, and 2 DSP in both cases. These are arithmetic headrooms only, not merged placement/routing evidence.
- Existing schema1 and schema2 TEST packages both pass read-only integrity checks: payload/padded hashes, padded CRC32, 393 contiguous field offsets/lengths/counts, segment hashes, layer field offsets, 7,168 word lines, and all 56 lane-file hashes/512-line reconstructions.
- Schema1 and schema2 share the 14x512x160 physical geometry and the same offset/length/count layout, but are not interchangeable. The first payload byte difference is offset 432; payload SHA256 and padded CRC32 differ, and per-channel/per-SiLU field meanings changed. Both packages are TEST fixtures, not E7/QAT deployment weights.
- The current DDR source hashes still match the prior receipt. The source proves a 25-bit/128-bit PAXI boundary, permanently asserted RREADY, missing user-visible RLAST, an undriven `O_mc_app_rd_data_end`, and failure to expose real WREADY upstream.

## Still unproven / blocking

- No shell report contains the 56-ERAM schema2 parameter ROM, full network, real DDR loop, or video-template merge.
- Existing RAM evidence does not prove vendor collision behavior beyond the source scheduling assumptions, nor does it prove a new ERAM mapping or its latency.
- ROM integrity does not prove ROM RTL address adaptation, vendor initialization, synthesis mapping, or runtime readback.
- All five production DDR questions remain blocked: byte-address conversion, AW/W timing, write visibility, no-RREADY return capacity/termination, and reset late return. H1-B is mock-only, `integration_release=false`, and its strict gate remains failed.
- No new RTL gate was run. Public gate state for this review is: compile/ast/readability/comment/naming/profile `not_run_in_this_review`; testbench/toolchain `not_requested`.

## Recommended next action

1. Keep the current parameter geometry but bind only schema2 field semantics when a separately authorized ROM-read path is implemented; do not reuse schema1 names or CRC.
2. If one cache is tested for ERAM migration, start with `reg_output_cache[0:383]`: its write and one-byte export-read phases are mutually exclusive. Treat the possible one-ERAM-for-64-DRAM-LUT trade as a candidate until synchronous read latency, 384-byte export behavior, synthesis resource change, and timing are measured.
3. Do not first migrate halo, weights, DW cache, or runtime parameters to one single-port ERAM; their current cycle requires parallel reads and would need banking or a schedule/interface change.
4. Before M4, obtain build-matched controller evidence answering every item in `paxi_evidence_questions.md`. Do not use `byte_addr >> 1`, fixed-N waits, mock `i_commit_confirmed`, or timeout owner release as production guarantees.

Decision: storage/package evidence is sufficient to continue planning M2, but ROM and DDR are not released; no resource result here establishes that the full design fits.
