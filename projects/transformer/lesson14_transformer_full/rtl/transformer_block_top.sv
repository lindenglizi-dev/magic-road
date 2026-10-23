`timescale 1ns/1ps
// Lesson12: ONE physical GEMM instance runs Q, Key, V, SCORE, and PV.
// A/weight/x / Q/Key/V/P physical 4-bank SRAMs reside outside this module.
// Score SRAM: independent 32-bit read + write (fixed one-cycle response).
// Read banks: fixed one-cycle response; writes: unconditional acceptance.
// Lesson14: full single-head Attention plus FFN1/FFN2 with ONE GEMM instance.
// Memory has fixed-one-cycle valid response and writes always accept data.
// No Croc/OBI, DDR interface, LayerNorm, residual, bias, or ASIC SRAM macros.
module transformer_block_top #(parameter integer ADDR_W=18) (
    input logic clk, rst_n, start,
    input logic [8:0] cfg_seq_len, cfg_dim, cfg_hidden_dim,
    input logic [4:0] cfg_shift_attn, cfg_shift_hidden,
    input logic [16:0] cfg_scale_q16,
    input logic [ADDR_W-1:0] cfg_x_base,
    input logic [ADDR_W-1:0] cfg_wq_base,cfg_wk_base,cfg_wv_base,
    input logic [ADDR_W-1:0] cfg_q_base,cfg_key_base,cfg_v_base,
    input logic [4:0] cfg_shift_q,cfg_shift_key,cfg_shift_v,
    input logic [ADDR_W-1:0] cfg_score_base,
    input logic [ADDR_W-1:0] cfg_w1_base,cfg_w2_base,
    output logic busy,done,error,
    output logic [3:0] x_rd_en,w_rd_en,
    output logic [4*ADDR_W-1:0] x_rd_addr,w_rd_addr,
    input logic [31:0] x_rd_data,w_rd_data,
    input logic [3:0] x_rd_valid,w_rd_valid,
    output logic [3:0] q_wr_en,key_wr_en,v_wr_en,
    output logic [4*ADDR_W-1:0] q_wr_addr,key_wr_addr,v_wr_addr,
    output logic [31:0] q_wr_data,key_wr_data,v_wr_data,
    output logic [3:0] q_rd_en,key_rd_en,v_rd_en,p_rd_en,
    output logic [4*ADDR_W-1:0] q_rd_addr,key_rd_addr,v_rd_addr,p_rd_addr,
    input logic [31:0] q_rd_data,key_rd_data,v_rd_data,p_rd_data,
    input logic [3:0] q_rd_valid,key_rd_valid,v_rd_valid,p_rd_valid,
    output logic [3:0] act_rd_en,hidden_rd_en,
    output logic [4*ADDR_W-1:0] act_rd_addr,hidden_rd_addr,
    input logic [31:0] act_rd_data,hidden_rd_data,
    input logic [3:0] act_rd_valid,hidden_rd_valid,
    output logic act_wr_en,hidden_wr_en,
    output logic [1:0] act_wr_bank,hidden_wr_bank,
    output logic [ADDR_W-1:0] act_wr_addr,hidden_wr_addr,
    output logic signed [7:0] act_wr_data,hidden_wr_data,
    output logic y_wr_en,
    output logic [ADDR_W-1:0] y_wr_addr,
    output logic signed [31:0] y_wr_data,
    output logic score_wr_en,
    output logic [ADDR_W-1:0] score_wr_addr,
    output logic signed [31:0] score_wr_data,
    output logic score_rd_en,
    output logic [ADDR_W-1:0] score_rd_addr,
    input logic signed [31:0] score_rd_data,
    input logic score_rd_valid,
    output logic p_wr_en,
    output logic [1:0] p_wr_bank,
    output logic [ADDR_W-1:0] p_wr_addr,
    output logic signed [7:0] p_wr_data,
    output logic out_valid,
    output logic [ADDR_W-1:0] out_addr,
    output logic signed [7:0] out_data,
    output logic [2:0] out_phase,
    output logic signed [31:0] out_raw,
    output logic o_wr_en,
    output logic [ADDR_W-1:0] o_wr_addr,
    output logic signed [31:0] o_wr_data,
    output logic [2:0] dbg_phase,
    output logic [3:0] dbg_state,
    output logic dbg_gemm_start,dbg_gemm_done
);
    localparam logic [3:0] IDLE=0, ISSUE=1, WAIT_GEMM=2, DRAIN=3,
       ROW_START=4, ROW_STREAM=5, ROW_WAIT=6, FINISH=7;
    localparam logic [2:0] PH_Q=0, PH_K=1, PH_V=2, PH_SCORE=3, PH_PV=4, PH_FFN1=5, PH_FFN2=6;
    logic [3:0] state;
    logic [2:0] phase;
    logic [8:0] l_q,d_q,f_q;
    logic [4:0] shift_attn_q,shift_hidden_q;
    logic [16:0] scale_q;
    logic [ADDR_W-1:0] x_base_q,w_base_q[0:2],y_base_q[0:2],score_base_q,w1_base_q,w2_base_q;
    logic [4:0] shift_q[0:2];
    logic [6:0] row_q,issued_q,received_q;
    wire [63:0] limit=(64'd1<<ADDR_W);
    wire [63:0] xspan=((64'd0+cfg_seq_len+3)/4)*cfg_dim;
    wire [63:0] wspan=((64'd0+cfg_dim+3)/4)*cfg_dim;
    wire [63:0] yspan=(64'd0+cfg_seq_len)*cfg_dim;
    wire [63:0] sspan=(64'd0+cfg_seq_len)*cfg_seq_len;
    wire [63:0] w1span=(64'd0+cfg_dim)*((64'd0+cfg_hidden_dim+3)/4);
    wire [63:0] w2span=(64'd0+cfg_hidden_dim)*((64'd0+cfg_dim+3)/4);
    wire [63:0] aspan=((64'd0+cfg_seq_len+3)/4)*cfg_dim;
    wire [63:0] hspan=((64'd0+cfg_seq_len+3)/4)*cfg_hidden_dim;
    wire cfg_ok=cfg_seq_len>=1 && cfg_seq_len<=64 && cfg_dim>=1 && cfg_dim<=256
      && cfg_hidden_dim>=1 && cfg_hidden_dim<=256
      && cfg_scale_q16>=1 && cfg_scale_q16<=17'd65536
      && (64'd0+cfg_x_base+xspan<=limit)
      && (64'd0+cfg_wq_base+wspan<=limit)
      && (64'd0+cfg_wk_base+wspan<=limit)
      && (64'd0+cfg_wv_base+wspan<=limit)
      && (64'd0+cfg_q_base+yspan<=limit)
      && (64'd0+cfg_key_base+yspan<=limit)
      && (64'd0+cfg_v_base+yspan<=limit)
      && (64'd0+cfg_score_base+sspan<=limit)
      && (64'd0+cfg_w1_base+w1span<=limit)
      && (64'd0+cfg_w2_base+w2span<=limit)
      && aspan<=limit && hspan<=limit
      && (64'd0+((cfg_seq_len+3)/4)*cfg_dim<=limit)
      && (64'd0+cfg_seq_len*((cfg_dim+3)/4)<=limit)
      && (64'd0+((cfg_seq_len+3)/4)*cfg_seq_len<=limit);
    assign busy=(state!=IDLE);
    assign dbg_state=state;
    assign dbg_phase=phase;
    wire score_mode=(phase==PH_SCORE);
    wire pv_mode=(phase==PH_PV);
    wire projection=(phase<PH_SCORE);
    wire ffn1_mode=(phase==PH_FFN1);
    wire ffn2_mode=(phase==PH_FFN2);
    wire g_start=(state==ISSUE) && !g_busy;
    wire g_busy,g_done,g_bad,g_memerr;
    assign dbg_gemm_start=g_start;
    assign dbg_gemm_done=g_done;
    wire [3:0] a_en,b_en;
    wire [4*ADDR_W-1:0] a_addr,b_addr;
    logic [31:0] a_data,b_data;
    logic [3:0] a_valid,b_valid;
    wire c_valid;
    wire [8:0] c_row,c_col;
    wire [ADDR_W-1:0] c_addr;
    wire signed [31:0] c_raw;
    logic [ADDR_W-1:0] selected_w,selected_y;
    logic [4:0] selected_shift;
    always_comb begin
       selected_w='0;selected_y='0;selected_shift=0;
       case (phase)
           PH_Q:begin selected_w=w_base_q[0];selected_y=y_base_q[0];selected_shift=shift_q[0];end
           PH_K:begin selected_w=w_base_q[1];selected_y=y_base_q[1];selected_shift=shift_q[1];end
           PH_V:begin selected_w=w_base_q[2];selected_y=y_base_q[2];selected_shift=shift_q[2];end
           PH_FFN1:begin selected_w=w1_base_q;end
           PH_FFN2:begin selected_w=w2_base_q;end
           default:begin end
       endcase
       a_data=score_mode?q_rd_data:pv_mode?p_rd_data:ffn1_mode?act_rd_data:ffn2_mode?hidden_rd_data:x_rd_data;
       b_data=score_mode?key_rd_data:pv_mode?v_rd_data:w_rd_data;
       a_valid=score_mode?q_rd_valid:pv_mode?p_rd_valid:ffn1_mode?act_rd_valid:ffn2_mode?hidden_rd_valid:x_rd_valid;
       b_valid=score_mode?key_rd_valid:pv_mode?v_rd_valid:w_rd_valid;
    end
    assign x_rd_en=projection?a_en:4'b0;
    assign w_rd_en=(projection || ffn1_mode || ffn2_mode)?b_en:4'b0;
    assign q_rd_en=score_mode?a_en:4'b0;
    assign key_rd_en=score_mode?b_en:4'b0;
    assign p_rd_en=pv_mode?a_en:4'b0;
    assign act_rd_en=ffn1_mode?a_en:4'b0;
    assign hidden_rd_en=ffn2_mode?a_en:4'b0;
    assign v_rd_en=pv_mode?b_en:4'b0;
    genvar lane;
    generate for(lane=0;lane<4;lane=lane+1) begin:g_addr
       assign x_rd_addr[lane*ADDR_W+:ADDR_W]=x_base_q+a_addr[lane*ADDR_W+:ADDR_W];
       assign w_rd_addr[lane*ADDR_W+:ADDR_W]=selected_w+b_addr[lane*ADDR_W+:ADDR_W];
       assign q_rd_addr[lane*ADDR_W+:ADDR_W]=a_addr[lane*ADDR_W+:ADDR_W];
       assign key_rd_addr[lane*ADDR_W+:ADDR_W]=b_addr[lane*ADDR_W+:ADDR_W];
       assign p_rd_addr[lane*ADDR_W+:ADDR_W]=a_addr[lane*ADDR_W+:ADDR_W];
       assign act_rd_addr[lane*ADDR_W+:ADDR_W]=a_addr[lane*ADDR_W+:ADDR_W];
       assign hidden_rd_addr[lane*ADDR_W+:ADDR_W]=a_addr[lane*ADDR_W+:ADDR_W];
       assign v_rd_addr[lane*ADDR_W+:ADDR_W]=b_addr[lane*ADDR_W+:ADDR_W];
    end endgenerate
    wire [31:0] g_cycles;
    wire [2:0] g_state;
    tiled_gemm_4x4_banked_compact #(.ADDR_W(ADDR_W),.MAX_DIM(256)) u_gemm (
       .clk(clk),.rst_n(rst_n),.start(g_start),
       .m_dim(l_q),.n_dim(score_mode?l_q:ffn1_mode?f_q:d_q),
       .k_dim(pv_mode?l_q:ffn2_mode?f_q:d_q),
       .b_src_transposed(score_mode),
       .a_rd_en(a_en),.a_rd_addr(a_addr),.a_rd_data(a_data),.a_rd_valid(a_valid),
       .b_rd_en(b_en),.b_rd_addr(b_addr),.b_rd_data(b_data),.b_rd_valid(b_valid),
       .c_wr_en(c_valid),.c_wr_row(c_row),.c_wr_col(c_col),
       .c_wr_addr(c_addr),.c_wr_data(c_raw),
       .busy(g_busy),.done(g_done),.bad_dim(g_bad),.mem_protocol_error(g_memerr),
       .cycles_total(g_cycles),.dbg_state(g_state)
    );
    logic [8:0] row_tag_q,col_tag_q;
    always_ff @(posedge clk or negedge rst_n)begin
       if(!rst_n)begin row_tag_q<=0;col_tag_q<=0;end
       else if(c_valid && projection)begin row_tag_q<=c_row;col_tag_q<=c_col;end
    end
    wire [1:0] rb=row_tag_q[1:0];
    wire [ADDR_W-1:0] raddr=(row_tag_q>>2)*d_q+col_tag_q;
    wire [1:0] vb=col_tag_q[1:0];
    wire [ADDR_W-1:0] vaddr=row_tag_q*((d_q+9'd3)>>2)+(col_tag_q>>2);
    wire rq_valid;
    wire [1:0] rq_phase;
    wire [ADDR_W-1:0] rq_addr;
    wire signed [7:0] rq_data;
    wire signed [31:0] rq_raw;
    wire rq_sat;
    requant_shift_sat #(.ADDR_W(ADDR_W)) u_requant(
      .clk(clk),.rst_n(rst_n),.in_valid(c_valid&&projection),
      .in_raw(c_raw),.in_shift(selected_shift),
      .in_addr(selected_y+c_addr),.in_phase(phase[1:0]),
      .out_valid(rq_valid),.out_data(rq_data),.out_addr(rq_addr),
      .out_phase(rq_phase),.out_raw(rq_raw),.out_saturated(rq_sat)
    );
    assign out_valid=rq_valid;
    assign out_phase={1'b0,rq_phase};
    assign out_addr=rq_addr;
    assign out_data=rq_data;
    assign out_raw=rq_raw;
    assign q_wr_data={4{rq_data}};
    assign key_wr_data={4{rq_data}};
    assign v_wr_data={4{rq_data}};
    generate for(lane=0;lane<4;lane=lane+1)begin:g_write
      assign q_wr_en[lane]=rq_valid&&rq_phase==2'd0&&(rb==lane);
      assign key_wr_en[lane]=rq_valid&&rq_phase==2'd1&&(rb==lane);
      assign v_wr_en[lane]=rq_valid&&rq_phase==2'd2&&(vb==lane);
      assign q_wr_addr[lane*ADDR_W+:ADDR_W]=raddr;
      assign key_wr_addr[lane*ADDR_W+:ADDR_W]=raddr;
      assign v_wr_addr[lane*ADDR_W+:ADDR_W]=vaddr;
    end endgenerate
    assign score_wr_en=c_valid&&score_mode;
    assign score_wr_addr=score_base_q+c_addr;
    assign score_wr_data=c_raw;
    assign o_wr_en=c_valid&&pv_mode;
    assign o_wr_addr=c_addr;
    assign o_wr_data=c_raw;
    // PV INT32 -> signed INT8 A-bank image for FFN1.
    // Important: capture address/row/col WITH the corresponding data.
    wire act_valid;
    wire signed [7:0] act_data;
    wire [ADDR_W-1:0] act_addr_tag;
    wire [1:0] act_phase_tag;
    requant_shift_sat #(.ADDR_W(ADDR_W)) u_attn_requant (
       .clk(clk),.rst_n(rst_n),.in_valid(c_valid && pv_mode),
       .in_raw(c_raw),.in_shift(shift_attn_q),
       .in_addr(c_addr),.in_phase(2'd0),
       .out_valid(act_valid),.out_data(act_data),
       .out_addr(act_addr_tag),.out_phase(act_phase_tag),
       .out_raw(),.out_saturated()
    );
    // c_addr is row-major; at FFN input, store data row-banked.
    // Carry explicit row/column to avoid a runtime divider.
    logic [8:0] att_row_q,att_col_q;
    always_ff @(posedge clk or negedge rst_n) begin
        if(!rst_n) begin att_row_q<=0;att_col_q<=0; end
        else if(c_valid && pv_mode) begin att_row_q<=c_row;att_col_q<=c_col; end
    end
    assign act_wr_en=act_valid;
    assign act_wr_bank=att_row_q[1:0];
    assign act_wr_addr=(att_row_q>>2)*d_q+att_col_q;
    assign act_wr_data=act_data;
    // FFN1 INT32 -> ReLU/quant -> Hidden row-bank image for FFN2.
    wire h_valid;
    wire signed [7:0] h_data;
    wire [8:0] h_row,h_col;
    ffn_relu_requant u_ffn_requant (
       .clk(clk),.rst_n(rst_n),.in_valid(c_valid && ffn1_mode),
       .in_raw(c_raw),.in_shift(shift_hidden_q),
       .in_row(c_row),.in_col(c_col),
       .out_valid(h_valid),.out_data(h_data),
       .out_row(h_row),.out_col(h_col)
    );
    assign hidden_wr_en=h_valid;
    assign hidden_wr_bank=h_row[1:0];
    assign hidden_wr_addr=(h_row>>2)*f_q+h_col;
    assign hidden_wr_data=h_data;
    assign y_wr_en=c_valid&&ffn2_mode;
    assign y_wr_addr=c_addr;
    assign y_wr_data=c_raw;
    // After SCORE, read Score SRAM in row-major order into the row Softmax.
    wire sm_start=(state==ROW_START);
    wire sm_ready,sm_busy,sm_done,sm_error,sm_valid,sm_last;
    wire [7:0] sm_data;
    wire [6:0] sm_index;
    wire [2:0] sm_state;
    wire [21:0] sm_sum;
    assign score_rd_en=(state==ROW_STREAM)&&(issued_q<l_q);
    assign score_rd_addr=score_base_q+row_q*l_q+issued_q;
    softmax_row_int32 #(.MAX_LEN(64),.LUT_FILE("rtl/exp_lut_q16.hex")) u_softmax(
       .clk(clk),.rst_n(rst_n),.start(sm_start),
       .seq_len(l_q[6:0]),.scale_q16(scale_q),
       .in_data(score_rd_data),
       .in_valid(score_rd_valid && state==ROW_STREAM),.in_ready(sm_ready),
       .out_data(sm_data),.out_index(sm_index),.out_valid(sm_valid),
       .out_ready(1'b1),.out_last(sm_last),.busy(sm_busy),
       .done(sm_done),.error(sm_error),.dbg_state(sm_state),.dbg_exp_sum(sm_sum)
    );
    wire p_row_done;
    probability_writer #(.ADDR_W(ADDR_W)) u_p_write (
      .clk(clk),.rst_n(rst_n),.seq_len(l_q[6:0]),.row_idx(row_q),
      .in_data(sm_data),.in_index(sm_index),.in_valid(sm_valid),.in_last(sm_last),
      .in_ready(),.wr_en(p_wr_en),.wr_bank(p_wr_bank),
      .wr_addr(p_wr_addr),.wr_data(p_wr_data),.row_done(p_row_done)
    );
    always_ff @(posedge clk or negedge rst_n) begin
      if(!rst_n)begin
         state<=IDLE;phase<=PH_Q;done<=0;error<=0;
         l_q<=0;d_q<=0;f_q<=0;shift_attn_q<=0;shift_hidden_q<=0;scale_q<=0;x_base_q<=0;score_base_q<=0;w1_base_q<=0;w2_base_q<=0;
         w_base_q[0]<=0;w_base_q[1]<=0;w_base_q[2]<=0;
         y_base_q[0]<=0;y_base_q[1]<=0;y_base_q[2]<=0;
         shift_q[0]<=0;shift_q[1]<=0;shift_q[2]<=0;
         row_q<=0;issued_q<=0;received_q<=0;
      end else begin
         done<=0;
         if(g_bad || g_memerr || sm_error) error<=1;
         case(state)
           IDLE: if(start) begin
             error<=!cfg_ok;phase<=PH_Q;
             if(cfg_ok) begin
               l_q<=cfg_seq_len;d_q<=cfg_dim;f_q<=cfg_hidden_dim;scale_q<=cfg_scale_q16;
               shift_attn_q<=cfg_shift_attn;shift_hidden_q<=cfg_shift_hidden;
               w1_base_q<=cfg_w1_base;w2_base_q<=cfg_w2_base;
               x_base_q<=cfg_x_base;score_base_q<=cfg_score_base;
               w_base_q[0]<=cfg_wq_base;w_base_q[1]<=cfg_wk_base;w_base_q[2]<=cfg_wv_base;
               y_base_q[0]<=cfg_q_base;y_base_q[1]<=cfg_key_base;y_base_q[2]<=cfg_v_base;
               shift_q[0]<=cfg_shift_q;shift_q[1]<=cfg_shift_key;shift_q[2]<=cfg_shift_v;
               state<=ISSUE;
             end else done<=1;
           end
           ISSUE: if(!g_busy) state<=WAIT_GEMM;
           WAIT_GEMM: if(g_done) state<=DRAIN;
           DRAIN: if(!(c_valid&&(projection||pv_mode||ffn1_mode)) && !rq_valid && !act_valid && !h_valid) begin
             if(error) begin state<=FINISH;end
             else if(phase==PH_SCORE)begin
                row_q<=0;issued_q<=0;received_q<=0;state<=ROW_START;
             end else if(phase==PH_FFN2)begin
                state<=FINISH;
             end else begin phase<=phase+3'd1;state<=ISSUE;end
           end
           ROW_START:begin issued_q<=0;received_q<=0;state<=ROW_STREAM;end
           ROW_STREAM:begin
             if(score_rd_en) issued_q<=issued_q+7'd1;
             if(score_rd_valid)begin
               if(!sm_ready) error<=1;
               else begin
                  received_q<=received_q+7'd1;
                  if(received_q+7'd1==l_q[6:0]) state<=ROW_WAIT;
               end
             end
           end
           ROW_WAIT: if(sm_done)begin
              if(row_q+7'd1==l_q[6:0])begin phase<=PH_PV;state<=ISSUE;end
              else begin row_q<=row_q+7'd1;state<=ROW_START;end
           end
           FINISH:begin done<=1;state<=IDLE;end
           default:begin state<=IDLE;error<=1;end
         endcase
      end
    end
endmodule
