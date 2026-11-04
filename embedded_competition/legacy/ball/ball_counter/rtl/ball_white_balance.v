`timescale 1ns / 1ps
// 中性样本统计和共享逐位除法；只在完整帧边界更新有界增益。
module ball_white_balance #(parameter C_MIN_SAMPLES=64,parameter C_WHITE_CARD=0)(
    input i_clk,input i_rstn,input [95:0] i_rgb,input i_valid,input i_early,
    output [19:0] o_gain_red,output [19:0] o_gain_blue,output o_ready
);
    reg [31:0] sum_red,sum_green,sum_blue;
    reg [21:0] cnt_samples;
    reg [9:0] inc_red,inc_green,inc_blue,low_value,high_value;
    reg [2:0] inc_samples;
    reg [7:0] red,green,blue;
    reg [95:0] reg_rgb_first;
    reg reg_valid_first,reg_valid_second,reg_valid_third;
    reg reg_early_first,reg_early_second,reg_early_third;
    reg [7:0] dec_red[0:3],dec_green[0:3],dec_blue[0:3];
    reg [7:0] reg_red[0:3],reg_green[0:3],reg_blue[0:3];
    reg [3:0] dec_samples,reg_samples;
    integer lane;
    always @(*)begin
        red=0;green=0;blue=0;low_value=0;high_value=0;dec_samples=0;
        for(lane=0;lane<4;lane=lane+1)begin
            red=reg_rgb_first[95-lane*24 -:8];green=reg_rgb_first[87-lane*24 -:8];blue=reg_rgb_first[79-lane*24 -:8];
            low_value=red < green ? red : green;
            if(blue < low_value)begin low_value=blue;end
            high_value=red > green ? red : green;
            if(blue > high_value)begin high_value=blue;end
            // 白纸档由用户保证中心区域是白纸，允许更大的色偏；仍拒绝过暗和饱和样本。
            dec_samples[lane]=C_WHITE_CARD ?
                (low_value >= 16 && high_value <= 248 && high_value <= (low_value << 1)) :
                (low_value >= 16 && high_value <= 224 && (high_value << 1) <= low_value+(low_value << 1));
            dec_red[lane]=dec_samples[lane] ? red : 8'd0;
            dec_green[lane]=dec_samples[lane] ? green : 8'd0;
            dec_blue[lane]=dec_samples[lane] ? blue : 8'd0;
        end
    end
    integer pixel;
    // 只给统计分支加三级寄存；RGB视频本身仍走原RAM延迟链。
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            reg_rgb_first<=0;reg_valid_first<=0;reg_valid_second<=0;reg_valid_third<=0;
            reg_early_first<=0;reg_early_second<=0;reg_early_third<=0;
            reg_samples<=0;inc_red<=0;inc_green<=0;inc_blue<=0;inc_samples<=0;
            for(pixel=0;pixel<4;pixel=pixel+1)begin reg_red[pixel]<=0;reg_green[pixel]<=0;reg_blue[pixel]<=0;end
        end else begin
            reg_rgb_first<=i_rgb;reg_valid_first<=i_valid;reg_valid_second<=reg_valid_first;reg_valid_third<=reg_valid_second;
            reg_early_first<=i_early;reg_early_second<=reg_early_first;reg_early_third<=reg_early_second;
            for(pixel=0;pixel<4;pixel=pixel+1)begin reg_red[pixel]<=dec_red[pixel];reg_green[pixel]<=dec_green[pixel];reg_blue[pixel]<=dec_blue[pixel];end
            reg_samples<=dec_samples;
            inc_red<=(reg_red[0]+reg_red[1])+(reg_red[2]+reg_red[3]);
            inc_green<=(reg_green[0]+reg_green[1])+(reg_green[2]+reg_green[3]);
            inc_blue<=(reg_blue[0]+reg_blue[1])+(reg_blue[2]+reg_blue[3]);
            inc_samples<=reg_samples[0]+reg_samples[1]+reg_samples[2]+reg_samples[3];
        end
    end
    localparam ST_IDLE=0,ST_RED=1,ST_BLUE=2;
    reg [1:0] state_current,state_next;
    reg [31:0] reg_denominator,reg_blue_sum;
    reg [47:0] reg_quotient,reg_numerator;
    reg [32:0] reg_remainder;
    reg [5:0] cnt_bits;
    reg [19:0] reg_gain_red,reg_gain_blue,reg_target_red,reg_target_blue;
    reg flag_pending,flag_ready;
    wire [32:0] wire_shift={reg_remainder[31:0],reg_quotient[47]};
    wire flag_subtract=wire_shift >= {1'b0,reg_denominator};
    wire [32:0] wire_remainder=flag_subtract ? wire_shift-{1'b0,reg_denominator} : wire_shift;
    wire [47:0] wire_quotient={reg_quotient[46:0],flag_subtract};
    wire [19:0] wire_clamped=wire_quotient < 48'd32768 ? 20'd32768 :
                                wire_quotient > 48'd131072 ? 20'd131072 : wire_quotient[19:0];
    wire flag_start=reg_early_third && cnt_samples >= C_MIN_SAMPLES && sum_red != 0 && sum_blue != 0;
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin state_current<=ST_IDLE;end
        else begin state_current<=state_next;end
    end
    always @(*)begin
        state_next=state_current;
        case(state_current)
            ST_IDLE:if(flag_start)begin state_next=ST_RED;end
            ST_RED:if(cnt_bits == 1)begin state_next=ST_BLUE;end
            ST_BLUE:if(cnt_bits == 1)begin state_next=ST_IDLE;end
            default:state_next=ST_IDLE;
        endcase
    end
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            sum_red<=0;sum_green<=0;sum_blue<=0;cnt_samples<=0;
            reg_denominator<=0;reg_blue_sum<=0;reg_quotient<=0;reg_numerator<=0;reg_remainder<=0;cnt_bits<=0;
            reg_gain_red<=65536;reg_gain_blue<=65536;reg_target_red<=65536;reg_target_blue<=65536;
            flag_pending<=0;flag_ready<=0;
        end else begin
            if(reg_early_third)begin
                sum_red<=reg_valid_third ? inc_red : 10'd0;sum_green<=reg_valid_third ? inc_green : 10'd0;sum_blue<=reg_valid_third ? inc_blue : 10'd0;
                cnt_samples<=reg_valid_third ? inc_samples : 3'd0;
                if(flag_pending)begin
                    if(C_WHITE_CARD)begin reg_gain_red<=reg_target_red;end
                    else if(reg_target_red >= reg_gain_red)begin reg_gain_red<=reg_gain_red+((reg_target_red-reg_gain_red) >> 2);end
                    else begin reg_gain_red<=reg_gain_red-((reg_gain_red-reg_target_red) >> 2);end
                    if(C_WHITE_CARD)begin reg_gain_blue<=reg_target_blue;end
                    else if(reg_target_blue >= reg_gain_blue)begin reg_gain_blue<=reg_gain_blue+((reg_target_blue-reg_gain_blue) >> 2);end
                    else begin reg_gain_blue<=reg_gain_blue-((reg_gain_blue-reg_target_blue) >> 2);end
                    flag_pending<=0;flag_ready<=1;
                end
            end else if(reg_valid_third)begin
                sum_red<=sum_red+inc_red;sum_green<=sum_green+inc_green;sum_blue<=sum_blue+inc_blue;
                cnt_samples<=cnt_samples+inc_samples;
            end
            case(state_current)
                ST_IDLE:if(flag_start)begin
                    reg_denominator<=sum_red;reg_blue_sum<=sum_blue;reg_quotient<={sum_green,16'd0};
                    reg_numerator<={sum_green,16'd0};reg_remainder<=0;cnt_bits<=48;
                end
                ST_RED:begin
                    reg_remainder<=wire_remainder;reg_quotient<=wire_quotient;cnt_bits<=cnt_bits-1'b1;
                    if(cnt_bits == 1)begin
                        reg_target_red<=wire_clamped;reg_denominator<=reg_blue_sum;
                        reg_quotient<=reg_numerator;reg_remainder<=0;cnt_bits<=48;
                    end
                end
                ST_BLUE:begin
                    reg_remainder<=wire_remainder;reg_quotient<=wire_quotient;cnt_bits<=cnt_bits-1'b1;
                    if(cnt_bits == 1)begin reg_target_blue<=wire_clamped;flag_pending<=1;end
                end
                default:begin end
            endcase
        end
    end
    assign o_gain_red=reg_gain_red;
    assign o_gain_blue=reg_gain_blue;
    assign o_ready=flag_ready;
endmodule
