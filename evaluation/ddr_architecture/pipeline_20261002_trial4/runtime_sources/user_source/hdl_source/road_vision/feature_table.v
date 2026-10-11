module feature_table #(
    parameter X_WIDTH     = 8,
    parameter Y_WIDTH     = 8,
    parameter LABEL_WIDTH = 6,
    parameter AREA_WIDTH  = 16,
    parameter MAX_LABEL   = 32
)(
    input  wire                     clk,
    input  wire                     rst_n,
    input  wire                     frame_clear,

    input  wire                     update_valid,
    input  wire                     update_new_label,
    input  wire [LABEL_WIDTH-1:0]   update_label,
    input  wire [X_WIDTH-1:0]       update_start,
    input  wire [X_WIDTH-1:0]       update_end,
    input  wire [Y_WIDTH-1:0]       update_y,
    output reg                      update_done,

    input  wire                     merge_req,
    input  wire [LABEL_WIDTH-1:0]   merge_src_label,
    input  wire [LABEL_WIDTH-1:0]   merge_dst_label,
    output reg                      merge_done,

    input  wire                     rd_req,
    input  wire [LABEL_WIDTH-1:0]   rd_label,
    output reg                      rd_valid,
    output reg                      rd_feature_valid,
    output reg  [AREA_WIDTH-1:0]    rd_area,
    output reg  [X_WIDTH-1:0]       rd_xmin,
    output reg  [X_WIDTH-1:0]       rd_xmax,
    output reg  [Y_WIDTH-1:0]       rd_ymin,
    output reg  [Y_WIDTH-1:0]       rd_ymax,

    output reg                      area_overflow,
    output reg                      protocol_error
);

    reg [AREA_WIDTH-1:0] area_mem  [0:MAX_LABEL];
    reg [X_WIDTH-1:0]    xmin_mem  [0:MAX_LABEL];
    reg [X_WIDTH-1:0]    xmax_mem  [0:MAX_LABEL];
    reg [Y_WIDTH-1:0]    ymin_mem  [0:MAX_LABEL];
    reg [Y_WIDTH-1:0]    ymax_mem  [0:MAX_LABEL];
    reg                  valid_mem [0:MAX_LABEL];
    reg                  epoch_mem [0:MAX_LABEL];
    reg                  frame_epoch;

    reg [X_WIDTH:0]       run_length;
    reg [AREA_WIDTH:0]    area_sum;

    wire update_label_in_range;
    wire merge_src_in_range;
    wire merge_dst_in_range;

    assign update_label_in_range =
        (update_label != {LABEL_WIDTH{1'b0}}) &&
        (update_label <= MAX_LABEL);
    assign merge_src_in_range =
        (merge_src_label != {LABEL_WIDTH{1'b0}}) &&
        (merge_src_label <= MAX_LABEL);
    assign merge_dst_in_range =
        (merge_dst_label != {LABEL_WIDTH{1'b0}}) &&
        (merge_dst_label <= MAX_LABEL);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            rd_valid         <= 1'b0;
            rd_feature_valid <= 1'b0;
            rd_area          <= {AREA_WIDTH{1'b0}};
            rd_xmin          <= {X_WIDTH{1'b0}};
            rd_xmax          <= {X_WIDTH{1'b0}};
            rd_ymin          <= {Y_WIDTH{1'b0}};
            rd_ymax          <= {Y_WIDTH{1'b0}};
        end else if (frame_clear) begin
            rd_valid         <= 1'b0;
            rd_feature_valid <= 1'b0;
        end else begin
            rd_valid <= 1'b0;

            if (rd_req) begin
                rd_valid <= 1'b1;
                if ((rd_label != {LABEL_WIDTH{1'b0}}) &&
                    (rd_label <= MAX_LABEL) &&
                    valid_mem[rd_label] &&
                    (epoch_mem[rd_label] == frame_epoch)) begin
                    rd_feature_valid <= 1'b1;
                    rd_area          <= area_mem[rd_label];
                    rd_xmin          <= xmin_mem[rd_label];
                    rd_xmax          <= xmax_mem[rd_label];
                    rd_ymin          <= ymin_mem[rd_label];
                    rd_ymax          <= ymax_mem[rd_label];
                end else begin
                    rd_feature_valid <= 1'b0;
                    rd_area          <= {AREA_WIDTH{1'b0}};
                    rd_xmin          <= {X_WIDTH{1'b0}};
                    rd_xmax          <= {X_WIDTH{1'b0}};
                    rd_ymin          <= {Y_WIDTH{1'b0}};
                    rd_ymax          <= {Y_WIDTH{1'b0}};
                end
            end
        end
    end

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            frame_epoch   <= 1'b0;
            update_done   <= 1'b0;
            merge_done    <= 1'b0;
            area_overflow <= 1'b0;
            protocol_error <= 1'b0;
            run_length    <= {(X_WIDTH+1){1'b0}};
            area_sum      <= {(AREA_WIDTH+1){1'b0}};
        end else if (frame_clear) begin
            frame_epoch    <= ~frame_epoch;
            update_done    <= 1'b0;
            merge_done     <= 1'b0;
            area_overflow  <= 1'b0;
            protocol_error <= 1'b0;
        end else begin
            update_done <= 1'b0;
            merge_done  <= 1'b0;

            if (update_valid && merge_req)
                protocol_error <= 1'b1;

            if (merge_req) begin
                merge_done <= 1'b1;

                if (!merge_src_in_range || !merge_dst_in_range) begin
                    protocol_error <= 1'b1;
                end else if (merge_src_label != merge_dst_label) begin
                    if (!valid_mem[merge_src_label] ||
                        (epoch_mem[merge_src_label] != frame_epoch)) begin
                        protocol_error <= 1'b1;
                    end else if (!valid_mem[merge_dst_label] ||
                                 (epoch_mem[merge_dst_label] != frame_epoch)) begin
                        area_mem[merge_dst_label]  <= area_mem[merge_src_label];
                        xmin_mem[merge_dst_label]  <= xmin_mem[merge_src_label];
                        xmax_mem[merge_dst_label]  <= xmax_mem[merge_src_label];
                        ymin_mem[merge_dst_label]  <= ymin_mem[merge_src_label];
                        ymax_mem[merge_dst_label]  <= ymax_mem[merge_src_label];
                        valid_mem[merge_dst_label] <= 1'b1;
                        epoch_mem[merge_dst_label] <= frame_epoch;
                        valid_mem[merge_src_label] <= 1'b0;
                    end else begin
                        area_sum = {1'b0, area_mem[merge_dst_label]} +
                                   {1'b0, area_mem[merge_src_label]};
                        if (area_sum[AREA_WIDTH]) begin
                            area_mem[merge_dst_label] <= {AREA_WIDTH{1'b1}};
                            area_overflow <= 1'b1;
                        end else begin
                            area_mem[merge_dst_label] <= area_sum[AREA_WIDTH-1:0];
                        end

                        if (xmin_mem[merge_src_label] < xmin_mem[merge_dst_label])
                            xmin_mem[merge_dst_label] <= xmin_mem[merge_src_label];
                        if (xmax_mem[merge_src_label] > xmax_mem[merge_dst_label])
                            xmax_mem[merge_dst_label] <= xmax_mem[merge_src_label];
                        if (ymin_mem[merge_src_label] < ymin_mem[merge_dst_label])
                            ymin_mem[merge_dst_label] <= ymin_mem[merge_src_label];
                        if (ymax_mem[merge_src_label] > ymax_mem[merge_dst_label])
                            ymax_mem[merge_dst_label] <= ymax_mem[merge_src_label];

                        valid_mem[merge_src_label] <= 1'b0;
                    end
                end
            end else if (update_valid) begin
                update_done <= 1'b1;

                if (!update_label_in_range || (update_start > update_end)) begin
                    protocol_error <= 1'b1;
                end else begin
                    run_length = {1'b0, update_end} -
                                 {1'b0, update_start} + 1'b1;

                    if (update_new_label) begin
                        area_mem[update_label]  <= run_length;
                        xmin_mem[update_label]  <= update_start;
                        xmax_mem[update_label]  <= update_end;
                        ymin_mem[update_label]  <= update_y;
                        ymax_mem[update_label]  <= update_y;
                        valid_mem[update_label] <= 1'b1;
                        epoch_mem[update_label] <= frame_epoch;
                    end else if (!valid_mem[update_label] ||
                                 (epoch_mem[update_label] != frame_epoch)) begin
                        protocol_error <= 1'b1;
                    end else begin
                        area_sum = {1'b0, area_mem[update_label]} + run_length;
                        if (area_sum[AREA_WIDTH]) begin
                            area_mem[update_label] <= {AREA_WIDTH{1'b1}};
                            area_overflow <= 1'b1;
                        end else begin
                            area_mem[update_label] <= area_sum[AREA_WIDTH-1:0];
                        end

                        if (update_start < xmin_mem[update_label])
                            xmin_mem[update_label] <= update_start;
                        if (update_end > xmax_mem[update_label])
                            xmax_mem[update_label] <= update_end;
                        if (update_y < ymin_mem[update_label])
                            ymin_mem[update_label] <= update_y;
                        if (update_y > ymax_mem[update_label])
                            ymax_mem[update_label] <= update_y;
                    end
                end
            end
        end
    end

endmodule
