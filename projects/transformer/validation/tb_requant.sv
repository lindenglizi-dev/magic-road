`timescale 1ns/1ps
// Python integer-floor goldens; every registered value and tag is checked.
module tb_requant;
  logic clk = 0;
  always #5 clk = ~clk;
  logic rst_n = 1, in_valid = 0;
  logic signed [31:0] in_raw = 0;
  logic [4:0] in_shift = 0;
  logic [17:0] in_addr = 0;
  logic [1:0] in_phase = 0;
  logic [8:0] in_row = 0, in_col = 0;
  wire rq_valid, rq_saturated, ffn_valid;
  wire signed [7:0] rq_data, ffn_data;
  wire [17:0] rq_addr;
  wire [1:0] rq_phase;
  wire signed [31:0] rq_raw;
  wire [8:0] ffn_row, ffn_col;

  requant_shift_sat dut_requant (
    .clk(clk), .rst_n(rst_n), .in_valid(in_valid), .in_raw(in_raw),
    .in_shift(in_shift), .in_addr(in_addr), .in_phase(in_phase),
    .out_valid(rq_valid), .out_data(rq_data), .out_addr(rq_addr),
    .out_phase(rq_phase), .out_raw(rq_raw), .out_saturated(rq_saturated)
  );
  ffn_relu_requant dut_ffn (
    .clk(clk), .rst_n(rst_n), .in_valid(in_valid), .in_raw(in_raw),
    .in_shift(in_shift), .in_row(in_row), .in_col(in_col),
    .out_valid(ffn_valid), .out_data(ffn_data), .out_row(ffn_row), .out_col(ffn_col)
  );

  bit expected_valid = 0;
  logic signed [7:0] expected_rq = 0, expected_ffn = 0;
  logic [17:0] expected_addr = 0;
  logic [1:0] expected_phase = 0;
  logic signed [31:0] expected_raw = 0;
  bit expected_sat = 0;
  logic [8:0] expected_row = 0, expected_col = 0;
  integer checked = 0, bubbles = 0, resets = 0, adjacent = 0;
  logic [31:0] seen_shifts = 0;
  integer file_handle, read_count, case_count, case_index;
  longint signed raw_read;
  integer shift_read, addr_read, phase_read, row_read, col_read;
  integer rq_read, sat_read, ffn_read;
  string vector_file, extra_token;

  task automatic check_outputs;
    begin
      if ({rq_valid, rq_data, rq_addr, rq_phase, rq_raw, rq_saturated} !==
          {expected_valid, expected_rq, expected_addr, expected_phase, expected_raw, expected_sat})
        $fatal(1, "requant mismatch case=%0d raw=%0d shift=%0d valid=%b data=%0d expected=%0d sat=%b expected_sat=%b",
               case_index, in_raw, in_shift, rq_valid, rq_data, expected_rq, rq_saturated, expected_sat);
      if ({ffn_valid, ffn_data, ffn_row, ffn_col} !==
          {expected_valid, expected_ffn, expected_row, expected_col})
        $fatal(1, "FFN mismatch case=%0d valid=%b data=%0d expected=%0d row=%0d col=%0d",
               case_index, ffn_valid, ffn_data, expected_ffn, ffn_row, ffn_col);
    end
  endtask

  // Drive away from the active edge; invalid payload changes must not leak out.
  task automatic step(input bit valid_in);
    begin
      @(negedge clk);
      in_valid = valid_in;
      in_raw = valid_in ? raw_read[31:0] : ~raw_read[31:0];
      in_shift = valid_in ? shift_read[4:0] : ~shift_read[4:0];
      in_addr = valid_in ? addr_read[17:0] : ~addr_read[17:0];
      in_phase = valid_in ? phase_read[1:0] : ~phase_read[1:0];
      in_row = valid_in ? row_read[8:0] : ~row_read[8:0];
      in_col = valid_in ? col_read[8:0] : ~col_read[8:0];
      #1;
      check_outputs();
      @(posedge clk);
      if (valid_in && expected_valid) adjacent = adjacent + 1;
      #1;
      expected_valid = valid_in;
      if (valid_in) begin
        expected_rq = rq_read[7:0]; expected_ffn = ffn_read[7:0];
        expected_addr = addr_read[17:0]; expected_phase = phase_read[1:0];
        expected_raw = raw_read[31:0]; expected_sat = sat_read[0];
        expected_row = row_read[8:0]; expected_col = col_read[8:0];
        checked = checked + 1;
        seen_shifts[shift_read] = 1'b1;
      end else bubbles = bubbles + 1;
      check_outputs();
    end
  endtask

  task automatic apply_reset;
    begin
      @(negedge clk);
      // Assert between edges with an unaccepted valid input pending.
      in_valid = 1; in_raw = 32'sh7fffffff; in_addr = 18'h3ffff;
      #1; rst_n = 0;
      expected_valid = 0; expected_rq = 0; expected_ffn = 0;
      expected_addr = 0; expected_phase = 0; expected_raw = 0;
      expected_sat = 0; expected_row = 0; expected_col = 0;
      #1; check_outputs();
      @(posedge clk); #1; check_outputs();
      @(negedge clk); in_valid = 0; rst_n = 1;
      @(posedge clk); #1; check_outputs();
      resets = resets + 1;
    end
  endtask

  initial begin
    if (!$value$plusargs("VECTORS=%s", vector_file))
      $fatal(1, "missing +VECTORS=<cases.txt>");
    file_handle = $fopen(vector_file, "r");
    if (!file_handle) $fatal(1, "cannot open requant vectors %s", vector_file);
    read_count = $fscanf(file_handle, "%d", case_count);
    if (read_count != 1 || (^case_count === 1'bx) || case_count < 32 || case_count > 10000)
      $fatal(1, "invalid requant case count");
    apply_reset();
    for (case_index = 0; case_index < case_count; case_index = case_index + 1) begin
      read_count = $fscanf(file_handle, "%d %d %d %d %d %d %d %d %d",
                           raw_read, shift_read, addr_read, phase_read, row_read, col_read,
                           rq_read, sat_read, ffn_read);
      if (read_count != 9 || (^{raw_read, shift_read, addr_read, phase_read, row_read, col_read,
                               rq_read, sat_read, ffn_read} === 1'bx))
        $fatal(1, "missing or unknown requant vector case=%0d", case_index);
      if (raw_read < -64'sd2147483648 || raw_read > 64'sd2147483647 ||
          shift_read < 0 || shift_read > 31 || addr_read < 0 || addr_read > 262143 ||
          phase_read < 0 || phase_read > 3 || row_read < 0 || row_read > 511 ||
          col_read < 0 || col_read > 511 || rq_read < -128 || rq_read > 127 ||
          sat_read < 0 || sat_read > 1 || ffn_read < 0 || ffn_read > 127)
        $fatal(1, "out-of-range requant vector case=%0d", case_index);
      if (case_index % 7 == 0) step(0);
      if (case_index % 11 == 0) step(0);
      step(1);
      if (case_index == case_count / 2) begin
        if (rq_valid !== 1'b1 || ffn_valid !== 1'b1) $fatal(1, "reset requires active outputs");
        apply_reset();
      end
    end
    if ($fscanf(file_handle, "%s", extra_token) == 1) $fatal(1, "extra requant vector data");
    $fclose(file_handle);
    repeat (3) step(0);
    if (checked != case_count || seen_shifts !== 32'hffffffff ||
        bubbles == 0 || adjacent == 0 || resets != 2)
      $fatal(1, "incomplete requant coverage checked=%0d expected=%0d", checked, case_count);
    $display("PASS REQUANT_UNIT vectors=%0d outputs=%0d shifts=32 bubbles=%0d adjacent=%0d resets=%0d",
             checked, 2 * checked, bubbles, adjacent, resets);
    $finish;
  end

  initial begin
    #1000000;
    $fatal(1, "requant watchdog expired");
  end
endmodule
