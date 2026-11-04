`timescale 1ns / 1ps
module tb_ball_count_hdmi;
    reg clk=0;
    always #5 clk=!clk;
    reg rstn=0,valid=0,user=0;
    reg [3:0] keys=15;
    reg [95:0] rgb=0;
    wire [127:0] data;
    wire out_valid,last,done,error;
    wire [1:0] track_status;
    wire mode;wire [2:0] gate_state;wire [31:0] red,green,yellow;wire [33:0] total;
    integer words=0,lines=0,frames=0,capture_file;
    wire [95:0] gamma_rgb;
    wire gamma_valid,gamma_user;
    axis_gamma_rgb96 gamma_Inst(.I_clk(clk),.I_rst_n(rstn),.I_tlast(1'b0),.I_tuser(user),
        .I_tdata(rgb),.I_tvalid(valid),.O_tlast(),.O_tuser(gamma_user),.O_tdata(gamma_rgb),.O_tvalid(gamma_valid));
    ball_runtime #(.C_FACE_GATE(0),.C_DEBOUNCE(3)) dut(.I_clk(clk),.I_rst_n(rstn),.I_camera_status({8'd0,1'b1,1'b1,2'd1,8'h16,16'h0480,12'h060}),.I_keys_n(keys),.I_rgb(gamma_rgb),.I_valid(gamma_valid),.I_user(gamma_user),.I_last(1'b0),
        .O_data(data),.O_valid(out_valid),.O_last(last),.O_done(done),.O_early(),.O_error(error),
        .O_red(red),.O_green(green),.O_yellow(yellow),.O_total(total),.O_count_mode(mode),.O_gate_state(gate_state),.O_track_status(track_status));
    always @(posedge clk)begin
        #1;
        if(out_valid)begin
            words=words+1;
            if(frames == 6)begin $fwrite(capture_file,"%032x\n",data); end
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
                            pixel={shade[7:0],shade[7:0],8'd18};
                            if(row >= 370 && row <= 390 && x >= center+20 && x <= center+40)begin pixel=24'hc8c8c8; end
                        end
                        if(((row>=180 && row<184) || (row>=204 && row<208) ||
                            (row>=228 && row<232) || (row>=252 && row<256)) &&
                            ((x>=552 && x<556) || (x>=680 && x<684)))pixel=24'hff2020;
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
        capture_file=$fopen("sim/hdmi_count_recovery_frame.hex","w");
        if(capture_file == 0)begin $fatal(1,"capture open failed"); end
        repeat(5)@(negedge clk); rstn=1;
        repeat(12)@(negedge clk);keys[0]=0;repeat(12)@(negedge clk);keys[0]=1;repeat(12)@(negedge clk);
        send_frame(-1000);send_frame(-1000);send_frame(-1000);
        if(!mode || gate_state!=1)$fatal(1,"sparse-noise gate did not become ready");
        send_frame(580);send_frame(580);
        if(gate_state!=2)$fatal(1,"gate not armed");
        send_frame(700);send_frame(700);
        if(frames != 7 || red != 0 || green != 0 || yellow != 1 || total != 1 || gate_state != 3 ||
           dut.reg_display_yellow_bcd != 40'h1 || dut.reg_display_x_bcd != 16'h0699 ||
           dut.reg_display_diag_count != 1 || dut.reg_display_diag_reject != 0)begin
            $fatal(1,"720P tracker/snapshot mismatch");
        end
        $fclose(capture_file);
        $display("PASS COUNT HDMI:7 full 1280x720 frames,1209600 DDR words, sparse-noise ready, yellow crossing=1 and actual frozen OSD capture");
        $finish;
    end
    initial begin #100000000; $fatal(1,"720P timeout"); end
endmodule
