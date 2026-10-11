"""Bounded DW scalar dispatch contract; not a whole-postprocess timing model."""

from collections import deque


def check_queue(limit, downstream_ready, cancel_at=None):
    """Model pre-edge readiness: at most two entries plus a held raw triple."""
    pending = deque()
    source = deque(range(3))
    delivered = []
    accepted = []
    peak = 0
    cancelled = 0
    for cycle in range(100):
        if cycle == cancel_at:
            cancelled += len(pending) + len(source)
            pending.clear()
            source.clear()
        pop = bool(pending) and downstream_ready(cycle)
        push = bool(source) and len(pending) < limit and len(pending) < 2
        if pop:
            delivered.append(pending.popleft())
        if push:
            pending.append(source.popleft())
            accepted.append(cycle)
        peak = max(peak, len(pending))
        assert len(pending) <= 2
        assert len(delivered) + len(pending) + len(source) + cancelled == 3
        if not source and not pending:
            break
    assert delivered == list(range(len(delivered)))
    if cancel_at is None:
        assert delivered == [0, 1, 2]
    return accepted, peak, cancelled


def main():
    old = check_queue(1, lambda cycle: True)
    new = check_queue(2, lambda cycle: True)
    assert old[0] == [0, 2, 4] and new[0] == [0, 1, 2]
    for limit in (1, 2):
        check_queue(limit, lambda cycle: cycle > 64)
        check_queue(limit, lambda cycle: cycle % 3 == 0)
        for cancel_at in range(5):
            check_queue(limit, lambda cycle: cycle > 64, cancel_at)
    assert check_queue(2, lambda cycle: cycle > 64)[1] == 2
    print('QUEUE_CONTRACT_PASS old_accepts=0,2,4 new_accepts=0,1,2 capacity=2')
    print('BOUNDARY_PASS long_stall=64 alternating_ready=1 cancellation_cases=10')


if __name__ == '__main__':
    main()
