# RoadYOLO FPGA integration contract

Status: implementation contract for future CNN integration; the separate
`cnn/template/design_top_wrapper.v` implements the video template only.
The production RTL and production TD project are not edited by this stage.
Numerical/model authority is `../contract.json`; this document does not replace
its evolving counts with the older 124,620-weight estimate.

## Fixed boundary

SC500/ISP and HDMI remain 1280x720. Retain the existing video frame ring and
controller configuration. The CNN receives AWB RGB as a nonblocking branch,
resizes to 512x288, and uses independent DDR input slots and feature arena.
All resize, convolution, requantization, activations, decoding, selection and NMS
must execute in FPGA for deployment. A CPU/NPU is not an inference dependency.
The isolated template contains no dummy CNN entity and does not expose future
signals as if implemented.

## Clock domains and pixel order

AWB runs in the camera byte-clock domain (configured about 60 MHz), CNN compute
at 100 MHz, DDR user at about 66.667 MHz, and HDMI pixel at about 75 MHz.
Those are configuration/STA values, not board measurements.
Current HDMI totals 1650x750 imply about 60.606 Hz. Do not silently change PLLs.

The AWB 96-bit beat holds RGB888 pixels. Each pixel has R[23:16], G[15:8], B[7:0].
The current DDR packer consumes the high end of the 96-bit word first, so define
the CNN serialized order as [95:72], [71:48], [47:24], [23:0], matching the
video memory/display path. Confirm physical sensor left-to-right order with
unique-index/ramp and color-bar vectors before accepting data. The legacy gray
adapter's low-lane-first convention is not evidence for this new RGB interface.

The resize kernel maps five source samples to two output samples with integer
numerators (2*p0+2*p1+p2) and (p2+2*p3+2*p4). Apply the same weights vertically;
retain intermediate precision and perform one final division by 25 using the
nearest-even rule in contract.json. Horizontal sums need 11 bits and final sums
13 bits. No letterbox padding is needed at these two 16:9 resolutions.
Four input pixels per camera valid require up to two horizontal outputs per
cycle; a single one-pixel-per-cycle consumer must not be assumed sufficient.
Golden checks must include beat boundaries, line 0/719, pixel 1279, pure RGB,
0/255 values and rounding ties.

## Capture slots, task identity and CDC

Every physical source SOF increments a 32-bit source_frame_id, including skipped
frames. Use a 32-bit epoch changed on coordinated restart; frame wrap must cause
a drained epoch change rather than ambiguous reuse. At SOF atomically choose a
FREE tensor slot or skip the entire frame. No mid-frame admission is permitted.
Camera cannot be stalled. FIFO overflow, malformed dimensions or premature SOF
invalidates that capture; accepted DDR writes still drain before reuse.

Each slot follows FREE -> CAPTURING -> READY -> READING -> FREE.
READY requires exactly 512*288*3 bytes and a proven DDR write-completion or
ordered-write/read-fence event. Being accepted into the request FIFO is not
completion. Release READING only after the final input-memory response has been
consumed and no outstanding request refers to that slot. Full-network done may
occur later. Any feature/input arena alias requires an explicit liveness proof.

Descriptor: epoch[31:0], frame_id[31:0], task_id[31:0], slot[0:0],
byte_base[31:0], payload_bytes[31:0], width=512, height=288, RGB888/NHWC,
resize_id[31:0], model_id[31:0].
For bundled-data toggle CDC, source freezes the entire descriptor before request
toggle and holds it through synchronized acknowledgement. Destination observes
the synchronized toggle, captures a stable payload into owned storage, then
acknowledges capture. Payload acknowledgement does NOT release its tensor bank.
A synchronizer pulse alone never validates a changing multibit bus.

Reset/cancel has priority over successful completion or new task acceptance.
A last response coincident with cancel still retires its reservation/owner;
cancelled tasks never publish success. A one-sided reset invalidates the old
epoch and requires coordinated FIFO/DDR drain before either side advertises FREE.

