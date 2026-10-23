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
      if(!rsp.rvalid)$fatal(1,"missing OBI response addr=%h",addr);
      if(rsp.r.rid!==txid)$fatal(1,"RID mismatch got=%h expected=%h",rsp.r.rid,txid);
      if(rsp.r.err!==expect_err)$fatal(1,"unexpected OBI error for %h",addr);
      if(rsp.gnt!==1'b0)$fatal(1,"one-outstanding contract violated");
      got=rsp.r.rdata;
      transactions=transactions+1;
      @(negedge clk_i);req.req=0;
      @(posedge clk_i);#1;
      if(rsp.rvalid)$fatal(1,"duplicate OBI response");
    end
  endtask
  task automatic wr(input logic [31:0] off,data);
    logic [31:0] unused;
    begin transact(1'b1,BASE+off,data,4'hf,3'd2,1'b0,unused); end
  endtask
  task automatic rd(input logic [31:0] off, output logic [31:0] data);
    begin transact(1'b0,BASE+off,32'd0,4'hf,3'd5,1'b0,data); end
  endtask
  integer i,j;
  logic [31:0] d,unused;
  logic signed [31:0] expected;
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
    wr(32'h00,32'd1);
    d=0;
    for(i=0;i<15 && !d[1];i=i+1) begin
      rd(32'h04,d);polls=polls+1;
    end
    if(!d[1] || d[0])$fatal(1,"timeout/busy mismatch status=%h",d);
    for(i=0;i<4;i=i+1) begin
      for(j=0;j<4;j=j+1) begin
        rd(32'h40+4*(4*i+j),d);
        expected=$signed({{24{b[i][8*j+7]}},b[i][8*j+:8]});
        if($signed(d)!==expected)$fatal(1,"C[%0d][%0d] got=%0d want=%0d",i,j,$signed(d),expected);
      end
    end
    // done is sticky until clear.
    rd(32'h04,d);if(!d[1])$fatal(1,"done not sticky");
    wr(32'h00,32'd2);
    rd(32'h04,d);if(d[1])$fatal(1,"done clear failed");
    $display("PASS OBI GEMM %0d transactions %0d status polls",transactions,polls);
    $finish;
  end
  initial begin #100000; $fatal(1,"watchdog"); end
endmodule
