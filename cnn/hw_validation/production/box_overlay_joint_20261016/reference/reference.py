"""FINAL97 display reference: direct outlines versus one 1280x18 event map.

No coordinate rounding occurs here. The frozen NMS has already performed RNE;
its source integer coordinates are stored in each 20-bit field as integer<<8.
RGB goldens contain all active pixels, row-major, R then G then B, no blanking.
"""

import argparse
import hashlib
import json
from pathlib import Path
import random
import runpy
import zlib

WIDTH, HEIGHT, MAX_BOXES = 1280, 720, 64
PERSON, VEHICLE, WHITE = 0x00ff00, 0x00ffff, 0xffffff
U64 = (1 << 64) - 1
PRODUCTION = Path(__file__).resolve().parents[2]
AGE_SOURCE = PRODUCTION / "source_sof_identity_20261015/reference/reference.py"
_age = runpy.run_path(str(AGE_SOURCE))
age_label, text_pixel = _age["age_label"], _age["text_pixel"]
REAL_SOURCE = PRODUCTION / "postprocess_golden_2fps_20261015/artifacts/real_image/result_table_97.hex"
REAL_SHA256 = "c5cd21644f6e3bd16fb19726839b20f18c4affa59e33e88062f895e883d3c96c"
REAL_HEADS = REAL_SOURCE.with_name("heads_cell_order_112.hex")
REAL_HEADS_SHA256 = "2fe18d831eba985796ad8735b1774b97c55c580f71f9c4e9a29a7e602f3a154f"
REAL_FINAL = REAL_SOURCE.with_name("final.json")
REAL_FINAL_SHA256 = "4e139e132e7e181dc5be0d6256fd9aeed53a9995a617b10fa5b4054b6c2e7141"


def pack_fields(label, score, x0, y0, x1, y1):
    """Pack exact 20-bit coordinate fields, including malformed fractions."""
    if label not in (0, 1) or not 0 <= score <= 65535:
        raise ValueError("class/score outside FINAL97 contract")
    fields = (x0, y0, x1, y1)
    if any(not 0 <= value < (1 << 20) for value in fields):
        raise ValueError("coordinate outside uint20")
    return label | (score << 1) | sum(value << shift for value, shift in
                                                   zip(fields, (17, 37, 57, 77)))


def pack_box(label, x0, y0, x1, y1, score=40000):
    return pack_fields(label, score, *(value << 8 for value in (x0, y0, x1, y1)))


def geometry(entry):
    """Return class and clipped half-open geometry; skip only malformed/collapse."""
    if not 0 <= entry < (1 << 97):
        raise ValueError("entry outside uint97")
    fields = [(entry >> shift) & 0xfffff for shift in (17, 37, 57, 77)]
    if any(value & 255 for value in fields):
        return None
    x0, y0, x1, y1 = (value >> 8 for value in fields)
    x0, x1 = min(x0, WIDTH), min(x1, WIDTH)
    y0, y1 = min(y0, HEIGHT), min(y1, HEIGHT)
    return (entry & 1, x0, y0, x1, y1) if x0 < x1 and y0 < y1 else None


def checked_entries(entries):
    entries = tuple(entries)
    if len(entries) > MAX_BOXES:
        raise ValueError("at most 64 table entries")
    for entry in entries:
        geometry(entry)
    return entries


def direct_mask(entries):
    """Independent outline rasterization; bit0 person, bit1 vehicle."""
    result = bytearray(WIDTH * HEIGHT)
    for entry in checked_entries(entries):
        box = geometry(entry)
        if box is None:
            continue
        label, x0, y0, x1, y1 = box
        bit = 1 << label
        for y in (y0, y1 - 1):
            for x in range(x0, x1):
                result[y * WIDTH + x] |= bit
        for y in range(y0, y1):
            result[y * WIDTH + x0] |= bit
            result[y * WIDTH + x1 - 1] |= bit
    return result


def endpoint_updates(entry, y):
    """Two optional endpoint operations; fixed five-stage schedule still applies."""
    box = geometry(entry)
    if box is None:
        return (None, None)
    label, x0, y0, x1, y1 = box
    if not y0 <= y < y1:
        return (None, None)
    if y in (y0, y1 - 1):
        return ((x0, label, 1, False),
                (x1, label, -1, False) if x1 < WIDTH else None)
    return ((x0, label, 0, True),
            (x1 - 1, label, 0, True) if x1 - 1 != x0 else None)


