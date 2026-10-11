`timescale 1ns / 1ps

// 固定三套DW/PW测试的发送、状态轮询和逐字比较；不提供外部脚本接口。
module road_board_selftest_player (
    input i_clk,                         // 计算时钟100MHz
    input i_rstn,                        // 顶层已同步释放的低有效复位
    input i_rx_ready,                    // 原壳接收许可
    input i_tx_valid,                    // 原壳响应有效
    input [15:0] i_tx_data,               // 原壳响应字
    output o_rx_valid,                   // 固定命令有效，阻塞保持
    output [15:0] o_rx_data,              // 固定命令字
    output o_tx_ready,                   // 响应比较许可
    output o_core_rstn,                  // 套间仅复位原计算壳
    output [255:0] o_payload             // 仅经冻结快照传送的诊断包
);
    //---------------状态参数区域---------------//
    localparam [4:0] ST_ADDRESS = 5'd0;
    localparam [4:0] ST_FETCH = 5'd1;
    localparam [4:0] ST_DECODE = 5'd2;
    localparam [4:0] ST_SEND = 5'd3;
    localparam [4:0] ST_EXPECT = 5'd4;
    localparam [4:0] ST_STATUS_CMD = 5'd5;
    localparam [4:0] ST_STATUS_READ = 5'd6;
    localparam [4:0] ST_RESET = 5'd7;
    localparam [4:0] ST_RELEASE = 5'd8;
    localparam [4:0] ST_END = 5'd9;
    localparam [4:0] ST_PASS = 5'd10;
    localparam [4:0] ST_FAIL = 5'd11;

    //---------------状态机信号-----------------//
    reg [4:0] state_current;
    reg [4:0] state_next;

    //---------------寄存器信号-----------------//
    reg [18:0] mem_program [0:32767];      // 固定脚本ROM，初始化须另核查
    reg [18:0] reg_rom_data;              // 同步ROM读结果
    reg [18:0] reg_instruction;           // 整条指令锁存至握手结束
    reg [14:0] reg_program_addr;          // 当前固定脚本地址
    reg reg_core_rstn;                   // 套间复位控制寄存器
    reg [3:0] cnt_reset_wait;            // 断言和释放各等八拍
    reg [4:0] cnt_status_word;           // 完整31字快照读进度
    reg [15:0] reg_status_flags;         // 当前轮询的冻结状态首字
    reg [31:0] reg_core_cycles;          // 原runner计时窗口
    reg [1:0] cnt_cases;                 // 完整C000结束字数量
    reg [10:0] cnt_compared;             // 已匹配数据项，最大1152
    reg [1:0] reg_status;                // 0运行、1通过、2失败
    reg [31:0] cnt_total_cycles;         // 不含全局复位的端点耗时
    reg [31:0] cnt_preload_cycles;       // 不在运行或导出区间的耗时
    reg [31:0] cnt_export_cycles;        // 4000接受至C000接受
    reg [24:0] cnt_run_elapsed;          // 3000接受至完成状态读完
    reg [31:0] cnt_sent_words;           // 真正被壳接收的字数
    reg reg_running;                     // 轮询期间仍算运行等待
    reg reg_exporting;                   // 导出握手窗口
    reg [14:0] reg_first_error_addr;     // 首错脚本地址
    reg [15:0] reg_first_expected;       // 首错期望响应
    reg [15:0] reg_first_actual;         // 首错实际响应
    reg [3:0] reg_error_kind;            // 1错字2状态3周期4计数5超时6协议
    reg [3:0] dec_error_kind;
    reg [15:0] dec_error_expected;

    //-----------------标志信号-----------------//
    wire flag_send;
    wire flag_receive;
    wire flag_done_snapshot;
    wire flag_terminal;

    //---------------其他信号连线---------------//
    assign flag_send = o_rx_valid & i_rx_ready;
    assign flag_receive = o_tx_ready & i_tx_valid;
    assign flag_done_snapshot = reg_status_flags[10] & ~reg_status_flags[9];
    assign flag_terminal = (state_current == ST_PASS) | (state_current == ST_FAIL);

    //---------------输出信号连线---------------//
    assign o_rx_valid = i_rstn & ((state_current == ST_SEND) | (state_current == ST_STATUS_CMD));
    assign o_rx_data = (state_current == ST_STATUS_CMD) ? 16'h5000 : reg_instruction[15:0];
    assign o_tx_ready = i_rstn & ((state_current == ST_EXPECT) | (state_current == ST_STATUS_READ));
    assign o_core_rstn = i_rstn & reg_core_rstn;
    assign o_payload = {reg_status, state_current, cnt_cases, cnt_compared, reg_core_cycles,
        cnt_preload_cycles, cnt_export_cycles, cnt_total_cycles, reg_first_error_addr,
        reg_first_expected, reg_first_actual, reg_error_kind, cnt_sent_words, cnt_run_elapsed};

    //---------------主要任务处理区域---------------//
    // ponytail: 未压缩的固定脚本换取简单播放器；仅在实际ERAM超预算时压缩。
    initial begin
        $readmemh("selftest_program.hex", mem_program);
    end

    // 地址改变后留完整一拍，再将同步ROM响应锁存为指令。
    always @(posedge i_clk) begin
        reg_rom_data <= mem_program[reg_program_addr];
    end

    // 状态寄存器独立于控制和诊断寄存器。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) state_current <= ST_ADDRESS;
        else state_current <= state_next;
    end

    // 完整状态响应读完才能继续；失败优先于结束成功。
    always @(*) begin
        state_next = state_current;
        dec_error_kind = 4'd0;
        dec_error_expected = reg_instruction[15:0];
        case (state_current)
            ST_ADDRESS: state_next = ST_FETCH;
            ST_FETCH: state_next = ST_DECODE;
            ST_DECODE: begin
                case (reg_instruction[18:16])
                    3'd0, 3'd4, 3'd5: state_next = ST_SEND;
                    3'd1: state_next = ST_EXPECT;
                    3'd2: state_next = ST_STATUS_CMD;
                    3'd3: state_next = (reg_instruction[15:0] == 16'd0) ? ST_RESET : ST_END;
                    default: state_next = ST_FAIL;
                endcase
            end
            ST_SEND: if (flag_send) state_next = ST_ADDRESS;
            ST_EXPECT: if (flag_receive) begin
                if (i_tx_data != reg_instruction[15:0]) begin
                    state_next = ST_FAIL;
                    dec_error_kind = 4'd1;
                end else state_next = ST_ADDRESS;
            end
            ST_STATUS_CMD: if (flag_send) state_next = ST_STATUS_READ;
            ST_STATUS_READ: if (flag_receive) begin
                if ((cnt_status_word == 5'd0) &&
                    (i_tx_data[12] | i_tx_data[11] | i_tx_data[8] | ~i_tx_data[7])) begin
                    state_next = ST_FAIL;
                    dec_error_kind = 4'd2;
                    dec_error_expected = 16'h0080;
                end else if (cnt_status_word == 5'd30) begin
                    if (flag_done_snapshot) begin
                        if (reg_core_cycles != {16'd0, reg_instruction[15:0]}) begin
                            state_next = ST_FAIL;
                            dec_error_kind = 4'd3;
                            dec_error_expected = reg_instruction[15:0];
                        end else state_next = ST_ADDRESS;
                    end else state_next = ST_STATUS_CMD;
                end
            end
            ST_RESET: if (cnt_reset_wait == 4'd7) state_next = ST_RELEASE;
            ST_RELEASE: if (cnt_reset_wait == 4'd7) state_next = ST_ADDRESS;
            ST_END: begin
                if ((cnt_cases == 2'd3) && (cnt_compared == 11'd1152)) state_next = ST_PASS;
                else begin
                    state_next = ST_FAIL;
                    dec_error_kind = 4'd4;
                    dec_error_expected = 16'd1152;
                end
            end
            ST_PASS: state_next = ST_PASS;
            ST_FAIL: state_next = ST_FAIL;
            default: begin state_next = ST_FAIL; dec_error_kind = 4'd6; end
        endcase
        if (!flag_terminal && (cnt_total_cycles >= 32'd500000)) begin
            state_next = ST_FAIL;
            dec_error_kind = 4'd5;
        end
        if (!flag_terminal && i_tx_valid && (i_tx_data == 16'he001) &&
            (state_current != ST_STATUS_READ)) begin
            state_next = ST_FAIL;
            dec_error_kind = 4'd6;
        end
    end

    // 总计只在全局复位清零；套间复位只作用于原计算壳。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) begin
            reg_instruction <= 19'd0;
            reg_program_addr <= 15'd0;
            reg_core_rstn <= 1'b0;
            cnt_reset_wait <= 4'd0;
            cnt_status_word <= 5'd0;
            reg_status_flags <= 16'd0;
            reg_core_cycles <= 32'd0;
            cnt_cases <= 2'd0;
            cnt_compared <= 11'd0;
            reg_status <= 2'd0;
            cnt_total_cycles <= 32'd0;
            cnt_preload_cycles <= 32'd0;
            cnt_export_cycles <= 32'd0;
            cnt_run_elapsed <= 25'd0;
            cnt_sent_words <= 32'd0;
            reg_running <= 1'b0;
            reg_exporting <= 1'b0;
            reg_first_error_addr <= 15'd0;
            reg_first_expected <= 16'd0;
            reg_first_actual <= 16'd0;
            reg_error_kind <= 4'd0;
        end else begin
            if (!flag_terminal) begin
                cnt_total_cycles <= cnt_total_cycles + 32'd1;
                if (reg_running) cnt_run_elapsed <= cnt_run_elapsed + 25'd1;
                else if (reg_exporting) cnt_export_cycles <= cnt_export_cycles + 32'd1;
                else cnt_preload_cycles <= cnt_preload_cycles + 32'd1;
            end
            if (state_current == ST_FETCH) reg_instruction <= reg_rom_data;
            if ((state_current == ST_DECODE) && (reg_instruction[18:16] == 3'd3) &&
                (reg_instruction[15:0] == 16'd0)) begin
                reg_core_rstn <= 1'b0;
                cnt_reset_wait <= 4'd0;
                reg_status_flags <= 16'd0;
                reg_core_cycles <= 32'd0;
            end
            if (state_current == ST_RESET) begin
                if (cnt_reset_wait == 4'd7) begin
                    reg_core_rstn <= 1'b1;
                    cnt_reset_wait <= 4'd0;
                end else cnt_reset_wait <= cnt_reset_wait + 4'd1;
            end
            if (state_current == ST_RELEASE) begin
                if (cnt_reset_wait == 4'd7) begin
                    reg_program_addr <= reg_program_addr + 15'd1;
                    cnt_reset_wait <= 4'd0;
                end else cnt_reset_wait <= cnt_reset_wait + 4'd1;
            end
            if (flag_send) begin
                cnt_sent_words <= cnt_sent_words + 32'd1;
                if (state_current == ST_SEND) begin
                    reg_program_addr <= reg_program_addr + 15'd1;
                    if (reg_instruction[18:16] == 3'd4) reg_running <= 1'b1;
                    if (reg_instruction[18:16] == 3'd5) reg_exporting <= 1'b1;
                end else cnt_status_word <= 5'd0;
            end
            if ((state_current == ST_STATUS_READ) && flag_receive) begin
                cnt_status_word <= cnt_status_word + 5'd1;
                if (cnt_status_word == 5'd0) reg_status_flags <= i_tx_data;
                if (cnt_status_word == 5'd3) reg_core_cycles[15:0] <= i_tx_data;
                if (cnt_status_word == 5'd4) reg_core_cycles[31:16] <= i_tx_data;
                if ((cnt_status_word == 5'd30) && flag_done_snapshot) begin
                    reg_program_addr <= reg_program_addr + 15'd1;
                    reg_running <= 1'b0;
                end
            end
            if ((state_current == ST_EXPECT) && flag_receive && (i_tx_data == reg_instruction[15:0])) begin
                reg_program_addr <= reg_program_addr + 15'd1;
                if (i_tx_data[15:12] == 4'h9) cnt_compared <= cnt_compared + 11'd1;
                if (i_tx_data == 16'hc000) begin
                    cnt_cases <= cnt_cases + 2'd1;
                    reg_exporting <= 1'b0;
                end
            end
            if (state_next == ST_PASS) reg_status <= 2'd1;
            if ((state_next == ST_FAIL) && (state_current != ST_FAIL)) begin
                reg_status <= 2'd2;
                reg_core_rstn <= 1'b0;
                reg_first_error_addr <= reg_program_addr;
                reg_first_expected <= dec_error_expected;
                reg_first_actual <= (dec_error_kind == 4'd3) ? reg_core_cycles[15:0] : i_tx_data;
                reg_error_kind <= dec_error_kind;
            end
        end
    end
endmodule
