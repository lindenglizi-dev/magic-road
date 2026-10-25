"""Reproduce the bounded record-FIFO scheduling proof for road_area_resize."""

from collections import deque


RECORD_LENGTHS = (1, 2, 1, 2, 2)
ACTIVE_BEATS = 320
FIFO_DEPTH = 128


def simulate(line_interval, rows=2):
    arrivals = {
        row * line_interval + beat: (row, beat, RECORD_LENGTHS[beat % 5])
        for row in range(rows)
        for beat in range(ACTIVE_BEATS)
    }
    fifo = deque()
    held_second = False
    read_pointer = 0
    write_pointer = 0
    maximum_records = 0
    maximum_pending_pixels = 0
    bypass_cycles = 0
    simultaneous_push_pop_cycles = 0
    same_address_read_write = 0
    overflow = None

    final_arrival = (rows - 1) * line_interval + ACTIVE_BEATS - 1
    for cycle in range(final_arrival + 4096):
        arrival = arrivals.get(cycle)

        worker_from_second = held_second
        worker_from_fifo = not worker_from_second and bool(fifo)
        worker_from_new = arrival is not None and not worker_from_second and not worker_from_fifo
        fifo_push = arrival is not None and not worker_from_new
        fifo_pop = worker_from_fifo

        if fifo_push and len(fifo) == FIFO_DEPTH:
            source_row, source_beat, _ = arrival
            overflow = (cycle, source_row, source_beat)
            break

        if fifo_push and fifo_pop:
            simultaneous_push_pop_cycles += 1
            if write_pointer == read_pointer:
                same_address_read_write += 1

        if worker_from_second:
            held_second = False
        elif worker_from_fifo:
            record_length = fifo.popleft()
            read_pointer = (read_pointer + 1) % FIFO_DEPTH
            held_second = record_length == 2
        elif worker_from_new:
            _, _, record_length = arrival
            bypass_cycles += 1
            held_second = record_length == 2

        if fifo_push:
            _, _, record_length = arrival
            fifo.append(record_length)
            write_pointer = (write_pointer + 1) % FIFO_DEPTH

        pending_pixels = sum(fifo) + int(held_second)
        maximum_records = max(maximum_records, len(fifo))
        maximum_pending_pixels = max(maximum_pending_pixels, pending_pixels)

        if cycle > final_arrival and not fifo and not held_second:
            break
    else:
        raise RuntimeError("simulation did not drain")

    return {
        "line_interval": line_interval,
        "rows": rows,
        "max_records": maximum_records,
        "max_pending_pixels": maximum_pending_pixels,
        "bypass_cycles": bypass_cycles,
        "simultaneous_push_pop_cycles": simultaneous_push_pop_cycles,
        "same_address_read_write": same_address_read_write,
        "overflow": overflow,
    }


def main():
    expected = {
        800: (120, 192, None),
        512: (120, 192, None),
        320: (128, 205, (342, 1, 22)),
    }
    for line_interval in (800, 512, 320):
        result = simulate(line_interval)
        observed = (
            result["max_records"],
            result["max_pending_pixels"],
            result["overflow"],
        )
        assert observed == expected[line_interval], (observed, expected[line_interval])
        print(result)


if __name__ == "__main__":
    main()
