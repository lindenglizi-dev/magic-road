`timescale 1ns/1ps

module ddr_roi_byte_reader #(
    parameter FRAME_WIDTH  = 1280,
    parameter FRAME_HEIGHT = 720,
    parameter TASK_WIDTH   = 16,
    parameter FRAME_ID_WIDTH = 16
)(
    input  wire                      clk,
    input  wire                      rst_n,

    input  wire                      start_valid,
    output wire                      start_ready,
    input  wire [TASK_WIDTH-1:0]     start_task_id,
    input  wire [FRAME_ID_WIDTH-1:0] start_frame_id,
    input  wire [31:0]               start_frame_base_byte,
    input  wire [10:0]               start_x0,
    input  wire [9:0]                start_y0,
    input  wire [10:0]               start_x1,
    input  wire [9:0]                start_y1,
    input  wire                      cancel,

    output wire                      rd_req_valid,
    input  wire                      rd_req_ready,
    output wire [31:0]               rd_req_addr_byte,
    output wire [TASK_WIDTH-1:0]     rd_req_task_id,
    output wire [FRAME_ID_WIDTH-1:0] rd_req_frame_id,
    input  wire                      rd_rsp_valid,
    input  wire [127:0]              rd_rsp_data,

    output reg                       roi_valid,
    output reg  [TASK_WIDTH-1:0]     roi_task_id,
    output reg  [FRAME_ID_WIDTH-1:0] roi_frame_id,
    output reg  [4:0]                roi_x,
    output reg  [4:0]                roi_y,
    output reg  [7:0]                roi_gray,
    output reg                       done,
    output reg                       cancel_done,
    output reg                       busy,
    output wire                      drained,
    output wire [1:0]                occupied_count,
    output wire [1:0]                reserved_count,
    output reg                       protocol_error
);

    localparam S_IDLE          = 4'd0;
    localparam S_PREP          = 4'd1;
    localparam S_FIRST_CHECK   = 4'd2;
    localparam S_REQ_FIRST     = 4'd3;
    localparam S_WAIT_FIRST    = 4'd4;
    localparam S_EXTRACT_FIRST = 4'd5;
    localparam S_REQ_SECOND    = 4'd6;
    localparam S_WAIT_SECOND   = 4'd7;
    localparam S_EMIT          = 4'd8;

    reg [3:0] state;
    reg [TASK_WIDTH-1:0] task_id_reg;
    reg [FRAME_ID_WIDTH-1:0] frame_id_reg;
    reg [31:0] frame_base_reg;
    reg [10:0] x0_reg;
    reg [10:0] x1_reg;
    reg [9:0] y0_reg;
    reg [9:0] y1_reg;
    reg [4:0] sample_u;
    reg [4:0] sample_v;

    reg [31:0] first_beat_addr;
    reg [31:0] request_addr_reg;
    reg [3:0] pixel_byte_offset;
    reg [7:0] pixel_r;
    reg [7:0] pixel_g;
    reg [7:0] pixel_b;

    reg pending;
    reg canceling;
    reg [TASK_WIDTH-1:0] accepted_task_id;
    reg [FRAME_ID_WIDTH-1:0] accepted_frame_id;

    reg cache_valid;
    reg [31:0] cache_addr;
    reg [127:0] cache_data;
    reg [31:0] cache_frame_base;
    reg [FRAME_ID_WIDTH-1:0] cache_frame_id;

    wire [31:0] roi_width_calc;
    wire [31:0] roi_height_calc;
    wire [31:0] sample_x_scale;
    wire [31:0] sample_y_scale;
    wire [31:0] source_x_calc;
    wire [31:0] source_y_calc;
    wire [31:0] pixel_index_calc;
    wire [31:0] pixel_byte_addr_calc;
    wire request_accept;
    wire cache_hit;

    assign roi_width_calc = {21'd0, x1_reg} - {21'd0, x0_reg};
    assign roi_height_calc = {22'd0, y1_reg} - {22'd0, y0_reg};
    assign sample_x_scale = roi_width_calc * ({26'd0, sample_u, 1'b0} + 32'd1);
    assign sample_y_scale = roi_height_calc * ({26'd0, sample_v, 1'b0} + 32'd1);
    assign source_x_calc = {21'd0, x0_reg} + (sample_x_scale >> 6);
    assign source_y_calc = {22'd0, y0_reg} + (sample_y_scale >> 6);
    assign pixel_index_calc = source_y_calc * FRAME_WIDTH + source_x_calc;
    assign pixel_byte_addr_calc = frame_base_reg + pixel_index_calc * 3;

    assign start_ready = !busy;
    assign rd_req_valid = ((state == S_REQ_FIRST) || (state == S_REQ_SECOND)) &&
                          !canceling && !cancel;
    assign rd_req_addr_byte = request_addr_reg;
    assign rd_req_task_id = task_id_reg;
    assign rd_req_frame_id = frame_id_reg;
    assign request_accept = rd_req_valid && rd_req_ready;
    assign cache_hit = cache_valid && (cache_addr == first_beat_addr) &&
                       (cache_frame_id == frame_id_reg) &&
                       (cache_frame_base == frame_base_reg);
    assign occupied_count = cache_valid ? 2'd1 : 2'd0;
    assign reserved_count = pending ? 2'd1 : 2'd0;
    assign drained = !busy && !pending;

    function [7:0] beat_byte;
        input [127:0] data;
        input [3:0] index;
        begin
            beat_byte = data >> ((15-index) * 8);
        end
    endfunction

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state <= S_IDLE;
            task_id_reg <= {TASK_WIDTH{1'b0}};
            frame_id_reg <= {FRAME_ID_WIDTH{1'b0}};
            frame_base_reg <= 32'd0;
            x0_reg <= 11'd0;
            x1_reg <= 11'd0;
            y0_reg <= 10'd0;
            y1_reg <= 10'd0;
            sample_u <= 5'd0;
            sample_v <= 5'd0;
            first_beat_addr <= 32'd0;
            request_addr_reg <= 32'd0;
            pixel_byte_offset <= 4'd0;
            pixel_r <= 8'd0;
            pixel_g <= 8'd0;
            pixel_b <= 8'd0;
            pending <= 1'b0;
            canceling <= 1'b0;
            accepted_task_id <= {TASK_WIDTH{1'b0}};
            accepted_frame_id <= {FRAME_ID_WIDTH{1'b0}};
            cache_valid <= 1'b0;
            cache_addr <= 32'd0;
            cache_data <= 128'd0;
            cache_frame_base <= 32'd0;
            cache_frame_id <= {FRAME_ID_WIDTH{1'b0}};
            roi_valid <= 1'b0;
            roi_task_id <= {TASK_WIDTH{1'b0}};
            roi_frame_id <= {FRAME_ID_WIDTH{1'b0}};
            roi_x <= 5'd0;
            roi_y <= 5'd0;
            roi_gray <= 8'd0;
            done <= 1'b0;
            cancel_done <= 1'b0;
            busy <= 1'b0;
            protocol_error <= 1'b0;
        end else begin
            roi_valid <= 1'b0;
            done <= 1'b0;
            cancel_done <= 1'b0;

            if ((occupied_count + reserved_count) > 1)
                protocol_error <= 1'b1;
            if (rd_rsp_valid && !pending)
                protocol_error <= 1'b1;

            if ((cancel || canceling) && busy) begin
                canceling <= 1'b1;
                cache_valid <= 1'b0;
                if (pending) begin
                    if (rd_rsp_valid) begin
                        pending <= 1'b0;
                        canceling <= 1'b0;
                        busy <= 1'b0;
                        cancel_done <= 1'b1;
                        state <= S_IDLE;
                    end
                end else begin
                    canceling <= 1'b0;
                    busy <= 1'b0;
                    cancel_done <= 1'b1;
                    state <= S_IDLE;
                end
            end else begin
                case (state)
                    S_IDLE: begin
                        canceling <= 1'b0;
                        if (start_valid) begin
                            if ((start_x0 >= start_x1) ||
                                (start_y0 >= start_y1) ||
                                (start_x1 > FRAME_WIDTH) ||
                                (start_y1 > FRAME_HEIGHT)) begin
                                protocol_error <= 1'b1;
                            end else begin
                                task_id_reg <= start_task_id;
                                frame_id_reg <= start_frame_id;
                                frame_base_reg <= start_frame_base_byte;
                                x0_reg <= start_x0;
                                x1_reg <= start_x1;
                                y0_reg <= start_y0;
                                y1_reg <= start_y1;
                                sample_u <= 5'd0;
                                sample_v <= 5'd0;
                                busy <= 1'b1;
                                state <= S_PREP;
                            end
                        end
                    end

                    S_PREP: begin
                        first_beat_addr <= {pixel_byte_addr_calc[31:4], 4'b0000};
                        pixel_byte_offset <= pixel_byte_addr_calc[3:0];
                        state <= S_FIRST_CHECK;
                    end

                    S_FIRST_CHECK: begin
                        if (cache_hit) begin
                            state <= S_EXTRACT_FIRST;
                        end else begin
                            cache_valid <= 1'b0;
                            request_addr_reg <= first_beat_addr;
                            state <= S_REQ_FIRST;
                        end
                    end

                    S_REQ_FIRST: begin
                        if (request_accept) begin
                            pending <= 1'b1;
                            accepted_task_id <= task_id_reg;
                            accepted_frame_id <= frame_id_reg;
                            state <= S_WAIT_FIRST;
                        end
                    end

                    S_WAIT_FIRST: begin
                        if (rd_rsp_valid) begin
                            if ((accepted_task_id != task_id_reg) ||
                                (accepted_frame_id != frame_id_reg))
                                protocol_error <= 1'b1;
                            pending <= 1'b0;
                            cache_valid <= 1'b1;
                            cache_addr <= request_addr_reg;
                            cache_data <= rd_rsp_data;
                            cache_frame_base <= frame_base_reg;
                            cache_frame_id <= frame_id_reg;
                            state <= S_EXTRACT_FIRST;
                        end
                    end

                    S_EXTRACT_FIRST: begin
                        pixel_r <= beat_byte(cache_data, pixel_byte_offset);
                        if (pixel_byte_offset <= 13) begin
                            pixel_g <= beat_byte(cache_data, pixel_byte_offset + 1'b1);
                            pixel_b <= beat_byte(cache_data, pixel_byte_offset + 2'd2);
                            state <= S_EMIT;
                        end else begin
                            if (pixel_byte_offset == 14)
                                pixel_g <= beat_byte(cache_data, 4'd15);
                            cache_valid <= 1'b0;
                            request_addr_reg <= first_beat_addr + 16;
                            state <= S_REQ_SECOND;
                        end
                    end

                    S_REQ_SECOND: begin
                        if (request_accept) begin
                            pending <= 1'b1;
                            accepted_task_id <= task_id_reg;
                            accepted_frame_id <= frame_id_reg;
                            state <= S_WAIT_SECOND;
                        end
                    end

                    S_WAIT_SECOND: begin
                        if (rd_rsp_valid) begin
                            if ((accepted_task_id != task_id_reg) ||
                                (accepted_frame_id != frame_id_reg))
                                protocol_error <= 1'b1;
                            pending <= 1'b0;
                            cache_valid <= 1'b1;
                            cache_addr <= request_addr_reg;
                            cache_data <= rd_rsp_data;
                            cache_frame_base <= frame_base_reg;
                            cache_frame_id <= frame_id_reg;
                            if (pixel_byte_offset == 14) begin
                                pixel_b <= beat_byte(rd_rsp_data, 4'd0);
                            end else begin
                                pixel_g <= beat_byte(rd_rsp_data, 4'd0);
                                pixel_b <= beat_byte(rd_rsp_data, 4'd1);
                            end
                            state <= S_EMIT;
                        end
                    end

                    S_EMIT: begin
                        roi_valid <= 1'b1;
                        roi_task_id <= task_id_reg;
                        roi_frame_id <= frame_id_reg;
                        roi_x <= sample_u;
                        roi_y <= sample_v;
                        roi_gray <= (pixel_r >> 2) + (pixel_g >> 1) +
                                    (pixel_b >> 2);
                        if ((sample_u == 31) && (sample_v == 31)) begin
                            done <= 1'b1;
                            busy <= 1'b0;
                            state <= S_IDLE;
                        end else begin
                            if (sample_u == 31) begin
                                sample_u <= 5'd0;
                                sample_v <= sample_v + 1'b1;
                            end else begin
                                sample_u <= sample_u + 1'b1;
                            end
                            state <= S_PREP;
                        end
                    end

                    default: begin
                        protocol_error <= 1'b1;
                        busy <= 1'b0;
                        pending <= 1'b0;
                        cache_valid <= 1'b0;
                        state <= S_IDLE;
                    end
                endcase
            end
        end
    end
endmodule
