`timescale 1ns / 1ps

////////////////////////////////////English///////////////////////////////////////
// Company:         RoadYOLO
// Engineer:        Codex
// Create Date:     2026/10/16
// Design Name:     Complete visible frame dispatcher
// Module Name:     road_frame_ready_dispatch
// Description:     Pair two source identities with READY slots before claim/job
// Simulations:     verification/tb_road_frame_ready_dispatch.v
// Referrences:     dispatcher_spec.json
// Dependencies:    road_capture_slots; caller supplies synchronous reset release
// Version:         V1.0
// Revision Date:   2026/10/16
// History:
// Time             Version     Revised by        Contents
// 2026/10/16       V1.0        Codex             Create file
///////////////////////////////////Chinese////////////////////////////////////////
// 版权归属:        RoadYOLO
// 开发人员:        Codex
// 创建日期:        2026年10月16日
// 设计名称:        完整可见帧任务调度
// 模块名称:        road_frame_ready_dispatch
// 模块说明:        两条源身份与完整READY输入槽配对后才提交任务
// 仿真工程:        verification/tb_road_frame_ready_dispatch.v
// 参考资料:        dispatcher_spec.json
// 依赖文件:        road_capture_slots及调用方本域同步释放复位
// 当前版本:        V1.0
// 修订日期:        2026年10月16日
// 修订历史:
// 时间             版本        修订人            修订内容
// 2026年10月16日   V1.0        Codex             创建文件

module road_frame_ready_dispatch
(
	//---------------全局信号---------------//
	input i_clk,                            // 任务与槽控制共享的100MHz时钟
	input i_rstn,                           // 共同异步取消，本域由调用者同步释放
	//---------------用户接口---------------//
	input [31:0]i_epoch,                    // 本复位区间保持的源代次
	input [31:0]i_model_id,                 // 启动选择时锁定的模型配置
	input i_identity_valid,                 // 完整源身份跨域后有效
	input [127:0]i_identity_payload,        // 高32代次、中32源帧、低64采集毫秒
	input [1:0]i_slot_free_mask,            // 原槽管理器的真实FREE状态
	input [1:0]i_slot_ready_mask,           // 完整帧且写可见后的真实READY状态
	input [1:0]i_slot_reading_mask,         // 已claim输入的READING所有权
	input [1:0]i_slot_quarantine_mask,      // 不能再使用的隔离槽
	input [63:0]i_slot_epochs,              // slot0低半、slot1高半的代次
	input [63:0]i_slot_frame_ids,           // 两槽实际采集身份，不等于task
	input [127:0]i_slot_timestamps,         // 两槽内部诊断时间，不改源capture
	input i_claim_ready,                    // 原槽匹配预边沿READY后确认claim
	input i_job_ready,                      // 共享计算与publisher汇总启动许可
	input i_task_done,                      // 已接受任务的计算完成事件
	input [31:0]i_task_done_id,             // 完成事件所对应的task标识
	input i_last_read_valid,                // 最后输入返回已真正消费且允许复用
	input i_last_read_slot,                 // 最后读所对应的物理槽
	input [31:0]i_last_read_epoch,          // 返回所属的原采集代次
	input [31:0]i_last_read_frame_id,       // 返回所属的源帧，不使用task替代
	output o_identity_ready,                // 两上下文容量及身份诊断接受许可
	output o_claim_valid,                   // 先取得原槽READING所有权
	output o_claim_slot,                    // 冻结的输入槽索引
	output [31:0]o_claim_epoch,             // claim使用的源代次
	output [31:0]o_claim_frame_id,          // claim使用的源帧号
	output o_job_valid,                     // claim成功后保持至任务接受
	output [224:0]o_job_descriptor,         // 完整slot/base/epoch/task/frame/model/capture
	output o_job_timestamp_mismatch,        // 诊断时间差异，不拒绝或替换源时间
	output o_last_read_consumed,            // 仅匹配实际最后消费事实才释放输入
	output o_release_slot,                  // 释放原输入的槽索引
	output [31:0]o_release_epoch,           // 防止晚返回释放新代次
	output [31:0]o_release_frame_id,        // 防止晚返回释放新帧
	output o_busy,                          // 当前任务所有权，FAULT仍占用
	output o_error,                         // 错身份/错事件的粘滞诊断
	output o_task_wrap_fault                // 最后合法task后禁止再次claim
);
	//-------------状态参数区域-------------//
	// claim与job分拍，不把完成或事件ACK当释放。
	localparam [2:0] ST_IDLE = 3'd0;        // 等待身份和完整可见槽同时成立
	localparam [2:0] ST_CLAIM = 3'd1;       // 原槽读所有权握手阶段
	localparam [2:0] ST_JOB = 3'd2;         // 已拥有输入，保持计算任务描述符
	localparam [2:0] ST_RUN = 3'd3;         // 独立等待计算完成与最后读事实
	localparam [2:0] ST_FAULT = 3'd4;       // 已拥有槽遭违约改变，等共同复位

	//---------------计数信号---------------//
	// 饱和编号只在实际job握手后前进。
	reg [31:0]cnt_next_task = 1;            // 下一合法任务从一开始，不用源帧号

	//--------------状态机信号--------------//
	// 独立转移及状态寄存过程。
	reg [2:0]state_current = 0;             // 当前计算任务生命周期
	reg [2:0]state_next = 0;                // 下边沿进入的调度阶段

	//--------------寄存器信号--------------//
	// ponytail: 两槽各一份身份，旧任务占用时反压新身份，不扩队列。
	reg [127:0]reg_identity_low = 0;        // slot0源身份，保留至任务退休
	reg [127:0]reg_identity_high = 0;       // slot1源身份，保留至任务退休
	reg reg_slot = 0;                      // 选择后不变的当前物理槽
	reg reg_prefer_slot = 0;               // 两槽同时可用时交替优先
	reg [31:0]reg_task_id = 0;              // 当前任务编号，反压期间不变
	reg [31:0]reg_model_id = 0;             // 当前任务模型，不另存第三份身份
	reg reg_timestamp_mismatch = 0;        // 选择时记录槽诊断时间是否不同

	//---------------标志信号---------------//
	// 两条身份及独立退休事实。
	reg [1:0]flag_identity_valid = 0;       // 每槽小上下文是否被占用
	reg flag_task_done = 0;                // 已接受匹配task的完成事件
	reg flag_read_released = 0;            // 已转发一次合法最后读消费
	reg flag_error = 0;                    // 诊断不伪造释放，其他合法任务可继续
	reg flag_wrap = 0;                     // FFFFFFFF已接受，直到共同reset
	wire [1:0]flag_incoming_match;         // 非FREE非隔离槽与输入身份匹配
	wire flag_identity_bad;               // 错代次、无匹配或双槽歧义
	wire flag_identity_target;            // 恰一匹配身份的物理槽
	wire flag_identity_duplicate;         // 同epoch/frame已保存，不重写capture
	wire flag_identity_accept;            // 完整身份在本域真正接受
	wire flag_identity_store;             // 新且有空上下文才写身份寄存器
	wire [1:0]flag_eligible;               // 身份与READY同时成立的两个候选
	wire flag_select;                     // IDLE在未耗尽task时选择输入
	wire flag_selected_slot;              // 交替优先后的选择结果
	wire flag_selected_match;             // 当前上下文与原槽epoch/frame一致
	wire flag_preclaim_ok;                // 所有权取得前仍为READY且未被使用
	wire flag_owned_ok;                   // 取得后仍为本任务READING
	wire flag_owner_loss;                 // 未读完前槽所有权异常丢失
	wire flag_claim_accept;               // 原槽实际确认读所有权
	wire flag_job_accept;                 // 下游实际接下本任务
	wire flag_done_accept;                // 匹配且首次计算完成事件
	wire flag_last_accept;                // 匹配且首次最后输入消费事实
	wire flag_retire;                     // 两个预存事实都完成才退休
	wire [1:0]flag_purge;                  // 空闲时隔离槽对应小上下文作废
	wire flag_claim_lost;                 // claim未接受前槽已不再合格

	//---------------其他信号---------------//
	// 所有宽总线均来自同域冻结上下文，不进行新的CDC。
	wire [127:0]wire_incoming_context;     // 输入匹配槽当前存着的身份
	wire [127:0]wire_selected_context;     // 当前选中且有效的唯一身份
	wire [127:0]wire_choose_context;       // IDLE选择边沿使用的源时间
	wire [31:0]wire_slot_epoch;            // 当前原槽的代次快照
	wire [31:0]wire_slot_frame;            // 当前原槽的帧身份快照
	wire [63:0]wire_choose_timestamp;      // 选择边沿的内部诊断时间
	wire [31:0]wire_base;                  // 已冻结输入区两个512KiB槽地址

	//-------------其他信号连线-------------//
	// 身份错误消费并诊断；满上下文的新帧必须等待，不覆盖旧任务。
	assign flag_incoming_match[0] = !i_slot_free_mask[0] && !i_slot_quarantine_mask[0] && (i_identity_payload[127:96] == i_slot_epochs[31:0]) && (i_identity_payload[95:64] == i_slot_frame_ids[31:0]); // slot0实际分配身份匹配
	assign flag_incoming_match[1] = !i_slot_free_mask[1] && !i_slot_quarantine_mask[1] && (i_identity_payload[127:96] == i_slot_epochs[63:32]) && (i_identity_payload[95:64] == i_slot_frame_ids[63:32]); // slot1不受另一槽READY先后影响
	assign flag_identity_bad = (i_identity_payload[127:96] != i_epoch) || !(flag_incoming_match[0] ^ flag_incoming_match[1]); // 双槽同身份不能任选
	assign flag_identity_target = flag_identity_bad ? 1'b0 : flag_incoming_match[1]; // 错身份的索引没有写入权限
	assign wire_incoming_context = flag_identity_target ? reg_identity_high : reg_identity_low; // 只用于检出重复键
	assign flag_identity_duplicate = !flag_identity_bad && flag_identity_valid[flag_identity_target] && (wire_incoming_context[127:64] == i_identity_payload[127:64]); // capture变化也不能覆盖相同身份
	assign flag_identity_accept = i_identity_valid && o_identity_ready; // ACK只表示小身份已收下或诊断丢弃
	assign flag_identity_store = flag_identity_accept && !flag_identity_bad && !flag_identity_valid[flag_identity_target]; // 不以READY时间取代源capture
	assign flag_eligible[0] = flag_identity_valid[0] && i_slot_ready_mask[0] && !i_slot_free_mask[0] && !i_slot_reading_mask[0] && !i_slot_quarantine_mask[0] && (reg_identity_low[127:96] == i_slot_epochs[31:0]) && (reg_identity_low[95:64] == i_slot_frame_ids[31:0]); // slot0完整可见且身份仍一致
	assign flag_eligible[1] = flag_identity_valid[1] && i_slot_ready_mask[1] && !i_slot_free_mask[1] && !i_slot_reading_mask[1] && !i_slot_quarantine_mask[1] && (reg_identity_high[127:96] == i_slot_epochs[63:32]) && (reg_identity_high[95:64] == i_slot_frame_ids[63:32]); // slot1可以绕过未READY的slot0
	assign flag_select = i_rstn && (state_current == ST_IDLE) && !flag_wrap && (|flag_eligible); // task耗尽就不预占新槽
	assign flag_selected_slot = (&flag_eligible) ? reg_prefer_slot : flag_eligible[1]; // 双就绪时交替，其余选择真正就绪者
	assign wire_choose_context = flag_selected_slot ? reg_identity_high : reg_identity_low; // 不复制第三个源身份寄存器
	assign wire_choose_timestamp = flag_selected_slot ? i_slot_timestamps[127:64] : i_slot_timestamps[63:0]; // 只用于诊断差异
	assign wire_selected_context = !flag_identity_valid[reg_slot] ? 128'd0 : reg_slot ? reg_identity_high : reg_identity_low; // 无效上下文不暴露陈旧控制身份
	assign wire_slot_epoch = reg_slot ? i_slot_epochs[63:32] : i_slot_epochs[31:0]; // 所有权guard原槽代次
	assign wire_slot_frame = reg_slot ? i_slot_frame_ids[63:32] : i_slot_frame_ids[31:0]; // 所有权guard原槽帧号
	assign flag_selected_match = flag_identity_valid[reg_slot] && (wire_selected_context[127:96] == wire_slot_epoch) && (wire_selected_context[95:64] == wire_slot_frame); // claim后不能被重贴身份
	assign flag_preclaim_ok = flag_selected_match && i_slot_ready_mask[reg_slot] && !i_slot_free_mask[reg_slot] && !i_slot_reading_mask[reg_slot] && !i_slot_quarantine_mask[reg_slot]; // 未获得输入时只有READY可claim
	assign flag_owned_ok = flag_selected_match && i_slot_reading_mask[reg_slot] && !i_slot_free_mask[reg_slot] && !i_slot_quarantine_mask[reg_slot]; // 真实READING是最后读释放前提
	assign flag_owner_loss = ((state_current == ST_JOB) || ((state_current == ST_RUN) && !flag_read_released)) && !flag_owned_ok; // 真正读完后允许槽再捕获
	assign flag_claim_accept = o_claim_valid && i_claim_ready; // 不把请求发出当取得所有权
	assign flag_job_accept = o_job_valid && i_job_ready; // task计数只由此事件推进
	assign flag_done_accept = (state_current == ST_RUN) && i_task_done && (i_task_done_id == reg_task_id) && !flag_task_done; // 重复或早到完成不算退休事实
	assign flag_last_accept = i_rstn && (state_current == ST_RUN) && i_last_read_valid && !flag_read_released && flag_owned_ok && (i_last_read_slot == reg_slot) && (i_last_read_epoch == wire_selected_context[127:96]) && (i_last_read_frame_id == wire_selected_context[95:64]); // 无在途且最后返回已消费的匹配事件
	assign flag_retire = (state_current == ST_RUN) && flag_task_done && flag_read_released; // 两个事实已寄存后再清上下文
	assign flag_claim_lost = (state_current == ST_CLAIM) && !flag_preclaim_ok; // 未取得槽时作废小身份，不伪造FREE
	assign flag_purge = (state_current == ST_IDLE) ? (flag_identity_valid & i_slot_quarantine_mask) : 2'b00; // 隔离槽不会再等成READY
	assign wire_base = reg_slot ? 32'h03480000 : 32'h03400000; // 既有独立输入槽，不占视频bank

	//-------------输出信号连线-------------//
	// 用户接口
	assign o_identity_ready = i_rstn && (state_current != ST_FAULT) && (flag_identity_bad || flag_identity_duplicate || !flag_identity_valid[flag_identity_target]); // 旧任务占着目标上下文时持续反压
	assign o_claim_valid = i_rstn && (state_current == ST_CLAIM) && flag_preclaim_ok; // valid不等待ready才出现
	assign o_claim_slot = reg_slot;        // 槽选择贯穿claim/job/run
	assign o_claim_epoch = wire_selected_context[127:96]; // claim仅使用已接受源代次
	assign o_claim_frame_id = wire_selected_context[95:64]; // 原槽按帧身份检验claim
	assign o_job_valid = i_rstn && (state_current == ST_JOB) && flag_owned_ok; // 真实claim完成后才可以开工
	assign o_job_descriptor = {wire_selected_context[63:0], reg_model_id, wire_selected_context[95:64], reg_task_id, wire_selected_context[127:96], wire_base, reg_slot}; // 所有225位在job反压时稳定
	assign o_job_timestamp_mismatch = reg_timestamp_mismatch; // 时间差异只诊断，不拒绝合法身份
	assign o_last_read_consumed = flag_last_accept; // 不连接NNdone或结果copy_ack
	assign o_release_slot = reg_slot;      // 只释放当前任务原输入槽
	assign o_release_epoch = wire_selected_context[127:96]; // 晚返回不能释放其他代次
	assign o_release_frame_id = wire_selected_context[95:64]; // 已重捕获的新帧不受旧释放影响
	assign o_busy = i_rstn && (state_current != ST_IDLE); // 等待READY的context不表示计算已占用
	assign o_error = i_rstn && flag_error; // 诊断保持至共同reset但不自动释放槽
	assign o_task_wrap_fault = i_rstn && flag_wrap; // 编号耗尽后须新epoch/排空再复位

	//--------------状态机区域--------------//
	// 调用方负责同步释放，断言仍即时撤销所有接口许可。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			state_current <= ST_IDLE;           // 共同取消旧任务所有权
		end else begin
			state_current <= state_next;        // 原槽状态不由本过程修改
		end
	end

	// 所有权异常优先于job，正常完成等待两个独立事实。
	always@(*)begin
		state_next = state_current;            // 背压或未完成时保持阶段
		case(state_current)
			// IDLE仅从完整可见且身份配对的槽选择。
			ST_IDLE:begin
				if(flag_select == 1'b1)begin
					state_next = ST_CLAIM;          // 下一拍开始申请原槽
				end else begin
					state_next = ST_IDLE;           // 身份单独到达不能启动
				end
			end

			// claim还未接受时可以作废失效身份。
			ST_CLAIM:begin
				if(flag_claim_lost == 1'b1)begin
					state_next = ST_IDLE;           // 原槽保留其自身隔离/完成状态
				end else if(flag_claim_accept == 1'b1)begin
					state_next = ST_JOB;            // 槽已进入READING才给计算任务
				end else begin
					state_next = ST_CLAIM;          // claim载荷保持直到确认
				end
			end

			// JOB接受当拍不接收早到done或lastread。
			ST_JOB:begin
				if(flag_owner_loss == 1'b1)begin
					state_next = ST_FAULT;          // 不能使用已被违约改变的输入
				end else if(flag_job_accept == 1'b1)begin
					state_next = ST_RUN;            // 本边沿才算一次真实任务
				end else begin
					state_next = ST_JOB;            // valid及完整描述符不变
				end
			end

			// 最后读后槽可复用，但旧身份等计算完成才清。
			ST_RUN:begin
				if(flag_owner_loss == 1'b1)begin
					state_next = ST_FAULT;          // 保持占用等待协调reset/排空
				end else if(flag_retire == 1'b1)begin
					state_next = ST_IDLE;           // 下一任务不得跨越两个退休事实
				end else begin
					state_next = ST_RUN;            // NNdone单独到达不能FREE
				end
			end

			// 外部恢复槽标志也不能自动解除所有权故障。
			ST_FAULT:begin
				state_next = ST_FAULT;             // 只允许共同reset清故障
			end

			// 非法编码不允许产生新的输入读任务。
			default:begin
				state_next = ST_FAULT;             // 不把未知状态伪装空闲
			end
		endcase
	end

	//-----------状态任务处理区域-----------//
	// 两个valid位分别处理存入、隔离和当前任务退休。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_identity_valid <= 2'b00;       // 旧小身份共同取消
		end else begin
			if(flag_identity_store == 1'b1)begin
				flag_identity_valid[flag_identity_target] <= 1'b1; // 本边沿之后才可用于选择
			end
			if(flag_purge[0] || ((flag_retire || flag_claim_lost) && !reg_slot))begin
				flag_identity_valid[0] <= 1'b0; // 清slot0旧身份，不释放原存储槽
			end
			if(flag_purge[1] || ((flag_retire || flag_claim_lost) && reg_slot))begin
				flag_identity_valid[1] <= 1'b0; // 清slot1旧身份，不占第三上下文
			end
		end
	end

	// 源身份只写对应空上下文，直到退休不被新capture覆盖。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_identity_low <= 128'd0;         // slot0无有效身份
		end else if(flag_identity_store && !flag_identity_target)begin
			reg_identity_low <= i_identity_payload; // 保守源时间原样保留
		end
	end

	// slot1独立接收，不等待slot0先READY。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_identity_high <= 128'd0;        // slot1旧代次不泄漏
		end else if(flag_identity_store && flag_identity_target)begin
			reg_identity_high <= i_identity_payload; // 第二且唯一另一身份存储
		end
	end

	// 选择输入后其索引保持到当前任务退休。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_slot <= 1'b0;                   // 默认索引不授予输入权限
		end else if(flag_select)begin
			reg_slot <= flag_selected_slot;     // READY乱序时选实际可用者
		end
	end

	// 每次选择轮转，双槽就绪时不会永久偏向slot0。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_prefer_slot <= 1'b0;            // 初次同时就绪先slot0
		end else if(flag_select)begin
			reg_prefer_slot <= !flag_selected_slot; // 下次相同条件优先另一槽
		end
	end

	// task不是源帧编号，选择和等待都不推进计数。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_task_id <= 32'd0;               // 无任务时不产生完成匹配
		end else if(flag_select)begin
			reg_task_id <= cnt_next_task;       // JOB期间保持本编号
		end
	end

	// 模型配置随选择锁定，不随计算等待变化。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_model_id <= 32'd0;              // 无valid时零配置无消费语义
		end else if(flag_select)begin
			reg_model_id <= i_model_id;         // 此任务使用选中模型
		end
	end

	// 内部槽时间不同只诊断，不能把图显得更新。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_timestamp_mismatch <= 1'b0;     // 还没有时间差异观察
		end else if(flag_select)begin
			reg_timestamp_mismatch <= wire_choose_timestamp != wire_choose_context[63:0]; // 不覆盖job capture_ms
		end
	end

	// 编号耗尽不回卷，最后合法任务仍正常完成。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			cnt_next_task <= 32'd1;             // 新epoch排空后重建任务编号
		end else if(flag_job_accept && (cnt_next_task != 32'hffffffff))begin
			cnt_next_task <= cnt_next_task + 1'b1; // 唯一推进事件是实际job接受
		end
	end

	// 饱和许可独立于error，防止再claim无法启动的任务。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_wrap <= 1'b0;                  // 新代次共同复位才允许再使用编号
		end else if(flag_job_accept && (cnt_next_task == 32'hffffffff))begin
			flag_wrap <= 1'b1;                  // 最大编号只发送一次
		end
	end

	// 计算完成与输入释放分开记录，均不能相互代替。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_task_done <= 1'b0;             // 旧计算完成不进入新任务
		end else if(flag_select)begin
			flag_task_done <= 1'b0;             // 当前任务尚未收到完成
		end else if(flag_done_accept)begin
			flag_task_done <= 1'b1;             // 只锁匹配的RUN完成事件
		end
	end

	// 实际转发最后返回消费后才允许原槽FREE。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_read_released <= 1'b0;         // 旧输入消费事实失效
		end else if(flag_select)begin
			flag_read_released <= 1'b0;         // 新任务输入尚未退休
		end else if(flag_last_accept)begin
			flag_read_released <= 1'b1;         // 原槽可能重捕获，但本身份仍保留
		end
	end

	// 不吞掉错误事件，也绝不因此伪造FREE或重写正确身份。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			flag_error <= 1'b0;                 // 诊断由共同reset清除
		end else if((flag_identity_accept && (flag_identity_bad || flag_identity_duplicate)) || (i_task_done && !flag_done_accept) || (i_last_read_valid && !flag_last_accept) || flag_owner_loss || flag_claim_lost || (|flag_purge))begin
			flag_error <= 1'b1;                 // 合法其他任务不因诊断自动被释放
		end
	end
endmodule
