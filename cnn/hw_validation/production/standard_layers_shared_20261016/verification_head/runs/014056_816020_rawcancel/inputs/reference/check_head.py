"""Independent stdlib checks for raw16 tails, graph addresses and HWC7 packing."""
import ast
import hashlib
import json
import math
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parent
PRODUCTION=ROOT.parents[1]


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def words(path):
    return [int(line,16) for line in path.read_text(encoding="ascii").splitlines()]


def main():
    manifest=read(ROOT/"artifact_manifest.json")
    assert all(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==value for name,value in manifest.items())
    binding=read(ROOT/"input_binding.json")
    assert all(hashlib.sha256(Path(name).read_bytes()).hexdigest()==value for name,value in binding["source_sha256"].items())
    graph=read(PRODUCTION/"graph_artifacts/graph.json")
    tree=ast.parse((PRODUCTION/"graph.py").read_text(encoding="utf-8"))
    function=next(node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name=="resolve_byte_address")
    namespace={"math":math,"Any":Any}
    exec(compile(ast.Module(body=[function],type_ignores=[]),"graph.py","exec"),namespace)
    resolve=namespace["resolve_byte_address"]
    parameters=read(ROOT/"parameter_responses.json")
    assert len(parameters)==2118
    for row in parameters:
        if row["layer_id"] in (85,88,93,96,101,104):
            assert row["quant248"]>>210==0
            if row["channel"]==3 or row["layer_id"] in (85,93,101):
                assert row["weight192"]>>128==0
                assert (row["quant248"]>>64)&0xffffffff==0
                assert (row["quant248"]>>160)&0xffffffff==0
                assert (row["quant248"]>>204)&63==0
        if row["window"]==3:
            assert row["weight192"]>>64==0
    for layer in (83,86,91,94,99,102):
        for channel in range(48):
            selected=[row for row in parameters if row["layer_id"]==layer and row["channel"]==channel]
            assert len(selected)==4 and len({row["quant248"] for row in selected})==1
            assert {(row["window"],row["group"],row["slot"]) for row in selected}=={(5,0,0),(5,1,1),(3,0,2),(3,1,3)}
    checked=0
    for layer in read(ROOT/"tasks.json")["layers"]:
        assert layer["input_source"]["synthetic"] is True and layer["input_source"]["continuous_prefix"] is False
        if not layer["output_int16"]:
            continue
        folder=ROOT/layer["name"]
        assert "post_multiplier" not in read(folder/"parameters.json")
        assert words(folder/"expected_hwc_pre.hex")==words(folder/"expected_hwc_post.hex")
        assert not any(words(folder/"expected_hwc_silu.hex"))
        h,w,c=layer["output_shape_hwc"]
        expected=words(folder/"expected_hwc_post.hex")
        for case in layer["cases"]:
            expected_writes=[]
            for task in read(ROOT/case["directory"]/"tasks.json"):
                assert task["output_int16"]==1 and task["post"]==task["pre"]
                assert task["mask"]==(3 if c==2 or task["channel"]==3 else 7)
                for lane in range(3):
                    if not task["mask"]&(1<<lane):
                        assert task["post"][lane]==0
                        continue
                    y,x=case["tile_y"]+task["r"],case["tile_x"]+task["c"]
                    assert y<h
                    channel=task["channel"]+lane
                    data=expected[(y*w+x)*c+channel]
                    address=resolve(graph,layer["name"],y,x,channel)
                    assert task["addresses"][lane]==address and task["post"][lane]&65535==data
                    expected_writes.append((address<<16)|data)
                    checked+=1
            assert words(ROOT/case["directory"]/"output_writes48.hex")==expected_writes
    cells=words(ROOT/"head_cells112.hex")
    cell_addresses=words(ROOT/"head_cell_addresses224.hex")
    assert len(cells)==len(cell_addresses)==12096
    offset=0
    for head,h,w in ((2,72,128),(3,36,64),(4,18,32)):
        reg=words(ROOT/f"head{head}.reg_out/expected_hwc_post.hex")
        cls=words(ROOT/f"head{head}.cls_out/expected_hwc_post.hex")
        for pixel in range(h*w):
            y,x=divmod(pixel,w)
            expected=reg[pixel*5:pixel*5+5]+cls[pixel*2:pixel*2+2]
            assert [(cells[offset]>>(lane*16))&65535 for lane in range(7)]==expected
            addresses=[resolve(graph,f"head{head}.reg_out",y,x,lane) for lane in range(5)]
            addresses+=[resolve(graph,f"head{head}.cls_out",y,x,lane) for lane in range(2)]
            assert [(cell_addresses[offset]>>(lane*32))&0xffffffff for lane in range(7)]==addresses
            offset+=1
    print(json.dumps({"status":"PASS","artifact_hashes":len(manifest),"input_hashes":len(binding["source_sha256"]),
                      "raw16_active_tile_outputs":checked,"head_cells112":offset,"raw_tail_quant_and_masks":"PASS"}))


if __name__=="__main__":
    main()
