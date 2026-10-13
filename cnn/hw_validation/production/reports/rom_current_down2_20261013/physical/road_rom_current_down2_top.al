<?xml version="1.0" encoding="UTF-8"?>
<Project Version="3" Minor="2" Path="E:/project/qiansai/anlogic_topic2_work/lab1_sc500_road_vision/cnn/hw_validation/production/reports/rom_current_down2_20261013/physical">
    <Project_Created_Time></Project_Created_Time>
    <TD_Encoding>UTF-8</TD_Encoding>
    <TD_Version>6.2.168116</TD_Version>
    <Name>road_rom_current_down2_top</Name>
    <HardWare>
        <Family>PH1</Family>
        <Device>PH1P35MDG324</Device>
        <Speed>-3</Speed>
    </HardWare>
    <Source_Files>
        <Verilog>
<File Path="../rtl/road_down2_parameter_prefetch.v"/>
<File Path="../rtl/road_down2_tile_scheduler.v"/>
<File Path="../rtl/road_frontend_shared_core.v"/>
<File Path="../rtl/road_numeric_rom_reader.v"/>
<File Path="../rtl/road_rom_current_down2_top.v"/>
<File Path="../rtl/road_stem_tile_scheduler.v"/>
<File Path="../rtl/road_yolo_numeric_rom_group.v"/>
<File Path="../../board_selftest_20261010/core/down2_dynamic_tile_runner.v"/>
<File Path="../../board_selftest_20261010/core/road_down2_dynamic_adapter.v"/>
<File Path="../../board_selftest_20261010/core/road_dynamic_overlap_low_io_top.v"/>
<File Path="../../board_selftest_20261010/core/road_dynamic_postprocess.v"/>
<File Path="../../board_selftest_20261010/core/road_dynamic_requant.v"/>
<File Path="../../board_selftest_20261010/core/road_mac_probe.v"/>
<File Path="../../board_selftest_20261010/core/road_round_shift.v"/>
<File Path="../../board_selftest_20261010/core/silu_shared_unit.v"/>
</Verilog>
    </Source_Files>
    <FileSets>
        <FileSet Name="design_1" Type="DesignFiles">
        </FileSet>
        <FileSet Name="constraint_1" Type="ConstrainFiles">
        </FileSet>
    </FileSets>
    <TOP_MODULE>
        <LABEL>road_rom_current_down2_top</LABEL>
        <MODULE>road_rom_current_down2_top</MODULE>
        <CREATEINDEX>user</CREATEINDEX>
    </TOP_MODULE>
    <Property>
    </Property>
    <Device_Settings>
    </Device_Settings>
    <Configurations>
        <FeatureRow>
            <boot_mode>mspix4</boot_mode>
        </FeatureRow>
    </Configurations>
    <Runs>
        <Run Name="syn_1" Type="Synthesis" ConstraintSet="constraint_1" Description="" Active="true" useDefaultScript="false">
            <Strategy Name="Default_Synthesis_Strategy">
            </Strategy>
            <UserParams>
            </UserParams>
        </Run>
        <Run Name="phy_1" Type="PhysicalDesign" ConstraintSet="constraint_1" Description="" SynRun="syn_1" Active="true">
            <Strategy Name="Default_PhysicalDesign_Strategy">
            </Strategy>
            <UserParams>
            </UserParams>
        </Run>
    </Runs>
    <Project_Settings>
    </Project_Settings>
</Project>
