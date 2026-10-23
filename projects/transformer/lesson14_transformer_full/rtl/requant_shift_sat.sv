`timescale 1ns/1ps
// Explicit teaching policy, NOT a trained-model quantization configuration:
// y = clamp(floor(x / 2**shift), -128, 127), zero_point=0.
// Arithmetic right shift rounds NEGATIVE values toward minus infinity.
// One output-register stage; sink must accept EVERY out_valid clock.
// Address, phase, data and diagnostic raw value travel together.
module requant_shift_sat #(parameter integer ADDR_W=18) (
    input logic clk, rst_n,
    input logic in_valid,
    input logic signed [31:0] in_raw,
    input logic [4:0] in_shift,
    input logic [ADDR_W-1:0] in_addr,
    input logic [1:0] in_phase,
    output logic out_valid,
    output logic signed [7:0] out_data,
    output logic [ADDR_W-1:0] out_addr,
    output logic [1:0] out_phase,
    output logic signed [31:0] out_raw,
    output logic out_saturated
);
    wire signed [31:0] scaled = $signed(in_raw) >>> in_shift;
    wire clipped = (scaled>32'sd127) || (scaled<(-32'sd128));
    wire signed [7:0] quantized = (scaled>32'sd127) ? 8'sh7f :
                                   (scaled<(-32'sd128)) ? 8'sh80 : scaled[7:0];
    always_ff @(posedge clk or negedge rst_n) begin
        if(!rst_n) begin
            out_valid<=0; out_data<=0; out_addr<=0;
            out_phase<=0; out_raw<=0; out_saturated<=0;
        end else begin
            out_valid<=in_valid;
            if(in_valid) begin
                out_data<=quantized;
                out_addr<=in_addr;
                out_phase<=in_phase;
                out_raw<=in_raw;
                out_saturated<=clipped;
            end
        end
    end
endmodule
