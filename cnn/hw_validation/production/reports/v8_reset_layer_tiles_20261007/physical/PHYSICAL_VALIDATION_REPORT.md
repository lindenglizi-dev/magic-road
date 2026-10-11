# Reset-layer physical validation report

## Verdict

The routed 100 MHz diagnostic build completed with setup passing, but it does **not** pass physical sign-off. The final minimum-delay result contains 34 violations: 31 diagnostic-input hold violations and 3 raw external-reset removal violations on the synchronizer registers. No timing exception was added, and no bitstream was generated.

The functional evidence is positive and the frozen reset-shell source did not change during implementation: ModelSim SE-64 2020.4 reports `TB_PASS_RESET cases=6 errors=0 release_stages=2 first_consume_edge=3` and `TB_PASS_LOW_IO cases=14 errors=0`. This functional result does not waive the routed reset-removal failures.

## Frozen inputs and tool identity

- Top: `road_low_io_reset_shell`
- Target: PH1P35MDG324, speed grade -3, 100 MHz
- Tool: Tang Dynasty 6.2.168116
- Tool executable SHA-256: `e2e04ada5e256dccd017240c0f4dcface7f96dca67cde0e56e606ac0e02f827a`
- Reset shell SHA-256 before and after P&R: `8bd23e055a25af2691c867bad3f1d7e16b81fd39614748c4e988b1113493538e`
- SDC SHA-256: `0acbd5f47b4e262f839b022377e0da98850aa49bb06c79106be3207871fc3d5e`
- Old physical shell SHA-256: `c7bd74ccf995f7f7a8527e7c6f8f661183bccd0a3f266922d4c0a026d019f5d5`
- Frozen core SHA-256: `6ec48c6ddda89ab91e66926c42e012b3d9c45cc93150823ffb50c1eb627f7132`
- Gate DB SHA-256: `d018d9972cce848d8332bb941349ddcb6450c5e0171bcdd0b8f0bcdf06974256`
- Routed DB SHA-256: `9fe24b34691da0cc3294e0322ab7f1f18e0fb4fc4abdbf760bdbd7e7a874f0a9`
- Routed netlist SHA-256: `afb4d58bb0145322091579f45589f6f713d827bb3f5db2f54e1363cde66a62c1`

The retained diagnostic SDC constrains 19 non-clock input bits, including `i_rstn`, with both max and min delay at 0 ns, and all 18 output bits with both max and min delay at 0 ns. It contains no false path, multicycle path, max-delay exception, or min-delay exception.

## STA scope and coverage

TD reports routed confidence, 100.00% STA coverage, 10,120 endpoints, and 49,859 analyzed paths. `Check Corner` is `Both (Slow and Fast)`, with all four check cells enabled: Slow Max, Slow Min, Fast Max, and Fast Min. Actual reported path processes include `slow_m40c`, `slow_125c`, `fast_m40c`, and `fast_125c`; these are the process labels evidenced by this TD database, not a claim about unsupported additional corners.

| Path class | Setup | Hold | Recovery | Removal | Result |
|---|---:|---:|---:|---:|---|
| Global summary | +0.090 ns max | -0.950 ns min | included | included | max pass; min fail |
| Internal reg-to-reg | +2.055 ns | +0.042 ns | N/A | N/A | pass |
| Diagnostic inputs to registers | +3.263 ns | -0.950 ns | N/A | N/A | 31 hold failures |
| Registers to diagnostic outputs | +0.090 ns | +2.680 ns | N/A | N/A | pass |
| External `i_rstn` entry | +3.597 ns | +0.085 ns | +8.088 ns | **-0.511 ns** | 3 removal failures |
| Synchronizer stage-to-stage | +7.691 ns | +0.251 ns | N/A | N/A | pass |
| Functional reset distribution | +5.664 ns | +0.251 ns | +6.771 ns | +0.099 ns | pass |
| DSP reset | +6.221 ns | +0.206 ns | +6.414 ns | +0.201 ns | pass |
| DSP operands | +2.972 ns | +0.150 ns | N/A | N/A | pass |
| DSP internal/results | +3.624 ns | +0.463 ns | N/A | N/A | pass |
| ERAM inputs | +4.109 ns | +0.023 ns | N/A | N/A | pass |
| ERAM outputs | +6.534 ns | +0.928 ns | N/A | N/A | pass |

