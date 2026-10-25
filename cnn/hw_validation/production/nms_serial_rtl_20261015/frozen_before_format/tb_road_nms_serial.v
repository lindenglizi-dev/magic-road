`timescale 1ns / 1ps

module tb_road_nms_serial;

    reg i_clk;
    reg i_rstn;
    reg i_cancel;
    reg i_sealed_valid;
    reg [31:0] i_frame_token;
    reg [7:0] i_count_person;
    reg [7:0] i_count_vehicle;
    reg i_read_ready;
    reg i_response_valid;
    reg i_response_class;
    reg [6:0] i_response_index;
    reg [159:0] i_response_data;
    reg i_response_error;
    reg i_entry_ready;

    wire o_sealed_ready;
    wire o_read_valid;
    wire o_read_class;
    wire [6:0] o_read_index;
    wire o_response_ready;
    wire o_entry_valid;
    wire [96:0] o_entry_data;
    wire [31:0] o_frame_token;
    wire [6:0] o_output_count;
    wire o_done;
    wire o_fault;

    reg [159:0] candidate_words [0:255];
    reg [96:0] expected_words [0:63];
    reg [135:0] comparison_words [0:6943];
    reg [9:0] decision_words [0:255];

    reg [4095:0] candidate_path;
    reg [4095:0] expected_path;
    reg [4095:0] comparison_path;
    reg [4095:0] decision_path;
    integer count_person_arg;
    integer count_vehicle_arg;
    integer output_count_arg;
    integer comparison_count_arg;
    integer decision_count_arg;
    integer case_id;
    integer pause_mode;
    integer test_kind;

    integer error_count;
    integer output_seen;
    integer comparison_seen;
    integer decision_seen;
    integer done_seen;
    integer request_seen;
    integer response_seen;
    integer cycle_total;
    integer cycle_request_wait;
    integer cycle_response_wait;
    integer cycle_output_wait;
    integer cycle_multiply;
    integer cycle_other;
    integer stall_request;
    integer stall_response;
    integer stall_output;
    integer response_delay;
    integer recovery_runs;

    reg scoreboard_enable;
    reg cycle_enable;
    reg service_outstanding;
    reg service_class;
    reg [6:0] service_index;
    reg inject_enable;
    reg force_read_stall;
    reg force_response_stall;
    reg force_entry_stall;
    reg [31:0] lfsr;

    reg hold_read;
    reg hold_read_class;
    reg [6:0] hold_read_index;
    reg hold_entry;
    reg [96:0] hold_entry_data;
    reg [31:0] hold_entry_token;
    reg hold_response;
    reg hold_response_class;
    reg [6:0] hold_response_index;
    reg [159:0] hold_response_data;
    reg hold_response_error;

    reg [135:0] actual_comparison;
    reg [9:0] actual_decision;
    reg [159:0] response_word;
    reg [39:0] expected_area;

    road_nms_serial dut(
        .i_clk(i_clk),
        .i_rstn(i_rstn),
        .i_cancel(i_cancel),
        .i_sealed_valid(i_sealed_valid),
        .i_frame_token(i_frame_token),
        .i_count_person(i_count_person),
        .i_count_vehicle(i_count_vehicle),
        .i_read_ready(i_read_ready),
        .i_response_valid(i_response_valid),
        .i_response_class(i_response_class),
        .i_response_index(i_response_index),
        .i_response_data(i_response_data),
        .i_response_error(i_response_error),
        .i_entry_ready(i_entry_ready),
        .o_sealed_ready(o_sealed_ready),
        .o_read_valid(o_read_valid),
        .o_read_class(o_read_class),
        .o_read_index(o_read_index),
        .o_response_ready(o_response_ready),
        .o_entry_valid(o_entry_valid),
        .o_entry_data(o_entry_data),
        .o_frame_token(o_frame_token),
        .o_output_count(o_output_count),
        .o_done(o_done),
        .o_fault(o_fault)
    );

    always #5 i_clk = ~i_clk;

    function [39:0] area_of;
        input [159:0] word;
        reg [17:0] width_value;
        reg [17:0] height_value;
        begin
            width_value = word[53:36] - word[17:0];
            height_value = word[71:54] - word[35:18];
            area_of = width_value * height_value;
        end
    endfunction

    task fail;
        input [1023:0] message;
        begin
            error_count = error_count + 1;
            $display("TB_ERROR case=%0d kind=%0d time=%0t %0s", case_id, test_kind, $time, message);
        end
    endtask

    task clear_scoreboard;
        begin
            output_seen = 0;
            comparison_seen = 0;
            decision_seen = 0;
            done_seen = 0;
            request_seen = 0;
            response_seen = 0;
            cycle_total = 0;
            cycle_request_wait = 0;
            cycle_response_wait = 0;
            cycle_output_wait = 0;
            cycle_multiply = 0;
            cycle_other = 0;
            stall_request = 0;
            stall_response = 0;
            stall_output = 0;
        end
    endtask

    task reset_dut;
        begin
            scoreboard_enable = 1'b0;
            cycle_enable = 1'b0;
            i_sealed_valid = 1'b0;
            i_cancel = 1'b0;
            i_rstn = 1'b0;
            repeat (4) @(negedge i_clk);
            i_rstn = 1'b1;
            repeat (3) @(negedge i_clk);
            if (!o_sealed_ready || o_fault || o_done || o_entry_valid || o_read_valid || o_response_ready)
                fail("reset release did not return to clean idle");
        end
    endtask

    task seal_case;
        input integer override_count;
        begin
            clear_scoreboard;
            @(negedge i_clk);
            i_frame_token = 32'h4e4d5300 + case_id;
            i_count_person = override_count ? 8'd129 : count_person_arg[7:0];
            i_count_vehicle = count_vehicle_arg[7:0];
            i_sealed_valid = 1'b1;
            while (!o_sealed_ready) @(negedge i_clk);
            @(negedge i_clk);
            i_sealed_valid = 1'b0;
            scoreboard_enable = 1'b1;
            cycle_enable = 1'b1;
        end
    endtask

    task pulse_cancel;
        begin
            scoreboard_enable = 1'b0;
            cycle_enable = 1'b0;
            @(negedge i_clk);
            i_cancel = 1'b1;
            @(posedge i_clk);
            #1;
            if (o_sealed_ready || o_read_valid || o_response_ready || o_entry_valid || o_done)
                fail("cancel did not mask ready/valid/done");
            @(negedge i_clk);
            i_cancel = 1'b0;
            repeat (3) @(negedge i_clk);
            if (!o_sealed_ready || o_fault || o_output_count != 0)
                fail("cancel did not restore clean idle");
        end
    endtask

    task pulse_reset;
        begin
            scoreboard_enable = 1'b0;
            cycle_enable = 1'b0;
            @(negedge i_clk);
            i_rstn = 1'b0;
            #1;
            if (o_sealed_ready || o_read_valid || o_response_ready || o_entry_valid || o_done)
                fail("asynchronous reset did not mask ready/valid/done");
            repeat (3) @(negedge i_clk);
            i_rstn = 1'b1;
            repeat (3) @(negedge i_clk);
            if (!o_sealed_ready || o_fault || o_output_count != 0)
                fail("reset did not restore clean idle");
        end
    endtask

    task wait_for_done;
        integer watchdog;
        begin
            watchdog = 0;
            while (!o_done && !o_fault && watchdog < 2000000) begin
                @(posedge i_clk);
                watchdog = watchdog + 1;
            end
            if (watchdog >= 2000000)
                fail("timeout waiting for done");
            if (o_fault)
                fail("unexpected fault in valid case");
            @(negedge i_clk);
            scoreboard_enable = 1'b0;
            cycle_enable = 1'b0;
            if (output_seen != output_count_arg)
                fail("output count mismatch");
            if (comparison_seen != comparison_count_arg)
                fail("comparison count mismatch");
            if (decision_seen != decision_count_arg)
                fail("decision count mismatch");
            if (done_seen != 1)
                fail("done was not exactly one cycle");
            if (o_output_count != output_count_arg[6:0])
                fail("reported output count mismatch");
            if (cycle_total != cycle_request_wait + cycle_response_wait + cycle_output_wait +
                               cycle_multiply + cycle_other)
                fail("cycle categories are not disjoint and complete");
            repeat (2) @(negedge i_clk);
            if (o_done)
                fail("done was wider than one cycle");
            $display("CASE_RESULT id=%0d pause=%0d outputs=%0d comparisons=%0d decisions=%0d cycles=%0d request_phase=%0d response_phase=%0d output_phase=%0d multiply=%0d other=%0d request_stall=%0d response_stall=%0d output_stall=%0d",
                case_id, pause_mode, output_seen, comparison_seen, decision_seen, cycle_total,
                cycle_request_wait, cycle_response_wait, cycle_output_wait, cycle_multiply, cycle_other,
                stall_request, stall_response, stall_output);
        end
    endtask

    task run_valid_case;
        begin
            inject_enable = 1'b0;
            force_read_stall = 1'b0;
            force_response_stall = 1'b0;
            force_entry_stall = 1'b0;
            seal_case(0);
            wait_for_done;
            recovery_runs = recovery_runs + 1;
        end
    endtask

    task wait_for_fault;
        integer watchdog;
        begin
            watchdog = 0;
            while (!o_fault && watchdog < 20000) begin
                @(posedge i_clk);
                watchdog = watchdog + 1;
            end
            if (!o_fault)
                fail("timeout waiting for required fault");
            if (o_done || o_output_count != 0 || o_entry_valid || o_read_valid || o_response_ready)
                fail("fault did not discard the partial table and stop interfaces");
            repeat (3) @(posedge i_clk);
            if (!o_fault)
                fail("fault was not sticky");
            scoreboard_enable = 1'b0;
            cycle_enable = 1'b0;
        end
    endtask

    task run_fault_then_recover;
        begin
            inject_enable = (test_kind != 6 && test_kind != 9);
            seal_case(test_kind == 6);
            wait_for_fault;
            if (test_kind == 9 && output_seen == 0)
                fail("late fault occurred before any output was accepted");
            pulse_cancel;
            run_valid_case;
        end
    endtask

    task run_abort_then_recover;
        integer phase;
        begin
            phase = test_kind - 20;
            force_read_stall = (phase == 0 || phase == 4);
            force_response_stall = (phase == 1 || phase == 5);
            force_entry_stall = 1'b0;
            inject_enable = 1'b0;
            seal_case(0);
            if (phase == 0 || phase == 4) begin
                while (!o_read_valid) @(posedge i_clk);
                repeat (5) @(posedge i_clk);
            end else if (phase == 1 || phase == 5) begin
                while (!service_outstanding) @(posedge i_clk);
                repeat (5) @(posedge i_clk);
            end else if (phase == 2 || phase == 6) begin
                while (dut.state_current != dut.ST_MULTIPLY_CURRENT &&
                       dut.state_current != dut.ST_MULTIPLY_PREVIOUS &&
                       dut.state_current != dut.ST_MULTIPLY_INTERSECTION) @(posedge i_clk);
                repeat (7) @(posedge i_clk);
            end else begin
                while (output_seen == 0) @(posedge i_clk);
                force_entry_stall = 1'b1;
                @(negedge i_clk);
                while (o_entry_valid) @(posedge i_clk);
                while (!o_entry_valid) @(posedge i_clk);
                repeat (4) @(posedge i_clk);
            end
            if (phase < 4)
                pulse_cancel;
            else
                pulse_reset;
            force_read_stall = 1'b0;
            force_response_stall = 1'b0;
            force_entry_stall = 1'b0;
            run_valid_case;
        end
    endtask

    task run_long_output_backpressure;
        begin
            inject_enable = 1'b0;
            force_read_stall = 1'b0;
            force_response_stall = 1'b0;
            force_entry_stall = 1'b1;
            seal_case(0);
            while (!o_entry_valid) @(posedge i_clk);
            repeat (128) @(posedge i_clk);
            if (!o_entry_valid)
                fail("entry valid did not survive deterministic 128-cycle backpressure");
            force_entry_stall = 1'b0;
            wait_for_done;
            recovery_runs = recovery_runs + 1;
        end
    endtask

    always @(posedge i_clk) begin
        if (!i_rstn || i_cancel) begin
            service_outstanding = 1'b0;
            response_delay = 0;
        end else begin
            if (o_read_valid && i_read_ready) begin
                if (service_outstanding)
                    fail("second read accepted while one response was outstanding");
                service_outstanding = 1'b1;
                service_class = o_read_class;
                service_index = o_read_index;
                request_seen = request_seen + 1;
                response_delay = pause_mode ? (lfsr[2:0] % 5) : 0;
            end
            if (i_response_valid && o_response_ready) begin
                if (!service_outstanding)
                    fail("response accepted without an outstanding request");
                service_outstanding = 1'b0;
                response_seen = response_seen + 1;
                inject_enable = 1'b0;
            end
        end
    end

    always @(negedge i_clk) begin
        lfsr = {lfsr[30:0], lfsr[31] ^ lfsr[21] ^ lfsr[1] ^ lfsr[0]};
        if (!i_rstn || i_cancel) begin
            i_read_ready = 1'b0;
            i_response_valid = 1'b0;
            i_response_class = 1'b0;
            i_response_index = 7'd0;
            i_response_data = 160'd0;
            i_response_error = 1'b0;
            i_entry_ready = 1'b0;
        end else begin
            i_read_ready = !force_read_stall && (!pause_mode || lfsr[1:0] != 2'b00);
            i_entry_ready = !force_entry_stall && (!pause_mode || lfsr[4:2] != 3'b000);
            if (service_outstanding && !force_response_stall) begin
                if (response_delay != 0) begin
                    response_delay = response_delay - 1;
                    i_response_valid = 1'b0;
                end else begin
                    response_word = candidate_words[{service_class, service_index}];
                    i_response_valid = 1'b1;
                    i_response_class = service_class;
                    i_response_index = service_index;
                    i_response_data = response_word;
                    i_response_error = 1'b0;
                    if (inject_enable || (test_kind == 9 && output_seen != 0)) begin
                        if (test_kind == 1)
                            i_response_class = ~service_class;
                        else if (test_kind == 2)
                            i_response_index = service_index ^ 7'd1;
                        else if (test_kind == 3)
                            i_response_data[102] = ~service_class;
                        else if (test_kind == 4)
                            i_response_error = 1'b1;
                        else if (test_kind == 5)
                            i_response_index = service_class ? count_vehicle_arg[6:0] : count_person_arg[6:0];
                        else if (test_kind == 7) begin
                            i_response_data = 160'd0;
                            i_response_data[17:0] = 18'd0;
                            i_response_data[35:18] = 18'd0;
                            i_response_data[53:36] = 18'd131073;
                            i_response_data[71:54] = 18'd256;
                            i_response_data[102] = service_class;
                            i_response_data[103] = 1'b1;
                        end else if (test_kind == 8)
                            i_response_data[104] = 1'b1;
                        else if (test_kind == 9)
                            i_response_error = 1'b1;
                    end
                end
            end else begin
                i_response_valid = 1'b0;
                i_response_error = 1'b0;
            end
        end
    end

    always @(posedge i_clk) begin
        if (!i_rstn || i_cancel) begin
            hold_read = 1'b0;
            hold_entry = 1'b0;
            hold_response = 1'b0;
        end else begin
            if (hold_read && (!o_read_valid || o_read_class !== hold_read_class || o_read_index !== hold_read_index))
                fail("read request changed while stalled");
            hold_read = o_read_valid && !i_read_ready;
            if (hold_read) begin
                hold_read_class = o_read_class;
                hold_read_index = o_read_index;
            end
            if (hold_entry && (!o_entry_valid || o_entry_data !== hold_entry_data ||
                               o_frame_token !== hold_entry_token))
                fail("entry payload changed while stalled");
            hold_entry = o_entry_valid && !i_entry_ready;
            if (hold_entry) begin
                hold_entry_data = o_entry_data;
                hold_entry_token = o_frame_token;
            end
            if (hold_response && (!i_response_valid || i_response_class !== hold_response_class ||
                                  i_response_index !== hold_response_index ||
                                  i_response_data !== hold_response_data ||
                                  i_response_error !== hold_response_error))
                fail("response service changed payload while stalled");
            hold_response = i_response_valid && !o_response_ready;
            if (hold_response) begin
                hold_response_class = i_response_class;
                hold_response_index = i_response_index;
                hold_response_data = i_response_data;
                hold_response_error = i_response_error;
            end
        end
    end

    always @(posedge i_clk) begin
        if (scoreboard_enable && i_rstn && !i_cancel) begin
            if (o_frame_token !== 32'h4e4d5300 + case_id)
                fail("frame token changed during active case");
            if (o_entry_valid && i_entry_ready) begin
                if (output_seen >= output_count_arg)
                    fail("duplicate output entry");
                else if (o_entry_data !== expected_words[output_seen])
                    fail("output entry mismatch");
                expected_area = area_of(candidate_words[{dut.reg_class, dut.cnt_candidate[6:0]}]);
                if (dut.reg_area_current !== expected_area)
                    fail("kept candidate current area mismatch");
                actual_decision = {dut.reg_class, dut.cnt_candidate[6:0], 2'd2};
                if (decision_seen >= decision_count_arg || actual_decision !== decision_words[decision_seen])
                    fail("keep decision trace mismatch");
                output_seen = output_seen + 1;
                decision_seen = decision_seen + 1;
            end
            if (dut.state_current == dut.ST_CURRENT_CHECK && !dut.reg_current[103]) begin
                actual_decision = {dut.reg_class, dut.cnt_candidate[6:0], 2'd0};
                if (decision_seen >= decision_count_arg || actual_decision !== decision_words[decision_seen])
                    fail("invalid-geometry decision trace mismatch");
                decision_seen = decision_seen + 1;
            end
            if (dut.state_current == dut.ST_COMPARE_DECIDE) begin
                actual_comparison = {dut.reg_class, dut.cnt_candidate[6:0], dut.reg_read_index,
                    dut.reg_product, dut.reg_area_current, dut.reg_area_previous,
                    (dut.reg_compare_left > dut.reg_compare_right)};
                if (comparison_seen >= comparison_count_arg ||
                    actual_comparison !== comparison_words[comparison_seen])
                    fail("comparison trace mismatch");
                if (dut.reg_product !== comparison_words[comparison_seen][120:81] ||
                    dut.reg_area_current !== comparison_words[comparison_seen][80:41] ||
                    dut.reg_area_previous !== comparison_words[comparison_seen][40:1])
                    fail("40-bit area/intersection mismatch");
                if (dut.reg_compare_left !== ({2'b00, dut.reg_product} +
                                              {1'b0, dut.reg_product, 1'b0}))
                    fail("42-bit comparison left side mismatch");
                if (dut.reg_compare_right !== ({2'b00, dut.reg_area_current} +
                                               {2'b00, dut.reg_area_previous}))
                    fail("42-bit comparison right side mismatch");
                comparison_seen = comparison_seen + 1;
                if (dut.reg_compare_left > dut.reg_compare_right) begin
                    actual_decision = {dut.reg_class, dut.cnt_candidate[6:0], 2'd1};
                    if (decision_seen >= decision_count_arg || actual_decision !== decision_words[decision_seen])
                        fail("suppress decision trace mismatch");
                    decision_seen = decision_seen + 1;
                end
            end
            if (o_done) begin
                done_seen = done_seen + 1;
                if (output_seen != output_count_arg || comparison_seen != comparison_count_arg ||
                    decision_seen != decision_count_arg)
                    fail("done asserted before all expected observations");
            end
        end
    end

    always @(posedge i_clk) begin
        if (cycle_enable && i_rstn && !i_cancel) begin
            cycle_total = cycle_total + 1;
            if (dut.state_current == dut.ST_CURRENT_REQUEST ||
                dut.state_current == dut.ST_PREVIOUS_REQUEST)
                cycle_request_wait = cycle_request_wait + 1;
            else if (dut.state_current == dut.ST_CURRENT_WAIT ||
                     dut.state_current == dut.ST_PREVIOUS_WAIT)
                cycle_response_wait = cycle_response_wait + 1;
            else if (dut.state_current == dut.ST_OUTPUT)
                cycle_output_wait = cycle_output_wait + 1;
            else if (dut.state_current == dut.ST_MULTIPLY_CURRENT ||
                     dut.state_current == dut.ST_MULTIPLY_PREVIOUS ||
                     dut.state_current == dut.ST_MULTIPLY_INTERSECTION)
                cycle_multiply = cycle_multiply + 1;
            else
                cycle_other = cycle_other + 1;
            if ((dut.state_current == dut.ST_CURRENT_REQUEST ||
                 dut.state_current == dut.ST_PREVIOUS_REQUEST) && o_read_valid && !i_read_ready)
                stall_request = stall_request + 1;
            if ((dut.state_current == dut.ST_CURRENT_WAIT ||
                 dut.state_current == dut.ST_PREVIOUS_WAIT) && !i_response_valid)
                stall_response = stall_response + 1;
            if (dut.state_current == dut.ST_OUTPUT && o_entry_valid && !i_entry_ready)
                stall_output = stall_output + 1;
        end
    end

    initial begin
        i_clk = 1'b0;
        i_rstn = 1'b0;
        i_cancel = 1'b0;
        i_sealed_valid = 1'b0;
        i_frame_token = 32'd0;
        i_count_person = 8'd0;
        i_count_vehicle = 8'd0;
        i_read_ready = 1'b0;
        i_response_valid = 1'b0;
        i_response_class = 1'b0;
        i_response_index = 7'd0;
        i_response_data = 160'd0;
        i_response_error = 1'b0;
        i_entry_ready = 1'b0;
        error_count = 0;
        recovery_runs = 0;
        scoreboard_enable = 1'b0;
        cycle_enable = 1'b0;
        service_outstanding = 1'b0;
        inject_enable = 1'b0;
        force_read_stall = 1'b0;
        force_response_stall = 1'b0;
        force_entry_stall = 1'b0;
        lfsr = 32'h1f123bb5;
        hold_read = 1'b0;
        hold_entry = 1'b0;
        hold_response = 1'b0;

        if (!$value$plusargs("CANDIDATE=%s", candidate_path) ||
            !$value$plusargs("EXPECTED=%s", expected_path) ||
            !$value$plusargs("COMPARISONS=%s", comparison_path) ||
            !$value$plusargs("DECISIONS=%s", decision_path) ||
            !$value$plusargs("COUNT_PERSON=%d", count_person_arg) ||
            !$value$plusargs("COUNT_VEHICLE=%d", count_vehicle_arg) ||
            !$value$plusargs("OUTPUT_COUNT=%d", output_count_arg) ||
            !$value$plusargs("COMPARISON_COUNT=%d", comparison_count_arg) ||
            !$value$plusargs("DECISION_COUNT=%d", decision_count_arg) ||
            !$value$plusargs("CASE_ID=%d", case_id))
            $fatal(1, "missing required vector plusargs");
        if (!$value$plusargs("PAUSE=%d", pause_mode)) pause_mode = 0;
        if (!$value$plusargs("TEST_KIND=%d", test_kind)) test_kind = 0;

        $readmemh(candidate_path, candidate_words);
        $readmemh(expected_path, expected_words);
        $readmemh(comparison_path, comparison_words);
        $readmemh(decision_path, decision_words);

        reset_dut;
        if (test_kind == 0)
            run_valid_case;
        else if (test_kind >= 1 && test_kind <= 9)
            run_fault_then_recover;
        else if (test_kind >= 20 && test_kind <= 27)
            run_abort_then_recover;
        else if (test_kind == 28)
            run_long_output_backpressure;
        else
            $fatal(1, "unknown TEST_KIND=%0d", test_kind);

        if (error_count != 0)
            $fatal(1, "TB_FAIL case=%0d kind=%0d errors=%0d", case_id, test_kind, error_count);
        $display("TB_PASS_NMS case=%0d kind=%0d pause=%0d recovery_runs=%0d", case_id, test_kind,
                 pause_mode, recovery_runs);
        $finish;
    end

    initial begin
        #30000000;
        $fatal(1, "global timeout");
    end

endmodule
