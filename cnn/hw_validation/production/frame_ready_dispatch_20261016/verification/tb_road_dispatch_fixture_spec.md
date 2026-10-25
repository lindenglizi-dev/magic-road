# tb_road_dispatch_fixture

100MHz simulation helper instantiating the frozen road_capture_slots and new dispatcher, with one common low-active reset. It implements controlled SOF, complete/partial EOF bytes, write-visible identity and already-crossed128-bit source identity inputs. It holds claim and job payloads under backpressure, checks actual pre-edge READING on release, and logs every accepted225-bit job.

It does not implement camera admission credit, CDC, pixel capture, DMA, NN inference or DDR completion. Its last_read task explicitly injects a service fact rather than deriving it from NNdone. External done can come from the controlled joint pipeline; manual done is available to the standalone ownership test.

Timing: capture allocation→identity/EOF in either order→write_visible→READY→claim→READING→job accept→independent taskdone/lastresponse consumption→task retirement. NNdone alone leaves READING intact. A matching consumed final response may free the slot before taskdone while the dispatcher retains its old identity context.

[Protocol timing](dispatch_timing.svg) shows the independent milestones.
