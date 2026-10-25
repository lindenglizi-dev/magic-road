`timescale 1ps/1ps

module tb_road_time_snapshot;
	reg i_src_clk = 1'b0;
	reg i_dst_clk = 1'b0;
	reg i_rstn = 1'b0;
	reg [31:0] i_src_epoch = 32'h10203040;
	reg src_clock_enable = 1'b1;
	wire [63:0] o_src_now_ms;
	wire o_src_tick;
	wire o_src_busy;
	wire [63:0] o_dst_now_ms;
	wire [31:0] o_dst_epoch;
	wire o_dst_time_valid;
	wire o_dst_update;

	integer case_id = 0;
	integer src_cycles = 0;
	integer dst_cycles = 0;
	integer ticks = 0;
	integer updates = 0;
	integer watchdog_invalid = 0;
	integer watchdog_elapsed = 0;
	integer last_update_dst_cycle = -1;
	integer last_tick_cycle = -1;
	integer request_dst_cycle = -1;
	integer busy_start_cycle = -1;
	integer req_update_min = 32'h7fffffff;
	integer req_update_max = 0;
	integer roundtrip_min = 32'h7fffffff;
	integer roundtrip_max = 0;
	integer latency;
	reg request_pending = 1'b0;
	reg busy_was_high = 1'b0;
	reg valid_was_high = 1'b0;
	reg [63:0] busy_now_ms = 64'd0;
	reg [31:0] busy_epoch = 32'd0;
	reg [63:0] last_dst_ms = 64'd0;

	road_time_snapshot dut(
		.i_src_clk(i_src_clk), .i_dst_clk(i_dst_clk), .i_rstn(i_rstn),
		.i_src_epoch(i_src_epoch), .o_src_now_ms(o_src_now_ms),
		.o_src_tick(o_src_tick), .o_src_busy(o_src_busy),
		.o_dst_now_ms(o_dst_now_ms), .o_dst_epoch(o_dst_epoch),
		.o_dst_time_valid(o_dst_time_valid), .o_dst_update(o_dst_update)
	);

	always begin
		#5000;
		if(src_clock_enable)
			i_src_clk = ~i_src_clk;
	end

	initial begin
		#2300;
		forever #6667 i_dst_clk = ~i_dst_clk;
	end

	always @(posedge i_src_clk) begin
		src_cycles = src_cycles + 1;
		#1;
		if(!i_rstn) begin
			last_tick_cycle = -1;
			busy_was_high = 1'b0;
			request_pending = 1'b0;
		end else begin
			if(o_src_tick) begin
				ticks = ticks + 1;
				if(last_tick_cycle >= 0 && src_cycles-last_tick_cycle != 100000)
					$fatal(1,"source tick spacing=%0d expected=100000",src_cycles-last_tick_cycle);
				last_tick_cycle = src_cycles;
				if(request_pending)
					$fatal(1,"new source tick while prior CDC request pending");
				request_pending = 1'b1;
				request_dst_cycle = dst_cycles;
			end
			if(o_src_busy && !busy_was_high) begin
				busy_start_cycle = src_cycles;
				busy_now_ms = o_src_now_ms;
				busy_epoch = i_src_epoch;
			end
			if(o_src_busy) begin
				if(o_src_now_ms !== busy_now_ms)
					$fatal(1,"source time payload changed while busy old=%0d new=%0d",busy_now_ms,o_src_now_ms);
				if(i_src_epoch !== busy_epoch)
					$fatal(1,"testbench changed epoch while source busy");
			end
			if(!o_src_busy && busy_was_high) begin
				latency = src_cycles-busy_start_cycle;
				if(latency < roundtrip_min) roundtrip_min = latency;
				if(latency > roundtrip_max) roundtrip_max = latency;
				if(latency <= 0 || latency > 32)
					$fatal(1,"source busy roundtrip latency out of bound=%0d",latency);
			end
			busy_was_high = o_src_busy;
		end
	end

	always @(posedge i_dst_clk) begin
		dst_cycles = dst_cycles + 1;
		#1;
		if(!i_rstn) begin
			valid_was_high = 1'b0;
			last_dst_ms = 64'd0;
		end else begin
			if(o_dst_update) begin
				if(!request_pending)
					$fatal(1,"destination update without source request");
				latency = dst_cycles-request_dst_cycle;
				if(latency < req_update_min) req_update_min = latency;
				if(latency > req_update_max) req_update_max = latency;
				if(latency <= 0 || latency > 16)
					$fatal(1,"request-to-destination latency out of bound=%0d",latency);
				if(updates > 0 && o_dst_now_ms <= last_dst_ms)
					$fatal(1,"destination time did not advance old=%0d new=%0d",last_dst_ms,o_dst_now_ms);
				if(o_dst_now_ms !== o_src_now_ms)
					$fatal(1,"destination snapshot time mismatch src=%0d dst=%0d",o_src_now_ms,o_dst_now_ms);
				if(o_dst_epoch !== busy_epoch)
					$fatal(1,"destination snapshot epoch mismatch expected=%h actual=%h",busy_epoch,o_dst_epoch);
				last_dst_ms = o_dst_now_ms;
				updates = updates + 1;
				last_update_dst_cycle = dst_cycles;
				request_pending = 1'b0;
			end
			if(valid_was_high && !o_dst_time_valid) begin
				watchdog_invalid = watchdog_invalid + 1;
				watchdog_elapsed = dst_cycles-last_update_dst_cycle;
				if(watchdog_elapsed != 150001)
					$fatal(1,"watchdog elapsed=%0d expected=150001",watchdog_elapsed);
			end
			valid_was_high = o_dst_time_valid;
		end
	end

	task reset_both;
		begin
			i_rstn = 1'b0;
			repeat(4) @(posedge i_src_clk);
			i_rstn = 1'b1;
			repeat(4) @(posedge i_src_clk);
		end
	endtask

	initial begin
		if(!$value$plusargs("CASE=%d",case_id))
			case_id = 0;
		if(case_id != 0 && case_id != 1)
			$fatal(1,"unsupported time case %0d",case_id);
		reset_both;

		if(case_id == 0) begin
			wait(updates >= 3);
			wait(!o_src_busy);
			@(negedge i_src_clk); i_src_epoch = 32'h55667788;
			wait(updates >= 6);
			if(o_dst_epoch !== 32'h55667788 || o_dst_time_valid !== 1'b1)
				$fatal(1,"epoch or validity did not propagate epoch=%h valid=%b",o_dst_epoch,o_dst_time_valid);
			if(watchdog_invalid != 0)
				$fatal(1,"unexpected watchdog invalid event");
		end else begin
			wait(updates >= 2 && o_dst_time_valid);
			@(negedge i_src_clk); src_clock_enable = 1'b0;
			wait(!o_dst_time_valid);
			#2;
			if(watchdog_invalid != 1)
				$fatal(1,"watchdog invalid count=%0d expected=1",watchdog_invalid);
			repeat(32) @(posedge i_dst_clk);
			src_clock_enable = 1'b1;
			wait(updates >= 4 && o_dst_time_valid);
			if(o_dst_now_ms < 4)
				$fatal(1,"source clock recovery did not resume snapshots now=%0d",o_dst_now_ms);
		end

		if(req_update_min == 32'h7fffffff || roundtrip_min == 32'h7fffffff)
			$fatal(1,"latency metrics were not observed");
		$display("TB_PASS_TIME case=%0d src_cycles=%0d dst_cycles=%0d ticks=%0d updates=%0d req_update_min=%0d req_update_max=%0d roundtrip_min=%0d roundtrip_max=%0d watchdog_invalid=%0d watchdog_elapsed=%0d",
			case_id,src_cycles,dst_cycles,ticks,updates,req_update_min,req_update_max,
			roundtrip_min,roundtrip_max,watchdog_invalid,watchdog_elapsed);
		$finish;
	end

	initial begin
		#(64'd10000000000);
		$fatal(1,"time snapshot timeout");
	end
endmodule
