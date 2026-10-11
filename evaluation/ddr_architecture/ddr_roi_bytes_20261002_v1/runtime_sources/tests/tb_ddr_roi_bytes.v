`timescale 1ns/1ps

module tb_ddr_roi_bytes;
    reg clk = 1'b0;
    reg rst_n = 1'b0;
    reg start_valid = 1'b0;
    wire start_ready;
    reg [15:0] start_task_id = 16'd0;
    reg [15:0] start_frame_id = 16'd0;
    reg [31:0] start_frame_base_byte = 32'd0;
    reg [10:0] start_x0 = 11'd0;
    reg [9:0] start_y0 = 10'd0;
    reg [10:0] start_x1 = 11'd0;
    reg [9:0] start_y1 = 10'd0;
    reg cancel = 1'b0;

    wire rd_req_valid;
    reg rd_req_ready = 1'b0;
    wire [31:0] rd_req_addr_byte;
    wire [15:0] rd_req_task_id;
    wire [15:0] rd_req_frame_id;
    reg rd_rsp_valid = 1'b0;
    reg [127:0] rd_rsp_data = 128'd0;

    wire roi_valid;
    wire [15:0] roi_task_id;
    wire [15:0] roi_frame_id;
    wire [4:0] roi_x;
    wire [4:0] roi_y;
    wire [7:0] roi_gray;
    wire done;
    wire cancel_done;
    wire busy;
    wire drained;
    wire [1:0] occupied_count;
    wire [1:0] reserved_count;
    wire protocol_error;

    reg [31:0] lfsr = 32'h1aceb00c;
    reg model_pending = 1'b0;
    reg [31:0] model_addr = 32'd0;
    integer model_delay = 0;
    reg hold_response = 1'b0;
    integer accepted_requests = 0;
    integer returned_beats = 0;
    integer roi_count = 0;
    integer total_roi_count = 0;
    integer start_request_count = 0;
    integer scenario_requests [0:3];
    integer cancel_outputs = 0;
    integer exp_x;
    integer exp_y;
    integer exp_r;
    integer exp_g;
    integer exp_b;
    integer exp_gray;
    integer wait_cycles;
    reg check_roi_active = 1'b0;
    reg [15:0] expected_task_id = 16'd0;
    reg [15:0] expected_frame_id = 16'd0;
    reg [31:0] expected_base = 32'd0;
    integer expected_x0 = 0;
    integer expected_y0 = 0;
    integer expected_x1 = 0;
    integer expected_y1 = 0;
    reg [2047:0] log_path;
    integer log_fd;

    always #5 clk = ~clk;

    ddr_roi_byte_reader dut (
        .clk(clk), .rst_n(rst_n),
        .start_valid(start_valid), .start_ready(start_ready),
        .start_task_id(start_task_id), .start_frame_id(start_frame_id),
        .start_frame_base_byte(start_frame_base_byte),
        .start_x0(start_x0), .start_y0(start_y0),
        .start_x1(start_x1), .start_y1(start_y1), .cancel(cancel),
        .rd_req_valid(rd_req_valid), .rd_req_ready(rd_req_ready),
        .rd_req_addr_byte(rd_req_addr_byte),
        .rd_req_task_id(rd_req_task_id), .rd_req_frame_id(rd_req_frame_id),
        .rd_rsp_valid(rd_rsp_valid), .rd_rsp_data(rd_rsp_data),
        .roi_valid(roi_valid), .roi_task_id(roi_task_id),
        .roi_frame_id(roi_frame_id), .roi_x(roi_x), .roi_y(roi_y),
        .roi_gray(roi_gray), .done(done), .cancel_done(cancel_done),
        .busy(busy), .drained(drained),
        .occupied_count(occupied_count), .reserved_count(reserved_count),
        .protocol_error(protocol_error)
    );

    function [7:0] model_byte;
        input [31:0] address;
        input [31:0] frame_base;
        integer offset;
        integer pixel;
        integer channel;
        integer x;
        integer y;
        begin
            offset = address - frame_base;
            pixel = offset / 3;
            channel = offset % 3;
            x = pixel % 1280;
            y = pixel / 1280;
            case (channel)
                0: model_byte = (3*x + 5*y + 17) & 255;
                1: model_byte = (7*x + 11*y + 29) & 255;
                default: model_byte = (13*x + 19*y + 43) & 255;
            endcase
        end
    endfunction

    function [127:0] model_beat;
        input [31:0] address;
        input [31:0] frame_base;
        integer lane;
        begin
            model_beat = 128'd0;
            for (lane = 0; lane < 16; lane = lane + 1)
                model_beat[127-lane*8 -: 8] = model_byte(address + lane, frame_base);
        end
    endfunction

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            lfsr <= 32'h1aceb00c;
            rd_req_ready <= 1'b0;
            rd_rsp_valid <= 1'b0;
            rd_rsp_data <= 128'd0;
            model_pending <= 1'b0;
            model_addr <= 32'd0;
            model_delay <= 0;
        end else begin
            lfsr <= {lfsr[30:0], lfsr[31] ^ lfsr[21] ^ lfsr[1] ^ lfsr[0]};
            rd_req_ready <= !model_pending && lfsr[0];
            rd_rsp_valid <= 1'b0;

            if (rd_req_valid && rd_req_ready) begin
                if (model_pending)
                    $fatal(1, "more than one request outstanding");
                if (rd_req_addr_byte[3:0] != 0)
                    $fatal(1, "unaligned byte address %h", rd_req_addr_byte);
                if ((rd_req_task_id != expected_task_id) ||
                    (rd_req_frame_id != expected_frame_id))
                    $fatal(1, "request tag mismatch");
                model_pending <= 1'b1;
                model_addr <= rd_req_addr_byte;
                model_delay <= 1 + (lfsr[4:2] % 5);
                accepted_requests <= accepted_requests + 1;
                $fwrite(log_fd, "ACCEPT,%0d,%0d,%0d\n",
                        rd_req_task_id, rd_req_frame_id, rd_req_addr_byte);
            end else if (model_pending && !hold_response) begin
                if (model_delay == 0) begin
                    rd_rsp_valid <= 1'b1;
                    rd_rsp_data <= model_beat(model_addr, expected_base);
                    model_pending <= 1'b0;
                    returned_beats <= returned_beats + 1;
                    $fwrite(log_fd, "RETURN,%0d\n", model_addr);
                end else begin
                    model_delay <= model_delay - 1;
                end
            end
        end
    end

    always @(negedge clk) begin
        if (rst_n && ((occupied_count + reserved_count) > 1))
            $fatal(1, "occupied+reserved exceeded receive depth");
        if (rst_n && roi_valid) begin
            if (!check_roi_active) begin
                cancel_outputs = cancel_outputs + 1;
            end else begin
                if ((roi_task_id != expected_task_id) ||
                    (roi_frame_id != expected_frame_id))
                    $fatal(1, "ROI tag mismatch");
                if ((roi_x != (roi_count % 32)) ||
                    (roi_y != (roi_count / 32)))
                    $fatal(1, "ROI coordinate order mismatch count=%0d", roi_count);
                exp_x = expected_x0 +
                        ((expected_x1-expected_x0) * (2*(roi_count % 32)+1) >> 6);
                exp_y = expected_y0 +
                        ((expected_y1-expected_y0) * (2*(roi_count / 32)+1) >> 6);
                exp_r = (3*exp_x + 5*exp_y + 17) & 255;
                exp_g = (7*exp_x + 11*exp_y + 29) & 255;
                exp_b = (13*exp_x + 19*exp_y + 43) & 255;
                exp_gray = (exp_r >> 2) + (exp_g >> 1) + (exp_b >> 2);
                if (roi_gray != exp_gray)
                    $fatal(1, "gray mismatch u=%0d v=%0d got=%0d expected=%0d",
                           roi_x, roi_y, roi_gray, exp_gray);
                $fwrite(log_fd, "ROI,%0d,%0d,%0d,%0d,%0d\n",
                        roi_task_id, roi_frame_id, roi_x, roi_y, roi_gray);
                roi_count = roi_count + 1;
                total_roi_count = total_roi_count + 1;
            end
        end
    end

    task start_job;
        input [15:0] task_id;
        input [15:0] frame_id;
        input [31:0] frame_base;
        input integer x0;
        input integer y0;
        input integer x1;
        input integer y1;
        begin
            expected_task_id = task_id;
            expected_frame_id = frame_id;
            expected_base = frame_base;
            expected_x0 = x0;
            expected_y0 = y0;
            expected_x1 = x1;
            expected_y1 = y1;
            roi_count = 0;
            start_request_count = accepted_requests;
            @(negedge clk);
            start_task_id = task_id;
            start_frame_id = frame_id;
            start_frame_base_byte = frame_base;
            start_x0 = x0;
            start_y0 = y0;
            start_x1 = x1;
            start_y1 = y1;
            start_valid = 1'b1;
            while (!start_ready)
                @(negedge clk);
            @(negedge clk);
            start_valid = 1'b0;
        end
    endtask

    task run_success;
        input integer scenario;
        input [15:0] task_id;
        input [15:0] frame_id;
        input [31:0] frame_base;
        input integer x0;
        input integer y0;
        input integer x1;
        input integer y1;
        begin
            check_roi_active = 1'b1;
            start_job(task_id, frame_id, frame_base, x0, y0, x1, y1);
            wait_cycles = 0;
            while (!done && (wait_cycles < 2000000)) begin
                @(negedge clk);
                wait_cycles = wait_cycles + 1;
            end
            #1;
            if (!done || (roi_count != 1024))
                $fatal(1, "successful job incomplete scenario=%0d pixels=%0d", scenario, roi_count);
            scenario_requests[scenario] = accepted_requests - start_request_count;
            $fwrite(log_fd, "JOB_DONE,%0d,%0d,%0d\n",
                    scenario, roi_count, scenario_requests[scenario]);
            check_roi_active = 1'b0;
            @(negedge clk);
        end
    endtask

    initial begin
        if (!$value$plusargs("LOG=%s", log_path))
            $fatal(1, "missing +LOG=<event log>");
        log_fd = $fopen(log_path, "w");
        if (!log_fd)
            $fatal(1, "cannot open log");
        repeat (5) @(posedge clk);
        @(negedge clk);
        rst_n = 1'b1;

        run_success(0, 16'h101, 16'h201, 32'h00100000,
                    0, 0, 1280, 720);
        run_success(1, 16'h102, 16'h202, 32'h00400000,
                    5, 0, 6, 1);
        run_success(2, 16'h103, 16'h203, 32'h00700000,
                    1279, 719, 1280, 720);
        run_success(3, 16'h104, 16'h204, 32'h00a00000,
                    10, 719, 11, 720);

        // Late cancel: the accepted return must be consumed before drained.
        check_roi_active = 1'b0;
        start_job(16'h301, 16'h401, 32'h00d00000, 10, 719, 11, 720);
        while (accepted_requests == start_request_count)
            @(negedge clk);
        cancel = 1'b1;
        @(negedge clk);
        cancel = 1'b0;
        wait_cycles = 0;
        while (!cancel_done && (wait_cycles < 100)) begin
            @(negedge clk);
            wait_cycles = wait_cycles + 1;
        end
        if (!cancel_done || !drained || busy || (reserved_count != 0))
            $fatal(1, "late cancel did not drain");
        $fwrite(log_fd, "LATE_CANCEL_DONE,%0d\n", wait_cycles);

        // No-return probe: cancel cannot clear an accepted reservation.
        hold_response = 1'b1;
        start_job(16'h302, 16'h402, 32'h01000000, 5, 0, 6, 1);
        while (accepted_requests == start_request_count)
            @(negedge clk);
        cancel = 1'b1;
        @(negedge clk);
        cancel = 1'b0;
        repeat (20) @(negedge clk);
        if (!busy || drained || (reserved_count != 1) || cancel_done)
            $fatal(1, "no-return cancel released reservation early");
        $fwrite(log_fd, "NO_RETURN_HELD,20,%0d,%0d,%0d\n",
                busy, drained, reserved_count);
        hold_response = 1'b0;
        wait_cycles = 0;
        while (!cancel_done && (wait_cycles < 100)) begin
            @(negedge clk);
            wait_cycles = wait_cycles + 1;
        end
        if (!cancel_done || !drained || busy || (reserved_count != 0))
            $fatal(1, "released no-return probe did not drain");

        if (cancel_outputs != 0 || protocol_error)
            $fatal(1, "unexpected cancel output or protocol error");
        $fwrite(log_fd,
                "SUMMARY,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d\n",
                total_roi_count, accepted_requests, returned_beats,
                scenario_requests[0], scenario_requests[1],
                scenario_requests[2], scenario_requests[3], cancel_outputs);
        $fflush(log_fd);
        repeat (3) @(posedge clk);
        $fclose(log_fd);
        $display("PASS roi=%0d accepted=%0d returned=%0d",
                 total_roi_count, accepted_requests, returned_beats);
        $finish;
    end
endmodule
