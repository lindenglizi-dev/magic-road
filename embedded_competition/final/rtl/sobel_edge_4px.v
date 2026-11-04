`timescale 1ns / 1ps // 仿真时间单位1ns、精度1ps；不生成硬件。
// 四套独立Sobel：对接stage4的九根32位窗口总线，高字节为最左窗口。
// 五级寄存器：加权和→有符号差→绝对值→幅值和→阈值/输出。
// 输入E0采入，在E4后输出；每拍处理四个窗口，无ready/背压。
module sobel_edge_4px #( // 新增算法模块，保留I_/O_/S_命名与低有效复位风格。
    parameter [10:0] THRESHOLD = 11'd128 // 无符号阈值0..2047；边界无论阈值如何都输出0。
)( // 模块端口表开始。
    input wire I_clk, // 与窗口发生器相同的算法时钟，不产生新时钟域。
    input wire I_rst_n, // 低有效异步复位，清空所有流水寄存器。
    input wire [31:0] I_p11, I_p12, I_p13, // 上行左/中/右邻点，各包含四个8位像素。
    input wire [31:0] I_p21, I_p22, I_p23, // 中行邻点；p22权重为0，保留端口以匹配窗口接口。
    input wire [31:0] I_p31, I_p32, I_p33, // 下行左/中/右邻点，各包含四个8位像素。
    input wire [3:0] I_window_valid, // bit3对应最左窗口，0表示边界/不完整窗口。
    input wire I_tvalid, I_tuser, I_tlast, // 组有效、首帧组、末行组标记，均按五级移位。
    input wire [11:0] I_x, I_y, // 窗口中心坐标：x是本组最左列，y是行号。
    input wire I_frame_done, // 来自stage4的末帧组标记，与数据一起延迟。
    output wire O_tvalid, O_tuser, O_tlast, // 延迟五级后的组有效/帧首/行尾。
    output wire [11:0] O_x, O_y, // 延迟五级后的中心坐标。
    output wire O_frame_done, // Sobel最后一组处理完成；不同于上游输入接收busy。
    output wire [3:0] O_window_valid, // 与输出数据对齐的窗口掩码，无效拍清0。
    output wire [31:0] O_edge_data, // 四个8位二值结果，每个为0或255。
    output wire [95:0] O_tdata, // 将每个二值结果复制为RGB888，供后续显示适配。
    output wire [43:0] O_gx, O_gy, // 四个独立11位二补码梯度；总线本身不是单个signed数。
    output wire [43:0] O_magnitude // 四个独立11位无符号|Gx|+|Gy|，用于波形与自检。
); // 端口表结束。
    reg [4:0] S_valid, S_user, S_last, S_done; // 四条五级控制移位链，低索引是最早一级。
    reg [3:0] S_mask [0:4]; // 各流水级的四窗口有效掩码。
    reg [11:0] S_x [0:4], S_y [0:4]; // 各流水级的组中心坐标。
    integer j; // 固定五级寄存器移位循环索引，综合时展开，不是运行时软件循环。
    always @(posedge I_clk or negedge I_rst_n) begin // 每拍移动控制，消隐拍也移动。
        if(!I_rst_n) begin // 异步复位控制通路，避免旧帧标记泄漏。
            S_valid <= 0; S_user <= 0; S_last <= 0; S_done <= 0; // 清空全部控制位。
            for(j=0;j<5;j=j+1) begin // 只清少量流水寄存器，不涉及行RAM。
                S_mask[j] <= 0; S_x[j] <= 0; S_y[j] <= 0; // 清空当前级掩码和坐标。
            end // 复位循环结束。
        end else begin // 正常工作，每个时钟无条件推进。
            S_valid <= {S_valid[3:0],I_tvalid}; // 组有效标记移动一拍。
            S_user <= {S_user[3:0],I_tuser}; // 帧首标记移动一拍，不以valid门控。
            S_last <= {S_last[3:0],I_tlast}; // 行尾标记移动一拍。
            S_done <= {S_done[3:0],I_frame_done}; // 最终帧完成标记移动一拍。
            S_mask[0] <= I_window_valid; S_x[0] <= I_x; S_y[0] <= I_y; // 捕获第一级元数据。
            for(j=1;j<5;j=j+1) begin // 后四级接收上一拍的前一级值。
                S_mask[j] <= S_mask[j-1]; S_x[j] <= S_x[j-1]; S_y[j] <= S_y[j-1]; // 非阻塞赋值确保逐级移动。
            end // 元数据移位循环结束。
        end // 正常工作分支结束。
    end // 控制时序块结束。
    assign O_tvalid=S_valid[4]; // 第五级有效，与阈值输出同拍。
    assign O_tuser=S_user[4]; // 第五级帧首。
    assign O_tlast=S_last[4]; // 第五级行尾。
    assign O_frame_done=S_done[4]; // 第五级帧完成。
    assign O_x=S_x[4]; assign O_y=S_y[4]; // 第五级坐标，不增加额外寄存器。
    assign O_window_valid=S_mask[4] & {4{S_valid[4]}}; // 组无效时对外掩码必须为0。
    genvar i; // 四路静态展开索引，i=0为最低字节/本组最右像素。
    generate for(i=0;i<4;i=i+1) begin : gen_sobel // 每个像素拥有自己的梯度和流水寄存器。
        wire [7:0] p11=I_p11[i*8+:8], p12=I_p12[i*8+:8], p13=I_p13[i*8+:8]; // 提取本路上行三个点。
        wire [7:0] p21=I_p21[i*8+:8], p23=I_p23[i*8+:8]; // 提取本路中行左右点，中心p22不参与运算。
        wire [7:0] p31=I_p31[i*8+:8], p32=I_p32[i*8+:8], p33=I_p33[i*8+:8]; // 提取本路下行三个点。
        reg [9:0] S_right, S_left, S_bottom, S_top; // 每个正权重和最大255+510+255=1020，用10位。
        reg signed [10:0] S_gx, S_gy; // 差值范围-1020..1020，11位signed范围-1024..1023。
        reg [10:0] S_abs_x, S_abs_y; // 两个非负绝对值，最大1020。
        reg [10:0] S_mag; // 幅值和保守上界2040，11位无符号足够，不能截成8位。
        reg signed [10:0] S_gx_d3, S_gy_d3, S_gx_d4, S_gy_d4; // 仅供诊断输出的梯度延迟，跟随绝对值与幅值级。
        reg signed [10:0] S_gx_out, S_gy_out; // 与最终二值结果同拍的梯度诊断寄存器。
        reg [10:0] S_mag_out; // 与最终结果同拍的幅值诊断寄存器。
        reg [7:0] S_edge; // 当前通道的0/255二值像素。
        always @(posedge I_clk or negedge I_rst_n) begin // 本路五级数据流水，均用非阻塞赋值。
            if(!I_rst_n) begin // 异步复位每一级；不允许旧窗口残留至新帧。
                S_right<=0; S_left<=0; S_bottom<=0; S_top<=0; // 清第一级加权和。
                S_gx<=0; S_gy<=0; S_abs_x<=0; S_abs_y<=0; S_mag<=0; // 清第二至第四级算法寄存器。
                S_gx_d3<=0; S_gy_d3<=0; S_gx_d4<=0; S_gy_d4<=0; // 清诊断延迟链。
                S_gx_out<=0; S_gy_out<=0; S_mag_out<=0; S_edge<=0; // 清最终输出。
            end else begin // 正常工作，各表达式读取上一拍寄存值。
                S_right <= {2'b0,p13}+{1'b0,p23,1'b0}+{2'b0,p33}; // 一级：右列加权和，显式10位扩展防止移位溢出。
                S_left <= {2'b0,p11}+{1'b0,p21,1'b0}+{2'b0,p31}; // 一级：左列加权和。
                S_bottom <= {2'b0,p31}+{1'b0,p32,1'b0}+{2'b0,p33}; // 一级：下行加权和。
                S_top <= {2'b0,p11}+{1'b0,p12,1'b0}+{2'b0,p13}; // 一级：上行加权和。
                S_gx <= $signed({1'b0,S_right})-$signed({1'b0,S_left}); // 二级：右减左，先零扩展再解释为signed。
                S_gy <= $signed({1'b0,S_bottom})-$signed({1'b0,S_top}); // 二级：下减上，方向与用户给定Gy一致。
                S_abs_x <= S_gx[10] ? (~S_gx+11'd1) : S_gx; // 三级：负数用二补码取反加1，存为无符号绝对值。
                S_abs_y <= S_gy[10] ? (~S_gy+11'd1) : S_gy; // 三级：Gy的绝对值，范围不含不可表示的-1024。
                S_gx_d3<=S_gx; S_gy_d3<=S_gy; // 三级：诊断梯度跟随绝对值计算。
                S_mag <= S_abs_x+S_abs_y; // 四级：无符号绝对值和，不用平方根或除法。
                S_gx_d4<=S_gx_d3; S_gy_d4<=S_gy_d3; // 四级：诊断梯度跟随幅值计算。
                if(S_valid[3] && S_mask[3][i]) begin // 五级：使用同一窗口的第四级valid和掩码。
                    S_edge <= (S_mag>=THRESHOLD) ? 8'hff : 8'h00; // 大于等于阈值为白，否则为黑。
                    S_gx_out<=S_gx_d4; S_gy_out<=S_gy_d4; S_mag_out<=S_mag; // 输出同一窗口的诊断值。
                end else begin // 无效组或边界窗口：包括THRESHOLD=0也必须黑色。
                    S_edge<=0; S_gx_out<=0; S_gy_out<=0; S_mag_out<=0; // 防止无效数据和旧梯度出现在输出。
                end // 阈值有效性分支结束。
            end // 数据流水正常工作分支结束。
        end // 本路数据时序块结束。
        assign O_edge_data[i*8+:8]=S_edge; // 保留stage4四路像素顺序。
        assign O_tdata[i*24+:24]={S_edge,S_edge,S_edge}; // 灰度复制到RGB三通道，不增加延迟。
        assign O_gx[i*11+:11]=S_gx_out; assign O_gy[i*11+:11]=S_gy_out; // 打包四路二补码，读回时需逐片转signed。
        assign O_magnitude[i*11+:11]=S_mag_out; // 打包四路无符号幅值。
    end endgenerate // 四套电路展开结束。
endmodule // Sobel模块结束。
