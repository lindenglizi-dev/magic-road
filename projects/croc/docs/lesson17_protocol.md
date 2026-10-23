# Croc OBI Protocol: annotated timeline

Croc source (commit 29b2e74): the User subordinate receives `user_design_obi_req.a` with `addr,we,be,wdata,aid`; the response includes `gnt,rvalid,rdata,rid,err`.

## E0 / E1 / E2
At cycle E0, `req=1`, `gnt=1`. At rising edge E0, request **accepted** and register operation captured. Just after E0, `gnt=0`, `rvalid=1`, response `rid=aid` and `rdata` valid. At rising edge E1, response is retired and `rvalid=0`, `gnt=1`; a new request can be accepted at E2.

A CPU store is complete as an OBI transaction after a response. That does **not** mean GEMM arithmetic finished: CPU must poll STATUS.done. The control write merely starts the `IDLE→CLEAR→RUN` MAC state machine.

## Why `req` is not `rvalid`
`req/gnt` is the address/command acceptance handshake. `rvalid` belongs to a separately registered response. The master must not infer success from `gnt` alone. `aid` must return unchanged as `rid` even through arbitration/multiplexing.

## Why one outstanding transaction
The register leaf's read is combinational and write is clocked; supporting multiple accepted requests would require a FIFO for response data, errors and IDs. A single outstanding adapter is easy to verify, but it deliberately cuts maximum throughput to at most one request per two cycles. It is sufficient for 4×4 MMIO control/transfer, not suitable for bulk model tensors.

## Why partial byte writes are rejected
The existing leaf does not expose `reg_be` and blindly replaces a whole 32-bit A/B word on a write. The adapter responds `err=1` instead of silently corrupting untouched bytes. Later integration can add per-byte write masks to leaf RTL.

## Why address window is only 4 KB
Official `user_pkg.sv` maps UserDesign from 0x20000000 over a huge window by default. We narrow it to 0x20001000–0x20002000 so that other user-domain addresses hit the existing `obi_err_sbr`. This avoids accidental aliases due to the adapter decoding only the low 12 address bits.
