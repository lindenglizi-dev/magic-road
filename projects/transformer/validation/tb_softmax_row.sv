`timescale 1ns/1ps
// Self-checking row Softmax: Python goldens, input bubbles and output backpressure.
module tb_softmax_row;
  logic clk = 0;
  always #5 clk = ~clk;
  logic rst_n = 0, start = 0;
  logic [6:0] seq_len = 0;
  logic [16:0] scale_q16 = 0;
  logic signed [31:0] in_data = 0;
  logic in_valid = 0, out_ready = 0;
  wire in_ready, out_valid, out_last, busy, done, error;
  wire [7:0] out_data;
  wire [6:0] out_index;
  wire [2:0] dbg_state;
  wire [21:0] dbg_exp_sum;
  softmax_row_int32 dut (.*);

  integer scores [0:63], expected [0:63];
  integer row_len, row_scale, expected_sum;
  integer accepted_in = 0, accepted_out = 0;
  integer completed_rows = 0, total_outputs = 0;
  integer stalled_cycles = 0, bubble_cycles = 0;
  integer file_handle, read_count, case_count, case_index, index;
  bit row_active = 0, previous_stall = 0;
  logic [7:0] held_data;
  logic [6:0] held_index;
  logic held_last;
  string vector_file;

  // All drives occur on falling edges; transfer checks sample before NBA updates.
  task automatic step(input bit launch, input bit valid_in,
                      input logic signed [31:0] score, input bit ready_out);
    bit final_transfer, expect_error;
    begin
      @(negedge clk);
      start = launch; in_valid = valid_in; in_data = score; out_ready = ready_out;
      @(posedge clk);
      final_transfer = 0;
      expect_error = launch && (busy === 1'b0) &&
                     (seq_len == 0 || seq_len > 64 || scale_q16 == 0 || scale_q16 > 65536);
      if ((in_ready !== 1'b0 && in_ready !== 1'b1) ||
          (out_valid !== 1'b0 && out_valid !== 1'b1) ||
          (busy !== 1'b0 && busy !== 1'b1))
        $fatal(1, "Softmax unknown handshake state");
      if (previous_stall &&
          (out_valid !== 1'b1 || out_data !== held_data ||
           out_index !== held_index || out_last !== held_last))
        $fatal(1, "Softmax output changed while blocked");
      previous_stall = (out_valid === 1'b1 && !ready_out);
      if (previous_stall) begin
        held_data = out_data; held_index = out_index; held_last = out_last;
        stalled_cycles = stalled_cycles + 1;
      end
      if (out_valid === 1'b1) begin
        if (!row_active || accepted_in != row_len || accepted_out >= row_len)
          $fatal(1, "Softmax unexpected or premature output");
        if (out_index !== accepted_out[6:0] || out_data !== expected[accepted_out][7:0] ||
            out_last !== (accepted_out == row_len - 1))
          $fatal(1, "Softmax mismatch case=%0d index=%0d got=%0d expected=%0d last=%b",
                 case_index, accepted_out, out_data, expected[accepted_out], out_last);
        if (dbg_exp_sum !== expected_sum[21:0])
          $fatal(1, "Softmax exponent sum mismatch got=%0d expected=%0d", dbg_exp_sum, expected_sum);
        if (ready_out) begin
          final_transfer = (accepted_out == row_len - 1);
          accepted_out = accepted_out + 1;
          total_outputs = total_outputs + 1;
        end
      end
      if (in_ready === 1'b1) begin
        if (valid_in) begin
          if (!row_active || accepted_in >= row_len)
            $fatal(1, "Softmax accepted unexpected input");
          accepted_in = accepted_in + 1;
        end else bubble_cycles = bubble_cycles + 1;
      end
      #1;
      if (done !== final_transfer || error !== expect_error)
        $fatal(1, "Softmax pulse mismatch done=%b expected=%b error=%b expected=%b",
               done, final_transfer, error, expect_error);
      if (final_transfer) begin
        if (busy !== 1'b0 || out_valid !== 1'b0 || in_ready !== 1'b0)
          $fatal(1, "Softmax did not return idle on final transfer");
        completed_rows = completed_rows + 1;
        row_active = 0;
      end else if (row_active && busy !== 1'b1)
        $fatal(1, "Softmax dropped busy before final transfer");
      if (expect_error && (busy !== 1'b0 || in_ready !== 1'b0 || out_valid !== 1'b0))
        $fatal(1, "Softmax invalid start entered busy state");
    end
  endtask

  task automatic apply_reset;
    begin
      @(negedge clk);
      rst_n = 0; start = 0; in_valid = 0; out_ready = 0;
      row_active = 0; previous_stall = 0; accepted_in = 0; accepted_out = 0;
      repeat (2) begin
        @(posedge clk); #1;
        if (busy !== 1'b0 || done !== 1'b0 || error !== 1'b0 ||
            in_ready !== 1'b0 || out_valid !== 1'b0)
          $fatal(1, "Softmax reset failed to clear protocol state");
      end
      @(negedge clk); rst_n = 1;
      step(0, 0, 0, 0);
    end
  endtask

  task automatic collect_row;
    integer sample_index, gap;
    begin
      seq_len = row_len; scale_q16 = row_scale;
      accepted_in = 0; accepted_out = 0; row_active = 1;
      step(1, 0, 0, 0);
      for (sample_index = 0; sample_index < row_len; sample_index = sample_index + 1) begin
        for (gap = 0; gap <= sample_index % 3; gap = gap + 1)
          step(0, 0, 32'sh5a5a5a5a, 0);
        step(0, 1, scores[sample_index], 0);
        if (accepted_in != sample_index + 1)
          $fatal(1, "Softmax input handshake missing");
      end
    end
  endtask

  task automatic wait_output;
    integer wait_cycles;
    begin
      wait_cycles = 0;
      while (out_valid !== 1'b1 && wait_cycles < 1000) begin
        step(0, 0, 0, 0);
        wait_cycles = wait_cycles + 1;
      end
      if (out_valid !== 1'b1) $fatal(1, "Softmax output timeout");
    end
  endtask

  task automatic run_row;
    integer output_index;
    begin
      collect_row();
      for (output_index = 0; output_index < row_len; output_index = output_index + 1) begin
        wait_output();
        repeat (3) step(0, 0, 0, 0);
        step(0, 0, 0, 1);
      end
      if (accepted_out != row_len) $fatal(1, "Softmax output count mismatch");
      repeat (2) step(0, 0, 0, 0);
      $display("Softmax case=%0d len=%0d scale=%0d PASS", case_index, row_len, row_scale);
    end
  endtask

  task automatic reject_start(input integer bad_len, input integer bad_scale);
    begin
      seq_len = bad_len; scale_q16 = bad_scale;
      step(1, 0, 0, 0);
      step(0, 0, 0, 0);
    end
  endtask

  initial begin
    if (!$value$plusargs("VECTORS=%s", vector_file))
      vector_file = "../reports/softmax_unit_vectors/cases.txt";
    file_handle = $fopen(vector_file, "r");
    if (!file_handle) $fatal(1, "Cannot open Softmax vectors: %s", vector_file);
    read_count = $fscanf(file_handle, "%d", case_count);
    if (read_count != 1 || case_count != 9) $fatal(1, "Invalid Softmax case count");
    apply_reset();
    reject_start(0, 65536);
    reject_start(65, 65536);
    reject_start(1, 0);
    reject_start(1, 65537);
    for (case_index = 0; case_index < case_count; case_index = case_index + 1) begin
      read_count = $fscanf(file_handle, "%d %d %d", row_len, row_scale, expected_sum);
      if (read_count != 3 || row_len < 1 || row_len > 64 || row_scale < 1 || row_scale > 65536)
        $fatal(1, "Invalid Softmax vector header");
      for (index = 0; index < row_len; index = index + 1) begin
        read_count = $fscanf(file_handle, "%d %d", scores[index], expected[index]);
        if (read_count != 2 || expected[index] < 0 || expected[index] > 255)
          $fatal(1, "Invalid Softmax vector element");
      end
      run_row();
    end
    $fclose(file_handle);
    // Reset while a valid output is blocked, then restart without stale transfers.
    collect_row(); wait_output(); repeat (2) step(0, 0, 0, 0);
    if (busy !== 1'b1 || out_valid !== 1'b1) $fatal(1, "Softmax reset case did not reach stall");
    apply_reset();
    run_row();
    if (completed_rows != case_count + 1 || stalled_cycles < total_outputs * 3 || bubble_cycles == 0)
      $fatal(1, "Softmax coverage missing rows=%0d stalls=%0d bubbles=%0d",
             completed_rows, stalled_cycles, bubble_cycles);
    $display("PASS SOFTMAX_ROW rows=%0d outputs=%0d stalls=%0d bubbles=%0d invalid_starts=4 reset_restart=1",
             completed_rows, total_outputs, stalled_cycles, bubble_cycles);
    $finish;
  end

  initial begin
    #1000000;
    $fatal(1, "Softmax global watchdog timeout");
  end
endmodule
