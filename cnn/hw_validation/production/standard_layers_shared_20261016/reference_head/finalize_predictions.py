"""Add six committed-plane CPU images and strict graph field-address goldens."""
from datetime import datetime,timezone
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys
import traceback
from typing import Any

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("fixed_head_reference",HERE/"generate_head.py")
head=importlib.util.module_from_spec(spec)
spec.loader.exec_module(head)
base=head.base


def words(path):
    return [int(line,16) for line in path.read_text(encoding="ascii").splitlines()]


def main():
    receipt=base.read(HERE/"verification_receipt.json")
    assert receipt["status"]=="PASS" and receipt["layers"]==21
    previous_manifest=base.read(HERE/"artifact_manifest.json")
    assert all(base.sha(HERE/name)==value for name,value in previous_manifest.items())
    binding=base.read(HERE/"input_binding.json")
    original=base.read(HERE/"head_generation_binding.json") if binding.get("prediction_phase") else binding
    assert all(base.sha(Path(name))==value for name,value in original["source_sha256"].items())
    base.save(HERE/"head_generation_binding.json",original)
    graph_path=head.PRODUCTION/"graph_artifacts/graph.json"
    graph=base.read(graph_path)
    resolver=head.extended.functions(head.PRODUCTION/"graph.py",["resolve_byte_address"],{"math":math,"Any":Any})["resolve_byte_address"]
    nodes={node["name"]:node for node in graph["nodes"]}
    planes={}
    plane_inputs=[]
    ranges=[]
    for scale in (2,3,4):
        for branch in ("reg_out","cls_out"):
            name=f"head{scale}.{branch}"
            node=nodes[name]
            storage=node["storage"]
            data_path=HERE/name/"expected_hwc_post.hex"
            values=words(data_path)
            plane_inputs.append(data_path)
            h,w,c=node["output_shape_hwc"]
            assert len(values)==h*w*c and storage["bytes_per_element"]==2
            image=bytearray(storage["allocated_bytes"])
            for y in range(h):
                for x in range(w):
                    for channel in range(c):
                        addr=resolver(graph,name,y,x,channel)
                        tile=(y//4)*((w+3)//4)+x//4
                        local=(y%4)*4+x%4
                        assert addr==storage["base"]+(tile*16*c+local*c+channel)*2
                        value=values[(y*w+x)*c+channel]
                        assert 0<=value<65536 and addr%2==0
                        offset=addr-storage["base"]
                        image[offset:offset+2]=value.to_bytes(2,"little")
            assert storage["base"]%16==0 and len(image)%16==0
            planes[name]={"node":node,"image":image,"values":values}
            ranges.append({"tensor":name,"shape_hwc":node["output_shape_hwc"],**storage})
    lines=[]
    for plane in sorted(planes.values(),key=lambda row:row["node"]["storage"]["base"]):
        begin=plane["node"]["storage"]["base"]
        for offset in range(0,len(plane["image"]),16):
            lines.append(((begin+offset)<<128)|int.from_bytes(plane["image"][offset:offset+16],"little"))
    base.emit(HERE/"prediction_lines160.hex",lines,160)
    addresses=[]
    rebuilt_cells=[]
    for scale in (2,3,4):
        h,w,_=nodes[f"head{scale}.reg_out"]["output_shape_hwc"]
        for y in range(h):
            for x in range(w):
                fields=[]
                for branch,channels in (("reg_out",5),("cls_out",2)):
                    name=f"head{scale}.{branch}"
                    plane=planes[name]
                    for channel in range(channels):
                        addr=resolver(graph,name,y,x,channel)
                        addresses.append(addr)
                        offset=addr-plane["node"]["storage"]["base"]
                        value=int.from_bytes(plane["image"][offset:offset+2],"little")
                        assert value==plane["values"][(y*w+x)*channels+channel]
                        fields.append(value)
                rebuilt_cells.append(base.pack(fields,16))
    assert len(addresses)==84672 and rebuilt_cells==words(HERE/"head_cells112.hex")
    original_packed=words(HERE/"head_cell_addresses224.hex")
    assert all(base.pack(addresses[index*7:index*7+7],32)==value for index,value in enumerate(original_packed))
    base.emit(HERE/"cell_field_addresses32.hex",addresses,32)
    base.save(HERE/"prediction_backing_ranges.json",{"planes":ranges,"plane_count":6,"unused_allocated_bytes":0,
              "read128_rule":"16-byte aligned and entire line contained in one declared allocation; byte0 is lowest address",
              "required_external_condition":"predictions_committed before start and all six planes stable throughout reading",
              "retirement_boundary":"Last source read response consumption is distinct from last output cell acceptance",
              "boundary":"Controlled CPU prediction-plane images only, not actual hardware head producers or DDR visibility proof"})
    sources={**original["source_sha256"],str(HERE/"head_generation_binding.json"):base.sha(HERE/"head_generation_binding.json"),
             str(Path(__file__)):base.sha(Path(__file__)),str(HERE/"PREDICTION_FORMAT.txt"):base.sha(HERE/"PREDICTION_FORMAT.txt")}
    for path in plane_inputs+[HERE/"head_cells112.hex",HERE/"head_cell_addresses224.hex"]:
        sources[str(path)]=base.sha(path)
    closure=hashlib.sha256(json.dumps(sources,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    base.save(HERE/"input_binding.json",{**original,"closure_sha256":closure,"source_sha256":sources,"prediction_phase":True,
              "head_generation_closure_sha256":original["closure_sha256"]})
    tasks=base.read(HERE/"tasks.json")
    tasks["closure_sha256"]=closure
    base.save(HERE/"tasks.json",tasks)
    receipt.update({"closure_sha256":closure,"prediction_planes":6,"prediction_lines160":len(lines),"cell_field_addresses32":len(addresses),
                    "prediction_cells_rebuilt_from_physical_planes":"12096/12096 exact","head_generation_closure_sha256":original["closure_sha256"]})
    base.save(HERE/"verification_receipt.json",receipt)
    base.save(HERE/"prediction_receipt.json",{"status":"PASS","planes":6,"lines":len(lines),"field_addresses":len(addresses),
              "cells":len(rebuilt_cells),"graph_byte_addresses":"All84672 fields checked with original graph resolver",
              "closure_sha256":closure,"boundary":"Controlled CPU head outputs and backing images; no hardware producer or new DDR protocol claim"})
    base.save(HERE/"artifact_manifest.json",{str(path.relative_to(HERE)).replace("\\","/"):base.sha(path)
              for path in HERE.rglob("*") if path.is_file() and path.name!="artifact_manifest.json" and "__pycache__" not in path.parts})
    print(json.dumps(base.read(HERE/"prediction_receipt.json")))


if __name__=="__main__":
    try:
        main()
    except Exception:
        stamp=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
        base.save(HERE/("failure_prediction_"+stamp+".json"),{"status":"FAIL","traceback":traceback.format_exc()})
        raise
