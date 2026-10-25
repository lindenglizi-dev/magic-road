# tb_road_dispatch_publish

Portless integration testbench reusing the previous actual-ROM numerical and table-publication checker. Only fixedMODE1 runs: real7-frame then a normal complete empty frame. The new fixture provides an actual READY-slot claim and225-bit job, whose epoch/task/source/model/capture fields become the frozen publisher start context on the same source edge as job acceptance.

Capture EOF, visibility, safely crossed identity, precomputed12096-cell head stream, NN/task completion proxy and image final-response consumption remain controlled services. Headstream completion triggers a separate controlled last_read fact; NMSdone supplies the task completion proxy. Neither result metadata acceptance nor copy_ack is connected to slot release.

All225job bits, all97bits of each output/active entry and all265metadata bits are checked. Complete empty count0 clears the previous7-box table at the next normalSOF. Time source is the unchanged real road_time_snapshot,100MHz source/75MHz-average destination and1237500-cycle normalSOF with explicit arbitrary phase. Existing disjoint start→meta→ack→active intervals and contained waits remain the measured boundary, not fullcamera/NN/DDR/FPS evidence.

Timing: READY claim→job/publisher start→controlledHEAD112stream→controlledlastresponse consumption frees input slot while task remains busy→NMSdone→publisher metadata→C8copy_ack→laterSOFactive. The selected phase observes ack before active; no universal CDC ordering is asserted.

[Dispatch timing](dispatch_timing.svg) illustrates the controlled input-owner portion; output publication follows the frozen publisher contract.
