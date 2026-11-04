`timescale 1ns / 1ps
module tb_ball_components;
    reg clk=0;
    always #5 clk=!clk;
    reg rstn=0,valid=0,sof=0,eof=0;
    reg [11:0] x=0,y=0;
    reg [7:0] labels=0;
    reg [2:0] hits=0;
    reg [15:0] epoch=0;
    wire start,candidate,done,overflow,fault,error;
    wire [1:0] color;
    wire [19:0] area,gate_pixels,diag_area;
    wire [11:0] left,right,top,bottom,diag_width,diag_height;
    wire [15:0] out_epoch;
    wire [3:0] diag_count,diag_reject;
    wire [6:0] diag_fill;
    reg [7:0] inputs[0:81919];
    reg [63:0] headers[0:15];
    reg [71:0] expected_candidates[0:127];
    integer frame_index=-1,word_index,row,group_index,lane,seen=0,finished=0,cycles=0,start_cycle=0;
    integer gate_expected=0,wait_count,max_queue=0;
    reg [71:0] actual_candidate;
    reg [63:0] actual_header;
    ball_components #(.C_WIDTH(160),.C_HEIGHT(128),.C_X_MIN(8),.C_Y_MIN(8),.C_X_END(152),.C_Y_END(120),
        .C_MIN_AREA(32),.C_MIN_SIZE(8),.C_MAX_SIZE(96)) dut(
        .i_clk(clk),.i_rstn(rstn),.i_session_clear(1'b0),.i_valid(valid),.i_sof(sof),.i_eof(eof),.i_x(x),.i_y(y),
        .i_labels(labels),.i_gate_hits(hits),.i_epoch(epoch),
        .o_frame_start(start),.o_candidate_valid(candidate),.o_color(color),.o_area(area),
        .o_x_min(left),.o_x_max(right),.o_y_min(top),.o_y_max(bottom),.o_frame_done(done),
        .o_gate_pixels(gate_pixels),.o_epoch(out_epoch),.o_overflow(overflow),.o_fault(fault),.o_error(error),
        .o_diag_count(diag_count),.o_diag_width(diag_width),.o_diag_height(diag_height),
        .o_diag_area(diag_area),.o_diag_fill(diag_fill),.o_diag_reject(diag_reject));
    always @(posedge clk)begin
        cycles=cycles+1;
        #1;
        if(rstn)begin
            if(error || fault)begin $fatal(1,"unexpected frame collision f=%0d state=%0d",frame_index,dut.state_current);end
            if(dut.cnt_queue > max_queue)begin max_queue=dut.cnt_queue;end
            if(start)begin
                seen=0;start_cycle=cycles;
                if(out_epoch !== 17+frame_index)begin $fatal(1,"epoch mismatch");end
            end
            if(candidate)begin
                actual_candidate={2'd0,bottom,top,right,left,area,color};
                if(seen >= 8 || actual_candidate !== expected_candidates[frame_index*8+seen])begin
                    $display("actual=%018x expected=%018x",actual_candidate,expected_candidates[frame_index*8+seen]);
                    $fatal(1,"candidate mismatch frame=%0d index=%0d",frame_index,seen);
                end
                seen=seen+1;
            end
            if(done)begin
                actual_header={4'd0,diag_reject,diag_fill,diag_area,diag_height,diag_width,overflow,diag_count};
                if(actual_header !== headers[frame_index] || seen !== diag_count || gate_pixels !== gate_expected)begin
                    $display("actual=%016x expected=%016x gate=%0d/%0d",actual_header,headers[frame_index],gate_pixels,gate_expected);
                    $fatal(1,"diagnostic mismatch frame=%0d",frame_index);
                end
                if(cycles-start_cycle > 40*1008+128)begin $fatal(1,"processing bound exceeded");end
                $display("COMPONENT frame=%0d N=%0d W=%0d H=%0d A=%0d F=%0d R=%x overflow=%0d cycles=%0d",
                    frame_index,diag_count,diag_width,diag_height,diag_area,diag_fill,diag_reject,overflow,cycles-start_cycle);
                finished=finished+1;
            end
        end
    end
    initial begin
        $readmemh("sim/component_frames.hex",inputs);
        $readmemh("sim/component_headers.hex",headers);
        $readmemh("sim/component_candidates.hex",expected_candidates);
        repeat(5)@(negedge clk);rstn=1;
        for(frame_index=0;frame_index<16;frame_index=frame_index+1)begin
            gate_expected=0;epoch=17+frame_index;
            for(row=0;row<128;row=row+1)begin
                for(group_index=0;group_index<40;group_index=group_index+1)begin
                    x=group_index*4;y=row;
                    labels=inputs[frame_index*5120+row*40+group_index];hits=0;
                    for(lane=0;lane<4;lane=lane+1)begin
                        if(x+lane >= 56 && x+lane < 104 && y >= 8 && y < 120 && labels[lane*2 +:2] != 0)begin hits=hits+1'b1;end
                    end
                    gate_expected=gate_expected+hits;
                    valid=1;sof=row == 0 && group_index == 0;eof=row == 127 && group_index == 39;
                    @(negedge clk);
                    if(group_index == 13)begin valid=0;sof=0;eof=0;repeat(2)@(negedge clk);end
                end
                valid=0;sof=0;eof=0;repeat(3)@(negedge clk);
            end
            wait_count=0;
            while(finished <= frame_index && wait_count < 60000)begin @(negedge clk);wait_count=wait_count+1;end
            if(finished <= frame_index)begin $fatal(1,"frame timeout");end
            repeat(4)@(negedge clk);
        end
        $display("PASS components: 16 model vectors, candidates/area/diagnostics/gate/epochs/bubbles; max queue=%0d",max_queue);
        $finish;
    end
    initial begin #30000000;$fatal(1,"global timeout");end
endmodule