The violations-only report contains exactly 31 `hold` checks and 3 `removal` checks. Of these, 26 are reported at `slow_m40c` and 8 at `fast_125c`. The global worst path is a diagnostic boundary path from `i_rx_data[2]` to `reg_run_packet_count_reg[2]`, hold slack -0.950 ns at `slow_m40c`; it is not a reset path.

## Reset implementation and physical paths

Vendor model and routed-netlist evidence agree on asynchronous active-low reset behavior. The ordinary PH1P slice cells use inverted ASR selection and asynchronous reset values. Each DSP SIOU uses `RST0=INV` with `SR0MODE` through `SR3MODE` set to `ASYNC`. The vendor model supports both ASYNC and SYNC modes, but supplies no evidence that mandates a two-stage or three-stage synchronizer; the implemented two-stage contract is therefore validated as implemented, not as a vendor-prescribed stage count.

TD retained one first-stage register and automatically replicated only the second stage:

| Physical cell | Logical role | Recovery | Removal | Raw-reset delay | Functional fanout |
|---|---|---:|---:|---:|---:|
| `reg_release_done_reg_syn_3` | first stage, output is `reg_release_meta` | +8.969 ns, fast_m40c | **-0.511 ns, slow_m40c** | 2.464 ns | 3 second-stage D pins |
| `reg_release_done_reg_syn_4` | replicated `reg_release_done` | +8.365 ns, slow_125c | **-0.022 ns, fast_125c** | 1.402 ns | 110 |
| `reg_release_done_reg_syn_5` | replicated `reg_release_done` | +8.916 ns, slow_125c | **-0.426 ns, slow_m40c** | 2.549 ns | 177 |
| `reg_release_done_reg_syn_6` | replicated `reg_release_done` | +8.088 ns, slow_125c | +0.096 ns, fast_125c | 1.512 ns | 2255 |

The raw external reset physical fanout is 9. It drives the asynchronous reset inputs of the one first-stage and three second-stage physical registers, as well as the immediate interface gating logic. The three negative removal checks above remain blocking because the first and second synchronizer stages themselves are asynchronously reset.

The first-stage output has fanout 3 and drives only the three second-stage copies. Its worst stage-to-stage setup path is +7.691 ns at `slow_m40c`, with 2.123 ns data delay; its worst hold path is +0.251 ns at `fast_m40c`, with 0.335 ns data delay.

The second-stage copies drive the frozen shell/core reset. Functional distribution covers 2,624 max endpoints and 3,504 min endpoints. The worst removal path is +0.099 ns at `fast_m40c`; data delay is 0.158 ns, including 0.096 ns net delay, on the 2,255-fanout copy. Thus the functional reset distribution passes, but the external asynchronous entry does not. Functional consumption remains on edge 3 after raw reset release, matching the simulation contract.

TD QoR reports `async_reg=0`, so the tool did not recognize a dedicated asynchronous-register attribute on this chain. No new attribute or source change was introduced in this diagnostic run.

## DSP, ERAM, and data-path preservation

The routed design contains 26 DSP SIOU cells and 26 paired DSP multiplier cells. DSP reset timing covers 52 max and 52 min endpoints with no violation. DSP operand timing covers 1,549 max/min endpoints, and DSP internal/result timing covers 421 max/min endpoints, all passing.

The machine audit records all 26 SIOU instances and their `ce`, `rst`, `xa`, `y`, `mul9_mode`, `mul9_signed`, and result connections. All 52 `mul9_mode`/`mul9_signed` outputs are connected to their paired DSP multiplier; they are nevertheless reported by TD as dummy timing endpoints. All 24 MAC DSPs retain dynamic activation on XA and dynamic weight on Y. References cover all 64 activation bits, all 192 weight bits, and all 96 bias bits.

