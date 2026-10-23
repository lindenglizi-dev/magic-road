# Run from lesson14_transformer_full project directory:
# vsim -c -do ../validation/run_modelsim_all.do
onerror {quit -code 1 -f}
vlib work
vlog -sv rtl/mac_array_4x4.sv ../validation/tb_mac_smoke.sv
vsim -c tb_mac_smoke
run -all
quit -sim
vlog -sv rtl/mac_array_4x4.sv rtl/tiled_gemm_4x4_banked_compact.sv rtl/requant_shift_sat.sv rtl/ffn_relu_requant.sv rtl/softmax_row_int32.sv rtl/probability_writer.sv rtl/transformer_block_top.sv tb/tb_transformer_block.sv
foreach c {demo edge_5x7 random_00 sat_1x1} {
    puts "==== BEGIN RTL CASE $c ===="
    vsim -c tb_transformer_block +CASE=vectors/$c
    run -all
    quit -sim
}
puts "==== ALL CASES FINISHED; verify PASS lines above ===="
quit -code 0 -f
