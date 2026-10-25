# tb_road_frame_ready_dispatch

Portless100MHz self-checking protocol testbench using the real slot state machine through tb_road_dispatch_fixture. It checks the cases listed in verification_plan.txt with full225-bit job comparisons, controlled identity capture timestamps distinct from slot diagnostic timestamps, and task numbers independent of source frame IDs.

The explicit task-maximum test depositsFFFFFFFF into the documented next-task register, accepts that last task once and requires wrap_fault to block subsequent claims/jobs until reset. It does not claim billions of real tasks were executed. Common reset is exercised while claim/job is backpressured and while RUN owns a slot.

Timing: job_valid may precede job_ready by16cycles while its complete descriptor and mismatch flag remain fixed. After accepted NNdone, the actual reading mask remains asserted until a separately matching last_read event. Conversely, after last_read first, a recaptured identity must remain backpressured until the old taskdone retires its context.

Review regressions add late duplicate identities after context caching and during claim backpressure. Neither may claim either READY slot. The claim-hold assertion is bypassed only during this explicitly illegal-candidate probe, because the documented preclaim guard must cancel the candidate rather than preserve an invalid claim.

[Protocol timing](dispatch_timing.svg) is rendered with the governed WaveDrom runtime.
