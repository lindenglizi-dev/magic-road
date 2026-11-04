module ethernet_image_link #(parameter LOCAL_IP=32'hc0a88902)(
 input sys_clk,pclk,rst_n,input vsync,de,input [23:0] rgb,
 input [15:0] view_tag,
 input [3:0] rgmii_rxd,input rgmii_rx_ctl,rgmii_rxc,
 output [3:0] rgmii_txd,output rgmii_tx_ctl,rgmii_txc,phy_rst_n,mdc,inout mdio,
 output [31:0] network_status,
 output [7:0] rx_data,output rx_valid,
 input tx_start,input [7:0] tx_command,tx_seq,tx_length,tx_data,output [5:0] tx_index,output tx_busy);
 wire clk125,clk90,clk25,locked;
 ethernet_pll u_eth_pll(.refclk(sys_clk),.reset(!rst_n),.lock(locked),.clk0_out(clk125),.clk1_out(clk90),.clk2_out(clk25));
 wire reset_n=rst_n&&locked;
 wire phy_ready;
 yt8511_init u_phy(.clk(sys_clk),.rst_n(reset_n),.phy_rst_n(phy_rst_n),.mdc(mdc),.mdio(mdio),.ready(phy_ready),.status(network_status));
 (* ASYNC_REG="TRUE" *) reg [1:0] er,pr;
 always @(posedge clk125 or negedge reset_n)if(!reset_n)begin er<=0;pr<=0;end else begin er<={er[0],1'b1};pr<={pr[0],phy_ready};end
 wire reset=!er[1];
 wire [7:0] gd_rx;wire uv_rx;
 wire [7:0] gd,rd,ud,td;wire gv,rv,uv,req,busy;wire rxclk;wire [15:0] len,rlen,srcport;
 wire [31:0] source_ip;reg [31:0] peer_ip;reg [15:0] peer_port;
 wire mac_error,ip_error;
 reg [7:0] rxindex;reg [31:0] magic;reg [28:0] lease;reg subscribed;
 reg enabled;
 always @(posedge clk125 or negedge er[1])
 if(!er[1])enabled<=0;else enabled<=subscribed&&lease!=0&&pr[1];
                                                                              
                                                                                   
 always @(posedge clk125 or posedge reset)begin
 if(reset)begin rxindex<=0;magic<=0;lease<=0;subscribed<=0;peer_ip<=32'hc0a88901;peer_port<=6001;end
 else begin
 if(lease!=0)lease<=lease-1'b1;
 if(!rv)begin rxindex<=0;magic<=0;end
 else begin
 if(rxindex<4)magic<={rd,magic[31:8]};
 if(rxindex==4&&magic==32'h53565848&&rlen==5)begin
 peer_ip<=source_ip;peer_port<=srcport;subscribed<=rd==1;lease<=29'd375000000;
 end
 if(rxindex!=255)rxindex<=rxindex+1'b1;
 end
 end end
 eth_rx_mailbox u_rx(.eclk(clk125),.sclk(sys_clk),.rst_n(er[1]),.data(rd),
 .valid(rv&&srcport==peer_port&&source_ip==peer_ip),.length(rlen),.sdata(rx_data),.svalid(rx_valid));
 wire reply_available,reply_pop;wire [7:0] rc,rs,rl,rp;wire [5:0] ri;
 eth_reply_mailbox u_reply(.sclk(sys_clk),.eclk(clk125),.rst_n(reset_n),.start(tx_start),.command(tx_command),.seq(tx_seq),
 .length(tx_length),.payload_data(tx_data),.payload_index(tx_index),.busy(tx_busy),.available(reply_available),.pop(reply_pop),.ecommand(rc),.eseq(rs),.elength(rl),.read_index(ri),.epayload_byte(rp));
 wire video_available,video_pop;wire [10:0] vi;wire [7:0] vd;wire [31:0] dropped;
 eth_video_queue u_video(.pclk(pclk),.tclk(clk125),.rst_n(er[1]),.enable(enabled),.vsync(vsync),.de(de),.rgb(rgb),.view_tag(view_tag),
 .available(video_available),.pop(video_pop),.byte_index(vi),.byte_data(vd),.dropped(dropped));
 eth_udp_sender u_sender(.clk(clk125),.rst_n(er[1]),.enabled(enabled),.link_ready(pr[1]),.udp_busy(busy),.gmii_valid(gv),
 .udp_req(req),.udp_valid(uv),.udp_data(ud),.udp_length(len),.video_available(video_available),.video_pop(video_pop),
 .video_index(vi),.video_data(vd),.reply_available(reply_available),.reply_pop(reply_pop),.reply_command(rc),.reply_seq(rs),.reply_length(rl),.reply_index(ri),.reply_data(rp));
 uiudp_stack u_stack(.I_uclk(clk125),.I_reset(reset),.I_mac_local_addr(48'h020000351a01),.I_udp_local_port(16'd6002),
 .I_ip_local_addr(LOCAL_IP),.I_udp_dest_port(peer_port),.I_ip_dest_addr(peer_ip),.O_R_ip_source_addr(source_ip),
 .O_W_udp_busy(busy),.I_W_udp_req(req),.I_W_udp_valid(uv),.I_W_udp_data(ud),.I_W_udp_len(len),
 .O_R_udp_valid(rv),.O_R_udp_data(rd),.O_R_udp_len(rlen),.O_R_udp_src_port(srcport),
 .I_gmii_rclk(rxclk),.I_gmii_rvalid(uv_rx),.I_gmii_rdata(gd_rx),.I_gmii_tclk(clk125),.O_gmii_tvalid(gv),.O_gmii_tdata(gd),
 .O_ip_rerror(ip_error),.O_mac_rerror(mac_error));

 rgmii_interface u_rgmii(.speed_10_100(1'b0),.gmii_tx_clk_d(clk125),.gmii_tx_reset_d(reset),.gmii_tx_reset(reset),
 .gmii_tx_clk(clk125),.gmii_txd(gd),.gmii_tx_en(gv),.gmii_tx_er(1'b0),
 .gmii_rx_reset(reset),.gmii_rx_clk(rxclk),.gmii_rxd(gd_rx),.gmii_rx_dv(uv_rx),.gmii_rx_er(),
 .rgmii_txd(rgmii_txd),.rgmii_tx_ctl(rgmii_tx_ctl),.rgmii_txc(rgmii_txc),.rgmii_rxd(rgmii_rxd),
 .rgmii_rx_ctl(rgmii_rx_ctl),.rgmii_rxc(rgmii_rxc),.gmii_crs(),.gmii_col(),.link_status(),.clock_speed(),.duplex_status());
endmodule
