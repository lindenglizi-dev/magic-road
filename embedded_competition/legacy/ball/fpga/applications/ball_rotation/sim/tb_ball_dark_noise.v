`timescale 1ns / 1ps
// 从真实RGB经前端进入二维检测；成片噪声必须到达检测器再被分离。
module tb_ball_dark_noise;
    reg clk=0;always #5 clk=!clk;
    reg rstn=0,valid=0,early=0,clear_track=0;
    reg [95:0] rgb=0;
    wire front_valid,front_sof,front_eof,front_error;
    wire [11:0] front_x,front_y;
    wire [7:0] labels;
    wire [2:0] hits;
    wire [15:0] front_epoch;
    wire candidate,done,overflow,fault,error;
    wire [1:0] color;
    wire [11:0] left,right,top,bottom;
    wire start,tracked;
    wire [19:0] area;
    wire [1:0] track_status,track_color;
    wire [11:0] center_x,center_y;
    integer seen=0,expected_color=0,frames=0,noise_words=0;
    ball_stream_front #(.C_WIDTH(160),.C_HEIGHT(192),.C_X_MIN(0),.C_Y_MIN(0),
        .C_X_END(160),.C_Y_END(192),.C_GATE_MIN(56),.C_GATE_END(104)) front(
        .i_clk(clk),.i_rstn(rstn),.i_session_clear(1'b0),.i_rgb(rgb),.i_valid(valid),.i_early(early),.i_strict(1'b0),.i_epoch(16'h1234),
        .o_rgb(),.o_valid(front_valid),.o_sof(front_sof),.o_eol(),.o_eof(front_eof),
        .o_x(front_x),.o_y(front_y),.o_labels(labels),.o_gate_hits(hits),.o_epoch(front_epoch),.o_error(front_error));
    ball_components #(.C_WIDTH(160),.C_HEIGHT(192),.C_X_MIN(0),.C_Y_MIN(0),.C_X_END(160),.C_Y_END(192)) components(
        .i_clk(clk),.i_rstn(rstn),.i_valid(front_valid),.i_sof(front_sof),.i_eof(front_eof),
        .i_x(front_x),.i_y(front_y),.i_labels(labels),.i_gate_hits(hits),.i_epoch(front_epoch),
        .o_frame_start(start),.o_candidate_valid(candidate),.o_color(color),.o_area(area),
        .o_x_min(left),.o_x_max(right),.o_y_min(top),.o_y_max(bottom),.o_frame_done(done),
        .o_gate_pixels(),.o_epoch(),.o_overflow(overflow),.o_fault(fault),.o_error(error));
    ball_target_tracker tracker(.i_clk(clk),.i_rstn(rstn),.i_clear(clear_track),
        .i_frame_start(start),.i_candidate_valid(candidate),.i_color(color),.i_area(area),
        .i_x_min(left),.i_x_max(right),.i_y_min(top),.i_y_max(bottom),.i_frame_done(done),.i_overflow(overflow),
        .o_valid(tracked),.o_status(track_status),.o_color(track_color),.o_x_min(),.o_x_max(),.o_y_min(),.o_y_max(),
        .o_center_x(center_x),.o_center_y(center_y));
    always @(posedge clk)begin
        #1;
        if(candidate)begin
            seen=seen+1;
            if(color!=expected_color || left!=56 || right!=103 || top!=104 || bottom!=155)
                $fatal(1,"Dark/noise candidate color%0d bbox%0d,%0d-%0d,%0d",color,left,top,right,bottom);
        end
        if(front_valid && front_y<100 && labels!=0)noise_words=noise_words+1;
        if(rstn && (front_error || error || overflow || fault))$fatal(1,"Frame protocol error");
    end
    task frame;
        input integer ball_color,dim,noise_y;
        integer row,group,lane,px,dx,dy;
        reg [23:0] pixel,ball_pixel;
        begin
            case(ball_color)
                1:ball_pixel=dim ? 24'h3c1c18 : 24'ha03c30;
                2:ball_pixel=dim ? 24'h3c3a14 : 24'ha09830;
                3:ball_pixel=dim ? 24'h183c1c : 24'h30a03c;
                default:ball_pixel=24'h141414;
            endcase
            seen=0;noise_words=0;expected_color=ball_color;
            for(row=0;row<192;row=row+1)begin
                for(group=0;group<40;group=group+1)begin
                    @(negedge clk);
                    for(lane=0;lane<4;lane=lane+1)begin
                        px=group*4+lane;dx=px-80;dy=row-130;pixel=24'h141414;
                        if(dx*dx+dy*dy<=24*24)pixel=ball_pixel;
                        if(noise_y>=0 && row>=noise_y && row<noise_y+4 && px>=76 && px<84)
                            pixel=ball_color==1 ? 24'h14dc14 : 24'hdc1414;
                        if(noise_y>=0 && row>=noise_y+8 && row<noise_y+12 && px>=76 && px<84)pixel=ball_pixel;
                        rgb[95-lane*24 -:24]=pixel;
                    end
                    valid=1;early=row==0 && group==0;
                end
                @(negedge clk);valid=0;early=0;
                repeat(2)@(negedge clk);
            end
            wait(done);@(negedge clk);
            if(seen!=1)$fatal(1,"Ball missing/duplicated color%0d dim%0d noise_y%0d seen%0d",ball_color,dim,noise_y,seen);
            if(noise_y>=0 && noise_words==0)$fatal(1,"Noise was not injected into region detector");
            frames=frames+1;
            $display("PASS dark/noise frame color%0d dim%0d noise_y%0d box56,104-103,155 noise_words=%0d",ball_color,dim,noise_y,noise_words);
            repeat(5)@(negedge clk);
        end
    endtask
    integer c;
    initial begin
        repeat(5)@(negedge clk);rstn=1;
        for(c=1;c<=3;c=c+1)begin
            @(negedge clk);clear_track=1;
            @(negedge clk);clear_track=0;
            frame(c,0,-1);frame(c,1,70);frame(c,1,10);
            if(!tracked || track_status!=2 || track_color!=c || center_x!=79 || center_y!=129)
                $fatal(1,"Weak-ball tracker failed color%0d state%0d center%0d,%0d",c,track_status,center_x,center_y);
        end
        $display("PASS dark RGB and disconnected same/other-color patches: %0d frames3colors; CCL bounds within3pixel quantization",frames);
        $finish;
    end
    initial begin #10000000;$fatal(1,"Dark/noise timeout");end
endmodule
