# Lesson 18 — Croc OBI verification gate and baseline prep

Based on Lesson 17. One outstanding OBI register slave, **not yet verified on the complete Croc SoC**.

Run `bash scripts/validate.sh` (exit 0 = standalone RTL tests really passed; exit 2 = simulator unavailable; exit 1 = failed).

Independent model: `python3 reference/obi_reference.py`. Pinned Croc baseline methodology: `docs/lesson18_checks.md`.

The standalone TB uses `tb/croc_pkg_stub.sv` and is not equivalent to running the official Croc simulation. Integration instructions/patch remain in `scripts/integrate_into_croc.py`.

Use `scripts/capture_baseline.sh /path/to/croc /path/to/report_dir` to record provenance. This does **not** perform synthesis.
