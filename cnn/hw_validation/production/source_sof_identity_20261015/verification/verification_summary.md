# Source SOF identity and age overlay digital verification

Final runs: `identity_attempt2/receipt.json` and `overlay_attempt3/receipt.json`.
Command: `D:/Python313/python.exe -B -X utf8 verify.py all`, from this candidate root, with permission to launch the installed local ModelSim tools.
Each attempt retains input snapshots, SHA256 source/tool closure, commands, compile logs, simulator logs and receipt. Before/after frozen-dependency checks reported 12 checked, no changes. Both final compiles and simulations reported zero errors and zero warnings.

## Identity

The frozen read-only `detection_table_cdc_20261015/rtl/road_time_snapshot.v` supplies the sole absolute millisecond counter and actual millisecond tick at 100 MHz. The camera domain runs at nominal 60 MHz. The simulation ran 15.101782638 ms; stimulated SOF intervals are adversarial test intervals, not a camera frame-rate measurement.

- 9 admitted descriptors, 7 actual destination accepts, 2 events intentionally cancelled by common reset, and 10 skipped source SOFs.
- Observed AWB SOF edges count without credit, before first time, during stale time and while an event is busy. A high SOF across reset creates no phantom frame; a held high SOF counts once.
- A mirror completing on the first SOF is ineligible; a later simultaneous mirror/SOF uses the previously completed mirror. Source admission tuple is checked before the sampling edge and descriptor transfers match that tuple exactly.
- 100014 valid-stalled destination edges; descriptor and held128 payload remain unchanged until actual ready-valid accept. Event ACK may change only on that accept. Event backpressure spans a real millisecond mirror update and cannot stop the independent time channel.
- 110087 held96 edges and 60042 held128 edges checked against their returned two-stage ACK hold rules. Published held96 equals the sampled external epoch/time; completed camera mirror equals that atomic frozen payload.
- Exact expiry on the 120001st camera edge without a completed new snapshot, with valid retained through edge120000; publication and time-clock restart both resume valid operation.
- Common reset cancels a pending mirror, a descriptor pending-copy phase and a held valid descriptor, resets the upstream time, and restarts identity under a new epoch.
- Explicitly labelled ARTIFICIAL STATE FORCING reaches uint32 counter wrap: last ID admitted once, subsequent SOFs saturate and set sticky fault, common reset clears it. This is a boundary-state test, not four billion observed source frames.

| Measured endpoint | Final value |
| --- | ---: |
| SOF admission to descriptor valid, maximum | 39.959 ns |
| Descriptor valid to actual accept, maximum intentional stall | 1000140.000 ns |
| Actual accept to event busy deassertion, maximum | 23.347 ns |
| Continuous source publication to completed mirror copy, maximum | 63.391 ns / 4 camera edges |
| Continuous valid mirror lag versus actual absolute time, maximum | 1 ms |
| Camera-stop queued publication to mirror copy, separate fault case | 1100222.663 ns |
| Time-clock stop test duration | 120010 camera edges |
| Publication-stop watchdog expiry | 120001 camera edges |

Endpoint maxima cover this deterministic clock phasing and stimulus. Camera-clock stop also stops the watchdog and therefore does not prove bounded freshness; the separate stopped-clock result is not included in the continuous-clock maximum.

## Overlay

16 frames, 87040 full active-pixel comparisons against `reference.py` golden pixels: 9508 white glyph pixels and 77532 transparent/pass-through pixels. All 132x16 text pixels, cell padding and surrounding pixels are checked. Numeric cases include 0, 1996, 1997, 2000, 2001, 9999, plus every decimal digit; 10000 and UINT64_MAX render `AGE_INVALID`.

The test models an active-table switch on SOF using actual nonblocking assignment ordering. It verifies capture at the first following blank edge, stable text despite midframe age changes, numeric finite age for an initially empty table with draw=0, 16 immediate live draw-disable checks, and 87616 registered RGB/VS/HS/DE alignment checks at nominal 75 MHz.

## Retained earlier attempts and limits

`overlay/` retains the sandbox WinError623 process-start failure before ModelSim compilation. `overlay_attempt2/` and `identity/` retain earlier passing source/test closures. Final passing attempts were fresh directories; none of these earlier reports were overwritten.

These tests cover the existing reconstructed AWB SOF marker, not guaranteed one-to-one sensor exposure or CSI short-packet frame identity. The active-bank timing stimulus is a testbench model, not an instantiated detection-table integration. No pixel DMA/credit-slot association, real DDR late-return drain, physical CDC/MTBF or bundled-bus timing signoff, production integration, TD, bitstream, board, training or Flash evidence is claimed. Strict generated-deliverable gates are separate coordinator-owned evidence.
