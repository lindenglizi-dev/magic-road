// Four 16x16 status tiles over the unmodified HDMI image:
// green = object, yellow = event, red = error, blue = frame-buffer reader.
module road_status_overlay (
    input  wire        clk,
    input  wire        rst_n,
    input  wire        in_vsync,
    input  wire        in_hsync,
    input  wire        in_de,
    input  wire [23:0] in_rgb,
    input  wire [2:0]  status,
    input  wire         frame_buffer_seen,
    input  wire [7:0]   frame_buffer_checksum,
    output reg         out_vsync,
    output reg         out_hsync,
    output reg         out_de,
    output reg  [23:0] out_rgb
);
    reg [10:0] x;
    reg [9:0] y;
    reg de_d, vsync_d;
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
            end else if (in_de)
                x <= x + 1'b1;
            else if (de_d) begin
                x <= 11'd0;
                y <= y + 1'b1;
            end
            if (in_de && (y < 16)) begin
                if (x < 16)
                    out_rgb <= status[0] ? 24'h00ff00 : 24'h103010;
                else if (x < 32)
                    out_rgb <= status[1] ? 24'hffff00 : 24'h303010;
                else if (x < 48)
                    out_rgb <= status[2] ? 24'hff0000 : 24'h301010;
                else if (x < 64)
                    out_rgb <= frame_buffer_seen ?
                               {8'h20, 8'h40, frame_buffer_checksum} :
                               24'h101030;
            end
        end
    end
endmodule
