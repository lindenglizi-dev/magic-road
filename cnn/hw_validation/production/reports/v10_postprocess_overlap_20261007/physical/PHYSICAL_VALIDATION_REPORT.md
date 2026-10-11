# V10 overlapping postprocess physical validation

Date: 2026-10-07  
Top: `road_postprocess_low_io_top`  
Device: PH1P35MDG324, speed grade -3  
Clock: 100 MHz (`probe_clk`, 10.000 ns)  
Disposition: **FAIL — diagnostic routed baseline only; not production signoff**

## Scope and frozen implementation

This is the first routed baseline of the real v10 implementation, not a reuse of the old low-I/O shell numbers. It contains the dynamically loaded 1296-byte halo, DW/PW feature/weight/bias/output stores, real DW/PW tile scheduler, two-deep result queue, eight-entry metadata FIFO, frozen v9 24-lane MAC, two unchanged round units, and one shared SiLU ERAM. Runtime `commit_ready` is controlled through the narrow command port and was not tied to a constant.

The routed build used these frozen hashes:

- shell: `d5ab9e5117ad390f8b9ebf3918d1a871adff9d431da79033fa728a2e10671538`
- runner: `df69af9bad06a76d5c2a72caab9dd556f6c0d21f1cbbcd2b0dab4fb5c87e108d`
- postprocess stream: `63392a96003d24ba000a3b0abaa7eafa9c5e49a921e22d2e56949326f1040650`
- v9 MAC: `04a8519e0c9e464add189ee4eb4c5ac25a6c7c716ce0ca4adf2f8fbb0fd19b51`
- round: `cb8f1e308e5832eecc9d5a0cebb86df221ea5f12abe97a5796dc49bea04b382d`
- SiLU: `5f357b493c7b3f941d9fa954a0ce5ec09091e466b641474360d2f64d0e42c938`

The later final functional regressions use the same runner and postprocess hashes. Runner four-case ModelSim passed (`vsim_attempt4.log`, SHA256 `61c35472c2d51a5aacf0dd3ea33108f8c76137f3edf06bdf96100a2e1b4a1ee8`), standalone overlap/backpressure/reset stress passed (`vsim_postprocess_attempt4.log`, SHA256 `c28bb0ab6b1092f944c7514c263a4346e675c9cce297cd6336f87d798b416af6`), and the narrow shell regression passed with 1024 table loads, 664 cache/weight/bias loads, 128 MAC results/jobs (two input groups per job, 256 groups total), 384 scalar results, 384 exports, and all 31 status words.

No bitstream, flash, board operation, or training run was performed.

## Routed utilization

| Resource | Used | Available | Utilization |
|---|---:|---:|---:|
| Slice | 8,723 | 21,216 | 41.12% |
| Slice register | 6,481 | 42,432 | 15.27% |
| LUT6 | 8,026 | 21,216 | 37.83% |
| MSlice | 3,968 | 8,112 | 48.92% |
| LSlice | 4,755 | 13,104 | 36.29% |
| PLB | 1,693 | 2,652 | 63.84% |
| Distributed-RAM LUT | 1,160 | — | — |
| Shifter LUT | 64 | — | — |
| ERAM20K | 1 | 108 | 0.93% |
| DSP | 26 | 40 | 65.00% |
| I/O | 38 | 160 | 23.75% |
| GCLK / SCLK | 1 / 4 | 32 / 48 | 3.12% / 8.33% |

Dynamic discovery found 26 DSPSIOU/DSPMULT pairs: 24 under `road_mac_probe` and 2 under the fixed pre/post round hierarchy. The two non-MAC DSPs are the legal implementation cost of the fixed round coefficients; they are not a generic runtime-coefficient multiplier estimate. One ERAM is the SiLU table. The routed netlist retains the real queue, metadata and storage names, including `reg_group_data_head`, `reg_group_data_tail`, `reg_group_mask_head`, `reg_group_mask_tail`, `cnt_result_queue`, `reg_meta_fifo`, `cnt_meta`, `reg_halo`, `reg_dw_cache`, `reg_output_cache`, DW/PW weights and biases, and `reg_commit_ready`.

The 145 DRAM hard connections map to actual consumers: 80 halo-read, 24 DW-weight, 2 DW-bias, 24 PW-weight, 6 PW-bias, 8 output-cache, and 1 metadata-FIFO source groups. These counts reflect physical banking/replication, not byte capacity. Source declarations, routed-name evidence, and functional full-address loading together establish retention of the complete dynamic stores.

## Timing coverage and violation classification

TD reports 100.00% STA coverage at both slow and fast corners, max and min checks, over 17,396 endpoints and 118,508 analyzed paths. The 100,000-endpoint cap is above the actual endpoint count. There are no timing exceptions or ignored path groups.

Global routed status:

| Check | WNS | TNS | Violating endpoints |
|---|---:|---:|---:|
| Setup | -1.892 ns | -23.676 ns | 22 |
| Min check | -1.491 ns | -80.518 ns | 233 |

The 22 setup failures are:

- 15 diagnostic-output endpoints. The worst is `cnt_export[1] -> output DRAM/mux -> o_tx_data[0]` at -1.892 ns. These paths use the explicitly diagnostic 0 ns output delay and are not external-interface signoff.
- 7 internal endpoints. Six terminate on DSP-related logic: five in `road_round_shift_Inst_pre` (worst -0.232 ns) and one at MAC `mult17.xa[1]` (-0.044 ns). The seventh is SiLU `table_fault` to runner `cnt_output` control (-0.151 ns).

