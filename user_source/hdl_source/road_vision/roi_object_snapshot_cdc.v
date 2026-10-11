// Freeze the four CCL candidate boxes and transfer the stable snapshot from
// the camera domain to the 100 MHz ROI domain. One entry is 40 bits:
// {valid, class[1:0], xmin, xmax, ymin, ymax, 5'b0}.
module roi_object_snapshot_cdc (
    input  wire         src_clk,
    input  wire         src_rst_n,
    input  wire         frame_clear,
    input  wire         obj_valid,
    input  wire [1:0]   obj_index,
    input  wire [1:0]   obj_class,
    input  wire [7:0]   obj_xmin,
    input  wire [7:0]   obj_xmax,
    input  wire [7:0]   obj_ymin,
    input  wire [7:0]   obj_ymax,
    input  wire [2:0]   object_count,
    input  wire         object_frame_done,
    input  wire         discard_frame,

    input  wire         dst_clk,
    input  wire         dst_rst_n,
    output reg          dst_update,
    output reg  [31:0]  dst_frame_id,
    output reg  [2:0]   dst_object_count,
    output reg  [159:0] dst_boxes
);
    wire [39:0] object_word = {1'b1, obj_class, obj_xmin, obj_xmax,
                               obj_ymin, obj_ymax, 5'b0};
    reg [39:0] stage_box [0:3];
    reg [159:0] src_boxes;
    reg [31:0] src_frame_id, src_next_frame_id;
    reg [2:0] src_object_count;
    reg src_toggle;
    integer i;

    always @(posedge src_clk or negedge src_rst_n) begin
        if (!src_rst_n) begin
            src_boxes <= 160'd0;
            src_frame_id <= 32'd0;
            src_next_frame_id <= 32'd0;
            src_object_count <= 3'd0;
            src_toggle <= 1'b0;
            for (i = 0; i < 4; i = i + 1)
                stage_box[i] <= 40'd0;
        end else begin
            if (frame_clear)
                for (i = 0; i < 4; i = i + 1)
                    stage_box[i] <= 40'd0;

            if (obj_valid)
                stage_box[obj_index] <= object_word;

            if (object_frame_done) begin
                src_frame_id <= src_next_frame_id;
                src_next_frame_id <= src_next_frame_id + 1'b1;
                src_object_count <= discard_frame ? 3'd0 :
                                    ((object_count > 4) ? 3'd4 : object_count);
                if (discard_frame) begin
                    src_boxes <= 160'd0;
                end else begin
                    src_boxes[39:0] <= stage_box[0];
                    src_boxes[79:40] <= stage_box[1];
                    src_boxes[119:80] <= stage_box[2];
                    src_boxes[159:120] <= stage_box[3];
                    // Preserve a final object if valid and frame_done happen
                    // on the same source clock.
                    if (obj_valid)
                        case (obj_index)
                            2'd0: src_boxes[39:0] <= object_word;
                            2'd1: src_boxes[79:40] <= object_word;
                            2'd2: src_boxes[119:80] <= object_word;
                            2'd3: src_boxes[159:120] <= object_word;
                        endcase
                end
                src_toggle <= ~src_toggle;
            end
        end
    end

    (* async_reg = "true" *) reg toggle_meta, toggle_sync;
    reg toggle_seen;
    reg [159:0] boxes_meta;
    reg [31:0] frame_id_meta;
    reg [2:0] count_meta;

    always @(posedge dst_clk or negedge dst_rst_n) begin
        if (!dst_rst_n) begin
            toggle_meta <= 1'b0;
            toggle_sync <= 1'b0;
            toggle_seen <= 1'b0;
            boxes_meta <= 160'd0;
            frame_id_meta <= 32'd0;
            count_meta <= 3'd0;
            dst_update <= 1'b0;
            dst_frame_id <= 32'd0;
            dst_object_count <= 3'd0;
            dst_boxes <= 160'd0;
        end else begin
            boxes_meta <= src_boxes;
            frame_id_meta <= src_frame_id;
            count_meta <= src_object_count;
            toggle_meta <= src_toggle;
            toggle_sync <= toggle_meta;
            dst_update <= 1'b0;
            if (toggle_sync != toggle_seen) begin
                toggle_seen <= toggle_sync;
                dst_frame_id <= frame_id_meta;
                dst_object_count <= count_meta;
                dst_boxes <= boxes_meta;
                dst_update <= 1'b1;
            end
        end
    end
endmodule

