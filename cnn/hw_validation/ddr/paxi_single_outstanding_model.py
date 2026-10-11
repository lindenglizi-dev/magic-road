"""Behavior reference for the isolated one-request PAXI bridge."""

from dataclasses import dataclass
from enum import Enum, auto
from random import Random


BASE = 0x0340_0000
END = 0x0400_0000


class State(Enum):
    IDLE = auto()
    CHECK = auto()
    READ_ADDR = auto()
    READ_RETURN = auto()
    WRITE_ADDR = auto()
    WRITE_DATA = auto()
    WRITE_COMMIT = auto()
    RESULT = auto()
    FAULT = auto()


def legal_address(byte_addr: int) -> bool:
    return BASE <= byte_addr <= END - 16 and byte_addr % 16 == 0


@dataclass
class Request:
    write: bool
    byte_addr: int
    data: int
    mask: int
    epoch: int
    owner: int


class BridgeModel:
    def __init__(self) -> None:
        self.state = State.IDLE
        self.request: Request | None = None
        self.cancelled = False
        self.aw_accepted = False
        self.result: tuple[Request, int] | None = None
        self.accepted_count = 0
        self.success_count = 0
        self.cancelled_drain_count = 0
        self.late_discard_count = 0
        self.protocol_fault = False

    @property
    def drain_done(self) -> bool:
        return self.state is State.IDLE and self.result is None

    def accept_request(self, request: Request) -> bool:
        if self.state is not State.IDLE or not legal_address(request.byte_addr):
            if self.state is State.IDLE:
                self._fault()
            return False
        self.request = request
        self.cancelled = False
        self.aw_accepted = False
        self.state = State.CHECK
        return True

    def cancel(self) -> None:
        if self.request is None:
            return
        self.cancelled = True
        if self.state is State.CHECK:
            self.state = State.IDLE
            self.request = None
            self.cancelled_drain_count += 1
        elif self.state is State.RESULT:
            self.state = State.IDLE
            self.result = None
            self.request = None
            self.cancelled_drain_count += 1

    def tick(
        self,
        *,
        arready: bool = False,
        awready: bool = False,
        wready: bool = False,
        rvalid: bool = False,
        rlast: bool = True,
        rdata: int = 0,
        commit_confirmed: bool = False,
        result_ready: bool = False,
    ) -> None:
        if rvalid and self.state is not State.READ_RETURN:
            self._fault()
            return
        if commit_confirmed and self.state is not State.WRITE_COMMIT:
            self._fault()
            return
        if self.state is State.CHECK:
            assert self.request is not None
            self.state = State.WRITE_ADDR if self.request.write else State.READ_ADDR
        elif self.state is State.READ_ADDR and arready:
            self.state = State.READ_RETURN
            self.accepted_count += 1
        elif self.state is State.READ_RETURN and rvalid:
            if not rlast:
                self._fault()
            elif self.cancelled:
                self.state = State.IDLE
                self.request = None
                self.late_discard_count += 1
                self.cancelled_drain_count += 1
            else:
                assert self.request is not None
                self.result = (self.request, rdata)
                self.state = State.RESULT
        elif self.state is State.WRITE_ADDR and awready:
            self.aw_accepted = True
            self.state = State.WRITE_DATA
        elif self.state is State.WRITE_DATA and wready:
            self.state = State.WRITE_COMMIT
            self.accepted_count += 1
        elif self.state is State.WRITE_COMMIT and commit_confirmed:
            if self.cancelled:
                self.state = State.IDLE
                self.request = None
                self.late_discard_count += 1
                self.cancelled_drain_count += 1
            else:
                assert self.request is not None
                self.result = (self.request, 0)
                self.state = State.RESULT
        elif self.state is State.RESULT and result_ready:
            self.state = State.IDLE
            self.result = None
            self.request = None
            self.success_count += 1

    def _fault(self) -> None:
        self.protocol_fault = True
        self.state = State.FAULT
        self.result = None


def self_check() -> None:
    assert legal_address(BASE)
    assert legal_address(END - 16)
    assert not legal_address(BASE - 16)
    assert not legal_address(END)
    assert not legal_address(BASE + 1)

    rng = Random(0x51B)
    write = Request(True, BASE, rng.getrandbits(128), 0x8421, 7, 11)
    model = BridgeModel()
    assert model.accept_request(write)
    model.tick()
    model.tick(awready=False, wready=True)
    assert model.state is State.WRITE_ADDR
    model.tick(awready=True, wready=False)
    assert model.state is State.WRITE_DATA and model.request == write
    model.tick(wready=False)
    assert model.state is State.WRITE_DATA and model.request.mask == 0x8421
    model.tick(wready=True)
    assert model.state is State.WRITE_COMMIT and model.accepted_count == 1
    model.tick(commit_confirmed=True)
    model.tick(result_ready=True)
    assert model.drain_done and model.success_count == 1

    read = Request(False, BASE + 16, 0, 0, 8, 12)
    model = BridgeModel()
    assert model.accept_request(read)
    model.tick()
    model.tick(arready=True)
    model.cancel()
    assert model.state is State.READ_RETURN and not model.drain_done
    model.tick(rvalid=True, rlast=True, rdata=rng.getrandbits(128))
    assert model.drain_done and model.late_discard_count == 1
    assert model.success_count == 0

    model = BridgeModel()
    assert model.accept_request(read)
    model.cancel()
    assert model.drain_done and model.cancelled_drain_count == 1

    model = BridgeModel()
    assert model.accept_request(read)
    model.tick()
    model.tick(arready=True)
    model.tick(rvalid=True, rlast=False)
    assert model.protocol_fault and model.state is State.FAULT

    model = BridgeModel()
    model.tick(rvalid=True)
    assert model.protocol_fault

    model = BridgeModel()
    assert model.accept_request(write)
    model.tick()
    model.tick(commit_confirmed=True)
    assert model.protocol_fault

    model = BridgeModel()
    assert not model.accept_request(Request(False, END, 0, 0, 1, 1))
    assert model.protocol_fault

    model = BridgeModel()
    assert model.accept_request(read)
    model.tick()
    model.cancel()
    assert model.state is State.READ_ADDR and model.cancelled
    model.tick(arready=False)
    assert model.state is State.READ_ADDR
    model.tick(arready=True)
    model.tick(rvalid=True, rlast=True)
    assert model.accepted_count == 1
    assert model.late_discard_count == 1 and model.success_count == 0


if __name__ == "__main__":
    self_check()
    print("H1-B Python behavior reference: PASS")
