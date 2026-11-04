`timescale 1ns / 1ps
// Integral builder / 同步RAM单读单写，行前缀加上一行同列积分值。
module face_integral(
    input i_clk,
    input i_rstn,
    input i_clear,
    input i_start,
    input [6:0] i_size,
    output o_gray_read,
    output [11:0] o_gray_address,
    input [7:0] i_gray,
    output o_read,
    output [11:0] o_read_address,
    input [19:0] i_above,
    output o_write,
    output [11:0] o_write_address,
    output [19:0] o_data,
    output o_done
);
    localparam ST_IDLE=0,ST_READ=1,ST_PREFIX=2,ST_ADD=3,ST_WRITE=4,ST_DONE=5;
    reg [2:0] state_current,state_next;
    reg [6:0] reg_size;
    reg [5:0] cnt_x,cnt_y;
    reg [14:0] reg_prefix;
    reg [19:0] reg_above,reg_data_o;
    wire [5:0] wire_above_y=cnt_y-1'b1;
    assign o_gray_read=state_current == ST_READ;
    assign o_gray_address={cnt_y,cnt_x};
    assign o_read=state_current == ST_READ && cnt_y != 0;
    assign o_read_address={wire_above_y,cnt_x};
    assign o_write=state_current == ST_WRITE && !i_clear;
    assign o_write_address={cnt_y,cnt_x};
    assign o_data=reg_data_o;
    assign o_done=state_current == ST_DONE;
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)state_current<=ST_IDLE;
        else if(i_clear)state_current<=ST_IDLE;
        else state_current<=state_next;
    end
    always @(*)begin
        state_next=state_current;
        case(state_current)
            ST_IDLE:if(i_start)state_next=ST_READ;
            ST_READ:state_next=ST_PREFIX;
            ST_PREFIX:state_next=ST_ADD;
            ST_ADD:state_next=ST_WRITE;
            ST_WRITE:state_next=cnt_x+7'd1 == reg_size && cnt_y+7'd1 == reg_size ? ST_DONE : ST_READ;
            ST_DONE:state_next=ST_IDLE;
            default:state_next=ST_IDLE;
        endcase
    end
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin reg_size<=64;cnt_x<=0;cnt_y<=0;reg_prefix<=0;reg_above<=0;reg_data_o<=0;end
        else if(!i_clear)begin
            case(state_current)
                ST_IDLE:if(i_start)begin reg_size<=i_size;cnt_x<=0;cnt_y<=0;reg_prefix<=0;end
                ST_PREFIX:begin
                    reg_prefix<=reg_prefix+i_gray;reg_above<=cnt_y == 0 ? 20'd0 : i_above;
                end
                ST_ADD:reg_data_o<=reg_above+reg_prefix;
                ST_WRITE:if(cnt_x+7'd1 == reg_size)begin cnt_x<=0;cnt_y<=cnt_y+1'b1;reg_prefix<=0;end
                    else cnt_x<=cnt_x+1'b1;
                default:begin end
            endcase
        end
    end
endmodule
