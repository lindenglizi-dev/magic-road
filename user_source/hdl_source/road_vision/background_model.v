module background_model #(
    parameter X_WIDTH       = 8,
    parameter Y_WIDTH       = 8,
    parameter ADDR_WIDTH    = 16,
    parameter FRAME_WIDTH   = 256,
    parameter FRAME_HEIGHT  = 150,
    parameter LEARN_FRAMES  = 4,
    parameter LEARN_SHIFT   = 2,
    parameter UPDATE_SHIFT  = 4
)(
    input  wire                    clk,
    input  wire                    rst_n,

    input  wire                    in_valid,
    input  wire [7:0]              in_gray,
    input  wire [X_WIDTH-1:0]      in_x,
    input  wire [Y_WIDTH-1:0]      in_y,
    input  wire                    in_sof,
    input  wire                    in_eol,
    input  wire                    in_eof,

    input  wire [7:0]              diff_threshold,
    input  wire                    update_enable,
    input  wire                    freeze_foreground,
    input  wire                    relearn,

    output reg                     out_valid,
    output reg  [7:0]              out_gray,
    output reg                     out_mask,
    output reg  [7:0]              out_diff,
    output reg  [7:0]              out_background,
    output reg  [X_WIDTH-1:0]      out_x,
    output reg  [Y_WIDTH-1:0]      out_y,
    output reg                     out_sof,
    output reg                     out_eol,
    output reg                     out_eof,

    output reg                     learning,
    output reg                     background_ready,
    output reg  [7:0]              learned_frame_count,
    output reg                     protocol_error
);

    localparam FRAME_PIXELS = FRAME_WIDTH * FRAME_HEIGHT;

    // The comment is recognized by TD's front end; the attribute keeps the
    // intended implementation explicit for other synthesis tools.
    (* ram_style = "block" *)
    reg [7:0] background_mem [0:FRAME_PIXELS-1]; /* fehdl force_ram=1, ram_style="bram_fast" */

    reg [7:0] ram_q;
    reg [ADDR_WIDTH:0] pixel_count;
    reg frame_active;
    reg frame_bad;
    reg [X_WIDTH:0] expected_x;
    reg [Y_WIDTH:0] expected_y;
    reg relearn_pending;

    reg p_valid;
    reg [7:0] p_gray;
    reg [ADDR_WIDTH-1:0] p_addr;
    reg [X_WIDTH-1:0] p_x;
    reg [Y_WIDTH-1:0] p_y;
    reg p_sof;
    reg p_eol;
    reg p_eof;
    reg p_relearn_start;
    reg [7:0] p_diff_threshold;
    reg p_update_enable;
    reg p_freeze_foreground;
    reg p_frame_good;

    reg calc_valid;
    reg [7:0] calc_gray;
    reg [7:0] calc_background;
    reg [7:0] calc_diff;
    reg [ADDR_WIDTH-1:0] calc_addr;
    reg [X_WIDTH-1:0] calc_x;
    reg [Y_WIDTH-1:0] calc_y;
    reg calc_sof;
    reg calc_eol;
    reg calc_eof;
    reg calc_relearn_start;
    reg [7:0] calc_diff_threshold;
    reg calc_update_enable;
    reg calc_freeze_foreground;
    reg calc_frame_good;

    reg write_valid;
    reg [ADDR_WIDTH-1:0] write_addr;
    reg [7:0] write_data;

    wire [ADDR_WIDTH-1:0] input_addr;
    wire sof_fault;
    wire data_fault;
    wire eol_fault;
    wire eof_fault;
    wire input_fault_now;
    wire input_cycle_good;
    wire foreground_now;

    // The deployed 256-pixel line maps directly to {y,x}; no multiplier or
    // drifting stream counter is needed. The generic branch keeps small unit
    // tests and alternative frame widths usable.
    generate
        if ((FRAME_WIDTH == 256) && (X_WIDTH == 8) &&
            (Y_WIDTH == 8) && (ADDR_WIDTH == 16)) begin : g_addr_256
            assign input_addr = {in_y, in_x};
        end else begin : g_addr_generic
            assign input_addr = (in_y * FRAME_WIDTH) + in_x;
        end
    endgenerate

    assign sof_fault = in_sof &&
                       (!in_valid || in_eol || in_eof || frame_active ||
                        (in_x != 0) || (in_y != 0));
    assign data_fault = in_valid && !in_sof &&
                        (!frame_active || in_eol || in_eof ||
                         ({1'b0, in_x} != expected_x) ||
                         ({1'b0, in_y} != expected_y) ||
                         ({1'b0, in_x} >= FRAME_WIDTH) ||
                         ({1'b0, in_y} >= FRAME_HEIGHT));
    assign eol_fault = in_eol &&
                       (in_valid || in_eof || !frame_active ||
                        (expected_x != FRAME_WIDTH) ||
                        (expected_y >= FRAME_HEIGHT));
    assign eof_fault = in_eof &&
                       (in_valid || in_eol || !frame_active ||
                        (expected_x != 0) ||
                        (expected_y != FRAME_HEIGHT) ||
                        (pixel_count != FRAME_PIXELS));
    assign input_fault_now = sof_fault || data_fault ||
                             eol_fault || eof_fault;
    assign input_cycle_good = in_sof ? !sof_fault :
                              (!frame_bad && !input_fault_now);
    assign foreground_now = (calc_diff >= calc_diff_threshold);

    function [7:0] learn_toward;
        input [7:0] old_value;
        input [7:0] new_value;
        reg [8:0] delta;
        begin
            if (new_value > old_value) begin
                delta = ({1'b0, new_value} - {1'b0, old_value}) >>
                        LEARN_SHIFT;
                if (delta == 0)
                    delta = 1;
                learn_toward = old_value + delta[7:0];
            end else if (new_value < old_value) begin
                delta = ({1'b0, old_value} - {1'b0, new_value}) >>
                        LEARN_SHIFT;
                if (delta == 0)
                    delta = 1;
                learn_toward = old_value - delta[7:0];
            end else begin
                learn_toward = old_value;
            end
        end
    endfunction

    function [7:0] update_toward;
        input [7:0] old_value;
        input [7:0] new_value;
        reg [8:0] delta;
        begin
            if (new_value > old_value) begin
                delta = ({1'b0, new_value} - {1'b0, old_value}) >>
                        UPDATE_SHIFT;
                if (delta == 0)
                    delta = 1;
                update_toward = old_value + delta[7:0];
            end else if (new_value < old_value) begin
                delta = ({1'b0, old_value} - {1'b0, new_value}) >>
                        UPDATE_SHIFT;
                if (delta == 0)
                    delta = 1;
                update_toward = old_value - delta[7:0];
            end else begin
                update_toward = old_value;
            end
        end
    endfunction

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            ram_q            <= 8'd0;
            pixel_count      <= {(ADDR_WIDTH+1){1'b0}};
            frame_active     <= 1'b0;
            frame_bad        <= 1'b0;
            expected_x       <= {(X_WIDTH+1){1'b0}};
            expected_y       <= {(Y_WIDTH+1){1'b0}};
            relearn_pending  <= 1'b0;
            p_valid          <= 1'b0;
            p_gray           <= 8'd0;
            p_addr           <= {ADDR_WIDTH{1'b0}};
            p_x              <= {X_WIDTH{1'b0}};
            p_y              <= {Y_WIDTH{1'b0}};
            p_sof            <= 1'b0;
            p_eol            <= 1'b0;
            p_eof            <= 1'b0;
            p_relearn_start  <= 1'b0;
            p_diff_threshold <= 8'd0;
            p_update_enable  <= 1'b0;
            p_freeze_foreground <= 1'b0;
            p_frame_good     <= 1'b0;
            calc_valid       <= 1'b0;
            calc_gray        <= 8'd0;
            calc_background  <= 8'd0;
            calc_diff        <= 8'd0;
            calc_addr        <= {ADDR_WIDTH{1'b0}};
            calc_x           <= {X_WIDTH{1'b0}};
            calc_y           <= {Y_WIDTH{1'b0}};
            calc_sof         <= 1'b0;
            calc_eol         <= 1'b0;
            calc_eof         <= 1'b0;
            calc_relearn_start <= 1'b0;
            calc_diff_threshold <= 8'd0;
            calc_update_enable <= 1'b0;
            calc_freeze_foreground <= 1'b0;
            calc_frame_good  <= 1'b0;
            protocol_error   <= 1'b0;
        end else begin
            p_valid         <= in_valid;
            p_gray          <= in_gray;
            p_addr          <= input_addr;
            p_x             <= in_x;
            p_y             <= in_y;
            p_sof           <= in_sof;
            p_eol           <= in_eol;
            p_eof           <= in_eof;
            p_relearn_start <= 1'b0;
            p_diff_threshold <= diff_threshold;
            p_update_enable <= update_enable;
            p_freeze_foreground <= freeze_foreground;
            p_frame_good    <= input_cycle_good;

            calc_valid       <= p_valid;
            calc_gray        <= p_gray;
            calc_background  <= ram_q;
            calc_addr        <= p_addr;
            calc_x           <= p_x;
            calc_y           <= p_y;
            calc_sof         <= p_sof;
            calc_eol         <= p_eol;
            calc_eof         <= p_eof;
            calc_relearn_start <= p_relearn_start;
            calc_diff_threshold <= p_diff_threshold;
            calc_update_enable <= p_update_enable;
            calc_freeze_foreground <= p_freeze_foreground;
            calc_frame_good  <= p_frame_good;

            if (p_valid) begin
                if (p_gray >= ram_q)
                    calc_diff <= p_gray - ram_q;
                else
                    calc_diff <= ram_q - p_gray;
            end else begin
                calc_diff <= 8'd0;
            end

            if (relearn)
                relearn_pending <= 1'b1;

            if (in_sof) begin
                protocol_error <= 1'b0;
                frame_bad <= sof_fault;
                if (sof_fault)
                    protocol_error <= 1'b1;
                frame_active <= 1'b1;
                pixel_count  <= {{ADDR_WIDTH{1'b0}}, 1'b1};
                expected_x   <= {{X_WIDTH{1'b0}}, 1'b1};
                expected_y   <= {(Y_WIDTH+1){1'b0}};
                if (relearn || relearn_pending) begin
                    p_relearn_start <= 1'b1;
                    relearn_pending <= 1'b0;
                end
            end else if (in_valid) begin
                if (data_fault) begin
                    protocol_error <= 1'b1;
                    frame_bad <= 1'b1;
                end
                pixel_count <= pixel_count + 1'b1;
                expected_x <= expected_x + 1'b1;
            end

            if (in_valid)
                ram_q <= background_mem[input_addr];

            if (write_valid)
                background_mem[write_addr] <= write_data;

            if (in_eol) begin
                if (eol_fault) begin
                    protocol_error <= 1'b1;
                    frame_bad <= 1'b1;
                end
                expected_x <= {(X_WIDTH+1){1'b0}};
                expected_y <= expected_y + 1'b1;
            end

            if (in_eof) begin
                if (eof_fault) begin
                    protocol_error <= 1'b1;
                    frame_bad <= 1'b1;
                end
                frame_active <= 1'b0;
            end
        end
    end

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            out_valid           <= 1'b0;
            out_gray            <= 8'd0;
            out_mask            <= 1'b0;
            out_diff            <= 8'd0;
            out_background      <= 8'd0;
            out_x               <= {X_WIDTH{1'b0}};
            out_y               <= {Y_WIDTH{1'b0}};
            out_sof             <= 1'b0;
            out_eol             <= 1'b0;
            out_eof             <= 1'b0;
            learning            <= 1'b1;
            background_ready    <= 1'b0;
            learned_frame_count <= 8'd0;
            write_valid         <= 1'b0;
            write_addr          <= {ADDR_WIDTH{1'b0}};
            write_data          <= 8'd0;
        end else begin
            out_valid <= calc_valid;
            out_gray  <= calc_gray;
            out_x     <= calc_x;
            out_y     <= calc_y;
            out_sof   <= calc_sof;
            out_eol   <= calc_eol;
            out_eof   <= calc_eof;
            out_mask  <= 1'b0;
            out_diff  <= 8'd0;
            write_valid <= 1'b0;

            if (calc_relearn_start) begin
                learning            <= 1'b1;
                background_ready    <= 1'b0;
                learned_frame_count <= 8'd0;
            end

            if (calc_valid) begin
                write_addr     <= calc_addr;
                write_data     <= calc_background;
                out_diff       <= calc_diff;
                out_background <= calc_background;

                if (!calc_frame_good) begin
                    // Keep downstream timing intact, but never let a malformed
                    // frame modify the persistent background model.
                    out_mask <= 1'b0;
                end else if (calc_relearn_start || learning) begin
                    out_mask <= 1'b0;
                    if (calc_relearn_start ||
                        (learned_frame_count == 0)) begin
                        write_valid           <= 1'b1;
                        write_data            <= calc_gray;
                        out_background        <= calc_gray;
                        out_diff              <= 8'd0;
                    end else begin
                        write_valid <= 1'b1;
                        write_data  <= learn_toward(calc_background,
                                                    calc_gray);
                    end
                end else begin
                    out_mask <= foreground_now;
                    if (calc_update_enable &&
                        !(calc_freeze_foreground && foreground_now)) begin
                        write_valid <= 1'b1;
                        write_data  <= update_toward(calc_background,
                                                     calc_gray);
                    end
                end
            end

            if (calc_eof && learning && calc_frame_good) begin
                if ((learned_frame_count + 1'b1) >= LEARN_FRAMES) begin
                    learned_frame_count <= LEARN_FRAMES;
                    learning            <= 1'b0;
                    background_ready    <= 1'b1;
                end else begin
                    learned_frame_count <= learned_frame_count + 1'b1;
                end
            end
        end
    end

endmodule
