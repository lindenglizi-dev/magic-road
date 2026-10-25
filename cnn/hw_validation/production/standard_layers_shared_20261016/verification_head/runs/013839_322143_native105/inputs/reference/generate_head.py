"""Fixed 21-head-layer CPU reference; controlled standalone head inputs only.

Reuses frozen integer, parameter decoder, convolution and backing-store helpers.
DW changes only its spatial packing to stride1; raw predictions use pre16 only.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import math
import sys
import traceback
from pathlib import Path
from typing import Any

import numpy as np

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
PRODUCTION=HERE.parents[1]
PROJECT=PRODUCTION.parents[2]
OLD=HERE.parent/"reference"
EXTENDED=HERE.parent/"reference_extended"
spec=importlib.util.spec_from_file_location("frozen_extended_reference",EXTENDED/"generate_extended.py")
extended=importlib.util.module_from_spec(spec)
spec.loader.exec_module(extended)
base=extended.base
base.HERE=HERE


def quant(params,channels):
    def values(field):
        return [int(params[field][channel]) if channel is not None else 0 for channel in channels]
    return (base.pack(values("bias"),32) | base.pack(values("pre_multiplier"),32)<<96
            | base.pack(values("pre_shift"),6)<<192
            | int(params.get("post_multiplier",[0])[0])<<210
            | int(params.get("post_shift",[0])[0])<<242)


def execute(node,source,params,conv):
    if node["dtype"]=="int8":
        return base.execute(node,source,params,conv)
    assert node["dtype"]=="int16_q7_8" and "post_multiplier" not in params and "post_shift" not in params
    acc=conv(source,params["weights"],params["bias"],node["stride"][0],node["padding"][0],node["groups"])
    pre=base.requantize(acc,params["pre_multiplier"],params["pre_shift"],-32768,32767).astype(np.int16)
    return {"acc":acc,"pre":pre,"silu":np.zeros_like(pre),"post":pre.copy()}


def schedule(node,source_node,source,params,expected,root,address):
    """Original fixed task/trace structure with stride1 DW and raw16 output tails."""
    h,w,cout=node["output_shape_hwc"]
    cin=node["input_shape_hwc"][2]
    dw=node["groups"]>1
    raw=node["dtype"]=="int16_q7_8"
    assert node["stride"]==[1,1] and cin%8==0
    origins=[(0,0),(0,w-4),(((h-1)//4)*4,0),(((h-1)//4)*4,w-4),((h//8)*4,(w//8)*4)]
    cases=[]
    for case_id,(y0,x0) in enumerate(origins):
        case=root/f"tile_{case_id}_y{y0}_x{x0}"
        case.mkdir(parents=True,exist_ok=True)
        tasks,groups,trace,weights,quants=[],[],[],[],[]
        byte_writes,byte_reads,weight_writes,weight_reads,fill_addresses=[],[],[],[],[]
        for channel in (range(cin) if dw else range(0,cout,3)):
            channels=[channel]*3 if dw else [channel+lane if channel+lane<cout else None for lane in range(3)]
            if dw:
                store=[int(source[y0-1+r,x0-1+c,channel]) if 0<=y0-1+r<h and 0<=x0-1+c<w else 0
                       for r in range(6) for c in range(6)]
                banks=[]
                for window in (5,3):
                    for group in range(2):
                        sparse=[]
                        for lane in range(3):
                            for k in range(8):
                                n=group*8+k
                                ky,ux=divmod(n,window)
                                kx=ux-lane
                                sparse.append(int(params["weights"][channel,0,ky,kx])
                                              if n<3*window and 0<=kx<3 and (window==5 or lane==0) else 0)
                        banks.append({"window":window,"group":group,"slot":len(banks),"weight192":base.pack(sparse,8)})
            else:
                store=[int(source[y0+r,x0+c,k]) if y0+r<h else 0
                       for r in range(4) for c in range(4) for k in range(cin)]
                banks=[{"window":0,"group":group,"slot":group,
                        "weight192":base.pack([int(params["weights"][oc,group*8+k,0,0]) if oc is not None else 0
                                               for oc in channels for k in range(8)],8)} for group in range(cin//8)]
            assert len(store)<=3072 and len(banks)<=24
            q=quant(params,channels)
            quants.append(q)
            if dw or channel==0:
                for local,value in enumerate(store):
                    trace.append(("byte",1,local,value&255,0))
                    byte_writes.append((local<<8)|(value&255))
                    if dw:
                        fy,fx,fc=y0-1+local//6,x0-1+local%6,channel
                    else:
                        pixel,fc=divmod(local,cin)
                        fy,fx=y0+pixel//4,x0+pixel%4
                    fill_addresses.append(address(source_node,fy,fx,fc) if 0<=fy<h and 0<=fx<w else 0xffffffff)
            for bank in banks:
                trace.append(("weight",1,bank["slot"],bank["weight192"],0))
                weight_writes.append((bank["slot"]<<192)|bank["weight192"])
                weights.append({"channel":channel,**bank,"quant248":q})
            valid_rows=min(4,h-y0)
            # Existing scalar convolution independently checks every emitted tile/channel.
            if dw:
                scalar=base.conv2d(np.array(store,dtype=np.int8).reshape(6,6,1),
                                  params["weights"][channel:channel+1],params["bias"][channel:channel+1])
                assert np.array_equal(scalar[:valid_rows,:,0],expected["acc"][y0:y0+valid_rows,x0:x0+4,channel])
            else:
                active=min(3,cout-channel)
                scalar=base.conv2d(np.array(store,dtype=np.int8).reshape(4,4,cin),
                                  params["weights"][channel:channel+active],params["bias"][channel:channel+active])
                assert np.array_equal(scalar[:valid_rows],expected["acc"][y0:y0+valid_rows,x0:x0+4,channel:channel+active])
            for r,c in ((r,c) for r in range(valid_rows) for c in ((0,3) if dw else range(4))):
                window=(5 if c==0 else 3) if dw else 0
                active=(3 if c==0 else 1) if dw else min(3,cout-channel)
                task_id=len(tasks)
                dst=[address(node,y0+r,x0+c+(lane if dw else 0),channel if dw else channels[lane]) if lane<active else 0 for lane in range(3)]
                outputs=[[int(expected[field][y0+r,x0+c+(lane if dw else 0),channel if dw else channels[lane]]) if lane<active else 0
                          for lane in range(3)] for field in ("acc","pre","silu","post")]
                task={"task":task_id,"channel":channel,"r":r,"c":c,"window":window,
                      "mask":(1<<active)-1,"quant248":q,"addresses":dst,"output_int16":int(raw),
                      **dict(zip(("acc","pre","silu","post"),outputs)),"first_group":len(groups)}
                running=[int(params["bias"][channels[lane]]) if lane<active else 0 for lane in range(3)]
                selected=[bank for bank in banks if bank["window"]==window]
                for index,bank in enumerate(selected):
                    count=min(8,(3*window if dw else cin)-bank["group"]*8)
                    offsets=[]
                    for k in range(count):
                        n=bank["group"]*8+k
                        if dw:
                            ky,ux=divmod(n,window)
                            offsets.append((r+ky)*6+c+ux)
                        else:
                            offsets.append((r*4+c)*cin+n)
                    values=[store[offset] for offset in offsets]+[0]*(8-count)
                    trace.append(("weight",0,bank["slot"],0,bank["weight192"]))
                    weight_reads.append((bank["slot"]<<192)|bank["weight192"])
                    for offset in offsets:
                        trace.append(("byte",0,offset,0,store[offset]&255))
                        byte_reads.append((offset<<8)|(store[offset]&255))
                    raw_weight=bank["weight192"].to_bytes(24,"little")
                    for lane in range(active):
                        running[lane]+=sum(values[k]*(raw_weight[lane*8+k] if raw_weight[lane*8+k]<128 else raw_weight[lane*8+k]-256) for k in range(count))
                        assert -(1<<32)<=running[lane]<(1<<32)
                    groups.append({"task":task_id,"slot":bank["slot"],"first":int(index==0),"last":int(index==len(selected)-1),
                                   "mask":(1<<count)-1,"activation64":base.pack(values,8),"weight192":bank["weight192"],
                                   "offsets":offsets,"acc33":running.copy()})
                assert running==outputs[0]
                if raw:
                    assert outputs[3]==outputs[1] and q>>210==0
                task["group_count"]=len(selected)
                tasks.append(task)
        memory={"byte":{},"weight":{}}
        for port,write,offset,data,response in trace:
            assert 0<=offset<(3072 if port=="byte" else 24)
            if write:
                assert response==0
                memory[port][offset]=data
            else:
                assert data==0 and offset in memory[port] and memory[port][offset]==response
        assert len({dst for task in tasks for lane,dst in enumerate(task["addresses"]) if task["mask"]&(1<<lane)})==valid_rows*4*cout
        base.save(case/"tasks.json",tasks)
        base.save(case/"parameter_responses.json",weights)
        for field,bits in (("activation64",64),("weight192",192),("first",1),("last",1),("mask",8),("slot",5)):
            base.emit(case/("group_"+field+".hex"),(row[field] for row in groups),bits)
        base.emit(case/"group_offsets96.hex",(base.pack(row["offsets"]+[0]*(8-len(row["offsets"])),12) for row in groups),96)
        base.emit(case/"group_acc99.hex",(base.pack(row["acc33"],33) for row in groups),99)
        for name,values,bits in (("weight_writes197",weight_writes,197),("weight_reads197",weight_reads,197),
                                 ("byte_writes20",byte_writes,20),("byte_reads20",byte_reads,20),
                                 ("fill_source_addresses32",fill_addresses,32),("parameter_quant248",quants,248)):
            base.emit(case/(name+".hex"),values,bits)
        base.emit(case/"output_writes48.hex",((row["addresses"][lane]<<16)|(row["post"][lane]&(65535 if raw else 255))
                  for row in tasks for lane in range(3) if row["mask"]&(1<<lane)),48)
        base.emit(case/"task_output48.hex",(base.pack([value&(65535 if raw else 255) for value in row["post"]],16) for row in tasks),48)
        base.emit(case/"task_output_int16.hex",(row["output_int16"] for row in tasks),1)
        for field,bits in (("acc",32),("pre",16),("silu",16),("post",16 if raw else 8),("addresses",32),("mask",1)):
            base.emit(case/("task_"+field+".hex"),(row[field] if field=="mask" else base.pack(row[field],bits) for row in tasks),3 if field=="mask" else bits*3)
        with (case/"wif1_transactions.csv").open("w",encoding="ascii",newline="") as stream:
            writer=base.csv.writer(stream)
            writer.writerow(["sequence","channel","write","address_or_group","request_hex","response_hex","error"])
            writer.writerows((n,*row[:3],f"{row[3]:x}",f"{row[4]:x}",0) for n,row in enumerate(trace))
        cases.append({"case":case_id,"tile_y":y0,"tile_x":x0,"valid_rows":valid_rows,"tasks":len(tasks),"groups":len(groups),
                      "output_int16":int(raw),"directory":str(case.relative_to(HERE)).replace("\\","/"),"wif1_transactions":len(trace)})
    return cases


def main():
    frozen={directory:base.read(directory/"artifact_manifest.json") for directory in (OLD,EXTENDED)}
    for directory,manifest in frozen.items():
        assert all(base.sha(directory/name)==want for name,want in manifest.items())
    graph_path=PRODUCTION/"graph_artifacts/graph.json"
    remaining_path=PRODUCTION/"rom_two_client_20261015/remaining_layers.json"
    manifest_path=base.PACKAGE/"manifest.json"
    payload_path=base.PACKAGE/"numeric_test.bin"
    graph,remaining,manifest=map(base.read,(graph_path,remaining_path,manifest_path))
    assert base.sha(graph_path)==remaining["graph_sha256"] and base.sha(manifest_path)==remaining["manifest_sha256"]
    assert base.sha(payload_path)==manifest["payload_sha256"]==base.PAYLOAD
    payload=payload_path.read_bytes()
    segments={row["name"]:row for row in manifest["segments"]}
    lut=segments["shared.silu"]
    assert np.array_equal(np.frombuffer(payload[lut["offset"]:lut["offset"]+lut["length"]],dtype="<i2"),base.tables()["silu"])
    trained=PRODUCTION/"trained_integer.py"
    conv=extended.functions(trained,["conv_exact"],{"np":np})["conv_exact"]
    family=PRODUCTION/"csp_family_layer_scheduled_20261015/reference/generate_reference.py"
    maps=extended.functions(family,["graph_index","storage_of","source_views","physical_address","view_for_channel"],{"math":math})
    graph_source=PRODUCTION/"graph.py"
    resolver=extended.functions(graph_source,["resolve_byte_address"],{"math":math,"Any":Any})["resolve_byte_address"]
    nodes,producers=maps["graph_index"](graph)

    def address(node,y,x,channel):
        if "_source_views" in node:
            view=maps["view_for_channel"](node["_source_views"],channel)
            h,w,_=node["output_shape_hwc"]
            assert 0<=y<h and 0<=x<w
            return maps["physical_address"](view,h,w,y,x,channel)
        h,w,c=node["output_shape_hwc"]
        assert 0<=y<h and 0<=x<w and 0<=channel<c
        pixel=((y//4)*((w+3)//4)+x//4)*16+(y%4)*4+x%4
        result=node["storage"]["base"]+(pixel*c+channel)*node["storage"]["bytes_per_element"]
        assert result==resolver(graph,node["name"],y,x,channel)
        return result

    layers,parameter_rows,heads=[],[],{}
    checked_bytes=0
    for head,stem_id in ((4,98),(3,90),(2,82)):
        first=next(row for row in remaining["layers"] if row["graph_index"]==stem_id)
        values={first["inputs"][0]:extended.synthetic(first["input_shape_hwc"],stem_id)}
        for layer_id in range(stem_id,stem_id+7):
            node=next(row for row in remaining["layers"] if row["graph_index"]==layer_id)
            assert graph["nodes"][layer_id]["name"]==node["name"]
            source=values[node["inputs"][0]]
            params=base.parameters(node,payload,segments)
            result=execute(node,source,params,conv)
            values[node["name"]]=result["post"]
            raw=node["dtype"]=="int16_q7_8"
            root=HERE/node["name"]
            root.mkdir(parents=True,exist_ok=True)
            base.emit(root/"input_hwc8.hex",source.ravel(),8)
            for field,bits in (("acc",32),("pre",16),("silu",16),("post",16 if raw else 8)):
                base.emit(root/("expected_hwc_"+field+".hex"),result[field].ravel(),bits)
            provenance={"synthetic":True,"continuous_prefix":False,"standalone_cpu_head_prefix":True,
                        "kind":"controlled_fused_pan_input" if layer_id==stem_id else "cpu_head_prefix_output",
                        "head":head,"seed_layer_id":stem_id,"tensor":node["inputs"][0],
                        "formula":"((y*37+x*19+c*53+stem_layer_id*11+(y*x)%251)%256)-128",
                        "input_bytes_sha256":hashlib.sha256(source.tobytes()).hexdigest(),
                        "boundary":"No actual PAN/residual producer or continuous backbone execution is claimed"}
            base.save(root/"input_source.json",provenance)
            base.save(root/"parameters.json",{name:value.tolist() for name,value in params.items()})
            views=maps["source_views"](node["inputs"][0],node["input_shape_hwc"][2],nodes,producers)
            source_node={"output":node["inputs"][0],"output_shape_hwc":node["input_shape_hwc"],"_source_views":views}
            # The existing backing-image helper checks every logical byte against graph.py.
            checked_bytes+=extended.backing_input(root,source_node,source,views,graph,resolver,address)
            cases=schedule(node,source_node,source,params,result,root,address)
            for row in base.read(HERE/cases[0]["directory"]/"parameter_responses.json"):
                parameter_rows.append({"layer_id":layer_id,**row})
            layers.append({"layer_id":layer_id,"name":node["name"],"input_shape_hwc":node["input_shape_hwc"],
                           "output_shape_hwc":node["output_shape_hwc"],"storage":node["storage"],"source_views":views,
                           "input_source":provenance,"output_int16":int(raw),"activate":int(not raw),"cases":cases})
            print(f"layer {layer_id} {node['name']}: five tiles checked; output_int16={int(raw)}",flush=True)
        heads[head]={"cells":np.concatenate((values[f"head{head}.reg_out"],values[f"head{head}.cls_out"]),axis=2),
                     "reg_node":nodes[f"head{head}.reg_out"],"cls_node":nodes[f"head{head}.cls_out"]}
    cell_words,cell_addresses,cell_index=[],[],[]
    for head,stride in ((2,4),(3,8),(4,16)):
        data=heads[head]["cells"]
        h,w,channels=data.shape
        assert channels==7 and data.dtype==np.int16
        start=len(cell_words)
        for y,x in np.ndindex(h,w):
            cell_words.append(base.pack(data[y,x],16))
            addresses=[address(heads[head]["reg_node"],y,x,c) for c in range(5)]+[address(heads[head]["cls_node"],y,x,c) for c in range(2)]
            assert all(addr%2==0 for addr in addresses)
            cell_addresses.append(base.pack(addresses,32))
        cell_index.append({"head":head,"stride":stride,"height":h,"width":w,"first_cell":start,"cells":h*w,
                           "order":["tx","ty","tw","th","objectness","person_logit","vehicle_logit"]})
    assert len(cell_words)==12096
    base.emit(HERE/"head_cells112.hex",cell_words,112)
    base.emit(HERE/"head_cell_addresses224.hex",cell_addresses,224)
    base.save(HERE/"head_cells_index.json",{"cells":12096,"bits_per_cell":112,"order":"S4 then S8 then S16; row-major y/x; first component low16","scales":cell_index,"synthetic":True,"continuous_prefix":False})
    expected_parameters=sum(row["output_shape_hwc"][2]*4 if row["groups"]>1 else
                            ((row["output_shape_hwc"][2]+2)//3)*(row["input_shape_hwc"][2]//8)
                            for row in remaining["layers"] if row["family"]=="head")
    assert expected_parameters==2118
    assert len(parameter_rows)==expected_parameters and len({(row["layer_id"],row["channel"],row["window"],row["group"]) for row in parameter_rows})==expected_parameters
    base.save(HERE/"parameter_responses.json",parameter_rows)
    base.emit(HERE/"parameter_requests22.hex",((row["layer_id"]<<15)|(row["channel"]<<8)|(row["window"]<<5)|row["group"] for row in parameter_rows),22)
    base.emit(HERE/"parameter_weight192.hex",(row["weight192"] for row in parameter_rows),192)
    base.emit(HERE/"parameter_quant248.hex",(row["quant248"] for row in parameter_rows),248)
    inputs=[Path(__file__),HERE/"FORMAT.txt",OLD/"generate_reference.py",OLD/"artifact_manifest.json",EXTENDED/"generate_extended.py",
            EXTENDED/"artifact_manifest.json",graph_path,remaining_path,manifest_path,payload_path,trained,family,graph_source,
            PROJECT/"cnn/integer.py",Path(sys.executable)]
    inputs+=list({Path(module.__file__) for name,module in sys.modules.items() if name.startswith("numpy") and getattr(module,"__file__",None)})
    binding={str(path):base.sha(path) for path in inputs}
    closure=hashlib.sha256(json.dumps(binding,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    boundary="21 CPU standalone head layers from synthetic fused-PAN inputs; no actual PAN/backbone producer, RTL, DDR, physical mapping, timing, deployment QAT or accuracy acceptance"
    base.save(HERE/"tasks.json",{"status":"CPU_REFERENCE_ONLY_REAL_G10_HEAD_PARAMETERS_CONTROLLED_INPUTS","payload_sha256":base.PAYLOAD,
              "closure_sha256":closure,"continuous_prefix":False,"layers":layers})
    base.save(HERE/"input_binding.json",{"closure_sha256":closure,"source_sha256":binding,"python":sys.version,"numpy":np.__version__,"boundary":boundary})
    receipt={"status":"PASS","layers":21,"tiles":105,"tasks":sum(case["tasks"] for row in layers for case in row["cases"]),
             "groups":sum(case["groups"] for row in layers for case in row["cases"]),"parameter_responses":len(parameter_rows),
             "head_cells112":len(cell_words),"graph_source_bytes_checked":checked_bytes,"closure_sha256":closure,"boundary":boundary,
             "scalar_oracle":"Every emitted tile/channel matches original conv2d; every sparse signed33 reduction matches conv_exact",
             "frozen_artifacts_unchanged":{directory.name:len(manifest) for directory,manifest in frozen.items()}}
    for directory,manifest in frozen.items():
        assert all(base.sha(directory/name)==want for name,want in manifest.items())
    base.save(HERE/"verification_receipt.json",receipt)
    base.save(HERE/"artifact_manifest.json",{str(path.relative_to(HERE)).replace("\\","/"):base.sha(path)
              for path in HERE.rglob("*") if path.is_file() and path.name!="artifact_manifest.json" and "__pycache__" not in path.parts})
    print(json.dumps(receipt))


if __name__=="__main__":
    try:
        main()
    except Exception:
        stamp=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
        base.save(HERE/("failure_"+stamp+".json"),{"status":"FAIL","traceback":traceback.format_exc()})
        raise
