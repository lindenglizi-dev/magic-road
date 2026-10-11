`timescale 1ns/1ps

// Two-bank pixel-line cache for isolated DDR/CCL experiments.
module ccl_pixel_line_banks #(
    parameter WIDTH = 129,
    parameter X_WIDTH = 8,
    parameter Y_WIDTH = 8,
    parameter ID_WIDTH = 32
)(
    input wire clk,
    input wire rst_n,
    input wire cancel,
    input wire in_valid,
    output wire in_ready,
    input wire [ID_WIDTH-1:0] in_task_id,
    input wire [Y_WIDTH-1:0] in_y,
    input wire in_pixel,
    input wire in_last,
    input wire in_frame_last,
    output wire out_valid,
    input wire out_ready,
    output wire [ID_WIDTH-1:0] out_task_id,
    output wire [Y_WIDTH-1:0] out_y,
    output wire [X_WIDTH-1:0] out_x,
    output wire out_pixel,
    output wire out_last,
    output wire out_frame_last,
    output wire empty,
    output reg protocol_error
);
    localparam BANK_EMPTY = 2'd0;
    localparam BANK_FILL = 2'd1;
    localparam BANK_FULL = 2'd2;
    localparam BANK_READ = 2'd3;

    reg pixel_mem [0:(2*WIDTH)-1];
    reg [1:0] bank_state [0:1];
    reg [ID_WIDTH-1:0] bank_task_id [0:1];
    reg [Y_WIDTH-1:0] bank_y [0:1];
    reg bank_frame_last [0:1];
    reg [X_WIDTH-1:0] fill_x [0:1];
    reg write_bank;
    reg read_bank;
    reg [X_WIDTH:0] read_x;

    reg read_pending;
    reg [X_WIDTH:0] pending_address;
    reg pending_bank;
    reg [ID_WIDTH-1:0] pending_task_id;
    reg [Y_WIDTH-1:0] pending_y;
    reg [X_WIDTH-1:0] pending_x;
    reg pending_last;
    reg pending_frame_last;

    reg held_valid;
    reg held_bank;
    reg [ID_WIDTH-1:0] held_task_id;
    reg [Y_WIDTH-1:0] held_y;
    reg [X_WIDTH-1:0] held_x;
    reg held_pixel;
    reg held_last;
    reg held_frame_last;

    wire selected_empty;
    wire selected_fill;
    wire input_transfer;
    wire expected_last;
    wire metadata_mismatch;
    wire input_bad;
    wire output_transfer;
    wire output_slot_available;
    wire read_bank_available;
    wire read_request;

    assign selected_empty = bank_state[write_bank] == BANK_EMPTY;
    assign selected_fill = bank_state[write_bank] == BANK_FILL;
    assign in_ready = rst_n && !cancel && (selected_empty || selected_fill);
    assign input_transfer = in_valid && in_ready;
    assign expected_last = fill_x[write_bank] == WIDTH - 1;
    assign metadata_mismatch = selected_fill &&
                               ((in_task_id != bank_task_id[write_bank]) ||
                                (in_y != bank_y[write_bank]));
    assign input_bad = metadata_mismatch || (in_last != expected_last) ||
                       (in_frame_last && !in_last);

    assign out_valid = rst_n && !cancel && held_valid;
    assign out_task_id = held_task_id;
    assign out_y = held_y;
    assign out_x = held_x;
    assign out_pixel = held_pixel;
    assign out_last = held_last;
    assign out_frame_last = held_frame_last;
    assign output_transfer = out_valid && out_ready;

    assign output_slot_available = !held_valid || output_transfer;
    assign read_bank_available = (bank_state[read_bank] == BANK_FULL) ||
                                 (bank_state[read_bank] == BANK_READ);
    assign read_request = !read_pending && output_slot_available &&
                          read_bank_available && (read_x < WIDTH);
    assign empty = (bank_state[0] == BANK_EMPTY) &&
                   (bank_state[1] == BANK_EMPTY) &&
                   !read_pending && !held_valid;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            bank_state[0] <= BANK_EMPTY;
            bank_state[1] <= BANK_EMPTY;
            bank_task_id[0] <= {ID_WIDTH{1'b0}};
            bank_task_id[1] <= {ID_WIDTH{1'b0}};
            bank_y[0] <= {Y_WIDTH{1'b0}};
            bank_y[1] <= {Y_WIDTH{1'b0}};
            bank_frame_last[0] <= 1'b0;
            bank_frame_last[1] <= 1'b0;
            fill_x[0] <= {X_WIDTH{1'b0}};
            fill_x[1] <= {X_WIDTH{1'b0}};
            write_bank <= 1'b0;
            read_bank <= 1'b0;
            read_x <= {(X_WIDTH+1){1'b0}};
            read_pending <= 1'b0;
            pending_address <= {(X_WIDTH+1){1'b0}};
            pending_bank <= 1'b0;
            pending_task_id <= {ID_WIDTH{1'b0}};
            pending_y <= {Y_WIDTH{1'b0}};
            pending_x <= {X_WIDTH{1'b0}};
            pending_last <= 1'b0;
            pending_frame_last <= 1'b0;
            held_valid <= 1'b0;
            held_bank <= 1'b0;
            held_task_id <= {ID_WIDTH{1'b0}};
            held_y <= {Y_WIDTH{1'b0}};
            held_x <= {X_WIDTH{1'b0}};
            held_pixel <= 1'b0;
            held_last <= 1'b0;
            held_frame_last <= 1'b0;
            protocol_error <= 1'b0;
        end else if (cancel) begin
            bank_state[0] <= BANK_EMPTY;
            bank_state[1] <= BANK_EMPTY;
            fill_x[0] <= {X_WIDTH{1'b0}};
            fill_x[1] <= {X_WIDTH{1'b0}};
            write_bank <= 1'b0;
            read_bank <= 1'b0;
            read_x <= {(X_WIDTH+1){1'b0}};
            read_pending <= 1'b0;
            held_valid <= 1'b0;
        end else begin
            if (input_transfer) begin
                pixel_mem[(write_bank ? WIDTH : 0) + fill_x[write_bank]] <= in_pixel;
                if (selected_empty) begin
                    bank_task_id[write_bank] <= in_task_id;
                    bank_y[write_bank] <= in_y;
                    bank_frame_last[write_bank] <= 1'b0;
                end
                if (input_bad) begin
                    protocol_error <= 1'b1;
                    bank_state[write_bank] <= BANK_EMPTY;
                    fill_x[write_bank] <= {X_WIDTH{1'b0}};
                end else if (in_last) begin
                    bank_state[write_bank] <= BANK_FULL;
                    bank_frame_last[write_bank] <= in_frame_last;
                    fill_x[write_bank] <= {X_WIDTH{1'b0}};
                    write_bank <= !write_bank;
                end else begin
                    bank_state[write_bank] <= BANK_FILL;
                    fill_x[write_bank] <= fill_x[write_bank] + 1'b1;
                end
            end

            if (output_transfer) begin
                held_valid <= 1'b0;
                if (held_last) begin
                    bank_state[held_bank] <= BANK_EMPTY;
                    read_bank <= !read_bank;
                    read_x <= {(X_WIDTH+1){1'b0}};
                end
            end

            if (read_pending) begin
                held_valid <= 1'b1;
                held_bank <= pending_bank;
                held_task_id <= pending_task_id;
                held_y <= pending_y;
                held_x <= pending_x;
                held_pixel <= pixel_mem[pending_address];
                held_last <= pending_last;
                held_frame_last <= pending_frame_last;
                read_pending <= 1'b0;
            end

            if (read_request) begin
                bank_state[read_bank] <= BANK_READ;
                pending_address <= (read_bank ? WIDTH : 0) + read_x;
                pending_bank <= read_bank;
                pending_task_id <= bank_task_id[read_bank];
                pending_y <= bank_y[read_bank];
                pending_x <= read_x[X_WIDTH-1:0];
                pending_last <= read_x == WIDTH - 1;
                pending_frame_last <= bank_frame_last[read_bank] &&
                                      (read_x == WIDTH - 1);
                read_pending <= 1'b1;
                read_x <= read_x + 1'b1;
            end
        end
    end
endmodule
