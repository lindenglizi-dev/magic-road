"""Minimal transaction-level contract for the one-slot PAXI mailbox."""

from dataclasses import dataclass

ADDR_FIRST = 0x1A00000
ADDR_LIMIT = 0x2000000
ERR_ADDR = 0x1
ERR_PHY = 0x2
ERR_LAST = 0x4
ERR_PROTOCOL = 0x8


@dataclass(frozen=True)
class Request:
    write: bool
    addr: int
    data: int = 0


@dataclass(frozen=True)
class Response:
    data: int
    error: int


def address_error(addr: int) -> int:
    """Return the address error bit for the native PAXI reservation."""
    return ERR_ADDR if not (ADDR_FIRST <= addr < ADDR_LIMIT and addr % 8 == 0) else 0


class MailboxModel:
    """Single-owner model: accept, endpoint completion, then source consume."""

    def __init__(self) -> None:
        self.request = None
        self.response = None
        self.fault = False

    def accept(self, request: Request, phy_ready: bool = True) -> None:
        assert self.request is None and self.response is None and not self.fault
        error = address_error(request.addr) | (0 if phy_ready else ERR_PHY)
        self.request = request
        if error:
            self.publish(0, error)

    def publish(self, data: int = 0, error: int = 0) -> None:
        assert self.request is not None and self.response is None
        assert 0 <= data < (1 << 128) and 0 <= error < 16
        self.response = Response(data, error)
        self.fault |= bool(error)

    def consume(self) -> Response:
        assert self.response is not None
        response = self.response
        self.request = None
        self.response = None
        return response

    def common_reset(self) -> None:
        self.__init__()


def _self_check() -> None:
    model = MailboxModel()
    model.accept(Request(True, ADDR_FIRST, 0x1234))
    model.publish()
    assert model.consume() == Response(0, 0)
    model.accept(Request(False, ADDR_FIRST + 8))
    model.publish((1 << 128) - 1)
    assert model.consume().data == (1 << 128) - 1
    model.accept(Request(False, ADDR_FIRST + 1))
    assert model.consume().error == ERR_ADDR and model.fault
    model.common_reset()
    assert not model.fault and model.request is None


if __name__ == "__main__":
    _self_check()
    print("PASS mailbox_reference")
