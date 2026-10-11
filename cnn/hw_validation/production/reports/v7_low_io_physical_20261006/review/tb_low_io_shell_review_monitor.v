`timescale 1ns / 1ps

// Independent, non-intrusive review monitor for the low-I/O shell testbench.
// It drives no DUT signal and is loaded as an additional ModelSim top level.
module tb_low_io_shell_review_monitor;

	integer review_cycle;
	integer preload_start_cycle;
	integer core_start_cycle;
	integer export_start_cycle;
	integer expected_preload_cycles;
	integer expected_core_cycles;
	integer expected_export_cycles;
	integer review_error_count;
	integer review_check_count;
	integer review_log;

	reg pending_preload_check;
	reg pending_core_check;
	reg pending_export_check;
	reg hold_core_payload;
	reg hold_table_payload;
	reg hold_tx_payload;
	reg [361:0]held_core_payload;
	reg [25:0]held_table_payload;
	reg [15:0]held_tx_payload;

	initial begin
		review_cycle = 0;
		preload_start_cycle = -1;
		core_start_cycle = -1;
		export_start_cycle = -1;
		expected_preload_cycles = 0;
		expected_core_cycles = 0;
		expected_export_cycles = 0;
		review_error_count = 0;
		review_check_count = 0;
		pending_preload_check = 1'b0;
		pending_core_check = 1'b0;
		pending_export_check = 1'b0;
		hold_core_payload = 1'b0;
		hold_table_payload = 1'b0;
		hold_tx_payload = 1'b0;
		held_core_payload = 362'd0;
		held_table_payload = 26'd0;
		held_tx_payload = 16'd0;
		review_log = $fopen("shell_review_monitor.csv", "w");
		$fwrite(review_log, "check,start_cycle,end_cycle,expected,observed,pass\n");
	end

	// Record protocol event endpoints before the DUT nonblocking updates.
	always@(posedge tb_road_low_io_physical_shell.i_clk)begin
		review_cycle = review_cycle + 1;
		if(tb_road_low_io_physical_shell.i_rstn == 1'b0)begin
			preload_start_cycle = -1;
			core_start_cycle = -1;
			export_start_cycle = -1;
			pending_preload_check = 1'b0;
			pending_core_check = 1'b0;
			pending_export_check = 1'b0;
		end else begin
			if((tb_road_low_io_physical_shell.dut.state_current == 4'd0) &&
			   tb_road_low_io_physical_shell.dut.flag_rx_transfer &&
			   (tb_road_low_io_physical_shell.i_rx_data == 16'h1000))begin
				preload_start_cycle = review_cycle;
			end

			if((tb_road_low_io_physical_shell.dut.state_current == 4'd0) &&
			   tb_road_low_io_physical_shell.dut.flag_rx_transfer &&
			   (tb_road_low_io_physical_shell.i_rx_data[15:12] == 4'h3) &&
			   tb_road_low_io_physical_shell.dut.flag_run_command_legal)begin
				if(preload_start_cycle < 0)begin
					review_error_count = review_error_count + 1;
				end else begin
					expected_preload_cycles = review_cycle - preload_start_cycle;
					pending_preload_check = 1'b1;
				end
			end

			if(tb_road_low_io_physical_shell.dut.flag_core_input_transfer &&
			   (tb_road_low_io_physical_shell.dut.cnt_core_inputs == 32'd0))begin
				core_start_cycle = review_cycle;
			end

			if((tb_road_low_io_physical_shell.dut.state_current == 4'd6) &&
			   tb_road_low_io_physical_shell.dut.flag_core_busy_observed &&
			   tb_road_low_io_physical_shell.dut.chain_input_ready)begin
				if(core_start_cycle < 0)begin
					review_error_count = review_error_count + 1;
				end else begin
					expected_core_cycles = review_cycle - core_start_cycle;
					pending_core_check = 1'b1;
				end
			end

			if((tb_road_low_io_physical_shell.dut.state_current == 4'd0) &&
			   tb_road_low_io_physical_shell.dut.flag_rx_transfer &&
			   (tb_road_low_io_physical_shell.i_rx_data == 16'h4000) &&
			   tb_road_low_io_physical_shell.dut.flag_normal_export_legal)begin
				export_start_cycle = review_cycle;
			end

			if((tb_road_low_io_physical_shell.dut.state_current == 4'd10) &&
			   tb_road_low_io_physical_shell.dut.flag_tx_transfer &&
			   ({1'b0, tb_road_low_io_physical_shell.dut.cnt_export_addr} + 5'd1 >=
			    {1'b0, tb_road_low_io_physical_shell.dut.reg_export_count}))begin
				if(export_start_cycle < 0)begin
					review_error_count = review_error_count + 1;
				end else begin
					expected_export_cycles = review_cycle - export_start_cycle;
					pending_export_check = 1'b1;
				end
			end
		end
	end

	// Check counters after DUT NBA updates and prove held payloads at a quiet edge.
	always@(negedge tb_road_low_io_physical_shell.i_clk)begin
		if(tb_road_low_io_physical_shell.i_rstn == 1'b0)begin
			hold_core_payload = 1'b0;
			hold_table_payload = 1'b0;
			hold_tx_payload = 1'b0;
		end else begin
			if(pending_preload_check)begin
				review_check_count = review_check_count + 1;
				$fwrite(review_log, "preload_endpoint,%0d,%0d,%0d,%0d,%0d\n",
					preload_start_cycle, review_cycle, expected_preload_cycles,
					tb_road_low_io_physical_shell.dut.cnt_preload_cycles,
					tb_road_low_io_physical_shell.dut.cnt_preload_cycles == expected_preload_cycles);
				if(tb_road_low_io_physical_shell.dut.cnt_preload_cycles != expected_preload_cycles)
					review_error_count = review_error_count + 1;
				pending_preload_check = 1'b0;
			end

			if(pending_core_check)begin
				review_check_count = review_check_count + 1;
				$fwrite(review_log, "core_endpoint,%0d,%0d,%0d,%0d,%0d\n",
					core_start_cycle, review_cycle, expected_core_cycles,
					tb_road_low_io_physical_shell.dut.cnt_core_cycles,
					tb_road_low_io_physical_shell.dut.cnt_core_cycles == expected_core_cycles);
				if(tb_road_low_io_physical_shell.dut.cnt_core_cycles != expected_core_cycles)
					review_error_count = review_error_count + 1;
				pending_core_check = 1'b0;
			end

			if(pending_export_check)begin
				review_check_count = review_check_count + 1;
				$fwrite(review_log, "export_endpoint,%0d,%0d,%0d,%0d,%0d\n",
					export_start_cycle, review_cycle, expected_export_cycles,
					tb_road_low_io_physical_shell.dut.cnt_export_cycles,
					tb_road_low_io_physical_shell.dut.cnt_export_cycles == expected_export_cycles);
				if(tb_road_low_io_physical_shell.dut.cnt_export_cycles != expected_export_cycles)
					review_error_count = review_error_count + 1;
				pending_export_check = 1'b0;
			end

			if(tb_road_low_io_physical_shell.dut.chain_input_valid &&
			   (~tb_road_low_io_physical_shell.dut.chain_input_ready))begin
				if(hold_core_payload &&
				   ({tb_road_low_io_physical_shell.dut.chain_first,
				     tb_road_low_io_physical_shell.dut.chain_last,
				     tb_road_low_io_physical_shell.dut.chain_lane_mask,
				     tb_road_low_io_physical_shell.dut.chain_activation_data,
				     tb_road_low_io_physical_shell.dut.chain_weight_data,
				     tb_road_low_io_physical_shell.dut.chain_bias_data} !== held_core_payload))begin
					review_error_count = review_error_count + 1;
					$fwrite(review_log, "core_payload_stability,%0d,%0d,1,0,0\n", review_cycle, review_cycle);
				end
				held_core_payload = {tb_road_low_io_physical_shell.dut.chain_first,
					tb_road_low_io_physical_shell.dut.chain_last,
					tb_road_low_io_physical_shell.dut.chain_lane_mask,
					tb_road_low_io_physical_shell.dut.chain_activation_data,
					tb_road_low_io_physical_shell.dut.chain_weight_data,
					tb_road_low_io_physical_shell.dut.chain_bias_data};
				hold_core_payload = 1'b1;
			end else begin
				hold_core_payload = 1'b0;
			end

			if(tb_road_low_io_physical_shell.dut.chain_table_valid &&
			   (~tb_road_low_io_physical_shell.dut.chain_table_ready))begin
				if(hold_table_payload &&
				   ({tb_road_low_io_physical_shell.dut.chain_table_addr,
				     tb_road_low_io_physical_shell.dut.chain_table_data} !== held_table_payload))begin
					review_error_count = review_error_count + 1;
					$fwrite(review_log, "table_payload_stability,%0d,%0d,1,0,0\n", review_cycle, review_cycle);
				end
				held_table_payload = {tb_road_low_io_physical_shell.dut.chain_table_addr,
					tb_road_low_io_physical_shell.dut.chain_table_data};
				hold_table_payload = 1'b1;
			end else begin
				hold_table_payload = 1'b0;
			end

			if(tb_road_low_io_physical_shell.o_tx_valid &&
			   (~tb_road_low_io_physical_shell.i_tx_ready))begin
				if(hold_tx_payload &&
				   (tb_road_low_io_physical_shell.o_tx_data !== held_tx_payload))begin
					review_error_count = review_error_count + 1;
					$fwrite(review_log, "tx_payload_stability,%0d,%0d,1,0,0\n", review_cycle, review_cycle);
				end
				held_tx_payload = tb_road_low_io_physical_shell.o_tx_data;
				hold_tx_payload = 1'b1;
			end else begin
				hold_tx_payload = 1'b0;
			end
		end
	end

endmodule
