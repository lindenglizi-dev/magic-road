`timescale 1ns / 1ps
// One outstanding 160-bit read; fixed fourteen-group schema2 layout.
module road_numeric_rom_reader(
    input i_clk,
    input i_rstn,
    input i_request_valid,
    input [12:0]i_request_addr,
    output o_request_ready,
    output o_response_valid,
    output [159:0]o_response_data,
    input i_response_ready,
    output o_fault
);
    localparam [1:0]ST_IDLE=2'd0, ST_WAIT=2'd1, ST_RESPONSE=2'd2, ST_FAULT=2'd3;
    reg [1:0]state_current, state_next;
    reg [12:0]reg_address;
    reg [3:0]cnt_wait;
    reg [159:0]response_data_o;
    wire [159:0]group_data [0:13];
    reg [159:0]reg_pair [0:6];
    reg [159:0]reg_quad [0:3];
    reg [159:0]reg_oct [0:1];
    reg [159:0]reg_selected;
    integer index;
    assign o_request_ready=(state_current == ST_IDLE) && i_rstn;
    assign o_response_valid=(state_current == ST_RESPONSE) && i_rstn;
    assign o_response_data=response_data_o;
    assign o_fault=(state_current == ST_FAULT) && i_rstn;
    always @(*) begin
        state_next=state_current;
        case(state_current)
            ST_IDLE: if(i_request_valid) state_next=(i_request_addr < 13'd7168) ? ST_WAIT : ST_FAULT;
            ST_WAIT: if(cnt_wait == 4'd7) state_next=ST_RESPONSE;
            ST_RESPONSE: if(i_response_ready) state_next=ST_IDLE;
            ST_FAULT: state_next=ST_FAULT;
            default: state_next=ST_FAULT;
        endcase
    end
    always @(posedge i_clk or negedge i_rstn) begin
        if(!i_rstn) state_current<=ST_IDLE;
        else state_current<=state_next;
    end
    always @(posedge i_clk or negedge i_rstn) begin
        if(!i_rstn) begin
            reg_address<=13'd0; cnt_wait<=4'd0; response_data_o<=160'd0;
        end else begin
            if(i_request_valid && o_request_ready) begin reg_address<=i_request_addr; cnt_wait<=4'd0; end
            else if(state_current == ST_WAIT) begin
                cnt_wait<=cnt_wait+4'd1;
                if(cnt_wait == 4'd7) response_data_o<=reg_selected;
            end
        end
    end
    // Address remains locked for the complete group pipeline and response hold.
    always @(posedge i_clk or negedge i_rstn) begin
        if(!i_rstn) begin
            for(index=0; index<7; index=index+1) reg_pair[index]<=160'd0;
            for(index=0; index<4; index=index+1) reg_quad[index]<=160'd0;
            reg_oct[0]<=160'd0; reg_oct[1]<=160'd0; reg_selected<=160'd0;
        end else begin
            for(index=0; index<7; index=index+1)
                reg_pair[index]<=reg_address[9] ? group_data[index*2+1] : group_data[index*2];
            reg_quad[0]<=reg_address[10] ? reg_pair[1] : reg_pair[0];
            reg_quad[1]<=reg_address[10] ? reg_pair[3] : reg_pair[2];
            reg_quad[2]<=reg_address[10] ? reg_pair[5] : reg_pair[4];
            reg_quad[3]<=reg_pair[6];
            reg_oct[0]<=reg_address[11] ? reg_quad[1] : reg_quad[0];
            reg_oct[1]<=reg_address[11] ? reg_quad[3] : reg_quad[2];
            reg_selected<=reg_address[12] ? reg_oct[1] : reg_oct[0];
        end
    end
    road_yolo_numeric_rom_group #(
        .C_LANE_ALPHA_FILE("artifacts/group_00_lane_0.dath"),
        .C_LANE_BETA_FILE("artifacts/group_00_lane_1.dath"),
        .C_LANE_GAMMA_FILE("artifacts/group_00_lane_2.dath"),
        .C_LANE_DELTA_FILE("artifacts/group_00_lane_3.dath")
    ) road_yolo_numeric_rom_group_Inst_alpha(
        .i_clk(i_clk), .i_rstn(i_rstn), .i_word_addr(reg_address[8:0]), .o_word_data(group_data[0])
    );
    road_yolo_numeric_rom_group #(
        .C_LANE_ALPHA_FILE("artifacts/group_01_lane_0.dath"),
        .C_LANE_BETA_FILE("artifacts/group_01_lane_1.dath"),
        .C_LANE_GAMMA_FILE("artifacts/group_01_lane_2.dath"),
        .C_LANE_DELTA_FILE("artifacts/group_01_lane_3.dath")
    ) road_yolo_numeric_rom_group_Inst_beta(
        .i_clk(i_clk), .i_rstn(i_rstn), .i_word_addr(reg_address[8:0]), .o_word_data(group_data[1])
    );
    road_yolo_numeric_rom_group #(
        .C_LANE_ALPHA_FILE("artifacts/group_02_lane_0.dath"),
        .C_LANE_BETA_FILE("artifacts/group_02_lane_1.dath"),
        .C_LANE_GAMMA_FILE("artifacts/group_02_lane_2.dath"),
        .C_LANE_DELTA_FILE("artifacts/group_02_lane_3.dath")
    ) road_yolo_numeric_rom_group_Inst_gamma(
        .i_clk(i_clk), .i_rstn(i_rstn), .i_word_addr(reg_address[8:0]), .o_word_data(group_data[2])
    );
    road_yolo_numeric_rom_group #(
        .C_LANE_ALPHA_FILE("artifacts/group_03_lane_0.dath"),
        .C_LANE_BETA_FILE("artifacts/group_03_lane_1.dath"),
        .C_LANE_GAMMA_FILE("artifacts/group_03_lane_2.dath"),
        .C_LANE_DELTA_FILE("artifacts/group_03_lane_3.dath")
    ) road_yolo_numeric_rom_group_Inst_delta(
        .i_clk(i_clk), .i_rstn(i_rstn), .i_word_addr(reg_address[8:0]), .o_word_data(group_data[3])
    );
    road_yolo_numeric_rom_group #(
        .C_LANE_ALPHA_FILE("artifacts/group_04_lane_0.dath"),
        .C_LANE_BETA_FILE("artifacts/group_04_lane_1.dath"),
        .C_LANE_GAMMA_FILE("artifacts/group_04_lane_2.dath"),
        .C_LANE_DELTA_FILE("artifacts/group_04_lane_3.dath")
    ) road_yolo_numeric_rom_group_Inst_epsilon(
        .i_clk(i_clk), .i_rstn(i_rstn), .i_word_addr(reg_address[8:0]), .o_word_data(group_data[4])
    );
    road_yolo_numeric_rom_group #(
        .C_LANE_ALPHA_FILE("artifacts/group_05_lane_0.dath"),
        .C_LANE_BETA_FILE("artifacts/group_05_lane_1.dath"),
        .C_LANE_GAMMA_FILE("artifacts/group_05_lane_2.dath"),
        .C_LANE_DELTA_FILE("artifacts/group_05_lane_3.dath")
    ) road_yolo_numeric_rom_group_Inst_zeta(
        .i_clk(i_clk), .i_rstn(i_rstn), .i_word_addr(reg_address[8:0]), .o_word_data(group_data[5])
    );
    road_yolo_numeric_rom_group #(
        .C_LANE_ALPHA_FILE("artifacts/group_06_lane_0.dath"),
        .C_LANE_BETA_FILE("artifacts/group_06_lane_1.dath"),
        .C_LANE_GAMMA_FILE("artifacts/group_06_lane_2.dath"),
        .C_LANE_DELTA_FILE("artifacts/group_06_lane_3.dath")
    ) road_yolo_numeric_rom_group_Inst_eta(
        .i_clk(i_clk), .i_rstn(i_rstn), .i_word_addr(reg_address[8:0]), .o_word_data(group_data[6])
    );
    road_yolo_numeric_rom_group #(
        .C_LANE_ALPHA_FILE("artifacts/group_07_lane_0.dath"),
        .C_LANE_BETA_FILE("artifacts/group_07_lane_1.dath"),
        .C_LANE_GAMMA_FILE("artifacts/group_07_lane_2.dath"),
        .C_LANE_DELTA_FILE("artifacts/group_07_lane_3.dath")
    ) road_yolo_numeric_rom_group_Inst_theta(
        .i_clk(i_clk), .i_rstn(i_rstn), .i_word_addr(reg_address[8:0]), .o_word_data(group_data[7])
    );
    road_yolo_numeric_rom_group #(
        .C_LANE_ALPHA_FILE("artifacts/group_08_lane_0.dath"),
        .C_LANE_BETA_FILE("artifacts/group_08_lane_1.dath"),
        .C_LANE_GAMMA_FILE("artifacts/group_08_lane_2.dath"),
        .C_LANE_DELTA_FILE("artifacts/group_08_lane_3.dath")
    ) road_yolo_numeric_rom_group_Inst_iota(
        .i_clk(i_clk), .i_rstn(i_rstn), .i_word_addr(reg_address[8:0]), .o_word_data(group_data[8])
    );
    road_yolo_numeric_rom_group #(
        .C_LANE_ALPHA_FILE("artifacts/group_09_lane_0.dath"),
        .C_LANE_BETA_FILE("artifacts/group_09_lane_1.dath"),
        .C_LANE_GAMMA_FILE("artifacts/group_09_lane_2.dath"),
        .C_LANE_DELTA_FILE("artifacts/group_09_lane_3.dath")
    ) road_yolo_numeric_rom_group_Inst_kappa(
        .i_clk(i_clk), .i_rstn(i_rstn), .i_word_addr(reg_address[8:0]), .o_word_data(group_data[9])
    );
    road_yolo_numeric_rom_group #(
        .C_LANE_ALPHA_FILE("artifacts/group_10_lane_0.dath"),
        .C_LANE_BETA_FILE("artifacts/group_10_lane_1.dath"),
        .C_LANE_GAMMA_FILE("artifacts/group_10_lane_2.dath"),
        .C_LANE_DELTA_FILE("artifacts/group_10_lane_3.dath")
    ) road_yolo_numeric_rom_group_Inst_lambda(
        .i_clk(i_clk), .i_rstn(i_rstn), .i_word_addr(reg_address[8:0]), .o_word_data(group_data[10])
    );
    road_yolo_numeric_rom_group #(
        .C_LANE_ALPHA_FILE("artifacts/group_11_lane_0.dath"),
        .C_LANE_BETA_FILE("artifacts/group_11_lane_1.dath"),
        .C_LANE_GAMMA_FILE("artifacts/group_11_lane_2.dath"),
        .C_LANE_DELTA_FILE("artifacts/group_11_lane_3.dath")
    ) road_yolo_numeric_rom_group_Inst_mu(
        .i_clk(i_clk), .i_rstn(i_rstn), .i_word_addr(reg_address[8:0]), .o_word_data(group_data[11])
    );
    road_yolo_numeric_rom_group #(
        .C_LANE_ALPHA_FILE("artifacts/group_12_lane_0.dath"),
        .C_LANE_BETA_FILE("artifacts/group_12_lane_1.dath"),
        .C_LANE_GAMMA_FILE("artifacts/group_12_lane_2.dath"),
        .C_LANE_DELTA_FILE("artifacts/group_12_lane_3.dath")
    ) road_yolo_numeric_rom_group_Inst_nu(
        .i_clk(i_clk), .i_rstn(i_rstn), .i_word_addr(reg_address[8:0]), .o_word_data(group_data[12])
    );
    road_yolo_numeric_rom_group #(
        .C_LANE_ALPHA_FILE("artifacts/group_13_lane_0.dath"),
        .C_LANE_BETA_FILE("artifacts/group_13_lane_1.dath"),
        .C_LANE_GAMMA_FILE("artifacts/group_13_lane_2.dath"),
        .C_LANE_DELTA_FILE("artifacts/group_13_lane_3.dath")
    ) road_yolo_numeric_rom_group_Inst_xi(
        .i_clk(i_clk), .i_rstn(i_rstn), .i_word_addr(reg_address[8:0]), .o_word_data(group_data[13])
    );
endmodule

