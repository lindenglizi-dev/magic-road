`timescale 1ns / 1ps
// Python独立模型向量与正式两拍前端逐组对照，包含strict及跨帧切换。
module tb_ball_color_support;
    reg clk=0;always #5 clk=!clk;
    reg rstn=0,valid=0,early=0,strict=0;
    reg [95:0] rgb=0;
    wire [95:0] output_rgb;
    wire output_valid,sof,eol,eof,error;
    wire [7:0] labels;
    wire [2:0] hits;
    wire [11:0] x,y;
    wire [15:0] epoch;
    ball_stream_front #(.C_WIDTH(16),.C_HEIGHT(1),.C_X_MIN(0),.C_Y_MIN(0),
        .C_X_END(16),.C_Y_END(1),.C_GATE_MIN(0),.C_GATE_END(16)) dut(
        .i_clk(clk),.i_rstn(rstn),.i_rgb(rgb),.i_valid(valid),.i_early(early),.i_strict(strict),.i_epoch(16'h4321),
        .o_rgb(output_rgb),.o_valid(output_valid),.o_sof(sof),.o_eol(eol),.o_eof(eof),
        .o_x(x),.o_y(y),.o_labels(labels),.o_gate_hits(hits),.o_epoch(epoch),.o_error(error));
    integer fd,scanned,strict_value,index=0,lane,expected_hits;
    reg [95:0] pixels;
    reg [7:0] expected;
    initial begin
        fd=$fopen("sim/color_support_vectors.txt","r");if(fd==0)$fatal(1,"Missing independent model vectors");
        repeat(4)@(negedge clk);rstn=1;
        while(!$feof(fd))begin
            scanned=$fscanf(fd,"%d %h %h\n",strict_value,pixels,expected);
            if(scanned==3)begin
                @(negedge clk);rgb=pixels;strict=strict_value;valid=1;early=index%4==0;
                @(posedge clk);#1;
                if(output_valid)$fatal(1,"Front changed to one-clock latency");
                @(negedge clk);valid=0;early=0;
                @(posedge clk);#1;
                expected_hits=0;for(lane=0;lane<4;lane=lane+1)if(expected[lane*2 +:2]!=0)expected_hits=expected_hits+1;
                if(!output_valid || labels!==expected || hits!=expected_hits || output_rgb!==pixels ||
                   x!=(index%4)*4 || y!=0 || epoch!=16'h4321 || sof!=(index%4==0) ||
                   eol!=(index%4==3) || eof!=(index%4==3) || error)
                    $fatal(1,"Support vector%0d strict%0d expected%h got%h x%0d",index,strict_value,expected,labels,x);
                @(negedge clk);
                @(posedge clk);#1;if(output_valid)$fatal(1,"Invalid bubble retained valid");
                index=index+1;
            end
        end
        if(index!=2048)$fatal(1,"Vector count mismatch");
        $fclose(fd);$display("PASS color support: %0d independent group vectors, RGB/epoch/coordinates/markers, strict bypass and2clock latency",index);
        $finish;
    end
    initial begin #1000000;$fatal(1,"Color support timeout");end
endmodule
