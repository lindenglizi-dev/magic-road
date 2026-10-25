"""Stdlib readback check of the physical prediction lines and field sequence."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def words(name):
    return [int(line,16) for line in (ROOT/name).read_text(encoding="ascii").splitlines()]


def main():
    manifest=read(ROOT/"artifact_manifest.json")
    assert all(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==value for name,value in manifest.items())
    binding=read(ROOT/"input_binding.json")
    assert all(hashlib.sha256(Path(name).read_bytes()).hexdigest()==value for name,value in binding["source_sha256"].items())
    ranges=read(ROOT/"prediction_backing_ranges.json")["planes"]
    assert len(ranges)==6
    lines={word>>128:word&((1<<128)-1) for word in words("prediction_lines160.hex")}
    assert len(lines)==sum(row["allocated_bytes"]//16 for row in ranges)
    for address in lines:
        assert address%16==0 and sum(row["base"]<=address and address+16<=row["end"] for row in ranges)==1
    fields=words("cell_field_addresses32.hex")
    cells=words("head_cells112.hex")
    assert len(fields)==len(cells)*7==84672
    for cell_index,cell in enumerate(cells):
        rebuilt=0
        for lane,address in enumerate(fields[cell_index*7:cell_index*7+7]):
            assert address%2==0 and address&15<=14
            data=(lines[address&~15]>>((address&15)*8))&65535
            rebuilt|=data<<(lane*16)
        assert rebuilt==cell
    # All remaining padding bytes in every allocation are explicitly zero.
    valid=set()
    for address in fields:
        valid.update((address,address+1))
    padding=0
    for address,line in lines.items():
        for lane in range(16):
            if address+lane not in valid:
                assert (line>>(lane*8))&255==0
                padding+=1
    print(json.dumps({"status":"PASS","planes":6,"lines":len(lines),"field_addresses":len(fields),
                      "cells112":len(cells),"zero_padding_bytes":padding,"artifacts":len(manifest),"input_hashes":len(binding["source_sha256"])}))


if __name__=="__main__":
    main()
