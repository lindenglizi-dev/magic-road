// Croc OBI subordinate adapter for the Lesson 16 GEMM register block.
// Uses croc_pkg::sbr_obi_req_t and croc_pkg::sbr_obi_rsp_t.
// Response latency: response registered on acceptance edge; visible for one cycle.
// At most ONE outstanding transaction: after accepting a request, no grant
// until the corresponding response cycle has completed.
// Full-word aligned accesses only. Partial writes and unmapped offsets respond err=1.
module croc_gemm_obi
  import croc_pkg::*;
(
    input  logic         clk_i,
    input  logic         rst_ni,
    input  sbr_obi_req_t obi_req_i,
    output sbr_obi_rsp_t obi_rsp_o
);
    logic                     rsp_valid_q;
    logic [SbrObiCfg.DataWidth-1:0] rsp_data_q;
    logic [SbrObiCfg.IdWidth-1:0]   rsp_id_q;
    logic                     rsp_err_q;

    wire accept = obi_req_i.req && obi_rsp_o.gnt;
    wire [11:0] offset = obi_req_i.a.addr[11:0];
    localparam logic [31:0] GEMM_BASE = 32'h2000_1000;
    wire addr_in_window = (obi_req_i.a.addr[31:12] == GEMM_BASE[31:12]);
    wire aligned = (offset[1:0] == 2'b00);
    wire full_byte_write = (obi_req_i.a.be == 4'b1111);
    wire readable = (offset == 12'h000) || (offset == 12'h004)
        || (offset >= 12'h010 && offset <= 12'h02c)
        || (offset >= 12'h040 && offset <= 12'h07c);
    wire writable = (offset == 12'h000)
        || (offset >= 12'h010 && offset <= 12'h02c);
    wire invalid_access = !addr_in_window || !aligned ||
        (obi_req_i.a.we ? (!full_byte_write || !writable) : !readable);

    logic [31:0] reg_rdata;
    logic reg_ready_unused, busy_unused, done_unused, error_unused;

    // The existing leaf register block supports single-cycle, full-word operations.
    // Do not let an illegal OBI access produce side effects.
    gemm_mmio_4x4 u_regs (
        .clk(clk_i), .rst_n(rst_ni),
        .reg_valid(accept && !invalid_access),
        .reg_write(obi_req_i.a.we),
        .reg_addr(offset),
        .reg_wdata(obi_req_i.a.wdata),
        .reg_ready(reg_ready_unused),
        .reg_rdata(reg_rdata),
        .busy(busy_unused), .done(done_unused), .error(error_unused)
    );

    always_comb begin
        obi_rsp_o = '0;
        // gnt does NOT depend combinationally on req (CombGnt=0 Croc config).
        obi_rsp_o.gnt       = !rsp_valid_q;
        obi_rsp_o.rvalid    = rsp_valid_q;
        obi_rsp_o.r.rdata  = rsp_data_q;
        obi_rsp_o.r.rid    = rsp_id_q;
        obi_rsp_o.r.err    = rsp_err_q;
        obi_rsp_o.r.r_optional = '0;
    end

    always_ff @(posedge clk_i or negedge rst_ni) begin
        if (!rst_ni) begin
            rsp_valid_q <= 1'b0;
            rsp_data_q  <= '0;
            rsp_id_q    <= '0;
            rsp_err_q   <= 1'b0;
        end else begin
            rsp_valid_q <= 1'b0;
            if (accept) begin
                rsp_valid_q <= 1'b1;
                rsp_data_q  <= invalid_access ? 32'b0 : reg_rdata;
                rsp_id_q    <= obi_req_i.a.aid;
                rsp_err_q   <= invalid_access;
            end
        end
    end
endmodule
