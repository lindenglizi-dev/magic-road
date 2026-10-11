module top4_selector #(
    parameter X_WIDTH     = 8,
    parameter Y_WIDTH     = 8,
    parameter LABEL_WIDTH = 6,
    parameter AREA_WIDTH  = 16,
    parameter MAX_LABEL   = 32,
    parameter MIN_AREA    = 4
)(
    input  wire                     clk,
    input  wire                     rst_n,
    input  wire                     frame_clear,
    input  wire                     start,
    input  wire [LABEL_WIDTH:0]     label_limit,

    output reg                      feature_rd_req,
    output reg  [LABEL_WIDTH-1:0]   feature_rd_label,
    input  wire                     feature_rd_valid,
    input  wire                     feature_valid,
    input  wire [AREA_WIDTH-1:0]    feature_area,
    input  wire [X_WIDTH-1:0]       feature_xmin,
    input  wire [X_WIDTH-1:0]       feature_xmax,
    input  wire [Y_WIDTH-1:0]       feature_ymin,
    input  wire [Y_WIDTH-1:0]       feature_ymax,

    output reg                      obj_valid,
    output reg  [1:0]               obj_index,
    output reg  [LABEL_WIDTH-1:0]   obj_label,
    output reg  [X_WIDTH-1:0]       obj_xmin,
    output reg  [X_WIDTH-1:0]       obj_xmax,
    output reg  [Y_WIDTH-1:0]       obj_ymin,
    output reg  [Y_WIDTH-1:0]       obj_ymax,
    output reg  [X_WIDTH-1:0]       obj_center_x,
    output reg  [Y_WIDTH-1:0]       obj_center_y,
    output reg  [AREA_WIDTH-1:0]    obj_area,
    output reg  [2:0]               object_count,
    output reg                      object_frame_done,

    output reg                      busy,
    output reg  [31:0]              select_cycle_count,
    output reg  [31:0]              select_cycle_max,
    output reg                      selector_error,
    output reg                      protocol_error
);

    localparam S_IDLE      = 3'd0;
    localparam S_READ_REQ  = 3'd1;
    localparam S_READ_WAIT = 3'd2;
    localparam S_EMIT      = 3'd3;
    localparam S_DONE      = 3'd4;

    reg [2:0] state;
    reg [LABEL_WIDTH-1:0] scan_label;
    reg [LABEL_WIDTH:0]   label_limit_latched;
    reg [1:0]             emit_index;

    reg                    top_valid [0:3];
    reg [LABEL_WIDTH-1:0]  top_label [0:3];
    reg [AREA_WIDTH-1:0]   top_area  [0:3];
    reg [X_WIDTH-1:0]      top_xmin  [0:3];
    reg [X_WIDTH-1:0]      top_xmax  [0:3];
    reg [Y_WIDTH-1:0]      top_ymin  [0:3];
    reg [Y_WIDTH-1:0]      top_ymax  [0:3];

    integer i;

    wire last_label;
    assign last_label = ({1'b0, scan_label} + 1'b1) >=
                        label_limit_latched;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state               <= S_IDLE;
            scan_label          <= {{(LABEL_WIDTH-1){1'b0}}, 1'b1};
            label_limit_latched <= {{LABEL_WIDTH{1'b0}}, 1'b1};
            emit_index          <= 2'd0;
            feature_rd_req      <= 1'b0;
            feature_rd_label    <= {LABEL_WIDTH{1'b0}};
            obj_valid           <= 1'b0;
            obj_index           <= 2'd0;
            obj_label           <= {LABEL_WIDTH{1'b0}};
            obj_xmin            <= {X_WIDTH{1'b0}};
            obj_xmax            <= {X_WIDTH{1'b0}};
            obj_ymin            <= {Y_WIDTH{1'b0}};
            obj_ymax            <= {Y_WIDTH{1'b0}};
            obj_center_x        <= {X_WIDTH{1'b0}};
            obj_center_y        <= {Y_WIDTH{1'b0}};
            obj_area            <= {AREA_WIDTH{1'b0}};
            object_count        <= 3'd0;
            object_frame_done   <= 1'b0;
            busy                <= 1'b0;
            select_cycle_count  <= 32'd0;
            select_cycle_max    <= 32'd0;
            selector_error      <= 1'b0;
            protocol_error      <= 1'b0;
            for (i = 0; i < 4; i = i + 1) begin
                top_valid[i] <= 1'b0;
                top_label[i] <= {LABEL_WIDTH{1'b0}};
                top_area[i]  <= {AREA_WIDTH{1'b0}};
                top_xmin[i]  <= {X_WIDTH{1'b0}};
                top_xmax[i]  <= {X_WIDTH{1'b0}};
                top_ymin[i]  <= {Y_WIDTH{1'b0}};
                top_ymax[i]  <= {Y_WIDTH{1'b0}};
            end
        end else if (frame_clear) begin
            state              <= S_IDLE;
            feature_rd_req     <= 1'b0;
            obj_valid          <= 1'b0;
            object_frame_done  <= 1'b0;
            object_count       <= 3'd0;
            busy               <= 1'b0;
            select_cycle_count <= 32'd0;
            select_cycle_max   <= 32'd0;
            selector_error     <= 1'b0;
            protocol_error     <= 1'b0;
            for (i = 0; i < 4; i = i + 1)
                top_valid[i] <= 1'b0;
        end else begin
            feature_rd_req    <= 1'b0;
            obj_valid         <= 1'b0;
            object_frame_done <= 1'b0;

            if (busy)
                select_cycle_count <= select_cycle_count + 1'b1;

            if ((state != S_IDLE) && start)
                protocol_error <= 1'b1;

            case (state)
                S_IDLE: begin
                    busy <= 1'b0;
                    if (start) begin
                        if ((label_limit < 1) ||
                            (label_limit > (MAX_LABEL + 1))) begin
                            selector_error    <= 1'b1;
                            object_frame_done <= 1'b1;
                        end else begin
                            busy                <= 1'b1;
                            select_cycle_count  <= 32'd0;
                            label_limit_latched <= label_limit;
                            scan_label          <= {{(LABEL_WIDTH-1){1'b0}}, 1'b1};
                            emit_index          <= 2'd0;
                            object_count        <= 3'd0;
                            for (i = 0; i < 4; i = i + 1)
                                top_valid[i] <= 1'b0;

                            if (label_limit == 1)
                                state <= S_EMIT;
                            else
                                state <= S_READ_REQ;
                        end
                    end
                end

                S_READ_REQ: begin
                    feature_rd_req   <= 1'b1;
                    feature_rd_label <= scan_label;
                    state            <= S_READ_WAIT;
                end

                S_READ_WAIT: begin
                    if (feature_rd_valid) begin
                        if (feature_valid && (feature_area >= MIN_AREA)) begin
                            if (object_count < 4)
                                object_count <= object_count + 1'b1;

                            if (!top_valid[0] || (feature_area > top_area[0])) begin
                                top_valid[3] <= top_valid[2];
                                top_label[3] <= top_label[2];
                                top_area[3]  <= top_area[2];
                                top_xmin[3]  <= top_xmin[2];
                                top_xmax[3]  <= top_xmax[2];
                                top_ymin[3]  <= top_ymin[2];
                                top_ymax[3]  <= top_ymax[2];
                                top_valid[2] <= top_valid[1];
                                top_label[2] <= top_label[1];
                                top_area[2]  <= top_area[1];
                                top_xmin[2]  <= top_xmin[1];
                                top_xmax[2]  <= top_xmax[1];
                                top_ymin[2]  <= top_ymin[1];
                                top_ymax[2]  <= top_ymax[1];
                                top_valid[1] <= top_valid[0];
                                top_label[1] <= top_label[0];
                                top_area[1]  <= top_area[0];
                                top_xmin[1]  <= top_xmin[0];
                                top_xmax[1]  <= top_xmax[0];
                                top_ymin[1]  <= top_ymin[0];
                                top_ymax[1]  <= top_ymax[0];
                                top_valid[0] <= 1'b1;
                                top_label[0] <= scan_label;
                                top_area[0]  <= feature_area;
                                top_xmin[0]  <= feature_xmin;
                                top_xmax[0]  <= feature_xmax;
                                top_ymin[0]  <= feature_ymin;
                                top_ymax[0]  <= feature_ymax;
                            end else if (!top_valid[1] ||
                                         (feature_area > top_area[1])) begin
                                top_valid[3] <= top_valid[2];
                                top_label[3] <= top_label[2];
                                top_area[3]  <= top_area[2];
                                top_xmin[3]  <= top_xmin[2];
                                top_xmax[3]  <= top_xmax[2];
                                top_ymin[3]  <= top_ymin[2];
                                top_ymax[3]  <= top_ymax[2];
                                top_valid[2] <= top_valid[1];
                                top_label[2] <= top_label[1];
                                top_area[2]  <= top_area[1];
                                top_xmin[2]  <= top_xmin[1];
                                top_xmax[2]  <= top_xmax[1];
                                top_ymin[2]  <= top_ymin[1];
                                top_ymax[2]  <= top_ymax[1];
                                top_valid[1] <= 1'b1;
                                top_label[1] <= scan_label;
                                top_area[1]  <= feature_area;
                                top_xmin[1]  <= feature_xmin;
                                top_xmax[1]  <= feature_xmax;
                                top_ymin[1]  <= feature_ymin;
                                top_ymax[1]  <= feature_ymax;
                            end else if (!top_valid[2] ||
                                         (feature_area > top_area[2])) begin
                                top_valid[3] <= top_valid[2];
                                top_label[3] <= top_label[2];
                                top_area[3]  <= top_area[2];
                                top_xmin[3]  <= top_xmin[2];
                                top_xmax[3]  <= top_xmax[2];
                                top_ymin[3]  <= top_ymin[2];
                                top_ymax[3]  <= top_ymax[2];
                                top_valid[2] <= 1'b1;
                                top_label[2] <= scan_label;
                                top_area[2]  <= feature_area;
                                top_xmin[2]  <= feature_xmin;
                                top_xmax[2]  <= feature_xmax;
                                top_ymin[2]  <= feature_ymin;
                                top_ymax[2]  <= feature_ymax;
                            end else if (!top_valid[3] ||
                                         (feature_area > top_area[3])) begin
                                top_valid[3] <= 1'b1;
                                top_label[3] <= scan_label;
                                top_area[3]  <= feature_area;
                                top_xmin[3]  <= feature_xmin;
                                top_xmax[3]  <= feature_xmax;
                                top_ymin[3]  <= feature_ymin;
                                top_ymax[3]  <= feature_ymax;
                            end
                        end

                        if (last_label) begin
                            emit_index <= 2'd0;
                            state      <= S_EMIT;
                        end else begin
                            scan_label <= scan_label + 1'b1;
                            state      <= S_READ_REQ;
                        end
                    end
                end

                S_EMIT: begin
                    obj_index <= emit_index;
                    if (top_valid[emit_index]) begin
                        obj_valid    <= 1'b1;
                        obj_label    <= top_label[emit_index];
                        obj_xmin     <= top_xmin[emit_index];
                        obj_xmax     <= top_xmax[emit_index];
                        obj_ymin     <= top_ymin[emit_index];
                        obj_ymax     <= top_ymax[emit_index];
                        obj_center_x <= ({1'b0, top_xmin[emit_index]} +
                                         {1'b0, top_xmax[emit_index]}) >> 1;
                        obj_center_y <= ({1'b0, top_ymin[emit_index]} +
                                         {1'b0, top_ymax[emit_index]}) >> 1;
                        obj_area     <= top_area[emit_index];
                    end

                    if (emit_index == 2'd3)
                        state <= S_DONE;
                    else
                        emit_index <= emit_index + 1'b1;
                end

                S_DONE: begin
                    busy              <= 1'b0;
                    object_frame_done <= 1'b1;
                    if (select_cycle_count > select_cycle_max)
                        select_cycle_max <= select_cycle_count;
                    state <= S_IDLE;
                end

                default: begin
                    state          <= S_IDLE;
                    busy           <= 1'b0;
                    selector_error <= 1'b1;
                end
            endcase
        end
    end

endmodule