## DDR client and byte addressing

Keep the original video-ring clients and add one CNN client. The CNN client
internally arbitrates independent tensor-capture writes and compute DMA reads/
writes. All logical addresses are byte addresses. The reserved tentative region
is [0x03400000,0x04000000); input slot bases and arena bounds are in contract.json.
No production DMA may be enabled until physical capacity and address unit pass
controller/board tests. Existing +8 addresses per 128-bit beat suggest 16-bit-word
addressing, but byte_address>>1 remains unverified at this boundary.

The front-end request descriptor is held stable with req_valid until req_ready:
{client_id, epoch, task_id, op, byte_addr, beat_count, return_owner}.
For writes, reserve command and write-data capacity atomically; ordered write
data is held until its own data-valid/data-ready acceptance. At the controller:
- Read address: AR accepted only on ARVALID && ARREADY; hold address otherwise.
- Write address: AW accepted only on AWVALID && AWREADY; latch aw_accepted.
- Write data: W accepted only on WVALID && WREADY; latch each accepted beat,
  preserving WLAST/mask. AW and W may accept independently and in either order.
- Do not pop a write transaction until its address and all its data are accepted.
  Acceptance is not persistence/completion. Define commit/fence from documented
  PAXI behavior and verify it; do not invent an AXI B response absent from the IP.
- Do not use (ARREADY || AWREADY) to decide acceptance of a particular operation.
- Expose RLAST or prove the configured exact beats-per-command before use.
  Every accepted read creates an owner entry and reserves all expected beats.
  No-READY user returns must always find capacity or be explicitly discarded
  with their owner still known.

For each response buffer, occupied + reserved <= depth. Accepted requests add
reserved; each incoming beat removes exactly one reserved unit and either adds
occupied or is deliberately discarded for a cancelled owner. Ownership remains
until the last attributed response is processed. Cancellation stops issuing new
requests but retains outstanding owners/reservations. Reset cannot erase counters
while the controller may still return old data. No fixed timeout implies drain.

Select FIFO watermarks to protect HDMI underrun/camera overflow; bound CNN service
to measure rather than assume minimum detector FPS. Keep counters for issued/
accepted/completed bytes, max reserved, starvation, input skips, age and overflow.
A low average bandwidth estimate is not proof of worst-case scheduling.

## Immutable numeric storage

PH1P primitive library documents 1/2/5/10/20/40-bit physical widths; 40-bit requires
PDP20K rather than a two-independent-reader true dual port. Build a physical ROM
group as four 40x512 ERAMs at the same word address: one 160-bit word is 20 bytes,
512 words are 10,240 bytes. A logical 128-bit reader must use a gearbox or gather
adjacent physical words. Do not index a 160-bit word as if it were 16 bytes.
Layer offsets are byte offsets; unaligned tails and group crossings must be
explicit in the immutable manifest. INIT_FILE (.dat/.dath) embeds data in the
bitstream; verify the exact initialization file format, physical bit order and
post-synthesis initialized bytes. Flash user-read bootloading is not assumed.

Store folded INT8 per-channel weights, INT32 biases, requant multipliers/shifts
and shared activation tables once. The current contract uses an INT16 Q7.8
pre-SiLU quantization and a separate per-layer INT8 output requantization: QAT
must model BOTH stages and the actual shared-table endpoint/tail/rounding rules.
Do not replace that contract by a separate 256-entry LUT for each of 61 layers.
Read current contract.json for 1024-entry stored tables plus hardwired endpoints;
older planning text describing 1025 stored entries is superseded.

Shared ROM bandwidth is finite. Concurrent convolution-weight and LUT accesses
must be scheduled or use an explicitly budgeted small active table/cache.
Four 40-bit ROM slices do not provide a free second 160-bit read port.
Full activations/skip tensors remain in DDR, with only bounded tiles and INT32
partial sums on-chip. Resource arithmetic is an estimate until complete mapping.
A 24-MAC engine at 100 MHz does not imply every convolution sustains 24 MAC/cycle.

