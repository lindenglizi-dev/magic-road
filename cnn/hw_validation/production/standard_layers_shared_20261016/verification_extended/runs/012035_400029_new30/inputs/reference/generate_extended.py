"""Extend the frozen tile reference with six fixed real-G10 layers.

Only imports the original generator; writes exclusively reference_extended.
Synthetic PAN inputs are controlled layer tests, never a continuous prefix.
"""
from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
OLD = HERE.parent / "reference"
PRODUCTION = HERE.parents[1]
PROJECT = PRODUCTION.parents[2]
spec = importlib.util.spec_from_file_location("frozen_standard_reference", OLD / "generate_reference.py")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
base.HERE = HERE  # Redirect only generated file locations; frozen source stays unchanged.


def functions(path, names, namespace):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    selected = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in names]
    assert {node.name for node in selected} == set(names)
    exec(compile(ast.Module(body=selected, type_ignores=[]), str(path), "exec"), namespace)
    return namespace


def synthetic(shape, layer):
    y, x, c = np.indices(shape, dtype=np.int64)
    return ((y*37 + x*19 + c*53 + layer*11 + (y*x)%251)%256 - 128).astype(np.int8)


def backing_input(root, node, source, views, graph, resolver, address):
    """Scatter logical input bytes into actual backing stores, with explicit zeros."""
    allocations = []
    for view in views:
        storage = next(row["storage"] for row in graph["nodes"]
                       if row.get("storage", {}).get("base") == view["base"])
        if not any(row["base"] == storage["base"] for row in allocations):
            allocations.append({**storage, "data": bytearray(storage["allocated_bytes"])})
    checked = 0
    for y, x, channel in np.ndindex(source.shape):
        actual = address(node, y, x, channel)
        expected = resolver(graph, node["output"], y, x, channel)
        assert actual == expected, (node["output"], y, x, channel, actual, expected)
        store = next(row for row in allocations if row["base"] <= actual < row["end"])
        store["data"][actual-store["base"]] = int(source[y,x,channel]) & 255
        checked += 1
    # This is a testbench image, never a proposed private hardware RAM.
    base.emit(root / "input_physical40.hex", ((row["base"]+offset)<<8 | value
              for row in sorted(allocations,key=lambda row:row["base"])
              for offset,value in enumerate(row["data"])),40)
    base.emit(root / "input_lines160.hex", ((row["base"]+offset)<<128 | int.from_bytes(row["data"][offset:offset+16],"little")
              for row in sorted(allocations,key=lambda row:row["base"])
              for offset in range(0,len(row["data"]),16)),160)
    ranges = [{key:value for key,value in row.items() if key != "data"} for row in allocations]
    base.save(root / "input_backing_ranges.json",{"source_tensor":node["output"],"source_views":views,
              "allocations":ranges,"unused_parent_channels_and_padding":0,
              "read128_rule":"Require address%16==0 and [address,address+16) fully inside one allocation; byte0 is lowest address"})
    assert all(row["base"]%16==0 and row["allocated_bytes"]%16==0 for row in allocations)
    return checked


