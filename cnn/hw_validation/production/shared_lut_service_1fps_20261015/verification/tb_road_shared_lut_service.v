`timescale 1ns / 1ps
// Controlled-ROM verification for the one-outstanding shared LUT service.
module tb_road_shared_lut_service;
    localparam [31:0] MODEL_ID = 32'hB35D4A66;
    localparam [31:0] WRONG_MODEL = 32'hA55A1234;

    reg i_clk = 1'b0; // 100 MHz verification clock.
    reg i_rstn = 1'b0; // Common service and controlled-reader reset.
    always #5 i_clk = ~i_clk;

    reg i_cancel;
    reg i_lut_req_valid;
    reg i_lut_req_kind;
    reg [9:0] i_lut_req_address;
    reg [15:0] i_lut_req_tag;
    reg [31:0] i_lut_req_frame_token;
    reg [31:0] i_lut_req_model_id;
    reg i_lut_rsp_ready;
    wire o_lut_req_ready;
    wire o_lut_rsp_valid;
    wire o_lut_rsp_kind;
    wire [9:0] o_lut_rsp_address;
    wire [15:0] o_lut_rsp_tag;
    wire [31:0] o_lut_rsp_frame_token;
    wire [31:0] o_lut_rsp_model_id;
    wire [15:0] o_lut_rsp_data;
    wire o_lut_rsp_error;
    wire o_rom_request_valid;
    wire [12:0] o_rom_request_addr;
    wire o_rom_response_ready;
    wire o_fault;
    wire i_rom_request_ready;
    reg i_rom_response_valid;
    reg [159:0] i_rom_response_data;
    reg i_rom_fault;

    reg odd_cancel;
    reg odd_lut_req_valid;
    reg odd_lut_req_kind;
    reg [9:0] odd_lut_req_address;
    reg [15:0] odd_lut_req_tag;
    reg [31:0] odd_lut_req_frame_token;
    reg [31:0] odd_lut_req_model_id;
    reg odd_lut_rsp_ready;
    wire odd_lut_req_ready;
    wire odd_lut_rsp_valid;
    wire odd_lut_rsp_kind;
    wire [9:0] odd_lut_rsp_address;
    wire [15:0] odd_lut_rsp_tag;
    wire [31:0] odd_lut_rsp_frame_token;
    wire [31:0] odd_lut_rsp_model_id;
    wire [15:0] odd_lut_rsp_data;
    wire odd_lut_rsp_error;
    wire odd_rom_request_valid;
    wire [12:0] odd_rom_request_addr;
    wire odd_rom_response_ready;
    wire odd_fault;
    wire odd_rom_request_ready;
    reg odd_rom_response_valid;
    reg [159:0] odd_rom_response_data;
    reg odd_rom_fault;

    reg [159:0] rom_words [0:7167]; // Test-only physical G10 payload words.
    reg [15:0] sigmoid_expected [0:1023]; // Frozen default sigmoid entries.
    reg [15:0] exp_expected [0:255]; // Frozen default exponential entries.
    reg [15:0] odd_sigmoid_expected [0:1023]; // Odd-base relocation expectation.
    reg [15:0] odd_exp_expected [0:255]; // Odd-base relocation expectation.
    reg [4095:0] rom_path;

    reg endpoint_enable;
    reg endpoint_pending;
    reg [12:0] endpoint_address;
    integer endpoint_delay;
    integer endpoint_delay_config;
    integer rom_read_count;
    reg odd_endpoint_enable;
    reg odd_endpoint_pending;
    reg [12:0] odd_endpoint_address;
    integer odd_endpoint_delay;
    integer odd_endpoint_delay_config;
    integer odd_rom_read_count;
    integer total_rom_read_count;
    integer total_odd_rom_read_count;
    integer cycle_count;
    integer default_latency_min;
    integer default_latency_max;
    integer default_latency_sum;
    integer default_queries;
    integer odd_latency_min;
    integer odd_latency_max;
    integer odd_latency_sum;
    integer odd_queries;
    integer index;
    integer reads_before;
    reg [106:0] held_response;

    assign i_rom_request_ready = endpoint_enable && !endpoint_pending && !i_rom_response_valid;
    assign odd_rom_request_ready = odd_endpoint_enable && !odd_endpoint_pending && !odd_rom_response_valid;

    road_shared_lut_service dut (
        .i_clk(i_clk), .i_rstn(i_rstn), .i_cancel(i_cancel),
        .i_lut_req_valid(i_lut_req_valid), .i_lut_req_kind(i_lut_req_kind),
        .i_lut_req_address(i_lut_req_address), .i_lut_req_tag(i_lut_req_tag),
        .i_lut_req_frame_token(i_lut_req_frame_token), .i_lut_req_model_id(i_lut_req_model_id),
        .o_lut_req_ready(o_lut_req_ready), .o_lut_rsp_valid(o_lut_rsp_valid),
        .o_lut_rsp_kind(o_lut_rsp_kind), .o_lut_rsp_address(o_lut_rsp_address),
        .o_lut_rsp_tag(o_lut_rsp_tag), .o_lut_rsp_frame_token(o_lut_rsp_frame_token),
        .o_lut_rsp_model_id(o_lut_rsp_model_id), .o_lut_rsp_data(o_lut_rsp_data),
        .o_lut_rsp_error(o_lut_rsp_error), .i_lut_rsp_ready(i_lut_rsp_ready),
        .o_rom_request_valid(o_rom_request_valid), .o_rom_request_addr(o_rom_request_addr),
        .i_rom_request_ready(i_rom_request_ready), .i_rom_response_valid(i_rom_response_valid),
        .i_rom_response_data(i_rom_response_data), .o_rom_response_ready(o_rom_response_ready),
        .i_rom_fault(i_rom_fault), .o_fault(o_fault)
    );

    road_shared_lut_service #(
        .C_SIGMOID_BYTE_OFFSET(19), .C_EXP_BYTE_OFFSET(39)
    ) dut_odd (
        .i_clk(i_clk), .i_rstn(i_rstn), .i_cancel(odd_cancel),
        .i_lut_req_valid(odd_lut_req_valid), .i_lut_req_kind(odd_lut_req_kind),
        .i_lut_req_address(odd_lut_req_address), .i_lut_req_tag(odd_lut_req_tag),
        .i_lut_req_frame_token(odd_lut_req_frame_token), .i_lut_req_model_id(odd_lut_req_model_id),
        .o_lut_req_ready(odd_lut_req_ready), .o_lut_rsp_valid(odd_lut_rsp_valid),
        .o_lut_rsp_kind(odd_lut_rsp_kind), .o_lut_rsp_address(odd_lut_rsp_address),
        .o_lut_rsp_tag(odd_lut_rsp_tag), .o_lut_rsp_frame_token(odd_lut_rsp_frame_token),
        .o_lut_rsp_model_id(odd_lut_rsp_model_id), .o_lut_rsp_data(odd_lut_rsp_data),
        .o_lut_rsp_error(odd_lut_rsp_error), .i_lut_rsp_ready(odd_lut_rsp_ready),
        .o_rom_request_valid(odd_rom_request_valid), .o_rom_request_addr(odd_rom_request_addr),
        .i_rom_request_ready(odd_rom_request_ready), .i_rom_response_valid(odd_rom_response_valid),
        .i_rom_response_data(odd_rom_response_data), .o_rom_response_ready(odd_rom_response_ready),
        .i_rom_fault(odd_rom_fault), .o_fault(odd_fault)
    );

    // The endpoint models one untagged ROM-reader transaction and a held response.
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) begin
            endpoint_pending <= 1'b0;
            endpoint_address <= 13'd0;
            endpoint_delay <= 0;
            i_rom_response_valid <= 1'b0;
            i_rom_response_data <= 160'd0;
            rom_read_count <= 0;
        end else begin
            if (o_rom_request_valid && i_rom_request_ready) begin
                endpoint_pending <= 1'b1;
                endpoint_address <= o_rom_request_addr;
                endpoint_delay <= endpoint_delay_config;
                rom_read_count <= rom_read_count + 1;
                total_rom_read_count <= total_rom_read_count + 1;
            end else if (endpoint_pending && endpoint_delay != 0) begin
                endpoint_delay <= endpoint_delay - 1;
            end else if (endpoint_pending) begin
                endpoint_pending <= 1'b0;
                i_rom_response_valid <= 1'b1;
                i_rom_response_data <= rom_words[endpoint_address];
            end
            if (i_rom_response_valid && o_rom_response_ready)
                i_rom_response_valid <= 1'b0;
        end
    end

    // A second independent endpoint exposes the odd-base crossword branch.
    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn) begin
            odd_endpoint_pending <= 1'b0;
            odd_endpoint_address <= 13'd0;
            odd_endpoint_delay <= 0;
            odd_rom_response_valid <= 1'b0;
            odd_rom_response_data <= 160'd0;
            odd_rom_read_count <= 0;
        end else begin
            if (odd_rom_request_valid && odd_rom_request_ready) begin
                odd_endpoint_pending <= 1'b1;
                odd_endpoint_address <= odd_rom_request_addr;
                odd_endpoint_delay <= odd_endpoint_delay_config;
                odd_rom_read_count <= odd_rom_read_count + 1;
                total_odd_rom_read_count <= total_odd_rom_read_count + 1;
            end else if (odd_endpoint_pending && odd_endpoint_delay != 0) begin
                odd_endpoint_delay <= odd_endpoint_delay - 1;
            end else if (odd_endpoint_pending) begin
                odd_endpoint_pending <= 1'b0;
                odd_rom_response_valid <= 1'b1;
                odd_rom_response_data <= rom_words[odd_endpoint_address];
            end
            if (odd_rom_response_valid && odd_rom_response_ready)
                odd_rom_response_valid <= 1'b0;
        end
    end

    always @(posedge i_clk or negedge i_rstn) begin
        if (!i_rstn)
            cycle_count <= 0;
        else
            cycle_count <= cycle_count + 1;
    end

    // Wait for a ready service slot with a bounded watchdog.
    task wait_default_ready; // Explain default-slot synchronization.
        integer guard;
        begin
            guard = 0;
            while (!o_lut_req_ready && guard < 1000) begin
                @(negedge i_clk);
                guard = guard + 1;
            end
            if (!o_lut_req_ready) $fatal(1, "TB_FAIL default request slot timeout");
        end
    endtask // End default-slot synchronization.

    // Drive one default request and verify its complete response identity.
    task query_default; // Explain default lookup transaction.
        input request_kind;
        input [9:0] request_address;
        input [15:0] request_tag;
        input [31:0] request_frame;
        input [31:0] request_model;
        input [15:0] expected_data;
        input expected_error;
        input integer hold_cycles;
        integer accepted_cycle;
        integer response_cycle;
        integer guard;
        begin
            wait_default_ready;
            @(negedge i_clk);
            i_lut_req_valid = 1'b1;
            i_lut_req_kind = request_kind;
            i_lut_req_address = request_address;
            i_lut_req_tag = request_tag;
            i_lut_req_frame_token = request_frame;
            i_lut_req_model_id = request_model;
            while (!o_lut_req_ready) @(negedge i_clk);
            accepted_cycle = cycle_count;
            @(negedge i_clk);
            i_lut_req_valid = 1'b0;
            i_lut_rsp_ready = (hold_cycles == 0);
            guard = 0;
            while (!o_lut_rsp_valid && guard < 1000) begin
                @(negedge i_clk);
                guard = guard + 1;
            end
            if (!o_lut_rsp_valid) $fatal(1, "TB_FAIL default response timeout kind=%0d addr=%0d", request_kind, request_address);
            response_cycle = cycle_count;
            if ({o_lut_rsp_kind, o_lut_rsp_address, o_lut_rsp_tag, o_lut_rsp_frame_token,
                 o_lut_rsp_model_id, o_lut_rsp_data, o_lut_rsp_error} !==
                {request_kind, request_address, request_tag, request_frame,
                 request_model, expected_data, expected_error})
                $fatal(1, "TB_FAIL default response mismatch kind=%0d addr=%0d", request_kind, request_address);
            held_response = {o_lut_rsp_kind, o_lut_rsp_address, o_lut_rsp_tag,
                             o_lut_rsp_frame_token, o_lut_rsp_model_id, o_lut_rsp_data};
            repeat (hold_cycles) begin
                @(negedge i_clk);
                if (!o_lut_rsp_valid || held_response !== {o_lut_rsp_kind, o_lut_rsp_address,
                    o_lut_rsp_tag, o_lut_rsp_frame_token, o_lut_rsp_model_id, o_lut_rsp_data})
                    $fatal(1, "TB_FAIL default held response changed");
            end
            i_lut_rsp_ready = 1'b1;
            @(negedge i_clk);
            i_lut_rsp_ready = 1'b0;
            if (o_lut_rsp_valid) $fatal(1, "TB_FAIL default response duplicated");
            if (!expected_error) begin
                if (response_cycle - accepted_cycle < default_latency_min)
                    default_latency_min = response_cycle - accepted_cycle;
                if (response_cycle - accepted_cycle > default_latency_max)
                    default_latency_max = response_cycle - accepted_cycle;
                default_latency_sum = default_latency_sum + response_cycle - accepted_cycle;
                default_queries = default_queries + 1;
            end
        end
    endtask // End default lookup transaction.

    // Drive one odd-base request and verify crossword reconstruction.
    task query_odd; // Explain odd-base lookup transaction.
        input request_kind;
        input [9:0] request_address;
        input [15:0] expected_data;
        integer accepted_cycle;
        integer response_cycle;
        integer guard;
        begin
            guard = 0;
            while (!odd_lut_req_ready && guard < 1000) begin
                @(negedge i_clk);
                guard = guard + 1;
            end
            if (!odd_lut_req_ready) $fatal(1, "TB_FAIL odd request slot timeout");
            repeat (request_address[1:0]) @(negedge i_clk);
            odd_lut_req_valid = 1'b1;
            odd_lut_req_kind = request_kind;
            odd_lut_req_address = request_address;
            odd_lut_req_tag = 16'h8000 ^ request_address;
            odd_lut_req_frame_token = 32'h30000000 + request_address + {31'd0, request_kind};
            odd_lut_req_model_id = MODEL_ID;
            while (!odd_lut_req_ready) @(negedge i_clk);
            accepted_cycle = cycle_count;
            @(negedge i_clk);
            odd_lut_req_valid = 1'b0;
            odd_lut_rsp_ready = 1'b1;
            guard = 0;
            while (!odd_lut_rsp_valid && guard < 1000) begin
                @(negedge i_clk);
                guard = guard + 1;
            end
            if (!odd_lut_rsp_valid) $fatal(1, "TB_FAIL odd response timeout kind=%0d addr=%0d", request_kind, request_address);
            response_cycle = cycle_count;
            if (odd_lut_rsp_error || odd_lut_rsp_kind !== request_kind ||
                odd_lut_rsp_address !== request_address || odd_lut_rsp_data !== expected_data ||
                odd_lut_rsp_tag !== (16'h8000 ^ request_address) ||
                odd_lut_rsp_frame_token !== (32'h30000000 + request_address + {31'd0, request_kind}) ||
                odd_lut_rsp_model_id !== MODEL_ID)
                $fatal(1, "TB_FAIL odd response mismatch kind=%0d addr=%0d", request_kind, request_address);
            @(negedge i_clk);
            odd_lut_rsp_ready = 1'b0;
            if (response_cycle - accepted_cycle < odd_latency_min)
                odd_latency_min = response_cycle - accepted_cycle;
            if (response_cycle - accepted_cycle > odd_latency_max)
                odd_latency_max = response_cycle - accepted_cycle;
            odd_latency_sum = odd_latency_sum + response_cycle - accepted_cycle;
            odd_queries = odd_queries + 1;
        end
    endtask // End odd-base lookup transaction.

    // Assert a common reset and clear the controlled reader's sticky fault inputs.
    task common_reset; // Explain common reset sequencing.
        begin
            @(negedge i_clk);
            i_rstn = 1'b0;
            i_rom_fault = 1'b0;
            odd_rom_fault = 1'b0;
            repeat (4) @(negedge i_clk);
            i_rstn = 1'b1;
            repeat (4) @(negedge i_clk);
        end
    endtask // End common reset sequencing.

    initial begin
        if (!$value$plusargs("ROM=%s", rom_path)) $fatal(1, "TB_FAIL missing +ROM path");
        $readmemh(rom_path, rom_words);
        $readmemh("assets/sigmoid_expected_16.hex", sigmoid_expected);
        $readmemh("assets/exp_expected_16.hex", exp_expected);
        $readmemh("assets/odd19_sigmoid_expected_16.hex", odd_sigmoid_expected);
        $readmemh("assets/odd39_exp_expected_16.hex", odd_exp_expected);
        i_cancel = 1'b0;
        i_lut_req_valid = 1'b0;
        i_lut_req_kind = 1'b0;
        i_lut_req_address = 10'd0;
        i_lut_req_tag = 16'd0;
        i_lut_req_frame_token = 32'd0;
        i_lut_req_model_id = MODEL_ID;
        i_lut_rsp_ready = 1'b0;
        i_rom_fault = 1'b0;
        endpoint_enable = 1'b1;
        endpoint_delay_config = 0;
        odd_cancel = 1'b0;
        odd_lut_req_valid = 1'b0;
        odd_lut_req_kind = 1'b0;
        odd_lut_req_address = 10'd0;
        odd_lut_req_tag = 16'd0;
        odd_lut_req_frame_token = 32'd0;
        odd_lut_req_model_id = MODEL_ID;
        odd_lut_rsp_ready = 1'b0;
        odd_rom_fault = 1'b0;
        odd_endpoint_enable = 1'b1;
        odd_endpoint_delay_config = 0;
        default_latency_min = 32'h7fffffff;
        default_latency_max = 0;
        default_latency_sum = 0;
        default_queries = 0;
        odd_latency_min = 32'h7fffffff;
        odd_latency_max = 0;
        odd_latency_sum = 0;
        odd_queries = 0;
        total_rom_read_count = 0;
        total_odd_rom_read_count = 0;

        common_reset;

        // Exhaust every production table entry with changing tag/frame identity.
        reads_before = rom_read_count;
        for (index = 0; index < 1024; index = index + 1) begin
            repeat (index[1:0]) @(negedge i_clk);
            query_default(1'b0, index[9:0], 16'h1000 ^ index[15:0],
                32'h20000000 + index, MODEL_ID, sigmoid_expected[index], 1'b0, 0);
        end
        for (index = 0; index < 256; index = index + 1) begin
            repeat (index[1:0]) @(negedge i_clk);
            query_default(1'b1, index[9:0], 16'h4000 ^ index[15:0],
                32'h21000000 + index, MODEL_ID, exp_expected[index], 1'b0, 0);
        end
        if (rom_read_count - reads_before != 1280)
            $fatal(1, "TB_FAIL default exhaustive ROM reads=%0d", rom_read_count - reads_before);
        $display("METRIC default_entries=1280 default_rom_reads=%0d latency_min=%0d latency_max=%0d latency_avg_x100=%0d",
            rom_read_count - reads_before, default_latency_min, default_latency_max,
            (default_latency_sum * 100) / default_queries);

        // Hold the LUT response and separately stall the outgoing ROM request.
        endpoint_delay_config = 17;
        query_default(1'b0, 10'd17, 16'h55AA, 32'h12345678, MODEL_ID,
            sigmoid_expected[17], 1'b0, 37);
        endpoint_delay_config = 0;
        endpoint_enable = 1'b0;
        fork
            begin
                repeat (23) @(negedge i_clk);
                endpoint_enable = 1'b1;
            end
            begin
                query_default(1'b1, 10'd73, 16'h0F0F, 32'h89ABCDEF, MODEL_ID,
                    exp_expected[73], 1'b0, 0);
            end
        join

        // Invalid requests must echo identity and must never touch the ROM endpoint.
        reads_before = rom_read_count;
        query_default(1'b0, 10'd9, 16'hDEAD, 32'hCAFEBABE, WRONG_MODEL, 16'd0, 1'b1, 9);
        query_default(1'b1, 10'd256, 16'h0100, 32'h00000100, MODEL_ID, 16'd0, 1'b1, 0);
        query_default(1'b1, 10'd1023, 16'h03FF, 32'h000003FF, MODEL_ID, 16'd0, 1'b1, 0);
        if (rom_read_count != reads_before) $fatal(1, "TB_FAIL invalid request read ROM");

        // Cancel a request before the untagged ROM reader accepts it.
        endpoint_enable = 1'b0;
        wait_default_ready;
        @(negedge i_clk);
        i_lut_req_valid = 1'b1;
        i_lut_req_kind = 1'b0;
        i_lut_req_address = 10'd31;
        i_lut_req_tag = 16'hCA01;
        i_lut_req_frame_token = 32'hCA000001;
        i_lut_req_model_id = MODEL_ID;
        while (!o_lut_req_ready) @(negedge i_clk);
        @(negedge i_clk);
        i_lut_req_valid = 1'b0;
        while (!o_rom_request_valid) @(negedge i_clk);
        reads_before = rom_read_count;
        i_cancel = 1'b1;
        @(negedge i_clk);
        if (o_lut_req_ready || o_lut_rsp_valid || o_rom_request_valid)
            $fatal(1, "TB_FAIL cancel-before-accept outputs not blocked");
        i_cancel = 1'b0;
        endpoint_enable = 1'b1;
        wait_default_ready;
        if (rom_read_count != reads_before) $fatal(1, "TB_FAIL cancel-before-accept reached ROM");

        // Cancel after acceptance; readiness must wait for the late response to drain.
        endpoint_delay_config = 31;
        wait_default_ready;
        @(negedge i_clk);
        i_lut_req_valid = 1'b1;
        i_lut_req_kind = 1'b0;
        i_lut_req_address = 10'd32;
        i_lut_req_tag = 16'hCA02;
        i_lut_req_frame_token = 32'hCA000002;
        i_lut_req_model_id = MODEL_ID;
        while (!o_lut_req_ready) @(negedge i_clk);
        @(negedge i_clk);
        i_lut_req_valid = 1'b0;
        while (!endpoint_pending) @(negedge i_clk);
        i_cancel = 1'b1;
        repeat (3) @(negedge i_clk);
        i_cancel = 1'b0;
        while (endpoint_pending || i_rom_response_valid) begin
            if (o_lut_req_ready || o_lut_rsp_valid) $fatal(1, "TB_FAIL drain exposed a reusable slot");
            @(negedge i_clk);
        end
        wait_default_ready;
        if (o_lut_rsp_valid) $fatal(1, "TB_FAIL canceled response leaked");
        endpoint_delay_config = 0;
        query_default(1'b0, 10'd33, 16'hCA03, 32'hCA000003, MODEL_ID,
            sigmoid_expected[33], 1'b0, 0);

        // Common reset during a pending read must remove all prior ownership.
        endpoint_delay_config = 50;
        wait_default_ready;
        @(negedge i_clk);
        i_lut_req_valid = 1'b1;
        i_lut_req_kind = 1'b0;
        i_lut_req_address = 10'd41;
        while (!o_lut_req_ready) @(negedge i_clk);
        @(negedge i_clk);
        i_lut_req_valid = 1'b0;
        while (!endpoint_pending) @(negedge i_clk);
        common_reset;
        endpoint_delay_config = 0;
        if (o_lut_rsp_valid || o_fault) $fatal(1, "TB_FAIL reset-during-wait leaked state");
        query_default(1'b0, 10'd42, 16'h5201, 32'h52000001, MODEL_ID,
            sigmoid_expected[42], 1'b0, 0);

        // Common reset must also clear a held service response.
        wait_default_ready;
        @(negedge i_clk);
        i_lut_req_valid = 1'b1;
        i_lut_req_kind = 1'b0;
        i_lut_req_address = 10'd43;
        i_lut_req_tag = 16'h5202;
        i_lut_req_frame_token = 32'h52000002;
        i_lut_req_model_id = MODEL_ID;
        i_lut_rsp_ready = 1'b0;
        while (!o_lut_req_ready) @(negedge i_clk);
        @(negedge i_clk);
        i_lut_req_valid = 1'b0;
        while (!o_lut_rsp_valid) @(negedge i_clk);
        repeat (11) @(negedge i_clk);
        common_reset;
        if (o_lut_rsp_valid) $fatal(1, "TB_FAIL reset-held-response remained valid");

        // Reader fault is sticky across cancel and only the common reset clears it.
        endpoint_delay_config = 20;
        wait_default_ready;
        @(negedge i_clk);
        i_lut_req_valid = 1'b1;
        i_lut_req_kind = 1'b0;
        i_lut_req_address = 10'd44;
        i_lut_req_tag = 16'hFA17;
        i_lut_req_frame_token = 32'hFA170001;
        i_lut_req_model_id = MODEL_ID;
        while (!o_lut_req_ready) @(negedge i_clk);
        @(negedge i_clk);
        i_lut_req_valid = 1'b0;
        while (!endpoint_pending) @(negedge i_clk);
        i_rom_fault = 1'b1;
        while (!o_lut_rsp_valid) @(negedge i_clk);
        if (!o_lut_rsp_error || o_lut_rsp_data != 16'd0 || !o_fault ||
            o_lut_rsp_tag != 16'hFA17 || o_lut_rsp_frame_token != 32'hFA170001)
            $fatal(1, "TB_FAIL reader fault response");
        i_lut_rsp_ready = 1'b1;
        @(negedge i_clk);
        i_lut_rsp_ready = 1'b0;
        i_cancel = 1'b1;
        @(negedge i_clk);
        i_cancel = 1'b0;
        if (!o_fault) $fatal(1, "TB_FAIL cancel cleared reader fault");
        common_reset;
        endpoint_delay_config = 0;
        if (o_fault) $fatal(1, "TB_FAIL common reset did not clear fault");

        // Exhaust the odd relocation and prove every lane-19 entry uses two reads.
        reads_before = odd_rom_read_count;
        for (index = 0; index < 1024; index = index + 1)
            query_odd(1'b0, index[9:0], odd_sigmoid_expected[index]);
        for (index = 0; index < 256; index = index + 1)
            query_odd(1'b1, index[9:0], odd_exp_expected[index]);
        if (odd_rom_read_count - reads_before != 1409)
            $fatal(1, "TB_FAIL odd exhaustive ROM reads=%0d", odd_rom_read_count - reads_before);
        $display("METRIC odd_entries=1280 lane19_entries=129 odd_rom_reads=%0d latency_min=%0d latency_max=%0d latency_avg_x100=%0d",
            odd_rom_read_count - reads_before, odd_latency_min, odd_latency_max,
            (odd_latency_sum * 100) / odd_queries);

        // Cancel between the two reads of an odd-base lane-19 lookup.
        reads_before = odd_rom_read_count;
        odd_endpoint_delay_config = 3;
        while (!odd_lut_req_ready) @(negedge i_clk);
        odd_lut_req_valid = 1'b1;
        odd_lut_req_kind = 1'b0;
        odd_lut_req_address = 10'd0;
        odd_lut_req_tag = 16'h0DD0;
        odd_lut_req_frame_token = 32'h0DD00001;
        odd_lut_req_model_id = MODEL_ID;
        while (!odd_lut_req_ready) @(negedge i_clk);
        @(negedge i_clk);
        odd_lut_req_valid = 1'b0;
        while (odd_rom_read_count == reads_before) @(negedge i_clk);
        odd_endpoint_enable = 1'b0;
        while (!odd_rom_request_valid) @(negedge i_clk);
        if (odd_rom_read_count - reads_before != 1) $fatal(1, "TB_FAIL odd first-read count");
        odd_cancel = 1'b1;
        @(negedge i_clk);
        if (odd_rom_request_valid || odd_lut_rsp_valid) $fatal(1, "TB_FAIL odd cancel did not suppress second read");
        odd_cancel = 1'b0;
        odd_endpoint_enable = 1'b1;
        odd_endpoint_delay_config = 0;
        while (!odd_lut_req_ready) @(negedge i_clk);
        if (odd_rom_read_count - reads_before != 1 || odd_lut_rsp_valid)
            $fatal(1, "TB_FAIL odd canceled crossword leaked");

        $display("METRIC total_default_rom_reads=%0d total_odd_rom_reads=%0d", total_rom_read_count, total_odd_rom_read_count);
        $display("TB_PASS_SHARED_LUT default_entries=1280 odd_entries=1280 invalid=3 cancel=3 reset=2 reader_fault=1");
        $finish;
    end

    initial begin
        #10000000;
        $fatal(1, "TB_FAIL global timeout");
    end
endmodule
