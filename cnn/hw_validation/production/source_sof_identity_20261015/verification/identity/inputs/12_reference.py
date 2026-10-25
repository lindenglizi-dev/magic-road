"""Edge model for held source-SOF CDC and fixed age text; stdlib only.

Inputs are sampled BEFORE an edge, returned state is AFTER that edge. Call
camera_edge/time_edge in actual edge order. For simultaneous edges, snapshot
both models before updating; independent source clocks and reset release are
environment assumptions, not analog CDC or physical timing proof.
"""

from dataclasses import dataclass, field
import argparse
import hashlib
import json
from pathlib import Path

U32 = (1 << 32) - 1
U64 = (1 << 64) - 1
TIMEOUT = 120000

# Seven rows, five bits per row, MSB is left. Fixed row-bitmap mechanism.
FONT = {
    " ": (0, 0, 0, 0, 0, 0, 0),
    "0": (14, 17, 19, 21, 25, 17, 14),
    "1": (4, 12, 4, 4, 4, 4, 14),
    "2": (14, 17, 1, 2, 4, 8, 31),
    "3": (30, 1, 1, 14, 1, 1, 30),
    "4": (2, 6, 10, 18, 31, 2, 2),
    "5": (31, 16, 16, 30, 1, 1, 30),
    "6": (14, 16, 16, 30, 17, 17, 14),
    "7": (31, 1, 2, 4, 8, 8, 8),
    "8": (14, 17, 17, 14, 17, 17, 14),
    "9": (14, 17, 17, 15, 1, 1, 14),
    "A": (14, 17, 17, 31, 17, 17, 17),
    "G": (14, 17, 16, 23, 17, 17, 15),
    "E": (31, 16, 16, 30, 16, 16, 31),
    "_": (0, 0, 0, 0, 0, 0, 31),
    "I": (14, 4, 4, 4, 4, 4, 14),
    "N": (17, 25, 25, 21, 19, 19, 17),
    "V": (17, 17, 17, 17, 17, 10, 4),
    "L": (16, 16, 16, 16, 16, 16, 31),
    "D": (30, 17, 17, 17, 17, 17, 30),
    "m": (0, 0, 26, 21, 21, 21, 21),
    "s": (0, 0, 15, 16, 14, 1, 30),
}


def glyph35(character):
    """Packed [34:30] top row through [4:0] bottom row."""
    value = 0
    for row in FONT[character]:
        value = (value << 5) | row
    return value


def age_label(age):
    if not 0 <= age <= U64:
        raise ValueError("age input must be uint64")
    return f"AGE {age:04d} ms" if age <= 9999 else "AGE_INVALID"


