vlib work
vlog -sv rtl/mac_array_4x4.sv rtl/tiled_gemm_4x4_banked_compact.sv rtl/requant_shift_sat.sv rtl/ffn_relu_requant.sv rtl/softmax_row_int32.sv rtl/probability_writer.sv rtl/transformer_block_top.sv tb/tb_transformer_block.sv
vsim -c tb_transformer_block +CASE=vectors/demo -do "run -all; quit -f"
