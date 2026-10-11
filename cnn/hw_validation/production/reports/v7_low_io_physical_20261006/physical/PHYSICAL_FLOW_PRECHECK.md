# Low-I/O physical flow precheck

## Scope and hold point

This directory is an isolated diagnostic implementation target for the frozen
RoadYOLO minimal computation chain.  The physical run must not start until the
coordinator supplies the exact top-level source closure, its frozen hashes, and
a passing low-I/O functional regression.  This precheck does not modify the
MAC, round, SiLU, computation-chain RTL, internal interfaces, numerical
contract, reset contract, or initiation interval.

The run targets `PH1P35MDG324`, speed grade `-3`, at 100 MHz.  It stops before
bitstream generation.  It does not program a board or Flash and does not add a
false path, multicycle path, max/min path override, timing waiver, or hold
padding.

## Expected diagnostic boundary

The approved shell boundary has 38 logical I/O bits:

- clock and active-low asynchronous reset: 2 bits;
- 16-bit RX payload plus valid/ready: 18 bits;
- 16-bit TX payload plus valid/ready: 18 bits.

The exact port spelling remains a hold-point input.  The SDC must fail closed
if its clock, reset, RX, or TX port collections do not match the frozen top.

## Constraint contract

- `create_clock`: 10.000 ns period, rising edge at 0.000 ns and falling edge at
  5.000 ns.
- All non-clock inputs: diagnostic `-max 0.000` ns and `-min 0.000` ns input
  delays relative to the shell clock.
- All outputs: diagnostic `-max 0.000` ns and `-min 0.000` ns output delays
  relative to the shell clock.
- Reset remains an external asynchronous active-low input.  It receives the
  same explicit 0.000/0.000 ns diagnostic input-delay assumption and is not
  excluded from timing.  Recovery and removal paths from reset to registers
  must be exported.

The zero-delay values mean only that no external-device or board delay is
modeled in this isolated fixture.  They are deliberately fixed before the run
and must not be tuned to make timing pass.  They are not a board-interface
timing claim.

The installed TD manuals describe clock period and I/O delay values in ns; the
existing same-tool V6 run used a 10.000 ns clock and reported 100 MHz, which is
the local cross-check for the command units.

## Planned TD flow

1. Import `ph1_35p.db`, package `PH1P35MDG324`, speed `3`.
2. Open the isolated project in single-run mode and elaborate only the frozen
   low-I/O top.
3. Read the empty diagnostic ADC file, optimize RTL, and export the RTL area
   report.
4. Read the frozen SDC, optimize the gate netlist, legalize physical instances,
   reread the same SDC, and export the gate database and mapped netlist.
5. Update timing, place, route, export the routed database and implemented
   netlist, and export implemented area/QoR.
6. Update final timing and export the reports listed below.
7. Close the project.  No `bitgen` command is permitted.

## Mandatory evidence

- complete TD transcript, warning log, gate database, routed database, mapped
  and routed netlists;
- RTL and routed area, gate/place/route QoR, I/O listing, route status and DRC;
- timing status and summary, violation-only summary, and summary including
  ignored paths;
- complete register-to-register paths and reset-to-register recovery/removal
  paths;
- clock summary and endpoint coverage, `check_timing -verbose`, timing
  exceptions, ignored paths, abnormal targets, and unconstrained/partial-I/O
  diagnostics;
- hierarchy/resource evidence locating DSP, ERAM and feature-cache structures,
  plus mapped-netlist evidence that dynamic activation/weight/bias paths were
  not replaced by constants;
- source, constraint, tool, manual, database, netlist, and report hashes.

The physical result is reported as including the validation shell unless TD
provides reliable hierarchy accounting.  Fixed rescale coefficients may be
legally folded; that folding must be named and must not be represented as the
cost of a programmable multiplier.

## Official command evidence

The command set was checked against the installed TD 6.2 manuals and the
previous successful V6 PH1P run.  SWUG105 documents `report_area`,
`report_timing_summary`, `report_timing_path`, `report_clock_summary`,
`report_timing_exception`, `report_timing_ignored`, `update_timing`, and
`check_timing`.  SWUG200 documents `set_input_delay`, `set_output_delay`, and
recovery/removal analysis.

Tool and manual hashes:

- `td_commands_prompt.exe`:
  `e2e04ada5e256dccd017240c0f4dcface7f96dca67cde0e56e606ac0e02f827a`
- `SWUG105_TCL_Command_User_Guide.pdf`:
  `c6d97356cb930eab5b5613e4e9cf670a9a0cfec11dc04b678367f0e7d2431380`
- `SWUG200_Timing_Constraints_User_Guide.pdf`:
  `0865a98f86198b7d3c7837d52399041a505156a91e4c8cbb87631804527c361c`

The installed command reports TD version `6.2.168116`.  No TD synthesis,
placement, or routing has been run for the low-I/O shell at this precheck
stage.
