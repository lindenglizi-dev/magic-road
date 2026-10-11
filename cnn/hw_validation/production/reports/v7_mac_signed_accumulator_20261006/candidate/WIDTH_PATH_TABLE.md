# Signed accumulator width path

The table follows one output channel. Alpha, beta, and gamma use the same widths. Packed three-channel state uses alpha in the least-significant lane.

| Stage or object | Per-channel width | Packed width | Signed interpretation | Preserved bits / rule |
| --- | ---: | ---: | --- | --- |
| Activation | 8 | 64 for eight lanes | signed INT8 | One byte per lane |
| Weight | 8 | 192 for three groups of eight | signed INT8 | One byte per lane and output |
| Product register | 16 | 384 internal bank | signed | Exact INT8 multiplication, range -16256 to 16384 |
| Pair register | 17 | 204 internal bank | signed | Exact sum of two products |
| Quad register | 18 | 108 internal bank | signed | Exact sum of four products |
| Dot register | 19 | 57 internal bank | signed | Exact sum of eight products |
| Bias input lane | 32 | 96 | signed INT32 | Each lane is sign-extended independently before packing |
| Bias / history base | 33 | 99 | signed | alpha `[32:0]`, beta `[65:33]`, gamma `[98:66]` |
| Base product / pair / quad / dot pipeline | 33 | 99 each | signed | Bit 32 is retained through every alignment register |
| Extended dot operand | 33 | three independent wires | signed | The 19-bit dot is sign-extended to 33 bits |
| Candidate combinational sum | 34 | three independent wires | signed | `signed33 + signed33`; the carry/sign extension is retained |
| Candidate / hold / final pipeline | 34 | three independent registers per stage | signed | Bits `[33:0]` remain intact to the aligned decision stage |
| Terminal INT32 test | 34 | three flags | signed | Overflow when bit 33 or bit 32 differs from bit 31 |
| Writeback buffer | 33 | 99 | signed | Candidate `[32:0]` is packed; bit 32 is not discarded |
| Cross-group accumulator | 33 | 99 | signed | Legal reductions remain inside signed33 by the frozen proof |
| Fault-safe visible lane | 32 | 96 | signed INT32 | Only terminal success exposes candidate `[31:0]`; any terminal lane fault forces all lanes to zero |

## Range basis

- Frozen graph closure: 67 layers.
- Maximum legal reduction: 192 active INT8 products, at most 24 accepted eight-lane beats.
- Product range: `[-16256, 16384]`.
- Bias plus every legal prefix: `[-2150604800, 2150629375]`.
- Signed33 storage range: `[-4294967296, 4294967295]`.

The proof is conditional on the caller beginning a reduction with `first`, ending it with `last`, and never exceeding 24 beats / 192 active terms. Unbounded malformed streams are not proved and no counter or interface was added.

## Alignment

| Accepted-edge offset | Relevant state |
| ---: | --- |
| 0 | Front payload, `first`, and `last` are accepted |
| 1 | Products and the selected signed33 base enter their pipelines |
| 2 | Pair sums |
| 3 | Quad sums |
| 4 | Dot sums and aligned base |
| 5 | Signed34 candidate sum is registered |
| 6 | Candidate hold and per-lane INT32 facts are registered |
| 7 | Candidate final, `flag_last`, and last-gated overflow summary align |
| 8 | Signed33 writeback buffer, fault-safe visible data, and terminal/commit events align |
| 9 | Terminal result becomes valid; successful candidate commits |

No pipeline stage was added. Simulation retained terminal latency 9, non-last accepted interval 11, and the existing three-cycle-stall terminal interval 16.
