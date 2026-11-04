module uart_byte_tx #(parameter CLK_HZ=50000000,BAUD=115200)(
 input clk,rst_n,input [7:0] data,input valid,output wire ready,output reg tx);
 localparam TICKS=(CLK_HZ+BAUD/2)/BAUD;
 reg [$clog2(TICKS+1)-1:0] timer;reg [9:0] bits;reg [3:0] index;reg busy;
 assign ready=!busy;
 always @(posedge clk or negedge rst_n)begin
 if(!rst_n)begin timer<=0;bits<=10'h3ff;index<=0;busy<=0;tx<=1;end
 else if(!busy)begin
 if(valid)begin bits<={1'b1,data,1'b0};tx<=0;timer<=TICKS-1;index<=0;busy<=1;end
 end else if(timer!=0)timer<=timer-1'b1;
 else if(index==9)begin busy<=0;tx<=1;end
 else begin index<=index+1'b1;tx<=bits[index+1'b1];timer<=TICKS-1;end
 end
endmodule

module uart_frame_tx #(parameter CLK_HZ=50000000,BAUD=115200)(
 input clk,rst_n,start,input [7:0] command,seq,length,input [511:0] payload,
 output reg busy,output tx);
 reg [511:0] body;reg [7:0] cmd,sn,len;reg [8:0] index;reg [15:0] crc;
 reg [7:0] byte_data;wire byte_ready;
 function [15:0] add_crc;input [15:0] old;input [7:0] b;reg [15:0] c;integer k;
 begin c=old^{b,8'b0};for(k=0;k<8;k=k+1)c=c[15]?(c<<1)^16'h1021:c<<1;add_crc=c;end endfunction
 always @*begin
 byte_data=0;
 case(index)
 0:byte_data=8'haa;1:byte_data=8'h55;2:byte_data=2;3:byte_data=sn;4:byte_data=cmd;5:byte_data=len;
 default:begin
 if(index<6+len)byte_data=body[(index-6)*8+:8];
 else if(index==6+len)byte_data=crc[7:0];
 else if(index==7+len)byte_data=crc[15:8];
 else if(index==8+len)byte_data=13;else byte_data=10;
 end endcase
 end
 uart_byte_tx #(.CLK_HZ(CLK_HZ),.BAUD(BAUD)) u_byte(.clk(clk),.rst_n(rst_n),.data(byte_data),.valid(busy),.ready(byte_ready),.tx(tx));
 always @(posedge clk or negedge rst_n)begin
 if(!rst_n)begin busy<=0;body<=0;cmd<=0;sn<=0;len<=0;index<=0;crc<=16'hffff;end
 else if(start&&!busy)begin busy<=1;body<=payload;cmd<=command;sn<=seq;len<=length;index<=0;crc<=16'hffff;end
 else if(busy&&byte_ready)begin
 if(index>=2&&index<6+len)crc<=add_crc(crc,byte_data);
 if(index==9+len)busy<=0;else index<=index+1'b1;
 end end
endmodule
