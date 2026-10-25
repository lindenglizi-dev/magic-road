`timescale 1ns/1ps

module tb_road_area_resize;
	localparam integer SOURCE_ROWS = 720;
	localparam integer BEATS_PER_ROW = 320;
	localparam integer INPUT_WORDS = 230400;
	localparam integer OUTPUT_ROWS = 288;
	localparam integer OUTPUT_COLUMNS = 512;
	localparam integer OUTPUT_PIXELS = 147456;
	localparam integer OUTPUT_BYTES = 442368;

	reg i_clk = 1'b0;
	reg i_rstn = 1'b0;
	reg [95:0] i_rgb = 96'd0;
	reg i_valid = 1'b0;
	reg i_sof = 1'b0;
	reg i_eol = 1'b0;
	wire [47:0] o_pixels;
	wire [1:0] o_pixel_mask;
	wire o_sof;
	wire o_eol;
	wire o_eof;
	wire o_frame_error;
	wire o_busy;

	reg [95:0] input_words [0:INPUT_WORDS-1];
	reg [47:0] expected_words [0:OUTPUT_PIXELS-1];
	reg checking_outputs = 1'b0;
	reg frame_done = 1'b0;
	reg saw_busy = 1'b0;
	integer case_id = 0;
	integer cycles = 0;
	integer first_input_cycle = -1;
	integer first_output_offset = -1;
	integer last_output_offset = -1;
	integer expected_index = 0;
	integer output_beats = 0;
	integer output_bytes = 0;
	integer frame_errors = 0;
	integer first_error_offset = -1;
	integer lane_count = 0;
	integer beat_end_index = 0;
	integer wait_cycles = 0;
	reg [8*1024-1:0] input_path;
	reg [8*1024-1:0] expected_path;

	road_area_resize dut(
		.i_clk(i_clk), .i_rstn(i_rstn), .i_rgb(i_rgb), .i_valid(i_valid),
		.i_sof(i_sof), .i_eol(i_eol), .o_pixels(o_pixels),
		.o_pixel_mask(o_pixel_mask), .o_sof(o_sof), .o_eol(o_eol),
		.o_eof(o_eof), .o_frame_error(o_frame_error), .o_busy(o_busy)
	);

	always #5 i_clk = ~i_clk;

	always @(posedge i_clk) begin
		if(i_rstn) begin
			cycles = cycles + 1;
			if(i_valid && first_input_cycle<0) first_input_cycle=cycles;
			if(o_busy) saw_busy=1'b1;
			if(o_frame_error) begin
				frame_errors=frame_errors+1;
				if(first_error_offset<0 && first_input_cycle>=0) first_error_offset=cycles-first_input_cycle;
			end
			if(o_pixel_mask!==2'b00 && o_pixel_mask!==2'b01 && o_pixel_mask!==2'b11)
				$fatal(1,"Illegal or unknown output mask %b",o_pixel_mask);
			if(o_pixel_mask===2'b00 && {o_sof,o_eol,o_eof}!==3'b000)
				$fatal(1,"Output boundary flag without a pixel flags=%b%b%b",o_sof,o_eol,o_eof);
			if(o_pixel_mask!==2'b00) begin
				if(!checking_outputs) $fatal(1,"Output escaped an aborted/reset frame mask=%b",o_pixel_mask);
				lane_count=(o_pixel_mask==2'b11) ? 2 : 1;
				if(expected_index+lane_count>OUTPUT_PIXELS) $fatal(1,"Too many output pixels index=%0d lanes=%0d",expected_index,lane_count);
				if(o_pixels[23:0]!==expected_words[expected_index][23:0])
					$fatal(1,"Pixel mismatch index=%0d actual=%h expected=%h",expected_index,o_pixels[23:0],expected_words[expected_index][23:0]);
				if(expected_words[expected_index][47:24]!==0) $fatal(1,"Reference upper lane is not serial-zero");
				if(lane_count==2) begin
					if((expected_index%OUTPUT_COLUMNS)==OUTPUT_COLUMNS-1) $fatal(1,"Two-lane beat crosses an output row");
					if(o_pixels[47:24]!==expected_words[expected_index+1][23:0])
						$fatal(1,"Pixel lane1 mismatch index=%0d actual=%h expected=%h",expected_index+1,o_pixels[47:24],expected_words[expected_index+1][23:0]);
				end
				beat_end_index=expected_index+lane_count-1;
				if(o_sof!==((expected_index==0) ? 1'b1 : 1'b0))
					$fatal(1,"Output SOF position mismatch index=%0d sof=%b",expected_index,o_sof);
				if(o_eol!==(((beat_end_index%OUTPUT_COLUMNS)==OUTPUT_COLUMNS-1) ? 1'b1 : 1'b0))
					$fatal(1,"Output EOL position mismatch index=%0d eol=%b",beat_end_index,o_eol);
				if(o_eof!==((beat_end_index==OUTPUT_PIXELS-1) ? 1'b1 : 1'b0))
					$fatal(1,"Output EOF position mismatch index=%0d eof=%b",beat_end_index,o_eof);
				if(first_output_offset<0) first_output_offset=cycles-first_input_cycle;
				last_output_offset=cycles-first_input_cycle;
				expected_index=expected_index+lane_count;
				output_beats=output_beats+1;
				output_bytes=output_bytes+3*lane_count;
				if(o_eof) frame_done=1'b1;
			end
		end
	end

	task clear_driver;
		begin
			i_rgb=0; i_valid=0; i_sof=0; i_eol=0;
		end
	endtask

	task reset_dut;
		begin
			@(negedge i_clk); clear_driver; i_rstn=0; checking_outputs=0;
			repeat(4) @(negedge i_clk);
			#1;
			if(o_pixel_mask!==0 || o_sof!==0 || o_eol!==0 || o_eof!==0 || o_frame_error!==0 || o_busy!==0)
				$fatal(1,"Reset output leakage mask=%b flags=%b%b%b error=%b busy=%b",o_pixel_mask,o_sof,o_eol,o_eof,o_frame_error,o_busy);
			i_rstn=1;
			repeat(2) @(posedge i_clk);
		end
	endtask

	task pulse_sof;
		begin
			@(negedge i_clk); i_sof=1; i_valid=0; i_eol=0;
			@(negedge i_clk); i_sof=0;
		end
	endtask

	task clear_result_counters;
		begin
			first_input_cycle=-1; first_output_offset=-1; last_output_offset=-1;
			expected_index=0; output_beats=0; output_bytes=0; frame_done=0; saw_busy=0;
		end
	endtask

	task drive_full_frame;
		input integer blank_cycles;
		integer row;
		integer beat;
		integer input_index;
		begin
			clear_result_counters;
			checking_outputs=1;
			pulse_sof;
			input_index=0;
			for(row=0;row<SOURCE_ROWS;row=row+1) begin
				for(beat=0;beat<BEATS_PER_ROW;beat=beat+1) begin
					@(negedge i_clk);
					i_rgb=input_words[input_index]; i_valid=1; i_eol=(beat==BEATS_PER_ROW-1);
					input_index=input_index+1;
				end
				@(negedge i_clk); i_valid=0; i_eol=0; i_rgb=0;
				repeat(blank_cycles-1) @(negedge i_clk);
			end
			if(input_index!=INPUT_WORDS) $fatal(1,"Input word coverage mismatch %0d",input_index);
			wait_cycles=0;
			while(!frame_done && wait_cycles<20000) begin @(posedge i_clk); wait_cycles=wait_cycles+1; end
			if(!frame_done) $fatal(1,"Timed out waiting for output EOF index=%0d",expected_index);
			if(expected_index!=OUTPUT_PIXELS || output_bytes!=OUTPUT_BYTES)
				$fatal(1,"Output conservation pixels=%0d bytes=%0d",expected_index,output_bytes);
			if(!saw_busy) $fatal(1,"Busy never asserted for a full frame");
			@(posedge i_clk); #1;
			if(o_pixel_mask!==0 || o_eof!==0) $fatal(1,"Output repeated after EOF");
			checking_outputs=0;
		end
	endtask

	task drive_partial_line;
		input integer beats;
		input last_has_eol;
		integer beat;
		begin
			for(beat=0;beat<beats;beat=beat+1) begin
				@(negedge i_clk); i_rgb=input_words[beat]; i_valid=1; i_eol=(last_has_eol && beat==beats-1);
			end
			@(negedge i_clk); i_valid=0; i_eol=0; i_rgb=0;
		end
	endtask

	task wait_for_new_error;
		input integer previous_errors;
		integer timeout;
		begin
			timeout=0;
			while(frame_errors==previous_errors && timeout<64) begin @(posedge i_clk); timeout=timeout+1; end
			if(frame_errors==previous_errors) $fatal(1,"Expected frame error did not arrive");
		end
	endtask

	task case_fault_recovery;
		integer before;
		begin
			reset_dut;
			before=frame_errors; pulse_sof; drive_partial_line(10,1'b1); wait_for_new_error(before);
			repeat(16) @(posedge i_clk);
			reset_dut;
			before=frame_errors; pulse_sof; drive_partial_line(321,1'b1); wait_for_new_error(before);
			reset_dut;
			before=frame_errors; pulse_sof; drive_partial_line(100,1'b0); pulse_sof; wait_for_new_error(before);
			reset_dut;
			pulse_sof; drive_partial_line(100,1'b0);
			@(negedge i_clk); i_rstn=0;
			repeat(4) @(negedge i_clk);
			#1;
			if(o_pixel_mask!==0 || o_frame_error!==0 || o_busy!==0) $fatal(1,"Mid-frame reset leaked state");
			i_rstn=1; repeat(2) @(posedge i_clk);
			drive_full_frame(480);
		end
	endtask

	task case_overload;
		integer row;
		integer beat;
		integer input_index;
		integer before;
		begin
			reset_dut;
			clear_result_counters;
			checking_outputs=0;
			before=frame_errors;
			pulse_sof;
			input_index=0;
			row=0;
			while(row<SOURCE_ROWS && frame_errors==before) begin
				beat=0;
				while(beat<BEATS_PER_ROW && frame_errors==before) begin
					@(negedge i_clk); i_rgb=input_words[input_index]; i_valid=1; i_eol=(beat==BEATS_PER_ROW-1);
					input_index=input_index+1; beat=beat+1;
				end
				row=row+1;
			end
			@(negedge i_clk); i_valid=0; i_eol=0; i_rgb=0;
			wait_for_new_error(before);
			repeat(32) @(posedge i_clk);
			if(o_eof) $fatal(1,"Overloaded frame emitted EOF");
		end
	endtask

	initial begin
		if(!$value$plusargs("CASE=%d",case_id)) case_id=0;
		if(!$value$plusargs("INPUT=%s",input_path)) $fatal(1,"Missing INPUT vector path");
		if(!$value$plusargs("EXPECTED=%s",expected_path)) $fatal(1,"Missing EXPECTED vector path");
		$readmemh(input_path,input_words);
		$readmemh(expected_path,expected_words);
		clear_driver;
		case(case_id)
			0,1,2: begin reset_dut; drive_full_frame(480); if(frame_errors!=0) $fatal(1,"Normal frame raised error"); end
			3: case_fault_recovery;
			4: case_overload;
			default: $fatal(1,"Scaler CASE must be 0..4");
		endcase
		$display("TB_PASS_AREA_RESIZE case=%0d cycles=%0d output_pixels=%0d output_beats=%0d output_bytes=%0d first_output=%0d last_output=%0d frame_errors=%0d first_error=%0d",
		         case_id,cycles,expected_index,output_beats,output_bytes,first_output_offset,last_output_offset,frame_errors,first_error_offset);
		$finish;
	end
endmodule
