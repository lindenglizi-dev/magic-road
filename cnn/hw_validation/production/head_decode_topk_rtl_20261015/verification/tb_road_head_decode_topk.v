`timescale 1ns/1ps

// Self-checking endpoint and protocol verification for road_head_decode_topk.
module tb_road_head_decode_topk;

    localparam [31:0] MODEL_ID = 32'hB35D4A66, FRAME_TOKEN = 32'h10203040; // 固定模型和帧身份
    localparam [2:0] PHASE_FREE = 3'd0, PHASE_SCAN = 3'd1, PHASE_SORT = 3'd2; // 前三阶段编码
    localparam [2:0] PHASE_DECODE = 3'd3, PHASE_NMS = 3'd4; // 后两阶段编码

    reg i_clk, i_rstn, i_abort, i_start_valid, i_cell_valid; // 时钟复位和输入握手驱动
    reg i_lut_rsp_valid, i_lut_rsp_kind, i_lut_rsp_error; // 受控查表响应控制
    reg i_sealed_ready, i_read_req_valid, i_read_req_class; // 封存和读请求控制
    reg i_read_rsp_ready, i_finish_valid; // 读响应和结束控制
    reg [31:0] i_start_frame_token, i_start_model_id, i_cell_frame_token; // 输入身份字段
    reg [31:0] i_lut_rsp_frame_token, i_lut_rsp_model_id; // 查表响应身份字段
    reg [31:0] i_finish_frame_token; // 帧释放身份字段
    reg [111:0] i_cell_data; // 当前输入单元七字段
    reg [13:0] i_cell_id; // 全局单元序号
    reg [9:0] i_lut_rsp_address; // 查表响应地址回显
    reg [15:0] i_lut_rsp_tag, i_lut_rsp_data; // 查表响应标签和值
    reg [6:0] i_read_req_index; // 类内候选读取序号
    wire i_lut_req_ready; // 受控查表端点接收许可

    wire o_start_ready, o_cell_ready, o_lut_req_valid, o_lut_req_kind; // 启动、输入和查表请求控制
    wire o_lut_rsp_ready, o_lut_cancel, o_sealed_valid; // 查表响应与封存控制
    wire o_read_req_ready, o_read_rsp_valid, o_read_rsp_class; // 候选读取控制与类别回显
    wire o_read_rsp_error, o_finish_ready, o_fault; // 候选错误、释放和故障状态
    wire [9:0] o_lut_req_address; // 受控查表请求地址
    wire [15:0] o_lut_req_tag; // 受控查表请求标签
    wire [31:0] o_lut_req_frame_token, o_lut_req_model_id; // 查表请求身份字段
    wire [31:0] o_sealed_frame_token; // 封存帧身份
    wire [7:0] o_count_person, o_count_vehicle; // 两类封存候选数
    wire [6:0] o_read_rsp_index; // 候选响应序号
    wire [159:0] o_read_rsp_data; // 完整解码候选响应
    wire [3:0] o_error_code; // 首个故障原因编码
    wire [2:0] o_phase; // 当前互斥处理阶段
    wire [31:0] o_scan_cycles, o_sort_cycles, o_decode_cycles; // 三阶段周期计数
    wire [31:0] o_input_wait_cycles, o_lut_wait_cycles, o_ram_wait_cycles; // 三类等待计数
    wire [31:0] o_ram_read_words, o_ram_write_words; // 候选存储物理词计数

    reg [15:0] sigmoid_lut [0:1023]; // 共享整数参考导出的概率表
    reg [15:0] exp_lut [0:255]; // 共享整数参考导出的指数表
    reg [111:0] first_head, streamed_head; // 首项及流式输入单元
    reg [159:0] streamed_expected; // 当前期望解码记录
    integer head_handle, expected_handle, scan_result; // 向量文件句柄和读取状态

    reg [2047:0] head_file, expected_file; // 输入和期望文件路径
    reg [2047:0] sigmoid_file, exp_file; // 查表文件路径
    integer mode, expect_person, expect_vehicle, stall_mode; // 用例模式、计数和停顿选择
    integer max_cycles, fail_count, cycle_count; // 看门狗、失败和全局周期
    integer start_cycle, seal_cycle, phase_cycles [0:5], index; // 端点和阶段观测计数
    reg monitor_enable, profile_frozen; // 观测使能和首次封存冻结
    reg [31:0] seal_ram_read_words, seal_ram_write_words; // 首次封存RAM计数快照

    reg lut_pending, lut_pending_kind, lut_injection_used; // 查表未决状态和错误注入状态
    integer lut_delay, lut_inject; // 查表延迟和注入选择
    reg [9:0] lut_pending_address; // 未决查表地址
    reg [15:0] lut_pending_tag; // 未决查表标签
    reg [31:0] lut_pending_frame_token, lut_pending_model_id; // 未决查表身份

    reg prior_lut_wait, prior_lut_kind, prior_sealed_wait; // 上拍查表和封存等待状态
    reg prior_read_wait, prior_read_class, prior_read_error; // 上拍候选响应等待状态
    reg [9:0] prior_lut_address; // 上拍查表请求地址
    reg [15:0] prior_lut_tag; // 上拍查表请求标签
    reg [31:0] prior_lut_frame, prior_lut_model, prior_sealed_frame; // 上拍保持身份
    reg [7:0] prior_person_count, prior_vehicle_count; // 上拍封存计数
    reg [6:0] prior_read_index; // 上拍候选响应序号
    reg [159:0] prior_read_data; // 上拍候选响应载荷

    road_head_decode_topk dut ( // 被测解码与TopK端点
        .i_clk(i_clk),
        .i_rstn(i_rstn),
        .i_abort(i_abort),
        .i_start_valid(i_start_valid),
        .i_start_frame_token(i_start_frame_token),
        .i_start_model_id(i_start_model_id),
        .i_cell_valid(i_cell_valid),
        .i_cell_data(i_cell_data),
        .i_cell_id(i_cell_id),
        .i_cell_frame_token(i_cell_frame_token),
        .i_lut_req_ready(i_lut_req_ready),
        .i_lut_rsp_valid(i_lut_rsp_valid),
        .i_lut_rsp_kind(i_lut_rsp_kind),
        .i_lut_rsp_address(i_lut_rsp_address),
        .i_lut_rsp_tag(i_lut_rsp_tag),
        .i_lut_rsp_frame_token(i_lut_rsp_frame_token),
        .i_lut_rsp_model_id(i_lut_rsp_model_id),
        .i_lut_rsp_data(i_lut_rsp_data),
        .i_lut_rsp_error(i_lut_rsp_error),
        .i_sealed_ready(i_sealed_ready),
        .i_read_req_valid(i_read_req_valid),
        .i_read_req_class(i_read_req_class),
        .i_read_req_index(i_read_req_index),
        .i_read_rsp_ready(i_read_rsp_ready),
        .i_finish_valid(i_finish_valid),
        .i_finish_frame_token(i_finish_frame_token),
        .o_start_ready(o_start_ready),
        .o_cell_ready(o_cell_ready),
        .o_lut_req_valid(o_lut_req_valid),
        .o_lut_req_kind(o_lut_req_kind),
        .o_lut_req_address(o_lut_req_address),
        .o_lut_req_tag(o_lut_req_tag),
        .o_lut_req_frame_token(o_lut_req_frame_token),
        .o_lut_req_model_id(o_lut_req_model_id),
        .o_lut_rsp_ready(o_lut_rsp_ready),
        .o_lut_cancel(o_lut_cancel),
        .o_sealed_valid(o_sealed_valid),
        .o_sealed_frame_token(o_sealed_frame_token),
        .o_count_person(o_count_person),
        .o_count_vehicle(o_count_vehicle),
        .o_read_req_ready(o_read_req_ready),
        .o_read_rsp_valid(o_read_rsp_valid),
        .o_read_rsp_class(o_read_rsp_class),
        .o_read_rsp_index(o_read_rsp_index),
        .o_read_rsp_data(o_read_rsp_data),
        .o_read_rsp_error(o_read_rsp_error),
        .o_finish_ready(o_finish_ready),
        .o_fault(o_fault),
        .o_error_code(o_error_code),
        .o_phase(o_phase),
        .o_scan_cycles(o_scan_cycles),
        .o_sort_cycles(o_sort_cycles),
        .o_decode_cycles(o_decode_cycles),
        .o_input_wait_cycles(o_input_wait_cycles),
        .o_lut_wait_cycles(o_lut_wait_cycles),
        .o_ram_wait_cycles(o_ram_wait_cycles),
        .o_ram_read_words(o_ram_read_words),
        .o_ram_write_words(o_ram_write_words)
    );

    always #5 i_clk = ~i_clk; // 产生100MHz验证时钟

    // LUT服务只在空闲且非停顿拍接收一个请求。
    assign i_lut_req_ready = i_rstn && !i_abort && !lut_pending && // 仅空闲服务接收
                             !i_lut_rsp_valid &&
                             (!stall_mode || ((cycle_count % 11) != 0));

    // 任务：累计可定位的自检失败。
    task mark_error;
        input integer error_id; // 失败检查点编号
        begin
            fail_count = fail_count + 1;
            $display("TB_ERROR id=%0d cycle=%0d phase=%0d code=%0d", error_id,
                     cycle_count, o_phase, o_error_code);
        end
    endtask // 结束失败累计任务

    // 任务：将所有主动输入恢复为空闲值。
    task clear_inputs;
        begin
            i_abort = 1'b0;
            i_start_valid = 1'b0;
            i_start_frame_token = 32'd0;
            i_start_model_id = 32'd0;
            i_cell_valid = 1'b0;
            i_cell_data = 112'd0;
            i_cell_id = 14'd0;
            i_cell_frame_token = 32'd0;
            i_sealed_ready = 1'b0;
            i_read_req_valid = 1'b0;
            i_read_req_class = 1'b0;
            i_read_req_index = 7'd0;
            i_read_rsp_ready = 1'b0;
            i_finish_valid = 1'b0;
            i_finish_frame_token = 32'd0;
        end
    endtask // 结束输入清空任务

    // 任务：施加异步复位并检查无旧事务泄漏。
    task reset_dut;
        begin
            monitor_enable = 1'b0;
            profile_frozen = 1'b0;
            seal_ram_read_words = 0;
            seal_ram_write_words = 0;
            clear_inputs;
            i_rstn = 1'b0;
            repeat (4) @(posedge i_clk);
            @(negedge i_clk);
            i_rstn = 1'b1;
            repeat (3) @(posedge i_clk);
            if (o_phase !== PHASE_FREE || o_sealed_valid || o_read_rsp_valid ||
                o_lut_req_valid || o_fault) begin
                mark_error(100);
            end
            for (index = 0; index < 6; index = index + 1) begin
                phase_cycles[index] = 0;
            end
        end
    endtask // 结束复位检查任务

    // 任务：按握手启动指定模型帧。
    task start_frame;
        input [31:0] model_id; // 本次启动模型身份
        integer wait_cycles; // 启动等待看门狗
        begin
            wait_cycles = 0;
            @(negedge i_clk);
            i_start_frame_token = FRAME_TOKEN;
            i_start_model_id = model_id;
            i_start_valid = 1'b1;
            while (!o_start_ready && wait_cycles < 1000) begin
                @(posedge i_clk);
                wait_cycles = wait_cycles + 1;
            end
            if (!o_start_ready) begin
                mark_error(110);
            end
            else begin
                @(posedge i_clk);
                start_cycle = cycle_count;
            end
            @(negedge i_clk);
            i_start_valid = 1'b0;
        end
    endtask // 结束帧启动任务

    // 任务：保持单个输入单元直到被接收。
    task send_cell;
        input [13:0] cell_number; // 期望全局单元序号
        input [31:0] cell_token; // 单元所属帧身份
        input [111:0] cell_value; // 七项INT16输入载荷
        integer wait_cycles; // 输入等待看门狗
        begin
            wait_cycles = 0;
            @(negedge i_clk);
            i_cell_id = cell_number;
            i_cell_frame_token = cell_token;
            i_cell_data = cell_value;
            i_cell_valid = 1'b1;
            while (!o_cell_ready && wait_cycles < 100000) begin
                @(posedge i_clk);
                wait_cycles = wait_cycles + 1;
            end
            if (!o_cell_ready) begin
                mark_error(120);
            end
            else begin
                @(posedge i_clk);
            end
            @(negedge i_clk);
            i_cell_valid = 1'b0;
        end
    endtask // 结束单元发送任务

    // 任务：流式发送完整12096项保存向量。
    task send_all_cells;
        integer cell_number; // 当前全局单元序号
        begin
            head_handle = $fopen(head_file, "r");
            if (head_handle == 0) begin
                mark_error(122);
            end
            for (cell_number = 0; cell_number < 12096; cell_number = cell_number + 1) begin
                scan_result = $fscanf(head_handle, "%h\n", streamed_head);
                if (scan_result != 1) begin
                    mark_error(123);
                    cell_number = 12096;
                end
                if (stall_mode && (cell_number == 7 || (cell_number % 997) == 0)) begin
                    i_cell_valid = 1'b0;
                    repeat (cell_number == 7 ? 17 : 2) @(posedge i_clk);
                end
                if (cell_number < 12096) begin
                    send_cell(cell_number[13:0], FRAME_TOKEN, streamed_head);
                end
                if (o_fault && cell_number < 12096) begin
                    mark_error(121);
                    cell_number = 12096;
                end
            end
            if (head_handle != 0) begin
                $fclose(head_handle);
            end
        end
    endtask // 结束全帧发送任务

    // 任务：等待并核对首个故障编码。
    task wait_for_fault;
        input [3:0] expected_code; // 期望故障编码
        integer wait_cycles; // 故障等待看门狗
        begin
            wait_cycles = 0;
            while (!o_fault && wait_cycles < 100000) begin
                @(posedge i_clk);
                wait_cycles = wait_cycles + 1;
            end
            if (!o_fault || o_error_code !== expected_code) begin
                mark_error(130 + expected_code);
            end
            if (o_sealed_valid) begin
                mark_error(140 + expected_code);
            end
        end
    endtask // 结束故障等待任务

    // 任务：等待目标互斥处理阶段。
    task wait_for_phase;
        input [2:0] expected_phase; // 期望阶段编码
        integer wait_cycles; // 阶段等待看门狗
        begin
            wait_cycles = 0;
            while (o_phase !== expected_phase && !o_fault && wait_cycles < 2000000) begin
                @(posedge i_clk);
                wait_cycles = wait_cycles + 1;
            end
            if (o_phase !== expected_phase || o_fault) begin
                mark_error(150 + expected_phase);
            end
        end
    endtask // 结束阶段等待任务

    // 任务：对封存输出施加长反压后接收。
    task accept_seal;
        integer hold_cycles; // 封存等待看门狗
        begin
            hold_cycles = 0;
            i_sealed_ready = 1'b0;
            while (!o_sealed_valid && !o_fault && hold_cycles < 5000000) begin
                @(posedge i_clk);
                hold_cycles = hold_cycles + 1;
            end
            if (!o_sealed_valid || o_fault) begin
                mark_error(160);
            end
            else begin
                seal_cycle = cycle_count;
                seal_ram_read_words = o_ram_read_words;
                seal_ram_write_words = o_ram_write_words;
                if (o_sealed_frame_token !== FRAME_TOKEN ||
                    o_count_person !== expect_person[7:0] ||
                    o_count_vehicle !== expect_vehicle[7:0]) begin
                    mark_error(161);
                end
                repeat (13) @(posedge i_clk);
                @(negedge i_clk);
                i_sealed_ready = 1'b1;
                @(posedge i_clk);
                @(negedge i_clk);
                i_sealed_ready = 1'b0;
            end
        end
    endtask // 结束封存接收任务

    // 任务：发起一次候选读并逐位对拍响应。
    task read_record;
        input expected_class; // 期望响应类别
        input [6:0] expected_index; // 期望类内序号
        input [159:0] expected_data; // 期望完整解码记录
        integer wait_cycles; // 读事务等待看门狗
        begin
            wait_cycles = 0;
            @(negedge i_clk);
            i_read_req_class = expected_class;
            i_read_req_index = expected_index;
            i_read_req_valid = 1'b1;
            while (!o_read_req_ready && wait_cycles < 10000) begin
                @(posedge i_clk);
                wait_cycles = wait_cycles + 1;
            end
            if (!o_read_req_ready) begin
                mark_error(170);
            end
            else begin
                @(posedge i_clk);
            end
            @(negedge i_clk);
            i_read_req_valid = 1'b1;
            i_read_req_index = expected_index + 1'b1;
            @(posedge i_clk);
            if (o_read_req_ready) begin
                mark_error(171);
            end
            @(negedge i_clk);
            i_read_req_valid = 1'b0;

            wait_cycles = 0;
            while (!o_read_rsp_valid && !o_fault && wait_cycles < 10000) begin
                @(posedge i_clk);
                wait_cycles = wait_cycles + 1;
            end
            if (!o_read_rsp_valid || o_fault) begin
                mark_error(172);
            end
            else if (o_read_rsp_class !== expected_class ||
                     o_read_rsp_index !== expected_index ||
                     o_read_rsp_data !== expected_data || o_read_rsp_error) begin
                mark_error(173);
            end
            if (expected_index[2:0] == 3'd3) begin
                repeat (7) @(posedge i_clk);
            end
            @(negedge i_clk);
            i_read_rsp_ready = 1'b1;
            @(posedge i_clk);
            @(negedge i_clk);
            i_read_rsp_ready = 1'b0;
        end
    endtask // 结束单记录对拍任务

    // 任务：顺序读取两类所有封存候选。
    task read_all_records;
        integer record_number; // 当前类内记录序号
        begin
            expected_handle = $fopen(expected_file, "r");
            if ((expect_person + expect_vehicle) != 0 && expected_handle == 0) begin
                mark_error(174);
            end
            for (record_number = 0; record_number < expect_person; record_number = record_number + 1) begin
                scan_result = $fscanf(expected_handle, "%h\n", streamed_expected);
                if (scan_result != 1) begin
                    mark_error(175);
                end
                read_record(1'b0, record_number[6:0], streamed_expected);
            end
            for (record_number = 0; record_number < expect_vehicle; record_number = record_number + 1) begin
                scan_result = $fscanf(expected_handle, "%h\n", streamed_expected);
                if (scan_result != 1) begin
                    mark_error(176);
                end
                read_record(1'b1, record_number[6:0], streamed_expected);
            end
            if (expected_handle != 0) begin
                $fclose(expected_handle);
            end
        end
    endtask // 结束全记录对拍任务

    // 任务：按帧身份释放候选存储所有权。
    task finish_frame;
        input [31:0] finish_token; // 结束请求帧身份
        integer wait_cycles; // 结束握手等待看门狗
        begin
            wait_cycles = 0;
            @(negedge i_clk);
            i_finish_frame_token = finish_token;
            i_finish_valid = 1'b1;
            while (!o_finish_ready && !o_fault && wait_cycles < 10000) begin
                @(posedge i_clk);
                wait_cycles = wait_cycles + 1;
            end
            if (!o_finish_ready && !o_fault) begin
                mark_error(180);
            end
            else if (!o_fault) begin
                @(posedge i_clk);
            end
            @(negedge i_clk);
            i_finish_valid = 1'b0;
        end
    endtask // 结束帧释放任务

    // 任务：打印端点、阶段、等待和RAM实测计数。
    task print_metrics;
        begin
            $display("METRIC endpoint_start_to_seal=%0d observed_scan=%0d observed_sort=%0d observed_decode=%0d",
                     seal_cycle - start_cycle, phase_cycles[1], phase_cycles[2], phase_cycles[3]);
            $display("METRIC dut_scan=%0d dut_sort=%0d dut_decode=%0d input_wait=%0d lut_wait=%0d ram_wait=%0d ram_read_words=%0d ram_write_words=%0d",
                     o_scan_cycles, o_sort_cycles, o_decode_cycles,
                     o_input_wait_cycles, o_lut_wait_cycles, o_ram_wait_cycles,
                     o_ram_read_words, o_ram_write_words);
            $display("METRIC seal_ram_read_words=%0d seal_ram_write_words=%0d post_nms_ram_read_words=%0d",
                     seal_ram_read_words, seal_ram_write_words, o_ram_read_words);
        end
    endtask // 结束指标打印任务

    // 任务：执行一个完整保存向量回归。
    task run_normal;
        begin
            reset_dut;
            monitor_enable = 1'b1;
            start_frame(MODEL_ID);
            send_all_cells;
            accept_seal;
            read_all_records;
            print_metrics;
            finish_frame(FRAME_TOKEN);
            repeat (3) @(posedge i_clk);
            if (o_fault || o_phase !== PHASE_FREE) begin
                mark_error(190);
            end
        end
    endtask // 结束正常回归任务

    // 任务：验证越界NMS读进入READ_RANGE故障。
    task run_out_of_range;
        integer wait_cycles; // 越界请求等待看门狗
        begin
            reset_dut;
            monitor_enable = 1'b1;
            start_frame(MODEL_ID);
            send_all_cells;
            accept_seal;
            @(negedge i_clk);
            i_read_req_class = 1'b0;
            i_read_req_index = expect_person[6:0];
            i_read_req_valid = 1'b1;
            wait_cycles = 0;
            while (!o_read_req_ready && wait_cycles < 10000) begin
                @(posedge i_clk);
                wait_cycles = wait_cycles + 1;
            end
            @(posedge i_clk);
            @(negedge i_clk);
            i_read_req_valid = 1'b0;
            wait_for_fault(4'd5);
            if (o_read_rsp_valid && !o_read_rsp_error) begin
                mark_error(191);
            end
        end
    endtask // 结束越界读取任务

    // 任务：验证错误结束帧身份被拒绝。
    task run_wrong_finish;
        begin
            reset_dut;
            monitor_enable = 1'b1;
            start_frame(MODEL_ID);
            send_all_cells;
            accept_seal;
            finish_frame(FRAME_TOKEN ^ 32'd1);
            wait_for_fault(4'd6);
        end
    endtask // 结束错误释放任务

    // 任务：验证取消同时清除TB查表旧返回。
    task run_abort_lut;
        integer wait_cycles; // 查表未决等待看门狗
        begin
            reset_dut;
            stall_mode = 1;
            monitor_enable = 1'b1;
            start_frame(MODEL_ID);
            send_cell(14'd0, FRAME_TOKEN, first_head);
            wait_cycles = 0;
            while (!lut_pending && !i_lut_rsp_valid && wait_cycles < 1000) begin
                @(posedge i_clk);
                wait_cycles = wait_cycles + 1;
            end
            @(negedge i_clk);
            i_abort = 1'b1;
            @(posedge i_clk);
            if (!o_lut_cancel) begin
                mark_error(192);
            end
            @(posedge i_clk);
            @(negedge i_clk);
            i_abort = 1'b0;
            repeat (7) @(posedge i_clk);
            if (lut_pending || i_lut_rsp_valid || o_lut_req_valid ||
                o_sealed_valid || o_read_rsp_valid || o_phase !== PHASE_FREE) begin
                mark_error(193);
            end
        end
    endtask // 结束查表取消任务

    // 任务：执行身份、错误、取消和越界协议回归。
    task run_protocol;
        integer injection_number; // 当前查表错误注入类别
        begin
            lut_inject = 0;
            reset_dut;
            monitor_enable = 1'b1;
            start_frame(32'hDEADBEEF);
            wait_for_fault(4'd1);

            reset_dut;
            monitor_enable = 1'b1;
            start_frame(MODEL_ID);
            send_cell(14'd1, FRAME_TOKEN, first_head);
            wait_for_fault(4'd2);

            reset_dut;
            monitor_enable = 1'b1;
            start_frame(MODEL_ID);
            send_cell(14'd0, FRAME_TOKEN ^ 32'd1, first_head);
            wait_for_fault(4'd2);

            for (injection_number = 1; injection_number <= 6; injection_number = injection_number + 1) begin
                lut_inject = injection_number;
                reset_dut;
                monitor_enable = 1'b1;
                start_frame(MODEL_ID);
                send_cell(14'd0, FRAME_TOKEN, first_head);
                wait_for_fault(4'd3);
            end
            lut_inject = 0;
            run_out_of_range;
            run_wrong_finish;
            run_abort_lut;
        end
    endtask // 结束协议回归任务

    // 任务：在指定阶段异步复位并检查清空。
    task reset_during_phase;
        input [2:0] target_phase; // 复位注入阶段
        begin
            reset_dut;
            monitor_enable = 1'b1;
            start_frame(MODEL_ID);
            if (target_phase == PHASE_SCAN) begin
                wait_for_phase(PHASE_SCAN);
                send_cell(14'd0, FRAME_TOKEN, first_head);
            end
            else begin
                send_all_cells;
                wait_for_phase(target_phase);
            end
            @(negedge i_clk);
            i_rstn = 1'b0;
            repeat (3) @(posedge i_clk);
            if (lut_pending || i_lut_rsp_valid) begin
                mark_error(200 + target_phase);
            end
            @(negedge i_clk);
            i_rstn = 1'b1;
            repeat (4) @(posedge i_clk);
            if (o_phase !== PHASE_FREE || o_fault || o_sealed_valid ||
                o_read_rsp_valid || o_lut_req_valid) begin
                mark_error(210 + target_phase);
            end
        end
    endtask // 结束单阶段复位任务

    // 任务：依次覆盖SCAN、SORT和DECODE复位。
    task run_phase_resets;
        begin
            lut_inject = 0;
            reset_during_phase(PHASE_SCAN);
            reset_during_phase(PHASE_SORT);
            reset_during_phase(PHASE_DECODE);
        end
    endtask // 结束三阶段复位任务

    always @(posedge i_clk or negedge i_rstn) begin // 受控LUT单未决服务与错误注入
        if (!i_rstn || i_abort) begin
            lut_pending <= 1'b0;
            lut_delay <= 0;
            i_lut_rsp_valid <= 1'b0;
            i_lut_rsp_kind <= 1'b0;
            i_lut_rsp_address <= 10'd0;
            i_lut_rsp_tag <= 16'd0;
            i_lut_rsp_frame_token <= 32'd0;
            i_lut_rsp_model_id <= 32'd0;
            i_lut_rsp_data <= 16'd0;
            i_lut_rsp_error <= 1'b0;
            lut_injection_used <= 1'b0;
        end
        else begin
            if (i_lut_rsp_valid && o_lut_rsp_ready) begin
                i_lut_rsp_valid <= 1'b0;
            end
            if (o_lut_req_valid && i_lut_req_ready) begin
                lut_pending <= 1'b1;
                lut_delay <= stall_mode ? (5 + (o_lut_req_tag % 13)) : 1;
                lut_pending_kind <= o_lut_req_kind;
                lut_pending_address <= o_lut_req_address;
                lut_pending_tag <= o_lut_req_tag;
                lut_pending_frame_token <= o_lut_req_frame_token;
                lut_pending_model_id <= o_lut_req_model_id;
            end
            else if (lut_pending && lut_delay != 0) begin
                lut_delay <= lut_delay - 1;
            end
            else if (lut_pending && !i_lut_rsp_valid) begin
                lut_pending <= 1'b0;
                i_lut_rsp_valid <= 1'b1;
                i_lut_rsp_kind <= lut_pending_kind;
                i_lut_rsp_address <= lut_pending_address;
                i_lut_rsp_tag <= lut_pending_tag;
                i_lut_rsp_frame_token <= lut_pending_frame_token;
                i_lut_rsp_model_id <= lut_pending_model_id;
                i_lut_rsp_error <= lut_pending_kind && (lut_pending_address > 10'd255);
                if (lut_pending_kind) begin
                    i_lut_rsp_data <= exp_lut[lut_pending_address[7:0]];
                end
                else begin
                    i_lut_rsp_data <= sigmoid_lut[lut_pending_address];
                end
                if (!lut_injection_used && lut_inject != 0) begin
                    lut_injection_used <= 1'b1;
                    case (lut_inject)
                        1: i_lut_rsp_kind <= ~lut_pending_kind;
                        2: i_lut_rsp_address <= lut_pending_address + 1'b1;
                        3: i_lut_rsp_tag <= lut_pending_tag + 1'b1;
                        4: i_lut_rsp_frame_token <= lut_pending_frame_token ^ 32'd1;
                        5: i_lut_rsp_model_id <= lut_pending_model_id ^ 32'd1;
                        6: i_lut_rsp_error <= 1'b1;
                        default: i_lut_rsp_error <= i_lut_rsp_error;
                    endcase
                end
            end
        end
    end

    always @(posedge i_clk) begin // 看门狗、阶段计数和反压稳定性断言
        cycle_count = cycle_count + 1;
        if (cycle_count > max_cycles) begin
            mark_error(900);
            $display("TB_FAIL failures=%0d", fail_count);
            $finish;
        end
        if (!i_rstn || i_abort) begin
            prior_lut_wait <= 1'b0;
            prior_sealed_wait <= 1'b0;
            prior_read_wait <= 1'b0;
        end
        else begin
            if (monitor_enable && !profile_frozen && !o_sealed_valid) begin
                if ((^o_phase) === 1'bx || o_phase > 3'd5) begin
                    mark_error(300);
                end
                else begin
                    phase_cycles[o_phase] = phase_cycles[o_phase] + 1;
                end
            end
            if (monitor_enable && o_sealed_valid) begin
                profile_frozen <= 1'b1;
            end
            if (prior_lut_wait && (!o_lut_req_valid ||
                o_lut_req_kind !== prior_lut_kind ||
                o_lut_req_address !== prior_lut_address ||
                o_lut_req_tag !== prior_lut_tag ||
                o_lut_req_frame_token !== prior_lut_frame ||
                o_lut_req_model_id !== prior_lut_model)) begin
                mark_error(301);
            end
            if (prior_sealed_wait && (!o_sealed_valid ||
                o_sealed_frame_token !== prior_sealed_frame ||
                o_count_person !== prior_person_count ||
                o_count_vehicle !== prior_vehicle_count)) begin
                mark_error(302);
            end
            if (prior_read_wait && (!o_read_rsp_valid ||
                o_read_rsp_class !== prior_read_class ||
                o_read_rsp_index !== prior_read_index ||
                o_read_rsp_data !== prior_read_data ||
                o_read_rsp_error !== prior_read_error)) begin
                mark_error(303);
            end
            prior_lut_wait <= o_lut_req_valid && !i_lut_req_ready;
            prior_lut_kind <= o_lut_req_kind;
            prior_lut_address <= o_lut_req_address;
            prior_lut_tag <= o_lut_req_tag;
            prior_lut_frame <= o_lut_req_frame_token;
            prior_lut_model <= o_lut_req_model_id;
            prior_sealed_wait <= o_sealed_valid && !i_sealed_ready;
            prior_sealed_frame <= o_sealed_frame_token;
            prior_person_count <= o_count_person;
            prior_vehicle_count <= o_count_vehicle;
            prior_read_wait <= o_read_rsp_valid && !i_read_rsp_ready;
            prior_read_class <= o_read_rsp_class;
            prior_read_index <= o_read_rsp_index;
            prior_read_data <= o_read_rsp_data;
            prior_read_error <= o_read_rsp_error;
        end
    end

    initial begin // 读取加号参数并选择回归套件
        i_clk = 1'b0;
        i_rstn = 1'b0;
        monitor_enable = 1'b0;
        profile_frozen = 1'b0;
        seal_ram_read_words = 0;
        seal_ram_write_words = 0;
        fail_count = 0;
        cycle_count = 0;
        start_cycle = 0;
        seal_cycle = 0;
        lut_inject = 0;
        stall_mode = 0;
        mode = 0;
        expect_person = 0;
        expect_vehicle = 0;
        max_cycles = 20000000;
        clear_inputs;
        for (index = 0; index < 6; index = index + 1) begin
            phase_cycles[index] = 0;
        end
        if (!$value$plusargs("MODE=%d", mode) ||
            !$value$plusargs("HEAD=%s", head_file) ||
            !$value$plusargs("EXPECTED=%s", expected_file) ||
            !$value$plusargs("EXPECT_PERSON=%d", expect_person) ||
            !$value$plusargs("EXPECT_VEHICLE=%d", expect_vehicle) ||
            !$value$plusargs("SIGMOID=%s", sigmoid_file) ||
            !$value$plusargs("EXP=%s", exp_file)) begin
            mark_error(901);
            $display("TB_FAIL missing plusargs");
            $finish;
        end
        if (!$value$plusargs("STALL=%d", stall_mode)) begin
            stall_mode = 0;
        end
        if (!$value$plusargs("MAX_CYCLES=%d", max_cycles)) begin
            max_cycles = 20000000;
        end
        head_handle = $fopen(head_file, "r");
        if (head_handle == 0) begin
            mark_error(903);
        end
        else begin
            scan_result = $fscanf(head_handle, "%h\n", first_head);
            if (scan_result != 1) begin
                mark_error(904);
            end
            $fclose(head_handle);
        end
        $readmemh(sigmoid_file, sigmoid_lut);
        $readmemh(exp_file, exp_lut);

        if (mode == 0) begin
            run_normal;
        end
        else if (mode == 1) begin
            run_protocol;
        end
        else if (mode == 2) begin
            run_phase_resets;
        end
        else begin
            mark_error(902);
        end

        monitor_enable = 1'b0;
        if (fail_count == 0) begin
            $display("TB_PASS mode=%0d cycles=%0d", mode, cycle_count);
        end
        else begin
            $display("TB_FAIL failures=%0d mode=%0d", fail_count, mode);
        end
        $finish;
    end

endmodule
