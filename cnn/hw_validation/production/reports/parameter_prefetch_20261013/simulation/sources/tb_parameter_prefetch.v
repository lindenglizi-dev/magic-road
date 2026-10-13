`timescale 1ns / 1ps

// Focused ownership test: parameters must follow accepted MAC tasks, not live issuer state.
module tb_parameter_prefetch();
    reg clk = 1'b0;
    always #5 clk = ~clk;

    reg rstn = 1'b0;
    reg table_loaded = 1'b1;
    reg load_valid = 1'b0;
    reg [2:0] load_kind = 3'd0;
    reg [10:0] load_addr = 11'd0;
    reg signed [31:0] load_data = 32'sd0;
    reg start = 1'b0;
    reg pw_only = 1'b0;
    reg commit_ready = 1'b1;
    reg export_start = 1'b0;
    reg output_ready = 1'b1;
    reg mac_ready = 1'b0;
    reg mac_result_valid = 1'b0;
    reg [95:0] mac_result = 96'd0;
    reg mac_fault = 1'b0;
    reg pp_ready = 1'b0;
    reg pp_valid = 1'b0;
    reg signed [15:0] pp_data = 16'sd0;
    reg [15:0] pp_tag = 16'd0;
    reg pp_int16 = 1'b0;
    reg pp_fault = 1'b0;
    reg [1:0] pp_result_queue_count = 2'd0;
    reg [3:0] pp_meta_count = 4'd0;
    reg pp_pre_busy = 1'b0;
    reg pp_silu_busy = 1'b0;
    reg pp_post_busy = 1'b0;
    reg pp_pre_accept = 1'b0;
    reg pp_silu_accept = 1'b0;
    reg pp_post_accept = 1'b0;

    wire load_ready, busy, done, fault, output_valid, export_done;
    wire signed [7:0] output_data;
    wire [8:0] output_index;
    wire debug_valid, debug_layer;
    wire [1:0] debug_phase;
    wire [3:0] debug_position;
    wire [4:0] debug_channel;
    wire signed [31:0] debug_value;
    wire [31:0] preload_writes, core_cycles, mac_cycles, pre_cycles;
    wire [31:0] silu_cycles, post_cycles, writeback_cycles;
    wire [31:0] storage_wait_cycles, scheduler_idle_cycles, export_cycles;
    wire [1:0] result_queue_count;
    wire result_reserved;
    wire [3:0] meta_count;
    wire [31:0] mac_result_count, pre_accept_count, silu_accept_count;
    wire [31:0] post_accept_count, writeback_count;
    wire mac_valid, mac_first, mac_last, mac_result_ready;
    wire [7:0] mac_mask;
    wire [63:0] mac_activation;
    wire [191:0] mac_weight;
    wire [95:0] mac_bias;
    wire pp_input_valid;
    wire [95:0] pp_acc, pp_multipliers;
    wire [17:0] pp_shifts;
    wire [31:0] pp_post_multiplier;
    wire [5:0] pp_post_shift;
    wire [2:0] pp_mask;
    wire [47:0] pp_tags;
    wire pp_input_fault, pp_output_ready;

    integer i;
    integer ticks = 0;
    integer checks = 0;

    road_down2_tile_scheduler dut(
        .i_clk(clk), .i_rstn(rstn), .i_table_loaded(table_loaded),
        .i_load_valid(load_valid), .i_load_kind(load_kind), .i_load_addr(load_addr),
        .i_load_data(load_data), .o_load_ready(load_ready), .i_start(start),
        .i_pw_only(pw_only), .i_commit_ready(commit_ready), .o_busy(busy),
        .o_done(done), .o_fault(fault), .i_export_start(export_start),
        .i_output_ready(output_ready), .o_output_valid(output_valid),
        .o_output_data(output_data), .o_output_index(output_index),
        .o_export_done(export_done), .o_debug_valid(debug_valid),
        .o_debug_phase(debug_phase), .o_debug_layer(debug_layer),
        .o_debug_position(debug_position), .o_debug_channel(debug_channel),
        .o_debug_value(debug_value), .o_preload_writes(preload_writes),
        .o_core_cycles(core_cycles), .o_mac_cycles(mac_cycles),
        .o_pre_cycles(pre_cycles), .o_silu_cycles(silu_cycles),
        .o_post_cycles(post_cycles), .o_writeback_cycles(writeback_cycles),
        .o_storage_wait_cycles(storage_wait_cycles),
        .o_scheduler_idle_cycles(scheduler_idle_cycles), .o_export_cycles(export_cycles),
        .o_result_queue_count(result_queue_count), .o_result_reserved(result_reserved),
        .o_meta_count(meta_count), .o_mac_result_count(mac_result_count),
        .o_pre_accept_count(pre_accept_count), .o_silu_accept_count(silu_accept_count),
        .o_post_accept_count(post_accept_count), .o_writeback_count(writeback_count),
        .i_mac_ready(mac_ready), .i_mac_result_valid(mac_result_valid),
        .i_mac_result(mac_result), .i_mac_fault(mac_fault), .o_mac_valid(mac_valid),
        .o_mac_first(mac_first), .o_mac_last(mac_last), .o_mac_mask(mac_mask),
        .o_mac_activation(mac_activation), .o_mac_weight(mac_weight),
        .o_mac_bias(mac_bias), .o_mac_result_ready(mac_result_ready),
        .i_pp_ready(pp_ready), .i_pp_valid(pp_valid), .i_pp_data(pp_data),
        .i_pp_tag(pp_tag), .i_pp_int16(pp_int16), .i_pp_fault(pp_fault),
        .i_pp_result_queue_count(pp_result_queue_count), .i_pp_meta_count(pp_meta_count),
        .i_pp_pre_busy(pp_pre_busy), .i_pp_silu_busy(pp_silu_busy),
        .i_pp_post_busy(pp_post_busy), .i_pp_pre_accept(pp_pre_accept),
        .i_pp_silu_accept(pp_silu_accept), .i_pp_post_accept(pp_post_accept),
        .o_pp_valid(pp_input_valid), .o_pp_acc(pp_acc),
        .o_pp_multipliers(pp_multipliers), .o_pp_shifts(pp_shifts),
        .o_pp_post_multiplier(pp_post_multiplier), .o_pp_post_shift(pp_post_shift),
        .o_pp_mask(pp_mask), .o_pp_tags(pp_tags), .o_pp_input_fault(pp_input_fault),
        .o_pp_ready(pp_output_ready)
    );

    always @(posedge clk) begin
        ticks = ticks + 1;
        if (ticks > 4000) $fatal(1, "Parameter prefetch timeout");
    end

    function [31:0] expected_multiplier;
        input integer generation;
        input integer channel;
        begin
            expected_multiplier = 32'h10000000 + generation * 32'h00010000 + channel;
        end
    endfunction

    function [5:0] expected_shift;
        input integer generation;
        input integer channel;
        begin
            expected_shift = (generation * 9 + channel + 1) % 63;
        end
    endfunction

    function [31:0] expected_post_multiplier;
        input integer generation;
        input integer layer;
        begin
            expected_post_multiplier = 32'h20000000 + generation * 32'h00010000 + layer;
        end
    endfunction

    function [5:0] expected_post_shift;
        input integer generation;
        input integer layer;
        begin
            expected_post_shift = 6'd50 + generation + layer;
        end
    endfunction

    task reset_epoch;
        begin
            @(negedge clk);
            rstn = 1'b0;
            load_valid = 1'b0;
            mac_ready = 1'b0;
            mac_result_valid = 1'b0;
            mac_fault = 1'b0;
            pp_ready = 1'b0;
            pp_fault = 1'b0;
            repeat (2) @(posedge clk);
            #1;
            if (dut.cnt_pw_meta !== 0 || dut.flag_result_reserved !== 0 || pp_input_valid !== 0)
                $fatal(1, "Reset did not cancel ownership validity");
            @(negedge clk);
            rstn = 1'b1;
            repeat (2) @(posedge clk);
        end
    endtask

    task load_parameters;
        input integer generation;
        begin
            for (i = 0; i < 40; i = i + 1) begin
                @(negedge clk);
                load_valid = 1'b1;
                load_kind = 3'd6;
                load_addr = i;
                load_data = expected_multiplier(generation, i);
                if (!load_ready) $fatal(1, "Multiplier load rejected address=%0d", i);
            end
            @(negedge clk);
            load_valid = 1'b0;
            for (i = 0; i < 40; i = i + 1) begin
                @(negedge clk);
                load_valid = 1'b1;
                load_kind = 3'd7;
                load_addr = i;
                load_data = expected_shift(generation, i);
                if (!load_ready) $fatal(1, "Shift load rejected address=%0d", i);
            end
            for (i = 40; i < 42; i = i + 1) begin
                @(negedge clk);
                load_addr = i;
                load_data = expected_post_multiplier(generation, i - 40);
                if (!load_ready) $fatal(1, "Post multiplier load rejected address=%0d", i);
            end
            for (i = 42; i < 44; i = i + 1) begin
                @(negedge clk);
                load_addr = i;
                load_data = expected_post_shift(generation, i - 42);
                if (!load_ready) $fatal(1, "Post shift load rejected address=%0d", i);
            end
            @(negedge clk);
            load_valid = 1'b0;
        end
    endtask

    task force_scheduler;
        input integer layer_pw;
        begin
            force dut.state_current = 4'd2;
            force dut.flag_busy_o = 1'b1;
            force dut.flag_layer_pw = layer_pw[0];
            force dut.cnt_mac_group = 2'd0;
        end
    endtask

    task release_scheduler;
        begin
            release dut.state_current;
            release dut.flag_busy_o;
            release dut.flag_layer_pw;
            release dut.cnt_mac_group;
            release dut.cnt_position;
            release dut.cnt_output;
        end
    endtask

    task issue_task;
        input integer layer_pw;
        input integer position;
        input integer channel;
        begin
            force dut.cnt_position = position[3:0];
            if (layer_pw != 0)
                force dut.cnt_output = (channel / 3);
            else
                force dut.cnt_output = channel[4:0];
            @(negedge clk);
            mac_ready = 1'b1;
            #1;
            if (!mac_valid || !mac_first)
                $fatal(1, "First group was not offered layer=%0d pos=%0d channel=%0d", layer_pw, position, channel);
            @(posedge clk);
            #1;
            mac_ready = 1'b0;
        end
    endtask

    task expect_parameters;
        input integer generation;
        input integer layer;
        input integer base;
        begin
            #1;
            if (pp_multipliers !== {expected_multiplier(generation, base + 2),
                                    expected_multiplier(generation, base + 1),
                                    expected_multiplier(generation, base)} ||
                pp_shifts !== {expected_shift(generation, base + 2),
                               expected_shift(generation, base + 1),
                               expected_shift(generation, base)} ||
                pp_post_multiplier !== expected_post_multiplier(generation, layer) ||
                pp_post_shift !== expected_post_shift(generation, layer))
                $fatal(1, "Parameter mismatch generation=%0d layer=%0d base=%0d", generation, layer, base);
            checks = checks + 1;
        end
    endtask

    task accept_pw_result;
        input integer generation;
        input integer group_base;
        begin
            @(negedge clk);
            mac_result_valid = 1'b1;
            pp_ready = 1'b1;
            #1;
            if (!pp_input_valid || !mac_result_ready || pp_mask !== 3'b111)
                $fatal(1, "PW result was not valid group=%0d", group_base);
            expect_parameters(generation, 1, 16 + group_base);
            @(posedge clk);
            #1;
            mac_result_valid = 1'b0;
            pp_ready = 1'b0;
        end
    endtask

    reg [95:0] held_multipliers;
    reg [17:0] held_shifts;
    reg [31:0] held_post_multiplier;
    reg [5:0] held_post_shift;
    reg [95:0] held_acc;
    reg [47:0] held_tags;
    reg [2:0] held_mask;
    reg [1:0] ring_wrap_origin;

    initial begin
        reset_epoch;
        load_parameters(0);

        // Ownership fault-injection after legal parameter loads; full-frame input-only tests run separately.
        // PW capture must match the frozen legacy lookup and hold under output stall.
        force_scheduler(1);
        issue_task(1, 2, 6);
        mac_result = {32'h33333333, 32'h22222222, 32'h11111111};
        @(negedge clk);
        mac_result_valid = 1'b1;
        pp_ready = 1'b0;
        #1;
        if (!pp_input_valid || mac_result_ready || pp_acc !== mac_result || pp_mask !== 3'b111)
            $fatal(1, "PW stalled payload precondition failed");
        expect_parameters(0, 1, 22);
        held_multipliers = pp_multipliers;
        held_shifts = pp_shifts;
        held_post_multiplier = pp_post_multiplier;
        held_post_shift = pp_post_shift;
        held_acc = pp_acc;
        held_tags = pp_tags;
        held_mask = pp_mask;
        repeat (3) begin
            @(posedge clk);
            #1;
            if (!pp_input_valid || {pp_multipliers, pp_shifts, pp_post_multiplier,
                pp_post_shift, pp_acc, pp_tags, pp_mask} !==
                {held_multipliers, held_shifts, held_post_multiplier,
                held_post_shift, held_acc, held_tags, held_mask})
                $fatal(1, "PW payload changed while ready was low");
        end
        pp_ready = 1'b1;
        @(posedge clk);
        #1;
        mac_result_valid = 1'b0;
        pp_ready = 1'b0;
        if (dut.cnt_pw_meta !== 0) $fatal(1, "PW transfer did not pop owner");

        // Four full-ring pop/push edges must read the old head and wrap both pointers.
        issue_task(1, 0, 0);
        issue_task(1, 1, 3);
        issue_task(1, 2, 6);
        issue_task(1, 3, 9);
        ring_wrap_origin = dut.ptr_pw_meta_read;
        if (dut.ptr_pw_meta_write !== ring_wrap_origin || dut.cnt_pw_meta !== 4)
            $fatal(1, "Full-ring setup did not align read/write pointers");
        force dut.cnt_position = 4'd9;
        force dut.cnt_output = 5'd4;
        @(negedge clk);
        mac_ready = 1'b1;
        #1;
        if (mac_valid) $fatal(1, "Full owner ring accepted without a pop");
        mac_ready = 1'b0;
        for (i = 0; i < 4; i = i + 1) begin
            force dut.cnt_position = i + 4;
            force dut.cnt_output = i + 4;
            @(negedge clk);
            mac_ready = 1'b1;
            mac_result_valid = 1'b1;
            pp_ready = 1'b1;
            #1;
            if (!mac_valid || !mac_result_ready || !pp_input_valid)
                $fatal(1, "Full-ring simultaneous transfer missing index=%0d", i);
            expect_parameters(0, 1, 16 + i * 3);
            @(posedge clk);
            #1;
            mac_ready = 1'b0;
            mac_result_valid = 1'b0;
            pp_ready = 1'b0;
            if (dut.cnt_pw_meta !== 4) $fatal(1, "Full-ring count changed index=%0d", i);
        end
        if (dut.ptr_pw_meta_read !== ring_wrap_origin ||
            dut.ptr_pw_meta_write !== ring_wrap_origin)
            $fatal(1, "Owner pointers did not wrap");
        for (i = 0; i < 4; i = i + 1)
            accept_pw_result(0, (i + 4) * 3);

        // An accepted record must ignore later RAM mutation; loads are illegal while busy.
        issue_task(1, 5, 9);
        dut.reg_pre_multiplier[25] = 32'h7ffff001;
        dut.reg_pre_multiplier[26] = 32'h7ffff002;
        dut.reg_pre_multiplier[27] = 32'h7ffff003;
        dut.reg_pre_shift[25] = 6'd1;
        dut.reg_pre_shift[26] = 6'd2;
        dut.reg_pre_shift[27] = 6'd3;
        dut.reg_post_multiplier[1] = 32'h7ffff004;
        dut.reg_post_shift[1] = 6'd4;
        accept_pw_result(0, 9);

        // DW pop transfers the snapshot into active; same edge consumes old scalar and installs new.
        release_scheduler;
        reset_epoch;
        load_parameters(0);
        force_scheduler(0);
        issue_task(0, 3, 5);
        issue_task(0, 4, 14);
        dut.reg_pre_multiplier[3] = 32'h7ffff011;
        dut.reg_pre_multiplier[4] = 32'h7ffff012;
        dut.reg_pre_multiplier[5] = 32'h7ffff013;
        dut.reg_pre_multiplier[12] = 32'h7ffff021;
        dut.reg_pre_multiplier[13] = 32'h7ffff022;
        dut.reg_pre_multiplier[14] = 32'h7ffff023;
        dut.reg_post_multiplier[0] = 32'h7ffff024;
        mac_result = {32'hcccccccc, 32'hbbbbbbbb, 32'haaaaaaaa};
        @(negedge clk);
        mac_result_valid = 1'b1;
        #1;
        if (!mac_result_ready || pp_input_valid) $fatal(1, "First DW pop precondition failed");
        @(posedge clk);
        #1;
        mac_result_valid = 1'b0;
        if (!pp_input_valid || pp_mask !== 3'b100) $fatal(1, "First DW active payload missing");
        expect_parameters(0, 0, 3);
        mac_result = {32'h66666666, 32'h55555555, 32'h44444444};
        @(negedge clk);
        mac_result_valid = 1'b1;
        pp_ready = 1'b1;
        #1;
        if (!pp_input_valid || !mac_result_ready) $fatal(1, "DW replacement edge missing");
        expect_parameters(0, 0, 3);
        @(posedge clk);
        #1;
        mac_result_valid = 1'b0;
        pp_ready = 1'b0;
        if (!pp_input_valid || dut.reg_dw_active_meta !== {4'd4, 5'd14})
            $fatal(1, "DW replacement did not install new owner");
        expect_parameters(0, 0, 12);
        held_multipliers = pp_multipliers;
        held_shifts = pp_shifts;
        held_post_multiplier = pp_post_multiplier;
        held_post_shift = pp_post_shift;
        repeat (2) begin
            @(posedge clk);
            #1;
            if ({pp_multipliers, pp_shifts, pp_post_multiplier, pp_post_shift} !==
                {held_multipliers, held_shifts, held_post_multiplier, held_post_shift})
                $fatal(1, "DW active parameters changed during stall");
        end
        for (i = 0; i < 3; i = i + 1) begin
            @(negedge clk);
            pp_ready = 1'b1;
            #1;
            if (!pp_input_valid || pp_tags[14:11] !== 4 + i)
                $fatal(1, "DW scalar order mismatch index=%0d", i);
            expect_parameters(0, 0, 12);
            @(posedge clk);
            #1;
            pp_ready = 1'b0;
        end
        if (dut.flag_result_reserved || pp_input_valid)
            $fatal(1, "DW active slot did not retire");

        // DW full-ring same-slot pop/push also replaces a retiring active scalar on that edge.
        release_scheduler;
        reset_epoch;
        load_parameters(0);
        force_scheduler(0);
        issue_task(0, 3, 15);
        mac_result = {32'h03030303, 32'h02020202, 32'h01010101};
        @(negedge clk);
        mac_result_valid = 1'b1;
        #1;
        if (!mac_result_ready || pp_input_valid) $fatal(1, "DW channel15 active setup failed");
        @(posedge clk);
        #1;
        mac_result_valid = 1'b0;
        if (!pp_input_valid || pp_mask !== 3'b001)
            $fatal(1, "DW channel15 did not use onehot lane0");
        expect_parameters(0, 0, 15);
        issue_task(0, 0, 0);
        issue_task(0, 3, 1);
        issue_task(0, 4, 2);
        issue_task(0, 7, 3);
        if (dut.cnt_pw_meta !== 4 || dut.ptr_pw_meta_read !== dut.ptr_pw_meta_write)
            $fatal(1, "DW full-ring setup failed");
        ring_wrap_origin = dut.ptr_pw_meta_read;
        force dut.cnt_position = 4'd8;
        force dut.cnt_output = 5'd6;
        mac_result = {32'h33330003, 32'h22220002, 32'h11110001};
        @(negedge clk);
        mac_ready = 1'b1;
        mac_result_valid = 1'b1;
        pp_ready = 1'b1;
        #1;
        if (!dut.flag_shared_meta_push || !dut.flag_shared_meta_pop ||
            !dut.flag_dw_active_last_accept || !pp_input_valid || !mac_result_ready)
            $fatal(1, "DW full-ring replace/push edge was not simultaneous");
        if (pp_mask !== 3'b001) $fatal(1, "DW old active payload changed before replacement");
        expect_parameters(0, 0, 15);
        @(posedge clk);
        #1;
        mac_ready = 1'b0;
        mac_result_valid = 1'b0;
        pp_ready = 1'b0;
        if (dut.cnt_pw_meta !== 4 || dut.ptr_pw_meta_read !== ring_wrap_origin + 2'd1 ||
            dut.ptr_pw_meta_write !== ring_wrap_origin + 2'd1)
            $fatal(1, "DW full-ring same-slot pointers/count incorrect");
        if (!dut.flag_result_reserved || dut.reg_dw_active_meta !== {4'd0, 5'd0})
            $fatal(1, "DW full-ring pop did not install the old head");
        expect_parameters(0, 0, 0);

        // A faulting MAC result pops/cancels ownership but must never install an active record.
        release_scheduler;
        reset_epoch;
        load_parameters(0);
        force_scheduler(0);
        issue_task(0, 0, 5);
        mac_result = {32'hdead0003, 32'hdead0002, 32'hdead0001};
        @(negedge clk);
        mac_result_valid = 1'b1;
        mac_fault = 1'b1;
        #1;
        if (!mac_result_ready || !dut.flag_mac_fault_accept)
            $fatal(1, "MAC fault was not accepted");
        @(posedge clk);
        #1;
        mac_result_valid = 1'b0;
        mac_fault = 1'b0;
        if (dut.flag_result_reserved || pp_input_valid || dut.cnt_pw_meta !== 0 ||
            dut.reg_dw_active_meta !== 9'd0)
            $fatal(1, "Faulting MAC result installed active ownership");

        // Terminal fault blocks stale ownership; reset creates a clean epoch and new parameters.
        release_scheduler;
        reset_epoch;
        load_parameters(0);
        force_scheduler(1);
        issue_task(1, 1, 0);
        release_scheduler;
        @(negedge clk);
        pp_fault = 1'b1;
        @(posedge clk);
        #1;
        if (!fault || pp_input_valid || busy || dut.cnt_pw_meta !== 1)
            $fatal(1, "Fault did not gate stale ownership");
        pp_fault = 1'b0;
        reset_epoch;
        load_parameters(1);
        force_scheduler(1);
        issue_task(1, 0, 0);
        mac_result = 96'h0123456789abcdef01234567;
        @(negedge clk);
        mac_result_valid = 1'b1;
        pp_ready = 1'b0;
        #1;
        if (!pp_input_valid) $fatal(1, "New epoch result missing");
        expect_parameters(1, 1, 16);
        if (pp_multipliers === {expected_multiplier(0, 18), expected_multiplier(0, 17),
                                expected_multiplier(0, 16)})
            $fatal(1, "Old epoch parameters leaked");
        pp_ready = 1'b1;
        @(posedge clk);
        #1;
        mac_result_valid = 1'b0;
        pp_ready = 1'b0;

        if (checks < 19) $fatal(1, "Insufficient parameter comparisons checks=%0d", checks);
        $display("TB_PASS_PARAMETER_PREFETCH checks=%0d ring_wrap=1 dw_replace=1 stalls=1 fault=1 epoch_reset=1", checks);
        $finish;
    end
endmodule
