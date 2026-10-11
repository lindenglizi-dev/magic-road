// Scans the four committed tracks after track_frame_done. Event bits are
// {dwell, left-to-right line crossing, zone entry}; pulses last one clock.
module track_event_detector #(
    parameter X_WIDTH = 8,
    parameter Y_WIDTH = 8,
    parameter ZONE_X_MIN = 80,
    parameter ZONE_X_MAX = 175,
    parameter ZONE_Y_MIN = 50,
    parameter ZONE_Y_MAX = 149,
    parameter LINE_X = 128,
    parameter DWELL_FRAMES = 30
)(
    input  wire                   clk,
    input  wire                   rst_n,
    input  wire                   track_frame_done,
    output reg  [1:0]             track_rd_index,
    input  wire                   track_valid,
    input  wire                   track_visible,
    input  wire                   track_confirmed,
    input  wire [15:0]            track_id,
    input  wire [X_WIDTH-1:0]     track_center_x,
    input  wire [Y_WIDTH-1:0]     track_center_y,
    input  wire [1:0]             track_class,
    output reg                    event_valid,
    output reg  [2:0]             event_type,
    output reg  [15:0]            event_track_id,
    output reg  [1:0]             event_track_class,
    output reg  [15:0]            line_cross_count,
    output reg                    event_frame_done,
    output reg                    protocol_error
);
    localparam S_IDLE = 1'b0, S_SCAN = 1'b1;
    reg state;
    reg prior_valid [0:3];
    reg prior_visible [0:3];
    reg prior_inside [0:3];
    reg prior_dwell_fired [0:3];
    reg [15:0] prior_id [0:3];
    reg [X_WIDTH-1:0] prior_x [0:3];
    reg [15:0] dwell_count [0:3];
    integer i;

    wire inside_zone = (track_center_x >= ZONE_X_MIN) &&
                       (track_center_x <= ZONE_X_MAX) &&
                       (track_center_y >= ZONE_Y_MIN) &&
                       (track_center_y <= ZONE_Y_MAX);
    wire same_track = prior_valid[track_rd_index] &&
                      (prior_id[track_rd_index] == track_id);
    wire continuous_inside = same_track &&
                             prior_visible[track_rd_index] &&
                             prior_inside[track_rd_index];
    wire zone_entry = inside_zone &&
                      (!same_track || !prior_inside[track_rd_index]);
    wire line_cross = same_track && prior_visible[track_rd_index] &&
                      (prior_x[track_rd_index] < LINE_X) &&
                      (track_center_x >= LINE_X);
    wire dwell_due = inside_zone &&
                     !(same_track && prior_dwell_fired[track_rd_index]) &&
                     ((continuous_inside ? dwell_count[track_rd_index] : 16'd0)
                      >= (DWELL_FRAMES - 1));

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state <= S_IDLE;
            track_rd_index <= 2'd0;
            event_valid <= 1'b0;
            event_type <= 3'd0;
            event_track_id <= 16'd0;
            event_track_class <= 2'd0;
            line_cross_count <= 16'd0;
            event_frame_done <= 1'b0;
            protocol_error <= 1'b0;
            for (i = 0; i < 4; i = i + 1) begin
                prior_valid[i] <= 1'b0;
                prior_visible[i] <= 1'b0;
                prior_inside[i] <= 1'b0;
                prior_dwell_fired[i] <= 1'b0;
                prior_id[i] <= 16'd0;
                prior_x[i] <= {X_WIDTH{1'b0}};
                dwell_count[i] <= 16'd0;
            end
        end else begin
            event_valid <= 1'b0;
            event_type <= 3'd0;
            event_frame_done <= 1'b0;
            if (track_frame_done && state != S_IDLE)
                protocol_error <= 1'b1;
            case (state)
                S_IDLE: if (track_frame_done) begin
                    track_rd_index <= 2'd0;
                    state <= S_SCAN;
                end
                S_SCAN: begin
                    if (track_valid && track_confirmed && track_visible) begin
                        event_valid <= zone_entry || line_cross || dwell_due;
                        event_type <= {dwell_due, line_cross, zone_entry};
                        event_track_id <= track_id;
                        event_track_class <= track_class;
                        if (line_cross && line_cross_count != 16'hffff)
                            line_cross_count <= line_cross_count + 1'b1;
                        prior_valid[track_rd_index] <= 1'b1;
                        prior_visible[track_rd_index] <= 1'b1;
                        prior_inside[track_rd_index] <= inside_zone;
                        prior_id[track_rd_index] <= track_id;
                        prior_x[track_rd_index] <= track_center_x;
                        if (inside_zone) begin
                            if (continuous_inside) begin
                                if (dwell_count[track_rd_index] < DWELL_FRAMES)
                                    dwell_count[track_rd_index] <=
                                        dwell_count[track_rd_index] + 1'b1;
                            end else
                                dwell_count[track_rd_index] <= 16'd1;
                            prior_dwell_fired[track_rd_index] <=
                                dwell_due || (same_track &&
                                prior_dwell_fired[track_rd_index]);
                        end else begin
                            dwell_count[track_rd_index] <= 16'd0;
                            prior_dwell_fired[track_rd_index] <= 1'b0;
                        end
                    end else if (track_valid && track_confirmed &&
                                 prior_valid[track_rd_index] &&
                                 prior_id[track_rd_index] == track_id) begin
                        // A short miss is not a new zone entry. Dwell time
                        // restarts, while a previously fired alert stays fired.
                        prior_visible[track_rd_index] <= 1'b0;
                        dwell_count[track_rd_index] <= 16'd0;
                    end else begin
                        prior_valid[track_rd_index] <= 1'b0;
                        prior_visible[track_rd_index] <= 1'b0;
                        prior_inside[track_rd_index] <= 1'b0;
                        prior_dwell_fired[track_rd_index] <= 1'b0;
                        dwell_count[track_rd_index] <= 16'd0;
                    end
                    if (track_rd_index == 2'd3) begin
                        event_frame_done <= 1'b1;
                        state <= S_IDLE;
                    end else
                        track_rd_index <= track_rd_index + 1'b1;
                end
            endcase
        end
    end
endmodule
