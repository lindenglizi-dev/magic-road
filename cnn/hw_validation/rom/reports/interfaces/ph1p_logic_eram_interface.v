module PH1P_LOGIC_ERAM (
  dia,
  addra, cea, ocea, clka, wea, rsta, bea,
  dib,
  addrb, ceb, oceb, clkb, web, rstb, beb,
  ecc_sbiterrinj, ecc_dbiterrinj,
  doa,
  dob,
  ecc_sbiterr,
  ecc_dbiterr
  );
parameter DATA_WIDTH_A = 20;
parameter DATA_WIDTH_B = DATA_WIDTH_A;
parameter ADDR_WIDTH_A = 10;
parameter ADDR_WIDTH_B = ADDR_WIDTH_A;
parameter DATA_DEPTH_A = 2 ** ADDR_WIDTH_A;
parameter DATA_DEPTH_B = 2 ** ADDR_WIDTH_B;
parameter BYTE_ENABLE = 0;
parameter BYTE_A = BYTE_ENABLE == 0 ? 1 : DATA_WIDTH_A / BYTE_ENABLE;
parameter BYTE_B = BYTE_ENABLE == 0 ? 1 : DATA_WIDTH_B / BYTE_ENABLE;
output ecc_sbiterr;
output ecc_dbiterr;
output [DATA_WIDTH_A-1:0] doa;
output [DATA_WIDTH_B-1:0] dob;
input [DATA_WIDTH_A-1:0] dia;
input [DATA_WIDTH_B-1:0] dib;
input ecc_sbiterrinj;
input ecc_dbiterrinj;
input cea;
input ocea;
input clka;
input wea;
input rsta;
input ceb;
input oceb;
input clkb;
input web;
input rstb;
input [BYTE_A - 1 : 0] bea;
input [BYTE_B - 1 : 0] beb;
input [ADDR_WIDTH_A-1:0] addra;
input [ADDR_WIDTH_B-1:0] addrb;
endmodule
