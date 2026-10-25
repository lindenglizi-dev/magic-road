`timescale 1ps/1ps

module tb_road_detection_table_cdc;
	localparam [31:0] EXPECTED_MODEL_ID = 32'hB35D4A66;

	reg i_src_clk = 1'b0;
	reg i_dst_clk = 1'b0;
	reg i_rstn = 1'b0;
	reg i_src_entry_valid = 1'b0;
	reg [96:0] i_src_entry = 97'd0;
	reg i_src_meta_valid = 1'b0;
	reg [264:0] i_src_metadata = 265'd0;
	reg i_src_abort = 1'b0;
	reg i_dst_copy_enable = 1'b1;
	reg i_dst_sof = 1'b0;
	reg [63:0] i_dst_now_ms = 64'd0;
	reg [31:0] i_dst_time_epoch = 32'd0;
	reg i_dst_time_valid = 1'b0;
	reg [5:0] i_dst_read_index = 6'd0;

	wire o_src_entry_ready_500;
	wire o_src_meta_ready_500;
	wire o_src_copy_ack_500;
	wire o_src_busy_500;
	wire o_src_error_500;
	wire [96:0] o_dst_entry_500;
	wire [264:0] o_dst_metadata_500;
	wire o_dst_active_valid_500;
	wire o_dst_draw_valid_500;
	wire o_dst_pending_valid_500;
	wire o_dst_copy_busy_500;
	wire o_dst_update_500;
	wire [63:0] o_dst_age_upper_ms_500;
	wire o_dst_error_500;

	wire o_src_entry_ready_2000;
	wire o_src_meta_ready_2000;
	wire o_src_copy_ack_2000;
	wire o_src_busy_2000;
	wire o_src_error_2000;
	wire [96:0] o_dst_entry_2000;
	wire [264:0] o_dst_metadata_2000;
	wire o_dst_active_valid_2000;
	wire o_dst_draw_valid_2000;
	wire o_dst_pending_valid_2000;
	wire o_dst_copy_busy_2000;
	wire o_dst_update_2000;
	wire [63:0] o_dst_age_upper_ms_2000;
	wire o_dst_error_2000;

	integer case_id = 10;
	integer src_cycles = 0;
	integer dst_cycles = 0;
	integer sealed_tables = 0;
	integer accepted_entries = 0;
	integer copy_acks = 0;
	integer active_updates = 0;
	integer common_resets = 0;
	integer max_copy_wait = 0;
	integer source_error_pulses = 0;
	integer burst_entries = 0;
	integer copy_wait_start = -1;
	integer this_wait;
	integer table_serial = 0;
	integer index;
	integer pos;
	integer wait_count;
	reg [31:0] lfsr = 32'h13579BDF;
	reg [264:0] expected_meta;
	reg [264:0] cpu_metadata [0:4];
	reg [96:0] cpu_entries [0:319];
	reg [264:0] cpu_diag_metadata [0:2];
	reg [96:0] cpu_diag_entries [0:2];
	reg [1023:0] metadata_vector_path;
	reg [1023:0] entries_vector_path;
	reg [1023:0] diagnostic_metadata_path;
	reg [1023:0] diagnostic_entries_path;

	road_detection_table_cdc #(
		.AGE_LIMIT_MS(500), .EXPECTED_MODEL_ID(EXPECTED_MODEL_ID)
	) dut500(
		.i_src_clk(i_src_clk), .i_dst_clk(i_dst_clk), .i_rstn(i_rstn),
		.i_src_entry_valid(i_src_entry_valid), .i_src_entry(i_src_entry),
		.o_src_entry_ready(o_src_entry_ready_500), .i_src_meta_valid(i_src_meta_valid),
		.i_src_metadata(i_src_metadata), .o_src_meta_ready(o_src_meta_ready_500),
		.i_src_abort(i_src_abort), .o_src_copy_ack(o_src_copy_ack_500),
		.o_src_busy(o_src_busy_500), .o_src_error(o_src_error_500),
		.i_dst_copy_enable(i_dst_copy_enable), .i_dst_sof(i_dst_sof),
		.i_dst_now_ms(i_dst_now_ms), .i_dst_time_epoch(i_dst_time_epoch),
		.i_dst_time_valid(i_dst_time_valid), .i_dst_read_index(i_dst_read_index),
		.o_dst_entry(o_dst_entry_500), .o_dst_metadata(o_dst_metadata_500),
		.o_dst_active_valid(o_dst_active_valid_500), .o_dst_draw_valid(o_dst_draw_valid_500),
		.o_dst_pending_valid(o_dst_pending_valid_500), .o_dst_copy_busy(o_dst_copy_busy_500),
		.o_dst_update(o_dst_update_500), .o_dst_age_upper_ms(o_dst_age_upper_ms_500),
		.o_dst_error(o_dst_error_500)
	);

	road_detection_table_cdc #(
		.AGE_LIMIT_MS(2000), .EXPECTED_MODEL_ID(EXPECTED_MODEL_ID)
	) dut2000(
		.i_src_clk(i_src_clk), .i_dst_clk(i_dst_clk), .i_rstn(i_rstn),
		.i_src_entry_valid(i_src_entry_valid), .i_src_entry(i_src_entry),
		.o_src_entry_ready(o_src_entry_ready_2000), .i_src_meta_valid(i_src_meta_valid),
		.i_src_metadata(i_src_metadata), .o_src_meta_ready(o_src_meta_ready_2000),
		.i_src_abort(i_src_abort), .o_src_copy_ack(o_src_copy_ack_2000),
		.o_src_busy(o_src_busy_2000), .o_src_error(o_src_error_2000),
		.i_dst_copy_enable(i_dst_copy_enable), .i_dst_sof(i_dst_sof),
		.i_dst_now_ms(i_dst_now_ms), .i_dst_time_epoch(i_dst_time_epoch),
		.i_dst_time_valid(i_dst_time_valid), .i_dst_read_index(i_dst_read_index),
		.o_dst_entry(o_dst_entry_2000), .o_dst_metadata(o_dst_metadata_2000),
		.o_dst_active_valid(o_dst_active_valid_2000), .o_dst_draw_valid(o_dst_draw_valid_2000),
		.o_dst_pending_valid(o_dst_pending_valid_2000), .o_dst_copy_busy(o_dst_copy_busy_2000),
		.o_dst_update(o_dst_update_2000), .o_dst_age_upper_ms(o_dst_age_upper_ms_2000),
		.o_dst_error(o_dst_error_2000)
	);

	always #5000 i_src_clk = ~i_src_clk;
	initial begin
		#2300;
		forever #6667 i_dst_clk = ~i_dst_clk;
	end

	function [96:0] make_entry;
		input [31:0] serial;
		input [31:0] item;
		begin
			make_entry = {serial[0],serial ^ 32'hA5A55A5A,item,serial + item + 32'h12340000};
		end
	endfunction

	function [264:0] make_metadata;
		input [31:0] epoch;
		input [31:0] task_id;
		input [31:0] frame_id;
		input [31:0] model_id;
		input [6:0] count;
		input [1:0] status;
		input [63:0] capture_ms;
		input [63:0] completion_ms;
		begin
			make_metadata = {completion_ms,capture_ms,status,count,model_id,frame_id,task_id,epoch};
		end
	endfunction

	always @(posedge i_src_clk) begin
		src_cycles = src_cycles + 1;
		#1;
		if(i_rstn) begin
			if(o_src_entry_ready_500 !== o_src_entry_ready_2000 ||
			   o_src_meta_ready_500 !== o_src_meta_ready_2000 ||
			   o_src_busy_500 !== o_src_busy_2000 || o_src_copy_ack_500 !== o_src_copy_ack_2000 ||
			   o_src_error_500 !== o_src_error_2000)
				$fatal(1,"parameter instances disagree in source protocol");
			if(o_src_copy_ack_500)
				copy_acks = copy_acks + 1;
			if(o_src_error_500)
				source_error_pulses = source_error_pulses + 1;
			if(case_id != 14 && (o_src_error_500 || o_src_error_2000))
				$fatal(1,"unexpected source protocol error");
		end
	end

	always @(posedge i_dst_clk) begin
		dst_cycles = dst_cycles + 1;
		#1;
		if(i_rstn) begin
			if(o_dst_pending_valid_500 !== o_dst_pending_valid_2000 ||
			   o_dst_copy_busy_500 !== o_dst_copy_busy_2000 ||
			   o_dst_update_500 !== o_dst_update_2000 ||
			   o_dst_active_valid_500 !== o_dst_active_valid_2000 ||
			   o_dst_metadata_500 !== o_dst_metadata_2000 ||
			   o_dst_entry_500 !== o_dst_entry_2000 ||
			   o_dst_age_upper_ms_500 !== o_dst_age_upper_ms_2000 ||
			   o_dst_error_500 !== o_dst_error_2000)
				$fatal(1,"parameter instances disagree outside draw-age decision");
			if(o_dst_copy_busy_500 && copy_wait_start < 0)
				copy_wait_start = dst_cycles;
			if(!o_dst_copy_busy_500 && copy_wait_start >= 0) begin
				this_wait = dst_cycles-copy_wait_start;
				if(this_wait > max_copy_wait) max_copy_wait = this_wait;
				copy_wait_start = -1;
			end
			if(o_dst_update_500)
				active_updates = active_updates + 1;
			if(case_id != 14 && (o_dst_error_500 || o_dst_error_2000))
				$fatal(1,"unexpected destination protocol error");
		end else begin
			copy_wait_start = -1;
		end
	end

	task clear_inputs;
		begin
			i_src_entry_valid=0; i_src_entry=0; i_src_meta_valid=0; i_src_metadata=0; i_src_abort=0;
			i_dst_copy_enable=1; i_dst_sof=0; i_dst_now_ms=0; i_dst_time_epoch=0;
			i_dst_time_valid=0; i_dst_read_index=0;
		end
	endtask

	task publish_cpu_diagnostic;
		input integer diagnostic_index;
		begin
			send_entry_value(cpu_diag_entries[diagnostic_index],0);
			@(negedge i_src_clk);
			i_src_metadata=cpu_diag_metadata[diagnostic_index];
			i_src_meta_valid=1;
			#1;
			wait_count=0;
			while(!(o_src_meta_ready_500 && o_src_meta_ready_2000)) begin
				@(negedge i_src_clk); #1; wait_count=wait_count+1;
				if(wait_count>200) $fatal(1,"CPU diagnostic metadata timeout index=%0d",diagnostic_index);
			end
			@(posedge i_src_clk);
			@(negedge i_src_clk); i_src_meta_valid=0;
			sealed_tables=sealed_tables+1;
			wait_copy_ack;
			sof_and_require_update;
			i_dst_read_index=0; #1000;
			if(!o_dst_active_valid_500 || o_dst_draw_valid_500 ||
			   o_dst_metadata_500!==cpu_diag_metadata[diagnostic_index] ||
			   o_dst_entry_500!==cpu_diag_entries[diagnostic_index])
				$fatal(1,"CPU diagnostic copy mismatch index=%0d",diagnostic_index);
			if(o_dst_age_upper_ms_500!==64'd500 || o_dst_age_upper_ms_2000!==64'd500)
				$fatal(1,"status diagnostic mathematical age mismatch index=%0d",diagnostic_index);
		end
	endtask

	task reset_both;
		begin
			clear_inputs;
			i_rstn = 1'b0;
			#1733;
			repeat(3) @(posedge i_src_clk);
			i_rstn = 1'b1;
			repeat(4) @(posedge i_src_clk);
			repeat(4) @(posedge i_dst_clk);
			#1;
			common_resets = common_resets + 1;
			if(o_src_busy_500!==0 || o_src_copy_ack_500!==0 || o_src_error_500!==0 ||
			   o_dst_pending_valid_500!==0 || o_dst_copy_busy_500!==0 ||
			   o_dst_active_valid_500!==0 || o_dst_draw_valid_500!==0 || o_dst_update_500!==0)
				$fatal(1,"non-empty state after common reset");
			if(o_dst_age_upper_ms_500!==64'hFFFFFFFFFFFFFFFF ||
			   o_dst_age_upper_ms_2000!==64'hFFFFFFFFFFFFFFFF)
				$fatal(1,"no-active age telemetry was not unknown sentinel");
		end
	endtask

	task source_gap;
		input integer randomize;
		begin
			if(randomize) begin
				lfsr = {lfsr[30:0],lfsr[31]^lfsr[21]^lfsr[1]^lfsr[0]};
				repeat(lfsr[2:0]) @(negedge i_src_clk);
			end
		end
	endtask

	task send_entry;
		input [31:0] serial;
		input [31:0] item;
		input integer randomize;
		begin
			source_gap(randomize);
			@(negedge i_src_clk);
			i_src_entry = make_entry(serial,item);
			i_src_entry_valid = 1'b1;
			#1;
			wait_count = 0;
			while(!(o_src_entry_ready_500 && o_src_entry_ready_2000)) begin
				@(negedge i_src_clk); #1; wait_count = wait_count + 1;
				if(wait_count > 200) $fatal(1,"source entry handshake timeout item=%0d",item);
			end
			@(posedge i_src_clk);
			accepted_entries = accepted_entries + 1;
			@(negedge i_src_clk); i_src_entry_valid = 1'b0;
		end
	endtask

	task send_entry_value;
		input [96:0] value;
		input integer randomize;
		begin
			source_gap(randomize);
			@(negedge i_src_clk);
			i_src_entry = value;
			i_src_entry_valid = 1'b1;
			#1;
			wait_count = 0;
			while(!(o_src_entry_ready_500 && o_src_entry_ready_2000)) begin
				@(negedge i_src_clk); #1; wait_count = wait_count + 1;
				if(wait_count > 200) $fatal(1,"CPU entry handshake timeout");
			end
			@(posedge i_src_clk);
			accepted_entries = accepted_entries + 1;
			@(negedge i_src_clk); i_src_entry_valid = 1'b0;
		end
	endtask

	task seal_table;
		input [31:0] serial;
		input [6:0] count;
		input [264:0] metadata;
		input integer randomize;
		begin
			for(index=0; index<count; index=index+1)
				send_entry(serial,index,randomize);
			source_gap(randomize);
			@(negedge i_src_clk);
			i_src_metadata = metadata;
			i_src_meta_valid = 1'b1;
			#1;
			wait_count = 0;
			while(!(o_src_meta_ready_500 && o_src_meta_ready_2000)) begin
				@(negedge i_src_clk); #1; wait_count = wait_count + 1;
				if(wait_count > 200) $fatal(1,"source metadata handshake timeout count=%0d",count);
			end
			@(posedge i_src_clk);
			@(negedge i_src_clk); i_src_meta_valid = 1'b0;
			sealed_tables = sealed_tables + 1;
		end
	endtask

	task publish_cpu_case;
		input integer case_index;
		input [6:0] count;
		begin
			for(index=0;index<count;index=index+1)
				send_entry_value(cpu_entries[case_index*64+index],1);
			@(negedge i_src_clk);
			i_src_metadata=cpu_metadata[case_index];
			i_src_meta_valid=1;
			#1;
			wait_count=0;
			while(!(o_src_meta_ready_500 && o_src_meta_ready_2000)) begin
				@(negedge i_src_clk); #1; wait_count=wait_count+1;
				if(wait_count>200) $fatal(1,"CPU metadata handshake timeout count=%0d",count);
			end
			@(posedge i_src_clk);
			@(negedge i_src_clk); i_src_meta_valid=0;
			sealed_tables=sealed_tables+1;
			wait_copy_ack;
			sof_and_require_update;
			if(!o_dst_active_valid_500 || o_dst_metadata_500!==cpu_metadata[case_index])
				$fatal(1,"CPU complete table presence/metadata mismatch case=%0d",case_index);
			if(count==0 && o_dst_draw_valid_500)
				$fatal(1,"CPU count-zero diagnostic table became drawable");
			begin
				for(index=0;index<64;index=index+1) begin
					i_dst_read_index=index[5:0]; #1000;
					if(index<count) begin
						if(o_dst_entry_500!==cpu_entries[case_index*64+index])
							$fatal(1,"CPU entry mismatch case=%0d index=%0d",case_index,index);
					end else if(o_dst_entry_500!==97'd0)
						$fatal(1,"CPU out-of-count entry nonzero case=%0d index=%0d",case_index,index);
				end
			end
		end
	endtask

	task wait_copy_ack;
		begin
			wait_count = 0;
			while(!(o_src_copy_ack_500 && o_src_copy_ack_2000)) begin
				@(posedge i_src_clk); #1; wait_count = wait_count + 1;
				if(wait_count > 5000) $fatal(1,"copy acknowledgement timeout");
			end
			@(posedge i_src_clk);
		end
	endtask

	task sof_and_require_update;
		begin
			@(negedge i_dst_clk); i_dst_sof = 1'b1;
			@(posedge i_dst_clk); #1;
			if(!o_dst_update_500 || !o_dst_update_2000)
				$fatal(1,"complete pending table did not update on SOF");
			@(negedge i_dst_clk); i_dst_sof = 1'b0;
		end
	endtask

	task verify_active;
		input [31:0] serial;
		input [6:0] count;
		input [264:0] metadata;
		begin
			#1;
			if(!o_dst_active_valid_500 || !o_dst_active_valid_2000)
				$fatal(1,"complete publication did not make active table present count=%0d",count);
			if(o_dst_metadata_500 !== metadata || o_dst_metadata_2000 !== metadata)
				$fatal(1,"active metadata mismatch count=%0d",count);
			if(count==0 && (o_dst_draw_valid_500 || o_dst_draw_valid_2000))
				$fatal(1,"count-zero diagnostic table became drawable");
			for(index=0; index<64; index=index+1) begin
				i_dst_read_index = index[5:0];
				#1000;
				if(index < count) begin
					if(o_dst_entry_500 !== make_entry(serial,index) ||
					   o_dst_entry_2000 !== make_entry(serial,index))
						$fatal(1,"active entry mismatch index=%0d count=%0d",index,count);
				end else if(o_dst_entry_500 !== 97'd0 || o_dst_entry_2000 !== 97'd0) begin
					$fatal(1,"out-of-count read was not zero index=%0d count=%0d",index,count);
				end
			end
		end
	endtask

	task publish_and_activate;
		input [31:0] serial;
		input [6:0] count;
		input [264:0] metadata;
		input integer randomize;
		begin
			seal_table(serial,count,metadata,randomize);
			wait_copy_ack;
			if(!o_dst_pending_valid_500 || !o_dst_pending_valid_2000)
				$fatal(1,"copy acknowledgement without pending table");
			sof_and_require_update;
			verify_active(serial,count,metadata);
		end
	endtask

	task pulse_abort;
		begin
			@(negedge i_src_clk); i_src_abort=1'b1;
			@(negedge i_src_clk); i_src_abort=1'b0;
		end
	endtask

	task expect_draw;
		input expected500;
		input expected2000;
		input [63:0] expected_age;
		begin
			#1000;
			if(o_dst_draw_valid_500 !== expected500 || o_dst_draw_valid_2000 !== expected2000)
				$fatal(1,"draw decision mismatch expected=%b/%b actual=%b/%b age=%0d",
					expected500,expected2000,o_dst_draw_valid_500,o_dst_draw_valid_2000,o_dst_age_upper_ms_500);
			if(expected500 || expected2000) begin
				if(o_dst_age_upper_ms_500 !== expected_age || o_dst_age_upper_ms_2000 !== expected_age)
					$fatal(1,"age upper mismatch expected=%0d actual=%0d",expected_age,o_dst_age_upper_ms_500);
			end
		end
	endtask

	task run_counts_random;
		begin
			publish_cpu_case(0,0);
			publish_cpu_case(1,1);
			publish_cpu_case(2,32);
			publish_cpu_case(3,33);
			publish_cpu_case(4,64);
		end
	endtask

	task run_stall_pending_sof;
		reg [264:0] meta_a;
		reg [264:0] meta_b;
		reg [264:0] meta_c;
		begin
			table_serial=101;
			meta_a=make_metadata(1,2,101,EXPECTED_MODEL_ID,33,0,10,11);
			i_dst_copy_enable=0;
			seal_table(101,33,meta_a,0);
			wait(o_dst_copy_busy_500 && o_dst_copy_busy_2000);
			repeat(512) begin
				@(posedge i_dst_clk); #1;
				if(o_dst_pending_valid_500 || o_src_copy_ack_500)
					$fatal(1,"copy progressed through disabled destination gate");
			end
			i_dst_copy_enable=1;
			wait_copy_ack;
			if(!o_dst_pending_valid_500) $fatal(1,"stalled copy did not complete");

			table_serial=102;
			meta_b=make_metadata(1,2,102,EXPECTED_MODEL_ID,32,0,12,13);
			seal_table(102,32,meta_b,0);
			repeat(200) begin
				@(posedge i_dst_clk); #1;
				if(o_src_copy_ack_500) $fatal(1,"pending-full table was overwritten or acknowledged");
			end
			sof_and_require_update;
			verify_active(101,33,meta_a);
			wait_copy_ack;
			if(o_dst_metadata_500 !== meta_a)
				$fatal(1,"active metadata changed before next SOF");
			sof_and_require_update;
			verify_active(102,32,meta_b);

			table_serial=103;
			meta_c=make_metadata(1,2,103,EXPECTED_MODEL_ID,1,0,14,15);
			seal_table(103,1,meta_c,0);
			wait(o_dst_copy_busy_500);
			@(negedge i_dst_clk); i_dst_sof=1'b1;
			@(posedge i_dst_clk); #1;
			if(o_dst_update_500)
				$fatal(1,"last-copy/SOF bypassed pending into active table");
			@(negedge i_dst_clk); i_dst_sof=1'b0;
			wait_copy_ack;
			if(o_dst_metadata_500 !== meta_b)
				$fatal(1,"active table changed without a later SOF");
			sof_and_require_update;
			verify_active(103,1,meta_c);
		end
	endtask

	task run_reset_positions;
		begin
			for(pos=0;pos<64;pos=pos+1) begin
				reset_both;
				table_serial=200+pos;
				expected_meta=make_metadata(3,4,table_serial,EXPECTED_MODEL_ID,64,0,20,21);
				seal_table(table_serial,64,expected_meta,0);
				wait(o_dst_copy_busy_500 && o_dst_copy_busy_2000);
				for(index=0;index<pos;index=index+1) begin
					@(posedge i_dst_clk); #1;
					if(!o_dst_copy_busy_500)
						$fatal(1,"copy ended before reset position=%0d index=%0d",pos,index);
				end
				i_rstn=1'b0;
				#1733;
				if(o_src_copy_ack_500 || o_dst_pending_valid_500 || o_dst_active_valid_500)
					$fatal(1,"reset leaked table state at copy position=%0d",pos);
			end
			reset_both;
			table_serial=299;
			expected_meta=make_metadata(3,4,299,EXPECTED_MODEL_ID,1,0,30,31);
			publish_and_activate(299,1,expected_meta,0);
		end
	endtask

	task activate_meta;
		input [264:0] metadata;
		begin
			table_serial=table_serial+1;
			publish_and_activate(table_serial,1,metadata,0);
		end
	endtask

	task run_metadata_age;
		begin
			i_dst_time_epoch=32'hABCD0001;
			i_dst_time_valid=1;
			table_serial=300;
			activate_meta(make_metadata(32'hABCD0001,7,table_serial+1,EXPECTED_MODEL_ID,1,0,100,110));
			i_dst_now_ms=596; expect_draw(1,1,500);
			i_dst_now_ms=597; expect_draw(0,1,501);
			i_dst_now_ms=2096; expect_draw(0,1,2000);
			i_dst_now_ms=2097; expect_draw(0,0,2001);
			i_dst_time_valid=0; expect_draw(0,0,2001);
			if(o_dst_age_upper_ms_500!==64'hFFFFFFFFFFFFFFFF ||
			   o_dst_age_upper_ms_2000!==64'hFFFFFFFFFFFFFFFF)
				$fatal(1,"time-invalid age telemetry was not unknown sentinel");
			i_dst_time_valid=1;

			activate_meta(make_metadata(32'hABCD0000,7,table_serial+1,EXPECTED_MODEL_ID,1,0,100,110));
			i_dst_now_ms=120; expect_draw(0,0,24);
			if(o_dst_age_upper_ms_500!==64'hFFFFFFFFFFFFFFFF ||
			   o_dst_age_upper_ms_2000!==64'hFFFFFFFFFFFFFFFF)
				$fatal(1,"epoch-mismatch age telemetry was not unknown sentinel");
			activate_meta(make_metadata(32'hABCD0001,7,table_serial+1,32'hDEADBEEF,1,0,100,110));
			expect_draw(0,0,24);
			if(o_dst_age_upper_ms_500!==64'd24 || o_dst_age_upper_ms_2000!==64'd24)
				$fatal(1,"model-mismatch valid-time mathematical age mismatch");
			i_dst_time_epoch=32'h10203040;
			i_dst_now_ms=1496;
			publish_cpu_diagnostic(0);
			publish_cpu_diagnostic(1);
			publish_cpu_diagnostic(2);
			i_dst_time_epoch=32'hABCD0001;
			i_dst_now_ms=120;
			activate_meta(make_metadata(32'hABCD0001,7,table_serial+1,EXPECTED_MODEL_ID,1,0,111,110));
			expect_draw(0,0,13);
			if(o_dst_age_upper_ms_500!==64'hFFFFFFFFFFFFFFFF ||
			   o_dst_age_upper_ms_2000!==64'hFFFFFFFFFFFFFFFF)
				$fatal(1,"capture-after-completion age telemetry was not unknown sentinel");
			activate_meta(make_metadata(32'hABCD0001,7,table_serial+1,EXPECTED_MODEL_ID,1,0,100,121));
			expect_draw(0,0,24);
			if(o_dst_age_upper_ms_500!==64'hFFFFFFFFFFFFFFFF ||
			   o_dst_age_upper_ms_2000!==64'hFFFFFFFFFFFFFFFF)
				$fatal(1,"completion-after-now age telemetry was not unknown sentinel");
			activate_meta(make_metadata(32'hABCD0001,7,table_serial+1,EXPECTED_MODEL_ID,1,0,121,121));
			expect_draw(0,0,3);
			if(o_dst_age_upper_ms_500!==64'hFFFFFFFFFFFFFFFF ||
			   o_dst_age_upper_ms_2000!==64'hFFFFFFFFFFFFFFFF)
				$fatal(1,"future capture age telemetry was not unknown sentinel");

			activate_meta(make_metadata(32'hABCD0001,7,table_serial+1,EXPECTED_MODEL_ID,1,0,
				64'hFFFFFFFFFFFFFFFD,64'hFFFFFFFFFFFFFFFE));
			i_dst_now_ms=64'hFFFFFFFFFFFFFFFF; expect_draw(1,1,6);
			activate_meta(make_metadata(32'hABCD0001,7,table_serial+1,EXPECTED_MODEL_ID,1,0,0,1));
			i_dst_now_ms=64'hFFFFFFFFFFFFFFFF; expect_draw(0,0,3);
			if(o_dst_age_upper_ms_500!==64'hFFFFFFFFFFFFFFFF ||
			   o_dst_age_upper_ms_2000!==64'hFFFFFFFFFFFFFFFF)
				$fatal(1,"age telemetry did not saturate at UINT64_MAX");
		end
	endtask

	task run_abort_errors;
		integer errors_before;
		begin
			for(index=0;index<17;index=index+1)
				send_entry(400,index,1);
			pulse_abort;
			repeat(4) @(posedge i_src_clk);
			if(o_src_busy_500 || !o_src_entry_ready_500)
				$fatal(1,"partial-table abort did not return source to empty load state");
			if(source_error_pulses!=0)
				$fatal(1,"partial unsealed abort incorrectly raised an error");
			expected_meta=make_metadata(9,10,401,EXPECTED_MODEL_ID,1,0,40,41);
			seal_table(401,1,expected_meta,0);
			if(!o_src_busy_500)
				$fatal(1,"sealed source did not become busy");
			errors_before=source_error_pulses;
			pulse_abort;
			repeat(3) @(posedge i_src_clk);
			if(source_error_pulses!=errors_before+1)
				$fatal(1,"sealed abort error pulses=%0d expected=%0d",source_error_pulses,errors_before+1);
			wait_copy_ack;
			if(!o_dst_pending_valid_500)
				$fatal(1,"abort illegally cancelled sealed publication");
			sof_and_require_update;
			verify_active(401,1,expected_meta);

			// Hold valid continuously and change payload only between 64 adjacent accepts.
			table_serial=500;
			@(negedge i_src_clk);
			i_src_entry_valid=1;
			i_src_entry=make_entry(table_serial,0);
			#1;
			for(index=0;index<64;index=index+1) begin
				if(!(o_src_entry_ready_500 && o_src_entry_ready_2000))
					$fatal(1,"continuous source II=1 not ready index=%0d",index);
				@(posedge i_src_clk);
				accepted_entries=accepted_entries+1;
				burst_entries=burst_entries+1;
				if(index<63) begin
					@(negedge i_src_clk);
					i_src_entry=make_entry(table_serial,index+1);
					#1;
				end
			end
			@(negedge i_src_clk);
			i_src_entry_valid=0;
			expected_meta=make_metadata(9,10,500,EXPECTED_MODEL_ID,64,0,50,51);
			i_src_metadata=expected_meta;
			i_src_meta_valid=1;
			#1;
			if(!(o_src_meta_ready_500 && o_src_meta_ready_2000))
				$fatal(1,"continuous source table did not become seal-ready");
			@(posedge i_src_clk);
			@(negedge i_src_clk); i_src_meta_valid=0;
			sealed_tables=sealed_tables+1;
			wait_copy_ack;
			sof_and_require_update;
			verify_active(500,64,expected_meta);
		end
	endtask

	initial begin
		if(!$value$plusargs("CASE=%d",case_id)) case_id=10;
		if(case_id<10 || case_id>14) $fatal(1,"unsupported table case %0d",case_id);
		if(!$value$plusargs("TABLE_META=%s",metadata_vector_path) ||
		   !$value$plusargs("TABLE_ENTRIES=%s",entries_vector_path) ||
		   !$value$plusargs("DIAG_META=%s",diagnostic_metadata_path) ||
		   !$value$plusargs("DIAG_ENTRIES=%s",diagnostic_entries_path))
			$fatal(1,"CPU vector paths are required");
		$readmemh(metadata_vector_path,cpu_metadata);
		$readmemh(entries_vector_path,cpu_entries);
		$readmemh(diagnostic_metadata_path,cpu_diag_metadata);
		$readmemh(diagnostic_entries_path,cpu_diag_entries);
		reset_both;
		case(case_id)
			10: run_counts_random;
			11: run_stall_pending_sof;
			12: run_reset_positions;
			13: run_metadata_age;
			14: run_abort_errors;
		endcase
		$display("TB_PASS_TABLE case=%0d src_cycles=%0d dst_cycles=%0d tables=%0d entries=%0d acks=%0d updates=%0d max_wait=%0d resets=%0d src_errors=%0d burst_entries=%0d",
			case_id,src_cycles,dst_cycles,sealed_tables,accepted_entries,copy_acks,
			active_updates,max_copy_wait,common_resets,source_error_pulses,burst_entries);
		$finish;
	end

	initial begin
		#(64'd10000000000);
		$fatal(1,"detection table CDC timeout case=%0d",case_id);
	end
endmodule
