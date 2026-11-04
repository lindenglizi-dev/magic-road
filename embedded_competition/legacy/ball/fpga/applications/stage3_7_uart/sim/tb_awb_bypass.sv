`timescale 1ns/1ps
// Behavioral models of vendor IP interfaces. Not a transistor/IP timing model.
module divider(input clk,rst,start,input [31:0] denominator,input [47:0] numerator,
 output [47:0] quotient,output done);
 reg [47:0] q[0:47];reg [47:0] v;integer i;
 always @(posedge clk)begin
 if(rst)begin v<=0;for(i=0;i<48;i=i+1)q[i]<=0;end
 else begin
 v<={v[46:0],start};q[0]<=denominator==0?48'd0:numerator/denominator;
 for(i=1;i<48;i=i+1)q[i]<=q[i-1];
 end end
 assign quotient=q[47];assign done=v[47];
endmodule
module blk_mem_gen_awb_delay_signal(input clka,wea,input [10:0] addra,input [95:0] dia,
 input clkb,input [10:0] addrb,output reg [95:0] dob);
 reg [95:0] mem[0:2047];
 always @(posedge clka)if(wea)mem[addra]<=dia;
 always @(posedge clkb)dob<=mem[addrb];
endmodule
module tb_awb_bypass;
 reg clk=0;always #5 clk=~clk;
 reg rst=0,valid=0,early=0;reg [95:0] rgb=0;wire [95:0] raw,balanced;wire ov,ou;
 awb #(.IMG_WIDTH(256),.IMG_HEIGHT(4)) dut(.I_clk(clk),.I_rst_n(rst),.I_tlast(1'b0),.I_tuser(early),
 .I_tdata(rgb),.I_tvalid(valid),.I_tready(),.O_tlast(),.O_tuser(ou),.O_tdata(balanced),
 .O_uncorrected(raw),.O_tvalid(ov),.O_tready(1'b1));
 reg [95:0] expected[0:255];integer sent=0,received=0,different=0;
 reg [95:0] sample_raw,sample_corrected;reg sample_valid;integer lane;
 function automatic [7:0] gain(input [7:0] c,input [19:0] coefficient);
 reg [27:0] n;begin n=c*coefficient;return n>28'd16777215 ? 8'd255 : n[23:16];end endfunction
 always @(posedge clk)begin
 if(rst)begin
 if(valid)begin expected[sent]=rgb;sent=sent+1;end
 sample_raw=dut.data_d1;sample_valid=dut.valid_d1;
 for(lane=0;lane<4;lane=lane+1)begin
 sample_corrected[lane*24+16+:8]=gain(sample_raw[lane*24+16+:8],dut.in_r_r1);
 sample_corrected[lane*24+8+:8]=sample_raw[lane*24+8+:8];
 sample_corrected[lane*24+:8]=gain(sample_raw[lane*24+:8],dut.in_b_r1);
 end
 #1;
 if(ov!==sample_valid)$fatal(1,"AWB valid latency");
 if(ov)begin
 if(received>=sent || raw!==expected[received])$fatal(1,"AWB raw bypass pixel order %d",received);
 if(balanced!==sample_corrected)$fatal(1,"AWB gain/bypass alignment");
 if(balanced!=raw)different=different+1;
 received=received+1;
 end end end
 task ticks(input integer n);repeat(n)@(negedge clk);endtask
 initial begin
 ticks(4);rst=1;ticks(4);early=1;ticks(1);early=0;ticks(20);
 for(integer row=0;row<4;row=row+1)begin
 for(integer col=0;col<64;col=col+1)begin
 rgb={24'hfa8010,24'h0050ff,24'h504032,24'h285014};
 rgb[95:88]=192+col;rgb[23:16]=32+col;
 valid=1;ticks(1);
 end
 valid=0;ticks(100);
 end
 ticks(200);
 if(sent!=256||received!=256||different<100)$fatal(1,"AWB coverage %d %d %d",sent,received,different);
 $display("PASS AWB bypass pixel order, valid/gain alignment, saturation and distinct corrected output (behavioral vendor IP)");$finish;
 end
 initial begin #1000000;$fatal(1,"AWB timeout");end
endmodule
