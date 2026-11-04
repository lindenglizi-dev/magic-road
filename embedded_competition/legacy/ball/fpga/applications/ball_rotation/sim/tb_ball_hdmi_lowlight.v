`timescale 1ns / 1ps
module tb_ball_hdmi_lowlight;
    reg clk=0;
    always #5 clk=!clk;
    reg rstn=0,valid=0,user=0;
    reg [95:0] rgb=0;
    wire [127:0] data;
    wire out_valid,last,done,error;
    wire [1:0] track_status;
    integer words=0,lines=0,frames=0,capture_file;
    wire [95:0] gamma_rgb;
    wire gamma_valid,gamma_user;
    axis_gamma_rgb96 gamma_Inst(.I_clk(clk),.I_rst_n(rstn),.I_tlast(1'b0),.I_tuser(user),
        .I_tdata(rgb),.I_tvalid(valid),.O_tlast(),.O_tuser(gamma_user),.O_tdata(gamma_rgb),.O_tvalid(gamma_valid));
    ball_runtime dut(.I_clk(clk),.I_rst_n(rstn),.I_camera_status({8'd0,1'b1,1'b1,2'd1,8'h16,16'h0480,12'h060}),.I_keys_n(4'hf),.I_rgb(gamma_rgb),.I_valid(gamma_valid),.I_user(gamma_user),.I_last(1'b0),
        .O_data(data),.O_valid(out_valid),.O_last(last),.O_done(done),.O_early(),.O_error(error),
        .O_red(),.O_green(),.O_yellow(),.O_total(),.O_count_mode(),.O_gate_state(),.O_track_status(track_status));
    always @(posedge clk)begin
        #1;
        if(out_valid)begin
            words=words+1;
            if(frames == 2)begin $fwrite(capture_file,"%032x\n",data); end
            if(last)begin lines=lines+1; end
            if(done)begin
                frames=frames+1;
                if(words != frames*172800 || lines != frames*720)begin $fatal(1,"720P stream counts"); end
                $display("HDMI frame %0d: %0d words, track=%0d",frames,words,track_status);
            end
        end
    end
    task send_frame;
        input integer center;
        integer row,group_index,lane,x,shade;
        reg [23:0] pixel;
        begin
            @(negedge clk); user=1;
            @(negedge clk); user=0;
            repeat(8)@(negedge clk);
            for(row=0;row<720;row=row+1)begin
                for(group_index=0;group_index<320;group_index=group_index+1)begin
                    for(lane=0;lane<4;lane=lane+1)begin
                        x=group_index*4+lane;
                        pixel=24'h183c40;
                                                if((row-400)*(row-400)+(x-center)*(x-center) <= 10000)begin
                            shade=45+(row-300)/5;
                            pixel={shade[7:0],8'd22,8'd18};
                            if(row >= 370 && row <= 390 && x >= center+20 && x <= center+40)begin pixel=24'hc8c8c8; end
                        end
                        rgb[95-lane*24 -:24]=pixel;
                    end
                    valid=1; @(negedge clk);
                    if(group_index == 13)begin valid=0; repeat(2)@(negedge clk); end
                end
                valid=0; repeat(4)@(negedge clk);
            end
            // 连续四像素突发后留统计时间；帧率仍高于真实720P60输入。
            repeat(250000)@(negedge clk);
            if(error)begin $fatal(1,"720P error flag"); end
        end
    endtask
    initial begin
        capture_file=$fopen("sim/hdmi_motion_frame.hex","w");
        if(capture_file == 0)begin $fatal(1,"capture open failed"); end
        repeat(5)@(negedge clk); rstn=1;
        send_frame(300); send_frame(316); send_frame(332); send_frame(348);
        if(frames != 4 || track_status != 2 || dut.reg_display_x_bcd != 16'h0347 ||
           dut.reg_display_diag_count != 1 || dut.reg_display_diag_reject != 0)begin
            $fatal(1,"720P tracker/snapshot mismatch");
        end
        $fclose(capture_file);
        $display("PASS ball HDMI: 4 full 1280x720 frames, 691200 DDR words, frozen tracking OSD, actual capture");
        $finish;
    end
    initial begin #100000000; $fatal(1,"720P timeout"); end
endmodule
