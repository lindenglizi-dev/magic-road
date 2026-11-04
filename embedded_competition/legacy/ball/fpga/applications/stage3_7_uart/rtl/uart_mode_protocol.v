// V2: AA 55 VERSION SEQ CMD LEN DATA CRClo CRChi 0D 0A.
// Only MODE (01), LEN=1 is implemented. CRC16/CCITT-FALSE covers VERSION..DATA.
module uart_mode_protocol #(parameter integer TIMEOUT_CYCLES=1000000)(
 input wire clk,rst_n,input wire [7:0] data,input wire valid,framing_error,
 output reg [3:0] mode,output reg mode_valid);
 reg [3:0] state;reg [15:0] crc;reg [7:0] candidate;
 localparam integer CW=$clog2(TIMEOUT_CYCLES+1);
 reg [CW-1:0] idle_count;
 function [15:0] crc_byte;
 input [15:0] previous;input [7:0] value;
 reg [15:0] c;integer i;
 begin c=previous^{value,8'b0};for(i=0;i<8;i=i+1)c=c[15]?(c<<1)^16'h1021:c<<1;crc_byte=c;end
 endfunction
 always @(posedge clk or negedge rst_n)begin
 if(!rst_n)begin state<=0;crc<=16'hffff;candidate<=0;mode<=0;mode_valid<=0;idle_count<=0;end
 else begin
 mode_valid<=0;
 if(framing_error)begin state<=0;idle_count<=0;end
 else if(valid)begin
 idle_count<=0;
 case(state)
 0:if(data==8'haa)state<=1;
 1:if(data==8'h55)begin state<=2;crc<=16'hffff;end else state<=data==8'haa ? 1 : 0;
 2:if(data==2)begin crc<=crc_byte(crc,data);state<=3;end else state<=data==8'haa ? 1 : 0;
 3:begin crc<=crc_byte(crc,data);state<=4;end // SEQ reserved for responses
 4:if(data==1)begin crc<=crc_byte(crc,data);state<=5;end else state<=data==8'haa ? 1 : 0;
 5:if(data==1)begin crc<=crc_byte(crc,data);state<=6;end else state<=data==8'haa ? 1 : 0;
 6:begin candidate<=data;crc<=crc_byte(crc,data);state<=7;end
 7:if(data==crc[7:0])state<=8;else state<=data==8'haa ? 1 : 0;
 8:if(data==crc[15:8])state<=9;else state<=data==8'haa ? 1 : 0;
 9:if(data==8'h0d)state<=10;else state<=data==8'haa ? 1 : 0;
 10:begin
   if(data==8'h0a && candidate<=11)begin mode<=candidate[3:0];mode_valid<=1;end
   state<=data==8'haa ? 1 : 0;
 end
 default:state<=0;
 endcase
 end else if(state!=0)begin
 if(idle_count==TIMEOUT_CYCLES-1)begin state<=0;idle_count<=0;end
 else idle_count<=idle_count+1'b1;
 end
 end end
endmodule
