# RoadYOLO low-I/O physical-shell functional validation

## Result

Status is **functional simulation passed, strict delivery gate failed, physical TD result pending**. This stage does not establish production readiness, board readiness, resource closure, or timing closure.

- Top-level I/O is 38 bits across exactly eight ports.
- Frozen RTL SHA-256 is `c7bd74ccf995f7f7a8527e7c6f8f661183bccd0a3f266922d4c0a026d019f5d5`.
- Frozen testbench SHA-256 is `62424751aab4f8292a154531600cab2d630e1a7813238056700a8b44dcc86bc6`.
- ModelSim compiled the full frozen dependency set with 0 errors and 0 warnings.
- ModelSim ran 14 test groups with 0 test errors. The encrypted PH1P ERAM model emitted two retained `INIT_FILE` part-select warnings.
- The public strict gate did not pass: shell 667 errors; testbench explicitly included 219 errors. These failures are retained.

## Frozen function

The shell dynamically loads the 1024-entry SiLU table, then buffers up to 96 complete 362-bit compute packets. One to four positions are accepted, with no more than 24 groups and 192 enabled products per position. A legal RUN forwards the original full-width parallel fields unchanged to the frozen chain. Completion is published only after the last input handshake, an observed busy-low interval, and the original chain returning ready. The real cache read port supplies every exported feature/fault item.

Only one RUN is allowed per reset. A second RUN is explicitly rejected because the frozen chain does not clear all prior cache-valid state for address reuse. Reset cancels partial table, partial packet, active compute, held result, and held status transactions; a new table load is required afterward.

## Functional cases

The final clean ModelSim library covers:

1. Partial table cannot start compute.
2. Base 16-channel result, TX backpressure, counters, status, and second-RUN rejection.
3. Tail 13-channel result.
4. Output saturation.
5. Atomic terminal MAC fault producing three faulted zero cache items.
6. Positive signed-33 temporary excursion followed by legal recovery.
7. Negative signed-33 temporary excursion followed by legal recovery.
8. Maximum legal 24-group/192-term nonzero result, compared item by item.
9. Maximum 24-group final overflow fault.
10. Full 96-packet/four-position buffer producing exactly 12 results.
11. A 25th group rejected without starting RUN.
12. Partial packet blocking plus reset cancellation.
13. Uncommitted address 0 and out-of-range address 15 diagnostic reads returning fault and zero data.
14. Reset during compute, held export, and held status, followed by table reload and successful recovery.

The testbench also asserts one RX transfer per host word, stable buffered parallel payload during core backpressure, stable TX data during backpressure, exact result ordering, and equality between STATUS counters and independently observed phase endpoints. Checksums remain auxiliary and never replace itemwise comparison.

## Measured cycles

All phase values use endpoint differences and exclude the start endpoint:

- Preload: TABLE_BEGIN handshake to legal RUN handshake. It includes table loading and narrow packet upload.
- Core: first original parallel input handshake to complete-position terminal completion.
- Export: EXPORT command handshake to consumption of the last actual cache result. The completion frame is recorded separately and is not added.

Representative results from `shell_phase_cycles.csv`:

| Case | Preload | Core | Export | Result |
|---|---:|---:|---:|---|
| base16 | 2428 | 436 | 60 | complete |
| maximum_192_legal | 3180 | 351 | 13 | complete |
| maximum_192_fault | 3180 | 266 | 13 | terminal fault |
| maximum_96_packets | 6564 | 1404 | 60 | complete |
| cancelled_core_reset | 2099 | 2 | — | cancelled, excluded from throughput |
| held_export_setup | 2099 | 98 | — | export cancelled by reset |

The base16 core-only 436 cycles break down without overlap or double counting as: MAC 88, pre-requant 132, SiLU 84, post-requant 120, commit 12, fault 0. The older 482-cycle observation included a different readback boundary and must not be compared as if it were the same core interval.

## Strict eight-gate state

The shell strict report is not delivery-ready:

| Gate | Shell | Explicitly included TB |
|---|---|---|
| compile | passed | failed (unsupported multi-module behavioral shape) |
| ast | failed: 12 | failed: 2 |
| readability | failed: 654 | failed: 125 |
| comment | failed: 1 | failed: 93 |
| naming | failed: 32 | failed: 120 |
| profile | failed: 1 | failed: 1 |
| testbench | not requested | passed |
| toolchain | not requested | not requested |

ModelSim PASS is separate external evidence and is not presented as the public `toolchain` gate passing.

The 667 shell errors include both potentially semantic findings and formatting/static-closure limitations. Important groups are literal/arithmetic width (VG125 56, VG122 15), FSM reachability (VG098 16), source/driver closure (VG097 1, VG153 15), and combinational complexity/budget (VG145 8, VG146 106, VG147 48). Formatting and comment-placement findings are listed separately in the full report, led by VG060 216 and VG061 44. VG104 combinational-loop and VG141 multiple-driver produced no findings, but that is not a waiver for the AST and source-closure failures. The earlier frozen chain's 374 diagnostics remain independently open.

## Change history and artifact routing

The final functional fix cleared the held RUN-report TX valid after its one accepted transfer. The pre-fix source is retained as `road_low_io_physical_shell_before_run_report_clear.v`; `modelsim_shell_run_second.log` demonstrates the stale-library/pre-fix deadlock. A fully clean recompile produced the final passing evidence.

After functional freeze, only four bilingual header comment fields were corrected: English Description and Simulations, plus Chinese 模块说明 and 仿真工程. No executable RTL changed in that comment-only step. The final C7BD hash was then rebuilt in a clean ModelSim library.

The valid generated specification is `spec/low_io_physical/road_low_io_physical_shell_spec.md`. The duplicate `spec/spec/low_io_physical/` tree is an obsolete output-routing diagnostic and is not authoritative. It is retained rather than silently deleted.

## Boundary

This work did not alter the signed-33 MAC, rounding, SiLU, minimal chain, coefficient contract, external chain interface, current II, production project, training, board, Flash, or deployment bitstream. Resource usage, worst physical path, setup/hold/recovery/removal, and PH1P35 100 MHz closure must come from the separate TD run.
