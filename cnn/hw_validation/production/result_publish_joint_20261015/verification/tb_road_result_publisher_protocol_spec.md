# tb_road_result_publisher_protocol

Portless 100MHz direct-drive testbench for publisher guard branches only. Its controlled table signals do not establish C8 CDC or ROM behavior; the complete-chain testbench owns that evidence.

Success counts0,1 and64 check exact265-bit metadata, FINAL97 direct forwarding,32-cycle metadata hold,32-cycle committed cancel/fault hold, and copy_ack retirement. Invalid entry token, invalid completion token, count mismatch, simultaneous entry and done, completion before capture, pipeline fault, table error, cancel,65th valid and META ready simultaneous with cancel/fault/error/unexpected entry each require immediate publication blocking, an ABORT pulse, pipeline cancellation and bounded return to idle. Admission while source busy is prohibited. Upstream valid must remain asserted while pipeline ready is low. Common reset is exercised in RUN, META and WAIT_ACK.

There is no arithmetic model in this testbench. Inputs and expected protocol outcomes directly follow the frozen publisher contract. A hard100us watchdog prevents an unbounded test.

The legal publication sequence is illustrated by the shared [timing diagram](spec_waveform.svg): last entry acceptance, later done, metadata valid held until ready, then copy acknowledgement. Malformed preseal cases replace the metadata phase with ABORT; WAIT_ACK cases preserve the committed metadata until acknowledgement.
