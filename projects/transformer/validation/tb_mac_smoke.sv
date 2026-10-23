`timescale 1ns/1ps
module tb_mac_smoke;
  logic clk = 0;
  always #5 clk = ~clk;
  logic rst_n = 0, clear = 0, mac_en = 0;
  logic [31:0] a_vec = 0, b_vec = 0;
  wire [511:0] acc_bus;
  mac_array_4x4 dut (.*);
  integer exp_acc [0:3][0:3];
  integer n, r, c, a, b;
  task automatic apply_beat(input logic clr, input logic en,
                            input logic [31:0] av, input logic [31:0] bv);
    begin
      @(negedge clk);
      clear=clr; mac_en=en; a_vec=av; b_vec=bv;
      @(posedge clk);
      for (integer rr=0; rr<4; rr=rr+1)
        for (integer cc=0; cc<4; cc=cc+1) begin
          if (clr) exp_acc[rr][cc]=0;
          else if (en) begin
            a=$signed(av[rr*8 +: 8]);
            b=$signed(bv[cc*8 +: 8]);
            exp_acc[rr][cc]=exp_acc[rr][cc]+a*b;
          end
        end
      #1;
      for (integer rr=0; rr<4; rr=rr+1)
        for (integer cc=0; cc<4; cc=cc+1)
          if ($signed(acc_bus[32*(4*rr+cc) +: 32]) !== exp_acc[rr][cc])
            $fatal(1,"MAC mismatch r=%0d c=%0d expected=%0d got=%0d",
                   rr,cc,exp_acc[rr][cc],$signed(acc_bus[32*(4*rr+cc) +: 32]));
    end
  endtask
  initial begin
    for (r=0;r<4;r=r+1) for(c=0;c<4;c=c+1) exp_acc[r][c]=0;
    repeat(3) @(negedge clk);
    rst_n=1;
    apply_beat(1'b1,1'b0,32'd0,32'd0);
    // +127/-128 limit products, then a stall, then clear-vs-enable priority.
    apply_beat(1'b0,1'b1,32'h7f8080ff,32'h807f017f);
    apply_beat(1'b0,1'b0,32'hffffffff,32'hffffffff);
    apply_beat(1'b0,1'b1,32'h80808080,32'h80808080);
    apply_beat(1'b1,1'b1,32'h01010101,32'h01010101);
    for (n=0;n<120;n=n+1) begin
      // 16-bit random chunks: deterministic arithmetic checks, not unconstrained X.
      apply_beat(1'b0, (n%7)!=0, $random, $random);
    end
    $display("PASS MAC_SMOKE directed + 120 random/stall beats");
    $finish;
  end
endmodule
