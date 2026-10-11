`timescale 1ns / 1ps
// 固定播放器与真实冻结核联合回归，链路气泡在两侧同时施加。
module tb_board_selftest;
    reg clk = 1'b0;
    always #5 clk = ~clk;
    reg rstn = 1'b0;
    reg allow_rx = 1'b1;
    reg allow_tx = 1'b1;
    wire player_valid, player_ready, core_ready, core_valid, player_tx_ready, core_rstn;
    wire [15:0] player_data, core_data;
    wire [255:0] payload;
    reg [255:0] scenario;
    reg [4095:0] vector_dir, path;
    reg [7:0] expected [0:1151];
    integer ticks = 0, compared = 0, tables = 0, load_records = 0, resets = 0;
    reg held = 1'b0;
    reg [15:0] held_data;
    reg response_held = 1'b0;
    reg [15:0] response_data;
    reg hold_rx_reset = 1'b0, hold_tx_reset = 1'b0;

    assign player_ready = core_ready & allow_rx;
    road_board_selftest_player dut (
        .i_clk(clk), .i_rstn(rstn), .i_rx_ready(player_ready), .i_tx_valid(core_valid & allow_tx),
        .i_tx_data(core_data), .o_rx_valid(player_valid), .o_rx_data(player_data),
        .o_tx_ready(player_tx_ready), .o_core_rstn(core_rstn), .o_payload(payload)
    );
    road_dynamic_overlap_low_io_top core (
        .i_clk(clk), .i_rstn(core_rstn), .i_rx_valid(player_valid & allow_rx), .i_rx_data(player_data),
        .o_rx_ready(core_ready), .o_tx_valid(core_valid), .o_tx_data(core_data),
        .i_tx_ready(player_tx_ready & allow_tx)
    );

    // 独立比较原结果字节，防止播放器比较数自证。
    always @(posedge clk) begin
        ticks = ticks + 1;
        if (ticks > 700000) $fatal(1, "TB absolute timeout");
        if (!rstn) begin
            held = 0; response_held = 0; compared = 0; tables = 0; load_records = 0;
        end else begin
            if (held && (!player_valid || player_data !== held_data)) $fatal(1, "RX not held");
            held = player_valid && !player_ready;
            held_data = player_data;
            if (!core_rstn) response_held = 0;
            else begin
                if (response_held && (!core_valid || core_data !== response_data)) $fatal(1, "Core TX not held");
                response_held = core_valid && !(player_tx_ready && allow_tx);
                response_data = core_data;
            end
            if (core.flag_table_transfer) tables = tables + 1;
            if (core.flag_load_transfer) load_records = load_records + 1;
            if (core_valid && player_tx_ready && allow_tx && dut.state_current == 5'd4 && core_data[15:12] == 4'h9) begin
                if (compared >= 1152 || core_data[7:0] !== expected[compared]) $fatal(1, "Independent golden mismatch %0d", compared);
                compared = compared + 1;
            end
        end
    end

    // 插入确定性短气泡和持续长停顿，发送/接收两端独立停顿。
    always @(negedge clk) begin
        if (scenario == "stalls") begin
            allow_rx = (ticks % 11 != 0) && !(ticks % 307 > 250);
            allow_tx = (ticks % 7 != 0) && !(ticks % 241 > 180);
        end else if (scenario == "timeout") begin
            allow_rx = 0;
            allow_tx = 1;
        end else if (scenario == "held_reset") begin
            allow_rx = !hold_rx_reset;
            allow_tx = !hold_tx_reset;
        end else begin
            allow_rx = 1;
            allow_tx = 1;
        end
    end

    task cancel_global;
        begin
            @(negedge clk); #1 rstn = 0;
            #1;
            if (player_valid || player_tx_ready || core_rstn) $fatal(1, "Immediate cancellation failed");
            repeat (4) @(negedge clk);
            #1 rstn = 1;
            resets = resets + 1;
        end
    endtask

    initial begin
        scenario = "normal";
        if (!$value$plusargs("CASE=%s", scenario)) scenario = "normal";
        if (!$value$plusargs("VECTORS=%s", vector_dir)) $fatal(1, "Missing frozen VECTORS");
        $sformat(path, "%0s/edge_output.hex", vector_dir); $readmemh(path, expected, 0, 383);
        $sformat(path, "%0s/interior_output.hex", vector_dir); $readmemh(path, expected, 384, 767);
        $sformat(path, "%0s/bottom_right_output.hex", vector_dir); $readmemh(path, expected, 768, 1151);
        #1;
        if (scenario == "wrong") $readmemh("wrong_expected.hex", dut.mem_program);
        if (scenario == "missing") $readmemh("missing_table.hex", dut.mem_program);
        repeat (10) @(negedge clk);
        #1 rstn = 1;
        if (scenario == "reset") begin
            wait (dut.reg_program_addr > 15'd100); cancel_global;
            wait (dut.reg_program_addr > 15'd1400); cancel_global;
            wait (dut.reg_running); cancel_global;
            wait (dut.reg_exporting); cancel_global;
        end
        if (scenario == "held_reset") begin
            hold_rx_reset = 1;
            wait (player_valid && !player_ready);
            repeat (4) @(negedge clk);
            cancel_global; hold_rx_reset = 0;
            wait (dut.reg_exporting); hold_tx_reset = 1;
            wait (core_valid && !(player_tx_ready && allow_tx));
            repeat (4) @(negedge clk);
            cancel_global; hold_tx_reset = 0;
        end
        wait (payload[255:254] != 2'd0);
        @(negedge clk);
        if (scenario == "wrong" || scenario == "missing" || scenario == "timeout") begin
            if (payload[255:254] !== 2'd2) $fatal(1, "Negative case falsely passed");
            if (scenario == "wrong" && dut.reg_error_kind !== 4'd1) $fatal(1, "Wrong expectation not detected");
            if (scenario == "timeout" && dut.reg_error_kind !== 4'd5) $fatal(1, "Timeout not detected");
        end else begin
            if (payload[255:254] !== 2'd1) $fatal(1, "Unexpected FAIL pc=%0d kind=%0d exp=%h actual=%h", dut.reg_first_error_addr, dut.reg_error_kind, dut.reg_first_expected, dut.reg_first_actual);
            if (compared != 1152 || tables != 3072 || load_records != 5844) $fatal(1, "Bad accepted totals %0d %0d %0d", compared, tables, load_records);
            if (dut.reg_core_cycles != 1687) $fatal(1, "Core window changed");
            if (dut.cnt_total_cycles != dut.cnt_preload_cycles + dut.cnt_export_cycles + dut.cnt_run_elapsed) $fatal(1, "Cycle classes not mutually exclusive");
        end
        $display("TB_PASS_BOARD_SELFTEST case=%0s status=%0d compared=%0d tables=%0d records=%0d resets=%0d total=%0d preload=%0d run_elapsed=%0d export=%0d core_last=%0d error=%0d", scenario,
            payload[255:254], compared, tables, load_records, resets, dut.cnt_total_cycles, dut.cnt_preload_cycles,
            dut.cnt_run_elapsed, dut.cnt_export_cycles, dut.reg_core_cycles, dut.reg_error_kind);
        repeat (10) @(negedge clk);
        $finish;
    end
endmodule