def main():
    immutable = base.read(OLD / "artifact_manifest.json")
    assert all(base.sha(OLD/name)==want for name,want in immutable.items())
    graph_path = PRODUCTION / "graph_artifacts/graph.json"
    remaining_path = PRODUCTION / "rom_two_client_20261015/remaining_layers.json"
    manifest_path = base.PACKAGE / "manifest.json"
    payload_path = base.PACKAGE / "numeric_test.bin"
    graph, remaining, manifest = map(base.read,(graph_path,remaining_path,manifest_path))
    assert base.sha(graph_path)==remaining["graph_sha256"]
    assert base.sha(manifest_path)==remaining["manifest_sha256"]
    assert base.sha(payload_path)==manifest["payload_sha256"]==base.PAYLOAD
    payload=payload_path.read_bytes()
    segments={row["name"]:row for row in manifest["segments"]}
    lut=segments["shared.silu"]
    lut_bytes=payload[lut["offset"]:lut["offset"]+lut["length"]]
    assert hashlib.sha256(lut_bytes).hexdigest()==lut["sha256"]
    assert np.array_equal(np.frombuffer(lut_bytes,dtype="<i2"),base.tables()["silu"])
    trained=PRODUCTION/"trained_integer.py"
    conv=functions(trained,["conv_exact"],{"np":np})["conv_exact"]
    family=PRODUCTION/"csp_family_layer_scheduled_20261015/reference/generate_reference.py"
    maps=functions(family,["graph_index","storage_of","source_views","physical_address","view_for_channel"],{"math":math})
    graph_source=PRODUCTION/"graph.py"
    resolver=functions(graph_source,["resolve_byte_address"],{"math":math,"Any":Any})["resolve_byte_address"]
    nodes,producers=maps["graph_index"](graph)
    original_address=base.address

    def address(node,y,x,channel):
        if "_source_views" not in node:
            return original_address(node,y,x,channel)
        view=maps["view_for_channel"](node["_source_views"],channel)
        h,w,_=node["output_shape_hwc"]
        assert 0<=y<h and 0<=x<w
        return maps["physical_address"](view,h,w,y,x,channel)

    base.address=address
    sppf_root=PRODUCTION/"feature_blocks_shared_20261015/reference"
    sppf_manifest_path=sppf_root/"sppf_manifest.json"
    sppf_source=sppf_root/"sppf/sppf.out.conv.post.npy"
    sppf_manifest=base.read(sppf_manifest_path)
    assert sppf_manifest["payload_sha256"]==base.PAYLOAD
    assert base.sha(sppf_source)==sppf_manifest["artifacts"]["sppf/sppf.out.conv.post.npy"]
    sources={46:np.load(sppf_source,allow_pickle=False)}
    input_sources={46:{"synthetic":False,"kind":"existing_cpu_real_road_tensor","path":str(sppf_source),"sha256":base.sha(sppf_source)}}
    layers,parameter_rows=[],[]
    checked_bytes=0
    for layer_id in (46,55,64,65,73,74):
        node=next(row for row in remaining["layers"] if row["graph_index"]==layer_id)
        assert graph["nodes"][layer_id]["name"]==node["name"]
        if layer_id not in sources:
            sources[layer_id]=synthetic(node["input_shape_hwc"],layer_id)
            input_sources[layer_id]={"synthetic":True,"kind":"deterministic_layer_input",
               "formula":"((y*37+x*19+c*53+layer_id*11+(y*x)%251)%256)-128",
               "residual_storage_assumption":"concat right branch is an already-fused stored tensor; this controlled input neither computes nor proves its producer"}
        source=sources[layer_id]
        provenance={**input_sources[layer_id],"continuous_prefix":False,"tensor":node["inputs"][0],
                    "input_bytes_sha256":hashlib.sha256(source.tobytes()).hexdigest()}
        params=base.parameters(node,payload,segments)
        result=base.execute(node,source,params,conv)
        root=HERE/node["name"]
        root.mkdir(parents=True,exist_ok=True)
        base.emit(root/"input_hwc8.hex",source.ravel(),8)
        for field,bits in (("acc",32),("pre",16),("silu",16),("post",8)):
            base.emit(root/("expected_hwc_"+field+".hex"),result[field].ravel(),bits)
        base.save(root/"input_source.json",provenance)
        base.save(root/"parameters.json",{name:value.tolist() for name,value in params.items()})
        views=maps["source_views"](node["inputs"][0],node["input_shape_hwc"][2],nodes,producers)
        source_node={"output":node["inputs"][0],"output_shape_hwc":node["input_shape_hwc"],"_source_views":views}
        checked_bytes+=backing_input(root,source_node,source,views,graph,resolver,address)
        cases=base.schedule(node,source_node,source,params,result,root)
        for row in base.read(HERE/cases[0]["directory"]/"parameter_responses.json"):
            parameter_rows.append({"layer_id":layer_id,**row})
        layers.append({"layer_id":layer_id,"name":node["name"],"input_shape_hwc":node["input_shape_hwc"],
                       "output_shape_hwc":node["output_shape_hwc"],"storage":node["storage"],"source_views":views,
                       "input_source":provenance,"cases":cases})
        if layer_id in (64,73):
            sources[layer_id+1]=result["post"]
            input_sources[layer_id+1]={"synthetic":True,"kind":"cpu_output_of_synthetic_input_layer",
               "producer_layer_id":layer_id,"continuous_prefix":False}
        print(f"layer {layer_id} {node['name']}: five tiles checked; synthetic={provenance['synthetic']}",flush=True)
    assert len(parameter_rows)==840 and len({(row["layer_id"],row["channel"],row["window"],row["group"]) for row in parameter_rows})==840
    base.save(HERE/"parameter_responses.json",parameter_rows)
    base.emit(HERE/"parameter_requests22.hex",((row["layer_id"]<<15)|(row["channel"]<<8)|(row["window"]<<5)|row["group"] for row in parameter_rows),22)
    base.emit(HERE/"parameter_weight192.hex",(row["weight192"] for row in parameter_rows),192)
    base.emit(HERE/"parameter_quant248.hex",(row["quant248"] for row in parameter_rows),248)
    inputs=[Path(__file__),HERE/"FORMAT.txt",OLD/"generate_reference.py",OLD/"artifact_manifest.json",graph_path,
            remaining_path,manifest_path,payload_path,trained,family,graph_source,PROJECT/"cnn/integer.py",
            sppf_manifest_path,sppf_source,Path(sys.executable)]
    inputs+=list({Path(module.__file__) for name,module in sys.modules.items()
                  if name.startswith("numpy") and getattr(module,"__file__",None)})
    binding={str(path):base.sha(path) for path in inputs}
    closure=hashlib.sha256(json.dumps(binding,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    boundary="Six CPU layer references; one existing real-road input, five synthetic or synthetic-derived inputs; no continuous prefix, RTL, DDR, physical mapping, timing, full-network, QAT or accuracy claim"
    base.save(HERE/"tasks.json",{"status":"CPU_REFERENCE_ONLY_REAL_G10_PARAMETERS_MIXED_INPUT_PROVENANCE",
              "payload_sha256":base.PAYLOAD,"closure_sha256":closure,"continuous_prefix":False,"layers":layers})
    base.save(HERE/"input_binding.json",{"closure_sha256":closure,"source_sha256":binding,"python":sys.version,"numpy":np.__version__,"boundary":boundary})
    receipt={"status":"PASS","layers":6,"tiles":30,"tasks":sum(case["tasks"] for row in layers for case in row["cases"]),
             "groups":sum(case["groups"] for row in layers for case in row["cases"]),"parameter_responses":840,
             "graph_source_bytes_checked":checked_bytes,"scalar_oracle":"Every emitted tile/channel matches cnn.integer.conv2d; each sparse signed33 reduction matches conv_exact",
             "frozen_reference_artifacts_unchanged":len(immutable),"closure_sha256":closure,"boundary":boundary}
    assert all(base.sha(OLD/name)==want for name,want in immutable.items())
    base.save(HERE/"verification_receipt.json",receipt)
    base.save(HERE/"artifact_manifest.json",{str(path.relative_to(HERE)).replace("\\","/"):base.sha(path)
              for path in HERE.rglob("*") if path.is_file() and path.name!="artifact_manifest.json" and "__pycache__" not in path.parts})
    print(json.dumps(receipt))


if __name__=="__main__":
    main()
