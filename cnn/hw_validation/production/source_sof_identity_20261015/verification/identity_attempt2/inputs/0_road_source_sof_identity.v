`timescale 1ns / 1ps
////////////////////////////////////////////////////////////////////////////////
// Company: RoadYOLO
// Engineer: Codex
// Create Date: 2026-10-15
// Design Name: Source SOF identity
// Module Name: road_source_sof_identity
// Description: Held source identity and external time mirror
// Simulations: ../tests/tb_road_source_sof_identity.v
// Referrences: ../specifications/road_source_sof_identity.json
// Dependencies: external road_time_snapshot counter
// Version: V1.0
// Revision Date: 2026-10-15
// History: V1.0 initial implementation
// 版权归属: RoadYOLO
// 开发人员: Codex
// 创建日期: 2026-10-15
// 设计名称: 源帧身份与时间镜像
// 模块名称: road_source_sof_identity
// 模块说明: AWB重建帧标记与已完成时间镜像的保持总线传递
// 仿真工程: ../tests/tb_road_source_sof_identity.v
// 参考资料: ../specifications/road_source_sof_identity.json
// 依赖文件: 外部road_time_snapshot唯一绝对计时器
// 当前版本: V1.0
// 修订日期: 2026-10-15
// 修订历史: V1.0 首次实现
////////////////////////////////////////////////////////////////////////////////
module road_source_sof_identity
#(
	parameter MIRROR_TIMEOUT_CYCLES = 120000 // 摄像头边沿失联上限，不构成第二个绝对计时器
)
(
	//---------------全局信号---------------//
	input i_time_clk,                       // 唯一绝对时间来源所属时钟
	input i_camera_clk,                     // AWB重建帧标记的采样时钟
	input i_rstn,                           // 两端共同异步取消，低有效
	//---------------用户接口---------------//
	input [63:0]i_time_now_ms,               // 外部单计时器已完成毫秒值
	input i_time_tick,                      // 时间源允许发布快照的节拍
	input [31:0]i_time_epoch,                // 共同复位间保持不变的身份代号
	input i_camera_sof,                     // AWB标记，不证明CSI包或曝光对应
	input i_capture_credit,                 // 同域既有FREE槽所有者授予接纳
	input i_desc_ready,                     // 时间域消费者本拍真实接受描述符
	output o_frame_admit,                   // SOF采样前有效，供同拍像素所有者使用
	output [31:0]o_admit_epoch,              // 接纳限定时使用旧镜像的代号
	output [31:0]o_admit_frame_id,           // 当前物理AWB计数加一的候选身份
	output [63:0]o_admit_capture_ms,         // 接纳限定时使用旧镜像的捕获毫秒
	output [31:0]o_source_frame_id,          // 含跳帧在内的已观察AWB上升沿计数
	output [63:0]o_mirror_ms,                // 摄像头域最后完整复制的毫秒镜像
	output [31:0]o_mirror_epoch,             // 与镜像毫秒原子复制的代号
	output o_mirror_valid,                  // 已有完整镜像且未失联过期
	output o_event_busy,                    // 源事件尚未收到真实消费的回执
	output o_frame_skip,                    // 每个未接纳AWB上升沿产生寄存脉冲
	output o_wrap_fault,                    // 帧号饱和后再来SOF产生粘滞故障
	output o_desc_valid,                    // 时间域描述符完整且等待消费
	output [127:0]o_desc_payload             // 原子排列为代号、AWB帧号、捕获毫秒
);
	//---------------计数信号---------------//
	//镜像失联边沿累计
	reg [31:0]cnt_mirror_silence = 0;        // 达到上限后饱和，避免过期后重新有效

	//--------------寄存器信号--------------//
	//异步取消与本地释放
	(* ASYNC_REG = "TRUE" *) reg [1:0]reg_time_release = 0; // 时间域复位释放的两级移位
	(* ASYNC_REG = "TRUE" *) reg [1:0]reg_camera_release = 0; // 摄像头域复位释放的两级移位

	//保持总线与控制同步链
	reg [95:0]reg_time_payload = 0;         // 发布后保持到镜像完成回执返回
	reg [127:0]reg_event_payload = 0;       // 接纳边沿冻结，消费回执返回前不改写
	(* ASYNC_REG = "TRUE" *) reg [1:0]reg_time_request_sync = 0; // 时间请求进入摄像头域的两级同步
	(* ASYNC_REG = "TRUE" *) reg [1:0]reg_time_acknowledge_sync = 0; // 镜像完成回执进入时间域的两级同步
	(* ASYNC_REG = "TRUE" *) reg [1:0]reg_event_request_sync = 0; // 接纳事件请求进入时间域的两级同步
	(* ASYNC_REG = "TRUE" *) reg [1:0]reg_event_acknowledge_sync = 0; // 消费回执进入摄像头域的两级同步
	reg reg_previous_sof = 0;              // 去除持续高电平的重复帧边沿

	//---------------标志信号---------------//
	//独立的双向保持总线控制
	reg flag_time_request = 0;             // 时间端每次冻结快照后翻转
	reg flag_time_acknowledge = 0;         // 摄像头完成实际镜像复制后应答
	reg flag_time_capture_wait = 0;        // 请求检测后额外等待一个摄像头边沿
	reg flag_event_request = 0;            // 摄像头真正接纳一帧后翻转
	reg flag_event_acknowledge = 0;        // 描述符valid和ready同拍才应答
	reg flag_event_capture_wait = 0;       // 接纳请求检测后额外等待一个时间边沿
	reg flag_sof_armed = 0;                // 释放后观察过低电平才允许计数

	//---------------其他信号---------------//
	//本地复位与接纳条件
	wire time_rstn;                        // 共同异步取消、时间域同步释放
	wire camera_rstn;                      // 共同异步取消、摄像头域同步释放
	wire flag_source_edge;                 // 已武装AWB低到高边沿的当前资格
	wire flag_event_busy;                  // 接纳请求与返回回执尚未相等
	wire flag_frame_admit;                 // 外部槽信用与旧镜像共同限定接纳
	wire [31:0]reg_candidate_frame_id;      // 饱和计数的下一个候选，不允许回卷

	//---------------输出信号---------------//
	//摄像头端可观察状态
	reg [31:0]source_frame_id_o = 0;        // 已观察帧数在最大身份处保持
	reg [63:0]mirror_ms_o = 0;             // 完整快照的低位绝对时间
	reg [31:0]mirror_epoch_o = 0;           // 同一快照的高位复位代号
	reg mirror_valid_o = 0;                // 完成镜像建立，失联后清除
	reg frame_skip_o = 0;                  // 未接纳帧事件的单周期记录
	reg wrap_fault_o = 0;                  // 饱和后的再次帧边沿只能共同复位清除

	//时间端消费状态
	reg desc_valid_o = 0;                  // 整份描述符保持直到消费者接受
	reg [127:0]desc_payload_o = 0;         // 背压期间冻结的完整接纳身份

	//-------------其他信号连线-------------//
	assign time_rstn = reg_time_release[1]; // 第二级释放位驱动时间端本地复位
	assign camera_rstn = reg_camera_release[1]; // 第二级释放位驱动摄像头端本地复位
	assign flag_source_edge = i_camera_sof && !reg_previous_sof && flag_sof_armed; // 仅已见低电平后的上升沿代表一帧
	assign flag_event_busy = flag_event_request != reg_event_acknowledge_sync[1]; // 回执同步完成前持续占用事件通道
	assign reg_candidate_frame_id = source_frame_id_o == 32'hffffffff ? 32'hffffffff : source_frame_id_o + 1'b1; // 最大身份不回卷到零
	assign flag_frame_admit = camera_rstn && flag_source_edge && i_capture_credit && mirror_valid_o && !flag_event_busy && !wrap_fault_o && source_frame_id_o != 32'hffffffff; // 本边沿仅消费已存在的镜像与返回回执

	//-------------输出信号连线-------------//
	assign o_frame_admit = flag_frame_admit; // 对外接纳在SOF边沿前完成组合判定
	assign o_admit_epoch = mirror_epoch_o; // 接纳时读取镜像原子的复位代号
	assign o_admit_frame_id = reg_candidate_frame_id; // 接纳时预约下一AWB观察身份
	assign o_admit_capture_ms = mirror_ms_o; // 本边沿新镜像不会改变已采样旧时间
	assign o_source_frame_id = source_frame_id_o; // 导出含被拒帧的累计物理标记
	assign o_mirror_ms = mirror_ms_o;       // 导出摄像头侧完整毫秒副本
	assign o_mirror_epoch = mirror_epoch_o; // 导出镜像随附的共同复位代号
	assign o_mirror_valid = mirror_valid_o; // 导出已完成且未失联的资格
	assign o_event_busy = flag_event_busy; // 供槽所有者观察描述符占用窗口
	assign o_frame_skip = frame_skip_o;     // 导出刚刚拒绝的一整帧事件
	assign o_wrap_fault = wrap_fault_o;     // 导出需共同复位恢复的身份耗尽故障
	assign o_desc_valid = desc_valid_o;     // 消费者必须同时给ready才算传输
	assign o_desc_payload = desc_payload_o; // 输出完整且可在背压时保持的描述符

	//-----------输出信号处理区域-----------//
	//每个已武装上升沿递增，跳帧也消耗物理AWB身份
	always@(posedge i_camera_clk or negedge camera_rstn)begin
		if(camera_rstn == 1'b0)begin
			source_frame_id_o <= 0;        // 新共同复位区间从零开始编号
		end else if(flag_source_edge && source_frame_id_o != 32'hffffffff)begin
			source_frame_id_o <= source_frame_id_o + 1'b1; // 最后合法身份只到最大值一次
		end
	end

	//镜像毫秒仅在额外等待完成后整份采样
	always@(posedge i_camera_clk or negedge camera_rstn)begin
		if(camera_rstn == 1'b0)begin
			mirror_ms_o <= 0;              // 未建立时间镜像时数值不授予资格
		end else if(flag_time_capture_wait)begin
			mirror_ms_o <= reg_time_payload[63:0]; // 源端保持总线已经历同步与等待
		end
	end

	//代号使用与毫秒相同的复制条件以保持原子关联
	always@(posedge i_camera_clk or negedge camera_rstn)begin
		if(camera_rstn == 1'b0)begin
			mirror_epoch_o <= 0;           // 取消前一区间的镜像身份
		end else if(flag_time_capture_wait)begin
			mirror_epoch_o <= reg_time_payload[95:64]; // 同拍复制快照高位代号
		end
	end

	//有效镜像持续到第上限加一条未更新边沿
	always@(posedge i_camera_clk or negedge camera_rstn)begin
		if(camera_rstn == 1'b0)begin
			mirror_valid_o <= 0;           // 上电或取消后没有可用时间
		end else if(flag_time_capture_wait)begin
			mirror_valid_o <= 1'b1;        // 实际复制完成才建立有效资格
		end else if(cnt_mirror_silence == MIRROR_TIMEOUT_CYCLES)begin
			mirror_valid_o <= 1'b0;        // 第120001条无更新边沿使资格过期
		end
	end

	//拒绝脉冲与刚刚采样的帧边沿对应
	always@(posedge i_camera_clk or negedge camera_rstn)begin
		if(camera_rstn == 1'b0)begin
			frame_skip_o <= 0;             // 共同取消不制造一帧拒绝事件
		end else begin
			frame_skip_o <= flag_source_edge && !flag_frame_admit; // 任一资格不足均跳过整帧
		end
	end

	//最大身份之后再次观察帧边沿锁定故障
	always@(posedge i_camera_clk or negedge camera_rstn)begin
		if(camera_rstn == 1'b0)begin
			wrap_fault_o <= 0;             // 新代号共同复位后才允许重新开始
		end else if(flag_source_edge && source_frame_id_o == 32'hffffffff)begin
			wrap_fault_o <= 1'b1;          // 不生成与旧区间重复的身份零
		end
	end

	//有效描述符只能由真实消费清除，等待拍不提前传输
	always@(posedge i_time_clk or negedge time_rstn)begin
		if(time_rstn == 1'b0)begin
			desc_valid_o <= 0;             // 取消所有未消费的旧事件
		end else if(desc_valid_o && i_desc_ready)begin
			desc_valid_o <= 1'b0;          // 消费者本边沿已经接受完整描述符
		end else if(flag_event_capture_wait)begin
			desc_valid_o <= 1'b1;          // 拷贝完成后下一个边沿才可消费
		end
	end

	//消费者背压时载荷保持，未确认前不会捕获第二份
	always@(posedge i_time_clk or negedge time_rstn)begin
		if(time_rstn == 1'b0)begin
			desc_payload_o <= 0;           // 移除上一共同复位区间的输出载荷
		end else if(flag_event_capture_wait)begin
			desc_payload_o <= reg_event_payload; // 整个128位保持总线同拍复制
		end
	end

	//-----------主要任务处理区域-----------//
	//原始共同复位异步拉低，释放需两个时间边沿
	always@(posedge i_time_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_time_release <= 0;         // 立即取消时间域释放状态
		end else begin
			reg_time_release <= {reg_time_release[0],1'b1}; // 释放链仅移入已解除的复位
		end
	end

	//摄像头停钟期间保持取消，恢复后独立同步释放
	always@(posedge i_camera_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_camera_release <= 0;       // 立即取消摄像头域所有旧资格
		end else begin
			reg_camera_release <= {reg_camera_release[0],1'b1}; // 同域第二级用于安全解除
		end
	end

	//时间源只在通道空闲且节拍到来时冻结外部绝对计数
	always@(posedge i_time_clk or negedge time_rstn)begin
		if(time_rstn == 1'b0)begin
			reg_time_payload <= 0;         // 取消尚未完成镜像的旧时间载荷
		end else if(i_time_tick && flag_time_request == reg_time_acknowledge_sync[1])begin
			reg_time_payload <= {i_time_epoch,i_time_now_ms}; // 接纳外部唯一计时器原子输入
		end
	end

	//冻结时间载荷与翻转请求使用相同的源端条件
	always@(posedge i_time_clk or negedge time_rstn)begin
		if(time_rstn == 1'b0)begin
			flag_time_request <= 0;        // 双端共同取消时请求基准一致
		end else if(i_time_tick && flag_time_request == reg_time_acknowledge_sync[1])begin
			flag_time_request <= !flag_time_request; // 新快照仅发布一次翻转
		end
	end

	//镜像回执只同步控制位，保持总线不逐位同步
	always@(posedge i_time_clk or negedge time_rstn)begin
		if(time_rstn == 1'b0)begin
			reg_time_acknowledge_sync <= 0; // 清除跨区间的镜像完成回执
		end else begin
			reg_time_acknowledge_sync <= {reg_time_acknowledge_sync[0],flag_time_acknowledge}; // 两级回程限定源端复用
		end
	end

	//时间请求经过两个摄像头寄存级后才用于检测
	always@(posedge i_camera_clk or negedge camera_rstn)begin
		if(camera_rstn == 1'b0)begin
			reg_time_request_sync <= 0;    // 不把复位前的请求误作新镜像
		end else begin
			reg_time_request_sync <= {reg_time_request_sync[0],flag_time_request}; // 同步翻转而非宽总线
		end
	end

	//检测请求后保留一条额外目的边沿用于总线稳定
	always@(posedge i_camera_clk or negedge camera_rstn)begin
		if(camera_rstn == 1'b0)begin
			flag_time_capture_wait <= 0;   // 取消未完成的镜像复制等待
		end else if(flag_time_capture_wait)begin
			flag_time_capture_wait <= 1'b0; // 本边沿复制完成后离开等待
		end else if(reg_time_request_sync[1] != flag_time_acknowledge)begin
			flag_time_capture_wait <= 1'b1; // 检测到新翻转但本拍不取载荷
		end
	end

	//镜像真正复制完成的同拍才应答时间源
	always@(posedge i_camera_clk or negedge camera_rstn)begin
		if(camera_rstn == 1'b0)begin
			flag_time_acknowledge <= 0;    // 统一回执翻转的初始值
		end else if(flag_time_capture_wait)begin
			flag_time_acknowledge <= reg_time_request_sync[1]; // 应答已复制的完整快照
		end
	end

	//失联看门狗只累计摄像头边沿，不替代绝对时间
	always@(posedge i_camera_clk or negedge camera_rstn)begin
		if(camera_rstn == 1'b0)begin
			cnt_mirror_silence <= 0;       // 清空前一代号的失联累计
		end else if(flag_time_capture_wait)begin
			cnt_mirror_silence <= 0;       // 完整镜像更新重新开始边沿计龄
		end else if(cnt_mirror_silence != MIRROR_TIMEOUT_CYCLES)begin
			cnt_mirror_silence <= cnt_mirror_silence + 1'b1; // 达到阈值后饱和不回卷
		end
	end

	//帧边沿历史每拍采样，与是否接纳无关
	always@(posedge i_camera_clk or negedge camera_rstn)begin
		if(camera_rstn == 1'b0)begin
			reg_previous_sof <= 0;         // 高电平复位由武装位抑制幻帧
		end else begin
			reg_previous_sof <= i_camera_sof; // 下一拍比较真实AWB标记变化
		end
	end

	//只在本地释放后实际看到低电平才武装观察
	always@(posedge i_camera_clk or negedge camera_rstn)begin
		if(camera_rstn == 1'b0)begin
			flag_sof_armed <= 0;           // 上电时持续高的SOF没有观察资格
		end else if(!i_camera_sof)begin
			flag_sof_armed <= 1'b1;        // 此后每次低到高均计入物理身份
		end
	end

	//接纳载荷只在真实SOF同拍冻结，返回ACK之前绝不覆盖
	always@(posedge i_camera_clk or negedge camera_rstn)begin
		if(camera_rstn == 1'b0)begin
			reg_event_payload <= 0;        // 丢弃共同复位前的未完成事件
		end else if(flag_frame_admit)begin
			reg_event_payload <= {mirror_epoch_o,reg_candidate_frame_id,mirror_ms_o}; // 同拍新时间镜像不能进入此描述符
		end
	end

	//翻转请求与实际帧接纳保持同一个条件
	always@(posedge i_camera_clk or negedge camera_rstn)begin
		if(camera_rstn == 1'b0)begin
			flag_event_request <= 0;       // 取消帧事件通道的旧请求
		end else if(flag_frame_admit)begin
			flag_event_request <= !flag_event_request; // 一帧只发布一份冻结身份
		end
	end

	//消费者ACK返回两级摄像头同步，直到完成都保持busy
	always@(posedge i_camera_clk or negedge camera_rstn)begin
		if(camera_rstn == 1'b0)begin
			reg_event_acknowledge_sync <= 0; // 共同取消后不保留旧消费完成位
		end else begin
			reg_event_acknowledge_sync <= {reg_event_acknowledge_sync[0],flag_event_acknowledge}; // 回程第二级解除事件占用
		end
	end

	//时间端仅同步事件翻转，原子载荷由等待拍保护
	always@(posedge i_time_clk or negedge time_rstn)begin
		if(time_rstn == 1'b0)begin
			reg_event_request_sync <= 0;   // 未完成请求由共同复位作废
		end else begin
			reg_event_request_sync <= {reg_event_request_sync[0],flag_event_request}; // 两级请求同步后再检测
		end
	end

	//有新事件且输出空闲时进入一条目的稳定等待
	always@(posedge i_time_clk or negedge time_rstn)begin
		if(time_rstn == 1'b0)begin
			flag_event_capture_wait <= 0;  // 不在新代号区间复制旧事件
		end else if(flag_event_capture_wait)begin
			flag_event_capture_wait <= 1'b0; // 本边沿完整拷贝后结束等待
		end else if(!desc_valid_o && reg_event_request_sync[1] != flag_event_acknowledge)begin
			flag_event_capture_wait <= 1'b1; // 消费尚未完成时不能启动第二份拷贝
		end
	end

	//复制到输出并不等于消费，只有valid和ready交握才ACK
	always@(posedge i_time_clk or negedge time_rstn)begin
		if(time_rstn == 1'b0)begin
			flag_event_acknowledge <= 0;   // 源与目的共同回到一致初始翻转
		end else if(desc_valid_o && i_desc_ready)begin
			flag_event_acknowledge <= reg_event_request_sync[1]; // 此时消费者已取得整份描述符
		end
	end

endmodule