The distributed memory implementation contains 93 `PH1P_PHY_DRAMHARDCON` controllers and 744 DPRAM MSLICE cells. Every controller has dynamic byte/write address, write clock, and write-enable inputs; `wrst=0` is the expected fixed content-reset choice. The RAM MSLICE data connections cover all 64 activation packet bits, all 192 weight packet bits, and all 96 bias packet bits.

The single ERAM has dynamic address, data, chip-select function, and write enable. Its input timing is +4.109/+0.023 ns and output timing is +6.534/+0.928 ns. Its primitive reset muxes are fixed inactive in this design, so it is not part of the functional reset fanout.

## SYN-5025 and timing-audit status

`SYN-5025 WARNING: Using 0 for all undriven pins and nets` remains **unclosed** because the warning is generic and does not identify each forced pin. It must not be reported as cleared merely because the functional paths below remain dynamic.

`check_timing -verbose` inventories exactly 53 dummy endpoints:

- 52 DSP timing endpoints: `mul9_mode` and `mul9_signed` on every one of the 26 SIOU cells. These nets are connected to paired DSPMULT cells.
- One unused LSLICE output: `road_low_io_physical_shell_Inst_reset/road_onchip_chain_Inst_shell/road_mac_probe_Inst_chain/reg_accumulator_reg[82]_syn_2.ofa`.

This last dummy differs from the prior baseline's SiLU `ofa` dummy, so no old name was carried forward. Every object and connection is serialized in `routed_netlist_audit.json`; its status is `WARNING_UNCLOSED_STRUCTURAL_DATA_PATHS_PRESENT`.

Other timing checks report zero no-clock nets, zero invalid constraints, zero combinational loops, zero missing/partial input/output delays, zero timing exceptions, and zero ignored paths. They also report one local clock (`probe_clk`) and one inferred/generated clock not connected to its master clock. Two independent fresh-process `pr.db` imports preserved the original reports and re-exported the checks; both warnings remained. The routed area report's local-clock resource count of zero does not replace the `check_timing` result. These clock-definition warnings therefore remain unclosed even though `probe_clk` endpoint coverage is 100%.

## Resources and implementation warnings

The routed top uses 4,066 slices, 3,783 slice registers, 26 DSPs, 1 ERAM, 93 distributed-RAM hard controllers, 38 IOs, 1 GCLK, and 4 SCLKs. The frozen old shell accounts for 3,779 routed registers; the reset wrapper accounts for four physical registers because TD replicated the logical second stage three ways. Compared with the prior 4,068-slice baseline, the slice count changed by -2; DSP, ERAM, and IO counts remain 26/1/38.

TD ran its normal `fix_hold` stage; it was not pointlessly re-enabled. `PHY-5089` reports 34 abnormal paths skipped during routing, matching the final 34 min violations and improving from the old 437-skipped diagnostic. The run also retains the intentional diagnostic condition that all 38 IOs lack board pin assignments; TD warns that bit generation would abort. No override was added.

The initial `td_commands_prompt.exe -h` probe failed because the executable interpreted `-h` as a Tcl filename. Its `td_20261007_162049.log` and `.logw` records are preserved and were not overwritten. The actual build log is `td_20261007_162237.log`; the build exited successfully. The project metadata also emitted an inert `mclk_freq=33MHz` setting warning, while the effective STA clock is the explicit 10.000 ns SDC clock.

Fresh routed-database checks were run with `reexport_check_timing_fresh.tcl` and `reexport_check_timing_fresh2.tcl`, producing separate `fresh*` and `fresh2*` reports and TD logs. They did not overwrite build-session evidence and did not add constraints or exceptions.

## Coverage, omissions, and prohibited outputs

- STA coverage: 100.00% as reported by TD.
- Unconstrained input/output delay bits: 0/0.
- Timing exceptions: 0; ignored timing paths: 0.
- Setup violations: 0; minimum-delay violations: 34.
- Bit generation: not invoked.
- Bitstream/programming files created: 0.
- Board, Flash, and hardware programming: not performed.

The correct next decision is not an exception. Any further closure work must preserve timing of the raw reset entry and must not false-path the synchronizer, fabricate input minimum delay, blindly replicate the first stage, or change the frozen core interface. The routed evidence first requires an explicit architectural decision about the asynchronous-reset removal failures.
