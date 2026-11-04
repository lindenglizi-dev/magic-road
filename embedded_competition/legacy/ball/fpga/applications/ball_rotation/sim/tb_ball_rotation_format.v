`timescale 1ns / 1ps
// 仅注入旋转测量结果，检查显示换算和跨帧整包提交。
module tb_ball_rotation_format;
    reg clk=0;
    always #5 clk=!clk;
    reg rstn=0,user=0,sample_done=0,clear=0,count_mode=0,enabled=1;
    reg [15:0] epoch=1,sample_epoch=1,phase=0;
    reg [47:0] net=0;
    reg [23:0] rpm=0;
    reg [31:0] cw=0,ccw=0;
    reg [2:0] status=0;
    reg [3:0] reason=0,flags=0;
    wire angle_valid=flags[3],rpm_valid=flags[2],partial=flags[1],saturated=flags[0];
    ball_runtime #(.C_FACE_GATE(0),.C_ROTATION_ENABLE(1),.C_WIDTH(32),.C_HEIGHT(16),
        .C_X_MIN(0),.C_Y_MIN(0),.C_X_END(32),.C_Y_END(16),.C_DEBOUNCE(3)) dut(
        .I_clk(clk),.I_rst_n(rstn),.I_keys_n(4'hf),.I_camera_status(48'd0),
        .I_rgb(96'd0),.I_valid(1'b0),.I_user(user),.I_last(1'b0),
        .O_data(),.O_valid(),.O_last(),.O_done(),.O_early(),.O_error(),
        .O_red(),.O_green(),.O_yellow(),.O_total(),.O_count_mode(),
        .O_gate_state(),.O_track_status(),.O_camera_step());
    wire [158:0] display_packet={dut.reg_rotation_display_rpm_bcd,dut.reg_rotation_display_angle_bcd,
        dut.reg_rotation_display_net_bcd,dut.reg_rotation_display_cw_bcd,dut.reg_rotation_display_ccw_bcd,
        dut.reg_rotation_display_status,dut.reg_rotation_display_reason,dut.flag_rotation_display_angle,
        dut.flag_rotation_display_rpm,dut.flag_rotation_display_partial,dut.flag_rotation_display_negative};
    wire [158:0] pending_packet={dut.reg_rotation_pending_rpm_bcd,dut.reg_rotation_pending_angle_bcd,
        dut.reg_rotation_pending_net_bcd,dut.reg_rotation_pending_cw_bcd,dut.reg_rotation_pending_ccw_bcd,
        dut.reg_rotation_pending_status,dut.reg_rotation_pending_reason,dut.flag_rotation_pending_angle,
        dut.flag_rotation_pending_rpm,dut.flag_rotation_pending_partial,dut.flag_rotation_pending_negative};
    reg [158:0] previous_display=0,expected=0,old_packet=0;
    reg allow_change;
    integer vectors=0,checks=0,fd,nread,collision,kind,stage,index,timeout;

    function [39:0] decimal;
        input [31:0] binary;
        reg [31:0] rest;
        integer digit;
        begin
            rest=binary;
            for(digit=0;digit<10;digit=digit+1)begin
                decimal[digit*4 +: 4]=rest%10;
                rest=rest/10;
            end
        end
    endfunction
    // 参考保持原48位绝对值、64位乘100、Q16截断和饱和顺序。
    function [158:0] reference_packet;
        input [47:0] signed_net;
        input [23:0] signed_rpm;
        input [15:0] input_phase;
        input [31:0] input_cw,input_ccw;
        input [2:0] input_status;
        input [3:0] input_reason,input_flags;
        reg [47:0] magnitude;
        reg [63:0] scaled;
        reg [31:0] angle;
        reg [23:0] rpm_magnitude;
        reg [39:0] rpm_digits,angle_digits,net_digits;
        reg [3:0] result_reason;
        begin
            magnitude=signed_net[47] ? -signed_net : signed_net;
            scaled=({16'd0,magnitude}*64'd100)>>16;
            result_reason=input_flags[0] ? 4'd15 : (scaled>99999 ? 4'd14 : input_reason);
            if(scaled>99999)scaled=99999;
            rpm_magnitude=signed_rpm[23] ? -signed_rpm : signed_rpm;
            angle=({16'd0,input_phase}*32'd3600)>>16;
            rpm_digits=decimal({8'd0,rpm_magnitude});
            angle_digits=decimal(angle);
            net_digits=decimal(scaled[31:0]);
            reference_packet={rpm_digits[31:0],angle_digits[15:0],net_digits[19:0],decimal(input_cw),decimal(input_ccw),
                input_status,result_reason,input_flags[3],input_flags[2],(input_flags[1]||input_flags[0]),signed_net[47]};
        end
    endfunction
    task step;
        begin @(posedge clk);#1;end
    endtask
    task capture;
        begin sample_done=1;step;sample_done=0;end
    endtask
    task clean;
        begin clear=1;step;clear=0;step;end
    endtask
    task set_sample;
        input integer identity;
        begin
            net=identity*65536+153;rpm=-identity*13;phase=identity*1500;
            cw=32'h10203000+identity;ccw=32'h40506000+identity;
            status=identity%8;reason=identity%16;flags=identity%16;sample_epoch=epoch;
        end
    endtask
    task remember_expected;
        begin expected=reference_packet(net,rpm,phase,cw,ccw,status,reason,flags);end
    endtask
    task finish_latest;
        input publish;
        begin
            timeout=0;
            while(!dut.flag_rotation_pending && timeout<50)begin step;timeout=timeout+1;end
            if(!dut.flag_rotation_pending)$fatal(1,"latest result did not finish");
            if(pending_packet!==expected)$fatal(1,"mixed/stale pending packet got=%h expected=%h",pending_packet,expected);
            if(publish)begin
                user=1;step;user=0;
                if(display_packet!==expected)$fatal(1,"frame commit mismatch");
            end
            checks=checks+1;
        end
    endtask
    always @(posedge clk)begin
        allow_change=user || clear || !enabled || count_mode;
        #2;
        if(rstn && !allow_change && display_packet!==previous_display)$fatal(1,"display changed inside frame");
        previous_display=display_packet;
    end
    initial begin
        force dut.rotation_done=sample_done;
        force dut.rotation_epoch=sample_epoch;
        force dut.rotation_phase=phase;
        force dut.rotation_net=net;
        force dut.rotation_rpm=rpm;
        force dut.rotation_cw=cw;
        force dut.rotation_ccw=ccw;
        force dut.rotation_status=status;
        force dut.rotation_reason=reason;
        force dut.rotation_angle_valid=angle_valid;
        force dut.rotation_rpm_valid=rpm_valid;
        force dut.rotation_partial=partial;
        force dut.rotation_saturated=saturated;
        force dut.rotation_fault=1'b0;
        force dut.clear_history=clear;
        force dut.ball_enabled=enabled;
        force dut.mode=count_mode;
        force dut.active_epoch=epoch;
        repeat(3)step;rstn=1;step;
        fd=$fopen("reports/optimized_build/format_vectors.txt","r");
        if(!fd)$fatal(1,"missing numeric vectors");
        while(!$feof(fd))begin
            nread=$fscanf(fd,"%h %h %h %h %h %h %h %h\n",net,rpm,phase,cw,ccw,status,reason,flags);
            if(nread!=8)$fatal(1,"invalid numeric vector");
            sample_epoch=epoch;remember_expected;capture;finish_latest(1);vectors=vectors+1;
        end
        $fclose(fd);
        // 新结果分别在旧done之前0/1/2拍到达，撞捕获/缩位/加载边界。
        for(collision=0;collision<3;collision=collision+1)begin
            clean;set_sample(3);capture;step;step;
            timeout=0;
            if(collision==0)begin
                while(!dut.rotation_format_done && timeout<40)begin step;timeout=timeout+1;end
            end else begin
                while((dut.rotation_cw_decimal_Inst.cnt_bits!=collision || !dut.rotation_cw_decimal_Inst.o_busy) && timeout<40)
                    begin step;timeout=timeout+1;end
            end
            if(timeout>=40)$fatal(1,"failed to align formatter collision");
            set_sample(9+collision);remember_expected;capture;
            if(dut.flag_rotation_pending)$fatal(1,"old formatter retired at capture");
            finish_latest(1);
        end
        // 连续结果覆盖尚未加载的缩位数据；仅最后一组数值和元数据退役。
        clean;set_sample(1);capture;set_sample(2);capture;set_sample(13);remember_expected;capture;finish_latest(1);
        // 清空、计数模式、epoch提交、禁用在各在途边界撤销结果。
        for(kind=0;kind<4;kind=kind+1)begin
            for(stage=0;stage<4;stage=stage+1)begin
                clean;set_sample(5);capture;
                if(stage<3)begin for(index=0;index<stage;index=index+1)step;end
                else begin
                    timeout=0;
                    while(!dut.rotation_format_done && timeout<45)begin step;timeout=timeout+1;end
                    if(timeout>=45)$fatal(1,"cancel boundary alignment failed");
                end
                old_packet=display_packet;
                case(kind)
                    0:clear=1;
                    1:count_mode=1;
                    2:epoch=epoch+1'b1;
                    3:enabled=0;
                endcase
                step;clear=0;count_mode=0;enabled=1;
                if(kind!=2)old_packet=0;
                repeat(40)step;
                user=1;step;user=0;
                if(dut.flag_rotation_pending || display_packet!==old_packet)$fatal(1,"cancelled result escaped kind=%0d stage=%0d",kind,stage);
                set_sample(15);remember_expected;capture;finish_latest(1);
            end
        end
        clean;set_sample(4);sample_epoch=epoch-1'b1;capture;repeat(40)step;
        if(dut.flag_rotation_pending || dut.flag_rotation_scale)$fatal(1,"stale epoch accepted");
        // 帧边界与新结果同拍：允许旧完整包提交，不能拼接新元数据。
        clean;set_sample(7);remember_expected;capture;finish_latest(0);old_packet=expected;
        set_sample(14);remember_expected;user=1;capture;user=0;
        if(display_packet!==old_packet)$fatal(1,"old ready packet lost atomicity at new result");
        finish_latest(1);
        $display("PASS ROTATION FORMAT: %0d numeric vectors, %0d packets; latest-wins, capture/scale/load done races, clear/mode/epoch/disable cancellation and atomic frame commit",vectors,checks);
        $finish;
    end
    initial begin #5000000;$fatal(1,"format test timeout");end
endmodule
