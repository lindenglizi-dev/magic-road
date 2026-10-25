R256 static graph and address reference, 2026-10-16

Run from the project directory:
python cnn/hw_validation/production/r256_graph_contract_20261016/graph_reference.py
Standard library only. The script runs the complete assertion self-check before
writing derived files. graph.json, parameter index and candidate JSON are inputs;
their SHA256 hashes, this script hash and Python hash are in the receipt.

Public functions:
build_graph() -> complete 106-node graph, 67 convs, 70 physical allocations.
tensor_shape(graph, name) -> [H,W,C], including split output tensors.
resolve_byte_address(graph, tensor, y, x, c, slot=0) -> first logical byte address.
operator_sample(graph, node/name, y, x, c, slot=0) -> address or explicit fill.
head_address_rows(graph) -> iterator over 21168 field-address dictionaries.
tile_rows(graph) -> iterator over every allocated tensor's physical 4x4 tiles.
self_check(graph, baseline=None, index=None) -> shape/address assertion receipt.
resource_delta(graph, baseline) -> per-allocation and whole-graph static budget.
run() -> self-check, export, return receipt.

Outputs:
graph.json: full frozen topology with propagated R256 input/output/view shapes,
  explicit recursive address rules, newly allocated tile storage, unchanged
  complete parameter_fields (weight/bias/quant offsets, shapes, hashes).
layers.csv: all 67 conv descriptors, MAC, weight offset and new storage bounds.
views.json: all 36 virtual-node descriptors; split has 14 output tensors.
tiles.csv: physical tile base/end, valid row/column counts and 16-bit pixel mask.
head_addresses.csv: all 3024 cells x seven fields in HWC7 stream order.
  packed_byte_offset is an offset in an export/consume stream, NOT a DDR base.
  physical_byte_address is the real tile4x4 reg_out/cls_out storage-view address.
  INT16 bytes are little endian. End addresses are exclusive. Head outputs stay
  virtual reg5+cls2 concatenations; no second full head allocation is introduced.
resource_delta.json: old/new logical, physical tile and 4096-aligned allocations.
self_check_receipt.json: exact coverage, scale boundaries, hashes, limitations.
  run() also requires rejection of old-P4-size/4, modified weight offset, wrong
  MAC count and relocated input slot. Invalid H/W/C coordinates and invalid slot
  IDs are rejected by the complete self-check.

Address semantics:
input: slot_base + ((y*256+x)*3+c), pixel-128 remains a Stem numeric operation.
stored: base + (((y//4)*ceil(W/4)+x//4)*16*C +
                  ((y%4)*4+x%4)*C+c)*bytes_per_element.
split: recurse to source with channel_offset+c.
concat: select the channel segment, recurse to its source and local channel.
nearest: recurse with y//2,x//2; P4 y8 maps to P3 y16 and y17.
residual: alias the branch output; original branch write_transform still requires
  aligned bypass addition and sat8. Address alias is not numerical validation.
conv out-of-logical-image samples fill 0; maxpool samples fill -128; physically
  invalid tile pixels fill 0. Alignment slack is not a logical tensor element.
P4 16x9 uses three tile rows; final row is mask 0x000f, one valid row.

Static results:
Input is 110592B; both original bases and 524288B slot allocations are retained.
Feature allocation is 2011136B (old 7204864B), with no liveness reuse.
Head stream is 42336B; physical tiles 43904B; aligned allocations 57344B.
Cells 0..2303 stride4, 2304..2879 stride8, 2880..3023 stride16.
Weights stay 113100 and MAC is 53616384. P4 physical tile bytes are 30% of old,
not 25%; each tensor is recomputed with ceil, then aligned independently.

Evidence boundary:
This is a byte-address/shape reference, not CNN values, actual DDR visibility,
resource synthesis, timing, board evidence or measured FPS. Unchanged MAC lanes,
ROM and fixed workstores do not shrink merely because input dimensions shrink.
Original DDR address-unit/ownership/visibility release blocks remain in graph.
