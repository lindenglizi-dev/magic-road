# Toolchain environment failure retained

The first ModelSim launch in the restricted subprocess failed before Verilog compilation with the Windows message `无效的系统 DLL 重定位`. No source was changed in response, and no behavioral RAM substitute was used.

The identical local vendor-model flow was rerun with the approved unrestricted subprocess. ModelSim SE-64 2020.4 then compiled the complete source closure with zero errors and zero warnings. The final reset and regression runs both passed; each retained two vendor-model `INIT_FILE` part-select warnings from `ph1p_logic_eram.v(165)`.

A second command-closure failure, caused by omitting the required `PH1P_PHY_GSR` simulation top, is retained verbatim in `modelsim_regression_missing_gsr_failure.log`. The corrected run explicitly loaded both `reset_work.PH1P_PHY_GSR` and the testbench top.
