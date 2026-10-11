`timescale 1ns / 1ps

// Directed proof that the compact two-group tail keeps depthwise tap eight.
module tb_dw_tail_compact;
    reg clk = 0;
    reg rstn = 0;
    reg table_valid = 0;
    reg [9:0] table_addr = 0;
    reg signed [15:0] table_data = 0;
    reg load_valid = 0;
    reg [2:0] load_kind = 0;
    reg [10:0] load_addr = 0;
    reg signed [31:0] load_data = 0;
    reg start = 0;
    wire table_ready;
    wire table_loaded;
    wire load_ready;
    wire busy;
    wire done;
    wire fault;
    integer index;
    integer cycles = 0;
    integer target_groups = 0;
    reg target_acc_seen = 0;

    always #5 clk = ~clk;

    down2_dynamic_tile_runner dut(
        .i_clk(clk), .i_rstn(rstn),
        .i_table_valid(table_valid), .i_table_addr(table_addr),
        .i_table_data(table_data), .o_table_ready(table_ready),
        .o_table_loaded(table_loaded), .o_table_fault(),
        .i_load_valid(load_valid), .i_load_kind(load_kind),
        .i_load_addr(load_addr), .i_load_data(load_data),
        .o_load_ready(load_ready), .i_start(start), .i_pw_only(1'b0),
        .i_commit_ready(1'b1), .o_busy(busy), .o_done(done), .o_fault(fault),
        .i_export_start(1'b0), .i_output_ready(1'b1),
        .o_output_valid(), .o_output_data(), .o_output_index(), .o_export_done(),
        .o_debug_valid(), .o_debug_phase(), .o_debug_layer(),
        .o_debug_position(), .o_debug_channel(), .o_debug_value(),
        .o_preload_writes(), .o_core_cycles(), .o_mac_cycles(),
        .o_pre_cycles(), .o_silu_cycles(), .o_post_cycles(),
        .o_writeback_cycles(), .o_storage_wait_cycles(),
        .o_scheduler_idle_cycles(), .o_export_cycles(),
        .o_result_queue_count(), .o_result_reserved(), .o_meta_count(),
        .o_mac_result_count(), .o_pre_accept_count(), .o_silu_accept_count(),
        .o_post_accept_count(), .o_writeback_count()
    );

    task load_one;
        input [2:0] kind;
        input integer address;
        input signed [31:0] value;
        begin
            @(negedge clk);
            load_valid = 1;
            load_kind = kind;
            load_addr = address;
            load_data = value;
            if (!load_ready) $fatal(1, "preload blocked kind=%0d addr=%0d", kind, address);
        end
    endtask

    always @(posedge clk) begin
        cycles = cycles + 1;
        if (cycles > 20000) $fatal(1, "tail counterexample timeout");
        if (rstn && fault) $fatal(1, "unexpected runner fault");
        if (rstn && dut.flag_mac_input_accept && !dut.flag_layer_pw &&
            dut.cnt_position == 4'd3 && dut.cnt_output == 5'd0) begin
            if (target_groups == 0) begin
                if (dut.cnt_mac_group !== 2'd0 || dut.reg_mac_mask !== 8'hff)
                    $fatal(1, "tail G0 mapping mismatch group=%0d mask=%h",
                           dut.cnt_mac_group, dut.reg_mac_mask);
            end else if (target_groups == 1) begin
                if (dut.cnt_mac_group !== 2'd1 || dut.reg_mac_mask !== 8'h01)
                    $fatal(1, "tail G1 mapping mismatch group=%0d mask=%h",
                           dut.cnt_mac_group, dut.reg_mac_mask);
                if ($signed(dut.reg_mac_activation[7:0]) !== 8'sd1 ||
                    $signed(dut.reg_mac_weight[7:0]) !== 8'sd1)
                    $fatal(1, "tail tap eight was not mapped to lane zero");
            end else begin
                $fatal(1, "tail task issued more than two MAC groups");
            end
            target_groups = target_groups + 1;
        end
        if (rstn && dut.flag_pp_input_accept && !dut.flag_layer_pw &&
            dut.wire_pp_position == 4'd3 && dut.wire_result_channel_base == 5'd0) begin
            if (target_groups != 2)
                $fatal(1, "tail accumulator arrived before exactly two groups");
            if ($signed(dut.wire_pp_result_data[31:0]) !== 32'sd1)
                $fatal(1, "last-tap accumulator mismatch got=%0d expected=1",
                       $signed(dut.wire_pp_result_data[31:0]));
            target_acc_seen = 1;
        end
    end

    initial begin
        repeat (3) @(negedge clk);
        rstn = 1;

        for (index = 0; index < 1024; index = index + 1) begin
            @(negedge clk);
            table_valid = 1;
            table_addr = index;
            table_data = 0;
            if (!table_ready) $fatal(1, "table load blocked addr=%0d", index);
        end
        @(negedge clk);
        table_valid = 0;
        if (!table_loaded) $fatal(1, "table did not publish after 1024 writes");

        for (index = 0; index < 1296; index = index + 1)
            load_one(3'd0, index, index == 416 ? 32'sd1 : 32'sd0);
        for (index = 0; index < 144; index = index + 1)
            load_one(3'd2, index, index == 8 ? 32'sd1 : 32'sd0);
        for (index = 0; index < 16; index = index + 1)
            load_one(3'd3, index, 32'sd0);
        for (index = 0; index < 384; index = index + 1)
            load_one(3'd4, index, 32'sd0);
        for (index = 0; index < 24; index = index + 1)
            load_one(3'd5, index, 32'sd0);
        @(negedge clk);
        load_valid = 0;

        @(negedge clk);
        start = 1;
        @(negedge clk);
        start = 0;
        wait (target_acc_seen);
        $display("TB_PASS_DW_TAIL_COMPACT position=3 channel=0 groups=2 g0_mask=ff g1_mask=01 halo416=1 weight8=1 acc=1");
        $finish;
    end
endmodule
