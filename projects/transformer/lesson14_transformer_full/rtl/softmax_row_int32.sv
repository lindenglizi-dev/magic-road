`timescale 1ns/1ps
// Lesson09, area-first deterministic row Softmax.
// Raw signed INT32 scores from Q @ Key^T.
// A full row is received before outputs can begin (max-reduce dependency).
// scale_q16 = round(65536/sqrt(D)) (1..65536); 1/sqrt(D) applied to score differences.
// exp LUT Q16 exp(-j/16), j=0..128; below -8 clamp to zero.
// Normalization uses an 8-step unsigned restoring divider with nearest rounding.
// out_data is unsigned Q0.8 mapped to [0..255], not signed INT8.
// Each output retains out_valid/out_data/index until out_ready handshake.
module softmax_row_int32 #(
    parameter integer MAX_LEN=64,
    parameter LUT_FILE="rtl/exp_lut_q16.hex"
)(
    input  logic clk,
    input  logic rst_n,
    input  logic start,
    input  logic [6:0] seq_len,
    input  logic [16:0] scale_q16,
    input  logic signed [31:0] in_data,
    input  logic in_valid,
    output logic in_ready,
    output logic [7:0] out_data,
    output logic [6:0] out_index,
    output logic out_valid,
    input  logic out_ready,
    output logic out_last,
    output logic busy,
    output logic done,
    output logic error,
    output logic [2:0] dbg_state,
    output logic [21:0] dbg_exp_sum
);
    localparam [2:0] ST_IDLE=3'd0, ST_COLLECT=3'd1, ST_EXP=3'd2,
                     ST_DIV_INIT=3'd3, ST_DIV_STEP=3'd4, ST_OUTPUT=3'd5;
    logic [2:0] state;
    logic [6:0] len_q, recv_idx, exp_idx, emit_idx;
    logic [16:0] scale_q;
    logic signed [31:0] max_score;
    logic signed [31:0] score_mem[0:MAX_LEN-1];
    logic [15:0] exp_mem[0:MAX_LEN-1];
    logic [15:0] exp_rom[0:128];
    logic [21:0] exp_sum;
    logic [31:0] remainder_q;
    logic [7:0] quotient_q;
    logic [2:0] div_bit;

    initial $readmemh(LUT_FILE,exp_rom);

    // Subtract before scale: softmax(s_i) = softmax(s_i - max(s)).
    // Sign extension to 33 bits prevents overflow when INT32 inputs differ widely.
    wire signed [32:0] score_delta =
        $signed({score_mem[exp_idx][31],score_mem[exp_idx]}) -
        $signed({max_score[31],max_score});
    // The 17-bit scale is extended to signed 18 bits, so 65536 is positive.
    wire signed [50:0] product_q16 = score_delta * $signed({1'b0,scale_q});
    // score_delta*(scale/65536)*16 = product / 4096, in Q4.
    wire signed [50:0] delta_q4 = product_q16 >>> 12;
    wire signed [50:0] negate_delta = -delta_q4;
    wire [7:0] lut_index=negate_delta[7:0];
    wire [15:0] exp_lut_value=(delta_q4 < -51'sd128) ? 16'd0 : exp_rom[lut_index];

    wire [31:0] numerator = ({16'd0,exp_mem[emit_idx]} * 32'd255) +
                            ({10'd0,exp_sum} >> 1);
    wire [31:0] test_divisor = {10'd0,exp_sum} << div_bit;

    assign in_ready=(state==ST_COLLECT);
    assign out_valid=(state==ST_OUTPUT);
    assign out_data=quotient_q;
    assign out_index=emit_idx;
    assign out_last=(emit_idx + 7'd1 == len_q);
    assign busy=(state!=ST_IDLE);
    assign dbg_state=state;
    assign dbg_exp_sum=exp_sum;

    always_ff @(posedge clk or negedge rst_n) begin
        if(!rst_n)begin
            state <= ST_IDLE;
            len_q<=0; scale_q<=0;recv_idx<=0;exp_idx<=0;emit_idx<=0;
            max_score<=0;exp_sum<=0;remainder_q<=0;quotient_q<=0;div_bit<=0;
            done<=0;error<=0;
        end else begin
            done <= 1'b0;
            error <= 1'b0;
            case(state)
              ST_IDLE: begin
                if(start) begin
                    if(seq_len==0 || seq_len>MAX_LEN || scale_q16==0 || scale_q16>17'd65536)
                        error<=1'b1;
                    else begin
                        len_q<=seq_len;
                        scale_q<=scale_q16;
                        recv_idx<=0; exp_idx<=0;emit_idx<=0;
                        exp_sum<=0;
                        state<=ST_COLLECT;
                    end
                end
              end
              ST_COLLECT: begin
                if(in_valid && in_ready) begin
                    score_mem[recv_idx]<=in_data;
                    if(recv_idx==0 || in_data>max_score)
                        max_score<=in_data;
                    if(recv_idx+7'd1==len_q) begin
                        exp_idx<=0;
                        exp_sum<=0;
                        state<=ST_EXP;
                    end else recv_idx<=recv_idx+7'd1;
                end
              end
              ST_EXP: begin
                exp_mem[exp_idx]<=exp_lut_value;
                exp_sum<=exp_sum + {6'd0,exp_lut_value};
                if(exp_idx+7'd1==len_q) begin
                    emit_idx<=0;
                    state<=ST_DIV_INIT;
                end else exp_idx<=exp_idx+7'd1;
              end
              ST_DIV_INIT: begin
                remainder_q<=numerator;
                quotient_q<=0;
                div_bit<=3'd7;
                state<=ST_DIV_STEP;
              end
              ST_DIV_STEP: begin
                if(remainder_q>=test_divisor) begin
                    remainder_q<=remainder_q-test_divisor;
                    quotient_q[div_bit]<=1'b1;
                end
                if(div_bit==0) state<=ST_OUTPUT;
                else div_bit<=div_bit-3'd1;
              end
              ST_OUTPUT: begin
                if(out_ready) begin
                    if(emit_idx+7'd1==len_q) begin
                        done<=1'b1;
                        state<=ST_IDLE;
                    end else begin
                        emit_idx<=emit_idx+7'd1;
                        state<=ST_DIV_INIT;
                    end
                end
              end
              default:state<=ST_IDLE;
            endcase
        end
    end
endmodule
