`timescale 1ns / 1ps
`include "vector_count.vh"
module tb_road_dynamic_requant;
	reg clk = 0;
	reg rstn = 0;
	reg input_valid = 0;
	reg output_ready = 0;
	reg signed [31:0]accumulator;
	reg [30:0]multiplier;
	reg [5:0]shift;
	reg [15:0]tag;
	wire input_ready;
	wire output_valid;
	wire signed [15:0]output_data;
	wire [15:0]output_tag;
	wire fault;
	reg [111:0]vectors [0:`VECTOR_COUNT-1];
	integer sent = 0;
	integer received = 0;
	integer cycles = 0;
	integer phase;
	integer reset_done;
	integer seed = 42;
	integer random_value;
	integer stalled = 0;
	reg held = 0;
	reg input_accepted = 0;
	reg [32:0]held_payload;
	always #5 clk = !clk;
	road_dynamic_requant dut(
		.i_clk(clk), .i_rstn(rstn), .i_input_valid(input_valid),
		.i_accumulator(accumulator), .i_multiplier(multiplier),
		.i_shift(shift), .i_tag(tag), .o_input_ready(input_ready),
		.i_output_ready(output_ready), .o_output_valid(output_valid),
		.o_output_data(output_data), .o_output_tag(output_tag), .o_fault(fault)
	);
	always @(posedge clk) begin
		if (!rstn) begin
			received = sent;
			held = 0;
			input_accepted = 0;
		end else begin
			input_accepted = input_valid && input_ready;
			if (held && {output_tag, output_data, fault} !== held_payload) begin
				$fatal(1, "held output changed");
			end
			if (output_valid && output_ready) begin
				if (received >= sent || output_tag !== vectors[received][39:24] ||
					output_data !== vectors[received][23:8] || fault !== vectors[received][0]) begin
					$fatal(1, "mismatch phase=%0d index=%0d tag=%h data=%h fault=%b expected=%h", phase, received, output_tag, output_data, fault, vectors[received]);
				end
				received = received + 1;
			end
			if (input_valid && input_ready) begin
				sent = sent + 1;
			end
			held = output_valid && !output_ready;
			held_payload = {output_tag, output_data, fault};
			if (held) stalled = stalled + 1;
		end
	end
	initial begin
		$readmemh("vectors.hex", vectors);
		for (phase = 0; phase < 3; phase = phase + 1) begin
			@(negedge clk); rstn = 0; input_valid = 0; sent = 0; received = 0;
			cycles = 0; reset_done = 0;
			repeat (3) @(negedge clk);
			rstn = 1;
			while (received < `VECTOR_COUNT) begin
				@(negedge clk);
				cycles = cycles + 1;
				if (cycles > 20000) $fatal(1, "timeout");
				if (phase == 2 && sent >= 30 && !reset_done) begin
					rstn = 0; input_valid = 0;
					repeat (3) @(negedge clk);
					rstn = 1; reset_done = 1;
				end
				random_value = $random(seed) & 32'h7fffffff;
				output_ready = phase == 0 || ((random_value % 5 != 0) && !(cycles >= 150 && cycles < 350));
				if (!input_valid || input_accepted) begin
					input_valid = sent < `VECTOR_COUNT && (phase == 0 || random_value % 3 != 0);
					if (sent < `VECTOR_COUNT) begin
						accumulator = vectors[sent][111:80]; multiplier = vectors[sent][78:48];
						shift = vectors[sent][45:40]; tag = vectors[sent][39:24];
					end
				end
			end
			@(negedge clk); input_valid = 0; output_ready = 1;
			repeat (20) @(negedge clk);
			$display("PHASE_PASS phase=%0d sent=%0d accounted=%0d cycles=%0d", phase, sent, received, cycles);
		end
		$display("TB_PASS_DYNAMIC_REQUANT vectors=%0d phases=3 stalled=%0d", `VECTOR_COUNT, stalled);
		$finish;
	end
endmodule
