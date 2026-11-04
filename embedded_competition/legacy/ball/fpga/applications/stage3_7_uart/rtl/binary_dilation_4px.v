`timescale 1ns / 1ps
// 膨胀：九个邻点至少一个白就输出白；3×3全1结构元素，白色255为前景。
// 仅定义0/255二值输入；完整窗口之外强制黑色，保留帧尺寸。
// 两级寄存：E0计算三行判断，E1输出；每拍四窗口，不支持背压。
module binary_dilation_4px (
    input wire I_clk, // 与Sobel和窗口发生器相同的算法时钟。
    input wire I_rst_n, // 低有效异步复位，清空数据和标记流水。
    input wire [31:0] I_p11, I_p12, I_p13, // 四窗口的上行邻点，高字节对应最左窗口。
    input wire [31:0] I_p21, I_p22, I_p23, // 四窗口的中行邻点，p22是中心。
    input wire [31:0] I_p31, I_p32, I_p33, // 四窗口的下行邻点。
    input wire [3:0] I_window_valid, // bit3最左；0表示不完整邻域，强制黑色。
    input wire I_tvalid, I_tuser, I_tlast, // 有效组、帧首组、行末组。
    input wire [11:0] I_x, I_y, // 本组最左中心的列号和公共行号。
    input wire I_frame_done, // 最后一组标记，必须与像素一起延迟。
    output wire O_tvalid, O_tuser, O_tlast, // 与处理后的四像素严格对齐。
    output wire [11:0] O_x, O_y, // 输出中心坐标。
    output wire O_frame_done, // 本模块的末帧组输出标记。
    output wire [3:0] O_window_valid, // 对齐后的邻域有效掩码。
    output wire [31:0] O_binary_data, // 四个0/255结果，高字节最左。
    output wire [95:0] O_tdata // 四份RGB888，每份三个通道复制同一二值像素。
);
    reg [1:0] S_valid, S_user, S_last, S_done; // 两级标记链，索引0为首级。
    reg [3:0] S_mask [0:1]; // 每级四个独立窗口的有效位。
    reg [11:0] S_x [0:1], S_y [0:1]; // 数据等待时，坐标也要等待。
    integer j; // 两级寄存器的静态循环索引，不是运行时图像计数器。
    // 控制流水：空拍也前进，防止valid气泡使标记错位。
    always @(posedge I_clk or negedge I_rst_n) begin
        if(!I_rst_n) begin
            S_valid<=0; S_user<=0; S_last<=0; S_done<=0;
            for(j=0;j<2;j=j+1) begin
                S_mask[j]<=0; S_x[j]<=0; S_y[j]<=0;
            end
        end else begin
            S_valid<={S_valid[0],I_tvalid}; S_user<={S_user[0],I_tuser};
            S_last<={S_last[0],I_tlast}; S_done<={S_done[0],I_frame_done};
            S_mask[0]<=I_window_valid; S_mask[1]<=S_mask[0];
            S_x[0]<=I_x; S_x[1]<=S_x[0];
            S_y[0]<=I_y; S_y[1]<=S_y[0];
        end
    end
    assign O_tvalid=S_valid[1]; assign O_tuser=S_user[1];
    assign O_tlast=S_last[1]; assign O_frame_done=S_done[1];
    assign O_x=S_x[1]; assign O_y=S_y[1];
    assign O_window_valid=S_mask[1] & {4{S_valid[1]}};
    genvar i; // 四路并行展开；i=0是最低字节，即组内最右像素。
    generate for(i=0;i<4;i=i+1) begin : gen_binary
        reg S_top, S_middle, S_bottom; // 首级分别保存三行的白色条件，各只需1bit。
        reg [7:0] S_pixel; // 第二级保存本路最终0或255，与标记链末级对齐。
        // 数据流水：先判断每行，再合并三行；边界和空拍强制输出0。
        always @(posedge I_clk or negedge I_rst_n) begin
            if(!I_rst_n) begin
                S_top<=0; S_middle<=0; S_bottom<=0; S_pixel<=0;
            end else begin
                S_top <= (I_p11[i*8+:8]==8'hff) | (I_p12[i*8+:8]==8'hff) | (I_p13[i*8+:8]==8'hff); // 只对白色255置位。
                S_middle <= (I_p21[i*8+:8]==8'hff) | (I_p22[i*8+:8]==8'hff) | (I_p23[i*8+:8]==8'hff); // 只对白色255置位。
                S_bottom <= (I_p31[i*8+:8]==8'hff) | (I_p32[i*8+:8]==8'hff) | (I_p33[i*8+:8]==8'hff); // 只对白色255置位。
                if(S_valid[0] && S_mask[0][i]) // 沿前首级标记属于同一组行判断结果。
                    S_pixel <= (S_top | S_middle | S_bottom) ? 8'hff : 8'h00;
                else S_pixel<=0; // 不完整窗口不参与运算，避免边界错误扩展。
            end
        end
        assign O_binary_data[i*8+:8]=S_pixel; // 保持四像素原顺序。
        assign O_tdata[i*24+:24]={S_pixel,S_pixel,S_pixel}; // 纯连线，不新增延迟。
    end endgenerate
endmodule
