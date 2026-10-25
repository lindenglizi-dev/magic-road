`timescale 1ns / 1ps

////////////////////////////////////English///////////////////////////////////////
// Company:         Erie
// Engineer:        Erie
//
// Create Date:     2026/10/14 00:00:00
// Design Name:     road_paxi_mailbox
// Module Name:     road_paxi_mailbox
// Description:     One-slot frozen CDC mailbox with a native PAXI endpoint
// Simulations:     ModelSim 2020.4 / tb_paxi_mailbox
//
// Referrences:
// File Format      File Name
// 1.Contract       mailbox_contract.json
//
// Dependencies:
// Module Name      Version
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
// 模块名称:        road_paxi_mailbox
// 模块说明:        单槽冻结CDC邮箱与原生PAXI有限端点
// 仿真工程:        ModelSim 2020.4 / tb_paxi_mailbox
//
// 参考资料:
// 文件格式         文件名称
// 1.Contract       mailbox_contract.json
//
// 依赖文件:
// 模块名称         版本
//
// 当前版本:        V1.0
// 修订日期:        2026年10月14日
// 修订历史:
// 时间             版本        修订人            修订内容
// 2026年10月14日   V1.0        Erie              创建文件

module road_paxi_mailbox #(
	parameter [26:0] C_TIMEOUT = 27'h7ffffff // DDR端点一次事务的最大等待拍数
)(
	//-----------------全局信号-----------------//
	input i_clk,                                // 100MHz请求源时钟
	input i_rstn,                               // 源域低有效复位，必须与DDR域共同断言
	input i_ddr_clk,                            // 约133.33MHz的DDR用户时钟
	input i_ddr_rstn,                           // DDR域低有效复位，必须与源域共同断言
	input i_phy_ready,                          // DDR PHY已完成初始化且持续可用

	//----------------源请求接口----------------//
	input i_req_valid,                          // 请求有效，等待ready期间载荷由上游保持
	input i_req_write,                          // 高电平选择写事务，低电平选择读事务
	input [24:0] i_req_addr,                    // 原生PAXI地址，合法步长为八
	input [127:0] i_req_data,                   // 单拍写入的完整128位载荷
	output o_req_ready,                         // 无在途事务且无故障时允许接收

	//----------------源响应接口----------------//
	output o_rsp_valid,                         // 完整响应已复制并保持至源端消费
	output [127:0] o_rsp_data,                  // 单拍读数据，写响应固定为零
	output [3:0] o_rsp_error,                   // 地址、PHY、RLAST、协议或超时分类
	input i_rsp_ready,                          // 源端确认已消费冻结响应
	output o_fault,                             // 任一端点错误的源域粘滞观测

	//---------------PAXI写地址通道-------------//
	input i_awready,                            // DDR控制器写地址接收条件
	output [24:0] o_awaddr,                     // 冻结请求中的原生写地址
	output o_awvalid,                           // 写地址持续呈现至独立握手

	//---------------PAXI写数据通道-------------//
	input i_wready,                             // DDR控制器写数据接收条件
	output [127:0] o_wdata,                     // 冻结请求中的128位写数据
	output [15:0] o_wstrb,                      // 当前控制器约定的全零高有效掩码
	output o_wvalid,                            // 写数据持续呈现至独立握手
	output o_wlast,                             // 唯一写数据拍的末拍标志

	//---------------PAXI读地址通道-------------//
	input i_arready,                            // DDR控制器读地址接收条件
	output [24:0] o_araddr,                     // 冻结请求中的原生读地址
	output o_arvalid,                           // 读地址持续呈现至真实握手

	//---------------PAXI读返回通道-------------//
	input i_rvalid,                             // DDR控制器返回一拍128位数据
	input i_rlast,                              // 单拍读返回必须同时声明末拍
	input [127:0] i_rdata,                      // 原生PAXI读返回载荷
	output o_rready                             // 预留返回槽后允许接收读数据
);

	//---------------配置参数区域---------------//
	// 原生地址保留区与四类响应错误
	localparam [24:0] C_ADDR_FIRST = 25'h1a00000; // CNN独占原生地址下界
	localparam [25:0] C_ADDR_LIMIT = 26'h2000000; // CNN独占原生地址开区间上界
	localparam [3:0] C_ERR_ADDR = 4'b0001;     // 地址越界或未按八对齐
	localparam [3:0] C_ERR_PHY = 4'b0010;      // 已拥有请求期间PHY掉线
	localparam [3:0] C_ERR_LAST = 4'b0100;     // 读返回未携带RLAST
	localparam [3:0] C_ERR_PROTOCOL = 4'b1000; // 意外返回或端点等待超时

	//---------------状态参数区域---------------//
	// DDR域单在途事务阶段
	localparam [2:0] ST_IDLE = 3'd0;           // 等待跨域请求toggle
	localparam [2:0] ST_CHECK = 3'd1;          // 校验冻结地址与PHY状态
	localparam [2:0] ST_WRITE_ADDR = 3'd2;     // 保持AW直到控制器接受
	localparam [2:0] ST_WRITE_DATA = 3'd3;     // AW接受后一拍开始保持W
	localparam [2:0] ST_READ_ADDR = 3'd4;      // 提出AR并允许同拍返回
	localparam [2:0] ST_READ_DATA = 3'd5;      // 等待唯一完整读返回
	localparam [2:0] ST_RESPONSE = 3'd6;       // 冻结响应直至源端消费确认
	localparam [2:0] ST_FAULT = 3'd7;          // 粘滞故障后的静止终态

	//----------------状态机信号----------------//
	// DDR端点控制状态
	reg [2:0] state_current = ST_IDLE;         // 当前PAXI事务阶段
	reg [2:0] state_next = ST_IDLE;            // 下一PAXI事务阶段

	//-----------------请求CDC信号--------------//
	// 源域冻结槽与请求toggle
	reg flag_source_busy = 1'b0;               // 从请求接受到响应消费保持占用
	reg reg_req_write_hold_src = 1'b0;         // 源域冻结的读写类型
	reg [24:0] reg_req_addr_hold_src = 25'd0;  // 源域冻结的原生地址
	reg [127:0] reg_req_data_hold_src = 128'd0; // 源域冻结的写载荷
	reg req_toggle_src = 1'b0;                 // 每次源请求接受后翻转

	// DDR域两级请求同步器与复制槽
	(* ASYNC_REG = "TRUE" *) reg req_toggle_meta_ddr = 1'b0; // 请求toggle第一级同步寄存器
	(* ASYNC_REG = "TRUE" *) reg req_toggle_sync_ddr = 1'b0; // 请求toggle第二级同步寄存器
	reg req_toggle_seen_ddr = 1'b0;            // DDR域最后复制的请求世代
	reg reg_req_write_ddr = 1'b0;              // DDR域复制后的读写类型
	reg [24:0] reg_req_addr_ddr = 25'd0;       // DDR域复制后的稳定地址
	reg [127:0] reg_req_data_ddr = 128'd0;     // DDR域复制后的稳定写数据

	//----------------响应CDC信号---------------//
	// DDR域冻结响应与发布toggle
	reg [127:0] reg_rsp_data_hold_ddr = 128'd0; // DDR域冻结的完整响应数据
	reg [3:0] reg_rsp_error_hold_ddr = 4'd0;   // DDR域冻结的响应错误分类
	reg rsp_toggle_ddr = 1'b0;                 // 每次完整响应发布后翻转

	// 源域两级响应同步器与输出槽
	(* ASYNC_REG = "TRUE" *) reg rsp_toggle_meta_src = 1'b0; // 响应toggle第一级同步寄存器
	(* ASYNC_REG = "TRUE" *) reg rsp_toggle_sync_src = 1'b0; // 响应toggle第二级同步寄存器
	reg rsp_toggle_seen_src = 1'b0;            // 源域最后复制的响应世代
	reg rsp_ack_toggle_src = 1'b0;             // 响应消费后返回对应世代
	reg rsp_valid_o = 1'b0;                    // 源域冻结响应有效状态
	reg [127:0] rsp_data_o = 128'd0;           // 源域复制后的响应数据
	reg [3:0] rsp_error_o = 4'd0;              // 源域复制后的响应错误

	// DDR域两级响应确认同步器
	(* ASYNC_REG = "TRUE" *) reg rsp_ack_meta_ddr = 1'b0; // 响应确认第一级同步寄存器
	(* ASYNC_REG = "TRUE" *) reg rsp_ack_sync_ddr = 1'b0; // 响应确认第二级同步寄存器

	//-----------------端点任务信号-------------//
	// DDR域端点等待与故障状态
	reg [26:0] cnt_timeout = 27'd0;            // 当前端点事务累计等待拍数
	reg flag_phy_seen_ddr = 1'b0;              // PHY曾经进入可用状态
	reg flag_fault_ddr = 1'b0;                 // DDR域协议或端点粘滞故障

	// 源域故障同步器
	(* ASYNC_REG = "TRUE" *) reg fault_meta_src = 1'b0; // 故障状态第一级同步寄存器
	(* ASYNC_REG = "TRUE" *) reg fault_sync_src = 1'b0; // 故障状态第二级同步寄存器

	//-----------------组合判定信号-------------//
	// 请求、地址、握手与异常事件
	wire flag_req_arrive_ddr;                  // DDR域观察到未复制的新请求
	wire flag_addr_valid;                      // 冻结地址属于保留区且八对齐
	wire flag_timeout_hit;                     // 当前累计等待达到参数上限
	wire flag_phy_lost;                        // 已就绪PHY随后掉线
	wire flag_ar_accept;                       // 本拍实际完成AR握手
	wire flag_expected_r;                      // 返回属于已发出或同拍接受的AR
	wire flag_unexpected_r;                    // 返回不属于当前唯一读请求

	//---------------输出信号连线---------------//
	// 源域请求和响应接口
	assign o_req_ready = i_rstn && !flag_source_busy && !fault_sync_src; // 复位期间关闭准入，释放后只在完整空闲且无故障时接收
	assign o_rsp_valid = rsp_valid_o;           // 导出源域冻结响应有效位
	assign o_rsp_data = rsp_data_o;             // 导出源域稳定响应载荷
	assign o_rsp_error = rsp_error_o;           // 导出源域稳定错误分类
	assign o_fault = fault_sync_src;            // 两级同步后报告DDR粘滞故障

	// PAXI写通道保持独立有效状态
	assign o_awaddr = reg_req_addr_ddr;         // AW反压期间使用DDR域冻结地址
	assign o_awvalid = state_current == ST_WRITE_ADDR; // 未握手前持续呈现AW
	assign o_wdata = reg_req_data_ddr;          // W反压期间使用DDR域冻结数据
	assign o_wstrb = 16'h0000;                  // 原控制器高有效掩码约定为全零
	assign o_wvalid = state_current == ST_WRITE_DATA; // AW接受后的下一拍开始呈现W
	assign o_wlast = o_wvalid;                  // 唯一写数据拍始终同时声明末拍

	// PAXI读通道为同拍返回预留容量
	assign o_araddr = reg_req_addr_ddr;         // AR反压期间使用DDR域冻结地址
	assign o_arvalid = state_current == ST_READ_ADDR; // 直到ARREADY才撤销地址
	assign o_rready = (state_current == ST_READ_DATA) || ((state_current == ST_READ_ADDR) && i_arready); // AR接受当拍即可接收R

	//---------------其他信号连线---------------//
	// 组合事件保持单一明确含义
	assign flag_req_arrive_ddr = req_toggle_sync_ddr != req_toggle_seen_ddr; // 世代不同表示冻结请求待复制
	assign flag_addr_valid = ({1'b0, reg_req_addr_ddr} >= {1'b0, C_ADDR_FIRST}) && ({1'b0, reg_req_addr_ddr} < C_ADDR_LIMIT) && (reg_req_addr_ddr[2:0] == 3'b000); // 范围与原生步长同时合法
	assign flag_timeout_hit = cnt_timeout >= (C_TIMEOUT - 1'b1); // 参数拍数到达后终止等待
	assign flag_phy_lost = flag_phy_seen_ddr && !i_phy_ready; // 只把已建立后的掉线视为故障
	assign flag_ar_accept = o_arvalid && i_arready; // ARVALID和ARREADY共同构成接收
	assign flag_expected_r = (state_current == ST_READ_DATA) || ((state_current == ST_READ_ADDR) && flag_ar_accept); // 唯一读或AR同拍返回有归属
	assign flag_unexpected_r = i_rvalid && !flag_expected_r; // 其他任何RVALID均为协议故障

	//-------------源域CDC任务处理区域----------//
	// 接受请求时冻结载荷，直到对应响应真正消费
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_source_busy <= 1'b0;              // 共同复位取消旧事务所有权
			reg_req_write_hold_src <= 1'b0;        // 共同复位清除旧读写类型
			reg_req_addr_hold_src <= 25'd0;        // 共同复位清除旧地址
			reg_req_data_hold_src <= 128'd0;       // 共同复位清除旧写数据
			req_toggle_src <= 1'b0;                // 两域世代回到共同零值
		end else if(i_req_valid && o_req_ready)begin
			flag_source_busy <= 1'b1;              // 新请求取得唯一源槽
			reg_req_write_hold_src <= i_req_write; // 冻结操作类型供DDR域复制
			reg_req_addr_hold_src <= i_req_addr;   // 冻结地址至响应消费
			reg_req_data_hold_src <= i_req_data;   // 冻结写数据至响应消费
			req_toggle_src <= !req_toggle_src;     // 载荷锁存后发布新世代
		end else if(rsp_valid_o && i_rsp_ready)begin
			flag_source_busy <= 1'b0;              // 响应消费后才允许下一请求
		end
	end

	// 两级同步DDR域发布的响应世代和粘滞故障
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			rsp_toggle_meta_src <= 1'b0;           // 共同复位清除响应同步第一级
			rsp_toggle_sync_src <= 1'b0;           // 共同复位清除响应同步第二级
			fault_meta_src <= 1'b0;                // 共同复位清除故障同步第一级
			fault_sync_src <= 1'b0;                // 共同复位清除故障同步第二级
		end else begin
			rsp_toggle_meta_src <= rsp_toggle_ddr; // 第一级仅采样异步世代位
			rsp_toggle_sync_src <= rsp_toggle_meta_src; // 第二级提供稳定事件判定
			fault_meta_src <= flag_fault_ddr;      // 第一级仅采样DDR故障状态
			fault_sync_src <= fault_meta_src;      // 第二级导出源域故障观测
		end
	end

	// 新响应世代到达后复制冻结总线并保持到ready
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			rsp_toggle_seen_src <= 1'b0;           // 共同复位清除已复制世代
			rsp_ack_toggle_src <= 1'b0;            // 共同复位清除消费确认世代
			rsp_valid_o <= 1'b0;                   // 复位期间没有可见响应
			rsp_data_o <= 128'd0;                  // 清除旧响应数据避免泄漏
			rsp_error_o <= 4'd0;                   // 清除旧错误分类避免泄漏
		end else if(rsp_toggle_sync_src != rsp_toggle_seen_src)begin
			rsp_toggle_seen_src <= rsp_toggle_sync_src; // 记录已复制的新响应世代
			rsp_valid_o <= 1'b1;                   // 复制完成后才向源端发布
			rsp_data_o <= reg_rsp_data_hold_ddr;   // 两级等待后采样冻结数据总线
			rsp_error_o <= reg_rsp_error_hold_ddr; // 两级等待后采样冻结错误总线
		end else if(rsp_valid_o && i_rsp_ready)begin
			rsp_valid_o <= 1'b0;                   // 源端消费后撤销响应有效
			rsp_ack_toggle_src <= rsp_toggle_seen_src; // 返回已消费的响应世代
		end
	end

	//-------------DDR域CDC任务处理区域---------//
	// 两级同步请求世代和响应消费确认世代
	always@(posedge i_ddr_clk or negedge i_ddr_rstn)begin
		if(i_ddr_rstn == 1'b0)begin
			req_toggle_meta_ddr <= 1'b0;           // 共同复位清除请求同步第一级
			req_toggle_sync_ddr <= 1'b0;           // 共同复位清除请求同步第二级
			rsp_ack_meta_ddr <= 1'b0;              // 共同复位清除确认同步第一级
			rsp_ack_sync_ddr <= 1'b0;              // 共同复位清除确认同步第二级
		end else begin
			req_toggle_meta_ddr <= req_toggle_src; // 第一级仅采样异步请求世代
			req_toggle_sync_ddr <= req_toggle_meta_ddr; // 第二级提供稳定请求事件
			rsp_ack_meta_ddr <= rsp_ack_toggle_src; // 第一级仅采样异步确认世代
			rsp_ack_sync_ddr <= rsp_ack_meta_ddr;  // 第二级提供稳定释放条件
		end
	end

	// DDR空闲时只复制一个已经跨越两级同步的冻结请求
	always@(posedge i_ddr_clk or negedge i_ddr_rstn)begin
		if(i_ddr_rstn == 1'b0)begin
			req_toggle_seen_ddr <= 1'b0;           // 共同复位清除DDR已见世代
			reg_req_write_ddr <= 1'b0;             // 共同复位清除DDR读写类型
			reg_req_addr_ddr <= 25'd0;             // 共同复位清除DDR地址槽
			reg_req_data_ddr <= 128'd0;            // 共同复位清除DDR数据槽
		end else if((state_current == ST_IDLE) && flag_req_arrive_ddr)begin
			req_toggle_seen_ddr <= req_toggle_sync_ddr; // 标记该请求只复制一次
			reg_req_write_ddr <= reg_req_write_hold_src; // 源端保持窗口内复制类型
			reg_req_addr_ddr <= reg_req_addr_hold_src; // 源端保持窗口内复制地址
			reg_req_data_ddr <= reg_req_data_hold_src; // 源端保持窗口内复制数据
		end
	end

	//----------------状态机区域----------------//
	// DDR状态寄存器只由共同复位和下一状态控制
	always@(posedge i_ddr_clk or negedge i_ddr_rstn)begin
		if(i_ddr_rstn == 1'b0)begin
			state_current <= ST_IDLE;              // 共同复位回到无所有者状态
		end else begin
			state_current <= state_next;           // 每拍进入组合判定的下一阶段
		end
	end

	// 组合下一状态覆盖单槽PAXI事务的全部阶段
	always@(*)begin
		state_next = state_current;              // 默认保持当前阶段
		case(state_current)
			// 空闲仅响应一个新的同步请求世代
			ST_IDLE:begin
				if(flag_unexpected_r || flag_phy_lost)begin
					state_next = ST_FAULT;            // 无读所有者的返回直接闭锁
				end else if(flag_req_arrive_ddr)begin
					state_next = ST_CHECK;            // 下一拍使用已复制请求
				end
			end

			// 地址与PHY检查在发出PAXI之前完成
			ST_CHECK:begin
				if(flag_unexpected_r || !flag_addr_valid || !i_phy_ready)begin
					state_next = ST_RESPONSE;         // 发布分类错误且不重试
				end else if(reg_req_write_ddr)begin
					state_next = ST_WRITE_ADDR;       // 合法写先保持AW到真实接受
				end else begin
					state_next = ST_READ_ADDR;        // 合法读首先提出AR
				end
			end

			// AW保持到接受，厂商已知路径不允许W先行
			ST_WRITE_ADDR:begin
				if(flag_unexpected_r || !i_phy_ready || flag_timeout_hit)begin
					state_next = ST_RESPONSE;         // 端点失败停止当前实验
				end else if(o_awvalid && i_awready)begin
					state_next = ST_WRITE_DATA;       // 紧接下一拍首次提出W
				end
			end

			// W在AW接受后的下一拍提出并保持到接受
			ST_WRITE_DATA:begin
				if(flag_unexpected_r || !i_phy_ready || flag_timeout_hit)begin
					state_next = ST_RESPONSE;         // W等待失败停止当前实验
				end else if(o_wvalid && i_wready)begin
					state_next = ST_RESPONSE;         // AW和W均接受后返回非提交成功
				end
			end

			// AR接受当拍允许唯一R返回直接完成
			ST_READ_ADDR:begin
				if(!i_phy_ready || flag_timeout_hit || flag_unexpected_r)begin
					state_next = ST_RESPONSE;         // 地址阶段错误终止且不重试
				end else if(flag_ar_accept && i_rvalid)begin
					state_next = ST_RESPONSE;         // 同拍返回已完整捕获
				end else if(flag_ar_accept)begin
					state_next = ST_READ_DATA;        // 地址接受后等待唯一返回
				end
			end

			// 已接受AR后等待一拍带RLAST的数据
			ST_READ_DATA:begin
				if(!i_phy_ready || flag_timeout_hit)begin
					state_next = ST_RESPONSE;         // 等待期间端点失败停止实验
				end else if(i_rvalid)begin
					state_next = ST_RESPONSE;         // 数据或RLAST错误均形成响应
				end
			end

			// 响应保持到源端消费确认跨回DDR域
			ST_RESPONSE:begin
				if(rsp_ack_sync_ddr == rsp_toggle_ddr)begin
					if(flag_fault_ddr)begin
						state_next = ST_FAULT;        // 错误响应消费后保持故障
					end else begin
						state_next = ST_IDLE;         // 成功响应消费后释放唯一槽
					end
				end
			end

			// 故障只允许共同复位恢复
			ST_FAULT:begin
				state_next = ST_FAULT;             // 禁止自动重试或局部恢复
			end

			// 未知编码按协议故障闭锁
			default:begin
				state_next = ST_FAULT;             // 不猜测非法状态的恢复路径
			end
		endcase
	end

	//-------------状态任务处理区域-------------//
	// 事务等待计数不包含源端响应反压阶段
	always@(posedge i_ddr_clk or negedge i_ddr_rstn)begin
		if(i_ddr_rstn == 1'b0)begin
			cnt_timeout <= 27'd0;                 // 共同复位清除旧等待时间
		end else if((state_current == ST_WRITE_ADDR) || (state_current == ST_WRITE_DATA) || (state_current == ST_READ_ADDR) || (state_current == ST_READ_DATA))begin
			if(!flag_timeout_hit)begin
				cnt_timeout <= cnt_timeout + 1'b1; // 有界增加并在上限饱和
			end
		end else begin
			cnt_timeout <= 27'd0;                 // 非端点等待阶段重新计时
		end
	end

	// 在事务终止边沿一次性发布冻结响应载荷
	always@(posedge i_ddr_clk or negedge i_ddr_rstn)begin
		if(i_ddr_rstn == 1'b0)begin
			reg_rsp_data_hold_ddr <= 128'd0;      // 共同复位清除旧响应数据
			reg_rsp_error_hold_ddr <= 4'd0;       // 共同复位清除旧错误分类
			rsp_toggle_ddr <= 1'b0;               // 两域响应世代回到共同零值
		end else if(state_current == ST_CHECK && (!flag_addr_valid || !i_phy_ready || flag_unexpected_r))begin
			reg_rsp_data_hold_ddr <= 128'd0;      // 发出PAXI前失败没有读数据
			reg_rsp_error_hold_ddr <= !flag_addr_valid ? C_ERR_ADDR : (!i_phy_ready ? C_ERR_PHY : C_ERR_PROTOCOL); // 保留首个检查错误
			rsp_toggle_ddr <= !rsp_toggle_ddr;    // 完整错误载荷写入后发布
		end else if(state_current == ST_WRITE_ADDR && (!i_phy_ready || flag_timeout_hit || flag_unexpected_r))begin
			reg_rsp_data_hold_ddr <= 128'd0;      // AW阶段失败没有响应数据
			reg_rsp_error_hold_ddr <= !i_phy_ready ? C_ERR_PHY : C_ERR_PROTOCOL; // AW超时或意外R归为协议错误
			rsp_toggle_ddr <= !rsp_toggle_ddr;    // AW阶段错误结果只发布一次
		end else if(state_current == ST_WRITE_DATA && ((o_wvalid && i_wready) || !i_phy_ready || flag_timeout_hit || flag_unexpected_r))begin
			reg_rsp_data_hold_ddr <= 128'd0;      // 写响应不携带提交或读数据
			reg_rsp_error_hold_ddr <= !i_phy_ready ? C_ERR_PHY : ((flag_timeout_hit || flag_unexpected_r) ? C_ERR_PROTOCOL : 4'd0); // W接受成功否则分类失败
			rsp_toggle_ddr <= !rsp_toggle_ddr;    // 写终止结果只发布一次
		end else if(state_current == ST_READ_ADDR && (!i_phy_ready || flag_timeout_hit || flag_unexpected_r || (flag_ar_accept && i_rvalid)))begin
			reg_rsp_data_hold_ddr <= (flag_ar_accept && i_rvalid && i_rlast) ? i_rdata : 128'd0; // 仅合法同拍返回保留数据
			reg_rsp_error_hold_ddr <= !i_phy_ready ? C_ERR_PHY : ((flag_timeout_hit || flag_unexpected_r) ? C_ERR_PROTOCOL : (i_rlast ? 4'd0 : C_ERR_LAST)); // 同拍检查末拍语义
			rsp_toggle_ddr <= !rsp_toggle_ddr;    // 地址阶段终止结果只发布一次
		end else if(state_current == ST_READ_DATA && (!i_phy_ready || flag_timeout_hit || i_rvalid))begin
			reg_rsp_data_hold_ddr <= (i_rvalid && i_rlast) ? i_rdata : 128'd0; // 仅完整单拍返回保留数据
			reg_rsp_error_hold_ddr <= !i_phy_ready ? C_ERR_PHY : (flag_timeout_hit ? C_ERR_PROTOCOL : (i_rlast ? 4'd0 : C_ERR_LAST)); // 返回阶段检查末拍语义
			rsp_toggle_ddr <= !rsp_toggle_ddr;    // 数据阶段终止结果只发布一次
		end
	end

	// 任一错误在DDR域锁存，只有共同复位能够清除
	always@(posedge i_ddr_clk or negedge i_ddr_rstn)begin
		if(i_ddr_rstn == 1'b0)begin
			flag_phy_seen_ddr <= 1'b0;              // 共同复位重新等待PHY首次建立
			flag_fault_ddr <= 1'b0;               // 共同复位清除粘滞故障
		end else begin
			if(i_phy_ready)begin
				flag_phy_seen_ddr <= 1'b1;          // 记录PHY已经真实建立过
			end
			if(flag_unexpected_r || flag_phy_lost ||
			((state_current == ST_CHECK) && (!flag_addr_valid || !i_phy_ready)) ||
			(((state_current == ST_WRITE_ADDR) || (state_current == ST_WRITE_DATA)) && (!i_phy_ready || flag_timeout_hit)) ||
			((state_current == ST_READ_ADDR) && (!i_phy_ready || flag_timeout_hit || (flag_ar_accept && i_rvalid && !i_rlast))) ||
			((state_current == ST_READ_DATA) && (!i_phy_ready || flag_timeout_hit || (i_rvalid && !i_rlast))))begin
				flag_fault_ddr <= 1'b1;             // 不重试且保持到两域共同复位
			end
		end
	end

endmodule