def signed8(value):
    return value - 256 if value & 128 else value


def line_events(entries, y):
    """1280 packed18 words: {vehicle_point,person_point,vehicle_d8,person_d8}."""
    entries = checked_entries(entries)
    if not 0 <= y < HEIGHT:
        raise ValueError("row outside active frame")
    words = [0] * WIDTH
    for entry in entries:
        # FETCH,READ0,WRITE0,READ1,WRITE1: read stages never write. WRITE
        # stages drive dummy async read address (write_address XOR 1).
        for update in endpoint_updates(entry, y):
            if update is None:
                continue
            x, label, delta, point = update
            assert (x ^ 1) != x and 0 <= (x ^ 1) < WIDTH
            if point:
                words[x] |= 1 << (16 + label)
            else:
                shift = 8 * label
                value = signed8((words[x] >> shift) & 255) + delta
                assert -64 <= value <= 64
                words[x] = (words[x] & ~(255 << shift)) | ((value & 255) << shift)
    return words


def consume_line(words):
    """Read current event before clearing previous x, including DEfall final x."""
    if len(words) != WIDTH:
        raise ValueError("line map must have 1280 words")
    words = list(words)
    result = bytearray(WIDTH)
    person = vehicle = 0
    for x in range(WIDTH):
        word = words[x]
        person += signed8(word & 255)
        vehicle += signed8((word >> 8) & 255)
        assert 0 <= person <= 64 and 0 <= vehicle <= 64
        result[x] = int(bool(person or word & (1 << 16))) | (
            int(bool(vehicle or word & (1 << 17))) << 1)
        if x:
            assert x - 1 != x
            words[x - 1] = 0
    words[-1] = 0  # First blank edge (DEfall) clears the remaining consumed word.
    assert not any(words)
    return result


def event_mask(entries):
    entries = checked_entries(entries)
    return b"".join(consume_line(line_events(entries, y)) for y in range(HEIGHT))


def pixel_rgb(mask, x, y, label, draw=True, raw_rgb=0x123456):
    """AGE always has priority; draw permission is sampled live at this pixel."""
    if text_pixel(label, x, y):
        return WHITE
    if draw and mask:
        return PERSON if mask & 1 else VEHICLE
    return raw_rgb


def final_live_rgb(age_rgb, raw_delayed, live_draw):
    """Final mux after two video registers removes any already queued box color."""
    return age_rgb if live_draw or age_rgb == WHITE else raw_delayed


def render_frame(entries, age=U64, draw=True, raw_rgb=0x123456, model="events"):
    """All720x1280 active RGB bytes. draw/raw_rgb may be (x,y) callables.

    age is the frame-latched age, regardless of later live age changes. This
    pixel function is the oracle; the RTL test separately checks two registers.
    """
    if model not in ("events", "direct"):
        raise ValueError("model must be events or direct")
    mask = event_mask(entries) if model == "events" else direct_mask(entries)
    label = age_label(age)
    result = bytearray(WIDTH * HEIGHT * 3)
    for y in range(HEIGHT):
        for x in range(WIDTH):
            permission = draw(x, y) if callable(draw) else draw
            raw = raw_rgb(x, y) if callable(raw_rgb) else raw_rgb
            if not 0 <= raw <= 0xffffff:
                raise ValueError("raw RGB outside uint24")
            rgb = pixel_rgb(mask[y * WIDTH + x], x, y, label, permission, raw)
            offset = (y * WIDTH + x) * 3
            result[offset:offset + 3] = rgb.to_bytes(3, "big")
    return bytes(result)


def real_entries():
    data = REAL_SOURCE.read_bytes()
    assert hashlib.sha256(data).hexdigest() == REAL_SHA256
    entries = [int(line, 16) for line in data.decode("ascii").splitlines() if line]
    assert len(entries) == 7
    assert hashlib.sha256(REAL_HEADS.read_bytes()).hexdigest() == REAL_HEADS_SHA256
    final_data = REAL_FINAL.read_bytes()
    assert hashlib.sha256(final_data).hexdigest() == REAL_FINAL_SHA256
    detections = json.loads(final_data)["detections"]
    assert len(detections) == 7
    for entry, detection in zip(entries, detections):
        assert geometry(entry) == (detection["label"], *detection["box_source"])
        assert ((entry >> 1) & 65535) == detection["score_uint16"]
    return entries


