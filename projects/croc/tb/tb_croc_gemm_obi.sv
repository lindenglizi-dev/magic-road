`timescale 1ns/1ps
module tb_croc_gemm_obi;
  import croc_pkg::*;
  logic clk_i=0, rst_ni=0;
  always #5 clk_i=~clk_i;
  sbr_obi_req_t req;
  sbr_obi_rsp_t rsp;
  croc_gemm_obi dut(.clk_i,.rst_ni,.obi_req_i(req),.obi_rsp_o(rsp));
  localparam logic [31:0] BASE=32'h2000_1000;
  logic [31:0] a[0:3], b[0:3];
  integer transactions=0, polls=0;
  task automatic transact(input logic we,
                          input logic [31:0] addr,wdata,
                          input logic [3:0] byte_en,
                          input logic [2:0] txid,
                          input logic expect_err,
                          output logic [31:0] got);
    integer timeout;
    begin
      @(negedge clk_i);
      req.req=1; req.a.addr=addr; req.a.we=we;
      req.a.be=byte_en; req.a.wdata=wdata; req.a.aid=txid;
      timeout=0;
      // Croc accepts only on req && gnt at rising edge.
      while(rsp.gnt!==1'b1 && timeout<30) begin
        @(negedge clk_i); timeout=timeout+1;
      end
      if(timeout==30)$fatal(1,"OBI grant timeout addr=%h",addr);
      @(posedge clk_i);#1;
      if(rsp.rvalid!==1'b1)$fatal(1,"missing OBI response addr=%h",addr);
      if(rsp.r.rid!==txid)$fatal(1,"RID mismatch got=%h expected=%h",rsp.r.rid,txid);
      if(rsp.r.err!==expect_err)$fatal(1,"unexpected OBI error for %h",addr);
      if(rsp.gnt!==1'b0)$fatal(1,"one-outstanding contract violated");
      got=rsp.r.rdata;
      transactions=transactions+1;
      @(negedge clk_i);req.req=0;
      @(posedge clk_i);#1;
      if(rsp.rvalid!==1'b0)$fatal(1,"duplicate OBI response");
    end
  endtask
  task automatic wr(input logic [31:0] off,data);
    logic [31:0] unused;
    begin transact(1'b1,BASE+off,data,4'hf,3'd2,1'b0,unused); end
  endtask
  task automatic rd(input logic [31:0] off, output logic [31:0] data);
    begin transact(1'b0,BASE+off,32'd0,4'hf,3'd5,1'b0,data); end
  endtask
  task automatic run_and_check;
    integer row,col,k,poll_count;
    logic [31:0] data;
    logic signed [31:0] expected;
    begin
      wr(32'h00,32'd1);
      data=0;
      for(poll_count=0;poll_count<15 && !data[1];poll_count=poll_count+1) begin
        rd(32'h04,data);polls=polls+1;
      end
      if(data[2:0]!==3'b010)$fatal(1,"invalid final status=%h",data);
      for(row=0;row<4;row=row+1) begin
        for(col=0;col<4;col=col+1) begin
          expected=0;
          for(k=0;k<4;k=k+1)
            expected=expected+$signed(a[row][8*k+:8])*$signed(b[k][8*col+:8]);
          rd(32'h40+4*(4*row+col),data);
          if($signed(data)!==expected)
            $fatal(1,"C[%0d][%0d] got=%0d want=%0d",row,col,$signed(data),expected);
        end
      end
      rd(32'h04,data);if(data[1]!==1'b1)$fatal(1,"done not sticky");
    end
  endtask
  integer i;
  logic [31:0] d,unused;
  initial begin
    req='0;
    a[0]=32'h00000001;a[1]=32'h00000100;
    a[2]=32'h00010000;a[3]=32'h01000000;
    b[0]=32'hFE030201;b[1]=32'h08070605;
    b[2]=32'h0C0B0A09;b[3]=32'h100F0E0D;
    repeat(3) @(posedge clk_i);
    @(negedge clk_i);rst_ni=1;
    wr(32'h00,32'd2);
    for(i=0;i<4;i=i+1) begin
      wr(32'h10+4*i,a[i]);wr(32'h20+4*i,b[i]);
    end
    rd(32'h10,d);
    if(d!==a[0])$fatal(1,"register readback failed");
    // Invalid byte enables must be an error and MUST NOT change registers.
    transact(1'b1,BASE+32'h10,32'hdeadbeef,4'b0011,3'd3,1'b1,unused);
    rd(32'h10,d);if(d!==a[0])$fatal(1,"partial write corrupted register");
    // Unmapped read must report err rather than alias a valid register.
    transact(1'b0,BASE+32'h80,32'd0,4'hf,3'd4,1'b1,unused);
    // Misaligned transaction must have no side effects.
    transact(1'b1,BASE+32'h11,32'hdeadbeef,4'hf,3'd1,1'b1,unused);
    run_and_check();
    // Start a second job without reset or explicit done clear. Include INT8
    // extrema and a 65536 result to catch sign/accumulator-width mistakes.
    a[0]=32'h80808080;a[1]=32'h7F807F80;
    a[2]=32'hFD0201FF;a[3]=32'h0700FB03;
    b[0]=32'h01FF7F80;b[1]=32'h807FFF80;
    b[2]=32'h7F018080;b[3]=32'hFF807F80;
    for(i=0;i<4;i=i+1) begin
      wr(32'h10+4*i,a[i]);wr(32'h20+4*i,b[i]);
    end
    run_and_check();
    wr(32'h00,32'd2);
    rd(32'h04,d);if(d[1]!==1'b0)$fatal(1,"done clear failed");
    $display("PASS OBI GEMM 2 jobs, 32 golden results, %0d transactions %0d status polls",transactions,polls);
    $finish;
  end
  initial begin #100000; $fatal(1,"watchdog"); end
endmodule
