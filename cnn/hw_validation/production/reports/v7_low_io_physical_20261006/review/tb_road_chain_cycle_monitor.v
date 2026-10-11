`timescale 1ns / 1ps

module tb_road_chain_cycle_monitor;

	integer cycle_count;
	integer start_cycle;
	integer end_cycle;
	integer response_count;
	integer trace_file;
	reg monitor_active;
	reg monitor_done;

	wire input_accept;
	wire mac_terminal;
	wire pre_round;
	wire silu_input;
	wire silu_output;
	wire post_round;
	wire cache_request;
	wire cache_response;

	assign input_accept = tb_road_onchip_chain.i_input_valid & tb_road_onchip_chain.o_input_ready;
	assign mac_terminal = tb_road_onchip_chain.dut.flag_mac_result_transfer;
	assign pre_round = (tb_road_onchip_chain.dut.state_current == 4'd3) & tb_road_onchip_chain.dut.round_result_valid;
	assign silu_input = tb_road_onchip_chain.dut.flag_silu_input_transfer;
	assign silu_output = tb_road_onchip_chain.dut.flag_silu_output_transfer;
	assign post_round = (tb_road_onchip_chain.dut.state_current == 4'd7) & tb_road_onchip_chain.dut.round_result_valid;
	assign cache_request = tb_road_onchip_chain.dut.flag_cache_request;
	assign cache_response = tb_road_onchip_chain.dut.flag_cache_response;

	initial begin
		cycle_count = 0;
		start_cycle = 0;
		end_cycle = 0;
		response_count = 0;
		monitor_active = 1'b0;
		monitor_done = 1'b0;
		trace_file = $fopen("review_cycle_trace.csv", "w");
		$fwrite(trace_file, "cycle,state,position,channel,input_accept,mac_terminal,pre_round,silu_input,silu_output,post_round,commit_alpha,commit_beta,commit_gamma,cache_request,cache_response,cache_valid,table_loaded\n");
	end

	always@(posedge tb_road_onchip_chain.i_clk)begin
		cycle_count = cycle_count + 1;
		if((monitor_done == 1'b0) && (monitor_active == 1'b0) && (input_accept == 1'b1))begin
			monitor_active = 1'b1;
			start_cycle = cycle_count;
		end
		if((monitor_active == 1'b1) && (monitor_done == 1'b0))begin
			$fwrite(trace_file, "%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%03h,%0d\n",
				cycle_count,
				tb_road_onchip_chain.dut.state_current,
				tb_road_onchip_chain.dut.cnt_position,
				tb_road_onchip_chain.dut.cnt_channel,
				input_accept,
				mac_terminal,
				pre_round,
				silu_input,
				silu_output,
				post_round,
				(tb_road_onchip_chain.dut.state_current == 4'd8),
				(tb_road_onchip_chain.dut.state_current == 4'd9),
				(tb_road_onchip_chain.dut.state_current == 4'd10),
				cache_request,
				cache_response,
				tb_road_onchip_chain.dut.reg_cache_valid,
				tb_road_onchip_chain.o_table_loaded);
			if(cache_response == 1'b1)begin
				response_count = response_count + 1;
				if(response_count == 12)begin
					end_cycle = cycle_count;
					monitor_active = 1'b0;
					monitor_done = 1'b1;
					$fclose(trace_file);
					$display("REVIEW_MONITOR base16_start=%0d base16_end=%0d endpoint_difference=%0d responses=%0d", start_cycle, end_cycle, end_cycle - start_cycle, response_count);
				end
			end
		end
	end

endmodule
