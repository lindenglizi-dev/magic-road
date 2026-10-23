`timescale 1ns/1ps
// Control recovery tests use the real MAC and a registered one-cycle SRAM model.
module tb_gemm_control;
  localparam integer AW=18, WATCHDOG=2000;
  logic clk=0;
  always #5 clk=~clk;
  logic rst_n=0,start=0;
  logic [8:0] m_dim=0,n_dim=0,k_dim=0;
  logic b_src_transposed=0;
  wire [3:0] a_rd_en,b_rd_en;
  wire [4*AW-1:0] a_rd_addr,b_rd_addr;
  logic [31:0] a_rd_data=0,b_rd_data=0;
  logic [3:0] a_rd_valid=0,b_rd_valid=0;
  wire c_wr_en,busy,done,bad_dim,mem_protocol_error;
  wire [8:0] c_wr_row,c_wr_col;
  wire [AW-1:0] c_wr_addr;
  wire signed [31:0] c_wr_data;
  wire [31:0] cycles_total,cycles_load,cycles_mac,cycles_store,cycles_overlap,cycles_wait_data;
  wire [8:0] dbg_tile_m,dbg_tile_n,dbg_tile_k;
  wire [2:0] dbg_state;
  wire [1:0] dbg_load_state;
  wire dbg_load_bank,dbg_mac_bank;
  tiled_gemm_4x4_banked_compact #(.ADDR_W(AW)) dut(.*);

  integer seen[0:34];
  integer writes=0,done_count=0,completed_jobs=0,aborted_jobs=0,invalid_jobs=0;
  integer bank,addr,row,col,kk,groups,expected_value,index,sum,t,i;
  integer numeric_outputs=0,baseline_cycles=0,elapsed;
  logic active=0,previous_done=0,corrupt;

  function automatic integer a_value(input integer r,input integer k);
    a_value=2*r-k-5;
  endfunction
  function automatic integer b_value(input integer k,input integer c);
    b_value=k+3*c-6;
  endfunction

  // Address decoding is independent of DUT state and buffer indices.
  always @(posedge clk) begin
    if (!rst_n) begin
      a_rd_valid<=0;b_rd_valid<=0;
      a_rd_data<=0;b_rd_data<=0;
      previous_done=0;
    end else begin
      if ((^{busy,done,bad_dim,mem_protocol_error,c_wr_en,a_rd_en,b_rd_en})===1'bx)
        $fatal(1,"GEMM_CONTROL unknown control");
      a_rd_valid<=a_rd_en;b_rd_valid<=b_rd_en;
      if (!active && ((|a_rd_en) || (|b_rd_en) || c_wr_en || done || busy))
        $fatal(1,"GEMM_CONTROL activity without accepted job");
      if ((|a_rd_en) || (|b_rd_en) || c_wr_en)
        if (busy!==1'b1) $fatal(1,"GEMM_CONTROL memory access without busy");
      if (active && busy && (bad_dim!==1'b0 || mem_protocol_error!==1'b0))
        $fatal(1,"GEMM_CONTROL error on legal job");
      for (bank=0;bank<4;bank=bank+1) begin
        if (a_rd_en[bank]) begin
          addr=a_rd_addr[bank*AW+:AW];
          row=(addr/k_dim)*4+bank;kk=addr%k_dim;
          if ((^addr)===1'bx || row>=m_dim) $fatal(1,"GEMM_CONTROL A address");
          a_rd_data[bank*8+:8]<=a_value(row,kk);
        end
        if (b_rd_en[bank]) begin
          groups=(n_dim+3)/4;
          addr=b_rd_addr[bank*AW+:AW];
          kk=addr/groups;col=(addr%groups)*4+bank;
          if ((^addr)===1'bx || kk>=k_dim || col>=n_dim)
            $fatal(1,"GEMM_CONTROL B address");
          b_rd_data[bank*8+:8]<=b_value(kk,col);
        end
      end
      if (c_wr_en) begin
        if ((^{c_wr_row,c_wr_col,c_wr_addr,c_wr_data})===1'bx ||
            c_wr_row>=m_dim || c_wr_col>=n_dim)
          $fatal(1,"GEMM_CONTROL unknown/out-of-range output");
        index=c_wr_row*n_dim+c_wr_col;
        if (c_wr_addr!==index || seen[index]!=0)
          $fatal(1,"GEMM_CONTROL duplicate/wrong output address");
        sum=0;
        for (kk=0;kk<k_dim;kk=kk+1)
          sum=sum+a_value(c_wr_row,kk)*b_value(kk,c_wr_col);
        expected_value=sum;
        if (corrupt && numeric_outputs==0) expected_value=expected_value+1;
        if (c_wr_data!==expected_value)
          $fatal(1,"GEMM_CONTROL numeric row=%0d col=%0d actual=%0d expected=%0d",
                 c_wr_row,c_wr_col,c_wr_data,expected_value);
        seen[index]=1;writes=writes+1;numeric_outputs=numeric_outputs+1;
      end
      if (done) begin
        if (previous_done || busy!==1'b0 || c_wr_en || writes!=m_dim*n_dim)
          $fatal(1,"GEMM_CONTROL early/repeated done");
        done_count=done_count+1;
      end
      previous_done=done;
    end
  end

  task automatic tick;
    begin @(posedge clk);#1;end
  endtask

  task automatic reset_and_check;
    begin
      // Assert between clock edges, including a possible pending SRAM response.
      @(negedge clk);#2;rst_n=0;start=0;active=0;
      #1;
      if ({busy,done,bad_dim,mem_protocol_error,c_wr_en,a_rd_en,b_rd_en}!==12'b0 ||
          {cycles_total,cycles_load,cycles_mac,cycles_store,cycles_overlap,cycles_wait_data}!==192'b0)
        $fatal(1,"GEMM_CONTROL asynchronous reset did not quiesce");
      repeat (2) tick();
      @(negedge clk);rst_n=1;
      repeat (4) begin
        tick();
        if (busy || done || c_wr_en || (|a_rd_en) || (|b_rd_en) || mem_protocol_error)
          $fatal(1,"GEMM_CONTROL stale activity after reset");
      end
    end
  endtask

  task automatic begin_job(input integer m,input integer n,input integer k);
    begin
      @(negedge clk);
      m_dim=m;n_dim=n;k_dim=k;start=1;
      writes=0;done_count=0;active=1;
      for (i=0;i<35;i=i+1) seen[i]=0;
      tick();
      if (busy!==1'b1 || done!==1'b0 || bad_dim!==1'b0 || mem_protocol_error!==1'b0)
        $fatal(1,"GEMM_CONTROL legal start not accepted/flags not cleared");
      @(negedge clk);start=0;
    end
  endtask

  task automatic finish_job;
    begin
      elapsed=0;
      while (done!==1'b1 && elapsed<WATCHDOG) begin tick();elapsed=elapsed+1;end
      if (done!==1'b1 || busy!==1'b0 || writes!=m_dim*n_dim)
        $fatal(1,"GEMM_CONTROL completion timeout/count");
      tick();
      if (done!==1'b0 || done_count!=1) $fatal(1,"GEMM_CONTROL done is not one pulse");
      active=0;
      repeat (4) tick();
      completed_jobs=completed_jobs+1;
    end
  endtask

  task automatic invalid_job(input integer m,input integer n,input integer k);
    begin
      @(negedge clk);m_dim=m;n_dim=n;k_dim=k;start=1;
      tick();
      if (bad_dim!==1'b1 || busy!==1'b0 || done!==1'b0 || cycles_total!==0)
        $fatal(1,"GEMM_CONTROL invalid dimensions accepted");
      @(negedge clk);start=0;
      repeat (4) begin
        tick();
        if (bad_dim!==1'b1) $fatal(1,"GEMM_CONTROL bad_dim not sticky until next start");
      end
      invalid_jobs=invalid_jobs+1;
    end
  endtask

  // phase=0: pending read; phase=1: active MAC; phase=2: partial output stored.
  task automatic wait_phase(input integer phase);
    begin
      t=0;
      while (!((phase==0 && (|a_rd_valid)) ||
               (phase==1 && cycles_mac!=0 && dbg_state==2) ||
               (phase==2 && c_wr_en && writes>0)) && t<WATCHDOG) begin tick();t=t+1;end
      if (t==WATCHDOG || busy!==1'b1) $fatal(1,"GEMM_CONTROL phase not reached");
    end
  endtask

  integer phase;
  initial begin
    corrupt=$test$plusargs("CORRUPT_EXPECTED");
    reset_and_check();
    invalid_job(0,4,8);invalid_job(4,0,8);invalid_job(4,4,0);
    invalid_job(257,4,8);invalid_job(4,257,8);invalid_job(4,4,257);
    begin_job(5,7,8);finish_job();baseline_cycles=cycles_total;
    for (phase=0;phase<3;phase=phase+1) begin
      begin_job(5,7,8);wait_phase(phase);
      // Configurations are live ports: keep all dimensions/layout stable while busy.
      @(negedge clk);start=1;
      tick();
      if (busy!==1'b1 || bad_dim || mem_protocol_error)
        $fatal(1,"GEMM_CONTROL busy start changed status");
      @(negedge clk);start=0;
      finish_job();
      if (cycles_total!==baseline_cycles) $fatal(1,"GEMM_CONTROL busy start restarted task");
    end
    for (phase=0;phase<3;phase=phase+1) begin
      begin_job(5,7,8);wait_phase(phase);
      reset_and_check();aborted_jobs=aborted_jobs+1;
      begin_job(2,3,5);finish_job();
    end
    if (invalid_jobs!=6 || completed_jobs!=7 || aborted_jobs!=3)
      $fatal(1,"GEMM_CONTROL scenario count");
    $display("PASS GEMM_CONTROL invalid=%0d completed=%0d reset_aborts=%0d numeric_outputs=%0d",
             invalid_jobs,completed_jobs,aborted_jobs,numeric_outputs);
    $finish;
  end
  initial begin #500000;$fatal(1,"GEMM_CONTROL global watchdog");end
endmodule
