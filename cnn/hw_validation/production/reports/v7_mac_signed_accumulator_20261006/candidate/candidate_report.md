# Signed33 MAC candidate handoff

Assumption: the frozen 67-layer caller obeys `first`/`last` framing and limits a reduction to 24 accepted beats / 192 active terms.

Changed: `road_mac_probe.v` keeps the original module name and ports but widens the three cross-group accumulators, all aligned base registers, and writeback state to signed33. Each candidate is a same-cycle signed33-plus-signed33 to signed34 sum. INT32 overflow becomes terminal-only; any channel's terminal overflow still returns all-zero data, raises fault, and suppresses commit.

Verified:

- Frozen source SHA256: `5DF97DA6910C5673F35807207CC06260FC6ED6EDC7D9313AA2FAC9EC7B3016BE`.
- Candidate SHA256: `F8BF6CACE6EB99BD9B915BE5E27E1D38AF4B3A2485FFEB6E87675D8BFC3478E8`.
- Frozen base 8/8, tail 8/8, and stream 1031/1031 regressions pass without vector edits.
- Signed33 directed suite passes 84 beats / 12 cases, including all three channels' positive and negative temporary INT32 excursions and recovery, eight terminal fault cases, ten reset points, ready-high output, and backpressure.
- Official ModelSim SE-64 2020.4 recompilation and execution of the final source report zero errors/warnings and the same 84-beat PASS.
- Observed accepted intervals are 11, 16, and 25 cycles for the exercised continuation/terminal stall scenarios; terminal result latency remains 9 cycles.
- Strict baseline and final candidate each report `delivery_ready=true`, zero errors, and zero strict warnings. This scope is the one MAC source only; it does not include the testbench, SiLU, or any larger closure.

Remaining risk: malformed reductions beyond the proved bound are not detected locally. This candidate does not improve II, connect the minimum chain, run TD, establish physical timing, or authorize production use.

Detailed evidence:

- `RTL_CLASSIFIER_REPORT.md`
- `WIDTH_PATH_TABLE.md`
- `COMMANDS_AND_EXITS.md`
- `receipt.json`
- `road_mac_probe_signed33.patch`
- `spec/mac/road_mac_probe_spec.md`
