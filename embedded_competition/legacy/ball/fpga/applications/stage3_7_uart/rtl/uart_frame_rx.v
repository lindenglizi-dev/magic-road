// V2 compatible framing; payload held until take. UART is still 115200/8N1.
module uart_frame_rx #(parameter TIMEOUT=1000000,MAX_PAYLOAD=240)(
 input clk,rst_n,input [7:0] data,input valid,framing_error,take,
 input [7:0] payload_addr,output [7:0] payload_data,
 output reg frame_valid,output reg [7:0] command,seq,length,output reg [15:0] signature);
 reg [7:0] memory[0:MAX_PAYLOAD-1];assign payload_data=memory[payload_addr<MAX_PAYLOAD?payload_addr:0];
 reg [3:0] state;reg [7:0] index;reg [15:0] crc;reg [$clog2(TIMEOUT+1)-1:0] idle;
 function [15:0] add_crc;input [15:0] old;input [7:0] b;reg [15:0] c;integer k;
 begin c=old^{b,8'b0};for(k=0;k<8;k=k+1)c=c[15]?(c<<1)^16'h1021:c<<1;add_crc=c;end endfunction
 always @(posedge clk or negedge rst_n)begin
 if(!rst_n)begin state<=0;index<=0;crc<=16'hffff;idle<=0;frame_valid<=0;command<=0;seq<=0;length<=0;signature<=0;end
 else if(take)begin frame_valid<=0;state<=0;idle<=0;end
 else if(!frame_valid)begin
 if(framing_error)begin state<=0;idle<=0;end
 else if(valid)begin
 idle<=0;
 case(state)
 0:if(data==8'haa)state<=1;
 1:if(data==8'h55)begin state<=2;crc<=16'hffff;end else state<=data==8'haa ? 1 : 0;
 2:if(data==2)begin crc<=add_crc(crc,data);state<=3;end else state<=data==8'haa ? 1 : 0;
 3:begin seq<=data;crc<=add_crc(crc,data);state<=4;end
 4:begin command<=data;crc<=add_crc(crc,data);state<=5;end
 5:if(data<=MAX_PAYLOAD)begin length<=data;index<=0;crc<=add_crc(crc,data);state<=data==0 ? 7 : 6;end else state<=0;
 6:begin memory[index]<=data;crc<=add_crc(crc,data);if(index==length-1)state<=7;else index<=index+1'b1;end
 7:if(data==crc[7:0])state<=8;else state<=data==8'haa ? 1 : 0;
 8:if(data==crc[15:8])begin state<=9;signature<=crc;end else state<=data==8'haa ? 1 : 0;
 9:if(data==13)state<=10;else state<=data==8'haa ? 1 : 0;
 10:begin if(data==10)frame_valid<=1;state<=0;end
 default:state<=0;
 endcase
 end else if(state!=0)begin if(idle==TIMEOUT-1)begin state<=0;idle<=0;end else idle<=idle+1'b1;end
 end end
endmodule
