`timescale 1ns / 1ps

// SRIF1 detection-table crossing with a frozen source and two rotating display banks.
module road_detection_table_cdc #(
    parameter integer AGE_LIMIT_MS = 500,
    parameter [31:0] EXPECTED_MODEL_ID = 32'd3009235558
) (
    input          i_src_clk,
    input          i_dst_clk,
    input          i_rstn,
    input          i_src_entry_valid,
    input  [96:0]  i_src_entry,
    output         o_src_entry_ready,
    input          i_src_meta_valid,
    input  [264:0] i_src_metadata,
    output         o_src_meta_ready,
    input          i_src_abort,
    output         o_src_copy_ack,
    output         o_src_busy,
    output         o_src_error,
    input          i_dst_copy_enable,
    input          i_dst_sof,
    input  [63:0]  i_dst_now_ms,
    input  [31:0]  i_dst_time_epoch,
    input          i_dst_time_valid,
    input  [5:0]   i_dst_read_index,
    output [96:0]  o_dst_entry,
    output [264:0] o_dst_metadata,
    output         o_dst_active_valid,
    output         o_dst_draw_valid,
    output         o_dst_pending_valid,
    output         o_dst_copy_busy,
    output         o_dst_update,
    output [63:0]  o_dst_age_upper_ms,
    output         o_dst_error
);

    localparam [6:0] TABLE_CAPACITY = 7'd64;
    localparam [64:0] AGE_LIMIT_EXTENDED = AGE_LIMIT_MS;

    // Common reset asserts asynchronously; each domain releases after two local edges.
    (* ASYNC_REG = "TRUE" *) reg flag_src_release_meta;
    (* ASYNC_REG = "TRUE" *) reg flag_src_release;
    (* ASYNC_REG = "TRUE" *) reg flag_dst_release_meta;
    (* ASYNC_REG = "TRUE" *) reg flag_dst_release;

    always @(posedge i_src_clk or negedge i_rstn) begin
        if (!i_rstn) begin
            flag_src_release_meta <= 1'b0;
            flag_src_release      <= 1'b0;
        end else begin
            flag_src_release_meta <= 1'b1;
            flag_src_release      <= flag_src_release_meta;
        end
    end

    always @(posedge i_dst_clk or negedge i_rstn) begin
        if (!i_rstn) begin
            flag_dst_release_meta <= 1'b0;
            flag_dst_release      <= 1'b0;
        end else begin
            flag_dst_release_meta <= 1'b1;
            flag_dst_release      <= flag_dst_release_meta;
        end
    end

    // The source table is written only in source order and freezes when metadata seals it.
    reg [96:0]  mem_source_entry [0:63];
    reg [264:0] reg_source_metadata;
    reg [6:0]   cnt_source_entry;
    reg         flag_source_sealed;
    reg         flag_request_toggle_src;
    reg         flag_source_copy_ack_o;
    reg         flag_source_error_o;
    reg         flag_ack_toggle_dst;

    (* ASYNC_REG = "TRUE" *) reg flag_ack_meta_src;
    (* ASYNC_REG = "TRUE" *) reg flag_ack_sync_src;

    wire [6:0] wire_input_box_count;
    wire       flag_input_count_legal;
    wire       flag_source_entry_ready;
    wire       flag_source_meta_ready;

    assign wire_input_box_count = i_src_metadata[134:128];
    assign flag_input_count_legal = wire_input_box_count <= TABLE_CAPACITY;
    assign flag_source_entry_ready = flag_src_release && !flag_source_sealed
                                   && !i_src_abort && (cnt_source_entry < TABLE_CAPACITY);
    assign flag_source_meta_ready = flag_src_release && !flag_source_sealed
                                  && !i_src_abort && !i_src_entry_valid
                                  && flag_input_count_legal
                                  && (wire_input_box_count == cnt_source_entry);

    assign o_src_entry_ready = flag_source_entry_ready;
    assign o_src_meta_ready  = flag_source_meta_ready;
    assign o_src_copy_ack    = flag_source_copy_ack_o;
    assign o_src_busy        = flag_src_release
                             && (flag_source_sealed || (cnt_source_entry != 7'd0));
    assign o_src_error       = flag_source_error_o;

    always @(posedge i_src_clk or negedge flag_src_release) begin
        if (!flag_src_release) begin
            flag_ack_meta_src <= 1'b0;
            flag_ack_sync_src <= 1'b0;
        end else begin
            flag_ack_meta_src <= flag_ack_toggle_dst;
            flag_ack_sync_src <= flag_ack_meta_src;
        end
    end

    always @(posedge i_src_clk or negedge flag_src_release) begin
        if (!flag_src_release) begin
            cnt_source_entry          <= 7'd0;
            flag_source_sealed        <= 1'b0;
            flag_request_toggle_src   <= 1'b0;
            flag_source_copy_ack_o    <= 1'b0;
            flag_source_error_o       <= 1'b0;
        end else begin
            flag_source_copy_ack_o <= 1'b0;
            flag_source_error_o    <= 1'b0;

            if (i_src_abort && !flag_source_sealed) begin
                cnt_source_entry <= 7'd0;
            end else begin
                if (i_src_entry_valid && flag_source_entry_ready) begin
                    mem_source_entry[cnt_source_entry[5:0]] <= i_src_entry;
                    cnt_source_entry <= cnt_source_entry + 7'd1;
                end

                if (i_src_meta_valid && flag_source_meta_ready) begin
                    reg_source_metadata      <= i_src_metadata;
                    flag_source_sealed       <= 1'b1;
                    flag_request_toggle_src  <= !flag_request_toggle_src;
                end

                if (!flag_source_sealed && i_src_entry_valid
                 && (cnt_source_entry == TABLE_CAPACITY)) begin
                    flag_source_error_o <= 1'b1;
                end
                if (!flag_source_sealed && i_src_meta_valid
                 && !flag_input_count_legal) begin
                    flag_source_error_o <= 1'b1;
                end
                if (flag_source_sealed && i_src_abort) begin
                    flag_source_error_o <= 1'b1;
                end
            end

            if (flag_source_sealed
             && (flag_ack_sync_src == flag_request_toggle_src)) begin
                cnt_source_entry       <= 7'd0;
                flag_source_sealed     <= 1'b0;
                flag_source_copy_ack_o <= 1'b1;
            end
        end
    end

    // Request and acknowledgement toggles are the only dynamically sampled CDC controls.
    (* ASYNC_REG = "TRUE" *) reg flag_request_meta_dst;
    (* ASYNC_REG = "TRUE" *) reg flag_request_sync_dst;
    reg flag_request_seen_dst;

    always @(posedge i_dst_clk or negedge flag_dst_release) begin
        if (!flag_dst_release) begin
            flag_request_meta_dst <= 1'b0;
            flag_request_sync_dst <= 1'b0;
        end else begin
            flag_request_meta_dst <= flag_request_toggle_src;
            flag_request_sync_dst <= flag_request_meta_dst;
        end
    end

    // Destination payload banks are written only while inactive and are never reset.
    reg [96:0]  mem_destination_a [0:63];
    reg [96:0]  mem_destination_b [0:63];
    reg [264:0] reg_destination_meta_a;
    reg [264:0] reg_destination_meta_b;
    reg         flag_active_bank_dst;
    reg         flag_active_present_dst;
    reg         flag_active_valid_dst;
    reg         flag_pending_bank_dst;
    reg         flag_pending_valid_dst;
    reg         flag_copy_bank_dst;
    reg         flag_metadata_wait_dst;
    reg         flag_copy_busy_dst;
    reg [5:0]   cnt_copy_index_dst;
    reg [6:0]   cnt_copy_entry_dst;
    reg         flag_destination_update_o;
    reg         flag_destination_error_o;

    wire [96:0]  wire_source_read_entry;
    wire [264:0] wire_active_metadata;
    wire [264:0] wire_pending_metadata;
    wire [6:0]   wire_active_box_count;
    wire [6:0]   wire_pending_box_count;

    assign wire_source_read_entry = mem_source_entry[cnt_copy_index_dst];
    assign wire_active_metadata = flag_active_bank_dst
                                ? reg_destination_meta_b : reg_destination_meta_a;
    assign wire_pending_metadata = flag_pending_bank_dst
                                 ? reg_destination_meta_b : reg_destination_meta_a;
    assign wire_active_box_count = wire_active_metadata[134:128];
    assign wire_pending_box_count = wire_pending_metadata[134:128];

    always @(posedge i_dst_clk or negedge flag_dst_release) begin
        if (!flag_dst_release) begin
            flag_request_seen_dst     <= 1'b0;
            flag_ack_toggle_dst       <= 1'b0;
            flag_active_bank_dst      <= 1'b0;
            flag_active_present_dst   <= 1'b0;
            flag_active_valid_dst     <= 1'b0;
            flag_pending_bank_dst     <= 1'b0;
            flag_pending_valid_dst    <= 1'b0;
            flag_copy_bank_dst        <= 1'b0;
            flag_metadata_wait_dst    <= 1'b0;
            flag_copy_busy_dst        <= 1'b0;
            cnt_copy_index_dst        <= 6'd0;
            cnt_copy_entry_dst        <= 7'd0;
            flag_destination_update_o <= 1'b0;
            flag_destination_error_o  <= 1'b0;
        end else begin
            flag_destination_update_o <= 1'b0;
            flag_destination_error_o  <= 1'b0;

            if (i_dst_sof && flag_pending_valid_dst) begin
                flag_active_bank_dst    <= flag_pending_bank_dst;
                flag_active_present_dst <= 1'b1;
                flag_active_valid_dst   <= wire_pending_box_count != 7'd0;
                flag_pending_valid_dst  <= 1'b0;
                flag_destination_update_o <= 1'b1;
            end

            if (!flag_pending_valid_dst && !flag_copy_busy_dst
             && !flag_metadata_wait_dst
             && (flag_request_sync_dst != flag_request_seen_dst)) begin
                flag_request_seen_dst  <= flag_request_sync_dst;
                flag_copy_bank_dst     <= !flag_active_bank_dst;
                flag_metadata_wait_dst <= 1'b1;
            end else if (flag_metadata_wait_dst) begin
                flag_metadata_wait_dst <= 1'b0;
                cnt_copy_entry_dst     <= reg_source_metadata[134:128];
                cnt_copy_index_dst     <= 6'd0;

                if (flag_copy_bank_dst) begin
                    reg_destination_meta_b <= reg_source_metadata;
                end else begin
                    reg_destination_meta_a <= reg_source_metadata;
                end

                if (reg_source_metadata[134:128] > TABLE_CAPACITY) begin
                    flag_destination_error_o <= 1'b1;
                    flag_ack_toggle_dst      <= flag_request_seen_dst;
                end else if (reg_source_metadata[134:128] == 7'd0) begin
                    flag_pending_bank_dst  <= flag_copy_bank_dst;
                    flag_pending_valid_dst <= 1'b1;
                    flag_ack_toggle_dst    <= flag_request_seen_dst;
                end else begin
                    flag_copy_busy_dst <= 1'b1;
                end
            end else if (flag_copy_busy_dst && i_dst_copy_enable) begin
                if (flag_copy_bank_dst) begin
                    mem_destination_b[cnt_copy_index_dst] <= wire_source_read_entry;
                end else begin
                    mem_destination_a[cnt_copy_index_dst] <= wire_source_read_entry;
                end

                if ({1'b0, cnt_copy_index_dst} + 7'd1 == cnt_copy_entry_dst) begin
                    flag_copy_busy_dst     <= 1'b0;
                    flag_pending_bank_dst  <= flag_copy_bank_dst;
                    flag_pending_valid_dst <= 1'b1;
                    flag_ack_toggle_dst    <= flag_request_seen_dst;
                end else begin
                    cnt_copy_index_dst <= cnt_copy_index_dst + 6'd1;
                end
            end
        end
    end

    // Active data is an asynchronous LUTRAM read and is isolated by valid/count.
    reg [96:0] reg_destination_entry;

    always @(*) begin
        reg_destination_entry = 97'd0;
        if (flag_active_valid_dst
         && ({1'b0, i_dst_read_index} < wire_active_box_count)) begin
            if (flag_active_bank_dst) begin
                reg_destination_entry = mem_destination_b[i_dst_read_index];
            end else begin
                reg_destination_entry = mem_destination_a[i_dst_read_index];
            end
        end
    end

    // A 65-bit age path prevents now-capture+4 from wrapping into a valid age.
    wire [63:0] wire_capture_ms;
    wire [63:0] wire_completion_ms;
    wire [64:0] wire_age_delta_extended;
    wire [64:0] wire_age_upper_extended;
    wire        flag_timestamp_order_valid;
    wire        flag_draw_identity_valid;
    wire        flag_draw_age_valid;

    assign wire_capture_ms = wire_active_metadata[200:137];
    assign wire_completion_ms = wire_active_metadata[264:201];
    assign wire_age_delta_extended = {1'b0, i_dst_now_ms}
                                    - {1'b0, wire_capture_ms};
    assign wire_age_upper_extended = wire_age_delta_extended + 65'd4;
    assign flag_timestamp_order_valid = wire_capture_ms <= wire_completion_ms
                                      && wire_completion_ms <= i_dst_now_ms;
    assign flag_draw_identity_valid = i_dst_time_valid
                                    && (wire_active_metadata[31:0] == i_dst_time_epoch)
                                    && (wire_active_metadata[127:96] == EXPECTED_MODEL_ID)
                                    && (wire_active_metadata[136:135] == 2'd0)
                                    && (wire_active_box_count <= TABLE_CAPACITY);
    assign flag_draw_age_valid = !wire_age_upper_extended[64]
                               && (wire_age_upper_extended <= AGE_LIMIT_EXTENDED);

    assign o_dst_entry = reg_destination_entry;
    assign o_dst_metadata = flag_active_present_dst ? wire_active_metadata : 265'd0;
    assign o_dst_active_valid = flag_active_present_dst;
    assign o_dst_draw_valid = flag_active_valid_dst && flag_draw_identity_valid
                            && flag_timestamp_order_valid && flag_draw_age_valid;
    assign o_dst_pending_valid = flag_pending_valid_dst;
    assign o_dst_copy_busy = flag_copy_busy_dst;
    assign o_dst_update = flag_destination_update_o;
    assign o_dst_age_upper_ms = !flag_active_present_dst
                              || (wire_capture_ms > i_dst_now_ms) ? 64'd0
                              : wire_age_upper_extended[64]
                              ? 64'hFFFFFFFFFFFFFFFF
                              : wire_age_upper_extended[63:0];
    assign o_dst_error = flag_destination_error_o;

endmodule
