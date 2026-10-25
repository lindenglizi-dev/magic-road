`timescale 1ns / 1ps

module tb_road_postprocess_real_rom;

    localparam [31:0] MODEL_ID = 32'hB35D4A66;
    localparam [2:0] PHASE_FREE = 3'd0;
    localparam [2:0] PHASE_SCAN = 3'd1;
    localparam [2:0] PHASE_SORT = 3'd2;
    localparam [2:0] PHASE_DECODE = 3'd3;
    localparam [2:0] PHASE_NMS = 3'd4;

    reg i_clk;
    reg i_rstn;
    reg common_cancel;
    reg start_valid;
    reg [31:0] start_frame_token;
    reg [31:0] start_model_id;
    reg cell_valid;
    reg [111:0] cell_data;
    reg [13:0] cell_id;
    reg [31:0] cell_frame_token;
    wire lut_rsp_valid;
    wire lut_rsp_kind;
    wire [9:0] lut_rsp_address;
    wire [15:0] lut_rsp_tag;
    wire [31:0] lut_rsp_frame_token;
    wire [31:0] lut_rsp_model_id;
    wire [15:0] lut_rsp_data;
    wire lut_rsp_error;
    reg entry_ready;

    wire start_ready;
    wire cell_ready;
    wire lut_req_valid;
    wire lut_req_kind;
    wire [9:0] lut_req_address;
    wire [15:0] lut_req_tag;
    wire [31:0] lut_req_frame_token;
    wire [31:0] lut_req_model_id;
    wire lut_req_ready;
    wire lut_rsp_ready;
    wire lut_cancel;
    wire sealed_valid;
    wire [31:0] sealed_frame_token;
    wire [7:0] count_person;
    wire [7:0] count_vehicle;
    wire read_req_ready;
    wire read_rsp_valid;
    wire read_rsp_class;
    wire [6:0] read_rsp_index;
    wire [159:0] read_rsp_data;
    wire read_rsp_error;
    wire finish_ready;
    wire c2_fault;
    wire [3:0] c2_error_code;
    wire [2:0] c2_phase;
    wire [31:0] c2_scan_cycles;
    wire [31:0] c2_sort_cycles;
    wire [31:0] c2_decode_cycles;
    wire [31:0] c2_input_wait_cycles;
    wire [31:0] c2_lut_wait_cycles;
    wire [31:0] c2_ram_wait_cycles;
    wire [31:0] c2_ram_read_words;
    wire [31:0] c2_ram_write_words;

    wire nms_sealed_ready;
    wire nms_read_valid;
    wire nms_read_class;
    wire [6:0] nms_read_index;
    wire nms_response_ready;
    wire nms_entry_valid;
    wire [96:0] nms_entry_data;
    wire [31:0] nms_frame_token;
    wire [6:0] nms_output_count;
    wire nms_done;
    wire nms_fault;
    wire injected_response_error;

    // Simulation-only image: the controlled endpoint models one outstanding 160-bit read.
    reg [159:0] physical_words [0:7167];
    reg [4095:0] physical_path;
    wire rom_request_valid;
    wire [12:0] rom_request_addr;
    wire rom_request_ready;
    reg rom_response_valid;
    reg [159:0] rom_response_data;
    wire rom_response_ready;
    wire service_fault;
    reg rom_fault;
    reg rom_pending;
    reg [12:0] rom_pending_address;
    integer rom_delay;
    reg hold_rom_response;
    reg hold_rom_request;
    reg [12:0] held_rom_address;
    reg hold_rom_word;
    reg [159:0] held_rom_word;
    integer rom_words_accepted;
    integer rom_words_consumed;
    integer rom_request_wait;
    integer rom_response_wait;
    integer adapter_queries;
    integer adapter_latency_total;
    integer adapter_latency_max;
    integer adapter_accept_cycle;
    integer drain_words;
    integer budget_fail_count;
    reg [96:0] expected_words [0:63];
    reg [111:0] streamed_head;
    reg [4095:0] head_path;
    reg [4095:0] expected_path;
    reg [4095:0] head2_path;
    reg [4095:0] expected2_path;

    integer mode;
    integer stall_mode;
    integer expect_person;
    integer expect_vehicle;
    integer expect_outputs;
    integer expect2_person;
    integer expect2_vehicle;
    integer expect2_outputs;
    integer max_cycles;
    integer cycle_count;
    integer fail_count;
    integer head_handle;
    integer scan_result;
    integer output_seen;
    integer done_seen;
    integer start_accept_cycle;
    integer seal_accept_cycle;
    integer seal_ram_write_words;
    integer last_output_cycle;
    integer done_cycle;
    integer frame_number;
    integer recovery_runs;

    integer nms_cycle_total;
    integer nms_request_phase;
    integer nms_response_phase;
    integer nms_output_phase;
    integer nms_multiply_phase;
    integer nms_other_phase;
    integer nms_request_stall;
    integer nms_response_stall;
    integer nms_output_stall;

    reg frame_monitor;
    reg nms_cycle_enable;
    reg force_output_stall;
    reg late_error_arm;
    reg late_error_used;
    reg [31:0] lfsr;

    reg hold_lut_request;
    reg hold_lut_kind;
    reg [9:0] hold_lut_address;
    reg [15:0] hold_lut_tag;
    reg [31:0] hold_lut_frame;
    reg [31:0] hold_lut_model;
    reg hold_seal;
    reg [31:0] hold_seal_token;
    reg [7:0] hold_seal_person;
    reg [7:0] hold_seal_vehicle;
    reg hold_entry;
    reg [96:0] hold_entry_data;
    reg [31:0] hold_entry_token;

    assign rom_request_ready = i_rstn && !rom_pending && !rom_response_valid &&
                               (!stall_mode || lfsr[5:3] != 3'b000);
    assign injected_response_error = late_error_arm && !late_error_used &&
                                     (output_seen != 0) && read_rsp_valid;

    road_head_decode_topk c2(
        .i_clk(i_clk), .i_rstn(i_rstn), .i_abort(common_cancel),
        .i_start_valid(start_valid), .i_start_frame_token(start_frame_token),
        .i_start_model_id(start_model_id), .i_cell_valid(cell_valid),
        .i_cell_data(cell_data), .i_cell_id(cell_id), .i_cell_frame_token(cell_frame_token),
        .i_lut_req_ready(lut_req_ready), .i_lut_rsp_valid(lut_rsp_valid),
        .i_lut_rsp_kind(lut_rsp_kind), .i_lut_rsp_address(lut_rsp_address),
        .i_lut_rsp_tag(lut_rsp_tag), .i_lut_rsp_frame_token(lut_rsp_frame_token),
        .i_lut_rsp_model_id(lut_rsp_model_id), .i_lut_rsp_data(lut_rsp_data),
        .i_lut_rsp_error(lut_rsp_error), .i_sealed_ready(nms_sealed_ready),
        .i_read_req_valid(nms_read_valid), .i_read_req_class(nms_read_class),
        .i_read_req_index(nms_read_index), .i_read_rsp_ready(nms_response_ready),
        .i_finish_valid(nms_done), .i_finish_frame_token(nms_frame_token),
        .o_start_ready(start_ready), .o_cell_ready(cell_ready),
        .o_lut_req_valid(lut_req_valid), .o_lut_req_kind(lut_req_kind),
        .o_lut_req_address(lut_req_address), .o_lut_req_tag(lut_req_tag),
        .o_lut_req_frame_token(lut_req_frame_token), .o_lut_req_model_id(lut_req_model_id),
        .o_lut_rsp_ready(lut_rsp_ready), .o_lut_cancel(lut_cancel),
        .o_sealed_valid(sealed_valid), .o_sealed_frame_token(sealed_frame_token),
        .o_count_person(count_person), .o_count_vehicle(count_vehicle),
        .o_read_req_ready(read_req_ready), .o_read_rsp_valid(read_rsp_valid),
        .o_read_rsp_class(read_rsp_class), .o_read_rsp_index(read_rsp_index),
        .o_read_rsp_data(read_rsp_data), .o_read_rsp_error(read_rsp_error),
        .o_finish_ready(finish_ready), .o_fault(c2_fault), .o_error_code(c2_error_code),
        .o_phase(c2_phase), .o_scan_cycles(c2_scan_cycles),
        .o_sort_cycles(c2_sort_cycles), .o_decode_cycles(c2_decode_cycles),
        .o_input_wait_cycles(c2_input_wait_cycles), .o_lut_wait_cycles(c2_lut_wait_cycles),
        .o_ram_wait_cycles(c2_ram_wait_cycles), .o_ram_read_words(c2_ram_read_words),
        .o_ram_write_words(c2_ram_write_words)
    );

    // Frozen real adapter owns lookup identity and byte extraction; no direct LUT oracle.
    road_shared_lut_service service(
        .i_clk(i_clk), .i_rstn(i_rstn), .i_cancel(common_cancel | lut_cancel),
        .i_lut_req_valid(lut_req_valid), .i_lut_req_kind(lut_req_kind),
        .i_lut_req_address(lut_req_address), .i_lut_req_tag(lut_req_tag),
        .i_lut_req_frame_token(lut_req_frame_token), .i_lut_req_model_id(lut_req_model_id),
        .o_lut_req_ready(lut_req_ready), .o_lut_rsp_valid(lut_rsp_valid),
        .o_lut_rsp_kind(lut_rsp_kind), .o_lut_rsp_address(lut_rsp_address),
        .o_lut_rsp_tag(lut_rsp_tag), .o_lut_rsp_frame_token(lut_rsp_frame_token),
        .o_lut_rsp_model_id(lut_rsp_model_id), .o_lut_rsp_data(lut_rsp_data),
        .o_lut_rsp_error(lut_rsp_error), .i_lut_rsp_ready(lut_rsp_ready),
        .o_rom_request_valid(rom_request_valid), .o_rom_request_addr(rom_request_addr),
        .i_rom_request_ready(rom_request_ready), .i_rom_response_valid(rom_response_valid),
        .i_rom_response_data(rom_response_data), .o_rom_response_ready(rom_response_ready),
        .i_rom_fault(rom_fault), .o_fault(service_fault)
    );

    road_nms_serial c9(
        .i_clk(i_clk), .i_rstn(i_rstn), .i_cancel(common_cancel),
        .i_sealed_valid(sealed_valid), .i_frame_token(sealed_frame_token),
        .i_count_person(count_person), .i_count_vehicle(count_vehicle),
        .i_read_ready(read_req_ready), .i_response_valid(read_rsp_valid),
        .i_response_class(read_rsp_class), .i_response_index(read_rsp_index),
        .i_response_data(read_rsp_data),
        .i_response_error(read_rsp_error | injected_response_error),
        .i_entry_ready(entry_ready), .o_sealed_ready(nms_sealed_ready),
        .o_read_valid(nms_read_valid), .o_read_class(nms_read_class),
        .o_read_index(nms_read_index), .o_response_ready(nms_response_ready),
        .o_entry_valid(nms_entry_valid), .o_entry_data(nms_entry_data),
        .o_frame_token(nms_frame_token), .o_output_count(nms_output_count),
        .o_done(nms_done), .o_fault(nms_fault)
    );

    always #5 i_clk = ~i_clk;

    task mark_error;
        input integer error_id;
        begin
            fail_count = fail_count + 1;
            $display("TB_ERROR id=%0d cycle=%0d c2_phase=%0d c2_code=%0d nms_state=%0d",
                     error_id, cycle_count, c2_phase, c2_error_code, c9.state_current);
        end
    endtask

    task clear_drives;
        begin
            common_cancel = 1'b0;
            start_valid = 1'b0;
            start_frame_token = 32'd0;
            start_model_id = 32'd0;
            cell_valid = 1'b0;
            cell_data = 112'd0;
            cell_id = 14'd0;
            cell_frame_token = 32'd0;
            force_output_stall = 1'b0;
            late_error_arm = 1'b0;
        end
    endtask

    task clear_frame_metrics;
        begin
            rom_words_accepted = 0;
            rom_words_consumed = 0;
            rom_request_wait = 0;
            rom_response_wait = 0;
            adapter_queries = 0;
            adapter_latency_total = 0;
            adapter_latency_max = 0;
            adapter_accept_cycle = -1;
            output_seen = 0;
            done_seen = 0;
            start_accept_cycle = -1;
            seal_accept_cycle = -1;
            seal_ram_write_words = -1;
            last_output_cycle = -1;
            done_cycle = -1;
            nms_cycle_total = 0;
            nms_request_phase = 0;
            nms_response_phase = 0;
            nms_output_phase = 0;
            nms_multiply_phase = 0;
            nms_other_phase = 0;
            nms_request_stall = 0;
            nms_response_stall = 0;
            nms_output_stall = 0;
            late_error_used = 1'b0;
        end
    endtask

    task reset_dut;
        begin
            frame_monitor = 1'b0;
            nms_cycle_enable = 1'b0;
            clear_drives;
            i_rstn = 1'b0;
            repeat (4) @(negedge i_clk);
            i_rstn = 1'b1;
            repeat (3) @(negedge i_clk);
            if (!start_ready || c2_phase !== PHASE_FREE || c2_fault || nms_fault ||
                sealed_valid || read_rsp_valid || nms_entry_valid || nms_done)
                mark_error(100);
        end
    endtask

    task load_expected;
        input [4095:0] path_value;
        integer clear_index;
        begin
            for (clear_index = 0; clear_index < 64; clear_index = clear_index + 1)
                expected_words[clear_index] = 97'd0;
            if (expect_outputs > 0)
                $readmemh(path_value, expected_words, 0, expect_outputs - 1);
        end
    endtask

    task start_frame;
        integer watchdog;
        begin
            clear_frame_metrics;
            frame_number = frame_number + 1;
            watchdog = 0;
            @(negedge i_clk);
            start_frame_token = 32'h504f5300 + frame_number;
            start_model_id = MODEL_ID;
            start_valid = 1'b1;
            frame_monitor = 1'b1;
            while (!start_ready && watchdog < 10000) begin
                @(posedge i_clk);
                watchdog = watchdog + 1;
            end
            if (!start_ready)
                mark_error(110);
            @(posedge i_clk);
            @(negedge i_clk);
            start_valid = 1'b0;
        end
    endtask

    task send_cells;
        input [4095:0] path_value;
        input integer limit;
        integer cell_number;
        integer watchdog;
        begin
            head_handle = $fopen(path_value, "r");
            if (head_handle == 0)
                mark_error(120);
            for (cell_number = 0; cell_number < limit; cell_number = cell_number + 1) begin
                scan_result = $fscanf(head_handle, "%h\n", streamed_head);
                if (scan_result != 1) begin
                    mark_error(121);
                    cell_number = limit;
                end
                if (cell_number < limit) begin
                    if (stall_mode && (cell_number == 7 || (cell_number % 997) == 0)) begin
                        cell_valid = 1'b0;
                        repeat (cell_number == 7 ? 17 : 2) @(posedge i_clk);
                    end
                    watchdog = 0;
                    @(negedge i_clk);
                    cell_id = cell_number[13:0];
                    cell_frame_token = start_frame_token;
                    cell_data = streamed_head;
                    cell_valid = 1'b1;
                    while (!cell_ready && watchdog < 100000) begin
                        @(posedge i_clk);
                        watchdog = watchdog + 1;
                    end
                    if (!cell_ready)
                        mark_error(122);
                    @(posedge i_clk);
                    @(negedge i_clk);
                    cell_valid = 1'b0;
                end
            end
            if (head_handle != 0)
                $fclose(head_handle);
        end
    endtask

    task wait_for_done;
        integer watchdog;
        begin
            watchdog = 0;
            while (!nms_done && !nms_fault && !c2_fault && watchdog < 2000000) begin
                @(posedge i_clk);
                watchdog = watchdog + 1;
            end
            if (!nms_done || nms_fault || c2_fault)
                mark_error(130);
            repeat (4) @(posedge i_clk);
            if (c2_phase !== PHASE_FREE || !start_ready)
                mark_error(131);
            frame_monitor = 1'b0;
            nms_cycle_enable = 1'b0;
            if (output_seen != expect_outputs || nms_output_count != expect_outputs[6:0])
                mark_error(132);
            if (done_seen != 1)
                mark_error(133);
            if (done_cycle - start_accept_cycle > 2000000) begin
                budget_fail_count = budget_fail_count + 1;
                $display("TB_BUDGET_FAIL cycles=%0d allowance=2000000", done_cycle - start_accept_cycle);
            end
            if (nms_cycle_total != nms_request_phase + nms_response_phase + nms_output_phase +
                                    nms_multiply_phase + nms_other_phase)
                mark_error(135);
            if (nms_cycle_total != done_cycle - seal_accept_cycle)
                mark_error(136);
        end
    endtask

    task print_metrics;
        begin
            $display("JOINT_RESULT frame=%0d outputs=%0d start_to_seal=%0d seal_to_last=%0d seal_to_done=%0d start_to_last=%0d start_to_done=%0d",
                     frame_number, output_seen, seal_accept_cycle - start_accept_cycle,
                     (last_output_cycle < 0) ? -1 : last_output_cycle - seal_accept_cycle,
                     done_cycle - seal_accept_cycle,
                     (last_output_cycle < 0) ? -1 : last_output_cycle - start_accept_cycle,
                     done_cycle - start_accept_cycle);
            $display("ROM_RESULT accepted_words=%0d consumed_words=%0d request_wait=%0d response_wait=%0d adapter_queries=%0d adapter_latency_total=%0d adapter_latency_max=%0d drain_words=%0d",
                     rom_words_accepted, rom_words_consumed, rom_request_wait, rom_response_wait,
                     adapter_queries, adapter_latency_total, adapter_latency_max, drain_words);
            $display("C2_RESULT scan=%0d sort=%0d decode=%0d input_wait=%0d lut_wait=%0d ram_wait=%0d ram_read_words=%0d ram_write_words=%0d",
                     c2_scan_cycles, c2_sort_cycles, c2_decode_cycles, c2_input_wait_cycles,
                     c2_lut_wait_cycles, c2_ram_wait_cycles, c2_ram_read_words, c2_ram_write_words);
            $display("NMS_RESULT cycles=%0d request_phase=%0d response_phase=%0d multiply=%0d output_phase=%0d other=%0d request_stall=%0d response_stall=%0d output_stall=%0d",
                     nms_cycle_total, nms_request_phase, nms_response_phase, nms_multiply_phase,
                     nms_output_phase, nms_other_phase, nms_request_stall,
                     nms_response_stall, nms_output_stall);
        end
    endtask

    task run_complete;
        input [4095:0] active_head;
        begin
            start_frame;
            send_cells(active_head, 12096);
            wait_for_done;
            print_metrics;
            recovery_runs = recovery_runs + 1;
        end
    endtask

    task pulse_reset;
        begin
            frame_monitor = 1'b0;
            nms_cycle_enable = 1'b0;
            @(negedge i_clk);
            i_rstn = 1'b0;
            #1;
            if (sealed_valid || read_rsp_valid || nms_entry_valid || nms_done ||
                nms_sealed_ready || nms_read_valid || nms_response_ready)
                mark_error(140);
            repeat (3) @(negedge i_clk);
            i_rstn = 1'b1;
            repeat (3) @(negedge i_clk);
            if (!start_ready || c2_phase !== PHASE_FREE || c2_fault || nms_fault)
                mark_error(141);
        end
    endtask

    task pulse_cancel;
        begin
            frame_monitor = 1'b0;
            nms_cycle_enable = 1'b0;
            @(negedge i_clk);
            common_cancel = 1'b1;
            @(posedge i_clk);
            #1;
            if (sealed_valid || read_rsp_valid || nms_entry_valid || nms_done ||
                nms_sealed_ready || nms_read_valid || nms_response_ready)
                mark_error(142);
            @(negedge i_clk);
            common_cancel = 1'b0;
            repeat (3) @(negedge i_clk);
            if (!start_ready || c2_phase !== PHASE_FREE || c2_fault || nms_fault)
                mark_error(143);
        end
    endtask

    task recover_after_reset;
        begin
            pulse_reset;
            force_output_stall = 1'b0;
            late_error_arm = 1'b0;
            load_expected(expected_path);
            run_complete(head_path);
        end
    endtask

    task run_reset_case;
        begin
            start_frame;
            if (mode == 2) begin
                send_cells(head_path, 64);
                if (c2_phase !== PHASE_SCAN)
                    mark_error(150);
            end else begin
                if (mode == 6)
                    force_output_stall = 1'b1;
                send_cells(head_path, 12096);
                if (mode == 3) begin
                    while (c2_phase !== PHASE_SORT && !c2_fault) @(posedge i_clk);
                end else if (mode == 4) begin
                    while (c2_phase !== PHASE_DECODE && !c2_fault) @(posedge i_clk);
                end else if (mode == 5) begin
                    while (c9.state_current != c9.ST_MULTIPLY_CURRENT &&
                           c9.state_current != c9.ST_MULTIPLY_PREVIOUS &&
                           c9.state_current != c9.ST_MULTIPLY_INTERSECTION && !nms_fault) @(posedge i_clk);
                    repeat (7) @(posedge i_clk);
                end else begin
                    while (!nms_entry_valid && !nms_fault) @(posedge i_clk);
                    repeat (8) @(posedge i_clk);
                    if (!nms_entry_valid)
                        mark_error(151);
                end
            end
            recover_after_reset;
        end
    endtask

    task run_late_error;
        integer watchdog;
        begin
            late_error_arm = 1'b1;
            start_frame;
            send_cells(head_path, 12096);
            watchdog = 0;
            while (!nms_fault && watchdog < 2000000) begin
                @(posedge i_clk);
                watchdog = watchdog + 1;
            end
            if (!nms_fault || output_seen == 0 || !late_error_used)
                mark_error(160);
            if (nms_done || nms_output_count != 0 || nms_entry_valid)
                mark_error(161);
            repeat (3) @(posedge i_clk);
            if (!nms_fault || c2_phase !== PHASE_NMS)
                mark_error(162);
            pulse_cancel;
            late_error_arm = 1'b0;
            load_expected(expected_path);
            run_complete(head_path);
        end
    endtask

    task run_long_output_stall;
        begin
            force_output_stall = 1'b1;
            start_frame;
            send_cells(head_path, 12096);
            while (!nms_entry_valid && !nms_fault) @(posedge i_clk);
            repeat (128) @(posedge i_clk);
            if (!nms_entry_valid)
                mark_error(170);
            force_output_stall = 1'b0;
            wait_for_done;
            print_metrics;
            recovery_runs = recovery_runs + 1;
        end
    endtask

    // Common cancel deliberately does not clear the endpoint: accepted reads must drain.
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) begin
            rom_pending <= 1'b0;
            rom_delay <= 0;
            rom_response_valid <= 1'b0;
            rom_response_data <= 160'd0;
            rom_pending_address <= 13'd0;
        end else begin
            if (rom_response_valid && rom_response_ready)
                rom_response_valid <= 1'b0;
            if (rom_request_valid && rom_request_ready) begin
                if (rom_request_addr >= 7168)
                    mark_error(180);
                rom_pending <= 1'b1;
                rom_pending_address <= rom_request_addr;
                rom_delay <= stall_mode ? (1 + (lfsr[4:2] % 13)) : 1;
            end else if (rom_pending && rom_delay != 0) begin
                rom_delay <= rom_delay - 1;
            end else if (rom_pending && !rom_response_valid && !hold_rom_response) begin
                rom_pending <= 1'b0;
                rom_response_valid <= 1'b1;
                rom_response_data <= physical_words[rom_pending_address];
            end
        end
    end

    // Verify both physical-word holds and adapter identity, including canceled late returns.
    always @(posedge i_clk) begin
        if (!i_rstn) begin
            hold_rom_request <= 1'b0;
            hold_rom_word <= 1'b0;
        end else begin
            if (hold_rom_request && !common_cancel && !lut_cancel &&
                (!rom_request_valid || rom_request_addr !== held_rom_address))
                mark_error(181);
            if (hold_rom_word && (!rom_response_valid || rom_response_data !== held_rom_word))
                mark_error(182);
            hold_rom_request <= rom_request_valid && !rom_request_ready;
            held_rom_address <= rom_request_addr;
            hold_rom_word <= rom_response_valid && !rom_response_ready;
            held_rom_word <= rom_response_data;
            if (rom_response_valid && rom_response_ready && service.state_current == service.ST_DRAIN)
                drain_words = drain_words + 1;
            if (frame_monitor) begin
                if (rom_request_valid && rom_request_ready)
                    rom_words_accepted = rom_words_accepted + 1;
                if (rom_response_valid && rom_response_ready)
                    rom_words_consumed = rom_words_consumed + 1;
                if (rom_request_valid && !rom_request_ready)
                    rom_request_wait = rom_request_wait + 1;
                if (rom_pending && !rom_response_valid)
                    rom_response_wait = rom_response_wait + 1;
                if (lut_req_valid && lut_req_ready) begin
                    adapter_queries = adapter_queries + 1;
                    adapter_accept_cycle = cycle_count;
                end
                if (lut_rsp_valid && lut_rsp_ready) begin
                    if (lut_rsp_frame_token !== start_frame_token || lut_rsp_model_id !== MODEL_ID)
                        mark_error(183);
                    adapter_latency_total = adapter_latency_total + cycle_count - adapter_accept_cycle;
                    if (cycle_count - adapter_accept_cycle > adapter_latency_max)
                        adapter_latency_max = cycle_count - adapter_accept_cycle;
                end
            end
        end
    end

    task run_owned_rom_boundary;
        integer watchdog;
        integer before_drain;
        begin
            hold_rom_response = 1'b1;
            before_drain = drain_words;
            start_frame;
            send_cells(head_path, 1);
            watchdog = 0;
            while (!rom_pending && watchdog < 1000) begin
                @(negedge i_clk);
                watchdog = watchdog + 1;
            end
            if (!rom_pending)
                mark_error(210);
            if (mode == 9) begin
                pulse_cancel;
                if (!rom_pending || lut_req_ready || lut_rsp_valid)
                    mark_error(211);
                hold_rom_response = 1'b0;
                load_expected(expected_path);
                run_complete(head_path);
                if (drain_words != before_drain + 1)
                    mark_error(212);
            end else if (mode == 10) begin
                pulse_reset;
                hold_rom_response = 1'b0;
                if (rom_pending || rom_response_valid)
                    mark_error(213);
                load_expected(expected_path);
                run_complete(head_path);
            end else begin
                // Fault injection is at the controlled reader fault boundary, never a PH1P claim.
                rom_fault = 1'b1;
                repeat (6) @(negedge i_clk);
                if (!service_fault || !c2_fault)
                    mark_error(214);
                pulse_cancel;
                if (!service_fault)
                    mark_error(215);
                rom_fault = 1'b0;
                hold_rom_response = 1'b0;
                recover_after_reset;
            end
        end
    endtask

    always @(negedge i_clk) begin
        lfsr = {lfsr[30:0], lfsr[31] ^ lfsr[21] ^ lfsr[1] ^ lfsr[0]};
        if (!i_rstn || common_cancel)
            entry_ready = 1'b0;
        else if (force_output_stall)
            entry_ready = 1'b0;
        else
            entry_ready = !stall_mode || lfsr[2:0] != 3'b000;
    end

    always @(posedge i_clk) begin
        cycle_count = cycle_count + 1;
        if (cycle_count > max_cycles) begin
            mark_error(900);
            $fatal(1, "joint watchdog");
        end
        if (!i_rstn || common_cancel) begin
            hold_lut_request <= 1'b0;
            hold_seal <= 1'b0;
            hold_entry <= 1'b0;
        end else begin
            if (hold_lut_request && (!lut_req_valid || lut_req_kind !== hold_lut_kind ||
                lut_req_address !== hold_lut_address || lut_req_tag !== hold_lut_tag ||
                lut_req_frame_token !== hold_lut_frame || lut_req_model_id !== hold_lut_model))
                mark_error(190);
            hold_lut_request <= lut_req_valid && !lut_req_ready;
            hold_lut_kind <= lut_req_kind;
            hold_lut_address <= lut_req_address;
            hold_lut_tag <= lut_req_tag;
            hold_lut_frame <= lut_req_frame_token;
            hold_lut_model <= lut_req_model_id;
            if (hold_seal && (!sealed_valid || sealed_frame_token !== hold_seal_token ||
                count_person !== hold_seal_person || count_vehicle !== hold_seal_vehicle))
                mark_error(191);
            hold_seal <= sealed_valid && !nms_sealed_ready;
            hold_seal_token <= sealed_frame_token;
            hold_seal_person <= count_person;
            hold_seal_vehicle <= count_vehicle;
            if (hold_entry && (!nms_entry_valid || nms_entry_data !== hold_entry_data ||
                nms_frame_token !== hold_entry_token))
                mark_error(192);
            hold_entry <= nms_entry_valid && !entry_ready;
            hold_entry_data <= nms_entry_data;
            hold_entry_token <= nms_frame_token;
        end

        // Seal is excluded and done is included, so this occupancy interval is
        // exactly done_cycle - seal_accept_cycle cycles.
        if (nms_cycle_enable && i_rstn && !common_cancel) begin
            nms_cycle_total = nms_cycle_total + 1;
            if (c9.state_current == c9.ST_CURRENT_REQUEST || c9.state_current == c9.ST_PREVIOUS_REQUEST)
                nms_request_phase = nms_request_phase + 1;
            else if (c9.state_current == c9.ST_CURRENT_WAIT || c9.state_current == c9.ST_PREVIOUS_WAIT)
                nms_response_phase = nms_response_phase + 1;
            else if (c9.state_current == c9.ST_OUTPUT)
                nms_output_phase = nms_output_phase + 1;
            else if (c9.state_current == c9.ST_MULTIPLY_CURRENT ||
                     c9.state_current == c9.ST_MULTIPLY_PREVIOUS ||
                     c9.state_current == c9.ST_MULTIPLY_INTERSECTION)
                nms_multiply_phase = nms_multiply_phase + 1;
            else
                nms_other_phase = nms_other_phase + 1;
            if ((c9.state_current == c9.ST_CURRENT_REQUEST || c9.state_current == c9.ST_PREVIOUS_REQUEST) &&
                nms_read_valid && !read_req_ready)
                nms_request_stall = nms_request_stall + 1;
            if ((c9.state_current == c9.ST_CURRENT_WAIT || c9.state_current == c9.ST_PREVIOUS_WAIT) &&
                !read_rsp_valid)
                nms_response_stall = nms_response_stall + 1;
            if (c9.state_current == c9.ST_OUTPUT && nms_entry_valid && !entry_ready)
                nms_output_stall = nms_output_stall + 1;
        end

        if (frame_monitor && i_rstn && !common_cancel) begin
            if (start_valid && start_ready && start_accept_cycle < 0)
                start_accept_cycle = cycle_count;
            if (sealed_valid && nms_sealed_ready) begin
                seal_accept_cycle = cycle_count;
                seal_ram_write_words = c2_ram_write_words;
                nms_cycle_enable = 1'b1;
                if (sealed_frame_token !== start_frame_token || count_person !== expect_person[7:0] ||
                    count_vehicle !== expect_vehicle[7:0])
                    mark_error(200);
            end
            if (seal_ram_write_words >= 0 && !nms_done &&
                c2_ram_write_words != seal_ram_write_words)
                mark_error(203);
            if (nms_entry_valid && entry_ready) begin
                if (output_seen >= expect_outputs || nms_entry_data !== expected_words[output_seen] ||
                    nms_frame_token !== start_frame_token)
                    mark_error(201);
                output_seen = output_seen + 1;
                last_output_cycle = cycle_count;
            end
            if (injected_response_error && read_rsp_valid && nms_response_ready)
                late_error_used <= 1'b1;
            if (nms_done) begin
                done_seen = done_seen + 1;
                done_cycle = cycle_count;
                if (output_seen != expect_outputs || !finish_ready ||
                    nms_frame_token !== start_frame_token)
                    mark_error(202);
                nms_cycle_enable = 1'b0;
            end
        end
    end

    initial begin
        i_clk = 1'b0;
        i_rstn = 1'b0;
        fail_count = 0;
        cycle_count = 0;
        frame_number = 0;
        recovery_runs = 0;
        frame_monitor = 1'b0;
        nms_cycle_enable = 1'b0;
        rom_fault = 1'b0;
        rom_pending = 1'b0;
        rom_response_valid = 1'b0;
        hold_rom_response = 1'b0;
        hold_rom_request = 1'b0;
        hold_rom_word = 1'b0;
        drain_words = 0;
        budget_fail_count = 0;
        entry_ready = 1'b0;
        lfsr = 32'h7254a19d;
        hold_lut_request = 1'b0;
        hold_seal = 1'b0;
        hold_entry = 1'b0;
        clear_drives;
        if (!$value$plusargs("MODE=%d", mode) || !$value$plusargs("HEAD=%s", head_path) ||
            !$value$plusargs("EXPECTED=%s", expected_path) ||
            !$value$plusargs("EXPECT_PERSON=%d", expect_person) ||
            !$value$plusargs("EXPECT_VEHICLE=%d", expect_vehicle) ||
            !$value$plusargs("EXPECT_OUTPUTS=%d", expect_outputs) ||
            !$value$plusargs("PHYSICAL=%s", physical_path))
            $fatal(1, "missing joint plusargs");
        if (!$value$plusargs("STALL=%d", stall_mode)) stall_mode = 0;
        if (!$value$plusargs("MAX_CYCLES=%d", max_cycles)) max_cycles = 30000000;
        if (!$value$plusargs("HEAD2=%s", head2_path)) head2_path = head_path;
        if (!$value$plusargs("EXPECTED2=%s", expected2_path)) expected2_path = expected_path;
        if (!$value$plusargs("EXPECT2_PERSON=%d", expect2_person)) expect2_person = expect_person;
        if (!$value$plusargs("EXPECT2_VEHICLE=%d", expect2_vehicle)) expect2_vehicle = expect_vehicle;
        if (!$value$plusargs("EXPECT2_OUTPUTS=%d", expect2_outputs)) expect2_outputs = expect_outputs;
        $readmemh(physical_path, physical_words);
        load_expected(expected_path);
        reset_dut;
        if (mode == 0) begin
            run_complete(head_path);
        end else if (mode == 1) begin
            run_complete(head_path);
            expect_person = expect2_person;
            expect_vehicle = expect2_vehicle;
            expect_outputs = expect2_outputs;
            load_expected(expected2_path);
            run_complete(head2_path);
        end else if (mode >= 2 && mode <= 6) begin
            run_reset_case;
        end else if (mode == 7) begin
            run_late_error;
        end else if (mode == 8) begin
            run_long_output_stall;
        end else if (mode >= 9 && mode <= 11) begin
            run_owned_rom_boundary;
        end else begin
            mark_error(901);
        end
        frame_monitor = 1'b0;
        if (fail_count != 0)
            $fatal(1, "TB_FAIL failures=%0d mode=%0d", fail_count, mode);
        $display("TB_PASS_POSTPROCESS_REAL_ROM mode=%0d frames=%0d recoveries=%0d budget_failures=%0d", mode, frame_number, recovery_runs, budget_fail_count);
        $finish;
    end

endmodule

