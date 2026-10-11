`timescale 1ns/1ps

module tb_road_yolo_numeric_rom_probe (
    output reg o_test_done
);

    localparam [14:0] ST_BIT_FETCH = 15'b000000100000000;
    localparam integer C_TOTAL_WORDS = 7168;
    localparam integer C_WATCHDOG_CYCLES = 2500000;
    `include "artifacts/numeric_test_seed42_crc32.vh"

    reg i_clk;
    reg i_rstn;
    wire o_done;
    wire [31:0] o_checksum;
    reg [159:0] expected_words [0:C_TOTAL_WORDS-1];
    integer compared_words;
    integer watchdog_cycles;
    integer observed_index;
    reg saw_first_word;
    reg saw_first_group_end;
    reg saw_second_group_start;
    reg saw_payload_boundary_before;
    reg saw_payload_boundary_word;
    reg saw_final_word;

    road_yolo_numeric_rom_probe dut (
        .i_clk(i_clk),
        .i_rstn(i_rstn),
        .o_done(o_done),
        .o_checksum(o_checksum)
    );

    initial begin
        i_clk = 1'b0;
        forever #5 i_clk = ~i_clk;
    end

    initial begin
        o_test_done = 1'b0;
        i_rstn = 1'b0;
        compared_words = 0;
        watchdog_cycles = 0;
        saw_first_word = 1'b0;
        saw_first_group_end = 1'b0;
        saw_second_group_start = 1'b0;
        saw_payload_boundary_before = 1'b0;
        saw_payload_boundary_word = 1'b0;
        saw_final_word = 1'b0;
        $readmemh("artifacts/numeric_test_seed42_words.dath", expected_words);
        repeat (4) @(posedge i_clk);
        i_rstn = 1'b1;
    end

    always @(posedge i_clk) begin
        if (i_rstn) begin
            watchdog_cycles = watchdog_cycles + 1;
            if (watchdog_cycles > C_WATCHDOG_CYCLES)
                $fatal(1, "watchdog expired after %0d cycles", watchdog_cycles);

            if ((dut.state_current == ST_BIT_FETCH) && (dut.cnt_bit_index == 8'd0)) begin
                observed_index = dut.cnt_group_index * 512 + dut.cnt_word_addr;
                if (observed_index != compared_words)
                    $fatal(1, "word order mismatch: observed %0d expected %0d",
                           observed_index, compared_words);
                if (dut.reg_word_buffer !== expected_words[observed_index])
                    $fatal(1, "word mismatch at group %0d word %0d absolute %0d",
                           dut.cnt_group_index, dut.cnt_word_addr, observed_index);
                if (observed_index == 0) saw_first_word = 1'b1;
                if (observed_index == 511) saw_first_group_end = 1'b1;
                if (observed_index == 512) saw_second_group_start = 1'b1;
                if (observed_index == 7025) saw_payload_boundary_before = 1'b1;
                if (observed_index == 7026) saw_payload_boundary_word = 1'b1;
                if (observed_index == 7167) saw_final_word = 1'b1;
                compared_words = compared_words + 1;
            end

            if (o_done) begin
                if (compared_words != C_TOTAL_WORDS)
                    $fatal(1, "compared %0d words, expected %0d",
                           compared_words, C_TOTAL_WORDS);
                if (o_checksum !== C_EXPECTED_CHECKSUM)
                    $fatal(1, "checksum mismatch: got %08x expected %08x",
                           o_checksum, C_EXPECTED_CHECKSUM);
                if (!(saw_first_word && saw_first_group_end && saw_second_group_start &&
                      saw_payload_boundary_before && saw_payload_boundary_word && saw_final_word))
                    $fatal(1, "one or more explicit boundary observations are missing");
                o_test_done = 1'b1;
                $display("PASS: 7168 words / 143360 bytes checked, CRC32=%08x", o_checksum);
                $finish;
            end
        end
    end

endmodule
