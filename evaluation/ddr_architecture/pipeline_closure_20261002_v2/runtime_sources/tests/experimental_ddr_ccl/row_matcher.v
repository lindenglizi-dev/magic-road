module row_matcher #(
    parameter X_WIDTH     = 8,
    parameter Y_WIDTH     = 8,
    parameter LABEL_WIDTH = 6,
    parameter ADDR_WIDTH  = 6,
    parameter MAX_RUN     = 64,
    parameter MAX_LABEL   = 32
)(
    input  wire                     clk,
    input  wire                     rst_n,
    input  wire                     frame_clear,
    input  wire                     start,

    input  wire                     raw_locked,
    input  wire [Y_WIDTH-1:0]       raw_row_y,
    input  wire [ADDR_WIDTH:0]      raw_run_count,
    output wire                     raw_rd_req,
    output wire [ADDR_WIDTH-1:0]    raw_rd_idx,
    input  wire                     raw_rd_valid,
    input  wire [X_WIDTH-1:0]       raw_rd_start,
    input  wire [X_WIDTH-1:0]       raw_rd_end,
    output reg                      raw_release,

    input  wire [ADDR_WIDTH:0]      prev_count,
    output wire                     prev_rd_req,
    output wire [ADDR_WIDTH-1:0]    prev_rd_idx,
    input  wire                     prev_rd_valid,
    input  wire [X_WIDTH-1:0]       prev_rd_start,
    input  wire [X_WIDTH-1:0]       prev_rd_end,
    input  wire [LABEL_WIDTH-1:0]   prev_rd_label,

    output reg                      curr_wr_en,
    output reg  [X_WIDTH-1:0]       curr_wr_start,
    output reg  [X_WIDTH-1:0]       curr_wr_end,
    output reg  [LABEL_WIDTH-1:0]   curr_wr_label,
    output reg                      row_commit,

    output reg                      alloc_req,
    input  wire                     alloc_done,
    input  wire [LABEL_WIDTH-1:0]   alloc_label,
    output reg                      union_req,
    output reg  [LABEL_WIDTH-1:0]   union_a,
    output reg  [LABEL_WIDTH-1:0]   union_b,
    input  wire                     union_done,
    input  wire [LABEL_WIDTH-1:0]   union_root,

    output reg                      feature_update_valid,
    output reg                      feature_update_new_label,
    output reg  [LABEL_WIDTH-1:0]   feature_update_label,
    output reg  [X_WIDTH-1:0]       feature_update_start,
    output reg  [X_WIDTH-1:0]       feature_update_end,
    output reg  [Y_WIDTH-1:0]       feature_update_y,

    output reg                      busy,
    output reg                      row_done,
    output reg  [31:0]              row_match_cycle_count,
    output reg  [31:0]              row_match_cycle_max,
    output reg                      matcher_error
);

    localparam S_IDLE           = 4'd0;
    localparam S_LOAD_CURR_REQ  = 4'd1;
    localparam S_LOAD_CURR_WAIT = 4'd2;
    localparam S_SCAN_PREV      = 4'd3;
    localparam S_RESOLVE_LABELS = 4'd4;
    localparam S_ALLOC_REQ      = 4'd5;
    localparam S_ALLOC_WAIT     = 4'd6;
    localparam S_UNION_WAIT     = 4'd7;
    localparam S_WRITE_CURR     = 4'd8;
    localparam S_FINISH_ROW     = 4'd9;
    localparam S_COMMIT_WAIT    = 4'd10;

    reg [3:0] state;

    reg [ADDR_WIDTH-1:0] curr_idx;
    // One bit wider than the RAM address so MAX_RUN itself is representable.
    // Otherwise a full table (for example 4 entries with ADDR_WIDTH=2)
    // wraps 3 -> 0 and the matcher repeatedly reads the previous row.
    reg [ADDR_WIDTH:0]   prev_issue_count;
    reg [ADDR_WIDTH:0]   prev_receive_count;
    reg [ADDR_WIDTH:0]   raw_count_latched;
    reg [ADDR_WIDTH:0]   prev_count_latched;
    reg [Y_WIDTH-1:0]    current_y;

    reg [X_WIDTH-1:0] curr_start_reg;
    reg [X_WIDTH-1:0] curr_end_reg;
    reg [MAX_LABEL-1:0] match_label_bitmap;
    // Largest overlapping raw label; union roots do not change scan order.
    reg [LABEL_WIDTH-1:0] match_label_limit;
    reg [LABEL_WIDTH:0] label_scan_index;
    reg [LABEL_WIDTH-1:0] base_label;
    reg [LABEL_WIDTH-1:0] final_label;
    reg final_label_is_new;

    wire prev_request_active;
    wire runs_touch_8n;

    assign raw_rd_req = (state == S_LOAD_CURR_REQ);
    assign raw_rd_idx = curr_idx;

    assign prev_request_active =
        (state == S_SCAN_PREV) &&
        (prev_issue_count < prev_count_latched);
    assign prev_rd_req = prev_request_active;
    assign prev_rd_idx = prev_issue_count[ADDR_WIDTH-1:0];

    assign runs_touch_8n =
        ({1'b0, curr_start_reg} <= ({1'b0, prev_rd_end} + 1'b1)) &&
        ({1'b0, prev_rd_start} <= ({1'b0, curr_end_reg} + 1'b1));

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state                    <= S_IDLE;
            curr_idx                 <= {ADDR_WIDTH{1'b0}};
            prev_issue_count         <= {(ADDR_WIDTH+1){1'b0}};
            prev_receive_count       <= {(ADDR_WIDTH+1){1'b0}};
            raw_count_latched        <= {(ADDR_WIDTH+1){1'b0}};
            prev_count_latched       <= {(ADDR_WIDTH+1){1'b0}};
            current_y                <= {Y_WIDTH{1'b0}};
            curr_start_reg           <= {X_WIDTH{1'b0}};
            curr_end_reg             <= {X_WIDTH{1'b0}};
            match_label_bitmap       <= {MAX_LABEL{1'b0}};
            match_label_limit        <= {LABEL_WIDTH{1'b0}};
            label_scan_index         <= {{LABEL_WIDTH{1'b0}}, 1'b1};
            base_label               <= {LABEL_WIDTH{1'b0}};
            final_label              <= {LABEL_WIDTH{1'b0}};
            final_label_is_new       <= 1'b0;

            raw_release              <= 1'b0;
            curr_wr_en               <= 1'b0;
            curr_wr_start            <= {X_WIDTH{1'b0}};
            curr_wr_end              <= {X_WIDTH{1'b0}};
            curr_wr_label            <= {LABEL_WIDTH{1'b0}};
            row_commit               <= 1'b0;
            alloc_req                <= 1'b0;
            union_req                <= 1'b0;
            union_a                  <= {LABEL_WIDTH{1'b0}};
            union_b                  <= {LABEL_WIDTH{1'b0}};
            feature_update_valid     <= 1'b0;
            feature_update_new_label <= 1'b0;
            feature_update_label     <= {LABEL_WIDTH{1'b0}};
            feature_update_start     <= {X_WIDTH{1'b0}};
            feature_update_end       <= {X_WIDTH{1'b0}};
            feature_update_y         <= {Y_WIDTH{1'b0}};

            busy                     <= 1'b0;
            row_done                 <= 1'b0;
            row_match_cycle_count    <= 32'd0;
            row_match_cycle_max      <= 32'd0;
            matcher_error            <= 1'b0;
        end else if (frame_clear) begin
            state                    <= S_IDLE;
            match_label_limit        <= {LABEL_WIDTH{1'b0}};
            raw_release              <= 1'b0;
            curr_wr_en               <= 1'b0;
            row_commit               <= 1'b0;
            alloc_req                <= 1'b0;
            union_req                <= 1'b0;
            feature_update_valid     <= 1'b0;
            feature_update_new_label <= 1'b0;
            busy                     <= 1'b0;
            row_done                 <= 1'b0;
            row_match_cycle_count    <= 32'd0;
            row_match_cycle_max      <= 32'd0;
            matcher_error            <= 1'b0;
        end else begin
            raw_release              <= 1'b0;
            curr_wr_en               <= 1'b0;
            row_commit               <= 1'b0;
            alloc_req                <= 1'b0;
            union_req                <= 1'b0;
            feature_update_valid     <= 1'b0;
            feature_update_new_label <= 1'b0;
            row_done                 <= 1'b0;

            if (busy)
                row_match_cycle_count <= row_match_cycle_count + 1'b1;

            if ((state != S_IDLE) && start)
                matcher_error <= 1'b1;

            case (state)
                S_IDLE: begin
                    busy <= 1'b0;
                    if (start) begin
                        if (!raw_locked || (raw_run_count > MAX_RUN) ||
                            (prev_count > MAX_RUN)) begin
                            matcher_error <= 1'b1;
                        end else begin
                            busy                  <= 1'b1;
                            row_match_cycle_count <= 32'd0;
                            raw_count_latched     <= raw_run_count;
                            prev_count_latched    <= prev_count;
                            current_y             <= raw_row_y;
                            curr_idx              <= {ADDR_WIDTH{1'b0}};
                            if (raw_run_count == 0)
                                state <= S_FINISH_ROW;
                            else
                                state <= S_LOAD_CURR_REQ;
                        end
                    end
                end

                S_LOAD_CURR_REQ: begin
                    state <= S_LOAD_CURR_WAIT;
                end

                S_LOAD_CURR_WAIT: begin
                    if (raw_rd_valid) begin
                        if (raw_rd_start > raw_rd_end) begin
                            matcher_error <= 1'b1;
                            state         <= S_FINISH_ROW;
                        end else begin
                            curr_start_reg     <= raw_rd_start;
                            curr_end_reg       <= raw_rd_end;
                            match_label_bitmap <= {MAX_LABEL{1'b0}};
                            match_label_limit  <= {LABEL_WIDTH{1'b0}};
                            prev_issue_count   <= {(ADDR_WIDTH+1){1'b0}};
                            prev_receive_count <= {(ADDR_WIDTH+1){1'b0}};
                            label_scan_index   <= {{LABEL_WIDTH{1'b0}}, 1'b1};
                            base_label         <= {LABEL_WIDTH{1'b0}};

                            if (prev_count_latched == 0)
                                state <= S_RESOLVE_LABELS;
                            else
                                state <= S_SCAN_PREV;
                        end
                    end
                end

                S_SCAN_PREV: begin
                    if (prev_request_active)
                        prev_issue_count <= prev_issue_count + 1'b1;

                    if (prev_rd_valid) begin
                        if ((prev_rd_label == {LABEL_WIDTH{1'b0}}) ||
                            (prev_rd_label > MAX_LABEL)) begin
                            matcher_error <= 1'b1;
                        end else if (runs_touch_8n) begin
                            match_label_bitmap[prev_rd_label-1'b1] <= 1'b1;
                            if (prev_rd_label > match_label_limit)
                                match_label_limit <= prev_rd_label;
                        end

                        prev_receive_count <= prev_receive_count + 1'b1;
                        if ((prev_receive_count + 1'b1) >= prev_count_latched) begin
                            label_scan_index <= {{LABEL_WIDTH{1'b0}}, 1'b1};
                            base_label       <= {LABEL_WIDTH{1'b0}};
                            state            <= S_RESOLVE_LABELS;
                        end
                    end
                end

                S_RESOLVE_LABELS: begin
                    // Last previous-row return is visible on this next clock.
                    if (label_scan_index > {1'b0, match_label_limit}) begin
                        if (base_label == {LABEL_WIDTH{1'b0}}) begin
                            state <= S_ALLOC_REQ;
                        end else begin
                            final_label        <= base_label;
                            final_label_is_new <= 1'b0;
                            state              <= S_WRITE_CURR;
                        end
                    end else if (match_label_bitmap[label_scan_index-1'b1]) begin
                        if (base_label == {LABEL_WIDTH{1'b0}}) begin
                            base_label       <= label_scan_index[LABEL_WIDTH-1:0];
                            label_scan_index <= label_scan_index + 1'b1;
                        end else begin
                            union_req <= 1'b1;
                            union_a   <= base_label;
                            union_b   <= label_scan_index[LABEL_WIDTH-1:0];
                            state     <= S_UNION_WAIT;
                        end
                    end else begin
                        label_scan_index <= label_scan_index + 1'b1;
                    end
                end

                S_ALLOC_REQ: begin
                    alloc_req <= 1'b1;
                    state     <= S_ALLOC_WAIT;
                end

                S_ALLOC_WAIT: begin
                    if (alloc_done) begin
                        if (alloc_label == {LABEL_WIDTH{1'b0}}) begin
                            matcher_error <= 1'b1;
                            state         <= S_FINISH_ROW;
                        end else begin
                            final_label        <= alloc_label;
                            final_label_is_new <= 1'b1;
                            state              <= S_WRITE_CURR;
                        end
                    end
                end

                S_UNION_WAIT: begin
                    if (union_done) begin
                        if (union_root == {LABEL_WIDTH{1'b0}}) begin
                            matcher_error <= 1'b1;
                            state         <= S_FINISH_ROW;
                        end else begin
                            base_label       <= union_root;
                            label_scan_index <= label_scan_index + 1'b1;
                            state            <= S_RESOLVE_LABELS;
                        end
                    end
                end

                S_WRITE_CURR: begin
                    curr_wr_en    <= 1'b1;
                    curr_wr_start <= curr_start_reg;
                    curr_wr_end   <= curr_end_reg;
                    curr_wr_label <= final_label;

                    feature_update_valid     <= 1'b1;
                    feature_update_new_label <= final_label_is_new;
                    feature_update_label     <= final_label;
                    feature_update_start     <= curr_start_reg;
                    feature_update_end       <= curr_end_reg;
                    feature_update_y         <= current_y;

                    if (({1'b0, curr_idx} + 1'b1) >= raw_count_latched) begin
                        state <= S_FINISH_ROW;
                    end else begin
                        curr_idx <= curr_idx + 1'b1;
                        state    <= S_LOAD_CURR_REQ;
                    end
                end

                S_FINISH_ROW: begin
                    row_commit  <= 1'b1;
                    raw_release <= 1'b1;
                    state       <= S_COMMIT_WAIT;
                end

                S_COMMIT_WAIT: begin
                    busy     <= 1'b0;
                    row_done <= 1'b1;
                    if (row_match_cycle_count > row_match_cycle_max)
                        row_match_cycle_max <= row_match_cycle_count;
                    state <= S_IDLE;
                end

                default: begin
                    state         <= S_IDLE;
                    busy          <= 1'b0;
                    matcher_error <= 1'b1;
                end
            endcase
        end
    end

endmodule
