`timescale 1ns/1ps
module tb_transformer_block;
 localparam integer AW=18, DEPTH=65536, OUTDEPTH=49152;
 logic clk=0;always #5 clk=~clk;
 logic rst_n=0,start=0;
 logic [8:0] cfg_seq_len=0,cfg_dim=0,cfg_hidden_dim=0;
 logic [4:0] cfg_shift_attn=0,cfg_shift_hidden=0;
 logic [AW-1:0] cfg_w1_base=0,cfg_w2_base=0;
 logic [16:0] cfg_scale_q16=0;
 logic [AW-1:0] cfg_x_base=0,cfg_wq_base=0,cfg_wk_base=0,cfg_wv_base=0;
 logic [AW-1:0] cfg_q_base=0,cfg_key_base=0,cfg_v_base=0,cfg_score_base=100;
 logic [4:0] cfg_shift_q=0,cfg_shift_key=0,cfg_shift_v=0;
 wire busy,done,error;
 wire [3:0] x_rd_en,w_rd_en,q_wr_en,key_wr_en,v_wr_en;
 wire [4*AW-1:0] x_rd_addr,w_rd_addr,q_wr_addr,key_wr_addr,v_wr_addr;
 wire [31:0] q_wr_data,key_wr_data,v_wr_data;
 logic [31:0] x_rd_data=0,w_rd_data=0;
 logic [3:0] x_rd_valid=0,w_rd_valid=0;
 wire [3:0] q_rd_en,key_rd_en,v_rd_en,p_rd_en,act_rd_en,hidden_rd_en;
 wire [4*AW-1:0] q_rd_addr,key_rd_addr,v_rd_addr,p_rd_addr,act_rd_addr,hidden_rd_addr;
 logic [31:0] q_rd_data=0,key_rd_data=0,v_rd_data=0,p_rd_data=0,act_rd_data=0,hidden_rd_data=0;
 logic [3:0] q_rd_valid=0,key_rd_valid=0,v_rd_valid=0,p_rd_valid=0,act_rd_valid=0,hidden_rd_valid=0;
 wire score_wr_en,score_rd_en,p_wr_en,o_wr_en,out_valid;
 wire act_wr_en,hidden_wr_en,y_wr_en;
 wire [1:0] act_wr_bank,hidden_wr_bank;
 wire [AW-1:0] act_wr_addr,hidden_wr_addr,y_wr_addr;
 wire signed [7:0] act_wr_data,hidden_wr_data;
 wire signed [31:0] y_wr_data;
 wire [AW-1:0] score_wr_addr,score_rd_addr,p_wr_addr,o_wr_addr,out_addr;
 wire signed [31:0] score_wr_data,o_wr_data,out_raw;
 logic signed [31:0] score_rd_data=0;
 logic score_rd_valid=0;
 wire [1:0] p_wr_bank;
 wire signed [7:0] p_wr_data,out_data;
 wire [2:0] out_phase,dbg_phase;
 wire [3:0] dbg_state;
 wire dbg_gemm_start,dbg_gemm_done;
 transformer_block_top #(.ADDR_W(AW)) dut(.*);
 logic [7:0] xm[0:4*DEPTH-1],wm[0:4*DEPTH-1];
 logic signed [7:0] qm[0:4*DEPTH-1],km[0:4*DEPTH-1];
 logic signed [7:0] vm[0:4*DEPTH-1],pm[0:4*DEPTH-1],am[0:4*DEPTH-1],hm[0:4*DEPTH-1];
 logic signed [31:0] scoremem[0:4095];
 logic signed [31:0] score_expected[0:4095],pv_expected[0:16383];
 logic signed [7:0] p_expected[0:4095],out_expected[0:OUTDEPTH-1];
 logic signed [31:0] raw_expected[0:OUTDEPTH-1],final_expected[0:OUTDEPTH-1];
 logic signed [7:0] act_expected[0:OUTDEPTH-1],hidden_expected[0:OUTDEPTH-1];
 integer L,D,F,scale,sh[0:2],xb,wb[0:2],yb[0:2],asft,hsft,w1base,w2base;
 integer writes=0,scorewrites=0,pwrites=0,owrites=0,vwrites=0,actwrites=0,hiddenwrites=0,ywrites=0,launches=0,cycles=0;
 integer seenO[0:16383],seenP[0:4095],seenS[0:4095];
 integer seenQ[0:OUTDEPTH-1],seenA[0:OUTDEPTH-1],seenH[0:OUTDEPTH-1],seenY[0:OUTDEPTH-1];
 integer i,j,off,idx,bank,addr,fd,nread,timeout=1000000;
 string case_dir;
 genvar lane;
 generate for(lane=0;lane<4;lane=lane+1)begin:g_src
    wire [AW-1:0] xa=x_rd_addr[lane*AW+:AW],wa=w_rd_addr[lane*AW+:AW];
    always @(posedge clk)begin
      if(!rst_n)begin
        x_rd_valid[lane]<=0;w_rd_valid[lane]<=0;
        x_rd_data[lane*8+:8]<=0;w_rd_data[lane*8+:8]<=0;
      end else begin
        x_rd_valid[lane]<=x_rd_en[lane];
        w_rd_valid[lane]<=w_rd_en[lane];
        if(x_rd_en[lane])begin
          if(xa<xb || xa>=xb+((L+3)/4)*D || xa>=DEPTH) $fatal(1,"X read range");
          x_rd_data[lane*8+:8]<=xm[lane*DEPTH+xa];
        end
        if(w_rd_en[lane])begin
          if(dbg_phase==3 || dbg_phase==4 || dbg_phase>6 ||
             (dbg_phase<=2 && (wa<wb[dbg_phase] || wa>=wb[dbg_phase]+((D+3)/4)*D)) ||
             (dbg_phase==5 && (wa<w1base || wa>=w1base+D*((F+3)/4))) ||
             (dbg_phase==6 && (wa<w2base || wa>=w2base+F*((D+3)/4))) || wa>=DEPTH)
              $fatal(1,"W read range phase=%0d",dbg_phase);
          w_rd_data[lane*8+:8]<=wm[lane*DEPTH+wa];
        end
      end
    end
 end endgenerate
 genvar bk;
 generate for(bk=0;bk<4;bk=bk+1)begin:g_banks
    wire [AW-1:0] qr=q_rd_addr[bk*AW+:AW],kr=key_rd_addr[bk*AW+:AW];
    wire [AW-1:0] pr=p_rd_addr[bk*AW+:AW],vr=v_rd_addr[bk*AW+:AW];
    wire [AW-1:0] ar=act_rd_addr[bk*AW+:AW],hr=hidden_rd_addr[bk*AW+:AW];
    wire [AW-1:0] qw=q_wr_addr[bk*AW+:AW],kw=key_wr_addr[bk*AW+:AW];
    wire [AW-1:0] vw=v_wr_addr[bk*AW+:AW];
    always @(posedge clk)begin
      if(!rst_n)begin
        q_rd_valid[bk]<=0;key_rd_valid[bk]<=0;p_rd_valid[bk]<=0;v_rd_valid[bk]<=0;act_rd_valid[bk]<=0;hidden_rd_valid[bk]<=0;
        q_rd_data[bk*8+:8]<=0;key_rd_data[bk*8+:8]<=0;
        p_rd_data[bk*8+:8]<=0;v_rd_data[bk*8+:8]<=0;act_rd_data[bk*8+:8]<=0;hidden_rd_data[bk*8+:8]<=0;
      end else begin
        q_rd_valid[bk]<=q_rd_en[bk];key_rd_valid[bk]<=key_rd_en[bk];
        p_rd_valid[bk]<=p_rd_en[bk];v_rd_valid[bk]<=v_rd_en[bk];act_rd_valid[bk]<=act_rd_en[bk];hidden_rd_valid[bk]<=hidden_rd_en[bk];
        if(act_wr_en && act_wr_bank==bk)begin
          if(act_wr_addr>=((L+3)/4)*D) $fatal(1,"ACT write out of range");
          am[bk*DEPTH+act_wr_addr]<=act_wr_data;
        end
        if(hidden_wr_en && hidden_wr_bank==bk)begin
          if(hidden_wr_addr>=((L+3)/4)*F) $fatal(1,"Hidden write out of range");
          hm[bk*DEPTH+hidden_wr_addr]<=hidden_wr_data;
        end
        if(q_wr_en[bk])begin
          if(qw>=((L+3)/4)*D) $fatal(1,"Q write range");
          qm[bk*DEPTH+qw]<=q_wr_data[bk*8+:8];
        end
        if(key_wr_en[bk])begin
          if(kw>=((L+3)/4)*D) $fatal(1,"Key write range");
          km[bk*DEPTH+kw]<=key_wr_data[bk*8+:8];
        end
        if(v_wr_en[bk])begin
          if(vw>=L*((D+3)/4)) $fatal(1,"V write range");
          vm[bk*DEPTH+vw]<=v_wr_data[bk*8+:8];
        end
        if(act_rd_en[bk])begin
          if(ar>=((L+3)/4)*D) $fatal(1,"ACT read out of range");
          act_rd_data[bk*8+:8]<=am[bk*DEPTH+ar];
        end
        if(hidden_rd_en[bk])begin
          if(hr>=((L+3)/4)*F) $fatal(1,"Hidden read out of range");
          hidden_rd_data[bk*8+:8]<=hm[bk*DEPTH+hr];
        end
        if(q_rd_en[bk])begin
          if(qr>=((L+3)/4)*D) $fatal(1,"Q read range");
          q_rd_data[bk*8+:8]<=qm[bk*DEPTH+qr];
        end
        if(key_rd_en[bk])begin
          if(kr>=((L+3)/4)*D) $fatal(1,"Key read range");
          key_rd_data[bk*8+:8]<=km[bk*DEPTH+kr];
        end
        if(p_rd_en[bk])begin
          if(pr>=((L+3)/4)*L) $fatal(1,"P read range");
          p_rd_data[bk*8+:8]<=pm[bk*DEPTH+pr];
        end
        if(v_rd_en[bk])begin
          if(vr>=L*((D+3)/4)) $fatal(1,"V read range");
          v_rd_data[bk*8+:8]<=vm[bk*DEPTH+vr];
        end
      end
    end
 end endgenerate
 always @(posedge clk)begin
    if(!rst_n)begin score_rd_valid<=0;score_rd_data<=0;end
    else begin
      score_rd_valid<=score_rd_en;
      if(score_rd_en)begin
        if(score_rd_addr<100 || score_rd_addr>=100+L*L) $fatal(1,"Score rd range");
        score_rd_data<=scoremem[score_rd_addr-100];
      end
    end
 end
 always @(posedge clk) if(rst_n)begin
    cycles=cycles+1;
    if(cycles>timeout) $fatal(1,"TIMEOUT phase=%0d state=%0d",dbg_phase,dbg_state);
    if(error) $fatal(1,"DUT error phase=%0d state=%0d",dbg_phase,dbg_state);
    if(dbg_gemm_start)begin
       if(dbg_phase!==launches) $fatal(1,"GEMM launch order exp=%0d got=%0d",launches,dbg_phase);
       launches=launches+1;
    end
    if(out_valid)begin
       if(out_phase>2) $fatal(1,"QKV output phase");
       off=out_addr-yb[out_phase];
       idx=out_phase*L*D+off;
       if(off<0 || off>=L*D || seenQ[idx]!=0) $fatal(1,"QKV duplicate/range idx=%0d",idx);
       if(out_raw!==raw_expected[idx] || out_data!==out_expected[idx])
          $fatal(1,"QKV mismatch phase=%0d off=%0d got=%0d exp=%0d",out_phase,off,out_data,out_expected[idx]);
       seenQ[idx]=1;writes=writes+1;
    end
    if(score_wr_en)begin
       off=score_wr_addr-100;
       if(off<0 || off>=L*L || seenS[off]!=0) $fatal(1,"Score duplicate/range");
       if(score_wr_data!==score_expected[off]) $fatal(1,"Score mismatch off=%0d",off);
       seenS[off]=1;scorewrites=scorewrites+1;
       scoremem[off]<=score_wr_data;
    end
    if(p_wr_en)begin
       idx=p_wr_bank*DEPTH+p_wr_addr;
       if(p_wr_addr>=((L+3)/4)*L || idx>=4*DEPTH) $fatal(1,"P write invalid");
       pm[idx]<=p_wr_data;
       pwrites=pwrites+1;
    end
    if(act_wr_en)begin
       off=(act_wr_addr/D)*4+act_wr_bank;
       addr=act_wr_addr%D;
       idx=off*D+addr;
       if(off>=L || addr>=D || idx>=OUTDEPTH || seenA[idx]!=0) $fatal(1,"ACT duplicate/range");
       if(act_wr_data!==act_expected[idx]) $fatal(1,"ACT mismatch idx=%0d",idx);
       seenA[idx]=1;actwrites=actwrites+1;
    end
    if(hidden_wr_en)begin
       off=(hidden_wr_addr/F)*4+hidden_wr_bank;
       addr=hidden_wr_addr%F;
       idx=off*F+addr;
       if(off>=L || addr>=F || idx>=OUTDEPTH || seenH[idx]!=0) $fatal(1,"Hidden duplicate/range");
       if(hidden_wr_data!==hidden_expected[idx]) $fatal(1,"Hidden mismatch idx=%0d",idx);
       seenH[idx]=1;hiddenwrites=hiddenwrites+1;
    end
    if(y_wr_en)begin
       if(y_wr_addr>=L*D || seenY[y_wr_addr]!=0) $fatal(1,"Y duplicate/range");
       if(y_wr_data!==final_expected[y_wr_addr]) $fatal(1,"Y mismatch addr=%0d got=%0d expected=%0d",y_wr_addr,y_wr_data,final_expected[y_wr_addr]);
       seenY[y_wr_addr]=1;ywrites=ywrites+1;
    end
    if(o_wr_en)begin
       if(o_wr_addr>=L*D || seenO[o_wr_addr]!=0) $fatal(1,"O duplicate/range");
       if(o_wr_data!==pv_expected[o_wr_addr]) $fatal(1,"O mismatch addr=%0d got=%0d exp=%0d",o_wr_addr,o_wr_data,pv_expected[o_wr_addr]);
       seenO[o_wr_addr]=1;owrites=owrites+1;
    end
    for(integer k=0;k<4;k=k+1)if(v_wr_en[k])vwrites=vwrites+1;
 end
 initial begin
   if(!$value$plusargs("CASE=%s",case_dir))case_dir="vectors/demo";
   fd=$fopen({case_dir,"/config.txt"},"r");
   if(fd==0)$fatal(1,"Missing config file");
   nread=$fscanf(fd,"%d %d %d %d %d %d %d %d %d %d %d %d",L,D,sh[0],sh[1],sh[2],xb,wb[0],wb[1],wb[2],yb[0],yb[1],yb[2]);
   $fclose(fd);
   if(nread!=12) $fatal(1,"Bad config");
   fd=$fopen({case_dir,"/ffn_config.txt"},"r");
   if(fd==0)$fatal(1,"Missing FFN config");
   nread=$fscanf(fd,"%d %d %d %d %d",F,asft,hsft,w1base,w2base);
   $fclose(fd);
   if(nread!=5)$fatal(1,"Bad FFN config");
   fd=$fopen({case_dir,"/softmax_scale.txt"},"r");
   nread=$fscanf(fd,"%d",scale);$fclose(fd);
   if(nread!=1) $fatal(1,"Bad softmax scale");
   cfg_seq_len=L;cfg_dim=D;cfg_hidden_dim=F;
   cfg_shift_attn=asft;cfg_shift_hidden=hsft;
   cfg_w1_base=w1base;cfg_w2_base=w2base;
   cfg_scale_q16=scale;
   cfg_x_base=xb;cfg_wq_base=wb[0];cfg_wk_base=wb[1];cfg_wv_base=wb[2];
   cfg_q_base=yb[0];cfg_key_base=yb[1];cfg_v_base=yb[2];
   cfg_shift_q=sh[0];cfg_shift_key=sh[1];cfg_shift_v=sh[2];
   $readmemh({case_dir,"/x_sparse.hex"},xm);
   $readmemh({case_dir,"/weights_sparse.hex"},wm);
   $readmemh({case_dir,"/raw.hex"},raw_expected,0,3*L*D-1);
   $readmemh({case_dir,"/out.hex"},out_expected,0,3*L*D-1);
   $readmemh({case_dir,"/score.hex"},score_expected,0,L*L-1);
   $readmemh({case_dir,"/prob.hex"},p_expected,0,L*L-1);
   $readmemh({case_dir,"/pv.hex"},pv_expected,0,L*D-1);
   $readmemh({case_dir,"/act.hex"},act_expected,0,L*D-1);
   $readmemh({case_dir,"/hidden.hex"},hidden_expected,0,L*F-1);
   $readmemh({case_dir,"/final.hex"},final_expected,0,L*D-1);
   for(i=0;i<3*L*D;i=i+1)seenQ[i]=0;
   for(i=0;i<L*D;i=i+1)begin seenO[i]=0;seenA[i]=0;seenY[i]=0;end
   for(i=0;i<L*F;i=i+1)seenH[i]=0;
   for(i=0;i<L*L;i=i+1)begin seenP[i]=0;seenS[i]=0;end
   for(i=0;i<4*DEPTH;i=i+1)begin qm[i]='x;km[i]='x;vm[i]='x;pm[i]='x;am[i]='x;hm[i]='x;end
   repeat(4)@(negedge clk);rst_n=1;
   @(negedge clk);start=1;
   @(negedge clk);start=0;
   begin:wait_done
      integer t;
      t=0;
      while(!done && t<timeout) begin @(negedge clk);t=t+1;end
      if(!done)$fatal(1,"timeout before DONE");
   end
   if(error || busy || launches!=7 || writes!=3*L*D || scorewrites!=L*L || pwrites!=L*L || owrites!=L*D || vwrites!=L*D || actwrites!=L*D || hiddenwrites!=L*F || ywrites!=L*D)
      $fatal(1,"Count mismatch launches=%0d QKV=%0d Score=%0d P=%0d PV=%0d Vwrites=%0d",launches,writes,scorewrites,pwrites,owrites,vwrites);
   for(i=0;i<L;i=i+1)begin
      for(j=0;j<L;j=j+1)begin
         bank=i%4;addr=(i/4)*L+j;
         if(pm[bank*DEPTH+addr]!==p_expected[i*L+j]) $fatal(1,"P bank mismatch i=%0d j=%0d",i,j);
      end
      for(j=0;j<D;j=j+1)begin
         bank=i%4;addr=(i/4)*D+j;
         if(qm[bank*DEPTH+addr]!==out_expected[i*D+j]) $fatal(1,"Q bank mismatch i=%0d j=%0d",i,j);
         if(km[bank*DEPTH+addr]!==out_expected[L*D+i*D+j]) $fatal(1,"Key bank mismatch i=%0d j=%0d",i,j);
         bank=j%4;addr=i*((D+3)/4)+j/4;
         if(vm[bank*DEPTH+addr]!==out_expected[2*L*D+i*D+j]) $fatal(1,"V bank mismatch i=%0d j=%0d",i,j);
      end
   end
   for(i=0;i<L*D;i=i+1)begin
     if(seenO[i]!=1 || seenA[i]!=1 || seenY[i]!=1)$fatal(1,"Missing O/ACT/Y element %0d",i);
   end
   for(i=0;i<L*F;i=i+1)if(seenH[i]!=1)$fatal(1,"Missing Hidden element %0d",i);
   for(i=0;i<L;i=i+1)begin
     for(j=0;j<D;j=j+1)begin
       bank=i%4;addr=(i/4)*D+j;
       if(am[bank*DEPTH+addr]!==act_expected[i*D+j]) $fatal(1,"ACT bank mismatch");
     end
     for(j=0;j<F;j=j+1)begin
       bank=i%4;addr=(i/4)*F+j;
       if(hm[bank*DEPTH+addr]!==hidden_expected[i*F+j]) $fatal(1,"Hidden bank mismatch");
     end
   end
   $display("PASS TRANSFORMER BLOCK case=%0s L=%0d D=%0d F=%0d GEMM=%0d QKV=%0d SCORE=%0d P=%0d PV=%0d ACT=%0d HIDDEN=%0d FINAL=%0d cycles=%0d",case_dir,L,D,F,launches,writes,scorewrites,pwrites,owrites,actwrites,hiddenwrites,ywrites,cycles);
   $finish;
 end
endmodule
