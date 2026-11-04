`timescale 1ns/1ps
                                                                          
                                                                                 
module quad_group_serializer #(parameter C_DATA_BITS=96, C_SYNCHRONOUS_FLUSH=0)(
 input clk,rst_n,clear,input [C_DATA_BITS-1:0] data,input valid,user_mark,last_mark,done,
 output [C_DATA_BITS-1:0] group_data,output [1:0] lane,
 output ov,ou,ol,od,output busy,error,output [9:0] level
);
 reg [C_DATA_BITS+2:0] memory[0:511];
 reg [C_DATA_BITS+2:0] memory_output,current_group;
 reg [8:0] write_address,read_address;
 reg [9:0] count;
 reg active,pending,overflow;
 reg [1:0] phase;
 wire flush=C_SYNCHRONOUS_FLUSH && clear;
 wire fetch=!flush && !pending && (!active || phase==2) && count!=0;
 wire push=!flush && valid && (count!=511 || fetch);
 always @(posedge clk)begin
  if(push)memory[write_address]<={user_mark,last_mark,done,data};
  if(fetch)memory_output<=memory[read_address];
  if(!flush && (!active || phase==3) && pending)current_group<=memory_output;
 end
 always @(posedge clk or negedge rst_n)begin
  if(!rst_n)begin
   write_address<=0;read_address<=0;count<=0;active<=0;pending<=0;overflow<=0;phase<=0;
  end else if(flush)begin
   write_address<=0;read_address<=0;count<=0;active<=0;pending<=0;overflow<=0;phase<=0;
  end else begin
   pending<=fetch;
   if(push)write_address<=write_address+1'b1;
   if(fetch)read_address<=read_address+1'b1;
   case({push,fetch})
    2'b10:count<=count+1'b1;
    2'b01:count<=count-1'b1;
    default:begin end
   endcase
   if(valid && !push)overflow<=1;
   if(active)begin
    if(phase==3)begin phase<=0;active<=pending;end
    else phase<=phase+1'b1;
   end else if(pending)begin phase<=0;active<=1;end
  end
 end
 assign group_data=current_group[C_DATA_BITS-1:0];
 assign lane=phase;
 assign ov=active;
 assign ou=active && phase==0 && current_group[C_DATA_BITS+2];
 assign ol=active && phase==3 && current_group[C_DATA_BITS+1];
 assign od=active && phase==3 && current_group[C_DATA_BITS];
 assign busy=active || pending || count!=0;
 assign error=overflow;
 assign level=count;
endmodule
