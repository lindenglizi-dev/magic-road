`timescale 1ns / 1ps
// 38-bit diagnostic boundary only, no board protocol or pin assignment.
module road_dynamic_low_io_top(
    input i_clk, input i_rstn,
    input i_rx_valid, input [15:0] i_rx_data, output o_rx_ready,
    output o_tx_valid, output [15:0] o_tx_data, input i_tx_ready
);
    localparam ST_IDLE=3'd0, ST_TABLE=3'd1, ST_PACKET=3'd2;
    localparam ST_SUBMIT=3'd3, ST_WAIT=3'd4, ST_TX=3'd5;
    reg reg_release_meta, reg_release_done;
    wire wire_rstn = i_rstn && reg_release_done;
    reg [2:0] state_current;
    reg [9:0] reg_table_addr;
    reg [4:0] reg_word_count;
    reg [303:0] reg_packet;
    reg [2:0] reg_remaining;
    reg [1:0] reg_tx_index;
    reg [15:0] reg_tx_tag, reg_tx_data, reg_tx_status;
    reg [31:0] reg_cycles;
    reg [15:0] reg_input_count, reg_output_count;
    wire flag_table_ready, flag_table_loaded, flag_input_ready;
    wire flag_output_valid, flag_output_int16, flag_fault;
    wire [15:0] wire_output_data, wire_output_tag;
    wire flag_rx = i_rx_valid && o_rx_ready;

    // Assertion cancels immediately; release requires two clock edges.
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) begin
            reg_release_meta <= 1'b0;
            reg_release_done <= 1'b0;
        end else begin
            reg_release_meta <= 1'b1;
            reg_release_done <= reg_release_meta;
        end
    end
    assign o_rx_ready = wire_rstn &&
        (state_current == ST_IDLE || state_current == ST_PACKET ||
         (state_current == ST_TABLE && flag_table_ready));
    assign o_tx_valid = wire_rstn && state_current == ST_TX;
    assign o_tx_data = reg_tx_index == 2'd0 ? reg_tx_tag :
                      reg_tx_index == 2'd1 ? reg_tx_data : reg_tx_status;

    // A000 loads 1024 sequential table words. B000 loads 19 packet words,
    // least-significant word first. C000 returns counters, D000 cycle count.
    // Packet: accum[95:0], pre[191:96], shifts[209:192], post[241:210],
    // post_shift[247:242], activate[248], mask[251:249], tags[299:252], fault[300].
    always @(posedge i_clk or negedge wire_rstn) begin
        if (!wire_rstn) begin
            state_current <= ST_IDLE;
            reg_table_addr <= 10'd0; reg_word_count <= 5'd0;
            reg_packet <= 304'd0; reg_remaining <= 3'd0;
            reg_tx_index <= 2'd0; reg_tx_tag <= 16'd0;
            reg_tx_data <= 16'd0; reg_tx_status <= 16'd0;
            reg_cycles <= 32'd0; reg_input_count <= 16'd0;
            reg_output_count <= 16'd0;
        end else begin
            if (state_current == ST_SUBMIT || state_current == ST_WAIT)
                reg_cycles <= reg_cycles + 32'd1;
            case (state_current)
                ST_IDLE: if (flag_rx) begin
                    case (i_rx_data)
                        16'ha000: begin state_current <= ST_TABLE; reg_table_addr <= 10'd0; end
                        16'hb000: begin state_current <= ST_PACKET; reg_word_count <= 5'd0; end
                        16'hc000,16'hd000: begin
                            reg_remaining <= 3'd0; reg_tx_index <= 2'd0;
                            reg_tx_tag <= i_rx_data == 16'hc000 ? reg_input_count : reg_cycles[15:0];
                            reg_tx_data <= i_rx_data == 16'hc000 ? reg_output_count : reg_cycles[31:16];
                            reg_tx_status <= {14'd0,flag_table_loaded,flag_fault};
                            state_current <= ST_TX;
                        end
                        default: begin end
                    endcase
                end
                ST_TABLE: if (flag_rx) begin
                    if (reg_table_addr == 10'd1023) state_current <= ST_IDLE;
                    else reg_table_addr <= reg_table_addr + 10'd1;
                end
                ST_PACKET: if (flag_rx) begin
                    reg_packet <= {i_rx_data,reg_packet[303:16]};
                    if (reg_word_count == 5'd18) begin
                        state_current <= ST_SUBMIT; reg_cycles <= 32'd0;
                    end else reg_word_count <= reg_word_count + 5'd1;
                end
                ST_SUBMIT: if (flag_input_ready) begin
                    reg_remaining <= reg_packet[251:249];
                    reg_input_count <= reg_input_count + 16'd1;
                    state_current <= ST_WAIT;
                end
                ST_WAIT: begin
                    if (flag_fault) begin
                        reg_tx_tag <= 16'hffff; reg_tx_data <= 16'd0;
                        reg_tx_status <= 16'd1; reg_remaining <= 3'd0;
                        reg_tx_index <= 2'd0; state_current <= ST_TX;
                    end else if (flag_output_valid) begin
                        reg_tx_tag <= wire_output_tag; reg_tx_data <= wire_output_data;
                        reg_tx_status <= {14'd0,flag_output_int16,1'b0};
                        reg_output_count <= reg_output_count + 16'd1;
                        reg_remaining <= reg_remaining & (reg_remaining - 3'd1);
                        reg_tx_index <= 2'd0; state_current <= ST_TX;
                    end
                end
                ST_TX: if (i_tx_ready) begin
                    if (reg_tx_index == 2'd2)
                        state_current <= reg_remaining == 3'd0 ? ST_IDLE : ST_WAIT;
                    else reg_tx_index <= reg_tx_index + 2'd1;
                end
                default: state_current <= ST_IDLE;
            endcase
        end
    end
    road_dynamic_postprocess u_chain(
        .i_clk(i_clk), .i_rstn(wire_rstn),
        .i_table_valid(state_current == ST_TABLE && i_rx_valid),
        .i_table_addr(reg_table_addr), .i_table_data(i_rx_data),
        .o_table_ready(flag_table_ready), .o_table_loaded(flag_table_loaded),
        .i_input_valid(state_current == ST_SUBMIT),
        .i_accumulators(reg_packet[95:0]), .i_pre_multipliers(reg_packet[191:96]),
        .i_pre_shifts(reg_packet[209:192]), .i_post_multiplier(reg_packet[241:210]),
        .i_post_shift(reg_packet[247:242]), .i_activate(reg_packet[248]),
        .i_lane_mask(reg_packet[251:249]), .i_tags(reg_packet[299:252]),
        .i_input_fault(reg_packet[300]), .o_input_ready(flag_input_ready),
        .i_output_ready(state_current == ST_WAIT), .o_output_valid(flag_output_valid),
        .o_output_data(wire_output_data), .o_output_tag(wire_output_tag),
        .o_output_int16(flag_output_int16), .o_fault(flag_fault)
    );
endmodule
