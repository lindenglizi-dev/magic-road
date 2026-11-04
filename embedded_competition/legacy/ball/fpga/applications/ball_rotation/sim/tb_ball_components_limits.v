`timescale 1ns / 1ps
module tb_ball_components_limits;
    reg clk=0;always #5 clk=!clk;
    reg rstn=0,valid=0,sof=0,eof=0,allow_fault=0;
    reg [11:0] x=0,y=0;reg [7:0] labels=0;reg [15:0] epoch=0;
    wire [1:0] start,candidate,done,overflow,fault,error;
    wire [3:0] color;
    wire [39:0] area,diag_area;
    wire [23:0] left,right,top,bottom,diag_width,diag_height;
    wire [7:0] diag_count,diag_reject;
    wire [13:0] diag_fill;
    reg [7:0] inputs[0:25199];reg [63:0] headers[0:9];reg [71:0] expected[0:79];
    integer seen[0:1];integer finished[0:1];integer frame_index=-1,row,group_index,wait_count,which;
    reg [63:0] header;reg [71:0] actual;
    genvar detector_index;
    generate for(detector_index=0;detector_index<2;detector_index=detector_index+1)begin:gen_detector
        ball_components #(.C_WIDTH(160),.C_HEIGHT(126),.C_X_MIN(3),.C_Y_MIN(2),.C_X_END(157),.C_Y_END(126),
            .C_MIN_AREA(32),.C_MIN_SIZE(8),.C_MAX_SIZE(384),.C_QUEUE_BITS(detector_index == 0 ? 12 : 1)) dut(
            .i_clk(clk),.i_rstn(rstn),.i_session_clear(1'b0),.i_valid(valid),.i_sof(sof),.i_eof(eof),.i_x(x),.i_y(y),
            .i_labels(labels),.i_gate_hits(3'd0),.i_epoch(epoch),.o_frame_start(start[detector_index]),
            .o_candidate_valid(candidate[detector_index]),.o_color(color[detector_index*2 +:2]),.o_area(area[detector_index*20 +:20]),
            .o_x_min(left[detector_index*12 +:12]),.o_x_max(right[detector_index*12 +:12]),
            .o_y_min(top[detector_index*12 +:12]),.o_y_max(bottom[detector_index*12 +:12]),.o_frame_done(done[detector_index]),
            .o_gate_pixels(),.o_epoch(),.o_overflow(overflow[detector_index]),.o_fault(fault[detector_index]),.o_error(error[detector_index]),
            .o_diag_count(diag_count[detector_index*4 +:4]),.o_diag_width(diag_width[detector_index*12 +:12]),
            .o_diag_height(diag_height[detector_index*12 +:12]),.o_diag_area(diag_area[detector_index*20 +:20]),
            .o_diag_fill(diag_fill[detector_index*7 +:7]),.o_diag_reject(diag_reject[detector_index*4 +:4]));
    end endgenerate
    always @(posedge clk)begin
        #1;
        if(rstn && !allow_fault)begin
            if(error != 0 || fault != 0)$fatal(1,"unexpected protocol fault");
            for(which=0;which<2;which=which+1)begin
                if(start[which])seen[which]=0;
                if(candidate[which])begin
                    actual={2'd0,bottom[which*12 +:12],top[which*12 +:12],right[which*12 +:12],left[which*12 +:12],area[which*20 +:20],color[which*2 +:2]};
                    if(actual !== expected[(frame_index*2+which)*8+seen[which]])$fatal(1,"partial ROI candidate mismatch f%0d detector_index%0d",frame_index,which);
                    seen[which]=seen[which]+1;
                end
                if(done[which])begin
                    header={4'd0,diag_reject[which*4 +:4],diag_fill[which*7 +:7],diag_area[which*20 +:20],
                        diag_height[which*12 +:12],diag_width[which*12 +:12],overflow[which],diag_count[which*4 +:4]};
                    if(header !== headers[frame_index*2+which])begin
                        $display("header %016x/%016x",header,headers[frame_index*2+which]);
                        $fatal(1,"partial diagnostic mismatch f%0d detector_index%0d",frame_index,which);
                    end
                    finished[which]=finished[which]+1;
                end
            end
        end
    end
    task send_frame;
        input integer selected;
        begin
            for(row=0;row<126;row=row+1)begin
                for(group_index=0;group_index<40;group_index=group_index+1)begin
                    x=group_index*4;y=row;labels=inputs[selected*5040+row*40+group_index];
                    valid=1;sof=row==0 && group_index==0;eof=row==125 && group_index==39;
                    @(negedge clk);
                    if(group_index==7)begin valid=0;sof=0;eof=0;repeat(2)@(negedge clk);end
                end
                valid=0;sof=0;eof=0;@(negedge clk);
            end
        end
    endtask
    initial begin
        seen[0]=0;seen[1]=0;finished[0]=0;finished[1]=0;
        $readmemh("sim/component_partial_frames.hex",inputs);
        $readmemh("sim/component_partial_headers.hex",headers);
        $readmemh("sim/component_partial_candidates.hex",expected);
        repeat(5)@(negedge clk);rstn=1;
        for(frame_index=0;frame_index<5;frame_index=frame_index+1)begin
            epoch=frame_index+32;send_frame(frame_index);wait_count=0;
            while((finished[0]<=frame_index || finished[1]<=frame_index) && wait_count<70000)begin
                @(negedge clk);wait_count=wait_count+1;
            end
            if(wait_count==70000)$fatal(1,"partial ROI timeout");
            repeat(5)@(negedge clk);
        end
        // 故意给出超过统计吞吐的帧率：必须报告冲突而非静默覆盖活动帧。
        allow_fault=1;send_frame(1);send_frame(1);send_frame(1);
        repeat(5)@(negedge clk);
        if(!error[0])$fatal(1,"capture collision was not reported");
        $display("PASS component limits: partial ROI/last partial row, 4-vs3 support, queue overflow/recovery, busy collision");
        $finish;
    end
    initial begin #20000000;$fatal(1,"limits timeout");end
endmodule
