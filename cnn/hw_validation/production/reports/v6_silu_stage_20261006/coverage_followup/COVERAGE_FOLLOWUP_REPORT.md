# V6 routed-STA coverage follow-up

## Scope and result

This follow-up only reopened the existing routed `pr.db` and exported timing
diagnostics.  It did not rerun synthesis, placement, routing, or hold fixing;
did not change RTL, SDC, checker behavior, production files, or exceptions;
and did not run bitstream generation.

The 99.92% STA metric remains **not closed to a named object**.  TD's public
local commands reproduce the percentage but do not expose an uncovered-object
list.  Therefore the remaining 0.08% is `BLOCKED_TOOL_ENUMERATION`, not waived
and not reclassified as harmless.

## Clock-object evidence

The read-only command below was run against the routed database:

```tcl
get_clocks -include_generated_clocks -verbose *
```

TD returned exactly one object, `probe_clk`.  `list_property probe_clk`
reported the public property names `CLASS DUTY_CYCLE FACTOR NAME PERIOD`.
The debug clock report classifies it as a `primary` 100 MHz clock sourced by
top-level `i_clk`.  Its tree contains 108 clock loads: 107 `lslice` loads and
one ERAM clock load; `nonclocks=0`.

No second or generated clock object is present in the public clock collection.
This is stronger evidence than trying to infer an object from an unlabelled
warning count.

## Non-verbose versus verbose `check_timing`

The original in-flow `physical/td/check.timing` says:

- one local clock;
- one generated clock not connected to its master clock.

After importing the same routed database, `check_timing -verbose` says:

- zero local clocks;
- zero generated clocks not connected to their master clocks;
- zero no-clock nets, dummy nodes, invalid constraints, combinational loops,
  missing/partial I/O delays, and no-path constraints.

The original warning has therefore **not been proven fixed or harmless**.  It
is not reproducible in the re-imported verbose report, and neither report names
an offending clock.  The evidence supports only an inconsistency between the
original non-verbose in-flow diagnostic and the re-imported verbose diagnostic.

## 99.92% coverage localization attempt

`report_timing_summary -include_ignored` still reports 99.92%, Slow/Fast Max
and Min checked, and the same single `probe_clk -> probe_clk` path group:

- 490 max endpoints, zero violations, 1,346 paths analyzed;
- 490 min endpoints, zero violations, 1,346 paths analyzed;
- SWNS `+1.338 ns`; HWNS `+0.034 ns`.

The exported ignored-path report is empty, the timing-exception report is
empty, and the abnormal-target report is empty.  The official installed
SWUG105 command guide documents `report_timing_summary`,
`report_timing_ignored`, `report_clock_summary`, and `check_timing`; its public
interfaces contain no command that enumerates the objects behind the aggregate
STA-coverage percentage.  SWUG201 names the displayed value as STA coverage
but does not define an object-level export in the consulted Timing General and
Check Timing sections.

Consequently, assigning the 0.08% to a particular register, RAM pin, reset
arc, or tool-created clock would be speculation.  No exception or constraint
change was made to force the percentage to 100%.

## Internal and reset path classification

These values are taken from the already-frozen detailed reports whose hashes
are included in `SHA256SUMS.txt`.

| Filtered report | Check/corner | Worst slack | Begin point | End point |
|---|---|---:|---|---|
| `get_regs -> get_regs` | setup / `slow_m40c` | +4.262 ns | `reg_table_valid_reg_syn_3.clk` | `reg_table_addr_reg[1]_syn_2.cea` |
| `get_regs -> get_regs` | hold / `fast_m40c` | +0.054 ns | `silu_shared_unit_Inst_stage/flag_round_upper_reg_syn_3.clk` | `silu_shared_unit_Inst_stage/flag_value_lower_reg_syn_3.imb` |
| `i_rstn -> get_regs` | recovery / `slow_125c` | +4.975 ns | `i_rstn` | `reg_input_data_reg[13]_syn_7.asr` |
| `i_rstn -> get_regs` | removal / `fast_125c` | +0.053 ns | `i_rstn` | `reg_checksum_reg[10]_syn_2.asr` |

The `get_regs -> get_regs` report is a filtered register report, not a complete
internal-path inventory: it excludes ERAM and pad endpoints.  In particular,
the global setup and hold results remain `+1.338 ns` and `+0.034 ns`; the
filtered values must not replace them.

## Command and exit

Working directory: this `coverage_followup` directory.

```powershell
E:\Anlogic\TD_6.2.1_Engineer_6.2.168.116\bin\td_commands_prompt.exe export_coverage.tcl
```

Process exit: `0`.  `td_20261006_103438.log` records database import and every
report command.  The script contains only device/database import, final timing
refresh, object queries, and reports.

## Public RTL gate boundary

No RTL was created or modified in this follow-up.  The public delivery matrix
(`compile`, `ast`, `readability`, `comment`, `naming`, `profile`, `testbench`,
`toolchain`) was not rerun.  This directory adds only routed-toolchain
diagnostics; the frozen strict reports in `physical/` remain authoritative and
blocking.
