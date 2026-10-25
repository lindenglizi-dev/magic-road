`timescale 1ns / 1ps
////////////////////////////////////English///////////////////////////////////////
// Company: RoadYOLO
// Engineer: Codex
// Create Date: 2026-10-15
// Design Name: Complete CSP tile peripheral client
// Module Name: road_csp_complete_client
// Description: road_csp_complete_client_spec.md
// Simulations: tb_csp_complete_client
// Referrences: Frozen CSP graph and same-package integer reference
// Dependencies: External single arithmetic owner, parameter reader and memory service
// Version: V1.0
// Revision Date: 2026-10-15
// History: 2026-10-15 V1.0 Codex Create file
///////////////////////////////////Chinese////////////////////////////////////////
// 版权归属: RoadYOLO
// 开发人员: Codex
// 创建日期: 2026-10-15
// 设计名称: 完整CSP块外围客户
// 模块名称: road_csp_complete_client
// 模块说明: 两次半通道残差及末端融合，不私有实例化算术核
// 仿真工程: tb_csp_complete_client
// 参考资料: 冻结图及同包整数参考
// 依赖文件: 外部唯一算术owner、参数读取与逻辑字节内存服务
// 当前版本: V1.0
// 修订日期: 2026-10-15
// 修订历史: 2026-10-15 V1.0 Codex 创建独立外围候选
module road_csp_complete_client(
    input i_clk, // 与算术owner同域100MHz
    input i_rstn, // 共同复位，外部服务须同时取消旧响应
    input i_start, // ready时接受一个固定图tile
    input [6:0]i_tile_y, // 0至68且四对齐
    input [7:0]i_tile_x, // 0至124且四对齐
    input i_cancel, // 取消后不释放外部存储，需共同复位
    input i_table_loaded, // 外部owner已有同包完整SiLU表
    output o_start_ready, // 空闲且表有效才接任务
    output o_busy, // 故障时保持占有，不冒充排空
    output o_done, // 末层可见性确认后一拍完成
    output o_fault, // 粘滞协议错误
    output [2:0]o_layer, // 当前五个卷积阶段
    output o_parameter_valid, // 一组参数读取请求
    output [4:0]o_parameter_channel, // DW通道或PW三输出起点
    output [1:0]o_parameter_group, // 八输入组编号
    output [2:0]o_parameter_window, // DW并集宽3或5；PW为0
    input i_parameter_ready, // 请求真实被参数服务接受
    input i_parameter_response_valid, // 注册参数响应，保持至response_ready
    output o_parameter_response_ready, // 仅等待本请求时消费
    input [2:0]i_parameter_response_layer, // 响应阶段身份
    input [4:0]i_parameter_response_channel, // 响应输出通道身份
    input [1:0]i_parameter_response_group, // 响应归约组身份
    input [2:0]i_parameter_response_window, // 响应DW窗口形态
    input [191:0]i_parameter_weight, // OIHW映射到三路八输入
    input [247:0]i_parameter_data, // 原bias/pre/post字段紧凑排列
    input i_parameter_error, // 外部参数读取故障
    output o_read_valid, // 单个逻辑字节读请求
    output [31:0]o_read_address, // 冻结graph逻辑字节，非native地址
    input i_read_ready, // 服务接受请求，不代表响应已到
    input i_read_response_valid, // 一次请求对应一次注册响应
    output o_read_response_ready, // 不接受其它任务旧响应
    input [31:0]i_read_response_address, // 与请求绑定的字节地址
    input [7:0]i_read_response_data, // 真正读取的INT8字节
    input i_read_error, // 服务显式读错误
    output o_write_valid, // 合法算术结果才向外发布
    output [31:0]o_write_address, // 本次真实写地址
    output [7:0]o_write_data, // 融合后sat8值
    output signed [8:0]o_write_sum, // 饱和前精确残差和
    input i_write_ready, // 写服务接受，尚不等于可见
    output o_barrier_valid, // 本阶段全部写接受后请求可见性屏障
    input i_barrier_ready, // 明确保证此前写可供后续读消费
    input [2:0]i_barrier_layer, // 屏障所属阶段，不能承认旧层ack
    output o_core_valid, // 原算术核组valid
    input i_core_ready, // 原算术核输入组ready
    output o_core_first, // 原接口首组语义不变
    output o_core_last, // 原接口末组语义不变
    output [7:0]o_core_input_mask, // 八输入尾mask
    output [63:0]o_core_activation, // 原64位INT8输入
    output [191:0]o_core_weight, // 原192位权重
    output [95:0]o_core_bias, // first只加一次的三路bias
    output [2:0]o_core_output_mask, // 图边界或三空间点尾路
    output [47:0]o_core_tags, // 单任务lane身份0/1/2
    output [95:0]o_core_addresses, // 三路完整真实字节地址
    output [95:0]o_core_pre_multiplier, // 三路原pre乘数
    output [17:0]o_core_pre_shift, // 三路六位pre移位
    output [31:0]o_core_post_multiplier, // 当前层共享post乘数
    output [5:0]o_core_post_shift, // 当前层共享post移位
    output o_core_residual, // 两个PW阶段才做旁路融合
    output [23:0]o_core_bypass, // 对应三输出的真实旁路
    input i_core_output_valid, // 原五级写回发布结果
    output o_core_output_ready, // 合法结果与外部写原子接受
    input [15:0]i_core_output_tag, // 原核返回任务lane
    input [31:0]i_core_output_address, // 原核返回完整地址
    input [7:0]i_core_output_data, // 原核sat8输出
    input signed [8:0]i_core_output_sum, // 原核signed9和
    input i_core_fault // 原核错误，不修改其故障语义
);
    //-----------------状态参数区域-----------------//
    localparam [3:0]ST_IDLE=0; // 等待有完整表的tile
    localparam [3:0]ST_SETUP=1; // 注册任务坐标和有效路
    localparam [3:0]ST_PARAMETER=2; // 保持参数请求至接受
    localparam [3:0]ST_PARAMETER_WAIT=3; // 等待匹配参数响应
    localparam [3:0]ST_FETCH=4; // 注册下一源字节地址
    localparam [3:0]ST_READ=5; // 单一未完成读请求
    localparam [3:0]ST_READ_WAIT=6; // 等待匹配读返回
    localparam [3:0]ST_FETCH_NEXT=7; // 推进输入槽或切换旁路读取
    localparam [3:0]ST_SEND=8; // 整组保持至原核接受
    localparam [3:0]ST_WRITE_WAIT=9; // 等待所有真实结果写接受
    localparam [3:0]ST_RETIRE=10; // 消费注册末次写凭据
    localparam [3:0]ST_ADVANCE=11; // 推进任务或请求层屏障
    localparam [3:0]ST_BARRIER=12; // 等待真实写可见性确认
    localparam [3:0]ST_FINISH=13; // 完整块结束，不保留旧完成位
    localparam [3:0]ST_FAULT=14; // 不释放故障所有权
    //-----------------状态机信号-----------------//
    reg [3:0]state_current; // 当前外围阶段
    reg [3:0]state_next; // 独立下一状态过程
    //-----------------寄存器信号-----------------//
    reg [6:0]reg_origin_y; // 本tile全图行起点
    reg [7:0]reg_origin_x; // 本tile全图列起点
    reg [2:0]reg_layer; // 固定图五卷积阶段
    reg [2:0]reg_row; // 第一残差六行，后续四行
    reg [2:0]reg_column; // DW三点起始或PW单像素
    reg [4:0]reg_channel; // DW单通道或PW三通道起点
    reg [1:0]reg_group; // 当前八输入归约组
    reg [2:0]reg_fetch_lane; // 逐字节取数槽
    reg flag_bypass; // 当前读取的是残差旁路
    reg [2:0]reg_output_mask; // 当前任务有效输出路
    reg [2:0]reg_written; // 当前任务已经实际写出的路
    reg [95:0]reg_addresses; // 首组冻结三路写地址
    reg [63:0]reg_activation; // 当前组拼装的输入
    reg [23:0]reg_bypass; // 首组取得的旁路值
    reg [191:0]reg_weight; // 参数响应后的驻留权重
    reg [247:0]reg_parameter; // 当前任务的量化字段
    reg [31:0]reg_read_address; // 请求保持期间不重新计算
    reg flag_task_done; // 末次实际写后一拍退休凭据
    reg flag_fault; // 协议失败只能共同复位清除
    //-----------------其他信号-----------------//
    wire flag_dw; // 两个深度卷积阶段
    wire flag_residual; // 两个融合残差PW阶段
    wire [2:0]wire_extent; // 当前阶段输出区域边长
    wire [2:0]wire_window; // DW并集宽度
    wire [4:0]wire_inputs; // 本任务实际输入数
    wire [1:0]wire_last_group; // 归约末组编号
    wire [7:0]wire_input_mask; // 末组低四或低一lane有效
    wire flag_parameter_accept; // 匹配参数响应真实消费
    wire flag_read_accept; // 匹配字节响应真实消费
    wire flag_core_accept; // 原核组真实接受
    wire flag_write_legal; // 路身份、地址和唯一性核对
    wire flag_write_accept; // 最终外部写接受
    wire [2:0]wire_write_lane; // 返回tag的onehot形式
    wire flag_last_write; // 当前任务最后合法写
    wire flag_task_last; // 当前层最后坐标和通道
    wire flag_bad_parameter; // 错路由或组间参数漂移
    wire flag_bad_read; // 读服务错误或错地址
    wire flag_bad_write; // 未拥有、重复或错地址结果
    integer dec_y; // 可表示负邻域的全图行
    integer dec_x; // 可表示负邻域的全图列
    integer dec_lane; // 当前固定三路展开索引
    integer dec_slot; // 当前实际输入编号
    integer dec_source_y; // 本次读取的真实源行
    integer dec_source_x; // 本次读取的真实源列
    integer dec_source_channel; // split/concat之后的物理通道
    integer dec_source_channels; // 物理源存储通道数
    reg [31:0]dec_source_base; // 冻结图对应分配基址
    reg [31:0]dec_output_base; // 当前层写分配基址
    reg [2:0]dec_mask; // 只选择真实图内有效输出
    reg [95:0]dec_addresses; // 当前任务三路图地址
    reg [31:0]dec_read_address; // 图tile4x4_hwc地址
    reg flag_padding; // 无效输入不得发外部读

    //-----------------其他信号连线-----------------//
    assign flag_dw = reg_layer==0 || reg_layer==2; // 第一及第二DW
    assign flag_residual = reg_layer==1 || reg_layer==3; // 同尺度残差相加
    assign wire_extent = reg_layer<2 ? 3'd6 : 3'd4; // 为第二DW先生成六乘六真邻域
    assign wire_window = flag_dw ? ((wire_extent-reg_column)>=3 ? 3'd5 : 3'd3) : 3'd0; // 三输出并集或尾一输出并集
    assign wire_inputs = flag_dw ? wire_window*3 : (reg_layer==4 ? 5'd24 : 5'd12); // 不改变输入分组宽度
    assign wire_last_group = reg_layer==4 ? 2'd2 : 2'd1; // PW融合24输入为三组
    assign wire_input_mask = wire_inputs-reg_group*8>=8 ? 8'hff : ((8'h01 << (wire_inputs-reg_group*8))-1'b1); // 尾组只消费真实输入
    assign wire_write_lane = i_core_output_tag==0 ? 3'b001 : i_core_output_tag==1 ? 3'b010 : i_core_output_tag==2 ? 3'b100 : 3'd0; // 固定lane身份范围
    assign flag_write_legal = wire_write_lane!=0 && (wire_write_lane & reg_output_mask)!=0 && (wire_write_lane & reg_written)==0 &&
        (i_core_output_address==(i_core_output_tag==0 ? reg_addresses[31:0] : i_core_output_tag==1 ? reg_addresses[63:32] : reg_addresses[95:64])); // 不允许错地址或重复写进入外部
    assign flag_write_accept = o_write_valid && i_write_ready; // 与原核退休同一接受事件
    assign flag_last_write = flag_write_accept && ((reg_written | wire_write_lane)==reg_output_mask); // 不用裸valid结束
    assign flag_task_last = reg_row==wire_extent-1 && (flag_dw ? reg_column==3 : reg_column==wire_extent-1) &&
        reg_channel==(flag_dw ? 11 : reg_layer==4 ? 21 : 9); // 固定形状最后任务
    assign flag_parameter_accept = i_parameter_response_valid && o_parameter_response_ready; // 参数返回只消费一次
    assign flag_read_accept = i_read_response_valid && o_read_response_ready; // 字节返回只消费一次
    assign flag_core_accept = o_core_valid && i_core_ready; // 只在原核ready时推进归约
    assign flag_bad_parameter = flag_parameter_accept && (i_parameter_error || i_parameter_response_layer!=reg_layer ||
        i_parameter_response_channel!=reg_channel || i_parameter_response_group!=reg_group || i_parameter_response_window!=wire_window ||
        (reg_group!=0 && i_parameter_data!=reg_parameter)); // 同任务参数一致且路由匹配
    assign flag_bad_read = flag_read_accept && (i_read_error || i_read_response_address!=reg_read_address); // 明确读错误不变成背景零
    assign flag_bad_write = i_core_output_valid && (state_current!=ST_WRITE_WAIT || !flag_write_legal); // 原核多余或旧结果粘滞拒绝

    //-----------------输出信号连线-----------------//
    assign o_start_ready = state_current==ST_IDLE && i_rstn && i_table_loaded && !o_fault; // 完整表及空闲合同
    assign o_busy = state_current!=ST_IDLE; // 故障不声称owner已排空
    assign o_done = state_current==ST_FINISH && !o_fault; // 末层屏障已确认
    assign o_fault = flag_fault || i_core_fault || i_cancel; // 原算术错误立即阻止提交
    assign o_layer = reg_layer; // 请求与写身份均绑定当前阶段
    assign o_parameter_valid = state_current==ST_PARAMETER && !o_fault; // 等待ready期间元数据不变
    assign o_parameter_channel = reg_channel; // 参数从冻结输出通道索引
    assign o_parameter_group = reg_group; // 参数权重当前八输入分片
    assign o_parameter_window = wire_window; // DW空间打包形态明确交接
    assign o_parameter_response_ready = state_current==ST_PARAMETER_WAIT && !o_fault; // 不接受未请求参数
    assign o_read_valid = state_current==ST_READ && !o_fault; // 最多一个未完成读
    assign o_read_address = reg_read_address; // 请求和响应核对同一地址
    assign o_read_response_ready = state_current==ST_READ_WAIT && !o_fault; // 响应消费受状态保护
    assign o_write_valid = state_current==ST_WRITE_WAIT && i_core_output_valid && flag_write_legal && !o_fault; // 错误结果不对外写
    assign o_write_address = i_core_output_address; // 原五级写回冻结地址
    assign o_write_data = i_core_output_data; // 原核融合sat8值
    assign o_write_sum = i_core_output_sum; // 原核signed9观测
    assign o_barrier_valid = state_current==ST_BARRIER && !o_fault; // 写接受与可见性严格分离
    assign o_core_valid = state_current==ST_SEND && !o_fault; // 整组固定至接受
    assign o_core_first = reg_group==0; // 仅首组锁存元数据
    assign o_core_last = reg_group==wire_last_group; // 末组关闭归约
    assign o_core_input_mask = wire_input_mask; // 原核八输入尾mask
    assign o_core_activation = reg_activation; // 已注册读响应拼装值
    assign o_core_weight = {reg_output_mask[2] ? reg_weight[191:128] : 64'd0,reg_output_mask[1] ? reg_weight[127:64] : 64'd0,reg_output_mask[0] ? reg_weight[63:0] : 64'd0}; // 无效输出路全零保留原子溢出语义
    assign o_core_bias = {reg_output_mask[2] ? reg_parameter[95:64] : 32'd0,reg_output_mask[1] ? reg_parameter[63:32] : 32'd0,reg_output_mask[0] ? reg_parameter[31:0] : 32'd0}; // 图外路不引入偏置
    assign o_core_output_mask = reg_output_mask; // 当前任务固定有效路
    assign o_core_tags = 48'h000200010000; // 原核元数据仍为不透明tag
    assign o_core_addresses = reg_addresses; // 当前任务固定完整地址
    assign o_core_pre_multiplier = {reg_output_mask[2] ? reg_parameter[191:160] : 32'd0,reg_output_mask[1] ? reg_parameter[159:128] : 32'd0,reg_output_mask[0] ? reg_parameter[127:96] : 32'd0}; // 图外量化路清零
    assign o_core_pre_shift = {reg_output_mask[2] ? reg_parameter[209:204] : 6'd0,reg_output_mask[1] ? reg_parameter[203:198] : 6'd0,reg_output_mask[0] ? reg_parameter[197:192] : 6'd0}; // 移位与对应通道绑定
    assign o_core_post_multiplier = reg_parameter[241:210]; // 当前层共享后乘数
    assign o_core_post_shift = reg_parameter[247:242]; // 当前层共享后移位
    assign o_core_residual = flag_residual; // 其它卷积不执行旁路求和
    assign o_core_bypass = reg_bypass; // 旁路读自真实源而非黄金值
    assign o_core_output_ready = state_current==ST_WRITE_WAIT && i_write_ready && flag_write_legal && !o_fault; // 两个消费者一致接受

    // 只对真实全幅图像外补零；图内坐标一律交给内存服务读取。
    // ponytail: 单字节串行服务先证功能；性能不足时由唯一DDR owner接16B缓存，不另造桥。
    always @(*)begin
        dec_y=reg_origin_y+reg_row-(reg_layer<2 ? 1 : 0);
        dec_x=reg_origin_x+reg_column-(reg_layer<2 ? 1 : 0);
        dec_mask=0;
        dec_addresses=0;
        case(reg_layer)
            0:dec_output_base=32'h035ea000;
            1:dec_output_base=32'h03605000;
            2:dec_output_base=32'h03620000;
            3:dec_output_base=32'h0363b000;
            default:dec_output_base=32'h03656000;
        endcase
        for(dec_lane=0;dec_lane<3;dec_lane=dec_lane+1)begin
            if(dec_y>=0 && dec_y<72 && dec_x+(flag_dw ? dec_lane : 0)>=0 && dec_x+(flag_dw ? dec_lane : 0)<128 &&
                (!flag_dw || reg_column+dec_lane<wire_extent))begin
                dec_mask[dec_lane]=1'b1;
                dec_addresses[dec_lane*32 +: 32]=dec_output_base+
                    (((dec_y/4)*32+(dec_x+(flag_dw ? dec_lane : 0))/4)*16+(dec_y%4)*4+(dec_x+(flag_dw ? dec_lane : 0))%4)*
                    (reg_layer==4 ? 24 : 12)+reg_channel+(flag_dw ? 0 : dec_lane);
            end
        end
        dec_slot=reg_group*8+reg_fetch_lane;
        dec_source_y=dec_y;
        dec_source_x=dec_x;
        dec_source_channel=dec_slot;
        dec_source_channels=12;
        dec_source_base=32'h035ea000;
        if(flag_bypass)begin
            dec_source_channel=reg_channel+reg_fetch_lane;
            if(reg_layer==1)begin
                dec_source_base=32'h035b4000;
                dec_source_channels=24;
                dec_source_channel=dec_source_channel+12;
            end else begin
                dec_source_base=32'h03605000;
            end
        end else if(flag_dw)begin
            dec_source_y=dec_y-1+dec_slot/wire_window;
            dec_source_x=dec_x-1+dec_slot%wire_window;
            dec_source_channel=reg_channel;
            if(reg_layer==0)begin
                dec_source_base=32'h035b4000;
                dec_source_channels=24;
                dec_source_channel=dec_source_channel+12;
            end else begin
                dec_source_base=32'h03605000;
            end
        end else if(reg_layer==3)begin
            dec_source_base=32'h03620000;
        end else if(reg_layer==4)begin
            if(dec_slot<12)begin
                dec_source_base=32'h035b4000;
                dec_source_channels=24;
            end else begin
                dec_source_base=32'h0363b000;
                dec_source_channel=dec_slot-12;
            end
        end
        flag_padding=dec_source_y<0 || dec_source_y>=72 || dec_source_x<0 || dec_source_x>=128 ||
            (!flag_bypass && dec_slot>=wire_inputs) || (flag_bypass && !reg_output_mask[reg_fetch_lane]);
        dec_read_address=0;
        if(!flag_padding)begin
            dec_read_address=dec_source_base+(((dec_source_y/4)*32+dec_source_x/4)*16+(dec_source_y%4)*4+dec_source_x%4)*dec_source_channels+dec_source_channel;
        end
    end

    // 状态寄存器独立于控制任务，错误进入占有状态直到共同复位。
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)state_current<=ST_IDLE;
        else state_current<=state_next;
    end

    // 下一状态只使用已经注册的任务与事件，不反馈末次写组合完成。
    always @(*)begin
        state_next=state_current;
        case(state_current)
            ST_IDLE:if(i_start && o_start_ready)state_next=ST_SETUP;
            ST_SETUP:if(dec_mask==0)state_next=ST_ADVANCE; else state_next=ST_PARAMETER;
            ST_PARAMETER:if(i_parameter_ready)state_next=ST_PARAMETER_WAIT;
            ST_PARAMETER_WAIT:if(flag_parameter_accept)state_next=ST_FETCH;
            ST_FETCH:if(flag_padding)state_next=ST_FETCH_NEXT; else state_next=ST_READ;
            ST_READ:if(i_read_ready)state_next=ST_READ_WAIT;
            ST_READ_WAIT:if(flag_read_accept)state_next=ST_FETCH_NEXT;
            ST_FETCH_NEXT:if((!flag_bypass && reg_fetch_lane==7) || (flag_bypass && reg_fetch_lane==2))begin
                if(!flag_bypass && flag_residual && reg_group==0)state_next=ST_FETCH;
                else state_next=ST_SEND;
            end else state_next=ST_FETCH;
            ST_SEND:if(flag_core_accept)begin
                if(o_core_last)state_next=ST_WRITE_WAIT;
                else state_next=ST_PARAMETER;
            end
            ST_WRITE_WAIT:if(flag_last_write)state_next=ST_RETIRE;
            ST_RETIRE:if(flag_task_done)state_next=ST_ADVANCE;
            ST_ADVANCE:if(flag_task_last)state_next=ST_BARRIER; else state_next=ST_SETUP;
            ST_BARRIER:if(i_barrier_ready)begin
                if(reg_layer==4)state_next=ST_FINISH;
                else state_next=ST_SETUP;
            end
            ST_FINISH:state_next=ST_IDLE;
            ST_FAULT:state_next=ST_FAULT;
            default:state_next=ST_FAULT;
        endcase
        if(o_fault)state_next=ST_FAULT;
    end

    // 末次外部写事件注册一拍，与原有效候选的task_done语义一致。
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)flag_task_done<=1'b0;
        else flag_task_done<=flag_last_write;
    end

    // 仅明确信任边界错误置位；不自动恢复或释放取消任务存储。
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)flag_fault<=1'b0;
        else if(i_cancel || i_core_fault || flag_bad_parameter || flag_bad_read || flag_bad_write ||
            (i_start && o_start_ready && (i_tile_y>68 || i_tile_x>124 || i_tile_y[1:0]!=0 || i_tile_x[1:0]!=0)) ||
            (o_barrier_valid && i_barrier_ready && i_barrier_layer!=reg_layer))flag_fault<=1'b1;
    end

    // 有界五阶段遍历；源、参数和写回只随真实握手推进。
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            reg_origin_y<=0; reg_origin_x<=0; reg_layer<=0; reg_row<=0; reg_column<=0; reg_channel<=0;
            reg_group<=0; reg_fetch_lane<=0; flag_bypass<=0; reg_output_mask<=0; reg_written<=0;
            reg_addresses<=0; reg_activation<=0; reg_bypass<=0; reg_weight<=0; reg_parameter<=0;
            reg_read_address<=0;
        end else if(!o_fault)begin
            if(i_start && o_start_ready)begin
                reg_origin_y<=i_tile_y; reg_origin_x<=i_tile_x; reg_layer<=0; reg_row<=0; reg_column<=0; reg_channel<=0;
            end
            if(state_current==ST_SETUP)begin
                reg_output_mask<=dec_mask; reg_addresses<=dec_addresses; reg_written<=0; reg_group<=0;
                reg_fetch_lane<=0; flag_bypass<=0; reg_activation<=0; reg_bypass<=0;
            end
            if(flag_parameter_accept && !flag_bad_parameter)begin
                reg_weight<=i_parameter_weight; reg_parameter<=i_parameter_data;
                reg_fetch_lane<=0; flag_bypass<=0; reg_activation<=0;
            end
            if(state_current==ST_FETCH)begin
                reg_read_address<=dec_read_address;
                if(flag_padding)begin
                    if(flag_bypass)reg_bypass[reg_fetch_lane*8 +: 8]<=0;
                    else reg_activation[reg_fetch_lane*8 +: 8]<=0;
                end
            end
            if(flag_read_accept && !flag_bad_read)begin
                if(flag_bypass)reg_bypass[reg_fetch_lane*8 +: 8]<=i_read_response_data;
                else reg_activation[reg_fetch_lane*8 +: 8]<=i_read_response_data;
            end
            if(state_current==ST_FETCH_NEXT)begin
                if(!flag_bypass && reg_fetch_lane==7 && flag_residual && reg_group==0)begin
                    flag_bypass<=1'b1; reg_fetch_lane<=0;
                end else reg_fetch_lane<=reg_fetch_lane+1'b1;
            end
            if(flag_core_accept && !o_core_last)reg_group<=reg_group+1'b1;
            if(flag_write_accept)reg_written<=reg_written | wire_write_lane;
            if(state_current==ST_ADVANCE && !flag_task_last)begin
                if(reg_channel==(flag_dw ? 11 : reg_layer==4 ? 21 : 9))begin
                    reg_channel<=0;
                    if(flag_dw ? reg_column==3 : reg_column==wire_extent-1)begin
                        reg_column<=0; reg_row<=reg_row+1'b1;
                    end else reg_column<=reg_column+(flag_dw ? 3 : 1);
                end else reg_channel<=reg_channel+(flag_dw ? 1 : 3);
            end
            if(o_barrier_valid && i_barrier_ready && i_barrier_layer==reg_layer && reg_layer!=4)begin
                reg_layer<=reg_layer+1'b1; reg_row<=0; reg_column<=0; reg_channel<=0;
            end
        end
    end
endmodule
