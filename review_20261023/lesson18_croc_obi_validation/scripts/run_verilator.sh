#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
if ! command -v verilator >/dev/null; then echo 'RTL_UNVERIFIED: missing verilator'; exit 2; fi
mkdir -p reports
verilator --binary --timing --assert -Wno-fatal --top-module tb_croc_gemm_obi \
 --Mdir reports/obj_obi_gemm tb/croc_pkg_stub.sv rtl/mac_array_4x4.sv \
 rtl/gemm_mmio_4x4.sv rtl/croc_gemm_obi.sv tb/tb_croc_gemm_obi.sv
reports/obj_obi_gemm/Vtb_croc_gemm_obi | tee reports/verilator_sim.log
grep -q '^PASS OBI GEMM' reports/verilator_sim.log
