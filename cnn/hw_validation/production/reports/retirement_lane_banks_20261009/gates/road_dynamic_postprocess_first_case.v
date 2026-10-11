`timescale 1ns / 1ps

// Diagnostic candidate: bounded batch reservation and overlapped frozen operators.
// No runtime parameters are inferred from tags; external tags are opaque payloads.
module road_dynamic_postprocess(
    input i_clk,
    input i_rstn,
    input i_table_valid,
    input [9:0]i_table_addr,
    input signed [15:0]i_table_data,
    output o_table_ready,
    output o_table_loaded,
    input i_input_valid,
    input [95:0]i_accumulators,
    input [95:0]i_pre_multipliers,
    input [17:0]i_pre_shifts,
    input [31:0]i_post_multiplier,
    input [5:0]i_post_shift,
    input i_activate,
    input [2:0]i_lane_mask,
    input [47:0]i_tags,
    input i_input_fault,
    output o_input_ready,
    input i_output_ready,
    output o_output_valid,
    output signed [15:0]o_output_data,
    output [15:0]o_output_tag,
    output o_output_int16,
    output o_fault,
    output [1:0]o_queue_count,
    output [3:0]o_pending_count,
    output [3:0]o_meta_count,
    output o_pre_busy,
    output o_silu_busy,
    output o_post_busy,
    output o_pre_accept,
    output o_silu_accept,
    output o_post_accept
);
    // Two complete-batch ingress entries remain owned through last PRE acceptance.
    reg [95:0]reg_ingress_acc[0:1];
    reg [95:0]reg_ingress_mul[0:1];
    reg [17:0]reg_ingress_shift[0:1];
    reg [2:0]reg_ingress_slot[0:1];
    reg [2:0]reg_ingress_mask[0:1];
    reg reg_ingress_read, reg_ingress_write;
    reg [1:0]reg_ingress_count;

    // Retirement is reserved on batch acceptance, never on pipeline completion.
    reg [2:0]reg_retire_mask[0:7];
    reg [2:0]reg_retire_done[0:7];
    reg [2:0]reg_retire_emit[0:7];
    reg [2:0]reg_retire_seen[0:7];
    // Full-element writes keep each result lane independently inferable.
    reg [15:0]reg_retire_alpha[0:7];
    reg [15:0]reg_retire_beta[0:7];
    reg [15:0]reg_retire_gamma[0:7];
    reg [47:0]reg_retire_tags[0:7];
    reg reg_retire_activate[0:7];
    reg [30:0]reg_retire_multiplier[0:7];
    reg [5:0]reg_retire_shift[0:7];
    reg [7:0]reg_retire_valid, reg_retire_fault;
    reg [2:0]reg_retire_read, reg_retire_write;
    reg [3:0]reg_retire_count;
    reg flag_fault_pending, flag_fatal;

    // One registered selection boundary ahead of each full-width multiplier.
    reg flag_pre_buffer_valid, reg_pre_last;
    reg signed [31:0]reg_pre_acc;
    reg [30:0]reg_pre_mul;
    reg [5:0]reg_pre_shift;
    reg [15:0]reg_pre_tag;
    reg flag_post_buffer_valid;
    reg signed [31:0]reg_post_acc;
    reg [30:0]reg_post_mul;
    reg [5:0]reg_post_shift;
    reg [15:0]reg_post_tag;
    reg [4:0]reg_pre_inflight, reg_post_inflight;

    // SiLU has no tag port: this FIFO advances only on real stage handshakes.
    reg [15:0]reg_meta_tags[0:7];
    reg [2:0]reg_meta_read, reg_meta_write;
    reg [3:0]reg_meta_count;
    wire pre_input_ready, pre_result_valid, pre_result_fault;
    wire signed [15:0]pre_result_data;
    wire [15:0]pre_result_tag;
    wire post_input_ready, post_result_valid, post_result_fault;
    wire signed [15:0]post_result_data;
    wire signed [15:0]wire_post_saturated =
        post_result_data > 16'sd127 ? 16'sd127 :
        post_result_data < -16'sd128 ? -16'sd128 : post_result_data;
    wire [15:0]post_result_tag;
    wire silu_input_ready, silu_output_valid, silu_table_ready, silu_table_fault;
    wire signed [15:0]silu_output_data;
    wire [2:0]wire_pre_slot = pre_result_tag[4:2];
    wire [1:0]wire_pre_lane = pre_result_tag[1:0];
    wire [2:0]wire_post_slot = post_result_tag[4:2];
    wire [1:0]wire_post_lane = post_result_tag[1:0];
    wire flag_pre_identity = pre_result_tag[15:5] == 11'd0 &&
        wire_pre_lane < 2'd3 && reg_retire_valid[wire_pre_slot] &&
        reg_retire_mask[wire_pre_slot][wire_pre_lane] &&
        !reg_retire_seen[wire_pre_slot][wire_pre_lane];
    wire flag_post_identity = post_result_tag[15:5] == 11'd0 &&
        wire_post_lane < 2'd3 && reg_retire_valid[wire_post_slot] &&
        reg_retire_mask[wire_post_slot][wire_post_lane] &&
        !reg_retire_done[wire_post_slot][wire_post_lane];
    wire flag_empty = reg_ingress_count == 2'd0 && reg_retire_count == 4'd0 &&
        !flag_pre_buffer_valid && reg_pre_inflight == 5'd0 &&
        reg_meta_count == 4'd0 && !flag_post_buffer_valid && reg_post_inflight == 5'd0;
    wire flag_table_enable = i_rstn && !flag_fatal && flag_empty;
    wire flag_pre_active = flag_pre_identity && reg_retire_activate[wire_pre_slot];
    wire flag_pre_drop = !flag_pre_identity || pre_result_fault ||
        reg_retire_fault[wire_pre_slot];
    wire flag_pre_result_ready = i_rstn && !flag_fatal &&
        (flag_pre_drop || (flag_pre_active ?
        (silu_input_ready && reg_meta_count < 4'd8) : !post_result_valid));
    wire flag_pre_complete = pre_result_valid && flag_pre_result_ready;
    wire flag_pre_accept = i_rstn && !flag_fatal && flag_pre_buffer_valid && pre_input_ready;
    wire flag_silu_accept = flag_pre_complete && !flag_pre_drop && flag_pre_active;
    wire flag_post_buffer_ready = !flag_post_buffer_valid || post_input_ready;
    wire flag_silu_result_ready = i_rstn && !flag_fatal &&
        flag_post_buffer_ready && reg_meta_count != 4'd0;
    wire flag_post_accept = silu_output_valid && flag_silu_result_ready;
    wire flag_quant_post_accept = i_rstn && !flag_fatal &&
        flag_post_buffer_valid && post_input_ready;
    wire flag_post_complete = i_rstn && !flag_fatal && post_result_valid;
    wire flag_ingress_pop = flag_pre_accept && reg_pre_last;
    reg flag_bad_parameters;
    integer check_lane;
    always @(*) begin
        flag_bad_parameters = i_input_fault || i_lane_mask == 3'd0;
        for (check_lane = 0; check_lane < 3; check_lane = check_lane + 1)
            if (i_lane_mask[check_lane] &&
                (i_pre_multipliers[check_lane*32+31] ||
                 i_pre_shifts[check_lane*6 +: 6] == 6'd63))
                flag_bad_parameters = 1'b1;
        if (i_activate && (i_post_multiplier[31] || i_post_shift == 6'd63))
            flag_bad_parameters = 1'b1;
    end
    assign o_input_ready = i_rstn && o_table_loaded && !silu_table_fault &&
        !flag_fault_pending && !flag_fatal && !i_table_valid &&
        reg_ingress_count < 2'd2 && reg_retire_count < 4'd8;
    wire flag_input_accept = i_input_valid && o_input_ready;
    wire flag_ingress_push = flag_input_accept && !flag_bad_parameters;
    wire flag_head_fault = reg_retire_count != 4'd0 &&
        reg_retire_fault[reg_retire_read];
    wire [2:0]wire_emit_mask = reg_retire_emit[reg_retire_read];
    wire [1:0]wire_emit_lane = wire_emit_mask[0] ? 2'd0 :
        wire_emit_mask[1] ? 2'd1 : 2'd2;
    wire [2:0]wire_emit_bit = 3'b001 << wire_emit_lane;
    assign o_output_valid = i_rstn && !flag_fatal && reg_retire_count != 4'd0 &&
        !flag_head_fault && reg_retire_done[reg_retire_read] == reg_retire_mask[reg_retire_read];
    assign o_output_data = wire_emit_lane == 2'd0 ? reg_retire_alpha[reg_retire_read] :
        wire_emit_lane == 2'd1 ? reg_retire_beta[reg_retire_read] :
        wire_emit_lane == 2'd2 ? reg_retire_gamma[reg_retire_read] : 16'd0;
    assign o_output_tag = reg_retire_tags[reg_retire_read][wire_emit_lane*16 +: 16];
    assign o_output_int16 = !reg_retire_activate[reg_retire_read];
    wire flag_emit = o_output_valid && i_output_ready;
    wire flag_retire_pop = flag_emit && wire_emit_mask == wire_emit_bit;
    assign o_fault = i_rstn && (flag_fatal || silu_table_fault);
    assign o_table_ready = flag_table_enable && silu_table_ready;
    assign o_queue_count = reg_ingress_count;
    assign o_pending_count = reg_retire_count;
    assign o_meta_count = reg_meta_count;
    assign o_pre_busy = flag_pre_buffer_valid || reg_pre_inflight != 5'd0;
    assign o_silu_busy = reg_meta_count != 4'd0;
    assign o_post_busy = flag_post_buffer_valid || reg_post_inflight != 5'd0;
    assign o_pre_accept = flag_pre_accept;
    assign o_silu_accept = flag_silu_accept;
    assign o_post_accept = flag_post_accept;

    // Refill selection on acceptance; a full queue may conservatively bubble.
    reg flag_select_valid;
    reg select_entry;
    reg [2:0]select_mask;
    reg [1:0]select_lane;
    always @(*) begin
        select_entry = reg_ingress_read;
        select_mask = reg_ingress_mask[reg_ingress_read];
        flag_select_valid = reg_ingress_count != 2'd0;
        if (flag_pre_accept) begin
            if (reg_pre_last) begin
                select_entry = !reg_ingress_read;
                select_mask = reg_ingress_mask[!reg_ingress_read];
                flag_select_valid = reg_ingress_count > 2'd1;
            end else begin
                select_mask = select_mask & ~(3'b001 << reg_pre_tag[1:0]);
            end
        end
        select_lane = select_mask[0] ? 2'd0 : select_mask[1] ? 2'd1 : 2'd2;
    end

    road_dynamic_requant u_pre(
        .i_clk(i_clk),.i_rstn(i_rstn),
        .i_input_valid(flag_pre_buffer_valid && !flag_fatal),
        .i_accumulator(reg_pre_acc),.i_multiplier(reg_pre_mul),.i_shift(reg_pre_shift),
        .i_tag(reg_pre_tag),.o_input_ready(pre_input_ready),
        .i_output_ready(flag_pre_result_ready),.o_output_valid(pre_result_valid),
        .o_output_data(pre_result_data),.o_output_tag(pre_result_tag),.o_fault(pre_result_fault)
    );
    silu_shared_unit u_silu(
        .i_clk(i_clk),.i_rstn(i_rstn),
        .i_table_valid(i_table_valid && flag_table_enable),.i_table_addr(i_table_addr),
        .i_table_data(i_table_data),.o_table_ready(silu_table_ready),
        .o_table_loaded(o_table_loaded),.o_table_fault(silu_table_fault),
        .i_input_valid(pre_result_valid && !flag_pre_drop && flag_pre_active &&
            reg_meta_count < 4'd8 && !flag_fatal),.i_input_data(pre_result_data),
        .o_input_ready(silu_input_ready),.i_output_ready(flag_silu_result_ready),
        .o_output_valid(silu_output_valid),.o_output_data(silu_output_data)
    );
    road_dynamic_requant u_post(
        .i_clk(i_clk),.i_rstn(i_rstn),
        .i_input_valid(flag_post_buffer_valid && !flag_fatal),
        .i_accumulator(reg_post_acc),.i_multiplier(reg_post_mul),.i_shift(reg_post_shift),
        .i_tag(reg_post_tag),.o_input_ready(post_input_ready),
        .i_output_ready(i_rstn && !flag_fatal),.o_output_valid(post_result_valid),
        .o_output_data(post_result_data),.o_output_tag(post_result_tag),.o_fault(post_result_fault)
    );

    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) begin
            reg_ingress_read <= 1'b0; reg_ingress_write <= 1'b0;
            reg_ingress_count <= 2'd0;
            reg_retire_read <= 3'd0; reg_retire_write <= 3'd0;
            reg_retire_count <= 4'd0; reg_retire_valid <= 8'd0; reg_retire_fault <= 8'd0;
            flag_fault_pending <= 1'b0; flag_fatal <= 1'b0;
            flag_pre_buffer_valid <= 1'b0; reg_pre_last <= 1'b0;
            reg_pre_acc <= 32'sd0; reg_pre_mul <= 31'd0;
            reg_pre_shift <= 6'd0; reg_pre_tag <= 16'd0;
            flag_post_buffer_valid <= 1'b0;
            reg_post_acc <= 32'sd0; reg_post_mul <= 31'd0;
            reg_post_shift <= 6'd0; reg_post_tag <= 16'd0;
            reg_pre_inflight <= 5'd0; reg_post_inflight <= 5'd0;
            reg_meta_read <= 3'd0; reg_meta_write <= 3'd0; reg_meta_count <= 4'd0;
        end else if (flag_head_fault || silu_table_fault) begin
            // Ordered cancellation: older outputs have already retired completely.
            flag_fatal <= 1'b1; flag_fault_pending <= 1'b1;
            reg_ingress_count <= 2'd0; reg_retire_count <= 4'd0;
            reg_retire_valid <= 8'd0; reg_retire_fault <= 8'd0;
            flag_pre_buffer_valid <= 1'b0; flag_post_buffer_valid <= 1'b0;
            reg_pre_inflight <= 5'd0; reg_post_inflight <= 5'd0; reg_meta_count <= 4'd0;
        end else if (!flag_fatal) begin
            case ({flag_ingress_push,flag_ingress_pop})
                2'b10: reg_ingress_count <= reg_ingress_count + 2'd1;
                2'b01: reg_ingress_count <= reg_ingress_count - 2'd1;
                default: reg_ingress_count <= reg_ingress_count;
            endcase
            case ({flag_input_accept,flag_retire_pop})
                2'b10: reg_retire_count <= reg_retire_count + 4'd1;
                2'b01: reg_retire_count <= reg_retire_count - 4'd1;
                default: reg_retire_count <= reg_retire_count;
            endcase
            case ({flag_pre_accept,flag_pre_complete})
                2'b10: reg_pre_inflight <= reg_pre_inflight + 5'd1;
                2'b01: reg_pre_inflight <= reg_pre_inflight - 5'd1;
                default: reg_pre_inflight <= reg_pre_inflight;
            endcase
            case ({flag_quant_post_accept,flag_post_complete})
                2'b10: reg_post_inflight <= reg_post_inflight + 5'd1;
                2'b01: reg_post_inflight <= reg_post_inflight - 5'd1;
                default: reg_post_inflight <= reg_post_inflight;
            endcase
            case ({flag_silu_accept,flag_post_accept})
                2'b10: reg_meta_count <= reg_meta_count + 4'd1;
                2'b01: reg_meta_count <= reg_meta_count - 4'd1;
                default: reg_meta_count <= reg_meta_count;
            endcase
            if (flag_input_accept) begin
                reg_retire_valid[reg_retire_write] <= 1'b1;
                reg_retire_fault[reg_retire_write] <= flag_bad_parameters;
                reg_retire_mask[reg_retire_write] <= i_lane_mask;
                reg_retire_done[reg_retire_write] <= 3'd0;
                reg_retire_seen[reg_retire_write] <= 3'd0;
                reg_retire_emit[reg_retire_write] <= i_lane_mask;
                reg_retire_tags[reg_retire_write] <= i_tags;
                reg_retire_activate[reg_retire_write] <= i_activate;
                reg_retire_multiplier[reg_retire_write] <= i_post_multiplier[30:0];
                reg_retire_shift[reg_retire_write] <= i_post_shift;
                reg_retire_write <= reg_retire_write + 3'd1;
                if (flag_bad_parameters) flag_fault_pending <= 1'b1;
            end
            if (flag_ingress_push) begin
                reg_ingress_acc[reg_ingress_write] <= i_accumulators;
                reg_ingress_mul[reg_ingress_write] <= i_pre_multipliers;
                reg_ingress_shift[reg_ingress_write] <= i_pre_shifts;
                reg_ingress_mask[reg_ingress_write] <= i_lane_mask;
                reg_ingress_slot[reg_ingress_write] <= reg_retire_write;
                reg_ingress_write <= !reg_ingress_write;
            end
            if (flag_pre_accept) begin
                reg_ingress_mask[reg_ingress_read] <=
                    reg_ingress_mask[reg_ingress_read] & ~(3'b001 << reg_pre_tag[1:0]);
                if (reg_pre_last) reg_ingress_read <= !reg_ingress_read;
            end
            if (!flag_pre_buffer_valid || flag_pre_accept) begin
                flag_pre_buffer_valid <= flag_select_valid;
                if (flag_select_valid) begin
                    reg_pre_acc <= reg_ingress_acc[select_entry][select_lane*32 +: 32];
                    reg_pre_mul <= reg_ingress_mul[select_entry][select_lane*32 +: 31];
                    reg_pre_shift <= reg_ingress_shift[select_entry][select_lane*6 +: 6];
                    reg_pre_tag <= {11'd0,reg_ingress_slot[select_entry],select_lane};
                    reg_pre_last <= select_mask == (3'b001 << select_lane);
                end
            end
            if (flag_pre_complete) begin
                if (flag_pre_identity) begin
                    reg_retire_seen[wire_pre_slot][wire_pre_lane] <= 1'b1;
                    if (pre_result_fault) begin
                        reg_retire_fault[wire_pre_slot] <= 1'b1;
                        flag_fault_pending <= 1'b1;
                    end
                end else begin
                    // Unowned token is corruption, not a trustworthy batch identifier.
                    reg_retire_fault[reg_retire_read] <= 1'b1;
                    flag_fault_pending <= 1'b1;
                end
            end
            if (flag_silu_accept) begin
                reg_meta_tags[reg_meta_write] <= pre_result_tag;
                reg_meta_write <= reg_meta_write + 3'd1;
            end
            if (flag_post_buffer_ready) begin
                flag_post_buffer_valid <= flag_post_accept;
                if (flag_post_accept) begin
                    reg_post_acc <= {{16{silu_output_data[15]}},silu_output_data};
                    reg_post_tag <= reg_meta_tags[reg_meta_read];
                    reg_post_mul <= reg_retire_multiplier[reg_meta_tags[reg_meta_read][4:2]];
                    reg_post_shift <= reg_retire_shift[reg_meta_tags[reg_meta_read][4:2]];
                end
            end
            if (flag_post_accept) reg_meta_read <= reg_meta_read + 3'd1;
            // One result write port. RAW is held above when POST owns this edge.
            if (flag_post_complete) begin
                if (!flag_post_identity || post_result_fault) begin
                    reg_retire_fault[flag_post_identity ? wire_post_slot : reg_retire_read] <= 1'b1;
                    flag_fault_pending <= 1'b1;
                end else if (!reg_retire_fault[wire_post_slot]) begin
                    reg_retire_done[wire_post_slot][wire_post_lane] <= 1'b1;
                    case (wire_post_lane)
                        2'd0: reg_retire_alpha[wire_post_slot] <= wire_post_saturated;
                        2'd1: reg_retire_beta[wire_post_slot] <= wire_post_saturated;
                        2'd2: reg_retire_gamma[wire_post_slot] <= wire_post_saturated;
                        default: begin end // Identity validation rejects lane three.
                    endcase
                end
            end else if (flag_pre_complete && !flag_pre_drop && !flag_pre_active) begin
                reg_retire_done[wire_pre_slot][wire_pre_lane] <= 1'b1;
                case (wire_pre_lane)
                    2'd0: reg_retire_alpha[wire_pre_slot] <= pre_result_data;
                    2'd1: reg_retire_beta[wire_pre_slot] <= pre_result_data;
                    2'd2: reg_retire_gamma[wire_pre_slot] <= pre_result_data;
                    default: begin end // Identity validation rejects lane three.
                endcase
            end
            if (flag_emit) begin
                reg_retire_emit[reg_retire_read] <= wire_emit_mask & ~wire_emit_bit;
                if (flag_retire_pop) begin
                    reg_retire_valid[reg_retire_read] <= 1'b0;
                    reg_retire_read <= reg_retire_read + 3'd1;
                end
            end
        end
    end
endmodule
