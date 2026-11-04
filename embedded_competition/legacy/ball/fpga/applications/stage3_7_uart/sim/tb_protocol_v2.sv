`timescale 1ns/1ps
module tb_protocol_v2;
 reg clk=0;always #10 clk=~clk;
 reg rst=0,v=0,framing=0;reg [7:0] data=0;wire [3:0] mode;wire mv;
 uart_mode_protocol dut(.clk(clk),.rst_n(rst),.data(data),.valid(v),.framing_error(framing),.mode(mode),.mode_valid(mv));
 integer count=0;reg [3:0] last=0;
 always @(posedge clk)if(mv)begin count=count+1;last=mode;end
 task ticks(input integer n);repeat(n)@(negedge clk);endtask
 task send(input [7:0] b);begin data=b;v=1;ticks(1);v=0;ticks(1);end endtask
 function automatic [15:0] crc(input [15:0] old,input [7:0] b);
 reg [15:0] c;begin c=old^{b,8'b0};repeat(8)c=c[15]?(c<<1)^16'h1021:c<<1;return c;end endfunction
 task packet(input [7:0] version,value,input bit bad=0,input [7:0] command=1,ending=10);
 reg [15:0] c;begin
 c=crc(crc(crc(crc(crc(16'hffff,version),0),command),1),value);
 send(8'haa);send(8'h55);send(version);send(0);send(command);send(1);send(value);
 send(c[7:0]^{7'b0,bad});send(c[15:8]);send(13);send(ending);ticks(3);
 end endtask
 initial begin
 ticks(4);rst=1;ticks(4);
 for(integer n=0;n<12;n=n+1)begin packet(2,n);if(count!=n+1||last!=n)$fatal(1,"mode map");end
 packet(1,0);packet(2,12);packet(2,255);packet(2,0,1);packet(2,0,0,3);packet(2,0,0,1,11);
 if(count!=12)$fatal(1,"bad frame executed");
 send(8'haa);send(8'h55);send(2);ticks(1000010);
 // Without reset, a complete frame after the actual 20ms timeout must succeed.
 packet(2,4);if(count!=13||last!=4)$fatal(1,"timeout recovery");
 $display("PASS protocol V2 0..11, V1 rejection, invalid mode/CMD/CRC/trailer and actual 20ms timeout");$finish;
 end
endmodule
