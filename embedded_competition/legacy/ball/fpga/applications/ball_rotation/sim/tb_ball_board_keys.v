`timescale 1ns / 1ps
// 两个无关时钟验证板载按键到相机档位的完整控制路径。
module tb_ball_board_keys;
    reg video_clk=0,reference_clk=0;
    always #5 video_clk=!video_clk;
    always #7 reference_clk=!reference_clk;
    reg rstn=0,early=0;
    reg [3:0] keys=15;
    wire mode,mask,strict,clear_history,clear_counts;
    wire [15:0] epoch;
    wire [1:0] camera_step;
    reg configured=0,ae_done=0;
    wire request;
    wire [15:0] exposure,gain;
    integer frame_clock=0,requests=0,clears=0;
    reg previous_request=0;
    ball_key_control #(.C_DEBOUNCE(3),.C_LONG_PRESS(32)) keys_dut(
        .i_clk(video_clk),.i_rstn(rstn),.i_keys_n(keys),.i_session_restart(1'b0),.i_early(early),
        .o_count_mode(mode),.o_mask(mask),.o_strict(strict),.o_epoch(epoch),
        .o_clear(clear_history),.o_clear_counts(clear_counts),.o_camera_step(camera_step));
    ae_set camera_dut(.I_clk(reference_clk),.I_rst(!rstn),.I_step(camera_step),
        .I_cam_cfg_done(configured),.I_ae_cfg_done(ae_done),
        .O_ae_req(request),.O_ae(exposure),.O_ag(gain));
    always @(negedge video_clk)begin
        frame_clock=frame_clock+1;early=(frame_clock%17)==0;
    end
    always @(posedge video_clk)begin if(rstn && clear_counts)clears=clears+1;end
    always @(posedge reference_clk)begin
        if(rstn)begin
            if(request)requests=requests+1;
            if(request && previous_request)$fatal(1,"AE request was not a single pulse");
            previous_request=request;
        end else previous_request=0;
    end
    task settle;
        begin repeat(50)@(negedge video_clk);end
    endtask
    task press;
        input integer key,clocks;
        begin
            @(negedge video_clk);keys[key]=0;
            repeat(clocks)@(negedge video_clk);
            keys[key]=1;settle();
        end
    endtask
    integer saved_requests;
    reg [15:0] saved_epoch;
    initial begin
        repeat(5)@(negedge video_clk);rstn=1;settle();
        if(requests!=0)$fatal(1,"AE request before sensor configuration");
        configured=1;ae_done=1;settle();
        if(exposure!=1991 || gain!=144 || requests!=1)$fatal(1,"default profile/reset CDC");
        // 不足消抖门限的按下/松开毛刺不能触发任何功能。
        @(negedge video_clk);keys[0]=0;@(negedge video_clk);keys[0]=1;settle();
        if(mode || camera_step!=0 || requests!=1)$fatal(1,"press bounce created an event");
        // 前两键按住时不立即执行短按；松开后只执行一次。
        @(negedge video_clk);keys[0]=0;repeat(15)@(negedge video_clk);
        if(mode || keys_dut.flag_request_mode)$fatal(1,"short action fired on press");
        keys[0]=1;settle();
        if(!mode || epoch!=1 || camera_step!=0)$fatal(1,"mode short release");
        press(1,15);
        if(!mask || epoch!=1 || requests!=1)$fatal(1,"mask short release");
        // 长按跨过多个帧边界，既不能切模式/掩膜，也不能重复切相机档位。
        saved_requests=requests;saved_epoch=epoch;
        @(negedge video_clk);keys[0]=0;repeat(180)@(negedge video_clk);
        if(exposure!=480 || requests!=saved_requests+1 || !mode || epoch!=saved_epoch)$fatal(1,"exposure long hold repeated or changed application");
        keys[0]=1;@(negedge video_clk);keys[0]=0;repeat(80)@(negedge video_clk);
        if(exposure!=480 || requests!=saved_requests+1 || epoch!=saved_epoch)$fatal(1,"release bounce rearmed long action");
        keys[0]=1;settle();
        if(!mode || epoch!=saved_epoch || exposure!=480)$fatal(1,"long release also fired short action");
        press(1,180);
        if(gain!=176 || !mask || epoch!=saved_epoch)$fatal(1,"gain long hold changed mask");
        press(0,45);if(exposure!=240)$fatal(1,"exposure240");
        press(0,45);if(exposure!=120)$fatal(1,"exposure120");
        press(0,45);if(exposure!=1991)$fatal(1,"exposure wrap");
        press(1,45);if(gain!=80)$fatal(1,"gain4");
        press(1,45);if(gain!=112)$fatal(1,"gain8");
        press(1,45);if(gain!=144)$fatal(1,"gain wrap");
        // I2C忙时档位选择仍接收，事务输出保持，完成后只提交最新选择。
        ae_done=0;saved_requests=requests;
        press(0,45);press(0,45);press(1,45);
        if(exposure!=1991 || gain!=144 || requests!=saved_requests)$fatal(1,"AE outputs changed during active I2C batch");
        ae_done=1;settle();
        if(exposure!=240 || gain!=176 || requests!=saved_requests+1)$fatal(1,"queued latest profile was lost");
        // 两键同时长按仍各一次，且恢复后的短按可以继续使用。
        saved_requests=requests;
        @(negedge video_clk);keys[1:0]=0;repeat(80)@(negedge video_clk);keys[1:0]=3;settle();
        if(exposure!=120 || gain!=80 || requests!=saved_requests+1 || !mode || !mask)$fatal(1,"simultaneous long presses");
        press(0,15);press(1,15);
        if(mode || mask || epoch!=2)$fatal(1,"short press did not rearm after long press");
        press(2,80);
        if(!strict || epoch!=3)$fatal(1,"strict key hold repeated");
        press(3,80);
        if(clears!=1 || epoch!=4)$fatal(1,"clear key hold repeated");
        // 复位同时清除事件源和目的域，不得产生幽灵曝光请求。
        @(negedge video_clk);rstn=0;configured=0;ae_done=0;
        repeat(6)@(negedge video_clk);rstn=1;settle();saved_requests=requests;
        if(camera_step!=0 || mode || mask || strict || epoch!=0)$fatal(1,"key reset state");
        configured=1;ae_done=1;settle();
        if(exposure!=1991 || gain!=144 || requests!=saved_requests+1)$fatal(1,"reset fabricated CDC event");
        $display("PASS board keys: bounce, release-only short, one-shot long, frame commits, asynchronous toggle CDC, all profiles, busy queue, simultaneous holds, reset");
        $finish;
    end
    initial begin #2000000;$fatal(1,"board keys timeout");end
endmodule
