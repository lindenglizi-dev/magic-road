// Draw up to four tracker boxes on the 1280x720 HDMI stream.
// Tracker coordinates are from the 256x144 analysis image, so each coordinate
// is expanded by five. Pedestrian=green, vehicle=cyan, unknown=magenta.
module road_box_overlay (
    input  wire         clk,
    input  wire         rst_n,
    input  wire         in_vsync,
    input  wire         in_hsync,
    input  wire         in_de,
    input  wire [23:0]  in_rgb,
    input  wire [159:0] tracks,
    output reg          out_vsync,
    output reg          out_hsync,
    output reg          out_de,
    output reg  [23:0]  out_rgb
);
    reg [10:0] x;
    reg [9:0]  y;
    reg de_d, vsync_d;

    wire [39:0] track0 = tracks[39:0];
    wire [39:0] track1 = tracks[79:40];
    wire [39:0] track2 = tracks[119:80];
    wire [39:0] track3 = tracks[159:120];

    // Spell out x5 as shift-plus-add. This keeps simple display scaling in LUTs
    // instead of consuming one hardware multiplier for every box coordinate.
    function [10:0] scale5;
        input [7:0] value;
        begin
            scale5 = {3'b000, value} + {1'b0, value, 2'b00};
        end
    endfunction

    function box_hit;
        input [39:0] t;
        input [10:0] px;
        input [9:0]  py;
        reg [10:0] xmin, xmax;
        reg [9:0] ymin, ymax;
        reg on_vertical, on_horizontal;
        begin
            xmin = scale5(t[34:27]);
            xmax = scale5(t[26:19]) + 4;
            ymin = scale5(t[18:11]);
            ymax = scale5(t[10:3]) + 4;
            on_vertical = ((px >= xmin) && (px <= xmin + 2)) ||
                          ((px <= xmax) && (px + 2 >= xmax));
            on_horizontal = ((py >= ymin) && (py <= ymin + 2)) ||
                            ((py <= ymax) && (py + 2 >= ymax));
            box_hit = t[39] && t[38] && t[37] &&
                      (px >= xmin) && (px <= xmax) &&
                      (py >= ymin) && (py <= ymax) &&
                      (on_vertical || on_horizontal);
        end
    endfunction

    function [23:0] class_color;
        input [1:0] class_code;
        begin
            case (class_code)
                2'd1: class_color = 24'h00ff00;
                2'd2: class_color = 24'h00ffff;
                default: class_color = 24'hff00ff;
            endcase
        end
    endfunction

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            x <= 11'd0;
            y <= 10'd0;
            de_d <= 1'b0;
            vsync_d <= 1'b0;
            out_vsync <= 1'b0;
            out_hsync <= 1'b0;
            out_de <= 1'b0;
            out_rgb <= 24'd0;
        end else begin
            de_d <= in_de;
            vsync_d <= in_vsync;
            out_vsync <= in_vsync;
            out_hsync <= in_hsync;
            out_de <= in_de;
            out_rgb <= in_rgb;

            if (in_vsync && !vsync_d) begin
                x <= 11'd0;
                y <= 10'd0;
            end else if (in_de) begin
                x <= x + 1'b1;
            end else if (de_d) begin
                x <= 11'd0;
                y <= y + 1'b1;
            end

            if (in_de) begin
                if (box_hit(track0, x, y))
                    out_rgb <= class_color(track0[36:35]);
                else if (box_hit(track1, x, y))
                    out_rgb <= class_color(track1[36:35]);
                else if (box_hit(track2, x, y))
                    out_rgb <= class_color(track2[36:35]);
                else if (box_hit(track3, x, y))
                    out_rgb <= class_color(track3[36:35]);
            end
        end
    end
endmodule