def text_pixel(label, x, y):
    """11 fixed 12x16 cells, 2x glyph pixels; no opaque background."""
    if not (16 <= x <= 147 and 16 <= y <= 31):
        return False
    cell, cell_x = divmod(x - 16, 12)
    cell_y = y - 16
    return cell_x < 10 and cell_y < 14 and bool(
        FONT[label[cell]][cell_y // 2] & (1 << (4 - cell_x // 2))
    )


def descriptor(epoch, frame_id, capture_ms):
    if not (0 <= epoch <= U32 and 0 <= frame_id <= U32 and 0 <= capture_ms <= U64):
        raise ValueError("descriptor fields outside uint32/uint32/uint64")
    return (epoch << 96) | (frame_id << 64) | capture_ms


@dataclass
class Identity:
    """Two held buses. Counter input belongs to the external frozen timebase.

    time_edge publishes one current snapshot at idle on i_time_tick. No private
    millisecond counter. Every request takes two sync stages, detection edge,
    and one extra destination edge before stable capture. Returned ACK takes
    two sync stages; source cannot reuse the payload until a later source edge
    observes the completed ACK. No hot epoch switching is supported.
    """

    timeout: int = TIMEOUT
    time_req: int = 0
    time_ack: int = 0
    time_payload: int = 0
    time_ack_pipe: list = field(default_factory=lambda: [0, 0])
    time_req_pipe: list = field(default_factory=lambda: [0, 0])
    time_wait: bool = False
    event_req: int = 0
    event_ack: int = 0
    event_payload: int = 0
    event_ack_pipe: list = field(default_factory=lambda: [0, 0])
    event_req_pipe: list = field(default_factory=lambda: [0, 0])
    event_wait: bool = False
    desc_valid: bool = False
    desc_payload: int = 0
    mirror_valid: bool = False
    mirror_epoch: int = 0
    mirror_ms: int = 0
    mirror_age: int = 0
    armed: bool = False
    previous_sof: bool = False
    frame_id: int = 0
    wrap_fault: bool = False

    def reset(self):
        self.__dict__.update(Identity(timeout=self.timeout).__dict__)

    @property
    def event_busy(self):
        return self.event_req != self.event_ack_pipe[1]

    def camera_inputs(self, sof, credit):
        edge = bool(sof and not self.previous_sof and self.armed)
        admit = bool(edge and credit and self.mirror_valid and not self.event_busy
                     and not self.wrap_fault and self.frame_id != U32)
        return {
            "frame_edge": edge, "admit": admit, "skip": edge and not admit,
            "epoch": self.mirror_epoch, "frame_id": min(self.frame_id + 1, U32),
            "capture_ms": self.mirror_ms,
        }

    def camera_edge(self, sof=False, credit=False):
        before = self.camera_inputs(sof, credit)
        old_time_sync = self.time_req_pipe[1]
        self.time_req_pipe = [self.time_req, self.time_req_pipe[0]]
        self.event_ack_pipe = [self.event_ack, self.event_ack_pipe[0]]
        # SOF admission consumes only state present BEFORE this edge.
        if before["frame_edge"]:
            if self.frame_id == U32:
                self.wrap_fault = True
            else:
                self.frame_id += 1
            if before["admit"]:
                self.event_payload = descriptor(before["epoch"], before["frame_id"],
                                                before["capture_ms"])
                self.event_req ^= 1
        if not sof:
            self.armed = True
        self.previous_sof = bool(sof)
        completed = False
        if self.time_wait:
            self.mirror_epoch = self.time_payload >> 64
            self.mirror_ms = self.time_payload & U64
            self.mirror_valid = True
            self.mirror_age = 0
            self.time_ack = old_time_sync
            self.time_wait = False
            completed = True
        elif old_time_sync != self.time_ack:
            self.time_wait = True
        if not completed:
            if self.mirror_age == self.timeout:
                self.mirror_valid = False
            else:
                self.mirror_age += 1
        return before

    def time_edge(self, now_ms=0, epoch=0, tick=False, ready=False):
        if not (0 <= now_ms <= U64 and 0 <= epoch <= U32):
            raise ValueError("time input must be uint64/uint32")
        old_time_ack = self.time_ack_pipe[1]
        old_event_req = self.event_req_pipe[1]
        accepted = self.desc_payload if self.desc_valid and ready else None
        self.time_ack_pipe = [self.time_ack, self.time_ack_pipe[0]]
        self.event_req_pipe = [self.event_req, self.event_req_pipe[0]]
        if tick and self.time_req == old_time_ack:
            self.time_payload = (epoch << 64) | now_ms
            self.time_req ^= 1
        if accepted is not None:
            self.event_ack = old_event_req
            self.desc_valid = False
        elif self.event_wait:
            self.desc_payload = self.event_payload
            self.desc_valid = True
            self.event_wait = False
        elif not self.desc_valid and old_event_req != self.event_ack:
            self.event_wait = True
        return accepted


@dataclass
class Overlay:
    """Only first blank edge strictly AFTER SOF latches text; draw is live."""

    label: str = "AGE_INVALID"
    pending: bool = False
    x: int = 0
    y: int = 0
    previous_de: bool = False

    def edge(self, sof=False, de=False, age=U64, draw=False, reset=False):
        if reset:
            self.label, self.pending = "AGE_INVALID", False
            self.x, self.y, self.previous_de = 0, 0, False
        elif sof:
            assert not de, "SOF must be in blanking"
            self.pending = True
        elif self.pending and not de:
            self.label, self.pending = age_label(age), False
        elif de:
            assert not self.pending, "first active pixel must follow age latch edge"
        return {"label": self.label, "draw_permit": bool(draw and not reset)}

    def raster_edge(self, sof=False, vsync=False, hsync=False, de=False,
                    rgb=0, age=U64, draw=False, reset=False):
        """Postedge outputs of one output register, SOF-relative raster cursor.

        Same conventions as the existing overlay: evaluate current pixel using
        the preedge cursor; increment x on DE and y on first following blank.
        New interface uses explicit SOF to reset cursor, not VS polarity.
        """
        if not 0 <= rgb <= 0xffffff:
            raise ValueError("rgb must be uint24")
        hit = bool(de and text_pixel(self.label, self.x, self.y))
        result = self.edge(sof=sof, de=de, age=age, draw=draw, reset=reset)
        if reset:
            return {**result, "vsync": False, "hsync": False, "de": False, "rgb": 0}
        if sof:
            self.x, self.y = 0, 0
        elif de:
            self.x = (self.x + 1) & 0x7ff
        elif self.previous_de:
            self.x = 0
            self.y = (self.y + 1) & 0x3ff
        self.previous_de = bool(de)
        return {**result, "vsync": bool(vsync), "hsync": bool(hsync),
                "de": bool(de), "rgb": 0xffffff if hit else rgb}


def selfcheck():
    checks = []
    m = Identity()
    assert not m.camera_edge(sof=True, credit=True)["frame_edge"]
    assert not m.camera_edge(sof=True, credit=True)["frame_edge"]
    m.camera_edge(sof=False)
    assert m.camera_edge(sof=True, credit=True)["skip"] and m.frame_id == 1
    checks.append("reset_high_no_phantom_and_unknown_mirror_skips")
    m.camera_edge(sof=False)
    m.time_edge(now_ms=100, epoch=7, tick=True)
    for _ in range(3):
        m.camera_edge()
        assert not m.mirror_valid
    # Completed mirror on this same edge MUST NOT admit first eligible frame.
    assert m.camera_edge(sof=True, credit=True)["skip"]
    assert (m.mirror_valid, m.mirror_epoch, m.mirror_ms) == (True, 7, 100)
    m.camera_edge()
    admitted = m.camera_edge(sof=True, credit=True)
    assert admitted["admit"] and admitted["frame_id"] == 3
    assert m.event_payload == descriptor(7, 3, 100)
    checks.append("same_edge_first_mirror_ineligible_next_sof_admits")
    frozen = m.event_payload
    for _ in range(3):
        assert m.time_edge(ready=True) is None
        assert not m.desc_valid
    assert m.time_edge(ready=True) is None and m.desc_valid
    assert m.desc_payload == frozen
    for _ in range(10):
        assert m.time_edge(ready=False) is None and m.desc_valid
        m.camera_edge()
        assert m.event_payload == frozen and m.event_busy
    assert m.camera_edge(sof=True, credit=True)["skip"] and m.frame_id == 4
    assert m.time_edge(ready=True) == frozen and not m.desc_valid
    assert m.event_busy
    m.camera_edge()
    assert m.event_busy
    m.camera_edge()
    assert not m.event_busy
    checks.append("held128_no_half_descriptor_stall_ack_only_on_accept")
    # Updated source snapshot reaches camera exactly on a SOF; use old mirror.
    m.time_edge(now_ms=200, epoch=7, tick=True)
    for _ in range(3):
        m.camera_edge()
    admitted = m.camera_edge(sof=True, credit=True)
    assert admitted["admit"] and admitted["capture_ms"] == 100
    assert m.mirror_ms == 200 and (m.event_payload & U64) == 100
    checks.append("same_edge_update_uses_completed_old_mirror")
    count = m.frame_id
    assert not m.camera_edge(sof=True, credit=True)["frame_edge"]
    assert m.frame_id == count
    m.camera_edge()
    assert m.camera_edge(sof=True, credit=False)["skip"] and m.frame_id == count + 1
    checks.append("continued_high_not_counted_creditless_sof_counted")
    m.reset()
    assert not m.desc_valid and not m.event_busy and not m.mirror_valid
    assert not m.camera_edge(sof=True, credit=True)["frame_edge"]
    m.time_edge(ready=True)
    assert not m.desc_valid
    checks.append("common_reset_cancels_inflight")
    m = Identity()
    m.time_edge(now_ms=123, epoch=8, tick=True)
    held_time = m.time_payload
    for index in range(20):
        m.time_edge(now_ms=124 + index, epoch=8, tick=True)
        assert m.time_payload == held_time
    for _ in range(4):
        m.camera_edge()
    assert m.mirror_valid and m.mirror_age == 0
    for _ in range(TIMEOUT):
        m.camera_edge()
    assert m.mirror_valid and m.mirror_age == TIMEOUT
    m.camera_edge()
    assert not m.mirror_valid
    assert m.camera_edge(sof=True, credit=True)["skip"]
    checks.append("held96_timeout_at_120001_no_timeclock_progress")
    m.reset()
    m.armed, m.mirror_valid, m.mirror_epoch, m.frame_id = True, True, 9, U32 - 1
    assert m.camera_edge(sof=True, credit=True)["admit"] and m.frame_id == U32
    m.camera_edge()
    assert m.camera_edge(sof=True, credit=True)["skip"]
    assert m.frame_id == U32 and m.wrap_fault
    m.camera_edge()
    assert m.camera_edge(sof=True, credit=True)["skip"] and m.frame_id == U32
    checks.append("uint32_last_id_once_then_sticky_saturated_wrap_fault")
    m.reset()
    m.time_edge(now_ms=0, epoch=10, tick=True)
    for _ in range(4):
        m.camera_edge()
    assert m.camera_edge(sof=True, credit=True)["admit"]
    assert m.event_payload == descriptor(10, 1, 0)
    checks.append("coordinated_reset_new_epoch_restarts_identity")
    # Source mirror lag can only add age: downstream delta+4 remains conservative.
    for true_capture in (0, 1, 500, U64 - 4):
        for lag in (0, 1, min(2, true_capture)):
            mirror_capture = max(0, true_capture - lag)
            for display_age in (0, 1, 4, 100):
                true_now = min(U64, true_capture + display_age)
                for destination_lag in (0, 1, 4):
                    snapshot_now = max(mirror_capture, true_now - destination_lag)
                    upper = min(U64, snapshot_now - mirror_capture + 4)
                    assert upper >= true_now - true_capture
                    assert mirror_capture <= true_capture
    checks.append("old_source_mirror_lag_increases_conservative_age")
    for age in (0, 1, 9, 10, 99, 100, 999, 1000, 1999, 2000, 2001, 9998, 9999,
                10000, U64 - 1, U64):
        label = age_label(age)
        assert len(label) == 11
        assert label == (f"AGE {age:04d} ms" if age < 10000 else "AGE_INVALID")
        for y in range(15, 33):
            for x in range(15, 149):
                if x in (15, 148) or y in (15, 32):
                    assert not text_pixel(label, x, y)
    o = Overlay()
    assert o.edge(sof=True, age=11)["label"] == "AGE_INVALID"
    assert o.edge(age=2000)["label"] == "AGE 2000 ms"
    assert o.edge(de=True, age=3, draw=True) == {
        "label": "AGE 2000 ms", "draw_permit": True}
    assert o.edge(de=True, age=U64, draw=False) == {
        "label": "AGE 2000 ms", "draw_permit": False}
    assert o.edge(sof=True, age=2001)["label"] == "AGE 2000 ms"
    assert o.edge(age=2001)["label"] == "AGE 2001 ms"
    assert o.edge(reset=True, draw=True)["draw_permit"] is False
    checks.append("eleven_cells_boundaries_frame_stable_text_live_draw")
    o = Overlay()
    o.raster_edge(sof=True, age=1)
    o.raster_edge(age=2000)
    for y in range(33):
        for x in range(150):
            output = o.raster_edge(de=True, rgb=0x123456, age=U64,
                                   vsync=bool(x & 1), hsync=bool(y & 1))
            expected_rgb = 0xffffff if text_pixel("AGE 2000 ms", x, y) else 0x123456
            assert output["rgb"] == expected_rgb
            assert output["de"] and output["vsync"] == bool(x & 1)
            assert output["hsync"] == bool(y & 1)
        o.raster_edge(rgb=0x123456)
        assert o.x == 0 and o.y == y + 1
    checks.append("registered_rgb_sync_passthrough_full_raster_fixed_cursor")
    # Full 5x7 glyph extraction compared to independent indexed packed bitmap.
    for char, rows in FONT.items():
        packed = glyph35(char)
        for y in range(7):
            for x in range(5):
                assert bool(rows[y] & (1 << (4 - x))) == bool(
                    packed & (1 << (34 - y * 5 - x)))
    checks.append("all_glyph_full35bit_pixel_vectors")
    return checks


def identity_vectors():
    """Compact deterministic edge sequences, repeat only identical idle edges."""
    m = Identity()
    vectors = []

    def edge(domain, repeat=1, **inputs):
        before = None
        for _ in range(repeat):
            before = (m.camera_edge(**inputs) if domain == "camera"
                      else m.time_edge(**inputs))
        state = {name: getattr(m, name) for name in (
            "mirror_valid", "mirror_epoch", "mirror_ms", "mirror_age", "frame_id",
            "wrap_fault", "time_req", "time_ack", "time_payload", "event_req",
            "event_ack", "event_payload", "event_busy", "desc_valid", "desc_payload")}
        vectors.append({"domain": domain, "repeat": repeat, "inputs": inputs,
                        "last_edge_result": before, "state_after": state})

    edge("camera", sof=True, credit=True)
    edge("camera", sof=False)
    edge("camera", sof=True, credit=True)
    edge("camera")
    edge("time", now_ms=100, epoch=7, tick=True)
    edge("camera", repeat=3)
    edge("camera", sof=True, credit=True)
    edge("camera")
    edge("camera", sof=True, credit=False)
    edge("camera")
    edge("camera", sof=True, credit=True)
    edge("time", repeat=4, ready=False)
    edge("time", repeat=6, ready=False, now_ms=101)
    edge("camera")
    edge("camera", sof=True, credit=True)
    edge("time", ready=True)
    edge("camera", repeat=2)
    edge("time", now_ms=102, epoch=7, tick=True)
    edge("camera", repeat=3)
    edge("camera", sof=True, credit=True)
    edge("camera", repeat=TIMEOUT)
    edge("camera")
    edge("camera", sof=True, credit=True)
    m.reset()
    vectors.append({"domain": "common_reset", "state_after": {
        "frame_id": m.frame_id, "mirror_valid": m.mirror_valid,
        "desc_valid": m.desc_valid, "event_busy": m.event_busy}})
    edge("camera", sof=True, credit=True)
    edge("camera")
    edge("time", now_ms=1, epoch=8, tick=True)
    edge("camera", repeat=4)
    # Verification-only state injection reaches wrap boundary without 2**32 edges.
    m.frame_id = U32 - 1
    vectors.append({"domain": "inject_frame_id", "value": U32 - 1})
    edge("camera", sof=True, credit=True)
    edge("camera")
    edge("camera", sof=True, credit=True)
    edge("camera")
    edge("camera", sof=True, credit=True)
    return vectors


def emit_vectors(directory):
    checks = selfcheck()
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    ages = (0, 1, 9, 10, 99, 100, 999, 1000, 1999, 2000, 2001, 9998, 9999,
            10000, U64 - 1, U64)
    glyphs = []
    for char, rows in FONT.items():
        # All192 cell pixels are included; top/left orientation is explicit.
        pixel_rows = ["".join("1" if x < 10 and y < 14 and
                                  rows[y // 2] & (1 << (4 - x // 2)) else "0"
                                  for x in range(12)) for y in range(16)]
        glyphs.append({"character": char, "ascii": ord(char), "rows5": rows,
                       "packed35_hex": f"{glyph35(char):09x}",
                       "cell12x16_pixel_rows": pixel_rows})
    labels = []
    for age in ages:
        label = age_label(age)
        labels.append({"age": age, "age64_hex": f"{age:016x}", "label": label,
                       "pixel_rows132": ["".join("1" if text_pixel(label, x, y)
                                                else "0" for x in range(16, 148))
                                          for y in range(16, 32)]})
    o = Overlay()
    frame_inputs = [
        {"sof": True, "age": 5, "draw": False},
        {"age": 2000, "draw": False},
        {"de": True, "age": 2001, "draw": False},
        {"de": True, "age": U64, "draw": True},
        {"de": True, "age": 1, "draw": False},
        {"sof": True, "age": 2001, "draw": False},
        {"age": 10000, "draw": False},
        {"de": True, "age": 0, "draw": True},
        {"reset": True, "draw": True},
    ]
    payload = {"schema": 1, "selfcheck_passes": checks,
               "glyphs": glyphs, "age_boundaries": labels,
               "overlay_frame_edges": [{"inputs": inputs, "after": o.edge(**inputs)}
                                       for inputs in frame_inputs],
               "identity_edges": identity_vectors()}
    path = directory / "vectors.json"
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    # Each label produces2112 row-major bits as one-bit hexadecimal memory words.
    (directory / "age_pixels.mem").write_text("".join(
        bit + "\n" for item in labels for row in item["pixel_rows132"] for bit in row),
        encoding="ascii")
    (directory / "glyph35.mem").write_text("".join(
        item["packed35_hex"] + "\n" for item in glyphs), encoding="ascii")
    (directory / "age_values.mem").write_text("".join(
        item["age64_hex"] + "\n" for item in labels), encoding="ascii")
    files = [Path(__file__), directory / "contract.json", path,
             directory / "age_pixels.mem", directory / "glyph35.mem",
             directory / "age_values.mem"]
    (directory / "manifest.sha256").write_text("".join(
        hashlib.sha256(item.read_bytes()).hexdigest() + "  " + item.name + "\n"
        for item in files), encoding="ascii")
    print(f"VECTORS_PASS glyphs={len(glyphs)} age_boundaries={len(labels)} "
          f"full_label_pixels={len(labels) * 132 * 16} identity_steps={len(payload['identity_edges'])}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", type=Path, help="regenerate deterministic reference assets")
    args = parser.parse_args()
    for check in selfcheck():
        print("PASS", check)
    print("SOURCE_SOF_REFERENCE_PASS")
    if args.emit:
        emit_vectors(args.emit)
