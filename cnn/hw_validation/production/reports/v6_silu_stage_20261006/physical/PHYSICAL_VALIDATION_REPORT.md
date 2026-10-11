# V6 isolated SiLU physical validation

## Decision

The frozen SiLU candidate elaborates with the PH1P vendor library, maps one
ERAM20K, completes placement and routing on `PH1P35MDG324` speed grade `-3`,
and has positive routed margins at the diagnostic 100 MHz constraint.  This is
component-level, automatic-placement evidence only.  It is not a board,
silicon, full-CNN, training, Flash, or merge acceptance result.

The upstream strict result remains blocking.  This probe was intentionally not
used to lower a threshold or hide an unknown.  Its own strict reports are also
retained as failing: probe-only has 214 errors and closure has 370 errors, both
with `delivery_ready=false` and zero strict warnings.

## Frozen inputs and assumptions

- DUT source: `production/reports/v3_silu_stall_candidate_20261005/silu_shared_unit.v`.
- DUT SHA-256: `5f357b493c7b3f941d9fa954a0ce5ec09091e466b641474360d2f64d0e42c938`.
- The copied DUT in `rtl/silu_shared_unit.v` has the same hash.
- Tool: Tang Dynasty `6.2.168116`; device `PH1P35MDG324`; speed grade `-3`.
- Clock: external `i_clk`, 10.000 ns period, 50% waveform.
- Reset: external asynchronous active-low `i_rstn`; no false path is applied.
- I/O delay: zero for the isolated diagnostic boundary only.
- Pins: deliberately unassigned.  TD performed automatic placement and issued
  `SYN-6021` for all 45 unconstrained logical ports.  The reported pin names
  and default I/O standards are not a proposed or accepted board mapping.
- No bitstream, programming, board run, timing waiver, min-delay padding,
  multicycle path, training, or Flash operation was performed.
- The workspace target is not inside a discoverable Git repository, so no
  branch or commit identity is claimed.

## Probe and functional evidence

`reference.py` fixes an 18-sample signed contract across lower bypass, central
lookup, the rounded address-1024 edge, upper bypass, consecutive input, and
output backpressure.  The table contract is `entry[address] = address - 512`
for all 1024 addresses.

The probe drives table, input, and output-ready controls from registers.  It
waits for the frozen DUT's `o_table_loaded`, holds valid/data through stalls,
checks every result, and exposes a registered count/checksum/error summary.
It does not substitute or infer a second memory.

Observed RTL simulation result:

```text
PASS table_writes=1024 inputs=18 results=18 stalls=2 checksum=00001e01
```

Python, compilation, and simulation each exited zero.  Raw stdout is in
`logs/reference_stdout.log` and `logs/simulation_stdout.log`.  The spec and
WaveDrom sources are under `spec/physical_probe/` and have the same module
name as the probe.

## Vendor binding and implemented ERAM

TD elaborated the source instance through the vendor definition in
`arch/ph1p_macro.v` and mapped it to one `PH1P_PHY_ERAM_V2` in the routed
netlist.  Relevant implemented-netlist facts are retained at
`td/routed_netlist.v`:

- mode: `DP20K`, port width 20, depth 1024, `REGMODE_A=NOREG`;
- address: `.addra({wire_table_address, 4'b1111})`;
- write enable: `.wea(flag_table_write_enable)`;
- output: `.doa(...)`/`.doa_extra(...)` reconstruct `wire_table_read_data`;
- clock: `.clka(i_clk...)`;
- source `CEA`: implemented as the active chip-select bit
  `.csa({flag_pipeline_enable, ...})`.

The last point is an implementation mapping, not an assumption that an opaque
black-box output is known.  The full routed netlist and routed database are
retained and hashed.

## Routed resources

| Resource | Used | Device capacity | Utilization |
|---|---:|---:|---:|
| Slice | 164 | 21,216 | 0.77% |
| LUT6 | 147 | 21,216 | 0.69% |
| Registers | 168 | 42,432 | 0.40% |
| ERAM20K | 1 | 108 | 0.93% |
| DSP | 0 | 40 | 0.00% |

TD reported no multi-drive, no abnormal timing path, routing DRC pass, and a
final routed wire length of 53,296.

## Routed timing

`all_paths_full.timing` reports both Slow and Fast corner checks and 99.92% STA
coverage.  There are no violated endpoints in the reported setup/hold groups.

| Check | Process corner | Paths recorded | Worst slack |
|---|---|---:|---:|
| Setup | `slow_m40c` | 385 | +1.338 ns |
| Hold | `fast_m40c` | 453 | +0.034 ns |
| Recovery | `slow_125c` | 107 | +4.975 ns |
| Removal | `fast_125c` | 107 | +0.053 ns |

The main clock group contains 490 setup and 490 hold endpoints with zero
violations and 1,346 paths analyzed.  The achieved diagnostic intra-clock Fmax
is 115.447 MHz against 100 MHz.

`check.timing` reports zero missing clocks, zero invalid constraints, zero
missing/partial input or output delays, and zero combinational loops.  It also
reports one tool-generated clock not connected to its master clock, while the
clock summary reports the single user clock with 108 endpoints.  Because STA
coverage is 99.92%, not 100%, this result must not be represented as complete
board-level timing closure.  No exception was added to conceal the residual.

## Retained evidence

- `td/gate.db`, `td/pr.db`: synthesis and routed databases.
- `td/gate_netlist.v`, `td/routed_netlist.v`: mapped netlists.
- `td/probe_route.area`, `td/route.qor`: resource/QoR reports.
- `td/probe_route.timing`, `td/all_paths_full.timing`: summarized and complete
  routed endpoint reports.
- `td/reset_to_regs_full.timing`: explicit recovery/removal paths.
- `td/internal_reg_to_reg_full.timing`: full register-to-register paths.
- `td/all_violations.timing`: violation-only export (no violation details).
- `td/check.timing`, `td/exceptions.timing`, `td/ignored.timing`,
  `td/abnormal_targets.timing`: coverage and waiver diagnostics.
- `td/td_20261006_020212.log`: successful synthesis/place/route transcript.
- `SHA256SUMS.txt`: immutable hashes for the principal inputs and outputs.

## Remaining risk and bounded conclusion

The result validates only the frozen component inside a synthetic registered
source/sink shell.  It does not validate the original design's strict gate,
real board pinout/I/O timing, power, CDC integration, full-CNN throughput, or
hardware behavior.  Stage-4 optimization was not attempted.  Any optimization
or board claim requires a separate authorized task with real top-level
constraints and must begin from this unmodified baseline.
