`timescale 1ns / 1ps
// 四像素采集保持满速；4x4单元按同色四邻接分离，统计分支不延迟视频。
module ball_components #(
    parameter C_WIDTH=1280,C_HEIGHT=720,
    parameter C_X_MIN=64,C_Y_MIN=160,C_X_END=1216,C_Y_END=640,
    parameter C_GATE_MIN=544,C_GATE_END=736,
    parameter C_MIN_AREA=128,C_MIN_SIZE=12,C_MAX_SIZE=384,
    parameter C_MAX_CANDIDATES=8,C_QUEUE_BITS=12,
    parameter C_ROUND_MIN_SIZE=24,C_ROUND_MAX_SIZE=384,
    parameter [6:0] C_ROUND_COMPACT=27,parameter C_HIGHLIGHT_REPAIR=0,
    parameter C_PANEL_CONFIG=0,parameter C_FRAME_CHECK=0
)(
    input i_clk,
    input i_rstn,
    input i_session_clear,
    input i_capture_fault,
    input i_valid,
    input i_sof,
    input i_eof,
    input [11:0] i_x,
    input [11:0] i_y,
    input [7:0] i_labels,
    input [3:0] i_highlight,
    input [2:0] i_gate_hits,
    input [15:0] i_epoch,
    input i_shape_enable,
    input [191:0] i_settings,
    output o_frame_start,
    output o_candidate_valid,
    output o_reject_valid,
    output [1:0] o_color,
    output [1:0] o_shape_flags,
    output [3:0] o_shape_reject,
    output [19:0] o_area,
    output [11:0] o_x_min,
    output [11:0] o_x_max,
    output [11:0] o_y_min,
    output [11:0] o_y_max,
    output o_frame_done,
    output [19:0] o_gate_pixels,
    output o_gate_occupied,
    output [15:0] o_epoch,
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
    localparam C_ROW_PIXEL_BITS=$clog2(C_COLUMNS*16+1);
    localparam C_SUMMARY_BITS=C_COLUMN_BITS*2+C_ROW_PIXEL_BITS+1;
                                                                              
                                                                                                             
    localparam C_FIT_NUM_BITS=C_COLUMN_BITS+C_ROW_BITS+8;
    localparam C_FIT_VALUE_BITS=C_COLUMN_BITS+9;
    localparam C_CONTOUR_ERROR_BITS=C_COLUMN_BITS+13;
    localparam [C_CONTOUR_ERROR_BITS:0] C_CONTOUR_MARGIN=512;
    localparam C_BOTTOM_ROW=(C_LAST_ROW*4 < C_HEIGHT ? C_LAST_ROW*4 : C_HEIGHT)-1;
    localparam ST_IDLE=0,ST_SCAN_READ=1,ST_SCAN_LOAD=2,ST_SCAN_CHECK=3,
        ST_POP_TEST=4,ST_POP_READ=5,ST_POP_LOAD=6,ST_NODE=7,
        ST_NEIGHBOR_READ=8,ST_NEIGHBOR_LOAD=9,ST_NEIGHBOR_CHECK=10,ST_NEIGHBOR_ADVANCE=11,
        ST_REGION_MEASURE=12,ST_REGION_SIZE=13,ST_REGION_AREA=14,ST_REGION_FILTER=15,
        ST_REGION_EMIT=16,ST_SCAN_ADVANCE=17,ST_DIAG_INIT=18,ST_DIAG_DIVIDE=19,ST_DONE=20,
        ST_SHAPE_INIT=21,ST_SHAPE_SQUARE=22,ST_SHAPE_CHECK=23,
        ST_HOLE_READ=24,ST_HOLE_LOAD=25,ST_HOLE_CHECK=26,ST_HOLE_COMMIT=27,
        ST_ROW_RESET=28,ST_ROW_CLEAR=29,ST_PROFILE_INIT=30,ST_PROFILE_READ=31,
        ST_PROFILE_LOAD=32,ST_PROFILE_ADVANCE=33,ST_PROFILE_CHECK=34,ST_ROW_ABORT=35,
        ST_PROBE_INIT=36,ST_PROBE_NODE_READ=37,ST_PROBE_NODE_LOAD=38,
        ST_PROBE_NEXT_READ=39,ST_PROBE_NEXT_LOAD=40,ST_PROBE_NEXT_CHECK=41,
        ST_PROBE_LOOK_READ=42,ST_PROBE_LOOK_LOAD=43,ST_PROBE_LOOK_CHECK=44,
        ST_PROBE_APPEND=45,ST_PROBE_ADVANCE=46,
        ST_CONTOUR_INIT=47,ST_CONTOUR_READ=48,ST_CONTOUR_LOAD=49,ST_CONTOUR_CAPTURE=50,
        ST_CONTOUR_COEFF=51,ST_CONTOUR_MULTIPLY=52,ST_CONTOUR_DIV_INIT=53,
        ST_CONTOUR_DIVIDE=54,ST_CONTOUR_ERROR=55,ST_CONTOUR_NEXT_POINT=56,
        ST_CONTOUR_NEXT_MODEL=57,ST_CONTOUR_FINISH=58,
        ST_CONTOUR_ADDRESS=59,ST_CONTOUR_REQUEST=60,ST_CONTOUR_DELTA=61,
        ST_OWNER_READ=62,ST_OWNER_CHECK=63;
    reg [5:0] state_current,state_next;
    wire [6:0] wire_discovery_size=i_settings[7:1]==0 ? 7'd12 : i_settings[7:1];
    wire [19:0] wire_discovery_area=i_settings[15:10]==0 ? 20'd64 : {10'd0,i_settings[15:10],4'd0};
    reg flag_capture_bank,flag_scan_bank,flag_drop_frame;
    reg flag_capture,flag_capture_first,flag_capture_last,flag_roi_end,reg_capture_bank;
    reg [C_COLUMN_BITS-1:0] reg_capture_column;
    reg [C_ADDRESS_BITS-1:0] reg_capture_address;
    reg [4:0] reg_capture_red,reg_capture_yellow,reg_capture_green,reg_capture_white;
    reg [15:0] reg_capture_epoch;
    reg flag_capture_shape,flag_scan_shape,flag_shape_reject;
    reg [16:0] cnt_region_cells;
    reg [18:0] cnt_perimeter;
    reg [37:0] reg_square;
    reg [4:0] cnt_square;
    wire [37:0] wire_compact_limit=cnt_region_cells*C_ROUND_COMPACT;
    wire [37:0] wire_grid_area={21'd0,cnt_region_cells}<<8;
    reg [25:0] reg_box_area,reg_diag_box_area;
    reg [11:0] reg_left,reg_right,reg_top,reg_bottom,reg_width,reg_height;
    wire [37:0] wire_grid_limit=({12'd0,reg_box_area}<<4)-{12'd0,reg_box_area};
    reg [19:0] cnt_gate;
    reg [4:0] dec_red,dec_yellow,dec_green,dec_white;
    integer lane;
    wire flag_busy=state_current != ST_IDLE && state_current != ST_ROW_RESET;
    wire flag_conflict=flag_busy && flag_capture_bank == flag_scan_bank;
    wire flag_drop_now=i_sof ? flag_conflict : flag_drop_frame;
    wire flag_inside=i_valid && (i_x >> 2) >= C_FIRST_COLUMN && (i_x >> 2) < C_LAST_COLUMN &&
        (i_y >> 2) >= C_FIRST_ROW && (i_y >> 2) < C_LAST_ROW;
    wire wire_capture_fault=C_FRAME_CHECK ? i_capture_fault && !(i_valid && i_sof) : 1'b0;
    wire flag_capture_now=flag_inside && !flag_drop_now && !i_session_clear && !wire_capture_fault;
    wire [C_COLUMN_BITS-1:0] wire_capture_column=(i_x >> 2)-C_FIRST_COLUMN;
    wire [C_ADDRESS_BITS-1:0] wire_capture_address=((i_y >> 2)-C_FIRST_ROW)*C_COLUMNS+wire_capture_column;
    wire [19:0] wire_row_counts;
    wire [4:0] wire_white=(flag_capture_first ? 5'd0 : wire_row_counts[19:15])+reg_capture_white;
    wire [4:0] wire_red=(flag_capture_first ? 5'd0 : wire_row_counts[14:10])+reg_capture_red;
    wire [4:0] wire_yellow=(flag_capture_first ? 5'd0 : wire_row_counts[9:5])+reg_capture_yellow;
    wire [4:0] wire_green=(flag_capture_first ? 5'd0 : wire_row_counts[4:0])+reg_capture_green;
                                                             
                                                                          
    wire [5:0] wire_red_others={1'b0,wire_yellow}+{1'b0,wire_green};
    wire [5:0] wire_yellow_others={1'b0,wire_red}+{1'b0,wire_green};
    wire [5:0] wire_green_others={1'b0,wire_red}+{1'b0,wire_yellow};
    wire [7:0] wire_red_limit={1'b0,wire_red_others,1'b0}+{2'd0,wire_red_others};
    wire [7:0] wire_yellow_limit={1'b0,wire_yellow_others,1'b0}+{2'd0,wire_yellow_others};
    wire [7:0] wire_green_limit={1'b0,wire_green_others,1'b0}+{2'd0,wire_green_others};
    reg [5:0] dec_cell;
    wire [4:0] wire_red_code=wire_red-5'd3;
    wire [4:0] wire_yellow_code=wire_yellow-5'd3;
    wire [4:0] wire_green_code=wire_green-5'd3;

    // 门区像素独立统计，有效空拍不重复累计。
    always @(*)begin
        dec_red=0;dec_yellow=0;dec_green=0;dec_white=0;
        for(lane=0;lane<4;lane=lane+1)begin
            if(i_highlight[lane])dec_white=dec_white+1'b1;
            case(i_labels[lane*2 +:2])
                1:dec_red=dec_red+1'b1;
                2:dec_yellow=dec_yellow+1'b1;
                3:dec_green=dec_green+1'b1;
                default:begin end
            endcase
        end
                                                                                           
        dec_cell=0;
        if(wire_red >= 4 && {3'd0,wire_red} >= wire_red_limit)begin
            dec_cell={2'd1,wire_red_code[3:0]};
        end else if(wire_yellow >= 4 && {3'd0,wire_yellow} >= wire_yellow_limit)begin
            dec_cell={2'd2,wire_yellow_code[3:0]};
        end else if(wire_green >= 4 && {3'd0,wire_green} >= wire_green_limit)begin
            dec_cell={2'd3,wire_green_code[3:0]};
        end else if(C_HIGHLIGHT_REPAIR && wire_white>=12)begin
                                                                                    
            dec_cell=6'h0e;
        end
    end
    ball_component_store #(.C_DEPTH(C_COLUMNS),.C_ADDR_BITS(C_COLUMN_BITS),.C_DATA_BITS(20)) row_Inst(
        .i_clk(i_clk),.i_read_enable(flag_capture_now),.i_read_address(wire_capture_column),
        .i_write_enable(flag_capture && !i_session_clear),.i_write_address(reg_capture_column),
        .i_write_data({wire_white,wire_red,wire_yellow,wire_green}),.o_read_data(wire_row_counts));
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            flag_capture_bank<=0;flag_drop_frame<=0;flag_capture<=0;flag_capture_first<=0;
            flag_capture_last<=0;flag_roi_end<=0;reg_capture_bank<=0;reg_capture_column<=0;
            reg_capture_address<=0;reg_capture_red<=0;reg_capture_yellow<=0;reg_capture_green<=0;reg_capture_white<=0;
            reg_capture_epoch<=0;flag_capture_shape<=0;cnt_gate<=0;
        end else if(i_session_clear)begin
            flag_capture_bank<=0;flag_drop_frame<=1;flag_capture<=0;flag_capture_first<=0;
            flag_capture_last<=0;flag_roi_end<=0;reg_capture_bank<=0;reg_capture_column<=0;
            reg_capture_address<=0;reg_capture_red<=0;reg_capture_yellow<=0;reg_capture_green<=0;reg_capture_white<=0;
            reg_capture_epoch<=0;flag_capture_shape<=0;cnt_gate<=0;
        end else if(wire_capture_fault)begin
                                                                                              
            flag_drop_frame<=1;flag_capture<=0;flag_roi_end<=0;
        end else begin
            flag_capture<=flag_capture_now;
            flag_roi_end<=flag_capture_now && i_y == C_BOTTOM_ROW && wire_capture_column == C_COLUMNS-1;
            if(i_valid)begin
                if(i_sof)begin flag_drop_frame<=flag_conflict;end
                cnt_gate<=(i_sof ? 20'd0 : cnt_gate)+i_gate_hits;
                if(i_eof)begin flag_capture_bank<=!flag_capture_bank;end
            end
            if(flag_capture_now)begin
                reg_capture_bank<=flag_capture_bank;reg_capture_column<=wire_capture_column;
                reg_capture_address<=wire_capture_address;reg_capture_epoch<=i_epoch;flag_capture_shape<=i_shape_enable;
                flag_capture_first<=i_y[1:0] == 0;
                flag_capture_last<=i_y[1:0] == 3 || i_y == C_HEIGHT-1;
                reg_capture_red<=dec_red;reg_capture_yellow<=dec_yellow;reg_capture_green<=dec_green;reg_capture_white<=dec_white;
            end
        end
    end

    reg [C_ADDRESS_BITS-1:0] cnt_scan_address,reg_node_address,reg_neighbor_address;
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
    wire flag_seed=state_current == ST_SCAN_CHECK && reg_cell[4:0] != 0 && reg_cell[6:5] != 0;
    wire flag_neighbor_match=reg_neighbor_cell[4:0] != 0 && reg_neighbor_cell[6:5] == reg_region_color && reg_neighbor_cell[6:5] != 0;
                                                                                            
    reg [2:0] cnt_hole_direction;
    reg [3:0] cnt_hole_distance;
    reg [1:0] reg_hole_color;
    reg flag_hole_white,flag_hole_accept,flag_hole_perimeter;
    reg [10:0] cnt_red_probes;
    reg [18:0] cnt_hole_work;
                                                                                          
    wire [2:0] wire_hole_direction=flag_hole_perimeter && C_PANEL_CONFIG && cnt_hole_direction<4 ?
        {1'b0,(cnt_hole_direction[1:0]+cnt_direction)} : cnt_hole_direction;
    reg signed [12:0] dec_hole_column,dec_hole_row;
    reg flag_hole_valid;
    reg [C_ADDRESS_BITS-1:0] dec_hole_address;
    reg signed [C_ADDRESS_BITS+2:0] dec_hole_offset;
    wire flag_white_hole_target=C_HIGHLIGHT_REPAIR && flag_scan_shape &&
        reg_neighbor_cell[6:5]==0 && reg_neighbor_cell[4:0]==17;
                                                                                
                                                                                           
    // 孔洞填补范围限于种子周围七格内的32格，大孔洞保留为次品。
    wire flag_red_hole_target=C_HIGHLIGHT_REPAIR && flag_scan_shape &&
        (C_PANEL_CONFIG ? reg_neighbor_cell[6:5]!=reg_region_color : reg_region_color==1 && reg_neighbor_cell[6:5]!=reg_region_color) &&
        !(reg_neighbor_cell[6:5]==0 && reg_neighbor_cell[4:0]>=17) &&
        cnt_region_cells>=8 && cnt_red_probes<(C_PANEL_CONFIG ? 128 : 1024) &&
        (!C_PANEL_CONFIG || cnt_hole_work<19'd262143);
    wire flag_hole_target=flag_white_hole_target || flag_red_hole_target;
    wire flag_hole_push=state_current==ST_HOLE_COMMIT && flag_hole_accept && !flag_hole_perimeter;
    wire [3:0] wire_hole_distance_limit=C_PANEL_CONFIG && flag_hole_perimeter ? 4'd7 : 4'd2;
    reg signed [C_ADDRESS_BITS+2:0] dec_hole_row_distance;
    always @(*)begin
        dec_hole_row_distance=$signed({1'b0,cnt_hole_distance})*C_COLUMNS;
        case(wire_hole_direction)
            0:dec_hole_offset=-$signed({1'b0,cnt_hole_distance});
            1:dec_hole_offset=$signed({1'b0,cnt_hole_distance});
            2:dec_hole_offset=-dec_hole_row_distance;
            3:dec_hole_offset=dec_hole_row_distance;
            4:dec_hole_offset=-dec_hole_row_distance-$signed({1'b0,cnt_hole_distance});
            5:dec_hole_offset=-dec_hole_row_distance+$signed({1'b0,cnt_hole_distance});
            6:dec_hole_offset=dec_hole_row_distance-$signed({1'b0,cnt_hole_distance});
            7:dec_hole_offset=dec_hole_row_distance+$signed({1'b0,cnt_hole_distance});
            default:dec_hole_offset=0;
        endcase
        dec_hole_column=$signed({1'b0,reg_neighbor_column});
        dec_hole_row=$signed({1'b0,reg_neighbor_row});
        case(wire_hole_direction)
            0,4,6:dec_hole_column=dec_hole_column-$signed({1'b0,cnt_hole_distance});
            1,5,7:dec_hole_column=dec_hole_column+$signed({1'b0,cnt_hole_distance});
            default:begin end
        endcase
        case(wire_hole_direction)
            2,4,5:dec_hole_row=dec_hole_row-$signed({1'b0,cnt_hole_distance});
            3,6,7:dec_hole_row=dec_hole_row+$signed({1'b0,cnt_hole_distance});
            default:begin end
        endcase
        flag_hole_valid=dec_hole_column>=0 && dec_hole_column<C_COLUMNS && dec_hole_row>=0 && dec_hole_row<C_ROWS;
                                                                                        
        dec_hole_address=$signed({3'b000,reg_neighbor_address})+dec_hole_offset;
    end
                                                                                  
                                                                                                
    localparam C_PROBE_POSITION_BITS=C_COLUMN_BITS+C_ROW_BITS;
    localparam C_PROBE_WORD_BITS=C_PROBE_POSITION_BITS+C_ADDRESS_BITS;
    reg [5:0] cnt_probe_count,cnt_probe_head,cnt_probe_lookup;
    reg [1:0] cnt_probe_direction,reg_probe_color;
    reg [C_COLUMN_BITS-1:0] reg_probe_column,dec_probe_column;
    reg [C_ROW_BITS-1:0] reg_probe_row,dec_probe_row;
    reg flag_probe_valid;
    reg [C_ADDRESS_BITS-1:0] reg_probe_address,dec_probe_address;
    wire [C_PROBE_WORD_BITS-1:0] wire_probe_data;
    wire [C_PROBE_POSITION_BITS-1:0] wire_probe_target={dec_probe_row,dec_probe_column};
    wire flag_probe_extent=({1'b0,dec_probe_column}<={1'b0,reg_neighbor_column}+7) &&
        ({1'b0,reg_neighbor_column}<={1'b0,dec_probe_column}+7) &&
        ({1'b0,dec_probe_row}<={1'b0,reg_neighbor_row}+7) &&
        ({1'b0,reg_neighbor_row}<={1'b0,dec_probe_row}+7);
    wire flag_probe_state=state_current>=ST_PROBE_INIT && state_current<=ST_PROBE_ADVANCE;
    wire flag_hole_work_state=flag_probe_state || state_current==ST_HOLE_READ ||
        state_current==ST_HOLE_LOAD || state_current==ST_HOLE_CHECK;
    wire flag_hole_work_expired=C_PANEL_CONFIG && flag_hole_work_state && cnt_hole_work>=19'd262143;
    always @(*)begin
        dec_probe_column=reg_probe_column;dec_probe_row=reg_probe_row;
        dec_probe_address=reg_probe_address;flag_probe_valid=1;
        case(cnt_probe_direction)
            0:begin flag_probe_valid=reg_probe_column!=0;dec_probe_column=reg_probe_column-1'b1;dec_probe_address=dec_probe_address-1'b1;end
            1:begin flag_probe_valid=reg_probe_column<C_COLUMNS-1;dec_probe_column=reg_probe_column+1'b1;dec_probe_address=dec_probe_address+1'b1;end
            2:begin flag_probe_valid=reg_probe_row!=0;dec_probe_row=reg_probe_row-1'b1;dec_probe_address=dec_probe_address-C_COLUMNS;end
            3:begin flag_probe_valid=reg_probe_row<C_ROWS-1;dec_probe_row=reg_probe_row+1'b1;dec_probe_address=dec_probe_address+C_COLUMNS;end
            default:begin end
        endcase
    end
    generate if(C_PANEL_CONFIG)begin:gen_closed_hole
        ball_component_store #(.C_DEPTH(32),.C_ADDR_BITS(5),.C_DATA_BITS(C_PROBE_WORD_BITS)) work_Inst(
            .i_clk(i_clk),.i_read_enable(state_current==ST_PROBE_NODE_READ || state_current==ST_PROBE_LOOK_READ),
            .i_read_address(state_current==ST_PROBE_NODE_READ ? cnt_probe_head[4:0] : cnt_probe_lookup[4:0]),
            .i_write_enable((state_current==ST_PROBE_INIT || state_current==ST_PROBE_APPEND) && !i_session_clear),
            .i_write_address(state_current==ST_PROBE_INIT ? 5'd0 : cnt_probe_count[4:0]),
            .i_write_data(state_current==ST_PROBE_INIT ? {reg_neighbor_address,reg_neighbor_row,reg_neighbor_column} :
                {dec_probe_address,wire_probe_target}),
            .o_read_data(wire_probe_data));
    end else begin:gen_no_closed_hole
        assign wire_probe_data={C_PROBE_WORD_BITS{1'b0}};
    end endgenerate
    wire flag_queue_full=cnt_queue == C_QUEUE_DEPTH;
    wire flag_push=((state_current == ST_NEIGHBOR_CHECK && flag_neighbor_match) || flag_hole_push) && !flag_queue_full;
    wire flag_queue_write=flag_seed || flag_push;
    wire [C_QUEUE_BITS-1:0] wire_queue_write_address=flag_seed ? {C_QUEUE_BITS{1'b0}} : cnt_tail;
    wire [C_QUEUE_WORD_BITS-1:0] wire_queue_write_data=flag_seed ?
        {reg_cell[4:0],cnt_scan_row,cnt_scan_column} :
        {flag_hole_push ? (flag_hole_perimeter ? 5'd0 : 5'd16) : reg_neighbor_cell[4:0],reg_neighbor_row,reg_neighbor_column};
    ball_component_store #(.C_DEPTH(C_QUEUE_DEPTH),.C_ADDR_BITS(C_QUEUE_BITS),.C_DATA_BITS(C_QUEUE_WORD_BITS)) queue_Inst(
        .i_clk(i_clk),.i_read_enable(state_current == ST_POP_READ),.i_read_address(cnt_head),
        .i_write_enable(flag_queue_write && !i_session_clear),.i_write_address(wire_queue_write_address),
        .i_write_data(wire_queue_write_data),.o_read_data(wire_queue_data));

                                                                           
                                                                                         
    reg [C_ROW_BITS-1:0] cnt_summary_row;
    reg [4:0] reg_node_area;
    reg [3:0] cnt_profile;
    reg [C_ROW_BITS-1:0] reg_profile_top,reg_profile_quarter_top,reg_profile_middle,
        reg_profile_quarter_bottom,reg_profile_bottom;
    reg [C_ROW_BITS-1:0] dec_summary_read_row;
    wire [C_SUMMARY_BITS-1:0] wire_summary_data;
    wire flag_summary_valid=wire_summary_data[C_SUMMARY_BITS-1];
    wire [C_COLUMN_BITS-1:0] wire_summary_left=wire_summary_data[C_COLUMN_BITS-1:0];
    wire [C_COLUMN_BITS-1:0] wire_summary_right=wire_summary_data[C_COLUMN_BITS +:C_COLUMN_BITS];
    wire [C_ROW_PIXEL_BITS-1:0] wire_summary_area=wire_summary_data[C_COLUMN_BITS*2 +:C_ROW_PIXEL_BITS];
    wire [C_COLUMN_BITS-1:0] wire_summary_next_left=flag_summary_valid && wire_summary_left<reg_node_column ? wire_summary_left : reg_node_column;
    wire [C_COLUMN_BITS-1:0] wire_summary_next_right=flag_summary_valid && wire_summary_right>reg_node_column ? wire_summary_right : reg_node_column;
    wire [C_ROW_PIXEL_BITS-1:0] wire_summary_next_area=(flag_summary_valid ? wire_summary_area : {C_ROW_PIXEL_BITS{1'b0}})+reg_node_area;
    wire [C_COLUMN_BITS:0] wire_summary_width={1'b0,wire_summary_right}-{1'b0,wire_summary_left}+1'b1;
    reg [C_COLUMN_BITS:0] reg_profile_width[0:4];
    reg [4:0] reg_profile_support;
    reg [C_COLUMN_BITS:0] reg_profile_box_width;
    reg flag_profile_small,flag_profile_reject,flag_summary_cleaned;
    reg flag_profile_large,flag_profile_center_bad,flag_profile_center_loss;
    reg [1:0] reg_profile_arc_bad;
    reg [C_COLUMN_BITS+5:0] reg_outer_low,reg_outer_high,reg_quarter_low,reg_quarter_high;
    wire flag_summary_supported=flag_summary_valid && wire_summary_area>=(wire_summary_width<<2);
                                                                                 
                                                                                    
    wire [C_COLUMN_BITS:0] wire_profile_reference=flag_profile_large ?
        (reg_profile_width[2]+1'b1<reg_profile_box_width ? reg_profile_box_width : reg_profile_width[2]) : wire_summary_width;
    wire [C_COLUMN_BITS+5:0] wire_profile_scaled={1'b0,reg_profile_width[cnt_profile],4'd0};
    wire [C_COLUMN_BITS+5:0] wire_profile_tolerant=wire_profile_scaled+(flag_profile_small ? 6'd32 : 6'd16);
    wire flag_profile_outer_bad=!reg_profile_support[cnt_profile] ||
        (!flag_profile_small && wire_profile_tolerant<reg_outer_low) || wire_profile_scaled>reg_outer_high;
    wire flag_profile_quarter_bad=!reg_profile_support[cnt_profile] ||
        wire_profile_tolerant<reg_quarter_low || wire_profile_scaled>reg_quarter_high;
    wire [C_ROW_BITS-1:0] wire_region_row_span=reg_max_row-reg_min_row;
                                                                             
                                                                               
    reg [3:0] cnt_contour_point,cnt_contour_knot;
    reg flag_contour_side,flag_contour_valid,flag_contour_rectangle;
    reg [C_COLUMN_BITS-1:0] reg_contour_left[0:8],reg_contour_right[0:8];
    reg [C_ROW_BITS-1:0] reg_contour_row[0:8];
    reg [C_ROW_BITS-1:0] reg_contour_span,reg_contour_offset,reg_contour_address;
    reg [C_COLUMN_BITS:0] reg_contour_reference;
    reg [C_ROW_BITS+4:0] dec_contour_offset;
    reg [8:0] dec_contour_ellipse;
    wire [C_ROW_BITS-1:0] wire_contour_row=reg_contour_address;
    wire [C_COLUMN_BITS:0] wire_contour_width={1'b0,reg_max_column}-{1'b0,reg_min_column}+1'b1;
    wire flag_contour_large=C_PANEL_CONFIG && reg_width>48 && reg_height>48;
    wire [C_FIT_VALUE_BITS-1:0] wire_contour_circle_observed=wire_summary_width<<8;
    wire [C_FIT_VALUE_BITS-1:0] wire_contour_circle_expected=reg_contour_reference*dec_contour_ellipse;
    reg [C_FIT_VALUE_BITS-1:0] reg_circle_observed,reg_circle_expected,reg_circle_delta;
    wire [C_FIT_VALUE_BITS-1:0] wire_contour_circle_delta=reg_circle_observed>=reg_circle_expected ?
        reg_circle_observed-reg_circle_expected : reg_circle_expected-reg_circle_observed;
    reg [C_CONTOUR_ERROR_BITS-1:0] reg_contour_circle_error,reg_contour_error,reg_contour_best_left,reg_contour_best_right;
    wire [C_CONTOUR_ERROR_BITS:0] wire_contour_line_error={1'b0,reg_contour_best_left}+{1'b0,reg_contour_best_right};
    wire [C_CONTOUR_ERROR_BITS:0] wire_contour_line_limit=(reg_contour_reference<<6)+C_CONTOUR_MARGIN;
    reg [C_COLUMN_BITS:0] reg_fit_start,reg_fit_end,reg_fit_point;
    reg [C_ROW_BITS:0] reg_fit_first_row,reg_fit_last_row,reg_fit_point_row,reg_fit_denominator;
    reg flag_fit_negative;
    reg [C_FIT_NUM_BITS-1:0] reg_fit_numerator,reg_fit_dividend,reg_fit_quotient;
    reg signed [C_FIT_VALUE_BITS-1:0] reg_fit_observed;
    reg [C_ROW_BITS+1:0] reg_fit_remainder;
    reg [5:0] cnt_fit_divide;
    wire [C_COLUMN_BITS-1:0] wire_fit_distance=reg_fit_end>=reg_fit_start ?
        reg_fit_end-reg_fit_start : reg_fit_start-reg_fit_end;
    wire [C_ROW_BITS-1:0] wire_fit_row_offset=reg_fit_point_row-reg_fit_first_row;
    wire [C_ROW_BITS-1:0] wire_fit_row_extent=reg_fit_last_row-reg_fit_first_row;
    wire [C_COLUMN_BITS+C_ROW_BITS-1:0] wire_fit_product=wire_fit_distance*wire_fit_row_offset;
    wire signed [C_COLUMN_BITS:0] wire_fit_observed_delta=$signed({1'b0,reg_fit_point[C_COLUMN_BITS-1:0]})-
        $signed({1'b0,reg_fit_start[C_COLUMN_BITS-1:0]});
    wire [C_ROW_BITS+1:0] wire_fit_trial={reg_fit_remainder[C_ROW_BITS:0],reg_fit_dividend[C_FIT_NUM_BITS-1]};
    wire signed [C_FIT_VALUE_BITS-1:0] wire_fit_interpolation=flag_fit_negative ?
        -$signed({1'b0,reg_fit_quotient[C_FIT_VALUE_BITS-2:0]}) : $signed({1'b0,reg_fit_quotient[C_FIT_VALUE_BITS-2:0]});
    wire signed [C_FIT_VALUE_BITS:0] wire_fit_residual=$signed({reg_fit_observed[C_FIT_VALUE_BITS-1],reg_fit_observed})-
        $signed({wire_fit_interpolation[C_FIT_VALUE_BITS-1],wire_fit_interpolation});
    wire [C_FIT_VALUE_BITS:0] wire_fit_absolute=wire_fit_residual[C_FIT_VALUE_BITS] ? -wire_fit_residual : wire_fit_residual;
    wire [3:0] wire_fit_first_index=cnt_contour_point<=cnt_contour_knot ? 4'd0 : cnt_contour_knot;
    wire [3:0] wire_fit_last_index=cnt_contour_point<=cnt_contour_knot ? cnt_contour_knot : 4'd8;
    always @(*)begin
        dec_contour_offset=0;dec_contour_ellipse=0;
        case(cnt_contour_point)
            0:begin dec_contour_offset=reg_contour_span;dec_contour_ellipse=124;end
            1:begin dec_contour_offset=reg_contour_span*2;dec_contour_ellipse=169;end
            2:begin dec_contour_offset=reg_contour_span*4;dec_contour_ellipse=222;end
            3:begin dec_contour_offset=reg_contour_span*6;dec_contour_ellipse=248;end
            4:begin dec_contour_offset=reg_contour_span*8;dec_contour_ellipse=256;end
            5:begin dec_contour_offset=reg_contour_span*10;dec_contour_ellipse=248;end
            6:begin dec_contour_offset=reg_contour_span*12;dec_contour_ellipse=222;end
            7:begin dec_contour_offset=reg_contour_span*14;dec_contour_ellipse=169;end
            8:begin dec_contour_offset=reg_contour_span*15;dec_contour_ellipse=124;end
            default:begin end
        endcase
    end
    always @(*)begin
        dec_summary_read_row=wire_queue_data[C_COLUMN_BITS +:C_ROW_BITS];
        if(state_current==ST_PROFILE_READ)begin
            case(cnt_profile)
                0:dec_summary_read_row=reg_profile_top;
                1:dec_summary_read_row=reg_profile_quarter_top;
                2:dec_summary_read_row=reg_profile_middle;
                3:dec_summary_read_row=reg_profile_quarter_bottom;
                4:dec_summary_read_row=reg_profile_bottom;
                5:dec_summary_read_row=reg_profile_middle>reg_min_row ? reg_profile_middle-1'b1 : reg_min_row;
                6:dec_summary_read_row=reg_profile_middle<reg_max_row ? reg_profile_middle+1'b1 : reg_max_row;
                7:dec_summary_read_row=reg_profile_middle-reg_min_row>=2 ? reg_profile_middle-2'd2 : reg_min_row;
                default:dec_summary_read_row=reg_max_row-reg_profile_middle>=2 ? reg_profile_middle+2'd2 : reg_max_row;
            endcase
        end
        if(state_current==ST_CONTOUR_REQUEST)dec_summary_read_row=wire_contour_row;
    end
    generate if(C_PANEL_CONFIG)begin:gen_region_rows
        wire flag_clear=state_current==ST_ROW_RESET || state_current==ST_ROW_CLEAR || state_current==ST_ROW_ABORT;
        ball_component_store #(.C_DEPTH(C_ROWS),.C_ADDR_BITS(C_ROW_BITS),.C_DATA_BITS(C_SUMMARY_BITS)) rows_Inst(
            .i_clk(i_clk),.i_read_enable(state_current==ST_POP_LOAD || state_current==ST_PROFILE_READ || state_current==ST_CONTOUR_REQUEST),
            .i_read_address(dec_summary_read_row),.i_write_enable((flag_clear || state_current==ST_NODE) && !i_session_clear),
            .i_write_address(flag_clear ? cnt_summary_row : reg_node_row),
            .i_write_data(flag_clear ? {C_SUMMARY_BITS{1'b0}} :
                {1'b1,wire_summary_next_area,wire_summary_next_right,wire_summary_next_left}),.o_read_data(wire_summary_data));
    end else begin:gen_no_region_rows
        assign wire_summary_data={C_SUMMARY_BITS{1'b0}};
    end endgenerate

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
    wire flag_grid_read=state_current == ST_SCAN_READ || (state_current == ST_NEIGHBOR_READ && flag_neighbor_valid) ||
        (state_current==ST_HOLE_READ && flag_hole_valid) ||
        (state_current==ST_PROBE_NEXT_READ && flag_probe_valid);
    wire [C_ADDRESS_BITS-1:0] wire_grid_read_address=state_current == ST_SCAN_READ ? cnt_scan_address :
        state_current==ST_HOLE_READ ? dec_hole_address :
        state_current==ST_PROBE_NEXT_READ ? dec_probe_address : dec_neighbor_address;
    wire flag_grid_clear=flag_seed || flag_push ||
        (state_current==ST_HOLE_COMMIT && !flag_hole_accept && !flag_hole_perimeter);
    wire [C_ADDRESS_BITS-1:0] wire_grid_clear_address=flag_seed ? cnt_scan_address : dec_neighbor_address;
    // 有效面积4..16编码为1..13；零表示空/已入队，保留颜色以统计边界。
    wire [11:0] wire_grid_data;
    genvar bank;
    generate
        for(bank=0;bank<2;bank=bank+1)begin:gen_frame_bank
            wire flag_cell_write=flag_capture && flag_capture_last && reg_capture_bank == bank;
            wire flag_cell_clear=flag_grid_clear && flag_scan_bank == bank;
            ball_component_store #(.C_DEPTH(C_CELLS),.C_ADDR_BITS(C_ADDRESS_BITS),.C_DATA_BITS(6)) frame_Inst(
                .i_clk(i_clk),.i_read_enable(flag_grid_read && flag_scan_bank == bank),.i_read_address(wire_grid_read_address),
                .i_write_enable((flag_cell_write || flag_cell_clear) && !i_session_clear),
                .i_write_address(flag_cell_write ? reg_capture_address : wire_grid_clear_address),
                .i_write_data(flag_cell_write ? dec_cell :
                    state_current==ST_HOLE_COMMIT && !flag_hole_accept ? 6'h0f :
                    {flag_seed ? reg_cell[6:5] : reg_region_color,4'd0}),.o_read_data(wire_grid_data[bank*6 +:6]));
        end
    endgenerate
    wire [5:0] wire_scan_code=flag_scan_bank ? wire_grid_data[11:6] : wire_grid_data[5:0];
    wire [4:0] wire_scan_area=wire_scan_code[3:0] == 0 ? 5'd0 : {1'b0,wire_scan_code[3:0]}+5'd3;
    wire [6:0] wire_scan_cell={wire_scan_code[5:4],wire_scan_area};

    reg [3:0] reg_reject,cnt_candidates;
    integer profile_index;
    reg reg_start_o,reg_valid_o,reg_done_o,flag_overflow_o,flag_fault_o,flag_error_o;
    reg [1:0] reg_color_o,reg_shape_o;
    reg [3:0] reg_shape_reject_o;
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
    wire [11:0] wire_roi_left=C_PANEL_CONFIG ? i_settings[43:32] : C_X_MIN;
    wire [11:0] wire_roi_top=C_PANEL_CONFIG ? i_settings[59:48] : C_Y_MIN;
    wire [11:0] wire_roi_last_x=C_PANEL_CONFIG ? i_settings[75:64]-12'd1 : C_X_END-1;
    wire [11:0] wire_roi_last_y=C_PANEL_CONFIG ? i_settings[91:80]-12'd1 : C_Y_END-1;
    wire flag_candidate_overflow=!C_PANEL_CONFIG && reg_reject == 0 && cnt_candidates == C_MAX_CANDIDATES;
    wire flag_large_shape=C_PANEL_CONFIG && reg_width>48 && reg_height>48;
    wire [37:0] wire_shape_limit=flag_large_shape ? ({21'd0,cnt_region_cells}<<5) : wire_compact_limit;
    wire flag_compact_reject=reg_square>wire_shape_limit || wire_grid_area>wire_grid_limit;
                                                                                                
    wire flag_small_known_ng=C_PANEL_CONFIG && (reg_width<C_ROUND_MIN_SIZE || reg_height<C_ROUND_MIN_SIZE) &&
        ({4'd0,reg_width}<i_settings[111:96] || {4'd0,reg_height}<i_settings[143:128] ||
         reg_region_area<{4'd0,i_settings[191:176]});
    wire flag_region_selected=!C_PANEL_CONFIG || i_settings[9:8]==0 || reg_region_color==i_settings[9:8];
    wire flag_region_round=!flag_shape_reject && (!C_PANEL_CONFIG || !flag_profile_reject) &&
        (!flag_contour_large || !flag_contour_rectangle) &&
        ({1'b0,reg_width}<<1)<=({1'b0,reg_height}<<1)+reg_height &&
        ({1'b0,reg_height}<<1)<=({1'b0,reg_width}<<1)+reg_width &&
        ({6'd0,reg_region_area}<<2)>=reg_box_area;
    wire flag_region_rectangle=flag_contour_large ? flag_contour_rectangle : wire_grid_area>=wire_grid_limit;
                                                                                                       
                                                                                                 
    localparam C_OWNER_WORD_BITS=22+C_COLUMN_BITS*2+C_ROW_BITS*2;
    reg [2:0] cnt_owner_parents;
    reg [1:0] cnt_owner_lookup;
    reg [2:0] reg_owner_colors;
    reg [19:0] reg_owner_filled_area;
    reg [C_ROW_BITS-1:0] reg_owner_last_bottom;
    reg flag_owner_suppressed;
    reg [C_COLUMN_BITS-1:0] reg_owner_core_left,reg_owner_core_right;
    reg [C_ROW_BITS-1:0] reg_owner_core_top,reg_owner_core_bottom;
    wire [2:0] wire_owner_color_mask=reg_region_color==1 ? 3'b001 : reg_region_color==2 ? 3'b010 : 3'b100;
    wire [19:0] wire_owner_colored_area=reg_region_area-reg_owner_filled_area;
    wire flag_owner_parent=C_PANEL_CONFIG && flag_contour_large && flag_region_round && flag_contour_valid &&
        {1'b0,reg_contour_circle_error}+C_CONTOUR_MARGIN<wire_contour_line_error &&
        ({6'd0,wire_owner_colored_area}<<1)>=reg_box_area &&
        reg_owner_core_left<=reg_owner_core_right && reg_owner_core_top>reg_min_row &&
        reg_owner_core_top<reg_owner_core_bottom && cnt_owner_parents<4;
    wire flag_owner_lookup=C_PANEL_CONFIG && flag_region_selected && cnt_owner_parents!=0 &&
        (|(reg_owner_colors & ~wire_owner_color_mask)) && !flag_region_round && !flag_region_rectangle;
    wire [C_OWNER_WORD_BITS-1:0] wire_owner_data;
    wire [C_COLUMN_BITS-1:0] wire_parent_left=wire_owner_data[C_COLUMN_BITS-1:0];
    wire [C_COLUMN_BITS-1:0] wire_parent_right=wire_owner_data[C_COLUMN_BITS +:C_COLUMN_BITS];
    wire [C_ROW_BITS-1:0] wire_parent_top=wire_owner_data[C_COLUMN_BITS*2 +:C_ROW_BITS];
    wire [C_ROW_BITS-1:0] wire_parent_bottom=wire_owner_data[C_COLUMN_BITS*2+C_ROW_BITS +:C_ROW_BITS];
    wire [19:0] wire_parent_area=wire_owner_data[C_COLUMN_BITS*2+C_ROW_BITS*2 +:20];
    wire [1:0] wire_parent_color=wire_owner_data[C_OWNER_WORD_BITS-1 -:2];
                                                                                                                   
    wire flag_owner_match=reg_reject[1:0]==0 && reg_region_color!=wire_parent_color &&
        {reg_region_area,3'd0}<{3'd0,wire_parent_area} &&
        reg_min_column>=wire_parent_left && reg_max_column<=wire_parent_right &&
        reg_min_row>=wire_parent_top && reg_max_row<=wire_parent_bottom;
    generate if(C_PANEL_CONFIG)begin:gen_owner_parents
        ball_component_store #(.C_DEPTH(4),.C_ADDR_BITS(2),.C_DATA_BITS(C_OWNER_WORD_BITS)) parents_Inst(
            .i_clk(i_clk),.i_read_enable(state_current==ST_OWNER_READ),.i_read_address(cnt_owner_lookup),
            .i_write_enable(state_current==ST_REGION_FILTER && flag_owner_parent && !i_session_clear),
            .i_write_address(cnt_owner_parents[1:0]),
            .i_write_data({reg_region_color,wire_owner_colored_area,reg_owner_core_bottom,reg_owner_core_top,reg_owner_core_right,reg_owner_core_left}),
            .o_read_data(wire_owner_data));
    end else begin:gen_no_owner_parents
        assign wire_owner_data={C_OWNER_WORD_BITS{1'b0}};
    end endgenerate
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin state_current<=C_PANEL_CONFIG ? ST_ROW_RESET : ST_IDLE;end
        else if(i_session_clear)begin state_current<=C_PANEL_CONFIG ? ST_ROW_RESET : ST_IDLE;end
        else begin state_current<=state_next;end
    end
    always @(*)begin
        state_next=state_current;
        case(state_current)
            ST_ROW_RESET:if(cnt_summary_row==C_ROWS-1)state_next=ST_IDLE;
            ST_IDLE:if(flag_roi_end && !wire_capture_fault)begin state_next=ST_SCAN_READ;end
            ST_SCAN_READ:state_next=ST_SCAN_LOAD;
            ST_SCAN_LOAD:state_next=ST_SCAN_CHECK;
            ST_SCAN_CHECK:state_next=flag_seed ? ST_POP_TEST : ST_SCAN_ADVANCE;
            ST_POP_TEST:state_next=cnt_queue == 0 ? ST_REGION_MEASURE : ST_POP_READ;
            ST_POP_READ:state_next=ST_POP_LOAD;
            ST_POP_LOAD:state_next=ST_NODE;
            ST_NODE:state_next=ST_NEIGHBOR_READ;
            ST_NEIGHBOR_READ:state_next=flag_neighbor_valid ? ST_NEIGHBOR_LOAD : ST_NEIGHBOR_ADVANCE;
            ST_NEIGHBOR_LOAD:state_next=ST_NEIGHBOR_CHECK;
            ST_NEIGHBOR_CHECK:state_next=flag_hole_target ? ST_HOLE_READ : flag_neighbor_match && flag_queue_full ? ST_DIAG_INIT : ST_NEIGHBOR_ADVANCE;
            ST_HOLE_READ:state_next=flag_hole_valid ? ST_HOLE_LOAD : ST_HOLE_COMMIT;
            ST_HOLE_LOAD:state_next=ST_HOLE_CHECK;
            ST_HOLE_CHECK:begin
                if(reg_hole_color==reg_region_color)state_next=cnt_hole_direction==7 ?
                    (C_PANEL_CONFIG && flag_hole_perimeter ? ST_PROBE_INIT : ST_HOLE_COMMIT) : ST_HOLE_READ;
                else state_next=flag_hole_white && cnt_hole_distance<wire_hole_distance_limit ? ST_HOLE_READ : ST_HOLE_COMMIT;
            end
            ST_HOLE_COMMIT:state_next=flag_hole_push && flag_queue_full ? ST_DIAG_INIT : ST_NEIGHBOR_ADVANCE;
            ST_PROBE_INIT:state_next=ST_PROBE_NODE_READ;
            ST_PROBE_NODE_READ:state_next=ST_PROBE_NODE_LOAD;
            ST_PROBE_NODE_LOAD:state_next=ST_PROBE_NEXT_READ;
            ST_PROBE_NEXT_READ:state_next=flag_probe_valid ? ST_PROBE_NEXT_LOAD : ST_HOLE_COMMIT;
            ST_PROBE_NEXT_LOAD:state_next=ST_PROBE_NEXT_CHECK;
            ST_PROBE_NEXT_CHECK:state_next=reg_probe_color==reg_region_color ? ST_PROBE_ADVANCE :
                flag_probe_extent ? ST_PROBE_LOOK_READ : ST_HOLE_COMMIT;
            ST_PROBE_LOOK_READ:state_next=ST_PROBE_LOOK_LOAD;
            ST_PROBE_LOOK_LOAD:state_next=ST_PROBE_LOOK_CHECK;
            ST_PROBE_LOOK_CHECK:state_next=wire_probe_data[C_PROBE_POSITION_BITS-1:0]==wire_probe_target ? ST_PROBE_ADVANCE :
                cnt_probe_lookup==cnt_probe_count-1'b1 ?
                    (cnt_probe_count==32 ? ST_HOLE_COMMIT : ST_PROBE_APPEND) : ST_PROBE_LOOK_READ;
            ST_PROBE_APPEND:state_next=ST_PROBE_ADVANCE;
            ST_PROBE_ADVANCE:state_next=cnt_probe_direction!=3 ? ST_PROBE_NEXT_READ :
                cnt_probe_head+1'b1<cnt_probe_count ? ST_PROBE_NODE_READ : ST_HOLE_COMMIT;
            ST_NEIGHBOR_ADVANCE:state_next=cnt_direction == 3 ? ST_POP_TEST : ST_NEIGHBOR_READ;
            ST_REGION_MEASURE:state_next=ST_REGION_SIZE;
            ST_REGION_SIZE:state_next=ST_REGION_AREA;
            ST_REGION_AREA:state_next=C_PANEL_CONFIG ?
                (reg_region_area>=wire_discovery_area && reg_width>=wire_discovery_size && reg_height>=wire_discovery_size && !flag_small_known_ng ? ST_SHAPE_INIT : ST_REGION_FILTER) :
                (flag_scan_shape && reg_region_area>=C_MIN_AREA &&
                 reg_width>=C_ROUND_MIN_SIZE && reg_width<=C_ROUND_MAX_SIZE &&
                 reg_height>=C_ROUND_MIN_SIZE && reg_height<=C_ROUND_MAX_SIZE ? ST_SHAPE_INIT : ST_REGION_FILTER);
            ST_SHAPE_INIT:state_next=ST_SHAPE_SQUARE;
            ST_SHAPE_SQUARE:if(cnt_square==1)begin state_next=ST_SHAPE_CHECK;end
            ST_SHAPE_CHECK:state_next=flag_contour_large ? ST_CONTOUR_INIT :
                C_PANEL_CONFIG && !flag_compact_reject ? ST_PROFILE_INIT : ST_REGION_FILTER;
            ST_CONTOUR_INIT:state_next=ST_CONTOUR_READ;
            ST_CONTOUR_READ:state_next=ST_CONTOUR_ADDRESS;
            ST_CONTOUR_ADDRESS:state_next=ST_CONTOUR_REQUEST;
            ST_CONTOUR_REQUEST:state_next=ST_CONTOUR_LOAD;
            ST_CONTOUR_LOAD:state_next=ST_CONTOUR_DELTA;
            ST_CONTOUR_DELTA:state_next=ST_CONTOUR_CAPTURE;
            ST_CONTOUR_CAPTURE:state_next=cnt_contour_point==8 ? ST_CONTOUR_COEFF : ST_CONTOUR_READ;
            ST_CONTOUR_COEFF:state_next=ST_CONTOUR_MULTIPLY;
            ST_CONTOUR_MULTIPLY:state_next=ST_CONTOUR_DIV_INIT;
            ST_CONTOUR_DIV_INIT:state_next=ST_CONTOUR_DIVIDE;
            ST_CONTOUR_DIVIDE:if(cnt_fit_divide==1)state_next=ST_CONTOUR_ERROR;
            ST_CONTOUR_ERROR:state_next=ST_CONTOUR_NEXT_POINT;
            ST_CONTOUR_NEXT_POINT:state_next=cnt_contour_point==8 ? ST_CONTOUR_NEXT_MODEL : ST_CONTOUR_COEFF;
            ST_CONTOUR_NEXT_MODEL:state_next=cnt_contour_knot==7 && flag_contour_side ? ST_CONTOUR_FINISH : ST_CONTOUR_COEFF;
            ST_CONTOUR_FINISH:state_next=!flag_compact_reject ? ST_PROFILE_INIT : ST_REGION_FILTER;
            ST_PROFILE_INIT:state_next=ST_PROFILE_READ;
            ST_PROFILE_READ:state_next=ST_PROFILE_LOAD;
            ST_PROFILE_LOAD:state_next=ST_PROFILE_ADVANCE;
            ST_PROFILE_ADVANCE:state_next=cnt_profile==(flag_profile_large ? 8 : 4) ? ST_PROFILE_CHECK : ST_PROFILE_READ;
            ST_PROFILE_CHECK:if(cnt_profile==4)state_next=ST_REGION_FILTER;
            ST_REGION_FILTER:state_next=C_PANEL_CONFIG ? (flag_owner_lookup ? ST_OWNER_READ : ST_ROW_CLEAR) : ST_REGION_EMIT;
            ST_OWNER_READ:state_next=ST_OWNER_CHECK;
            ST_OWNER_CHECK:state_next=flag_owner_match || {1'b0,cnt_owner_lookup}+3'd1>=cnt_owner_parents ? ST_ROW_CLEAR : ST_OWNER_READ;
            ST_ROW_CLEAR:if(cnt_summary_row==reg_max_row)state_next=ST_REGION_EMIT;
            ST_REGION_EMIT:state_next=flag_candidate_overflow ? ST_DIAG_INIT : ST_SCAN_ADVANCE;
            ST_SCAN_ADVANCE:state_next=cnt_scan_address == C_CELLS-1 ? ST_DIAG_INIT : ST_SCAN_READ;
            ST_DIAG_INIT:state_next=C_PANEL_CONFIG && flag_overflow_o && !flag_summary_cleaned ? ST_ROW_ABORT :
                reg_diag_box_area == 0 ? ST_DONE : ST_DIAG_DIVIDE;
            ST_ROW_ABORT:if(cnt_summary_row==C_ROWS-1)state_next=ST_DIAG_INIT;
            ST_DIAG_DIVIDE:if(reg_fill_remaining < {1'b0,reg_diag_box_area})begin state_next=ST_DONE;end
            ST_DONE:state_next=ST_IDLE;
            default:state_next=ST_IDLE;
        endcase
        if(flag_hole_work_expired)state_next=ST_HOLE_COMMIT;
    end
    // 所有候选与诊断只属于一个冻结epoch；超限在done处使整帧失效。
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            flag_scan_bank<=0;cnt_scan_address<=0;cnt_scan_column<=0;cnt_scan_row<=0;
            cnt_owner_parents<=0;cnt_owner_lookup<=0;reg_owner_colors<=0;reg_owner_last_bottom<=0;reg_owner_filled_area<=0;flag_owner_suppressed<=0;
            reg_owner_core_left<=0;reg_owner_core_right<=0;reg_owner_core_top<=0;reg_owner_core_bottom<=0;
            reg_node_address<=0;reg_neighbor_address<=0;reg_node_column<=0;reg_node_row<=0;reg_neighbor_column<=0;reg_neighbor_row<=0;
            reg_min_column<=0;reg_max_column<=0;reg_min_row<=0;reg_max_row<=0;
            reg_cell<=0;reg_neighbor_cell<=0;reg_region_color<=0;reg_region_area<=0;cnt_direction<=0;
            cnt_head<=0;cnt_tail<=0;cnt_queue<=0;cnt_candidates<=0;
            reg_left<=0;reg_right<=0;reg_top<=0;reg_bottom<=0;reg_width<=0;reg_height<=0;
            reg_box_area<=0;reg_diag_box_area<=0;reg_reject<=0;
            reg_start_o<=0;reg_valid_o<=0;reg_done_o<=0;flag_overflow_o<=0;flag_fault_o<=0;flag_error_o<=0;
            reg_color_o<=0;reg_shape_o<=0;reg_shape_reject_o<=0;reg_area_o<=0;reg_gate_o<=0;reg_epoch_o<=0;
            flag_gate_occupied_o<=0;
            flag_scan_shape<=0;flag_shape_reject<=0;cnt_region_cells<=0;cnt_perimeter<=0;
            reg_square<=0;cnt_square<=0;
            cnt_summary_row<=0;reg_node_area<=0;cnt_profile<=0;
            reg_profile_top<=0;reg_profile_quarter_top<=0;reg_profile_middle<=0;reg_profile_quarter_bottom<=0;reg_profile_bottom<=0;
            reg_profile_support<=0;reg_profile_box_width<=0;flag_profile_small<=0;flag_profile_reject<=0;flag_summary_cleaned<=0;
            flag_profile_large<=0;flag_profile_center_bad<=0;flag_profile_center_loss<=0;reg_profile_arc_bad<=0;
            reg_outer_low<=0;reg_outer_high<=0;reg_quarter_low<=0;reg_quarter_high<=0;
            for(profile_index=0;profile_index<5;profile_index=profile_index+1)reg_profile_width[profile_index]<=0;
            cnt_hole_direction<=0;cnt_hole_distance<=1;reg_hole_color<=0;flag_hole_white<=0;flag_hole_accept<=0;
            flag_hole_perimeter<=0;cnt_red_probes<=0;
            cnt_probe_count<=0;cnt_probe_head<=0;cnt_probe_lookup<=0;cnt_probe_direction<=0;
            reg_probe_column<=0;reg_probe_row<=0;reg_probe_address<=0;reg_probe_color<=0;cnt_hole_work<=0;
            cnt_contour_point<=0;cnt_contour_knot<=1;flag_contour_side<=0;flag_contour_valid<=0;flag_contour_rectangle<=0;
            reg_contour_circle_error<=0;reg_contour_error<=0;reg_contour_best_left<=0;reg_contour_best_right<=0;
            reg_contour_span<=0;reg_contour_offset<=0;reg_contour_address<=0;reg_contour_reference<=0;
            reg_circle_observed<=0;reg_circle_expected<=0;reg_circle_delta<=0;
            reg_fit_start<=0;reg_fit_end<=0;reg_fit_point<=0;reg_fit_first_row<=0;reg_fit_last_row<=0;reg_fit_point_row<=0;
            reg_fit_denominator<=0;flag_fit_negative<=0;reg_fit_numerator<=0;reg_fit_dividend<=0;reg_fit_quotient<=0;
            reg_fit_observed<=0;reg_fit_remainder<=0;cnt_fit_divide<=0;
            reg_left_o<=0;reg_right_o<=0;reg_top_o<=0;reg_bottom_o<=0;
            reg_diag_width_o<=0;reg_diag_height_o<=0;reg_diag_area_o<=0;reg_diag_fill_o<=0;
            reg_diag_reject_o<=0;reg_fill_remaining<=0;
        end else if(i_session_clear)begin
            flag_scan_bank<=0;cnt_scan_address<=0;cnt_scan_column<=0;cnt_scan_row<=0;
            cnt_owner_parents<=0;cnt_owner_lookup<=0;reg_owner_colors<=0;reg_owner_last_bottom<=0;reg_owner_filled_area<=0;flag_owner_suppressed<=0;
            reg_owner_core_left<=0;reg_owner_core_right<=0;reg_owner_core_top<=0;reg_owner_core_bottom<=0;
            reg_node_address<=0;reg_neighbor_address<=0;reg_node_column<=0;reg_node_row<=0;reg_neighbor_column<=0;reg_neighbor_row<=0;
            reg_min_column<=0;reg_max_column<=0;reg_min_row<=0;reg_max_row<=0;
            reg_cell<=0;reg_neighbor_cell<=0;reg_region_color<=0;reg_region_area<=0;cnt_direction<=0;
            cnt_head<=0;cnt_tail<=0;cnt_queue<=0;cnt_candidates<=0;
            reg_left<=0;reg_right<=0;reg_top<=0;reg_bottom<=0;reg_width<=0;reg_height<=0;
            reg_box_area<=0;reg_diag_box_area<=0;reg_reject<=0;
            reg_start_o<=0;reg_valid_o<=0;reg_done_o<=0;flag_overflow_o<=0;flag_fault_o<=0;flag_error_o<=0;
            reg_color_o<=0;reg_shape_o<=0;reg_shape_reject_o<=0;reg_area_o<=0;reg_gate_o<=0;reg_epoch_o<=0;
            flag_gate_occupied_o<=0;
            flag_scan_shape<=0;flag_shape_reject<=0;cnt_region_cells<=0;cnt_perimeter<=0;
            reg_square<=0;cnt_square<=0;
            cnt_summary_row<=0;reg_node_area<=0;cnt_profile<=0;
            reg_profile_top<=0;reg_profile_quarter_top<=0;reg_profile_middle<=0;reg_profile_quarter_bottom<=0;reg_profile_bottom<=0;
            reg_profile_support<=0;reg_profile_box_width<=0;flag_profile_small<=0;flag_profile_reject<=0;flag_summary_cleaned<=0;
            flag_profile_large<=0;flag_profile_center_bad<=0;flag_profile_center_loss<=0;reg_profile_arc_bad<=0;
            reg_outer_low<=0;reg_outer_high<=0;reg_quarter_low<=0;reg_quarter_high<=0;
            for(profile_index=0;profile_index<5;profile_index=profile_index+1)reg_profile_width[profile_index]<=0;
            cnt_hole_direction<=0;cnt_hole_distance<=1;reg_hole_color<=0;flag_hole_white<=0;flag_hole_accept<=0;
            flag_hole_perimeter<=0;cnt_red_probes<=0;
            cnt_probe_count<=0;cnt_probe_head<=0;cnt_probe_lookup<=0;cnt_probe_direction<=0;
            reg_probe_column<=0;reg_probe_row<=0;reg_probe_address<=0;reg_probe_color<=0;cnt_hole_work<=0;
            cnt_contour_point<=0;cnt_contour_knot<=1;flag_contour_side<=0;flag_contour_valid<=0;flag_contour_rectangle<=0;
            reg_contour_circle_error<=0;reg_contour_error<=0;reg_contour_best_left<=0;reg_contour_best_right<=0;
            reg_contour_span<=0;reg_contour_offset<=0;reg_contour_address<=0;reg_contour_reference<=0;
            reg_circle_observed<=0;reg_circle_expected<=0;reg_circle_delta<=0;
            reg_fit_start<=0;reg_fit_end<=0;reg_fit_point<=0;reg_fit_first_row<=0;reg_fit_last_row<=0;reg_fit_point_row<=0;
            reg_fit_denominator<=0;flag_fit_negative<=0;reg_fit_numerator<=0;reg_fit_dividend<=0;reg_fit_quotient<=0;
            reg_fit_observed<=0;reg_fit_remainder<=0;cnt_fit_divide<=0;
            reg_left_o<=0;reg_right_o<=0;reg_top_o<=0;reg_bottom_o<=0;
            reg_diag_width_o<=0;reg_diag_height_o<=0;reg_diag_area_o<=0;reg_diag_fill_o<=0;
            reg_diag_reject_o<=0;reg_fill_remaining<=0;
        end else begin
            reg_start_o<=0;reg_valid_o<=0;reg_done_o<=0;flag_fault_o<=0;
            if(C_PANEL_CONFIG && flag_hole_work_state && cnt_hole_work<19'd262143)cnt_hole_work<=cnt_hole_work+1'b1;
            if((i_valid && i_sof && flag_conflict && !wire_capture_fault) || (flag_roi_end && flag_busy && !wire_capture_fault))begin
                flag_fault_o<=1;flag_error_o<=1;
            end
                                                                                              
            if((state_current==ST_PROFILE_LOAD && cnt_profile==2 && !flag_profile_large) ||
               (state_current==ST_PROFILE_ADVANCE && cnt_profile==8 && flag_profile_large))begin
                reg_outer_low<=wire_profile_reference*8;
                reg_outer_high<=wire_profile_reference*13+8;
                reg_quarter_low<=wire_profile_reference*12;
                reg_quarter_high<=wire_profile_reference*15+(flag_profile_small ? 16 : 0);
            end
            case(state_current)
                ST_ROW_RESET:begin
                    if(cnt_summary_row==C_ROWS-1)cnt_summary_row<=0;
                    else cnt_summary_row<=cnt_summary_row+1'b1;
                end
                ST_ROW_ABORT:begin
                    if(cnt_summary_row==C_ROWS-1)begin cnt_summary_row<=0;flag_summary_cleaned<=1;end
                    else cnt_summary_row<=cnt_summary_row+1'b1;
                end
                ST_IDLE:if(flag_roi_end && !wire_capture_fault)begin
                    cnt_hole_work<=0;
                    cnt_owner_parents<=0;cnt_owner_lookup<=0;reg_owner_colors<=0;reg_owner_last_bottom<=0;reg_owner_filled_area<=0;flag_owner_suppressed<=0;
                    flag_scan_bank<=reg_capture_bank;reg_epoch_o<=reg_capture_epoch;reg_gate_o<=cnt_gate;
                    flag_scan_shape<=C_PANEL_CONFIG ? 1'b1 : flag_capture_shape;
                    cnt_scan_address<=0;cnt_scan_column<=0;cnt_scan_row<=0;cnt_candidates<=0;cnt_red_probes<=0;
                    flag_summary_cleaned<=0;
                    cnt_head<=0;cnt_tail<=0;cnt_queue<=0;flag_overflow_o<=0;reg_start_o<=1;
                    reg_diag_width_o<=0;reg_diag_height_o<=0;reg_diag_area_o<=0;reg_diag_fill_o<=0;
                    reg_diag_reject_o<=0;reg_diag_box_area<=0;
                    flag_gate_occupied_o<=0;
                end
                ST_SCAN_LOAD:reg_cell<=wire_scan_cell;
                ST_SCAN_CHECK:begin
                    if(C_PANEL_CONFIG && cnt_scan_row>reg_owner_last_bottom)begin
                        cnt_owner_parents<=0;reg_owner_colors<=0;reg_owner_last_bottom<=0;
                    end
                    if(flag_seed)begin
                        if(C_PANEL_CONFIG)cnt_red_probes<=0;
                        reg_owner_filled_area<=0;
                        reg_owner_core_left<=0;reg_owner_core_right<=0;reg_owner_core_top<=0;reg_owner_core_bottom<=0;
                        flag_owner_suppressed<=0;
                        reg_region_color<=reg_cell[6:5];reg_region_area<=0;
                        cnt_region_cells<=0;cnt_perimeter<=0;flag_shape_reject<=0;
                        flag_profile_reject<=0;
                        flag_contour_rectangle<=0;flag_contour_valid<=0;
                        reg_min_column<=cnt_scan_column;reg_max_column<=cnt_scan_column;
                        reg_min_row<=cnt_scan_row;reg_max_row<=cnt_scan_row;
                        cnt_head<=0;cnt_tail<=1;cnt_queue<=1;
                    end
                end
                ST_POP_LOAD:begin
                    reg_node_column<=wire_queue_data[C_COLUMN_BITS-1:0];
                    reg_node_row<=wire_queue_data[C_COLUMN_BITS +:C_ROW_BITS];
                    reg_region_area<=reg_region_area+wire_queue_data[C_COLUMN_BITS+C_ROW_BITS +:5];
                    reg_node_area<=wire_queue_data[C_COLUMN_BITS+C_ROW_BITS +:5];
                    cnt_head<=cnt_head+1'b1;cnt_queue<=cnt_queue-1'b1;
                end
                ST_NODE:begin
                    cnt_region_cells<=cnt_region_cells+1'b1;
                    reg_node_address<=reg_node_row*C_COLUMNS+reg_node_column;cnt_direction<=0;
                    if(reg_node_column < reg_min_column)begin reg_min_column<=reg_node_column;end
                    if(reg_node_column > reg_max_column)begin reg_max_column<=reg_node_column;end
                    if(reg_node_row < reg_min_row)begin reg_min_row<=reg_node_row;end
                    if(reg_node_row > reg_max_row)begin reg_max_row<=reg_node_row;end
                end
                ST_NEIGHBOR_LOAD:begin
                    reg_neighbor_cell<=wire_scan_cell;
                    reg_neighbor_column<=dec_neighbor_column;reg_neighbor_row<=dec_neighbor_row;
                    reg_neighbor_address<=dec_neighbor_address;
                end
                ST_NEIGHBOR_READ:if(!flag_neighbor_valid)begin cnt_perimeter<=cnt_perimeter+1'b1;end
                ST_NEIGHBOR_CHECK:begin
                    // 入队已保存面积；网格面积置零标记已访问，颜色保留用于外边/孔洞统计。
                    if(reg_neighbor_cell[6:5]!=reg_region_color && !flag_hole_target)begin cnt_perimeter<=cnt_perimeter+1'b1;end
                    if(flag_hole_target)begin
                        cnt_hole_direction<=0;cnt_hole_distance<=1;flag_hole_accept<=1;
                        flag_hole_perimeter<=flag_red_hole_target;
                        if(flag_red_hole_target)cnt_red_probes<=cnt_red_probes+1'b1;
                    end
                    if(flag_neighbor_match)begin
                        if(flag_queue_full)begin flag_overflow_o<=1;end
                        else begin cnt_tail<=cnt_tail+1'b1;cnt_queue<=cnt_queue+1'b1;end
                    end
                end
                ST_HOLE_READ:if(!flag_hole_valid)flag_hole_accept<=0;
                ST_HOLE_LOAD:begin
                    reg_hole_color<=wire_scan_cell[6:5];
                    flag_hole_white<=wire_scan_code==6'h0e || wire_scan_code==6'h0f ||
                        (flag_hole_perimeter && wire_scan_cell[6:5]!=reg_region_color);
                end
                ST_HOLE_CHECK:begin
                    if(reg_hole_color==reg_region_color)begin cnt_hole_direction<=cnt_hole_direction+1'b1;cnt_hole_distance<=1;end
                    else if(flag_hole_white && cnt_hole_distance<wire_hole_distance_limit)cnt_hole_distance<=cnt_hole_distance+1'b1;
                    else flag_hole_accept<=0;
                end
                ST_HOLE_COMMIT:begin
                    if(flag_hole_push)begin
                        if(flag_queue_full)flag_overflow_o<=1;
                        else begin
                            cnt_tail<=cnt_tail+1'b1;cnt_queue<=cnt_queue+1'b1;
                            if(C_PANEL_CONFIG)reg_owner_filled_area<=reg_owner_filled_area+20'd16;
                        end
                    end else if(!flag_hole_accept)cnt_perimeter<=cnt_perimeter+1'b1;
                end
                ST_PROBE_INIT:begin cnt_probe_count<=1;cnt_probe_head<=0;cnt_probe_lookup<=0;end
                ST_PROBE_NODE_LOAD:begin
                    reg_probe_column<=wire_probe_data[C_COLUMN_BITS-1:0];
                    reg_probe_row<=wire_probe_data[C_COLUMN_BITS +:C_ROW_BITS];cnt_probe_direction<=0;
                    reg_probe_address<=wire_probe_data[C_PROBE_POSITION_BITS +:C_ADDRESS_BITS];
                end
                ST_PROBE_NEXT_READ:if(!flag_probe_valid)flag_hole_accept<=0;
                ST_PROBE_NEXT_LOAD:reg_probe_color<=wire_scan_cell[6:5];
                ST_PROBE_NEXT_CHECK:begin
                    cnt_probe_lookup<=0;
                    if(reg_probe_color!=reg_region_color && !flag_probe_extent)flag_hole_accept<=0;
                end
                ST_PROBE_LOOK_CHECK:if(wire_probe_data[C_PROBE_POSITION_BITS-1:0]!=wire_probe_target)begin
                    if(cnt_probe_lookup==cnt_probe_count-1'b1)begin
                        if(cnt_probe_count==32)flag_hole_accept<=0;
                    end else cnt_probe_lookup<=cnt_probe_lookup+1'b1;
                end
                ST_PROBE_APPEND:cnt_probe_count<=cnt_probe_count+1'b1;
                ST_PROBE_ADVANCE:begin
                    if(cnt_probe_direction==3)cnt_probe_head<=cnt_probe_head+1'b1;
                    else cnt_probe_direction<=cnt_probe_direction+1'b1;
                end
                ST_NEIGHBOR_ADVANCE:cnt_direction<=cnt_direction+1'b1;
                ST_REGION_MEASURE:begin
                    reg_left<=wire_left < wire_roi_left ? wire_roi_left : wire_left[11:0];
                    reg_right<=wire_right > wire_roi_last_x ? wire_roi_last_x : wire_right[11:0];
                    reg_top<=wire_top < wire_roi_top ? wire_roi_top : wire_top[11:0];
                    reg_bottom<=wire_bottom > wire_roi_last_y ? wire_roi_last_y : wire_bottom[11:0];
                end
                ST_REGION_SIZE:begin reg_width<=reg_right-reg_left+1'b1;reg_height<=reg_bottom-reg_top+1'b1;end
                ST_REGION_AREA:begin
                    reg_box_area<=reg_width*reg_height;
                    if(flag_small_known_ng)flag_shape_reject<=1;
                end
                ST_SHAPE_INIT:begin
                    reg_square<=cnt_perimeter*cnt_perimeter;cnt_square<=C_PANEL_CONFIG ? 1 : 19;
                end
                ST_SHAPE_SQUARE:begin
                    cnt_square<=cnt_square-1'b1;
                end
                ST_SHAPE_CHECK:begin flag_shape_reject<=flag_compact_reject;end
                ST_CONTOUR_INIT:begin
                    cnt_contour_point<=0;cnt_contour_knot<=1;flag_contour_side<=0;
                    flag_contour_valid<=1;flag_contour_rectangle<=0;
                    reg_contour_circle_error<=0;reg_contour_error<=0;
                    reg_contour_best_left<={C_CONTOUR_ERROR_BITS{1'b1}};reg_contour_best_right<={C_CONTOUR_ERROR_BITS{1'b1}};
                    reg_contour_span<=wire_region_row_span;reg_contour_reference<=wire_contour_width;
                end
                ST_CONTOUR_READ:reg_contour_offset<=dec_contour_offset>>4;
                ST_CONTOUR_ADDRESS:reg_contour_address<=reg_min_row+reg_contour_offset;
                ST_CONTOUR_LOAD:begin
                    reg_circle_observed<=wire_contour_circle_observed;reg_circle_expected<=wire_contour_circle_expected;
                end
                ST_CONTOUR_DELTA:reg_circle_delta<=wire_contour_circle_delta;
                ST_CONTOUR_CAPTURE:begin
                    reg_contour_left[cnt_contour_point]<=wire_summary_left;
                    reg_contour_right[cnt_contour_point]<=wire_summary_right;
                    reg_contour_row[cnt_contour_point]<=wire_contour_row;
                                                                                                      
                    if(cnt_contour_point==2)begin
                        reg_owner_core_left<=wire_summary_left;reg_owner_core_right<=wire_summary_right;
                        reg_owner_core_top<=wire_contour_row;
                    end
                    if(cnt_contour_point==6)begin
                        if(wire_summary_left>reg_owner_core_left)reg_owner_core_left<=wire_summary_left;
                        if(wire_summary_right<reg_owner_core_right)reg_owner_core_right<=wire_summary_right;
                        reg_owner_core_bottom<=wire_contour_row;
                    end
                    if(!flag_summary_supported)flag_contour_valid<=0;
                    reg_contour_circle_error<=reg_contour_circle_error+reg_circle_delta;
                    if(cnt_contour_point==8)cnt_contour_point<=0;
                    else cnt_contour_point<=cnt_contour_point+1'b1;
                end
                ST_CONTOUR_COEFF:begin
                    reg_fit_start<=flag_contour_side ? reg_contour_right[wire_fit_first_index] : reg_contour_left[wire_fit_first_index];
                    reg_fit_end<=flag_contour_side ? reg_contour_right[wire_fit_last_index] : reg_contour_left[wire_fit_last_index];
                    reg_fit_point<=flag_contour_side ? reg_contour_right[cnt_contour_point] : reg_contour_left[cnt_contour_point];
                    reg_fit_first_row<=reg_contour_row[wire_fit_first_index];
                    reg_fit_last_row<=reg_contour_row[wire_fit_last_index];
                    reg_fit_point_row<=reg_contour_row[cnt_contour_point];
                end
                ST_CONTOUR_MULTIPLY:begin
                    flag_fit_negative<=reg_fit_end<reg_fit_start;
                    reg_fit_numerator<={wire_fit_product,8'd0};
                    reg_fit_observed<={wire_fit_observed_delta,8'd0};
                    if(reg_fit_last_row==reg_fit_first_row)begin reg_fit_denominator<=1;flag_contour_valid<=0;end
                    else reg_fit_denominator<=wire_fit_row_extent;
                end
                ST_CONTOUR_DIV_INIT:begin
                    reg_fit_dividend<=reg_fit_numerator;reg_fit_quotient<=0;reg_fit_remainder<=0;cnt_fit_divide<=C_FIT_NUM_BITS;
                end
                ST_CONTOUR_DIVIDE:begin
                    reg_fit_dividend<=reg_fit_dividend<<1;cnt_fit_divide<=cnt_fit_divide-1'b1;
                    if(wire_fit_trial>={1'b0,reg_fit_denominator})begin
                        reg_fit_remainder<=wire_fit_trial-{1'b0,reg_fit_denominator};
                        reg_fit_quotient<={reg_fit_quotient[C_FIT_NUM_BITS-2:0],1'b1};
                    end else begin reg_fit_remainder<=wire_fit_trial;reg_fit_quotient<={reg_fit_quotient[C_FIT_NUM_BITS-2:0],1'b0};end
                end
                ST_CONTOUR_ERROR:begin
                    reg_contour_error<=reg_contour_error+wire_fit_absolute;
                    if(wire_fit_absolute>{C_CONTOUR_ERROR_BITS{1'b1}})flag_contour_valid<=0;
                end
                ST_CONTOUR_NEXT_POINT:if(cnt_contour_point!=8)cnt_contour_point<=cnt_contour_point+1'b1;
                ST_CONTOUR_NEXT_MODEL:begin
                    if(flag_contour_side)begin
                        if(reg_contour_error<reg_contour_best_right)reg_contour_best_right<=reg_contour_error;
                    end else if(reg_contour_error<reg_contour_best_left)reg_contour_best_left<=reg_contour_error;
                    reg_contour_error<=0;cnt_contour_point<=0;
                    if(cnt_contour_knot==7)begin cnt_contour_knot<=1;flag_contour_side<=1;end
                    else cnt_contour_knot<=cnt_contour_knot+1'b1;
                end
                ST_CONTOUR_FINISH:begin
                                                                                   
                                                                                           
                    flag_contour_rectangle<=flag_contour_valid &&
                        wire_contour_line_error+C_CONTOUR_MARGIN<{1'b0,reg_contour_circle_error} &&
                        wire_contour_line_error<=wire_contour_line_limit;
                end
                ST_PROFILE_INIT:begin
                    cnt_profile<=0;reg_profile_support<=0;
                    flag_profile_large<=flag_large_shape;flag_profile_center_bad<=0;flag_profile_center_loss<=0;reg_profile_arc_bad<=0;
                    reg_profile_top<=reg_min_row+(wire_region_row_span>>3);
                    reg_profile_quarter_top<=reg_min_row+(wire_region_row_span>>2);
                    reg_profile_middle<=reg_min_row+(wire_region_row_span>>1);
                    reg_profile_quarter_bottom<=reg_max_row-(wire_region_row_span>>2);
                    reg_profile_bottom<=reg_max_row-(wire_region_row_span>>3);
                    reg_profile_box_width<={1'b0,reg_max_column}-{1'b0,reg_min_column}+1'b1;
                    flag_profile_small<=wire_region_row_span<12 || reg_max_column-reg_min_column<12;
                end
                ST_PROFILE_LOAD:begin
                    if(cnt_profile<5)begin
                        reg_profile_width[cnt_profile]<=flag_summary_valid ? wire_summary_width : 0;
                        reg_profile_support[cnt_profile]<=flag_summary_supported;
                        if(flag_profile_large && cnt_profile==2 && !flag_summary_supported)reg_profile_width[2]<=0;
                    end else if(flag_summary_supported)begin
                        reg_profile_support[2]<=1;
                        if(wire_summary_width>reg_profile_width[2])reg_profile_width[2]<=wire_summary_width;
                    end
                end
                ST_PROFILE_ADVANCE:cnt_profile<=cnt_profile==(flag_profile_large ? 8 : 4) ? 0 : cnt_profile+1'b1;
                ST_PROFILE_CHECK:begin
                    if(flag_profile_large)begin
                        case(cnt_profile)
                            0:reg_profile_arc_bad[0]<=flag_profile_outer_bad;
                            1:if(flag_profile_quarter_bad)reg_profile_arc_bad[0]<=1;
                            2:begin
                                flag_profile_center_bad<=!reg_profile_support[2] || reg_profile_width[2]+2'd2<reg_profile_box_width ||
                                    (reg_profile_width[2]+1'b1<reg_profile_box_width &&
                                     {reg_profile_width[2],4'd0}<({reg_profile_box_width,4'd0}-reg_profile_box_width));
                                flag_profile_center_loss<=reg_profile_width[2]+1'b1<reg_profile_box_width;
                            end
                            3:reg_profile_arc_bad[1]<=flag_profile_quarter_bad;
                            4:flag_profile_reject<=flag_profile_center_bad ||
                                (flag_profile_center_loss ?
                                 (reg_profile_arc_bad[0] || reg_profile_arc_bad[1] || flag_profile_outer_bad) :
                                 (reg_profile_arc_bad[0] && (reg_profile_arc_bad[1] || flag_profile_outer_bad)));
                            default:begin end
                        endcase
                    end else begin
                        if(!reg_profile_support[cnt_profile])flag_profile_reject<=1;
                        if(cnt_profile==2)begin
                            if(reg_profile_width[2]+1'b1<reg_profile_box_width)flag_profile_reject<=1;
                        end else if(cnt_profile==0 || cnt_profile==4)begin
                            if(flag_profile_outer_bad)flag_profile_reject<=1;
                        end else if(flag_profile_quarter_bad)flag_profile_reject<=1;
                    end
                    if(cnt_profile!=4)cnt_profile<=cnt_profile+1'b1;
                end
                ST_REGION_FILTER:begin
                    if(C_PANEL_CONFIG)cnt_summary_row<=reg_min_row;
                    // 较大连通区域即使尺寸/形状不合格仍保持占用；孤立小片不累计成球。
                    if(!C_PANEL_CONFIG && reg_region_area >= C_MIN_AREA && reg_left < C_GATE_END && reg_right >= C_GATE_MIN)begin
                        flag_gate_occupied_o<=1;
                    end
                    cnt_owner_lookup<=0;
                    if(flag_owner_parent)begin
                        cnt_owner_parents<=cnt_owner_parents+1'b1;
                        reg_owner_colors<=reg_owner_colors | wire_owner_color_mask;
                        if(reg_owner_core_bottom>reg_owner_last_bottom)reg_owner_last_bottom<=reg_owner_core_bottom;
                    end
                    reg_reject[0]<=C_PANEL_CONFIG ? reg_region_area < wire_discovery_area : reg_region_area < C_MIN_AREA;
                    reg_reject[1]<=C_PANEL_CONFIG ?
                        (reg_width<wire_discovery_size || reg_width>C_X_END-C_X_MIN || reg_height<wire_discovery_size || reg_height>C_Y_END-C_Y_MIN) :
                        (reg_width < C_MIN_SIZE || reg_width > C_MAX_SIZE || reg_height < C_MIN_SIZE || reg_height > C_MAX_SIZE ||
                        (flag_scan_shape && (reg_width<C_ROUND_MIN_SIZE || reg_width>C_ROUND_MAX_SIZE || reg_height<C_ROUND_MIN_SIZE || reg_height>C_ROUND_MAX_SIZE)));
                    reg_reject[2]<=C_PANEL_CONFIG ? 1'b0 : flag_scan_shape ?
                        (({1'b0,reg_width}<<1)>({1'b0,reg_height}<<1)+reg_height || ({1'b0,reg_height}<<1)>({1'b0,reg_width}<<1)+reg_width) :
                        (reg_width > ({1'b0,reg_height} << 1) || reg_height > ({1'b0,reg_width} << 1));
                    reg_reject[3]<=C_PANEL_CONFIG ? (i_settings[9:8]!=0 && reg_region_color!=i_settings[9:8]) :
                        ({6'd0,reg_region_area} << 2) < reg_box_area || (flag_scan_shape && flag_shape_reject);
                end
                ST_OWNER_CHECK:begin
                    if(flag_owner_match)flag_owner_suppressed<=1;
                    else cnt_owner_lookup<=cnt_owner_lookup+1'b1;
                end
                ST_ROW_CLEAR:if(cnt_summary_row!=reg_max_row)cnt_summary_row<=cnt_summary_row+1'b1;
                ST_REGION_EMIT:begin
                    if(C_PANEL_CONFIG && flag_region_selected && !flag_owner_suppressed &&
                       reg_region_area>=C_MIN_AREA && reg_left<C_GATE_END && reg_right>=C_GATE_MIN)begin
                        flag_gate_occupied_o<=1;
                    end
                    if((!C_PANEL_CONFIG || (flag_region_selected && !flag_owner_suppressed)) && reg_region_area > reg_diag_area_o)begin
                        reg_diag_width_o<=reg_width;reg_diag_height_o<=reg_height;reg_diag_area_o<=reg_region_area;
                        reg_diag_reject_o<=reg_reject;reg_diag_box_area<=reg_box_area;
                    end
                    if(reg_reject == 0 && (!C_PANEL_CONFIG || !flag_owner_suppressed))begin
                        if(flag_candidate_overflow)begin flag_overflow_o<=1;end
                        else begin
                            if(!C_PANEL_CONFIG || cnt_candidates<9)cnt_candidates<=cnt_candidates+1'b1;
                            reg_valid_o<=1;
                            reg_color_o<=reg_region_color;reg_area_o<=reg_region_area;
                            reg_shape_o[0]<=flag_region_round;
                            reg_shape_o[1]<=flag_region_rectangle;
                            reg_shape_reject_o[0]<=flag_shape_reject;
                            reg_shape_reject_o[1]<=C_PANEL_CONFIG && (flag_profile_reject || (flag_contour_large && flag_contour_rectangle));
                            reg_shape_reject_o[2]<=({1'b0,reg_width}<<1)>({1'b0,reg_height}<<1)+reg_height ||
                                ({1'b0,reg_height}<<1)>({1'b0,reg_width}<<1)+reg_width;
                            reg_shape_reject_o[3]<=({6'd0,reg_region_area}<<2)<reg_box_area;
                            reg_left_o<=reg_left;reg_right_o<=reg_right;reg_top_o<=reg_top;reg_bottom_o<=reg_bottom;
                        end
                    end
                end
                ST_SCAN_ADVANCE:begin
                    cnt_scan_address<=cnt_scan_address+1'b1;
                    if(cnt_scan_column == C_COLUMNS-1)begin cnt_scan_column<=0;cnt_scan_row<=cnt_scan_row+1'b1;end
                    else begin cnt_scan_column<=cnt_scan_column+1'b1;end
                end
                ST_DIAG_INIT:begin
                    reg_fill_remaining<=reg_diag_area_o*100;reg_diag_fill_o<=0;
                    if(C_PANEL_CONFIG && flag_overflow_o && !flag_summary_cleaned)cnt_summary_row<=0;
                end
                ST_DIAG_DIVIDE:if(reg_fill_remaining >= {1'b0,reg_diag_box_area})begin
                    reg_fill_remaining<=reg_fill_remaining-{1'b0,reg_diag_box_area};reg_diag_fill_o<=reg_diag_fill_o+1'b1;
                end
                ST_DONE:reg_done_o<=1;
                default:begin end
            endcase
            if(flag_hole_work_expired)flag_hole_accept<=0;
        end
    end
                                                                                               
    assign o_reject_valid=state_current==ST_REGION_EMIT &&
        (C_PANEL_CONFIG ? reg_region_color!=0 && flag_region_selected && !flag_owner_suppressed && (|reg_reject) : (|reg_reject[3:1])) && !i_session_clear;
    assign o_frame_start=reg_start_o;
    assign o_candidate_valid=reg_valid_o;
    assign o_color=reg_color_o;
    assign o_shape_flags=reg_shape_o;
    assign o_shape_reject=reg_shape_reject_o;
    assign o_area=reg_area_o;
    assign o_x_min=reg_left_o;
    assign o_x_max=reg_right_o;
    assign o_y_min=reg_top_o;
    assign o_y_max=reg_bottom_o;
    assign o_frame_done=reg_done_o;
    assign o_gate_pixels=reg_gate_o;
    assign o_gate_occupied=flag_gate_occupied_o;
    assign o_epoch=reg_epoch_o;
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
