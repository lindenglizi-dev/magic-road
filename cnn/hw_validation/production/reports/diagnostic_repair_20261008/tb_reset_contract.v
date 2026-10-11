`timescale 1ns / 1ps
// 检查数字仿真的取消与释放语义；不模拟亚稳态或证明MTBF。
module tb_reset_contract;
    reg clk = 0;
    reg rstn = 0;
    reg rx_valid = 0;
    reg tx_ready = 0;
    reg [15:0] rx_data = 0;
    wire rx_ready, tx_valid;
    wire [15:0] tx_data;
    reg [15:0] table_words [0:1023];
    reg [303:0] packet;
    integer checks = 0, cycles = 0, address, index, waited;
    reg held = 0;
    reg [15:0] held_data;
    reg [15:0] value;
    always #5 clk = !clk;
    road_dynamic_low_io_top dut(clk,rstn,rx_valid,rx_data,rx_ready,tx_valid,tx_data,tx_ready);
    always @(posedge clk) begin
        cycles = cycles + 1;
        if (cycles > 100000) $fatal(1,"reset-contract watchdog");
        if (!rstn) held = 0;
        else begin
            if (held && (!tx_valid || tx_data !== held_data)) $fatal(1,"TX payload changed under stall");
            held = tx_valid && !tx_ready;
            held_data = tx_data;
            if (dut.state_current == 3'd4 && dut.flag_output_valid && !dut.u_chain.o_output_valid)
                $fatal(1,"missing chain valid");
        end
    end
    task cancel;
        begin
            rstn = 0; rx_valid = 0; tx_ready = 0;
            #0.001;
            if (rx_ready || tx_valid || dut.flag_table_loaded || dut.reg_input_count || dut.reg_output_count)
                $fatal(1,"asynchronous cancel or table invalidation failed");
            held = 0;
        end
    endtask
    task release_at;
        input real offset;
        integer edge_count;
        begin
            @(negedge clk); cancel;
            @(negedge clk); #offset; rstn = 1;
            edge_count = 0;
            while (!rx_ready) begin
                @(posedge clk); #0.001;
                edge_count = edge_count + 1;
                if (edge_count == 1 && rx_ready) $fatal(1,"released after only one edge");
                if (edge_count > 3) $fatal(1,"release did not finish");
            end
            if (dut.flag_table_loaded || dut.flag_input_ready || tx_valid)
                $fatal(1,"compute permission before reload");
            checks = checks + 1;
        end
    endtask
    task send;
        input [15:0] word;
        begin
            @(negedge clk); rx_valid = 1; rx_data = word;
            begin: wait_accept
                forever begin
                    @(posedge clk);
                    if (rx_ready) disable wait_accept;
                end
            end
            @(negedge clk); rx_valid = 0; rx_data = 16'hdead;
        end
    endtask
    task receive;
        output [15:0] word;
        begin
            @(negedge clk); tx_ready = 1;
            begin: wait_result
                forever begin
                    @(posedge clk);
                    if (tx_valid) begin word = tx_data; disable wait_result; end
                end
            end
            @(negedge clk); tx_ready = 0;
        end
    endtask
    task load_table;
        begin
            send(16'ha000);
            for (address = 0; address < 1023; address = address + 1) begin
                send(table_words[address]);
                if (dut.flag_table_loaded || dut.flag_input_ready) $fatal(1,"partial table accepted for compute");
            end
            send(table_words[1023]);
            if (!dut.flag_table_loaded) $fatal(1,"complete table not published");
        end
    endtask
    task send_packet;
        input integer words;
        begin
            send(16'hb000);
            for (index = 0; index < words; index = index + 1)
                send(packet[index*16+:16]);
        end
    endtask
    initial begin
        $readmemh("table.hex",table_words);
        // 单路INT16旁路：acc=-123、乘数1、shift0，tag=A555。
        packet = 304'd0;
        packet[31:0] = -32'sd123;
        packet[127:96] = 32'd1;
        packet[251:249] = 3'b001;
        packet[267:252] = 16'ha555;
        release_at(4.999);
        release_at(5.000);
        release_at(5.001);
        send(16'ha000);
        for (address = 0; address < 17; address = address + 1) send(table_words[address]);
        @(negedge clk); cancel;
        release_at(4.999); checks = checks + 1;
        load_table;
        send_packet(18);
        repeat (20) @(negedge clk);
        if (tx_valid || dut.reg_input_count) $fatal(1,"partial packet submitted");
        cancel; release_at(5.001); checks = checks + 1;
        load_table;
        send_packet(19);
        if (dut.state_current !== 3'd3) $fatal(1,"expected SUBMIT before cancel");
        cancel; release_at(4.999); checks = checks + 1;
        load_table;
        send_packet(19);
        @(negedge clk);
        if (dut.state_current !== 3'd4) $fatal(1,"expected WAIT before cancel");
        cancel; release_at(5.001); checks = checks + 1;
        load_table;
        send_packet(19);
        waited = 0;
        while (!tx_valid) begin
            @(negedge clk); waited = waited + 1;
            if (waited > 150) $fatal(1,"result did not arrive");
        end
        repeat (32) @(negedge clk);
        cancel; release_at(4.999); checks = checks + 1;
        repeat (50) @(negedge clk);
        if (tx_valid || dut.reg_input_count || dut.reg_output_count) $fatal(1,"old result leaked after reset");
        load_table;
        send_packet(19);
        receive(value); if (value !== 16'ha555) $fatal(1,"new tag mismatch");
        receive(value); if (value !== 16'hff85) $fatal(1,"new result mismatch");
        receive(value); if (value !== 16'd2) $fatal(1,"new status mismatch");
        repeat (30) @(negedge clk);
        if (tx_valid || dut.reg_input_count != 1 || dut.reg_output_count != 1)
            $fatal(1,"duplicate or lost result");
        $display("RESET_CONTRACT_PASS checks=%0d near_edge=3 table_reset=1 packet_reset=1 submit_reset=1 wait_reset=1 tx_stall_reset=1 reload=1 no_old_result=1",checks);
        $finish;
    end
endmodule
