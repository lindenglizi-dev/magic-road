# v11 Internal-Timing Physical Validation

## Result

**FAIL at 100 MHz.** The authorized product-cut repaired all seven v10 logical endpoint families, but this same single routed build exposes five new internal setup failures. The worst internal path is `-0.943 ns` from `state_current_reg[3]_syn_2.clk` to `down2_overlap_tile_runner_Inst_shell/reg_mac_weight_reg[4]_syn_2.imb`. No second seed, timing exception, bitstream, or arithmetic-core change was used.

The global worst setup is `-2.264 ns`; 15 of 20 setup failures terminate at the deliberately 0 ns diagnostic outputs. Those diagnostic paths are evidence only and are not external-interface signoff. Internal register hold is positive at `+0.054 ns`; global hold failures are diagnostic-input/raw-reset paths. Four raw-reset removal failures remain at the shell release synchronizer, while recovery has no violation and functional reset distribution is positive.

## Frozen candidate and functional evidence

- Stream SHA-256: `a51590f53c62f3a6dc51eaded0c77301b692f0cf2ae95109bd1e73afb29193fb`
- Runner SHA-256: `c2d8e603855600d6c09579f285ff8a3f62d82f8c7509634dcc66786c3ad99405`
- Runner regression: four cases, all 640 stage/writebacks, no-stall 5433 cycles.
- Standalone regression: latency 24/25 cycles, reset ages 1..25, pressure cases, and explicit full-cut payload-hold assertion PASS.

## Old seven endpoint-family mapping

| Rank | Logical endpoint family | v10 slack ns | v11 worst setup ns | Status |
| --- | --- | --- | --- | --- |
| 1 | pre_round_absolute[34] | -0.232 | +4.648 | PASS |
| 2 | pre_round_absolute[31] | -0.152 | +4.702 | PASS |
| 3 | runner_cnt_output[2] | -0.151 | +0.777 | PASS |
| 4 | pre_round_absolute[33] | -0.074 | +4.648 | PASS |
| 5 | pre_round_absolute[29] | -0.056 | +4.648 | PASS |
| 6 | mac_mult17_xa[1] | -0.044 | +3.438 | PASS |
| 7 | pre_round_absolute[35] | -0.004 | +5.271 | PASS |

The five pre-round families now launch through the registered product cut. `cnt_output[2]` and `mult17.xa[1]` are mapped from the complete 100,000-endpoint-cap all-path report, not inferred from absence in the violation report.

## New internal setup failures

| Slack ns | Begin | End |
| --- | --- | --- |
| -0.943 | state_current_reg[3]_syn_2.clk | down2_overlap_tile_runner_Inst_shell/reg_mac_weight_reg[4]_syn_2.imb |
| -0.667 | state_current_reg[3]_syn_2.clk | down2_overlap_tile_runner_Inst_shell/cnt_output_reg[0]_syn_46.ima |
| -0.255 | state_current_reg[3]_syn_2.clk | down2_overlap_tile_runner_Inst_shell/cnt_output_reg[0]_syn_36.ima |
| -0.146 | state_current_reg[3]_syn_2.clk | down2_overlap_tile_runner_Inst_shell/cnt_output_reg[0]_syn_36.imb |
| -0.081 | state_current_reg[3]_syn_2.clk | down2_overlap_tile_runner_Inst_shell/cnt_output_reg[0]_syn_41.ima |

All five launch from the shell `state_current[3]` decode and terminate in one MAC-weight storage data pin or four `cnt_output[0]` logic pins. This is a new shell scheduling/ack cone, not the repaired mask-to-fixed-round cone. The next candidate must be separately frozen and functionally proven; this baseline is sealed without further RTL changes.

## Coverage and constraints

- Complete report: 17,578 endpoints and 140,328 analyzed paths; cap 100,000 did not truncate endpoints.
- Global setup: 20 endpoints, WNS `-2.264 ns`, TNS `-24.016 ns`.
- Global min: 411 endpoints, WNS `-1.449 ns`, TNS `-330.652 ns`; 407 hold plus four removal records.
- No false path, multicycle path, ignored path, invalid constraint, or combinational loop is present.
- Clock report: one 100 MHz `probe_clk`, 6,273 clock endpoints. The 0 ns narrow-I/O constraints are diagnostic only.

## Hard blocks and memory

- 26 routed DSPs: 24 dynamic MAC DSPs plus two actual fixed-coefficient round DSPs. The latter are legal implementation cost, not a generic runtime-coefficient multiplier estimate.
- One SiLU ERAM and 145 distributed-RAM hard connections were discovered from this routed netlist.
- DSP timing: setup `+0.994 ns`, hold `+0.133 ns`; MAC-only setup `+1.784 ns`.
- DRAM timing: setup `+0.627 ns`, hold `+0.043 ns`.
- ERAM setup is `+3.454 ns`; its `-1.449 ns` hold failure is from the 0 ns diagnostic table-load input.
- Routed retained-name evidence includes metadata FIFO, result queue count, group head/tail data and masks, commit-ready control, halo, DW/PW weights and biases, DW cache, and output cache.

## Area

- 8,733 slices (41.16%): 7,509 logic and 1,224 RAM slices.
- 8,032 LUT6, 6,567 registers, 1,160 DRAM LUTs, 64 shifter LUTs.
- 1 ERAM, 26 DSPs, 38 I/O pins.

## SYN5025 / dummy-node audit

TD lists 52 unused optional `mul9_mode`/`mul9_signed` pins: 48 on the 24 MAC DSPs and four on the two fixed-round DSPs. These are disabled 9x submode controls on full-width multipliers; signed operands remain sign-extended at `xa/y`. The named-storage unused-LSLICE count is zero. Raw `check_timing` also retains one anonymous `_al_n1_syn_556.ofb` dummy output; it is not attributed to a queue, metadata, cache, or weight-storage bit.

## Evidence preservation

The initial `postroute_audit.json` and all three dynamic-export attempts remain unchanged. Corrected classification is in `postroute_audit_v2.json`; compact machine status is `physical_status.json`. `gate.db`, `pr.db`, routed netlist, all raw timing reports, failed logs, and guard receipts are retained. The frozen v10/prior guard remained unchanged before and after every guarded action.
