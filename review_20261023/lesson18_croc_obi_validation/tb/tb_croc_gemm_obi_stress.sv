`timescale 1ns/1ps
// Standalone protocol stress test. Uses Croc-compatible type stub, NOT full SoC.
module tb_croc_gemm_obi_stress;
  import croc_pkg::*;
  logic clk_i=0,rst_ni=0;
  always #5 clk_i=~clk_i;
  sbr_obi_req_t req;
  sbr_obi_rsp_t rsp;
  croc_gemm_obi dut(.clk_i,.rst_ni,.obi_req_i(req),.obi_rsp_o(rsp));
  localparam logic [31:0] BASE=32'h20001000;
  integer accepted=0,responses=0;
  always @(posedge clk_i) if(rst_ni) begin
    if(req.req && rsp.gnt) accepted=accepted+1;
    if(rsp.rvalid) responses=responses+1;
  end
  task automatic set_req(input logic wr, input logic [31:0] addr,
      input logic [31:0] wd, input logic [3:0] be, input logic [2:0] id);
    begin
      req.req=1;req.a.we=wr;req.a.addr=addr;req.a.wdata=wd;req.a.be=be;req.a.aid=id;
    end
  endtask
  task automatic transfer(input logic wr,input logic [31:0] addr,
      input logic [31:0] wd,input logic [3:0] be,input logic [2:0] id,
      input logic bad,output logic [31:0] data);
    integer wd_cycles;
    begin
      @(negedge clk_i);set_req(wr,addr,wd,be,id);
      wd_cycles=0;
      while(rsp.gnt!==1'b1)begin
        @(negedge clk_i);wd_cycles=wd_cycles+1;
        if(wd_cycles>10)$fatal(1,"missing grant");
      end
      @(posedge clk_i);#1;
      if(!rsp.rvalid || rsp.r.rid!==id || rsp.r.err!==bad)
        $fatal(1,"response mismatch addr %h id %d",addr,id);
      if(rsp.gnt)$fatal(1,"unexpected grant during response");
      data=rsp.r.rdata;
      @(negedge clk_i);req.req=0;
      @(posedge clk_i);#1;
      if(rsp.rvalid!==0)$fatal(1,"duplicate response");
    end
  endtask
  logic [31:0] data;
  integer i,old_acc,old_rsp;
  initial begin
    req='0;repeat(3)@(negedge clk_i);rst_ni=1;
    // Normal register write/read + repeated read stable.
    transfer(1,BASE+32'h10,32'hFE030201,4'hf,3'd2,0,data);
    transfer(0,BASE+32'h10,0,4'hf,3'd3,0,data);
    if(data!==32'hFE030201)$fatal(1,"readback fail");
    // Address-alias security: invalid absolute base must not touch registers.
    transfer(1,BASE+32'h1000,32'hDEADBEEF,4'hf,3'd4,1,data);
    transfer(0,BASE+32'h10,0,4'hf,3'd5,0,data);
    if(data!==32'hFE030201)$fatal(1,"out-of-range write alias");
    transfer(1,BASE+32'h10,32'hDEADBEEF,4'h7,3'd4,1,data);
    transfer(1,BASE+32'h11,32'hDEADBEEF,4'hf,3'd1,1,data);
    transfer(0,BASE+32'h10,0,4'hf,3'd5,0,data);
    if(data!==32'hFE030201)$fatal(1,"invalid write side effect");
    // Real OBI backpressure: keep second request asserted while grant is low.
    @(negedge clk_i);set_req(1,BASE+32'h14,32'h00010203,4'hf,3'd1);
    if(!rsp.gnt)$fatal(1,"first grant not available");
    @(posedge clk_i);#1;
    if(!rsp.rvalid || rsp.r.rid!==3'd1)$fatal(1,"first response");
    @(negedge clk_i);set_req(1,BASE+32'h18,32'h090A0B0C,4'hf,3'd6);
    // No grant until response is drained; second req remains high.
    if(rsp.gnt)$fatal(1,"grant during outstanding response");
    @(posedge clk_i);#1;
    if(rsp.rvalid || !rsp.gnt)$fatal(1,"no recovery after response");
    @(posedge clk_i);#1;
    if(!rsp.rvalid || rsp.r.rid!==3'd6 || rsp.r.err)$fatal(1,"second response");
    @(negedge clk_i);req.req=0;
    @(posedge clk_i);#1;
    if(rsp.rvalid)$fatal(1,"duplicate second response");
    transfer(0,BASE+32'h14,0,4'hf,3'd2,0,data);
    if(data!==32'h00010203)$fatal(1,"first backpressure write lost");
    transfer(0,BASE+32'h18,0,4'hf,3'd3,0,data);
    if(data!==32'h090A0B0C)$fatal(1,"second backpressure write lost");
    // Busy-time writes are leaf status errors, not OBI transport errors.
    transfer(1,BASE+32'h00,32'd1,4'hf,3'd2,0,data);
    transfer(1,BASE+32'h10,32'hDEADBEEF,4'hf,3'd3,0,data);
    transfer(0,BASE+32'h04,0,4'hf,3'd3,0,data);
    if(!data[2])$fatal(1,"busy write should set sticky leaf error");
    transfer(0,BASE+32'h10,0,4'hf,3'd2,0,data);
    if(data!==32'hFE030201)$fatal(1,"busy-time write changed A");
    transfer(1,BASE+32'h00,32'd2,4'hf,3'd2,0,data);
    transfer(0,BASE+32'h04,0,4'hf,3'd2,0,data);
    if(data[2])$fatal(1,"sticky error not cleared");
    if(accepted!==responses+1 && accepted!==responses)
      $fatal(1,"OBI transaction accounting mismatch");
    $display("PASS STRESS: OBI backpressure, IDs, invalid access, sticky error, accepted=%0d",accepted);
    $finish;
  end
  initial begin #100000;$fatal(1,"STRESS TIMEOUT");end
endmodule
