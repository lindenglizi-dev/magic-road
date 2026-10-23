# Lesson 18 — Local verification evidence

Use `summary.json` for the latest actual result. Do not infer the current gate
from older logs or existing `.vvp` files. The old "simulator unavailable" note
is superseded: Icarus and vvp are installed on this host.

`python scripts/validate.py --strict` runs structural/integration-fixture checks,
the independent 1,004-transfer Python model, and actual Icarus compilation and
simulation of both standalone TBs. Exit 0 and `gate=RTL_PASS` require every
stage to pass; failed compile prevents running its binary. Unavailable tools,
timeouts and skipped tests cannot pass the gate.

The type stub proves standalone IP behavior only. Official Croc CPU simulation,
synthesis, placement/routing, timing, and PPA are not covered by these tests.

`toolchain_failure_20261023.md` preserves an earlier Windows toolchain failure;
later successful runs, if present, do not erase that diagnostic history.
