`timescale 1ns/1ps
module tb_replay_1080;
 reg clk=0;always #5 clk=~clk;
 reg rst=0,pub=0,busy=0,done=0,selected=0;wire ack,valid_image,in_frame,start;
 wire [24:0] address;reg [127:0] data=0;wire [95:0] rgb;wire valid,early,last;
 pc_image_replay #(.FRAME_GAP(50)) dut(.clk(clk),.rst_n(rst),.selected(selected),.runtime_busy(busy),.publish(pub),.publish_bank(1'b0),
 .publish_ack(ack),.image_valid(valid_image),.in_frame(in_frame),.mem_start(start),.mem_address(address),.mem_busy(1'b0),.mem_done(done),.mem_result(data),
 .rgb(rgb),.valid(valid),.early(early),.last(last));
 function automatic [15:0] pixel(input integer x,y);return {5'(x%32),6'(y%64),5'((x+y)%32)};endfunction
 function automatic [23:0] expand(input [15:0] v);return {v[15:11],v[15:13],v[10:5],v[10:9],v[4:0],v[4:2]};endfunction
 integer i,n,base,x,y,groups=0,lines=0,reads=0,drain=0;
 always @(posedge clk)begin
 done<=0;
 if(start)begin
 if(address<25165824||address>=27239424||address%8!=0)$fatal(1,"1080 DDR bank range");
 base=address-25165824;
 for(i=0;i<8;i=i+1)data[i*16+:16]<=pixel((base+i)%1920,(base+i)/1920);
 done<=1;reads=reads+1;
 end
 end
 always @(negedge clk)begin
 if(early)busy=1;
 if(valid)begin
 y=groups/320;
 for(n=0;n<4;n=n+1)begin
 x=(groups%320)*4+n;
 if(rgb[95-n*24-:24]!==expand(pixel(x*3/2,y*3/2)))$fatal(1,"native replay pixel (%d,%d)",x,y);
 end
 if(last!==(groups%320==319))$fatal(1,"native line marker");
 if(last)lines=lines+1;
 groups=groups+1;
 if(groups==230400)begin selected=0;drain=20;end
 end
 if(drain>0)begin drain=drain-1;if(drain==0)busy=0;end
 end
 initial begin
 repeat(5)@(negedge clk);rst=1;pub=1;wait(ack);selected=1;wait(groups==230400);wait(!in_frame);
 if(lines!=720||reads!=172800)$fatal(1,"native dimensions/stride count");
 $display("PASS native 1080 DDR replay: 1920x1080 stride/bank, 172800 reads, all 921600 RGB pixels and 720 line boundaries match 1280x720 mapping");$finish;
 end
 initial begin #50000000;$fatal(1,"native replay timeout");end
endmodule
