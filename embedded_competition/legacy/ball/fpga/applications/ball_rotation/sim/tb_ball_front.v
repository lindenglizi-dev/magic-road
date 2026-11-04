`timescale 1ns / 1ps
module tb_ball_front;
    reg clk=0;
    always #5 clk=!clk;
    reg rstn=0,valid=0,early=0,strict=0;
    reg [95:0] rgb=0;
    wire out_valid,sof,eol,eof,error;
    wire [7:0] labels;
    wire [2:0] hits;
    wire [11:0] x,y;
    ball_stream_front #(.C_WIDTH(16),.C_HEIGHT(1),.C_X_MIN(0),.C_Y_MIN(0),.C_X_END(16),.C_Y_END(1),
        .C_GATE_MIN(0),.C_GATE_END(16)) dut(.i_clk(clk),.i_rstn(rstn),.i_rgb(rgb),.i_valid(valid),.i_early(early),
        .i_strict(strict),.i_epoch(16'd9),.o_rgb(),.o_valid(out_valid),.o_sof(sof),.o_eol(eol),.o_eof(eof),
        .o_x(x),.o_y(y),.o_labels(labels),.o_gate_hits(hits),.o_epoch(),.o_error(error));
    task group;
        input [95:0] pixels;
        input start;
        input [7:0] expected_labels;
        input [2:0] expected_hits;
        input integer expected_x;
        begin
            @(negedge clk); valid=1; early=start; rgb=pixels;
            @(negedge clk); valid=0; early=0;
            @(posedge clk); #1;
            if(!out_valid || labels !== expected_labels || hits !== expected_hits || x != expected_x || y != 0)begin
                $fatal(1,"classification/lane order expected=%h got=%h",expected_labels,labels);
            end
            if(sof != start || eol != (expected_x == 12) || eof != (expected_x == 12))begin $fatal(1,"front markers"); end
            @(negedge clk); valid=0; early=0;
        end
    endtask
    initial begin
        repeat(4)@(negedge clk); rstn=1;
        group({24'hff0000,24'hff0000,24'h00ff00,24'h00ff00},1,8'hf5,4,0);
        repeat(3)@(negedge clk);
        if(out_valid)begin $fatal(1,"invalid gap advanced data"); end
        group({24'h0000ff,24'h808080,24'h780000,24'h000000},0,8'h00,0,4);
        group({24'hfffa00,24'hfffa00,24'hffffff,24'h00ff00},0,8'h0a,2,8);
        group({4{24'hff0000}},0,8'h55,4,12);
        strict=1;
        group({24'h780000,24'hc80000,24'hfffa00,24'h00ff00},1,8'he4,3,0);
        group({4{24'hffffff}},0,0,0,4);
        group({4{24'h0000ff}},0,0,0,8);
        group({4{24'h00ff00}},0,8'hff,4,12);
        if(error)begin $fatal(1,"unexpected frame error"); end
        $display("PASS ball front: RGB/strict presets, nine-bit yellow compare, lane order, gaps, early+valid, final group");
        $finish;
    end
endmodule
