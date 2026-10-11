`timescale 1ns / 1ps

////////////////////////////////////English///////////////////////////////////////
// Company:         Erie
// Engineer:        Erie
//
// Create Date:     2026/10/04 00:00:00
// Design Name:     tb_road_mac_stream_probe
// Module Name:     tb_road_mac_stream_probe
// Description:     description/tb_road_mac_stream_probe_Design.pdf
// Simulations:     testbench/iverilog/road_mac_stream_probe
//
// Referrences:     cnn/hw_validation/mac/mac_reference.py
//
// Dependencies:    road_mac_stream_probe.v road_mac_probe.v
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
// 设计名称:        tb_road_mac_stream_probe
// 模块名称:        tb_road_mac_stream_probe
// 模块说明:        Description/tb_road_mac_stream_probe_Design.pdf
// 仿真工程:        TestBench/Icarus/road_mac_stream_probe
//
// 参考资料:        cnn/hw_validation/mac/mac_reference.py
//
// 依赖文件:        road_mac_stream_probe.v road_mac_probe.v
//
// 当前版本:        V1.0
// 修订日期:        2026年10月04日
// 修订历史:
// 时间             版本        修订人            修订内容
// 2026年10月04日   V1.0        Erie              创建文件

//三十二位动态装载乘加资源探针自检测试台
module tb_road_mac_stream_probe;

	//--------------寄存器信号--------------//
	//被测包装层输入驱动
	reg reg_clk = 0;                          // 十纳秒周期仿真时钟
	reg reg_rstn = 0;                        // 被测模块异步低有效复位
	reg reg_command_valid = 0;               // 当前命令负载有效驱动
	reg [1:0]reg_command_opcode = 0;          // 当前命令类别驱动
	reg [2:0]reg_command_index = 0;           // 当前命令字序号驱动
	reg [31:0]reg_command_data = 0;           // 当前三十二位动态负载
	reg reg_result_ready = 0;                // 结果通道背压驱动

	//Python向量输入与期望数据
	reg [7:0]reg_lane_mask = 0;              // 当前向量通道掩码
	reg [63:0]reg_activation_data = 0;       // 当前八通道激活负载
	reg [191:0]reg_weight_data = 0;          // 当前三组八通道权重负载
	reg [95:0]reg_bias_data = 0;             // 当前三路偏置负载
	reg [95:0]reg_expected_data = 0;         // Python给出的期望结果
	reg [383:0]reg_expected_products = 0;    // Python给出的二十四项乘积bank
	reg [203:0]reg_expected_pairs = 0;       // Python给出的十二项相邻对bank
	reg [107:0]reg_expected_quads = 0;       // Python给出的六项四输入bank
	reg [56:0]reg_expected_dots = 0;         // Python给出的三项八输入点积bank
	reg [95:0]reg_stalled_data = 0;          // 输出停顿期间的数据快照
	reg reg_stalled_fault = 0;               // 输出停顿期间的故障快照
	reg [1023:0]reg_vector_path = 0;         // 运行参数提供的向量文件路径

	//---------------其他信号---------------//
	//包装层可见输出及核心中间bank
	wire flag_command_ready;                 // 包装层命令就绪状态
	wire flag_result_valid;                  // 包装层结果有效状态
	wire [95:0]result_data;                  // 包装层三路结果负载
	wire flag_fault;                         // 包装层越界故障状态
	wire [383:0]product_bank_observed;       // 拼接核心二十四项乘积供对拍
	wire [203:0]pair_bank_observed;          // 拼接核心十二项相邻对供对拍
	wire [107:0]quad_bank_observed;          // 拼接核心六项四输入和供对拍
	wire [56:0]dot_bank_observed;            // 拼接核心三项点积供对拍

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

	//------------模块实例化区域------------//
	//三十二位动态装载资源探针被测实例
	road_mac_stream_probe road_mac_stream_probe_Inst_dut(
		.i_clk(reg_clk),                       // 连接十纳秒周期仿真时钟
		.i_rstn(reg_rstn),                     // 连接异步低有效复位驱动
		.i_command_valid(reg_command_valid),   // 连接命令有效驱动
		.i_command_opcode(reg_command_opcode), // 连接命令类别驱动
		.i_command_index(reg_command_index),   // 连接类别内字序号驱动
		.i_command_data(reg_command_data),     // 连接动态三十二位负载
		.i_result_ready(reg_result_ready),     // 连接结果下游就绪驱动
		.o_command_ready(flag_command_ready),  // 观察合法命令接受能力
		.o_result_valid(flag_result_valid),    // 观察终态有效状态
		.o_result_data(result_data),           // 观察三路结果负载
		.o_fault(flag_fault)                   // 观察溢出故障属性
	);

	assign product_bank_observed = {
		road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.reg_product_gamma_eighth,
		road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.reg_product_gamma_seventh,
		road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.reg_product_gamma_sixth,
		road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.reg_product_gamma_fifth,
		road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.reg_product_gamma_fourth,
		road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.reg_product_gamma_third,
		road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.reg_product_gamma_second,
		road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.reg_product_gamma_first,
		road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.reg_product_beta_eighth,
		road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.reg_product_beta_seventh,
		road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.reg_product_beta_sixth,
		road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.reg_product_beta_fifth,
		road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.reg_product_beta_fourth,
		road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.reg_product_beta_third,
		road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.reg_product_beta_second,
		road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.reg_product_beta_first,
		road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.reg_product_alpha_eighth,
		road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.reg_product_alpha_seventh,
		road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.reg_product_alpha_sixth,
		road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.reg_product_alpha_fifth,
		road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.reg_product_alpha_fourth,
		road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.reg_product_alpha_third,
		road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.reg_product_alpha_second,
		road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.reg_product_alpha_first
	};                                      // 保持Python输出优先和低lane优先布局
	assign pair_bank_observed = {
		road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.reg_pair_gamma_fourth,
		road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.reg_pair_gamma_third,
		road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.reg_pair_gamma_second,
		road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.reg_pair_gamma_first,
		road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.reg_pair_beta_fourth,
		road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.reg_pair_beta_third,
		road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.reg_pair_beta_second,
		road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.reg_pair_beta_first,
		road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.reg_pair_alpha_fourth,
		road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.reg_pair_alpha_third,
		road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.reg_pair_alpha_second,
		road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.reg_pair_alpha_first
	};                                      // 保持十二项相邻对Python布局
	assign quad_bank_observed = {
		road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.reg_quad_gamma_second,
		road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.reg_quad_gamma_first,
		road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.reg_quad_beta_second,
		road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.reg_quad_beta_first,
		road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.reg_quad_alpha_second,
		road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.reg_quad_alpha_first
	};                                      // 保持六项四输入和Python布局
	assign dot_bank_observed = {
		road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.reg_dot_gamma,
		road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.reg_dot_beta,
		road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.reg_dot_alpha
	};                                      // 保持三项点积Python布局

	//--------------任务定义区域--------------//
	//保持单个命令直到合法地址完成真实握手
	task send_command;
		input [1:0]task_opcode;
		input [2:0]task_index;
		input [31:0]task_data;
		begin
			@(negedge reg_clk);
			reg_command_opcode = task_opcode;
			reg_command_index = task_index;
			reg_command_data = task_data;
			reg_command_valid = 1'b1;
			cnt_wait = 0;
			while(flag_command_ready !== 1'b1)begin
				@(posedge reg_clk);
				#1;
				cnt_wait = cnt_wait + 1;
				if(cnt_wait > 64)begin
					$display(" > ERR: [Verilog] command timeout case=%0d opcode=%0d index=%0d", cnt_case, task_opcode, task_index);
					cnt_error = cnt_error + 1;
					$finish;
				end
			end
			@(posedge reg_clk);
			#1;
			@(negedge reg_clk);
			reg_command_valid = 1'b0;
		end
	endtask

	//按冻结十二字事务装载一个完整核心输入拍
	task load_current_beat;
		begin
			send_command(2'b00, 3'd0, reg_activation_data[31:0]);
			send_command(2'b00, 3'd1, reg_activation_data[63:32]);
			send_command(2'b01, 3'd0, reg_weight_data[31:0]);
			send_command(2'b01, 3'd1, reg_weight_data[63:32]);
			send_command(2'b01, 3'd2, reg_weight_data[95:64]);
			send_command(2'b01, 3'd3, reg_weight_data[127:96]);
			send_command(2'b01, 3'd4, reg_weight_data[159:128]);
			send_command(2'b01, 3'd5, reg_weight_data[191:160]);
			send_command(2'b10, 3'd0, reg_bias_data[31:0]);
			send_command(2'b10, 3'd1, reg_bias_data[63:32]);
			send_command(2'b10, 3'd2, reg_bias_data[95:64]);
			send_command(2'b11, 3'd0, {22'd0, enc_last[0], enc_first[0], reg_lane_mask});
		end
	endtask

	//--------------初始化区域--------------//
	//产生持续运行的百兆等效仿真时钟
	always begin
		#5 reg_clk = ~reg_clk;
	end

	//限制失控仿真的最长运行时间
	initial begin
		#3000000;
		$display(" > ERR: [Verilog] timeout cases=%0d errors=%0d", cnt_case, cnt_error);
		$finish;
	end

	//读取Python向量并验证串行装载后的真实核心数值
	initial begin
		repeat(4)begin
			@(posedge reg_clk);
		end
		@(negedge reg_clk);
		reg_rstn = 1'b1;

		//乱序首字只能形成未完整事务且不得启动核心
		reg_command_opcode = 2'b11;
		reg_command_index = 3'd1;
		reg_command_data = 32'hffffffff;
		reg_command_valid = 1'b1;
		#1;
		if(flag_command_ready !== 1'b1)begin
			$display(" > ERR: [Verilog] command buffer did not accept malformed first word");
			cnt_error = cnt_error + 1;
		end
		@(posedge reg_clk);
		#1;
		reg_command_valid = 1'b0;
		@(posedge reg_clk);
		#1;
		if((road_mac_stream_probe_Inst_dut.flag_all_loaded !== 1'b0) || (flag_result_valid !== 1'b0))begin
			$display(" > ERR: [Verilog] malformed partial transaction launched core");
			cnt_error = cnt_error + 1;
		end
		//窄接口契约要求乱序事务由上层复位丢弃
		@(negedge reg_clk);
		reg_rstn = 1'b0;
		#1;
		if((road_mac_stream_probe_Inst_dut.reg_progress !== 13'b0000000000001) || (road_mac_stream_probe_Inst_dut.flag_command_pending !== 1'b0))begin
			$display(" > ERR: [Verilog] reset failed to discard malformed transaction");
			cnt_error = cnt_error + 1;
		end
		@(negedge reg_clk);
		reg_rstn = 1'b1;

		if($value$plusargs("VECTORS=%s", reg_vector_path) == 1'b0)begin
			reg_vector_path = "mac_vectors.txt";
		end
		file_vectors = $fopen(reg_vector_path, "r");
		if(file_vectors == 0)begin
			$display(" > ERR: [Verilog] cannot open vectors path=%0s", reg_vector_path);
			$finish;
		end

		while(!$feof(file_vectors))begin
			status_scan = $fscanf(file_vectors, "%d %d %h %h %h %h %d %d %h %h %h %h %h\n", enc_first, enc_last, reg_lane_mask, reg_activation_data, reg_weight_data, reg_bias_data, enc_emit, enc_fault, reg_expected_data, reg_expected_products, reg_expected_pairs, reg_expected_quads, reg_expected_dots);
			if(status_scan == 13)begin
				load_current_beat;
				while((road_mac_stream_probe_Inst_dut.flag_all_loaded !== 1'b1) || (road_mac_stream_probe_Inst_dut.flag_core_input_ready !== 1'b1))begin
					@(negedge reg_clk);
				end
				@(posedge reg_clk);
				#1;
				cnt_case = cnt_case + 1;

				@(posedge reg_clk);
				#1;
				if((road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.flag_product_valid !== 1'b1) || (product_bank_observed !== reg_expected_products))begin
					$display(" > ERR: [Verilog] product bank mismatch case=%0d", cnt_case);
					cnt_error = cnt_error + 1;
				end
				@(posedge reg_clk);
				#1;
				if((road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.flag_stage_valid[0] !== 1'b1) || (pair_bank_observed !== reg_expected_pairs))begin
					$display(" > ERR: [Verilog] pair bank mismatch case=%0d", cnt_case);
					cnt_error = cnt_error + 1;
				end
				@(posedge reg_clk);
				#1;
				if((road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.flag_stage_valid[1] !== 1'b1) || (quad_bank_observed !== reg_expected_quads))begin
					$display(" > ERR: [Verilog] quad bank mismatch case=%0d", cnt_case);
					cnt_error = cnt_error + 1;
				end
				@(posedge reg_clk);
				#1;
				if((road_mac_stream_probe_Inst_dut.road_mac_probe_Inst_core.flag_stage_valid[2] !== 1'b1) || (dot_bank_observed !== reg_expected_dots))begin
					$display(" > ERR: [Verilog] dot bank mismatch case=%0d", cnt_case);
					cnt_error = cnt_error + 1;
				end

				if(enc_emit != 0)begin
					reg_result_ready = 1'b0;
					cnt_wait = 4;
					while(flag_result_valid !== 1'b1)begin
						@(posedge reg_clk);
						#1;
						cnt_wait = cnt_wait + 1;
						if(cnt_wait > 64)begin
							$display(" > ERR: [Verilog] result timeout case=%0d", cnt_case);
							cnt_error = cnt_error + 1;
							$finish;
						end
					end
					if(cnt_wait != 9)begin
						$display(" > ERR: [Verilog] core latency mismatch case=%0d got=%0d exp=9", cnt_case, cnt_wait);
						cnt_error = cnt_error + 1;
					end
					if((flag_fault !== enc_fault[0]) || (result_data !== reg_expected_data))begin
						$display(" > ERR: [Verilog] terminal mismatch case=%0d got=%024h/%0b exp=%024h/%0b", cnt_case, result_data, flag_fault, reg_expected_data, enc_fault[0]);
						cnt_error = cnt_error + 1;
					end
					if((enc_fault != 0) && (result_data !== 96'd0))begin
						$display(" > ERR: [Verilog] overflow payload was not zero case=%0d", cnt_case);
						cnt_error = cnt_error + 1;
					end
					reg_stalled_data = result_data;
					reg_stalled_fault = flag_fault;
					repeat(3)begin
						@(posedge reg_clk);
						#1;
						if((flag_result_valid !== 1'b1) || (result_data !== reg_stalled_data) || (flag_fault !== reg_stalled_fault))begin
							$display(" > ERR: [Verilog] stalled output changed case=%0d", cnt_case);
							cnt_error = cnt_error + 1;
						end
					end
					@(negedge reg_clk);
					reg_result_ready = 1'b1;
					@(posedge reg_clk);
					#1;
					@(negedge reg_clk);
					reg_result_ready = 1'b0;
				end else if(flag_result_valid !== 1'b0)begin
					$display(" > ERR: [Verilog] non-last beat published case=%0d", cnt_case);
					cnt_error = cnt_error + 1;
				end
			end
		end
		$fclose(file_vectors);

		//完整动态装载进入归约后异步复位必须取消包装层和核心状态
		reg_activation_data = 64'h0807060504030201;
		reg_weight_data = {24{8'h01}};
		reg_bias_data = 96'd0;
		reg_lane_mask = 8'hff;
		enc_first = 1;
		enc_last = 1;
		load_current_beat;
		while((road_mac_stream_probe_Inst_dut.flag_all_loaded !== 1'b1) || (road_mac_stream_probe_Inst_dut.flag_core_input_ready !== 1'b1))begin
			@(negedge reg_clk);
		end
		@(posedge reg_clk);
		repeat(2)begin
			@(posedge reg_clk);
		end
		@(negedge reg_clk);
		reg_rstn = 1'b0;
		#1;
		if((flag_result_valid !== 1'b0) || (road_mac_stream_probe_Inst_dut.reg_progress !== 13'b0000000000001) || (road_mac_stream_probe_Inst_dut.flag_command_pending !== 1'b0) || (road_mac_stream_probe_Inst_dut.flag_all_loaded !== 1'b0))begin
			$display(" > ERR: [Verilog] reset failed to cancel wrapper or core state");
			cnt_error = cnt_error + 1;
		end
		@(negedge reg_clk);
		reg_rstn = 1'b1;
		reg_command_opcode = 2'b00;
		reg_command_index = 3'd0;
		#1;
		if(flag_command_ready !== 1'b1)begin
			$display(" > ERR: [Verilog] reset failed to reopen command input");
			cnt_error = cnt_error + 1;
		end

		if(cnt_error == 0)begin
			$display("VERILOG-GEN-RESULT PASS cases=%0d errors=%0d reset=1 dynamic_words=12 io=140", cnt_case, cnt_error);
		end else begin
			$display("VERILOG-GEN-RESULT FAIL cases=%0d errors=%0d reset=1 dynamic_words=12 io=140", cnt_case, cnt_error);
		end
		$finish;
	end

endmodule
