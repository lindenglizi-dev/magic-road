# down2 4x4 tile functional validation

## Result

ModelSim SE-64 2020.4 compiled the final source closure with 0 errors and 0 warnings. The final vendor-model simulation finished with `TB_PASS_DOWN2_TILE cases=4`, 0 simulator errors, and the two retained official `INIT_FILE=NONE` part-select warnings from `ph1p_logic_eram.v`.

All four deterministic cases matched Python at every accumulator, pre-round INT16, SiLU INT16, post-round INT16, and final exported INT8 value. Full cases each checked 640 result records (256 DW and 384 PW); PW standalone checked 384. None of the 384 final outputs in any nominal case saturated, so saturation evidence remains the responsibility of the already frozen arithmetic-core regression, not this layer result.

## Measured cycles

At 100 MHz, each full DW->PW tile measured 27,393 core cycles (273.93 us). The mutually exclusive categories are 8,064 MAC, 6,400 pre-round, 4,480 SiLU, 6,400 post-round, 640 writeback, 768 local storage preparation, and 641 scheduler idle cycles. Their sum is exactly 27,393, and the independently observed RUN-to-done endpoint difference is also 27,393.

The runner also counted each layer directly. DW measured 13,312 cycles: 5,376 MAC, 2,560 pre-round, 1,792 SiLU, 2,560 post-round, 256 writeback, 512 local storage preparation, and 256 scheduler idle. PW measured 14,081 cycles: 2,688 MAC, 3,840 pre-round, 2,688 SiLU, 3,840 post-round, 384 writeback, 256 local storage preparation, and 385 scheduler idle. Both layer sums were asserted in the TB; DW+PW equals the full 27,393 endpoint without using subtraction as the measurement method.

PW standalone measured 14,081 core cycles (140.81 us): 2,688 MAC, 3,840 pre-round, 2,688 SiLU, 3,840 post-round, 384 writeback, 256 local storage preparation, and 385 scheduler idle cycles.

The real preload endpoint was 2,894 cycles for full tiles (1,024 accepted table writes plus 1,864 accepted cache/parameter writes) and 1,692 cycles for PW standalone (1,024 plus 664). The fixed export-backpressure pattern measured 449 cycles for 384 transfers. `storage_wait` is the runner's one-cycle local array-read/operand-register preparation per MAC group; it is not DDR latency or measured dynamic memory backpressure.

## DW utilization

The tile performs 256 x 9 = 2,304 useful depthwise products in 512 MAC groups. The frozen common-A 8x3-output MAC exposes 12,288 physical multiplication slots, so physical slot utilization is 18.75%; activation-lane utilization is 56.25%. Common masks open 6,912 physical slots, of which 4,608 deliberately multiply zero weights in the two non-target output lanes. Tail masks suppress 5,376 physical slots. Top-left padding contributes 368 legitimate zero-valued kernel products; those are not tail-masked operations.

## Protocol and fault checks

- Table writes were rejected while core work was active.
- Incomplete preload could not start a run.
- Export held data and index under backpressure.
- Reset during an in-flight PW run cancelled valid/busy/debug/table-loaded state and produced no ghost event for 20 cycles.
- A directed signed-accumulator overflow raised fault, never raised done, and left the partial tile unavailable to export.
- Internal PW channel writes are not externally visible until the whole tile completes without fault.

## Evidence boundary

This is an isolated 4x4 layer-tile functional measurement with deterministic test coefficients, not trained QAT. It does not prove whole-network throughput, DDR behavior, place-and-route resources/timing, board behavior, or accuracy. No training, production bitstream, Flash write, timing exception, frozen arithmetic-core interface, or production RTL was changed. The result is not compared as an acceleration against the older v7 position-chain because its work and endpoints differ.

The first simulation failed only because the TB sampled export after the consuming edge; that preserved log is `modelsim_run_first_failed.log`. The corrected final run is `modelsim_run_complete.log`.

## Strict gate

The governed strict deliverable gate is a real failure: `delivery_ready=false`, 319 errors, 0 strict warnings. Public states are compile/AST/readability/comment/naming/profile failed, testbench passed, and toolchain not requested by that static gate. The dominant root is a control-parser strict failure on this array/index-heavy validation runner, with additional missing Erie header/comment coverage and compact case-item style findings. The full JSON and Markdown reports are retained. Functional ModelSim success does not override this delivery blocker, and no broad style/parser-driven RTL rewrite was made after the frozen passing simulation.

