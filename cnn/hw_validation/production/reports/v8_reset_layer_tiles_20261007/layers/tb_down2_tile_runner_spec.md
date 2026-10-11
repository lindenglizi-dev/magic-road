# tb_down2_tile_runner specification

Self-checking Verilog-2001 testbench for `down2_tile_runner` using the official PH1P vendor model.

- Reloads 1024 SiLU entries after every reset.
- Runs top-left, interior, bottom-right, and PW-only deterministic cases.
- Checks every debug phase against `vectors/*_stages.hex` and all 384 exported INT8 values.
- Checks preload and core endpoint cycles, mutually exclusive counter reconciliation, table-write exclusion during core work, incomplete-preload rejection, export backpressure stability, in-flight reset cancellation, a 20-cycle no-ghost interval, and faulted-tile invisibility.
- Emits `TB_PASS_DOWN2_TILE cases=4` only when the accumulated error count is zero; a 19 ms watchdog terminates hangs.

Timing follows `waveforms/down2_tile_runner_full.json5`; the testbench samples ready-valid payloads on the consuming edge before nonblocking state updates.
