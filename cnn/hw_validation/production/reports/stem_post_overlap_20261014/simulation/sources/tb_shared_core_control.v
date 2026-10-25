`timescale 1ns / 1ps

// 最小控制验证：运行中统一复位必须取消两个调度器、唯一算术链和共享表状态。
module tb_shared_core_control();
    reg clk = 1'b0;
    always #5 clk = ~clk;
    reg rstn = 1'b0;
    reg table_valid = 1'b0;
    reg load_valid = 1'b0;
    reg start = 1'b0;
    reg commit_ready = 1'b1;
    reg export_start = 1'b0;
    reg collecting = 1'b0;
    reg select_valid = 1'b0;
    reg select_down2 = 1'b0;
    reg [9:0] table_addr = 10'd0;
    reg [2:0] load_kind = 3'd0;
    reg [10:0] load_addr = 11'd0;
    wire select_ready, selected_down2, table_ready, table_loaded, table_fault;
    wire load_ready, busy, done, fault, output_valid, export_done;
    wire signed [7:0] output_data;
    wire [8:0] output_index;
    wire [31:0] core_cycles;
    integer i, ticks = 0, exports = 0;

    road_frontend_shared_core dut(
        .i_clk(clk), .i_rstn(rstn), .i_select_valid(select_valid), .i_select_down2(select_down2),
        .o_select_ready(select_ready), .o_selected_down2(selected_down2),
        .i_table_valid(table_valid), .i_table_addr(table_addr), .i_table_data(16'sd0),
        .o_table_ready(table_ready), .o_table_loaded(table_loaded), .o_table_fault(table_fault),
        .i_load_valid(load_valid), .i_load_kind(load_kind), .i_load_addr(load_addr),
        .i_load_data(32'sd0), .o_load_ready(load_ready), .i_start(start),
        .i_commit_ready(commit_ready), .o_busy(busy), .o_done(done), .o_fault(fault),
        .o_core_cycles(core_cycles), .i_export_start(export_start), .i_output_ready(1'b1),
        .o_output_valid(output_valid), .o_output_data(output_data),
        .o_output_index(output_index), .o_export_done(export_done)
    );

    always @(posedge clk) begin
        ticks = ticks + 1;
        if (ticks > 50000) $fatal(1, "Control reset timeout");
        if (rstn && done && select_ready) $fatal(1, "Select ready during done");
        if (collecting && output_valid) begin
            if (output_index !== exports || output_data !== 8'sd0)
                $fatal(1, "Recovery export mismatch index=%0d data=%0d", output_index, output_data);
            exports = exports + 1;
        end
    end

    task load_zero;
        input [2:0] kind;
        input integer address;
        begin
            @(negedge clk);
            load_valid = 1'b1;
            load_kind = kind;
            load_addr = address;
            if (!load_ready) $fatal(1, "Control load rejected kind=%0d address=%0d", kind, address);
        end
    endtask

    task load_stem_fixture;
        begin
            for (i = 0; i < 432; i = i + 1) load_zero(3'd2, i);
            for (i = 0; i < 16; i = i + 1) load_zero(3'd3, i);
            for (i = 0; i < 16; i = i + 1) load_zero(3'd4, i);
            for (i = 0; i < 16; i = i + 1) load_zero(3'd5, i);
            for (i = 0; i < 2; i = i + 1) load_zero(3'd6, i);
            for (i = 0; i < 243; i = i + 1) load_zero(3'd1, i);
            @(negedge clk); load_valid = 1'b0;
        end
    endtask

    task load_complete_table;
        begin
            for (i = 0; i < 1024; i = i + 1) begin
                @(negedge clk);
                table_valid = 1'b1;
                table_addr = i;
                if (!table_ready) $fatal(1, "Control table rejected address=%0d", i);
            end
            @(negedge clk); table_valid = 1'b0;
            @(posedge clk); @(negedge clk);
            if (!table_loaded) $fatal(1, "Control table incomplete");
        end
    endtask

    task pulse_start;
        begin
            @(negedge clk); start = 1'b1;
            @(negedge clk); start = 1'b0;
        end
    endtask

    task reset_and_check;
        begin
            @(negedge clk); rstn = 1'b0; table_valid = 1'b0; load_valid = 1'b0;
            @(posedge clk); #1;
            if (busy || done || output_valid || export_done || selected_down2 || table_loaded ||
                fault || table_fault || dut.pp_valid || dut.mac_result_valid || dut.s_mac_valid)
                $fatal(1, "Common reset did not cancel shared core state");
            repeat (2) @(negedge clk);
            rstn = 1'b1;
            repeat (2) @(posedge clk);
            if (!select_ready || selected_down2 || table_loaded)
                $fatal(1, "Reset release state invalid");
        end
    endtask

    initial begin
        repeat (4) @(negedge clk);
        rstn = 1'b1;
        // 已装参数和halo时，在共享表装载途中复位；释放后旧状态不能启动。
        load_stem_fixture;
        for (i = 0; i < 128; i = i + 1) begin
            @(negedge clk);
            table_valid = 1'b1;
            table_addr = i;
            if (!table_ready) $fatal(1, "Control table rejected address=%0d", i);
        end
        reset_and_check;
        pulse_start;
        repeat (4) @(posedge clk);
        if (busy || done) $fatal(1, "Reset-retained table or parameters admitted start");

        // Stem 窄地址越界不得截断写入，粘滞 fault 必须封锁所有命令。
        @(negedge clk);
        load_valid = 1'b1;
        load_kind = 3'd2;
        load_addr = 11'd512;
        if (!load_ready || dut.u_stem.cnt_weight_address != 0)
            $fatal(1, "Illegal Stem address precondition");
        @(negedge clk); load_valid = 1'b0;
        if (!fault || dut.u_stem.cnt_weight_address != 0)
            $fatal(1, "Illegal Stem address was truncated or not faulted");
        if (select_ready || load_ready) $fatal(1, "Fault did not block select/load");
        pulse_start;
        if (busy || done) $fatal(1, "Fault did not block start");
        reset_and_check;

        // 长写回反压产生在途结果后复位，旧 valid 不得泄漏；完整重装后必须恢复。
        load_complete_table;
        load_stem_fixture;
        commit_ready = 1'b0;
        pulse_start;
        wait (busy);
        wait (dut.pp_valid);
        repeat (8) @(posedge clk);
        if (!dut.pp_valid || !busy) $fatal(1, "Commit backpressure did not hold result");
        reset_and_check;
        pulse_start;
        repeat (4) @(posedge clk);
        if (busy || done || dut.pp_valid || output_valid)
            $fatal(1, "Old work leaked after reset");
        load_complete_table;
        load_stem_fixture;
        commit_ready = 1'b1;
        pulse_start;
        wait (done);
        if (select_ready) $fatal(1, "Done edge exposed stage switch");
        wait (dut.u_stem.state_current == 4'd0);
        exports = 0;
        collecting = 1'b1;
        @(negedge clk); export_start = 1'b1;
        @(negedge clk); export_start = 1'b0;
        wait (export_done); @(negedge clk);
        collecting = 1'b0;
        if (exports != 256 || fault || !table_loaded)
            $fatal(1, "Recovery tile did not complete");
        // select提前保持valid直到ready，旧主仍必须完成计算及导出，不能循环等待。
        pulse_start;
        wait(busy);
        @(negedge clk); select_valid=1'b1; select_down2=1'b1;
        wait(done);
        if(selected_down2 || select_ready) $fatal(1,"Pending select changed owner before export");
        wait(dut.u_stem.state_current==4'd0);
        exports=0; collecting=1'b1;
        @(negedge clk); export_start=1'b1;
        @(negedge clk); export_start=1'b0;
        wait(export_done); @(negedge clk); collecting=1'b0;
        if(exports!=256) $fatal(1,"Pending select blocked export");
        wait(selected_down2);
        @(negedge clk); select_valid=1'b0;
        if(!table_loaded || dut.pp_pending_count!=0) $fatal(1,"Pending select did not drain");
        @(negedge clk); select_valid=1'b1; select_down2=1'b0;
        if(!select_ready) $fatal(1,"Return to Stem not ready");
        @(negedge clk); select_valid=1'b0;
        if(selected_down2) $fatal(1,"Return to Stem failed");

        // 装表请求在核心运行时保持valid；不能阻止PP排空，也不能提前写坏活动表。
        pulse_start;
        wait(busy);
        @(negedge clk); table_valid=1'b1; table_addr=10'd0;
        #1; if(table_ready) $fatal(1,"Table admitted while running");
        wait(done);
        if(table_ready || !table_loaded) $fatal(1,"Pending table modified active table");
        wait(dut.u_stem.state_current==4'd0);
        exports=0; collecting=1'b1;
        @(negedge clk); export_start=1'b1;
        @(negedge clk); export_start=1'b0;
        wait(export_done); @(negedge clk); collecting=1'b0;
        if(exports!=256) $fatal(1,"Pending table blocked export");
        wait(table_ready);
        @(posedge clk); @(negedge clk); table_valid=1'b0;
        @(posedge clk); @(negedge clk);
        if(table_loaded || fault) $fatal(1,"Pending first table entry not accepted once");
        for(i=1;i<1024;i=i+1)begin
            @(negedge clk); table_valid=1'b1; table_addr=i;
            if(!table_ready) $fatal(1,"Pending table remainder rejected");
        end
        @(negedge clk); table_valid=1'b0;
        @(posedge clk); @(negedge clk);
        if(!table_loaded || fault) $fatal(1,"Pending table did not complete");
        $display("TB_PASS_SHARED_CORE_CONTROL table_reset=1 stale_start_blocked=1 address_fault=1 fault_commands_blocked=1 inflight_reset=1 recovery_tile=1 held_select_progress=1 held_table_progress=1 exports=768");
        $finish;
    end
    counter_prepared_check counter_observer(.clk(clk), .rstn(rstn), .state(dut.u_down2.state_current),
        .layer_pw(dut.u_down2.flag_layer_pw), .position(dut.u_down2.cnt_position),
        .count(dut.u_down2.cnt_output), .prepared(dut.u_down2.reg_cnt_output_prepared),
        .accept(dut.u_down2.flag_mac_input_accept), .last_group(dut.u_down2.flag_mac_last_group),
        .start_accept(dut.u_down2.flag_start_accept), .dw_writes(dut.u_down2.cnt_dw_writes),
        .pp_fault(dut.u_down2.pp_fault), .load_fault(dut.u_down2.flag_load_fault));
endmodule
