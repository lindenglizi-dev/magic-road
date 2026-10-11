`timescale 1ns / 1ps

// 完整层验证环境：外部 testbench 负责 tile 顺序，不冒充硬件 DDR 控制器。
module tb_down2_full_tensor();
    reg clk = 1'b0; // 仿真时钟初值。
    always #5 clk = ~clk; // 100 MHz，周期统计不含板级时钟误差。
    reg rstn = 1'b0; // 低有效复位，运行前清空核有效状态。
    reg table_valid = 1'b0, load_valid = 1'b0, start = 1'b0; // 表、存储和任务入口控制。
    reg commit_ready = 1'b1, output_ready = 1'b1, export_start = 1'b0; // 写回与导出独立反压。
    reg [9:0] table_addr = 10'd0; // 顺序装载的 SiLU 地址。
    reg signed [15:0] table_data = 16'sd0; // Q7.8 查表值。
    reg [2:0] load_kind = 3'd0; // 冻结核的存储种类编码。
    reg [10:0] load_addr = 11'd0; // 当前种类内的元素偏移。
    reg signed [31:0] load_data = 32'sd0; // 字节符号扩展或完整量化参数。
    wire table_ready, table_loaded, table_fault, load_ready, busy, done, fault; // 原核握手及故障观察。
    wire output_valid, export_done; // 缓存导出握手及末项完成。
    wire signed [7:0] output_data; // 实际缓存读口输出，不能用内部比较值代替。
    wire [8:0] output_index; // 当前 tile 内的 0 至 383 偏移。
    wire [31:0] core_cycles, export_cycles, preload_writes; // 原核的三个独立计数窗口。
    reg [15:0] table_mem [0:1023]; // 完整 SiLU 测试表。
    reg [7:0] input_tensor [0:589823], expected_halo [0:746495]; // 分块输入及独立 Python halo。
    reg [7:0] dw_weight [0:143], pw_weight [0:383], expected_output [0:221183]; // OIHW 权重及完整输出黄金值。
    reg [31:0] dw_bias [0:15], pw_bias [0:23], multipliers [0:39], controls [0:43]; // 测试偏置和动态系数，不是模型参数。
    reg [31:0] expected_acc [0:368639], expected_stages [0:1105919]; // 每个 DW/PW 标量的累加及三个量化阶段。
    reg [7:0] actual_output [0:221183]; // 由真实导出握手写入，最终完整落盘。
    reg seen_commit [0:368639], seen_export [0:221183]; // 每地址一次性记分牌，用于查重及漏写。
    reg checking = 1'b0, held_commit = 1'b0, held_export = 1'b0; // 比较许可及上拍反压状态。
    reg [15:0] previous_tag; // 写回反压期间的身份快照。
    reg [8:0] previous_index; // 导出反压期间的地址快照。
    reg [7:0] previous_commit_data, previous_export_data; // 两个通路分别保持数据。
    reg [15:0] random_bits = 16'hace1; // 可复现气泡序列。
    reg [4095:0] vector_dir, report_path, dump_path, file_path; // 调用者显式传入的独立输出路径。
    reg [127:0] mode; // 无停顿或反压模式。
    integer ticks = 0, tile = 0, report, dump; // 全局超时、tile 身份及两个文件句柄。
    integer i, j, hy, hx, hc, gy, gx, source_address, padding_count = 0; // 装载循环及全图坐标。
    integer lane, layer, position, channel, local_index, full_index, index_stage; // 实际退休结果的地址解析。
    integer dw_commits, pw_commits, exports, acc_count, pre_count, silu_count, post_count; // 各阶段逐项计数。
    integer bins [0:7]; // 按优先级互斥归类的核心周期。
    integer category, bin_sum, core_seen, dw_cycles, pw_cycles, load_begin; // 周期闭合及本 tile 装载计数起点。

    down2_dynamic_tile_runner dut ( // 直接实例化冻结计算链，不覆写内部存储。
        .i_clk(clk), .i_rstn(rstn), .i_table_valid(table_valid), .i_table_addr(table_addr),
        .i_table_data(table_data), .o_table_ready(table_ready), .o_table_loaded(table_loaded),
        .o_table_fault(table_fault), .i_load_valid(load_valid), .i_load_kind(load_kind),
        .i_load_addr(load_addr), .i_load_data(load_data), .o_load_ready(load_ready),
        .i_start(start), .i_pw_only(1'b0), .i_commit_ready(commit_ready),
        .o_busy(busy), .o_done(done), .o_fault(fault), .i_export_start(export_start),
        .i_output_ready(output_ready), .o_output_valid(output_valid), .o_output_data(output_data),
        .o_output_index(output_index), .o_export_done(export_done), .o_core_cycles(core_cycles),
        .o_export_cycles(export_cycles), .o_preload_writes(preload_writes), // 核侧计数与 testbench 观察值交叉核对。
        .o_debug_valid(), .o_debug_phase(), .o_debug_layer(), .o_debug_position(),
        .o_debug_channel(), .o_debug_value(), .o_mac_cycles(), .o_pre_cycles(),
        .o_silu_cycles(), .o_post_cycles(), .o_writeback_cycles(), .o_storage_wait_cycles(),
        .o_scheduler_idle_cycles(), .o_result_queue_count(), .o_result_reserved(), .o_meta_count(),
        .o_mac_result_count(), .o_pre_accept_count(), .o_silu_accept_count(), .o_post_accept_count(), .o_writeback_count()
    );

    // 内部 tag 仅作验证观察，解析真实退休记录，不依赖发射计数器。
    // 用环形退休记录还原完整层地址。
    task resolve_stage; // 按实际退休槽取得当前标量身份。
        input [15:0] internal_tag; // 后处理流水携带的在途槽号。
        output integer resolved; // 当前 tile 在全层参考中的标量地址。
        reg [47:0] tags; // 三路外部身份记录。
        reg [15:0] external_tag; // 当前 lane 的层、位置和通道。
        integer slot, tag_lane, tag_layer, tag_position, tag_channel; // 显式拆分，避免使用当前发射身份。
        begin
            if (internal_tag[15:5] !== 11'd0 || internal_tag[1:0] > 2)
                $fatal(1, "Invalid stage tag tile=%0d", tile);
            slot = internal_tag[4:2]; tag_lane = internal_tag[1:0];
            tags = dut.road_postprocess_stream_Inst_tile.u_chain.reg_retire_tags[slot];
            external_tag = tags >> (tag_lane * 16);
            tag_layer = external_tag[15]; tag_position = external_tag[14:11];
            tag_channel = external_tag[10:6];
            if ((!tag_layer && tag_channel >= 16) || (tag_layer && tag_channel >= 24))
                $fatal(1, "Invalid stage channel");
            resolved = tile * 640 + (tag_layer ? 256 + tag_position * 24 + tag_channel :
                                                               tag_position * 16 + tag_channel);
        end
    endtask

    // 输出和写回两端独立制造气泡及 96 拍长反压。
    always @(negedge clk) begin
        if (mode == "stalls") begin
            random_bits = {random_bits[14:0], random_bits[15] ^ random_bits[13] ^ random_bits[12] ^ random_bits[10]};
            commit_ready = random_bits[0] && (ticks % 521 >= 96);
            output_ready = random_bits[1] && (ticks % 293 >= 64);
        end else begin
            commit_ready = 1'b1; output_ready = 1'b1;
        end
    end

    always @(posedge clk) begin // 只在握手被接受时比较和更新地址覆盖。
        ticks = ticks + 1;
        if (ticks > 5000000) $fatal(1, "Full layer timeout tile=%0d", tile);
        if (rstn && (fault || table_fault)) $fatal(1, "Kernel fault tile=%0d", tile);
        if (checking) begin
            if (held_commit && (!dut.pp_output_valid || dut.pp_output_tag !== previous_tag ||
                                dut.pp_output_data !== previous_commit_data)) $fatal(1, "Commit not held");
            held_commit = dut.pp_output_valid && !commit_ready;
            previous_tag = dut.pp_output_tag; previous_commit_data = dut.pp_output_data;
            if (held_export && (!output_valid || output_index !== previous_index ||
                               output_data !== previous_export_data)) $fatal(1, "Export not held");
            held_export = output_valid && !output_ready;
            previous_index = output_index; previous_export_data = output_data;
            if (busy) begin
                core_seen = core_seen + 1;
                if (dut.flag_layer_pw) pw_cycles = pw_cycles + 1; else dw_cycles = dw_cycles + 1;
                if (dut.pp_output_valid && !commit_ready) category = 0;
                else if (((dut.state_current == 4'd2) && dut.cnt_mac_group == 0 && !dut.flag_can_reserve) ||
                         (dut.flag_pp_input_valid && !dut.pp_input_ready)) category = 1;
                else if (dut.flag_commit_accept) category = 2;
                else if (dut.flag_mac_input_accept) category = 3;
                else if (dut.state_current == 4'd1 || dut.state_current == 4'd2) category = 4;
                else if (dut.state_current == 4'd3 || dut.state_current == 4'd9) category = 5;
                else if (dut.state_current == 4'd4 || dut.state_current == 4'd5) category = 6;
                else category = 7;
                bins[category] = bins[category] + 1;
            end
            if (dut.flag_pp_input_accept) begin
                for (lane = 0; lane < 3; lane = lane + 1) if (dut.wire_result_lane_mask[lane]) begin
                    layer = dut.flag_layer_pw; position = dut.wire_pp_position;
                    channel = dut.wire_result_channel_base + lane;
                    local_index = layer ? 256 + position * 24 + channel : position * 16 + channel;
                    full_index = tile * 640 + local_index;
                    if ($signed(dut.wire_pp_result_data[lane*32+:32]) !== $signed(expected_acc[full_index]))
                        $fatal(1, "MAC mismatch tile=%0d local=%0d", tile, local_index);
                    acc_count = acc_count + 1;
                end
            end
            if (dut.road_postprocess_stream_Inst_tile.u_chain.flag_silu_accept) begin
                resolve_stage(dut.road_postprocess_stream_Inst_tile.u_chain.pre_result_tag, index_stage);
                if ($signed(dut.road_postprocess_stream_Inst_tile.u_chain.pre_result_data) !==
                    $signed(expected_stages[index_stage*3])) $fatal(1, "Pre mismatch index=%0d", index_stage);
                pre_count = pre_count + 1;
            end
            if (dut.road_postprocess_stream_Inst_tile.u_chain.flag_post_accept) begin
                resolve_stage(dut.road_postprocess_stream_Inst_tile.u_chain.reg_meta_tags[
                              dut.road_postprocess_stream_Inst_tile.u_chain.reg_meta_read], index_stage);
                if ($signed(dut.road_postprocess_stream_Inst_tile.u_chain.silu_output_data) !==
                    $signed(expected_stages[index_stage*3+1])) $fatal(1, "SiLU mismatch index=%0d", index_stage);
                silu_count = silu_count + 1;
            end
            if (dut.road_postprocess_stream_Inst_tile.u_chain.flag_post_complete) begin
                resolve_stage(dut.road_postprocess_stream_Inst_tile.u_chain.post_result_tag, index_stage);
                if ($signed(dut.road_postprocess_stream_Inst_tile.u_chain.post_result_data) !==
                    $signed(expected_stages[index_stage*3+2])) $fatal(1, "Post mismatch index=%0d", index_stage);
                post_count = post_count + 1;
            end
            if (dut.flag_commit_accept) begin
                layer = dut.pp_output_tag[15]; position = dut.pp_output_tag[14:11];
                channel = dut.pp_output_tag[10:6];
                if ((!layer && channel >= 16) || (layer && channel >= 24)) $fatal(1, "Invalid write channel");
                local_index = layer ? 256 + position * 24 + channel : position * 16 + channel;
                full_index = tile * 640 + local_index;
                if (seen_commit[full_index]) $fatal(1, "Duplicate write index=%0d", full_index);
                if ($signed(dut.pp_output_data) !== $signed(expected_stages[full_index*3+2]))
                    $fatal(1, "Write mismatch index=%0d", full_index);
                seen_commit[full_index] = 1'b1;
                if (layer) pw_commits = pw_commits + 1; else dw_commits = dw_commits + 1;
            end
            if (output_valid && output_ready) begin
                if (output_index !== exports || exports >= 384) $fatal(1, "Invalid export sequence");
                // 从全图坐标推导目的布局，与参考 reshape 独立。
                position = output_index / 24; channel = output_index % 24;
                gy = (tile / 32) * 4 + position / 4;
                gx = (tile % 32) * 4 + position % 4;
                full_index = ((gy / 4) * 32 + gx / 4) * 384 + ((gy % 4) * 4 + gx % 4) * 24 + channel;
                if (full_index < 0 || full_index >= 221184 || seen_export[full_index]) $fatal(1, "Duplicate/out of range export");
                if (output_data !== expected_output[full_index]) $fatal(1, "Export mismatch address=%0d", full_index);
                actual_output[full_index] = output_data;
                seen_export[full_index] = 1'b1;
                exports = exports + 1;
            end
        end
    end

    // 在下降沿准备，下一上升沿完成真实装载握手。
    task load_value; // 原装载口的一个顺序元素传输。
        input [2:0] kind; // 保持冻结种类编码。
        input integer address; // 当前种类内连续地址。
        input [31:0] value; // 完整输入值，字节由调用点显式符号扩展。
        begin
            @(negedge clk); load_valid = 1'b1; load_kind = kind;
            load_addr = address; load_data = value;
            if (!load_ready) $fatal(1, "Load blocked tile=%0d address=%0d", tile, address);
        end
    endtask

    initial begin // 先装一次参数和表，再连续执行全部 576 个 tile。
        if (!$value$plusargs("VECTORS=%s", vector_dir) || !$value$plusargs("REPORT=%s", report_path) ||
            !$value$plusargs("DUMP=%s", dump_path)) $fatal(1, "Missing paths");
        if (!$value$plusargs("MODE=%s", mode)) mode = "normal";
        report = $fopen(report_path, "w"); dump = $fopen(dump_path, "w");
        if (!report || !dump) $fatal(1, "Cannot open outputs");
        $fwrite(report, "tile,core,dw_core,pw_core,preload,export_cycles,dw_commits,pw_commits,exports,bin0,bin1,bin2,bin3,bin4,bin5,bin6,bin7\n");
        $sformat(file_path, "%0s/silu.hex", vector_dir); $readmemh(file_path, table_mem);
        $sformat(file_path, "%0s/input_tiled.hex", vector_dir); $readmemh(file_path, input_tensor);
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
        for (i = 0; i < 368640; i = i + 1) seen_commit[i] = 1'b0;
        for (i = 0; i < 221184; i = i + 1) seen_export[i] = 1'b0;
        repeat (8) @(negedge clk); rstn = 1'b1;
        for (i = 0; i < 1024; i = i + 1) begin
            @(negedge clk); table_valid = 1'b1; table_addr = i; table_data = table_mem[i];
            if (!table_ready || (i < 1023 && table_loaded)) $fatal(1, "Invalid table loading");
        end
        @(negedge clk); table_valid = 1'b0;
        if (!table_loaded) $fatal(1, "Table not complete");
        for (i = 0; i < 144; i = i + 1) load_value(3'd2, i, {{24{dw_weight[i][7]}}, dw_weight[i]});
        for (i = 0; i < 16; i = i + 1) load_value(3'd3, i, dw_bias[i]);
        for (i = 0; i < 384; i = i + 1) load_value(3'd4, i, {{24{pw_weight[i][7]}}, pw_weight[i]});
        for (i = 0; i < 24; i = i + 1) load_value(3'd5, i, pw_bias[i]);
        for (i = 0; i < 40; i = i + 1) load_value(3'd6, i, multipliers[i]);
        for (i = 0; i < 44; i = i + 1) load_value(3'd7, i, controls[i]);
        @(negedge clk); load_valid = 1'b0;
        for (tile = 0; tile < 576; tile = tile + 1) begin
            load_begin = preload_writes;
            for (j = 0; j < 1296; j = j + 1) begin
                hy = j / 144; hx = (j / 16) % 9; hc = j % 16;
                gy = (tile / 32) * 8 + hy - 1; gx = (tile % 32) * 8 + hx - 1;
                if (gy < 0 || gy >= 144 || gx < 0 || gx >= 256) begin
                    load_value(3'd0, j, 32'd0); padding_count = padding_count + 1;
                end else begin
                    source_address = ((gy / 4) * 64 + gx / 4) * 256 + ((gy % 4) * 4 + gx % 4) * 16 + hc;
                    if (source_address < 0 || source_address >= 589824) $fatal(1, "Invalid input address");
                    load_value(3'd0, j, {{24{input_tensor[source_address][7]}}, input_tensor[source_address]});
                end
                if (load_data[7:0] !== expected_halo[tile*1296+j]) $fatal(1, "Halo/padding mismatch tile=%0d local=%0d", tile, j);
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
            @(negedge clk); start = 1'b1; @(negedge clk); start = 1'b0;
            wait (done); @(negedge clk);
            if (acc_count != 640 || pre_count != 640 || silu_count != 640 || post_count != 640 ||
                dw_commits != 256 || pw_commits != 384) $fatal(1, "Missing intermediate values tile=%0d", tile);
            bin_sum = 0; for (i = 0; i < 8; i = i + 1) bin_sum = bin_sum + bins[i];
            if (bin_sum != core_cycles || core_seen != core_cycles || dw_cycles + pw_cycles != core_cycles)
                $fatal(1, "Cycle bins do not close");
            if (mode == "normal" && core_cycles != 1687) $fatal(1, "Baseline cycles changed");
            export_start = 1'b1; @(negedge clk); export_start = 1'b0;
            wait (export_done); @(negedge clk);
            if (exports != 384) $fatal(1, "Missing exports");
            checking = 1'b0;
            $fwrite(report, "%0d,%0d,%0d,%0d,1296,%0d,%0d,%0d,%0d", tile, core_cycles, dw_cycles, pw_cycles,
                    export_cycles, dw_commits, pw_commits, exports);
            for (i = 0; i < 8; i = i + 1) $fwrite(report, ",%0d", bins[i]);
            $fwrite(report, "\n");
            if (tile % 64 == 63) $display("FULL_LAYER_PROGRESS mode=%0s completed=%0d/576", mode, tile+1);
        end
        for (i = 0; i < 368640; i = i + 1) if (!seen_commit[i]) $fatal(1, "Missing commit %0d", i);
        for (i = 0; i < 221184; i = i + 1) begin
            if (!seen_export[i]) $fatal(1, "Missing output address %0d", i);
            $fwrite(dump, "%02x\n", actual_output[i]);
        end
        if (preload_writes != 747148 || padding_count != 7184) $fatal(1, "Whole layer load/padding accounting");
        $fclose(report); $fclose(dump);
        $display("TB_PASS_DOWN2_FULL_TENSOR mode=%0s tiles=576 dw_commits=147456 pw_commits=221184 exports=221184 duplicates=0 holes=0 padding_bytes=%0d total_tb_ticks=%0d", mode, padding_count, ticks);
        $finish;
    end
endmodule
