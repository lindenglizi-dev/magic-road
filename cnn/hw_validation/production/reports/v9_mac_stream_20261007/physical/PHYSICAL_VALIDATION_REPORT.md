# V9 MAC stream isolated physical validation

Status: **DIAGNOSTIC_COMPLETE_SIGNOFF_FAIL**. Tang Dynasty 6.2.168116 completed synthesis, placement, routing, and routed STA for `road_low_io_reset_shell` on PH1P35MDG324 speed grade -3 at 100 MHz. Setup passes, but minimum-delay and raw-reset removal do not. No timing exception, protocol change, numerical change, bit generation, board action, or Flash action was used.

## Scope and frozen inputs

This is a 38-bit low-I/O diagnostic shell containing the frozen v9 MAC, unchanged round/SiLU/on-chip chain and feature cache, and unchanged v8 reset wrapper. It is not a physical implementation of `down2_tile_runner`; the layer runner currently has real-shape functional cycle evidence only.

The TD log records the actual read order as reset shell, old physical shell, on-chip chain, v9 `road_mac_probe.v`, round, and SiLU. All six actual RTL hashes still match `prebuild_manifest.json`. In particular, the approved MAC hash is `04a8519e0c9e464add189ee4eb4c5ac25a6c7c716ce0ca4adf2f8fbb0fd19b51`. `shell.sdc` remains byte-identical to v8 (`0acbd5f...d5e`): 0 ns max/min I/O delays and no exceptions. `build.tcl` also retains its frozen hash (`8043de12...971e`). TD updated its `.al` project metadata during the run; this is not an RTL/SDC change.

The verification collector files continued to append after the build gate, as allowed. Their latest hashes are recorded separately in the receipt and were not treated as source drift.

## Routed result

| Item | V9 | V8 reference | Delta |
|---|---:|---:|---:|
| Slice | 3831 | 4066 | -235 (-5.78%) |
| Slice registers | 3353 | 3783 | -430 |
| DSP | 26 | 26 | 0 |
| ERAM | 1 | 1 | 0 |
| DRAM hard controllers | 93 | 93 | 0 |
| I/O | 38 | 38 | 0 |

The design uses one GCLK and four SCLKs. All 38 ports lack user pin locations; TD assigned temporary random locations and states that bit generation would abort. No bitstream was requested or created.

## STA and the failing boundary

Routed STA coverage is 100.00%, with slow/fast max/min all enabled and process records for `slow_m40c`, `slow_125c`, `fast_m40c`, and `fast_125c`.

| Group | Setup WNS | Hold/min WNS | Violations |
|---|---:|---:|---:|
| Global | +0.059 ns | -0.696 ns | 0 setup, 41 minimum |
| Internal reg-to-reg | +1.505 ns | +0.048 ns | 0 |
| Diagnostic inputs to registers | +2.375 ns | -0.696 ns | 38 hold |
| Registers to diagnostic outputs | +0.059 ns | +2.642 ns | 0 |
| MAC internal reg-to-reg | +2.833 ns | +0.048 ns | 0 |
| MAC A5 accumulator feedback | +4.478 ns | +0.135 ns | 0 |

The 41 negative minimum paths are exactly 38 hold plus 3 removal. The 38 holds are external diagnostic-input paths: 35 end in shell registers and 3 end in MAC registers. The three MAC endpoints are `i_rx_data[2] -> reg_bias_front[15]` (-0.320 ns), `i_rx_data[11] -> reg_final_data_stage3[73]` (-0.157 ns), and `i_rx_data[1] -> reg_final_data_stage0[39]` (-0.026 ns). They are not internal MAC reg-to-reg paths. Therefore the positive +0.048 ns MAC-internal hold result does not mean all MAC boundaries pass. The global worst hold is `i_rx_data[2] -> reg_table_pending_data[2]` at -0.696 ns.

Violation processes are 30 hold at `slow_m40c`, 8 hold at `fast_125c`, 1 removal at `slow_m40c`, and 2 removal at `fast_125c`. Relative to v8, diagnostic hold violations increase from 31 to 38 (+7); reset removal remains 3. Global min WNS improves from -0.950 to -0.696 ns, while setup WNS changes from +0.090 to +0.059 ns.

### MAC-specific paths

The MAC-only report is selected from 1567 current routed register objects, not old synthesized instance names. Its worst setup path is +2.833 ns from the registered `dot_gamma_wide[0]` source through the accumulator/final-data adder cone to `reg_final_data_stage0[81]`; its worst hold is +0.048 ns from `reg_final_data_stage0[66]` to `reg_final_data_stage1[69]`.

