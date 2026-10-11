# Strict-gate semantic risk review

Status: read-only review of the retained strict reports. This document does not waive, rewrite, or downgrade any gate result. `gates/road_postprocess_stream.json` remains non-deliverable, and the runner/closure formatter-AST parse failures remain blocking coverage gaps until the checker can parse those sources.

## Findings with direct semantic review

### VG122 counter arithmetic

The ten reported expressions are one-step `+ 1'b1` or `- 1'b1` updates. Their safety comes from the handshake invariants, not from silent truncation.

- Result queue, width 2: push requires `o_input_ready`, which requires `Q < 2`; pop requires a valid head, which requires `Q != 0`. The four simultaneous-event cases map `Q=0..2` only to `0..2`. Therefore the reported additions/subtractions at lines 204 and 223 cannot carry out or underflow.
- Pre-round occupancy, width 4: a push is an actual accepted pre-round scalar and a pop is an actual accepted pre-round output. The unchanged round unit has nine enabled register stages. When all nine are occupied, its tail is valid and `flag_pre_advance` permits a new push only with the same-edge SiLU pop. A pop cannot occur when the round output is invalid. Thus `0 <= pre_count <= 9`; lines 300-301 cannot wrap.
- Metadata/SiLU occupancy, width 4: push and pop use actual SiLU input/output handshakes. The unchanged SiLU has six enabled stages, so actual pending metadata is at most six even though the external FIFO has eight entries. A pop requires `cnt_meta != 0`. Thus `0 <= meta_count <= 6`; lines 282-283 cannot wrap.
- Post-round occupancy, width 4: the same nine-stage argument applies to post-round acceptance and final output acceptance. Thus `0 <= post_count <= 9`; lines 305-306 cannot wrap.
- Fault and asynchronous reset have priority over all counter updates and assign zero directly. After a fault, `flag_fatal` blocks new input and output handshakes. Consequently fault/reset cannot create a one-step decrement from zero or preserve a wrapped value.

Conclusion: no counter-overflow semantic bug was found. VG122 remains an explicit-width style blocker in the retained report; the proof above is not a waiver.

### Metadata FIFO pointers and dynamic storage

`cnt_meta_read` and `cnt_meta_write` are three-bit pointers into exactly eight 16-bit entries. Their `+ 1'b1` updates intentionally implement modulo-eight wrap. Every write uses the current write pointer on an actual SiLU input handshake; every read presented to the post-round input uses the current read pointer only when `cnt_meta != 0` and an actual SiLU output handshake is possible.

The count invariant guarantees FIFO order: a metadata item is written before its corresponding read, simultaneous push/pop reads the old head and writes the old tail under nonblocking-assignment semantics, and reset-invalid array contents cannot be observed because reset clears the count and both pointers. The maximum live distance is six, below the eight-entry capacity. `reg_meta_fifo` is a small unpacked memory, not a large packed dynamic lookup.

Conclusion: the three-bit wrap and dynamic RAM access are intentional and bounded. The single-file VG153 `reg_meta_fifo` finding does not recognize the procedural indexed write at line 269; no read-before-write path was found.

### VG125 literal widths

The fourteen literals match the local operand roles:

- `2'd0..2` select a three-lane identity encoded in two bits.
- `5'd0,3,6,9,12,15,18,21` compare against a five-bit channel base.
- The DW bound compares the five-bit `base + zero-extended lane` result with `5'd15`; legal DW inputs have a mathematical maximum of 15, so this expression does not rely on wrap.
- `16'sd127` and `-16'sd128` are signed INT16 comparison limits; `8'sd127` and `-8'sd128` are the exact signed INT8 saturation results.

Conclusion: no mismatched literal semantics were found. VG125 remains present because the checker requires its own declared-width convention.

### VG097/VG153 external drivers and port widths

The single-file run lacks the frozen child definitions, so instance outputs appear undriven and the three instances are inconclusive. The actual connections are width-consistent:

| Child port family | Candidate signal width | Frozen child width |
|---|---:|---:|
| round product | signed 64 | signed 64 |
| round shift | 6 | 6 |
| round input/output tag | 16 | 16 |
| round result data | 16 | 16 |
| round valid/fault/advance | 1 | 1 |
| SiLU table address/data | 10 / signed 16 | 10 / signed 16 |
| SiLU input/output data | signed 16 | signed 16 |
| SiLU ready/valid/loaded/fault | 1 | 1 |

The relevant frozen hashes are MAC `04A8519E0C9E464ADD189EE4EB4C5AC25A6C7C716CE0CA4ADF2F8FBB0FD19B51`, round `CB8F1E308E5832EECC9D5A0CEBB86DF221EA5F12ABE97A5796DC49BEA04B382D`, and SiLU `5F357B493C7B3F941D9FA954A0CE5EC09091E466B641474360D2F64D0E42C938`.

The guarded Verilog-2005 closure compile completed with these exact sources. The physical wrapper also compiled the same functional hierarchy. Those checks support interface binding but do not convert the single-file VG097/VG153 results into passes.

## Runner and closure parse boundary

The strict runner and closure reports failed formatter-AST parsing. Findings derived from incomplete coverage are not treated as evidence of semantic failure or success. In particular, this review does not claim that unparsed naming, comment, source-cone, region, or profile rules pass. They remain listed separately as style/coverage blockers and require checker-compatible parsing or independent structural evidence.

## Behavior evidence relevant to the reviewed invariants

- Guarded Icarus Verilog compile succeeded for runner, postprocess, frozen MAC, frozen round, and frozen SiLU sources. `-Wall` emitted only whole-array `always @(*)` sensitivity notices for the dynamic tile stores.
- The four functional tile cases passed the verifier's second attempt. With the final posedge endpoint convention, the combined no-stall run measured 3611 DW cycles, 1820 PW cycles, and 5431 total core cycles; each scalar-stage endpoint count was 640. The independently started PW-only window measured 1821 cycles because its start/layer boundary differs from the combined run.
- The physical PW-only narrow-shell regression compiled and completed 128 MAC results, 384 scalar writebacks, and 384 indexed exports under backpressure.

These are bounded validation facts, not whole-network, timing-signoff, or gate-waiver claims.

## Review result

No real semantic bug was found in the requested queue, pipeline occupancy, pointer-wrap, metadata storage, reset/fault, or child-port-width items. Remaining strict failures stay visible: explicit-width/style findings, missing-definition findings in the single-file run, and formatter-AST coverage failures for the runner and closure.

