`timescale 1ns / 1ps
// 同一批碎片、双候选、形状拒绝和越线帧，穿过真实二维扫描器与计数器。
module tb_ball_gate_recovery;
    reg clk=0;always #5 clk=!clk;
    reg rstn=0,valid=0,sof=0,eof=0;
    reg [11:0] x=0,y=0;reg [7:0] labels=0;reg [2:0] hits=0;
    wire start,candidate,done,overflow,fault,error,occupied;
    wire [1:0] color;wire [11:0] left,right,top,bottom;
    wire [19:0] gate_pixels;
    wire [3:0] diag_count;
    wire [31:0] red,green,yellow;wire [33:0] total;wire [2:0] state,reason;
    reg [7:0] words[0:460799];
    integer frame,row,group_index,lane,px,finished=0,wait_count,file_handle,rc;
    integer expected_raw,expected_occupied,expected_candidates,expected_overflow,expected_state,expected_reason,er,eg,ey;
    ball_components #(.C_WIDTH(320),.C_HEIGHT(128),.C_X_MIN(0),.C_Y_MIN(0),.C_X_END(320),.C_Y_END(128)
`ifndef LEGACY_GATE
        ,.C_GATE_MIN(136),.C_GATE_END(184)
`endif
    ) detector(
        .i_clk(clk),.i_rstn(rstn),.i_session_clear(1'b0),.i_valid(valid),.i_sof(sof),.i_eof(eof),.i_x(x),.i_y(y),.i_labels(labels),.i_gate_hits(hits),.i_epoch(16'd0),
        .o_frame_start(start),.o_candidate_valid(candidate),.o_color(color),.o_area(),.o_x_min(left),.o_x_max(right),.o_y_min(top),.o_y_max(bottom),
        .o_frame_done(done),.o_gate_pixels(gate_pixels),.o_epoch(),.o_overflow(overflow),.o_fault(fault),.o_error(error),
`ifndef LEGACY_GATE
        .o_gate_occupied(occupied),
`endif
        .o_diag_count(diag_count),.o_diag_width(),.o_diag_height(),.o_diag_area(),.o_diag_fill(),.o_diag_reject());
    wire [19:0] effective_gate;
`ifdef LEGACY_GATE
    assign occupied=1'b1;
    assign effective_gate=gate_pixels;
`else
    assign effective_gate=occupied ? gate_pixels : 20'd0;
`endif
    ball_gate_counter #(.C_GATE_MIN(136),.C_GATE_END(184),.C_GATE_TOP(0),.C_GATE_BOTTOM(128),.C_LINE(160),.C_HYST(4)) counter(
        .i_clk(clk),.i_rstn(rstn),.i_clear(1'b0),.i_clear_counts(1'b0),.i_fault(fault),.i_frame_start(start),
        .i_candidate_valid(candidate),.i_color(color),.i_x_min(left),.i_x_max(right),.i_y_min(top),.i_y_max(bottom),
        .i_frame_done(done),.i_overflow(overflow),.i_gate_pixels(effective_gate),.o_red(red),.o_yellow(yellow),.o_green(green),.o_total(total),
        .o_state(state),.o_empty(),.o_event(),.o_reason(reason),.o_center_x(),.o_center_y());
    always @(posedge clk)begin #1;if(done)finished=finished+1;if(rstn && error)$fatal(1,"gate recovery protocol error");end
    initial begin
        $readmemh("sim/gate_recovery_frames.hex",words);
        file_handle=$fopen("sim/gate_recovery_headers.txt","r");if(file_handle==0)$fatal(1,"headers missing");
        repeat(5)@(negedge clk);rstn=1;
        for(frame=0;frame<45;frame=frame+1)begin
            rc=$fscanf(file_handle,"%d %d %d %d %d %d %d %d %d\n",expected_raw,expected_occupied,expected_candidates,expected_overflow,expected_state,expected_reason,er,eg,ey);
            if(rc!=9)$fatal(1,"header count %0d",rc);
            for(row=0;row<128;row=row+1)begin
                for(group_index=0;group_index<80;group_index=group_index+1)begin
                    x=group_index*4;y=row;labels=words[frame*10240+row*80+group_index];hits=0;
                    for(lane=0;lane<4;lane=lane+1)begin
                        px=x+lane;if(px>=136 && px<184 && labels[lane*2 +:2]!=0)hits=hits+1'b1;
                    end
                    valid=1;sof=row==0 && group_index==0;eof=row==127 && group_index==79;@(negedge clk);
                end
                valid=0;sof=0;eof=0;@(negedge clk);
            end
            wait_count=0;while(finished<=frame && wait_count<100000)begin @(negedge clk);wait_count=wait_count+1;end
            if(wait_count==100000)$fatal(1,"frame timeout");repeat(4)@(negedge clk);
            if(gate_pixels!==expected_raw[19:0] || diag_count!==expected_candidates[3:0] || overflow!==expected_overflow[0])
                $fatal(1,"frame %0d metadata mismatch",frame);
`ifndef LEGACY_GATE
            if(occupied!==expected_occupied[0])$fatal(1,"frame %0d gate occupancy mismatch",frame);
`endif
            if(state!==expected_state[2:0] || reason!==expected_reason[2:0] || red!==er || green!==eg || yellow!==ey)
                $fatal(1,"frame %0d gate=%0d err=%0d expected=%0d/%0d counts=%0d/%0d/%0d expected=%0d/%0d/%0d raw=%0d busy=%0d",
                    frame,state,reason,expected_state,expected_reason,red,green,yellow,er,eg,ey,gate_pixels,occupied);
        end
        $fclose(file_handle);
        if(total!=3)$fatal(1,"total mismatch");
        $display("PASS gate recovery:45 frames; sparse noise recovery, rejected-region hold, dropout dedup, color mismatch and overflow; red2 green1 yellow0");
        $finish;
    end
    initial begin #200000000;$fatal(1,"gate recovery timeout");end
endmodule
