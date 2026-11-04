`timescale 1ns / 1ps
module tb_ball_calibration;
    reg clk=0;always #5 clk=!clk;
    reg rstn=0,valid=0,early=0;
    reg [95:0] rgb=0;
    wire [19:0] gain_red,gain_blue;
    wire ready;
    ball_white_balance dut(.i_clk(clk),.i_rstn(rstn),.i_rgb(rgb),.i_valid(valid),.i_early(early),
        .o_gain_red(gain_red),.o_gain_blue(gain_blue),.o_ready(ready));
    reg [19:0] old_red=65536,old_blue=65536;
    reg allowed_update;
    always @(posedge clk)begin
        allowed_update=dut.reg_early_third;
        #1;
        if(rstn && !allowed_update && (gain_red != old_red || gain_blue != old_blue))$fatal(1,"WB changed inside frame");
        old_red=gain_red;old_blue=gain_blue;
    end
    task reset_wb;
        begin @(negedge clk);rstn=0;valid=0;early=0;repeat(4)@(negedge clk);rstn=1;end
    endtask
    task boundary;
        begin @(negedge clk);early=1;valid=0;@(negedge clk);early=0;repeat(4)@(negedge clk);end
    endtask
    integer file_id,red,green,blue,expected_red,expected_blue,scanned,index,vectors=0;
    reg [23:0] pixel;
    reg [1:0] camera_step=0;
    reg cam_done=0,ae_done=0;
    wire request;
    wire [15:0] exposure,gain;
    integer requests=0;
    ae_set control(.I_clk(clk),.I_rst(!rstn),.I_step(camera_step),
        .I_cam_cfg_done(cam_done),.I_ae_cfg_done(ae_done),.O_ae_req(request),.O_ae(exposure),.O_ag(gain));
    always @(posedge clk)begin if(request)requests=requests+1;end
    task press;
        input integer key;
        begin @(negedge clk);camera_step[key-2]=!camera_step[key-2];repeat(20)@(negedge clk);end
    endtask
    initial begin
        file_id=$fopen("sim/wb_vectors.txt","r");if(file_id==0)$fatal(1,"WB vectors missing");
        while(!$feof(file_id))begin
            scanned=$fscanf(file_id,"%d %d %d %d %d\n",red,green,blue,expected_red,expected_blue);
            if(scanned==5)begin
                reset_wb();boundary();pixel={red[7:0],green[7:0],blue[7:0]};
                for(index=0;index<16;index=index+1)begin rgb={4{pixel}};valid=1;@(negedge clk);end
                valid=0;repeat(5)@(negedge clk);
                if(dut.cnt_samples!=64)$fatal(1,"WB did not sample all four lanes");
                boundary();repeat(100)@(negedge clk);
                if(dut.reg_target_red!=expected_red || dut.reg_target_blue!=expected_blue)$fatal(1,"WB exact division mismatch");
                if(gain_red!=65536 || gain_blue!=65536)$fatal(1,"WB target applied before frame boundary");
                boundary();
                if(gain_red != (expected_red>=65536 ? 65536+(expected_red-65536)/4 : 65536-(65536-expected_red)/4) ||
                   gain_blue != (expected_blue>=65536 ? 65536+(expected_blue-65536)/4 : 65536-(65536-expected_blue)/4) || !ready)
                    $fatal(1,"WB smoothing/commit mismatch");
                vectors=vectors+1;
            end
        end
        $fclose(file_id);
        reset_wb();boundary();
        rgb={24'hc81414,24'h3c7882,24'hffffff,24'h000000};valid=1;repeat(100)@(negedge clk);valid=0;repeat(5)@(negedge clk);
        if(dut.cnt_samples!=0)$fatal(1,"colored/dark/saturated pixels entered WB");
        boundary();repeat(120)@(negedge clk);boundary();
        if(gain_red!=65536 || gain_blue!=65536 || ready)$fatal(1,"no-neutral frame fabricated gains");
        // 少于64个中性样本不能更新；valid空拍不能累加。
        rgb={24'h646464,24'hc81414,24'hc81414,24'hc81414};valid=1;repeat(63)@(negedge clk);valid=0;
        repeat(10)@(negedge clk);if(dut.cnt_samples!=63)$fatal(1,"WB sample threshold/gaps");
        boundary();repeat(110)@(negedge clk);if(ready)$fatal(1,"too few WB samples accepted");
        reset_wb();cam_done=1;ae_done=1;repeat(5)@(negedge clk);
        if(exposure!=1991 || gain!=144 || requests<1)$fatal(1,"initial AE request missing");
        ae_done=0;
        press(2);press(2);press(2);
        if(exposure!=1991)$fatal(1,"AE values changed during I2C batch");
        ae_done=1;repeat(5)@(negedge clk);
        if(exposure!=120)$fatal(1,"queued latest exposure lost");
        press(2);if(exposure!=1991)$fatal(1,"exposure profile wrap");
        press(2);if(exposure!=480)$fatal(1,"4ms profile");
        press(2);if(exposure!=240)$fatal(1,"2ms profile");
        press(3);if(gain!=176)$fatal(1,"gain32 profile");
        press(3);if(gain!=80)$fatal(1,"gain4 profile");
        press(3);if(gain!=112)$fatal(1,"gain8 profile");
        press(3);if(gain!=144)$fatal(1,"gain16 profile wrap");
        press(2);repeat(100)@(negedge clk);
        if(exposure!=120)$fatal(1,"long press repeated exposure selection");
        $display("PASS calibration: %0d integer WB vectors, frame freeze, neutral selection, sample threshold, AE queued/toggle profiles",vectors);
        $finish;
    end
    initial begin #10000000;$fatal(1,"calibration timeout");end
endmodule
