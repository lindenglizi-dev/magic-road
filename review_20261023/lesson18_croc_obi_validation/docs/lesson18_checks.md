# Lesson 18: OBI protocol acceptance and Croc baseline methodology

## This revision actually changes
- `croc_gemm_obi.sv` now checks the **complete 4 KiB absolute address window**, not just the low 12 bits. Previously a standalone request to `0x2000_2000` could alias CTRL at `0x2000_1000`; actual `user_domain` normally rejects such a request but standalone IP must not assume its caller always decodes correctly.
- Adds `tb_croc_gemm_obi_stress.sv` to hold a second request valid while the first response is in flight, test ID retention and grant recovery, invalid accesses, and busy-time register writes.
- Adds `reference/obi_reference.py` independent Python cycle-based *protocol* model. This is NOT RTL simulation.

## Timing convention
- Cycle N: `req && gnt` accepted on rising edge. The leaf register write commits, or combinational read data is captured.
- Cycle N->N+1: response `rvalid=1`, with `rid=aid` and `err`/`rdata` stable. `gnt=0` while response is presented.
- Next edge: `rvalid` clears and `gnt` resumes; next request is only accepted on a subsequent edge.
- Since `UseRReady=0`, no `rready` channel exists in the selected Croc subordinate type.
- At least 2 cycles between acceptances with this simple adapter; continuous requests incur bubbles. This is correct for a conservative baseline, **not** high-throughput OBI.

## Test split
| Gate | Tool | Pass proves | Not proved |
|---|---|---|---|
| Static | Python | expected files/patch shape | Verilog elaboration |
| Protocol model | Python | independent transfer policy under 1000+ accesses | RTL implements model |
| `run_iverilog.sh` | Icarus | standalone GEMM OBI transactions | real Croc/SoC |
| `run_stress.sh` | Icarus | continuous held request + invalid writes + leaf status | OBI network/CPU integration |
| Croc `gemm_obi_test` | Verilator + RISC-V GCC | CPU→crossbar→user_domain→GEMM | ASIC PPA |
| Croc Yosys baseline & modified | Yosys + PDK | area/path proxy | post-route power & CTS |

## Croc integration
Pin upstream commit `29b2e748e72c592a5a895c2b11fa85bc9080f67a`. Preserve a clean baseline worktree and a separate modified worktree. Run original Hello World **before** modifying anything. Add files with `integrate_into_croc.py`, inspect `git diff`, then regenerate `Bender` file lists. The patch uses genuine `user_design_obi_req` and `user_design_obi_rsp` ports from official `rtl/user_domain.sv`.

## Record for both runs
Croc git SHA and dirty/clean state, tool versions, clock constraints, synthesis cell library, register count, cell area, logic depth, critical path, dynamic/static power methodology. Do not put invented or estimated values in a comparison table. Track CPU-side GEMM instructions/cycles separately from raw MAC cycles (this 4×4 register-MMIO accelerates matrix arithmetic, not necessarily full program latency).
