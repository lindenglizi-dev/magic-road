module key_mode_control #(parameter integer DEBOUNCE_CYCLES=2100000)(
 input wire clk,rst_n,input wire uart_valid,input wire [3:0] uart_mode,input wire unlocked,input wire [3:0] keys_n,output reg [3:0] mode);
 (* ASYNC_REG="TRUE" *) reg [3:0] sync1,sync2;
 reg [3:0] stable,press;
 localparam CW=$clog2(DEBOUNCE_CYCLES+1);
 reg [CW-1:0] count[0:3];integer k;
 always @(posedge clk or negedge rst_n)begin
 if(!rst_n)begin sync1<=15;sync2<=15;stable<=15;press<=0;
 for(k=0;k<4;k=k+1)count[k]<=0;end
 else begin sync1<=keys_n;sync2<=sync1;press<=0;
 for(k=0;k<4;k=k+1)begin
 if(sync2[k]==stable[k])count[k]<=0;
 else if(count[k]==DEBOUNCE_CYCLES-1)begin
 count[k]<=0;stable[k]<=sync2[k];press[k]<=!sync2[k];end
 else count[k]<=count[k]+1'b1;
 end end end
 // 0 original; 1..11 in catalogue order. Local keys win same-cycle UART.
 always @(posedge clk or negedge rst_n)begin
 if(!rst_n)mode<=0;
 else if(press[3])mode<=mode==0?1:0;
 else if(unlocked && mode!=0 && press[2])mode<=1;
 else if(unlocked && mode!=0 && press[0])mode<=mode==1?11:mode-1'b1;
 else if(unlocked && mode!=0 && press[1])mode<=mode==11?1:mode+1'b1;
 else if(uart_valid && uart_mode<=11)mode<=uart_mode;
 end
endmodule
