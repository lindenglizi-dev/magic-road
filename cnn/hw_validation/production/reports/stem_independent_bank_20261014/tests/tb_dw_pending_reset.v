`timescale 1ns / 1ps
module tb_dw_pending_reset(output reg o_test_done);
    reg clk=0; always #5 clk=~clk;
    reg rstn=0, valid=0;
    reg signed [31:0]data=32'sd17;
    wire ready;
    road_down2_tile_scheduler dut(.i_clk(clk),.i_rstn(rstn),.i_table_loaded(1'b0),
        .i_load_valid(valid),.i_load_kind(3'd2),.i_load_addr(11'd0),.i_load_data(data),.o_load_ready(ready),
        .i_start(1'b0),.i_pw_only(1'b0),.i_commit_ready(1'b1),.i_export_start(1'b0),.i_output_ready(1'b1),
        .i_mac_ready(1'b0),.i_mac_result_valid(1'b0),.i_mac_result(96'd0),.i_mac_fault(1'b0),
        .i_pp_ready(1'b0),.i_pp_valid(1'b0),.i_pp_data(16'sd0),.i_pp_tag(16'd0),.i_pp_int16(1'b0),.i_pp_fault(1'b0),
        .i_pp_result_queue_count(2'd0),.i_pp_meta_count(4'd0),.i_pp_pre_busy(1'b0),.i_pp_silu_busy(1'b0),
        .i_pp_post_busy(1'b0),.i_pp_pre_accept(1'b0),.i_pp_silu_accept(1'b0),.i_pp_post_accept(1'b0));
    initial begin
        o_test_done=0;
        repeat(2) @(negedge clk);rstn=1;
        @(negedge clk);valid=1;
        @(posedge clk);#1;if(!dut.flag_dw_weight_write_pending) $fatal(1,"First write not queued");
        @(negedge clk);valid=0;
        @(posedge clk);#1;if(dut.reg_dw_weight_top_left[0] !== 8'sd17) $fatal(1,"First write not committed");
        @(negedge clk);valid=1;data=-32'sd99;
        @(posedge clk);#1;if(!dut.flag_dw_weight_write_pending || dut.reg_dw_weight_top_left[0] !== 8'sd17)
            $fatal(1,"Second write queue timing changed");
        #1;rstn=0;#1;
        if(dut.flag_dw_weight_write_pending || dut.flag_dw_weight_loaded) $fatal(1,"Reset did not cancel queued write");
        @(negedge clk);valid=0;
        @(posedge clk);#1;if(dut.reg_dw_weight_top_left[0] !== 8'sd17) $fatal(1,"Cancelled write changed RAM");
        @(negedge clk);rstn=1;
        repeat(2)begin @(posedge clk);#1;if(dut.reg_dw_weight_top_left[0] !== 8'sd17) $fatal(1,"Old write leaked after reset");end
        o_test_done=1;$display("TB_PASS_DW_PENDING_RESET cancelled_old_write=1");$finish;
    end
    initial begin #10000;$fatal(1,"Pending reset timeout");end
endmodule
