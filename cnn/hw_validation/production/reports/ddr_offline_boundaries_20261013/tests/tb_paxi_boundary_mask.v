`timescale 1ns / 1ps

// Offline boundary, byte-mask, backpressure, and cancellation testbench.
module tb_paxi_boundary_mask;

    localparam [31:0]BASE_BYTE_ADDR = 32'h03400000;
    localparam [31:0]END_BYTE_ADDR = 32'h04000000;
    localparam integer MAX_SLOTS = 1024;

    reg clk = 1'b0;
    reg rstn = 1'b0;
    reg req_valid = 1'b0;
    reg req_write = 1'b0;
    reg [31:0]req_byte_addr = 32'd0;
    reg [127:0]req_write_data = 128'd0;
    reg [15:0]req_write_mask = 16'd0;
    reg [31:0]req_epoch = 32'd0;
    reg [31:0]req_owner = 32'd0;
    reg cancel = 1'b0;
    reg commit_confirmed = 1'b0;
    reg result_ready = 1'b0;
    reg paxi_arready = 1'b0;
    reg paxi_awready = 1'b0;
    reg paxi_wready = 1'b0;
    reg paxi_rvalid = 1'b0;
    reg paxi_rlast = 1'b0;
    reg [127:0]paxi_rdata = 128'd0;

    wire req_ready;
    wire result_valid;
    wire result_write;
    wire result_committed;
    wire [31:0]result_epoch;
    wire [31:0]result_owner;
    wire [127:0]result_read_data;
    wire paxi_accepted_valid;
    wire paxi_accepted_write;
    wire [31:0]paxi_accepted_epoch;
    wire [31:0]paxi_accepted_owner;
    wire drain_done;
    wire protocol_fault;
    wire [31:0]late_discard_count;
    wire [31:0]cancelled_drain_count;
    wire paxi_arvalid;
    wire [24:0]paxi_araddr;
    wire paxi_awvalid;
    wire [24:0]paxi_awaddr;
    wire paxi_wvalid;
    wire [127:0]paxi_wdata;
    wire [15:0]paxi_wmask;

    reg [31:0]slot_addresses [0:MAX_SLOTS - 1];
    reg [127:0]sparse_memory [0:MAX_SLOTS - 1];
    integer mode;
    integer vector_count;
    integer slot_count;
    integer random_seed = 32'h51b00da7;
    integer error_count = 0;
    integer vector_read_count = 0;
    integer vector_write_count = 0;
    integer invalid_count = 0;
    integer cancel_test_count = 0;
    integer cycle_count = 0;
    integer max_aw_wait = 0;
    integer max_w_wait = 0;
    integer max_ar_wait = 0;
    integer max_commit_wait = 0;
    integer max_return_wait = 0;
    integer max_result_wait = 0;
    integer vector_file;
    integer vector_index;
    integer fields_read;
    integer initialize_index;
    integer lane_index;
    integer observed_slot;
    integer issue_count_before;
    integer paxi_issue_count = 0;
    reg [3:0]vector_op;
    reg [31:0]vector_address;
    reg [15:0]vector_mask;
    reg [127:0]vector_write_data;
    reg [127:0]vector_expected_read;
    reg [31:0]vector_slot;
    reg [127:0]active_expected_write_data = 128'd0;
    reg [15:0]active_expected_write_mask = 16'd0;
    reg [31:0]active_expected_epoch = 32'd0;
    reg [31:0]active_expected_owner = 32'd0;

    always #5 clk = ~clk;

    always@(posedge clk)begin
        cycle_count = cycle_count + 1;
    end

    task report_error;
        input [8 * 160 - 1:0]message;
        begin
            error_count = error_count + 1;
            $display(" > ERR: [Verilog] %0s", message);
        end
    endtask

    task check_condition;
        input condition;
        input [8 * 160 - 1:0]message;
        begin
            if(condition !== 1'b1)begin
                report_error(message);
            end
        end
    endtask

    function integer find_slot;
        input [31:0]byte_address;
        integer search_index;
        begin
            find_slot = -1;
            for(search_index = 0; search_index < slot_count; search_index = search_index + 1)begin
                if(slot_addresses[search_index] == byte_address)begin
                    find_slot = search_index;
                end
            end
        end
    endfunction

    function integer delay_for;
        input integer phase;
        input integer item_index;
        integer random_value;
        begin
            if(mode == 0)begin
                delay_for = 0;
            end else if(mode == 1)begin
                random_value = $random(random_seed);
                delay_for = random_value & 7;
            end else if(((item_index + phase * 13) % 64) == 0)begin
                delay_for = 1024;
            end else begin
                delay_for = (item_index + phase) & 3;
            end
        end
    endfunction

    task coordinated_reset;
        begin
            @(negedge clk);
            rstn = 1'b0;
            req_valid = 1'b0;
            cancel = 1'b0;
            commit_confirmed = 1'b0;
            result_ready = 1'b0;
            paxi_arready = 1'b0;
            paxi_awready = 1'b0;
            paxi_wready = 1'b0;
            paxi_rvalid = 1'b0;
            paxi_rlast = 1'b0;
            repeat(3)@(posedge clk);
            @(negedge clk);
            rstn = 1'b1;
            repeat(2)@(posedge clk);
            check_condition(drain_done && !result_valid, "reset did not leave bridge drained");
        end
    endtask

    task send_request;
        input write_request;
        input [31:0]byte_address;
        input [127:0]write_data;
        input [15:0]write_mask;
        input [31:0]epoch;
        input [31:0]owner;
        begin
            while(!req_ready)@(negedge clk);
            req_write = write_request;
            req_byte_addr = byte_address;
            req_write_data = write_data;
            req_write_mask = write_mask;
            req_epoch = epoch;
            req_owner = owner;
            active_expected_write_data = write_data;
            active_expected_write_mask = write_mask;
            active_expected_epoch = epoch;
            active_expected_owner = owner;
            req_valid = 1'b1;
            @(posedge clk);
            check_condition(req_ready, "request was not accepted while ready was observed");
            @(negedge clk);
            req_valid = 1'b0;
            req_write = ~write_request;
            req_byte_addr = ~byte_address;
            req_write_data = ~write_data;
            req_write_mask = ~write_mask;
            req_epoch = ~epoch;
            req_owner = ~owner;
        end
    endtask

    task pulse_cancel;
        begin
            cancel = 1'b1;
            @(posedge clk);
            @(negedge clk);
            cancel = 1'b0;
        end
    endtask

    task accept_write_address;
        input integer stall_cycles;
        input [31:0]expected_address;
        input integer expected_slot;
        output integer actual_slot;
        integer stall_index;
        integer waited_cycles;
        reg [24:0]held_address;
        begin
            while(!paxi_awvalid)@(negedge clk);
            held_address = paxi_awaddr;
            check_condition(!paxi_wvalid, "WVALID appeared before AW acceptance");
            check_condition({paxi_awaddr, 1'b0} == expected_address,
                            "observed AW address did not match the request");
            actual_slot = find_slot({paxi_awaddr, 1'b0});
            check_condition(actual_slot == expected_slot, "observed AW address selected the wrong sparse slot");
            waited_cycles = 0;
            for(stall_index = 0; stall_index < stall_cycles; stall_index = stall_index + 1)begin
                @(negedge clk);
                waited_cycles = waited_cycles + 1;
                check_condition(paxi_awvalid && paxi_awaddr == held_address,
                                "AW payload changed or valid withdrew under backpressure");
                check_condition(!paxi_wvalid, "WVALID appeared while AW was blocked");
            end
            if(waited_cycles > max_aw_wait)begin
                max_aw_wait = waited_cycles;
            end
            paxi_awready = 1'b1;
            @(posedge clk);
            paxi_issue_count = paxi_issue_count + 1;
            @(negedge clk);
            paxi_awready = 1'b0;
            check_condition(paxi_wvalid, "WVALID was not presented after AW acceptance");
        end
    endtask

    task accept_write_data;
        input integer stall_cycles;
        input integer actual_slot;
        integer stall_index;
        integer waited_cycles;
        reg [127:0]held_data;
        reg [15:0]held_mask;
        begin
            held_data = paxi_wdata;
            held_mask = paxi_wmask;
            check_condition(held_data == active_expected_write_data &&
                            held_mask == active_expected_write_mask,
                            "observed W data or mask did not match the accepted request");
            waited_cycles = 0;
            for(stall_index = 0; stall_index < stall_cycles; stall_index = stall_index + 1)begin
                @(negedge clk);
                waited_cycles = waited_cycles + 1;
                check_condition(paxi_wvalid && paxi_wdata == held_data && paxi_wmask == held_mask,
                                "W payload changed or valid withdrew under backpressure");
            end
            if(waited_cycles > max_w_wait)begin
                max_w_wait = waited_cycles;
            end
            paxi_wready = 1'b1;
            @(posedge clk);
            check_condition(paxi_wvalid, "W handshake occurred without WVALID");
            check_condition(paxi_wdata == active_expected_write_data &&
                            paxi_wmask == active_expected_write_mask,
                            "W handshake data or mask did not transparently forward the request");
            if(actual_slot >= 0 && actual_slot < slot_count)begin
                for(lane_index = 0; lane_index < 16; lane_index = lane_index + 1)begin
                    if(paxi_wmask[lane_index] == 1'b0)begin
                        sparse_memory[actual_slot][lane_index * 8 +: 8] = paxi_wdata[lane_index * 8 +: 8];
                    end
                end
            end else begin
                report_error("accepted write address had no sparse-memory slot");
            end
            paxi_issue_count = paxi_issue_count + 1;
            @(negedge clk);
            paxi_wready = 1'b0;
            check_condition(paxi_accepted_valid && paxi_accepted_write,
                            "write acceptance telemetry was missing");
            check_condition(paxi_accepted_epoch == active_expected_epoch &&
                            paxi_accepted_owner == active_expected_owner,
                            "write acceptance telemetry epoch or owner was wrong");
        end
    endtask

    task provide_commit;
        input integer stall_cycles;
        integer stall_index;
        integer waited_cycles;
        begin
            waited_cycles = 0;
            for(stall_index = 0; stall_index < stall_cycles; stall_index = stall_index + 1)begin
                @(negedge clk);
                waited_cycles = waited_cycles + 1;
                check_condition(!result_valid && !drain_done,
                                "write completed without endpoint commit evidence");
            end
            if(waited_cycles > max_commit_wait)begin
                max_commit_wait = waited_cycles;
            end
            commit_confirmed = 1'b1;
            @(posedge clk);
            @(negedge clk);
            commit_confirmed = 1'b0;
        end
    endtask

    task accept_read_address;
        input integer stall_cycles;
        input [31:0]expected_address;
        input integer expected_slot;
        output integer actual_slot;
        integer stall_index;
        integer waited_cycles;
        reg [24:0]held_address;
        begin
            while(!paxi_arvalid)@(negedge clk);
            held_address = paxi_araddr;
            check_condition({paxi_araddr, 1'b0} == expected_address,
                            "observed AR address did not match the request");
            actual_slot = find_slot({paxi_araddr, 1'b0});
            check_condition(actual_slot == expected_slot, "observed AR address selected the wrong sparse slot");
            waited_cycles = 0;
            for(stall_index = 0; stall_index < stall_cycles; stall_index = stall_index + 1)begin
                @(negedge clk);
                waited_cycles = waited_cycles + 1;
                check_condition(paxi_arvalid && paxi_araddr == held_address,
                                "AR payload changed or valid withdrew under backpressure");
            end
            if(waited_cycles > max_ar_wait)begin
                max_ar_wait = waited_cycles;
            end
            paxi_arready = 1'b1;
            @(posedge clk);
            paxi_issue_count = paxi_issue_count + 1;
            @(negedge clk);
            paxi_arready = 1'b0;
            check_condition(paxi_accepted_valid && !paxi_accepted_write,
                            "read acceptance telemetry was missing");
            check_condition(paxi_accepted_epoch == active_expected_epoch &&
                            paxi_accepted_owner == active_expected_owner,
                            "read acceptance telemetry epoch or owner was wrong");
        end
    endtask

    task provide_read_return;
        input integer stall_cycles;
        input integer actual_slot;
        integer stall_index;
        integer waited_cycles;
        reg [127:0]endpoint_data;
        begin
            if(actual_slot >= 0 && actual_slot < slot_count)begin
                endpoint_data = sparse_memory[actual_slot];
            end else begin
                endpoint_data = 128'd0;
                report_error("accepted read address had no sparse-memory slot");
            end
            waited_cycles = 0;
            for(stall_index = 0; stall_index < stall_cycles; stall_index = stall_index + 1)begin
                @(negedge clk);
                waited_cycles = waited_cycles + 1;
                check_condition(!result_valid && !drain_done,
                                "read completed before endpoint return");
            end
            if(waited_cycles > max_return_wait)begin
                max_return_wait = waited_cycles;
            end
            paxi_rdata = endpoint_data;
            paxi_rlast = 1'b1;
            paxi_rvalid = 1'b1;
            @(posedge clk);
            @(negedge clk);
            paxi_rvalid = 1'b0;
            paxi_rlast = 1'b0;
            paxi_rdata = ~endpoint_data;
        end
    endtask

    task consume_result;
        input integer stall_cycles;
        input expected_write;
        input [31:0]expected_epoch;
        input [31:0]expected_owner;
        input [127:0]expected_data;
        integer stall_index;
        integer waited_cycles;
        reg held_write;
        reg held_committed;
        reg [31:0]held_epoch;
        reg [31:0]held_owner;
        reg [127:0]held_data;
        begin
            while(!result_valid)@(negedge clk);
            held_write = result_write;
            held_committed = result_committed;
            held_epoch = result_epoch;
            held_owner = result_owner;
            held_data = result_read_data;
            check_condition(result_write == expected_write, "result operation type was wrong");
            check_condition(result_committed == expected_write, "result committed flag was wrong");
            check_condition(result_epoch == expected_epoch && result_owner == expected_owner,
                            "result epoch or owner was wrong");
            if(!expected_write)begin
                check_condition(result_read_data == expected_data, "read result data mismatched the independent endpoint memory");
            end
            waited_cycles = 0;
            for(stall_index = 0; stall_index < stall_cycles; stall_index = stall_index + 1)begin
                @(negedge clk);
                waited_cycles = waited_cycles + 1;
                check_condition(result_valid && result_write == held_write &&
                                result_committed == held_committed && result_epoch == held_epoch &&
                                result_owner == held_owner && result_read_data == held_data,
                                "result payload changed or valid withdrew under backpressure");
            end
            if(waited_cycles > max_result_wait)begin
                max_result_wait = waited_cycles;
            end
            result_ready = 1'b1;
            @(posedge clk);
            @(negedge clk);
            result_ready = 1'b0;
            check_condition(drain_done && !result_valid, "result handshake did not drain the bridge");
        end
    endtask

    task execute_write_vector;
        input integer item_index;
        input [31:0]byte_address;
        input [15:0]write_mask;
        input [127:0]write_data;
        input [127:0]expected_after_write;
        input integer expected_slot;
        reg [31:0]epoch;
        reg [31:0]owner;
        integer actual_slot;
        begin
            epoch = 32'hb0000000 | mode;
            owner = item_index + 1;
            send_request(1'b1, byte_address, write_data, write_mask, epoch, owner);
            accept_write_address(delay_for(0, item_index), byte_address, expected_slot, actual_slot);
            accept_write_data(delay_for(1, item_index), actual_slot);
            if(actual_slot >= 0 && actual_slot < slot_count)begin
                check_condition(sparse_memory[actual_slot] == expected_after_write,
                                "masked write result mismatched vector expectation");
            end
            provide_commit(delay_for(3, item_index));
            consume_result(delay_for(4, item_index), 1'b1, epoch, owner, 128'd0);
            vector_write_count = vector_write_count + 1;
        end
    endtask

    task execute_read_vector;
        input integer item_index;
        input [31:0]byte_address;
        input [127:0]expected_read;
        input integer expected_slot;
        reg [31:0]epoch;
        reg [31:0]owner;
        integer actual_slot;
        begin
            epoch = 32'hb0000000 | mode;
            owner = item_index + 1;
            send_request(1'b0, byte_address, 128'd0, 16'd0, epoch, owner);
            accept_read_address(delay_for(2, item_index), byte_address, expected_slot, actual_slot);
            provide_read_return(delay_for(3, item_index), actual_slot);
            consume_result(delay_for(4, item_index), 1'b0, epoch, owner, expected_read);
            vector_read_count = vector_read_count + 1;
        end
    endtask

    task execute_invalid_vector;
        input integer item_index;
        input write_request;
        input [31:0]byte_address;
        input [127:0]write_data;
        input [15:0]write_mask;
        integer wait_index;
        begin
            issue_count_before = paxi_issue_count;
            send_request(write_request, byte_address, write_data, write_mask,
                         32'hd0000000 | mode, item_index + 1);
            for(wait_index = 0; wait_index < 4; wait_index = wait_index + 1)begin
                @(negedge clk);
                check_condition(!paxi_awvalid && !paxi_wvalid && !paxi_arvalid,
                                "invalid request reached a PAXI channel");
            end
            check_condition(protocol_fault, "invalid request did not enter sticky fault state");
            check_condition(paxi_issue_count == issue_count_before,
                            "invalid request caused an endpoint handshake");
            invalid_count = invalid_count + 1;
            coordinated_reset();
        end
    endtask

    task wait_cancelled_drain;
        integer wait_index;
        begin
            while(!drain_done)begin
                @(negedge clk);
                check_condition(!result_valid, "cancelled transaction published a result before drain");
            end
            for(wait_index = 0; wait_index < 2; wait_index = wait_index + 1)begin
                @(negedge clk);
                check_condition(!result_valid, "cancelled transaction leaked an old result");
            end
        end
    endtask

    task probe_next_owner;
        input integer probe_index;
        input [31:0]byte_address;
        input integer expected_slot;
        integer actual_slot;
        reg [31:0]epoch;
        reg [31:0]owner;
        begin
            epoch = 32'he0000000 | mode;
            owner = 32'he1000000 + probe_index;
            send_request(1'b0, byte_address, 128'd0, 16'd0, epoch, owner);
            accept_read_address(0, byte_address, expected_slot, actual_slot);
            provide_read_return(0, actual_slot);
            consume_result(1, 1'b0, epoch, owner, sparse_memory[expected_slot]);
        end
    endtask

    task run_cancel_case;
        input integer cancel_phase;
        input [31:0]byte_address;
        input integer expected_slot;
        integer actual_slot;
        integer hold_index;
        reg [31:0]epoch;
        reg [31:0]owner;
        reg [127:0]cancel_data;
        reg [24:0]held_address;
        reg [127:0]held_data;
        reg [15:0]held_mask;
        reg held_result_write;
        reg held_result_committed;
        reg [127:0]held_result_data;
        begin
            epoch = 32'hc0000000 | mode;
            owner = 32'hc1000000 + cancel_phase;
            cancel_data = {32'hca110000 + cancel_phase, 32'h76543210,
                           32'h89abcdef, 32'h01234567};
            if(cancel_phase == 0)begin
                send_request(1'b1, byte_address, cancel_data, 16'h0000, epoch, owner);
                while(!paxi_awvalid)@(negedge clk);
                held_address = paxi_awaddr;
                check_condition(!paxi_wvalid, "cancel-AW case presented W before AW");
                pulse_cancel();
                for(hold_index = 0; hold_index < 1024; hold_index = hold_index + 1)begin
                    @(negedge clk);
                    check_condition(paxi_awvalid && paxi_awaddr == held_address && !paxi_wvalid,
                                    "cancel-AW backpressure was not stable");
                    check_condition(!req_ready && !drain_done,
                                    "cancel-AW wait released ownership before endpoint acceptance");
                end
                if(1024 > max_aw_wait)begin
                    max_aw_wait = 1024;
                end
                accept_write_address(0, byte_address, expected_slot, actual_slot);
                accept_write_data(1, actual_slot);
                provide_commit(1);
            end else if(cancel_phase == 1)begin
                send_request(1'b1, byte_address, cancel_data, 16'h00f0, epoch, owner);
                accept_write_address(0, byte_address, expected_slot, actual_slot);
                while(!paxi_wvalid)@(negedge clk);
                held_data = paxi_wdata;
                held_mask = paxi_wmask;
                pulse_cancel();
                for(hold_index = 0; hold_index < 1024; hold_index = hold_index + 1)begin
                    @(negedge clk);
                    check_condition(paxi_wvalid && paxi_wdata == held_data && paxi_wmask == held_mask,
                                    "cancel-W backpressure changed or withdrew its payload");
                    check_condition(!req_ready && !drain_done,
                                    "cancel-W wait released ownership before endpoint acceptance");
                end
                if(1024 > max_w_wait)begin
                    max_w_wait = 1024;
                end
                accept_write_data(0, actual_slot);
                provide_commit(1);
            end else if(cancel_phase == 2)begin
                send_request(1'b0, byte_address, 128'd0, 16'd0, epoch, owner);
                while(!paxi_arvalid)@(negedge clk);
                held_address = paxi_araddr;
                pulse_cancel();
                for(hold_index = 0; hold_index < 1024; hold_index = hold_index + 1)begin
                    @(negedge clk);
                    check_condition(paxi_arvalid && paxi_araddr == held_address,
                                    "cancel-AR backpressure changed or withdrew its payload");
                    check_condition(!req_ready && !drain_done,
                                    "cancel-AR wait released ownership before endpoint acceptance");
                end
                if(1024 > max_ar_wait)begin
                    max_ar_wait = 1024;
                end
                accept_read_address(0, byte_address, expected_slot, actual_slot);
                provide_read_return(1, actual_slot);
            end else if(cancel_phase == 3)begin
                send_request(1'b1, byte_address, cancel_data, 16'h5555, epoch, owner);
                accept_write_address(0, byte_address, expected_slot, actual_slot);
                accept_write_data(0, actual_slot);
                pulse_cancel();
                for(hold_index = 0; hold_index < 1024; hold_index = hold_index + 1)begin
                    @(negedge clk);
                    check_condition(!req_ready && !drain_done && !result_valid,
                                    "cancel-commit wait retired without endpoint commit");
                end
                if(1024 > max_commit_wait)begin
                    max_commit_wait = 1024;
                end
                provide_commit(0);
            end else if(cancel_phase == 4)begin
                send_request(1'b0, byte_address, 128'd0, 16'd0, epoch, owner);
                accept_read_address(0, byte_address, expected_slot, actual_slot);
                pulse_cancel();
                for(hold_index = 0; hold_index < 1024; hold_index = hold_index + 1)begin
                    @(negedge clk);
                    check_condition(!req_ready && !drain_done && !result_valid,
                                    "cancel-return wait retired without endpoint return");
                end
                if(1024 > max_return_wait)begin
                    max_return_wait = 1024;
                end
                provide_read_return(0, actual_slot);
            end else begin
                send_request(1'b0, byte_address, 128'd0, 16'd0, epoch, owner);
                accept_read_address(0, byte_address, expected_slot, actual_slot);
                provide_read_return(0, actual_slot);
                while(!result_valid)@(negedge clk);
                held_result_write = result_write;
                held_result_committed = result_committed;
                held_result_data = result_read_data;
                for(hold_index = 0; hold_index < 1024; hold_index = hold_index + 1)begin
                    @(negedge clk);
                    check_condition(result_valid && result_write == held_result_write &&
                                    result_committed == held_result_committed &&
                                    result_epoch == epoch && result_owner == owner &&
                                    result_read_data == held_result_data,
                                    "cancel-result case did not hold ownership");
                    check_condition(!req_ready && !drain_done,
                                    "cancel-result backpressure released ownership before cancellation");
                end
                if(1024 > max_result_wait)begin
                    max_result_wait = 1024;
                end
                pulse_cancel();
            end
            wait_cancelled_drain();
            cancel_test_count = cancel_test_count + 1;
            probe_next_owner(cancel_phase, byte_address, expected_slot);
        end
    endtask

    initial begin
        if(!$value$plusargs("MODE=%d", mode) || !$value$plusargs("COUNT=%d", vector_count) ||
           !$value$plusargs("SLOTS=%d", slot_count))begin
            $display("PAXI_BOUNDARY_FAIL missing +MODE, +COUNT, or +SLOTS");
            $finish;
        end
        if(mode < 0 || mode > 2 || vector_count <= 0 || slot_count <= 0 || slot_count > MAX_SLOTS)begin
            $display("PAXI_BOUNDARY_FAIL invalid plusargs mode=%0d count=%0d slots=%0d",
                     mode, vector_count, slot_count);
            $finish;
        end
        for(initialize_index = 0; initialize_index < MAX_SLOTS; initialize_index = initialize_index + 1)begin
            slot_addresses[initialize_index] = 32'hxxxxxxxx;
            sparse_memory[initialize_index] = 128'd0;
        end
        $readmemh("addresses.hex", slot_addresses);
        vector_file = $fopen("vectors.txt", "r");
        if(vector_file == 0)begin
            $display("PAXI_BOUNDARY_FAIL could not open vectors.txt");
            $finish;
        end
        coordinated_reset();
        for(vector_index = 0; vector_index < vector_count; vector_index = vector_index + 1)begin
            fields_read = $fscanf(vector_file, "%h %h %h %h %h %h\n", vector_op,
                                  vector_address, vector_mask, vector_write_data,
                                  vector_expected_read, vector_slot);
            if(fields_read != 6)begin
                $display(" > ERR: [Verilog] malformed vector index=%0d fields=%0d", vector_index, fields_read);
                error_count = error_count + 1;
                vector_index = vector_count;
            end else if(vector_slot >= slot_count)begin
                $display(" > ERR: [Verilog] vector slot out of range index=%0d slot=%0d", vector_index, vector_slot);
                error_count = error_count + 1;
            end else begin
                check_condition(slot_addresses[vector_slot] == vector_address,
                                "vector address did not match addresses.hex slot");
                case(vector_op)
                    4'h0: begin
                        check_condition(vector_address >= BASE_BYTE_ADDR && vector_address < END_BYTE_ADDR &&
                                        vector_address[3:0] == 4'd0, "valid read vector had an invalid address");
                        execute_read_vector(vector_index, vector_address, vector_expected_read, vector_slot);
                    end
                    4'h1: begin
                        check_condition(vector_address >= BASE_BYTE_ADDR && vector_address < END_BYTE_ADDR &&
                                        vector_address[3:0] == 4'd0, "valid write vector had an invalid address");
                        execute_write_vector(vector_index, vector_address, vector_mask, vector_write_data,
                                             vector_expected_read, vector_slot);
                    end
                    4'h2: begin
                        check_condition(!(vector_address >= BASE_BYTE_ADDR && vector_address < END_BYTE_ADDR &&
                                          vector_address[3:0] == 4'd0), "invalid read vector was actually legal");
                        execute_invalid_vector(vector_index, 1'b0, vector_address, vector_write_data, vector_mask);
                    end
                    4'h3: begin
                        check_condition(!(vector_address >= BASE_BYTE_ADDR && vector_address < END_BYTE_ADDR &&
                                          vector_address[3:0] == 4'd0), "invalid write vector was actually legal");
                        execute_invalid_vector(vector_index, 1'b1, vector_address, vector_write_data, vector_mask);
                    end
                    default: begin
                        $display(" > ERR: [Verilog] unknown op index=%0d op=%0h", vector_index, vector_op);
                        error_count = error_count + 1;
                    end
                endcase
            end
        end
        $fclose(vector_file);
        coordinated_reset();
        for(vector_index = 0; vector_index < 6; vector_index = vector_index + 1)begin
            run_cancel_case(vector_index, slot_addresses[0], 0);
        end
        $display("SUMMARY mode=%0d vectors=%0d reads=%0d writes=%0d invalid=%0d cancels=%0d errors=%0d cycles=%0d max_aw=%0d max_w=%0d max_ar=%0d max_commit=%0d max_return=%0d max_result=%0d",
                 mode, vector_count, vector_read_count, vector_write_count,
                 invalid_count, cancel_test_count, error_count, cycle_count,
                 max_aw_wait, max_w_wait, max_ar_wait, max_commit_wait,
                 max_return_wait, max_result_wait);
        if(error_count == 0 && vector_read_count + vector_write_count + invalid_count == vector_count &&
           cancel_test_count == 6)begin
            $display("PAXI_BOUNDARY_PASS");
        end else begin
            $display("PAXI_BOUNDARY_FAIL");
        end
        $finish;
    end

    initial begin
        repeat(3000000)@(posedge clk);
        $display(" > ERR: [Verilog] timeout mode=%0d", mode);
        $display("PAXI_BOUNDARY_FAIL");
        $finish;
    end

    paxi_single_outstanding_bridge dut(
        .i_clk(clk),
        .i_rstn(rstn),
        .i_req_valid(req_valid),
        .i_req_write(req_write),
        .i_req_byte_addr(req_byte_addr),
        .i_req_write_data(req_write_data),
        .i_req_write_mask(req_write_mask),
        .i_req_epoch(req_epoch),
        .i_req_owner(req_owner),
        .i_cancel(cancel),
        .o_req_ready(req_ready),
        .i_commit_confirmed(commit_confirmed),
        .i_result_ready(result_ready),
        .o_result_valid(result_valid),
        .o_result_write(result_write),
        .o_result_committed(result_committed),
        .o_result_epoch(result_epoch),
        .o_result_owner(result_owner),
        .o_result_read_data(result_read_data),
        .o_paxi_accepted_valid(paxi_accepted_valid),
        .o_paxi_accepted_write(paxi_accepted_write),
        .o_paxi_accepted_epoch(paxi_accepted_epoch),
        .o_paxi_accepted_owner(paxi_accepted_owner),
        .o_drain_done(drain_done),
        .o_protocol_fault(protocol_fault),
        .o_late_discard_count(late_discard_count),
        .o_cancelled_drain_count(cancelled_drain_count),
        .i_paxi_arready(paxi_arready),
        .o_paxi_arvalid(paxi_arvalid),
        .o_paxi_araddr(paxi_araddr),
        .i_paxi_awready(paxi_awready),
        .o_paxi_awvalid(paxi_awvalid),
        .o_paxi_awaddr(paxi_awaddr),
        .i_paxi_wready(paxi_wready),
        .o_paxi_wvalid(paxi_wvalid),
        .o_paxi_wdata(paxi_wdata),
        .o_paxi_wmask(paxi_wmask),
        .i_paxi_rvalid(paxi_rvalid),
        .i_paxi_rlast(paxi_rlast),
        .i_paxi_rdata(paxi_rdata)
    );

endmodule
