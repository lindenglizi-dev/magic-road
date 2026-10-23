`timescale 1ns/1ps
// FFN hidden layer: floor(arithmetic shift) -> ReLU -> saturate signed INT8.
// One registered stage. Metadata row/col advances with the data.
module ffn_relu_requant #(parameter integer ADDR_W=18)(
 input logic clk, rst_n, in_valid,
 input logic signed [31:0] in_raw,
 input logic [4:0] in_shift,
 input logic [8:0] in_row,in_col,
 output logic out_valid,
 output logic signed [7:0] out_data,
 output logic [8:0] out_row,out_col
);
 wire signed [31:0] shifted=$signed(in_raw) >>> in_shift;
 wire signed [7:0] mapped=shifted<=0?8'sd0:(shifted>127?8'sd127:shifted[7:0]);
 always_ff @(posedge clk or negedge rst_n)
  if(!rst_n)begin
   out_valid<=0;out_data<=0;out_row<=0;out_col<=0;
  end else begin
   out_valid<=in_valid;
   if(in_valid)begin out_data<=mapped;out_row<=in_row;out_col<=in_col;end
  end
endmodule
