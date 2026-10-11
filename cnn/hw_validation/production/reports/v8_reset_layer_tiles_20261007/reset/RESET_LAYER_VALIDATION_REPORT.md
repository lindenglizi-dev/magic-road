# Reset-layer candidate validation report

## Outcome

The reset wrapper is functionally verified through the unchanged frozen 38-bit shell hierarchy with the PH1P vendor ERAM model. The final ModelSim evidence passes all fourteen inherited cases and six reset-focused cases. The routed physical snapshot was built from the exact same wrapper source hash, but it is **not deployment-ready** because minimum/removal findings remain. Static strict gates also remain failed and are retained without waiver.

Candidate RTL: `road_low_io_reset_shell.v`  
Top module: `road_low_io_reset_shell`  
Locked SHA-256: `8bd23e055a25af2691c867bad3f1d7e16b81fd39614748c4e988b1113493538e`  
Physical prebuild source SHA-256: identical (`match=true`)

## Interface and reset contract

The wrapper leaves the old shell interface widths and payloads unchanged. It adds no epoch signal and no arithmetic or scheduling state.

| Cycle/event | `i_rstn` | `reg_release_meta` after edge | `reg_release_done` after edge | frozen shell view on that edge | external ready/valid |
| --- | ---: | ---: | ---: | --- | --- |
| asynchronous assertion | 0 | 0 immediately | 0 immediately | reset asserted through `shell_rstn=0` | forced 0 immediately |
| first sampled release edge | 1 | 1 | 0 | reset remains asserted | forced 0 |
| second sampled release edge | 1 | 1 | 1 | shell still samples the old low `shell_rstn` | forced 0 through the sampled edge |
| third sampled release edge | 1 | 1 | 1 | first edge with reset high | first legal new transfer |

`shell_rstn` is exactly `reg_release_done`. Raw `i_rstn` is not ANDed into the frozen core reset path. Raw reset only asynchronously clears the two release registers and participates in `flag_interface_open = i_rstn & reg_release_done`, which immediately blocks:

- external `o_rx_ready` and `o_tx_valid`;
- internal `shell_rx_valid` and `shell_tx_ready`.

The first stage has no fanout other than the second stage. Simulation at 0.1 ns before and after a rising edge checks the first-sampled-edge rule; it does not prove analog metastability resolution.

Reset cancels table, packet, run, export, and held-response state inside the unchanged old shell. Recovery starts with a new `TABLE_BEGIN` and reloads all 1024 table entries. The external producer and consumer must discard an interrupted frame. A producer that keeps a pre-reset `valid` asserted through reset is outside the proved contract because no epoch interface was added.

Normal arithmetic, fixed multipliers, 38-bit low-I/O budget, run initiation interval, immediate-cancellation behavior, and the 436-cycle core schedule remain unchanged. The reset release and table reload interval is a separate recovery window.

The generated normative specification and cycle diagrams are under:

- `spec/reset_shell/road_low_io_reset_shell_spec.md`
- `spec/reset_shell/waveforms/road_low_io_reset_shell_two-stage-release.json5`
- `spec/reset_shell/waveforms/road_low_io_reset_shell_two-stage-release.svg`
- `spec/reset_shell/waveforms/road_low_io_reset_shell_asynchronous-cancel.json5`
- `spec/reset_shell/waveforms/road_low_io_reset_shell_asynchronous-cancel.svg`

## Functional verification

Tool: ModelSim SE-64 2020.4 from `D:/modeltech64_2020.4/win64`.

Compile closure:

1. PH1P vendor `ph1p_logic_eram.v` and `ph1p_phy_gsr.v`;
2. frozen `road_mac_probe.v`, `road_round_shift.v`, `silu_shared_unit.v`;
3. frozen `road_onchip_chain.v` and `road_low_io_physical_shell.v`;
4. locked reset wrapper and the selected testbench.

No behavioral RAM replacement was used.

| Run | Result | Compile | Simulation | Retained warnings |
| --- | --- | --- | --- | --- |
| reset-focused | `TB_PASS_RESET cases=6 errors=0 release_stages=2 first_consume_edge=3` | 0 errors, 0 warnings | 0 errors, 2 warnings | PH1P `INIT_FILE` part-select bounds |
| inherited regression through new wrapper | `TB_PASS_LOW_IO cases=14 errors=0 io_bits=38 max_packets=96 max_groups=24 max_terms=192` | 0 errors, 0 warnings | 0 errors, 2 warnings | same vendor warnings |

