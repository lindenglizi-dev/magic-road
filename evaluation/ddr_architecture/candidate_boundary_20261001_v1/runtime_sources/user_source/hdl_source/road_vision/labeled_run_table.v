module labeled_run_table #(
    parameter X_WIDTH     = 8,
    parameter LABEL_WIDTH = 6,
    parameter ADDR_WIDTH  = 6,
    parameter MAX_RUN     = 64
)(
    input  wire                     clk,
    input  wire                     rst_n,

    input  wire                     frame_clear,
    input  wire                     row_commit,

    input  wire                     curr_wr_en,
    input  wire [X_WIDTH-1:0]       curr_wr_start,
    input  wire [X_WIDTH-1:0]       curr_wr_end,
    input  wire [LABEL_WIDTH-1:0]   curr_wr_label,

    input  wire                     prev_rd_req,
    input  wire [ADDR_WIDTH-1:0]    prev_rd_idx,
    output reg                      prev_rd_valid,
    output reg  [X_WIDTH-1:0]       prev_rd_start,
    output reg  [X_WIDTH-1:0]       prev_rd_end,
    output reg  [LABEL_WIDTH-1:0]   prev_rd_label,

    output reg  [ADDR_WIDTH:0]      prev_count,
    output reg  [ADDR_WIDTH:0]      curr_count,
    output reg                      prev_bank_sel,
    output wire                     curr_bank_sel,

    output reg                      labeled_overflow,
    output reg                      protocol_error
);

    reg [X_WIDTH-1:0]     start_mem_a [0:MAX_RUN-1];
    reg [X_WIDTH-1:0]     end_mem_a   [0:MAX_RUN-1];
    reg [LABEL_WIDTH-1:0] label_mem_a [0:MAX_RUN-1];

    reg [X_WIDTH-1:0]     start_mem_b [0:MAX_RUN-1];
    reg [X_WIDTH-1:0]     end_mem_b   [0:MAX_RUN-1];
    reg [LABEL_WIDTH-1:0] label_mem_b [0:MAX_RUN-1];

    assign curr_bank_sel = ~prev_bank_sel;

    // Prev bank uses synchronous read. A valid request returns one entry
    // after the active clock edge. Out-of-range requests return no valid data.
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            prev_rd_valid <= 1'b0;
            prev_rd_start <= {X_WIDTH{1'b0}};
            prev_rd_end   <= {X_WIDTH{1'b0}};
            prev_rd_label <= {LABEL_WIDTH{1'b0}};
        end else if (frame_clear) begin
            prev_rd_valid <= 1'b0;
            prev_rd_start <= {X_WIDTH{1'b0}};
            prev_rd_end   <= {X_WIDTH{1'b0}};
            prev_rd_label <= {LABEL_WIDTH{1'b0}};
        end else begin
            prev_rd_valid <= 1'b0;

            if (prev_rd_req && ({1'b0, prev_rd_idx} < prev_count)) begin
                if (prev_bank_sel == 1'b0) begin
                    prev_rd_start <= start_mem_a[prev_rd_idx];
                    prev_rd_end   <= end_mem_a[prev_rd_idx];
                    prev_rd_label <= label_mem_a[prev_rd_idx];
                end else begin
                    prev_rd_start <= start_mem_b[prev_rd_idx];
                    prev_rd_end   <= end_mem_b[prev_rd_idx];
                    prev_rd_label <= label_mem_b[prev_rd_idx];
                end
                prev_rd_valid <= 1'b1;
            end
        end
    end

    // Control priority: frame_clear, row_commit, current-entry write.
    // Memory contents are not cleared. Counts define which entries are valid.
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            prev_count       <= {(ADDR_WIDTH+1){1'b0}};
            curr_count       <= {(ADDR_WIDTH+1){1'b0}};
            prev_bank_sel    <= 1'b0;
            labeled_overflow <= 1'b0;
            protocol_error   <= 1'b0;
        end else if (frame_clear) begin
            prev_count       <= {(ADDR_WIDTH+1){1'b0}};
            curr_count       <= {(ADDR_WIDTH+1){1'b0}};
            prev_bank_sel    <= 1'b0;
            labeled_overflow <= 1'b0;
            protocol_error   <= 1'b0;
        end else begin
            if (row_commit && (curr_wr_en || prev_rd_req)) begin
                protocol_error <= 1'b1;
            end

            if (row_commit) begin
                prev_count    <= curr_count;
                curr_count    <= {(ADDR_WIDTH+1){1'b0}};
                prev_bank_sel <= ~prev_bank_sel;
            end else if (curr_wr_en) begin
                if (curr_wr_label == {LABEL_WIDTH{1'b0}}) begin
                    protocol_error <= 1'b1;
                end else if (curr_count < MAX_RUN) begin
                    if (curr_bank_sel == 1'b0) begin
                        start_mem_a[curr_count[ADDR_WIDTH-1:0]] <= curr_wr_start;
                        end_mem_a[curr_count[ADDR_WIDTH-1:0]]   <= curr_wr_end;
                        label_mem_a[curr_count[ADDR_WIDTH-1:0]] <= curr_wr_label;
                    end else begin
                        start_mem_b[curr_count[ADDR_WIDTH-1:0]] <= curr_wr_start;
                        end_mem_b[curr_count[ADDR_WIDTH-1:0]]   <= curr_wr_end;
                        label_mem_b[curr_count[ADDR_WIDTH-1:0]] <= curr_wr_label;
                    end
                    curr_count <= curr_count + 1'b1;
                end else begin
                    labeled_overflow <= 1'b1;
                end
            end
        end
    end

endmodule
