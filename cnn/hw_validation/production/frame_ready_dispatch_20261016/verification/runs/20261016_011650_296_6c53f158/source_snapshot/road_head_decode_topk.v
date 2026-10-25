`timescale 1ns / 1ps
// 固定三尺度输入、共享查表、串行分数与两类原地候选处理。
module road_head_decode_topk(
    input i_clk,
    input i_rstn,
    input i_abort,
    input i_start_valid,
    input [31:0] i_start_frame_token,
    input [31:0] i_start_model_id,
    input i_cell_valid,
    input [111:0] i_cell_data,
    input [13:0] i_cell_id,
    input [31:0] i_cell_frame_token,
    input i_lut_req_ready,
    input i_lut_rsp_valid,
    input i_lut_rsp_kind,
    input [9:0] i_lut_rsp_address,
    input [15:0] i_lut_rsp_tag,
    input [31:0] i_lut_rsp_frame_token,
    input [31:0] i_lut_rsp_model_id,
    input [15:0] i_lut_rsp_data,
    input i_lut_rsp_error,
    input i_sealed_ready,
    input i_read_req_valid,
    input i_read_req_class,
    input [6:0] i_read_req_index,
    input i_read_rsp_ready,
    input i_finish_valid,
    input [31:0] i_finish_frame_token,
    output o_start_ready,
    output o_cell_ready,
    output o_lut_req_valid,
    output o_lut_req_kind,
    output [9:0] o_lut_req_address,
    output [15:0] o_lut_req_tag,
    output [31:0] o_lut_req_frame_token,
    output [31:0] o_lut_req_model_id,
    output o_lut_rsp_ready,
    output o_lut_cancel,
    output o_sealed_valid,
    output [31:0] o_sealed_frame_token,
    output [7:0] o_count_person,
    output [7:0] o_count_vehicle,
    output o_read_req_ready,
    output o_read_rsp_valid,
    output o_read_rsp_class,
    output [6:0] o_read_rsp_index,
    output [159:0] o_read_rsp_data,
    output o_read_rsp_error,
    output o_finish_ready,
    output o_fault,
    output [3:0] o_error_code,
    output [2:0] o_phase,
    output [31:0] o_scan_cycles,
    output [31:0] o_sort_cycles,
    output [31:0] o_decode_cycles,
    output [31:0] o_input_wait_cycles,
    output [31:0] o_lut_wait_cycles,
    output [31:0] o_ram_wait_cycles,
    output [31:0] o_ram_read_words,
    output [31:0] o_ram_write_words
);

    //-------------配置参数区域-------------//
    localparam [31:0] MODEL_ID=32'hB35D4A66; // 完整包身份由外层清单同时绑定
    localparam [15:0] THRESHOLD=16'd32768; // 诊断分数阈值，等号保留
    localparam [15:0] SIGMOID_UPPER=16'd65514; // 正端点舍入的共享常量
    //-------------状态参数区域-------------//
    localparam ST_IDLE=0, ST_CELL=1, ST_SIG_RAW=2, ST_SIG_CHECK=3,
        ST_SIG_ABS=4, ST_SIG_ROUND=5, ST_SIG_ADDR=6, ST_SIG_REQUEST=7,
        ST_SIG_STORE=8, ST_MULT_INIT=9, ST_MULT_STEP=10, ST_SCORE=11,
        ST_CANDIDATE=12, ST_SELECT=13, ST_CLASS_NEXT=14, ST_CELL_NEXT=15,
        ST_UP_START=16, ST_UP_COMPARE=17, ST_UP_MOVE=18,
        ST_DOWN_START=19, ST_DOWN_LEFT=20, ST_DOWN_RIGHT=21,
        ST_DOWN_COMPARE=22, ST_DOWN_MOVE=23,
        ST_MEMORY_REQUEST=24, ST_MEMORY_WAIT=25,
        ST_LUT_REQUEST=26, ST_LUT_WAIT=27,
        ST_SORT_INIT=28, ST_SORT_START=29, ST_SORT_ROOT=30,
        ST_SORT_LAST=31, ST_SORT_SETUP=32, ST_SORT_NEXT=33, ST_SORT_CLASS=34,
        ST_DECODE_INIT=35, ST_DECODE_READ=36, ST_DECODE_PREP=37,
        ST_CLIP=38, ST_EXP_OFFSET=39, ST_DIV_INIT=40, ST_DIV_STEP=41,
        ST_DIV_ROUND=42, ST_EXP_REQUEST=43, ST_EXP_RESULT=44,
        ST_HALF=45, ST_CENTER=46, ST_CENTER_SHIFT=47, ST_BOUNDS=48,
        ST_AXIS_CLIP=49, ST_AXIS_NEXT=50, ST_PACK=51, ST_DECODE_NEXT=52,
        ST_DECODE_CLASS=53, ST_SEALED=54, ST_NMS=55,
        ST_NMS_RESULT=56, ST_NMS_REPLY=57, ST_NMS_RANGE=58, ST_FAULT=59;
    //--------------状态机信号--------------//
    reg [6:0] state_current=0;
    reg [6:0] state_next=0;
    reg [6:0] reg_after_memory=0;
    reg [6:0] reg_after_lut=0;
    reg [6:0] reg_after_heap=0;
    //--------------寄存器信号--------------//
    reg [1:0] reg_release=0;
    reg [31:0] reg_frame=0;
    reg [111:0] reg_cell=0;
    reg [13:0] cnt_cell=0;
    reg [6:0] reg_grid_x=0;
    reg [6:0] reg_grid_y=0;
    reg [1:0] reg_scale=0;
    reg [1:0] reg_logit=0;
    reg signed [15:0] reg_raw=0;
    reg [16:0] reg_magnitude=0;
    reg [14:0] reg_rounded=0;
    reg [10:0] reg_sigmoid_address=0;
    reg [15:0] reg_probability=0;
    reg [15:0] reg_objectness=0;
    reg [15:0] reg_person=0;
    reg [15:0] reg_vehicle=0;
    reg reg_class=0;
    reg [31:0] reg_product=0;
    reg [31:0] reg_multiplicand=0;
    reg [15:0] reg_multiplier=0;
    reg [4:0] cnt_multiply=0;
    reg [15:0] reg_score=0;
    reg [159:0] reg_candidate=0;
    reg [7:0] cnt_person=0;
    reg [7:0] cnt_vehicle=0;
    reg [31:0] reg_root_person=0;
    reg [31:0] reg_root_vehicle=0;
    reg [7:0] reg_heap_limit=0;
    reg [6:0] reg_heap_index=0;
    reg [6:0] reg_parent=0;
    reg [7:0] reg_left=0;
    reg [7:0] reg_right=0;
    reg [6:0] reg_child_index=0;
    reg [159:0] reg_child=0;
    reg [159:0] reg_sort_root=0;
    reg [6:0] reg_sort_end=0;
    reg [6:0] reg_decode_index=0;
    reg [159:0] reg_decode_raw=0;
    reg reg_axis=0;
    reg signed [15:0] reg_clipped=0;
    reg [10:0] reg_offset=0;
    reg [18:0] reg_dividend=0;
    reg [11:0] reg_remainder=0;
    reg [7:0] reg_quotient=0;
    reg [4:0] cnt_divide=0;
    reg [7:0] reg_exp_address=0;
    reg [17:0] reg_size=0;
    reg [17:0] reg_half=0;
    reg signed [21:0] reg_center_base=0;
    reg signed [21:0] reg_center=0;
    reg signed [21:0] reg_low=0;
    reg signed [21:0] reg_high=0;
    reg [17:0] reg_xlow=0;
    reg [17:0] reg_xhigh=0;
    reg [17:0] reg_ylow=0;
    reg [17:0] reg_yhigh=0;
    reg flag_memory_valid=0;
    reg reg_memory_write=0;
    reg reg_memory_class=0;
    reg [6:0] reg_memory_index=0;
    reg [159:0] reg_memory_data=0;
    reg [159:0] reg_read_record=0;
    reg flag_lut_valid=0;
    reg reg_lut_kind=0;
    reg [9:0] reg_lut_address=0;
    reg [15:0] cnt_lut_tag=0;
    reg [15:0] reg_lut_tag=0;
    reg [15:0] reg_lut_value=0;
    reg flag_fault=0;
    reg [3:0] reg_error=0;
    reg [2:0] reg_phase=0;
    reg flag_read_response=0;
    reg reg_read_class=0;
    reg [6:0] reg_read_index=0;
    reg [159:0] reg_read_data=0;
    reg reg_read_error=0;
    reg [31:0] cnt_scan=0, cnt_sort=0, cnt_decode=0;
    reg [31:0] cnt_input_wait=0, cnt_lut_wait=0, cnt_ram_wait=0;
    wire flag_cancel;
    wire flag_start;
    wire flag_cell;
    wire [7:0] selected_count;
    wire [31:0] selected_root;
    wire [6:0] grid_last_x;
    wire [6:0] grid_last_y;
    wire [11:0] divided_remainder;
    wire [21:0] axis_limit;
    wire memory_ready, memory_response_valid, memory_response_class, memory_error;
    wire [6:0] memory_response_index;
    wire [159:0] memory_response_data;
    wire [31:0] memory_read_words, memory_write_words;
    wire memory_response_ready;
    //-------------其他信号连线-------------//
    assign flag_cancel=i_abort||!reg_release[1];
    assign flag_start=i_start_valid&&o_start_ready;
    assign flag_cell=i_cell_valid&&o_cell_ready;
    assign selected_count=reg_class ? cnt_vehicle : cnt_person;
    assign selected_root=reg_class ? reg_root_vehicle : reg_root_person;
    assign grid_last_x=reg_scale==0 ? 7'd127 : reg_scale==1 ? 7'd63 : 7'd31;
    assign grid_last_y=reg_scale==0 ? 7'd71 : reg_scale==1 ? 7'd35 : 7'd17;
    assign divided_remainder={reg_remainder[10:0],reg_dividend[18]};
    assign axis_limit=reg_axis ? 22'd73728 : 22'd131072;
    assign memory_response_ready=(state_current==ST_MEMORY_WAIT)&&!flag_cancel&&!flag_fault;
    //-------------输出信号连线-------------//
    assign o_start_ready=(state_current==ST_IDLE)&&reg_release[1]&&!i_abort&&!flag_fault;
    assign o_cell_ready=(state_current==ST_CELL)&&reg_release[1]&&!i_abort&&!flag_fault;
    assign o_lut_req_valid=flag_lut_valid&&!flag_cancel&&!flag_fault;
    assign o_lut_req_kind=reg_lut_kind;
    assign o_lut_req_address=reg_lut_address;
    assign o_lut_req_tag=reg_lut_tag;
    assign o_lut_req_frame_token=reg_frame;
    assign o_lut_req_model_id=MODEL_ID;
    assign o_lut_rsp_ready=(state_current==ST_LUT_WAIT)&&!flag_cancel&&!flag_fault;
    assign o_lut_cancel=flag_cancel;
    assign o_sealed_valid=(state_current==ST_SEALED)&&!flag_fault&&!flag_cancel;
    assign o_sealed_frame_token=reg_frame;
    assign o_count_person=cnt_person;
    assign o_count_vehicle=cnt_vehicle;
    assign o_read_req_ready=(state_current==ST_NMS)&&!flag_fault&&!flag_cancel&&!i_finish_valid;
    assign o_read_rsp_valid=flag_read_response&&!flag_cancel;
    assign o_read_rsp_class=reg_read_class;
    assign o_read_rsp_index=reg_read_index;
    assign o_read_rsp_data=reg_read_data;
    assign o_read_rsp_error=reg_read_error;
    assign o_finish_ready=(state_current==ST_NMS)&&!flag_fault&&!flag_cancel;
    assign o_fault=flag_fault;
    assign o_error_code=reg_error;
    assign o_phase=reg_phase;
    assign o_scan_cycles=cnt_scan;
    assign o_sort_cycles=cnt_sort;
    assign o_decode_cycles=cnt_decode;
    assign o_input_wait_cycles=cnt_input_wait;
    assign o_lut_wait_cycles=cnt_lut_wait;
    assign o_ram_wait_cycles=cnt_ram_wait;
    assign o_ram_read_words=memory_read_words;
    assign o_ram_write_words=memory_write_words;
    //--------------状态机区域--------------//
    // 异步断言后至少两拍同步释放，第三个有效边沿才接受新任务。
    always@(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin reg_release<=0; end
        else begin reg_release<={reg_release[0],1'b1}; end
    end
    // 状态寄存器与任务处理独立。
    always@(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin state_current<=ST_IDLE; end
        else if(i_abort)begin state_current<=ST_IDLE; end
        else begin state_current<=state_next; end
    end
    // 固定图后处理的三段式状态转移。
    always@(*)begin
        state_next=state_current;
        if(flag_fault)begin state_next=ST_FAULT; end
        else begin
            case(state_current)
                ST_IDLE:begin if(flag_start)begin state_next=ST_CELL; end end
                ST_CELL:begin if(flag_cell)begin state_next=ST_SIG_RAW; end end
                ST_SIG_RAW:begin state_next=ST_SIG_CHECK; end
                ST_SIG_CHECK:begin
                    if(reg_raw<=-16'sd2048||reg_raw>=16'sd2048)begin state_next=ST_SIG_STORE; end
                    else begin state_next=ST_SIG_ABS; end
                end
                ST_SIG_ABS:begin state_next=ST_SIG_ROUND; end
                ST_SIG_ROUND:begin state_next=ST_SIG_ADDR; end
                ST_SIG_ADDR:begin state_next=ST_SIG_REQUEST; end
                ST_SIG_REQUEST:begin
                    if(reg_sigmoid_address==11'd1024)begin state_next=ST_SIG_STORE; end
                    else begin state_next=ST_LUT_REQUEST; end
                end
                ST_SIG_STORE:begin
                    if(reg_logit==2'd2)begin state_next=ST_MULT_INIT; end
                    else begin state_next=ST_SIG_RAW; end
                end
                ST_MULT_INIT:begin state_next=ST_MULT_STEP; end
                ST_MULT_STEP:begin if(cnt_multiply==5'd1)begin state_next=ST_SCORE; end end
                ST_SCORE:begin state_next=ST_CANDIDATE; end
                ST_CANDIDATE:begin
                    if(reg_score<THRESHOLD)begin state_next=ST_CLASS_NEXT; end
                    else begin state_next=ST_SELECT; end
                end
                ST_SELECT:begin
                    if(selected_count<8'd128)begin state_next=ST_UP_START; end
                    else if(reg_candidate[159:128]>selected_root)begin state_next=ST_DOWN_START; end
                    else begin state_next=ST_CLASS_NEXT; end
                end
                ST_CLASS_NEXT:begin
                    if(reg_class)begin state_next=ST_CELL_NEXT; end
                    else begin state_next=ST_MULT_INIT; end
                end
                ST_CELL_NEXT:begin
                    if(cnt_cell==14'd12095)begin state_next=ST_SORT_INIT; end
                    else begin state_next=ST_CELL; end
                end
                ST_UP_START:begin state_next=ST_MEMORY_REQUEST; end
                ST_UP_COMPARE:begin state_next=ST_MEMORY_REQUEST; end
                ST_UP_MOVE:begin state_next=ST_UP_START; end
                ST_DOWN_START:begin
                    if(({1'b0,reg_heap_index,1'b0}+9'd1)>={1'b0,reg_heap_limit})begin state_next=ST_MEMORY_REQUEST; end
                    else begin state_next=ST_MEMORY_REQUEST; end
                end
                ST_DOWN_LEFT:begin
                    if(reg_right<reg_heap_limit)begin state_next=ST_MEMORY_REQUEST; end
                    else begin state_next=ST_DOWN_COMPARE; end
                end
                ST_DOWN_RIGHT:begin state_next=ST_DOWN_COMPARE; end
                ST_DOWN_COMPARE:begin state_next=ST_MEMORY_REQUEST; end
                ST_DOWN_MOVE:begin state_next=ST_DOWN_START; end
                ST_MEMORY_REQUEST:begin if(flag_memory_valid&&memory_ready)begin state_next=ST_MEMORY_WAIT; end end
                ST_MEMORY_WAIT:begin if(memory_response_valid&&memory_response_ready)begin state_next=reg_after_memory; end end
                ST_LUT_REQUEST:begin if(o_lut_req_valid&&i_lut_req_ready)begin state_next=ST_LUT_WAIT; end end
                ST_LUT_WAIT:begin if(i_lut_rsp_valid&&o_lut_rsp_ready)begin state_next=reg_after_lut; end end
                ST_SORT_INIT:begin state_next=ST_SORT_START; end
                ST_SORT_START:begin
                    if(reg_heap_limit<=8'd1)begin state_next=ST_SORT_CLASS; end
                    else begin state_next=ST_MEMORY_REQUEST; end
                end
                ST_SORT_ROOT:begin state_next=ST_MEMORY_REQUEST; end
                ST_SORT_LAST:begin state_next=ST_MEMORY_REQUEST; end
                ST_SORT_SETUP:begin state_next=ST_DOWN_START; end
                ST_SORT_NEXT:begin state_next=ST_SORT_START; end
                ST_SORT_CLASS:begin
                    if(reg_class)begin state_next=ST_DECODE_INIT; end
                    else begin state_next=ST_SORT_INIT; end
                end
                ST_DECODE_INIT:begin state_next=ST_DECODE_READ; end
                ST_DECODE_READ:begin
                    if({1'b0,reg_decode_index}>=selected_count)begin state_next=ST_DECODE_CLASS; end
                    else begin state_next=ST_MEMORY_REQUEST; end
                end
                ST_DECODE_PREP:begin state_next=ST_CLIP; end
                ST_CLIP:begin state_next=ST_EXP_OFFSET; end
                ST_EXP_OFFSET:begin state_next=ST_DIV_INIT; end
                ST_DIV_INIT:begin state_next=ST_DIV_STEP; end
                ST_DIV_STEP:begin if(cnt_divide==5'd1)begin state_next=ST_DIV_ROUND; end end
                ST_DIV_ROUND:begin state_next=ST_EXP_REQUEST; end
                ST_EXP_REQUEST:begin state_next=ST_LUT_REQUEST; end
                ST_EXP_RESULT:begin state_next=ST_HALF; end
                ST_HALF:begin state_next=ST_CENTER; end
                ST_CENTER:begin state_next=ST_CENTER_SHIFT; end
                ST_CENTER_SHIFT:begin state_next=ST_BOUNDS; end
                ST_BOUNDS:begin state_next=ST_AXIS_CLIP; end
                ST_AXIS_CLIP:begin state_next=ST_AXIS_NEXT; end
                ST_AXIS_NEXT:begin
                    if(reg_axis)begin state_next=ST_PACK; end
                    else begin state_next=ST_CLIP; end
                end
                ST_PACK:begin state_next=ST_MEMORY_REQUEST; end
                ST_DECODE_NEXT:begin
                    if({1'b0,reg_decode_index}+8'd1>=selected_count)begin state_next=ST_DECODE_CLASS; end
                    else begin state_next=ST_DECODE_READ; end
                end
                ST_DECODE_CLASS:begin
                    if(reg_class)begin state_next=ST_SEALED; end
                    else begin state_next=ST_DECODE_INIT; end
                end
                ST_SEALED:begin if(o_sealed_valid&&i_sealed_ready)begin state_next=ST_NMS; end end
                ST_NMS:begin
                    if(i_finish_valid&&o_finish_ready)begin state_next=ST_IDLE; end
                    else if(i_read_req_valid&&o_read_req_ready)begin
                        if({1'b0,i_read_req_index}>=(i_read_req_class?cnt_vehicle:cnt_person))begin state_next=ST_NMS_RANGE; end
                        else begin state_next=ST_MEMORY_REQUEST; end
                    end
                end
                ST_NMS_RESULT:begin state_next=ST_NMS_REPLY; end
                ST_NMS_REPLY:begin if(o_read_rsp_valid&&i_read_rsp_ready)begin state_next=ST_NMS; end end
                ST_NMS_RANGE:begin state_next=ST_FAULT; end
                ST_FAULT:begin state_next=ST_FAULT; end
                default:begin state_next=ST_FAULT; end
            endcase
        end
    end
    //-----------状态任务处理区域-----------//
    // 所有算术任务串行，跨状态数据保持；复位取消的旧事务不发布封存。
    always@(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            reg_frame<=0; reg_cell<=0; cnt_cell<=0; reg_grid_x<=0; reg_grid_y<=0; reg_scale<=0;
            reg_logit<=0; reg_raw<=0; reg_magnitude<=0; reg_rounded<=0; reg_sigmoid_address<=0;
            reg_probability<=0; reg_objectness<=0; reg_person<=0; reg_vehicle<=0; reg_class<=0;
            reg_product<=0; reg_multiplicand<=0; reg_multiplier<=0; cnt_multiply<=0; reg_score<=0;
            reg_candidate<=0; cnt_person<=0; cnt_vehicle<=0; reg_root_person<=0; reg_root_vehicle<=0;
            reg_heap_limit<=0; reg_heap_index<=0; reg_parent<=0; reg_left<=0; reg_right<=0;
            reg_child_index<=0; reg_child<=0; reg_sort_root<=0; reg_sort_end<=0; reg_decode_index<=0;
            reg_decode_raw<=0; reg_axis<=0; reg_clipped<=0; reg_offset<=0; reg_dividend<=0;
            reg_remainder<=0; reg_quotient<=0; cnt_divide<=0; reg_exp_address<=0; reg_size<=0;
            reg_half<=0; reg_center_base<=0; reg_center<=0; reg_low<=0; reg_high<=0;
            reg_xlow<=0; reg_xhigh<=0; reg_ylow<=0; reg_yhigh<=0;
            flag_memory_valid<=0; reg_memory_write<=0; reg_memory_class<=0; reg_memory_index<=0;
            reg_memory_data<=0; reg_read_record<=0; reg_after_memory<=0; reg_after_lut<=0; reg_after_heap<=0;
            flag_lut_valid<=0; reg_lut_kind<=0; reg_lut_address<=0; cnt_lut_tag<=0; reg_lut_tag<=0; reg_lut_value<=0;
            flag_fault<=0; reg_error<=0; reg_phase<=0; flag_read_response<=0;
            reg_read_class<=0; reg_read_index<=0; reg_read_data<=0; reg_read_error<=0;
        end else if(i_abort)begin
            flag_memory_valid<=0; flag_lut_valid<=0; flag_read_response<=0;
            flag_fault<=0; reg_error<=0; reg_phase<=0; cnt_person<=0; cnt_vehicle<=0;
        end else begin
            if(flag_read_response&&i_read_rsp_ready)begin flag_read_response<=0; end
            if(flag_fault)begin reg_phase<=3'd5; flag_memory_valid<=0; flag_lut_valid<=0; end
            else begin
                case(state_current)
                    ST_IDLE:begin
                        if(flag_start)begin
                            reg_frame<=i_start_frame_token; cnt_person<=0; cnt_vehicle<=0;
                            cnt_cell<=0; reg_grid_x<=0; reg_grid_y<=0; reg_scale<=0; reg_logit<=0; reg_class<=0;
                            reg_phase<=3'd1; reg_root_person<=0; reg_root_vehicle<=0;
                            if(i_start_model_id!=MODEL_ID)begin flag_fault<=1; reg_error<=4'd1; end
                        end
                    end
                    ST_CELL:begin
                        if(flag_cell)begin
                            if(i_cell_id!=cnt_cell||i_cell_frame_token!=reg_frame)begin flag_fault<=1; reg_error<=4'd2; end
                            else begin reg_cell<=i_cell_data; reg_logit<=0; reg_class<=0; end
                        end
                    end
                    ST_SIG_RAW:begin
                        case(reg_logit)
                            0:begin reg_raw<=reg_cell[79:64]; end
                            1:begin reg_raw<=reg_cell[95:80]; end
                            default:begin reg_raw<=reg_cell[111:96]; end
                        endcase
                    end
                    ST_SIG_CHECK:begin
                        if(reg_raw<=-16'sd2048)begin reg_probability<=0; end
                        else if(reg_raw>=16'sd2048)begin reg_probability<=16'hffff; end
                    end
                    ST_SIG_ABS:begin
                        if(reg_raw[15])begin reg_magnitude<=~{1'b1,reg_raw}+17'd1; end
                        else begin reg_magnitude<={1'b0,reg_raw}; end
                    end
                    ST_SIG_ROUND:begin
                        reg_rounded<=reg_magnitude[16:2]+
                            ((reg_magnitude[1:0]==2'd3)||((reg_magnitude[1:0]==2'd2)&&reg_magnitude[2]));
                    end
                    ST_SIG_ADDR:begin
                        if(reg_raw[15])begin reg_sigmoid_address<=11'd512-reg_rounded[10:0]; end
                        else begin reg_sigmoid_address<=11'd512+reg_rounded[10:0]; end
                    end
                    ST_SIG_REQUEST:begin
                        if(reg_sigmoid_address==11'd1024)begin reg_probability<=SIGMOID_UPPER; end
                        else begin
                            flag_lut_valid<=1; reg_lut_kind<=0; reg_lut_address<=reg_sigmoid_address[9:0];
                            reg_lut_tag<=cnt_lut_tag; cnt_lut_tag<=cnt_lut_tag+1'b1; reg_after_lut<=ST_SIG_STORE;
                        end
                    end
                    ST_SIG_STORE:begin
                        case(reg_logit)
                            0:begin reg_objectness<=reg_probability; end
                            1:begin reg_person<=reg_probability; end
                            default:begin reg_vehicle<=reg_probability; end
                        endcase
                        if(reg_logit!=2)begin reg_logit<=reg_logit+1'b1; end
                    end
                    ST_MULT_INIT:begin
                        reg_product<=0; reg_multiplicand<={16'd0,reg_objectness};
                        reg_multiplier<=reg_class?reg_vehicle:reg_person; cnt_multiply<=5'd16;
                    end
                    ST_MULT_STEP:begin
                        if(reg_multiplier[0])begin reg_product<=reg_product+reg_multiplicand; end
                        reg_multiplicand<=reg_multiplicand<<1; reg_multiplier<=reg_multiplier>>1;
                        cnt_multiply<=cnt_multiply-1'b1;
                    end
                    ST_SCORE:begin
                        reg_score<=reg_product[31:16]+((reg_product[15:0]>16'h8000)||
                            ((reg_product[15:0]==16'h8000)&&reg_product[16]));
                    end
                    ST_CANDIDATE:begin
                        reg_candidate<={{reg_score,~cnt_cell,2'b00},17'd0,reg_grid_y,reg_grid_x,
                            reg_scale,reg_class,reg_score,cnt_cell,reg_cell[63:0]};
                    end
                    ST_SELECT:begin
                        reg_after_heap<=ST_CLASS_NEXT; reg_memory_class<=reg_class;
                        if(selected_count<8'd128)begin
                            reg_heap_index<=selected_count[6:0]; reg_heap_limit<=selected_count+1'b1;
                            if(reg_class)begin cnt_vehicle<=cnt_vehicle+1'b1; end
                            else begin cnt_person<=cnt_person+1'b1; end
                        end else if(reg_candidate[159:128]>selected_root)begin
                            reg_heap_index<=0; reg_heap_limit<=8'd128;
                        end
                    end
                    ST_UP_START:begin
                        flag_memory_valid<=1; reg_memory_class<=reg_class;
                        if(reg_heap_index==0)begin
                            reg_memory_write<=1; reg_memory_index<=0; reg_memory_data<=reg_candidate;
                            reg_after_memory<=reg_after_heap;
                        end else begin
                            reg_parent<=(reg_heap_index-1'b1)>>1;
                            reg_memory_index<=(reg_heap_index-1'b1)>>1; reg_memory_write<=0;
                            reg_after_memory<=ST_UP_COMPARE;
                        end
                    end
                    ST_UP_COMPARE:begin
                        flag_memory_valid<=1; reg_memory_write<=1; reg_memory_class<=reg_class;
                        reg_memory_index<=reg_heap_index;
                        if(reg_candidate[159:128]<reg_read_record[159:128])begin
                            reg_memory_data<=reg_read_record; reg_after_memory<=ST_UP_MOVE;
                        end else begin reg_memory_data<=reg_candidate; reg_after_memory<=reg_after_heap; end
                    end
                    ST_UP_MOVE:begin reg_heap_index<=reg_parent; end
                    ST_DOWN_START:begin
                        flag_memory_valid<=1; reg_memory_class<=reg_class;
                        reg_left<={reg_heap_index,1'b0}+8'd1; reg_right<={reg_heap_index,1'b0}+8'd2;
                        if(({1'b0,reg_heap_index,1'b0}+9'd1)>={1'b0,reg_heap_limit})begin
                            reg_memory_write<=1; reg_memory_index<=reg_heap_index;
                            reg_memory_data<=reg_candidate; reg_after_memory<=reg_after_heap;
                        end else begin
                            reg_memory_write<=0; reg_memory_index<={reg_heap_index[5:0],1'b0}+7'd1;
                            reg_after_memory<=ST_DOWN_LEFT;
                        end
                    end
                    ST_DOWN_LEFT:begin
                        reg_child<=reg_read_record; reg_child_index<=reg_left[6:0];
                        if(reg_right<reg_heap_limit)begin
                            flag_memory_valid<=1; reg_memory_write<=0; reg_memory_class<=reg_class;
                            reg_memory_index<=reg_right[6:0]; reg_after_memory<=ST_DOWN_RIGHT;
                        end
                    end
                    ST_DOWN_RIGHT:begin
                        if(reg_read_record[159:128]<reg_child[159:128])begin
                            reg_child<=reg_read_record; reg_child_index<=reg_right[6:0];
                        end
                    end
                    ST_DOWN_COMPARE:begin
                        flag_memory_valid<=1; reg_memory_write<=1; reg_memory_class<=reg_class;
                        reg_memory_index<=reg_heap_index;
                        if(reg_child[159:128]<reg_candidate[159:128])begin
                            reg_memory_data<=reg_child; reg_after_memory<=ST_DOWN_MOVE;
                        end else begin reg_memory_data<=reg_candidate; reg_after_memory<=reg_after_heap; end
                    end
                    ST_DOWN_MOVE:begin reg_heap_index<=reg_child_index; end
                    ST_MEMORY_REQUEST:begin if(flag_memory_valid&&memory_ready)begin flag_memory_valid<=0; end end
                    ST_MEMORY_WAIT:begin
                        if(memory_response_valid&&memory_response_ready)begin
                            if(memory_error||memory_response_class!=reg_memory_class||memory_response_index!=reg_memory_index)begin
                                flag_fault<=1; reg_error<=4'd4;
                                if(reg_phase==4)begin flag_read_response<=1; reg_read_error<=1; reg_read_data<=0; end
                            end else begin
                                reg_read_record<=memory_response_data;
                                if(reg_memory_write&&reg_memory_index==0)begin
                                    if(reg_memory_class)begin reg_root_vehicle<=reg_memory_data[159:128]; end
                                    else begin reg_root_person<=reg_memory_data[159:128]; end
                                end
                            end
                        end
                    end
                    ST_LUT_REQUEST:begin if(o_lut_req_valid&&i_lut_req_ready)begin flag_lut_valid<=0; end end
                    ST_LUT_WAIT:begin
                        if(i_lut_rsp_valid&&o_lut_rsp_ready)begin
                            if(i_lut_rsp_error||i_lut_rsp_kind!=reg_lut_kind||i_lut_rsp_address!=reg_lut_address||
                                i_lut_rsp_tag!=reg_lut_tag||i_lut_rsp_frame_token!=reg_frame||i_lut_rsp_model_id!=MODEL_ID)begin
                                flag_fault<=1; reg_error<=4'd3;
                            end else begin reg_probability<=i_lut_rsp_data; reg_lut_value<=i_lut_rsp_data; end
                        end
                    end
                    ST_CLASS_NEXT:begin if(!reg_class)begin reg_class<=1; end end
                    ST_CELL_NEXT:begin
                        reg_class<=0; reg_logit<=0;
                        if(cnt_cell==14'd12095)begin reg_class<=0; end
                        else begin
                            cnt_cell<=cnt_cell+1'b1;
                            if(reg_grid_x==grid_last_x)begin
                                reg_grid_x<=0;
                                if(reg_grid_y==grid_last_y)begin reg_grid_y<=0; reg_scale<=reg_scale+1'b1; end
                                else begin reg_grid_y<=reg_grid_y+1'b1; end
                            end else begin reg_grid_x<=reg_grid_x+1'b1; end
                        end
                    end
                    ST_SORT_INIT:begin reg_phase<=2; reg_heap_limit<=selected_count; end
                    ST_SORT_START:begin
                        if(reg_heap_limit>1)begin
                            reg_sort_end<=reg_heap_limit-1'b1; flag_memory_valid<=1;
                            reg_memory_write<=0; reg_memory_class<=reg_class; reg_memory_index<=0; reg_after_memory<=ST_SORT_ROOT;
                        end
                    end
                    ST_SORT_ROOT:begin
                        reg_sort_root<=reg_read_record; flag_memory_valid<=1; reg_memory_write<=0;
                        reg_memory_class<=reg_class; reg_memory_index<=reg_sort_end; reg_after_memory<=ST_SORT_LAST;
                    end
                    ST_SORT_LAST:begin
                        reg_candidate<=reg_read_record; flag_memory_valid<=1; reg_memory_write<=1;
                        reg_memory_class<=reg_class; reg_memory_index<=reg_sort_end;
                        reg_memory_data<=reg_sort_root; reg_after_memory<=ST_SORT_SETUP;
                    end
                    ST_SORT_SETUP:begin
                        reg_heap_limit<=reg_heap_limit-1'b1; reg_heap_index<=0; reg_after_heap<=ST_SORT_NEXT;
                    end
                    ST_SORT_CLASS:begin reg_class<=!reg_class; end
                    ST_DECODE_INIT:begin reg_phase<=3; reg_decode_index<=0; end
                    ST_DECODE_READ:begin
                        if({1'b0,reg_decode_index}<selected_count)begin
                            flag_memory_valid<=1; reg_memory_write<=0; reg_memory_class<=reg_class;
                            reg_memory_index<=reg_decode_index; reg_after_memory<=ST_DECODE_PREP;
                        end
                    end
                    ST_DECODE_PREP:begin
                        reg_decode_raw<=reg_read_record; reg_axis<=0;
                        if(reg_read_record[94]!=reg_class||reg_read_record[96:95]>2)begin flag_fault<=1; reg_error<=7; end
                    end
                    ST_CLIP:begin
                        if(!reg_axis)begin
                            if($signed(reg_decode_raw[47:32]) < -16'sd1024)begin reg_clipped<=-16'sd1024; end
                            else if($signed(reg_decode_raw[47:32])>16'sd896)begin reg_clipped<=16'sd896; end
                            else begin reg_clipped<=reg_decode_raw[47:32]; end
                        end else begin
                            if($signed(reg_decode_raw[63:48]) < -16'sd1024)begin reg_clipped<=-16'sd1024; end
                            else if($signed(reg_decode_raw[63:48])>16'sd896)begin reg_clipped<=16'sd896; end
                            else begin reg_clipped<=reg_decode_raw[63:48]; end
                        end
                    end
                    ST_EXP_OFFSET:begin reg_offset<=$signed(reg_clipped)+17'sd1024; end
                    ST_DIV_INIT:begin
                        reg_dividend<=({8'd0,reg_offset}<<8)-reg_offset;
                        reg_remainder<=0; reg_quotient<=0; cnt_divide<=5'd19;
                    end
                    ST_DIV_STEP:begin
                        if(divided_remainder>=12'd1920)begin
                            reg_remainder<=divided_remainder-12'd1920;
                            reg_quotient<={reg_quotient[6:0],1'b1};
                        end else begin reg_remainder<=divided_remainder; reg_quotient<={reg_quotient[6:0],1'b0}; end
                        reg_dividend<=reg_dividend<<1; cnt_divide<=cnt_divide-1'b1;
                    end
                    ST_DIV_ROUND:begin
                        reg_exp_address<=reg_quotient+((reg_remainder>12'd960)||
                            ((reg_remainder==12'd960)&&reg_quotient[0]));
                    end
                    ST_EXP_REQUEST:begin
                        flag_lut_valid<=1; reg_lut_kind<=1; reg_lut_address<={2'b00,reg_exp_address};
                        reg_lut_tag<=cnt_lut_tag; cnt_lut_tag<=cnt_lut_tag+1'b1; reg_after_lut<=ST_EXP_RESULT;
                    end
                    ST_EXP_RESULT:begin reg_size<={2'b00,reg_lut_value}<<reg_decode_raw[96:95]; end
                    ST_HALF:begin reg_half<=(reg_size>>1)+(reg_size[0]&&reg_size[1]); end
                    ST_CENTER:begin
                        if(!reg_axis)begin reg_center_base<=$signed({{6{reg_decode_raw[15]}},reg_decode_raw[15:0]})+
                            $signed({7'd0,reg_decode_raw[103:97],8'd0}); end
                        else begin reg_center_base<=$signed({{6{reg_decode_raw[31]}},reg_decode_raw[31:16]})+
                            $signed({7'd0,reg_decode_raw[110:104],8'd0}); end
                    end
                    ST_CENTER_SHIFT:begin reg_center<=reg_center_base<<<(reg_decode_raw[96:95]+3'd2); end
                    ST_BOUNDS:begin reg_low<=reg_center-$signed({4'd0,reg_half}); reg_high<=reg_center+$signed({4'd0,reg_half}); end
                    ST_AXIS_CLIP:begin
                        if(!reg_axis)begin
                            if(reg_low<0)begin reg_xlow<=0; end
                            else if(reg_low>$signed(axis_limit))begin reg_xlow<=axis_limit[17:0]; end
                            else begin reg_xlow<=reg_low[17:0]; end
                            if(reg_high<0)begin reg_xhigh<=0; end
                            else if(reg_high>$signed(axis_limit))begin reg_xhigh<=axis_limit[17:0]; end
                            else begin reg_xhigh<=reg_high[17:0]; end
                        end else begin
                            if(reg_low<0)begin reg_ylow<=0; end
                            else if(reg_low>$signed(axis_limit))begin reg_ylow<=axis_limit[17:0]; end
                            else begin reg_ylow<=reg_low[17:0]; end
                            if(reg_high<0)begin reg_yhigh<=0; end
                            else if(reg_high>$signed(axis_limit))begin reg_yhigh<=axis_limit[17:0]; end
                            else begin reg_yhigh<=reg_high[17:0]; end
                        end
                    end
                    ST_AXIS_NEXT:begin if(!reg_axis)begin reg_axis<=1; end end
                    ST_PACK:begin
                        flag_memory_valid<=1; reg_memory_write<=1; reg_memory_class<=reg_class;
                        reg_memory_index<=reg_decode_index;
                        reg_memory_data<={56'd0,((reg_xlow<reg_xhigh)&&(reg_ylow<reg_yhigh)),reg_class,
                            reg_decode_raw[93:78],reg_decode_raw[77:64],reg_yhigh,reg_xhigh,reg_ylow,reg_xlow};
                        reg_after_memory<=ST_DECODE_NEXT;
                    end
                    ST_DECODE_NEXT:begin reg_decode_index<=reg_decode_index+1'b1; end
                    ST_DECODE_CLASS:begin reg_class<=!reg_class; end
                    ST_SEALED:begin if(o_sealed_valid&&i_sealed_ready)begin reg_phase<=4; end end
                    ST_NMS:begin
                        if(i_finish_valid&&o_finish_ready)begin
                            if(i_finish_frame_token!=reg_frame)begin flag_fault<=1; reg_error<=6; end
                            else begin reg_phase<=0; end
                        end else if(i_read_req_valid&&o_read_req_ready)begin
                            reg_read_class<=i_read_req_class; reg_read_index<=i_read_req_index;
                            reg_read_error<=0;
                            if({1'b0,i_read_req_index}<(i_read_req_class?cnt_vehicle:cnt_person))begin
                                flag_memory_valid<=1; reg_memory_write<=0; reg_memory_class<=i_read_req_class;
                                reg_memory_index<=i_read_req_index; reg_after_memory<=ST_NMS_RESULT;
                            end
                        end
                    end
                    ST_NMS_RESULT:begin
                        reg_read_data<=reg_read_record; flag_read_response<=1; reg_read_error<=0;
                    end
                    ST_NMS_RANGE:begin
                        flag_fault<=1; reg_error<=5; flag_read_response<=1; reg_read_error<=1; reg_read_data<=0;
                    end
                    default:begin end
                endcase
            end
        end
    end
    // 每拍只属于SCAN、SORT、DECODE之一；等待是其中子集，不再相加。
    always@(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin cnt_scan<=0; cnt_sort<=0; cnt_decode<=0; cnt_input_wait<=0; cnt_lut_wait<=0; cnt_ram_wait<=0; end
        else if(flag_start)begin cnt_scan<=0; cnt_sort<=0; cnt_decode<=0; cnt_input_wait<=0; cnt_lut_wait<=0; cnt_ram_wait<=0; end
        else if(!flag_fault&&!flag_cancel&&state_current!=ST_SEALED)begin
            case(reg_phase)
                1:begin cnt_scan<=cnt_scan+1'b1; end
                2:begin cnt_sort<=cnt_sort+1'b1; end
                3:begin cnt_decode<=cnt_decode+1'b1; end
                default:begin end
            endcase
            if(state_current==ST_CELL&&!i_cell_valid)begin cnt_input_wait<=cnt_input_wait+1'b1; end
            if((state_current==ST_LUT_REQUEST&&!i_lut_req_ready)||(state_current==ST_LUT_WAIT&&!i_lut_rsp_valid))begin
                cnt_lut_wait<=cnt_lut_wait+1'b1;
            end
            if((state_current==ST_MEMORY_REQUEST&&!memory_ready)||(state_current==ST_MEMORY_WAIT&&!memory_response_valid))begin
                cnt_ram_wait<=cnt_ram_wait+1'b1;
            end
        end
    end
    //------------模块实例化区域------------//
    // 唯一40960bit候选仓：扫描、排序、解码和NMS分时共用。
    road_candidate_ram road_candidate_ram_Inst_store(
        .i_clk(i_clk), .i_rstn(i_rstn), .i_cancel(flag_cancel), .i_clear_counters(flag_start),
        .i_req_valid(flag_memory_valid&&!flag_fault), .i_req_write(reg_memory_write),
        .i_req_class(reg_memory_class), .i_req_index(reg_memory_index), .i_req_data(reg_memory_data),
        .i_rsp_ready(memory_response_ready), .o_req_ready(memory_ready),
        .o_rsp_valid(memory_response_valid), .o_rsp_class(memory_response_class),
        .o_rsp_index(memory_response_index), .o_rsp_data(memory_response_data), .o_rsp_error(memory_error),
        .o_read_words(memory_read_words), .o_write_words(memory_write_words)
    );
endmodule

