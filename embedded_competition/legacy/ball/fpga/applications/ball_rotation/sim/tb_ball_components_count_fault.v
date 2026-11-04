`timescale 1ns / 1ps
module tb_ball_components_count_fault;
    reg clk=0;always #5 clk=!clk;
    reg rstn=0,valid=0,sof=0,eof=0;
    reg [11:0] x=0,y=0;reg [7:0] labels=0;reg [2:0] hits=0;
    wire start,candidate,done,overflow,fault,error;
    wire [1:0] color;wire [11:0] left,right,top,bottom;
    wire [19:0] gate_pixels;
    wire [31:0] red;wire [33:0] total;wire [2:0] state,reason;
    integer frame,row,group_index,lane,px,patch,finished=0,wait_count;
    ball_components #(.C_WIDTH(320),.C_HEIGHT(128),.C_X_MIN(0),.C_Y_MIN(0),.C_X_END(320),.C_Y_END(128)) detector(
        .i_clk(clk),.i_rstn(rstn),.i_session_clear(1'b0),.i_valid(valid),.i_sof(sof),.i_eof(eof),.i_x(x),.i_y(y),.i_labels(labels),.i_gate_hits(hits),.i_epoch(16'd0),
        .o_frame_start(start),.o_candidate_valid(candidate),.o_color(color),.o_area(),.o_x_min(left),.o_x_max(right),.o_y_min(top),.o_y_max(bottom),
        .o_frame_done(done),.o_gate_pixels(gate_pixels),.o_epoch(),.o_overflow(overflow),.o_fault(fault),.o_error(error),
        .o_diag_count(),.o_diag_width(),.o_diag_height(),.o_diag_area(),.o_diag_fill(),.o_diag_reject());
    ball_gate_counter #(.C_GATE_MIN(136),.C_GATE_END(184),.C_GATE_TOP(0),.C_GATE_BOTTOM(128),.C_LINE(160),.C_HYST(4)) counter(
        .i_clk(clk),.i_rstn(rstn),.i_clear(1'b0),.i_clear_counts(1'b0),.i_fault(fault),.i_frame_start(start),
        .i_candidate_valid(candidate),.i_color(color),.i_x_min(left),.i_x_max(right),.i_y_min(top),.i_y_max(bottom),
        .i_frame_done(done),.i_overflow(overflow),.i_gate_pixels(gate_pixels),.o_red(red),.o_yellow(),.o_green(),.o_total(total),
        .o_state(state),.o_empty(),.o_event(),.o_reason(reason),.o_center_x(),.o_center_y());
    always @(posedge clk)begin #1;if(done)finished=finished+1;if(rstn && error)$fatal(1,"count fault test protocol error");end
    initial begin
        repeat(5)@(negedge clk);rstn=1;
        for(frame=0;frame<6;frame=frame+1)begin
            for(row=0;row<128;row=row+1)begin
                for(group_index=0;group_index<80;group_index=group_index+1)begin
                    x=group_index*4;y=row;labels=0;hits=0;
                    for(lane=0;lane<4;lane=lane+1)begin
                        px=x+lane;
                        if(frame>=3 && row>=40 && row<52 &&
                           ((frame<5 && px>=144 && px<156) || (frame==5 && px>=164 && px<176)))labels[lane*2 +:2]=1;
                        if(frame==5 && row>=80 && row<92)begin
                            for(patch=0;patch<8;patch=patch+1)begin
                                if(px>=(patch<4 ? 16+patch*32 : 208+(patch-4)*32) &&
                                   px<(patch<4 ? 28+patch*32 : 220+(patch-4)*32))labels[lane*2 +:2]=1;
                            end
                        end
                        if(px>=136 && px<184 && labels[lane*2 +:2]!=0)hits=hits+1'b1;
                    end
                    valid=1;sof=row==0 && group_index==0;eof=row==127 && group_index==79;
                    @(negedge clk);
                end
                valid=0;sof=0;eof=0;@(negedge clk);
            end
            wait_count=0;while(finished<=frame && wait_count<50000)begin @(negedge clk);wait_count=wait_count+1;end
            if(wait_count==50000)$fatal(1,"count fault frame timeout");
            repeat(4)@(negedge clk);
            if(frame==2 && state!=1)$fatal(1,"gate not ready");
            if(frame==4 && state!=2)$fatal(1,"gate not armed before overflow");
        end
        if(!overflow || state!=4 || reason!=1 || red!=0 || total!=0)$fatal(1,"overflow frame produced a count");
        $display("PASS components -> counter: downstream candidate emitted in an overflowing frame cannot increment an armed counter");
        $finish;
    end
    initial begin #20000000;$fatal(1,"count fault timeout");end
endmodule
