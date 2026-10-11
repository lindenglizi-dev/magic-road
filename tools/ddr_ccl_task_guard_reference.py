#!/usr/bin/env python3
"""Single-clock, single-task publication guard reference; no DDR/CDC model."""
from __future__ import annotations

import json


class TaskGuard:
    def __init__(self):
        self.state = 'idle'
        self.accepted = []
        self.terminals = []
        self.task_id = self.frame_id = self.reason = 0
        self.started = False
        self.stage = {}
        self.declared = 0
        self.result = None

    def tick(self, *, task=None, stream=None, core_object=None, core_done=False,
             core_count=0, core_reason=0, result_ready=False, cancel=False,
             drain_done=False):
        # stream is (task_id, sof); each pixel/EOL/EOF is an identified event.
        ready = self.state == 'idle'
        accepted = task is not None and ready
        matching = self.state == 'run' and stream is not None and stream[0] == self.task_id
        repeated_sof = matching and stream[1] and self.started
        enabled = matching and not repeated_sof and not cancel
        outputs = {'task_ready': ready, 'accepted': accepted,
                   'core_clear': accepted or (self.state == 'cancel' and drain_done),
                   'stream_enabled': enabled,
                   'rejected_stream': stream is not None and not enabled,
                   'result': self.result if self.state == 'hold' else None}
        if accepted:
            self.task_id, self.frame_id = task
            self.accepted.append((self.task_id, self.frame_id))
            self.reason = 0
            self.started = False
            self.stage = {}
            self.result = None
            self.state = 'run'
        elif self.state == 'run':
            self.reason |= core_reason
            if repeated_sof:
                self.reason |= 1
            if enabled:
                self.started = True
            if core_object is not None:
                index, payload = core_object
                if index not in range(4) or index in self.stage:
                    self.reason |= 16
                if index in range(4):
                    self.stage[index] = payload
            if cancel:
                self.reason |= 32
                self.state = 'cancel'
            elif core_done:
                self.declared = core_count
                self.state = 'flush'
        elif self.state == 'flush':
            self.reason |= core_reason
            if (core_object is not None or self.declared > 4 or
                    set(self.stage) != set(range(self.declared))):
                self.reason |= 16
            self.publish(False)
        elif self.state == 'cancel' and drain_done:
            self.publish(True)
        elif self.state == 'hold' and result_ready:
            self.terminals.append(self.result)
            self.state = 'idle'
        assert len(self.accepted) == len(self.terminals) + int(self.state != 'idle')
        return outputs

    def publish(self, cancelled):
        success = self.reason == 0 and not cancelled
        self.result = {'task_id': self.task_id, 'frame_id': self.frame_id,
                       'success': success, 'cancelled': cancelled, 'reason': self.reason,
                       'count': self.declared if success else 0,
                       'objects': dict(self.stage) if success else {}}
        self.state = 'hold'


def self_check():
    guard = TaskGuard()
    assert guard.tick(task=(10, 100))['accepted']
    assert not guard.tick(task=(11, 101), stream=(11, True))['stream_enabled']
    guard.tick(stream=(11, False))
    guard.tick(core_object=(0, {'area': 5}), core_done=True, core_count=1, core_reason=2)
    guard.tick()
    result = dict(guard.result)
    for _ in range(3):
        assert guard.tick(task=(11, 101))['result'] == result
    assert not result['success'] and result['count'] == 0 and result['reason'] == 2
    guard.tick(result_ready=True)
    guard.tick(task=(11, 101)); guard.tick(core_done=True, core_count=0); guard.tick()
    assert guard.result['success'] and not guard.result['objects']
    guard.tick(result_ready=True)
    guard.tick(task=(12, 102)); guard.tick(core_reason=4); guard.tick()
    guard.tick(core_done=True, core_count=0); guard.tick()
    assert guard.result['reason'] == 4 and not guard.result['success']
    guard.tick(result_ready=True)
    guard.tick(task=(13, 103)); guard.tick(core_object=(0, {'area': 7}),
                                          core_done=True, core_count=1)
    guard.tick()
    assert guard.result['success'] and guard.result['objects'][0]['area'] == 7
    guard.tick(result_ready=True)
    guard.tick(task=(14, 104)); guard.tick(cancel=True)
    assert not guard.tick(stream=(14, False))['stream_enabled']
    assert guard.state == 'cancel'
    assert guard.tick(drain_done=True)['core_clear']
    assert guard.result['cancelled'] and not guard.result['success']
    guard.tick(result_ready=True)
    guard.tick(task=(15, 105)); guard.tick(core_object=(0, {})); guard.tick(core_object=(0, {}))
    guard.tick(core_done=True, core_count=1); guard.tick()
    assert guard.result['reason'] & 16
    guard.tick(result_ready=True)
    guard.tick(task=(16, 106)); guard.tick(stream=(16, True)); guard.tick(stream=(16, True))
    guard.tick(core_done=True); guard.tick()
    assert guard.result['reason'] & 1
    guard.tick(result_ready=True)
    guard.tick(task=(17, 107)); guard.tick(core_object=(1, {}), core_done=True, core_count=1)
    guard.tick()
    assert guard.result['reason'] & 16
    guard.tick(result_ready=True)
    assert len(guard.accepted) == len(guard.terminals) == 8
    return {'status': 'PASS_reference_only', 'accepted': 8, 'terminal': 8,
            'boundary': 'identified streams and explicit external drain ACK, no DDR or CDC'}


if __name__ == '__main__':
    print(json.dumps(self_check(), ensure_ascii=False, indent=2))
