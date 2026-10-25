"""Three-table event reference; timestamps are coherent oracle inputs, NOT CDC."""
import random


class Tables:
    def __init__(self):
        self.source = None
        self.pending = None
        self.active = None
        self.copied = []
        self.acks = 0

    def publish(self, metadata, entries):
        assert self.source is None, 'source must hold until final-copy ack'
        assert 0 <= len(entries) <= 64
        assert all(0 <= entry < (1 << 97) for entry in entries)
        self.source = (dict(metadata), tuple(entries))

    def destination_tick(self, copy_ready, sof):
        prior_pending = self.pending
        if sof and prior_pending is not None:
            self.active = prior_pending
            self.pending = None
        if prior_pending is None and self.source is not None and copy_ready:
            metadata, entries = self.source
            if len(self.copied) < len(entries):
                self.copied.append(entries[len(self.copied)])
            if len(self.copied) == len(entries):
                self.pending = (dict(metadata), tuple(self.copied))
                self.copied = []
                self.source = None
                self.acks += 1

    def visible(self, coherent_now_ms):
        if self.active is None:
            return ()
        metadata, entries = self.active
        age = coherent_now_ms - metadata['source_timestamp_ms']
        return entries if 0 <= age <= 500 else ()


def main():
    rng = random.Random(20261015)
    for count in (0, 1, 32, 33, 64):
        tables = Tables()
        entries = tuple(rng.getrandbits(97) for _ in range(count))
        metadata = {'source_frame_id': count + 1, 'source_timestamp_ms': 1000}
        tables.publish(metadata, entries)
        for _ in range(max(count - 1, 0)):
            tables.destination_tick(True, False)
            assert tables.source is not None and tables.pending is None
        frozen = tables.source
        for _ in range(137):
            tables.destination_tick(False, False)
            assert tables.source == frozen and tables.active is None
        tables.destination_tick(True, True)
        assert tables.acks == 1 and tables.pending[1] == entries and tables.active is None
        tables.destination_tick(False, True)
        assert tables.active[1] == entries and tables.pending is None
        assert tables.visible(1500) == entries
        assert tables.visible(1501) == ()
        assert tables.visible(999) == ()
        tables.publish({'source_frame_id': 100, 'source_timestamp_ms': 1100}, ())
        tables.destination_tick(True, False)
        assert tables.active[1] == entries
        tables.publish({'source_frame_id': 101, 'source_timestamp_ms': 1200}, (7,))
        held = tables.source
        for _ in range(91):
            tables.destination_tick(True, False)
            assert tables.source == held and tables.pending[1] == ()
        tables.destination_tick(True, True)
        assert tables.active[1] == () and tables.source == held
        tables.destination_tick(True, False)
        assert tables.pending[1] == (7,)
        tables.__init__()
        for _ in range(10):
            tables.destination_tick(True, True)
        assert tables.source is None and tables.pending is None and tables.active is None
    print('TABLE_EVENT_REFERENCE_PASS counts=0,1,32,33,64; actual CDC/time provider NOT_RUN')


if __name__ == '__main__':
    main()
