`timescale 1ns/1ps
module tb_source_select;
 reg clk=0;always #5 clk=~clk;
 reg rst=0,target=0,busy=0,pc_frame=0,cv=0,ce=0,pv=0,pe=0;
 wire source,valid,early,last;wire [95:0] rgb;
 image_source_mux dut(.clk(clk),.rst_n(rst),.target(target),.runtime_busy(busy),.pc_in_frame(pc_frame),
 .camera_rgb({4{24'h123456}}),.camera_valid(cv),.camera_early(ce),.camera_last(1'b0),
 .pc_rgb({4{24'habcd01}}),.pc_valid(pv),.pc_early(pe),.pc_last(1'b0),.source(source),.rgb(rgb),.valid(valid),.early(early),.last(last));
 task step;@(negedge clk);endtask
 initial begin
 step();rst=1;cv=1;step();if(valid)$fatal(1,"camera enabled midframe after reset");
 ce=1;step();ce=0;busy=1;step();if(!valid||source)$fatal(1,"camera early not armed");
 target=1;repeat(4)step();if(source)$fatal(1,"source switched while processing frame");
 busy=0;step();if(!source)$fatal(1,"source did not switch between frames");
 pc_frame=1;busy=1;pv=1;pe=1;#1;if(!valid||!early||rgb!=={4{24'habcd01}})$fatal(1,"PC RGB/markers");
 step();pe=0;target=0;repeat(4)step();if(!source)$fatal(1,"source switched in PC frame");
 busy=0;step();if(!source)$fatal(1,"source ignored PC inflight flag");
 pc_frame=0;step();if(source||valid)$fatal(1,"camera return accepted partial frame");
 ce=1;#1;if(!early||!valid)$fatal(1,"new camera early blocked");step();ce=0;step();
 if(!valid||rgb!=={4{24'h123456}})$fatal(1,"camera resume");
 $display("PASS source select: frame drain, PC in-flight protection, camera re-arm and RGB/marker routing");$finish;
 end
 initial begin #10000;$fatal(1,"source timeout");end
endmodule
