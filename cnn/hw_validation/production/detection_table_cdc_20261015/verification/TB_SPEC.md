# Detection table CDC testbench specification

## Scope and clocks

The retained suite checks `road_time_snapshot` and `road_detection_table_cdc` as controlled components. The source clock is exactly 100 MHz. The destination test clock has a 13.334 ns period (74.996250 MHz after 1 ps quantization of the nominal 75 MHz template clock) and starts with a 2.3 ns phase offset. This is intentionally not an integer source/destination ratio.

The Python SRIF oracle specifies metadata, FINAL97 values, filter decisions, CDC timing bounds, and age telemetry. It is not used as a substitute for the hardware CDC path. Case 20 connects the real destination outputs of `road_time_snapshot` directly to the table time inputs.

## Time cases

- Case 0 runs beyond 6 ms, requires exact 100000-source-clock ticks, checks the frozen 96-bit snapshot while busy, verifies epoch/time atomicity, and records request-to-update plus acknowledgement round-trip latency.
- Case 1 stops the source clock only after valid snapshots, keeps the destination clock running, requires validity withdrawal exactly 150001 destination clocks after the last update, then resumes the source and requires valid snapshots to recover. This is a time-watchdog test, not unilateral reset support.

## Table cases

- Case 10 consumes CPU vectors for counts 0, 1, 32, 33, and 64 with deterministic random source bubbles. Every accepted entry, all 265 metadata bits, count gating, zero out-of-count reads, copy acknowledgement, pending publication, and SOF activation are checked. Count zero remains a complete active diagnostic table but cannot draw.
- Case 11 holds `copy_enable` low for 512 destination clocks, fills pending, seals a second table while pending is occupied, holds it for 200 destination clocks, and verifies that the first active table cannot change before SOF. A one-entry copy presents SOF on the last-copy edge and proves no same-edge bypass.
- Case 12 applies the common asynchronous reset with locally synchronized release at every destination copy cursor value 0 through 63. Each interrupted generation must leave no ack, pending, active, or stale readable result. A complete recovery publication follows.
- Case 13 uses independent 500 ms and 2000 ms parameter instances. It checks raw age 496/497 and 1996/1997 boundaries, time/epoch/model/status/order/future failures, CPU status 1/2/3 diagnostic tables, valid near-`UINT64_MAX` time, 65-bit overflow rejection, and `UINT64_MAX` unknown/saturated age telemetry.
- Case 14 distinguishes partial unsealed abort from sealed abort. A sealed abort must raise one source error pulse without cancelling or changing the publication. The same case holds source `valid` high for 64 adjacent accepted source clocks with different FINAL97 payloads, then seals, copies, activates, and reads back all 64 items.
- Case 20 directly connects real time CDC outputs to the table. It fills pending, keeps a second table blocked with `copy_enable=0` while time snapshots continue, activates both tables only on SOF, withdraws draw after a source-clock outage, and restores draw on the first recovered time snapshot.

## Reset, failure, and receipt rules

Only a common reset is claimed. RAM contents are not cleared; valid/count state must isolate them. Every run uses a fresh retained directory. Compilation must finish with zero errors and zero warnings, both Python reference self-checks must pass, and a test-specific PASS marker is required before a receipt is written. Failed attempts remain under `verification/` and are never promoted to final receipts.

Free-running time cycles are reported independently from table preload/copy/SOF intervals; they are not added together as a processing latency.
