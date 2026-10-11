# Isolated 720p video template

This is the preserved camera/ISP/DDR/HDMI foundation, with the old road-analysis
branch removed. It does not contain RoadYOLO, a CNN placeholder, training weights,
new DDR arbitration, or deployment-ready detections.

The only copied RTL is design_top_wrapper.v. source_manifest.json records 52
direct common/IP/constraint references and SHA256 hashes. IP descriptors resolve
their original child sources in place; IP trees and video data were not copied.
Production top and TD project hashes were checked unchanged after this build.

Run from cnn/template/output:

```powershell
& 'E:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/bin/td_commands_prompt.exe' '../run_template.tcl'
```

The TD project file is output/cnn_video_template.al, using absolute workspace
paths. Keep that file when retaining the build recipe. The run script uses
paths relative to its required output working directory. A failed TD command can
still return process exit code 0; inspect the tool log and final reports.

Actual 2026-10-02 routed result: 9,865 LUT6, 12,358 Slice, 13,313 Slice registers,
40 ERAM20K and 8 DSP. SWNS +1.408 ns, HWNS +0.020 ns, both total negative slacks
zero; STA coverage 95.64%. Thus arithmetic headroom is 68 ERAM and 32 DSP before
new CNN logic, memory port replication, routing and timing. No board FPS claim.

Strict skill gate did not pass: 1,091 reported errors, including inherited port
normalization failure, naming/style and comments. Read output/strict_gate.json
and .md. Its compile/AST failure is a formatter-contract result, separate from
successful real TD elaboration and routing. Existing IP undriven-net warnings
remain in the TD log. No broad legacy reformat or production repair was made.

See verification_receipt.json for evidence, design_top_wrapper_spec.md for the
template contract, and ../spec/integration_contract.md for future CNN boundaries.
The latter documents the unresolved DDR bridge handshake defects and live-video
versus delayed-detection semantics; template route does not approve those issues.

