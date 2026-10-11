`timescale 1ns / 1ps

// 全量共享核验证：真实 Stem 导出喂给 down2，两个阶段只使用一套 MAC 和后处理。
module tb_frontend_shared();
    reg clk = 1'b0;
    always #5 clk = ~clk;
    reg rstn = 1'b0;
    reg select_valid = 1'b0;
    reg select_down2 = 1'b0;
    reg table_valid = 1'b0;
    reg load_valid = 1'b0;
    reg start = 1'b0;
    reg commit_ready = 1'b1;
    reg output_ready = 1'b1;
    reg export_start = 1'b0;
    reg force_output_stall = 1'b0;
    reg stem_load_valid = 1'b0;
    reg stem_start = 1'b0;
    reg stem_export_start = 1'b0;
    reg [9:0] table_addr = 10'd0;
    reg signed [15:0] table_data = 16'sd0;
    reg [2:0] load_kind = 3'd0;
    reg [10:0] load_addr = 11'd0;
    reg signed [31:0] load_data = 32'sd0;
    reg [2:0] stem_load_kind = 3'd0;
    reg [8:0] stem_load_addr = 9'd0;
    reg [31:0] stem_load_data = 32'd0;
    wire select_ready, selected_down2;
    wire table_ready, table_loaded, table_fault, core_load_ready;
    wire busy, done, fault, output_valid, export_done;
    wire signed [7:0] output_data;
    wire [8:0] output_index;
    wire [31:0] core_cycles;
    wire core_load_valid = selected_down2 ? load_valid : stem_load_valid;
    wire [2:0] core_load_kind = selected_down2 ? load_kind : stem_load_kind;
    wire [10:0] core_load_addr = selected_down2 ? load_addr : {2'd0, stem_load_addr};
    wire signed [31:0] core_load_data = selected_down2 ? load_data : stem_load_data;
    wire core_start = selected_down2 ? start : stem_start;
    wire core_export_start = selected_down2 ? export_start : stem_export_start;
    wire load_ready = selected_down2 && core_load_ready;
    wire [31:0] preload_writes = dut.u_down2.cnt_preload_writes;
    wire [31:0] export_cycles = dut.u_down2.cnt_export_cycles;
    reg [15:0] table_mem [0:1023];
    reg [7:0] input_tensor [0:589823];
    reg [7:0] expected_halo [0:746495];
    reg [7:0] expected_stem [0:589823];
    reg [7:0] dw_weight [0:143];
    reg [7:0] pw_weight [0:383];
    reg [7:0] expected_output [0:221183];
    reg [31:0] dw_bias [0:15];
    reg [31:0] pw_bias [0:23];
    reg [31:0] multipliers [0:39];
    reg [31:0] controls [0:43];
    reg [31:0] expected_acc [0:368639];
    reg [31:0] expected_stages [0:1105919];
    reg [7:0] actual_output [0:221183];
    reg seen_commit [0:368639];
    reg seen_export [0:221183];
    reg checking = 1'b0;
    reg held_commit = 1'b0;
    reg held_export = 1'b0;
    reg [15:0] previous_tag;
    reg [8:0] previous_index;
    reg [7:0] previous_commit_data, previous_export_data;
    reg [15:0] random_bits = 16'hace1;
    reg [4095:0] vector_dir, report_path, dump_path, file_path;
    reg [127:0] mode;
    integer ticks = 0, tile = 0, report, dump;
    integer i, j, hy, hx, hc, gy, gx, source_address, padding_count = 0;
    integer lane, layer, position, channel, local_index, full_index, index_stage;
    integer dw_commits, pw_commits, exports, acc_count, pre_count, silu_count, post_count;
    integer bins [0:7];
    integer category, bin_sum, core_seen, dw_cycles, pw_cycles, load_begin;

    road_frontend_shared_core dut(
        .i_clk(clk), .i_rstn(rstn), .i_select_valid(select_valid),
        .i_select_down2(select_down2), .o_select_ready(select_ready),
        .o_selected_down2(selected_down2), .i_table_valid(table_valid),
        .i_table_addr(table_addr), .i_table_data(table_data), .o_table_ready(table_ready),
        .o_table_loaded(table_loaded), .o_table_fault(table_fault),
        .i_load_valid(core_load_valid), .i_load_kind(core_load_kind),
        .i_load_addr(core_load_addr), .i_load_data(core_load_data), .o_load_ready(core_load_ready),
        .i_start(core_start), .i_commit_ready(commit_ready), .o_busy(busy), .o_done(done),
        .o_fault(fault), .o_core_cycles(core_cycles), .i_export_start(core_export_start),
        .i_output_ready(output_ready), .o_output_valid(output_valid), .o_output_data(output_data),
        .o_output_index(output_index), .o_export_done(export_done)
    );

    task resolve_stage;
        input [15:0] internal_tag;
        output integer resolved;
        reg [47:0] tags;
        reg [15:0] external_tag;
        integer slot, tag_lane, tag_layer, tag_position, tag_channel;
        begin
            if (internal_tag[15:5] !== 11'd0 || internal_tag[1:0] > 2)
                $fatal(1, "Invalid stage tag tile=%0d", tile);
            slot = internal_tag[4:2];
            tag_lane = internal_tag[1:0];
            tags = dut.u_pp.reg_retire_tags[slot];
            external_tag = tags >> (tag_lane * 16);
            tag_layer = external_tag[15];
            tag_position = external_tag[14:11];
            tag_channel = external_tag[10:6];
            if ((!tag_layer && tag_channel >= 16) || (tag_layer && tag_channel >= 24))
                $fatal(1, "Invalid stage channel");
            resolved = tile * 640 + (tag_layer ? 256 + tag_position * 24 + tag_channel :
                                                   tag_position * 16 + tag_channel);
        end
    endtask

    task reject_select;
        input requested_down2;
        input [319:0] reason;
        reg previous_owner;
        begin
            previous_owner = selected_down2;
            @(negedge clk);
            select_valid = 1'b1;
            select_down2 = requested_down2;
            #1;
            if (select_ready) $fatal(1, "Stage switch unexpectedly ready: %0s", reason);
            @(negedge clk);
            select_valid = 1'b0;
            if (selected_down2 !== previous_owner)
                $fatal(1, "Stage owner changed on rejected request: %0s", reason);
        end
    endtask

    task reject_select_now;
        input requested_down2;
        input [319:0] reason;
        reg previous_owner;
        begin
            previous_owner = selected_down2;
            select_valid = 1'b1;
            select_down2 = requested_down2;
            #1;
            if (select_ready) $fatal(1, "Stage switch unexpectedly ready: %0s", reason);
            @(negedge clk);
            select_valid = 1'b0;
            if (selected_down2 !== previous_owner)
                $fatal(1, "Stage owner changed on rejected request: %0s", reason);
        end
    endtask

    task accept_select;
        input requested_down2;
        begin
            @(negedge clk);
            if (!select_ready) $fatal(1, "Stage switch not ready after drain");
            select_valid = 1'b1;
            select_down2 = requested_down2;
            @(negedge clk);
            select_valid = 1'b0;
            if (selected_down2 !== requested_down2) $fatal(1, "Stage switch not accepted");
        end
    endtask

    always @(negedge clk) begin
        if (force_output_stall) begin
            output_ready = 1'b0;
        end else if (mode == "stalls") begin
            random_bits = {random_bits[14:0],
                           random_bits[15] ^ random_bits[13] ^ random_bits[12] ^ random_bits[10]};
            commit_ready = random_bits[0] && (ticks % 521 >= 96);
            output_ready = random_bits[1] && (ticks % 293 >= 64);
        end else begin
            commit_ready = 1'b1;
            output_ready = 1'b1;
        end
    end

    always @(posedge clk) begin
        ticks = ticks + 1;
        if (ticks > 40000000)
            $fatal(1, "Full layer timeout down2=%0d stem=%0d state=%0d writes=%0d",
                   tile, st, dut.u_stem.state_current, stem_commits);
        if (rstn && (fault || table_fault)) $fatal(1, "Kernel fault tile=%0d", tile);
        if (rstn && done && select_ready) $fatal(1, "Stage switch ready while done is asserted");
        if (checking) begin
            if (held_commit && (!dut.d_pp_output_valid || dut.pp_tag !== previous_tag ||
                                dut.pp_data !== previous_commit_data))
                $fatal(1, "Commit not held");
            held_commit = dut.d_pp_output_valid && !commit_ready;
            previous_tag = dut.pp_tag;
            previous_commit_data = dut.pp_data;
            if (held_export && (!output_valid || output_index !== previous_index ||
                                output_data !== previous_export_data))
                $fatal(1, "Export not held");
            held_export = output_valid && !output_ready;
            previous_index = output_index;
            previous_export_data = output_data;
            if (busy) begin
                core_seen = core_seen + 1;
                if (dut.u_down2.flag_layer_pw) pw_cycles = pw_cycles + 1;
                else dw_cycles = dw_cycles + 1;
                if (dut.d_pp_output_valid && !commit_ready) category = 0;
                else if (((dut.u_down2.state_current == 4'd2) &&
                          dut.u_down2.cnt_mac_group == 0 && !dut.u_down2.flag_can_reserve) ||
                         (dut.u_down2.flag_pp_input_valid && !dut.d_pp_ready)) category = 1;
                else if (dut.u_down2.flag_commit_accept) category = 2;
                else if (dut.u_down2.flag_mac_input_accept) category = 3;
                else if (dut.u_down2.state_current == 4'd1 || dut.u_down2.state_current == 4'd2)
                    category = 4;
                else if (dut.u_down2.state_current == 4'd3 || dut.u_down2.state_current == 4'd9)
                    category = 5;
                else if (dut.u_down2.state_current == 4'd4 || dut.u_down2.state_current == 4'd5)
                    category = 6;
                else category = 7;
                bins[category] = bins[category] + 1;
            end
            if (dut.u_down2.flag_pp_input_accept) begin
                for (lane = 0; lane < 3; lane = lane + 1)
                    if (dut.u_down2.wire_result_lane_mask[lane]) begin
                        layer = dut.u_down2.flag_layer_pw;
                        position = dut.u_down2.wire_pp_position;
                        channel = dut.u_down2.wire_result_channel_base + lane;
                        local_index = layer ? 256 + position * 24 + channel :
                                              position * 16 + channel;
                        full_index = tile * 640 + local_index;
                        if ($signed(dut.u_down2.wire_pp_result_data[lane*32+:32]) !==
                            $signed(expected_acc[full_index]))
                            $fatal(1, "MAC mismatch tile=%0d local=%0d", tile, local_index);
                        acc_count = acc_count + 1;
                    end
            end
            if (dut.u_pp.flag_silu_accept) begin
                resolve_stage(dut.u_pp.pre_result_tag, index_stage);
                if ($signed(dut.u_pp.pre_result_data) !== $signed(expected_stages[index_stage*3]))
                    $fatal(1, "Pre mismatch index=%0d", index_stage);
                pre_count = pre_count + 1;
            end
            if (dut.u_pp.flag_post_accept) begin
                resolve_stage(dut.u_pp.reg_meta_tags[dut.u_pp.reg_meta_read], index_stage);
                if ($signed(dut.u_pp.silu_output_data) !== $signed(expected_stages[index_stage*3+1]))
                    $fatal(1, "SiLU mismatch index=%0d", index_stage);
                silu_count = silu_count + 1;
            end
            if (dut.u_pp.flag_post_complete) begin
                resolve_stage(dut.u_pp.post_result_tag, index_stage);
                if ($signed(dut.u_pp.post_result_data) !== $signed(expected_stages[index_stage*3+2]))
                    $fatal(1, "Post mismatch index=%0d", index_stage);
                post_count = post_count + 1;
            end
            if (dut.u_down2.flag_commit_accept) begin
                layer = dut.pp_tag[15];
                position = dut.pp_tag[14:11];
                channel = dut.pp_tag[10:6];
                if ((!layer && channel >= 16) || (layer && channel >= 24))
                    $fatal(1, "Invalid write channel");
                local_index = layer ? 256 + position * 24 + channel : position * 16 + channel;
                full_index = tile * 640 + local_index;
                if (seen_commit[full_index]) $fatal(1, "Duplicate write index=%0d", full_index);
                if ($signed(dut.pp_data) !== $signed(expected_stages[full_index*3+2]))
                    $fatal(1, "Write mismatch index=%0d", full_index);
                seen_commit[full_index] = 1'b1;
                if (layer) pw_commits = pw_commits + 1;
                else dw_commits = dw_commits + 1;
            end
            if (output_valid && output_ready) begin
                if (output_index !== exports || exports >= 384) $fatal(1, "Invalid export sequence");
                position = output_index / 24;
                channel = output_index % 24;
                gy = (tile / 32) * 4 + position / 4;
                gx = (tile % 32) * 4 + position % 4;
                full_index = ((gy / 4) * 32 + gx / 4) * 384 +
                             ((gy % 4) * 4 + gx % 4) * 24 + channel;
                if (full_index < 0 || full_index >= 221184 || seen_export[full_index])
                    $fatal(1, "Duplicate/out of range export");
                if (output_data !== expected_output[full_index])
                    $fatal(1, "Export mismatch address=%0d", full_index);
                actual_output[full_index] = output_data;
                seen_export[full_index] = 1'b1;
                exports = exports + 1;
            end
        end
    end

    task load_value;
        input [2:0] kind;
        input integer address;
        input [31:0] value;
        begin
            @(negedge clk);
            load_valid = 1'b1;
            load_kind = kind;
            load_addr = address;
            load_data = value;
            if (!load_ready) $fatal(1, "Load blocked tile=%0d address=%0d", tile, address);
        end
    endtask

    task load_shared_table;
        begin
            for (i = 0; i < 1023; i = i + 1) begin
                @(negedge clk);
                table_valid = 1'b1;
                table_addr = i;
                table_data = table_mem[i];
                if (!table_ready || table_loaded) $fatal(1, "Invalid partial table loading");
            end
            @(negedge clk); table_valid = 1'b0; stem_start = 1'b1;
            @(negedge clk); stem_start = 1'b0;
            if (busy || done) $fatal(1, "Partial table admitted start");
            @(negedge clk);
            table_valid = 1'b1;
            table_addr = 10'd1023;
            table_data = table_mem[1023];
            if (!table_ready || table_loaded) $fatal(1, "Invalid final table handshake");
            @(negedge clk); table_valid = 1'b0;
            if (!table_loaded) $fatal(1, "Shared table not complete");
        end
    endtask

    `include "shared_stem_driver.vh"

    initial begin
        if (!$value$plusargs("VECTORS=%s", vector_dir) ||
            !$value$plusargs("REPORT=%s", report_path) ||
            !$value$plusargs("DUMP=%s", dump_path)) $fatal(1, "Missing paths");
        if (!$value$plusargs("MODE=%s", mode)) mode = "normal";
        report = $fopen(report_path, "w");
        dump = $fopen(dump_path, "w");
        if (!report || !dump) $fatal(1, "Cannot open outputs");
        $fwrite(report, "tile,core,dw_core,pw_core,preload,export_cycles,dw_commits,pw_commits,exports,bin0,bin1,bin2,bin3,bin4,bin5,bin6,bin7\n");
        $sformat(file_path, "%0s/silu.hex", vector_dir); $readmemh(file_path, table_mem);
        $sformat(file_path, "%0s/input_tiled.hex", vector_dir); $readmemh(file_path, expected_stem);
        $sformat(file_path, "%0s/halos.hex", vector_dir); $readmemh(file_path, expected_halo);
        $sformat(file_path, "%0s/output_tiled.hex", vector_dir); $readmemh(file_path, expected_output);
        $sformat(file_path, "%0s/acc.hex", vector_dir); $readmemh(file_path, expected_acc);
        $sformat(file_path, "%0s/stages.hex", vector_dir); $readmemh(file_path, expected_stages);
        $sformat(file_path, "%0s/dw_weights.hex", vector_dir); $readmemh(file_path, dw_weight);
        $sformat(file_path, "%0s/dw_biases.hex", vector_dir); $readmemh(file_path, dw_bias);
        $sformat(file_path, "%0s/pw_weights.hex", vector_dir); $readmemh(file_path, pw_weight);
        $sformat(file_path, "%0s/pw_biases.hex", vector_dir); $readmemh(file_path, pw_bias);
        $sformat(file_path, "%0s/multipliers.hex", vector_dir); $readmemh(file_path, multipliers);
        $sformat(file_path, "%0s/controls.hex", vector_dir); $readmemh(file_path, controls);
        load_stem_vectors;
        for (i = 0; i < 368640; i = i + 1) seen_commit[i] = 1'b0;
        for (i = 0; i < 221184; i = i + 1) seen_export[i] = 1'b0;
        repeat (8) @(negedge clk);
        rstn = 1'b1;
        load_shared_table;
        run_stem;
        repeat (2) @(negedge clk);
        accept_select(1'b1);
        if (!table_loaded) $fatal(1, "Table lost across Stem/down2 switch");
        for (i = 0; i < 144; i = i + 1)
            load_value(3'd2, i, {{24{dw_weight[i][7]}}, dw_weight[i]});
        for (i = 0; i < 16; i = i + 1) load_value(3'd3, i, dw_bias[i]);
        for (i = 0; i < 384; i = i + 1)
            load_value(3'd4, i, {{24{pw_weight[i][7]}}, pw_weight[i]});
        for (i = 0; i < 24; i = i + 1) load_value(3'd5, i, pw_bias[i]);
        for (i = 0; i < 40; i = i + 1) load_value(3'd6, i, multipliers[i]);
        for (i = 0; i < 44; i = i + 1) load_value(3'd7, i, controls[i]);
        @(negedge clk); load_valid = 1'b0;
        for (tile = 0; tile < 576; tile = tile + 1) begin
            load_begin = preload_writes;
            for (j = 0; j < 1296; j = j + 1) begin
                hy = j / 144;
                hx = (j / 16) % 9;
                hc = j % 16;
                gy = (tile / 32) * 8 + hy - 1;
                gx = (tile % 32) * 8 + hx - 1;
                if (gy < 0 || gy >= 144 || gx < 0 || gx >= 256) begin
                    load_value(3'd0, j, 32'd0);
                    padding_count = padding_count + 1;
                end else begin
                    source_address = ((gy / 4) * 64 + gx / 4) * 256 +
                                     ((gy % 4) * 4 + gx % 4) * 16 + hc;
                    if (source_address < 0 || source_address >= 589824)
                        $fatal(1, "Invalid input address");
                    load_value(3'd0, j,
                               {{24{input_tensor[source_address][7]}}, input_tensor[source_address]});
                end
                if (load_data[7:0] !== expected_halo[tile*1296+j])
                    $fatal(1, "Halo/padding mismatch tile=%0d local=%0d", tile, j);
                if (j == 1294) begin
                    @(negedge clk); load_valid = 1'b0; start = 1'b1;
                    @(negedge clk); start = 1'b0;
                    if (busy) $fatal(1, "Partial halo started tile=%0d", tile);
                end
            end
            @(negedge clk); load_valid = 1'b0;
            if (preload_writes - load_begin != 1296) $fatal(1, "Incomplete halo writes");
            dw_commits = 0; pw_commits = 0; exports = 0; acc_count = 0;
            pre_count = 0; silu_count = 0; post_count = 0;
            core_seen = 0; dw_cycles = 0; pw_cycles = 0;
            for (i = 0; i < 8; i = i + 1) bins[i] = 0;
            checking = 1'b1;
            @(negedge clk); start = 1'b1;
            @(negedge clk); start = 1'b0;
            wait (done); @(negedge clk);
            if (acc_count != 640 || pre_count != 640 || silu_count != 640 ||
                post_count != 640 || dw_commits != 256 || pw_commits != 384)
                $fatal(1, "Missing intermediate values tile=%0d", tile);
            bin_sum = 0;
            for (i = 0; i < 8; i = i + 1) bin_sum = bin_sum + bins[i];
            if (bin_sum != core_cycles || core_seen != core_cycles ||
                dw_cycles + pw_cycles != core_cycles) $fatal(1, "Cycle bins do not close");
            if (mode == "normal" && core_cycles != 1687) $fatal(1, "Baseline cycles changed");
            export_start = 1'b1; @(negedge clk); export_start = 1'b0;
            wait (export_done); @(negedge clk);
            if (exports != 384) $fatal(1, "Missing exports");
            checking = 1'b0;
            $fwrite(report, "%0d,%0d,%0d,%0d,1296,%0d,%0d,%0d,%0d", tile, core_cycles,
                    dw_cycles, pw_cycles, export_cycles, dw_commits, pw_commits, exports);
            for (i = 0; i < 8; i = i + 1) $fwrite(report, ",%0d", bins[i]);
            $fwrite(report, "\n");
            if (tile % 64 == 63)
                $display("FULL_LAYER_PROGRESS mode=%0s completed=%0d/576", mode, tile+1);
        end
        for (i = 0; i < 368640; i = i + 1)
            if (!seen_commit[i]) $fatal(1, "Missing commit %0d", i);
        for (i = 0; i < 221184; i = i + 1) begin
            if (!seen_export[i]) $fatal(1, "Missing output address %0d", i);
            $fwrite(dump, "%02x\n", actual_output[i]);
        end
        if (preload_writes != 747148 || padding_count != 7184)
            $fatal(1, "Whole layer load/padding accounting");
        $fclose(report);
        $fclose(dump);
        $display("TB_PASS_FRONTEND_SHARED_CORE mode=%0s stem_tiles=2304 down2_tiles=576 dw_commits=147456 pw_commits=221184 exports=221184 shared_mac=1 shared_pp=1 table_loads=1 duplicates=0 holes=0 padding_bytes=%0d total_tb_ticks=%0d",
                 mode, padding_count, ticks);
        $finish;
    end
endmodule
