`timescale 1ps/1ps

module tb_time_table_integrated;
	localparam [31:0] EXPECTED_MODEL_ID = 32'hB35D4A66;
	reg i_src_clk = 1'b0;
	reg i_dst_clk = 1'b0;
	reg i_rstn = 1'b0;
	reg src_clock_enable = 1'b1;
	reg [31:0] i_src_epoch = 32'h22334455;
	reg i_src_entry_valid = 1'b0;
	reg [96:0] i_src_entry = 97'd0;
	reg i_src_meta_valid = 1'b0;
	reg [264:0] i_src_metadata = 265'd0;
	reg i_src_abort = 1'b0;
	reg i_dst_copy_enable = 1'b1;
	reg i_dst_sof = 1'b0;
	reg [5:0] i_dst_read_index = 6'd0;

	wire [63:0] src_now_ms;
	wire src_tick;
	wire time_src_busy;
	wire [63:0] dst_now_ms;
	wire [31:0] dst_epoch;
	wire dst_time_valid;
	wire dst_time_update;
	wire src_entry_ready;
	wire src_meta_ready;
	wire src_copy_ack;
	wire table_src_busy;
	wire src_error;
	wire [96:0] dst_entry;
	wire [264:0] dst_metadata;
	wire dst_active_valid;
	wire dst_draw_valid;
	wire dst_pending_valid;
	wire dst_copy_busy;
	wire dst_table_update;
	wire [63:0] dst_age_upper_ms;
	wire dst_error;

	integer case_id = 20;
	integer src_cycles = 0;
	integer dst_cycles = 0;
	integer time_updates = 0;
	integer tables = 0;
	integer acks = 0;
	integer active_updates = 0;
	integer watchdog_invalid = 0;
	integer copy_wait_start = -1;
	integer copy_wait = 0;
	integer update_mark;
	integer wait_count;
	reg valid_was_high = 1'b0;
	reg [63:0] capture_a;
	reg [63:0] capture_b;
	reg [264:0] meta_a;
	reg [264:0] meta_b;

	road_time_snapshot u_time(
		.i_src_clk(i_src_clk), .i_dst_clk(i_dst_clk), .i_rstn(i_rstn),
		.i_src_epoch(i_src_epoch), .o_src_now_ms(src_now_ms), .o_src_tick(src_tick),
		.o_src_busy(time_src_busy), .o_dst_now_ms(dst_now_ms), .o_dst_epoch(dst_epoch),
		.o_dst_time_valid(dst_time_valid), .o_dst_update(dst_time_update)
	);

	road_detection_table_cdc #(
		.AGE_LIMIT_MS(500), .EXPECTED_MODEL_ID(EXPECTED_MODEL_ID)
	) u_table(
		.i_src_clk(i_src_clk), .i_dst_clk(i_dst_clk), .i_rstn(i_rstn),
		.i_src_entry_valid(i_src_entry_valid), .i_src_entry(i_src_entry),
		.o_src_entry_ready(src_entry_ready), .i_src_meta_valid(i_src_meta_valid),
		.i_src_metadata(i_src_metadata), .o_src_meta_ready(src_meta_ready),
		.i_src_abort(i_src_abort), .o_src_copy_ack(src_copy_ack),
		.o_src_busy(table_src_busy), .o_src_error(src_error),
		.i_dst_copy_enable(i_dst_copy_enable), .i_dst_sof(i_dst_sof),
		.i_dst_now_ms(dst_now_ms), .i_dst_time_epoch(dst_epoch),
		.i_dst_time_valid(dst_time_valid), .i_dst_read_index(i_dst_read_index),
		.o_dst_entry(dst_entry), .o_dst_metadata(dst_metadata),
		.o_dst_active_valid(dst_active_valid), .o_dst_draw_valid(dst_draw_valid),
		.o_dst_pending_valid(dst_pending_valid), .o_dst_copy_busy(dst_copy_busy),
		.o_dst_update(dst_table_update), .o_dst_age_upper_ms(dst_age_upper_ms),
		.o_dst_error(dst_error)
	);

	always begin
		#5000;
		if(src_clock_enable) i_src_clk = ~i_src_clk;
	end

	initial begin
		#2300;
		forever #6667 i_dst_clk = ~i_dst_clk;
	end

	function [96:0] make_entry;
		input [31:0] serial;
		begin
			make_entry={serial[0],serial^32'h55AA55AA,serial+32'h10203040,serial^32'hDEADBEEF};
		end
	endfunction

	function [264:0] make_metadata;
		input [31:0] frame_id;
		input [63:0] capture_ms;
		begin
			make_metadata={capture_ms,capture_ms,2'b00,7'd1,EXPECTED_MODEL_ID,
				frame_id,32'h77889900,i_src_epoch};
		end
	endfunction

	always @(posedge i_src_clk) begin
		src_cycles=src_cycles+1;
		#1;
		if(i_rstn) begin
			if(src_copy_ack) acks=acks+1;
			if(src_error) $fatal(1,"integrated source protocol error");
		end
	end

	always @(posedge i_dst_clk) begin
		dst_cycles=dst_cycles+1;
		#1;
		if(!i_rstn) begin
			valid_was_high=0;
			copy_wait_start=-1;
		end else begin
			if(dst_time_update) time_updates=time_updates+1;
			if(dst_table_update) active_updates=active_updates+1;
			if(valid_was_high && !dst_time_valid) watchdog_invalid=watchdog_invalid+1;
			valid_was_high=dst_time_valid;
			if(dst_copy_busy && copy_wait_start<0) copy_wait_start=dst_cycles;
			if(!dst_copy_busy && copy_wait_start>=0) begin
				if(dst_cycles-copy_wait_start>copy_wait) copy_wait=dst_cycles-copy_wait_start;
				copy_wait_start=-1;
			end
			if(dst_error) $fatal(1,"integrated destination protocol error");
		end
	end

	task send_one;
		input [31:0] serial;
		input [264:0] metadata;
		begin
			@(negedge i_src_clk); i_src_entry=make_entry(serial); i_src_entry_valid=1;
			#1;
			wait_count=0;
			while(!src_entry_ready) begin
				@(negedge i_src_clk); #1; wait_count=wait_count+1;
				if(wait_count>200) $fatal(1,"integrated entry handshake timeout");
			end
			@(posedge i_src_clk);
			@(negedge i_src_clk); i_src_entry_valid=0; i_src_metadata=metadata; i_src_meta_valid=1;
			#1;
			wait_count=0;
			while(!src_meta_ready) begin
				@(negedge i_src_clk); #1; wait_count=wait_count+1;
				if(wait_count>200) $fatal(1,"integrated metadata handshake timeout");
			end
			@(posedge i_src_clk);
			@(negedge i_src_clk); i_src_meta_valid=0;
			tables=tables+1;
		end
	endtask

	task wait_ack;
		begin
			wait_count=0;
			while(!src_copy_ack) begin
				@(posedge i_src_clk); #1; wait_count=wait_count+1;
				if(wait_count>300000) $fatal(1,"integrated copy acknowledgement timeout");
			end
		end
	endtask

	task sof_expect_update;
		begin
			@(negedge i_dst_clk); i_dst_sof=1;
			@(posedge i_dst_clk); #1;
			if(!dst_table_update) $fatal(1,"integrated SOF did not activate pending table");
			@(negedge i_dst_clk); i_dst_sof=0;
		end
	endtask

	initial begin
		if(!$value$plusargs("CASE=%d",case_id)) case_id=20;
		if(case_id!=20) $fatal(1,"unsupported integrated case %0d",case_id);
		i_rstn=0;
		repeat(4) @(posedge i_src_clk);
		i_rstn=1;
		wait(dst_time_valid && time_updates>=1);

		wait(!time_src_busy);
		@(negedge i_src_clk); capture_a=src_now_ms; meta_a=make_metadata(32'hA1,capture_a);
		send_one(32'hA1,meta_a);
		wait_ack;
		if(!dst_pending_valid) $fatal(1,"first integrated table not pending");

		wait(!time_src_busy);
		@(negedge i_src_clk); capture_b=src_now_ms; meta_b=make_metadata(32'hB2,capture_b);
		send_one(32'hB2,meta_b);
		if(!table_src_busy) $fatal(1,"second integrated table not held while pending full");
		i_dst_copy_enable=0;
		update_mark=time_updates;
		while(time_updates<update_mark+2) @(posedge i_dst_clk);
		if(src_copy_ack || !table_src_busy)
			$fatal(1,"pending-full/disabled copy was acknowledged early");

		sof_expect_update;
		#1000;
		if(!dst_active_valid || !dst_draw_valid || dst_metadata!==meta_a || dst_entry!==make_entry(32'hA1))
			$fatal(1,"direct-time first table did not draw correctly");
		update_mark=time_updates;
		while(time_updates<update_mark+1) @(posedge i_dst_clk);
		if(!dst_draw_valid) $fatal(1,"time updates stopped or draw dropped during copy backpressure");
		i_dst_copy_enable=1;
		wait_ack;
		sof_expect_update;
		#1000;
		if(!dst_draw_valid || dst_metadata!==meta_b || dst_entry!==make_entry(32'hB2))
			$fatal(1,"direct-time second table did not draw correctly");

		@(negedge i_src_clk); src_clock_enable=0;
		wait(!dst_time_valid);
		#1000;
		if(dst_draw_valid || dst_age_upper_ms!==64'hFFFFFFFFFFFFFFFF)
			$fatal(1,"watchdog expiry did not withdraw draw and mark age unknown");
		if(watchdog_invalid!=1) $fatal(1,"integrated watchdog invalid count=%0d",watchdog_invalid);
		repeat(16) @(posedge i_dst_clk);
		update_mark=time_updates;
		src_clock_enable=1;
		while(time_updates==update_mark) @(posedge i_dst_clk);
		#1000;
		if(!dst_time_valid || !dst_draw_valid)
			$fatal(1,"first recovered time snapshot did not restore draw");

		$display("TB_PASS_INTEGRATED case=%0d src_cycles=%0d dst_cycles=%0d time_updates=%0d tables=%0d acks=%0d active_updates=%0d copy_wait=%0d watchdog_invalid=%0d",
			case_id,src_cycles,dst_cycles,time_updates,tables,acks,active_updates,copy_wait,watchdog_invalid);
		$finish;
	end

	initial begin
		#(64'd12000000000);
		$fatal(1,"integrated time/table timeout");
	end
endmodule
