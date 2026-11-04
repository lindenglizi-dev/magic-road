`timescale 1ns / 1ps
module tb_ball_camera_monitor;
    reg refclk=0,vidclk=0;
    always #5 refclk=!refclk;
    always #3 vidclk=!vidclk;
    reg rstn=0,frame=0,read_valid=0,read_match=1,bus_error=0;
    reg [15:0] exposure=1991;
    reg [23:0] gain=24'h0f0080;
    wire [47:0] status;
    ball_camera_monitor #(.C_REF_CYCLES(1000)) dut(.i_ref_clk(refclk),.i_video_clk(vidclk),.i_rstn(rstn),
        .i_frame(frame),.i_cfg_done(1'b1),.i_read_valid(read_valid),.i_read_match(read_match),.i_bus_error(bus_error),
        .i_read_exposure(exposure),.i_read_gain(gain),.o_status(status));
    task pulse;
        begin @(negedge vidclk);frame=1;@(negedge vidclk);frame=0;end
    endtask
    task wait_transfer;
        begin repeat(80)@(negedge refclk);end
    endtask
    integer index;
    initial begin
        repeat(5)@(negedge refclk);rstn=1;
        read_valid=1;wait_transfer();
        if(status[27:12]!=16'h1991 || status[35:28]!=8'h16 || status[37:36]!=1)$fatal(1,"readback BCD or CDC wrong");
        for(index=0;index<7;index=index+1)begin pulse();repeat(30)@(negedge refclk);end
        wait(dut.reg_fps!=0);wait_transfer();
        if(status[11:0]!=12'h007)$fatal(1,"FPS did not count actual frame events");
        read_valid=0;wait_transfer();exposure=480;gain=24'h1f0080;read_valid=1;wait_transfer();
        if(status[27:12]!=16'h0480 || status[35:28]!=8'h32 || status[37:36]!=1)$fatal(1,"new readback snapshot wrong");
        read_match=0;wait_transfer();if(status[37:36]!=2)$fatal(1,"readback mismatch hidden");
        bus_error=1;wait_transfer();if(status[37:36]!=3)$fatal(1,"I2C bus error hidden");
        wait(dut.reg_fps==0);wait_transfer();if(status[11:0]!=0)$fatal(1,"stopped input FPS not zero");
        $display("PASS camera monitor: asynchronous clocks, actual FPS7/0, readback BCD, coherent CDC, mismatch/NACK status");$finish;
    end
    initial begin #1000000;$fatal(1,"monitor timeout");end
endmodule
