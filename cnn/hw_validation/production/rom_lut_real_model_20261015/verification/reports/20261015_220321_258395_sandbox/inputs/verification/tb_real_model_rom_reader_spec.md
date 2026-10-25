# tb_real_model_rom_reader

100 MHz simulation clock; common active-low asynchronous reset. Single actual reader with real PH1P ERAM initialization. Test-only golden 7168 x 160-bit array compares all 143360 bytes; each response remains stable until ready. Acceptance cycle is the request handshake rising edge; response cycle is the first rising edge exposing response valid.

Checks: all 7168 words and 143360 byte slices; 28 group edges; payload tail at word 7026 with two valid bytes; 2838 zero padding bytes; 37-cycle holds; common reset during WAIT and held RESPONSE; illegal address 7168 faults without completion for 37 observed cycles. Watchdog prevents hung runs.

Timing scenario: `request valid + ready → eight reader WAIT cycles → response valid held → response ready`. Full CSV records each acceptance/response cycle and hold duration. This is functional simulation, not silicon timing.
