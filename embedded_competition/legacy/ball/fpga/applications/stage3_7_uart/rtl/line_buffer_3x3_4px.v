`timescale 1ns / 1ps

// 四像素并行、以中心像素为坐标的完整尺寸3x3窗口。
// I_gray_data[31:24]最左，依次到[7:0]最右，直接匹配rgb2gray_96。
// 每个O_pij也以高字节为最左窗口；O_window_valid[3]对应最左窗口。
// 一圈边界保留O_tvalid，但九个邻点置0、window_valid置0。
// 输入tuser允许提前于valid或与首组同拍；tlast允许末有效拍或消隐拍。
// 输出tuser重新生成，与首组有效窗口同拍；tlast与每行末组同拍。
// 输出帧标记语义已规范化，不能未经适配直接驱动官方DDR写FIFO复位。
// 无背压。设G=IMG_WIDTH/4，最后输入沿E后，在E+G+3输出最后一组；
// 下一帧最早在E+G+4采入。等待O_busy降低；否则报协议错误并须复位。
module line_buffer_3x3_4px #(
    parameter integer IMG_WIDTH = 1024, // 必须为4的倍数，4..4096。
    parameter integer IMG_HEIGHT = 600 // 2..4096。
)(
    input wire I_clk,
    input wire I_rst_n,
    input wire [31:0] I_gray_data,
    input wire I_tvalid,
    input wire I_tuser,
    input wire I_tlast,
    output reg [31:0] O_p11, O_p12, O_p13,
    output reg [31:0] O_p21, O_p22, O_p23,
    output reg [31:0] O_p31, O_p32, O_p33,
    output reg [3:0] O_window_valid,
    output reg O_tvalid,
    output reg O_tuser,
    output reg O_tlast,
    output reg [11:0] O_x, // 本组最左中心像素的列号，0,4,8,...。
    output reg [11:0] O_y, // 四个窗口共同的中心行号。
    output wire O_busy,
    output reg O_frame_done,
    output reg O_protocol_error
);
    function integer address_bits;
        input integer depth;
        integer v;
        begin
            v = depth - 1;
            address_bits = 0;
            while(v > 0) begin
                address_bits = address_bits + 1;
                v = v >> 1;
            end
            if(address_bits == 0) address_bits = 1;
        end
    endfunction
    localparam integer GROUPS = IMG_WIDTH / 4;
    localparam integer AW = address_bits(GROUPS);
    localparam [AW-1:0] LAST_GROUP = GROUPS - 1;
    localparam [11:0] LAST_ROW = IMG_HEIGHT - 1;
    localparam [11:0] PENULT_ROW = IMG_HEIGHT - 2;

    // 输入坐标只按有效组推进，valid间隙不会改变像素位置。
    reg S_active;
    reg S_input_done;
    reg [AW-1:0] S_group;
    reg [11:0] S_row;
    wire [AW-1:0] S_in_group = I_tuser ? {AW{1'b0}} : S_group;
    wire [11:0] S_in_row = I_tuser ? 12'd0 : S_row;
    wire S_accept = I_tvalid && (I_tuser || (S_active && !S_input_done));
    assign O_busy = S_active;

    // 第一行RAM返回上一行；第二行RAM在下一拍接收旧行，返回上上行。
    wire [31:0] S_line1_q;
    wire [31:0] S_line2_q;
    reg S_valid_d1, S_valid_d2;
    reg [AW-1:0] S_group_d1, S_group_d2;
    reg [11:0] S_row_d1, S_row_d2;
    reg [31:0] S_current_d1, S_current_d2;
    reg [31:0] S_middle_d2;

    window_line_ram #(.DEPTH(GROUPS), .ADDR_WIDTH(AW)) u_line1 (
        .I_clk(I_clk), .I_en(S_accept && I_rst_n),
        .I_addr(S_in_group), .I_data(I_gray_data), .O_data(S_line1_q)
    );
    window_line_ram #(.DEPTH(GROUPS), .ADDR_WIDTH(AW)) u_line2 (
        .I_clk(I_clk), .I_en(S_valid_d1 && !I_tuser && I_rst_n),
        .I_addr(S_group_d1), .I_data(S_line1_q), .O_data(S_line2_q)
    );

    // 保存尚缺右邻点的一组。下一组到达后，四个中心均有左右邻点。
    reg S_have_group;
    reg [31:0] S_prev_top, S_prev_middle, S_prev_bottom;
    reg [7:0] S_left_top, S_left_middle, S_left_bottom;
    reg [AW-1:0] S_prev_group;
    reg [11:0] S_center_row;
    reg S_bottom_active;
    reg [AW-1:0] S_bottom_group;
    wire S_finish = S_bottom_active && (S_bottom_group == LAST_GROUP);
    wire S_flush = S_have_group && (S_prev_group == LAST_GROUP);
    wire S_emit = S_have_group && (S_flush ||
                  (S_valid_d2 && S_row_d2 != 0 && S_group_d2 != 0));
    // 6个横向位置：左外邻点 + 4个中心位置 + 右外邻点。
    wire [47:0] S_strip_top = {S_left_top, S_prev_top,
                               (S_flush ? 8'd0 : S_line2_q[31:24])};
    wire [47:0] S_strip_middle = {S_left_middle, S_prev_middle,
                                  (S_flush ? 8'd0 : S_middle_d2[31:24])};
    wire [47:0] S_strip_bottom = {S_left_bottom, S_prev_bottom,
                                  (S_flush ? 8'd0 : S_current_d2[31:24])};

    // 第一个always管理输入帧与坐标。输入末行后停止接收，等待输出补齐。
    // 协议错误为粘滞标志：错误帧不保证完整，外部必须复位重新开始。
    always @(posedge I_clk or negedge I_rst_n) begin
        if(!I_rst_n) begin
            S_active <= 1'b0;
            S_input_done <= 1'b0;
            S_group <= 0;
            S_row <= 0;
            O_protocol_error <= 1'b0;
        end
        else begin
            if(S_finish) S_active <= 1'b0;
            if(I_tuser) begin
                if(S_active) O_protocol_error <= 1'b1;
                S_active <= 1'b1;
                S_input_done <= 1'b0;
                S_group <= 0;
                S_row <= 0;
            end
            if(I_tvalid && !S_accept) O_protocol_error <= 1'b1;
            if(I_tvalid && I_tlast && S_in_group != LAST_GROUP)
                O_protocol_error <= 1'b1;
            if(S_accept) begin
                if(S_in_group == LAST_GROUP) begin
                    S_group <= 0;
                    if(S_in_row == LAST_ROW) S_input_done <= 1'b1;
                    else S_row <= S_in_row + 12'd1;
                end
                else S_group <= S_in_group + 1'b1;
            end
        end
    end

    // 两级RAM读流水：在E0取第一行，在E1取第二行并补齐当前/中间行延迟。
    // RAM内容不清零；前两行的有效性由坐标屏蔽，防止上帧旧像素泄漏。
    always @(posedge I_clk or negedge I_rst_n) begin
        if(!I_rst_n) begin
            S_valid_d1 <= 0; S_valid_d2 <= 0;
            S_group_d1 <= 0; S_group_d2 <= 0;
            S_row_d1 <= 0; S_row_d2 <= 0;
            S_current_d1 <= 0; S_current_d2 <= 0; S_middle_d2 <= 0;
        end
        else begin
            S_valid_d1 <= S_accept;
            S_group_d1 <= S_in_group;
            S_row_d1 <= S_in_row;
            S_current_d1 <= I_gray_data;
            S_valid_d2 <= I_tuser ? 1'b0 : S_valid_d1;
            S_group_d2 <= S_group_d1;
            S_row_d2 <= S_row_d1;
            S_current_d2 <= S_current_d1;
            S_middle_d2 <= S_line1_q;
        end
    end

    integer k;
    // 窗口输出级：寄存窗口与坐标/标记，所有输出由同一组条件更新。
    // 行末无右侧像素，因此不等待下一行，自动输出末组并屏蔽最后一列。
    // 末帧后生成整行黑边，保持输出总尺寸仍为IMG_WIDTH*IMG_HEIGHT。
    always @(posedge I_clk or negedge I_rst_n) begin
        if(!I_rst_n) begin
            S_have_group <= 0;
            S_prev_top <= 0; S_prev_middle <= 0; S_prev_bottom <= 0;
            S_left_top <= 0; S_left_middle <= 0; S_left_bottom <= 0;
            S_prev_group <= 0; S_center_row <= 0;
            S_bottom_active <= 0; S_bottom_group <= 0;
            O_p11 <= 0; O_p12 <= 0; O_p13 <= 0;
            O_p21 <= 0; O_p22 <= 0; O_p23 <= 0;
            O_p31 <= 0; O_p32 <= 0; O_p33 <= 0;
            O_window_valid <= 0; O_tvalid <= 0; O_tuser <= 0; O_tlast <= 0;
            O_x <= 0; O_y <= 0; O_frame_done <= 0;
        end
        else begin
            O_p11 <= 0; O_p12 <= 0; O_p13 <= 0;
            O_p21 <= 0; O_p22 <= 0; O_p23 <= 0;
            O_p31 <= 0; O_p32 <= 0; O_p33 <= 0;
            O_window_valid <= 0; O_tvalid <= 0; O_tuser <= 0; O_tlast <= 0;
            O_x <= 0; O_y <= 0; O_frame_done <= 0;
            if(I_tuser) begin
                S_have_group <= 0;
                S_bottom_active <= 0;
                S_bottom_group <= 0;
                S_left_top <= 0; S_left_middle <= 0; S_left_bottom <= 0;
            end
            else if(S_bottom_active) begin
                // 只有最后一行采用合成输出，不对RAM做虚拟写入。
                O_tvalid <= 1'b1;
                O_tlast <= (S_bottom_group == LAST_GROUP);
                O_x <= S_bottom_group * 12'd4;
                O_y <= LAST_ROW;
                if(S_finish) begin
                    S_bottom_active <= 0;
                    S_bottom_group <= 0;
                    O_frame_done <= 1'b1;
                end
                else S_bottom_group <= S_bottom_group + 1'b1;
            end
            else begin
                if(S_emit) begin
                    O_tvalid <= 1'b1;
                    O_tuser <= (S_center_row == 0 && S_prev_group == 0);
                    O_tlast <= (S_prev_group == LAST_GROUP);
                    O_x <= S_prev_group * 12'd4;
                    O_y <= S_center_row;
                    for(k = 0; k < 4; k = k + 1) begin
                        // 边界整个窗口清零，而不是只填缺失邻点，确保最终黑边。
                        if(S_center_row != 0 && S_center_row != LAST_ROW &&
                           !(S_prev_group == 0 && k == 0) &&
                           !(S_prev_group == LAST_GROUP && k == 3)) begin
                            O_window_valid[3-k] <= 1'b1;
                            O_p11[31-k*8 -: 8] <= S_strip_top[47-k*8 -: 8];
                            O_p12[31-k*8 -: 8] <= S_strip_top[39-k*8 -: 8];
                            O_p13[31-k*8 -: 8] <= S_strip_top[31-k*8 -: 8];
                            O_p21[31-k*8 -: 8] <= S_strip_middle[47-k*8 -: 8];
                            O_p22[31-k*8 -: 8] <= S_strip_middle[39-k*8 -: 8];
                            O_p23[31-k*8 -: 8] <= S_strip_middle[31-k*8 -: 8];
                            O_p31[31-k*8 -: 8] <= S_strip_bottom[47-k*8 -: 8];
                            O_p32[31-k*8 -: 8] <= S_strip_bottom[39-k*8 -: 8];
                            O_p33[31-k*8 -: 8] <= S_strip_bottom[31-k*8 -: 8];
                        end
                    end
                    S_have_group <= 0;
                    if(S_flush && S_center_row == PENULT_ROW) begin
                        S_bottom_active <= 1'b1;
                        S_bottom_group <= 0;
                    end
                end
                if(S_valid_d2 && S_row_d2 != 0) begin
                    // 保存新组；在连续输入时允许同拍输出旧组并装入新组。
                    S_have_group <= 1'b1;
                    S_prev_top <= S_line2_q;
                    S_prev_middle <= S_middle_d2;
                    S_prev_bottom <= S_current_d2;
                    S_prev_group <= S_group_d2;
                    S_center_row <= S_row_d2 - 12'd1;
                    S_left_top <= (S_group_d2 == 0) ? 8'd0 : S_prev_top[7:0];
                    S_left_middle <= (S_group_d2 == 0) ? 8'd0 : S_prev_middle[7:0];
                    S_left_bottom <= (S_group_d2 == 0) ? 8'd0 : S_prev_bottom[7:0];
                end
            end
        end
    end

    // synthesis translate_off
    initial begin
        if(IMG_WIDTH < 4 || IMG_WIDTH > 4096 || IMG_WIDTH % 4 != 0 ||
           IMG_HEIGHT < 2 || IMG_HEIGHT > 4096) begin
            $display("ERROR: unsupported window dimensions %0dx%0d", IMG_WIDTH, IMG_HEIGHT);
            $finish;
        end
    end
    // synthesis translate_on
endmodule

