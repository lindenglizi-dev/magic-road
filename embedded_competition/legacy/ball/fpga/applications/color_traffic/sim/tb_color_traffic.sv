`timescale 1ns/1ps
module tb_color_traffic;
 reg clk=0;always #5 clk=~clk;
 reg rst=0,valid=0,early=0,traffic=1,strict=0,mask=0;
 reg [95:0] rgb=0;
 wire [95:0] out_rgb;wire v,u,l,d,error;
 wire [2:0] result,frame_result;wire [31:0] rc,yc,gc,bc;
 wire [127:0] packed_data;wire pv,pl,pd,pe;
 integer words=0,lines=0,frames=0,pixels=0,starts=0;
 color_traffic_core #(.W(160),.H(64),.X0(40),.Y0(8),.X1(160),.Y1(64),.MIN_PIXELS(8),.DOM_MARGIN(4)) dut
 (.clk(clk),.rst_n(rst),.rgb(rgb),.valid(valid),.early(early),.traffic(traffic),.strict(strict),.mask(mask),
 .out_rgb(out_rgb),.out_valid(v),.out_user(u),.out_last(l),.out_done(d),.result(result),.frame_result(frame_result),
 .red_count(rc),.yellow_count(yc),.green_count(gc),.blue_count(bc),.error(error));
 rgb96_pack128_valid packer(.I_clk(clk),.I_rst_n(rst),.I_rgb(out_rgb),.I_valid(v),.I_user(u),.I_last(l),.I_done(d),
 .O_data(packed_data),.O_valid(pv),.O_last(pl),.O_done(pd),.O_error(pe));
 reg [255:0] bytes_pending=0;integer nbytes=0;
 always @(posedge clk)begin
 // Inputs accepted by packer on this edge, output observed after NBA.
 if(v)begin
 bytes_pending=(bytes_pending<<96)|out_rgb;nbytes=nbytes+12;
 pixels=pixels+4;if(u)starts=starts+1;
 end
 #1;
 if(pv)begin
 if(nbytes<16)$fatal(1,"unexpected packed word");
 if(packed_data !== 128'(bytes_pending >> ((nbytes-16)*8)))$fatal(1,"DDR byte order");
 nbytes=nbytes-16;
 bytes_pending=bytes_pending & ((256'b1 << (nbytes*8))-1);
 words=words+1;if(pl)lines=lines+1;if(pd)frames=frames+1;
 end
 end
 task send_frame(input [23:0] color,input [2:0] expected_frame,input [2:0] expected_vote);
 integer row,col,w0,l0,p0,f0,s0;
 begin
 w0=words;l0=lines;p0=pixels;f0=frames;s0=starts;
 @(negedge clk);early=1;
 @(negedge clk);early=0;repeat(8)@(negedge clk);
 for(row=0;row<64;row=row+1)begin
 for(col=0;col<40;col=col+1)begin
 valid=1;rgb={4{color}};@(negedge clk);
 if(col==13)begin valid=0;repeat(2)@(negedge clk);end
 end
 valid=0;repeat(4)@(negedge clk);
 end
 repeat(8)@(negedge clk);
 if(frame_result!==expected_frame || result!==expected_vote)$fatal(1,"class got %d/%d expected %d/%d",frame_result,result,expected_frame,expected_vote);
 if(words-w0!=1920 || lines-l0!=64 || pixels-p0!=10240 || frames-f0!=1 || starts-s0!=1 || nbytes!=0)$fatal(1,"stream counts");
 if(error || pe)$fatal(1,"protocol error");
 case(expected_frame)
 1:if(rc!=6720)$fatal(1,"red count %d",rc);
 2:if(yc!=6720)$fatal(1,"yellow count");
 3:if(gc!=6720)$fatal(1,"green count");
 4:if(bc!=6720)$fatal(1,"blue count");
 endcase
 end endtask
 initial begin
 repeat(4)@(negedge clk);rst=1;
 send_frame(24'hff0000,1,0);send_frame(24'hff0000,1,0);send_frame(24'hff0000,1,1);
 send_frame(24'h00ff00,3,1);send_frame(24'h00ff00,3,3);
 send_frame(24'hffff00,2,3);send_frame(24'hffff00,2,2);
 send_frame(24'hffffff,0,2);send_frame(24'h000000,0,0);
 send_frame(24'h0000ff,0,0);
 traffic=0;
 send_frame(24'h0000ff,4,0);send_frame(24'h0000ff,4,0);send_frame(24'h0000ff,4,4);
 strict=1;
 send_frame(24'h780000,0,0);send_frame(24'h780000,0,0);send_frame(24'h780000,0,0);
 $display("PASS color traffic: 16 frames, ROI counts, voting, presets, blanking, markers and DDR bytes");$finish;
 end
 initial begin #10000000;$fatal(1,"timeout");end
endmodule
