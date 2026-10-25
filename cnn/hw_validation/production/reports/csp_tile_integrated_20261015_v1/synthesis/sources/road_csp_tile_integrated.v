`timescale 1ns / 1ps
////////////////////////////////////English///////////////////////////////////////
// Company: RoadYOLO
// Engineer: Codex
// Create Date: 2026-10-15
// Design Name: Hardware-driven first residual tile
// Module Name: road_csp_tile_integrated
// Description: road_csp_tile_integrated_spec.md
// Simulations: tb_csp_tile_integrated
// Referrences: road_csp_tile_integrated_spec.md
// Dependencies: road_csp_tile_schedule, road_csp_dw_cache, road_csp_first_probe
// Version: V1.0
// Revision Date: 2026-10-15
// History: 2026-10-15 V1.0 Codex Create file
///////////////////////////////////Chinese////////////////////////////////////////
// 版权归属: RoadYOLO
// 开发人员: Codex
// 创建日期: 2026-10-15
// 设计名称: 首残差tile硬件闭环
// 模块名称: road_csp_tile_integrated
// 模块说明: 固定ROM参数、单端口源取数、DW缓存与真实写退休
// 仿真工程: tb_csp_tile_integrated
// 参考资料: road_csp_tile_integrated_spec.md
// 依赖文件: 调度、DW缓存与冻结算术包装
// 当前版本: V1.0
// 修订日期: 2026-10-15
// 修订历史: 2026-10-15 V1.0 Codex 创建固定tile闭环
module road_csp_tile_integrated #(
    parameter C_WEIGHT_FILE = "weight_program.hex", // 同一模型导出的56个紧凑稀疏权重词
    parameter C_PARAMETER_FILE = "parameter_program.hex" // 同一模型导出的16个量化参数词
)(
    input i_clk, // 100MHz同域时钟
    input i_rstn, // 全部模块共同异步低有效取消
    input i_table_valid, // 空闲时重载SiLU表
    input [9:0]i_table_addr, // 顺序1024项表地址
    input signed [15:0]i_table_data, // 原包Q7.8表项
    output o_table_ready, // 表项真实接受许可
    output o_table_loaded, // 完整表可供本地复用
    input i_source_begin, // begin_ready时清理源有效位
    output o_source_begin_ready, // 上一tile已退休才允许替换源
    input i_source_valid, // 写入一个源字节并保持至ready
    input [9:0]i_source_address, // 0至431为halo，432至623为旁路
    input [7:0]i_source_data, // 源INT8补码字节
    output o_source_ready, // 只在采集阶段接受源字节
    output o_source_loaded, // 624个不同源位置均已写入
    input i_start, // start_ready时启动160个任务
    output o_start_ready, // 完整源和表且计算空闲
    input i_cancel, // 边沿前取消，粘滞至共同复位
    input i_output_ready, // 外部真实写端反压
    output o_output_valid, // 外部写与DW缓存写原子接受
    output [7:0]o_output_data, // 真实饱和INT8结果
    output [15:0]o_output_tag, // DW为0至191，PW为192至383
    output [31:0]o_output_address, // 冻结图逻辑字节地址
    output signed [8:0]o_output_sum, // 实际残差中间值
    output o_busy, // 任务或操作数适配仍占有
    output o_done, // 最后实际写接受后单拍完成
    output o_fault // 任一模块故障粘滞，需要共同复位
);
    //-----------------状态参数-----------------//
    localparam [3:0]ST_IDLE = 4'd0; // 等待硬件调度器的组描述符
    localparam [3:0]ST_PREPARE = 4'd1; // 注册紧凑权重和参数
    localparam [3:0]ST_HALO_ADDRESS = 4'd2; // 为单端口源RAM产生一个地址
    localparam [3:0]ST_HALO_READ = 4'd3; // 注册一个DW激活字节
    localparam [3:0]ST_PW_REQUEST = 4'd4; // 请求当前实际DW缓存组
    localparam [3:0]ST_PW_WAIT = 4'd5; // 消费注册缓存响应
    localparam [3:0]ST_BYPASS_ADDRESS = 4'd6; // 为一个旁路字节产生地址
    localparam [3:0]ST_BYPASS_READ = 4'd7; // 注册一个旁路字节
    localparam [3:0]ST_SEND = 4'd8; // 整组载荷保持至算术核接受
    //-----------------状态与源存储-----------------//
    reg [3:0]state_current; // 适配器当前状态
    reg [3:0]state_next; // 独立组合下一状态
    reg [7:0]mem_source [0:623]; // RAM数据不复位，由完整位图保护
    reg [623:0]reg_source_written; // 每个源位置本次已写标志
    reg [9:0]reg_source_count; // 唯一源字节数
    reg flag_fault; // 源、取消或内部协议错误的粘滞记录
    reg [191:0]mem_weight [0:55]; // DW12通道两种空间布局及PW四输出组
    reg [247:0]mem_parameter [0:15]; // 偏置、双重定标参数的紧凑只读词
    reg [191:0]reg_weight; // 当前组驻留权重
    reg [247:0]reg_parameter; // 当前任务量化参数
    reg [63:0]reg_activation; // 单端口读取拼装后的八输入
    reg [23:0]reg_bypass; // PW首组的三个真实旁路值
    reg [2:0]reg_fetch_lane; // 源RAM串行读取位置
    reg [9:0]reg_source_index; // 注册后的源RAM字节索引
    reg [8:0]reg_halo_base; // 当前DW窗口左上角在halo内的位置
    reg [7:0]reg_output_base; // 当前像素输出通道局部索引
    reg [47:0]reg_tags; // 当前任务三个完整tag
    reg [95:0]reg_addresses; // 当前任务三个完整字节地址
    reg [15:0]reg_final_tag; // 当前任务最后有效输出标识
    //-----------------调度接口-----------------//
    wire schedule_start_ready; // 固定调度器空闲许可
    wire schedule_group_valid; // 描述符保持至整组真实接受
    wire schedule_first; // 当前组首标志
    wire schedule_last; // 当前组末标志
    wire schedule_pw; // DW之后才进入PW
    wire [1:0]schedule_y; // tile内行坐标
    wire [1:0]schedule_x; // 三点起始横坐标或PW像素
    wire [3:0]schedule_channel; // DW通道或PW三通道起点
    wire [2:0]schedule_mask; // 有效输出路
    wire [7:0]schedule_input_mask; // 当前八输入有效掩码
    wire [7:0]schedule_task; // 单调任务编号
    wire schedule_busy; // 调度器尚未退休
    wire schedule_done; // 最后真实写退休事件
    wire schedule_fault; // 描述符故障
    //-----------------算术与缓存接口-----------------//
    wire core_table_ready; // 原共享表接口ready
    wire core_loaded; // 表已完整激活
    wire core_ready; // 冻结算术组准入
    wire core_valid; // 真实算术写载荷valid
    wire [7:0]core_data; // 真实算术输出
    wire [15:0]core_tag; // 算术元数据tag
    wire [31:0]core_address; // 算术元数据地址
    wire signed [8:0]core_sum; // 残差signed9和
    wire core_fault; // 原冻结算术错误
    wire cache_write_ready; // 仅采集时接受DW
    wire cache_loaded; // 192实际DW写的完整屏障
    wire [7:0]cache_write_count; // 实际缓存写计数
    wire cache_fault; // 重复或越界缓存写故障
    wire cache_read_ready; // DW缓存请求许可
    wire cache_valid; // 注册PW操作数响应
    wire [63:0]cache_data; // 八输入组真实缓存值
    wire [7:0]cache_mask; // 尾四lane置零
    wire [3:0]cache_pixel; // 响应像素身份
    wire cache_group; // 响应组身份
    //-----------------本地事件及地址-----------------//
    wire flag_cancel; // 不把调度器组合故障回接自身
    wire flag_start; // 顶层真实启动
    wire flag_source_begin; // 真正接受源重建命令
    wire flag_source_accept; // 单字节源真实接受
    wire flag_source_index_valid; // 源写不得越界
    wire flag_source_duplicate; // 重复写不得凑完整数量
    wire flag_group_accept; // 本组真实进入核心并推进调度器
    wire flag_write_ready; // 外部和DW缓存原子接收许可
    wire flag_write_accept; // 最终真实外部写接受
    wire flag_task_done; // 当前任务末个有效写事件
    wire [3:0]wire_slot; // DW并集中的当前输入位置
    reg [7:0]wire_halo_offset; // 固定3x5或3x3地址偏移表
    wire [5:0]wire_weight_index; // 紧凑权重ROM地址
    wire [3:0]wire_parameter_index; // 紧凑参数ROM地址
    wire [7:0]wire_output_base; // 4x4x12逻辑通道索引
    wire [15:0]wire_tag_base; // 当前任务第一输出标识
    wire [31:0]wire_address_base; // 冻结图第一输出字节地址
    wire [15:0]wire_tag_step; // DW空间步长12或PW通道步长1
    wire flag_cache_read; // 只有硬件PW请求状态能读缓存
    wire flag_cache_response; // 实际缓存响应消费
    wire flag_adapter_fault; // 有效响应身份必须与请求相同

    // 固定模型初始化；本候选不含通用网络解释器。
    initial begin
        $readmemh(C_WEIGHT_FILE,mem_weight); // 56词来自同一冻结模型
        $readmemh(C_PARAMETER_FILE,mem_parameter); // 16词覆盖本tile两层
    end

    assign flag_cancel = flag_fault || core_fault || cache_fault || i_cancel; // 直接故障源
    assign o_fault = flag_cancel || schedule_fault; // 调度故障只在边界汇总
    assign o_busy = schedule_busy || state_current != ST_IDLE; // 不提前释放源RAM
    assign o_source_begin_ready = i_rstn && !o_busy && !o_fault; // 只在完整退休后重建源
    assign flag_source_begin = i_source_begin && o_source_begin_ready; // 源重建独立于裸脉冲
    assign flag_source_index_valid = i_source_address < 10'd624; // 源存储物理边界
    assign flag_source_duplicate = flag_source_index_valid ? reg_source_written[i_source_address] : 1'b0; // 越界不索引位图
    assign o_source_ready = o_source_begin_ready && !i_source_begin && reg_source_count < 10'd624; // 采集阶段许可
    assign flag_source_accept = i_source_valid && o_source_ready; // 仅握手写入源
    assign o_source_loaded = reg_source_count == 10'd624 && !o_fault && i_rstn; // 最后唯一写之后开放
    assign o_start_ready = schedule_start_ready && o_source_loaded && !i_source_begin && !i_table_valid && state_current == ST_IDLE; // 启动完整合同
    assign flag_start = i_start && o_start_ready; // 一次启动驱动全部160任务
    assign o_table_ready = core_table_ready && !o_busy && !o_fault; // 不与活动任务争共享表
    assign o_table_loaded = core_loaded; // 同一表跨本地tile复用
    assign flag_group_accept = state_current == ST_SEND && schedule_group_valid && core_ready && !o_fault; // 唯一描述符推进事件
    assign flag_write_ready = i_output_ready && (schedule_pw || cache_write_ready) && !o_fault; // DW写两消费者同时许可
    assign o_output_valid = core_valid && (schedule_pw || cache_write_ready) && !o_fault; // 完整写载荷的有效性
    assign flag_write_accept = o_output_valid && i_output_ready; // 不随裸valid计数
    assign flag_task_done = flag_write_accept && core_tag == reg_final_tag; // 最后合法写才允许下一任务
    assign o_output_data = core_data; // 输出真实算术值
    assign o_output_tag = core_tag; // 输出真实任务标识
    assign o_output_address = core_address; // 输出真实地址
    assign o_output_sum = core_sum; // 输出精确和观察值
    assign o_done = schedule_done && !o_fault; // 最后写退休后单拍脉冲
    assign wire_slot = {schedule_last,reg_fetch_lane}; // 两个八输入组
    assign wire_weight_index = schedule_pw ? (6'd48 + {3'd0,schedule_task[1:0],schedule_last}) : {schedule_channel,schedule_x[0],schedule_last}; // 56个权重词覆盖全部320组
    assign wire_parameter_index = schedule_pw ? (4'd12 + {2'd0,schedule_task[1:0]}) : schedule_channel; // 参数按逻辑输出通道复用
    assign wire_output_base = {schedule_y,schedule_x} * 8'd12 + schedule_channel; // 本tileHWC地址
    assign wire_tag_base = schedule_pw ? 16'd192 + wire_output_base : {8'd0,wire_output_base}; // 两层tag空间分离
    assign wire_address_base = schedule_pw ? 32'h03605000 + wire_output_base : 32'h035ea000 + wire_output_base; // 原图地址保持
    assign wire_tag_step = schedule_pw ? 16'd1 : 16'd12; // 通道或空间相邻输出
    assign flag_cache_read = state_current == ST_PW_REQUEST && !o_fault; // 不是TB产生缓存读
    assign flag_cache_response = state_current == ST_PW_WAIT && cache_valid && !o_fault; // 消费同一实际响应
    assign flag_adapter_fault = flag_cache_response && (cache_pixel != {schedule_y,schedule_x} || cache_group != schedule_last || cache_mask != schedule_input_mask); // 响应路由和尾mask核验

    // 固定DW窗口并集偏移，避免每输入重新乘除和多端口源RAM。
    always @(*) begin
        wire_halo_offset = 8'd0; // 无效尾输入不会读取源
        if(schedule_x == 2'd3)begin
            case(wire_slot)
                4'd0:wire_halo_offset = 8'd0;
                4'd1:wire_halo_offset = 8'd12;
                4'd2:wire_halo_offset = 8'd24;
                4'd3:wire_halo_offset = 8'd72;
                4'd4:wire_halo_offset = 8'd84;
                4'd5:wire_halo_offset = 8'd96;
                4'd6:wire_halo_offset = 8'd144;
                4'd7:wire_halo_offset = 8'd156;
                4'd8:wire_halo_offset = 8'd168;
                default:wire_halo_offset = 8'd0;
            endcase
        end else begin
            case(wire_slot)
                4'd0:wire_halo_offset = 8'd0;
                4'd1:wire_halo_offset = 8'd12;
                4'd2:wire_halo_offset = 8'd24;
                4'd3:wire_halo_offset = 8'd36;
                4'd4:wire_halo_offset = 8'd48;
                4'd5:wire_halo_offset = 8'd72;
                4'd6:wire_halo_offset = 8'd84;
                4'd7:wire_halo_offset = 8'd96;
                4'd8:wire_halo_offset = 8'd108;
                4'd9:wire_halo_offset = 8'd120;
                4'd10:wire_halo_offset = 8'd144;
                4'd11:wire_halo_offset = 8'd156;
                4'd12:wire_halo_offset = 8'd168;
                4'd13:wire_halo_offset = 8'd180;
                4'd14:wire_halo_offset = 8'd192;
                default:wire_halo_offset = 8'd0;
            endcase
        end
    end

    // 适配器状态只在本时钟边沿改变。
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)state_current <= ST_IDLE;
        else state_current <= state_next;
    end

    // 下一状态独立处理；组发送后由调度器等待真实写退休。
    always @(*)begin
        state_next = state_current;
        case(state_current)
            ST_IDLE:begin
                if(schedule_group_valid)state_next = ST_PREPARE;
            end
            ST_PREPARE:begin
                if(schedule_pw)state_next = ST_PW_REQUEST;
                else state_next = ST_HALO_ADDRESS;
            end
            ST_HALO_ADDRESS:state_next = ST_HALO_READ;
            ST_HALO_READ:begin
                if(reg_fetch_lane == 3'd7)state_next = ST_SEND;
                else state_next = ST_HALO_ADDRESS;
            end
            ST_PW_REQUEST:begin
                if(cache_read_ready)state_next = ST_PW_WAIT;
            end
            ST_PW_WAIT:begin
                if(cache_valid)begin
                    if(schedule_first)state_next = ST_BYPASS_ADDRESS;
                    else state_next = ST_SEND;
                end
            end
            ST_BYPASS_ADDRESS:state_next = ST_BYPASS_READ;
            ST_BYPASS_READ:begin
                if(reg_fetch_lane == 3'd2)state_next = ST_SEND;
                else state_next = ST_BYPASS_ADDRESS;
            end
            ST_SEND:begin
                if(flag_group_accept)state_next = ST_IDLE;
            end
            default:state_next = ST_IDLE;
        endcase
        if(o_fault)state_next = ST_IDLE;
    end

    // 源位图确保没有用重复/缺失源冒充完整输入。
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            reg_source_count <= 10'd0;
            reg_source_written <= 624'd0;
        end else if(flag_source_begin)begin
            reg_source_count <= 10'd0;
            reg_source_written <= 624'd0;
        end else if(flag_source_accept && flag_source_index_valid && !flag_source_duplicate)begin
            reg_source_count <= reg_source_count + 10'd1;
            reg_source_written[i_source_address] <= 1'b1;
        end
    end

    // 源RAM不复位；读写阶段互斥，避免依赖未证明的碰撞行为。
    always @(posedge i_clk)begin
        if(flag_source_accept && flag_source_index_valid && !flag_source_duplicate)begin
            mem_source[i_source_address] <= i_source_data;
        end
    end

    // 故障不由新start/source_begin清除。
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)flag_fault <= 1'b0;
        else if(i_cancel || flag_adapter_fault || (flag_source_accept && (!flag_source_index_valid || flag_source_duplicate)))flag_fault <= 1'b1;
    end

    // 串行源取数与紧凑ROM读取，只在描述符保持期间执行。
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            reg_weight <= 192'd0;
            reg_parameter <= 248'd0;
            reg_activation <= 64'd0;
            reg_bypass <= 24'd0;
            reg_fetch_lane <= 3'd0;
            reg_source_index <= 10'd0;
            reg_halo_base <= 9'd0;
            reg_output_base <= 8'd0;
            reg_tags <= 48'd0;
            reg_addresses <= 96'd0;
            reg_final_tag <= 16'd0;
        end else if(!o_fault)begin
            if(state_current == ST_PREPARE)begin
                reg_weight <= mem_weight[wire_weight_index];
                reg_parameter <= mem_parameter[wire_parameter_index];
                reg_fetch_lane <= 3'd0;
                reg_halo_base <= schedule_y * 9'd72 + schedule_x * 9'd12 + schedule_channel;
                reg_output_base <= wire_output_base;
                reg_tags[15:0] <= wire_tag_base;
                reg_tags[31:16] <= schedule_mask[1] ? wire_tag_base + wire_tag_step : 16'hffff;
                reg_tags[47:32] <= schedule_mask[2] ? wire_tag_base + wire_tag_step * 16'd2 : 16'hffff;
                reg_addresses[31:0] <= wire_address_base;
                reg_addresses[63:32] <= schedule_mask[1] ? wire_address_base + wire_tag_step : 32'd0;
                reg_addresses[95:64] <= schedule_mask[2] ? wire_address_base + wire_tag_step * 16'd2 : 32'd0;
                if(!schedule_pw)reg_bypass <= 24'd0;
            end
            if(state_current == ST_HALO_ADDRESS)reg_source_index <= reg_halo_base + wire_halo_offset;
            if(state_current == ST_HALO_READ)begin
                reg_activation[reg_fetch_lane*8 +: 8] <= schedule_input_mask[reg_fetch_lane] ? mem_source[reg_source_index] : 8'd0;
                reg_fetch_lane <= reg_fetch_lane + 3'd1;
            end
            if(flag_cache_response)begin
                reg_activation <= cache_data;
                reg_fetch_lane <= 3'd0;
            end
            if(state_current == ST_BYPASS_ADDRESS)reg_source_index <= 10'd432 + reg_output_base + reg_fetch_lane;
            if(state_current == ST_BYPASS_READ)begin
                reg_bypass[reg_fetch_lane*8 +: 8] <= mem_source[reg_source_index];
                reg_fetch_lane <= reg_fetch_lane + 3'd1;
            end
            if(flag_group_accept && schedule_first)begin
                reg_final_tag <= schedule_mask[2] ? reg_tags[47:32] : schedule_mask[1] ? reg_tags[31:16] : reg_tags[15:0];
            end
        end
    end

    //-----------------复用模块-----------------//
    road_csp_tile_schedule schedule_Inst(
        .i_clk(i_clk),.i_rstn(i_rstn),.i_start(flag_start),.i_table_loaded(core_loaded),
        .i_group_ready(flag_group_accept),.i_task_done(flag_task_done),.i_core_fault(flag_cancel),
        .o_start_ready(schedule_start_ready),.o_group_valid(schedule_group_valid),
        .o_first(schedule_first),.o_last(schedule_last),.o_pw(schedule_pw),
        .o_y(schedule_y),.o_x(schedule_x),.o_channel(schedule_channel),.o_output_mask(schedule_mask),
        .o_input_mask(schedule_input_mask),.o_task_index(schedule_task),
        .o_busy(schedule_busy),.o_done(schedule_done),.o_fault(schedule_fault)
    );

    road_csp_dw_cache cache_Inst(
        .i_clk(i_clk),.i_rstn(i_rstn),.i_clear(flag_start),
        .i_write_valid(core_valid && !schedule_pw && i_output_ready && !o_fault),
        .i_write_index(core_tag[7:0]),.i_write_data(core_data),
        .i_read_valid(flag_cache_read),.i_read_pixel({schedule_y,schedule_x}),.i_read_group(schedule_last),
        .i_output_ready(state_current == ST_PW_WAIT && !o_fault),
        .o_write_ready(cache_write_ready),.o_loaded(cache_loaded),.o_write_count(cache_write_count),
        .o_fault(cache_fault),.o_read_ready(cache_read_ready),.o_output_valid(cache_valid),
        .o_output_data(cache_data),.o_output_mask(cache_mask),.o_output_pixel(cache_pixel),.o_output_group(cache_group)
    );

    road_csp_first_probe arithmetic_Inst(
        .i_clk(i_clk),.i_rstn(i_rstn),.i_table_valid(i_table_valid && !o_busy && !o_fault),
        .i_table_addr(i_table_addr),.i_table_data(i_table_data),.o_table_ready(core_table_ready),.o_table_loaded(core_loaded),
        .i_input_valid(state_current == ST_SEND && schedule_group_valid && !o_fault),
        .i_first(schedule_first),.i_last(schedule_last),.i_lane_mask(schedule_input_mask),
        .i_activation_data(reg_activation),.i_weight_data(reg_weight),
        .i_bias_data({schedule_mask[2] ? reg_parameter[95:64] : 32'd0,schedule_mask[1] ? reg_parameter[63:32] : 32'd0,reg_parameter[31:0]}),
        .i_output_mask(schedule_mask),.i_tags(reg_tags),.i_addresses(reg_addresses),
        .i_pre_multipliers({schedule_mask[2] ? reg_parameter[191:160] : 32'd0,schedule_mask[1] ? reg_parameter[159:128] : 32'd0,reg_parameter[127:96]}),
        .i_pre_shifts({schedule_mask[2] ? reg_parameter[209:204] : 6'd0,schedule_mask[1] ? reg_parameter[203:198] : 6'd0,reg_parameter[197:192]}),
        .i_post_multiplier(reg_parameter[241:210]),.i_post_shift(reg_parameter[247:242]),
        .i_residual(schedule_pw),.i_bypass_data(reg_bypass),.i_input_fault(1'b0),.i_output_ready(flag_write_ready),
        .o_input_ready(core_ready),.o_output_valid(core_valid),.o_output_data(core_data),
        .o_output_tag(core_tag),.o_output_address(core_address),.o_output_sum(core_sum),.o_fault(core_fault)
    );
endmodule
