`timescale 1ns / 1ps
// Company: User project
// Engineer: Codex
// Create Date: 2026-10-20
// Design Name: Marked ball rotation
// Module Name: ball_marker_extract
// Description: Same-frame median threshold and bounded four-connected dark marker extraction
// Simulations: sim/tb_ball_rotation_image.v
// Referrences: E:/project/ball/fpga/applications/ball_rotation/python_sim/rotation_rtl_model.py
// Dependencies: same-clock synchronous memories
// Version: V1.0
// Revision Date: 2026-10-20
// History: V1.0 Create file
// 版权归属: 用户工程
// 开发人员: Codex
// 创建日期: 2026-10-20
// 设计名称: 带标记小球旋转
// 模块名称: ball_marker_extract
// 模块说明: Same-frame median threshold and bounded four-connected dark marker extraction
// 仿真工程: sim/tb_ball_rotation_image.v
// 参考资料: E:/project/ball/fpga/applications/ball_rotation/python_sim/rotation_rtl_model.py
// 依赖文件: 同时钟同步存储
// 当前版本: V1.0
// 修订日期: 2026-10-20
// 修订历史: V1.0 创建文件
module ball_marker_extract #(
    parameter C_X_MIN=64,C_Y_MIN=160,C_X_END=1216,C_Y_END=640, C_QUEUE_BITS=9 // 完整球体检测边界与队列容量。
)(
    input i_clk, // 灰度统计时钟
    input i_rstn, // 异步低有效复位
    input i_clear, // 撤销当前黑点提取
    input i_start, // 空闲时提交已冻结bank
    input [12-1:0] i_origin_x, // 采集窗左边界
    input [12-1:0] i_origin_y, // 采集窗上边界
    input [12-1:0] i_left, // 同帧实测球框左边界
    input [12-1:0] i_right, // 同帧实测球框右边界
    input [12-1:0] i_top, // 同帧实测球框上边界
    input [12-1:0] i_bottom, // 同帧实测球框下边界
    input [16-1:0] i_read_data, // 同步灰度读返回值
    output o_read, // 同步灰度读请求
    output [13-1:0] o_read_address, // 灰度双单元字地址
    output o_busy, // 正在处理冻结bank
    output o_done, // 黑点提取结束
    output o_valid, // 恰好识别出一个合格黑点
    output [4-1:0] o_reason, // 裁切几何窗口队列或标记错误
    output [16-1:0] o_center_x, // Q4实测球心横坐标
    output [16-1:0] o_center_y, // Q4实测球心纵坐标
    output [16-1:0] o_marker_x, // Q4黑点横坐标
    output [16-1:0] o_marker_y, // Q4黑点纵坐标
    output [8-1:0] o_median, // 本帧内圆低中位灰度
    output [8-1:0] o_threshold // 本帧黑点阈值
);
    localparam ST_IDLE=0;
    localparam ST_GEOMETRY=1;
    localparam ST_RADIUS=2;
    localparam ST_LIMITS=3;
    localparam ST_MAXIMUM=4;
    localparam ST_MAXIMUM_WAIT=5;
    localparam ST_HISTOGRAM_CLEAR=6;
    localparam ST_READ=7;
    localparam ST_LOAD=8;
    localparam ST_POSITION=9;
    localparam ST_SQUARE=10;
    localparam ST_INSIDE=11;
    localparam ST_CHECK=12;
    localparam ST_HISTOGRAM_READ=13;
    localparam ST_HISTOGRAM_WRITE=14;
    localparam ST_ADVANCE=15;
    localparam ST_MEDIAN_READ=16;
    localparam ST_MEDIAN_CHECK=17;
    localparam ST_DARK_SCAN=18;
    localparam ST_ENQUEUE=19;
    localparam ST_POP_TEST=20;
    localparam ST_POP_READ=21;
    localparam ST_POP_LOAD=22;
    localparam ST_NODE=23;
    localparam ST_NEIGHBOR=24;
    localparam ST_NEIGHBOR_TEST=25;
    localparam ST_NEIGHBOR_NEXT=26;
    localparam ST_AREA=27;
    localparam ST_AREA_CHECK=28;
    localparam ST_CENTROID_X=29;
    localparam ST_CENTROID_X_WAIT=30;
    localparam ST_CENTROID_Y=31;
    localparam ST_CENTROID_Y_WAIT=32;
    localparam ST_OFFSET=33;
    localparam ST_OFFSET_SQUARE=34;
    localparam ST_FILTER=35;
    localparam ST_ACCEPT=36;
    localparam ST_FINISH=37;
    localparam ST_CLIPPED=38;
    localparam ST_GEOMETRY_BAD=39;
    localparam ST_WINDOW_BAD=40;
    localparam ST_QUEUE_BAD=41;
    localparam ST_MULTIPLE=42;
    localparam ST_DONE=43;
    reg [5:0] state_current,state_next;
    reg [11:0] reg_origin_x,reg_origin_y,reg_left,reg_right,reg_top,reg_bottom;
    reg [12:0] reg_width,reg_height;
    reg [15:0] reg_center_x_o,reg_center_y_o,reg_marker_x_o,reg_marker_y_o;
    reg [15:0] reg_radius,reg_inner,reg_offset_low,reg_offset_high;
    reg [31:0] reg_radius_square,reg_inner_square,reg_offset_low_square,reg_offset_high_square;
    reg [3:0] reg_minimum_area,reg_reason_o;
    reg [31:0] reg_maximum_area;
    reg [13:0] cnt_scan,reg_address,reg_node;
    reg flag_histogram,flag_neighbor,flag_inside,flag_neighbor_valid;
    reg [7:0] reg_pixel,reg_median_o,reg_threshold_o,cnt_gray;
    reg signed [15:0] reg_dx,reg_dy;
    reg [31:0] reg_square_x,reg_square_y;
    reg [14:0] mem_histogram[0:255];
    reg [14:0] reg_histogram_data,cnt_total;
    reg [15:0] reg_cumulative;
    wire flag_visited;
    reg [C_QUEUE_BITS-1:0] cnt_head,cnt_tail;
    reg [C_QUEUE_BITS:0] cnt_queue;
    reg [14:0] cnt_area;
    reg [16:0] reg_area;
    reg [31:0] reg_sum_x,reg_sum_y,reg_box_area;
    reg [6:0] reg_min_column,reg_max_column,reg_min_row,reg_max_row;
    reg [8:0] reg_component_width,reg_component_height;
    reg [15:0] reg_marker_x,reg_marker_y;
    reg [1:0] cnt_direction,cnt_markers;
    reg [13:0] dec_neighbor_address;
    reg dec_neighbor_valid;
    reg flag_valid_o,flag_done_o;
    reg [31:0] reg_math_left,reg_math_right;
    reg flag_math_round,flag_math_start;
    wire flag_math_done;
    wire [31:0] wire_math_result;
    wire [13:0] wire_queue_data;
    wire [15:0] wire_global_x={reg_origin_x,4'd0}+{4'd0,reg_address[6:0],5'd8};
    wire [15:0] wire_global_y={reg_origin_y,4'd0}+{4'd0,reg_address[13:7],5'd8};
    wire [31:0] wire_inner_product=(({16'd0,reg_radius} << 8)-({16'd0,reg_radius} << 5))-(({16'd0,reg_radius} << 3)-{16'd0,reg_radius});
    wire [31:0] wire_low_product=(({16'd0,reg_radius} << 5)+({16'd0,reg_radius} << 4))+(({16'd0,reg_radius} << 1)+{16'd0,reg_radius});
    wire [31:0] wire_high_product=({16'd0,reg_radius} << 7)+(({16'd0,reg_radius} << 6)+({16'd0,reg_radius} << 3));
    wire [15:0] wire_cumulative=reg_cumulative+{1'b0,reg_histogram_data};
    wire [15:0] wire_threshold_product=(({8'd0,cnt_gray} << 7)-({8'd0,cnt_gray} << 4))+(({8'd0,cnt_gray} << 1)+{8'd0,cnt_gray});
    wire [31:0] wire_offset=reg_square_x+reg_square_y;
    wire [31:0] wire_area_hundred=(({15'd0,reg_area} << 6)+({15'd0,reg_area} << 5))+({15'd0,reg_area} << 2);
    wire [31:0] wire_box_thirtyfive=({16'd0,reg_box_area} << 5)+(({16'd0,reg_box_area} << 1)+{16'd0,reg_box_area});
    wire flag_histogram_read=state_current == ST_HISTOGRAM_READ || state_current == ST_MEDIAN_READ;
    wire [7:0] wire_histogram_address=state_current == ST_HISTOGRAM_READ ? reg_pixel : cnt_gray;
    wire flag_queue_write=state_current == ST_ENQUEUE;
    wire [C_QUEUE_BITS-1:0] wire_queue_address=flag_neighbor ? cnt_tail : {C_QUEUE_BITS{1'b0}};
    ball_rotation_arithmetic #(.C_BITS(32)) centroid_Inst(
        .i_clk(i_clk),.i_rstn(i_rstn),.i_clear(i_clear),.i_start(flag_math_start),.i_divide(1'b1),
        .i_round(flag_math_round),.i_left(reg_math_left),.i_right(reg_math_right),
        .o_busy(),.o_done(flag_math_done),.o_error(),.o_result(wire_math_result));
    ball_component_store #(.C_DEPTH(1 << C_QUEUE_BITS),.C_ADDR_BITS(C_QUEUE_BITS),.C_DATA_BITS(14)) queue_Inst(
        .i_clk(i_clk),.i_read_enable(state_current == ST_POP_READ),.i_read_address(cnt_head),
        .i_write_enable(flag_queue_write && !i_clear),.i_write_address(wire_queue_address),
        .i_write_data(reg_address),.o_read_data(wire_queue_data));
    // 复用工程的同步简单双端口模板；清零和读取互斥，避免安路写模式推断失败。
    wire flag_visit_clear=state_current == ST_READ && flag_histogram;
    ball_component_store #(.C_DEPTH(16384),.C_ADDR_BITS(14),.C_DATA_BITS(1)) visited_Inst(
        .i_clk(i_clk),.i_read_enable(state_current == ST_READ && !flag_histogram && !i_clear),.i_read_address(reg_address),
        .i_write_enable((flag_visit_clear || flag_queue_write) && !i_clear),.i_write_address(reg_address),
        .i_write_data(flag_queue_write),.o_read_data(flag_visited));
    // 每次完整扫描先写零访问位；直方图同一bin的读改写在独立状态内完成。
    always @(posedge i_clk)begin
        if(!i_clear)begin
            if(state_current == ST_HISTOGRAM_CLEAR)begin mem_histogram[cnt_gray]<=0;end
            else if(state_current == ST_HISTOGRAM_WRITE)begin mem_histogram[reg_pixel]<=reg_histogram_data+1'b1;end
            if(flag_histogram_read)begin reg_histogram_data<=mem_histogram[wire_histogram_address];end
        end
    end
    always @(*)begin
        dec_neighbor_address=reg_node;dec_neighbor_valid=0;
        case(cnt_direction)
            0:begin dec_neighbor_address=reg_node-14'd1;dec_neighbor_valid=reg_node[6:0] != 0;end
            1:begin dec_neighbor_address=reg_node+14'd1;dec_neighbor_valid=reg_node[6:0] != 127;end
            2:begin dec_neighbor_address=reg_node-14'd128;dec_neighbor_valid=reg_node[13:7] != 0;end
            3:begin dec_neighbor_address=reg_node+14'd128;dec_neighbor_valid=reg_node[13:7] != 127;end
            default:begin end
        endcase
    end
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin state_current<=ST_IDLE;end
        else if(i_clear)begin state_current<=ST_IDLE;end
        else begin state_current<=state_next;end
    end
    always @(*)begin
        state_next=state_current;
        case(state_current)
            ST_IDLE:begin if(i_start)begin state_next=ST_GEOMETRY;end end
            ST_GEOMETRY:begin if(reg_left <= C_X_MIN+2 || reg_top <= C_Y_MIN+2 || reg_right >= C_X_END-3 || reg_bottom >= C_Y_END-3)begin state_next=ST_CLIPPED;end
else if(reg_width < 80 || reg_height < 80 || reg_width > 192 || reg_height > 192 ||
    reg_width*4 > reg_height*5 || reg_height*4 > reg_width*5)begin state_next=ST_GEOMETRY_BAD;end
else if(reg_left < reg_origin_x || reg_top < reg_origin_y || {1'b0,reg_right} >= {1'b0,reg_origin_x}+13'd256 ||
    {1'b0,reg_bottom} >= {1'b0,reg_origin_y}+13'd256)begin state_next=ST_WINDOW_BAD;end
else begin state_next=ST_RADIUS;end end
            ST_RADIUS:begin state_next=ST_LIMITS; end
            ST_LIMITS:begin state_next=ST_MAXIMUM; end
            ST_MAXIMUM:begin state_next=ST_MAXIMUM_WAIT; end
            ST_MAXIMUM_WAIT:begin if(flag_math_done)begin state_next=ST_HISTOGRAM_CLEAR;end end
            ST_HISTOGRAM_CLEAR:begin if(cnt_gray == 255)begin state_next=ST_READ;end end
            ST_READ:begin state_next=ST_LOAD; end
            ST_LOAD:begin state_next=ST_POSITION; end
            ST_POSITION:begin state_next=ST_SQUARE; end
            ST_SQUARE:begin state_next=ST_INSIDE; end
            ST_INSIDE:begin state_next=ST_CHECK; end
            ST_CHECK:begin if(flag_histogram)begin
    if(flag_inside)begin state_next=ST_HISTOGRAM_READ;end else begin state_next=ST_ADVANCE;end
end else if(flag_inside && reg_pixel < reg_threshold_o && !flag_visited)begin
    if(flag_neighbor && cnt_queue == (1 << C_QUEUE_BITS))begin state_next=ST_QUEUE_BAD;end
    else begin state_next=ST_ENQUEUE;end
end else if(flag_neighbor)begin state_next=ST_NEIGHBOR_NEXT;end
else begin state_next=ST_ADVANCE;end end
            ST_HISTOGRAM_READ:begin state_next=ST_HISTOGRAM_WRITE; end
            ST_HISTOGRAM_WRITE:begin state_next=ST_ADVANCE; end
            ST_ADVANCE:begin if(cnt_scan == 16383)begin
    if(flag_histogram)begin state_next=ST_MEDIAN_READ;end else begin state_next=ST_FINISH;end
end else begin state_next=ST_READ;end end
            ST_MEDIAN_READ:begin state_next=ST_MEDIAN_CHECK; end
            ST_MEDIAN_CHECK:begin if(wire_cumulative >= (({1'b0,cnt_total}+16'd1) >> 1))begin state_next=ST_DARK_SCAN;end
else begin state_next=ST_MEDIAN_READ;end end
            ST_DARK_SCAN:begin state_next=ST_READ; end
            ST_ENQUEUE:begin if(flag_neighbor)begin state_next=ST_NEIGHBOR_NEXT;end else begin state_next=ST_POP_TEST;end end
            ST_POP_TEST:begin if(cnt_queue == 0)begin state_next=ST_AREA;end else begin state_next=ST_POP_READ;end end
            ST_POP_READ:begin state_next=ST_POP_LOAD; end
            ST_POP_LOAD:begin state_next=ST_NODE; end
            ST_NODE:begin state_next=ST_NEIGHBOR; end
            ST_NEIGHBOR:begin state_next=ST_NEIGHBOR_TEST; end
            ST_NEIGHBOR_TEST:begin if(flag_neighbor_valid)begin state_next=ST_READ;end else begin state_next=ST_NEIGHBOR_NEXT;end end
            ST_NEIGHBOR_NEXT:begin if(cnt_direction == 3)begin state_next=ST_POP_TEST;end else begin state_next=ST_NEIGHBOR;end end
            ST_AREA:begin state_next=ST_AREA_CHECK; end
            ST_AREA_CHECK:begin if(reg_area < reg_minimum_area || reg_area > reg_maximum_area)begin state_next=ST_ADVANCE;end
else begin state_next=ST_CENTROID_X;end end
            ST_CENTROID_X:begin state_next=ST_CENTROID_X_WAIT; end
            ST_CENTROID_X_WAIT:begin if(flag_math_done)begin state_next=ST_CENTROID_Y;end end
            ST_CENTROID_Y:begin state_next=ST_CENTROID_Y_WAIT; end
            ST_CENTROID_Y_WAIT:begin if(flag_math_done)begin state_next=ST_OFFSET;end end
            ST_OFFSET:begin state_next=ST_OFFSET_SQUARE; end
            ST_OFFSET_SQUARE:begin state_next=ST_FILTER; end
            ST_FILTER:begin if(wire_offset >= reg_offset_low_square && wire_offset <= reg_offset_high_square &&
    reg_component_width <= (reg_component_height << 1) && reg_component_height <= (reg_component_width << 1) &&
    wire_area_hundred >= wire_box_thirtyfive)begin
    if(cnt_markers != 0)begin state_next=ST_MULTIPLE;end else begin state_next=ST_ACCEPT;end
end else begin state_next=ST_ADVANCE;end end
            ST_ACCEPT:begin state_next=ST_ADVANCE; end
            ST_FINISH:begin state_next=ST_DONE; end
            ST_CLIPPED:begin state_next=ST_DONE; end
            ST_GEOMETRY_BAD:begin state_next=ST_DONE; end
            ST_WINDOW_BAD:begin state_next=ST_DONE; end
            ST_QUEUE_BAD:begin state_next=ST_DONE; end
            ST_MULTIPLE:begin state_next=ST_DONE; end
            ST_DONE:begin state_next=ST_IDLE; end
            default:begin state_next=ST_IDLE;end
        endcase
    end
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            reg_origin_x<=0;reg_origin_y<=0;reg_left<=0;reg_right<=0;reg_top<=0;reg_bottom<=0;
            reg_width<=0;reg_height<=0;reg_center_x_o<=0;reg_center_y_o<=0;reg_marker_x_o<=0;reg_marker_y_o<=0;
            reg_radius<=0;reg_inner<=0;reg_offset_low<=0;reg_offset_high<=0;reg_radius_square<=0;
            reg_inner_square<=0;reg_offset_low_square<=0;reg_offset_high_square<=0;reg_minimum_area<=0;reg_maximum_area<=0;
            cnt_scan<=0;reg_address<=0;reg_node<=0;flag_histogram<=0;flag_neighbor<=0;flag_inside<=0;flag_neighbor_valid<=0;
            reg_pixel<=0;reg_median_o<=0;reg_threshold_o<=0;cnt_gray<=0;reg_dx<=0;reg_dy<=0;reg_square_x<=0;reg_square_y<=0;
            cnt_total<=0;reg_cumulative<=0;cnt_head<=0;cnt_tail<=0;cnt_queue<=0;cnt_area<=0;reg_area<=0;
            reg_sum_x<=0;reg_sum_y<=0;reg_box_area<=0;reg_min_column<=0;reg_max_column<=0;reg_min_row<=0;reg_max_row<=0;
            reg_component_width<=0;reg_component_height<=0;reg_marker_x<=0;reg_marker_y<=0;cnt_direction<=0;cnt_markers<=0;
            flag_valid_o<=0;flag_done_o<=0;reg_reason_o<=0;reg_math_left<=0;reg_math_right<=0;
            flag_math_round<=0;flag_math_start<=0;
        end else if(i_clear)begin
            flag_valid_o<=0;flag_done_o<=0;flag_math_start<=0;reg_reason_o<=0;
        end else begin
            flag_done_o<=0;flag_math_start<=0;
            case(state_current)
                ST_IDLE:begin
if(i_start)begin
    reg_origin_x<=i_origin_x;reg_origin_y<=i_origin_y;
    reg_left<=i_left;reg_right<=i_right;reg_top<=i_top;reg_bottom<=i_bottom;
    flag_valid_o<=0;reg_reason_o<=0;cnt_markers<=0;reg_median_o<=0;reg_threshold_o<=0;
    reg_center_x_o<=({4'd0,i_left}+{4'd0,i_right}) << 3;
    reg_center_y_o<=({4'd0,i_top}+{4'd0,i_bottom}) << 3;
    reg_width<=({1'b0,i_right}-{1'b0,i_left})+13'd1;
    reg_height<=({1'b0,i_bottom}-{1'b0,i_top})+13'd1;
end
                end
                ST_GEOMETRY:begin
reg_radius<=(reg_width < reg_height ? reg_width : reg_height) << 3;
                end
                ST_RADIUS:begin
reg_radius_square<=reg_radius*reg_radius;
reg_inner<=wire_inner_product >> 8;reg_offset_low<=wire_low_product >> 8;reg_offset_high<=wire_high_product >> 8;
                end
                ST_LIMITS:begin
reg_inner_square<=reg_inner*reg_inner;
reg_offset_low_square<=reg_offset_low*reg_offset_low;reg_offset_high_square<=reg_offset_high*reg_offset_high;
reg_minimum_area<=reg_radius_square >= 32'd2240000 ? 4'd7 : 4'd6;
                end
                ST_MAXIMUM:begin
reg_math_left<=((reg_radius_square << 10)-(reg_radius_square << 8))+((reg_radius_square << 5)+(reg_radius_square << 2));reg_math_right<=32'd1638400;
flag_math_round<=0;flag_math_start<=1;
                end
                ST_MAXIMUM_WAIT:begin
if(flag_math_done)begin
    reg_maximum_area<=wire_math_result;cnt_gray<=0;cnt_total<=0;
    cnt_scan<=0;reg_address<=0;flag_histogram<=1;flag_neighbor<=0;
end
                end
                ST_HISTOGRAM_CLEAR:begin
cnt_gray<=cnt_gray+1'b1;
                end
                ST_LOAD:begin
reg_pixel<=reg_address[0] ? i_read_data[7:0] : i_read_data[15:8];
                end
                ST_POSITION:begin
reg_dx<=$signed({1'b0,wire_global_x})-$signed({1'b0,reg_center_x_o});
reg_dy<=$signed({1'b0,wire_global_y})-$signed({1'b0,reg_center_y_o});
                end
                ST_SQUARE:begin
reg_square_x<=reg_dx*reg_dx;reg_square_y<=reg_dy*reg_dy;
                end
                ST_INSIDE:begin
flag_inside<=reg_square_x+reg_square_y < reg_inner_square;
                end
                ST_HISTOGRAM_WRITE:begin
cnt_total<=cnt_total+1'b1;
                end
                ST_ADVANCE:begin
cnt_scan<=cnt_scan+1'b1;reg_address<=cnt_scan+1'b1;flag_neighbor<=0;
cnt_gray<=0;reg_cumulative<=0;
                end
                ST_MEDIAN_CHECK:begin
if(wire_cumulative >= (({1'b0,cnt_total}+16'd1) >> 1))begin
    reg_median_o<=cnt_gray;reg_threshold_o<=wire_threshold_product[15:8];
end else begin cnt_gray<=cnt_gray+1'b1;reg_cumulative<=wire_cumulative;end
                end
                ST_DARK_SCAN:begin
flag_histogram<=0;flag_neighbor<=0;reg_address<=0;cnt_scan<=0;
                end
                ST_ENQUEUE:begin
if(flag_neighbor)begin
    cnt_tail<=cnt_tail+1'b1;cnt_queue<=cnt_queue+1'b1;
end else begin
    cnt_head<=0;cnt_tail<=1;cnt_queue<=1;cnt_area<=0;reg_sum_x<=0;reg_sum_y<=0;
    reg_min_column<=reg_address[6:0];reg_max_column<=reg_address[6:0];
    reg_min_row<=reg_address[13:7];reg_max_row<=reg_address[13:7];
end
                end
                ST_POP_LOAD:begin
reg_node<=wire_queue_data;cnt_head<=cnt_head+1'b1;cnt_queue<=cnt_queue-1'b1;
                end
                ST_NODE:begin
cnt_area<=cnt_area+1'b1;
reg_sum_x<=reg_sum_x+{20'd0,reg_node[6:0],5'd8};
reg_sum_y<=reg_sum_y+{20'd0,reg_node[13:7],5'd8};
if(reg_node[6:0] < reg_min_column)begin reg_min_column<=reg_node[6:0];end
if(reg_node[6:0] > reg_max_column)begin reg_max_column<=reg_node[6:0];end
if(reg_node[13:7] < reg_min_row)begin reg_min_row<=reg_node[13:7];end
if(reg_node[13:7] > reg_max_row)begin reg_max_row<=reg_node[13:7];end
cnt_direction<=0;
                end
                ST_NEIGHBOR:begin
reg_address<=dec_neighbor_address;flag_neighbor_valid<=dec_neighbor_valid;flag_neighbor<=1;
                end
                ST_NEIGHBOR_NEXT:begin
cnt_direction<=cnt_direction+1'b1;
                end
                ST_AREA:begin
reg_area<={cnt_area,2'b0};
reg_component_width<=({2'd0,reg_max_column}-{2'd0,reg_min_column}+9'd1) << 1;
reg_component_height<=({2'd0,reg_max_row}-{2'd0,reg_min_row}+9'd1) << 1;
                end
                ST_AREA_CHECK:begin
reg_box_area<=reg_component_width*reg_component_height;
                end
                ST_CENTROID_X:begin
reg_math_left<=reg_sum_x;reg_math_right<=cnt_area;flag_math_round<=1;flag_math_start<=1;
                end
                ST_CENTROID_X_WAIT:begin
if(flag_math_done)begin reg_marker_x<={reg_origin_x,4'd0}+wire_math_result[15:0];end
                end
                ST_CENTROID_Y:begin
reg_math_left<=reg_sum_y;reg_math_right<=cnt_area;flag_math_start<=1;
                end
                ST_CENTROID_Y_WAIT:begin
if(flag_math_done)begin reg_marker_y<={reg_origin_y,4'd0}+wire_math_result[15:0];end
                end
                ST_OFFSET:begin
reg_dx<=$signed({1'b0,reg_marker_x})-$signed({1'b0,reg_center_x_o});
reg_dy<=$signed({1'b0,reg_marker_y})-$signed({1'b0,reg_center_y_o});
                end
                ST_OFFSET_SQUARE:begin
reg_square_x<=reg_dx*reg_dx;reg_square_y<=reg_dy*reg_dy;
                end
                ST_ACCEPT:begin
cnt_markers<=cnt_markers+1'b1;reg_marker_x_o<=reg_marker_x;reg_marker_y_o<=reg_marker_y;
                end
                ST_FINISH:begin
flag_valid_o<=cnt_markers == 1;reg_reason_o<=cnt_markers == 1 ? 4'd0 : 4'd9;
                end
                ST_CLIPPED:begin
reg_reason_o<=5;
                end
                ST_GEOMETRY_BAD:begin
reg_reason_o<=6;
                end
                ST_WINDOW_BAD:begin
reg_reason_o<=7;
                end
                ST_QUEUE_BAD:begin
reg_reason_o<=8;flag_valid_o<=0;
                end
                ST_MULTIPLE:begin
reg_reason_o<=10;flag_valid_o<=0;
                end
                ST_DONE:begin
flag_done_o<=1;
                end
                default:begin end
            endcase
        end
    end
    assign o_busy=state_current != ST_IDLE;
    assign o_done=flag_done_o;
    assign o_valid=flag_valid_o;
    assign o_reason=reg_reason_o;
    assign o_center_x=reg_center_x_o;
    assign o_center_y=reg_center_y_o;
    assign o_marker_x=reg_marker_x_o;
    assign o_marker_y=reg_marker_y_o;
    assign o_median=reg_median_o;
    assign o_threshold=reg_threshold_o;
    assign o_read=state_current == ST_READ;
    assign o_read_address=reg_address[13:1];

endmodule
