module frame_resolver #(
    parameter LABEL_WIDTH = 6,
    parameter MAX_LABEL   = 32
)(
    input  wire                     clk,
    input  wire                     rst_n,
    input  wire                     frame_clear,
    input  wire                     start,
    input  wire [LABEL_WIDTH:0]     label_limit,

    output reg                      find_req,
    output reg  [LABEL_WIDTH-1:0]   find_label,
    input  wire                     find_done,
    input  wire [LABEL_WIDTH-1:0]   find_root,

    output reg                      merge_req,
    output reg  [LABEL_WIDTH-1:0]   merge_src_label,
    output reg  [LABEL_WIDTH-1:0]   merge_dst_label,
    input  wire                     merge_done,

    output reg                      busy,
    output reg                      done,
    output reg  [31:0]              resolve_cycle_count,
    output reg  [31:0]              resolve_cycle_max,
    output reg                      resolver_error,
    output reg                      protocol_error
);

    localparam S_IDLE       = 3'd0;
    localparam S_FIND_REQ   = 3'd1;
    localparam S_FIND_WAIT  = 3'd2;
    localparam S_MERGE_REQ  = 3'd3;
    localparam S_MERGE_WAIT = 3'd4;
    localparam S_FINISH     = 3'd5;

    reg [2:0] state;
    reg [LABEL_WIDTH-1:0] scan_label;
    reg [LABEL_WIDTH:0]   label_limit_latched;
    reg [LABEL_WIDTH-1:0] root_latched;

    wire last_label;

    assign last_label = ({1'b0, scan_label} + 1'b1) >=
                        label_limit_latched;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state                 <= S_IDLE;
            scan_label            <= {{(LABEL_WIDTH-1){1'b0}}, 1'b1};
            label_limit_latched   <= {{LABEL_WIDTH{1'b0}}, 1'b1};
            root_latched          <= {LABEL_WIDTH{1'b0}};
            find_req              <= 1'b0;
            find_label            <= {LABEL_WIDTH{1'b0}};
            merge_req             <= 1'b0;
            merge_src_label       <= {LABEL_WIDTH{1'b0}};
            merge_dst_label       <= {LABEL_WIDTH{1'b0}};
            busy                  <= 1'b0;
            done                  <= 1'b0;
            resolve_cycle_count   <= 32'd0;
            resolve_cycle_max     <= 32'd0;
            resolver_error        <= 1'b0;
            protocol_error        <= 1'b0;
        end else if (frame_clear) begin
            state                 <= S_IDLE;
            scan_label            <= {{(LABEL_WIDTH-1){1'b0}}, 1'b1};
            label_limit_latched   <= {{LABEL_WIDTH{1'b0}}, 1'b1};
            root_latched          <= {LABEL_WIDTH{1'b0}};
            find_req              <= 1'b0;
            merge_req             <= 1'b0;
            busy                  <= 1'b0;
            done                  <= 1'b0;
            resolve_cycle_count   <= 32'd0;
            resolve_cycle_max     <= 32'd0;
            resolver_error        <= 1'b0;
            protocol_error        <= 1'b0;
        end else begin
            find_req  <= 1'b0;
            merge_req <= 1'b0;
            done      <= 1'b0;

            if (busy)
                resolve_cycle_count <= resolve_cycle_count + 1'b1;

            if ((state != S_IDLE) && start)
                protocol_error <= 1'b1;

            case (state)
                S_IDLE: begin
                    busy <= 1'b0;
                    if (start) begin
                        if ((label_limit < 1) ||
                            (label_limit > (MAX_LABEL + 1))) begin
                            resolver_error <= 1'b1;
                            done           <= 1'b1;
                        end else begin
                            busy                <= 1'b1;
                            resolve_cycle_count <= 32'd0;
                            label_limit_latched <= label_limit;
                            scan_label          <= {{(LABEL_WIDTH-1){1'b0}}, 1'b1};

                            if (label_limit == 1)
                                state <= S_FINISH;
                            else
                                state <= S_FIND_REQ;
                        end
                    end
                end

                S_FIND_REQ: begin
                    find_req   <= 1'b1;
                    find_label <= scan_label;
                    state      <= S_FIND_WAIT;
                end

                S_FIND_WAIT: begin
                    if (find_done) begin
                        if ((find_root == {LABEL_WIDTH{1'b0}}) ||
                            (find_root > MAX_LABEL) ||
                            ({1'b0, find_root} >= label_limit_latched)) begin
                            resolver_error <= 1'b1;
                            state          <= S_FINISH;
                        end else if (find_root != scan_label) begin
                            root_latched <= find_root;
                            state        <= S_MERGE_REQ;
                        end else if (last_label) begin
                            state <= S_FINISH;
                        end else begin
                            scan_label <= scan_label + 1'b1;
                            state      <= S_FIND_REQ;
                        end
                    end
                end

                S_MERGE_REQ: begin
                    merge_req       <= 1'b1;
                    merge_src_label <= scan_label;
                    merge_dst_label <= root_latched;
                    state           <= S_MERGE_WAIT;
                end

                S_MERGE_WAIT: begin
                    if (merge_done) begin
                        if (last_label) begin
                            state <= S_FINISH;
                        end else begin
                            scan_label <= scan_label + 1'b1;
                            state      <= S_FIND_REQ;
                        end
                    end
                end

                S_FINISH: begin
                    busy <= 1'b0;
                    done <= 1'b1;
                    if (resolve_cycle_count > resolve_cycle_max)
                        resolve_cycle_max <= resolve_cycle_count;
                    state <= S_IDLE;
                end

                default: begin
                    state          <= S_IDLE;
                    busy           <= 1'b0;
                    resolver_error <= 1'b1;
                end
            endcase
        end
    end

endmodule
