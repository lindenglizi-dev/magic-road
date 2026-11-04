`timescale 1ns / 1ps
// 四lane、双帧列RAM；帧末顺序扫描输出最多八个独立颜色候选。
module ball_projection #(
    parameter C_WIDTH = 1280,
    parameter C_HEIGHT = 720,
    parameter C_MIN_AREA = 128,
    parameter C_MIN_SIZE = 12,
    parameter C_MAX_SIZE = 384,
    parameter C_MIN_COLUMN = 2,
    parameter C_GAP_MERGE = 2,
    parameter C_MAX_CANDIDATES = 8,
    parameter C_ADDR_BITS = $clog2(C_WIDTH/4)
)(
    input i_clk,
    input i_rstn,
    input i_valid,
    input i_sof,
    input i_eof,
    input [11:0] i_x,
    input [11:0] i_y,
    input [7:0] i_labels,
    input [2:0] i_gate_hits,
    input [15:0] i_epoch,
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
    output [15:0] o_epoch,
    output o_overflow,
    output o_fault,
    output o_error
);
    localparam ST_IDLE=0, ST_READ=1, ST_LOAD=2, ST_ACC=3, ST_MEASURE=4,
               ST_FILTER=5, ST_EMIT=6, ST_ADVANCE=7, ST_DONE=8;
    reg [3:0] state_current, state_next;
    reg flag_capture_bank, flag_scan_bank;
    reg flag_write, flag_write_bank, flag_write_first, flag_write_last, flag_write_drop;
    reg flag_drop_frame;
    reg [C_ADDR_BITS-1:0] reg_write_address;
    reg [9:0] reg_write_y;
    reg [7:0] reg_write_labels;
    reg [15:0] reg_write_epoch;
    reg [19:0] cnt_gate, reg_complete_gate;
    reg [11:0] cnt_scan_x;
    reg [49:0] reg_column;
    reg flag_segment;
    reg [11:0] reg_left, reg_right, reg_top, reg_bottom;
    reg [19:0] cnt_red, cnt_yellow, cnt_green;
    reg [11:0] cnt_gap;
    reg [3:0] cnt_candidates;
    reg [12:0] reg_width, reg_height;
    reg [21:0] reg_area;
    reg [19:0] reg_dominant;
    reg [1:0] reg_winner;
    reg [25:0] reg_box_area;
    reg flag_good;
    reg reg_start_o, reg_valid_o, reg_done_o, flag_overflow_o, flag_fault_o, flag_error_o;
    reg [1:0] reg_color_o;
    reg [19:0] reg_area_o, reg_gate_o;
    reg [11:0] reg_left_o, reg_right_o, reg_top_o, reg_bottom_o;
    reg [15:0] reg_epoch_o;
    wire flag_busy = state_current != ST_IDLE;
    wire flag_conflict = flag_busy && flag_capture_bank == flag_scan_bank;
    wire flag_drop_now = i_sof ? flag_conflict : flag_drop_frame;
    wire flag_capture_read = i_valid && !flag_drop_now;
    wire flag_scan_read = state_current == ST_READ;
    wire [C_ADDR_BITS-1:0] wire_capture_address = i_x >> 2;
    wire [C_ADDR_BITS-1:0] wire_scan_address = cnt_scan_x >> 2;
    wire [399:0] wire_ram_data;
    wire [21:0] wire_column_area = {12'd0,reg_column[49:40]}+
                                  {12'd0,reg_column[39:30]}+{12'd0,reg_column[29:20]};
    wire flag_column_active = wire_column_area >= C_MIN_COLUMN;
    wire flag_close_segment = flag_segment && !flag_column_active && cnt_gap == C_GAP_MERGE;
    wire flag_last_column = cnt_scan_x == C_WIDTH-1;
    genvar bank, lane;
    generate
        for(bank=0; bank<2; bank=bank+1)begin:gen_frame_bank
            for(lane=0; lane<4; lane=lane+1)begin:gen_pixel_lane
                wire flag_read_capture = flag_capture_read && flag_capture_bank == bank;
                wire flag_read_scan = flag_scan_read && flag_scan_bank == bank;
                wire [49:0] wire_previous = wire_ram_data[(bank*4+lane)*50 +: 50];
                wire [1:0] wire_color = reg_write_labels[lane*2 +: 2];
                wire [9:0] wire_red = flag_write_first ? 10'd0 : wire_previous[49:40];
                wire [9:0] wire_yellow = flag_write_first ? 10'd0 : wire_previous[39:30];
                wire [9:0] wire_green = flag_write_first ? 10'd0 : wire_previous[29:20];
                wire [9:0] wire_top = flag_write_first ? 10'd1023 : wire_previous[19:10];
                wire [9:0] wire_bottom = flag_write_first ? 10'd0 : wire_previous[9:0];
                wire [9:0] wire_new_top = wire_color != 0 && reg_write_y < wire_top ? reg_write_y : wire_top;
                wire [9:0] wire_new_bottom = wire_color != 0 && reg_write_y > wire_bottom ? reg_write_y : wire_bottom;
                wire [9:0] wire_new_red = wire_red+(wire_color == 1);
                wire [9:0] wire_new_yellow = wire_yellow+(wire_color == 2);
                wire [9:0] wire_new_green = wire_green+(wire_color == 3);
                ball_column_store #(.C_DEPTH(C_WIDTH/4),.C_ADDR_BITS(C_ADDR_BITS)) column_Inst(
                    .i_clk(i_clk),
                    .i_read_enable(flag_read_capture || flag_read_scan),
                    .i_read_address(flag_read_capture ? wire_capture_address : wire_scan_address),
                    .i_write_enable(flag_write && !flag_write_drop && flag_write_bank == bank),
                    .i_write_address(reg_write_address),
                    .i_write_data({wire_new_red,wire_new_yellow,wire_new_green,wire_new_top,wire_new_bottom}),
                    .o_read_data(wire_ram_data[(bank*4+lane)*50 +: 50])
                );
            end
        end
    endgenerate

    // 采集读改写相隔一拍；有效空拍不会改变列地址或重用旧标签。
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            flag_capture_bank<=0; flag_write<=0; flag_write_bank<=0;
            flag_write_first<=0; flag_write_last<=0; flag_write_drop<=0; flag_drop_frame<=0;
            reg_write_address<=0; reg_write_y<=0; reg_write_labels<=0; reg_write_epoch<=0;
            cnt_gate<=0; reg_complete_gate<=0;
        end else begin
            flag_write<=i_valid;
            flag_write_last<=i_valid && i_eof;
            if(i_valid)begin
                flag_write_bank<=flag_capture_bank;
                flag_write_first<=i_y == 0;
                flag_write_drop<=flag_drop_now;
                reg_write_address<=wire_capture_address;
                reg_write_y<=i_y[9:0]; reg_write_labels<=i_labels; reg_write_epoch<=i_epoch;
                if(i_sof)begin flag_drop_frame<=flag_conflict; end
                cnt_gate <= (i_sof ? 20'd0 : cnt_gate)+i_gate_hits;
                if(i_eof)begin
                    reg_complete_gate <= (i_sof ? 20'd0 : cnt_gate)+i_gate_hits;
                    flag_capture_bank <= !flag_capture_bank;
                end
            end
        end
    end

    // 扫描FSM采用独立状态寄存、组合转移和数据任务三个过程。
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin state_current<=ST_IDLE; end
        else begin state_current<=state_next; end
    end
    always @(*)begin
        state_next=state_current;
        case(state_current)
            ST_IDLE:begin
                if(flag_write_last && !flag_write_drop)begin state_next=ST_READ; end
            end
            ST_READ:begin state_next=ST_LOAD; end
            ST_LOAD:begin state_next=ST_ACC; end
            ST_ACC:begin
                if(flag_close_segment || (flag_last_column && (flag_segment || flag_column_active)))begin
                    state_next=ST_MEASURE;
                end else begin state_next=ST_ADVANCE; end
            end
            ST_MEASURE:begin state_next=ST_FILTER; end
            ST_FILTER:begin state_next=ST_EMIT; end
            ST_EMIT:begin state_next=ST_ADVANCE; end
            ST_ADVANCE:begin
                if(flag_last_column)begin state_next=ST_DONE; end
                else begin state_next=ST_READ; end
            end
            ST_DONE:begin state_next=ST_IDLE; end
            default:begin state_next=ST_IDLE; end
        endcase
    end

    // 每次完成帧均有start/done，即使无候选也提供可靠的空门确认。
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            flag_scan_bank<=0; cnt_scan_x<=0; reg_column<=0; flag_segment<=0;
            reg_left<=0; reg_right<=0; reg_top<=0; reg_bottom<=0;
            cnt_red<=0; cnt_yellow<=0; cnt_green<=0; cnt_gap<=0; cnt_candidates<=0;
            reg_width<=0; reg_height<=0; reg_area<=0; reg_dominant<=0;
            reg_winner<=0; reg_box_area<=0; flag_good<=0;
            reg_start_o<=0; reg_valid_o<=0; reg_done_o<=0;
            flag_overflow_o<=0; flag_fault_o<=0; flag_error_o<=0;
            reg_color_o<=0; reg_area_o<=0; reg_gate_o<=0; reg_epoch_o<=0;
            reg_left_o<=0; reg_right_o<=0; reg_top_o<=0; reg_bottom_o<=0;
        end else begin
            reg_start_o<=0; reg_valid_o<=0; reg_done_o<=0; flag_fault_o<=0;
            if(flag_write_last && (flag_busy || flag_write_drop))begin
                flag_fault_o<=1; flag_error_o<=1;
            end
            case(state_current)
                ST_IDLE:begin
                    if(flag_write_last && !flag_write_drop)begin
                        flag_scan_bank<=flag_write_bank; reg_epoch_o<=reg_write_epoch;
                        reg_gate_o<=reg_complete_gate; cnt_scan_x<=0; cnt_candidates<=0;
                        flag_segment<=0; flag_overflow_o<=0; reg_start_o<=1; cnt_gap<=0;
                    end
                end
                ST_LOAD:begin
                    reg_column<=wire_ram_data[(flag_scan_bank*4+cnt_scan_x[1:0])*50 +: 50];
                end
                ST_ACC:begin
                    if(flag_column_active)begin
                        cnt_gap<=0; reg_right<=cnt_scan_x;
                        if(!flag_segment)begin
                            flag_segment<=1; reg_left<=cnt_scan_x;
                            reg_top<={2'd0,reg_column[19:10]}; reg_bottom<={2'd0,reg_column[9:0]};
                            cnt_red<=reg_column[49:40]; cnt_yellow<=reg_column[39:30]; cnt_green<=reg_column[29:20];
                        end else begin
                            if(reg_column[19:10] < reg_top)begin reg_top<=reg_column[19:10]; end
                            if(reg_column[9:0] > reg_bottom)begin reg_bottom<=reg_column[9:0]; end
                            cnt_red<=cnt_red+reg_column[49:40];
                            cnt_yellow<=cnt_yellow+reg_column[39:30];
                            cnt_green<=cnt_green+reg_column[29:20];
                        end
                    end else if(flag_segment)begin cnt_gap<=cnt_gap+1'b1; end
                end
                ST_MEASURE:begin
                    reg_width<={1'b0,reg_right}-{1'b0,reg_left}+1'b1;
                    reg_height<={1'b0,reg_bottom}-{1'b0,reg_top}+1'b1;
                    reg_area<={2'd0,cnt_red}+{2'd0,cnt_yellow}+{2'd0,cnt_green};
                    if(cnt_red >= cnt_yellow && cnt_red >= cnt_green)begin
                        reg_winner<=1; reg_dominant<=cnt_red;
                    end else if(cnt_yellow >= cnt_green)begin
                        reg_winner<=2; reg_dominant<=cnt_yellow;
                    end else begin reg_winner<=3; reg_dominant<=cnt_green; end
                    flag_segment<=0;
                end
                ST_FILTER:begin
                    reg_box_area<=reg_width*reg_height;
                    flag_good <= reg_area >= C_MIN_AREA &&
                        reg_width >= C_MIN_SIZE && reg_width <= C_MAX_SIZE &&
                        reg_height >= C_MIN_SIZE && reg_height <= C_MAX_SIZE &&
                        reg_width <= (reg_height << 1) && reg_height <= (reg_width << 1) &&
                        ({2'd0,reg_dominant} << 2) >= (reg_area*3);
                end
                ST_EMIT:begin
                    if(flag_good && ({4'd0,reg_area} << 2) >= reg_box_area)begin
                        if(cnt_candidates < C_MAX_CANDIDATES)begin
                            reg_valid_o<=1; cnt_candidates<=cnt_candidates+1'b1;
                            reg_color_o<=reg_winner; reg_area_o<=reg_area[19:0];
                            reg_left_o<=reg_left; reg_right_o<=reg_right;
                            reg_top_o<=reg_top; reg_bottom_o<=reg_bottom;
                        end else begin flag_overflow_o<=1; end
                    end
                end
                ST_ADVANCE:begin cnt_scan_x<=cnt_scan_x+1'b1; end
                ST_DONE:begin reg_done_o<=1; end
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
    assign o_epoch=reg_epoch_o;
    assign o_overflow=flag_overflow_o;
    assign o_fault=flag_fault_o;
    assign o_error=flag_error_o;
endmodule
