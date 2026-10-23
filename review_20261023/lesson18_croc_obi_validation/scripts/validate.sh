#!/usr/bin/env bash
set -uo pipefail
cd "$(dirname "$0")/.."
mkdir -p reports
python3 scripts/check_structure.py > reports/static.log 2>&1 || { cat reports/static.log; exit 1; }
python3 reference/obi_reference.py > reports/protocol_model.log 2>&1 || { cat reports/protocol_model.log; exit 1; }
if command -v iverilog >/dev/null && command -v vvp >/dev/null; then
  bash scripts/run_iverilog.sh || exit 1
  bash scripts/run_stress.sh || exit 1
  echo 'RTL_SIM_PASS (standalone Croc-type stub, not full SoC)'
else
  echo 'RTL_UNVERIFIED: no iverilog and/or vvp in PATH'
  exit 2
fi
