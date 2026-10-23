#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
if ! command -v iverilog >/dev/null; then echo "RTL_UNVERIFIED: iverilog not installed";exit 2;fi
mkdir -p reports
iverilog -g2012 -s tb_croc_gemm_obi_stress -o reports/stress.vvp \
  tb/croc_pkg_stub.sv rtl/mac_array_4x4.sv rtl/gemm_mmio_4x4.sv \
  rtl/croc_gemm_obi.sv tb/tb_croc_gemm_obi_stress.sv
vvp reports/stress.vvp | tee reports/stress.log
grep -q '^PASS STRESS:' reports/stress.log
