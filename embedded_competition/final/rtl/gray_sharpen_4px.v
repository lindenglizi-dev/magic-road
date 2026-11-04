`timescale 1ns/1ps
// 灰度锐化：中心 + (4*中心-四邻点和)/2^DETAIL_SHIFT，负数向下取整后饱和。
// 三层寄存：输入E0采入，E2沿后输出；吞吐每拍四像素；无ready背压。
module gray_sharpen_4px #(parameter integer DETAIL_SHIFT=0)( // 0..3；0保持原来的全强度锐化。
    input wire I_clk,I_rst_n, // 现有算法时钟、低有效异步复位。
    input wire [31:0] I_p11,I_p12,I_p13, // 上行左/中/右邻点，每根总线包含四个窗口的对应像素。
    input wire [31:0] I_p21,I_p22,I_p23, // 中行邻点；每根总线高字节对应最左窗口。
    input wire [31:0] I_p31,I_p32,I_p33, // 下行邻点，与Stage4保持相同接口。
    input wire [3:0] I_window_valid, // bit3对应最左窗口，0时强制输出黑色。
    input wire I_tvalid,I_tuser,I_tlast,I_frame_done, // 组有效/帧首/行末/帧末标记。
    input wire [11:0] I_x,I_y, // 本组最左中心坐标。
    output wire [31:0] O_pixel_data, // 四个饱和后的8bit灰度像素。
    output wire [95:0] O_tdata, // 四份RGB888，分别把结果复制到R/G/B。
    output wire O_tvalid,O_tuser,O_tlast,O_frame_done, // 与结果严格对齐的标记。
    output wire [11:0] O_x,O_y, // 与结果对齐的中心坐标。
    output wire [3:0] O_window_valid // 各窗口是否完整，无效组清0。
);
    reg [2:0] S_valid,S_user,S_last,S_done; // 三层标记流水，与三层计算同步前进。
    reg [3:0] S_mask[0:2]; // 每层四窗口有效位，区别于整组valid。
    reg [11:0] S_x[0:2],S_y[0:2]; // 保存像素在流水期间的身份坐标。
    integer j; // 固定三层数组的循环索引，综合展开成寄存器。
    // 标记每拍移动，包含valid=0的空拍；复位清空旧帧身份。
    always @(posedge I_clk or negedge I_rst_n) begin
        if(!I_rst_n)begin
            S_valid<=0;S_user<=0;S_last<=0;S_done<=0;
            for(j=0;j<3;j=j+1)begin S_mask[j]<=0;S_x[j]<=0;S_y[j]<=0;end
        end else begin
            S_valid<={S_valid[1:0],I_tvalid};S_user<={S_user[1:0],I_tuser};
            S_last<={S_last[1:0],I_tlast};S_done<={S_done[1:0],I_frame_done};
            S_mask[0]<=I_window_valid;S_x[0]<=I_x;S_y[0]<=I_y;
            for(j=1;j<3;j=j+1)begin S_mask[j]<=S_mask[j-1];S_x[j]<=S_x[j-1];S_y[j]<=S_y[j-1];end
        end
    end
    assign O_tvalid=S_valid[2];assign O_tuser=S_user[2];assign O_tlast=S_last[2];assign O_frame_done=S_done[2];
    assign O_x=S_x[2];assign O_y=S_y[2];assign O_window_valid=S_mask[2]&{4{S_valid[2]}};
    genvar i; // i=0是最低字节/最右窗口；四套硬件并行展开。
    generate for(i=0;i<4;i=i+1)begin: gen_pixel
        wire [7:0] p11=I_p11[i*8+:8], p12=I_p12[i*8+:8], p13=I_p13[i*8+:8]; // 本通道三个邻点的组合切片。
        wire [7:0] p21=I_p21[i*8+:8], p22=I_p22[i*8+:8], p23=I_p23[i*8+:8]; // 本通道三个邻点的组合切片。
        wire [7:0] p31=I_p31[i*8+:8], p32=I_p32[i*8+:8], p33=I_p33[i*8+:8]; // 本通道三个邻点的组合切片。
        reg [7:0] S_pixel; // 第三级保存最终像素，匹配标记索引2。
        reg [12:0] S_center_weighted; // 第一级(4+2^shift)*中心；shift<=3时最大3060。
        reg [9:0] S_cross; // 上下左右四邻点和，最大1020，需10bit。
        reg signed [11:0] S_value; // 第二级差值-1020..1275，12bit signed范围足够。
        // 先扩位再移位/相加；负数钳0，超过255钳255，不能直接截断。
        always @(posedge I_clk or negedge I_rst_n)begin
            if(!I_rst_n)begin S_center_weighted<=0;S_cross<=0;S_value<=0;S_pixel<=0;end
            else begin
                S_center_weighted<=({5'b0,p22}<<2)+({5'b0,p22}<<DETAIL_SHIFT);
                S_cross<={2'b0,p12}+{2'b0,p21}+{2'b0,p23}+{2'b0,p32};
                S_value<=($signed(S_center_weighted)-$signed({3'b0,S_cross}))>>>DETAIL_SHIFT;
                if(!S_valid[1] || !S_mask[1][i])S_pixel<=0;
                else if(S_value<12'sd0)S_pixel<=0;
                else if(S_value>12'sd255)S_pixel<=255;
                else S_pixel<=S_value[7:0];
            end
        end
        assign O_pixel_data[i*8+:8]=S_pixel;
        assign O_tdata[i*24+:24]={S_pixel,S_pixel,S_pixel}; // RGB复制为连线，不额外延迟。
    end endgenerate
endmodule
