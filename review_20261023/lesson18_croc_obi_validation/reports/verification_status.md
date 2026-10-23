# Lesson 18 — Local verification status

- Python structural/integration script: **PASS** (minimal stand-in Croc template only).
- Python independent OBI handshake model: **PASS**, 1,004 transfers with IDs, validity checks and outstanding accounting.
- Icarus standalone RTL functional test: **NOT RUN**; tool unavailable.
- Icarus standalone RTL stress test: **NOT RUN**; tool unavailable.
- Official Croc CPU RTL simulation: **NOT RUN**; official checkout and tools not available here.
- Yosys synthesis/IHP130 backend: **NOT RUN**; toolchain and PDK not present here.

**No RTL or PPA success is asserted.**

## Reproduction
`bash scripts/validate.sh` returns 0 only when actual standalone RTL sims pass; 2 when HDL tools are missing; 1 on failure.
