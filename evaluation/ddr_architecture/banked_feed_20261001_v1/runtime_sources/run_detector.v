module run_detector #(
    parameter X_WIDTH    = 8,
    parameter Y_WIDTH    = 8,
    parameter LINE_WIDTH = 256,
    parameter MIN_RUN_LENGTH = 2
)(
    input  wire                   clk,
    input  wire                   rst_n,

    input  wire                   valid,
    input  wire                   mask,
    input  wire [X_WIDTH-1:0]     x,
    input  wire [Y_WIDTH-1:0]     y,
    input  wire                   sof,
    input  wire                   eol,
    input  wire                   eof,

    output reg                    run_valid,
    output reg  [X_WIDTH-1:0]     run_x_start,
    output reg  [X_WIDTH-1:0]     run_x_end,
    output reg  [Y_WIDTH-1:0]     run_y,

    output reg                    row_end,
    output reg  [Y_WIDTH-1:0]     row_end_y,
    output wire                   line_end,
    output reg                    frame_end,
    output reg                    protocol_error
);

    reg                   inside_run;
    reg [X_WIDTH-1:0]     run_start_x;
    reg [X_WIDTH-1:0]     last_valid_x;
    reg [Y_WIDTH-1:0]     current_y;
    reg                   row_seen_valid;
    reg                   row_end_pending;
    reg [Y_WIDTH-1:0]     pending_row_y;
    reg                   frame_end_pending;

    wire [X_WIDTH:0] expected_x;
    wire [X_WIDTH:0] closed_run_length;
    wire [X_WIDTH:0] tail_run_length;
    assign expected_x = {1'b0, last_valid_x} + 1'b1;
    assign closed_run_length = {1'b0, x} - {1'b0, run_start_x};
    assign tail_run_length = {1'b0, last_valid_x} -
                             {1'b0, run_start_x} + 1'b1;
    assign line_end   = row_end;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            inside_run       <= 1'b0;
            run_start_x       <= {X_WIDTH{1'b0}};
            last_valid_x      <= {X_WIDTH{1'b0}};
            current_y         <= {Y_WIDTH{1'b0}};
            row_seen_valid    <= 1'b0;
            row_end_pending   <= 1'b0;
            pending_row_y     <= {Y_WIDTH{1'b0}};
            frame_end_pending <= 1'b0;

            run_valid         <= 1'b0;
            run_x_start       <= {X_WIDTH{1'b0}};
            run_x_end         <= {X_WIDTH{1'b0}};
            run_y             <= {Y_WIDTH{1'b0}};
            row_end           <= 1'b0;
            row_end_y         <= {Y_WIDTH{1'b0}};
            frame_end         <= 1'b0;
            protocol_error    <= 1'b0;
        end else begin
            run_valid <= 1'b0;
            row_end   <= 1'b0;
            frame_end <= 1'b0;

            // A row ending with foreground emits its final Run on EOL.
            // row_end follows one clock later, so ordering is unambiguous.
            if (row_end_pending) begin
                row_end         <= 1'b1;
                row_end_y       <= pending_row_y;
                row_end_pending <= 1'b0;
            end

            // EOF is converted to a clean pulse after any pending row_end.
            if (frame_end_pending && !row_end_pending) begin
                frame_end         <= 1'b1;
                frame_end_pending <= 1'b0;
            end

            if (sof) begin
                if (inside_run || row_seen_valid || row_end_pending)
                    protocol_error <= 1'b1;
                inside_run     <= 1'b0;
                row_seen_valid <= 1'b0;
            end

            if (valid) begin
                if (eol || eof || row_end_pending)
                    protocol_error <= 1'b1;

                if (!row_seen_valid) begin
                    if (x != {X_WIDTH{1'b0}})
                        protocol_error <= 1'b1;
                    current_y      <= y;
                    row_seen_valid <= 1'b1;
                end else begin
                    if (y != current_y)
                        protocol_error <= 1'b1;
                    if ({1'b0, x} != expected_x)
                        protocol_error <= 1'b1;
                end

                last_valid_x <= x;

                if (!inside_run && mask) begin
                    run_start_x <= x;
                    inside_run  <= 1'b1;
                end else if (inside_run && !mask) begin
                    if (closed_run_length >= MIN_RUN_LENGTH) begin
                        run_valid   <= 1'b1;
                        run_x_start <= run_start_x;
                        run_x_end   <= x - 1'b1;
                        run_y       <= y;
                    end
                    inside_run  <= 1'b0;
                end
            end

            if (eol) begin
                if (valid || eof || row_end_pending)
                    protocol_error <= 1'b1;

                if (!row_seen_valid)
                    protocol_error <= 1'b1;
                else if (last_valid_x != LINE_WIDTH-1)
                    protocol_error <= 1'b1;

                if (inside_run) begin
                    if (tail_run_length >= MIN_RUN_LENGTH) begin
                        run_valid       <= 1'b1;
                        run_x_start     <= run_start_x;
                        run_x_end       <= last_valid_x;
                        run_y           <= current_y;
                        row_end_pending <= 1'b1;
                        pending_row_y   <= current_y;
                    end else begin
                        row_end   <= 1'b1;
                        row_end_y <= current_y;
                    end
                    inside_run <= 1'b0;
                end else begin
                    row_end   <= 1'b1;
                    row_end_y <= current_y;
                end

                row_seen_valid <= 1'b0;
            end

            if (eof) begin
                if (valid || eol || inside_run || row_seen_valid)
                    protocol_error <= 1'b1;
                frame_end_pending <= 1'b1;
            end
        end
    end

endmodule
