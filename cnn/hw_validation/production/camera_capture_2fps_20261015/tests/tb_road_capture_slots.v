`timescale 1ns/1ps

module tb_road_capture_slots;
	localparam [31:0] SLOT0_BASE = 32'h03400000;
	localparam [31:0] SLOT1_BASE = 32'h03480000;
	localparam [18:0] PAYLOAD_BYTES = 19'd442368;

	reg i_clk = 1'b0;
	reg i_rstn = 1'b0;
	reg i_sof = 1'b0;
	reg [31:0] i_epoch = 32'd0;
	reg [31:0] i_frame_id = 32'd0;
	reg [63:0] i_timestamp = 64'd0;
	reg i_capture_end = 1'b0;
	reg [18:0] i_capture_bytes = 19'd0;
	reg i_frame_error = 1'b0;
	reg i_write_visible = 1'b0;
	reg i_visible_slot = 1'b0;
	reg [31:0] i_visible_epoch = 32'd0;
	reg [31:0] i_visible_frame_id = 32'd0;
	reg i_read_claim_valid = 1'b0;
	reg i_read_claim_slot = 1'b0;
	reg [31:0] i_read_claim_epoch = 32'd0;
	reg [31:0] i_read_claim_frame_id = 32'd0;
	reg i_last_read_consumed = 1'b0;
	reg i_release_slot = 1'b0;
	reg [31:0] i_release_epoch = 32'd0;
	reg [31:0] i_release_frame_id = 32'd0;
	wire o_claim_ready;
	wire o_capture_active;
	wire o_capture_slot;
	wire [31:0] o_capture_base;
	wire o_capture_accepted;
	wire o_frame_skipped;
	wire [1:0] o_free_mask;
	wire [1:0] o_ready_mask;
	wire [1:0] o_reading_mask;
	wire [1:0] o_quarantine_mask;
	wire [63:0] o_slot_epochs;
	wire [63:0] o_slot_frame_ids;
	wire [127:0] o_slot_timestamps;
	wire o_protocol_error;

	integer case_id = 0;
	integer cycles = 0;
	integer protocol_errors = 0;
	integer skipped_frames = 0;

	road_capture_slots dut(
		.i_clk(i_clk), .i_rstn(i_rstn), .i_sof(i_sof), .i_epoch(i_epoch),
		.i_frame_id(i_frame_id), .i_timestamp(i_timestamp), .i_capture_end(i_capture_end),
		.i_capture_bytes(i_capture_bytes), .i_frame_error(i_frame_error),
		.i_write_visible(i_write_visible), .i_visible_slot(i_visible_slot),
		.i_visible_epoch(i_visible_epoch), .i_visible_frame_id(i_visible_frame_id),
		.i_read_claim_valid(i_read_claim_valid), .i_read_claim_slot(i_read_claim_slot),
		.i_read_claim_epoch(i_read_claim_epoch), .i_read_claim_frame_id(i_read_claim_frame_id),
		.i_last_read_consumed(i_last_read_consumed), .i_release_slot(i_release_slot),
		.i_release_epoch(i_release_epoch), .i_release_frame_id(i_release_frame_id),
		.o_claim_ready(o_claim_ready), .o_capture_active(o_capture_active),
		.o_capture_slot(o_capture_slot), .o_capture_base(o_capture_base),
		.o_capture_accepted(o_capture_accepted), .o_frame_skipped(o_frame_skipped),
		.o_free_mask(o_free_mask), .o_ready_mask(o_ready_mask),
		.o_reading_mask(o_reading_mask), .o_quarantine_mask(o_quarantine_mask),
		.o_slot_epochs(o_slot_epochs), .o_slot_frame_ids(o_slot_frame_ids),
		.o_slot_timestamps(o_slot_timestamps), .o_protocol_error(o_protocol_error)
	);

	always #5 i_clk = ~i_clk;

	always @(posedge i_clk) begin
		if(i_rstn) begin
			cycles = cycles + 1;
			if((o_free_mask & o_ready_mask) != 0 || (o_free_mask & o_reading_mask) != 0 ||
		   (o_free_mask & o_quarantine_mask) != 0 || (o_ready_mask & o_reading_mask) != 0 ||
		   (o_ready_mask & o_quarantine_mask) != 0 || (o_reading_mask & o_quarantine_mask) != 0)
				$fatal(1,"Slot state masks overlap");
			if(o_capture_active && (o_ready_mask[o_capture_slot] || o_reading_mask[o_capture_slot] ||
			   o_quarantine_mask[o_capture_slot] || o_free_mask[o_capture_slot]))
				$fatal(1,"Active capture slot has a conflicting state");
		end
	end

	always @(negedge i_clk) begin
		if(i_rstn) begin
			if(o_protocol_error) protocol_errors = protocol_errors + 1;
			if(o_frame_skipped) skipped_frames = skipped_frames + 1;
		end
	end

	task clear_inputs;
		begin
			i_sof=0; i_epoch=0; i_frame_id=0; i_timestamp=0;
			i_capture_end=0; i_capture_bytes=0; i_frame_error=0;
			i_write_visible=0; i_visible_slot=0; i_visible_epoch=0; i_visible_frame_id=0;
			i_read_claim_valid=0; i_read_claim_slot=0; i_read_claim_epoch=0; i_read_claim_frame_id=0;
			i_last_read_consumed=0; i_release_slot=0; i_release_epoch=0; i_release_frame_id=0;
		end
	endtask

	task reset_dut;
		begin
			@(negedge i_clk); clear_inputs; i_rstn=0;
			repeat(3) @(negedge i_clk);
			i_rstn=1;
			repeat(2) @(posedge i_clk);
			#1;
			if(o_free_mask!==2'b11 || o_ready_mask!==0 || o_reading_mask!==0 ||
			   o_quarantine_mask!==0 || o_capture_active!==0 || o_claim_ready!==0 ||
			   o_capture_accepted!==0 || o_frame_skipped!==0 || o_protocol_error!==0)
				$fatal(1,"Reset state mismatch free=%b ready=%b reading=%b quarantine=%b active=%b",
				       o_free_mask,o_ready_mask,o_reading_mask,o_quarantine_mask,o_capture_active);
		end
	endtask

	task pulse_sof;
		input [31:0] epoch;
		input [31:0] frame_id;
		input [63:0] timestamp;
		begin
			@(negedge i_clk); i_epoch=epoch; i_frame_id=frame_id; i_timestamp=timestamp; i_sof=1;
			@(negedge i_clk); i_sof=0;
			#1;
		end
	endtask

	task pulse_end;
		input [18:0] byte_count;
		input frame_error;
		begin
			@(negedge i_clk); i_capture_bytes=byte_count; i_frame_error=frame_error; i_capture_end=1;
			@(negedge i_clk); i_capture_end=0; i_frame_error=0;
			#1;
		end
	endtask

	task pulse_visible;
		input slot;
		input [31:0] epoch;
		input [31:0] frame_id;
		begin
			@(negedge i_clk); i_visible_slot=slot; i_visible_epoch=epoch; i_visible_frame_id=frame_id; i_write_visible=1;
			@(negedge i_clk); i_write_visible=0;
			#1;
		end
	endtask

	task pulse_end_visible;
		input slot;
		input [31:0] epoch;
		input [31:0] frame_id;
		begin
			@(negedge i_clk);
			i_capture_bytes=PAYLOAD_BYTES; i_capture_end=1;
			i_visible_slot=slot; i_visible_epoch=epoch; i_visible_frame_id=frame_id; i_write_visible=1;
			@(negedge i_clk); i_capture_end=0; i_write_visible=0;
			#1;
		end
	endtask

	task claim_slot;
		input slot;
		input [31:0] epoch;
		input [31:0] frame_id;
		input expect_ready;
		begin
			@(negedge i_clk);
			i_read_claim_slot=slot; i_read_claim_epoch=epoch; i_read_claim_frame_id=frame_id;
			i_read_claim_valid=1;
			#1;
			if(o_claim_ready!==expect_ready) $fatal(1,"Claim ready mismatch slot=%0d got=%b expected=%b",slot,o_claim_ready,expect_ready);
			@(negedge i_clk); i_read_claim_valid=0;
			#1;
		end
	endtask

	task release_slot;
		input slot;
		input [31:0] epoch;
		input [31:0] frame_id;
		begin
			@(negedge i_clk);
			i_release_slot=slot; i_release_epoch=epoch; i_release_frame_id=frame_id; i_last_read_consumed=1;
			@(negedge i_clk); i_last_read_consumed=0;
			#1;
		end
	endtask

	task expect_masks;
		input [1:0] free_mask;
		input [1:0] ready_mask;
		input [1:0] reading_mask;
		input [1:0] quarantine_mask;
		begin
			#1;
			if(o_free_mask!==free_mask || o_ready_mask!==ready_mask ||
			   o_reading_mask!==reading_mask || o_quarantine_mask!==quarantine_mask)
				$fatal(1,"Mask mismatch free=%b/%b ready=%b/%b reading=%b/%b quarantine=%b/%b",
				       o_free_mask,free_mask,o_ready_mask,ready_mask,o_reading_mask,reading_mask,
				       o_quarantine_mask,quarantine_mask);
		end
	endtask

	task expect_slot0_identity;
		input [31:0] epoch;
		input [31:0] frame_id;
		input [63:0] timestamp;
		begin
			if(o_slot_epochs[31:0]!==epoch || o_slot_frame_ids[31:0]!==frame_id ||
			   o_slot_timestamps[63:0]!==timestamp)
				$fatal(1,"Slot0 identity mismatch");
		end
	endtask

	task expect_slot1_identity;
		input [31:0] epoch;
		input [31:0] frame_id;
		input [63:0] timestamp;
		begin
			if(o_slot_epochs[63:32]!==epoch || o_slot_frame_ids[63:32]!==frame_id ||
			   o_slot_timestamps[127:64]!==timestamp)
				$fatal(1,"Slot1 identity mismatch");
		end
	endtask

	task case_lifecycle;
		begin
			reset_dut;
			pulse_sof(32'd11,32'd101,64'd1001);
			if(!o_capture_active || o_capture_slot!==0 || o_capture_base!==SLOT0_BASE) $fatal(1,"Slot0 allocation mismatch");
			expect_slot0_identity(32'd11,32'd101,64'd1001);
			pulse_end(PAYLOAD_BYTES,1'b0);
			expect_masks(2'b10,2'b00,2'b00,2'b00);
			pulse_visible(0,32'd11,32'd101);
			expect_masks(2'b10,2'b01,2'b00,2'b00);
			pulse_sof(32'd12,32'd102,64'd1002);
			if(!o_capture_active || o_capture_slot!==1 || o_capture_base!==SLOT1_BASE) $fatal(1,"Slot1 allocation mismatch");
			expect_slot1_identity(32'd12,32'd102,64'd1002);
			pulse_end_visible(1,32'd12,32'd102);
			expect_masks(2'b00,2'b11,2'b00,2'b00);
			claim_slot(1,32'd12,32'd102,1'b1);
			expect_masks(2'b00,2'b01,2'b10,2'b00);
			release_slot(1,32'd12,32'd102);
			expect_masks(2'b10,2'b01,2'b00,2'b00);
			claim_slot(0,32'd11,32'd101,1'b1);
			expect_masks(2'b10,2'b00,2'b01,2'b00);
			release_slot(0,32'd11,32'd101);
			expect_masks(2'b11,2'b00,2'b00,2'b00);
		end
	endtask

	task case_protection;
		integer skipped_before;
		begin
			reset_dut;
			pulse_sof(32'd21,32'd201,64'd2001);
			pulse_end_visible(0,32'd21,32'd201);
			pulse_sof(32'd22,32'd202,64'd2002);
			skipped_before=skipped_frames;
			pulse_sof(32'd23,32'd203,64'd2003);
			if(skipped_frames!=skipped_before+1 || o_capture_active) $fatal(1,"Reentrant SOF did not skip/quarantine");
			expect_masks(2'b00,2'b01,2'b00,2'b10);
			claim_slot(0,32'd21,32'd201,1'b1);
			expect_masks(2'b00,2'b00,2'b01,2'b10);
			skipped_before=skipped_frames;
			pulse_sof(32'd24,32'd204,64'd2004);
			if(skipped_frames!=skipped_before+1) $fatal(1,"No-free SOF was not skipped");
			expect_masks(2'b00,2'b00,2'b01,2'b10);
			@(negedge i_clk);
			i_sof=1; i_epoch=32'd25; i_frame_id=32'd205; i_timestamp=64'd2005;
			i_last_read_consumed=1; i_release_slot=0; i_release_epoch=32'd21; i_release_frame_id=32'd201;
			@(negedge i_clk); i_sof=0; i_last_read_consumed=0;
			#1;
			if(o_capture_active) $fatal(1,"Same-edge release illegally bypassed pre-edge FREE allocation");
			expect_masks(2'b01,2'b00,2'b00,2'b10);
			pulse_sof(32'd26,32'd206,64'd2006);
			if(!o_capture_active || o_capture_slot!==0) $fatal(1,"Freed slot0 was not allocatable on next SOF");
			reset_dut;
			pulse_sof(32'd27,32'd207,64'd2007);
			pulse_end_visible(0,32'd27,32'd207);
			claim_slot(0,32'd27,32'd207,1'b1);
			pulse_sof(32'd28,32'd208,64'd2008);
			if(!o_capture_active || o_capture_slot!==1) $fatal(1,"Concurrent-event setup did not capture slot1");
			skipped_before=skipped_frames;
			@(negedge i_clk);
			i_sof=1; i_epoch=32'd29; i_frame_id=32'd209; i_timestamp=64'd2009;
			i_last_read_consumed=1; i_release_slot=0; i_release_epoch=32'd27; i_release_frame_id=32'd207;
			@(negedge i_clk); i_sof=0; i_last_read_consumed=0;
			#1;
			if(skipped_frames!=skipped_before+1 || o_capture_active)
				$fatal(1,"SOF did not interrupt capture while concurrent release completed");
			expect_masks(2'b01,2'b00,2'b00,2'b10);
		end
	endtask

	task case_protocol;
		integer errors_before;
		begin
			reset_dut;
			errors_before=protocol_errors;
			pulse_visible(0,32'd31,32'd301);
			if(protocol_errors<=errors_before) $fatal(1,"Early visible did not flag protocol error");
			expect_masks(2'b11,0,0,0);
			pulse_sof(32'd31,32'd301,64'd3001);
			pulse_visible(0,32'd30,32'd300);
			expect_masks(2'b10,0,0,0);
			pulse_end(PAYLOAD_BYTES,0);
			pulse_visible(0,32'd31,32'd999);
			expect_masks(2'b10,0,0,0);
			pulse_visible(0,32'd31,32'd301);
			expect_masks(2'b10,2'b01,0,0);
			pulse_visible(0,32'd31,32'd301);
			expect_masks(2'b10,2'b01,0,0);
			claim_slot(0,32'd31,32'd999,1'b0);
			expect_masks(2'b10,2'b01,0,0);
			claim_slot(0,32'd31,32'd301,1'b1);
			expect_masks(2'b10,0,2'b01,0);
			release_slot(0,32'd31,32'd999);
			expect_masks(2'b10,0,2'b01,0);
			release_slot(0,32'd31,32'd301);
			expect_masks(2'b11,0,0,0);
			release_slot(0,32'd31,32'd301);
			expect_masks(2'b11,0,0,0);
			if(protocol_errors<errors_before+6) $fatal(1,"Protocol error coverage too small: %0d",protocol_errors-errors_before);
		end
	endtask

	task case_malformed_reset;
		integer skipped_before;
		begin
			reset_dut;
			pulse_sof(32'd41,32'd401,64'd4001);
			pulse_end(PAYLOAD_BYTES-1'b1,0);
			expect_masks(2'b10,0,0,2'b01);
			pulse_sof(32'd42,32'd402,64'd4002);
			pulse_end(PAYLOAD_BYTES+1'b1,0);
			expect_masks(0,0,0,2'b11);
			skipped_before=skipped_frames;
			pulse_sof(32'd43,32'd403,64'd4003);
			if(skipped_frames!=skipped_before+1) $fatal(1,"No-free malformed slots did not skip SOF");
			reset_dut;
			pulse_sof(32'd44,32'd404,64'd4004);
			@(negedge i_clk); i_frame_error=1;
			@(negedge i_clk); i_frame_error=0;
			#1;
			expect_masks(2'b10,0,0,2'b01);
			reset_dut;
			pulse_sof(32'd45,32'd405,64'd4005);
			reset_dut;
			expect_masks(2'b11,0,0,0);
			pulse_end(PAYLOAD_BYTES,0);
			expect_masks(2'b11,0,0,0);
		end
	endtask

	initial begin
		if(!$value$plusargs("CASE=%d",case_id)) case_id=0;
		clear_inputs;
		case(case_id)
			0: case_lifecycle;
			1: case_protection;
			2: case_protocol;
			3: case_malformed_reset;
			default: $fatal(1,"Slot CASE must be 0..3");
		endcase
		$display("TB_PASS_CAPTURE_SLOTS case=%0d cycles=%0d protocol_errors=%0d skipped=%0d",case_id,cycles,protocol_errors,skipped_frames);
		$finish;
	end
endmodule
