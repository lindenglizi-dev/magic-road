`timescale 1ns / 1ps

////////////////////////////////////English///////////////////////////////////////
// Company:         Erie
// Engineer:        Erie
//
// Create Date:     2026/10/02 02:21:43
// Design Name:     ccl_pipeline_trial_top
// Module Name:     ccl_pipeline_trial_top
// Description:     description/ccl_pipeline_trial_top_Design.pdf
// Simulations:     testbench/vivado/2021.1/ccl_pipeline_trial_top
//
// Referrences:     None
//
// Dependencies:    None
//
// Version:         V1.0
// Revision Date:   2026/10/02 02:21:43
// History:
// Time             Version     Revised by        Contents
// 2026/10/02       V1.0        Erie              Create file.
///////////////////////////////////Chinese////////////////////////////////////////
// 版权归属:        Erie
// 开发人员:        Erie
//
// 创建日期:        2026年10月02日
// 设计名称:        ccl_pipeline_trial_top
// 模块名称:        ccl_pipeline_trial_top
// 模块说明:        Description/ccl_pipeline_trial_top_Design.pdf
// 仿真工程:        TestBench/Vivado/2021.1/ccl_pipeline_trial_top
//
// 参考资料:        None
//
// 依赖文件:        None
//
// 当前版本:        V1.0
// 修订日期:        2026年10月02日
// 修订历史:
// 时间             版本        修订人            修订内容
// 2026年10月02日   V1.0        Erie              创建文件

module ccl_pipeline_trial_top
#(
	parameter C_WIDTH = 129,                    // parameter
	parameter C_HEIGHT = 8,                     // parameter
	parameter C_X_WIDTH = 8,                    // parameter
	parameter C_Y_WIDTH = 4,                    // parameter
	parameter C_ID_WIDTH = 32,                  // parameter
	parameter C_LABEL_WIDTH = 8,                // parameter
	parameter C_MAX_LABEL = 128,                // parameter
	parameter C_MAX_RUN = 64,                   // parameter
	parameter C_AREA_WIDTH = 16,                // parameter
	parameter C_MIN_RUN_LENGTH = 1,             // parameter
	parameter C_MIN_AREA = 1                    // parameter
)
(
	//-----------------全局信号-----------------//
	input i_clk,                                // port signal
	input i_rstn,                               // port signal
	output o_core_reset_active,                 // port signal

	//-----------------用户接口-----------------//
	input i_task_valid,                         // port signal
	input [C_ID_WIDTH - 1:0]i_task_id,          // port signal
	input [C_ID_WIDTH - 1:0]i_task_frame_id,    // port signal
	input i_in_valid,                           // port signal
	input [C_ID_WIDTH - 1:0]i_in_task_id,       // port signal

	//IN接口
	input [C_Y_WIDTH - 1:0]i_in_y,              // port signal
	input i_in_pixel,                           // port signal
	input i_in_last,                            // port signal
	input i_in_frame_last,                      // port signal
	input i_cancel,                             // port signal
	input i_candidate_release,                  // port signal
	input i_read_valid,                         // port signal
	input [1:0]i_read_index,                    // port signal
	input i_response_ready,                     // port signal
	input i_processed_valid,                    // port signal
	input [C_ID_WIDTH - 1:0]i_processed_task_id, // port signal
	input [C_ID_WIDTH - 1:0]i_processed_frame_id, // port signal
	input [2:0]i_processed_count,               // port signal
	input [2:0]i_accepted_count,                // port signal
	input i_processed_error,                    // port signal
	input i_object_done_valid,                  // port signal
	input [C_ID_WIDTH - 1:0]i_object_task_id,   // port signal
	input [C_ID_WIDTH - 1:0]i_object_frame_id,  // port signal
	input [1:0]i_object_done_index,             // port signal
	input i_object_accepted,                    // port signal
	input i_display_commit_ack,                 // port signal
	input [C_ID_WIDTH - 1:0]i_display_ack_task_id, // port signal
	input [C_ID_WIDTH - 1:0]i_display_ack_frame_id, // port signal
	input i_commit_ready,                       // port signal
	input i_failure_ack,                        // port signal
	output o_task_ready,                        // port signal
	output o_in_ready,                          // port signal
	output o_rejected_input,                    // port signal

	//CANDIDATE接口
	output o_candidate_valid,                   // port signal
	output o_candidate_success,                 // port signal
	output [7:0]o_candidate_reason,             // port signal
	output [2:0]o_candidate_count,              // port signal
	output [C_ID_WIDTH - 1:0]o_candidate_task_id, // port signal
	output [C_ID_WIDTH - 1:0]o_candidate_frame_id, // port signal
	output o_candidate_release_blocked,         // port signal
	output o_read_ready,                        // port signal

	//RESPONSE接口
	output o_response_valid,                    // port signal
	output [1:0]o_response_index,               // port signal
	output [C_LABEL_WIDTH - 1:0]o_response_label, // port signal
	output [C_X_WIDTH - 1:0]o_response_xmin,    // port signal
	output [C_X_WIDTH - 1:0]o_response_xmax,    // port signal
	output [C_Y_WIDTH - 1:0]o_response_ymin,    // port signal
	output [C_Y_WIDTH - 1:0]o_response_ymax,    // port signal
	output [C_AREA_WIDTH - 1:0]o_response_area, // port signal
	output [C_ID_WIDTH - 1:0]o_response_task_id, // port signal
	output [C_ID_WIDTH - 1:0]o_response_frame_id, // port signal
	output o_processed_ready,                   // port signal
	output o_object_done_ready,                 // port signal

	//FINAL接口
	output o_final_valid,                       // port signal
	output o_final_success,                     // port signal
	output [7:0]o_final_reason,                 // port signal
	output [2:0]o_final_candidate_count,        // port signal
	output [2:0]o_final_processed_count,        // port signal
	output [2:0]o_final_accepted_count,         // port signal
	output [C_ID_WIDTH - 1:0]o_final_task_id,   // port signal
	output [C_ID_WIDTH - 1:0]o_final_frame_id,  // port signal
	output o_commit_valid,                      // port signal
	output o_algorithm_release,                 // port signal
	output o_banks_empty,                       // port signal
	output o_abort_active                       // port signal
);

	//---------------配置参数区域---------------//
	localparam IDLE = 3'd0;                     // parameter
	localparam RUN = 3'd1;                      // parameter
	localparam DRAIN = 3'd2;                    // parameter
	localparam RESET_CORE = 3'd3;               // parameter
	localparam RECOVER = 3'd4;                  // parameter
	localparam CANDIDATE = 3'd5;                // parameter
	localparam PROCESS = 3'd6;                  // parameter
	localparam FINAL = 3'd7;                    // parameter

	//---------------状态参数区域---------------//
	localparam ST_WAIT_ROW = 3'd0;              // parameter
	localparam ST_PIXELS = 3'd1;                // parameter
	localparam ST_EOL = 3'd2;                   // parameter
	localparam ST_ROW_COMMIT = 3'd3;            // parameter
	localparam ST_LAST_ROW = 3'd4;              // parameter
	localparam ST_EOF_EVENT = 3'd5;             // parameter
	localparam ST_INPUT_DONE = 3'd6;            // parameter

	//--------------模块实例化信号--------------//
	//ccl_pixel_line_banks--用户接口
	wire bank_ready;                            // signal
	wire bank_valid;                            // signal
	wire [C_ID_WIDTH - 1:0]bank_task;           // signal
	wire [C_Y_WIDTH - 1:0]bank_y;               // signal
	wire [C_X_WIDTH - 1:0]bank_x;               // signal
	wire bank_pixel;                            // signal
	wire bank_last;                             // signal
	wire bank_frame_last;                       // signal
	wire bank_error;                            // signal

	//ccl_task_guard--用户接口
	wire guard_ready;                           // signal
	wire guard_stream_enable;                   // signal

	//ccl_task_guard--全局信号
	wire guard_clear;                           // signal

	//ccl_task_guard--用户接口
	wire guard_rejected;                        // signal
	wire guard_abort;                           // signal
	wire guard_valid;                           // signal
	wire guard_cancelled;                       // signal
	wire guard_rd_valid;                        // signal
	wire [C_LABEL_WIDTH - 1:0]guard_label;      // signal
	wire [C_X_WIDTH - 1:0]guard_xmin;           // signal
	wire [C_X_WIDTH - 1:0]guard_xmax;           // signal
	wire [C_Y_WIDTH - 1:0]guard_ymin;           // signal
	wire [C_Y_WIDTH - 1:0]guard_ymax;           // signal
	wire [C_AREA_WIDTH - 1:0]guard_area;        // signal

	//ccl_rle_stream_core--用户接口
	wire core_ready;                            // signal
	wire core_commit;                           // signal
	wire core_idle;                             // signal
	wire core_obj_valid;                        // signal
	wire [1:0]core_index;                       // signal
	wire [C_LABEL_WIDTH - 1:0]core_label;       // signal
	wire [C_X_WIDTH - 1:0]core_xmin;            // signal
	wire [C_X_WIDTH - 1:0]core_xmax;            // signal
	wire [C_Y_WIDTH - 1:0]core_ymin;            // signal
	wire [C_Y_WIDTH - 1:0]core_ymax;            // signal
	wire [C_X_WIDTH - 1:0]core_center_x;        // signal
	wire [C_Y_WIDTH - 1:0]core_center_y;        // signal
	wire [C_AREA_WIDTH - 1:0]core_area;         // signal
	wire core_done;                             // signal
	wire core_row_done;                         // signal
	wire core_run_error;                        // signal
	wire core_label_error;                      // signal
	wire core_raw_error;                        // signal
	wire core_labeled_error;                    // signal
	wire core_protocol_error;                   // signal
	wire core_error;                            // signal

	//-----------------计数信号-----------------//
	reg [2:0]cnt_read = 0;                      // signal
	wire [2:0]cnt_core;                         // signal

	//----------------状态机信号----------------//
	reg [2:0]state_state = 0;                   // signal
	reg [2:0]state_next_state = 0;              // signal
	reg [2:0]state_current = 0;                 // signal
	reg [2:0]state_next = 0;                    // signal

	//----------------寄存器信号----------------//
	//ccl_pixel_line_banks--用户接口
	reg [C_ID_WIDTH - 1:0]reg_line_task = 0;    // signal
	reg reg_line_frame_last = 0;                // signal
	reg reg_input_error = 0;                    // signal
	reg reg_input_complete = 0;                 // signal

	//ccl_rle_stream_core--用户接口
	reg [C_Y_WIDTH:0]reg_committed_rows = 0;    // signal
	reg [C_Y_WIDTH:0]reg_completed_rows = 0;    // signal
	reg reg_read_pending = 0;                   // signal
	reg [1:0]reg_pending_index = 0;             // signal
	reg [2:0]reg_completed_objects = 0;         // signal
	reg [2:0]reg_accepted_objects = 0;          // signal
	reg reg_processing_fault = 0;               // signal
	reg reg_commit_published = 0;               // signal
	reg reg_previous_display_ack = 0;           // signal

	//-----------------其他信号-----------------//
	wire accepted;                              // signal
	wire guard_release;                         // signal
	wire bank_take;                             // signal
	wire core_rst_n;                            // signal
	wire abort_now;                             // signal
	wire drain_done;                            // signal
	wire event_valid;                           // signal
	wire read_take;                             // signal
	wire response_take;                         // signal
	wire table_read_done;                       // signal
	wire pixel_event;                           // signal
	wire eol_event;                             // signal
	wire eof_event;                             // signal
	wire processed_identity_ok;                 // signal
	wire processed_counts_ok;                   // signal
	wire object_take;                           // signal
	wire object_identity_ok;                    // signal
	wire object_index_ok;                       // signal
	wire processed_take;                        // signal
	wire qualified_display_ack;                 // signal
	wire display_identity_ok;                   // signal
	wire commit_take;                           // signal
	wire [7:0]error_reason;                     // signal

	//-----------------输出信号-----------------//
	//全局信号
	reg core_reset_active_o = 0;                // internal output signal

	//用户接口CANDIDATE接口
	wire candidate_success_o;                   // signal
	wire [7:0]candidate_reason_o;               // signal
	wire [2:0]cnt_candidate_o;                  // signal

	//用户接口
	reg [C_ID_WIDTH - 1:0]reg_active_task = 0;  // signal
	reg [C_ID_WIDTH - 1:0]reg_active_frame = 0; // signal

	//用户接口RESPONSE接口
	reg response_valid_o = 0;                   // internal output signal
	reg [1:0]response_index_o = 0;              // internal output signal
	reg [C_LABEL_WIDTH - 1:0]response_label_o = 0; // internal output signal
	reg [C_X_WIDTH - 1:0]response_xmin_o = 0;   // internal output signal
	reg [C_X_WIDTH - 1:0]response_xmax_o = 0;   // internal output signal
	reg [C_Y_WIDTH - 1:0]response_ymin_o = 0;   // internal output signal
	reg [C_Y_WIDTH - 1:0]response_ymax_o = 0;   // internal output signal
	reg [C_AREA_WIDTH - 1:0]response_area_o = 0; // internal output signal

	//用户接口
	reg [C_ID_WIDTH - 1:0]response_task_id_o = 0; // internal output signal
	reg [C_ID_WIDTH - 1:0]response_frame_id_o = 0; // internal output signal

	//用户接口FINAL接口
	reg final_success_o = 0;                    // internal output signal
	reg [7:0]final_reason_o = 0;                // internal output signal

	//用户接口
	reg [2:0]cnt_final_candidate_o = 0;         // internal output signal
	reg [2:0]cnt_final_processed_o = 0;         // internal output signal
	reg [2:0]cnt_final_accepted_o = 0;          // internal output signal
	reg banks_empty_o = 0;                      // internal output signal
	wire abort_active_o;                        // signal

	//---------------其他信号连线---------------//
	//其他信号连线
	assign accepted = i_task_valid && o_task_ready; // assign
	assign abort_now = (state_state == RUN) && (i_cancel || bank_error || reg_input_error || core_error); // assign
	assign abort_active_o = abort_now || (state_state == DRAIN) || (state_state == RESET_CORE) || (state_state == RECOVER); // assign
	assign core_rst_n = i_rstn && !core_reset_active_o; // assign
	assign pixel_event = (state_state == RUN) && (state_current == ST_PIXELS) && bank_valid; // assign
	assign eol_event = (state_state == RUN) && (state_current == ST_EOL); // assign
	assign eof_event = (state_state == RUN) && (state_current == ST_EOF_EVENT); // assign
	assign event_valid = pixel_event || eol_event || eof_event; // assign
	assign bank_take = pixel_event && guard_stream_enable && !abort_now; // assign
	assign error_reason = {4'd0, (core_error || bank_error || reg_input_error), core_run_error, core_label_error, 1'b0}; // assign
	assign drain_done = (state_state == RECOVER) && banks_empty_o && core_idle && !core_error; // assign
	assign read_take = i_read_valid && o_read_ready; // assign
	assign response_take = response_valid_o && i_response_ready; // assign
	assign table_read_done = !reg_read_pending && !response_valid_o && (cnt_read == cnt_candidate_o); // assign
	assign guard_release = i_candidate_release && o_candidate_valid && table_read_done; // assign
	assign object_take = i_object_done_valid && o_object_done_ready; // assign
	assign object_identity_ok = (i_object_task_id == reg_active_task) && (i_object_frame_id == reg_active_frame); // assign
	assign object_index_ok = (i_object_done_index == reg_completed_objects) && (reg_completed_objects < cnt_final_candidate_o); // assign
	assign processed_take = i_processed_valid && o_processed_ready; // assign
	assign processed_identity_ok = (i_processed_task_id == reg_active_task) && (i_processed_frame_id == reg_active_frame); // assign
	assign processed_counts_ok = (i_processed_count == cnt_final_candidate_o) && (i_processed_count == reg_completed_objects) && (i_accepted_count == reg_accepted_objects); // assign
	assign commit_take = o_commit_valid && i_commit_ready; // assign
	assign display_identity_ok = (i_display_ack_task_id == reg_active_task) && (i_display_ack_frame_id == reg_active_frame); // assign
	assign qualified_display_ack = i_display_commit_ack && !reg_previous_display_ack && reg_commit_published && display_identity_ok; // assign

	//---------------输出信号连线---------------//
	//全局信号
	assign o_core_reset_active = core_reset_active_o; // output bridge

	//用户接口
	assign o_task_ready = (state_state == IDLE) && guard_ready && banks_empty_o; // assign
	assign o_in_ready = (state_state == RUN) && !abort_now && !reg_input_complete && (i_in_task_id == reg_active_task) && bank_ready; // assign
	assign o_rejected_input = i_in_valid && (i_in_task_id != reg_active_task || state_state != RUN); // assign

	//用户接口CANDIDATE接口
	assign o_candidate_valid = guard_valid && (state_state == CANDIDATE); // assign
	assign o_candidate_success = candidate_success_o; // assign
	assign o_candidate_reason = candidate_reason_o; // assign
	assign o_candidate_count = cnt_candidate_o; // assign

	//用户接口
	assign o_candidate_task_id = reg_active_task; // assign
	assign o_candidate_frame_id = reg_active_frame; // assign
	assign o_candidate_release_blocked = i_candidate_release && o_candidate_valid && !table_read_done; // assign
	assign o_read_ready = o_candidate_valid && candidate_success_o && !reg_read_pending && !response_valid_o && (cnt_read < cnt_candidate_o) && (i_read_index == cnt_read); // assign

	//用户接口RESPONSE接口
	assign o_response_valid = response_valid_o; // output bridge
	assign o_response_index = response_index_o; // output bridge
	assign o_response_label = response_label_o; // output bridge
	assign o_response_xmin = response_xmin_o;   // output bridge
	assign o_response_xmax = response_xmax_o;   // output bridge
	assign o_response_ymin = response_ymin_o;   // output bridge
	assign o_response_ymax = response_ymax_o;   // output bridge
	assign o_response_area = response_area_o;   // output bridge

	//用户接口
	assign o_response_task_id = response_task_id_o; // output bridge
	assign o_response_frame_id = response_frame_id_o; // output bridge
	assign o_processed_ready = (state_state == PROCESS) && !i_object_done_valid; // assign

	// A last object completion precedes the aggregate report even if both VALIDs arrive together.
	assign o_object_done_ready = (state_state == PROCESS); // assign

	//用户接口FINAL接口
	assign o_final_valid = (state_state == FINAL); // assign
	assign o_final_success = final_success_o;   // output bridge
	assign o_final_reason = final_reason_o;     // output bridge

	//用户接口
	assign o_final_candidate_count = cnt_final_candidate_o; // output bridge
	assign o_final_processed_count = cnt_final_processed_o; // output bridge
	assign o_final_accepted_count = cnt_final_accepted_o; // output bridge
	assign o_final_task_id = reg_active_task;   // assign
	assign o_final_frame_id = reg_active_frame; // assign
	assign o_commit_valid = o_final_valid && final_success_o && !reg_commit_published; // assign
	assign o_algorithm_release = o_final_valid && (final_success_o ? qualified_display_ack : i_failure_ack); // assign
	assign o_banks_empty = banks_empty_o;       // output bridge
	assign o_abort_active = abort_active_o;     // assign

	//-------------输出信号处理区域-------------//
	//用户接口
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			cnt_final_accepted_o <= 0;
		end else begin
			// Registered reset avoids combinational state_state-decode glitches on asynchronous resets.
			if(accepted == 1'b1)begin
				cnt_final_accepted_o <= 0;
			end
			if(processed_take == 1'b1)begin
				cnt_final_accepted_o <= i_accepted_count;
			end
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			cnt_final_candidate_o <= 0;
		end else begin
			// Registered reset avoids combinational state_state-decode glitches on asynchronous resets.
			if(accepted == 1'b1)begin
				cnt_final_candidate_o <= 0;
			end
			if(guard_release == 1'b1)begin
				cnt_final_candidate_o <= cnt_candidate_o;
			end
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			cnt_final_processed_o <= 0;
		end else begin
			// Registered reset avoids combinational state_state-decode glitches on asynchronous resets.
			if(accepted == 1'b1)begin
				cnt_final_processed_o <= 0;
			end
			if(processed_take == 1'b1)begin
				cnt_final_processed_o <= i_processed_count;
			end
		end
	end

	//全局信号
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			core_reset_active_o <= 0;
		end else begin
			// Registered reset avoids combinational state_state-decode glitches on asynchronous resets.
			core_reset_active_o <= (state_next_state == RESET_CORE);
		end
	end

	//用户接口FINAL接口
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			final_reason_o <= 0;
		end else begin
			// Registered reset avoids combinational state_state-decode glitches on asynchronous resets.
			if(accepted == 1'b1)begin
				final_reason_o <= 0;
			end
			if(guard_release == 1'b1)begin
				final_reason_o <= candidate_reason_o;
			end
			if(processed_take == 1'b1)begin
				if(i_processed_error == 1'b1 || reg_processing_fault == 1'b1 || processed_identity_ok == 1'b0 || processed_counts_ok == 1'b0)begin
					final_reason_o <= 8'h40;
				end
			end
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			final_success_o <= 0;
		end else begin
			// Registered reset avoids combinational state_state-decode glitches on asynchronous resets.
			if(accepted == 1'b1)begin
				final_success_o <= 0;
			end
			if(guard_release == 1'b1)begin
				final_success_o <= 0;
			end
			if(processed_take == 1'b1)begin
				final_success_o <= !i_processed_error && !reg_processing_fault &&
				processed_identity_ok && processed_counts_ok;
			end
		end
	end

	//用户接口
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_active_frame <= 0;
		end else begin
			// Registered reset avoids combinational state_state-decode glitches on asynchronous resets.
			if(accepted == 1'b1)begin
				reg_active_frame <= i_task_frame_id;
			end
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_active_task <= 0;
		end else begin
			// Registered reset avoids combinational state_state-decode glitches on asynchronous resets.
			if(accepted == 1'b1)begin
				reg_active_task <= i_task_id;
			end
		end
	end

	//用户接口RESPONSE接口
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			response_area_o <= 0;
		end else begin
			// Registered reset avoids combinational state_state-decode glitches on asynchronous resets.
			if(reg_read_pending == 1'b1)begin
				response_area_o <= guard_area;
			end
		end
	end

	//用户接口
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			response_frame_id_o <= 0;
		end else begin
			// Registered reset avoids combinational state_state-decode glitches on asynchronous resets.
			if(reg_read_pending == 1'b1)begin
				response_frame_id_o <= reg_active_frame;
			end
		end
	end

	//用户接口RESPONSE接口
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			response_index_o <= 0;
		end else begin
			// Registered reset avoids combinational state_state-decode glitches on asynchronous resets.
			if(reg_read_pending == 1'b1)begin
				response_index_o <= reg_pending_index;
			end
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			response_label_o <= 0;
		end else begin
			// Registered reset avoids combinational state_state-decode glitches on asynchronous resets.
			if(reg_read_pending == 1'b1)begin
				response_label_o <= guard_label;
			end
		end
	end

	//用户接口
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			response_task_id_o <= 0;
		end else begin
			// Registered reset avoids combinational state_state-decode glitches on asynchronous resets.
			if(reg_read_pending == 1'b1)begin
				response_task_id_o <= reg_active_task;
			end
		end
	end

	//用户接口RESPONSE接口
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			response_valid_o <= 0;
		end else begin
			// Registered reset avoids combinational state_state-decode glitches on asynchronous resets.
			if(accepted == 1'b1)begin
				response_valid_o <= 0;
			end
			if(reg_read_pending == 1'b1)begin
				response_valid_o <= 1;
			end
			if(response_take == 1'b1)begin
				response_valid_o <= 0;
			end
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			response_xmax_o <= 0;
		end else begin
			// Registered reset avoids combinational state_state-decode glitches on asynchronous resets.
			if(reg_read_pending == 1'b1)begin
				response_xmax_o <= guard_xmax;
			end
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			response_xmin_o <= 0;
		end else begin
			// Registered reset avoids combinational state_state-decode glitches on asynchronous resets.
			if(reg_read_pending == 1'b1)begin
				response_xmin_o <= guard_xmin;
			end
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			response_ymax_o <= 0;
		end else begin
			// Registered reset avoids combinational state_state-decode glitches on asynchronous resets.
			if(reg_read_pending == 1'b1)begin
				response_ymax_o <= guard_ymax;
			end
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			response_ymin_o <= 0;
		end else begin
			// Registered reset avoids combinational state_state-decode glitches on asynchronous resets.
			if(reg_read_pending == 1'b1)begin
				response_ymin_o <= guard_ymin;
			end
		end
	end

	//----------------状态机区域----------------//
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			state_current <= ST_WAIT_ROW;
		end else begin
			state_current <= state_next;
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			state_state <= IDLE;
		end else begin
			state_state <= state_next_state;
		end
	end

	always@(*)begin
		state_next_state = state_state;
		case(state_state)
			IDLE:begin
				if(accepted == 1'b1)begin
					state_next_state = RUN;
				end
			end
			RUN:begin
				if(abort_now == 1'b1)begin
					state_next_state = DRAIN;
				end else if(guard_valid == 1'b1)begin
					state_next_state = CANDIDATE;
				end
			end
			DRAIN:begin
				if(banks_empty_o == 1'b1)begin
					state_next_state = RESET_CORE;
				end
			end
			RESET_CORE:begin
				state_next_state = RECOVER;
			end
			RECOVER:begin
				if(drain_done == 1'b1)begin
					state_next_state = CANDIDATE;
				end
			end
			CANDIDATE:begin
				if(guard_release == 1'b1)begin
					if(candidate_success_o == 1'b1)begin
						state_next_state = PROCESS;
					end else begin
						state_next_state = FINAL;
					end
				end
			end
			PROCESS:begin
				if(processed_take == 1'b1)begin
					state_next_state = FINAL;
				end
			end
			FINAL:begin
				if(o_algorithm_release == 1'b1)begin
					state_next_state = IDLE;
				end
			end
			default:begin
				state_next_state = IDLE;
			end
		endcase
	end

	always@(*)begin
		state_next = state_current;
		if(accepted == 1'b1 || abort_active_o == 1'b1)begin
			state_next = ST_WAIT_ROW;
		end else if(state_state == RUN)begin
			case(state_current)
				ST_WAIT_ROW:begin
					if(core_ready == 1'b1)begin
						state_next = ST_PIXELS;
					end
				end
				ST_PIXELS:begin
					if(bank_take == 1'b1 && bank_last == 1'b1)begin
						state_next = ST_EOL;
					end
				end
				ST_EOL:begin
					if(guard_stream_enable == 1'b1)begin
						state_next = ST_ROW_COMMIT;
					end
				end
				ST_ROW_COMMIT:begin
					if(core_commit == 1'b1)begin
						if(reg_line_frame_last == 1'b1)begin
							state_next = ST_LAST_ROW;
						end else begin
							state_next = ST_WAIT_ROW;
						end
					end
				end
				ST_LAST_ROW:begin
					if(reg_completed_rows == C_HEIGHT)begin
						state_next = ST_EOF_EVENT;
					end
				end
				ST_EOF_EVENT:begin
					if(guard_stream_enable == 1'b1)begin
						state_next = ST_INPUT_DONE;
					end
				end
				ST_INPUT_DONE:begin
					state_next = ST_INPUT_DONE;
				end
				default:begin
					state_next = ST_WAIT_ROW;
				end
			endcase
		end
	end

	//-------------状态任务处理区域-------------//
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_committed_rows <= 0;
		end else begin
			// Registered reset avoids combinational state_state-decode glitches on asynchronous resets.
			if(accepted == 1'b1)begin
				reg_committed_rows <= 0;
			end
			if((state_state == RUN) && (state_current == ST_ROW_COMMIT) && core_commit == 1'b1)begin
				reg_committed_rows <= reg_committed_rows + 1'b1;
			end
		end
	end

	//-------------主要任务处理区域-------------//
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			cnt_read <= 0;
		end else begin
			// Registered reset avoids combinational state_state-decode glitches on asynchronous resets.
			if(accepted == 1'b1)begin
				cnt_read <= 0;
			end
			if(response_take == 1'b1)begin
				cnt_read <= cnt_read + 1'b1;
			end
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_accepted_objects <= 0;
		end else begin
			// Registered reset avoids combinational state_state-decode glitches on asynchronous resets.
			if(accepted == 1'b1)begin
				reg_accepted_objects <= 0;
			end
			if(object_take == 1'b1)begin
				if(object_identity_ok == 1'b0 || object_index_ok == 1'b0)begin
					reg_accepted_objects <= reg_accepted_objects;
				end else begin
					if(i_object_accepted == 1'b1)begin
						reg_accepted_objects <= reg_accepted_objects + 1'b1;
					end
				end
			end
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_commit_published <= 0;
		end else begin
			// Registered reset avoids combinational state_state-decode glitches on asynchronous resets.
			if(commit_take == 1'b1)begin
				reg_commit_published <= 1;
			end
			if(accepted == 1'b1)begin
				reg_commit_published <= 0;
			end
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_completed_objects <= 0;
		end else begin
			// Registered reset avoids combinational state_state-decode glitches on asynchronous resets.
			if(accepted == 1'b1)begin
				reg_completed_objects <= 0;
			end
			if(object_take == 1'b1)begin
				if(object_identity_ok == 1'b0 || object_index_ok == 1'b0)begin
					reg_completed_objects <= reg_completed_objects;
				end else begin
					reg_completed_objects <= reg_completed_objects + 1'b1;
				end
			end
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_completed_rows <= 0;
		end else begin
			// Registered reset avoids combinational state_state-decode glitches on asynchronous resets.
			if(accepted == 1'b1)begin
				reg_completed_rows <= 0;
			end
			if((state_state == RUN) && core_row_done == 1'b1)begin
				reg_completed_rows <= reg_completed_rows + 1'b1;
			end
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_input_complete <= 0;
		end else begin
			// Registered reset avoids combinational state_state-decode glitches on asynchronous resets.
			if(accepted == 1'b1)begin
				reg_input_complete <= 0;
			end
			if(i_in_valid == 1'b1 && o_in_ready == 1'b1 && i_in_frame_last == 1'b1)begin
				reg_input_complete <= 1;
			end
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_input_error <= 0;
		end else begin
			// Registered reset avoids combinational state_state-decode glitches on asynchronous resets.
			if(accepted == 1'b1)begin
				reg_input_error <= 0;
			end
			if(bank_take == 1'b1 && bank_last == 1'b1)begin
				if(bank_frame_last != (bank_y == C_HEIGHT - 1) || bank_y != reg_committed_rows)begin
					reg_input_error <= 1;
				end
			end
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_line_frame_last <= 0;
		end else begin
			// Registered reset avoids combinational state_state-decode glitches on asynchronous resets.
			if(bank_take == 1'b1 && bank_last == 1'b1)begin
				reg_line_frame_last <= bank_frame_last;
			end
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_line_task <= 0;
		end else begin
			// Registered reset avoids combinational state_state-decode glitches on asynchronous resets.
			if(bank_take == 1'b1 && bank_last == 1'b1)begin
				reg_line_task <= bank_task;
			end
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_pending_index <= 0;
		end else begin
			// Registered reset avoids combinational state_state-decode glitches on asynchronous resets.
			if(read_take == 1'b1)begin
				reg_pending_index <= i_read_index;
			end
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_previous_display_ack <= 0;
		end else begin
			// Registered reset avoids combinational state_state-decode glitches on asynchronous resets.
			reg_previous_display_ack <= i_display_commit_ack;
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_processing_fault <= 0;
		end else begin
			// Registered reset avoids combinational state_state-decode glitches on asynchronous resets.
			if(accepted == 1'b1)begin
				reg_processing_fault <= 0;
			end
			if(object_take == 1'b1)begin
				if(object_identity_ok == 1'b0 || object_index_ok == 1'b0)begin
					reg_processing_fault <= 1;
				end else begin
					reg_processing_fault <= reg_processing_fault;
				end
			end
		end
	end

	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_read_pending <= 0;
		end else begin
			// Registered reset avoids combinational state_state-decode glitches on asynchronous resets.
			if(accepted == 1'b1)begin
				reg_read_pending <= 0;
			end
			if(read_take == 1'b1)begin
				reg_read_pending <= 1;
			end
			if(reg_read_pending == 1'b1)begin
				reg_read_pending <= 0;
			end
		end
	end

	//--------------模块实例化区域--------------//
	ccl_pixel_line_banks #(
		.WIDTH(C_WIDTH),                        // WIDTH参数映射为C_WIDTH
		.X_WIDTH(C_X_WIDTH),                    // X_WIDTH参数映射为C_X_WIDTH
		.Y_WIDTH(C_Y_WIDTH),                    // Y_WIDTH参数映射为C_Y_WIDTH
		.ID_WIDTH(C_ID_WIDTH)                   // ID_WIDTH参数映射为C_ID_WIDTH
	)u_lines(
		.clk(i_clk),                            // clk端口连接i_clk
		.rst_n(core_rst_n),                     // rst_n端口连接core_rst_n
		.cancel(abort_active_o),                // cancel端口连接abort_active_o
		.in_valid(i_in_valid && o_in_ready),    // in_valid端口连接i_in_valid && o_in_ready
		.in_ready(bank_ready),                  // in_ready端口连接bank_ready
		.in_task_id(i_in_task_id),              // in_task_id端口连接i_in_task_id
		.in_y(i_in_y),                          // in_y端口连接i_in_y
		.in_pixel(i_in_pixel),                  // in_pixel端口连接i_in_pixel
		.in_last(i_in_last),                    // in_last端口连接i_in_last
		.in_frame_last(i_in_frame_last),        // in_frame_last端口连接i_in_frame_last
		.out_valid(bank_valid),                 // out_valid端口连接bank_valid
		.out_ready(bank_take),                  // out_ready端口连接bank_take
		.out_task_id(bank_task),                // out_task_id端口连接bank_task
		.out_y(bank_y),                         // out_y端口连接bank_y
		.out_x(bank_x),                         // out_x端口连接bank_x
		.out_pixel(bank_pixel),                 // out_pixel端口连接bank_pixel
		.out_last(bank_last),                   // out_last端口连接bank_last
		.out_frame_last(bank_frame_last),       // out_frame_last端口连接bank_frame_last
		.empty(banks_empty_o),                  // empty端口连接banks_empty_o
		.protocol_error(bank_error)             // protocol_error端口连接bank_error
	);

	ccl_task_guard #(
		.ID_WIDTH(C_ID_WIDTH),                  // ID_WIDTH参数映射为C_ID_WIDTH
		.X_WIDTH(C_X_WIDTH),                    // X_WIDTH参数映射为C_X_WIDTH
		.Y_WIDTH(C_Y_WIDTH),                    // Y_WIDTH参数映射为C_Y_WIDTH
		.LABEL_WIDTH(C_LABEL_WIDTH),            // LABEL_WIDTH参数映射为C_LABEL_WIDTH
		.AREA_WIDTH(C_AREA_WIDTH)               // AREA_WIDTH参数映射为C_AREA_WIDTH
	)u_guard(
		.clk(i_clk),                            // clk端口连接i_clk
		.rst_n(i_rstn),                         // rst_n端口连接i_rstn
		.task_valid(accepted),                  // task_valid端口连接accepted
		.task_ready(guard_ready),               // task_ready端口连接guard_ready
		.task_id(i_task_id),                    // task_id端口连接i_task_id
		.task_frame_id(i_task_frame_id),        // task_frame_id端口连接i_task_frame_id
		.stream_event(event_valid),             // stream_event端口连接event_valid
		.stream_task_id(pixel_event ? bank_task : reg_line_task), // stream_task_id端口连接pixel_event ? bank_task : reg_line_task
		.stream_sof(1'b0),                      // stream_sof端口连接1'b0
		.core_stream_enable(guard_stream_enable), // core_stream_enable端口连接guard_stream_enable
		.core_frame_clear(guard_clear),         // core_frame_clear端口连接guard_clear
		.rejected_stream(guard_rejected),       // rejected_stream端口连接guard_rejected
		.core_obj_valid(core_obj_valid),        // core_obj_valid端口连接core_obj_valid
		.core_obj_index(core_index),            // core_obj_index端口连接core_index
		.core_obj_label(core_label),            // core_obj_label端口连接core_label
		.core_obj_xmin(core_xmin),              // core_obj_xmin端口连接core_xmin
		.core_obj_xmax(core_xmax),              // core_obj_xmax端口连接core_xmax
		.core_obj_ymin(core_ymin),              // core_obj_ymin端口连接core_ymin
		.core_obj_ymax(core_ymax),              // core_obj_ymax端口连接core_ymax
		.core_obj_center_x(core_center_x),      // core_obj_center_x端口连接core_center_x
		.core_obj_center_y(core_center_y),      // core_obj_center_y端口连接core_center_y
		.core_obj_area(core_area),              // core_obj_area端口连接core_area
		.core_object_count(cnt_core),           // core_object_count端口连接cnt_core
		.core_done(core_done),                  // core_done端口连接core_done
		.core_error_reason(error_reason),       // core_error_reason端口连接error_reason
		.cancel_valid(abort_now),               // cancel_valid端口连接abort_now
		.drain_done(drain_done),                // drain_done端口连接drain_done
		.abort_request(guard_abort),            // abort_request端口连接guard_abort
		.result_valid(guard_valid),             // result_valid端口连接guard_valid
		.result_ready(guard_release),           // result_ready端口连接guard_release
		.result_task_id(),                      // result_task_id端口预留连接
		.result_frame_id(),                     // result_frame_id端口预留连接
		.result_success(candidate_success_o),   // result_success端口连接candidate_success_o
		.result_cancelled(guard_cancelled),     // result_cancelled端口连接guard_cancelled
		.result_reason(candidate_reason_o),     // result_reason端口连接candidate_reason_o
		.result_object_count(cnt_candidate_o),  // result_object_count端口连接cnt_candidate_o
		.rd_index(reg_read_pending ? reg_pending_index : i_read_index), // rd_index端口连接reg_read_pending ? reg_pending_index : i_read_index
		.rd_valid(guard_rd_valid),              // rd_valid端口连接guard_rd_valid
		.rd_label(guard_label),                 // rd_label端口连接guard_label
		.rd_xmin(guard_xmin),                   // rd_xmin端口连接guard_xmin
		.rd_xmax(guard_xmax),                   // rd_xmax端口连接guard_xmax
		.rd_ymin(guard_ymin),                   // rd_ymin端口连接guard_ymin
		.rd_ymax(guard_ymax),                   // rd_ymax端口连接guard_ymax
		.rd_center_x(),                         // rd_center_x端口预留连接
		.rd_center_y(),                         // rd_center_y端口预留连接
		.rd_area(guard_area)                    // rd_area端口连接guard_area
	);

	ccl_rle_stream_core #(
		.X_WIDTH(C_X_WIDTH),                    // X_WIDTH参数映射为C_X_WIDTH
		.Y_WIDTH(C_Y_WIDTH),                    // Y_WIDTH参数映射为C_Y_WIDTH
		.LABEL_WIDTH(C_LABEL_WIDTH),            // LABEL_WIDTH参数映射为C_LABEL_WIDTH
		.AREA_WIDTH(C_AREA_WIDTH),              // AREA_WIDTH参数映射为C_AREA_WIDTH
		.LINE_WIDTH(C_WIDTH),                   // LINE_WIDTH参数映射为C_WIDTH
		.MAX_RUN(C_MAX_RUN),                    // MAX_RUN参数映射为C_MAX_RUN
		.MAX_LABEL(C_MAX_LABEL),                // MAX_LABEL参数映射为C_MAX_LABEL
		.MIN_AREA(C_MIN_AREA),                  // MIN_AREA参数映射为C_MIN_AREA
		.MIN_RUN_LENGTH(C_MIN_RUN_LENGTH)       // MIN_RUN_LENGTH参数映射为C_MIN_RUN_LENGTH
	)u_core(
		.clk(i_clk),                            // clk端口连接i_clk
		.rst_n(core_rst_n),                     // rst_n端口连接core_rst_n
		.analysis_valid(bank_take),             // analysis_valid端口连接bank_take
		.analysis_mask(bank_pixel),             // analysis_mask端口连接bank_pixel
		.analysis_x(bank_x),                    // analysis_x端口连接bank_x
		.analysis_y(bank_y),                    // analysis_y端口连接bank_y
		.analysis_sof(guard_clear),             // analysis_sof端口连接guard_clear
		.analysis_eol(eol_event && guard_stream_enable && !abort_now), // analysis_eol端口连接eol_event && guard_stream_enable && !abort_now
		.analysis_eof(eof_event && guard_stream_enable && !abort_now), // analysis_eof端口连接eof_event && guard_stream_enable && !abort_now
		.row_input_ready(core_ready),           // row_input_ready端口连接core_ready
		.row_input_commit(core_commit),         // row_input_commit端口连接core_commit
		.core_idle(core_idle),                  // core_idle端口连接core_idle
		.obj_valid(core_obj_valid),             // obj_valid端口连接core_obj_valid
		.obj_index(core_index),                 // obj_index端口连接core_index
		.obj_label(core_label),                 // obj_label端口连接core_label
		.obj_xmin(core_xmin),                   // obj_xmin端口连接core_xmin
		.obj_xmax(core_xmax),                   // obj_xmax端口连接core_xmax
		.obj_ymin(core_ymin),                   // obj_ymin端口连接core_ymin
		.obj_ymax(core_ymax),                   // obj_ymax端口连接core_ymax
		.obj_center_x(core_center_x),           // obj_center_x端口连接core_center_x
		.obj_center_y(core_center_y),           // obj_center_y端口连接core_center_y
		.obj_area(core_area),                   // obj_area端口连接core_area
		.object_count(cnt_core),                // object_count端口连接cnt_core
		.object_frame_done(core_done),          // object_frame_done端口连接core_done
		.row_done_debug(core_row_done),         // row_done_debug端口连接core_row_done
		.row_match_cycle_max(),                 // row_match_cycle_max端口预留连接
		.resolve_cycle_max(),                   // resolve_cycle_max端口预留连接
		.select_cycle_max(),                    // select_cycle_max端口预留连接
		.run_overflow(core_run_error),          // run_overflow端口连接core_run_error
		.label_overflow(core_label_error),      // label_overflow端口连接core_label_error
		.raw_overrun(core_raw_error),           // raw_overrun端口连接core_raw_error
		.labeled_overflow(core_labeled_error),  // labeled_overflow端口连接core_labeled_error
		.protocol_error(core_protocol_error),   // protocol_error端口连接core_protocol_error
		.ccl_error(core_error)                  // ccl_error端口连接core_error
	);

endmodule
