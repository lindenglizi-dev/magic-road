create_clock -name {sys_clk_50m} -period 20.000 -waveform {0.000 10.000} [get_ports {I_sys_clk}]
create_clock -name {mipi_rx_ck_pad} -period 2.415 -waveform {0.000 1.208} [get_nets {IO_rx_clk_pad_p}]

derive_clocks

rename_clock -name {pll_clk_100m} [get_clocks {u_PLL/ph1p_phy_pll_wrapper_25a56e5ce2f9_Inst/u_PH1P_PHY_PLL.clkc[0]}]
rename_clock -name {pll_clk_24m} [get_clocks {u_PLL/ph1p_phy_pll_wrapper_25a56e5ce2f9_Inst/u_PH1P_PHY_PLL.clkc[1]}]
rename_clock -name {HDMI_PIXEL_CLK} [get_clocks {u_PLL/ph1p_phy_pll_wrapper_25a56e5ce2f9_Inst/u_PH1P_PHY_PLL.clkc[4]}]
rename_clock -name {HDMI_SERIAL_CLK} [get_clocks {u_PLL/ph1p_phy_pll_wrapper_25a56e5ce2f9_Inst/u_PH1P_PHY_PLL.clkc[5]}]

rename_clock -name {MIPI_RX_BYTE_CLK} [get_clocks {u_mipi_dphy_rx_ph1p_mipiio_wrapper/u_ph1p_mipiio_rx_wrapper/u_PH1P_LOGIC_DPHY_MIPI_RX.o_fabric_div4_8_clk}]


# uicfgcs520 uses CLK_DIV = 23809524/100000-1 = 237.
# uii2c toggles after 119 source cycles; all internal state uses I_clk enables.

# Unrelated control-clock families. DDR/video FIFO pairs are deliberately
# absent here: their Gray buses retain real datapath-only max-delay checks.
set_clock_groups -asynchronous \
    -group [get_clocks {mipi_rx_ck_pad MIPI_RX_BYTE_CLK}] \
    -group [get_clocks {sys_clk_50m pll_clk_100m pll_clk_24m HDMI_PIXEL_CLK HDMI_SERIAL_CLK}]
set_clock_groups -asynchronous \
    -group [get_clocks {sys_clk_50m pll_clk_100m pll_clk_24m HDMI_SERIAL_CLK}] \
    -group [get_clocks {u_ph1p35_324_ddr_wrapper/u_ddr2/ddr_clk u_ph1p35_324_ddr_wrapper/u_ddr2/usr_clk}]

# Independent clock phases have no synchronous hold relationship. Bound
# every crossing data path by min(source,destination period)-0.300 ns,
# matching the FIFO IP timing contract; keep the IP's per-Gray checks too.
set_max_delay -datapath_only -from [get_clocks MIPI_RX_BYTE_CLK] -to [get_clocks {u_ph1p35_324_ddr_wrapper/u_ddr2/usr_clk}] 9.360
set_max_delay -datapath_only -from [get_clocks {u_ph1p35_324_ddr_wrapper/u_ddr2/usr_clk}] -to [get_clocks MIPI_RX_BYTE_CLK] 9.360
set_false_path -hold -from [get_clocks MIPI_RX_BYTE_CLK] -to [get_clocks {u_ph1p35_324_ddr_wrapper/u_ddr2/usr_clk}]
set_false_path -hold -from [get_clocks {u_ph1p35_324_ddr_wrapper/u_ddr2/usr_clk}] -to [get_clocks MIPI_RX_BYTE_CLK]
set_max_delay -datapath_only -from [get_clocks HDMI_PIXEL_CLK] -to [get_clocks {u_ph1p35_324_ddr_wrapper/u_ddr2/usr_clk}] 13.033
set_max_delay -datapath_only -from [get_clocks {u_ph1p35_324_ddr_wrapper/u_ddr2/usr_clk}] -to [get_clocks HDMI_PIXEL_CLK] 13.033
set_false_path -hold -from [get_clocks HDMI_PIXEL_CLK] -to [get_clocks {u_ph1p35_324_ddr_wrapper/u_ddr2/usr_clk}]
set_false_path -hold -from [get_clocks {u_ph1p35_324_ddr_wrapper/u_ddr2/usr_clk}] -to [get_clocks HDMI_PIXEL_CLK]

