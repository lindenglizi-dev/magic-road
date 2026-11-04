`timescale 1ns / 1ps
// Window variance / 窗口方差：484个灰度平方串行累加，34位整数开方。
module face_window_norm(
    input i_clk,
    input i_rstn,
    input i_clear,
    input i_start,
    input [5:0] i_x,
    input [5:0] i_y,
    output o_gray_read,
    output [11:0] o_gray_address,
    input [7:0] i_gray,
    output o_integral_read,
    output [11:0] o_integral_address,
    input [19:0] i_integral,
    output o_done,
    output o_contrast,
    output [16:0] o_root,
    output [33:0] o_variance
);
    localparam ST_IDLE=0,ST_READ=1,ST_SQUARE=2,ST_ACCUMULATE=3,ST_RECT_START=4,
        ST_RECT_WAIT=5,ST_PRODUCTS=6,ST_VARIANCE=7,ST_ROOT_INIT=8,ST_ROOT=9,ST_DONE=10;
    reg [3:0] state_current,state_next;
    reg [5:0] reg_x,reg_y,cnt_x,cnt_y;
    reg [15:0] reg_square;
    reg [24:0] reg_square_sum;
    reg [33:0] reg_weighted,reg_sum_squared,reg_variance,reg_radix;
    reg [16:0] reg_root;
    reg [35:0] reg_remainder;
    reg [4:0] cnt_root;
    wire [35:0] wire_remainder={reg_remainder[33:0],reg_radix[33:32]};
    wire [35:0] wire_trial={17'd0,reg_root,2'b01};
    wire flag_subtract=wire_remainder >= wire_trial;
    wire rectangle_done;
    wire [19:0] rectangle_sum;
    // 22x22x255=123420；有效窗口的像素和不超过17位，无损缩窄乘法器。
    wire [16:0] wire_norm_sum=rectangle_sum[16:0];
    wire [33:0] wire_scaled_difference={reg_square_sum,9'd0}-{4'd0,reg_square_sum,5'd0};
    wire [33:0] wire_scaled_square=wire_scaled_difference+{7'd0,reg_square_sum,2'd0};
    wire [6:0] wire_left={1'b0,reg_x}+7'd1,wire_top={1'b0,reg_y}+7'd1;
    wire [6:0] wire_right={1'b0,reg_x}+7'd23,wire_bottom={1'b0,reg_y}+7'd23;
    wire [5:0] wire_gray_x=reg_x+cnt_x,wire_gray_y=reg_y+cnt_y;
    assign o_gray_read=state_current == ST_READ;
    assign o_gray_address={wire_gray_y,wire_gray_x};
    assign o_done=state_current == ST_DONE;
    assign o_contrast=reg_variance > 34'd23425600;
    assign o_root=reg_root;
    assign o_variance=reg_variance;
    face_rectangle_sum rectangle_Inst(
        .i_clk(i_clk),.i_rstn(i_rstn),.i_clear(i_clear),.i_start(state_current == ST_RECT_START),
        .i_left(wire_left),.i_top(wire_top),.i_right(wire_right),.i_bottom(wire_bottom),
        .o_read(o_integral_read),.o_address(o_integral_address),.i_data(i_integral),
        .o_done(rectangle_done),.o_sum(rectangle_sum));
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)state_current<=ST_IDLE;
        else if(i_clear)state_current<=ST_IDLE;
        else state_current<=state_next;
    end
    always @(*)begin
        state_next=state_current;
        case(state_current)
            ST_IDLE:if(i_start)state_next=ST_READ;
            ST_READ:state_next=ST_SQUARE;
            ST_SQUARE:state_next=ST_ACCUMULATE;
            ST_ACCUMULATE:state_next=cnt_x == 22 && cnt_y == 22 ? ST_RECT_START : ST_READ;
            ST_RECT_START:state_next=ST_RECT_WAIT;
            ST_RECT_WAIT:if(rectangle_done)state_next=ST_PRODUCTS;
            ST_PRODUCTS:state_next=ST_VARIANCE;
            ST_VARIANCE:state_next=ST_ROOT_INIT;
            ST_ROOT_INIT:state_next=ST_ROOT;
            ST_ROOT:if(cnt_root == 16)state_next=ST_DONE;
            ST_DONE:state_next=ST_IDLE;
            default:state_next=ST_IDLE;
        endcase
    end
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            reg_x<=0;reg_y<=0;cnt_x<=1;cnt_y<=1;reg_square<=0;reg_square_sum<=0;
            reg_weighted<=0;reg_sum_squared<=0;reg_variance<=0;reg_radix<=0;
            reg_root<=0;reg_remainder<=0;cnt_root<=0;
        end else if(!i_clear)begin
            case(state_current)
                ST_IDLE:if(i_start)begin
                    reg_x<=i_x;reg_y<=i_y;cnt_x<=1;cnt_y<=1;reg_square_sum<=0;
                end
                ST_SQUARE:reg_square<=i_gray*i_gray;
                ST_ACCUMULATE:begin
                    reg_square_sum<=reg_square_sum+reg_square;
                    if(cnt_x == 22)begin cnt_x<=1;cnt_y<=cnt_y+1'b1;end
                    else cnt_x<=cnt_x+1'b1;
                end
                ST_PRODUCTS:begin
                    reg_weighted<=wire_scaled_square;
                    reg_sum_squared<=wire_norm_sum*wire_norm_sum;
                end
                ST_VARIANCE:reg_variance<=reg_weighted-reg_sum_squared;
                ST_ROOT_INIT:begin
                    reg_radix<=reg_variance;reg_root<=0;reg_remainder<=0;cnt_root<=0;
                end
                ST_ROOT:begin
                    reg_radix<=reg_radix << 2;cnt_root<=cnt_root+1'b1;
                    reg_root<={reg_root[15:0],flag_subtract};
                    reg_remainder<=flag_subtract ? wire_remainder-wire_trial : wire_remainder;
                end
                default:begin end
            endcase
        end
    end
endmodule
