#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -ne 2 ]; then echo 'usage: capture_baseline.sh /path/to/croc report_directory';exit 2;fi
repo=$(realpath "$1"); out=$(realpath -m "$2");mkdir -p "$out"
(cd "$repo" && { git rev-parse HEAD; git status --porcelain; }) > "$out/git_state.txt"
for tool in verilator yosys bender openroad; do
  if command -v "$tool" >/dev/null;then "$tool" --version > "$out/${tool}_version.txt" 2>&1 || true
  else echo 'NOT_AVAILABLE' > "$out/${tool}_version.txt";fi
done
printf 'NO SYNTHESIS HAS BEEN RUN BY THIS SCRIPT.\n' > "$out/ppa_status.txt"
echo "Captured provenance to $out. Run the OFFICIAL Croc simulation and synthesis, preserving raw logs, before PPA claims."
