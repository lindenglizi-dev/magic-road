`timescale 1ns / 1ps

////////////////////////////////////English///////////////////////////////////////
// Company:         Erie
// Engineer:        Erie
//
// Create Date:     2026/10/14 00:00:00
// Design Name:     road_paxi_mailbox
// Module Name:     tb_paxi_mailbox
// Description:     Directed asynchronous-clock regression for the PAXI mailbox
// Simulations:     ModelSim 2020.4 / tb_paxi_mailbox
//
// Referrences:
// File Format      File Name
// 1.Contract       mailbox_contract.json
//
// Dependencies:
// Module Name      Version
// road_paxi_mailbox V1.0
//
// Version:         V1.0
// Revision Date:   2026/10/14 00:00:00
// History:
// Time             Version     Revised by        Contents
// 2026/10/14       V1.0        Erie              Create file.
///////////////////////////////////Chinese////////////////////////////////////////
// 版权归属:        Erie
// 开发人员:        Erie
//
// 创建日期:        2026年10月14日
// 设计名称:        road_paxi_mailbox
// 模块名称:        tb_paxi_mailbox
// 模块说明:        PAXI邮箱异相时钟定向自检回归
// 仿真工程:        ModelSim 2020.4 / tb_paxi_mailbox
//
// 参考资料:
// 文件格式         文件名称
// 1.Contract       mailbox_contract.json
//
// 依赖文件:
// 模块名称         版本
// road_paxi_mailbox V1.0
//
// 当前版本:        V1.0
// 修订日期:        2026年10月14日
// 修订历史:
// 时间             版本        修订人            修订内容
// 2026年10月14日   V1.0        Erie              创建文件

module tb_paxi_mailbox;

	//---------------配置参数区域---------------//
	// 缩短超时以覆盖有限等待失败
	localparam [26:0] C_TB_TIMEOUT = 27'd8;     // 仿真专用端点超时拍数
	localparam [24:0] C_ADDR_A = 25'h1a00000;  // 合法保留区首地址
	localparam [24:0] C_ADDR_B = 25'h1a00008;  // 第二个合法原生地址
	localparam [127:0] C_DATA_A = 128'h00112233445566778899aabbccddeeff; // 第一组可辨识载荷
	localparam [127:0] C_DATA_B = 128'hffeeddccbbaa99887766554433221100; // 第二组可辨识载荷

	//-----------------时钟复位信号-------------//
	// 两个互质相位的独立仿真时钟
	reg i_clk = 1'b0;                          // 100MHz源域时钟驱动
	reg i_rstn = 1'b0;                         // 源域低有效复位驱动
	reg i_ddr_clk = 1'b0;                      // 约133.33MHz DDR域时钟驱动
	reg i_ddr_rstn = 1'b0;                     // DDR域低有效复位驱动
	reg i_phy_ready = 1'b0;                    // PHY就绪状态驱动

	//----------------源请求接口----------------//
	reg i_req_valid = 1'b0;                    // 源请求有效驱动
	reg i_req_write = 1'b0;                    // 源请求读写类型驱动
	reg [24:0] i_req_addr = 25'd0;             // 源请求原生地址驱动
	reg [127:0] i_req_data = 128'd0;           // 源请求写载荷驱动
	wire o_req_ready;                          // DUT请求接收能力

	//----------------源响应接口----------------//
	wire o_rsp_valid;                          // DUT源响应有效状态
	wire [127:0] o_rsp_data;                   // DUT源响应数据载荷
	wire [3:0] o_rsp_error;                    // DUT源响应错误分类
	reg i_rsp_ready = 1'b0;                    // 源响应消费驱动
	wire o_fault;                              // DUT源域粘滞故障观测

	//----------------PAXI端点信号--------------//
	// 写地址、写数据和读地址独立反压
	reg i_awready = 1'b0;                      // 模拟端点AW接收条件
	wire [24:0] o_awaddr;                      // DUT写地址输出
	wire o_awvalid;                            // DUT写地址有效状态
	reg i_wready = 1'b0;                       // 模拟端点W接收条件
	wire [127:0] o_wdata;                      // DUT写数据输出
	wire [15:0] o_wstrb;                       // DUT写掩码输出
	wire o_wvalid;                             // DUT写数据有效状态
	wire o_wlast;                              // DUT写数据末拍输出
	reg i_arready = 1'b0;                      // 模拟端点AR接收条件
	wire [24:0] o_araddr;                      // DUT读地址输出
	wire o_arvalid;                            // DUT读地址有效状态
	reg i_rvalid = 1'b0;                       // 模拟端点R有效驱动
	reg i_rlast = 1'b0;                        // 模拟端点R末拍驱动
	reg [127:0] i_rdata = 128'd0;              // 模拟端点R数据驱动
	wire o_rready;                             // DUT读返回接收能力

	//-----------------自检记录信号-------------//
	// 失败、守恒与稳定窗口记录
	integer cnt_error = 0;                     // 累计所有真实比较失败
	integer cnt_req_accept = 0;                // 当前复位世代源请求接受数
	integer cnt_rsp_consume = 0;               // 当前复位世代源响应消费数
	integer cnt_aw_accept = 0;                 // 当前复位世代AW接受数
	integer cnt_w_accept = 0;                  // 当前复位世代W接受数
	integer cnt_ar_accept = 0;                 // 当前复位世代AR接受数
	integer cnt_r_accept = 0;                  // 当前复位世代R接受数
	reg [24:0] reg_expected_req_addr = 25'd0;  // 接受时记录的冻结地址
	reg [127:0] reg_expected_req_data = 128'd0; // 接受时记录的冻结写数据
	reg reg_expected_req_write = 1'b0;         // 接受时记录的冻结操作类型
	reg flag_rsp_hold_seen = 1'b0;             // 响应反压稳定检查已经取样
	reg [127:0] reg_rsp_hold_data = 128'd0;     // 响应反压首拍数据快照
	reg [3:0] reg_rsp_hold_error = 4'd0;        // 响应反压首拍错误快照

	//-----------------时钟生成区域-------------//
	// 100MHz源域时钟持续运行
	always #5.0 i_clk = !i_clk;                 // 十纳秒周期形成100MHz

	// 约133.33MHz DDR域时钟使用异相边沿
	always #3.75 i_ddr_clk = !i_ddr_clk;        // 七点五纳秒周期形成目标频率

	//-----------------在线检查区域-------------//
	// 每个共同复位世代独立统计请求响应守恒
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			cnt_req_accept = 0;                    // 新复位世代从零统计请求
			cnt_rsp_consume = 0;                   // 新复位世代从零统计响应
			reg_expected_req_addr = 25'd0;         // 清除旧地址期望
			reg_expected_req_data = 128'd0;        // 清除旧数据期望
			reg_expected_req_write = 1'b0;         // 清除旧类型期望
		end else begin
			if(i_req_valid && o_req_ready)begin
				cnt_req_accept = cnt_req_accept + 1; // 每次源请求握手只计一次
				reg_expected_req_addr = i_req_addr; // 保存源域保持窗口期望
				reg_expected_req_data = i_req_data; // 保存源域数据保持期望
				reg_expected_req_write = i_req_write; // 保存源域类型保持期望
			end
			if(o_rsp_valid && i_rsp_ready)begin
				cnt_rsp_consume = cnt_rsp_consume + 1; // 只按真实响应握手计数
			end
		end
	end

	// DDR端点各通道按真实握手分别计数
	always@(posedge i_ddr_clk or negedge i_ddr_rstn)begin
		if(i_ddr_rstn == 1'b0)begin
			cnt_aw_accept = 0;                     // 新复位世代清除AW计数
			cnt_w_accept = 0;                      // 新复位世代清除W计数
			cnt_ar_accept = 0;                     // 新复位世代清除AR计数
			cnt_r_accept = 0;                      // 新复位世代清除R计数
		end else begin
			if(o_awvalid && i_awready) cnt_aw_accept = cnt_aw_accept + 1; // AW握手守恒
			if(o_wvalid && i_wready) cnt_w_accept = cnt_w_accept + 1; // W握手守恒
			if(o_arvalid && i_arready) cnt_ar_accept = cnt_ar_accept + 1; // AR握手守恒
			if(o_rready && i_rvalid) cnt_r_accept = cnt_r_accept + 1; // R握手守恒
		end
	end

	// 源请求槽在完整响应消费前不得变化
	always@(negedge i_clk)begin
		if(i_rstn && road_paxi_mailbox_Inst.flag_source_busy)begin
			if((road_paxi_mailbox_Inst.reg_req_addr_hold_src !== reg_expected_req_addr) ||
				(road_paxi_mailbox_Inst.reg_req_data_hold_src !== reg_expected_req_data) ||
				(road_paxi_mailbox_Inst.reg_req_write_hold_src !== reg_expected_req_write))begin
				cnt_error = cnt_error + 1;           // 冻结请求变化即违反CDC合同
				$display(" > ERR: [Verilog] source request payload changed before response consumption");
			end
		end
	end

	// 源响应在反压期间保持全部载荷稳定
	always@(negedge i_clk)begin
		if(!i_rstn || !o_rsp_valid)begin
			flag_rsp_hold_seen = 1'b0;             // 无有效响应时准备下一次快照
		end else if(!flag_rsp_hold_seen)begin
			flag_rsp_hold_seen = 1'b1;             // 首个有效半拍建立稳定基线
			reg_rsp_hold_data = o_rsp_data;        // 记录完整响应数据
			reg_rsp_hold_error = o_rsp_error;      // 记录完整错误分类
		end else if((o_rsp_data !== reg_rsp_hold_data) || (o_rsp_error !== reg_rsp_hold_error))begin
			cnt_error = cnt_error + 1;             // ready到达前响应不得变化
			$display(" > ERR: [Verilog] response payload changed under backpressure");
		end
	end

	//-----------------辅助任务区域-------------//
	// 记录一个带场景名的自检失败
	task fail_case;
		input [8*80-1:0] text;                   // 失败原因的定长ASCII描述
		begin
			cnt_error = cnt_error + 1;             // 所有失败汇入唯一退出判定
			$display(" > ERR: [Verilog] %0s", text); // 输出可检索失败原因
		end
	endtask

	// 同时断言两域复位并在各自安全边沿释放
	task common_reset;
		begin
			i_rstn = 1'b0;                         // 异步清除源域所有权
			i_ddr_rstn = 1'b0;                     // 同拍异步清除DDR域所有权
			i_phy_ready = 1'b0;                    // 复位期间端点不可用
			i_req_valid = 1'b0;                    // 复位期间不提出源请求
			i_rsp_ready = 1'b0;                    // 复位期间不消费响应
			i_awready = 1'b0;                      // 复位期间关闭AW端点
			i_wready = 1'b0;                       // 复位期间关闭W端点
			i_arready = 1'b0;                      // 复位期间关闭AR端点
			i_rvalid = 1'b0;                       // 复位期间不返回数据
			i_rlast = 1'b0;                        // 复位期间无返回末拍
			i_rdata = 128'd0;                      // 复位期间返回总线清零
			#31;                                   // 覆盖两个时钟的多个有效边沿
			@(negedge i_clk) i_rstn = 1'b1;       // 源域在本地低相位同步释放
			@(negedge i_ddr_clk) i_ddr_rstn = 1'b1; // DDR域在本地低相位同步释放
			i_phy_ready = 1'b1;                    // 两域释放后开放真实端点
			repeat(4) @(posedge i_clk);            // 等待故障同步链稳定为零
			if(o_rsp_valid || o_fault) fail_case("common reset leaked an old response or fault"); // 共同复位必须清除旧结果
		end
	endtask

	// 在源域完成唯一请求握手
	task send_request;
		input req_write;                         // 本次请求的读写类型
		input [24:0] req_addr;                   // 本次请求的原生地址
		input [127:0] req_data;                  // 本次请求的写数据
		begin
			@(negedge i_clk);                      // 只在源时钟低相位开始驱动请求
			while(!o_req_ready) @(negedge i_clk);  // 等待唯一槽确实释放
			i_req_write = req_write;               // 握手前设置稳定操作类型
			i_req_addr = req_addr;                 // 握手前设置稳定地址
			i_req_data = req_data;                 // 握手前设置稳定数据
			i_req_valid = 1'b1;                    // 保持valid跨越一个有效边沿
			@(negedge i_clk) i_req_valid = 1'b0;   // 已接受后撤销源请求
		end
	endtask

	// 无额外停顿地依次接受AW与下一拍W
	task accept_write_together;
		begin
			while(!o_awvalid) @(negedge i_ddr_clk); // 等待AW首次提出
			if(o_wvalid) fail_case("WVALID preceded AW acceptance"); // 厂商路径禁止W先行
			i_awready = 1'b1;                      // 本拍完成AW握手
			@(negedge i_ddr_clk);                  // AW接受后的下一拍观察W
			i_awready = 1'b0;                      // 地址已接受后撤销ready
			if(o_awvalid || !o_wvalid) fail_case("WVALID was not presented immediately after AW acceptance"); // 不插入额外gap
			if((o_wstrb !== 16'h0000) || !o_wlast) fail_case("write sideband contract mismatch"); // 检查掩码与末拍
			i_wready = 1'b1;                       // 首个W有效拍立即接受
			@(negedge i_ddr_clk) i_wready = 1'b0;  // 一个上升沿后关闭W
		end
	endtask

	// 分别反压AW和W并检查两阶段保持
	task accept_write_split;
		reg [24:0] held_addr;                    // AW反压期间的地址基线
		reg [127:0] held_data;                   // W反压期间的数据基线
		begin
			while(!o_awvalid) @(negedge i_ddr_clk); // 等待AW首次提出
			held_addr = o_awaddr;                  // 保存地址反压基线
			repeat(2)begin
				@(negedge i_ddr_clk);                // 延长AW通道反压窗口
				if(!o_awvalid || o_wvalid || (o_awaddr !== held_addr)) fail_case("AW hold changed or W preceded AW acceptance"); // AW阶段不得提前W
			end
			i_awready = 1'b1;                      // 先只接受AW
			@(negedge i_ddr_clk) i_awready = 1'b0; // 一个上升沿后关闭AW
			if(!o_wvalid) fail_case("stalled write did not present W on the next cycle"); // AW后不额外延迟
			held_data = o_wdata;                   // 保存W反压前写数据
			repeat(2)begin
				@(negedge i_ddr_clk);                // 延长W通道反压窗口
				if(!o_wvalid || (o_wdata !== held_data)) fail_case("W payload did not remain stable after AW acceptance"); // W必须独立保持
			end
			i_wready = 1'b1;                       // 最后单独接受W
			@(negedge i_ddr_clk) i_wready = 1'b0;  // 一个上升沿后关闭W
		end
	endtask

	// 接受AR并在同一边沿返回完整读数据
	task return_same_edge;
		input [127:0] data;                      // 同拍返回的预期数据
		input last;                              // 同拍返回的末拍值
		begin
			while(!o_arvalid) @(negedge i_ddr_clk); // 等待读地址真实提出
			i_arready = 1'b1;                      // 本拍接受AR
			i_rvalid = 1'b1;                       // 同一拍提供读返回
			i_rlast = last;                        // 驱动本场景末拍状态
			i_rdata = data;                        // 驱动本场景返回数据
			#0.001;                                // 等待组合rready传播一个仿真精度
			if(!o_rready) fail_case("AR same-edge response did not reserve R capacity"); // 同拍必须ready
			@(negedge i_ddr_clk);                  // 让同一个上升沿完成AR和R
			i_arready = 1'b0;                      // 防止重复AR接收
			i_rvalid = 1'b0;                       // 单拍返回后撤销有效
			i_rlast = 1'b0;                        // 返回空闲值
			i_rdata = 128'd0;                      // 返回总线恢复空闲
		end
	endtask

	// 先接受AR，再延迟若干拍提供返回
	task return_delayed;
		input [127:0] data;                      // 延迟返回的预期数据
		input last;                              // 延迟返回的末拍值
		input integer delay_cycles;              // AR后延迟的DDR拍数
		integer index;                           // 延迟循环索引
		begin
			while(!o_arvalid) @(negedge i_ddr_clk); // 等待读地址有效
			i_arready = 1'b1;                      // 允许一个AR握手
			@(negedge i_ddr_clk) i_arready = 1'b0; // 地址接受后立即反压
			for(index = 0; index < delay_cycles; index = index + 1)begin
				@(negedge i_ddr_clk);                // 构造有限随机样式延迟
			end
			i_rvalid = 1'b1;                       // 提供唯一读返回
			i_rlast = last;                        // 驱动返回末拍属性
			i_rdata = data;                        // 驱动返回数据载荷
			if(!o_rready) fail_case("delayed read response arrived without reserved capacity"); // AR后必须持续ready
			@(negedge i_ddr_clk);                  // 让一个上升沿接受返回
			i_rvalid = 1'b0;                       // 单拍返回后撤销有效
			i_rlast = 1'b0;                        // 清除末拍驱动
			i_rdata = 128'd0;                      // 清除返回数据驱动
		end
	endtask

	// 检查响应并完成源端消费
	task consume_response;
		input [127:0] expected_data;             // 期望的完整响应数据
		input [3:0] expected_error;              // 期望的响应错误分类
		input integer backpressure_cycles;       // 消费前保持的源时钟拍数
		integer index;                           // 反压循环索引
		begin
			while(!o_rsp_valid) @(negedge i_clk);   // 等待跨域复制完整完成
			for(index = 0; index < backpressure_cycles; index = index + 1)begin
				@(negedge i_clk);                    // 延长源端响应反压
				if((o_rsp_data !== expected_data) || (o_rsp_error !== expected_error)) fail_case("response payload mismatch under source backpressure"); // 每拍检查稳定值
			end
			if((o_rsp_data !== expected_data) || (o_rsp_error !== expected_error)) fail_case("response payload mismatch before consumption"); // 消费前最终比较
			i_rsp_ready = 1'b1;                    // 允许一个源响应握手
			@(negedge i_clk) i_rsp_ready = 1'b0;   // 一个上升沿后撤销ready
			repeat(6) @(posedge i_clk);            // 等待确认跨回DDR并释放状态
		end
	endtask

	// 等待同步故障并验证不再接受请求
	task expect_fault;
		integer watchdog;                        // 有界等待源域故障同步
		begin
			watchdog = 0;                          // 从零开始等待故障传播
			while(!o_fault && watchdog < 20)begin
				@(posedge i_clk);                    // 按源时钟观察两级同步结果
				watchdog = watchdog + 1;             // 防止仿真无限等待
			end
			if(!o_fault) fail_case("sticky fault did not reach source domain"); // 必须在有界同步延迟内到达
			if(o_req_ready) fail_case("faulted mailbox accepted a new request"); // 故障后禁止槽复用
		end
	endtask

	//----------------DUT实例化区域-------------//
	// 被测模块使用缩短的仿真超时参数
	road_paxi_mailbox #(
		.C_TIMEOUT(C_TB_TIMEOUT)                 // 仅测试覆盖使用八拍超时
	) road_paxi_mailbox_Inst (
		.i_clk(i_clk),                           // 连接100MHz源域时钟
		.i_rstn(i_rstn),                         // 连接源域共同复位分支
		.i_ddr_clk(i_ddr_clk),                   // 连接异相DDR用户时钟
		.i_ddr_rstn(i_ddr_rstn),                 // 连接DDR域共同复位分支
		.i_phy_ready(i_phy_ready),               // 连接PHY就绪状态
		.i_req_valid(i_req_valid),               // 连接源请求有效驱动
		.i_req_write(i_req_write),               // 连接源请求读写类型
		.i_req_addr(i_req_addr),                 // 连接源请求原生地址
		.i_req_data(i_req_data),                 // 连接源请求写数据
		.o_req_ready(o_req_ready),               // 观察源请求接收能力
		.o_rsp_valid(o_rsp_valid),               // 观察源响应有效状态
		.o_rsp_data(o_rsp_data),                 // 观察源响应完整数据
		.o_rsp_error(o_rsp_error),               // 观察源响应错误分类
		.i_rsp_ready(i_rsp_ready),               // 连接源响应消费驱动
		.o_fault(o_fault),                       // 观察源域粘滞故障
		.i_awready(i_awready),                   // 连接模拟AW端点ready
		.i_wready(i_wready),                     // 连接模拟W端点ready
		.i_arready(i_arready),                   // 连接模拟AR端点ready
		.i_rvalid(i_rvalid),                     // 连接模拟R端点valid
		.i_rlast(i_rlast),                       // 连接模拟R端点末拍
		.i_rdata(i_rdata),                       // 连接模拟R端点数据
		.o_awaddr(o_awaddr),                     // 观察冻结写地址
		.o_araddr(o_araddr),                     // 观察冻结读地址
		.o_wdata(o_wdata),                       // 观察冻结写数据
		.o_wstrb(o_wstrb),                       // 观察控制器写掩码
		.o_awvalid(o_awvalid),                   // 观察AW通道有效状态
		.o_wvalid(o_wvalid),                     // 观察W通道有效状态
		.o_wlast(o_wlast),                       // 观察W通道末拍状态
		.o_arvalid(o_arvalid),                   // 观察AR通道有效状态
		.o_rready(o_rready)                      // 观察R通道接收能力
	);

	//-----------------主测试流程---------------//
	// 顺序覆盖成功、反压、错误、超时和共同复位位置
	initial begin
		$display(" > INFO: [Verilog] start asynchronous PAXI mailbox regression"); // 标记回归开始

		common_reset();                          // 建立第一个干净复位世代
		send_request(1'b1, C_ADDR_A, C_DATA_A);  // normal写请求
		accept_write_together();                 // AW后下一拍立即接受W
		consume_response(128'd0, 4'd0, 0);       // 写响应不表示提交且数据为零
		if((cnt_req_accept != 1) || (cnt_rsp_consume != 1) || (cnt_aw_accept != 1) || (cnt_w_accept != 1)) fail_case("normal write conservation mismatch"); // 检查一次性守恒

		send_request(1'b1, C_ADDR_B, C_DATA_B);  // split_aw_w写请求
		accept_write_split();                    // 分别反压并完成AW和W
		consume_response(128'd0, 4'd0, 16);      // long_response_backpressure
		if((cnt_req_accept != 2) || (cnt_rsp_consume != 2) || (cnt_aw_accept != 2) || (cnt_w_accept != 2)) fail_case("split write conservation mismatch"); // 检查双写无重复

		send_request(1'b0, C_ADDR_A, 128'd0);    // ARsameedge读请求
		return_same_edge(C_DATA_A, 1'b1);        // AR与R在同一边沿完成
		consume_response(C_DATA_A, 4'd0, 3);     // 检查读数据跨域冻结
		if((cnt_ar_accept != 1) || (cnt_r_accept != 1)) fail_case("same-edge read conservation mismatch"); // 同拍仍只计一次

		send_request(1'b0, C_ADDR_B, 128'd0);    // randomstalls读请求
		repeat(3) @(negedge i_ddr_clk);          // 构造AR随机样式反压
		return_delayed(C_DATA_B, 1'b1, 3);       // AR后再次随机样式延迟R
		consume_response(C_DATA_B, 4'd0, 1);     // 消费延迟返回数据
		if((cnt_req_accept != 4) || (cnt_rsp_consume != 4) || (cnt_ar_accept != 2) || (cnt_r_accept != 2)) fail_case("asynchronous request conservation mismatch"); // 四请求四响应无丢失重复

		common_reset();                          // 地址边界用例使用独立故障世代
		send_request(1'b0, C_ADDR_A + 1'b1, 128'd0); // 发出未按原生步长对齐的请求
		consume_response(128'd0, 4'b0001, 0);    // 地址错误不得到达PAXI端点
		if(o_awvalid || o_wvalid || o_arvalid) fail_case("invalid address reached the PAXI endpoint"); // 非法请求不得外发
		expect_fault();                          // 地址错误同样保持到共同复位

		common_reset();                          // bad_rlast前清空成功世代
		send_request(1'b0, C_ADDR_A, 128'd0);    // 发出错误末拍读请求
		return_delayed(C_DATA_A, 1'b0, 1);       // 返回数据但缺少RLAST
		consume_response(128'd0, 4'b0100, 0);    // 仅报告RLAST错误且不泄漏数据
		expect_fault();                          // 错误必须粘滞至共同复位

		common_reset();                          // unsolicited前清除粘滞故障
		@(negedge i_ddr_clk);                    // 在端点空闲期制造意外返回
		i_rvalid = 1'b1;                         // 无AR所有者仍驱动RVALID
		i_rlast = 1'b1;                          // 即使RLAST正确仍属意外
		i_rdata = C_DATA_B;                      // 使用可辨识旧结果模式
		@(negedge i_ddr_clk) i_rvalid = 1'b0;    // 一个边沿后撤销意外返回
		i_rlast = 1'b0;                          // 清除意外末拍驱动
		i_rdata = 128'd0;                        // 清除意外数据驱动
		expect_fault();                          // 无请求返回直接闭锁
		if(o_rsp_valid) fail_case("unsolicited return created a source response"); // 无所有者不得伪造响应

		common_reset();                          // 空闲PHY掉线使用独立复位世代
		repeat(3) @(posedge i_ddr_clk);          // 先让DDR域记录PHY已经建立
		i_phy_ready = 1'b0;                      // 无在途请求时模拟真实PHY掉线
		expect_fault();                          // 空闲掉线同样必须粘滞
		if(o_rsp_valid) fail_case("idle PHY loss created a source response"); // 无请求所有者不得伪造响应

		common_reset();                          // PHYlost前恢复空闲状态
		send_request(1'b0, C_ADDR_A, 128'd0);    // 发出合法读请求
		while(!o_arvalid) @(negedge i_ddr_clk);  // 等待AR已经提出
		i_phy_ready = 1'b0;                      // 请求拥有期间模拟PHY掉线
		consume_response(128'd0, 4'b0010, 0);    // 报告PHY错误且不重试
		expect_fault();                          // PHY错误保持至共同复位

		common_reset();                          // timeout前恢复端点
		send_request(1'b1, C_ADDR_A, C_DATA_B);  // 发出写请求但永久反压端点
		consume_response(128'd0, 4'b1000, 0);    // 八拍后报告超时错误
		expect_fault();                          // 超时必须闭锁后续请求

		common_reset();                          // commonreset写中位置覆盖
		send_request(1'b1, C_ADDR_B, C_DATA_A);  // 发出写请求
		while(!o_awvalid) @(negedge i_ddr_clk);  // 等待AW提出且W尚未允许
		i_awready = 1'b1;                        // 只接受AW后立即共同复位
		@(negedge i_ddr_clk) i_awready = 1'b0;   // 完成一次AW握手
		common_reset();                          // 取消半完成写且清除所有世代
		if(o_awvalid || o_wvalid || o_rsp_valid) fail_case("reset during split write leaked activity"); // 复位后不得延续半事务

		send_request(1'b0, C_ADDR_A, 128'd0);    // commonreset读等待位置覆盖
		while(!o_arvalid) @(negedge i_ddr_clk);  // 等待AR提出
		i_arready = 1'b1;                        // 接受AR进入返回等待
		@(negedge i_ddr_clk) i_arready = 1'b0;   // 完成唯一AR握手
		common_reset();                          // 取消等待返回的读事务
		if(o_rready || o_rsp_valid) fail_case("reset during read wait leaked reserved response"); // 不保留旧返回槽

		send_request(1'b0, C_ADDR_B, 128'd0);    // commonreset响应保持位置覆盖
		return_same_edge(C_DATA_B, 1'b1);        // 产生一个尚未消费的完整响应
		while(!o_rsp_valid) @(negedge i_clk);     // 确认响应已经到达源域
		common_reset();                          // 在响应反压期间共同复位
		if(o_rsp_valid || (o_rsp_data !== 128'd0) || (o_rsp_error !== 4'd0)) fail_case("common reset did not clear stale response payload"); // 无旧结果泄漏

		send_request(1'b0, C_ADDR_A, 128'd0);    // 复位后发出新读证明世代恢复
		return_delayed(C_DATA_A, 1'b1, 1);       // 返回与旧结果不同的确定值
		consume_response(C_DATA_A, 4'd0, 0);     // 新结果必须独立正确
		if((cnt_req_accept != 1) || (cnt_rsp_consume != 1)) fail_case("post-reset request conservation mismatch"); // 最终世代一进一出

		if(cnt_error == 0)begin
			$display(" > INFO: [Verilog] PASS tb_paxi_mailbox"); // 只有全部比较执行且无失败才通过
			$display("VERILOG-GEN-RESULT: PASS"); // 输出机器可检索成功标记
		end else begin
			$display(" > ERR: [Verilog] FAIL tb_paxi_mailbox errors=%0d", cnt_error); // 汇总真实失败数量
			$display("VERILOG-GEN-RESULT: FAIL"); // 输出机器可检索失败标记
		end
		$finish;                                 // 完成全部定向回归后退出
	end

	// 仿真看门狗防止任一握手场景永久悬挂
	initial begin
		#20000;                                  // 覆盖所有有限超时和跨域等待
		fail_case("simulation watchdog expired"); // 超时必须形成明确失败
		$display("VERILOG-GEN-RESULT: FAIL");   // 看门狗路径输出机器失败标记
		$finish;                                 // 终止悬挂仿真
	end

endmodule
