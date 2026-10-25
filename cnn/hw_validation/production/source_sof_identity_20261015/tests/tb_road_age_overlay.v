`timescale 1ns / 1ps
// CPU golden pixels cover all 11 cells and every pixel around their perimeter.
module tb_road_age_overlay;
    localparam CASE_COUNT = 16;
    localparam WIDTH = 160;
    localparam HEIGHT = 34;
    reg clk = 0;
    reg rstn = 0;
    reg sof = 0;
    reg vsync = 0;
    reg hsync = 0;
    reg de = 0;
    reg [23:0] rgb = 0;
    reg [63:0] age = 64'hffffffffffffffff;
    reg table_draw_valid = 0;
    wire out_vsync, out_hsync, out_de, draw_permit;
    wire [23:0] out_rgb;
    reg expected_pixels [0:CASE_COUNT*WIDTH*HEIGHT-1];
    reg [63:0] ages [0:CASE_COUNT-1];
    reg [63:0] switched_age;
    reg switch_at_sof = 0;
    reg [23:0] previous_rgb = 0;
    reg previous_vs = 0;
    reg previous_hs = 0;
    reg previous_de = 0;
    reg previous_known = 0;
    reg [23:0] expected_rgb;
    integer frame_index;
    integer x;
    integer y;
    integer pixels_checked = 0;
    integer white_checked = 0;
    integer pass_checked = 0;
    integer sync_checked = 0;
    integer live_off_checked = 0;

    always #6.667 clk = !clk; // Nominal75MHz pixel domain.
    // Model the table active-bank switch on SOF with real NBA ordering.
    always @(posedge clk) begin
        if (switch_at_sof && sof) age <= switched_age;
    end

    road_age_overlay dut (
        .i_clk(clk), .i_rstn(rstn), .i_sof(sof), .i_vsync(vsync),
        .i_hsync(hsync), .i_de(de), .i_rgb(rgb), .i_age_upper_ms(age),
        .i_table_draw_valid(table_draw_valid), .o_vsync(out_vsync),
        .o_hsync(out_hsync), .o_de(out_de), .o_rgb(out_rgb),
        .o_draw_permit(draw_permit)
    );

    task pixel;
        input in_sof;
        input in_vs;
        input in_hs;
        input in_de;
        input [23:0] in_rgb;
        input [23:0] wanted_rgb;
        begin
            @(negedge clk);
            sof = in_sof;
            vsync = in_vs;
            hsync = in_hs;
            de = in_de;
            rgb = in_rgb;
            #1;
            if (previous_known && rstn && {out_vsync,out_hsync,out_de,out_rgb} !== {previous_vs,previous_hs,previous_de,previous_rgb})
                $fatal(1, "pixel outputs changed before registered edge frame=%0d x=%0d y=%0d", frame_index,x,y);
            if (draw_permit !== (rstn && table_draw_valid))
                $fatal(1, "live draw permission differs from input before edge");
            @(posedge clk);
            #1;
            if (rstn) begin
                if ({out_vsync,out_hsync,out_de} !== {in_vs,in_hs,in_de})
                    $fatal(1, "RGB/sync pipeline misaligned frame=%0d x=%0d y=%0d", frame_index,x,y);
                if (out_rgb !== wanted_rgb)
                    $fatal(1, "CPU glyph pixel mismatch frame=%0d age=%0d x=%0d y=%0d got=%h want=%h", frame_index,ages[frame_index],x,y,out_rgb,wanted_rgb);
                previous_rgb = wanted_rgb;
                previous_vs = in_vs;
                previous_hs = in_hs;
                previous_de = in_de;
                previous_known = 1;
                sync_checked = sync_checked + 1;
            end else previous_known = 0;
        end
    endtask

    initial begin
        $readmemh("overlay_pixels.hex", expected_pixels);
        $readmemh("overlay_ages.hex", ages);
        repeat (3) @(negedge clk);
        if (draw_permit !== 0) $fatal(1, "reset must immediately disable draw");
        rstn = 1;
        for (frame_index = 0; frame_index < CASE_COUNT; frame_index = frame_index + 1) begin
            // Finite0 with draw0 represents a legitimate empty table.
            table_draw_valid = (ages[frame_index] != 0 && ages[frame_index] <= 2000);
            age = 64'hffffffffffffffff;
            switched_age = ages[frame_index];
            switch_at_sof = 1;
            pixel(1,1,0,0,24'h314159,24'h314159);
            switch_at_sof = 0;
            pixel(0,0,1,0,24'h271828,24'h271828); // First blank edge AFTER SOF.
            for (y = 0; y < HEIGHT; y = y + 1) begin
                for (x = 0; x < WIDTH; x = x + 1) begin
                    // The live table may change; this frame's text must remain frozen.
                    if (y == 18 && x == 20) age = 64'hffffffffffffffff;
                    if (y == 20 && x == 32) begin
                        table_draw_valid = 1;
                        #1;
                        if (draw_permit !== 1) $fatal(1, "draw permission did not immediately enable");
                    end
                    if (y == 20 && x == 80) begin
                        table_draw_valid = 0;
                        #1;
                        if (draw_permit !== 0) $fatal(1, "draw permission did not immediately disable");
                        live_off_checked = live_off_checked + 1;
                    end
                    rgb = 24'h125000 + x + y*WIDTH + frame_index;
                    expected_rgb = expected_pixels[frame_index*WIDTH*HEIGHT+y*WIDTH+x] ? 24'hffffff : rgb;
                    pixel(0,(y%3 == 0),(x%7 == 0),1,rgb,expected_rgb);
                    pixels_checked = pixels_checked + 1;
                    if (expected_rgb == 24'hffffff) white_checked = white_checked + 1;
                    else pass_checked = pass_checked + 1;
                end
                pixel(0,0,1,0,24'h654321,24'h654321); // DE falling edge advances y.
            end
        end
        // Common reset while text is live cancels frame latch and drawing.
        @(negedge clk);
        table_draw_valid = 1;
        rstn = 0;
        #1;
        if (draw_permit !== 0) $fatal(1, "reset failed to remove live draw permission");
        $display("TB_PASS_OVERLAY frames=%0d pixels=%0d glyph_pixels=%0d passthrough=%0d sync_edges=%0d live_off=%0d",CASE_COUNT,pixels_checked,white_checked,pass_checked,sync_checked,live_off_checked);
        $finish;
    end

    initial begin
        #10000000;
        $fatal(1, "overlay simulation watchdog frame=%0d x=%0d y=%0d", frame_index,x,y);
    end
endmodule
