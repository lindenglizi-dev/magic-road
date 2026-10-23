`timescale 1ns/1ps
module tb_probability_writer;
  logic clk = 0;
  always #5 clk = ~clk;
  logic rst_n = 1;
  logic [6:0] seq_len = 1, row_idx = 0, in_index = 0;
  logic [7:0] in_data = 0;
  logic in_valid = 0, in_last = 0;
  wire in_ready, wr_en, row_done;
  wire [1:0] wr_bank;
  wire [15:0] wr_addr;
  wire signed [7:0] wr_data;
  probability_writer dut (.*);

  logic expected_done = 0, corrupt_expected;
  integer checked_beats = 0, valid_beats = 0, bubbles = 0;
  integer data_values = 0, matrix_positions = 0;
  integer value, shape, length, row, column;

  task automatic check_comb;
    integer expected_data, expected_bank, expected_addr;
    begin
      // Integer ceil and limit: no DUT shift/low-bit expression is reused.
      expected_data = (integer'(in_data) + 1) / 2;
      if (expected_data > 127) expected_data = 127;
      if (corrupt_expected && checked_beats == 0)
        expected_data = expected_data ^ 1;
      expected_bank = integer'(row_idx) % 4;
      expected_addr = (integer'(row_idx) / 4) * integer'(seq_len) + integer'(in_index);
      if (in_ready !== 1'b1 || wr_en !== in_valid)
        $fatal(1,"PROBABILITY_WRITER handshake mismatch beat=%0d",checked_beats);
      if ($signed(wr_data) !== expected_data)
        $fatal(1,"PROBABILITY_WRITER data mismatch input=%0d expected=%0d got=%0d",
               in_data,expected_data,$signed(wr_data));
      if (wr_bank !== expected_bank[1:0] || wr_addr !== expected_addr[15:0])
        $fatal(1,"PROBABILITY_WRITER address mismatch L=%0d row=%0d col=%0d bank=%0d addr=%0d",
               seq_len,row_idx,in_index,wr_bank,wr_addr);
    end
  endtask

  task automatic apply_beat(input integer len, input integer rr, input integer cc,
                            input integer data, input logic valid, input logic last);
    begin
      @(negedge clk);
      seq_len=len; row_idx=rr; in_index=cc; in_data=data;
      in_valid=valid; in_last=last;
      #1;
      check_comb();
      if (row_done !== expected_done)
        $fatal(1,"PROBABILITY_WRITER row_done changed before sampling edge");
      @(posedge clk);
      check_comb();
      expected_done=valid && last;
      #1;
      if (row_done !== expected_done)
        $fatal(1,"PROBABILITY_WRITER row_done mismatch valid=%0b last=%0b got=%0b",
               valid,last,row_done);
      checked_beats=checked_beats+1;
      if (valid) valid_beats=valid_beats+1;
      else bubbles=bubbles+1;
    end
  endtask

  initial begin
    #1000000;
    $fatal(1,"PROBABILITY_WRITER watchdog");
  end

  initial begin
    corrupt_expected=$test$plusargs("CORRUPT_EXPECTED");
    #2; rst_n=0;
    #1;
    if (row_done !== 1'b0) $fatal(1,"PROBABILITY_WRITER initial async reset");
    repeat(2) @(negedge clk);
    rst_n=1;
    // Adjacent single-item rows legally keep row_done high across two edges.
    apply_beat(1,0,0,255,1,1);
    apply_beat(1,0,0,0,1,1);
    apply_beat(1,0,0,1,1,1);
    apply_beat(1,0,0,254,0,1);
    apply_beat(1,0,0,253,0,0);

    for (value=0;value<256;value=value+1) begin
      apply_beat(64,12+value/64,value%64,value,1,value%64==63);
      data_values=data_values+1;
    end
    for (shape=0;shape<4;shape=shape+1) begin
      case (shape)
        0: length=1;
        1: length=2;
        2: length=5;
        3: length=64;
      endcase
      for (row=0;row<length;row=row+1) begin
        apply_beat(length,row,length-1,(row+253)%256,0,1);
        for (column=0;column<length;column=column+1) begin
          if (column%17==7)
            apply_beat(length,row,column,(row+column+128)%256,0,0);
          apply_beat(length,row,column,(row*73+column*19+shape)%256,1,column==length-1);
          matrix_positions=matrix_positions+1;
        end
      end
    end

    apply_beat(64,63,63,255,1,1);
    @(negedge clk);
    #2; rst_n=0;
    #1;
    expected_done=0;
    check_comb();
    if (row_done !== 1'b0 || wr_en !== 1'b1)
      $fatal(1,"PROBABILITY_WRITER reset must clear done without masking combinational write");
    @(posedge clk);
    #1;
    if (row_done !== 1'b0) $fatal(1,"PROBABILITY_WRITER done during reset");
    @(negedge clk);
    in_valid=0; in_last=1; in_data=2; row_idx=0; in_index=0;
    #1; check_comb();
    @(posedge clk);
    #1;
    if (row_done !== 1'b0) $fatal(1,"PROBABILITY_WRITER stale done during reset");
    @(negedge clk);
    rst_n=1;
    apply_beat(2,1,1,254,1,1);
    apply_beat(2,0,0,0,0,1);
    if (data_values != 256 || matrix_positions != 4126)
      $fatal(1,"PROBABILITY_WRITER incomplete value/position coverage");
    $display("PASS PROBABILITY_WRITER values=%0d matrix_positions=%0d valid_beats=%0d bubbles=%0d async_reset=PASS",
             data_values,matrix_positions,valid_beats,bubbles);
    $finish;
  end
endmodule
