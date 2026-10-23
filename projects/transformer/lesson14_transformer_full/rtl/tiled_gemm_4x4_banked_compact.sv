`timescale 1ns/1ps
// Lesson 06: compact valid-only ST_STORE. Same datapath and loader.
// Lesson 05: four *independent* 8-bit SRAM banks for A and four for B.
// One byte per bank, each clock -> 4 bytes per operand per clock.
// Unlike a fictitious unaligned 32-bit wide word, this interface exposes
// physical bank selects and bank-local byte addresses.
// A: bank=row%4, addr=(row/4)*K+col.
// B normal: bank=col%4, addr=row*ceil(N/4)+col/4.
// B transposed-source: bank=col%4, addr=(col/4)*K+row.
// Keep the two operand-buffer sets from Lesson04 for loader/MAC overlap.
// Memory must respond with registered data/valid ONE cycle after request;
// no variable-latency DDR/OBI or SRAM macro inference is claimed.
module tiled_gemm_4x4_banked_compact #(
    parameter integer MAX_DIM = 256,
    parameter integer ADDR_W  = 18
) (
    input  logic clk,
    input  logic rst_n,
    input  logic start,
    input  logic [8:0] m_dim, n_dim, k_dim,
    input  logic b_src_transposed,

    // Independent single-read byte banks. Each flat bus is lane-major.
    output logic [3:0]            a_rd_en,
    output logic [4*ADDR_W-1:0]   a_rd_addr,
    input  logic [31:0]           a_rd_data,
    input  logic [3:0]            a_rd_valid,
    output logic [3:0]            b_rd_en,
    output logic [4*ADDR_W-1:0]   b_rd_addr,
    input  logic [31:0]           b_rd_data,
    input  logic [3:0]            b_rd_valid,

    output logic c_wr_en,
    output logic [8:0] c_wr_row, c_wr_col,
    output logic [ADDR_W-1:0] c_wr_addr,
    output logic signed [31:0] c_wr_data,
    output logic busy,
    output logic done,
    output logic bad_dim,
    output logic mem_protocol_error,
    output logic [31:0] cycles_total,
    output logic [31:0] cycles_load,
    output logic [31:0] cycles_mac,
    output logic [31:0] cycles_store,
    output logic [31:0] cycles_overlap,
    output logic [31:0] cycles_wait_data,
    output logic [8:0] dbg_tile_m,
    output logic [8:0] dbg_tile_n,
    output logic [8:0] dbg_tile_k,
    output logic [2:0] dbg_state,
    output logic [1:0] dbg_load_state,
    output logic       dbg_load_bank,
    output logic       dbg_mac_bank
);
    localparam logic [2:0] ST_IDLE=3'd0, ST_CLEAR=3'd1,
                            ST_RUN=3'd2, ST_STORE=3'd3, ST_NEXT=3'd4;
    localparam logic [1:0] LD_IDLE=2'd0, LD_ISSUE=2'd1, LD_DRAIN=2'd2;
    localparam logic       CP_WAIT=1'b0, CP_MAC=1'b1;

    logic [2:0] state;
    logic [1:0] ld_state;
    logic       cp_state;
    logic [8:0] tm, tn, tk;
    logic [8:0] next_load_k;
    logic       next_load_bank, next_mac_bank;
    logic       ld_bank;
    logic [8:0] ld_k;
    logic [1:0] ld_idx;
    logic [3:0] store_idx;
    logic [1:0] mac_k;
    logic [1:0] bank_occupied, bank_ready;

    // Flat address = 16*bank + tile offset; preserve both ping-pong buffers.
    logic signed [7:0] a_buf [0:31];
    logic signed [7:0] b_buf [0:31];
    logic       rsp_inflight;
    logic [1:0] rsp_tag;
    logic       rsp_bank;
    logic [3:0] rsp_a_needed, rsp_b_needed;

    // During issue cycle t, read four A rows and four B columns.
    // tm/tn are always multiples of 4, so physical bank index == local lane.
    // INVALID lanes are zero-filled without touching the external SRAM.
    wire issuing = (state == ST_RUN) && (ld_state == LD_ISSUE);
    wire [9:0] out_row = {1'b0,tm} + {8'b0,store_idx[3:2]};
    wire [9:0] out_col = {1'b0,tn} + {8'b0,store_idx[1:0]};
    wire c_valid_index = out_row < {1'b0,m_dim} && out_col < {1'b0,n_dim};
    // Output tile is always within the logical matrix; remaining sizes are 1..4.
    // The row/col index is still 4-wide because acc_bus has 16 fixed positions.
    // Skip invalid columns by jumping to the next 4-slot register row.
    wire [9:0] rows_left = {1'b0,m_dim} - {1'b0,tm};
    wire [9:0] cols_left = {1'b0,n_dim} - {1'b0,tn};
    wire [9:0] rows_valid = (rows_left >= 10'd4) ? 10'd4 : rows_left;
    wire [9:0] cols_valid = (cols_left >= 10'd4) ? 10'd4 : cols_left;
    wire store_end_col = ({8'd0,store_idx[1:0]} + 10'd1 == cols_valid);
    wire store_end_row = ({8'd0,store_idx[3:2]} + 10'd1 == rows_valid);
    wire [9:0] b_groups = ({1'b0,n_dim}+10'd3) >> 2;

    genvar lane;
    generate for (lane=0; lane<4; lane=lane+1) begin : g_mem_lanes
        wire [9:0] a_row = {1'b0,tm} + lane;
        wire [9:0] a_col = {1'b0,ld_k} + {8'b0,ld_idx};
        wire [9:0] b_row = {1'b0,ld_k} + {8'b0,ld_idx};
        wire [9:0] b_col = {1'b0,tn} + lane;
        assign a_rd_en[lane] = issuing &&
            (a_row < {1'b0,m_dim}) && (a_col < {1'b0,k_dim});
        assign b_rd_en[lane] = issuing &&
            (b_row < {1'b0,k_dim}) && (b_col < {1'b0,n_dim});
        assign a_rd_addr[ADDR_W*lane +: ADDR_W] =
            (a_row >> 2) * k_dim + a_col;
        assign b_rd_addr[ADDR_W*lane +: ADDR_W] =
            b_src_transposed ? ((b_col >> 2) * k_dim + b_row)
                             : (b_row * b_groups + (b_col >> 2));
    end endgenerate

    logic [31:0] a_vec, b_vec;
    logic [511:0] acc_bus;
    genvar g;
    generate
        for (g=0; g<4; g=g+1) begin : gen_feeder
            assign a_vec[8*g +: 8] = a_buf[16*next_mac_bank + 4*g + mac_k];
            assign b_vec[8*g +: 8] = b_buf[16*next_mac_bank + 4*mac_k + g];
        end
    endgenerate
    mac_array_4x4 u_mac_array (
        .clk(clk), .rst_n(rst_n), .clear(state==ST_CLEAR),
        .mac_en((state==ST_RUN)&&(cp_state==CP_MAC)),
        .a_vec(a_vec), .b_vec(b_vec), .acc_bus(acc_bus)
    );
    assign c_wr_en   = (state == ST_STORE) && c_valid_index;
    assign c_wr_row = out_row[8:0];
    assign c_wr_col = out_col[8:0];
    assign c_wr_addr = out_row * n_dim + out_col;
    assign c_wr_data = $signed(acc_bus[32*store_idx +: 32]);
    assign dbg_tile_m = tm;
    assign dbg_tile_n = tn;
    assign dbg_tile_k = tk;
    assign dbg_state = state;
    assign dbg_load_state = ld_state;
    assign dbg_load_bank = ld_bank;
    assign dbg_mac_bank = next_mac_bank;

    integer j, b, r;
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state <= ST_IDLE;
            ld_state <= LD_IDLE;
            cp_state <= CP_WAIT;
            busy <= 1'b0;
            done <= 1'b0;
            bad_dim <= 1'b0;
            mem_protocol_error <= 1'b0;
            tm <= 0; tn <= 0; tk <= 0;
            next_load_k <= 0;
            next_load_bank <= 0;
            next_mac_bank <= 0;
            ld_bank <= 0;
            ld_k <= 0;
            ld_idx <= 0;
            store_idx <= 0;
            mac_k <= 0;
            bank_occupied <= 0;
            bank_ready <= 0;
            rsp_inflight <= 0;
            rsp_tag <= 0;
            rsp_bank <= 0;
            rsp_a_needed <= 0;
            rsp_b_needed <= 0;
            cycles_total <= 0;
            cycles_load <= 0;
            cycles_mac <= 0;
            cycles_store <= 0;
            cycles_overlap <= 0;
            cycles_wait_data <= 0;
            for (b=0; b<2; b=b+1)
                for (j=0; j<16; j=j+1) begin
                    a_buf[16*b + j] <= 0;
                    b_buf[16*b + j] <= 0;
                end
        end else begin
            done <= 1'b0;
            if (state != ST_IDLE)
                cycles_total <= cycles_total + 1;
            if ((state == ST_RUN) && (ld_state != LD_IDLE))
                cycles_load <= cycles_load + 1;
            if ((state == ST_RUN) && (cp_state == CP_MAC))
                cycles_mac <= cycles_mac + 1;
            if (state == ST_STORE)
                cycles_store <= cycles_store + 1;
            if ((state == ST_RUN) && (ld_state != LD_IDLE) && (cp_state == CP_MAC))
                cycles_overlap <= cycles_overlap + 1;
            if ((state == ST_RUN) && (cp_state == CP_WAIT) &&
                (next_load_k != 0 || ld_state != LD_IDLE))
                cycles_wait_data <= cycles_wait_data + 1;

            // Capture previous cycle's read response before releasing the bank.
            if (rsp_inflight) begin
                for (r=0; r<4; r=r+1) begin
                    if (rsp_a_needed[r]) begin
                        if (a_rd_valid[r])
                            a_buf[16*rsp_bank + 4*r + rsp_tag] <= $signed(a_rd_data[8*r +: 8]);
                        else
                            mem_protocol_error <= 1'b1;
                    end
                    if (rsp_b_needed[r]) begin
                        if (b_rd_valid[r])
                            b_buf[16*rsp_bank + 4*rsp_tag + r] <= $signed(b_rd_data[8*r +: 8]);
                        else
                            mem_protocol_error <= 1'b1;
                    end
                end
            end
            rsp_inflight <= 1'b0;

            case (state)
                ST_IDLE: begin
                    if (start) begin
                        cycles_total <= 0;
                        cycles_load <= 0;
                        cycles_mac <= 0;
                        cycles_store <= 0;
                        cycles_overlap <= 0;
                        cycles_wait_data <= 0;
                        mem_protocol_error <= 1'b0;
                        bad_dim <= (m_dim == 0) || (n_dim == 0) || (k_dim == 0) ||
                                   (m_dim > MAX_DIM) || (n_dim > MAX_DIM) || (k_dim > MAX_DIM);
                        if (m_dim != 0 && n_dim != 0 && k_dim != 0 &&
                            m_dim <= MAX_DIM && n_dim <= MAX_DIM && k_dim <= MAX_DIM) begin
                            busy <= 1'b1;
                            tm <= 0;
                            tn <= 0;
                            state <= ST_CLEAR;
                        end
                    end
                end
                ST_CLEAR: begin
                    // Reset both independent engines for this output tile.
                    // Only the MAC registers are cleared; neither the A/B
                    // buffers nor the GEMM result memory are asynchronously cleared.
                    tk <= 0;
                    next_load_k <= 0;
                    next_load_bank <= 0;
                    next_mac_bank <= 0;
                    bank_occupied <= 0;
                    bank_ready <= 0;
                    ld_state <= LD_IDLE;
                    cp_state <= CP_WAIT;
                    ld_idx <= 0;
                    mac_k <= 0;
                    store_idx <= 0;
                    state <= ST_RUN;
                end
                ST_RUN: begin
                    // Loader engine. It may run in the SAME cycle as CP_MAC.
                    case (ld_state)
                        LD_IDLE: begin
                            if (({1'b0,next_load_k} < {1'b0,k_dim}) &&
                                !bank_occupied[next_load_bank]) begin
                                ld_state <= LD_ISSUE;
                                ld_bank <= next_load_bank;
                                ld_k <= next_load_k;
                                ld_idx <= 0;
                                bank_occupied[next_load_bank] <= 1'b1;
                                next_load_k <= next_load_k + 9'd4;
                                next_load_bank <= ~next_load_bank;
                            end
                        end
                        LD_ISSUE: begin
                            rsp_tag <= ld_idx;
                            rsp_bank <= ld_bank;
                            rsp_a_needed <= a_rd_en;
                            rsp_b_needed <= b_rd_en;
                            rsp_inflight <= 1'b1;
                            for (r=0; r<4; r=r+1) begin
                                if (!a_rd_en[r]) a_buf[16*ld_bank+4*r+ld_idx] <= 8'sd0;
                                if (!b_rd_en[r]) b_buf[16*ld_bank+4*ld_idx+r] <= 8'sd0;
                            end
                            if (ld_idx == 2'd3)
                                ld_state <= LD_DRAIN;
                            else
                                ld_idx <= ld_idx + 1'b1;
                        end
                        LD_DRAIN: begin
                            // The last memory response is captured at this edge.
                            // Compute sees ready on a subsequent edge.
                            ld_state <= LD_IDLE;
                            bank_ready[ld_bank] <= 1'b1;
                        end
                        default: ld_state <= LD_IDLE;
                    endcase

                    // Compute engine: follow the same alternating bank order.
                    if (cp_state == CP_WAIT) begin
                        if (bank_ready[next_mac_bank]) begin
                            cp_state <= CP_MAC;
                            mac_k <= 0;
                        end
                    end else begin
                        if (mac_k == 2'd3) begin
                            // The consumed bank can now be overwritten.
                            bank_ready[next_mac_bank] <= 1'b0;
                            bank_occupied[next_mac_bank] <= 1'b0;
                            next_mac_bank <= ~next_mac_bank;
                            cp_state <= CP_WAIT;
                            if (({1'b0,tk} + 10'd4) < {1'b0,k_dim})
                                tk <= tk + 9'd4;
                            else begin
                                store_idx <= 0;
                                state <= ST_STORE;
                            end
                        end else
                            mac_k <= mac_k + 1'b1;
                    end
                end
                ST_STORE: begin
                    // Only visit valid rows/columns. Keep the original 4x4
                    // accumulator selection: acc_bus[32*store_idx +: 32].
                    // Example 1x2 tile: store_idx=0,1 then NEXT (not 0..15).
                    if (store_end_col) begin
                        if (store_end_row)
                            state <= ST_NEXT;
                        else
                            store_idx <= { (store_idx[3:2] + 2'd1), 2'b00 };
                    end else begin
                        store_idx <= store_idx + 1'b1;
                    end
                end
                ST_NEXT: begin
                    if (({1'b0,tn} + 10'd4) < {1'b0,n_dim}) begin
                        tn <= tn + 9'd4;
                        state <= ST_CLEAR;
                    end else if (({1'b0,tm} + 10'd4) < {1'b0,m_dim}) begin
                        tm <= tm + 9'd4;
                        tn <= 0;
                        state <= ST_CLEAR;
                    end else begin
                        busy <= 1'b0;
                        done <= 1'b1;
                        state <= ST_IDLE;
                    end
                end
                default: state <= ST_IDLE;
            endcase
        end
    end
endmodule
