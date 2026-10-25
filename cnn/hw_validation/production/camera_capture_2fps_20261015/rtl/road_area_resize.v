`timescale 1ns / 1ps

// 精确1280x720到512x288彩色面积缩放器。
// 输入端不可反压；正常时序要求每行320拍有效数据后至少192拍空闲。
module road_area_resize (
    input          i_clk,                 // AWB像素与缩放处理共用时钟
    input          i_rstn,                // 低有效异步复位
    input  [95:0]  i_rgb,                 // 四个高lane优先的RGB888像素
    input          i_valid,               // 本拍四个输入像素有效
    input          i_sof,                 // 新源帧开始，可早于首个有效拍
    input          i_eol,                 // 当前有效拍结束源行
    output [47:0]  o_pixels,              // 低24位为串行RGB888输出
    output [1:0]   o_pixel_mask,          // 串行输出固定使用01
    output         o_sof,                 // 首个缩放像素标志
    output         o_eol,                 // 缩放输出行末标志
    output         o_eof,                 // 缩放输出帧末标志
    output         o_frame_error,         // 几何、重入或缓存溢出错误脉冲
    output         o_busy                 // 从接受SOF到末像素或错误保持忙
);

    //------------------------------输入解包------------------------------//
    wire [23:0] wire_pixel_zero;           // 本拍最早的高lane像素
    wire [23:0] wire_pixel_one;            // 本拍第二个输入像素
    wire [23:0] wire_pixel_two;            // 本拍第三个输入像素
    wire [23:0] wire_pixel_three;          // 本拍最晚的低lane像素

    assign wire_pixel_zero  = i_rgb[95:72]; // AWB高lane映射到时间最早像素
    assign wire_pixel_one   = i_rgb[71:48]; // AWB次高lane映射到第二像素
    assign wire_pixel_two   = i_rgb[47:24]; // AWB次低lane映射到第三像素
    assign wire_pixel_three = i_rgb[23:0];  // AWB低lane映射到时间最晚像素

    //------------------------------帧控制------------------------------//
    reg          flag_capture_active;      // 当前帧仍接受源像素
    reg  [8:0]   cnt_input_beat;            // 当前源行的四像素拍号
    reg  [9:0]   cnt_input_row;             // 当前源行号
    reg  [2:0]   cnt_horizontal_phase;      // 源横坐标模五相位

    reg          busy_o;                    // 帧处理忙输出寄存器
    reg          frame_error_o;             // 帧错误脉冲输出寄存器

    wire         flag_start_frame;          // 空闲时接受的新SOF
    wire         flag_reentrant_sof;        // 忙期间出现的新SOF
    wire         flag_effective_capture;    // 本拍可按当前帧解析输入
    wire [8:0]   wire_effective_beat;       // 新帧同拍输入使用零拍号
    wire [9:0]   wire_effective_row;        // 新帧同拍输入使用零行号
    wire [2:0]   wire_effective_phase;      // 新帧同拍输入使用零相位
    wire         flag_expected_eol;         // 当前有效拍应当结束源行
    wire         flag_geometry_error;       // EOL位置或空拍EOL不合法

    assign flag_start_frame       = i_sof && !busy_o; // 空闲SOF建立新帧代际
    assign flag_reentrant_sof     = i_sof && busy_o;  // 忙态SOF拒绝未完成旧帧
    assign flag_effective_capture = flag_capture_active || flag_start_frame; // 支持SOF与首valid同拍
    assign wire_effective_beat    = flag_start_frame ? 9'd0 : cnt_input_beat; // 新帧首拍从零开始
    assign wire_effective_row     = flag_start_frame ? 10'd0 : cnt_input_row; // 新帧首行从零开始
    assign wire_effective_phase   = flag_start_frame ? 3'd0 : cnt_horizontal_phase; // 横向五相位复位
    assign flag_expected_eol      = wire_effective_beat == 9'd319; // 第320个有效拍必须带EOL
    assign flag_geometry_error    = flag_effective_capture
                                  && ((i_eol && !i_valid)
                                  || (i_valid && (i_eol != flag_expected_eol))); // 仅用EOL核对几何

    //------------------------------水平缩放------------------------------//
    reg  [32:0] reg_partial_even;           // 下一偶数输出的三通道部分和
    reg  [32:0] reg_partial_odd;            // 下一奇数输出的三通道部分和
    reg  [32:0] reg_horizontal_first;       // 本拍首个水平结果
    reg  [32:0] reg_horizontal_second;      // 本拍可选第二个水平结果
    reg         flag_horizontal_second;     // 本拍产生两个水平结果

    // 四输入拍按源横坐标模五计算一项或两项十一位水平和。
    always @(*) begin
        reg_horizontal_first  = 33'd0;
        reg_horizontal_second = 33'd0;
        flag_horizontal_second = 1'b0;
        case (wire_effective_phase)
            3'd0: begin
                reg_horizontal_first[10:0]  = ({3'd0, wire_pixel_zero[23:16]} << 1)
                                               + ({3'd0, wire_pixel_one[23:16]} << 1)
                                               + {3'd0, wire_pixel_two[23:16]};
                reg_horizontal_first[21:11] = ({3'd0, wire_pixel_zero[15:8]} << 1)
                                               + ({3'd0, wire_pixel_one[15:8]} << 1)
                                               + {3'd0, wire_pixel_two[15:8]};
                reg_horizontal_first[32:22] = ({3'd0, wire_pixel_zero[7:0]} << 1)
                                               + ({3'd0, wire_pixel_one[7:0]} << 1)
                                               + {3'd0, wire_pixel_two[7:0]};
            end
            3'd4: begin
                reg_horizontal_first[10:0]  = reg_partial_odd[10:0]
                                               + ({3'd0, wire_pixel_zero[23:16]} << 1);
                reg_horizontal_first[21:11] = reg_partial_odd[21:11]
                                               + ({3'd0, wire_pixel_zero[15:8]} << 1);
                reg_horizontal_first[32:22] = reg_partial_odd[32:22]
                                               + ({3'd0, wire_pixel_zero[7:0]} << 1);
                reg_horizontal_second[10:0]  = ({3'd0, wire_pixel_one[23:16]} << 1)
                                                + ({3'd0, wire_pixel_two[23:16]} << 1)
                                                + {3'd0, wire_pixel_three[23:16]};
                reg_horizontal_second[21:11] = ({3'd0, wire_pixel_one[15:8]} << 1)
                                                + ({3'd0, wire_pixel_two[15:8]} << 1)
                                                + {3'd0, wire_pixel_three[15:8]};
                reg_horizontal_second[32:22] = ({3'd0, wire_pixel_one[7:0]} << 1)
                                                + ({3'd0, wire_pixel_two[7:0]} << 1)
                                                + {3'd0, wire_pixel_three[7:0]};
                flag_horizontal_second = 1'b1;
            end
            3'd3: begin
                reg_horizontal_first[10:0]  = reg_partial_odd[10:0]
                                               + ({3'd0, wire_pixel_zero[23:16]} << 1)
                                               + ({3'd0, wire_pixel_one[23:16]} << 1);
                reg_horizontal_first[21:11] = reg_partial_odd[21:11]
                                               + ({3'd0, wire_pixel_zero[15:8]} << 1)
                                               + ({3'd0, wire_pixel_one[15:8]} << 1);
                reg_horizontal_first[32:22] = reg_partial_odd[32:22]
                                               + ({3'd0, wire_pixel_zero[7:0]} << 1)
                                               + ({3'd0, wire_pixel_one[7:0]} << 1);
            end
            3'd2: begin
                reg_horizontal_first[10:0]  = reg_partial_even[10:0]
                                               + {3'd0, wire_pixel_zero[23:16]};
                reg_horizontal_first[21:11] = reg_partial_even[21:11]
                                               + {3'd0, wire_pixel_zero[15:8]};
                reg_horizontal_first[32:22] = reg_partial_even[32:22]
                                               + {3'd0, wire_pixel_zero[7:0]};
                reg_horizontal_second[10:0]  = {3'd0, wire_pixel_zero[23:16]}
                                                + ({3'd0, wire_pixel_one[23:16]} << 1)
                                                + ({3'd0, wire_pixel_two[23:16]} << 1);
                reg_horizontal_second[21:11] = {3'd0, wire_pixel_zero[15:8]}
                                                + ({3'd0, wire_pixel_one[15:8]} << 1)
                                                + ({3'd0, wire_pixel_two[15:8]} << 1);
                reg_horizontal_second[32:22] = {3'd0, wire_pixel_zero[7:0]}
                                                + ({3'd0, wire_pixel_one[7:0]} << 1)
                                                + ({3'd0, wire_pixel_two[7:0]} << 1);
                flag_horizontal_second = 1'b1;
            end
            default: begin
                reg_horizontal_first[10:0]  = reg_partial_even[10:0]
                                               + ({3'd0, wire_pixel_zero[23:16]} << 1)
                                               + {3'd0, wire_pixel_one[23:16]};
                reg_horizontal_first[21:11] = reg_partial_even[21:11]
                                               + ({3'd0, wire_pixel_zero[15:8]} << 1)
                                               + {3'd0, wire_pixel_one[15:8]};
                reg_horizontal_first[32:22] = reg_partial_even[32:22]
                                               + ({3'd0, wire_pixel_zero[7:0]} << 1)
                                               + {3'd0, wire_pixel_one[7:0]};
                reg_horizontal_second[10:0]  = {3'd0, wire_pixel_one[23:16]}
                                                + ({3'd0, wire_pixel_two[23:16]} << 1)
                                                + ({3'd0, wire_pixel_three[23:16]} << 1);
                reg_horizontal_second[21:11] = {3'd0, wire_pixel_one[15:8]}
                                                + ({3'd0, wire_pixel_two[15:8]} << 1)
                                                + ({3'd0, wire_pixel_three[15:8]} << 1);
                reg_horizontal_second[32:22] = {3'd0, wire_pixel_one[7:0]}
                                                + ({3'd0, wire_pixel_two[7:0]} << 1)
                                                + ({3'd0, wire_pixel_three[7:0]} << 1);
                flag_horizontal_second = 1'b1;
            end
        endcase
    end

    //------------------------------有界记录队列------------------------------//
    reg  [66:0] reg_pair_fifo [0:127];      // 单写异步读LUTRAM候选队列
    reg  [6:0]  cnt_fifo_write;             // 记录写指针
    reg  [6:0]  cnt_fifo_read;              // 记录读指针
    reg  [7:0]  cnt_fifo_records;           // 队列记录数，允许表示满128
    reg         flag_second_pending;        // 已弹出记录的第二像素待处理
    reg  [32:0] reg_second_sum;             // 队列外保存的第二水平和

    wire [66:0] wire_new_record;            // 当前输入拍形成的变长记录
    wire [66:0] wire_fifo_head;             // 当前队头记录
    wire         flag_new_record_valid;     // 当前输入拍通过几何检查
    wire         flag_worker_from_second;   // worker处理已保存第二像素
    wire         flag_worker_from_fifo;     // worker弹出一个队列记录
    wire         flag_worker_from_new;      // 空队列时当前结果直接旁路
    wire         flag_worker_issue;         // 本拍纵向端口接收一个像素
    wire [32:0]  wire_worker_sum;            // worker当前水平和
    wire         flag_fifo_push;            // 当前记录需要写入队列
    wire         flag_fifo_pop;             // 当前记录从队列弹出
    wire         flag_fifo_overflow;         // 满队列遇到新记录
    wire         flag_fatal_error;           // 本拍必须取消整帧

    assign wire_new_record = {flag_horizontal_second,
                              reg_horizontal_first,
                              reg_horizontal_second}; // 每输入拍最多写一条记录
    assign wire_fifo_head = reg_pair_fifo[cnt_fifo_read]; // LUTRAM异步读队头
    assign flag_new_record_valid = flag_effective_capture && i_valid
                                 && !flag_geometry_error && !flag_reentrant_sof; // 错误拍不入队
    assign flag_worker_from_second = !flag_start_frame && flag_second_pending; // 第二像素优先保持顺序
    assign flag_worker_from_fifo = !flag_start_frame && !flag_second_pending
                                 && (cnt_fifo_records != 8'd0); // 非空队列提供下一记录
    assign flag_worker_from_new = flag_new_record_valid
                                && !flag_worker_from_second && !flag_worker_from_fifo; // 空队列直通
    assign flag_worker_issue = flag_worker_from_second
                             || flag_worker_from_fifo || flag_worker_from_new; // 串行端口每拍至多一项
    assign wire_worker_sum = flag_worker_from_second ? reg_second_sum
                           : flag_worker_from_fifo ? wire_fifo_head[65:33]
                           : reg_horizontal_first; // 保持水平输出先后顺序
    assign flag_fifo_push = flag_new_record_valid && !flag_worker_from_new; // 忙worker时缓存完整记录
    assign flag_fifo_pop = flag_worker_from_fifo; // 仅处理记录首像素时弹出
    assign flag_fifo_overflow = flag_fifo_push && (cnt_fifo_records == 8'd128); // 满时不依赖同址碰撞
    assign flag_fatal_error = flag_reentrant_sof || flag_geometry_error || flag_fifo_overflow; // 错误统一冲刷代际

    //------------------------------纵向调度------------------------------//
    reg  [8:0]  cnt_worker_x;               // 串行worker水平输出坐标
    reg  [2:0]  cnt_worker_row_phase;       // worker源行模五相位
    reg  [8:0]  cnt_worker_output_y;        // 下一有效缩放输出行号

    wire [8:0]  wire_worker_x;              // 新帧同拍处理使用零横坐标
    wire [2:0]  wire_worker_row_phase;      // 新帧同拍处理使用零行相位
    wire [8:0]  wire_worker_output_y;       // 新帧同拍处理使用零输出行

    wire        flag_read_accum_a;          // 读取首个纵向累加行
    wire        flag_read_accum_b;          // 读取第二个纵向累加行
    wire        flag_direct_write_a;        // 源相位0初始化首累加行
    wire        flag_direct_write_b;        // 源相位2初始化第二累加行
    wire [38:0] wire_worker_double;          // 当前水平和乘二的三通道字

    assign wire_worker_x = flag_start_frame ? 9'd0 : cnt_worker_x; // SOF与首valid同拍时从x0开始
    assign wire_worker_row_phase = flag_start_frame ? 3'd0 : cnt_worker_row_phase; // 新帧首行相位固定0
    assign wire_worker_output_y = flag_start_frame ? 9'd0 : cnt_worker_output_y; // 新帧首输出行固定0
    assign flag_read_accum_a = flag_worker_issue
                             && ((wire_worker_row_phase == 3'd1)
                             || (wire_worker_row_phase == 3'd2)); // 相位1更新、相位2输出
    assign flag_read_accum_b = flag_worker_issue
                             && ((wire_worker_row_phase == 3'd3)
                             || (wire_worker_row_phase == 3'd4)); // 相位3更新、相位4输出
    assign flag_direct_write_a = flag_worker_issue && (wire_worker_row_phase == 3'd0); // 2倍和初始化A
    assign flag_direct_write_b = flag_worker_issue && (wire_worker_row_phase == 3'd2); // 1倍和初始化B
    assign wire_worker_double = {{1'b0, wire_worker_sum[32:22], 1'b0},
                                 {1'b0, wire_worker_sum[21:11], 1'b0},
                                 {1'b0, wire_worker_sum[10:0], 1'b0}}; // 三个十一位值分别扩展乘二

    //------------------------------ERAM读返回------------------------------//
    reg         flag_ram_read_pending;      // 上拍ERAM读请求有效
    reg  [2:0]  reg_ram_read_phase;         // 读返回对应源行相位
    reg  [32:0] reg_ram_read_sum;           // 读返回对应水平和
    reg  [8:0]  reg_ram_read_x;             // 读返回对应输出横坐标
    reg  [8:0]  reg_ram_read_output_y;      // 读返回对应输出纵坐标

    wire [39:0] wire_accum_a_read;          // 首累加ERAM读数据
    wire [39:0] wire_accum_b_read;          // 第二累加ERAM读数据
    wire        flag_update_write_a;        // 相位1读改写A
    wire        flag_update_write_b;        // 相位3读改写B
    wire [38:0] wire_update_data_a;          // A累加行的新值
    wire [38:0] wire_update_data_b;          // B累加行的新值
    wire        flag_accum_a_write;         // A口对应ERAM的B端口写使能
    wire        flag_accum_b_write;         // B口对应ERAM的B端口写使能
    wire [8:0]  wire_accum_a_write_addr;    // A累加ERAM写地址
    wire [8:0]  wire_accum_b_write_addr;    // B累加ERAM写地址
    wire [39:0] wire_accum_a_write_data;    // A累加ERAM写数据
    wire [39:0] wire_accum_b_write_data;    // B累加ERAM写数据

    assign flag_update_write_a = flag_ram_read_pending && (reg_ram_read_phase == 3'd1)
                               && !flag_start_frame && !flag_fatal_error; // 错误边界禁止旧代写回
    assign flag_update_write_b = flag_ram_read_pending && (reg_ram_read_phase == 3'd3)
                               && !flag_start_frame && !flag_fatal_error; // 新SOF冲刷旧读返回
    assign wire_update_data_a[12:0]  = wire_accum_a_read[12:0]
                                      + ({2'd0, reg_ram_read_sum[10:0]} << 1); // R加二倍水平和
    assign wire_update_data_a[25:13] = wire_accum_a_read[25:13]
                                      + ({2'd0, reg_ram_read_sum[21:11]} << 1); // G加二倍水平和
    assign wire_update_data_a[38:26] = wire_accum_a_read[38:26]
                                      + ({2'd0, reg_ram_read_sum[32:22]} << 1); // B加二倍水平和
    assign wire_update_data_b[12:0]  = wire_accum_b_read[12:0]
                                      + ({2'd0, reg_ram_read_sum[10:0]} << 1); // R更新第二累加行
    assign wire_update_data_b[25:13] = wire_accum_b_read[25:13]
                                      + ({2'd0, reg_ram_read_sum[21:11]} << 1); // G更新第二累加行
    assign wire_update_data_b[38:26] = wire_accum_b_read[38:26]
                                      + ({2'd0, reg_ram_read_sum[32:22]} << 1); // B更新第二累加行
    assign flag_accum_a_write = flag_update_write_a || (flag_direct_write_a && !flag_fatal_error); // A更新优先于直接初始化
    assign flag_accum_b_write = flag_update_write_b || (flag_direct_write_b && !flag_fatal_error); // B更新优先于直接初始化
    assign wire_accum_a_write_addr = flag_update_write_a ? reg_ram_read_x : wire_worker_x; // 更新写回原读地址
    assign wire_accum_b_write_addr = flag_update_write_b ? reg_ram_read_x : wire_worker_x; // 初始化写当前worker地址
    assign wire_accum_a_write_data = flag_update_write_a ? {1'b0, wire_update_data_a}
                                                        : {1'b0, wire_worker_double}; // A保存三路十三位和
    assign wire_accum_b_write_data = flag_update_write_b ? {1'b0, wire_update_data_b}
                                                        : {1'b0,
                                                           2'd0, wire_worker_sum[32:22],
                                                           2'd0, wire_worker_sum[21:11],
                                                           2'd0, wire_worker_sum[10:0]}; // B相位2保存三路十三位一倍和

    //------------------------------一次RNE除二十五------------------------------//
    reg         flag_divide_input;          // 纵向最终和进入除法流水
    reg  [12:0] reg_divide_red;              // 加十二后的R分子
    reg  [12:0] reg_divide_green;            // 加十二后的G分子
    reg  [12:0] reg_divide_blue;             // 加十二后的B分子
    reg  [8:0]  reg_divide_x;                // 除法输入横坐标
    reg  [8:0]  reg_divide_y;                // 除法输入纵坐标

    reg         flag_magic_one;             // 常数乘法第一级有效
    reg  [25:0] reg_magic_red_a;             // R的10240倍部分积
    reg  [20:0] reg_magic_red_b;             // R的248倍部分积
    reg  [13:0] reg_magic_red_c;             // R的2倍修正项
    reg  [25:0] reg_magic_green_a;           // G的10240倍部分积
    reg  [20:0] reg_magic_green_b;           // G的248倍部分积
    reg  [13:0] reg_magic_green_c;           // G的2倍修正项
    reg  [25:0] reg_magic_blue_a;            // B的10240倍部分积
    reg  [20:0] reg_magic_blue_b;             // B的248倍部分积
    reg  [13:0] reg_magic_blue_c;             // B的2倍修正项
    reg  [8:0]  reg_magic_one_x;             // 第一级横坐标
    reg  [8:0]  reg_magic_one_y;             // 第一级纵坐标

    reg         flag_magic_two;             // 常数乘法第二级有效
    reg  [26:0] reg_magic_red_ab;            // R的10488倍临时和
    reg  [13:0] reg_magic_red_c_delay;        // R的2倍延迟修正项
    reg  [26:0] reg_magic_green_ab;          // G的10488倍临时和
    reg  [13:0] reg_magic_green_c_delay;      // G的2倍延迟修正项
    reg  [26:0] reg_magic_blue_ab;           // B的10488倍临时和
    reg  [13:0] reg_magic_blue_c_delay;       // B的2倍延迟修正项
    reg  [8:0]  reg_magic_two_x;             // 第二级横坐标
    reg  [8:0]  reg_magic_two_y;             // 第二级纵坐标

    reg         flag_magic_three;           // 精确10486倍结果有效
    reg  [26:0] reg_magic_red_product;       // R常数乘积
    reg  [26:0] reg_magic_green_product;     // G常数乘积
    reg  [26:0] reg_magic_blue_product;      // B常数乘积
    reg  [8:0]  reg_magic_three_x;           // 最终乘积横坐标
    reg  [8:0]  reg_magic_three_y;           // 最终乘积纵坐标

    wire        flag_final_sum_ready;        // ERAM读返回形成最终二维和
    wire [12:0] wire_final_red;               // R纵向十三位和
    wire [12:0] wire_final_green;             // G纵向十三位和
    wire [12:0] wire_final_blue;              // B纵向十三位和

    assign flag_final_sum_ready = flag_ram_read_pending
                                && ((reg_ram_read_phase == 3'd2)
                                || (reg_ram_read_phase == 3'd4)); // 两个输出源相位
    assign wire_final_red = reg_ram_read_phase == 3'd2
                          ? wire_accum_a_read[12:0] + {2'd0, reg_ram_read_sum[10:0]}
                          : wire_accum_b_read[12:0] + ({2'd0, reg_ram_read_sum[10:0]} << 1); // 按纵向权重完成R和
    assign wire_final_green = reg_ram_read_phase == 3'd2
                            ? wire_accum_a_read[25:13] + {2'd0, reg_ram_read_sum[21:11]}
                            : wire_accum_b_read[25:13] + ({2'd0, reg_ram_read_sum[21:11]} << 1); // 按纵向权重完成G和
    assign wire_final_blue = reg_ram_read_phase == 3'd2
                           ? wire_accum_a_read[38:26] + {2'd0, reg_ram_read_sum[32:22]}
                           : wire_accum_b_read[38:26] + ({2'd0, reg_ram_read_sum[32:22]} << 1); // 按纵向权重完成B和

    //------------------------------输出桥接------------------------------//
    reg  [47:0] pixels_o;                   // 串行RGB输出寄存器
    reg  [1:0]  pixel_mask_o;               // 输出lane有效掩码寄存器
    reg         sof_o;                       // 缩放帧首标志寄存器
    reg         eol_o;                       // 缩放行末标志寄存器
    reg         eof_o;                       // 缩放帧末标志寄存器

    assign o_pixels      = pixels_o;         // 输出低lane像素
    assign o_pixel_mask  = pixel_mask_o;     // 输出有效lane掩码
    assign o_sof         = sof_o;            // 输出帧首脉冲
    assign o_eol         = eol_o;            // 输出行末脉冲
    assign o_eof         = eof_o;            // 输出帧末脉冲
    assign o_frame_error = frame_error_o;    // 输出拒帧错误脉冲
    assign o_busy        = busy_o;           // 输出当前帧占用状态

    //------------------------------主时序过程------------------------------//
    // 控制输入、FIFO、纵向调度和定点流水，ERAM内容不依赖复位初始化。
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) begin
            flag_capture_active    <= 1'b0;
            cnt_input_beat         <= 9'd0;
            cnt_input_row          <= 10'd0;
            cnt_horizontal_phase   <= 3'd0;
            reg_partial_even       <= 33'd0;
            reg_partial_odd        <= 33'd0;
            cnt_fifo_write         <= 7'd0;
            cnt_fifo_read          <= 7'd0;
            cnt_fifo_records       <= 8'd0;
            flag_second_pending    <= 1'b0;
            reg_second_sum         <= 33'd0;
            cnt_worker_x           <= 9'd0;
            cnt_worker_row_phase   <= 3'd0;
            cnt_worker_output_y    <= 9'd0;
            flag_ram_read_pending  <= 1'b0;
            reg_ram_read_phase     <= 3'd0;
            reg_ram_read_sum       <= 33'd0;
            reg_ram_read_x         <= 9'd0;
            reg_ram_read_output_y  <= 9'd0;
            flag_divide_input      <= 1'b0;
            flag_magic_one         <= 1'b0;
            flag_magic_two         <= 1'b0;
            flag_magic_three       <= 1'b0;
            busy_o                 <= 1'b0;
            frame_error_o          <= 1'b0;
            pixels_o               <= 48'd0;
            pixel_mask_o           <= 2'b00;
            sof_o                  <= 1'b0;
            eol_o                  <= 1'b0;
            eof_o                  <= 1'b0;
        end else begin
            frame_error_o <= 1'b0;
            pixel_mask_o  <= 2'b00;
            sof_o         <= 1'b0;
            eol_o         <= 1'b0;
            eof_o         <= 1'b0;

            if (flag_fatal_error) begin
                flag_capture_active   <= 1'b0;
                cnt_fifo_write        <= 7'd0;
                cnt_fifo_read         <= 7'd0;
                cnt_fifo_records      <= 8'd0;
                flag_second_pending   <= 1'b0;
                cnt_worker_x          <= 9'd0;
                cnt_worker_row_phase  <= 3'd0;
                cnt_worker_output_y   <= 9'd0;
                flag_ram_read_pending <= 1'b0;
                flag_divide_input     <= 1'b0;
                flag_magic_one        <= 1'b0;
                flag_magic_two        <= 1'b0;
                flag_magic_three      <= 1'b0;
                busy_o                <= 1'b0;
                frame_error_o         <= 1'b1;
            end else begin
                if (flag_start_frame) begin
                    flag_capture_active   <= 1'b1;
                    cnt_input_beat        <= 9'd0;
                    cnt_input_row         <= 10'd0;
                    cnt_horizontal_phase  <= 3'd0;
                    reg_partial_even      <= 33'd0;
                    reg_partial_odd       <= 33'd0;
                    cnt_fifo_write        <= 7'd0;
                    cnt_fifo_read         <= 7'd0;
                    cnt_fifo_records      <= 8'd0;
                    flag_second_pending   <= 1'b0;
                    cnt_worker_x          <= 9'd0;
                    cnt_worker_row_phase  <= 3'd0;
                    cnt_worker_output_y   <= 9'd0;
                    flag_ram_read_pending <= 1'b0;
                    flag_divide_input     <= 1'b0;
                    flag_magic_one        <= 1'b0;
                    flag_magic_two        <= 1'b0;
                    flag_magic_three      <= 1'b0;
                    busy_o                <= 1'b1;
                end

                if (flag_new_record_valid) begin
                    case (wire_effective_phase)
                        3'd0: begin
                            reg_partial_odd[10:0]  <= {3'd0, wire_pixel_two[23:16]}
                                                       + ({3'd0, wire_pixel_three[23:16]} << 1);
                            reg_partial_odd[21:11] <= {3'd0, wire_pixel_two[15:8]}
                                                       + ({3'd0, wire_pixel_three[15:8]} << 1);
                            reg_partial_odd[32:22] <= {3'd0, wire_pixel_two[7:0]}
                                                       + ({3'd0, wire_pixel_three[7:0]} << 1);
                            cnt_horizontal_phase <= 3'd4;
                        end
                        3'd4: begin
                            reg_partial_odd[10:0]  <= {3'd0, wire_pixel_three[23:16]};
                            reg_partial_odd[21:11] <= {3'd0, wire_pixel_three[15:8]};
                            reg_partial_odd[32:22] <= {3'd0, wire_pixel_three[7:0]};
                            cnt_horizontal_phase <= 3'd3;
                        end
                        3'd3: begin
                            reg_partial_even[10:0]  <= ({3'd0, wire_pixel_two[23:16]} << 1)
                                                        + ({3'd0, wire_pixel_three[23:16]} << 1);
                            reg_partial_even[21:11] <= ({3'd0, wire_pixel_two[15:8]} << 1)
                                                        + ({3'd0, wire_pixel_three[15:8]} << 1);
                            reg_partial_even[32:22] <= ({3'd0, wire_pixel_two[7:0]} << 1)
                                                        + ({3'd0, wire_pixel_three[7:0]} << 1);
                            cnt_horizontal_phase <= 3'd2;
                        end
                        3'd2: begin
                            reg_partial_even[10:0]  <= ({3'd0, wire_pixel_three[23:16]} << 1);
                            reg_partial_even[21:11] <= ({3'd0, wire_pixel_three[15:8]} << 1);
                            reg_partial_even[32:22] <= ({3'd0, wire_pixel_three[7:0]} << 1);
                            cnt_horizontal_phase <= 3'd1;
                        end
                        default: begin
                            reg_partial_even     <= 33'd0;
                            reg_partial_odd      <= 33'd0;
                            cnt_horizontal_phase <= 3'd0;
                        end
                    endcase

                    if (flag_expected_eol) begin
                        cnt_input_beat <= 9'd0;
                        if (wire_effective_row == 10'd719) begin
                            flag_capture_active <= 1'b0;
                        end else begin
                            cnt_input_row <= wire_effective_row + 10'd1;
                        end
                    end else begin
                        cnt_input_beat <= wire_effective_beat + 9'd1;
                    end
                end

                if (flag_fifo_push) begin
                    reg_pair_fifo[cnt_fifo_write] <= wire_new_record;
                    cnt_fifo_write <= cnt_fifo_write + 7'd1;
                end
                if (flag_fifo_pop) begin
                    cnt_fifo_read <= cnt_fifo_read + 7'd1;
                end
                case ({flag_fifo_push, flag_fifo_pop})
                    2'b10: cnt_fifo_records <= cnt_fifo_records + 8'd1;
                    2'b01: cnt_fifo_records <= cnt_fifo_records - 8'd1;
                    default: begin
                    end
                endcase

                if (flag_worker_from_second) begin
                    flag_second_pending <= 1'b0;
                end else if (flag_worker_from_fifo) begin
                    flag_second_pending <= wire_fifo_head[66];
                    reg_second_sum <= wire_fifo_head[32:0];
                end else if (flag_worker_from_new) begin
                    flag_second_pending <= flag_horizontal_second;
                    reg_second_sum <= reg_horizontal_second;
                end

                if (flag_worker_issue) begin
                    if (wire_worker_x == 9'd511) begin
                        cnt_worker_x <= 9'd0;
                        if (wire_worker_row_phase == 3'd4) begin
                            cnt_worker_row_phase <= 3'd0;
                        end else begin
                            cnt_worker_row_phase <= wire_worker_row_phase + 3'd1;
                        end
                        if ((wire_worker_row_phase == 3'd2)
                         || (wire_worker_row_phase == 3'd4)) begin
                            cnt_worker_output_y <= wire_worker_output_y + 9'd1;
                        end
                    end else begin
                        cnt_worker_x <= wire_worker_x + 9'd1;
                    end
                end

                flag_ram_read_pending <= flag_read_accum_a || flag_read_accum_b;
                if (flag_read_accum_a || flag_read_accum_b) begin
                    reg_ram_read_phase    <= wire_worker_row_phase;
                    reg_ram_read_sum      <= wire_worker_sum;
                    reg_ram_read_x        <= wire_worker_x;
                    reg_ram_read_output_y <= wire_worker_output_y;
                end

                flag_divide_input <= flag_final_sum_ready;
                if (flag_final_sum_ready) begin
                    reg_divide_red   <= wire_final_red + 13'd12;
                    reg_divide_green <= wire_final_green + 13'd12;
                    reg_divide_blue  <= wire_final_blue + 13'd12;
                    reg_divide_x     <= reg_ram_read_x;
                    reg_divide_y     <= reg_ram_read_output_y;
                end

                flag_magic_one <= flag_divide_input;
                if (flag_divide_input) begin
                    reg_magic_red_a   <= ({reg_divide_red, 13'd0})
                                       + ({reg_divide_red, 11'd0});
                    reg_magic_red_b   <= ({reg_divide_red, 8'd0})
                                       - ({reg_divide_red, 3'd0});
                    reg_magic_red_c   <= {reg_divide_red, 1'b0};
                    reg_magic_green_a <= ({reg_divide_green, 13'd0})
                                       + ({reg_divide_green, 11'd0});
                    reg_magic_green_b <= ({reg_divide_green, 8'd0})
                                       - ({reg_divide_green, 3'd0});
                    reg_magic_green_c <= {reg_divide_green, 1'b0};
                    reg_magic_blue_a  <= ({reg_divide_blue, 13'd0})
                                       + ({reg_divide_blue, 11'd0});
                    reg_magic_blue_b  <= ({reg_divide_blue, 8'd0})
                                       - ({reg_divide_blue, 3'd0});
                    reg_magic_blue_c  <= {reg_divide_blue, 1'b0};
                    reg_magic_one_x   <= reg_divide_x;
                    reg_magic_one_y   <= reg_divide_y;
                end

                flag_magic_two <= flag_magic_one;
                if (flag_magic_one) begin
                    reg_magic_red_ab       <= reg_magic_red_a + reg_magic_red_b;
                    reg_magic_red_c_delay  <= reg_magic_red_c;
                    reg_magic_green_ab     <= reg_magic_green_a + reg_magic_green_b;
                    reg_magic_green_c_delay <= reg_magic_green_c;
                    reg_magic_blue_ab      <= reg_magic_blue_a + reg_magic_blue_b;
                    reg_magic_blue_c_delay <= reg_magic_blue_c;
                    reg_magic_two_x        <= reg_magic_one_x;
                    reg_magic_two_y        <= reg_magic_one_y;
                end

                flag_magic_three <= flag_magic_two;
                if (flag_magic_two) begin
                    reg_magic_red_product   <= reg_magic_red_ab - reg_magic_red_c_delay;
                    reg_magic_green_product <= reg_magic_green_ab - reg_magic_green_c_delay;
                    reg_magic_blue_product  <= reg_magic_blue_ab - reg_magic_blue_c_delay;
                    reg_magic_three_x       <= reg_magic_two_x;
                    reg_magic_three_y       <= reg_magic_two_y;
                end

                if (flag_magic_three) begin
                    pixels_o <= {24'd0,
                                 reg_magic_blue_product[25:18],
                                 reg_magic_green_product[25:18],
                                 reg_magic_red_product[25:18]};
                    pixel_mask_o <= 2'b01;
                    sof_o <= (reg_magic_three_x == 9'd0)
                          && (reg_magic_three_y == 9'd0);
                    eol_o <= reg_magic_three_x == 9'd511;
                    eof_o <= (reg_magic_three_x == 9'd511)
                          && (reg_magic_three_y == 9'd287);
                    if ((reg_magic_three_x == 9'd511)
                     && (reg_magic_three_y == 9'd287)) begin
                        busy_o <= 1'b0;
                    end
                end
            end
        end
    end

    //------------------------------纵向ERAM实例------------------------------//
    // 首个纵向输出累加行，A口读、B口写，40x512双口配置。
    PH1P_LOGIC_ERAM #(
        .DATA_WIDTH_A(40),
        .DATA_WIDTH_B(40),
        .ADDR_WIDTH_A(9),
        .ADDR_WIDTH_B(9),
        .DATA_DEPTH_A(512),
        .DATA_DEPTH_B(512),
        .BYTE_ENABLE(0),
        .BYTE_A(1),
        .BYTE_B(1),
        .MODE("DP"),
        .REGMODE_A("NOREG"),
        .REGMODE_B("NOREG"),
        .WRITEMODE_A("NORMAL"),
        .WRITEMODE_B("NORMAL"),
        .RESETMODE_A("ASYNC"),
        .RESETMODE_B("ASYNC"),
        .OREGSET_A("RESET"),
        .OREGSET_B("RESET"),
        .SSROVERCE("DISABLE"),
        .ECC_DECODE("DISABLE"),
        .ECC_ENCODE("DISABLE"),
        .ASYNC_RESET_RELEASE_A("ASYNC"),
        .ASYNC_RESET_RELEASE_B("ASYNC"),
        .CLKMODE("SYNC"),
        .DEBUGGABLE("NO"),
        .PACKABLE("NO"),
        .FORCE_KEEP("ON"),
        .INIT_FILE("NONE"),
        .FILL_ALL("NONE"),
        .IMPLEMENT("20K")
    ) PH1P_LOGIC_ERAM_Inst_accum_a (
        .dia(40'd0),
        .addra(wire_worker_x),
        .cea(flag_read_accum_a),
        .ocea(1'b0),
        .clka(i_clk),
        .wea(1'b0),
        .rsta(1'b0),
        .bea(1'b0),
        .dib(wire_accum_a_write_data),
        .addrb(wire_accum_a_write_addr),
        .ceb(flag_accum_a_write),
        .oceb(1'b0),
        .clkb(i_clk),
        .web(flag_accum_a_write),
        .rstb(1'b0),
        .beb(1'b0),
        .ecc_sbiterrinj(1'b0),
        .ecc_dbiterrinj(1'b0),
        .doa(wire_accum_a_read),
        .dob(),
        .ecc_sbiterr(),
        .ecc_dbiterr()
    );

    // 第二个纵向输出累加行，首次用前由相位2完整覆盖全部地址。
    PH1P_LOGIC_ERAM #(
        .DATA_WIDTH_A(40),
        .DATA_WIDTH_B(40),
        .ADDR_WIDTH_A(9),
        .ADDR_WIDTH_B(9),
        .DATA_DEPTH_A(512),
        .DATA_DEPTH_B(512),
        .BYTE_ENABLE(0),
        .BYTE_A(1),
        .BYTE_B(1),
        .MODE("DP"),
        .REGMODE_A("NOREG"),
        .REGMODE_B("NOREG"),
        .WRITEMODE_A("NORMAL"),
        .WRITEMODE_B("NORMAL"),
        .RESETMODE_A("ASYNC"),
        .RESETMODE_B("ASYNC"),
        .OREGSET_A("RESET"),
        .OREGSET_B("RESET"),
        .SSROVERCE("DISABLE"),
        .ECC_DECODE("DISABLE"),
        .ECC_ENCODE("DISABLE"),
        .ASYNC_RESET_RELEASE_A("ASYNC"),
        .ASYNC_RESET_RELEASE_B("ASYNC"),
        .CLKMODE("SYNC"),
        .DEBUGGABLE("NO"),
        .PACKABLE("NO"),
        .FORCE_KEEP("ON"),
        .INIT_FILE("NONE"),
        .FILL_ALL("NONE"),
        .IMPLEMENT("20K")
    ) PH1P_LOGIC_ERAM_Inst_accum_b (
        .dia(40'd0),
        .addra(wire_worker_x),
        .cea(flag_read_accum_b),
        .ocea(1'b0),
        .clka(i_clk),
        .wea(1'b0),
        .rsta(1'b0),
        .bea(1'b0),
        .dib(wire_accum_b_write_data),
        .addrb(wire_accum_b_write_addr),
        .ceb(flag_accum_b_write),
        .oceb(1'b0),
        .clkb(i_clk),
        .web(flag_accum_b_write),
        .rstb(1'b0),
        .beb(1'b0),
        .ecc_sbiterrinj(1'b0),
        .ecc_dbiterrinj(1'b0),
        .doa(wire_accum_b_read),
        .dob(),
        .ecc_sbiterr(),
        .ecc_dbiterr()
    );

endmodule