The filtered register-to-register report covers 14,202 register endpoints and shows setup WNS -0.232 ns, TNS -0.669 ns, six violating endpoints, and hold WNS +0.051 ns. It must not be treated as complete coverage of mapped RAM/DSP/control endpoints; the global 17,396-endpoint report is authoritative. The worst real internal path is:

`reg_group_mask_head[1] -> mux/add -> fixed-factor DSP multiply -> road_round_shift_Inst_pre.reg_absolute[34]`

Its data delay is 10.042 ns, so the current frozen core does not meet 100 MHz internally. This failure cannot be absorbed into the diagnostic-I/O limitation.

The 233 min-check failures are exactly 229 hold paths plus 4 removal paths:

| Origin | Endpoint class | Count |
|---|---|---:|
| Diagnostic input | pre-round | 131 |
| Diagnostic input | SiLU ERAM data | 10 |
| Diagnostic input | SiLU control | 8 |
| Diagnostic input | result queue / metadata | 1 |
| Diagnostic input | runner scheduler/storage | 20 |
| Diagnostic input | shell control | 15 |
| Raw reset | pre-round hold | 44 |
| Raw reset | reset synchronizer removal | 4 |

All reported hold failures originate at unregistered external diagnostic pins or raw reset under the 0 ns boundary model. There is no internal register-to-register hold failure. TD also retained `abnormal_targets.rpt`; routing emitted PHY-5089 because 158 hold/skew paths were not automatically repaired. No exception or waiver was added.

## Reset timing

The raw-reset entry report contains 2,479 setup and 2,479 hold paths plus five recovery and five removal checks:

- setup: WNS +1.193 ns, no violation;
- hold: WNS -0.343 ns, 45 violating paths in the reset-specific report;
- recovery: WNS +8.154 ns, no violation;
- removal: WNS -0.123 ns, four of five paths violate.

The global one-path-per-endpoint report selects 44 raw-reset hold paths because one competing endpoint is represented by a worse non-reset diagnostic-input path; it still includes all four removal failures.

After the two-flop release synchronizer, functional-reset distribution passes: setup +0.409 ns, hold +0.234 ns, recovery +3.814 ns, and removal +0.072 ns. TD finds one mapped `release_meta` register and five replicated `release_done` registers after fanout optimization. Raw reset remains timed; it is not false-pathed.

## RAM and DSP timing

| Endpoint family | Setup | Hold | Recovery / removal |
|---|---|---|---|
| All 26 DSPs | 1,525 paths, WNS -0.232 ns, 6 failures | 1,525 paths, WNS +0.125 ns, 0 failures | 24 / 24 paths, +3.140 / +0.268 ns, 0 failures |
| 24 MAC DSPs | 1,488 paths, WNS -0.044 ns, 1 failure | 1,488 paths, WNS +0.125 ns, 0 failures | 24 / 24 paths, +3.140 / +0.268 ns, 0 failures |
| SiLU ERAM | 48 paths, WNS +4.174 ns, 0 failures | 48 paths, WNS -1.491 ns, 10 external-input failures | not reported for this primitive |
| Distributed RAM | 425 paths, WNS +0.488 ns, 0 failures | 425 paths, WNS +0.023 ns, 0 failures | not reported for these endpoints |

The ERAM hold failure is `i_rx_data[7] -> SiLU ERAM dia[6]` at -1.491 ns and belongs to the unregistered diagnostic load boundary. The distributed-RAM endpoints themselves pass; the global output failure merely has an output DRAM in its combinational cone.

## SYN-5025 and timing-check audit

Synthesis issued one `SYN-5025 WARNING: Using 0 for all undriven pins and nets`. The routed `check_timing` detail resolves this into two dummy-node model classes:

- 52 optional DSP 9x-submode pins: 48 `mul9_mode`/`mul9_signed` pins across the 24 MAC DSPs and 4 across the two fixed-round DSPs. The design uses the full-width multiplier path and explicitly sign-extends the active `xa`/`y` operands; the unused 9x-submode controls are zero-filled.
- one unused secondary `ofb` output on the LSLICE implementing `reg_group_data_head[81]`. This is an unused primitive output, not a missing queue bit; the complete 96-bit head and tail storage names and their consumers remain in the routed netlist.

`check_timing` reports no missing clocks, invalid constraints, combinational loops, unsupported FIFO exceptions, no-path constraints, missing/partial input or output delays, or abnormal input delays. It does report the single local diagnostic clock definition and the two dummy-node model classes above. All raw `check_timing`, ignored-path, exception, abnormal-target, RAM, DSP, ERAM, coverage and route reports are preserved.

## Conclusion

This run proves that the new real scheduler, dynamic stores, queue/metadata pipeline, 24-DSP MAC, two round units, and SiLU ERAM survive synthesis and routing with the measured resource footprint above. It does **not** pass 100 MHz physical signoff: the core has a real -0.232 ns internal setup failure, raw reset has four removal failures, and the zero-delay diagnostic boundary has many external hold/output setup failures. The broader strict static gate also remains non-passing, and the current functional performance estimate remains above the 20M-cycle target.

The highest-value next physical experiment is a separately approved, single-variable pipeline candidate around the pre-round multiply/shift/tag boundary. It must retain ports, arithmetic and initiation behavior while re-verifying added latency and obligation bounds. No such candidate was implemented in this baseline.
