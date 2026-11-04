`timescale 1ns/1ps
                                                                    
                                                                          
                                                                               
module board_power_on_reset #(parameter C_POWER_ON_CYCLES=65536)(
 input I_clk,input I_pll_locked,output O_pll_reset,output O_logic_reset_n,output O_ref_logic_reset_n,output O_ref_startup_complete);
 localparam C_COUNT_BITS=C_POWER_ON_CYCLES>1?$clog2(C_POWER_ON_CYCLES):1;
 reg [C_COUNT_BITS-1:0] startup_count=0;
 (*preserve*) reg startup_complete=0;
                                                                        
 (*preserve*) reg ref_startup_complete=0;
 always @(posedge I_clk)begin
 if(!startup_complete)begin
 if(startup_count==C_POWER_ON_CYCLES-1)begin
 startup_complete<=1;
 ref_startup_complete<=1;
 end
 else startup_count<=startup_count+1'b1;
 end
 end
 assign O_pll_reset=!startup_complete;
 assign O_logic_reset_n=startup_complete && I_pll_locked;
 assign O_ref_logic_reset_n=ref_startup_complete && I_pll_locked;
 assign O_ref_startup_complete=ref_startup_complete;
endmodule
