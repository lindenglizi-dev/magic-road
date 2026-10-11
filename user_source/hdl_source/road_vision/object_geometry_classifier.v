module object_geometry_classifier #(
    parameter X_WIDTH             = 8,
    parameter Y_WIDTH             = 8,
    parameter LABEL_WIDTH         = 6,
    parameter AREA_WIDTH          = 16,
    parameter CLASS_MIN_AREA      = 16,
    parameter PED_MIN_HEIGHT      = 8,
    parameter VEH_MIN_WIDTH       = 8,
    parameter MIN_FILL_QUARTERS   = 1
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
    input  wire                    in_object_frame_done,

    output reg                     obj_valid,
    output reg  [1:0]              obj_index,
    output reg  [LABEL_WIDTH-1:0]  obj_label,
    output reg  [X_WIDTH-1:0]      obj_xmin,
    output reg  [X_WIDTH-1:0]      obj_xmax,
    output reg  [Y_WIDTH-1:0]      obj_ymin,
    output reg  [Y_WIDTH-1:0]      obj_ymax,
    output reg  [X_WIDTH-1:0]      obj_center_x,
    output reg  [Y_WIDTH-1:0]      obj_center_y,
    output reg  [AREA_WIDTH-1:0]   obj_area,
    output reg  [X_WIDTH:0]        obj_width,
    output reg  [Y_WIDTH:0]        obj_height,
    output reg  [X_WIDTH+Y_WIDTH+1:0] obj_bbox_area,
    output reg  [1:0]              obj_fill_level,
    output reg  [1:0]              obj_class,
    output reg                     object_frame_done,
    output reg                     protocol_error
);

    localparam [1:0] CLASS_UNKNOWN = 2'd0;
    localparam [1:0] CLASS_PED     = 2'd1;
    localparam [1:0] CLASS_VEHICLE = 2'd2;

    localparam GEOM_AREA_WIDTH = X_WIDTH + Y_WIDTH + 2;
    localparam COMP_WIDTH = (GEOM_AREA_WIDTH > (AREA_WIDTH + 2)) ?
                            GEOM_AREA_WIDTH : (AREA_WIDTH + 2);
    localparam ASPECT_WIDTH = ((X_WIDTH > Y_WIDTH) ? X_WIDTH : Y_WIDTH) + 3;

    reg s0_valid;
    reg [1:0]             s0_index;
    reg [LABEL_WIDTH-1:0] s0_label;
    reg [X_WIDTH-1:0]     s0_xmin;
    reg [X_WIDTH-1:0]     s0_xmax;
    reg [Y_WIDTH-1:0]     s0_ymin;
    reg [Y_WIDTH-1:0]     s0_ymax;
    reg [X_WIDTH-1:0]     s0_center_x;
    reg [Y_WIDTH-1:0]     s0_center_y;
    reg [AREA_WIDTH-1:0]  s0_area;
    reg [X_WIDTH:0]       s0_width;
    reg [Y_WIDTH:0]       s0_height;
    reg                    s0_bbox_valid;

    reg s1_valid;
    reg [1:0]             s1_index;
    reg [LABEL_WIDTH-1:0] s1_label;
    reg [X_WIDTH-1:0]     s1_xmin;
    reg [X_WIDTH-1:0]     s1_xmax;
    reg [Y_WIDTH-1:0]     s1_ymin;
    reg [Y_WIDTH-1:0]     s1_ymax;
    reg [X_WIDTH-1:0]     s1_center_x;
    reg [Y_WIDTH-1:0]     s1_center_y;
    reg [AREA_WIDTH-1:0]  s1_area;
    reg [X_WIDTH:0]       s1_width;
    reg [Y_WIDTH:0]       s1_height;
    reg [GEOM_AREA_WIDTH-1:0] s1_bbox_area;
    reg                    s1_bbox_valid;

    reg done_d0;
    reg done_d1;

    wire [COMP_WIDTH-1:0] area_times4;
    wire [COMP_WIDTH-1:0] bbox_times1;
    wire [COMP_WIDTH-1:0] bbox_times2;
    wire [COMP_WIDTH-1:0] bbox_times3;
    wire [ASPECT_WIDTH-1:0] width_ext;
    wire [ASPECT_WIDTH-1:0] height_ext;
    wire ped_shape;
    wire vehicle_shape;
    wire fill_pass;
    wire area_inside_bbox;

    assign area_times4 =
        {{(COMP_WIDTH-AREA_WIDTH-2){1'b0}}, s1_area, 2'b00};
    assign bbox_times1 =
        {{(COMP_WIDTH-GEOM_AREA_WIDTH){1'b0}}, s1_bbox_area};
    assign bbox_times2 = bbox_times1 << 1;
    assign bbox_times3 = bbox_times2 + bbox_times1;

    assign width_ext =
        {{(ASPECT_WIDTH-X_WIDTH-1){1'b0}}, s1_width};
    assign height_ext =
        {{(ASPECT_WIDTH-Y_WIDTH-1){1'b0}}, s1_height};

    // Hardware-friendly 3:2 aspect tests; no divider is used.
    assign ped_shape = (height_ext << 1) >=
                       ((width_ext << 1) + width_ext);
    assign vehicle_shape = (width_ext << 1) >=
                           ((height_ext << 1) + height_ext);

    assign fill_pass = (MIN_FILL_QUARTERS == 0) ? 1'b1 :
                       (MIN_FILL_QUARTERS == 1) ?
                           (area_times4 >= bbox_times1) :
                       (MIN_FILL_QUARTERS == 2) ?
                           (area_times4 >= bbox_times2) :
                           (area_times4 >= bbox_times3);

    assign area_inside_bbox =
        {{(COMP_WIDTH-AREA_WIDTH){1'b0}}, s1_area} <= bbox_times1;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            s0_valid           <= 1'b0;
            s1_valid           <= 1'b0;
            done_d0            <= 1'b0;
            done_d1            <= 1'b0;
            obj_valid          <= 1'b0;
            object_frame_done  <= 1'b0;
            protocol_error     <= 1'b0;
            obj_index          <= 2'd0;
            obj_label          <= {LABEL_WIDTH{1'b0}};
            obj_xmin           <= {X_WIDTH{1'b0}};
            obj_xmax           <= {X_WIDTH{1'b0}};
            obj_ymin           <= {Y_WIDTH{1'b0}};
            obj_ymax           <= {Y_WIDTH{1'b0}};
            obj_center_x       <= {X_WIDTH{1'b0}};
            obj_center_y       <= {Y_WIDTH{1'b0}};
            obj_area           <= {AREA_WIDTH{1'b0}};
            obj_width          <= {(X_WIDTH+1){1'b0}};
            obj_height         <= {(Y_WIDTH+1){1'b0}};
            obj_bbox_area      <= {GEOM_AREA_WIDTH{1'b0}};
            obj_fill_level     <= 2'd0;
            obj_class          <= CLASS_UNKNOWN;
        end else if (frame_clear) begin
            s0_valid           <= 1'b0;
            s1_valid           <= 1'b0;
            done_d0            <= 1'b0;
            done_d1            <= 1'b0;
            obj_valid          <= 1'b0;
            object_frame_done  <= 1'b0;
            protocol_error     <= 1'b0;
        end else begin
            s0_valid          <= in_obj_valid;
            s1_valid          <= s0_valid;
            obj_valid         <= s1_valid;
            done_d0           <= in_object_frame_done;
            done_d1           <= done_d0;
            object_frame_done <= done_d1;

            if (in_obj_valid) begin
                s0_index      <= in_obj_index;
                s0_label      <= in_obj_label;
                s0_xmin       <= in_obj_xmin;
                s0_xmax       <= in_obj_xmax;
                s0_ymin       <= in_obj_ymin;
                s0_ymax       <= in_obj_ymax;
                s0_center_x   <= in_obj_center_x;
                s0_center_y   <= in_obj_center_y;
                s0_area       <= in_obj_area;
                s0_width      <= {1'b0, in_obj_xmax} -
                                 {1'b0, in_obj_xmin} + 1'b1;
                s0_height     <= {1'b0, in_obj_ymax} -
                                 {1'b0, in_obj_ymin} + 1'b1;
                s0_bbox_valid <= (in_obj_xmax >= in_obj_xmin) &&
                                 (in_obj_ymax >= in_obj_ymin) &&
                                 (in_obj_area != 0);
            end

            if (s0_valid) begin
                s1_index      <= s0_index;
                s1_label      <= s0_label;
                s1_xmin       <= s0_xmin;
                s1_xmax       <= s0_xmax;
                s1_ymin       <= s0_ymin;
                s1_ymax       <= s0_ymax;
                s1_center_x   <= s0_center_x;
                s1_center_y   <= s0_center_y;
                s1_area       <= s0_area;
                s1_width      <= s0_width;
                s1_height     <= s0_height;
                s1_bbox_area  <= s0_width * s0_height;
                s1_bbox_valid <= s0_bbox_valid;
            end

            if (s1_valid) begin
                obj_index     <= s1_index;
                obj_label     <= s1_label;
                obj_xmin      <= s1_xmin;
                obj_xmax      <= s1_xmax;
                obj_ymin      <= s1_ymin;
                obj_ymax      <= s1_ymax;
                obj_center_x  <= s1_center_x;
                obj_center_y  <= s1_center_y;
                obj_area      <= s1_area;
                obj_width     <= s1_width;
                obj_height    <= s1_height;
                obj_bbox_area <= s1_bbox_area;

                if (area_times4 >= bbox_times3)
                    obj_fill_level <= 2'd3;
                else if (area_times4 >= bbox_times2)
                    obj_fill_level <= 2'd2;
                else if (area_times4 >= bbox_times1)
                    obj_fill_level <= 2'd1;
                else
                    obj_fill_level <= 2'd0;

                if (!s1_bbox_valid || !area_inside_bbox) begin
                    obj_class      <= CLASS_UNKNOWN;
                    protocol_error <= 1'b1;
                end else if ((s1_area >= CLASS_MIN_AREA) && fill_pass &&
                             (s1_height >= PED_MIN_HEIGHT) && ped_shape) begin
                    obj_class <= CLASS_PED;
                end else if ((s1_area >= CLASS_MIN_AREA) && fill_pass &&
                             (s1_width >= VEH_MIN_WIDTH) && vehicle_shape) begin
                    obj_class <= CLASS_VEHICLE;
                end else begin
                    obj_class <= CLASS_UNKNOWN;
                end
            end
        end
    end

endmodule
