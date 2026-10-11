`timescale 1ns / 1ps

////////////////////////////////////English///////////////////////////////////////
// Company:         Erie
// Engineer:        Erie
//
// Create Date:     2026/10/04 00:00:00
// Design Name:     tb_road_mac_probe
// Module Name:     tb_road_mac_probe
// Description:     description/tb_road_mac_probe_Design.pdf
// Simulations:     testbench/iverilog/road_mac_probe
//
// Referrences:     cnn/hw_validation/mac/mac_reference.py
//
// Dependencies:    road_mac_probe.v
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
// 设计名称:        tb_road_mac_probe
// 模块名称:        tb_road_mac_probe
// 模块说明:        Description/tb_road_mac_probe_Design.pdf
// 仿真工程:        TestBench/Icarus/road_mac_probe
//
// 参考资料:        cnn/hw_validation/mac/mac_reference.py
//
// 依赖文件:        road_mac_probe.v
//
// 当前版本:        V1.0
// 修订日期:        2026年10月04日
// 修订历史:
// 时间             版本        修订人            修订内容
// 2026年10月04日   V1.0        Erie              创建文件

//道路检测乘加探针自检测试台
module tb_road_mac_probe;

	//--------------寄存器信号--------------//
	//被测模块输入驱动
	reg reg_clk = 0;                          // 十纳秒周期仿真时钟
	reg reg_rstn = 0;                        // 被测模块异步低有效复位
	reg reg_input_valid = 0;                 // 当前向量输入有效驱动
	reg reg_first = 0;                       // 当前向量首拍属性
	reg reg_last = 0;                        // 当前向量末拍属性
	reg [7:0]reg_lane_mask = 0;              // 当前向量通道掩码
	reg [63:0]reg_activation_data = 0;       // 当前八通道激活负载
	reg [191:0]reg_weight_data = 0;          // 当前三组八通道权重负载
	reg [95:0]reg_bias_data = 0;             // 当前三路偏置负载
	reg reg_result_ready = 0;                // 结果通道背压驱动

	//期望值与背压保持快照
	reg [95:0]reg_expected_data = 0;         // Python向量给出的期望结果
	reg [383:0]reg_expected_products = 0;    // Python给出的二十四项乘积bank
	reg [203:0]reg_expected_pairs = 0;       // Python给出的十二项相邻对bank
	reg [107:0]reg_expected_quads = 0;       // Python给出的六项四输入bank
	reg [56:0]reg_expected_dots = 0;         // Python给出的三项八输入点积bank
	reg [95:0]reg_stalled_data = 0;          // 输出停顿期间的数据快照
	reg reg_stalled_fault = 0;               // 输出停顿期间的故障快照
	reg [1023:0]reg_vector_path = 0;         // 运行参数提供的向量文件路径

	//---------------其他信号---------------//
	//被测模块可见输出
	wire flag_input_ready;                   // 被测模块输入就绪状态
	wire flag_result_valid;                  // 被测模块结果有效状态
	wire [95:0]result_data;                  // 被测模块三路结果负载
	wire flag_fault;                         // 被测模块越界故障状态
	wire [383:0]product_bank_observed;       // 拼接二十四项乘积供整组对拍
	wire [203:0]pair_bank_observed;          // 拼接十二项相邻对供整组对拍
	wire [107:0]quad_bank_observed;          // 拼接六项四输入和供整组对拍
	wire [56:0]dot_bank_observed;            // 拼接三项点积供整组对拍

	//仿真文件与检查计数
	integer file_vectors = 0;                // Python向量输入文件句柄
	integer status_scan = 0;                 // 单行字段扫描返回数量
	integer cnt_case = 0;                    // 已完成对拍向量数量
	integer cnt_error = 0;                   // 累计自检失败数量
	integer cnt_wait = 0;                    // 单阶段超时保护计数
	integer enc_first = 0;                   // 文件读取的首拍属性
	integer enc_last = 0;                    // 文件读取的末拍属性
	integer enc_emit = 0;                    // 文件读取的终态产生属性
	integer enc_fault = 0;                   // 文件读取的故障期望属性
	integer enc_previous_emit = 0;           // 前一拍是否经过三周期终态背压
	integer time_previous_accept = 0;        // 前一输入握手的仿真时间
	integer cnt_accept_interval = 0;         // 相邻输入握手间隔周期

	//------------模块实例化区域------------//
	//八输入三输出乘加探针被测实例
	road_mac_probe road_mac_probe_Inst_dut(
		.i_clk(reg_clk),                      // 连接十纳秒周期仿真时钟
		.i_rstn(reg_rstn),                    // 连接异步低有效复位驱动
		.i_input_valid(reg_input_valid),      // 连接向量输入有效驱动
		.i_first(reg_first),                  // 连接向量首拍属性驱动
		.i_last(reg_last),                    // 连接向量末拍属性驱动
		.i_lane_mask(reg_lane_mask),          // 连接八通道共享掩码
		.i_activation_data(reg_activation_data), // 连接八个有符号激活值
		.i_weight_data(reg_weight_data),      // 连接二十四个有符号权重
		.i_bias_data(reg_bias_data),          // 连接三路有符号偏置值
		.i_result_ready(reg_result_ready),    // 连接结果下游就绪驱动
		.o_input_ready(flag_input_ready),     // 观察被测模块输入就绪状态
		.o_result_valid(flag_result_valid),   // 观察被测模块终态有效状态
		.o_result_data(result_data),          // 观察被测模块三路结果负载
		.o_fault(flag_fault)                  // 观察被测模块溢出故障属性
	);

	assign product_bank_observed = {
		road_mac_probe_Inst_dut.reg_product_gamma_eighth,
		road_mac_probe_Inst_dut.reg_product_gamma_seventh,
		road_mac_probe_Inst_dut.reg_product_gamma_sixth,
		road_mac_probe_Inst_dut.reg_product_gamma_fifth,
		road_mac_probe_Inst_dut.reg_product_gamma_fourth,
		road_mac_probe_Inst_dut.reg_product_gamma_third,
		road_mac_probe_Inst_dut.reg_product_gamma_second,
		road_mac_probe_Inst_dut.reg_product_gamma_first,
		road_mac_probe_Inst_dut.reg_product_beta_eighth,
		road_mac_probe_Inst_dut.reg_product_beta_seventh,
		road_mac_probe_Inst_dut.reg_product_beta_sixth,
		road_mac_probe_Inst_dut.reg_product_beta_fifth,
		road_mac_probe_Inst_dut.reg_product_beta_fourth,
		road_mac_probe_Inst_dut.reg_product_beta_third,
		road_mac_probe_Inst_dut.reg_product_beta_second,
		road_mac_probe_Inst_dut.reg_product_beta_first,
		road_mac_probe_Inst_dut.reg_product_alpha_eighth,
		road_mac_probe_Inst_dut.reg_product_alpha_seventh,
		road_mac_probe_Inst_dut.reg_product_alpha_sixth,
		road_mac_probe_Inst_dut.reg_product_alpha_fifth,
		road_mac_probe_Inst_dut.reg_product_alpha_fourth,
		road_mac_probe_Inst_dut.reg_product_alpha_third,
		road_mac_probe_Inst_dut.reg_product_alpha_second,
		road_mac_probe_Inst_dut.reg_product_alpha_first
	};                                      // 保持Python输出优先和低lane优先布局
	assign pair_bank_observed = {
		road_mac_probe_Inst_dut.reg_pair_gamma_fourth,
		road_mac_probe_Inst_dut.reg_pair_gamma_third,
		road_mac_probe_Inst_dut.reg_pair_gamma_second,
		road_mac_probe_Inst_dut.reg_pair_gamma_first,
		road_mac_probe_Inst_dut.reg_pair_beta_fourth,
		road_mac_probe_Inst_dut.reg_pair_beta_third,
		road_mac_probe_Inst_dut.reg_pair_beta_second,
		road_mac_probe_Inst_dut.reg_pair_beta_first,
		road_mac_probe_Inst_dut.reg_pair_alpha_fourth,
		road_mac_probe_Inst_dut.reg_pair_alpha_third,
		road_mac_probe_Inst_dut.reg_pair_alpha_second,
		road_mac_probe_Inst_dut.reg_pair_alpha_first
	};                                      // 保持十二项相邻对Python布局
	assign quad_bank_observed = {
		road_mac_probe_Inst_dut.reg_quad_gamma_second,
		road_mac_probe_Inst_dut.reg_quad_gamma_first,
		road_mac_probe_Inst_dut.reg_quad_beta_second,
		road_mac_probe_Inst_dut.reg_quad_beta_first,
		road_mac_probe_Inst_dut.reg_quad_alpha_second,
		road_mac_probe_Inst_dut.reg_quad_alpha_first
	};                                      // 保持六项四输入和Python布局
	assign dot_bank_observed = {
		road_mac_probe_Inst_dut.reg_dot_gamma,
		road_mac_probe_Inst_dut.reg_dot_beta,
		road_mac_probe_Inst_dut.reg_dot_alpha
	};                                      // 保持三项点积Python布局

	//--------------初始化区域--------------//
	//产生持续运行的百兆等效仿真时钟
	always begin
		#5 reg_clk = ~reg_clk;                // 每五纳秒翻转一次时钟
	end

	//限制失控仿真的最长运行时间
	initial begin
		#2000000;                             // 允许全部向量完成握手
		$display(" > ERR: [Verilog] timeout cases=%0d errors=%0d", cnt_case, cnt_error); // 报告全局超时
		$finish;                              // 超时后终止仿真进程
	end

	//读取Python向量并执行逐项自检
	initial begin
		reg_input_valid = 1'b0;               // 启动时不声明输入负载
		reg_result_ready = 1'b0;              // 启动时对结果施加背压
		reg_first = 1'b0;                     // 启动时清除首拍属性
		reg_last = 1'b0;                      // 启动时清除末拍属性
		reg_lane_mask = 8'd0;                 // 启动时关闭全部输入通道
		reg_activation_data = 64'd0;          // 启动时清空激活负载
		reg_weight_data = 192'd0;             // 启动时清空权重负载
		reg_bias_data = 96'd0;                // 启动时清空偏置负载
		repeat(4)begin
			@(posedge reg_clk);                 // 保持复位跨越四个工作边沿
		end
		@(negedge reg_clk);                   // 在安全半周期释放复位
		reg_rstn = 1'b1;                     // 开始正常向量执行

		if($value$plusargs("VECTORS=%s", reg_vector_path) == 1'b0)begin
			reg_vector_path = "mac_vectors.txt"; // 使用本目录默认生成向量
		end
		file_vectors = $fopen(reg_vector_path, "r"); // 打开Python冻结的文本向量
		if(file_vectors == 0)begin
			$display(" > ERR: [Verilog] cannot open vectors path=%0s", reg_vector_path); // 报告向量文件缺失
			$finish;                           // 无参考向量时禁止伪通过
		end

		while(!$feof(file_vectors))begin
			status_scan = $fscanf(file_vectors, "%d %d %h %h %h %h %d %d %h %h %h %h %h\n", enc_first, enc_last, reg_lane_mask, reg_activation_data, reg_weight_data, reg_bias_data, enc_emit, enc_fault, reg_expected_data, reg_expected_products, reg_expected_pairs, reg_expected_quads, reg_expected_dots); // 读取一个完整参考向量
			if(status_scan == 13)begin
				@(negedge reg_clk);               // 在下降沿建立稳定输入负载
				reg_first = enc_first[0];         // 驱动参考向量首拍属性
				reg_last = enc_last[0];           // 驱动参考向量末拍属性
				reg_input_valid = 1'b1;           // 保持输入有效直到真实握手
				cnt_wait = 0;                     // 清零本次输入等待计数
				while(flag_input_ready !== 1'b1)begin
					@(posedge reg_clk);             // 等待被测模块释放单在途通路
					#1;                             // 避免与时序非阻塞更新竞争
					cnt_wait = cnt_wait + 1;        // 累计输入背压持续周期
					if(cnt_wait > 64)begin
						$display(" > ERR: [Verilog] input timeout case=%0d", cnt_case); // 报告输入通道停滞
						cnt_error = cnt_error + 1;    // 记录输入等待超时失败
						$finish;                      // 协议停滞时立即终止
					end
				end
				@(posedge reg_clk);               // 就绪与有效同时成立并接受输入
				#1;                               // 等待被测模块锁存当前负载
				reg_input_valid = 1'b0;           // 握手后撤销输入有效标志
				if(cnt_case != 0)begin
					cnt_accept_interval = ($time - time_previous_accept) / 10; // 换算十纳秒时钟周期间隔
					if(((enc_previous_emit == 0) && (cnt_accept_interval != 11)) || ((enc_previous_emit != 0) && (cnt_accept_interval != 16)))begin
						$display(" > ERR: [Verilog] accept interval mismatch case=%0d got=%0d exp=%0d", cnt_case + 1, cnt_accept_interval, enc_previous_emit ? 16 : 11); // 报告单在途释放节拍不符
						cnt_error = cnt_error + 1;      // 记录输入接受间隔契约失败
					end
				end
				time_previous_accept = $time;     // 保存本次输入握手时刻
				enc_previous_emit = enc_emit;     // 保存本次输出路径供下一拍检查
				cnt_case = cnt_case + 1;          // 记录一个已接受参考向量

				@(posedge reg_clk);               // 接受后第一拍到达乘积寄存级
				#1;                               // 等待乘积bank非阻塞更新完成
				if((road_mac_probe_Inst_dut.flag_product_valid !== 1'b1) || (product_bank_observed !== reg_expected_products))begin
					$display(" > ERR: [Verilog] product bank mismatch case=%0d got=%096h exp=%096h", cnt_case, product_bank_observed, reg_expected_products); // 报告二十四项乘积不符
					cnt_error = cnt_error + 1;      // 记录乘积级对拍失败
				end
				@(posedge reg_clk);               // 接受后第二拍到达相邻对寄存级
				#1;                               // 等待相邻对bank非阻塞更新完成
				if((road_mac_probe_Inst_dut.flag_stage_valid[0] !== 1'b1) || (pair_bank_observed !== reg_expected_pairs))begin
					$display(" > ERR: [Verilog] pair bank mismatch case=%0d got=%051h exp=%051h", cnt_case, pair_bank_observed, reg_expected_pairs); // 报告十二项相邻对不符
					cnt_error = cnt_error + 1;      // 记录相邻对级对拍失败
				end
				@(posedge reg_clk);               // 接受后第三拍到达四输入寄存级
				#1;                               // 等待四输入bank非阻塞更新完成
				if((road_mac_probe_Inst_dut.flag_stage_valid[1] !== 1'b1) || (quad_bank_observed !== reg_expected_quads))begin
					$display(" > ERR: [Verilog] quad bank mismatch case=%0d got=%027h exp=%027h", cnt_case, quad_bank_observed, reg_expected_quads); // 报告六项四输入和不符
					cnt_error = cnt_error + 1;      // 记录四输入级对拍失败
				end
				@(posedge reg_clk);               // 接受后第四拍到达八输入点积级
				#1;                               // 等待点积bank非阻塞更新完成
				if((road_mac_probe_Inst_dut.flag_stage_valid[2] !== 1'b1) || (dot_bank_observed !== reg_expected_dots))begin
					$display(" > ERR: [Verilog] dot bank mismatch case=%0d got=%015h exp=%015h", cnt_case, dot_bank_observed, reg_expected_dots); // 报告三项八输入点积不符
					cnt_error = cnt_error + 1;      // 记录点积级对拍失败
				end

				if(enc_emit != 0)begin
					reg_result_ready = 1'b0;        // 强制输出保持以验证背压稳定性
					cnt_wait = 4;                   // 已观察接受后的四个归约周期
					while(flag_result_valid !== 1'b1)begin
						@(posedge reg_clk);            // 等待正常结果或故障终态
						#1;                            // 采样时避开非阻塞更新区
						cnt_wait = cnt_wait + 1;       // 累计内部流水延迟周期
						if(cnt_wait > 64)begin
							$display(" > ERR: [Verilog] result timeout case=%0d", cnt_case); // 报告终态缺失
							cnt_error = cnt_error + 1;   // 记录结果等待超时失败
							$finish;                     // 缺失终态时立即终止
						end
					end
					if(cnt_wait != 9)begin
						$display(" > ERR: [Verilog] terminal latency mismatch case=%0d got=%0d exp=9", cnt_case, cnt_wait); // 报告接受到终态的固定延迟不符
						cnt_error = cnt_error + 1;      // 记录终态延迟契约失败
					end
					if(flag_fault !== enc_fault[0])begin
						$display(" > ERR: [Verilog] fault mismatch case=%0d got=%0b exp=%0b", cnt_case, flag_fault, enc_fault[0]); // 报告故障属性不符
						cnt_error = cnt_error + 1;    // 记录故障属性对拍失败
					end
					if(result_data !== reg_expected_data)begin
						$display(" > ERR: [Verilog] data mismatch case=%0d got=%024h exp=%024h", cnt_case, result_data, reg_expected_data); // 报告正常数值或故障零值不符
						cnt_error = cnt_error + 1;    // 记录三路数值对拍失败
					end
					if((enc_fault != 0) && (flag_result_valid & ~flag_fault))begin
						$display(" > ERR: [Verilog] overflow published success case=%0d", cnt_case); // 阻止溢出伪装为成功结果
						cnt_error = cnt_error + 1;    // 记录故障成功语义违规
					end
					reg_stalled_data = result_data; // 保存输出停顿开始时的数据
					reg_stalled_fault = flag_fault; // 保存输出停顿开始时的属性
					repeat(3)begin
						@(posedge reg_clk);            // 维持三周期结果背压
						#1;                            // 等待时序输出稳定
						if((flag_result_valid !== 1'b1) || (result_data !== reg_stalled_data) || (flag_fault !== reg_stalled_fault))begin
							$display(" > ERR: [Verilog] stalled output changed case=%0d", cnt_case); // 报告背压保持违规
							cnt_error = cnt_error + 1;   // 记录输出稳定性失败
						end
					end
					@(negedge reg_clk);             // 在下降沿开放结果接受
					reg_result_ready = 1'b1;        // 允许下游完成终态握手
					@(posedge reg_clk);             // 接受当前保持终态
					#1;                             // 等待有效寄存器撤销
					@(negedge reg_clk);             // 在半周期边界恢复背压
					reg_result_ready = 1'b0;        // 下一终态继续测试保持能力
				end else begin
					repeat(2)begin
						@(posedge reg_clk);            // 非末拍期间观察不应出现终态
						#1;                            // 避免边沿采样竞争
						if(flag_result_valid !== 1'b0)begin
							$display(" > ERR: [Verilog] non-last beat published case=%0d", cnt_case); // 报告过早发布终态
							cnt_error = cnt_error + 1;   // 记录非末拍输出违规
						end
					end
				end
			end
		end
		$fclose(file_vectors);                // 完成全部参考向量后关闭文件

		//流水处理中异步复位必须取消潜在终态
		@(negedge reg_clk);                   // 建立复位取消前的测试负载
		reg_first = 1'b1;                    // 取消场景从独立首拍开始
		reg_last = 1'b1;                     // 取消场景原本会产生结果
		reg_lane_mask = 8'hff;               // 取消场景启用全部输入通道
		reg_activation_data = {8{8'h01}};     // 取消场景每路激活取一
		reg_weight_data = {24{8'h01}};        // 取消场景每个权重取一
		reg_bias_data = 96'd0;                // 取消场景三路偏置清零
		reg_input_valid = 1'b1;               // 声明取消场景输入有效
		while(flag_input_ready !== 1'b1)begin
			@(posedge reg_clk);                 // 等待前序终态完全释放
			#1;                                 // 等待输出握手记账更新
		end
		@(posedge reg_clk);                   // 接受即将被复位取消的负载
		#1;                                   // 等待乘法级记录有效
		reg_input_valid = 1'b0;               // 撤销取消场景输入有效
		repeat(2)begin
			@(posedge reg_clk);                 // 让负载进入中间归约级
		end
		@(negedge reg_clk);                   // 在中间流水阶段拉低复位
		reg_rstn = 1'b0;                     // 异步取消全部内部状态
		#1;                                   // 等待异步复位传播
		if(flag_result_valid !== 1'b0)begin
			$display(" > ERR: [Verilog] reset failed to cancel result"); // 报告复位后仍存在终态
			cnt_error = cnt_error + 1;          // 记录复位取消失败
		end
		@(negedge reg_clk);                   // 保持至少一个完整复位周期
		reg_rstn = 1'b1;                     // 恢复正常工作状态
		#1;                                   // 等待组合输入就绪重新建立
		if(flag_input_ready !== 1'b1)begin
			$display(" > ERR: [Verilog] reset failed to reopen input"); // 报告复位后输入未恢复
			cnt_error = cnt_error + 1;          // 记录复位恢复失败
		end

		if(cnt_error == 0)begin
			$display("VERILOG-GEN-RESULT PASS cases=%0d errors=%0d reset=1", cnt_case, cnt_error); // 仅在真实比较全通过后打印成功
		end else begin
			$display("VERILOG-GEN-RESULT FAIL cases=%0d errors=%0d reset=1", cnt_case, cnt_error); // 汇总所有已记录失败
		end
		$finish;                              // 正常结束自检仿真
	end

endmodule
