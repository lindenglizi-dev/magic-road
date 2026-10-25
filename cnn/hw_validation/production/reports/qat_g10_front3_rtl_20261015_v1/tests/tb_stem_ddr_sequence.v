`timescale 1ns / 1ps

// Independent 100 MHz regression for sixteen Stem tiles and four down2 tiles.
module tb_stem_ddr_sequence;
	localparam [26:0] C_TB_TIMEOUT = 27'd20000;
	localparam integer ST_RUN = 6;
	localparam integer ST_STEM_BYTE = 8;
	localparam integer ST_WRITE = 10;
	localparam integer ST_WRITE_RESPONSE = 11;
	localparam integer ST_READ_RESPONSE = 17;
	localparam integer ST_HALO_BYTE = 19;
	localparam integer ST_OUTPUT_BYTE = 21;

	reg clk = 1'b0;
	reg rstn = 1'b0;
	reg phy_ready = 1'b0;
	reg ddr_fault = 1'b0;
	reg req_ready = 1'b0;
	reg rsp_valid = 1'b0;
	reg [127:0]rsp_data = 128'd0;
	reg [3:0]rsp_error = 4'd0;
	wire req_valid;
	wire req_write;
	wire [24:0]req_addr;
	wire [127:0]req_data;
	wire rsp_ready;
	wire [1:0]status;
	wire [3:0]error_code;
	wire [4:0]phase;
	wire [8:0]writes;
	wire [8:0]reads;
	wire [10:0]output_bytes;
	wire [31:0]cycles;
	wire [319:0]cycle_bins;
	wire [24:0]address_debug;
	wire [127:0]expected_debug;
	wire [127:0]actual_debug;

	reg [127:0]stem_golden [0:255];
	reg [31:0]stem_addresses [0:255];
	reg [15:0]halo_map [0:511];
	reg [15:0]read_indices [0:288];
	reg [7:0]pw_golden [0:2047];
	reg [31:0]stem_acc [0:4095];
	reg [15:0]stem_pre [0:4095];
	reg [15:0]stem_silu [0:4095];
	reg [7:0]stem_post [0:4095];
	reg [31:0]dw_acc [0:1023];
	reg [15:0]dw_pre [0:1023];
	reg [15:0]dw_silu [0:1023];
	reg [7:0]dw_post [0:1023];
	reg [31:0]pw_acc [0:1535];
	reg [15:0]pw_pre [0:1535];
	reg [15:0]pw_silu [0:1535];
	reg [7:0]pw_post [0:1535];

	reg [127:0]endpoint_mem [0:255];
	reg write_seen [0:255];
	integer read_hits [0:255];
	integer expected_read_hits [0:255];
	reg output_seen [0:1535];
	reg stem_acc_seen [0:4095];
	reg stem_pre_seen [0:4095];
	reg stem_silu_seen [0:4095];
	reg stem_post_seen [0:4095];
	reg dw_acc_seen [0:1023];
	reg dw_pre_seen [0:1023];
	reg dw_silu_seen [0:1023];
	reg dw_post_seen [0:1023];
	reg pw_acc_seen [0:1535];
	reg pw_pre_seen [0:1535];
	reg pw_silu_seen [0:1535];
	reg pw_post_seen [0:1535];

	reg pending = 1'b0;
	reg pending_write = 1'b0;
	reg pending_drop = 1'b0;
	integer pending_slot = 0;
	integer response_delay = 0;
	integer long_wait = 0;
	reg [15:0]random_bits = 16'hace1;
	reg held_request = 1'b0;
	reg [153:0]held_request_payload = 154'd0;
	reg reset_done = 1'b0;
	reg started = 1'b0;
	reg reset_target_seen = 1'b0;
	reg [4095:0]vector_dir;
	reg [4095:0]path;

	integer case_id = 0;
	integer ticks = 0;
	integer i;
	integer j;
	integer slot;
	integer map_index;
	integer lane;
	integer family;
	integer value_index;
	integer write_requests;
	integer write_responses;
	integer read_requests;
	integer read_responses;
	integer stem_exports;
	integer halo_bytes;
	integer padding_pixels;
	integer final_exports;
	integer high_read_requests;
	integer duplicate_read_requests;
	integer reads_by_tile [0:3];
	integer padding_by_tile [0:3];
	integer accumulator_checks;
	integer pre_checks;
	integer silu_checks;
	integer post_checks;
	integer stem_acc_checks;
	integer stem_pre_checks;
	integer stem_silu_checks;
	integer stem_post_checks;
	integer dw_acc_checks;
	integer dw_pre_checks;
	integer dw_silu_checks;
	integer dw_post_checks;
	integer pw_acc_checks;
	integer pw_pre_checks;
	integer pw_silu_checks;
	integer pw_post_checks;
	integer table_entries_total = 0;
	integer generation = 0;
	integer sum_bins;
	reg [15:0]stem_export_starts;
	reg [3:0]pw_export_starts;

	always #5 clk = !clk;

	road_stem_ddr_sequence #(.C_TIMEOUT(C_TB_TIMEOUT)) dut(
		.i_clk(clk),.i_rstn(rstn),.i_phy_ready(phy_ready),.i_ddr_fault(ddr_fault),
		.i_req_ready(req_ready),.i_rsp_valid(rsp_valid),.i_rsp_data(rsp_data),
		.i_rsp_error(rsp_error),.o_req_valid(req_valid),.o_req_write(req_write),
		.o_req_addr(req_addr),.o_req_data(req_data),.o_rsp_ready(rsp_ready),
		.o_status(status),.o_error(error_code),.o_phase(phase),.o_writes(writes),
		.o_reads(reads),.o_output_bytes(output_bytes),.o_cycles(cycles),
		.o_cycle_bins(cycle_bins),.o_address(address_debug),
		.o_expected(expected_debug),.o_actual(actual_debug)
	);

	function integer find_slot;
		input [24:0]candidate;
		integer search;
		begin
			find_slot = -1;
			for(search=0;search<256;search=search+1)
				if(candidate === stem_addresses[search][24:0]) find_slot = search;
		end
	endfunction

	// Decode the scheduler tag into the corresponding tile-ordered reference item.
	task decode_external_tag;
		input [15:0]external_tag;
		output integer resolved_family;
		output integer resolved_index;
		integer tile_number;
		integer position;
		integer channel;
		begin
			if(!dut.u_core.flag_owner_down2) begin
				if(external_tag[15:8] !== 8'd0) $fatal(1,"Invalid Stem tag %h",external_tag);
				tile_number = write_requests/16;
				position = external_tag[7:4];
				channel = external_tag[3:0];
				resolved_family = 0;
				resolved_index = tile_number*256 + position*16 + channel;
				if(tile_number>=16 || resolved_index>=4096) $fatal(1,"Stem tag range");
			end else begin
				tile_number = final_exports/384;
				position = external_tag[14:11];
				channel = external_tag[10:6];
				resolved_family = external_tag[15] ? 2 : 1;
				resolved_index = tile_number*(external_tag[15] ? 384 : 256) +
				                 position*(external_tag[15] ? 24 : 16) + channel;
				if(external_tag[5:0] !== 6'd0 || tile_number>=4 || position>=16 ||
				   (resolved_family==1 && (channel>=16 || resolved_index>=1024)) ||
				   (resolved_family==2 && (channel>=24 || resolved_index>=1536)))
					$fatal(1,"Down2 tag range tag=%h family=%0d index=%0d",external_tag,resolved_family,resolved_index);
			end
		end
	endtask

	task resolve_internal_tag;
		input [15:0]internal_tag;
		output integer resolved_family;
		output integer resolved_index;
		reg [47:0]tags;
		reg [15:0]external_tag;
		begin
			if(internal_tag[15:5] !== 11'd0 || internal_tag[1:0] > 2)
				$fatal(1,"Invalid internal postprocess tag %h",internal_tag);
			tags = dut.u_core.u_pp.reg_retire_tags[internal_tag[4:2]];
			external_tag = tags >> (internal_tag[1:0]*16);
			decode_external_tag(external_tag,resolved_family,resolved_index);
		end
	endtask

	// The endpoint returns only bytes previously accepted from the DUT.
	always @(posedge clk or negedge rstn) begin
		if(!rstn) begin
			rsp_valid <= 1'b0;
			rsp_data <= 128'd0;
			rsp_error <= 4'd0;
			pending <= 1'b0;
			pending_write <= 1'b0;
			pending_drop <= 1'b0;
			pending_slot <= 0;
			response_delay <= 0;
			long_wait <= 0;
			random_bits <= 16'hace1;
			held_request <= 1'b0;
			held_request_payload <= 154'd0;
			write_requests <= 0;
			write_responses <= 0;
			read_requests <= 0;
			read_responses <= 0;
			high_read_requests <= 0;
			duplicate_read_requests <= 0;
			for(i=0;i<256;i=i+1) begin
				endpoint_mem[i] <= 128'd0;
				write_seen[i] <= 1'b0;
				read_hits[i] <= 0;
			end
			for(i=0;i<4;i=i+1) reads_by_tile[i] <= 0;
		end else begin
			random_bits <= {random_bits[14:0],random_bits[15]^random_bits[13]^random_bits[12]^random_bits[10]};
			if(held_request && (!req_valid || {req_write,req_addr,req_data} !== held_request_payload))
				$fatal(1,"Request payload changed under backpressure case=%0d",case_id);
			held_request <= req_valid && !req_ready;
			held_request_payload <= {req_write,req_addr,req_data};

			if(req_valid && req_ready) begin
				slot = find_slot(req_addr);
				if(slot < 0) $fatal(1,"Request address outside 256-vector set: %h",req_addr);
				pending <= 1'b1;
				pending_write <= req_write;
				pending_slot <= slot;
				pending_drop <= case_id==11 && !req_write && read_requests==0;
				response_delay <= case_id==2 ? 80 : case_id==1 ? random_bits[6:3] : 1;
				rsp_data <= req_write ? 128'd0 :
					(endpoint_mem[slot] ^ ((case_id==3 && read_requests==17) ? 128'd1 : 128'd0));
				rsp_error <= case_id==4 && req_write && write_requests==0 ? 4'h4 : 4'd0;
				if(req_write) begin
					if(write_requests>=256 || slot!=write_requests || write_seen[slot])
						$fatal(1,"Write identity/duplicate failure request=%0d slot=%0d",write_requests,slot);
					if(req_data !== stem_golden[write_requests]) $fatal(1,"Write payload mismatch %0d",write_requests);
					endpoint_mem[slot] <= req_data;
					write_seen[slot] <= 1'b1;
					write_requests <= write_requests + 1;
				end else begin
					if(write_responses!=256 || read_requests>=289 || slot!=read_indices[read_requests])
						$fatal(1,"Read ownership/order failure request=%0d slot=%0d expected=%0d writes=%0d",
						       read_requests,slot,read_indices[read_requests],write_responses);
					if(read_hits[slot]!=0) duplicate_read_requests <= duplicate_read_requests + 1;
					read_hits[slot] <= read_hits[slot] + 1;
					if(slot>=128) high_read_requests <= high_read_requests + 1;
					if(dut.cnt_down2_tile>=4) $fatal(1,"Read tile owner range");
					reads_by_tile[dut.cnt_down2_tile] <= reads_by_tile[dut.cnt_down2_tile] + 1;
					read_requests <= read_requests + 1;
				end
			end

			if(pending && !rsp_valid && !pending_drop) begin
				if(response_delay==0) rsp_valid <= 1'b1;
				else response_delay <= response_delay - 1;
			end
			if(rsp_valid && rsp_ready) begin
				if(pending_write) write_responses <= write_responses + 1;
				else read_responses <= read_responses + 1;
				rsp_valid <= 1'b0;
				pending <= 1'b0;
				rsp_error <= 4'd0;
			end
			if(req_valid && !req_ready) long_wait <= long_wait + 1;
			else long_wait <= 0;
		end
	end

	// Backpressure is driven between active edges, including the final Stem write.
	always @(negedge clk or negedge rstn) begin
		if(!rstn) req_ready <= 1'b0;
		else if(pending || rsp_valid) req_ready <= 1'b0;
		else if(case_id==6 && !reset_done && req_valid && req_write && write_requests==255) req_ready <= 1'b0;
		else if(case_id==2 && req_valid && long_wait<80) req_ready <= 1'b0;
		else if(case_id==1) req_ready <= random_bits[0] && random_bits[2];
		else req_ready <= 1'b1;
	end

	// Count all accepted table items across reset generations.
	always @(posedge clk) begin
		if(rstn && dut.flag_table_accept) table_entries_total = table_entries_total + 1;
	end

	// Scoreboard every exported byte, halo byte, and arithmetic pipeline stage.
	always @(posedge clk or negedge rstn) begin
		if(!rstn) begin
			stem_exports <= 0;
			halo_bytes <= 0;
			padding_pixels <= 0;
			final_exports <= 0;
			accumulator_checks <= 0;
			pre_checks <= 0;
			silu_checks <= 0;
			post_checks <= 0;
			stem_acc_checks <= 0;
			stem_pre_checks <= 0;
			stem_silu_checks <= 0;
			stem_post_checks <= 0;
			dw_acc_checks <= 0;
			dw_pre_checks <= 0;
			dw_silu_checks <= 0;
			dw_post_checks <= 0;
			pw_acc_checks <= 0;
			pw_pre_checks <= 0;
			pw_silu_checks <= 0;
			pw_post_checks <= 0;
			stem_export_starts <= 16'd0;
			pw_export_starts <= 4'd0;
			for(j=0;j<4;j=j+1) padding_by_tile[j] <= 0;
			for(j=0;j<4096;j=j+1) begin
				stem_acc_seen[j] <= 1'b0;
				stem_pre_seen[j] <= 1'b0;
				stem_silu_seen[j] <= 1'b0;
				stem_post_seen[j] <= 1'b0;
				if(j<1536) begin
					output_seen[j] <= 1'b0;
					pw_acc_seen[j] <= 1'b0;
					pw_pre_seen[j] <= 1'b0;
					pw_silu_seen[j] <= 1'b0;
					pw_post_seen[j] <= 1'b0;
				end
				if(j<1024) begin
					dw_acc_seen[j] <= 1'b0;
					dw_pre_seen[j] <= 1'b0;
					dw_silu_seen[j] <= 1'b0;
					dw_post_seen[j] <= 1'b0;
				end
			end
		end else begin
			if(phase==ST_STEM_BYTE && dut.core_output_valid && dut.flag_output_ready) begin
				if(stem_exports>=4096 || dut.core_output_index !== stem_exports%256 ||
				   dut.core_output_data !== stem_golden[stem_exports/16][(stem_exports%16)*8 +: 8])
					$fatal(1,"Stem export mismatch byte=%0d local=%0d",stem_exports,dut.core_output_index);
				if((stem_exports%256)==0) begin
					if(dut.core_output_index!==0) $fatal(1,"Stem local export did not restart tile=%0d",stem_exports/256);
					stem_export_starts[stem_exports/256] = 1'b1;
				end
				stem_exports = stem_exports + 1;
			end

			if(dut.flag_halo_load && dut.core_load_ready) begin
				map_index=(halo_bytes/1296)*128+(halo_bytes%1296)/16;
				if(map_index>=512) $fatal(1,"Halo map overflow byte=%0d",halo_bytes);
				if(halo_map[map_index][8]) begin
					if(dut.wire_load_data[7:0] !== 8'd0) $fatal(1,"Nonzero padding byte=%0d",halo_bytes);
					if((halo_bytes%16)==0) begin
						padding_pixels = padding_pixels + 1;
						padding_by_tile[halo_bytes/1296] = padding_by_tile[halo_bytes/1296] + 1;
					end
				end else begin
					if(halo_map[map_index][7:0]>=256) $fatal(1,"Halo data index range");
					if(dut.wire_load_data[7:0] !== endpoint_mem[halo_map[map_index][7:0]][(halo_bytes%16)*8 +: 8])
						$fatal(1,"Halo byte did not come from endpoint byte=%0d index=%0d",halo_bytes,halo_map[map_index][7:0]);
				end
				halo_bytes = halo_bytes + 1;
			end

			if(phase==ST_OUTPUT_BYTE && dut.core_output_valid && dut.flag_output_ready) begin
				if(final_exports>=1536 || dut.core_output_index !== final_exports%384 ||
				   output_seen[final_exports] || dut.core_output_data !== pw_golden[final_exports])
					$fatal(1,"PW export mismatch global=%0d local=%0d",final_exports,dut.core_output_index);
				if((final_exports%384)==0) begin
					if(dut.core_output_index!==0) $fatal(1,"PW local export did not restart tile=%0d",final_exports/384);
					pw_export_starts[final_exports/384] = 1'b1;
				end
				output_seen[final_exports] = 1'b1;
				final_exports = final_exports + 1;
			end

			if(!dut.u_core.flag_owner_down2 && dut.u_core.s_pp_valid && dut.u_core.s_pp_ready) begin
				for(lane=0;lane<3;lane=lane+1) if(dut.u_core.s_pp_mask[lane]) begin
					decode_external_tag(dut.u_core.s_pp_tags[lane*16 +: 16],family,value_index);
					if(family!=0 || stem_acc_seen[value_index] ||
					   $signed(dut.u_core.s_pp_acc[lane*32 +: 32]) !== $signed(stem_acc[value_index]))
						$fatal(1,"Stem accumulator mismatch index=%0d",value_index);
					stem_acc_seen[value_index] = 1'b1;
					stem_acc_checks = stem_acc_checks + 1;
					accumulator_checks = accumulator_checks + 1;
				end
			end else if(dut.u_core.flag_owner_down2 && dut.u_core.u_down2.flag_pp_input_accept) begin
				for(lane=0;lane<3;lane=lane+1) if(dut.u_core.d_pp_mask[lane]) begin
					decode_external_tag(dut.u_core.d_pp_tags[lane*16 +: 16],family,value_index);
					if(family==1) begin
						if(dw_acc_seen[value_index] || $signed(dut.u_core.d_pp_acc[lane*32 +: 32]) !== $signed(dw_acc[value_index]))
							$fatal(1,"DW accumulator mismatch index=%0d",value_index);
						dw_acc_seen[value_index] = 1'b1;
						dw_acc_checks = dw_acc_checks + 1;
					end else if(family==2) begin
						if(pw_acc_seen[value_index] || $signed(dut.u_core.d_pp_acc[lane*32 +: 32]) !== $signed(pw_acc[value_index]))
							$fatal(1,"PW accumulator mismatch index=%0d",value_index);
						pw_acc_seen[value_index] = 1'b1;
						pw_acc_checks = pw_acc_checks + 1;
					end else $fatal(1,"Down2 accumulator family");
					accumulator_checks = accumulator_checks + 1;
				end
			end

			if(dut.u_core.u_pp.flag_silu_accept) begin
				resolve_internal_tag(dut.u_core.u_pp.pre_result_tag,family,value_index);
				if(family==0) begin
					if(stem_pre_seen[value_index] || dut.u_core.u_pp.pre_result_data !== stem_pre[value_index]) $fatal(1,"Stem pre mismatch index=%0d",value_index);
					stem_pre_seen[value_index]=1'b1; stem_pre_checks=stem_pre_checks+1;
				end else if(family==1) begin
					if(dw_pre_seen[value_index] || dut.u_core.u_pp.pre_result_data !== dw_pre[value_index]) $fatal(1,"DW pre mismatch index=%0d",value_index);
					dw_pre_seen[value_index]=1'b1; dw_pre_checks=dw_pre_checks+1;
				end else begin
					if(pw_pre_seen[value_index] || dut.u_core.u_pp.pre_result_data !== pw_pre[value_index]) $fatal(1,"PW pre mismatch index=%0d",value_index);
					pw_pre_seen[value_index]=1'b1; pw_pre_checks=pw_pre_checks+1;
				end
				pre_checks=pre_checks+1;
			end

			if(dut.u_core.u_pp.flag_post_accept) begin
				resolve_internal_tag(dut.u_core.u_pp.reg_meta_tags[dut.u_core.u_pp.reg_meta_read],family,value_index);
				if(family==0) begin
					if(stem_silu_seen[value_index] || dut.u_core.u_pp.silu_output_data !== stem_silu[value_index]) $fatal(1,"Stem SiLU mismatch index=%0d",value_index);
					stem_silu_seen[value_index]=1'b1; stem_silu_checks=stem_silu_checks+1;
				end else if(family==1) begin
					if(dw_silu_seen[value_index] || dut.u_core.u_pp.silu_output_data !== dw_silu[value_index]) $fatal(1,"DW SiLU mismatch index=%0d",value_index);
					dw_silu_seen[value_index]=1'b1; dw_silu_checks=dw_silu_checks+1;
				end else begin
					if(pw_silu_seen[value_index] || dut.u_core.u_pp.silu_output_data !== pw_silu[value_index]) $fatal(1,"PW SiLU mismatch index=%0d",value_index);
					pw_silu_seen[value_index]=1'b1; pw_silu_checks=pw_silu_checks+1;
				end
				silu_checks=silu_checks+1;
			end

			if(dut.u_core.u_pp.flag_post_complete) begin
				resolve_internal_tag(dut.u_core.u_pp.post_result_tag,family,value_index);
				if(family==0) begin
					if(stem_post_seen[value_index] || $signed(dut.u_core.u_pp.wire_post_saturated) !== $signed({{8{stem_post[value_index][7]}},stem_post[value_index]})) $fatal(1,"Stem post mismatch index=%0d",value_index);
					stem_post_seen[value_index]=1'b1; stem_post_checks=stem_post_checks+1;
				end else if(family==1) begin
					if(dw_post_seen[value_index] || $signed(dut.u_core.u_pp.wire_post_saturated) !== $signed({{8{dw_post[value_index][7]}},dw_post[value_index]})) $fatal(1,"DW post mismatch index=%0d",value_index);
					dw_post_seen[value_index]=1'b1; dw_post_checks=dw_post_checks+1;
				end else begin
					if(pw_post_seen[value_index] || $signed(dut.u_core.u_pp.wire_post_saturated) !== $signed({{8{pw_post[value_index][7]}},pw_post[value_index]})) $fatal(1,"PW post mismatch index=%0d",value_index);
					pw_post_seen[value_index]=1'b1; pw_post_checks=pw_post_checks+1;
				end
				post_checks=post_checks+1;
			end
		end
	end

	// Later reset points cover the last Stem response, overlap read, and fourth tile.
	initial begin
		wait(started);
		if(case_id>=5 && case_id<=10) begin
			case(case_id)
				5: wait(rstn && phase==ST_WRITE_RESPONSE && write_requests==256 && pending_write && rsp_valid);
				6: wait(rstn && phase==ST_WRITE && req_valid && !req_ready && write_requests==255);
				7: wait(rstn && phase==ST_READ_RESPONSE && read_requests==65 && pending_slot==19 && rsp_valid);
				8: wait(rstn && phase==ST_HALO_BYTE && dut.cnt_down2_tile==3 && halo_bytes>=5088);
				9: wait(rstn && phase==ST_RUN && dut.u_core.flag_owner_down2 && dut.u_core.d_busy && final_exports==1152);
				10: wait(rstn && phase==ST_OUTPUT_BYTE && dut.cnt_down2_tile==3 && dut.core_output_index>=300);
			endcase
			reset_target_seen = 1'b1;
			#1 rstn = 1'b0;
			repeat(4) @(negedge clk);
			if(dut.u_core.o_table_loaded) $fatal(1,"SiLU table survived common reset");
			reset_done = 1'b1;
			generation = generation + 1;
			rstn = 1'b1;
			@(posedge clk);
			if(rsp_valid || pending || req_valid || rsp_ready) $fatal(1,"Old transaction survived common reset");
		end
	end

	task check_success;
		begin
			if(writes!==256 || reads!==289 || output_bytes!==1536 ||
			   write_requests!=256 || write_responses!=256 || read_requests!=289 || read_responses!=289)
				$fatal(1,"Endpoint conservation W=%0d/%0d/%0d R=%0d/%0d/%0d O=%0d",
				       write_requests,write_responses,writes,read_requests,read_responses,reads,output_bytes);
			if(stem_exports!=4096 || halo_bytes!=5184 || padding_pixels!=35 || final_exports!=1536)
				$fatal(1,"Data path counts Stem=%0d halo=%0d pad=%0d PW=%0d",stem_exports,halo_bytes,padding_pixels,final_exports);
			if(stem_acc_checks!=4096 || dw_acc_checks!=1024 || pw_acc_checks!=1536 ||
			   stem_pre_checks!=4096 || dw_pre_checks!=1024 || pw_pre_checks!=1536 ||
			   stem_silu_checks!=4096 || dw_silu_checks!=1024 || pw_silu_checks!=1536 ||
			   stem_post_checks!=4096 || dw_post_checks!=1024 || pw_post_checks!=1536 ||
			   accumulator_checks!=6656 || pre_checks!=6656 || silu_checks!=6656 || post_checks!=6656)
				$fatal(1,"Arithmetic coverage total=%0d/%0d/%0d/%0d Stem=%0d/%0d/%0d/%0d DW=%0d/%0d/%0d/%0d PW=%0d/%0d/%0d/%0d",
				       accumulator_checks,pre_checks,silu_checks,post_checks,
				       stem_acc_checks,stem_pre_checks,stem_silu_checks,stem_post_checks,
				       dw_acc_checks,dw_pre_checks,dw_silu_checks,dw_post_checks,
				       pw_acc_checks,pw_pre_checks,pw_silu_checks,pw_post_checks);
			if(high_read_requests!=136 || duplicate_read_requests!=33)
				$fatal(1,"High/duplicate read coverage high=%0d duplicate=%0d",high_read_requests,duplicate_read_requests);
			if(reads_by_tile[0]!=64 || reads_by_tile[1]!=72 || reads_by_tile[2]!=72 || reads_by_tile[3]!=81)
				$fatal(1,"Read tile counts %0d/%0d/%0d/%0d",reads_by_tile[0],reads_by_tile[1],reads_by_tile[2],reads_by_tile[3]);
			if(padding_by_tile[0]!=17 || padding_by_tile[1]!=9 || padding_by_tile[2]!=9 || padding_by_tile[3]!=0)
				$fatal(1,"Padding tile counts %0d/%0d/%0d/%0d",padding_by_tile[0],padding_by_tile[1],padding_by_tile[2],padding_by_tile[3]);
			if(stem_export_starts!==16'hffff || pw_export_starts!==4'hf)
				$fatal(1,"Per-tile export restart coverage Stem=%h PW=%h",stem_export_starts,pw_export_starts);
			if(table_entries_total != ((case_id>=5 && case_id<=10) ? 2048 : 1024))
				$fatal(1,"SiLU table reload count=%0d generation=%0d",table_entries_total,generation);
			for(i=0;i<256;i=i+1) begin
				if(!write_seen[i]) $fatal(1,"Endpoint write hole slot=%0d",i);
				if(read_hits[i]!=expected_read_hits[i]) $fatal(1,"Endpoint read ownership slot=%0d actual=%0d expected=%0d",i,read_hits[i],expected_read_hits[i]);
			end
			for(i=0;i<1536;i=i+1) if(!output_seen[i]) $fatal(1,"PW output hole=%0d",i);
			sum_bins=0;
			for(i=0;i<10;i=i+1) sum_bins=sum_bins+cycle_bins[i*32 +: 32];
			if(sum_bins!==cycles) $fatal(1,"Cycle bins do not close sum=%0d cycles=%0d",sum_bins,cycles);
			if(case_id>=5 && case_id<=10 && (!reset_done || !reset_target_seen || generation!=2))
				$fatal(1,"Requested reset phase not covered");
		end
	endtask

	initial begin
		if(!$value$plusargs("CASE=%d",case_id)) case_id=0;
		if(!$value$plusargs("VECTORS=%s",vector_dir)) $fatal(1,"Missing +VECTORS=<absolute path>");
		if(case_id<0 || case_id>12) $fatal(1,"CASE must be 0..12");
		$sformat(path,"%0s/stem_golden.hex",vector_dir); $readmemh(path,stem_golden);
		$sformat(path,"%0s/stem_addresses.hex",vector_dir); $readmemh(path,stem_addresses);
		$sformat(path,"%0s/halo_map.hex",vector_dir); $readmemh(path,halo_map);
		$sformat(path,"%0s/read_indices.hex",vector_dir); $readmemh(path,read_indices);
		$sformat(path,"%0s/pw_golden.hex",vector_dir); $readmemh(path,pw_golden);
		$sformat(path,"%0s/stem_acc.hex",vector_dir); $readmemh(path,stem_acc);
		$sformat(path,"%0s/stem_pre.hex",vector_dir); $readmemh(path,stem_pre);
		$sformat(path,"%0s/stem_silu.hex",vector_dir); $readmemh(path,stem_silu);
		$sformat(path,"%0s/stem_post.hex",vector_dir); $readmemh(path,stem_post);
		$sformat(path,"%0s/dw_acc.hex",vector_dir); $readmemh(path,dw_acc);
		$sformat(path,"%0s/dw_pre.hex",vector_dir); $readmemh(path,dw_pre);
		$sformat(path,"%0s/dw_silu.hex",vector_dir); $readmemh(path,dw_silu);
		$sformat(path,"%0s/dw_post.hex",vector_dir); $readmemh(path,dw_post);
		$sformat(path,"%0s/pw_acc.hex",vector_dir); $readmemh(path,pw_acc);
		$sformat(path,"%0s/pw_pre.hex",vector_dir); $readmemh(path,pw_pre);
		$sformat(path,"%0s/pw_silu.hex",vector_dir); $readmemh(path,pw_silu);
		$sformat(path,"%0s/pw_post.hex",vector_dir); $readmemh(path,pw_post);
		for(i=0;i<256;i=i+1) begin
			expected_read_hits[i]=0;
			if(stem_addresses[i][31:25]!==0 || stem_addresses[i][2:0]!==0) $fatal(1,"Invalid native address vector %0d",i);
			for(j=0;j<i;j=j+1) if(stem_addresses[i]===stem_addresses[j]) $fatal(1,"Duplicate vector address %0d/%0d",j,i);
		end
		j=0;
		for(i=0;i<289;i=i+1) begin
			if(read_indices[i]>=256) $fatal(1,"Read index out of range ordinal=%0d value=%0d",i,read_indices[i]);
			expected_read_hits[read_indices[i]]=expected_read_hits[read_indices[i]]+1;
			if(read_indices[i]>=128) j=j+1;
		end
		slot=0;
		for(i=0;i<256;i=i+1) if(expected_read_hits[i]!=0) slot=slot+1;
		if(j!=136 || slot!=256) $fatal(1,"Read vector coverage mismatch high=%0d unique=%0d",j,slot);
		repeat(8) @(negedge clk);
		phy_ready=1'b1;
		generation=1;
		rstn=1'b1;
		started=1'b1;
		while(status==0) begin
			@(posedge clk);
			ticks=ticks+1;
			if(ticks>2000000) $fatal(1,"TB timeout case=%0d phase=%0d",case_id,phase);
		end
		if(case_id==3) begin
			if(status!==2 || error_code!==5) $fatal(1,"Read corruption expected error 5, got %0d",error_code);
		end else if(case_id==4) begin
			if(status!==2 || error_code!==7) $fatal(1,"Response error expected error 7, got %0d",error_code);
		end else if(case_id==11) begin
			if(status!==2 || error_code!==9) $fatal(1,"Dropped read expected timeout 9, got %0d",error_code);
		end else begin
			if(status!==1) $fatal(1,"Unexpected failure case=%0d error=%0d phase=%0d",case_id,error_code,phase);
			check_success;
			if(case_id==12) begin
				@(negedge clk); ddr_fault=1'b1;
				wait(status==2); @(posedge clk);
				if(error_code!==1) $fatal(1,"Post-PASS DDR fault expected error 1, got %0d",error_code);
			end
		end
		$display("TB_PASS_STEM_DDR_SEQUENCE case=%0d status=%0d error=%0d generation=%0d cycles=%0d W=%0d R=%0d Stem=%0d halo=%0d pad=%0d PW=%0d acc/pre/silu/post=%0d/%0d/%0d/%0d table=%0d StemStages=%0d/%0d/%0d/%0d DWStages=%0d/%0d/%0d/%0d PWStages=%0d/%0d/%0d/%0d",
		         case_id,status,error_code,generation,cycles,write_requests,read_requests,
		         stem_exports,halo_bytes,padding_pixels,final_exports,
		         accumulator_checks,pre_checks,silu_checks,post_checks,table_entries_total,
		         stem_acc_checks,stem_pre_checks,stem_silu_checks,stem_post_checks,
		         dw_acc_checks,dw_pre_checks,dw_silu_checks,dw_post_checks,
		         pw_acc_checks,pw_pre_checks,pw_silu_checks,pw_post_checks);
		$finish;
	end
endmodule