The six reset cases cover:

1. ordinary asynchronous assertion and two-edge release;
2. release 0.1 ns before a positive edge;
3. release 0.1 ns after a positive edge;
4. reset during partial table load;
5. full 1024-entry table reload;
6. reset during stalled STATUS response followed by recovery with no old receive count or transmit transaction.

The fourteen inherited cases use the original frozen vector files directly, rather than newline-normalized copies. Full vector and source hashes are in `SOURCE_AND_VECTOR_HASHES.json`. Final log hashes and cycle-trace hash are also recorded there.

Two non-RTL failures are deliberately retained:

- the restricted subprocess initially failed before compilation with a Windows DLL relocation error (`FIRST_ATTEMPT_TOOLCHAIN_FAILURE.md`);
- one diagnostic regression command omitted the `PH1P_PHY_GSR` top and failed at optimization (`modelsim_regression_missing_gsr_failure.log`).

The successful final command explicitly loaded both `reset_work.PH1P_PHY_GSR` and the testbench top.

## Strict eight-gate status

Static delivery readiness is false. The exact eight-check matrices and evidence hashes are in `STRICT_EIGHT_GATE_REPORT.md`.

- New wrapper: 54 strict errors.
- New reset-focused TB: 148 strict errors.
- Frozen evidence retained unchanged: shell 667, chain 374, included TB 219.
- The adapted regression TB also has current non-passing quality and comment-gate artifacts; they do not replace the frozen 219-error integrated baseline report.

The wrapper was not edited to chase style results after physical capture because even a comment-only change would break source-to-layout provenance. No failure is hidden by the functional pass.

## Physical cross-check and boundary

The physical build's `prebuild_manifest.json` records the same candidate, shell, and chain hashes. Its final receipt is `../physical/physical_validation_receipt.json`, SHA-256 `12eb916a4375f3907141fab710af97c7d94e0c4d8f62f15ddc836acf72c4da7d`, with status `DIAGNOSTIC_COMPLETE_SIGNOFF_FAIL`. That receipt also freezes the final 14+6 functional log hashes listed here. PH1P library evidence shows the existing mapped ordinary registers and DSP SIOU reset registers use low-active asynchronous reset modes; the library supports selectable asynchronous/synchronous SR modes but does not mandate two versus three synchronizer stages.

Routed snapshot summary:

- PH1P35MDG324-3, 100 MHz;
- 4066 slices, 1 ERAM, 26 DSP, 38 I/O bits;
- setup WNS +0.090 ns with zero setup endpoints violated;
- global minimum WNS -0.950 ns with 34 violated endpoints: 31 hold endpoints plus 3 raw-reset removal endpoints;
- STA coverage 100%, Slow/Fast max/min;
- routed audit found one physical stage-1 register and three auto-replicated stage-2 reset-distribution registers.

Reset-specific timing separates the intended synchronization path from the asynchronous entry boundary:

- stage-1 to stage-2 interstage setup +7.691 ns and hold +0.251 ns both pass; stage-1 fanout is exactly 3;
- functional reset distribution passes setup +5.664 ns, hold +0.251 ns, recovery +6.771 ns, and removal +0.099 ns; the three stage-2 replica fanouts are 110, 177, and 2255;
- raw external-reset removal fails at three of four physical release registers: -0.511 ns for stage 1 at slow/-40 C, and -0.426 ns slow/-40 C plus -0.022 ns fast/125 C for two stage-2 replicas; the remaining replica is +0.096 ns;
- 31 diagnostic-input hold failures and the generic `SYN-5025` closure issue also remain;
- the fresh check-timing report retains one local-clock warning and one orphan-generated-clock warning.

The two-stage architecture is therefore a candidate, not a metastability or timing-signoff claim. External-reset removal paths and the remaining minimum paths require physical closure. No timing exception was added; timing exception and ignored-path reports are empty.

## Scope confirmation

- No frozen source was edited.
- No training was run.
- No production bitstream was generated.
- No board or Flash operation was performed.
- No new timing exception was created.
- All authored files are confined to this `reset/` report directory.

Machine-readable handoff: `validation_receipt.json`.
