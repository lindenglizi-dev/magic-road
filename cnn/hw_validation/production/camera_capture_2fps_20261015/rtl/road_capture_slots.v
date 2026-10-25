//==============================================================================
// Module: road_capture_slots
// Description: 完整帧双槽管理 / Complete-frame double-slot ownership.
// Reset cancels local state; caller must drain real DDR before generation reuse.
//==============================================================================
module road_capture_slots (
    input wire i_clk,
    input wire i_rstn,
    input wire i_sof,
    input wire [31:0] i_epoch,
    input wire [31:0] i_frame_id,
    input wire [63:0] i_timestamp,
    input wire i_capture_end,
    input wire [18:0] i_capture_bytes,
    input wire i_frame_error,
    input wire i_write_visible,
    input wire i_visible_slot,
    input wire [31:0] i_visible_epoch,
    input wire [31:0] i_visible_frame_id,
    input wire i_read_claim_valid,
    input wire i_read_claim_slot,
    input wire [31:0] i_read_claim_epoch,
    input wire [31:0] i_read_claim_frame_id,
    input wire i_last_read_consumed,
    input wire i_release_slot,
    input wire [31:0] i_release_epoch,
    input wire [31:0] i_release_frame_id,
    output wire o_claim_ready,
    output wire o_capture_active,
    output wire o_capture_slot,
    output wire [31:0] o_capture_base,
    output wire o_capture_accepted,
    output wire o_frame_skipped,
    output wire [1:0] o_free_mask,
    output wire [1:0] o_ready_mask,
    output wire [1:0] o_reading_mask,
    output wire [1:0] o_quarantine_mask,
    output wire [63:0] o_slot_epochs,
    output wire [63:0] o_slot_frame_ids,
    output wire [127:0] o_slot_timestamps,
    output wire o_protocol_error
);
    // Slot-state encoding; quarantine has no automatic reuse path.
    localparam [2:0] FREE = 3'd0;
    localparam [2:0] CAPTURING = 3'd1;
    localparam [2:0] WAIT_VISIBLE = 3'd2;
    localparam [2:0] READY = 3'd3;
    localparam [2:0] READING = 3'd4;
    localparam [2:0] QUARANTINE = 3'd5;

    // Pre-edge ownership masks prevent allocation from bypassing a release.
    wire [1:0] capture_mask;
    wire [1:0] visible_accept;
    wire [1:0] release_accept;
    wire [1:0] claim_match;
    wire capture_present;
    wire free_present;
    wire allocate;
    wire allocate_slot;
    wire end_good;
    reg capture_slot_o;
    reg capture_accepted_o;
    reg frame_skipped_o;
    reg protocol_error_o;
    genvar bank;

    // Outputs are meaningful only when their corresponding owner is active.
    assign capture_present = |capture_mask;
    assign free_present = |o_free_mask;
    assign allocate = i_sof && !capture_present && free_present;
    assign allocate_slot = !o_free_mask[0];
    assign end_good = i_capture_end && (i_capture_bytes == 19'd442368)
                    && !i_frame_error && !i_sof;
    assign o_capture_active = i_rstn && capture_present;
    assign o_capture_slot = capture_slot_o;
    assign o_capture_base = capture_slot_o ? 32'd55050240 : 32'd54525952;
    assign o_claim_ready = i_rstn && claim_match[i_read_claim_slot];
    assign o_capture_accepted = capture_accepted_o;
    assign o_frame_skipped = frame_skipped_o;
    assign o_protocol_error = protocol_error_o;

    // Each bank has independent state and metadata; unrelated events are retained.
    generate
        for (bank = 0; bank < 2; bank = bank + 1) begin : slot_bank
            reg [2:0] state_current;
            reg [2:0] state_next;
            reg [31:0] epoch_store;
            reg [31:0] frame_store;
            reg [63:0] timestamp_store;
            wire visible_identity;
            wire release_identity;
            wire claim_identity;
            wire visible_eligible;

            // Identity checks prevent stale completion from publishing a new frame.
            assign visible_identity = (i_visible_epoch == epoch_store)
                                    && (i_visible_frame_id == frame_store);
            assign release_identity = (i_release_epoch == epoch_store)
                                    && (i_release_frame_id == frame_store);
            assign claim_identity = (i_read_claim_epoch == epoch_store)
                                  && (i_read_claim_frame_id == frame_store);
            assign visible_eligible = (state_current == WAIT_VISIBLE)
                                    || ((state_current == CAPTURING) && end_good);
            assign visible_accept[bank] = i_write_visible && (i_visible_slot == bank)
                                         && visible_identity && visible_eligible;
            assign release_accept[bank] = i_last_read_consumed && (i_release_slot == bank)
                                         && release_identity && (state_current == READING);
            assign claim_match[bank] = claim_identity && (state_current == READY);
            assign capture_mask[bank] = (state_current == CAPTURING);
            assign o_free_mask[bank] = (state_current == FREE);
            assign o_ready_mask[bank] = (state_current == READY);
            assign o_reading_mask[bank] = (state_current == READING);
            assign o_quarantine_mask[bank] = (state_current == QUARANTINE);
            assign o_slot_epochs[bank*32 +: 32] = epoch_store;
            assign o_slot_frame_ids[bank*32 +: 32] = frame_store;
            assign o_slot_timestamps[bank*64 +: 64] = timestamp_store;

            // State register: asynchronous local cancellation.
            always @(posedge i_clk or negedge i_rstn) begin
                if (!i_rstn)
                    state_current <= FREE;
                else
                    state_current <= state_next;
            end

            // Transition process: only complete visible frames can become READY.
            always @(*) begin
                state_next = state_current;
                case (state_current)
                    FREE: begin
                        if (allocate && (allocate_slot == bank))
                            state_next = CAPTURING;
                    end
                    CAPTURING: begin
                        if (i_sof || i_frame_error)
                            state_next = QUARANTINE;
                        else if (i_capture_end) begin
                            if (!end_good)
                                state_next = QUARANTINE;
                            else if (visible_accept[bank])
                                state_next = READY;
                            else
                                state_next = WAIT_VISIBLE;
                        end
                    end
                    WAIT_VISIBLE: begin
                        if (visible_accept[bank])
                            state_next = READY;
                    end
                    READY: begin
                        if (i_read_claim_valid && (i_read_claim_slot == bank)
                            && claim_match[bank])
                            state_next = READING;
                    end
                    READING: begin
                        if (release_accept[bank])
                            state_next = FREE;
                    end
                    QUARANTINE: state_next = QUARANTINE;
                    default: state_next = QUARANTINE;
                endcase
            end

            // State task process: metadata changes only on a fresh allocation.
            always @(posedge i_clk or negedge i_rstn) begin
                if (!i_rstn) begin
                    epoch_store <= 32'd0;
                    frame_store <= 32'd0;
                    timestamp_store <= 64'd0;
                end else if (allocate && (allocate_slot == bank)) begin
                    epoch_store <= i_epoch;
                    frame_store <= i_frame_id;
                    timestamp_store <= i_timestamp;
                end
            end
        end
    endgenerate

    // Acceptance and skip pulses are mutually exclusive and last one cycle.
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) begin
            capture_slot_o <= 1'b0;
            capture_accepted_o <= 1'b0;
            frame_skipped_o <= 1'b0;
        end else begin
            capture_accepted_o <= allocate;
            frame_skipped_o <= i_sof && !allocate;
            if (allocate)
                capture_slot_o <= allocate_slot;
        end
    end

    // Bad events are sticky diagnostics, not permission to reuse another slot.
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn)
            protocol_error_o <= 1'b0;
        else if ((i_sof && capture_present)
                 || (capture_present && i_frame_error)
                 || (i_capture_end && (!capture_present || (i_capture_bytes != 19'd442368)))
                 || (i_write_visible && !(|visible_accept))
                 || (i_last_read_consumed && !(|release_accept)))
            protocol_error_o <= 1'b1;
    end
endmodule
