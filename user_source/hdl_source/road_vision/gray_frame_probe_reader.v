// Temporary 100 MHz consumer used to validate frame-buffer bandwidth and CDC.
// It scans every byte and releases the bank.  The HOG/ROI accelerator will
// later replace this module without changing gray_frame_pingpong.
module gray_frame_probe_reader #(
    parameter ADDR_WIDTH = 16,
    parameter FRAME_PIXELS = 256*144
)(
    input  wire                  clk,
    input  wire                  rst_n,
    input  wire                  frame_ready,
    input  wire [31:0]           frame_id,
    output reg                   release_frame,
    output reg                   rd_req_valid,
    output reg [ADDR_WIDTH-1:0]  rd_req_addr,
    input  wire                  rd_rsp_valid,
    input  wire [7:0]            rd_rsp_gray,
    output reg                   busy,
    output reg                   frame_done,
    output reg [31:0]            completed_frame_id,
    output reg [7:0]             frame_checksum,
    output reg                   protocol_error
);
    reg [ADDR_WIDTH:0] issue_count;
    reg [ADDR_WIDTH:0] response_count;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            release_frame <= 1'b0;
            rd_req_valid <= 1'b0;
            rd_req_addr <= 0;
            busy <= 1'b0;
            frame_done <= 1'b0;
            completed_frame_id <= 0;
            frame_checksum <= 0;
            issue_count <= 0;
            response_count <= 0;
            protocol_error <= 1'b0;
        end else begin
            release_frame <= 1'b0;
            rd_req_valid <= 1'b0;
            frame_done <= 1'b0;

            if (frame_ready) begin
                if (busy)
                    protocol_error <= 1'b1;
                else begin
                    busy <= 1'b1;
                    issue_count <= 0;
                    response_count <= 0;
                    completed_frame_id <= frame_id;
                    frame_checksum <= 0;
                end
            end

            if (busy) begin
                if (issue_count < FRAME_PIXELS) begin
                    rd_req_valid <= 1'b1;
                    rd_req_addr <= issue_count[ADDR_WIDTH-1:0];
                    issue_count <= issue_count + 1'b1;
                end
                if (rd_rsp_valid) begin
                    frame_checksum <= frame_checksum ^ rd_rsp_gray;
                    response_count <= response_count + 1'b1;
                    if (response_count == FRAME_PIXELS-1) begin
                        busy <= 1'b0;
                        frame_done <= 1'b1;
                        release_frame <= 1'b1;
                    end
                end
            end else if (rd_rsp_valid) begin
                protocol_error <= 1'b1;
            end
        end
    end
endmodule
