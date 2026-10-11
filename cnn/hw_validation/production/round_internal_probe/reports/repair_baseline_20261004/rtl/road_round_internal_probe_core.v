`timescale 1ns / 1ps

////////////////////////////////////English///////////////////////////////////////
// Company:         Erie
// Engineer:        Erie
//
// Create Date:     2026/10/04 00:00:00
// Design Name:     road_round_internal_probe_core
// Module Name:     road_round_internal_probe_core
// Description:     description/road_round_internal_probe_core_Design.pdf
// Simulations:     testbench/vivado/2021.1/road_round_internal_probe_core
//
// Referrences:
// File Format      File Name
// 1.Book           road_round_internal_probe_core.contract.json
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
// 设计名称:        road_round_internal_probe_core
// 模块名称:        road_round_internal_probe_core
// 模块说明:        Description/road_round_internal_probe_core_Design.pdf
// 仿真工程:        TestBench/Vivado/2021.1/road_round_internal_probe_core
//
// 参考资料:
// 文件格式         文件名称
// 1.Book           road_round_internal_probe_core.contract.json
//
// 依赖文件:
// 模块名称         版本
//
// 当前版本:        V1.0
// 修订日期:        2026年10月04日
// 修订历史:
// 时间             版本        修订人            修订内容
// 2026/10/04       V1.0        Erie              创建文件

module road_round_internal_probe_core
(
	//-----------------全局信号-----------------//
	input i_clk,                                // 探针与舍入流水工作时钟
	input i_rstn,                               // 外部异步低有效复位

	//----------------RESULT接口----------------//

	//RESULT接口
	output o_result_valid,                      // 下游边界本拍接收结果
	output [15:0]o_result_data,                 // 下游边界接收数值位型
	output [15:0]o_result_tag,                  // 下游边界接收源身份
	output o_result_fault,                      // 下游边界接收故障标志
	output [63:0]o_checksum,                    // 已消费结果令牌异或校验
	output o_error,                             // 故障标志与源序列不一致
	output [15:0]o_result_count                 // 已纳入校验的结果数
);

	//---------------配置参数区域---------------//
	// 非零初值保证确定性反馈寄存器不会进入全零状态。
	localparam [63:0]PRBS_SEED = 64'h1d872b41c9e6a5f3; // 确定性反馈状态非零初值

	//--------------模块实例化信号--------------//
	//road_round_shift--RESULT接口
	wire [15:0]wire_core_result_data;           // 核心返回饱和数值位型
	wire [15:0]wire_core_result_tag;            // 核心返回源令牌身份

	//-----------------计数信号-----------------//
	reg [15:0]cnt_tag = 16'd0;                  // 下一条生成身份

	//----------------寄存器信号----------------//
	// 源发生器先寄存状态，再跨真实边界送入舍入核心。
	reg [1:0]reg_stall_phase = 2'd0;            // 每四拍插入一次共同停顿
	reg [63:0]reg_prbs = PRBS_SEED;             // 确定性六十四位源状态
	reg signed [63:0]reg_product_source = 64'd0; // 核心输入乘积边界
	reg [5:0]reg_shift_source = 6'd0;           // 核心输入移位边界
	reg [15:0]reg_tag_source = 16'd0;           // 核心输入身份边界

	// 接收边界与校验边界分开，防止核心组合锥直达可观察状态。
	reg [32:0]reg_checksum_token = 33'd0;       // 规范化故障、身份与数值

	//-----------------标志信号-----------------//
	//road_round_shift--RESULT接口
	wire flag_core_result_valid;                // 核心完成令牌有效标志
	wire flag_core_result_fault;                // 核心返回非法输入标志
	reg flag_source_valid = 1'd0;               // 核心输入令牌有效
	reg flag_source_active = 1'd0;              // 限定一次固定长度探针批次
	reg flag_advance = 1'd0;                    // 源与核心共同推进许可
	reg flag_checksum_token = 1'd0;             // 校验边界令牌有效
	reg flag_fault_mismatch = 1'd0;             // 返回故障与身份模式不符

	// 两抽头反馈只依赖当前已寄存源状态。
	wire flag_prbs_feedback;                    // 六十四位反馈移位输入位

	//-----------------其他信号-----------------//
	wire [16:0]wire_result_count_next;          // 消费计数扩位加法结果

	//-----------------输出信号-----------------//
	//RESULT接口
	reg result_valid_o = 1'd0;                  // 接收边界有效脉冲
	reg [15:0]result_data_o = 16'd0;            // 接收边界数值
	reg [15:0]result_tag_o = 16'd0;             // 接收边界身份
	reg result_fault_o = 1'd0;                  // 接收边界故障
	reg [63:0]checksum_o = 64'd0;               // 已消费令牌异或摘要
	reg error_o = 1'd0;                         // 协议错误锁存
	reg [15:0]cnt_result_o = 16'd0;             // 已消费有效结果数

	//---------------其他信号连线---------------//
	//road_round_shift--RESULT接口
	//其他信号连线
	assign wire_core_result_data = 16'hzzzz;    // 实例输出提供饱和数值

	//其他信号连线
	assign wire_core_result_tag = 16'hzzzz;     // 实例输出提供返回身份
	assign flag_prbs_feedback = reg_prbs[63] ^ reg_prbs[62]; // 两抽头确定性反馈
	assign wire_result_count_next = {1'b0, cnt_result_o} + 17'b00000000000000001; // 显式扩位递增
	assign flag_core_result_valid = 1'bz;       // 实例输出提供完成令牌有效
	assign flag_core_result_fault = 1'bz;       // 实例输出提供非法输入标志

	//---------------输出信号连线---------------//
	//RESULT接口
	assign o_result_valid = result_valid_o;     // 发布接收边界有效脉冲
	assign o_result_data = result_data_o;       // 发布接收边界数值
	assign o_result_tag = result_tag_o;         // 发布接收边界身份
	assign o_result_fault = result_fault_o;     // 发布接收边界故障
	assign o_checksum = checksum_o;             // 发布动态结果摘要
	assign o_error = error_o;                   // 发布协议错误锁存
	assign o_result_count = cnt_result_o;       // 发布已消费结果数

	//-------------输出信号处理区域-------------//
	//RESULT接口
	// 只有共同推进拍可以形成新的下游接收脉冲。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			result_valid_o <= 1'd0;             // 取消下游接收脉冲
		end else begin
			result_valid_o <= flag_advance ? (flag_core_result_valid) : 1'd0; // 标记真实接收
		end
	end

	// 接收边界保存核心返回数值，结果有效位负责资格限定。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			result_data_o <= 16'd0;             // 清除接收数值
		end else begin
			result_data_o <= flag_advance ? (wire_core_result_data) : result_data_o; // 接收核心数值
		end
	end

	// 返回身份在同一接收边界寄存，供逐令牌核对。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			result_tag_o <= 16'd0;              // 清除接收身份
		end else begin
			result_tag_o <= flag_advance ? (wire_core_result_tag) : result_tag_o; // 接收核心身份
		end
	end

	// 返回故障与身份、数值一起跨越同一寄存器边界。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			result_fault_o <= 1'd0;             // 清除接收故障
		end else begin
			result_fault_o <= flag_advance ? (flag_core_result_fault) : result_fault_o; // 接收核心故障
		end
	end

	// 动态令牌必须参与摘要，避免核心和源逻辑被常量传播裁剪。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			checksum_o <= 64'd0;                // 清除结果摘要
		end else if(flag_checksum_token == 1'b1)begin
			checksum_o <= checksum_o ^ {31'd0, reg_checksum_token}; // 消费一个结果令牌
		end
	end

	// 任一故障模式不一致都会锁存，复位前不自动恢复。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			error_o <= 1'd0;                    // 清除协议错误
		end else if(flag_checksum_token == 1'b1)begin
			error_o <= error_o | flag_fault_mismatch; // 锁存故障模式差异
		end
	end

	// 结果计数与摘要在同一资格拍更新。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			cnt_result_o <= 16'd0;              // 清除已消费数量
		end else if(flag_checksum_token == 1'b1)begin
			cnt_result_o <= wire_result_count_next[15:0]; // 记录一个结果令牌
		end
	end

	//-------------主要任务处理区域-------------//
	// 停顿相位自由运行，确保共同推进不会在停顿状态自锁。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_stall_phase <= 2'd0;            // 从可推进相位重新开始
		end else if(reg_stall_phase == 2'b00)begin
			reg_stall_phase <= 2'b01;           // 进入第二推进相位
		end else if(reg_stall_phase == 2'b01)begin
			reg_stall_phase <= 2'b10;           // 进入第三推进相位
		end else if(reg_stall_phase == 2'b10)begin
			reg_stall_phase <= 2'b11;           // 进入共同停顿相位
		end else begin
			reg_stall_phase <= 2'b00;           // 停顿后返回第一相位
		end
	end

	// 比较结果先寄存再驱动核心，隔离共同使能组合锥。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_advance <= 1'd0;               // 复位期间禁止推进
		end else begin
			flag_advance <= reg_stall_phase != 2'd3; // 形成一拍共同停顿
		end
	end

	// 源状态只在共同推进拍移动，停顿时产品保持不变。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_prbs <= PRBS_SEED;              // 恢复确定性序列起点
		end else begin
			reg_prbs <= flag_advance ? ({reg_prbs[62:0], flag_prbs_feedback}) : reg_prbs; // 推进反馈状态
		end
	end

	// 重复最高位形成合法六十二位幅值范围，天然排除最小负数。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_product_source <= 64'd0;        // 取消待发送乘积
		end else begin
			reg_product_source <= flag_advance ? ({reg_prbs[63], reg_prbs[63], reg_prbs[61:0]}) : reg_product_source; // 装载动态乘积
		end
	end

	// 身份低六位遍历合法指数并周期性产生六十三故障测试。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_shift_source <= 6'd0;           // 取消待发送移位
		end else begin
			reg_shift_source <= flag_advance ? (cnt_tag[5:0]) : reg_shift_source; // 装载可变指数
		end
	end

	// 每个生成槽位都有唯一十六位身份。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_tag_source <= 16'd0;            // 取消待发送身份
		end else begin
			reg_tag_source <= flag_advance ? (cnt_tag) : reg_tag_source; // 装载当前身份
		end
	end

	// 每八个生成槽位插入一个气泡，批次结束后不再发布新令牌。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_source_valid <= 1'd0;          // 取消待发送有效位
		end else begin
			flag_source_valid <= flag_advance ? (flag_source_active & (cnt_tag[2:0] != 3'd0)) : flag_source_valid; // 装载气泡模式
		end
	end

	// 一百九十二个生成槽位后关闭源有效位，允许流水自然排空。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_source_active <= 1'd1;         // 允许新探针批次
		end else if(flag_advance == 1'b1)begin
			flag_source_active <= (cnt_tag == 16'b0000000010111111) ? 1'd0 : flag_source_active; // 关闭固定批次
		end
	end

	// 身份计数与反馈源在同一个共同推进条件下同步前进。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			cnt_tag <= 16'd0;                   // 返回序列起点
		end else begin
			cnt_tag <= flag_advance ? (cnt_tag + 16'b0000000000000001) : cnt_tag; // 生成下一身份
		end
	end

	// 故障结果的数据未定义，进入摘要前规范化为零。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_checksum_token <= 33'd0;        // 清除待汇总令牌
		end else begin
			reg_checksum_token <= result_fault_o ? ({1'b1, result_tag_o, 16'd0}) : ({1'b0, result_tag_o, result_data_o}); // 规范化令牌
		end
	end

	// 校验有效位比可观察接收边界晚一拍。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_checksum_token <= 1'd0;        // 取消待汇总资格
		end else begin
			flag_checksum_token <= result_valid_o; // 对齐规范化令牌
		end
	end

	// 身份低六位全一是本探针唯一预期故障条件。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_fault_mismatch <= 1'd0;        // 清除故障模式检查
		end else begin
			flag_fault_mismatch <= result_fault_o ^ (&result_tag_o[5:0]); // 检查返回故障
		end
	end

	//--------------模块实例化区域--------------//
	// 生产舍入核心按共同推进接收已寄存源令牌。
	road_round_shift road_round_shift_Inst_core( // 实例化生产舍入核心
		.i_clk(i_clk),                          // 共享探针工作时钟
		.i_rstn(i_rstn),                        // 使用两拍同步释放复位
		.i_advance(flag_advance),               // 共同推进冻结全部核心级
		.i_input_valid(flag_source_valid),      // 传递源边界令牌资格
		.i_product(reg_product_source),         // 送入合法六十二位乘积
		.i_shift(reg_shift_source),             // 送入遍历与故障移位
		.i_tag(reg_tag_source),                 // 绑定确定性源身份
		.o_result_valid(flag_core_result_valid), // 返回完成令牌资格
		.o_result_data(wire_core_result_data),  // 返回舍入饱和数值
		.o_result_tag(wire_core_result_tag),    // 返回原始源身份
		.o_fault(flag_core_result_fault)        // 返回非法移位标志
	);

endmodule
