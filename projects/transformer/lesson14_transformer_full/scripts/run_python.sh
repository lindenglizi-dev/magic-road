#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 reference/verify_full_block.py
python3 reference/static_contracts.py
