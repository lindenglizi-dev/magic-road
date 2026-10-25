`timescale 1ns / 1ps

////////////////////////////////////English///////////////////////////////////////
// Company:         Erie
// Engineer:        Erie
//
// Create Date:     2026/10/04 00:00:00
// Design Name:     tb_paxi_single_outstanding_bridge
// Module Name:     tb_paxi_single_outstanding_bridge
// Description:     Fixed-seed self-check for the isolated PAXI safety probe
// Simulations:     Icarus Verilog
//
// Referrences:     cnn/hw_validation/ddr/requirements.md
//
// Dependencies:    paxi_single_outstanding_bridge.v
//
// Version:         V1.0
// Revision Date:   2026/10/04 00:00:00
// History:
// Time             Version     Revised by        Contents
// 2026/10/04       V1.0        Erie              Create file.
///////////////////////////////////Chinese////////////////////////////////////////
// 版权归属:        Erie
// 开发人员:        Erie
//
// 创建日期:        2026年10月04日
// 设计名称:        tb_paxi_single_outstanding_bridge
// 模块名称:        tb_paxi_single_outstanding_bridge
// 模块说明:        隔离PAXI安全探针固定种子自检
// 仿真工程:        Icarus Verilog
//
// 参考资料:        cnn/hw_validation/ddr/requirements.md
//
// 依赖文件:        paxi_single_outstanding_bridge.v
//
// 当前版本:        V1.0
// 修订日期:        2026年10月04日
// 修订历史:
// 时间             版本        修订人            修订内容
// 2026年10月04日   V1.0        Erie              创建文件

//PAXI安全探针自检平台
module tb_paxi_single_outstanding_bridge;

    //--------------寄存器信号--------------//
    // 时钟和协调复位驱动
    reg reg_clk = 0;                        // 十纳秒周期测试时钟
    reg reg_rstn = 0;                       // 同时复位DUT与模拟端点

    // 上游请求驱动
    reg flag_req_valid = 0;                 // 请求载荷有效驱动
    reg flag_req_write = 0;                 // 请求读写类型驱动
    reg [31:0]reg_req_byte_addr = 0;         // 请求字节地址驱动
    reg [127:0]reg_req_write_data = 0;       // 请求写载荷驱动
    reg [15:0]reg_req_write_mask = 0;        // 高有效写屏蔽驱动
    reg [31:0]reg_req_epoch = 0;             // 请求世代驱动
    reg [31:0]reg_req_owner = 0;             // 请求所有者驱动
    reg flag_cancel = 0;                    // 当前唯一事务取消驱动

    // 上游结果与提交驱动
    reg flag_commit_confirmed = 0;           // 显式写提交事件驱动
    reg flag_result_ready = 0;               // 结果接收反压驱动

    // 模拟PAXI端点驱动
    reg flag_paxi_arready = 0;               // 读地址就绪驱动
    reg flag_paxi_awready = 0;               // 写地址就绪驱动
    reg flag_paxi_wready = 0;                // 写数据就绪驱动
    reg flag_paxi_rvalid = 0;                // 无READY返回有效驱动
    reg flag_paxi_rlast = 0;                 // 返回末拍驱动
    reg [127:0]reg_paxi_rdata = 0;           // 返回载荷驱动

    // 固定种子和自检统计
    integer reg_seed = 32'h0000051b;        // 确定性随机载荷种子
    integer cnt_error = 0;                  // 自检失败累计值
    integer cnt_accepted = 0;               // 控制器接收事务累计值
    integer cnt_success = 0;                // 上游成功握手累计值

    //---------------其他信号---------------//
    // 上游请求与结果观察点
    wire flag_req_ready;                    // DUT本地请求就绪
    wire flag_result_valid;                 // DUT成功结果有效
    wire flag_result_write;                 // 结果操作类型
    wire flag_result_committed;             // 写提交证明状态
    wire [31:0]result_epoch;                 // 结果世代观察值
    wire [31:0]result_owner;                 // 结果所有者观察值
    wire [127:0]result_read_data;            // 结果读载荷观察值

    // 接收和状态遥测观察点
    wire flag_paxi_accepted_valid;          // 控制器接收事件
    wire flag_paxi_accepted_write;          // 接收事件读写类型
    wire [31:0]paxi_accepted_epoch;          // 接收事件世代
    wire [31:0]paxi_accepted_owner;          // 接收事件所有者
    wire flag_drain_done;                   // DUT完全排空状态
    wire flag_protocol_fault;               // DUT粘滞协议故障
    wire [31:0]cnt_late_discard;             // 取消后晚到事件累计值
    wire [31:0]cnt_cancelled_drain;          // 已接收取消排空累计值

    // PAXI输出观察点
    wire flag_paxi_arvalid;                 // 读地址有效观察值
    wire [24:0]paxi_araddr;                  // 读字地址观察值
    wire flag_paxi_awvalid;                 // 写地址有效观察值
    wire [24:0]paxi_awaddr;                  // 写字地址观察值
    wire flag_paxi_wvalid;                  // 写数据有效观察值
    wire [127:0]paxi_wdata;                  // 写载荷观察值
    wire [15:0]paxi_wmask;                   // 高有效屏蔽观察值

    //---------------任务定义区域---------------//
    // 比较条件并记录可继续执行的失败
    task check_condition;
        input i_condition;                  // 预期为真的布尔条件
        input [8 * 96 - 1:0]i_message;       // 失败时打印的场景说明
        begin
            if(i_condition !== 1'b1)begin
                cnt_error = cnt_error + 1;  // 保留全部失败而不是首错退出
                $display(" > ERR: [Verilog] %0s", i_message); // 输出可检索失败原因
            end
        end
    endtask

    // 驱动一个保持到ready的本地请求
    task send_request;
        input i_write;                      // 当前请求操作类型
        input [31:0]i_byte_addr;             // 当前请求字节地址
        input [127:0]i_write_data;           // 当前请求写载荷
        input [15:0]i_write_mask;            // 当前请求高有效屏蔽
        input [31:0]i_epoch;                 // 当前请求世代
        input [31:0]i_owner;                 // 当前请求所有者
        begin
            @(negedge reg_clk);             // 在采样沿前建立请求载荷
            flag_req_write = i_write;       // 选择本次读写方向
            reg_req_byte_addr = i_byte_addr; // 提供十六字节对齐地址
            reg_req_write_data = i_write_data; // 提供AW前缓存载荷
            reg_req_write_mask = i_write_mask; // 提供控制器屏蔽语义
            reg_req_epoch = i_epoch;        // 绑定事务世代
            reg_req_owner = i_owner;        // 绑定返回所有者
            flag_req_valid = 1'b1;          // 开始请求握手
            @(posedge reg_clk);             // 等待DUT采样本地请求
            check_condition(flag_req_ready, "request was not accepted in idle"); // 确认本地握手发生
            @(negedge reg_clk);             // 握手后撤销请求有效
            flag_req_valid = 1'b0;          // 防止重复接收同一请求
        end
    endtask

    // 施加与模拟端点同步的协调硬复位
    task coordinated_reset;
        begin
            @(negedge reg_clk);             // 在非采样沿拉低协调复位
            reg_rstn = 1'b0;                // 同时代表端点复位
            flag_req_valid = 1'b0;          // 复位期间禁止新请求
            flag_cancel = 1'b0;             // 复位期间撤销本地取消
            flag_commit_confirmed = 1'b0;   // 复位期间无提交证明
            flag_result_ready = 1'b0;       // 复位期间不接收结果
            flag_paxi_arready = 1'b0;       // 模拟端点关闭AR接收
            flag_paxi_awready = 1'b0;       // 模拟端点关闭AW接收
            flag_paxi_wready = 1'b0;        // 模拟端点关闭W接收
            flag_paxi_rvalid = 1'b0;        // 模拟端点保证无旧返回
            flag_paxi_rlast = 1'b0;         // 清除返回末拍驱动
            repeat(3)@(posedge reg_clk);    // 覆盖多个协调复位时钟
            @(negedge reg_clk);             // 在非采样沿释放复位
            reg_rstn = 1'b1;                // 端点与DUT共同重新启动
            repeat(2)@(posedge reg_clk);    // 等待空闲状态稳定
        end
    endtask

    //-------------其他信号连线-------------//
    // 固定周期时钟
    always #5 reg_clk = ~reg_clk;           // 产生一百兆赫测试时钟

    // 统计控制器真实接收事件
    always@(posedge reg_clk or negedge reg_rstn)begin
        if(reg_rstn == 1'b0)begin
            cnt_accepted <= 0;              // 每次协调复位重建守恒基线
        end else if(flag_paxi_accepted_valid == 1'b1)begin
            cnt_accepted <= cnt_accepted + 1; // 接收脉冲只计一次
        end
    end

    // 统计上游成功结果握手
    always@(posedge reg_clk or negedge reg_rstn)begin
        if(reg_rstn == 1'b0)begin
            cnt_success <= 0;               // 每次协调复位清空成功数
        end else if(flag_result_valid == 1'b1 && flag_result_ready == 1'b1)begin
            cnt_success <= cnt_success + 1; // 只统计未被取消的结果
        end
    end

    //--------------初始化区域--------------//
    // 固定种子主测试序列覆盖反压、取消和协议错误
    initial begin
        reg_req_write_data = {$random(reg_seed), $random(reg_seed), $random(reg_seed), $random(reg_seed)}; // 生成确定性首个写载荷
        coordinated_reset();                // 建立无旧返回的起始状态

        send_request(1'b1, 32'h03400000, reg_req_write_data, 16'h8421, 32'd7, 32'd11); // 提交将被取消的写事务
        @(posedge reg_clk);                 // 从检查态进入AW呈现态
        @(negedge reg_clk);                 // 在稳定半周期检查通道
        check_condition(flag_paxi_awvalid && !flag_paxi_wvalid, "W appeared before AW acceptance"); // W禁止先于AW
        check_condition(paxi_awaddr == 25'h1a00000, "byte address was not shifted by one"); // 核对固定地址换算
        flag_cancel = 1'b1;                 // AW受压时取消当前所有者
        repeat(2)@(posedge reg_clk);        // 验证VALID跨取消保持
        check_condition(flag_paxi_awvalid, "cancel withdrew presented AWVALID"); // 已呈现AW不得撤回
        check_condition(paxi_awaddr == 25'h1a00000, "AW address changed under backpressure"); // 地址必须保持稳定
        @(negedge reg_clk);                 // 结束取消脉冲并允许AW接收
        flag_cancel = 1'b0;                 // 保留内部取消归属
        flag_paxi_awready = 1'b1;           // 模拟端点接收AW
        @(posedge reg_clk);                 // 完成AW握手
        @(negedge reg_clk);                 // 观察AW后一拍W呈现
        flag_paxi_awready = 1'b0;           // 避免额外AW接收
        check_condition(flag_paxi_wvalid, "W was not presented one cycle after AW acceptance"); // 检查呈现期限
        check_condition(paxi_wdata == reg_req_write_data, "cached W data changed before acceptance"); // 核对载荷缓存
        check_condition(paxi_wmask == 16'h8421, "high-active mask was altered"); // 屏蔽位必须原样传递
        reg_req_write_data = ~reg_req_write_data; // 扰动上游总线验证缓存隔离
        reg_req_write_mask = 16'h0000;      // 扰动上游屏蔽输入
        repeat(2)@(posedge reg_clk);        // 延长WREADY反压窗口
        check_condition(flag_paxi_wvalid && paxi_wmask == 16'h8421, "W payload was not held under backpressure"); // 检查稳定性
        @(negedge reg_clk);                 // 在采样沿前开启W接收
        flag_paxi_wready = 1'b1;            // 模拟端点接收缓存数据
        @(posedge reg_clk);                 // 完成W握手
        @(negedge reg_clk);                 // 观察延迟一拍的接收遥测
        flag_paxi_wready = 1'b0;            // 防止重复数据握手
        check_condition(flag_paxi_accepted_valid && flag_paxi_accepted_write, "write acceptance telemetry missing"); // accepted不等于committed
        repeat(2)@(posedge reg_clk);        // 在没有提交证明时等待
        check_condition(!flag_result_valid && !flag_drain_done, "write completed without explicit commit proof"); // 禁止默认提交
        @(negedge reg_clk);                 // 在后续独立周期提供提交证明
        flag_commit_confirmed = 1'b1;       // 模拟已证明的外部终止事件
        @(posedge reg_clk);                 // 捕获取消后的晚到提交
        @(negedge reg_clk);                 // 撤销单周期证明输入
        flag_commit_confirmed = 1'b0;       // 防止重复提交事件
        repeat(2)@(posedge reg_clk);        // 等待退休阶段更新计数
        check_condition(flag_drain_done && !flag_result_valid, "cancelled write published success"); // 取消事务只能排空
        check_condition(cnt_late_discard == 32'd1 && cnt_cancelled_drain == 32'd1, "cancelled write counters mismatch"); // 核对晚到丢弃

        reg_req_write_data = {$random(reg_seed), $random(reg_seed), $random(reg_seed), $random(reg_seed)}; // 生成确定性正常写载荷
        send_request(1'b1, 32'h03400010, reg_req_write_data, 16'h00f0, 32'd8, 32'd12); // 提交正常写事务
        @(posedge reg_clk);                 // 进入AW呈现阶段
        @(negedge reg_clk);                 // 建立立即AW接收
        flag_paxi_awready = 1'b1;           // 允许地址握手
        flag_paxi_wready = 1'b1;            // 即使WREADY高也不得抢先
        @(posedge reg_clk);                 // 完成AW握手
        @(negedge reg_clk);                 // 观察下一拍WVALID
        flag_paxi_awready = 1'b0;           // 关闭地址接收
        check_condition(flag_paxi_wvalid, "normal write did not present W after AW"); // 验证正常写顺序
        @(posedge reg_clk);                 // WREADY高时完成W握手
        @(negedge reg_clk);                 // 关闭数据就绪
        flag_paxi_wready = 1'b0;            // 后续周期无数据接收
        check_condition(flag_paxi_accepted_valid && flag_paxi_accepted_write, "normal write acceptance missing"); // 检查写接收遥测
        flag_commit_confirmed = 1'b1;       // 在W握手后的独立周期证明提交
        @(posedge reg_clk);                 // 捕获提交终止事件
        @(negedge reg_clk);                 // 结束提交脉冲
        flag_commit_confirmed = 1'b0;       // 保持事件单拍
        repeat(2)@(posedge reg_clk);        // 进入结果保持状态
        check_condition(flag_result_valid && flag_result_write && flag_result_committed, "committed write result missing"); // 写成功必须明确标注提交
        check_condition(result_epoch == 32'd8 && result_owner == 32'd12, "write result ownership changed"); // 世代与所有者保持
        @(negedge reg_clk);                 // 准备接收保持结果
        flag_result_ready = 1'b1;           // 上游接受写结果
        @(posedge reg_clk);                 // 完成结果握手
        @(negedge reg_clk);                 // 撤销结果就绪
        flag_result_ready = 1'b0;           // 防止影响下一事务

        send_request(1'b0, 32'h03400020, 128'd0, 16'd0, 32'd9, 32'd13); // 提交将被取消的读事务
        @(posedge reg_clk);                 // 进入AR呈现阶段
        @(negedge reg_clk);                 // 在AR反压时取消
        check_condition(flag_paxi_arvalid, "read address was not presented"); // 确认取消发生在呈现后
        flag_cancel = 1'b1;                 // 标记当前读所有者取消
        repeat(2)@(posedge reg_clk);        // ARREADY保持低电平
        check_condition(flag_paxi_arvalid, "cancel withdrew presented ARVALID"); // AR必须保持至接收
        @(negedge reg_clk);                 // 结束取消并打开ARREADY
        flag_cancel = 1'b1;                 // 再次覆盖取消与AR接收同拍边界
        flag_paxi_arready = 1'b1;           // 模拟端点接收读地址
        @(posedge reg_clk);                 // 完成AR握手
        @(negedge reg_clk);                 // 关闭地址就绪并准备返回
        check_condition(flag_paxi_accepted_valid && !flag_paxi_accepted_write, "cancel-coincident AR acceptance telemetry missing"); // 同拍取消不能漏计真实握手
        flag_cancel = 1'b0;                 // 内部继续保存取消标志
        flag_paxi_arready = 1'b0;           // 防止重复AR握手
        flag_paxi_rvalid = 1'b1;            // 发送取消后的归属返回
        flag_paxi_rlast = 1'b1;             // 单拍返回必须同时结束
        reg_paxi_rdata = 128'h112233445566778899aabbccddeeff00; // 提供可识别返回载荷
        @(posedge reg_clk);                 // DUT无READY捕获返回
        @(negedge reg_clk);                 // 撤销返回输入
        flag_paxi_rvalid = 1'b0;            // 保证只有一个返回拍
        flag_paxi_rlast = 1'b0;             // 清除末拍标志
        repeat(2)@(posedge reg_clk);        // 等待取消退休完成
        check_condition(flag_drain_done && !flag_result_valid, "cancelled read published success"); // 晚返回必须静默丢弃
        check_condition(cnt_late_discard == 32'd2 && cnt_cancelled_drain == 32'd2, "cancelled read counters mismatch"); // 检查累计守恒

        send_request(1'b0, 32'h03fffff0, 128'd0, 16'd0, 32'd10, 32'd14); // 读取预留区最后合法块
        @(posedge reg_clk);                 // 进入AR呈现阶段
        @(negedge reg_clk);                 // 检查末地址换算
        check_condition(paxi_araddr == 25'h1fffff8, "last arena address conversion mismatch"); // 末块仍在端点范围
        flag_paxi_arready = 1'b1;           // 接收末地址读请求
        @(posedge reg_clk);                 // 完成AR握手
        @(negedge reg_clk);                 // 驱动正常单拍返回
        flag_paxi_arready = 1'b0;           // 关闭地址接收
        flag_paxi_rvalid = 1'b1;            // 提供归属返回
        flag_paxi_rlast = 1'b1;             // 标记唯一返回拍结束
        reg_paxi_rdata = 128'hffeeddccbbaa99887766554433221100; // 提供正常读期望值
        @(posedge reg_clk);                 // 捕获读返回
        @(negedge reg_clk);                 // 撤销返回通道
        flag_paxi_rvalid = 1'b0;            // 返回有效只保持一拍
        flag_paxi_rlast = 1'b0;             // 清除末拍驱动
        repeat(2)@(posedge reg_clk);        // 进入结果保持状态
        check_condition(flag_result_valid && !flag_result_write, "normal read result missing"); // 读结果不能标记为写
        check_condition(result_read_data == 128'hffeeddccbbaa99887766554433221100, "read data changed before consumption"); // 核对返回载荷
        check_condition(result_epoch == 32'd10 && result_owner == 32'd14, "read result ownership changed"); // 核对返回归属
        repeat(2)@(posedge reg_clk);        // 继续施加结果反压
        check_condition(flag_result_valid && result_read_data == 128'hffeeddccbbaa99887766554433221100, "read result was not stable under backpressure"); // 结果必须保持
        @(negedge reg_clk);                 // 允许上游接收读结果
        flag_result_ready = 1'b1;           // 打开结果ready
        @(posedge reg_clk);                 // 完成读结果握手
        @(negedge reg_clk);                 // 关闭结果ready
        flag_result_ready = 1'b0;           // 回到默认反压状态
        repeat(2)@(posedge reg_clk);        // 等待遥测计数稳定
        check_condition(cnt_accepted == cnt_success + cnt_cancelled_drain, "accepted conservation failed at drain"); // 无在途时守恒闭合
        check_condition(cnt_accepted == 4 && cnt_success == 2, "unexpected accepted or success count"); // 四次控制器接收两次成功

        coordinated_reset();                // 独立检查非法地址故障
        send_request(1'b0, 32'h04000000, 128'd0, 16'd0, 32'd20, 32'd20); // 提交越过端点的地址
        repeat(3)@(posedge reg_clk);        // 等待检查态进入故障
        check_condition(flag_protocol_fault, "out-of-range address did not fail closed"); // 非法地址必须闭锁
        check_condition(!flag_paxi_arvalid && !flag_paxi_awvalid, "invalid address reached PAXI"); // 不得向端点呈现

        coordinated_reset();                // 独立检查缺失RLAST故障
        send_request(1'b0, 32'h03400000, 128'd0, 16'd0, 32'd21, 32'd21); // 提交合法读事务
        @(posedge reg_clk);                 // 进入AR呈现阶段
        @(negedge reg_clk);                 // 打开读地址接收
        flag_paxi_arready = 1'b1;           // 接受AR
        @(posedge reg_clk);                 // 完成AR握手
        @(negedge reg_clk);                 // 提供违反合同的返回
        flag_paxi_arready = 1'b0;           // 关闭地址就绪
        flag_paxi_rvalid = 1'b1;            // 返回数据到达
        flag_paxi_rlast = 1'b0;             // 故意缺少唯一末拍
        @(posedge reg_clk);                 // 采样末拍错误
        @(negedge reg_clk);                 // 撤销错误返回
        flag_paxi_rvalid = 1'b0;            // 只注入一次错误
        repeat(3)@(posedge reg_clk);        // 等待采样故障闭锁状态
        check_condition(flag_protocol_fault, "missing RLAST did not fail closed"); // 末拍错误不得形成结果

        coordinated_reset();                // 独立检查无归属返回
        @(negedge reg_clk);                 // 在空闲态注入返回
        flag_paxi_rvalid = 1'b1;            // 返回没有任何owner
        flag_paxi_rlast = 1'b1;             // 即使末拍正确也无归属
        @(posedge reg_clk);                 // 采样意外返回
        @(negedge reg_clk);                 // 撤销意外返回
        flag_paxi_rvalid = 1'b0;            // 保持事件单拍
        flag_paxi_rlast = 1'b0;             // 清除末拍驱动
        repeat(3)@(posedge reg_clk);        // 等待故障状态生效
        check_condition(flag_protocol_fault, "unexpected return did not fail closed"); // 不得猜测owner

        coordinated_reset();                // 独立检查W同拍提交拒绝
        send_request(1'b1, 32'h03400030, 128'h55, 16'h0000, 32'd22, 32'd22); // 提交合法写事务
        @(posedge reg_clk);                 // 进入AW呈现阶段
        @(negedge reg_clk);                 // 允许AW接收
        flag_paxi_awready = 1'b1;           // 完成写地址握手
        @(posedge reg_clk);                 // 进入写数据阶段
        @(negedge reg_clk);                 // 在W采样沿前同时给出提交
        flag_paxi_awready = 1'b0;           // 关闭写地址ready
        flag_paxi_wready = 1'b1;            // 接收缓存写数据
        flag_commit_confirmed = 1'b1;       // 故意违反later事件规则
        @(posedge reg_clk);                 // 同拍采样W与过早提交
        @(negedge reg_clk);                 // 撤销两个单拍输入
        flag_paxi_wready = 1'b0;            // 防止重复W握手
        flag_commit_confirmed = 1'b0;       // 防止后续合法归属
        repeat(3)@(posedge reg_clk);        // 等待故障采样闭锁
        check_condition(flag_protocol_fault, "same-cycle W commit was not rejected"); // 该原型要求后续独立事件

        if(cnt_error == 0)begin
            $display(" > INFO: [Verilog] H1-B isolated PAXI bridge PASS"); // 仅全部比较成功后报告通过
            $finish;                        // 正常结束固定种子仿真
        end else begin
            $display(" > ERR: [Verilog] H1-B isolated PAXI bridge FAIL count=%0d", cnt_error); // 汇总失败数量
            $finish_and_return(1);          // 向调用脚本返回失败
        end
    end

    // 超时看门狗阻止悬挂仿真被误判成功
    initial begin
        repeat(500)@(posedge reg_clk);      // 覆盖全部定向场景的最大周期数
        $display(" > ERR: [Verilog] H1-B timeout"); // 输出明确的超时失败
        $finish_and_return(1);              // 超时必须返回非零状态
    end

    //------------模块实例化区域------------//
    // 被测单请求PAXI安全探针
    paxi_single_outstanding_bridge paxi_single_outstanding_bridge_Inst_dut(
        .i_clk(reg_clk),                    // 连接测试时钟
        .i_rstn(reg_rstn),                  // 连接协调硬复位
        .i_req_valid(flag_req_valid),       // 连接请求有效驱动
        .i_req_write(flag_req_write),       // 连接请求类型驱动
        .i_req_byte_addr(reg_req_byte_addr), // 连接请求地址驱动
        .i_req_write_data(reg_req_write_data), // 连接请求写载荷
        .i_req_write_mask(reg_req_write_mask), // 连接高有效屏蔽驱动
        .i_req_epoch(reg_req_epoch),        // 连接请求世代驱动
        .i_req_owner(reg_req_owner),        // 连接请求所有者驱动
        .i_cancel(flag_cancel),             // 连接全局单事务取消
        .o_req_ready(flag_req_ready),       // 观察本地请求就绪
        .i_commit_confirmed(flag_commit_confirmed), // 连接显式提交证明
        .i_result_ready(flag_result_ready), // 连接结果ready驱动
        .o_result_valid(flag_result_valid), // 观察结果有效
        .o_result_write(flag_result_write), // 观察结果读写类型
        .o_result_committed(flag_result_committed), // 观察写提交标志
        .o_result_epoch(result_epoch),      // 观察结果世代
        .o_result_owner(result_owner),      // 观察结果所有者
        .o_result_read_data(result_read_data), // 观察读返回数据
        .o_paxi_accepted_valid(flag_paxi_accepted_valid), // 观察控制器接收脉冲
        .o_paxi_accepted_write(flag_paxi_accepted_write), // 观察接收操作类型
        .o_paxi_accepted_epoch(paxi_accepted_epoch), // 观察接收世代
        .o_paxi_accepted_owner(paxi_accepted_owner), // 观察接收所有者
        .o_drain_done(flag_drain_done),     // 观察所有权排空状态
        .o_protocol_fault(flag_protocol_fault), // 观察粘滞协议故障
        .o_late_discard_count(cnt_late_discard), // 观察晚到丢弃计数
        .o_cancelled_drain_count(cnt_cancelled_drain), // 观察取消排空计数
        .i_paxi_arready(flag_paxi_arready), // 连接真实ARREADY模拟
        .o_paxi_arvalid(flag_paxi_arvalid), // 观察ARVALID保持
        .o_paxi_araddr(paxi_araddr),        // 观察PAXI读地址
        .i_paxi_awready(flag_paxi_awready), // 连接真实AWREADY模拟
        .o_paxi_awvalid(flag_paxi_awvalid), // 观察AWVALID保持
        .o_paxi_awaddr(paxi_awaddr),        // 观察PAXI写地址
        .i_paxi_wready(flag_paxi_wready),   // 连接真实WREADY模拟
        .o_paxi_wvalid(flag_paxi_wvalid),   // 观察AW后WVALID
        .o_paxi_wdata(paxi_wdata),          // 观察缓存写数据
        .o_paxi_wmask(paxi_wmask),          // 观察高有效写屏蔽
        .i_paxi_rvalid(flag_paxi_rvalid),   // 连接无READY返回有效
        .i_paxi_rlast(flag_paxi_rlast),     // 连接单拍返回末拍
        .i_paxi_rdata(reg_paxi_rdata)       // 连接模拟返回载荷
    );

endmodule
