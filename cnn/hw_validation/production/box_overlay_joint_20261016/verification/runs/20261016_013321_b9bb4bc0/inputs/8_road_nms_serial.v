`timescale 1ns / 1ps

////////////////////////////////////English///////////////////////////////////////
// Company:         RoadYOLO project
// Engineer:        Codex
// Create Date:     2026/10/15
// Design Name:     road_nms_serial
// Module Name:     road_nms_serial
// Description:     spec/nms_serial/road_nms_serial_spec.md
// Simulations:     tb_road_nms_serial.v
// Referrences:     PIF1; cnn/integer.py
// Dependencies:    None
// Version:         V1.0
// Revision Date:   2026/10/15
// History:
// Time             Version     Revised by        Contents
// 2026/10/15       V1.0        Codex             Create file.
///////////////////////////////////Chinese////////////////////////////////////////
// 版权归属:        RoadYOLO project
// 开发人员:        Codex
// 创建日期:        2026年10月15日
// 设计名称:        road_nms_serial
// 模块名称:        road_nms_serial
// 模块说明:        spec/nms_serial/road_nms_serial_spec.md
// 仿真工程:        tb_road_nms_serial.v
// 参考资料:        PIF1；cnn/integer.py
// 依赖文件:        无
// 当前版本:        V1.0
// 修订日期:        2026年10月15日
// 修订历史:
// 时间             版本        修订人            修订内容
// 2026年10月15日   V1.0        Codex             创建文件

module road_nms_serial
(
	// 全局时钟与共同取消
	input i_clk,                               // 单一计算时钟
	input i_rstn,                              // 低有效异步复位，外部同步释放
	input i_cancel,                            // 与候选读服务共同取消旧帧
	// 封存与外部候选读服务
	input i_sealed_valid,                      // 完整排序解码表可读
	input [31:0] i_frame_token,                // 本帧来源标识
	input [7:0] i_count_person,                // 行人槽数，最大128
	input [7:0] i_count_vehicle,               // 车辆槽数，最大128
	input i_read_ready,                        // 接受一个class/index请求
	input i_response_valid,                    // 响应记录有效且保持
	input i_response_class,                    // 返回所属类别
	input [6:0] i_response_index,              // 返回所属槽号
	input [159:0] i_response_data,             // 完整DECODED160
	input i_response_error,                    // 服务错误，撤销整帧
	input i_entry_ready,                       // 下游接收临时表条目
	// 握手与结果
	output o_sealed_ready,                     // 仅空闲接纳新封存表
	output o_read_valid,                       // 请求在接受前保持
	output o_read_class,                       // 当前读类别
	output [6:0] o_read_index,                 // 当前读槽
	output o_response_ready,                   // 仅有一个未决读时消费
	output o_entry_valid,                      // 输出条目等待接收
	output [96:0] o_entry_data,                // FINAL97稳定载荷
	output [31:0] o_frame_token,               // 当前输出所属封存帧
	output [6:0] o_output_count,               // 已接受数；故障清零
	output o_done,                             // 完整表所有条目已被接受
	output o_fault                             // 粘滞故障，复位或取消恢复
);

	//-------------状态参数区域-------------//
	// 读服务、串行面积和条目导出阶段
	localparam [5:0] ST_IDLE = 6'd0;            // 等待封存
	localparam [5:0] ST_VALIDATE = 6'd1;        // 检查两类数量
	localparam [5:0] ST_CLASS_CHECK = 6'd2;     // 类结束或达到32上限
	localparam [5:0] ST_CURRENT_ADDRESS = 6'd3; // 当前候选地址寄存
	localparam [5:0] ST_CURRENT_REQUEST = 6'd4; // 当前记录读请求
	localparam [5:0] ST_CURRENT_WAIT = 6'd5;    // 当前记录等待返回
	localparam [5:0] ST_CURRENT_CHECK = 6'd6;   // 几何与身份检查
	localparam [5:0] ST_INIT_CURRENT = 6'd7;    // 当前面积乘法装载
	localparam [5:0] ST_MULTIPLY_CURRENT = 6'd8;// 当前面积20步乘法
	localparam [5:0] ST_SAVE_CURRENT = 6'd9;    // 当前面积保存
	localparam [5:0] ST_COMPARE_CHECK = 6'd10;  // 是否已比完所有保留框
	localparam [5:0] ST_PREVIOUS_ADDRESS = 6'd11;// 从索引表取旧框地址
	localparam [5:0] ST_PREVIOUS_REQUEST = 6'd12;// 旧框读取请求
	localparam [5:0] ST_PREVIOUS_WAIT = 6'd13;   // 旧框读取响应
	localparam [5:0] ST_PREVIOUS_CHECK = 6'd14; // 旧框合同检查
	localparam [5:0] ST_INTERSECTION_BOUNDS = 6'd15;// 交集四边界寄存
	localparam [5:0] ST_INTERSECTION_SIZE = 6'd16;// 交集宽高截零
	localparam [5:0] ST_INIT_PREVIOUS = 6'd17;  // 旧框面积乘法装载
	localparam [5:0] ST_MULTIPLY_PREVIOUS = 6'd18;// 旧框面积20步乘法
	localparam [5:0] ST_SAVE_PREVIOUS = 6'd19;  // 保存旧框面积
	localparam [5:0] ST_INIT_INTERSECTION = 6'd20;// 交集乘法装载
	localparam [5:0] ST_MULTIPLY_INTERSECTION = 6'd21;// 交集20步乘法
	localparam [5:0] ST_COMPARE_PREPARE = 6'd22;// 42位比较两侧寄存
	localparam [5:0] ST_COMPARE_DECIDE = 6'd23; // 严格IoU大于一半
	localparam [5:0] ST_SOURCE_SCALE = 6'd24;   // 网络坐标精确乘5
	localparam [5:0] ST_SOURCE_ROUND = 6'd25;   // 单次除512最近偶数
	localparam [5:0] ST_OUTPUT_PACK = 6'd26;    // 拼装97位结果
	localparam [5:0] ST_OUTPUT = 6'd27;         // 下游接受后才更新索引
	localparam [5:0] ST_ADVANCE = 6'd28;        // 丢弃当前候选后向前
	localparam [5:0] ST_NEXT_CLASS = 6'd29;     // 复用索引空间给车辆
	localparam [5:0] ST_FINISH = 6'd30;         // 无在途读或未接受输出
	localparam [5:0] ST_FAULT = 6'd31;          // 错误锁定直到共同取消

	//---------------计数信号---------------//
	// 候选位置可表示128，输出可表示64
	reg [7:0] cnt_person = 0;                  // 冻结行人数
	reg [7:0] cnt_vehicle = 0;                 // 冻结车辆数
	reg [7:0] cnt_candidate = 0;               // 当前候选序号及结束哨兵
	reg [5:0] cnt_kept = 0;                    // 当前类已接受保留框
	reg [5:0] cnt_compare = 0;                 // 当前类比较游标
	reg [4:0] cnt_multiply = 0;                // 移位乘法步数0..19

	//--------------状态机信号--------------//
	// 下一状态只在独立组合过程中决定
	reg [5:0] state_current = 0;               // 当前控制阶段
	reg [5:0] state_next = 0;                  // 条件转移目标

	//--------------寄存器信号--------------//
	// 不复制整表，只保存两条读记录和一个小索引表
	reg reg_class = 0;                        // person为0，vehicle为1
	reg [6:0] reg_read_index = 0;              // 在途读身份直到响应接受
	reg [159:0] reg_current = 0;               // 待决定的候选记录
	reg [159:0] reg_previous = 0;              // 当前比较的已保留记录
	reg [6:0] reg_kept_index [0:31];           // 两类顺序复用；计数之外旧内容不可见
	reg [39:0] reg_multiplicand = 0;           // 移位被乘数，保留40位
	reg [19:0] reg_multiplier = 0;             // 逐位消耗的乘数
	reg [39:0] reg_product = 0;                // 精确非负部分积
	reg [39:0] reg_area_current = 0;           // 当前框面积，每候选只算一次
	reg [39:0] reg_area_previous = 0;          // 旧框面积
	reg [41:0] reg_compare_left = 0;           // 三倍交集，不截断
	reg [41:0] reg_compare_right = 0;          // 两框面积之和，零扩展
	reg [17:0] reg_inter_left = 0;             // 两左边界的较大者
	reg [17:0] reg_inter_top = 0;              // 两上边界的较大者
	reg [17:0] reg_inter_right = 0;            // 两右边界的较小者
	reg [17:0] reg_inter_bottom = 0;           // 两下边界的较小者
	reg [17:0] reg_inter_width = 0;            // 交集宽，分离时为0
	reg [17:0] reg_inter_height = 0;           // 交集高，分离时为0
	reg [20:0] reg_scale_left = 0;             // 左坐标乘5中间值
	reg [20:0] reg_scale_top = 0;              // 上坐标乘5中间值
	reg [20:0] reg_scale_right = 0;            // 右坐标乘5中间值
	reg [20:0] reg_scale_bottom = 0;           // 下坐标乘5中间值
	reg [11:0] reg_source_left = 0;            // 源图左边整数像素
	reg [11:0] reg_source_top = 0;             // 源图上边整数像素
	reg [11:0] reg_source_right = 0;           // 源图右边整数像素
	reg [11:0] reg_source_bottom = 0;          // 源图下边整数像素

	//---------------标志信号---------------//
	// 数据检查在响应握手时锁存，避免依赖随后变化的总线
	reg flag_response_bad = 0;                // 未决读身份或服务出错
	wire flag_interface;                      // 共同接口允许传输
	wire flag_current_bad;                    // 当前有效几何超界或反序
	wire flag_previous_bad;                   // 已保留记录不再满足几何合同
	wire flag_response_bad_now;               // 响应身份检查组合值
	wire flag_suppress;                       // 等号保留的整数抑制判定
	wire flag_multiply;                       // 唯一乘法器忙状态

	//---------------其他信号---------------//
	// 只在当前类别内比较
	wire [7:0] selected_count;                // 当前类别冻结槽数
	wire [17:0] current_width;                // 已验证当前框宽
	wire [17:0] current_height;               // 已验证当前框高
	wire [17:0] previous_width;               // 已验证旧框宽
	wire [17:0] previous_height;              // 已验证旧框高

	//---------------输出信号---------------//
	// 输出数据和帧标识只由时序寄存器驱动
	reg [96:0] entry_data_o = 0;               // 反压期间不改写的结果
	reg [31:0] frame_token_o = 0;              // 当前任务归属
	reg [6:0] output_count_o = 0;              // 已握手输出个数

	//-------------其他信号连线-------------//
	assign flag_interface = i_rstn && !i_cancel; // 取消不等待下一次请求
	assign selected_count = reg_class ? cnt_vehicle : cnt_person; // 复用类别计数
	assign current_width = reg_current[53:36] - reg_current[17:0]; // 几何检查后才乘
	assign current_height = reg_current[71:54] - reg_current[35:18]; // 网络Q8纵跨度
	assign previous_width = reg_previous[53:36] - reg_previous[17:0]; // 旧框横跨度
	assign previous_height = reg_previous[71:54] - reg_previous[35:18]; // 旧框纵跨度
	assign flag_current_bad = (reg_current[17:0] >= reg_current[53:36]) ||
		(reg_current[35:18] >= reg_current[71:54]) ||
		(reg_current[53:36] > 18'd131072) || (reg_current[71:54] > 18'd73728); // 有效框必须在512x288内
	assign flag_previous_bad = !reg_previous[103] ||
		(reg_previous[17:0] >= reg_previous[53:36]) ||
		(reg_previous[35:18] >= reg_previous[71:54]) ||
		(reg_previous[53:36] > 18'd131072) || (reg_previous[71:54] > 18'd73728); // 已保留框不能变无效
	assign flag_response_bad_now = i_response_error || (i_response_class != reg_class) ||
		(i_response_index != reg_read_index) || ({1'b0, i_response_index} >= selected_count) ||
		(i_response_data[102] != reg_class) || (i_response_data[159:104] != 56'd0); // 不接受跨槽或非法记录
	assign flag_suppress = reg_compare_left > reg_compare_right; // IoU等号不得抑制
	assign flag_multiply = (state_current == ST_MULTIPLY_CURRENT) ||
		(state_current == ST_MULTIPLY_PREVIOUS) || (state_current == ST_MULTIPLY_INTERSECTION); // 三阶段共用加法器

	//-------------输出信号连线-------------//
	assign o_sealed_ready = flag_interface && (state_current == ST_IDLE); // 空闲才能接新表
	assign o_read_valid = flag_interface && ((state_current == ST_CURRENT_REQUEST) ||
		(state_current == ST_PREVIOUS_REQUEST)); // 未接纳请求持续有效
	assign o_read_class = reg_class;           // 等待请求接受时类别不变
	assign o_read_index = reg_read_index;      // 等待响应前不复用身份
	assign o_response_ready = flag_interface && ((state_current == ST_CURRENT_WAIT) ||
		(state_current == ST_PREVIOUS_WAIT));   // 一次只消费一个响应
	assign o_entry_valid = flag_interface && (state_current == ST_OUTPUT); // 只在完整条目就绪后置位
	assign o_entry_data = entry_data_o;        // 握手期间固定载荷
	assign o_frame_token = frame_token_o;      // 供整表收集者识别所属任务
	assign o_output_count = output_count_o;    // 完成时是完整表数量
	assign o_done = flag_interface && (state_current == ST_FINISH); // 所有条目接受后完成
	assign o_fault = flag_interface && (state_current == ST_FAULT); // 故障表绝不发布

	//--------------状态机区域--------------//
	// 共同取消立即回到空闲；外部必须同时取消读服务和临时表
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			state_current <= ST_IDLE;          // 复位取消当前事务
		end else if(i_cancel == 1'b1)begin
			state_current <= ST_IDLE;          // 取消后可接下一完整任务
		end else begin
			state_current <= state_next;       // 常规阶段推进
		end
	end

	// 只有真实握手才能跨过请求、响应或导出状态
	always@(*)begin
		state_next = state_current;            // 停顿时保留当前阶段
		case(state_current)
			// 接受元数据后先检查范围
			ST_IDLE:begin
				if(i_sealed_valid && o_sealed_ready)begin
					state_next = ST_VALIDATE;
				end
			end
			// 不把非法数量截成较小数
			ST_VALIDATE:begin
				if((cnt_person > 8'd128) || (cnt_vehicle > 8'd128))begin
					state_next = ST_FAULT;
				end else begin
					state_next = ST_CLASS_CHECK;
				end
			end
			// 32个已接受框后不再读该类剩余候选
			ST_CLASS_CHECK:begin
				if((cnt_candidate >= selected_count) || (cnt_kept == 6'd32))begin
					if(reg_class)begin
						state_next = ST_FINISH;
					end else begin
						state_next = ST_NEXT_CLASS;
					end
				end else begin
					state_next = ST_CURRENT_ADDRESS;
				end
			end
			// 寄存地址再提出请求
			ST_CURRENT_ADDRESS:begin
				state_next = ST_CURRENT_REQUEST;
			end
			// 当前读请求可以任意反压
			ST_CURRENT_REQUEST:begin
				if(o_read_valid && i_read_ready)begin
					state_next = ST_CURRENT_WAIT;
				end
			end
			// 等待完整记录与身份
			ST_CURRENT_WAIT:begin
				if(i_response_valid && o_response_ready)begin
					state_next = ST_CURRENT_CHECK;
				end
			end
			// 无效几何跳过，合同错误故障
			ST_CURRENT_CHECK:begin
				if(flag_response_bad)begin
					state_next = ST_FAULT;
				end else if(!reg_current[103])begin
					state_next = ST_ADVANCE;
				end else if(flag_current_bad)begin
					state_next = ST_FAULT;
				end else begin
					state_next = ST_INIT_CURRENT;
				end
			end
			// 乘法输入在独立装载拍就绪
			ST_INIT_CURRENT:begin
				state_next = ST_MULTIPLY_CURRENT;
			end
			// 固定20次移位相加
			ST_MULTIPLY_CURRENT:begin
				if(cnt_multiply == 5'd19)begin
					state_next = ST_SAVE_CURRENT;
				end
			end
			// 保存当前框面积以复用
			ST_SAVE_CURRENT:begin
				state_next = ST_COMPARE_CHECK;
			end
			// 第一个框无需比较也可保留
			ST_COMPARE_CHECK:begin
				if(cnt_compare == cnt_kept)begin
					state_next = ST_SOURCE_SCALE;
				end else begin
					state_next = ST_PREVIOUS_ADDRESS;
				end
			end
			// 取已保留的候选槽索引
			ST_PREVIOUS_ADDRESS:begin
				state_next = ST_PREVIOUS_REQUEST;
			end
			// 旧框通过同一个读服务返回
			ST_PREVIOUS_REQUEST:begin
				if(o_read_valid && i_read_ready)begin
					state_next = ST_PREVIOUS_WAIT;
				end
			end
			// 当前候选在旧框返回期间保持
			ST_PREVIOUS_WAIT:begin
				if(i_response_valid && o_response_ready)begin
					state_next = ST_PREVIOUS_CHECK;
				end
			end
			// 原先已保留的框必须仍然有效
			ST_PREVIOUS_CHECK:begin
				if(flag_response_bad || flag_previous_bad)begin
					state_next = ST_FAULT;
				end else begin
					state_next = ST_INTERSECTION_BOUNDS;
				end
			end
			// 将min/max与减法分开
			ST_INTERSECTION_BOUNDS:begin
				state_next = ST_INTERSECTION_SIZE;
			end
			// 非相交宽高截为零
			ST_INTERSECTION_SIZE:begin
				state_next = ST_INIT_PREVIOUS;
			end
			// 共用乘法器计算旧框面积
			ST_INIT_PREVIOUS:begin
				state_next = ST_MULTIPLY_PREVIOUS;
			end
			// 第二次面积计算的迭代步
			ST_MULTIPLY_PREVIOUS:begin
				if(cnt_multiply == 5'd19)begin
					state_next = ST_SAVE_PREVIOUS;
				end
			end
			// 保留旧面积后腾出乘法器
			ST_SAVE_PREVIOUS:begin
				state_next = ST_INIT_INTERSECTION;
			end
			// 交集宽高已经截零
			ST_INIT_INTERSECTION:begin
				state_next = ST_MULTIPLY_INTERSECTION;
			end
			// 零交集同样走确定的20拍
			ST_MULTIPLY_INTERSECTION:begin
				if(cnt_multiply == 5'd19)begin
					state_next = ST_COMPARE_PREPARE;
				end
			end
			// 左右量显式扩到42位
			ST_COMPARE_PREPARE:begin
				state_next = ST_COMPARE_DECIDE;
			end
			// 抑制后不再比较其他旧框
			ST_COMPARE_DECIDE:begin
				if(flag_suppress)begin
					state_next = ST_ADVANCE;
				end else begin
					state_next = ST_COMPARE_CHECK;
				end
			end
			// 乘5由移位加法完成
			ST_SOURCE_SCALE:begin
				state_next = ST_SOURCE_ROUND;
			end
			// 唯一一次网络到源图舍入
			ST_SOURCE_ROUND:begin
				state_next = ST_OUTPUT_PACK;
			end
			// 输出数据在valid之前寄存
			ST_OUTPUT_PACK:begin
				state_next = ST_OUTPUT;
			end
			// 即使是最后条目也等到实际接收
			ST_OUTPUT:begin
				if(o_entry_valid && i_entry_ready)begin
					state_next = ST_CLASS_CHECK;
				end
			end
			// 无效或受抑制候选向下一槽推进
			ST_ADVANCE:begin
				state_next = ST_CLASS_CHECK;
			end
			// 清当前类别索引计数，不复位整表
			ST_NEXT_CLASS:begin
				state_next = ST_CLASS_CHECK;
			end
			// 完成只有一个周期
			ST_FINISH:begin
				state_next = ST_IDLE;
			end
			// 不自行重启出错帧
			ST_FAULT:begin
				state_next = ST_FAULT;
			end
			// 非法状态安全停机
			default:begin
				state_next = ST_FAULT;
			end
		endcase
	end

	//-----------状态任务处理区域-----------//
	// 事务状态与输出；不对小索引存储做复位以避免整表复位扇出
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			cnt_person <= 0;
			cnt_vehicle <= 0;
			cnt_candidate <= 0;
			cnt_kept <= 0;
			cnt_compare <= 0;
			reg_class <= 0;
			reg_read_index <= 0;
			reg_current <= 0;
			reg_previous <= 0;
			flag_response_bad <= 0;
			frame_token_o <= 0;
			output_count_o <= 0;
			entry_data_o <= 0;
		end else if(i_cancel == 1'b1)begin
			cnt_person <= 0;
			cnt_vehicle <= 0;
			cnt_candidate <= 0;
			cnt_kept <= 0;
			cnt_compare <= 0;
			reg_class <= 0;
			reg_read_index <= 0;
			reg_current <= 0;
			reg_previous <= 0;
			flag_response_bad <= 0;
			frame_token_o <= 0;
			output_count_o <= 0;
			entry_data_o <= 0;
		end else begin
			if(state_next == ST_FAULT)begin
				output_count_o <= 0;           // 故障否定本帧全部临时条目
			end
			case(state_current)
				// 新任务覆盖上一任务所有逻辑所有权
				ST_IDLE:begin
					if(i_sealed_valid && o_sealed_ready)begin
						cnt_person <= i_count_person;
						cnt_vehicle <= i_count_vehicle;
						frame_token_o <= i_frame_token;
						output_count_o <= 0;
						cnt_candidate <= 0;
						cnt_kept <= 0;
						cnt_compare <= 0;
						reg_class <= 0;
					end
				end
				// 只有槽范围已检查后才取低7位
				ST_CURRENT_ADDRESS:begin
					reg_read_index <= cnt_candidate[6:0];
				end
				// 返回总线只在握手时锁存
				ST_CURRENT_WAIT:begin
					if(i_response_valid && o_response_ready)begin
						reg_current <= i_response_data;
						flag_response_bad <= flag_response_bad_now;
						cnt_compare <= 0;
					end
				end
				// 比较游标严格小于保留数时才到达此状态
				ST_PREVIOUS_ADDRESS:begin
					reg_read_index <= reg_kept_index[cnt_compare[4:0]];
				end
				// 与当前记录使用同一受检响应通道
				ST_PREVIOUS_WAIT:begin
					if(i_response_valid && o_response_ready)begin
						reg_previous <= i_response_data;
						flag_response_bad <= flag_response_bad_now;
					end
				end
				// 不抑制才检查下一个保留框
				ST_COMPARE_DECIDE:begin
					if(!flag_suppress)begin
						cnt_compare <= cnt_compare + 6'd1;
					end
				end
				// 坐标整数之后拼入8个零位，不再舍入
				ST_OUTPUT_PACK:begin
					entry_data_o <= {reg_source_bottom, 8'd0, reg_source_right, 8'd0,
						reg_source_top, 8'd0, reg_source_left, 8'd0, reg_current[101:86], reg_class};
				end
				// 已接受条目才成为后续NMS比较对象
				ST_OUTPUT:begin
					if(o_entry_valid && i_entry_ready)begin
						cnt_kept <= cnt_kept + 6'd1;
						output_count_o <= output_count_o + 7'd1;
						cnt_candidate <= cnt_candidate + 8'd1;
					end
				end
				// 仅推进候选，不增加保留数
				ST_ADVANCE:begin
					cnt_candidate <= cnt_candidate + 8'd1;
				end
				// 两类不会共享已保留集合
				ST_NEXT_CLASS:begin
					reg_class <= 1'b1;
					cnt_candidate <= 0;
					cnt_kept <= 0;
					cnt_compare <= 0;
				end
				// 未列出的状态保持事务数据
				default:begin
				end
			endcase
		end
	end

	// 小索引空间只有接受输出时写；旧内容由cnt_kept隔离
	always@(posedge i_clk)begin
		if(o_entry_valid && i_entry_ready)begin
			reg_kept_index[cnt_kept[4:0]] <= cnt_candidate[6:0]; // 不缓存整份框记录
		end
	end

	// ponytail: 面积逐位相乘固定20拍；只在实测总预算不足时考虑替换此单一单元。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_multiplicand <= 0;
			reg_multiplier <= 0;
			reg_product <= 0;
			cnt_multiply <= 0;
			reg_area_current <= 0;
			reg_area_previous <= 0;
			reg_compare_left <= 0;
			reg_compare_right <= 0;
		end else if(i_cancel == 1'b1)begin
			reg_multiplicand <= 0;
			reg_multiplier <= 0;
			reg_product <= 0;
			cnt_multiply <= 0;
			reg_area_current <= 0;
			reg_area_previous <= 0;
			reg_compare_left <= 0;
			reg_compare_right <= 0;
		end else begin
			if(state_current == ST_INIT_CURRENT)begin
				reg_multiplicand <= {22'd0, current_width};
				reg_multiplier <= {2'd0, current_height};
				reg_product <= 0;
				cnt_multiply <= 0;
			end else if(state_current == ST_INIT_PREVIOUS)begin
				reg_multiplicand <= {22'd0, previous_width};
				reg_multiplier <= {2'd0, previous_height};
				reg_product <= 0;
				cnt_multiply <= 0;
			end else if(state_current == ST_INIT_INTERSECTION)begin
				reg_multiplicand <= {22'd0, reg_inter_width};
				reg_multiplier <= {2'd0, reg_inter_height};
				reg_product <= 0;
				cnt_multiply <= 0;
			end else if(flag_multiply)begin
				if(reg_multiplier[0])begin
					reg_product <= reg_product + reg_multiplicand;
				end
				reg_multiplicand <= {reg_multiplicand[38:0], 1'b0};
				reg_multiplier <= {1'b0, reg_multiplier[19:1]};
				cnt_multiply <= cnt_multiply + 5'd1;
			end
			if(state_current == ST_SAVE_CURRENT)begin
				reg_area_current <= reg_product;
			end
			if(state_current == ST_SAVE_PREVIOUS)begin
				reg_area_previous <= reg_product;
			end
			if(state_current == ST_COMPARE_PREPARE)begin
				reg_compare_left <= {2'd0, reg_product} + {1'b0, reg_product, 1'b0};
				reg_compare_right <= {2'd0, reg_area_current} + {2'd0, reg_area_previous};
			end
		end
	end

	// 交集min/max、差分截零各用一拍，避免无符号下溢
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_inter_left <= 0;
			reg_inter_top <= 0;
			reg_inter_right <= 0;
			reg_inter_bottom <= 0;
			reg_inter_width <= 0;
			reg_inter_height <= 0;
		end else if(i_cancel == 1'b1)begin
			reg_inter_left <= 0;
			reg_inter_top <= 0;
			reg_inter_right <= 0;
			reg_inter_bottom <= 0;
			reg_inter_width <= 0;
			reg_inter_height <= 0;
		end else begin
			if(state_current == ST_INTERSECTION_BOUNDS)begin
				reg_inter_left <= (reg_current[17:0] > reg_previous[17:0]) ? reg_current[17:0] : reg_previous[17:0];
				reg_inter_top <= (reg_current[35:18] > reg_previous[35:18]) ? reg_current[35:18] : reg_previous[35:18];
				reg_inter_right <= (reg_current[53:36] < reg_previous[53:36]) ? reg_current[53:36] : reg_previous[53:36];
				reg_inter_bottom <= (reg_current[71:54] < reg_previous[71:54]) ? reg_current[71:54] : reg_previous[71:54];
			end
			if(state_current == ST_INTERSECTION_SIZE)begin
				reg_inter_width <= (reg_inter_right > reg_inter_left) ? reg_inter_right - reg_inter_left : 18'd0;
				reg_inter_height <= (reg_inter_bottom > reg_inter_top) ? reg_inter_bottom - reg_inter_top : 18'd0;
			end
		end
	end

	// 乘5与最近偶数分拍；不会以两次舍入替代一次缩放
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_scale_left <= 0;
			reg_scale_top <= 0;
			reg_scale_right <= 0;
			reg_scale_bottom <= 0;
			reg_source_left <= 0;
			reg_source_top <= 0;
			reg_source_right <= 0;
			reg_source_bottom <= 0;
		end else if(i_cancel == 1'b1)begin
			reg_scale_left <= 0;
			reg_scale_top <= 0;
			reg_scale_right <= 0;
			reg_scale_bottom <= 0;
			reg_source_left <= 0;
			reg_source_top <= 0;
			reg_source_right <= 0;
			reg_source_bottom <= 0;
		end else begin
			if(state_current == ST_SOURCE_SCALE)begin
				reg_scale_left <= {1'b0, reg_current[17:0], 2'b00} + {3'b000, reg_current[17:0]};
				reg_scale_top <= {1'b0, reg_current[35:18], 2'b00} + {3'b000, reg_current[35:18]};
				reg_scale_right <= {1'b0, reg_current[53:36], 2'b00} + {3'b000, reg_current[53:36]};
				reg_scale_bottom <= {1'b0, reg_current[71:54], 2'b00} + {3'b000, reg_current[71:54]};
			end
			if(state_current == ST_SOURCE_ROUND)begin
				if((reg_scale_left[8:0] > 9'd256) || ((reg_scale_left[8:0] == 9'd256) && reg_scale_left[9]))begin
					reg_source_left <= reg_scale_left[20:9] + 12'd1;
				end else begin
					reg_source_left <= reg_scale_left[20:9];
				end
				if((reg_scale_top[8:0] > 9'd256) || ((reg_scale_top[8:0] == 9'd256) && reg_scale_top[9]))begin
					reg_source_top <= reg_scale_top[20:9] + 12'd1;
				end else begin
					reg_source_top <= reg_scale_top[20:9];
				end
				if((reg_scale_right[8:0] > 9'd256) || ((reg_scale_right[8:0] == 9'd256) && reg_scale_right[9]))begin
					reg_source_right <= reg_scale_right[20:9] + 12'd1;
				end else begin
					reg_source_right <= reg_scale_right[20:9];
				end
				if((reg_scale_bottom[8:0] > 9'd256) || ((reg_scale_bottom[8:0] == 9'd256) && reg_scale_bottom[9]))begin
					reg_source_bottom <= reg_scale_bottom[20:9] + 12'd1;
				end else begin
					reg_source_bottom <= reg_scale_bottom[20:9];
				end
			end
		end
	end

endmodule
