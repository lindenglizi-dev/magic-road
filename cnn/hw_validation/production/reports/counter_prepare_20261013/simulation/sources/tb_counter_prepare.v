`timescale 1ns / 1ps

// Observe the old recurrence at each real edge; do not alter the tested scheduler.
module counter_prepared_check(
    input clk, input rstn, input [3:0] state, input layer_pw,
    input [3:0] position, input [4:0] count, input [4:0] prepared,
    input accept, input last_group, input start_accept,
    input [8:0] dw_writes, input pp_fault, input load_fault
);
    reg [4:0] expected;
    reg [4:0] after_last;
    integer checks = 0;
    integer last_checks = 0;
    integer stalled_last_checks = 0;
    integer fault_checks = 0;
    integer reset_checks = 0;

    always @(posedge clk) begin
        expected = count;
        after_last = count;
        if (layer_pw) begin
            if (count < 5'd7) after_last = count + 5'd1;
            else if (position < 4'd15) after_last = 5'd0;
        end else begin
            if (count < 5'd15) after_last = count + 5'd1;
            else after_last = 5'd0;
        end
        if (!rstn) expected = 5'd0;
        else if (pp_fault || load_fault) fault_checks = fault_checks + 1;
        else case (state)
            4'd0: if (start_accept) expected = 5'd0;
            4'd2: begin
                if (accept && last_group) begin
                    if (prepared !== after_last)
                        $fatal(1, "Prepared count stale count=%0d prep=%0d expected=%0d layer=%0d pos=%0d", count, prepared, after_last, layer_pw, position);
                    last_checks = last_checks + 1;
                    // Independent old clear/increment recurrence.
                    if (layer_pw) begin
                        if (count < 5'd7) expected = count + 5'd1;
                        else if (position < 4'd15) expected = 5'd0;
                    end else if (count < 5'd15) expected = count + 5'd1;
                    else expected = 5'd0;
                end else if (last_group) stalled_last_checks = stalled_last_checks + 1;
            end
            4'd4: if (dw_writes == 9'd256) expected = 5'd0;
            default: begin end
        endcase
        #1;
        if (count !== expected) $fatal(1, "Counter recurrence mismatch got=%0d expected=%0d", count, expected);
        if (!rstn && prepared !== 5'd0) $fatal(1, "Prepared count reset mismatch");
        checks = checks + 1;
    end

    always @(negedge rstn) begin
        #1;
        if (count !== 5'd0 || prepared !== 5'd0) $fatal(1, "Asynchronous counter cancellation failed");
        reset_checks = reset_checks + 1;
    end
endmodule

// Forced issuer-state unit test; the legal complete-top tests supply the reachability evidence.
module tb_counter_prepare();
    reg clk = 1'b0;
    always #5 clk = ~clk;
    reg rstn = 1'b0;
    reg [3:0] test_state = 4'd2;
    reg test_layer = 1'b0;
    reg [3:0] test_position = 4'd0;
    reg [4:0] test_count = 5'd0;
    reg [1:0] test_group = 2'd0;
    reg test_accept = 1'b0;
    reg test_start = 1'b0;
    reg [8:0] test_writes = 9'd0;
    reg pp_fault = 1'b0;
    reg load_fault = 1'b0;
    reg monitor_rstn = 1'b0;
    integer layer, position, output_group, group_index, variant;
    integer cases = 0;

    road_down2_tile_scheduler dut(.i_clk(clk), .i_rstn(rstn), .i_pp_fault(pp_fault),
        .i_start(1'b0), .i_export_start(1'b0), .i_load_valid(1'b0), .i_table_loaded(1'b0),
        .i_mac_ready(1'b0), .i_mac_result_valid(1'b0), .i_pp_valid(1'b0), .i_pp_ready(1'b0));
    counter_prepared_check check_counter(.clk(clk), .rstn(monitor_rstn), .state(dut.state_current),
        .layer_pw(dut.flag_layer_pw), .position(dut.cnt_position), .count(dut.cnt_output),
        .prepared(dut.reg_cnt_output_prepared), .accept(dut.flag_mac_input_accept),
        .last_group(dut.flag_mac_last_group), .start_accept(dut.flag_start_accept),
        .dw_writes(dut.cnt_dw_writes), .pp_fault(dut.pp_fault), .load_fault(dut.flag_load_fault));

    initial begin
        force dut.state_current = test_state;
        force dut.flag_layer_pw = test_layer;
        force dut.cnt_position = test_position;
        force dut.cnt_mac_group = test_group;
        force dut.flag_mac_input_accept = test_accept;
        force dut.flag_start_accept = test_start;
        force dut.cnt_dw_writes = test_writes;
        force dut.flag_load_fault = load_fault;
        repeat (2) @(negedge clk);
        rstn = 1'b1;
        monitor_rstn = 1'b1;
        for (layer = 0; layer < 2; layer = layer + 1)
            for (position = 0; position < 16; position = position + 1)
                if (layer || position % 4 == 0 || position % 4 == 3)
                    for (output_group = 0; output_group < (layer ? 8 : 16); output_group = output_group + 1)
                        for (variant = 0; variant < 4; variant = variant + 1) begin
                            @(negedge clk);
                            // Prime the new register while count is forced; acceptance remains disabled.
                            test_state = 4'd2;
                            test_layer = layer;
                            test_position = position;
                            test_count = output_group;
                            test_group = 2'd0;
                            test_accept = 1'b0;
                            pp_fault = 1'b0;
                            load_fault = 1'b0;
                            force dut.cnt_output = test_count;
                            @(negedge clk);
                            release dut.cnt_output;
                            test_accept = 1'b1;
                            // group0 is followed immediately by group1 for PW: minimum preparation window.
                            for (group_index = 0; group_index < (layer ? 2 : 3); group_index = group_index + 1) begin
                                test_group = group_index;
                                if (group_index == (layer ? 1 : 2)) begin
                                    if (variant == 1) begin
                                        test_accept = 1'b0;
                                        repeat (12) @(negedge clk);
                                        test_accept = 1'b1;
                                    end
                                    pp_fault = variant == 2;
                                    load_fault = variant == 3;
                                end
                                @(negedge clk);
                            end
                            test_accept = 1'b0;
                            pp_fault = 1'b0;
                            load_fault = 1'b0;
                            cases = cases + 1;
                        end
        // Immediate reset in every issuer group and storage/drain boundary.
        for (group_index = 0; group_index < 5; group_index = group_index + 1) begin
            @(negedge clk);
            test_state = group_index < 3 ? 4'd2 : (group_index == 3 ? 4'd1 : 4'd4);
            test_group = group_index % 3;
            #2; rstn = 1'b0; monitor_rstn = 1'b0;
            #2;
            if (dut.cnt_output !== 0 || dut.reg_cnt_output_prepared !== 0) $fatal(1, "Reset group=%0d", group_index);
            @(negedge clk); rstn = 1'b1; monitor_rstn = 1'b1;
            repeat (2) @(negedge clk);
        end
        $display("TB_PASS_COUNTER_PREPARE cases=%0d checks=%0d last=%0d stalls=%0d faults=%0d resets=%0d", cases, check_counter.checks, check_counter.last_checks, check_counter.stalled_last_checks, check_counter.fault_checks, check_counter.reset_checks);
        $finish;
    end
endmodule
