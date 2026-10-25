# Shared LUT service verification

This directory owns only the controlled-ROM verification for `road_shared_lut_service`.
It does not instantiate or copy the production ROM. The test-only `physical_words_160.hex`
is regenerated directly from the frozen G10 `numeric_test.bin`, after checking payload
SHA-256 `b35d4a66a69e441dc29bc60c7e3f507661f48da5f33b810d7340f6ed17a65145`.

```powershell
python .\cnn\hw_validation\production\shared_lut_service_1fps_20261015\verification\prepare_vectors.py --check
python .\cnn\hw_validation\production\shared_lut_service_1fps_20261015\verification\run_rtl.py --timeout 180
```

The runner uses only the existing local Icarus/VVP installation. A nonzero compiler
return code is written as `COMPILE_FAILED` and the simulation is not run or counted as
a pass. ModelSim is intentionally not retried for this batch.

Coverage includes every 1024-entry sigmoid and 256-entry exp value and response identity,
an odd-base 19/39 second instance for all lane-19 cross-word reads, request/response
backpressure, cancellation/draining, shared reset, invalid model/range, and reader fault.

`readable-python-generator` and `readable-script-generator` are not installed in this
workspace, so no result claims those gates. The scripts use only the Python standard
library and the existing simulator.
