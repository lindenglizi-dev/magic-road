module raw_run_table #(
    parameter X_WIDTH    = 8,
    parameter Y_WIDTH    = 8,
    parameter ADDR_WIDTH = 6,
    parameter MAX_RUN    = 64
)(
    input  wire                   clk,
    input  wire                   rst_n,
    input  wire                   frame_clear,

    input  wire                   run_valid,
    input  wire [X_WIDTH-1:0]     run_start,
    input  wire [X_WIDTH-1:0]     run_end,
    input  wire                   row_end,
    input  wire [Y_WIDTH-1:0]     row_end_y,

    input  wire                   row_release,

    input  wire                   rd_req,
    input  wire [ADDR_WIDTH-1:0]  rd_idx,
    output reg                    rd_valid,
    output reg  [X_WIDTH-1:0]     rd_start,
    output reg  [X_WIDTH-1:0]     rd_end,

    output wire                   raw_locked,
    output wire [Y_WIDTH-1:0]     raw_row_y,
    output wire [ADDR_WIDTH:0]    raw_run_count,
    output wire                   run_overflow,
    output reg                    raw_overrun,
    output reg                    protocol_error
);

    reg [X_WIDTH-1:0] start_mem_a [0:MAX_RUN-1];
    reg [X_WIDTH-1:0] end_mem_a   [0:MAX_RUN-1];
    reg [X_WIDTH-1:0] start_mem_b [0:MAX_RUN-1];
    reg [X_WIDTH-1:0] end_mem_b   [0:MAX_RUN-1];

    reg [ADDR_WIDTH:0] count_a;
    reg [ADDR_WIDTH:0] count_b;
    reg [Y_WIDTH-1:0] row_y_a;
    reg [Y_WIDTH-1:0] row_y_b;
    reg full_a;
    reg full_b;
    reg overflow_a;
    reg overflow_b;
    reg write_bank;
    reg read_bank;

    wire read_bank_full;
    wire write_bank_full;

    assign read_bank_full  = read_bank ? full_b : full_a;
    assign write_bank_full = write_bank ? full_b : full_a;
    assign raw_locked      = read_bank_full;
    assign raw_row_y       = read_bank ? row_y_b : row_y_a;
    assign raw_run_count   = read_bank ? count_b : count_a;
    assign run_overflow    = overflow_a || overflow_b;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            rd_valid <= 1'b0;
            rd_start <= {X_WIDTH{1'b0}};
            rd_end   <= {X_WIDTH{1'b0}};
        end else if (frame_clear) begin
            rd_valid <= 1'b0;
            rd_start <= {X_WIDTH{1'b0}};
            rd_end   <= {X_WIDTH{1'b0}};
        end else begin
            rd_valid <= 1'b0;
            if (rd_req && raw_locked &&
                ({1'b0, rd_idx} < raw_run_count)) begin
                if (read_bank) begin
                    rd_start <= start_mem_b[rd_idx];
                    rd_end   <= end_mem_b[rd_idx];
                end else begin
                    rd_start <= start_mem_a[rd_idx];
                    rd_end   <= end_mem_a[rd_idx];
                end
                rd_valid <= 1'b1;
            end
        end
    end

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            count_a        <= {(ADDR_WIDTH+1){1'b0}};
            count_b        <= {(ADDR_WIDTH+1){1'b0}};
            row_y_a        <= {Y_WIDTH{1'b0}};
            row_y_b        <= {Y_WIDTH{1'b0}};
            full_a         <= 1'b0;
            full_b         <= 1'b0;
            overflow_a     <= 1'b0;
            overflow_b     <= 1'b0;
            write_bank     <= 1'b0;
            read_bank      <= 1'b0;
            raw_overrun    <= 1'b0;
            protocol_error <= 1'b0;
        end else if (frame_clear) begin
            count_a        <= {(ADDR_WIDTH+1){1'b0}};
            count_b        <= {(ADDR_WIDTH+1){1'b0}};
            row_y_a        <= {Y_WIDTH{1'b0}};
            row_y_b        <= {Y_WIDTH{1'b0}};
            full_a         <= 1'b0;
            full_b         <= 1'b0;
            overflow_a     <= 1'b0;
            overflow_b     <= 1'b0;
            write_bank     <= 1'b0;
            read_bank      <= 1'b0;
            raw_overrun    <= 1'b0;
            protocol_error <= 1'b0;
        end else begin
            if (rd_req && !raw_locked)
                protocol_error <= 1'b1;
            if (row_release && !raw_locked)
                protocol_error <= 1'b1;
            if (run_valid && row_end)
                protocol_error <= 1'b1;

            if (row_release && raw_locked) begin
                if (read_bank) begin
                    full_b     <= 1'b0;
                    count_b    <= {(ADDR_WIDTH+1){1'b0}};
                    overflow_b <= 1'b0;
                end else begin
                    full_a     <= 1'b0;
                    count_a    <= {(ADDR_WIDTH+1){1'b0}};
                    overflow_a <= 1'b0;
                end
                read_bank <= ~read_bank;
            end

            if (run_valid) begin
                if (write_bank_full) begin
                    raw_overrun    <= 1'b1;
                    protocol_error <= 1'b1;
                end else if (run_start > run_end) begin
                    protocol_error <= 1'b1;
                end else if (write_bank) begin
                    if (count_b < MAX_RUN) begin
                        start_mem_b[count_b[ADDR_WIDTH-1:0]] <= run_start;
                        end_mem_b[count_b[ADDR_WIDTH-1:0]]   <= run_end;
                        count_b <= count_b + 1'b1;
                    end else begin
                        overflow_b <= 1'b1;
                    end
                end else begin
                    if (count_a < MAX_RUN) begin
                        start_mem_a[count_a[ADDR_WIDTH-1:0]] <= run_start;
                        end_mem_a[count_a[ADDR_WIDTH-1:0]]   <= run_end;
                        count_a <= count_a + 1'b1;
                    end else begin
                        overflow_a <= 1'b1;
                    end
                end
            end

            if (row_end) begin
                if (write_bank_full) begin
                    raw_overrun    <= 1'b1;
                    protocol_error <= 1'b1;
                end else if (write_bank) begin
                    row_y_b    <= row_end_y;
                    full_b     <= 1'b1;
                    write_bank <= 1'b0;
                    if (!full_a && !(row_release && !read_bank)) begin
                        count_a    <= {(ADDR_WIDTH+1){1'b0}};
                        overflow_a <= 1'b0;
                    end
                end else begin
                    row_y_a    <= row_end_y;
                    full_a     <= 1'b1;
                    write_bank <= 1'b1;
                    if (!full_b && !(row_release && read_bank)) begin
                        count_b    <= {(ADDR_WIDTH+1){1'b0}};
                        overflow_b <= 1'b0;
                    end
                end
            end
        end
    end

endmodule
