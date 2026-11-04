`timescale 1ns/1ps
module tb_osd_runtime;
 reg clk=0;always #5 clk=~clk;
 reg rst=0,valid=0,early=0;reg [3:0] keys=15;
 wire [127:0] data;wire v,l,d,e,error;wire [2:0] result;
 reg [127:0] expected[0:1382399];integer index=0,lines=0,frames=0,early_count=0;
 integer frame,row,col,preview,preview_color;
 color_traffic_runtime #(.DEBOUNCE_CYCLES(4)) dut(.I_clk(clk),.I_rst_n(rst),.I_keys_n(keys),
 .I_rgb({4{24'hff0000}}),.I_valid(valid),.I_user(early),.I_last(1'b0),
 .O_data(data),.O_valid(v),.O_last(l),.O_done(d),.O_early(e),.O_error(error),.result(result));
 always @(posedge clk)begin
 #1;
 if(e)early_count=early_count+1;
 if(v)begin
 if(index>=1382400)$fatal(1,"excess output");
 if(data!==expected[index])$fatal(1,"OSD pixel mismatch word=%0d got=%h expected=%h",index,data,expected[index]);
 if(l !== (index%240==239))$fatal(1,"line marker");
 if(d !== (index%172800==172799))$fatal(1,"frame marker");
 if(index>=518400 && index<556800)$fdisplay(preview,"%032h",data);
 if(index>=1209600 && index<1248000)$fdisplay(preview_color,"%032h",data);
 index=index+1;if(l)lines=lines+1;if(d)frames=frames+1;
 end
 if(error)$fatal(1,"protocol error");
 end
 initial begin
 $readmemh("osd_expected.hex",expected);preview=$fopen("osd_actual_top.hex","w");
 preview_color=$fopen("osd_actual_color_top.hex","w");
 repeat(4)@(negedge clk);rst=1;
 for(frame=0;frame<8;frame=frame+1)begin
 early=1;@(negedge clk);early=0;repeat(60)@(negedge clk);
 for(row=0;row<720;row=row+1)begin
 // Change requested mode mid-frame. Current label must remain unchanged.
 if(row==200 && frame==3)keys=14;
 if(row==201)keys=15;
 for(col=0;col<320;col=col+1)begin
 valid=1;@(negedge clk);
 if(col==53)begin valid=0;repeat(2)@(negedge clk);end
 end
 valid=0;repeat(4)@(negedge clk);
 end
 repeat(30)@(negedge clk);
 end
 if(index!=1382400 || lines!=5760 || frames!=8 || early_count!=8)$fatal(1,"output counts");
 if(result!=1)$fatal(1,"detector changed");
 $fclose(preview);$fclose(preview_color);
 $display("PASS OSD runtime: 8 full frames, voted result text, mode change clears stale result, logo, ROI/status, DDR pixels and markers");$finish;
 end
 initial begin #30000000;$fatal(1,"timeout");end
endmodule
