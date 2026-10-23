`timescale 1ns/1ps
// Independent Python dot products, exact physical requests, and fixed-cycle faults.
module tb_tiled_gemm;
  localparam integer AW=18, DEPTH=512, MAX_OUTPUTS=35, WATCHDOG=20000;
  logic clk=0;
  always #5 clk=~clk;
  logic rst_n=0, start=0;
  logic [8:0] m_dim=0, n_dim=0, k_dim=0;
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

  logic [7:0] a_memory[0:4*DEPTH-1],b_memory[0:4*DEPTH-1];
  logic signed [31:0] expected[0:MAX_OUTPUTS-1];
  integer seen[0:MAX_OUTPUTS-1];
  integer m,n,k,transposed,fault;
  integer writes=0,read_beats=0,a_reads=0,b_reads=0,case_cycles=0;
  integer last_write_cycle=-1,drop_cycle=-1,dropped=0;
  integer case_count,case_index,fd,nread,i,t,numeric_cases=0,fault_cases=0,total_numeric=0;
  integer bank,addr,expected_addr,request_row,request_col,request_k,groups;
  integer output_index;
  logic active=0,previous_done=0,previous_error=0;
  string vector_dir,case_name,case_dir;

  // The SRAM returns registered data at this edge; the DUT samples it next edge.
  // Every request is checked against an independently counted logical tile order.
  always @(posedge clk) begin
    if (!rst_n) begin
      a_rd_valid<=0;b_rd_valid<=0;
      a_rd_data<=0;b_rd_data<=0;
    end else begin
      if ((^{busy,done,bad_dim,mem_protocol_error,c_wr_en,a_rd_en,b_rd_en})===1'bx)
        $fatal(1,"GEMM unknown control signal");
      a_rd_valid<=a_rd_en;
      b_rd_valid<=b_rd_en;
      if (!active && ((|a_rd_en) || (|b_rd_en) || c_wr_en))
        $fatal(1,"GEMM activity outside task");
      if (active) begin
        case_cycles=case_cycles+1;
        if (case_cycles>WATCHDOG) $fatal(1,"GEMM watchdog case=%0s",case_name);
        if (bad_dim!==1'b0) $fatal(1,"GEMM bad_dim on legal dimensions");
        if (fault==0 && mem_protocol_error!==1'b0) $fatal(1,"GEMM unexpected protocol error");
        if (previous_error && !mem_protocol_error) $fatal(1,"GEMM error flag lost before restart");
        previous_error=mem_protocol_error;
        if (dropped!=0 && case_cycles==drop_cycle+2 && !mem_protocol_error)
          $fatal(1,"GEMM missing response not flagged after capture");
        if ((|a_rd_en) || (|b_rd_en)) begin
          if (busy!==1'b1) $fatal(1,"GEMM request without busy");
          groups=(n+3)/4;
          request_row=(read_beats/(k*groups))*4;
          request_col=((read_beats/k)%groups)*4;
          request_k=read_beats%k;
          if (request_row>=m) $fatal(1,"GEMM extra read beat");
          for (bank=0;bank<4;bank=bank+1) begin
            if (a_rd_en[bank] !== ((request_row+bank)<m))
              $fatal(1,"GEMM A lane/zero-fill case=%0s beat=%0d bank=%0d",case_name,read_beats,bank);
            if (b_rd_en[bank] !== ((request_col+bank)<n))
              $fatal(1,"GEMM B lane/zero-fill case=%0s beat=%0d bank=%0d",case_name,read_beats,bank);
            if (a_rd_en[bank]) begin
              addr=a_rd_addr[bank*AW+:AW];
              expected_addr=(request_row/4)*k+request_k;
              if (addr!==expected_addr || addr>=DEPTH)
                $fatal(1,"GEMM A physical address case=%0s got=%0d expected=%0d",case_name,addr,expected_addr);
              if ((^a_memory[bank*DEPTH+addr])===1'bx) $fatal(1,"GEMM missing A vector data");
              a_rd_data[bank*8+:8]<=a_memory[bank*DEPTH+addr];
              a_reads=a_reads+1;
            end
            if (b_rd_en[bank]) begin
              addr=b_rd_addr[bank*AW+:AW];
              expected_addr=transposed ? (request_col/4)*k+request_k
                                       : request_k*groups+request_col/4;
              if (addr!==expected_addr || addr>=DEPTH)
                $fatal(1,"GEMM B physical address case=%0s got=%0d expected=%0d",case_name,addr,expected_addr);
              if ((^b_memory[bank*DEPTH+addr])===1'bx) $fatal(1,"GEMM missing B vector data");
              b_rd_data[bank*8+:8]<=b_memory[bank*DEPTH+addr];
              b_reads=b_reads+1;
            end
          end
          // Drop one needed bank response only; no retry/abort is assumed.
          if (dropped==0 && fault!=0) begin
            if (fault==1) a_rd_valid[0]<=0;
            else b_rd_valid[0]<=0;
            dropped=1;drop_cycle=case_cycles;
          end
          read_beats=read_beats+1;
        end
        if (c_wr_en) begin
          if (busy!==1'b1 || done!==1'b0 || (^c_wr_row)===1'bx || (^c_wr_col)===1'bx || c_wr_row>=m || c_wr_col>=n)
            $fatal(1,"GEMM invalid write metadata");
          output_index=c_wr_row*n+c_wr_col;
          if (c_wr_addr!==output_index || seen[output_index]!=0)
            $fatal(1,"GEMM write duplicate/address case=%0s row=%0d col=%0d",case_name,c_wr_row,c_wr_col);
          if (fault==0 && c_wr_data!==expected[output_index])
            $fatal(1,"GEMM numeric case=%0s index=%0d got=%0d expected=%0d",case_name,output_index,c_wr_data,expected[output_index]);
          seen[output_index]=1;writes=writes+1;last_write_cycle=case_cycles;
        end
      end
      if (done && previous_done) $fatal(1,"GEMM done longer than one cycle");
      if (done && (!active || busy || c_wr_en || writes!=m*n || case_cycles<=last_write_cycle))
        $fatal(1,"GEMM premature/unexpected done");
      previous_done=done;
    end
  end

  initial begin
    if (!$value$plusargs("VECTORS=%s",vector_dir)) vector_dir="../reports/gemm_unit_vectors";
    fd=$fopen({vector_dir,"/cases.txt"},"r");
    if (fd==0) $fatal(1,"GEMM missing vector manifest");
    nread=$fscanf(fd,"%d",case_count);
    if (nread!=1 || case_count!=10) $fatal(1,"GEMM invalid case count");
    repeat(3) @(negedge clk);
    rst_n=1;
    for (case_index=0;case_index<case_count;case_index=case_index+1) begin
      nread=$fscanf(fd,"%s %d %d %d %d %d",case_name,m,n,k,transposed,fault);
      if (nread!=6 || m<1 || m>5 || n<1 || n>7 || k<1 || k>256 || fault<0 || fault>2)
        $fatal(1,"GEMM invalid case config");
      case_dir={vector_dir,"/",case_name};
      // Poison previous task data so failed/truncated loads cannot reuse it.
      for (i=0;i<4*DEPTH;i=i+1) begin a_memory[i]='x;b_memory[i]='x;end
      for (i=0;i<MAX_OUTPUTS;i=i+1) expected[i]='x;
      $readmemh({case_dir,"/a.hex"},a_memory);
      $readmemh({case_dir,"/b.hex"},b_memory);
      $readmemh({case_dir,"/expected.hex"},expected,0,m*n-1);
      for (i=0;i<m*n;i=i+1)
        if ((^expected[i])===1'bx) $fatal(1,"GEMM missing expected vector data");
      for (i=0;i<MAX_OUTPUTS;i=i+1) seen[i]=0;
      writes=0;read_beats=0;a_reads=0;b_reads=0;case_cycles=0;
      last_write_cycle=-1;drop_cycle=-1;dropped=0;previous_error=0;
      m_dim=m;n_dim=n;k_dim=k;b_src_transposed=transposed;
      start=1;
      @(negedge clk);
      start=0;active=1;
      if (busy!==1'b1 || done!==1'b0 || bad_dim!==1'b0 || mem_protocol_error!==1'b0)
        $fatal(1,"GEMM start did not clear status case=%0s",case_name);
      t=0;
      while (!done && t<WATCHDOG) begin
        @(negedge clk);t=t+1;
        if (done!==1'b1 && busy!==1'b1) $fatal(1,"GEMM busy dropped before done");
      end
      if (done!==1'b1) $fatal(1,"GEMM timeout case=%0s",case_name);
      if (busy!==1'b0 || bad_dim!==1'b0 || writes!=m*n || mem_protocol_error!==(fault!=0) || dropped!=(fault!=0))
        $fatal(1,"GEMM final status case=%0s",case_name);
      if (read_beats!=((m+3)/4)*((n+3)/4)*k ||
          a_reads!=m*k*((n+3)/4) || b_reads!=n*k*((m+3)/4))
        $fatal(1,"GEMM read counts case=%0s beats=%0d A=%0d B=%0d",case_name,read_beats,a_reads,b_reads);
      for (i=0;i<m*n;i=i+1) if (seen[i]!=1) $fatal(1,"GEMM missing write index=%0d",i);
      if (fault==0) begin
        numeric_cases=numeric_cases+1;total_numeric=total_numeric+writes;
        $display("PASS GEMM_NUMERIC case=%0s M=%0d N=%0d K=%0d transposed=%0d writes=%0d cycles=%0d",case_name,m,n,k,transposed,writes,case_cycles);
      end else begin
        fault_cases=fault_cases+1;
        $display("PASS GEMM_FAULT case=%0s missing=%0d flagged=1 numeric=NOT_CHECKED",case_name,fault);
      end
      // Observe the entire done pulse, sticky error, and no activity after completion.
      @(negedge clk);
      if (done!==1'b0 || busy!==1'b0 || mem_protocol_error!==(fault!=0)) $fatal(1,"GEMM idle status");
      active=0;
      @(negedge clk);
    end
    $fclose(fd);
    if (numeric_cases!=8 || fault_cases!=2 || total_numeric!=174) $fatal(1,"GEMM suite incomplete");
    $display("PASS GEMM_UNIT cases=%0d numeric=%0d elements=%0d faults=%0d reset_count=1",case_count,numeric_cases,total_numeric,fault_cases);
    $finish;
  end
endmodule
