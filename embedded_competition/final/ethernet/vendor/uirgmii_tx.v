`timescale 1ns / 1ps

module uirgmii_tx(
input wire         I_reset,
input wire         I_gmii_tclk,
input wire         I_gmii_tclk_90,
                            
input wire         I_gmii_tvalid,
input wire [7:0]   I_gmii_tdata,
	 
output wire        O_rgmii_tx_clk,
output wire        O_rgmii_tx_ctrl,
output wire [3:0]  O_rgmii_tx_data 
);


wire         not_I_gmii_tclk;	 
wire         O_rgmii_tx_clk_obuf;
wire         O_rgmii_tx_ctrl_obuf;
wire [3:0]   O_rgmii_tx_data_obuf;



  OBUF rgmii_txc_obuf_i (
     .I              (O_rgmii_tx_clk_obuf),
     .O              (O_rgmii_tx_clk)
  );
  
  OBUF rgmii_tx_ctl_obuf_i (
     .I              (O_rgmii_tx_ctrl_obuf),
     .O              (O_rgmii_tx_ctrl)
  );
  
  genvar i;
  generate for (i=0; i<4; i=i+1)
    begin : obuf_data
      OBUF rgmii_txd_obuf_i (
         .I              (O_rgmii_tx_data_obuf[i]),
         .O              (O_rgmii_tx_data[i])
      );
    end
  endgenerate
	 	 

   ODDR #(
      .DDR_CLK_EDGE("SAME_EDGE"),                                   
      .INIT(1'b0),                                       
      .SRTYPE("SYNC")                                      
   ) rgmii_txc_ddr (
      .Q(O_rgmii_tx_clk_obuf),                      
      .C(I_gmii_tclk_90),                       
      .CE(1'b1),                            
      .D1(1'b1),                                    
      .D2(1'b0),                                    
      .R(I_reset),                 
      .S(1'b0)                
   );   
	


   ODDR #(
      .DDR_CLK_EDGE("SAME_EDGE"),                                   
      .INIT(1'b0),                                       
      .SRTYPE("SYNC")                                      
   ) rgmii_ctl_ddr (
      .Q(O_rgmii_tx_ctrl_obuf),                      
      .C(I_gmii_tclk),                       
      .CE(1'b1),                            
      .D1(I_gmii_tvalid),                                    
      .D2(I_gmii_tvalid ^ 1'b0),                                    
      .R(I_reset),                 
      .S(1'b0)                
   ); 
  
	
genvar j;
generate for (j=0; j<4; j=j+1)
   begin : O_rgmii_tx_data_BUS	
	
   ODDR #(      //使用双边沿触发器，分别在上升沿和下降沿输出RGMII的低4位和高4位数据
      .DDR_CLK_EDGE("SAME_EDGE"),                                   
      .INIT(1'b0),                                       
      .SRTYPE("SYNC")                                      
   ) rgmii_data_ddr (
      .Q(O_rgmii_tx_data_obuf[j]),                      
      .C(I_gmii_tclk),                       
      .CE(1'b1),                            
      .D1(I_gmii_tdata[j]),                                    
      .D2(I_gmii_tdata[j+4]),                                    
      .R(I_reset),                 
      .S(1'b0)                
   );    
		
	end
endgenerate
	 
endmodule
