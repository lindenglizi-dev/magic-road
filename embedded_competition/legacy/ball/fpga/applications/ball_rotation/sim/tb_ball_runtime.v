`timescale 1ns / 1ps
module tb_ball_runtime;
    reg [47:0] camera_status=0,previous_camera_status=0;
    always @(negedge clk)begin if(rstn)camera_status=camera_status+1'b1;end
    always @(posedge clk)begin
        #1;
        if(rstn && user && dut.reg_camera_status!==camera_status)$fatal(1,"camera snapshot not captured at boundary");
        if(rstn && !user && dut.reg_camera_status!==previous_camera_status)$fatal(1,"camera snapshot changed inside frame");
        previous_camera_status=dut.reg_camera_status;
    end
    reg clk=0;
    always #5 clk=!clk;
    reg rstn=0,valid=0,user=0;
    reg [3:0] keys=15;
    reg [95:0] rgb=0;
    wire [127:0] data;
    wire out_valid,last,done,early,error,mode;
    wire [31:0] red,green,yellow;
    wire [33:0] total;
    wire [2:0] gate_state;
    wire [1:0] track_state;
    ball_runtime #(.C_FACE_GATE(0),.C_WIDTH(160),.C_HEIGHT(192),.C_X_MIN(0),.C_Y_MIN(112),.C_X_END(160),.C_Y_END(192),
        .C_GATE_MIN(56),.C_GATE_END(104),.C_LINE(80),.C_HYST(4),.C_MIN_AREA(16),.C_MIN_SIZE(3),.C_MAX_SIZE(64),
        .C_MAX_MOVE(12),.C_DEBOUNCE(3)) dut(
        .I_clk(clk),.I_rst_n(rstn),.I_camera_status(camera_status),.I_keys_n(keys),.I_rgb(rgb),.I_valid(valid),.I_user(user),.I_last(1'b0),
        .O_data(data),.O_valid(out_valid),.O_last(last),.O_done(done),.O_early(early),.O_error(error),
        .O_red(red),.O_green(green),.O_yellow(yellow),.O_total(total),.O_count_mode(mode),.O_gate_state(gate_state),.O_track_status(track_state));
    integer words=0,lines=0,frames=0,starts=0;
    reg [255:0] queue=0;
    reg [127:0] expected;
    integer nbytes=0;
    reg expected_early;
    always @(posedge clk)begin
        expected_early=user;
        if(dut.osd_valid)begin
            queue=(queue<<96)|dut.osd_rgb; nbytes=nbytes+12;
            if(dut.osd_sof)begin starts=starts+1; end
        end
        #1;
        if(rstn && early !== expected_early)begin $fatal(1,"early latency changed"); end
        if(out_valid)begin
            expected=queue >> ((nbytes-16)*8);
            if(nbytes < 16 || data !== expected)begin $fatal(1,"runtime DDR byte order"); end
            nbytes=nbytes-16; queue=queue & ((256'b1 << (nbytes*8))-1);
            words=words+1;
            if(last)begin lines=lines+1; end
            if(done)begin frames=frames+1; end
        end
    end
    task tap_key;
        input integer index;
        begin
            @(negedge clk); keys[index]=0;
            repeat(12)@(negedge clk);
            keys[index]=1;
            repeat(12)@(negedge clk);
        end
    endtask
    task send_frame;
        input integer center,color,post_clocks;
        integer y,xgroup,lane,x,w0,l0,f0,s0;
        reg [23:0] pixel;
        begin
            w0=words; l0=lines; f0=frames; s0=starts;
            @(negedge clk); user=1;
            @(negedge clk); user=0;
            repeat(8)@(negedge clk);
            for(y=0;y<192;y=y+1)begin
                for(xgroup=0;xgroup<40;xgroup=xgroup+1)begin
                    for(lane=0;lane<4;lane=lane+1)begin
                        x=xgroup*4+lane; pixel=24'h181818;
                        if(color != 0 && y >= 140 && y <= 156 && x >= center-8 && x <= center+8)begin
                            case(color)
                                1:pixel=24'hff2020;
                                2:pixel=24'hffff00;
                                3:pixel=24'h00ff40;
                                default:pixel=24'h181818;
                            endcase
                        end
                        rgb[95-lane*24 -:24]=pixel;
                    end
                    valid=1; @(negedge clk);
                    if(xgroup == 13)begin valid=0; repeat(2)@(negedge clk); end
                end
                valid=0; repeat(3)@(negedge clk);
            end
            repeat(20)@(negedge clk);
            if(words-w0 != 5760 || lines-l0 != 192 || frames-f0 != 1 || starts-s0 != 1 || nbytes != 0)begin
                $fatal(1,"runtime stream counts");
            end
            repeat(post_clocks)@(negedge clk);
            if(error)begin $fatal(1,"runtime error flag"); end
        end
    endtask
    integer hold_frame;
    reg [79:0] previous_diagnostics=0;
    reg expected_clear;
    always @(posedge clk)begin
        expected_clear=dut.clear_history;
        #1;
        if(rstn && !user && !expected_clear &&
           {dut.reg_display_diag_count,dut.reg_display_diag_reject,dut.reg_display_diag_width_bcd,
            dut.reg_display_diag_height_bcd,dut.reg_display_diag_area_bcd,dut.reg_display_diag_fill_bcd} !== previous_diagnostics)
            $fatal(1,"diagnostics changed away from a boundary/explicit clear");
        previous_diagnostics={dut.reg_display_diag_count,dut.reg_display_diag_reject,dut.reg_display_diag_width_bcd,
            dut.reg_display_diag_height_bcd,dut.reg_display_diag_area_bcd,dut.reg_display_diag_fill_bcd};
    end
    initial begin
        repeat(5)@(negedge clk); rstn=1;
        send_frame(35,1,6000); send_frame(39,1,6000); send_frame(39,1,6000);
        // x31是孤立组边缘，支持规则将左边界收至32，中心仍为39。
        if(mode || track_state != 2 || dut.reg_display_valid != 1 || dut.reg_display_left[11:0] != 32)begin
            $fatal(1,"tracking display snapshot");
        end
        if(dut.reg_display_diag_count !== 1 || dut.reg_display_diag_width_bcd !== 16'h0016 ||
           dut.reg_display_diag_height_bcd !== 16'h0020 || dut.reg_display_diag_area_bcd !== 28'h0000272 ||
           dut.reg_display_diag_fill_bcd !== 12'h085 || dut.reg_display_diag_reject !== 0)begin
            $fatal(1,"component diagnostic snapshot");
        end
        // 旧帧仍在RAM扫描时提交模式请求，不能推进新配置的空门确认。
        send_frame(39,1,0);
        tap_key(0);
        if(mode)begin $fatal(1,"mode changed before frame boundary"); end
        send_frame(0,0,6000);
        if(!mode || dut.epoch != 1 || gate_state != 0 || dut.counter_Inst.cnt_empty != 1)begin
            $fatal(1,"old epoch consumed after mode commit");
        end
        send_frame(0,0,6000); send_frame(0,0,6000);
        if(gate_state != 1)begin $fatal(1,"count gate readiness"); end
        send_frame(65,1,6000); send_frame(65,1,6000); send_frame(87,1,6000); send_frame(87,1,6000);
        if(red != 1 || total != 1 || dut.reg_display_red_bcd != 40'h1)begin $fatal(1,"counter OSD snapshot"); end
        for(hold_frame=0;hold_frame<5;hold_frame=hold_frame+1)begin send_frame(87,1,6000); end
        send_frame(0,0,6000); send_frame(0,0,6000); send_frame(87,1,6000);
        if(red != 1 || gate_state != 3)begin $fatal(1,"runtime duplicate after dropout"); end
        send_frame(0,0,6000); send_frame(0,0,6000); send_frame(0,0,6000);
        send_frame(65,1,6000); send_frame(65,1,6000);
        send_frame(87,1,0);
        // 在旧数值转换进行时清零，旧BCD完成不能重新发布清零前的2。
        wait(dut.flag_format_load);
        tap_key(3);
        send_frame(87,1,6000);
        if(red != 0 || total != 0 || gate_state != 0 || dut.reg_display_red_bcd != 0)begin
            $fatal(1,"clear during formatter resurrected old count");
        end
        send_frame(87,1,6000);
        if(dut.reg_display_red_bcd != 0)begin $fatal(1,"late old BCD accepted"); end
        tap_key(2); send_frame(0,0,6000);
        if(!dut.strict || dut.epoch != 3)begin $fatal(1,"strict commit"); end
        $display("PASS ball runtime: %0d frames, key commits, epoch rejection, format clear, frozen OSD and packed bytes",frames);
        $finish;
    end
    initial begin #100000000; $fatal(1,"runtime timeout"); end
endmodule
