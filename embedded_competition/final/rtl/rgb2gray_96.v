`timescale 1ns / 1ps

// RGB888 四像素并行转灰度，适配官方 AWB 的 96 位像素排列。
// 每个像素独立计算 Gray = (77*R + 150*G + 29*B) >> 8，不合并相邻像素。
// I_tdata[95:72] 为最高位像素，其余依次是 [71:48]、[47:24]、[23:0]。
// 每个 24 位像素均为 {R[7:0], G[7:0], B[7:0]}，输出保持原有顺序。
  
// 时序契约：数据和三个标记均经过 3 级寄存器，无停顿、每拍可接收 4 像素。
// 输入在 E0 上升沿进入乘积寄存器，E1 求和，E2 输出对应的灰度和标记。
// 不提供 ready 握手，不能作为支持任意背压的 AXI4-Stream 模块使用。
// 此 ISP 接口没有独立 hsync/vsync；仅透传原有 tlast/tuser 的电平及脉冲。
// 不根据 valid 裁掉标记，以保留官方可能出现在消隐期的帧/行标记。
module rgb2gray_96 (
    input  wire        I_clk,
    input  wire        I_rst_n,
    input  wire        I_tlast,
    input  wire        I_tuser,
    input  wire [95:0] I_tdata,
    input  wire        I_tvalid,

    output wire        O_tlast,
    output wire        O_tuser,
    output wire [95:0] O_tdata,
    output wire        O_tvalid,
    output wire [31:0] O_gray_data
);

    // 三个标记与像素运算经过相同的三级寄存器，消隐期间也继续移动。
    reg [2:0] S_tlast_delay;
    reg [2:0] S_tuser_delay;
    reg [2:0] S_tvalid_delay;

    always @(posedge I_clk or negedge I_rst_n) begin
        if(!I_rst_n) begin
            S_tlast_delay  <= 3'b000;
            S_tuser_delay  <= 3'b000;
            S_tvalid_delay <= 3'b000;
        end
        else begin
            S_tlast_delay  <= {S_tlast_delay[1:0], I_tlast};
            S_tuser_delay  <= {S_tuser_delay[1:0], I_tuser};
            S_tvalid_delay <= {S_tvalid_delay[1:0], I_tvalid};
        end
    end

    assign O_tlast  = S_tlast_delay[2];
    assign O_tuser  = S_tuser_delay[2];
    assign O_tvalid = S_tvalid_delay[2];

    // generate 在综合时展开成四套并行运算电路，不是运行时循环。
    genvar i;
    generate
        for(i = 0; i < 4; i = i + 1) begin : gen_gray_pixel
            wire [7:0] S_red;
            wire [7:0] S_green;
            wire [7:0] S_blue;

            // 乘积最大值分别为 19635、38250、7395；统一用 16 位无符号数。
            // 总和最大为 255*(77+150+29)=65280，小于 2^16，不会溢出。
            // 本模块的所有像素和权重都是非负数，不需要 signed。
            reg [15:0] S_red_product;
            reg [15:0] S_green_product;
            reg [15:0] S_blue_product;
            reg [15:0] S_gray_sum;
            reg [7:0]  S_gray;

            assign S_red   = I_tdata[i*24+16 +: 8];
            assign S_green = I_tdata[i*24+8  +: 8];
            assign S_blue  = I_tdata[i*24    +: 8];

            // 第一级：将 RGB 与常数权重相乘；显式扩展到 16 位避免表达式截断。
            // 使用常数乘法保留精确整数公式，DSP/LUT 的最终映射由厂商综合决定。
            always @(posedge I_clk or negedge I_rst_n) begin
                if(!I_rst_n) begin
                    S_red_product   <= 16'd0;
                    S_green_product <= 16'd0;
                    S_blue_product  <= 16'd0;
                end
                else begin
                    S_red_product   <= {8'd0, S_red}   * 16'd77;
                    S_green_product <= {8'd0, S_green} * 16'd150;
                    S_blue_product  <= {8'd0, S_blue}  * 16'd29;
                end
            end

            // 第二级：累加上一拍的三个乘积，将乘法和加法分在不同流水级。
            always @(posedge I_clk or negedge I_rst_n) begin
                if(!I_rst_n)
                    S_gray_sum <= 16'd0;
                else
                    S_gray_sum <= S_red_product + S_green_product + S_blue_product;
            end

            // 第三级：取高 8 位，相当于除以 256 并向下取整，不生成除法器。
            // 有效标记来自同一像素的第二级；无效输出置零，标记仍正常传递。
            always @(posedge I_clk or negedge I_rst_n) begin
                if(!I_rst_n)
                    S_gray <= 8'd0;
                else if(S_tvalid_delay[1])
                    S_gray <= S_gray_sum[15:8];
                else
                    S_gray <= 8'd0;
            end

            // 32 位输出供后续窗口使用；96 位输出将灰度复制到 RGB 三通道，
            // 便于后续继续复用官方的 96→128 位打包和 DDR/HDMI 彩色视频通路。
            assign O_gray_data[i*8 +: 8] = S_gray;
            assign O_tdata[i*24 +: 24]   = {S_gray, S_gray, S_gray};
        end
    endgenerate

endmodule
