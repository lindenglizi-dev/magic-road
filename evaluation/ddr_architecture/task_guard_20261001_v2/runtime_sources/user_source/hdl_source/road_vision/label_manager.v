module label_manager #(
    parameter LABEL_WIDTH = 6,
    parameter MAX_LABEL   = 32
)(
    input  wire                     clk,
    input  wire                     rst_n,
    input  wire                     frame_clear,

    input  wire                     alloc_req,
    output reg                      alloc_done,
    output reg  [LABEL_WIDTH-1:0]   alloc_label,

    input  wire                     union_req,
    input  wire [LABEL_WIDTH-1:0]   union_a,
    input  wire [LABEL_WIDTH-1:0]   union_b,
    output reg                      union_done,
    output reg  [LABEL_WIDTH-1:0]   union_root,

    input  wire                     find_req,
    input  wire [LABEL_WIDTH-1:0]   find_label,
    output reg                      find_done,
    output reg  [LABEL_WIDTH-1:0]   find_root,

    output reg                      busy,
    output reg  [LABEL_WIDTH:0]     next_label,
    output reg                      label_overflow,
    output reg                      parent_chain_error,
    output reg                      protocol_error
);

    localparam S_IDLE         = 4'd0;
    localparam S_FIND_A_READ  = 4'd1;
    localparam S_FIND_A_CHECK = 4'd2;
    localparam S_FIND_B_READ  = 4'd3;
    localparam S_FIND_B_CHECK = 4'd4;
    localparam S_LINK         = 4'd5;
    localparam S_FIND_EXT_READ  = 4'd6;
    localparam S_FIND_EXT_CHECK = 4'd7;

    reg [3:0] state;

    reg [LABEL_WIDTH-1:0] parent_mem [0:MAX_LABEL];
    reg [LABEL_WIDTH-1:0] walk_label;
    reg [LABEL_WIDTH-1:0] parent_value;
    reg [LABEL_WIDTH-1:0] root_a;
    reg [LABEL_WIDTH-1:0] root_b;
    reg [LABEL_WIDTH:0]   find_steps;

    wire union_a_valid;
    wire union_b_valid;
    wire find_label_valid;

    assign union_a_valid = (union_a != {LABEL_WIDTH{1'b0}}) &&
                           ({1'b0, union_a} < next_label) &&
                           (union_a <= MAX_LABEL);

    assign union_b_valid = (union_b != {LABEL_WIDTH{1'b0}}) &&
                           ({1'b0, union_b} < next_label) &&
                           (union_b <= MAX_LABEL);

    assign find_label_valid = (find_label != {LABEL_WIDTH{1'b0}}) &&
                              ({1'b0, find_label} < next_label) &&
                              (find_label <= MAX_LABEL);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state              <= S_IDLE;
            alloc_done         <= 1'b0;
            alloc_label        <= {LABEL_WIDTH{1'b0}};
            union_done         <= 1'b0;
            union_root         <= {LABEL_WIDTH{1'b0}};
            find_done          <= 1'b0;
            find_root          <= {LABEL_WIDTH{1'b0}};
            busy               <= 1'b0;
            next_label         <= {{LABEL_WIDTH{1'b0}}, 1'b1};
            label_overflow     <= 1'b0;
            parent_chain_error <= 1'b0;
            protocol_error     <= 1'b0;
            walk_label         <= {LABEL_WIDTH{1'b0}};
            parent_value       <= {LABEL_WIDTH{1'b0}};
            root_a             <= {LABEL_WIDTH{1'b0}};
            root_b             <= {LABEL_WIDTH{1'b0}};
            find_steps         <= {(LABEL_WIDTH+1){1'b0}};
        end else if (frame_clear) begin
            state              <= S_IDLE;
            alloc_done         <= 1'b0;
            alloc_label        <= {LABEL_WIDTH{1'b0}};
            union_done         <= 1'b0;
            union_root         <= {LABEL_WIDTH{1'b0}};
            find_done          <= 1'b0;
            find_root          <= {LABEL_WIDTH{1'b0}};
            busy               <= 1'b0;
            next_label         <= {{LABEL_WIDTH{1'b0}}, 1'b1};
            label_overflow     <= 1'b0;
            parent_chain_error <= 1'b0;
            protocol_error     <= 1'b0;
            walk_label         <= {LABEL_WIDTH{1'b0}};
            parent_value       <= {LABEL_WIDTH{1'b0}};
            root_a             <= {LABEL_WIDTH{1'b0}};
            root_b             <= {LABEL_WIDTH{1'b0}};
            find_steps         <= {(LABEL_WIDTH+1){1'b0}};
        end else begin
            alloc_done <= 1'b0;
            union_done <= 1'b0;
            find_done  <= 1'b0;

            if ((state != S_IDLE) && (alloc_req || union_req || find_req)) begin
                protocol_error <= 1'b1;
            end

            case (state)
                S_IDLE: begin
                    busy <= 1'b0;

                    if ((alloc_req && union_req) ||
                        (alloc_req && find_req) ||
                        (union_req && find_req)) begin
                        protocol_error <= 1'b1;
                    end else if (alloc_req) begin
                        alloc_done <= 1'b1;

                        if (next_label <= MAX_LABEL) begin
                            alloc_label <= next_label[LABEL_WIDTH-1:0];
                            parent_mem[next_label[LABEL_WIDTH-1:0]]
                                <= next_label[LABEL_WIDTH-1:0];
                            next_label <= next_label + 1'b1;
                        end else begin
                            alloc_label    <= {LABEL_WIDTH{1'b0}};
                            label_overflow <= 1'b1;
                        end
                    end else if (union_req) begin
                        if (!union_a_valid || !union_b_valid) begin
                            protocol_error <= 1'b1;
                            union_done     <= 1'b1;
                            union_root     <= {LABEL_WIDTH{1'b0}};
                        end else begin
                            busy       <= 1'b1;
                            walk_label <= union_a;
                            find_steps <= {(LABEL_WIDTH+1){1'b0}};
                            state      <= S_FIND_A_READ;
                        end
                    end else if (find_req) begin
                        if (!find_label_valid) begin
                            protocol_error <= 1'b1;
                            find_done      <= 1'b1;
                            find_root      <= {LABEL_WIDTH{1'b0}};
                        end else begin
                            busy       <= 1'b1;
                            walk_label <= find_label;
                            find_steps <= {(LABEL_WIDTH+1){1'b0}};
                            state      <= S_FIND_EXT_READ;
                        end
                    end
                end

                S_FIND_A_READ: begin
                    if ((walk_label == {LABEL_WIDTH{1'b0}}) ||
                        (walk_label > MAX_LABEL)) begin
                        parent_chain_error <= 1'b1;
                        union_done         <= 1'b1;
                        union_root         <= {LABEL_WIDTH{1'b0}};
                        busy               <= 1'b0;
                        state              <= S_IDLE;
                    end else begin
                        parent_value <= parent_mem[walk_label];
                        state        <= S_FIND_A_CHECK;
                    end
                end

                S_FIND_A_CHECK: begin
                    if (parent_value == walk_label) begin
                        root_a     <= walk_label;
                        walk_label <= union_b;
                        find_steps <= {(LABEL_WIDTH+1){1'b0}};
                        state      <= S_FIND_B_READ;
                    end else if ((parent_value == {LABEL_WIDTH{1'b0}}) ||
                                 (parent_value > MAX_LABEL) ||
                                 (find_steps >= MAX_LABEL)) begin
                        parent_chain_error <= 1'b1;
                        union_done         <= 1'b1;
                        union_root         <= {LABEL_WIDTH{1'b0}};
                        busy               <= 1'b0;
                        state              <= S_IDLE;
                    end else begin
                        walk_label <= parent_value;
                        find_steps <= find_steps + 1'b1;
                        state      <= S_FIND_A_READ;
                    end
                end

                S_FIND_B_READ: begin
                    if ((walk_label == {LABEL_WIDTH{1'b0}}) ||
                        (walk_label > MAX_LABEL)) begin
                        parent_chain_error <= 1'b1;
                        union_done         <= 1'b1;
                        union_root         <= {LABEL_WIDTH{1'b0}};
                        busy               <= 1'b0;
                        state              <= S_IDLE;
                    end else begin
                        parent_value <= parent_mem[walk_label];
                        state        <= S_FIND_B_CHECK;
                    end
                end

                S_FIND_B_CHECK: begin
                    if (parent_value == walk_label) begin
                        root_b <= walk_label;
                        state  <= S_LINK;
                    end else if ((parent_value == {LABEL_WIDTH{1'b0}}) ||
                                 (parent_value > MAX_LABEL) ||
                                 (find_steps >= MAX_LABEL)) begin
                        parent_chain_error <= 1'b1;
                        union_done         <= 1'b1;
                        union_root         <= {LABEL_WIDTH{1'b0}};
                        busy               <= 1'b0;
                        state              <= S_IDLE;
                    end else begin
                        walk_label <= parent_value;
                        find_steps <= find_steps + 1'b1;
                        state      <= S_FIND_B_READ;
                    end
                end

                S_LINK: begin
                    if (root_a == root_b) begin
                        union_root <= root_a;
                    end else if (root_a < root_b) begin
                        parent_mem[root_b] <= root_a;
                        union_root         <= root_a;
                    end else begin
                        parent_mem[root_a] <= root_b;
                        union_root         <= root_b;
                    end

                    union_done <= 1'b1;
                    busy       <= 1'b0;
                    state      <= S_IDLE;
                end

                S_FIND_EXT_READ: begin
                    if ((walk_label == {LABEL_WIDTH{1'b0}}) ||
                        (walk_label > MAX_LABEL)) begin
                        parent_chain_error <= 1'b1;
                        find_done          <= 1'b1;
                        find_root          <= {LABEL_WIDTH{1'b0}};
                        busy               <= 1'b0;
                        state              <= S_IDLE;
                    end else begin
                        parent_value <= parent_mem[walk_label];
                        state        <= S_FIND_EXT_CHECK;
                    end
                end

                S_FIND_EXT_CHECK: begin
                    if (parent_value == walk_label) begin
                        find_done <= 1'b1;
                        find_root <= walk_label;
                        busy      <= 1'b0;
                        state     <= S_IDLE;
                    end else if ((parent_value == {LABEL_WIDTH{1'b0}}) ||
                                 (parent_value > MAX_LABEL) ||
                                 (find_steps >= MAX_LABEL)) begin
                        parent_chain_error <= 1'b1;
                        find_done          <= 1'b1;
                        find_root          <= {LABEL_WIDTH{1'b0}};
                        busy               <= 1'b0;
                        state              <= S_IDLE;
                    end else begin
                        walk_label <= parent_value;
                        find_steps <= find_steps + 1'b1;
                        state      <= S_FIND_EXT_READ;
                    end
                end

                default: begin
                    state          <= S_IDLE;
                    busy           <= 1'b0;
                    protocol_error <= 1'b1;
                end
            endcase
        end
    end

endmodule
