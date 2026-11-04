create_clock -name {sys_clk_50m} -period 20.000 -waveform {0.000 10.000} [get_ports {I_sys_clk}]
create_clock -name {mipi_rx_ck_pad} -period 2.415 -waveform {0.000 1.208} [get_nets {IO_rx_clk_pad_p}]

create_clock -name ETH_RX_CLK -period 8.000 -waveform {0.000 4.000} [get_ports I_a_rgmii_rxc]
derive_clocks
rename_clock -name ETH_TX_CLK [get_clocks {u_ethernet/u_eth_pll/ph1p_phy_pll_wrapper_d2616deaaa79_Inst/u_PH1P_PHY_PLL.clkc[0]}]
rename_clock -name ETH_RX_FABRIC [get_clocks {u_ethernet/u_rgmii/u_gmii_rx_clk.clkout}]


create_generated_clock -name PHY_TX_CAPTURE \
    -source [get_pins {u_ethernet/u_eth_pll/ph1p_phy_pll_wrapper_d2616deaaa79_Inst/u_PH1P_PHY_PLL.clkc[0]}] \
    -master_clock [get_clocks ETH_TX_CLK] -edges {1 2 3} \
    -edge_shift {2.000 2.000 2.000} [get_ports O_a_rgmii_txc]


rename_clock -name {pll_clk_100m} [get_clocks {u_PLL/ph1p_phy_pll_wrapper_25a56e5ce2f9_Inst/u_PH1P_PHY_PLL.clkc[0]}]
rename_clock -name {pll_clk_24m} [get_clocks {u_PLL/ph1p_phy_pll_wrapper_25a56e5ce2f9_Inst/u_PH1P_PHY_PLL.clkc[1]}]
rename_clock -name {HDMI_PIXEL_CLK} [get_clocks {u_PLL/ph1p_phy_pll_wrapper_25a56e5ce2f9_Inst/u_PH1P_PHY_PLL.clkc[4]}]
rename_clock -name {HDMI_SERIAL_CLK} [get_clocks {u_PLL/ph1p_phy_pll_wrapper_25a56e5ce2f9_Inst/u_PH1P_PHY_PLL.clkc[5]}]

rename_clock -name {MIPI_RX_BYTE_CLK} [get_clocks {u_mipi_dphy_rx_ph1p_mipiio_wrapper/u_ph1p_mipiio_rx_wrapper/u_PH1P_LOGIC_DPHY_MIPI_RX.o_fabric_div4_8_clk}]









set_max_delay -datapath_only -from [get_clocks MIPI_RX_BYTE_CLK] -to [get_clocks {sys_clk_50m pll_clk_24m}] 9.000
set_max_delay -datapath_only -from [get_clocks {sys_clk_50m pll_clk_24m}] -to [get_clocks MIPI_RX_BYTE_CLK] 9.000
set_max_delay -datapath_only -from [get_clocks {MIPI_RX_BYTE_CLK pll_clk_24m HDMI_PIXEL_CLK}] -to [get_clocks {u_ph1p35_324_ddr_wrapper/u_ddr2/usr_clk}] 7.000




set_max_delay -datapath_only -from [get_clocks {u_ph1p35_324_ddr_wrapper/u_ddr2/usr_clk}] -to [get_clocks {MIPI_RX_BYTE_CLK pll_clk_24m HDMI_PIXEL_CLK}] 7.000






set_input_delay -clock ETH_RX_CLK -max 2.500 [get_ports {I_a_rgmii_rxd[*] I_a_rgmii_rx_ctl}]
set_input_delay -clock ETH_RX_CLK -min 1.500 [get_ports {I_a_rgmii_rxd[*] I_a_rgmii_rx_ctl}]
set_input_delay -clock ETH_RX_CLK -clock_fall -add_delay -max 2.500 [get_ports {I_a_rgmii_rxd[*] I_a_rgmii_rx_ctl}]
set_input_delay -clock ETH_RX_CLK -clock_fall -add_delay -min 1.500 [get_ports {I_a_rgmii_rxd[*] I_a_rgmii_rx_ctl}]


set_output_delay -clock PHY_TX_CAPTURE -max 1.350 [get_ports {O_a_rgmii_txd[*] O_a_rgmii_tx_ctl}]
set_output_delay -clock PHY_TX_CAPTURE -min -1.350 [get_ports {O_a_rgmii_txd[*] O_a_rgmii_tx_ctl}]
set_output_delay -clock PHY_TX_CAPTURE -clock_fall -add_delay -max 1.350 [get_ports {O_a_rgmii_txd[*] O_a_rgmii_tx_ctl}]
set_output_delay -clock PHY_TX_CAPTURE -clock_fall -add_delay -min -1.350 [get_ports {O_a_rgmii_txd[*] O_a_rgmii_tx_ctl}]





set_max_delay -datapath_only -from [get_clocks sys_clk_50m] -to [get_clocks ETH_TX_CLK] 6.000
set_max_delay -datapath_only -from [get_clocks ETH_TX_CLK] -to [get_clocks sys_clk_50m] 6.000


set_max_delay -datapath_only -from [get_clocks HDMI_PIXEL_CLK] -to [get_clocks ETH_TX_CLK] 7.000
set_max_delay -datapath_only -from [get_clocks ETH_TX_CLK] -to [get_clocks HDMI_PIXEL_CLK] 7.000

set_max_delay -datapath_only -from [get_clocks ETH_RX_FABRIC] -to [get_clocks ETH_TX_CLK] 7.000
set_max_delay -datapath_only -from [get_clocks ETH_TX_CLK] -to [get_clocks ETH_RX_FABRIC] 7.000

set_max_delay -datapath_only -from [get_clocks ETH_TX_CLK] -to [get_clocks ETH_RX_CLK] 7.000










set_max_delay -datapath_only -from [get_clocks MIPI_RX_BYTE_CLK] -to [get_clocks ETH_TX_CLK] 7.000
