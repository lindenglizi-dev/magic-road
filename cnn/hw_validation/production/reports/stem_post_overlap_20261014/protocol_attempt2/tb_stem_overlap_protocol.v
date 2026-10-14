`timescale 1ns / 1ps

// Stem/PP重叠协议验证；使用共享顶层及真实MAC、重定标、SiLU和退休队列。
module tb_stem_overlap_protocol(output reg o_test_done);
    localparam [3:0] ST_SEND = 4'd2;
    localparam [3:0] ST_MAC_WAIT = 4'd3;
    localparam [3:0] ST_FAULT = 4'd8;

    reg clk;
    reg rstn;
    reg table_valid;
    reg load_valid;
    reg start;
    reg commit_ready;
    reg export_start;
    reg output_ready;
    reg select_valid;
    reg select_down2;
    reg [9:0] table_addr;
    reg signed [15:0] table_data;
    reg [2:0] load_kind;
    reg [10:0] load_addr;
    reg signed [31:0] load_data;
    wire select_ready;
    wire selected_down2;
    wire table_ready;
    wire table_loaded;
    wire table_fault;
    wire load_ready;
    wire busy;
    wire done;
    wire fault;
    wire [31:0] core_cycles;
    wire output_valid;
    wire signed [7:0] output_data;
    wire [8:0] output_index;
    wire export_done;

    integer ticks;
    integer i;
    integer stage;
    integer lane;
    integer commit_count;
    integer export_count;
    integer metadata_batches;
    integer mac_accept_while_pending;
    integer max_pending;
    integer max_ingress;
    integer reset_checks;
    integer tag_fault_checks;
    integer successful_tiles;
    reg track_commits;
    reg track_exports;
    reg check_metadata;
    reg export_armed;
    reg [15:0] held_tag;
    reg signed [15:0] held_data;
    reg held_int16;
    reg [15:0] observed_tag;
    reg [31:0] expected_multiplier;

    road_frontend_shared_core dut(
        .i_clk(clk), .i_rstn(rstn),
        .i_select_valid(select_valid), .i_select_down2(select_down2),
        .o_select_ready(select_ready), .o_selected_down2(selected_down2),
        .i_table_valid(table_valid), .i_table_addr(table_addr), .i_table_data(table_data),
        .o_table_ready(table_ready), .o_table_loaded(table_loaded), .o_table_fault(table_fault),
        .i_load_valid(load_valid), .i_load_kind(load_kind), .i_load_addr(load_addr),
        .i_load_data(load_data), .o_load_ready(load_ready), .i_start(start),
        .i_commit_ready(commit_ready), .o_busy(busy), .o_done(done), .o_fault(fault),
        .o_core_cycles(core_cycles), .i_export_start(export_start), .i_output_ready(output_ready),
        .o_output_valid(output_valid), .o_output_data(output_data),
        .o_output_index(output_index), .o_export_done(export_done)
    );

    always #5 clk = ~clk;

    // 仅在真实握手上计数；标签顺序和每通道动态pre参数同时检查。
    always @(posedge clk) begin
        ticks = ticks + 1;
        if (ticks > 200000)
            $fatal(1, "Stem overlap watchdog timeout");
        if (rstn) begin
            if (dut.pp_pending_count > max_pending)
                max_pending = dut.pp_pending_count;
            if (dut.pp_queue_count > max_ingress)
                max_ingress = dut.pp_queue_count;
            if (dut.s_mac_valid && dut.s_mac_ready && dut.pp_pending_count != 0)
                mac_accept_while_pending = mac_accept_while_pending + 1;
            if (check_metadata && dut.s_pp_valid && dut.s_pp_ready) begin
                metadata_batches = metadata_batches + 1;
                for (lane = 0; lane < 3; lane = lane + 1) begin
                    if (dut.s_pp_mask[lane]) begin
                        observed_tag = dut.s_pp_tags[lane*16 +: 16];
                        expected_multiplier = {28'd0, observed_tag[3:0]} + 32'd1;
                        if (observed_tag[15:8] !== 8'd0)
                            $fatal(1, "Stem PP input tag high bits lane=%0d tag=%h", lane, observed_tag);
                        if (dut.s_pp_multipliers[lane*32 +: 32] !== expected_multiplier)
                            $fatal(1, "Stem PP multiplier capture lane=%0d tag=%h got=%h expected=%h",
                                   lane, observed_tag, dut.s_pp_multipliers[lane*32 +: 32], expected_multiplier);
                    end else if (dut.s_pp_multipliers[lane*32 +: 32] !== 32'd0) begin
                        $fatal(1, "Stem PP masked multiplier not zero lane=%0d", lane);
                    end
                end
            end
            if (track_commits && dut.pp_valid && dut.s_pp_output_ready) begin
                if (dut.pp_tag[15:8] !== 8'd0 || dut.pp_tag[7:0] !== commit_count[7:0])
                    $fatal(1, "Stem commit order got=%h expected=%0d", dut.pp_tag, commit_count);
                if (dut.pp_int16 || dut.pp_data !== 16'sd0)
                    $fatal(1, "Stem zero commit payload tag=%h data=%0d int16=%0d",
                           dut.pp_tag, $signed(dut.pp_data), dut.pp_int16);
                commit_count = commit_count + 1;
            end
            if (track_commits && done && commit_count != 256)
                $fatal(1, "Stem done before all commits count=%0d", commit_count);
            if (output_valid && (!export_armed || commit_count != 256))
                $fatal(1, "Stem output published early commits=%0d armed=%0d", commit_count, export_armed);
            if (track_exports && output_valid && output_ready) begin
                if (output_index !== export_count || output_data !== 8'sd0)
                    $fatal(1, "Stem recovery export mismatch index=%0d expected=%0d data=%0d",
                           output_index, export_count, $signed(output_data));
                export_count = export_count + 1;
            end
            if (export_done && export_count != 256)
                $fatal(1, "Stem export_done before 256 outputs count=%0d", export_count);
        end
    end

    task load_word;
        input [2:0] kind;
        input integer address;
        input [31:0] value;
        begin
            @(negedge clk);
            load_valid = 1'b1;
            load_kind = kind;
            load_addr = address;
            load_data = value;
            #1;
            if (!load_ready)
                $fatal(1, "Stem overlap load rejected kind=%0d address=%0d", kind, address);
        end
    endtask

    task load_table;
        begin
            for (i = 0; i < 1024; i = i + 1) begin
                @(negedge clk);
                table_valid = 1'b1;
                table_addr = i;
                table_data = 16'sd0;
                #1;
                if (!table_ready)
                    $fatal(1, "Stem overlap table rejected address=%0d", i);
            end
            @(negedge clk);
            table_valid = 1'b0;
            @(posedge clk);
            #1;
            if (!table_loaded || table_fault)
                $fatal(1, "Stem overlap table incomplete or faulted");
        end
    endtask

    task load_zero_fixture;
        begin
            for (i = 0; i < 432; i = i + 1)
                load_word(3'd2, i, 32'd0);
            for (i = 0; i < 16; i = i + 1)
                load_word(3'd3, i, 32'd0);
            // Distinct multipliers prove that each queued batch retains its own channel metadata.
            for (i = 0; i < 16; i = i + 1)
                load_word(3'd4, i, i + 1);
            for (i = 0; i < 16; i = i + 1)
                load_word(3'd5, i, 32'd0);
            load_word(3'd6, 0, 32'd1);
            load_word(3'd6, 1, 32'd0);
            for (i = 0; i < 243; i = i + 1)
                load_word(3'd1, i, 32'd0);
            @(negedge clk);
            load_valid = 1'b0;
            #1;
            if (dut.u_stem.reg_loaded !== 6'b111111)
                $fatal(1, "Stem overlap fixture incomplete loaded=%b", dut.u_stem.reg_loaded);
        end
    endtask

    task prepare_fixture;
        begin
            if (!rstn || fault || busy || table_loaded)
                $fatal(1, "Stem overlap prepare precondition rstn=%0d fault=%0d busy=%0d table=%0d",
                       rstn, fault, busy, table_loaded);
            load_table;
            load_zero_fixture;
        end
    endtask

    task pulse_start;
        begin
            export_armed = 1'b0;
            @(negedge clk);
            start = 1'b1;
            @(negedge clk);
            start = 1'b0;
            wait (busy);
        end
    endtask

    task reset_and_check;
        input integer stage_code;
        begin
            @(negedge clk);
            rstn = 1'b0;
            table_valid = 1'b0;
            load_valid = 1'b0;
            start = 1'b0;
            export_start = 1'b0;
            commit_ready = 1'b1;
            output_ready = 1'b1;
            track_commits = 1'b0;
            track_exports = 1'b0;
            check_metadata = 1'b0;
            export_armed = 1'b0;
            commit_count = 0;
            #1;
            if (busy || done || fault || table_loaded || output_valid || export_done ||
                dut.mac_result_valid || dut.pp_valid || dut.pp_pending_count != 0 ||
                dut.pp_queue_count != 0 || dut.pp_meta_count != 0 || dut.pp_pre_busy ||
                dut.pp_silu_busy || dut.pp_post_busy || dut.u_stem.state_current != 4'd0 ||
                dut.u_stem.cnt_written != 0 || dut.u_stem.flag_tile_valid ||
                dut.u_stem.reg_loaded != 0)
                $fatal(1, "Reset did not cancel stage=%0d", stage_code);
            repeat (2) @(negedge clk);
            rstn = 1'b1;
            repeat (2) @(posedge clk);
            #1;
            if (!select_ready || selected_down2 || table_loaded || fault ||
                dut.pp_pending_count != 0 || dut.pp_queue_count != 0 || dut.pp_meta_count != 0)
                $fatal(1, "Reset release invalid stage=%0d", stage_code);
            reset_checks = reset_checks + 1;
        end
    endtask

    task export_zero_tile;
        begin
            wait (dut.u_stem.state_current == 4'd0);
            if (output_valid || export_done)
                $fatal(1, "Stem output visible before export command");
            export_count = 0;
            track_exports = 1'b1;
            export_armed = 1'b1;
            @(negedge clk);
            export_start = 1'b1;
            @(negedge clk);
            export_start = 1'b0;
            wait (export_done);
            @(negedge clk);
            track_exports = 1'b0;
            if (export_count != 256 || fault)
                $fatal(1, "Stem zero tile export incomplete count=%0d fault=%0d", export_count, fault);
        end
    endtask

    task run_success_tile;
        input hold_commits;
        begin
            commit_count = 0;
            export_count = 0;
            metadata_batches = 0;
            mac_accept_while_pending = 0;
            max_pending = 0;
            max_ingress = 0;
            track_commits = 1'b1;
            check_metadata = 1'b1;
            commit_ready = hold_commits ? 1'b0 : 1'b1;
            pulse_start;
            if (hold_commits) begin
                wait (dut.pp_pending_count == 4'd8 && dut.pp_valid);
                held_tag = dut.pp_tag;
                held_data = dut.pp_data;
                held_int16 = dut.pp_int16;
                if (dut.u_stem.cnt_written != 0 || done || output_valid || dut.u_stem.flag_tile_valid)
                    $fatal(1, "Stem published before stalled PP head retired");
                for (i = 0; i < 512; i = i + 1) begin
                    @(posedge clk);
                    #1;
                    if (!dut.pp_valid || dut.pp_tag !== held_tag || dut.pp_data !== held_data ||
                        dut.pp_int16 !== held_int16)
                        $fatal(1, "Stem PP payload changed under 512-cycle stall cycle=%0d", i);
                    if (dut.pp_pending_count != 4'd8 || dut.s_pp_output_ready ||
                        dut.u_stem.cnt_written != 0 || done || output_valid || !busy)
                        $fatal(1, "Stem full PP queue escaped backpressure cycle=%0d", i);
                end
                @(negedge clk);
                commit_ready = 1'b1;
            end
            wait (done);
            #1;
            if (commit_count != 256 || dut.u_stem.cnt_written != 9'd256 ||
                !dut.u_stem.flag_tile_valid)
                $fatal(1, "Stem completion mismatch commits=%0d written=%0d valid=%0d",
                       commit_count, dut.u_stem.cnt_written, dut.u_stem.flag_tile_valid);
            if (max_pending < 2 || mac_accept_while_pending == 0 || metadata_batches != 96)
                $fatal(1, "Stem overlap proof missing pending=%0d mac_overlap=%0d batches=%0d",
                       max_pending, mac_accept_while_pending, metadata_batches);
            if (hold_commits && max_pending != 8)
                $fatal(1, "Stem retirement queue never filled max=%0d", max_pending);
            @(negedge clk);
            track_commits = 1'b0;
            check_metadata = 1'b0;
            export_zero_tile;
            successful_tiles = successful_tiles + 1;
        end
    endtask

    task reset_during_stage;
        input integer stage_code;
        begin
            prepare_fixture;
            commit_ready = stage_code == 4 ? 1'b0 : 1'b1;
            pulse_start;
            case (stage_code)
                0: wait (dut.s_mac_valid && dut.s_mac_ready && dut.u_stem.state_current == ST_SEND);
                1: wait (dut.pp_pre_busy);
                2: wait (dut.pp_silu_busy);
                3: wait (dut.pp_post_busy);
                4: wait (dut.pp_valid && !dut.s_pp_output_ready);
                default: $fatal(1, "Unknown reset stage=%0d", stage_code);
            endcase
            reset_and_check(stage_code);
        end
    endtask

    task inject_tag_fault;
        input duplicate_tag;
        begin
            prepare_fixture;
            commit_ready = duplicate_tag ? 1'b1 : 1'b0;
            pulse_start;
            if (duplicate_tag) begin
                wait (dut.u_stem.cnt_written == 9'd1);
                @(negedge clk);
                commit_ready = 1'b0;
                wait (dut.pp_valid);
                force dut.pp_tag = 16'h0000;
            end else begin
                wait (dut.pp_valid);
                force dut.pp_tag = 16'h0100;
            end
            #1;
            commit_ready = 1'b1;
            @(posedge clk);
            #1;
            release dut.pp_tag;
            repeat (2) @(posedge clk);
            #1;
            if (!fault || dut.u_stem.state_current != ST_FAULT ||
                dut.u_stem.flag_tile_valid || done || output_valid || export_done) begin
                if (duplicate_tag)
                    $fatal(1, "Stem duplicate tag did not fault without publication");
                else
                    $fatal(1, "Stem illegal tag did not fault without publication");
            end
            tag_fault_checks = tag_fault_checks + 1;
            reset_and_check(duplicate_tag ? 6 : 5);
        end
    endtask

    task inject_last_mac_fault;
        begin
            prepare_fixture;
            commit_ready = 1'b1;
            pulse_start;
            wait (dut.u_stem.state_current == ST_MAC_WAIT &&
                  dut.u_stem.cnt_position == 4'd15 && dut.u_stem.cnt_channel == 4'd15 &&
                  dut.mac_result_valid);
            force dut.mac_fault = 1'b1;
            @(posedge clk);
            #1;
            release dut.mac_fault;
            repeat (2) @(posedge clk);
            #1;
            if (!fault || dut.u_stem.state_current != ST_FAULT ||
                dut.u_stem.flag_tile_valid || done || output_valid || export_done ||
                dut.u_stem.cnt_written > 9'd255)
                $fatal(1, "Late MAC fault published a tile written=%0d", dut.u_stem.cnt_written);
            reset_and_check(7);
        end
    endtask

    initial begin
        clk = 1'b0;
        rstn = 1'b0;
        table_valid = 1'b0;
        load_valid = 1'b0;
        start = 1'b0;
        commit_ready = 1'b1;
        export_start = 1'b0;
        output_ready = 1'b1;
        select_valid = 1'b0;
        select_down2 = 1'b0;
        table_addr = 10'd0;
        table_data = 16'sd0;
        load_kind = 3'd0;
        load_addr = 11'd0;
        load_data = 32'sd0;
        o_test_done = 1'b0;
        ticks = 0;
        commit_count = 0;
        export_count = 0;
        metadata_batches = 0;
        mac_accept_while_pending = 0;
        max_pending = 0;
        max_ingress = 0;
        reset_checks = 0;
        tag_fault_checks = 0;
        successful_tiles = 0;
        track_commits = 1'b0;
        track_exports = 1'b0;
        check_metadata = 1'b0;
        export_armed = 1'b0;

        repeat (4) @(negedge clk);
        rstn = 1'b1;
        repeat (2) @(posedge clk);

        // 退休队列填满并保持512拍，释放后仍须按0..255提交和导出。
        prepare_fixture;
        run_success_tile(1'b1);
        reset_and_check(8);

        // 五个实际活动点的复位均取消MAC/PP/表/发布状态。
        for (stage = 0; stage < 5; stage = stage + 1)
            reset_during_stage(stage);

        // 真实PP valid保持，仅替换接口tag，分别命中非法高位和重复序号守卫。
        inject_tag_fault(1'b0);
        inject_tag_fault(1'b1);

        // 最后一项真实MAC结果上注入故障，已完成的旧PP项也不得发布整tile。
        inject_last_mac_fault;

        // 所有取消/故障复位后完整重装，恢复256个已知零输出。
        prepare_fixture;
        run_success_tile(1'b0);

        if (reset_checks != 9 || tag_fault_checks != 2 || successful_tiles != 2)
            $fatal(1, "Stem protocol coverage counters reset=%0d tag=%0d success=%0d",
                   reset_checks, tag_fault_checks, successful_tiles);
        o_test_done = 1'b1;
        $display("TB_PASS_STEM_OVERLAP_PROTOCOL pending_max=8 ingress_max=%0d mac_accept_while_pending=%0d stall_cycles=512 commits=256 exports=256 reset_points=5 tag_faults=2 late_mac_fault=1 recovery_tiles=%0d",
                 max_ingress, mac_accept_while_pending, successful_tiles);
        $finish;
    end
endmodule
