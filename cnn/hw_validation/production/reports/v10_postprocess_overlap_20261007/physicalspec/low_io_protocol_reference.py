"""Reference framing for the v10 16-bit physical-validation port."""

from dataclasses import dataclass, field


TABLE_BEGIN = 0x1000
LOAD_BEGIN = 0x2000
START_DW_PW = 0x3000
START_PW_ONLY = 0x3001
EXPORT = 0x4000
COMMIT_BLOCK = 0x6000
COMMIT_ALLOW = 0x6001


def signed32(low: int, high: int) -> int:
    """Join two little-endian 16-bit words into one signed 32-bit value."""
    value = ((high & 0xFFFF) << 16) | (low & 0xFFFF)
    return value - (1 << 32) if value & (1 << 31) else value


def encode_result(index: int, value: int) -> tuple[int, int]:
    """Encode one indexed INT8 result as metadata then data."""
    if not 0 <= index < 512 or not -128 <= value <= 127:
        raise ValueError("result outside physical protocol range")
    return 0x8000 | index, 0x9000 | (value & 0xFF)


@dataclass
class Decoder:
    """Decode accepted RX words; ready/valid timing remains an RTL concern."""

    state: str = "command"
    table_addr: int = 0
    descriptor: int = 0
    low_word: int = 0
    actions: list[tuple] = field(default_factory=list)

    def accept(self, word: int) -> None:
        if not 0 <= word <= 0xFFFF:
            raise ValueError("RX word must be unsigned 16-bit")
        if self.state == "table":
            self.actions.append(("table", self.table_addr, word))
            self.table_addr += 1
            if self.table_addr == 1024:
                self.state = "command"
            return
        if self.state == "descriptor":
            if word & 0x1800:
                raise ValueError("load descriptor reserved bits are nonzero")
            self.descriptor = word
            self.state = "load_low"
            return
        if self.state == "load_low":
            self.low_word = word
            self.state = "load_high"
            return
        if self.state == "load_high":
            self.actions.append(
                ("load", (self.descriptor >> 13) & 0x7, self.descriptor & 0x7FF,
                 signed32(self.low_word, word))
            )
            self.state = "command"
            return

        if word == TABLE_BEGIN:
            self.table_addr = 0
            self.state = "table"
        elif word == LOAD_BEGIN:
            self.state = "descriptor"
        elif word in (START_DW_PW, START_PW_ONLY):
            self.actions.append(("start", word == START_PW_ONLY))
        elif word == EXPORT:
            self.actions.append(("export",))
        elif word in (COMMIT_BLOCK, COMMIT_ALLOW):
            self.actions.append(("commit_ready", bool(word & 1)))
        else:
            raise ValueError(f"unsupported command 0x{word:04x}")


def _self_check() -> None:
    decoder = Decoder()
    decoder.accept(LOAD_BEGIN)
    decoder.accept((5 << 13) | 0x345)
    decoder.accept(0xCDEF)
    decoder.accept(0x89AB)
    decoder.accept(START_PW_ONLY)
    decoder.accept(COMMIT_ALLOW)
    decoder.accept(COMMIT_BLOCK)
    decoder.accept(EXPORT)
    assert decoder.actions == [
        ("load", 5, 0x345, -1985229329),
        ("start", True),
        ("commit_ready", True),
        ("commit_ready", False),
        ("export",),
    ]
    assert encode_result(511, -1) == (0x81FF, 0x90FF)

    table = Decoder()
    table.accept(TABLE_BEGIN)
    for address in range(1024):
        table.accept(address)
    assert table.state == "command"
    assert table.actions[-1] == ("table", 1023, 1023)


if __name__ == "__main__":
    _self_check()
    print("PASS low_io_protocol_reference")
