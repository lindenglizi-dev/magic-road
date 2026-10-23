// Minimal compatible shape of Croc sbr_obi_* types for standalone IP testing.
// NOT a replacement for Croc's real croc_pkg.sv during SoC integration.
package croc_pkg;
  typedef struct packed {
    logic [31:0] addr;
    logic we;
    logic [3:0] be;
    logic [31:0] wdata;
    logic [2:0] aid;
    logic a_optional;
  } sbr_obi_a_chan_t;
  typedef struct packed { sbr_obi_a_chan_t a; logic req; } sbr_obi_req_t;
  typedef struct packed {
    logic [31:0] rdata;
    logic [2:0] rid;
    logic err;
    logic r_optional;
  } sbr_obi_r_chan_t;
  typedef struct packed {
    sbr_obi_r_chan_t r;
    logic gnt;
    logic rvalid;
  } sbr_obi_rsp_t;
  typedef struct packed { integer DataWidth; integer IdWidth; } fake_cfg_t;
  localparam fake_cfg_t SbrObiCfg = {32'd32, 32'd3};
endpackage
