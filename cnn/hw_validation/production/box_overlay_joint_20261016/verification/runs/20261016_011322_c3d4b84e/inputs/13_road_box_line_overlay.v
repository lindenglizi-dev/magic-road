`timescale 1ns / 1ps

////////////////////////////////////English///////////////////////////////////////
// Company:         RoadYOLO
// Engineer:        Codex
// Create Date:     2026/10/16
// Design Name:     Serial line endpoint overlay
// Module Name:     road_box_line_overlay
// Description:     Five-cycle endpoint preparation and one-register RGB overlay.
// Simulations:     independent box_overlay_joint testbench
// Referrences:     road_box_line_overlay_spec.md
// Dependencies:    PH1P_LOGIC_DRAM
// Version:         V1.0
// Revision Date:   2026/10/16
// History:
// Time             Version     Revised by        Contents
// 2026/10/16       V1.0        Codex             Create file.
///////////////////////////////////Chinese////////////////////////////////////////
// 版权归属:        RoadYOLO
// 开发人员:        Codex
// 创建日期:        2026年10月16日
// 设计名称:        串行行端点描边
// 模块名称:        road_box_line_overlay
// 模块说明:        五拍准备框端点并保持视频单拍输出。
// 仿真工程:        独立框与年龄叠加验证
// 参考资料:        road_box_line_overlay_spec.md
// 依赖文件:        PH1P_LOGIC_DRAM
// 当前版本:        V1.0
// 修订日期:        2026年10月16日
// 修订历史:
// 时间             版本        修订人            修订内容
// 2026年10月16日   V1.0        Codex             创建文件

module road_box_line_overlay
(
	//---------------全局信号---------------//
	input i_clk,                                  // HDMI像素域时钟
	input i_rstn,                                 // 公共低有效复位
	//---------------用户接口---------------//
	input i_sof,                                  // 消隐期新显示帧边沿
	input i_vsync,                                // 输入垂直同步电平
	input i_hsync,                                // 输入水平同步电平
	input i_de,                                   // 当前输入像素有效
	input [23:0] i_rgb,                            // 未叠加的输入颜色
	input i_table_active_valid,                   // 已提交整表的存在标志
	input [6:0] i_table_count,                     // 活动整表的框数上限六十四
	input [96:0] i_table_entry,                    // 当前索引的异步FINAL97表项
	input i_table_draw_valid,                     // 当前像素实时绘框许可
	output [5:0] o_table_read_index,               // 唯一表读口的串行索引
	output o_vsync,                               // 延后一拍的垂直同步
	output o_hsync,                               // 延后一拍的水平同步
	output o_de,                                  // 延后一拍的有效像素电平
	output [23:0] o_rgb,                           // 单拍延迟的描边颜色
	output o_sof,                                 // 与输出视频等延迟的帧标记
	output o_line_ready,                          // 本行端点图已完整准备
	output o_prepare_busy,                        // 清图或串行准备尚未结束
	output [8:0] o_last_prepare_cycles,            // 最近一行的五拍扫描总数
	output o_fault                                // 复位前保持的非法或超时标志
);

	//-------------状态参数区域-------------//
	// 单存储端口按清除、等待、五拍扫描与显示顺序复用。
	localparam [3:0] ST_CLEAR = 4'd0;              // 逐地址抹去整张事件图
	localparam [3:0] ST_WAIT = 4'd1;               // 消隐边沿采样已切换活动表
	localparam [3:0] ST_FETCH = 4'd2;              // 锁存当前框的两个端点意图
	localparam [3:0] ST_READ_LEFT = 4'd3;          // 仅采样左端点旧存储字
	localparam [3:0] ST_WRITE_LEFT = 4'd4;         // 写回左端点累积事件
	localparam [3:0] ST_READ_RIGHT = 4'd5;         // 仅采样右端点旧存储字
	localparam [3:0] ST_WRITE_RIGHT = 4'd6;        // 写回右端点并推进框索引
	localparam [3:0] ST_READY = 4'd7;             // 等待有效行或下一行消隐

	//---------------计数信号---------------//
	// 视频位置和准备测量分别计数，清图不计入扫描周期。
	reg [10:0] cnt_pixel = 0;                     // 当前输入有效行的横坐标
	reg [9:0] cnt_row = 0;                        // 当前待描边行的纵坐标
	reg [10:0] cnt_clear_address = 0;             // 全图清零的当前字地址
	reg [6:0] cnt_box_limit = 0;                  // 本行锁存且截到六十四的表长度
	reg [8:0] cnt_prepare_cycles = 0;             // 已完成的扫描状态边沿数

	//--------------状态机信号--------------//
	// 下一状态与时序寄存器严格分离。
	reg [3:0] state_current = 0;                  // 当前端点存储端口用途
	reg [3:0] state_next = 0;                     // 下一拍的端口调度状态

	//--------------寄存器信号--------------//
	// 一框端点暂存避免保留第二份完整检测表。
	reg reg_de_previous = 0;                     // 识别有效行起止的前拍电平
	reg [10:0] reg_left_address = 0;              // 当前框左侧事件所在字地址
	reg [10:0] reg_right_address = 0;             // 当前框右侧事件所在字地址
	reg reg_box_vehicle = 0;                     // 本框选择车辆事件字段
	reg reg_horizontal_border = 0;               // 本行属于框顶边或底边
	reg reg_left_enabled = 0;                    // 左端点存在且几何合法
	reg reg_right_enabled = 0;                   // 右端点存在且无需去重或省略
	reg [17:0] reg_old_word = 0;                  // 读拍捕获的十八位旧事件字
	reg signed [8:0] reg_person_prefix = 0;       // 人类水平区间的非负覆盖数
	reg signed [8:0] reg_vehicle_prefix = 0;      // 车辆水平区间的非负覆盖数
	reg reg_map_write_enable = 0;                // 原生事件RAM的边沿写允许
	reg [10:0] reg_map_write_address = 0;         // 清除或更新的写字地址
	reg [10:0] reg_map_read_address = 0;          // 像素消费或准备读取的地址
	reg [17:0] reg_map_write_word = 0;            // 更新事件或显式清零的写值

	//---------------其他信号---------------//
	// FINAL97整数字段仅裁剪，低八位异常不做再次舍入。
	wire [11:0] wire_left_clipped;               // 裁到一千二百八十的左边界
	wire [11:0] wire_right_clipped;              // 裁到屏宽的半开右边界
	wire [11:0] wire_top_clipped;                // 裁到七百二十的顶边界
	wire [11:0] wire_bottom_clipped;             // 裁到屏高的半开底边界
	wire wire_fractional;                       // 任一坐标携带非零小数位
	wire wire_geometry_valid;                   // 正面积且覆盖当前纵坐标
	wire wire_horizontal_border;                // 当前纵坐标命中上下水平边
	wire [17:0] wire_map_read_word;              // 无输出寄存器的原生异步读值
	wire signed [8:0] wire_person_delta;         // 人类有符号八位增量的扩展
	wire signed [8:0] wire_vehicle_delta;        // 车辆有符号八位增量的扩展
	wire signed [8:0] wire_person_sum;           // 当前像素消费事件后的覆盖数
	wire signed [8:0] wire_vehicle_sum;          // 车辆区间在当前像素的新覆盖数
	wire wire_prefix_legal;                     // 两类覆盖数均在零至六十四
	wire wire_person_hit;                       // 人类区间或独立垂线点命中
	wire wire_vehicle_hit;                      // 车辆区间或独立垂线点命中

	//---------------输出信号---------------//
	// 输出状态与视频使用明确的桥接，不增加视频反压。
	reg [5:0] table_read_index_o = 0;            // 串行异步表口的当前框位置
	reg vsync_o = 0;                            // 垂直同步的唯一流水寄存器
	reg hsync_o = 0;                            // 水平同步的唯一流水寄存器
	reg de_o = 0;                               // 像素有效的唯一流水寄存器
	reg [23:0] rgb_o = 0;                       // 原始或框色的唯一流水寄存器
	reg sof_o = 0;                              // 新帧标记的唯一流水寄存器
	reg line_ready_o = 0;                       // 准备完成后保持至本行结束
	wire prepare_busy_o;                        // 显示就绪状态以外均占用准备端
	reg [8:0] last_prepare_cycles_o = 0;         // 完整扫描结束时冻结测量结果
	reg fault_o = 0;                            // 超时或覆盖数非法的粘滞故障

	//-------------其他信号连线-------------//
	assign wire_left_clipped = i_table_entry[36:25] > 12'd1280 ? 12'd1280 : i_table_entry[36:25]; // 左边整数端点先限幅
	assign wire_right_clipped = i_table_entry[76:65] > 12'd1280 ? 12'd1280 : i_table_entry[76:65]; // 右边整数端点保持半开语义
	assign wire_top_clipped = i_table_entry[56:45] > 12'd720 ? 12'd720 : i_table_entry[56:45]; // 顶边越界时限到屏高
	assign wire_bottom_clipped = i_table_entry[96:85] > 12'd720 ? 12'd720 : i_table_entry[96:85]; // 底边越界时限到屏高
	assign wire_fractional = |{i_table_entry[24:17], i_table_entry[44:37], i_table_entry[64:57], i_table_entry[84:77]}; // 四组小数位合并检查
	assign wire_geometry_valid = !wire_fractional && wire_left_clipped < wire_right_clipped && wire_top_clipped < wire_bottom_clipped && cnt_row >= wire_top_clipped && cnt_row < wire_bottom_clipped; // 非法小数与裁剪塌缩只跳过本框
	assign wire_horizontal_border = cnt_row == wire_top_clipped || cnt_row == wire_bottom_clipped - 12'd1; // 半开底边向内收一像素
	assign wire_person_delta = {wire_map_read_word[7], wire_map_read_word[7:0]}; // 人类增量补符号位到九位
	assign wire_vehicle_delta = {wire_map_read_word[15], wire_map_read_word[15:8]}; // 车辆增量独立补符号位
	assign wire_person_sum = (reg_de_previous ? reg_person_prefix : 9'sd0) + wire_person_delta; // 行首从零开始消费人类事件
	assign wire_vehicle_sum = (reg_de_previous ? reg_vehicle_prefix : 9'sd0) + wire_vehicle_delta; // 行首从零开始消费车辆事件
	assign wire_prefix_legal = wire_person_sum >= 9'sd0 && wire_person_sum <= 9'sd64 && wire_vehicle_sum >= 9'sd0 && wire_vehicle_sum <= 9'sd64; // 非法覆盖计数禁止绕回继续画框
	assign wire_person_hit = wire_person_sum > 9'sd0 || wire_map_read_word[16]; // 水平覆盖与人类垂线点合并
	assign wire_vehicle_hit = wire_vehicle_sum > 9'sd0 || wire_map_read_word[17]; // 水平覆盖与车辆垂线点合并
	assign prepare_busy_o = state_current != ST_READY; // 清图和五拍扫描都对外标忙

	//-------------输出信号连线-------------//
	assign o_table_read_index = table_read_index_o; // 活动表地址从本模块单一输出
	assign o_vsync = vsync_o;                    // 同步信号与RGB共用一拍边界
	assign o_hsync = hsync_o;                    // 行同步保持输入原始极性
	assign o_de = de_o;                          // 有效标记不被准备状态阻塞
	assign o_rgb = rgb_o;                        // 已选颜色直接桥接输出端口
	assign o_sof = sof_o;                        // AGE接收等延迟的新帧标记
	assign o_line_ready = line_ready_o;          // 完成标记供行预算检查使用
	assign o_prepare_busy = prepare_busy_o;      // 内部端口占用状态对外可见
	assign o_last_prepare_cycles = last_prepare_cycles_o; // 最近完成行的扫描周期可观测
	assign o_fault = fault_o;                    // 故障保持直到公共复位

	//-----------输出信号处理区域-----------//
	// 每拍无条件推进视频，仅许可有效且完整的整行覆盖；人类颜色优先。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			vsync_o <= 0;                       // 复位期间输出同步回低
			hsync_o <= 0;                       // 初始化行同步流水
			de_o <= 0;                          // 清除输出有效像素
			rgb_o <= 0;                         // 复位输出黑色
			sof_o <= 0;                         // 禁止复位遗留帧标记
		end else begin
			vsync_o <= i_vsync;                 // 垂直同步延迟一个时钟
			hsync_o <= i_hsync;                 // 水平同步同拍向前传递
			de_o <= i_de;                       // DE始终按固定一拍输出
			sof_o <= i_sof;                     // SOF与对应视频相位对齐
			rgb_o <= i_rgb;                     // 没有描边条件时透传原始颜色
			if(i_de && i_table_draw_valid && line_ready_o && wire_prefix_legal && cnt_pixel < 11'd1280)begin
				if(wire_person_hit)begin
					rgb_o <= 24'h00ff00;          // 交叉重叠时人类边框覆盖车辆
				end else if(wire_vehicle_hit)begin
					rgb_o <= 24'h00ffff;          // 没有人类命中时使用车辆青色
				end else begin
					rgb_o <= i_rgb;              // 两类事件均未命中时保留输入
				end
			end
		end
	end

	//--------------状态机区域--------------//
	// 公共复位及每次SOF重新清除存储；未完成准备的行首立即取消扫描。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			state_current <= ST_CLEAR;          // 冷启动先走显式清图
		end else begin
			state_current <= state_next;        // 更新三段式控制状态
		end
	end

	// 扫描只在消隐运行；清图可跨异常有效期，但不会在该行中途开始绘制。
	always@(*)begin
		state_next = state_current;             // 未触发转换时维持端口用途
		if(i_sof)begin
			state_next = ST_CLEAR;              // 表切换边沿优先撤销旧行
		end else if(i_de && !reg_de_previous && !line_ready_o && state_current != ST_CLEAR)begin
			state_next = ST_READY;              // 迟到准备取消且本行始终透传
		end else begin
			case(state_current)
				// 清完最后一字后等待消隐，以免中途准备旧行零。
				ST_CLEAR:begin
					if(cnt_clear_address == 11'd1279)begin
						state_next = ST_WAIT;   // 全图清完才允许采样新表
					end
				end
				// 此边沿在表提交之后，零框也明确形成准备完成状态。
				ST_WAIT:begin
					if(!i_de && cnt_row < 10'd720)begin
						if(i_table_active_valid && i_table_count != 0)begin
							state_next = ST_FETCH; // 非空表开始固定五拍扫描
						end else begin
							state_next = ST_READY; // 空表无需构建事件
						end
					end
				end
				// FETCH为每框保留独立几何采样周期。
				ST_FETCH:begin
					state_next = ST_READ_LEFT;  // 下一拍读取第一个端点
				end
				// 左端点读拍不写存储。
				ST_READ_LEFT:begin
					state_next = ST_WRITE_LEFT; // 已捕获旧字后执行写回
				end
				// 左端点写拍读地址异或一避开碰撞。
				ST_WRITE_LEFT:begin
					state_next = ST_READ_RIGHT; // 给第二端点完整读取周期
				end
				// 右端点即使省略也保留读状态。
				ST_READ_RIGHT:begin
					state_next = ST_WRITE_RIGHT; // 固定每框第五拍完成写回
				end
				// 六十四框末拍后立即标记整行完成。
				ST_WRITE_RIGHT:begin
					if({1'b0, table_read_index_o} + 7'd1 >= cnt_box_limit)begin
						state_next = ST_READY;  // 所有框的端点均已处理
					end else begin
						state_next = ST_FETCH;  // 继续活动表下一索引
					end
				end
				// DE下降边沿先清最后字，最后一行结束后无后续准备。
				ST_READY:begin
					if(!i_de && reg_de_previous && cnt_row < 10'd719)begin
						state_next = ST_WAIT;   // 下一消隐边沿锁存表计数
					end
				end
				// 无效编码先清图，防止不完整事件被消费。
				default:begin
					state_next = ST_CLEAR;      // 恢复到不依赖RAM初值的路径
				end
			endcase
		end
	end

	//-----------状态任务处理区域-----------//
	// 本行只保存计数、两个端点和一个旧字，扫描状态边沿严格五次计数。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			cnt_clear_address <= 0;             // 冷清图从地址零开始
			cnt_box_limit <= 0;                 // 尚未采样活动框表
			cnt_prepare_cycles <= 0;            // 清除扫描测量累积
			table_read_index_o <= 0;            // 初始异步表索引为零
			last_prepare_cycles_o <= 0;         // 没有完整扫描测量时返回零
			reg_left_address <= 0;              // 初始化左端点暂存
			reg_right_address <= 0;             // 初始化右端点暂存
			reg_box_vehicle <= 0;               // 复位类选择为人类
			reg_horizontal_border <= 0;         // 禁用未锁存的水平区间
			reg_left_enabled <= 0;              // 复位不存在可写左端点
			reg_right_enabled <= 0;             // 复位不存在可写右端点
			reg_old_word <= 0;                  // 旧事件字在读取之前无效
		end else if(i_sof)begin
			cnt_clear_address <= 0;             // 新帧再次清除全部一千二百八十字
			cnt_prepare_cycles <= 0;            // 新帧不延续旧行扫描时间
			table_read_index_o <= 0;            // 活动新表从首框开始
			reg_left_enabled <= 0;              // 撤销SOF之前的左写请求
			reg_right_enabled <= 0;             // 撤销SOF之前的右写请求
		end else if(state_current == ST_CLEAR)begin
			if(cnt_clear_address != 11'd1279)begin
				cnt_clear_address <= cnt_clear_address + 11'd1; // 每拍清一字直至末地址
			end
		end else if(!i_de)begin
			if(state_current == ST_WAIT && cnt_row < 10'd720)begin
				cnt_box_limit <= !i_table_active_valid ? 7'd0 : (i_table_count > 7'd64 ? 7'd64 : i_table_count); // 不存在整表时等价空表
				table_read_index_o <= 0;        // 每行重新串行遍历同一冻结表
				cnt_prepare_cycles <= 0;        // 单行计数排除等待与清图
				if(!i_table_active_valid || i_table_count == 0)begin
					last_prepare_cycles_o <= 0; // 空表完成没有框扫描周期
				end
			end else if(state_current >= ST_FETCH && state_current <= ST_WRITE_RIGHT)begin
				cnt_prepare_cycles <= cnt_prepare_cycles + 9'd1; // 五个扫描状态都占一个边沿
				if(state_current == ST_FETCH)begin
					reg_left_address <= wire_left_clipped[10:0]; // 记录本框的起始事件位置
					reg_right_address <= wire_horizontal_border ? wire_right_clipped[10:0] : wire_right_clipped - 12'd1; // 水平区间终点与垂线右点分用
					reg_box_vehicle <= i_table_entry[0]; // 类别来自已冻结FINAL97最低位
					reg_horizontal_border <= wire_horizontal_border; // 后续写拍使用同一几何判定
					reg_left_enabled <= wire_geometry_valid; // 越界塌缩和小数异常只禁本框
					reg_right_enabled <= wire_geometry_valid && (wire_horizontal_border ? wire_right_clipped < 12'd1280 : wire_right_clipped - 12'd1 != wire_left_clipped); // 终端事件省略且单像素垂线去重
				end
				if(state_current == ST_READ_LEFT || state_current == ST_READ_RIGHT)begin
					reg_old_word <= wire_map_read_word; // 两个读取阶段均先捕获原生异步字
				end
				if(state_current == ST_WRITE_RIGHT)begin
					if({1'b0, table_read_index_o} + 7'd1 >= cnt_box_limit)begin
						last_prepare_cycles_o <= cnt_prepare_cycles + 9'd1; // 末框第五拍纳入最终统计
					end else begin
						table_read_index_o <= table_read_index_o + 6'd1; // 两端点完成后才推进异步表口
					end
				end
			end
		end
	end

	// 单存储读口在有效期只消费当前横坐标，写口清除前一像素，读写永不同址。
	always@(*)begin
		reg_map_write_enable = 0;               // 未命中的阶段禁止任何写入
		reg_map_write_address = 0;              // 默认写地址不影响关闭的写口
		reg_map_read_address = 0;               // 空闲读口指向合法字零
		reg_map_write_word = 0;                 // 清图和消费默认写显式零字
		if(i_rstn && !i_sof)begin
			if(state_current == ST_CLEAR)begin
				reg_map_write_enable = 1;       // 全图初始化每拍写一个字
				reg_map_write_address = cnt_clear_address; // 清零遍历受限深度一千二百八十
				reg_map_read_address = cnt_clear_address ^ 11'd1; // 清图不消费读口且避同址
			end else if(i_de)begin
				if(cnt_pixel < 11'd1280)begin
					reg_map_read_address = cnt_pixel; // 像素零也直接读取事件图首字
					if(cnt_pixel != 0)begin
						reg_map_write_enable = 1; // 当前读取之后清掉前一已消费事件
						reg_map_write_address = cnt_pixel - 11'd1; // 写地址严格落后当前横坐标
					end
				end
			end else if(reg_de_previous && cnt_pixel != 0)begin
				reg_map_write_enable = 1;       // 首个消隐边沿清最后已读事件
				reg_map_write_address = cnt_pixel - 11'd1; // 正常宽行此地址为一千二百七十九
				reg_map_read_address = reg_map_write_address ^ 11'd1; // DE下降不再有像素读取消费者
			end else begin
				case(state_current)
					// 左读阶段的RAM输出只交给旧字寄存器。
					ST_READ_LEFT:begin
						reg_map_read_address = reg_left_address; // 首端点读拍保持写允许为零
					end
					// 左水平事件加一，垂线事件仅置相应类点位。
					ST_WRITE_LEFT:begin
						reg_map_write_enable = reg_left_enabled; // 被跳过框仍保留本拍但不写RAM
						reg_map_write_address = reg_left_address; // 左端点写回先前读取的位置
						reg_map_read_address = reg_left_address ^ 11'd1; // 写拍不依赖碰撞时的读输出
						reg_map_write_word = reg_old_word; // 未修改的另一类字段完整保留
						if(reg_horizontal_border)begin
							if(reg_box_vehicle)begin
								reg_map_write_word[15:8] = reg_old_word[15:8] + 8'd1; // 车辆区间进入事件累加
							end else begin
								reg_map_write_word[7:0] = reg_old_word[7:0] + 8'd1; // 人类区间进入事件累加
							end
						end else if(reg_box_vehicle)begin
							reg_map_write_word[17] = 1; // 车辆左垂线使用幂等点标志
						end else begin
							reg_map_write_word[16] = 1; // 人类左垂线使用幂等点标志
						end
					end
					// 右读阶段在左写结束后读取，允许两框共用端点。
					ST_READ_RIGHT:begin
						reg_map_read_address = reg_right_enabled ? reg_right_address : 11'd0; // 省略的屏外终点不产生非法地址
					end
					// 右水平事件减一，非水平行按独立点写回。
					ST_WRITE_RIGHT:begin
						reg_map_write_enable = reg_right_enabled; // 屏宽终端或重复垂点不实际写入
						reg_map_write_address = reg_right_enabled ? reg_right_address : 11'd0; // 关闭写口也保持地址范围合法
						reg_map_read_address = reg_map_write_address ^ 11'd1; // 原生RAM写拍读地址与写地址分离
						reg_map_write_word = reg_old_word; // 右端点保留另一个类别的事件
						if(reg_horizontal_border)begin
							if(reg_box_vehicle)begin
								reg_map_write_word[15:8] = reg_old_word[15:8] - 8'd1; // 车辆半开区间离开事件
							end else begin
								reg_map_write_word[7:0] = reg_old_word[7:0] - 8'd1; // 人类半开区间离开事件
							end
						end else if(reg_box_vehicle)begin
							reg_map_write_word[17] = 1; // 车辆右垂线与已有点进行合并
						end else begin
							reg_map_write_word[16] = 1; // 人类右垂线与已有点进行合并
						end
					end
					// 等待和几何取样阶段不访问写端。
					default:begin
						reg_map_write_enable = 0; // 非读改写阶段保持事件图不变
					end
				endcase
			end
		end
	end

	//-----------主要任务处理区域-----------//
	// 视频位置与运行时覆盖计数跟随输入DE，即使实时绘制许可已经撤销。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			reg_de_previous <= 0;               // 冷启动不存在前一有效像素
			cnt_pixel <= 0;                     // 当前行读取位置从零开始
			cnt_row <= 0;                       // 第一显示行使用纵坐标零
			reg_person_prefix <= 0;             // 人类前缀覆盖计数复位
			reg_vehicle_prefix <= 0;            // 车辆前缀覆盖计数复位
		end else begin
			reg_de_previous <= i_de;            // DE下降时保留一个清尾字边沿
			if(i_sof)begin
				cnt_pixel <= 0;                 // 新帧重新定位左上角
				cnt_row <= 0;                   // SOF属于屏幕零行准备窗口
				reg_person_prefix <= 0;         // 新表不能继承旧帧水平覆盖
				reg_vehicle_prefix <= 0;        // 车辆覆盖也在帧边界归零
			end else if(i_de)begin
				if(cnt_pixel < 11'd1280)begin
					cnt_pixel <= cnt_pixel + 11'd1; // 每个有效像素消费一个事件地址
				end
				if(line_ready_o && wire_prefix_legal)begin
					reg_person_prefix <= wire_person_sum; // 九位保留全部六十四人类重叠
					reg_vehicle_prefix <= wire_vehicle_sum; // 车辆类覆盖独立累积
				end else begin
					reg_person_prefix <= 0;     // 非法或整行未完成时不回绕计数
					reg_vehicle_prefix <= 0;    // 同步禁用残缺车辆区间
				end
			end else begin
				cnt_pixel <= 0;                 // 消隐期间读位置固定在下一行首
				reg_person_prefix <= 0;         // 行末水平前缀不跨行保留
				reg_vehicle_prefix <= 0;        // 车辆覆盖在下一行独立重建
				if(reg_de_previous && cnt_row < 10'd720)begin
					cnt_row <= cnt_row + 10'd1; // 最后一行结束后停在七百二十
				end
			end
		end
	end

	// 整行准备许可独立于实时表年龄；行首迟到或非法前缀都会关闭余下整行。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			line_ready_o <= 0;                  // 显式清图之前禁止任何描边
		end else if(i_sof)begin
			line_ready_o <= 0;                  // 新帧在清图和扫描完成前不可画
		end else if(i_de)begin
			if(!wire_prefix_legal || cnt_pixel >= 11'd1280)begin
				line_ready_o <= 0;              // 计数不合法时抑制当前行后续颜色
			end
		end else if(reg_de_previous)begin
			line_ready_o <= 0;                  // 清尾字同时撤销上一行完成标志
		end else if(state_current == ST_WAIT && cnt_row < 10'd720)begin
			if(!i_table_active_valid || i_table_count == 0)begin
				line_ready_o <= 1;              // 空表也已准备完可消费的零事件图
			end
		end else if(state_current == ST_WRITE_RIGHT && {1'b0, table_read_index_o} + 7'd1 >= cnt_box_limit)begin
			line_ready_o <= 1;                  // 最后一框写拍完成后整行可画
		end
	end

	// 超时仅报告而不阻塞视频，末行之后无下一行预算要求。
	always@(posedge i_clk or negedge i_rstn)begin
		if(i_rstn == 1'b0)begin
			fault_o <= 0;                       // 唯一清除粘滞故障的公共复位
		end else if(i_sof && i_de)begin
			fault_o <= 1;                       // SOF违反消隐来源契约
		end else if(i_de && !reg_de_previous && !line_ready_o && cnt_row < 10'd720)begin
			fault_o <= 1;                       // DE到来前未准备完成整行
		end else if(i_de && line_ready_o && !wire_prefix_legal)begin
			fault_o <= 1;                       // 九位覆盖数超出合法零至六十四
		end else if(i_de && cnt_pixel >= 11'd1280)begin
			fault_o <= 1;                       // 防止有效行超宽导致地址回绕
		end else if(state_current == ST_WAIT && !i_de && i_table_active_valid && i_table_count > 7'd64)begin
			fault_o <= 1;                       // 超长表截到物理六十四框并报告
		end
	end

	//------------模块实例化区域------------//
	// 原生分布式RAM只使用异步读输出；运行时清除而非初始化保证内容有效。
	PH1P_LOGIC_DRAM
	#(
		.DATA_WIDTH_W(18),                     // 单字含两点与两路八位有符号增量
		.DATA_WIDTH_R(18),                     // 读写字段布局保持完全一致
		.ADDR_WIDTH_W(11),                     // 写地址覆盖屏宽一千二百八十
		.ADDR_WIDTH_R(11),                     // 独立读口使用相同字寻址
		.DATA_DEPTH_W(1280),                   // 禁止扩展为完整框表或ERAM
		.DATA_DEPTH_R(1280),                   // 仅读取当前行的端点事件图
		.INIT_FILE("NONE"),                    // 没有外部初始化文件依赖
		.FILL_ALL("NONE"),                     // 运行时完整清图覆盖上电内容
		.READREG("DISABLE"),                   // 单像素读口不增加RAM输出拍
		.RESETMODE("SYNC")                     // 未使用的读寄存器维持同步模式
	)PH1P_LOGIC_DRAM_Inst_line_events(
		.di(reg_map_write_word),               // 清零或读改写后的事件字
		.waddr(reg_map_write_address),         // 全图遍历或单端点写回位置
		.we(reg_map_write_enable),             // 读阶段严格关闭写使能
		.wclk(i_clk),                          // 端点写入与视频使用同一像素时钟
		.rclk(i_clk),                          // 原生异步输出不使用读时钟寄存
		.rrst(1'b0),                           // 事件内容由显式地址清图负责
		.rce(1'b0),                            // 不启用未使用的输出寄存器
		.raddr(reg_map_read_address),          // 消费当前像素或读取端点旧值
		.rdoq(),                               // 注册读输出未参与视频路径
		.rdo(wire_map_read_word)               // 唯一实际被消费的异步读端
	);

endmodule
