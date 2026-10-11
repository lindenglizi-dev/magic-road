# Clock / zeroing semantic questions

## Review conclusion

No reviewed RTL fact currently requires stopping the isolated `max_fanout = 16` diagnostic. The candidate is exactly one synthesis attribute on the existing `flag_mac_input_accept` wire; its Boolean definition and all data-path/control behavior are unchanged.

This conclusion is deliberately narrow. `SYN-5025`, the unnamed disconnected generated clock, primitive dummy nodes, and routed abnormal-path accounting remain open questions. The six `state_next` records with `PINS 0 DRIVER 0` prove only that those six elaborated nets are unloaded. They do **not** prove that every mapped primitive pin covered by the generic warning is harmless.

## Questions that must retain object identity

| Topic / concrete object | Current evidence | Question that remains | Acceptable answer for this experiment | Stop / signoff condition |
|---|---|---|---|---|
| `state_next_b22[3]`, `[1]`, `[0]`; `state_next_b16[2]`, `[1]`, `[0]` | Each query record says `PINS 0 DRIVER 0`; `loaded=[]`. | Are these purely optimized/dead state-decode fragments? | Yes, for these six objects only. | Any record changes to `PINS>0` with no driver, or is shown to feed active next-state logic. |
| `SYN-5025` warning object set | TD emits the generic message “Using 0 for all undriven pins and nets”; the message contains no object name. | Which exact mapped cells/pins/nets were zero-filled? What are their loads and owners? | The property experiment may proceed while this is pending because the RTL is unchanged apart from the attribute. | A loaded object is found on valid/ready/enable/state, MAC operand, weight, bias, RAM address/data/write-enable, or active primitive configuration. Such a result blocks the experiment result from being accepted and blocks signoff. |
| `PH1P_LOGIC_ERAM_Inst_silu_table.doa` / `wire_table_read_data` | RTL connects `doa` to the 20-bit wire; active A-port data/address/clock/enable/write controls are explicitly connected. B port is explicitly disabled; unused outputs are open. | Does the mapped ERAM retain the expected `doa` owner and synchronous-read behavior? | A mapped-driver query identifies the ERAM output as owner; no loaded ERAM input is undriven. | `doa` is constant-zeroed/unowned, or an active ERAM input is undriven. |
| ERAM address/data/write-enable: `addra`, `dia`, `wea`, `cea`, `clka` | Source connections are present and table protocol is range-guarded. | Are all five mapped pins driven after technology mapping, and does none appear in the SYN-5025 zeroed set? | All have a concrete source/constant and expected load. | Any active pin has no driver or unexpected constant replacement. |
| DSP mode nodes `PH1P_PHY_DSPSIOU_V2.*.mul9_mode` and `*.mul9_signed` | Listed as dummy nodes by timing checks for runner MACs and postprocess multipliers. | Are these unused model/configuration nodes, or live mode controls for signed multiplication? | They have no functional loads/endpoints, or their constant mode matches the inferred signed arithmetic contract. | A dummy node controls live DSP signedness/mode without a verified value. |
| `PH1P_PHY_LSLICE _al_n1_syn_752.ofb` | Listed once as a dummy node. | Which logical cone, load count, and endpoint correspond to this output? | No functional load/endpoint. | It feeds active control/data or a timing endpoint. |
| Primary `probe_clk` on `i_clk` | 100 MHz primary clock; 5550 clock endpoints, zero nonclock endpoints; no-clock count is zero; no multi-clock leaf pins; no internal-network clocks. | Do the candidate reports preserve exactly this endpoint coverage? | Same endpoint accounting and no new clock domain. | Endpoint loss, nonclock sequential endpoint, new unintended clock, or multi-clock leaf. |
| Unnamed generated clock disconnected from master | `check_timing` reports one instance, but the clock summary names only primary `probe_clk` and one local clock. | What are the generated clock name, source pin, master clock, and endpoint count? Is it a tool-created unused clock object? | Named object has zero functional endpoints and is demonstrably tool/model residue. | It owns any functional endpoint, clocks an active primitive, or represents an intended domain whose master is absent. This blocks timing signoff. |
| `PHY-5089` abnormal paths / final 44 targets | The final target list uses `probe_clk` at launch/capture; constraints contain no exceptions. Some paths are external diagnostic-shell IO; internal accounting must remain separate. | For every target, is the path external/diagnostic or internal/functionally reachable, and is it included in setup/hold/recovery/removal accounting? | All internal paths are analyzed and represented in the failed-endpoint counts; external zero-delay shell paths remain explicitly non-signoff. | Any reachable internal path is skipped or disappears from accounting. |

## Width and state protections relevant to zeroing triage

- Runner parameter indices stay inside the 40-entry arrays: PW `base/beta/gamma = 16..37 / 17..38 / 18..39`; accepted DW indices are at most 17.
- Runner queue pointers are intentional modulo-4 values, while `cnt_pw_meta` is protected at `0..4`. Work counters have terminal guards: DW writes `0..256`, PW writes `0..384`, position `0..15`, PW/DW MAC group `0..1 / 0..2`, export `0..383`.
- Adapter channel addition is protected by `flag_shape_fault`; invalid base/mask combinations enter ordered fault handling rather than normal publication.
- Postprocess storage is bounded by explicit ready conditions: ingress `0..2`, retire `0..8`, meta `0..8`; up to three lanes per one of eight retire entries keeps 5-bit inflight counters below 32.
- MAC result reservation/occupancy is `0..4`; a first-group accept is blocked at four unless a same-cycle result pop releases capacity.
- SiLU table expectation is `0..1023` then reset. Active lookup is `0..1024`, with address 1024 explicitly bypassed to `UPPER_VALUE`; the common pipeline enable freezes all stages under output backpressure.

These protections are why the existing VG122/VG109 reports do not currently establish a reachable overflow, underflow, latch, or missing-driver defect. They are not permission to discard those findings globally.

## Runner-entry review

The candidate `run.py` correctly binds imported helpers to the candidate `ROOT`, freezes the read-only baseline/dependencies, asserts an exact one-line RTL scope, reads the current gate JSON shape (`issues`, `checks.compile`, `parse_errors`), reviews only the known VG138 attribute-literal addition, and stops on exceptions. `functional()` performs scope and gate comparison before invoking simulation stages. `finish()` requires receipts, rejects nonempty `loaded`, verifies source hashes, and keeps production/deployment false.

The evidence-assurance gap found during review has been repaired in the current `run.py`: `finish()` now requires the exact scope string “elaborated top net query; not a complete mapped primitive pin proof” and requires every undriven record to contain `PINS 0 DRIVER 0`. This makes the entrypoint preserve the intended evidence boundary. The boundary itself remains incomplete, so even a successful `finish` must not be cited as closing `SYN-5025` or all primitive-pin zeroing.

At the updated review point, the authorized outside-sandbox rerun resolved Windows error 623. `simulation_current` points to `simulation_attempt2`: four suites pass 16 cases each, 64 total; `cycle_comparison` reports 64 full-field-identical rows and 1687 cycles on both sides; `mac_sim` passes with tasks 119, groups 849, and cycles 1211; all four load-boundary suites pass; and `shell_rtl` passes six tiles / 2304 bytes. TD implementation has started in the existing session 41379, but this review records no implementation result yet and did not call TD.
