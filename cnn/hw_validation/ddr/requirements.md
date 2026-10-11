# H1-B isolated PAXI bridge requirements

## Scope

- Generate one isolated Verilog-2001 bridge, one Python behavior reference, one self-checking testbench, the canonical module spec, and local reports under this directory only.
- Do not edit or instantiate the production bridge, generated DDR IP, top level, parameters, Flash flow, training flow, or TD project.
- The prototype is a controller-facing mock boundary. Passing it does not prove vendor ordering, persistence, capacity, board wiring, or production readiness.

## Confirmed interface contract

- Upstream accepts one request at a time with `valid/ready`, `write`, 32-bit byte address, 128-bit write data, 16-bit high-active write mask, 32-bit epoch, and 32-bit owner.
- Every request is exactly one 16-byte transfer. Legal byte addresses are 16-byte aligned and lie in `[0x03400000, 0x04000000)`.
- The emitted 25-bit PAXI address is `byte_addr >> 1`; no burst-length signal is generated.
- Read address acceptance is only `ARVALID && ARREADY`.
- Write address and write data acceptance are tracked independently using the real `AWREADY` and `WREADY` inputs.
- Write data is buffered before AW is presented. W is first presented in the cycle after AW acceptance, never before AW acceptance, and then held stable until W acceptance.
- The manual's two-clock rule is interpreted as a **presentation deadline**, not an acceptance deadline. W is presented one clock after AW acceptance. WREADY may delay acceptance; whether the vendor permits that delay remains a required vendor clarification.
- `WSTRB` is a high-active mask: `1` means the corresponding byte is masked. The bridge forwards the request mask without inversion.
- A PAXI read return has no READY. Because the bridge permits only one controller request in flight, the accepted read reserves the only return slot before AR issuance.
- `RLAST` must be high on the single expected read beat. A missing RLAST or an unexpected RVALID is a sticky protocol fault and blocks new requests.

## Acceptance, completion, cancel, and reset

- `o_paxi_accepted_valid` is telemetry: for reads it pulses on AR acceptance; for writes it pulses only after both AW and W have accepted. It never means committed.
- A read result is successful only after its attributed one-beat return arrives with RLAST and the upstream accepts the held result.
- A write result is successful only after both AW/W acceptance and a later explicit `i_commit_confirmed` event. Current vendor semantics do not supply this proof, so production must tie this input low until a reviewed controller event exists.
- An early or otherwise unattributed commit confirmation is a sticky protocol fault; the bridge never synthesizes a commit event from AW/W acceptance.
- A global local-cancel input has priority over result publication. Because this prototype is globally single-outstanding, it unambiguously names the sole active owner. Cancellation may stop issue only in the internal check stage before ARVALID/AWVALID is first presented. Once ARVALID or AWVALID has been presented, VALID and address remain stable through READY; the transaction then preserves epoch/owner and drains its attributed read return or write commit event without publishing success.
- `i_commit_confirmed` asserted in the same cycle that W first handshakes is rejected as early. The prototype requires a later cycle so attribution is unambiguous; this is a conservative probe rule, not a claim about undocumented vendor behavior.
- `o_late_discard_count` increments when an attributed return/commit is deliberately discarded after cancellation. No timeout may release the owner or return slot.
- Cancelling a held result is an explicit shared flush exception to ordinary ready/valid stability: the upstream asserts `i_cancel` only when it abandons that result, and the bridge suppresses `o_result_valid` in the same cycle so cancel wins over ready. Without this shared flush contract, cancelling during result backpressure is illegal.
- `o_drain_done` is high only when no request, return reservation, or held result remains.
- `i_rstn` is a coordinated hard reset shared with the mock/controller endpoint. It may clear ownership only because the endpoint is reset at the same time. Local cancellation is not implemented by reset.

## Checkable success

- Python checks cover address bounds/alignment, independent AW/W backpressure, high-active mask stability, cancel before/after acceptance, late-return discard, missing RLAST, unexpected return, and early commit rejection.
- A fixed-seed Verilog testbench checks the same protocol rules plus conservation: accepted controller requests equal successful results plus cancelled drained transactions plus current outstanding ownership.
- The testbench includes cancel coincident with AR acceptance and requires acceptance telemetry/conservation to count that real handshake.
- Canonical spec rendering and the strict generated-deliverable gate run from the installed readable-verilog-generator skill.
- Icarus compile/execute is local external evidence for the isolated mock only. TD, synthesis, encrypted vendor IP, and board tests are out of scope.
