`timescale 1ns / 1ps

// Independent task-stream arithmetic, reservation and reset scoreboard.
module tb_mac_task_stream();
    reg clk = 1'b0;
    always #5 clk = ~clk;
    reg rstn = 1'b0;
    reg input_valid = 1'b0;
    reg result_ready = 1'b0;
    reg [361:0]input_word = 362'd0;
    wire input_ready, result_valid, fault;
    wire [95:0]result_data;
    reg [361:0]inputs[0:2047];
    reg [96:0]expected[0:255];
    reg [4095:0]input_path, expected_path;
    integer group_count, task_count;
    integer phase = 0;
    integer send_index = 0;
    integer result_index = 0;
    integer cycles = 0;
    integer reserved_model = 0;
    integer open_model = 0;
    integer input_accept_sample = 0;
    integer result_accept_sample = 0;
    integer first_accept_sample = 0;
    integer count_before = 0;
    integer reserved_before = 0;
    integer held = 0;
    reg [96:0]held_result;
    reg [31:0]random_state = 32'h20261009;
    integer saw_full = 0;
    integer saw_full_continuation = 0;
    integer saw_push_pop = 0;
    integer saw_first_pop = 0;
    integer saw_stable_stall = 0;
    integer saw_mid_reset = 0;
    integer saw_full_reset = 0;
    integer fault_count = 0;

    road_mac_probe dut(
        .i_clk(clk), .i_rstn(rstn),
        .i_input_valid(input_valid), .i_first(input_word[361]),
        .i_last(input_word[360]), .i_lane_mask(input_word[359:352]),
        .i_bias_data(input_word[351:256]), .i_weight_data(input_word[255:64]),
        .i_activation_data(input_word[63:0]), .o_input_ready(input_ready),
        .i_result_ready(result_ready), .o_result_valid(result_valid),
        .o_result_data(result_data), .o_fault(fault)
    );

    // Hold an offered input until its sampled handshake; random gaps only between beats.
    always @(negedge clk) begin
        if (!rstn || phase == 0) begin
            input_valid = 1'b0;
            result_ready = 1'b0;
            input_word = 362'd0;
        end else begin
            random_state = {random_state[30:0],
                random_state[31] ^ random_state[21] ^ random_state[1] ^ random_state[0]};
            if (send_index < group_count) begin
                input_word = inputs[send_index];
                input_valid = (input_valid && !input_accept_sample) ||
                    cycles < 120 || random_state[0] || random_state[3];
            end else begin
                input_valid = 1'b0;
            end
            result_ready = phase == 2 && cycles >= 120 &&
                (random_state[4] || random_state[9]);
        end
    end

    always @(posedge clk) begin
        if (!rstn) begin
            send_index = 0;
            result_index = 0;
            cycles = 0;
            reserved_model = 0;
            open_model = 0;
            input_accept_sample = 0;
            result_accept_sample = 0;
            first_accept_sample = 0;
            held = 0;
        end else if (phase != 0) begin
            cycles = cycles + 1;
            input_accept_sample = input_valid && input_ready;
            result_accept_sample = result_valid && result_ready;
            first_accept_sample = input_accept_sample && input_word[361];
            count_before = dut.cnt_result_count;
            reserved_before = dut.cnt_reserved;
            if (held) begin
                if (!result_valid || {fault,result_data} !== held_result)
                    $fatal(1, "Output changed while stalled at cycle %0d", cycles);
                saw_stable_stall = 1;
            end
            held = result_valid && !result_ready;
            held_result = {fault,result_data};
            if (input_accept_sample) begin
                if (input_word[361] != !open_model)
                    $fatal(1, "Malformed generated task boundary at group %0d", send_index);
                if (reserved_before == 4 && !input_word[361])
                    saw_full_continuation = 1;
                open_model = !input_word[360];
                send_index = send_index + 1;
            end
            if (result_accept_sample) begin
                if (phase != 2 || result_index >= task_count)
                    $fatal(1, "Unexpected extra result %0d", result_index);
                if ({fault,result_data} !== expected[result_index])
                    $fatal(1, "Task %0d got %025h expected %025h", result_index,
                        {fault,result_data}, expected[result_index]);
                if (fault) fault_count = fault_count + 1;
                result_index = result_index + 1;
            end
            if (first_accept_sample && result_accept_sample) saw_first_pop = 1;
            reserved_model = reserved_model + first_accept_sample - result_accept_sample;
            #1;
            if (dut.cnt_reserved !== reserved_model[2:0])
                $fatal(1, "Reservation mismatch got %0d expected %0d", dut.cnt_reserved, reserved_model);
            if (dut.flag_reduction_open !== open_model[0])
                $fatal(1, "Reduction-open mismatch at cycle %0d", cycles);
            if (reserved_model < 0 || reserved_model > 4 ||
                dut.cnt_result_count > dut.cnt_reserved)
                $fatal(1, "Credit conservation violated at cycle %0d", cycles);
            if (dut.cnt_result_count == 4) saw_full = 1;
            if (result_accept_sample && dut.cnt_result_count == count_before)
                saw_push_pop = 1;
            if (cycles > 20000) $fatal(1, "Timeout send=%0d result=%0d", send_index, result_index);
        end
    end

    initial begin
        if (!$value$plusargs("INPUTS=%s", input_path) ||
            !$value$plusargs("EXPECTED=%s", expected_path) ||
            !$value$plusargs("N_GROUPS=%d", group_count) ||
            !$value$plusargs("N_TASKS=%d", task_count))
            $fatal(1, "Run mac_reference.py; pass INPUTS, EXPECTED, N_GROUPS, N_TASKS");
        if (group_count < 24 || group_count > 2048 || task_count > 256)
            $fatal(1, "Invalid vector bounds");
        $readmemh(input_path, inputs, 0, group_count - 1);
        $readmemh(expected_path, expected, 0, task_count - 1);
        repeat (3) @(negedge clk);
        #1; phase = 1; rstn = 1'b1;
        repeat (6) @(negedge clk);
        #1;
        if (!dut.flag_reduction_open || dut.cnt_reserved == 0)
            $fatal(1, "Mid-task reset did not hit active work");
        rstn = 1'b0;
        #1;
        if (input_ready !== 1'b1 || result_valid || dut.cnt_reserved != 0 || dut.flag_reduction_open)
            $fatal(1, "Asynchronous reset failed to cancel active work or preserve legacy ready=1");
        saw_mid_reset = 1;
        repeat (3) @(negedge clk);
        #1; rstn = 1'b1;
        repeat (70) @(negedge clk);
        #1;
        if (dut.cnt_result_count != 4)
            $fatal(1, "Output block did not fill four result slots");
        rstn = 1'b0;
        #1;
        if (input_ready !== 1'b1 || result_valid || dut.cnt_reserved != 0 || dut.cnt_result_count != 0)
            $fatal(1, "Asynchronous reset failed to cancel completed work or preserve legacy ready=1");
        saw_full_reset = 1;
        repeat (3) @(negedge clk);
        #1; phase = 2; rstn = 1'b1;
        wait (result_index == task_count);
        repeat (4) @(negedge clk);
        #2;
        if (send_index != group_count || dut.cnt_reserved != 0 ||
            dut.cnt_result_count != 0 || result_valid || open_model)
            $fatal(1, "Final drain incomplete");
        if (!(saw_full && saw_full_continuation && saw_push_pop && saw_first_pop &&
            saw_stable_stall && saw_mid_reset && saw_full_reset) || fault_count != 2)
            $fatal(1, "Missing coverage full=%0d continue=%0d pushpop=%0d firstpop=%0d stall=%0d reset=%0d/%0d faults=%0d",
                saw_full, saw_full_continuation, saw_push_pop, saw_first_pop,
                saw_stable_stall, saw_mid_reset, saw_full_reset, fault_count);
        $display("PASS mac_task_stream tasks=%0d groups=%0d cycles=%0d faults=%0d full=1 full_continue=1 push_pop=1 first_pop=1 stall=1 resets=2",
            task_count, group_count, cycles, fault_count);
        $finish;
    end
endmodule
