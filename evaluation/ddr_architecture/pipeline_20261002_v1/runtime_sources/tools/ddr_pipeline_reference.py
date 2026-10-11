"""Single-task ownership contract; no DDR, classifier or display implementation."""
from dataclasses import dataclass


@dataclass
class Pipeline:
    state: str = 'idle'
    identity: tuple = ()
    candidates: int = 0
    read_count: int = 0
    pending_read: bool = False
    candidate_success: bool = False
    final_success: bool = False
    accepted: int = 0
    terminals: int = 0
    displayed: int = 0

    def accept(self, identity):
        assert self.state == 'idle'
        self.identity = identity
        self.state = 'run'
        self.accepted += 1

    def candidate_done(self, count, success):
        assert self.state == 'run' and 0 <= count <= 4
        self.candidates = count if success else 0
        self.candidate_success = success
        self.read_count = 0
        self.state = 'candidate'

    def read_request(self, index):
        assert self.state == 'candidate' and self.candidate_success
        assert not self.pending_read and index == self.read_count < self.candidates
        self.pending_read = True

    def read_response_taken(self):
        assert self.pending_read
        self.pending_read = False
        self.read_count += 1

    def release_table(self):
        if self.pending_read or self.read_count != self.candidates:
            return False
        assert self.state == 'candidate'
        self.state = 'processed' if self.candidate_success else 'final'
        self.final_success = False
        return True

    def processed(self, identity, completed, accepted, error=False):
        assert self.state == 'processed'
        self.final_success = (identity == self.identity and not error and
                              completed == self.candidates and
                              0 <= accepted <= completed)
        self.state = 'final'

    def display_commit(self):
        assert self.state == 'final' and self.final_success
        self.displayed += 1
        self.terminals += 1
        self.state = 'idle'

    def failure_ack(self):
        assert self.state == 'final' and not self.final_success
        self.terminals += 1
        self.state = 'idle'

    def cancel(self):
        assert self.state == 'run'
        self.state = 'drain'

    def drain(self, banks_empty):
        if banks_empty:
            assert self.state == 'drain'
            self.state = 'reset_core'

    def reset_core(self):
        assert self.state == 'reset_core'
        self.state = 'recover'

    def recovered(self, core_idle, error):
        assert self.state == 'recover'
        if core_idle and not error:
            self.state = 'run'
            self.candidate_done(0, False)


def self_check():
    p = Pipeline()
    p.accept((1, 101)); p.candidate_done(4, True)
    for i in range(4):
        p.read_request(i)
        assert not p.release_table()  # Last request is still not a last response.
        p.read_response_taken()
    assert p.release_table() and p.state == 'processed'
    p.processed((1, 101), 2, 2, error=True)
    assert not p.final_success  # Two local classifications cannot publish four.
    try:
        p.display_commit()
    except AssertionError:
        pass
    else:
        raise AssertionError('failure changed the display')
    p.failure_ack()
    p.accept((2, 102)); p.candidate_done(0, True)
    assert p.release_table()
    p.processed((2, 102), 0, 0)
    assert p.final_success  # Empty success differs from a failed frame.
    p.display_commit()
    p.accept((3, 103)); p.candidate_done(1, True)
    p.read_request(0); p.read_response_taken(); assert p.release_table()
    p.processed((3, 103), 1, 0)
    assert p.final_success  # All correctly processed candidates may be rejected.
    p.display_commit()
    assert p.accepted == p.terminals == 3 and p.displayed == 2
    p.accept((4, 104)); p.cancel(); p.drain(False)
    assert p.state == 'drain'  # Stopping VALID alone cannot prove drain.
    p.drain(True); p.reset_core(); p.recovered(False, True)
    assert p.state == 'recover'
    p.recovered(True, False)
    assert p.state == 'candidate' and not p.candidate_success
    assert p.release_table(); p.failure_ack()
    assert p.accepted == p.terminals == 4 and p.displayed == 2
    return {'status': 'PASS', 'tasks': 4, 'display_commits': 2, 'failure_acks': 2}


if __name__ == '__main__':
    print(self_check())
