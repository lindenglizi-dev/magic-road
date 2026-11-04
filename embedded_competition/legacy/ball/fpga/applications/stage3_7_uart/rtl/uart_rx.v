// 8N1, LSB first. All counters use clk enables; no generated clocks.
module uart_rx #(parameter integer CLK_HZ=50000000, BAUD=115200)(
 input wire clk,rst_n,rx,output reg [7:0] data,output reg valid,output reg framing_error);
 localparam integer TICKS=(CLK_HZ+BAUD/2)/BAUD;
 localparam integer CW=$clog2(TICKS+1);
 (* ASYNC_REG="TRUE" *) reg rx_meta,rx_sync;
 reg [CW-1:0] timer;reg [1:0] state;reg [2:0] bit_index;reg [7:0] shift;
 always @(posedge clk or negedge rst_n)
 if(!rst_n)begin rx_meta<=1;rx_sync<=1;end
 else begin rx_meta<=rx;rx_sync<=rx_meta;end
 always @(posedge clk or negedge rst_n)begin
 if(!rst_n)begin data<=0;valid<=0;framing_error<=0;timer<=0;state<=0;bit_index<=0;shift<=0;end
 else begin
 valid<=0;framing_error<=0;
 case(state)
 0:if(!rx_sync)begin timer<=TICKS/2-1;state<=1;end
 1:if(timer!=0)timer<=timer-1'b1;else if(rx_sync)state<=0;
   else begin timer<=TICKS-1;bit_index<=0;state<=2;end
 2:if(timer!=0)timer<=timer-1'b1;else begin
   shift[bit_index]<=rx_sync;timer<=TICKS-1;
   if(bit_index==7)state<=3;else bit_index<=bit_index+1'b1;end
 3:if(timer!=0)timer<=timer-1'b1;else begin
   if(rx_sync)begin data<=shift;valid<=1;end else framing_error<=1;
   state<=0;end
 endcase
 end end
endmodule
