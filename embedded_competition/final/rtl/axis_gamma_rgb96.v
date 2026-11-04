`timescale 1ns/1ps
                                                                          
module axis_gamma_rgb96 #(
 parameter CURVE_FILE="../rtl/gamma_fixed.mem"
)(
 input I_clk,I_rst_n,I_tlast,I_tuser,input [95:0] I_tdata,input I_tvalid,
 output [95:0] O_tdata,output O_tvalid,O_tuser,O_tlast
);
 reg valid_delay,user_delay,last_delay;
 always @(posedge I_clk or negedge I_rst_n)begin
  if(!I_rst_n)begin valid_delay<=0;user_delay<=0;last_delay<=0;end
  else begin valid_delay<=I_tvalid;user_delay<=I_tuser;last_delay<=I_tlast;end
 end
 assign O_tvalid=valid_delay;assign O_tuser=user_delay;assign O_tlast=last_delay;
 genvar pair;
 generate for(pair=0;pair<6;pair=pair+1)begin:gen_curve
  (* ram_style="block" *) reg [7:0] curve[0:511];
  reg [7:0] first_byte,second_byte;
  initial $readmemh(CURVE_FILE,curve);
  always @(posedge I_clk)begin
   first_byte<=curve[{1'b0,I_tdata[pair*16+:8]}];
   second_byte<=curve[{1'b0,I_tdata[pair*16+8+:8]}];
  end
  assign O_tdata[pair*16+:16]=valid_delay?{second_byte,first_byte}:16'd0;
 end endgenerate
endmodule
