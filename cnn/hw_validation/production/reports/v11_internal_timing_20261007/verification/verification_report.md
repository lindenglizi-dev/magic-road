# v11 internal timing repair verification

## Outcome

The exact v11 RTL candidate passed the independent Python reference, standalone protocol stress, four same-vector DW/PW runner cases, and every freshly rerun legacy regression. The repair adds one elastic product/shift/tag register before the unchanged pre-round core. Numeric results and scalar II=1 are unchanged; accepted-scalar latency is one cycle longer.

Authoritative RTL hashes:

- `road_postprocess_stream.v`: `a51590f53c62f3a6dc51eaded0c77301b692f0cf2ae95109bd1e73afb29193fb`
- `down2_overlap_tile_runner.v`: `c2d8e603855600d6c09579f285ff8a3f62d82f8c7509634dcc66786c3ad99405`

The frozen-prior guard remained unchanged over 4,686 files; manifest SHA-256 is `7fa8cc8baa1cdd5451ae4eb3fa9953f36e6e46b5da4af97209bf1fd899616bb7`.

## New pipeline evidence

The standalone ModelSim test passed continuous traffic, fixed bubbles, fixed-seed random input gaps, random output-ready stalls, two long backpressure windows, full queue occupancy, table partial-load and held-reload fencing, coefficient/lane switching, terminal fault, and every reset age 1 through 25. The final test additionally asserts that the new cut's product, shift, tag, and valid remain stable whenever the downstream pre-round pipeline cannot advance.

- Latency: scalar accepted at edge `t`, output valid after the `t+24` NBA update, first possible transfer/write at edge `t+25`.
- Empty-pipeline pressure: 10 groups / 30 scalars accepted, final denial held 43 cycles, last accepted group 28 edges after ready withdrawal.
- Existing-tail pressure: 7 groups / 21 new scalars accepted, final denial held 52 cycles, last accepted group 19 edges after ready withdrawal.
- Observed maxima: group queue 2, pre cut+round 10, SiLU metadata 6, post round 9, scalar obligations 30.
- The structural safe obligation upper bound is 31. Neither the Python directed cases nor RTL stress is represented as having observed 31.

The Python fatal-fault model deletes externally masked old tokens for compact reasoning. Frozen RTL subcores may retain internal register bits until reset; the verified contract is no externally visible old output, no new admission, then external reset and full table reload. Likewise, reservation-aware global emptiness is a composed-runner property, not a standalone-wrapper port.

## Same-vector runner evidence

All four DW/PW cases passed all 640 accumulator, pre-round, SiLU, post-round, and writeback comparisons. Credit remained at most two. The random commit-ready case introduced 1,301 stall cycles without loss, duplication, or value/tag mismatch.

The no-stall endpoint moved from v10's 5,431 cycles to 5,433 cycles. Measured layer endpoints moved by one cycle each: DW 3,611 to 3,612 and PW 1,820 to 1,821. MAC state time stayed 5,376 cycles; the mutually exclusive measured job trace remains 2 `ST_STORAGE` + 2 `ST_MAC_SEND` + 10 `ST_MAC_WAIT` = 14 cycles for G=2. Pre/SiLU/post/writeback busy counters overlap that interval and are not added to it.

## Task-turnaround headroom

Read-only timestamps from two DW and two PW jobs all agreed:

- first group accept to last group accept: 2 cycles;
- last group accept to result acknowledge: 10 cycles;
- result acknowledge to the next job's first group accept: 2 cycles.

The frozen MAC does not reopen ready on the result-ack edge, so a future runner-only next-job prefetch can safely target 2 to 1 cycles, not zero. At one cycle per 3,801,024 jobs, that is a conditional 3,801,024-cycle frame saving. Separately, the previously analyzed consecutive-group schedule conditionally saves 9,024,192 cycles. Combining both unimplemented ideas gives 12,825,216 conditional cycles; applying the measured one-cycle tail to 61 active layers leaves an analytical 50,837,370 cycles. This is not implemented, not measured full-frame performance, and not a strict bound.

The next finite experiment should change only next-job first-tuple prefetch. It passes only if DW and PW ack-to-next-first becomes exactly one while the 2/10 group/tail intervals, credit bound, numeric vectors, reset, fault, reload, and backpressure tests remain unchanged.

## Fresh legacy regression matrix

- v9 MAC stream: PASS, 123 vectors, 17 results, 9 faults.
- v9 serial layers: PASS, four cases; DW 11,008 + PW 12,929 = 23,937 cycles.
- v8 layers: PASS, four cases; DW 13,312 + PW 14,081 = 27,393 cycles.
- low-IO shell: PASS, 14 cases.
- reset shell: PASS, 6 cases.
- round core: PASS, 7,042 cases.
- SiLU core: PASS, 65,536 inputs.

ModelSim reported the two known RAM `INIT_FILE` width warnings where that primitive is present; simulations report zero tool errors. The round regression used its frozen Icarus flow and passed.

## Preserved failures and scope

Three pre-RTL Python attempts are retained and document incorrect reachability assertions before the structural-versus-observed distinction was fixed. The first standalone RTL log is also retained: it failed only because two stale v10 testbench checks still rejected the newly proved legal pre occupancy of 10. The corrected assertion reruns pass; the RTL did not change between them.

Physical timing closure is a separate gate. Full-frame numbers exclude DDR, non-convolution work, and NMS, and behavior for G greater than two remains extrapolated rather than measured.
