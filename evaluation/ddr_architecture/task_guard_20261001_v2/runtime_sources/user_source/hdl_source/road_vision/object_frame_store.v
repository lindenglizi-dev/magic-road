module object_frame_store #(
    parameter X_WIDTH     = 8,
    parameter Y_WIDTH     = 8,
    parameter LABEL_WIDTH = 6,
    parameter AREA_WIDTH  = 16
)(
    input  wire                    clk,
    input  wire                    rst_n,
    input  wire                    frame_clear,

    input  wire                    in_obj_valid,
    input  wire [1:0]              in_obj_index,
    input  wire [LABEL_WIDTH-1:0]  in_obj_label,
    input  wire [X_WIDTH-1:0]      in_obj_xmin,
    input  wire [X_WIDTH-1:0]      in_obj_xmax,
    input  wire [Y_WIDTH-1:0]      in_obj_ymin,
    input  wire [Y_WIDTH-1:0]      in_obj_ymax,
    input  wire [X_WIDTH-1:0]      in_obj_center_x,
    input  wire [Y_WIDTH-1:0]      in_obj_center_y,
    input  wire [AREA_WIDTH-1:0]   in_obj_area,
    input  wire [X_WIDTH:0]        in_obj_width,
    input  wire [Y_WIDTH:0]        in_obj_height,
    input  wire [1:0]              in_obj_fill_level,
    input  wire [1:0]              in_obj_class,
    input  wire [2:0]              in_object_count,
    input  wire                    in_object_frame_done,
    input  wire                    discard_frame,

    input  wire [1:0]              rd_index,
    output reg                     rd_valid,
    output reg  [LABEL_WIDTH-1:0]  rd_label,
    output reg  [X_WIDTH-1:0]      rd_xmin,
    output reg  [X_WIDTH-1:0]      rd_xmax,
    output reg  [Y_WIDTH-1:0]      rd_ymin,
    output reg  [Y_WIDTH-1:0]      rd_ymax,
    output reg  [X_WIDTH-1:0]      rd_center_x,
    output reg  [Y_WIDTH-1:0]      rd_center_y,
    output reg  [AREA_WIDTH-1:0]   rd_area,
    output reg  [X_WIDTH:0]        rd_width,
    output reg  [Y_WIDTH:0]        rd_height,
    output reg  [1:0]              rd_fill_level,
    output reg  [1:0]              rd_class,
    input  wire [1:0]              track_rd_index,
    output wire                    track_obj_valid,
    output wire [X_WIDTH-1:0]      track_obj_xmin,
    output wire [X_WIDTH-1:0]      track_obj_xmax,
    output wire [Y_WIDTH-1:0]      track_obj_ymin,
    output wire [Y_WIDTH-1:0]      track_obj_ymax,
    output wire [X_WIDTH-1:0]      track_obj_center_x,
    output wire [Y_WIDTH-1:0]      track_obj_center_y,
    output wire [1:0]              track_obj_class,
    output reg  [2:0]              stored_object_count,
    output reg  [31:0]             frame_sequence,
    output reg                     object_table_commit,
    output reg                     protocol_error
);

    reg stage_valid [0:3];
    reg [LABEL_WIDTH-1:0] stage_label [0:3];
    reg [X_WIDTH-1:0] stage_xmin [0:3];
    reg [X_WIDTH-1:0] stage_xmax [0:3];
    reg [Y_WIDTH-1:0] stage_ymin [0:3];
    reg [Y_WIDTH-1:0] stage_ymax [0:3];
    reg [X_WIDTH-1:0] stage_center_x [0:3];
    reg [Y_WIDTH-1:0] stage_center_y [0:3];
    reg [AREA_WIDTH-1:0] stage_area [0:3];
    reg [X_WIDTH:0] stage_width [0:3];
    reg [Y_WIDTH:0] stage_height [0:3];
    reg [1:0] stage_fill_level [0:3];
    reg [1:0] stage_class [0:3];

    reg front_valid [0:3];
    reg [LABEL_WIDTH-1:0] front_label [0:3];
    reg [X_WIDTH-1:0] front_xmin [0:3];
    reg [X_WIDTH-1:0] front_xmax [0:3];
    reg [Y_WIDTH-1:0] front_ymin [0:3];
    reg [Y_WIDTH-1:0] front_ymax [0:3];
    reg [X_WIDTH-1:0] front_center_x [0:3];
    reg [Y_WIDTH-1:0] front_center_y [0:3];
    reg [AREA_WIDTH-1:0] front_area [0:3];
    reg [X_WIDTH:0] front_width [0:3];
    reg [Y_WIDTH:0] front_height [0:3];
    reg [1:0] front_fill_level [0:3];
    reg [1:0] front_class [0:3];

    reg [2:0] stage_received_count;
    integer i;

    assign track_obj_valid = front_valid[track_rd_index];
    assign track_obj_xmin = front_xmin[track_rd_index];
    assign track_obj_xmax = front_xmax[track_rd_index];
    assign track_obj_ymin = front_ymin[track_rd_index];
    assign track_obj_ymax = front_ymax[track_rd_index];
    assign track_obj_center_x = front_center_x[track_rd_index];
    assign track_obj_center_y = front_center_y[track_rd_index];
    assign track_obj_class = front_class[track_rd_index];

    always @(*) begin
        rd_valid      = front_valid[rd_index];
        rd_label      = front_label[rd_index];
        rd_xmin       = front_xmin[rd_index];
        rd_xmax       = front_xmax[rd_index];
        rd_ymin       = front_ymin[rd_index];
        rd_ymax       = front_ymax[rd_index];
        rd_center_x   = front_center_x[rd_index];
        rd_center_y   = front_center_y[rd_index];
        rd_area       = front_area[rd_index];
        rd_width      = front_width[rd_index];
        rd_height     = front_height[rd_index];
        rd_fill_level = front_fill_level[rd_index];
        rd_class      = front_class[rd_index];
    end

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            stage_received_count <= 3'd0;
            stored_object_count  <= 3'd0;
            frame_sequence       <= 32'd0;
            object_table_commit  <= 1'b0;
            protocol_error       <= 1'b0;
            for (i = 0; i < 4; i = i + 1) begin
                stage_valid[i] <= 1'b0;
                front_valid[i] <= 1'b0;
                stage_label[i] <= {LABEL_WIDTH{1'b0}};
                stage_xmin[i] <= {X_WIDTH{1'b0}};
                stage_xmax[i] <= {X_WIDTH{1'b0}};
                stage_ymin[i] <= {Y_WIDTH{1'b0}};
                stage_ymax[i] <= {Y_WIDTH{1'b0}};
                stage_center_x[i] <= {X_WIDTH{1'b0}};
                stage_center_y[i] <= {Y_WIDTH{1'b0}};
                stage_area[i] <= {AREA_WIDTH{1'b0}};
                stage_width[i] <= {(X_WIDTH+1){1'b0}};
                stage_height[i] <= {(Y_WIDTH+1){1'b0}};
                stage_fill_level[i] <= 2'd0;
                stage_class[i] <= 2'd0;
                front_label[i] <= {LABEL_WIDTH{1'b0}};
                front_xmin[i] <= {X_WIDTH{1'b0}};
                front_xmax[i] <= {X_WIDTH{1'b0}};
                front_ymin[i] <= {Y_WIDTH{1'b0}};
                front_ymax[i] <= {Y_WIDTH{1'b0}};
                front_center_x[i] <= {X_WIDTH{1'b0}};
                front_center_y[i] <= {Y_WIDTH{1'b0}};
                front_area[i] <= {AREA_WIDTH{1'b0}};
                front_width[i] <= {(X_WIDTH+1){1'b0}};
                front_height[i] <= {(Y_WIDTH+1){1'b0}};
                front_fill_level[i] <= 2'd0;
                front_class[i] <= 2'd0;
            end
        end else begin
            object_table_commit <= 1'b0;

            if (frame_clear) begin
                stage_received_count <= 3'd0;
                protocol_error <= 1'b0;
                for (i = 0; i < 4; i = i + 1)
                    stage_valid[i] <= 1'b0;
            end else begin
                if (in_obj_valid) begin
                    if (stage_valid[in_obj_index])
                        protocol_error <= 1'b1;
                    else
                        stage_received_count <= stage_received_count + 1'b1;

                    stage_valid[in_obj_index] <= 1'b1;
                    stage_label[in_obj_index] <= in_obj_label;
                    stage_xmin[in_obj_index] <= in_obj_xmin;
                    stage_xmax[in_obj_index] <= in_obj_xmax;
                    stage_ymin[in_obj_index] <= in_obj_ymin;
                    stage_ymax[in_obj_index] <= in_obj_ymax;
                    stage_center_x[in_obj_index] <= in_obj_center_x;
                    stage_center_y[in_obj_index] <= in_obj_center_y;
                    stage_area[in_obj_index] <= in_obj_area;
                    stage_width[in_obj_index] <= in_obj_width;
                    stage_height[in_obj_index] <= in_obj_height;
                    stage_fill_level[in_obj_index] <= in_obj_fill_level;
                    stage_class[in_obj_index] <= in_obj_class;
                end

                if (in_object_frame_done) begin
                    frame_sequence      <= frame_sequence + 1'b1;
                    object_table_commit <= 1'b1;
                    if (discard_frame) begin
                        // Commit an explicit empty frame. This prevents a
                        // partial/overflowed CCL result from creating tracks,
                        // while still allowing existing tracks to age out.
                        stored_object_count <= 3'd0;
                        for (i = 0; i < 4; i = i + 1)
                            front_valid[i] <= 1'b0;
                    end else begin
                        if ((in_object_count > 4) ||
                            (stage_received_count != in_object_count))
                            protocol_error <= 1'b1;

                        stored_object_count <= (in_object_count > 4) ?
                                               3'd4 : in_object_count;
                        for (i = 0; i < 4; i = i + 1) begin
                            front_valid[i] <= stage_valid[i];
                            front_label[i] <= stage_label[i];
                            front_xmin[i] <= stage_xmin[i];
                            front_xmax[i] <= stage_xmax[i];
                            front_ymin[i] <= stage_ymin[i];
                            front_ymax[i] <= stage_ymax[i];
                            front_center_x[i] <= stage_center_x[i];
                            front_center_y[i] <= stage_center_y[i];
                            front_area[i] <= stage_area[i];
                            front_width[i] <= stage_width[i];
                            front_height[i] <= stage_height[i];
                            front_fill_level[i] <= stage_fill_level[i];
                            front_class[i] <= stage_class[i];
                        end
                    end
                end
            end
        end
    end

endmodule