## Future output interface (contract only, not instantiated)

One frame-result stream in the compute domain:
result_valid/result_ready; epoch[31:0], task_id[31:0], source_frame_id[31:0],
model_id[31:0], box_count[6:0], result_status[1:0], capture_timestamp[63:0],
completion_timestamp[63:0]. Status 0=valid result (including valid empty result),
1=cancelled, 2=input/compute/memory fault, 3=reserved.
Once valid, all metadata stays stable until ready. Accepting metadata initiates
a stable table transfer; it does not declare the table fully copied.

The associated table contains up to the contract's per-class maximum (currently
32 per class, 64 total), valid entries in deterministic NMS order with
class_id[0:0], score_q16[15:0], source x1/x2/y1/y2 in unsigned Q12.8 [19:0].
Coordinates use continuous half-open xyxy and clip to 1280x720, after exact
network-coordinate scaling by 5/2. Class confidence is a calibrated arithmetic
output, not an empirical correctness probability. Table-read request and response
each have independent valid/ready; one outstanding read is sufficient initially.
Keep result table stable until an explicit table_copy_ack after the final entry
response acceptance. For an empty result, metadata acceptance plus zero count
permits copy acknowledgement. Reject early ack. No partial table becomes active.

Transfer result metadata/table to a pending HDMI-domain buffer with the same
hold/capture/ack discipline. Only HDMI SOF exchanges pending and active tables;
active entries remain immutable for the whole display frame. Age uses a shared
timebase with explicit CDC, not subtraction of unrelated domain counters.
The contract age limit is 500 ms. Results from wrong epoch/model or beyond age
limit are not treated as current detections; expose degraded/invalid state.

This independent-tensor design overlays latest detections on live video, NOT
strictly the source camera frame. Preserve source identity/age visibly in debug
telemetry. Strict same-frame overlay requires a separate authorized video-ring
ownership/delay design. Existing track_snapshot_cdc lacks source_frame_id/ack/
SOF gating and cannot establish the new result contract by itself.

## Existing bridge findings; unchanged in this stage

- mc_to_user_interface.v:46-58 pops a shared FIFO from I_mc_app_rdy and
  I_mc_app_wdf_rdy. The wrapper combines ARREADY/AWREADY and reports AWREADY as
  write-data-ready. Independent AR/AW/W backpressure can therefore misattribute
  acceptance or drop a command/data beat.
- ph1p35_ddr/ph1p35_324_ddr_wrapper.v:69-76,96-103 connects real WREADY but does
  not use it in the upstream ready; RREADY is tied high and RLAST is not forwarded.
  O_mc_app_rd_data_end is declared but undriven.
- video_in.v:106-138 advances original ring pointers without CNN ownership.
  This contract deliberately avoids using those banks as CNN tensor slots.
- track_snapshot_cdc.v:77-84 updates immediately after a toggle, not at HDMI SOF.

These are source-backed defects/limitations requiring later isolated repair and
backpressure simulation before third-client production integration. Template
synthesis does not prove their protocol behavior safe.

## Acceptance sequence

1. Isolated template elaboration/route and nonmutation receipt.
2. RGB resize bit-exact vectors; 160-bit ROM mapping/init; independent DDR
   handshake, split AW/W acceptance, return ownership, epoch/cancel/late-response
   and FIFO-reservation tests.
3. Layer intermediate equality against integer.py, then full CNN plus decode/NMS.
4. Integrated resource/STA evidence including coverage; continuous camera/HDMI
   board test with dropped frames, FIFO peaks and frame age.
5. Frozen trained model, scene-isolated metrics and user-selected precision/
   recall/FPS gates. Architecture counts or template route do not pass these.

