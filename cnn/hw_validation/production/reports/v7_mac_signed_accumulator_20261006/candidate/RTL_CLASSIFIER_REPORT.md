# V7 signed33 MAC candidate report

## Outcome

The independent `road_mac_probe` candidate now retains three signed33 accumulators across groups and applies the signed INT32 range check only to the aligned last group. Its ports, module name, registered single-inflight protocol, terminal latency, non-last acceptance interval, backpressure behavior, and reset cancellation behavior are unchanged.

The candidate is functionally verified for the frozen legal caller contract and passes its single-file strict gate. This report does not authorize production merge, board programming, training, Flash, TD implementation, timing exceptions, or an II optimization.

## Surgical RTL change

- Widened only the three-channel base/history path: accumulator, base product/pair/quad/dot, and delayed writeback are 99 bits (`3 x signed33`).
- Independently sign-extended each signed32 bias before packing it into the 99-bit first-beat base.
- Formed each candidate as `signed33 + signed33 -> signed34`; retained the existing candidate/hold/final register count.
- Wrote candidate bit 32 back on non-last groups instead of truncating at bit 31.
- Gated the existing overflow summary with the same payload's `reg_last_pipe[5]`. The per-lane range facts, final candidate, `flag_last`, and publish/commit events keep their original relative phases.
- Kept visible results at three signed32 lanes. A terminal fault in any lane still forces the complete 96-bit result to zero and suppresses commit.

The exact source patch is `road_mac_probe_signed33.patch`; the complete arithmetic path is `WIDTH_PATH_TABLE.md`.

## Proof boundary

The machine-readable proof in `../coordinator/range_proof.json` closes all 67 frozen graph layers. Its maximum is `fuse4_bu.reduce.conv`, 192 active terms / 24 beats. Bias plus every legal prefix is `[-2150604800, 2150629375]`, inside signed33.

This relies on the caller obligation that `first` starts a reduction, `last` ends it, and the scheduler does not exceed 24 beats / 192 active terms. Infinite or malformed first/last streams are outside the proof. No counter, port, watchdog, or hidden saturation behavior was added.

## Verification summary

| Evidence | Result |
| --- | --- |
| Frozen base vectors | 8/8 pass |
| Frozen tail-mask vectors | 8/8 pass |
| Frozen stream regression | 1031/1031 pass |
| Signed33 directed suite | 84 beats, 12 cases, zero errors |
| Official ModelSim 2020.4 rerun | compile/run zero errors and warnings; same 84-beat PASS |
| Temporary positive/negative INT32 excursion and recovery | alpha, beta, and gamma covered |
| Terminal positive/negative overflow | each channel covered; atomic zero/fault/no-commit checked |
| Maximum legal reduction | 24 beats / 192 terms covered with bias extremes |
| Reset cancellation | 10 pipeline/output points pass |
| Backpressure | held output stable; three-cycle-stall interval 16 |
| Terminal latency | 9 cycles |
| Non-last accepted interval | 11 cycles |
| Legacy counterexample | two early intermediate faults reproduced |
| Frozen-source strict gate | pass, 0 errors / 0 warnings |
| Candidate strict gate | pass, 0 errors / 0 warnings |

The public strict check matrix is explicit in `COMMANDS_AND_EXITS.md`. Testbench inclusion and optional remote/toolchain checks were not requested by those single-file strict commands; they are not presented as passed checks.

## Remaining risks

- The legal caller obligation is assumed, not enforced in this module.
- Successful last-group commit behavior intentionally remains as in the frozen RTL.
- This candidate changes accumulator semantics but does not improve II, connect the minimum chain, run synthesis/PNR, or establish physical timing.
- The workspace path inspected for this task was not recognized as a Git repository, so no branch or checkpoint commit was available. All evidence is path- and SHA256-based.
