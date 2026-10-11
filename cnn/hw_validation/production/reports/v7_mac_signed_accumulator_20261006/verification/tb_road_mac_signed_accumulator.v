`timescale 1ns / 1ps

////////////////////////////////////English///////////////////////////////////////
// Company:         Erie
// Engineer:        Erie
//
// Create Date:     2026/10/06 00:00:00
// Design Name:     tb_road_mac_signed_accumulator
// Module Name:     tb_road_mac_signed_accumulator
// Description:     tb_road_mac_signed_accumulator.spec.json
// Simulations:     ModelSim SE-64 2020.4
//
// Referrences:     signed33_reference.py
//
// Dependencies:    road_mac_probe.v
//
// Version:         V1.0
// Revision Date:   2026/10/06 00:00:00
// History:
// Time             Version     Revised by        Contents
// 2026/10/06       V1.0        Erie              Create file.
///////////////////////////////////Chinese////////////////////////////////////////
// 版权归属:        Erie
// 开发人员:        Erie
//
// 创建日期:        2026年10月06日
// 设计名称:        tb_road_mac_signed_accumulator
// 模块名称:        tb_road_mac_signed_accumulator
// 模块说明:        tb_road_mac_signed_accumulator.spec.json
// 仿真工程:        ModelSim SE-64 2020.4
//
// 参考资料:        signed33_reference.py
//
// 依赖文件:        road_mac_probe.v
//
// 当前版本:        V1.0
// 修订日期:        2026年10月06日
// 修订历史:
// 时间             版本        修订人            修订内容
// 2026年10月06日   V1.0        Erie              创建文件

//三十三位跨组累加语义定向自检测试台
module tb_road_mac_signed_accumulator;

	parameter MAX_VECTORS = 128;                // 冻结向量最大条目数

	//被测模块输入驱动
	reg reg_clk = 1'b0;                         // 十纳秒周期仿真时钟
	reg reg_rstn = 1'b0;                        // 异步低有效复位
	reg reg_input_valid = 1'b0;                 // 输入负载有效
	reg reg_first = 1'b0;                       // 当前拍开始新归约
	reg reg_last = 1'b0;                        // 当前拍结束归约
	reg [7:0]reg_lane_mask = 8'd0;              // 八路共享有效掩码
	reg [63:0]reg_activation_data = 64'd0;      // 八路有符号激活
	reg [191:0]reg_weight_data = 192'd0;        // 三组三路有符号权重
	reg [95:0]reg_bias_data = 96'd0;            // 三路INT32偏置
	reg reg_result_ready = 1'b0;                // 输出下游就绪

	//输入保持期快照
	reg [7:0]reg_hold_mask = 8'd0;              // 忙期掩码快照
	reg [63:0]reg_hold_activation = 64'd0;      // 忙期激活快照
	reg [191:0]reg_hold_weight = 192'd0;        // 忙期权重快照
	reg [95:0]reg_hold_bias = 96'd0;            // 忙期偏置快照
	reg reg_hold_first = 1'b0;                  // 忙期首拍快照
	reg reg_hold_last = 1'b0;                   // 忙期末拍快照

	//文本向量数组
	integer vec_case [0:MAX_VECTORS-1];         // 用例编号
	integer vec_beat [0:MAX_VECTORS-1];         // 用例内拍编号
	integer vec_first [0:MAX_VECTORS-1];        // 首拍属性
	integer vec_last [0:MAX_VECTORS-1];         // 末拍属性
	integer vec_emit [0:MAX_VECTORS-1];         // 终态产生属性
	integer vec_fault [0:MAX_VECTORS-1];        // 终态故障属性
	integer vec_stall [0:MAX_VECTORS-1];        // 输出背压周期数
	reg [7:0]vec_mask [0:MAX_VECTORS-1];        // 通道掩码
	reg [63:0]vec_activation [0:MAX_VECTORS-1]; // 激活负载
	reg [191:0]vec_weight [0:MAX_VECTORS-1];    // 权重负载
	reg [95:0]vec_bias [0:MAX_VECTORS-1];       // 偏置负载
	reg [95:0]vec_data [0:MAX_VECTORS-1];       // 期望终态数据
	reg [383:0]vec_products [0:MAX_VECTORS-1];  // 期望乘积bank
	reg [203:0]vec_pairs [0:MAX_VECTORS-1];     // 期望相邻对bank
	reg [107:0]vec_quads [0:MAX_VECTORS-1];     // 期望四输入bank
	reg [56:0]vec_dots [0:MAX_VECTORS-1];       // 期望八输入点积bank
	reg [98:0]vec_base [0:MAX_VECTORS-1];       // 期望三路三十三位基值
	reg [101:0]vec_candidate [0:MAX_VECTORS-1]; // 期望三路三十四位候选
	reg [98:0]vec_accumulator [0:MAX_VECTORS-1]; // 期望提交后三十三位累加器

	//被测模块输出与真实内部bank观察
	wire flag_input_ready;                     // 输入就绪
	wire flag_result_valid;                    // 输出有效
	wire [95:0]result_data;                    // 三路INT32终态
	wire flag_fault;                           // 三路原子故障属性
	wire [383:0]product_bank_observed;         // 二十四项真实乘积bank
	wire [203:0]pair_bank_observed;            // 十二项真实相邻对bank
	wire [107:0]quad_bank_observed;            // 六项真实四输入bank
	wire [56:0]dot_bank_observed;              // 三项真实八输入点积bank
	wire [98:0]base_bank_observed;             // 三路三十三位点积对齐基值
	wire [101:0]candidate_bank_observed;       // 三路三十四位候选
	wire [101:0]candidate_hold_observed;       // 三路三十四位候选保持级
	wire [101:0]candidate_final_observed;      // 三路三十四位候选判定级
	wire [98:0]accumulator_observed;           // 三路三十三位跨拍累加器

	//文件、模式与检查计数
	reg [2047:0]reg_vector_path = 0;           // 向量文件运行参数
	reg [2047:0]reg_trace_path = 0;            // 机器可读周期记录路径
	integer file_vectors = 0;                  // 向量文件句柄
	integer file_trace = 0;                    // 周期记录文件句柄
	integer status_scan = 0;                   // 单行字段扫描数量
	integer cnt_vector = 0;                    // 已载入向量数
	integer cnt_index = 0;                     // 当前向量索引
	integer cnt_error = 0;                     // 累计错误数
	integer cnt_cycle = 0;                     // 全局仿真时钟周期
	integer cnt_busy_hold = 0;                 // 输入有效且未就绪保持周期
	integer cnt_reset = 0;                     // 已执行复位取消点数
	integer cnt_ready_high = 0;                // 结果前预置就绪回归数
	integer cnt_wait = 0;                      // 局部超时保护
	integer cycle_accept = 0;                  // 当前输入接受周期
	integer cycle_previous_accept = -1;        // 前一输入接受周期
	integer expected_interval = 0;             // 期望相邻接受间隔
	integer flag_legacy_mode = 0;              // 旧核提前拒绝负例模式
	reg [95:0]reg_stalled_data = 96'd0;        // 背压输出数据快照
	reg reg_stalled_fault = 1'b0;              // 背压输出故障快照

	//八输入三输出乘加探针被测实例
	road_mac_probe road_mac_probe_Inst_dut(
		.i_clk(reg_clk),
		.i_rstn(reg_rstn),
		.i_input_valid(reg_input_valid),
		.i_first(reg_first),
		.i_last(reg_last),
		.i_lane_mask(reg_lane_mask),
		.i_activation_data(reg_activation_data),
		.i_weight_data(reg_weight_data),
		.i_bias_data(reg_bias_data),
		.i_result_ready(reg_result_ready),
		.o_input_ready(flag_input_ready),
		.o_result_valid(flag_result_valid),
		.o_result_data(result_data),
		.o_fault(flag_fault)
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
	};                                          // 低位保持alpha和低lane布局

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
	};                                          // 对拍全部相邻对寄存器

	assign quad_bank_observed = {
		road_mac_probe_Inst_dut.reg_quad_gamma_second,
		road_mac_probe_Inst_dut.reg_quad_gamma_first,
		road_mac_probe_Inst_dut.reg_quad_beta_second,
		road_mac_probe_Inst_dut.reg_quad_beta_first,
		road_mac_probe_Inst_dut.reg_quad_alpha_second,
		road_mac_probe_Inst_dut.reg_quad_alpha_first
	};                                          // 对拍全部四输入寄存器

	assign dot_bank_observed = {
		road_mac_probe_Inst_dut.reg_dot_gamma,
		road_mac_probe_Inst_dut.reg_dot_beta,
		road_mac_probe_Inst_dut.reg_dot_alpha
	};                                          // 对拍全部八输入点积寄存器
	assign base_bank_observed = road_mac_probe_Inst_dut.reg_base_dot; // 观察完整三十三位基值链末级
	assign candidate_bank_observed = {
		road_mac_probe_Inst_dut.reg_candidate_gamma,
		road_mac_probe_Inst_dut.reg_candidate_beta,
		road_mac_probe_Inst_dut.reg_candidate_alpha
	};                                          // 观察完整三十四位候选
	assign candidate_hold_observed = {
		road_mac_probe_Inst_dut.reg_candidate_gamma_hold,
		road_mac_probe_Inst_dut.reg_candidate_beta_hold,
		road_mac_probe_Inst_dut.reg_candidate_alpha_hold
	};                                          // 观察候选保持级全位
	assign candidate_final_observed = {
		road_mac_probe_Inst_dut.reg_candidate_gamma_final,
		road_mac_probe_Inst_dut.reg_candidate_beta_final,
		road_mac_probe_Inst_dut.reg_candidate_alpha_final
	};                                          // 观察候选判定级全位
	assign accumulator_observed = road_mac_probe_Inst_dut.reg_accumulator; // 观察完整三十三位写回

	//持续运行的百兆等效仿真时钟
	always begin
		#5 reg_clk = ~reg_clk;
	end

	//周期计数不随被测复位归零，便于跨复位记录
	always@(posedge reg_clk)begin
		cnt_cycle = cnt_cycle + 1;
	end

	//输入在有效且未就绪期间必须由驱动端保持稳定
	always@(posedge reg_clk)begin
		#1;
		if((reg_input_valid == 1'b1) && (flag_input_ready == 1'b0))begin
			cnt_busy_hold = cnt_busy_hold + 1;
			if((reg_first !== reg_hold_first) || (reg_last !== reg_hold_last) ||
			   (reg_lane_mask !== reg_hold_mask) || (reg_activation_data !== reg_hold_activation) ||
			   (reg_weight_data !== reg_hold_weight) || (reg_bias_data !== reg_hold_bias))begin
				$display(" > ERR: busy input payload changed cycle=%0d", cnt_cycle);
				cnt_error = cnt_error + 1;
			end
		end
	end

	//限制失控仿真的最长运行时间
	initial begin
		#5000000;
		$display(" > ERR: timeout vectors=%0d errors=%0d", cnt_vector, cnt_error);
		$finish;
	end

	//把一条冻结向量建立到输入接口并保存保持期快照
	task drive_vector;
		input integer index;
		begin
			reg_first = vec_first[index][0];
			reg_last = vec_last[index][0];
			reg_lane_mask = vec_mask[index];
			reg_activation_data = vec_activation[index];
			reg_weight_data = vec_weight[index];
			reg_bias_data = vec_bias[index];
			reg_hold_first = vec_first[index][0];
			reg_hold_last = vec_last[index][0];
			reg_hold_mask = vec_mask[index];
			reg_hold_activation = vec_activation[index];
			reg_hold_weight = vec_weight[index];
			reg_hold_bias = vec_bias[index];
			reg_input_valid = 1'b1;
		end
	endtask

	//等待当前稳定输入被接受并记录机器可读周期
	task accept_current;
		input integer index;
		begin
			cnt_wait = 0;
			while(flag_input_ready !== 1'b1)begin
				@(posedge reg_clk);
				#1;
				cnt_wait = cnt_wait + 1;
				if(cnt_wait > 128)begin
					$display(" > ERR: input timeout vector=%0d", index);
					cnt_error = cnt_error + 1;
					$finish;
				end
			end
			@(posedge reg_clk);
			#1;
			cycle_accept = cnt_cycle;
			$fwrite(file_trace, "%0d,accept,%0d,%0d,%0d,%0d,%0d\n",
				cnt_cycle, vec_case[index], vec_beat[index], vec_first[index], vec_last[index], vec_stall[index]);
			if(cycle_previous_accept >= 0)begin
				expected_interval = vec_emit[index-1] ? (13 + vec_stall[index-1]) : 11;
				if((cycle_accept - cycle_previous_accept) != expected_interval)begin
					$display(" > ERR: accept interval vector=%0d got=%0d exp=%0d", index,
						cycle_accept - cycle_previous_accept, expected_interval);
					cnt_error = cnt_error + 1;
				end
			end
			cycle_previous_accept = cycle_accept;
			@(negedge reg_clk);
			reg_input_valid = 1'b0;
		end
	endtask

	//检查候选正常模式下的一条输入拍及固定流水周期
	task check_candidate_vector;
		input integer index;
		integer hold_index;
		begin
			@(posedge reg_clk);
			#1;
			if((road_mac_probe_Inst_dut.flag_product_valid !== 1'b1) ||
			   (product_bank_observed !== vec_products[index]))begin
				$display(" > ERR: product bank vector=%0d", index);
				cnt_error = cnt_error + 1;
			end
			@(posedge reg_clk);
			#1;
			if((road_mac_probe_Inst_dut.flag_stage_valid[0] !== 1'b1) ||
			   (pair_bank_observed !== vec_pairs[index]))begin
				$display(" > ERR: pair bank vector=%0d", index);
				cnt_error = cnt_error + 1;
			end
			@(posedge reg_clk);
			#1;
			if((road_mac_probe_Inst_dut.flag_stage_valid[1] !== 1'b1) ||
			   (quad_bank_observed !== vec_quads[index]))begin
				$display(" > ERR: quad bank vector=%0d", index);
				cnt_error = cnt_error + 1;
			end
			@(posedge reg_clk);
			#1;
			if((road_mac_probe_Inst_dut.flag_stage_valid[2] !== 1'b1) ||
			   (dot_bank_observed !== vec_dots[index]) || (base_bank_observed !== vec_base[index]))begin
				$display(" > ERR: dot/base bank vector=%0d got_base=%025h exp_base=%025h",
					index, base_bank_observed, vec_base[index]);
				cnt_error = cnt_error + 1;
			end

			//尽早建立下一拍，覆盖输入忙保持且不改变原有接受间隔。
			@(negedge reg_clk);
			if(index + 1 < cnt_vector)begin
				drive_vector(index + 1);
			end else begin
				reg_input_valid = 1'b0;
			end

			@(posedge reg_clk);
			#1;
			if((road_mac_probe_Inst_dut.flag_stage_valid[3] !== 1'b1) ||
			   (candidate_bank_observed !== vec_candidate[index]))begin
				$display(" > ERR: candidate full-width vector=%0d got=%026h exp=%026h",
					index, candidate_bank_observed, vec_candidate[index]);
				cnt_error = cnt_error + 1;
			end
			@(posedge reg_clk);
			#1;
			if((road_mac_probe_Inst_dut.flag_stage_valid[4] !== 1'b1) ||
			   (candidate_hold_observed !== vec_candidate[index]))begin
				$display(" > ERR: candidate hold vector=%0d", index);
				cnt_error = cnt_error + 1;
			end
			@(posedge reg_clk);
			#1;
			if((road_mac_probe_Inst_dut.flag_stage_valid[5] !== 1'b1) ||
			   (candidate_final_observed !== vec_candidate[index]))begin
				$display(" > ERR: candidate final vector=%0d", index);
				cnt_error = cnt_error + 1;
			end
			@(posedge reg_clk);
			#1;
			if(road_mac_probe_Inst_dut.flag_commit_event !== (vec_fault[index] ? 1'b0 : 1'b1))begin
				$display(" > ERR: commit decision vector=%0d", index);
				cnt_error = cnt_error + 1;
			end
			if(road_mac_probe_Inst_dut.flag_publish_event !== vec_emit[index][0])begin
				$display(" > ERR: publish decision vector=%0d", index);
				cnt_error = cnt_error + 1;
			end
			@(posedge reg_clk);
			#1;
			if(accumulator_observed !== vec_accumulator[index])begin
				$display(" > ERR: accumulator writeback vector=%0d got=%025h exp=%025h",
					index, accumulator_observed, vec_accumulator[index]);
				cnt_error = cnt_error + 1;
			end
			if(vec_emit[index] != 0)begin
				if((flag_result_valid !== 1'b1) || ((cnt_cycle - cycle_accept) != 9))begin
					$display(" > ERR: terminal latency vector=%0d got=%0d exp=9",
						index, cnt_cycle - cycle_accept);
					cnt_error = cnt_error + 1;
				end
				if((flag_fault !== vec_fault[index][0]) || (result_data !== vec_data[index]))begin
					$display(" > ERR: terminal payload vector=%0d got_fault=%0b exp_fault=%0b got=%024h exp=%024h",
						index, flag_fault, vec_fault[index][0], result_data, vec_data[index]);
					cnt_error = cnt_error + 1;
				end
				if((vec_fault[index] != 0) && (result_data !== 96'd0))begin
					$display(" > ERR: atomic fault payload not all zero vector=%0d", index);
					cnt_error = cnt_error + 1;
				end
				$fwrite(file_trace, "%0d,result_valid,%0d,%0d,%0d,%0d,%024h\n",
					cnt_cycle, vec_case[index], vec_beat[index], vec_fault[index],
					cnt_cycle-cycle_accept, result_data);
				reg_stalled_data = result_data;
				reg_stalled_fault = flag_fault;
				for(hold_index = 0; hold_index < vec_stall[index]; hold_index = hold_index + 1)begin
					@(posedge reg_clk);
					#1;
					if((flag_result_valid !== 1'b1) || (result_data !== reg_stalled_data) ||
					   (flag_fault !== reg_stalled_fault))begin
						$display(" > ERR: stalled output changed vector=%0d hold=%0d", index, hold_index);
						cnt_error = cnt_error + 1;
					end
				end
				@(negedge reg_clk);
				reg_result_ready = 1'b1;
				@(posedge reg_clk);
				#1;
				$fwrite(file_trace, "%0d,result_accept,%0d,%0d,%0d,%0d,%024h\n",
					cnt_cycle, vec_case[index], vec_beat[index], vec_fault[index],
					cnt_cycle-cycle_accept, result_data);
				@(negedge reg_clk);
				reg_result_ready = 1'b0;
			end else if(flag_result_valid !== 1'b0)begin
				$display(" > ERR: non-last published vector=%0d", index);
				cnt_error = cnt_error + 1;
			end
		end
	endtask

	//在指定真实流水阶段施加异步复位并确认没有幽灵终态
	task reset_cancel_stage;
		input integer stage_offset;
		input integer reset_id;
		input integer terminal;
		integer wait_index;
		begin
			while(flag_input_ready !== 1'b1)begin
				@(posedge reg_clk);
				#1;
			end
			@(negedge reg_clk);
			reg_first = 1'b1;
			reg_last = terminal[0];
			reg_lane_mask = 8'hff;
			reg_activation_data = {8{8'h02}};
			reg_weight_data = {24{8'h03}};
			reg_bias_data = 96'd0;
			reg_hold_first = 1'b1;
			reg_hold_last = terminal[0];
			reg_hold_mask = 8'hff;
			reg_hold_activation = {8{8'h02}};
			reg_hold_weight = {24{8'h03}};
			reg_hold_bias = 96'd0;
			reg_input_valid = 1'b1;
			@(posedge reg_clk);
			#1;
			$fwrite(file_trace, "%0d,reset_probe_accept,%0d,%0d,0,0,0\n",
				cnt_cycle, reset_id, stage_offset);
			@(negedge reg_clk);
			reg_input_valid = 1'b0;
			for(wait_index = 0; wait_index < stage_offset; wait_index = wait_index + 1)begin
				@(posedge reg_clk);
				#1;
			end
			if((stage_offset == 9) && (terminal == 0) && (accumulator_observed == 99'd0))begin
				$display(" > ERR: writeback reset probe never reached accumulator");
				cnt_error = cnt_error + 1;
			end
			if((stage_offset == 9) && (terminal != 0) && (flag_result_valid !== 1'b1))begin
				$display(" > ERR: output-hold reset probe never reached result");
				cnt_error = cnt_error + 1;
			end
			@(negedge reg_clk);
			reg_rstn = 1'b0;
			#1;
			cnt_reset = cnt_reset + 1;
			$fwrite(file_trace, "%0d,reset_assert,%0d,%0d,0,0,0\n",
				cnt_cycle, reset_id, stage_offset);
			if((flag_input_ready !== 1'b1) || (flag_result_valid !== 1'b0) ||
			   (result_data !== 96'd0) || (flag_fault !== 1'b0) ||
			   (road_mac_probe_Inst_dut.flag_stage_valid !== 6'd0) ||
			   (road_mac_probe_Inst_dut.reg_last_pipe !== 6'd0) ||
			   (road_mac_probe_Inst_dut.reg_base_product !== 99'd0) ||
			   (road_mac_probe_Inst_dut.reg_base_pair !== 99'd0) ||
			   (road_mac_probe_Inst_dut.reg_base_quad !== 99'd0) ||
			   (road_mac_probe_Inst_dut.reg_base_dot !== 99'd0) ||
			   (road_mac_probe_Inst_dut.reg_publish_data !== 99'd0) ||
			   (candidate_bank_observed !== 102'd0) ||
			   (candidate_hold_observed !== 102'd0) ||
			   (candidate_final_observed !== 102'd0) ||
			   (accumulator_observed !== 99'd0))begin
				$display(" > ERR: reset did not clear stage reset_id=%0d offset=%0d", reset_id, stage_offset);
				cnt_error = cnt_error + 1;
			end
			@(posedge reg_clk);
			@(negedge reg_clk);
			reg_rstn = 1'b1;
			#1;
			if(flag_input_ready !== 1'b1)begin
				$display(" > ERR: reset did not reopen input reset_id=%0d", reset_id);
				cnt_error = cnt_error + 1;
			end
			for(wait_index = 0; wait_index < 12; wait_index = wait_index + 1)begin
				@(posedge reg_clk);
				#1;
				if(flag_result_valid !== 1'b0)begin
					$display(" > ERR: ghost result after reset reset_id=%0d", reset_id);
					cnt_error = cnt_error + 1;
				end
			end
		end
	endtask

	//下游提前就绪时，跨INT32恢复终态仍应固定九周期出现并只消费一次。
	task ready_high_terminal;
		integer ready_wait;
		integer ready_first_cycle;
		integer ready_accept_cycle;
		integer ready_handshake;
		reg [95:0]ready_handshake_data;
		reg ready_handshake_fault;
		begin
			while(flag_input_ready !== 1'b1)begin
				@(posedge reg_clk);
				#1;
			end
			@(negedge reg_clk);
			reg_result_ready = 1'b1;
			drive_vector(0);
			@(posedge reg_clk);
			#1;
			ready_first_cycle = cnt_cycle;
			$fwrite(file_trace, "%0d,ready_high_recovery_first,1,0,0,0,0\n", cnt_cycle);
			@(negedge reg_clk);
			drive_vector(1);
			ready_wait = 0;
			while(flag_input_ready !== 1'b1)begin
				@(posedge reg_clk);
				#1;
				ready_wait = ready_wait + 1;
				if(ready_wait > 16)begin
					$display(" > ERR: pre-ready recovery second beat timeout");
					cnt_error = cnt_error + 1;
					$finish;
				end
			end
			@(posedge reg_clk);
			#1;
			ready_accept_cycle = cnt_cycle;
			if((ready_accept_cycle-ready_first_cycle) != 11)begin
				$display(" > ERR: pre-ready recovery nonlast interval got=%0d exp=11",
					ready_accept_cycle-ready_first_cycle);
				cnt_error = cnt_error + 1;
			end
			$fwrite(file_trace, "%0d,ready_high_recovery_last,1,1,0,0,0\n", cnt_cycle);
			@(negedge reg_clk);
			reg_input_valid = 1'b0;
			for(ready_wait = 0; ready_wait < 9; ready_wait = ready_wait + 1)begin
				@(posedge reg_clk);
				#1;
			end
			if((flag_result_valid !== 1'b1) || (flag_fault !== 1'b0) ||
			   (result_data !== vec_data[1]) || ((cnt_cycle-ready_accept_cycle) != 9))begin
				$display(" > ERR: pre-ready terminal mismatch latency=%0d valid=%0b fault=%0b data=%024h",
					cnt_cycle-ready_accept_cycle, flag_result_valid, flag_fault, result_data);
				cnt_error = cnt_error + 1;
			end
			$fwrite(file_trace, "%0d,ready_high_result,11,0,0,%0d,%024h\n",
				cnt_cycle, cnt_cycle-ready_accept_cycle, result_data);
			@(posedge reg_clk);
			ready_handshake = flag_result_valid & reg_result_ready;
			ready_handshake_data = result_data;
			ready_handshake_fault = flag_fault;
			#1;
			if((ready_handshake != 1) || (ready_handshake_data !== vec_data[1]) ||
			   (ready_handshake_fault !== 1'b0) || (flag_result_valid !== 1'b0))begin
				$display(" > ERR: pre-ready terminal consume mismatch accepted=%0d data=%024h valid_after=%0b",
					ready_handshake, ready_handshake_data, flag_result_valid);
				cnt_error = cnt_error + 1;
			end
			@(negedge reg_clk);
			reg_result_ready = 1'b0;
			for(ready_wait = 0; ready_wait < 4; ready_wait = ready_wait + 1)begin
				@(posedge reg_clk);
				#1;
				if(flag_result_valid !== 1'b0)begin
					$display(" > ERR: pre-ready recovery repeated or ghost terminal cycle=%0d", cnt_cycle);
					cnt_error = cnt_error + 1;
				end
			end
			ready_wait = 0;
			while(flag_input_ready !== 1'b1)begin
				@(posedge reg_clk);
				#1;
				ready_wait = ready_wait + 1;
				if(ready_wait > 8)begin
					$display(" > ERR: pre-ready terminal failed to release input");
					cnt_error = cnt_error + 1;
					$finish;
				end
			end
			cnt_ready_high = cnt_ready_high + 1;
		end
	endtask

	//冻结旧核必须在恢复序列第一拍提前故障，保留为反证而非候选通过条件。
	task run_legacy_negative;
		integer legacy_index;
		integer legacy_case;
		begin
			for(legacy_case = 0; legacy_case < 2; legacy_case = legacy_case + 1)begin
				legacy_index = legacy_case == 0 ? 0 : 2;
				cycle_previous_accept = -1;
				@(negedge reg_clk);
				drive_vector(legacy_index);
				accept_current(legacy_index);
				cnt_wait = 0;
				while(flag_result_valid !== 1'b1)begin
					@(posedge reg_clk);
					#1;
					cnt_wait = cnt_wait + 1;
					if(cnt_wait > 16)begin
						$display(" > ERR: legacy did not reject recovery case=%0d", legacy_case);
						cnt_error = cnt_error + 1;
						$finish;
					end
				end
				if((flag_fault !== 1'b1) || (result_data !== 96'd0) ||
				   ((cnt_cycle - cycle_accept) != 9))begin
					$display(" > ERR: legacy rejection mismatch case=%0d", legacy_case);
					cnt_error = cnt_error + 1;
				end
				$fwrite(file_trace, "%0d,legacy_early_fault,%0d,0,1,%0d,%024h\n",
					cnt_cycle, legacy_case, cnt_cycle-cycle_accept, result_data);
				@(negedge reg_clk);
				reg_result_ready = 1'b1;
				@(posedge reg_clk);
				#1;
				@(negedge reg_clk);
				reg_result_ready = 1'b0;
			end
			if(cnt_error == 0)begin
				$display("VERILOG-GEN-NEGATIVE PASS legacy_early_faults=2 errors=0");
			end else begin
				$display("VERILOG-GEN-NEGATIVE FAIL legacy_early_faults=2 errors=%0d", cnt_error);
			end
	end
	endtask

	//读取向量、执行候选检查或旧核反证模式
	initial begin
		if($value$plusargs("VECTORS=%s", reg_vector_path) == 1'b0)begin
			reg_vector_path = "signed33_vectors.txt";
		end
		if($value$plusargs("TRACE=%s", reg_trace_path) == 1'b0)begin
			reg_trace_path = "timing_trace.csv";
		end
		flag_legacy_mode = $test$plusargs("LEGACY_NEGATIVE");
		file_vectors = $fopen(reg_vector_path, "r");
		file_trace = $fopen(reg_trace_path, "w");
		if((file_vectors == 0) || (file_trace == 0))begin
			$display(" > ERR: cannot open vectors or trace");
			$finish;
		end
		$fwrite(file_trace, "cycle,event,case,beat,fault,latency_or_stall,data\n");
		while((!$feof(file_vectors)) && (cnt_vector < MAX_VECTORS))begin
			status_scan = $fscanf(file_vectors,
				"%d %d %d %d %h %h %h %h %d %d %h %h %h %h %h %h %h %h %d\n",
				vec_case[cnt_vector], vec_beat[cnt_vector], vec_first[cnt_vector], vec_last[cnt_vector],
				vec_mask[cnt_vector], vec_activation[cnt_vector], vec_weight[cnt_vector], vec_bias[cnt_vector],
				vec_emit[cnt_vector], vec_fault[cnt_vector], vec_data[cnt_vector], vec_products[cnt_vector],
				vec_pairs[cnt_vector], vec_quads[cnt_vector], vec_dots[cnt_vector], vec_base[cnt_vector],
				vec_candidate[cnt_vector], vec_accumulator[cnt_vector], vec_stall[cnt_vector]);
			if(status_scan == 19)begin
				cnt_vector = cnt_vector + 1;
			end else if(status_scan != -1)begin
				$display(" > ERR: malformed vector fields=%0d index=%0d", status_scan, cnt_vector);
				$finish;
			end
		end
		$fclose(file_vectors);
		if(cnt_vector != 84)begin
			$display(" > ERR: vector count got=%0d exp=84", cnt_vector);
			$finish;
		end

		repeat(4)begin
			@(posedge reg_clk);
		end
		@(negedge reg_clk);
		reg_rstn = 1'b1;
		#1;

		if(flag_legacy_mode != 0)begin
			run_legacy_negative;
		end else begin
			@(negedge reg_clk);
			drive_vector(0);
			for(cnt_index = 0; cnt_index < cnt_vector; cnt_index = cnt_index + 1)begin
				accept_current(cnt_index);
				check_candidate_vector(cnt_index);
			end

			//归约、全扩展候选链、判定、写回和输出保持十个复位取消点。
			reset_cancel_stage(1, 1, 1);
			reset_cancel_stage(2, 2, 1);
			reset_cancel_stage(3, 3, 1);
			reset_cancel_stage(4, 4, 1);
			reset_cancel_stage(5, 5, 1);
			reset_cancel_stage(6, 6, 1);
			reset_cancel_stage(7, 7, 1);
			reset_cancel_stage(8, 8, 1);
			reset_cancel_stage(9, 9, 0);
			reset_cancel_stage(9, 10, 1);
			ready_high_terminal;

			if((cnt_error == 0) && (cnt_busy_hold > 3) && (cnt_reset == 10) && (cnt_ready_high == 1))begin
				$display("VERILOG-GEN-RESULT PASS vectors=%0d errors=0 busy_hold=%0d resets=%0d ready_high=%0d latency=9 ii_nonlast=11 ii_stall3=16",
					cnt_vector, cnt_busy_hold, cnt_reset, cnt_ready_high);
			end else begin
				$display("VERILOG-GEN-RESULT FAIL vectors=%0d errors=%0d busy_hold=%0d resets=%0d ready_high=%0d",
					cnt_vector, cnt_error, cnt_busy_hold, cnt_reset, cnt_ready_high);
			end
		end
		$fclose(file_trace);
		$finish;
	end

endmodule
