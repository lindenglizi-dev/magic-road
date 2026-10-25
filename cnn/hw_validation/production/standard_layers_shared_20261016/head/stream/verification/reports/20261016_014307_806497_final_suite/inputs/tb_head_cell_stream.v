`timescale 1ns / 1ps
////////////////////////////////////English///////////////////////////////////////
// Company: RoadYOLO
// Engineer: Codex
// Create Date: 2026-10-16
// Design Name: Controlled INT16 prediction reader verification
// Module Name: tb_head_cell_stream
// Description: description/tb_head_cell_stream_Design.pdf
// Simulations: testbench/vivado/2021.1/tb_head_cell_stream
// Referrences: Frozen prediction planes and field addresses
// Dependencies: road_head_cell_stream
// Version: V1.0
// Revision Date: 2026-10-16
// History: 2026-10-16 V1.0 Codex Create file
///////////////////////////////////Chinese////////////////////////////////////////
// 版权归属: RoadYOLO
// 开发人员: Codex
// 创建日期: 2026-10-16
// 设计名称: 受控预测张量读取自检
// 模块名称: tb_head_cell_stream
// 模块说明: Description/tb_head_cell_stream_Design.pdf
// 仿真工程: TestBench/Vivado/2021.1/tb_head_cell_stream
// 参考资料: 冻结预测平面及字段地址
// 依赖文件: road_head_cell_stream
// 当前版本: V1.0
// 修订日期: 2026-10-16
// 修订历史: 2026-10-16 V1.0 Codex 创建文件
module tb_head_cell_stream
(
	output o_test_complete // 所有当前案例比较通过后置位
);

	//--------------寄存器信号--------------//
	// 所有刺激只在下降沿修改，避免与DUT采样竞争。
	reg i_clk = 0; // 100MHz同域时钟
	reg i_rstn = 0; // 读服务与DUT共同复位
	reg i_cancel = 0; // 主动取消刺激
	reg i_start_valid = 0; // 完整预测任务请求
	reg [31:0]i_start_frame_token = 32'h12345678; // 首次准入任务标识
	reg [31:0]i_start_model_id = 32'h87654321; // 首次准入模型标识
	reg i_predictions_committed = 0; // 六平面可读许可
	reg i_read_ready = 0; // 逻辑读请求随机接纳
	reg i_read_rsp_valid = 0; // 唯一未决响应有效
	reg [31:0]i_read_rsp_address = 0; // 完整行地址回显
	reg [127:0]i_read_rsp_data = 0; // 实际物理行镜像数据
	reg i_read_error = 0; // 独立源服务错误注入
	reg i_cell_ready = 0; // 实际cell接收背压
	reg [31:0]reg_random = 32'h6ac934e1; // 固定可复现随机序列
	reg flag_pending = 0; // 行请求接受后到响应消费的所有权
	reg [31:0]reg_pending_address = 0; // 未决源行地址
	reg [127:0]reg_pending_data = 0; // 未决源行数据
	reg [31:0]reg_expected_token = 0; // 首握手冻结的预期任务
	reg [31:0]reg_expected_model = 0; // 首握手冻结的预期参数包
	reg flag_request_hold = 0; // 上拍请求被反压
	reg [31:0]reg_held_request = 0; // 请求保持基准
	reg flag_cell_hold = 0; // 上拍cell未消费
	reg [189:0]reg_held_cell = 0; // 112data+14id+64identity保持基准
	reg flag_response_hold = 0; // 行响应被暂停消费
	reg [160:0]reg_held_response = 0; // 响应地址/数据/error整体保持
	reg flag_force_request_stall = 0; // 定向未接受请求
	reg flag_force_cell_stall = 0; // 定向完整cell保持
	reg flag_force_response = 0; // 取消同时交付未决响应
	reg flag_verified_job = 0; // 本次任务已发生准入
	reg flag_test_complete = 0; // 当前独立案例终结标志
	reg [159:0]mem_lines [0:11263]; // 行镜像仅属于行为服务
	reg [31:0]mem_fields [0:84671]; // 独立原graph字段地址
	reg [111:0]mem_cells [0:12095]; // 独立完整HWC7数据
	reg [8191:0]reg_root; // 运行快照向量根目录
	reg [8191:0]reg_trace; // 当前尝试事务日志路径
	reg [111:0]reg_expected_cell; // 当前输出期望原始16位数据
	integer reg_mode = 0; // 定向协议案例编号
	integer reg_case = 0; // 保留原始案例编号用于回执
	integer reg_negative = 0; // 实际比较器一位反例
	integer reg_delay = 0; // 未决源响应等待拍数
	integer reg_line_index; // 二分查找返回的真实行
	integer reg_trace_file; // 每次尝试独立事务日志
	integer cnt_cycle = 0; // 本次任务周期数
	integer cnt_cells = 0; // 实际消费cell数
	integer cnt_fields = 0; // 实际缓存命中并复制字段数
	integer cnt_requests = 0; // 真实源请求握手数
	integer cnt_responses = 0; // 真实源响应消费数
	integer cnt_request_stalls = 0; // 请求背压拍数
	integer cnt_cell_stalls = 0; // cell保持拍数
	integer cnt_response_stalls = 0; // 响应保持拍数
	integer cnt_last_source = 0; // 最后源响应实际消费拍
	integer cnt_last_cell = 0; // 最末cell实际消费拍
	integer cnt_done = 0; // 完成脉冲计数
	integer cnt_long_hold = 0; // 首末cell额外长背压
	integer cnt_scale_boundaries = 0; // 两次真实尺度跨越
	integer cnt_directed; // 定向等待循环计数

	//---------------其他信号---------------//
	// 被测应用的原始端口，不添加替代输出驱动。
	wire o_start_ready; // 原始启动接纳
	wire o_busy; // 未退休所有权
	wire o_done; // 末cell消费后完成
	wire o_fault; // 取消或错误粘滞
	wire o_read_valid; // 原始源行请求
	wire [31:0]o_read_address; // 实际源地址
	wire o_read_rsp_ready; // 实际响应退休
	wire o_cell_valid; // 原始完整预测cell
	wire [111:0]o_cell_data; // 不截断的七个INT16
	wire [13:0]o_cell_id; // 全局预测位置
	wire [31:0]o_cell_frame_token; // 输出任务上下文
	wire [31:0]o_cell_model_id; // 输出模型上下文
	assign o_test_complete = flag_test_complete; // 只有显式PASS路径才能置位

	//--------------主要任务区域--------------//
	// 固定源行表按地址排序，二分查找不伪造空洞返回。
	function integer find_line;
		input [31:0]address; // 已接受的完整行请求
		integer lower_bound; // 当前查找下界
		integer upper_bound; // 当前查找上界
		integer middle; // 当前候选行
		begin
			lower_bound = 0; upper_bound = 11263; find_line = -1;
			while(lower_bound <= upper_bound)begin
				middle = (lower_bound + upper_bound) / 2;
				if(mem_lines[middle][159:128] == address)begin
					find_line = middle; lower_bound = upper_bound + 1;
				end else if(mem_lines[middle][159:128] < address)begin
					lower_bound = middle + 1;
				end else begin
					upper_bound = middle - 1;
				end
			end
		end
	endfunction

	// 真正共同reset取消行为服务与DUT，不沿用旧缓存。
	task common_reset;
		begin
			@(negedge i_clk); i_rstn = 0; i_start_valid = 0; i_predictions_committed = 0; i_cancel = 0;
			flag_force_request_stall = 0; flag_force_cell_stall = 0; flag_force_response = 0;
			repeat(3)begin @(negedge i_clk); end
			i_rstn = 1;
			repeat(3)begin @(posedge i_clk); #1; end
			if(o_busy || o_fault || o_read_valid || o_cell_valid || o_done || o_start_ready)begin
				$display(" > ERR: [Verilog] RESET_STATE mode=%0d",reg_mode); $fatal(1);
			end
		end
	endtask

	// 只把真实start握手当成任务开始。
	task start_job;
		begin
			@(negedge i_clk); i_predictions_committed = 1; i_start_valid = 1;
			@(posedge i_clk);
			while(!o_start_ready)begin @(posedge i_clk); end
			@(negedge i_clk); i_start_valid = 0;
		end
	endtask

	// 取消或读错误不能以返回空闲假装源服务排空。
	task fault_hold;
		begin
			repeat(3)begin @(posedge i_clk); #1; end
			@(negedge i_clk); i_cancel = 0;
			repeat(20)begin
				@(posedge i_clk); #1;
				if(!o_fault || !o_busy || o_start_ready || o_done || o_read_valid || o_read_rsp_ready || o_cell_valid)begin
					$display(" > ERR: [Verilog] FAULT_OWNER_RELEASE mode=%0d",reg_mode); $fatal(1);
				end
			end
		end
	endtask

	// 完整协议恢复必须由共同reset后新任务产生真实cell。
	task recover_job;
		begin
			common_reset;
			reg_mode = 2;
			start_job;
			wait(cnt_cells == 1);
			@(negedge i_clk);
		end
	endtask

	// 单时钟，不混入摄像头或DDR时钟假设。
	initial begin
		forever begin
			#5 i_clk = !i_clk; // 每半周期翻转同域时钟
		end
	end

	// 行服务和cell接收端保持可变等待，输入身份每拍扰动。
	always@(negedge i_clk)begin
		if(!i_rstn)begin
			i_read_ready = 0; i_read_rsp_valid = 0; i_read_rsp_address = 0; i_read_rsp_data = 0;
			i_read_error = 0; i_cell_ready = 0; reg_random = 32'h6ac934e1; cnt_long_hold = 0;
		end else begin
			reg_random = {reg_random[30:0],reg_random[31] ^ reg_random[21] ^ reg_random[1] ^ reg_random[0]};
			i_start_frame_token = reg_random; i_start_model_id = ~reg_random;
			i_read_ready = !flag_force_request_stall && reg_random[1:0] != 0;
			i_cell_ready = !flag_force_cell_stall && reg_random[3:2] != 0;
			if(reg_mode == 0 && o_cell_valid && (o_cell_id == 0 || o_cell_id == 12095) && cnt_long_hold < 40)begin
				i_cell_ready = 0; cnt_long_hold = cnt_long_hold + 1;
			end
			if(reg_mode == 0 && o_cell_id == 1)begin cnt_long_hold = 0; end
			i_read_rsp_valid = flag_pending && (reg_delay == 0 || flag_force_response);
			i_read_rsp_address = reg_pending_address + ((reg_mode == 7 && cnt_responses == 0) ? 32'd16 : 32'd0);
			i_read_rsp_data = reg_pending_data;
			i_read_error = reg_mode == 8 && cnt_responses == 0;
		end
	end

	// 服务只从已接受请求取物理镜像，响应消费后才退休。
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			flag_pending <= 0; reg_pending_address <= 0; reg_pending_data <= 0; reg_delay <= 0;
		end else begin
			if(flag_pending && reg_delay != 0)begin reg_delay <= reg_delay - 1; end
			if(i_read_rsp_valid && o_read_rsp_ready)begin flag_pending <= 0; end
			if(o_read_valid && i_read_ready)begin
				if(flag_pending)begin $display(" > ERR: [Verilog] MULTIPLE_PENDING"); $fatal(1); end
				reg_line_index = find_line(o_read_address);
				if(reg_line_index < 0 || o_read_address[3:0] != 0)begin
					$display(" > ERR: [Verilog] SOURCE_RANGE address=%08x",o_read_address); $fatal(1);
				end
				flag_pending <= 1; reg_pending_address <= o_read_address;
				reg_pending_data <= mem_lines[reg_line_index][127:0];
				reg_delay <= reg_mode == 5 ? 12 : {29'd0,reg_random[6:4]};
			end
		end
	end

	// 比较真实端点，并用内部字段编号定位独立graph地址。
	always@(posedge i_clk or negedge i_rstn)begin
		if(!i_rstn)begin
			cnt_cycle = 0; cnt_cells = 0; cnt_fields = 0; cnt_requests = 0; cnt_responses = 0;
			cnt_request_stalls = 0; cnt_cell_stalls = 0; cnt_response_stalls = 0;
			cnt_last_source = 0; cnt_last_cell = 0; cnt_done = 0; cnt_scale_boundaries = 0;
			flag_request_hold = 0; flag_cell_hold = 0; flag_response_hold = 0; flag_verified_job = 0;
			reg_expected_token = 0; reg_expected_model = 0;
		end else begin
			cnt_cycle = cnt_cycle + 1;
			if(i_start_valid && o_start_ready)begin
				flag_verified_job = 1; reg_expected_token = i_start_frame_token; reg_expected_model = i_start_model_id;
			end
			if(flag_request_hold && !i_cancel && !o_fault && (!o_read_valid || o_read_address !== reg_held_request))begin
				$display(" > ERR: [Verilog] REQUEST_CHANGED"); $fatal(1);
			end
			if(flag_cell_hold && !i_cancel && !o_fault && (!o_cell_valid || {o_cell_data,o_cell_id,o_cell_frame_token,o_cell_model_id} !== reg_held_cell))begin
				$display(" > ERR: [Verilog] CELL_HOLD_CHANGED"); $fatal(1);
			end
			if(flag_response_hold && {i_read_rsp_address,i_read_rsp_data,i_read_error} !== reg_held_response)begin
				$display(" > ERR: [Verilog] RESPONSE_HOLD_CHANGED"); $fatal(1);
			end
			flag_request_hold = o_read_valid && !i_read_ready;
			reg_held_request = o_read_address;
			flag_cell_hold = o_cell_valid && !i_cell_ready;
			reg_held_cell = {o_cell_data,o_cell_id,o_cell_frame_token,o_cell_model_id};
			flag_response_hold = i_read_rsp_valid && !o_read_rsp_ready;
			reg_held_response = {i_read_rsp_address,i_read_rsp_data,i_read_error};
			if(flag_request_hold)begin cnt_request_stalls = cnt_request_stalls + 1; end
			if(flag_cell_hold)begin cnt_cell_stalls = cnt_cell_stalls + 1; end
			if(flag_response_hold)begin cnt_response_stalls = cnt_response_stalls + 1; end
			if(dut.state_current == 1 && dut.flag_hit && !o_fault)begin
				if(dut.dec_field_address !== mem_fields[dut.reg_cell_id * 7 + dut.reg_field])begin
					$display(" > ERR: [Verilog] FIELD_ADDRESS cell=%0d field=%0d actual=%08x",dut.reg_cell_id,dut.reg_field,dut.dec_field_address); $fatal(1);
				end
				if((dut.reg_scale == 0 && (dut.reg_y >= 72 || dut.reg_x >= 128)) ||
					(dut.reg_scale == 1 && (dut.reg_y >= 36 || dut.reg_x >= 64)) ||
					(dut.reg_scale == 2 && (dut.reg_y >= 18 || dut.reg_x >= 32)))begin
					$display(" > ERR: [Verilog] SCALE_TAIL_RANGE"); $fatal(1);
				end
				cnt_fields = cnt_fields + 1;
			end
			if(o_read_valid && i_read_ready)begin
				if(o_read_address !== {mem_fields[dut.reg_cell_id * 7 + dut.reg_field][31:4],4'b0000})begin
					$display(" > ERR: [Verilog] REQUEST_ADDRESS cell=%0d field=%0d",dut.reg_cell_id,dut.reg_field); $fatal(1);
				end
				cnt_requests = cnt_requests + 1;
				$fdisplay(reg_trace_file,"R,%0d,%0d,%0d,%08x",cnt_cycle,dut.reg_cell_id,dut.reg_field,o_read_address);
			end
			if(i_read_rsp_valid && o_read_rsp_ready)begin cnt_responses = cnt_responses + 1; cnt_last_source = cnt_cycle; end
			if(o_cell_valid)begin
				reg_expected_cell = mem_cells[cnt_cells] ^ ((reg_negative != 0 && cnt_cells == 0) ? 112'd1 : 112'd0);
				if(o_cell_data !== reg_expected_cell || o_cell_id !== cnt_cells ||
					o_cell_frame_token !== reg_expected_token || o_cell_model_id !== reg_expected_model || !flag_verified_job)begin
					$display(" > ERR: [Verilog] CELL_MISMATCH cell=%0d actual=%028x expected=%028x token=%08x/%08x",cnt_cells,o_cell_data,reg_expected_cell,o_cell_frame_token,reg_expected_token); $fatal(1);
				end
			end
			if(o_cell_valid && i_cell_ready)begin
				if(o_cell_id == 9216 || o_cell_id == 11520)begin cnt_scale_boundaries = cnt_scale_boundaries + 1; end
				$fdisplay(reg_trace_file,"C,%0d,%0d,%028x,%08x,%08x",cnt_cycle,cnt_cells,o_cell_data,o_cell_frame_token,o_cell_model_id);
				cnt_cells = cnt_cells + 1; cnt_last_cell = cnt_cycle;
			end
			if(o_done)begin
				cnt_done = cnt_done + 1;
				if(cnt_cells != 12096 || cnt_fields != 84672 || cnt_requests != cnt_responses || flag_pending ||
					cnt_last_source >= cnt_last_cell || cnt_last_cell >= cnt_cycle || cnt_done != 1 || !o_busy || cnt_scale_boundaries != 2)begin
					$display(" > ERR: [Verilog] EARLY_DONE cells=%0d fields=%0d pending=%0d lastread=%0d lastcell=%0d done=%0d",cnt_cells,cnt_fields,flag_pending,cnt_last_source,cnt_last_cell,cnt_cycle); $fatal(1);
				end
			end
		end
	end

	// 独立案例先检查保持条件，再共同reset验证恢复。
	initial begin
		if(!$value$plusargs("VECTOR_ROOT=%s",reg_root))begin $fatal(1,"VECTOR_ROOT required"); end
		if(!$value$plusargs("TRACE=%s",reg_trace))begin $fatal(1,"TRACE required"); end
		if(!$value$plusargs("MODE=%d",reg_mode))begin reg_mode = 0; end
		if(!$value$plusargs("NEGATIVE=%d",reg_negative))begin reg_negative = 0; end
		reg_case = reg_mode;
		$readmemh({reg_root,"/prediction_lines160.hex"},mem_lines);
		$readmemh({reg_root,"/cell_field_addresses32.hex"},mem_fields);
		$readmemh({reg_root,"/head_cells112.hex"},mem_cells);
		reg_trace_file = $fopen(reg_trace,"w");
		if(reg_trace_file == 0)begin $fatal(1,"TRACE open failed"); end
		common_reset;
		if(reg_mode == 1)begin
			@(negedge i_clk); i_start_valid = 1;
			repeat(20)begin
				@(posedge i_clk); #1;
				if(o_start_ready || o_busy || o_read_valid || o_cell_valid)begin $fatal(1,"UNCOMMITTED_ADMITTED"); end
			end
			@(negedge i_clk); i_start_valid = 0;
		end
		if(reg_mode == 3 || reg_mode == 4)begin flag_force_request_stall = 1; end
		if(reg_mode == 6 || reg_mode == 9)begin flag_force_cell_stall = 1; end
		start_job;
		case(reg_mode)
			0:begin
				wait(cnt_done == 1); @(negedge i_clk); @(posedge i_clk); #1;
				if(o_busy || o_done || cnt_request_stalls == 0 || cnt_cell_stalls < 80)begin $fatal(1,"NORMAL_RETIREMENT"); end
			end
			1,2:begin wait(cnt_cells == 2); @(negedge i_clk); end
			3:begin wait(o_read_valid && !i_read_ready); @(negedge i_clk); i_cancel = 1; fault_hold; recover_job; end
			4:begin wait(o_read_valid && !i_read_ready); repeat(5)begin @(posedge i_clk); end recover_job; end
			5:begin
				wait(flag_pending); @(negedge i_clk); i_cancel = 1; flag_force_response = 1;
				wait(i_read_rsp_valid && !o_read_rsp_ready); repeat(5)begin @(posedge i_clk); end recover_job;
			end
			6:begin wait(o_cell_valid && !i_cell_ready); repeat(5)begin @(posedge i_clk); end recover_job; end
			7,8:begin wait(o_fault); fault_hold; recover_job; end
			9:begin wait(o_cell_valid && !i_cell_ready); @(negedge i_clk); i_cancel = 1; fault_hold; recover_job; end
			default:begin $fatal(1,"UNKNOWN_MODE"); end
		endcase
		flag_test_complete = 1;
		$display("HEAD_STREAM_PASS mode=%0d cells=%0d fields=%0d reads=%0d responses=%0d cycles=%0d reqstall=%0d cellstall=%0d rspstall=%0d lastread=%0d lastcell=%0d",reg_case,cnt_cells,cnt_fields,cnt_requests,cnt_responses,cnt_cycle,cnt_request_stalls,cnt_cell_stalls,cnt_response_stalls,cnt_last_source,cnt_last_cell);
		$fclose(reg_trace_file); $finish;
	end

	// 挂起不会被误报成功。
	initial begin
		repeat(2000000)begin @(posedge i_clk); end
		$display(" > ERR: [Verilog] WATCHDOG mode=%0d state=%0d cells=%0d",reg_mode,dut.state_current,cnt_cells); $fatal(1);
	end

	//---------------模块实例化区域---------------//
	// DUT保持原始所有端口与内部存储组织。
	road_head_cell_stream dut(
		.i_clk(i_clk), .i_rstn(i_rstn), .i_cancel(i_cancel),
		.i_start_valid(i_start_valid), .i_start_frame_token(i_start_frame_token), .i_start_model_id(i_start_model_id),
		.i_predictions_committed(i_predictions_committed), .i_read_ready(i_read_ready),
		.i_read_rsp_valid(i_read_rsp_valid), .i_read_rsp_address(i_read_rsp_address), .i_read_rsp_data(i_read_rsp_data),
		.i_read_error(i_read_error), .i_cell_ready(i_cell_ready), .o_start_ready(o_start_ready), .o_busy(o_busy),
		.o_done(o_done), .o_fault(o_fault), .o_read_valid(o_read_valid), .o_read_address(o_read_address),
		.o_read_rsp_ready(o_read_rsp_ready), .o_cell_valid(o_cell_valid), .o_cell_data(o_cell_data),
		.o_cell_id(o_cell_id), .o_cell_frame_token(o_cell_frame_token), .o_cell_model_id(o_cell_model_id)
	);
endmodule
