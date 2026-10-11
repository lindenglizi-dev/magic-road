#!/usr/bin/env python3
"""Cycle model for the isolated two-bank CCL pixel-line cache."""
from __future__ import annotations

import json
from dataclasses import dataclass, field


@dataclass
class Bank:
    state: str = 'empty'
    task_id: int = 0
    y: int = 0
    pixels: list[int] = field(default_factory=list)
    frame_last: bool = False


class LineBanks:
    """Model accepted-input ordering, one-cycle reads, holding and cancel."""

    def __init__(self, width: int = 5):
        if width < 1:
            raise ValueError('width must be positive')
        self.width = width
        self.banks = [Bank(), Bank()]
        self.write_bank = 0
        self.read_bank = 0
        self.read_x = 0
        self.pending = None
        self.held = None
        self.protocol_error = False

    @property
    def in_ready(self) -> bool:
        return self.banks[self.write_bank].state in ('empty', 'fill')

    @property
    def empty(self) -> bool:
        return (all(bank.state == 'empty' for bank in self.banks) and
                self.pending is None and self.held is None)

    def tick(self, *, cancel=False, item=None, out_ready=False):
        """Advance one rising edge; item is (task_id, y, pixel, last, frame_last)."""
        output = self.held
        taken = output if output is not None and out_ready and not cancel else None
        accepted = item is not None and self.in_ready and not cancel

        if cancel:
            self.banks = [Bank(), Bank()]
            self.write_bank = self.read_bank = self.read_x = 0
            self.pending = self.held = None
            return {'accepted': False, 'taken': None, 'output': None}

        if taken is not None:
            self.held = None
            if taken['last']:
                self.banks[taken['bank']] = Bank()
                self.read_bank ^= 1
                self.read_x = 0

        if self.pending is not None:
            if self.held is not None:
                raise AssertionError('pending return collided with held output')
            self.held = self.pending
            self.pending = None

        if accepted:
            task_id, y, pixel, last, frame_last = item
            bank = self.banks[self.write_bank]
            if bank.state == 'empty':
                bank.state, bank.task_id, bank.y = 'fill', task_id, y
                bank.pixels = []
            expected_last = len(bank.pixels) == self.width - 1
            bad = ((bank.task_id, bank.y) != (task_id, y) or
                   bool(last) != expected_last or (frame_last and not last))
            bank.pixels.append(int(bool(pixel)))
            if bad:
                self.protocol_error = True
                self.banks[self.write_bank] = Bank()
            elif last:
                bank.state = 'full'
                bank.frame_last = bool(frame_last)
                self.write_bank ^= 1

        bank = self.banks[self.read_bank]
        slot_available = self.pending is None and self.held is None
        if slot_available and bank.state in ('full', 'read'):
            bank.state = 'read'
            self.pending = {
                'bank': self.read_bank, 'task_id': bank.task_id, 'y': bank.y,
                'x': self.read_x, 'pixel': bank.pixels[self.read_x],
                'last': self.read_x == self.width - 1,
                'frame_last': bank.frame_last and self.read_x == self.width - 1,
            }
            self.read_x += 1
        return {'accepted': accepted, 'taken': taken, 'output': output}


def push_line(model, task_id, y, pixels, frame_last=False):
    for x, pixel in enumerate(pixels):
        item = (task_id, y, pixel, x == len(pixels) - 1, frame_last and x == len(pixels) - 1)
        while not model.tick(item=item)['accepted']:
            model.tick()


def drain(model, ready_pattern=(True, False, True)):
    outputs = []
    cycle = 0
    while not model.empty:
        result = model.tick(out_ready=ready_pattern[cycle % len(ready_pattern)])
        if result['taken'] is not None:
            outputs.append(result['taken'])
        cycle += 1
        if cycle > 500:
            raise AssertionError('drain timed out')
    return outputs


def self_check():
    model = LineBanks(5)
    push_line(model, 11, 3, [1, 0, 1, 0, 1])
    push_line(model, 12, 4, [0, 1, 0, 1, 0], True)
    assert not model.in_ready
    outputs = drain(model)
    assert [(v['task_id'], v['y'], v['x'], v['pixel']) for v in outputs] == [
        *((11, 3, x, p) for x, p in enumerate([1, 0, 1, 0, 1])),
        *((12, 4, x, p) for x, p in enumerate([0, 1, 0, 1, 0])),
    ]
    assert outputs[-1]['last'] and outputs[-1]['frame_last']

    push_line(model, 21, 7, [1] * 5)
    push_line(model, 22, 8, [0] * 5)
    model.tick(cancel=True, out_ready=True)
    assert model.empty
    for _ in range(4):
        assert model.tick(out_ready=True)['taken'] is None

    push_line(model, 31, 9, [1, 1, 0, 0, 1])
    while True:
        result = model.tick(out_ready=True)
        if result['taken'] is not None and result['taken']['x'] == 3:
            break
    model.tick(cancel=True, out_ready=True)
    assert model.empty and model.tick(out_ready=True)['taken'] is None

    for bad in (((1, 1, 0, False, False), (2, 1, 0, False, False)),
                ((1, 1, 0, False, False), (1, 2, 0, False, False)),
                ((1, 1, 0, True, False),)):
        check = LineBanks(5)
        for item in bad:
            check.tick(item=item)
        assert check.protocol_error and not check.protocol_error is False

    return {'status': 'PASS_reference_self_check', 'width': 5,
            'checks': ['backpressure', 'bank_order', 'dual_full_cancel',
                       'last_return_cancel', 'task_y_length_errors', 'tag_retention']}


if __name__ == '__main__':
    print(json.dumps(self_check(), ensure_ascii=False, indent=2))
