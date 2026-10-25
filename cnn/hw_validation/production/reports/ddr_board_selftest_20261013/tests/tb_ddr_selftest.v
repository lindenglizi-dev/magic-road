`timescale 1ns / 1ps

// 受控PAXI端点仅验证请求器的账目、比较和取消；不是DDR器件模型。
module tb_ddr_selftest;
    reg clk = 0;                           // 约133MHz用户时钟
    reg rstn = 0;                          // 同时取消请求器及受控端点
    reg phy_ready = 0;                     // 可注入初始化超时或掉ready
    reg awready = 0;                       // 地址侧独立背压
    reg wready = 0;                        // 数据侧独立背压
    reg arready = 0;                       // 读地址侧独立背压
    wire [24:0] awaddr;                    // 被测原生写地址
    wire awvalid;                          // 被测地址请求
    wire [127:0] wdata;                    // 被测写字
    wire [15:0] wstrb;                     // 检查与既有工程一致的掩码值
    wire wvalid;                           // 被测数据请求
    wire wlast;                            // 被测单拍写尾
    wire [24:0] araddr;                    // 被测逆序读地址
    wire arvalid;                          // 被测读请求
    wire rready;                           // 请求器数据接受许可
    wire [1:0] status;                     // 被测持续终态
    wire [3:0] error_kind;                 // 首错编码
    wire [3:0] state_value;                // 实验当前阶段
    wire [3:0] writes;                     // 请求器成对接受计数
    wire [3:0] reads;                      // 请求器正确比较计数
    wire [24:0] address;                   // 首错地址观测
    wire [127:0] expected_data;            // 首错完整期望字
    wire [127:0] actual_data;              // 首错完整实际字
    wire [31:0] cycles;                    // 核心经过周期
    wire rvalid;                           // 受控端点有效返回
    wire rlast;                            // 单拍返回或故意缺尾
    wire [127:0] rdata;                    // 受控端点数据或故意翻转
    reg response_valid = 0;                // 延迟响应持有寄存器
    reg [127:0] response_data = 0;          // 延迟响应的独立存储读出
    reg [127:0] memory [0:3];              // 四字端点存储，不能当真实DDR
    reg [127:0] vectors [0:7];             // Python独立导出的八个期望字
    reg pending_aw = 0;                    // 已接受尚未配对的地址
    reg pending_w = 0;                     // 已接受尚未配对的数据
    reg [24:0] held_aw = 0;                // 分离握手时冻结地址
    reg [127:0] held_w = 0;                // 分离握手时冻结写字
    reg pending_read = 0;                  // 已登记的唯一读事务
    reg [24:0] held_ar = 0;                // 延迟响应地址
    reg [127:0] previous_wdata = 0;        // 检查W背压保持
    reg [284:0] terminal_scene = 0;        // 首错地址、期望、实际与编码必须保持
    reg [24:0] previous_awaddr = 0;        // 检查AW背压保持
    reg [24:0] previous_araddr = 0;        // 检查AR背压保持
    reg blocked_aw = 0;                    // 上拍地址未接受
    reg blocked_w = 0;                     // 上拍数据未接受
    reg blocked_ar = 0;                    // 上拍读地址未接受
    integer test_case = 0;                 // 外部选择场景
    integer active_mode = 0;               // 复位恢复后可切换正常端点
    integer tick = 0;                      // 当前复位世代的周期
    integer aw_count = 0;                  // 端点接受地址次数
    integer w_count = 0;                   // 端点接受数据次数
    integer ar_count = 0;                  // 端点接受读地址次数
    integer r_count = 0;                   // 端点返回握手次数
    integer read_delay = 0;                // 受控可变响应等待
    integer expected_error = 0;            // 本用例应观察到的故障
    integer seed = 42;                     // 固定随机流
    integer choice = 0;                   // 确定性气泡选择值
    integer index;                        // 初始化存储循环索引
    integer ignored;                      // 接收plusarg返回值

    // 用户时钟不替代真实IP的时钟启动证据。
    always #3.75 clk = ~clk;               // 端点仿真周期7.5ns

    // 同拍返回及故障注入仅在本受控端点中存在。
    assign rvalid = response_valid || ((active_mode == 2) && arvalid && arready) || ((active_mode == 10) && phy_ready && (tick == 12)) || ((active_mode == 16) && (status == 1)); // 生成指定场景返回
    assign rlast = (active_mode != 4);     // 场景四故意遗漏RLAST
    assign rdata = (((active_mode == 2) && arvalid && arready) ? memory[araddr[4:3]] : response_data) ^ ((active_mode == 3) ? 128'd1 : 128'd0); // 单比特错误可定位

    // 真实被测请求器，超时缩短只用于端点回归。
    road_ddr_selftest #(.C_TIMEOUT(27'd63)) dut (
        .i_clk(clk), .i_rstn(rstn), .i_phy_ready(phy_ready),
        .i_awready(awready), .i_wready(wready), .i_arready(arready),
        .i_rvalid(rvalid), .i_rlast(rlast), .i_rdata(rdata),
        .o_awaddr(awaddr), .o_awvalid(awvalid), .o_wdata(wdata), .o_wstrb(wstrb),
        .o_wvalid(wvalid), .o_wlast(wlast), .o_araddr(araddr), .o_arvalid(arvalid),
        .o_rready(rready), .o_status(status), .o_error(error_kind), .o_state(state_value),
        .o_writes(writes), .o_reads(reads), .o_address(address),
        .o_expected(expected_data), .o_actual(actual_data), .o_cycles(cycles)
    );

    // 在下降沿改变端点许可，避免与DUT上升沿竞争。
    always @(negedge clk) begin
        if (!rstn) begin
            phy_ready = 0;                // 整个端点复位
            awready = 0;                  // 复位期间不接受地址
            wready = 0;                   // 复位期间不接受数据
            arready = 0;                  // 复位期间不接受读请求
        end else begin
            phy_ready = (tick >= 4) && (active_mode != 5); // 初始化等待可终止
            awready = (active_mode != 6); // 单独注入AW永久背压
            wready = (active_mode != 7);  // 单独注入W永久背压
            arready = (active_mode != 8); // 单独注入AR永久背压
            if (active_mode == 1) begin
                awready = (tick % 3 == 0); // AW与W不同节奏
                wready = (tick % 5 == 0); // 检查W提前或延后接受
                arready = (tick % 4 == 0); // 读地址也有气泡
            end
            if (active_mode == 12) begin
                wready = 0;               // 复位前制造部分接受
            end
            if (active_mode == 14) begin
                awready = (tick % 40 == 0); // 长停顿仍小于看门狗
                wready = (tick % 41 == 0); // 不能依赖两个ready相同
                arready = (tick % 37 == 0); // 长读请求等待
            end
            if (active_mode == 15) begin
                choice = $random(seed);   // 可复现随机气泡
                awready = choice[0];     // AW随机许可
                wready = choice[1];      // W独立随机许可
                arready = choice[2];     // AR独立随机许可
            end
            if ((active_mode == 11) && (writes != 0)) begin
                phy_ready = 0;            // 运行中丢失ready
            end
        end
    end

    // 独立端点按握手登记、成对提交并返回，不能用DUT自身期望充当存储。
    always @(posedge clk or negedge rstn) begin
        if (!rstn) begin
            tick = 0;                     // 清除旧世代时间
            aw_count = 0;                 // 清除端点AW账目
            w_count = 0;                  // 清除端点W账目
            ar_count = 0;                 // 清除端点AR账目
            r_count = 0;                  // 清除端点返回账目
            pending_aw = 0;               // 取消部分地址
            pending_w = 0;                // 取消部分写数据
            pending_read = 0;             // 取消在途读
            response_valid <= 0;          // 不泄漏旧返回；NBA避免与DUT采样竞争
            response_data <= 0;           // 取消旧返回payload
            blocked_aw = 0;               // 新世代不沿用背压断言
            blocked_w = 0;                // 旧W保持条件取消
            blocked_ar = 0;               // 旧AR保持条件取消
            read_delay = 0;               // 旧响应延迟取消
            for (index = 0; index < 4; index = index + 1) begin
                memory[index] = 128'hfeedface; // 未写过不能恰好匹配向量
            end
        end else begin
            tick = tick + 1;              // 所有等待周期都推进
            if (blocked_aw && (status == 0) && (!awvalid || (awaddr !== previous_awaddr))) begin
                $fatal(1, "AW changed before acceptance"); // 地址保持断言
            end
            if (blocked_w && (status == 0) && (!wvalid || (wdata !== previous_wdata) || !wlast)) begin
                $fatal(1, "W changed before acceptance"); // 数据和末拍保持断言
            end
            if (blocked_ar && (status == 0) && (!arvalid || (araddr !== previous_araddr))) begin
                $fatal(1, "AR changed before acceptance"); // 读地址保持断言
            end
            blocked_aw = awvalid && !awready && (status == 0); // 只登记未接受请求
            blocked_w = wvalid && !wready && (status == 0); // 独立W背压账目
            blocked_ar = arvalid && !arready && (status == 0); // 独立AR背压账目
            previous_awaddr = awaddr;      // 下一拍保持检查基准
            previous_wdata = wdata;        // 不从返回数据反推请求
            previous_araddr = araddr;      // 下一拍读地址保持基准
            if (rvalid && rready) begin
                r_count = r_count + 1;    // 仅实际接收时退休返回
                response_valid <= 0;      // 已接受数据不重复提供
                pending_read = 0;         // 唯一在途槽释放
            end
            if (awvalid && awready) begin
                if (pending_aw || (aw_count >= 8) || (awaddr !== ((aw_count % 4) * 8))) begin
                    $fatal(1, "AW duplicated or wrong native address"); // 地址独立检查
                end
                held_aw = awaddr;         // 冻结已接受地址
                pending_aw = 1;           // 等待对应数据
                aw_count = aw_count + 1;  // 接受次数只增加一次
            end
            if (wvalid && wready) begin
                if (pending_w || (w_count >= 8) || (wdata !== vectors[w_count]) || (wstrb !== 16'h0000) || !wlast) begin
                    $fatal(1, "W duplicated, wrong vector or mask"); // 独立Python向量检查
                end
                held_w = wdata;           // 不假设AW与W同拍
                pending_w = 1;            // 等待对应地址
                w_count = w_count + 1;    // 数据接受次数
            end
            if (pending_aw && pending_w) begin
                memory[held_aw[4:3]] = held_w; // 受控端点提交，不声称真实写屏障
                pending_aw = 0;           // 释放配对地址槽
                pending_w = 0;            // 释放配对数据槽
            end
            if (arvalid && arready) begin
                if (pending_read || (ar_count >= 8) || (araddr !== ((3 - (ar_count % 4)) * 8))) begin
                    $fatal(1, "AR duplicated or out of reverse order"); // 检查逆序与单在途
                end
                ar_count = ar_count + 1;  // 读地址只接受一次
                if (active_mode != 2) begin
                    pending_read = 1;     // 延迟返回持有唯一读槽
                    held_ar = araddr;     // 独立捕获响应地址
                    read_delay = 4;       // 仅端点测试的响应时延
                end
            end
            if (pending_read && !response_valid && (active_mode != 9) && (active_mode != 13)) begin
                if (read_delay == 0) begin
                    response_data <= memory[held_ar[4:3]]; // 从独立存储返回真实写入字
                    response_valid <= 1;  // 返回保持到RREADY
                end else begin
                    read_delay = read_delay - 1; // 测试可变返回等待
                end
            end
        end
    end

    // 全部用例共享同一DUT与Python向量。
    initial begin
        ignored = $value$plusargs("CASE=%d", test_case); // 选择单个可复现场景
        active_mode = test_case;           // 默认不更改注入类型
        $readmemh("patterns.hex", vectors); // 期望来源独立于RTL常量
        repeat (4) @(negedge clk);         // 明确施加启动复位
        rstn = 1;                         // 开始新世代
        if (test_case == 12) begin
            wait (aw_count == 1);          // AW已接受而W尚未接受
            @(negedge clk); rstn = 0;      // 取消部分写事务
            #0.1;
            if (awvalid || wvalid || arvalid || rready) $fatal(1, "Reset did not cancel request"); // 立即取消
            repeat (3) @(negedge clk);     // 整个端点复位
            active_mode = 0; rstn = 1;     // 恢复后重跑八次比较
        end
        if (test_case == 13) begin
            wait (pending_read);          // 读请求已接受、返回尚未产生
            @(negedge clk); rstn = 0;      // 同时取消端点在途读
            repeat (3) @(negedge clk);     // 旧读不能穿过复位
            active_mode = 0; rstn = 1;     // 完整重新初始化
        end
        case (test_case)
            3: expected_error = 5;          // 错字必须失败
            4: expected_error = 6;          // 缺末拍必须失败
            5: expected_error = 1;          // 初始化超时
            6, 7: expected_error = 2;       // 任一写通道永久背压
            8: expected_error = 3;          // 读地址超时
            9: expected_error = 4;          // 读返回超时
            10: expected_error = 7;         // 无请求返回
            11: expected_error = 8;         // 初始化状态掉落
            16: expected_error = 7;         // 通过后出现额外返回
            default: expected_error = 0;   // 其他场景必须正常结束
        endcase
        if (test_case == 16) begin
            wait (status == 1);            // 先完成全部数据比较
            wait (status == 2);            // 额外返回必须推翻终态
        end else begin
            wait (status != 0);            // 不用固定周期猜测完成
        end
        #1;
        if (expected_error == 0) begin
            if ((status !== 1) || (writes !== 8) || (reads !== 8) || (aw_count != 8) || (w_count != 8) || (ar_count != 8) || (r_count != 8)) begin
                $fatal(1, "Missing/duplicate transaction status=%d counts=%d/%d/%d/%d", status, aw_count, w_count, ar_count, r_count); // 接受与返回守恒
            end
        end else if ((status !== 2) || (error_kind !== expected_error)) begin
            $fatal(1, "Wrong failure case=%d error=%d expected=%d", test_case, error_kind, expected_error); // 故障分类正确
        end
        if ((test_case == 3) && ((address !== 25'd24) || (expected_data !== vectors[3]) || (actual_data !== (vectors[3] ^ 128'd1)))) begin
            $fatal(1, "First mismatch evidence differs"); // 首错完整数据必须可复现
        end
        if ((test_case == 4) && ((address !== 25'd24) || (expected_data !== vectors[3]) || (actual_data !== vectors[3]))) begin
            $fatal(1, "Missing-last evidence differs"); // 区分数据正确但末拍丢失
        end
        terminal_scene = {address, expected_data, actual_data, error_kind}; // 保存完整终态证据
        repeat (5) @(negedge clk);         // 终态必须保持，无新请求
        if ({address, expected_data, actual_data, error_kind} !== terminal_scene) $fatal(1, "First evidence changed"); // 禁止后续覆盖首错
        if (awvalid || wvalid || arvalid || rready) $fatal(1, "Terminal issued traffic"); // 结束后不重跑
        $display("DDR_REQUESTER_PASS case=%0d cycles=%0d writes=%0d reads=%0d error=%0d", test_case, cycles, writes, reads, error_kind); // 机器可读结果
        $finish;                           // 本测试只证明请求器
    end

    // 所有场景均有独立平台超时，防止失效状态无穷等待。
    initial begin
        #100000;
        $fatal(1, "Testbench timeout");    // 保留无法结束的用例
    end
endmodule
