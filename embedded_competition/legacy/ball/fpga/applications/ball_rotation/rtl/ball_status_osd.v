`timescale 1ns / 1ps
// 五乘七字模，每点放大两倍；每组四像素共享字符查询。
module ball_status_osd #(parameter C_ROTATION=0)(
    input i_clk,
    input i_rstn,
    input [95:0] i_rgb,
    input i_valid,
    input i_sof,
    input i_eol,
    input i_eof,
    input [11:0] i_x,
    input [11:0] i_y,
    input i_count_mode,
    input i_strict,
    input i_face_unlocked,
    input i_face_busy,
    input i_face_fault,
    input [1:0] i_face_confirmed,
    input i_rotation_enable,
    input [2:0] i_rotation_status,
    input [3:0] i_rotation_reason,
    input i_rotation_angle_valid,
    input i_rotation_rpm_valid,
    input i_rotation_partial,
    input i_rotation_negative,
    input [31:0] i_rotation_rpm_bcd,
    input [15:0] i_rotation_angle_bcd,
    input [19:0] i_rotation_net_bcd,
    input [39:0] i_rotation_cw_bcd,
    input [39:0] i_rotation_ccw_bcd,
    input [47:0] i_camera_status,
    input [3:0] i_diag_count,
    input [3:0] i_diag_reject,
    input [15:0] i_diag_width_bcd,
    input [15:0] i_diag_height_bcd,
    input [27:0] i_diag_area_bcd,
    input [11:0] i_diag_fill_bcd,
    input [39:0] i_red_bcd,
    input [39:0] i_green_bcd,
    input [39:0] i_yellow_bcd,
    input [43:0] i_total_bcd,
    input [15:0] i_x_bcd,
    input [15:0] i_y_bcd,
    input [2:0] i_gate_state,
    input [1:0] i_track_status,
    input [2:0] i_reason,
    output [95:0] o_rgb,
    output o_valid,
    output o_sof,
    output o_eol,
    output o_eof
);
    function [34:0] glyph;
        input [6:0] character;
        begin
            case(character)
                43:glyph=35'b00000_00100_00100_11111_00100_00100_00000;
                45:glyph=35'b00000_00000_00000_11111_00000_00000_00000;
                46:glyph=35'b00000_00000_00000_00000_00000_00110_00110;
                37:glyph=35'b11001_11010_00100_01000_10110_00110_00000;
                48:glyph=35'b01110_10001_10011_10101_11001_10001_01110;
                49:glyph=35'b00100_01100_00100_00100_00100_00100_01110;
                50:glyph=35'b01110_10001_00001_00010_00100_01000_11111;
                51:glyph=35'b11110_00001_00001_01110_00001_00001_11110;
                52:glyph=35'b00010_00110_01010_10010_11111_00010_00010;
                53:glyph=35'b11111_10000_10000_11110_00001_00001_11110;
                54:glyph=35'b01110_10000_10000_11110_10001_10001_01110;
                55:glyph=35'b11111_00001_00010_00100_01000_01000_01000;
                56:glyph=35'b01110_10001_10001_01110_10001_10001_01110;
                57:glyph=35'b01110_10001_10001_01111_00001_00001_01110;
                65:glyph=35'b01110_10001_10001_11111_10001_10001_10001;
                66:glyph=35'b11110_10001_10001_11110_10001_10001_11110;
                67:glyph=35'b01111_10000_10000_10000_10000_10000_01111;
                68:glyph=35'b11110_10001_10001_10001_10001_10001_11110;
                69:glyph=35'b11111_10000_10000_11110_10000_10000_11111;
                70:glyph=35'b11111_10000_10000_11110_10000_10000_10000;
                71:glyph=35'b01111_10000_10000_10111_10001_10001_01111;
                72:glyph=35'b10001_10001_10001_11111_10001_10001_10001;
                73:glyph=35'b01110_00100_00100_00100_00100_00100_01110;
                75:glyph=35'b10001_10010_10100_11000_10100_10010_10001;
                76:glyph=35'b10000_10000_10000_10000_10000_10000_11111;
                77:glyph=35'b10001_11011_10101_10101_10001_10001_10001;
                78:glyph=35'b10001_11001_10101_10011_10001_10001_10001;
                79:glyph=35'b01110_10001_10001_10001_10001_10001_01110;
                80:glyph=35'b11110_10001_10001_11110_10000_10000_10000;
                82:glyph=35'b11110_10001_10001_11110_10100_10010_10001;
                83:glyph=35'b01111_10000_10000_01110_00001_00001_11110;
                84:glyph=35'b11111_00100_00100_00100_00100_00100_00100;
                85:glyph=35'b10001_10001_10001_10001_10001_10001_01110;
                87:glyph=35'b10001_10001_10001_10101_10101_10101_01010;
                88:glyph=35'b10001_10001_01010_00100_01010_10001_10001;
                89:glyph=35'b10001_10001_01010_00100_00100_00100_00100;
                61:glyph=35'b00000_00000_11111_00000_11111_00000_00000;
                default:glyph=0;
            endcase
        end
    endfunction
    integer character_column,local_column,glyph_row,lane,pixel_column;
    reg [6:0] dec_character;
    reg [34:0] dec_glyph;
    reg [23:0] dec_ink;
    reg flag_text;
    reg [95:0] reg_rgb;
    reg [3:0] reg_markers;
    reg [34:0] reg_glyph;
    reg [2:0] reg_glyph_row;
    reg [3:0] reg_pixel_offset;
    reg [23:0] reg_ink;
    reg flag_panel;
    reg [95:0] reg_rgb_o;
    reg [3:0] reg_markers_o;
    reg [23:0] pixel;
    // 字符选择仅对一个四像素组求值，数字已由帧间BCD模块准备。
    always @(*)begin
        character_column=(i_x-16) >> 4;
        local_column=0; glyph_row=0; dec_character=32; dec_ink=24'hdce8f0; flag_text=0;
        if(i_y >= 16 && i_y < 30)begin
            flag_text=1; glyph_row=(i_y-16) >> 1;
            case(character_column)
                0:dec_character=66;1:dec_character=65;2:dec_character=76;3:dec_character=76;
                5:dec_character=68;6:dec_character=69;7:dec_character=84;8:dec_character=69;
                9:dec_character=67;10:dec_character=84;11:dec_character=73;12:dec_character=79;13:dec_character=78;
                16:dec_character=i_count_mode ? 67 : 84;
                17:dec_character=i_count_mode ? 79 : 82;
                18:dec_character=i_count_mode ? 85 : 65;
                19:dec_character=i_count_mode ? 78 : 67;
                20:dec_character=i_count_mode ? 84 : 75;
                21:dec_character=i_count_mode ? 50 : 32;
                24:dec_character=71;25:dec_character=65;26:dec_character=77;
                27:dec_character=77;28:dec_character=65;
                32:dec_character=i_count_mode ? 32 : 80;
                33:dec_character=i_count_mode ? 32 : 82;
                34:dec_character=i_count_mode ? 32 : 69;
                35:dec_character=i_count_mode ? 32 : 68;
                42:dec_character=i_strict ? 83 : 78;
                43:dec_character=i_strict ? 84 : 79;
                44:dec_character=82;
                45:dec_character=i_strict ? 73 : 77;
                46:dec_character=i_strict ? 67 : 65;
                47:dec_character=i_strict ? 84 : 76;
                51:dec_character=70;52:dec_character=65;53:dec_character=67;54:dec_character=69;55:dec_character=61;
                56:dec_character=i_face_unlocked ? 79 : 76;
                57:dec_character=i_face_unlocked ? 80 : 79;
                58:dec_character=i_face_unlocked ? 69 : 67;
                59:dec_character=i_face_unlocked ? 78 : 75;
                61:dec_character=67;62:dec_character=61;63:dec_character=48+i_face_confirmed;
                65:dec_character=66;66:dec_character=61;67:dec_character=48+i_face_busy;
                69:dec_character=69;70:dec_character=61;71:dec_character=48+i_face_fault;
                default:begin end
            endcase
        end else if(i_y >= 40 && i_y < 54)begin
            flag_text=1; glyph_row=(i_y-40) >> 1;
            if(character_column < 19)begin
                dec_ink=24'hff4050;
                case(character_column)
                    0:dec_character=82;1:dec_character=69;2:dec_character=68;
                    default:begin
                        if(character_column >= 4 && character_column < 14)begin
                            dec_character=48+i_red_bcd[(13-character_column)*4 +:4];
                        end
                    end
                endcase
            end else if(character_column < 38)begin
                dec_ink=24'h20ef70; local_column=character_column-19;
                case(local_column)
                    0:dec_character=71;1:dec_character=82;2:dec_character=69;3:dec_character=69;4:dec_character=78;
                    default:begin
                        if(local_column >= 6 && local_column < 16)begin dec_character=48+i_green_bcd[(15-local_column)*4 +:4]; end
                    end
                endcase
            end else if(character_column < 57)begin
                dec_ink=24'hffdf20; local_column=character_column-38;
                case(local_column)
                    0:dec_character=89;1:dec_character=69;2:dec_character=76;3:dec_character=76;4:dec_character=79;5:dec_character=87;
                    default:begin
                        if(local_column >= 7 && local_column < 17)begin dec_character=48+i_yellow_bcd[(16-local_column)*4 +:4]; end
                    end
                endcase
            end else begin
                local_column=character_column-57;
                case(local_column)
                    0:dec_character=84;1:dec_character=79;2:dec_character=84;3:dec_character=65;4:dec_character=76;
                    default:begin
                        if(local_column >= 6 && local_column < 17)begin dec_character=48+i_total_bcd[(16-local_column)*4 +:4]; end
                    end
                endcase
            end
        end else if(i_y >= 72 && i_y < 86)begin
            flag_text=1; glyph_row=(i_y-72) >> 1;
            case(character_column)
                0:dec_character=88;1:dec_character=61;
                10:dec_character=89;11:dec_character=61;
                24:dec_character=71;25:dec_character=65;26:dec_character=84;27:dec_character=69;28:dec_character=61;
                29:dec_character=48+i_gate_state;
                34:dec_character=84;35:dec_character=82;36:dec_character=65;37:dec_character=67;38:dec_character=75;39:dec_character=61;
                40:dec_character=48+i_track_status;
                45:dec_character=69;46:dec_character=82;47:dec_character=82;48:dec_character=61;49:dec_character=48+i_reason;
                default:begin
                    if(character_column >= 2 && character_column < 6)begin dec_character=48+i_x_bcd[(5-character_column)*4 +:4]; end
                    else if(character_column >= 12 && character_column < 16)begin dec_character=48+i_y_bcd[(15-character_column)*4 +:4]; end
                end
            endcase
        end
        if(i_y >= 96 && i_y < 110)begin
            flag_text=1;glyph_row=(i_y-96) >> 1;
            case(character_column)
                0:dec_character=70;1:dec_character=80;2:dec_character=83;3:dec_character=61;
                4:dec_character=48+i_camera_status[11:8];5:dec_character=48+i_camera_status[7:4];6:dec_character=48+i_camera_status[3:0];
                8:dec_character=69;9:dec_character=88;10:dec_character=80;11:dec_character=61;
                12:dec_character=48+i_camera_status[27:24];13:dec_character=48+i_camera_status[23:20];
                14:dec_character=48+i_camera_status[19:16];15:dec_character=48+i_camera_status[15:12];
                18:dec_character=71;19:dec_character=61;
                20:dec_character=48+i_camera_status[35:32];21:dec_character=48+i_camera_status[31:28];
                24:dec_character=82;25:dec_character=66;26:dec_character=61;27:dec_character=48+i_camera_status[37:36];
                30:dec_character=87;31:dec_character=66;32:dec_character=61;33:dec_character=48+i_camera_status[39];
                36:dec_character=67;37:dec_character=65;38:dec_character=76;
                default:dec_character=32;
            endcase
            if(i_camera_status[37:36] > 1 && character_column >= 24 && character_column <= 27)begin dec_ink=24'hff4050;end
        end
        if(i_y >= 128 && i_y < 142)begin
            flag_text=1;glyph_row=(i_y-128) >> 1;dec_character=32;
            case(character_column)
                0:dec_character=67;1:dec_character=67;2:dec_character=76;3:dec_character=52;
                5:dec_character=78;6:dec_character=61;7:dec_character=48+i_diag_count;
                9:dec_character=87;10:dec_character=61;
                16:dec_character=72;17:dec_character=61;
                23:dec_character=65;24:dec_character=61;
                33:dec_character=70;34:dec_character=61;38:dec_character=37;
                40:dec_character=82;41:dec_character=61;
                42:dec_character=i_diag_reject < 10 ? 48+i_diag_reject : 55+i_diag_reject;
                default:begin
                    if(character_column >= 11 && character_column < 15)begin dec_character=48+i_diag_width_bcd[(14-character_column)*4 +:4];end
                    else if(character_column >= 18 && character_column < 22)begin dec_character=48+i_diag_height_bcd[(21-character_column)*4 +:4];end
                    else if(character_column >= 25 && character_column < 32)begin dec_character=48+i_diag_area_bcd[(31-character_column)*4 +:4];end
                    else if(character_column >= 35 && character_column < 38)begin dec_character=48+i_diag_fill_bcd[(37-character_column)*4 +:4];end
                end
            endcase
            if(i_diag_reject != 0 && character_column >= 40)begin dec_ink=24'hff4050;end
        end
        if(C_ROTATION && i_rotation_enable && !i_count_mode && i_y >= 144 && i_y < 158)begin
            flag_text=1;glyph_row=(i_y-144) >> 1;dec_character=32;dec_ink=24'h80e8ff;
            case(character_column)
                0:dec_character=82;1:dec_character=79;2:dec_character=84;3:dec_character=61;4:dec_character=48+i_rotation_status;
                6:dec_character=82;7:dec_character=80;8:dec_character=77;9:dec_character=61;
                13:dec_character=46;
                16:dec_character=65;17:dec_character=61;21:dec_character=46;
                24:dec_character=78;25:dec_character=69;26:dec_character=84;27:dec_character=61;
                28:dec_character=i_rotation_negative ? 45 : 43;32:dec_character=46;
                36:dec_character=67;37:dec_character=87;38:dec_character=61;
                50:dec_character=67;51:dec_character=67;52:dec_character=87;53:dec_character=61;
                65:dec_character=80;66:dec_character=61;67:dec_character=48+i_rotation_partial;
                69:dec_character=69;70:dec_character=61;71:dec_character=i_rotation_reason < 10 ? 48+i_rotation_reason : 55+i_rotation_reason;
                default:begin
                    if(character_column >= 10 && character_column <= 12)begin dec_character=i_rotation_rpm_valid ? 48+i_rotation_rpm_bcd[(13-character_column)*4 +:4] : 45;end
                    else if(character_column == 14)begin dec_character=i_rotation_rpm_valid ? 48+i_rotation_rpm_bcd[3:0] : 45;end
                    else if(character_column >= 18 && character_column <= 20)begin dec_character=i_rotation_angle_valid ? 48+i_rotation_angle_bcd[(21-character_column)*4 +:4] : 45;end
                    else if(character_column == 22)begin dec_character=i_rotation_angle_valid ? 48+i_rotation_angle_bcd[3:0] : 45;end
                    else if(character_column >= 29 && character_column <= 31)begin dec_character=48+i_rotation_net_bcd[(33-character_column)*4 +:4];end
                    else if(character_column >= 33 && character_column <= 34)begin dec_character=48+i_rotation_net_bcd[(34-character_column)*4 +:4];end
                    else if(character_column >= 39 && character_column <= 48)begin dec_character=48+i_rotation_cw_bcd[(48-character_column)*4 +:4];end
                    else if(character_column >= 54 && character_column <= 63)begin dec_character=48+i_rotation_ccw_bcd[(63-character_column)*4 +:4];end
                end
            endcase
        end
        if(i_x < 16 || i_x >= 1264 || !flag_text)begin dec_character=32; end
        dec_glyph=glyph(dec_character);
    end
    // 字模查询与像素合成分两级，所有标记同时延迟。
    always @(posedge i_clk or negedge i_rstn)begin
        if(!i_rstn)begin
            reg_rgb<=0; reg_markers<=0; reg_glyph<=0; reg_glyph_row<=0;
            reg_pixel_offset<=0; reg_ink<=0; flag_panel<=0;
            reg_rgb_o<=0; reg_markers_o<=0;
        end else begin
            reg_rgb<=i_rgb; reg_markers<={i_valid,i_sof,i_eol,i_eof};
            reg_glyph<=dec_glyph; reg_glyph_row<=glyph_row; reg_pixel_offset<=i_x[3:0];
            reg_ink<=dec_ink; flag_panel<=i_y < 144 || (C_ROTATION && i_rotation_enable && !i_count_mode && i_y < 160);
            reg_markers_o<=reg_markers;
            for(lane=0;lane<4;lane=lane+1)begin
                pixel=flag_panel ? 24'h101c2a : reg_rgb[95-lane*24 -:24];
                pixel_column=(reg_pixel_offset+lane) >> 1;
                if(flag_panel && pixel_column < 5 && reg_glyph[34-reg_glyph_row*5-pixel_column])begin pixel=reg_ink; end
                reg_rgb_o[95-lane*24 -:24]<=pixel;
            end
        end
    end
    assign o_rgb=reg_rgb_o;
    assign o_valid=reg_markers_o[3];
    assign o_sof=reg_markers_o[2];
    assign o_eol=reg_markers_o[1];
    assign o_eof=reg_markers_o[0];
endmodule
