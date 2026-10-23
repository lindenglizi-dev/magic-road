#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
bash scripts/run_python.sh
if ! command -v iverilog >/dev/null; then
  echo 'RTL NOT RUN: iverilog unavailable. Use ModelSim/Questa or install Icarus.' >&2
  exit 2
fi
mkdir -p build
iverilog -g2012 -s tb_transformer_block -o build/transformer_block_sim \
  rtl/mac_array_4x4.sv rtl/tiled_gemm_4x4_banked_compact.sv \
  rtl/requant_shift_sat.sv rtl/ffn_relu_requant.sv \
  rtl/softmax_row_int32.sv rtl/probability_writer.sv \
  rtl/transformer_block_top.sv tb/tb_transformer_block.sv
for CASE in demo edge_5x7 random_00 sat_1x1; do
  echo "=== RTL CASE: $CASE ==="
  vvp build/transformer_block_sim +CASE="vectors/$CASE"
done
