`timescale 1ns / 1ps
// Actual TD gate netlist, including initialized ROM and vendor PLL/HDMI cells.
// No forced internal clock, operand, table, result, or status.
module tb_mapped_board_selftest;
    reg clk = 1'b0;
    reg rstn = 1'b0;
    wire blue, green, red, tmds_clock;
    wire [255:0] payload;
    integer cycles = 0;
    road_board_selftest_top dut (
        .i_sys_clk(clk), .i_rstn(rstn), .o_tmds_blue_p(blue),
        .o_tmds_green_p(green), .o_tmds_red_p(red), .o_tmds_clock_p(tmds_clock)
    );
    assign payload = dut.\road_board_selftest_player_Inst/o_payload ;
    always #10 clk = ~clk;
    initial begin
        #5000 rstn = 1'b1;
        #5000000;
        $display("TB_FAIL_MAPPED timeout payload=%h", payload);
        $fatal(1);
    end
    always @(posedge clk) begin
        cycles = cycles + 1;
        if (payload[255:254] == 2'd2) begin
            $display("TB_FAIL_MAPPED failure payload=%h", payload);
            $fatal(1);
        end
        if (payload[255:254] == 2'd1) begin
            if (payload[248:247] !== 2'd3 || payload[246:236] !== 11'd1152 ||
                payload[235:204] !== 32'd1687) begin
                $display("TB_FAIL_MAPPED counters payload=%h", payload);
                $fatal(1);
            end
            $display("TB_PASS_MAPPED_BOARD_SELFTEST cases=3 compared=1152 core_last=1687 external_50m_cycles=%0d payload=%h", cycles, payload);
            $finish;
        end
    end
endmodule