def cases():
    """Deterministic renderer injections, plus the provenance-bound real7 table."""
    result = []
    for count in (0, 1, 32, 33, 64):
        result.append({"name": f"count_{count}", "entries": [
            pack_box(i & 1, 2 + i * 17, 4 + i * 7, 12 + i * 17, 14 + i * 7)
            for i in range(count)], "age": 123, "draw": True})
    for label in (0, 1):
        result.append({"name": f"overlap64_class{label}", "entries": [
            pack_box(label, 0, 0, WIDTH, HEIGHT)] * 64, "age": 2000, "draw": True})
    result.append({"name": "overlap64_signed_negative64", "entries": [
        pack_box(1, 0, 0, WIDTH - 1, HEIGHT - 1)] * 64, "age": 10, "draw": True})
    result.append({"name": "crossing_types", "entries": [
        pack_box(0, 10, 16, 150, 32), pack_box(1, 16, 10, 148, 40),
        pack_box(0, 640, 0, 641, HEIGHT), pack_box(1, 0, 360, WIDTH, 361)],
        "age": 1999, "draw": True})
    result.append({"name": "borders_degenerate_clip", "entries": [
        pack_box(0, 0, 0, WIDTH, HEIGHT), pack_box(1, 0, 0, 1, HEIGHT),
        pack_box(1, WIDTH - 1, 0, WIDTH, HEIGHT), pack_box(1, 0, 0, WIDTH, 1),
        pack_box(1, 0, HEIGHT - 1, WIDTH, HEIGHT), pack_box(0, 1, 1, 2, 2),
        pack_box(1, 1278, 718, 4095, 4095)], "age": 0, "draw": True})
    result.append({"name": "collapse_fractional_skip_only", "entries": [
        pack_box(0, 9, 9, 9, 20), pack_box(1, 5, 20, 12, 20),
        pack_box(0, 2000, 2000, 4095, 4095), pack_box(1, 100, 100, 50, 50),
        pack_fields(0, 65535, (10 << 8) + 1, 10 << 8, 20 << 8, 20 << 8),
        pack_box(1, 30, 30, 50, 50)], "age": 9999, "draw": True})
    result.append({"name": "same_endpoint_signed_cancellation", "entries": [
        pack_box(i & 1, 0 if i < 32 else 640, 200, 640 if i < 32 else 1280, 300)
        for i in range(64)], "age": 1, "draw": True})
    rng = random.Random(20261016)
    random_boxes = [pack_box(rng.randrange(2), rng.randrange(1400), rng.randrange(800),
                             rng.randrange(1400), rng.randrange(800)) for _ in range(64)]
    result.append({"name": "random_seed_20261016", "entries": random_boxes,
                   "age": 10000, "draw": True})
    result.append({"name": "expired_finite_age", "entries": real_entries(),
                   "age": 2001, "draw": False})
    result.append({"name": "unknown_age", "entries": real_entries(),
                   "age": U64, "draw": False})
    result.append({"name": "live_withdraw", "entries": [pack_box(0, 0, 0, WIDTH, HEIGHT)],
                   "age": 2000, "draw": True, "withdraw_pixel": 20 * WIDTH + 64})
    result.append({"name": "real7_final97", "entries": real_entries(),
                   "age": 2000, "draw": True, "source": str(REAL_SOURCE),
                   "source_sha256": REAL_SHA256, "heads_source": str(REAL_HEADS),
                   "heads_source_sha256": REAL_HEADS_SHA256,
                   "final_source": str(REAL_FINAL), "final_source_sha256": REAL_FINAL_SHA256})
    return result


def draw_function(case):
    limit = case.get("withdraw_pixel")
    return (lambda x, y: case["draw"] and y * WIDTH + x < limit) if limit is not None else case["draw"]


