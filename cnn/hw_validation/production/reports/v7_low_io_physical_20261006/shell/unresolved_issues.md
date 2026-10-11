# Open items and measurement boundaries

1. TD synthesis, placement, routing, physical timing, and resource reports are pending in the separately approved physical run.
2. The shell strict delivery gate remains failed with 667 errors. The explicitly included TB gate remains failed with 219 errors. The frozen chain's prior 374 diagnostics remain open.
3. Static source closure is incomplete in the shell-only strict invocation, so some child-driven signals are reported as unconfirmed. This is not silently classified as a false positive.
4. The fixed requant coefficients may be legally folded by synthesis. The physical result therefore does not represent the cost of a generic dynamic multiplier.
5. Two official PH1P ERAM-model `INIT_FILE` range warnings remain in the passing simulation log.
6. The `spec/spec/low_io_physical/` duplicate is obsolete output-routing evidence. The authoritative path is `spec/low_io_physical/`.
7. The shell permits one RUN per reset by design. Reuse without reset would require a frozen-chain cache-valid contract change and is outside this stage.
8. No board test, production integration, deployment bitstream, training, or Flash write was performed.
