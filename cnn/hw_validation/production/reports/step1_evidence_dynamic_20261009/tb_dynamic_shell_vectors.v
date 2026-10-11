`timescale 1ns / 1ps

// Testbench: identical serialized vectors for frozen RTL and synthesized PH1P netlist.
// Verification inputs are runtime data, not synthesis constants.
module tb_dynamic_shell_vectors();

	reg reg_clk = 1'b0;
	reg reg_rstn = 1'b0;
	reg reg_rx_valid = 1'b0;
	reg [15:0] reg_rx_data = 16'd0;
	reg reg_tx_ready = 1'b0;
	wire wire_rx_ready;
	wire wire_tx_valid;
	wire [15:0] wire_tx_data;
	reg [303:0] reg_packets [0:329];
	reg [47:0] reg_expected [0:603];
	reg [2:0] reg_masks [0:329];
	reg [15:0] reg_table [0:1023];
	reg [4095:0] reg_vector_path;
	reg flag_held = 1'b0;
	reg [15:0] reg_held_data;
	reg [303:0] reg_packet;
	integer cnt_cycles = 0;
	integer idx_batch;
	integer idx_word;
	integer idx_lane;
	integer idx_result = 0;
	integer idx_table;
	integer cnt_wait;
	integer cnt_stalls = 0;

	always #5 reg_clk = !reg_clk;

	road_dynamic_chain_low_io_top dut(
		.i_clk(reg_clk), .i_rstn(reg_rstn),
		.i_rx_valid(reg_rx_valid), .i_rx_data(reg_rx_data),
		.o_rx_ready(wire_rx_ready), .o_tx_valid(wire_tx_valid),
		.o_tx_data(wire_tx_data), .i_tx_ready(reg_tx_ready)
	);

	always @(posedge reg_clk) begin
		cnt_cycles = cnt_cycles + 1;
		if (cnt_cycles > 500000) $fatal(1, " > ERR: [Verilog] shell watchdog");
		if (!reg_rstn) begin
			flag_held = 1'b0;
		end else begin
			if (flag_held && (wire_tx_valid !== 1'b1 || wire_tx_data !== reg_held_data))
				$fatal(1, " > ERR: [Verilog] result changed under backpressure");
			flag_held = wire_tx_valid === 1'b1 && !reg_tx_ready;
			if (flag_held) begin
				reg_held_data = wire_tx_data;
				cnt_stalls = cnt_stalls + 1;
			end
		end
	end

	task send_word;
		input [15:0] data;
		begin
			@(negedge reg_clk);
			reg_rx_data = data;
			reg_rx_valid = 1'b1;
			@(posedge reg_clk);
			while (wire_rx_ready !== 1'b1) @(posedge reg_clk);
			@(negedge reg_clk);
			reg_rx_valid = 1'b0;
		end
	endtask

	task expect_word;
		input [15:0] data;
		input integer delay_cycles;
		begin
			@(negedge reg_clk);
			reg_tx_ready = 1'b0;
			while (wire_tx_valid !== 1'b1) @(negedge reg_clk);
			repeat (delay_cycles) @(negedge reg_clk);
			reg_tx_ready = 1'b1;
			@(posedge reg_clk);
			if (wire_tx_valid !== 1'b1 || wire_tx_data !== data)
				$fatal(1, " > ERR: [Verilog] word mismatch batch=%0d output=%0d expected=%h actual=%h",
					idx_batch, idx_result, data, wire_tx_data);
			@(negedge reg_clk);
			reg_tx_ready = 1'b0;
		end
	endtask

	task load_table;
		begin
			send_word(16'ha000);
			for (idx_table = 0; idx_table < 1024; idx_table = idx_table + 1)
				send_word(reg_table[idx_table]);
		end
	endtask

	initial begin
		if (!$value$plusargs("VECTORS=%s", reg_vector_path))
			$fatal(1, " > ERR: [Verilog] VECTORS path required");
		$readmemh({reg_vector_path, "/packets.hex"}, reg_packets);
		$readmemh({reg_vector_path, "/expected.hex"}, reg_expected);
		$readmemh({reg_vector_path, "/masks.hex"}, reg_masks);
		$readmemh({reg_vector_path, "/table.hex"}, reg_table);
		// Actual vendor GSR completes at 20 ns; keep user reset asserted beyond it.
		repeat (10) @(negedge reg_clk);
		reg_rstn = 1'b1;
		repeat (4) @(negedge reg_clk);
		load_table;
		for (idx_batch = 0; idx_batch < 330; idx_batch = idx_batch + 1) begin
			send_word(16'hb000);
			reg_packet = reg_packets[idx_batch];
			for (idx_word = 0; idx_word < 19; idx_word = idx_word + 1) begin
				send_word(reg_packet[15:0]);
				reg_packet = reg_packet >> 16;
			end
			for (idx_lane = 0; idx_lane < 3; idx_lane = idx_lane + 1) begin
				if (reg_masks[idx_batch][idx_lane]) begin
					expect_word(reg_expected[idx_result][15:0], idx_result % 7);
					expect_word(reg_expected[idx_result][31:16], idx_result % 5);
					expect_word(reg_expected[idx_result][47:32], idx_result % 3);
					idx_result = idx_result + 1;
				end
			end
		end
		send_word(16'hc000);
		expect_word(16'd330, 8);
		expect_word(16'd604, 8);
		expect_word(16'd2, 8);
		// Cancel a half-loaded packet: it must not become a transaction after reset.
		send_word(16'hb000);
		repeat (9) send_word(16'hffff);
		@(negedge reg_clk); reg_rstn = 1'b0;
		repeat (4) @(negedge reg_clk);
		reg_rstn = 1'b1;
		repeat (4) @(negedge reg_clk);
		send_word(16'hc000);
		expect_word(16'd0, 8);
		expect_word(16'd0, 8);
		expect_word(16'd0, 8);
		load_table;
		send_word(16'hc000);
		expect_word(16'd0, 8);
		expect_word(16'd0, 8);
		expect_word(16'd2, 8);
		if (idx_result != 604 || cnt_stalls == 0)
			$fatal(1, " > ERR: [Verilog] coverage not reached");
		$display(" > INFO: [Verilog] TB_PASS_DYNAMIC_SHELL packets=330 outputs=604 stalls=%0d cycles=%0d", cnt_stalls, cnt_cycles);
		$finish;
	end
endmodule
