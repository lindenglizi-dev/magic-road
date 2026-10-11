"""Minimal PW two-group prefetch scheduling contract."""


def payload(position: int, output_group: int, mac_group: int) -> tuple:
    """Return the frozen cache, weight and bias addresses for one accepted group."""
    activation = tuple(position * 16 + mac_group * 8 + lane for lane in range(8))
    weight = tuple(
        (output_group * 3 + output_lane) * 16 + mac_group * 8 + lane
        for output_lane in range(3)
        for lane in range(8)
    )
    bias = tuple(output_group * 3 + output_lane for output_lane in range(3))
    return activation, weight, bias


def simulate(ready, *, position=0, output_group=0, reset_cycles=(), result_fault=False):
    """Model capture-on-accept; reset cancels the prefetched second group."""
    active = True
    group = 0
    held = payload(position, output_group, group)
    accepts = []
    published = False
    for cycle, is_ready in enumerate(ready):
        if cycle in reset_cycles:
            active = False
            group = 0
            held = None
            continue
        before = held
        if active and is_ready:
            assert held == payload(position, output_group, group)
            accepts.append((cycle, group, held))
            if group == 0:
                group = 1
                held = payload(position, output_group, group)
            else:
                active = False
                published = not result_fault
        elif active:
            assert held == before
    return accepts, published, held


def self_check() -> None:
    for position in range(16):
        for output_group in range(8):
            continuous, published, _ = simulate(
                [True, True], position=position, output_group=output_group
            )
            assert [item[0] for item in continuous] == [0, 1]
            assert [item[1] for item in continuous] == [0, 1]
            assert published

            stalled, published, _ = simulate(
                [False, True, False, False, True],
                position=position,
                output_group=output_group,
            )
            assert [item[0] for item in stalled] == [1, 4]
            assert [item[1] for item in stalled] == [0, 1]
            assert published

    before_first, published, held = simulate([True, True], reset_cycles={0})
    assert before_first == [] and not published and held is None

    after_prefetch, published, held = simulate([True, True], reset_cycles={1})
    assert [item[1] for item in after_prefetch] == [0]
    assert not published and held is None

    faulted, published, _ = simulate([True, True], result_fault=True)
    assert [item[1] for item in faulted] == [0, 1]
    assert not published

    print(
        "PW_PREFETCH_CONTRACT_PASS positions=16 output_groups=8 "
        "continuous_accepts=0,1 stalled_accepts=1,4 resets=2 last_fault_cancel=1"
    )


if __name__ == "__main__":
    self_check()
