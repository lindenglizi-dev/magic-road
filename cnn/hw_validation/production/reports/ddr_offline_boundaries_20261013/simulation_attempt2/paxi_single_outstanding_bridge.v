`timescale 1ns / 1ps

////////////////////////////////////English///////////////////////////////////////
// Company:         Erie
// Engineer:        Erie
//
// Create Date:     2026/10/04 00:00:00
// Design Name:     paxi_single_outstanding_bridge
// Module Name:     paxi_single_outstanding_bridge
// Description:     description/paxi_single_outstanding_bridge_Design.pdf
// Simulations:     testbench/vivado/2021.1/paxi_single_outstanding_bridge
//
// Referrences:
// File Format      File Name
// 1.Book           cnn/spec/integration_contract.md
//
// Dependencies:
// Module Name      Version
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
// 设计名称:        paxi_single_outstanding_bridge
// 模块名称:        paxi_single_outstanding_bridge
// 模块说明:        Description/paxi_single_outstanding_bridge_Design.pdf
// 仿真工程:        TestBench/Vivado/2021.1/paxi_single_outstanding_bridge
//
// 参考资料:
// 文件格式         文件名称
// 1.Book           cnn/spec/integration_contract.md
//
// 依赖文件:
// 模块名称         版本
//
// 当前版本:        V1.0
// 修订日期:        2026年10月04日
// 修订历史:
// 时间             版本        修订人            修订内容
// 2026年10月04日   V1.0        Erie              创建文件

module paxi_single_outstanding_bridge
(
	//-----------------全局信号-----------------//
	input i_clk,                                // PAXI用户时钟
	input i_rstn,                               // 与DDR端点协调的低有效硬复位

	//-----------------请求接口-----------------//
	input i_req_valid,                          // 上游请求有效并保持载荷稳定
	input i_req_write,                          // 高电平选择写操作
	input [31:0]i_req_byte_addr,                // CNN预留区内的字节地址
	input [127:0]i_req_write_data,              // 单个十六字节写载荷
	input [15:0]i_req_write_mask,               // 高电平表示对应字节被屏蔽
	input [31:0]i_req_epoch,                    // 协调重启后的任务世代
	input [31:0]i_req_owner,                    // 返回归属标识
	input i_cancel,                             // 取消当前唯一所有者并继续排空
	output o_req_ready,                         // 可接收一个本地请求

	//-----------------提交接口-----------------//
	input i_commit_confirmed,                   // 外部已证明的写提交事件

	//-----------------结果接口-----------------//

	//RESULT接口
	input i_result_ready,                       // 上游接收结果
	output o_result_valid,                      // 结果载荷有效并保持稳定
	output o_result_write,                      // 结果来源于写事务
	output o_result_committed,                  // 写结果已有显式提交证明
	output [31:0]o_result_epoch,                // 结果任务世代
	output [31:0]o_result_owner,                // 结果归属标识
	output [127:0]o_result_read_data,           // 单拍读返回数据

	//-----------------接收遥测-----------------//

	//PAXI_ACCEPTED接口
	output o_paxi_accepted_valid,               // 控制器接收事件脉冲
	output o_paxi_accepted_write,               // 接收事件属于写事务
	output [31:0]o_paxi_accepted_epoch,         // 接收事件任务世代
	output [31:0]o_paxi_accepted_owner,         // 接收事件归属标识

	//-----------------状态遥测-----------------//
	output o_drain_done,                        // 无请求、预留或保持结果
	output o_protocol_fault,                    // 粘滞协议故障状态
	output [31:0]o_late_discard_count,          // 取消后晚到终止事件计数
	output [31:0]o_cancelled_drain_count,       // 已接收事务的取消排空计数

	//--------------PAXI读地址通道--------------//

	//PAXI接口
	input i_paxi_arready,                       // 控制器真实读地址就绪
	output o_paxi_arvalid,                      // 单拍读地址有效
	output [24:0]o_paxi_araddr,                 // 十六位字地址

	//--------------PAXI写地址通道--------------//

	//PAXI接口
	input i_paxi_awready,                       // 控制器真实写地址就绪
	output o_paxi_awvalid,                      // 单拍写地址有效
	output [24:0]o_paxi_awaddr,                 // 写通道使用的十六位字地址

	//--------------PAXI写数据通道--------------//

	//PAXI接口
	input i_paxi_wready,                        // 控制器真实写数据就绪
	output o_paxi_wvalid,                       // AW接收后呈现的写数据有效
	output [127:0]o_paxi_wdata,                 // 已缓存的写载荷
	output [15:0]o_paxi_wmask,                  // 原样转发的高有效屏蔽位

	//--------------PAXI读返回通道--------------//

	//PAXI接口
	input i_paxi_rvalid,                        // 无READY返回数据有效
	input i_paxi_rlast,                         // 单请求唯一返回拍标志
	input [127:0]i_paxi_rdata                   // 控制器返回数据
);

	//---------------配置参数区域---------------//
	// CNN预留地址边界
	localparam [31:0]BASE_BYTE_ADDR = 32'h03400000; // 预留区首字节地址
	localparam [31:0]LAST_BYTE_ADDR = 32'h03fffff0; // 最后合法十六字节块

	//---------------状态参数区域---------------//
	// 单在途控制阶段
	localparam [3:0]ST_IDLE = 4'd0;             // 等待本地请求
	localparam [3:0]ST_CHECK = 4'd1;            // 检查缓存请求边界
	localparam [3:0]ST_READ_ADDR = 4'd2;        // 等待读地址接收
	localparam [3:0]ST_READ_RETURN = 4'd3;      // 等待无READY读返回
	localparam [3:0]ST_WRITE_ADDR = 4'd4;       // 等待写地址接收
	localparam [3:0]ST_WRITE_DATA = 4'd5;       // AW后等待写数据接收
	localparam [3:0]ST_WRITE_COMMIT = 4'd6;     // 等待显式提交证明
	localparam [3:0]ST_RETIRE = 4'd7;           // 按取消状态归并终止事件
	localparam [3:0]ST_RESULT = 4'd8;           // 保持成功结果至上游接收
	localparam [3:0]ST_FAULT = 4'd9;            // 故障后禁止新请求

	//----------------状态机信号----------------//
	// 主控制状态
	reg [3:0]state_current = ST_IDLE;           // 当前控制阶段
	reg [3:0]state_next = ST_IDLE;              // 下一控制阶段

	//-----------------标志信号-----------------//
	// 地址资格寄存器
	reg flag_addr_range = 1'b0;                 // 地址位于CNN预留区
	reg flag_addr_aligned = 1'b0;               // 地址满足十六字节对齐

	// 事务生命周期标志
	reg flag_cancelled = 1'b0;                  // 当前事务收到本地取消
	reg flag_cancel_before_terminal = 1'b0;     // 终止事件到达时已取消

	// 控制器接收事件标志
	reg flag_read_accepted = 1'b0;              // 本拍读地址被控制器接收

	// 协议故障采样标志
	reg flag_bad_return = 1'b0;                 // 未分配读所有者时收到返回
	reg flag_bad_commit = 1'b0;                 // 未等待写提交时收到证明
	reg flag_bad_last = 1'b0;                   // 单拍读返回缺少末拍标志

	// 合并故障来源
	wire flag_bad_external;                     // 返回或提交事件无归属
	wire flag_bad_protocol;                     // 任一采样协议错误

	//-----------------输出信号-----------------//
	//结果接口RESULT接口
	// 已接收请求载荷
	reg flag_req_write_cache = 1'b0;            // 缓存的读写类型
	reg [31:0]reg_epoch = 32'h00000000;         // 当前事务世代所有权
	reg [31:0]reg_owner = 32'h00000000;         // 当前事务返回所有者
	//结果接口
	reg [127:0]result_read_data_o = 128'h00000000000000000000000000000000; // 已归属的读返回数据

	//接收遥测PAXI_ACCEPTED接口
	reg paxi_accepted_write_o = 1'b0;           // 本拍写地址和数据均已接收

	//状态遥测
	reg drain_done_o = 1'b0;                    // 状态机空闲指示
	// 遥测计数寄存器
	reg [31:0]cnt_late_discard_o = 32'h00000000; // 取消先于终止事件的次数
	reg [31:0]cnt_cancelled_drain_o = 32'h00000000; // 已接收事务完成取消排空次数

	//PAXI读地址通道PAXI接口
	reg [24:0]reg_paxi_addr = 25'b0000000000000000000000000; // 字节地址右移一位后的地址

	//PAXI写数据通道PAXI接口
	reg [127:0]paxi_wdata_o = 128'h00000000000000000000000000000000; // AW前缓存的写数据
	reg [15:0]paxi_wmask_o = 16'h0000;          // AW前缓存的高有效屏蔽位

	//---------------其他信号连线---------------//
	//其他信号连线
	// 故障归并
	assign flag_bad_external = flag_bad_return || flag_bad_commit; // 合并两类外部误事件
	assign flag_bad_protocol = flag_bad_external || flag_bad_last; // 形成状态机故障请求

	//---------------输出信号连线---------------//
	//请求接口
	// 上游请求与结果
	assign o_req_ready = (state_current == ST_IDLE) && (i_cancel == 1'b0); // 取消周期不接收新请求

	//结果接口RESULT接口
	assign o_result_valid = (state_current == ST_RESULT) && (i_cancel == 1'b0); // 取消优先于成功握手
	assign o_result_write = flag_req_write_cache; // 保持当前结果操作类型
	assign o_result_committed = flag_req_write_cache; // 仅写结果经过提交状态
	assign o_result_epoch = reg_epoch;          // 返回缓存的世代标识
	assign o_result_owner = reg_owner;          // 返回缓存的所有者标识

	//结果接口
	assign o_result_read_data = result_read_data_o; // 返回归属后的读数据

	//接收遥测PAXI_ACCEPTED接口
	// 控制器接收遥测
	assign o_paxi_accepted_valid = flag_read_accepted || paxi_accepted_write_o; // 任一实际接收事件
	assign o_paxi_accepted_write = paxi_accepted_write_o; // 高电平仅代表写双通道已接收
	assign o_paxi_accepted_epoch = reg_epoch;   // 接收事件对应的缓存世代
	assign o_paxi_accepted_owner = reg_owner;   // 接收事件对应的缓存所有者

	//状态遥测
	assign o_drain_done = drain_done_o;         // 导出无在途所有权状态
	assign o_protocol_fault = (state_current == ST_FAULT); // 故障状态保持至协调复位
	assign o_late_discard_count = cnt_late_discard_o; // 导出晚到丢弃累计值
	assign o_cancelled_drain_count = cnt_cancelled_drain_o; // 导出取消排空累计值

	//PAXI读地址通道PAXI接口
	// PAXI读地址通道
	assign o_paxi_arvalid = (state_current == ST_READ_ADDR); // 首次呈现后保持至真实接收
	assign o_paxi_araddr = reg_paxi_addr;       // 读地址来自已缓存字地址

	//PAXI写地址通道PAXI接口
	// PAXI写地址通道
	assign o_paxi_awvalid = (state_current == ST_WRITE_ADDR); // 写地址呈现后保持至AWREADY
	assign o_paxi_awaddr = reg_paxi_addr;       // 写地址来自已缓存字地址

	//PAXI写数据通道PAXI接口
	// PAXI写数据通道
	assign o_paxi_wvalid = (state_current == ST_WRITE_DATA); // AW接受后一拍开始呈现
	assign o_paxi_wdata = paxi_wdata_o;         // 反压期间保持写数据
	assign o_paxi_wmask = paxi_wmask_o;         // 反压期间保持高有效屏蔽位

	//-------------输出信号处理区域-------------//
	//状态遥测
	// 状态输出过程只声明是否已经完全排空
	always@(*)begin
		drain_done_o = 1'b0;                    // 非空闲状态默认保留所有权
		if(state_current == ST_IDLE)begin
			drain_done_o = 1'b1;                // 空闲状态允许观察到排空完成
		end
	end

	//结果接口RESULT接口
	// 缓存请求操作类型
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_req_write_cache <= 1'b0;       // 协调复位默认读类型
		end else if(i_req_valid == 1'b1 && o_req_ready == 1'b1)begin
			flag_req_write_cache <= i_req_write; // 本地握手时固定操作类型
		end
	end

	//PAXI读地址通道PAXI接口
	// 将字节地址转换为十六位字地址
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_paxi_addr <= 25'b0000000000000000000000000; // 协调复位清空地址缓存
		end else if(i_req_valid == 1'b1 && o_req_ready == 1'b1)begin
			reg_paxi_addr <= i_req_byte_addr[25:1]; // 固定配置下执行右移一位
		end
	end

	//PAXI写数据通道PAXI接口
	// 在任何AW呈现前缓存完整写载荷
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			paxi_wdata_o <= 128'h00000000000000000000000000000000; // 协调复位清空写数据缓存
		end else if(i_req_valid == 1'b1 && o_req_ready == 1'b1)begin
			paxi_wdata_o <= i_req_write_data;   // 后续反压不得改变载荷
		end
	end

	// 缓存控制器定义的高有效屏蔽位
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			paxi_wmask_o <= 16'h0000;           // 全零表示不屏蔽任何字节
		end else if(i_req_valid == 1'b1 && o_req_ready == 1'b1)begin
			paxi_wmask_o <= i_req_write_mask;   // 不采用AXI字节使能语义
		end
	end

	//结果接口RESULT接口
	// 请求握手后保持世代直到当前事务排空
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_epoch <= 32'h00000000;          // 协调复位清除旧世代
		end else if(i_req_valid == 1'b1 && o_req_ready == 1'b1)begin
			reg_epoch <= i_req_epoch;           // 新请求取得唯一所有权
		end
	end

	// 请求握手后保持返回所有者直到终止事件
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_owner <= 32'h00000000;          // 协调复位清除旧所有者
		end else if(i_req_valid == 1'b1 && o_req_ready == 1'b1)begin
			reg_owner <= i_req_owner;           // 新请求绑定返回归属
		end
	end

	//结果接口
	// 锁存已归属的单拍读返回数据
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			result_read_data_o <= 128'h00000000000000000000000000000000; // 协调复位清空返回缓存
		end else if(state_current == ST_READ_RETURN && i_paxi_rvalid == 1'b1 && i_paxi_rlast == 1'b1)begin
			result_read_data_o <= i_paxi_rdata; // 无READY返回到达即捕获
		end
	end

	//接收遥测PAXI_ACCEPTED接口
	// 写数据接收代表AW和W均已完成
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			paxi_accepted_write_o <= 1'b0;      // 协调复位无写接收事件
		end else begin
			paxi_accepted_write_o <= (state_current == ST_WRITE_DATA) && i_paxi_wready; // AW已在前一状态接收
		end
	end

	//状态遥测
	// 在取消早于控制器终止时累加晚返诊断值
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			cnt_late_discard_o <= 32'h00000000; // 协调复位清空诊断计数
		end else if(state_current == ST_RETIRE && flag_cancel_before_terminal == 1'b1)begin
			cnt_late_discard_o <= cnt_late_discard_o + 1'b1; // 晚到事件已归属但不发布成功
		end
	end

	// 统计已被控制器接收后完成排空的取消事务
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			cnt_cancelled_drain_o <= 32'h00000000; // 协调复位清空守恒计数
		end else if(state_current == ST_RETIRE && (flag_cancelled == 1'b1 || i_cancel == 1'b1))begin
			cnt_cancelled_drain_o <= cnt_cancelled_drain_o + 1'b1; // 终止事件完成排空
		end else if(state_current == ST_RESULT && i_cancel == 1'b1)begin
			cnt_cancelled_drain_o <= cnt_cancelled_drain_o + 1'b1; // 保持结果被取消后排空
		end
	end

	//----------------状态机区域----------------//
	// 当前状态寄存器响应协调硬复位
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			state_current <= ST_IDLE;           // DDR端点同时复位后清空所有权
		end else begin
			state_current <= state_next;        // 进入已判定的下一阶段
		end
	end

	// 下一状态过程解析唯一事务的阶段转移
	always@(*)begin
		state_next = state_current;             // 默认保持当前阶段
		case(state_current)

			// 空闲时只缓存一个上游请求
			ST_IDLE:begin
				if(i_req_valid == 1'b1 && o_req_ready == 1'b1)begin
					state_next = ST_CHECK;      // 下一拍检查缓存的地址属性
				end else begin
					state_next = ST_IDLE;       // 没有请求时继续排空
				end
			end

			// 请求检查失败直接进入粘滞故障
			ST_CHECK:begin
				if(i_cancel == 1'b1)begin
					state_next = ST_IDLE;       // 未发出控制器请求即可取消
				end else if(flag_addr_range == 1'b0 || flag_addr_aligned == 1'b0)begin
					state_next = ST_FAULT;      // 非法地址绝不呈现给PAXI
				end else if(flag_req_write_cache == 1'b1)begin
					state_next = ST_WRITE_ADDR; // 合法写请求先发AW
				end else begin
					state_next = ST_READ_ADDR;  // 合法读请求发AR
				end
			end

			// 读地址只按真实ARREADY接收
			ST_READ_ADDR:begin
				if(o_paxi_arvalid == 1'b1 && i_paxi_arready == 1'b1)begin
					state_next = ST_READ_RETURN; // 为无READY返回保留唯一槽
				end else begin
					state_next = ST_READ_ADDR;  // 反压期间保持地址
				end
			end

			// 读返回必须携带单拍末拍标志
			ST_READ_RETURN:begin
				if(i_paxi_rvalid == 1'b1 && i_paxi_rlast == 1'b1)begin
					state_next = ST_RETIRE;     // 先锁存终止事件再判取消
				end else begin
					state_next = ST_READ_RETURN; // 不用超时释放所有权
				end
			end

			// 写地址只按真实AWREADY接收
			ST_WRITE_ADDR:begin
				if(o_paxi_awvalid == 1'b1 && i_paxi_awready == 1'b1)begin
					state_next = ST_WRITE_DATA; // 下一拍首次呈现W
				end else begin
					state_next = ST_WRITE_ADDR; // AW反压期间保持写地址阶段
				end
			end

			// AW已接收后必须继续排空W
			ST_WRITE_DATA:begin
				if(o_paxi_wvalid == 1'b1 && i_paxi_wready == 1'b1)begin
					state_next = ST_WRITE_COMMIT; // 双通道已接收但尚未提交
				end else begin
					state_next = ST_WRITE_DATA; // 持有缓存数据直至真实接收
				end
			end

			// 只有显式外部事件能够证明写提交
			ST_WRITE_COMMIT:begin
				if(i_commit_confirmed == 1'b1)begin
					state_next = ST_RETIRE;     // 终止事件进入统一退休阶段
				end else begin
					state_next = ST_WRITE_COMMIT; // 未证明时永不自行成功
				end
			end

			// 取消事务静默排空，正常事务形成结果
			ST_RETIRE:begin
				if(flag_cancelled == 1'b1 || i_cancel == 1'b1)begin
					state_next = ST_IDLE;       // 不发布已取消事务成功
				end else begin
					state_next = ST_RESULT;     // 保持成功载荷至上游接收
				end
			end

			// 结果握手或取消后释放所有权
			ST_RESULT:begin
				if(i_cancel == 1'b1)begin
					state_next = ST_IDLE;       // 同拍取消压过成功握手
				end else if(o_result_valid == 1'b1 && i_result_ready == 1'b1)begin
					state_next = ST_IDLE;       // 上游接收后完成事务
				end else begin
					state_next = ST_RESULT;     // 反压期间保持全部元数据
				end
			end

			// 协议故障只能由协调硬复位清除
			ST_FAULT:begin
				state_next = ST_FAULT;          // 故障后禁止继续试探控制器
			end

			// 非法状态同样闭锁流量
			default:begin
				state_next = ST_FAULT;          // 不猜测未知状态恢复路径
			end
		endcase
		if(flag_bad_protocol == 1'b1)begin
			state_next = ST_FAULT;              // 任何协议误事件均闭锁新流量
		end
	end

	//-------------状态任务处理区域-------------//
	// 本地取消在控制器接收后保持至终止事件
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_cancelled <= 1'b0;             // 协调复位清除取消状态
		end else if(i_req_valid == 1'b1 && o_req_ready == 1'b1)begin
			flag_cancelled <= 1'b0;             // 新事务从未取消状态开始
		end else if(i_cancel == 1'b1 && state_current != ST_IDLE)begin
			flag_cancelled <= 1'b1;             // 不擦除缓存的世代和所有者
		end
	end

	// 在终止事件边界冻结取消先后关系
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_cancel_before_terminal <= 1'b0; // 协调复位清空事件分类
		end else if(i_req_valid == 1'b1 && o_req_ready == 1'b1)begin
			flag_cancel_before_terminal <= 1'b0; // 新请求尚无终止事件
		end else if(state_current == ST_READ_RETURN && i_paxi_rvalid == 1'b1 && i_paxi_rlast == 1'b1)begin
			flag_cancel_before_terminal <= flag_cancelled || i_cancel; // 记录读返回是否晚于取消
		end else if(state_current == ST_WRITE_COMMIT && i_commit_confirmed == 1'b1)begin
			flag_cancel_before_terminal <= flag_cancelled || i_cancel; // 记录提交事件是否晚于取消
		end
	end

	// 读地址真实接收形成单周期遥测
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_read_accepted <= 1'b0;         // 复位时撤销读接收遥测脉冲
		end else begin
			flag_read_accepted <= (state_current == ST_READ_ADDR) && i_paxi_arready; // 取消同拍也必须记录真实AR握手
		end
	end

	// 采样没有读所有者的返回事件
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_bad_return <= 1'b0;            // 协调复位清除错误采样
		end else begin
			flag_bad_return <= i_paxi_rvalid && (state_current != ST_READ_RETURN); // 不允许猜测返回归属
		end
	end

	// 采样没有写等待者的提交事件
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_bad_commit <= 1'b0;            // 复位时清除无归属提交记录
		end else begin
			flag_bad_commit <= i_commit_confirmed && (state_current != ST_WRITE_COMMIT); // 只接受显式归属事件
		end
	end

	// 采样违反单拍返回合同的事件
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_bad_last <= 1'b0;              // 协调复位清除末拍错误
		end else begin
			flag_bad_last <= (state_current == ST_READ_RETURN) && i_paxi_rvalid && (i_paxi_rlast == 1'b0); // 缺少RLAST时失败闭锁
		end
	end

	//-------------主要任务处理区域-------------//
	// 采样预留区起止边界
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_addr_range <= 1'b0;            // 复位值不授权任何地址
		end else if(i_req_valid == 1'b1 && o_req_ready == 1'b1)begin
			flag_addr_range <= (i_req_byte_addr >= BASE_BYTE_ADDR) && (i_req_byte_addr <= LAST_BYTE_ADDR); // 两端均为完整块边界
		end
	end

	// 采样十六字节块对齐条件
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_addr_aligned <= 1'b0;          // 复位值不授权未检查请求
		end else if(i_req_valid == 1'b1 && o_req_ready == 1'b1)begin
			flag_addr_aligned <= (i_req_byte_addr[3:0] == 4'b0000); // 单请求固定十六字节
		end
	end

endmodule
