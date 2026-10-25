`timescale 1ns / 1ps

// 受控PAXI端点逐条核对独立文本向量；它不是DDR器件或写完成屏障模型。
module tb_ddr_selftest;
    localparam [3:0] ST_WAIT = 4'd0;
    localparam [3:0] ST_FETCH = 4'd1;
    localparam [3:0] ST_LOAD = 4'd2;
    localparam [3:0] ST_ISSUE = 4'd3;
    localparam [3:0] ST_WRITE = 4'd4;
    localparam [3:0] ST_READ_ADDR = 4'd5;
    localparam [3:0] ST_READ_DATA = 4'd6;
    localparam [3:0] ST_CHECK = 4'd7;
    localparam [3:0] ST_ADVANCE = 4'd8;
    localparam [3:0] ST_PASS = 4'd9;
    localparam [3:0] ST_FAIL = 4'd10;

    reg clk = 1'b0;
    reg rstn = 1'b0;
    reg phy_ready = 1'b0;
    reg awready = 1'b0;
    reg wready = 1'b0;
    reg arready = 1'b0;
    reg response_valid = 1'b0;
    reg [127:0] response_data = 128'd0;
    reg response_last = 1'b1;
    reg unsolicited_valid = 1'b0;
    wire [24:0] awaddr;
    wire awvalid;
    wire [127:0] wdata;
    wire [15:0] wstrb;
    wire wvalid;
    wire wlast;
    wire [24:0] araddr;
    wire arvalid;
    wire rready;
    wire [1:0] status;
    wire [3:0] error_kind;
    wire [3:0] state_value;
    wire [9:0] writes;
    wire [9:0] reads;
    wire [24:0] address;
    wire [127:0] expected_data;
    wire [127:0] actual_data;
    wire [31:0] cycles;
    wire [31:0] init_cycles;
    wire [31:0] wait_both;
    wire [31:0] wait_aw;
    wire [31:0] wait_w;
    wire [31:0] wait_ar;
    wire [31:0] wait_r;
    wire same_edge_response;
    wire rvalid;
    wire rlast;
    wire [127:0] rdata;

    reg command_write [0:1055];
    reg [25:0] command_byte_address [0:1055];
    reg [24:0] command_native_address [0:1055];
    reg [15:0] command_mask [0:1055];
    reg [127:0] command_data [0:1055];
    reg [127:0] command_expected [0:1055];
    reg [7:0] command_slot [0:1055];
    integer write_order [0:527];
    integer read_order [0:527];
    reg [24:0] slot_address [0:193];
    reg slot_seen [0:193];
    reg [127:0] storage [0:193];

    reg pending_aw = 1'b0;
    reg pending_w = 1'b0;
    reg pending_read = 1'b0;
    reg [24:0] held_aw = 25'd0;
    reg [127:0] held_w = 128'd0;
    reg [15:0] held_mask = 16'd0;
    integer held_aw_command = 0;
    integer held_w_command = 0;
    integer held_read_slot = 0;
    integer read_delay = 0;

    reg blocked_aw = 1'b0;
    reg blocked_w = 1'b0;
    reg blocked_ar = 1'b0;
    reg blocked_r = 1'b0;
    reg [24:0] previous_awaddr = 25'd0;
    reg [127:0] previous_wdata = 128'd0;
    reg [15:0] previous_wstrb = 16'd0;
    reg [24:0] previous_araddr = 25'd0;
    reg [127:0] previous_rdata = 128'd0;
    reg previous_rlast = 1'b0;

    integer test_case = 0;
    integer active_mode = 0;
    integer expected_error = 0;
    integer tick = 0;
    integer aw_count = 0;
    integer w_count = 0;
    integer ar_count = 0;
    integer r_count = 0;
    integer long_write_left = 1024;
    integer long_ar_left = 1024;
    reg [15:0] lfsr = 16'h1ace;

    integer vector_file;
    integer scan_result;
    integer load_index;
    integer write_index;
    integer read_index;
    integer loop_index;
    integer byte_index;
    integer current_command;
    integer current_slot;
    integer ignored;
    reg scan_write;
    reg [25:0] scan_address;
    reg [15:0] scan_mask;
    reg [127:0] scan_data;
    reg [127:0] scan_expected;
    reg [7:0] scan_slot;

    reg monitor_valid = 1'b0;
    reg [3:0] previous_state = ST_WAIT;
    reg [31:0] previous_cycles = 32'd0;
    reg [31:0] previous_init_cycles = 32'd0;
    reg [31:0] previous_wait_both = 32'd0;
    reg [31:0] previous_wait_aw = 32'd0;
    reg [31:0] previous_wait_w = 32'd0;
    reg [31:0] previous_wait_ar = 32'd0;
    reg [31:0] previous_wait_r = 32'd0;
    integer run_delta;
    integer init_delta;
    integer both_delta;
    integer aw_delta;
    integer w_delta;
    integer ar_delta;
    integer r_delta;

    reg [24:0] terminal_address;
    reg [127:0] terminal_expected;
    reg [127:0] terminal_actual;
    reg [3:0] terminal_error;
    reg [9:0] terminal_writes;
    reg [9:0] terminal_reads;
    reg [31:0] terminal_cycles;
    reg [31:0] terminal_init_cycles;
    reg [31:0] terminal_wait_both;
    reg [31:0] terminal_wait_aw;
    reg [31:0] terminal_wait_w;
    reg [31:0] terminal_wait_ar;
    reg [31:0] terminal_wait_r;

    always #4 clk = ~clk;

    function integer find_slot;
        input [24:0] native_address;
        integer search_index;
        begin
            find_slot = -1;
            for (search_index = 0; search_index < 194; search_index = search_index + 1) begin
                if (slot_seen[search_index] && (slot_address[search_index] == native_address)) begin
                    find_slot = search_index;
                end
            end
        end
    endfunction

    assign same_edge_response = (active_mode == 5) && arvalid && arready;
    assign rvalid = response_valid || same_edge_response || unsolicited_valid;
    assign rlast = same_edge_response ? 1'b1 : (unsolicited_valid ? 1'b1 : response_last);
    assign rdata = same_edge_response ? storage[find_slot(araddr)] :
                   (unsolicited_valid ? 128'h756e65787065637465645f726573706f : response_data);

    road_ddr_selftest #(.C_TIMEOUT(27'd1100)) dut (
        .i_clk(clk), .i_rstn(rstn), .i_phy_ready(phy_ready),
        .i_awready(awready), .i_wready(wready), .i_arready(arready),
        .i_rvalid(rvalid), .i_rlast(rlast), .i_rdata(rdata),
        .o_awaddr(awaddr), .o_awvalid(awvalid), .o_wdata(wdata), .o_wstrb(wstrb),
        .o_wvalid(wvalid), .o_wlast(wlast), .o_araddr(araddr), .o_arvalid(arvalid),
        .o_rready(rready), .o_status(status), .o_error(error_kind), .o_state(state_value),
        .o_writes(writes), .o_reads(reads), .o_address(address),
        .o_expected(expected_data), .o_actual(actual_data), .o_cycles(cycles),
        .o_init_cycles(init_cycles), .o_wait_both(wait_both), .o_wait_aw(wait_aw),
        .o_wait_w(wait_w), .o_wait_ar(wait_ar), .o_wait_r(wait_r)
    );

    // 许可只在下降沿改变，避免与DUT和端点的上升沿采样竞争。
    always @(negedge clk) begin
        if (!rstn) begin
            phy_ready = 1'b0;
            awready = 1'b0;
            wready = 1'b0;
            arready = 1'b0;
            unsolicited_valid = 1'b0;
        end else begin
            phy_ready = (tick >= 4) && (active_mode != 8);
            awready = 1'b1;
            wready = 1'b1;
            arready = 1'b1;
            case (active_mode)
                1: begin
                    awready = !pending_aw;
                    wready = pending_aw;
                end
                2: begin
                    awready = pending_w;
                    wready = !pending_w;
                end
                3: begin
                    lfsr = {lfsr[14:0], lfsr[15] ^ lfsr[13] ^ lfsr[12] ^ lfsr[10]};
                    awready = lfsr[0];
                    wready = lfsr[3];
                    arready = lfsr[7];
                end
                4: begin
                    if ((aw_count == 0) && (w_count == 0) && awvalid && (long_write_left != 0)) begin
                        awready = 1'b0;
                        wready = 1'b0;
                        long_write_left = long_write_left - 1;
                    end
                    if ((ar_count == 0) && arvalid && (long_ar_left != 0)) begin
                        arready = 1'b0;
                        long_ar_left = long_ar_left - 1;
                    end
                end
                9: awready = 1'b0;
                10: wready = 1'b0;
                11: arready = 1'b0;
                15: wready = 1'b0;
                16: awready = 1'b0;
                default: begin
                    awready = awready;
                    wready = wready;
                    arready = arready;
                end
            endcase
            if ((active_mode == 13) && (writes == 10'd1)) begin
                unsolicited_valid = 1'b1;
            end
            if ((active_mode == 14) && (writes == 10'd1)) begin
                phy_ready = 1'b0;
            end
            if ((active_mode == 22) && (status == 2'd1)) begin
                unsolicited_valid = 1'b1;
            end
        end
    end

    // 独立端点逐握手核对命令，并在194个稀疏槽内执行高有效字节屏蔽。
    always @(posedge clk or negedge rstn) begin
        if (!rstn) begin
            tick = 0;
            aw_count = 0;
            w_count = 0;
            ar_count = 0;
            r_count = 0;
            pending_aw = 1'b0;
            pending_w = 1'b0;
            pending_read = 1'b0;
            response_valid <= 1'b0;
            response_data <= 128'd0;
            response_last <= 1'b1;
            blocked_aw = 1'b0;
            blocked_w = 1'b0;
            blocked_ar = 1'b0;
            blocked_r = 1'b0;
            read_delay = 0;
            long_write_left = 1024;
            long_ar_left = 1024;
            lfsr = 16'h1ace;
            for (loop_index = 0; loop_index < 194; loop_index = loop_index + 1) begin
                storage[loop_index] = 128'd0;
            end
        end else begin
            tick = tick + 1;
            if (blocked_aw && (status == 2'd0) && (!awvalid || (awaddr !== previous_awaddr))) begin
                $fatal(1, "AW changed before acceptance");
            end
            if (blocked_w && (status == 2'd0) && (!wvalid || (wdata !== previous_wdata) ||
                              (wstrb !== previous_wstrb) || !wlast)) begin
                $fatal(1, "W changed before acceptance");
            end
            if (blocked_ar && (status == 2'd0) && (!arvalid || (araddr !== previous_araddr))) begin
                $fatal(1, "AR changed before acceptance");
            end
            if (blocked_r && (status == 2'd0) && (!rvalid || (rdata !== previous_rdata) || (rlast !== previous_rlast))) begin
                $fatal(1, "Controlled response changed before acceptance");
            end
            blocked_aw = awvalid && !awready;
            blocked_w = wvalid && !wready;
            blocked_ar = arvalid && !arready;
            blocked_r = rvalid && !rready && (status == 2'd0);
            previous_awaddr = awaddr;
            previous_wdata = wdata;
            previous_wstrb = wstrb;
            previous_araddr = araddr;
            previous_rdata = rdata;
            previous_rlast = rlast;

            if (rvalid && rready) begin
                if (r_count >= 528) begin
                    $fatal(1, "Duplicate read response");
                end
                current_command = read_order[r_count];
                if ((active_mode != 6) && (rdata !== command_expected[current_command])) begin
                    $fatal(1, "Endpoint returned wrong command data index=%0d", current_command);
                end
                r_count = r_count + 1;
                response_valid <= 1'b0;
                pending_read = 1'b0;
            end
            if (awvalid && awready) begin
                if (pending_aw || (aw_count >= 528)) begin
                    $fatal(1, "Duplicate AW transaction");
                end
                current_command = write_order[aw_count];
                if (awaddr !== command_native_address[current_command]) begin
                    $fatal(1, "Wrong AW address command=%0d got=%h expected=%h", current_command, awaddr, command_native_address[current_command]);
                end
                held_aw = awaddr;
                held_aw_command = current_command;
                pending_aw = 1'b1;
                aw_count = aw_count + 1;
            end
            if (wvalid && wready) begin
                if (pending_w || (w_count >= 528)) begin
                    $fatal(1, "Duplicate W transaction");
                end
                current_command = write_order[w_count];
                if ((wdata !== command_data[current_command]) ||
                    (wstrb !== command_mask[current_command]) || !wlast) begin
                    $fatal(1, "Wrong W payload command=%0d", current_command);
                end
                held_w = wdata;
                held_mask = wstrb;
                held_w_command = current_command;
                pending_w = 1'b1;
                w_count = w_count + 1;
            end
            if (pending_aw && pending_w) begin
                if (held_aw_command != held_w_command) begin
                    $fatal(1, "AW and W paired from different commands");
                end
                current_slot = command_slot[held_aw_command];
                if ((current_slot < 0) || (current_slot >= 194) ||
                    (held_aw !== slot_address[current_slot])) begin
                    $fatal(1, "Write used inconsistent sparse slot");
                end
                for (byte_index = 0; byte_index < 16; byte_index = byte_index + 1) begin
                    if (!held_mask[byte_index]) begin
                        storage[current_slot][byte_index * 8 +: 8] = held_w[byte_index * 8 +: 8];
                    end
                end
                if (storage[current_slot] !== command_expected[held_aw_command]) begin
                    $fatal(1, "Byte mask result mismatch command=%0d", held_aw_command);
                end
                pending_aw = 1'b0;
                pending_w = 1'b0;
            end
            if (arvalid && arready) begin
                if (pending_read || (ar_count >= 528)) begin
                    $fatal(1, "Duplicate or overlapping AR transaction");
                end
                current_command = read_order[ar_count];
                current_slot = command_slot[current_command];
                if ((araddr !== command_native_address[current_command]) ||
                    (current_slot < 0) || (current_slot >= 194) ||
                    (storage[current_slot] !== command_expected[current_command])) begin
                    $fatal(1, "Wrong AR address or independent stored value command=%0d", current_command);
                end
                ar_count = ar_count + 1;
                if (active_mode != 5) begin
                    pending_read = 1'b1;
                    held_read_slot = current_slot;
                    read_delay = ((active_mode == 4) && (ar_count == 1)) ? 1024 : 2;
                end
            end
            if (pending_read && !response_valid && (active_mode != 12) && (active_mode != 17)) begin
                if (read_delay == 0) begin
                    response_data <= storage[held_read_slot] ^ ((active_mode == 6) ? 128'd1 : 128'd0);
                    response_last <= (active_mode != 7);
                    response_valid <= 1'b1;
                end else begin
                    read_delay = read_delay - 1;
                end
            end
        end
    end

    // 逐拍检查初始化、运行和五类等待计数互斥，且终态不再计数。
    always @(negedge clk) begin
        if (!rstn) begin
            monitor_valid = 1'b0;
            previous_state = ST_WAIT;
            previous_cycles = 32'd0;
            previous_init_cycles = 32'd0;
            previous_wait_both = 32'd0;
            previous_wait_aw = 32'd0;
            previous_wait_w = 32'd0;
            previous_wait_ar = 32'd0;
            previous_wait_r = 32'd0;
        end else begin
            if (monitor_valid) begin
                run_delta = cycles - previous_cycles;
                init_delta = init_cycles - previous_init_cycles;
                both_delta = wait_both - previous_wait_both;
                aw_delta = wait_aw - previous_wait_aw;
                w_delta = wait_w - previous_wait_w;
                ar_delta = wait_ar - previous_wait_ar;
                r_delta = wait_r - previous_wait_r;
                if ((run_delta < 0) || (run_delta > 1) || (init_delta < 0) || (init_delta > 1)) begin
                    $fatal(1, "Run/init counter step invalid");
                end
                if ((both_delta < 0) || (both_delta > 1) || (aw_delta < 0) || (aw_delta > 1) ||
                    (w_delta < 0) || (w_delta > 1) || (ar_delta < 0) || (ar_delta > 1) ||
                    (r_delta < 0) || (r_delta > 1) ||
                    ((both_delta + aw_delta + w_delta + ar_delta + r_delta) > 1)) begin
                    $fatal(1, "Wait counters are not mutually exclusive");
                end
                if (previous_state == ST_WAIT) begin
                    if ((init_delta != 1) || (run_delta != 0)) $fatal(1, "WAIT accounting mismatch");
                end else if ((previous_state == ST_PASS) || (previous_state == ST_FAIL)) begin
                    if ((init_delta != 0) || (run_delta != 0) ||
                        ((both_delta + aw_delta + w_delta + ar_delta + r_delta) != 0)) begin
                        $fatal(1, "Terminal counters changed");
                    end
                end else if ((init_delta != 0) || (run_delta != 1)) begin
                    $fatal(1, "Run accounting mismatch state=%0d", previous_state);
                end
                if ((both_delta || aw_delta || w_delta) && (previous_state != ST_WRITE)) begin
                    $fatal(1, "Write wait counter changed outside WRITE");
                end
                if (ar_delta && (previous_state != ST_READ_ADDR)) begin
                    $fatal(1, "AR wait counter changed outside READ_ADDR");
                end
                if (r_delta && (previous_state != ST_READ_DATA)) begin
                    $fatal(1, "R wait counter changed outside READ_DATA");
                end
            end
            monitor_valid = 1'b1;
            previous_state = state_value;
            previous_cycles = cycles;
            previous_init_cycles = init_cycles;
            previous_wait_both = wait_both;
            previous_wait_aw = wait_aw;
            previous_wait_w = wait_w;
            previous_wait_ar = wait_ar;
            previous_wait_r = wait_r;
        end
    end

    always @(negedge rstn) begin
        #0.1;
        if (awvalid || wvalid || arvalid || rready) begin
            $fatal(1, "Reset did not cancel all DUT requests");
        end
    end

    initial begin
        ignored = $value$plusargs("CASE=%d", test_case);
        active_mode = test_case;
        for (loop_index = 0; loop_index < 194; loop_index = loop_index + 1) begin
            slot_seen[loop_index] = 1'b0;
            slot_address[loop_index] = 25'd0;
        end
        vector_file = $fopen("board_vectors.txt", "r");
        if (vector_file == 0) $fatal(1, "Cannot open board_vectors.txt");
        load_index = 0;
        write_index = 0;
        read_index = 0;
        while (load_index < 1056) begin
            scan_result = $fscanf(vector_file, "%h %h %h %h %h %h\n",
                                  scan_write, scan_address, scan_mask, scan_data,
                                  scan_expected, scan_slot);
            if (scan_result != 6) $fatal(1, "Malformed board vector index=%0d", load_index);
            if ((scan_address < 26'h3400000) || (scan_address > 26'h3fffff0) ||
                (scan_address[3:0] != 4'd0) || (scan_slot >= 194)) begin
                $fatal(1, "Illegal independent vector index=%0d", load_index);
            end
            command_write[load_index] = scan_write;
            command_byte_address[load_index] = scan_address;
            command_native_address[load_index] = scan_address[25:1];
            command_mask[load_index] = scan_mask;
            command_data[load_index] = scan_data;
            command_expected[load_index] = scan_expected;
            command_slot[load_index] = scan_slot;
            if (slot_seen[scan_slot] && (slot_address[scan_slot] != scan_address[25:1])) begin
                $fatal(1, "Sparse slot aliases two addresses slot=%0d", scan_slot);
            end
            slot_seen[scan_slot] = 1'b1;
            slot_address[scan_slot] = scan_address[25:1];
            if (scan_write) begin
                if (write_index >= 528) $fatal(1, "Too many write vectors");
                write_order[write_index] = load_index;
                write_index = write_index + 1;
            end else begin
                if (read_index >= 528) $fatal(1, "Too many read vectors");
                read_order[read_index] = load_index;
                read_index = read_index + 1;
            end
            load_index = load_index + 1;
        end
        $fclose(vector_file);
        if ((write_index != 528) || (read_index != 528)) begin
            $fatal(1, "Independent vector counts differ writes=%0d reads=%0d", write_index, read_index);
        end

        #1;
        case (test_case)
            18: dut.reg_commands[0][181] = ~dut.reg_commands[0][181];
            19: dut.reg_commands[0][170] = ~dut.reg_commands[0][170];
            20: dut.reg_commands[0][168:144] = 25'h19ffff8;
            21: dut.reg_commands[1000][181] = ~dut.reg_commands[1000][181];
            default: begin
                // 正常用例不读取DUT命令存储作为期望。
            end
        endcase

        repeat (4) @(negedge clk);
        rstn = 1'b1;
        if (test_case == 15) begin
            wait (pending_aw && !pending_w);
            @(negedge clk); rstn = 1'b0;
            repeat (3) @(negedge clk);
            active_mode = 0; rstn = 1'b1;
        end
        if (test_case == 16) begin
            wait (pending_w && !pending_aw);
            @(negedge clk); rstn = 1'b0;
            repeat (3) @(negedge clk);
            active_mode = 0; rstn = 1'b1;
        end
        if (test_case == 17) begin
            wait (pending_read);
            @(negedge clk); rstn = 1'b0;
            repeat (3) @(negedge clk);
            active_mode = 0; rstn = 1'b1;
        end
        if (test_case == 23) begin
            wait ((writes == 10'd528) && (reads == 10'd527));
            @(negedge clk);
            dut.cnt_writes = 10'd527;
        end

        case (test_case)
            6: expected_error = 5;
            7: expected_error = 6;
            8: expected_error = 1;
            9, 10: expected_error = 2;
            11: expected_error = 3;
            12: expected_error = 4;
            13, 22: expected_error = 7;
            14: expected_error = 8;
            18, 19, 20, 21: expected_error = 9;
            23: expected_error = 10;
            default: expected_error = 0;
        endcase
        if (test_case == 22) begin
            wait (status == 2'd1);
            wait (status == 2'd2);
        end else begin
            wait (status != 2'd0);
        end
        #1;

        if (expected_error == 0) begin
            if ((status !== 2'd1) || (error_kind !== 4'd0) ||
                (writes !== 10'd528) || (reads !== 10'd528) ||
                (aw_count != 528) || (w_count != 528) ||
                (ar_count != 528) || (r_count != 528)) begin
                $fatal(1, "Successful run lost or duplicated traffic");
            end
        end else if ((status !== 2'd2) || (error_kind !== expected_error)) begin
            $fatal(1, "Wrong failure case=%0d got=%0d expected=%0d", test_case, error_kind, expected_error);
        end

        if (((test_case == 1) && (wait_w == 0)) ||
            ((test_case == 2) && (wait_aw == 0))) begin
            $fatal(1, "Split AW/W case did not exercise its wait category");
        end
        if ((test_case == 4) && ((wait_both < 1024) || (wait_ar < 1024) || (wait_r < 1024))) begin
            $fatal(1, "Long-stall counters did not cover 1024 cycles");
        end
        if ((test_case == 6) && ((address !== command_native_address[194]) ||
            (expected_data !== command_expected[194]) ||
            (actual_data !== (command_expected[194] ^ 128'd1)))) begin
            $fatal(1, "Mismatch first-error evidence differs");
        end
        if ((test_case == 7) && ((address !== command_native_address[194]) ||
            (expected_data !== command_expected[194]) ||
            (actual_data !== command_expected[194]))) begin
            $fatal(1, "RLAST first-error evidence differs");
        end
        if ((test_case >= 18) && (test_case <= 20) &&
            ((aw_count != 0) || (w_count != 0) || (ar_count != 0) || (r_count != 0))) begin
            $fatal(1, "Early ROM corruption escaped before traffic");
        end
        if ((test_case == 21) && ((aw_count != 500) || (w_count != 500) ||
            (ar_count != 500) || (r_count != 500))) begin
            $fatal(1, "Late ROM corruption stopped at wrong command boundary");
        end
        if ((test_case == 23) && ((aw_count != 528) || (w_count != 528) ||
            (ar_count != 528) || (r_count != 528) ||
            (writes !== 10'd527) || (reads !== 10'd528))) begin
            $fatal(1, "Final-count negative did not preserve endpoint traffic");
        end

        terminal_address = address;
        terminal_expected = expected_data;
        terminal_actual = actual_data;
        terminal_error = error_kind;
        terminal_writes = writes;
        terminal_reads = reads;
        terminal_cycles = cycles;
        terminal_init_cycles = init_cycles;
        terminal_wait_both = wait_both;
        terminal_wait_aw = wait_aw;
        terminal_wait_w = wait_w;
        terminal_wait_ar = wait_ar;
        terminal_wait_r = wait_r;
        repeat (5) @(negedge clk);
        if ((address !== terminal_address) || (expected_data !== terminal_expected) ||
            (actual_data !== terminal_actual) || (error_kind !== terminal_error) ||
            (writes !== terminal_writes) || (reads !== terminal_reads) ||
            (cycles !== terminal_cycles) || (init_cycles !== terminal_init_cycles) ||
            (wait_both !== terminal_wait_both) || (wait_aw !== terminal_wait_aw) ||
            (wait_w !== terminal_wait_w) || (wait_ar !== terminal_wait_ar) ||
            (wait_r !== terminal_wait_r)) begin
            $fatal(1, "Terminal evidence or counters changed");
        end
        if (awvalid || wvalid || arvalid || rready) begin
            $fatal(1, "Terminal state issued traffic");
        end
        $display("DDR_EXTENDED_PASS case=%0d cycles=%0d writes=%0d reads=%0d error=%0d", test_case, cycles, writes, reads, error_kind);
        $finish;
    end

    initial begin
        #1000000;
        $fatal(1, "Testbench timeout case=%0d", test_case);
    end
endmodule
