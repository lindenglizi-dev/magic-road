`timescale 1ns / 1ps

// Actual sequence plus actual CDC endpoint; the external memory is controlled.
module tb_stem_ddr_mailbox;
	reg clk=0,ddr_clk=0,rstn=0,phy_ready=0;
	always #5 clk=~clk;
	initial begin #1.7; forever #3.75 ddr_clk=~ddr_clk; end
	wire req_valid,req_ready,req_write,rsp_valid,rsp_ready,fault;
	wire [24:0]req_addr,awaddr,araddr;
	wire [127:0]req_data,rsp_data,wdata;
	wire [3:0]rsp_error;
	wire awvalid,wvalid,wlast,arvalid,rready;
	wire [15:0]wstrb;
	reg awready=0,wready=0,arready=0,rvalid=0;
	reg [127:0]rdata=0;
	wire [1:0]status;
	wire [3:0]error_code;
	wire [4:0]phase;
	wire [8:0]writes,reads;
	wire [10:0]output_bytes;
	wire [31:0]cycles;
	wire [319:0]cycle_bins;
	reg [31:0]addresses[0:255];
	reg [127:0]golden[0:255],memory[0:255];
	reg [7:0]golden_pw[0:2047];
	reg [15:0]read_indices[0:288];
	reg seen_write[0:255],seen_read[0:255];
	reg pending_aw=0,pending_read=0;
	reg [24:0]held_aw;
	reg [15:0]random_bits=16'hace1;
	reg [4095:0]vectors,file_path;
	integer mode=0,unused,aw_count=0,w_count=0,ar_count=0,r_count=0;
	integer slot=0,read_slot=0,delay_left=0,ticks=0,k,total,source_writes=0,source_reads=0;

	road_stem_ddr_sequence #(.C_TIMEOUT(27'd20000)) dut(
		.i_clk(clk),.i_rstn(rstn),.i_phy_ready(phy_ready),.i_ddr_fault(fault),
		.i_req_ready(req_ready),.i_rsp_valid(rsp_valid),.i_rsp_data(rsp_data),.i_rsp_error(rsp_error),
		.o_req_valid(req_valid),.o_req_write(req_write),.o_req_addr(req_addr),.o_req_data(req_data),.o_rsp_ready(rsp_ready),
		.o_status(status),.o_error(error_code),.o_phase(phase),.o_writes(writes),.o_reads(reads),
		.o_output_bytes(output_bytes),.o_cycles(cycles),.o_cycle_bins(cycle_bins),.o_address(),.o_expected(),.o_actual()
	);
	road_paxi_mailbox #(.C_TIMEOUT(27'd20000)) mailbox(
		.i_clk(clk),.i_rstn(rstn),.i_ddr_clk(ddr_clk),.i_ddr_rstn(rstn),.i_phy_ready(phy_ready),
		.i_req_valid(req_valid),.i_req_write(req_write),.i_req_addr(req_addr),.i_req_data(req_data),.o_req_ready(req_ready),
		.o_rsp_valid(rsp_valid),.o_rsp_data(rsp_data),.o_rsp_error(rsp_error),.i_rsp_ready(rsp_ready),.o_fault(fault),
		.i_awready(awready),.i_wready(wready),.i_arready(arready),.i_rvalid(rvalid),.i_rlast(1'b1),.i_rdata(rdata),
		.o_awaddr(awaddr),.o_awvalid(awvalid),.o_wdata(wdata),.o_wstrb(wstrb),.o_wvalid(wvalid),.o_wlast(wlast),
		.o_araddr(araddr),.o_arvalid(arvalid),.o_rready(rready)
	);

	// Drive endpoint readiness away from its sampling edge.
	always@(negedge ddr_clk)begin
		random_bits={random_bits[14:0],random_bits[15]^random_bits[13]^random_bits[12]^random_bits[10]};
		awready=rstn && (mode==0 || random_bits[0]);
		wready=rstn && (mode==0 || random_bits[3]);
		arready=rstn && (mode==0 || random_bits[6]);
	end

	// Four consumers may reread overlap; each producer address is written once.
	always@(posedge ddr_clk)begin
		if(rstn)begin
			if(awvalid && awready)begin
				if(pending_aw || aw_count>=256 || awaddr!==addresses[aw_count][24:0]) $fatal(1,"AW sequence or duplicate");
				pending_aw=1; held_aw=awaddr; aw_count=aw_count+1;
			end
			if(wvalid && wready)begin
				if(!pending_aw || w_count>=256 || held_aw!==addresses[w_count][24:0] || wstrb!==16'd0 || !wlast)
					$fatal(1,"W without unique accepted AW");
				if(wdata!==golden[w_count] || seen_write[w_count]) $fatal(1,"Actual Stem write mismatch");
				memory[w_count]=wdata; seen_write[w_count]=1; pending_aw=0; w_count=w_count+1;
			end
			if(rvalid && rready)begin rvalid<=0; pending_read=0; r_count=r_count+1; end
			if(arvalid && arready)begin
				if(pending_read || w_count!=256 || ar_count>=289) $fatal(1,"Read before all accepted writes");
				slot=-1;
				for(k=0;k<256;k=k+1) if(araddr==addresses[k][24:0]) slot=k;
				if(slot<0) $fatal(1,"Unknown read address");
				if(!seen_write[slot] || slot!==read_indices[ar_count]) $fatal(1,"Read ownership/order mismatch");
				seen_read[slot]=1; read_slot=slot; pending_read=1; delay_left=mode==0 ? 2 : 2+random_bits[11:8];
				ar_count=ar_count+1;
			end
			if(pending_read && !rvalid)begin
				if(delay_left==0)begin rdata<=memory[read_slot]; rvalid<=1; end
				else delay_left=delay_left-1;
			end
		end
	end

	// Check the final real cache port and classify total endpoint cycles independently.
	always@(posedge clk)begin
		if(rstn)begin
			ticks=ticks+1;
			if(ticks>200000) $fatal(1,"Integrated timeout phase=%0d error=%0d",phase,error_code);
			if(req_valid && req_ready)begin
				if(req_write) source_writes=source_writes+1; else source_reads=source_reads+1;
			end
			if(dut.core_output_valid && dut.flag_output_ready && dut.core_selected)begin
				if(dut.core_output_data!==golden_pw[output_bytes]) $fatal(1,"Actual PW export mismatch");
			end
		end
	end

	initial begin
		unused=$value$plusargs("MODE=%d",mode);
		if(!$value$plusargs("VECTORS=%s",vectors)) $fatal(1,"Missing vectors");
		$sformat(file_path,"%0s/stem_addresses.hex",vectors); $readmemh(file_path,addresses);
		$sformat(file_path,"%0s/stem_golden.hex",vectors); $readmemh(file_path,golden);
		$sformat(file_path,"%0s/pw_golden.hex",vectors); $readmemh(file_path,golden_pw);
		$sformat(file_path,"%0s/read_indices.hex",vectors); $readmemh(file_path,read_indices);
		for(k=0;k<256;k=k+1)begin memory[k]=0;seen_write[k]=0;seen_read[k]=0;end
		#31; rstn=1;
		#19; phy_ready=1;
		wait(status!=0); #1;
		if(status!=1 || error_code!=0 || writes!=256 || reads!=289 || output_bytes!=1536)
			$fatal(1,"Integrated failed phase=%0d error=%0d W=%0d R=%0d PW=%0d",phase,error_code,writes,reads,output_bytes);
		if(aw_count!=256 || w_count!=256 || ar_count!=289 || r_count!=289 || source_writes!=256 || source_reads!=289)
			$fatal(1,"Integrated handshake conservation");
		total=0;
		for(k=0;k<10;k=k+1)begin
			total=total+cycle_bins[k*32+:32];
			$display("INTEGRATED_BIN mode=%0d bin=%0d cycles=%0d",mode,k,cycle_bins[k*32+:32]);
		end
		if(total!=cycles) $fatal(1,"Mutually exclusive cycle sum mismatch");
		for(k=0;k<256;k=k+1) if(!seen_read[k]) $fatal(1,"Unconsumed producer word");
		$display("STEM_DDR_MAILBOX_PASS mode=%0d cycles=%0d W=256 R=289 PW=1536",mode,cycles);
		repeat(10) @(negedge clk);
		$finish;
	end
endmodule
