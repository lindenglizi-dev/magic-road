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
    committed: int = 0

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
        assert self.state == 'final'
        self.committed += 1
        self.state = 'idle'


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
    p.display_commit()
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
    assert p.accepted == p.committed == 3
    return {'status': 'PASS', 'tasks': 3}


if __name__ == '__main__':
    print(self_check())
