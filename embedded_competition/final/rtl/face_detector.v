`timescale 1ns / 1ps
// Face detector / 单核心处理可移动256区域，保持11个尺度与5496窗口。
module face_detector #(
    parameter C_STUMPS="../rtl/face_rom/stumps.mem",C_STAGES="../rtl/face_rom/stages.mem",
    parameter C_COORDINATES="../rtl/face_rom/coordinates.mem"
)(
    input i_clk,
    input i_rstn,
    input i_clear,
    input i_enable,
    input [2:0] i_request_roi,
    input [11:0] i_request_x,
    input [95:0] i_rgb,
    input i_valid,
    input i_sof,
    input i_eof,
    input i_error,
    input [11:0] i_x,
    input [11:0] i_y,
    input [15:0] i_epoch,
    output o_busy,
    output o_done,
    output o_positive,
    output o_fault,
    output [31:0] o_sample,
    output [15:0] o_epoch,
    output [31:0] o_cycles,
    output [11:0] o_left,
    output [11:0] o_top,
    output [11:0] o_right,
    output [11:0] o_bottom,
    output [7:0] o_raw_count,
    output [2:0] o_roi_id,
    output o_capture_accept
);
    localparam ST_CAPTURE=0,ST_PYRAMID_START=1,ST_PYRAMID_WAIT=2,ST_INTEGRAL_START=3,
        ST_INTEGRAL_WAIT=4,ST_NORM_START=5,ST_NORM_WAIT=6,ST_HAAR_START=7,ST_HAAR_WAIT=8,
        ST_MAP_INIT=9,ST_MAP_START=10,ST_MAP_WAIT=11,ST_CANDIDATE=12,ST_WINDOW_NEXT=13,
        ST_MERGE_START=14,ST_MERGE_WAIT=15,ST_DONE=16;
    reg [4:0] state_current,state_next;
    reg [3:0] cnt_scale;
    reg [6:0] dec_size;
    reg [5:0] cnt_x,cnt_y;
    reg [31:0] reg_sample_o,cnt_cycles;
    reg [15:0] reg_epoch_o;
    reg [2:0] reg_roi_o;
    reg [11:0] reg_origin_x;
    reg flag_fault;
    reg [1:0] cnt_map;
    reg [19:0] reg_numerator;
    reg [8:0] reg_mapped_x,reg_mapped_y,reg_mapped_width;
    reg [8:0] reg_box_x,reg_box_y,reg_box_width,reg_box_height;
    reg [7:0] reg_support;
    wire capture_write,capture_done,capture_fault;
    wire [11:0] capture_address;
    wire [7:0] capture_gray;
    wire [31:0] capture_sample;
    wire [15:0] capture_epoch;
    wire [2:0] capture_roi;
    wire [11:0] capture_origin;
    wire pyramid_read,pyramid_write,pyramid_done;
    wire [11:0] pyramid_address,pyramid_write_address;
    wire [7:0] pyramid_gray,base_gray,working_gray;
    wire integral_gray_read,integral_read,integral_write,integral_done;
    wire [11:0] integral_gray_address,integral_read_address,integral_write_address;
    wire [19:0] integral_write_data,integral_data;
    wire norm_gray_read,norm_integral_read,norm_done,norm_contrast;
    wire [11:0] norm_gray_address,norm_integral_address;
    wire [16:0] norm_root;
    wire [33:0] norm_variance;
    wire haar_read,haar_done,haar_positive,haar_fault;
    wire [11:0] haar_address;
    wire divide_done;
    wire [19:0] divide_quotient;
    wire merge_done,merge_positive,merge_overflow,merge_box_valid;
    wire [8:0] merge_x,merge_y,merge_width,merge_height;
    wire [7:0] merge_support;
    wire flag_abort=i_clear || !i_enable;
    wire flag_base_read=pyramid_read || (cnt_scale == 0 && (integral_gray_read || norm_gray_read));
    wire [11:0] wire_image_address=integral_gray_read ? integral_gray_address : norm_gray_address;
    wire [11:0] wire_base_address=pyramid_read ? pyramid_address : wire_image_address;
    wire flag_integral_read=integral_read || norm_integral_read || haar_read;
    wire [11:0] wire_integral_address=integral_read ? integral_read_address :
        (norm_integral_read ? norm_integral_address : haar_address);
    wire [7:0] wire_image_gray=cnt_scale == 0 ? base_gray : working_gray;
    assign o_busy=state_current != ST_CAPTURE;
    assign o_done=(state_current == ST_DONE || capture_fault) && i_enable && !i_clear;
    assign o_positive=merge_positive && !flag_fault && !merge_overflow && !capture_fault;
    assign o_fault=flag_fault || merge_overflow || capture_fault;
    assign o_sample=capture_fault ? capture_sample : reg_sample_o;
    assign o_epoch=capture_fault ? capture_epoch : reg_epoch_o;
    assign o_roi_id=capture_fault ? capture_roi : reg_roi_o;
    assign o_cycles=cnt_cycles;
    assign o_left=reg_origin_x+reg_box_x;assign o_top=12'd232+reg_box_y;
    assign o_right=reg_origin_x+reg_box_x+reg_box_width-12'd1;
    assign o_bottom=12'd231+reg_box_y+reg_box_height;
    always @(*)begin
        case(cnt_scale)
            0:dec_size=64;1:dec_size=58;2:dec_size=53;3:dec_size=48;4:dec_size=44;5:dec_size=40;
            6:dec_size=36;7:dec_size=33;8:dec_size=30;9:dec_size=27;10:dec_size=24;default:dec_size=24;
        endcase
    end
    face_roi_capture capture_Inst(.i_clk(i_clk),.i_rstn(i_rstn),.i_clear(flag_abort),
        .i_arm(state_current == ST_CAPTURE && i_enable && !capture_done && !capture_fault),
        .i_roi_id(i_request_roi),.i_origin_x(i_request_x),.i_valid(i_valid),.i_sof(i_sof),.i_eof(i_eof),
        .i_error(i_error),.i_x(i_x),.i_y(i_y),.i_rgb(i_rgb),.i_epoch(i_epoch),
        .o_write(capture_write),.o_address(capture_address),.o_gray(capture_gray),.o_done(capture_done),
        .o_sample(capture_sample),.o_epoch(capture_epoch),.o_fault(capture_fault),
        .o_accept(o_capture_accept),.o_roi_id(capture_roi),.o_origin_x(capture_origin));
    ball_component_store #(.C_DEPTH(4096),.C_ADDR_BITS(12),.C_DATA_BITS(8)) base_Inst(
        .i_clk(i_clk),.i_read_enable(flag_base_read),.i_read_address(wire_base_address),
        .i_write_enable(capture_write),.i_write_address(capture_address),.i_write_data(capture_gray),.o_read_data(base_gray));
    face_pyramid #(.C_COORDINATES(C_COORDINATES)) pyramid_Inst(.i_clk(i_clk),.i_rstn(i_rstn),.i_clear(flag_abort),
        .i_start(state_current == ST_PYRAMID_START),.i_scale(cnt_scale),.i_size(dec_size),
        .o_read(pyramid_read),.o_address(pyramid_address),.i_gray(base_gray),
        .o_write(pyramid_write),.o_write_address(pyramid_write_address),.o_gray(pyramid_gray),.o_done(pyramid_done));
    ball_component_store #(.C_DEPTH(4096),.C_ADDR_BITS(12),.C_DATA_BITS(8)) working_Inst(
        .i_clk(i_clk),.i_read_enable(integral_gray_read || norm_gray_read),.i_read_address(wire_image_address),
        .i_write_enable(pyramid_write),.i_write_address(pyramid_write_address),.i_write_data(pyramid_gray),.o_read_data(working_gray));
    face_integral integral_Inst(.i_clk(i_clk),.i_rstn(i_rstn),.i_clear(flag_abort),
        .i_start(state_current == ST_INTEGRAL_START),.i_size(dec_size),
        .o_gray_read(integral_gray_read),.o_gray_address(integral_gray_address),.i_gray(wire_image_gray),
        .o_read(integral_read),.o_read_address(integral_read_address),.i_above(integral_data),
        .o_write(integral_write),.o_write_address(integral_write_address),.o_data(integral_write_data),.o_done(integral_done));
    ball_component_store #(.C_DEPTH(4096),.C_ADDR_BITS(12),.C_DATA_BITS(20)) integral_store_Inst(
        .i_clk(i_clk),.i_read_enable(flag_integral_read),.i_read_address(wire_integral_address),
        .i_write_enable(integral_write),.i_write_address(integral_write_address),.i_write_data(integral_write_data),.o_read_data(integral_data));
    face_window_norm norm_Inst(.i_clk(i_clk),.i_rstn(i_rstn),.i_clear(flag_abort),.i_start(state_current == ST_NORM_START),
        .i_x(cnt_x),.i_y(cnt_y),.o_gray_read(norm_gray_read),.o_gray_address(norm_gray_address),.i_gray(wire_image_gray),
        .o_integral_read(norm_integral_read),.o_integral_address(norm_integral_address),.i_integral(integral_data),
        .o_done(norm_done),.o_contrast(norm_contrast),.o_root(norm_root),.o_variance(norm_variance));
    face_haar_core #(.C_STUMPS(C_STUMPS),.C_STAGES(C_STAGES)) haar_Inst(
        .i_clk(i_clk),.i_rstn(i_rstn),.i_clear(flag_abort),.i_start(state_current == ST_HAAR_START),
        .i_x(cnt_x),.i_y(cnt_y),.i_root(norm_root),.o_read(haar_read),.o_address(haar_address),.i_data(integral_data),
        .o_done(haar_done),.o_positive(haar_positive),.o_fault(haar_fault),
        .o_trace(),.o_weak_index(),.o_feature(),.o_take_right(),.o_score(),.o_reject_stage());
    face_unsigned_divide map_Inst(.i_clk(i_clk),.i_rstn(i_rstn),.i_clear(flag_abort),
        .i_start(state_current == ST_MAP_START),.i_numerator(reg_numerator),.i_denominator({1'b0,dec_size,1'b0}),
        .o_done(divide_done),.o_quotient(divide_quotient));
    face_candidate_merge merge_Inst(.i_clk(i_clk),.i_rstn(i_rstn),
        .i_clear(flag_abort || capture_done),.i_add(state_current == ST_CANDIDATE),
        .i_x(reg_mapped_x),.i_y(reg_mapped_y),.i_width(reg_mapped_width),.i_height(reg_mapped_width),
        .i_start(state_current == ST_MERGE_START),.o_done(merge_done),.o_positive(merge_positive),
        .o_overflow(merge_overflow),.o_raw_count(o_raw_count),.o_box_valid(merge_box_valid),
        .o_x(merge_x),.o_y(merge_y),.o_width(merge_width),.o_height(merge_height),.o_support(merge_support));
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)state_current<=ST_CAPTURE;
        else if(flag_abort)state_current<=ST_CAPTURE;
        else state_current<=state_next;
    end
    always @(*)begin
        state_next=state_current;
        case(state_current)
            ST_CAPTURE:if(capture_done)state_next=ST_INTEGRAL_START;
            ST_PYRAMID_START:state_next=ST_PYRAMID_WAIT;
            ST_PYRAMID_WAIT:if(pyramid_done)state_next=ST_INTEGRAL_START;
            ST_INTEGRAL_START:state_next=ST_INTEGRAL_WAIT;
            ST_INTEGRAL_WAIT:if(integral_done)state_next=ST_NORM_START;
            ST_NORM_START:state_next=ST_NORM_WAIT;
            ST_NORM_WAIT:if(norm_done)state_next=norm_contrast ? ST_HAAR_START : ST_WINDOW_NEXT;
            ST_HAAR_START:state_next=ST_HAAR_WAIT;
            ST_HAAR_WAIT:if(haar_done)state_next=haar_fault ? ST_DONE : (haar_positive ? ST_MAP_INIT : ST_WINDOW_NEXT);
            ST_MAP_INIT:state_next=ST_MAP_START;
            ST_MAP_START:state_next=ST_MAP_WAIT;
            ST_MAP_WAIT:if(divide_done)state_next=cnt_map == 2 ? ST_CANDIDATE : ST_MAP_START;
            ST_CANDIDATE:state_next=ST_WINDOW_NEXT;
            ST_WINDOW_NEXT:if(cnt_x+7'd24 == dec_size && cnt_y+7'd24 == dec_size)
                state_next=cnt_scale == 10 ? ST_MERGE_START : ST_PYRAMID_START;
                else state_next=ST_NORM_START;
            ST_MERGE_START:state_next=ST_MERGE_WAIT;
            ST_MERGE_WAIT:if(merge_done)state_next=ST_DONE;
            ST_DONE:state_next=ST_CAPTURE;
            default:state_next=ST_CAPTURE;
        endcase
    end
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            cnt_scale<=0;cnt_x<=0;cnt_y<=0;reg_sample_o<=0;reg_epoch_o<=0;cnt_cycles<=0;flag_fault<=0;reg_roi_o<=0;reg_origin_x<=512;
            cnt_map<=0;reg_numerator<=0;reg_mapped_x<=0;reg_mapped_y<=0;reg_mapped_width<=0;
            reg_box_x<=0;reg_box_y<=0;reg_box_width<=0;reg_box_height<=0;reg_support<=0;
        end else if(!flag_abort)begin
            if(state_current != ST_CAPTURE && state_current != ST_DONE)cnt_cycles<=cnt_cycles+1'b1;
            if(capture_done)begin
                cnt_scale<=0;cnt_x<=0;cnt_y<=0;reg_sample_o<=capture_sample;reg_epoch_o<=capture_epoch;
                reg_roi_o<=capture_roi;reg_origin_x<=capture_origin;
                cnt_cycles<=0;flag_fault<=0;reg_support<=0;reg_box_width<=0;reg_box_height<=0;
            end
            if(haar_done && haar_fault)flag_fault<=1;
            case(state_current)
                ST_MAP_INIT:begin cnt_map<=0;reg_numerator<=({14'd0,cnt_x} << 9)+dec_size;end
                ST_MAP_WAIT:if(divide_done)begin
                    cnt_map<=cnt_map+1'b1;
                    case(cnt_map)
                        0:begin reg_mapped_x<=divide_quotient[8:0];reg_numerator<=({14'd0,cnt_y} << 9)+dec_size;end
                        1:begin reg_mapped_y<=divide_quotient[8:0];reg_numerator<=20'd12288+dec_size;end
                        2:reg_mapped_width<=divide_quotient[8:0];
                    endcase
                end
                ST_WINDOW_NEXT:begin
                    if(cnt_x+7'd24 == dec_size)begin
                        cnt_x<=0;
                        if(cnt_y+7'd24 == dec_size)begin cnt_y<=0;cnt_scale<=cnt_scale+1'b1;end
                        else cnt_y<=cnt_y+1'b1;
                    end else cnt_x<=cnt_x+1'b1;
                end
                default:begin end
            endcase
            if(merge_box_valid && merge_support > reg_support)begin
                reg_box_x<=merge_x;reg_box_y<=merge_y;reg_box_width<=merge_width;reg_box_height<=merge_height;reg_support<=merge_support;
            end
        end
    end
endmodule
