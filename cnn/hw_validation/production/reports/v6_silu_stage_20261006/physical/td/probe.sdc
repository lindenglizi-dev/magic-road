# Internal SiLU fixture target, not a measured board oscillator.
create_clock -name {probe_clk} -period 10.000 -waveform {0.000 5.000} [get_ports {i_clk}]
# Zero-delay boundary is a diagnostic fixture assumption, NOT board timing.
# Keep reset checks visible; no false paths, min-delay padding or waiver.
set_input_delay -clock [get_clocks {probe_clk}] -max 0.000 [get_ports {i_rstn}]
set_input_delay -clock [get_clocks {probe_clk}] -min 0.000 [get_ports {i_rstn}]
set_output_delay -clock [get_clocks {probe_clk}] -max 0.000 [get_ports {o_done o_error o_phase[*] o_result_count[*] o_checksum[*]}]
set_output_delay -clock [get_clocks {probe_clk}] -min 0.000 [get_ports {o_done o_error o_phase[*] o_result_count[*] o_checksum[*]}]
