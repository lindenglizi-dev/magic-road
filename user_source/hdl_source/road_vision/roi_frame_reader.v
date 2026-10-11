// Read each valid CCL box from the grayscale frame buffer and normalize it to
// a 32x32 nearest-neighbour ROI stream. Coordinate generation uses fixed-point
// DDA accumulators, avoiding runtime division and multipliers.
module roi_frame_reader #(
    parameter FRAME_WIDTH = 256,
    parameter FRAME_HEIGHT = 144,
    parameter ROI_SIZE = 32,
    parameter ADDR_WIDTH = 16
)(
    input  wire                  clk,
    input  wire                  rst_n,
    input  wire                  frame_ready,
    input  wire [31:0]           frame_id,
    input  wire                  boxes_update,
    input  wire [31:0]           boxes_frame_id,
    input  wire [2:0]            object_count,
    input  wire [159:0]          boxes,
    output reg                   release_frame,
    output reg                   rd_req_valid,
    output reg [ADDR_WIDTH-1:0]  rd_req_addr,
    input  wire                  rd_rsp_valid,
    input  wire [7:0]            rd_rsp_gray,
    output reg                   roi_valid,
    output reg [1:0]             roi_object_index,
    output reg [4:0]             roi_x,
    output reg [4:0]             roi_y,
    output reg [7:0]             roi_gray,
    output reg                   busy,
    output reg                   frame_done,
    output reg [31:0]            completed_frame_id,
    output reg [7:0]             roi_checksum,
    output reg                   pair_miss,
    output reg                   protocol_error
);
    localparam ST_IDLE  = 3'd0;
    localparam ST_FIND  = 3'd1;
    localparam ST_SCAN  = 3'd2;
    localparam ST_DRAIN = 3'd3;
    localparam ROI_PIXELS = ROI_SIZE * ROI_SIZE;

    function [39:0] pick_box;
        input [159:0] box_table;
        input [1:0] box_sel;
        begin
            case (box_sel)
                2'd0: pick_box = box_table[39:0];
                2'd1: pick_box = box_table[79:40];
                2'd2: pick_box = box_table[119:80];
                default: pick_box = box_table[159:120];
            endcase
        end
    endfunction

    reg [2:0] state;
    reg frame_pending, boxes_pending;
    reg [31:0] pending_frame_id, pending_boxes_id;
    reg [2:0] pending_object_count;
    reg [159:0] pending_boxes;
    reg [2:0] object_cursor;
    wire [39:0] current_box = pick_box(pending_boxes,
                                      object_cursor[1:0]);
    wire current_valid = current_box[39];
    wire [7:0] current_xmin = current_box[36:29];
    wire [7:0] current_xmax = current_box[28:21];
    wire [7:0] current_ymin = current_box[20:13];
    wire [7:0] current_ymax = current_box[12:5];

    reg [7:0] bbox_xmin, bbox_xmax, bbox_ymin, bbox_ymax;
    reg [16:0] x_step, y_step, x_start, y_acc, x_acc;
    reg [4:0] sample_x, sample_y;
    reg [10:0] issue_count, response_count;
    wire [8:0] current_width = {1'b0, current_xmax} -
                               {1'b0, current_xmin} + 1'b1;
    wire [8:0] current_height = {1'b0, current_ymax} -
                                {1'b0, current_ymin} + 1'b1;
    wire [8:0] x_offset = x_acc[16:8];
    wire [8:0] y_offset = y_acc[16:8];
    wire [8:0] source_x_sum = {1'b0, bbox_xmin} + x_offset;
    wire [8:0] source_y_sum = {1'b0, bbox_ymin} + y_offset;
    wire [7:0] source_x = (source_x_sum > {1'b0, bbox_xmax}) ?
                           bbox_xmax : source_x_sum[7:0];
    wire [7:0] source_y = (source_y_sum > {1'b0, bbox_ymax}) ?
                           bbox_ymax : source_y_sum[7:0];

    reg [1:0] req_object_index, rsp_object_index;
    reg [4:0] req_roi_x, req_roi_y, rsp_roi_x, rsp_roi_y;
    reg rsp_meta_valid;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state <= ST_IDLE;
            frame_pending <= 1'b0;
            boxes_pending <= 1'b0;
            pending_frame_id <= 0;
            pending_boxes_id <= 0;
            pending_object_count <= 0;
            pending_boxes <= 0;
            object_cursor <= 0;
            bbox_xmin <= 0; bbox_xmax <= 0;
            bbox_ymin <= 0; bbox_ymax <= 0;
            x_step <= 0; y_step <= 0; x_start <= 0;
            x_acc <= 0; y_acc <= 0;
            sample_x <= 0; sample_y <= 0;
            issue_count <= 0; response_count <= 0;
            release_frame <= 1'b0;
            rd_req_valid <= 1'b0;
            rd_req_addr <= 0;
            roi_valid <= 1'b0;
            roi_object_index <= 0; roi_x <= 0; roi_y <= 0;
            roi_gray <= 0;
            busy <= 1'b0;
            frame_done <= 1'b0;
            completed_frame_id <= 0;
            roi_checksum <= 0;
            pair_miss <= 1'b0;
            protocol_error <= 1'b0;
            req_object_index <= 0; rsp_object_index <= 0;
            req_roi_x <= 0; req_roi_y <= 0;
            rsp_roi_x <= 0; rsp_roi_y <= 0;
            rsp_meta_valid <= 1'b0;
        end else begin
            release_frame <= 1'b0;
            rd_req_valid <= 1'b0;
            roi_valid <= 1'b0;
            frame_done <= 1'b0;
            pair_miss <= 1'b0;

            rsp_meta_valid <= rd_req_valid;
            if (rd_req_valid) begin
                rsp_object_index <= req_object_index;
                rsp_roi_x <= req_roi_x;
                rsp_roi_y <= req_roi_y;
            end

            if (frame_ready) begin
                if (frame_pending || busy)
                    protocol_error <= 1'b1;
                else begin
                    frame_pending <= 1'b1;
                    pending_frame_id <= frame_id;
                end
            end
            if (boxes_update) begin
                if (boxes_pending || busy)
                    protocol_error <= 1'b1;
                boxes_pending <= 1'b1;
                pending_boxes_id <= boxes_frame_id;
                pending_object_count <= object_count;
                pending_boxes <= boxes;
            end

            if (rd_rsp_valid) begin
                if (!busy || !rsp_meta_valid) begin
                    protocol_error <= 1'b1;
                end else begin
                    roi_valid <= 1'b1;
                    roi_object_index <= rsp_object_index;
                    roi_x <= rsp_roi_x;
                    roi_y <= rsp_roi_y;
                    roi_gray <= rd_rsp_gray;
                    roi_checksum <= roi_checksum ^ rd_rsp_gray;
                    response_count <= response_count + 1'b1;
                    if (response_count == ROI_PIXELS-1) begin
                        object_cursor <= object_cursor + 1'b1;
                        state <= ST_FIND;
                    end
                end
            end

            case (state)
                ST_IDLE: begin
                    busy <= 1'b0;
                    if (frame_pending && boxes_pending) begin
                        if (pending_frame_id == pending_boxes_id) begin
                            frame_pending <= 1'b0;
                            boxes_pending <= 1'b0;
                            completed_frame_id <= pending_frame_id;
                            roi_checksum <= 8'd0;
                            object_cursor <= 3'd0;
                            busy <= 1'b1;
                            state <= ST_FIND;
                        end else begin
                            pair_miss <= 1'b1;
                            if (pending_frame_id < pending_boxes_id) begin
                                release_frame <= 1'b1;
                                frame_pending <= 1'b0;
                            end else begin
                                boxes_pending <= 1'b0;
                            end
                        end
                    end
                end

                ST_FIND: begin
                    if ((object_cursor >= 4) ||
                        (pending_object_count == 0)) begin
                        release_frame <= 1'b1;
                        frame_done <= 1'b1;
                        busy <= 1'b0;
                        state <= ST_IDLE;
                    end else if (!current_valid ||
                                 (current_xmax < current_xmin) ||
                                 (current_ymax < current_ymin)) begin
                        if (current_valid)
                            protocol_error <= 1'b1;
                        object_cursor <= object_cursor + 1'b1;
                    end else begin
                        bbox_xmin <= current_xmin;
                        bbox_xmax <= current_xmax;
                        bbox_ymin <= current_ymin;
                        bbox_ymax <= current_ymax;
                        x_step <= current_width << 3;
                        y_step <= current_height << 3;
                        x_start <= current_width << 2;
                        x_acc <= current_width << 2;
                        y_acc <= current_height << 2;
                        sample_x <= 0;
                        sample_y <= 0;
                        issue_count <= 0;
                        response_count <= 0;
                        state <= ST_SCAN;
                    end
                end

                ST_SCAN: begin
                    rd_req_valid <= 1'b1;
                    rd_req_addr <= {source_y, source_x};
                    req_object_index <= object_cursor[1:0];
                    req_roi_x <= sample_x;
                    req_roi_y <= sample_y;
                    issue_count <= issue_count + 1'b1;
                    if (sample_x == ROI_SIZE-1) begin
                        sample_x <= 0;
                        x_acc <= x_start;
                        sample_y <= sample_y + 1'b1;
                        y_acc <= y_acc + y_step;
                    end else begin
                        sample_x <= sample_x + 1'b1;
                        x_acc <= x_acc + x_step;
                    end
                    if (issue_count == ROI_PIXELS-1)
                        state <= ST_DRAIN;
                end

                ST_DRAIN: begin
                    // Responses are counted above. The last response moves
                    // the FSM back to ST_FIND.
                end

                default: begin
                    protocol_error <= 1'b1;
                    state <= ST_IDLE;
                end
            endcase
        end
    end
endmodule
