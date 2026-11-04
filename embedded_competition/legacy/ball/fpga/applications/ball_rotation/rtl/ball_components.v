`timescale 1ns / 1ps
// 四像素采集保持满速；4x4单元按同色四邻接分离，统计分支不延迟视频。
module ball_components #(
    parameter C_WIDTH=1280,C_HEIGHT=720,
    parameter C_X_MIN=64,C_Y_MIN=160,C_X_END=1216,C_Y_END=640,
    parameter C_GATE_MIN=544,C_GATE_END=736,
    parameter C_MIN_AREA=128,C_MIN_SIZE=12,C_MAX_SIZE=384,
    parameter C_MAX_CANDIDATES=8,C_QUEUE_BITS=12
)(
    input i_clk,
    input i_rstn,
    input i_session_clear, // 同步撤销旧帧扫描/采集，RAM由下一个完整SOF覆盖。
    input i_valid,
    input i_sof,
    input i_eof,
    input [11:0] i_x,
    input [11:0] i_y,
    input [7:0] i_labels,
    input [2:0] i_gate_hits,
    input [15:0] i_epoch,
    input [31:0] i_frame_id, // 与像素流一起冻结的源帧编号。
    input [63:0] i_stamp, // 对应源帧SOF采集时间。
    output o_frame_start,
    output o_candidate_valid,
    output [1:0] o_color,
    output [19:0] o_area,
    output [11:0] o_x_min,
    output [11:0] o_x_max,
    output [11:0] o_y_min,
    output [11:0] o_y_max,
    output o_frame_done,
    output [19:0] o_gate_pixels,
    output o_gate_occupied,
    output [15:0] o_epoch,
    output [31:0] o_frame_id,
    output [63:0] o_stamp,
    output o_overflow,
    output o_fault,
    output o_error,
    output [3:0] o_diag_count,
    output [11:0] o_diag_width,
    output [11:0] o_diag_height,
    output [19:0] o_diag_area,
    output [6:0] o_diag_fill,
    output [3:0] o_diag_reject
);
    localparam C_FIRST_COLUMN=C_X_MIN/4,C_LAST_COLUMN=(C_X_END+3)/4;
    localparam C_FIRST_ROW=C_Y_MIN/4,C_LAST_ROW=(C_Y_END+3)/4;
    localparam C_COLUMNS=C_LAST_COLUMN-C_FIRST_COLUMN,C_ROWS=C_LAST_ROW-C_FIRST_ROW;
    localparam C_CELLS=C_COLUMNS*C_ROWS;
    localparam C_COLUMN_BITS=C_COLUMNS>1 ? $clog2(C_COLUMNS) : 1;
    localparam C_ROW_BITS=C_ROWS>1 ? $clog2(C_ROWS) : 1;
    localparam C_ADDRESS_BITS=C_CELLS>1 ? $clog2(C_CELLS) : 1;
    localparam C_QUEUE_DEPTH=1 << C_QUEUE_BITS;
    localparam C_QUEUE_WORD_BITS=C_COLUMN_BITS+C_ROW_BITS+5;
    localparam C_BOTTOM_ROW=(C_LAST_ROW*4 < C_HEIGHT ? C_LAST_ROW*4 : C_HEIGHT)-1;
    localparam ST_IDLE=0,ST_SCAN_READ=1,ST_SCAN_LOAD=2,ST_SCAN_CHECK=3,
        ST_POP_TEST=4,ST_POP_READ=5,ST_POP_LOAD=6,ST_NODE=7,
        ST_NEIGHBOR_READ=8,ST_NEIGHBOR_LOAD=9,ST_NEIGHBOR_CHECK=10,ST_NEIGHBOR_ADVANCE=11,
        ST_REGION_MEASURE=12,ST_REGION_SIZE=13,ST_REGION_AREA=14,ST_REGION_FILTER=15,
        ST_REGION_EMIT=16,ST_SCAN_ADVANCE=17,ST_DIAG_INIT=18,ST_DIAG_DIVIDE=19,ST_DONE=20;
    reg [4:0] state_current,state_next;
    reg flag_capture_bank,flag_scan_bank,flag_drop_frame;
    reg flag_capture,flag_capture_first,flag_capture_last,flag_roi_end,reg_capture_bank;
    reg [C_COLUMN_BITS-1:0] reg_capture_column;
    reg [C_ADDRESS_BITS-1:0] reg_capture_address;
    reg [4:0] reg_capture_red,reg_capture_yellow,reg_capture_green;
    reg [15:0] reg_capture_epoch;
    reg [31:0] reg_capture_frame,reg_frame_o;
    reg [63:0] reg_capture_stamp,reg_stamp_o;
    reg [19:0] cnt_gate;
    reg [4:0] dec_red,dec_yellow,dec_green;
    integer lane;
    wire flag_busy=state_current != ST_IDLE;
    wire flag_conflict=flag_busy && flag_capture_bank == flag_scan_bank;
    wire flag_drop_now=i_sof ? flag_conflict : flag_drop_frame;
    wire flag_inside=i_valid && (i_x >> 2) >= C_FIRST_COLUMN && (i_x >> 2) < C_LAST_COLUMN &&
        (i_y >> 2) >= C_FIRST_ROW && (i_y >> 2) < C_LAST_ROW;
    wire flag_capture_now=flag_inside && !flag_drop_now && !i_session_clear;
    wire [C_COLUMN_BITS-1:0] wire_capture_column=(i_x >> 2)-C_FIRST_COLUMN;
    wire [C_ADDRESS_BITS-1:0] wire_capture_address=((i_y >> 2)-C_FIRST_ROW)*C_COLUMNS+wire_capture_column;
    wire [14:0] wire_row_counts;
    wire [4:0] wire_red=(flag_capture_first ? 5'd0 : wire_row_counts[14:10])+reg_capture_red;
    wire [4:0] wire_yellow=(flag_capture_first ? 5'd0 : wire_row_counts[9:5])+reg_capture_yellow;
    wire [4:0] wire_green=(flag_capture_first ? 5'd0 : wire_row_counts[4:0])+reg_capture_green;
    wire [6:0] wire_color_total={2'd0,wire_red}+{2'd0,wire_yellow}+{2'd0,wire_green};
    reg [1:0] dec_cell_color;
    reg [4:0] dec_cell_count;
    reg [6:0] dec_cell;

    // 原始门占用保持原语义；有效空拍不重复累计像素。
    always @(*)begin
        dec_red=0;dec_yellow=0;dec_green=0;
        for(lane=0;lane<4;lane=lane+1)begin
            case(i_labels[lane*2 +:2])
                1:dec_red=dec_red+1'b1;
                2:dec_yellow=dec_yellow+1'b1;
                3:dec_green=dec_green+1'b1;
                default:begin end
            endcase
        end
        dec_cell_color=1;dec_cell_count=wire_red;
        if(wire_yellow > dec_cell_count)begin dec_cell_color=2;dec_cell_count=wire_yellow;end
        if(wire_green > dec_cell_count)begin dec_cell_color=3;dec_cell_count=wire_green;end
        dec_cell=0;
        if(dec_cell_count >= 4 && ({2'd0,dec_cell_count} << 2) >= wire_color_total*3)begin
            dec_cell={dec_cell_color,dec_cell_count};
        end
    end
    ball_component_store #(.C_DEPTH(C_COLUMNS),.C_ADDR_BITS(C_COLUMN_BITS),.C_DATA_BITS(15)) row_Inst(
        .i_clk(i_clk),.i_read_enable(flag_capture_now),.i_read_address(wire_capture_column),
        .i_write_enable(flag_capture && !i_session_clear),.i_write_address(reg_capture_column),
        .i_write_data({wire_red,wire_yellow,wire_green}),.o_read_data(wire_row_counts));
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            flag_capture_bank<=0;flag_drop_frame<=0;flag_capture<=0;flag_capture_first<=0;
            flag_capture_last<=0;flag_roi_end<=0;reg_capture_bank<=0;reg_capture_column<=0;
            reg_capture_address<=0;reg_capture_red<=0;reg_capture_yellow<=0;reg_capture_green<=0;
            reg_capture_epoch<=0;cnt_gate<=0;reg_capture_frame<=0;reg_capture_stamp<=0;
        end else if(i_session_clear)begin
            flag_capture_bank<=0;flag_drop_frame<=1;flag_capture<=0;flag_capture_first<=0;
            flag_capture_last<=0;flag_roi_end<=0;reg_capture_bank<=0;reg_capture_column<=0;
            reg_capture_address<=0;reg_capture_red<=0;reg_capture_yellow<=0;reg_capture_green<=0;
            reg_capture_epoch<=0;cnt_gate<=0;reg_capture_frame<=0;reg_capture_stamp<=0;
        end else begin
            flag_capture<=flag_capture_now;
            flag_roi_end<=flag_capture_now && i_y == C_BOTTOM_ROW && wire_capture_column == C_COLUMNS-1;
            if(i_valid)begin
                if(i_sof)begin flag_drop_frame<=flag_conflict;reg_capture_frame<=i_frame_id;reg_capture_stamp<=i_stamp;end
                cnt_gate<=(i_sof ? 20'd0 : cnt_gate)+i_gate_hits;
                if(i_eof)begin flag_capture_bank<=!flag_capture_bank;end
            end
            if(flag_capture_now)begin
                reg_capture_bank<=flag_capture_bank;reg_capture_column<=wire_capture_column;
                reg_capture_address<=wire_capture_address;reg_capture_epoch<=i_epoch;
                flag_capture_first<=i_y[1:0] == 0;
                flag_capture_last<=i_y[1:0] == 3 || i_y == C_HEIGHT-1;
                reg_capture_red<=dec_red;reg_capture_yellow<=dec_yellow;reg_capture_green<=dec_green;
            end
        end
    end

    reg [C_ADDRESS_BITS-1:0] cnt_scan_address,reg_node_address;
    reg [C_COLUMN_BITS-1:0] cnt_scan_column,reg_node_column,reg_neighbor_column,reg_min_column,reg_max_column;
    reg [C_ROW_BITS-1:0] cnt_scan_row,reg_node_row,reg_neighbor_row,reg_min_row,reg_max_row;
    reg [6:0] reg_cell,reg_neighbor_cell;
    reg [1:0] reg_region_color,cnt_direction;
    reg [19:0] reg_region_area;
    reg [C_QUEUE_BITS-1:0] cnt_head,cnt_tail;
    reg [C_QUEUE_BITS:0] cnt_queue;
    wire [C_QUEUE_WORD_BITS-1:0] wire_queue_data;
    reg flag_neighbor_valid;
    reg [C_ADDRESS_BITS-1:0] dec_neighbor_address;
    reg [C_COLUMN_BITS-1:0] dec_neighbor_column;
    reg [C_ROW_BITS-1:0] dec_neighbor_row;
    wire flag_seed=state_current == ST_SCAN_CHECK && reg_cell[6:5] != 0;
    wire flag_neighbor_match=reg_neighbor_cell[6:5] == reg_region_color && reg_neighbor_cell[6:5] != 0;
    wire flag_queue_full=cnt_queue == C_QUEUE_DEPTH;
    wire flag_push=state_current == ST_NEIGHBOR_CHECK && flag_neighbor_match && !flag_queue_full;
    wire flag_queue_write=flag_seed || flag_push;
    wire [C_QUEUE_BITS-1:0] wire_queue_write_address=flag_seed ? {C_QUEUE_BITS{1'b0}} : cnt_tail;
    wire [C_QUEUE_WORD_BITS-1:0] wire_queue_write_data=flag_seed ?
        {reg_cell[4:0],cnt_scan_row,cnt_scan_column} : {reg_neighbor_cell[4:0],reg_neighbor_row,reg_neighbor_column};
    ball_component_store #(.C_DEPTH(C_QUEUE_DEPTH),.C_ADDR_BITS(C_QUEUE_BITS),.C_DATA_BITS(C_QUEUE_WORD_BITS)) queue_Inst(
        .i_clk(i_clk),.i_read_enable(state_current == ST_POP_READ),.i_read_address(cnt_head),
        .i_write_enable(flag_queue_write && !i_session_clear),.i_write_address(wire_queue_write_address),
        .i_write_data(wire_queue_write_data),.o_read_data(wire_queue_data));

    // 左右上下顺序固定；先清除再入队，保证每个单元最多访问一次。
    always @(*)begin
        flag_neighbor_valid=0;dec_neighbor_address=reg_node_address;
        dec_neighbor_column=reg_node_column;dec_neighbor_row=reg_node_row;
        case(cnt_direction)
            0:begin
                flag_neighbor_valid=reg_node_column != 0;dec_neighbor_address=reg_node_address-1'b1;
                dec_neighbor_column=reg_node_column-1'b1;
            end
            1:begin
                flag_neighbor_valid=reg_node_column < C_COLUMNS-1;dec_neighbor_address=reg_node_address+1'b1;
                dec_neighbor_column=reg_node_column+1'b1;
            end
            2:begin
                flag_neighbor_valid=reg_node_row != 0;dec_neighbor_address=reg_node_address-C_COLUMNS;
                dec_neighbor_row=reg_node_row-1'b1;
            end
            3:begin
                flag_neighbor_valid=reg_node_row < C_ROWS-1;dec_neighbor_address=reg_node_address+C_COLUMNS;
                dec_neighbor_row=reg_node_row+1'b1;
            end
            default:begin end
        endcase
    end
    wire flag_grid_read=state_current == ST_SCAN_READ || (state_current == ST_NEIGHBOR_READ && flag_neighbor_valid);
    wire [C_ADDRESS_BITS-1:0] wire_grid_read_address=state_current == ST_SCAN_READ ? cnt_scan_address : dec_neighbor_address;
    wire flag_grid_clear=flag_seed || flag_push;
    wire [C_ADDRESS_BITS-1:0] wire_grid_clear_address=flag_seed ? cnt_scan_address : dec_neighbor_address;
    wire [13:0] wire_grid_data;
    genvar bank;
    generate
        for(bank=0;bank<2;bank=bank+1)begin:gen_frame_bank
            wire flag_cell_write=flag_capture && flag_capture_last && reg_capture_bank == bank;
            wire flag_cell_clear=flag_grid_clear && flag_scan_bank == bank;
            ball_component_store #(.C_DEPTH(C_CELLS),.C_ADDR_BITS(C_ADDRESS_BITS),.C_DATA_BITS(7)) frame_Inst(
                .i_clk(i_clk),.i_read_enable(flag_grid_read && flag_scan_bank == bank),.i_read_address(wire_grid_read_address),
                .i_write_enable((flag_cell_write || flag_cell_clear) && !i_session_clear),
                .i_write_address(flag_cell_write ? reg_capture_address : wire_grid_clear_address),
                .i_write_data(flag_cell_write ? dec_cell : 7'd0),.o_read_data(wire_grid_data[bank*7 +:7]));
        end
    endgenerate
    wire [6:0] wire_scan_cell=flag_scan_bank ? wire_grid_data[13:7] : wire_grid_data[6:0];

    reg [11:0] reg_left,reg_right,reg_top,reg_bottom,reg_width,reg_height;
    reg [25:0] reg_box_area,reg_diag_box_area;
    reg [3:0] reg_reject,cnt_candidates;
    reg reg_start_o,reg_valid_o,reg_done_o,flag_overflow_o,flag_fault_o,flag_error_o;
    reg [1:0] reg_color_o;
    reg [19:0] reg_area_o,reg_gate_o;
    reg flag_gate_occupied_o;
    reg [11:0] reg_left_o,reg_right_o,reg_top_o,reg_bottom_o;
    reg [15:0] reg_epoch_o;
    reg [11:0] reg_diag_width_o,reg_diag_height_o;
    reg [19:0] reg_diag_area_o;
    reg [6:0] reg_diag_fill_o;
    reg [3:0] reg_diag_reject_o;
    reg [26:0] reg_fill_remaining;
    wire [12:0] wire_left=C_FIRST_COLUMN*4+reg_min_column*4;
    wire [12:0] wire_right=C_FIRST_COLUMN*4+reg_max_column*4+3;
    wire [12:0] wire_top=C_FIRST_ROW*4+reg_min_row*4;
    wire [12:0] wire_bottom=C_FIRST_ROW*4+reg_max_row*4+3;
    wire flag_candidate_overflow=reg_reject == 0 && cnt_candidates == C_MAX_CANDIDATES;
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin state_current<=ST_IDLE;end
        else if(i_session_clear)begin state_current<=ST_IDLE;end
        else begin state_current<=state_next;end
    end
    always @(*)begin
        state_next=state_current;
        case(state_current)
            ST_IDLE:if(flag_roi_end)begin state_next=ST_SCAN_READ;end
            ST_SCAN_READ:state_next=ST_SCAN_LOAD;
            ST_SCAN_LOAD:state_next=ST_SCAN_CHECK;
            ST_SCAN_CHECK:state_next=reg_cell[6:5] != 0 ? ST_POP_TEST : ST_SCAN_ADVANCE;
            ST_POP_TEST:state_next=cnt_queue == 0 ? ST_REGION_MEASURE : ST_POP_READ;
            ST_POP_READ:state_next=ST_POP_LOAD;
            ST_POP_LOAD:state_next=ST_NODE;
            ST_NODE:state_next=ST_NEIGHBOR_READ;
            ST_NEIGHBOR_READ:state_next=flag_neighbor_valid ? ST_NEIGHBOR_LOAD : ST_NEIGHBOR_ADVANCE;
            ST_NEIGHBOR_LOAD:state_next=ST_NEIGHBOR_CHECK;
            ST_NEIGHBOR_CHECK:state_next=flag_neighbor_match && flag_queue_full ? ST_DIAG_INIT : ST_NEIGHBOR_ADVANCE;
            ST_NEIGHBOR_ADVANCE:state_next=cnt_direction == 3 ? ST_POP_TEST : ST_NEIGHBOR_READ;
            ST_REGION_MEASURE:state_next=ST_REGION_SIZE;
            ST_REGION_SIZE:state_next=ST_REGION_AREA;
            ST_REGION_AREA:state_next=ST_REGION_FILTER;
            ST_REGION_FILTER:state_next=ST_REGION_EMIT;
            ST_REGION_EMIT:state_next=flag_candidate_overflow ? ST_DIAG_INIT : ST_SCAN_ADVANCE;
            ST_SCAN_ADVANCE:state_next=cnt_scan_address == C_CELLS-1 ? ST_DIAG_INIT : ST_SCAN_READ;
            ST_DIAG_INIT:state_next=reg_diag_box_area == 0 ? ST_DONE : ST_DIAG_DIVIDE;
            ST_DIAG_DIVIDE:if(reg_fill_remaining < {1'b0,reg_diag_box_area})begin state_next=ST_DONE;end
            ST_DONE:state_next=ST_IDLE;
            default:state_next=ST_IDLE;
        endcase
    end
    // 所有候选与诊断只属于一个冻结epoch；超限在done处使整帧失效。
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            flag_scan_bank<=0;cnt_scan_address<=0;cnt_scan_column<=0;cnt_scan_row<=0;
            reg_node_address<=0;reg_node_column<=0;reg_node_row<=0;reg_neighbor_column<=0;reg_neighbor_row<=0;
            reg_min_column<=0;reg_max_column<=0;reg_min_row<=0;reg_max_row<=0;
            reg_cell<=0;reg_neighbor_cell<=0;reg_region_color<=0;reg_region_area<=0;cnt_direction<=0;
            cnt_head<=0;cnt_tail<=0;cnt_queue<=0;cnt_candidates<=0;
            reg_left<=0;reg_right<=0;reg_top<=0;reg_bottom<=0;reg_width<=0;reg_height<=0;
            reg_box_area<=0;reg_diag_box_area<=0;reg_reject<=0;
            reg_start_o<=0;reg_valid_o<=0;reg_done_o<=0;flag_overflow_o<=0;flag_fault_o<=0;flag_error_o<=0;
            reg_color_o<=0;reg_area_o<=0;reg_gate_o<=0;reg_epoch_o<=0;reg_frame_o<=0;reg_stamp_o<=0;
            flag_gate_occupied_o<=0;
            reg_left_o<=0;reg_right_o<=0;reg_top_o<=0;reg_bottom_o<=0;
            reg_diag_width_o<=0;reg_diag_height_o<=0;reg_diag_area_o<=0;reg_diag_fill_o<=0;
            reg_diag_reject_o<=0;reg_fill_remaining<=0;
        end else if(i_session_clear)begin
            flag_scan_bank<=0;cnt_scan_address<=0;cnt_scan_column<=0;cnt_scan_row<=0;
            reg_node_address<=0;reg_node_column<=0;reg_node_row<=0;reg_neighbor_column<=0;reg_neighbor_row<=0;
            reg_min_column<=0;reg_max_column<=0;reg_min_row<=0;reg_max_row<=0;
            reg_cell<=0;reg_neighbor_cell<=0;reg_region_color<=0;reg_region_area<=0;cnt_direction<=0;
            cnt_head<=0;cnt_tail<=0;cnt_queue<=0;cnt_candidates<=0;
            reg_left<=0;reg_right<=0;reg_top<=0;reg_bottom<=0;reg_width<=0;reg_height<=0;
            reg_box_area<=0;reg_diag_box_area<=0;reg_reject<=0;
            reg_start_o<=0;reg_valid_o<=0;reg_done_o<=0;flag_overflow_o<=0;flag_fault_o<=0;flag_error_o<=0;
            reg_color_o<=0;reg_area_o<=0;reg_gate_o<=0;reg_epoch_o<=0;reg_frame_o<=0;reg_stamp_o<=0;
            flag_gate_occupied_o<=0;
            reg_left_o<=0;reg_right_o<=0;reg_top_o<=0;reg_bottom_o<=0;
            reg_diag_width_o<=0;reg_diag_height_o<=0;reg_diag_area_o<=0;reg_diag_fill_o<=0;
            reg_diag_reject_o<=0;reg_fill_remaining<=0;
        end else begin
            reg_start_o<=0;reg_valid_o<=0;reg_done_o<=0;flag_fault_o<=0;
            if((i_valid && i_sof && flag_conflict) || (flag_roi_end && flag_busy))begin
                flag_fault_o<=1;flag_error_o<=1;
            end
            case(state_current)
                ST_IDLE:if(flag_roi_end)begin
                    flag_scan_bank<=reg_capture_bank;reg_epoch_o<=reg_capture_epoch;reg_gate_o<=cnt_gate;
                    reg_frame_o<=reg_capture_frame;reg_stamp_o<=reg_capture_stamp;
                    cnt_scan_address<=0;cnt_scan_column<=0;cnt_scan_row<=0;cnt_candidates<=0;
                    cnt_head<=0;cnt_tail<=0;cnt_queue<=0;flag_overflow_o<=0;reg_start_o<=1;
                    reg_diag_width_o<=0;reg_diag_height_o<=0;reg_diag_area_o<=0;reg_diag_fill_o<=0;
                    reg_diag_reject_o<=0;reg_diag_box_area<=0;
                    flag_gate_occupied_o<=0;
                end
                ST_SCAN_LOAD:reg_cell<=wire_scan_cell;
                ST_SCAN_CHECK:if(reg_cell[6:5] != 0)begin
                    reg_region_color<=reg_cell[6:5];reg_region_area<=0;
                    reg_min_column<=cnt_scan_column;reg_max_column<=cnt_scan_column;
                    reg_min_row<=cnt_scan_row;reg_max_row<=cnt_scan_row;
                    cnt_head<=0;cnt_tail<=1;cnt_queue<=1;
                end
                ST_POP_LOAD:begin
                    reg_node_column<=wire_queue_data[C_COLUMN_BITS-1:0];
                    reg_node_row<=wire_queue_data[C_COLUMN_BITS +:C_ROW_BITS];
                    reg_region_area<=reg_region_area+wire_queue_data[C_COLUMN_BITS+C_ROW_BITS +:5];
                    cnt_head<=cnt_head+1'b1;cnt_queue<=cnt_queue-1'b1;
                end
                ST_NODE:begin
                    reg_node_address<=reg_node_row*C_COLUMNS+reg_node_column;cnt_direction<=0;
                    if(reg_node_column < reg_min_column)begin reg_min_column<=reg_node_column;end
                    if(reg_node_column > reg_max_column)begin reg_max_column<=reg_node_column;end
                    if(reg_node_row < reg_min_row)begin reg_min_row<=reg_node_row;end
                    if(reg_node_row > reg_max_row)begin reg_max_row<=reg_node_row;end
                end
                ST_NEIGHBOR_LOAD:begin
                    reg_neighbor_cell<=wire_scan_cell;
                    reg_neighbor_column<=dec_neighbor_column;reg_neighbor_row<=dec_neighbor_row;
                end
                ST_NEIGHBOR_CHECK:if(flag_neighbor_match)begin
                    if(flag_queue_full)begin flag_overflow_o<=1;end
                    else begin cnt_tail<=cnt_tail+1'b1;cnt_queue<=cnt_queue+1'b1;end
                end
                ST_NEIGHBOR_ADVANCE:cnt_direction<=cnt_direction+1'b1;
                ST_REGION_MEASURE:begin
                    reg_left<=wire_left < C_X_MIN ? C_X_MIN : wire_left[11:0];
                    reg_right<=wire_right >= C_X_END ? C_X_END-1 : wire_right[11:0];
                    reg_top<=wire_top < C_Y_MIN ? C_Y_MIN : wire_top[11:0];
                    reg_bottom<=wire_bottom >= C_Y_END ? C_Y_END-1 : wire_bottom[11:0];
                end
                ST_REGION_SIZE:begin reg_width<=reg_right-reg_left+1'b1;reg_height<=reg_bottom-reg_top+1'b1;end
                ST_REGION_AREA:reg_box_area<=reg_width*reg_height;
                ST_REGION_FILTER:begin
                    // 较大连通区域即使尺寸/形状不合格仍保持占用；孤立小片不累计成球。
                    if(reg_region_area >= C_MIN_AREA && reg_left < C_GATE_END && reg_right >= C_GATE_MIN)begin
                        flag_gate_occupied_o<=1;
                    end
                    reg_reject[0]<=reg_region_area < C_MIN_AREA;
                    reg_reject[1]<=reg_width < C_MIN_SIZE || reg_width > C_MAX_SIZE || reg_height < C_MIN_SIZE || reg_height > C_MAX_SIZE;
                    reg_reject[2]<=reg_width > ({1'b0,reg_height} << 1) || reg_height > ({1'b0,reg_width} << 1);
                    reg_reject[3]<=({6'd0,reg_region_area} << 2) < reg_box_area;
                end
                ST_REGION_EMIT:begin
                    if(reg_region_area > reg_diag_area_o)begin
                        reg_diag_width_o<=reg_width;reg_diag_height_o<=reg_height;reg_diag_area_o<=reg_region_area;
                        reg_diag_reject_o<=reg_reject;reg_diag_box_area<=reg_box_area;
                    end
                    if(reg_reject == 0)begin
                        if(flag_candidate_overflow)begin flag_overflow_o<=1;end
                        else begin
                            cnt_candidates<=cnt_candidates+1'b1;reg_valid_o<=1;
                            reg_color_o<=reg_region_color;reg_area_o<=reg_region_area;
                            reg_left_o<=reg_left;reg_right_o<=reg_right;reg_top_o<=reg_top;reg_bottom_o<=reg_bottom;
                        end
                    end
                end
                ST_SCAN_ADVANCE:begin
                    cnt_scan_address<=cnt_scan_address+1'b1;
                    if(cnt_scan_column == C_COLUMNS-1)begin cnt_scan_column<=0;cnt_scan_row<=cnt_scan_row+1'b1;end
                    else begin cnt_scan_column<=cnt_scan_column+1'b1;end
                end
                ST_DIAG_INIT:begin reg_fill_remaining<=reg_diag_area_o*100;reg_diag_fill_o<=0;end
                ST_DIAG_DIVIDE:if(reg_fill_remaining >= {1'b0,reg_diag_box_area})begin
                    reg_fill_remaining<=reg_fill_remaining-{1'b0,reg_diag_box_area};reg_diag_fill_o<=reg_diag_fill_o+1'b1;
                end
                ST_DONE:reg_done_o<=1;
                default:begin end
            endcase
        end
    end
    assign o_frame_start=reg_start_o;
    assign o_candidate_valid=reg_valid_o;
    assign o_color=reg_color_o;
    assign o_area=reg_area_o;
    assign o_x_min=reg_left_o;
    assign o_x_max=reg_right_o;
    assign o_y_min=reg_top_o;
    assign o_y_max=reg_bottom_o;
    assign o_frame_done=reg_done_o;
    assign o_gate_pixels=reg_gate_o;
    assign o_gate_occupied=flag_gate_occupied_o;
    assign o_epoch=reg_epoch_o;
    assign o_frame_id=reg_frame_o;
    assign o_stamp=reg_stamp_o;
    assign o_overflow=flag_overflow_o;
    assign o_fault=flag_fault_o;
    assign o_error=flag_error_o;
    assign o_diag_count=cnt_candidates;
    assign o_diag_width=reg_diag_width_o;
    assign o_diag_height=reg_diag_height_o;
    assign o_diag_area=reg_diag_area_o;
    assign o_diag_fill=reg_diag_fill_o;
    assign o_diag_reject=reg_diag_reject_o;
endmodule