def selfcheck():
    checks = []
    for case in cases():
        original = tuple(case["entries"])
        direct = direct_mask(original)
        events = event_mask(original)
        assert direct == events, case["name"]
        assert original == tuple(case["entries"]), "display must not alter table"
        assert 5 * len(original) + 10 <= 330 < 370
        checks.append(case["name"])
    assert geometry(pack_box(0, 89, 408, 122, 463)) == (0, 89, 408, 122, 463)
    for shift in (17, 37, 57, 77):
        assert geometry(pack_box(0, 1, 1, 2, 2) | (1 << shift)) is None
    words = line_events([pack_box(0, 0, 0, WIDTH, HEIGHT)] * 64, 0)
    assert signed8(words[0] & 255) == 64 and words[-1] == 0
    words = line_events([pack_box(1, 0, 0, 100, 10)] * 64, 0)
    assert signed8((words[100] >> 8) & 255) == -64
    one = line_events([pack_box(0, 0, 0, 1, 3)], 1)
    assert one[0] == (1 << 16) and sum(bool(word) for word in one) == 1
    assert pixel_rgb(3, 0, 0, "AGE 0000 ms") == PERSON
    assert pixel_rgb(3, 0, 0, "AGE 0000 ms", False) == 0x123456
    for y in range(16, 32):
        for x in range(16, 148):
            if text_pixel("AGE 2000 ms", x, y):
                assert pixel_rgb(3, x, y, "AGE 2000 ms", False) == WHITE
    # Independent tagged ideal versus the wrapper's RGB-only live-withdraw mux.
    for raw in (0, 0x123456, WHITE, PERSON, VEHICLE):
        for text_hit in (False, True):
            for queued_box in (None, PERSON, VEHICLE):
                age_rgb = WHITE if text_hit else (raw if queued_box is None else queued_box)
                for live in (False, True):
                    ideal = WHITE if text_hit else (queued_box if live and queued_box is not None else raw)
                    assert final_live_rgb(age_rgb, raw, live) == ideal
    overlay = _age["Overlay"]()
    overlay.edge(sof=True, age=1)
    assert overlay.edge(age=2000)["label"] == "AGE 2000 ms"
    assert overlay.edge(de=True, age=U64, draw=False) == {
        "label": "AGE 2000 ms", "draw_permit": False}
    return checks


def emit(directory):
    """Generated files only; compressed fullframe goldens prevent huge text dumps."""
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    items = []
    for case in cases():
        name = case["name"]
        entries_path = directory / (name + ".boxes.hex")
        entries_path.write_text("".join(f"{entry:025x}\n" for entry in case["entries"]), encoding="ascii")
        rgb = render_frame(case["entries"], case["age"], draw_function(case), model="direct")
        rgb_events = render_frame(case["entries"], case["age"], draw_function(case), model="events")
        assert rgb == rgb_events, name
        rgb_path = directory / (name + ".rgb24.zlib")
        rgb_path.write_bytes(zlib.compress(rgb, 9))
        item = {key: value for key, value in case.items() if key != "entries"}
        item.update(box_count=len(case["entries"]), boxes_file=entries_path.name,
                    rgb_file=rgb_path.name, rgb_bytes=len(rgb), rgb_sha256=hashlib.sha256(rgb).hexdigest(),
                    compressed_sha256=hashlib.sha256(rgb_path.read_bytes()).hexdigest(),
                    boxes_sha256=hashlib.sha256(entries_path.read_bytes()).hexdigest(),
                    prepare_cycles_conservative=5 * len(case["entries"]) + 10,
                    provenance="frozen_real_NMS" if name == "real7_final97" else "renderer_test_injection")
        items.append(item)
    manifest = {"schema": 1, "width": WIDTH, "height": HEIGHT,
                "rgb_order": "active-only y-major then x-major RGB big-endian bytes; zlib stream",
                "event_word": "bit17 vehicle_point,bit16 person_point,bits15:8 signed8 vehicle_delta,bits7:0 signed8 person_delta",
                "age_dependency": str(AGE_SOURCE), "age_dependency_sha256": hashlib.sha256(AGE_SOURCE.read_bytes()).hexdigest(),
                "reference_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), "cases": items}
    (directory / "vector_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"GOLDENS_PASS cases={len(items)} full_active_pixels={len(items) * WIDTH * HEIGHT}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", type=Path)
    args = parser.parse_args()
    checks = selfcheck()
    print(f"BOX_REFERENCE_PASS cases={len(checks)} full_active_pixels={len(checks) * WIDTH * HEIGHT}")
    if args.emit:
        emit(args.emit)
