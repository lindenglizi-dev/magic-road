`timescale 1ns/1ps
// Croc-facing teaching *register block*, NOT an OBI slave yet.
// Local synchronous register-transaction protocol: valid and ready in same
// cycle, reads combinational; upstream OBI adapter must implement gnt/rvalid.
// All offsets are BYTE offsets. A and B are row-major 4x4 signed INT8:
//   A row r = regs[0x10 + 4*r], B row k = regs[0x20 + 4*k]
//   byte lane c in each row contains signed matrix element [r][c].
// Results C[r][c] at 0x40 + 4*(4*r+c), signed INT32.
module gemm_mmio_4x4 (
    input  logic clk,
    input  logic rst_n,
    input  logic reg_valid,
    input  logic reg_write,
    input  logic [11:0] reg_addr,
    input  logic [31:0] reg_wdata,
    output logic reg_ready,
    output logic [31:0] reg_rdata,
    output logic busy,
    output logic done,
    output logic error
);
    localparam logic [1:0] ST_IDLE=2'd0, ST_CLEAR=2'd1, ST_RUN=2'd2;
    logic [1:0] state;
    logic [1:0] k_idx;
    logic [31:0] a_words [0:3];
    logic [31:0] b_words [0:3];
    logic [31:0] avec, bvec;
    wire [511:0] accum;
    wire fire = reg_valid && reg_ready;
    wire [9:0] word_addr = reg_addr[11:2];
    integer r;
    genvar row,col;
    for (row=0; row<4; row=row+1) begin : g_a
        assign avec[row*8+:8] = a_words[row][k_idx*8+:8];
    end
    for (col=0; col<4; col=col+1) begin : g_b
        assign bvec[col*8+:8] = b_words[k_idx][col*8+:8];
    end
    mac_array_4x4 u_mac(
        .clk(clk),.rst_n(rst_n),.clear(state==ST_CLEAR),
        .mac_en(state==ST_RUN),.a_vec(avec),.b_vec(bvec),.acc_bus(accum)
    );
    assign reg_ready = 1'b1; // no write buffering and no stalls in this leaf block
    assign busy = (state != ST_IDLE);
    always_comb begin
        reg_rdata=32'b0;
        case(word_addr)
          10'd0: reg_rdata=32'b0; // CTRL write only
          10'd1: reg_rdata={29'b0,error,done,busy};
          default: begin
            if (word_addr>=10'd4 && word_addr<=10'd7)
                reg_rdata=a_words[word_addr-10'd4];
            else if(word_addr>=10'd8 && word_addr<=10'd11)
                reg_rdata=b_words[word_addr-10'd8];
            else if(word_addr>=10'd16 && word_addr<=10'd31 && done)
                reg_rdata=accum[32*(word_addr-10'd16)+:32];
          end
        endcase
    end
    always_ff @(posedge clk or negedge rst_n) begin
        if(!rst_n) begin
            state<=ST_IDLE; k_idx<=0; done<=0;error<=0;
            for(r=0;r<4;r=r+1) begin a_words[r]<=0; b_words[r]<=0; end
        end else begin
            case(state)
              ST_IDLE: begin end
              ST_CLEAR:begin k_idx<=0; state<=ST_RUN; end
              ST_RUN:begin
                if(k_idx==2'd3) begin
                    state<=ST_IDLE;
                    done<=1'b1;
                end else k_idx<=k_idx+2'd1;
              end
              default:begin state<=ST_IDLE;error<=1'b1;end
            endcase
            if(fire && reg_write) begin
                if (reg_addr[1:0]!=2'b00) error<=1'b1;
                else if(word_addr==10'd0)begin
                    if(reg_wdata[1]) begin done<=0;error<=0;end
                    if(reg_wdata[0]) begin
                        if(state==ST_IDLE)begin
                            done<=0;error<=0;state<=ST_CLEAR;
                        end else error<=1'b1;
                    end
                end else if(word_addr>=10'd4 && word_addr<=10'd7) begin
                    if(state==ST_IDLE) a_words[word_addr-10'd4]<=reg_wdata;
                    else error<=1'b1;
                end else if(word_addr>=10'd8 && word_addr<=10'd11)begin
                    if(state==ST_IDLE) b_words[word_addr-10'd8]<=reg_wdata;
                    else error<=1'b1;
                end else error<=1'b1;
            end
        end
    end
endmodule
