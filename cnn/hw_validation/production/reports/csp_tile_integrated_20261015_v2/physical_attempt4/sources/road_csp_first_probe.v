`timescale 1ns / 1ps

////////////////////////////////////English///////////////////////////////////////
// Company:         RoadYOLO
// Engineer:        Codex
//
// Create Date:     2026-10-15
// Design Name:     Single-context CSP arithmetic probe
// Module Name:     road_csp_first_probe
// Description:     description/road_csp_first_probe_Design.pdf
// Simulations:     testbench/vivado/2021.1/road_csp_first_probe
//
// Referrences:
// File Format      File Name
// 1.Book           road_csp_first_probe_spec.md
//
// Dependencies:
// Module Name      Version
// road_mac_probe, road_dynamic_postprocess
//
// Version:         V1.0
// Revision Date:   2026-10-15
// History:
// Time             Version     Revised by        Contents
// 2026-10-15       V1.0        Erie              Create file.
///////////////////////////////////Chinese////////////////////////////////////////
// 版权归属:        RoadYOLO
// 开发人员:        Codex
//
// 创建日期:        2026-10-15
// 设计名称:        Single-context CSP arithmetic probe
// 模块名称:        road_csp_first_probe
// 模块说明:        Description/road_csp_first_probe_Design.pdf
// 仿真工程:        TestBench/Vivado/2021.1/road_csp_first_probe
//
// 参考资料:
// 文件格式         文件名称
// 1.Book           road_csp_first_probe_spec.md
//
// 依赖文件:
// 模块名称         版本
// road_mac_probe, road_dynamic_postprocess
//
// 当前版本:        V1.0
// 修订日期:        2026-10-15
// 修订历史:
// 时间             版本        修订人            修订内容
// 2026-10-15    V1.0        Codex             创建文件

module road_csp_first_probe
(
	//-----------------全局信号-----------------//
	input i_clk,                                // 100MHz同域计算时钟
	input i_rstn,                               // 与全部算术核共同异步低有效复位

	//----------------TABLE接口-----------------//

	//TABLE接口
	input i_table_valid,                        // 空闲时装载共享SiLU表
	input [9:0]i_table_addr,                    // 顺序表项地址
	input signed [15:0]i_table_data,            // 原模型Q7.8表项

	//-----------------用户接口-----------------//
	input i_input_valid,                        // 一个八输入组有效并保持到ready
	input i_first,                              // 当前任务首组并锁存全部元数据
	input i_last,                               // 当前任务最后一个乘加组
	input [7:0]i_lane_mask,                     // 八输入槽有效掩码
	input [63:0]i_activation_data,              // 低字节优先八个INT8激活
	input [191:0]i_weight_data,                 // 三输出路各八个INT8权重
	input [95:0]i_bias_data,                    // 三个INT32偏置，仅first计入
	input [2:0]i_output_mask,                   // 首组锁存的有效输出路
	input [47:0]i_tags,                         // 首组锁存的三个不透明16位输出标识
	input [95:0]i_addresses,                    // 首组锁存的三个逻辑字节地址
	input [95:0]i_pre_multipliers,              // 三路原模型前重定标乘数
	input [17:0]i_pre_shifts,                   // 三路原模型六位移位
	input [31:0]i_post_multiplier,              // 本层共享后重定标乘数
	input [5:0]i_post_shift,                    // 本层共享后重定标移位
	input i_residual,                           // 首组锁存，高表示融合旁路
	input [23:0]i_bypass_data,                  // 三输出路对应的INT8旁路值
	input i_input_fault,                        // 首组注入任务错误供独立故障验证
	input i_output_ready,                       // 实际写端接受完整载荷
	output o_table_ready,                       // 表项真实接收条件
	output o_table_loaded,                      // 全表重新装满后许可计算
	output o_input_ready,                       // 唯一事务未关闭时允许接受组

	//----------------OUTPUT接口----------------//

	//OUTPUT接口
	output o_output_valid,                      // 数据地址标识整体保持至接受
	output signed [7:0]o_output_data,           // 已饱和INT8结果
	output [15:0]o_output_tag,                  // 与结果同事务的输出标识
	output [31:0]o_output_address,              // 与结果同事务的字节地址
	output signed [8:0]o_output_sum,            // 饱和前signed9和供观察
	output o_fault                              // 任一核或元数据错误粘滞，必须共同复位
);

	//--------------模块实例化信号--------------//
	//road_mac_probe--用户接口
	wire [95:0]mac_data;                        // 三路最终INT32累加结果
	wire mac_fault;                             // 原核末组原子故障

	//road_dynamic_postprocess--用户接口
	wire signed [15:0]pp_data;                  // 量化核符号扩展的INT8结果
	wire [15:0]pp_tag;                          // 量化结果对应的外部标识
	wire pp_fault;                              // 原量化核粘滞故障

	//----------------寄存器信号----------------//
	reg [2:0]reg_remaining = 0;                 // 尚未被写端接受的输出路
	reg [2:0]reg_output_mask = 0;               // 本任务固定输出路
	reg [47:0]reg_tags = 0;                     // 本任务固定输出标识
	reg [95:0]reg_addresses = 0;                // 本任务固定输出字节地址
	reg [95:0]reg_pre_multipliers = 0;          // 本任务固定三路前乘数
	reg [17:0]reg_pre_shifts = 0;               // 本任务固定三路前移位
	reg [31:0]reg_post_multiplier = 0;          // 本任务固定后乘数
	reg [5:0]reg_post_shift = 0;                // 本任务固定后移位
	reg [23:0]reg_bypass = 0;                   // 本任务三路固定旁路

	//-----------------标志信号-----------------//
	reg flag_owned = 0;                         // 首组接受至最后有效写端接受保持占有
	reg flag_closed = 0;                        // 末组已接受，禁止新乘加组混入
	reg flag_fault = 0;                         // 本探针发现的粘滞故障
	reg flag_residual = 0;                      // 本任务是否融合旁路
	reg flag_input_fault = 0;                   // 本任务传递至量化核的错误
	wire flag_mac_ready;                        // MAC允许接受下一乘加组
	wire flag_mac_valid;                        // MAC完整三路累加结果有效
	wire flag_pp_ready;                         // 量化核允许保管完整三路结果
	wire flag_pp_valid;                         // 量化核的串行输出有效
	wire flag_pp_rawmode;                       // 本探针不允许原始预测INT16模式
	wire flag_pp_table_ready;                   // 原量化核表端口接收条件
	wire flag_pp_output_ready;                  // 本探针写回槽可接纳量化结果
	wire flag_group_enable;                     // 空闲只接first，拥有时只接非first组
	wire flag_group_accept;                     // 本域实际接收乘加组
	wire flag_acc_accept;                       // MAC结果被量化核真实接受
	wire flag_pp_accept;                        // 量化结果被写回槽真实接受
	wire flag_write_accept;                     // 外部写端真实接受一个结果
	reg [2:0]reg_seen = 0;                     // 已进入非停顿流水的路号，独立于外部提交
	reg flag_match_valid = 0;                  // M级保存已接受的量化结果
	reg [2:0]reg_match_lane = 0;                // M级一次比较得到的onehot路号
	reg signed [7:0]reg_match_data = 0;         // M级符号有效的INT8量化值
	reg flag_select_valid = 0;                 // S级载荷已完成旁路选择
	reg [2:0]reg_select_lane = 0;               // S级保留写回槽身份
	reg signed [7:0]reg_select_data = 0;        // S级被加数
	reg signed [7:0]reg_select_bypass = 0;      // S级按残差模式选择的旁路
	reg [15:0]reg_select_tag = 0;               // S级固定外部标识
	reg [31:0]reg_select_address = 0;           // S级固定字节地址
	reg flag_add_valid = 0;                    // A级signed9求和已注册
	reg [2:0]reg_add_lane = 0;                  // A级保留路号
	reg signed [8:0]reg_add_sum = 0;            // A级显式扩展后的精确和
	reg [15:0]reg_add_tag = 0;                  // A级标识随和传递
	reg [31:0]reg_add_address = 0;              // A级地址随和传递
	reg flag_compare_valid = 0;                // C级饱和判断已注册
	reg [2:0]reg_compare_lane = 0;              // C级目标预留槽
	reg signed [8:0]reg_compare_sum = 0;        // C级保留未饱和值
	reg [15:0]reg_compare_tag = 0;              // C级结果标识
	reg [31:0]reg_compare_address = 0;          // C级结果地址
	reg flag_compare_high = 0;                 // C级严格大于127
	reg flag_compare_low = 0;                  // C级严格小于负128
	reg [2:0]reg_bank_valid = 0;                // W级每路一个固定预留槽
	reg [64:0]reg_bank_alpha = 0;               // 甲槽保存sum/address/tag/data整体
	reg [64:0]reg_bank_beta = 0;                // 乙槽保存同一事务完整载荷
	reg [64:0]reg_bank_gamma = 0;               // 丙槽保存尚未提交的完整载荷

	//-----------------其他信号-----------------//
	wire [2:0]wire_pp_match;                    // 当前量化标识对应的有效输出路
	wire [2:0]wire_write_match;                 // 当前写回标识对应的未提交路
	wire [2:0]wire_after_write;                 // 本次提交之后剩余输出路
	wire flag_bad_pp;                           // 同步检错不能撤回本边沿合法旧写
	wire [2:0]wire_selected_lane;              // 最低尚未提交路确定外部发布次序
	wire [64:0]wire_selected_payload;          // 不依赖新PP输入的已注册写槽载荷
	wire signed [7:0]wire_saturated;            // W级只使用已注册的饱和标志

	//-----------------输出信号-----------------//
	wire flag_valid_o;                          // 最低剩余路的槽已填入才发布

	//用户接口
	wire table_loaded_o;                        // 冻结核心确认完整SiLU表已激活

	//OUTPUT接口
	wire signed [7:0]output_data_o;             // 从最低有效固定槽发布饱和值
	wire [15:0]output_tag_o;                    // 从同一个槽发布标识
	wire [31:0]output_address_o;                // 从同一个槽发布地址
	wire signed [8:0]output_sum_o;              // 从同一个槽发布signed9和

	//---------------其他信号连线---------------//
	//其他信号连线
	assign flag_group_enable = flag_owned ? (!flag_closed && !i_first) : (i_first && !i_table_valid); // 空闲装表优先，已有归约不被待装表请求阻断
	assign flag_group_accept = i_input_valid && o_input_ready; // 仅真实握手推进任务
	assign flag_pp_output_ready = i_rstn && o_table_loaded && flag_owned && !o_fault && (reg_seen != reg_output_mask); // 固定预留容量使PP准入独立于外部写ready
	assign flag_pp_accept = flag_pp_valid && flag_pp_output_ready; // 量化输出进入写回槽
	assign flag_write_accept = o_output_valid && i_output_ready; // 最终所有权释放事件
	assign flag_acc_accept = flag_mac_valid && flag_owned && flag_closed && flag_pp_ready && !o_fault; // 结果只移交一次
	assign wire_pp_match[0] = reg_output_mask[0] && (pp_tag == reg_tags[15:0]); // 甲路标识命中
	assign wire_pp_match[1] = reg_output_mask[1] && (pp_tag == reg_tags[31:16]); // 乙路标识命中
	assign wire_pp_match[2] = reg_output_mask[2] && (pp_tag == reg_tags[47:32]); // 丙路标识命中
	assign wire_write_match[0] = reg_remaining[0] && (output_tag_o == reg_tags[15:0]); // 甲路尚未提交
	assign wire_write_match[1] = reg_remaining[1] && (output_tag_o == reg_tags[31:16]); // 乙路尚未提交
	assign wire_write_match[2] = reg_remaining[2] && (output_tag_o == reg_tags[47:32]); // 丙路尚未提交
	assign wire_after_write = reg_remaining & ~wire_write_match; // 只清除实际接受的一路
	assign flag_bad_pp = (flag_pp_valid && flag_owned && (reg_seen == reg_output_mask)) ||
		(flag_pp_accept && ((wire_pp_match != 3'b001 && wire_pp_match != 3'b010 && wire_pp_match != 3'b100) ||
		((wire_pp_match & reg_seen) != 3'd0) || flag_pp_rawmode || (pp_data[15:8] != {8{pp_data[7]}}))); // 额外valid、重复路、错误类型或非INT8符号扩展粘滞取消
	assign wire_selected_lane = reg_remaining[0] ? 3'b001 : reg_remaining[1] ? 3'b010 : 3'b100; // 到达乱序时仍等待最低未提交路
	assign wire_selected_payload = reg_remaining[0] ? reg_bank_alpha : reg_remaining[1] ? reg_bank_beta : reg_bank_gamma; // 只复用三个注册槽
	assign flag_valid_o = (reg_bank_valid & wire_selected_lane) != 3'd0; // 有效位控制整条写载荷
	assign output_data_o = wire_selected_payload[7:0]; // 保持结果低字节
	assign output_tag_o = wire_selected_payload[23:8]; // 输出标识与槽绑定
	assign output_address_o = wire_selected_payload[55:24]; // 输出地址与槽绑定
	assign output_sum_o = wire_selected_payload[64:56]; // 观察和与最终结果绑定
	assign wire_saturated = flag_compare_high ? 8'sh7f : flag_compare_low ? 8'sh80 : reg_compare_sum[7:0]; // W级饱和选择不重新计算加法或比较

	//---------------输出信号连线---------------//
	//用户接口
	assign o_table_ready = flag_pp_table_ready && !flag_owned && !o_fault; // 对外握手必须与内核真实装表一致
	assign o_table_loaded = table_loaded_o;     // 完整表状态原样转交调用方
	assign o_input_ready = i_rstn && o_table_loaded && !o_fault && flag_group_enable && flag_mac_ready; // 共同准入许可

	//OUTPUT接口
	assign o_output_valid = flag_valid_o && i_rstn && !o_fault; // 故障不发布旧载荷
	assign o_output_data = output_data_o;       // INT8写回载荷保持
	assign o_output_tag = output_tag_o;         // 输出标识保持
	assign o_output_address = output_address_o; // 输出地址保持
	assign o_output_sum = output_sum_o;         // 观察值与输出保持同拍
	assign o_fault = flag_fault || mac_fault || pp_fault; // 故障立即关闭对外提交

	//-------------输出信号处理区域-------------//
	// 五级流水只在任务首组、故障或共同复位时清空；正常结果均有固定容量。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_seen <= 3'd0; // 复位后全部路重新接收
			flag_match_valid <= 1'b0; // 取消M级
			flag_select_valid <= 1'b0; // 取消S级
			flag_add_valid <= 1'b0; // 取消A级
			flag_compare_valid <= 1'b0; // 取消C级
			reg_bank_valid <= 3'd0; // 取消三路待写
		end else if(o_fault || flag_bad_pp)begin
			flag_match_valid <= 1'b0; // 故障后不再推进已接收量化值
			flag_select_valid <= 1'b0; // 取消已选旁路
			flag_add_valid <= 1'b0; // 取消求和结果
			flag_compare_valid <= 1'b0; // 取消待饱和结果
			reg_bank_valid <= 3'd0; // 合法旧写已在本边沿接受，其余结果撤销
		end else if(flag_group_accept && i_first)begin
			reg_seen <= 3'd0; // 新所有权开始新的接收集合
			flag_match_valid <= 1'b0; // 首组前上个任务必须已经退休
			flag_select_valid <= 1'b0; // 不保留跨任务旁路
			flag_add_valid <= 1'b0; // 不保留跨任务和
			flag_compare_valid <= 1'b0; // 不保留跨任务饱和标志
			reg_bank_valid <= 3'd0; // 三槽重新预留
		end else begin
			flag_match_valid <= flag_pp_accept; // M级每拍可接收一项
			flag_select_valid <= flag_match_valid; // S级无外部背压
			flag_add_valid <= flag_select_valid; // A级跟随有效载荷
			flag_compare_valid <= flag_add_valid; // C级跟随有效和
			if(flag_pp_accept)reg_seen <= reg_seen | wire_pp_match; // 合法路只登记一次
			reg_bank_valid <= (reg_bank_valid & ~wire_write_match) | (flag_compare_valid ? reg_compare_lane : 3'd0); // 写槽出入独立路可同拍发生
			if(!flag_write_accept)reg_bank_valid <= reg_bank_valid | (flag_compare_valid ? reg_compare_lane : 3'd0); // 未握手时所有已有效槽保持
		end
	end

	// M级仅注册比较结果，缩短tag到加法的组合路径。
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			reg_match_lane <= 3'd0; // 无有效路身份
			reg_match_data <= 8'sd0; // 定义失效载荷
		end else if(flag_pp_accept)begin
			reg_match_lane <= wire_pp_match; // 一次比较后onehot沿流水传递
			reg_match_data <= pp_data[7:0]; // 高位合法性由同步检错保证
		end
	end

	// S级从首组冻结的元数据选择旁路和目标地址。
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			reg_select_bypass <= 8'sd0; // 清旁路
			reg_select_tag <= 16'd0; // 清标识
			reg_select_address <= 32'd0; // 清地址
		end else if(flag_match_valid)begin
			case(reg_match_lane)
				3'b001:begin
					reg_select_bypass <= flag_residual ? reg_bypass[7:0] : 8'sd0; // 甲路残差
					reg_select_tag <= reg_tags[15:0]; // 甲路标识
					reg_select_address <= reg_addresses[31:0]; // 甲路写地址
				end
				3'b010:begin
					reg_select_bypass <= flag_residual ? reg_bypass[15:8] : 8'sd0; // 乙路残差
					reg_select_tag <= reg_tags[31:16]; // 乙路标识
					reg_select_address <= reg_addresses[63:32]; // 乙路写地址
				end
				default:begin
					reg_select_bypass <= flag_residual ? reg_bypass[23:16] : 8'sd0; // 合法丙路残差
					reg_select_tag <= reg_tags[47:32]; // 丙路标识
					reg_select_address <= reg_addresses[95:64]; // 丙路写地址
				end
			endcase
		end
	end

	// S级路号和量化值与选择后的元数据同拍注册。
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			reg_select_lane <= 3'd0; // 清选择路号
			reg_select_data <= 8'sd0; // 清选择被加数
		end else if(flag_match_valid)begin
			reg_select_lane <= reg_match_lane; // 下级沿用M级路号
			reg_select_data <= reg_match_data; // 量化值与元数据同拍前进
		end
	end

	// A级只做两个signed8的显式扩展加法。
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			reg_add_lane <= 3'd0; // 清求和身份
			reg_add_sum <= 9'sd0; // 清精确和
			reg_add_tag <= 16'd0; // 清求和标识
			reg_add_address <= 32'd0; // 清求和地址
		end else if(flag_select_valid)begin
			reg_add_lane <= reg_select_lane; // 保持槽归属
			reg_add_sum <= $signed({reg_select_data[7],reg_select_data}) + $signed({reg_select_bypass[7],reg_select_bypass}); // 覆盖负256至正254而不回绕
			reg_add_tag <= reg_select_tag; // 标识跟随精确和
			reg_add_address <= reg_select_address; // 地址跟随精确和
		end
	end

	// C级注册饱和标志，W级无需重新比较。
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			reg_compare_lane <= 3'd0; // 清饱和目标
			reg_compare_sum <= 9'sd0; // 清饱和观察值
			reg_compare_tag <= 16'd0; // 清饱和标识
			reg_compare_address <= 32'd0; // 清饱和地址
			flag_compare_high <= 1'b0; // 清上界标志
			flag_compare_low <= 1'b0; // 清下界标志
		end else if(flag_add_valid)begin
			reg_compare_lane <= reg_add_lane; // 固定路号不重新匹配tag
			reg_compare_sum <= reg_add_sum; // 保留精确中间值
			reg_compare_tag <= reg_add_tag; // 保留结果标识
			reg_compare_address <= reg_add_address; // 保留目标地址
			flag_compare_high <= reg_add_sum > 9'sd127; // 上端严格饱和比较
			flag_compare_low <= reg_add_sum < -9'sd128; // 下端严格饱和比较
		end
	end

	// W级按注册路号填入固定槽；有效位决定是否允许提交。
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			reg_bank_alpha <= 65'd0; // 定义甲槽复位载荷
			reg_bank_beta <= 65'd0; // 定义乙槽复位载荷
			reg_bank_gamma <= 65'd0; // 定义丙槽复位载荷
		end else if(flag_compare_valid && !o_fault && !flag_bad_pp)begin
			if(reg_compare_lane == 3'b001)begin
				reg_bank_alpha <= {reg_compare_sum,reg_compare_address,reg_compare_tag,wire_saturated}; // 甲槽只接本路结果
			end
			if(reg_compare_lane == 3'b010)begin
				reg_bank_beta <= {reg_compare_sum,reg_compare_address,reg_compare_tag,wire_saturated}; // 乙槽只接本路结果
			end
			if(reg_compare_lane == 3'b100)begin
				reg_bank_gamma <= {reg_compare_sum,reg_compare_address,reg_compare_tag,wire_saturated}; // 丙槽只接合法剩余路
			end
		end
	end

	//-------------主要任务处理区域-------------//
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_owned <= 1'b0;
		end else begin
			if(flag_group_accept == 1'b1 && i_first == 1'b1)begin
				flag_owned <= 1'b1;
			end
			if(flag_write_accept == 1'b1 && wire_after_write == 3'd0)begin
				flag_owned <= 1'b0;
			end
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_closed <= 1'b0;
		end else begin
			if(flag_group_accept == 1'b1 && i_last == 1'b1)begin
				flag_closed <= 1'b1;
			end
			if(flag_write_accept == 1'b1 && wire_after_write == 3'd0)begin
				flag_closed <= 1'b0;
			end
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_fault <= 1'b0;
		end else begin
			if(mac_fault == 1'b1 || pp_fault == 1'b1)begin
				flag_fault <= 1'b1;
			end
			if(flag_group_accept == 1'b1 && i_first == 1'b1)begin
				if(i_output_mask == 3'd0 || (i_output_mask[0] && i_output_mask[1] && i_tags[15:0] == i_tags[31:16]) || (i_output_mask[0] && i_output_mask[2] && i_tags[15:0] == i_tags[47:32]) || (i_output_mask[1] && i_output_mask[2] && i_tags[31:16] == i_tags[47:32]))begin
					flag_fault <= 1'b1;
				end
			end
			if(flag_pp_accept == 1'b1 && (flag_owned == 1'b0 || wire_pp_match == 3'd0 || flag_pp_rawmode == 1'b1))begin
				flag_fault <= 1'b1;
			end
			if(flag_bad_pp)flag_fault <= 1'b1; // 收齐后额外valid零接受并保持故障
			if(flag_write_accept == 1'b1 && wire_write_match == 3'd0)begin
				flag_fault <= 1'b1;
			end
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_remaining <= 3'd0;
		end else begin
			if(flag_group_accept == 1'b1 && i_first == 1'b1)begin
				reg_remaining <= i_output_mask;
			end
			if(flag_write_accept == 1'b1)begin
				reg_remaining <= wire_after_write;
			end
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_output_mask <= 3'd0;
		end else if(flag_group_accept == 1'b1 && i_first == 1'b1)begin
			reg_output_mask <= i_output_mask;
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_tags <= 48'd0;
		end else if(flag_group_accept == 1'b1 && i_first == 1'b1)begin
			reg_tags <= i_tags;
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_addresses <= 96'd0;
		end else if(flag_group_accept == 1'b1 && i_first == 1'b1)begin
			reg_addresses <= i_addresses;
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_pre_multipliers <= 96'd0;
		end else if(flag_group_accept == 1'b1 && i_first == 1'b1)begin
			reg_pre_multipliers <= i_pre_multipliers;
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_pre_shifts <= 18'd0;
		end else if(flag_group_accept == 1'b1 && i_first == 1'b1)begin
			reg_pre_shifts <= i_pre_shifts;
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_post_multiplier <= 32'd0;
		end else if(flag_group_accept == 1'b1 && i_first == 1'b1)begin
			reg_post_multiplier <= i_post_multiplier;
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_post_shift <= 6'd0;
		end else if(flag_group_accept == 1'b1 && i_first == 1'b1)begin
			reg_post_shift <= i_post_shift;
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_residual <= 1'b0;
		end else if(flag_group_accept == 1'b1 && i_first == 1'b1)begin
			flag_residual <= i_residual;
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_bypass <= 24'd0;
		end else if(flag_group_accept == 1'b1 && i_first == 1'b1)begin
			reg_bypass <= i_bypass_data;
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_input_fault <= 1'b0;
		end else if(flag_group_accept == 1'b1 && i_first == 1'b1)begin
			flag_input_fault <= i_input_fault;
		end
	end

	//--------------模块实例化区域--------------//
	road_mac_probe road_mac_probe_Inst_core(
		.i_clk(i_clk),                          // i_clk端口连接i_clk
		.i_rstn(i_rstn),                        // i_rstn端口连接i_rstn
		.i_input_valid(i_input_valid && o_input_ready), // i_input_valid端口连接i_input_valid && o_input_ready
		.i_first(i_first),                      // i_first端口连接i_first
		.i_last(i_last),                        // i_last端口连接i_last
		.i_lane_mask(i_lane_mask),              // i_lane_mask端口连接i_lane_mask
		.i_activation_data(i_activation_data),  // i_activation_data端口连接i_activation_data
		.i_weight_data(i_weight_data),          // i_weight_data端口连接i_weight_data
		.i_bias_data(i_bias_data),              // i_bias_data端口连接i_bias_data
		.i_result_ready(flag_pp_ready && flag_owned && flag_closed && !o_fault), // i_result_ready端口连接flag_pp_ready && flag_owned && flag_closed && !o_fault
		.o_input_ready(flag_mac_ready),         // o_input_ready端口连接flag_mac_ready
		.o_result_valid(flag_mac_valid),        // o_result_valid端口连接flag_mac_valid
		.o_result_data(mac_data),               // o_result_data端口连接mac_data
		.o_fault(mac_fault)                     // o_fault端口连接mac_fault
	);

	road_dynamic_postprocess road_dynamic_postprocess_Inst_core(
		.i_clk(i_clk),                          // i_clk端口连接i_clk
		.i_rstn(i_rstn),                        // i_rstn端口连接i_rstn
		.i_table_valid(i_table_valid && !flag_owned && !o_fault), // i_table_valid端口连接i_table_valid && !flag_owned && !o_fault
		.i_table_addr(i_table_addr),            // i_table_addr端口连接i_table_addr
		.i_table_data(i_table_data),            // i_table_data端口连接i_table_data
		.o_table_ready(flag_pp_table_ready),    // o_table_ready端口连接flag_pp_table_ready
		.o_table_loaded(table_loaded_o),        // o_table_loaded端口连接table_loaded_o
		.i_input_valid(flag_mac_valid && flag_owned && flag_closed && !o_fault), // i_input_valid端口连接flag_mac_valid && flag_owned && flag_closed && !o_fault
		.i_accumulators(mac_data),              // i_accumulators端口连接mac_data
		.i_pre_multipliers(reg_pre_multipliers), // i_pre_multipliers端口连接reg_pre_multipliers
		.i_pre_shifts(reg_pre_shifts),          // i_pre_shifts端口连接reg_pre_shifts
		.i_post_multiplier(reg_post_multiplier), // i_post_multiplier端口连接reg_post_multiplier
		.i_post_shift(reg_post_shift),          // i_post_shift端口连接reg_post_shift
		.i_activate(1'b1),                      // i_activate端口连接1'b1
		.i_lane_mask(reg_output_mask),          // i_lane_mask端口连接reg_output_mask
		.i_tags(reg_tags),                      // i_tags端口连接reg_tags
		.i_input_fault(flag_input_fault),       // i_input_fault端口连接flag_input_fault
		.o_input_ready(flag_pp_ready),          // o_input_ready端口连接flag_pp_ready
		.i_output_ready(flag_pp_output_ready),  // i_output_ready端口连接flag_pp_output_ready
		.o_output_valid(flag_pp_valid),         // o_output_valid端口连接flag_pp_valid
		.o_output_data(pp_data),                // o_output_data端口连接pp_data
		.o_output_tag(pp_tag),                  // o_output_tag端口连接pp_tag
		.o_output_int16(flag_pp_rawmode),       // o_output_int16端口连接flag_pp_rawmode
		.o_fault(pp_fault)                      // o_fault端口连接pp_fault
	);

endmodule
