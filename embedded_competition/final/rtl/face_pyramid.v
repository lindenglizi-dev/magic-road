`timescale 1ns / 1ps
// Direct pyramid resize / 每层从原始64x64读取，坐标查表避免可变除法。
module face_pyramid #(
    parameter C_COORDINATES="../rtl/face_rom/coordinates.mem"
)(
    input i_clk,
    input i_rstn,
    input i_clear,
    input i_start,
    input [3:0] i_scale,
    input [6:0] i_size,
    output o_read,
    output [11:0] o_address,
    input [7:0] i_gray,
    output o_write,
    output [11:0] o_write_address,
    output [7:0] o_gray,
    output o_done
);
    localparam ST_IDLE=0,ST_COORD_READ=1,ST_COORD_LOAD=2,ST_READ=3,ST_LOAD=4,
        ST_HORIZONTAL=5,ST_VERTICAL=6,ST_ROUND=7,ST_WRITE=8,ST_DONE=9;
    reg [3:0] state_current,state_next;
    reg [13:0] mem_coordinate[0:703];
    reg [13:0] reg_coord_x,reg_coord_y;
    reg [5:0] cnt_x,cnt_y;
    reg [3:0] reg_scale;
    reg [6:0] reg_size;
    reg [1:0] cnt_corner;
    reg [7:0] reg_pixel_left,reg_pixel_right,reg_pixel_bottom_left,reg_pixel_bottom_right;
    reg [15:0] reg_upper,reg_lower;
    reg [23:0] reg_top_weight;
    reg signed [25:0] reg_bottom_weight;
    reg [24:0] reg_rounded;
    wire [5:0] wire_low_x=reg_coord_x[13:8],wire_low_y=reg_coord_y[13:8];
    wire [5:0] wire_high_x=wire_low_x == 63 ? 6'd63 : wire_low_x+1'b1;
    wire [5:0] wire_high_y=wire_low_y == 63 ? 6'd63 : wire_low_y+1'b1;
    // 差分双线性插值，乘加结果在末级统一舍入。
    wire signed [8:0] wire_upper_delta=$signed({1'b0,reg_pixel_right})-$signed({1'b0,reg_pixel_left});
    wire signed [8:0] wire_lower_delta=$signed({1'b0,reg_pixel_bottom_right})-$signed({1'b0,reg_pixel_bottom_left});
    wire signed [17:0] wire_upper_product=wire_upper_delta*$signed({1'b0,reg_coord_x[7:0]});
    wire signed [17:0] wire_lower_product=wire_lower_delta*$signed({1'b0,reg_coord_x[7:0]});
    wire signed [16:0] wire_vertical_delta=$signed({1'b0,reg_lower})-$signed({1'b0,reg_upper});
    initial $readmemh(C_COORDINATES,mem_coordinate);
    always @(posedge i_clk)begin
        if(state_current == ST_COORD_READ)begin
            reg_coord_x<=mem_coordinate[{reg_scale,cnt_x}];
            reg_coord_y<=mem_coordinate[{reg_scale,cnt_y}];
        end
    end
    assign o_read=state_current == ST_READ;
    assign o_address={cnt_corner[1] ? wire_high_y : wire_low_y,cnt_corner[0] ? wire_high_x : wire_low_x};
    assign o_write=state_current == ST_WRITE && !i_clear;
    assign o_write_address={cnt_y,cnt_x};
    assign o_gray=reg_rounded[23:16];
    assign o_done=state_current == ST_DONE;
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)state_current<=ST_IDLE;
        else if(i_clear)state_current<=ST_IDLE;
        else state_current<=state_next;
    end
    always @(*)begin
        state_next=state_current;
        case(state_current)
            ST_IDLE:if(i_start)state_next=ST_COORD_READ;
            ST_COORD_READ:state_next=ST_COORD_LOAD;
            ST_COORD_LOAD:state_next=ST_READ;
            ST_READ:state_next=ST_LOAD;
            ST_LOAD:state_next=cnt_corner == 3 ? ST_HORIZONTAL : ST_READ;
            ST_HORIZONTAL:state_next=ST_VERTICAL;
            ST_VERTICAL:state_next=ST_ROUND;
            ST_ROUND:state_next=ST_WRITE;
            ST_WRITE:state_next=cnt_x+7'd1 == reg_size && cnt_y+7'd1 == reg_size ? ST_DONE : ST_COORD_READ;
            ST_DONE:state_next=ST_IDLE;
            default:state_next=ST_IDLE;
        endcase
    end
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            cnt_x<=0;cnt_y<=0;reg_scale<=0;reg_size<=64;cnt_corner<=0;
            reg_pixel_left<=0;reg_pixel_right<=0;reg_pixel_bottom_left<=0;reg_pixel_bottom_right<=0;
            reg_upper<=0;reg_lower<=0;reg_top_weight<=0;reg_bottom_weight<=0;reg_rounded<=0;
        end else if(!i_clear)begin
            case(state_current)
                ST_IDLE:if(i_start)begin cnt_x<=0;cnt_y<=0;reg_scale<=i_scale;reg_size<=i_size;end
                ST_COORD_LOAD:cnt_corner<=0;
                ST_LOAD:begin
                    case(cnt_corner)
                        0:reg_pixel_left<=i_gray;
                        1:reg_pixel_right<=i_gray;
                        2:reg_pixel_bottom_left<=i_gray;
                        3:reg_pixel_bottom_right<=i_gray;
                    endcase
                    cnt_corner<=cnt_corner+1'b1;
                end
                ST_HORIZONTAL:begin
                    reg_upper<=$signed({2'b0,reg_pixel_left,8'b0})+wire_upper_product;
                    reg_lower<=$signed({2'b0,reg_pixel_bottom_left,8'b0})+wire_lower_product;
                end
                ST_VERTICAL:begin reg_top_weight<={reg_upper,8'd0};reg_bottom_weight<=wire_vertical_delta*$signed({1'b0,reg_coord_y[7:0]});end
                ST_ROUND:reg_rounded<=$signed({2'b0,reg_top_weight})+reg_bottom_weight+26'sd32768;
                ST_WRITE:if(cnt_x+7'd1 == reg_size)begin cnt_x<=0;cnt_y<=cnt_y+1'b1;end
                    else cnt_x<=cnt_x+1'b1;
                default:begin end
            endcase
        end
    end
endmodule
