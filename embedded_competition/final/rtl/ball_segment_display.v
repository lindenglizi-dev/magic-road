`timescale 1ns / 1ps
// Eight-digit board display / 板载八位数码管，CSI时钟使能扫描，无派生时钟。
module ball_segment_display #(
    parameter C_SCAN_CYCLES=25880,
    parameter C_PAGE_SCANS=1000,
    parameter C_BLANK_CYCLES=104
)(
    input i_clk,
    input i_rstn,
    input i_clear,
    input [39:0] i_red_bcd,
    input [39:0] i_green_bcd,
    input [39:0] i_yellow_bcd,
    input i_reject_valid,
    output [7:0] o_select_n,
    output [7:0] o_segments_n,
    output [27:0] o_reject_bcd
);
    localparam C_SCAN_BITS=C_SCAN_CYCLES>1 ? $clog2(C_SCAN_CYCLES) : 1;
    localparam C_PAGE_BITS=C_PAGE_SCANS>1 ? $clog2(C_PAGE_SCANS) : 1;
    reg [C_SCAN_BITS-1:0] cnt_scan;
    reg [C_PAGE_BITS-1:0] cnt_page;
    reg [2:0] reg_digit;
    reg [1:0] reg_page;
    reg [27:0] reg_error_bcd;
                                                                               
    assign o_reject_bcd=reg_error_bcd;
    reg [27:0] reg_frame_bcd;
    reg flag_frame_limit;
    reg [3:0] reg_frame_header;
    reg [7:0] reg_select_n,reg_segments_n;
    reg [39:0] dec_page_bcd;
    reg [27:0] dec_error_next;
    reg flag_carry;
    reg [3:0] dec_symbol;
    reg [7:0] dec_segments;
    integer digit;

    // 错误只接受形状/尺寸筛除的一拍候选事件；十进制进位，9999999饱和。
    always @(*)begin
        dec_error_next=reg_error_bcd;
        flag_carry=1;
        for(digit=0;digit<7;digit=digit+1)begin
            if(flag_carry)begin
                if(reg_error_bcd[digit*4 +:4]==9)begin
                    dec_error_next[digit*4 +:4]=0;
                end else begin
                    dec_error_next[digit*4 +:4]=reg_error_bcd[digit*4 +:4]+4'd1;
                    flag_carry=0;
                end
            end
        end
    end
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin reg_error_bcd<=0;end
        else if(i_clear)begin reg_error_bcd<=0;end
        else if(i_reject_valid && reg_error_bcd!=28'h9999999)begin reg_error_bcd<=dec_error_next;end
    end

    always @(*)begin
        case(reg_page)
            0:dec_page_bcd=i_red_bcd;
            1:dec_page_bcd=i_green_bcd;
            2:dec_page_bcd=i_yellow_bcd;
            default:dec_page_bcd={12'd0,reg_error_bcd};
        endcase
        if(i_clear)begin dec_page_bcd=0;end
        case(reg_digit)
            0:dec_symbol=reg_frame_header;
            1:dec_symbol=reg_frame_bcd[27:24];
            2:dec_symbol=reg_frame_bcd[23:20];
            3:dec_symbol=reg_frame_bcd[19:16];
            4:dec_symbol=reg_frame_bcd[15:12];
            5:dec_symbol=reg_frame_bcd[11:8];
            6:dec_symbol=reg_frame_bcd[7:4];
            default:dec_symbol=reg_frame_bcd[3:0];
        endcase
        case(dec_symbol)
            0:dec_segments=8'hc0;1:dec_segments=8'hf9;
            2:dec_segments=8'ha4;3:dec_segments=8'hb0;
            4:dec_segments=8'h99;5:dec_segments=8'h92;
            6:dec_segments=8'h82;7:dec_segments=8'hf8;
            8:dec_segments=8'h80;9:dec_segments=8'h90;
            10:dec_segments=8'haf;     
            11:dec_segments=8'h82;     
            12:dec_segments=8'h91;     
            13:dec_segments=8'h86;     
            default:dec_segments=8'hff;
        endcase
        if(reg_digit==0 || (reg_digit==7 && flag_frame_limit))begin dec_segments[7]=0;end
    end

    // 每位先全灭约1us，再装段码并等待约1us选通；每轮八位使用同一冻结快照。
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            cnt_scan<=0;cnt_page<=0;reg_digit<=0;reg_page<=0;
            reg_frame_bcd<=0;flag_frame_limit<=0;reg_frame_header<=10;
            reg_select_n<=8'hff;reg_segments_n<=8'hff;
        end else begin
            if(cnt_scan==C_SCAN_CYCLES-1)begin
                cnt_scan<=0;reg_select_n<=8'hff;reg_digit<=reg_digit+1'b1;
                if(reg_digit==7)begin
                    if(cnt_page==C_PAGE_SCANS-1)begin cnt_page<=0;reg_page<=reg_page+1'b1;end
                    else begin cnt_page<=cnt_page+1'b1;end
                end
            end else begin
                cnt_scan<=cnt_scan+1'b1;
                if(cnt_scan==0)begin
                    if(reg_digit==0)begin
                        reg_frame_bcd<=(|dec_page_bcd[39:28]) ? 28'h9999999 : dec_page_bcd[27:0];
                        flag_frame_limit<=(|dec_page_bcd[39:28]) || dec_page_bcd[27:0]==28'h9999999;
                        reg_frame_header<={2'b0,reg_page}+4'd10;
                    end
                end else if(cnt_scan==C_BLANK_CYCLES)begin reg_segments_n<=dec_segments;end
                else if(cnt_scan==2*C_BLANK_CYCLES)begin reg_select_n<=~(8'b1<<reg_digit);end
            end
        end
    end
    assign o_select_n=reg_select_n;
    assign o_segments_n=reg_segments_n;
endmodule
