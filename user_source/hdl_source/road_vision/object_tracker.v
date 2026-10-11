// Four-object, four-track nearest-neighbour tracker in the analysis clock domain.
// Reads the committed front bank of object_frame_store; no video backpressure.
module object_tracker #(
    parameter X_WIDTH = 8,
    parameter Y_WIDTH = 8,
    parameter MAX_DISTANCE = 24,
    parameter MAX_MISS = 2,
    parameter CONFIRM_HITS = 2
)(
    input  wire                    clk,
    input  wire                    rst_n,
    input  wire                    object_table_commit,
    output reg  [1:0]              object_rd_index,
    input  wire                    object_valid,
    input  wire [X_WIDTH-1:0]      object_center_x,
    input  wire [Y_WIDTH-1:0]      object_center_y,
    input  wire [X_WIDTH-1:0]      object_xmin,
    input  wire [X_WIDTH-1:0]      object_xmax,
    input  wire [Y_WIDTH-1:0]      object_ymin,
    input  wire [Y_WIDTH-1:0]      object_ymax,
    input  wire [1:0]              object_class,
    input  wire [2:0]              object_count,
    input  wire [1:0]              track_rd_index,
    // Independent read port for the event scanner; the display port stays free.
    input  wire [1:0]              event_rd_index,
    output wire                    event_track_valid,
    output wire                    event_track_visible,
    output wire                    event_track_confirmed,
    output wire [15:0]             event_track_id,
    output wire [X_WIDTH-1:0]      event_track_center_x,
    output wire [Y_WIDTH-1:0]      event_track_center_y,
    output wire [1:0]              event_track_class,
    output reg                     track_valid,
    output reg                     track_visible,
    output reg                     track_confirmed,
    output reg  [15:0]             track_id,
    output reg  [X_WIDTH-1:0]      track_center_x,
    output reg  [Y_WIDTH-1:0]      track_center_y,
    output reg  [X_WIDTH-1:0]      track_xmin,
    output reg  [X_WIDTH-1:0]      track_xmax,
    output reg  [Y_WIDTH-1:0]      track_ymin,
    output reg  [Y_WIDTH-1:0]      track_ymax,
    output reg  signed [X_WIDTH:0] track_vx,
    output reg  signed [Y_WIDTH:0] track_vy,
    output reg  [1:0]              track_class,
    output reg  [2:0]              track_miss_count,
    output reg                     track_table_ready,
    output reg                     track_frame_done,
    output reg                     track_overflow,
    output reg                     protocol_error
);
    localparam [2:0] S_IDLE = 3'd0, S_SCAN = 3'd1,
                     S_SELECT = 3'd2, S_APPLY = 3'd3,
                     S_AGE = 3'd4, S_DONE = 3'd5;
    localparam DIST_WIDTH = ((X_WIDTH > Y_WIDTH) ? X_WIDTH : Y_WIDTH) + 2;
    localparam CLASS_MISMATCH_PENALTY = MAX_DISTANCE / 2;

    reg [2:0] state;
    reg [1:0] age_index;
    reg [3:0] matched;
    reg [15:0] next_id;
    reg active [0:3];
    reg [15:0] id_mem [0:3];
    reg [X_WIDTH-1:0] cx_mem [0:3], xmin_mem [0:3], xmax_mem [0:3];
    reg [Y_WIDTH-1:0] cy_mem [0:3], ymin_mem [0:3], ymax_mem [0:3];
    reg signed [X_WIDTH:0] vx_mem [0:3];
    reg signed [Y_WIDTH:0] vy_mem [0:3];
    reg [1:0] class_mem [0:3];
    // Consecutive evidence is required before a track changes its class.
    reg [1:0] class_conf_mem [0:3];
    reg [2:0] hit_mem [0:3], miss_mem [0:3];
    reg scan_valid;
    reg scan_candidate_found, scan_free_found;
    reg [1:0] scan_candidate_index, scan_free_index;
    reg [X_WIDTH-1:0] scan_center_x, scan_xmin, scan_xmax;
    reg [Y_WIDTH-1:0] scan_center_y, scan_ymin, scan_ymax;
    reg [1:0] scan_class;

    reg candidate_found, free_found;
    reg [1:0] candidate_index, free_index;
    reg [DIST_WIDTH-1:0] best_score;
    reg [DIST_WIDTH-1:0] distance;
    reg [DIST_WIDTH-1:0] score;
    reg [X_WIDTH-1:0] dx;
    reg [Y_WIDTH-1:0] dy;
    integer j;
    integer i;

    assign event_track_valid = active[event_rd_index];
    assign event_track_visible = active[event_rd_index] && matched[event_rd_index];
    assign event_track_confirmed = active[event_rd_index] &&
                                   (hit_mem[event_rd_index] >= CONFIRM_HITS);
    assign event_track_id = id_mem[event_rd_index];
    assign event_track_center_x = cx_mem[event_rd_index];
    assign event_track_center_y = cy_mem[event_rd_index];
    assign event_track_class = class_mem[event_rd_index];

    // Class disagreement is a soft cost, not a hard gate: a single noisy
    // classification must not break the spatially continuous track ID.
    always @(*) begin
        candidate_found = 1'b0;
        candidate_index = 2'd0;
        free_found = 1'b0;
        free_index = 2'd0;
        best_score = {DIST_WIDTH{1'b1}};
        distance = {DIST_WIDTH{1'b0}};
        score = {DIST_WIDTH{1'b0}};
        dx = {X_WIDTH{1'b0}};
        dy = {Y_WIDTH{1'b0}};
        for (j = 0; j < 4; j = j + 1) begin
            if (!active[j] && !free_found) begin
                free_found = 1'b1;
                free_index = j[1:0];
            end
            dx = (scan_center_x >= cx_mem[j]) ?
                 (scan_center_x - cx_mem[j]) :
                 (cx_mem[j] - scan_center_x);
            dy = (scan_center_y >= cy_mem[j]) ?
                 (scan_center_y - cy_mem[j]) :
                 (cy_mem[j] - scan_center_y);
            distance = {{(DIST_WIDTH-X_WIDTH){1'b0}}, dx} +
                       {{(DIST_WIDTH-Y_WIDTH){1'b0}}, dy};
            score = distance;
            if ((class_mem[j] != 0) && (scan_class != 0) &&
                (class_mem[j] != scan_class))
                score = distance + CLASS_MISMATCH_PENALTY;
            if (active[j] && !matched[j] &&
                (distance <= MAX_DISTANCE) &&
                (!candidate_found || (score < best_score))) begin
                candidate_found = 1'b1;
                candidate_index = j[1:0];
                best_score = score;
            end
        end
    end

    always @(*) begin
        track_valid = active[track_rd_index];
        track_visible = active[track_rd_index] && matched[track_rd_index];
        track_confirmed = active[track_rd_index] &&
                          (hit_mem[track_rd_index] >= CONFIRM_HITS);
        track_id = id_mem[track_rd_index];
        track_center_x = cx_mem[track_rd_index];
        track_center_y = cy_mem[track_rd_index];
        track_xmin = xmin_mem[track_rd_index];
        track_xmax = xmax_mem[track_rd_index];
        track_ymin = ymin_mem[track_rd_index];
        track_ymax = ymax_mem[track_rd_index];
        track_vx = vx_mem[track_rd_index];
        track_vy = vy_mem[track_rd_index];
        track_class = class_mem[track_rd_index];
        track_miss_count = miss_mem[track_rd_index];
    end

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state <= S_IDLE;
            object_rd_index <= 2'd0;
            age_index <= 2'd0;
            matched <= 4'b0000;
            next_id <= 16'd1;
            scan_valid <= 1'b0;
            scan_candidate_found <= 1'b0;
            scan_free_found <= 1'b0;
            scan_candidate_index <= 2'd0;
            scan_free_index <= 2'd0;
            track_table_ready <= 1'b0;
            track_frame_done <= 1'b0;
            track_overflow <= 1'b0;
            protocol_error <= 1'b0;
            for (i = 0; i < 4; i = i + 1) begin
                active[i] <= 1'b0;
                id_mem[i] <= 16'd0;
                cx_mem[i] <= {X_WIDTH{1'b0}};
                cy_mem[i] <= {Y_WIDTH{1'b0}};
                xmin_mem[i] <= {X_WIDTH{1'b0}};
                xmax_mem[i] <= {X_WIDTH{1'b0}};
                ymin_mem[i] <= {Y_WIDTH{1'b0}};
                ymax_mem[i] <= {Y_WIDTH{1'b0}};
                vx_mem[i] <= {(X_WIDTH+1){1'b0}};
                vy_mem[i] <= {(Y_WIDTH+1){1'b0}};
                class_mem[i] <= 2'd0;
                class_conf_mem[i] <= 2'd0;
                hit_mem[i] <= 3'd0;
                miss_mem[i] <= 3'd0;
            end
        end else begin
            track_frame_done <= 1'b0;
            if (object_table_commit && state != S_IDLE)
                protocol_error <= 1'b1;
            case (state)
                S_IDLE: if (object_table_commit) begin
                    track_table_ready <= 1'b0;
                    matched <= 4'b0000;
                    object_rd_index <= 2'd0;
                    if (object_count > 4)
                        protocol_error <= 1'b1;
                    state <= (object_count == 0) ? S_AGE : S_SCAN;
                    age_index <= 2'd0;
                end

                S_SCAN: begin
                    scan_valid <= object_valid;
                    scan_center_x <= object_center_x;
                    scan_center_y <= object_center_y;
                    scan_xmin <= object_xmin;
                    scan_xmax <= object_xmax;
                    scan_ymin <= object_ymin;
                    scan_ymax <= object_ymax;
                    scan_class <= object_class;
                    state <= S_SELECT;
                end

                S_SELECT: begin
                    scan_candidate_found <= candidate_found;
                    scan_candidate_index <= candidate_index;
                    scan_free_found <= free_found;
                    scan_free_index <= free_index;
                    state <= S_APPLY;
                end

                S_APPLY: begin
                    if (scan_valid) begin
                        if (scan_candidate_found) begin
                            matched[scan_candidate_index] <= 1'b1;
                            vx_mem[scan_candidate_index] <=
                                $signed({1'b0, scan_center_x}) -
                                $signed({1'b0, cx_mem[scan_candidate_index]});
                            vy_mem[scan_candidate_index] <=
                                $signed({1'b0, scan_center_y}) -
                                $signed({1'b0, cy_mem[scan_candidate_index]});
                            cx_mem[scan_candidate_index] <= scan_center_x;
                            cy_mem[scan_candidate_index] <= scan_center_y;
                            xmin_mem[scan_candidate_index] <= scan_xmin;
                            xmax_mem[scan_candidate_index] <= scan_xmax;
                            ymin_mem[scan_candidate_index] <= scan_ymin;
                            ymax_mem[scan_candidate_index] <= scan_ymax;
                            if (scan_class != 0) begin
                                if (class_mem[scan_candidate_index] == 0) begin
                                    class_mem[scan_candidate_index] <= scan_class;
                                    class_conf_mem[scan_candidate_index] <= 2'd1;
                                end else if (class_mem[scan_candidate_index] ==
                                             scan_class) begin
                                    if (class_conf_mem[scan_candidate_index] < 2)
                                        class_conf_mem[scan_candidate_index] <=
                                            class_conf_mem[scan_candidate_index] + 1'b1;
                                end else if (class_conf_mem[scan_candidate_index] != 0) begin
                                    class_conf_mem[scan_candidate_index] <=
                                        class_conf_mem[scan_candidate_index] - 1'b1;
                                end else begin
                                    class_mem[scan_candidate_index] <= scan_class;
                                    class_conf_mem[scan_candidate_index] <= 2'd1;
                                end
                            end
                            if (hit_mem[scan_candidate_index] < CONFIRM_HITS)
                                hit_mem[scan_candidate_index] <=
                                    hit_mem[scan_candidate_index] + 1'b1;
                            miss_mem[scan_candidate_index] <= 3'd0;
                        end else if (scan_free_found) begin
                            active[scan_free_index] <= 1'b1;
                            matched[scan_free_index] <= 1'b1;
                            id_mem[scan_free_index] <= next_id;
                            next_id <= (next_id == 16'hffff) ? 16'd1 :
                                       next_id + 1'b1;
                            cx_mem[scan_free_index] <= scan_center_x;
                            cy_mem[scan_free_index] <= scan_center_y;
                            xmin_mem[scan_free_index] <= scan_xmin;
                            xmax_mem[scan_free_index] <= scan_xmax;
                            ymin_mem[scan_free_index] <= scan_ymin;
                            ymax_mem[scan_free_index] <= scan_ymax;
                            vx_mem[scan_free_index] <= {(X_WIDTH+1){1'b0}};
                            vy_mem[scan_free_index] <= {(Y_WIDTH+1){1'b0}};
                            class_mem[scan_free_index] <= scan_class;
                            class_conf_mem[scan_free_index] <=
                                (scan_class == 0) ? 2'd0 : 2'd1;
                            hit_mem[scan_free_index] <= 3'd1;
                            miss_mem[scan_free_index] <= 3'd0;
                        end else begin
                            track_overflow <= 1'b1;
                        end
                    end else
                        protocol_error <= 1'b1;
                    if (object_rd_index == object_count - 1'b1) begin
                        age_index <= 2'd0;
                        state <= S_AGE;
                    end else begin
                        object_rd_index <= object_rd_index + 1'b1;
                        state <= S_SCAN;
                    end
                end

                S_AGE: begin
                    if (active[age_index] && !matched[age_index]) begin
                        if (miss_mem[age_index] >= MAX_MISS) begin
                            active[age_index] <= 1'b0;
                            hit_mem[age_index] <= 3'd0;
                            miss_mem[age_index] <= 3'd0;
                            class_conf_mem[age_index] <= 2'd0;
                        end else begin
                            miss_mem[age_index] <= miss_mem[age_index] + 1'b1;
                            vx_mem[age_index] <= {(X_WIDTH+1){1'b0}};
                            vy_mem[age_index] <= {(Y_WIDTH+1){1'b0}};
                        end
                    end
                    if (age_index == 2'd3)
                        state <= S_DONE;
                    else
                        age_index <= age_index + 1'b1;
                end

                S_DONE: begin
                    track_table_ready <= 1'b1;
                    track_frame_done <= 1'b1;
                    state <= S_IDLE;
                end

                default: begin
                    state <= S_IDLE;
                    protocol_error <= 1'b1;
                end
            endcase
        end
    end
endmodule
