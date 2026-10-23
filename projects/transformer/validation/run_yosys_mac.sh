#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../lesson14_transformer_full"
if ! command -v yosys >/dev/null 2>&1; then
  echo "SKIP: Yosys not installed. No PPA claim." >&2
  exit 2
fi
# Yosys with yosys-slang plugin for modern SV; actual ASIC PPA requires IHP PDK and constraints.
yosys -m slang -p 'read_slang rtl/mac_array_4x4.sv; hierarchy -check -top mac_array_4x4; proc; opt; synth -top mac_array_4x4; stat' | tee ../reports/mac_generic_synth.log