The A5 accumulator-feedback collection contains 99 current accumulator register objects and 1001 max/min endpoints. Worst setup is +4.478 ns from `reg_accumulator_alpha[0]`, through the `road_mac_probe.v:208` adder chain, to `reg_accumulator_gamma[15]`. Worst hold is +0.135 ns from `reg_accumulator_beta[13]`, through the line-209 adder chain, to `reg_accumulator_beta[16]`. Dot-to-accumulator is +3.567/+0.211 ns, bias-to-MAC is +3.488/+0.054 ns, and valid-control-to-MAC is +4.898/+0.057 ns.

The source `reg_candidate_*` registers are absent after synthesis, so the first dynamic export correctly failed on that empty collection. No old candidate instance name was substituted. The retained accumulator feedback and dot-to-accumulator paths are the reliable A5 physical evidence.

## Reset audit

Raw reset enters four physical release registers. Recovery WNS is +7.848 ns. Removal WNS is -0.264 ns, with failures on `reg_release_done_reg_syn_4` (-0.018 ns), `_syn_5` (-0.264 ns), and `_syn_6` (-0.002 ns); `_syn_3` is +0.195 ns. Raw-reset physical fanout is 9.

The stage-1 to three stage-2 physical interstage paths pass at +8.290 ns setup and +0.190 ns hold. Functional reset distribution passes at +4.084 ns setup, +0.190 ns hold, +5.027 ns recovery, and +0.067 ns removal; the observed maximum physical fanout is 1887. This confirms the unchanged staged architecture, but the three raw-entry removal failures keep reset signoff false.

## Routed structure and hard-block endpoints

Dynamic parsing of this run's routed netlist found 26 `DSPSIOU` plus 26 `DSPMULT` primitives, of which 24 are the MAC multipliers. It proves dynamic use of all 64 activation bits and 192 weight bits, retention of all 96 bias bits, and all three signed 33-bit accumulators (99 bits total). Retained valid/control signals include front, quad, dot, four final-valid stages, result-valid, candidate-fault, first/last controls, and ready.

The source names `flag_product_valid`, `flag_pair_valid`, and `flag_candidate_valid`, and the three `reg_candidate_*` names, are absorbed by synthesis. This is recorded as netlist transformation rather than presented as an interface failure.

The one ERAM is the SiLU table. The feature cache is independently retained as one DRAM hard controller plus eight data MSLICEs from `road_onchip_chain.v:292`. All dynamically selected DSP, ERAM, cache, MAC register, bias, valid, dot, and accumulator collections were nonempty; exact counts are in `discovered_object_counts.txt`.

DSP reset, operands, internal/result paths, ERAM input/output paths, and feature-cache controller/data paths all have positive max/min slack. Exact endpoints and corner records are retained in their individual timing reports.

## SYN-5025, clock, DRC, and exceptions

`SYN-5025` remains open. A fresh `pr.db` import and `check_timing -verbose` reports 53 dummy endpoints: 52 `mul9_mode`/`mul9_signed` model pins across 26 DSP SIOUs (48 belong to the 24 MAC DSPs) and one on-chip-chain LSLICE `reg_accumulator_alpha_reg[25]_syn_2.ofa`. Dynamic A/W/bias/control/RAM evidence does not close this generic warning.

Fresh check-timing reports 0 no-clock nets, 0 invalid constraints, 0 combinational loops, 0 local clocks, and 0 generated clocks disconnected from masters. It also reports 0 unconstrained inputs/outputs. Timing exceptions and ignored paths are empty.

TD additionally retains `PHY-5089` for 41 abnormal paths, `SYN-6021` for all 38 ports without user locations, and DRC notices `PHY-1035/PHY-1039` for 56 MSLICEs with redundant/unused register or CE attributes. Clock-bound, sigmap, duplicated-self-drive, bound, multi-drive, and local-clock-routing checks passed.

## Commands and retained failures

Primary build:

`E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/bin/td_commands_prompt.exe build.tcl`

Dynamic discovery:

`E:/project/qiansai/.tools/road_yolo_venv/Scripts/python.exe discover_hardblocks.py routed_netlist.v discovered_hardblocks.json export_discovered_hardblocks.tcl`

Fresh routed export:

`E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/bin/td_commands_prompt.exe export_discovered_hardblocks.tcl`

The final routed export completed and wrote object counts and all specialized reports. Preserved failed attempts are `td_20261007_174711.log` (candidate-register collection empty, fail-closed) and `td_20261007_175012.log` (incorrect `.\` command spelling). They are diagnostic records, not successful evidence.

Targeted functional logs pass, but the earlier strict 431-error gate is retained as failed. No claim of full release or timing signoff is made.
