`timescale 1ns/1ps
// Changing raw RGB proves both registers independently of outline geometry.
module tb_road_box_video_delay;
    reg clk=0,rstn=0,sof=0,de=0,vs=0,hs=0,draw=1;
    reg [23:0] raw=0,raw_previous=0,raw_expected=0;
    reg [2:0] sync_previous=0,sync_expected=0;
    wire ovs,ohs,ode,ready,busy,fault;
    wire [23:0] rgb;
    wire [8:0] cycles;
    wire [5:0] index;
    integer step,checked=0;
    road_box_age_overlay dut(
        .i_clk(clk),.i_rstn(rstn),.i_sof(sof),.i_vsync(vs),.i_hsync(hs),.i_de(de),.i_rgb(raw),
        .i_table_active_valid(1'b1),.i_table_count(7'd0),.i_table_entry(97'd0),.i_table_draw_valid(draw),
        .i_age_upper_ms(64'd2000),.o_table_read_index(index),.o_vsync(ovs),.o_hsync(ohs),.o_de(ode),
        .o_rgb(rgb),.o_line_ready(ready),.o_prepare_busy(busy),.o_last_prepare_cycles(cycles),.o_fault(fault));
    always #6.666 clk=~clk;
    always @(posedge clk) begin
        if(!rstn) begin raw_previous=0;raw_expected=0;sync_previous=0;sync_expected=0;end
        else begin
            raw_expected=raw_previous;raw_previous=raw;
            sync_expected=sync_previous;sync_previous={vs,hs,de};
            #0.001;
            if(rgb!==raw_expected || {ovs,ohs,ode}!==sync_expected)
                $fatal(1,"VIDEO_NOT_TWO_REGISTERS raw=%h expected=%h rgb=%h",raw,raw_expected,rgb);
            checked=checked+1;
        end
    end
    initial begin
        repeat(4) @(negedge clk);rstn=1;sof=1;
        @(negedge clk);sof=0;
        repeat(1400) @(negedge clk);
        for(step=0;step<1650;step=step+1) begin
            raw=(step*24'h010307)^24'hac59e2;
            de=(step<1280);vs=(step>=1390);hs=(step>=1400 && step<1440);
            draw=(step<641);
            @(negedge clk);
        end
        repeat(4) @(negedge clk);
        if(fault) $fatal(1,"DELAY_TEST_FAULT");
        $display("TB_PASS_BOX_VIDEO_DELAY changing_raw_rgb fixed_two_registers sync_exact live_gate_raw_alignment checked=%0d",checked);
        $finish;
    end
endmodule
