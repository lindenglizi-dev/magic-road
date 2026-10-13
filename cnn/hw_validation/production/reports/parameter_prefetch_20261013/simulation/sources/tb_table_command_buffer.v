`timescale 1ns / 1ps

// Shared-wrapper table command buffer protocol checks; arithmetic is not exercised here.
module tb_table_command_buffer();
    reg clk = 1'b0;
    always #5 clk = ~clk;

    reg rstn = 1'b0;
    reg select_valid = 1'b0;
    reg select_down2 = 1'b0;
    reg table_valid = 1'b0;
    reg [9:0] table_addr = 10'd0;
    reg signed [15:0] table_data = 16'sd0;
    reg load_valid = 1'b0;
    reg [2:0] load_kind = 3'd0;
    reg [10:0] load_addr = 11'd0;
    reg signed [31:0] load_data = 32'sd0;
    reg start = 1'b0;
    reg commit_ready = 1'b1;
    reg export_start = 1'b0;
    reg output_ready = 1'b1;
    wire select_ready, selected_down2, table_ready, table_loaded, table_fault;
    wire load_ready, busy, done, fault, output_valid, export_done;
    wire signed [7:0] output_data;
    wire [8:0] output_index;
    wire [31:0] core_cycles;
    integer i;
    integer pushes = 0;
    integer pops = 0;
    integer inner_writes = 0;
    integer simultaneous = 0;
    integer cycles = 0;

    road_frontend_shared_core dut(
        .i_clk(clk), .i_rstn(rstn), .i_select_valid(select_valid),
        .i_select_down2(select_down2), .o_select_ready(select_ready),
        .o_selected_down2(selected_down2), .i_table_valid(table_valid),
        .i_table_addr(table_addr), .i_table_data(table_data),
        .o_table_ready(table_ready), .o_table_loaded(table_loaded),
        .o_table_fault(table_fault), .i_load_valid(load_valid),
        .i_load_kind(load_kind), .i_load_addr(load_addr), .i_load_data(load_data),
        .o_load_ready(load_ready), .i_start(start), .i_commit_ready(commit_ready),
        .o_busy(busy), .o_done(done), .o_fault(fault),
        .o_core_cycles(core_cycles), .i_export_start(export_start),
        .i_output_ready(output_ready), .o_output_valid(output_valid),
        .o_output_data(output_data), .o_output_index(output_index),
        .o_export_done(export_done)
    );

    always @(posedge clk) begin
        cycles = cycles + 1;
        if (cycles > 12000) $fatal(1, "Table command buffer timeout");
        if (rstn && dut.flag_table_push) pushes = pushes + 1;
        if (rstn && dut.flag_table_pop) pops = pops + 1;
        if (rstn && dut.u_pp.u_silu.flag_table_transfer)
            inner_writes = inner_writes + 1;
        if (rstn && (dut.flag_table_pop !== dut.u_pp.u_silu.flag_table_transfer))
            $fatal(1, "Wrapper pop disagrees with the physical SiLU table transfer");
        if (rstn && dut.flag_table_push && dut.flag_table_pop)
            simultaneous = simultaneous + 1;
    end

    task reset_core;
        begin
            rstn = 1'b0;
            #1;
            if (dut.flag_table_pending || dut.flag_table_push || dut.flag_table_pop ||
                table_loaded || table_fault)
                $fatal(1, "Asynchronous reset did not cancel table state");
            repeat (2) @(negedge clk);
            rstn = 1'b1;
            @(negedge clk);
            if (dut.flag_table_pending || table_loaded || table_fault)
                $fatal(1, "Table state invalid after reset release");
        end
    endtask

    task offer_table;
        input [9:0] address;
        input signed [15:0] data;
        begin
            @(negedge clk);
            table_valid = 1'b1;
            table_addr = address;
            table_data = data;
            #1;
            if (!table_ready) $fatal(1, "Table command rejected address=%0d", address);
            @(posedge clk);
            #1;
        end
    endtask

    task load_remainder_with_bubbles;
        input integer first_address;
        begin
            for (i = first_address; i < 1024; i = i + 1) begin
                if ((i % 17) == 0) begin
                    @(negedge clk);
                    table_valid = 1'b0;
                end
                offer_table(i[9:0], $signed((i * 73 + 19) & 16'hffff));
            end
        end
    endtask

    task load_complete_continuous;
        begin
            for (i = 0; i < 1024; i = i + 1)
                offer_table(i[9:0], $signed((i * 29 + 7) & 16'hffff));
            @(negedge clk);
            table_valid = 1'b0;
            @(posedge clk);
            @(negedge clk);
            if (!table_loaded || dut.flag_table_pending || table_fault)
                $fatal(1, "Continuous reload did not drain all 1024 commands");
        end
    endtask

    initial begin
        repeat (3) @(negedge clk);
        reset_core;

        // The wrapper owns an accepted command immediately, but PP cannot write it that cycle.
        force dut.u_pp.flag_table_enable = 1'b0;
        offer_table(10'd0, -16'sd123);
        if (!dut.flag_table_pending || dut.reg_table_address != 10'd0 ||
            dut.reg_table_data != -16'sd123 || dut.flag_table_pop)
            $fatal(1, "First command was not buffered for a later PP write");
        @(negedge clk);
        table_valid = 1'b0;
        repeat (8) begin
            @(posedge clk);
            #1;
            if (!dut.flag_table_pending || dut.reg_table_address != 10'd0 ||
                dut.reg_table_data != -16'sd123)
                $fatal(1, "Buffered payload changed under PP backpressure");
        end

        // A registered pending command blocks all four wrapper commands.
        @(negedge clk);
        select_valid = 1'b1;
        select_down2 = 1'b1;
        load_valid = 1'b1;
        start = 1'b1;
        export_start = 1'b1;
        #1;
        if (select_ready || load_ready || dut.u_stem.i_start ||
            dut.u_stem.i_load_valid || dut.u_stem.i_export_start)
            $fatal(1, "Pending table command did not block wrapper commands");
        @(negedge clk);
        select_valid = 1'b0;
        load_valid = 1'b0;
        start = 1'b0;
        export_start = 1'b0;

        // Releasing PP permits replacement in the same cycle without changing the held write.
        table_valid = 1'b1;
        table_addr = 10'd1;
        table_data = 16'sd456;
        release dut.u_pp.flag_table_enable;
        #1;
        if (!table_ready || !dut.flag_table_push || !dut.flag_table_pop)
            $fatal(1, "Expected same-cycle table pop and push");
        @(posedge clk);
        #1;
        if (!dut.flag_table_pending || dut.reg_table_address != 10'd1 ||
            dut.reg_table_data != 16'sd456)
            $fatal(1, "Same-cycle replacement lost the new payload");

        load_remainder_with_bubbles(2);

        // The final pending write may drain, but a nonzero successor cannot be accepted.
        @(negedge clk);
        table_valid = 1'b1;
        table_addr = 10'd1;
        table_data = 16'sd99;
        #1;
        if (table_ready || dut.flag_table_push || !dut.flag_table_pop)
            $fatal(1, "Nonzero command accepted beside final table pop");
        @(posedge clk);
        #1;
        if (!table_loaded || dut.flag_table_pending || table_fault)
            $fatal(1, "Final buffered table command did not complete the table");
        @(negedge clk);
        #1;
        if (table_ready || dut.flag_table_push)
            $fatal(1, "Loaded table accepted an illegal nonzero restart");

        // Address zero is the only legal restart; asynchronous reset cancels it immediately.
        force dut.u_pp.flag_table_enable = 1'b0;
        table_addr = 10'd0;
        table_data = 16'sd77;
        #1;
        if (!table_ready) $fatal(1, "Loaded table rejected address-zero restart");
        @(posedge clk);
        #1;
        if (!dut.flag_table_pending || dut.reg_table_address != 10'd0)
            $fatal(1, "Restart command was not buffered");
        rstn = 1'b0;
        #1;
        if (dut.flag_table_pending || table_loaded || table_fault)
            $fatal(1, "Asynchronous reset retained a buffered restart");
        release dut.u_pp.flag_table_enable;
        table_valid = 1'b0;
        repeat (2) @(negedge clk);
        rstn = 1'b1;
        @(negedge clk);

        // The underlying malformed-sequence fault remains observable and reset-only here.
        offer_table(10'd0, 16'sd0);
        @(negedge clk);
        table_valid = 1'b0;
        @(posedge clk);
        offer_table(10'd2, 16'sd2);
        @(negedge clk);
        table_valid = 1'b0;
        @(posedge clk);
        #1;
        if (!table_fault || !fault)
            $fatal(1, "Malformed table sequence did not retain its fault");

        reset_core;
        load_complete_continuous;
        if (pushes < 2051 || pops < 2050 || inner_writes != pops || simultaneous < 1900)
            $fatal(1, "Unexpected handshake coverage push=%0d pop=%0d inner=%0d simultaneous=%0d",
                pushes, pops, inner_writes, simultaneous);
        $display("TB_PASS_TABLE_COMMAND_BUFFER pushes=%0d pops=%0d inner=%0d simultaneous=%0d reset_cancel=1 malformed_fault=1 reload1024=1",
            pushes, pops, inner_writes, simultaneous);
        $finish;
    end
endmodule
