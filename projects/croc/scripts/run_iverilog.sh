#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
if ! command -v iverilog >/dev/null; then echo 'RTL_UNVERIFIED: missing iverilog'; exit 2; fi
mkdir -p reports
iverilog -g2012 -s tb_croc_gemm_obi -o reports/obi_gemm.vvp \
  tb/croc_pkg_stub.sv rtl/mac_array_4x4.sv rtl/gemm_mmio_4x4.sv \
  rtl/croc_gemm_obi.sv tb/tb_croc_gemm_obi.sv
vvp reports/obi_gemm.vvp | tee reports/rtl_sim.log
grep -q '^PASS OBI GEMM' reports/rtl_sim.log
