`timescale 1ns / 1ps

////////////////////////////////////English///////////////////////////////////////
// Company:         RoadYOLO project
// Engineer:        Codex
// Create Date:     2026/10/15
// Design Name:     Transactional result publisher
// Module Name:     road_result_publisher
// Description:     Direct FINAL97 stream with frozen SRIF1 context until copy ack
// Simulations:     verification/tb_road_result_publish_joint.v
// Referrences:     publisher_spec.json
// Dependencies:    road_detection_table_cdc
// Version:         V1.0
// Revision Date:   2026/10/15
// History:         2026/10/15 V1.0 Codex Create file
///////////////////////////////////Chinese////////////////////////////////////////
// 版权归属:        RoadYOLO project
// 开发人员:        Codex
// 创建日期:        2026年10月15日
// 设计名称:        完整检测表事务发布
// 模块名称:        road_result_publisher
// 模块说明:        框直接流入原表，仅冻结上下文与计数至复制确认
// 仿真工程:        verification/tb_road_result_publish_joint.v
// 参考资料:        publisher_spec.json
// 依赖文件:        road_detection_table_cdc
// 当前版本:        V1.0
// 修订日期:        2026年10月15日
// 修订历史:        2026年10月15日 V1.0 Codex 创建文件
module road_result_publisher
(
	//---------------全局信号---------------//
	input i_clk,                             // 所有发布事务的100MHz源时钟
	input i_rstn,                            // 与计算及表跨域共同取消的低有效复位
	//---------------用户接口---------------//
	input i_cancel,                          // 未封存任务的外部即时撤销
	input i_start_valid,                     // 描述符保持至启动接受
	input [31:0]i_start_epoch,                // 本次共同复位代次
	input [31:0]i_start_task_id,              // 锁存后成为计算链frame_token
	input [31:0]i_start_source_frame_id,      // 与物理源图关联的帧身份
	input [31:0]i_start_model_id,             // 对应当前数值模型的身份
	input [63:0]i_start_capture_ms,           // 描述符携带的同源采集时间
	input [63:0]i_now_ms,                     // 唯一源时基当前毫秒数
	input i_pipeline_start_ready,            // 原计算链空闲启动许可
	input i_entry_valid,                     // NMS当前输出框有效
	input [96:0]i_entry,                      // 不经新增缓存的完整框载荷
	input [31:0]i_result_frame_token,         // NMS当前事务身份
	input [6:0]i_result_count,                // NMS已接受输出的总数
	input i_result_done,                     // 晚于最后框接受的完成脉冲
	input i_pipeline_fault,                  // 上游计算或ROM服务故障聚合
	input i_table_entry_ready,               // 原source表可接受一个框
	input i_table_meta_ready,                // 原source表可封存一致元数据
	input i_table_copy_ack,                  // 完整复制完成的本源域确认
	input i_table_busy,                      // source表部分占用或已封存
	input i_table_error,                     // 原框表源端协议错误脉冲
	output o_start_ready,                    // 描述符与计算链原子接受许可
	output o_pipeline_start_valid,           // 不等待计算链ready的启动有效
	output [31:0]o_pipeline_frame_token,      // 启动时task，忙时锁定task
	output [31:0]o_pipeline_model_id,         // 计算链使用的锁定模型号
	output o_pipeline_cancel,                // 未提交取消或ABORT状态脉冲
	output o_entry_ready,                    // 原source背压直接回传NMS
	output o_table_entry_valid,              // 身份正确且未满表的输出有效
	output [96:0]o_table_entry,               // 原NMS数据的直接连线
	output o_table_meta_valid,               // 完成后单独一拍起保持至接受
	output [264:0]o_table_metadata,           // 冻结的完整SRIF1描述符
	output o_table_abort,                    // 封存前清部分表，提交后恒零
	output o_busy,                           // 从启动至复制确认的任务占用
	output o_error                           // ABORT状态持续一源周期
);
	//-------------状态参数区域-------------//
	// 单任务发布阶段，提交之后不撤回。
	localparam [2:0] ST_IDLE = 3'd0;          // source空闲时等待描述符
	localparam [2:0] ST_RUN = 3'd1;           // 计算及框直接转发阶段
	localparam [2:0] ST_META = 3'd2;          // 元数据冻结等待表接受
	localparam [2:0] ST_WAIT_ACK = 3'd3;      // 已提交，等待完整复制确认
	localparam [2:0] ST_ABORT = 3'd4;         // 清理部分表及原流水一拍

	//---------------计数信号---------------//
	// 计数含64终值，不使用六位回绕。
	reg [6:0]cnt_entry = 0;                  // 实际source框握手数量

	//--------------状态机信号--------------//
	// 状态寄存和组合下一状态由独立过程驱动。
	reg [2:0]state_current = 0;              // 本拍持有表所有权的阶段
	reg [2:0]state_next = 0;                 // 边沿后的发布阶段

	//--------------寄存器信号--------------//
	// 仅上下文存储，没有FINAL97数组。
	reg [264:0]reg_metadata = 0;             // 采集上下文及成功完成时间
	(* ASYNC_REG = "TRUE" *) reg [1:0]reg_release = 0; // 共同复位后的两级本域许可

	//---------------标志信号---------------//
	// 启动与未封存错误译码不改变数值计算。
	wire flag_released;                     // 两个源时钟后才开放接口
	wire flag_common_failure;               // 当前外部取消或服务错误
	wire flag_token_error;                  // 当前结果不属于锁定任务
	wire flag_entry_error;                  // 第65项或错误身份禁止写表
	wire flag_done_error;                   // 完成脉冲违反数量或时间顺序
	wire flag_run_failure;                  // RUN当前拍必须撤销的条件
	wire flag_meta_failure;                 // META提交前更高优先级错误
	wire flag_preseal_failure;              // 只作用于未提交事务的撤销
	wire flag_start_allowed;                // 除计算链ready外的启动条件
	wire flag_start_accept;                 // 双方同拍锁存描述符
	wire flag_forward;                      // 当前框可参与端到端握手
	wire flag_entry_accept;                 // NMS和source都实际接受此框
	wire flag_meta_accept;                  // source冻结表的提交边沿

	//-------------其他信号连线-------------//
	// 即时撤销只门控本任务；故障取消经ABORT寄存，避免反馈回路。
	assign flag_released = i_rstn && reg_release[1]; // 原始复位仍可即时关闭端口
	assign flag_common_failure = i_cancel || i_pipeline_fault || i_table_error; // 未提交错误汇总
	assign flag_token_error = i_result_frame_token != reg_metadata[63:32]; // 身份与锁存task逐位比较
	assign flag_entry_error = i_entry_valid && (flag_token_error || (cnt_entry >= 7'd64)); // 满表继续valid即失败
	assign flag_done_error = i_result_done && (i_entry_valid || flag_token_error || (i_result_count != cnt_entry) || (cnt_entry > 7'd64) || (i_now_ms < reg_metadata[200:137])); // done不得掩盖最后框或倒序时间
	assign flag_run_failure = flag_common_failure || flag_entry_error || flag_done_error; // 失败优先于框握手及完成
	assign flag_meta_failure = flag_common_failure || i_entry_valid; // 提交拍不得出现额外框
	assign flag_preseal_failure = ((state_current == ST_RUN) && flag_run_failure) || ((state_current == ST_META) && flag_meta_failure); // 已提交状态不参加撤销
	assign flag_start_allowed = flag_released && (state_current == ST_IDLE) && !flag_common_failure && !i_table_busy && i_table_entry_ready; // 计算中空表不代表发布器空闲
	assign flag_start_accept = flag_start_allowed && i_start_valid && i_pipeline_start_ready; // 只在ready与valid同时成立时冻结
	assign flag_forward = flag_released && (state_current == ST_RUN) && !flag_run_failure; // 不让坏框部分进入source表
	assign flag_entry_accept = flag_forward && i_entry_valid && i_table_entry_ready; // 端到端一致的框计数事件
	assign flag_meta_accept = flag_released && (state_current == ST_META) && !flag_meta_failure && i_table_meta_ready; // 撤销比封存具有更高优先级

	//-------------输出信号连线-------------//
	// 数据直接传递，valid控制所有权和复位取消。
	assign o_start_ready = flag_start_allowed && i_pipeline_start_ready; // 上游仅在计算链也接受时退休描述符
	assign o_pipeline_start_valid = flag_start_allowed && i_start_valid; // 不以ready作为valid的前提
	assign o_pipeline_frame_token = (state_current == ST_IDLE) ? i_start_task_id : reg_metadata[63:32]; // busy期间外部描述符变化不影响原任务
	assign o_pipeline_model_id = (state_current == ST_IDLE) ? i_start_model_id : reg_metadata[127:96]; // 模型身份随上下文冻结
	assign o_pipeline_cancel = flag_released && ((state_current == ST_ABORT) || (i_cancel && (state_current != ST_WAIT_ACK))); // fault不组合回馈NMS的cancel门
	assign o_entry_ready = flag_forward && i_table_entry_ready; // source反压逐拍传回原输出
	assign o_table_entry_valid = flag_forward && i_entry_valid; // 正常框有效不依赖ready
	assign o_table_entry = i_entry;          // 不添加任何框存储或延迟
	assign o_table_meta_valid = flag_released && (state_current == ST_META) && !flag_meta_failure; // 等ready期间完整描述符保持
	assign o_table_metadata = reg_metadata; // 元数据没有动态now旁路
	assign o_table_abort = flag_released && ((state_current == ST_ABORT) || flag_preseal_failure); // 当拍阻止半表继续写入
	assign o_busy = flag_released && (state_current != ST_IDLE); // copy_ack之前保持任务独占
	assign o_error = flag_released && (state_current == ST_ABORT); // 失败通知单拍而非虚构成功空表

	//--------------状态机区域--------------//
	// 共同复位立即取消状态，释放许可前保持空闲。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			state_current <= ST_IDLE;           // 丢弃任何旧发布所有权
		end else if(flag_released == 1'b0)begin
			state_current <= ST_IDLE;           // 复位释放期间不接受新事务
		end else begin
			state_current <= state_next;        // 只由组合转移结果更新
		end
	end

	// 完成、封存、复制确认分别占有独立阶段。
	always@(*)begin
		state_next = state_current;            // 没有事件时保持当前所有权
		case(state_current)
			// 空闲时仅原子启动握手推进。
			ST_IDLE:begin
				if(flag_start_accept == 1'b1)begin
					state_next = ST_RUN;            // 锁上下文并交给计算链
				end else begin
					state_next = ST_IDLE;           // 无许可不消耗描述符
				end
			end

			// 结果错误优先，合法完成后才允许提交。
			ST_RUN:begin
				if(flag_run_failure == 1'b1)begin
					state_next = ST_ABORT;          // 用下一拍取消上游，避开组合反馈
				end else if(i_result_done == 1'b1)begin
					state_next = ST_META;           // 完成时间锁定后再发metadata
				end else begin
					state_next = ST_RUN;            // 继续直接转发或等待计算
				end
			end

			// 同拍错误禁止source接受metadata。
			ST_META:begin
				if(flag_meta_failure == 1'b1)begin
					state_next = ST_ABORT;          // 部分表尚可安全撤销
				end else if(flag_meta_accept == 1'b1)begin
					state_next = ST_WAIT_ACK;       // 进入不可撤回的提交阶段
				end else begin
					state_next = ST_META;           // 全部265位等待ready保持
				end
			end

			// seal之后外部cancel和迟到故障不能提前释放。
			ST_WAIT_ACK:begin
				if(i_table_copy_ack == 1'b1)begin
					state_next = ST_IDLE;           // 完整复制确认才允许下一任务
				end else begin
					state_next = ST_WAIT_ACK;       // 不用NMS done替代copy_ack
				end
			end

			// 清部分source并取消流水保持一完整源周期。
			ST_ABORT:begin
				state_next = ST_IDLE;              // 已接受ROM读仍由原服务排空
			end

			// 非法状态不发布表，先走清理阶段。
			default:begin
				state_next = ST_ABORT;             // 不让未知状态伪装成功完成
			end
		endcase
	end

	//-----------状态任务处理区域-----------//
	// 一个计数器对应source实际接受，最高合法值为64。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			cnt_entry <= 7'd0;                  // 共同复位丢弃旧框计数
		end else if((state_current == ST_ABORT) || flag_start_accept || ((state_current == ST_WAIT_ACK) && i_table_copy_ack))begin
			cnt_entry <= 7'd0;                  // 撤销或正常退休后释放数量状态
		end else if(flag_entry_accept == 1'b1)begin
			cnt_entry <= cnt_entry + 7'd1;       // 饱满64后不会再握手回绕
		end
	end

	// 仅启动和合法done改上下文，metadata反压及复制期间完全冻结。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_metadata <= 265'd0;             // 无valid时复位载荷不表示成功表
		end else if(flag_start_accept == 1'b1)begin
			reg_metadata <= {64'd0, i_start_capture_ms, 2'd0, 7'd0, i_start_model_id, i_start_source_frame_id, i_start_task_id, i_start_epoch}; // 成功状态保留，完成时间尚未产生
		end else if((state_current == ST_RUN) && !flag_run_failure && i_result_done)begin
			reg_metadata <= {i_now_ms, reg_metadata[200:135], cnt_entry, reg_metadata[127:0]}; // 写入实际完成时刻及已接受数量
		end
	end

	//-----------主要任务处理区域-----------//
	// ponytail: 单任务直到copy_ack，不添加多任务队列；需要实测收益后再扩展。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_release <= 2'b00;               // 异步断言立即撤销接口许可
		end else begin
			reg_release <= {reg_release[0], 1'b1}; // 首级只传播到本地第二级
		end
	end
endmodule
