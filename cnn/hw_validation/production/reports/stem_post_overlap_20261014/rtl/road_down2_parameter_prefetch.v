`timescale 1ns / 1ps

// Fixed schema2 down2 fields; one word cache, no duplicate parameter RAM.
module road_down2_parameter_prefetch(
    input i_clk,
    input i_rstn,
    output o_rom_valid,
    output [12:0]o_rom_addr,
    input i_rom_ready,
    input i_rom_valid,
    input [159:0]i_rom_data,
    output o_rom_ready,
    output o_load_valid,
    output [2:0]o_load_kind,
    output [10:0]o_load_addr,
    output signed [31:0]o_load_data,
    input i_load_ready,
    output o_table_valid,
    output [9:0]o_table_addr,
    output signed [15:0]o_table_data,
    input i_table_ready,
    output o_done,
    output o_fault,
    output [31:0]o_cycles
);
    localparam [3:0]ST_FIELD=4'd0, ST_REQUEST=4'd1, ST_WAIT=4'd2;
    localparam [3:0]ST_BYTE=4'd3, ST_EMIT=4'd4, ST_ADVANCE=4'd5;
    localparam [3:0]ST_DONE=4'd6, ST_FAULT=4'd7;
    reg [3:0]state_current, state_next;
    reg [3:0]cnt_field;
    reg [12:0]reg_word_addr;
    reg [4:0]cnt_word_byte;
    reg [10:0]cnt_item, reg_items, reg_base;
    reg [2:0]cnt_item_byte, reg_size, reg_kind;
    reg [159:0]reg_word;
    reg [31:0]reg_assembly, cnt_cycles;
    reg flag_cached;
    reg [12:0]dec_word;
    reg [4:0]dec_byte;
    reg [10:0]dec_items, dec_base;
    reg [2:0]dec_size, dec_kind;
    wire [7:0]selected_byte;
    wire flag_transfer, flag_bad_parameter;
    wire [10:0]destination_addr;
    assign selected_byte = reg_word[cnt_word_byte*8 +: 8];
    assign destination_addr = reg_base + cnt_item;
    assign o_rom_valid = (state_current == ST_REQUEST) && i_rstn;
    assign o_rom_addr = reg_word_addr;
    assign o_rom_ready = (state_current == ST_WAIT) && i_rstn;
    assign flag_bad_parameter = ((reg_kind == 3'd6) && reg_assembly[31]) ||
        ((reg_kind == 3'd7) && (((destination_addr < 11'd40) || (destination_addr >= 11'd42)) ?
                              (reg_assembly > 32'd62) : reg_assembly[31]));
    assign o_load_valid = (state_current == ST_EMIT) && (cnt_field != 4'd12) &&
                          (~flag_bad_parameter) && i_rstn;
    assign o_load_kind = reg_kind;
    assign o_load_addr = destination_addr;
    assign o_load_data = ((reg_kind == 3'd2) || (reg_kind == 3'd4)) ?
                         {{24{reg_assembly[7]}}, reg_assembly[7:0]} : reg_assembly;
    assign o_table_valid = (state_current == ST_EMIT) && (cnt_field == 4'd12) && i_rstn;
    assign o_table_addr = cnt_item[9:0];
    assign o_table_data = reg_assembly[15:0];
    assign flag_transfer = (o_load_valid && i_load_ready) || (o_table_valid && i_table_ready);
    assign o_done = (state_current == ST_DONE) && i_rstn;
    assign o_fault = (state_current == ST_FAULT) && i_rstn;
    assign o_cycles = cnt_cycles;

    always @(*) begin
        dec_word=13'd0; dec_byte=5'd0; dec_items=11'd0;
        dec_size=3'd0; dec_kind=3'd0; dec_base=11'd0;
        case(cnt_field)
            4'd0: begin dec_word=13'd29; dec_byte=5'd1; dec_items=11'd144; dec_size=3'd1; dec_kind=3'd2; dec_base=11'd0; end
            4'd1: begin dec_word=13'd36; dec_byte=5'd5; dec_items=11'd16; dec_size=3'd4; dec_kind=3'd3; dec_base=11'd0; end
            4'd2: begin dec_word=13'd43; dec_byte=5'd14; dec_items=11'd384; dec_size=3'd1; dec_kind=3'd4; dec_base=11'd0; end
            4'd3: begin dec_word=13'd62; dec_byte=5'd18; dec_items=11'd24; dec_size=3'd4; dec_kind=3'd5; dec_base=11'd0; end
            4'd4: begin dec_word=13'd39; dec_byte=5'd9; dec_items=11'd16; dec_size=3'd4; dec_kind=3'd6; dec_base=11'd0; end
            4'd5: begin dec_word=13'd67; dec_byte=5'd14; dec_items=11'd24; dec_size=3'd4; dec_kind=3'd6; dec_base=11'd16; end
            4'd6: begin dec_word=13'd42; dec_byte=5'd13; dec_items=11'd16; dec_size=3'd1; dec_kind=3'd7; dec_base=11'd0; end
            4'd7: begin dec_word=13'd72; dec_byte=5'd10; dec_items=11'd24; dec_size=3'd1; dec_kind=3'd7; dec_base=11'd16; end
            4'd8: begin dec_word=13'd43; dec_byte=5'd9; dec_items=11'd1; dec_size=3'd4; dec_kind=3'd7; dec_base=11'd40; end
            4'd9: begin dec_word=13'd73; dec_byte=5'd14; dec_items=11'd1; dec_size=3'd4; dec_kind=3'd7; dec_base=11'd41; end
            4'd10: begin dec_word=13'd43; dec_byte=5'd13; dec_items=11'd1; dec_size=3'd1; dec_kind=3'd7; dec_base=11'd42; end
            4'd11: begin dec_word=13'd73; dec_byte=5'd18; dec_items=11'd1; dec_size=3'd1; dec_kind=3'd7; dec_base=11'd43; end
            4'd12: begin dec_word=13'd6795; dec_byte=5'd14; dec_items=11'd1024; dec_size=3'd2; dec_kind=3'd0; dec_base=11'd0; end
            default: begin dec_items=11'd0; end
        endcase
    end
    always @(*) begin
        state_next=state_current;
        case(state_current)
            ST_FIELD: state_next=(dec_items == 11'd0) ? ST_FAULT : ST_REQUEST;
            ST_REQUEST: if(i_rom_ready) state_next=ST_WAIT;
            ST_WAIT: if(i_rom_valid) state_next=ST_BYTE;
            ST_BYTE: begin
                if(cnt_item_byte + 3'd1 == reg_size) state_next=ST_EMIT;
                else if(cnt_word_byte == 5'd19) state_next=ST_REQUEST;
            end
            ST_EMIT: begin
                if((cnt_field != 4'd12) && flag_bad_parameter) state_next=ST_FAULT;
                else if(flag_transfer) state_next=ST_ADVANCE;
            end
            ST_ADVANCE: begin
                if(cnt_item + 11'd1 == reg_items)
                    state_next=(cnt_field == 4'd12) ? ST_DONE : ST_FIELD;
                else state_next=flag_cached ? ST_BYTE : ST_REQUEST;
            end
            ST_DONE: state_next=ST_DONE;
            ST_FAULT: state_next=ST_FAULT;
            default: state_next=ST_FAULT;
        endcase
    end
    always @(posedge i_clk or negedge i_rstn) begin
        if(!i_rstn) state_current<=ST_FIELD;
        else state_current<=state_next;
    end
    always @(posedge i_clk or negedge i_rstn) begin
        if(!i_rstn) begin
            cnt_field<=4'd0; reg_word_addr<=13'd0; cnt_word_byte<=5'd0;
            cnt_item<=11'd0; reg_items<=11'd0; reg_base<=11'd0;
            cnt_item_byte<=3'd0; reg_size<=3'd0; reg_kind<=3'd0;
            reg_word<=160'd0; reg_assembly<=32'd0; flag_cached<=1'b0;
            cnt_cycles<=32'd0;
        end else begin
            if((state_current != ST_DONE) && (state_current != ST_FAULT)) cnt_cycles<=cnt_cycles+32'd1;
            case(state_current)
                ST_FIELD: begin
                    reg_word_addr<=dec_word; cnt_word_byte<=dec_byte;
                    reg_items<=dec_items; reg_base<=dec_base; reg_size<=dec_size;
                    reg_kind<=dec_kind; cnt_item<=11'd0; cnt_item_byte<=3'd0;
                    reg_assembly<=32'd0; flag_cached<=1'b0;
                end
                ST_WAIT: if(i_rom_valid) begin reg_word<=i_rom_data; flag_cached<=1'b1; end
                ST_BYTE: begin
                    case(cnt_item_byte)
                        3'd0: reg_assembly[7:0]<=selected_byte;
                        3'd1: reg_assembly[15:8]<=selected_byte;
                        3'd2: reg_assembly[23:16]<=selected_byte;
                        3'd3: reg_assembly[31:24]<=selected_byte;
                        default: reg_assembly<=32'd0;
                    endcase
                    cnt_item_byte<=cnt_item_byte+3'd1;
                    if(cnt_word_byte == 5'd19) begin
                        cnt_word_byte<=5'd0; reg_word_addr<=reg_word_addr+13'd1; flag_cached<=1'b0;
                    end else cnt_word_byte<=cnt_word_byte+5'd1;
                end
                ST_ADVANCE: begin
                    reg_assembly<=32'd0; cnt_item_byte<=3'd0;
                    if(cnt_item+11'd1 == reg_items) cnt_field<=cnt_field+4'd1;
                    else cnt_item<=cnt_item+11'd1;
                end
                default: ; // No register update outside the listed states.
            endcase
        end
    end
endmodule
