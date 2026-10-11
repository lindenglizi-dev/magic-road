# road_round_internal_probe codegen plan

1. Reuse `production/round/reference.py::expected` to freeze deterministic PRBS products, shifts, tags, validity, expected results and checksum.
2. Stage `production/round/road_round_shift.v` byte-for-byte under `rtl/` and bind both hashes.
3. Add one source register boundary, the canonical common-stall RNE, one observable result boundary and a separate checksum boundary.
4. Allow asynchronous timing treatment only from top `i_rstn` to `road_round_reset_gen_Inst_release.reg_reset_meta` and `reg_reset_release`; do not exempt `reg_reset_release`, `wire_core_rstn`, the RNE, source, sink or checksum reset paths.
5. Check every generated payload and every result in Icarus, including reset cancellation and stall holds, then run the strict directory gate over the complete two-source RTL closure.

The eight public gates are compile, ast, readability, comment, naming, profile, testbench and toolchain. Local simulation proves only this component fixture.
