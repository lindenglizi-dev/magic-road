# Lesson 18 — Croc OBI verification gate and baseline prep

Based on Lesson 17. One outstanding OBI register slave, **not yet verified on the complete Croc SoC**.

Run `python scripts/validate.py --strict` from this directory on Windows or Linux.
`bash scripts/validate.sh --strict` forwards to the same Python entry point.
Exit 0 means all standalone RTL tests really passed; exit 2 means simulator
unavailable; exit 1 means failed or timed out. `reports/summary.json` is the
latest gate result; skipped stages never count as PASS. Both compilation and
simulation have bounded timeouts, and each stage records its command and exit code.

Independent model: `python3 reference/obi_reference.py`. Pinned Croc baseline methodology: `docs/lesson18_checks.md`.

The standalone TB uses `tb/croc_pkg_stub.sv` and is not equivalent to running the official Croc simulation. Integration instructions/patch remain in `scripts/integrate_into_croc.py`.

Use `scripts/capture_baseline.sh /path/to/croc /path/to/report_dir` to record provenance. This does **not** perform synthesis.

Functional coverage includes two consecutive jobs without reset, an identity
case and a non-identity signed INT8 extreme case, with all 32 results checked
against a scalar GEMM calculation. Protocol stress checks held requests, IDs,
invalid accesses, busy writes, and equal accepted/returned transaction counts.
See `docs/croc_gemm_obi_spec.md` for the preserved interface/timing contract.
