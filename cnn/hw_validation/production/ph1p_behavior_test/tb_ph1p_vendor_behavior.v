`timescale 1ns / 1ps

module tb_ph1p_vendor_behavior;

	reg [19:0]dia;
	reg [9:0]addra;
	reg cea;
	reg ocea;
	reg clka;
	reg wea;
	reg rsta;
	reg bea;
	integer sample_index;
	wire [19:0]doa;
	wire [19:0]dob;
	wire ecc_sbiterr;
	wire ecc_dbiterr;

	PH1P_LOGIC_ERAM #(
		.DATA_WIDTH_A(20),
		.DATA_WIDTH_B(20),
		.ADDR_WIDTH_A(10),
		.ADDR_WIDTH_B(10),
		.DATA_DEPTH_A(1024),
		.DATA_DEPTH_B(1024),
		.BYTE_ENABLE(0),
		.BYTE_A(1),
		.BYTE_B(1),
		.MODE("SP"),
		.REGMODE_A("NOREG"),
		.REGMODE_B("NOREG"),
		.WRITEMODE_A("NORMAL"),
		.WRITEMODE_B("NORMAL"),
		.RESETMODE_A("ASYNC"),
		.RESETMODE_B("ASYNC"),
		.OREGSET_A("RESET"),
		.OREGSET_B("RESET"),
		.SSROVERCE("DISABLE"),
		.ECC_DECODE("DISABLE"),
		.ECC_ENCODE("DISABLE"),
		.ASYNC_RESET_RELEASE_A("ASYNC"),
		.ASYNC_RESET_RELEASE_B("ASYNC"),
		.CLKMODE("ASYNC"),
		.DEBUGGABLE("NO"),
		.PACKABLE("NO"),
		.FORCE_KEEP("ON"),
		.INIT_FILE("NONE"),
		.FILL_ALL("NONE"),
		.IMPLEMENT("20K")
	) dut (
		.dia(dia),
		.addra(addra),
		.cea(cea),
		.ocea(ocea),
		.clka(clka),
		.wea(wea),
		.rsta(rsta),
		.bea(bea),
		.dib(20'd0),
		.addrb(10'd0),
		.ceb(1'b0),
		.oceb(1'b0),
		.clkb(clka),
		.web(1'b0),
		.rstb(1'b0),
		.beb(1'b0),
		.ecc_sbiterrinj(1'b0),
		.ecc_dbiterrinj(1'b0),
		.doa(doa),
		.dob(dob),
		.ecc_sbiterr(ecc_sbiterr),
		.ecc_dbiterr(ecc_dbiterr)
	);

	initial begin
		clka = 1'b0;
		forever #5 clka = ~clka;
	end

	initial begin
		dia = 20'd0;
		addra = 10'd0;
		cea = 1'b0;
		ocea = 1'b0;
		wea = 1'b0;
		rsta = 1'b0;
		bea = 1'b0;

		#1 $display("OBS initial_before_gsr_release t=%0t doa=%h dob=%h", $time, doa, dob);
		#60 $display("OBS after_gsr_guard t=%0t doa=%h dob=%h", $time, doa, dob);

		addra = 10'd10;
		cea = 1'b1;
		for(sample_index = 0; sample_index < 2; sample_index = sample_index + 1)begin
			@(posedge clka);
			#1 $display("OBS read_uninitialized_addr10 sample=%0d t=%0t doa=%h", sample_index, $time, doa);
		end

		addra = 10'd7;
		dia = 20'h12345;
		cea = 1'b1;
		wea = 1'b1;
		@(posedge clka);
		#1 $display("OBS write_addr7_plus1ns t=%0t doa=%h", $time, doa);

		wea = 1'b0;
		for(sample_index = 0; sample_index < 3; sample_index = sample_index + 1)begin
			@(posedge clka);
			#1 $display("OBS read_addr7_ocea0 sample=%0d t=%0t doa=%h", sample_index, $time, doa);
		end

		cea = 1'b0;
		addra = 10'd8;
		for(sample_index = 0; sample_index < 2; sample_index = sample_index + 1)begin
			@(posedge clka);
			#1 $display("OBS cea0_hold sample=%0d t=%0t doa=%h", sample_index, $time, doa);
		end

		cea = 1'b1;
		dia = 20'h2abcd;
		wea = 1'b1;
		@(posedge clka);
		#1 $display("OBS write_addr8_plus1ns t=%0t doa=%h", $time, doa);

		wea = 1'b0;
		for(sample_index = 0; sample_index < 3; sample_index = sample_index + 1)begin
			@(posedge clka);
			#1 $display("OBS read_addr8_ocea0 sample=%0d t=%0t doa=%h", sample_index, $time, doa);
		end

		addra = 10'd7;
		ocea = 1'b1;
		for(sample_index = 0; sample_index < 3; sample_index = sample_index + 1)begin
			@(posedge clka);
			#1 $display("OBS read_addr7_ocea1 sample=%0d t=%0t doa=%h", sample_index, $time, doa);
		end

		cea = 1'b0;
		#2 rsta = 1'b1;
		#1 $display("OBS async_reset_assert_plus1ns t=%0t doa=%h", $time, doa);
		#2 rsta = 1'b0;

		addra = 10'd8;
		cea = 1'b1;
		ocea = 1'b0;
		for(sample_index = 0; sample_index < 3; sample_index = sample_index + 1)begin
			@(posedge clka);
			#1 $display("OBS read_addr8_after_reset sample=%0d t=%0t doa=%h", sample_index, $time, doa);
		end

		addra = 10'd9;
		dia = 20'h54321;
		wea = 1'b1;
		@(posedge clka);
		#1 $display("OBS collision_write_addr9_plus1ns t=%0t doa=%h", $time, doa);
		wea = 1'b0;
		for(sample_index = 0; sample_index < 2; sample_index = sample_index + 1)begin
			@(posedge clka);
			#1 $display("OBS read_addr9_after_collision sample=%0d t=%0t doa=%h", sample_index, $time, doa);
		end

		$display("OBS complete t=%0t", $time);
		$finish;
	end

endmodule
